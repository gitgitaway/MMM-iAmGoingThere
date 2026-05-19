/*
 * node_helper.js – MMM-iAmGoingThere
 * Orchestrates FlightAwareService, WeatherService, and FileSystemProvider.
 */

const NodeHelper          = require("node_helper");
const fs                  = require("fs");
const path                = require("path");
const https               = require("https");
const FlightAwareService  = require("./services/FlightAwareService");
const WeatherService      = require("./services/WeatherService");
const FileSystemProvider  = require("./services/FileSystemProvider");

module.exports = NodeHelper.create({

  /* ───────────────────────── LIFECYCLE ────────────────────────────────── */
  start () {
    this.config                  = null;
    this.flightLegs              = [];
    this.pollTimer               = null;
    this.tripCompleteTime        = null;
    this._manualVisitedCountries = [];
    this._flightAware = new FlightAwareService(this.name);
    this._weather     = new WeatherService(this.name, path.join(__dirname, "cache", "weather_cache.json"));
    this._fsp         = new FileSystemProvider(this.name);
    console.log(`[${this.name}] node_helper started`);
  },

  /**
   * SEC-002: Strict Path Validation
   * Ensures the resolved path stays within the module directory.
   * @param {string} userPath The path provided in config
   * @param {string} defaultRelPath Fallback relative path
   * @returns {string} Absolute validated path
   */
  validatePath (userPath, defaultRelPath) {
    const base = path.resolve(__dirname);
    let resolved = path.resolve(__dirname, userPath || defaultRelPath);
    if (!resolved.startsWith(base)) {
      console.warn(`[${this.name}] SEC-002: Path traversal attempt detected: ${userPath}. Reverting to default.`);
      resolved = path.resolve(__dirname, defaultRelPath);
    }
    return resolved;
  },

  async socketNotificationReceived (notification, payload) {
    if (notification === "iAGT_REFRESH_WEATHER") {
      const { cityName } = payload;
      const attractionsDir = path.join(__dirname, "data", "attractions");
      const info = await this._fsp.getCityInfo(cityName, false, this._weather, attractionsDir);
      if (info && info.weather) {
        this.sendSocketNotification("iAGT_WEATHER_UPDATE", { cityName, weather: info.weather });
      }
      return;
    }
    if (notification === "iAGT_SAVE_ATTRACTIONS") {
      try {
        const result = await this._fsp.saveAttractionsFile(payload, path.join(__dirname, "documents"));
        this.sendSocketNotification("iAGT_SAVE_OK", result);
      } catch (e) {
        this.sendSocketNotification("iAGT_SAVE_ERROR", { type: "attractions", error: e.message });
      }
      return;
    }
    if (notification === "iAGT_SAVE_FLIGHTS") {
      try {
        const result = await this._fsp.saveFlightsFile(payload, path.join(__dirname, "documents"));
        this.sendSocketNotification("iAGT_SAVE_OK", result);
      } catch (e) {
        this.sendSocketNotification("iAGT_SAVE_ERROR", { type: "flights", error: e.message });
      }
      return;
    }
    if (notification === "iAGT_SAVE_TERMINAL_MAPS") {
      try {
        const result = await this._fsp.saveTerminalMapsFile(payload, path.join(__dirname, "documents"));
        this.sendSocketNotification("iAGT_SAVE_OK", result);
      } catch (e) {
        this.sendSocketNotification("iAGT_SAVE_ERROR", { type: "terminal_maps", error: e.message });
      }
      return;
    }
    if (notification === "iAGT_CLEAR_VISITED_COUNTRIES") {
      this._manualVisitedCountries = [];
      const fp = this.validatePath("data/manual_visited_countries.json", "data/manual_visited_countries.json");
      await this._fsp.saveManualVisitedCountries(fp, this._manualVisitedCountries);
      await this.processScenario();
      return;
    }
    if (notification === "iAGT_TOGGLE_VISITED_COUNTRY") {
      const { iso } = payload;
      if (!iso) return;
      const index = this._manualVisitedCountries.indexOf(iso);
      if (index === -1) {
        this._manualVisitedCountries.push(iso);
      } else {
        this._manualVisitedCountries.splice(index, 1);
      }
      const fp = this.validatePath("data/manual_visited_countries.json", "data/manual_visited_countries.json");
      await this._fsp.saveManualVisitedCountries(fp, this._manualVisitedCountries);
      await this.processScenario();
      return;
    }
    if (notification === "iAGT_GET_FUN_FACT") {
      const { cityName } = payload;
      if (cityName && this.config && this.config.funFactsEnabled) {
        this._fetchFunFact(cityName).catch((e) => {
          console.warn(`[${this.name}] INN-001: Fun fact fetch failed for ${cityName}: ${e.message}`);
        });
      }
      return;
    }
    if (notification === "UPDATE_SCENARIO") {
      this.config.scenario = payload.scenario;
      await this.processScenario();
      return;
    }
    if (notification === "iAGT_CONFIG") {
      this.config = payload;

      // SEC-001: Resolve API key. Priority: Environment Variable > config.js
      const envKey = (process.env.FLIGHTAWARE_API_KEY || "").trim();
      const cfgKey = (this.config.flightAwareApiKey  || "").trim();

      if (envKey) {
        this.config.flightAwareApiKey = envKey;
        if (cfgKey && cfgKey !== envKey) {
          console.log(`[${this.name}] SEC-001: Using FLIGHTAWARE_API_KEY from environment. config.js value ignored.`);
        }
      } else if (cfgKey) {
        this.config.flightAwareApiKey = cfgKey;
        console.warn(`[${this.name}] SEC-001 WARNING: API Key found in config.js. ` +
          `For better security, use the FLIGHTAWARE_API_KEY environment variable instead.`);
      }

      if (!this.config.flightAwareApiKey) {
        console.error(`[${this.name}] No FlightAware API key found. ` +
          `Set FLIGHTAWARE_API_KEY environment variable (highly recommended) ` +
          `or flightAwareApiKey in your config.js module block.`);
      }

      // PER-003: Load core data eagerly; football teams deferred until scenario 6 is active
      await Promise.all([
        this._fsp.loadCitiesData(this.validatePath(this.config.citiesFile, "data/cities.csv")),
        this._fsp.loadAirportsData(this.validatePath("data/airports.csv", "data/airports.csv")),
        this._fsp.loadManualVisitedCountries(this.validatePath("data/manual_visited_countries.json", "data/manual_visited_countries.json"))
          .then(list => { this._manualVisitedCountries = list || []; })
      ]);
      await this.processScenario();
      this.schedulePolling();
    }
  },

  _getEffectiveConfig () {
    const cfg = this.config;
    const scen = cfg.scenario;
    if (cfg.scenarios && cfg.scenarios[scen]) {
      return Object.assign({}, cfg, cfg.scenarios[scen]);
    }
    return cfg;
  },

  /* ─────────────────── SCENARIO PROCESSING ────────────────────────────── */
  async processScenario () {
    const cfg = this._getEffectiveConfig();

    // PER-003: Lazy-load football teams database only when scenario 6 is active
    if (cfg.scenario === 6) {
      await this._fsp.loadFootballTeamsData(this.validatePath("data/football_teams_database.csv", "data/football_teams_database.csv"));
    }

    const cfgFingerprint = JSON.stringify({
      flights:   cfg.flights   || [],
      travelers: cfg.travelers || [],
      overideDate: !!cfg.overideDate
    });
    const cached = await this._loadScenarioCache(this.config.scenario, cfgFingerprint);
    if (cached) {
      console.log(`[${this.name}] Loading Scenario ${this.config.scenario} from cache`);
      this.flightLegs = cached.legs;
      const visitedCountryIsos = this._fsp._buildVisitedCountryIsos(this.flightLegs, this._manualVisitedCountries, this.config.scenario);
      const regionData = await this._fsp._buildRegionData(cfg, path.join(__dirname, "node_modules", "@amcharts", "amcharts5-geodata"));
      this.sendSocketNotification("iAGT_INIT", {
        legs:                this.flightLegs,
        cityInfo:            cached.cityInfo,
        visitedCountryIsos,
        regionData
      });
      return;
    }

    this.flightLegs = [];
    let idx = 0;

    let overrideDateStr = "";
    let overrideTimeStr = "";
    if (cfg.overideDate) {
      const d = new Date(Date.now() + 5 * 60 * 1000);
      overrideDateStr = d.toISOString().split("T")[0];
      overrideTimeStr = d.toTimeString().split(" ")[0].substring(0, 5);
      console.log(`[${this.name}] Overriding all flight takeoff times to: ${overrideDateStr} ${overrideTimeStr}`);
    }

    const mkLeg = (f, travelerName, type) => ({
      id:             `leg_${idx++}`,
      travelerName:   travelerName || f.travelerName || "Traveler",
      flightNumber:   f.flightNumber   || "",
      departureDate:  cfg.overideDate ? overrideDateStr : (f.departureDate  || ""),
      departureTime:  cfg.overideDate ? overrideTimeStr : (f.departuretime || f.departureTime  || ""),
      from:           this._fsp.resolveAirport(f.from) || null,
      to:             this._fsp.resolveAirport(f.to)   || null,
      status:         "scheduled",
      progress:       0,
      currentLat:     null,
      currentLon:     null,
      actualDeparture:   null,
      estimatedArrival:  null,
      type:           type || f.type || "outbound",
      departureTerminal: null,
      departureGate:     null,
      arrivalTerminal:   null,
      arrivalGate:       null,
      scheduledDeparture:  null,
      estimatedDeparture:  null,
      scheduledArrival:    null,
      groundspeed:         null,
      altitude:            null,
      heading:             null,
      altitudeChange:      null,
      lastPositionUpdate:  null,
      aircraftType:        null,
      tailNumber:          null,
      foresightEta:        null,
      detailedStatus:      null
    });

    if (cfg.scenario === 1) {
      if ((!cfg.flights || cfg.flights.length === 0) && cfg.destination) {
        this.flightLegs = [mkLeg({
          from: cfg.home,
          to: cfg.destination,
          flightNumber: cfg.flightNumber || "GO",
          departureDate: cfg.departureDate || ""
        }, null, "outbound")];
      } else {
        this.flightLegs = (cfg.flights || []).map((f, i) => mkLeg(f, null, i === 0 ? "outbound" : "return"));
      }

    } else if (cfg.scenario === 2) {
      this.flightLegs = (cfg.flights || []).map(f => mkLeg(f, null, "outbound"));

    } else if (cfg.scenario === 3) {
      this.flightLegs = (cfg.travelers || []).reduce((acc, tv) => {
        (tv.flights       || []).forEach(f => acc.push(mkLeg(f, tv.name, "outbound")));
        (tv.returnFlights || []).forEach(f => acc.push(mkLeg(f, tv.name, "return")));
        return acc;
      }, []);

    } else if (cfg.scenario === 5) {
      const crewFile = cfg.crewFlightsFile || "data/my_flights.csv";
      const crewPath = this.validatePath(crewFile, "data/my_flights.csv");
      try {
        const raw   = await fs.promises.readFile(crewPath, "utf8");
        const lines = raw.split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"));
        if (!lines.length) throw new Error("CSV is empty");

        const hdrs = this._fsp.parseCSVLine(lines[0]).map(h => h.trim().toLowerCase());
        const getCol = (row, name) => {
          const i = hdrs.indexOf(name);
          return i !== -1 ? (row[i] || "").trim() : "";
        };

        this.flightLegs = lines.slice(1).map(line => {
          const vals = this._fsp.parseCSVLine(line);
          const travelerName = getCol(vals, "travelername") || getCol(vals, "traveler_name") || "Crew";
          const type         = getCol(vals, "type") || "outbound";

          let dateStr = getCol(vals, "departuredate") || getCol(vals, "departure_date");
          if (dateStr) {
            let m = dateStr.match(/^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})$/);
            if (m) {
              let d = m[1].padStart(2, "0");
              let mo = m[2].padStart(2, "0");
              let y = m[3];
              if (y.length === 2) y = "20" + y;
              dateStr = `${y}-${mo}-${d}`;
            }
          }

          return mkLeg({
            flightNumber:  getCol(vals, "flightnumber") || getCol(vals, "flight_number"),
            departureDate: dateStr,
            departureTime: getCol(vals, "departuretime") || getCol(vals, "departure_time"),
            from:          getCol(vals, "from"),
            to:            getCol(vals, "to"),
            type
          }, travelerName, type);
        }).filter(l => l.departureDate && l.from && l.to);

        console.log(`[${this.name}] Scenario 5: loaded ${this.flightLegs.length} legs from ${crewFile}`);
      } catch (e) {
        console.error(`[${this.name}] Scenario 5: failed to load ${crewFile}: ${e.message}`);
        this.flightLegs = [];
      }

    } else if (cfg.scenario === 4) {
      const homeAp = this._fsp.resolveAirport(cfg.home) || { name: "Home", iata: "HOME", lat: 0, lon: 0 };

      (cfg.flights || []).forEach(f => {
        const destAp = this._fsp.resolveAirport(f.to || f) || null;
        if (!destAp) return;

        if (cfg.showWhereIHaveBeen) {
          this.flightLegs.push(mkLeg({
            from: homeAp,
            to: destAp,
            flightNumber: f.flightNumber || "GO",
            departureDate: f.departureDate || ""
          }, "Traveler", "outbound"));

          this.flightLegs.push(mkLeg({
            from: destAp,
            to: homeAp,
            flightNumber: f.returnFlightNumber || "BACK",
            departureDate: f.returnDate || f.departureDate || ""
          }, "Traveler", "return"));
        } else {
          this.flightLegs.push({ to: destAp, status: "landed", type: "outbound" });
        }
      });

    } else if (cfg.scenario === 6) {
      const footballFile = cfg.footballAwayTripsFile || "data/footballAwayTrips.csv";
      const homeAp = this._fsp.resolveAirport(cfg.home) || { name: "Home", iata: "HOME", lat: 0, lon: 0 };
      const footballPath = this.validatePath(footballFile, "data/footballAwayTrips.csv");
      try {
        const raw = await fs.promises.readFile(footballPath, "utf8");
        const lines = raw.split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"));
        if (lines.length) {
          const hdrs = this._fsp.parseCSVLine(lines[0]).map(h => h.trim().toLowerCase());
          const getCol = (row, name) => {
            const i = hdrs.indexOf(name.toLowerCase());
            return i !== -1 ? (row[i] || "").trim() : "";
          };

          let unresolved = 0;
          this.flightLegs = lines.slice(1).map(line => {
            const vals = this._fsp.parseCSVLine(line);
            const travelerName = getCol(vals, "travlername") || getCol(vals, "travelername") || getCol(vals, "traveler_name") || "Fans";
            const type = getCol(vals, "type") || "outbound";
            const toRef = getCol(vals, "to");

            const to = this._fsp.resolveFootballTeam(toRef);

            if (!to) {
              unresolved++;
              console.warn(`[${this.name}] Scenario 6: could not resolve team "${toRef}" — skipping`);
              return null;
            }

            let dateStr = getCol(vals, "departuredate") || getCol(vals, "departure_date");
            if (dateStr) {
              let m = dateStr.match(/^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})$/);
              if (m) {
                let d = m[1].padStart(2, "0");
                let mo = m[2].padStart(2, "0");
                let y = m[3];
                if (y.length === 2) y = "20" + y;
                dateStr = `${y}-${mo}-${d}`;
              }
            }

            const leg = mkLeg({
              flightNumber: getCol(vals, "flightnumber") || getCol(vals, "flight_number") || "GO",
              departureDate: dateStr,
              departureTime: getCol(vals, "departuretime") || getCol(vals, "departure_time"),
              from: null,
              to,
              type
            }, travelerName, type);

            leg.opponent    = toRef;
            leg.competition = getCol(vals, "competition");
            leg.score       = getCol(vals, "score");
            leg.result      = getCol(vals, "result");

            return leg;
          }).filter(l => l && l.departureDate && l.to);
          console.log(`[${this.name}] Scenario 6: loaded ${this.flightLegs.length} trips, ${unresolved} unresolved from ${footballFile}`);
        }
      } catch (e) {
        console.error(`[${this.name}] Scenario 6 error: ${e.message}`);
      }
    }

    const destNames = Array.from(new Set(
      this.flightLegs
        .filter(l => l.to && l.to.name)
        .map(l => l.to.name)
        .concat(cfg.destination && cfg.destination.name ? [cfg.destination.name] : [])
    ));

    const cityInfo = {};
    const BATCH_SIZE = 5;
    const skipAllWeather = destNames.length > 5;
    const attractionsDir = path.join(__dirname, "data", "attractions");
    for (let i = 0; i < destNames.length; i += BATCH_SIZE) {
      const batch = destNames.slice(i, i + BATCH_SIZE);
      const infoPromises = batch.map(async name => {
        const info = await this._fsp.getCityInfo(name, skipAllWeather, this._weather, attractionsDir);
        if (info) cityInfo[name] = info;
      });
      await Promise.all(infoPromises);
    }

    const visitedCountryIsos = this._fsp._buildVisitedCountryIsos(this.flightLegs, this._manualVisitedCountries, this.config.scenario);
    const regionData         = await this._fsp._buildRegionData(cfg, path.join(__dirname, "node_modules", "@amcharts", "amcharts5-geodata"));

    await this._saveScenarioCache(this.config.scenario, { legs: this.flightLegs, cityInfo, visitedCountryIsos }, cfgFingerprint);

    this.sendSocketNotification("iAGT_INIT", {
      legs: this.flightLegs,
      cityInfo,
      visitedCountryIsos,
      regionData
    });

    /* INN-001: Fetch fun fact for the primary destination if enabled */
    if (cfg.funFactsEnabled) {
      const primaryDest = destNames[0];
      if (primaryDest) {
        this._fetchFunFact(primaryDest).catch((e) => {
          console.warn(`[${this.name}] INN-001: Fun fact fetch failed: ${e.message}`);
        });
      }
    }
  },

  /* ─────────────────────── POLLING ────────────────────────────────────── */
  schedulePolling () {
    if (this.pollTimer) clearInterval(this.pollTimer);

    if (!this.config.flightAwareApiKey) {
      console.log(`[${this.name}] No FlightAware API key configured — live tracking disabled`);
      this.sendSocketNotification("iAGT_NO_API_KEY", {});
      return;
    }

    const intervalMs = (this.config.pollInterval || 5) * 60 * 1000;
    this._runPoll();
    this.pollTimer = setInterval(() => this._runPoll(), intervalMs);
  },

  async _runPoll () {
    await this._flightAware.pollAllFlights(
      this.flightLegs,
      this.config.scenario,
      this.config.flightAwareApiKey,
      (legs) => {
        this.checkTripResetAndNotify();
        this.sendSocketNotification("iAGT_FLIGHT_UPDATE", { legs });
      }
    );
    this.checkTripResetAndNotify();
  },

  checkTripResetAndNotify () {
    this.tripCompleteTime = this._flightAware.checkTripReset(
      this.flightLegs,
      this.config.colorResetAfterDays,
      this.tripCompleteTime,
      (notification, payload) => {
        this.sendSocketNotification(notification, payload);
        if (this.pollTimer) { clearInterval(this.pollTimer); this.pollTimer = null; }
      }
    );
  },

  /* ─────────────────────── SCENARIO CACHING ──────────────────────────── */
  _getScenarioCachePath (scenario) {
    return this.validatePath(path.join("cache", `scenario_${scenario}.json`), "data/cities.csv");
  },

  async _saveScenarioCache (scenario, data, fingerprint) {
    try {
      const fp = this._getScenarioCachePath(scenario);
      await fs.promises.mkdir(path.dirname(fp), { recursive: true });
      const cacheData = {
        ts: Date.now(),
        fingerprint: fingerprint || "",
        data: data
      };
      await fs.promises.writeFile(fp, JSON.stringify(cacheData, null, 2), "utf8");
    } catch (e) {
      console.warn(`[${this.name}] Cache save error: ${e.message}`);
    }
  },

  async _loadScenarioCache (scenario, fingerprint) {
    try {
      const fp = this._getScenarioCachePath(scenario);
      const exists = await fs.promises.stat(fp).then(() => true).catch(() => false);
      if (exists) {
        const raw = await fs.promises.readFile(fp, "utf8");
        const cacheData = JSON.parse(raw);
        if (fingerprint && cacheData.fingerprint !== fingerprint) return null;
        if (Date.now() - cacheData.ts < 1800000) {
          return cacheData.data;
        }
      }
    } catch (e) {
      // ignore
    }
    return null;
  },

  async _clearScenarioCache () {
    try {
      const dir = path.join(__dirname, "cache");
      const exists = await fs.promises.stat(dir).then(() => true).catch(() => false);
      if (exists) {
        const files = await fs.promises.readdir(dir);
        for (const f of files) {
          if (f.startsWith("scenario_") && f.endsWith(".json")) {
            await fs.promises.unlink(path.join(dir, f));
          }
        }
        console.log(`[${this.name}] Scenario cache cleared`);
      }
    } catch (e) {
      console.warn(`[${this.name}] Cache clear error: ${e.message}`);
    }
  },

  /* ── INN-001: Fetch a fun fact from the Wikipedia REST API (free, no key) ── */
  async _fetchFunFact (cityName) {
    if (!cityName) return;
    const encoded = encodeURIComponent(cityName.trim());
    const options = {
      hostname: "en.wikipedia.org",
      port: 443,
      path: `/w/api.php?action=query&titles=${encoded}&prop=extracts&exintro=true&explaintext=true&format=json&redirects=1`,
      method: "GET",
      headers: { "User-Agent": "MMM-iAmGoingThere/1.0 (MagicMirror module)" }
    };

    const fact = await new Promise((resolve, reject) => {
      const req = https.request(options, (res) => {
        let raw = "";
        res.on("data", (chunk) => { raw += chunk; });
        res.on("end", () => {
          try {
            const data = JSON.parse(raw);
            const pages = data.query && data.query.pages ? data.query.pages : {};
            const page = Object.values(pages)[0];
            if (!page || !page.extract) { resolve(null); return; }
            const text = page.extract.replace(/\n+/g, " ").trim();
            const sentences = text.match(/[^.!?]+[.!?]+/g) || [];
            const fact = sentences.slice(0, 2).join(" ").trim() || text.slice(0, 200);
            resolve(fact || null);
          } catch (e) {
            reject(new Error(`JSON parse: ${e.message}`));
          }
        });
      });
      req.on("error", reject);
      req.setTimeout(8000, () => { req.destroy(); reject(new Error("timeout")); });
      req.end();
    });

    if (fact) {
      console.log(`[${this.name}] INN-001: Fun fact for ${cityName}: ${fact}`);
      this.sendSocketNotification("iAGT_FUN_FACT", { cityName, fact });
    }
  },

  /* ───────────────────────── CLEANUP ──────────────────────────────────── */
  stop () {
    if (this.pollTimer) { clearInterval(this.pollTimer); this.pollTimer = null; }
    console.log(`[${this.name}] node_helper stopped`);
  }
});

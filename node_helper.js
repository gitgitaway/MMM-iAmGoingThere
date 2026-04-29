/*
 * node_helper.js – MMM-iAmGoingThere
 *
 * Backend helper responsible for:
 *   - Parsing cities.csv and loading attraction JSON files
 *   - Building flight legs from the user config (all 3 scenarios)
 *   - Polling FlightAware AeroAPI for live flight status & position
 *   - Sending status updates back to the frontend module
 *
 * FlightAware AeroAPI v4  https://flightaware.com/aeroapi/
 * Endpoint: GET /flights/{ident}?start=YYYY-MM-DD&end=YYYY-MM-DD
 * Auth:     x-apikey header
 */

const NodeHelper = require("node_helper");
const https      = require("https");
const fs         = require("fs");
const path       = require("path");

module.exports = NodeHelper.create({

  /* ───────────────────────── LIFECYCLE ────────────────────────────────── */
  start () {
    this.config                  = null;
    this.flightLegs              = [];
    this.citiesData              = [];
    this.airportsData            = {};
    this.footballTeams           = {};
    this.footballTeamsNormalized = {};
    this.pollTimer               = null;
    this.tripCompleteTime  = null;
    this._attractionsCache = {};
    this._weatherCache     = {};
    this._manualVisitedCountries = [];
    console.log(`[${this.name}] node_helper started`);
  },

  async socketNotificationReceived (notification, payload) {
    if (notification === "iAGT_REFRESH_WEATHER") {
      const { cityName } = payload;
      const info = await this.getCityInfo(cityName);
      if (info && info.weather) {
        this.sendSocketNotification("iAGT_WEATHER_UPDATE", { cityName, weather: info.weather });
      }
      return;
    }
    if (notification === "iAGT_SAVE_ATTRACTIONS") {
      await this.saveAttractionsFile(payload);
      return;
    }
    if (notification === "iAGT_SAVE_FLIGHTS") {
      await this.saveFlightsFile(payload);
      return;
    }
    if (notification === "iAGT_SAVE_TERMINAL_MAPS") {
      await this.saveTerminalMapsFile(payload);
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
      await this.saveManualVisitedCountries();
      // Re-process scenario to update the frontend with new visited list
      await this.processScenario();
      return;
    }
    if (notification === "UPDATE_SCENARIO") {
      this.config.scenario = payload.scenario;
      await this.processScenario();
      return;
    }
    if (notification === "iAGT_CONFIG") {
      this.config = payload;

      // Resolve API key: env-var takes precedence, then config block value
      const envKey = (process.env.FLIGHTAWARE_API_KEY || "").trim();
      const cfgKey = (this.config.flightAwareApiKey  || "").trim();
      this.config.flightAwareApiKey = envKey || cfgKey;

      if (!this.config.flightAwareApiKey) {
        console.error(`[${this.name}] No FlightAware API key. ` +
          `Set flightAwareApiKey in your config.js module block ` +
          `or the FLIGHTAWARE_API_KEY environment variable.`);
      }

      await Promise.all([
        this.loadCitiesData(),
        this.loadAirportsData(),
        this.loadFootballTeamsData(),
        this.loadManualVisitedCountries()
      ]);
      await this.processScenario();
      this.schedulePolling();
    }
  },

  /* ─────────────────────── CSV PARSING ────────────────────────────────── */
  async loadCitiesData () {
    if (this.citiesData && this.citiesData.length > 0) return;
    let citiesFile = this.config.citiesFile || "data/cities.csv";
    let csvPath = path.resolve(__dirname, citiesFile);

    // SEC-003: Path-containment check
    if (!csvPath.startsWith(path.resolve(__dirname))) {
      console.warn(`[${this.name}] citiesFile path escapes module directory. Using default.`);
      csvPath = path.resolve(__dirname, "data/cities.csv");
    }

    try {
      const raw   = await fs.promises.readFile(csvPath, "utf8");
      const lines = raw.split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"));
      const hdrs  = this.parseCSVLine(lines[0]).map(h => h.trim());

      this.citiesData = lines.slice(1).map(line => {
        const vals = this.parseCSVLine(line);
        const obj  = {};
        hdrs.forEach((h, i) => { obj[h] = (vals[i] || "").trim(); });
        return obj;
      }).filter(r => r.city);

      console.log(`[${this.name}] Loaded ${this.citiesData.length} cities from CSV`);
    } catch (e) {
      console.error(`[${this.name}] cities.csv error: ${e.message}`);
      this.citiesData = [];
    }
  },

  async loadAirportsData () {
    if (this.airportsData && Object.keys(this.airportsData).length > 0) return;
    const csvPath = path.resolve(__dirname, "data", "airports.csv");
    try {
      const raw   = await fs.promises.readFile(csvPath, "utf8");
      const lines = raw.split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"));
      const hdrs  = this.parseCSVLine(lines[0]).map(h => h.trim());
      this.airportsData = {};
      lines.slice(1).forEach(line => {
        const vals = this.parseCSVLine(line);
        const obj  = {};
        hdrs.forEach((h, i) => { obj[h] = (vals[i] || "").trim(); });
        if (obj.iataCode) {
          this.airportsData[obj.iataCode.toUpperCase()] = {
            name: obj.name     || obj.iataCode,
            iata: obj.iataCode.toUpperCase(),
            lat:  parseFloat(obj.lat) || 0,
            lon:  parseFloat(obj.lon) || 0,
            country: obj.country || ""
          };
        }
      });
      console.log(`[${this.name}] Loaded ${Object.keys(this.airportsData).length} airports`);
    } catch (e) {
      console.warn(`[${this.name}] airports.csv not loaded: ${e.message}`);
      this.airportsData = {};
    }
  },

  _normalizeTeamName (name) {
    return name.toLowerCase()
      .replace(/\u00f8/g, "o")   // ø
      .replace(/\u00f6/g, "o")   // ö
      .replace(/\u00f3/g, "o")   // ó
      .replace(/\u00fa/g, "u")   // ú
      .replace(/\u00fc/g, "u")   // ü
      .replace(/\u00e9/g, "e")   // é
      .replace(/\u00e8/g, "e")   // è
      .replace(/\u00eb/g, "e")   // ë
      .replace(/\u00ea/g, "e")   // ê
      .replace(/\u00e1/g, "a")   // á
      .replace(/\u00e0/g, "a")   // à
      .replace(/\u00e4/g, "a")   // ä
      .replace(/\u00e2/g, "a")   // â
      .replace(/\u00e3/g, "a")   // ã
      .replace(/\u00ed/g, "i")   // í
      .replace(/\u00ef/g, "i")   // ï
      .replace(/\u00ee/g, "i")   // î
      .replace(/\u00f1/g, "n")   // ñ
      .replace(/\u00e7/g, "c")   // ç
      .replace(/\u00fd/g, "y")   // ý
      .replace(/\u017e/g, "z")   // ž
      .replace(/\u0161/g, "s")   // š
      .replace(/\u010d/g, "c")   // č
      .replace(/\u0159/g, "r")   // ř
      .replace(/\s+/g, " ")
      .trim();
  },

  async loadFootballTeamsData () {
    if (this.footballTeams && Object.keys(this.footballTeams).length > 0) return;
    const csvPath = path.resolve(__dirname, "data", "football_teams_database.csv");
    try {
      const raw   = await fs.promises.readFile(csvPath, "utf8");
      const lines = raw.split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"));
      if (!lines.length) {
        console.error(`[${this.name}] football_teams_database.csv is empty`);
        return;
      }

      const hdrs = this.parseCSVLine(lines[0]).map(h => h.trim().replace(/^\uFEFF/, ""));

      const teamIdx    = hdrs.indexOf("Team");
      const latIdx     = hdrs.indexOf("Latitude");
      const lonIdx     = hdrs.indexOf("Longitude");
      const countryIdx = hdrs.indexOf("Country");
      const crestIdx   = hdrs.indexOf("crestImage");

      if (teamIdx === -1 || latIdx === -1 || lonIdx === -1) {
        console.error(`[${this.name}] football_teams_database.csv missing required columns. Found: ${hdrs.join(", ")}`);
        return;
      }

      this.footballTeams = {};
      this.footballTeamsNormalized = {};

      lines.slice(1).forEach(line => {
        const vals = this.parseCSVLine(line);
        const name = (vals[teamIdx] || "").trim();
        const country = countryIdx !== -1 ? (vals[countryIdx] || "").trim() : "";
        const crestImg = crestIdx !== -1 ? (vals[crestIdx] || "").trim() : "";

        const lat = parseFloat(vals[latIdx]);
        const lon = parseFloat(vals[lonIdx]);

        if (!name || isNaN(lat) || isNaN(lon) || (lat === 0 && lon === 0)) return;

        let crestPath = null;
        if (country && crestImg && crestImg.toLowerCase() !== "not_found.png") {
          const countryFolder = country.replace(/ /g, "_");
          crestPath = `modules/MMM-iAmGoingThere/images/crests/${countryFolder}/${crestImg}`;
        }

        const entry = { name, iata: "TEAM", lat, lon, crest: crestPath, country };

        this.footballTeams[name.toLowerCase()] = entry;
        const norm = this._normalizeTeamName(name);
        if (!this.footballTeamsNormalized[norm]) {
          this.footballTeamsNormalized[norm] = entry;
        }
      });
      console.log(`[${this.name}] Loaded ${Object.keys(this.footballTeams).length} football teams`);
    } catch (e) {
      console.error(`[${this.name}] football_teams_database.csv not loaded: ${e.message}`);
      this.footballTeams = {};
      this.footballTeamsNormalized = {};
    }
  },

  resolveFootballTeam (toRef) {
    if (!toRef) return null;
    const lower = toRef.toLowerCase().trim();

    if (this.footballTeams[lower]) return this.footballTeams[lower];

    const norm = this._normalizeTeamName(toRef);
    if (this.footballTeamsNormalized[norm]) return this.footballTeamsNormalized[norm];

    const allKeys = Object.keys(this.footballTeams);
    const allNormKeys = Object.keys(this.footballTeamsNormalized);

    const exactSubKey = allKeys.find(k => lower.includes(k) || k.includes(lower));
    if (exactSubKey) return this.footballTeams[exactSubKey];

    const normSubKey = allNormKeys.find(k => norm.includes(k) || k.includes(norm));
    if (normSubKey) return this.footballTeamsNormalized[normSubKey];

    return null;
  },

  resolveAirport (ref) {
    if (!ref) return null;
    if (typeof ref === "string") {
      const iata = ref.trim().toUpperCase();
      const airport = this.airportsData[iata];
      if (airport) return airport;

      // Fallback to cities.csv lookup for city name
      const lower = ref.trim().toLowerCase();
      const city = this.citiesData.find(c => c.city && c.city.toLowerCase() === lower);
      if (city && city.lat != null && city.lon != null) {
        return { 
          name: city.city, 
          iata: city.iata || "CITY", 
          lat: parseFloat(city.lat), 
          lon: parseFloat(city.lon),
          country: city.country || ""
        };
      }

      // Fallback to football teams lookup
      const team = this.footballTeams[lower];
      if (team) return team;

      return null; // Return null instead of 0,0 for unknown locations
    }
    if (typeof ref === "object") {
      if (ref.lat != null && ref.lon != null) {
        if (ref.country) return ref;
        // Try to resolve country by name if missing
        const name = ref.to || ref.from || ref.name || ref.city;
        if (name) {
          const lower = name.trim().toLowerCase();
          const city = this.citiesData.find(c => c.city && c.city.toLowerCase() === lower);
          if (city) return { ...ref, country: city.country || "" };
          
          const team = this.footballTeams[lower];
          if (team) return { ...ref, country: team.country || "" };
        }
        return ref;
      }
      const iata = (ref.iata || "").trim().toUpperCase();
      const resolved = iata ? this.airportsData[iata] : null;
      if (resolved) return { ...resolved, ...ref, lat: resolved.lat, lon: resolved.lon };

      // Fallback to cities.csv or football teams lookup if object has a name, city, to, or from key
      const name = ref.to || ref.from || ref.name || ref.city;
      if (name) {
        const lower = name.trim().toLowerCase();
        const city = this.citiesData.find(c => c.city && c.city.toLowerCase() === lower);
        if (city && city.lat != null && city.lon != null) {
          return { 
            ...ref, 
            name: city.city, 
            lat: parseFloat(city.lat), 
            lon: parseFloat(city.lon),
            country: city.country || ""
          };
        }

        // Fallback to football teams lookup
        const team = this.footballTeams[lower];
        if (team) return { ...ref, ...team };
      }

      return null; // Return null instead of the input object if unresolved
    }
    return null;
  },

  parseCSVLine (line) {
    const res  = [];
    let   cur  = "";
    let   inQ  = false;
    for (const ch of line) {
      if      (ch === '"')          { inQ = !inQ; }
      else if (ch === "," && !inQ)  { res.push(cur); cur = ""; }
      else                          { cur += ch; }
    }
    res.push(cur);
    return res;
  },

  /* ───────────────────── ATTRACTIONS DATA ─────────────────────────────── */
  async loadAttractions (cityName) {
    const slug = cityName.toLowerCase()
      .replace(/[^a-z0-9]+/g, "_")
      .replace(/^_|_$/g, "");
    if (this._attractionsCache[slug] !== undefined) {
      return this._attractionsCache[slug];
    }
    const fp = path.join(__dirname, "data", "attractions", `${slug}.json`);
    let result = null;
    try {
      const exists = await fs.promises.stat(fp).then(() => true).catch(() => false);
      if (exists) {
        const raw = await fs.promises.readFile(fp, "utf8");
        result = JSON.parse(raw);
      }
    } catch (e) {
      console.warn(`[${this.name}] Attractions load error for ${cityName}: ${e.message}`);
    }
    this._attractionsCache[slug] = result;
    return result;
  },

  async getCityInfo (cityName, skipWeather = false) {
    const lower = cityName.toLowerCase();
    let city = this.citiesData.find(c => c.city && c.city.toLowerCase() === lower);
    if (!city) {
      city = this.citiesData.find(c => c.city && lower.includes(c.city.toLowerCase()));
    }
    if (!city) return null;
    const attractions = await this.loadAttractions(city.city);
    const weather = skipWeather ? null : await this.fetchWeather(city.lat, city.lon);
    return { ...city, attractions, weather };
  },

  async fetchWeather (lat, lon) {
    if (!lat || !lon) return null;
    const cacheKey = `${lat},${lon}`;
    if (this._weatherCache[cacheKey] && (Date.now() - this._weatherCache[cacheKey].ts < 1800000)) { // 30 min cache
      return this._weatherCache[cacheKey].data;
    }

    return new Promise((resolve) => {
      const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true`;
      https.get(url, (res) => {
        let body = "";
        res.on("data", (chunk) => { body += chunk; });
        res.on("end", () => {
          try {
            const data = JSON.parse(body);
            const weather = data.current_weather || null;
            if (weather) {
              this._weatherCache[cacheKey] = { ts: Date.now(), data: weather };
            }
            resolve(weather);
          } catch (e) {
            resolve(null);
          }
        });
      }).on("error", () => {
        resolve(null);
      });
    });
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

		// Try loading from cache first
		const cfgFingerprint = JSON.stringify({
			flights:   cfg.flights   || [],
			travelers: cfg.travelers || [],
			overideDate: !!cfg.overideDate
		});
		const cached = await this._loadScenarioCache(this.config.scenario, cfgFingerprint);
		if (cached) {
			console.log(`[${this.name}] Loading Scenario ${this.config.scenario} from cache`);
			this.flightLegs = cached.legs;
			const regionData = await this._buildRegionData();
			this.sendSocketNotification("iAGT_INIT", {
				legs:                this.flightLegs,
				cityInfo:            cached.cityInfo,
				visitedCountryIsos:  cached.visitedCountryIsos || [],
				regionData
			});
			return; // Skip full processing
		}

		this.flightLegs = [];
		let idx = 0;

		let overrideDateStr = "";
		let overrideTimeStr = "";
		if (cfg.overideDate) {
			const d = new Date(Date.now() + 5 * 60 * 1000);
			overrideDateStr = d.toISOString().split("T")[0]; // "YYYY-MM-DD"
			overrideTimeStr = d.toTimeString().split(" ")[0].substring(0, 5); // "HH:MM"
			console.log(`[${this.name}] Overriding all flight takeoff times to: ${overrideDateStr} ${overrideTimeStr}`);
		}

		const mkLeg = (f, travelerName, type) => ({
			id:             `leg_${idx++}`,
			travelerName:   travelerName || f.travelerName || "Traveler",
			flightNumber:   f.flightNumber   || "",
			departureDate:  cfg.overideDate ? overrideDateStr : (f.departureDate  || ""),
			departureTime:  cfg.overideDate ? overrideTimeStr : (f.departureTime  || ""),   // optional "HH:MM" for intra-day ordering
			from:           this.resolveAirport(f.from) || null,
      to:             this.resolveAirport(f.to)   || null,
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
      /*
       * Scenario 1: [ outbound_leg, return_leg ]
       */
      if ((!cfg.flights || cfg.flights.length === 0) && cfg.destination) {
        // Fallback: build a single leg from home to destination if no flights array
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
      /*
       * Scenario 2: [ leg1, leg2, …, legN ]  (N up to 10+ for RTW)
       */
      this.flightLegs = (cfg.flights || []).map(f => mkLeg(f, null, "outbound"));

    } else if (cfg.scenario === 3) {
      /*
       * Scenario 3: Multiple travelers / groups, each with outbound + return legs.
       * Supports direct flights and stopovers (multiple legs per traveler).
       */
      this.flightLegs = (cfg.travelers || []).reduce((acc, tv) => {
        (tv.flights       || []).forEach(f => acc.push(mkLeg(f, tv.name, "outbound")));
        (tv.returnFlights || []).forEach(f => acc.push(mkLeg(f, tv.name, "return")));
        return acc;
      }, []);
    } else if (cfg.scenario === 5) {
      /*
       * Scenario 5: Aircrew / Frequent Flyer CSV schedule
       * Reads flight legs from a user-maintained CSV file.
       * Default path: data/my_flights.csv
       * Required columns: departureDate, flightNumber, from, to
       * Optional columns: departureTime, travelerName, type (outbound|return)
       */
      const crewFile = cfg.crewFlightsFile || "data/my_flights.csv";
      let crewPath = path.resolve(__dirname, crewFile);
      if (!crewPath.startsWith(path.resolve(__dirname))) {
        console.warn(`[${this.name}] crewFlightsFile path escapes module directory. Using default.`);
        crewPath = path.resolve(__dirname, "data/my_flights.csv");
      }
      try {
        const raw   = await fs.promises.readFile(crewPath, "utf8");
        const lines = raw.split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"));
        if (!lines.length) throw new Error("CSV is empty");

        const hdrs = this.parseCSVLine(lines[0]).map(h => h.trim().toLowerCase());
        const getCol = (row, name) => {
          const i = hdrs.indexOf(name);
          return i !== -1 ? (row[i] || "").trim() : "";
        };

        this.flightLegs = lines.slice(1).map(line => {
          const vals = this.parseCSVLine(line);
          const travelerName = getCol(vals, "travelername") || getCol(vals, "traveler_name") || "Crew";
          const type         = getCol(vals, "type") || "outbound";
          
          let dateStr = getCol(vals, "departuredate") || getCol(vals, "departure_date");
          if (dateStr) {
            // Support D/M/YYYY or DD/MM/YYYY
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
      /*
       * Scenario 4: "Where I have been"
       * Places a white destination marker for all destinations in cfg.flights.
       * If showWhereIHaveBeen is true, shows home -> destination -> home return flights.
       */
      const homeAp = this.resolveAirport(cfg.home) || { name: "Home", iata: "HOME", lat: 0, lon: 0 };
      
      (cfg.flights || []).forEach(f => {
        const destAp = this.resolveAirport(f.to || f) || null;
        if (!destAp) return;

        if (cfg.showWhereIHaveBeen) {
          // Outbound: Home -> Destination
          this.flightLegs.push(mkLeg({
            from: homeAp,
            to: destAp,
            flightNumber: f.flightNumber || "GO",
            departureDate: f.departureDate || ""
          }, "Traveler", "outbound"));

          // Return: Destination -> Home
          this.flightLegs.push(mkLeg({
            from: destAp,
            to: homeAp,
            flightNumber: f.returnFlightNumber || "BACK",
            departureDate: f.returnDate || f.departureDate || ""
          }, "Traveler", "return"));
        } else {
          // If not showing tracks, we still want the "to" airports for attractions lookup
          // We can push a "dummy" leg that won't be rendered but provides the "to" info
          this.flightLegs.push({ to: destAp, status: "landed", type: "outbound" });
        }
      });
    } else if (cfg.scenario === 6) {
      /*
       * Scenario 6: Football Away Trips CSV
       * Reads trips from data/footballAwayTrips.csv
       * Required columns: departureDate, to
       * Optional columns: Competition, Score, Result, flightNumber, travelerName
       */
      const footballFile = cfg.footballAwayTripsFile || "data/footballAwayTrips.csv";
      const homeAp = this.resolveAirport(cfg.home) || { name: "Home", iata: "HOME", lat: 0, lon: 0 };
      let footballPath = path.resolve(__dirname, footballFile);
      if (!footballPath.startsWith(path.resolve(__dirname))) {
        footballPath = path.resolve(__dirname, "data/footballAwayTrips.csv");
      }
      try {
        const raw = await fs.promises.readFile(footballPath, "utf8");
        const lines = raw.split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"));
        if (lines.length) {
          const hdrs = this.parseCSVLine(lines[0]).map(h => h.trim().toLowerCase());
          const getCol = (row, name) => {
            const i = hdrs.indexOf(name.toLowerCase());
            return i !== -1 ? (row[i] || "").trim() : "";
          };

          let unresolved = 0;
          this.flightLegs = lines.slice(1).map(line => {
            const vals = this.parseCSVLine(line);
            const travelerName = getCol(vals, "travlername") || getCol(vals, "travelername") || getCol(vals, "traveler_name") || "Fans";
            const type = getCol(vals, "type") || "outbound";
            const toRef = getCol(vals, "to");

            const to = this.resolveFootballTeam(toRef);

            if (!to) {
              unresolved++;
              console.warn(`[${this.name}] Scenario 6: could not resolve team "${toRef}" — skipping`);
              return null;
            }

            // Support DD/MM/YYYY format found in footballAwayTrips.csv
            let dateStr = getCol(vals, "departuredate") || getCol(vals, "departure_date");
            if (dateStr) {
              // Support D/M/YYYY or DD/MM/YYYY
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

            leg.opponent = toRef;
            leg.competition = getCol(vals, "competition");
            leg.score = getCol(vals, "score");
            leg.result = getCol(vals, "result");

            return leg;
          }).filter(l => l && l.departureDate && l.to);
          console.log(`[${this.name}] Scenario 6: loaded ${this.flightLegs.length} trips, ${unresolved} unresolved from ${footballFile}`);
        }
      } catch (e) {
        console.error(`[${this.name}] Scenario 6 error: ${e.message}`);
      }
    }

    /* Collect destination city names for attractions lookup */
    const destNames = Array.from(new Set(
      this.flightLegs
        .filter(l => l.to && l.to.name)
        .map(l => l.to.name)
        .concat(cfg.destination && cfg.destination.name ? [cfg.destination.name] : [])
    ));

    const cityInfo = {};
    const BATCH_SIZE = 5;
    const skipAllWeather = destNames.length > 5;
    for (let i = 0; i < destNames.length; i += BATCH_SIZE) {
      const batch = destNames.slice(i, i + BATCH_SIZE);
      const infoPromises = batch.map(async name => {
        const info = await this.getCityInfo(name, skipAllWeather);
        if (info) cityInfo[name] = info;
      });
      await Promise.all(infoPromises);
    }

    const visitedCountryIsos = this._buildVisitedCountryIsos();
    const regionData         = await this._buildRegionData();

    await this._saveScenarioCache(this.config.scenario, { legs: this.flightLegs, cityInfo, visitedCountryIsos }, cfgFingerprint);

    this.sendSocketNotification("iAGT_INIT", {
      legs: this.flightLegs,
      cityInfo,
      visitedCountryIsos,
      regionData
    });
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
    this.pollAllFlights();   // immediate first poll
    this.pollTimer = setInterval(() => this.pollAllFlights(), intervalMs);
  },

  async pollAllFlights () {
    const now     = new Date();
    let   updated = false;

    // Mitigation: Skip Scenario 4 & 6 (no flight tracking)
    if (this.config.scenario === 4 || this.config.scenario === 6) return;

    const legsToFetch = this.flightLegs.filter(leg => {
      if (!leg.departureDate || leg.status === "cancelled") return false;
      
      // Calculate start of departure day in local time for comparison
      const depDate = new Date(`${leg.departureDate}T00:00:00`);
      const hoursUntil = (depDate - now) / 3600000;
      
      // If status is scheduled, only poll if departure is within 24 hours
      // (Increased from 12h to handle long-haul flights that might be airborne 
      // already from a previous leg if using same flight number, or just to be safe)
      if (leg.status === "scheduled" && hoursUntil > 24) return false;
      
      if (leg.status === "landed") return false;
      if (leg._nextPollTime && Date.now() < leg._nextPollTime) return false;
      return true;
    });

    const BATCH_SIZE = 3;
    for (let i = 0; i < legsToFetch.length; i += BATCH_SIZE) {
      const batch = legsToFetch.slice(i, i + BATCH_SIZE);
      const results = await Promise.allSettled(
        batch.map(leg => this.fetchFlightStatus(leg.flightNumber, leg.departureDate, leg.status))
      );
      results.forEach((result, j) => {
        const leg = batch[j];
        if (result.status === "fulfilled") {
          const data = result.value;
          if (data) {
            const prev = leg.status;
            this.updateLegFromAPI(leg, data);
            if (prev !== leg.status || leg.status === "active") updated = true;
          }
          leg._failCount    = 0;
          leg._nextPollTime = 0;
        } else {
          leg._failCount = (leg._failCount || 0) + 1;
          const retryMs  = Math.min(300000, 5000 * Math.pow(2, leg._failCount - 1));
          leg._nextPollTime = Date.now() + retryMs;
          console.warn(`[${this.name}] Poll failure ${leg._failCount} for ${leg.flightNumber}. ` +
            `Next attempt in ${retryMs / 1000}s. Error: ${result.reason.message}`);
        }
      });
    }

    if (this._apiCache) {
      const cutoff = Date.now() - 3600000;
      for (const key of Object.keys(this._apiCache)) {
        if (this._apiCache[key].ts < cutoff) delete this._apiCache[key];
      }
    }

    this.checkTripReset();
    if (updated) {
      this.sendSocketNotification("iAGT_FLIGHT_UPDATE", { legs: this.flightLegs });
    }
  },

  updateLegFromAPI (leg, data) {
    if (!data || !Array.isArray(data.flights) || data.flights.length === 0) return;
    
    /* Find the flight that matches our scheduled departureDate (ISO date part) */
    const flight = data.flights.find(f => {
      const sOut = f.scheduled_out || "";
      const aOut = f.actual_out || "";
      const sOff = f.scheduled_off || "";
      const aOff = f.actual_off || "";
      return sOut.startsWith(leg.departureDate) || 
             aOut.startsWith(leg.departureDate) || 
             sOff.startsWith(leg.departureDate) || 
             aOff.startsWith(leg.departureDate);
    }) || data.flights[0]; // fallback to first if no date match
    
    if (!flight) return;

    // Safety: If we fell back to data.flights[0], ensure it's at least for the same day 
    // or +- 1 day to avoid matching a flight from months ago that is already landed.
    const fDate = (flight.scheduled_out || flight.actual_out || flight.scheduled_off || flight.actual_off || "").split("T")[0];
    if (fDate) {
      const diffDays = Math.abs((new Date(fDate) - new Date(leg.departureDate)) / 86400000);
      if (diffDays > 1.5) {
        console.warn(`[${this.name}] Flight ${leg.flightNumber} found in AeroAPI but date ${fDate} is too far from ${leg.departureDate}. Skipping update.`);
        return;
      }
    }

    const s = (flight.status || "").toLowerCase();
    if (s.includes("scheduled")) {
      leg.status = "scheduled";
    } else if (
      s.includes("en route") || s.includes("en-route") || s.includes("enroute") ||
      s.includes("active") || s.includes("on the way") || s.includes("taxiing") || 
      s.includes("departed") || s.includes("diverted") || s.includes("flying") || 
      s.includes("airborne") || s.includes("in air") || s.includes("in-air") ||
      s.includes("in flight") || s.includes("in-flight")
    ) {
      leg.status = "active";
    } else if (s.includes("landed") || s.includes("arrived") || s.includes("completed")) {
      leg.status = "landed";
    } else if (s.includes("cancelled")) {
      leg.status = "cancelled";
    } else {
      leg.status = "scheduled";
    }

    if (typeof flight.progress_percent === "number" && !isNaN(flight.progress_percent)) {
      leg.progress = flight.progress_percent / 100;
    }

    if (flight.last_position) {
      const pos = flight.last_position;
      leg.currentLat         = pos.latitude       ?? leg.currentLat;
      leg.currentLon         = pos.longitude      ?? leg.currentLon;
      leg.groundspeed        = pos.groundspeed    != null ? pos.groundspeed    : leg.groundspeed;
      leg.altitude           = pos.altitude       != null ? pos.altitude       : leg.altitude;
      leg.heading            = pos.heading        != null ? pos.heading        : leg.heading;
      leg.altitudeChange     = pos.altitude_change != null ? pos.altitude_change : leg.altitudeChange;
      leg.lastPositionUpdate = pos.timestamp      || leg.lastPositionUpdate;
    }

    leg.actualDeparture  = flight.actual_out    || flight.scheduled_out || null;
    leg.estimatedArrival = flight.estimated_in  || flight.scheduled_in  || null;

    leg.departureTerminal = (flight.terminal_origin      != null) ? String(flight.terminal_origin)      : null;
    leg.departureGate     = (flight.gate_origin          != null) ? String(flight.gate_origin)          : null;
    leg.arrivalTerminal   = (flight.terminal_destination != null) ? String(flight.terminal_destination) : null;
    leg.arrivalGate       = (flight.gate_destination     != null) ? String(flight.gate_destination)     : null;

    leg.scheduledDeparture = flight.scheduled_out || flight.scheduled_off || null;
    leg.estimatedDeparture = flight.estimated_out || flight.actual_out    || null;
    leg.scheduledArrival   = flight.scheduled_in  || flight.scheduled_on  || null;
    leg.foresightEta       = (flight.foresight_predictions_available && flight.predicted_in)
                               ? flight.predicted_in : null;

    leg.aircraftType   = flight.aircraft_type || null;
    leg.tailNumber     = flight.registration  || flight.tail_number || null;
    leg.detailedStatus = flight.status        || null;
  },

  checkTripReset () {
    if (!this.flightLegs.length) return;

    const allDone = this.flightLegs.every(
      l => l.status === "landed" || l.status === "cancelled"
    );

    if (allDone && !this.tripCompleteTime) {
      this.tripCompleteTime = new Date();
      console.log(`[${this.name}] Trip complete at ${this.tripCompleteTime.toISOString()}`);
    }

    if (this.tripCompleteTime) {
      const elapsedDays = (new Date() - this.tripCompleteTime) / 86400000;
      const resetAfter  = this.config.colorResetAfterDays || 1;

      if (elapsedDays >= resetAfter) {
        this.sendSocketNotification("iAGT_TRIP_RESET", {});
        /* Stop polling after reset */
        if (this.pollTimer) { clearInterval(this.pollTimer); this.pollTimer = null; }
      }
    }
  },

  /* ─────────────────── FLIGHTAWARE AEROAPIV4 ──────────────────────────── */
  sleep (ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  },

  _normalizeIdent (fn) {
    if (!fn) return "";
    let ident = fn.replace(/\s+/g, "").toUpperCase();
    const map = {
      "VS":  "VIR",
      "BA":  "BAW",
      "UA":  "UAL",
      "AA":  "AAL",
      "DL":  "DAL",
      "AF":  "AFR",
      "LH":  "DLH",
      "KL":  "KLM",
      "EK":  "UAE",
      "QR":  "QTR",
      "EY":  "ETD",
      "SQ":  "SIA",
      "QF":  "QFA",
      "NZ":  "ANZ",
      "AC":  "ACA",
      "NH":  "ANA",
      "JL":  "JAL",
      "CX":  "CPA",
      "TG":  "THA",
      "MH":  "MAS",
      "OZ":  "AAR"
    };
    for (const [iata, icao] of Object.entries(map)) {
      if (ident.startsWith(iata) && !isNaN(parseInt(ident.substring(iata.length)))) {
        return icao + ident.substring(iata.length);
      }
    }
    return ident;
  },

  fetchFlightStatus (flightNumber, date, legStatus = "scheduled") {
    if (!(/^\d{4}-\d{2}-\d{2}$/).test(date)) {
      return Promise.reject(new Error(`Invalid date format: ${date}. Expected YYYY-MM-DD`));
    }

    this._apiCache = this._apiCache || {};
    const cacheKey = `${flightNumber}_${date}`;
    const cached   = this._apiCache[cacheKey];
    const hoursUntilDep = (new Date(date + "T00:00:00") - Date.now()) / 3600000;
    let ttl;
    if (legStatus === "active") {
      ttl = 60000;        // 1 min — en-route, positions update frequently
    } else if (legStatus === "landed") {
      ttl = 900000;       // 15 min — no further changes expected soon
    } else if (legStatus === "cancelled") {
      ttl = 1800000;      // 30 min — static state
    } else if (hoursUntilDep > 2) {
      ttl = 600000;       // 10 min — scheduled, departure >2 h away
    } else if (hoursUntilDep >= 0) {
      ttl = 120000;       // 2 min — scheduled, departure within 2 h
    } else {
      ttl = 30000;        // 30 s — departure time has passed, status still "scheduled"
                          // (FlightAware may flip to "en route" at any moment)
    }
    if (cached && (Date.now() - cached.ts) < ttl) {
      return Promise.resolve(cached.data);
    }

    const MAX_BODY = 512 * 1024;

    return new Promise((resolve, reject) => {
      const ident = encodeURIComponent(this._normalizeIdent(flightNumber));
      const headers = {
        "x-apikey": this.config.flightAwareApiKey,
        "Accept":   "application/json"
      };
      if (cached && cached.etag) {
        headers["If-None-Match"] = cached.etag;
      }

      // Widen the query window: 12h before to 36h after the start of departureDate
      // This ensures we catch flights that may have departed in another timezone
      // or are still in the air into the next calendar day.
      const startDate = new Date(date + "T00:00:00Z");
      startDate.setHours(startDate.getHours() - 12);
      const startStr = startDate.toISOString();

      const endDate = new Date(date + "T00:00:00Z");
      endDate.setHours(endDate.getHours() + 36);
      const endStr = endDate.toISOString();

      const opts = {
        hostname: "aeroapi.flightaware.com",
        path:     `/aeroapi/flights/${ident}?start=${encodeURIComponent(startStr)}&end=${encodeURIComponent(endStr)}`,
        method:   "GET",
        headers
      };

      console.log(`[${this.name}] Polling AeroAPI: ${flightNumber} (${this._normalizeIdent(flightNumber)}) for ${date}. Window: ${startStr} to ${endStr}`);

      const req = https.request(opts, res => {
        if (res.statusCode === 304 && cached) {
          this._apiCache[cacheKey].ts = Date.now();
          resolve(cached.data);
          return;
        }

        let body = "";
        res.on("data", chunk => {
          body += chunk;
          if (body.length > MAX_BODY) {
            req.destroy();
            reject(new Error("AeroAPI response too large"));
          }
        });
        res.on("end", () => {
          if (res.statusCode >= 400) {
            reject(new Error(`AeroAPI HTTP ${res.statusCode}: ${body.slice(0, 120)}`));
            return;
          }
          try {
            const parsed = JSON.parse(body);
            const count = (parsed && parsed.flights) ? parsed.flights.length : 0;
            console.log(`[${this.name}] AeroAPI response for ${flightNumber}: ${count} flights found`);
            if (count > 0 && parsed.flights[0].status) {
              console.log(`[${this.name}] First flight status: ${parsed.flights[0].status}`);
            }
            
            this._apiCache[cacheKey] = {
              ts:   Date.now(),
              data: parsed,
              etag: res.headers["etag"] || null
            };
            resolve(parsed);
          } catch (e) { reject(new Error(`JSON parse: ${e.message}`)); }
        });
      });

      req.on("error", reject);
      req.setTimeout(10000, () => { req.destroy(); reject(new Error("AeroAPI timeout")); });
      req.end();
    });
  },

  /* ─────────────────────── FILE SAVE HANDLERS ─────────────────────────── */
  async rotateDocuments (dir, limit = 20) {
    try {
      const files = await fs.promises.readdir(dir);
      if (files.length <= limit) return;
      
      const fileStats = await Promise.all(
        files.map(async f => {
          const fp = path.join(dir, f);
          const stat = await fs.promises.stat(fp);
          return { name: f, path: fp, mtime: stat.mtimeMs };
        })
      );
      
      fileStats.sort((a, b) => b.mtime - a.mtime); // Newest first
      const toDelete = fileStats.slice(limit);
      
      for (const f of toDelete) {
        await fs.promises.unlink(f.path);
        console.log(`[${this.name}] Rotated old document: ${f.name}`);
      }
    } catch (e) {
      console.warn(`[${this.name}] Rotation error in ${dir}: ${e.message}`);
    }
  },

  async saveAttractionsFile (payload) {
    try {
      const { cityName, things, airportPostcode, airportDistanceKm } = payload;
      const dir = path.join(__dirname, "documents", "MySavedCityAttractions");
      await fs.promises.mkdir(dir, { recursive: true });
      await this.rotateDocuments(dir);
      const slug     = (cityName || "city").toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "");
      const ts       = new Date().toISOString().replace(/[T:]/g, "-").replace(/\..+/, "").slice(0, 16);
      const fileName = `${slug}_${ts}.html`;
      await fs.promises.writeFile(path.join(dir, fileName), this._buildAttractionsHtml(cityName, things, airportPostcode, airportDistanceKm), "utf8");
      console.log(`[${this.name}] Saved attractions: ${fileName}`);
      this.sendSocketNotification("iAGT_SAVE_OK", { type: "attractions", fileName });
    } catch (e) {
      console.error(`[${this.name}] Save attractions error: ${e.message}`);
      this.sendSocketNotification("iAGT_SAVE_ERROR", { type: "attractions", error: e.message });
    }
  },

  async saveFlightsFile (payload) {
    try {
      const { legs, scenario } = payload;
      const dir = path.join(__dirname, "documents", "MySavedFlights");
      await fs.promises.mkdir(dir, { recursive: true });
      await this.rotateDocuments(dir);
      const ts       = new Date().toISOString().replace(/[T:]/g, "-").replace(/\..+/, "").slice(0, 16);
      const fileName = `flights_${ts}.html`;
      await fs.promises.writeFile(path.join(dir, fileName), this._buildFlightsHtml(legs, scenario), "utf8");
      console.log(`[${this.name}] Saved flights: ${fileName}`);
      this.sendSocketNotification("iAGT_SAVE_OK", { type: "flights", fileName });
    } catch (e) {
      console.error(`[${this.name}] Save flights error: ${e.message}`);
      this.sendSocketNotification("iAGT_SAVE_ERROR", { type: "flights", error: e.message });
    }
  },

  _nhEsc (s) {
    return String(s || "")
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  },

  _buildAttractionsHtml (cityName, things, airportPostcode, airportDistanceKm) {
    const now = new Date().toLocaleString();
    const esc = s => this._nhEsc(s);
    let rows = "";
    (things || []).forEach((t, i) => {
      rows += `<tr>
        <td class="num">${i + 1}</td>
        <td class="name">${esc(t.name)}</td>
        <td class="desc">${esc(t.description || "")}</td>
      </tr>`;
    });
    let airportLine = "";
    if (airportPostcode || airportDistanceKm != null) {
      const parts = [];
      if (airportPostcode)   parts.push(`Postcode: <strong>${esc(String(airportPostcode))}</strong>`);
      if (airportDistanceKm != null) parts.push(`Distance from city centre: <strong>${esc(String(airportDistanceKm))} km</strong>`);
      airportLine = `<p class="airport-meta">&#9992; Airport &mdash; ${parts.join(" &nbsp;&bull;&nbsp; ")}</p>`;
    }
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Top Attractions \u2013 ${esc(cityName)}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; color: #222; }
    h1   { font-size: 22px; margin-bottom: 4px; }
    .meta { font-size: 12px; color: #888; margin-bottom: 4px; }
    .airport-meta { font-size: 13px; color: #2C3E50; margin-bottom: 20px; }
    table { border-collapse: collapse; width: 100%; }
    th  { background: #2C3E50; color: #fff; padding: 8px 12px; text-align: left; font-size: 13px; }
    td  { padding: 7px 12px; border-bottom: 1px solid #eee; font-size: 13px; vertical-align: top; }
    .num  { color: #2255AA; font-weight: 700; width: 32px; text-align: center; }
    .name { font-weight: 600; width: 220px; }
    .desc { color: #555; }
    tr:hover td { background: #f5f9ff; }
    @media print { body { margin: 20px; } }
  </style>
</head>
<body>
  <h1>&#128205; Top Things To Do in ${esc(cityName)}</h1>
  <p class="meta">Saved: ${esc(now)}</p>
  ${airportLine}
  <table>
    <thead><tr><th>#</th><th>Attraction</th><th>Description</th></tr></thead>
    <tbody>${rows}</tbody>
  </table>
</body>
</html>`;
  },

  _buildFlightsHtml (legs, scenario) {
    const now = new Date().toLocaleString();
    const esc = s => this._nhEsc(s);
    const fmtDate = d => {
      if (!d) return "\u2014";
      const dt = new Date(d + "T00:00:00");
      return isNaN(dt.getTime()) ? d : dt.toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" });
    };
    const STATUS_LABEL = { scheduled: "Scheduled", active: "In Flight \u2708", landed: "Landed \u2713", cancelled: "Cancelled \u2717" };
    const STATUS_COLOR = { scheduled: "#555", active: "#2255AA", landed: "#007744", cancelled: "#CC2222" };

    const getSortKey = l => {
      if (l.actualDeparture) return new Date(l.actualDeparture).getTime();
      if (l.departureDate) {
        const t = l.departureTime ? `T${l.departureTime}:00` : "T00:00:00";
        return new Date(`${l.departureDate}${t}`).getTime();
      }
      return 0;
    };

    const sorted = [...(legs || [])].sort((a, b) => {
      if (scenario === 3) {
        const nc = (a.travelerName || "").localeCompare(b.travelerName || "");
        if (nc !== 0) return nc;
      }
      return getSortKey(a) - getSortKey(b);
    });

    let rows = "";
    sorted.forEach(l => {
      const st      = l.status || "scheduled";
      const color   = STATUS_COLOR[st]  || "#555";
      const label   = STATUS_LABEL[st]  || st;
      const pct     = st === "active" ? ` ${Math.round((l.progress || 0) * 100)}%` : "";
      const depStr  = fmtDate(l.departureDate) + (l.departureTime ? ` ${esc(l.departureTime)}` : "");
      const fromStr = l.from ? `${esc(l.from.name)} (${esc(l.from.iata)})` : "\u2014";
      const toStr   = l.to   ? `${esc(l.to.name)} (${esc(l.to.iata)})`   : "\u2014";
      rows += `<tr>
        <td>${esc(l.travelerName || "\u2014")}</td>
        <td class="fn">${esc(l.flightNumber || "\u2014")}</td>
        <td style="white-space:nowrap;">${depStr}</td>
        <td>${fromStr}</td>
        <td>${toStr}</td>
        <td style="color:${color};font-weight:700;">${esc(label)}${esc(pct)}</td>
      </tr>`;
    });

    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Flight Details</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; color: #222; }
    h1   { font-size: 22px; margin-bottom: 4px; }
    .meta { font-size: 12px; color: #888; margin-bottom: 20px; }
    table { border-collapse: collapse; width: 100%; }
    th  { background: #2C3E50; color: #fff; padding: 8px 12px; text-align: left; font-size: 13px; }
    td  { padding: 7px 12px; border-bottom: 1px solid #eee; font-size: 13px; vertical-align: top; }
    .fn { font-family: monospace; font-weight: 700; color: #8B6914; }
    tr:hover td { background: #f5f9ff; }
    @media print { body { margin: 20px; } }
  </style>
</head>
<body>
  <h1>&#9992; Flight Details</h1>
  <p class="meta">Saved: ${esc(now)}</p>
  <table>
    <thead>
      <tr><th>Name</th><th>Flight</th><th>Date / Time</th><th>From</th><th>To</th><th>Status</th></tr>
    </thead>
    <tbody>${rows}</tbody>
  </table>
</body>
</html>`;
  },

  async saveTerminalMapsFile (payload) {
    try {
      const { destinations } = payload;
      const dir = path.join(__dirname, "documents", "MySavedTerminalMaps");
      await fs.promises.mkdir(dir, { recursive: true });
      await this.rotateDocuments(dir);
      const ts       = new Date().toISOString().replace(/[T:]/g, "-").replace(/\..+/, "").slice(0, 16);
      const fileName = `terminal_maps_${ts}.html`;
      await fs.promises.writeFile(path.join(dir, fileName), this._buildTerminalMapsHtml(destinations), "utf8");
      console.log(`[${this.name}] Saved terminal maps: ${fileName}`);
      this.sendSocketNotification("iAGT_SAVE_OK", { type: "terminal_maps", fileName });
    } catch (e) {
      console.error(`[${this.name}] Save terminal maps error: ${e.message}`);
      this.sendSocketNotification("iAGT_SAVE_ERROR", { type: "terminal_maps", error: e.message });
    }
  },

  _buildTerminalMapsHtml (destinations) {
    const now = new Date().toLocaleString();
    const esc = s => this._nhEsc(s);
    let cards = "";
    (destinations || []).forEach(d => {
      const iata    = esc(d.iata  || "???");
      const name    = esc(d.name  || "Unknown Airport");
      const q       = encodeURIComponent(`${d.name || d.iata} terminal map`);
      const mapsUrl = `https://www.google.com/maps/search/${encodeURIComponent((d.name || d.iata) + " airport terminal")}`;
      const searchUrl = `https://www.google.com/search?q=${q}`;
      cards += `
      <div class="card">
        <div class="iata">${iata}</div>
        <div class="aname">${name}</div>
        <div class="links">
          <a href="${mapsUrl}" target="_blank">&#128506; Google Maps Terminal View</a>
          <a href="${searchUrl}" target="_blank">&#128269; Search Terminal Map</a>
        </div>
      </div>`;
    });
    if (!cards) {
      cards = `<p class="none">No destination airports found in flight data.</p>`;
    }
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Airport Terminal Maps</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; color: #222; background: #f8f9fa; }
    h1   { font-size: 22px; margin-bottom: 4px; color: #2C3E50; }
    .meta { font-size: 12px; color: #888; margin-bottom: 24px; }
    .grid { display: flex; flex-wrap: wrap; gap: 20px; }
    .card { background: #fff; border: 1px solid #dde; border-radius: 8px; padding: 20px 24px; min-width: 260px; flex: 1 1 260px; box-shadow: 0 1px 4px rgba(0,0,0,0.07); }
    .iata { font-size: 36px; font-weight: 700; color: #2255AA; letter-spacing: 3px; margin-bottom: 4px; }
    .aname { font-size: 15px; color: #333; margin-bottom: 14px; font-weight: 600; }
    .links { display: flex; flex-direction: column; gap: 8px; }
    .links a { display: inline-block; font-size: 13px; color: #2255AA; text-decoration: none; padding: 5px 10px; border: 1px solid #cce; border-radius: 4px; background: #f0f4ff; }
    .links a:hover { background: #dde8ff; }
    .none { color: #888; font-style: italic; }
    @media print { body { background: #fff; margin: 20px; } .links a { color: #000; } }
  </style>
</head>
<body>
  <h1>&#128506; Airport Terminal Maps</h1>
  <p class="meta">Saved: ${esc(now)}</p>
  <div class="grid">${cards}</div>
</body>
</html>`;
  },

  /* ─────────────────────── SCENARIO CACHING ──────────────────────────── */
  _getScenarioCachePath (scenario) {
    return path.join(__dirname, "cache", `scenario_${scenario}.json`);
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
        // Reject if config flights/travelers have changed
        if (fingerprint && cacheData.fingerprint !== fingerprint) return null;
        // Expiration check: 30 minutes
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

  /* ───────────────────── REGION / GEODATA ────────────────────────────── */
  _REGION_FILE_MAP: {
    "US": "usaLow",        "CA": "canadaLow",       "AU": "australiaLow",
    "DE": "germanyLow",    "FR": "franceDepartmentsLow", "JP": "japanLow",
    "CN": "chinaLow",      "IN": "indiaLow",         "BR": "brazilLow",
    "MX": "mexicoLow",     "RU": "russiaLow",        "PL": "polandLow",
    "IT": "italyProvincesLow", "ES": "spainProvincesLow", "NL": "netherlandsLow",
    "BE": "belgiumLow",    "AT": "austriaLow",        "AR": "argentinaLow",
    "ZA": "southAfricaLow","NG": "nigeriaLow",        "KR": "southKoreaLow",
    "TR": "turkeyLow",     "PK": "pakistanLow",       "ID": "indonesiaLow",
    "MY": "malaysiaLow",   "PH": "philippinesLow",    "TH": "thailandLow",
    "VN": "vietnamLow",    "NZ": "newZealandLow",     "CH": "switzerlandLow",
    "PT": "portugalRegionsLow", "GR": "greeceLow",    "SE": "swedenLow",
    "NO": "norwayLow",     "FI": "finlandLow",        "DK": "denmarkLow",
    "UA": "ukraineLow",    "RO": "romaniaLow",        "CZ": "czechiaLow",
    "HU": "hungaryLow",    "SK": "slovakiaLow",       "HR": "croatiaLow",
    "BA": "bosniaHerzegovinaCantonsLow", "RS": "serbiaLow", "BG": "bulgariaLow",
    "EG": "egyptLow",      "MA": "moroccoLow",        "DZ": "algeriaLow",
    "TN": "tunisiaLow",    "LY": "libyaLow",          "ET": "ethiopiaLow",
    "KE": "kenyaLow",      "TZ": "tanzaniaLow",       "UG": "ugandaLow",
    "GH": "ghanaLow",      "AO": "angolaLow",         "MZ": "mozambiqueLow",
    "ZM": "zambiaLow",     "ZW": "zimbabweLow",       "CO": "colombiaLow",
    "VE": "venezuelaLow",  "PE": "peruLow",            "CL": "chileLow",
    "BO": "boliviaLow",    "EC": "ecuadorLow",         "PY": "paraguayLow",
    "UY": "uruguayLow",    "IR": "iranLow",            "IQ": "iraqLow",
    "SA": "saudiArabiaLow","AF": "afghanistanLow",     "MM": "myanmarLow",
    "KZ": "kazakhstanLow", "KH": "cambodiaLow",        "LA": "laosLow",
    "KG": "kyrgyzstanLow", "MD": "moldovaLow",         "MN": "mongoliaLow",
    "LT": "lithuaniaLow",  "LV": "latviaLow",          "EE": "estoniaLow",
    "BY": "belarusLow",    "GE": "georgiaLow",         "AM": "armeniaLow",
    "AZ": "azerbaijanLow", "UZ": "uzbekistanLow",      "IE": "irelandProvincesLow",
    "CI": "cotedIvoireLow","CM": "cameroonLow",         "LU": "luxembourgLow",
    "MW": "malawiLow",     "NA": "namibiaLow",          "NP": "nepalLow",
    "SY": "syriaLow",      "YE": "yemenLow",            "BD": "bangladeshLow"
  },

  _COUNTRY_NAME_TO_ISO: {
    "Afghanistan": "AF", "Albania": "AL", "Algeria": "DZ", "Angola": "AO",
    "Argentina": "AR", "Armenia": "AM", "Australia": "AU", "Austria": "AT",
    "Azerbaijan": "AZ", "Bahrain": "BH", "Bangladesh": "BD", "Belarus": "BY",
    "Belgium": "BE", "Belize": "BZ", "Benin": "BJ", "Bolivia": "BO",
    "Bosnia and Herzegovina": "BA", "Botswana": "BW", "Brazil": "BR",
    "Brunei": "BN", "Bulgaria": "BG", "Burkina Faso": "BF", "Burundi": "BI",
    "Cambodia": "KH", "Cameroon": "CM", "Canada": "CA", "Cape Verde": "CV",
    "Central African Republic": "CF", "Chad": "TD", "Chile": "CL",
    "China": "CN", "Colombia": "CO", "Comoros": "KM", "Congo": "CG",
    "Costa Rica": "CR", "Croatia": "HR", "Cuba": "CU", "Cyprus": "CY",
    "Czech Republic": "CZ", "Czechia": "CZ", "Denmark": "DK",
    "Djibouti": "DJ", "Dominican Republic": "DO", "DR Congo": "CD",
    "Democratic Republic of the Congo": "CD", "Ecuador": "EC", "Egypt": "EG",
    "El Salvador": "SV", "Equatorial Guinea": "GQ", "Eritrea": "ER",
    "Estonia": "EE", "Ethiopia": "ET", "Eswatini": "SZ", "Swaziland": "SZ",
    "Finland": "FI", "France": "FR", "Gabon": "GA", "Georgia": "GE",
    "Germany": "DE", "Ghana": "GH", "Greece": "GR", "Guatemala": "GT",
    "Guinea": "GN", "Guinea-Bissau": "GW", "Guyana": "GY", "Haiti": "HT",
    "Honduras": "HN", "Hungary": "HU", "Iceland": "IS", "India": "IN",
    "Indonesia": "ID", "Iran": "IR", "Iraq": "IQ", "Ireland": "IE",
    "Israel": "IL", "Italy": "IT", "Jamaica": "JM", "Japan": "JP",
    "Jordan": "JO", "Kazakhstan": "KZ", "Kenya": "KE", "Kosovo": "XK",
    "Kuwait": "KW", "Kyrgyzstan": "KG", "Laos": "LA", "Latvia": "LV",
    "Lebanon": "LB", "Lesotho": "LS", "Liberia": "LR", "Libya": "LY",
    "Lithuania": "LT", "Luxembourg": "LU", "Madagascar": "MG",
    "Malawi": "MW", "Malaysia": "MY", "Mali": "ML", "Malta": "MT",
    "Mauritania": "MR", "Mauritius": "MU", "Mexico": "MX", "Moldova": "MD",
    "Mongolia": "MN", "Montenegro": "ME", "Morocco": "MA",
    "Mozambique": "MZ", "Myanmar": "MM", "Burma": "MM", "Namibia": "NA",
    "Nepal": "NP", "Netherlands": "NL", "New Zealand": "NZ",
    "Nicaragua": "NI", "Niger": "NE", "Nigeria": "NG", "North Korea": "KP",
    "North Macedonia": "MK", "Norway": "NO", "Oman": "OM", "Pakistan": "PK",
    "Panama": "PA", "Paraguay": "PY", "Peru": "PE", "Philippines": "PH",
    "Poland": "PL", "Portugal": "PT", "Qatar": "QA", "Romania": "RO",
    "Russia": "RU", "Rwanda": "RW", "Saudi Arabia": "SA", "Senegal": "SN",
    "Serbia": "RS", "Sierra Leone": "SL", "Slovakia": "SK", "Slovenia": "SI",
    "Somalia": "SO", "South Africa": "ZA", "South Korea": "KR",
    "South Sudan": "SS", "Spain": "ES", "Sri Lanka": "LK", "Sudan": "SD",
    "Sweden": "SE", "Switzerland": "CH", "Syria": "SY", "Taiwan": "TW",
    "Tanzania": "TZ", "Thailand": "TH", "Togo": "TG", "Tunisia": "TN",
    "Turkey": "TR", "Turkmenistan": "TM", "Uganda": "UG", "Ukraine": "UA",
    "United Arab Emirates": "AE", "United Kingdom": "GB",
    "United States": "US", "United States of America": "US", "USA": "US",
    "Uruguay": "UY", "Uzbekistan": "UZ", "Venezuela": "VE", "Vietnam": "VN",
    "Yemen": "YE", "Zambia": "ZM", "Zimbabwe": "ZW",
    "Ivory Coast": "CI", "Cote d'Ivoire": "CI", "Côte d'Ivoire": "CI",
    "Republic of the Congo": "CG"
  },

  async _loadGeoData (filename) {
    const geodataPath = path.join(__dirname, "node_modules", "@amcharts", "amcharts5-geodata", `${filename}.js`);
    try {
      const src = await fs.promises.readFile(geodataPath, "utf8");
      const withoutExport = src.replace(/export\s+default\s+map\s*;?\s*$/, "").trim();
      const withoutConst  = withoutExport.replace(/^const\s+map\s*=\s*/, "").trim();
      const jsonStr = withoutConst.endsWith(";") ? withoutConst.slice(0, -1) : withoutConst;
      return JSON.parse(jsonStr);
    } catch (e) {
      console.warn(`[${this.name}] Failed to load geodata ${filename}: ${e.message}`);
      return null;
    }
  },

  async _buildRegionData () {
    const regionData = {};
    if (!this.config || !this.config.showSubnationalRegions) return regionData;
    const countries = this.config.subnationalCountries || [];
    for (const iso of countries) {
      const key      = iso.toUpperCase();
      const filename = this._REGION_FILE_MAP[key];
      if (!filename) {
        console.warn(`[${this.name}] No region file mapping for ISO: ${iso}`);
        continue;
      }
      const geo = await this._loadGeoData(filename);
      if (geo) regionData[key] = geo;
    }
    return regionData;
  },

  _buildVisitedCountryIsos () {
    if (!this.config || this.config.scenario !== 4) return [];
    const isoSet = new Set(this._manualVisitedCountries || []);
    
    // Create a lower-case map for case-insensitive lookup
    const lowerMap = {};
    for (const [name, iso] of Object.entries(this._COUNTRY_NAME_TO_ISO)) {
      lowerMap[name.toLowerCase()] = iso;
    }

    this.flightLegs.forEach(leg => {
      if (leg.to && leg.to.country) {
        const country = leg.to.country.trim().toLowerCase();
        const iso = lowerMap[country];
        if (iso) isoSet.add(iso);
      }
    });
    return Array.from(isoSet);
  },

  async loadManualVisitedCountries () {
    const fp = path.join(__dirname, "data", "manual_visited_countries.json");
    try {
      const exists = await fs.promises.stat(fp).then(() => true).catch(() => false);
      if (exists) {
        const raw = await fs.promises.readFile(fp, "utf8");
        this._manualVisitedCountries = JSON.parse(raw);
      }
    } catch (e) {
      console.warn(`[${this.name}] Failed to load manual visited countries: ${e.message}`);
      this._manualVisitedCountries = [];
    }
  },

  async saveManualVisitedCountries () {
    const fp = path.join(__dirname, "data", "manual_visited_countries.json");
    try {
      await fs.promises.writeFile(fp, JSON.stringify(this._manualVisitedCountries, null, 2), "utf8");
    } catch (e) {
      console.error(`[${this.name}] Failed to save manual visited countries: ${e.message}`);
    }
  },

  /* ───────────────────────── CLEANUP ──────────────────────────────────── */
  stop () {
    if (this.pollTimer) { clearInterval(this.pollTimer); this.pollTimer = null; }
    console.log(`[${this.name}] node_helper stopped`);
  }
});

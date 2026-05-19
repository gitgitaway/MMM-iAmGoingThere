/* global am5, am5map, am5geodata_worldLow, iAGTGreatCircle */
/*
 * MagicMirrorÂ²
 * Module: MMM-iAmGoingThere
 *
 * Forked from MMM-iHaveBeenThere by Sebastian Merkel
 * https://github.com/basti0001/MMM-iHaveBeenThere
 *
 * Extended for future trip flight tracking with live FlightAware AeroAPI.
 *
 * Scenario 1 - Standard round trip  (home <-> destination, no stopovers)
 * Scenario 2 - Multi-leg Round The World trip (up to 10+ sequential legs)
 * Scenario 3 - Multi-origin trip (e.g. multiple family members departing from different cities to a common destination)
 * Scenario 4 - Where I Have Been (past trips from home to multiple destinations, no future flights)
 * Scenario 5 - CSV crew roster (parse a custom CSV file of flights, e.g. for airline crew or frequent travelers with complex itineraries)
 * Scenario 6 - Football Away Days (track upcoming matches in different cities with past match history, no future flights)
 *
 * Flight path colours:
 *   White  = Scheduled / future leg
 *   Blue   = In Flight  (progressive from origin as flight advances)
 *   Green  = Landed / completed
 *   Resets to White after colorResetAfterDays following final landing.
 *
 * MIT Licensed.
 */
Module.register("MMM-iAmGoingThere", {

	/* â”€â”€â”€ SCENARIO 3 TRAVELER COLOUR PALETTE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	/*
   * Palette deliberately excludes reds and orange-reds so no track colour
   * can clash with the plane icon (colorPlane default #FF6644 orange-red).
   */
	TRAVELER_COLORS: [
		"#4ECDC4", // teal
		"#FFE66D", // golden yellow
		"#A8E6CF", // mint
		"#C3A6FF", // lavender
		"#E040FB", // magenta
		"#40C4FF", // sky blue
		"#87CEEB", // pale blue
		"#F7D794", // peach
		"#98D8C8", // seafoam
		"#AEDE8C" // lime green
	],

	TRAVELER_SYMBOLS: [
		"\u25CF", // Circle
		"\u25A0", // Square
		"\u25B2", // Triangle Up
		"\u25C6", // Diamond
		"\u25BC", // Triangle Down
		"\u2605", // Star
		"\u271A", // Plus
		"\u2716", // Cross
		"\u2B22", // Hexagon
		"\u2B1F" // Pentagon
	],

	/* ─── UIX-002: Color-blind-friendly traveler palette ─────────────────────
	 * Based on IBM's color-blind-safe palette — distinguishable under
	 * Deuteranopia, Protanopia, and Tritanopia.
	 * Deliberately excludes orange-red to avoid clash with the plane icon.
	 */
	TRAVELER_COLORS_CB: [
		"#648FFF", // blue
		"#785EF0", // violet
		"#DC267F", // rose
		"#FFB000", // amber
		"#00B5D8", // cyan
		"#009D72", // green
		"#FE6100", // orange  (distinct from #FF6644 plane at this saturation)
		"#C2E0FF", // pale blue
		"#FFD699", // pale amber
		"#C8A2C8"  // lilac
	],

	TARGET_SVG: "M9,0C4.029,0,0,4.029,0,9s4.029,9,9,9s9-4.029,9-9S13.971,0,9,0z M9,15.93 c-3.83,0-6.93-3.1-6.93-6.93S5.17,2.07,9,2.07s6.93,3.1,6.93,6.93S12.83,15.93,9,15.93 M12.5,9c0,1.933-1.567,3.5-3.5,3.5S5.5,10.933,5.5,9S7.067,5.5,9,5.5 S12.5,7.067,12.5,9z",
	PLANE_SVG: "M 0,-150 L -10,-80 L -130,-20 L -130,20 L -10,20 L -20,80 L -50,120 L -50,150 L 0,130 L 50,150 L 50,120 L 20,80 L 10,20 L 130,20 L 130,-20 L 10,-80 Z",

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ DEFAULT CONFIGURATION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	defaults: {
		// 1. Scenario & Core
		scenario: 1, // 1=round trip | 2=multi-leg RTW | 3=multi-origin | 4=where I have been | 5=CSV crew roster | 6=football trips
		showWhereIHaveBeen: false, // Scenario 4: show return flights for all destinations
		tripTitle: "Our Destination", // Appended to "We Are On Our Way To â€“"
		overideDate: false, // Set all flights takeoff time to now + 5 minutes for this session only
		departureAlertHours: 0, // Hours before first departure to send a notification (0 = disabled)

		// 2. FlightAware AeroAPI
		flightAwareApiKey: "", // Required for live tracking
		pollInterval: 5, // Minutes between FlightAware polls

		// 3. Map Settings
		mapHeight: 700,
		mapProjection: "mercator", // "mercator" | "naturalEarth1" | "equirectangular" | "orthographic" | "stereographic"
		hideIceCaps: false,
		zoomLevel: 1,
		zoomLongitude: 0,
		zoomLatitude: 20,
		autoRotateGlobeToPlane: false, // Orthographic only: rotate globe to center on active plane(s)
		gcPoints: 100, // Great-circle interpolation points per leg
		lowPowerMode: false, // PER-002: Disable heavy CSS effects and reduce gcPoints for low-power hardware (e.g. Raspberry Pi Zero)
		displayDesc: true, // Show airport name labels
		showCityInfo: false,
		citiesFile: "data/cities.csv",
		cityInfoMode: "destination", // "destination" | "layovers"
		cityInfoCycleInterval: 20, // Seconds per city when cityInfoMode = "layovers"
		narrowBreakpoint: 900, // px â€” below this width both overlay panels switch to 95vw stacked layout

		// 4. Graticule Grid
		showGraticule: false,
		colorGraticule: "#ffffff",
		graticuleOpacity: 0.2,
		graticuleWidth: 0.5,
		graticuleStep: 10,

		// 5. Sub-national Regions
		showSubnationalRegions: false,
		subnationalAllCountries: false, // true = show regions for all supported countries
		subnationalCountries: [], // ISO-2 codes, e.g. ["US", "CA", "DE"]

		// 6. UI Controls (Onscreen)
		showPanControl: true,
		showZoomControl: true,
		showNudgeControl: true,
		showProjectionSelector: true,
		showVisitedSelector: true,
		showModeSelector: true,
		showScenarioSelector: true,
		showMapSelector: true, // Legacy alias for Projection + Visited selectors
		hideControlsUntilHover: false,

		// 7. Flight Details Overlay
		showFlightDetails: false,
		autoHideOverlays: false,
		autoHideDelay: 30,
		flightPanelWidth: "46vw",
		flightPanelHeight: "32vh",
		setFlightDetailsTextSize: "xsmall", // xsmall | small | medium | large | xlarge
		showTable: false, // Legacy alias
		tableX: 0,
		tableY: 0,

		// 8. Attractions Overlay
		showAttractionsDetails: false,
		attractionsPanelWidth: "50vw",
		attractionsPanelHeight: "32vh",
		setAttractionsDetailsTextSize: "xsmall",
		autoRotateAttractionsData: false,
		attractionsAutoScroll: false,
		attractionsScrollInterval: 3,
		maxAttractionsDisplay: 5,
		cityAttractions_Xaxis: 0,
		cityAttractions_Yaxis: 0,

		// 9. Flight Tracking & Animation
		showFlightTracks: "auto", // "auto" | "true" | "false" | "test"
		flightDisplayMode: "all", // "all" | "outbound" | "return"
		testModeDuration: 3,
		testModeDelay: 3,
		animationEnabled: true,
		pauseDuration: 3.0,
		animationDuration: 10.0,
		showPlaneShadow: true,

		// 10. Airport & Destination Markers
		showDestinations: true,
		tooltipDuration: 6,
		colorAirportHome: "#FFD700",
		colorAirportOther: "#FFFFFF",

		// 11. Colours (Map & Paths)
		colorMapBackground: "#000000",
		colorMapOcean: "#1A1A2E",
		colorCountries: "#2C3E50",
		colorCountryBorders: "#1A252F",
		colorVisitedCountry: "#00AA44",
		colorVisitedCountryBorder: "#008833",
		colorVisitedCountryOpacity: 0.75,
		colorFuturePath: "#FFFFFF",
		colorActivePath: "#4499FF",
		colorCompletedPath: "#00CC66",
		colorPreviousPath: "#888888",
		colorCancelledPath: "#FF4444",
		colorPlane: "#FF6644",
		colorTitleFont: "#FFFFFF",
		colorLegendFont: "#FFFFFF",
		colorLegendBorder: "#FFFFFF",
		colorBlindMode: false,
		colorResetAfterDays: 1,

		// 13. UIX-001: Zen Mode — hides all controls + overlays after inactivity
		zenMode: false,

		// 14. UIX-003: Fly-to — click flight row to zoom map to that leg
		flyToOnRowClick: true,

		// 15. INN-001: Destination Fun Facts (Wikipedia)
		funFactsEnabled: false,

		// 16. INN-002: Calendar-Driven Scenario Switching
		calendarDrivenScenario: false,
		calendarScenarioMap: [], // e.g. [{ keyword: "football", scenario: 6 }, { keyword: "holiday", scenario: 1 }]

		// 12. Data Sources
		home: { name: "Home Airport", iata: "HOME", lat: 51.5074, lon: -0.1278 },
		destination: null,
		flights: [],
		travelers: [],
		crewFlightsFile: "data/my_flights.csv"
	},

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ MAGICMIRROR LIFECYCLE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	getStyles: function () {
		return [this.file("MMM-iAmGoingThere.css")];
	},

	getScripts: function () {
		Log.info("[MMM-iAmGoingThere] getScripts returning local vendor scripts");
		return [
			this.file("lib/iAGT.StateController.js"),
			this.file("lib/iAGT.FlightProcessor.js"),
			this.file("lib/greatCircle.js"),
			this.file("vendor/index.js"),
			this.file("vendor/map.js"),
			this.file("vendor/worldLow.js")
		];
	},

	getTranslations: function () {
		return {
			en: "translations/en.json",
			de: "translations/de.json",
			fr: "translations/fr.json",
			es: "translations/es.json",
			nl: "translations/nl.json",
			it: "translations/it.json",
			pt: "translations/pt.json",
			gd: "translations/gd.json",
			ga: "translations/ga.json",
			af: "translations/af.json",
			ar: "translations/ar.json",
			cs: "translations/cs.json",
			cy: "translations/cy.json",
			da: "translations/da.json",
			el: "translations/el.json",
			fa: "translations/fa.json",
			fi: "translations/fi.json",
			hr: "translations/hr.json",
			ht: "translations/ht.json",
			hu: "translations/hu.json",
			ja: "translations/ja.json",
			ko: "translations/ko.json",
			mi: "translations/mi.json",
			no: "translations/no.json",
			pl: "translations/pl.json",
			ro: "translations/ro.json",
			sk: "translations/sk.json",
			sl: "translations/sl.json",
			sr: "translations/sr.json",
			sv: "translations/sv.json",
			tr: "translations/tr.json",
			uk: "translations/uk.json",
			uz: "translations/uz.json"
		};
	},

	_esc (str) {
		return String(str ?? "")
			.replace(/&/g, "&amp;")
			.replace(/</g, "&lt;")
			.replace(/>/g, "&gt;")
			.replace(/"/g, "&quot;");
	},

	/* TZ-001: Convert a leg's local departure date+time to UTC milliseconds.
	 * Priority: live API ISO timestamps → config date+time (adjusted for airport
	 * longitude-based UTC offset) → config date only (midday local assumption).
	 * This ensures flights near or past the International Date Line are correctly
	 * classified as past/future regardless of the viewer's local timezone.       */
	_legDepartureUtcMs (leg) {
		if (leg.estimatedDeparture) return new Date(leg.estimatedDeparture).getTime();
		if (leg.scheduledDeparture) return new Date(leg.scheduledDeparture).getTime();
		if (leg.actualDeparture)    return new Date(leg.actualDeparture).getTime();
		if (!leg.departureDate) return 0;
		const baseMs = Date.parse(leg.departureDate + "T00:00:00Z");
		if (isNaN(baseMs)) return 0;
		let timeMin = 12 * 60;
		if (leg.departureTime && typeof leg.departureTime === "string") {
			const parts = leg.departureTime.split(":");
			const h = parseInt(parts[0], 10);
			const m = parseInt(parts[1] || "0", 10);
			if (!isNaN(h) && !isNaN(m)) timeMin = h * 60 + m;
		}
		let lonOffsetMin = 0;
		if (leg.from && leg.from.lon != null) {
			lonOffsetMin = Math.round(parseFloat(leg.from.lon) / 15) * 60;
		}
		return baseMs + (timeMin - lonOffsetMin) * 60000;
	},

	_getEffectiveConfig () {
		let cfg = this.config;
		const scen = cfg.scenario;
		if (cfg.scenarios && cfg.scenarios[scen]) {
			cfg = Object.assign({}, cfg, cfg.scenarios[scen]);
		} else {
			cfg = Object.assign({}, cfg);
		}

		// Backward compatibility for UI flags
		if (cfg.showMapSelector === false) {
			if (cfg.showProjectionSelector === undefined) cfg.showProjectionSelector = false;
			if (cfg.showVisitedSelector === undefined) cfg.showVisitedSelector = false;
		}
		if (cfg.showScenarioSelector === false) {
			if (cfg.showModeSelector === undefined) cfg.showModeSelector = false;
		}

		// PER-002: Low Power Mode — cap gcPoints to reduce CPU load
		if (cfg.lowPowerMode) {
			cfg.gcPoints = Math.min(cfg.gcPoints || 100, 30);
		}

		return cfg;
	},

	_safeColor (c) {
		return (/^#[0-9A-Fa-f]{3,8}$|^rgba?\(/).test(c) ? c : "#FFFFFF";
	},

	getDom: function () {
		const cfg = this._getEffectiveConfig();
		const wrapper = document.createElement("div");
		let wrapClass = "iAGT-wrapper";
		if (cfg.lowPowerMode)   wrapClass += " iagt-low-power";
		if (cfg.colorBlindMode) wrapClass += " iagt-cb-mode";
		if ("ontouchstart" in window || navigator.maxTouchPoints > 0) wrapClass += " iagt-touch";
		wrapper.className = wrapClass;
		wrapper.id = `iAGT-wrapper-${this.identifier}`;

		/* ── Responsive breakpoint style injection ── */
		{
			const bp = Number.isFinite(cfg.narrowBreakpoint) ? cfg.narrowBreakpoint : 900;
			const styleId = `iAGT-narrow-style-${this.identifier}`;
			let styleEl = document.getElementById(styleId);
			if (!styleEl) {
				styleEl = document.createElement("style");
				styleEl.id = styleId;
				document.head.appendChild(styleEl);
			}
			styleEl.textContent = `@media (max-width: ${bp}px) {
  #iAGT-wrapper-${this.identifier} .iAGT-table-overlay,
  #iAGT-wrapper-${this.identifier} .iAGT-city-info-overlay {
    width: 95vw !important;
    left: 2.5vw !important;
    right: auto !important;
    max-width: none !important;
  }
  #iAGT-wrapper-${this.identifier} .iAGT-city-info-overlay {
    bottom: 0 !important;
    top: auto !important;
  }
  #iAGT-wrapper-${this.identifier} .iAGT-table-overlay {
    bottom: calc(${cfg.attractionsPanelHeight || "32vh"} + 8px) !important;
  }
}
@media (max-width: 480px) {
  #iAGT-wrapper-${this.identifier} .iAGT-city-info-overlay {
    bottom: 0 !important;
    top: auto !important;
    height: 26vh !important;
  }
  #iAGT-wrapper-${this.identifier} .iAGT-table-overlay {
    bottom: calc(26vh + 6px) !important;
    height: 26vh !important;
  }
}
#iAGT-wrapper-${this.identifier}.iagt-touch .iAGT-controls-auto-hide {
  opacity: 1 !important;
  pointer-events: auto !important;
}
#iAGT-wrapper-${this.identifier}.iagt-touch .iAGT-nudge-control {
  opacity: 1 !important;
}`;
		}

		/* ── Header ── */
		const header = document.createElement("div");
		header.className = "iAGT-header";

		const titleEl = document.createElement("div");
		titleEl.className = "iAGT-title";
		titleEl.id = `iAGT-title-${this.identifier}`;
		titleEl.innerHTML = `${this.translate("TITLE_PREFIX")} &ndash; <span class="iAGT-dest">${this._esc(cfg.tripTitle)}</span>`;
		header.appendChild(titleEl);

		const cdWrap = document.createElement("div");
		cdWrap.className = "iAGT-countdown-wrap";
		const cdEl = document.createElement("div");
		cdEl.className = "iAGT-countdown";
		cdEl.id = `iAGT-countdown-${this.identifier}`;
		cdEl.setAttribute("role", "status");
		cdEl.setAttribute("aria-live", "polite");
		cdEl.innerHTML = `<div class="iAGT-cd-main"><span class="iAGT-cd-icon">&#9203;</span><span class="iAGT-cd-text">${this.translate("LOADING")}</span></div><div class="iAGT-cd-subtitle" id="iAGT-cd-subtitle-${this.identifier}"></div>`;
		cdWrap.appendChild(cdEl);
		header.appendChild(cdWrap);
		wrapper.appendChild(header);

		/* â”€â”€ Map container â”€â”€ */
		const mapCont = document.createElement("div");
		mapCont.className = "iAGT-map-container";

		const mapDiv = document.createElement("div");
		mapDiv.id = `iAGTMapDiv-${this.identifier}`;
		mapDiv.style.width = "100%";
		mapDiv.style.height = "100%";
		mapDiv.style.position = "relative";
		mapDiv.style.zIndex = "1";

		const loadingEl = document.createElement("div");
		loadingEl.className = "iAGT-map-loading";
		loadingEl.id = `iAGT-map-loading-${this.identifier}`;
		loadingEl.textContent = this.translate("LOADING");
		mapDiv.appendChild(loadingEl);

		mapCont.appendChild(mapDiv);

		/* ── ACC-002: Hidden Live Region for Status Announcements ── */
		const announcer = document.createElement("div");
		announcer.id = `iAGT-announcer-${this.identifier}`;
		announcer.className = "iAGT-announcer visual-hidden";
		announcer.setAttribute("aria-live", "polite");
		announcer.setAttribute("aria-atomic", "true");
		wrapper.appendChild(announcer);

		/* ── Nudge Control (relative movement) ── */
		if (cfg.showNudgeControl) {
			const nudgeCtrl = document.createElement("div");
			nudgeCtrl.className = "iAGT-nudge-control";
			nudgeCtrl.innerHTML = `
				<button class="iAGT-nudge-btn iAGT-nudge-up" data-dir="nudge_up" aria-label="Nudge Up">▲</button>
				<button class="iAGT-nudge-btn iAGT-nudge-down" data-dir="nudge_down" aria-label="Nudge Down">▼</button>
				<button class="iAGT-nudge-btn iAGT-nudge-left" data-dir="nudge_left" aria-label="Nudge Left">◀</button>
				<button class="iAGT-nudge-btn iAGT-nudge-right" data-dir="nudge_right" aria-label="Nudge Right">▶</button>
			`;
			nudgeCtrl.querySelectorAll("button").forEach((btn) => {
				btn.addEventListener("click", (e) => {
					e.preventDefault();
					this._handleMapControl(btn.getAttribute("data-dir"));
				});
			});
			mapCont.appendChild(nudgeCtrl);
		}

		/* ── Map controls ── */
		const ctrlWrap = document.createElement("div");
		ctrlWrap.className = "iAGT-map-controls";
		if (cfg.hideControlsUntilHover) {
			ctrlWrap.classList.add("iAGT-controls-auto-hide");
		}
		ctrlWrap.style.zIndex = "10";

		if (cfg.showPanControl) {
			const panCtrl = document.createElement("div");
			panCtrl.className = "iAGT-pan-control";
			panCtrl.innerHTML = `
				<button class="iAGT-pan-btn iAGT-pan-up" data-dir="up" aria-label="Pan Up">N</button>
				<button class="iAGT-pan-btn iAGT-pan-down" data-dir="down" aria-label="Pan Down">S</button>
				<button class="iAGT-pan-btn iAGT-pan-left" data-dir="left" aria-label="Pan Left">W</button>
				<button class="iAGT-pan-btn iAGT-pan-right" data-dir="right" aria-label="Pan Right">E</button>
				<button class="iAGT-pan-btn iAGT-pan-center" data-dir="home" aria-label="Recenter Map">
					<div class="iAGT-needle">
						<div class="iAGT-needle-north"></div>
						<div class="iAGT-needle-south"></div>
					</div>
				</button>
			`;
			ctrlWrap.appendChild(panCtrl);
		}

		if (cfg.showZoomControl) {
			const zoomCtrl = document.createElement("div");
			zoomCtrl.className = "iAGT-zoom-control";
			zoomCtrl.innerHTML = `
				<button class="iAGT-zoom-btn iAGT-zoom-in" data-dir="in" aria-label="Zoom In">+</button>
				<button class="iAGT-zoom-btn iAGT-zoom-out" data-dir="out" aria-label="Zoom Out">-</button>
			`;
			ctrlWrap.appendChild(zoomCtrl);
		}

		// Top selectors
		if (cfg.showProjectionSelector) {
			const mapSel = document.createElement("div");
			mapSel.className = "iAGT-top-selector iAGT-map-selector";
			mapSel.innerHTML = `
				<select class="iAGT-selector-dropdown" id="iAGT-projection-select">
					<option value="mercator" ${cfg.mapProjection === "mercator" ? "selected" : ""}>Mercator</option>
					<option value="equirectangular" ${cfg.mapProjection === "equirectangular" ? "selected" : ""}>Equirectangular</option>
					<option value="naturalEarth1" ${cfg.mapProjection === "naturalEarth1" ? "selected" : ""}>Natural Earth</option>
					<option value="orthographic" ${cfg.mapProjection === "orthographic" ? "selected" : ""}>Globe (Orthographic)</option>
				</select>
			`;
			mapSel.querySelector("select").addEventListener("change", (e) => {
				this.config.mapProjection = e.target.value;
				this._updateProjection();
			});
			ctrlWrap.appendChild(mapSel);
		}

		if (cfg.showVisitedSelector) {
			const visitedSel = document.createElement("div");
			visitedSel.className = "iAGT-top-selector iAGT-visited-selector";
			visitedSel.id = `iAGT-visited-ctrl-${this.identifier}`;
			const _vhl = this._state.visitedHighlightEnabled !== false;
			const _gv = this._state.graticuleSeries ? this._state.graticuleSeries.get("visible") : cfg.showGraticule;
			visitedSel.innerHTML = `
				<select class="iAGT-selector-dropdown" id="iAGT-visited-select-${this.identifier}">
					<option value="show_graticule" ${_gv ? "selected" : ""}>${this.translate("VISITED_DRP_SHOW_GRATICULE")}</option>
					<option value="hide_graticule" ${!_gv ? "selected" : ""}>${this.translate("VISITED_DRP_HIDE_GRATICULE")}</option>
					<option value="highlight" ${_vhl ? "selected" : ""}>${this.translate("VISITED_DRP_HIGHLIGHT")}</option>
					<option value="none" ${!_vhl ? "selected" : ""}>${this.translate("VISITED_DRP_NONE")}</option>
					<option value="clear">${this.translate("VISITED_DRP_CLEAR")}</option>
					<option value="show_regions" ${this._state.regionsVisible ? "selected" : ""}>${this.translate("SUB_DRP_SHOW")}</option>
					<option value="hide_regions" ${!this._state.regionsVisible ? "selected" : ""}>${this.translate("SUB_DRP_HIDE")}</option>
				</select>
			`;
			visitedSel.querySelector("select").addEventListener("change", (e) => {
				const val = e.target.value;
				if (val === "show_graticule") {
					this._toggleGraticules(true);
				} else if (val === "hide_graticule") {
					this._toggleGraticules(false);
				} else if (val === "highlight") {
					this._state.visitedHighlightEnabled = true;
					this._applyVisitedCountriesColors();
				} else if (val === "none") {
					this._state.visitedHighlightEnabled = false;
					this._applyVisitedCountriesColors();
				} else if (val === "clear") {
					e.target.value = "highlight";
					this._state.visitedHighlightEnabled = true;
					this.sendSocketNotification("iAGT_CLEAR_VISITED_COUNTRIES", {});
				} else if (val === "show_regions") {
					this._toggleRegionLayers(true);
				} else if (val === "hide_regions") {
					this._toggleRegionLayers(false);
				}
			});
			ctrlWrap.appendChild(visitedSel);
		}

		if (cfg.showModeSelector) {
			// Mode selector (Auto/Test)
			const modeSel = document.createElement("div");
			modeSel.className = "iAGT-top-selector iAGT-mode-selector";
			const currMode = String(this.config.showFlightTracks);
			modeSel.innerHTML = `
				<select class="iAGT-selector-dropdown" id="iAGT-mode-select">
					<option value="auto" ${currMode === "auto" ? "selected" : ""}>Mode: Live Tracking</option>
					<option value="test" ${currMode === "test" ? "selected" : ""}>Mode: Test Animation</option>
				</select>
			`;
			modeSel.querySelector("select").addEventListener("change", (e) => {
				const mVal = e.target.value;
				this.config.showFlightTracks = mVal;
				if (mVal === "test") {
					this.startTestAnimation();
				} else {
					this.stopTestAnimation();
					// Trigger a fresh init to restore live state
					this.sendSocketNotification("iAGT_CONFIG", this.config);
				}
			});
			ctrlWrap.appendChild(modeSel);
		}

		if (cfg.showScenarioSelector) {
			const scenSel = document.createElement("div");
			scenSel.className = "iAGT-top-selector iAGT-scenario-selector";
			scenSel.innerHTML = `
				<select class="iAGT-selector-dropdown" id="iAGT-scenario-select">
					<option value="1" ${cfg.scenario === 1 ? "selected" : ""}>Scenario 1: Round Trip</option>
					<option value="2" ${cfg.scenario === 2 ? "selected" : ""}>Scenario 2: Multi-leg RTW</option>
					<option value="3" ${cfg.scenario === 3 ? "selected" : ""}>Scenario 3: Multi-origin</option>
					<option value="4" ${cfg.scenario === 4 ? "selected" : ""}>Scenario 4: Where I Have Been</option>
					<option value="5" ${cfg.scenario === 5 ? "selected" : ""}>Scenario 5: CSV Roster</option>
					<option value="6" ${cfg.scenario === 6 ? "selected" : ""}>Scenario 6: Football Away Days</option>
				</select>
			`;
			scenSel.querySelector("select").addEventListener("change", (e) => {
				const sVal = parseInt(e.target.value, 10);
				this.config.scenario = sVal;
				this.sendSocketNotification("UPDATE_SCENARIO", { scenario: sVal });
			});
			ctrlWrap.appendChild(scenSel);
		}

		// Event listeners for controls
		ctrlWrap.querySelectorAll("button").forEach((btn) => {
			btn.addEventListener("click", (e) => {
				e.preventDefault();
				const dir = btn.getAttribute("data-dir");
				this._handleMapControl(dir);
			});
		});

		mapCont.appendChild(ctrlWrap);

		/* â”€â”€ Overlay flight table â”€â”€ */
		const showFlight = cfg.showFlightDetails || cfg.showTable;
		if (showFlight) {
			const tblDiv = document.createElement("div");
			tblDiv.className = `iAGT-table-overlay iAGT-fs-${cfg.setFlightDetailsTextSize || "small"}`;
			tblDiv.id = `iAGT-table-${this.identifier}`;
			tblDiv.setAttribute("role", "region");
			tblDiv.setAttribute("aria-label", this.translate("TABLE_TITLE"));
			const tX = Number.isFinite(cfg.tableX) ? cfg.tableX : 0;
			const tY = Number.isFinite(cfg.tableY) ? cfg.tableY : 0;
			tblDiv.style.position = "absolute";
			tblDiv.style.left = `${tX}px`;
			tblDiv.style.bottom = `${tY}px`;
			tblDiv.style.right = "";
			tblDiv.style.top = "";
			tblDiv.style.width = cfg.flightPanelWidth;
			tblDiv.style.height = cfg.flightPanelHeight;
			tblDiv.style.zIndex = "150"; // anchor from bottom-left
			tblDiv.innerHTML = this.buildTableHTML([]);
			wrapper.appendChild(tblDiv);
		}

		/* ── City info panel ── */
		const showAtts = cfg.showAttractionsDetails || cfg.showCityInfo;
		if (showAtts) {
			const ciDiv = document.createElement("div");
			ciDiv.className = `iAGT-city-info-overlay iAGT-atts-${cfg.setAttractionsDetailsTextSize || "small"}`;
			ciDiv.id = `iAGT-city-info-${this.identifier}`;
			ciDiv.setAttribute("role", "complementary");
			ciDiv.setAttribute("aria-label", this.translate("TOP10_TITLE"));
			ciDiv.style.position = "absolute";
			ciDiv.style.bottom = `${Number.isFinite(cfg.cityAttractions_Yaxis) ? cfg.cityAttractions_Yaxis : 0}px`;
			ciDiv.style.right  = `${Number.isFinite(cfg.cityAttractions_Xaxis) ? cfg.cityAttractions_Xaxis : 0}px`;
			ciDiv.style.top = "";
			ciDiv.style.left = "";
			ciDiv.style.width = cfg.attractionsPanelWidth;
			ciDiv.style.height = cfg.attractionsPanelHeight;
			ciDiv.style.zIndex = "200";
			wrapper.appendChild(ciDiv);
		}

		/* ── Reserve space at bottom equal to the tallest visible overlay panel ── */
		/*
     * The overlay panels are position:absolute at bottom:0.
     * Setting padding-bottom on the wrapper (box-sizing:border-box, height:100vh)
     * means the flex map child stops exactly at the top edge of the tallest panel.
     */
		{
			const parseVh = (s) => parseFloat(s) || 0;
			const heights = [];
			if (showFlight) heights.push(parseVh(cfg.flightPanelHeight));
			if (showAtts)   heights.push(parseVh(cfg.attractionsPanelHeight));
			const tallest = heights.length ? Math.max(...heights) : 0;
			if (tallest > 0) wrapper.style.paddingBottom = `${tallest}vh`;
		}

		wrapper.appendChild(mapCont);

		/* ── UIX-001: Zen Mode interaction listeners ── */
		if (cfg.zenMode) {
			const _zenReset = () => this._resetZenModeTimer();
			wrapper.addEventListener("mousemove",  _zenReset, { passive: true });
			wrapper.addEventListener("click",      _zenReset, { passive: true });
			wrapper.addEventListener("keydown",    _zenReset, { passive: true });
			wrapper.addEventListener("touchstart", _zenReset, { passive: true });
		}

		this._resetOverlayHideTimer();
		this._resetZenModeTimer();

		return wrapper;
	},

	_resetOverlayHideTimer () {
		const cfg = this._getEffectiveConfig();
		if (!cfg.autoHideOverlays) return;
		
		const tbl = document.getElementById(`iAGT-table-${this.identifier}`);
		const ci = document.getElementById(`iAGT-city-info-${this.identifier}`);
		if (tbl) { tbl.style.transition = "opacity 0.5s"; tbl.style.opacity = "1"; }
		if (ci) { ci.style.transition = "opacity 0.5s"; ci.style.opacity = "1"; }

		if (this._state.overlayHideTimer) {
			clearTimeout(this._state.overlayHideTimer);
		}
		this._state.overlayHideTimer = setTimeout(() => {
			this._hideOverlays();
		}, (cfg.autoHideDelay || 30) * 1000);
	},

	_hideOverlays () {
		const cfg = this._getEffectiveConfig();
		if (!cfg.autoHideOverlays) return;
		const tbl = document.getElementById(`iAGT-table-${this.identifier}`);
		const ci = document.getElementById(`iAGT-city-info-${this.identifier}`);
		if (tbl) tbl.style.opacity = "0";
		if (ci) ci.style.opacity = "0";
	},

	/* ── UIX-001: Zen Mode — hide ALL controls after inactivity ── */
	_resetZenModeTimer () {
		const cfg = this._getEffectiveConfig();
		if (!cfg.zenMode) return;
		const wrapper = document.getElementById(`iAGT-wrapper-${this.identifier}`);
		if (wrapper) wrapper.classList.remove("iagt-zen-active");
		if (this._state.zenModeTimer) clearTimeout(this._state.zenModeTimer);
		this._state.zenModeTimer = setTimeout(() => {
			const w = document.getElementById(`iAGT-wrapper-${this.identifier}`);
			if (w) w.classList.add("iagt-zen-active");
		}, (cfg.autoHideDelay || 30) * 1000);
	},

	/* ── INN-001: Display Fun Fact in the city info panel header ── */
	_displayFunFact (cityName) {
		const city = cityName || this._state.currentDisplayedCity;
		const text = (this._state.funFactCache || {})[city];
		if (!text) return;
		const ciDiv = document.getElementById(`iAGT-city-info-${this.identifier}`);
		if (!ciDiv) return;
		let bar = ciDiv.querySelector(".iAGT-fun-fact-bar");
		if (!bar) {
			bar = document.createElement("div");
			bar.className = "iAGT-fun-fact-bar";
			ciDiv.insertBefore(bar, ciDiv.firstChild);
		}
		bar.innerHTML = `<span class="iAGT-fun-fact-icon">&#x1F4A1;</span><span class="iAGT-fun-fact-text">${this._esc(text)}</span>`;
	},

	_requestAndDisplayFunFact (cityName) {
		if (!cityName) return;
		const cfg = this._getEffectiveConfig();
		if (!cfg.funFactsEnabled) return;
		if (!this._state.funFactCache) this._state.funFactCache = {};
		if (this._state.funFactCache[cityName]) {
			this._displayFunFact(cityName);
		} else {
			this.sendSocketNotification("iAGT_GET_FUN_FACT", { cityName });
		}
	},

	/* ── UIX-003: Fly-to — animate map to midpoint of a flight leg ── */
	_flyToLeg (lat1, lon1, lat2, lon2) {
		if (!this._state.mapChart) return;
		const chart = this._state.mapChart;
		const midLat = (lat1 + lat2) / 2;
		const midLon = (lon1 + lon2) / 2;
		const dLat = Math.abs(lat2 - lat1);
		const dLon = Math.abs(lon2 - lon1);
		const span = Math.max(dLat, dLon);
		const targetZoom = span < 10 ? 6 : span < 30 ? 4 : span < 60 ? 2.5 : 1.5;
		chart.animate({ key: "rotationX",  to: -midLon,    duration: 800, easing: am5.ease.out(am5.ease.cubic) });
		chart.animate({ key: "rotationY",  to: -midLat,    duration: 800, easing: am5.ease.out(am5.ease.cubic) });
		chart.animate({ key: "zoomLevel",  to: targetZoom, duration: 800, easing: am5.ease.out(am5.ease.cubic) });
	},

	_getWeatherIcon (code) {
		const icons = {
			0: "\u2600", // Clear sky
			1: "\uD83C\uDF24", 2: "\uD83C\uDF24", 3: "\u2601", // Partly cloudy, cloudy
			45: "\uD83C\uDF2B", 48: "\uD83C\uDF2B", // Fog
			51: "\uD83C\uDF26", 53: "\uD83C\uDF26", 55: "\uD83C\uDF26", // Drizzle
			61: "\uD83C\uDF27", 63: "\uD83C\uDF27", 65: "\uD83C\uDF27", // Rain
			71: "\u2744", 73: "\u2744", 75: "\u2744", // Snow
			77: "\u2744", // Snow grains
			80: "\uD83C\uDF27", 81: "\uD83C\uDF27", 82: "\uD83C\uDF27", // Rain showers
			85: "\u2744", 86: "\u2744", // Snow showers
			95: "\u26C8", // Thunderstorm
			96: "\u26C8", 99: "\u26C8" // Thunderstorm with hail
		};
		return icons[code] || "\u23FB";
	},

	start () {
		this._state = new IagtStateController(this.config);
		Log.info(`[${this.name}] Starting`);
		this.sendSocketNotification("iAGT_CONFIG", this.config);
		this._state.cdTimer = setInterval(() => { this.updateCountdown(); }, 60000);
	},

	/* ACC-002: Hidden live region announcer */
	_announce (msg) {
		const el = document.getElementById(`iAGT-announcer-${this.identifier}`);
		if (el) {
			el.textContent = "";
			setTimeout(() => { el.textContent = msg; }, 100);
		}
	},

	socketNotificationReceived (notification, payload) {
		switch (notification) {
			case "iAGT_INIT":
				this._state.tripReset = false;
				this._state.flightLegs = payload.legs || [];
				this._state.cityInfo = payload.cityInfo || {};
				this._state.visitedCountryIsos = payload.visitedCountryIsos || [];
				this._state.regionData = payload.regionData || {};
				this._state.cityIndex = 0;
				this._buildTravelerMap();
				this._cacheGreatCirclePoints();
				this.updateCountdown();
				this.updateCityInfo();
				this.updateTitle();
				this.startCityInfoCycling();
				this._scheduleAlertTimer();
				if (this._state.mapReady && this._state.polygonSeries) {
					this._applyVisitedCountriesColors();
				}
				setTimeout(() => { this.initMap(); }, 300);
				if (this._state.weatherRefreshTimer) clearInterval(this._state.weatherRefreshTimer);
				this._state.weatherRefreshTimer = setInterval(() => { this._refreshWeather(); }, 3600000);
				break;

			case "iAGT_FLIGHT_UPDATE": {
				const cfg = this._getEffectiveConfig();
				if (String(cfg.showFlightTracks) === "test") break; // test mode owns leg state
				this._state.flightLegs = payload.legs || [];
				this._state.cityDisplayListCache = null;
				this._cacheGreatCirclePoints();
				{
					const filteredLegs = this._getFilteredLegs();
					this.updateCountdown(filteredLegs);
					this.updateMapLines(filteredLegs);
					this.updateTable(filteredLegs);
					this._resetOverlayHideTimer();
					if (!this._state.attractionsScrollTimer && !this._state.lastShownCity) {
						this.updateCityInfo();
					}
					this._maybeAutoRotateAttractions(filteredLegs);
				}
				break;
			}

			case "iAGT_TRIP_RESET":
				this._state.tripReset = true;
				this._state.flightLegs.forEach((l) => { l.status = "scheduled"; l.progress = 0; });
				this.updateMapLines();
				this.updateTable();
				this.updateCountdown();
				break;
			case "iAGT_NO_API_KEY":
				this._state.noApiKey = true;
				this.updateCountdown();
				break;

			case "iAGT_WEATHER_UPDATE": {
				const { cityName: wCity, weather: wData } = payload;
				if (wCity && wData && this._state.cityInfo[wCity]) {
					this._state.cityInfo[wCity].weather = wData;
					this._state.cityInfo[wCity].weatherUpdatedAt = Date.now();
					if (this._state.currentDisplayedCity === wCity) {
						this._renderCityByName(wCity);
					}
				}
				break;
			}

			case "iAGT_SAVE_OK":
			case "iAGT_SAVE_ERROR": {
				const ok = notification === "iAGT_SAVE_OK";
				const { type } = payload;
				if (this._state.pendingSaveEl && this._state.pendingSaveEl.type === type) {
					const panelEl = document.getElementById(this._state.pendingSaveEl.panelId);
					const btnSel = type === "flights" ? ".iAGT-save-flights-btn" : type === "terminal_maps" ? ".iAGT-save-terminal-btn" : ".iAGT-save-atts-btn";
					const defaultIcon = type === "terminal_maps" ? "\uD83D\uDDFA" : "\uD83D\uDDA8";
					const btn = panelEl && panelEl.querySelector(btnSel);
					if (btn) {
						btn.textContent = ok ? "\u2713" : "\u2717";
						btn.style.color = ok ? "#00CC66" : "#FF4444";
						btn.disabled = false;
						clearTimeout(this._state.saveToastTimer);
						this._state.saveToastTimer = setTimeout(() => {
							btn.textContent = defaultIcon;
							btn.style.color = "";
						}, 3000);
					}
					this._state.pendingSaveEl = null;
				}
				break;
			}

			case "iAGT_FUN_FACT": {
				const { cityName: ffCity, fact } = payload;
				if (fact && ffCity) {
					if (!this._state.funFactCache) this._state.funFactCache = {};
					this._state.funFactCache[ffCity] = fact;
					if (this._state.currentDisplayedCity === ffCity) this._displayFunFact(ffCity);
				}
				break;
			}
		}
	},

	/* ── INN-002: Calendar-Driven Scenario Switching ── */
	notificationReceived (notification, payload) {
		if (notification !== "CALENDAR_EVENTS") return;
		const cfg = this._getEffectiveConfig();
		if (!cfg.calendarDrivenScenario) return;
		const map = cfg.calendarScenarioMap;
		if (!Array.isArray(map) || !map.length) return;

		const events = Array.isArray(payload) ? payload : (payload && payload.events ? payload.events : []);
		if (!events.length) return;

		const now = Date.now();
		const upcoming = events.filter((ev) => {
			const start = ev.startDate || ev.start_date || 0;
			return start >= now / 1000 || start * 1000 >= now;
		});

		for (const rule of map) {
			const kw = (rule.keyword || "").toLowerCase();
			const targetScenario = parseInt(rule.scenario, 10);
			if (!kw || isNaN(targetScenario)) continue;
			const match = upcoming.find((ev) => {
				const title = (ev.title || ev.summary || "").toLowerCase();
				return title.includes(kw);
			});
			if (match && this.config.scenario !== targetScenario) {
				Log.info(`[${this.name}] INN-002: Calendar event "${match.title || match.summary}" matched keyword "${kw}" → switching to Scenario ${targetScenario}`);
				this.config.scenario = targetScenario;
				this.sendSocketNotification("UPDATE_SCENARIO", { scenario: targetScenario });
				break;
			}
		}
	},

	/* ─────────────── TRAVELER COLOUR & SYMBOL MAP  (Scenario 3) ─────────────── */
	_buildTravelerMap () {
		const cfg = this._getEffectiveConfig();
		const palette = cfg.colorBlindMode ? this.TRAVELER_COLORS_CB : this.TRAVELER_COLORS;
		const result = IagtFlightProcessor.buildTravelerMap(this._state.flightLegs, palette, this.TRAVELER_SYMBOLS);
		this._state.travelerColors = result.colors;
		this._state.travelerSymbols = result.symbols;
	},

	_getLegColor (leg) {
		const cfg = this._getEffectiveConfig();
		return IagtFlightProcessor.getLegColor(leg, this._state.travelerColors, cfg.scenario);
	},

	/* ─────────────────── CACHE GREAT CIRCLE POINTS ─────────────────────────── */
	_cacheGreatCirclePoints () {
		const cfg = this._getEffectiveConfig();
		IagtFlightProcessor.cacheGreatCirclePoints(this._state.flightLegs, cfg.gcPoints || 100);
	},

	/* â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€ GREAT CIRCLE PATH  (SLERP spherical interpolation) â"€â"€â"€â"€â"€ */
	generateGreatCirclePoints (lat1, lon1, lat2, lon2, n) {
		return IagtFlightProcessor.generateGreatCirclePoints(lat1, lon1, lat2, lon2, n);
	},

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ ANTIMERIDIAN SPLIT (Deprecated in amCharts 5) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	/*
   * amCharts 5 handles antimeridian crossing natively with lineType: "curved".
   * Keeping this as dead code for initial migration safety.
   */
	_splitAtAntimeridian (pts) {
		if (!pts || pts.length < 2) return pts ? [pts] : [];
		const segments = [];
		let current = [pts[0]];

		for (let i = 1; i < pts.length; i++) {
			const dLon = pts[i].lon - pts[i - 1].lon;

			if (Math.abs(dLon) > 180) {

				/* â”€â”€ Crossing detected â”€â”€ */
				const prevLat = pts[i - 1].lat;
				const currLat = pts[i].lat;
				const prevLon = pts[i - 1].lon;

				/* "Short-way" longitude delta (what the arc actually traverses) */
				const shortDLon = dLon > 0 ? dLon - 360 : dLon + 360;

				/* Fraction of the segment where we hit the Â±180Â° edge */
				const edgeLon = prevLon >= 0 ? 180 : -180;
				const t = Math.abs((edgeLon - prevLon) / shortDLon);
				const crossLat = prevLat + t * (currLat - prevLat);

				/* Close current segment at the edge, start new one at the mirror edge */
				current.push({ lat: crossLat, lon: edgeLon });
				segments.push(current);
				current = [{ lat: crossLat, lon: -edgeLon }];
			}

			current.push(pts[i]);
		}

		segments.push(current);
		return segments.filter((s) => s.length > 1);
	},

	/*
   * Helper: convert an array of points into a GeoJSON Feature
   * ready for amCharts 5 MapLineSeries.
   */
	_segmentsToLine (pts, customColor) {
		return IagtFlightProcessor.segmentsToLine(pts, customColor);
	},

	/* â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€ BEARING  (degrees clockwise from North) â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€ */
	_calculateBearing (lat1, lon1, lat2, lon2) {
		return IagtFlightProcessor.calculateBearing(lat1, lon1, lat2, lon2);
	},

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ FILTERED LEGS (Outbound/Return/All) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	_getFilteredLegs () {
		const cfg = this._getEffectiveConfig();
		return IagtFlightProcessor.getFilteredLegs(this._state.flightLegs, cfg.flightDisplayMode);
	},

	/* â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€ MAP LINE BUILDER â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€ */
	buildMapLines (legs) {
		if (!legs) legs = this._getFilteredLegs();
		const cfg = this._getEffectiveConfig();
		return IagtFlightProcessor.buildMapLines(legs, cfg, this._state.travelerColors, this._state.tripReset);
	},

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ AIRPORT MARKERS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	buildAirportMarkers (legs) {
		if (!legs) legs = this._getFilteredLegs();
		const cfg = this._getEffectiveConfig();
		return IagtFlightProcessor.buildAirportMarkers(legs, cfg, this._state.travelerColors, this._state.tripReset, cfg.gcPoints || 60);
	},

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ MAP INIT & UPDATE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	initMap () {
		if (typeof am5 === "undefined" || typeof am5map === "undefined" || typeof am5geodata_worldLow === "undefined") {
			Log.warn(`[${this.name}] amCharts 5 components not yet defined, retrying in 500ms...`);
			setTimeout(() => { this.initMap(); }, 500);
			return;
		}

		const cfg = this._getEffectiveConfig();
		const divId = `iAGTMapDiv-${this.identifier}`;
		if (!document.getElementById(divId)) {
			Log.error(`[${this.name}] Map div not found: ${divId}`);
			return;
		}

		try {
			// 1. Root
			const currentDiv = document.getElementById(divId);
			const projKey = (cfg.mapProjection || "mercator").toLowerCase().replace(/[^a-z0-9]/g, "");
			
			if (this._state.mapRoot) {
				// Optimization: If map already exists, is attached to the current div, 
				// AND the projection hasn't changed, don't dispose the root.
				if (this._state.mapReady && this._state.mapRootContainer === currentDiv && this._state.lastProjection === projKey) {
					const zoomLon  = (cfg.zoomLongitude !== undefined && cfg.zoomLongitude !== null) ? Number(cfg.zoomLongitude) : 0;
					const zoomLat  = (cfg.zoomLatitude  !== undefined && cfg.zoomLatitude  !== null) ? Number(cfg.zoomLatitude)  : 0;
					const zoomLvl  = (cfg.zoomLevel     !== undefined && cfg.zoomLevel     !== null) ? Number(cfg.zoomLevel)     : 1;

					if (this._state.mapChart) {
						this._state.mapChart.setAll({
							homeZoomLevel: zoomLvl,
							homeGeoPoint:  { longitude: zoomLon, latitude: zoomLat },
							homeRotationX: -zoomLon,
							homeRotationY: -zoomLat
						});
					}

					this.stopTestAnimation();
					this._flushMapLines(this._state.flightLegs);
					this._state.mapChart.goHome(0);
					if (String(cfg.showFlightTracks) === "test") this.startTestAnimation();
					this._startGlobeAutoRotation();
					return;
				}
				this._stopGlobeAutoRotation();
				this._state.mapRoot.dispose();
				this._state.mapRoot = null;
				this._state.mapRootContainer = null;
				this._state.polygonSeries = null;
				this._state.mapReady = false;
			}
			const root = am5.Root.new(divId);
			this._state.mapRoot = root;
			this._state.mapRootContainer = currentDiv;
			this._state.lastProjection = projKey;

			// 2. Chart
			/*
       * homeZoomLevel / homeRotationX / homeRotationY are the properties
       * consumed by goHome().  Setting them here means a single goHome(0)
       * call after first render correctly positions AND zooms the map.
       * zoomLevel 1 = full world; higher values zoom in.
       */
			const zoomLon  = (cfg.zoomLongitude !== undefined && cfg.zoomLongitude !== null) ? Number(cfg.zoomLongitude) : 0;
			const zoomLat  = (cfg.zoomLatitude  !== undefined && cfg.zoomLatitude  !== null) ? Number(cfg.zoomLatitude)  : 0;
			const zoomLvl  = (cfg.zoomLevel     !== undefined && cfg.zoomLevel     !== null) ? Number(cfg.zoomLevel)     : 1;
			const _projMap = {
				mercator:        () => am5map.geoMercator(),
				naturalearth1:   () => am5map.geoNaturalEarth1(),
				equirectangular: () => am5map.geoEquirectangular(),
				orthographic:    () => am5map.geoOrthographic(),
				stereographic:   () => am5map.geoStereographic()
			};
			const _projKey = (cfg.mapProjection || "mercator").toLowerCase().replace(/[^a-z0-9]/g, "");
			const _projFn  = (_projMap[_projKey] || _projMap["mercator"]);
			const chart = root.container.children.push(
				am5map.MapChart.new(root, {
					projection:    _projFn(),
					panX:          "rotateX",
					panY:          "rotateY",
					wheelX:        "none",
					wheelY:        "none",
					rotationX:     -zoomLon,
					rotationY:     -zoomLat,
					zoomLevel:     zoomLvl,
					homeZoomLevel: zoomLvl,
					homeGeoPoint:  { longitude: zoomLon, latitude: zoomLat },
					homeRotationX: -zoomLon,
					homeRotationY: -zoomLat
				})
			);
			this._state.mapChart = chart;

			// Listen for rotation changes to update compass needle
			chart.on("rotationX", () => {
				const needle = document.querySelector(`.iAGT-needle`);
				if (needle) {
					needle.style.transform = `rotate(${chart.get("rotationX")}deg)`;
				}
			});

			// 3a. Outer area (outside the map projection, e.g. corners around a globe)
			chart.chartContainer.get("background").setAll({
				fill:        am5.color(this._safeColor(cfg.colorMapBackground || "#000000")),
				fillOpacity: 1
			});

			// 3b. Ocean fill inside the map projection — a world-rectangle polygon series
			//     placed first so it sits behind countries
			const oceanSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {}));
			oceanSeries.mapPolygons.template.setAll({
				fill:         am5.color(this._safeColor(cfg.colorMapOcean || "#1A1A2E")),
				fillOpacity:  1,
				strokeOpacity: 0
			});
			oceanSeries.data.push({
				geometry: am5map.getGeoRectangle(90, 180, -90, -180)
			});

			// 4. Country polygon series
			const polygonSeries = chart.series.push(
				am5map.MapPolygonSeries.new(root, {
					geoJSON: am5geodata_worldLow,
					exclude: (cfg.hideIceCaps && cfg.mapProjection !== "orthographic") ? ["AQ"] : []
				})
			);
			polygonSeries.mapPolygons.template.setAll({
				fill: am5.color(this._safeColor(cfg.colorCountries)),
				fillOpacity: 0.6,
				stroke: am5.color(this._safeColor(cfg.colorCountryBorders)),
				strokeWidth: 0.5,
				tooltipText: "{name}",
				interactive: true,
				cursorOverStyle: "pointer"
			});

			// 4b. Scenario 4: colour visited countries — applied after data renders
			this._state.polygonSeries = polygonSeries;
			polygonSeries.events.on("datavalidated", () => {
				this._applyVisitedCountriesColors();
			});

			// 4b-2. Manual coloring via right-click — shows confirmation popup
			polygonSeries.mapPolygons.template.events.on("rightclick", (ev) => {
				const dataItem = ev.target.dataItem;
				if (dataItem && dataItem.dataContext && dataItem.dataContext.id) {
					const iso = dataItem.dataContext.id;
					const name = dataItem.dataContext.name || iso;
					const isVisited = (this._state.visitedCountryIsos || []).includes(iso);
					this._showVisitedPopup(iso, name, isVisited);
				}
			});

			// 4c. Graticule — uses same data.setAll() pattern as flight tracks to ensure
			//     template adapters fire correctly (geoJSON constructor path bypasses adapters).
			const step    = Number(cfg.graticuleStep) || 10;
			const color   = am5.color(this._safeColor(cfg.colorGraticule || "#ffffff"));
			const opacity = cfg.graticuleOpacity != null ? Number(cfg.graticuleOpacity) : 0.2;
			const width   = Number(cfg.graticuleWidth) || 0.5;

			this._state.graticuleSeries = chart.series.push(am5map.MapLineSeries.new(root, {
				visible: cfg.showGraticule
			}));

			this._state.graticuleSeries.mapLines.template.setAll({
				stroke:        color,
				strokeOpacity: opacity,
				strokeWidth:   width
			});
			this._state.graticuleSeries.mapLines.template.adapters.add("stroke",        () => color);
			this._state.graticuleSeries.mapLines.template.adapters.add("strokeOpacity", () => opacity);
			this._state.graticuleSeries.mapLines.template.adapters.add("strokeWidth",   () => width);

			const features = [];
			for (let lat = -80; lat <= 80; lat += step) {
				const coords = [];
				for (let lon = -180; lon <= 180; lon += 2) coords.push([lon, lat]);
				features.push({ type: "Feature", properties: {}, geometry: { type: "LineString", coordinates: coords } });
			}
			for (let lon = -180; lon < 180; lon += step) {
				const coords = [];
				for (let lat = -90; lat <= 90; lat += 2) coords.push([lon, lat]);
				features.push({ type: "Feature", properties: {}, geometry: { type: "LineString", coordinates: coords } });
			}

			this._state.graticuleSeries.data.setAll(features);

			// 4d. Sub-national region layers
			if (this.config.showSubnationalRegions) {
				this._initRegionLayers(root, chart);
			}

			// 5. Flight path line series (one per status bucket)
			this._initLineSeries(root, chart);

			// 6. Airport + plane point series
			this._initPointSeries(root, chart);

			// 7. Initial Viewport Zoom â€” set rotation/zoom directly on first frame.
			//    rotationX/rotationY/zoomLevel are already set in the constructor so
			//    the first render is correct; this redundant call ensures any deferred
			//    resize recalculation doesn't reset them.
			chart.events.once("frameended", () => {
				chart.setAll({
					rotationX: -zoomLon,
					rotationY: -zoomLat,
					zoomLevel: zoomLvl
				});
			});

			// 8. Ready
			this._state.mapReady = true;
			const loadingPlaceholder = document.getElementById(`iAGT-map-loading-${this.identifier}`);
			if (loadingPlaceholder) loadingPlaceholder.remove();
			this.updateTable();

			if (String(cfg.showFlightTracks) === "test") this.startTestAnimation();

			this.updateMapLines();
			this._startGlobeAutoRotation();

		} catch (e) {
			Log.error(`[${this.name}] amCharts 5 failed: ${e.message}`);
			const mapDiv = document.getElementById(divId);
			if (mapDiv) {
				mapDiv.innerHTML = `<div class="iAGT-map-error">
          <p><strong>${this.translate("MAP_ERROR_TITLE") || "Map Error"}</strong></p>
          <p>${this._esc(e.message)}</p>
        </div>`;
			}
		}
	},

	_handleMapControl (dir) {
		if (!this._state.mapChart) return;
		const chart = this._state.mapChart;
		const cfg = this._getEffectiveConfig();
		const rotStep = 0.5;

		switch (dir) {
			case "up":
				const nextYUp = (chart.get("rotationY") || 0) + rotStep;
				chart.animate({ key: "rotationY", to: nextYUp, duration: 300, easing: am5.ease.out(am5.ease.cubic) });
				break;
			case "down":
				const nextYDown = (chart.get("rotationY") || 0) - rotStep;
				chart.animate({ key: "rotationY", to: nextYDown, duration: 300, easing: am5.ease.out(am5.ease.cubic) });
				break;
			case "left":
				const nextXLeft = (chart.get("rotationX") || 0) + rotStep;
				chart.animate({ key: "rotationX", to: nextXLeft, duration: 300, easing: am5.ease.out(am5.ease.cubic) });
				break;
			case "right":
				const nextXRight = (chart.get("rotationX") || 0) - rotStep;
				chart.animate({ key: "rotationX", to: nextXRight, duration: 300, easing: am5.ease.out(am5.ease.cubic) });
				break;
			case "in":
				const nextZIn = (chart.get("zoomLevel") || 1) + 0.5;
				chart.animate({ key: "zoomLevel", to: nextZIn, duration: 300, easing: am5.ease.out(am5.ease.cubic) });
				break;
			case "out":
				const nextZOut = Math.max(1, (chart.get("zoomLevel") || 1) - 0.5);
				chart.animate({ key: "zoomLevel", to: nextZOut, duration: 300, easing: am5.ease.out(am5.ease.cubic) });
				break;
			case "home":
				const homeLon = cfg.home ? (cfg.home.lon || 0) : 0;
				const homeLat = cfg.home ? (cfg.home.lat || 0) : 0;
				chart.animate({ key: "rotationX", to: -homeLon, duration: 600, easing: am5.ease.out(am5.ease.cubic) });
				chart.animate({ key: "rotationY", to: -homeLat, duration: 600, easing: am5.ease.out(am5.ease.cubic) });
				chart.animate({ key: "zoomLevel", to: 1, duration: 600, easing: am5.ease.out(am5.ease.cubic) });
				chart.animate({ key: "dx", to: 0, duration: 600, easing: am5.ease.out(am5.ease.cubic) });
				chart.animate({ key: "dy", to: 0, duration: 600, easing: am5.ease.out(am5.ease.cubic) });
				break;
			case "nudge_up":
				chart.set("dy", (chart.get("dy") || 0) - 10);
				break;
			case "nudge_down":
				chart.set("dy", (chart.get("dy") || 0) + 10);
				break;
			case "nudge_left":
				chart.set("dx", (chart.get("dx") || 0) - 10);
				break;
			case "nudge_right":
				chart.set("dx", (chart.get("dx") || 0) + 10);
				break;
		}
	},

	_updateProjection () {
		if (!this._state.mapChart) return;
		const cfg = this._getEffectiveConfig();
		const proj = (cfg.mapProjection || "mercator").toLowerCase().replace(/[^a-z0-9]/g, "");
		let am5proj;
		switch (proj) {
			case "equirectangular": am5proj = am5map.geoEquirectangular(); break;
			case "naturalearth1":   am5proj = am5map.geoNaturalEarth1();   break;
			case "orthographic":    am5proj = am5map.geoOrthographic();    break;
			case "stereographic":   am5proj = am5map.geoStereographic();   break;
			case "mercator":
			default:                am5proj = am5map.geoMercator();        break;
		}
		this._state.mapChart.set("projection", am5proj);

		if (this._state.polygonSeries) {
			this._state.polygonSeries.set("exclude", (this.config.hideIceCaps && proj !== "orthographic") ? ["AQ"] : []);
		}
	},

	_initLineSeries (root, chart) {
		const cfg = this._getEffectiveConfig();
		this._ls = {};
		const cbm = cfg.colorBlindMode;

		const createSeries = (key, color, thickness, dash) => {
			const series = chart.series.push(am5map.MapLineSeries.new(root, {
				lineType: "curved"
			}));
			series.mapLines.template.setAll({
				stroke: am5.color(this._safeColor(color)),
				strokeWidth: thickness,
				strokeOpacity: 0.9,
				strokeDasharray: dash
			});

			// Adapter for Scenario 3 traveler colours
			series.mapLines.template.adapters.add("stroke", (stroke, target) => {
				const customColor = target.dataItem?.dataContext?.properties?.customColor;
				return customColor ? am5.color(customColor) : stroke;
			});

			// Adapter for color blind mode dashLength differentiation
			if (cbm) {
				series.mapLines.template.adapters.add("strokeDasharray", (dashArray, target) => {
					// scheduled: [8, 4], active: [], landed: [4, 4], previous: [4, 4], tail: [8, 4], cancelled: [8, 4]
					// We already set defaults in createSeries calls below, but this ensures 
					// any dynamic changes (if any) respect the mode.
					return dashArray;
				});
			}

			this._ls[key] = series;
		};

		createSeries("scheduled", cfg.colorFuturePath, 1, cbm ? [8, 4] : []);
		createSeries("active", cfg.colorActivePath, 3, []);
		createSeries("tail", cfg.colorFuturePath, 1, [8, 4]);
		createSeries("landed", cfg.colorCompletedPath, 2, cbm ? [4, 4] : []);
		createSeries("previous", cfg.colorPreviousPath, 2, cbm ? [4, 4] : []);
		createSeries("cancelled", cfg.colorCancelledPath, 1, [8, 4]);
	},

	_initRegionLayers (root, chart) {
		const regionData = this._state.regionData || {};
		const isos = Object.keys(regionData);
		this._state.regionSeriesList = [];
		if (isos.length === 0) return;

		const LAYER_COLORS = [
			{ base: "#2A3F6A", hover: "#3A5F9A", active: "#5080C0", border: "#1A2F5A" },
			{ base: "#2A5A3F", hover: "#3A8A5F", active: "#50B080", border: "#1A4A2F" },
			{ base: "#5A3A6A", hover: "#8A5A9A", active: "#B07AC0", border: "#4A2A5A" },
			{ base: "#6A5A2A", hover: "#9A8A3A", active: "#C0B050", border: "#5A4A1A" },
			{ base: "#6A2A2A", hover: "#9A4A4A", active: "#C06060", border: "#5A1A1A" },
			{ base: "#2A5A6A", hover: "#3A8A9A", active: "#50A0B0", border: "#1A4A5A" },
			{ base: "#6A3A2A", hover: "#9A5A3A", active: "#C07050", border: "#5A2A1A" },
			{ base: "#4A2A6A", hover: "#6A3A9A", active: "#8A50C0", border: "#3A1A5A" }
		];

		isos.forEach((iso, idx) => {
			const geoJSON = regionData[iso];
			if (!geoJSON) return;

			const colors = LAYER_COLORS[idx % LAYER_COLORS.length];

			const regionSeries = chart.series.push(
				am5map.MapPolygonSeries.new(root, { geoJSON, visible: this._state.regionsVisible })
			);
			this._state.regionSeriesList.push(regionSeries);

			regionSeries.mapPolygons.template.setAll({
				fill:           am5.color(this._safeColor(colors.base)),
				fillOpacity:    0.75,
				stroke:         am5.color(this._safeColor(colors.border)),
				strokeWidth:    0.5,
				tooltipText:    "{name}",
				cursorOverStyle: "pointer",
				interactive:    true,
				toggleKey:      "active"
			});

			regionSeries.mapPolygons.template.states.create("hover", {
				fill:        am5.color(this._safeColor(colors.hover)),
				fillOpacity: 0.9
			});

			regionSeries.mapPolygons.template.states.create("active", {
				fill:        am5.color(this._safeColor(colors.active)),
				fillOpacity: 1.0
			});
		});
	},

	_toggleRegionLayers (visible) {
		this._state.regionsVisible = visible;
		this._state.regionSeriesList.forEach((series) => {
			series.set("visible", visible);
		});
	},

	_toggleGraticules (visible) {
		if (this._state.graticuleSeries) {
			this._state.graticuleSeries.set("visible", visible);
		}
	},

	_initPointSeries (root, chart) {
		const cfg = this._getEffectiveConfig();
		// Airport Series
		const airportSeries = chart.series.push(am5map.MapPointSeries.new(root, {}));
		this._airportSeries = airportSeries;

		airportSeries.bullets.push((root, series, dataItem) => {
			const d = dataItem.dataContext;
			const showAtts = cfg.showAttractionsDetails || cfg.showCityInfo;
			
			const getTooltipText = (data) => {
				if (cfg.scenario === 6 && data.legs && data.legs.length > 0) {
					let tip = `[b]${data.name}[/b]`;
					data.legs.forEach(l => {
						const dParts = (l.departureDate || "").split("-");
						const dateStr = dParts.length === 3 ? `${dParts[2]}/${dParts[1]}/${dParts[0]}` : l.departureDate;
						tip += `\n${dateStr} - ${l.opponent || ""} (${l.competition || ""})\nScore: ${l.score || ""} (${l.result || ""})`;
					});
					return tip;
				}
				return data.name ? (showAtts ? `${data.name} — click for attractions` : data.name) : "";
			};

			const _makeTip = () => {
				const _tip = am5.Tooltip.new(root, { pointerOrientation: "vertical", getFillFromSprite: false, autoTextColor: false });
				_tip.get("background").setAll({ fill: am5.color(0x0d1117), fillOpacity: 0.96, stroke: am5.color(0x4499FF), strokeWidth: 1, strokeOpacity: 0.9, cornerRadiusTL: 4, cornerRadiusTR: 4, cornerRadiusBL: 4, cornerRadiusBR: 4 });
				_tip.label.setAll({ fill: am5.color(0xffffff), fontSize: 12 });
				return _tip;
			};

			let sprite;
			if (d.crest) {
				const borderColor = d.customColor || "#4499FF";
				const container = am5.Container.new(root, {
					width: 17,
					height: 17,
					centerX: am5.p50,
					centerY: am5.p50,
					cursorOverStyle: showAtts ? "pointer" : "default",
					tooltipText: getTooltipText(d),
					tooltip: _makeTip(),
					ariaLabel: d.name || "Football Team"
				});
				container.children.push(am5.Circle.new(root, {
					radius: 8,
					fill: am5.color(0x1a1a2e),
					stroke: am5.color(borderColor),
					strokeWidth: 1.5
				}));
				container.children.push(am5.Picture.new(root, {
					src: d.crest,
					width: 14,
					height: 14,
					centerX: am5.p50,
					centerY: am5.p50
				}));
				sprite = container;
			} else {
				sprite = am5.Graphics.new(root, {
					svgPath: this.TARGET_SVG,
					fill: am5.color(d.customColor || cfg.colorAirportOther),
					scale: 0.5,
					cursorOverStyle: showAtts ? "pointer" : "default",
					tooltipText: getTooltipText(d),
					tooltip: _makeTip(),
					ariaLabel: d.name || "Airport"
				});
			}

			if (showAtts) {
				sprite.events.on("click", () => {
					const cityName = d.name;
					if (cityName && this._state.cityInfo[cityName]) {
						this._state.lastShownCity = cityName;
						if (this._state.cityTimer) { clearInterval(this._state.cityTimer); this._state.cityTimer = null; }
						this._renderCityByName(cityName);
					}
				});
			}
			return am5.Bullet.new(root, { sprite });
		});

		// Plane Series
		const planeSeries = chart.series.push(am5map.MapPointSeries.new(root, {}));
		this._planeSeries = planeSeries;

		planeSeries.bullets.push((root, series, dataItem) => {
			const d = dataItem.dataContext;
			const sprite = am5.Graphics.new(root, {
				svgPath: this.PLANE_SVG,
				fill: am5.color(this._safeColor(d.customColor || cfg.colorPlane)),
				fillOpacity: (d.alpha != null) ? d.alpha : 1.0,
				stroke: am5.color(0x000000),
				strokeWidth: 0.5,
				strokeOpacity: 0.3,
				scale: (d.scale != null) ? d.scale : 0.084,
				rotation: (d.rotation != null) ? d.rotation : 0,
				centerX: am5.p50,
				centerY: am5.p50,
				tooltipText: "{tooltipContent}",
				ariaLabel: d.flightNumber ? `Flight ${d.flightNumber}` : "Active Flight",
				tooltip: (() => {
					const _tip = am5.Tooltip.new(root, { pointerOrientation: "vertical", getFillFromSprite: false, autoTextColor: false });
					_tip.get("background").setAll({ fill: am5.color(0x0d1117), fillOpacity: 0.96, stroke: am5.color(0x4499FF), strokeWidth: 1, strokeOpacity: 0.9, cornerRadiusTL: 4, cornerRadiusTR: 4, cornerRadiusBL: 4, cornerRadiusBR: 4 });
					_tip.label.setAll({ fill: am5.color(0xffffff), fontSize: 12 });
					return _tip;
				})()
			});

			// Simple property binding via adapters
			sprite.adapters.add("rotation", (rotation, target) => {
				return target.dataItem.get("rotation") ?? rotation;
			});

			sprite.adapters.add("fillOpacity", (opacity, target) => {
				return target.dataItem.get("opacity") ?? opacity;
			});

			sprite.adapters.add("scale", (scale, target) => {
				return target.dataItem.get("scale") ?? scale;
			});

			sprite.adapters.add("fill", (fill, target) => {
				const customColor = target.dataItem.dataContext?.customColor;
				return customColor ? am5.color(this._safeColor(customColor)) : fill;
			});

			return am5.Bullet.new(root, { sprite });
		});
	},

	updateMapLines (legs) {
		if (!this._state.mapChart || !this._state.mapReady) return;

		this._pendingMapLinesLegs = legs;
		if (this._state.validateTimer) clearTimeout(this._state.validateTimer);
		this._state.validateTimer = setTimeout(() => {
			this._state.validateTimer = null;
			this._flushMapLines(this._pendingMapLinesLegs);
		}, 250);
	},

	_showVisitedPopup (iso, countryName, isVisited) {
		const wrapperId = `iAGT-wrapper-${this.identifier}`;
		const wrapper = document.getElementById(wrapperId);
		if (!wrapper) return;

		const existing = wrapper.querySelector(".iAGT-visited-popup");
		if (existing) existing.remove();
		if (this._state.visitedPopupTimer) { clearTimeout(this._state.visitedPopupTimer); this._state.visitedPopupTimer = null; }

		const statusText = isVisited ? this.translate("VISITED_IS_VISITED") : this.translate("VISITED_NOT_VISITED");
		const confirmLabel = isVisited ? this.translate("VISITED_BTN_UNMARK") : this.translate("VISITED_BTN_MARK");

		const popup = document.createElement("div");
		popup.className = "iAGT-visited-popup";
		popup.innerHTML = `
			<div class="iAGT-visited-popup-title">${this.translate("VISITED_POPUP_TITLE")}</div>
			<div class="iAGT-visited-popup-country">${this._esc(countryName)}</div>
			<div class="iAGT-visited-popup-status ${isVisited ? "is-visited" : "not-visited"}">${statusText}</div>
			<div class="iAGT-visited-popup-btns">
				<button class="iAGT-popup-confirm">${this._esc(confirmLabel)}</button>
				<button class="iAGT-popup-cancel">${this.translate("VISITED_BTN_CANCEL")}</button>
			</div>
			<div class="iAGT-visited-popup-progress"><div class="iAGT-visited-popup-progress-bar"></div></div>
		`;

		popup.querySelector(".iAGT-popup-confirm").addEventListener("click", () => {
			popup.remove();
			if (this._state.visitedPopupTimer) { clearTimeout(this._state.visitedPopupTimer); this._state.visitedPopupTimer = null; }
			this.sendSocketNotification("iAGT_TOGGLE_VISITED_COUNTRY", { iso });
		});
		popup.querySelector(".iAGT-popup-cancel").addEventListener("click", () => {
			popup.remove();
			if (this._state.visitedPopupTimer) { clearTimeout(this._state.visitedPopupTimer); this._state.visitedPopupTimer = null; }
		});

		wrapper.appendChild(popup);
		this._state.visitedPopupTimer = setTimeout(() => {
			popup.remove();
			this._state.visitedPopupTimer = null;
		}, 5000);
	},

	_applyVisitedCountriesColors () {
		if (!this._state.polygonSeries) return;
		const cfg = this._getEffectiveConfig();
		const visitedSet = this._state.visitedHighlightEnabled ? new Set(this._state.visitedCountryIsos || []) : new Set();
		const defaultFill = am5.color(this._safeColor(cfg.colorCountries));
		const defaultOpacity = 0.6;
		const defaultStroke = am5.color(this._safeColor(cfg.colorCountryBorders));
		const visitedFill = am5.color(this._safeColor(cfg.colorVisitedCountry || "#00AA44"));
		const visitedOpacity = cfg.colorVisitedCountryOpacity != null ? Number(cfg.colorVisitedCountryOpacity) : 0.75;
		const visitedStroke = am5.color(this._safeColor(cfg.colorVisitedCountryBorder || "#008833"));
		this._state.polygonSeries.mapPolygons.each((polygon) => {
			const id = polygon.dataItem?.dataContext?.id;
			if (id && visitedSet.has(id)) {
				polygon.setAll({ fill: visitedFill, fillOpacity: visitedOpacity, stroke: visitedStroke });
			} else {
				polygon.setAll({ fill: defaultFill, fillOpacity: defaultOpacity, stroke: defaultStroke });
			}
		});
	},

	_flushMapLines (legs) {
		if (!legs) legs = this._state.flightLegs;
		if (!this._state.mapChart || !this._state.mapReady) return;

		const lineData = this.buildMapLines(legs);
		const markerData = this.buildAirportMarkers(legs);

		// 1. Update line series
		for (const [key, features] of Object.entries(lineData)) {
			if (this._ls[key]) {
				this._ls[key].data.setAll(features);
			}
		}

		// 2. Update airport markers only when the data actually changes.
		//    Calling setAll() on every animation tick destroys and recreates
		//    am5.Picture bullet sprites, forcing image re-fetches that cause flicker.
		const airportFingerprint = markerData.airports
			.map(a => `${a.latitude},${a.longitude},${a.crest || ""},${a.customColor}`)
			.join("|");
		if (this._airportSeries && airportFingerprint !== this._state.lastAirportFingerprint) {
			this._state.lastAirportFingerprint = airportFingerprint;
			this._airportSeries.data.setAll(markerData.airports);
		}

		// 3. Update plane series — tween positions when the same set of planes is showing
		if (this._planeSeries) {
			const planes = markerData.planes;
			const series = this._planeSeries;
			const cfg = this._getEffectiveConfig();
			const isTest = String(cfg.showFlightTracks) === "test";
			const currKeys = planes.map(p => `${p.flightNumber || ""}|${p.shadowOnly || false}`).join(",");
			
			if (this._state.planeKeys === currKeys && series.dataItems.length === planes.length) {
				planes.forEach((p, i) => {
					const dataItem = series.dataItems[i];
					if (dataItem) {
						// Update dataContext for tooltips etc.
						dataItem.set("dataContext", p);
						
						if (isTest) {
							series.data.setIndex(i, p);
							dataItem.set("latitude",  p.latitude);
							dataItem.set("longitude", p.longitude);
							dataItem.set("rotation",  p.rotation);
							dataItem.set("opacity",   p.alpha);
							dataItem.set("scale",     p.scale);
						} else {
							dataItem.animate({ key: "latitude",  to: p.latitude,  duration: 1000, easing: am5.ease.linear });
							dataItem.animate({ key: "longitude", to: p.longitude, duration: 1000, easing: am5.ease.linear });
							dataItem.animate({ key: "rotation",  to: p.rotation,  duration: 1000, easing: am5.ease.linear });
							dataItem.animate({ key: "opacity",   to: p.alpha,     duration: 1000, easing: am5.ease.linear });
							dataItem.animate({ key: "scale",     to: p.scale,     duration: 1000, easing: am5.ease.linear });
						}
					}
				});
			} else {
				series.data.setAll(planes);
				this._state.planeKeys = currKeys;
			}

			// 4. Auto-rotate globe to plane(s) — Orthographic only
			if (cfg.autoRotateGlobeToPlane && cfg.mapProjection === "orthographic" && planes.length > 0) {
				const activePlanes = planes.filter(p => !p.shadowOnly);
				if (activePlanes.length > 0) {
					const avgLat = activePlanes.reduce((sum, p) => sum + p.latitude, 0) / activePlanes.length;
					const avgLon = activePlanes.reduce((sum, p) => sum + p.longitude, 0) / activePlanes.length;
					
					// Smoothly rotate the globe to center on the active plane(s)
					this._state.mapChart.animate({ key: "rotationX", to: -avgLon, duration: 1000, easing: am5.ease.out(am5.ease.cubic) });
					this._state.mapChart.animate({ key: "rotationY", to: -avgLat, duration: 1000, easing: am5.ease.out(am5.ease.cubic) });
				}
			}
		}
	},

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ TEST MODE ANIMATION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */

	/*
   * Build the ordered sequence of legs for the test animation.
   *
   * flightDisplayMode:
   *   "auto"     â†’ all outbound legs (date-sorted) then all return legs (date-sorted)
   *   "outbound" â†’ outbound legs only, date-sorted
   *   "return"   â†’ return legs only, date-sorted
   *   "all"      â†’ every leg, date-sorted
   */
	_buildTestSequence () {

		/*
     * Sort key priority (highest to lowest):
     *  1. actualDeparture  â€” ISO timestamp from AeroAPI (live mode)
     *  2. departureDate + departureTime â€” user-supplied "YYYY-MM-DD" + "HH:MM"
     *  3. departureDate alone (date-only, treated as 00:00)
     *  4. flightNumber â€” alphabetical tiebreak
     */
		const getSortKey = (leg) => this._legDepartureUtcMs(leg);
		const sortByDateTime = (arr) => [...arr].sort((a, b) => {
			const da = getSortKey(a);
			const db = getSortKey(b);
			return da !== db ? da - db : (a.flightNumber || "").localeCompare(b.flightNumber || "");
		});
		const cfg = this._getEffectiveConfig();
		const mode = cfg.flightDisplayMode || "all";
		if (mode === "auto") {
			return [
				...sortByDateTime(this._state.flightLegs.filter((l) => l.type === "outbound")),
				...sortByDateTime(this._state.flightLegs.filter((l) => l.type === "return"))
			];
		}
		if (mode === "outbound") return sortByDateTime(this._state.flightLegs.filter((l) => l.type === "outbound"));
		if (mode === "return") return sortByDateTime(this._state.flightLegs.filter((l) => l.type === "return"));
		return sortByDateTime(this._state.flightLegs);
	},

	_getTestDepartureMin (leg) {
		const map = this._state._testConfigTimeMap || {};
		const t = leg.departureTime || map[`${leg.travelerName}|${(leg.flightNumber || "").trim()}`] || "";
		if (!t || typeof t !== "string") return null;
		const parts = t.split(":");
		const h = parseInt(parts[0], 10);
		const m = parseInt(parts[1], 10);
		if (isNaN(h) || isNaN(m)) return null;

		let min = h * 60 + m;

		// Convert local time to UTC-ish minutes using longitude to avoid overlapping legs in test mode.
		// offset = round(lon / 15) hours. Subtract offset to get UTC.
		if (leg.from && leg.from.lon != null) {
			const lon = parseFloat(leg.from.lon);
			const offsetMin = Math.round(lon / 15) * 60;
			min -= offsetMin;
		}

		return min;
	},

	_estimateFlightDurationMin (leg) {
		if (!leg.from || !leg.to) return 90;
		const R = 6371;
		const toRad = d => d * Math.PI / 180;
		const lat1 = toRad(+leg.from.lat);  const lon1 = toRad(+leg.from.lon);
		const lat2 = toRad(+leg.to.lat);    const lon2 = toRad(+leg.to.lon);
		const dlat = lat2 - lat1;           const dlon = lon2 - lon1;
		const a = Math.sin(dlat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dlon / 2) ** 2;
		const dist = R * 2 * Math.asin(Math.sqrt(Math.min(1, Math.max(0, a))));
		return Math.max(20, (dist / 850) * 60);
	},

	_startParallelTestAnimation (legs) {
		const cfg         = this._getEffectiveConfig();
		const durationMs  = (cfg.testModeDuration || 30) * 1000;
		const delayMs     = (cfg.testModeDelay || 3) * 1000;
		const FPS         = 30;
		const stepMs      = 1000 / FPS;
		const flySteps    = Math.max(1, Math.round(durationMs / stepMs));
		const pauseSteps  = Math.max(1, Math.round(delayMs / stepMs));
		const n           = cfg.gcPoints || 60;

		const configTimeMap = {};
		if (cfg.travelers) {
			cfg.travelers.forEach(tv => {
				[...(tv.flights || []), ...(tv.returnFlights || [])].forEach(f => {
					configTimeMap[`${tv.name}|${(f.flightNumber || "").trim()}`] = f.departuretime || f.departureTime || "";
				});
			});
		}
		this._state._testConfigTimeMap = configTimeMap;

		const dateGroups = {};
		legs.forEach(leg => {
			const d = leg.departureDate || "unknown";
			if (!dateGroups[d]) dateGroups[d] = [];
			dateGroups[d].push(leg);
		});
		const sortedDates = Object.keys(dateGroups).sort();

		const groups = sortedDates.map(date => {
			const groupLegs = dateGroups[date];
			const timeline = groupLegs.map(leg => {
				const depMin  = this._getTestDepartureMin(leg);
				const startMin = depMin !== null ? depMin : 0;
				const durMin  = this._estimateFlightDurationMin(leg);
				return { leg, startMin, endMin: startMin + durMin };
			});
			const globalMin = Math.min(...timeline.map(t => t.startMin));
			const globalMax = Math.max(...timeline.map(t => t.endMin));
			return { date, timeline, globalMin, globalMax, spanMin: Math.max(1, globalMax - globalMin) };
		});

		const maxSpanMin = Math.max(...groups.map(g => g.spanMin));
		groups.forEach(g => { g.scaledFlySteps = Math.max(1, Math.round(flySteps * (g.spanMin / maxSpanMin))); });

		this._state.testGroups     = groups;
		this._state.testGroupIndex = 0;
		this._state.testProgress   = 0;
		this._state.testPhase      = "flying";
		this._state.testPauseCount = 0;
		this._state.tripReset      = false;
		this._testFrameCount       = 0;

		legs.forEach(l => { l.status = "scheduled"; l.progress = 0; l.currentLat = null; l.currentLon = null; });

		const advanceLeg = (leg, legProgress) => {
			const clamped = Math.max(0, Math.min(1, legProgress));
			if (legProgress < 0) {
				leg.status = "scheduled"; leg.progress = 0; leg.currentLat = null; leg.currentLon = null;
			} else if (legProgress <= 1) {
				leg.status   = "active";
				leg.progress = clamped;
				if (leg._gcPoints && leg._gcPoints.length) {
					const pts   = leg._gcPoints;
					const ptIdx = Math.min(n - 1, Math.floor(clamped * n));
					leg.currentLat    = pts[ptIdx].lat;
					leg.currentLon    = pts[ptIdx].lon;
					leg.groundspeed   = 450 + Math.floor(Math.random() * 50);
					const p1 = pts[ptIdx];
					const p2 = pts[Math.min(n - 1, ptIdx + 1)];
					if (p1 && p2 && ptIdx < n - 1) {
						leg.heading = this._calculateBearing(p1.lat, p1.lon, p2.lat, p2.lon);
					} else if (ptIdx > 0) {
						leg.heading = this._calculateBearing(pts[ptIdx - 1].lat, pts[ptIdx - 1].lon, p1.lat, p1.lon);
					}
					if      (clamped < 0.2) { leg.altitude = Math.floor(clamped * 5 * 38000);           leg.altitudeChange = "C"; }
					else if (clamped > 0.8) { leg.altitude = Math.floor((1 - clamped) * 5 * 38000);     leg.altitudeChange = "D"; }
					else                    { leg.altitude = 38000;                                       leg.altitudeChange = "L"; }
				}
			} else {
				leg.status = "landed"; leg.progress = 1;
				leg.currentLat = leg.to ? leg.to.lat : null;
				leg.currentLon = leg.to ? leg.to.lon : null;
			}
		};

		this._state.testTimer = setInterval(() => {
			const grps = this._state.testGroups;
			if (!grps || !grps.length) return;

			const grpIdx = this._state.testGroupIndex % grps.length;
			const group  = grps[grpIdx];

			if (this._state.testPhase === "flying") {
				this._testFrameCount++;
				this._state.testProgress = Math.min(1, this._state.testProgress + 1 / (group.scaledFlySteps || flySteps));
				const globalTimeMin = group.globalMin + this._state.testProgress * group.spanMin;

				let statusChanged = false;
				group.timeline.forEach(({ leg, startMin, endMin }) => {
					const oldStatus  = leg.status;
					const legProgress = (globalTimeMin - startMin) / Math.max(1, endMin - startMin);
					advanceLeg(leg, legProgress);
					if (leg.status !== oldStatus) statusChanged = true;
				});

				if (statusChanged || this._testFrameCount % 30 === 0) {
					this.updateTable();
					this._maybeAutoRotateAttractions(legs);
				}
				if (statusChanged) this.updateCountdown();

				if (this._state.testProgress >= 1) {
					group.timeline.forEach(({ leg }) => {
						if (leg.status !== "landed") {
							leg.status = "landed"; leg.progress = 1;
							leg.currentLat = leg.to ? leg.to.lat : null;
							leg.currentLon = leg.to ? leg.to.lon : null;
						}
					});
					this._state.testPhase      = "pausing";
					this._state.testPauseCount = 0;
					this.updateTable();
					this.updateCountdown();
					this._maybeAutoRotateAttractions(legs);
				}

			} else {
				this._state.testPauseCount++;
				if (this._state.testPauseCount >= pauseSteps) {
					this._state.testGroupIndex = (this._state.testGroupIndex + 1) % grps.length;
					this._state.testProgress   = 0;
					this._state.testPhase      = "flying";
					this._state.testPauseCount = 0;

					if (this._state.testGroupIndex === 0) {
						legs.forEach(l => { l.status = "scheduled"; l.progress = 0; l.currentLat = null; l.currentLon = null; });
						this._state.lastShownCity = null;
						this.updateTable();
						this.updateCountdown();
						const ciEl = document.getElementById(`iAGT-city-info-${this.identifier}`);
						if (ciEl) ciEl.innerHTML = "";
					} else {
						const nextGroup = grps[this._state.testGroupIndex];
						nextGroup.timeline.forEach(({ leg }) => {
							leg.status = "scheduled"; leg.progress = 0; leg.currentLat = null; leg.currentLon = null;
						});
						this.updateTable();
						this.updateCountdown();
					}
				}
			}

			this._flushMapLines(legs);
			this._maybeAutoRotateAttractions();
		}, stepMs);
	},

	startTestAnimation () {
		this.stopTestAnimation();
		this._state.testLegs = this._buildTestSequence();
		const legs = this._state.testLegs;
		if (!legs.length) return;

		const cfg = this._getEffectiveConfig();
		if (cfg.scenario === 3) {
			this._startParallelTestAnimation(legs);
			return;
		}

		const durationMs = (cfg.testModeDuration || 30) * 1000;
		const delayMs = (cfg.testModeDelay || 3) * 1000;
		const FPS = 30;
		const stepMs = 1000 / FPS;
		const flySteps = Math.max(1, Math.round(durationMs / stepMs));
		const pauseSteps = Math.max(1, Math.round(delayMs / stepMs));
		const n = cfg.gcPoints || 60;

		this._state.testLegIndex = 0;
		this._state.testProgress = 0;
		this._state.testPhase = "flying";
		this._state.testPauseCount = 0;
		this._testFrameCount = 0;
		this._state.tripReset = false;

		legs.forEach((l) => {
			l.status = "scheduled"; l.progress = 0; l.currentLat = null; l.currentLon = null;
		});

		this._state.testTimer = setInterval(() => {
			const activeLegs = this._state.testLegs;
			if (!activeLegs.length) return;

			const leg = activeLegs[this._state.testLegIndex % activeLegs.length];

			if (this._state.testPhase === "flying") {
				this._state.testProgress = Math.min(1, this._state.testProgress + 1 / flySteps);
				this._testFrameCount++;
				const oldStatus = leg.status;
				leg.status = "active";
				leg.progress = this._state.testProgress;

				if (leg.from && leg.to && leg._gcPoints) {
					const pts = leg._gcPoints;
					const ptIdx = Math.min(n - 1, Math.floor(this._state.testProgress * n));
					leg.currentLat = pts[ptIdx].lat;
					leg.currentLon = pts[ptIdx].lon;

					// Mock data for tooltips in test mode
					leg.groundspeed = 450 + Math.floor(Math.random() * 50); // 450-500 kts
					
					// Re-calculate bearing for tooltip
					const p1 = pts[ptIdx];
					const p2 = pts[Math.min(n - 1, ptIdx + 1)];
					if (p1 && p2 && ptIdx < n - 1) {
						leg.heading = this._calculateBearing(p1.lat, p1.lon, p2.lat, p2.lon);
					} else if (ptIdx > 0) {
						// End of leg bearing
						const pPrev = pts[ptIdx - 1];
						leg.heading = this._calculateBearing(pPrev.lat, pPrev.lon, p1.lat, p1.lon);
					}

					// Profile: Climb to 38,000, cruise, descend
					if (this._state.testProgress < 0.2) {
						leg.altitude = Math.floor(this._state.testProgress * 5 * 38000);
						leg.altitudeChange = "C";
					} else if (this._state.testProgress > 0.8) {
						leg.altitude = Math.floor((1 - this._state.testProgress) * 5 * 38000);
						leg.altitudeChange = "D";
					} else {
						leg.altitude = 38000;
						leg.altitudeChange = "L";
					}
				}

				if (this._state.testProgress >= 1) {
					leg.status = "landed";
					leg.progress = 1;
					leg.currentLat = leg.to ? leg.to.lat : null;
					leg.currentLon = leg.to ? leg.to.lon : null;
					this._state.testPhase = "pausing";
					this._state.testPauseCount = 0;
					this._maybeAutoRotateAttractions(activeLegs);
				}

				if (oldStatus !== leg.status || this._testFrameCount % 30 === 0) {
					this.updateTable();
					this._maybeAutoRotateAttractions(activeLegs);
				}
				if (oldStatus !== leg.status) {
					this.updateCountdown();
				}

			} else {
				this._state.testPauseCount++;
				if (this._state.testPauseCount >= pauseSteps) {
					this._state.testLegIndex = (this._state.testLegIndex + 1) % activeLegs.length;
					this._state.testProgress = 0;
					this._state.testPhase = "flying";
					this._state.testPauseCount = 0;
					if (this._state.testLegIndex === 0) {
						activeLegs.forEach((l) => { l.status = "scheduled"; l.progress = 0; l.currentLat = null; l.currentLon = null; });
						this._state.lastShownCity = null;
						this.updateTable();
						this.updateCountdown();
						const ciEl = document.getElementById(`iAGT-city-info-${this.identifier}`);
						if (ciEl) ciEl.innerHTML = "";
					}
				}
			}

			this._flushMapLines(activeLegs);
			this._maybeAutoRotateAttractions();
		}, stepMs);
	},

	stopTestAnimation () {
		if (this._state.testTimer) { clearInterval(this._state.testTimer); this._state.testTimer = null; }
	},

	_startGlobeAutoRotation () {
		this._stopGlobeAutoRotation();
		const cfg = this._getEffectiveConfig();
		if (cfg.mapProjection !== "orthographic" || cfg.autoRotateGlobeToPlane !== false) return;
		if (!this._state.mapChart) return;
		const degreesPerTick = 360 / 86400;
		this._state.globeRotTimer = setInterval(() => {
			const cfg2 = this._getEffectiveConfig();
			if (!this._state.mapChart || cfg2.mapProjection !== "orthographic" || cfg2.autoRotateGlobeToPlane !== false) {
				this._stopGlobeAutoRotation();
				return;
			}
			const cur = this._state.mapChart.get("rotationX") || 0;
			this._state.mapChart.set("rotationX", cur - degreesPerTick);
		}, 1000);
	},

	_stopGlobeAutoRotation () {
		if (this._state.globeRotTimer) {
			clearInterval(this._state.globeRotTimer);
			this._state.globeRotTimer = null;
		}
	},

	updateTitle () {
		const el = document.getElementById(`iAGT-title-${this.identifier}`);
		if (!el) return;
		const cfg = this._getEffectiveConfig();
		el.innerHTML = `${this.translate("TITLE_PREFIX")} &ndash; <span class="iAGT-dest">${this._esc(cfg.tripTitle)}</span>`;
	},

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ COUNTDOWN BOX â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	updateCountdown (legs) {
		const cfg = this._getEffectiveConfig();
		const el = document.getElementById(`iAGT-countdown-${this.identifier}`);
		if (!el) return;
		const icon = el.querySelector(".iAGT-cd-icon");
		const text = el.querySelector(".iAGT-cd-text");
		const subtitle = document.getElementById(`iAGT-cd-subtitle-${this.identifier}`);
		if (!text) return;

		if (subtitle) {
			if (this._state.noApiKey) {
				subtitle.textContent = "\u26A0 Live tracking disabled \u2014 no API key";
				subtitle.style.display = "block";
			} else {
				subtitle.textContent = "";
				subtitle.style.display = "none";
			}
		}

		const set = (ic, msg, cls) => {
			if (icon) icon.textContent = ic;
			text.textContent = msg;
			el.className = `iAGT-countdown${cls ? ` ${cls}` : ""}`;
			
			// ACC-002: Announce major status changes
			if (this._lastAnnouncedMsg !== msg) {
				this._announce(msg);
				this._lastAnnouncedMsg = msg;
			}
		};

		if (!legs) legs = this._getFilteredLegs();
		if (!legs.length) return set("\u23F3", this.translate("NO_FLIGHTS"), "");

		if (this._state.tripReset) return set("\u2705", this.translate("COUNTDOWN_COMPLETE"), "iAGT-complete");

		const allDone = legs.every((l) => l.status === "landed" || l.status === "cancelled");
		if (allDone) return set("\u2705", this.translate("COUNTDOWN_COMPLETE"), "iAGT-complete");

		const active = legs.filter((l) => l.status === "active");
		if (active.length) {
			if (active.length > 1 && cfg.scenario === 3) {
				el.className = "iAGT-countdown iAGT-inflight";
				if (icon) icon.textContent = "";
				text.innerHTML = active.map((l) => {
					const pct = Math.round((l.progress || 0) * 100);
					const color = this._safeColor(this._state.travelerColors[l.travelerName] || cfg.colorPlane);
					const sym = this._state.travelerSymbols[l.travelerName] || "\u2708";
					return `<span style="color:${color}">${sym}&thinsp;${this._esc(l.flightNumber || "")} \u2014 ${pct}%</span>`;
				}).join("&ensp;|&ensp;");
				
				// ACC-002: Announce multiple active flights
				const msg = active.map(l => `${l.flightNumber || "Flight"} at ${Math.round((l.progress || 0) * 100)}%`).join(", ");
				if (this._lastAnnouncedMsg !== msg) {
					this._announce(msg);
					this._lastAnnouncedMsg = msg;
				}
				return;
			}
			const pct = Math.round((active[0].progress || 0) * 100);
			return set("\u2708", `${this.translate("COUNTDOWN_INFLIGHT")} ${active[0].flightNumber || ""} \u2014 ${pct}%`, "iAGT-inflight");
		}

		const future = legs.filter((l) => l.status === "scheduled" && l.departureDate);
		if (future.length) {
			const first = future.reduce((a, b) =>
				this._legDepartureUtcMs(a) <= this._legDepartureUtcMs(b) ? a : b
			);

			const depMs         = this._legDepartureUtcMs(first);
			const hoursUntilDep = (depMs - Date.now()) / 3600000;

			if (hoursUntilDep > 0 && hoursUntilDep < 24) {
				el.className = "iAGT-countdown iAGT-boarding";
				if (icon) icon.textContent = "\u2708";
				const etd = new Date(depMs).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
				let chips = `<span class="iAGT-board-flight">${this._esc(first.flightNumber || "")}</span>`;
				if (first.departureTerminal) chips += `<span class="iAGT-board-chip">T&thinsp;${this._esc(first.departureTerminal)}</span>`;
				if (first.departureGate)     chips += `<span class="iAGT-board-chip">G&thinsp;${this._esc(first.departureGate)}</span>`;
				chips += `<span class="iAGT-board-etd">ETD&thinsp;${etd}</span>`;
				text.innerHTML = chips;

				// ACC-002: Announce boarding/upcoming flight
				const msg = `${first.flightNumber || "Flight"} departing at ${etd}`;
				if (this._lastAnnouncedMsg !== msg) {
					this._announce(msg);
					this._lastAnnouncedMsg = msg;
				}
				return;
			}

			/* Departure time is known (via API or config) and has already passed in UTC
			   — flight has likely departed even if FlightAware hasn't updated yet.
			   When only a date is known, use the airport-longitude estimate: if the
			   entire local day at the departure airport has passed (estimate < -12 h),
			   treat the flight as departed rather than showing "Today".               */
			const hasKnownDepTime = !!(first.estimatedDeparture || first.scheduledDeparture || first.departureTime);
			const wholeLocalDayPassed = !hasKnownDepTime && (first.from && first.from.lon != null) && hoursUntilDep < -12;
			if (hoursUntilDep < 0 && (hasKnownDepTime || wholeLocalDayPassed)) {
				return set("\u2708", this.translate("COUNTDOWN_DEPARTED"), "iAGT-departed");
			}

			/* Fall back to day-based countdown: compare departure date (UTC midnight)
			   against today's UTC date so the result is timezone-neutral.             */
			const depDateUtcMs = Date.parse(first.departureDate + "T00:00:00Z");
			const nowUtcMidnightMs = Date.UTC(
				new Date().getUTCFullYear(), new Date().getUTCMonth(), new Date().getUTCDate()
			);
			const days = Math.round((depDateUtcMs - nowUtcMidnightMs) / 86400000);

			if (days <= 0) return set("\uD83D\uDEEB", this.translate("COUNTDOWN_TODAY"), "iAGT-today");
			if (days === 1) return set("\u23F3", `1 ${this.translate("COUNTDOWN_DAY")}`, "iAGT-soon");
			return set("\u23F3", `${days} ${this.translate("COUNTDOWN_DAYS")}`, "");
		}
	},

	/* â”€â”€â”€â”€â”€â”€â”€ OVERLAY TABLE  (Name | Flight No | Date | Dep | Arr | Status) â”€â”€ */
	buildTableHTML (legs) {
		const LABEL = {
			scheduled: "Scheduled",
			active: "In Flight \u2708",
			landed: "Landed \u2713",
			cancelled: "Cancelled \u2717"
		};
		const CLS = { scheduled: "st-sched", active: "st-active", landed: "st-landed", cancelled: "st-cancel" };

		/* UX-005: Format date locale-friendly */
		const fmtDate = (d) => {
			if (!d) return "\u2014";
			const dt = new Date(`${d}T00:00:00`);
			return isNaN(dt.getTime()) ? d : dt.toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" });
		};

		const fmtDateTime = (iso) => {
			if (!iso) return null;
			try {
				const dt = new Date(iso);
				return isNaN(dt.getTime()) ? null : dt.toLocaleString(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
			} catch (_e) { return null; }
		};

		const utcSortKey = (l) => this._legDepartureUtcMs(l);

		/* â”€â”€ Table title â”€â”€ */
		const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
		const title = `<div class="iAGT-tbl-title"><span class="iAGT-dest-clock" id="iAGT-dest-clock-${this.identifier}"></span><span class="iAGT-tbl-title-text">${this.translate("TABLE_TITLE")}</span><button class="iAGT-save-btn iAGT-save-flights-btn" title="Click to print to documents/MySavedFlights">\uD83D\uDDA8</button><span class="iAGT-save-sep">|</span><button class="iAGT-save-btn iAGT-save-terminal-btn" title="Click to save terminal maps to documents/MySavedTerminalMaps">\uD83D\uDDFA</button></div>`;

		let h = `${title}<div class="iAGT-scroll-wrap"><div class="iAGT-tbl-scroll"><table class="iAGT-tbl">
<thead><tr>
  <th class="col-name">${this.translate("TBL_NAME")}</th>
  <th class="col-fn">${this.translate("TBL_FLIGHT")}</th>
  <th class="col-date">${this.translate("TBL_DATE")} <small>(${tz})</small></th>
  <th class="col-dep">${this.translate("TBL_DEP")}</th>
  <th class="col-arr">${this.translate("TBL_ARR")}</th>
  <th class="col-st">${this.translate("TBL_STATUS")}</th>
</tr></thead><tbody>`;

		if (!legs || !legs.length) {
			h += `<tr><td colspan="6" class="iAGT-empty">${this.translate("LOADING")}</td></tr>`;
		} else {

			/*
       * Sort priority:  0=active (in-flight)  1=scheduled/cancelled  2=landed
       * Within each group, ascending by departure time then flight number.
       * Landed legs are hidden once their next leg (same traveler for Scenario 3)
       * has departed (status active or landed).
       */
			const STATUS_RANK = { active: 0, scheduled: 1, cancelled: 1, landed: 2 };

			// PERF-004: Pre-compute UTC timestamps for sort (date+time â†’ next-departure ordering)
			const legsWithTime = legs.map((l) => ({
				leg: l,
				t: utcSortKey(l)
			}));

			/* Pre-sort all legs by departure time to establish trip sequence */
			const byTime = [...legsWithTime]
				.sort((a, b) => (a.t !== b.t ? a.t - b.t : (a.leg.flightNumber || "").localeCompare(b.leg.flightNumber || "")))
				.map((x) => x.leg);

			/* For a given leg, return the next sequential leg in the same trip/traveler */
			const getNextLeg = (leg) => {
				const cfg = this._getEffectiveConfig();
				const idx = byTime.indexOf(leg);
				if (cfg.scenario === 3) {
					for (let i = idx + 1; i < byTime.length; i++) {
						if (byTime[i].travelerName === leg.travelerName) return byTime[i];
					}
					return null;
				}
				return idx < byTime.length - 1 ? byTime[idx + 1] : null;
			};

			const sorted = legsWithTime
				.filter((x) => {
					const leg = x.leg;
					if ((leg.status || "scheduled") !== "landed") return true;
					const next = getNextLeg(leg);
					if (!next) return true;
					const ns = next.status || "scheduled";
					return ns !== "active" && ns !== "landed";
				})
				.sort((a, b) => {
					const ra = STATUS_RANK[a.leg.status || "scheduled"] ?? 1;
					const rb = STATUS_RANK[b.leg.status || "scheduled"] ?? 1;
					if (ra !== rb) return ra - rb;
					return a.t !== b.t ? a.t - b.t : (a.leg.flightNumber || "").localeCompare(b.leg.flightNumber || "");
				})
				.map((x) => x.leg);

			sorted.forEach((leg) => {
				const st = leg.status || "scheduled";
				const cls = CLS[st] || "";
				let lbl = LABEL[st] || st;

				/* Override label for taxiing / diverted sub-states */
				if (leg.detailedStatus) {
					const ds = leg.detailedStatus.toLowerCase();
					if (ds.includes("taxiing"))       lbl = "Taxiing \u2708";
					else if (ds.includes("diverted")) lbl = "Diverted \u26A0";
				}

				let pct = st === "active" ? ` ${Math.round((leg.progress || 0) * 100)}%` : "";

				/* NEW-15: Delay badge */
				let delayBadge = "";
				if (leg.estimatedDeparture && leg.scheduledDeparture) {
					const diff = (new Date(leg.estimatedDeparture) - new Date(leg.scheduledDeparture)) / 60000;
					if (diff > 15) delayBadge = `<span class="iAGT-delay-badge">+${Math.round(diff)}m</span>`;
				}

				/* NEW-14: Connection risk indicator */
				let riskIcon = "";
				const prev = byTime.filter(l => l.travelerName === leg.travelerName && byTime.indexOf(l) < byTime.indexOf(leg)).pop();
				if (prev && prev.estimatedArrival && leg.estimatedDeparture) {
					const layover = (new Date(leg.estimatedDeparture) - new Date(prev.estimatedArrival)) / 60000;
					const prevDelayed = prev.estimatedDeparture && prev.scheduledDeparture && (new Date(prev.estimatedDeparture) - new Date(prev.scheduledDeparture)) > 0;
					if (layover > 0 && layover < 90 && prevDelayed) {
						riskIcon = ` <span class="iAGT-delay-badge" title="Tight connection risk (\u2264 90m layover with inbound delay)">\u26A0</span>`;
					}
				}

				const frm = leg.from ? `${this._esc(leg.from.name)} (${this._esc(leg.from.iata)})` : "\u2014";
				const too = leg.to ? `${this._esc(leg.to.name)} (${this._esc(leg.to.iata)})` : "\u2014";

				const cfg = this._getEffectiveConfig();
				/* Colour aircraft symbol and progress text for Scenario 3 active flights */
				if (st === "active" && cfg.scenario === 3 && this._state.travelerColors[leg.travelerName]) {
					const color = this._safeColor(this._state.travelerColors[leg.travelerName]);
					lbl = lbl.replace("\u2708", `<span style="color:${color}">\u2708</span>`);
					pct = `<span style="color:${color}">${pct}</span>`;
				}

				/* Colour name cell background for Scenario 3 traveler identification */
				let nameCellStyle = "";
				if (cfg.scenario === 3 && this._state.travelerColors[leg.travelerName]) {
					const color = this._safeColor(this._state.travelerColors[leg.travelerName]);
					nameCellStyle = ` style="background-color:${color};color:rgba(0,0,0,0.85);font-weight:600;"`;
				}

				const localTime = leg.departureTime ? `<span class="col-time">${this._esc(leg.departureTime)}\u202FLCL</span>` : "";
			const hasCoords = leg.from && leg.to && leg.from.lat != null && leg.to.lat != null;
			const flyAttr = hasCoords
				? ` data-fly-lat1="${leg.from.lat}" data-fly-lon1="${leg.from.lon}" data-fly-lat2="${leg.to.lat}" data-fly-lon2="${leg.to.lon}" class="${cls} iAGT-fly-row"`
				: ` class="${cls}"`;
			h += `<tr${flyAttr}>
  <td class="col-name"${nameCellStyle}>${this._esc(leg.travelerName) || "\u2014"}</td>
  <td class="col-fn">${this._esc(leg.flightNumber) || "\u2014"}</td>
  <td class="col-date">${fmtDate(leg.departureDate)}${localTime}</td>
  <td class="col-dep">${frm}</td>
  <td class="col-arr">${too}</td>
  <td class="col-st ${cls}">${lbl}${pct}${delayBadge}${riskIcon}</td>
</tr>`;

				/* â”€â”€ Details sub-row: terminal/gate, aircraft, times â”€â”€ */
				const _chips = [];
				if (leg.aircraftType || leg.tailNumber) {
					_chips.push(`\u2708 ${[this._esc(leg.aircraftType), leg.tailNumber ? `(${this._esc(leg.tailNumber)})` : null].filter(Boolean).join(" ")}`);
				}
				const _depTG = [leg.departureTerminal ? `T:${this._esc(leg.departureTerminal)}` : null, leg.departureGate ? `G:${this._esc(leg.departureGate)}` : null].filter(Boolean).join(" ");
				const _arrTG = [leg.arrivalTerminal   ? `T:${this._esc(leg.arrivalTerminal)}`   : null, leg.arrivalGate   ? `G:${this._esc(leg.arrivalGate)}`   : null].filter(Boolean).join(" ");
				if (_depTG || _arrTG) _chips.push(`${_depTG || "\u2014"} \u2192 ${_arrTG || "\u2014"}`);
				const _etd = fmtDateTime(leg.estimatedDeparture);
				const _eta = fmtDateTime(leg.foresightEta || leg.estimatedArrival);
				const _etaLabel = leg.foresightEta ? "ETA\u26A1" : "ETA";
				if (_etd || _eta) {
					_chips.push([_etd ? `ETD: ${_etd}` : null, _eta ? `${_etaLabel}: ${_eta}` : null].filter(Boolean).join("  "));
				}
				if (st === "active") {
					const _liveParts = [];
					if (leg.altitude    != null) _liveParts.push(`Alt: ${leg.altitude.toLocaleString()} ft`);
					if (leg.groundspeed != null) _liveParts.push(`${leg.groundspeed} kts`);
					if (leg.heading     != null) _liveParts.push(`Hdg: ${Math.round(leg.heading)}\u00B0`);
					if (leg.altitudeChange) {
						const _dir = leg.altitudeChange === "C" ? "\u25B2" : leg.altitudeChange === "D" ? "\u25BC" : "\u2192";
						_liveParts.push(`Rate: ${_dir}`);
					}
					if (leg.lastPositionUpdate) {
						try {
							const _upd = new Date(leg.lastPositionUpdate);
							if (!isNaN(_upd.getTime())) _liveParts.push(`Upd: ${_upd.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`);
						} catch (_e) { }
					}
					if (_liveParts.length) _chips.push(`\u{1F4E1} ${_liveParts.join("  ")}`);
				}
				if (_chips.length) {
					h += `<tr class="iAGT-details-row"><td colspan="6">${_chips.map(c => `<span class="iAGT-detail-chip">${c}</span>`).join("")}</td></tr>`;
				}
			});
		}
		return `${h}</tbody></table></div></div>`;
	},

	updateTable (legs) {
		const cfg = this._getEffectiveConfig();
		const el = document.getElementById(`iAGT-table-${this.identifier}`);
		if (!el) return;
		el.innerHTML = this.buildTableHTML(legs || this._getFilteredLegs());
		this._startDestClock(this._getCurrentDestLon());
		const wrap = el.querySelector(".iAGT-scroll-wrap");
		const scrollEl = el.querySelector(".iAGT-tbl-scroll");
		if (wrap && scrollEl) this._setupCustomScrollbar(scrollEl, wrap);
		const saveBtn = el.querySelector(".iAGT-save-flights-btn");
		const terminalBtn = el.querySelector(".iAGT-save-terminal-btn");
		if (saveBtn) saveBtn.addEventListener("click", () => this._saveFlights(el));
		if (terminalBtn) terminalBtn.addEventListener("click", () => this._saveTerminalMaps(el));

		/* ── UIX-003: Fly-to click handlers on flight rows ── */
		if (cfg.flyToOnRowClick !== false) {
			el.querySelectorAll("tr.iAGT-fly-row").forEach((row) => {
				row.addEventListener("click", () => {
					const lat1 = parseFloat(row.dataset.flyLat1);
					const lon1 = parseFloat(row.dataset.flyLon1);
					const lat2 = parseFloat(row.dataset.flyLat2);
					const lon2 = parseFloat(row.dataset.flyLon2);
					if (!isNaN(lat1) && !isNaN(lon1)) {
						this._flyToLeg(lat1, lon1, lat2, lon2);
						el.querySelectorAll("tr.iAGT-fly-row").forEach((r) => r.classList.remove("iAGT-fly-active"));
						row.classList.add("iAGT-fly-active");
						setTimeout(() => row.classList.remove("iAGT-fly-active"), 2000);
					}
				});
			});
		}
	},

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ CITY INFORMATION PANEL  (Top 10 things to do) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	getCityDisplayList () {
		if (this._state.cityDisplayListCache) return this._state.cityDisplayListCache;
		const cfg = this._getEffectiveConfig();
		const legs = this._getFilteredLegs();
		let result;
		if (cfg.cityInfoMode === "layovers") {
			const seen = new Set();
			const cities = [];
			legs.forEach((leg) => {
				if (leg.to && leg.to.name && !seen.has(leg.to.name)) {
					seen.add(leg.to.name);
					cities.push(leg.to.name);
				}
			});
			result = cities.filter((n) => this._state.cityInfo[n]);
		} else {
			let destName = null;
			if (cfg.destination && cfg.destination.name) {
				destName = cfg.destination.name;
			} else if (legs.length) {
				const last = legs[legs.length - 1];
				if (last.to) destName = last.to.name;
			}
			result = (destName && this._state.cityInfo[destName]) ? [destName] : [];
		}
		this._state.cityDisplayListCache = result;
		return result;
	},

	startCityInfoCycling () {
		if (this._state.cityTimer) { clearInterval(this._state.cityTimer); this._state.cityTimer = null; }
		const cfg = this._getEffectiveConfig();
		if (cfg.cityInfoMode !== "layovers") return;
		const cities = this.getCityDisplayList();
		if (cities.length <= 1) return;
		const ms = (cfg.cityInfoCycleInterval || 20) * 1000;
		this._state.cityTimer = setInterval(() => {
			this._state.cityIndex = (this._state.cityIndex + 1) % cities.length;
			this.updateCityInfo();
		}, ms);
	},

	updateCityInfo () {
		const el = document.getElementById(`iAGT-city-info-${this.identifier}`);
		if (!el) return;

		const cities = this.getCityDisplayList();
		if (!cities.length) { this._stopAttractionsAutoScroll(); el.innerHTML = ""; return; }

		const name = cities[this._state.cityIndex % cities.length];
		const info = this._state.cityInfo[name];
		if (!info) { this._stopAttractionsAutoScroll(); el.innerHTML = ""; return; }

		this._state.currentDisplayedCity = name;

		const cfg = this._getEffectiveConfig();
		const things = info.attractions && info.attractions.things ? info.attractions.things : [];
		const isMulti = cfg.cityInfoMode === "layovers" && cities.length > 1;
		const idxLabel = isMulti
			? `<span class="iAGT-ci-nav">${this._state.cityIndex % cities.length + 1}&thinsp;/&thinsp;${cities.length}</span>`
			: "";

		const maxAtt = cfg.maxAttractionsDisplay || 5;
		let weatherH = "";
		if (info.weather) {
			const w = info.weather;
			const wIcon = this._getWeatherIcon(w.weathercode);
			const updStr = info.weatherUpdatedAt
				? `<span class="iAGT-weather-updated">Updated\u202F${new Date(info.weatherUpdatedAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>`
				: "";
			weatherH = `<span class="iAGT-weather-pill">${wIcon} ${Math.round(w.temperature)}\u00B0C${updStr}</span>`;
		}
		let h = `<div class="iAGT-ci-hdr">
  <span class="iAGT-ci-clock" id="iAGT-ci-clock-${this.identifier}">${this._fmtLocalClock()}</span>
  <span class="ci-pin">&#128205;</span>
  Top ${maxAtt} ${this.translate("TOP_THINGS_TITLE")} <strong>${this._esc(name)}</strong>${weatherH}${idxLabel}
  <button class="iAGT-save-btn iAGT-save-atts-btn" title="Click to print to documents/MySavedCityAttractions">\uD83D\uDDA8</button>
</div>`;

		h += this._buildAttractionsHTML(things);

		if (isMulti) {
			h += "<div class=\"iAGT-ci-progress\">";
			cities.forEach((c, i) => {
				const active = i === this._state.cityIndex % cities.length;
				h += `<span class="iAGT-ci-dot${active ? " active" : ""}"></span>`;
			});
			h += "</div>";
		}

		const applyContent = () => {
			el.innerHTML = h;
			el.classList.remove("iAGT-ci-fading");
			const wrap = el.querySelector(".iAGT-scroll-wrap");
			const scrollEl = el.querySelector(".iAGT-atts-scroll");
			if (wrap && scrollEl) {
				this._setupCustomScrollbar(scrollEl, wrap);
			}
			this._attractionsThings = things;
			this._startAttractionsAutoScroll();
			this._startCiClock();
			const saveBtn = el.querySelector(".iAGT-save-atts-btn");
			if (saveBtn) saveBtn.addEventListener("click", () => this._saveAttractions(el));
		};

		if (el.innerHTML) {
			el.classList.add("iAGT-ci-fading");
			setTimeout(applyContent, 300);
		} else {
			applyContent();
		}
	},

	_refreshWeather () {
		const cities = Object.keys(this._state.cityInfo);
		if (!cities.length) return;
		cities.forEach(name => {
			this.sendSocketNotification("iAGT_REFRESH_WEATHER", { cityName: name });
		});
	},

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ AUTO-ROTATE ATTRACTIONS ON LANDING â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	_maybeAutoRotateAttractions (legs) {
		const showAtts = this.config.showAttractionsDetails || this.config.showCityInfo;
		if (!showAtts) return;
		if (!legs) legs = this._getFilteredLegs();
		if (!legs || !legs.length) return;

		// 1. If any flight is currently active, show its destination
		const activeLegs = legs.filter((l) => l.status === "active");
		if (activeLegs.length > 0) {
			const activeDestinations = [...new Set(activeLegs.map((l) => l.to ? l.to.name : null).filter(Boolean))];
			if (activeDestinations.length === 0) return;

			if (activeDestinations.length === 1) {
				const destName = activeDestinations[0];
				if (destName && this._state.lastShownCity !== destName && this._state.cityInfo[destName]) {
					this._state.lastShownCity = destName;
					if (this._state.cityTimer) { clearInterval(this._state.cityTimer); this._state.cityTimer = null; }
					this._renderCityByName(destName);
				}
				this._state.lastActiveDestFingerprint = null;
				return;
			}

			// Multiple active destinations and autoRotate is true -> Rotate through them
			const fingerPrint = activeDestinations.sort().join("|");
			if (this._state.lastActiveDestFingerprint === fingerPrint && this._state.cityTimer) {
				return; // Already rotating these exact destinations
			}

			this._state.lastActiveDestFingerprint = fingerPrint;
			if (this._state.cityTimer) { clearInterval(this._state.cityTimer); this._state.cityTimer = null; }

			let idx = activeDestinations.indexOf(this._state.lastShownCity);
			if (idx === -1) idx = 0;

			this._state.lastShownCity = activeDestinations[idx];
			this._renderCityByName(activeDestinations[idx]);

			this._state.cityTimer = setInterval(() => {
				idx = (idx + 1) % activeDestinations.length;
				const dest = activeDestinations[idx];
				this._state.lastShownCity = dest;
				this._renderCityByName(dest);
			}, (this.config.cityInfoCycleInterval || 20) * 1000);

			return;
		}

		// 2. Otherwise, show the traveller's current location (most recently landed destination)
		this._state.lastActiveDestFingerprint = null;

		const landedLegs = legs.filter((l) => l.status === "landed");
		if (!landedLegs.length) return;

		const lastLanded = landedLegs.reduce((best, l) =>
			this._legDepartureUtcMs(l) >= this._legDepartureUtcMs(best) ? l : best
		);
		if (!lastLanded.to) return;
		const destName = lastLanded.to.name;

		if (this._state.lastShownCity === destName) return;
		this._state.lastShownCity = destName;

		if (!this._state.cityInfo[destName]) return;

		if (this._state.cityTimer) { clearInterval(this._state.cityTimer); this._state.cityTimer = null; }
		this._renderCityByName(destName);
	},

	_renderCityByName (name) {
		const el = document.getElementById(`iAGT-city-info-${this.identifier}`);
		if (!el) return;
		const info = this._state.cityInfo[name];
		if (!info) { el.innerHTML = ""; return; }
		this._state.currentDisplayedCity = name;
		const things = info.attractions && info.attractions.things ? info.attractions.things : [];
		const maxAtt = this.config.maxAttractionsDisplay || 5;
		let weatherH = "";
		if (info.weather) {
			const w = info.weather;
			const wIcon = this._getWeatherIcon(w.weathercode);
			const updStr = info.weatherUpdatedAt
				? `<span class="iAGT-weather-updated">Updated\u202F${new Date(info.weatherUpdatedAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>`
				: "";
			weatherH = `<span class="iAGT-weather-pill">${wIcon} ${Math.round(w.temperature)}\u00B0C${updStr}</span>`;
		}

		let distH = "";
		if (info.attractions && (info.attractions.airportDistanceKm || info.attractions.airportPostcode)) {
			const d = info.attractions.airportDistanceKm;
			const p = info.attractions.airportPostcode;
			const dStr = d ? `${d}\u202Fkm` : "";
			const pStr = p ? ` (${p})` : "";
			distH = `<span class="iAGT-dist-pill" title="Distance from airport to city center">\u2708 ${dStr}${pStr}</span>`;
		}

		let h = `<div class="iAGT-ci-hdr"><span class="iAGT-ci-clock" id="iAGT-ci-clock-${this.identifier}">${this._fmtLocalClock()}</span><span class="ci-pin">&#128205;</span>Top ${maxAtt} ${this.translate("TOP_THINGS_TITLE")} <strong>${this._esc(name)}</strong>${weatherH}${distH}<button class="iAGT-save-btn iAGT-save-atts-btn" title="Click to print to documents/MySavedCityAttractions">\uD83D\uDDA8</button></div>`;
		h += this._buildAttractionsHTML(things);

		const applyContent = () => {
			el.innerHTML = h;
			el.classList.remove("iAGT-ci-fading");
			const wrap2 = el.querySelector(".iAGT-scroll-wrap");
			const scrollEl2 = el.querySelector(".iAGT-atts-scroll");
			if (wrap2 && scrollEl2) {
				this._setupCustomScrollbar(scrollEl2, wrap2);
			}
			this._attractionsThings = things;
			this._startAttractionsAutoScroll();
			this._startCiClock();
			const saveBtn = el.querySelector(".iAGT-save-atts-btn");
			if (saveBtn) saveBtn.addEventListener("click", () => this._saveAttractions(el));
			this._requestAndDisplayFunFact(name);
		};

		if (el.innerHTML) {
			el.classList.add("iAGT-ci-fading");
			setTimeout(applyContent, 300);
		} else {
			applyContent();
		}
	},

	_buildAttractionsHTML (things) {
		if (!things || !things.length) {
			return `<p class="iAGT-no-data">${this.translate("NO_ATTRACTIONS")}</p>`;
		}

		const maxAtt = this.config.maxAttractionsDisplay || 5;

		let h = "<div class=\"iAGT-scroll-wrap\"><div class=\"iAGT-atts-scroll\"><table class=\"iAGT-atts-tbl\"><thead><tr>"
		  + `<th>${this.translate("ATT_COL_NUM")}</th><th>${this.translate("ATT_COL_NAME")}</th><th>${this.translate("ATT_COL_DESC")}</th>`
		  + "</tr></thead><tbody>";

		things.slice(0, maxAtt).forEach((t, i) => {
			h += "<tr class=\"iAGT-att\">"
			  + `<td class="att-num">${i + 1}</td>`
			  + `<td class="att-name">${this._esc(t.name)}</td>`
			  + `<td class="att-desc">${this._esc(t.description || "")}</td>`
			  + "</tr>";
		});

		h += "</tbody></table></div></div>";
		return h;
	},

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ ATTRACTIONS AUTO-SCROLL â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	_stopAttractionsAutoScroll () {
		if (this._state.attractionsScrollTimer) {
			clearInterval(this._state.attractionsScrollTimer);
			this._state.attractionsScrollTimer = null;
		}
		this._attractionsPage = 0;
	},

	_startAttractionsAutoScroll () {
		this._stopAttractionsAutoScroll();
		if (!this.config.attractionsAutoScroll) return;

		const things = this._attractionsThings || [];
		const pageSize = this.config.maxAttractionsDisplay || 5;
		if (things.length <= pageSize) return;

		const panelId = `iAGT-city-info-${this.identifier}`;
		this._attractionsPage = 0;
		const intervalMs = Math.max(1000, (this.config.attractionsScrollInterval || 15) * 1000);

		this._state.attractionsScrollTimer = setInterval(() => {
			const p = document.getElementById(panelId);
			if (!p) return;
			const scrollEl = p.querySelector(".iAGT-atts-scroll");
			if (!scrollEl) return;
			const tbody = scrollEl.querySelector("tbody");
			if (!tbody) return;

			const totalPages = Math.ceil(things.length / pageSize);
			this._attractionsPage = (this._attractionsPage + 1) % totalPages;
			const start = this._attractionsPage * pageSize;
			const slice = things.slice(start, start + pageSize);

			let html = "";
			slice.forEach((t, i) => {
				html += "<tr class=\"iAGT-att\">"
				  + `<td class="att-num">${start + i + 1}</td>`
				  + `<td class="att-name">${this._esc(t.name)}</td>`
				  + `<td class="att-desc">${this._esc(t.description || "")}</td>`
				  + "</tr>";
			});
			tbody.innerHTML = html;
			scrollEl.scrollTop = 0;
		}, intervalMs);
	},

	/* ─────────────────── DESTINATION CITY LIVE CLOCK (flight panel) ───── */
	_getCurrentDestLon () {
		const legs = this._getFilteredLegs();
		const activeLegs = legs.filter(l => l.status === "active");
		if (activeLegs.length > 0) {
			const leg = activeLegs[0];
			return (leg.to && leg.to.lon != null) ? leg.to.lon : null;
		}
		const landedLegs = legs.filter(l => l.status === "landed");
		if (landedLegs.length > 0) {
			const lastLanded = landedLegs.reduce((best, l) =>
				this._legDepartureUtcMs(l) >= this._legDepartureUtcMs(best) ? l : best
			);
			return (lastLanded.to && lastLanded.to.lon != null) ? lastLanded.to.lon : null;
		}
		return null;
	},

	_startDestClock (lon) {
		if (this._state.destClockTimer) {
			clearInterval(this._state.destClockTimer);
			this._state.destClockTimer = null;
		}
		if (lon == null) return;
		const lonOffsetMin = Math.round(parseFloat(lon) / 15) * 60;
		const gmtHours = lonOffsetMin / 60;
		const gmtLabel = `GMT${gmtHours >= 0 ? "+" : ""}${gmtHours}`;
		const tick = () => {
			const el = document.getElementById(`iAGT-dest-clock-${this.identifier}`);
			if (!el) return;
			const localMs = Date.now() + lonOffsetMin * 60000;
			const d = new Date(localMs);
			const hh  = d.getUTCHours().toString().padStart(2, "0");
			const mm  = d.getUTCMinutes().toString().padStart(2, "0");
			const dd  = d.getUTCDate().toString().padStart(2, "0");
			const mon = d.toLocaleString("en", { month: "short", timeZone: "UTC" });
			const yy  = d.getUTCFullYear().toString().slice(-2);
			el.innerHTML = `${hh}:${mm} ${dd}/${mon}/${yy}<i class="iAGT-dest-gmt"> (${gmtLabel})</i>`;
		};
		tick();
		this._state.destClockTimer = setInterval(tick, 30000);
	},

	/* ─────────────────── ATTRACTIONS PANEL LIVE CLOCK ─────────────────── */
	_fmtLocalClock () {
		const cfg  = this._getEffectiveConfig();
		const mode = cfg.attractionsClockMode || "home";
		const n    = new Date();
		let hh, mm, dd, mon, yy, sfx;
		if (mode === "zulu") {
			hh  = n.getUTCHours().toString().padStart(2, "0");
			mm  = n.getUTCMinutes().toString().padStart(2, "0");
			dd  = n.getUTCDate().toString().padStart(2, "0");
			mon = n.toLocaleString("en", { month: "short", timeZone: "UTC" });
			yy  = n.getUTCFullYear().toString().slice(-2);
			sfx = `<i class="iAGT-ci-clock-sfx"> (Z)</i>`;
		} else {
			hh  = n.getHours().toString().padStart(2, "0");
			mm  = n.getMinutes().toString().padStart(2, "0");
			dd  = n.getDate().toString().padStart(2, "0");
			mon = n.toLocaleString("en", { month: "short" });
			yy  = n.getFullYear().toString().slice(-2);
			sfx = "";
		}
		return `${hh}:${mm} ${dd}/${mon}/${yy}${sfx}`;
	},

	_startCiClock () {
		if (this._state.ciClockTimer) {
			clearInterval(this._state.ciClockTimer);
			this._state.ciClockTimer = null;
		}
		const tick = () => {
			const el = document.getElementById(`iAGT-ci-clock-${this.identifier}`);
			if (el) el.innerHTML = this._fmtLocalClock();
		};
		tick();
		this._state.ciClockTimer = setInterval(tick, 30000);
	},

	/* â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€ CUSTOM SCROLLBAR â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€ */
	_setupCustomScrollbar (scrollEl, wrapEl) {
		if (wrapEl._sbObserver) {
			wrapEl._sbObserver.disconnect();
			wrapEl._sbObserver = null;
		}
		const existing = wrapEl.querySelector(".iAGT-sb-track");
		if (existing) existing.remove();

		const track = document.createElement("div");
		track.className = "iAGT-sb-track";
		track.setAttribute("role", "scrollbar");
		track.setAttribute("aria-orientation", "vertical");
		track.setAttribute("aria-controls", scrollEl.id || "");
		track.setAttribute("aria-valuenow", "0");
		track.setAttribute("aria-valuemin", "0");
		track.setAttribute("aria-valuemax", "100");
		const thumb = document.createElement("div");
		thumb.className = "iAGT-sb-thumb";
		track.appendChild(thumb);
		wrapEl.appendChild(track);

		const update = () => {
			const { scrollTop, scrollHeight, clientHeight } = scrollEl;
			if (scrollHeight <= clientHeight) {
				track.style.opacity = "0";
				track.style.pointerEvents = "none";
				return;
			}
			track.style.opacity = "1";
			track.style.pointerEvents = "auto";
			const trackH = track.clientHeight;
			const thumbH = Math.max(20, (clientHeight / scrollHeight) * trackH);
			const maxScroll = scrollHeight - clientHeight;
			const thumbTop = maxScroll > 0 ? (scrollTop / maxScroll) * (trackH - thumbH) : 0;
			thumb.style.height = `${thumbH}px`;
			thumb.style.top = `${thumbTop}px`;
			const pct = maxScroll > 0 ? Math.round((scrollTop / maxScroll) * 100) : 0;
			track.setAttribute("aria-valuenow", String(pct));
		};

		scrollEl.addEventListener("scroll", update, { passive: true });

		thumb.addEventListener("mousedown", (e) => {
			const startY = e.clientY;
			const startScrollTop = scrollEl.scrollTop;
			e.preventDefault();
			e.stopPropagation();

			const onMove = (ev) => {
				const { scrollHeight, clientHeight } = scrollEl;
				const trackRange = track.clientHeight - thumb.clientHeight;
				const scrollRange = scrollHeight - clientHeight;
				if (trackRange > 0) {
					scrollEl.scrollTop = startScrollTop + (ev.clientY - startY) * (scrollRange / trackRange);
				}
			};
			const onUp = () => {
				document.removeEventListener("mousemove", onMove);
				document.removeEventListener("mouseup", onUp);
			};
			document.addEventListener("mousemove", onMove);
			document.addEventListener("mouseup", onUp);
		});

		/* UX-006: Touch support for custom scrollbar */
		thumb.addEventListener("touchstart", (e) => {
			const startY = e.touches[0].clientY;
			const startScrollTop = scrollEl.scrollTop;
			e.stopPropagation();

			const onTouchMove = (ev) => {
				const { scrollHeight, clientHeight } = scrollEl;
				const trackRange = track.clientHeight - thumb.clientHeight;
				const scrollRange = scrollHeight - clientHeight;
				if (trackRange > 0) {
					scrollEl.scrollTop = startScrollTop + (ev.touches[0].clientY - startY) * (scrollRange / trackRange);
				}
				if (ev.cancelable) ev.preventDefault();
			};
			const onTouchEnd = () => {
				document.removeEventListener("touchmove", onTouchMove);
				document.removeEventListener("touchend", onTouchEnd);
			};
			document.addEventListener("touchmove", onTouchMove, { passive: false });
			document.addEventListener("touchend", onTouchEnd);
		}, { passive: true });

		track.addEventListener("click", (e) => {
			if (e.target === thumb) return;
			const rect = track.getBoundingClientRect();
			const ratio = (e.clientY - rect.top) / track.clientHeight;
			scrollEl.scrollTop = ratio * (scrollEl.scrollHeight - scrollEl.clientHeight);
		});

		const mo = new MutationObserver(() => requestAnimationFrame(update));
		mo.observe(scrollEl, { childList: true, subtree: true });
		wrapEl._sbObserver = mo;
		requestAnimationFrame(update);
	},

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ SAVE / PRINT HANDLERS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	_saveAttractions (panelEl) {
		const name = this._state.currentDisplayedCity;
		if (!name) return;
		const info = this._state.cityInfo[name];
		if (!info) return;
		const things = info.attractions && info.attractions.things ? info.attractions.things : [];
		const airportPostcode = info.attractions && info.attractions.airportPostcode ? info.attractions.airportPostcode : null;
		const airportDistanceKm = info.attractions && info.attractions.airportDistanceKm ? info.attractions.airportDistanceKm : null;
		const saveBtn = panelEl && panelEl.querySelector(".iAGT-save-atts-btn");
		if (saveBtn) { saveBtn.textContent = "\u23F3"; saveBtn.disabled = true; }
		this._state.pendingSaveEl = { type: "attractions", panelId: panelEl ? panelEl.id : null };
		this.sendSocketNotification("iAGT_SAVE_ATTRACTIONS", { cityName: name, things, airportPostcode, airportDistanceKm });
	},

	_saveFlights (panelEl) {
		const saveBtn = panelEl && panelEl.querySelector(".iAGT-save-flights-btn");
		if (saveBtn) { saveBtn.textContent = "\u23F3"; saveBtn.disabled = true; }
		this._state.pendingSaveEl = { type: "flights", panelId: panelEl ? panelEl.id : null };
		const legs = this._state.flightLegs.map((l) => ({
			travelerName: l.travelerName || "",
			flightNumber: l.flightNumber || "",
			departureDate: l.departureDate || "",
			departureTime: l.departureTime || "",
			status: l.status || "scheduled",
			progress: l.progress || 0,
			type: l.type || "",
			actualDeparture: l.actualDeparture || null,
			estimatedArrival: l.estimatedArrival || null,
			from: l.from ? { name: l.from.name || "", iata: l.from.iata || "" } : null,
			to: l.to ? { name: l.to.name || "", iata: l.to.iata || "" } : null
		}));
		this.sendSocketNotification("iAGT_SAVE_FLIGHTS", { legs, scenario: this.config.scenario });
	},

	_saveTerminalMaps (panelEl) {
		const saveBtn = panelEl && panelEl.querySelector(".iAGT-save-terminal-btn");
		if (saveBtn) { saveBtn.textContent = "\u23F3"; saveBtn.disabled = true; }
		this._state.pendingSaveEl = { type: "terminal_maps", panelId: panelEl ? panelEl.id : null };
		const destinations = [];
		const seen = new Set();
		this._state.flightLegs.forEach((l) => {
			if (l.to && l.to.iata && !seen.has(l.to.iata)) {
				seen.add(l.to.iata);
				destinations.push({ name: l.to.name || "", iata: l.to.iata });
			}
		});
		this.sendSocketNotification("iAGT_SAVE_TERMINAL_MAPS", { destinations });
	},

	/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ DEPARTURE ALERT NOTIFICATION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
	_scheduleAlertTimer () {
		if (this._state.alertTimer) { clearTimeout(this._state.alertTimer); this._state.alertTimer = null; }
		const alertHours = Number(this.config.departureAlertHours) || 0;
		if (alertHours <= 0) return;

		const legs = this._getFilteredLegs();
		const future = legs.filter((l) => l.status === "scheduled" && l.departureDate);
		if (!future.length) return;

		const first = future.reduce((a, b) => (new Date(a.departureDate) <= new Date(b.departureDate) ? a : b));

		const depTime = new Date(`${first.departureDate}T${first.departureTime || "00:00"}:00`);
		const alertTime = depTime.getTime() - alertHours * 3600000;
		const delay = alertTime - Date.now();

		if (delay <= 0 || this._state.alertFired) return;

		this._state.alertTimer = setTimeout(() => {
			this._state.alertFired = true;
			this.sendNotification("IAGT_DEPARTURE_ALERT", {
				flightNumber: first.flightNumber || "",
				departureDate: first.departureDate || "",
				from: first.from || null,
				to: first.to || null,
				hoursUntil: alertHours
			});
			Log.info(`[${this.name}] Departure alert fired for ${first.flightNumber || "unknown"}`);
		}, delay);
	},

	stop () {
		if (this._state.mapRoot) {
			this._state.mapRoot.dispose();
			this._state.mapRoot = null;
		}
		if (this._state.overlayHideTimer) {
			clearTimeout(this._state.overlayHideTimer);
			this._state.overlayHideTimer = null;
		}
		if (this._state.zenModeTimer) {
			clearTimeout(this._state.zenModeTimer);
			this._state.zenModeTimer = null;
		}
		if (this._state.cdTimer) { clearInterval(this._state.cdTimer); this._state.cdTimer = null; }
		if (this._state.cityTimer) { clearInterval(this._state.cityTimer); this._state.cityTimer = null; }
		if (this._state.testTimer) { clearInterval(this._state.testTimer); this._state.testTimer = null; }
		if (this._state.alertTimer) { clearTimeout(this._state.alertTimer); this._state.alertTimer = null; }
		if (this._state.saveToastTimer) { clearTimeout(this._state.saveToastTimer); this._state.saveToastTimer = null; }
		if (this._state.visitedPopupTimer) { clearTimeout(this._state.visitedPopupTimer); this._state.visitedPopupTimer = null; }
		const popup = document.querySelector(`#iAGT-wrapper-${this.identifier} .iAGT-visited-popup`);
		if (popup) popup.remove();
		this._stopGlobeAutoRotation();
		this._stopAttractionsAutoScroll();
		Log.info(`[${this.name}] Stopped`);
	}
});

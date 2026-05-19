/* iAGT.StateController.js - Centralized state management (STR-002) */
var IagtStateController = class {
	constructor(config) {
		this.flightLegs = [];
		this.cityInfo = {};
		this.visitedCountryIsos = [];
		this.regionData = {};

		this.mapChart = null;
		this.mapRoot = null;
		this.mapRootContainer = null;
		this.mapReady = false;
		this.polygonSeries = null;
		this.graticuleSeries = null;
		this.regionSeriesList = [];
		this.regionsVisible = !!(config && config.showSubnationalRegions);
		this.planeKeys = null;

		this.tripReset = false;
		this.noApiKey = false;
		this.visitedHighlightEnabled = true;

		this.cityIndex = 0;
		this.cityTimer = null;
		this.lastShownCity = null;
		this.currentDisplayedCity = null;
		this.cityDisplayListCache = null;

		this.travelerColors = {};
		this.travelerSymbols = {};

		this.testTimer = null;
		this.testLegs = [];
		this.testLegIndex = 0;
		this.testProgress = 0;
		this.testPhase = "flying";
		this.testPauseCount = 0;

		this.cdTimer = null;
		this.validateTimer = null;
		this.attractionsScrollTimer = null;
		this.attractionsScrollIndex = 0;
		this.alertFired = false;
		this.alertTimer = null;
		this.pendingSaveEl = null;
		this.saveToastTimer = null;
		this.overlayHideTimer = null;
		this.weatherRefreshTimer = null;
		this.visitedPopupTimer = null;

		this.lastAirportFingerprint = null;
		this.lastProjection = null;
		this.ciClockTimer = null;
		this.destClockTimer = null;
	}

	reset(config) {
		this.flightLegs = [];
		this.cityInfo = {};
		this.visitedCountryIsos = [];
		this.regionData = {};

		this.mapChart = null;
		this.mapRoot = null;
		this.mapRootContainer = null;
		this.mapReady = false;
		this.polygonSeries = null;
		this.graticuleSeries = null;
		this.regionSeriesList = [];
		this.regionsVisible = !!(config && config.showSubnationalRegions);
		this.planeKeys = null;

		this.tripReset = false;
		this.noApiKey = false;
		this.visitedHighlightEnabled = true;

		this.cityIndex = 0;
		this.cityTimer = null;
		this.lastShownCity = null;
		this.currentDisplayedCity = null;
		this.cityDisplayListCache = null;

		this.travelerColors = {};
		this.travelerSymbols = {};

		this.testTimer = null;
		this.testLegs = [];
		this.testLegIndex = 0;
		this.testProgress = 0;
		this.testPhase = "flying";
		this.testPauseCount = 0;

		this.cdTimer = null;
		this.validateTimer = null;
		this.attractionsScrollTimer = null;
		this.attractionsScrollIndex = 0;
		this.alertFired = false;
		this.alertTimer = null;
		this.pendingSaveEl = null;
		this.saveToastTimer = null;
		this.overlayHideTimer = null;
		this.weatherRefreshTimer = null;
		this.visitedPopupTimer = null;

		this.lastAirportFingerprint = null;
		this.lastProjection = null;
		this.ciClockTimer = null;
		this.destClockTimer = null;
	}

	clearTimers() {
		const timers = [
			"cdTimer", "validateTimer", "attractionsScrollTimer",
			"alertTimer", "saveToastTimer", "overlayHideTimer",
			"weatherRefreshTimer", "visitedPopupTimer", "cityTimer", "testTimer",
			"ciClockTimer", "destClockTimer"
		];
		timers.forEach((t) => {
			if (this[t]) {
				clearTimeout(this[t]);
				clearInterval(this[t]);
				this[t] = null;
			}
		});
	}
};

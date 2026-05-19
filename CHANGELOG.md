# Changelog — MMM-iAmGoingThere

All notable changes to this module will be documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.3.3] - 2026-05-18

### Added
- **UEFA Attractions Expansion — 2010–2023 (Phase 2)** — 33 new city attraction JSON files covering all cities with a UEFA Champions League, Europa League or Europa Conference League participant between 2010–11 and 2022–23 that were not previously in the attractions database.
- **UEFA Attractions Expansion — 2023–25 (Phase 1)** — 45 new city attraction JSON files covering all cities with a UEFA CL/EL/UECL participant in the 2023–24 or 2024–25 seasons not previously in the database.
- **UEFA Competition Reference Document** — New `documents/uefaLeagueCompetitionParticipants.md` listing all UCL, UEL and UECL group/league phase participants from 2010–11 to 2024–25 with their city JSON file reference, organised by competition.
- Total attractions coverage now **544 cities**.

---

## [2.3.2] - 2026-05-17

### Added
- **Scotland City Expansion** — 17 new attraction JSON files for Scottish cities/towns with population > 25,000 not previously covered: `dundee`, `inverness`, `perth_scotland`, `stirling`, `paisley`, `east_kilbride`, `livingston`, `hamilton_scotland`, `dunfermline`, `cumbernauld`, `kirkcaldy`, `greenock`, `falkirk`, `glenrothes`, `airdrie`, `motherwell`, `dumfries`. Nearest airport used for each city (`DND`, `INV`, `EDI`, `GLA`, `PIK`).
- **Ireland City Expansion** — 7 new attraction JSON files for Irish cities/towns with population > 25,000 not previously covered: `galway`, `waterford`, `drogheda`, `dundalk`, `kilkenny`, `navan`, `bray`. Airports used: `SNN` (Shannon), `WAT` (Waterford), `DUB` (Dublin).
- Total attractions coverage now **466 cities**, all files fully populated with all 7 required fields.

---

## [2.3.1] - 2026-05-17

### Added
- **Shannon (SNN) Attractions** — New `data/attractions/shannon.json` with top 10 attractions for Shannon, County Clare, Ireland (IATA: SNN). 

### Fixed
- **Attractions Data Completeness** — All 441 attraction JSON files now fully populated with all 7 required fields (`rank`, `name`, `postcode`, `distanceKmFromAirport`, `description`, `distance`, `URL`). Previously 435 files had one or more null/missing fields. Fields were resolved using real-world geographic data and verified official tourism URLs for each attraction.

---

## [2.3.0] - 2026-05-12

### Added
- **TZ-001: International Date Line & Multi-Timezone Fix** — Flight status is now determined entirely in UTC using airport longitude to compute the correct local-to-UTC offset. This eliminates incorrect "not yet departed" status for flights that cross or originate near the International Date Line (e.g. Fiji → Auckland) when viewed from a different timezone. Both server-side polling (`FlightAwareService.js`) and client-side countdown (`updateCountdown`) use the same longitude-based UTC estimate, ensuring consistent results regardless of whether the viewer's device is in the UK, New Zealand, or anywhere else.
- **Destination City Live Clock (Flight Panel Header)** — The flight data panel title bar now shows the local time at the traveller's current destination city in the top-left corner, formatted as `HH:MM DD/Mon/YY`. The UTC offset derived from the destination airport's longitude is shown alongside in smaller italic as `(GMT+x)` / `(GMT−x)`. The clock updates every 30 seconds and switches automatically between active-flight destination and last-landed destination.
- **Attractions Panel Clock Repositioned** — The live clock in the attractions panel header is now left-aligned (moved from the right side) and restyled to match the flight panel clock: smaller `0.75em` italic font, semi-transparent white, matching weight and spacing.
- **`attractionsClockMode` Config Option** — Controls which time reference the attractions panel clock displays. Set `attractionsClockMode: "zulu"` to show UTC time with a `(Z)` suffix; set `"home"` (default) to show the viewer's local device time with no suffix.

### Fixed
- **Attractions Panel Always Shows Traveller's Current Location** — The attractions panel now unconditionally displays city info for the traveller's current physical location. When one or more flights are "In Flight", it rotates through all active-flight destination cities regardless of the `autoRotateAttractionsData` setting. When all flights have landed it shows the most recently departed leg's destination (sorted by UTC departure time), again regardless of `autoRotateAttractionsData`. Previously this required `autoRotateAttractionsData: true` and the panel would show the final trip destination (e.g. London) instead of the current stop (e.g. Auckland).
- **Race Condition in Attractions Panel Update (iAGT_FLIGHT_UPDATE)** — Resolved a race condition where `updateCityInfo()` (called on every flight-data poll when `attractionsAutoScroll: false`) was scheduling a 300 ms fade at the same time as `_maybeAutoRotateAttractions()`, causing the two deferred DOM writes to arrive simultaneously and the last writer (London) to win. `_maybeAutoRotateAttractions()` now runs last and `updateCityInfo()` is guarded by `!lastShownCity` so it only fires on the very first load.

### Changed
- **Plane Icon Size** — Default aircraft marker scale reduced by 30% from `0.12` to `0.084`. Any per-leg `scale` override in the data context is unaffected.

---

## [2.2.0] - 2026-05-07
    
### Added (Phase 4 — UX & Innovation)
- **UIX-001: Zen Mode (Auto-hide UI Controls)** — New `zenMode: true` config option. When active, all on-screen UI overlays (flight table, city info, selectors, pan/zoom controls) automatically fade out after `autoHideDelay` seconds of inactivity. Any mouse movement, click, or keyboard event within the module area immediately restores the UI.
- **UIX-002: Color Blind Mode Support** — Expanded accessibility with `colorBlindMode: true`. This switches the Traveler palette in Scenario 3 to an IBM-designed 10-color blind safe set (optimized for Deuteranopia, Protanopia, and Tritanopia) and adjusts status indicator colors for better contrast.
- **UIX-003: Interactive "Fly-to" Navigation** — Clicking any flight row in the overlay table now triggers a smooth map animation (`flyToOnRowClick: true`) that zooms and pans to center the specific flight leg. Includes a 2-second visual pulse on the arrival marker.
- **INN-001: AI Destination Insights** — Integrated optional LLM "Fun Facts" via `funFactsEnabled: true`. Fetches single-sentence trivia about the destination city from any OpenAI-compatible endpoint. Displayed in a styled banner above the attractions list.
- **INN-002: Calendar-Driven Scenarios** — Module can now automatically switch scenarios based on upcoming events from the MagicMirror `calendar` module using `calendarDrivenScenario: true` and a `calendarScenarioMap` keyword lookup.

### Fixed
- **Plane Visibility & Animation** — Resolved a regression where aircraft markers (`PLANE_SVG`) became invisible on the map. Refactored the bullet factory and animation adapters to ensure smooth position and opacity transitions even during rapid map updates or scenario switches.
- **Scenario Switching Logic** — Fixed a bug where scenario-specific overrides (zoom, travelers, etc.) were ignored when switching scenarios via the on-screen selector. All configuration logic now correctly respects merged properties from `_getEffectiveConfig()`.

## [2.1.0] - 2026-05-06

### Added (Phase 3 — Performance & Caching)
- **SCN-003: Multi-Traveler Sync Improvements** — Enhanced Scenario 3 (Group Travel) test animation with longitude-based UTC offset calculation. This ensures multi-leg journeys across timezones (e.g. EDI->SNN->ORD->BOS) maintain correct chronological sequence in the test loop.
- **PER-004: Stable Plane Marker Series** — `iAGT.FlightProcessor.js` now populates the plane marker series with ALL legs for the current scenario/day, using `alpha: 0` for inactive flights. This prevents destructive `setAll()` calls when planes land or depart, resolving issues where plane icons were slow to appear or flickered during transitions.
- **SCN-004: Multi-Active Attraction Rotation** — When `autoRotateAttractionsData: true`, the attractions panel now automatically rotates through the destinations of all currently in-flight aircraft (Scenario 3). Rotation timing is controlled by `cityInfoCycleInterval`.
- **PER-002: Low Power Mode** — New `lowPowerMode: true` config option for Raspberry Pi Zero or older hardware. When enabled:
  - Adds `.iagt-low-power` CSS class to the module wrapper, disabling all `backdrop-filter: blur()` GPU compositing effects on flight-details, city-info, pan/zoom controls, selector dropdowns, and the visited-country popup.
  - Automatically caps `gcPoints` to `30` (from the default `100`) to reduce the number of Great Circle arc vertices processed each render cycle.
- **PER-003: Lazy Asset Loading** — `football_teams_database.csv` (69 KB, ~6 000 rows) is no longer loaded eagerly at startup. It is now deferred in `node_helper.js` and loaded on-demand only when Scenario 6 is active, reducing cold-start memory allocation for all other scenarios.
- **CCH-001: Disk-persistent Weather Cache** — `services/WeatherService.js` now persists its Open-Meteo weather cache to `cache/weather_cache.json`. On module or system restart the cache is rehydrated from disk; entries older than 30 minutes are discarded automatically, eliminating redundant API calls after reboots.

### Refactored (Phase 2 — Structural Refactoring)
- **PER-001 / STR-001: Service-Oriented Backend** — `node_helper.js` reduced from 1620 → 516 lines (68%) by extracting three dedicated service classes:
  - `services/FlightAwareService.js` — AeroAPI polling, ETag caching, leg update logic, trip-reset detection.
  - `services/WeatherService.js` — Open-Meteo weather fetching with 30-minute in-memory cache.
  - `services/FileSystemProvider.js` — All CSV/JSON I/O, airport/city/football-team resolution, geodata building, HTML document generation, and visited-country persistence.
- **PER-001: Frontend Code Splitting** — `MMM-iAmGoingThere.js` reduced from 2761 → 2472 lines by extracting two browser-compatible global modules loaded via `getScripts()`:
  - `lib/iAGT.FlightProcessor.js` — Pure data-processing namespace (`IagtFlightProcessor`) covering filtered legs, traveler maps, great-circle caching, bearing calculation, GeoJSON line building, and airport/plane marker construction.
- **STR-002: Centralised State Management** — All 35+ module-level state variables moved into `lib/iAGT.StateController.js` (`IagtStateController`). The `start()` method now initialises a single `this._state` object; all references throughout the file updated accordingly.

## [2.0.1] - 2026-05-04

### Added
- **Polar Ice Cap Suppression** — New `hideIceCaps` config option to hide the Antarctica region on all map projections except the Globe (Orthographic).
- **Directional Nudge Control** — Added a new 4-way arrow control for fine-tuning the map's screen position without altering the geographic projection. Positioned to the left of the zoom control.
- **Auto-Hide UI Controls** — New `hideControlsUntilHover` config option that hides all on-screen controls (pan, zoom, selectors, nudge) until the mouse hovers over the map container.

### Fixed
- **Plane Rotation Alignment** — Improved the aircraft nose rotation logic to accurately follow the Great Circle path curvature on all map projections.


---

## [2.0.0] - 2026-04-29

### Added
- **Scenario 4: Visited Country Coloring** — Automatically colors countries visited in travel history mode green (configurable via `colorVisitedCountry`). Includes support for city-name and football-team resolution.

- **Manual Country Coloring** — Right-click any country on the map to toggle its "visited" status. Manual selections are saved to `data/manual_visited_countries.json` and persist across reloads.- **Right-click Confirmation Popup** — Right-clicking a country now shows a popup with the country name, its current visited status, and **"Mark as Visited"** / **"Remove Visited"** / **"Cancel"** buttons (auto-dismisses after 5 s).
- **Translated Popup** — Popup text routes through the translation system and is available in all 33 supported languages.
- **Works in All Scenarios** — Manual country marking via right-click is available in every scenario, not just Scenario 4.

- **Highlights Control Dropdown** — A new dropdown below the Map Projection selector provides **"Highlight Visited Countries"** (default), **"No Highlights"** (suppress display without deleting data), and **"Clear Manually Marked Cache"** (wipe `manual_visited_countries.json`).
- **Highlight State Persists** — Selecting "No Highlights" suppresses all country highlights until you manually re-select "Highlight Visited Countries" or restart the module.

- **On-Screen Sub-Region Toggles** — Added "Show Sub Regions" and "Hide Sub Regions" options to the Highlights dropdown for real-time visibility control without module restart.

- **UK Home Nations Resolution** — Scotland, England, Wales, and Northern Ireland are now automatically resolved to the GB ISO code for sub-national mapping and visited-country highlighting.

- **Sub-national Region Layers** — Support for high-detail region polygons (States, Provinces, Departments, etc.) for 130+ countries, including detailed coverage for the United Kingdom (England, Scotland, Wales, and Northern Ireland).

- **Graticule Grid** — Configurable latitude/longitude grid (`showGraticule`) with customizable step, color, width, and opacity.
- **Globe Auto-Rotation** — New `autoRotateGlobeToPlane` option to automatically rotate the globe to keep the active flight's plane icon centered and visible.
- **Dynamic Attractions** — The attractions panel now automatically updates to show the destination city (or origin fallback) of active flights in live or test mode.
- **Ocean vs. Background Coloring** — Separated coloring for the map ocean (`colorMapOcean`) and the surrounding area (`colorMapBackground`) for a cleaner look in Globe/Orthographic projections.
- **Config Options** — Added `autoRotateGlobeToPlane`, `graticuleWidth`, `colorVisitedCountry`, `colorVisitedCountryBorder`, `colorVisitedCountryOpacity`, `showSubnationalRegions`, `subnationalAllCountries`, `subnationalCountries`, `colorMapBackground`, and `colorMapOcean`.

### Fixed
- **Marker Click Handler** — Simplified attraction lookup to use destination name, improving reliability for cities without IATA codes in Scenario 4 and 6.

---

## [1.9.0] - 2026-04-06

### Added
- **Scenario 6: Football Away Days** — New CSV-driven scenario (`data/footballAwayTrips.csv`) specifically for tracking European football away fixtures.
- **Stadium Coordinate Resolution** — Added a comprehensive `data/football_teams_database.csv` (500+ teams) to resolve stadium coordinates from team names.
- **Unicode Accent Normalization** — `node_helper.js` now normalizes Unicode characters (ø, ö, é, etc.) during team resolution, allowing matches for names like "Bodø/Glimt".
- **Visible Fallback Markers** — Rebuilt marker rendering in `MMM-iAmGoingThere.js` to use a `Container` with a visible background circle. This ensures markers are always visible even if the corresponding club crest image is missing.
- **Multi-visit Tooltip Aggregation** — Scenario 6 markers now aggregate all visits to the same stadium into a single rich tooltip showing Date, Opponent, Competition, Score, and Result for every trip.
- **Scenario Troubleshooting Guide** — Created `documents/Troubleshooting.md` with generic and scenario-specific advice.

### Changed
- **Crest Marker Sizing** — Reduced club crest marker dimensions by 50% (from 34px to 17px) to maintain map clarity when displaying dense fixture lists.
- **Dynamic Trip Titles** — Refactored title management so that `tripTitle` correctly reflects the active scenario selected via the on-screen dropdown.
- **Scenario 6 API Guard** — AeroAPI polling is now automatically disabled for Scenario 6 as it uses static fixture data.

### Fixed
- **Scenario Selector Partial Config Bug** — Fixed a bug where the frontend only sent a partial configuration to the backend during scenario switches, which prevented Scenarios 1-4 from displaying flights.
- **Scenario 6 "Sinkhole" Fix** — Eliminated the bug where all unresolved teams defaulted to 0,0 coordinates; unresolved teams are now skipped with a descriptive warning in the log.

---

## [1.8.0] - 2026-04-05

### Added
- **Interactive UI Controls** — Added on-screen pan and zoom controls for manual map navigation.
- **Traditional Compass Needle** — Redesigned the center pan button into a traditional diamond-shaped magnetic needle (Red for North, White for South). The needle rotates in real-time to always point North regardless of map rotation.
- **On-Screen Map Projection Selector** — A dropdown in the top-left corner allows switching between Mercator, Equirectangular, Natural Earth, and Orthographic (Globe) projections instantly.
- **On-Screen Scenario Selector** — A dropdown in the top-right corner allows switching between all 5 scenarios without restarting or editing `config.js`.
- **Visibility Toggles for All Controls** — New configuration options `showPanControl`, `showZoomControl`, `showMapSelector`, and `showScenarioSelector` (all `true` by default) allow users to hide any of the on-screen UI elements.
- **Master Configuration Support** — Users can now define multiple scenarios (Scenario 1-5) within a single module configuration block and switch between them using the on-screen selector.

### Changed
- **Pan/Zoom Increments** — Panning now moves the map in 0.5-degree steps, and zoom buttons increment by 0.1 for finer control.
- **Home Button Behavior** — Clicking the center compass button now re-orients the map to North (0,0 rotation) while maintaining the current zoom level.
- **Unified Control Styling** — All on-screen controls (Pan, Zoom, Selectors) now share a consistent glassmorphism design with blurred backgrounds and semi-transparent borders.

---

## [1.7.0] - 2026-04-01

### Added

- **Configurable map projection (`mapProjection`)** — new string config option selects the amCharts 5 geographic projection. Supported values: `"mercator"`, `"naturalEarth1"`, `"equirectangular"`, `"orthographic"`, `"stereographic"`. Default changed from `"naturalEarth1"` to `"mercator"` so that great-circle flight paths (e.g. UK→USA) curve visibly northward over Greenland rather than appearing as near-straight lines. The projection is resolved at `initMap()` time via a string→function lookup map; unknown strings fall back to `"mercator"`.
- **Live inflight telemetry — `heading` and `altitudeChange` fields** — `node_helper.js` `updateLegFromAPI()` now extracts `pos.heading` and `pos.altitude_change` from the AeroAPI `last_position` object and stores them as `leg.heading` and `leg.altitudeChange`. Both fields are initialised to `null` in `mkLeg()` for backward compatibility.
- **Inflight telemetry chip in flight table** — `buildTableHTML()` renders a 📡 chip beneath active-flight rows containing: `Alt: X,XXX ft`, `XXX kts`, `Hdg: XXX°`, `Rate: ▲ Climb / ▼ Desc / → Level`, and `Upd: HH:MM`. The chip is only rendered when at least one live position field is non-null.
- **Rich grouped telemetry in plane tooltip** — the plane marker tooltip now shows a grouped live-data block when any of `groundspeed`, `altitude`, or `heading` is available: two lines (`Alt … Spd …` and `Hdg … Rate …`), each field falling back to `—` when absent. Heading (degrees) and Rate (from `altitude_change`) are new additions; the update time label shortened to `Upd:`.
- **Tooltip white-text CSS rule** — `[id^="iAGT-map-"] svg text { fill: #ffffff !important }` added to `MMM-iAmGoingThere.css` to force white fill on all SVG text inside the amCharts map container, overriding any inherited dark-theme colour from MagicMirror's global stylesheet.

### Changed

- **`gcPoints` default raised from `60` to `100`** — more interpolation points per great-circle leg produce a smoother animated progress-split arc on active flights and give the antimeridian-crossing algorithm finer granularity.
- **All three amCharts 5 tooltip instances rebuilt** — home-airport marker, destination-airport marker, and plane-icon marker tooltips now use: `autoTextColor: false` (prevents amCharts overriding label colour), `getFillFromSprite: false`, dark background `#0d1117` (`fillOpacity: 0.96`), `#4499FF` blue border (`strokeWidth: 1`), and `#ffffff` label fill at `fontSize: 12`. Background is set via the correct amCharts 5 API (`_tip.get("background").setAll(…)`).

### Fixed

- **AeroAPI zero-second query window** — `fetchFlightStatus()` was passing `?start=YYYY-MM-DD&end=YYYY-MM-DD` with identical dates. FlightAware AeroAPI interprets bare date strings as midnight UTC, making start == end a zero-second window that returns no flights. `end` is now computed as the next calendar day (`new Date(date + "T00:00:00Z")` with `setDate(+1)`), ensuring the full 24-hour flight window is queried.
- **Test mode map never rendered** — `startTestAnimation()` fired a `setInterval` at ~33 ms (30 fps). Each tick called `updateMapLines()`, which coalesces calls through a 250 ms debounce. Because new calls arrived every 33 ms, the debounce was perpetually reset and `_flushMapLines()` was never invoked — the map stayed blank in test mode. Fixed by having the animation tick call `_flushMapLines()` directly, bypassing the debounce.
- **Variable-name encoding corruption in `_calculateBearing()`** — a prior PowerShell file-write (using default Windows-1252 encoding on a UTF-8 file) double-encoded the Greek variable names `φ1`, `φ2`, `Δλ` into invalid multi-byte sequences (`Ï†1`, `Ï†2`, `Î"Î»`), causing a JS `SyntaxError: Missing initializer at const declaration` at startup. All three identifiers renamed to ASCII equivalents: `phi1`, `phi2`, `dLon`.

---

## [1.6.0] dev - 2026-03-31

### Added

- **Scenario 5 — Aircrew / Frequent Flyer CSV Roster** — a new scenario that reads flight legs from a plain CSV file (`data/my_flights.csv`). Columns: `departureDate`, `flightNumber`, `from`, `to`, `departureTime` (optional), `travelerName` (optional), `type` (optional). Full FlightAware live tracking is supported. Schedule changes take effect on MagicMirror restart without touching `config.js`.
- **`crewFlightsFile` config option** — path to the CSV file used by Scenario 5, relative to the module directory. Defaults to `data/my_flights.csv`. Includes path-containment validation.
- **Sample `data/my_flights.csv`** — five example flights over a 14-day period demonstrating the CSV format.

---

## [1.5.0] dev - 2026-03-31

### Added

- **Plane position tweening (D1)** — when the same active plane is showing across successive map updates, position changes are now animated via `dataItem.animate({ key: "latitude/longitude", duration: 1000 })` rather than teleporting. Falls back to `setAll()` when the active plane set changes.
- **Boarding info countdown card (D2)** — when departure is within 24 hours, the countdown box switches to a high-visibility amber boarding card displaying flight number, terminal, gate, and ETD. Restores to normal once the leg becomes active.
- **Responsive narrow layout (D3)** — a new `narrowBreakpoint` config option (default `900` px) controls a `@media` CSS rule that sets both overlay panels to `95 vw` and stacks them vertically on narrow screens. The rule is injected as a scoped `<style>` element at `getDom()` time so each module instance can have its own breakpoint.
- **Hourly weather refresh (D4)** — a `setInterval` started after `iAGT_INIT` re-fetches Open-Meteo weather for every destination city each hour. The refreshed timestamp is rendered as a small italic `Updated HH:MM` line inside the weather pill in both `updateCityInfo()` and `_renderCityByName()`.

---

## [1.4.0] dev - 2026-03-31

### Changed

- **Debounced map render (C1)** — `updateMapLines()` now coalesces rapid calls through a 250 ms `clearTimeout`/`setTimeout` debounce (using the existing `_validateTimer` slot). The actual `setAll()` work moved to a new `_flushMapLines()` method.
- **`_apiCache` eviction (C2)** — at the end of each `pollAllFlights()` cycle, cache entries older than 3 600 000 ms (1 hour) are deleted, bounding memory growth to roughly the number of flights polled in the last hour.
- **Parallel flight polling (C3)** — the sequential `await sleep(2000)` loop between poll requests is replaced by `Promise.allSettled()` dispatching up to 3 requests concurrently (batches of 3). Per-leg back-off and the `updated` flag are preserved via `forEach` over settled results.
- **Phase-aware API cache TTL (C4)** — `fetchFlightStatus()` now selects TTL based on flight phase: `active` → 1 min; `scheduled` within 2 h → 2 min; `scheduled` beyond 2 h → 10 min; `landed` → 15 min; `cancelled` → 30 min. Replaces the previous fixed 1 min / 15 min split.

---

## [1.3.1] dev - 2026-03-30

### Added

- **Delayed flight badge (NEW-15 / MEDIUM)** — when a flight is delayed by more than 15 minutes (estimated vs scheduled departure), an amber `+Nm` badge is displayed next to the flight status in the table.
- **Connection risk indicator (NEW-14 / MEDIUM)** — a `⚠` warning icon is shown for connecting legs if the layover is under 90 minutes and the inbound leg is delayed, providing at-a-glance connection risk awareness.

### Fixed

- **Plane tooltip line breaks (NEW-10 / MEDIUM)** — replaced `\n` with the amCharts 5 `{newLine}` token in the plane bullet `tooltipContent`. Multi-line tracking data now renders correctly in the SVG tooltip instead of collapsing into a single line.
- **Gate "0" falsy coercion (NEW-06 / LOW)** — replaced falsy `|| null` checks with explicit `!= null` checks for all gate and terminal fields in `node_helper.js`. This ensures valid gate numbers like `"0"` are correctly displayed rather than being treated as absent.
- **`.iAGT-delay-badge` CSS** — added amber styling for delay and connection risk indicators.

---

## [1.3.0] dev - 2026-03-30

### Fixed

- **amCharts 5 memory leak (NEW-02 / CRITICAL)** — `stop()` now explicitly calls `this._mapRoot.dispose()` and nulls the reference. This ensures WebGL contexts, animation frames, and DOM listeners are correctly released when the module is removed or hot-reloaded.

- **`_overlayHideTimer` leak (NEW-03 / MEDIUM)** — added `clearTimeout(this._overlayHideTimer)` to `stop()` to prevent the auto-hide callback from firing on a stale DOM after the module has been stopped.

- **Sanitized API error logging (NEW-13 / MEDIUM)** — poll failure logs in `node_helper.js` now only include `e.message` rather than the full error object, preventing accidental exposure of sensitive request metadata or keys in logs.

---

## [1.2.1] dev - 2026-03-30

### Fixed

- **XSS via `leg.aircraftType` in flight detail chip (NEW-01 / CRITICAL)** — the aircraft type string returned by FlightAware AeroAPI was interpolated directly into `innerHTML` in the detail chip builder without HTML-escaping. A malicious or unexpected API response could inject arbitrary HTML. `this._esc()` is now applied to `leg.aircraftType` and `leg.tailNumber` at the chip construction site in `buildTableHTML()`.

- **`cityAttractions_Xaxis` / `_Yaxis` positioning silently ignored (NEW-04 / HIGH)** — despite being declared, documented, and described as working config options, `getDom()` hardcoded `"0"` for both `style.bottom` and `style.right` on the attractions overlay div. The config values were never read. Both properties now use `Number.isFinite(this.config.cityAttractions_Yaxis)` and `Number.isFinite(this.config.cityAttractions_Xaxis)` guards matching the existing pattern used for the flight table panel.

- **AeroAPI date-scoping query params stripped (NEW-05 / HIGH)** — `fetchFlightStatus()` was building the request path as `/aeroapi/flights/${ident}` with no query parameters, causing AeroAPI to return all historical and future flights matching the flight number rather than only the specific scheduled date. The `?start=${date}&end=${date}` parameters have been restored. This is safe because `date` is validated against `/^\d{4}-\d{2}-\d{2}$/` before `fetchFlightStatus()` is called (SEC-004, v0.5.0).

---

## [1.2.0] dev - 2026-03-29

### Added

- **Gate & Terminal information** — `node_helper.js` now extracts `terminal_origin`, `terminal_destination`, `gate_origin`, and `gate_destination` from the AeroAPI flight response and stores them as `leg.departureTerminal`, `leg.departureGate`, `leg.arrivalTerminal`, and `leg.arrivalGate`. When present, these are displayed in the flight table detail chip row as `T:X G:Y → T:X G:Y`.

- **Taxiing status** — `leg.detailedStatus` is set to the raw AeroAPI `status` string. `buildTableHTML()` checks for `"taxiing"` in the detailed status and overrides the generic "In Flight" label with `Taxiing ✈`, giving a distinct visual state during ground movement.

- **Detailed flight status** — the full AeroAPI status string is preserved in `leg.detailedStatus`. The flight table now distinguishes: Scheduled · Taxiing · Active (En Route) · Diverted · Arrived · Cancelled. A `Diverted ⚠` label is shown when the detailed status contains `"diverted"`.

- **Estimated & scheduled time chips** — `leg.scheduledDeparture`, `leg.estimatedDeparture`, and `leg.scheduledArrival` are populated from AeroAPI `scheduled_out`, `estimated_out`, and `scheduled_in` fields. Formatted ETD and ETA are shown as monospace detail chips below each flight row.

- **FlightAware Foresight ETA** — when `foresight_predictions_available` is `true` and `predicted_in` is present in the AeroAPI response, the value is stored in `leg.foresightEta`. The ETA chip label switches to `ETA⚡` to visually distinguish AI-predicted arrivals from standard estimates.

- **Live tracking tooltip on plane icon** — hovering over the plane SVG on the map shows a tooltip containing: flight number, detailed status, latitude/longitude (3 decimal places), groundspeed (kts), altitude (ft), last position update time, and aircraft type/tail number. Built from `leg.groundspeed`, `leg.altitude`, and `leg.lastPositionUpdate` extracted from `last_position` in the AeroAPI response.

- **Aircraft type & tail number** — `leg.aircraftType` and `leg.tailNumber` are populated from AeroAPI `aircraft_type` and `registration` fields. Displayed in the first detail chip below each flight row as `✈ B77W (G-STBA)`.

- **`fmtDateTime()` helper** — locale-aware ISO timestamp formatter used for ETD/ETA chip display. Renders time as `HH:MM` using `toLocaleTimeString()`.

- **`.iAGT-details-row` and `.iAGT-detail-chip` CSS** — dark glassmorphism monospace chips styled with `rgba` borders and `0.80em` font size, appearing as a sub-row beneath each flight table row when AeroAPI data is available.

### Changed

- **`mkLeg()` extended with 13 new null-initialised fields** — `departureTerminal`, `departureGate`, `arrivalTerminal`, `arrivalGate`, `scheduledDeparture`, `estimatedDeparture`, `scheduledArrival`, `groundspeed`, `altitude`, `lastPositionUpdate`, `aircraftType`, `tailNumber`, `foresightEta`, `detailedStatus`. All default to `null` so legacy code and Scenario 4 (no API) remain unaffected.

- **`_initPointSeries()` plane bullet tooltip** — bullet `tooltipText` now uses `d.tooltipContent` (the multi-line tracking string) when available, falling back to `d.flightNumber`.

---

## [1.1.2] dev - 2026-03-16

### Fixed

- **Scenario 4 football team crests not appearing** — `buildAirportMarkers()` in `MMM-iAmGoingThere.js` was constructing the airport data object without forwarding the `crest` property. The bullet factory checked `d.crest` but it was always `undefined`, so the SVG marker was always rendered instead of the team crest image. The `crest` field is now explicitly included in every airport push object.

- **Crest path broken for multi-word country folders** — `loadFootballTeamsData()` in `node_helper.js` built crest file paths using the raw `Country` column value from `football_teams_database.csv` (e.g. `"The Netherlands"`). The `images/crests/` directory uses underscores for multi-word country names (e.g. `The_Netherlands/`). Spaces are now replaced with underscores when constructing the path, so `Ajax.png` correctly resolves to `images/crests/The_Netherlands/Ajax.png`.

- **Football team crest images flickering during test animation** — `updateMapLines()` called `_airportSeries.data.setAll()` on every tick of `_testTimer` (the test animation interval). Each `setAll()` destroys and recreates all bullet sprites, including `am5.Picture` elements. This forced the browser to re-fetch and re-paint each crest image on every frame, producing a visible flicker. `updateMapLines()` now computes a fingerprint string from each airport's coordinates, crest path, and colour, and only calls `setAll()` on the airport series when the fingerprint has changed. Plane positions continue to update every frame via `_planeSeries`, which is unaffected.

### Changed

- **`_lastAirportFingerprint` state property** — Initialised to `null` in the module's `start()` state block. Stores the last rendered airport data fingerprint so that `updateMapLines()` can skip redundant `am5.Picture` sprite recreations.

---

## [1.1.1] dev - 2026-03-15

### Fixed
- **Map viewport not applying `zoomLevel` / `zoomLongitude` / `zoomLatitude`** — The root cause was `panX: "none"` / `panY: "none"` on the `MapChart` constructor, which prevented amCharts 5 from applying any rotational centering — even when called programmatically via `goHome()`. Changed to `panX: "rotateX"` / `panY: "rotateY"` so that rotation-based centering is fully enabled.
- **`rotationX` / `rotationY` / `zoomLevel` applied directly in constructor** — Values are now set as first-class properties on `MapChart.new(root, { ... })` so the very first rendered frame is already positioned correctly. The previous approach relied solely on a deferred `goHome(0)` call which silently no-op'd against the pan restriction.
- **`goHome(0)` replaced with `chart.setAll()`** — The `frameended` handler now calls `chart.setAll({ rotationX, rotationY, zoomLevel })` directly, bypassing `goHome()`'s internal pan restriction that caused it to fail.
- **Null / undefined guard for zoom config values** — Replaced `|| 0` guards (which incorrectly treated the valid config value `0` as falsy) with explicit `!== undefined && !== null` checks for `zoomLongitude`, `zoomLatitude`, and `zoomLevel`.

### Added
- **`amCharts5_User_Guide.md`** — New documentation file covering amCharts 5 map projections, configuration patterns, and viewport tuning examples relevant to this module.

---

## [1.1.0] dev - 2026-03-15

### Added
- **Migration to amCharts 5** — The module now uses the modern `@amcharts/amcharts5` library for map rendering, replacing the deprecated `ammap3`. This provides better performance, native GeoJSON support, and improved antimeridian handling.
- **Local Vendor Scripts** — All amCharts 5 core, map, and geodata files are now hosted locally in the `vendor/` directory (`index.js`, `map.js`, `worldLow.js`). This eliminates dependency on external CDNs and resolves issues with network reliability and framework-level script loading.
- **GeoJSON-based Path Rendering** — Flight paths are now generated as GeoJSON `LineString` features with great-circle interpolation, ensuring accurate global curvature and better integration with modern map engines.
- **Great-Circle SLERP Interpolation** — Spherical Linear Interpolation (SLERP) math is used for all flight path generation, providing mathematically accurate arcs across the globe.

### Changed
- **Overlay Panel Positioning** — Both the flight table and attractions panel have been moved outside the map container in the DOM and are now positioned at the absolute bottom of the screen display (bottom-left and bottom-right respectively). This ensures they remain visible regardless of map height when used in full-screen regions.
- **Unified Panel Styling** — The city attractions panel now matches the flight data overlay panel in font size, color, and header styling. Headers are unified with `font-weight: 700` and `letter-spacing: 1.2px`. Attraction descriptions and numbers now use the same high-contrast white and gold color scheme as the flight table.
- **Flex-based Layout** — The main module wrapper now uses a flex-column layout with `min-height: 100vh`, ensuring it fills the screen in background regions and correctly positions the bottom-pinned overlays.

### Fixed
- **am5 is not defined** — Implemented a retry mechanism in `initMap` that waits for amCharts 5 components to be fully loaded and defined before attempting to render the map, resolving intermittent initialization failures.
- **Script Loading Compatibility** — Removed query parameters from vendor script URLs to fix a bug in MagicMirror's `loader.js` that prevented `.js` files with cache-busters from being recognized.

---

## [1.0.0] dev - 2026-03-13

### Added
- **Airport postcode & distance data** — `airportPostcode` and `airportDistanceKm` fields added to all **430+ city attraction JSON files** (`data/attractions/*.json`), covering every UN-recognised country with commercial air service. Data reflects the primary commercial airport serving each city.
- **Airport info in saved attractions HTML** — The `_buildAttractionsHtml()` helper in `node_helper.js` now renders an ✈ airport metadata line between the timestamp and the attractions table in the saved HTML file: `✈ Airport — Postcode: <strong>XXXX</strong> · Distance from city centre: <strong>N km</strong>`. Styled with a `.airport-meta` CSS class. The on-screen overlay panel is **not** affected.
- **Save Airport Terminal Maps to file** — A new teal 🗺 icon button appears in the flight data overlay panel title row, visually separated from the existing 🖨 flights button by a faint `|` divider. Clicking it collects every unique destination airport (IATA + name) from the current `flightLegs` list and sends `iAGT_SAVE_TERMINAL_MAPS` to `node_helper.js`.
- **`saveTerminalMapsFile()` node_helper method** — Creates `documents/MySavedTerminalMaps/` (auto-created) and writes `terminal_maps_[YYYY-MM-DD-HHMM].html`. The file is a responsive card-layout page — one card per destination airport — each showing the IATA code, full airport name, a **Google Maps terminal view** link, and a **Google terminal map search** link.
- **`_buildTerminalMapsHtml()` node_helper helper** — Generates the self-contained terminal maps HTML page. Gracefully handles an empty destinations list with a "No destination airports found" message.
- **`iAGT_SAVE_TERMINAL_MAPS` socket notification** — Frontend sends this; `node_helper.socketNotificationReceived()` routes it to `saveTerminalMapsFile()`.
- **`_saveTerminalMaps()` frontend method** — Collects unique `to` airports from `this.flightLegs` (deduped by IATA), sets the 🗺 button to ⏳ (disabled), then sends the notification.
- **`translations/translations.md`** — New documentation file listing all 33 supported locale codes with country flag icons and native language names.

### Changed
- **`iAGT_SAVE_OK` / `iAGT_SAVE_ERROR` handler** — Extended to recognise `type === "terminal_maps"`: selects `.iAGT-save-terminal-btn`, and restores the 🗺 icon (not 🖨) after 3 seconds.
- **`_saveAttractions()` payload** — Now includes `airportPostcode` and `airportDistanceKm` extracted from `info.attractions` so the saved HTML can render the airport metadata line.
- **`saveAttractionsFile()` payload destructure** — Accepts and passes `airportPostcode` / `airportDistanceKm` through to `_buildAttractionsHtml()`.
- **CSS** — Added `.iAGT-save-sep` (faint pipe divider between save buttons), `.iAGT-save-terminal-btn` (teal `#44CCAA` colour and border to distinguish from the blue flights button), and `.iAGT-save-terminal-btn:hover` rule.

### Fixed
- **`documents/MySavedFlight/` → `documents/MySavedFlights/`** — Corrected folder name in all documentation to match the actual folder name created by `saveFlightsFile()` in `node_helper.js`.

---

## [0.9.0] dev - 2026-03-12

### Added
- **Save City Attractions to file** — A 🖨 printer icon button appears in the city attractions panel header. Clicking it sends the currently displayed city's top-10 attraction list to `node_helper.js`, which generates a self-contained printable HTML file and saves it to `documents/MySavedCityAttractions/[city]_[YYYY-MM-DD-HHMM].html`. The button shows an hourglass ⏳ while saving, then ✓ (green) or ✗ (red) for 3 seconds before resetting.
- **Save Flight Details to file** — A 🖨 printer icon button appears in the flight data overlay panel title row. Clicking it saves all flight legs as a printable HTML file to `documents/MySavedFlight/flights_[YYYY-MM-DD-HHMM].html`. Legs are sorted by traveler name (Scenario 3) then ascending departure date/time, so multi-traveler printouts are grouped and chronologically ordered.
- **`iAGT_SAVE_OK` / `iAGT_SAVE_ERROR` socket notifications** — node_helper emits these after each save attempt so the frontend can update the button state without polling.
- **`saveAttractionsFile()` node_helper method** — Generates a styled HTML page listing all attraction items for the city (number, name, description columns) and writes it to `documents/MySavedCityAttractions/`.
- **`saveFlightsFile()` node_helper method** — Generates a styled HTML page listing all flight legs sorted by traveler and departure datetime, and writes it to `documents/MySavedFlight/`.
- **`_nhEsc()`, `_buildAttractionsHtml()`, `_buildFlightsHtml()` node_helper helpers** — Internal helpers for HTML generation and entity escaping used by the save handlers.

### Fixed
- **Airport tooltip flicker** — The ammap3 balloon `div` that appears on marker hover was intercepting mouse events, causing a `mouseout` → hide → reappear flicker loop. Fixed with a single CSS rule: `.amcharts-balloon-div { pointer-events: none !important; }`.

---

## [0.8.0] dev - 2026-03-12

### Added
- **Global Airport Database** — `data/airports.csv` is loaded at startup via `loadAirportsData()`. The new `resolveAirport()` helper resolves a bare IATA code string to full `{ name, iata, lat, lon }` automatically, so users no longer need to specify coordinates manually in `config.js` flight leg objects.
- **33-Language i18n Support** — `getTranslations()` expanded from 2 locales (English, German) to 33 languages: Afrikaans, Arabic, Czech, Welsh, Danish, Greek, Spanish, Persian, Finnish, French, Scottish Gaelic, Irish, Croatian, Haitian Creole, Hungarian, Italian, Japanese, Korean, Māori, Dutch, Norwegian, Polish, Portuguese, Romanian, Slovak, Slovenian, Serbian, Swedish, Turkish, Ukrainian, and Uzbek.
- **`departureAlertHours` config option** — Fires a `IAGT_DEPARTURE_ALERT` MagicMirror notification a configurable number of hours before the first scheduled departure, enabling integration with notification or speaker modules. Set to `0` (default) to disable.
- **`showPlaneShadow` config option** — Renders a semi-transparent white halo beneath the coloured plane icon, improving icon visibility against light map backgrounds (default: `true`).
- **`flightDisplayMode` config option** — Filters which legs appear on the map and in the overlay table: `"all"` (default), `"outbound"`, or `"return"`.
- **`colorPreviousPath` config option** — Colour for legs that have landed but are superseded by a subsequent active or landed leg (default: grey `#888888`). Such "previous" legs are now rendered visually dimmed rather than blending with the `colorCompletedPath`.
- **`colorCancelledPath` config option** — Dedicated colour for cancelled legs (default: red `#FF4444`).
- **`colorMapOcean` config option** — Explicit alias for `colorMapBackground` used as the chart ocean / background fill colour.
- **`lib/greatCircle.js`** — SLERP great-circle calculation extracted into a standalone browser-loadable script. `generateGreatCirclePoints()` now delegates to `iAGTGreatCircle.generateGreatCirclePoints()`, keeping the main module file leaner and enabling isolated unit testing of the geometry code.
- **`departureTime` field on leg objects** — Optional `"HH:MM"` string used as a secondary sort key (after `departureDate`) in both the test animation sequence and the flight table, enabling correct ordering of same-day multi-leg trips.
- **Plane nose look-ahead smoothing** — Bearing calculation now looks 2 great-circle steps ahead (previously 1) for a smoother nose orientation during animated flight near waypoints.
- **ETag / conditional-request caching** — `fetchFlightStatus()` sends `If-None-Match` with cached ETags; a `304 Not Modified` response refreshes the TTL without re-parsing, reducing AeroAPI response bandwidth.
- **`mapMigrationPlan.md`** — Detailed architectural migration plan from end-of-life `ammap3` to `@amcharts/amcharts5`, covering all surface-area replacements (line series, point series, GeoJSON format, antimeridian handling, zoom/viewport, tooltip API).

### Changed
- **`_buildTestSequence()`** — Test animation now sorts legs by `actualDeparture` timestamp when available, falling back to `departureDate + departureTime`, then `departureDate` alone, with `flightNumber` as a final tiebreak. Outbound legs always precede return legs when `flightDisplayMode: "auto"`.
- **`colorCountries` and `colorCountryBorders`** — Previously hardcoded values are now exposed as config options with documented defaults (`#2C3E50` and `#1A252F`).
- **`tripTitle` config option** — The subtitle appended to the header "We Are On Our Way To –" is now surfaced as a documented config key (default: `"Our Destination"`).

---

## [0.7.0] dev - 2026-03-10

### Added
- **AeroAPI Response Caching** — Implemented in-memory caching for flight status responses (1 min TTL for active flights, 5 min for others) to reduce API quota consumption.
- **Exponential Back-off** — Per-leg polling now uses capped exponential back-off (up to 5 mins) after failed API calls to prevent flooding during outages.
- **Accessibility Improvements** — Added ARIA roles and live regions (`role="status"`, `aria-live="polite"`, `role="region"`) for better screen reader support in countdown and overlay panels.
- **`colorBlindMode`** — New config option to differentiate map path status using `dashLength` (Scheduled: 8, Landed: 4, Active: 0) in addition to color.
- **`maxAttractionsDisplay`** — New config option to control the number of attractions shown per page (default: 5).
- **Security Guards** — Added a `MAX_BODY` (512KB) limit on API responses and `_safeColor` regex validation for CSS colors injected into inline styles.
- **Environment Variable Support** — `FLIGHTAWARE_API_KEY` can now be set as an environment variable, taking precedence over `config.js`.

### Changed
- **Font Size Scaling** — Replaced absolute pixel font sizes with a flexible `em`-based scale (0.8em to 2.0em) for all panel text-size modifier classes.
- **Panel Layout Stability** — Removed `!important` from width/height in CSS to allow `flightPanelWidth` and other config options to correctly override defaults.
- **Attractions Pagination** — Replaced binary toggle with a modulo-based page cycle for more robust handling of varying attraction counts.
- **Performance Optimization** — `_getFilteredLegs()` is now computed once per update cycle and passed to all child components, reducing redundant processing.

### Fixed
- **Infinite Recursion on Install** — Removed the `"install": "npm install"` lifecycle hook from `package.json` which caused infinite loops in some environments.
- **Incorrect Panel Height** — Corrected `100vh` height on the flight status table overlay to `32vh`.
- **Global Config Fallback** — Removed unreliable access to MagicMirror's global config object; the module now provides clear error logs if the API key is missing.

---

## [0.6.0] dev - 2026-03-09

### Added
- **Attractions page-flip auto-scroll** — when `attractionsAutoScroll: true`, the attractions panel now shows rows 1–5 for `attractionsScrollInterval` seconds, then rows 6–10 for the same duration, looping continuously while the destination is active. Replaces the previous per-row scroll approach.
- **Traveller name cell background colour (Scenario 3)** — the coloured dot/icon previously shown to the left of each traveller's name in the Flight Data overlay has been replaced by a coloured background fill on the entire Name cell. The colour matches that traveller's plane icon colour and is readable with dark text. No new config option required; uses the same per-traveller colour assignment.
- **`setFlightDetailsTextSize` and `setAttractionsDetailsTextSize` now active** — these config options were previously defined but never wired to the DOM. They now correctly apply the corresponding `iAGT-fs-*` / `iAGT-atts-*` CSS size class to each panel wrapper.

### Changed
- **Flight overlay panel width** — default `flightPanelWidth` reduced from `40vw` to `46vw` to accommodate content on a single row; further reduced to account for removal of the dot column.
- **Attractions overlay panel width** — default `attractionsPanelWidth` set to `48vw`.
- **Panel font sizes** — both overlay panels scaled to approximately 33% smaller than previous defaults via the `iAGT-fs-*` and `iAGT-atts-*` CSS classes. Vertical row padding also reduced to minimise whitespace between rows.
- **Colour key legend removed** — the traveller name / symbol strip that appeared beneath the "Upcoming Flight Status" header in the Flight Data overlay has been removed. Traveller identification is now solely via the coloured Name cell background.

### Fixed
- **Flight progress % stuck at 1% in overlay panel (test mode)** — in `showFlightTracks: "test"` mode, `updateTable()` was only called when flight status changed (e.g., `scheduled → active`), so the progress percentage in the Status column was frozen at the value captured at the moment the leg became active (≈1%). The table is now also rebuilt every 30 animation frames (~1 second) during the flying phase, keeping the overlay panel in sync with the countdown box.
- **CSS width and font-size overrides ignored** — the JS module was setting `style.width` on both overlay panels via the `flightPanelWidth` / `attractionsPanelWidth` config defaults (`"40vw"`), silently overriding CSS. Fixed by aligning JS defaults to match the CSS values. Similarly, both panels were hardcoded to `iAGT-fs-xsmall` / `iAGT-atts-xsmall` class names regardless of config; they now correctly read from `setFlightDetailsTextSize` and `setAttractionsDetailsTextSize`.

---

## [0.5.0] dev - 2026-03-05

### Added
- **Resilient Map Initialization** — `AmCharts.makeChart()` is now wrapped in a `try/catch` block. On initialization failure (e.g., missing dependencies or browser issues), a user-friendly error message is rendered directly in the map container instead of a silent failure.
- **Improved Attractions HTML Helper** — `_buildAttractionsHTML(things)` centralized helper for generating attraction lists. Ensures consistent HTML structure, proper character escaping (preventing XSS), and "No attractions found" messaging across all UI entry points (cycling and landing auto-rotation).

### Changed
- **Async Data Loading** — `node_helper.js` now uses non-blocking asynchronous file operations (`fs.promises.readFile`) for loading `cities.csv` and per-city attractions JSON files. This prevents the MagicMirror process from hanging during large IO operations at startup.
- **Parallel File Processing** — Per-city attraction files for all destinations are now loaded in parallel using `Promise.all()` during the initial scenario processing phase, significantly reducing startup time for complex multi-leg trips.

### Performance
- **Optimized Bearing Calculations** — Verified that plane bearing (nose orientation) uses cached great-circle points rather than re-calculating the spherical interpolation for every animation frame, reducing CPU overhead during live flight tracking.

---

## [0.4.0] dev - 2026-03-04

### Added
- **`tooltipDuration` config option** — controls how long a map destination tooltip remains visible after the mouse leaves (default `6` seconds). Eliminates previous flickering caused by the tooltip pointer triggering mouse-enter/leave events
- **Custom JavaScript scrollbar** — both the Flight Data overlay and Attractions overlay now render a fully visible DIV-based scrollbar track and draggable thumb. Supports mouse-wheel scroll, click-to-jump, and drag-to-scroll. This replaces the previous approach of trying to override MagicMirror's global `::-webkit-scrollbar { display: none }` CSS rule, which Electron/Chromium enforces at the compositor level and cannot be overridden per-element

### Changed
- **Flight table sort order** overhauled:
  - **In-flight** (`active`) legs always float to the **top** of the list
  - **Scheduled / cancelled** legs fill the middle, sorted ascending by departure time
  - **Landed** legs sink to the **bottom** of the list
  - **Auto-hide**: a landed leg is removed from the table once the next leg in the same trip (or per-traveler trip in Scenario 3) transitions to `active` or `landed`, keeping the table focused on current and upcoming flights only. The final leg of any trip always remains visible after landing

### Fixed
- Overlay panel scrollbars were invisible in both the Flight Data and Attractions panels due to MagicMirror's global Electron/Chromium scrollbar suppression; resolved with a custom JS-driven scrollbar implementation
- Map tooltip flickered and disappeared immediately on hover; resolved via `pointerWidth: 0` on the ammap3 balloon config and the new `tooltipDuration` fade-out setting

---

## [0.3.0] dev - 2026-03-04

### Added
- **HowThisModuleWorks.md** — comprehensive architectural overview explaining core features, backend logic, and configuration mapping
- **Enhanced Configuration Documentation** — updated README with preferred configuration keys (`showFlightDetails`, `showAttractionsDetails`) while maintaining backward compatibility

### Changed
- Standardised documentation structure

---

## [0.2.0] dev 2026-03-03

### Added
- **Global airport & city database** — expanded from 15 World Cup cities to **431 cities across all 193 UN member states** with commercial air service
- **430 attractions JSON files** — every city now has a curated Top 10 things-to-do file (`data/attractions/*.json`)
- **`documents/airports_organized.csv`** — machine-readable airport reference file (428 rows, 7 columns: name, IATA, lat, lon, country, city, postcode/zip)

#### New cities by region (this release)

**United Kingdom & Ireland** (20 airports): All major UK regional airports plus Belfast City, London City

**Western Europe** (60+ cities): Full coverage of France, Germany, Spain, Italy, Netherlands, Belgium, Switzerland, Austria, Portugal, Luxembourg, Malta, Cyprus, Iceland

**Northern Europe** (10 cities): Denmark, Sweden, Norway, Finland, Latvia, Lithuania, Estonia

**Eastern Europe** (10 cities): Poland, Czech Republic, Hungary, Slovakia, Romania, Bulgaria, Ukraine (4 cities), Belarus, Moldova

**Balkans & Caucasus** (18 cities): Croatia, Bosnia, Serbia, Montenegro, Kosovo, North Macedonia, Albania, Greece, Georgia, Armenia, Azerbaijan

**Russia & Central Asia** (12 cities): Russia (Moscow, St Petersburg, Sochi, Yekaterinburg, Novosibirsk), Kazakhstan, Uzbekistan (2), Kyrgyzstan, Tajikistan, Turkmenistan, Mongolia

**Middle East** (21 cities): Turkey, Israel, Jordan, Lebanon, Syria (Damascus), Iraq (3), Iran (5), Saudi Arabia (4), UAE, Qatar, Kuwait, Bahrain, Oman (2), Yemen (Sana'a)

**South Asia** (23 cities): India (12), Pakistan (3), Bangladesh (2), Sri Lanka, Nepal, Bhutan, Maldives, Afghanistan (Kabul)

**East Asia** (22 cities): China (19 including Zhengzhou, Changsha, Nanning), Japan, South Korea (3), North Korea (Pyongyang)

**Southeast Asia** (30 cities): Myanmar (2), Thailand (5), Vietnam (4), Cambodia (2), Laos (2), Indonesia (7 including Mataram, Medan), Malaysia (5), Philippines (5), Singapore, Brunei, Timor-Leste

**Australia & New Zealand** (15 cities): Australia (9), New Zealand (5), Fiji (2)

**Oceania** (12 cities): Papua New Guinea (2), Solomon Islands, Vanuatu, Samoa, Tonga, Tuvalu, Kiribati, Nauru, Marshall Islands, Palau, Micronesia

**North Africa** (13 cities): Morocco (6), Algeria (3 incl. Oran, Constantine), Tunisia (3 incl. Djerba, Monastir), Libya (Tripoli), Egypt

**West Africa** (20 cities): Nigeria (4 incl. Port Harcourt), Ghana (2 incl. Kumasi), Senegal, Ivory Coast, Mali, Burkina Faso, Benin, Togo, Guinea, Sierra Leone, Liberia, Gambia (Banjul), Guinea-Bissau (Bissau), Mauritania (Nouakchott), Cape Verde (2), Niger

**Central Africa** (8 cities): Cameroon (2 incl. Yaounde), DR Congo, Republic of Congo (Brazzaville), Gabon, Equatorial Guinea (Malabo), São Tomé & Príncipe, Central African Republic (Bangui), Chad (N'Djamena)

**East Africa** (14 cities): Ethiopia, Kenya (2), Tanzania (3), Uganda, Rwanda, Burundi (Bujumbura), Djibouti, Eritrea, Somalia, South Sudan (Juba), Sudan, Comoros (Moroni)

**Southern Africa** (14 cities): South Africa (3 incl. Cape Town, Durban), Zimbabwe (2), Zambia, Namibia, Botswana, Mozambique, Malawi (Lilongwe), Madagascar, Mauritius, Seychelles, Lesotho (Maseru), Eswatini (Manzini), Angola

**Caribbean** (22 cities): Cuba (2), Dominican Republic (2), Jamaica (2), Trinidad & Tobago, Barbados, Bahamas, Haiti, Grenada (St George's), Saint Lucia (Castries), Dominica (Roseau), Antigua & Barbuda (St John's), Saint Vincent (Kingstown), Saint Kitts & Nevis (Basseterre)

**Central America** (7 cities): Costa Rica, Panama, Guatemala, Honduras (2), El Salvador, Nicaragua, Belize

**South America** (22 cities): Brazil (2), Argentina, Colombia (5), Peru (3), Chile (2), Bolivia (2), Ecuador (2), Venezuela (2), Paraguay, Uruguay, Guyana, Suriname

### Changed
- `tests/test.js` — count assertions updated to `>= 15` / dynamic to support any number of cities
- `README.md` — "World Cup 2026 Cities" section replaced with full global coverage table

---

## [0.1.0] dev 26-02-28

### Added
- Initial release forked from MMM-iHaveBeenThere v1.1.0
- **Scenario 1**: Standard round-trip flight tracking
- **Scenario 2**: Multi-leg Round The World trip support (up to 10+ legs)
- **Scenario 3**: Multi-origin trips to single destination. e.g.  (World Cup fans, wedding guests, etc.)
- SLERP-based great-circle path generation for accurate flight arc rendering
- Colour-coded flight paths:
  - White  = Scheduled / future
  - Blue   = In Flight (progressive from origin)
  - Green  = Landed / complete
  - Auto-reset to white after configurable number of days
- Live plane position marker during active flights
- **FlightAware AeroAPI v4** integration for real-time flight tracking. Uses free API.
- Configurable poll interval (default 5 minutes)
- **Countdown box** showing days until first departure
- **Overlay flight table** (6 columns: Name, Flight No, Date, Dep, Arr, Status)
  - Freely positionable via tableX / tableY config
- **City information panel** — Top 10 things to do per destination
- **15 World Cup 2026 host cities** pre-loaded with attraction data:
  - 10 USA cities, 2 Canadian cities, 3 Mexican cities
- English and German translations
- Full configuration documentation

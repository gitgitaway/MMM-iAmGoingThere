# How MMM-iAmGoingThere Works

This document provides a technical overview of how each main feature functions and the configuration options available to control them.

---

## 1. Six Trip Scenarios

The module is designed around six distinct travel scenarios, controlled by the `scenario` configuration option.

### **Scenario 1 — Standard Round Trip**
- **Function**: Designed for a simple trip from home to a destination and back.
- **Data Structure**: Uses the `flights` array. Expects exactly two legs (outbound and return).
- **Config Option**: `scenario: 1`

### **Scenario 2 — Multi-Leg / Round The World**
- **Function**: Designed for complex, sequential travel involving multiple stopovers before returning home.
- **Data Structure**: Uses the `flights` array. Supports an unlimited number of legs (typically up to 10+).
- **Config Option**: `scenario: 2`

### **Scenario 3 — Multi-Origin Group Event**
- **Function**: Designed for group events (e.g., World Cup, weddings) where multiple people fly from different locations to a shared destination.
- **Data Structure**: Uses the `travelers` array. Each traveler has their own `flights` (outbound) and `returnFlights` arrays.
- **Visuals**:
    - **Flight Paths**: Use standard colors (White/Blue/Green) for all travelers to maintain map clarity.
    - **Plane Icons**: Each traveler is assigned a unique color for their live plane icon. Multiple planes are rendered if multiple travelers are in flight simultaneously.
    - **Flight Table**: The Name cell for each traveler row is filled with a solid background in that traveler's assigned colour (matching their plane icon), with dark text for legibility. The aircraft symbol (✈) and progress percentage in the Status column are also color-coded during active flights.
- **Config Option**: `scenario: 3`

### **Scenario 4 — Where I Have Been**
- **Function**: Designed for visualising past travel history. Places a permanent marker for every destination that has been visited.
- **Data Structure**: Uses the `flights` array. Each entry requires only a `to` field and an optional `departureDate`. No `from`, `flightNumber`, or API key is needed.
- **Destination Resolution** — The `to` field is resolved through the following lookup chain (first match wins):
    1. **IATA code** (e.g. `"LHR"`) — resolved from `data/airports.csv`
    2. **City name** (e.g. `"San Francisco"`) — resolved from `data/cities.csv`
    3. **Football team name** (e.g. `"Bayern Munich"`) — resolved from `data/football_teams_database.csv` using the team's stadium coordinates
    4. **United Kingdom Regions** — "England", "Scotland", "Wales", and "Northern Ireland" are automatically resolved to **GB**.
    5. **Direct coordinates** — an object with `{ lat, lon }` fields used as-is
- **Map Markers**:
    - **Home** — rendered with a **Gold** (`#FFD700`) target marker.
    - **Destinations** — rendered with a **White** target marker by default.
    - **Football Team Crests** — when a destination is resolved via a team name and a crest image exists in `images/crests/[Country]/`, the white marker is replaced by an `am5.Picture` sprite rendering the official crest PNG/SVG. Country folder names use underscores in place of spaces (e.g. `The_Netherlands/`).
- **Crest Stability** — `updateMapLines()` computes a fingerprint string of all airport coordinates, crest paths, and colours on every call. The `_airportSeries.data.setAll()` call (which destroys and recreates all `am5.Picture` sprites) is only executed when the fingerprint changes. During test animation, where only plane positions change, the airport series is untouched, so crest images remain perfectly stable.
- **`showWhereIHaveBeen`** — When `true`, the module generates synthetic round-trip legs (Home → Destination → Home) for every `flights` entry so that the test animation plays them in order.
- **Flight Tracks** — Tracks are **only visible when `showFlightTracks: "test"`**. In normal display mode the map shows only the static markers.
- **No API Polling** — `pollAllFlights()` returns immediately for Scenario 4. No FlightAware API key is required.
- **Config Option**: `scenario: 4`

### **Scenario 5 — Aircrew / Frequent Flyer CSV Roster**
- **Function**: Designed for aircrew or frequent flyers whose schedule changes frequently. Reads legs from a plain CSV file.
- **Data Structure**: Reads from a CSV file (`data/my_flights.csv` by default).
- **Key Feature**: Schedule changes take effect on MagicMirror restart without modifying `config.js`. Full FlightAware live tracking is supported.
- **Config Option**: `crewFlightsFile` — path to the CSV file (relative to module directory).
- **Config Option**: `scenario: 5`

### **Scenario 6 — Football Away Days**
- **Function**: Designed for tracking European football away fixtures. Automatically resolves stadium locations from a comprehensive team database.
- **Data Structure**: Reads from `data/footballAwayTrips.csv`. Required columns are `departureDate` and `to`. Optional columns include `Competition`, `Score`, `Result`, and `flightNumber`.
- **Stadium Resolution**:
    - Uses `data/football_teams_database.csv` (500+ teams) for exact/fuzzy name matching.
    - Accents are normalized (e.g., ø → o) during matching to ensure matches for teams like "Bodø/Glimt".
    - Resolved coordinates are used to place markers directly on the stadium location.
- **Marker Rendering**:
    - Uses a visible **17x17px Container** with a dark circle background (`#1a1a2e`) and blue border.
    - Official club crest PNGs are rendered as a `Picture` sprite on top.
    - If a crest image is missing, the visible background circle remains, ensuring no "invisible" markers.
- **Tooltip Aggregation**: Multiple visits to the same stadium are automatically grouped into a single rich tooltip showing the full fixture history (Date, Opponent, Competition, Score, Result).
- **Config Option**: `scenario: 6`

---

## 2. Map Enhancement Layers (v2.0.0+)

### **Graticule Grid**
- **Function**: Adds a reference grid of latitude and longitude lines to the map.
- **Implementation**: Lines are generated in `MMM-iAmGoingThere.js` using GeoJSON `LineString` features. Coordinates are sampled every 2 degrees to ensure smooth curves even on high-distortion projections like Orthographic (Globe).
- **Technique**: Uses the `data.setAll()` pattern rather than the `geoJSON` constructor property to ensure that template adapters (for color/opacity/width) are correctly applied to every line in the series.
- **Config Option**: `showGraticule`, `graticuleStep`, `graticuleWidth`.

### **Sub-national Region Layers**
- **Function**: Displays detailed boundaries for states, provinces, cantons, and departments within specified countries.
- **Implementation**: 
    1. `node_helper.js` maintains a `_REGION_FILE_MAP` for **130+ countries**.
    2. When `showSubnationalRegions` is enabled, the backend reads the corresponding ES-module GeoJSON files from `@amcharts/amcharts5-geodata`.
    3. The files are parsed into JSON (removing ES `export` syntax) and sent to the frontend.
    4. The frontend creates a separate `MapPolygonSeries` for each country layer, applying a rotating 8-color palette (`LAYER_COLORS`) to ensure neighboring layers are visually distinct. Created series are stored in `this._regionSeriesList`.
- **On-screen Toggling**: Regions can be toggled on/off without a restart via the **Highlights** dropdown in the top-left corner. This calls `_toggleRegionLayers(visible)`.
- **UK Support**: Includes high-detail mapping for England, Scotland, Wales, and Northern Ireland.
- **Config Option**: `showSubnationalRegions`, `subnationalAllCountries`, `subnationalCountries`.

#### **Globe Auto-Rotation**
- **Function**: Automatically rotates the map to keep the active flight's plane icon centered.
- **Implementation**: When `autoRotateGlobeToPlane` is enabled and the projection is `orthographic`, the module calculates the average latitude and longitude of all active planes during the `_flushMapLines` phase. It then uses `mapChart.animate()` to smoothly rotate the globe to those coordinates.
- **Config Option**: `autoRotateGlobeToPlane`.

---

## 3. Live Flight Tracking (FlightAware AeroAPI)

The module integrates with the **FlightAware AeroAPI v4** to provide real-time updates.

- **Backend Polling**: `node_helper.js` handles all API requests.
- **Async Data Loading**: `node_helper.js` uses non-blocking asynchronous file operations (`fs.promises.readFile`) for loading `cities.csv`, `airports.csv`, and per-city attractions JSON files. This prevents the MagicMirror process from hanging during large IO operations at startup.
- **Parallel processing**: Per-city attraction files for all destinations are loaded in parallel using `Promise.all()` during the initial scenario processing phase, significantly reducing startup time for complex multi-leg trips.
- **Quota Conservation**: Polling for a specific flight only begins **24 hours before** its scheduled departure.
- **Update Frequency**: Controlled by `pollInterval` (default: 5 minutes).
- **Required Config**: `flightAwareApiKey` must be set for live tracking to function.
- **Environment Variable**: You can also set `FLIGHTAWARE_API_KEY` as an environment variable, which takes precedence over the config value.

### **Rich Live Status & Telemetry (v1.7.0+)**

Beyond basic status, the module captures and displays rich inflight telemetry:
- **Plane Tooltip**: Shows `Alt` (altitude), `Spd` (groundspeed), `Hdg` (heading), and `Rate` (▲ Climb / ▼ Desc / → Level).
- **Flight Table Chip**: Active flights display a 📡 telemetry chip with altitude, speed, heading, and vertical rate.
- **Heading & Altitude Change**: Extracted from AeroAPI `last_position.heading` and `last_position.altitude_change`.
- **Plane Position Tweening**: Plane icons smoothly animate between positions using a 1-second linear tween (`dataItem.animate()`).

### **Master Configuration Logic (v1.8.0+)**
- **Function**: Allows users to define multiple scenarios within a single module block using the `scenarios` object.
- **Data Merging**: When a scenario is selected (either via `config.scenario` at startup or the on-screen selector), the module uses `_getEffectiveConfig()` to merge the top-level global configuration with the scenario-specific configuration. Fields in the `scenarios[id]` object always take precedence over global fields.
- **Dynamic Re-initialization**: When the scenario is changed on-screen:
    1. The frontend notifies the `node_helper.js` via `UPDATE_SCENARIO`.
    2. The `node_helper.js` re-processes the flight data for the new scenario and sends `iAGT_INIT` back.
    3. The frontend `socketNotificationReceived` catches `iAGT_INIT`, calls `this._mapRoot.dispose()` to clean up the existing WebGL context, and re-runs the entire map initialization pipeline (`initMap()`) with the new configuration.
- **Config Option**: `scenarios: { "1": { ... }, "2": { ... } }`

### **Interactive UI Controls & Navigation (v1.8.0+)**

The module now features a suite of on-screen controls for manual map interaction:
- **Pan Control**: A directional pad (N, S, E, W) in the bottom-left allows fine-grained map panning in **0.5-degree steps**.
- **Zoom Control**: Standard `+` and `-` buttons in the bottom-right for manual zoom (**0.1 increments**).
- **Traditional Compass**: The center of the pan control is a functional **magnetic needle**. It rotates in real-time to always point North based on the map's current `rotationX`.
- **Recenter Behavior**: Clicking the compass needle re-orients the map to North (0,0 rotation) while preserving the user's current zoom level.
- **On-Screen Selectors**:
    - **Map Projection Selector** (Top-Left): Instantly switches between Mercator, Globe, etc., by calling `_updateProjection()`.
    - **Highlights Control** (Top-Left): Toggles visited country highlights and sub-national region visibility (`Show/Hide Sub Regions`).
    - **Scenario Selector** (Top-Right): Switches the active trip scenario (1-6). Changing the scenario triggers the dynamic re-initialization pipeline described above.

### **Responsive & Modern UI**
- **Glassmorphism Design**: All UI controls use a modern glassmorphism aesthetic with background-blur and semi-transparent borders.
- **Responsive Narrow Layout**: Triggered by `narrowBreakpoint` (default `900px`). Stacks overlay panels and increases width to `95vw` on smaller displays.
- **Hourly Weather Refresh**: Destination weather is re-fetched every hour from Open-Meteo.
- **Debounced Rendering**: `updateMapLines()` uses a 250ms debounce to prevent redundant map redraws during rapid data updates or animations.
- **Visibility Configuration**: Every UI element (Pan, Zoom, Map Selector, Scenario Selector) can be individually toggled via `showPanControl`, `showZoomControl`, etc., in the module configuration.

### **Interactive Country Mapping (v1.8.0+)**

The module supports both automated and manual country mapping, primarily for Scenario 4 ("Where I Have Been"):
- **Automatic Highlighting**: Countries visited in your flight history are automatically colored using `colorVisitedCountry`. The module resolves the country for every leg by looking up the destination city or stadium in the internal databases (`cities.csv` and `football_stadiums.csv`).
- **Manual Toggle (Right-Click)**: You can manually mark any country as "visited" by **right-clicking** its polygon on the map. This toggles the color between the default and the visited color.
- **Persistent Cache**: Manual selections are immediately saved to `data/manual_visited_countries.json`. This cache is reloaded every time the module starts, ensuring your manual changes are preserved across restarts.
- **Conflict Resolution**: Manual overrides take precedence over automatic detection.

### **Airport Database & IATA-Only Config**
At startup `node_helper.js` loads `data/airports.csv`, a built-in database of 300+ global airports (IATA code, name, latitude, longitude). The `resolveAirport()` helper is then available to resolve any airport reference:
- **String** (e.g. `"LHR"`) — resolved directly from the database; no coordinates required in `config.js`.
- **Object with `lat`/`lon`** — used as-is; database is not consulted.
- **Object with `iata` only** — coordinates are pulled from the database and merged.

This means flight legs can be written as compactly as `from: "LHR"` rather than providing the full `{ name, iata, lat, lon }` object.

### **Robust Polling & Caching**
The module implements several layers of stability for API communication:
- **In-Memory Caching**: Responses from AeroAPI are cached per-flight to reduce redundant calls. Active flights use a **1-minute TTL**, while scheduled/landed flights use a **5-minute TTL**.
- **ETag / Conditional Requests**: `fetchFlightStatus()` stores the `ETag` header returned by AeroAPI and sends it back as `If-None-Match` on subsequent requests. A `304 Not Modified` response refreshes the cache TTL without re-parsing the body, further reducing bandwidth consumption.
- **Exponential Back-off**: If an API call fails, the module increments a `_failCount` for that specific leg and implements a capped exponential back-off (doubling each time, max 5 minutes). This prevents flooding the API during service outages.
- **Response Size Guard**: To protect system memory, the module enforces a **512 KB limit** (`MAX_BODY`) on API responses. If a response exceeds this, the connection is immediately destroyed.

### Related Config Options:
- **`flightAwareApiKey`**: Your AeroAPI v4 key.
- **`pollInterval`**: Minutes between API calls.

---

## 2a. Live Flight Status Data (v1.2.0+)

When live tracking is active, the module surfaces a rich set of AeroAPI fields beyond the basic status/progress. All data is extracted in `updateLegFromAPI()` in `node_helper.js` from the same API response — no additional API calls are made.

### **Detailed Status Labels**

`leg.detailedStatus` holds the raw AeroAPI `status` string (e.g. `"Taxiing"`, `"En Route"`, `"Arrived"`, `"Diverted"`). The flight table in `buildTableHTML()` maps this to display labels:

| AeroAPI `status` contains | Display label |
|--------------------------|---------------|
| `"taxiing"` | `Taxiing ✈` |
| `"diverted"` | `Diverted ⚠` |
| `"en route"` / `"active"` | `In Flight ✈ N%` |
| `"landed"` / `"arrived"` | `Landed ✓` |
| `"cancelled"` | `Cancelled ✗` |
| `"scheduled"` | `Scheduled` |

### **Gate & Terminal Information**

Extracted from `terminal_origin`, `terminal_destination`, `gate_origin`, and `gate_destination` in the AeroAPI flight object. Stored as `leg.departureTerminal`, `leg.departureGate`, `leg.arrivalTerminal`, `leg.arrivalGate`. When present, rendered in the detail chip sub-row as:

```
T:2 G:B34 → T:5 G:A12
```

### **Detail Chips Sub-Row**

When any AeroAPI data is available, a second row (`.iAGT-details-row`) is rendered directly beneath each flight row in the table. It contains up to three monospace `.iAGT-detail-chip` elements:

1. **Aircraft chip** — `✈ B77W (G-STBA)` (aircraft type + tail number)
2. **Terminal/gate chip** — `T:2 G:B34 → T:5 G:A12` (departure → arrival)
3. **Time chip** — `ETD: 14:30  ETA⚡: 17:45` (estimated departure and arrival; `⚡` suffix when Foresight-sourced)

Chips are only rendered when the relevant data fields are non-null.

### **Time Data**

| Leg field | Source AeroAPI field | Meaning |
|-----------|---------------------|---------|
| `scheduledDeparture` | `scheduled_out` / `scheduled_off` | Published scheduled departure |
| `estimatedDeparture` | `estimated_out` / `actual_out` | Current estimated or actual departure |
| `scheduledArrival` | `scheduled_in` / `scheduled_on` | Published scheduled arrival |
| `estimatedArrival` | `estimated_in` / `scheduled_in` | Current best arrival estimate |
| `foresightEta` | `predicted_in` (when `foresight_predictions_available`) | FlightAware AI-predicted arrival |

When `foresightEta` is present, it takes priority over `estimatedArrival` in the ETA chip and the label changes to `ETA⚡`.

### **Live Tracking Tooltip**

When the plane SVG is rendered in `buildAirportMarkers()`, the amCharts 5 bullet's `tooltipText` is set to a multi-line string assembled from:

- Flight number
- `detailedStatus`
- `currentLat` / `currentLon` (° formatted to 3 d.p.)
- `groundspeed` (kts) — from `last_position.groundspeed`
- `altitude` (ft) — from `last_position.altitude × 100`
- `lastPositionUpdate` — formatted to `HH:MM` local time
- `aircraftType` + `tailNumber`

Hovering the plane icon on the map displays this information in the amCharts 5 tooltip bubble.

### **Aircraft Data**

| Leg field | Source AeroAPI field |
|-----------|---------------------|
| `aircraftType` | `aircraft_type` (e.g. `"B77W"`) |
| `tailNumber` | `registration` / `tail_number` |

### **Security Note**

All AeroAPI strings inserted into `innerHTML` are passed through `this._esc()` (the module's HTML-escaping helper) before rendering. This applies to `aircraftType`, `tailNumber`, `departureTerminal`, `arrivalTerminal`, `departureGate`, and `arrivalGate`.

---

## 3. Flight Path Rendering and Color Logic

Flight paths are rendered as **great-circle arcs** using SLERP (Spherical Linear Interpolation) for accurate global curvature. The SLERP math lives in `lib/greatCircle.js` — a standalone browser-loadable script — keeping the main module file lean and enabling independent unit testing of the geometry code.

- **Optimized Bearing Calculations**: The plane's nose orientation (bearing) uses pre-computed great-circle points rather than re-calculating the spherical interpolation for every animation frame. The look-ahead is **2 steps** along the great-circle arc for a smooth, accurate heading near waypoints.

### **Path Colors & Styles**
Paths change color and style dynamically based on flight status:
- ⬜ **Dotted White** (`colorFuturePath`): Scheduled or future legs.
- 🔵 **Solid Blue** (`colorActivePath`): Currently in the air. The arc "fills" progressively from the origin to the destination based on the `progress_percent` reported by the API.
- 🟢 **Solid Green** (`colorCompletedPath`): Flight has landed.
- 🔘 **Dimmed Grey** (`colorPreviousPath`): A leg that has landed but is **superseded** by a subsequent active or landed leg in the same trip (i.e. it is no longer the most recent completed leg). This keeps earlier legs visually subordinate to the current or most recent flight.
- 🔴 **Solid Red** (`colorCancelledPath`): Flight was cancelled.

### **Flight Display Mode**
`flightDisplayMode` filters which legs are rendered on the map and in the overlay table:
- `"all"` (default) — every leg regardless of type
- `"outbound"` — only outbound legs
- `"return"` — only return legs

This is useful for modules embedded in a shared display where you want to show only the outbound journey while traveling.

### **Accessibility — Colorblind Mode**
When `colorBlindMode: true`, the module uses the `dashLength` property to differentiate flight status in addition to color:
- **Scheduled/Cancelled**: `dashLength: 8` (long dashes)
- **Landed/Completed**: `dashLength: 4` (short dashes)
- **Active**: `dashLength: 0` (solid line)
This ensures users can distinguish flight status without relying on color perception.

### **Trip Completion & Reset**
Once all legs are completed, the module waits for `colorResetAfterDays` (default: 1 day) before resetting all paths to white. This indicates the trip is over and prevents the map from staying "green" indefinitely.

### Related Config Options:
- **`colorFuturePath`**, **`colorActivePath`**, **`colorCompletedPath`**, **`colorPreviousPath`**, **`colorCancelledPath`**.
- **`flightDisplayMode`**: Filter which legs are shown (`"all"` | `"outbound"` | `"return"`).
- **`colorResetAfterDays`**: Days to wait before resetting the map.
- **`gcPoints`**: Number of interpolation points (higher = smoother arcs).

---

## 4. Map Visuals and Animations

The module uses **amCharts 5** for rendering the high-performance interactive world map.

- **Local Map Engine**: All core libraries (`index.js`, `map.js`, `worldLow.js`) are bundled in the `vendor/` directory, ensuring stability and removing dependency on external CDNs.
### **Map Projections (v1.7.0+)**
The module supports multiple map projections via the `mapProjection` config option:
- **Mercator** (default): Best for high-latitude transatlantic flights; paths curve visibly over the poles.
- **Natural Earth 1**: A balanced world view.
- **Orthographic**: The "3D Globe" look.
- **Stereographic** & **Equirectangular** also supported.
See the [Map Projections User Guide](./mapProjections-User-Guide.md) for full details.

- **GeoJSON Rendering**: Flight paths are generated as native GeoJSON `LineString` features.
- **Resilient Initialization**: Map setup is wrapped in a `try/catch` block with a retry mechanism to ensure `am5` globals are fully defined before rendering.
- **Plane Icon**: A live plane icon is positioned at the aircraft's current latitude and longitude during active flights.
- **Plane Shadow**: When `showPlaneShadow: true` (default), a semi-transparent white halo is rendered beneath the coloured plane icon, improving visibility against light-coloured map backgrounds.
- **Airport Markers**: Distinct markers for the home airport (`colorAirportHome`) and all other destinations (`colorAirportOther`). Can be toggled via `showDestinations`. When a destination is resolved from a football team name, the marker is replaced by an `am5.Picture` rendering the team's official crest image.
- **Airport Series Fingerprinting**: `updateMapLines()` builds a fingerprint string from each airport's coordinates, crest path, and colour on every call. `_airportSeries.data.setAll()` — which destroys and recreates all bullet sprites — is only invoked when the fingerprint has changed since the last render. The plane series (`_planeSeries`) is always updated regardless, since aircraft positions change every frame. This prevents `am5.Picture` crest sprites from being recreated on every animation tick, eliminating the crest image flicker that would otherwise occur during test animation.
- **Test Mode**: If `showFlightTracks: "test"` is set, the module runs a continuous animation of all flight legs.

### Viewport — Zoom & Centering

amCharts 5 uses **globe rotation** to centre the NaturalEarth projection. This is different from a simple pan offset — the underlying globe is rotated so that the chosen coordinate appears at the centre of the viewport.

The three config values are translated to amCharts 5 properties as follows:

| Config option | amCharts 5 property | Value formula |
|---------------|---------------------|---------------|
| `zoomLongitude` | `rotationX` | `rotationX = -zoomLongitude` |
| `zoomLatitude` | `rotationY` | `rotationY = -zoomLatitude` |
| `zoomLevel` | `zoomLevel` | direct |

All three are set directly in the `MapChart.new()` constructor, so the very first rendered frame is already at the correct position. A `frameended` handler calls `chart.setAll()` as a secondary assertion to prevent any deferred resize recalculation from resetting them.

`panX: "rotateX"` and `panY: "rotateY"` are enabled on the chart to allow rotation-based centering to function — this does not enable user drag panning; it only unlocks the internal rotation mechanism used for programmatic centering.

**Presets:**

```js
// Full world
zoomLevel: 1, zoomLongitude: 0, zoomLatitude: 20

// Europe + North America (mid-Atlantic centre)
zoomLevel: 2.2, zoomLongitude: -30, zoomLatitude: 30

// Europe focus
zoomLevel: 3, zoomLongitude: 10, zoomLatitude: 52

// North America focus
zoomLevel: 2.5, zoomLongitude: -95, zoomLatitude: 40

// Asia-Pacific
zoomLevel: 2, zoomLongitude: 130, zoomLatitude: 25
```

### Related Config Options:
- **`zoomLevel`**: amCharts 5 zoom level (`1` = full world, `2` = 2× zoom, etc.).
- **`zoomLongitude`**: Longitude of the map centre (negative = West).
- **`zoomLatitude`**: Latitude of the map centre (negative = South).
- **`animationEnabled`**: Toggle the plane icon animation.
- **`showPlaneShadow`**: Renders a white shadow beneath the plane for better visibility (default `true`).
- **`showDestinations`**: Toggle airport destination markers (default `true`).
- **`showFlightTracks`**: Set to `"auto"` (default) for live tracking or `"test"` for demo mode.
- **`testModeDuration`**: Seconds per leg in test animation (default `12`).
- **`testModeDelay`**: Seconds pause between legs in test animation (default `2`).
- **`tooltipDuration`**: Seconds the airport/destination tooltip remains visible after the cursor leaves (default `8`).

---

## 5. Overlay Panels

The module includes two positionable overlay panels that sit at the **absolute bottom of the screen display** (bottom-left and bottom-right). Both panels contain a custom JavaScript-driven scrollbar that works independently of MagicMirror's global scrollbar suppression.

Both panels share a **unified design system** with identical header styling, high-contrast white text, and gold-coloured highlight keys.

To ensure compatibility with screen readers, both panels include ARIA accessibility roles (`role="region"` for flights, `role="complementary"` for attractions, and `role="status"` for the countdown box).

### **Flight Status Table**
- **Function**: Shows a 6-column table (Name · Flight No · Date · Departure · Arrival · Status) with live status and in-flight progress percentage.
- **Positioning**: Automatically pinned to the **bottom-left** of the screen wrapper.
- **Panel size**: `flightPanelWidth` (default `"46vw"`) and `flightPanelHeight` (default `"32vh"`).
- **Font size**: Controlled by `setFlightDetailsTextSize` (`xsmall` | `small` | `medium` | `large` | `xlarge`), which applies the corresponding `iAGT-fs-*` CSS class.

### **City Attractions Panel**
- **Function**: Displays a "Top Things To Do" list for the destination city or layovers.
- **Positioning**: Automatically pinned to the **bottom-right** of the screen wrapper.
- **Unified Style**: Matching font colors, header weight, and highlight colors with the flight table.
- **Panel size**: `attractionsPanelWidth` (default `"50vw"`) and `attractionsPanelHeight` (default `"32vh"`).
- **Font size**: Controlled by `setAttractionsDetailsTextSize`, which applies the `iAGT-atts-*` CSS class.

### **Scrollbars**
Both panels use a custom DIV-based scrollbar rather than native browser scrollbars. This is necessary because MagicMirror's global CSS (`main.css`) sets `::-webkit-scrollbar { display: none }` at the Electron/Chromium compositor level, which cannot be overridden per-element. The custom scrollbar supports mouse-wheel scrolling (via native `overflow-y: scroll`), click-to-jump on the track, and drag-to-scroll on the thumb. Touch events (`touchstart`/`touchmove`/`touchend`) are also supported for Raspberry Pi touchscreen users.

### Related Config Options:
- **`showFlightDetails`** / **`showAttractionsDetails`**: Toggle visibility.
- **`flightPanelWidth`** / **`flightPanelHeight`**: Size of the flight overlay panel.
- **`attractionsPanelWidth`** / **`attractionsPanelHeight`**: Size of the attractions overlay panel.
- **`setFlightDetailsTextSize`** / **`setAttractionsDetailsTextSize`**: Font size class applied to each panel.
- **`maxAttractionsDisplay`**: Maximum number of attraction rows shown per page (default `5`).
- **`attractionsAutoScroll`**: Enable the page-flip behaviour.
- **`attractionsScrollInterval`**: Seconds per page (default `3`).
- **`tableX`** / **`tableY`**: Position of flight table.
- **`cityAttractions_Xaxis`** / **`cityAttractions_Yaxis`**: Position of attractions panel.
- **`cityInfoMode`**: Toggle between `destination` or `layovers`.
- **`cityInfoCycleInterval`**: Rotation speed for layover mode.

---

## 6. Departure Alert Notification

When `departureAlertHours` is set to a positive number, the module schedules a one-shot `setTimeout` after `iAGT_INIT` fires. When the timer expires (i.e. the configured number of hours before the first scheduled departure), the module calls `this.sendNotification("IAGT_DEPARTURE_ALERT", payload)`, broadcasting to all other MagicMirror modules.

The payload contains:
```js
{
  flightNumber:  "BA0117",
  departureDate: "2026-06-10",
  from: { name: "...", iata: "...", lat: ..., lon: ... },
  to:   { name: "...", iata: "...", lat: ..., lon: ... },
  hoursUntil: 24
}
```

Other modules (e.g. compliments, alerts, or a TTS module) can listen for `IAGT_DEPARTURE_ALERT` via their own `notificationReceived()` handler to trigger reminders, announcements, or visual alerts.

Set `departureAlertHours: 0` (default) to disable this feature entirely.

---

## 8. Save / Print to File

All save buttons output self-contained HTML files (no external dependencies) that render cleanly in any browser or PDF printer. All output folders are created automatically on first save.

### **City Attractions Save**

Clicking the 🖨 save icon in the attractions panel header triggers:

1. The button shows ⏳ (disabled) while the request is in flight.
2. `MMM-iAmGoingThere.js` sends `iAGT_SAVE_ATTRACTIONS` to `node_helper.js` with `{ cityName, things, airportPostcode, airportDistanceKm }`.
3. `node_helper.js` creates `documents/MySavedCityAttractions/` if it does not exist, then writes:
   ```
   documents/MySavedCityAttractions/[city-slug]_[YYYY-MM-DD-HHMM].html
   ```
4. The file contains:
   - A `✈ Airport — Postcode: XXXX · Distance from city centre: N km` metadata line (if data is present in the city JSON).
   - A styled table: **#** · **Attraction** · **Description**.
5. `node_helper.js` emits `iAGT_SAVE_OK` (or `iAGT_SAVE_ERROR`).
6. The button shows ✓ (green) or ✗ (red) for 3 seconds, then resets to 🖨.

> The `airportPostcode` and `airportDistanceKm` fields are **only** included in the saved file — they do not appear in the on-screen overlay panel.

### **Flight Details Save**

Clicking the 🖨 save icon in the flight table title triggers:

1. The button shows ⏳ (disabled) while saving.
2. `MMM-iAmGoingThere.js` sends `iAGT_SAVE_FLIGHTS` to `node_helper.js` with `{ legs, scenario }`. Non-serializable fields (e.g. `_gcPoints`) are stripped before sending.
3. `node_helper.js` creates `documents/MySavedFlights/` if it does not exist, then writes:
   ```
   documents/MySavedFlights/flights_[YYYY-MM-DD-HHMM].html
   ```
4. The file contains a styled table: **Name** · **Flight** · **Date / Time** · **From** · **To** · **Status**. Legs are sorted by traveler name (Scenario 3) then ascending departure datetime, so multi-traveler printouts are grouped and chronologically ordered.
5. `node_helper.js` emits `iAGT_SAVE_OK` (or `iAGT_SAVE_ERROR`).
6. The button shows ✓ (green) or ✗ (red) for 3 seconds, then resets to 🖨.

### **Airport Terminal Maps Save**

Clicking the teal 🗺 icon button (to the right of the 🖨 flights button, separated by a `|` divider) triggers:

1. The button shows ⏳ (disabled) while saving.
2. `MMM-iAmGoingThere.js` deduplicates all `to` airports from `this.flightLegs` by IATA code and sends `iAGT_SAVE_TERMINAL_MAPS` to `node_helper.js` with `{ destinations: [{ name, iata }, ...] }`.
3. `node_helper.js` creates `documents/MySavedTerminalMaps/` if it does not exist, then writes:
   ```
   documents/MySavedTerminalMaps/terminal_maps_[YYYY-MM-DD-HHMM].html
   ```
4. The file is a **responsive card-layout page** — one card per destination airport — each card showing:
   - The **IATA code** (large, bold, blue)
   - The **full airport name**
   - A **🗺 Google Maps terminal view** link (satellite/maps view of the airport terminal area)
   - A **🔍 Google terminal map search** link
5. `node_helper.js` emits `iAGT_SAVE_OK` (or `iAGT_SAVE_ERROR`).
6. The button shows ✓ (green) or ✗ (red) for 3 seconds, then resets to 🗺.

### **Saved File Locations**

| Content | Folder | Filename format |
|---------|--------|-----------------|
| City attractions | `documents/MySavedCityAttractions/` | `[city-slug]_YYYY-MM-DD-HHMM.html` |
| Flight details | `documents/MySavedFlights/` | `flights_YYYY-MM-DD-HHMM.html` |
| Airport terminal maps | `documents/MySavedTerminalMaps/` | `terminal_maps_YYYY-MM-DD-HHMM.html` |

All folders are created automatically on first save.

---

## 7. Internationalisation (i18n)

The module ships with built-in translation files for **33 languages**. `getTranslations()` registers locale files under `translations/`, and MagicMirror² selects the appropriate file based on the global `language` setting in `config.js`.

Supported locales: `en` (English), `de` (German), `fr` (French), `es` (Spanish), `nl` (Dutch), `it` (Italian), `pt` (Portuguese), `gd` (Scottish Gaelic), `ga` (Irish), `af` (Afrikaans), `ar` (Arabic), `cs` (Czech), `cy` (Welsh), `da` (Danish), `el` (Greek), `fa` (Persian/Farsi), `fi` (Finnish), `hr` (Croatian), `ht` (Haitian Creole), `hu` (Hungarian), `ja` (Japanese), `ko` (Korean), `mi` (Māori), `no` (Norwegian), `pl` (Polish), `ro` (Romanian), `sk` (Slovak), `sl` (Slovenian), `sr` (Serbian), `sv` (Swedish), `tr` (Turkish), `uk` (Ukrainian), `uz` (Uzbek).

All visible strings — panel titles, table headers, status labels, countdown messages, and error text — route through `this.translate()`, so switching language requires only changing the MagicMirror global `language` config key.

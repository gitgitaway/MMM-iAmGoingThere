# amCharts 5 Map — User Guide for MMM-iAmGoingThere

This guide explains how the amCharts 5 map engine is used within **MMM-iAmGoingThere**, what features are available, and how to configure the map display to suit your trip layout.

---

## What is amCharts 5?

[amCharts 5](https://www.amcharts.com/docs/v5/) is a high-performance JavaScript charting and mapping library. The `@amcharts/amcharts5` package includes:

- A core rendering engine (`index.js`)
- A dedicated Map module with projections and series (`map.js`)
- Pre-built GeoJSON world geodata (`worldLow.js`, `worldHigh.js`, etc.)

This module uses the **locally bundled** version stored in `vendor/` — no internet connection is required at runtime.

---

## Library Files Used

| File | Purpose |
|------|---------|
| `vendor/index.js` | amCharts 5 core engine — `am5` global |
| `vendor/map.js` | Map chart module — `am5map` global |
| `vendor/worldLow.js` | Low-resolution GeoJSON world polygons — `am5geodata_worldLow` global |

These are loaded via `getScripts()` in `MMM-iAmGoingThere.js` before the module starts.

---

## Map Projection

This module uses the **NaturalEarth I** projection (`am5map.geoNaturalEarth1()`), which:

- Represents the world as a smooth, aesthetically balanced oval.
- Preserves rough area proportions across the globe.
- Is the standard reference projection for world-level travel maps.
- Is particularly legible when zoomed to show 2–3 continents simultaneously.

### Other Available Projections

amCharts 5 supports additional D3-compatible projections. To use a different one, the `projection` property in `MapChart.new()` can be changed in `initMap()`:

| Projection | Constructor | Best For |
|------------|-------------|----------|
| **NaturalEarth I** *(default)* | `am5map.geoNaturalEarth1()` | World-level travel maps |
| **Mercator** | `am5map.geoMercator()` | Navigation charts, web maps |
| **Orthographic** | `am5map.geoOrthographic()` | Globe / sphere view |
| **Albers USA** | `am5map.geoAlbersUsa()` | USA-only maps |
| **Equirectangular** | `am5map.geoEquirectangular()` | Simple lat/lon grid maps |
| **Miller Cylindrical** | `am5map.geoMiller()` | Political world maps |
| **Eckert IV** | `am5map.geoEckert4()` | Equal-area world maps |

> **Note:** Orthographic renders as a 3D globe. Rotation values centre the visible hemisphere exactly as with NaturalEarth; only the visual style differs.

---

## Viewport: Zoom & Centering

### How amCharts 5 Centering Works

Unlike simpler mapping APIs that use a pan offset to shift the viewport, amCharts 5 centres the NaturalEarth (and other projections) using **globe rotation**. The globe is rotated on its X and Y axes so that the target coordinate appears at the centre of the rendering area.

| Config option | amCharts 5 internal property | Formula |
|---------------|------------------------------|---------|
| `zoomLongitude` | `rotationX` | `rotationX = -zoomLongitude` |
| `zoomLatitude` | `rotationY` | `rotationY = -zoomLatitude` |
| `zoomLevel` | `zoomLevel` | direct (`1` = full world) |

All three are set directly in the `MapChart.new()` constructor **and** reasserted via `chart.setAll()` after the first rendered frame, ensuring the correct viewport even if a deferred layout recalculation runs after init.

### Zoom Level Guide

| `zoomLevel` | Approximate View |
|-------------|-----------------|
| `1` | Full world — all continents visible |
| `1.5` | Two hemispheres — e.g. Atlantic + both coasts |
| `2` | Two continents — e.g. Europe + North America |
| `2.5` | One large continent — e.g. North America alone |
| `3` | Sub-continental — e.g. Western Europe |
| `4+` | Regional / country level |

### Centering Reference Values

| Region | `zoomLongitude` | `zoomLatitude` | Suggested `zoomLevel` |
|--------|----------------|----------------|----------------------|
| Full world | `0` | `20` | `1` |
| Mid-Atlantic (Europe + N. America) | `-30` | `30` | `2.2` |
| Europe | `10` | `52` | `3` |
| North America | `-95` | `40` | `2.5` |
| Asia-Pacific | `130` | `25` | `2` |
| South America | `-60` | `-15` | `2.5` |
| Africa | `20` | `5` | `2` |
| Middle East | `45` | `25` | `3` |
| UK & Ireland | `-3` | `54` | `5` |

### config.js Examples

```js
// Full world — Round The World trip
zoomLevel: 1,
zoomLongitude: 0,
zoomLatitude: 20,

// Europe + North America — World Cup 2026
zoomLevel: 2.2,
zoomLongitude: -30,
zoomLatitude: 30,

// Europe only — Family holiday to Barcelona
zoomLevel: 3,
zoomLongitude: 10,
zoomLatitude: 52,

// North America only — Domestic US trip
zoomLevel: 2.5,
zoomLongitude: -95,
zoomLatitude: 40,

// Asia-Pacific — Australia / Japan trip
zoomLevel: 2,
zoomLongitude: 130,
zoomLatitude: 25,
```

---

## Map Colours

All map colours are configurable via `config.js`. They are applied using `am5.color()` which accepts any valid CSS hex colour string.

| Config option | Default | What it colours |
|---------------|---------|-----------------|
| `colorMapOcean` | `"#1A1A2E"` | Ocean / chart background fill |
| `colorCountries` | `"#2C3E50"` | Country polygon fill |
| `colorCountryBorders` | `"#1A252F"` | Country border stroke |
| `colorAirportHome` | `"#FFD700"` | Home airport marker (gold) |
| `colorAirportOther` | `"#FFFFFF"` | Other airport markers (white) |
| `colorFuturePath` | `"#FFFFFF"` | Scheduled / future leg |
| `colorActivePath` | `"#4499FF"` | In-flight leg (blue) |
| `colorCompletedPath` | `"#00CC66"` | Landed leg (green) |
| `colorPreviousPath` | `"#888888"` | Superseded landed leg (grey) |
| `colorCancelledPath` | `"#FF4444"` | Cancelled leg (red) |
| `colorPlane` | `"#FF6644"` | Live plane icon (orange) |
| `colorGraticule` | `"#FFFFFF"` | Graticule grid lines |
| `colorVisitedCountry` | `"#00AA44"` | Visited countries (Scenario 4) |
| `colorMapBackground` | `"#000000"` | Outer area outside projection |
| `colorMapOcean` | `"#1A1A2E"` | Water fill inside projection |

### Dark Ocean Theme (default)
```js
colorMapOcean:       "#1A1A2E",
colorCountries:      "#2C3E50",
colorCountryBorders: "#1A252F",
```

### Light Political Theme
```js
colorMapOcean:       "#4f9fd4",
colorCountries:      "#e8e0d0",
colorCountryBorders: "#aaaaaa",
```

### High Contrast Theme
```js
colorMapOcean:       "#000000",
colorCountries:      "#1a3a1a",
colorCountryBorders: "#00ff44",
colorFuturePath:     "#ffff00",
colorActivePath:     "#00ccff",
colorCompletedPath:  "#00ff88",
```

---

## Flight Path Rendering

Flight paths are rendered as **GeoJSON LineString** features using `am5map.MapLineSeries`. Multiple series are created — one per flight status bucket — allowing independent colour and dash styling:

| Series | Colour source | Dash style |
|--------|--------------|------------|
| Future/Scheduled | `colorFuturePath` | dotted (`dashArray: "4,4"`) |
| Active/In-flight | `colorActivePath` | solid |
| Completed/Landed | `colorCompletedPath` | solid |
| Previous (superseded) | `colorPreviousPath` | solid, dimmed |
| Cancelled | `colorCancelledPath` | long dash |

When `colorBlindMode: true` is set, dash patterns are also applied to Scheduled (`dashLength: 8`) and Landed (`dashLength: 4`) series so status is distinguishable without relying on colour alone.

The great-circle arc for each leg is generated using **SLERP** (Spherical Linear Interpolation) in `lib/greatCircle.js` with `gcPoints` interpolation steps (default `60`). Higher values produce smoother arcs at the cost of slightly more DOM nodes.

---

## Airport & Plane Markers

Airport markers and the live plane icon use `am5map.MapPointSeries`. Each marker is an SVG circle (airports) or the custom `images/plane.svg` icon (plane).

- **Airport markers** render at the `{ longitude, latitude }` of each `from`/`to` airport.
- **Plane icon** is positioned at `last_position.latitude` / `last_position.longitude` from the AeroAPI response and updates on each poll.
- In **Scenario 3** with multiple simultaneous in-flight legs, each traveler has a **separate plane icon** coloured with their assigned traveler colour.
- The plane SVG nose rotates to match the bearing along the great-circle arc (2-step look-ahead for smooth orientation).

---

## Interactive Features

### Airport Tooltips
Hovering over an airport marker shows a tooltip with the airport name and IATA code. The tooltip stays visible for `tooltipDuration` seconds (default `6`) after the cursor leaves, preventing flicker.

### Attraction Panel Link
When `showAttractionsDetails: true`, clicking an airport marker in the point series automatically loads that city's Top 10 attractions in the attractions overlay panel. This uses the `click` event on the `MapPointSeries` template.

### Manual Country Mapping (Right-Click)
In Scenario 4 ("Where I Have Been"), you can manually mark any country as visited:
- **Right-Click** on any country polygon to toggle its "visited" state.
- Visited countries are filled with `colorVisitedCountry`.
- Manual selections are saved to `data/manual_visited_countries.json` and persist across module reloads.
- This interactive feature uses the `rightclick` event on the `MapPolygonSeries` template.

---

## Graticule & Region Layers

### Graticule Grid
The graticule grid provides a subtle latitude and longitude reference on the map.
- **Implementation**: Uses `am5map.MapLineSeries` with dynamically generated LineString features.
- **Configuration**:
  - `showGraticule: true` to enable.
  - `graticuleStep`: Distance between lines in degrees (default `10`).
  - `colorGraticule`: Line color.
  - `graticuleOpacity`: Line transparency.
  - `graticuleWidth`: Line thickness.

### Polar Ice Cap Suppression
You can hide the Antarctica region to clean up maps where it might appear distorted or unnecessary.
- **Implementation**: Uses the `exclude` property on `MapPolygonSeries`.
- **Configuration**: `hideIceCaps: true` to enable. 
- **Note**: Ice caps are **always shown** on the **Orthographic** (Globe) projection for visual realism, regardless of this setting.

### Directional Nudge Control
Fine-tune the map's position on the screen without affecting the geographic rotation or projection center.
- **Implementation**: Uses `dx` and `dy` properties on the `MapChart`.
- **Functionality**: Moves the entire map visually left, right, up, or down. The "Home" button resets these offsets back to zero.
- **Discovery**: When `hideControlsUntilHover` is enabled, this control (along with others) is hidden until you hover over the map.

### Sub-national Region Layers
This feature allows you to display detailed administrative boundaries (States, Provinces, Departments, etc.) for specific countries.
- **Supported Countries**: Over 130 countries including USA, Canada, UK (England, Scotland, Wales, Northern Ireland), Germany, France, Japan, China, Brazil, and more.
- **Implementation**: Loads dedicated GeoJSON files from the `@amcharts/amcharts5-geodata` package via the `node_helper.js`.
- **Interactivity**:
  - **Hover Effects**: Regions change color on hover.
  - **Click-to-Select**: Clicking a region toggles an "active" state.
- **Configuration**:
  - `showSubnationalRegions: true` to enable.
  - `subnationalAllCountries: true` to enable for all supported countries.
  - `subnationalCountries`: Array of ISO-2 codes for specific countries, e.g., `["US", "CA", "GB"]`.

### Globe Auto-Rotation
For the **Orthographic** (Globe) projection, you can enable `autoRotateGlobeToPlane: true`. This feature automatically rotates the globe to ensure the active plane icon remains centered and visible as it travels. If multiple planes are active, the globe will center on the midpoint between them.

---

## Layout Architecture

```
.iAGT-wrapper (height: 100vh, flex-column)
├── .iAGT-header            ← countdown / title (flex: 0 0 auto)
├── .iAGT-map-container     ← amCharts 5 root div (flex: 1 1 0, fills remaining space)
│     └── am5.Root → MapChart → series...
├── .iAGT-overlay-flight    ← flight table (position: absolute, bottom-left)
└── .iAGT-overlay-city      ← attractions panel (position: absolute, bottom-right)
```

The wrapper uses `padding-bottom` equal to the tallest overlay panel height (in `vh`) so the flex map container stops exactly at the top edge of the panels, preventing them from obscuring map content.

---

## Updating the Bundled amCharts 5 Version

The vendor scripts are in `vendor/`. To update to a newer amCharts 5 release:

1. Download the new build from [amcharts.com/download](https://www.amcharts.com/download/) (choose **amCharts 5 — JavaScript Charts & Maps**).
2. Replace `vendor/index.js` with the new `index.js`.
3. Replace `vendor/map.js` with the new `map.js`.
4. Replace `vendor/worldLow.js` with the new `geodata/worldLow.js`.

> **Important:** Ensure each replacement file uses the **IIFE / UMD** bundle format (sets `am5`, `am5map`, `am5geodata_worldLow` as globals), not the ES-module `export` format. ES modules are not compatible with MagicMirror's `loader.js` script injector.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `am5 is not defined` in console | Scripts not yet loaded when `initMap` fires | Retry mechanism in `initMap` handles this automatically |
| `Unexpected token 'export'` | ES-module build used instead of IIFE/UMD | Replace `vendor/*.js` with UMD/IIFE builds |
| Map shows but at wrong position | `zoomLongitude` / `zoomLatitude` incorrect | Check the centering reference table above; remember negative = West/South |
| Map shows full world despite `zoomLevel > 1` | `panX: "none"` was set | Ensure `panX: "rotateX"` and `panY: "rotateY"` in `initMap` |
| Script loading fails with CDN URLs | No internet / MagicMirror caching | Use local `vendor/` files (already the default) |
| Country fill is very dark / invisible | `colorCountries` too close to `colorMapOcean` | Increase contrast between the two colours |

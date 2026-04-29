# Map Migration Plan: ammap3 → amCharts 5 (COMPLETED)

**Migration Status**: ✅ **Successfully completed 2026-03-15**

**Module**: MMM-iAmGoingThere  
**Current library**: `ammap3` v3.21.15 (end-of-life, no longer maintained)  
**Target library**: `@amcharts/amcharts5` (actively maintained, same vendor)  
**Geodata package**: `@amcharts/amcharts5-geodata`

---

## 1. Why Migrate

| Concern | Detail |
|---|---|
| **EOL** | ammap3 (amCharts 3) has been frozen; no bug fixes, security patches, or browser-compat updates |
| **amCharts 5 is the current generation** | Released 2021, actively maintained, documented, and compatible with modern JS runtimes |
| **Same vendor** | Conceptual continuity — map types, series names, and geodata format are familiar |
| **Better rendering** | amCharts 5 uses a fully SVG-based renderer with per-element reactivity rather than a full `validateData()` cycle |
| **Native antimeridian handling** | `lineType: "curved"` in `MapLineSeries` crosses ±180° correctly without the manual `_splitAtAntimeridian()` workaround |

---

## 2. Current ammap3 Usage Inventory

All map code lives in **`MMM-iAmGoingThere.js`**. The following is a complete inventory of ammap3 surface area that must be replaced:

### 2.1 Script loading (`getScripts`)
```js
this.file("node_modules/ammap3/ammap/ammap.js")
this.file("node_modules/ammap3/ammap/maps/js/worldLow.js")
```

### 2.2 Chart initialisation (`initMap`)
```js
AmCharts.makeChart(divId, {
  type: "map",
  dataProvider: {
    map: "worldLow",
    zoomLevel, zoomLongitude, zoomLatitude,
    lines: [...],    // array of ammap3 line descriptors
    images: [...]    // array of ammap3 image descriptors
  },
  areasSettings:  { unlistedAreasColor, unlistedAreasAlpha, unlistedAreasOutlineColor },
  imagesSettings: { color, selectedColor, pauseDuration, animationDuration, adjustAnimationSpeed },
  linesSettings:  { color, alpha, thickness },
  balloon:        { fadeOutDuration, pointerWidth, cornerRadius, borderThickness, fillAlpha },
  backgroundColor, backgroundAlpha
})
```

### 2.3 Line descriptors (`_segmentsToLines` / `buildMapLines`)
```js
{
  id, latitudes, longitudes,   // ammap3 proprietary format
  color, alpha, thickness, dashLength, arc
}
```

### 2.4 Image/marker descriptors (`buildAirportMarkers`)
```js
{
  svgPath, title, color, labelColor,
  latitude, longitude, scale,
  alpha, rotation           // plane icon rotation = bearing
}
```

### 2.5 Live update (`updateMapLines`)
```js
this.mapChart.dataProvider.lines  = this.buildMapLines(legs);
this.mapChart.dataProvider.images = this.buildAirportMarkers(legs);
this.mapChart.validateData();     // full re-render trigger
```

### 2.6 Test-mode animation (`startTestAnimation`)
```js
// Calls validateData() directly at 30 fps
if (this.mapChart) this.mapChart.validateData();
```

---

## 3. amCharts 5 API Equivalents

| ammap3 concept | amCharts 5 equivalent |
|---|---|
| `AmCharts.makeChart(id, { type:"map" })` | `am5.Root.new(id)` → `am5map.MapChart.new(root, {})` |
| `dataProvider.map: "worldLow"` | `am5map.MapPolygonSeries.new(root, { geoJSON: am5geodata_worldLow })` |
| `areasSettings.unlistedAreasColor` | `polygonSeries.mapPolygons.template.setAll({ fill: am5.color(...) })` |
| `areasSettings.unlistedAreasOutlineColor` | `polygonSeries.mapPolygons.template.setAll({ stroke: am5.color(...) })` |
| `areasSettings.unlistedAreasAlpha` | `polygonSeries.mapPolygons.template.setAll({ fillOpacity: 0.6 })` |
| `backgroundColor` | `chart.chartContainer.set("background", am5.Rectangle.new(root, { fill: am5.color(...) }))` |
| `dataProvider.zoomLevel/Longitude/Latitude` | `chart.zoomToGeoPoint({ longitude, latitude }, zoomLevel, false)` |
| `dataProvider.lines` (array) | `am5map.MapLineSeries` — one series per style group (color + dash) |
| Line `{latitudes, longitudes}` | GeoJSON `{ type:"LineString", coordinates: [[lon,lat],...] }` |
| Line `alpha` | `strokeOpacity` |
| Line `thickness` | `strokeWidth` |
| Line `dashLength` | `strokeDasharray` (e.g. `[8,4]`) |
| `dataProvider.images` (markers + plane) | `am5map.MapPointSeries` with `bullets` → `am5.Graphics.new(root, { svgPath })` |
| Image `rotation` (plane bearing) | `am5.Graphics` bullet with `rotation` set per data-item via adapter or manual set |
| Image `alpha` | `fillOpacity` / `strokeOpacity` on the bullet sprite |
| Image `scale` | `scale` property on the bullet sprite |
| `balloon` (tooltip) | `tooltip` on the bullet sprite or series |
| `mapChart.validateData()` | `series.data.setAll([...])` — reactive, partial, no full repaint |
| Antimeridian split (`_splitAtAntimeridian`) | **Eliminated** — amCharts 5 `MapLineSeries` with `lineType:"curved"` handles it natively |

---

## 4. Architecture Decision: Line Series Strategy

ammap3 allows a different color per individual line in a single flat array. amCharts 5 applies stroke styling at the **series** level via `mapLines.template`.

**Recommended approach — pool lines into typed series:**

Create a fixed set of named series (one per status/style):

| Series name | Color config key | Dash | Thickness |
|---|---|---|---|
| `lineSeriesScheduled` | `colorFuturePath` | `[8,4]` (colorBlindMode) or none | 1 |
| `lineSeriesActive` | `colorActivePath` | none | 3 |
| `lineSeriesTail` | `colorFuturePath` | `[8,4]` | 1 (dimmed active tail) |
| `lineSeriesLanded` | `colorCompletedPath` | `[4,4]` (cbm) or none | 2 |
| `lineSeriesPrevious` | `colorPreviousPath` | `[4,4]` (cbm) or none | 2 |
| `lineSeriesCancelled` | `colorCancelledPath` | `[8,4]` | 1 |

**Scenario 3 (multi-traveler) exception**: Each traveler has a unique color. Because colors are data-driven, use a **single generic line series** and set color per data-item via a `stroke` adapter keyed on a `customColor` field stored in the GeoJSON `properties`.

```js
lineSeries.mapLines.template.adapters.add("stroke", (stroke, target) => {
  const color = target.dataItem?.dataContext?.customColor;
  return color ? am5.color(color) : stroke;
});
```

---

## 5. Architecture Decision: Point / Marker Series Strategy

Use **two separate `MapPointSeries` instances**:

1. **`airportSeries`** — airport target markers (circle SVG path, static positions, tooltip with IATA name)
2. **`planeSeries`** — live plane icon(s) (plane SVG path, dynamic lat/lon, `rotation` updated each tick)

Each series uses `bullets.push()` to attach a custom `am5.Graphics` sprite with the appropriate SVG path and fill color.

Per-item color (home vs. other, or Scenario 3 traveler color) is applied via an adapter on the `fill` property, reading a `customColor` field from the data-item.

---

## 6. Step-by-Step Migration Tasks

### Phase 1 — Dependencies

**Task 1.1**: Update `package.json`
```json
"dependencies": {
  "@amcharts/amcharts5": "^5.x.x",
  "@amcharts/amcharts5-geodata": "^5.x.x"
}
```
Remove `"ammap3"`.

**Task 1.2**: Run `npm install` and confirm the packages resolve.

**Task 1.3**: Locate the browser-ready script files inside node_modules:
- `node_modules/@amcharts/amcharts5/index.js`
- `node_modules/@amcharts/amcharts5/map.js`
- `node_modules/@amcharts/amcharts5-geodata/worldLow.js`

These will be loaded via `getScripts()` exactly as ammap3 was.

---

### Phase 2 — Script Loading

**Task 2.1**: Replace `getScripts()` body:

```js
getScripts () {
  return [
    this.file("lib/greatCircle.js"),
    this.file("node_modules/@amcharts/amcharts5/index.js"),
    this.file("node_modules/@amcharts/amcharts5/map.js"),
    this.file("node_modules/@amcharts/amcharts5-geodata/worldLow.js")
  ];
}
```

Global variables exposed: `am5`, `am5map`, `am5geodata_worldLow`.

---

### Phase 3 — Chart Initialisation (`initMap`)

**Task 3.1**: Replace `AmCharts.makeChart()` with the amCharts 5 Root + Chart + Series pattern.

New `initMap()` structure:
```js
initMap () {
  const divId = `iAGTMapDiv-${this.identifier}`;
  if (!document.getElementById(divId)) { /* error handling */ return; }

  // 1. Root
  const root = am5.Root.new(divId);
  this._mapRoot = root;

  // 2. Chart
  const chart = root.container.children.push(
    am5map.MapChart.new(root, {
      projection:   am5map.geoNaturalEarth1(),
      panX:         "none",
      panY:         "none",
      wheelX:       "none",
      wheelY:       "none",
      rotationX:    -(this.config.zoomLongitude || 0),
      rotationY:    -(this.config.zoomLatitude  || 20)
    })
  );
  this.mapChart = chart;

  // 3. Ocean/background fill
  chart.chartContainer.get("background").setAll({
    fill:        am5.color(this._safeColor(this.config.colorMapOcean || this.config.colorMapBackground)),
    fillOpacity: 1
  });

  // 4. Country polygon series
  const polygonSeries = chart.series.push(
    am5map.MapPolygonSeries.new(root, {
      geoJSON:  am5geodata_worldLow,
      exclude:  []
    })
  );
  polygonSeries.mapPolygons.template.setAll({
    fill:        am5.color(this._safeColor(this.config.colorCountries)),
    fillOpacity: 0.6,
    stroke:      am5.color(this._safeColor(this.config.colorCountryBorders)),
    strokeWidth: 0.5,
    tooltipText: ""
  });

  // 5. Flight path line series (one per status bucket)
  this._initLineSeries(root, chart);

  // 6. Airport + plane point series
  this._initPointSeries(root, chart);

  // 7. Initial render
  this.mapReady = true;
  this.updateMapLines();
  /* ... */
}
```

**Task 3.2**: Implement `_initLineSeries(root, chart)` — creates the six status-keyed series (see §4 above) and stores references as `this._ls` map.

**Task 3.3**: Implement `_initPointSeries(root, chart)` — creates `this._airportSeries` and `this._planeSeries` with bullet templates.

---

### Phase 4 — Line Data Format (`_segmentsToLines` / `buildMapLines`)

**Task 4.1**: Eliminate `_splitAtAntimeridian()` — amCharts 5 handles antimeridian natively.

> **Note**: Keep `_splitAtAntimeridian()` as dead code initially and add a deprecation comment. Remove in a follow-up clean-up commit once the migration is verified.

**Task 4.2**: Rewrite `_segmentsToLines()` to return GeoJSON `Feature` objects:

```js
_segmentsToLine (pts, customColor) {
  return {
    type: "Feature",
    properties: { customColor: customColor || null },
    geometry: {
      type:        "LineString",
      coordinates: pts.map(p => [p.lon, p.lat])  // GeoJSON is [lon, lat]
    }
  };
}
```

**Task 4.3**: Update `buildMapLines()` to return a `Map<seriesKey, Feature[]>` instead of a flat array of ammap3 descriptors. The caller (`updateMapLines`) will call `series.data.setAll(features)` on each named series.

---

### Phase 5 — Marker & Plane Data Format (`buildAirportMarkers`)

**Task 5.1**: Rewrite `buildAirportMarkers()` to return two separate arrays:
- `airports`: `[{ latitude, longitude, iata, name, customColor }, ...]`
- `planes`:   `[{ latitude, longitude, rotation, flightNumber, customColor, shadowOnly, scale, alpha }, ...]`

**Task 5.2**: In `_initPointSeries`, set up the airport bullet:
```js
airportSeries.bullets.push(function(root, series, dataItem) {
  const d = dataItem.dataContext;
  return am5.Bullet.new(root, {
    sprite: am5.Graphics.new(root, {
      svgPath:     TARGET_SVG,
      fill:        am5.color(d.customColor || "#FFFFFF"),
      scale:       0.5,
      tooltipText: d.name ? `{name} ({iata})` : ""
    })
  });
});
```

**Task 5.3**: In `_initPointSeries`, set up the plane bullet:
```js
planeSeries.bullets.push(function(root, series, dataItem) {
  const d = dataItem.dataContext;
  const sprite = am5.Graphics.new(root, {
    svgPath:     PLANE_SVG,
    fill:        am5.color(d.customColor || "#FF6644"),
    fillOpacity: d.alpha ?? 0.9,
    scale:       d.scale ?? 0.06,
    rotation:    d.rotation ?? 0,
    centerX:     am5.p50,
    centerY:     am5.p50
  });
  return am5.Bullet.new(root, { sprite });
});
```

---

### Phase 6 — Live Update (`updateMapLines`)

**Task 6.1**: Replace `validateData()` calls with reactive data updates:

```js
updateMapLines (legs) {
  if (!this.mapChart || !this.mapReady) return;

  const lineData  = this.buildMapLines(legs);     // Map<key, GeoJSON Feature[]>
  const markerData = this.buildAirportMarkers(legs); // { airports, planes }

  for (const [key, features] of Object.entries(lineData)) {
    if (this._ls[key]) this._ls[key].data.setAll(features);
  }
  this._airportSeries.data.setAll(markerData.airports);
  this._planeSeries.data.setAll(markerData.planes);
}
```

**Task 6.2**: Remove the `_validateTimer` debounce mechanism — `series.data.setAll()` is inherently batched and does not require an external debounce.

---

### Phase 7 — Test Mode Animation

**Task 7.1**: In `startTestAnimation`, replace:
```js
if (this.mapChart) this.mapChart.validateData();
```
with:
```js
this.updateMapLines();
```
No other changes required; the reactive data pattern absorbs 30fps updates efficiently.

---

### Phase 8 — Zoom / Initial Viewport

**Task 8.1**: ammap3 used `dataProvider.zoomLevel/Longitude/Latitude` to set the initial viewport. amCharts 5 uses chart rotation for centering and `zoomToGeoPoint()` for zoom:

```js
chart.set("rotationX", -(this.config.zoomLongitude || 0));
chart.set("rotationY", -(this.config.zoomLatitude  || 20));
// Zoom after chart is ready:
chart.events.on("frameended", () => {
  chart.zoomToGeoPoint(
    { longitude: this.config.zoomLongitude, latitude: this.config.zoomLatitude },
    this.config.zoomLevel || 2,
    false
  );
}, this, { once: true });
```

---

### Phase 9 — Tooltip / Balloon

**Task 9.1**: ammap3's `balloon` config handled global tooltips. In amCharts 5, attach a `tooltip` directly to bullet sprites:

```js
am5.Graphics.new(root, {
  svgPath: TARGET_SVG,
  tooltipText: "{name} ({iata})",
  tooltip: am5.Tooltip.new(root, {
    pointerOrientation: "vertical",
    getFillFromSprite:  false,
    background: am5.RoundedRectangle.new(root, {
      fill:        am5.color(0x1a1a2e),
      fillOpacity: 0.85,
      cornerRadiusTL: 4, cornerRadiusTR: 4,
      cornerRadiusBL: 4, cornerRadiusBR: 4
    })
  })
})
```

---

### Phase 10 — Cleanup & Tests

**Task 10.1**: Delete `_splitAtAntimeridian()` (now dead code).

**Task 10.2**: Update `package.json` — remove `ammap3`, add amCharts 5 packages.

**Task 10.3**: Run `node tests/test.js` — the test suite does **not** test map rendering directly (it tests `greatCircle.js`, CSV parsing, and attractions JSON), so all existing tests should pass without modification.

**Task 10.4**: Run `npm run lint` — fix any new ESLint warnings introduced by the migration.

**Task 10.5**: Verify visually on the MagicMirror display:
- [ ] World map renders with correct colors
- [ ] Airport markers appear at correct lat/lon
- [ ] Flight paths render for each status (scheduled/active/landed/previous/cancelled)
- [ ] Plane icon renders at correct position with correct bearing rotation
- [ ] Scenario 3 traveler colors are distinct per traveler
- [ ] colorBlindMode dash patterns are applied
- [ ] Test mode animation runs smoothly
- [ ] Countdown and table overlays are unaffected

---

## 7. File Change Summary

| File | Change Type | Scope |
|---|---|---|
| `package.json` | Modify | Remove `ammap3`; add `@amcharts/amcharts5` + `@amcharts/amcharts5-geodata` |
| `MMM-iAmGoingThere.js` | Modify | `getScripts`, `initMap`, `_initLineSeries`(new), `_initPointSeries`(new), `_segmentsToLine`, `buildMapLines`, `buildAirportMarkers`, `updateMapLines`, `startTestAnimation` |
| `lib/greatCircle.js` | **No change** | SLERP logic is library-agnostic |
| `node_helper.js` | **No change** | Backend has no map dependency |
| `MMM-iAmGoingThere.css` | **No change** | Layout CSS is library-agnostic |
| `tests/test.js` | **No change** | Tests do not cover rendering |

---

## 8. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| amCharts 5 script globals differ from expected names | Medium | High | Verify `am5`, `am5map`, `am5geodata_worldLow` are exposed after loading index.js + map.js + worldLow.js; add guards in `initMap` |
| Per-item color on `MapLineSeries` requires adapter overhead | Low | Low | Use adapter pattern (§4); benchmark in test mode at 30fps |
| Plane rotation not auto-updating each tick | Medium | Medium | Set `rotation` directly on the data-item object; call `planeSeries.data.setAll()` each animation frame |
| amCharts 5 license requirement for commercial use | Low | High | amCharts 5 is free for non-commercial / open-source projects (MIT-like free tier); MagicMirror modules are open-source — verify on amcharts.com/online-store/licenses |
| MagicMirror's Electron version incompatible with amCharts 5 | Low | High | amCharts 5 targets ES6+ and modern SVG; Electron ≥12 is fully compatible |
| `node_modules` path changes break `getScripts` file references | Low | Medium | Test file resolution via `this.file(...)` after `npm install` |

---

## 9. Reference Links

- [amCharts 5 Map Chart docs](https://www.amcharts.com/docs/v5/charts/map-chart/)
- [MapLineSeries docs](https://www.amcharts.com/docs/v5/charts/map-chart/map-line-series/)
- [MapPointSeries docs](https://www.amcharts.com/docs/v5/charts/map-chart/map-point-series/)
- [amCharts 5 geodata npm](https://www.npmjs.com/package/@amcharts/amcharts5-geodata)
- [amCharts 5 npm](https://www.npmjs.com/package/@amcharts/amcharts5)
- [Migrating from amCharts 4](https://www.amcharts.com/docs/v5/migrating-from-amcharts-4/) *(conceptual reference; ammap3 is v3)*

# Map Projections User Guide

The **MMM-iAmGoingThere** module allows you to configure the geographic map projection used to display the world map. This is controlled via the `mapProjection` configuration option in your `config.js`.

| Projection | Value | Best Usage Case | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **Mercator** | `"mercator"` | Default. Zoomed-in views, navigation, high-latitude flight paths. | Familiar "square" map; flight paths curve visibly over the poles (e.g. UK to USA). | Significant area distortion at high latitudes (Greenland looks as large as Africa). |
| **Natural Earth 1** | `"naturalEarth1"` | Balanced world maps for data visualization. | Compromise projection; continents look "natural" and recognizable with minimal distortion. | Not conformal (doesn't preserve angles) or equal-area. |
| **Equirectangular** | `"equirectangular"` | Simple mapping of lat/lon to X/Y coordinates. | Computationally simple; constant scale along the equator. | Massive distortion at the poles; world looks "stretched" horizontally. |
| **Orthographic** | `"orthographic"` | "The Globe Look". Atmospheric or planet-wide views. | Beautiful 3D globe effect; zero distortion at the center. | Only half the Earth is visible at once; extreme distortion near the edges of the circle. |
| **Stereographic** | `"stereographic"` | Polar views or regional mapping. | Conformal (preserves shapes and angles locally); good for mapping one hemisphere. | Scale increases rapidly away from the center; not suitable for whole-world overview. |

---

## 🗺️ How to Change the Projection

In your `config.js`, add or update the `mapProjection` field:

```javascript
{
  module: "MMM-iAmGoingThere",
  config: {
    // ... other config options ...
    mapProjection: "orthographic", // Options: "mercator", "naturalEarth1", "equirectangular", "orthographic", "stereographic"
    // ...
  }
}
```

## 🛠️ Detailed Breakdown

### 1. Mercator (`"mercator"`)
The standard for web maps (Google Maps, OSM). In this module, it is the **default** because it forces great-circle paths between the US and Europe to arc visibly northward (over Greenland), which users typically expect.
- **Pros**: Familiar, maintains local angles (conformal).
- **Cons**: Polar regions are massively oversized.

### 2. Natural Earth 1 (`"naturalEarth1"`)
A pseudocylindrical compromise projection designed specifically for map-making software.
- **Pros**: Aesthetically pleasing for world maps where you want a balance of shape and size.
- **Cons**: Flight paths might appear "flatter" than in Mercator.

### 3. Equirectangular (`"equirectangular"`)
Maps longitude directly to X and latitude directly to Y.
- **Pros**: Good for simple data processing where you need to calculate screen coordinates from GPS coordinates.
- **Cons**: Very distorted near the poles; rarely used for final presentation.

### 4. Orthographic (`"orthographic"`)
Shows the earth as it would appear from deep space (a sphere).
- **Pros**: Great for "dashboard" aesthetics. Pairs well with `zoomLongitude` and `zoomLatitude` to center on your current trip.
- **Cons**: You cannot see both the start and end of a long-haul flight if they are on opposite sides of the planet without panning.

### 5. Stereographic (`"stereographic"`)
A conformal projection that projects the sphere onto a plane.
- **Pros**: Maintains shapes perfectly at the center point.
- **Cons**: The distance between continents is distorted as you move away from the center.

---

---

## 🌐 Visualizing Projections with Graticule Lines

You can enable latitude and longitude grid lines to better understand how each projection distorts the world. This is particularly useful for comparing the "Globe" (Orthographic) look versus the flat Mercator view.

```javascript
showGraticule: true,
graticuleStep: 15, // Draw a line every 15 degrees
colorGraticule: "#ffffff",
graticuleOpacity: 0.1
```

## 💡 Recommendation
- Use **`"mercator"`** if you want your transatlantic flight paths to look like the classic curved arcs seen on seat-back monitors.
- Use **`"orthographic"`** if you prefer a modern, 3D globe look and are tracking shorter regional flights.
- Use **`"naturalEarth1"`** for a balanced, high-quality "atlas" style view.

# MMM-iAmGoingThere — Accessibility Features

This document describes every accessibility feature built into the module, how each one works technically, and which configuration options (if any) control it.

---

## 1. ARIA Live Region — Countdown Box

### What it does
The countdown box announces state changes to screen readers and assistive technologies without requiring the user to navigate to it. When the countdown updates (e.g. from "3 Days Until Departure" to "Currently In Flight"), the new text is automatically read aloud by a screen reader.

### How it works
The countdown `<div>` is created with two ARIA attributes:

```html
<div role="status" aria-live="polite">
```

- **`role="status"`** — Identifies the element as a live status region, equivalent to a `<output>` element.
- **`aria-live="polite"`** — Instructs screen readers to read the updated content at the next natural pause, without interrupting ongoing speech.

The countdown is updated by `updateCountdown()` via `innerHTML`, which triggers the live region announcement automatically.

### Relevant config options
None — this feature is always active.

---

## 2. ARIA Landmark Roles — Overlay Panels

### What it does
Both overlay panels are marked as named landmark regions so that screen reader users can jump to them directly using standard landmark navigation shortcuts.

### How it works

**Flight Status Table panel:**
```html
<div role="region" aria-label="Upcoming Flights Status">
```
- **`role="region"`** — Marks it as a significant section of the page.
- **`aria-label`** — Provides a human-readable name sourced from the `TABLE_TITLE` translation key, so the label is correct in the user's chosen language.

**City Attractions panel:**
```html
<div role="complementary" aria-label="Top 10 Things To Do In">
```
- **`role="complementary"`** — Semantically marks the panel as supplementary content (equivalent to `<aside>`).
- **`aria-label`** — Sourced from the `TOP10_TITLE` translation key.

Both `aria-label` values update automatically when the MagicMirror `language` config changes, because they are set via `this.translate()`.

### Relevant config options
| Option | Effect on this feature |
|--------|----------------------|
| `showFlightDetails` | When `true`, the flight panel (with its `role="region"`) is added to the DOM |
| `showAttractionsDetails` | When `true`, the attractions panel (with its `role="complementary"`) is added to the DOM |

---

## 3. ARIA Scrollbar — Custom Panel Scrollbars

### What it does
Both overlay panels use a custom JavaScript-driven scrollbar (a `<div>` track with a draggable `<div>` thumb) rather than native browser scrollbars. The custom scrollbar is fully annotated for assistive technologies.

### Why a custom scrollbar is needed
MagicMirror's global stylesheet (`main.css`) applies `::-webkit-scrollbar { display: none }` at the Electron/Chromium compositor level. This rule cannot be overridden per-element, so native scrollbars are invisible even when content overflows. The custom scrollbar restores visible scroll affordance.

### How it works
The scrollbar track element is annotated with:

```html
<div
  role="scrollbar"
  aria-orientation="vertical"
  aria-controls="[scroll-panel-id]"
  aria-valuenow="0"
  aria-valuemin="0"
  aria-valuemax="100"
>
```

- **`role="scrollbar"`** — Identifies the element as a scrollbar to assistive technologies.
- **`aria-orientation="vertical"`** — Specifies the scroll axis.
- **`aria-controls`** — References the ID of the scrollable content panel.
- **`aria-valuenow`** — Updated in real time (0–100) as the user scrolls, so screen readers can report scroll position as a percentage.
- **`aria-valuemin` / `aria-valuemax`** — Fixed bounds (0 and 100).

`aria-valuenow` is refreshed on every `scroll` event and on every `requestAnimationFrame` update via a `MutationObserver` that watches for content changes inside the panel.

### Input methods supported
The custom scrollbar handles all of the following input types:

| Input | Mechanism |
|-------|-----------|
| Mouse wheel | Native `overflow-y: scroll` on the content panel |
| Click on track | Calculates target scroll position from click Y coordinate, jumps immediately |
| Drag thumb | `mousemove` / `mouseup` listeners on `document` during drag |
| Touch drag on thumb | `touchmove` / `touchend` listeners for Raspberry Pi touchscreen |
| Content change | `MutationObserver` re-measures and repositions the thumb whenever content is updated |

### Relevant config options
None — the custom scrollbar is always active on both panels when they are enabled.

---

## 4. Colorblind Mode — Path Status Differentiation

### What it does
By default, flight path status (Scheduled / In Flight / Landed / Cancelled) is communicated **only by colour** (white / blue / green / red). `colorBlindMode` adds a second, non-colour visual channel — **line dash pattern** — so that users who cannot distinguish colours can still identify flight status.

### How it works
When `colorBlindMode: true`, the `dashLength` property is applied to each map line segment:

| Status | Colour | `dashLength` | Visual |
|--------|--------|-------------|--------|
| Scheduled / Future | White | `8` | Long dashes |
| Cancelled | Red | `8` | Long dashes |
| Active (in flight) | Blue | `0` | Solid line |
| Landed / Completed | Green | `4` | Short dashes |
| Previous (superseded) | Grey | `8` | Long dashes |

When `colorBlindMode: false` (default), `dashLength` is not applied and all lines are solid.

The dash pattern is applied at the ammap3 line-series level via the `dashLength` property on each line object.

### Relevant config options
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `colorBlindMode` | `Boolean` | `false` | When `true`, applies `dashLength` patterns to flight paths in addition to colour |

> **Tip:** `colorBlindMode` can be combined with custom colours. You can override `colorFuturePath`, `colorActivePath`, `colorCompletedPath`, etc. to use a colour palette suitable for your specific colour vision profile.

---

## 5. CSS Color Injection Safety — `_safeColor()`

### What it does
Any CSS colour value that comes from user configuration (e.g. `colorPlane`, traveler path colours in Scenario 3) is validated before being injected into an inline `style` attribute. Invalid values are replaced with a safe fallback (`#FFFFFF`), preventing CSS injection attacks or malformed styles.

### How it works
The `_safeColor(c)` helper applies a regex test before every inline colour injection:

```js
_safeColor (c) {
  return /^#[0-9A-Fa-f]{3,8}$|^rgba?\(/.test(c) ? c : "#FFFFFF";
}
```

This allows:
- Hex colours: `#RGB`, `#RRGGBB`, `#RRGGBBAA`
- RGB/RGBA functions: `rgb(...)`, `rgba(...)`

All other values (e.g. `javascript:...`, named colours, CSS variables) are rejected and replaced with white.

### Relevant config options
All colour config options pass through `_safeColor()` when used in inline styles:
`colorPlane`, `colorFuturePath`, `colorActivePath`, `colorCompletedPath`, `colorPreviousPath`, `colorCancelledPath`, `colorAirportHome`, `colorAirportOther`, and Scenario 3 traveler colours from `TRAVELER_COLORS`.

---

## 6. Airport Marker Tooltips — Stable Hover Display

### What it does
Airport markers on the map show a tooltip balloon displaying the airport name and IATA code when the user hovers over the marker. Previously this tooltip flickered because the balloon element itself intercepted mouse events, triggering a hide/reappear loop. This has been fixed so the tooltip remains visible for the full configured duration.

### How it works
The ammap3 balloon `<div>` that appears on hover is assigned `pointer-events: none` via CSS:

```css
.amcharts-balloon-div {
  pointer-events: none !important;
}
```

This ensures the balloon is visually present but transparent to the mouse, so the `mouseout` event on the marker is never triggered by the balloon overlapping the cursor.

The tooltip fade-out delay is configured by `tooltipDuration`. The ammap3 `fadeOutDuration` property on the balloon is set to this value.

### Relevant config options
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `tooltipDuration` | `Number` | `6` | Seconds the tooltip balloon remains visible after the mouse leaves the airport marker |

---

## 7. Traveler Colour Identification — Scenario 3

### What it does
In Scenario 3 (multi-origin group trips), each traveler is assigned a unique colour that is applied consistently across:
- Their live plane icon on the map
- The aircraft symbol (✈) and progress percentage in the flight table Status column during active flight
- The full background fill of their Name cell in the flight table

This allows users to identify which flights belong to which traveler at a glance, even across multiple simultaneous active flights.

### How it works
Colours are assigned at module start from a pre-defined palette (`TRAVELER_COLORS`) that deliberately excludes reds and orange-reds to avoid clashing with the plane icon colour. Assignment is deterministic: the first traveler in the `travelers` array always receives the first palette colour.

The Name cell colour is set via an inline `style` attribute validated through `_safeColor()`:

```js
nameCellStyle = ` style="background-color:${color};color:rgba(0,0,0,0.85);font-weight:600;"`;
```

Dark text (`rgba(0,0,0,0.85)`) is used unconditionally, as the palette colours are all light/mid-tone.

### Relevant config options
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `scenario` | `Number` | `1` | Must be `3` to activate per-traveler colour assignment |
| `colorPlane` | `String` | `"#FF6644"` | Colour of the plane icon; palette excludes similar hues to maintain contrast |

---

## 8. Plane Shadow — Visibility Against Light Backgrounds

### What it does
A semi-transparent white halo is rendered beneath the coloured plane icon. This improves the icon's visibility against light-coloured map backgrounds or country fills, providing a contrast boost without changing the icon colour.

### How it works
When `showPlaneShadow: true`, a second ammap3 image marker is added to the map at the same coordinates as the plane, using a white version of the plane SVG, rendered at reduced opacity beneath the coloured icon. The shadow icon updates position in sync with the plane icon on every animation frame.

### Relevant config options
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `showPlaneShadow` | `Boolean` | `true` | Renders a white halo beneath the plane icon for contrast |

---

## 9. Internationalisation — All Visible Strings Translated

### What it does
All user-visible text strings (countdown messages, table headers, panel titles, status labels, placeholder text) are routed through `this.translate(KEY)`. Switching the display language requires no code change — only the global MagicMirror `language` config key needs updating.

### How it works
`getTranslations()` registers all 33 locale files. MagicMirror²'s i18n subsystem selects the correct file at startup. ARIA labels (`aria-label`) also use translated strings, so screen reader announcements are in the correct language.

### Relevant config options
| Setting | Location | Description |
|---------|----------|-------------|
| `language` | MagicMirror global `config.js` | ISO 639-1 locale code (e.g. `"en"`, `"de"`, `"fr"`) — not a module-level option |

See [`Translations.md`](./Translations.md) for a full list of supported languages and translation keys.

---

## Summary Table

| Feature | Always active | Config option(s) |
|---------|:-------------:|-----------------|
| ARIA live region (countdown) | ✓ | — |
| ARIA landmark roles (panels) | ✓ | `showFlightDetails`, `showAttractionsDetails` |
| ARIA scrollbar (custom scrollbar) | ✓ | — |
| Colorblind mode (dash patterns) | — | `colorBlindMode` |
| CSS color injection safety | ✓ | — |
| Stable airport tooltips | ✓ | `tooltipDuration` |
| Traveler colour identification | — | `scenario: 3` |
| Plane shadow (contrast) | ✓ | `showPlaneShadow` |
| Full i18n (all strings translated) | ✓ | `language` (global) |

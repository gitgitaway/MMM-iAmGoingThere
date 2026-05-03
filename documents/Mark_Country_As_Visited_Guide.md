# MMM-iAmGoingThere — Mark Country As Visited Guide

This guide explains how to mark countries as visited on the map, manage your visited-country list, and control how highlights are displayed — across all six scenarios.

---

## Overview

The module supports two ways to mark a country as visited:

| Method | Works in scenario | Persists after restart |
|--------|------------------|----------------------|
| **Automatic** — derived from flight destinations in `config.js` | Scenario 4 only | Yes (rebuilt each start) |
| **Manual** — right-click any country on the map | All scenarios | Yes (saved to `data/manual_visited_countries.json`) |

Both methods produce green highlights (or your chosen `colorVisitedCountry`) on the map. Automatic and manual entries are merged — a country is highlighted if it appears in either source.

---

## Highlight Colours (configurable)

| Config key | Default | Description |
|------------|---------|-------------|
| `colorVisitedCountry` | `#00AA44` | Fill colour for visited country polygons |
| `colorVisitedCountryBorder` | `#008833` | Border colour for visited country polygons |
| `colorVisitedCountryOpacity` | `0.75` | Fill opacity (0.0 – 1.0) |

Add any of these to your `config.js` block to override the defaults:

```js
config: {
  colorVisitedCountry:        "#1E90FF",  // blue instead of green
  colorVisitedCountryBorder:  "#0055CC",
  colorVisitedCountryOpacity: 0.8
}
```

---

## Automatic Highlighting (Scenario 4 only)

In **Scenario 4 ("Where I Have Been")**, the module inspects the destination (`to`) of every flight leg and resolves its country automatically. Any resolved country is highlighted without any manual action.

This includes:
- IATA airport codes resolved via the built-in `data/airports.csv` database
- City names resolved via `data/cities.csv`
- Football team names resolved via `data/football_teams_database.csv`
- **United Kingdom Regions**: "England", "Scotland", "Wales", and "Northern Ireland" are automatically resolved to **GB** (United Kingdom).

Automatic highlights are rebuilt on every module start. They cannot be individually removed, but you can suppress all highlights using the **Highlights Control** (see below).

---

## Manual Highlighting — Right-Click Popup

You can manually mark or unmark any country in **any scenario** by right-clicking it on the map.

### Steps

1. **Right-click** any country polygon on the map.
2. A confirmation popup appears showing:
   - The **country name**
   - Its **current visited status** (✔ green if already marked, ○ grey if not)
   - Two action buttons

   ![Popup appearance]

3. Click **"Mark as Visited"** to add the country, or **"Remove Visited"** to remove it.
4. Click **"Cancel"** (or wait 5 seconds for auto-dismiss) to close without changes.

### What happens next

- The country list is updated immediately in `data/manual_visited_countries.json`.
- The map re-colours within a second — no restart required.
- The change persists across MagicMirror restarts.

### Notes

- Right-clicking a different country while the popup is open replaces it immediately.
- The popup auto-dismisses after **5 seconds** if no button is pressed (a shrinking progress bar shows the remaining time).
- Manual marks apply on top of automatic (Scenario 4) marks; marking a country that is already automatically highlighted has no visible effect until automatic highlighting is removed.

---

## Highlights Control Dropdown

A **"Highlight Visited Countries"** dropdown appears in the top-left corner of the map, directly below the Map Projection selector (visible when `showMapSelector: true`).

### Options

| Option | Effect |
|--------|--------|
| **Highlight Visited Countries** *(default)* | Green highlights are shown for all visited countries (automatic + manual) |
| **No Highlights** | All country highlights are removed instantly. The map shows uniform country colours. This persists until you manually re-select "Highlight Visited Countries" or restart the module |
| **Clear Manually Marked Cache** | Wipes `data/manual_visited_countries.json` and removes all manually-added countries. Automatic highlights (Scenario 4 flight destinations) are unaffected. The dropdown reverts to "Highlight Visited Countries" automatically |
| **Show Sub Regions** | Shows internal borders (states, provinces, etc.) for supported countries |
| **Hide Sub Regions** | Hides internal borders (states, provinces, etc.) |

### Persistence rules

| Event | Highlights state after |
|-------|----------------------|
| Select "No Highlights" | Off — remains off until you change it |
| Flight data update (`iAGT_FLIGHT_UPDATE`) | Unchanged — highlight state is preserved |
| Module restart / MagicMirror reboot | Resets to **On** (default) |
| Select "Clear Manually Marked Cache" | Reverts to On; manual cache is wiped |

> **Tip:** "No Highlights" is a display-only toggle — it does **not** delete your saved data. Your `manual_visited_countries.json` is untouched; highlights simply aren't drawn. Switch back to "Highlight Visited Countries" at any time to restore them.

---

## Managing the Visited Cache File

Manual visited countries are stored in:

```
modules/MMM-iAmGoingThere/data/manual_visited_countries.json
```

### File format

```json
["GB", "FR", "DE", "PT", "IT"]
```

A plain JSON array of ISO 3166-1 alpha-2 country codes (uppercase two-letter codes).

### Editing manually

You can edit this file directly in any text editor to add or remove countries in bulk. MagicMirror must be restarted for direct file edits to take effect.

To find the correct ISO code for a country, refer to the [ISO 3166-1 alpha-2 Wikipedia list](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).

### Clearing via the dropdown

Select **"Clear Manually Marked Cache"** from the Highlights dropdown to wipe the file without editing it manually. This is the recommended method during a live session.

---

## Example: Scenario 4 Configuration with Custom Colours

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 4,
    tripTitle: "My Travel History",
    home: "LHR",
    showMapSelector: true,
    colorVisitedCountry:        "#00AA44",
    colorVisitedCountryBorder:  "#008833",
    colorVisitedCountryOpacity: 0.75,
    flights: [
      { to: "JFK", departureDate: "2023-05-10" },
      { to: "CDG", departureDate: "2023-09-01" },
      { to: "NRT", departureDate: "2024-03-15" }
    ]
  }
}
```

In this example, the USA, France, and Japan will be automatically highlighted green. Any additional countries you mark manually via right-click are also highlighted.

---

## Sub-national Regions vs. Highlights

If you have `showSubnationalRegions: true` enabled in your config:

- **Detailed Borders**: The map will show internal borders (states, provinces, etc.) for supported countries.
- **Independent Layers**: Sub-national regions are a separate visual layer. Marking a country as "Visited" (green highlight) applies to the **entire country polygon** in the base map layer.
- **UK Support**: The module includes detailed sub-national geodata for the United Kingdom (GB), which covers England, Scotland, Wales, and Northern Ireland.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Countries not highlighted at all | `showMapSelector: true` not set, or highlights control set to "No Highlights" | Check the dropdown state; restart to reset to default |
| Country not highlighted in Scenario 4 | Destination country not resolved from airport/city name | Check `data/airports.csv` or `data/cities.csv` for the destination; add a manual mark via right-click |
| Right-click popup does not appear | Map projection may be intercepting events | Try a different projection; check browser console for errors |
| Manual marks lost after restart | `data/manual_visited_countries.json` was deleted or replaced | Re-add via right-click; do not delete the file manually between sessions |
| "Clear Manually Marked Cache" clears automatic highlights | It does not — automatic highlights come from flight legs in `config.js` and are always rebuilt | No action needed; automatic highlights return on next data load |

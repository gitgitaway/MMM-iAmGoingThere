# MMM-iAmGoingThere — Translations Reference

This document lists every translation key used by the module, the 33 supported language locales, and step-by-step instructions for adding a new language.

---

## Translation Keys

All visible strings in the module route through `this.translate(KEY)`. The table below lists every key, where it appears in the UI, and its English value.

| Key | UI Location | English value |
|-----|------------|---------------|
| `TITLE_PREFIX` | Module header — prefix before the destination name | `"We Are On Our Way To"` |
| `COUNTDOWN_DAYS` | Countdown box — plural (2+ days remaining) | `"Days Until Departure"` |
| `COUNTDOWN_DAY` | Countdown box — singular (1 day remaining) | `"Day Until Departure"` |
| `COUNTDOWN_TODAY` | Countdown box — on departure day | `"Bon Voyage! Departure Day!"` |
| `COUNTDOWN_INFLIGHT` | Countdown box — while any leg is active | `"Currently In Flight"` |
| `COUNTDOWN_COMPLETE` | Countdown box — all legs landed | `"Journey Complete — Welcome Home!"` |
| `TOP10_TITLE` | Attractions panel ARIA label (`aria-label`) | `"Top 10 Things To Do In"` |
| `TOP_THINGS_TITLE` | Attractions panel header — inline heading beside the city name | `"Things To Do In"` |
| `NO_ATTRACTIONS` | Attractions panel — shown when no data is available for the city | `"No attractions data available for this city."` |
| `LOADING` | Map loading placeholder and flight table — initial state | `"Loading flight data…"` |
| `TABLE_TITLE` | Flight table title row and panel ARIA label | `"Upcoming Flights Status"` |
| `TBL_NAME` | Flight table — column header: traveler name | `"Name"` |
| `TBL_FLIGHT` | Flight table — column header: flight number | `"Flight No"` |
| `TBL_DATE` | Flight table — column header: departure date | `"Date"` |
| `TBL_DEP` | Flight table — column header: departure airport | `"Departure Airport"` |
| `TBL_ARR` | Flight table — column header: arrival airport | `"Arrival Airport"` |
| `TBL_STATUS` | Flight table — column header: flight status | `"Status"` |
| `ATT_COL_NUM` | Attractions table — column header: row number | `"#"` |
| `ATT_COL_NAME` | Attractions table — column header: attraction name | `"Attraction"` |
| `ATT_COL_DESC` | Attractions table — column header: description | `"Description"` |
| `NO_FLIGHTS` | Flight table — shown when no legs are configured | `"No flights configured"` |
| `VISITED_POPUP_TITLE` | Right-click popup header | `"Change visited status"` |
| `VISITED_IS_VISITED` | Right-click popup — current status (positive) | `"✔ Currently marked as visited"` |
| `VISITED_NOT_VISITED` | Right-click popup — current status (negative) | `"○ Not yet marked as visited"` |
| `VISITED_BTN_MARK` | Right-click popup — button to add country | `"Mark as Visited"` |
| `VISITED_BTN_UNMARK` | Right-click popup — button to remove country | `"Remove Visited"` |
| `VISITED_BTN_CANCEL` | Right-click popup — button to close | `"Cancel"` |
| `VISITED_DRP_HIGHLIGHT` | Highlights dropdown — option to enable | `"Highlight Visited Countries"` |
| `VISITED_DRP_NONE` | Highlights dropdown — option to disable | `"No Highlights"` |
| `VISITED_DRP_CLEAR` | Highlights dropdown — option to wipe cache | `"Clear Manually Marked Cache"` |
| `SUB_DRP_SHOW` | Highlights dropdown — option to show sub-regions | `"Show Sub Regions"` |
| `SUB_DRP_HIDE` | Highlights dropdown — option to hide sub-regions | `"Hide Sub Regions"` |

> **Total keys: 33**

---

## Supported Languages

The module ships translation files for 33 languages (predominently alligned with the confirmed WorldCup 2026 participants). MagicMirror² selects the correct file automatically based on the global `language` setting in your `config.js`.

| Locale code | Language | File |
|-------------|----------|------|
| `en` | English | `translations/en.json` |
| `de` | German | `translations/de.json` |
| `fr` | French | `translations/fr.json` |
| `es` | Spanish | `translations/es.json` |
| `nl` | Dutch | `translations/nl.json` |
| `it` | Italian | `translations/it.json` |
| `pt` | Portuguese | `translations/pt.json` |
| `gd` | Scottish Gaelic | `translations/gd.json` |
| `ga` | Irish | `translations/ga.json` |
| `af` | Afrikaans | `translations/af.json` |
| `ar` | Arabic | `translations/ar.json` |
| `cs` | Czech | `translations/cs.json` |
| `cy` | Welsh | `translations/cy.json` |
| `da` | Danish | `translations/da.json` |
| `el` | Greek | `translations/el.json` |
| `fa` | Persian / Farsi | `translations/fa.json` |
| `fi` | Finnish | `translations/fi.json` |
| `hr` | Croatian | `translations/hr.json` |
| `ht` | Haitian Creole | `translations/ht.json` |
| `hu` | Hungarian | `translations/hu.json` |
| `ja` | Japanese | `translations/ja.json` |
| `ko` | Korean | `translations/ko.json` |
| `mi` | Māori | `translations/mi.json` |
| `no` | Norwegian | `translations/no.json` |
| `pl` | Polish | `translations/pl.json` |
| `ro` | Romanian | `translations/ro.json` |
| `sk` | Slovak | `translations/sk.json` |
| `sl` | Slovenian | `translations/sl.json` |
| `sr` | Serbian | `translations/sr.json` |
| `sv` | Swedish | `translations/sv.json` |
| `tr` | Turkish | `translations/tr.json` |
| `uk` | Ukrainian | `translations/uk.json` |
| `uz` | Uzbek | `translations/uz.json` |

---

## Translation File Format

Each file is a flat JSON object. All 47 keys must be present. Below is the complete English reference file (`translations/en.json`):

```json
{
  "TITLE_PREFIX":        "We Are On Our Way To",
  "COUNTDOWN_DAYS":      "Days Until Departure",
  "COUNTDOWN_DAY":       "Day Until Departure",
  "COUNTDOWN_TODAY":     "Bon Voyage! Departure Day!",
  "COUNTDOWN_DEPARTED":  "Departed — Awaiting Live Tracking…",
  "COUNTDOWN_INFLIGHT":  "Currently In Flight",
  "COUNTDOWN_COMPLETE":  "Journey Complete — Welcome Home!",
  "TOP10_TITLE":         "Top 10 Things To Do In",
  "TOP_THINGS_TITLE":    "Things To Do In",
  "NO_ATTRACTIONS":      "No attractions data available for this city.",
  "LOADING":             "Loading flight data…",
  "TBL_NAME":            "Name",
  "TBL_FLIGHT":          "Flight No",
  "TBL_DATE":            "Date",
  "TBL_DEP":             "Departure Airport",
  "TBL_ARR":             "Arrival Airport",
  "TBL_STATUS":          "Status",
  "TABLE_TITLE":         "Upcoming Flights Status",
  "ATT_COL_NUM":         "#",
  "ATT_COL_NAME":        "Attraction",
  "ATT_COL_DESC":        "Description",
  "NO_FLIGHTS":          "No flights configured",
  "VISITED_POPUP_TITLE":      "Change visited status",
  "VISITED_IS_VISITED":       "✔ Currently marked as visited",
  "VISITED_NOT_VISITED":      "○ Not yet marked as visited",
  "VISITED_BTN_MARK":         "Mark as Visited",
  "VISITED_BTN_UNMARK":       "Remove Visited",
  "VISITED_BTN_CANCEL":       "Cancel",
  "VISITED_DRP_HIGHLIGHT":    "Highlight Visited Countries",
  "VISITED_DRP_NONE":         "No Highlights",
  "VISITED_DRP_CLEAR":        "Clear Manually Marked Cache",
  "SUB_DRP_SHOW":             "Show Sub Regions",
  "SUB_DRP_HIDE":             "Hide Sub Regions"
}
```

---

## How to Add a New Language

### Step 1 — Create the translation file

Copy `translations/en.json` to a new file using the [BCP 47 / ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) locale code as the filename. For example, to add Welsh (if it were not already included):

```
translations/cy.json
```

Translate every value in the JSON object. Do **not** rename or remove any keys — missing keys fall back to English automatically by MagicMirror², but leaving keys untranslated is cleaner.

### Step 2 — Register the locale in `MMM-iAmGoingThere.js`

Open `MMM-iAmGoingThere.js` and find the `getTranslations()` method (around line 163). Add one entry for your locale code:

```js
getTranslations () {
  return {
    en: "translations/en.json",
    de: "translations/de.json",
    // ... existing entries ...
    cy: "translations/cy.json"   // ← add your new locale here
  };
},
```

### Step 3 — Test it

In MagicMirror's main `config.js`, temporarily set the global language to your locale code:

```js
language: "cy",
```

Restart MagicMirror and verify all visible strings render correctly. Check the countdown box, the flight table column headers, and the attractions panel heading.

### Step 4 — Revert or keep the language setting

If you were testing, revert `language` to your preferred locale. If this is your actual desired locale, leave it set.

---

## Notes on Right-to-Left Languages

Arabic (`ar`), Persian (`fa`), Hebrew, and other RTL scripts work correctly at the text level because MagicMirror² renders inside Electron/Chromium, which handles Unicode bidirectional text automatically. If the overall UI layout should mirror for RTL, that requires additional CSS changes not currently in scope for this module.

---

## Missing or Partial Translations

If a key is present in `en.json` but missing from another locale file, MagicMirror²'s i18n subsystem falls back to the English string automatically — no error is thrown. However, incomplete translation files should be considered a bug and contributions are welcome.

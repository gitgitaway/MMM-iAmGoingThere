# MMM-iAmGoingThere — Translations

The module ships with built-in translation files for **33 languages**. MagicMirror² selects the correct file automatically based on the global `language` setting in your `config.js`.

All visible strings — panel titles, table headers, status labels, countdown messages, and error text — route through `this.translate()`, so switching language requires only changing the MagicMirror global `language` key.

---

## Setting Your Language

In your MagicMirror `config/config.js`:

```js
var config = {
  language: "fr",   // ← set to any locale code from the table below
  ...
}
```

---

## Supported Locales

| Flag | Locale Code | Language | Native Name |
|------|-------------|----------|-------------|
| 🇿🇦 | `af` | Afrikaans | Afrikaans |
| 🇸🇦 | `ar` | Arabic | العربية |
| 🇨🇿 | `cs` | Czech | Čeština |
| 🏴󠁧󠁢󠁷󠁬󠁳󠁿 | `cy` | Welsh | Cymraeg |
| 🇩🇰 | `da` | Danish | Dansk |
| 🇩🇪 | `de` | German | Deutsch |
| 🇬🇷 | `el` | Greek | Ελληνικά |
| 🇬🇧 | `en` | English | English |
| 🇮🇷 | `fa` | Persian / Farsi | فارسی |
| 🇫🇮 | `fi` | Finnish | Suomi |
| 🇫🇷 | `fr` | French | Français |
| 🇮🇪 | `ga` | Irish | Gaeilge |
| 🏴󠁧󠁢󠁳󠁣󠁴󠁿 | `gd` | Scottish Gaelic | Gàidhlig |
| 🇭🇷 | `hr` | Croatian | Hrvatski |
| 🇭🇹 | `ht` | Haitian Creole | Kreyòl Ayisyen |
| 🇭🇺 | `hu` | Hungarian | Magyar |
| 🇮🇹 | `it` | Italian | Italiano |
| 🇯🇵 | `ja` | Japanese | 日本語 |
| 🇰🇷 | `ko` | Korean | 한국어 |
| 🇳🇿 | `mi` | Māori | Te Reo Māori |
| 🇳🇱 | `nl` | Dutch | Nederlands |
| 🇳🇴 | `no` | Norwegian | Norsk |
| 🇵🇱 | `pl` | Polish | Polski |
| 🇵🇹 | `pt` | Portuguese | Português |
| 🇷🇴 | `ro` | Romanian | Română |
| 🇸🇰 | `sk` | Slovak | Slovenčina |
| 🇸🇮 | `sl` | Slovenian | Slovenščina |
| 🇷🇸 | `sr` | Serbian | Српски |
| 🇸🇪 | `sv` | Swedish | Svenska |
| 🇹🇷 | `tr` | Turkish | Türkçe |
| 🇺🇦 | `uk` | Ukrainian | Українська |
| 🇺🇿 | `uz` | Uzbek | O'zbek |
| 🇪🇸 | `es` | Spanish | Español |

---

## Translation File Structure

Each file (e.g. `translations/fr.json`) contains key–value pairs for every string displayed by the module:

```json
{
  "TABLE_TITLE":       "Statut des vols",
  "TBL_NAME":          "Voyageur",
  "TBL_FLIGHT":        "Vol",
  "TBL_DATE":          "Date",
  "TBL_DEP":           "Départ",
  "TBL_ARR":           "Arrivée",
  "TBL_STATUS":        "Statut",
  "ATT_TITLE":         "À faire à",
  "ATT_COL_NUM":       "#",
  "ATT_COL_NAME":      "Lieu",
  "ATT_COL_DESC":      "Description",
  "LOADING":           "Chargement…",
  "NO_ATTRACTIONS":    "Aucune attraction disponible.",
  "NO_API_KEY":        "Clé AeroAPI manquante.",
  "COUNTDOWN_DAYS":    "jours",
  "COUNTDOWN_TODAY":   "Aujourd'hui !",
  "COUNTDOWN_FLYING":  "En vol ✈",
  "COUNTDOWN_LANDED":  "Arrivé ✓"
}
```

---

## Contributing a New Translation

1. Copy `translations/en.json` to a new file named with the [BCP 47 locale code](https://en.wikipedia.org/wiki/IETF_language_tag) (e.g. `translations/fi.json`).
2. Translate every value (keep all JSON keys unchanged).
3. Add the locale to `getTranslations()` in `MMM-iAmGoingThere.js`.
4. Add a row to the table above in this file.

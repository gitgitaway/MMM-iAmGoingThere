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
  "TITLE_PREFIX": "Nous sommes en route vers",
  "COUNTDOWN_DAYS": "Jours avant le départ",
  "COUNTDOWN_DAY": "Jour avant le départ",
  "COUNTDOWN_TODAY": "Bon voyage ! Jour du départ !",
  "COUNTDOWN_INFLIGHT": "Actuellement en vol",
  "COUNTDOWN_COMPLETE": "Voyage terminé — Bienvenue à la maison !",
  "TOP10_TITLE": "Top 10 à faire à",
  "TOP_THINGS_TITLE": "Choses à faire à",
  "NO_ATTRACTIONS": "Aucune donnée d'attractions disponible pour cette ville.",
  "LOADING": "Chargement des données de vol…",
  "TBL_NAME": "Nom",
  "TBL_FLIGHT": "N° de vol",
  "TBL_DATE": "Date",
  "TBL_DEP": "Aéroport de départ",
  "TBL_ARR": "Aéroport d'arrivée",
  "TBL_STATUS": "Statut",
  "TABLE_TITLE": "Statut des vols à venir",
  "ATT_COL_NUM": "#",
  "ATT_COL_NAME": "Attraction",
  "ATT_COL_DESC": "Description",
  "NO_FLIGHTS": "Aucun vol configuré",
  "VISITED_POPUP_TITLE": "Modifier le statut de visite",
  "VISITED_IS_VISITED": "✔ Actuellement marqué comme visité",
  "VISITED_NOT_VISITED": "○ Pas encore marqué comme visité",
  "VISITED_BTN_MARK": "Marquer comme Visité",
  "VISITED_BTN_UNMARK": "Retirer Visité",
  "VISITED_BTN_CANCEL": "Annuler",
  "VISITED_DRP_HIGHLIGHT": "Mettre en évidence les pays visités",
  "VISITED_DRP_NONE": "Pas de mise en évidence",
  "VISITED_DRP_CLEAR": "Effacer le cache marqué manuellement"
}
```

---

## Contributing a New Translation

1. Copy `translations/en.json` to a new file named with the [BCP 47 locale code](https://en.wikipedia.org/wiki/IETF_language_tag) (e.g. `translations/fi.json`).
2. Translate every value (keep all JSON keys unchanged).
3. Add the locale to `getTranslations()` in `MMM-iAmGoingThere.js`.
4. Add a row to the table above in this file.

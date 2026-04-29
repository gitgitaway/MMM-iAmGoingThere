# MMM-iAmGoingThere — Scenarios Guide

This guide provides detailed configuration examples for the six supported trip scenarios in **MMM-iAmGoingThere**.

---

## Scenario 1 — Standard Round Trip

A single outbound leg and a single return leg between home and destination. No stopovers.

**Example — Glasgow to Barcelona (1–8 August 2026):**

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 1,
    tripTitle: "Barcelona – Summer 2026",
    flightAwareApiKey: "YOUR_AEROAPI_KEY_HERE",
    home: { name: "Glasgow Airport", iata: "GLA", lat: 55.8697, lon: -4.4331 },
    destination: { name: "Barcelona Airport", iata: "BCN", lat: 41.2971, lon: 2.0785 },
    flights: [
      {
        travelerName: "The Family",
        flightNumber: "FR2891",
        departureDate: "2026-08-01",
        from: "GLA",
        to: "BCN"
      },
      {
        travelerName: "The Family",
        flightNumber: "FR2892",
        departureDate: "2026-08-08",
        from: "BCN",
        to: "GLA"
      }
    ]
  }
}
```

---

## Scenario 2 — Multi-Leg / Round The World

Sequential legs departing from and ultimately returning to the same origin. Supports 10+ legs.

**Example — Round The World from Inverness (20 May – 20 June 2026):**

Route: **INV → LHR → SFO → Fiji → Auckland → Christchurch → Sydney → Singapore → LHR → INV**

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 2,
    tripTitle: "Round The World 2026",
    flightAwareApiKey: "YOUR_AEROAPI_KEY_HERE",
    zoomLevel: 1,
    zoomLongitude: 20,
    zoomLatitude: 20,
    home: { name: "Inverness Airport", iata: "INV", lat: 57.5425, lon: -4.0475 },
    flights: [
      { travelerName: "The Hobbit Family", flightNumber: "BA1478", departureDate: "2026-05-20", from: "INV", to: "LHR" },
      { travelerName: "The Hobbit Family", flightNumber: "BA0283", departureDate: "2026-05-20", from: "LHR", to: "SFO" },
      { travelerName: "The Hobbit Family", flightNumber: "FJ812",  departureDate: "2026-05-22", from: "SFO", to: "NAN" },
      { travelerName: "The Hobbit Family", flightNumber: "FJ411",  departureDate: "2026-05-25", from: "NAN", to: "AKL" },
      { travelerName: "The Hobbit Family", flightNumber: "NZ523",  departureDate: "2026-05-28", from: "AKL", to: "CHC" },
      { travelerName: "The Hobbit Family", flightNumber: "QF155",  departureDate: "2026-05-31", from: "CHC", to: "SYD" },
      { travelerName: "The Hobbit Family", flightNumber: "SQ231",  departureDate: "2026-06-05", from: "SYD", to: "SIN" },
      { travelerName: "The Hobbit Family", flightNumber: "SQ317",  departureDate: "2026-06-10", from: "SIN", to: "LHR" },
      { travelerName: "The Hobbit Family", flightNumber: "BA1477", departureDate: "2026-06-20", from: "LHR", to: "INV" }
    ]
  }
}
```

---

## Scenario 3 — Multi-Origin (World Cup / Group Events)

Multiple travelers flying from different origins to a shared destination. Each traveler has independent `flights` (outbound) and `returnFlights`.

**Example — John & Michael fly to Boston for World Cup 2026:**

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 3,
    tripTitle: "Boston – World Cup 2026",
    flightAwareApiKey: "YOUR_AEROAPI_KEY_HERE",
    home: { name: "Edinburgh Airport", iata: "EDI", lat: 55.9500, lon: -3.3725 },
    destination: { name: "Boston", iata: "BOS", lat: 42.3656, lon: -71.0096 },
    travelers: [
      {
        name: "John",
        flights: [
          { flightNumber: "FR1677", departureDate: "2026-06-10", from: "EDI", to: "SNN" },
          { flightNumber: "UA289",  departureDate: "2026-06-11", from: "SNN", to: "ORD" },
          { flightNumber: "UA1693", departureDate: "2026-06-11", from: "ORD", to: "BOS" }
        ],
        returnFlights: [
          { flightNumber: "UA1732", departureDate: "2026-06-21", from: "BOS", to: "ORD" },
          { flightNumber: "UA173",  departureDate: "2026-06-21", from: "ORD", to: "SNN" },
          { flightNumber: "FR1676", departureDate: "2026-06-22", from: "SNN", to: "EDI" }
        ]
      },
      {
        name: "Michael",
        flights: [
          { flightNumber: "UA2647", departureDate: "2026-06-11", from: "SFO", to: "BOS" }
        ],
        returnFlights: [
          { flightNumber: "UA1074", departureDate: "2026-06-22", from: "BOS", to: "SFO" }
        ]
      }
    ]
  }
}
```

---

## Scenario 4 — Where I Have Been

Displays a collection of all previously visited destinations. 
- Home location is marked with a **Gold** marker.
- All visited destinations (listed in `flights`) are marked with **White** markers (or crests).
- **Green Countries** — Countries that have been visited at least once are automatically colored green (or your chosen `colorVisitedCountry`). This includes destinations resolved via city names or football teams.
- **Manual Coloring** — You can manually mark any country as "visited" by **right-clicking** it on the map. Manual selections are saved to `data/manual_visited_countries.json` and persist after restarting.
- **Football Team Crests** — If a destination is resolved via a football team name, the marker is replaced by the team's crest.
- **Flight tracks** are only visible when `showFlightTracks` is set to `"test"`.

**Example — Tracking multiple past trips:**

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 4,
    showWhereIHaveBeen: true,
    showFlightTracks: "test",
    tripTitle: "My Past Travels",
    home: { name: "London Heathrow", iata: "LHR", lat: 51.4775, lon: -0.4614 },
    flights: [
      { to: "JFK", departureDate: "2023-05-10" },
      { to: "San Francisco", departureDate: "2023-08-15" },
      { to: "Manchester United", departureDate: "2024-01-10" },
      { to: { name: "Remote Cabin", lat: 64.1265, lon: -21.8174 }, departureDate: "2024-02-01" }
    ]
  }
}
```

---

## Scenario 5 — Aircrew / Frequent Flyer CSV Roster

Loads flight legs from a plain CSV file. Designed for aircrew, frequent flyers, or anyone who maintains a rolling schedule in a spreadsheet. No changes to `config.js` are needed when the schedule changes — just edit the CSV.

**CSV file location:** `data/my_flights.csv` (configurable via `crewFlightsFile`)

### CSV Format

```csv
# Lines beginning with # are comments and are ignored
departureDate,flightNumber,from,to,departureTime,travelerName,type
2026-04-02,BA0007,LHR,DXB,09:10,Alex Reid,outbound
2026-04-05,EK0500,DXB,BOM,14:30,Alex Reid,outbound
2026-04-06,BA0138,BOM,LHR,02:20,Alex Reid,return
2026-04-09,BA0175,LHR,JFK,11:15,Alex Reid,outbound
2026-04-14,BA0178,JFK,LHR,21:00,Alex Reid,return
```

| Column | Required | Description |
|--------|----------|-------------|
| `departureDate` | ✅ | `YYYY-MM-DD` |
| `flightNumber` | ✅ | Airline + number, e.g. `BA0117` |
| `from` | ✅ | IATA code of departure airport |
| `to` | ✅ | IATA code of arrival airport |
| `departureTime` | optional | `HH:MM` local — used for same-day leg ordering |
| `travelerName` | optional | Name shown in the flight table (defaults to `Crew`) |
| `type` | optional | `outbound` or `return` (defaults to `outbound`) |

### MagicMirror Config

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 5,
    tripTitle: "Alex Reid — Crew Schedule",
    flightAwareApiKey: "YOUR_AEROAPI_KEY_HERE",
    crewFlightsFile: "data/my_flights.csv",
    home: { name: "London Heathrow", iata: "LHR", lat: 51.4775, lon: -0.4614 },
    showFlightDetails: true,
    showFlightTracks: "auto"
  }
}
```

### Key Behaviours

- **Live tracking** — FlightAware AeroAPI is polled for each leg exactly as in Scenarios 1–3. Requires `flightAwareApiKey`.
- **No config restart** — editing `my_flights.csv` takes effect on the next MagicMirror restart. The CSV is re-read on every `iAGT_CONFIG` event.
- **Multiple crew members** — add more rows with different `travelerName` values; each name will appear as a separate row in the flight table.
- **Path containment** — `crewFlightsFile` is validated to stay within the module directory to prevent directory traversal.

---

## Scenario 6 — Football Away Days

Loads football fixtures from a CSV file and automatically resolves the stadium location for each opponent via a comprehensive built-in database. This scenario is ideal for tracking away days across Europe.

**CSV file location:** `data/footballAwayTrips.csv` (configurable via `footballAwayTripsFile`)

### CSV Format

The CSV requires `departureDate` and `to` (Opponent Name). Other columns are optional.

```csv
departureDate,Competition,to,flightNumber,travelerName,score,result
26/02/2026,Europa League,VfB Stuttgart,GO,Fans,1-0,W
22/01/2026,Europa League,Bologna,GO,Fans,1-1,D
27/11/2025,Europa League,Feyenoord,GO,Fans,0-0,D
```

| Column | Description |
|--------|-------------|
| `departureDate` | `DD/MM/YYYY` or `YYYY-MM-DD` |
| `to` | **Opponent Name**. This is used to resolve the stadium coordinates via `data/football_teams_database.csv`. |
| `Competition` | Name of the competition (shown in tooltip). |
| `score` | Match score (shown in tooltip). |
| `result` | Match result (W/D/L) (shown in tooltip). |

### MagicMirror Config

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 6,
    tripTitle: "Football European Away Days",
    footballAwayTripsFile: "data/footballAwayTrips.csv",
    showFlightDetails: false,
    showFlightTracks: null
  }
}
```

### Key Behaviours

- **Stadium Resolution** — The module matches the `to` name against a database of over 500 European teams. It supports exact, fuzzy, and substring matching, and automatically handles common Unicode accents (e.g., Bodø/Glimt).
- **Marker Rendering** — Destinations are marked with official club crests if the image exists in `images/crests/[Country]/`. If the image is missing, it falls back to a visible circle marker.
- **Tooltip Aggregation** — If you visit the same stadium multiple times, the fixture details are aggregated into a single rich tooltip.
- **Size Reduction** — Markers in this scenario are rendered at 50% scale (17x17px) to keep the map readable even with many markers.
- **Static Display** — Flight tracking is disabled for this scenario by default as it focus on destination history.



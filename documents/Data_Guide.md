# MMM-iAmGoingThere — Data & Coverage Guide

This guide details the built-in databases and coverage provided by **MMM-iAmGoingThere**, along with instructions for adding custom data.

---

## Pre-loaded Databases

The module includes several built-in databases for easy location resolution:

- **Cities (`data/cities.csv`)** — 430+ cities spanning every UN-recognised country.
- **Attractions (`data/attractions/`)** — Curated Top 10 attractions JSON file for every city.
- **Football Teams (`data/football_teams_database.csv`)** — Global database of professional football teams, allowing you to set destinations by team name.
- **Airports (`data/airports.csv`)** — 300+ global airports resolved by IATA code.

---

## Sub-national Region Coverage

The module supports high-detail sub-national boundaries (states, provinces, departments, etc.) for **130+ countries**, provided by the `amcharts5-geodata` package.

### Coverage Breakdown:
- **Europe**: Comprehensive coverage across the continent, including detailed mapping for the **United Kingdom (England, Scotland, Wales, Northern Ireland)**, Germany, France, Italy, Spain, and others.
- **Americas**: Full coverage for USA (States), Canada (Provinces), Brazil, Mexico, Argentina, etc.
- **Asia**: Russia, China, India, Japan, Indonesia, etc.
- **Oceania**: Australia and New Zealand.
- **Africa**: South Africa, Nigeria, Egypt, Morocco, etc.

To enable these layers, set `showSubnationalRegions: true` and `subnationalAllCountries: true` in your `config.js`.

---

## FIFA World Cup 2026 Host Cities

| City | Country | IATA | Stadium |
|------|---------|------|---------|
| New York | USA | JFK/EWR | MetLife Stadium |
| Los Angeles | USA | LAX | SoFi Stadium |
| Dallas | USA | DFW | AT&T Stadium |
| San Francisco | USA | SFO | Levi's Stadium |
| Seattle | USA | SEA | Lumen Field |
| Boston | USA | BOS | Gillette Stadium |
| Miami | USA | MIA | Hard Rock Stadium |
| Atlanta | USA | ATL | Mercedes-Benz Stadium |
| Kansas City | USA | MCI | Arrowhead Stadium |
| Houston | USA | IAH | NRG Stadium |
| Toronto | Canada | YYZ | BMO Field |
| Vancouver | Canada | YVR | BC Place |
| Mexico City | Mexico | MEX | Estadio Azteca |
| Guadalajara | Mexico | GDL | Estadio Akron |
| Monterrey | Mexico | MTY | Estadio BBVA |

---

## Global Coverage by Region

The module includes 430+ cities across all UN member states. Major regional highlights:

| Region | Coverage Details |
|--------|------------------|
| **UK & Ireland** | 20+ airports across England, Scotland, Wales, Northern Ireland, Republic of Ireland |
| **Western Europe** | France, Germany, Spain, Italy, Austria, Netherlands, etc. |
| **Northern Europe** | Scandinavia, Baltics, Iceland |
| **Eastern Europe** | Poland, Czech Republic, Hungary, Romania, etc. |
| **Balkans & Greece** | Croatia, Serbia, Greece, etc. |
| **Russia & Central Asia** | Russia (5 cities), Kazakhstan, Uzbekistan, etc. |
| **Middle East** | Turkey, Israel, Saudi Arabia, UAE, Qatar, etc. |
| **South Asia** | India (12 cities), Pakistan, Bangladesh, etc. |
| **East Asia** | China (19 cities), Japan, South Korea, etc. |
| **Southeast Asia** | Thailand, Vietnam, Indonesia, Malaysia, Singapore, etc. |
| **Oceania** | Australia (9 cities), New Zealand (5 cities), Pacific Islands |
| **Africa** | Coverage across all 54 African nations including South Africa, Nigeria, Kenya, Egypt, Morocco |
| **Americas** | USA, Canada, Mexico, Central America, Caribbean, and all South American nations |

---

## Adding Custom Cities

1. Add a row to `data/cities.csv`:
```csv
"My City","Country","IATA",lat,lon,"Venue Name",my_city.json
```

2. Create `data/attractions/my_city.json`:
```json
{
  "city": "My City",
  "country": "Country",
  "airportPostcode": "AB1 2CD",
  "airportDistanceKm": 15,
  "things": [
    { "rank": 1, "name": "Top Attraction", "description": "Brief description" },
    { "rank": 2, "name": "Second Attraction", "description": "Brief description" }
  ]
}
```

> **Note:** The filename must match the city name lowercased with spaces replaced by underscores (e.g. `new_york.json`).

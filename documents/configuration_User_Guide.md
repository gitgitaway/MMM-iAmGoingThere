# MMM-iAmGoingThere — Detailed Configuration Guide

## Airport References — Full Object vs. IATA-Only

Flight leg `from` and `to` fields accept three forms. All three are equivalent:

```js
// 1. Full object (explicit — always works)
from: { name: "London Heathrow", iata: "LHR", lat: 51.4775, lon: -0.4614 }

// 2. IATA string only (coordinates resolved from built-in airports.csv database)
from: "LHR"

// 3. Partial object with iata key (name and coordinates filled in from database)
from: { iata: "LHR" }
```

> **Tip:** For any airport in the built-in `data/airports.csv` database, using the IATA string is the most concise option and avoids coordinate typos.

---

## Scenario Configuration Examples

### Scenario 1: Round Trip — IATA shorthand

The simplest possible config using bare IATA strings:

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 1,
    showFlightTracks: "auto",
    tripTitle: "New York trip 2026",
    flightAwareApiKey: "YOUR_API_KEY_HERE",
    home: "LHR",
    destination: "JFK",
    flights: [
      { travelerName: "Your Name", flightNumber: "BA0117", departureDate: "2026-06-10", from: "LHR", to: "JFK" },
      { travelerName: "Your Name", flightNumber: "BA0116", departureDate: "2026-06-24", from: "JFK", to: "LHR" }
    ]
  }
}
```

### Scenario 1: Round Trip — Full Objects

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 1,
    showFlightTracks: "auto",
    tripTitle: "New York World Cup 2026",
    flightAwareApiKey: "YOUR_API_KEY_HERE",
    home: { name: "London Heathrow", iata: "LHR", lat: 51.4775, lon: -0.4614 },
    destination: { name: "New York", iata: "JFK", lat: 40.6413, lon: -73.7781 },
    flights: [
      {
        travelerName: "Your Name",
        flightNumber: "BA0117",
        departureDate: "2026-06-10",
        from: { name: "London Heathrow", iata: "LHR", lat: 51.4775, lon: -0.4614 },
        to:   { name: "New York JFK",    iata: "JFK", lat: 40.6413, lon: -73.7781 }
      },
      {
        travelerName: "Your Name",
        flightNumber: "BA0116",
        departureDate: "2026-06-24",
        from: { name: "New York JFK",    iata: "JFK", lat: 40.6413, lon: -73.7781 },
        to:   { name: "London Heathrow", iata: "LHR", lat: 51.4775, lon: -0.4614 }
      }
    ]
  }
}
```

---

### Scenario 2: Round The World (10 Legs)

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 2,
    showFlightTracks: "auto",
    tripTitle: "Round The World 2026",
    flightAwareApiKey: "YOUR_API_KEY_HERE",
    zoomLevel: 1.5,
    flights: [
        {
					travelerName:  "The Hobbit Family",
					flightNumber:  "BA1478",
					departureDate: "2026-05-20",
					from: { name: "Inverness Airport",  iata: "INV", lat:  57.5425, lon:   -4.0475 },
					to:   { name: "London Heathrow",    iata: "LHR", lat:  51.4775, lon:   -0.4614 }
				},
				{
					travelerName:  "The Hobbit Family",
					flightNumber:  "BA0283",
					departureDate: "2026-05-20",
					from: { name: "London Heathrow",    iata: "LHR", lat:  51.4775, lon: -0.4614   },
					to:   { name: "San Francisco",      iata: "SFO", lat:  37.6213, lon: -122.3790 }
				},

				{
					travelerName:  "The Hobbit Family",
					flightNumber:  "FJ812",
					departureDate: "2026-05-22",
					from: { name: "San Francisco",      iata: "SFO", lat:  37.6213, lon: -122.3790 },
					to:   { name: "Nadi (Fiji)",        iata: "NAN", lat: -17.7553, lon:  177.4431 }
				},
				{
					travelerName:  "The Hobbit Family",
					flightNumber:  "FJ411",
					departureDate: "2026-05-25",
					from: { name: "Nadi (Fiji)",        iata: "NAN", lat: -17.7553, lon:  177.4431 },
					to:   { name: "Auckland",           iata: "AKL", lat: -37.0082, lon:  174.7850 }
				},
				{
					travelerName:  "The Hobbit Family",
					flightNumber:  "NZ523",
					departureDate: "2026-05-28",
					from: { name: "Auckland",           iata: "AKL", lat: -37.0082, lon:  174.7850 },
					to:   { name: "Christchurch",       iata: "CHC", lat: -43.4894, lon:  172.5322 }
				},
				{
					travelerName:  "The Hobbit Family",
					flightNumber:  "QF155",
					departureDate: "2026-05-31",
					from: { name: "Christchurch",       iata: "CHC", lat: -43.4894, lon:  172.5322 },
					to:   { name: "Sydney",             iata: "SYD", lat: -33.9399, lon:  151.1753 }
				},
				{
					travelerName:  "The Hobbit Family",
					flightNumber:  "SQ231",
					departureDate: "2026-06-05",
					from: { name: "Sydney",             iata: "SYD", lat: -33.9399, lon:  151.1753 },
					to:   { name: "Singapore Changi",   iata: "SIN", lat:   1.3644, lon:  103.9915 }
				},
				{
					travelerName:  "The Hobbit Family",
					flightNumber:  "SQ317",
					departureDate: "2026-06-10",
					from: { name: "Singapore Changi",   iata: "SIN", lat:   1.3644, lon:  103.9915 },
					to:   { name: "London Heathrow",    iata: "LHR", lat:  51.4775, lon:   -0.4614 }
				},
				{
					travelerName:  "The Hobbit Family",
					flightNumber:  "BA1477",
					departureDate: "2026-06-20",
					from: { name: "London Heathrow",    iata: "LHR", lat:  51.4775, lon:  -0.4614 },
					to:   { name: "Inverness Airport",  iata: "INV", lat:  57.5425, lon:  -4.0475 }
				}
    ]
  }
}
```

---

### Scenario 3: World Cup 2026 — Multiple Fan Groups

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 3,
    showFlightTracks: "auto",
    tripTitle: "Boston - World Cup 2026",
    flightAwareApiKey: "YOUR_API_KEY_HERE",
    zoomLevel: 2,
    zoomLongitude: -80,
    zoomLatitude: 30,
    destination: { name: "New York", iata: "JFK", lat: 40.6413, lon: -73.7781 },
    travelers: [
      {
        name: "Guest Name 1",
        flights: [
          { flightNumber: "BA0117", departureDate: "2026-06-10",
            from: { name:"London LHR",   iata:"LHR", lat:51.4775,  lon:-0.4614  },
            to:   { name:"New York JFK", iata:"JFK", lat:40.6413,  lon:-73.7781 } }
        ],
        returnFlights: [
          { flightNumber: "BA0116", departureDate: "2026-06-20",
            from: { name:"New York JFK", iata:"JFK", lat:40.6413,  lon:-73.7781 },
            to:   { name:"London LHR",   iata:"LHR", lat:51.4775,  lon:-0.4614  } }
        ]
      },
      {
        name: "Guest Name 2",
        flights: [
          { flightNumber: "QF0108", departureDate: "2026-06-08",
            from: { name:"Melbourne",    iata:"MEL", lat:-37.6733, lon:144.8431 },
            to:   { name:"Los Angeles",  iata:"LAX", lat:33.9416,  lon:-118.408 } },
          { flightNumber: "AA0002", departureDate: "2026-06-09",
            from: { name:"Los Angeles",  iata:"LAX", lat:33.9416,  lon:-118.408 },
            to:   { name:"New York JFK", iata:"JFK", lat:40.6413,  lon:-73.7781 } }
        ],
        returnFlights: []
      }
    ]
  }
}
```

### Scenario 4: Where I Have Been — Destinations & Crests

Displays a collection of all previously visited destinations. 

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 4,
    showFlightTracks: "test",
    showWhereIHaveBeen: true,
    showFlightTracks: "test", // Required to see tracks in Scenario 4
    tripTitle: "My Past Travels",
    home: "LHR",
    flights: [
      { to: "JFK", departureDate: "2023-05-10" }, // IATA Code
      { to: "San Francisco", departureDate: "2023-08-15" }, // City Name
      { to: "Manchester United", departureDate: "2024-01-10" }, // Football Team
      { to: { name: "Remote Cabin", lat: 64.1265, lon: -21.8174 }, departureDate: "2024-02-01" } // Coordinates
    ]
  }
}
```

---

### Scenario 5: Aircrew / Frequent Flyer CSV Roster

Reads flight legs from a plain CSV file. No arrays in `config.js` — just edit the CSV.

```js
{
  module: "MMM-iAmGoingThere",
  position: "fullscreen_below",
  config: {
    scenario: 5,
    showFlightTracks: "auto",
    tripTitle: "Alex Reid — Crew Schedule",
    flightAwareApiKey: "YOUR_API_KEY_HERE",
    crewFlightsFile: "data/my_flights.csv",
    home: { name: "London Heathrow", iata: "LHR", lat: 51.4775, lon: -0.4614 },
    showFlightDetails: true,
    showFlightTracks: "auto"
  }
}
```

See `data/my_flights.csv` for the sample file format and column definitions.

---

### Scenario 6: Football European Away Days

New CSV-driven scenario specifically for tracking football fixtures at stadium locations.

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

See `data/footballAwayTrips.csv` for the sample file format and column definitions.

---

- **Home location** is marked with a **Gold** target.
- **Visited destinations** are marked with **White** targets.
- **Football Team Crests** — If a destination is resolved via a football team name, the standard white marker is replaced by the team's official crest image (from `images/crests/[Country]/`).

---

### Master Configuration — The "All-in-One" Approach (v1.8.0+)

The **Master Configuration** allows you to define all 6 scenarios simultaneously within a single module block. This is the most powerful way to use the module, as it enables instant switching between trip types using the on-screen Scenario Selector without editing any files.

When using the `scenarios` object, the module will merge your top-level "global" config with the active scenario's specific fields.

#### Example: Master Configuration with 6 Scenarios

```js
{
			module: "MMM-iAmGoingThere",
			position: "fullscreen_below",
			config: {
				scenario: 1, // Default starting scenario
				showScenarioSelector: true, // REQUIRED for on-screen switching
				showMapSelector: true,
				flightAwareApiKey: "YOUR_API_KEY",
				home: "EDI",
				
				scenarios: {
				// 1: FAO Holiday (Scenario 1)
				"1": {
					tripTitle: "FAO Holiday",
					flights: [
					{ flightNumber: "EZY3311", departureDate: "2026-04-06", from: "EDI", to: "FAO" },
					{ flightNumber: "EZY3312", departureDate: "2026-04-11", from: "FAO", to: "EDI" }
					]
				},

				// 2: Off to Oz (Scenario 2 - Multi-leg RTW)
				"2": {
					tripTitle: "Off to Oz",
					flights: [
					{ travelerName: "The Hobbits", flightNumber: "VS19", departureDate: "2026-05-04", from: "LHR", to: "SFO" },
					{ travelerName: "The Hobbits", flightNumber: "FJ871", departureDate: "2026-05-06", from: "SFO", to: "NAN" },
					{ travelerName: "The Hobbits", flightNumber: "FJ411", departureDate: "2026-05-11", from: "NAN", to: "AKL" },
					{ travelerName: "The Hobbits", flightNumber: "NZ0617", departureDate: "2026-05-16", from: "AKL", to: "ZQN" },
					{ travelerName: "The Hobbits", flightNumber: "NZ231", departureDate: "2026-05-20", from: "ZQN", to: "SYD" },
					{ travelerName: "The Hobbits", flightNumber: "SQ232", departureDate: "2026-05-22", from: "SYD", to: "SIN" },
					{ travelerName: "The Hobbits", flightNumber: "SQ322", departureDate: "2026-05-23", from: "SIN", to: "LHR" }
					]
				},

				// 3: World Cup 2026 - Boston (Scenario 3 - Multi-origin)
				"3": {
					tripTitle: "World Cup 2026 - Boston",
					travelers: [
					{
						name: "John",
						flights: [
						{ flightNumber: "FR1677", departureDate: "2026-06-10", from: "EDI", to: "SNN" },
						{ flightNumber: "UA289", departureDate: "2026-06-11", from: "SNN", to: "ORD" },
						{ flightNumber: "UA1693", departureDate: "2026-06-11", from: "ORD", to: "BOS" }
						]
					},          
					{
						name: "Michael", 
						flights: [
						{ flightNumber: "UA951", departureDate: "2026-06-11", from: "BRU", to: "BOS" }
						] 
					},
					{ name: "Brendan", 
					flights: [
						{ flightNumber: "LX52", departureDate: "2026-06-11", from: "ZRH", to: "BOS" }
						] 
					}
					]
				},

				// 4: Where I Have Been (Scenario 4 - Destinations & Crests)
				"4": {
					tripTitle: "We Have Been Here",
					showWhereIHaveBeen: true,
					flights: [
					{ to: "Real Madrid", departureDate: "2024-01-10" },
					{ to: "Bayer Leverkusen", departureDate: "2024-01-10" },
					{ to: "Manchester United", departureDate: "2024-01-10" },
					{ to: "Barcelona", departureDate: "2024-01-10" },
					{ to: "LHR", departureDate: "2025-05-10" }
					]
				},

				// 5: Amelia Earhart's Crew Schedule (Scenario 5 - CSV Roster)
				"5": {
					tripTitle: "Amelia Earhart's Crew Schedule",
					crewFlightsFile: "data/my_flights.csv"
				},

				// 6: Football Away Days (Scenario 6 - CSV Roster)
				"6": {
					tripTitle: "Football European Away Days",
					footballAwayTripsFile: "data/footballAwayTrips.csv",
					showFlightDetails: true,
					showFlightTracks: "auto"
				}
				}
			}
		}
```

---

## All Configuration Options

### 1. Scenario & Core
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `scenario` | `Number` | `1` | Trip type: `1`=round trip, `2`=multi-leg RTW, `3`=multi-origin, `4`=Where I have been, `5`=CSV crew roster, `6`=CSV football trips |
| `showWhereIHaveBeen` | `Boolean` | `false` | Scenario 4: If `true`, the module generates return flights from Home to each destination |
| `tripTitle` | `String` | `"Our Destination"` | Text appended to the "We Are On Our Way To –" title |
| `overideDate` | `Boolean` | `false` | Debug: Set all flights takeoff time to now + 5 minutes for this session only |
| `departureAlertHours` | `Number` | `0` | Hours before first departure to send notification (0 = disabled) |

### 2. FlightAware AeroAPI
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `flightAwareApiKey` | `String` | `""` | FlightAware AeroAPI key (required for live tracking) |
| `pollInterval` | `Number` | `5` | Minutes between FlightAware API polls |

### 3. Map Settings
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mapHeight` | `Number` | `700` | Map height in pixels |
| `mapProjection` | `String` | `"mercator"` | Default projection: `"mercator"`, `"naturalEarth1"`, `"equirectangular"`, `"orthographic"`, `"stereographic"` |
| `hideIceCaps` | `Boolean` | `false` | If `true`, the polar ice cap regions (Antarctica) are hidden on all projections except `"orthographic"` (Globe) |
| `zoomLevel` | `Number` | `1` | amCharts 5 zoom level (`1` = full world) |
| `zoomLongitude` | `Number` | `0` | Map centre longitude |
| `zoomLatitude` | `Number` | `20` | Map centre latitude |
| `autoRotateGlobeToPlane` | `Boolean` | `false` | Orthographic projection: rotate globe to keep active plane(s) centered |
| `gcPoints` | `Number` | `100` | Great-circle interpolation points per leg |
| `displayDesc` | `Boolean` | `true` | Show airport name labels on markers |
| `showCityInfo` | `Boolean` | `false` | Show city name and local time overlay |
| `citiesFile` | `String` | `"data/cities.csv"` | Path to cities CSV data file |
| `cityInfoMode` | `String` | `"destination"` | `"destination"` or `"layovers"` (cycle through stopovers) |
| `cityInfoCycleInterval` | `Number` | `20` | Seconds per city when `cityInfoMode = "layovers"` |
| `narrowBreakpoint` | `Number` | `900` | Screen width (px) below which both overlay panels switch to `95vw` stacked layout |

### 4. Graticule Grid
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `showGraticule` | `Boolean` | `false` | Show latitude/longitude grid lines on the map |
| `colorGraticule` | `String` | `"#ffffff"` | Hex color for the graticule lines |
| `graticuleOpacity` | `Number` | `0.2` | Opacity of the graticule lines (0.0 to 1.0) |
| `graticuleWidth` | `Number` | `0.5` | Stroke width of the graticule lines |
| `graticuleStep` | `Number` | `10` | Frequency of graticule lines in degrees (e.g. 10°) |

### 5. Sub-national Regions
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `showSubnationalRegions` | `Boolean` | `false` | Enable layered map polygons for sub-national regions (states, provinces, etc.) |
| `subnationalAllCountries`| `Boolean` | `false` | If `true`, enables sub-national regions for ALL supported countries (~130+) |
| `subnationalCountries` | `Array` | `[]` | List of ISO-2 codes to show regions for, e.g. `["US", "CA", "GB"]` |

### 6. UI Controls (Onscreen)
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `showPanControl` | `Boolean" | `true` | Show on-screen pan arrows and compass |
| `showZoomControl` | `Boolean` | `true` | Show on-screen + and - zoom buttons |
| `showNudgeControl` | `Boolean` | `true` | Show on-screen directional arrows for nudging the map position |
| `showProjectionSelector` | `Boolean` | `true` | Show map projection dropdown (top-left) |
| `showVisitedSelector` | `Boolean` | `true` | Show the Highlights Control dropdown (top-left) |
| `showModeSelector` | `Boolean` | `true` | Show mode selector (Auto/Test) (top-right) |
| `showScenarioSelector` | `Boolean` | `true` | Show scenario dropdown (top-right) |
| `showMapSelector` | `Boolean` | `true` | Legacy alias: toggles both Projection and Visited selectors |
| `hideControlsUntilHover` | `Boolean` | `false` | If `true`, all on-screen controls are hidden until the mouse hovers over the map |

### 7. Flight Details Overlay
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `showFlightDetails` | `Boolean" | `false` | Show the overlay flight status table |
| `autoHideOverlays` | `Boolean" | `false` | If `true`, the flight table and city info panels fade out after inactivity |
| `autoHideDelay` | `Number" | `30` | Seconds to wait before fading out overlay panels |
| `flightPanelWidth` | `String" | `"46vw"` | CSS width of the flight status overlay panel |
| `flightPanelHeight` | `String" | `"32vh"` | CSS height of the flight status overlay panel |
| `setFlightDetailsTextSize` | `String" | `"xsmall"` | Font size for the flight table |
| `showTable` | `Boolean" | `false` | Legacy alias for `showFlightDetails` |
| `tableX` | `Number" | `0` | px from left edge of map |
| `tableY` | `Number" | `0` | px from bottom edge of map |

### 8. Attractions Overlay
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `showAttractionsDetails` | `Boolean" | `false` | Show Top 10 city attractions overlay |
| `attractionsPanelWidth` | `String" | `"50vw"` | CSS width of the attractions overlay panel |
| `attractionsPanelHeight` | `String" | `"32vh"` | CSS height of the attractions overlay panel |
| `setAttractionsDetailsTextSize` | `String" | `"xsmall"` | Font size for the attractions panel |
| `maxAttractionsDisplay` | `Number" | `5` | Maximum number of attractions to display per page |
| `attractionsAutoScroll` | `Boolean" | `false` | When `true`, page-flips the attractions list |
| `attractionsScrollInterval` | `Number" | `3` | Seconds each page is displayed before flipping |
| `autoRotateAttractionsData` | `Boolean" | `false` | Auto-rotate attractions to destination when trip completes |
| `cityAttractions_Xaxis` | `Number" | `0` | px from left edge of map |
| `cityAttractions_Yaxis" | `Number" | `0` | px from bottom edge of map |

### 9. Flight Tracking & Animation
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `showFlightTracks` | `String" | `"auto"` | `"auto"` (live), `"true"` (static), `"false"` (hidden), or `"test"` (animation) |
| `flightDisplayMode` | `String" | `"all"` | Filter legs: `"all"` \| `"outbound"` \| `"return"` |
| `testModeDuration` | `Number" | `3` | Seconds per leg in test animation |
| `testModeDelay" | `Number" | `3` | Seconds pause between legs in test animation |
| `animationEnabled" | `Boolean" | `true` | Show live plane icon on active leg |
| `pauseDuration" | `Number" | `3.0` | Pause duration for animation |
| `animationDuration" | `Number" | `10.0` | Speed of plane animation |
| `showPlaneShadow" | `Boolean" | `true` | Render a white halo beneath the plane icon |

### 10. Airport & Destination Markers
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `showDestinations" | `Boolean" | `true` | Show airport destination markers on the map |
| `tooltipDuration" | `Number" | `6` | Seconds tooltip stays visible |
| `colorAirportHome" | `String" | `"#FFD700"` | Home airport marker colour (gold) |
| `colorAirportOther" | `String" | `"#FFFFFF"` | Other airport marker colour |

### 11. Colours (Map & Paths)
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `colorMapBackground" | `String" | `"#000000"` | Color of the area outside the map projection |
| `colorMapOcean" | `String" | `"#1A1A2E"` | Color of the ocean fill inside the map projection |
| `colorCountries" | `String" | `"#2C3E50"` | Map country fill colour |
| `colorCountryBorders" | `String" | `"#1A252F"` | Map border colour |
| `colorVisitedCountry" | `String" | `"#00AA44"` | Fill colour for visited countries |
| `colorVisitedCountryBorder"| `String" | `"#008833"` | Border colour for visited countries |
| `colorVisitedCountryOpacity"| `Number" | `0.75` | Opacity of the visited country fill (0.0–1.0) |
| `colorFuturePath" | `String" | `"#FFFFFF"` | Scheduled leg colour |
| `colorActivePath" | `String" | `"#4499FF"` | In-flight leg colour |
| `colorCompletedPath" | `String" | `"#00CC66"` | Landed leg colour |
| `colorPreviousPath" | `String" | `"#888888"` | Superseded-landed leg colour (grey) |
| `colorCancelledPath" | `String" | `"#FF4444"` | Cancelled leg colour |
| `colorPlane" | `String" | `"#FF6644"` | Live plane icon colour |
| `colorTitleFont" | `String" | `"#FFFFFF"` | Main title font colour |
| `colorLegendFont" | `String" | `"#FFFFFF"` | Legend font colour |
| `colorLegendBorder" | `String" | `"#FFFFFF"` | Legend border colour |
| `colorBlindMode" | `Boolean" | `false` | When `true`, differentiates path status via `dashLength` |
| `colorResetAfterDays" | `Number" | `1` | Days after final landing before paths reset to white |

### 12. Data Sources
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `home" | `Object" | see defaults | Home airport `{ name, iata, lat, lon }` |
| `destination" | `Object" | `null` | Primary destination airport object |
| `flights" | `Array" | `[]` | Leg objects for Scenario 1, 2 & 4 |
| `travelers" | `Array" | `[]` | Traveler objects for Scenario 3 |
| `crewFlightsFile" | `String" | `"data/my_flights.csv"` | Scenario 5: CSV flight roster path |
| `footballAwayTripsFile" | `String" | `"data/footballAwayTrips.csv"` | Scenario 6: football trips CSV path |

---

## Sub-national Regions (v2.1.0+)

The module supports high-detail sub-national region layers (states, provinces, departments, etc.) for **130+ countries**.

### Enabling Regions

1. Set `showSubnationalRegions: true`.
2. Choose which countries to show:
   - **All countries**: Set `subnationalAllCountries: true`. This is the easiest way to see regions everywhere they are available.
   - **Specific countries**: Add ISO-2 codes to the `subnationalCountries` array, e.g., `["US", "CA", "GB", "DE"]`.

### Supported Countries include:

- **Europe**: GB (UK - includes England, Scotland, Wales, NI), DE (Germany), FR (France), IT (Italy), ES (Spain), etc.
- **Americas**: US (USA), CA (Canada), BR (Brazil), MX (Mexico), etc.
- **Asia**: CN (China), IN (India), JP (Japan), RU (Russia), etc.
- **Oceania**: AU (Australia), NZ (New Zealand).
- **Africa**: ZA (South Africa), NG (Nigeria), EG (Egypt), etc.

> **Note on the UK:** To see regions for England, Scotland, Wales, or Northern Ireland, use the **GB** country code. The module automatically maps these names to GB.

---

## Visited Countries — Highlights Control

When `showVisitedSelector: true`, a **Highlights Control** dropdown is displayed in the top-left corner of the map, directly below the Map Projection selector.

| Dropdown option | Effect |
|-----------------|--------|
| **Show Graticule Lines** | Displays latitude/longitude grid lines on the map |
| **Hide Graticule Lines** | Hides latitude/longitude grid lines |
| **Highlight Visited Countries** *(default)* | Green highlights shown for all visited countries |
| **No Highlights** | All highlights suppressed (display-only; no data is deleted). Persists until option is changed or module restarts |
| **Clear Manually Marked Cache** | Wipes `data/manual_visited_countries.json`; reverts dropdown to "Highlight Visited Countries" |
| **Show Sub Regions** | Shows internal borders (states, provinces, etc.) for supported countries |
| **Hide Sub Regions** | Hides internal borders (states, provinces, etc.) |

### Right-click popup (all scenarios)

Right-clicking any country polygon opens a confirmation popup:
- Shows the **country name** and **current visited status**
- **"Mark as Visited"** — adds to `manual_visited_countries.json`
- **"Remove Visited"** — removes from `manual_visited_countries.json`
- **"Cancel"** — closes without changes
- Auto-dismisses after **5 seconds**

Manual marks are applied in all six scenarios. Automatic country detection from flight destinations applies to **Scenario 4 only**.

> Full details: [Mark Country As Visited Guide](./Mark_Country_As_Visited_Guide.md)

---

## Table Position

The overlay table can be placed anywhere on the map:

```js
showFlightDetails: true,
tableX: 10,    // px from left edge
tableY: 10,    // px from bottom edge
```

Common positions:
- Top-left:     `tableX: 10,  tableY: 500`
- Top-right:    `tableX: 600, tableY: 500`
- Bottom-left:  `tableX: 10,  tableY: 10`

---

## Flight Display Mode

`flightDisplayMode` filters which legs appear on both the map and the overlay table.
Useful when you only want to watch the outbound journey while you're traveling, for example.

```js
flightDisplayMode: "all",       // default — show every leg
flightDisplayMode: "outbound",  // only outbound legs
flightDisplayMode: "return",    // only return legs
```

---

## Same-Day Multi-Leg Sorting (`departureTime`)

When two or more legs share the same `departureDate`, add the optional `departureTime` field (`"HH:MM"`) to ensure correct ordering in the test animation and the flight table:

```js
flights: [
  { flightNumber: "BA1478", departureDate: "2026-05-20", departureTime: "07:30", from: "INV", to: "LHR" },
  { flightNumber: "BA0283", departureDate: "2026-05-20", departureTime: "11:15", from: "LHR", to: "SFO" }
]
```

Without `departureTime`, same-date legs are sorted alphabetically by flight number.

---

## Departure Alert

Set `departureAlertHours` to fire a `IAGT_DEPARTURE_ALERT` MagicMirror notification before your first flight:

```js
departureAlertHours: 24,   // alert 24 hours before departure
```

The notification payload sent to all other modules:
```js
{
  flightNumber:  "BA0117",
  departureDate: "2026-06-10",
  from:          { name: "London Heathrow", iata: "LHR", lat: 51.4775, lon: -0.4614 },
  to:            { name: "New York JFK",    iata: "JFK", lat: 40.6413, lon: -73.7781 },
  hoursUntil:    24
}
```

Any other module can respond by implementing `notificationReceived`:
```js
notificationReceived(notification, payload) {
  if (notification === "IAGT_DEPARTURE_ALERT") {
    // e.g. speak an announcement, show a banner, etc.
  }
}
```

Set to `0` (default) to disable.

---

## City Attractions

Each city in `data/cities.csv` maps to a JSON file in `data/attractions/`.
The `attractionsFile` column contains the JSON filename (e.g. `new_york.json`).

JSON format:
```json
{
  "city": "City Name",
  "country": "Country",
  "things": [
    { "rank": 1, "name": "Attraction Name", "description": "Short description" },
    { "rank": 2, "name": "Another Attraction", "description": "..." }
  ]
}
```

Control how many items are shown per page with `maxAttractionsDisplay` (default `5`).
Enable automatic page-flipping with `attractionsAutoScroll: true` and set the time per page with `attractionsScrollInterval` (seconds, default `3`).

---

## Save / Print to File

Both overlay panels include a clickable **🖨 printer icon** button that saves a formatted, printable HTML file to disk.

### City Attractions — Save Button

The 🖨 button appears in the attractions panel header, beside the city name.

| Detail | Value |
|--------|-------|
| Output folder | `documents/MySavedCityAttractions/` |
| Filename pattern | `[city-slug]_YYYY-MM-DD-HHMM.html` |
| Example | `new_york_2026-06-10-1430.html` |

The file contains a styled three-column table (**#**, **Attraction**, **Description**) for all items in the displayed city's attractions list.

The folder is created automatically if it does not exist.

### Flight Details — Save Button

The 🖨 button appears in the flight data overlay title row, to the right of the "Flight Details" heading.

| Detail | Value |
|--------|-------|
| Output folder | `documents/MySavedFlight/` |
| Filename pattern | `flights_YYYY-MM-DD-HHMM.html` |
| Example | `flights_2026-06-10-0930.html` |

The file contains a six-column table (**Name**, **Flight**, **Date / Time**, **From**, **To**, **Status**) for all flight legs. Legs are sorted:
- **Scenario 3**: grouped by traveler name (alphabetical), then ascending departure date/time within each group.
- **Scenarios 1 & 2**: ascending departure date/time only.

The folder is created automatically if it does not exist.

### Button Feedback States

| State | Button text | Colour |
|-------|------------|--------|
| Idle | 🖨 | Blue |
| Saving | ⏳ | — (disabled) |
| Success | ✓ | Green (resets to 🖨 after 3 s) |
| Error | ✗ | Red (resets to 🖨 after 3 s) |

### Airport Tooltip Fix

Airport marker tooltips now remain visible while the mouse hovers over the marker label. Previously they flickered because the tooltip balloon element intercepted mouse events and triggered a hide/reappear loop. This is fixed automatically via CSS and requires no configuration.

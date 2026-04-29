# Troubleshooting MMM-iAmGoingThere

If you encounter issues with the module, please check this guide first.

---

## General Troubleshooting

### 1. API Keys & Data
- **FlightAware AeroAPI Key**: Ensure your key is valid and has remaining credits. The module uses AeroAPI v4.
- **Poll Interval**: If you are hitting rate limits, increase `pollInterval` (default is 5 minutes).
- **Date/Time**: Ensure your MagicMirror system time is correct. Flight tracking depends on accurate UTC comparisons.

### 2. Map & Display
- **Black Map**: If the map doesn't appear, check the browser console (`Ctrl+Shift+I` in Electron) for errors. Usually caused by missing dependencies or invalid JSON in `config.js`.
- **Crest Images**: If club crests are missing, ensure they are located in `modules/MMM-iAmGoingThere/images/crests/[Country]/[Club].png`. Country folders should use underscores for spaces (e.g., `The_Netherlands`).
- **White Circle Markers**: If a crest image is not found, the module falls back to a white circle with a blue border.

### 3. CSV Formatting
- **UTF-8 Encoding**: Ensure all CSV files (`cities.csv`, `my_flights.csv`, `footballAwayTrips.csv`) are saved with UTF-8 encoding.
- **BOM (Byte Order Mark)**: The module handles UTF-8 BOM, but plain UTF-8 is preferred.
- **Line Endings**: Use Unix (LF) or Windows (CRLF) line endings.

---

## Scenario-Specific Advice

### Scenario 1 & 2: Round Trip / Multi-Leg
- **IATA Codes**: If a path doesn't appear, verify the IATA codes in `flights` match those in `data/airports.csv`.
- **Departure Dates**: Format must be `YYYY-MM-DD`.

### Scenario 3: Multi-Origin
- **Unique Colors**: Each traveler is assigned a color. If you have many travelers, colors may repeat.
- **Flight Visibility**: Ensure each traveler has at least one outbound flight.

### Scenario 4: Where I Have Been
- **Missing Markers**: If a destination name doesn't resolve to a marker, check if it exists in `data/cities.csv` (city name) or `data/football_teams_database.csv` (team name).
- **Paths**: Paths only show in "test" mode (`showFlightTracks: "test"`).

### Scenario 5: Aircrew Roster
- **CSV Path**: Ensure `crewFlightsFile` points to the correct relative path from the module root.
- **Columns**: Verify the header names match: `departureDate`, `flightNumber`, `from`, `to`.

### Scenario 6: Football Away Days
- **Unresolved Teams**: Check the logs (`pm2 logs` or terminal) for "could not resolve team" warnings. Try matching the name exactly as it appears in `data/football_teams_database.csv`.
- **Unicode Matching**: The module handles some common accents (e.g., ø, ö, é), but it's best to use the name from the database.
- **Tooltip Aggregation**: If multiple visits to the same stadium occur, they are grouped into a single marker. Hover over the marker to see the full fixture history.
- **Crest Sizing**: Crests are rendered at 50% scale (17x17px) to maintain map clarity for dense fixture lists.

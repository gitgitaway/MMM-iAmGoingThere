# MMM-iAmGoingThere — API Rate Limit Mitigation Guide

This guide outlines the measures implemented to prevent exceeding the FlightAware AeroAPI rate limits across all four trip scenarios.

## Overview

The module uses the FlightAware AeroAPI v4 to track live flight status. To conserve API credits and stay within rate limits, the following strategies are employed:

| Strategy | Implementation | Benefit |
|----------|----------------|---------|
| **Scenario Filtering** | Polling is disabled for Scenario 4 ("Where I Have Been"). | Prevents pointless calls for historical data. |
| **Temporal Gating** | Polling only starts within 12 hours of scheduled departure. | Saves credits for flights days or weeks away. |
| **Status-Aware TTL** | Active flights use 1-minute cache; scheduled flights use 15-minute cache. | Balances real-time accuracy with credit conservation. |
| **Sequential Delay** | A 2-second pause is enforced between requests in a single poll cycle. | Prevents "burst" violations of per-second rate limits. |
| **ETag Caching** | Supports `If-None-Match` headers. | Reduces bandwidth and processing overhead. |
| **Failure Back-off** | Exponential back-off for flights that return errors. | Prevents hammering the API when a flight ident is invalid or service is down. |

---

## Scenario-Specific Measures

### Scenario 1 — Standard Round Trip
- Polling is restricted to the outbound leg until it lands, then shifts to the return leg.
- Since there are only 2 legs, the risk of exhaustion is low.

### Scenario 2 — Multi-Leg / Round The World
- Polling is focused only on the **next upcoming leg** and any currently **active** leg.
- Legs scheduled more than 12 hours in the future are ignored during the current cycle.

### Scenario 3 — Multi-Origin Group Trips
- **High Risk**: This scenario can involve many simultaneous travelers.
- Sequential request queuing is critical here. The module processes travelers one by one with a delay to avoid burst limits.
- If a traveler's trip is entirely in the past or far future, they are skipped entirely.

### Scenario 4 — Where I Have Been
- **Zero Polling**: Since this scenario tracks past travels, live API polling is disabled. Coordinates are resolved once from local databases (`airports.csv`, `cities.csv`, `football_teams_database.csv`).

---

## Technical Configuration

### `pollInterval`
Default: `5` minutes.
- Increasing this to `10` or `15` is recommended for large Scenario 3 groups on free-tier API accounts.

### `colorResetAfterDays`
Default: `1` day.
- Once the final leg lands and this period elapses, the module stops all polling for the trip.

## Monitoring

Check your MagicMirror logs for "AeroAPI HTTP 429" errors. If these appear, increase your `pollInterval` or reduce the number of travelers in Scenario 3.

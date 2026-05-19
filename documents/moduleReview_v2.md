# Module Review v2 — MMM-iAmGoingThere

**Review Date**: 2026-03-30  
**Based On**: v1.2.1 codebase  
**Previous Review**: `moduleReview _v1.md` (v0.4.0 cycle — 23 findings, all resolved by v1.1.2)

---

## Prior Recommendations Status Summary

All 23 items from the v1 review have been fully resolved:

| Batch | Items | Status |
|-------|-------|--------|
| Stage 1 — Critical Fixes (v0.4.1) | SEC-001, PERF-001, PERF-002, PERF-003, UX-001 | ✅ All resolved |
| Stage 2 — Security & Performance (v0.5.0) | SEC-002, SEC-003, SEC-004, PERF-004, PERF-006, UX-003, UX-005 | ✅ All resolved |
| Stage 3 — UI/UX Polish (v0.6.0) | UX-002, UX-004, UX-006, UX-008, UX-009, UX-010, UX-011 | ✅ All resolved |
| Stage 4 — Architecture (v0.7.0) | UX-007, UX-012, PERF-007, PERF-005 | ✅ All resolved |

---

## New Findings (v2 Review Cycle)

This review was conducted across three parallel specialised passes: **verification + correctness**, **security + memory + robustness**, and **UI/UX + performance innovation**.

---

### Security

| Ref | File | Line | Issue | Criticality | Status |
|-----|------|------|-------|-------------|--------|
| NEW-01 | `MMM-iAmGoingThere.js` | ~1412 | **XSS via `leg.aircraftType` in detail chip** — newly added detail chip concatenated `leg.aircraftType` directly into `innerHTML` without `this._esc()`, allowing a malicious AeroAPI response to inject HTML. | 🔴 CRITICAL | ✅ Fixed v1.2.1 |
| NEW-13 | `node_helper.js` | ~469 | **API error log leaks key** — the `console.warn` in the polling catch block included the full error object. If `e.message` contains request headers (some HTTP clients include them), the AeroAPI key could appear in logs. The warning should log only `e.message`, not the full object. | 🟡 MEDIUM | ✅ Fixed v1.3.0 |

---

### Memory / Resource Leaks

| Ref | File | Line | Issue | Criticality | Status |
|-----|------|------|-------|-------------|--------|
| NEW-02 | `MMM-iAmGoingThere.js` | `stop()` | **amCharts 5 `_mapRoot` not disposed** — `stop()` does not call `this._mapRoot.dispose()`. amCharts 5 roots hold WebGL contexts, `requestAnimationFrame` loops, DOM references, and event listeners. Without `dispose()`, every MagicMirror hot-reload or module restart leaks these resources permanently. | 🔴 CRITICAL | ✅ Fixed v1.3.0 |
| NEW-03 | `MMM-iAmGoingThere.js` | `stop()` | **`_overlayHideTimer` not cleared in `stop()`** — The auto-hide feature uses `this._overlayHideTimer = setTimeout(...)`. If the module is stopped while the timer is pending, the callback fires after `stop()`, accessing stale DOM nodes. `clearTimeout(this._overlayHideTimer)` must be added to `stop()`. | 🟡 MEDIUM | ✅ Fixed v1.3.0 |

---

### Correctness / Broken Features

| Ref | File | Line | Issue | Criticality | Status |
|-----|------|------|-------|-------------|--------|
| NEW-04 | `MMM-iAmGoingThere.js` | ~299 | **`cityAttractions_Xaxis` / `_Yaxis` silently broken** — config options were declared and documented but `getDom()` hardcoded `"0"` instead of reading from `this.config`, so the attractions panel could not be repositioned at all. | 🟠 HIGH | ✅ Fixed v1.2.1 |
| NEW-05 | `node_helper.js` | ~593 | **Date params stripped from AeroAPI URL** — the `?start=` / `?end=` date-scoping query parameters were missing from `fetchFlightStatus()`. Without them, AeroAPI returns multiple flights across many dates for the same flight number; `updateLegFromAPI()` attempts a date-match fallback but it relies on `scheduled_out` matching `leg.departureDate`, which is unreliable for red-eye or date-boundary flights. | 🟠 HIGH | ✅ Fixed v1.2.1 |
| NEW-06 | `node_helper.js` | `updateLegFromAPI()` | **Gate `0` treated as absent** — `flight.gate_origin || null` uses falsy coercion, so gate `"0"` (a valid gate number at some airports) is silently converted to `null` and never displayed. Should use `flight.gate_origin != null ? flight.gate_origin : null` (null-check, not falsy). | 🟢 LOW | ✅ Fixed v1.3.1 |
| NEW-10 | `MMM-iAmGoingThere.js` | ~790 | **Plane tooltip `\n` renders as collapsed whitespace in amCharts 5** — the `tooltipText` for the plane bullet is assembled with `\n` joins. amCharts 5 SVG tooltips do not treat `\n` as a line break; the text renders as a single line with spaces. The correct amCharts 5 line-break separator is `[/]` or explicit `\n` escaped as the library's `{newLine}` token. | 🟡 MEDIUM | ✅ Fixed v1.3.1 |

---

### Performance

| Ref | File | Line | Issue | Criticality | Status |
|-----|------|------|-------|-------------|--------|
| NEW-07 | `MMM-iAmGoingThere.js` | `_initPointSeries()` | **`PERF-006` debounce incomplete** — `_validateTimer` placeholder was added but no debounce logic was wired. `_planeSeries.data.setAll()` and `_mapLineSeries.data.setAll()` in `updateMapLines()` fire synchronously on every call. A 250 ms `clearTimeout` / `setTimeout` wrapper must be added around the `data.setAll()` calls for these two series. | 🟡 MEDIUM | ⬜ Open |
| NEW-08 | `node_helper.js` | `pollAllFlights()` | **Sequential 2-second sleep inflates poll cycles** — between each flight poll the helper `await`s a 2-second sleep. For a 3-traveler Scenario 3 trip with 6 legs, the poll loop takes at minimum 12 seconds to complete. If `pollInterval` is set to 5 minutes the effective cadence per flight is 5m + 12s. For larger trip configs this could push polls well outside the intended interval. Consider parallel polling with `Promise.allSettled()` where quota allows. | 🟡 MEDIUM | ⬜ Open |
| NEW-09 | `node_helper.js` | `_apiCache` | **Unbounded cache growth** — `_apiCache` is a plain object keyed by `flightNumber_date`. Entries are updated with a `ts` timestamp but never deleted. Across a month-long multi-leg trip, every polled flight accumulates an entry that is never evicted, growing indefinitely. A simple TTL-based eviction on every poll cycle (remove entries older than 1 hour) would prevent this. | 🟡 MEDIUM | ⬜ Open |
| NEW-11 | `node_helper.js` | `pollAllFlights()` | **No adaptive polling** — poll interval is fixed at `pollInterval` minutes regardless of flight phase. A flight that landed 2 hours ago is polled at the same frequency as one that departed 10 minutes ago. A phase-aware strategy (5 min pre-departure, 1 min en-route, 10 min post-landing, 30 min next-day) would dramatically reduce API quota consumption without sacrificing real-time accuracy. | 🟡 MEDIUM | ⬜ Open |

---

### UX / Innovation

| Ref | Area | Issue / Opportunity | Priority |
|-----|------|---------------------|----------|
| NEW-12 | Plane Animation | **Smooth plane motion tweening** — the plane bullet jumps to new coordinates on each `_planeSeries.data.setAll()`. amCharts 5 supports interpolated `animate()` transitions on data items. Adding position tweening at ~1-second intervals would produce a realistic smooth glide instead of discrete position hops. | 🟡 MEDIUM |
| NEW-14 | Connection Risk | **Connection risk indicator** — when a multi-leg journey has a layover under 90 minutes and the inbound leg is delayed, the module has enough data to compute a connection risk. A ⚠ amber badge in the flight table row for the connecting leg would be highly actionable. | 🟡 MEDIUM |
| NEW-15 | Status Badge | **Delayed flight badge** — when `scheduledDeparture` and `estimatedDeparture` are both present and the estimated is > 15 minutes later, render a `+Nm` delay badge in amber in the flight table status cell. This gives at-a-glance delay awareness without needing to read timestamps. | 🟡 MEDIUM |
| NEW-16 | Countdown | **Countdown action box** — the countdown box currently shows days remaining. When the departure is within 24 hours, it could show gate, terminal, and estimated departure time in a high-visibility "check-in" layout, replacing the generic countdown with immediately actionable boarding information. | 🟢 LOW |
| NEW-17 | Responsive Layout | **Responsive breakpoints** — the overlay panel widths (`flightPanelWidth`, `attractionsPanelWidth`) are fixed `vw` values. On portrait-mode or narrow displays (e.g. a 7" RPi display), the panels overlap. A CSS custom property approach combined with a `@media` rule for narrow viewports would handle this automatically. | 🟢 LOW |
| NEW-18 | Weather Staleness | **Stale destination weather indicator** — the weather fetch runs once at startup. There is no visible indicator of when the weather data was last refreshed, and no re-fetch on a long-running mirror session. A last-updated timestamp below the weather reading and an hourly background refresh would prevent stale data from misleading users on multi-day displays. | 🟢 LOW |

---

## Full Findings Summary

| Ref | Area | One-line description | Criticality | Status |
|-----|------|----------------------|-------------|--------|
| NEW-01 | Security | XSS via `leg.aircraftType` in detail chip `innerHTML` | 🔴 CRITICAL | ✅ Fixed |
| NEW-02 | Memory | amCharts 5 `_mapRoot` not disposed in `stop()` | 🔴 CRITICAL | ✅ Fixed |
| NEW-03 | Memory | `_overlayHideTimer` not cleared in `stop()` | 🟡 MEDIUM | ✅ Fixed |
| NEW-04 | Correctness | `cityAttractions_Xaxis/Yaxis` hardcoded to `"0"` | 🟠 HIGH | ✅ Fixed |
| NEW-05 | Correctness | Date params stripped from AeroAPI URL | 🟠 HIGH | ✅ Fixed |
| NEW-06 | Correctness | Gate `"0"` treated as absent via falsy coercion | 🟢 LOW | ✅ Fixed |
| NEW-07 | Performance | PERF-006 debounce wiring incomplete | 🟡 MEDIUM | ⬜ Open |
| NEW-08 | Performance | Sequential 2-second sleep inflates poll cycles | 🟡 MEDIUM | ⬜ Open |
| NEW-09 | Performance | Unbounded `_apiCache` growth, no TTL eviction | 🟡 MEDIUM | ⬜ Open |
| NEW-10 | Correctness | Plane tooltip `\n` collapses in amCharts 5 SVG text | 🟡 MEDIUM | ✅ Fixed |
| NEW-11 | Performance | No adaptive polling based on flight phase | 🟡 MEDIUM | ⬜ Open |
| NEW-12 | UX | Plane position tweening — no smooth animation | 🟡 MEDIUM | ⬜ Open |
| NEW-13 | Security | API error log may leak AeroAPI key in some clients | 🟡 MEDIUM | ✅ Fixed |
| NEW-14 | UX | Connection risk indicator for short layovers | 🟡 MEDIUM | ✅ Fixed |
| NEW-15 | UX | Delayed flight `+Nm` badge in flight table | 🟡 MEDIUM | ✅ Fixed |
| NEW-16 | UX | Countdown box replaced by boarding info within 24 h | 🟢 LOW | ⬜ Open |
| NEW-17 | UX | Responsive overlay breakpoints for narrow displays | 🟢 LOW | ✅ Fixed v2.2.0 |
| NEW-18 | UX | Stale weather indicator + hourly re-fetch | 🟢 LOW | ⬜ Open |
| NEW-19 | UX | **Mobile & Touch Optimization** — implement `100dvh`, safe-area insets, and enlarged touch targets (44px) for mobile devices. | 🟠 HIGH | ✅ Fixed v2.2.0 |
| NEW-20 | ACC | **Touch-device Focus & Accessibility** — force 16px font on inputs to prevent iOS auto-zoom; support `touchstart` in Zen Mode. | 🟠 HIGH | ✅ Fixed v2.2.0 |

---

## Implementation Plan (v2 cycle)

### Stage A — Immediate (Critical Safety) `v1.3.0`

*Target: eliminate memory leaks that affect every hot-reload / restart cycle.*

| # | Ref | Action | Files |
|---|-----|--------|-------|
| A1 | NEW-02 | Call `this._mapRoot.dispose()` as the first statement in `stop()`. Also null the reference: `this._mapRoot = null`. | `MMM-iAmGoingThere.js` |
| A2 | NEW-03 | Add `clearTimeout(this._overlayHideTimer)` to `stop()` alongside the other timer clears. | `MMM-iAmGoingThere.js` |
| A3 | NEW-13 | Change the catch-block warn to `console.warn(\`[...] Error: ${e.message}\`)` — omit the full error object. | `node_helper.js` |

Estimated effort: **30 minutes**. All three are one- to two-line changes.

---

### Stage B — Short-term (Correctness & UX) `v1.3.1`

*Target: fix the two remaining correctness issues and add the highest-value UX improvements.*

| # | Ref | Action | Files |
|---|-----|--------|-------|
| B1 | NEW-10 | Replace `_tipLines.join("\n")` with `_tipLines.join("\n")` → test in amCharts 5. If text still collapses, switch to the amCharts 5 `{newLine}` token or use `[/]` separator. Add a small unit test to verify tooltip rendering. | `MMM-iAmGoingThere.js` |
| B2 | NEW-06 | Replace `flight.gate_origin \|\| null` and the three equivalent falsy guards with explicit `!= null` checks: `flight.gate_origin != null ? String(flight.gate_origin) : null`. | `node_helper.js` |
| B3 | NEW-15 | In `buildTableHTML()`, after computing `estimatedDeparture` and `scheduledDeparture`, calculate delay minutes. If delay > 15, append `<span class="iAGT-delay-badge">+${delay}m</span>` to the status cell. Add `.iAGT-delay-badge` CSS in amber. | `MMM-iAmGoingThere.js`, `MMM-iAmGoingThere.css` |
| B4 | NEW-14 | In `buildTableHTML()`, for connecting legs (not the first outbound), compute layover minutes from previous leg's `estimatedArrival` to current leg's `estimatedDeparture`. If layover < 90 and previous leg has any delay, append a `⚠` badge to the connecting leg status cell. | `MMM-iAmGoingThere.js` |

Estimated effort: **2–3 hours**.

---

### Stage C — Performance (API & Render) `v1.4.0`

*Target: reduce API quota consumption and improve rendering efficiency.*

| # | Ref | Action | Files |
|---|-----|--------|-------|
| C1 | NEW-07 | Wire the existing `_validateTimer` placeholder: replace the synchronous `this._planeSeries.data.setAll(planes)` and `this._mapLineSeries.data.setAll(lines)` calls in `updateMapLines()` with a 250 ms debounced wrapper using `clearTimeout` / `setTimeout`. | `MMM-iAmGoingThere.js` |
| C2 | NEW-09 | In `pollAllFlights()`, after each poll cycle, scan `_apiCache` and delete any entries whose `ts` is older than 3,600,000 ms (1 hour). This caps cache size to approximately the number of flights polled within the last hour. | `node_helper.js` |
| C3 | NEW-08 | Replace the sequential `await sleep(2000)` between flight polls with parallel `Promise.allSettled()`. Group per-leg fetches into a single `Promise.allSettled(legs.map(leg => this.pollFlight(leg)))`, eliminating the serial accumulation of sleeps. Rate-limit by batching in groups of 3 if API quota is a concern. | `node_helper.js` |
| C4 | NEW-11 | Implement phase-aware TTL in `fetchFlightStatus()`: scheduled (>2h) → 10 min TTL; scheduled (within 2h) → 2 min TTL; active / en-route → 1 min TTL; landed → 15 min TTL; cancelled → 30 min TTL. Remove the fixed 1 min / 5 min split. | `node_helper.js` |

Estimated effort: **3–4 hours**.

---

### Stage D — UX Enhancements `v1.5.0`

*Target: high-impact UX innovations for an immersive display experience.*

| # | Ref | Action | Files |
|---|-----|--------|-------|
| D1 | NEW-12 | On each poll that returns updated `currentLat` / `currentLon`, tween the plane bullet using `dataItem.animate({ key: "latitude", to: newLat, duration: 1000 })`. Requires storing the previous position on the data item. | `MMM-iAmGoingThere.js` |
| D2 | NEW-16 | In `updateCountdown()`, when `hoursUntilDeparture < 24`, switch the countdown box to a boarding-info layout: show gate, terminal, ETD in a high-visibility card with a ✈ icon. Restore normal countdown when departure passes. | `MMM-iAmGoingThere.js`, `MMM-iAmGoingThere.css` |
| D3 | NEW-17 | Add a CSS `@media (max-width: 900px)` rule that sets both overlay panel widths to `95vw` and stacks them vertically. Expose `narrowBreakpoint` config option (default `900`) that is injected as a `<style>` element at `getDom()` time. | `MMM-iAmGoingThere.js`, `MMM-iAmGoingThere.css` |
| D4 | NEW-18 | Schedule an hourly `setInterval` in `start()` to re-fetch weather for the current destination. Store the last-fetched timestamp and render it as a small `Updated: HH:MM` line below the weather reading in the city info panel. | `MMM-iAmGoingThere.js`, `node_helper.js` |

Estimated effort: **4–6 hours**.

---

*Review conducted as part of v1.2.0–v1.2.1 development cycle.*

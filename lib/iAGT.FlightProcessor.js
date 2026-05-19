/* iAGT.FlightProcessor.js - Pure flight data processing functions (PER-001) */
var IagtFlightProcessor = {

	/* ── FILTERED LEGS ── */
	getFilteredLegs: function(flightLegs, flightDisplayMode) {
		const mode = flightDisplayMode || "all";
		if (mode === "outbound") {
			return flightLegs.filter((l) => l.type === "outbound");
		}
		if (mode === "return") {
			return flightLegs.filter((l) => l.type === "return");
		}
		return flightLegs;
	},

	/* ── TRAVELER MAP ── */
	buildTravelerMap: function(flightLegs, travelerColors, travelerSymbols) {
		const colors = {};
		const symbols = {};
		let idx = 0;
		flightLegs.forEach((leg) => {
			const name = leg.travelerName;
			if (name && !colors[name]) {
				colors[name] = travelerColors[idx % travelerColors.length];
				symbols[name] = travelerSymbols[idx % travelerSymbols.length];
				idx++;
			}
		});
		return { colors, symbols };
	},

	/* ── LEG COLOR ── */
	getLegColor: function(leg, travelerColors, scenario) {
		if (scenario === 3 && leg.travelerName && travelerColors[leg.travelerName]) {
			return travelerColors[leg.travelerName];
		}
		return null;
	},

	/* ── SEGMENTS TO LINE ── */
	segmentsToLine: function(pts, customColor) {
		return {
			type: "Feature",
			properties: { customColor: customColor || null },
			geometry: {
				type: "LineString",
				coordinates: pts.map((p) => [p.lon, p.lat])
			}
		};
	},

	/* ── CALCULATE BEARING ── */
	calculateBearing: function(lat1, lon1, lat2, lon2) {
		const toRad = (d) => d * Math.PI / 180;
		const phi1 = toRad(lat1);
		const phi2 = toRad(lat2);
		const dLon = toRad(lon2 - lon1);
		const y = Math.sin(dLon) * Math.cos(phi2);
		const x = Math.cos(phi1) * Math.sin(phi2) - Math.sin(phi1) * Math.cos(phi2) * Math.cos(dLon);
		return (Math.atan2(y, x) * 180 / Math.PI + 360) % 360;
	},

	/* ── GREAT CIRCLE POINTS ── */
	generateGreatCirclePoints: function(lat1, lon1, lat2, lon2, n) {
		return iAGTGreatCircle.generateGreatCirclePoints(lat1, lon1, lat2, lon2, n);
	},

	/* ── CACHE GREAT CIRCLE POINTS ── */
	cacheGreatCirclePoints: function(flightLegs, gcPoints) {
		const n = gcPoints || 60;
		flightLegs.forEach((leg) => {
			if (leg._gcCachedN === n && leg._gcPoints) return;
			if (leg.from && leg.to) {
				leg._gcPoints = IagtFlightProcessor.generateGreatCirclePoints(
					leg.from.lat, leg.from.lon, leg.to.lat, leg.to.lon, n
				);
				leg._gcCachedN = n;
			} else {
				leg._gcPoints = [];
				leg._gcCachedN = n;
			}
		});
	},

	/* ── GET DEPARTURE MS ── */
	getDepartureMs: function(leg) {
		if (!leg || !leg.departure) return 0;
		const t = new Date(leg.departure);
		return isNaN(t.getTime()) ? 0 : t.getTime();
	},

	/* ── BUILD MAP LINES ── */
	buildMapLines: function(legs, config, travelerColors, tripReset, getFilteredLegs) {
		const mode = String(config.showFlightTracks || "auto");
		const data = {
			scheduled: [],
			active: [],
			tail: [],
			landed: [],
			previous: [],
			cancelled: []
		};

		if (mode === "false") return data;
		if (config.scenario === 4 && mode !== "test") return data;

		const n = config.gcPoints || 60;
		if (!legs) legs = getFilteredLegs ? getFilteredLegs() : [];

		legs.forEach((leg, idx) => {
			if (!leg.from || !leg.to || !leg._gcPoints) return;

			const pts = leg._gcPoints;
			let st = leg.status || "scheduled";

			let hasSubsequentDeparted = false;
			if (config.scenario === 3) {
				hasSubsequentDeparted = legs.some((l, i) => i > idx && l.travelerName === leg.travelerName && (l.status === "active" || l.status === "landed"));
			} else {
				hasSubsequentDeparted = legs.some((l, i) => i > idx && (l.status === "active" || l.status === "landed"));
			}
			if (st === "landed" && hasSubsequentDeparted) st = "previous";

			const customColor = IagtFlightProcessor.getLegColor(leg, travelerColors, config.scenario);

			if (mode === "true") {
				if (data[st]) {
					data[st].push(IagtFlightProcessor.segmentsToLine(pts, customColor));
				}
			} else {
				if (st === "active") {
					const sp = Math.max(0, Math.min(n - 1, Math.floor((leg.progress || 0) * n)));
					const done = pts.slice(0, sp + 1);
					const rem = pts.slice(sp);

					data.active.push(IagtFlightProcessor.segmentsToLine(done, customColor));
					if (rem.length > 1) {
						data.tail.push(IagtFlightProcessor.segmentsToLine(rem, customColor));
					}
				} else if (data[st]) {
					data[st].push(IagtFlightProcessor.segmentsToLine(pts, customColor));
				}
			}
		});

		return data;
	},

	/* ── BUILD AIRPORT MARKERS ── */
	buildAirportMarkers: function(legs, config, travelerColors, tripReset, gcPoints) {
		const airports = [];
		const planes = [];
		const seen = new Set();
		const homeIata = config.home ? config.home.iata : null;

		if (config.showDestinations !== false) {
			const addAirport = (ap) => {
				if (!ap) return;
				let lat = parseFloat(ap.lat);
				let lon = parseFloat(ap.lon);
				if (isNaN(lat) || isNaN(lon)) return;

				if (lat === 0 && lon === 0) return;

				const key = `${lat.toFixed(3)}_${lon.toFixed(3)}`;

				const existing = airports.find((a) => `${(+a.latitude).toFixed(3)}_${(+a.longitude).toFixed(3)}` === key);
				if (existing) {
					if (!existing.crest && ap.crest) existing.crest = ap.crest;
					const newLegs = legs.filter((l) => l.to && l.to.lat === ap.lat && l.to.lon === ap.lon);
					newLegs.forEach((nl) => {
						if (!existing.legs.find((el) => el.id === nl.id)) {
							existing.legs.push(nl);
						}
					});
					return;
				}
				if (seen.has(key)) return;
				seen.add(key);

				airports.push({
					iata: ap.iata,
					name: ap.name,
					latitude: ap.lat,
					longitude: ap.lon,
					crest: ap.crest || null,
					legs: legs.filter((l) => l.to && l.to.lat === ap.lat && l.to.lon === ap.lon),
					customColor: (homeIata && ap.iata === homeIata)
						? (config.scenario === 4 || config.scenario === 6 ? "#FFD700" : config.colorAirportHome)
						: (config.scenario === 4 || config.scenario === 6 ? "#FFFFFF" : config.colorAirportOther)
				});
			};
			legs.forEach((leg) => { addAirport(leg.from); addAirport(leg.to); });
		}

		if (config.animationEnabled && !tripReset) {
			legs.forEach((leg) => {
				const isActive = leg.status === "active";
				if (!isActive) return; // Only process active flights for plane markers

				let planeLat = leg.currentLat;
				let planeLon = leg.currentLon;

				if ((planeLat === null || planeLon === null) && (leg.progress !== null && leg.progress !== undefined) && leg._gcPoints && leg._gcPoints.length) {
					const n = gcPoints || 60;
					const ptIdx = Math.min(n - 1, Math.floor((leg.progress || 0) * n));
					const pt = leg._gcPoints[ptIdx];
					if (pt) {
						planeLat = pt.lat;
						planeLon = pt.lon;
					}
				}

				if (planeLat === null || planeLon === null) {
					planeLat = leg.from ? leg.from.lat : 0;
					planeLon = leg.from ? leg.from.lon : 0;
				}

				let rotation = 0;
				if (leg.from && leg.to && leg._gcPoints && leg._gcPoints.length) {
					const n = gcPoints || 60;
					const prog = leg.progress || 0;
					const pts = leg._gcPoints;
					const i = Math.min(pts.length - 1, Math.floor(prog * pts.length));

					if (i < pts.length - 1) {
						rotation = IagtFlightProcessor.calculateBearing(pts[i].lat, pts[i].lon, pts[i + 1].lat, pts[i + 1].lon);
					} else if (i > 0) {
						rotation = IagtFlightProcessor.calculateBearing(pts[i - 1].lat, pts[i - 1].lon, pts[i].lat, pts[i].lon);
					}
				} else if (leg.heading != null && !isNaN(leg.heading)) {
					rotation = leg.heading;
				} else if (leg.to && leg.to.lat != null && leg.to.lon != null) {
					rotation = IagtFlightProcessor.calculateBearing(planeLat, planeLon, leg.to.lat, leg.to.lon);
				}

				let planeColor = config.colorPlane;
				if (config.scenario === 3 && leg.travelerName && travelerColors[leg.travelerName]) {
					planeColor = travelerColors[leg.travelerName];
				}

				if (config.showPlaneShadow) {
					planes.push({
						latitude: planeLat - 0.1,
						longitude: planeLon + 0.1,
						rotation: rotation,
						customColor: "#FFFFFF",
						alpha: 0.15,
						scale: 0.1,
						shadowOnly: true,
						flightNumber: leg.flightNumber || ""
					});
				}

				const _fmtTip = (iso) => {
					if (!iso) return null;
					try {
						const t = new Date(iso);
						return isNaN(t.getTime()) ? null : t.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
					} catch (_e) { return null; }
				};
				const _tipLines = [leg.flightNumber || ""];
				if (leg.detailedStatus) _tipLines.push(`Status: ${leg.detailedStatus}`);
				if (planeLat != null && planeLon != null) {
					_tipLines.push(`Pos: ${planeLat.toFixed(3)}\u00B0, ${planeLon.toFixed(3)}\u00B0`);
				}
				const _hasLive = (leg.groundspeed != null && !isNaN(leg.groundspeed)) || (leg.altitude != null && !isNaN(leg.altitude)) || (leg.heading != null && !isNaN(leg.heading));
				if (_hasLive) {
					const _altFt = (leg.altitude != null && !isNaN(leg.altitude)) ? `${leg.altitude.toLocaleString()} ft` : "\u2014";
					const _spd = (leg.groundspeed != null && !isNaN(leg.groundspeed)) ? `${leg.groundspeed} kts` : "\u2014";
					const _hdg = (leg.heading != null && !isNaN(leg.heading)) ? `${Math.round(leg.heading)}\u00B0` : "\u2014";
					const _rateMap = { C: "\u25B2 Climb", D: "\u25BC Desc", L: "\u2192 Level" };
					const _rate = leg.altitudeChange ? (_rateMap[leg.altitudeChange] || leg.altitudeChange) : "\u2014";
					_tipLines.push(`Alt: ${_altFt}  Spd: ${_spd}`);
					_tipLines.push(`Hdg: ${_hdg}  Rate: ${_rate}`);
				}
				if (leg.lastPositionUpdate) _tipLines.push(`Upd: ${_fmtTip(leg.lastPositionUpdate) || leg.lastPositionUpdate}`);
				if (leg.aircraftType || leg.tailNumber) {
					_tipLines.push([leg.aircraftType, leg.tailNumber ? `(${leg.tailNumber})` : null].filter(Boolean).join(" "));
				}

				planes.push({
					latitude: planeLat,
					longitude: planeLon,
					rotation: rotation,
					customColor: planeColor,
					alpha: 1.0,
					scale: 0.12,
					flightNumber: leg.flightNumber || "",
					tooltipContent: _tipLines.join("\n")
				});
			});
		}

		return { airports, planes };
	}
};

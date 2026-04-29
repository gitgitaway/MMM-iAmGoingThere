/*
 * lib/greatCircle.js — MMM-iAmGoingThere
 *
 * SLERP spherical interpolation for great-circle path generation.
 * Single source of truth shared by the frontend module (via getScripts)
 * and the Node.js test suite (via require).
 */

(function (root) {

  function generateGreatCirclePoints (lat1, lon1, lat2, lon2, n) {
    const rad   = d => d * Math.PI / 180;
    const deg   = r => r * 180 / Math.PI;
    const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

    const p1 = rad(lat1); const l1 = rad(lon1);
    const p2 = rad(lat2); const l2 = rad(lon2);

    const x1 = Math.cos(p1) * Math.cos(l1);
    const y1 = Math.cos(p1) * Math.sin(l1);
    const z1 = Math.sin(p1);
    const x2 = Math.cos(p2) * Math.cos(l2);
    const y2 = Math.cos(p2) * Math.sin(l2);
    const z2 = Math.sin(p2);

    const dot   = clamp(x1 * x2 + y1 * y2 + z1 * z2, -1, 1);
    const omega = Math.acos(dot);
    const sinO  = Math.sin(omega);

    const pts = [];
    for (let i = 0; i <= n; i++) {
      const t = i / n;
      let px, py, pz;
      if (Math.abs(omega) < 0.00001) {
        px = x1; py = y1; pz = z1;
      } else {
        const f1 = Math.sin((1 - t) * omega) / sinO;
        const f2 = Math.sin(t * omega) / sinO;
        px = f1 * x1 + f2 * x2;
        py = f1 * y1 + f2 * y2;
        pz = f1 * z1 + f2 * z2;
      }
      pts.push({
        lat: deg(Math.asin(clamp(pz, -1, 1))),
        lon: deg(Math.atan2(py, px))
      });
    }
    return pts;
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { generateGreatCirclePoints };
  } else {
    root.iAGTGreatCircle = { generateGreatCirclePoints };
  }

}(typeof window !== "undefined" ? window : global));

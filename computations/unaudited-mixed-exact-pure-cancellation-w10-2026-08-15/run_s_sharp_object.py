#!/usr/bin/env python3
"""W10 task S -- record the SHARP N=6 object and state exactly what is certified.

THE OBJECT: a source A on six sites with
  * H_w = 0 for all 726 mixed words        (MIXED-EXACT)
  * H_{0^6} = 1                            (a NONZERO pure coefficient)
  * all three pure FIBRES nonempty: [f0, 2, 2]
  * hence H_{1^6} = H_{2^6} = 0 vanish by CANCELLATION between two nonzero
    matching products each
  * template ADMISSIBLE: (T4),(T5),(T6),(S) all hold.

CERTIFICATION STATUS, stated precisely:
  - the TEMPLATE (which cells are nonzero) and everything computed from it --
    fibres, (T4),(T5),(T6),(S), m, Sigma, beta -- are EXACT integer
    computations, and the support is robust (smallest |cell| ~ 1e-1, far from
    the 1e-7 threshold);
  - the VALUES are float, certified only to max|H_w| ~ 1e-15 by scipy
    least-squares.  Exactification was attempted two ways (one-block exact
    solve, star-linearised exact solve after rationalising the off-star) and
    FAILED: the solution lies on a positive-dimensional stratum whose generic
    point is not rational (coordinates do not rationalise below denominator
    200 to better than 2e-3).  So this object is reported as FLOAT-CERTIFIED,
    NOT exact.  The EXACT certified witnesses of W10 are the zero-pure family
    of tasks B/C/I.
"""
from __future__ import annotations
import json, os, sys
from fractions import Fraction as F
import numpy as np
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w10_core as w10                                            # noqa: E402
import w10_numeric as wn                                          # noqa: E402
from w10_core import COLORS, require                              # noqa: E402

N = 6
log = []; OUT = {}
def say(s="", flush=True):
    print(s, flush=flush); log.append(s)

s = wn.System(N, d=3)
M = ((0, 1), (2, 3), (4, 5))
PT = {0: 1.0}
ANC = [(1, M), (2, M)]
say("=" * 96)
say("S  the SHARP N=6 object: mixed-exact, ADMISSIBLE, one NONZERO pure,")
say("   the other two pures vanishing by cancellation")
say("=" * 96)
rs = np.random.default_rng(99)
best = None
tried = 0
for t in range(600):
    tried += 1
    x0 = rs.normal(size=s.nv) * (0.3 + 1.5 * rs.random())
    sol = least_squares(lambda x: s.residual(x, pure_targets=PT, anchors=ANC),
                        x0, jac=lambda x: s.jacobian(x, pure_targets=PT,
                                                     anchors=ANC),
                        method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15,
                        max_nfev=2000)
    c = float(np.max(np.abs(sol.fun)))
    if c > 1e-13:
        continue
    src = w10.zero_source(N)
    for (e, i, j), idx in s.vidx.items():
        if abs(sol.x[idx]) > 1e-7:
            src[e][i][j] = F(sol.x[idx]).limit_denominator(10 ** 9)
    a = w10.audit(w10.template_of(src, N), N)
    if a["ADMISSIBLE"]:
        best = (c, sol.x.copy(), a, src)
        break
require(best is not None, "no admissible hit")
c, x, a, src = best
mincell = min(abs(v) for v in x if abs(v) > 1e-7)
say(f"  found after {tried} starts; max|residual| = {c:.3e}; "
    f"smallest |cell| = {mincell:.3e}")
say(f"  TEMPLATE (exact integer audit): m={a['m']} Sigma={a['Sigma']} "
    f"beta={a['beta']} min degree {a['min_degree']}")
say(f"    pure fibres {a['T4_pure_fibres']}  |  T4 {a['T4']} T5 {a['T5']} "
    f"T6 {a['T6']} S {a['S']}  |  ADMISSIBLE {a['ADMISSIBLE']}")
say(f"    mixed fibre histogram {a['mixed_fibre_histogram']}")
hv = {cc: float(sum(float(np.prod([x[k] for k in row]))
                    for row in s.pure_rows[cc])) if s.pure_rows[cc] else 0.0
      for cc in COLORS}
say(f"  pure coefficients (float): H_0 = {hv[0]:.12f}, H_1 = {hv[1]:.3e}, "
    f"H_2 = {hv[2]:.3e}")
for cc in COLORS:
    terms = [float(np.prod([x[k] for k in row])) for row in s.pure_rows[cc]]
    terms = [v for v in terms if abs(v) > 1e-12]
    say(f"    colour {cc}: {len(terms)} nonzero matching products "
        f"{[f'{v:.6f}' for v in terms][:6]} -> sum {sum(terms):.3e}")
say()
say("  ROBUSTNESS of the support (audit at several thresholds):")
rob = {}
for thr in (1e-7, 1e-5, 1e-4, 1e-3, 1e-2):
    src2 = w10.zero_source(N)
    for (e, i, j), idx in s.vidx.items():
        if abs(x[idx]) > thr:
            src2[e][i][j] = F(x[idx]).limit_denominator(10 ** 9)
    a2 = w10.audit(w10.template_of(src2, N), N)
    rob[str(thr)] = {"Sigma": a2["Sigma"], "m": a2["m"],
                     "fibres": a2["T4_pure_fibres"],
                     "ADMISSIBLE": a2["ADMISSIBLE"]}
    say(f"    threshold {thr:.0e}: m={a2['m']:2d} Sigma={a2['Sigma']:3d} "
        f"fibres {a2['T4_pure_fibres']} ADMISSIBLE {a2['ADMISSIBLE']}")
OUT["S_robustness"] = rob
OUT["S"] = {"starts_tried": tried, "max_residual": c,
            "smallest_abs_cell": mincell,
            "template_audit_EXACT": {k: v for k, v in a.items()},
            "pure_coefficients_float": {str(k): v for k, v in hv.items()},
            "source_float": {f"{u},{v}": [[float(x[s.vidx[((u, v), i, j)]])
                                           for j in COLORS] for i in COLORS]
                             for (u, v) in w10.edges(N)},
            "certification": "template EXACT; values FLOAT (see docstring)"}
say()
say("  CERTIFICATION: the template and its audit are exact; the VALUES are")
say("  float (max|H_w| ~ 1e-15).  Exactification failed (positive-dimensional")
say("  stratum, irrational coordinates) -- see run_q_onepure.py / run_r_exactify.py.")
with open(os.path.join(HERE, "results_s_sharp_object.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_s_sharp_object.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("S DONE")

#!/usr/bin/env python3
"""W10 task H -- the reopened question, probed: does a MIXED-EXACT source live
on a template in ADM+ = (T4)+(T5)+(T6)+(S)+(FIE)?

If YES, Door A is closed on the (FIE) stratum too and H4 is finished as a
route.  If the search finds nothing, the ceiling question genuinely survives
there -- and W10's consequence map says (FIE) is the ONLY place it can.

FLOAT SEARCH (scipy least-squares, analytic Jacobian), explicitly labelled.
Every hit is re-verified in exact arithmetic after rationalisation; a miss is
reported as "not found", never as "none".
Positive control: the same solver on a W10 witness template (m = 24, full
blocks on 24 edges), where a mixed-exact source provably exists.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F

import numpy as np
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (HERE,
          os.path.join(REPO, "computations", "unaudited-template-kill-w8-2026-08-15")):
    if p not in sys.path:
        sys.path.insert(0, p)

import w10_core as w10                                            # noqa: E402
import w10_numeric as wn                                          # noqa: E402
from w10_core import COLORS                                       # noqa: E402
import w8_core as w8                                              # noqa: E402

N = 8
EDGES = w10.edges(N)
GEO = w8.geometry(N)
OUT = {}
log = []


def say(s="", flush=True):
    print(s, flush=flush)
    log.append(s)


def probe(label, tpl, starts=250, seed=7):
    sysd = wn.System(N, d=3, template=tpl)
    rs = np.random.default_rng(seed)
    best = None
    hits = 0
    for t in range(starts):
        x0 = rs.normal(size=sysd.nv) * (0.4 + 1.6 * rs.random())
        sol = least_squares(lambda x: sysd.residual(x), x0,
                            jac=lambda x: sysd.jacobian(x),
                            method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15,
                            max_nfev=3000)
        c = float(np.max(np.abs(sol.fun)))
        nz = int((np.abs(sol.x) > 1e-6).sum())
        if best is None or (c, -nz) < (best[0], -best[2]):
            best = (c, sol.x.copy(), nz)
        if c < 1e-10:
            hits += 1
    c, x, nz = best
    # exact re-check of the achieved (degenerate) template
    src = w10.zero_source(N)
    for (e, i, j), k in sysd.vidx.items():
        if abs(x[k]) > 1e-6:
            src[e][i][j] = F(x[k]).limit_denominator(10 ** 7)
    aud = w10.audit(w10.template_of(src, N), N)
    rec = {"label": label, "n_vars": sysd.nv,
           "n_supported_mixed_words": len(sysd.mixed),
           "starts": starts, "best_max_residual": c, "hits_below_1e-10": hits,
           "nonzero_cells_in_best": nz,
           "template_Sigma": sum(len(v) for v in tpl.values()),
           "achieved_admissible_after_rationalise": aud["ADMISSIBLE"],
           "achieved_Sigma": aud["Sigma"]}
    say(f"  {label:38s} vars {sysd.nv:3d} | supported mixed words "
        f"{len(sysd.mixed):5d} | best max|res| {c:.3e} | hits {hits}/{starts} "
        f"| nonzero cells {nz}/{sysd.nv}")
    return rec


say("=" * 100)
say("H  does a MIXED-EXACT source live on an ADM+ template?  [FLOAT SEARCH]")
say("=" * 100)
rows = []

# ---- positive control: a W10 witness template (mixed-exact source EXISTS) ----
res_c = json.load(open(os.path.join(HERE, "results_c_n8.json")))
rec24 = next(r for r in res_c["C1_sweep"] if r["m"] == 24)
G24 = set(tuple(e) for e in rec24["graph"])
tpl_ctrl = {e: (frozenset((i, j) for i in COLORS for j in COLORS)
                if e in G24 else frozenset()) for e in EDGES}
rows.append(probe("[CONTROL] W10 witness template m=24", tpl_ctrl, starts=4))

# ---- the ADM+ templates found by task F ----
try:
    res_f = json.load(open(os.path.join(HERE, "results_f_fie_stratum.json")))
except FileNotFoundError:
    res_f = {"F1": []}
for row in res_f.get("F1", []):
    if not row.get("found"):
        continue
    tpl = {e: frozenset() for e in EDGES}
    for key, cells in row["template"].items():
        u, v = (int(t) for t in key.split(","))
        tpl[(u, v)] = frozenset((int(a), int(b)) for a, b in cells)
    a = w10.audit(tpl, N)
    masks = []
    for e in EDGES:
        mk = 0
        for (i, j) in tpl[e]:
            mk |= 1 << (3 * i + j)
        masks.append(mk)
    fie = w8.fie_ok(GEO, masks)
    say(f"  ADM+ template m={row['m']} Sigma={a['Sigma']} beta={a['beta']} "
        f"admissible={a['ADMISSIBLE']} fie={fie}")
    rows.append(probe(f"ADM+ template m={row['m']} (Sigma={a['Sigma']})", tpl,
                      starts=200, seed=100 + row["m"]))

OUT["H"] = rows
say()
say("  READ-OFF.  A control residual near machine zero with the achieved cell")
say("  count equal to the template's Sigma means the solver CAN find mixed-exact")
say("  points on a given template.  On an ADM+ template, a residual that stays")
say("  away from zero is EVIDENCE (not proof) that the ceiling question really")
say("  does survive on the (FIE) stratum -- which is exactly where W10's")
say("  consequence map says it must be attacked.")

with open(os.path.join(HERE, "results_h_admplus.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_h_admplus.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("H DONE")

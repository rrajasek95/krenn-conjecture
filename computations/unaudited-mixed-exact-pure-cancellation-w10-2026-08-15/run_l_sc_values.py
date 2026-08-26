#!/usr/bin/env python3
"""W10 task L -- the layer-2 (slice-cover) question at VALUE level, done right.

Task H's first attempt was defective: with no anti-degeneracy constraint the
least-squares solver collapses to the ZERO source (which is mixed-exact but has
an empty template).  That control failure is recorded honestly in
`log_h_run.txt`; this script replaces it.

FIX: Rabinowitsch anti-degeneracy.  For every cell k of the template add an
auxiliary variable y_k and the residual  x_k * y_k - 1 = 0.  Any exact zero of
the extended system has EVERY template cell nonzero, so it realises the
template exactly -- no collapse is possible.

Question: does a MIXED-EXACT source live on a template in
   ADM+ := (T4)+(T5)+(T6)+(S)+(SC)?
Positive control: the same solver, same anti-degeneracy, on a task-B/C witness
template, where a mixed-exact source with the full template provably exists.
FLOAT SEARCH; every hit re-verified exactly after rationalisation.
"""
from __future__ import annotations
import json, os, sys, time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (HERE, os.path.join(REPO, "computations",
                             "unaudited-template-kill-w8-2026-08-15")):
    if p not in sys.path:
        sys.path.insert(0, p)
import w10_core as w10                                            # noqa: E402
import w10_numeric as wn                                          # noqa: E402
from w10_core import COLORS, require                              # noqa: E402
import w8_core as w8                                              # noqa: E402

OUT = {}; log = []
def say(s="", flush=True):
    print(s, flush=flush); log.append(s)

def probe(label, N, tpl, starts=150, seed=5, budget=240.0):
    s = wn.System(N, d=3, template=tpl)
    nv = s.nv
    def res(z):
        x, y = z[:nv], z[nv:]
        return np.concatenate([s.residual(x), x * y - 1.0])
    def jac(z):
        x, y = z[:nv], z[nv:]
        J1 = s.jacobian(x)
        top = np.hstack([J1, np.zeros((J1.shape[0], nv))])
        bot = np.hstack([np.diag(y), np.diag(x)])
        return np.vstack([top, bot])
    rs = np.random.default_rng(seed)
    best = None; hits = 0; t0 = time.time(); done = 0
    for t in range(starts):
        if time.time() - t0 > budget:
            break
        done += 1
        x0 = rs.normal(size=nv)
        x0[np.abs(x0) < 0.3] = 0.5
        z0 = np.concatenate([x0, 1.0 / x0])
        sol = least_squares(res, z0, jac=jac, method="lm",
                            xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=3000)
        c = float(np.max(np.abs(sol.fun)))
        if best is None or c < best[0]:
            best = (c, sol.x[:nv].copy())
        if c < 1e-9:
            hits += 1
    c, x = best
    src = w10.zero_source(N)
    for (e, i, j), k in s.vidx.items():
        src[e][i][j] = F(x[k]).limit_denominator(10 ** 8)
    a = w10.audit(w10.template_of(src, N), N)
    rec = {"label": label, "N": N, "n_cells": nv,
           "supported_mixed_words": len(s.mixed), "starts_done": done,
           "best_max_residual": c, "hits": hits,
           "template_realised": a["Sigma"] == nv,
           "achieved_Sigma": a["Sigma"]}
    say(f"  {label:32s} cells {nv:3d} | supp mixed {len(s.mixed):5d} | starts "
        f"{done:4d} | best max|res| {c:.3e} | hits {hits} | template fully "
        f"realised {rec['template_realised']}")
    return rec

rows = []
say("=" * 100)
say("L  MIXED-EXACT values on ADM+ = (T4)+(T5)+(T6)+(S)+(SC) templates")
say("   [Rabinowitsch anti-degeneracy: every template cell forced nonzero]")
say("=" * 100)

# ---------- N = 8 ----------
say("N = 8:")
res_c = json.load(open(os.path.join(HERE, "results_c_n8.json")))
rec24 = next(r for r in res_c["C1_sweep"] if r["m"] == 24)
G24 = set(tuple(e) for e in rec24["graph"])
tpl_ctrl = {e: (frozenset((i, j) for i in COLORS for j in COLORS)
                if e in G24 else frozenset()) for e in w10.edges(8)}
rows.append(probe("[CONTROL] W10 witness m=24", 8, tpl_ctrl, starts=3,
                  budget=300.0))
res_f = json.load(open(os.path.join(HERE, "results_f_fie_stratum.json")))
for row in res_f.get("F1", []):
    if not row.get("found"):
        continue
    tpl = {e: frozenset() for e in w10.edges(8)}
    for key, cells in row["template"].items():
        u, v = (int(t) for t in key.split(","))
        tpl[(u, v)] = frozenset((int(a), int(b)) for a, b in cells)
    rows.append(probe(f"ADM+ m={row['m']} (Sigma={row['best_sigma']})", 8, tpl,
                      starts=200, seed=100 + row["m"], budget=300.0))

OUT["L"] = rows
say()
say("  A control at machine zero with the template fully realised means the")
say("  method works.  On an ADM+ template a residual that stays away from zero")
say("  is EVIDENCE (not proof) that no mixed-exact source realises it.")
with open(os.path.join(HERE, "results_l_sc_values.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_l_sc_values.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("L DONE")

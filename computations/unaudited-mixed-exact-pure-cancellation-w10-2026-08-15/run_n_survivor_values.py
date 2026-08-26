#!/usr/bin/env python3
"""W10 task N -- value-level probe of (SC)-admissible templates, done with a
parametrisation that CANNOT collapse.

Task H used no anti-degeneracy (solver collapsed to the zero source: control
failed, 0/216 cells nonzero).  Task L/M used Rabinowitsch pairs x_k*y_k = 1
(control still failed to converge).  Both failures are recorded in
log_h_run.txt / log_l_run.txt / log_m_run.txt.

FIX: write every cell as  x_k = s_k * exp(u_k)  with a FIXED random sign
pattern s and a bounded u.  Then no cell can ever be zero, the template is
realised by construction, and the system is smooth in u.  Signs are re-drawn
per start, so the search covers all 2^Sigma sign sectors stochastically.

CONTROL: the same solver on a task-B/C witness template, where a mixed-exact
source realising the full template PROVABLY exists.  If the control does not
converge, the probe is declared non-discriminating and NO conclusion is drawn.
FLOAT SEARCH; hits re-verified exactly.
"""
from __future__ import annotations
import json, os, sys, time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
W8DIR = os.path.join(REPO, "computations", "unaudited-template-kill-w8-2026-08-15")
for p in (HERE, W8DIR):
    if p not in sys.path:
        sys.path.insert(0, p)
import w10_core as w10                                            # noqa: E402
import w10_numeric as wn                                          # noqa: E402
from w10_core import COLORS, require                              # noqa: E402
import w8_core as w8                                              # noqa: E402

EDGES8 = w10.edges(8)
OUT = {}; log = []
def say(s="", flush=True):
    print(s, flush=flush); log.append(s)

def probe(label, N, tpl, pure_targets=None, starts=400, seed=5, budget=180.0):
    s = wn.System(N, d=3, template=tpl)
    nv = s.nv
    rs = np.random.default_rng(seed)
    best = None; hits = 0; t0 = time.time(); done = 0
    for t in range(starts):
        if time.time() - t0 > budget:
            break
        done += 1
        sg = rs.choice([-1.0, 1.0], size=nv)
        def res(u, sg=sg):
            return s.residual(sg * np.exp(u), pure_targets=pure_targets)
        def jac(u, sg=sg):
            x = sg * np.exp(u)
            return s.jacobian(x, pure_targets=pure_targets) * x
        u0 = rs.normal(size=nv) * 0.7
        sol = least_squares(res, u0, jac=jac, method="trf",
                            bounds=(-8.0, 8.0), xtol=1e-15, ftol=1e-15,
                            gtol=1e-15, max_nfev=1500)
        c = float(np.max(np.abs(sol.fun)))
        if best is None or c < best[0]:
            best = (c, sg * np.exp(sol.x))
        if c < 1e-9:
            hits += 1
    c, x = best
    src = w10.zero_source(N)
    for (e, i, j), k in s.vidx.items():
        src[e][i][j] = F(x[k]).limit_denominator(10 ** 8)
    a = w10.audit(w10.template_of(src, N), N)
    rec = {"label": label, "N": N, "cells": nv,
           "supported_mixed": len(s.mixed), "pure_targets": pure_targets,
           "starts_done": done, "best_max_residual": c, "hits": hits,
           "template_fully_realised": a["Sigma"] == nv}
    say(f"  {label:42s} cells {nv:3d} | supp mixed {len(s.mixed):5d} | starts "
        f"{done:4d} | best max|res| {c:.3e} | hits {hits} | full template "
        f"{rec['template_fully_realised']}")
    return rec

rows = []
say("=" * 104)
say("N  value-level probe with the non-collapsing parametrisation x = s*exp(u)")
say("=" * 104)
say("CONTROLS (mixed-exact sources realising these templates provably EXIST):")
b = json.load(open(os.path.join(HERE, "results_b_witness_n6.json")))
srcA = w10.src_from_repr(b["WA"]["source"], 6)
rows.append(probe("[CTRL] N=6 task-B template m=15", 6,
                  w10.template_of(srcA, 6), starts=200, budget=180.0))
srcC = w10.src_from_repr(b["WC"][0]["source"], 6)
rows.append(probe("[CTRL] N=6 task-B template m=9", 6,
                  w10.template_of(srcC, 6), starts=200, budget=120.0))
res_c = json.load(open(os.path.join(HERE, "results_c_n8.json")))
rec12 = next(r for r in res_c["C1_sweep"] if r["m"] == 12)
G12 = set(tuple(e) for e in rec12["graph"])
tpl12 = {e: (frozenset((i, j) for i in COLORS for j in COLORS)
             if e in G12 else frozenset()) for e in EDGES8}
rows.append(probe("[CTRL] N=8 task-C template m=12", 8, tpl12, starts=30,
                  budget=240.0))

say()
say("W8 SURVIVOR TEMPLATES (all ADM+ = T4/T5/T6/S/SC, audited in task M):")
cands = []
sur = json.load(open(os.path.join(W8DIR, "results_close_m20.json")))
for k, masks in enumerate(sur["survivors"]):
    cands.append((f"CEGAR survivor m=20 #{k} (Sigma=58)", masks))
imm = json.load(open(os.path.join(W8DIR, "results_immunity.json")))
for r in imm["results"]:
    if r["m"] in (20, 22):
        cands.append((f"immune m={r['m']} (Sigma={r['audit']['sigma']})",
                      r["template"]))
for label, masks in cands:
    tpl = {EDGES8[n]: frozenset(w8.cells(masks[n])) for n in range(28)}
    rows.append(probe(label, 8, tpl, pure_targets=None, starts=400, seed=17,
                      budget=240.0))
say()
say("  and the same with all three pures = 1 (= EXACTNESS on that template,")
say("  by Lemma W10-G):")
for label, masks in cands[:2]:
    tpl = {EDGES8[n]: frozenset(w8.cells(masks[n])) for n in range(28)}
    rows.append(probe(label + " [3 pures=1]", 8, tpl,
                      pure_targets={0: 1.0, 1: 1.0, 2: 1.0}, starts=400,
                      seed=19, budget=240.0))
OUT["N"] = rows
with open(os.path.join(HERE, "results_n_survivor_values.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_n_survivor_values.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("N DONE")

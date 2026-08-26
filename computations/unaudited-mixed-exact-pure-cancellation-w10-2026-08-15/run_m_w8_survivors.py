#!/usr/bin/env python3
"""W10 task M -- the two named W8 survivor families, tested with Lemma W10-G.

THE REDUCTION (proved in task A, gauge-invariance in task J).  On ANY template
T the following two problems are the SAME problem:
    (i)  a MIXED-EXACT source on T with all three pure coefficients NONZERO;
    (ii) a fully EXACT source on T.
(=> is Lemma W10-G, which gauges (i) to (ii) with the SAME template; <= is
trivial.)  So W8/W12's survivor systems -- "all mixed equations satisfied with
the three constant fibres required nonzero" -- carry NO slack relative to
exactness: there is no intermediate object to hunt.  All the content sits in
"pures nonzero"; W10's task B/C witnesses show that dropping it makes the
system solvable at the MAXIMUM cell count Sigma = 9m on admissible templates.

WHAT IS ACTUALLY MEASURED HERE.  For each survivor template T:
  M1  audit T (T4/T5/T6/S/SC) with W10's and W8's auditors;
  M2  is there a MIXED-EXACT source realising T (every cell nonzero, pures
      unconstrained)?  If NO, the survivor dies on the mixed system alone.
      If YES, by the reduction the residual kill must be the pure equations.
Rabinowitsch anti-degeneracy (x_k*y_k = 1) forces every template cell nonzero.
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

N = 8
EDGES = w10.edges(N)
GEO = w8.geometry(N)
OUT = {}; log = []
def say(s="", flush=True):
    print(s, flush=flush); log.append(s)

def tpl_of_masks(masks):
    return {EDGES[n]: frozenset(w8.cells(masks[n])) for n in range(28)}

def probe(label, tpl, pure_targets=None, starts=120, seed=5, budget=420.0):
    s = wn.System(N, d=3, template=tpl)
    nv = s.nv
    def res(z):
        x, y = z[:nv], z[nv:]
        return np.concatenate([s.residual(x, pure_targets=pure_targets),
                               x * y - 1.0])
    def jac(z):
        x, y = z[:nv], z[nv:]
        J1 = s.jacobian(x, pure_targets=pure_targets)
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
                            xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=2000)
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
    rec = {"label": label, "cells": nv, "supported_mixed": len(s.mixed),
           "pure_targets": pure_targets, "starts_done": done,
           "best_max_residual": c, "hits": hits,
           "template_fully_realised": a["Sigma"] == nv}
    say(f"  {label:44s} cells {nv:3d} | supp mixed {len(s.mixed):5d} | starts "
        f"{done:4d} | best max|res| {c:.3e} | hits {hits} | full template "
        f"{rec['template_fully_realised']}")
    return rec

say("=" * 104)
say("M  the W8 survivors: template audit + the mixed-only value question")
say("=" * 104)
say("  REDUCTION (Lemma W10-G): on any template, {mixed-exact with all three")
say("  pures nonzero} = {exact}, up to gauge, WITH THE SAME TEMPLATE.")
say("  So the survivor systems carry no slack relative to exactness.")
say()

cands = []
sur = json.load(open(os.path.join(W8DIR, "results_close_m20.json")))
for k, masks in enumerate(sur["survivors"]):
    cands.append((f"CEGAR survivor m=20 #{k}", masks))
imm = json.load(open(os.path.join(W8DIR, "results_immunity.json")))
for r in imm["results"]:
    if r["m"] in (20, 22, 24):
        cands.append((f"immune m={r['m']}", r["template"]))

rows = []
say("M1  template audits (W10 auditor vs W8 auditor):")
for label, masks in cands:
    tpl = tpl_of_masks(masks)
    a = w10.audit(tpl, N)
    a8 = w8.audit(GEO, masks)
    agree = (a["Sigma"] == a8["sigma"] and a["m"] == a8["m"]
             and a["S"] == (a8["mixed_singletons"] == 0)
             and a["T4"] == bool(a8["constants"]))
    say(f"  {label:28s} m={a['m']:2d} Sigma={a['Sigma']:3d} beta={a['beta']:2d} "
        f"| T4 {a['T4']} T5 {a['T5']} T6 {a['T6']} S {a['S']} | SC "
        f"{bool(a8['fie'])} | ADM {a['ADMISSIBLE']} | auditors agree {agree}")
    rows.append({"label": label, "m": a["m"], "Sigma": a["Sigma"],
                 "beta": a["beta"], "T4": a["T4"], "T5": a["T5"],
                 "T6": a["T6"], "S": a["S"], "SC": bool(a8["fie"]),
                 "ADMISSIBLE": a["ADMISSIBLE"], "auditors_agree": bool(agree),
                 "min_mixed_fibre": min(k for k in a["mixed_fibre_histogram"]
                                        if k > 0) if a["mixed_fibre_histogram"] else None})
OUT["M1_audits"] = rows

say()
say("M2  is there a MIXED-EXACT source realising the template (pures free)?")
probes = []
for label, masks in cands:
    probes.append(probe(label, tpl_of_masks(masks), pure_targets=None,
                        starts=120, seed=11))
OUT["M2_mixed_only"] = probes
say()
say("M3  the same with all three pures = 1 (equivalently, EXACTNESS on T):")
probes3 = []
for label, masks in cands[:2]:
    probes3.append(probe(label + " [+3 pures=1]", tpl_of_masks(masks),
                         pure_targets={0: 1.0, 1: 1.0, 2: 1.0},
                         starts=120, seed=13))
OUT["M3_exact"] = probes3

with open(os.path.join(HERE, "results_m_w8_survivors.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_m_w8_survivors.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("M DONE")

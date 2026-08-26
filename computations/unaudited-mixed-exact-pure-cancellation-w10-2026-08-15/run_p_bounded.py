#!/usr/bin/env python3
"""W10 task P -- the decisive value-level measurement, with the degeneracy
loophole closed.

Task N reported "hits" on the W8 survivor templates, but task O showed the
float optimiser had pressed one cell against the lower bound |x| = e^-8 and
that unconstrained Newton then drives that cell to ZERO -- i.e. the nearby
genuine solution of the mixed system does NOT realise the template.  That is a
control failure of task N and it is recorded here, not hidden.

CORRECT TEST.  Parametrise x_k = s_k exp(u_k) with |u_k| <= B.  A solution with
max|H_w| ~ 0 at SMALL B has every cell within a factor e^B of 1, so it really
realises the template.  Scaling B down and watching the attainable residual
separates "the template is realised" from "the solution wants a cell to
vanish".  Note the mixed system is gauge-covariant, so a genuine full-template
solution can always be gauge-normalised into a bounded window; the controls
below confirm the method sees that.
"""
from __future__ import annotations
import json, os, sys, time
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
from w10_core import COLORS                                       # noqa: E402
import w8_core as w8                                              # noqa: E402

EDGES8 = w10.edges(8)
log = []; OUT = {}
def say(s="", flush=True):
    print(s, flush=flush); log.append(s)


def scan(label, N, tpl, Bs=(8.0, 3.0, 1.5), starts=250, seed=5, budget=150.0):
    s = wn.System(N, d=3, template=tpl)
    nv = s.nv
    out = {"label": label, "N": N, "cells": nv,
           "supported_mixed": len(s.mixed), "rows": []}
    for B in Bs:
        rs = np.random.default_rng(seed)
        best = None
        t0 = time.time(); done = 0
        for t in range(starts):
            if time.time() - t0 > budget:
                break
            done += 1
            sg = rs.choice([-1.0, 1.0], size=nv)
            u0 = np.clip(rs.normal(size=nv) * min(0.7, B / 3),
                         -0.98 * B, 0.98 * B)
            sol = least_squares(lambda u: s.residual(sg * np.exp(u)), u0,
                                jac=lambda u: s.jacobian(sg * np.exp(u))
                                * (sg * np.exp(u)),
                                method="trf", bounds=(-B, B), xtol=1e-15,
                                ftol=1e-15, gtol=1e-15, max_nfev=1200)
            c = float(np.max(np.abs(sol.fun)))
            if best is None or c < best[0]:
                best = (c, sol.x.copy())
        c, u = best
        mn = float(np.min(np.abs(u)))
        atbound = int((np.abs(np.abs(u) - B) < 1e-6).sum())
        say(f"  {label:36s} B={B:4.1f} starts {done:4d} best max|res| "
            f"{c:.3e}  cells at the bound: {atbound}/{nv}")
        out["rows"].append({"B": B, "starts": done, "best_max_residual": c,
                            "cells_at_bound": atbound})
    return out


rows = []
say("=" * 104)
say("P  bounded-cell scan: does the mixed system have a solution that really")
say("   REALISES the template (no cell driven to zero)?")
say("=" * 104)
say("CONTROLS -- templates where a full-template mixed-exact source PROVABLY")
say("exists (task B/C witnesses).  They must stay near zero as B shrinks.")
b = json.load(open(os.path.join(HERE, "results_b_witness_n6.json")))
for key, lbl in (("WA", "[CTRL] N=6 witness m=15"),):
    src = w10.src_from_repr(b[key]["source"], 6)
    rows.append(scan(lbl, 6, w10.template_of(src, 6), starts=200, budget=120.0))
srcC = w10.src_from_repr(b["WC"][0]["source"], 6)
rows.append(scan("[CTRL] N=6 witness m=9", 6, w10.template_of(srcC, 6),
                 starts=200, budget=120.0))
res_c = json.load(open(os.path.join(HERE, "results_c_n8.json")))
rec12 = next(r for r in res_c["C1_sweep"] if r["m"] == 12)
G12 = set(tuple(e) for e in rec12["graph"])
tpl12 = {e: (frozenset((i, j) for i in COLORS for j in COLORS)
             if e in G12 else frozenset()) for e in EDGES8}
rows.append(scan("[CTRL] N=8 witness m=12", 8, tpl12, starts=40, budget=240.0))

say()
say("W8 SURVIVOR TEMPLATES:")
sur = json.load(open(os.path.join(W8DIR, "results_close_m20.json")))
tplS = {EDGES8[n]: frozenset(w8.cells(sur["survivors"][0][n])) for n in range(28)}
rows.append(scan("CEGAR survivor m=20 (Sigma=58)", 8, tplS, starts=400,
                 seed=17, budget=200.0))
imm = json.load(open(os.path.join(W8DIR, "results_immunity.json")))
for r in imm["results"]:
    if r["m"] == 20:
        tplI = {EDGES8[n]: frozenset(w8.cells(r["template"][n]))
                for n in range(28)}
        rows.append(scan("immune m=20 (Sigma=84)", 8, tplI, starts=400,
                         seed=19, budget=240.0))
OUT["P"] = rows
say()
say("READ-OFF: a control that stays at ~1e-10 for B = 1.5 shows the method can")
say("certify a realised template.  A survivor whose best residual BLOWS UP as B")
say("shrinks is telling us its mixed system only has solutions that degenerate")
say("the template -- which would KILL it at the mixed level.")
with open(os.path.join(HERE, "results_p_bounded.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_p_bounded.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("P DONE")

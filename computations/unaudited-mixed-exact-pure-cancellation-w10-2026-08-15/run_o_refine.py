#!/usr/bin/env python3
"""W10 task O -- high-precision confirmation that the W8 CEGAR survivor's
MIXED system really is solvable on its own template (task N found it with a
float solver; here it is refined to 60 digits by Gauss-Newton in mpmath).

A float least-squares "hit" can be a stall near a near-solution.  If Newton in
60-digit arithmetic drives max|H_w| below 1e-45 while every template cell stays
bounded away from zero, the point is on the variety to any reasonable standard.
This is still not an exact certificate over Q -- that is stated as a soft spot.
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np
from scipy.optimize import least_squares
import mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
W8DIR = os.path.join(REPO, "computations", "unaudited-template-kill-w8-2026-08-15")
for p in (HERE, W8DIR):
    if p not in sys.path:
        sys.path.insert(0, p)
import w10_core as w10                                            # noqa: E402
import w10_numeric as wn                                          # noqa: E402
import w8_core as w8                                              # noqa: E402

EDGES8 = w10.edges(8)
log = []; OUT = {}
def say(s="", flush=True):
    print(s, flush=flush); log.append(s)

sur = json.load(open(os.path.join(W8DIR, "results_close_m20.json")))
masks = sur["survivors"][0]
tpl = {EDGES8[n]: frozenset(w8.cells(masks[n])) for n in range(28)}
s = wn.System(8, d=3, template=tpl)
nv = s.nv
say(f"CEGAR survivor m=20: {nv} cells, {len(s.mixed)} supported mixed words")

rs = np.random.default_rng(17)
best = None
for t in range(400):
    sg = rs.choice([-1.0, 1.0], size=nv)
    sol = least_squares(lambda u: s.residual(sg * np.exp(u)),
                        rs.normal(size=nv) * 0.7,
                        jac=lambda u: s.jacobian(sg * np.exp(u)) * (sg * np.exp(u)),
                        method="trf", bounds=(-8.0, 8.0), xtol=1e-15,
                        ftol=1e-15, gtol=1e-15, max_nfev=1500)
    c = float(np.max(np.abs(sol.fun)))
    if best is None or c < best[0]:
        best = (c, sg * np.exp(sol.x))
say(f"float stage: best max|H_w| = {best[0]:.3e}")

mp.mp.dps = 60
x = [mp.mpf(float(v)) for v in best[1]]
idx, mask = s.mixed_idx


def resid(xv):
    out = []
    for r in range(idx.shape[0]):
        tot = mp.mpf(0)
        for k in range(idx.shape[1]):
            if not mask[r, k].any():
                continue
            p = mp.mpf(1)
            for q in range(idx.shape[2]):
                p *= xv[int(idx[r, k, q])]
            tot += p
        out.append(tot)
    return out


def jacob(xv):
    J = mp.zeros(idx.shape[0], nv)
    for r in range(idx.shape[0]):
        for k in range(idx.shape[1]):
            if not mask[r, k].any():
                continue
            for q in range(idx.shape[2]):
                p = mp.mpf(1)
                for q2 in range(idx.shape[2]):
                    if q2 != q:
                        p *= xv[int(idx[r, k, q2])]
                J[r, int(idx[r, k, q])] += p
    return J


t0 = time.time()
for it in range(12):
    F0 = resid(x)
    nrm = max(abs(v) for v in F0)
    say(f"  Newton it {it}: max|H_w| = {mp.nstr(nrm, 8)}")
    if nrm < mp.mpf('1e-50'):
        break
    J = jacob(x)
    b = mp.matrix([-v for v in F0])
    # Levenberg-damped normal equations (the solution variety is
    # positive-dimensional -- the gauge orbit alone is 24-dimensional -- so
    # J^T J is singular and a damped least-norm step is the right move).
    JT = J.T
    A = JT * J
    lam = mp.mpf(10) ** (-30)
    for k in range(nv):
        A[k, k] += lam
    dx = mp.lu_solve(A, JT * b)
    for k in range(nv):
        x[k] += dx[k]
F0 = resid(x)
nrm = max(abs(v) for v in F0)
mn = min(abs(v) for v in x)
say(f"  final: max|H_w| = {mp.nstr(nrm, 8)},  min |cell| = {mp.nstr(mn, 8)}")
say(f"  ({time.time()-t0:.0f} s at {mp.mp.dps} digits)")
OUT["cegar_m20"] = {"cells": nv, "supported_mixed": len(s.mixed),
                    "float_best": best[0], "mp_dps": mp.mp.dps,
                    "final_max_abs_H": mp.nstr(nrm, 12),
                    "min_abs_cell": mp.nstr(mn, 12),
                    "solution": [mp.nstr(v, 25) for v in x]}
with open(os.path.join(HERE, "results_o_refine.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_o_refine.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("O DONE")

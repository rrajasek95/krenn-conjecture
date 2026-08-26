#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- CONTROL for the float existence search of run_t6.

The harness must FAIL where the campaign has a committed impossibility:
no exact d=3 source on N=6 sites.  If the same optimiser finds a d=3/N=6
"solution", the d=2 hits of run_t6 are worthless.  (Float only; no verdict.)
"""
from __future__ import annotations
import json, os, sys
from itertools import combinations, product
import numpy as np
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import w12_core as C  # noqa: E402


def build(n, q):
    edges = list(combinations(range(n), 2))
    eidx = {e: k for k, e in enumerate(edges)}
    matchings = [[eidx[e] for e in m] for m in C.perfect_matchings(tuple(range(n)))]
    words = list(product(range(q), repeat=n))
    return edges, matchings, words


def residuals(x, q, edges, matchings, words):
    vals = x.view(np.complex128).reshape(len(edges), q * q)
    out = []
    for w in words:
        h = 0j
        for m in matchings:
            t = 1 + 0j
            for e in m:
                u, v = edges[e]
                t *= vals[e][q * w[u] + w[v]]
            h += t
        out.append(h - (1.0 if len(set(w)) == 1 else 0.0))
    r = np.array(out, dtype=np.complex128)
    return np.concatenate([r.real, r.imag])


def search(n, q, trials, seed=0):
    edges, matchings, words = build(n, q)
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(trials):
        x0 = rng.normal(size=len(edges) * q * q * 2) * 0.7
        try:
            sol = least_squares(residuals, x0, args=(q, edges, matchings, words),
                                xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=3000)
        except Exception:                                    # noqa: BLE001
            continue
        cost = float(np.max(np.abs(residuals(sol.x, q, edges, matchings, words))))
        if best is None or cost < best:
            best = cost
        if cost < 1e-11:
            return cost
    return best


out = {}
for (n, q, trials, note) in ((4, 2, 30, "known solvable"),
                             (6, 3, 60, "COMMITTED IMPOSSIBLE"),
                             (8, 3, 25, "the open case")):
    c = search(n, q, trials)
    out[f"N{n}_d{q}"] = {"best_max_residual": c, "note": note,
                         "float_verdict": "SOLVED" if c < 1e-9 else "not found"}
    print(f"N={n} d={q} ({note}): best |residual| = {c:.3e} -> "
          f"{out[f'N{n}_d{q}']['float_verdict']}", flush=True)
json.dump(out, open(os.path.join(HERE, "results_t6b_control.json"), "w"), indent=1)
print("wrote results_t6b_control.json")

#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- cheap harness control for the float search.

The optimiser must FAIL on a d=2, N=8 instance that is impossible for a
one-line reason: restrict the template to the single perfect matching
{01,23,45,67}.  Then H_w = prod_i A_{2i,2i+1}[w_{2i}][w_{2i+1}], so
H(0^8) != 0 and H(1^8) != 0 force every diagonal entry nonzero, whence
H(0,0,0,0,1,1,1,1) = A01[0][0] A23[0][0] A45[1][1] A67[1][1] != 0 -- but that
word is mixed.  Impossible.  If least_squares 'solves' it, the harness lies."""
from __future__ import annotations
import json, os
import numpy as np
from scipy.optimize import least_squares
from itertools import product
HERE = os.path.dirname(os.path.abspath(__file__))
EDGES = [(0, 1), (2, 3), (4, 5), (6, 7)]
WORDS = list(product((0, 1), repeat=8))


def res(x):
    v = x.view(np.complex128).reshape(4, 4)
    out = []
    for w in WORDS:
        h = 1 + 0j
        for k, (u, t) in enumerate(EDGES):
            h *= v[k][2 * w[u] + w[t]]
        out.append(h - (1.0 if len(set(w)) == 1 else 0.0))
    r = np.array(out)
    return np.concatenate([r.real, r.imag])


rng = np.random.default_rng(0)
best = None
for _ in range(200):
    sol = least_squares(res, rng.normal(size=32) * 0.8, xtol=1e-15,
                        ftol=1e-15, gtol=1e-15, max_nfev=3000)
    c = float(np.max(np.abs(res(sol.x))))
    best = c if best is None else min(best, c)
print(f"HARNESS CONTROL (provably impossible d=2/N=8 instance): "
      f"best |residual| over 200 restarts = {best:.4e}  -> "
      f"{'FAILED TO FIND (correct)' if best > 1e-6 else 'BUG: claims a solution'}")
json.dump({"best_max_residual": best,
           "harness_correct": bool(best > 1e-6)},
          open(os.path.join(HERE, "results_t6c_harness_control.json"), "w"),
          indent=1)

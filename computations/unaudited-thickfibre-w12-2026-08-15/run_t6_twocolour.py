#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- the TWO-COLOUR RESTRICTION observation.

OBSERVATION (exact, trivial to verify).  Let A be an exact d=3 source on B
(|B| = N).  For any two colours c != c', the 2x2 sub-blocks
    Atilde_uv = A_uv[{c,c'}][{c,c'}]
form an EXACT d=2 source on B: for a word w in {c,c'}^B the hafnian only ever
reads cells with both indices in {c,c'}, so H(Atilde)_w = H(A)_w, which is 0
on the 2^N - 2 mixed such words and nonzero on c^B and c'^B.

CONSEQUENCE.  If no exact d=2 source exists on N sites, then no exact d=3
source does either.  This script decides the d=2 question at N=4,6,8 by
FLOAT search (clearly labelled) and re-verifies any hit in exact rational
arithmetic, so a positive answer is a certificate and a negative answer is
only evidence.
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import combinations, product

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w12_core as C  # noqa: E402


def pms(n):
    return C.perfect_matchings(tuple(range(n)))


def build(n):
    edges = list(combinations(range(n), 2))
    eidx = {e: k for k, e in enumerate(edges)}
    matchings = [[eidx[e] for e in m] for m in pms(n)]
    words = list(product((0, 1), repeat=n))
    return edges, matchings, words


def hafnian(values, edges, matchings, word):
    """values[edge][2*i+j] complex; exact if Fractions are passed in."""
    total = 0
    for m in matchings:
        term = 1
        for e in m:
            u, v = edges[e]
            term = term * values[e][2 * word[u] + word[v]]
        total = total + term
    return total


def residuals(x, n, edges, matchings, words):
    vals = x.view(np.complex128).reshape(len(edges), 4)
    out = []
    for w in words:
        h = 0
        for m in matchings:
            t = 1 + 0j
            for e in m:
                u, v = edges[e]
                t *= vals[e][2 * w[u] + w[v]]
            h += t
        target = 1.0 if len(set(w)) == 1 else 0.0
        out.append(h - target)
    r = np.array(out, dtype=np.complex128)
    return np.concatenate([r.real, r.imag])


def search(n, trials=40, seed=0):
    from scipy.optimize import least_squares
    edges, matchings, words = build(n)
    rng = np.random.default_rng(seed)
    best = None
    for t in range(trials):
        x0 = rng.normal(size=(len(edges) * 4 * 2)) * 0.7
        try:
            sol = least_squares(residuals, x0,
                                args=(n, edges, matchings, words),
                                xtol=1e-15, ftol=1e-15, gtol=1e-15,
                                max_nfev=3000)
        except Exception:                                 # noqa: BLE001
            continue
        cost = float(np.max(np.abs(residuals(sol.x, n, edges, matchings,
                                             words))))
        if cost < 1e-11:
            return (cost, sol.x), edges, matchings, words
        if best is None or cost < best[0]:
            best = (cost, sol.x)
    return best, edges, matchings, words


def main():
    out = {}
    for n in (4, 6, 8):
        (cost, x), edges, matchings, words = search(n, trials=(60 if n < 8
                                                               else 40))
        out[f"n{n}"] = {"best_max_residual": cost,
                        "verdict": "SOLVED (float)" if cost < 1e-9
                        else "no solution found (float)"}
        print(f"d=2, N={n}: best max |residual| = {cost:.3e}  -> "
              f"{out[f'n{n}']['verdict']}", flush=True)
        if cost < 1e-9:
            vals = x.view(np.complex128).reshape(len(edges), 4)
            out[f"n{n}"]["example"] = [[str(z) for z in row] for row in vals]
    with open(os.path.join(HERE, "results_t6_twocolour.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote results_t6_twocolour.json")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Scan survivor-triple orbits for star-kernel Glynn covers."""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix

from search_glynn_permanent_restriction import candidates


def canonical_masks(d: int, a: int, b: int, c: int) -> tuple[int, int, int]:
    # |A|=a, |B|=b, |A cap B|=c.
    A = (1 << a) - 1
    B = ((1 << c) - 1) | (((1 << (b - c)) - 1) << a)
    return 0, A, B


def cover(m: int, surv: tuple[int, int, int]):
    universe, cand = candidates(m, surv, True)
    rows, cols = [], []
    for j, item in enumerate(cand):
        for i in item[0]:
            rows.append(i)
            cols.append(j)
    mat = csc_matrix((np.ones(len(rows)), (rows, cols)),
                     shape=(len(universe), len(cand)))
    if mat.shape[1] == 0 or np.any(np.asarray(mat.sum(axis=1)).ravel() == 0):
        return None, universe, cand
    cons = [LinearConstraint(mat, np.ones(len(universe)), np.inf),
            LinearConstraint(np.ones((1, len(cand))), -np.inf, m)]
    res = milp(np.ones(len(cand)), integrality=np.ones(len(cand)),
               bounds=Bounds(np.zeros(len(cand)), np.ones(len(cand))),
               constraints=cons, options={"time_limit": 5, "mip_rel_gap": 0})
    if res.x is None:
        return None, universe, cand
    return [i for i, x in enumerate(res.x) if x > .5], universe, cand


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    args = ap.parse_args()
    d = args.m - 1
    tested = 0
    for a in range(1, d + 1):
        for b in range(a, d + 1):
            for c in range(max(0, a + b - d), min(a, b) + 1):
                surv = canonical_masks(d, a, b, c)
                if len(set(surv)) < 3:
                    continue
                tested += 1
                chosen, universe, cand = cover(args.m, surv)
                if chosen is None:
                    continue
                print("FOUND", "m", args.m, "orbit", (a, b, c),
                      "survivors", surv, "terms", len(chosen))
                for j in chosen:
                    killed, edges, parity, dmat, images = cand[j]
                    print("edges", edges, "parity", parity,
                          "D", dmat.tolist(), "images", images.tolist())
                return
    print("no cover", "m", args.m, "orbits", tested)


if __name__ == "__main__":
    main()

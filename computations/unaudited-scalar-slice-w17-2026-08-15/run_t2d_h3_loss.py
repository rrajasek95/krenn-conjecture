#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- T2(d): does the rank-one re-basing lose at h = 3 too?

At h = 3 the cap error is AFFINE in the internal blocks for a FIXED cap K
(the r^3 term is x-free and the 3 s r^2 x term is linear in x).  So a pair
with a general-cap witness can be built directly:

  1. random star blocks A_pa, A_qa, random A_pq, random rank-3 cap K with
     s kappa_0 kappa_1 kappa_2 != 0;
  2. solve the affine system E_pq(K) = 0 for the 15 internal blocks
     (729 equations, 135 unknowns, exact);
  3. verify E_pq(K) = 0 with the independent matching-sum evaluator;
  4. decide whether ANY admissible rank-one cap is clean at that pair
     (Singular over Q, plus a modular cross-check).

A source produced this way with no rank-one witness is an h = 3 loss of the
re-basing, at the same pair -- the eight-site analogue of T1's six-site
counterexamples.
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import w17_h3 as H3
from w17_core import (COLORS, ekey, matrix_rank, oriented, run_singular)
from w17_general import R_general, cap_scalars_general, general_cap_error


def random_source(rng, n=8, lo=-4, hi=4):
    return {(u, v): [[Fraction(rng.randint(lo, hi)) for _ in range(3)]
                     for _ in range(3)]
            for u, v in combinations(range(n), 2)}


def solve_internal_for_cap(source, p, q, sites, K):
    """Internal blocks x with E_pq(K) = 0 (affine, exact) or None."""
    sites = tuple(sites)
    slot = {a: n for n, a in enumerate(sites)}
    s, _ = cap_scalars_general(source, p, q, K)
    matchings = H3.__dict__.get("_MATCH")
    from w17_core import perfect_matchings
    MU = perfect_matchings(sites)
    coords = [(a, b, ca, cb) for a, b in combinations(sites, 2)
              for ca in COLORS for cb in COLORS]
    index = {c: n for n, c in enumerate(coords)}
    rows = []
    Rcache = {}

    def R(a, b, ca, cb):
        key = (a, b, ca, cb)
        if key not in Rcache:
            Rcache[key] = R_general(source, p, q, K, a, b, ca, cb)
        return Rcache[key]

    for word in product(COLORS, repeat=6):
        wof = {a: word[slot[a]] for a in sites}
        const = Fraction(0)
        for M in MU:
            term = Fraction(1)
            for a, b in M:
                term *= R(a, b, wof[a], wof[b])
                if term == 0:
                    break
            const += term
        row = [Fraction(0)] * (len(coords) + 1)
        row[-1] = -const
        for a, b in combinations(sites, 2):
            rest = tuple(t for t in sites if t not in (a, b))
            tot = Fraction(0)
            for M in perfect_matchings(rest):
                term = Fraction(1)
                for c, d in M:
                    term *= R(c, d, wof[c], wof[d])
                    if term == 0:
                        break
                tot += term
            if tot:
                row[index[(a, b, wof[a], wof[b])]] += s * tot
        if any(x != 0 for x in row):
            rows.append(row)
    n = len(coords)
    mat = [list(r) for r in rows]
    piv_cols, rank = [], 0
    for col in range(n):
        piv = None
        for i in range(rank, len(mat)):
            if mat[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        head = mat[rank]
        for i in range(len(mat)):
            if i != rank and mat[i][col] != 0:
                f = mat[i][col] / head[col]
                mat[i] = [x - f * y for x, y in zip(mat[i], head)]
        piv_cols.append(col)
        rank += 1
    for i in range(rank, len(mat)):
        if all(x == 0 for x in mat[i][:n]) and mat[i][n] != 0:
            return None, rank
    x = [Fraction(0)] * n
    for r, col in enumerate(piv_cols):
        x[col] = mat[r][n] / mat[r][col]
    blocks = {}
    for (a, b, ca, cb), val in zip(coords, x):
        blocks.setdefault((a, b), [[Fraction(0)] * 3 for _ in range(3)])
        blocks[(a, b)][ca][cb] = val
    return blocks, rank


def main(trials=12):
    t0 = time.time()
    rng = random.Random(31415)
    p, q = 0, 1
    U = tuple(a for a in range(8) if a not in (p, q))
    print("== W17 T2(d): h = 3 general-cap witnesses vs rank-one witnesses ==")
    out = []
    losses = 0
    made = 0
    for trial in range(trials):
        src = random_source(rng)
        K = [[Fraction(rng.randint(-4, 4)) for _ in range(3)]
             for _ in range(3)]
        s, kappa = cap_scalars_general(src, p, q, K)
        if s == 0 or any(k == 0 for k in kappa) or matrix_rank(K) < 3:
            continue
        blocks, rank = solve_internal_for_cap(src, p, q, U, K)
        if blocks is None:
            print(f"  trial {trial}: affine system inconsistent (rank {rank})")
            continue
        for (a, b), blk in blocks.items():
            src[ekey(a, b)] = blk
        err = general_cap_error(src, p, q, K, U)
        if err:
            print(f"  trial {trial}: SOLVER ERROR, {len(err)} components")
            continue
        made += 1
        eqs, sbp = H3.rank_one_equations_h3(src, p, q, U)
        tag = f"L{trial}"
        rk1 = H3.parse_rk1(run_singular(H3.rk1_query(list(eqs.values()), sbp,
                                                    tag), timeout=900), tag)
        rk1m = H3.parse_rk1(run_singular(
            H3.rk1_query_modular(list(eqs.values()), sbp, tag, 32003),
            timeout=900), tag)
        iranks = [matrix_rank(oriented(src, a, b)) for a, b in combinations(U, 2)]
        print(f"  trial {trial}: general-cap witness YES (rank-3 cap, "
              f"affine rank {rank}), rank-one witness {rk1} (mod {rk1m}); "
              f"internal ranks {sorted(set(iranks))}, error components "
              f"{len(eqs)} [{time.time() - t0:.0f}s]")
        out.append({"trial": trial, "cap": [[str(x) for x in r] for r in K],
                    "s": str(s), "kappa": [str(k) for k in kappa],
                    "affine_rank": rank, "rank_one_witness": rk1,
                    "rank_one_modular": rk1m,
                    "internal_ranks": iranks,
                    "nonzero_components": len(eqs),
                    "blocks": {f"{a},{b}": [[str(x) for x in row]
                                            for row in src[(a, b)]]
                               for a, b in combinations(range(8), 2)}})
        if rk1 is False:
            losses += 1
        if made >= 8:
            break
    print(f"\n  built {made} eight-site pairs with an explicit general-cap "
          f"witness; of these {losses} have NO rank-one witness "
          f"(h = 3 losses of the re-basing)")
    with open(os.path.join(HERE, "results_t2d_h3_loss.json"), "w") as fh:
        json.dump({"made": made, "losses": losses, "records": out}, fh,
                  indent=1, default=str)
    print(f"wrote results_t2d_h3_loss.json [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()

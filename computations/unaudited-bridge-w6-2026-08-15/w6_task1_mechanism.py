#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- J.1c task (b): the exactness mechanism at a pair.

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

Establishes and exercises the identity that ties the pair block to its
neighbourhood.  Three stages:

  A. (EXP) verified exactly on random sources at N = 6 and N = 8 (an identity
     for EVERY source; no exactness needed).
  B. (STAR) the exactness consequence, exercised on the committed near-exact
     eight-site source: for every NON-CONSTANT colouring v of U,
     C(v) A_pq + P(v)M(v)Q(v)^T = 0.  The residual is exactly the GHZ defect
     of the two bad words, so the identity is checked as
         C(v) A_pq[i][j] + D(v)[i][j] = H_{(i,j,v)}
     with H the actual (near-exact) tensor.
  C. THE PINNING COROLLARY: for an exact source with C(v) != 0 for at least
     one non-constant v, the whole 3x3 block A_pq is a rational function of
     the rest of the source.  We measure, on the near-exact source and on
     exactly-solved local deformations, WHICH minors of A_pq are forced to
     vanish once det A_pq = 0 is imposed inside the pinned family.

Run: python3 w6_task1_mechanism.py
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, product

import w6_core as core
from w6_core import COLORS, require

P1 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-p1-2026-08-15")
if P1 not in sys.path:
    sys.path.insert(0, P1)


def random_source(rng, size, lo=-4, hi=4, zero_prob=0.0):
    src = {}
    for u, v in combinations(range(size), 2):
        src[(u, v)] = [[0 if rng.random() < zero_prob else rng.randint(lo, hi)
                        for _ in COLORS] for _ in COLORS]
    return src


# ------------------------------------------------------------------ stage A


def stage_a(trials=6):
    rng = random.Random(20260815)
    out = []
    for size in (6, 8):
        for trial in range(trials):
            src = random_source(rng, size,
                                zero_prob=0.4 if trial % 2 else 0.0)
            p, q = (0, 1) if trial % 3 else (2, 5)
            U = [x for x in range(size) if x not in (p, q)]
            if size == 8:
                words = [tuple(rng.randrange(3) for _ in U) for _ in range(12)]
            else:
                words = None
            checked, bad = core.verify_edge_expansion(src, size, p, q, words)
            out.append({"N": size, "pair": [p, q], "checked": checked,
                        "violations": bad})
            require(bad == 0, ("EXP violated", size, p, q))
    return out


# ------------------------------------------------------------------ stage B


def load_stage_a_source():
    import wsplit_sources as sources
    return sources.load_stage_a()


def stage_b(physical, sample=90, seed=11):
    """(STAR) residuals on the committed near-exact eight-site source."""
    rng = random.Random(seed)
    tensor = core.full_tensor(physical, 8)
    defects = [w for w, value in tensor.items()
               if value != (1 if len(set(w)) == 1 else 0)]
    universe = [w for w in product(COLORS, repeat=6) if len(set(w)) > 1]
    records = []
    for p, q in combinations(range(8), 2):
        U = [x for x in range(8) if x not in (p, q)]
        nonzero_C = 0
        star_violations = 0
        exp_violations = 0
        pinned = None
        block = core.oriented(physical, p, q)
        for vword in rng.sample(universe, sample):
            v = {u: vword[n] for n, u in enumerate(U)}
            if len(set(vword)) == 1:
                continue                      # constant U-word: not in (STAR)
            C, _M, _P, _Q, D = core.pair_expansion(physical, 8, p, q, v)
            if C:
                nonzero_C += 1
                if pinned is None:
                    pinned = [[Fraction(-D[i][j], 1) / C for j in COLORS]
                              for i in COLORS]
            for i in COLORS:
                for j in COLORS:
                    colour = dict(v)
                    colour[p], colour[q] = i, j
                    word = tuple(colour[u] for u in range(8))
                    if block[i][j] * C + D[i][j] != tensor[word]:
                        exp_violations += 1
                    if C * block[i][j] + D[i][j] != 0:
                        star_violations += 1
        records.append({
            "pair": [p, q],
            "sampled_nonconstant_U_words": sample,
            "nonconstant_U_words_with_C_nonzero": nonzero_C,
            "EXP_violations": exp_violations,
            "STAR_violations": star_violations,
            "pinned_equals_block": (pinned is not None
                                    and all(pinned[i][j] == block[i][j]
                                            for i in COLORS for j in COLORS)),
        })
    return {"ghz_defect_words": [list(w) for w in defects],
            "pairs": records}


# ------------------------------------------------------------------ stage C


def det3(matrix):
    return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
            - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
            + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))


def cofactor(matrix, i, j):
    rows = [r for r in COLORS if r != i]
    cols = [c for c in COLORS if c != j]
    return (matrix[rows[0]][cols[0]] * matrix[rows[1]][cols[1]]
            - matrix[rows[0]][cols[1]] * matrix[rows[1]][cols[0]])


def minor_profile(matrix):
    return {
        "det": det3(matrix) == 0,
        "cof_diag": [cofactor(matrix, c, c) == 0 for c in COLORS],
        "diag": [matrix[c][c] == 0 for c in COLORS],
        "rank": core.matrix_rank(matrix),
        "cells": len(core.cells(matrix)),
        "class": core.classify_block(matrix),
    }


def pinned_block(source, size, p, q):
    """A_pq as forced by (STAR): -(P M Q^T)/C at the first non-constant v."""
    U = [x for x in range(size) if x not in (p, q)]
    for vword in product(COLORS, repeat=len(U)):
        if len(set(vword)) == 1:
            continue
        v = {u: vword[n] for n, u in enumerate(U)}
        C, _M, _P, _Q, D = core.pair_expansion(source, size, p, q, v)
        if C:
            return [[Fraction(-D[i][j]) / C for j in COLORS] for i in COLORS], vword
    return None, None


def stage_c(seed=7, trials=400, size=6):
    """Deformation forcing: move the ENVIRONMENT, keep the pair block pinned.

    For a random environment (all blocks except A_pq) we compute the block
    A_pq forced by (STAR).  We then search, inside a one-parameter family of
    environments, for parameter values where det(pinned) = 0, and record the
    full minor profile there.  This is the exact test of

        "det A_pq = 0 at a pinned pair  =>  cofactor / diagonal vanishing too?"
    """
    rng = random.Random(seed)
    hits = []
    stats = {"samples": 0, "det_zero": 0,
             "det_zero_and_some_cof_zero": 0,
             "det_zero_and_some_diag_zero": 0,
             "det_zero_rank1": 0, "det_zero_rank2": 0, "det_zero_rank0": 0}
    for _ in range(trials):
        base = random_source(rng, size, lo=-3, hi=3,
                             zero_prob=rng.choice([0.0, 0.3, 0.5]))
        step = random_source(rng, size, lo=-2, hi=2, zero_prob=0.6)
        p, q = 0, 1
        block, vword = pinned_block(base, size, p, q)
        if block is None:
            continue
        # one-parameter family: environment + t * step (pair block excluded).
        values = []
        for t in range(-6, 7):
            src = {k: [[base[k][i][j] + t * step[k][i][j] for j in COLORS]
                       for i in COLORS] for k in base}
            src[(p, q)] = [[0] * 3 for _ in COLORS]
            blk, _ = pinned_block(src, size, p, q)
            if blk is None:
                continue
            values.append((t, blk))
        for t, blk in values:
            stats["samples"] += 1
            profile = minor_profile(blk)
            if profile["det"]:
                stats["det_zero"] += 1
                stats[f"det_zero_rank{profile['rank']}"] = stats.get(
                    f"det_zero_rank{profile['rank']}", 0) + 1
                if any(profile["cof_diag"]):
                    stats["det_zero_and_some_cof_zero"] += 1
                if any(profile["diag"]):
                    stats["det_zero_and_some_diag_zero"] += 1
                if len(hits) < 25:
                    hits.append({"t": t, "profile": profile,
                                 "block": [[str(x) for x in row] for row in blk]})
    return {"stats": stats, "samples": hits}


def main():
    print("UNAUDITED PROBE (W6) -- J.1c mechanism, HEAD 31cefe2", flush=True)
    report = {}

    print("== stage A: the edge expansion (EXP) is an identity ==", flush=True)
    report["stage_a"] = stage_a()
    for rec in report["stage_a"]:
        print(f"  N={rec['N']} pair={rec['pair']}: {rec['checked']} checks, "
              f"{rec['violations']} violations")

    print("== stage B: (STAR) on the committed near-exact 8-site source ==",
          flush=True)
    physical = load_stage_a_source()
    report["stage_b"] = stage_b(physical)
    print(f"  GHZ defect words: {report['stage_b']['ghz_defect_words']}")
    bad_exp = sum(r["EXP_violations"] for r in report["stage_b"]["pairs"])
    print(f"  total EXP violations over all 28 pairs: {bad_exp}")
    for rec in report["stage_b"]["pairs"]:
        print(f"  pair {rec['pair']}: C!=0 on {rec['nonconstant_U_words_with_C_nonzero']:4d}"
              f"/{rec['sampled_nonconstant_U_words']} sampled non-constant U-words, STAR residual words "
              f"{rec['STAR_violations']:3d}, pinned==block {rec['pinned_equals_block']}")

    print("== stage C: deformation forcing inside the pinned family (N=6) ==",
          flush=True)
    report["stage_c"] = stage_c()
    print(json.dumps(report["stage_c"]["stats"], indent=1))

    with open("results_mechanism.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print("wrote results_mechanism.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

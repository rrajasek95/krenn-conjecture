#!/usr/bin/env python3
"""A7 SUB-AUDIT -- ITEM A4: n = 5 spot checks the W20 probe did NOT do.

Strata (all EXHAUSTIVE within the stated value set, reduced only by exact
symmetries of the question):

  S0  ALL normals in {-1,0,1}^5 \ {0}, i.e. all 121 sign-representatives,
      swept over MULTISETS of 5 (per is symmetric in the columns, and
      ker(nv) = ker(-nv)); 234,531,275 multisets == all 121^5 = 25,937,424,601
      ordered configurations == all 242^5 unreduced normal tuples.
  S1  all 31 nonzero 0/1 normals (every possible SUPPORT pattern, with the
      most degenerate common value 1), multisets of 5: 324,632.
  S2  all 25 sign-reps of support <= 2 (the most zero-rich normals, where an
      empty common support is easiest to arrange), multisets of 5: 118,755.
  S3  the transversal-zero stratum: normal j vanishes exactly at coordinate j
      (so the common support is EMPTY -- the only regime where a
      counterexample can live once step (A) is granted) and every other entry
      is +-1: 8^5 = 32,768 configurations, exhaustive.
  S4  >= 2000 exact RANDOM RATIONAL instances (Fraction entries).

S0 is run with multiprocessing; everything is exact integer arithmetic.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction
from itertools import combinations_with_replacement, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from a7_core import (kernel_basis, is_common_coordinate,          # noqa: E402
                     per_vanishes_on_product, sign_reps)

CAND5 = sign_reps(5)
BASES5 = [kernel_basis(nv) for nv in CAND5]


def _chunk(i0):
    """all multisets of 5 indices with smallest index i0."""
    tested = 0
    vanishing = []
    violations = []
    rest = range(i0, len(CAND5))
    for tail in combinations_with_replacement(rest, 4):
        combo = (i0,) + tail
        tested += 1
        if per_vanishes_on_product([BASES5[k] for k in combo]):
            normals = [CAND5[k] for k in combo]
            vanishing.append([list(x) for x in normals])
            if not is_common_coordinate(normals):
                violations.append([list(x) for x in normals])
    return tested, vanishing, violations


def sweep_S0(nproc=16):
    import multiprocessing as mp
    t0 = time.time()
    tested = 0
    vanishing = []
    violations = []
    with mp.Pool(nproc) as pool:
        for tt, vv, bb in pool.imap_unordered(_chunk, range(len(CAND5))):
            tested += tt
            vanishing += vv
            violations += bb
    return dict(tag="S0 exhaustive {-1,0,1}^5 multisets",
                n_candidate_normals=len(CAND5), n_multisets_tested=tested,
                equivalent_ordered_configs=len(CAND5) ** 5,
                equivalent_unreduced_configs=(2 * len(CAND5)) ** 5,
                n_vanishing=len(vanishing), vanishing=vanishing[:12],
                n_violations=len(violations), violations=violations[:5],
                seconds=round(time.time() - t0, 1))


def sweep_generic(cand, tag, k=5):
    bases = [kernel_basis(nv) for nv in cand]
    tested = 0
    vanishing = []
    violations = []
    for combo in combinations_with_replacement(range(len(cand)), k):
        tested += 1
        if per_vanishes_on_product([bases[i] for i in combo]):
            normals = [cand[i] for i in combo]
            vanishing.append([list(x) for x in normals])
            if not is_common_coordinate(normals):
                violations.append([list(x) for x in normals])
    return dict(tag=tag, n_candidate_normals=len(cand),
                n_multisets_tested=tested, n_vanishing=len(vanishing),
                vanishing=vanishing[:12], n_violations=len(violations),
                violations=violations[:5])


def sweep_transversal():
    """normal j has its unique zero at coordinate j; other entries +-1."""
    signs = list(product((1, -1), repeat=4))
    tested = 0
    vanishing = []
    violations = []
    for pick in product(range(len(signs)), repeat=5):
        normals = []
        for j in range(5):
            s = signs[pick[j]]
            nv = []
            t = 0
            for i in range(5):
                if i == j:
                    nv.append(0)
                else:
                    nv.append(s[t])
                    t += 1
            normals.append(tuple(nv))
        tested += 1
        if per_vanishes_on_product([kernel_basis(nv) for nv in normals]):
            vanishing.append([list(x) for x in normals])
            if not is_common_coordinate(normals):
                violations.append([list(x) for x in normals])
    return dict(tag="S3 transversal-zero stratum, entries +-1",
                n_tested=tested, n_vanishing=len(vanishing),
                n_violations=len(violations), violations=violations[:5],
                note="common support is EMPTY for every configuration here")


def random_rationals(n=5, trials=5000, seed=101):
    rng = random.Random(seed)
    tested = 0
    nvan = 0
    bad = []
    while tested < trials:
        normals = []
        for _ in range(n):
            nv = tuple(Fraction(rng.randint(-9, 9), rng.randint(1, 7))
                       for _ in range(n))
            normals.append(nv)
        if not all(any(x) for x in normals):
            continue
        tested += 1
        v = per_vanishes_on_product([kernel_basis(nv) for nv in normals])
        c = is_common_coordinate(normals)
        if v:
            nvan += 1
        if v != c:
            bad.append([[str(x) for x in nv] for nv in normals])
    return dict(n=n, trials=tested, n_vanishing=nvan, n_violations=len(bad),
                violations=bad[:5])


def random_sparse_rationals(n=5, trials=5000, seed=202, pzero=0.35):
    """random rationals WITH zeros, so that the common support is often
    empty -- the only regime a counterexample could live in."""
    rng = random.Random(seed)
    tested = 0
    nvan = 0
    bad = []
    empties = 0
    while tested < trials:
        normals = []
        for _ in range(n):
            nv = tuple(Fraction(0) if rng.random() < pzero
                       else Fraction(rng.randint(-9, 9) or 4,
                                     rng.randint(1, 7)) for _ in range(n))
            normals.append(nv)
        if not all(any(x) for x in normals):
            continue
        tested += 1
        if not set.intersection(*[set(i for i in range(n) if nv[i])
                                  for nv in normals]):
            empties += 1
        v = per_vanishes_on_product([kernel_basis(nv) for nv in normals])
        c = is_common_coordinate(normals)
        if v:
            nvan += 1
        if v != c:
            bad.append([[str(x) for x in nv] for nv in normals])
    return dict(n=n, trials=tested, n_with_empty_common_support=empties,
                n_vanishing=nvan, n_violations=len(bad), violations=bad[:5])


def main():
    res = {"_header": "A7 SUB-AUDIT -- A4, n=5 batteries. Exact only."}
    res["S1_zero_one_all_supports"] = sweep_generic(
        [v for v in product((0, 1), repeat=5) if any(v)],
        "S1 all 0/1 normals (all support patterns)")
    print("S1:", res["S1_zero_one_all_supports"], flush=True)
    res["S2_low_support"] = sweep_generic(
        [v for v in sign_reps(5) if sum(1 for x in v if x) <= 2],
        "S2 support <= 2, {-1,0,1}")
    print("S2:", res["S2_low_support"], flush=True)
    res["S3_transversal"] = sweep_transversal()
    print("S3:", res["S3_transversal"], flush=True)
    res["S4_random_rationals"] = random_rationals()
    print("S4:", res["S4_random_rationals"], flush=True)
    res["S4b_random_sparse_rationals"] = random_sparse_rationals()
    print("S4b:", res["S4b_random_sparse_rationals"], flush=True)
    res["S0_exhaustive"] = sweep_S0()
    print("S0:", res["S0_exhaustive"], flush=True)
    json.dump(res, open(os.path.join(HERE, "a7_results_A4_n5.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()

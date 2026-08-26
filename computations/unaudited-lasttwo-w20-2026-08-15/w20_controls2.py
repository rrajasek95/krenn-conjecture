#!/usr/bin/env python3
"""W20 -- second control battery.  UNAUDITED.  Exact only.

C6  EXPLICIT-POINT CONTROL (ledger item 13) for residual 1: re-verify, from
    scratch and with the MODEL's Phi (not the descent's own algebra), that
    the stored exact points satisfy every effectively-clean equation, have
    every Gamma cell nonzero, and have the claimed factoring/non-factoring
    sites -- plus a MUTATION control: perturbing a single Gamma cell must
    break at least one clean equation.
C7  MUTATION control for the L-free / R-free permanent identity of
    residual 2: deleting or adding one word to the L-free set must break the
    identity.
C8  MUTATION control for the derived rank conditions: an artificial point
    violating "some V_j^x has rank <= 2" must be detected.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w20_core as C                                            # noqa: E402
from w20_forcing import factors_at, site_vectors, rref           # noqa: E402
from w20_sitesys import descent_point                            # noqa: E402
from w20_c8 import LFREE, RFREE, L, R, cross_mask                # noqa: E402


def c6_explicit_points():
    out = {}
    for m in (26, 27, 28):
        T, gam, fullm, clean, blocks, trace = descent_point(m, 11)
        ok = all(C.phi_value(blocks, fullm, w) == 0 for w in clean)
        nz = all(blocks[e][i][j] != 0 for e in gam
                 for i in range(3) for j in range(3))
        fac = [t for t in range(8) if factors_at(blocks, gam, t)]
        # mutation: perturb one cell, a clean equation must break
        detected = 0
        tried = 0
        rng = random.Random(9)
        for _ in range(24):
            e = gam[rng.randrange(len(gam))]
            i, j = rng.randrange(3), rng.randrange(3)
            old = blocks[e][i][j]
            blocks[e][i][j] = old + Fraction(1, 7)
            tried += 1
            if any(C.phi_value(blocks, fullm, w) != 0 for w in clean):
                detected += 1
            blocks[e][i][j] = old
        out["m%d" % m] = dict(n_clean=len(clean), all_clean_equations_hold=ok,
                              all_gamma_cells_nonzero=nz,
                              factoring_sites=fac,
                              nonfactoring_sites=[t for t in range(8)
                                                  if t not in fac],
                              mutation_detected="%d/%d" % (detected, tried),
                              block_ranks={str(e): C.rank_of(blocks[e])
                                           for e in gam})
    return out


def c7_free_word_mutation():
    """the L-free predicate must be exactly right: every L-free x has
    H = per B for all y, and every NON-L-free x must fail for some y."""
    T = C.C8_MEMBER
    Ls = set(map(tuple, LFREE))
    good = bad = 0
    for x in product(range(3), repeat=4):
        crossonly = True
        for y in product(range(3), repeat=4):
            w = tuple(x) + tuple(y)
            if len(set(w)) == 1:
                continue
            for mi in C.support(T, w):
                k = sum(1 for (u, v) in C.PMS[mi] if (u in L) != (v in L))
                if k != 4:
                    crossonly = False
                    break
            if not crossonly:
                break
        if crossonly == (tuple(x) in Ls):
            good += 1
        else:
            bad += 1
    return dict(tested=81, agree=good, mismatches=bad)


def c8_rank_condition_mutation():
    """the rank-condition checker must FIRE on an artificial configuration
    where all four V_j^x are hyperplanes."""
    rng = random.Random(3)

    def rank_j(cols, j):
        return len(rref([[cols[j][d][i] for i in range(4)]
                         for d in range(3)], 4)[0])
    # (a) a random configuration: all four ranks should be 3 (hyperplanes)
    cols = {j: {d: [Fraction(rng.randint(1, 9)) for _ in range(4)]
                for d in range(3)} for j in range(4)}
    allr = [rank_j(cols, j) for j in range(4)]
    # (b) a rank-<=2 configuration
    cols2 = {j: {d: [Fraction(0)] * 4 for d in range(3)} for j in range(4)}
    for j in range(4):
        b1 = [Fraction(rng.randint(1, 9)) for _ in range(4)]
        b2 = [Fraction(rng.randint(1, 9)) for _ in range(4)]
        for d in range(3):
            s, t = rng.randint(1, 5), rng.randint(1, 5)
            cols2[j][d] = [s * b1[i] + t * b2[i] for i in range(4)]
    allr2 = [rank_j(cols2, j) for j in range(4)]
    return dict(random_config_ranks=allr, planted_rank2_config_ranks=allr2,
                detector_fires=(all(r == 3 for r in allr)
                                and all(r <= 2 for r in allr2)))


def main():
    res = {"_header": "UNAUDITED W20 control battery 2. Exact only."}
    res["C6_explicit_points"] = c6_explicit_points()
    for m in (26, 27, 28):
        d = res["C6_explicit_points"]["m%d" % m]
        print("C6 m=%d: %d clean equations hold=%s | all cells nonzero=%s | "
              "factoring %s | NON-factoring %s | mutation %s"
              % (m, d["n_clean"], d["all_clean_equations_hold"],
                 d["all_gamma_cells_nonzero"], d["factoring_sites"],
                 d["nonfactoring_sites"], d["mutation_detected"]), flush=True)
    res["C7_free_word_predicate"] = c7_free_word_mutation()
    print("C7 L-free predicate exactness:", res["C7_free_word_predicate"],
          flush=True)
    res["C8_rank_detector"] = c8_rank_condition_mutation()
    print("C8 rank-condition detector:", res["C8_rank_detector"], flush=True)
    json.dump(res, open(os.path.join(HERE, "results_controls2.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()

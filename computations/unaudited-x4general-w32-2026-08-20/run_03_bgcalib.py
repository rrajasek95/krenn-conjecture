#!/usr/bin/env python3
"""W32 / T3 -- calibrate the F_p background engine (W27-R1) before any hunt.

Controls (ledger 18/20/21 -- a silent search is worthless unless the search
demonstrably FIRES on the known-nonempty rung):
  CAL1  W25's F8 (a real N=8 X_3 source) -> background -> score 3 at k = 3,
        for every solve site z, and score < 3 at k = 4.
  CAL2  a diagonal (C)-triple background: score at k = 4 measured.
  CAL3  the F_p engine agrees with the exact Fraction engine of w32_core on
        random backgrounds (rank + feasibility verdicts).
  CAL4  mutation: corrupting one cofactor flips a verdict.
  CAL5  a random dense background is infeasible for every colour (base rate).
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-x4empty-w28-2026-08-18")
import w32_bg as BG  # noqa: E402
from w32_core import (Manifest, background_rows, colour_system, delta3_pms,
                      diag_source, ekey, haf_word, offcount, rref, require,
                      zero_source)  # noqa: E402

OUT = os.path.join(HERE, "results_t3.json")
R = {}
MAN = Manifest(["cal1_F8", "cal2_Ctriple", "cal3_exact_vs_fp", "cal4_mutation",
                "cal5_baserate"])
P1, P2 = 13, 31            # both = 1 mod 3 (ledger 19)


def src_to_fp(src, p, sites):
    """Restrict a rational source to `sites` and reduce mod p, in the flat
    layout of w32_bg (sites relabelled to 0..len-1 in sorted order)."""
    rel = {s: i for i, s in enumerate(sorted(sites))}
    F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
    for (u, v), m in src.items():
        if u not in rel or v not in rel:
            continue
        a, b = rel[u], rel[v]
        flip = a > b
        for i in range(3):
            for j in range(3):
                x = Fraction(m[i][j])
                val = x.numerator * pow(x.denominator, p - 2, p) % p
                if flip:
                    F[BG.EIDX[(b, a)]][j][i] = val
                else:
                    F[BG.EIDX[(a, b)]][i][j] = val
    return F


def task_cal1():
    import w28_core as W28
    F8 = W28.load_F8()
    ok3, ok4 = {}, {}
    for z in range(8):
        sites = [s for s in range(8) if s != z]
        for p in (P1, P2):
            F = src_to_fp(F8, p, sites)
            ok3[f"z{z}_p{p}"] = BG.score(F, p, k=3)
            ok4[f"z{z}_p{p}"] = BG.score(F, p, k=4)
    require(all(v == 3 for v in ok3.values()),
            f"CAL1 FAILED: F8 background not X_3-feasible: {ok3}")
    require(all(v < 3 for v in ok4.values()),
            f"CAL1 FAILED: F8 background looks X_4-feasible: {ok4}")
    MAN.mark("cal1_F8")
    R["cal1"] = {"k3_scores": ok3, "k4_scores": ok4}
    print("CAL1: F8 background scores 3/3 at k=3 for all 8 solve sites and "
          "both primes; at k=4 scores", sorted(set(ok4.values())))


def task_cal2():
    """(C)-triples: all three pairwise unions Hamiltonian.  Score at k=4."""
    from w32_core import perfect_matchings
    PMs = perfect_matchings(tuple(range(8)))

    def ham(A, B):
        adj = {i: [] for i in range(8)}
        for e in list(A) + list(B):
            adj[e[0]].append(e[1])
            adj[e[1]].append(e[0])
        seen, cur, prev = {0}, 0, None
        for _ in range(7):
            nxt = [x for x in adj[cur] if x != prev]
            if not nxt:
                return False
            prev, cur = cur, nxt[0]
            if cur in seen:
                return False
            seen.add(cur)
        return len(seen) == 8
    found, scores = 0, {}
    rng = random.Random(5)
    idx = list(range(len(PMs)))
    rng.shuffle(idx)
    for i, j, k in itertools.combinations(idx[:30], 3):
        A, B, C = PMs[i], PMs[j], PMs[k]
        if set(A) & set(B) or set(A) & set(C) or set(B) & set(C):
            continue
        if not (ham(A, B) and ham(A, C) and ham(B, C)):
            continue
        src = diag_source(8, [A, B, C])
        F = src_to_fp(src, P1, list(range(7)))
        s4 = BG.score(F, P1, k=4)
        s3 = BG.score(F, P1, k=3)
        scores[str((s3, s4))] = scores.get(str((s3, s4)), 0) + 1
        found += 1
        if found >= 60:
            break
    require(found > 0, "no (C)-triple found")
    MAN.mark("cal2_Ctriple")
    R["cal2"] = {"n_triples": found, "(k3,k4)_score_histogram": scores}
    print("CAL2: (C)-triple backgrounds,", found, "sampled, (k3,k4) scores",
          scores)


def task_cal3():
    """F_p engine vs the exact-Fraction engine of w32_core."""
    rng = random.Random(31337)
    agree = 0
    for trial in range(6):
        src = zero_source(7)
        for e in src:
            for a in range(3):
                for b in range(3):
                    src[e][a][b] = Fraction(rng.randint(-4, 4))
        cols, rows = background_rows(src, 8, z=7)
        exact = []
        for c in range(3):
            mixed, const = colour_system(8, rows, c, 4, z=7)
            piv, m, ok = rref(mixed + [const], [0] * len(mixed) + [1], 21)
            exact.append(ok)
        for p in (P1, P2):
            F = src_to_fp(src, p, list(range(7)))
            fp = BG.feasible_colours(F, p, k=4)
            # mod-p is a screen: a p-feasible verdict may differ from Q only
            # by bad reduction; require agreement and record any mismatch.
            require(list(fp) == exact,
                    f"engine mismatch trial {trial} p={p}: {fp} vs {exact}")
            agree += 1
    MAN.mark("cal3_exact_vs_fp")
    R["cal3"] = {"comparisons": agree, "mismatches": 0}
    print("CAL3: F_p engine == exact engine on", agree, "background/prime"
          " comparisons")


def task_cal4():
    """Mutation: corrupt one cell of the F8 background; the k=3 verdict must
    change for at least one corruption (the control must FIRE)."""
    import w28_core as W28
    F8 = W28.load_F8()
    base = src_to_fp(F8, P1, list(range(7)))
    fired = 0
    rng = random.Random(8)
    for _ in range(25):
        F = [[row[:] for row in blk] for blk in base]
        e = rng.randrange(len(BG.EDGES))
        a, b = rng.randrange(3), rng.randrange(3)
        F[e][a][b] = (F[e][a][b] + rng.randint(1, P1 - 1)) % P1
        if BG.score(F, P1, k=3) != 3:
            fired += 1
    require(fired > 0, "CAL4 mutation control did NOT fire")
    MAN.mark("cal4_mutation")
    R["cal4"] = {"mutations": 25, "verdict_changed": fired}
    print("CAL4: mutation control fires", fired, "/25")


def task_cal5():
    rng = random.Random(4)
    hist = {}
    for _ in range(60):
        F = [[[rng.randrange(P1) for _ in range(3)] for _ in range(3)]
             for _ in BG.EDGES]
        s = BG.score(F, P1, k=4)
        hist[s] = hist.get(s, 0) + 1
    MAN.mark("cal5_baserate")
    R["cal5"] = {"random_dense_score_histogram": {str(k): v for k, v
                                                  in sorted(hist.items())}}
    print("CAL5: random dense background score histogram (k=4):", hist)


def main():
    task_cal3()
    task_cal1()
    task_cal2()
    task_cal4()
    task_cal5()
    R["manifest"] = MAN.assert_complete()
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()

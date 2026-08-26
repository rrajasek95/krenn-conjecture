#!/usr/bin/env python3
"""A9-01: link-8 (product formula + hafnian engines) and the profile claims.

1. haf_dp vs haf_pm vs W29's engine vs W28's engine, random exact inputs.
2. THE PRODUCT FORMULA: H_w (raw 105-matching sum with 3x3 blocks) equals
   prod_c haf(t^c|w^{-1}(c)) -- 50 random diagonal sources x all 3^8 words.
3. Mutation control: a NON-diagonal source must BREAK the product formula.
4. The profile claim: at N=8 every even profile has a part of size >= 4, so
   EXACT = X_4 for diagonal sources (and the analogue at N=4,6,10,12).
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

BASE = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a9-2026-08-20"
W29 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-diagclose-w29-2026-08-19"
W28 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-x4empty-w28-2026-08-18"
for p in (BASE, W29, W28):
    if p not in sys.path:
        sys.path.insert(0, p)
import a9_haf as H                                                   # noqa: E402

RES = {}
OUT = f"{BASE}/results_a9_01_basics.json"


def ck(tag=""):
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print(f"   [ck {tag}]", flush=True)


def rand_weights(rng, V, dens=0.6, lo=-5, hi=5):
    t = {}
    for e in combinations(V, 2):
        if rng.random() < dens:
            v = Fraction(rng.randint(lo, hi), rng.randint(1, 3))
            if v != 0:
                t[e] = v
    return t


def part1_engines(trials=60, seed=7):
    import w29_core as C
    import w28_core as K
    rng = random.Random(seed)
    bad = []
    for it in range(trials):
        n = rng.choice([4, 6, 8])
        V = tuple(range(n))
        t = rand_weights(rng, V, dens=rng.choice([0.3, 0.6, 1.0]))
        for m in (0, 2, 4, 6, 8):
            if m > n:
                continue
            S = tuple(sorted(rng.sample(V, m)))
            a = H.haf_dp(t, S)
            b = H.haf_pm(t, S)
            c = C.haf(t, S)
            d = K.haf_w(t, S, Fraction(0), Fraction(1))
            if not (a == b == c == d):
                bad.append((it, n, S, str(a), str(b), str(c), str(d)))
    return {"trials": trials, "disagreements": len(bad), "examples": bad[:4],
            "PASS": not bad}


def part2_product_formula(nsrc=50, n=8, seed=13):
    """RAW 105-matching evaluation vs prod_c haf(t^c|w^{-1}(c))."""
    rng = random.Random(seed)
    V = tuple(range(n))
    npm = len(H.perfect_matchings(V))
    words = list(product(range(3), repeat=n))
    bad = []
    t0 = time.time()
    for s in range(nsrc):
        ts = [rand_weights(rng, V, dens=rng.choice([0.35, 0.7, 1.0]))
              for _ in range(3)]
        A = H.diag_blocks(ts, V)
        for w in words:
            raw = H.H_word(A, w, V)
            prd = Fraction(1)
            for c in range(3):
                prd = prd * H.haf_dp(ts[c], tuple(v for v in V if w[v] == c))
            if raw != prd:
                bad.append((s, w, str(raw), str(prd)))
                if len(bad) > 5:
                    return {"PASS": False, "examples": bad}
    return {"n_sources": nsrc, "n_words": len(words), "n_pm": npm,
            "disagreements": len(bad), "PASS": not bad,
            "secs": round(time.time() - t0, 1)}


def part3_mutation_nondiagonal(n=8, seed=21, trials=6):
    """CONTROL: put ONE off-diagonal entry in ONE block; the product formula
    must then FAIL for at least one word (else the test above is vacuous)."""
    rng = random.Random(seed)
    V = tuple(range(n))
    words = list(product(range(3), repeat=n))
    fired = 0
    detail = []
    for _ in range(trials):
        ts = [rand_weights(rng, V, dens=1.0) for _ in range(3)]
        A = H.diag_blocks(ts, V)
        e = rng.choice(list(combinations(V, 2)))
        i, j = rng.sample(range(3), 2)
        A[e][i][j] = Fraction(rng.randint(1, 4))
        hit = None
        for w in words:
            raw = H.H_word(A, w, V)
            prd = Fraction(1)
            for c in range(3):
                prd = prd * H.haf_dp(ts[c], tuple(v for v in V if w[v] == c))
            if raw != prd:
                hit = (e, i, j, w)
                break
        if hit:
            fired += 1
            detail.append(str(hit))
    return {"trials": trials, "fired": fired, "PASS": fired == trials,
            "examples": detail[:3]}


def part4_profiles():
    out = {}
    for n in (4, 6, 8, 10, 12):
        profs = H.even_profiles(n)
        offs = sorted({n - max(p) for p in profs if max(p) != n})
        out[f"n{n}"] = {"n_even_profiles": len(profs),
                        "mixed_offcounts": offs,
                        "max_offcount": max(offs),
                        "EXACT_equals_X": max(offs)}
    out["N8_EXACT_IS_X4"] = out["n8"]["max_offcount"] == 4
    out["N6_EXACT_IS_X4"] = out["n6"]["max_offcount"] == 4
    out["N10_EXACT_IS_X6"] = out["n10"]["max_offcount"] == 6
    return out


def main():
    t0 = time.time()
    print("=== A9-01 ===", flush=True)
    RES["p4_profiles"] = part4_profiles()
    print("p4", RES["p4_profiles"]["n8"], flush=True)
    ck("p4")
    RES["p1_engines"] = part1_engines()
    print("p1", RES["p1_engines"], flush=True)
    ck("p1")
    RES["p3_mutation_nondiagonal"] = part3_mutation_nondiagonal()
    print("p3", RES["p3_mutation_nondiagonal"], flush=True)
    ck("p3")
    RES["p2_product_formula"] = part2_product_formula()
    print("p2", RES["p2_product_formula"], flush=True)
    RES["secs"] = round(time.time() - t0, 1)
    ck("final")


if __name__ == "__main__":
    main()

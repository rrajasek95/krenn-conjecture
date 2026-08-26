#!/usr/bin/env python3
"""W22 T0 -- controls: independent evaluators, inter-probe agreement with W17
and W5, Lemma W22-M / W22-H identities, and mutation controls.

Exact arithmetic only.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, product

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-scalar-slice-w17-2026-08-15")
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-slice-dirtiness-w5-2026-08-15")
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-induction2-w22-2026-08-15")

import w17_core                                   # noqa: E402
import slice_core                                 # noqa: E402
import w22_core as W                              # noqa: E402

RES = {"controls": [], "failures": []}


def rec(name, ok, detail=""):
    RES["controls"].append({"name": name, "ok": bool(ok), "detail": detail})
    if not ok:
        RES["failures"].append({"name": name, "detail": detail})
    print(f"[{'OK ' if ok else 'FAIL'}] {name} {detail}")


def rand_source(rng, n, lo=-4, hi=4, zero_prob=0.0):
    src = {}
    for a, b in combinations(range(n), 2):
        src[(a, b)] = [[0 if rng.random() < zero_prob else rng.randint(lo, hi)
                        for _ in range(3)] for _ in range(3)]
    return src


def rand_K(rng, lo=-3, hi=3):
    return [[rng.randint(lo, hi) for _ in range(3)] for _ in range(3)]


def main():
    rng = random.Random(220815)

    # ---- C1: my two evaluators agree (general caps), N = 6 and N = 8
    for n in (6, 8):
        agree = 0
        for _ in range(12 if n == 6 else 4):
            src = rand_source(rng, n, zero_prob=0.25)
            p, q = 0, 1
            sites = tuple(x for x in range(n) if x not in (p, q))
            K = rand_K(rng)
            e1 = W.cap_error_direct(src, p, q, K, sites)
            e2 = W.cap_error_hafnian(src, p, q, K, sites, n)
            if e1 != e2:
                rec(f"C1 evaluators agree N={n}", False, "mismatch")
                return
            agree += 1
        rec(f"C1 W22-M == W22-H (general cap) N={n}", True, f"{agree} instances")

    # ---- C2: inter-probe -- rank-one specialisation == W17's evaluator
    for n in (6, 8):
        agree = 0
        for _ in range(10 if n == 6 else 3):
            src = rand_source(rng, n, zero_prob=0.2)
            p, q = 0, 1
            sites = tuple(x for x in range(n) if x not in (p, q))
            u = [rng.randint(-3, 3) for _ in range(3)]
            v = [rng.randint(-3, 3) for _ in range(3)]
            mine = W.cap_error_direct(src, p, q, W.outer_K(u, v), sites)
            theirs = w17_core.rank_one_error(src, p, q, u, v, sites)
            theirs = {k: val for k, val in theirs.items() if val != 0}
            if mine != theirs:
                rec(f"C2 vs W17 N={n}", False, "mismatch")
                return
            agree += 1
        rec(f"C2 rank-one == W17 rank_one_error N={n}", True,
            f"{agree} instances")

    # ---- C3: inter-probe -- monochrome component == W5's scalar slice error
    # (Lemma W17.10: W5's E is the c^U component of E_pq(E_cc))
    agree = 0
    for n in (6, 8):
        for _ in range(8 if n == 6 else 3):
            src = rand_source(rng, n, zero_prob=0.2)
            p, q = 0, 1
            sites = tuple(x for x in range(n) if x not in (p, q))
            for c in (0, 1, 2):
                K = [[0] * 3 for _ in range(3)]
                K[c][c] = 1
                mine = W.cap_error_direct(src, p, q, K, sites)
                w = {W.ekey(a, b): src[(a, b)][c][c]
                     for a, b in combinations(range(n), 2)}
                theirs = slice_core.slice_error(w, p, q, sites, check=True)
                mv = mine.get((c,) * len(sites), 0)
                if mv != theirs:
                    rec("C3 vs W5 scalar slice", False,
                        f"n={n} c={c} {mv} != {theirs}")
                    return
                agree += 1
    rec("C3 monochrome component == W5 slice error", True, f"{agree} instances")

    # ---- C4: h=2 structure predicate (W17.1) reproduced independently and
    #          agreeing with the vanishing of the full tensor error
    ok = 0
    for _ in range(400):
        src = rand_source(rng, 6, lo=-3, hi=3, zero_prob=rng.choice([0.0, .3, .5, .7]))
        p, q = rng.sample(range(6), 2)
        sites = tuple(x for x in range(6) if x not in (p, q))
        u = [rng.randint(-2, 2) for _ in range(3)]
        v = [rng.randint(-2, 2) for _ in range(3)]
        pred, _ = W.h2_predicate(src, p, q, u, v, sites)
        mine = W.cap_error_direct(src, p, q, W.outer_K(u, v), sites)
        theirs, _ = w17_core.h2_structure_predicate(src, p, q, u, v, sites)
        if pred != (len(mine) == 0) or pred != theirs:
            rec("C4 h2 predicate", False, f"{pred} {len(mine)} {theirs}")
            return
        ok += 1
    rec("C4 W17.1 predicate == tensor vanishing (indep. reimpl.)", True,
        f"{ok}/400")

    # ---- C5: Lemma W22-M support criterion is SUFFICIENT for cleanliness
    tested = clean_by_support = 0
    for _ in range(600):
        n = rng.choice([6, 8])
        src = rand_source(rng, n, lo=-3, hi=3, zero_prob=rng.choice([.5, .7, .85]))
        p, q = rng.sample(range(n), 2)
        sites = tuple(x for x in range(n) if x not in (p, q))
        K = rand_K(rng, -2, 2)
        sup = W.support_clean(src, p, q, K, sites)
        err = W.cap_error_direct(src, p, q, K, sites)
        tested += 1
        if sup:
            clean_by_support += 1
            if err:
                rec("C5 support criterion", False, "support-clean but E != 0")
                return
    rec("C5 Lemma W22-M: support-clean => E = 0", True,
        f"{clean_by_support}/{tested} support-clean, 0 violations")

    # ---- C6: MUTATION controls -- each must FAIL
    mut = []
    src = rand_source(rng, 6, zero_prob=0.1)
    p, q = 0, 1
    sites = (2, 3, 4, 5)
    K = rand_K(rng)
    base = W.cap_error_direct(src, p, q, K, sites)

    # M1: drop the s^{h-k} weight  (h=2: only k=2 term, so mutate at N=8)
    src8 = rand_source(rng, 8, zero_prob=0.1)
    s8 = (2, 3, 4, 5, 6, 7)
    K8 = rand_K(rng)
    good8 = W.cap_error_direct(src8, 0, 1, K8, s8)

    def mutated_direct(source, p, q, K, sites, mode):
        sites = tuple(sorted(sites))
        h = len(sites) // 2
        s = W.cap_s(source, p, q, K)
        R = W.cap_R(source, p, q, K, sites)
        A = {(a, b): W.oriented(source, a, b) for a, b in combinations(sites, 2)}
        slot = {a: i for i, a in enumerate(sites)}
        out = {}
        for word in product(range(3), repeat=len(sites)):
            total = 0
            for M in W.perfect_matchings(sites):
                lo = 1 if mode == "kmin1" else 2
                for size in range(lo, h + 1):
                    pref = 1 if mode == "nos" else s ** (h - size)
                    for J in combinations(range(h), size):
                        Js = set(J)
                        term = pref
                        for i, (a, b) in enumerate(M):
                            ca, cb = word[slot[a]], word[slot[b]]
                            tab = R if i in Js else A
                            if mode == "swap":
                                tab = A if i in Js else R
                            term *= W._entry(tab, a, b, ca, cb)
                            if term == 0:
                                break
                        total += term
            if total != 0:
                out[word] = total
        return out

    for mode, tag in (("nos", "M1 drop s^{h-k}"), ("kmin1", "M2 allow |J|=1"),
                      ("swap", "M3 swap R/A roles")):
        m = mutated_direct(src8, 0, 1, K8, s8, mode)
        rec(f"C6 mutation {tag} changes E (N=8)", m != good8,
            "differs" if m != good8 else "IDENTICAL")

    # M4: wrong R (drop the second term of R_ab)
    def R_half(source, p, q, K, sites, ncol=3):
        Rh = {}
        for a, b in combinations(sorted(sites), 2):
            apa = W.oriented(source, p, a)
            aqb = W.oriented(source, q, b)
            Rh[(a, b)] = [[sum(K[i][j] * apa[i][ca] * aqb[j][cb]
                               for i in range(3) for j in range(3))
                           for cb in range(3)] for ca in range(3)]
        return Rh
    saved = W.cap_R
    W.cap_R = R_half
    try:
        m = W.cap_error_direct(src, p, q, K, sites)
    finally:
        W.cap_R = saved
    rec("C6 mutation M4 half-R changes E (N=6)", m != base,
        "differs" if m != base else "IDENTICAL")

    # M5: transpose the cap
    Kt = [[K[j][i] for j in range(3)] for i in range(3)]
    m = W.cap_error_direct(src, p, q, Kt, sites)
    rec("C6 mutation M5 transposed cap changes E", m != base,
        "differs" if m != base else "IDENTICAL")

    # ---- C7: the descent identity.  E = 0 and s,kappa != 0  =>  the capped
    # source y = A + R/s has H_U(y) = (1/s) sum_c kappa_c X_c^U.
    checked = 0
    for _ in range(4000):
        src = rand_source(rng, 6, lo=-2, hi=2, zero_prob=0.75)
        p, q = rng.sample(range(6), 2)
        sites = tuple(x for x in range(6) if x not in (p, q))
        K = rand_K(rng, -2, 2)
        if not W.is_admissible(src, p, q, K):
            continue
        if W.cap_error_direct(src, p, q, K, sites):
            continue
        s = Fraction(W.cap_s(src, p, q, K))
        R = W.cap_R(src, p, q, K, sites)
        y = {}
        for a, b in combinations(sites, 2):
            blk = W.oriented(src, a, b)
            y[(a, b)] = [[Fraction(blk[i][j]) + Fraction(R[(a, b)][i][j]) / s
                          for j in range(3)] for i in range(3)]
        bad = 0
        for word in product(range(3), repeat=4):
            wo = {a: word[i] for i, a in enumerate(sites)}
            val = W._haf_tensor(y, sites, wo)
            cap = Fraction(0)
            for i in range(3):
                for j in range(3):
                    if K[i][j] == 0:
                        continue
                    full = [0] * 6
                    for a in sites:
                        full[a] = wo[a]
                    full[p], full[q] = i, j
                    cap += K[i][j] * W.ghz_coefficient(src, tuple(full), 6)
            if val != cap / s:
                bad += 1
        if bad:
            rec("C7 descent identity", False, f"{bad} bad words")
            return
        checked += 1
        if checked >= 40:
            break
    rec("C7 E=0 => s*Haf_U(y) = K contraction of H_B(A)", checked > 0,
        f"{checked} witnesses verified")

    RES["summary"] = {"n_controls": len(RES["controls"]),
                      "n_failures": len(RES["failures"])}
    with open("/Users/rishi/workplace/krenn-conjecture/computations/"
              "unaudited-induction2-w22-2026-08-15/results_t0_controls.json",
              "w") as fh:
        json.dump(RES, fh, indent=1)
    print("\nfailures:", len(RES["failures"]))


if __name__ == "__main__":
    main()

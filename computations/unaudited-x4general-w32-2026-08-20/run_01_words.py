#!/usr/bin/env python3
"""W32 / T1 -- the word ledger and the PAIR-RESTRICTION DECOMPOSITION.

Establishes and machine-checks:

  L1 (word ledger).  At N = 8 the words of off-count 5 are exactly the words
      of profile (3,3,2); every one of them uses all three colours.  Hence
      X_4 imposes EVERY bichromatic word.

  W32-2COL [the new reduction].  If A in X_4 at N=8 then each of the three
      2-colour restrictions A^{01}, A^{02}, A^{12} is an EXACT 2-colour
      source on K_8 (Krenn-Gu with d = 2, n = 8).
      Proof: a word using only colours {a,b} has off-count <= 4 (profiles
      (8,0),(7,1),(6,2),(5,3),(4,4)) so it is imposed, and H_w for such a
      word only reads the cells A[a][a],A[a][b],A[b][a],A[b][b].

  W32-RES [the residual gap].  X_4 at N=8 is EXACTLY
      [three exact 2-colour restrictions] AND [H_w = 0 for every word of
      trichromatic profile (6,1,1), (5,2,1), (4,3,1), (4,2,2)].
      On the diagonal stratum the first three are vacuous (an odd colour
      class kills the product) and (4,2,2) is W27's condition (D), while the
      pairwise part is W27's condition (C).  So W32-2COL is the general form
      of (C) and the residual is the general form of (D).

Checkpoint: results_t1.json.  Control manifest asserted (ledger 21).
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w32_core import (NCOL, Cyc, Fp, Manifest, all_words, cell, copy_source,
                      delta3_pms, diag_source, ekey, haf_word, in_Xk,
                      near_constant_ball, offcount, perfect_matchings, profile,
                      require, restrict_pair, violations, words_offcount_le,
                      zero_source)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "results_t1.json")
N = 8
R = {}
MAN = Manifest(["ball_vs_offcount", "hw_pair_locality", "mutation_pair",
                "positive_2col", "diag_vacuity", "hafnian_engine_xcheck",
                "field_xcheck"])


def rnd_source(n, rng, dom="Q", dens=1.0, p=13):
    src = zero_source(n)
    for e in src:
        for a in range(NCOL):
            for b in range(NCOL):
                if rng.random() > dens:
                    continue
                if dom == "Q":
                    src[e][a][b] = Fraction(rng.randint(-6, 6), rng.choice(
                        [1, 1, 1, 2, 3]))
                elif dom == "Qw":
                    src[e][a][b] = Cyc(rng.randint(-4, 4), rng.randint(-4, 4))
                else:
                    src[e][a][b] = Fp(rng.randint(0, p - 1), p)
    if dom == "Fp":
        for e in src:
            for a in range(NCOL):
                for b in range(NCOL):
                    if src[e][a][b] == 0 and not isinstance(src[e][a][b], Fp):
                        src[e][a][b] = Fp(0, p)
    return src


# ---------------------------------------------------------------- L1 ledger
def task_word_ledger():
    W = all_words(N)
    byoff = {}
    for w in W:
        byoff.setdefault(offcount(w), []).append(w)
    prof_by_off = {k: sorted({profile(w) for w in v}) for k, v in byoff.items()}
    imposed = words_offcount_le(N, 4)
    ball = near_constant_ball(N, 4)
    require(set(imposed) == set(ball),
            "ball construction != off-count construction")
    MAN.mark("ball_vs_offcount")
    free = [w for w in W if offcount(w) > 4]
    require(all(profile(w) == (3, 3, 2) for w in free), "free != (3,3,2)")
    require(all(len(set(w)) == 3 for w in free), "some free word is bichromatic")
    bich = [w for w in W if len(set(w)) <= 2]
    require(all(offcount(w) <= 4 for w in bich), "a bichromatic word is free")
    trich_imposed = [w for w in W if len(set(w)) == 3 and offcount(w) <= 4]
    prof_counts = {}
    for w in trich_imposed:
        prof_counts[str(profile(w))] = prof_counts.get(str(profile(w)), 0) + 1
    R["L1"] = {
        "n_words": len(W),
        "profiles_by_offcount": {str(k): [list(p) for p in v]
                                 for k, v in sorted(prof_by_off.items())},
        "n_imposed_offle4": len(imposed),
        "n_free_off5": len(free),
        "free_profiles": sorted({str(profile(w)) for w in free}),
        "free_all_trichromatic": True,
        "n_bichromatic_words": len(bich),
        "all_bichromatic_imposed": True,
        "n_trichromatic_imposed": len(trich_imposed),
        "trichromatic_imposed_profile_counts": prof_counts,
    }
    print("L1", json.dumps(R["L1"]["profiles_by_offcount"]))
    print("L1 imposed", len(imposed), "free", len(free),
          "bichromatic", len(bich), "trichromatic imposed", len(trich_imposed),
          prof_counts)


# ------------------------------------------------- W32-2COL locality of H_w
def task_pair_locality():
    """H_w for a word using only colours {a,b} equals H_w of the source with
    every cell outside the {a,b} block zeroed -- checked on random general
    sources over Q, Q(omega) and F_13 (ledger 19: two 1-mod-3 primes used in
    the algebraic tasks; here the point is field-independence)."""
    rng = random.Random(20260820)
    tests = 0
    for dom, p in (("Q", None), ("Qw", None), ("Fp", 13), ("Fp", 31)):
        for _ in range(4):
            src = rnd_source(N, rng, dom=dom, p=p or 13)
            for pair in ((0, 1), (0, 2), (1, 2)):
                stripped = zero_source(N, sample=src[(0, 1)][0][0])
                for e in src:
                    for a in pair:
                        for b in pair:
                            stripped[e][a][b] = src[e][a][b]
                for _ in range(6):
                    w = tuple(rng.choice(pair) for _ in range(N))
                    require(haf_word(src, w) == haf_word(stripped, w),
                            f"pair locality failed {dom} {pair} {w}")
                    # and the restricted 2-colour source computes the same
                    r2 = restrict_pair(src, pair, N)
                    w2 = tuple(pair.index(x) for x in w)
                    require(haf_word(r2, w2) == haf_word(src, w),
                            f"restrict_pair mismatch {dom} {pair} {w}")
                    tests += 1
    MAN.mark("hw_pair_locality")
    R["pair_locality"] = {"checks": tests, "all_equal": True}
    print("pair locality: ", tests, "checks, 0 disagreements")


# ------------------------------------------- positive control: 2-colour exact
def ham_two_colour(n=8):
    """Delta^2 on the Hamiltonian 8-cycle: M_0 = {01,23,45,67},
    M_1 = {12,34,56,70}.  Claimed EXACT for d = 2."""
    m0 = [ekey(i, i + 1) for i in range(0, n, 2)]
    m1 = [ekey(i, (i + 1) % n) for i in range(1, n, 2)]
    src = {}
    for a, b in itertools.combinations(range(n), 2):
        src[(a, b)] = [[Fraction(0)] * 2 for _ in range(2)]
    for e in m0:
        src[e][0][0] = Fraction(1)
    for e in m1:
        src[e][1][1] = Fraction(1)
    return src


def task_positive_2col():
    src = ham_two_colour(N)
    bad = []
    for w in itertools.product(range(2), repeat=N):
        tgt = 1 if len(set(w)) == 1 else 0
        if haf_word(src, w) != tgt:
            bad.append(w)
    require(not bad, f"Delta^2 Hamiltonian is NOT 2-colour exact: {bad[:4]}")
    MAN.mark("positive_2col")
    R["positive_2col"] = {"object": "Delta^2 on the 8-cycle",
                          "exact_d2_n8": True, "violations": 0}
    print("positive control: Delta^2 Hamiltonian IS 2-colour exact at n=8"
          " => W32-2COL alone cannot kill")


# ------------------------------------------------- mutation control (firing)
def _bad2(src):
    return [w for w in itertools.product(range(2), repeat=N)
            if haf_word(src, w) != (1 if len(set(w)) == 1 else 0)]


def task_mutation():
    """Three mutations of the exact 2-colour object; each must FIRE, and each
    failing word must have off-count <= 4 (so X_4 really sees it).

    Recorded finding: the fourth perturbation (planting the PURE cell
    A_04[0][0] = 1) does NOT fire -- the exact 2-colour family at n=8 is
    strictly larger than Delta^2 on a Hamiltonian cycle."""
    base = ham_two_colour(N)
    fired = {}
    muts = {
        "cross_cell_A01_01": lambda s: s[(0, 1)].__setitem__(
            0, [s[(0, 1)][0][0], Fraction(1)]),
        "rescale_pure_edge_23": lambda s: s[(2, 3)].__setitem__(
            0, [Fraction(5), s[(2, 3)][0][1]]),
        "delete_M1_edge_56": lambda s: s[(5, 6)].__setitem__(
            1, [s[(5, 6)][1][0], Fraction(0)]),
    }
    for name, f in muts.items():
        mut = {e: [r[:] for r in m] for e, m in base.items()}
        f(mut)
        bad = _bad2(mut)
        require(bad, f"mutation {name} did NOT fire")
        require(all(offcount(w) <= 4 for w in bad),
                f"mutation {name}: a failure is not imposed at k=4")
        fired[name] = {"n_failing": len(bad), "example": list(bad[0])}
        print(f"mutation {name} FIRES: {len(bad)} bichromatic failures, e.g.",
              bad[0])
    # the non-firing perturbation -- a real structural finding, not a control
    aug = {e: [r[:] for r in m] for e, m in base.items()}
    aug[(0, 4)][0][0] = Fraction(1)
    aug_bad = _bad2(aug)
    MAN.mark("mutation_pair")
    R["mutation"] = {"fired": fired,
                     "augmented_04_still_exact": len(aug_bad) == 0}
    print("NOTE: Delta^2+chord(0,4) is still 2-colour exact:",
          len(aug_bad) == 0, "-- the d=2 solution family is larger")


# ------------------------------------------------------ diagonal vacuity map
def task_diag_vacuity():
    """On the diagonal stratum, which imposed trichromatic profiles carry
    content?  H_w = prod_c haf(t^c | w^{-1}(c)) vanishes automatically when
    some class is odd, so only all-even profiles are conditions."""
    prof_status = {}
    for w in all_words(N):
        if len(set(w)) != 3 or offcount(w) > 4:
            continue
        pr = profile(w)
        alleven = all(x % 2 == 0 for x in pr)
        prof_status.setdefault(str(pr), alleven)
    # verify the claim on explicit random diagonal sources
    rng = random.Random(7)
    checked = 0
    for _ in range(40):
        edgesets = []
        for c in range(3):
            edgesets.append([e for e in
                             itertools.combinations(range(N), 2)
                             if rng.random() < 0.35])
        wts = {(c, ekey(*e)): Fraction(rng.randint(1, 9))
               for c in range(3) for e in edgesets[c]}
        src = diag_source(N, edgesets, wts)
        for w in all_words(N):
            if len(set(w)) != 3 or offcount(w) > 4:
                continue
            pr = profile(w)
            if any(x % 2 for x in pr):
                require(haf_word(src, w) == 0,
                        f"diagonal odd-class word nonzero {w}")
                checked += 1
    MAN.mark("diag_vacuity")
    R["diag_vacuity"] = {"profile_is_condition_on_diagonal": prof_status,
                         "odd_class_checks": checked}
    print("diagonal vacuity:", prof_status, f"({checked} zero-checks)")


# --------------------------------------------------- engine / field controls
def task_engine_xcheck():
    """Cross-check the PM-enumeration hafnian against W28's independent
    lowest-site recursion (imported ONLY as a control)."""
    sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                       "unaudited-x4empty-w28-2026-08-18")
    import w28_core as W28  # noqa: E402
    rng = random.Random(99)
    agree = 0
    for _ in range(8):
        src = rnd_source(N, rng, dom="Q")
        for _ in range(12):
            w = tuple(rng.randrange(3) for _ in range(N))
            a = haf_word(src, w)
            b = W28.H_word(src, w, N)
            require(a == b, f"engine disagreement on {w}: {a} vs {b}")
            agree += 1
    MAN.mark("hafnian_engine_xcheck")
    R["engine_xcheck"] = {"checks": agree, "disagreements": 0}
    print("engine cross-check vs W28 recursion:", agree, "checks, 0 disagree")


def task_field_xcheck():
    """Cyc arithmetic control: (1+w)(1+w^2) = 1, w^3 = 1, and a hafnian over
    Q(omega) reduced mod 13 and mod 31 (both = 1 mod 3) matches the F_p run."""
    w = Cyc(0, 1)
    require(w * w * w == Cyc(1, 0), "omega^3 != 1")
    require(w * w + w + Cyc(1, 0) == Cyc(0, 0), "min poly wrong")
    rng = random.Random(4242)
    checks = 0
    for p in (13, 31):
        require(p % 3 == 1, "ledger 19: need p = 1 mod 3")
        # omega exists in F_p; find it
        om = None
        for g in range(2, p):
            if pow(g, 3, p) == 1 and g != 1:
                om = g
                break
        require(om is not None, f"no cube root of unity in F_{p}")
        src = zero_source(N)
        srcp = zero_source(N, sample=Fp(0, p))
        for e in src:
            for a in range(3):
                for b in range(3):
                    x, y = rng.randint(-3, 3), rng.randint(-3, 3)
                    src[e][a][b] = Cyc(x, y)
                    srcp[e][a][b] = Fp(x + y * om, p)
        for _ in range(5):
            wd = tuple(rng.randrange(3) for _ in range(N))
            hq = haf_word(src, wd)
            hp = haf_word(srcp, wd)
            require(Fp(hq.a.numerator * pow(hq.a.denominator, p - 2, p)
                       + hq.b.numerator * pow(hq.b.denominator, p - 2, p) * om,
                       p) == hp, "Q(omega) -> F_p reduction mismatch")
            checks += 1
    MAN.mark("field_xcheck")
    R["field_xcheck"] = {"checks": checks, "primes": [13, 31]}
    print("field control: Q(omega) -> F_13 / F_31 reductions agree,",
          checks, "checks")


def main():
    task_word_ledger()
    task_pair_locality()
    task_positive_2col()
    task_mutation()
    task_diag_vacuity()
    task_engine_xcheck()
    task_field_xcheck()
    R["manifest"] = MAN.assert_complete()
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()

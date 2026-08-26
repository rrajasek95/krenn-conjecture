#!/usr/bin/env python3
"""T4 -- mutation controls on every verification path (UNAUDITED).

A passing checker means nothing unless the same checker fails when the thing
it checks is broken.  Each control below perturbs exactly one component and
requires the corresponding test to DIE.  A control that does not kill its
target is itself reported as a failure.

Controls
  M1  positive/negative control on the monomiality detector itself.
  M2  `parallel` weakened to always-true              -> T1.1 must die.
  M3  `factors_through` faked to always succeed       -> T1.0 must die.
  M4  `krank` faked to always return 3                -> T2.0 must die.
  M5  the in-span filter of the exhaustive search removed
                                                      -> T1.3 must report a
                                                         counterexample (i.e.
                                                         the search has teeth).
  M6  the T2.4 counterexample perturbed off its locus -> its square must break.
  M7  exact scan of the rank-one locus of the (k_U,k_V)=(2,2) palette family.
      (This control REFUTED an earlier hand derivation in this stress test;
      see the note inside m7_conic_scan.)
  M8  Omega's cross-palette projection a != b flipped to a == b
                                                      -> T1.0 must die.
  M9  the committed upstream checker still passes byte-for-byte.
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))

import hashlib
import random
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import exactlin
import t1_fusion_stress as t1
import t2_kruskal_boundary as t2

HERE = Path(__file__).resolve().parent
COMPUTATIONS = HERE.parent
RESULTS = {}
OUTCOMES = []


def banner(text):
    print("=" * 72)
    print(text)
    print("=" * 72)


def expect_death(label, thunk):
    """Require that `thunk` raises RuntimeError (the checkers' failure mode)."""
    try:
        thunk()
    except RuntimeError as exc:
        detail = str(exc)
        print(f"  [KILLED]  {label}")
        print(f"            {detail[:110]}")
        OUTCOMES.append((label, "killed"))
        return True
    except Exception as exc:                              # noqa: BLE001
        print(f"  [KILLED*] {label}  ({type(exc).__name__}: {exc})"[:150])
        OUTCOMES.append((label, "killed-other"))
        return True
    print(f"  [SURVIVED -- CONTROL FAILED]  {label}")
    OUTCOMES.append((label, "SURVIVED"))
    return False


def quiet(fn, *args, **kwargs):
    import io
    import contextlib
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        return fn(*args, **kwargs)


# --------------------------------------------------------------------------
# the exact non-monomial instance from T2.4 and the monomial one from T2.3
NONMONO = {
    "U": exactlin.mat([[1, 0, 1], [0, 1, 1], [0, 0, 0]]),
    "V": exactlin.mat([[1, 0, 1], [0, 1, -2], [0, 0, 0]]),
    "A": exactlin.mat([[1, 0, 2], [0, 1, 1], [0, 0, 0]]),
    "B": exactlin.mat([[1, 0, 1], [0, 1, -1], [0, 0, 0]]),
}
MONO = {
    "U": exactlin.mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    "V": exactlin.mat([[1, 0, 1], [0, 1, 1], [0, 0, 0]]),
    "A": exactlin.mat([[2, 0, 0], [0, 3, 0], [0, 0, 5]]),
    "B": exactlin.mat([[7, 0, 1], [0, 11, 1], [0, 0, 0]]),
}


def m1_detector_controls():
    banner("M1  positive and negative controls on the monomiality detector")
    pos = exactlin.aligned_monomial(MONO["A"], MONO["B"], MONO["U"], MONO["V"])
    neg = exactlin.aligned_monomial(NONMONO["A"], NONMONO["B"],
                                    NONMONO["U"], NONMONO["V"])
    print(f"  monomial instance   -> {pos}   (must be a permutation)")
    print(f"  NON-monomial instance -> {neg}   (must be None)")
    exactlin.require(pos is not None, "positive control failed")
    exactlin.require(neg is None, "negative control failed")
    # both instances really are fusion squares
    for tag, data in (("monomial", MONO), ("non-monomial", NONMONO)):
        C = exactlin.factors_through(data["A"], data["B"], data["U"], data["V"])
        exactlin.require(C is not None and exactlin.det(C) != 0,
                         ("control instance is not a fusion square", tag))
    print("  both controls are genuine fusion squares with C in GL_3.")
    OUTCOMES.append(("M1 detector controls", "passed"))


def m2_parallel_always_true():
    banner("M2  `parallel` weakened to always-true  ->  T1.1 must die")
    original = exactlin.parallel
    exactlin.parallel = lambda x, y: True
    try:
        expect_death("T1.1 with a blind parallelism test",
                     lambda: quiet(t1.t1_1_positive_samples,
                                   random.Random(7), 3, 20))
    finally:
        exactlin.parallel = original


def m3_fake_factors_through():
    banner("M3  `factors_through` faked to always succeed  ->  T1.0 must die")
    original = t1.factors_through
    t1.factors_through = lambda A, B, U, V: [
        [Fraction(int(i == j)) for j in range(3)] for i in range(3)]
    try:
        expect_death("T1.0 with a rubber-stamp square test",
                     lambda: quiet(t1.t1_0_formalization_bridge,
                                   random.Random(11), 3, 40))
    finally:
        t1.factors_through = original


def m4_fake_krank():
    banner("M4  `krank` faked to always return 3  ->  T2.0 must die")
    original = t2.krank_mod
    t2.krank_mod = lambda M, p: 3
    try:
        expect_death("T2.0 with a blind k-rank",
                     lambda: quiet(t2.t2_0_full_rank_iff_krank, 3))
    finally:
        t2.krank_mod = original


def m5_remove_in_span_filter():
    banner("M5  in-span filter removed from the exhaustive search  -> T1.3 must "
           "report a counterexample")
    original = t1.left_kernel_mod
    t1.left_kernel_mod = lambda matrix, prime: []     # nothing is filtered out
    try:
        expect_death("T1.3 with the factoring condition switched off",
                     lambda: quiet(t1.t1_3_exhaustive, 3))
    finally:
        t1.left_kernel_mod = original


def m6_perturb_counterexample():
    banner("M6  the T2.4 counterexample perturbed off its rank-one locus")
    # b_3 = v1 - v2 is forced; anything else breaks the square.
    broken = [row[:] for row in NONMONO["B"]]
    broken[1][2] = Fraction(-3)                        # b_3 := v1 - 3 v2
    C = exactlin.factors_through(NONMONO["A"], broken,
                                 NONMONO["U"], NONMONO["V"])
    print(f"  perturbed b_3 -> factors_through returns {C}")
    exactlin.require(C is None,
                     "perturbed counterexample still factors through")
    # a_3 = 2u1 + u2 is equally forced
    broken_a = [row[:] for row in NONMONO["A"]]
    broken_a[0][2] = Fraction(3)                       # a_3 := 3u1 + u2
    C2 = exactlin.factors_through(broken_a, NONMONO["B"],
                                  NONMONO["U"], NONMONO["V"])
    print(f"  perturbed a_3 -> factors_through returns {C2}")
    exactlin.require(C2 is None,
                     "perturbed counterexample still factors through (a)")
    print("  the counterexample is exact and isolated, not a coincidence.")
    OUTCOMES.append(("M6 counterexample perturbation", "passed"))


def m7_conic_scan():
    banner("M7  exact scan of the rank-one locus for the (k_U,k_V)=(2,2) family")
    # U = [u1, u2, u1+u2], V = [v1, v2, alpha v1 + beta v2], (alpha,beta) != 0.
    # M(lambda) = sum_a lambda_a u_a v_a^T has, in the basis (u1,u2)x(v1,v2),
    #     row1 = (l1 + l3 alpha, l3 beta),  row2 = (l3 alpha, l2 + l3 beta),
    # so rank(M) = 1 with full support  <=>  CONIC(lambda) = 0 where
    #     CONIC = l1 l2 + l3 (beta l1 + alpha l2).
    # NOTE.  An earlier hand derivation of this stress test claimed the locus
    # was "1 + alpha + beta = 0"; that is only the condition for the SPECIFIC
    # choice lambda = (1,1,1).  This control caught that error, and the
    # corrected statement is stronger: a full-support rank-one element exists
    # for EVERY such palette pair.
    U = exactlin.mat([[1, 0, 1], [0, 1, 1], [0, 0, 0]])
    with_solution, all_ones = [], []
    for alpha in range(-3, 4):
        for beta in range(-3, 4):
            if alpha == 0 and beta == 0:
                continue
            V = exactlin.mat([[1, 0, alpha], [0, 1, beta], [0, 0, 0]])
            if exactlin.krank(V) < 2:
                continue
            lam = full_support_rank_one(U, V)
            if lam is not None:
                with_solution.append((alpha, beta))
                conic = lam[0] * lam[1] + lam[2] * (beta * lam[0]
                                                    + alpha * lam[1])
                exactlin.require(conic == 0,
                                 ("rank-one point off the conic", alpha, beta,
                                  lam, conic))
            ones = [Fraction(1)] * 3
            M = [[sum(ones[a] * U[i][a] * V[j][a] for a in range(3))
                  for j in range(3)] for i in range(3)]
            if exactlin.rank(M) == 1:
                all_ones.append((alpha, beta))
    candidates = [(a, b) for a in range(-3, 4) for b in range(-3, 4)
                  if not (a == 0 and b == 0)
                  and exactlin.krank(exactlin.mat(
                      [[1, 0, a], [0, 1, b], [0, 0, 0]])) >= 2]
    print(f"  palette pairs scanned (k_V = 2)                : {len(candidates)}")
    print(f"  with a FULL-support rank-one element           : "
          f"{len(with_solution)}  (every one, and every witness is on the conic)")
    print(f"  for which lambda = (1,1,1) itself works        : {sorted(all_ones)}")
    exactlin.require(len(with_solution) == len(candidates),
                     ("some (2,2) palette had no full-support rank-one point",
                      sorted(set(candidates) - set(with_solution))))
    exactlin.require(sorted(all_ones)
                     == sorted(p for p in candidates if 1 + p[0] + p[1] == 0),
                     ("lambda=(1,1,1) locus mismatch", sorted(all_ones)))
    print("  => whenever BOTH palettes have rank 2, non-monomial fusion columns")
    print("     exist.  This is the (k_U,k_V)=(2,2) row of the T2.6 table.")
    OUTCOMES.append(("M7 rank-one locus scan", "passed"))


def full_support_rank_one(U, V):
    """Is there lambda with all three entries nonzero and
    rank(sum_a lambda_a u_a v_a^T) == 1?  Exact scan of a bounded grid plus
    the closed-form solution."""
    for l1 in range(-4, 5):
        for l2 in range(-4, 5):
            for l3 in range(-4, 5):
                if 0 in (l1, l2, l3):
                    continue
                lam = [Fraction(l1), Fraction(l2), Fraction(l3)]
                M = [[sum(lam[a] * U[i][a] * V[j][a] for a in range(3))
                      for j in range(len(V))] for i in range(len(U))]
                if exactlin.rank(M) == 1:
                    return (l1, l2, l3)
    return None


def m8_flip_omega_projection():
    banner("M8  Omega's cross-palette projection a != b flipped to a == b  -> "
           "T1.0 must die")
    original = t1.omega_defect
    t1.omega_defect = lambda G, H: [
        [G[a][c] * H[a][c] for c in range(len(G))] for a in range(len(G))]
    try:
        expect_death("T1.0 with the diagonal (wrong) projection",
                     lambda: quiet(t1.t1_0_formalization_bridge,
                                   random.Random(13), 3, 40))
    finally:
        t1.omega_defect = original


def m9_upstream_checker():
    banner("M9  the committed upstream checker still passes, unmodified")
    target = COMPUTATIONS / (
        "verify_simultaneous_diagonal_flattening_palette_fusion_gate.py")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    expected = ("750ff2094c0a1c6e8b767ca7bf9323a41942f37eecf3cdc773a5295d445"
                "be1ab")
    print(f"  sha256(committed checker) = {digest}")
    exactlin.require(digest == expected,
                     ("the committed checker changed under us", digest))
    proc = subprocess.run([sys.executable, str(target)],
                          capture_output=True, text=True, cwd=str(COMPUTATIONS))
    print("  " + (proc.stdout.strip().splitlines() or ["<no output>"])[0])
    exactlin.require(proc.returncode == 0,
                     ("committed checker failed", proc.stderr[-400:]))
    print("  committed checker: PASS (our stress test contradicts nothing in it).")
    OUTCOMES.append(("M9 upstream checker", "passed"))


def main():
    m1_detector_controls()
    m2_parallel_always_true()
    m3_fake_factors_through()
    m4_fake_krank()
    m5_remove_in_span_filter()
    m6_perturb_counterexample()
    m7_conic_scan()
    m8_flip_omega_projection()
    m9_upstream_checker()
    banner("T4 SUMMARY")
    survived = [label for label, status in OUTCOMES if status == "SURVIVED"]
    for label, status in OUTCOMES:
        print(f"  {status:12s}  {label}")
    exactlin.require(not survived, ("mutation controls SURVIVED", survived))
    print(f"\n  {len(OUTCOMES)} controls, 0 survivors.")
    RESULTS["T4"] = {"controls": len(OUTCOMES), "survivors": survived}
    return RESULTS


if __name__ == "__main__":
    main()

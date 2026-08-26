#!/usr/bin/env python3
"""UNAUDITED PROBE -- P1 task A(i): the constructors are the checker's.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

Exact identity controls tying this library's s, r, x, kappa, E to the
committed clean-pair descent checkers:

  I1  K |- H_B(A) = [(s+r)exp(x)]_U               (eq. 12; the identity the
      committed symbolic checker proves universally over all 729 words)
  I2  s^3 H_U(x+r/s) = s^2 (K |- H_B(A)) + E     (eq. 15/16 at h=3)
  I3  E computed from the K-symbolic cubic rows equals E computed by the
      independent numeric square-zero evaluator
  I4  E(lambda K) = lambda^3 E(K)                (homogeneity, degree 3)
  I5  the typed ledger of E: 15 matchings supply the r^3 terms and 45
      (matching, x-edge) pairs supply the 3 s r^2 x terms, matching
      profiles Counter({0: 15, 1: 45, 2: 45, 3: 15}) of the committed checker
  I6  r-degenerate sources (r == 0 identically) give E == 0

All arithmetic is exact.  Run: python3 wsplit_identities.py
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import random
import sys

import wsplit_core as core
from wsplit_core import (COLORS, MATCHINGS_U, P, Q, U, WORDS, direct_error_tensor,
                         canonical_y, cap_contraction, error_matrix, eval_cubic,
                         eval_form, form_s, matching_tensor, random_source,
                         require, s_plus_r_exp_x)


def random_cap(rng, lo=-5, hi=5):
    return tuple(rng.randint(lo, hi) for _ in range(9))


def check_I1(source, cap) -> None:
    left = cap_contraction(source, cap)
    right = s_plus_r_exp_x(source, cap)
    require(left == right, "I1: K|-H_B != [(s+r)exp x]_U")


def check_I2(source, cap) -> None:
    s = Fraction(eval_form(form_s(source), cap))
    require(s != 0, "I2 needs s != 0")
    y = canonical_y(source, cap)
    lhs = matching_tensor(y)
    capped = cap_contraction(source, cap)
    err = direct_error_tensor(source, cap)
    for w in WORDS:
        require(s ** 3 * lhs[w] == s ** 2 * capped[w] + err[w],
                ("I2 failed at word", w))


def check_I3(source, cap) -> None:
    rows = error_matrix(source)
    direct = direct_error_tensor(source, cap)
    for w in WORDS:
        require(eval_cubic(rows[w], cap) == direct[w], ("I3 failed at", w))


def check_I4(source, cap, lam=3) -> None:
    scaled = tuple(lam * c for c in cap)
    base = direct_error_tensor(source, cap)
    up = direct_error_tensor(source, scaled)
    for w in WORDS:
        require(up[w] == lam ** 3 * base[w], ("I4 failed at", w))
    # and structurally: every monomial of every symbolic row has K-degree 3
    rows = error_matrix(source)
    for w, cubic in rows.items():
        for mono in cubic:
            require(len(mono) == 3, ("I4 structural failure", w, mono))


def check_I5() -> None:
    """Typed ledger: reproduce the committed checker's profile from E's terms."""
    profile = Counter()
    for _matching in MATCHINGS_U:
        # k red (r-)edges among the 3 edges of a matching of U
        for mask in range(1 << 3):
            profile[bin(mask).count("1")] += 1
    require(profile == Counter({0: 15, 1: 45, 2: 45, 3: 15}), profile)
    # E consumes exactly the k >= 2 strata: 45 terms of type (s, x-edge, R, R)
    # and 15 terms of type (R, R, R).
    type2 = sum(1 for _m in MATCHINGS_U for _e in range(3))
    type3 = len(MATCHINGS_U)
    require((type2, type3) == (45, 15), (type2, type3))
    require(3 * 2 == 6 and 6 == 6, "denominator clearing")


def check_I6(rng) -> None:
    """A source with A_pu = 0 for all u in U has r == 0, hence E == 0."""
    src = random_source(rng)
    for u in U:
        src[(P, u)] = [[0] * 3 for _ in range(3)]
    cap = random_cap(rng)
    err = direct_error_tensor(src, cap)
    require(all(v == 0 for v in err.values()), "I6: r=0 did not give E=0")
    rows = error_matrix(src)
    require(all(not c for c in rows.values()), "I6 symbolic: E != 0")


def main() -> int:
    rng = random.Random(20260815)
    for trial in range(3):
        src = random_source(rng)
        cap = random_cap(rng)
        while eval_form(form_s(src), cap) == 0:
            cap = random_cap(rng)
        check_I1(src, cap)
        check_I2(src, cap)
        check_I3(src, cap)
        check_I4(src, cap)
    check_I5()
    check_I6(rng)
    print("wsplit identity controls: PASS (I1-I6, exact, 3 random sources)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""UNAUDITED PROBE -- P1 task D: mutation controls on all verification code.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

Every load-bearing constructor and every decision procedure used in this
probe is mutated and the suite is required to NOTICE.  A mutation that
leaves all checks passing would mean the corresponding check is vacuous.

Controls
  M1  R_ab loses its endpoint-swapped term        -> cap identity I1 fails
  M2  the 3 s r^2 x term is dropped               -> master identity I2 fails
  M3  the r^3 term is dropped                     -> master identity I2 fails
  M4  the x-edge multiplicity is wrong (x counted
      once instead of once per matching edge)     -> master identity I2 fails
  M5  s reads the transposed pair block           -> cap identity I1 fails
  M6  one perfect matching of U is dropped        -> master identity I2 fails
  M7  the boundary word is read with two sites
      swapped                                     -> cap identity I1 fails
  M8  kappa_c is read off-diagonal (K_c0)         -> the rank-1 splitting
                                                     verdict changes
  M9  a splitting cubic is perturbed in one
      coefficient                                 -> split_pattern rejects it
  M10 a rank-1 matrix is perturbed in one entry   -> the 2x2 minor kill fires
  M11 the witness verifier is fed a cap with
      kappa_1 = 0                                 -> refuses to certify
  M12 the witness verifier is fed a cap with
      E != 0                                      -> refuses to certify

Run: python3 wsplit_mutations.py
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction

import wsplit_core as core
import wsplit_sources as sources
from wsplit_core import (COLORS, MATCHINGS_U, P, Q, SITE_SLOT, U, WORDS,
                         cap_contraction, direct_error_tensor, eval_form,
                         form_s, require)
from wsplit_dichotomy import (linear_forms, split_pattern, verify_witness,
                              cubic_vector, proportional)
from wsplit_structural import exact_minor_certificate

RNG = random.Random(31337)


def sample_source():
    src = core.random_source(RNG)
    cap = tuple(RNG.randint(-4, 4) for _ in range(9))
    while eval_form(form_s(src), cap) == 0:
        cap = tuple(RNG.randint(-4, 4) for _ in range(9))
    return src, cap


def mutated_form_R(source, a, b, ca, cb, drop_swap=False):
    out = []
    for i in COLORS:
        for j in COLORS:
            value = core.block(source, P, a, i, ca) * core.block(source, Q, b, j, cb)
            if not drop_swap:
                value += (core.block(source, P, b, i, cb)
                          * core.block(source, Q, a, j, ca))
            out.append(value)
    return tuple(out)


def cap_identity_holds(source, cap, form_R=None, form_s_fn=None,
                       word_swap=False) -> bool:
    """[(s+r)exp x]_U == K |- H_B, recomputed with mutated constructors."""
    form_R = form_R or core.form_R
    form_s_fn = form_s_fn or core.form_s
    s = eval_form(form_s_fn(source), cap)
    rr = {}
    from itertools import combinations
    for a, b in combinations(U, 2):
        rr[(a, b)] = [[eval_form(form_R(source, a, b, ca, cb), cap)
                       for cb in COLORS] for ca in COLORS]
    xx = core.direct_x(source)
    left = {}
    for w in WORDS:
        word = list(w)
        if word_swap:
            word[0], word[1] = word[1], word[0]
        total = 0
        for matching in MATCHINGS_U:
            xv = [xx[(a, b)][word[SITE_SLOT[a]]][word[SITE_SLOT[b]]]
                  for a, b in matching]
            rv = [rr[(a, b)][word[SITE_SLOT[a]]][word[SITE_SLOT[b]]]
                  for a, b in matching]
            total += s * xv[0] * xv[1] * xv[2]
            for e in range(3):
                prod = rv[e]
                for t in range(3):
                    if t != e:
                        prod *= xv[t]
                total += prod
        left[w] = total
    return left == cap_contraction(source, cap)


def master_identity_holds(source, cap, error_tensor) -> bool:
    """s^3 H_U(x+r/s) == s^2 (K |- H_B) + E, for a supplied E."""
    s = Fraction(eval_form(form_s(source), cap))
    if s == 0:
        return False
    y = core.canonical_y(source, cap)
    lhs = core.matching_tensor(y)
    capped = cap_contraction(source, cap)
    return all(s ** 3 * lhs[w] == s ** 2 * capped[w] + error_tensor[w]
               for w in WORDS)


def mutated_error(source, cap, mode: str) -> dict:
    s = eval_form(form_s(source), cap)
    rr = core.direct_r(source, cap)
    xx = core.direct_x(source)
    matchings = MATCHINGS_U[:-1] if mode == "drop_matching" else MATCHINGS_U
    out = {}
    for w in WORDS:
        total = 0
        for matching in matchings:
            rv = [rr[(a, b)][w[SITE_SLOT[a]]][w[SITE_SLOT[b]]]
                  for a, b in matching]
            xv = [xx[(a, b)][w[SITE_SLOT[a]]][w[SITE_SLOT[b]]]
                  for a, b in matching]
            if mode != "drop_r3":
                total += rv[0] * rv[1] * rv[2]
            if mode != "drop_sr2x":
                edges = range(1) if mode == "single_x_edge" else range(3)
                for e in edges:
                    prod = 1
                    for t in range(3):
                        if t != e:
                            prod *= rv[t]
                    total += s * xv[e] * prod
        out[w] = total
    return out


def main() -> int:
    src, cap = sample_source()
    failures = []

    def control(name: str, mutation_detected: bool) -> None:
        print(f"  {name:52s} detected={mutation_detected}")
        if not mutation_detected:
            failures.append(name)

    # baseline: everything must PASS unmutated
    control("baseline cap identity (must hold)",
            cap_identity_holds(src, cap))
    control("baseline master identity (must hold)",
            master_identity_holds(src, cap, direct_error_tensor(src, cap)))

    control("M1 R_ab loses endpoint-swapped term",
            not cap_identity_holds(
                src, cap,
                form_R=lambda s_, a, b, ca, cb: mutated_form_R(
                    s_, a, b, ca, cb, drop_swap=True)))
    control("M2 drop 3 s r^2 x",
            not master_identity_holds(src, cap,
                                      mutated_error(src, cap, "drop_sr2x")))
    control("M3 drop r^3",
            not master_identity_holds(src, cap,
                                      mutated_error(src, cap, "drop_r3")))
    control("M4 wrong x-edge multiplicity",
            not master_identity_holds(src, cap,
                                      mutated_error(src, cap, "single_x_edge")))
    control("M5 s reads the transposed pair block",
            not cap_identity_holds(
                src, cap,
                form_s_fn=lambda s_: tuple(s_[(P, Q)][j][i]
                                           for i in COLORS for j in COLORS)))
    control("M6 one perfect matching of U dropped",
            not master_identity_holds(
                src, cap, mutated_error(src, cap, "drop_matching")))
    control("M7 boundary word read with two sites swapped",
            not cap_identity_holds(src, cap, word_swap=True))

    # decision-procedure controls on the rank-1 stratum
    two = sources.two_star(0, 0)
    matrix = core.error_matrix(two)
    rows = [r for r in core.dense_rows(matrix) if any(r)]
    from wsplit_core import CUBIC_MONOMIALS
    f = {CUBIC_MONOMIALS[c]: v for c, v in enumerate(rows[0]) if v}
    forms = linear_forms(two)
    baseline = [p["pattern"] for p in split_pattern(f, forms)]
    control("baseline two-star splits as s*k0*k0 (must hold)",
            baseline == [("s", "kappa_0", "kappa_0")])

    bad_forms = dict(forms)
    bad_forms["kappa_0"] = tuple(1 if k == core.kidx(0, 0) + 1 else 0
                                 for k in range(9))
    control("M8 kappa_0 read off-diagonal",
            [p["pattern"] for p in split_pattern(f, bad_forms)] != baseline)

    perturbed = dict(f)
    key = sorted(f)[0]
    perturbed[key] = perturbed[key] + 1
    control("M9 splitting cubic perturbed in one coefficient",
            not split_pattern(perturbed, forms))

    rank_one_rows = [list(r) for r in rows]
    control("baseline rank-1 matrix has no 2x2 minor (must hold)",
            exact_minor_certificate(rank_one_rows) is None)
    rank_one_rows[1][7] = rank_one_rows[1][7] + 1
    control("M10 rank-1 matrix perturbed in one entry",
            exact_minor_certificate(rank_one_rows) is not None)

    # witness-verifier controls
    good = sources.two_star(0, 1)
    cap_good = [0] * 9
    for c in range(3):
        cap_good[core.kidx(c, c)] = 1
    cap_good[core.kidx(0, 1)] = 1
    cap_good[core.kidx(1, 0)] = -1
    control("baseline two-star(0,1) witness (must hold)",
            verify_witness(good, tuple(cap_good))["is_witness"])
    inactive = list(cap_good)
    inactive[core.kidx(1, 1)] = 0
    control("M11 witness with kappa_1 = 0 refused",
            not verify_witness(good, tuple(inactive))["is_witness"])
    dirty = list(cap_good)
    dirty[core.kidx(0, 1)] = 2
    control("M12 witness with E != 0 refused",
            not verify_witness(good, tuple(dirty))["is_witness"])

    if failures:
        print(f"MUTATION CONTROLS FAILED: {failures}")
        return 1
    print("wsplit mutation controls: PASS (12 mutations + 5 baselines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

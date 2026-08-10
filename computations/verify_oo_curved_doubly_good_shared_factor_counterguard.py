#!/usr/bin/env python3
"""Exact extra-term guard for the curved-OO shared-factor proposal.

The minimal active packet of ``verify_oo_curved_doubly_good_minimal_fullnine_unit``
has

    g_diag = x*y*z - 1,       g_mix = y*z.

Curvature, goodness, and cofactor activity do not make the second row private.
Adding the first two missing cells of an alternate matching gives

    a=A01(1,1), b=A45(1,1),  g_mix = y*z + a*b*z.

The pure row is unchanged.  The mixed monomial gcd is now only z, so none of
P/x, P/y, P/z for P=xyz divides the whole mixed row.  Moreover the two-row
Laurent ideal is proper: x=y=z=a=1, b=-1 is a rational torus point.  Thus a
shared factor by itself would not imply a unit, and in this guard even the
proposed P/variable factor is absent.

The complete source packet is nevertheless empty for an independent reason:
it already has literal monomial zero rows.  This is a counterguard to the
proposed *two-row transport*, not a Krenn counterexample.  A valid transport
needs physical private-matching provenance (or source equations killing every
alternate matching), which is not implied by rank, curvature, or activity.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_oo_curved_doubly_good_minimal_fullnine_unit.py":
        "5340f74c4f430241d006b69db35cac464fc227f369de52db17c10e8d19253396",
    "computations/verify_oo_lambda_conservation_all_order.py":
        "72402e9a3e97e72b1547349f80943950e0c6d521d46adfd6ef4baefb82a4d0b3",
}
EXPECTED_LEDGER_SHA256 = (
    "3e51409d068f9ac18a95dd14602dacfdfa573ae2073e671ec34c8a20eb093d14"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_pinned(name, relative):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINS[relative],
            f"dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


UNIT_PATH = (
    "computations/verify_oo_curved_doubly_good_minimal_fullnine_unit.py"
)
LAMBDA_PATH = "computations/verify_oo_lambda_conservation_all_order.py"
unit = load_pinned("oo_minimal_fullnine_unit", UNIT_PATH)
require(sha256((ROOT / LAMBDA_PATH).read_bytes()).hexdigest()
        == PINS[LAMBDA_PATH], "the all-order Lambda/Hasse no-go changed")
base = unit.base
frontier = unit.frontier


CONTAMINANTS = (
    (0, 1, 1, 1),  # a=A01(1,1)
    (4, 5, 1, 1),  # b=A45(1,1)
)
VARIABLES = ("x=A03_11", "y=A15_11", "z=A67_11",
             "a=A01_11", "b=A45_11")


def source_distance_audit(blocks):
    """Audit only the 105 matchings of the selected off-diagonal word."""
    old_support = set(blocks) | set(unit.CANONICAL_ADDED)
    old_index = {
        cell: index for index, cell in enumerate(unit.CANONICAL_ADDED)
    }
    records = []
    histogram = Counter()
    for matching in base.perfect_matchings(base.VERTICES):
        cells = tuple(base.key(u, v, unit.MIXED_WORD[u], unit.MIXED_WORD[v])
                      for u, v in matching)
        missing = tuple(cell for cell in cells if cell not in old_support)
        old_mask = sum(1 << old_index[cell]
                       for cell in cells if cell in old_index)
        histogram[len(missing)] += 1
        records.append((len(missing), missing, old_mask, matching, cells))

    require(histogram == Counter({4: 50, 3: 38, 2: 15, 1: 1, 0: 1}),
            f"the selected-word matching distances changed: {histogram}")
    distance_one = [record for record in records if record[0] == 1]
    require(len(distance_one) == 1
            and distance_one[0][1] == ((3, 4, 0, 1),)
            and distance_one[0][2] == 6,
            "the unique one-cell contaminant changed")

    distance_two = sorted(
        (record for record in records if record[0] == 2),
        key=lambda record: record[1],
    )
    losing_yz = [record for record in distance_two
                 if record[2] & 6 != 6]
    require(len(distance_two) == 15 and len(losing_yz) == 14,
            "the first loss of the old yz factor changed")
    first = losing_yz[0]
    require(first[1] == CONTAMINANTS and first[2] == 4
            and first[3] == ((0, 1), (2, 3), (4, 5), (6, 7)),
            "the lexicographically first factor-losing matching changed")
    return histogram, distance_one[0], first, len(losing_yz)


def factor_guard(blocks):
    added = unit.CANONICAL_ADDED + CONTAMINANTS
    tensor = frontier.tensor_polynomials(blocks, added)
    residuals = frontier.target_residuals(tensor)
    pure = residuals[unit.PURE_ONE]
    mixed = residuals[unit.MIXED_WORD]
    require(pure == {0: Fraction(-1), 7: Fraction(1)},
            f"the pure anchor acquired an extra matching: {pure}")
    require(mixed == {6: Fraction(1), 28: Fraction(1)},
            f"the selected mixed row changed: {mixed}")

    pure_terms = unit.matching_terms(blocks, added, unit.PURE_ONE)
    mixed_terms = unit.matching_terms(blocks, added, unit.MIXED_WORD)
    require(pure_terms == (
        (((0, 3), (1, 5), (2, 4), (6, 7)), 7),
    ), "the pure source provenance changed")
    require(mixed_terms == (
        (((0, 1), (2, 3), (4, 5), (6, 7)), 28),
        (((0, 4), (1, 5), (2, 3), (6, 7)), 6),
    ), "the two mixed source matchings changed")

    monomial_gcd = reduce(int.__and__, mixed)
    p_over_variable = {"P/x": 6, "P/y": 5, "P/z": 3}
    divisibility = {
        name: all(mask & candidate == candidate for mask in mixed)
        for name, candidate in p_over_variable.items()
    }
    require(monomial_gcd == 4 and not any(divisibility.values()),
            "a proposed P/variable factor unexpectedly divides the row")

    # x*g_mix-g_diag = 1+x*a*b*z, not 1.
    failed_certificate = unit.add_polynomials(
        unit.multiply_squarefree(mixed, 1), pure, -1
    )
    require(failed_certificate == {0: Fraction(1), 29: Fraction(1)},
            f"the failed two-row identity changed: {failed_certificate}")

    # Exact torus point for just these two rows: (x,y,z,a,b)=(1,1,1,1,-1).
    point = (Fraction(1), Fraction(1), Fraction(1),
             Fraction(1), Fraction(-1))

    def evaluate(polynomial):
        total = Fraction(0)
        for mask, coefficient in polynomial.items():
            monomial = Fraction(1)
            for index, value in enumerate(point):
                if mask & (1 << index):
                    monomial *= value
            total += coefficient * monomial
        return total

    require(all(point) and evaluate(pure) == 0 and evaluate(mixed) == 0,
            "the rational Laurent counterpoint changed")

    numeric = dict(blocks)
    for cell in added:
        base.add_cell(numeric, *cell)
    direct_ranks = (
        base.rational_rank(base.direct_matrix(numeric, base.P, base.Q)),
        base.rational_rank(base.direct_matrix(numeric, base.P, base.R)),
    )
    star_ranks = (
        base.star_rank(numeric, base.P, base.Q),
        base.star_rank(numeric, base.Q, base.P),
        base.star_rank(numeric, base.P, base.R),
        base.star_rank(numeric, base.R, base.P),
    )
    curvature = (
        base.entry(numeric, base.P, base.Q, 1, 0)
        * base.entry(numeric, base.R, base.FOURTH, 1, 0)
        - base.entry(numeric, base.P, base.R, 1, 1)
        * base.entry(numeric, base.Q, base.FOURTH, 0, 0)
    )
    activity = tuple(frontier.is_support_active(blocks, added, arm)
                     for arm in frontier.ARMS)
    rulings = (
        base.audit_ruling(numeric, (base.P, base.Q), 0),
        base.audit_ruling(numeric, (base.P, base.R), 1),
    )
    require(direct_ranks == (1, 1) and star_ranks == (3, 3, 3, 3)
            and curvature == -1 and activity == (True, True)
            and rulings == ((3,), (2,)),
            "the curved doubly-good/activity hypotheses changed")

    cofactors = {
        "pq": frontier.cofactor_polynomials(
            blocks, added, (base.P, base.Q)),
        "pr": frontier.cofactor_polynomials(
            blocks, added, (base.P, base.R)),
    }
    require(cofactors == {
        "pq": {
            (1, 2, 2, 1, 0, 0): {2: Fraction(1)},
            (1, 2, 2, 1, 1, 1): {6: Fraction(1)},
        },
        "pr": {
            (1, 0, 0, 1, 0, 0): {2: Fraction(1)},
            (1, 0, 0, 1, 1, 1): {6: Fraction(1)},
        },
    }, "the two active cofactors changed")

    # Do not overclaim: the complete packet is already killed by unrelated
    # monomial rows, e.g. the displayed z row.  The guard concerns only the
    # proposed diagonal/off-diagonal two-row transport.
    singleton_rows = {
        word: polynomial for word, polynomial in residuals.items()
        if len(polynomial) == 1
    }
    require(singleton_rows[(0, 0, 0, 0, 0, 0, 1, 1)]
            == {4: Fraction(1)} and len(singleton_rows) == 12,
            "the independent full-packet monomial obstruction changed")
    size_histogram = Counter(len(polynomial)
                             for polynomial in residuals.values())
    require(len(residuals) == 15
            and size_histogram == Counter({1: 12, 2: 3}),
            "the complete sparse full-row census changed")

    return {
        "support_cells": len(blocks) + len(added),
        "variables": list(VARIABLES),
        "contaminating_cells": [f"{u}{v}:{i}{j}"
                                for u, v, i, j in CONTAMINANTS],
        "direct_arm_ranks": list(direct_ranks),
        "good_star_ranks": list(star_ranks),
        "curvature": str(curvature),
        "both_arm_cofactors_active": list(activity),
        "active_rulings": [list(ruling) for ruling in rulings],
        "pure_row": "x*y*z-1",
        "mixed_row": "y*z+a*b*z",
        "mixed_monomial_gcd": "z",
        "p_over_variable_divisibility": divisibility,
        "failed_identity": "x*g_mix-g_diag=1+x*a*b*z",
        "two_row_laurent_point": [str(value) for value in point],
        "pure_matching_count": len(pure_terms),
        "mixed_matching_count": len(mixed_terms),
        "nonzero_full_rows": len(residuals),
        "full_row_term_count_histogram": dict(sorted(size_histogram.items())),
        "independent_monomial_zero_rows": len(singleton_rows),
        "displayed_independent_unit_row": "word 00000011: z=0",
    }


def main():
    blocks = base.build_packet()
    require(len(blocks) == 11,
            "the alternating-C8 two-anchor packet size changed")
    distance_histogram, distance_one, distance_two, losing_count = (
        source_distance_audit(blocks)
    )
    guard = factor_guard(blocks)
    ledger = {
        "pins": PINS,
        "selected_word_matching_distance_histogram": dict(sorted(
            distance_histogram.items())),
        "unique_one_cell_contaminant": {
            "cell": f"{distance_one[1][0][0]}{distance_one[1][0][1]}:"
                    f"{distance_one[1][0][2]}{distance_one[1][0][3]}",
            "old_variable_mask": distance_one[2],
            "effect": "multiplies the old yz row by 1+t; factor remains but unit does not",
        },
        "two_cell_alternates": 15,
        "two_cell_alternates_losing_yz": losing_count,
        "first_factor_losing_alternate": {
            "missing_cells": [f"{u}{v}:{i}{j}"
                              for u, v, i, j in distance_two[1]],
            "old_variable_mask": distance_two[2],
            "matching": [list(edge) for edge in distance_two[3]],
        },
        "guard": guard,
        "theorem_boundary": (
            "rank-one direct arms, four good stars, nonzero curvature, and "
            "two active arm cofactors do not force the needed private mixed "
            "matching; a transport theorem must additionally prove a unique "
            "support-live offdiagonal matching P/x, or use pinned physical "
            "source rows to annihilate every alternate matching"
        ),
        "scope": (
            "counterguard to the proposed diagonal/offdiagonal two-row "
            "shared-factor transport only; the complete displayed support is "
            "not coefficient-feasible because independent monomial rows kill it"
        ),
        "lambda_hasse_scope_guard": (
            "all equations are literal physical full-output source rows; no "
            "Ward, jet, Hasse, or cap-codomain generator is introduced"
        ),
        "verdict": (
            "the proposed generalization is false from curved doubly-good "
            "activity alone: an exact two-matching contamination preserves all "
            "those hypotheses but removes every P/variable factor from the "
            "selected mixed row and leaves its two-row Laurent ideal proper"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"curved-OO shared-factor guard changed: {digest}")

    print("curved doubly-good shared-factor counterguard: PASS")
    print("selected-word distance histogram: 0:1 1:1 2:15 3:38 4:50")
    print("first factor-losing cells: A01_11, A45_11")
    print("rows: g_diag=x*y*z-1; g_mix=y*z+a*b*z")
    print("two-row Laurent point: (x,y,z,a,b)=(1,1,1,1,-1)")
    print("scope: transport guard only; 12 other monomial rows kill full packet")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

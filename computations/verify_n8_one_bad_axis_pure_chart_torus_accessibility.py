#!/usr/bin/env python3
"""Target-compatible torus obstruction to the axis-pure chart.

Write h(v,c) for the site/colour cocharacter, mu for the common source-cell
weight retained after a scalar source gauge, and T_c for the three pure
target weights.  Retaining the twelve cells of the endpoint-minor pure chart
requires weight mu on every anchor; response compatibility requires
T_c=sum_v h(v,c)=4*mu.

The two extra residual cells 01:02 and 34:02 form a character circuit with
the retained anchors 03:00 and 14:22.  Their relative weights sum to zero.
Thus a finite limit on both extras retains both, and no target-compatible
torus can delete them while retaining the pure chart.  The obstruction is
minimal: no single residual extra cell is forced to weight zero.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib
import itertools
import json
from math import gcd, lcm
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_endpoint_minor_arbitrary_pure_unary_completion.py":
        "f77b99d56d817689e55f4790e000799bc34c9b6960d2b9f035300d407562f20a",
    "computations/verify_n8_one_bad_multisite_permanent_null_defect.py":
        "94946c00fc25cd08eead06148deae85cc2ed80e0cce65c68bc37ad50384f6f53",
}
EXPECTED_LEDGER_SHA256 = (
    "4fe9868ecd42282b535680ce921ea989c2c62c02cd2085797a55dcb7eafa8a53"
)

VERTICES = tuple(range(8))
RESIDUAL = tuple(range(6))
COLOURS = tuple(range(3))
WIDTH = 28
MU = 24
TARGET = {colour: 25 + colour for colour in COLOURS}

# Canonical endpoint order throughout.
ANCHORS = (
    (0, 3, 0, 0), (1, 2, 0, 0), (4, 5, 0, 0), (6, 7, 0, 0),
    (0, 6, 1, 1), (1, 7, 1, 1), (2, 4, 1, 1), (3, 5, 1, 1),
    (0, 5, 2, 2), (1, 4, 2, 2), (2, 6, 2, 2), (3, 7, 2, 2),
)
EXTRA_LEFT = (0, 1, 0, 2)
EXTRA_RIGHT = (3, 4, 0, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def cell_character(cell, relative=True):
    left, right, left_colour, right_colour = cell
    row = [Fraction(0)] * WIDTH
    row[3 * left + left_colour] += 1
    row[3 * right + right_colour] += 1
    if relative:
        row[MU] -= 1
    return tuple(row)


def add_rows(*rows):
    return tuple(sum(values, Fraction(0)) for values in zip(*rows, strict=True))


def scale_row(row, scalar):
    return tuple(scalar * value for value in row)


def equation_matrix():
    rows = [cell_character(cell) for cell in ANCHORS]
    for colour in COLOURS:
        definition = [Fraction(0)] * WIDTH
        for vertex in VERTICES:
            definition[3 * vertex + colour] += 1
        definition[TARGET[colour]] -= 1
        rows.append(tuple(definition))

        response = [Fraction(0)] * WIDTH
        response[TARGET[colour]] += 1
        response[MU] -= 4
        rows.append(tuple(response))
    return tuple(rows)


def rref(rows):
    matrix = [list(row) for row in rows]
    pivots = []
    pivot_row = 0
    for column in range(WIDTH):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale
                             for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [value - scale * pivot_value
                           for value, pivot_value
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:pivot_row]), tuple(pivots)


def nullspace(rows):
    reduced, pivots = rref(rows)
    free = tuple(column for column in range(WIDTH) if column not in pivots)
    basis = []
    for free_column in free:
        vector = [Fraction(0)] * WIDTH
        vector[free_column] = 1
        for row, pivot in zip(reversed(reduced), reversed(pivots), strict=True):
            vector[pivot] = -sum(
                coefficient * vector[column]
                for column, coefficient in enumerate(row) if column != pivot
            )
        basis.append(tuple(vector))
    return basis, pivots


def pairing(row, vector):
    return sum(left * right for left, right in zip(row, vector, strict=True))


def quotient_character(cell, basis):
    row = cell_character(cell)
    return tuple(pairing(row, vector) for vector in basis)


def primitive(vector):
    denominator = 1
    for value in vector:
        denominator = lcm(denominator, value.denominator)
    integers = [int(value * denominator) for value in vector]
    common = 0
    for value in integers:
        common = gcd(common, abs(value))
    require(common, "the zero vector has no primitive ray")
    return tuple(value // common for value in integers)


def canonical_cell(left, right, left_colour, right_colour):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def pure_matching_audit(module, support):
    result = {}
    for colour in COLOURS:
        edges = {
            (left, right) for left, right, left_colour, right_colour in support
            if left_colour == right_colour == colour
        }
        matchings = tuple(
            matching for matching in module.perfect_matchings(VERTICES)
            if all(edge in edges for edge in matching)
        )
        result[colour] = matchings
    return result


def main():
    pin_dependencies()
    module = importlib.import_module(
        "verify_n8_one_bad_multisite_permanent_null_defect")

    equations = equation_matrix()
    basis, pivots = nullspace(equations)
    require((len(equations), len(pivots), len(basis)) == (18, 15, 13),
            "the target-compatible chart character dimensions changed")

    # All target weights are explicit variables.  These six equations say
    # T_c=sum_v h(v,c)=4*mu.  The latter equality is the degree-four source
    # gauge needed for the exact pure targets to have weight zero after the
    # source cells are shifted by mu.
    require(all(not pairing(row, vector)
                for row in equations for vector in basis),
            "the computed kernel violates a target/chart equation")

    left_row = cell_character(EXTRA_LEFT)
    right_row = cell_character(EXTRA_RIGHT)
    anchor_03 = cell_character((0, 3, 0, 0))
    anchor_14 = cell_character((1, 4, 2, 2))
    require(add_rows(left_row, right_row)
            == add_rows(anchor_03, anchor_14),
            "the four-port character circuit changed")
    require(all(not pairing(anchor, vector)
                for anchor in (anchor_03, anchor_14) for vector in basis),
            "a chart anchor moved in the solution space")

    left_quotient = quotient_character(EXTRA_LEFT, basis)
    right_quotient = quotient_character(EXTRA_RIGHT, basis)
    require(left_quotient == scale_row(right_quotient, -1)
            and any(left_quotient),
            "the two extras stopped being opposing quotient characters")

    # A concrete integral cocharacter deletes either extra singly (reverse
    # its sign to delete the other), but makes the mate negative.  Thus the
    # obstruction genuinely first appears at two extra cells.
    witness_rows = (
        (1, 1, 1), (1, 1, 1), (0, 1, 1), (0, 1, 1),
        (1, 0, 0), (0, 0, 0), (1, 0, 0), (0, 0, 0),
    )
    witness = tuple(Fraction(value) for row in witness_rows for value in row)
    witness += (Fraction(1), Fraction(4), Fraction(4), Fraction(4))
    require(len(witness) == WIDTH and all(not pairing(row, witness)
                                          for row in equations),
            "the integral one-extra cocharacter changed")
    require((pairing(left_row, witness), pairing(right_row, witness))
            == (1, -1),
            "the integral cocharacter no longer separates the extra pair")

    anchor_set = frozenset(ANCHORS)
    residual_extras = tuple(
        (left, right, left_colour, right_colour)
        for left, right in itertools.combinations(RESIDUAL, 2)
        for left_colour, right_colour in itertools.product(COLOURS, repeat=2)
        if (left, right, left_colour, right_colour) not in anchor_set
    )
    require(len(residual_extras) == 128,
            "the residual extra-cell universe changed")
    quotient = {cell: quotient_character(cell, basis)
                for cell in residual_extras}
    require(all(any(vector) for vector in quotient.values()),
            "a single residual extra became torically forced")

    offdiagonal = tuple(cell for cell in residual_extras
                        if cell[2] != cell[3])
    opposing_pairs = []
    rays = {cell: primitive(quotient[cell]) for cell in offdiagonal}
    for index, left in enumerate(offdiagonal):
        for right in offdiagonal[index + 1:]:
            left_ray, right_ray = rays[left], rays[right]
            pivot = next((position for position, value
                          in enumerate(left_ray) if value), None)
            require(pivot is not None, "an offdiagonal ray vanished")
            if (all(left_ray[position] * right_ray[pivot]
                    == right_ray[position] * left_ray[pivot]
                    for position in range(len(left_ray)))
                    and left_ray[pivot] * right_ray[pivot] < 0):
                opposing_pairs.append((left, right))
    require(len(offdiagonal) == 90 and len(opposing_pairs) == 22,
            "the mixed-cell opposing-ray census changed")
    require(opposing_pairs[0] == (EXTRA_LEFT, EXTRA_RIGHT),
            f"the minimal opposing pair changed: {opposing_pairs[0]}")

    support = anchor_set | frozenset((EXTRA_LEFT, EXTRA_RIGHT))
    pure_matchings = pure_matching_audit(module, support)
    expected_matchings = {
        0: (((0, 3), (1, 2), (4, 5), (6, 7)),),
        1: (((0, 6), (1, 7), (2, 4), (3, 5)),),
        2: (((0, 5), (1, 4), (2, 6), (3, 7)),),
    }
    require(pure_matchings == expected_matchings,
            f"the three unique pure anchors changed: {pure_matchings}")

    ledger = {
        "dependencies": PINS,
        "weight_variables": {
            "site_colour": 24,
            "source_gauge_mu": 1,
            "pure_target_weights": 3,
            "total": WIDTH,
        },
        "equations": {
            "chart_anchor_equalities": len(ANCHORS),
            "target_definitions": 3,
            "response_compatibility_Tc_equals_4mu": 3,
            "rows": len(equations),
            "rank": len(pivots),
            "solution_dimension": len(basis),
        },
        "minimal_counterguard": {
            "retained_chart_cells": len(ANCHORS),
            "extras": (EXTRA_LEFT, EXTRA_RIGHT),
            "character_identity": (
                "chi(01:02)+chi(34:02)=chi(03:00)+chi(14:22)"
            ),
            "relative_weight_identity": "ell_01:02+ell_34:02=0",
            "finite_limit_consequence": (
                "ell_left,ell_right>=0 forces ell_left=ell_right=0"
            ),
        },
        "minimality": {
            "residual_single_cells_tested": len(residual_extras),
            "forced_single_cells": 0,
            "offdiagonal_cells": len(offdiagonal),
            "opposing_offdiagonal_pairs": len(opposing_pairs),
            "single_cell_integral_witness": {
                "site_colour_rows": witness_rows,
                "mu": 1,
                "target_weights": (4, 4, 4),
                "extra_relative_weights": (1, -1),
            },
        },
        "permutation_guard": {
            "pure_matching_counts": {
                colour: len(matchings)
                for colour, matchings in pure_matchings.items()
            },
            "reason": (
                "the support has a unique pure matching in every colour; "
                "site/colour permutations only relabel the same circuit"
            ),
        },
        "verdict": (
            "axis purification alone does not place a source in the pure "
            "chart by a response-compatible torus: a two-cell mixed carrier "
            "circuit is retained in every finite chart-preserving limit"
        ),
        "required_non_toric_input": (
            "a source-valid matching exchange, coefficient cancellation, or "
            "non-diagonal colour operation must remove one member of every "
            "opposing carrier pair before the pure-chart theorem applies"
        ),
        "scope": (
            "exact character/inequality obstruction for the pinned pure-chart "
            "anchors plus a minimal axis-purified leading support; it is not "
            "an exact one-bad coefficient point and does not prove that source "
            "equations permit this counterguard support"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the torus accessibility ledger changed: {digest}")

    print("N=8 axis-pure chart torus accessibility: PASS")
    print("weight system: 28 variables, 18 equations, rank 15")
    print("single residual extras forced: 0/128")
    print("minimal mixed counterguard: 01:02 and 34:02")
    print("relative weights sum to zero; no finite toric deletion")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

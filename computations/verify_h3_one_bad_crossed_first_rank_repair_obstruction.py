#!/usr/bin/env python3
"""First source-deformation obstruction for the crossed one-bad packet.

At the exact crossed calibration of eb4bb0c, compute every one-cell affine
modification and the complete 6561-output Jacobian in all 252 physical
coordinates.  No one-cell modification reaches GHZ.  More strongly, the
linear correction equation is inconsistent, and every output-preserving
tangent has zero projection to the 36 cells which could repair either
missing selected-colour row of the bad pq endpoint stars.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_crossed_quadratic_oo_landing_guard.py":
        "9c629cd7ee51241f6170619c354b1417b636cd53b1faba35629cb57a2ae83281",
    "notes/h3-one-bad-crossed-quadratic-oo-landing-guard.md":
        "099be2be98f25876c5c6116d68669ef8c866b85f4b2c4eeefbf43b7a88c45382",
    "computations/verify_h3_one_bad_common_q_cap_extraction_boundary.py":
        "02517a037d7dfc273d2eee63dd85e8228d88cd4824397b7ac478c013624afe5e",
    "computations/verify_h3_one_bad_second_principal_parts_companion_closure.py":
        "3612f9d7c03a3e265792543cd602f27ebf64830390f95b5bddb8d953d238c3f5",
    "computations/verify_oo_doubly_good_two_anchor_counterguard.py":
        "b9d986f4e1725082c1101e73729018a6d66296aef628879de50b03508f804699",
}
EXPECTED_LEDGER_SHA256 = (
    "cbc2526a4a5c876630cf430ac0e6ae6b8a174835c16fea89a75a66cac850a947"
)

SEPARATOR = {
    tuple(map(int, "00000000")): Fraction(1),
    tuple(map(int, "00000110")): Fraction(-1),
    tuple(map(int, "00111000")): Fraction(-2),
    tuple(map(int, "00222112")): Fraction(2),
    tuple(map(int, "11012002")): Fraction(1),
    tuple(map(int, "11012112")): Fraction(1),
    tuple(map(int, "12000210")): Fraction(-1),
    tuple(map(int, "12111210")): Fraction(2),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def build_crossed_source(base, closure):
    source = dict(closure.build_eight_site_source(base, Fraction(-1)))
    source[base.cell(1, 7, 1, 1)] = Fraction(1)  # R_c@1
    source[base.cell(2, 5, 0, 1)] = Fraction(1)  # P_c@2
    return source


def derivative_column(oo, source, cell):
    """Derivative of the full hafnian tensor in one physical cell."""

    u, v, a, b = cell
    residual = tuple(site for site in range(8) if site not in (u, v))
    output = defaultdict(Fraction)
    for matching in oo.perfect_matchings(residual):
        choices = []
        for left, right in matching:
            available = [
                (i, j, coefficient)
                for i in range(3) for j in range(3)
                if (coefficient := oo.entry(source, left, right, i, j))
            ]
            if not available:
                choices = []
                break
            choices.append(available)
        if not choices:
            continue
        for selected in product(*choices):
            word = [None] * 8
            word[u], word[v] = a, b
            coefficient = Fraction(1)
            for (left, right), (i, j, value) in zip(
                    matching, selected, strict=True):
                word[left], word[right] = i, j
                coefficient *= value
            output[tuple(word)] += coefficient
    return {word: value for word, value in output.items() if value}


def sparse_rank(rows, columns, residual=None):
    """Exact rational row rank, optionally after adjoining one RHS."""

    pivots = {}
    rhs_index = max(columns, default=-1) + 1
    for word in rows:
        row = {
            column: value
            for column, values in columns.items()
            if (value := values.get(word))
        }
        if residual is not None and residual.get(word):
            row[rhs_index] = -residual[word]
        while row:
            pivot = min(row)
            if pivot not in pivots:
                scale = row[pivot]
                pivots[pivot] = {
                    column: value / scale for column, value in row.items()
                }
                break
            scale = row[pivot]
            old = pivots[pivot]
            for column, value in old.items():
                row[column] = row.get(column, Fraction(0)) - scale * value
                if not row[column]:
                    del row[column]
    return len(pivots)


def is_rank_repair_cell(cell):
    """A cell in either missing a-row, generously including other arm cells."""

    u, v, a, b = cell
    p, q = 5, 6
    return (
        (u == p and v != q and a == 0)
        or (v == p and u != q and b == 0)
        or (u == q and v != p and a == 0)
        or (v == q and u != p and b == 0)
    )


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    closure = importlib.import_module(
        "verify_h3_one_bad_second_principal_parts_companion_closure")
    oo = importlib.import_module(
        "verify_oo_doubly_good_two_anchor_counterguard")
    source = build_crossed_source(base, closure)

    tensor, _supported = oo.matching_tensor(source)
    residual = dict(tensor)
    for colour in range(3):
        word = (colour,) * 8
        residual[word] = residual.get(word, Fraction(0)) - 1
    residual = {word: value for word, value in residual.items() if value}
    require(len(residual) == 10, "the crossed residual packet changed")

    cells = tuple(
        (u, v, a, b)
        for u, v in combinations(range(8), 2)
        for a in range(3) for b in range(3)
    )
    require(len(cells) == 252, "the physical coordinate count changed")
    derivatives = {
        index: derivative_column(oo, source, cell)
        for index, cell in enumerate(cells)
    }
    all_rows = tuple(sorted(
        set(residual).union(*(set(column) for column in derivatives.values()))
    ))
    require(len(all_rows) == 639, "the first-deformation row set changed")
    require(sum(map(len, derivatives.values())) == 837,
            "the Jacobian nonzero count changed")

    # Since the hafnian is multiaffine in an individual physical cell,
    # source + s*cell is exactly tensor + s*derivative_column.  Thus this is
    # an exact affine one-cell census, not only a tangent test.
    one_cell_solutions = []
    for index, column in derivatives.items():
        scalars = []
        works = True
        for word in set(residual) | set(column):
            left = column.get(word, Fraction(0))
            right = residual.get(word, Fraction(0))
            if not left:
                if right:
                    works = False
                    break
            else:
                scalars.append(-right / left)
        if (works and scalars and scalars[0]
                and all(value == scalars[0] for value in scalars)):
            one_cell_solutions.append((cells[index], scalars[0]))
    require(not one_cell_solutions,
            f"a one-cell exact completion appeared: {one_cell_solutions}")

    repair_indices = tuple(
        index for index, cell in enumerate(cells) if is_rank_repair_cell(cell)
    )
    nonrepair_indices = tuple(
        index for index in range(len(cells)) if index not in repair_indices
    )
    require(len(repair_indices) == 36,
            f"the generous rank-repair universe changed: {len(repair_indices)}")

    # Every direct rank repair is invisible on the ten current residuals and
    # creates at least one fresh source label.  This is the literal first-row
    # reason no single repair can work.
    repair_tail_histogram = Counter()
    for index in repair_indices:
        column = derivatives[index]
        require(not set(column) & set(residual),
                f"a rank repair hit an old residual: {cells[index]}")
        require(column, f"a rank repair had zero derivative: {cells[index]}")
        repair_tail_histogram[len(column)] += 1
    require(repair_tail_histogram == Counter({1: 6, 2: 6, 3: 12, 4: 9, 5: 3}),
            f"the rank-repair tail histogram changed: {repair_tail_histogram}")

    full_columns = derivatives
    nonrepair_columns = {
        new_index: derivatives[old_index]
        for new_index, old_index in enumerate(nonrepair_indices)
    }
    rank_full = sparse_rank(all_rows, full_columns)
    rank_augmented = sparse_rank(all_rows, full_columns, residual)
    rank_nonrepair = sparse_rank(all_rows, nonrepair_columns)
    rank_nonrepair_augmented = sparse_rank(
        all_rows, nonrepair_columns, residual
    )
    require((rank_full, rank_augmented) == (245, 246),
            f"the affine tangent cokernel changed: {(rank_full, rank_augmented)}")
    require((rank_nonrepair, rank_nonrepair_augmented) == (209, 210),
            "the nonrepair affine tangent cokernel changed")

    full_nullity = len(cells) - rank_full
    nonrepair_nullity = len(nonrepair_indices) - rank_nonrepair
    require((full_nullity, nonrepair_nullity) == (7, 7),
            "the homogeneous tangent nullities changed")
    # ker(J) intersect {repair=0} is exactly ker(J_nonrepair).  Equal
    # dimensions therefore prove that every vector in ker(J) has all 36
    # repair coordinates zero.
    require(full_nullity == nonrepair_nullity,
            "an output-preserving tangent acquired a rank-repair coordinate")

    # A small primitive left-cokernel witness independently certifies the
    # rank jump.  These are eight literal full-output word labels.
    for index, column in derivatives.items():
        pairing = sum(
            coefficient * column.get(word, Fraction(0))
            for word, coefficient in SEPARATOR.items()
        )
        require(not pairing,
                f"the separator sees Jacobian column {cells[index]}: {pairing}")
    residual_pairing = sum(
        coefficient * residual.get(word, Fraction(0))
        for word, coefficient in SEPARATOR.items()
    )
    require(residual_pairing == -1,
            f"the primitive residual pairing changed: {residual_pairing}")
    require(gcd(*(abs(value.numerator) for value in SEPARATOR.values())) == 1,
            "the eight-row separator stopped being primitive")

    ledger = {
        "dependencies": PINS,
        "crossed_calibration": {
            "physical_cells": len(cells),
            "full_output_rows": 3 ** 8,
            "nonzero_residual_rows": len(residual),
        },
        "one_cell_affine_census": {
            "directions": len(cells),
            "exact_completions": 0,
        },
        "jacobian": {
            "occupied_rows": len(all_rows),
            "nonzero_entries": sum(map(len, derivatives.values())),
            "rank": rank_full,
            "augmented_rank": rank_augmented,
            "nullity": full_nullity,
        },
        "rank_repair": {
            "generous_candidate_cells": len(repair_indices),
            "old_residual_intersections": 0,
            "fresh_tail_histogram": dict(sorted(repair_tail_histogram.items())),
            "nonrepair_variables": len(nonrepair_indices),
            "nonrepair_rank": rank_nonrepair,
            "nonrepair_augmented_rank": rank_nonrepair_augmented,
            "nonrepair_nullity": nonrepair_nullity,
            "homogeneous_tangent_repair_projection_dimension": 0,
        },
        "primitive_separator": {
            "rows": {
                "".join(map(str, word)): str(coefficient)
                for word, coefficient in sorted(SEPARATOR.items())
            },
            "jacobian_pairing": 0,
            "residual_pairing": str(residual_pairing),
        },
        "minimal_order": (
            "no exact one-cell affine completion, no inhomogeneous first-order "
            "correction, and no homogeneous output-preserving tangent can "
            "repair either bad pq endpoint row; any completion must use a "
            "nonlinear simultaneous modification with at least quadratic "
            "interaction, or reselect outside this crossed chart"
        ),
        "scope": (
            "exact first-deformation theorem at the frozen crossed calibration; "
            "the base has ten mixed residuals and is not a GHZ source, so the "
            "rank-246 augmented obstruction is a correction obstruction, not "
            "a tangent-space statement at an exact source"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the first rank-repair ledger changed: {digest}")

    print("h=3 crossed first rank-repair obstruction: PASS")
    print("one-cell affine completions: 0 / 252")
    print("Jacobian 639x252: rank 245; augmented rank 246")
    print("rank-repair cells 36; tangent repair projection dimension 0")
    print("primitive eight-row separator pairs residual to -1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

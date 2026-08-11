#!/usr/bin/env python3
r"""Necessary-and-sufficient typed interface for the rootless C5 gate.

This checker does not assert that the missing physical cells exist.  It
builds the exact multigraded free resolution of

    I=(bd,ad,ac,ce,be),

then localizes on the five-cycle torus and forms the mapping cone of one
primitive anchor face.  The normalized cellular differential is

    top -> five cycle edges -> five lambda vertices,

with one additional anchor column.  The degree-five top maps to the signed
sum of the five repeated-site cubic cells.  A primitive anchor boundary
has aggregate +/-1.  Exactly under that condition the augmented integral
complex is acyclic and all five lambda classes die.

Thus a physical lift of these typed cells with anchor signature
(-1,0,0,0) would close rootless Component III.  The checker specifies and
verifies the interface; it does not construct the lift.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "9a6a4004e34a8a606d5298dddcee378f7b184609df64336244d51f8257f638c7"
PINS = {
    "computations/verify_h3_rootless_five_cycle_first_tor_multidegree_gate.py":
        "a5d9021664b904f895323c29806a825545afd16085c971dc573353bb6c11a81f",
    "computations/verify_h3_rootless_five_cycle_denominator_pp_aggregate_no_go.py":
        "4f691d119469e76436e36566a1ca7307bc49a52f66b0687c1554a9e6531ec4de",
}

VARIABLES = ("a=q12", "b=q23", "c=q34", "d=q45", "e=q15")
SITES = (1, 3, 5, 2, 4)  # cyclic order of h-generators
ZERO_MONOMIAL = (0, 0, 0, 0, 0)
FULL_MONOMIAL = (1, 1, 1, 1, 1)
ZERO = Q(0)

Monomial = tuple[int, int, int, int, int]
Polynomial = Counter[Monomial]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def monomial(*indices: int) -> Monomial:
    result = [0] * 5
    for index in indices:
        result[index] += 1
    return tuple(result)  # type: ignore[return-value]


def m_add(left: Monomial, right: Monomial) -> Monomial:
    return tuple(a + b for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def m_subtract(left: Monomial, right: Monomial) -> Monomial:
    result = tuple(a - b for a, b in zip(left, right, strict=True))
    require(all(value >= 0 for value in result), ("negative monomial", left, right))
    return result  # type: ignore[return-value]


def m_lcm(left: Monomial, right: Monomial) -> Monomial:
    return tuple(max(a, b) for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def p_monomial(value: Monomial, coefficient=1) -> Polynomial:
    coefficient = Q(coefficient)
    return Counter({value: coefficient}) if coefficient else Counter()


def p_add(*values: Polynomial) -> Polynomial:
    answer: Polynomial = Counter()
    for value in values:
        answer.update(value)
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def p_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = Counter()
    for left_term, left_value in left.items():
        for right_term, right_value in right.items():
            answer[m_add(left_term, right_term)] += left_value * right_value
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def zero_matrix(height, width):
    return [[Counter() for _ in range(width)] for _ in range(height)]


def polynomial_matrix_product(left, right):
    require(left and right and len(left[0]) == len(right), "matrix size mismatch")
    answer = zero_matrix(len(left), len(right[0]))
    for row in range(len(left)):
        for column in range(len(right[0])):
            answer[row][column] = p_add(*(
                p_multiply(left[row][middle], right[middle][column])
                for middle in range(len(right))
            ))
    return answer


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left_value - value * right_value
                         for left_value, right_value in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def determinant(rows) -> Q:
    size = len(rows)
    require(size and all(len(row) == size for row in rows), "not square")
    answer = ZERO
    for order in permutations(range(size)):
        inversions = sum(order[i] > order[j] for i in range(size)
                         for j in range(i + 1, size))
        term = Q(-1 if inversions % 2 else 1)
        for row, column in enumerate(order):
            term *= Q(rows[row][column])
        answer += term
    return answer


def dot(left, right) -> Q:
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), ZERO)


def multigraded_resolution():
    generators = (
        monomial(1, 3),  # h1=bd
        monomial(0, 3),  # h3=ad
        monomial(0, 2),  # h5=ac
        monomial(2, 4),  # h2=ce
        monomial(1, 4),  # h4=be
    )
    first_degrees = tuple(
        m_lcm(generators[index], generators[(index + 1) % 5])
        for index in range(5)
    )
    require(all(sum(value) == 3 for value in first_degrees),
            "first Tor stopped being cubic")

    # d0:F0->I, d1:F1->F0, d2:F2->F1.
    d0 = zero_matrix(1, 5)
    d1 = zero_matrix(5, 5)
    d2 = zero_matrix(5, 1)
    records = []
    for index in range(5):
        following = (index + 1) % 5
        target = first_degrees[index]
        left = m_subtract(target, generators[index])
        right = m_subtract(target, generators[following])
        d0[0][index] = p_monomial(generators[index])
        d1[index][index] = p_monomial(left, 1)
        d1[following][index] = p_monomial(right, -1)
        d2[index][0] = p_monomial(m_subtract(FULL_MONOMIAL, target), 1)
        records.append({
            "edge_cell": index,
            "lambda_sites": [SITES[index], SITES[following]],
            "shift_degree": list(target),
            "d1_left": [1, list(left)],
            "d1_right": [-1, list(right)],
            "d2_coefficient": list(m_subtract(FULL_MONOMIAL, target)),
        })

    require(all(not entry for row in polynomial_matrix_product(d0, d1)
                for entry in row), "d0*d1 is nonzero")
    require(all(not entry for row in polynomial_matrix_product(d1, d2)
                for entry in row), "d1*d2 is nonzero")

    # Every entry is homogeneous with the declared shifts.
    for column, target in enumerate(first_degrees):
        for row, generator_degree in enumerate(generators):
            for coefficient in d1[row][column]:
                require(m_add(coefficient, generator_degree) == target,
                        ("d1 lost fine homogeneity", row, column))
        for coefficient in d2[column][0]:
            require(m_add(coefficient, target) == FULL_MONOMIAL,
                    ("d2 lost fine homogeneity", column))

    return generators, first_degrees, d0, d1, d2, {
        "F0_shifts": [list(value) for value in generators],
        "F1_shifts": [list(value) for value in first_degrees],
        "F2_shift": list(FULL_MONOMIAL),
        "differential_records": records,
        "d0_d1": 0,
        "d1_d2": 0,
        "sign_convention": "s_i=left_i*e_i-right_i*e_(i+1); d2(top)=sum_i complement_i*s_i",
    }


def normalized_cellular_interface(generators):
    # After inverting a,b,c,d,e, set vertex_i=e_i/g_i,
    # edge_i=s_i/lcm_i, and top=F/(abcde).  The free resolution becomes the
    # ordinary augmented cellular chain of an oriented pentagon.
    edge_columns = []
    for index in range(5):
        column = [0] * 5
        column[index] = 1
        column[(index + 1) % 5] = -1
        edge_columns.append(column)
    top_column = [1, 1, 1, 1, 1]
    augmentation = [1, 1, 1, 1, 1]
    require(rank(edge_columns) == 4, "pentagon boundary rank changed")
    require(all(dot(augmentation, column) == 0 for column in edge_columns),
            "cellular augmentation stopped killing edges")
    require([sum(column[index] for column in edge_columns)
             for index in range(5)] == [0] * 5,
            "top boundary stopped being a cycle")

    # Add one physical relative cell A with primitive boundary p=e_0.
    # Its typed readout is the desired (-1,0,0,0); the five Tor cells and
    # their top relation have zero readouts.
    primitive_anchor_boundary = [1, 0, 0, 0, 0]
    augmented_columns = edge_columns + [primitive_anchor_boundary]
    top_in_augmented_C1 = top_column + [0]
    require(rank(augmented_columns) == 5,
            "primitive anchor failed to kill all five lambda vertices")
    require([sum(column[row] * top_in_augmented_C1[column_index]
                         for column_index, column in enumerate(augmented_columns))
             for row in range(5)] == [0] * 5,
            "augmented differential does not square")
    require(len(augmented_columns) - rank(augmented_columns) == 1,
            "augmented C1 kernel changed")

    # Integral necessity/sufficiency.  Four edge columns form a spanning
    # tree.  Appending a general p has determinant +/-sum(p_i), so the
    # cokernel vanishes integrally exactly when the aggregate is primitive.
    tree = edge_columns[:4]
    determinant_coefficients = []
    for row in range(5):
        basis = [0] * 5
        basis[row] = 1
        square_columns = tree + [basis]
        square_rows = [[column[row_index] for column in square_columns]
                       for row_index in range(5)]
        determinant_coefficients.append(int(determinant(square_rows)))
    require(len(set(determinant_coefficients)) == 1
            and abs(determinant_coefficients[0]) == 1,
            ("tree determinant is not aggregate", determinant_coefficients))
    for candidate in (
        [1, 0, 0, 0, 0],
        [0, -1, 0, 0, 0],
        [2, -1, 0, 0, 0],
        [1, 1, -1, 0, 0],
        [2, 0, 0, 0, 0],
        [1, -1, 0, 0, 0],
    ):
        square_columns = tree + [candidate]
        square_rows = [[column[row_index] for column in square_columns]
                       for row_index in range(5)]
        require(determinant(square_rows)
                == determinant_coefficients[0] * sum(candidate),
                ("anchor determinant is not its aggregate", candidate))

    # The unaugmented cellular complex is exact after the final augmentation
    # to the Laurent unit.  The mapping cone of a primitive anchor is exact
    # in lambda degrees: H1=H0=0.  All matrices use integral unit signs.
    readouts = {
        "five_repeated_site_cells": [0, 0, 0, 0],
        "degree_five_compatibility": [0, 0, 0, 0],
        "primitive_anchor_face": [-1, 0, 0, 0],
    }
    require(readouts["primitive_anchor_face"] == [-1, 0, 0, 0],
            "anchor signature changed")

    return {
        "localized_basis_change": {
            "vertex_i": "e_i/h_i",
            "edge_i": "s_i/lcm(h_i,h_(i+1))",
            "top": "top/(abcde)",
        },
        "cellular_d1_columns": edge_columns,
        "cellular_d2_column": top_column,
        "cellular_augmentation": augmentation,
        "unaugmented_ranks": {"d2": 1, "d1": 4, "augmentation": 1},
        "anchor_boundary": primitive_anchor_boundary,
        "anchor_aggregate": sum(primitive_anchor_boundary),
        "augmented_d1_rank": rank(augmented_columns),
        "augmented_kernel_rank": len(augmented_columns) - rank(augmented_columns),
        "d_squared": 0,
        "tree_determinant_coefficients": determinant_coefficients,
        "integral_criterion": "anchor boundary p is sufficient iff sum_i p_i=+/-1",
        "readouts_ainc_w_tgt_ores": readouts,
        "lambda_homology_after_anchor": 0,
        "component_III_terminal_after_pushout": 0,
    }


def polynomial_anchor_scope(generators, d1, d2):
    # Before cycle-cell localization, the anchor column e0 maps under d0 to
    # h1=bd, not to 1.  Adding it gives coker I/(bd), so it is not a global
    # source unit.  On the cycle torus bd is a unit and the normalized
    # cellular conclusion is valid.  This is the exact scope guard.
    anchor_image = generators[0]
    require(anchor_image == monomial(1, 3), "anchor image stopped being bd")
    augmented_d1 = [row + [p_monomial(ZERO_MONOMIAL, int(index == 0))]
                    for index, row in enumerate(d1)]
    augmented_d2 = [row[:] for row in d2] + [[Counter()]]
    require(all(not entry for row in polynomial_matrix_product(
        augmented_d1, augmented_d2
    ) for entry in row), "polynomial anchor mapping cone does not square")
    # The old first differential is rank four at the all-one torus point.
    evaluated_columns = []
    for column in range(5):
        vector = []
        for row in range(5):
            vector.append(sum(d1[row][column].values(), ZERO))
        evaluated_columns.append(vector)
    require(rank(evaluated_columns) == 4,
            "multigraded d1 lost torus rank four")
    evaluated_anchor = [1, 0, 0, 0, 0]
    require(rank(evaluated_columns + [evaluated_anchor]) == 5,
            "physical unit anchor failed at the diagonal torus point")
    return {
        "polynomial_anchor_image": "h1=bd",
        "polynomial_cokernel_before_localization": "I/(bd)",
        "required_open": "a*b*c*d*e != 0",
        "mapping_cone_d_squared": 0,
        "diagonal_rank_before_after_anchor": [4, 5],
        "global_claim": False,
    }


def main() -> None:
    pin_dependencies()
    generators, first_degrees, _d0, d1, d2, resolution = (
        multigraded_resolution()
    )
    interface = normalized_cellular_interface(generators)
    scope = polynomial_anchor_scope(generators, d1, d2)
    ledger = {
        "pins": PINS,
        "cycle_variables": list(VARIABLES),
        "lambda_site_order": list(SITES),
        "free_resolution": resolution,
        "typed_positive_interface": interface,
        "scope": scope,
        "necessary_and_sufficient_statement": (
            "on the five-cycle torus, five source-valid cubic cells with the "
            "displayed d1, one source-valid degree-five compatibility with "
            "the displayed d2, and one physical anchor cell whose boundary "
            "has aggregate +/-1 and signature (-1,0,0,0) are exactly the "
            "minimal typed data that make the lambda mapping cone acyclic"
        ),
        "existence_status": (
            "not constructed; 466bfd6 and dae10d3 prove the committed "
            "cofactor/denominator/PP inventory does not contain these data"
        ),
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED", ("pin ledger digest", digest))
    require(digest == EXPECTED_LEDGER_SHA256, ("ledger digest changed", digest))
    print("h=3 rootless five-cycle positive interface: PASS")
    print("multigraded resolution: d0*d1=d1*d2=0")
    print("localized cellular ranks: 1 -> 5 -> 5 -> 1 exact")
    print("one primitive anchor column raises lambda rank 4 -> 5")
    print("target/ores-zero physical lift would close Component III")
    print("existence: NOT CONSTRUCTED")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()

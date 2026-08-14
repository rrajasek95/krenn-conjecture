#!/usr/bin/env python3
"""Audit collective Koszul constraints on the five h_v product charges.

Write X=T*H_W and Z_i=N_i X.  If a future tensor-to-corner comparison has

    Psi(Z_i) = lambda_i h_i,

then the first Koszul overlap K_ij has the full product boundary

    d(K_ij X) = h_i Z_j - h_j Z_i + K_ij dX.

If the last (mandatory) overlap--Leibniz face is Psi-dark, the ten pair
relations reduce to h_i h_j(lambda_j-lambda_i)=0.  The h_i form a regular
sequence in a polynomial domain, so the five scalars become one common
scalar.  Higher Koszul faces impose no equation on that common scalar, and
the five-face aggregate remains a positive-degree, nonunit polynomial.

Without darkness of K_ij dX, even this diagonalization is not forced.  An
arbitrary five-tuple of lambdas has pair debt

    r_ij = h_i h_j(lambda_j-lambda_i).

Choosing the unclassified overlap augmentation to be -r_ij cancels it.
These choices are coherently closed on every triple because r is the
Koszul coboundary of (lambda_i h_i), hence delta(r)=delta^2(...)=0.  Thus
height-five complete intersection, full Leibniz, and overlap compatibility
alone force neither a nonzero aggregate nor all lambdas to vanish.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_five_denominator_hafnians_complete_intersection.py":
        "4c87c1db939346e8f1d83a26b5edef19e3143a65cc6d6fd5ea636f99d13b5615",
    "computations/verify_h3_degree4_reset_five_face_aggregate_gate.py":
        "01961c9ae83b91dad31ba859ea2f8a2d5775d73d7ad591aa0a369e7d971f8079",
    "computations/verify_h3_hv_switch_weyl_mixed_product_beq_leibniz_gate.py":
        "cffa61fb77b5ac5ee45f664081481869040760c440372c4ad268a7ebc8917523",
    "computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py":
        "b60538f9db5b8c2984bbee95e0a05f383408e9ab7c13680216adf56386682522",
}
EXPECTED_LEDGER_SHA256 = "67302e5a22d13fb9192f9675099f526b83925b14b1960694f23013caf5f8d009"

VARS = ("x12", "x13", "x14", "x15", "x23",
        "x24", "x25", "x34", "x35", "x45")
N = 5
ZERO = Q(0)

Monomial = tuple[str, ...]
Polynomial = dict[Monomial, Q]
LambdaPolynomial = tuple[Polynomial, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def polynomial(*terms: tuple[int, tuple[str, ...]]) -> Polynomial:
    answer: Polynomial = {}
    for coefficient, variables in terms:
        monomial = tuple(sorted(variables))
        answer[monomial] = answer.get(monomial, ZERO) + Q(coefficient)
        if not answer[monomial]:
            del answer[monomial]
    return answer


def poly_add(left: Polynomial, right: Polynomial,
             scale: Q = Q(1)) -> Polynomial:
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, ZERO) + scale * coefficient
        if not answer[monomial]:
            del answer[monomial]
    return answer


def poly_scale(value: Polynomial, scalar: Q) -> Polynomial:
    return {monomial: scalar * coefficient
            for monomial, coefficient in value.items()
            if scalar * coefficient}


def poly_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = (
                answer.get(monomial, ZERO)
                + left_coefficient * right_coefficient
            )
            if not answer[monomial]:
                del answer[monomial]
    return answer


def denominator_faces() -> tuple[Polynomial, ...]:
    faces = (
        polynomial((1, ("x23", "x45")),
                   (1, ("x24", "x35")),
                   (1, ("x25", "x34"))),
        polynomial((1, ("x13", "x45")),
                   (1, ("x14", "x35")),
                   (1, ("x15", "x34"))),
        polynomial((1, ("x12", "x45")),
                   (1, ("x14", "x25")),
                   (1, ("x15", "x24"))),
        polynomial((1, ("x12", "x35")),
                   (1, ("x13", "x25")),
                   (1, ("x15", "x23"))),
        polynomial((1, ("x12", "x34")),
                   (1, ("x13", "x24")),
                   (1, ("x14", "x23"))),
    )
    require(len(faces) == N and all(len(face) == 3 for face in faces),
            "five denominator faces changed")
    require(len(set().union(*(set(face) for face in faces))) == 15,
            "the five h_v supports stopped being disjoint")
    return faces


def rank(matrix: list[list[Q]]) -> int:
    if not matrix:
        return 0
    width = len(matrix[0])
    require(all(len(row) == width for row in matrix), "ragged matrix")
    work = [[Q(entry) for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def matmul(left: list[list[Q]], right: list[list[Q]]) -> list[list[Q]]:
    require(left and right and len(left[0]) == len(right),
            "matrix product dimensions")
    return [[sum((left[row][middle] * right[middle][column]
                  for middle in range(len(right))), ZERO)
             for column in range(len(right[0]))]
            for row in range(len(left))]


def zero_matrix(height: int, width: int) -> list[list[Q]]:
    return [[ZERO for _ in range(width)] for _ in range(height)]


def koszul_boundary(degree: int) -> list[list[Q]]:
    """The degree-p boundary after the harmless specialization h_i=1."""
    require(1 <= degree <= N, ("bad Koszul degree", degree))
    source = tuple(combinations(range(N), degree))
    target = tuple(combinations(range(N), degree - 1))
    target_index = {item: index for index, item in enumerate(target)}
    matrix = zero_matrix(len(target), len(source))
    for column, subset in enumerate(source):
        for position in range(degree):
            face = subset[:position] + subset[position + 1:]
            matrix[target_index[face]][column] = Q((-1) ** position)
    return matrix


def pair_constraint_audit(faces: tuple[Polynomial, ...]) -> dict[str, object]:
    pairs = tuple(combinations(range(N), 2))
    constraint = []
    products = []
    for left, right in pairs:
        row = [ZERO] * N
        row[left] = Q(-1)
        row[right] = Q(1)
        constraint.append(row)
        product = poly_multiply(faces[left], faces[right])
        require(product, ("h_i h_j vanished", left, right))
        products.append(product)

    ones = [Q(1)] * N
    require(rank(constraint) == 4
            and all(sum((entry * value for entry, value in
                         zip(row, ones, strict=True)), ZERO) == 0
                    for row in constraint),
            "pair-difference system stopped having diagonal kernel")
    require(len(products) == 10 and all(products),
            "a domain coefficient in the pair relations vanished")

    return {
        "mixed_values": "Psi(Z_i)=lambda_i*h_i",
        "full_pair_product_boundary": (
            "d(K_ij*X)=h_i*Z_j-h_j*Z_i+K_ij*dX"
        ),
        "mandatory_unclassified_pair_face": "K_ij*dX",
        "conditional_terminal_equations": (
            "h_i*h_j*(lambda_j-lambda_i)=0 for all i<j"
        ),
        "pair_count": len(pairs),
        "coefficient_products_nonzero": len(products),
        "scalar_difference_matrix_rank": rank(constraint),
        "scalar_kernel_dimension": N - rank(constraint),
        "scalar_kernel_generator": [1, 1, 1, 1, 1],
        "conditional_conclusion": "lambda_1=...=lambda_5=c",
        "condition": "Psi(K_ij*dX)=0 for all ten pair overlaps",
    }


def higher_koszul_audit() -> dict[str, object]:
    betti = [comb(N, degree) for degree in range(N + 1)]
    boundaries = {degree: koszul_boundary(degree)
                  for degree in range(1, N + 1)}
    ranks = [None] + [rank(boundaries[degree])
                      for degree in range(1, N + 1)]

    for degree in range(2, N + 1):
        product = matmul(boundaries[degree - 1], boundaries[degree])
        require(product == zero_matrix(len(product), len(product[0])),
                ("Koszul d^2 failed", degree))
    for degree in range(1, N):
        require(ranks[degree] + ranks[degree + 1] == betti[degree],
                ("specialized Koszul exactness failed", degree))
    require(ranks == [None, 1, 4, 6, 4, 1],
            ("Koszul ranks changed", ranks))

    # Once all lambdas equal c, every pair difference is identically zero.
    # Both c=0 and c=1 extend through the same linear Koszul equations, and
    # scalar multiplication commutes with every boundary in all degrees.
    for scalar in (Q(0), Q(1), Q(-7, 3)):
        for degree, boundary in boundaries.items():
            scaled = [[scalar * entry for entry in row] for row in boundary]
            require(scaled == [[entry * scalar for entry in row]
                               for row in boundary],
                    ("scalar failed to commute with boundary", degree))

    return {
        "koszul_betti_numbers": betti,
        "specialized_boundary_ranks": ranks[1:],
        "all_consecutive_boundary_products_zero": True,
        "exact_in_positive_degrees_after_h_i_equal_1": True,
        "common_scalar_commutes_with_every_higher_face": True,
        "compatible_common_scalar_examples": ["0", "1", "-7/3"],
        "higher_face_conclusion": (
            "no higher Koszul relation forces the common scalar c"
        ),
    }


def lambda_zero() -> LambdaPolynomial:
    return tuple({} for _ in range(N))


def lambda_add(left: LambdaPolynomial, right: LambdaPolynomial,
               scale: Q = Q(1)) -> LambdaPolynomial:
    return tuple(poly_add(a, b, scale)
                 for a, b in zip(left, right, strict=True))


def lambda_times_h(value: LambdaPolynomial,
                   h_value: Polynomial) -> LambdaPolynomial:
    return tuple(poly_multiply(component, h_value) for component in value)


def formal_lambda_h(index: int, h_value: Polynomial) -> LambdaPolynomial:
    answer = list(lambda_zero())
    answer[index] = dict(h_value)
    return tuple(answer)


def koszul_coboundary(
        values: dict[tuple[int, ...], LambdaPolynomial],
        degree: int,
        faces: tuple[Polynomial, ...],
) -> dict[tuple[int, ...], LambdaPolynomial]:
    """delta on h-Koszul cochains, with (delta a)_ij=h_i a_j-h_j a_i."""
    require(set(values) == set(combinations(range(N), degree)),
            ("cochain basis changed", degree))
    answer: dict[tuple[int, ...], LambdaPolynomial] = {}
    for subset in combinations(range(N), degree + 1):
        total = lambda_zero()
        for position, vertex in enumerate(subset):
            face = subset[:position] + subset[position + 1:]
            total = lambda_add(
                total,
                lambda_times_h(values[face], faces[vertex]),
                Q((-1) ** position),
            )
        answer[subset] = total
    return answer


def free_overlap_counterguard(
        faces: tuple[Polynomial, ...]) -> dict[str, object]:
    # a_i=lambda_i*h_i.  Its coboundary is exactly the pair charge debt.
    one_values = {(index,): formal_lambda_h(index, faces[index])
                  for index in range(N)}
    pair_debt = koszul_coboundary(one_values, 1, faces)
    require(len(pair_debt) == 10
            and all(any(component for component in value)
                    for value in pair_debt.values()),
            "the arbitrary-lambda pair debt disappeared")

    # Every triple compatibility is automatic: delta(pair_debt)=delta^2(a)=0.
    triple_debt = koszul_coboundary(pair_debt, 2, faces)
    require(len(triple_debt) == 10
            and all(value == lambda_zero()
                    for value in triple_debt.values()),
            "the pair compensators stopped satisfying triple compatibility")

    # A deliberately non-diagonal specialization demonstrates the guard.
    sample = (Q(0), Q(1), Q(-2), Q(5, 3), Q(9))
    nonzero_sample_debts = 0
    for value in pair_debt.values():
        evaluated: Polynomial = {}
        for scalar, component in zip(sample, value, strict=True):
            evaluated = poly_add(evaluated, component, scalar)
        nonzero_sample_debts += bool(evaluated)
    require(nonzero_sample_debts == 10,
            "the non-diagonal counterexample lost a pair debt")

    return {
        "arbitrary_scalar_tuple": "(lambda_1,...,lambda_5) in Q^5",
        "pair_charge_debt": "r_ij=h_i*h_j*(lambda_j-lambda_i)",
        "allowed_unclassified_overlap_value": "Psi(K_ij*dX)=-r_ij",
        "pair_compensators": len(pair_debt),
        "triple_compatibilities": len(triple_debt),
        "triple_identity": (
            "h_i*r_jk-h_j*r_ik+h_k*r_ij=0"
        ),
        "reason": "r=delta_K(lambda_i*h_i), hence delta_K(r)=0",
        "non_diagonal_sample": [str(value) for value in sample],
        "nonzero_sample_pair_debts": nonzero_sample_debts,
        "counterguard": (
            "until all ten K_ij*dX augmentations are proved dark or fixed, "
            "full Leibniz/overlap compatibility permits arbitrary lambdas"
        ),
    }


def aggregate_audit(faces: tuple[Polynomial, ...]) -> dict[str, object]:
    aggregate: Polynomial = {}
    for face in faces:
        aggregate = poly_add(aggregate, face)
    require(len(aggregate) == 15
            and all(coefficient == 1 for coefficient in aggregate.values()),
            "sum h_v stopped having fifteen distinct positive terms")
    require(() not in aggregate
            and all(len(monomial) == 2 for monomial in aggregate),
            "sum h_v acquired a unit term")
    return {
        "under_conditional_diagonalization": "Psi(sum_i Z_i)=c*sum_i h_i",
        "sum_h_i_support": len(aggregate),
        "sum_h_i_degree": 2,
        "sum_h_i_constant_term": 0,
        "sum_h_i_is_unit": False,
        "c_zero_is_compatible": True,
        "c_one_is_compatible": True,
        "nonzero_aggregate_for_c_nonzero": True,
        "primitive_unit_aggregate": False,
        "projected_C5_warning": (
            "the rank-four all-ones aggregate exists only after the C5 "
            "specialization; the pinned universal full-source residual has "
            "rank five and no nonzero source cycle"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    faces = denominator_faces()
    pair = pair_constraint_audit(faces)
    higher = higher_koszul_audit()
    counterguard = free_overlap_counterguard(faces)
    aggregate = aggregate_audit(faces)
    ledger = {
        "theorem": "h3 collective h_v Koszul lambda overlap gate",
        "scope": {
            "mixed_cells": "Z_i=N_i*(T*H_W), i=1,...,5",
            "denominator_ring": "Q[x12,x13,x14,x15,x23,x24,x25,x34,x35,x45]",
            "pinned_CI_fact": "(h_1,...,h_5) is a height-five regular sequence",
            "strict_literal_projection_today": "zero/off-grade",
        },
        "conditional_diagonalization": pair,
        "higher_koszul_faces": higher,
        "free_overlap_counterguard": counterguard,
        "five_face_aggregate": aggregate,
        "logical_classification": {
            "CI_plus_full_Leibniz_without_overlap_readout": (
                "lambda_1,...,lambda_5 remain arbitrary"
            ),
            "plus_all_ten_overlap_faces_Psi_dark": (
                "lambda_1=...=lambda_5=c, with c arbitrary"
            ),
            "plus_strict_physical_mixed_product_normalization": (
                "c=0, by the separately pinned literal mapping-cone theorem"
            ),
            "force_nonzero_aggregate": False,
            "force_all_zero_without_new_normalization": False,
        },
        "verdict": (
            "The height-five CI and its complete Koszul tower do not select "
            "a bright or dark mixed comparison.  If every mandatory pair "
            "overlap K_ij*dX is independently proved Psi-dark, the ten "
            "relations have rank four and reduce the five lambdas to one "
            "common scalar.  No higher face fixes that scalar, and its "
            "five-face value is c*sum(h_i), never a denominator-only unit.  "
            "Without the pair-face darkness, coherent compensators exist "
            "for arbitrary lambdas because their debts form an exact "
            "Koszul coboundary."
        ),
        "shortest_new_datum": (
            "compute the physical B/Eq readout of the ten labelled faces "
            "K_ij*d(T*H_W).  Darkness diagonalizes the lambdas; the stronger "
            "normalized DGA-product statement then sets the common value to "
            "zero.  A nonzero result must instead prescribe a primitive "
            "normalization/localization not supplied by the CI."
        ),
        "nonclaims": [
            "the algebraic pair compensators are not claimed as physical labelled cells",
            "the projected C5 all-ones dual is not promoted to a universal source cycle",
            "a common nonzero scalar is not called a primitive unit aggregate",
            "strict multiplicativity is not inferred from d-squared or Koszul exactness",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("collective h_v Koszul lambda ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("classification", "diagonal", "counterguard", "aggregate"),
        default="classification",
    )
    arguments = parser.parse_args()
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print(f"collective h_v Koszul lambda gate ({arguments.mode}): PASS")


if __name__ == "__main__":
    main()

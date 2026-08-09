#!/usr/bin/env python3
"""Exact closure of the exceptional blocked-row D1 residue support."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys
from fractions import Fraction
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_CANDIDATE_SHA256 = (
    "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_334_branch63_candidate.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_CANDIDATE_SHA256,
            "the pinned D1 candidate source changed")
C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
D = C.D

EXPECTED_LEDGER_SHA256 = (
    "12228ed0ac3a408d83927bda4c49ea9634491ccca808eff120f064e1eb5ff6c2"
)


def variable(name):
    return D.p_var(name)


def vector_add(left, right):
    return tuple(D.p_add(a, b) for a, b in zip(left, right))


def scalar_vector(scalar, vector):
    return tuple(D.p_mul(scalar, entry) for entry in vector)


def outer(left, right):
    return tuple(tuple(D.p_mul(a, b) for b in right) for a in left)


def matrix_add(left, right):
    return tuple(tuple(D.p_add(a, b) for a, b in zip(left_row, right_row))
                 for left_row, right_row in zip(left, right))


def scalar_matrix(scalar, matrix):
    return tuple(tuple(D.p_mul(scalar, entry) for entry in row)
                 for row in matrix)


def zero_matrix():
    return tuple(tuple(D.p_const(0) for _ in range(3)) for _ in range(3))


def matrix_equal(left, right):
    return all(a == b for left_row, right_row in zip(left, right)
               for a, b in zip(left_row, right_row))


def matrix_hash(matrix):
    return D.content_hash([
        [[[list(monomial), str(coefficient)]
          for monomial, coefficient in sorted(entry.items())]
         for entry in row]
        for row in matrix
    ])


def determinant(matrix):
    """Exact determinant over the rationals."""
    matrix = [[Fraction(entry) for entry in row] for row in matrix]
    size = len(matrix)
    value = Fraction(1)
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if matrix[row][column]), None)
        require(pivot is not None, "a selected rank minor became singular")
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            value = -value
        pivot_value = matrix[column][column]
        value *= pivot_value
        matrix[column] = [entry / pivot_value for entry in matrix[column]]
        for row in range(column + 1, size):
            scale = matrix[row][column]
            if scale:
                matrix[row] = [a - scale * b
                               for a, b in zip(matrix[row], matrix[column])]
    return value


def rank_certificate(columns, row_count):
    """Exact rank plus a unimodular minor, valid in every characteristic."""
    rows = [[Fraction(column.get(row, 0)) for column in columns]
            for row in range(row_count)]
    row_labels = list(range(row_count))
    rank = 0
    pivot_rows, pivot_columns = [], []
    for column in range(len(columns)):
        pivot = next((row for row in range(rank, row_count)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        row_labels[rank], row_labels[pivot] = row_labels[pivot], row_labels[rank]
        pivot_rows.append(row_labels[rank])
        pivot_columns.append(column)
        scale = rows[rank][column]
        rows[rank] = [entry / scale for entry in rows[rank]]
        for row in range(row_count):
            if row == rank or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [a - scale * b
                         for a, b in zip(rows[row], rows[rank])]
        rank += 1
    minor = [[columns[column].get(row, 0) for column in pivot_columns]
             for row in pivot_rows]
    minor_determinant = determinant(minor)
    require(abs(minor_determinant) == 1,
            "the rank certificate minor is not unimodular")
    return rank, pivot_rows, pivot_columns, int(minor_determinant)


def koszul_module_audit():
    """Prove completeness of the three-line first-syzygy normal form."""
    # Normalize the three nonzero lines to coordinate 0 in U,V,W.  The
    # relation map sends (F,E,D) to e0*F + E*e0 + D*e0.
    relation_columns = []
    domain_names = []
    for block in ("F", "E", "D"):
        for first, second in itertools.product(range(3), repeat=2):
            if block == "F":
                output = (0, first, second)
            elif block == "E":
                output = (first, 0, second)
            else:
                output = (first, second, 0)
            relation_columns.append({output[0] * 9 + output[1] * 3
                                     + output[2]: 1})
            domain_names.append((block, first, second))
    (relation_rank, relation_pivot_rows, relation_pivot_columns,
     relation_minor_det) = rank_certificate(relation_columns, 27)
    require(relation_rank == 19 and 27 - relation_rank == 8,
            "the three-line relation kernel dimension changed")

    # Universal pairwise-intersection parametrization:
    # F=-v*t+p*e, E=u*t+x*e, D=-u*p-x*v.
    domain_index = {name: index for index, name in enumerate(domain_names)}
    parameter_columns = []
    for family, coordinate in itertools.product(("t", "p", "x"), range(3)):
        column = {}

        def add(name, value):
            index = domain_index[name]
            column[index] = column.get(index, 0) + value

        if family == "t":
            add(("F", 0, coordinate), -1)
            add(("E", 0, coordinate), 1)
        elif family == "p":
            add(("F", coordinate, 0), 1)
            add(("D", 0, coordinate), -1)
        else:
            add(("E", coordinate, 0), 1)
            add(("D", coordinate, 0), -1)
        parameter_columns.append({key: value for key, value in column.items()
                                  if value})
    (parameter_rank, parameter_pivot_rows, parameter_pivot_columns,
     parameter_minor_det) = rank_certificate(parameter_columns, 27)
    require(parameter_rank == 8,
            "the pairwise-intersection generators changed rank")

    # Every parameter column lies in the relation kernel.  Equal dimensions
    # then prove that these generators exhaust every three-line relation.
    for parameter in parameter_columns:
        image = {}
        for domain_column, coefficient in parameter.items():
            for row, value in relation_columns[domain_column].items():
                image[row] = image.get(row, 0) + coefficient * value
        require(not {row: value for row, value in image.items() if value},
                "a Koszul parameter failed the three-line relation")
    return {
        "relation_domain_dimension": 27,
        "relation_rank": relation_rank,
        "relation_kernel_dimension": 27 - relation_rank,
        "relation_unimodular_minor": {
            "rows": relation_pivot_rows,
            "columns": relation_pivot_columns,
            "determinant": relation_minor_det,
        },
        "pairwise_parameter_dimension": 9,
        "pairwise_parameter_rank": parameter_rank,
        "parameter_unimodular_minor": {
            "rows": parameter_pivot_rows,
            "columns": parameter_pivot_columns,
            "determinant": parameter_minor_det,
        },
        "triple_overlap_gauge_dimension": 1,
        "normal_form": (
            "F=-v*t+p*e, E=u*t+x*e, D=-u*p-x*v"
        ),
    }


def exceptional_support_audit():
    """Reconstruct the maximal representative with the sharp residue rows."""
    _state, _extras, base_support, admissible, _stats = C.candidate_input()
    holes = set()
    # Row 1 is blocked at residue vertex 4 on all three incident edges.
    for edge in ((4, 5), (4, 6), (4, 7)):
        holes.update((*edge, 1, color) for color in C.V.COLORS)
    # The other non-target row of A47 is the target line gamma*e2.
    holes.update({(4, 7, 0, 0), (4, 7, 0, 1)})
    # D56 has support {02,12,20,21,22}.
    holes.update({(5, 6, 0, 0), (5, 6, 0, 1),
                  (5, 6, 1, 0), (5, 6, 1, 1)})
    support = set(admissible) - holes
    require(len(holes) == 15 and len(support) == 202
            and base_support <= support,
            "the exceptional blocked-row support changed")

    expected = {
        (4, 5): set(itertools.product((0, 2), C.V.COLORS)),
        (4, 6): set(itertools.product((0, 2), C.V.COLORS)),
        (4, 7): {(0, 2), (2, 0), (2, 1), (2, 2)},
        (5, 6): {(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)},
        (5, 7): set(itertools.product(C.V.COLORS, repeat=2)),
        (6, 7): set(itertools.product(C.V.COLORS, repeat=2)),
    }
    for edge, expected_cells in expected.items():
        actual = {(i, j) for i, j in itertools.product(C.V.COLORS, repeat=2)
                  if C.V.cell(*edge, i, j) in support}
        require(actual == expected_cells,
                "residue support changed on edge %s" % (edge,))
    shadow = C.support_shadow_audit(support)
    return {
        "localized_cells": len(support),
        "holes": [list(cell) for cell in sorted(holes)],
        "complete_fibres_checked": shadow["fibres_checked"],
        "live_matching_histogram": shadow["live_matching_histogram"],
    }


def symbolic_audit():
    """Replay the quotient filtration after normalizing row0(A47)=e2."""
    u = tuple(variable("u%d" % i) for i in range(3))
    v = tuple(variable("v%d" % i) for i in range(3))
    e = (D.p_const(0), D.p_const(0), D.p_const(1))
    t0, t1, lam = (variable(name) for name in ("t0", "t1", "lambda"))
    r, q = variable("r"), variable("q")
    h, s, c2 = (variable(name) for name in ("h", "s", "c2"))

    # The row-0 zero relation has, after the two quotient slices and the
    # upper-left 2-by-2 cancellation in D56, this exact normal form.
    t = (t0, t1, lam)
    E = matrix_add(outer(u, t), scalar_matrix(D.p_neg(q), outer(e, e)))
    F = matrix_add(scalar_matrix(D.p_const(-1), outer(v, t)),
                   scalar_matrix(D.p_neg(r), outer(e, e)))
    residue_D = matrix_add(scalar_matrix(r, outer(u, e)),
                           scalar_matrix(q, outer(e, v)))
    row0_slices = []
    for ell in range(3):
        value = matrix_add(outer(u, tuple(F[k][ell] for k in range(3))),
                           outer(tuple(E[j][ell] for j in range(3)), v))
        if ell == 2:
            value = matrix_add(value, residue_D)
        require(matrix_equal(value, zero_matrix()),
                "the row-0 normal form failed at colour %d" % ell)
        row0_slices.append(matrix_hash(value))

    # The two non-target pure-row slices make c_l=h*t_l and force the
    # displayed common rank-one factorization.
    a = vector_add(scalar_vector(s, u), scalar_vector(D.p_mul(h, q), e))
    b = vector_add(scalar_vector(s, v),
                   scalar_vector(D.p_neg(D.p_mul(h, r)), e))
    c = (D.p_mul(h, t0), D.p_mul(h, t1), c2)

    pure_slices = []
    for ell in range(3):
        value = matrix_add(
            outer(a, tuple(F[k][ell] for k in range(3))),
            matrix_add(
                outer(tuple(E[j][ell] for j in range(3)), b),
                scalar_matrix(c[ell], residue_D),
            ),
        )
        if ell < 2:
            require(matrix_equal(value, zero_matrix()),
                    "a non-target pure-row slice did not vanish")
        else:
            collapse_scalar = D.p_sub(D.p_sub(c2, D.p_mul(lam, h)), s)
            expected = scalar_matrix(collapse_scalar, residue_D)
            require(matrix_equal(value, expected),
                    "the target pure-row slice did not collapse to D56")
        pure_slices.append(matrix_hash(value))

    return {
        "row0_zero_slice_sha256": row0_slices,
        "pure_row_slice_sha256": pure_slices,
        "D56_normal_form_sha256": matrix_hash(residue_D),
        "target_collapse": "P22=(c2-lambda*h-s)*D56",
    }


def audit():
    started = monotonic()
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "three_line_koszul_module": koszul_module_audit(),
        "support": exceptional_support_audit(),
        "symbolic": symbolic_audit(),
        "quotient_lemmas": [
            "x*y^T+z*w^T=0 with nonzero factors makes the two left and "
            "two right factors pairwise proportional",
            "a vector supported only at target colour 2 is a scalar "
            "multiple of e2",
            "equality of two nonzero rank-one matrices synchronizes both "
            "factor lines",
        ],
        "normalization": (
            "the nonzero row0(A47)=gamma*e2 is normalized to e2 by the "
            "edge gauge A47 -> A47/gamma, D56 -> gamma*D56"
        ),
        "final_contradiction": (
            "E22=K*D56, while D56 has nonzero entries 02,12,20,21 and "
            "22: K=0 misses E22 and K!=0 has off-target support"
        ),
        "characteristic_scope": "empty over every field",
        "extension_scope": (
            "only the displayed six residue-edge row supports and their "
            "nonvanishing are used; cells outside the residue K4 are free"
        ),
        "status": "the exceptional blocked-row D1 residue support is empty",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the blocked-row exception ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 residue blocked-row exception: PASS (exact)")
    print("localized support:", ledger["support"]["localized_cells"])
    print("target collapse:", ledger["symbolic"]["target_collapse"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()

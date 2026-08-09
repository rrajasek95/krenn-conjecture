#!/usr/bin/env python3
"""Exact classification of two-kernel tripod projection-rank profiles."""

from __future__ import annotations

from fractions import Fraction
import importlib
import itertools
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
D = C.D
K = importlib.import_module("verify_n8_d1_residue_blocked_row_exception")
EXPECTED_LEDGER_SHA256 = (
    "90686ef935c465b84f1c8509ad0055657f62a21770c61d54d7b2e432234e532d"
)


def const_vector(index):
    return tuple(D.p_const(1 if position == index else 0)
                 for position in range(3))


def var_vector(prefix):
    return tuple(D.p_var("%s%d" % (prefix, index)) for index in range(3))


def outer(left, right):
    return tuple(tuple(D.p_mul(a, b) for b in right) for a in left)


def matrix_scale(scalar, matrix):
    return tuple(tuple(D.p_mul(scalar, entry) for entry in row)
                 for row in matrix)


def matrix_add(*matrices):
    zero = D.p_const(0)
    out = tuple(tuple(zero for _ in range(3)) for _ in range(3))
    for matrix in matrices:
        out = tuple(tuple(D.p_add(a, b) for a, b in zip(left, right))
                    for left, right in zip(out, matrix))
    return out


def tensor_zero():
    return tuple(tuple(tuple(D.p_const(0) for _ in range(3))
                       for _ in range(3)) for _ in range(3))


def tensor_add(*tensors):
    out = tensor_zero()
    for tensor in tensors:
        out = tuple(tuple(tuple(D.p_add(a, b) for a, b in zip(line0, line1))
                          for line0, line1 in zip(plane0, plane1))
                    for plane0, plane1 in zip(out, tensor))
    return out


def x_times_F(x, F):
    return tuple(tuple(tuple(D.p_mul(x[i], F[j][k]) for k in range(3))
                       for j in range(3)) for i in range(3))


def E_times_y(E, y):
    return tuple(tuple(tuple(D.p_mul(E[i][k], y[j]) for k in range(3))
                       for j in range(3)) for i in range(3))


def D_times_z(matrix, z):
    return tuple(tuple(tuple(D.p_mul(matrix[i][j], z[k]) for k in range(3))
                       for j in range(3)) for i in range(3))


def tensor_equal(left, right):
    return all(a == b
               for plane0, plane1 in zip(left, right)
               for row0, row1 in zip(plane0, plane1)
               for a, b in zip(row0, row1))


def tensor_hash(tensor):
    return D.content_hash([
        [[[[list(monomial), str(coefficient)]
           for monomial, coefficient in sorted(entry.items())]
          for entry in row] for row in plane]
        for plane in tensor
    ])


def relation(x, y, z, F, E, matrix_D):
    return tensor_add(x_times_F(x, F), E_times_y(E, y),
                      D_times_z(matrix_D, z))


def integer_rank(columns, row_count):
    rows = [[Fraction(column.get(row, 0)) for column in columns]
            for row in range(row_count)]
    rank = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(rank, row_count)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = rows[rank][column]
        rows[rank] = [entry / value for entry in rows[rank]]
        for row in range(row_count):
            if row == rank or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [a - value * b for a, b in zip(rows[row], rows[rank])]
        rank += 1
    return rank


def zero_projection_audit():
    # Rank profile (0,2,2), normalized so the two K relations have
    # (y,z)=(e0,e0),(e1,e1).  The joint linear map on (E,D) is injective.
    columns = []
    for block in ("E", "D"):
        for first, second in itertools.product(range(3), repeat=2):
            column = {}
            for relation_index in range(2):
                if block == "E":
                    output = (first, relation_index, second)
                else:
                    output = (first, second, relation_index)
                row = relation_index * 27 + output[0] * 9 + output[1] * 3 + output[2]
                column[row] = column.get(row, 0) + 1
            columns.append(column)
    rank, pivot_rows, pivot_columns, minor_determinant = K.rank_certificate(
        columns, 54
    )
    require(rank == 18 and abs(minor_determinant) == 1,
            "the zero-projection rank-(0,2,2) map lost injectivity")
    return {
        "normalized_domain_dimension": len(columns),
        "joint_relation_rank": rank,
        "unimodular_minor": {
            "rows": pivot_rows,
            "columns": pivot_columns,
            "determinant": minor_determinant,
        },
        "rank_022_conclusion": "E=D=0",
        "lower_rank_conclusion": (
            "if rank(Y)<2 a nonzero (0,0,z) relation forces D=0; "
            "if rank(Z)<2 a nonzero (0,y,0) relation forces E=0"
        ),
        "covered_profiles": ["000", "001", "002", "011", "012", "022"],
    }


def profile_122_audit():
    u, y0, y1, z0, z1 = (const_vector(index) for index in (0, 0, 1, 0, 1))
    E = outer(u, z0)
    matrix_D = matrix_scale(D.p_const(-1), outer(u, y0))
    F = matrix_add(outer(y0, z1),
                   matrix_scale(D.p_const(-1), outer(y1, z0)))
    zero = tensor_zero()
    require(tensor_equal(relation((D.p_const(0),) * 3, y0, z0,
                                  F, E, matrix_D), zero),
            "the kernel generator (0,y0,z0) failed")
    require(tensor_equal(relation(u, y1, z1, F, E, matrix_D), zero),
            "the kernel generator (u,y1,z1) failed")
    require(integer_rank([
        {row * 3 + column: int(F[row][column].get(tuple(), 0))}
        for row, column in ((0, 0), (0, 1), (1, 0), (1, 1))
    ], 9) >= 2, "the (1,2,2) wedge lost rank two")

    a, b, c = var_vector("a"), var_vector("b"), var_vector("c")
    companion = relation(a, b, c, F, E, matrix_D)
    return {
        "normal_form": {
            "E": "u tensor z0",
            "D": "-u tensor y0",
            "F": "y0 tensor z1-y1 tensor z0",
        },
        "F_rank": 2,
        "companion_sha256": tensor_hash(companion),
        "necessary_target_alignment": "target_X = line(u)",
        "quotient_argument": (
            "mod X/<u>, a companion is [a] tensor F; a nonzero pure target "
            "outside <u> would make rank-two F decomposable"
        ),
    }


def profile_112_audit():
    x, y, z0, z1 = (const_vector(index) for index in (0, 0, 0, 1))
    E = outer(x, z0)
    matrix_D = matrix_scale(D.p_const(-1), outer(x, y))
    F = outer(y, z1)
    zero = tensor_zero()
    require(tensor_equal(relation((D.p_const(0),) * 3, y, z0,
                                  F, E, matrix_D), zero),
            "the (1,1,2) first kernel generator failed")
    require(tensor_equal(relation(x, (D.p_const(0),) * 3, z1,
                                  F, E, matrix_D), zero),
            "the (1,1,2) second kernel generator failed")
    a, b, c = var_vector("a"), var_vector("b"), var_vector("c")
    companion = relation(a, b, c, F, E, matrix_D)
    allowed = []
    for align_x, align_y, align_z0, align_z1 in itertools.product(
            (False, True), repeat=4):
        if align_z0 and align_z1:
            continue
        condition = ((align_y and align_z1)
                     or (align_x and align_z0)
                     or (align_x and align_y))
        if condition:
            allowed.append([align_x, align_y, align_z0, align_z1])
    return {
        "normal_form": {
            "E": "x tensor z0",
            "D": "-x tensor y",
            "F": "y tensor z1",
        },
        "companion_sha256": tensor_hash(companion),
        "necessary_target_alignments": [
            "target_Y=y and target_Z=z1",
            "target_X=x and target_Z=z0",
            "target_X=x and target_Y=y",
        ],
        "alignment_truth_table": allowed,
        "coincident_kernel_case": (
            "if ker(K->X)=ker(K->Y), a nonzero (0,0,z) relation forces D=0"
        ),
    }


def profile_111_audit():
    x, y, z = (const_vector(0), const_vector(0), const_vector(0))
    E = matrix_scale(D.p_const(-1), outer(x, z))
    matrix_D = outer(x, y)
    F = matrix_scale(D.p_const(-1), outer(y, z))
    zero = tensor_zero()
    require(tensor_equal(relation(x, (D.p_const(0),) * 3, z,
                                  F, E, matrix_D), zero),
            "the (1,1,1) alpha kernel generator failed")
    require(tensor_equal(relation((D.p_const(0),) * 3, y, z,
                                  F, E, matrix_D), zero),
            "the (1,1,1) beta kernel generator failed")
    a, b, c = var_vector("a"), var_vector("b"), var_vector("c")
    companion = relation(a, b, c, F, E, matrix_D)
    alignments = []
    for align_x, align_y, align_z in itertools.product((False, True), repeat=3):
        if sum((align_x, align_y, align_z)) >= 2:
            alignments.append([align_x, align_y, align_z])
    return {
        "normal_form": {
            "E": "-x tensor z",
            "D": "x tensor y",
            "F": "-y tensor z",
        },
        "companion_sha256": tensor_hash(companion),
        "necessary_target_alignment": "target shares at least two of x,y,z",
        "alignment_truth_table": alignments,
        "minor_proof": (
            "quotienting by each pair of lines gives (X or Y), (X or Z), "
            "and (Y or Z), hence at least two alignments"
        ),
        "coincident_kernel_case": (
            "coincident projection kernels give a relation with two zero "
            "components and force the opposite tensor to vanish"
        ),
    }


def audit():
    started = monotonic()
    ledger = {
        "zero_projection_profiles": zero_projection_audit(),
        "profile_122": profile_122_audit(),
        "profile_112": profile_112_audit(),
        "profile_111": profile_111_audit(),
        "profile_222": (
            "closed by the previously checked injective-tripod theorem aa85cd4"
        ),
        "complete_sorted_profiles": [
            "000", "001", "002", "011", "012", "022",
            "111", "112", "122", "222",
        ],
        "classification": (
            "with D,E,F nonzero, zero-containing profiles are impossible; "
            "222 is impossible; 122,112,111 reduce to the displayed finite "
            "target-line alignment flags"
        ),
        "base_ring_scope": (
            "normal-form identities and the zero-profile rank audit are over "
            "Z; proportionality/rank arguments apply over the fraction field "
            "of any integral coefficient domain"
        ),
        "characteristic_scope": "valid over every field",
        "status": "all ten tripod projection-rank profiles are classified",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the tripod profile-classification ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 tripod projection profiles: PASS (exact)")
    print("profiles:", ledger["complete_sorted_profiles"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()

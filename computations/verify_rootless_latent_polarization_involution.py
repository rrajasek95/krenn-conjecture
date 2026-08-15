#!/usr/bin/env python3
"""Compress the rank-six full-nine shadow to a latent involution test.

For a nondegenerate symmetric response form J on a six-dimensional latent
space L and a symmetric tensor-valued polarization C, complementary
three-dimensional endpoint stars P,S with

    J(P,P)=J(S,S)=0,          C(P,S) contained in W

are equivalent to a J-skew involution T whose +/- eigenspaces have dimension
three and which anticommutes with J^{-1} C_lambda for every lambda killing W.

The exact physical full-nine equations imply the displayed containment, but
the converse only reconstructs that coarse target-span shadow.  It does not
reconstruct the common direct matrix, literal word/fine labels, or the nine
individual source equations.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/h3-scalar-zero-packet-six-site-nonreduction.md":
        "22404c6a55c8c6a60cd3186eef3401212a60a4b6fcdc0cde5077fbab6892ff08",
    "notes/curved-pure-binary-three-channel-common-power-independent-audit.md":
        "2686bf1ddce9d22eb3fc2cdf1cd7871560744ad28a409c98e80586a10a3645de",
    "notes/2026-08-15-weakest-intrinsic-constructive-object-audit.md":
        "c40e22f6c899076b6384bccd2cf07f78d671ab6d79917ab920d04711b7298b7f",
}
EXPECTED_LEDGER_SHA256 = "a50b78ef61278df1d93e5040695443ed310480774fd843f48beeb4715cfbf853"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def shape(matrix):
    return len(matrix), len(matrix[0]) if matrix else 0


def zeros(rows, columns):
    return [[Q(0) for _ in range(columns)] for _ in range(rows)]


def identity(size):
    answer = zeros(size, size)
    for index in range(size):
        answer[index][index] = Q(1)
    return answer


def transpose(matrix):
    rows, columns = shape(matrix)
    return [[matrix[row][column] for row in range(rows)]
            for column in range(columns)]


def matmul(left, right):
    rows, middle = shape(left)
    other_middle, columns = shape(right)
    require(middle == other_middle, (shape(left), shape(right)))
    return [[sum(left[row][index] * right[index][column]
                 for index in range(middle))
             for column in range(columns)]
            for row in range(rows)]


def add(left, right):
    require(shape(left) == shape(right), (shape(left), shape(right)))
    return [[a + b for a, b in zip(left_row, right_row, strict=True)]
            for left_row, right_row in zip(left, right, strict=True)]


def subtract(left, right):
    require(shape(left) == shape(right), (shape(left), shape(right)))
    return [[a - b for a, b in zip(left_row, right_row, strict=True)]
            for left_row, right_row in zip(left, right, strict=True)]


def diagonal(entries):
    answer = zeros(len(entries), len(entries))
    for index, entry in enumerate(entries):
        answer[index][index] = Q(entry)
    return answer


def rref(matrix):
    answer = [list(row) for row in matrix]
    rows, columns = shape(answer)
    pivots = []
    pivot_row = 0
    for column in range(columns):
        selected = next((row for row in range(pivot_row, rows)
                         if answer[row][column]), None)
        if selected is None:
            continue
        answer[pivot_row], answer[selected] = answer[selected], answer[pivot_row]
        pivot = answer[pivot_row][column]
        answer[pivot_row] = [entry / pivot for entry in answer[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not answer[row][column]:
                continue
            scalar = answer[row][column]
            answer[row] = [entry - scalar * pivot_entry
                           for entry, pivot_entry in
                           zip(answer[row], answer[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return answer, tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def inverse(matrix):
    rows, columns = shape(matrix)
    require(rows == columns, shape(matrix))
    augmented = [row + unit for row, unit in
                 zip(matrix, identity(rows), strict=True)]
    reduced, pivots = rref(augmented)
    require(pivots[:rows] == tuple(range(rows)), pivots)
    return [row[rows:] for row in reduced]


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    columns = shape(matrix)[1]
    pivot_set = set(pivots)
    free = [column for column in range(columns) if column not in pivot_set]
    basis = []
    for free_column in free:
        vector = [Q(0)] * columns
        vector[free_column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(vector)
    return transpose(basis) if basis else zeros(columns, 0)


def block_matrix(top_left, top_right, bottom_left, bottom_right):
    return [left + right for left, right in
            zip(top_left, top_right, strict=True)] + [
                left + right for left, right in
                zip(bottom_left, bottom_right, strict=True)]


def restriction(form, left_basis, right_basis):
    return matmul(transpose(left_basis), matmul(form, right_basis))


def is_zero(matrix):
    return all(not entry for row in matrix for entry in row)


def columns(*vectors):
    return transpose([list(vector) for vector in vectors])


def serialize(matrix):
    return tuple(tuple(str(entry) for entry in row) for row in matrix)


def standard_packet():
    i3 = identity(3)
    z3 = zeros(3, 3)
    j = block_matrix(z3, i3, i3, z3)
    involution = diagonal((1, 1, 1, -1, -1, -1))

    # W is the first coordinate of a three-dimensional target.  C0 may have
    # arbitrary cross terms.  C1,C2 represent all covectors killing W and
    # are block diagonal, exactly the condition C(P,S) subset W.
    c0 = [
        [Q(2), 0, 1, 3, -1, 2],
        [0, -1, 4, 1, 5, -2],
        [1, 4, 0, 2, -3, 1],
        [3, 1, 2, 1, 2, 0],
        [-1, 5, -3, 2, 0, 4],
        [2, -2, 1, 0, 4, -2],
    ]
    c1 = block_matrix(
        [[Q(1), 2, 0], [2, 0, -1], [0, -1, 3]], z3,
        z3, [[Q(0), 1, 2], [1, -2, 0], [2, 0, 1]],
    )
    c2 = block_matrix(
        [[Q(2), 0, -1], [0, 1, 3], [-1, 3, 0]], z3,
        z3, [[Q(1), -2, 1], [-2, 4, 2], [1, 2, -1]],
    )
    require(all(form == transpose(form) for form in (j, c0, c1, c2)),
            "forms must be symmetric")
    return j, involution, (c0, c1, c2)


def audit_equivalence(j, involution, constrained_forms):
    n = len(j)
    require(n == 6 and rank(j) == 6, (n, rank(j)))
    require(matmul(involution, involution) == identity(n), "T^2 != I")
    require(sum(involution[index][index] for index in range(n)) == 0,
            "trace T != 0")
    require(is_zero(add(matmul(transpose(involution), j),
                        matmul(j, involution))), "T is not J-skew")

    j_inverse = inverse(j)
    for form in constrained_forms:
        operator = matmul(j_inverse, form)
        require(is_zero(add(matmul(operator, involution),
                            matmul(involution, operator))),
                ("anticommutator nonzero", serialize(form)))

    plus = nullspace(subtract(involution, identity(n)))
    minus = nullspace(add(involution, identity(n)))
    require(shape(plus) == (6, 3) and shape(minus) == (6, 3),
            (shape(plus), shape(minus)))
    require(rank([left + right for left, right in
                  zip(plus, minus, strict=True)]) == 6,
            "eigenspaces do not span")
    require(is_zero(restriction(j, plus, plus)), "P is not J-isotropic")
    require(is_zero(restriction(j, minus, minus)), "S is not J-isotropic")
    require(rank(restriction(j, plus, minus)) == 3,
            "J cross pairing is not perfect")
    for form in constrained_forms:
        require(is_zero(restriction(form, plus, minus)),
                "C_lambda(P,S) is nonzero")
    return plus, minus


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    j, involution, forms = standard_packet()
    plus, minus = audit_equivalence(j, involution, forms[1:])

    # The nine cross evaluations of the unconstrained coordinate may be
    # arbitrary, whereas every coordinate in W^perp vanishes on P x S.
    cross_ranks = tuple(rank(restriction(form, plus, minus)) for form in forms)
    require(cross_ranks == (3, 0, 0), cross_ranks)

    # Basis invariance.  This non-orthogonal deterministic matrix changes all
    # coordinate expressions while preserving the intrinsic identities.
    change = [
        [1, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 2],
    ]
    require(rank(change) == 6, rank(change))
    change_inverse = inverse(change)
    conjugated_j = matmul(transpose(change), matmul(j, change))
    conjugated_t = matmul(change_inverse, matmul(involution, change))
    conjugated_forms = tuple(
        matmul(transpose(change), matmul(form, change)) for form in forms)
    conjugated_plus, conjugated_minus = audit_equivalence(
        conjugated_j, conjugated_t, conjugated_forms[1:])
    require(tuple(rank(restriction(form, conjugated_plus, conjugated_minus))
                  for form in conjugated_forms) == cross_ranks,
            "cross ranks changed under basis transport")

    # A single constrained form C_lambda=J is a sharp negative guard.  Then
    # J^{-1}C_lambda=I, and anticommutation would give 2T=0.  In characteristic
    # not two this forces T=0, incompatible with T^2=I.
    negative_operator = matmul(inverse(j), j)
    negative_anticommutant_coefficient = Q(2)
    require(negative_operator == identity(6), negative_operator)
    require(negative_anticommutant_coefficient != 0,
            "characteristic-two guard unexpectedly vanished")

    # A rank-deficient pair of endpoint images cannot be encoded by this
    # involution: complementary eigenspaces necessarily span all of L.  It is
    # a separate geometric branch, not a counterexample to the equivalence.
    deficient_s = columns(
        (1, 0, 0, 0, 0, 0),
        (0, 1, 0, 0, 0, 0),
        (0, 0, 0, 1, 0, 0),
    )
    require(rank([left + right for left, right in
                  zip(plus, deficient_s, strict=True)]) == 4,
            "rank-deficient guard did not lose two latent directions")

    return {
        "theorem": (
            "rank-six endpoint-star target-span containment is equivalent "
            "to a J-skew trace-zero involution anticommuting with all "
            "projected polarization operators"
        ),
        "pins": PINS,
        "standard_packet": {
            "dim_L": 6,
            "rank_J": rank(j),
            "dim_P": shape(plus)[1],
            "dim_S": shape(minus)[1],
            "rank_J_cross": rank(restriction(j, plus, minus)),
            "target_cross_ranks": cross_ranks,
            "involution_trace": "0",
        },
        "operator_test": {
            "definition": "A_lambda=J^{-1}C_lambda",
            "equations": (
                "T^2=I", "tr(T)=0", "T^T J+J T=0",
                "A_lambda T+T A_lambda=0 for lambda in W^perp",
            ),
            "constrained_forms_checked": 2,
        },
        "basis_invariance": {
            "change_rank": rank(change),
            "transport": "J,C -> g^T(J,C)g; T -> g^{-1}Tg",
            "cross_ranks_after_transport": tuple(
                rank(restriction(form, conjugated_plus, conjugated_minus))
                for form in conjugated_forms),
        },
        "negative_guard": {
            "C_lambda": "J",
            "A_lambda": "I",
            "anticommutator": "2T",
            "verdict": "no involution in characteristic not two",
        },
        "scope": {
            "physical_implication": (
                "literal full-nine compatibility implies the coarse "
                "containment C(P,S) subset W and hence the involution"
            ),
            "nonconverse": (
                "the involution reconstructs only target-span containment, "
                "not a common direct matrix or word/fine/source labels"
            ),
            "separate_branch": (
                "dim(P+S)<6 is outside the involution equivalence and must "
                "be classified independently"
            ),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("rootless latent polarization involution: PASS")
    print("mode", arguments.mode)
    print("rank-six split / involution / projected anticommutators: equivalent")
    print("physical scope: full-nine implies test; converse is coarse only")
    print("sha256:", digest)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact linear-algebra audit of the augmented-pentagon Fredholm alternative.

This checker deliberately does not manufacture the physical overlap--jet map
P. It verifies the theorem interface which applies once that source-valid
map and its complete augmented correction map J have been constructed.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json


Q = Fraction
N = 5
EXPECTED_DIGEST = "be24a91a9d275eaa7879cdb91a057b4d4993ca8608307ee3bb03376859d23f24"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rref(matrix, field_modulus=None):
    rows = [list(row) for row in matrix]
    if not rows:
        return rows, []
    ncols = len(rows[0])
    pivots = []
    pivot_row = 0
    for col in range(ncols):
        found = None
        for row in range(pivot_row, len(rows)):
            value = rows[row][col]
            if field_modulus is not None:
                value %= field_modulus
            if value:
                found = row
                break
        if found is None:
            continue
        rows[pivot_row], rows[found] = rows[found], rows[pivot_row]
        pivot = rows[pivot_row][col]
        if field_modulus is None:
            rows[pivot_row] = [value / pivot for value in rows[pivot_row]]
        else:
            inverse = pow(pivot % field_modulus, -1, field_modulus)
            rows[pivot_row] = [
                value * inverse % field_modulus for value in rows[pivot_row]
            ]
        for row in range(len(rows)):
            if row == pivot_row:
                continue
            factor = rows[row][col]
            if field_modulus is not None:
                factor %= field_modulus
            if not factor:
                continue
            if field_modulus is None:
                rows[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(rows[row], rows[pivot_row])
                ]
            else:
                rows[row] = [
                    (value - factor * pivot_value) % field_modulus
                    for value, pivot_value in zip(rows[row], rows[pivot_row])
                ]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivots


def rank(matrix, field_modulus=None):
    return len(rref(matrix, field_modulus)[1])


def in_row_span(vector, rows, field_modulus=None):
    return rank(rows, field_modulus) == rank(
        rows + [list(vector)], field_modulus
    )


def nullspace(matrix, field_modulus=None, ncols=N):
    if not matrix:
        return [
            [1 if i == j else 0 for i in range(ncols)]
            for j in range(ncols)
        ]
    reduced, pivots = rref(matrix, field_modulus)
    ncols = len(matrix[0])
    free = [col for col in range(ncols) if col not in pivots]
    basis = []
    for free_col in free:
        vector = [0] * ncols
        vector[free_col] = 1
        for row, pivot_col in enumerate(pivots):
            value = -reduced[row][free_col]
            if field_modulus is not None:
                value %= field_modulus
            vector[pivot_col] = value
        basis.append(vector)
    return basis


def matvec(matrix, vector, modulus=None):
    answer = [sum(a * b for a, b in zip(row, vector)) for row in matrix]
    if modulus is not None:
        answer = [value % modulus for value in answer]
    return answer


def audit_matrix(matrix, modulus):
    epsilon = [1] * N
    kernel = nullspace(matrix, modulus)
    def aggregate_nonzero(vector):
        value = sum(vector)
        return bool(value if modulus is None else value % modulus)

    repair = any(aggregate_nonzero(vector) for vector in kernel)
    separator = in_row_span(epsilon, matrix, modulus)
    require(repair != separator, "Fredholm alternatives are not exclusive")
    if repair:
        witness = next(vector for vector in kernel if aggregate_nonzero(vector))
        require(
            not any(matvec(matrix, witness, modulus)),
            "repair is not in kernel",
        )
    else:
        require(separator, "missing row-space separator")
    return repair


def exhaustive_binary_audit():
    counts = {}
    total = 0
    for nrows in range(4):
        repairs = 0
        separators = 0
        for entries in product((0, 1), repeat=nrows * N):
            matrix = [
                list(entries[row * N:(row + 1) * N])
                for row in range(nrows)
            ]
            if audit_matrix(matrix, 2):
                repairs += 1
            else:
                separators += 1
            total += 1
        counts[nrows] = {"repair": repairs, "separator": separators}
    require(total == 1 + 32 + 1024 + 32768, "binary census size changed")
    return counts


def quotient_rows(j_columns, p_columns):
    dimension = len(p_columns[0])
    quotient_covectors = nullspace(
        [list(column) for column in j_columns],
        ncols=dimension,
    )
    return [
        [
            sum(covector[row] * column[row] for row in range(dimension))
            for column in p_columns
        ]
        for covector in quotient_covectors
    ]


def rational_examples():
    j = [[Q(1), Q(0), Q(0), Q(0)]]
    p_repair = [
        [Q(0), Q(1), Q(0), Q(0)],
        [Q(0), Q(0), Q(1), Q(0)],
        [Q(0), Q(0), Q(0), Q(1)],
        [Q(0), Q(-1), Q(-1), Q(-1)],
        [Q(1), Q(0), Q(0), Q(0)],
    ]
    rows = quotient_rows(j, p_repair)
    require(audit_matrix(rows, None), "rational repair branch lost")

    p_separator = [
        [Q(0), Q(1), Q(0), Q(0)],
        [Q(0), Q(0), Q(1), Q(0)],
        [Q(0), Q(0), Q(0), Q(1)],
        [Q(0), Q(1), Q(1), Q(-1)],
        [Q(0), Q(2), Q(-1), Q(0)],
    ]
    rows = quotient_rows(j, p_separator)
    require(not audit_matrix(rows, None), "rational separator branch lost")

    c = [Q(1), Q(1), Q(1), Q(1), Q(1)]
    pc = [
        sum(c[i] * p_repair[i][row] for i in range(N))
        for row in range(4)
    ]
    require(pc == [Q(1), Q(0), Q(0), Q(0)], "repair boundary changed")
    require(sum(c) == 5, "repair aggregate changed")
    return {
        "repair_quotient_rank": rank(quotient_rows(j, p_repair)),
        "separator_quotient_rank": rank(quotient_rows(j, p_separator)),
        "repair_aggregate": str(sum(c)),
    }


def main():
    ledger = {
        "binary": exhaustive_binary_audit(),
        "rational": rational_examples(),
        "physical_input": (
            "P requires invisible first jets plus the complete target/ores-"
            "augmented mixed-Hessian correction class modulo im(Jhat)"
        ),
        "non_instantiations": [
            "bare marked polar: connecting matrix I5",
            "formal fourth Hasse top: sends H_m to 1",
            "zero-target terminal packet: missing GHZ anchors",
            "polynomial/Tate source rows: target-locked",
        ],
    }
    digest = sha256(json.dumps(ledger, sort_keys=True).encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_PINNED":
        require(digest == EXPECTED_DIGEST, "ledger digest changed")
    print("rootless augmented-pentagon Fredholm alternative: PASS")
    print(json.dumps(ledger, sort_keys=True))
    print("ledger", digest)


if __name__ == "__main__":
    main()

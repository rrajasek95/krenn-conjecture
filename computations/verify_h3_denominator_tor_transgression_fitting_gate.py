#!/usr/bin/env python3
"""Exact Tor/transgression gate for the five h=3 denominator defects.

The universal denominator differential is

    b : R^15 -> R^243,  d_(v,a) |-> e_a^(v) q^[2].

The cap-coordinate map selects the five columns (v,12112_v).  Universal
injectivity identifies Tor_1(coker(b),S) with ker(b tensor S).  This checker
reconstructs two exact rational specializations and computes the rank of the
cap projection on that kernel.  It uses no imports from earlier checkers.
"""

import argparse
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


ZERO = Q(0)
ONE = Q(1)
COLORS = (0, 1, 2)
SITES = (1, 2, 3, 4, 5)
WORDS = tuple(product(COLORS, repeat=5))
LABELS = tuple((site, color) for site in SITES for color in COLORS)
MIXED = (1, 2, 1, 1, 2)
SELECTED = tuple((site, MIXED[site - 1]) for site in SITES)
EXPECTED_DIGEST = "268c982050599af3358acb2c6b3dabc5eca0e95c994f75e50d560c41f132152a"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge_key(left, right, left_color, right_color):
    if left < right:
        return (left, right, left_color, right_color)
    return (right, left, right_color, left_color)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def denominator_matrix(value):
    """Return the 243 by 15 matrix of b for an exact cell-value function."""
    columns = []
    for site, color in LABELS:
        column = []
        for word in WORDS:
            if word[site - 1] != color:
                column.append(ZERO)
                continue
            total = ZERO
            remaining = tuple(vertex for vertex in SITES if vertex != site)
            for matching in matchings(remaining):
                term = ONE
                for left, right in matching:
                    term *= value(
                        left, right, word[left - 1], word[right - 1]
                    )
                total += term
            column.append(total)
        columns.append(column)
    return [
        [columns[column][row] for column in range(len(LABELS))]
        for row in range(len(WORDS))
    ]


def rref(matrix):
    work = [[Q(entry) for entry in row] for row in matrix]
    rank = 0
    pivots = []
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                scale = work[row][column]
                work[row] = [
                    entry - scale * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[rank])
                ]
        pivots.append(column)
        rank += 1
    return work, tuple(pivots)


def matrix_rank(matrix):
    return len(rref(matrix)[1])


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    width = len(matrix[0]) if matrix else 0
    free = tuple(column for column in range(width) if column not in pivots)
    basis = []
    for free_column in free:
        vector = [ZERO] * width
        vector[free_column] = ONE
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[row][free_column]
        basis.append(tuple(vector))
    return tuple(basis)


def determinant(matrix):
    work = [[Q(entry) for entry in row] for row in matrix]
    require(all(len(row) == len(work) for row in work), "determinant not square")
    answer = ONE
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return ZERO
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        scale = work[column][column]
        answer *= scale
        work[column] = [entry / scale for entry in work[column]]
        for row in range(column + 1, len(work)):
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[column])
            ]
    return answer


def submatrix(matrix, row_indices, column_indices):
    return [
        [matrix[row][column] for column in column_indices]
        for row in row_indices
    ]


def generic_value(left, right, left_color, right_color):
    """A fixed integral point certifying the universal column ranks."""
    if left > right:
        left, right = right, left
        left_color, right_color = right_color, left_color
    return Q(((((left - 1) * 5 + right) * 3 + left_color) * 3 + right_color) + 1)


# Only internal odd-site cells are needed for b.  These tables are copied as
# raw mathematical input, not imported from any earlier executable.
DIRECT_FREE_INTERNAL = (
    (1, 2, 1, 2, 1),
    (1, 3, 1, 2, 1),
    (1, 4, 1, 1, 1),
    (2, 3, 2, 0, 1),
    (3, 4, 0, 1, 1),
    (3, 5, 0, 2, 1),
)

TILTED_INTERNAL = (
    (1, 2, 1, 2, 1),
    (1, 3, 0, 0, 1),
    (1, 4, 1, 1, 1),
    (1, 5, 2, 2, 1),
    (2, 3, 2, 0, 1),
    (3, 4, 0, 1, 1),
    (3, 5, 0, 2, 1),
)


def sparse_value(rows):
    table = {}
    for left, right, left_color, right_color, value in rows:
        key = edge_key(left, right, left_color, right_color)
        require(key not in table, f"duplicate cell {key}")
        table[key] = Q(value)

    def value(left, right, left_color, right_color):
        return table.get(edge_key(left, right, left_color, right_color), ZERO)

    return value


def word_index(text):
    return WORDS.index(tuple(int(character) for character in text))


def label_indices(labels):
    return tuple(LABELS.index(label) for label in labels)


def vector_text(vector):
    terms = []
    for coefficient, label in zip(vector, LABELS):
        if coefficient:
            terms.append(f"{coefficient}:d{label[0]}{label[1]}")
    return terms


def universal_audit():
    matrix = denominator_matrix(generic_value)
    selected = label_indices(SELECTED)
    other = tuple(index for index in range(15) if index not in selected)

    full_rows = tuple(map(word_index, (
        "00000", "00001", "00002", "00010", "00011",
        "00020", "00100", "00101", "00110", "00111",
        "00200", "01000", "02000", "10000", "20000",
    )))
    full_minor = determinant(submatrix(matrix, full_rows, tuple(range(15))))
    require(
        full_minor == Q(-32451587105484628367742562673068054425600000),
        "universal rank-15 witness changed",
    )
    require(matrix_rank(matrix) == 15, "universal b lost injectivity witness")

    other_rows = tuple(map(word_index, (
        "00000", "00001", "00002", "00010", "00011",
        "00020", "00100", "00200", "01000", "20000",
    )))
    other_minor = determinant(submatrix(matrix, other_rows, other))
    require(
        other_minor == Q(8906634052942223094145500014691840000),
        "universal rank-10 unselected witness changed",
    )
    require(matrix_rank(submatrix(matrix, range(243), other)) == 10,
            "universal unselected block rank changed")
    return {
        "full_rank": 15,
        "full_minor": str(full_minor),
        "unselected_rank": 10,
        "unselected_minor": str(other_minor),
    }


PACKET_EXPECTATIONS = {
    "direct_free": {
        "rows": DIRECT_FREE_INTERNAL,
        "kappa": Q(-1, 4),
        "rank": 7,
        "unselected_rank": 6,
        "tor_dimension": 8,
        "transgression_rank": 4,
        "individual_classes_hit": (True, False, True, False, False),
        "kernel": (
            ("1:d10",), ("1:d11",), ("1:d12",),
            ("1:d30",), ("1:d31",), ("1:d32",),
            ("-1:d22", "1:d41"),
            ("-2:d22", "1:d52"),
        ),
        "projection": (
            (0, 0, 0, 0, 0), (1, 0, 0, 0, 0),
            (0, 0, 0, 0, 0), (0, 0, 0, 0, 0),
            (0, 0, 1, 0, 0), (0, 0, 0, 0, 0),
            (0, -1, 0, 1, 0), (0, -2, 0, 0, 1),
        ),
        "cokernel_covectors": ((0, 1, 0, 1, 2),),
        "witness_columns": (
            (2, 0), (2, 1), (4, 0), (4, 2),
            (5, 0), (5, 1), (2, 2),
        ),
        "witness_rows": (
            "10012", "11012", "12002", "12010",
            "12011", "12012", "12022",
        ),
        "witness_minor": Q(-4),
    },
    "tilted": {
        "rows": TILTED_INTERNAL,
        "kappa": Q(-5, 2),
        "rank": 8,
        "unselected_rank": 6,
        "tor_dimension": 7,
        "transgression_rank": 3,
        "individual_classes_hit": (True, False, True, False, False),
        "kernel": (
            ("1:d10",), ("1:d11",), ("1:d12",),
            ("1:d30",), ("1:d31",), ("1:d32",),
            ("-1:d22", "1:d41"),
        ),
        "projection": (
            (0, 0, 0, 0, 0), (1, 0, 0, 0, 0),
            (0, 0, 0, 0, 0), (0, 0, 0, 0, 0),
            (0, 0, 1, 0, 0), (0, 0, 0, 0, 0),
            (0, -1, 0, 1, 0),
        ),
        "cokernel_covectors": (
            (0, 1, 0, 1, 0), (0, 0, 0, 0, 1),
        ),
        "witness_columns": (
            (2, 0), (2, 1), (4, 0), (4, 2),
            (5, 0), (5, 1), (2, 2), (5, 2),
        ),
        "witness_rows": (
            "10012", "11012", "12002", "12010",
            "12011", "12012", "12022", "22012",
        ),
        "witness_minor": Q(8),
    },
}


def packet_audit(name):
    expected = PACKET_EXPECTATIONS[name]
    matrix = denominator_matrix(sparse_value(expected["rows"]))
    selected = label_indices(SELECTED)
    other = tuple(index for index in range(15) if index not in selected)
    full_rank = matrix_rank(matrix)
    other_rank = matrix_rank(submatrix(matrix, range(243), other))
    require(full_rank == expected["rank"], f"{name}: full rank changed")
    require(other_rank == expected["unselected_rank"],
            f"{name}: unselected rank changed")

    kernel = nullspace(matrix)
    require(len(kernel) == expected["tor_dimension"],
            f"{name}: Tor dimension changed")
    kernel_text = tuple(tuple(vector_text(vector)) for vector in kernel)
    require(kernel_text == expected["kernel"], f"{name}: kernel basis changed")
    projection = tuple(
        tuple(vector[index] for index in selected) for vector in kernel
    )
    require(projection == expected["projection"],
            f"{name}: transgression matrix changed")
    transgression_rank = matrix_rank(projection)
    require(transgression_rank == expected["transgression_rank"],
            f"{name}: transgression rank changed")
    individual_classes_hit = []
    for index in range(5):
        basis_vector = tuple(ONE if position == index else ZERO
                             for position in range(5))
        individual_classes_hit.append(
            matrix_rank(projection) == matrix_rank(list(projection) + [basis_vector])
        )
    require(tuple(individual_classes_hit) == expected["individual_classes_hit"],
            f"{name}: individual hit ledger changed")

    for covector in expected["cokernel_covectors"]:
        require(
            all(sum(c * x for c, x in zip(covector, row)) == 0
                for row in projection),
            f"{name}: claimed cokernel covector no longer annihilates image",
        )
    require(
        matrix_rank(list(projection) + list(expected["cokernel_covectors"]))
        == transgression_rank + len(expected["cokernel_covectors"]),
        f"{name}: cokernel covectors lost independence",
    )

    # The five scalar reset defects all vanish, but this only tests one word
    # row of each selected column and does not imply whole-column membership.
    mixed_row = WORDS.index(MIXED)
    defect_values = tuple(matrix[mixed_row][index] for index in selected)
    require(defect_values == (ZERO,) * 5, f"{name}: h_v values changed")

    witness_columns = label_indices(expected["witness_columns"])
    witness_rows = tuple(map(word_index, expected["witness_rows"]))
    witness_minor = determinant(
        submatrix(matrix, witness_rows, witness_columns)
    )
    require(witness_minor == expected["witness_minor"],
            f"{name}: nonmembership minor changed")
    require(expected["kappa"], f"{name}: inactive curvature packet")

    return {
        "kappa": str(expected["kappa"]),
        "h_values": [str(value) for value in defect_values],
        "rank_b": full_rank,
        "rank_b_unselected": other_rank,
        "tor1_dimension": len(kernel),
        "transgression_rank": transgression_rank,
        "transgression_cokernel_dimension": 5 - transgression_rank,
        "individual_classes_hit": individual_classes_hit,
        "kernel_basis": [list(row) for row in kernel_text],
        "transgression_rows": [list(map(str, row)) for row in projection],
        "cokernel_covectors": [
            list(map(str, row)) for row in expected["cokernel_covectors"]
        ],
        "nonmembership_minor": str(witness_minor),
        "nonmembership_minor_columns": [
            f"d{site}{color}" for site, color in expected["witness_columns"]
        ],
        "nonmembership_minor_rows": list(expected["witness_rows"]),
    }


def run(mode):
    ledger = {}
    if mode in ("all", "universal"):
        ledger["universal"] = universal_audit()
    if mode in ("all", "direct_free"):
        ledger["direct_free"] = packet_audit("direct_free")
    if mode in ("all", "tilted"):
        ledger["tilted"] = packet_audit("tilted")
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if mode == "all":
        require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")
    print(f"h=3 denominator Tor transgression/Fitting gate ({mode}): PASS")
    if mode in ("all", "universal"):
        print("universal b: rank 15; unselected block: rank 10")
    if mode in ("all", "direct_free"):
        print("direct-free: Tor_1 dimension 8, transgression rank 4 < 5")
    if mode in ("all", "tilted"):
        print("tilted: Tor_1 dimension 7, transgression rank 3 < 5")
    print(f"sha256: {digest}")
    return digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("all", "universal", "direct_free", "tilted"),
        default="all",
    )
    arguments = parser.parse_args()
    run(arguments.mode)


if __name__ == "__main__":
    main()

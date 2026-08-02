#!/usr/bin/env python3
"""Exact audit of the h=3 mixed-word reset / cross-quotient obstruction.

The checker reconstructs the two eight-site rational packets independently,
enumerates their full pq EqSystem failures, and tests the literal ordered map

    P_m = insertion(00000) o coefficient_extraction(m)

on the five-site odd quotient by R_1 q^[2].  It deliberately does not assert
that P_m has a lift to the source-relation or relative-Rees complex.
"""

from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


ZERO = Q(0)
ONE = Q(1)
COLORS = tuple(range(3))
INTERNAL = tuple(range(6))
ODD = (1, 2, 3, 4, 5)
P = 6
Q_SITE = 7
ALL_SITES = tuple(range(8))
PURE_ZERO = (0, 0, 0, 0, 0)
EXPECTED_DIGEST = "e6cdf0ba736f7444637967d4eeb18966cdc42ca721ea79d4cb2f5262bbaa8063"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge_key(left, right, left_color, right_color):
    if left < right:
        return (left, right, left_color, right_color)
    return (right, left, right_color, left_color)


def cells_from_rows(rows):
    cells = {}
    for left, right, left_color, right_color, numerator, denominator in rows:
        key = edge_key(left, right, left_color, right_color)
        value = Q(numerator, denominator)
        require(value and key not in cells, f"bad cell {key}")
        cells[key] = value
    return cells


DIRECT_FREE_ROWS = (
    (0, 1, 0, 1, 1, 1), (0, 2, 0, 2, 1, 1),
    (0, 3, 0, 1, 1, 1), (0, 4, 0, 1, 1, 1),
    (0, 5, 0, 2, 1, 1), (0, 6, 0, 0, 1, 1),
    (1, 2, 1, 2, 1, 1), (1, 3, 1, 2, 1, 1),
    (1, 4, 1, 1, 1, 1), (1, 6, 1, 1, 1, 1),
    (2, 3, 2, 0, 1, 1), (2, 6, 2, 2, 1, 1),
    (3, 4, 0, 1, 1, 1), (3, 5, 0, 2, 1, 1),
    (3, 7, 0, 0, 1, 1), (4, 7, 1, 1, 1, 1),
    (5, 7, 2, 2, 1, 1),
    (6, 7, 0, 1, -1, 4), (6, 7, 0, 2, -1, 2),
    (6, 7, 1, 1, -1, 2), (6, 7, 1, 2, -1, 2),
    (6, 7, 2, 0, -1, 4), (6, 7, 2, 1, -1, 4),
    (6, 7, 2, 2, -1, 4),
)


TILTED_ROWS = (
    (0, 1, 0, 1, 1, 1), (0, 2, 0, 2, 1, 1),
    (0, 4, 0, 1, 1, 1), (0, 5, 0, 2, 1, 1),
    (0, 6, 0, 0, 1, 1), (1, 2, 1, 2, 1, 1),
    (1, 3, 0, 0, 1, 1), (1, 4, 1, 1, 1, 1),
    (1, 5, 2, 2, 1, 1), (1, 6, 0, 2, -1, 4),
    (1, 6, 1, 0, 1, 1), (1, 6, 1, 1, 1, 1),
    (1, 6, 2, 0, 1, 4), (1, 6, 2, 1, 1, 2),
    (1, 6, 2, 2, 1, 8), (2, 3, 2, 0, 1, 1),
    (2, 6, 2, 2, 1, 1), (2, 7, 2, 1, 1, 1),
    (3, 4, 0, 1, 1, 1), (3, 5, 0, 2, 1, 1),
    (3, 7, 0, 0, 1, 1), (4, 7, 1, 1, 1, 1),
    (5, 7, 2, 2, 1, 1),
    (6, 7, 0, 1, -3, 2), (6, 7, 0, 2, -1, 1),
    (6, 7, 1, 1, -1, 1), (6, 7, 1, 2, -1, 2),
    (6, 7, 2, 0, -1, 4), (6, 7, 2, 1, -1, 4),
    (6, 7, 2, 2, -1, 4),
)


PACKETS = {
    "direct_free": {
        "cells": cells_from_rows(DIRECT_FREE_ROWS),
        "kappa": Q(-1, 4),
        "full_failures": (
            ((0, 0, 0, 0, 0, 0), 0, 0, ZERO, ONE),
            ((0, 1, 2, 1, 1, 2), 2, 2, ONE, ZERO),
            ((0, 1, 2, 2, 1, 2), 2, 1, ONE, ZERO),
            ((0, 1, 2, 2, 1, 2), 2, 2, ONE, ZERO),
            ((1, 1, 1, 1, 1, 1), 1, 1, ZERO, ONE),
            ((2, 2, 2, 2, 2, 2), 2, 2, ZERO, ONE),
        ),
        "mixed": (
            ("12112", 2, 2, ONE),
            ("12212", 2, 1, ONE),
            ("12212", 2, 2, ONE),
        ),
        "descent_witnesses": {
            "12112": (),
            "12212": (),
        },
    },
    "tilted": {
        "cells": cells_from_rows(TILTED_ROWS),
        "kappa": Q(-5, 2),
        "full_failures": (
            ((0, 0, 0, 0, 0, 0), 0, 0, ZERO, ONE),
            ((0, 0, 2, 0, 1, 2), 2, 2, Q(1, 2), ZERO),
            ((0, 2, 2, 0, 1, 2), 0, 2, Q(-3, 2), ZERO),
            ((0, 2, 2, 0, 1, 2), 2, 0, Q(1, 2), ZERO),
            ((0, 2, 2, 0, 1, 2), 2, 2, Q(-1, 4), ZERO),
            ((1, 1, 1, 1, 1, 1), 1, 1, ZERO, ONE),
            ((2, 2, 2, 2, 2, 2), 2, 2, ZERO, ONE),
        ),
        "mixed": (
            ("02012", 2, 2, Q(1, 2)),
            ("22012", 0, 2, Q(-3, 2)),
            ("22012", 2, 0, Q(1, 2)),
            ("22012", 2, 2, Q(-1, 4)),
        ),
        "descent_witnesses": {
            "02012": (),
            "22012": ((2, 2, ONE), (4, 1, ONE)),
        },
    },
}


def get(cells, left, right, left_color, right_color):
    return cells.get(edge_key(left, right, left_color, right_color), ZERO)


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def matching_value(cells, assignment, vertices=ALL_SITES):
    answer = ZERO
    for matching in matchings(tuple(vertices)):
        value = ONE
        for left, right in matching:
            value *= get(
                cells, left, right, assignment[left], assignment[right]
            )
            if not value:
                break
        answer += value
    return answer


def target_value(word, left_color, right_color):
    return ONE if (
        left_color == right_color
        and all(color == left_color for color in word)
    ) else ZERO


def cap_residual(cells, word, left_color, right_color):
    assignment = dict(zip(INTERNAL, word))
    assignment[P] = left_color
    assignment[Q_SITE] = right_color
    return (
        matching_value(cells, assignment)
        - target_value(word, left_color, right_color)
    )


def full_failure_ledger(cells):
    failures = []
    for word in product(COLORS, repeat=6):
        for left_color in COLORS:
            for right_color in COLORS:
                actual = cap_residual(cells, word, left_color, right_color)
                if actual:
                    target = target_value(word, left_color, right_color)
                    failures.append(
                        (
                            word, left_color, right_color,
                            actual + target, target,
                        )
                    )
    return tuple(failures)


def q_square_word_coefficient(cells, word, linear_site, linear_color):
    """Coefficient of word in e_(site,color) q_ODD^[2]."""
    position = ODD.index(linear_site)
    if word[position] != linear_color:
        return ZERO
    assignment = dict(zip(ODD, word))
    remainder = tuple(site for site in ODD if site != linear_site)
    answer = ZERO
    for matching in matchings(remainder):
        value = ONE
        for left, right in matching:
            value *= get(
                cells, left, right, assignment[left], assignment[right]
            )
        answer += value
    return answer


def denominator_columns(cells):
    words = tuple(product(COLORS, repeat=5))
    columns = []
    labels = []
    for site in ODD:
        for color in COLORS:
            columns.append([
                q_square_word_coefficient(cells, word, site, color)
                for word in words
            ])
            labels.append((site, color))
    return words, labels, columns


def matrix_rank(matrix):
    work = [list(row) for row in matrix]
    rank = 0
    for column in range(len(work[0]) if work else 0):
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
        rank += 1
    return rank


def audit_packet(name, packet):
    cells = packet["cells"]
    require(
        full_failure_ledger(cells) == packet["full_failures"],
        f"{name}: full EqSystem failure ledger changed",
    )

    words, labels, columns = denominator_columns(cells)
    word_index = {word: index for index, word in enumerate(words)}
    denominator_matrix = [
        [column[row] for column in columns]
        for row in range(len(words))
    ]
    denominator_rank = matrix_rank(denominator_matrix)
    require(
        denominator_rank == (7 if name == "direct_free" else 8),
        f"{name}: odd denominator rank changed",
    )

    y0 = [ONE if word == PURE_ZERO else ZERO for word in words]
    augmented = [
        row + [y0[index]]
        for index, row in enumerate(denominator_matrix)
    ]
    require(
        matrix_rank(augmented) == denominator_rank + 1,
        f"{name}: [00000] died in the odd quotient",
    )

    descent = {}
    for tag, expected_witnesses in packet["descent_witnesses"].items():
        word = tuple(int(character) for character in tag)
        row = word_index[word]
        witnesses = tuple(
            (site, color, columns[index][row])
            for index, (site, color) in enumerate(labels)
            if columns[index][row]
        )
        require(
            witnesses == expected_witnesses,
            f"{name}: quotient-descent witnesses for {tag} changed",
        )
        descent[tag] = not witnesses

    normalized_outputs = []
    for tag, left_color, right_color, expected in packet["mixed"]:
        word = (0,) + tuple(int(character) for character in tag)
        actual = cap_residual(cells, word, left_color, right_color)
        require(actual == expected, f"{name}: mixed row {tag} changed")
        require(
            target_value(word, left_color, right_color) == ZERO,
            f"{name}: mixed row {tag} acquired target",
        )
        if descent[tag]:
            scale = -packet["kappa"] / actual
            output = scale * actual
            require(
                output == -packet["kappa"],
                f"{name}: normalized reset output changed",
            )
            normalized_outputs.append((tag, left_color, right_color, scale, output))

    if name == "direct_free":
        require(
            len(normalized_outputs) == 3,
            "direct-free: a listed reset lost quotient descent",
        )
        # P_12112-P_12212 is nonzero on [12112], because both coordinate
        # functionals kill the denominator while [00000] survives.
        word_12112 = tuple(int(character) for character in "12112")
        require(
            all(
                column[word_index[word_12112]] == ZERO for column in columns
            ),
            "direct-free: 12112 no longer defines a quotient functional",
        )
        reset_difference_nonzero = True
    else:
        require(
            [item[0] for item in normalized_outputs] == ["02012"],
            "tilted: exact descended mixed reset set changed",
        )
        reset_difference_nonzero = False

    return {
        "denominator_rank": denominator_rank,
        "descent": descent,
        "normalized_outputs": [
            [tag, left, right, str(scale), str(output)]
            for tag, left, right, scale, output in normalized_outputs
        ],
        "reset_difference_nonzero": reset_difference_nonzero,
    }


def main():
    ledger = {
        name: audit_packet(name, packet)
        for name, packet in PACKETS.items()
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, "audit ledger digest changed")
    print("h=3 mixed-word reset cross-quotient chain-lift obstruction: PASS")
    print("direct-free descended tags: 12112, 12212")
    print("tilted descended tag: 02012; 22012 has two exact boundary defects")
    print("literal reset transports EqSystem failure, not a physical secondary cell")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

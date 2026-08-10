#!/usr/bin/env python3
"""Exact cross-q Hamming-one lift test for the nonclean pure-nine packet.

The three pure q-slices and both endpoint stars are frozen to the integral
packet of ``verify_h3_pure_nine_rank_two_hafnian_update_boundary.py``.  All
90 ordered cross-colour cells of the 15 internal physical blocks are free.
Every Hamming-one full-nine equation is linear in those cells.  This script
solves that complete affine system over Q and reports either an exact
Fredholm inconsistency certificate or one rational lift and its Hamming-two
residual ledger.

The exact outcome is frozen by
``verify_h3_pure_packet_hamming_one_fredholm_obstruction.py``.
"""

from __future__ import annotations

from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json


SITES = tuple(range(6))
COLORS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
MATCHING = frozenset(((0, 1), (2, 3), (4, 5)))

D = (
    (Q(0), Q(1), Q(0)),
    (Q(0), Q(0), Q(1)),
    (Q(1), Q(0), Q(0)),
)
P = (
    (Q(1), Q(1), Q(0)),
    (Q(1), Q(0), Q(0)),
    (Q(1), Q(0), Q(1)),
    (Q(1), Q(0), Q(0)),
    (Q(1), Q(0), Q(0)),
    (Q(1), Q(0), Q(0)),
)
S_BY_COLOR = (
    (
        (Q(2), Q(-1), Q(1)),
        (Q(0), Q(0), Q(-1)),
        (Q(0), Q(0), Q(0)),
        (Q(-1), Q(0), Q(0)),
        (Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(0)),
    ),
    (
        (Q(1), Q(-2), Q(1)),
        (Q(0), Q(1), Q(-1)),
        (Q(0), Q(0), Q(0)),
        (Q(-1), Q(0), Q(0)),
        (Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(0)),
    ),
    (
        (Q(1), Q(1), Q(0)),
        (Q(0), Q(0), Q(-1)),
        (Q(0), Q(1), Q(0)),
        (Q(-1), Q(0), Q(1)),
        (Q(0), Q(0), Q(0)),
        (Q(0), Q(-3), Q(0)),
    ),
)

CROSS_KEYS = tuple(
    (left, right, left_color, right_color)
    for left, right in EDGES
    for left_color, right_color in product(COLORS, repeat=2)
    if left_color != right_color
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


@lru_cache(maxsize=None)
def matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(remainder):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


def q_entry(cross, left, right, left_color, right_color):
    if left > right:
        left, right = right, left
        left_color, right_color = right_color, left_color
    if left_color == right_color:
        return Q((left, right) in MATCHING)
    return cross.get((left, right, left_color, right_color), Q(0))


def hafnian(cross, word, vertices=SITES):
    total = Q(0)
    for matching in matchings(tuple(vertices)):
        value = Q(1)
        for left, right in matching:
            value *= q_entry(cross, left, right, word[left], word[right])
        total += value
    return total


def response(cross, row, column, word, stars=S_BY_COLOR):
    total = Q(0)
    for left, right in EDGES:
        value = (
            P[left][row] * stars[word[right]][right][column]
            + P[right][row] * stars[word[left]][left][column]
        )
        if not value:
            continue
        complement = tuple(site for site in SITES if site not in (left, right))
        total += value * hafnian(cross, word, complement)
    return total


def residual(cross, row, column, word, stars=S_BY_COLOR):
    value = D[row][column] * hafnian(cross, word)
    value += response(cross, row, column, word, stars)
    value -= Q(row == column and all(color == row for color in word))
    return value


def hamming_words(distance):
    words = set()
    for base in COLORS:
        for sites in combinations(SITES, distance):
            for defects in product(tuple(color for color in COLORS if color != base), repeat=distance):
                word = [base] * len(SITES)
                for site, color in zip(sites, defects, strict=True):
                    word[site] = color
                words.add(tuple(word))
    return tuple(sorted(words))


def build_linear_system(stars=S_BY_COLOR):
    equations = []
    labels = []
    zero = {}
    for word in hamming_words(1):
        for row, column in product(COLORS, repeat=2):
            constant = residual(zero, row, column, word, stars)
            coefficients = []
            for key in CROSS_KEYS:
                coefficients.append(
                    residual({key: Q(1)}, row, column, word, stars) - constant
                )
            if constant or any(coefficients):
                equations.append(coefficients + [-constant])
                labels.append((row, column, word))
    return equations, labels


def rref_with_certificate(augmented):
    rows = len(augmented)
    columns = len(augmented[0]) - 1
    work = [list(map(Q, row)) for row in augmented]
    provenance = [
        [Q(index == other) for other in range(rows)]
        for index in range(rows)
    ]
    pivots = []
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        provenance[pivot_row], provenance[pivot] = provenance[pivot], provenance[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        provenance[pivot_row] = [entry / value for entry in provenance[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
            provenance[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(provenance[row], provenance[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break

    inconsistent = next(
        (row for row in range(rows)
         if not any(work[row][:columns]) and work[row][columns]),
        None,
    )
    if inconsistent is not None:
        return {
            "consistent": False,
            "rank": len(pivots),
            "certificate": provenance[inconsistent],
            "constant": work[inconsistent][columns],
        }

    solution = [Q(0)] * columns
    for row, pivot in enumerate(pivots):
        solution[pivot] = work[row][columns]
    return {
        "consistent": True,
        "rank": len(pivots),
        "nullity": columns - len(pivots),
        "solution": solution,
    }


def rational_string(value):
    value = Q(value)
    return (str(value.numerator) if value.denominator == 1
            else f"{value.numerator}/{value.denominator}")


def main():
    require(len(CROSS_KEYS) == 90, "cross-q variable count changed")
    system, labels = build_linear_system()
    solved = rref_with_certificate(system)

    ledger = {
        "variables": len(CROSS_KEYS),
        "nonzero_hamming_one_equations": len(system),
        "consistent": solved["consistent"],
        "rank": solved["rank"],
    }
    if not solved["consistent"]:
        certificate = solved["certificate"]
        support = [
            (labels[index], rational_string(value))
            for index, value in enumerate(certificate)
            if value
        ]
        # Recheck the Fredholm certificate directly against the unreduced
        # affine matrix.
        for column in range(len(CROSS_KEYS)):
            require(sum((certificate[row] * system[row][column]
                         for row in range(len(system))), Q(0)) == 0,
                    "Fredholm certificate misses a q column")
        constant = sum(
            (certificate[row] * system[row][-1]
             for row in range(len(system))), Q(0)
        )
        require(constant == solved["constant"] and constant,
                "Fredholm certificate lost its unit")
        ledger.update({
            "certificate_support": len(support),
            "certificate_constant": rational_string(constant),
            "certificate": [
                {
                    "row": row,
                    "column": column,
                    "word": "".join(map(str, word)),
                    "weight": weight,
                }
                for ((row, column, word), weight) in support
            ],
        })
    else:
        cross = {
            key: value for key, value in zip(CROSS_KEYS, solved["solution"], strict=True)
            if value
        }
        hamming_two_residuals = []
        for word in hamming_words(2):
            for row, column in product(COLORS, repeat=2):
                value = residual(cross, row, column, word)
                if value:
                    hamming_two_residuals.append((row, column, word, value))
        ledger.update({
            "nullity": solved["nullity"],
            "solution_support": len(cross),
            "hamming_two_residuals": len(hamming_two_residuals),
            "first_hamming_two_residuals": [
                {
                    "row": row,
                    "column": column,
                    "word": "".join(map(str, word)),
                    "value": rational_string(value),
                }
                for row, column, word, value in hamming_two_residuals[:20]
            ],
        })

    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    print("h3 pure-packet cross-q Hamming-one lift analysis")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

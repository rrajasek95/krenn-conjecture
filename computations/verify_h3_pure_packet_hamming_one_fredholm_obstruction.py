#!/usr/bin/env python3
"""Exact five-row Fredholm obstruction over the pure-nine packet.

This does not prove the general h=3 tangent-or-clean theorem.  It proves
that the exact nonclean pure-nine family from
``verify_h3_pure_nine_rank_two_hafnian_update_boundary.py`` cannot be
completed even through the Hamming-one rows by adding arbitrary ordered
cross-colour q cells.
"""

from fractions import Fraction as Q
from hashlib import sha256
import json

import analyze_h3_pure_packet_cross_q_hamming_one_lift as A


CERTIFICATE = (
    ((0, 2, (0, 0, 2, 0, 0, 0)), Q(1)),
    ((1, 0, (0, 0, 2, 0, 0, 0)), Q(1)),
    ((0, 1, (0, 2, 0, 0, 0, 0)), Q(-1)),
    ((0, 2, (0, 2, 0, 0, 0, 0)), Q(-1)),
    ((0, 0, (0, 2, 2, 2, 2, 2)), Q(-1)),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def stars(parameter):
    answer = [[list(row) for row in colour] for colour in A.S_BY_COLOR]
    answer[2][4][1] = Q(parameter)
    answer[2][5][1] = Q(-3) - Q(parameter)
    return tuple(tuple(tuple(row) for row in colour) for colour in answer)


def check_certificate(parameter):
    current_stars = stars(parameter)
    system, labels = A.build_linear_system(current_stars)
    index = {label: position for position, label in enumerate(labels)}
    weights = [Q(0)] * len(system)
    for label, weight in CERTIFICATE:
        require(label in index, ("certificate row disappeared", parameter, label))
        weights[index[label]] = weight

    for column in range(len(A.CROSS_KEYS)):
        value = sum(
            (weights[row] * system[row][column] for row in range(len(system))),
            Q(0),
        )
        require(value == 0, ("cross-q column survived", parameter, column, value))

    augmented_constant = sum(
        (weights[row] * system[row][-1] for row in range(len(system))),
        Q(0),
    )
    require(augmented_constant == 1,
            ("Fredholm unit moved", parameter, augmented_constant))

    solved = A.rref_with_certificate(system)
    require(not solved["consistent"] and solved["rank"] == 86,
            ("affine-system rank moved", parameter, solved))

    # The weighted sum of the affine residuals is therefore -1.  The
    # dependence on the family parameter is affine, so checking 0 and 1
    # certifies the displayed identity over Q[t].
    return len(system), solved["rank"]


def main():
    results = tuple(check_certificate(parameter) for parameter in (0, 1))
    require(results == ((209, 86), (213, 86)),
            ("Hamming-one equation ledger moved", results))

    # The family stays good: this fixed 3x3 minor of the varying second
    # colour-2 star is identically one.
    for parameter in (Q(0), Q(1)):
        current = stars(parameter)[2]
        minor = (
            current[0][0]
            * (current[1][1] * current[2][2] - current[1][2] * current[2][1])
            - current[0][1]
            * (current[1][0] * current[2][2] - current[1][2] * current[2][0])
            + current[0][2]
            * (current[1][0] * current[2][1] - current[1][1] * current[2][0])
        )
        require(minor == 1, ("good-star minor moved", parameter, minor))

    ledger = {
        "cross_q_variables": len(A.CROSS_KEYS),
        "family_parameter_checks": [0, 1],
        "hamming_one_equation_counts": [result[0] for result in results],
        "coefficient_ranks": [result[1] for result in results],
        "certificate_support": [
            {
                "row": row,
                "column": column,
                "word": "".join(map(str, word)),
                "weight": int(weight),
            }
            for ((row, column, word), weight) in CERTIFICATE
        ],
        "weighted_residual": -1,
        "conclusion": "no Hamming-one lift over Q[t]",
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    expected = "8c2608baa5435bd20b90f39f9d16b33431dd00f7b0549e433c435130867743e8"
    require(digest == expected, ("ledger changed", digest, ledger))
    print("h=3 pure-nine Hamming-one Fredholm obstruction: PASS")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

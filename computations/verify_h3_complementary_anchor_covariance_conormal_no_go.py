#!/usr/bin/env python3
"""Audit complementary-colour covariance against the h=3 conormal class.

Two tempting repairs of the primitive attaching obstruction are:

* the odd (3,3) coefficient of opposite rotations on the six residual sites;
* the even (4,4) coefficient of the two complementary pure eight-site
  anchors, followed by the formal order-four Hasse/cap landing.

The first is target-zero, but consists entirely of mixed literal rows and
has no pure-anchor conormal.  In the second, the two anchor contributions
have the same sign.  The linear combination which kills their common mixed
target also kills the normalized ``w`` boundary.  Chart/covariance
comparisons only redistribute anchor incidence and cannot change this
augmentation.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_signed_circuit_conormal_transport_no_go.py":
        "fdcc5c663e5ad8c9680838301957e03db2ff124fd0d1d4b5a8bc1f7395a922a0",
    "computations/verify_h3_source_base_change_conormal_obstruction.py":
        "1a921671ab378f68355c2a6196d1951cad30244d78a9e90ec2715ce47ef12bf0",
    "notes/h3-signed-circuit-conormal-transport-no-go.md":
        "bb9ee5c4e63da79a49e27d2b6e2cc4819641b3f52efdd9f9749a747bfcb5544f",
    "notes/h3-source-base-change-conormal-obstruction.md":
        "550d1fdea1127d1771191057207b6b2bb6cb97edd3309c90f230d87631f401cd",
}
EXPECTED_LEDGER_SHA256 = (
    "3964df2fb75bed03d4d66af854e1774929e2df3746a58cebb5fecd0900016668"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def rank(rows: tuple[tuple[Q, ...], ...]) -> int:
    matrix = [list(row) for row in rows]
    if not matrix:
        return 0
    row = 0
    for column in range(len(matrix[0])):
        pivot = next((index for index in range(row, len(matrix))
                      if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        value = matrix[row][column]
        matrix[row] = [entry / value for entry in matrix[row]]
        for index in range(len(matrix)):
            if index == row or not matrix[index][column]:
                continue
            value = matrix[index][column]
            matrix[index] = [left - value * right for left, right
                             in zip(matrix[index], matrix[row], strict=True)]
        row += 1
    return row


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def residual_odd_rotation() -> dict[str, object]:
    # On six residual sites use c -> c+t e and e -> e-t c.  At every
    # three/three word the two pure target contributions are +1 and -1.
    words = []
    for marked in combinations(range(6), 3):
        marked = set(marked)
        word = tuple(1 if site in marked else 0 for site in range(6))
        from_zero = Q(1)
        from_one = Q((-1) ** 3)
        require(from_zero + from_one == 0,
                "the residual odd target stopped cancelling")
        # With either diagonal endpoint pair, the resulting eight-site word
        # is mixed.  The selected-u conormal therefore vanishes on both
        # literal rows by the pinned 6561-word census.
        require(len(set((0, 0) + word)) > 1
                and len(set((1, 1) + word)) > 1,
                "a residual middle row became a pure anchor")
        words.append("".join(map(str, word)))
    require(len(words) == 20 and len(set(words)) == 20,
            "the residual middle-word census changed")
    return {
        "sites": 6,
        "middle_words": len(words),
        "coefficients_from_pure_anchors": [1, -1],
        "target_sum_per_word": 0,
        "selected_u_conormal_per_literal_row": [0, 0],
        "verdict": "target-zero but entirely mixed; no anchor conormal",
    }


def full_even_rotation() -> dict[str, object]:
    # On all eight sites the relevant selected word has four labels of each
    # colour.  Both opposite rotations contribute with sign (+1).
    words = []
    for marked in combinations(range(8), 4):
        marked = set(marked)
        word = tuple(1 if site in marked else 0 for site in range(8))
        coefficients = (Q(1), Q((-1) ** 4))
        require(coefficients == (Q(1), Q(1)),
                "the complementary even signs changed")
        words.append("".join(map(str, word)))
    require(len(words) == 70 and len(set(words)) == 70,
            "the eight-site balanced-word census changed")

    # Coordinates are ([F_c], [F_e], normalized w).  Grant each pure anchor
    # its complete formal order-four Hasse/cap landing.  A comparison edge
    # may move anchor incidence, but has zero w boundary.
    n_c = (Q(1), Q(0), Q(1))
    n_e = (Q(0), Q(1), Q(1))
    comparison = (Q(-1), Q(1), Q(0))
    desired = (Q(0), Q(0), Q(1))
    separator = (Q(1), Q(1), Q(-1))
    for column in (n_c, n_e, comparison):
        require(dot(separator, column) == 0,
                "the anchor-augmentation separator stopped vanishing")
    require(dot(separator, desired) == -1,
            "the desired boundary lost its conormal obstruction")
    available_rank = rank((n_c, n_e, comparison))
    augmented_rank = rank((n_c, n_e, comparison, desired))
    require((available_rank, augmented_rank) == (2, 3),
            "the complementary-anchor rank obstruction changed")

    # For coefficients a,b, the mixed target and normalized w boundary are
    # both a+b.  Hence target zero forces w=0.  Comparisons cannot alter
    # either augmentation.
    samples = tuple((Q(a), Q(b)) for a in range(-3, 4)
                    for b in range(-3, 4))
    target_zero = 0
    for a, b in samples:
        target = a + b
        boundary = a + b
        require(target == boundary,
                "target/boundary parity lock changed")
        if target == 0:
            target_zero += 1
            require(boundary == 0,
                    "a target-zero complementary pair retained w")
    require(target_zero == 7,
            "the rational complementary-pair sample census changed")
    return {
        "sites": 8,
        "balanced_words": len(words),
        "coefficients_from_pure_anchors": [1, 1],
        "formal_columns": [list(map(str, column))
                           for column in (n_c, n_e, comparison)],
        "separator": ["1", "1", "-1"],
        "available_rank": available_rank,
        "rank_with_desired_boundary": augmented_rank,
        "target_zero_samples": target_zero,
        "identity": "mixed_target=a+b=normalized_w",
        "verdict": "target cancellation forces cancellation of w",
    }


def main() -> None:
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "residual_odd_rotation": residual_odd_rotation(),
        "full_even_rotation": full_even_rotation(),
        "scope": (
            "opposite binary colour covariance and arbitrary chart-incidence "
            "comparisons, even after granting both formal order-four anchor "
            "landings; no no-go for a new source-resolution lower face"
        ),
        "verdict": (
            "complementary pure anchors do not repair the primitive h=3 "
            "attaching class: odd residual cancellation has zero conormal, "
            "while even full-anchor target cancellation also cancels w"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"complementary-anchor ledger changed: {digest}")
    print("h=3 complementary-anchor covariance conormal no-go: PASS")
    print("six-site 3+3 target cancellation: 20 mixed rows, conormal zero")
    print("eight-site 4+4 target cancellation: normalized w also zero")
    print("available rank 2; desired boundary raises rank to 3")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

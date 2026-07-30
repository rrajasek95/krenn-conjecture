#!/usr/bin/env python3
"""Lightweight exact audits for the full-nine selector normal form."""

from itertools import product
from random import Random


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(left, right, modulus):
    return sum(a * b for a, b in zip(left, right)) % modulus


def mat_vec(matrix, vector, modulus):
    return tuple(
        sum(matrix[3 * row + column] * vector[column] for column in range(3))
        % modulus
        for row in range(3)
    )


def bilinear(matrix, left, right, modulus):
    return dot(left, mat_vec(matrix, right, modulus), modulus)


def matrix_rank(matrix, modulus):
    rows = [list(matrix[3 * row : 3 * row + 3]) for row in range(3)]
    rank = 0
    for column in range(3):
        pivot = next(
            (
                row
                for row in range(rank, 3)
                if rows[row][column] % modulus
            ),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column] % modulus, -1, modulus)
        rows[rank] = [inverse * value % modulus for value in rows[rank]]
        for row in range(3):
            if row == rank:
                continue
            multiple = rows[row][column] % modulus
            if multiple:
                rows[row] = [
                    (left - multiple * right) % modulus
                    for left, right in zip(rows[row], rows[rank])
                ]
        rank += 1
    return rank


def outer(left, right, modulus):
    return tuple(
        left[row] * right[column] % modulus
        for row in range(3)
        for column in range(3)
    )


def add(left, right, modulus):
    return tuple((a + b) % modulus for a, b in zip(left, right))


def scale(value, matrix, modulus):
    return tuple(value * entry % modulus for entry in matrix)


def audit_irreducible_classifier():
    """Over F2, Q_d is contained in Q_N iff N is in the line of d."""
    modulus = 2
    vectors = tuple(
        vector for vector in product(range(modulus), repeat=3) if any(vector)
    )
    matrices = tuple(product(range(modulus), repeat=9))
    direct_blocks = 0
    comparisons = 0
    zero = (0,) * 9
    for direct in matrices:
        if matrix_rank(direct, modulus) < 2:
            continue
        isotropic = tuple(
            (left, right)
            for left in vectors
            for right in vectors
            if bilinear(direct, left, right, modulus) == 0
        )
        for candidate in matrices:
            vanishes = all(
                bilinear(candidate, left, right, modulus) == 0
                for left, right in isotropic
            )
            proportional = candidate in (zero, direct)
            check(
                vanishes == proportional,
                "rank-at-least-two bilinear classifier failed",
            )
            comparisons += 1
        direct_blocks += 1
    return direct_blocks, comparisons


def audit_rank_one_rulings():
    modulus = 2
    vectors = tuple(
        vector for vector in product(range(modulus), repeat=3) if any(vector)
    )
    matrices = tuple(product(range(modulus), repeat=9))
    checks = 0
    for factor in vectors:
        hyperplane = tuple(
            vector for vector in vectors if dot(factor, vector, modulus) == 0
        )
        left_aligned = {
            outer(factor, row, modulus)
            for row in product(range(modulus), repeat=3)
        }
        right_aligned = {
            outer(column, factor, modulus)
            for column in product(range(modulus), repeat=3)
        }
        for candidate in matrices:
            left_zero = all(
                bilinear(candidate, left, right, modulus) == 0
                for left in hyperplane
                for right in vectors
            )
            right_zero = all(
                bilinear(candidate, left, right, modulus) == 0
                for left in vectors
                for right in hyperplane
            )
            check(
                left_zero == (candidate in left_aligned),
                "left-ruling classifier failed",
            )
            check(
                right_zero == (candidate in right_aligned),
                "right-ruling classifier failed",
            )
            checks += 2
    return checks


def audit_target_activity():
    modulus = 2
    vectors = tuple(
        vector for vector in product(range(modulus), repeat=3) if any(vector)
    )
    matrices = tuple(product(range(modulus), repeat=9))
    checks = 0
    for direct in matrices:
        for target in range(3):
            active = any(
                left[target]
                and right[target]
                and bilinear(direct, left, right, modulus) == 0
                for left in vectors
                for right in vectors
            )
            unit = tuple(
                int(row == target and column == target)
                for row in range(3)
                for column in range(3)
            )
            obstructed = direct == unit  # the sole nonzero scalar in F2
            check(active == (not obstructed), "target-activity criterion failed")
            checks += 1
    return checks


def audit_transition_identity():
    modulus = 5
    rng = Random(20260730)
    checks = 0
    for _ in range(300):
        direct = tuple(rng.randrange(modulus) for _ in range(9))
        left = tuple(rng.randrange(modulus) for _ in range(3))
        right = tuple(rng.randrange(modulus) for _ in range(3))
        value = bilinear(direct, left, right, modulus)
        if value:
            # Make the rank-one functional direct-zero exactly in the field.
            image = mat_vec(direct, right, modulus)
            pivot = next((index for index, entry in enumerate(image) if entry), None)
            if pivot is None:
                continue
            adjusted = list(left)
            adjusted[pivot] = (
                adjusted[pivot]
                - value * pow(image[pivot], -1, modulus)
            ) % modulus
            left = tuple(adjusted)
        check(
            bilinear(direct, left, right, modulus) == 0,
            "failed to construct a direct-zero functional",
        )

        forward = tuple(rng.randrange(modulus) for _ in range(9))
        backward = tuple(rng.randrange(modulus) for _ in range(9))
        edge_value = rng.randrange(modulus)
        curvature_forward = add(
            scale(edge_value, direct, modulus),
            scale(-1, forward, modulus),
            modulus,
        )
        curvature_backward = add(
            scale(edge_value, direct, modulus),
            scale(-1, backward, modulus),
            modulus,
        )
        coefficient = bilinear(add(forward, backward, modulus), left, right, modulus)
        detected = -(
            bilinear(curvature_forward, left, right, modulus)
            + bilinear(curvature_backward, left, right, modulus)
        ) % modulus
        check(coefficient == detected, "transition relocation identity failed")
        if coefficient:
            check(
                bilinear(curvature_forward, left, right, modulus)
                or bilinear(curvature_backward, left, right, modulus),
                "nonzero cap coefficient detected no transition",
            )
        checks += 1
    return checks


def main():
    direct_blocks, comparisons = audit_irreducible_classifier()
    ruling_checks = audit_rank_one_rulings()
    target_checks = audit_target_activity()
    transition_checks = audit_transition_identity()
    print(
        "rank-at-least-two bilinear classifier: PASS "
        f"({direct_blocks} blocks, {comparisons} comparisons)"
    )
    print(f"rank-one ruling classifiers: PASS ({ruling_checks})")
    print(f"prescribed-target activity: PASS ({target_checks})")
    print(f"same-edge transition identity: PASS ({transition_checks})")


if __name__ == "__main__":
    main()

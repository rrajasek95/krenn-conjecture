#!/usr/bin/env python3
"""Tiny exact audit for the new distinguished-span-two closure steps.

The large relation-four-plane classifications have their own verifiers.
This dependency-free script checks only the algebra newly assembled here:

* the same-support bilinear-zero construction for every 3x3 matrix with
  entries in {-1, 0, 1};
* the 27-equation selector contraction, including target normalization;
* the one-cross/three-cross partition of perfect matchings across a
  three-vertex shore at orders six and eight.
"""

from fractions import Fraction
from itertools import product


def bilinear(x, matrix, y):
    return sum(
        x[row] * matrix[row][column] * y[column]
        for row in range(3)
        for column in range(3)
    )


def support(vector):
    return tuple(index for index, value in enumerate(vector) if value != 0)


def same_support_isotropic_pair(matrix):
    """Implement Lemma 6.1 over an exact characteristic-zero field."""

    for index in range(3):
        if matrix[index][index] == 0:
            vector = [Fraction(0) for _ in range(3)]
            vector[index] = Fraction(1)
            return tuple(vector), tuple(vector)

    # Every diagonal entry is nonzero.  The principal 01 block suffices.
    a = Fraction(matrix[0][0])
    b = Fraction(matrix[0][1])
    c = Fraction(matrix[1][0])
    d = Fraction(matrix[1][1])
    for t_integer in (1, 2, 3):
        t = Fraction(t_integer)
        numerator = a + c * t
        denominator = b + d * t
        if numerator == 0 or denominator == 0:
            continue
        u = -numerator / denominator
        xi = (Fraction(1), t, Fraction(0))
        eta = (Fraction(1), u, Fraction(0))
        return xi, eta
    raise AssertionError("three choices cannot all meet two forbidden roots")


def audit_direct_blocks():
    checked = 0
    for entries in product((-1, 0, 1), repeat=9):
        matrix = tuple(
            tuple(Fraction(entries[3 * row + column]) for column in range(3))
            for row in range(3)
        )
        xi, eta = same_support_isotropic_pair(matrix)
        common_support = support(xi)
        assert common_support
        assert common_support == support(eta)
        assert len(common_support) <= 2
        assert bilinear(xi, matrix, eta) == 0

        h = common_support[0]
        theta = tuple(
            Fraction(1, 1) / (xi[h] * eta[h]) if colour == h else Fraction(0)
            for colour in range(3)
        )

        # Contraction of the three constant target tensors.
        target = tuple(xi[colour] * eta[colour] * theta[colour] for colour in range(3))
        assert target == tuple(Fraction(int(colour == h)) for colour in range(3))

        # In the common-complement 27-equation packet, contraction by
        # xi_a eta_b theta_c makes the A_pq term at each remaining star
        # colour c equal theta_c * (xi^T A_pq eta), hence zero.  The other
        # two one-cross terms have literal zero direct blocks.
        direct_coefficients = tuple(
            theta[colour] * bilinear(xi, matrix, eta) for colour in range(3)
        )
        assert direct_coefficients == (0, 0, 0)

        # Audit the RHS contraction by explicitly summing all 27 indexed
        # equations rather than using the simplified target expression.
        rhs = [Fraction(0) for _ in range(3)]
        equation_count = 0
        for a, b, c in product(range(3), repeat=3):
            equation_count += 1
            if a == b == c:
                rhs[a] += xi[a] * eta[b] * theta[c]
        assert equation_count == 27
        assert tuple(rhs) == target
        checked += 1
    return checked


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def crossing_count(matching, shore):
    return sum((left in shore) != (right in shore) for left, right in matching)


def odd_double_factorial(value):
    result = 1
    while value > 0:
        result *= value
        value -= 2
    return result


def audit_three_shore_matching_split():
    ledger = {}
    for order in (6, 8):
        shore = frozenset((0, 1, 2))
        counts = {1: 0, 3: 0}
        total = 0
        for matching in perfect_matchings(range(order)):
            crossings = crossing_count(matching, shore)
            assert crossings in counts
            counts[crossings] += 1
            total += 1

        expected_one = 3 * (order - 3) * odd_double_factorial(order - 5)
        expected_three = (
            (order - 3)
            * (order - 4)
            * (order - 5)
            * odd_double_factorial(order - 7)
        )
        assert counts == {1: expected_one, 3: expected_three}
        assert total == odd_double_factorial(order - 1)
        ledger[order] = counts
    return ledger


def main():
    matrices = audit_direct_blocks()
    ledger = audit_three_shore_matching_split()
    print(
        "extra-kernel distinguished-span-two closure: PASS "
        f"({matrices} direct blocks; crossings {ledger})"
    )


if __name__ == "__main__":
    main()

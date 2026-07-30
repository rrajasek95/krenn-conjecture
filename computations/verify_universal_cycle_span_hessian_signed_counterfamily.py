#!/usr/bin/env python3
"""Exact lightweight audit of the signed universal-cycle counterfamily."""

from fractions import Fraction
from itertools import combinations


if not __debug__:
    raise RuntimeError("run without -O: optimized mode is outside this audit protocol")


VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
INDEX = {edge: index for index, edge in enumerate(EDGES)}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def vector(entries):
    return [Fraction(entries.get(edge, 0)) for edge in EDGES]


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def matvec(matrix, value):
    return [dot(row, value) for row in matrix]


def hessian(q):
    matrix = []
    universe = set(VERTICES)
    for first in EDGES:
        row = []
        for second in EDGES:
            remainder = universe.difference(first).difference(second)
            row.append(
                q[INDEX[tuple(sorted(remainder))]]
                if first[0] not in second and first[1] not in second
                else Fraction(0)
            )
        matrix.append(row)
    return matrix


def matching_products(four_set):
    a, b, c, d = four_set
    return (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))


def derivative(q, w, matching):
    first, second = matching
    return q[INDEX[first]] * w[INDEX[second]] + q[INDEX[second]] * w[INDEX[first]]


def matching_gradient(q, matching):
    first, second = matching
    result = [Fraction(0)] * len(EDGES)
    result[INDEX[first]] = q[INDEX[second]]
    result[INDEX[second]] = q[INDEX[first]]
    return result


def audit_separator(q, w, label):
    edge_01 = vector({(0, 1): 1})
    kernel = [a - b for a, b in zip(w, edge_01)]
    matrix = hessian(q)
    require(
        matrix == [list(column) for column in zip(*matrix)],
        f"{label}: Hessian not symmetric",
    )
    require(
        matvec(matrix, kernel) == [Fraction(0)] * len(EDGES),
        f"{label}: kernel certificate failed",
    )

    common_values = {}
    cycle_count = 0
    for four_set in combinations(VERTICES, 4):
        matchings = matching_products(four_set)
        values = [derivative(q, w, matching) for matching in matchings]
        require(
            values[0] == values[1] == values[2],
            f"{label}: cycle mismatch on {four_set}",
        )
        expected = (
            q[INDEX[tuple(vertex for vertex in four_set if vertex not in (0, 1))]] / 3
            if 0 in four_set and 1 in four_set
            else Fraction(0)
        )
        require(
            values[0] == expected,
            f"{label}: wrong common value on {four_set}",
        )
        common_values[four_set] = values[0]

        gradients = [matching_gradient(q, matching) for matching in matchings]
        for gradient in gradients[1:]:
            normal = [a - b for a, b in zip(gradients[0], gradient)]
            require(
                dot(normal, w) == 0,
                f"{label}: separator misses cycle on {four_set}",
            )
            cycle_count += 1
    require(cycle_count == 30, f"{label}: incomplete cycle-span audit")
    return common_values


def main():
    q = vector(
        {
            (0, 2): 1, (0, 3): 1, (0, 4): 1, (0, 5): 1,
            (1, 2): 1, (1, 3): 1, (1, 4): 1, (1, 5): 1,
            (2, 3): 6, (4, 5): -6,
        }
    )
    w = vector(
        {
            (0, 1): Fraction(1, 3),
            (0, 2): 1, (0, 3): 1, (0, 4): -1, (0, 5): -1,
            (1, 2): 1, (1, 3): 1, (1, 4): -1, (1, 5): -1,
            (2, 3): 6, (4, 5): 6,
        }
    )
    edge_01 = vector({(0, 1): 1})
    kernel = [a - b for a, b in zip(w, edge_01)]

    complement_hafnian = sum(
        q[INDEX[first]] * q[INDEX[second]]
        for first, second in matching_products((2, 3, 4, 5))
    )
    require(complement_hafnian == -36, "wrong complementary hafnian")
    common_values = audit_separator(q, w, "integral packet")

    # A second, unequal-spoke specialization audits all signs and both product
    # constraints in the parameter family from the note.
    r = Fraction(2)
    family_entries = {
        (0, 2): Fraction(2), (1, 3): Fraction(3),
        (0, 3): Fraction(1), (1, 2): Fraction(6),
        (0, 4): Fraction(2), (1, 5): Fraction(5),
        (0, 5): Fraction(1), (1, 4): Fraction(10),
    }
    require(
        family_entries[(0, 2)] * family_entries[(1, 3)]
        == family_entries[(0, 3)] * family_entries[(1, 2)],
        "A-spoke product constraint failed",
    )
    require(
        family_entries[(0, 4)] * family_entries[(1, 5)]
        == family_entries[(0, 5)] * family_entries[(1, 4)],
        "B-spoke product constraint failed",
    )
    family_entries[(2, 3)] = 6 * r * family_entries[(0, 2)] * family_entries[(1, 3)]
    family_entries[(4, 5)] = -6 * r * family_entries[(0, 4)] * family_entries[(1, 5)]
    family_q = vector(family_entries)
    family_w_entries = {(0, 1): Fraction(1, 3)}
    for pair in ((0, 2), (0, 3), (1, 2), (1, 3), (2, 3)):
        family_w_entries[pair] = r * family_entries[pair]
    for pair in ((0, 4), (0, 5), (1, 4), (1, 5), (4, 5)):
        family_w_entries[pair] = -r * family_entries[pair]
    family_w = vector(family_w_entries)
    audit_separator(family_q, family_w, "unequal-spoke family packet")
    family_hafnian = sum(
        family_q[INDEX[first]] * family_q[INDEX[second]]
        for first, second in matching_products((2, 3, 4, 5))
    )
    require(family_hafnian == -8640, "family cofactor mismatch")
    require([3 * value for value in kernel] == vector(
        {
            (0, 1): -2,
            (0, 2): 3, (0, 3): 3, (0, 4): -3, (0, 5): -3,
            (1, 2): 3, (1, 3): 3, (1, 4): -3, (1, 5): -3,
            (2, 3): 18, (4, 5): 18,
        }
    ), "integral kernel vector mismatch")

    require(common_values[(0, 1, 2, 3)] == 2, "A-block value mismatch")
    require(common_values[(0, 1, 4, 5)] == -2, "B-block value mismatch")
    print("universal cycle-span signed counterfamily: PASS")
    print("  complementary hafnian: -36")
    print("  all 15 four-set cycle equalities: PASS")
    print("  unequal-spoke family specialization: PASS")
    print("  H_q (w-e_01) = 0 and w in C_q^perp: PASS")
    print("  therefore every lambda in C_q intersect im(H_q) has lambda_01 = 0")


if __name__ == "__main__":
    main()

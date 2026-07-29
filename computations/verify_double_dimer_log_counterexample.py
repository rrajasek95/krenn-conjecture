#!/usr/bin/env python3
"""Counterexample to inferring the all-subset loop gas from the full GHZ tensor.

Start from the exact signed Delta_(6,2) cancellation gadget and add an
arbitrary rank-two tensor on edge 05 (zero-based 04).  Its four-vertex
hafnian cofactor is identically zero, so the full six-site tensor is
unchanged.  The induced two-site double-dimer coefficient on 04 is however
2 det(I)=2, and therefore the square-free logarithm has a proper connected
term despite all proper coefficients of the full six-site tensor vanishing.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

from verify_binary_spinflip_cycle_identity import perfect_matchings


N = 6
VERTICES = tuple(range(N))
ZERO = ((0, 0), (0, 0))

# Zero-based form of computations/verify_cancellation_example.py.
MATRICES = {
    (0, 1): ((1, 0), (1, 0)),
    (2, 3): ((1, 0), (0, 0)),
    (4, 5): ((1, 0), (0, 0)),
    (0, 2): ((0, 0), (-1, 0)),
    (1, 3): ((1, 0), (0, 0)),
    (0, 5): ((0, 0), (0, 1)),
    (1, 2): ((0, 0), (0, 1)),
    (3, 4): ((0, 0), (0, 1)),
    # The added tensor-inactive edge.  Its complement {1,2,3,5} has
    # identically zero matching tensor in the original gadget.
    (0, 4): ((1, 0), (0, 1)),
}


def induced_tensor(vertices):
    vertices = tuple(vertices)
    answer = {}
    for bits in itertools.product((0, 1), repeat=len(vertices)):
        coloring = dict(zip(vertices, bits))
        value = 0
        for matching in perfect_matchings(vertices):
            term = 1
            for edge in matching:
                u, v = edge
                term *= MATRICES.get(edge, ZERO)[coloring[u]][coloring[v]]
            value += term
        answer[bits] = value
    return answer


def spin_flip(tensor):
    return sum(
        (-1) ** sum(bits)
        * value
        * tensor[tuple(1 - bit for bit in bits)]
        for bits, value in tensor.items()
    )


def multiply(left, right):
    answer = {}
    for support_left, value_left in left.items():
        set_left = set(support_left)
        for support_right, value_right in right.items():
            if set_left.isdisjoint(support_right):
                support = tuple(sorted(support_left + support_right))
                answer[support] = answer.get(support, Fraction(0)) + value_left * value_right
    return {support: value for support, value in answer.items() if value}


def square_free_log(series):
    augmentation = dict(series)
    augmentation.pop((), None)
    power = {(): Fraction(1)}
    answer = {}
    for exponent in range(1, N // 2 + 1):
        power = multiply(power, augmentation)
        coefficient = Fraction((-1) ** (exponent + 1), exponent)
        for support, value in power.items():
            answer[support] = answer.get(support, Fraction(0)) + coefficient * value
    return {support: value for support, value in answer.items() if value}


def main():
    complement = induced_tensor((1, 2, 3, 5))
    assert not any(complement.values())

    full = induced_tensor(VERTICES)
    for bits, value in full.items():
        expected = int(not any(bits) or all(bits))
        assert value == expected, (bits, value)

    double_dimer = {(): Fraction(1)}
    for size in range(2, N + 1, 2):
        for support in itertools.combinations(VERTICES, size):
            value = spin_flip(induced_tensor(support))
            if value:
                double_dimer[support] = Fraction(value)

    connected = square_free_log(double_dimer)
    assert double_dimer[(0, 4)] == 2
    assert connected[(0, 4)] == 2
    assert spin_flip(full) == 2

    print("verified full matching tensor remains Delta_(6,2)")
    print("verified inactive edge 04 has zero four-site cofactor")
    print("all-subset double-dimer coefficient D_{04}=2")
    print("square-free log connected coefficient C_{04}=2")
    print(f"nonzero proper connected supports={sum(len(s) < N for s in connected)}")


if __name__ == "__main__":
    main()

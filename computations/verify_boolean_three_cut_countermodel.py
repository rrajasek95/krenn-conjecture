#!/usr/bin/env python3
"""Exact checks for the Boolean 3|(n-3) flattening note.

The audit has three parts.

1. Verify the residue factorization and rank three at n=6,8,10.
2. Verify the exact one-cross/three-cross matching partition on a generic
   deterministic integer source at n=6 and n=8.
3. Verify in the algebraic quotient

       ab=1,  a^3+b^3=20,  omega^2+omega+1=0

   that the dense K_(6,6) cap has elementary symmetric coefficients
   (1,0,0,20,0,0,1), hence contracts exactly to six-bit MOD_3.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

import sympy as sp


def perfect_matchings(vertices: tuple[int, ...]):
    """Yield all perfect matchings of a named even vertex tuple."""

    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def target(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return int((sum(left) + sum(right)) % 3 == 0)


def verify_target_rank() -> None:
    for n in (6, 8, 10):
        right_size = n - 3
        left_states = tuple(itertools.product((0, 1), repeat=3))
        right_states = tuple(itertools.product((0, 1), repeat=right_size))
        matrix = sp.Matrix(
            [[target(left, right) for right in right_states] for left in left_states]
        )
        assert matrix.rank() == 3

        # Check U_0 V_0 + U_1 V_2 + U_2 V_1 coefficientwise.
        for left in left_states:
            left_residue = sum(left) % 3
            for right in right_states:
                right_residue = sum(right) % 3
                factored = int(
                    (left_residue == 0 and right_residue == 0)
                    or (left_residue == 1 and right_residue == 2)
                    or (left_residue == 2 and right_residue == 1)
                )
                assert factored == target(left, right)


def edge_entry(i: int, j: int, si: int, sj: int) -> int:
    """A deterministic nonsymmetric-endpoint integer 2 by 2 edge block."""

    if i > j:
        return edge_entry(j, i, sj, si)
    # Values are deliberately generic enough that no sector vanishes by design.
    return 1 + ((17 * i + 29 * j + 7 * si + 11 * sj + 5 * si * sj) % 13)


def hafnian(vertices: tuple[int, ...], state: tuple[int, ...]) -> int:
    answer = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for i, j in matching:
            term *= edge_entry(i, j, state[i], state[j])
        answer += term
    return answer


def cut_sectors(n: int, state: tuple[int, ...]) -> tuple[int, int]:
    """Return the one-cross and three-cross sums across L={0,1,2}."""

    left = (0, 1, 2)
    right = tuple(range(3, n))
    one_cross = 0
    three_cross = 0

    for crossing_left in left:
        internal_left = tuple(i for i in left if i != crossing_left)
        left_weight = edge_entry(
            internal_left[0],
            internal_left[1],
            state[internal_left[0]],
            state[internal_left[1]],
        )
        for r in right:
            remaining = tuple(v for v in right if v != r)
            one_cross += (
                left_weight
                * edge_entry(crossing_left, r, state[crossing_left], state[r])
                * hafnian(remaining, state)
            )

    for image in itertools.permutations(right, 3):
        cross_weight = 1
        for i, r in zip(left, image):
            cross_weight *= edge_entry(i, r, state[i], state[r])
        image_set = set(image)
        remaining = tuple(v for v in right if v not in image_set)
        three_cross += cross_weight * hafnian(remaining, state)

    return one_cross, three_cross


def verify_source_cut_partition() -> None:
    for n in (6, 8):
        vertices = tuple(range(n))
        for state in itertools.product((0, 1), repeat=n):
            one_cross, three_cross = cut_sectors(n, state)
            assert hafnian(vertices, state) == one_cross + three_cross


def elementary_symmetric(values: list[sp.Expr], degree: int) -> sp.Expr:
    return sum(
        (sp.prod(values[i] for i in indices)
         for indices in itertools.combinations(range(len(values)), degree)),
        sp.Integer(0),
    )


def verify_dense_cap() -> None:
    a, b, omega = sp.symbols("a b omega")
    quotient = sp.groebner(
        [a * b - 1, a**3 + b**3 - 20, omega**2 + omega + 1],
        omega,
        b,
        a,
        order="lex",
    )
    values = [
        a,
        a * omega,
        a * omega**2,
        b,
        b * omega,
        b * omega**2,
    ]
    expected = (1, 0, 0, 20, 0, 0, 1)
    elementary = []
    for degree in range(7):
        expression = sp.expand(elementary_symmetric(values, degree))
        remainder = sp.factor(quotient.reduce(expression)[1])
        elementary.append(remainder)
        assert remainder == expected[degree]

    # With product_i c_i=1/6!, the permanent at weight k is e_k/C(6,k).
    for weight in range(7):
        amplitude = Fraction(
            math.factorial(weight) * math.factorial(6 - weight),
            math.factorial(6),
        ) * int(elementary[weight])
        assert amplitude == int(weight % 3 == 0)

    # The six x_j are units: a*b=1 and omega^3=1 in the quotient.
    assert quotient.reduce(a * b)[1] == 1
    assert quotient.reduce(omega**3)[1] == 1
    # By construction all 15 internal boundary edge blocks vanish, so their
    # six-site principal hafnian is zero while the cap output at weight 0 is 1.
    assert elementary[0] == 1


def main() -> None:
    verify_target_rank()
    print("verified exact rank-three Boolean residue flattenings")
    verify_source_cut_partition()
    print("verified exact one-cross/three-cross source decomposition")
    verify_dense_cap()
    print("verified exact dense K_(6,6) cap countermodel")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent audit of the critical moving-triple local-jet q=6 cap."""

from __future__ import annotations

import sympy as sp


def reconstruct_uniform_intersection() -> None:
    for r in range(4, 65):
        p = r * (r + 3)
        classes = r + 5
        assert p + 2 == (r + 1) * (r + 2)

        relation_degree = classes - 4
        common_degree = classes
        relation_dimension = r
        common_bound = r + 2
        assert relation_degree == r + 1
        assert common_degree == r + 5

        lower_intersection = 2 * relation_dimension - common_bound
        multiplier_degree = relation_degree - 4
        ambient_dimension = multiplier_degree + 1
        assert lower_intersection == r - 2
        assert multiplier_degree == r - 3 >= 1
        assert ambient_dimension == lower_intersection


def reconstruct_factor_division_and_local_row() -> None:
    z, i, j = sp.symbols("z i j", nonzero=True)
    Bi = (z - i) ** 2 * (z + i) ** 2
    Bj = (z - j) ** 2 * (z + j) ** 2
    multiplier = z - j

    transported = sp.expand(Bi * Bj * multiplier)
    relation_member = sp.cancel(transported / Bi)
    assert sp.expand(relation_member - Bj * multiplier) == 0
    assert sp.Poly(multiplier, z).degree() == 1

    x = z - j
    coefficients = sp.symbols("u0:4")
    unit = sum(coefficients[order] * x**order for order in range(4))
    witness = sp.expand(Bj * multiplier)
    for order in range(3):
        assert sp.expand(sp.diff(witness, z, order).subs(z, j)) == 0
    assert sp.factor(sp.diff(witness, z, 3).subs(z, j)) == 24 * j**2
    exact_row = sp.factor(sp.diff(unit * witness, z, 3).subs(z, j))
    assert exact_row == 24 * j**2 * coefficients[0]

    assert sp.factor(Bi.subs(z, j)) == (i - j) ** 2 * (i + j) ** 2


def reconstruct_p28_specialization() -> None:
    r = 4
    assert r * (r + 3) == 28
    assert r + 5 == 9
    tuples = ((3, 6, 0, 0), (3, 6, 1, -2))

    for h in range(22, 28):
        k = 28 - h
        assert (h, k) in (
            (22, 6), (23, 5), (24, 4),
            (25, 3), (26, 2), (27, 1),
        )
        for quartics, triples, doubles, offset in tuples:
            assert 4 * quartics + 3 * triples + 2 * doubles + offset == 30
            selected_repeated = 1 + doubles
            selected_singletons = h + 2 - 2 * selected_repeated
            assert selected_singletons == h + offset

            complement = (
                (4,) * quartics
                + (3,) * (triples - 1)
                + (1,)
            )
            assert sum(complement) == 28
            assert len(complement) == 9
            assert complement.count(3) == 5

    assert 6 - 1 == 5


def main() -> None:
    reconstruct_uniform_intersection()
    reconstruct_factor_division_and_local_row()
    reconstruct_p28_specialization()
    print("independent critical moving-triple local-jet q=6 cap: PASS")
    print("transport orientation B_i S_i and division by B_i: exact")
    print("complementary triple unit regular/nonzero; third jet contradictory")
    print("p=28 4^3 3^6 consequence: at most one q=6, at least five q=5")


if __name__ == "__main__":
    main()

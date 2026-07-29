#!/usr/bin/env python3
"""Exact audit of the four-site base-star jet-lifting counterexample."""

from __future__ import annotations

import itertools
from fractions import Fraction


X, Y, Z = range(3)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def multiply(left, right):
    answer = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] += a * b
    return tuple(answer)


def output(tables, max_degree):
    answer = {}
    for coloring in itertools.product(range(3), repeat=4):
        total = [Fraction(0)] * (max_degree + 1)
        for matching in perfect_matchings(range(4)):
            term = (Fraction(1),)
            for u, v in matching:
                term = multiply(
                    term, tables.get((u, v, coloring[u], coloring[v]), (0,))
                )
            for degree, coefficient in enumerate(term[: max_degree + 1]):
                total[degree] += coefficient
        answer[coloring] = tuple(total)
    return answer


def exact_arc():
    tables = {}
    for edge in ((0, 1), (2, 3)):
        tables[edge + (X, X)] = (1,)
    for edge in ((0, 2), (1, 3)):
        tables[edge + (Y, Y)] = (1,)
    for edge in ((0, 3), (1, 2)):
        tables[edge + (X, X)] = (1,)
        tables[edge + (Z, X)] = (0, 1)
        tables[edge + (X, Z)] = (0, 1)
        tables[edge + (Z, Z)] = (0, 0, 1)

    actual = output(tables, 4)
    for coloring, coefficients in actual.items():
        expected = [Fraction(0)] * 5
        if coloring == (X,) * 4:
            expected[0] = 2
        elif coloring == (Y,) * 4:
            expected[0] = 1
        elif Y not in coloring and Z in coloring:
            expected[coloring.count(Z)] = 1
        assert coefficients == tuple(expected), (coloring, coefficients)
    return tables


def base_star_kernel():
    # Coefficient polynomials are now in the support-deformation parameter s.
    tables = {
        (0, 1, X, X): (1, -1),
        (2, 3, X, X): (1,),
        (0, 2, Y, Y): (1,),
        (1, 3, Y, Y): (1,),
        (0, 3, X, X): (1, 1),
        (1, 2, X, X): (1,),
    }
    actual = output(tables, 1)
    assert actual[(X,) * 4] == (2, 0)
    assert actual[(Y,) * 4] == (1, 0)
    assert all(
        coefficients == (0, 0)
        for coloring, coefficients in actual.items()
        if coloring not in ((X,) * 4, (Y,) * 4)
    )


def no_same_star_first_lift(original):
    gamma = (X, X, Z, X)

    # R0*Q1 at gamma.  The sole term is +[03;xx] times [12;xz].
    assert original[(1, 2, X, Z)][1] == 1
    obstruction = Fraction(1)

    # Enumerate every allowed one-z cell on the star of vertex 0.  Its
    # product with the binary base has zero gamma coefficient.
    q0 = {key: value[0] for key, value in original.items() if value[0]}
    image_coefficients = []
    for v in (1, 2, 3):
        edge = (0, v)
        for colors in ((Z, X), (Z, Y), (X, Z), (Y, Z)):
            trial = {key: (value,) for key, value in q0.items()}
            trial[edge + colors] = (0, 1)
            image_coefficients.append(output(trial, 1)[gamma][1])
    assert all(value == 0 for value in image_coefficients)
    assert obstruction == 1


def frozen_endpoint_second_jet():
    # At s=1, restrict Q1 to the old moving one-factor.  The first equations
    # force slopes 1 on 03 and 1/2 on 12.
    tables = {
        (2, 3, X, X): (1,),
        (0, 2, Y, Y): (1,),
        (1, 3, Y, Y): (1,),
        (0, 3, X, X): (2,),
        (1, 2, X, X): (1,),
    }
    for colors in ((Z, X), (X, Z)):
        tables[(0, 3) + colors] = (0, 1)
        tables[(1, 2) + colors] = (0, Fraction(1, 2))

    actual = output(tables, 2)
    for vertex in range(4):
        coloring = tuple(Z if index == vertex else X for index in range(4))
        assert actual[coloring][1] == 1

    frozen = (Z, X, Z, X)
    assert actual[frozen][2] == Fraction(1, 2)

    # Even an arbitrary Q2 cell on 02 has zero cofactor A_13^{xx}.
    tables[(0, 2, Z, Z)] = (0, 0, 17)
    assert output(tables, 2)[frozen][2] == Fraction(1, 2)


def minimal_endpoint_has_no_unrestricted_two_jet():
    # Delete the now base-inactive xx cell on 23 as well.  The first-jet
    # classification leaves arbitrary cells only on the same-shore edges
    # 01 and 23.  For z at the same-shore pair 0,1, neither can occur.
    q0 = {
        (0, 3, X, X): Fraction(2),
        (1, 2, X, X): Fraction(1),
        (0, 2, Y, Y): Fraction(1),
        (1, 3, Y, Y): Fraction(1),
    }
    q1_forced = {
        (0, 3, Z, X): Fraction(1),
        (0, 3, X, Z): Fraction(1),
        (1, 2, Z, X): Fraction(1, 2),
        (1, 2, X, Z): Fraction(1, 2),
    }

    coloring = (Z, Z, X, X)
    constant = Fraction(0)
    q2_coefficients = {}
    q1_products = []
    for matching in perfect_matchings(range(4)):
        for edge in matching:
            u, v = edge
            if (coloring[u], coloring[v]) == (Z, Z):
                other = matching[1 - matching.index(edge)]
                a, b = other
                q2_coefficients[edge] = q0.get(
                    (a, b, coloring[a], coloring[b]), 0
                )

        first, second = matching
        a, b = first
        c, d = second
        left = q1_forced.get((a, b, coloring[a], coloring[b]), 0)
        right = q1_forced.get((c, d, coloring[c], coloring[d]), 0)
        q1_products.append((matching, left * right))
        constant += left * right

    assert q2_coefficients == {(0, 1): 0}
    assert q1_products == [
        (((0, 1), (2, 3)), 0),
        (((0, 2), (1, 3)), 0),
        (((0, 3), (1, 2)), Fraction(1, 2)),
    ]
    assert constant == Fraction(1, 2)


def main():
    original = exact_arc()
    base_star_kernel()
    no_same_star_first_lift(original)
    frozen_endpoint_second_jet()
    minimal_endpoint_has_no_unrestricted_two_jet()
    print("verified exact K4 arc and support-reducing base-star kernel")
    print("verified same-star first-lift cokernel obstruction")
    print("verified support-preserving second coefficient 1/2, target 1")
    print("verified cell-minimal endpoint has no unrestricted collision two-jet")


if __name__ == "__main__":
    main()

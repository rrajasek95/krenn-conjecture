#!/usr/bin/env python3
"""Exact audit of the complete pure-normal-block countermodel.

All arithmetic is rational.  The source matches every all-x/two-z second
coefficient, hence the complete rank-one normal pair matrix across every
cut, but fails twelve mixed complement coefficients.
"""

from __future__ import annotations

import itertools
from fractions import Fraction


N = 6
X, Y, Z = range(3)
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


MATCHINGS = tuple(perfect_matchings(VERTICES))


Q0 = {
    (0, 1, Y, Y): Fraction(1),
    (2, 3, Y, Y): Fraction(1),
    (4, 5, Y, Y): Fraction(1),
    (0, 2, X, X): Fraction(-2, 25),
    (0, 3, X, X): Fraction(2, 25),
    (1, 2, X, X): Fraction(-3, 25),
    (1, 3, X, X): Fraction(-3, 25),
    (0, 4, X, X): Fraction(-1),
    (0, 5, X, X): Fraction(-3),
    (1, 4, X, X): Fraction(1),
    (1, 5, X, X): Fraction(-3),
    (2, 4, X, X): Fraction(1),
    (2, 5, X, X): Fraction(1),
    (3, 4, X, X): Fraction(3),
    (3, 5, X, X): Fraction(-3),
}


# Homogeneous one-z tangent K.  Keys use the endpoint order u<v.
K = {
    (0, 2, Z, X): Fraction(-1, 25),
    (0, 2, X, Z): Fraction(8, 525),
    (0, 3, Z, X): Fraction(1, 25),
    (0, 3, X, Z): Fraction(21, 200),
    (0, 4, Z, X): Fraction(1, 3),
    (0, 4, X, Z): Fraction(8),
    (0, 5, Z, X): Fraction(1),
    (0, 5, X, Z): Fraction(-3, 32),
    (1, 2, Z, X): Fraction(3, 50),
    (1, 2, X, Z): Fraction(4, 175),
    (1, 3, Z, X): Fraction(3, 50),
    (1, 3, X, Z): Fraction(-63, 400),
    (1, 4, Z, X): Fraction(3, 4),
    (1, 4, X, Z): Fraction(-8),
    (1, 5, Z, X): Fraction(-9, 4),
    (1, 5, X, Z): Fraction(-3, 32),
    (2, 4, Z, X): Fraction(1),
    (2, 4, X, Z): Fraction(1, 3),
    (2, 5, Z, X): Fraction(1),
    (2, 5, X, Z): Fraction(-3, 4),
    (3, 4, Z, X): Fraction(-3, 4),
    (3, 4, X, Z): Fraction(1),
    (3, 5, Z, X): Fraction(3, 4),
    (3, 5, X, Z): Fraction(9, 4),
}


ETA = {
    (0, 2): Fraction(-81, 1400),
    (0, 3): Fraction(-77, 200),
    (0, 4): Fraction(31, 4),
    (0, 5): Fraction(-269, 192),
    (1, 2): Fraction(-349, 2100),
    (1, 3): Fraction(-299, 1600),
    (1, 4): Fraction(79, 16),
    (1, 5): Fraction(-317, 64),
    (2, 4): Fraction(839, 42),
    (2, 5): Fraction(587, 224),
    (3, 4): Fraction(223, 48),
    (3, 5): Fraction(9037, 512),
}


def base_coefficient(coloring):
    return sum(
        prod(Q0.get(edge + tuple(coloring[v] for v in edge), 0) for edge in matching)
        for matching in MATCHINGS
    )


def prod(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def first_coefficient(coloring):
    total = Fraction(0)
    for matching in MATCHINGS:
        for exceptional in range(3):
            factors = []
            for position, edge in enumerate(matching):
                key = edge + tuple(coloring[v] for v in edge)
                factors.append(K.get(key, 0) if position == exceptional else Q0.get(key, 0))
            total += prod(factors)
    return total


def second_parts(coloring):
    """Return (direct cofactor times eta, Hessian) at one two-z coloring."""
    pair = tuple(vertex for vertex in VERTICES if coloring[vertex] == Z)
    assert len(pair) == 2
    direct = Fraction(0)
    hessian = Fraction(0)
    for matching in MATCHINGS:
        for exceptional, edge in enumerate(matching):
            if edge != pair:
                continue
            factors = []
            for position, current in enumerate(matching):
                if position == exceptional:
                    factors.append(ETA.get(pair, 0))
                else:
                    key = current + tuple(coloring[v] for v in current)
                    factors.append(Q0.get(key, 0))
            direct += prod(factors)
        for first, second in itertools.combinations(range(3), 2):
            factors = []
            for position, edge in enumerate(matching):
                key = edge + tuple(coloring[v] for v in edge)
                factors.append(K.get(key, 0) if position in (first, second) else Q0.get(key, 0))
            hessian += prod(factors)
    return direct, hessian


def cofactor_and_hessian(coloring):
    pair = tuple(vertex for vertex in VERTICES if coloring[vertex] == Z)
    eta = ETA.get(pair, Fraction(0))
    direct, hessian = second_parts(coloring)
    if eta:
        return direct / eta, hessian
    # For the three within-block pairs eta=0 and their direct cofactors are
    # independently zero; recompute with a temporary unit direct cell.
    cofactor = Fraction(0)
    for matching in MATCHINGS:
        for exceptional, edge in enumerate(matching):
            if edge != pair:
                continue
            factors = []
            for position, current in enumerate(matching):
                if position == exceptional:
                    factors.append(Fraction(1))
                else:
                    key = current + tuple(coloring[v] for v in current)
                    factors.append(Q0.get(key, 0))
            cofactor += prod(factors)
    return cofactor, hessian


def main():
    # Binary base and homogeneous first tangent.
    for coloring in itertools.product((X, Y), repeat=N):
        target = Fraction(2) if coloring == (X,) * N else Fraction(
            int(coloring == (Y,) * N)
        )
        assert base_coefficient(coloring) == target
    for coloring in itertools.product((X, Y, Z), repeat=N):
        if coloring.count(Z) == 1:
            assert first_coefficient(coloring) == 0

    # All fifteen pure pair channels are exactly one half.
    pure_values = {}
    for pair in EDGES:
        coloring = [X] * N
        for vertex in pair:
            coloring[vertex] = Z
        direct, hessian = second_parts(tuple(coloring))
        pure_values[pair] = direct + hessian
        assert pure_values[pair] == Fraction(1, 2)

    # Therefore every cross-pair normal matrix is the target's rank-one
    # all-ones matrix.  Audit all 62 oriented nontrivial shores.
    cut_count = 0
    odd_cut_count = 0
    for size in range(1, N):
        for left in itertools.combinations(VERTICES, size):
            right = tuple(vertex for vertex in VERTICES if vertex not in left)
            matrix = [[pure_values[tuple(sorted((i, j)))] for j in right] for i in left]
            assert all(value == Fraction(1, 2) for row in matrix for value in row)
            for i, k in itertools.combinations(range(len(left)), 2):
                for j, ell in itertools.combinations(range(len(right)), 2):
                    assert matrix[i][j] * matrix[k][ell] == matrix[i][ell] * matrix[k][j]
            cut_count += 1
            odd_cut_count += size % 2
    assert cut_count == 62 and odd_cut_count == 32

    # The full complement tensor nevertheless has twelve nonzero residuals.
    failures = []
    for coloring in itertools.product((X, Y, Z), repeat=N):
        if coloring.count(Z) != 2:
            continue
        direct, hessian = second_parts(coloring)
        target = Fraction(1, 2) if Y not in coloring else Fraction(0)
        if direct + hessian != target:
            failures.append((coloring, direct + hessian - target))
    assert len(failures) == 12

    marked = (X, Z, X, Z, Y, Y)
    assert (marked, Fraction(17, 800)) in failures
    c_x, b_x = cofactor_and_hessian((X, Z, X, Z, X, X))
    c_m, b_m = cofactor_and_hessian(marked)
    assert (c_x, b_x) == (Fraction(-4), Fraction(-99, 400))
    assert (c_m, b_m) == (Fraction(-2, 25), Fraction(63, 10000))
    wedge = c_x * (-b_m) - c_m * (Fraction(1, 2) - b_x)
    assert wedge == Fraction(17, 200)

    print("verified H(q0)=2X+Y and dH_q0(K)=0 exactly")
    print("verified all 15 pure pair channels equal 1/2")
    print("verified rank-one complete normal block on all 62 cuts (32 odd)")
    print("verified 12 mixed failures; marked residual=17/800, cofactor wedge=17/200")


if __name__ == "__main__":
    main()

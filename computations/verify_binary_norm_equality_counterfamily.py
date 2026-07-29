#!/usr/bin/env python3
"""Exact audits for binary-norm-equality-counterfamily.md."""

from __future__ import annotations

import itertools

import sympy as sp

from verify_binary_spinflip_cycle_identity import perfect_matchings


SQRT_HALF = sp.sqrt(2) / 2


def edge(u, v):
    return tuple(sorted((u, v)))


def uniform_source(n):
    p0 = tuple((2 * k, 2 * k + 1) for k in range(n // 2))
    p0_prime = (edge(0, 2), edge(1, 3)) + p0[2:]
    p1 = tuple(edge(k, k + 1) for k in range(1, n - 1, 2)) + (edge(0, n - 1),)
    cells = {}
    for e in (edge(0, 1), edge(2, 3), edge(0, 2), edge(1, 3)):
        cells[e, 0] = SQRT_HALF
    for e in p0[2:]:
        cells[e, 0] = sp.S.One
    for e in p1:
        cells[e, 1] = sp.S.One
    return (p0, p0_prime, p1), cells


def supported_matchings(n, cells):
    answer = []
    for matching in perfect_matchings(tuple(range(n))):
        colors = []
        value = sp.S.One
        for e in matching:
            choices = [(color, weight) for (f, color), weight in cells.items() if f == e]
            if len(choices) != 1:
                value = 0
                break
            color, weight = choices[0]
            colors.append(color)
            value *= weight
        if value != 0:
            answer.append((matching, tuple(colors), sp.simplify(value)))
    return answer


def scalar_cofactor(n, cells, removed_edge, color):
    vertices = tuple(v for v in range(n) if v not in removed_edge)
    total = sp.S.Zero
    for matching in perfect_matchings(vertices):
        term = sp.S.One
        for e in matching:
            term *= cells.get((e, color), 0)
        total += term
    return sp.simplify(total)


def verify_uniform():
    for n in (4, 6, 8, 10, 12):
        expected, cells = uniform_source(n)
        terms = supported_matchings(n, cells)
        by_matching = {frozenset(term[0]): (term[1], term[2]) for term in terms}
        assert set(by_matching) == {frozenset(matching) for matching in expected}
        assert sorted(value for _, value in by_matching.values()) == [
            sp.Rational(1, 2), sp.Rational(1, 2), sp.S.One
        ]
        color_sets = [set(colors) for colors, _ in by_matching.values()]
        assert sorted(color_sets, key=str) == [
            {0}, {0}, {1}
        ]
        assert sp.simplify(sum(abs(value) ** 2 for value in cells.values())) == n
        assert len(cells) == n + 2

        for v in range(n):
            for color in (0, 1):
                incident = []
                cofactors = []
                for u in range(n):
                    if u == v:
                        continue
                    e = edge(u, v)
                    incident.append(cells.get((e, color), 0))
                    cofactors.append(scalar_cofactor(n, cells, e, color))
                assert sp.simplify(sum(abs(x) ** 2 for x in incident)) == 1
                assert incident == cofactors


def triple_source():
    families = (
        ((edge(0, 1),), ((edge(2, 3), edge(4, 5)), (edge(2, 4), edge(3, 5)))),
        ((edge(3, 4),), ((edge(0, 2), edge(1, 5)), (edge(0, 5), edge(1, 2)))),
        ((edge(2, 5),), ((edge(0, 3), edge(1, 4)), (edge(0, 4), edge(1, 3)))),
    )
    cells = {}
    monochrome = []
    for color, (shared, alternatives) in enumerate(families):
        cells[shared[0], color] = sp.S.One
        for pair in alternatives:
            monochrome.append(frozenset(shared + pair))
            for e in pair:
                cells[e, color] = SQRT_HALF
    return tuple(monochrome), cells


def verify_triple():
    monochrome, cells = triple_source()
    assert len(cells) == 15
    assert {e for e, _ in cells} == set(itertools.combinations(range(6), 2))

    fibers = {}
    for matching in perfect_matchings(tuple(range(6))):
        coloring = [None] * 6
        value = sp.S.One
        matching_colors = []
        for e in matching:
            choices = [(color, weight) for (f, color), weight in cells.items() if f == e]
            assert len(choices) == 1
            color, weight = choices[0]
            matching_colors.append(color)
            value *= weight
            coloring[e[0]] = coloring[e[1]] = color
        fibers.setdefault(tuple(coloring), []).append((frozenset(matching), sp.simplify(value)))

    for pair in itertools.combinations(range(3), 2):
        allowed = [
            (coloring, terms)
            for coloring, terms in fibers.items()
            if set(coloring) <= set(pair)
        ]
        assert len(allowed) == 2
        for coloring, terms in allowed:
            assert len(set(coloring)) == 1
            assert sp.simplify(sum(value for _, value in terms)) == 1
            assert len(terms) == 2

    mixed = [(coloring, terms) for coloring, terms in fibers.items() if len(set(coloring)) == 3]
    assert len(mixed) == 9
    assert all(len(terms) == 1 and terms[0][1] != 0 for _, terms in mixed)
    assert all(tuple(sorted(coloring.count(i) for i in range(3))) == (2, 2, 2) for coloring, _ in mixed)

    assert sp.simplify(sum(abs(value) ** 2 for value in cells.values())) == 9
    for v in range(6):
        for color in range(3):
            incidence = sum(
                abs(value) ** 2
                for (e, c), value in cells.items()
                if c == color and v in e
            )
            assert sp.simplify(incidence) == 1


def main():
    verify_uniform()
    verify_triple()
    print("verified uniform exact n+2-cell binary family for n=4,6,8,10,12")
    print("verified norm squared n, unit port incidence, and zero cofactor gaps")
    print("verified three simultaneous non-Hamilton binary restrictions on K6")
    print("verified nine distinct nonzero genuinely ternary singleton fibers")


if __name__ == "__main__":
    main()

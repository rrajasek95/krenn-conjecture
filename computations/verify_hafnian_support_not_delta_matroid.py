#!/usr/bin/env python3
"""Exact audit that nonzero principal hafnians need not be a delta-matroid."""

from __future__ import annotations

from fractions import Fraction


# Represent a+b*z in Q[z]/(z^2+1/2) by the pair (a,b).
def add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def multiply(left, right):
    return (
        left[0] * right[0] - left[1] * right[1] * Fraction(1, 2),
        left[0] * right[1] + left[1] * right[0],
    )


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def weight(u, v):
    same_shore = (u < 3) == (v < 3)
    return (Fraction(1), Fraction(0)) if same_shore else (Fraction(0), Fraction(1))


def hafnian(vertices):
    answer = (Fraction(0), Fraction(0))
    for matching in perfect_matchings(tuple(sorted(vertices))):
        term = (Fraction(1), Fraction(0))
        for edge in matching:
            term = multiply(term, weight(*edge))
        answer = add(answer, term)
    return answer


def main() -> None:
    x = frozenset((0, 1, 2, 3))
    y = frozenset((3, 4))
    assert hafnian(range(6)) == (Fraction(0), Fraction(6))
    assert hafnian(x) == (Fraction(0), Fraction(3))
    assert hafnian(y) == (Fraction(1), Fraction(0))
    difference = x ^ y
    u = 4
    assert difference == frozenset((0, 1, 2, 4))
    for v in difference - {u}:
        assert hafnian(x ^ {u, v}) == (Fraction(0), Fraction(0))
    print("VERIFIED: principal-hafnian support violates symmetric exchange")


if __name__ == "__main__":
    main()

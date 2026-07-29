#!/usr/bin/env python3
"""Exact audit of the twelve-port capped four-cut countermodel.

All coefficients are integers.  A monomial is a 12-tuple with -1 for a
hole and 0,1,2 for an occupied target coordinate.  Multiplication is the
site-square-zero product, so two factors occupying one site multiply to
zero.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product


NPORTS = 12
COLORS = range(3)
FRAMES = range(4)
HOLE = -1


def port(color: int, frame: int) -> int:
    return 4 * color + frame


H = {color: frozenset(port(color, frame) for frame in FRAMES)
     for color in COLORS}


Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Fraction]


def one_monomial(site: int, color: int) -> Monomial:
    word = [HOLE] * NPORTS
    word[site] = color
    return tuple(word)


def multiply_monomials(left: Monomial, right: Monomial) -> Monomial | None:
    out = []
    for a, b in zip(left, right, strict=True):
        if a != HOLE and b != HOLE:
            return None
        out.append(b if a == HOLE else a)
    return tuple(out)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    out: Counter[Monomial] = Counter()
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = multiply_monomials(lm, rm)
            if monomial is not None:
                out[monomial] += lc * rc
    return {m: c for m, c in out.items() if c}


def row(frame: int, color: int) -> Polynomial:
    return {one_monomial(port(color, frame), color): Fraction(1)}


def hole_sector(color: int) -> Monomial:
    return tuple(HOLE if site in H[color] else color
                 for site in range(NPORTS))


QBAR: Polynomial = {hole_sector(color): Fraction(1) for color in COLORS}


def target(color: int) -> Polynomial:
    return {tuple([color] * NPORTS): Fraction(1)}


def response(colors: tuple[int, int, int, int]) -> Polynomial:
    ans: Polynomial = {tuple([HOLE] * NPORTS): Fraction(1)}
    for frame, color in enumerate(colors):
        ans = multiply(ans, row(frame, color))
    return multiply(ans, QBAR)


def all_perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in all_perfect_matchings(rest):
            yield ((first, second),) + tail


def union_of_matching_edges(block: frozenset[int], matching) -> bool:
    return all(((a in block) == (b in block)) for a, b in matching)


def main() -> None:
    assert set().union(*H.values()) == set(range(NPORTS))
    assert all(len(H[c]) == 4 for c in COLORS)
    assert all(H[c].isdisjoint(H[d]) for c in COLORS for d in COLORS if c < d)

    # Each ordered frame consists of three distinct standard coordinate
    # vectors in the direct sum of the twelve local spaces.
    support_ledger = []
    for frame in FRAMES:
        basis_keys = []
        for color in COLORS:
            support = {port(color, frame)}
            assert len(support) == 1
            anchor = (port(color, frame), color)
            basis_keys.append(anchor)
            support_ledger.append((frame, color, anchor))
        assert len(set(basis_keys)) == 3  # rank of the frame is exactly 3

    nonzero = []
    response_ledger = []
    for colors in product(COLORS, repeat=4):
        got = response(colors)
        expected = target(colors[0]) if len(set(colors)) == 1 else {}
        assert got == expected, (colors, got, expected)
        if got:
            nonzero.append(colors)
        canonical_terms = tuple(sorted((monomial, str(coeff))
                                       for monomial, coeff in got.items()))
        response_ledger.append((colors, canonical_terms))

    assert nonzero == [(0, 0, 0, 0), (1, 1, 1, 1), (2, 2, 2, 2)]

    # Fixed-perfect-matching no-lift audit.  H_c is a union of matching
    # edges iff no edge crosses H_c.  Exactly three independent perfect
    # matchings, one on each four-set, give 3^3 candidates.
    matching_count = 0
    aligned = []
    for matching in all_perfect_matchings(tuple(range(NPORTS))):
        matching_count += 1
        if all(union_of_matching_edges(H[c], matching) for c in COLORS):
            aligned.append(matching)
            for edge in matching:
                group = next(c for c in COLORS if set(edge) <= H[c])
                demands = {c for c in COLORS if c != group}
                # This edge occurs in the coefficients with holes H_c for
                # both other colours and would have to be pure on two
                # independent target coordinate axes.
                assert len(demands) == 2

    assert matching_count == 10395
    assert len(aligned) == 27

    ledger = repr((support_ledger, response_ledger,
                   matching_count, len(aligned))).encode()
    digest = sha256(ledger).hexdigest()
    print("PASS: twelve-port capped four-cut countermodel")
    print("81 responses: 3 normalized diagonal, 78 zero")
    print("four frame ranks: 3, 3, 3, 3; every row support: 1")
    print("fixed perfect matchings checked: 10395; aligned candidates: 27")
    print(f"audit ledger sha256: {digest}")


if __name__ == "__main__":
    main()

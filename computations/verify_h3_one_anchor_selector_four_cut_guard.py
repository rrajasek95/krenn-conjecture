#!/usr/bin/env python3
"""Exact audit of the one-anchor selector/four-cut guard.

The script uses only the standard library.  It verifies the seven retained
pair rows, the two monochromatic selector matrices, the two coprime clean
coordinates, and the selected four-cut target coefficient.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product


SITES = ("A0", "A1", "A2", "B0", "B1", "B2")
POS = {site: index for index, site in enumerate(SITES)}
COLORS = range(3)
Polynomial = dict[tuple[int, int], Fraction]


def form(entries):
    return {(site, color): Fraction(weight) for site, color, weight in entries}


P = (
    form((("A0", 0, 1), ("A1", 1, 1), ("A2", 1, 1))),
    form((("A2", 0, 1),)),
    form((("B1", 0, 1),)),
)
S = (
    form((("A1", 0, 1),)),
    form(
        (
            ("B0", 0, 1),
            ("B0", 1, 1),
            ("B1", 1, 1),
            ("B2", 1, 1),
        )
    ),
    form((("B2", 0, 1),)),
)

Q_EDGES = (
    ("B0", 0, "B1", 0, Fraction(1)),
    ("A2", 0, "B2", 0, Fraction(1)),
)


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, Fraction(0)) + coefficient
    return {monomial: value for monomial, value in answer.items() if value}


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for (lu, lv), left_value in left.items():
        for (ru, rv), right_value in right.items():
            monomial = (lu + ru, lv + rv)
            answer[monomial] = (
                answer.get(monomial, Fraction(0)) + left_value * right_value
            )
    return {monomial: value for monomial, value in answer.items() if value}


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def add_edge(
    family: dict[tuple[int, int, int, int], Polynomial],
    left_site: str,
    left_color: int,
    right_site: str,
    right_color: int,
    polynomial: Polynomial,
) -> None:
    left = POS[left_site]
    right = POS[right_site]
    if left == right:
        return
    if left > right:
        left, right = right, left
        left_color, right_color = right_color, left_color
    key = (left, right, left_color, right_color)
    family[key] = poly_add(family.get(key, {}), polynomial)


def add_outer(
    family: dict[tuple[int, int, int, int], Polynomial],
    left_form,
    right_form,
    polynomial: Polynomial,
) -> None:
    for (left_site, left_color), left_weight in left_form.items():
        for (right_site, right_color), right_weight in right_form.items():
            add_edge(
                family,
                left_site,
                left_color,
                right_site,
                right_color,
                {
                    monomial: coefficient * left_weight * right_weight
                    for monomial, coefficient in polynomial.items()
                },
            )


def matching_tensor(
    family: dict[tuple[int, int, int, int], Polynomial],
) -> dict[tuple[int, ...], Polynomial]:
    answer = {}
    for coloring in product(COLORS, repeat=len(SITES)):
        polynomial: Polynomial = {}
        for matching in perfect_matchings(tuple(range(len(SITES)))):
            term: Polynomial = {(0, 0): Fraction(1)}
            for left, right in matching:
                term = poly_mul(
                    term,
                    family.get((left, right, coloring[left], coloring[right]), {}),
                )
            polynomial = poly_add(polynomial, term)
        if polynomial:
            answer[coloring] = polynomial
    return answer


def pair_row(i: int, j: int):
    """Return p_i s_j q^[2]; q^[3] is zero in this guard."""

    answer = {}
    for (left_site, left_color), left_weight in P[i].items():
        for (right_site, right_color), right_weight in S[j].items():
            if left_site == right_site:
                continue
            occupied = {
                POS[left_site],
                POS[right_site],
                POS["B0"],
                POS["B1"],
                POS["A2"],
                POS["B2"],
            }
            if len(occupied) != len(SITES):
                continue
            coloring = [None] * len(SITES)
            coloring[POS[left_site]] = left_color
            coloring[POS[right_site]] = right_color
            coloring[POS["B0"]] = 0
            coloring[POS["B1"]] = 0
            coloring[POS["A2"]] = 0
            coloring[POS["B2"]] = 0
            key = tuple(coloring)
            answer[key] = answer.get(key, Fraction(0)) + left_weight * right_weight
    return {word: value for word, value in answer.items() if value}


def selector_row(star, site: str, color: int):
    return tuple(star[index].get((site, color), Fraction(0)) for index in range(3))


def main() -> None:
    x0 = (0,) * len(SITES)

    # q has two disjoint edges, so q^[2] is their product and q^[3]=0.
    assert pair_row(0, 0) == {x0: Fraction(1)}
    for i in range(3):
        for j in range(3):
            if (i, j) != (0, 0):
                assert pair_row(i, j) == {}

    assert tuple(selector_row(P, site, 0) for site in ("A0", "A2", "B1")) == (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )
    assert tuple(selector_row(S, site, 0) for site in ("A1", "B0", "B2")) == (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )
    for site in ("A0", "A2", "B1"):
        assert selector_row(S, site, 0) == (0, 0, 0)
    for site in ("A1", "B0", "B2"):
        assert selector_row(P, site, 0) == (0, 0, 0)

    # F = u(q+p_0s_1) + v(p_0s_0+p_1s_1+p_2s_2).
    effective = {}
    for left_site, left_color, right_site, right_color, weight in Q_EDGES:
        add_edge(
            effective,
            left_site,
            left_color,
            right_site,
            right_color,
            {(1, 0): weight},
        )
    add_outer(effective, P[0], S[1], {(1, 0): Fraction(1)})
    for index in range(3):
        add_outer(effective, P[index], S[index], {(0, 1): Fraction(1)})

    clean = matching_tensor(effective)
    for color in COLORS:
        pure = (color,) * len(SITES)
        clean[pure] = poly_add(clean.get(pure, {}), {(2, 1): Fraction(-1)})
        if not clean[pure]:
            del clean[pure]

    mixed_word = (0, 1, 1, 1, 1, 1)
    assert clean[mixed_word] == {(3, 0): Fraction(6)}
    assert clean[x0] == {(0, 3): Fraction(1)}

    # On x=A0, y=A2, c=d=0, the four-cut row is
    # L_0 * e_0^(B2) * (B0B1)_0.  The u*s_1 part collides and the
    # v*e_0^(A1) part is v X_0^D.
    d_sites = ("A1", "B0", "B1", "B2")
    selected = {}
    for (site, color), weight in S[1].items():
        if site in ("B0", "B1", "B2"):
            # Collision with the fixed B0,B1,B2 factors.
            continue
        selected[(site, color)] = {(1, 0): weight}
    selected[("A1", 0)] = {(0, 1): Fraction(1)}
    four_cut = {}
    for (site, color), polynomial in selected.items():
        if site != "A1":
            continue
        word = tuple(0 for _ in d_sites)
        four_cut[word] = poly_add(four_cut.get(word, {}), polynomial)
    assert four_cut == {(0, 0, 0, 0): {(0, 1): Fraction(1)}}

    print("one-anchor physical rows and monochromatic selectors: PASS")
    print("clean coordinates: [Y]E=6u^3, [X0]E=v^3")
    print("selector-compatible four-cut coefficient: P_00=v X0^D")


if __name__ == "__main__":
    main()

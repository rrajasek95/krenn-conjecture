#!/usr/bin/env python3
"""Exact audit for the scalar-unit binary residual-target branch.

The script is deliberately dependency-free.  It uses the literal
site-square-zero algebra over fractions.Fraction and explicit failures,
so every check remains active under python -O.
"""

from __future__ import annotations

from fractions import Fraction
from math import factorial
from typing import Dict, Iterable, Iterator, Sequence, Tuple


Variable = Tuple[int, int]
Monomial = Tuple[Variable, ...]
Polynomial = Dict[Monomial, Fraction]
PhysicalEdge = Tuple[int, int]


class AuditError(RuntimeError):
    """Raised when an exact audit condition fails."""


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def normalize(poly: Polynomial) -> Polynomial:
    return {monomial: value for monomial, value in poly.items() if value}


def add(*polys: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for poly in polys:
        for monomial, value in poly.items():
            out[monomial] = out.get(monomial, Fraction(0)) + value
    return normalize(out)


def scale(poly: Polynomial, scalar: Fraction | int) -> Polynomial:
    scalar = Fraction(scalar)
    return normalize(
        {monomial: scalar * value for monomial, value in poly.items()}
    )


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for monomial_left, value_left in left.items():
        sites_left = {site for site, _ in monomial_left}
        for monomial_right, value_right in right.items():
            if sites_left.intersection(site for site, _ in monomial_right):
                continue
            monomial = tuple(sorted(monomial_left + monomial_right))
            out[monomial] = (
                out.get(monomial, Fraction(0)) + value_left * value_right
            )
    return normalize(out)


def ordinary_power(poly: Polynomial, exponent: int) -> Polynomial:
    out: Polynomial = {(): Fraction(1)}
    for _ in range(exponent):
        out = multiply(out, poly)
    return out


def divided_power(poly: Polynomial, exponent: int) -> Polynomial:
    return scale(ordinary_power(poly, exponent), Fraction(1, factorial(exponent)))


def variable(site: int, color: int, value: Fraction | int = 1) -> Polynomial:
    return {((site, color),): Fraction(value)}


def linear_form(entries: Iterable[Tuple[int, int, Fraction | int]]) -> Polynomial:
    return add(*(variable(site, color, value) for site, color, value in entries))


def cell(
    first_site: int,
    first_color: int,
    second_site: int,
    second_color: int,
    value: Fraction | int = 1,
) -> Polynomial:
    check(first_site != second_site, "a physical cell may not use one site twice")
    monomial = tuple(
        sorted(((first_site, first_color), (second_site, second_color)))
    )
    return {monomial: Fraction(value)}


def word(colors: Sequence[int]) -> Monomial:
    return tuple((site, color) for site, color in enumerate(colors))


def constant_word(order: int, color: int) -> Monomial:
    return word([color] * order)


def coefficient(poly: Polynomial, monomial: Monomial) -> Fraction:
    return poly.get(monomial, Fraction(0))


def project_colors(poly: Polynomial, allowed: set[int]) -> Polynomial:
    return {
        monomial: value
        for monomial, value in poly.items()
        if all(color in allowed for _, color in monomial)
    }


def physical_edges(poly: Polynomial) -> set[PhysicalEdge]:
    out: set[PhysicalEdge] = set()
    for monomial in poly:
        check(len(monomial) == 2, "physical-edge extraction expects a quadratic")
        u, v = sorted((monomial[0][0], monomial[1][0]))
        out.add((u, v))
    return out


def perfect_matchings(vertices: Sequence[int]) -> Iterator[Tuple[PhysicalEdge, ...]]:
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        edge = tuple(sorted((first, second)))
        for matching in perfect_matchings(rest):
            yield (edge,) + matching


def poly_from_word_coefficients(table: Dict[str, int]) -> Polynomial:
    return normalize(
        {
            word([int(character) for character in colors]): Fraction(value)
            for colors, value in table.items()
        }
    )


def verify_weighted_adjacent_switch() -> None:
    """Audit the uniform Hamilton projected equations (9), including weights."""

    for h in range(3, 10):
        order = 2 * h
        alpha = Fraction(3, 2)
        hamilton: Polynomial = {}
        b_weights = [Fraction(k + 2, k + 1) for k in range(h)]
        c_weights = [Fraction(2 * k + 3, 2 * k + 1) for k in range(h)]

        for k, value in enumerate(b_weights):
            hamilton = add(
                hamilton, cell(2 * k, 1, 2 * k + 1, 1, value)
            )
        for k, value in enumerate(c_weights):
            hamilton = add(
                hamilton,
                cell(2 * k + 1, 2, (2 * k + 2) % order, 2, value),
            )

        product_b = Fraction(1)
        product_c = Fraction(1)
        for value in b_weights:
            product_b *= value
        for value in c_weights:
            product_c *= value
        expected_top = {
            constant_word(order, 1): product_b,
            constant_word(order, 2): product_c,
        }
        top = divided_power(hamilton, h)
        check(top == expected_top, f"weighted Hamilton top failed at h={h}")

        left = linear_form(((0, 1, 1), (1, 2, 1)))
        right = linear_form(
            (
                (1, 1, -alpha * b_weights[0]),
                (2, 2, -alpha * c_weights[0]),
            )
        )
        response = multiply(left, right)
        check(len(response) == 3, f"adjacent response is not three-cell at h={h}")

        derivative = multiply(response, divided_power(hamilton, h - 1))
        check(
            derivative == scale(expected_top, -alpha),
            f"weighted Hamilton derivative equation failed at h={h}",
        )

        switched = add(scale(hamilton, alpha), response)
        check(
            not any(1 in edge for edge in physical_edges(switched)),
            f"the switched support did not isolate site 1 at h={h}",
        )
        check(
            divided_power(switched, h) == {},
            f"weighted Hamilton clean projection failed at h={h}",
        )


def build_six_site_guard() -> Tuple[Polynomial, Polynomial, Polynomial, Polynomial]:
    """Return q, p_a, s_a, and R=p_a*s_a for the rational h=3 guard."""

    q: Polynomial = {}
    for u, v in ((0, 1), (2, 3), (4, 5)):
        q = add(q, cell(u, 1, v, 1))
    for u, v in ((1, 2), (3, 4), (5, 0)):
        q = add(q, cell(u, 2, v, 2))
    for u, v in ((1, 5), (2, 4)):
        q = add(q, cell(u, 0, v, 0))

    p_a = linear_form(((0, 0, 1), (0, 1, 1), (1, 2, 1)))
    s_a = linear_form(((3, 0, 1), (1, 1, -1), (2, 2, -1)))
    response = multiply(p_a, s_a)
    return q, p_a, s_a, response


def verify_six_site_guard() -> None:
    q, p_a, s_a, response = build_six_site_guard()
    check(len(q) == 8, "the six-site guard does not have eight q-cells")
    check(len(p_a) == 3 and len(s_a) == 3, "the guard is not three-port")
    check(
        {color for monomial in p_a for _, color in monomial} == {0, 1, 2},
        "p_a does not contain all three colors",
    )
    check(
        {color for monomial in s_a for _, color in monomial} == {0, 1, 2},
        "s_a does not contain all three colors",
    )

    active_face = project_colors(q, {1, 2})
    check(len(active_face) == 6, "the active binary face is not cell-minimal")
    expected_top = {
        constant_word(6, 1): Fraction(1),
        constant_word(6, 2): Fraction(1),
    }
    top = divided_power(q, 3)
    check(top == expected_top, "the eight-cell guard does not have binary top")
    check(
        divided_power(active_face, 3) == expected_top,
        "the active Hamilton face has the wrong top",
    )

    edge_support = physical_edges(q)
    supported_matchings = {
        tuple(sorted(matching))
        for matching in perfect_matchings(tuple(range(6)))
        if set(matching).issubset(edge_support)
    }
    expected_matchings = {
        tuple(sorted(((0, 1), (2, 3), (4, 5)))),
        tuple(sorted(((0, 5), (1, 2), (3, 4)))),
    }
    check(
        supported_matchings == expected_matchings,
        "the top-inactive chords created an unexpected perfect matching",
    )
    check(
        all(
            (1, 5) not in matching and (2, 4) not in matching
            for matching in supported_matchings
        ),
        "a charged a-cell unexpectedly occurs in a full matching",
    )

    q_second = divided_power(q, 2)
    near_a_word = tuple(sorted(((1, 0), (2, 0), (4, 0), (5, 0))))
    check(
        coefficient(q_second, near_a_word) == 1,
        "the charged all-a near-perfect cofactor is not one",
    )
    missing_cap = cell(0, 0, 3, 0)
    capped = multiply(missing_cap, q_second)
    check(
        coefficient(capped, constant_word(6, 0)) == 1,
        "the top-inactive cells are not response-active",
    )

    derivative = multiply(response, q_second)
    clean_endpoint = divided_power(add(q, response), 3)
    residue_one = poly_from_word_coefficients(
        {
            "002220": -1,
            "011111": -1,
            "022011": 1,
            "100000": 1,
            "102220": -1,
            "122011": 1,
            "220002": 1,
        }
    )
    residue_two = poly_from_word_coefficients(
        {
            "002220": -1,
            "011111": -1,
            "022011": -1,
            "100000": 1,
            "102220": -1,
            "122011": -1,
            "220002": 1,
        }
    )
    expected_derivative = add(
        {constant_word(6, 0): Fraction(1)},
        {constant_word(6, 1): Fraction(-1)},
        {constant_word(6, 2): Fraction(-1)},
        residue_one,
    )
    expected_clean_endpoint = add(
        {constant_word(6, 0): Fraction(1)}, residue_two
    )
    check(
        derivative == expected_derivative,
        "the exact exceptional-row residue table is wrong",
    )
    check(
        clean_endpoint == expected_clean_endpoint,
        "the exact clean-endpoint residue table is wrong",
    )
    check(
        project_colors(derivative, {1, 2}) == scale(expected_top, -1),
        "the combined guard fails the active derivative projection",
    )
    check(
        project_colors(clean_endpoint, {1, 2}) == {},
        "the combined guard fails the active clean projection",
    )
    check(len(residue_one) == 7 and len(residue_two) == 7, "residue count drift")

    # Deleting the charged cells preserves q^[3] but destroys the named
    # near-perfect cofactor.  This is the exact q-alone-minimality mutation.
    hamilton_only = active_face
    check(
        divided_power(hamilton_only, 3) == top,
        "Hamilton deletion unexpectedly changed the binary top",
    )
    deleted_capped = multiply(missing_cap, divided_power(hamilton_only, 2))
    check(
        coefficient(deleted_capped, constant_word(6, 0)) == 0,
        "Hamilton deletion unexpectedly preserved the a-response",
    )

    # A response-sign mutation must be visible even under optimized Python.
    mutated_s = linear_form(((3, 0, 1), (1, 1, 1), (2, 2, -1)))
    mutated_derivative = multiply(multiply(p_a, mutated_s), q_second)
    check(
        coefficient(mutated_derivative, constant_word(6, 1)) == 1,
        "the response-sign mutation was not detected",
    )
    check(
        coefficient(mutated_derivative, constant_word(6, 1))
        != coefficient(derivative, constant_word(6, 1)),
        "the response-sign mutation left the audited row unchanged",
    )

    raw_top = ordinary_power(q, 3)
    check(
        coefficient(raw_top, constant_word(6, 1)) == factorial(3),
        "the divided-power factorial mutation was not detected",
    )


def main() -> None:
    verify_weighted_adjacent_switch()
    verify_six_site_guard()
    print(
        "scalar-unit binary residual target branch: PASS; "
        "weighted h=3..9 switch and exact rational h=3 guard"
    )


if __name__ == "__main__":
    main()

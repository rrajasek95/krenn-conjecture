#!/usr/bin/env python3
"""Exact audit of the restored-cc exact-cancellation selected-cross guard.

The calculation uses the literal decorated site-square-zero algebra over
fractions.Fraction.  Every audit uses explicit failure, including under
python -O.
"""

from __future__ import annotations

from fractions import Fraction
from math import factorial
from typing import Dict, Iterable, Sequence, Tuple


Variable = Tuple[int, int]
Monomial = Tuple[Variable, ...]
Polynomial = Dict[Monomial, Fraction]

A, B, C = 0, 1, 2
LABELS = (A, B, C)
ZERO: Polynomial = {}


class AuditError(RuntimeError):
    """Raised when an exact audit condition fails."""


def require(condition: bool, message: str) -> None:
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


def multiply(
    left: Polynomial,
    right: Polynomial,
    *rest: Polynomial,
) -> Polynomial:
    out: Polynomial = {}
    for left_monomial, left_value in left.items():
        left_sites = {site for site, _ in left_monomial}
        for right_monomial, right_value in right.items():
            if left_sites.intersection(site for site, _ in right_monomial):
                continue
            monomial = tuple(sorted(left_monomial + right_monomial))
            out[monomial] = (
                out.get(monomial, Fraction(0))
                + left_value * right_value
            )
    out = normalize(out)
    for poly in rest:
        out = multiply(out, poly)
    return out


def ordinary_power(poly: Polynomial, exponent: int) -> Polynomial:
    require(exponent >= 0, "negative ordinary-power exponent")
    out: Polynomial = {(): Fraction(1)}
    for _ in range(exponent):
        out = multiply(out, poly)
    return out


def divided_power(poly: Polynomial, exponent: int) -> Polynomial:
    return scale(
        ordinary_power(poly, exponent),
        Fraction(1, factorial(exponent)),
    )


def variable(
    site: int,
    color: int,
    value: Fraction | int = 1,
) -> Polynomial:
    return {((site, color),): Fraction(value)}


def linear_form(
    entries: Iterable[Tuple[int, int, Fraction | int]],
) -> Polynomial:
    return add(
        *(variable(site, color, value) for site, color, value in entries)
    )


def cell(
    first_site: int,
    first_color: int,
    second_site: int,
    second_color: int,
    value: Fraction | int = 1,
) -> Polynomial:
    require(first_site != second_site, "a cell reused one physical site")
    monomial = tuple(
        sorted(
            (
                (first_site, first_color),
                (second_site, second_color),
            )
        )
    )
    return {monomial: Fraction(value)}


def word(colors: Sequence[int]) -> Monomial:
    return tuple((site, color) for site, color in enumerate(colors))


def constant_word(color: int) -> Monomial:
    return word((color,) * 6)


def coefficient(poly: Polynomial, monomial: Monomial) -> Fraction:
    return poly.get(monomial, Fraction(0))


def sole_monomial(poly: Polynomial) -> Monomial:
    require(len(poly) == 1, "expected a one-monomial polynomial")
    return next(iter(poly))


def linear_coefficient(poly: Polynomial, site: int, color: int) -> Fraction:
    return coefficient(poly, ((site, color),))


def matrix_rank(rows: Sequence[Sequence[Fraction]]) -> int:
    work = [[Fraction(value) for value in row] for row in rows]
    if not work:
        return 0
    height = len(work)
    width = len(work[0])
    require(
        all(len(row) == width for row in work),
        "rank input has ragged rows",
    )
    rank = 0
    for column in range(width):
        pivot = next(
            (
                row
                for row in range(rank, height)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(height):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                work[row][entry] - factor * work[rank][entry]
                for entry in range(width)
            ]
        rank += 1
        if rank == height:
            break
    return rank


def linear_rank(forms: Sequence[Polynomial]) -> int:
    coordinates = sorted(
        {
            monomial[0]
            for form in forms
            for monomial in form
            if len(monomial) == 1
        }
    )
    require(
        all(all(len(monomial) == 1 for monomial in form) for form in forms),
        "star-rank input was not linear",
    )
    rows = [
        [coefficient(form, (coordinate,)) for coordinate in coordinates]
        for form in forms
    ]
    return matrix_rank(rows)


def build_guard() -> tuple[
    Polynomial,
    Dict[int, Polynomial],
    Dict[int, Polynomial],
    Dict[Tuple[int, int], Polynomial],
]:
    q = add(
        cell(2, B, 3, B, 2),
        cell(4, B, 5, B),
        cell(3, B, 4, B, -1),
        cell(2, B, 5, B),
        cell(1, C, 4, C),
        cell(3, C, 5, C),
    )
    p = {
        A: variable(3, B),
        B: variable(0, B),
        C: variable(2, C),
    }
    s = {
        A: variable(4, B, -1),
        B: variable(1, B),
        C: variable(0, C),
    }
    responses = {
        (i, j): multiply(p[i], s[j])
        for i in LABELS
        for j in LABELS
    }
    return q, p, s, responses


def original_row(
    q: Polynomial,
    responses: Dict[Tuple[int, int], Polynomial],
    i: int,
    j: int,
) -> Polynomial:
    response = multiply(responses[i, j], divided_power(q, 2))
    if (i, j) == (A, A):
        return add(divided_power(q, 3), response)
    return response


def verify_stars_and_segre(
    p: Dict[int, Polynomial],
    s: Dict[int, Polynomial],
    responses: Dict[Tuple[int, int], Polynomial],
) -> None:
    require(linear_rank(tuple(p.values())) == 3, "p-star rank is not three")
    require(linear_rank(tuple(s.values())) == 3, "s-star rank is not three")
    raa = responses[A, A]
    for j in LABELS:
        for k in LABELS:
            left = multiply(responses[j, k], raa)
            right = multiply(responses[j, A], responses[A, k])
            require(
                left == right,
                f"physical Segre square failed at ({j},{k})",
            )


def verify_original_rows(
    q: Polynomial,
    responses: Dict[Tuple[int, int], Polynomial],
) -> None:
    xa = {constant_word(A): Fraction(1)}
    xb = {constant_word(B): Fraction(1)}
    xc = {constant_word(C): Fraction(1)}
    mixed = {word((C, C, B, B, C, B)): Fraction(1)}

    actual_expected = {
        (A, A): ZERO,
        (A, B): ZERO,
        (A, C): mixed,
        (B, A): ZERO,
        (B, B): xb,
        (B, C): ZERO,
        (C, A): ZERO,
        (C, B): ZERO,
        (C, C): xc,
    }
    target_expected = {
        (i, j): (
            xa
            if (i, j) == (A, A)
            else xb
            if (i, j) == (B, B)
            else xc
            if (i, j) == (C, C)
            else ZERO
        )
        for i in LABELS
        for j in LABELS
    }

    failures = []
    for i in LABELS:
        for j in LABELS:
            actual = original_row(q, responses, i, j)
            require(
                actual == actual_expected[i, j],
                f"original-row table failed at ({i},{j})",
            )
            if actual != target_expected[i, j]:
                failures.append((i, j))
    require(
        failures == [(A, A), (A, C)],
        "the guard is not exactly seven-of-nine",
    )
    require(divided_power(q, 3) == ZERO, "q top power should be zero")


def verify_path_and_carrier(
    q: Polynomial,
    p: Dict[int, Polynomial],
    s: Dict[int, Polynomial],
    responses: Dict[Tuple[int, int], Polynomial],
) -> None:
    xb = {constant_word(B): Fraction(1)}
    xc = {constant_word(C): Fraction(1)}
    raa = responses[A, A]
    g = add(q, raa)

    require(
        raa == cell(3, B, 4, B, -1),
        "the marked response has the wrong cell",
    )
    require(
        responses[B, B] == cell(0, B, 1, B),
        "the bb cap has the wrong cell",
    )
    require(
        responses[C, C] == cell(2, C, 0, C),
        "the cc cap has the wrong cell",
    )
    require(responses[B, C] == ZERO, "the bc cap should collide")
    require(divided_power(raa, 2) == ZERO, "Raa^[2] should vanish")
    require(divided_power(g, 3) == ZERO, "transformed top should be zero")

    q2 = divided_power(q, 2)
    g2 = divided_power(g, 2)
    theta = add(g2, scale(q2, -1))
    h_carrier = add(q, scale(raa, Fraction(1, 2)))
    require(theta == multiply(raa, q), "Theta is not Raa*q")
    require(theta == multiply(raa, h_carrier), "Theta is not Raa*H")

    z = {
        (i, j): multiply(responses[i, j], theta)
        for i in LABELS
        for j in LABELS
    }
    for i in LABELS:
        for j in LABELS:
            expected = scale(xb, -1) if (i, j) == (B, B) else ZERO
            require(z[i, j] == expected, f"Z packet failed at ({i},{j})")

    complementary_old = {
        (B, B): xb,
        (B, C): ZERO,
        (C, B): ZERO,
        (C, C): xc,
    }
    complementary_new = {
        (B, B): ZERO,
        (B, C): ZERO,
        (C, B): ZERO,
        (C, C): xc,
    }
    for pair, expected in complementary_old.items():
        require(
            multiply(responses[pair], q2) == expected,
            f"old complementary endpoint failed at {pair}",
        )
    for pair, expected in complementary_new.items():
        require(
            multiply(responses[pair], g2) == expected,
            f"new complementary endpoint failed at {pair}",
        )

    for t in (
        Fraction(-3),
        Fraction(-1),
        Fraction(0),
        Fraction(1, 2),
        Fraction(1),
        Fraction(5, 3),
        Fraction(2),
    ):
        q_t = add(q, scale(raa, t))
        q_t_second = divided_power(q_t, 2)
        expected_path = {
            (B, B): scale(xb, 1 - t),
            (B, C): ZERO,
            (C, B): ZERO,
            (C, C): xc,
        }
        for pair, expected in expected_path.items():
            require(
                multiply(responses[pair], q_t_second) == expected,
                f"endpoint polynomial failed at t={t}, pair={pair}",
            )

        for j in LABELS:
            for k in LABELS:
                derivative = multiply(
                    responses[j, k],
                    raa,
                    q_t,
                )
                segre_derivative = multiply(
                    responses[j, A],
                    responses[A, k],
                    q_t,
                )
                require(
                    derivative == segre_derivative,
                    f"path Segre derivative failed at t={t}, ({j},{k})",
                )

    sole_carrier = multiply(
        responses[B, B],
        raa,
        cell(2, B, 5, B),
    )
    require(sole_carrier == scale(xb, -1), "sole carrier has wrong sign")
    require(
        multiply(responses[B, B], raa, q) == scale(xb, -1),
        "the full bb carrier is not the sole marked term",
    )

    marked_cell = sole_monomial(cell(3, B, 4, B))
    q_marked = coefficient(q, marked_cell)
    forward = (
        linear_coefficient(p[A], 3, B)
        * linear_coefficient(s[A], 4, B)
    )
    reverse = (
        linear_coefficient(p[A], 4, B)
        * linear_coefficient(s[A], 3, B)
    )
    require(q_marked == -1, "marked q coefficient is not -1")
    require(forward == -1, "forward Raa orientation is not -1")
    require(reverse == 0, "reverse Raa orientation is not zero")
    require(q_marked - forward == 0, "marked forward curvature is nonzero")


def verify_selected_cross_chase(
    q: Polynomial,
    responses: Dict[Tuple[int, int], Polynomial],
) -> None:
    omega = word((C, C, B, B, C, B))
    eta = word((B, C, B, C, B, C))
    raa = responses[A, A]
    rac = responses[A, C]
    rba = responses[B, A]

    q2 = divided_power(q, 2)
    require(
        coefficient(multiply(rac, q2), omega) == 1,
        "the selected ac residual is not one",
    )
    require(
        coefficient(original_row(q, responses, A, A), omega) == 0,
        "the aa row should be vacuous on the selected mixed word",
    )
    require(
        coefficient(multiply(rba, q2), eta) == 0,
        "the original ba transport word should vanish",
    )

    repaired = add(
        q,
        cell(1, C, 2, B),
        cell(4, C, 5, B, -1),
    )
    repaired_second = divided_power(repaired, 2)
    require(
        coefficient(multiply(rac, repaired_second), omega) == 0,
        "the 12|45 mate did not cancel the selected ac word",
    )
    require(
        coefficient(original_row(repaired, responses, A, A), omega) == 0,
        "the one-word repair changed the vacuous aa equation",
    )
    require(
        coefficient(multiply(rba, repaired_second), eta) == -1,
        "the ac repair did not transport residual -1 into ba",
    )
    marked = sole_monomial(cell(3, B, 4, B))
    require(
        coefficient(repaired, marked) == coefficient(q, marked) == -1,
        "the one-word repair changed the aligned marked coefficient",
    )

    # Audit the three matching formulas (25)--(30) on an independent
    # rational decorated-cell probe.
    x = Fraction(2, 3)
    y = Fraction(-5, 7)
    u = Fraction(11, 13)
    v = Fraction(17, 19)
    w = Fraction(-3, 5)
    z = Fraction(7, 11)
    s_cb = Fraction(13, 17)
    r = Fraction(19, 23)
    n = Fraction(-2, 9)
    ell = Fraction(5, 8)
    probe = add(
        cell(2, B, 5, B),
        cell(1, C, 2, B, x),
        cell(4, C, 5, B, y),
        cell(1, C, 4, C, u),
        cell(3, C, 5, C, v),
        cell(1, C, 3, C, w),
        cell(4, C, 5, C, z),
        cell(3, C, 5, B, s_cb),
        cell(2, B, 3, B, r),
        cell(2, B, 4, C, n),
        cell(3, B, 5, C, ell),
    )
    probe_second = divided_power(probe, 2)
    eta_reroute = word((B, C, B, C, B, B))
    zeta = word((B, B, B, B, C, C))
    cc_word = constant_word(C)
    require(
        coefficient(multiply(rac, probe_second), omega) == x * y + u,
        "the ac three-matching formula failed",
    )
    require(
        coefficient(multiply(rba, probe_second), eta) == -x * v,
        "the ba transport formula failed",
    )
    require(
        coefficient(
            multiply(responses[C, C], probe_second),
            cc_word,
        )
        == w * z + u * v,
        "the pure-cc reroute formula failed",
    )
    require(
        coefficient(multiply(rba, probe_second), eta_reroute)
        == -(x * s_cb + w),
        "the rerouted ba formula failed",
    )
    require(
        coefficient(
            multiply(responses[B, B], probe_second),
            zeta,
        )
        == r * z + n * ell,
        "the rerouted bb formula failed",
    )

    # The unique-pair implications in (24) are audited by mutations.
    theta_probe = multiply(raa, probe)
    zbb_probe = multiply(responses[B, B], theta_probe)
    zcc_probe = multiply(responses[C, C], theta_probe)
    require(
        zbb_probe == {constant_word(B): Fraction(-1)},
        "q25 purity did not give the exact bb jet",
    )
    require(zcc_probe == ZERO, "q15 absence did not give zero cc jet")

    bad_q25 = add(probe, cell(2, B, 5, C))
    bad_zbb = multiply(
        responses[B, B],
        multiply(raa, bad_q25),
    )
    require(
        bad_zbb != zbb_probe,
        "an off-colour q25 mutation escaped the bb jet",
    )
    bad_q15 = add(probe, cell(1, C, 5, C))
    bad_zcc = multiply(
        responses[C, C],
        multiply(raa, bad_q15),
    )
    require(
        bad_zcc != ZERO,
        "a q15 mutation escaped the cc jet",
    )


def verify_mutations(
    q: Polynomial,
    responses: Dict[Tuple[int, int], Polynomial],
) -> None:
    xb = {constant_word(B): Fraction(1)}
    xc = {constant_word(C): Fraction(1)}
    raa = responses[A, A]

    wrong_sign_endpoint = multiply(
        responses[B, B],
        divided_power(add(q, scale(raa, -1)), 2),
    )
    require(
        wrong_sign_endpoint == scale(xb, 2),
        "the Raa-sign mutation did not expose coefficient two",
    )

    missing_cc = add(q, cell(3, C, 5, C, -1))
    require(
        multiply(responses[C, C], divided_power(missing_cc, 2)) != xc,
        "deleting the second cc edge retained the cc target",
    )

    missing_ac = add(q, cell(1, C, 4, C, -1))
    omega = word((C, C, B, B, C, B))
    require(
        coefficient(
            multiply(responses[A, C], divided_power(missing_ac, 2)),
            omega,
        )
        == 0,
        "deleting q14 did not remove the selected ac residual",
    )

    wrong_weight = add(q, cell(2, B, 3, B, -1))
    require(
        multiply(responses[B, B], divided_power(wrong_weight, 2))
        == ZERO,
        "the b23-weight mutation did not destroy the old bb target",
    )


def main() -> None:
    q, p, s, responses = build_guard()
    verify_stars_and_segre(p, s, responses)
    verify_original_rows(q, responses)
    verify_path_and_carrier(q, p, s, responses)
    verify_selected_cross_chase(q, responses)
    verify_mutations(q, responses)
    print(
        "scalar-unit restored-cc exact-cancellation selected-cross guard: "
        "PASS; 7/9 rows, full complementary path, Segre carrier, "
        "zero marked curvature, and ac-to-ba transport audited"
    )


if __name__ == "__main__":
    main()

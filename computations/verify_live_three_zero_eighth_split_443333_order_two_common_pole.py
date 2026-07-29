#!/usr/bin/env python3
"""Exact audit of the h=8, k=2 profile (4,4,3,3,3,3) closure."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


w, z, mu = sp.symbols("w z mu")


def normalized_role(count: int, value: sp.Expr) -> sp.Expr:
    """The selected-class factor, divided by its common-pole value."""
    return (
        (1 - w / (value + mu)) ** (-count)
        * (1 + w / (value - mu)) ** (-(count + 1))
    )


def log_jets(count: int, value: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    """First and second logarithmic jets at w=0."""
    role = normalized_role(count, value)
    assert sp.factor(role.subs(w, 0) - 1) == 0
    first = sp.factor(sp.diff(role, w).subs(w, 0))
    second = sp.factor(sp.diff(role, w, 2).subs(w, 0) - first**2)
    return first, second


def leaves_singleton(
    multiplicities: tuple[int, ...], takes: dict[int, int]
) -> bool:
    return any(
        multiplicity - takes.get(index, 0) == 1
        for index, multiplicity in enumerate(multiplicities)
    )


def check_profile_and_legal_cores() -> None:
    h, p, k = 8, 10, 2
    multiplicities = (4, 4, 3, 3, 3, 3)
    assert sum(multiplicities) == p + h + 2 == 20

    witnessed = set()
    triple_indices = range(2, 6)
    for chosen in combinations(triple_indices, 3):
        for partial in chosen:
            takes = {
                index: (2 if index == partial else 3)
                for index in chosen
            }
            complement = tuple(
                multiplicity - takes.get(index, 0)
                for index, multiplicity in enumerate(multiplicities)
            )
            witnessed.add((chosen, partial))

            assert sum(takes.values()) == h
            assert len(takes) == 3
            assert sum(complement) == p + 2 == 12
            assert complement[partial] == 1
            assert sum(entry == 1 for entry in complement) == 1
            assert leaves_singleton(multiplicities, takes)

            denominator_degree = (k + 1) + sum(
                count + 1 for count in takes.values()
            )
            numerator_cap = p + len(takes) - 1
            residual_cap = numerator_cap - sum(complement)
            assert denominator_degree == 14
            assert numerator_cap == 12
            assert residual_cap == 0
            assert denominator_degree - numerator_cap == 2

    assert len(witnessed) == 4 * 3 == 12

    # The uniform 2k+1 moving-role theorem needs five candidates.  With
    # only six classes, fixing two roles leaves at most four, so the new
    # comparison really goes beyond that root count.
    assert len(multiplicities) - 2 == 4 < 2 * k + 1


def check_universal_baseline_and_exact_pole() -> None:
    value = sp.symbols("value")

    # This per-class identity proves that one full-unselected baseline is
    # common to every core.  The scalar constant residual may vary, but it
    # cancels from every zero-residue equation.
    for multiplicity in (3, 4):
        for count in range(1, multiplicity + 1):
            direct = (z - value) ** (multiplicity - count) / (
                z + value
            ) ** (count + 1)
            baseline = (z - value) ** multiplicity
            raw_role = 1 / (
                (z - value) ** count * (z + value) ** (count + 1)
            )
            assert sp.factor(direct - baseline * raw_role) == 0

            shifted = raw_role.subs(z, -mu + w)
            normalized = sp.factor(shifted / shifted.subs(w, 0))
            assert sp.factor(normalized - normalized_role(count, value)) == 0
            assert sp.factor(normalized.subs(w, 0) - 1) == 0

    # At an exact order-three pole, the residue is the w^2 coefficient.
    c0, c1, c2 = sp.symbols("c0 c1 c2")
    regular = c0 + c1 * w + c2 * w**2
    assert sp.residue(regular / w**3, w, 0) == c2


def check_order_two_logarithmic_formula() -> None:
    x, y, zeta = sp.symbols("x y zeta")
    u, v = sp.symbols("u v")

    # This polynomial has prescribed first and second logarithmic jets u,v.
    background = 1 + u * w + (u**2 + v) * w**2 / 2

    for counts in ((2, 3, 3), (3, 2, 3), (3, 3, 2)):
        values = (x, y, zeta)
        roles = [
            normalized_role(count, value)
            for count, value in zip(counts, values)
        ]
        regular = background * sp.prod(roles)
        second_derivative = sp.factor(sp.diff(regular, w, 2).subs(w, 0))

        first_jets = [
            log_jets(count, value)[0]
            for count, value in zip(counts, values)
        ]
        second_jets = [
            log_jets(count, value)[1]
            for count, value in zip(counts, values)
        ]
        expected = (
            (u + sum(first_jets)) ** 2 + v + sum(second_jets)
        )
        assert sp.factor(second_derivative - expected) == 0


def check_role_drop_and_three_subset_forcing() -> None:
    x, y = sp.symbols("x y")
    phi2, psi2 = log_jets(2, x)
    phi3, psi3 = log_jets(3, x)

    assert sp.factor(
        phi3 + (x + 7 * mu) / (x**2 - mu**2)
    ) == 0
    d = sp.factor(phi3 - phi2)
    delta_psi = sp.factor(psi3 - psi2)
    assert sp.factor(d + 2 * mu / (x**2 - mu**2)) == 0
    assert sp.factor(
        delta_psi
        - 2 * (x**2 + mu**2) / (x**2 - mu**2) ** 2
    ) == 0
    assert sp.factor(delta_psi - (d**2 - d / mu)) == 0

    # Distinct, nonopposite values give distinct d-values.  The displayed
    # factorization records every denominator and avoids hidden division.
    dy = sp.factor(log_jets(3, y)[0] - log_jets(2, y)[0])
    d_difference = sp.factor(d - dy)
    expected_difference = sp.factor(
        2
        * mu
        * (x - y)
        * (x + y)
        / (
            (x - mu)
            * (x + mu)
            * (y - mu)
            * (y + mu)
        )
    )
    assert sp.factor(d_difference - expected_difference) == 0

    # If T and W are the all-count-three total log jets on a fixed
    # three-subset, downgrading x to count two has this affine form.
    T, W = sp.symbols("T W")
    downgraded_equation = sp.expand((T - d) ** 2 + W - delta_psi)
    affine_equation = T**2 + W + (1 / mu - 2 * T) * d
    assert sp.factor(downgraded_equation - affine_equation) == 0

    dx, dy_formal = sp.symbols("d_x d_y")
    equation_x = T**2 + W + (1 / mu - 2 * T) * dx
    equation_y = T**2 + W + (1 / mu - 2 * T) * dy_formal
    assert sp.factor(
        equation_x
        - equation_y
        - (1 / mu - 2 * T) * (dx - dy_formal)
    ) == 0
    forced_T = sp.Rational(1, 2) / mu
    assert sp.factor((1 / mu - 2 * T).subs(T, forced_T)) == 0
    assert sp.factor(
        equation_x.subs(T, forced_T) - (W + 1 / (4 * mu**2))
    ) == 0

    # Equality of all four three-subset sums has rank three and forces the
    # four phi_3 values to be equal.
    incidence = sp.Matrix(
        [
            [0, 1, 1, 1],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [1, 1, 1, 0],
        ]
    )
    differences = sp.Matrix(
        [list(incidence.row(i) - incidence.row(0)) for i in range(1, 4)]
    )
    assert differences.rank() == 3
    assert differences.nullspace() == [sp.ones(4, 1)]

    fibre_value = sp.symbols("fibre_value")
    fibre_polynomial = sp.expand(
        fibre_value * (x**2 - mu**2) + x + 7 * mu
    )
    assert sp.Poly(fibre_polynomial, x).degree() == 2
    assert sp.Poly(fibre_polynomial, x).coeff_monomial(x) == 1
    assert sp.expand(fibre_polynomial.subs(fibre_value, 0)) == x + 7 * mu
    assert 4 > 2


def check_two_quartic_consecutive_swap() -> None:
    """Independent three-core audit, including the formal mu=0 edge."""
    a, b = sp.symbols("a b")
    u, v, fixed_first, fixed_second = sp.symbols(
        "u v fixed_first fixed_second"
    )

    phi_a = {count: log_jets(count, a)[0] for count in (2, 3, 4)}
    psi_a = {count: log_jets(count, a)[1] for count in (2, 3, 4)}
    phi_b = {count: log_jets(count, b)[0] for count in (2, 3, 4)}
    psi_b = {count: log_jets(count, b)[1] for count in (2, 3, 4)}

    first_sums = (
        fixed_first + phi_a[4] + phi_b[2],
        fixed_first + phi_a[3] + phi_b[3],
        fixed_first + phi_a[2] + phi_b[4],
    )
    second_sums = (
        fixed_second + psi_a[4] + psi_b[2],
        fixed_second + psi_a[3] + psi_b[3],
        fixed_second + psi_a[2] + psi_b[4],
    )
    equations = tuple(
        sp.expand((u + first) ** 2 + v + second)
        for first, second in zip(first_sums, second_sums)
    )

    d_a = sp.factor(phi_a[3] - phi_a[2])
    d_b = sp.factor(phi_b[3] - phi_b[2])
    e_a = sp.factor(psi_a[3] - psi_a[2])
    e_b = sp.factor(psi_b[3] - psi_b[2])
    D = sp.factor(d_b - d_a)
    E = sp.factor(e_b - e_a)

    assert sp.factor(first_sums[1] - first_sums[0] - D) == 0
    assert sp.factor(first_sums[2] - first_sums[1] - D) == 0
    assert sp.factor(second_sums[1] - second_sums[0] - E) == 0
    assert sp.factor(second_sums[2] - second_sums[1] - E) == 0
    assert sp.factor(
        (equations[2] - equations[1])
        - (equations[1] - equations[0])
        - 2 * D**2
    ) == 0

    # For mu != 0, D=0 forces a^2=b^2.  If one formally allows mu=0,
    # the remaining second-jet increment E supplies the same conclusion.
    assert sp.factor(
        D
        + 2
        * mu
        * (a - b)
        * (a + b)
        / (
            (a - mu)
            * (a + mu)
            * (b - mu)
            * (b + mu)
        )
    ) == 0
    assert sp.factor(E.subs(mu, 0) - (2 / b**2 - 2 / a**2)) == 0


def main() -> None:
    check_profile_and_legal_cores()
    check_universal_baseline_and_exact_pole()
    check_order_two_logarithmic_formula()
    check_role_drop_and_three_subset_forcing()
    check_two_quartic_consecutive_swap()
    print("eighth-split (4,4,3,3,3,3) order-two closure: PASS")
    print("twelve legal (3,3,2) cores and constant residuals: exact")
    print("common-pole first/second log jets and role drop: exact")
    print("four triple values in one degree-two Phi_3 fibre: impossible")
    print("two-quartic consecutive-swap cross-check: exact")


if __name__ == "__main__":
    main()

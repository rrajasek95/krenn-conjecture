#!/usr/bin/env python3
"""Exact audit of the adjacent-Euler/colon/Hankel type separation.

This checker uses only the Python standard library.  It verifies the
derived two-coordinate cycle in the suspended all-27-row guard, its
orientation, and the elementary representation-weight ledger.  The
literal 27 source rows are audited by verify_full_27_colon_cycle_guard.py.
This checker does not construct the missing filtered Bockstein or
filtered-to-Hankel maps.
"""

from fractions import Fraction
from math import factorial


Poly = dict[int, Fraction]


def clean(p: Poly) -> Poly:
    return {m: c for m, c in p.items() if c}


def add(*polys: Poly) -> Poly:
    out: Poly = {}
    for p in polys:
        for mask, coeff in p.items():
            out[mask] = out.get(mask, Fraction(0)) + coeff
    return clean(out)


def scale(p: Poly, scalar: Fraction | int) -> Poly:
    scalar = Fraction(scalar)
    return clean({mask: scalar * coeff for mask, coeff in p.items()})


def mul(p: Poly, q: Poly) -> Poly:
    out: Poly = {}
    for mask_p, coeff_p in p.items():
        for mask_q, coeff_q in q.items():
            if mask_p & mask_q:
                continue
            mask = mask_p | mask_q
            out[mask] = out.get(mask, Fraction(0)) + coeff_p * coeff_q
    return clean(out)


def variable(index: int) -> Poly:
    return {1 << index: Fraction(1)}


def monomial(coeff: Fraction | int, *indices: int) -> Poly:
    mask = 0
    for index in indices:
        bit = 1 << index
        if mask & bit:
            return {}
        mask |= bit
    return {mask: Fraction(coeff)}


def power(p: Poly, exponent: int) -> Poly:
    out: Poly = {0: Fraction(1)}
    for _ in range(exponent):
        out = mul(out, p)
    return out


def divided_power(p: Poly, exponent: int) -> Poly:
    return scale(power(p, exponent), Fraction(1, factorial(exponent)))


def require(condition: bool, message: str) -> None:
    """Raise independently of Python's ``assert`` optimization setting."""
    if not condition:
        raise RuntimeError(message)


def base_radial() -> Poly:
    return add(
        monomial(4, 1, 2),
        monomial(1, 1, 3),
        monomial(1, 2, 4),
    )


def old_guard_forms() -> tuple[tuple[Poly, Poly], tuple[Poly, Poly]]:
    """Return the two relevant y- and t-stars in the fixed e=0,a=1 chart."""
    y = (
        add(variable(0), variable(2)),
        scale(variable(1), -1),
    )
    t = (
        add(scale(variable(2), -1), variable(3), variable(4)),
        variable(4),
    )
    return y, t


def oriented_weighted_pair(e: int, a: int) -> tuple[Poly, Poly]:
    """Derive omega and Gamma_b for the ordered pair (e,a), with b=2."""
    require({e, a} == {0, 1}, "the weighted pair must order colours 0 and 1")
    y, t = old_guard_forms()
    p_b = (Fraction(3, 2), Fraction(1, 2))
    r_b = (Fraction(-2), Fraction(-2))
    t_block = ((Fraction(-9), Fraction(-1)), (Fraction(1), Fraction(-3)))
    b_entry = t_block[e][a]
    c_entry = t_block[a][e]

    omega = add(
        scale(mul(y[e], t[a]), c_entry),
        scale(mul(y[a], t[e]), -b_entry),
    )
    gamma = add(
        scale(t[a], c_entry * p_b[e]),
        scale(y[e], c_entry * r_b[a]),
        scale(t[e], -b_entry * p_b[a]),
        scale(y[a], -b_entry * r_b[e]),
    )
    return omega, gamma


def suspension_factor(h: int) -> Poly:
    out: Poly = {0: Fraction(1)}
    for r in range(h - 3):
        out = mul(out, monomial(1, 5 + 2 * r, 6 + 2 * r))
    return out


def guard_data(h: int) -> tuple[Poly, Poly, Poly, Poly]:
    """Return z_h, x_b, omega, Gamma_b from the rational suspended guard."""
    require(h >= 3, "h must be at least three")
    z = base_radial()
    for r in range(h - 3):
        z = add(z, monomial(1, 5 + 2 * r, 6 + 2 * r))

    x_b = monomial(Fraction(1, 2), 3)
    omega = add(
        monomial(1, 0, 4),
        monomial(1, 2, 4),
        monomial(1, 1, 2),
        monomial(-1, 1, 3),
        monomial(-1, 1, 4),
    )
    displayed_gamma = add(
        monomial(-2, 0),
        monomial(2, 1),
        monomial(Fraction(-5, 2), 2),
        monomial(Fraction(1, 2), 3),
        monomial(2, 4),
    )
    source_omega, source_gamma = oriented_weighted_pair(0, 1)
    require(source_omega == omega, "displayed omega has the wrong orientation")
    require(source_gamma == displayed_gamma, "displayed Gamma_b has the wrong sign")
    return z, x_b, omega, displayed_gamma


def check_euler_boundaries_and_colon_class() -> None:
    for h in range(3, 10):
        z, x_b, omega, gamma = guard_data(h)
        z_0 = base_radial()
        z_h_minus_2 = divided_power(z, h - 2)
        z_h_minus_1 = divided_power(z, h - 1)
        suspended_matching = suspension_factor(h)
        q_h = add(
            *(
                monomial(1, 5 + 2 * r, 6 + 2 * r)
                for r in range(h - 3)
            )
        )
        require(
            divided_power(q_h, h - 3) == suspended_matching,
            f"wrong matching divided-power coefficient at h={h}",
        )
        for old_site in range(5):
            old_linear = variable(old_site)
            require(
                mul(old_linear, z_h_minus_1)
                == mul(mul(old_linear, divided_power(z_0, 2)), suspended_matching),
                f"old-linear suspension identity failed at h={h}, u{old_site}",
            )

        # The full-27 pair is a cycle in d_h(C,Gamma)
        # = C z^[h-2] + Gamma z^[h-1].
        colon_first = mul(x_b, omega)
        colon_first_value = mul(colon_first, z_h_minus_2)
        colon_second_value = mul(gamma, z_h_minus_1)
        top = mul(monomial(1, 0, 1, 2, 3, 4), suspended_matching)
        require(
            colon_first_value == scale(top, 2),
            f"wrong positive colon summand at h={h}",
        )
        require(
            colon_second_value == scale(top, -2),
            f"wrong negative companion summand at h={h}",
        )
        require(
            colon_first_value == mul(mul(colon_first, z_0), suspended_matching),
            f"cubic-star suspension identity failed at h={h}",
        )
        require(
            colon_second_value
            == mul(mul(gamma, divided_power(z_0, 2)), suspended_matching),
            f"direct-star suspension identity failed at h={h}",
        )
        colon_value = add(colon_first_value, colon_second_value)
        require(not colon_value, f"full-27 colon equation failed at h={h}")

        # b_h(a)=(a z,-(h-1)a) is an Euler boundary.
        kappa = Fraction(7, 3)
        a = scale(x_b, kappa)
        boundary_first = mul(a, z)
        boundary_second = scale(a, -(h - 1))
        boundary_value = add(
            mul(boundary_first, z_h_minus_2),
            mul(boundary_second, z_h_minus_1),
        )
        require(not boundary_value, f"upper Euler boundary failed at h={h}")
        require(
            not add(scale(boundary_first, h - 1), mul(boundary_second, z)),
            f"upper boundary failed its coefficient criterion at h={h}",
        )

        # The connection/normal bracket is the same boundary one layer down.
        # Choose an arbitrary old quadratic delta*v, then multiply by x_b.
        delta_v = add(monomial(2, 0, 1), monomial(-3, 2, 4))
        lower_a = mul(x_b, delta_v)
        lower_first = mul(lower_a, z)
        lower_second = scale(lower_a, -(h - 2))
        lower_value = add(
            mul(lower_first, divided_power(z, h - 3)),
            mul(lower_second, z_h_minus_2),
        )
        require(not lower_value, f"lower Euler boundary failed at h={h}")

        # A cycle (C,Gamma) is an Euler boundary only if
        # (h-1)C+Gamma*z vanishes.  The guard has a uniform nonzero defect.
        defect = add(scale(colon_first, h - 1), mul(gamma, z))
        require(defect, f"colon boundary defect vanished at h={h}")
        recovered_a = scale(gamma, Fraction(-1, h - 1))
        require(
            scale(recovered_a, -(h - 1)) == gamma,
            f"second coordinate did not recover the boundary candidate at h={h}",
        )
        first_coordinate_mismatch = add(
            colon_first,
            scale(mul(recovered_a, z), -1),
        )
        require(
            first_coordinate_mismatch == scale(defect, Fraction(1, h - 1)),
            f"boundary iff criterion has the wrong sign at h={h}",
        )
        require(
            first_coordinate_mismatch,
            f"nonboundary pair acquired a boundary preimage at h={h}",
        )
        witness_mask = (1 << 0) | (1 << 3) | (1 << 4)
        expected = Fraction(h - 1, 2)
        require(
            defect.get(witness_mask, Fraction(0)) == expected,
            f"wrong u0*u3*u4 defect coefficient at h={h}",
        )
        require(
            not mul(defect, z_h_minus_2),
            f"colon defect is not killed by z^[h-2] at h={h}",
        )

        # Reversing the ordered (e,a) residual reverses omega, Gamma_b,
        # the cycle, and its defect, but leaves the complementary colour b.
        reversed_omega, reversed_gamma = oriented_weighted_pair(1, 0)
        require(
            reversed_omega == scale(omega, -1)
            and reversed_gamma == scale(gamma, -1),
            f"weighted residual did not reverse by a common sign at h={h}",
        )
        reversed_first = mul(x_b, reversed_omega)
        reversed_cycle = add(
            mul(reversed_first, z_h_minus_2),
            mul(reversed_gamma, z_h_minus_1),
        )
        reversed_defect = add(
            scale(reversed_first, h - 1),
            mul(reversed_gamma, z),
        )
        require(not reversed_cycle, f"reversed colon cycle failed at h={h}")
        require(
            reversed_defect == scale(defect, -1),
            f"reversed boundary defect has the wrong sign at h={h}",
        )
        require(
            reversed_defect.get(witness_mask, Fraction(0)) == -expected,
            f"reversed witness coefficient has the wrong sign at h={h}",
        )


def sl2_summand_orders(left: int, right: int) -> list[int]:
    """Orders in Sym^left tensor Sym^right, each with multiplicity one."""
    require(left >= 0 and right >= 0, "symmetric orders must be nonnegative")
    return list(range(left + right, abs(left - right) - 1, -2))


def check_parameter_types() -> None:
    """Audit exact orders and central characters on the three binary lines."""
    for h in range(3, 41):
        hankel_order = 2 * h - 1
        missing_order = hankel_order - 2

        require(hankel_order % 2 == 1, f"Hankel order is not odd at h={h}")
        require(missing_order == 2 * h - 3, f"wrong missing order at h={h}")
        require(missing_order % 2 == 1, f"missing covariant is not odd at h={h}")

        # Exact type triples are symmetric orders on
        # (U_clean,U_selector,U_transverse).  Dual/determinant variance is
        # deliberately suppressed here; parity records the independent
        # SL(2) central characters.
        selector_quadratic = (0, 2, 0)
        contracted_colon_cycle = (0, 0, 0)
        curvature = (0, 0, 1)
        ordered_transverse_endpoint = (0, 0, 1)
        physical_site_factor = (0, 0, 0)
        chosen_scalar_zero_lift = (1, 0, 0)
        hankel_target = (hankel_order, 0, 0)
        require(selector_quadratic == (0, 2, 0), "wrong selector order")
        require(contracted_colon_cycle == (0, 0, 0), "colon retained a parameter")
        require(physical_site_factor == (0, 0, 0), "site degree became binary order")
        require(chosen_scalar_zero_lift == (1, 0, 0), "wrong conditional lift order")

        transverse_decomposition = sl2_summand_orders(
            curvature[2], ordered_transverse_endpoint[2]
        )
        require(
            transverse_decomposition == [2, 0],
            f"wrong transverse tensor decomposition at h={h}",
        )
        transverse_bracket = (0, 0, transverse_decomposition[-1])
        selector_parity = tuple(order % 2 for order in selector_quadratic)
        bracket_parity = tuple(order % 2 for order in transverse_bracket)
        hankel_parity = tuple(order % 2 for order in hankel_target)
        require(
            transverse_bracket == (0, 0, 0),
            f"transverse bracket has wrong central type at h={h}",
        )
        require(
            selector_parity == (0, 0, 0)
            and bracket_parity == (0, 0, 0),
            f"an available even datum acquired odd central type at h={h}",
        )
        require(
            hankel_parity == (1, 0, 0)
            and bracket_parity != hankel_parity,
            f"transverse bracket accidentally acquired clean odd type at h={h}",
        )
        require(
            selector_quadratic[0] == 0 and hankel_target[0] == hankel_order,
            f"independent selector and clean groups were conflated at h={h}",
        )

        # Clebsch--Gordan:
        # Sym^2 tensor Sym^d contains Sym^D only for d=D-2,D,D+2.
        admissible_auxiliary_orders = [
            auxiliary
            for auxiliary in range(hankel_order + 3)
            if hankel_order in sl2_summand_orders(2, auxiliary)
        ]
        require(
            admissible_auxiliary_orders
            == [missing_order, hankel_order, hankel_order + 2],
            f"wrong Clebsch--Gordan slots at h={h}: {admissible_auxiliary_orders}",
        )
        require(
            admissible_auxiliary_orders[0] == 2 * h - 3
            and hankel_order not in sl2_summand_orders(2, 1),
            f"a scalar or lone endpoint incorrectly reaches Hankel order at h={h}",
        )
        require(
            sl2_summand_orders(2, missing_order)[0] == hankel_order,
            f"the minimal slot is not the Cartan summand at h={h}",
        )
        scalar_zero_veronese = tuple(
            missing_order * order for order in chosen_scalar_zero_lift
        )
        require(
            scalar_zero_veronese == (missing_order, 0, 0)
            and tuple(order % 2 for order in scalar_zero_veronese) == (1, 0, 0),
            f"wrong Veronese type for the conditional scalar-zero lift at h={h}",
        )


def main() -> None:
    check_euler_boundaries_and_colon_class()
    check_parameter_types()
    print(
        "PASS: adjacent Euler boundaries, non-Euler full-27 colon class, "
        "and clean/selector/transverse Hankel type mismatch"
    )


if __name__ == "__main__":
    main()

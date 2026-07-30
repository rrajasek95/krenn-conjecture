#!/usr/bin/env python3
"""Exact checks for the off-diagonal same-power target--residue lock.

This script audits normalizations and sparse site-square-zero expansions in
``notes/offdiagonal-same-power-target-residue-lock.md``.  The proof in that
note is uniform; the finite loop here is only an implementation check.
"""

from fractions import Fraction
from math import factorial


def require(condition, message):
    """Optimization-safe assertion."""
    if not condition:
        raise RuntimeError(message)


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
            if result[monomial] == 0:
                del result[monomial]
    return result


def scale(polynomial, scalar):
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in polynomial.items()
        if scalar * coefficient != 0
    }


def multiply(*polynomials):
    require(polynomials, "multiply needs input")
    result = {(): Fraction(1)}
    for right in polynomials:
        product = {}
        for left_monomial, left_coefficient in result.items():
            left_sites = {site for site, _colour in left_monomial}
            for right_monomial, right_coefficient in right.items():
                right_sites = {site for site, _colour in right_monomial}
                if left_sites & right_sites:
                    continue
                monomial = tuple(sorted(left_monomial + right_monomial))
                product[monomial] = (
                    product.get(monomial, Fraction(0))
                    + left_coefficient * right_coefficient
                )
                if product[monomial] == 0:
                    del product[monomial]
        result = product
    return result


def divided_power(polynomial, exponent):
    result = {(): Fraction(1)}
    for _unused in range(exponent):
        result = multiply(result, polynomial)
    return scale(result, Fraction(1, factorial(exponent)))


def variable(site, colour, coefficient=Fraction(1)):
    return {((site, colour),): coefficient}


def coefficient_at_site(polynomial, site, colour):
    result = {}
    for monomial, coefficient in polynomial.items():
        marker = (site, colour)
        if marker not in monomial:
            continue
        reduced = tuple(item for item in monomial if item != marker)
        result[reduced] = result.get(reduced, Fraction(0)) + coefficient
    return {key: value for key, value in result.items() if value != 0}


def sparse_odd_quadratic(h):
    """A sparse q0 with several near-perfect matching layers."""
    site_count = 2 * h - 1
    terms = []
    for offset in (0, 1):
        for index in range(h - 1):
            left = (2 * index + offset) % site_count
            right = (2 * index + 1 + offset) % site_count
            if left == right:
                continue
            terms.append(
                multiply(
                    variable(left, offset),
                    variable(right, offset),
                )
            )
    return add(*terms)


def check_divided_power_exposure():
    for h in range(3, 8):
        exposed = 2 * h - 1
        q0 = sparse_odd_quadratic(h)
        t = [
            add(
                variable((colour + 1) % (2 * h - 1), colour),
                variable((colour + 3) % (2 * h - 1), (colour + 1) % 3),
            )
            for colour in range(3)
        ]
        rho_terms = [multiply(variable(exposed, colour), t[colour]) for colour in range(3)]
        rho = add(*rho_terms)
        q = add(q0, rho)

        a_power = divided_power(q0, h - 1)
        b_power = divided_power(q0, h - 2)
        expansion = add(a_power, *[
            multiply(variable(exposed, colour), t[colour], b_power)
            for colour in range(3)
        ])
        require(
            divided_power(q, h - 1) == expansion,
            f"wrong exposed divided-power coefficient at h={h}",
        )
        require(
            multiply(q0, b_power) == scale(a_power, h - 1),
            f"wrong q0*B factor at h={h}",
        )

        qbar = add(
            multiply(variable(0, 2), variable(2, 1),),
            scale(multiply(variable(1, 0), variable(4, 2)), Fraction(-3, 5)),
        )
        ell = [
            add(variable((colour + 2) % (2 * h - 1), colour),
                scale(variable((colour + 4) % (2 * h - 1), 2 - colour), Fraction(2, 7)))
            for colour in range(3)
        ]
        quadratic = add(
            qbar,
            *[multiply(variable(exposed, colour), ell[colour]) for colour in range(3)],
        )
        product = multiply(quadratic, divided_power(q, h - 1))
        for colour in range(3):
            expected = add(
                multiply(ell[colour], a_power),
                multiply(qbar, t[colour], b_power),
            )
            require(
                coefficient_at_site(product, exposed, colour) == expected,
                f"same-power coefficient lock failed at h={h}, c={colour}",
            )


def cap_vector(direct_entry, h, row, column):
    """Coordinates: radial q followed by the nine x_i*y_j products."""
    result = [Fraction(0) for _ in range(10)]
    result[0] = direct_entry
    result[1 + 3 * row + column] = h
    return result


def vector_add(*vectors):
    require(vectors, "vector_add needs input")
    return [sum(entries, Fraction(0)) for entries in zip(*vectors)]


def vector_scale(vector, scalar):
    return [scalar * entry for entry in vector]


def response_vector(matrix):
    result = [Fraction(0) for _ in range(10)]
    for row in range(3):
        for column in range(3):
            result[1 + 3 * row + column] = matrix[row][column]
    return result


def target_vector(row, column, h):
    result = [Fraction(0), Fraction(0), Fraction(0)]
    if row == column:
        result[row] = h
    return result


def check_cap_syzygy_and_lift_normalization():
    samples = (
        # trace nonzero and deliberately not one
        [
            [Fraction(2), Fraction(5, 3), Fraction(-1, 2)],
            [Fraction(7, 4), Fraction(-3), Fraction(2, 5)],
            [Fraction(1, 7), Fraction(-4, 9), Fraction(5)],
        ],
        # trace zero
        [
            [Fraction(2), Fraction(-7, 3), Fraction(1, 4)],
            [Fraction(5, 6), Fraction(-3), Fraction(-2, 9)],
            [Fraction(8, 7), Fraction(3, 11), Fraction(1)],
        ],
    )

    a, b = 0, 1
    for h in range(3, 31):
        for direct in samples:
            alpha = direct[a][b]
            tau = sum((direct[index][index] for index in range(3)), Fraction(0))
            require(alpha != 0, "selected entry vanished")
            caps = [
                [cap_vector(direct[i][j], h, i, j) for j in range(3)]
                for i in range(3)
            ]
            trace_cap = vector_add(caps[0][0], caps[1][1], caps[2][2])
            require(
                tau * caps[a][b][0] == alpha * tau
                and alpha * trace_cap[0] == alpha * tau,
                f"literal cap terms do not both lift alpha*tau*q at h={h}",
            )
            syzygy = vector_add(
                vector_scale(caps[a][b], tau),
                vector_scale(trace_cap, -alpha),
            )

            kstar = [
                [(-alpha if i == j else Fraction(0)) for j in range(3)]
                for i in range(3)
            ]
            kstar[a][b] += tau
            expected = vector_scale(response_vector(kstar), h)
            require(syzygy == expected, f"cap syzygy failed at h={h}, tau={tau}")
            require(syzygy[0] == 0, f"radial term survived at h={h}, tau={tau}")

            trace_target = vector_add(
                target_vector(0, 0, h),
                target_vector(1, 1, h),
                target_vector(2, 2, h),
            )
            syzygy_target = vector_add(
                vector_scale(target_vector(a, b, h), tau),
                vector_scale(trace_target, -alpha),
            )
            normalized_target = vector_scale(syzygy_target, Fraction(1, h * alpha))
            require(
                normalized_target == [Fraction(-1)] * 3,
                f"wrong normalized target at h={h}, tau={tau}",
            )

            normalized_response = vector_scale(expected, Fraction(1, h * alpha))
            for colour in range(3):
                # Ordinary odd residue kills the radial/off-diagonal pieces
                # and sends x_c*y_c to Ybar_c.
                residue = normalized_response[1 + 3 * colour + colour]
                require(
                    residue == -1,
                    f"wrong response residue at h={h}, tau={tau}, c={colour}",
                )
                companion_residue = Fraction(1)
                require(
                    residue + companion_residue == 0,
                    f"same-power target companion failed to lock at h={h}",
                )

            if tau != 0:
                require(
                    vector_scale(caps[a][b], Fraction(1, alpha))[0] == 1
                    and vector_scale(trace_cap, Fraction(1, tau))[0] == 1,
                    f"normalized q lifts have wrong radial symbol at h={h}",
                )
                lift_difference = vector_add(
                    vector_scale(caps[a][b], Fraction(1, alpha)),
                    vector_scale(trace_cap, Fraction(-1, tau)),
                )
                expected_transition = vector_scale(
                    response_vector(kstar), Fraction(h, alpha * tau)
                )
                require(
                    lift_difference == expected_transition,
                    f"q-lift transition normalization failed at h={h}",
                )
                lower_transition = vector_scale(lift_difference, Fraction(1, h))
                require(
                    tau == 1 or lower_transition != normalized_response,
                    f"tau factor was accidentally lost at h={h}",
                )
            else:
                require(
                    vector_scale(caps[a][b], Fraction(1, alpha))[0] == 1
                    and trace_cap[0] == 0
                    and tau * caps[a][b][0] == 0,
                    f"tau=0 lift distinction failed at h={h}",
                )


def check_adjacent_power_overlap_ledger():
    """Audit the curvature/direct-double and connection/normal brackets.

    These are exact adjacent-power source identities.  The checker does not
    assert that a Bockstein connecting morphism has been constructed.
    """
    for h in range(3, 41):
        # Exact rational specialization of the literal formulas in
        # overlapping-pair-cap-bianchi-connection.md.  Here h=m-1 is the
        # canonical-cap coefficient.
        direct_a = Fraction(2 * h + 1, h + 3)
        direct_b = Fraction(3 - h, h + 5)
        direct_c = Fraction(5 * h - 2, 2 * h + 7)
        direct_e = Fraction(h + 4, 3 * h + 1)
        direct_f = Fraction(7 - 2 * h, 4 * h + 3)
        direct_u = Fraction(3 * h + 2, 5 * h + 1)
        star_x = Fraction(h - 5, 2 * h + 3)
        star_y = Fraction(4 * h + 1, 3 * h + 5)
        star_t = Fraction(2 - 3 * h, 5 * h + 7)
        star_v = Fraction(5 * h - 2, 2 * h + 7)
        radial_z = Fraction(7 * h + 1, 4 * h + 9)

        direct_connection = direct_a * star_t - direct_b * star_y
        kappa = direct_a * direct_u - direct_b * direct_f
        dv = direct_connection * star_v
        require(
            direct_connection != 0 and kappa != 0 and dv != 0,
            f"orientation specialization became vacuous at h={h}",
        )

        cap_pq = h * star_x * star_y + direct_a * radial_z
        cap_pr = h * star_x * star_t + direct_b * radial_z
        normal_pq_r = (
            h * (direct_b * star_y + direct_c * star_x)
            + direct_a * star_t
        )
        normal_pr_q = (
            h * (direct_a * star_t + direct_c * star_x)
            + direct_b * star_y
        )
        normal_pq_s = (
            h * (direct_e * star_y + direct_f * star_x)
            + direct_a * star_v
        )
        normal_pr_s = (
            h * (direct_e * star_t + direct_u * star_x)
            + direct_b * star_v
        )
        direct_double_pq = (
            h * (direct_b * direct_f + direct_e * direct_c)
            + direct_a * direct_u
        )
        direct_double_pr = (
            h * (direct_a * direct_u + direct_e * direct_c)
            + direct_b * direct_f
        )

        require(
            cap_pq * star_t - cap_pr * star_y
            == direct_connection * radial_z,
            f"power-free connection orientation failed at h={h}",
        )
        require(
            normal_pq_r - normal_pr_q == -(h - 1) * direct_connection,
            f"normal-connection orientation failed at h={h}",
        )
        require(
            direct_double_pq - direct_double_pr == -(h - 1) * kappa,
            f"direct-double orientation failed at h={h}",
        )
        curvature_left = (
            direct_u * cap_pq
            + star_t * normal_pq_s
            - direct_f * cap_pr
            - star_y * normal_pr_s
        )
        require(
            curvature_left == dv + kappa * radial_z,
            f"curvature orientation failed at h={h}",
        )

        # z*z^[h-2]=(h-1)z^[h-1] and
        # z*z^[h-3]=(h-2)z^[h-2].
        curvature_radial = kappa * (h - 1)
        direct_double = -(h - 1) * kappa
        normal_connection = -(h - 1) * dv
        curvature_connection = dv
        lower_connection = (h - 2) * dv

        require(
            direct_double + curvature_radial == 0,
            f"curvature/direct-double bracket failed at h={h}",
        )
        require(
            normal_connection + curvature_connection + lower_connection == 0,
            f"connection/normal bracket failed at h={h}",
        )
        require(
            direct_double
            + normal_connection
            + curvature_connection
            + curvature_radial
            + lower_connection
            == 0,
            f"complete four-cut adjacent-power ledger failed at h={h}",
        )


def main():
    check_divided_power_exposure()
    check_cap_syzygy_and_lift_normalization()
    check_adjacent_power_overlap_ledger()
    print(
        "PASS: divided-power exposure, cap syzygy, tau lift scaling, "
        "target-residue lock, and adjacent-power overlap signs"
    )


if __name__ == "__main__":
    main()

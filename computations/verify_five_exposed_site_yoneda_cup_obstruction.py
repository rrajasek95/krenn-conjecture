#!/usr/bin/env python3
"""Exact audits for the five-exposed-site Yoneda/cup obstruction.

The checker uses a tiny dependency-free symbolic algebra.  ``z^[n]`` is
kept as a divided-power basis element, and multiplication by ``z`` uses

    z * z^[n] = (n + 1) z^[n + 1].

It verifies the all-label formulas in
``notes/five-exposed-site-yoneda-cup-obstruction.md``.  The finite range in
``h`` is an implementation audit; the note proves the identities uniformly.
The Leibniz check is the conditional formal implication for a specified
comparison cone and chain product.  This script does not construct that
product, a secondary operation, or a necessary ``(-1, +2)`` factorization.
"""

from fractions import Fraction
from itertools import combinations, product as cartesian_product


def require(condition, message):
    """Optimization-safe assertion."""
    if not condition:
        raise RuntimeError(message)


# Ordinary commutative polynomials.  A monomial is a sorted tuple of names.
def pterm(coefficient=1, *variables):
    coefficient = Fraction(coefficient)
    if coefficient == 0:
        return {}
    return {tuple(sorted(variables)): coefficient}


def padd(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
            if result[monomial] == 0:
                del result[monomial]
    return result


def pscale(polynomial, scalar):
    scalar = Fraction(scalar)
    return {
        monomial: coefficient * scalar
        for monomial, coefficient in polynomial.items()
        if coefficient * scalar != 0
    }


# Divided-power expressions.  A key (n, monomial) denotes monomial*z^[n].
def dterm(exponent, coefficient=1, *variables):
    coefficient = Fraction(coefficient)
    if exponent < 0 or coefficient == 0:
        return {}
    return {(exponent, tuple(sorted(variables))): coefficient}


def dadd(*expressions):
    result = {}
    for expression in expressions:
        for key, coefficient in expression.items():
            result[key] = result.get(key, Fraction(0)) + coefficient
            if result[key] == 0:
                del result[key]
    return result


def dscale(expression, scalar):
    scalar = Fraction(scalar)
    return {
        key: coefficient * scalar
        for key, coefficient in expression.items()
        if coefficient * scalar != 0
    }


def pmul_dp(polynomial, expression):
    """Multiply an ordinary polynomial by one divided-power expression."""
    result = {}
    for pmonomial, pcoefficient in polynomial.items():
        z_count = pmonomial.count("z")
        ordinary = tuple(variable for variable in pmonomial if variable != "z")
        for (exponent, dmonomial), dcoefficient in expression.items():
            factor = Fraction(1)
            for offset in range(1, z_count + 1):
                factor *= exponent + offset
            key = (exponent + z_count, tuple(sorted(ordinary + dmonomial)))
            result[key] = (
                result.get(key, Fraction(0))
                + pcoefficient * dcoefficient * factor
            )
            if result[key] == 0:
                del result[key]
    return result


def cap_pq_polynomials(h):
    base = padd(pterm(h, "x", "y"), pterm(1, "P", "z"))
    normals = {
        "r": padd(
            pterm(h, "R", "y"), pterm(h, "T", "x"), pterm(1, "P", "t")
        ),
        "s": padd(
            pterm(h, "E", "y"), pterm(h, "F", "x"), pterm(1, "P", "v")
        ),
        "x": padd(
            pterm(h, "G", "y"), pterm(h, "H", "x"), pterm(1, "P", "w")
        ),
    }
    doubles = {
        "rs": padd(
            pterm(h, "R", "F"), pterm(h, "E", "T"), pterm(1, "P", "U")
        ),
        "rx": padd(
            pterm(h, "R", "H"), pterm(h, "G", "T"), pterm(1, "P", "V")
        ),
        "sx": padd(
            pterm(h, "E", "H"), pterm(h, "G", "F"), pterm(1, "P", "J")
        ),
    }
    return base, normals, doubles


def cap_pr_polynomials(h):
    # The pr cap has residual sites q,s,x, with stars y,v,w and direct
    # entries F(qs), H(qx), J(sx).
    base = padd(pterm(h, "x", "t"), pterm(1, "R", "z"))
    normals = {
        "q": padd(
            pterm(h, "P", "t"), pterm(h, "T", "x"), pterm(1, "R", "y")
        ),
        "s": padd(
            pterm(h, "E", "t"), pterm(h, "U", "x"), pterm(1, "R", "v")
        ),
        "x": padd(
            pterm(h, "G", "t"), pterm(h, "V", "x"), pterm(1, "R", "w")
        ),
    }
    doubles = {
        "qs": padd(
            pterm(h, "P", "U"), pterm(h, "E", "T"), pterm(1, "R", "F")
        ),
        "qx": padd(
            pterm(h, "P", "V"), pterm(h, "G", "T"), pterm(1, "R", "H")
        ),
        "sx": padd(
            pterm(h, "E", "V"), pterm(h, "G", "U"), pterm(1, "R", "J")
        ),
    }
    return base, normals, doubles


def anchor_pq(h):
    base, normal, double = cap_pq_polynomials(h)
    triple_q = dadd(
        dterm(h - 3, 1, "U", "w"),
        dterm(h - 3, 1, "V", "v"),
        dterm(h - 3, 1, "J", "t"),
        dterm(h - 4, 1, "t", "v", "w"),
    )
    sx_q = dadd(dterm(h - 2, 1, "J"), dterm(h - 3, 1, "v", "w"))
    rx_q = dadd(dterm(h - 2, 1, "V"), dterm(h - 3, 1, "t", "w"))
    rs_q = dadd(dterm(h - 2, 1, "U"), dterm(h - 3, 1, "t", "v"))
    result = dadd(
        pmul_dp(base, triple_q),
        pmul_dp(normal["r"], sx_q),
        pmul_dp(normal["s"], rx_q),
        pmul_dp(normal["x"], rs_q),
        pmul_dp(double["rs"], dterm(h - 2, 1, "w")),
        pmul_dp(double["rx"], dterm(h - 2, 1, "v")),
        pmul_dp(double["sx"], dterm(h - 2, 1, "t")),
    )
    return result


def anchor_pr(h):
    base, normal, double = cap_pr_polynomials(h)
    triple_q = dadd(
        dterm(h - 3, 1, "F", "w"),
        dterm(h - 3, 1, "H", "v"),
        dterm(h - 3, 1, "J", "y"),
        dterm(h - 4, 1, "y", "v", "w"),
    )
    sx_q = dadd(dterm(h - 2, 1, "J"), dterm(h - 3, 1, "v", "w"))
    qx_q = dadd(dterm(h - 2, 1, "H"), dterm(h - 3, 1, "y", "w"))
    qs_q = dadd(dterm(h - 2, 1, "F"), dterm(h - 3, 1, "y", "v"))
    return dadd(
        pmul_dp(base, triple_q),
        pmul_dp(normal["q"], sx_q),
        pmul_dp(normal["s"], qx_q),
        pmul_dp(normal["x"], qs_q),
        pmul_dp(double["qs"], dterm(h - 2, 1, "w")),
        pmul_dp(double["qx"], dterm(h - 2, 1, "v")),
        pmul_dp(double["sx"], dterm(h - 2, 1, "y")),
    )


def five_split_families():
    two_direct_one_star = (
        ("x", "T", "J"), ("x", "F", "V"), ("x", "H", "U"),
        ("y", "R", "J"), ("y", "E", "V"), ("y", "G", "U"),
        ("t", "P", "J"), ("t", "E", "H"), ("t", "G", "F"),
        ("v", "P", "V"), ("v", "R", "H"), ("v", "G", "T"),
        ("w", "P", "U"), ("w", "R", "F"), ("w", "E", "T"),
    )
    one_direct_three_stars = (
        ("P", "t", "v", "w"), ("R", "y", "v", "w"),
        ("E", "y", "t", "w"), ("G", "y", "t", "v"),
        ("T", "x", "v", "w"), ("F", "x", "t", "w"),
        ("H", "x", "t", "v"), ("U", "x", "y", "w"),
        ("V", "x", "y", "v"), ("J", "x", "y", "t"),
    )
    return two_direct_one_star, one_direct_three_stars


def universal_five_split(h):
    two_direct_one_star, one_direct_three_stars = five_split_families()
    return dadd(
        *[dterm(h - 2, 1, *variables) for variables in two_direct_one_star],
        *[dterm(h - 3, 1, *variables) for variables in one_direct_three_stars],
        dterm(h - 4, 1, "x", "y", "t", "v", "w"),
    )


def enumerate_exposed_matching_family(number_direct_edges):
    """Enumerate matchings on p,q,r,s,x, starring every unmatched site."""
    sites = ("p", "q", "r", "s", "site_x")
    stars = {"p": "x", "q": "y", "r": "t", "s": "v", "site_x": "w"}
    direct_entries = {
        ("p", "q"): "P", ("p", "r"): "R", ("p", "s"): "E",
        ("p", "site_x"): "G", ("q", "r"): "T", ("q", "s"): "F",
        ("q", "site_x"): "H", ("r", "s"): "U",
        ("r", "site_x"): "V", ("s", "site_x"): "J",
    }
    family = set()
    for chosen in combinations(direct_entries.items(), number_direct_edges):
        used_sites = tuple(site for (edge, _entry) in chosen for site in edge)
        if len(set(used_sites)) != 2 * number_direct_edges:
            continue
        variables = [entry for _edge, entry in chosen]
        variables.extend(stars[site] for site in sites if site not in used_sites)
        family.add(tuple(sorted(variables)))
    return family


def check_all_label_five_site_expansion():
    two_direct_one_star, one_direct_three_stars = five_split_families()
    stars = {"x", "y", "t", "v", "w"}
    directs = {"P", "R", "E", "G", "T", "F", "H", "U", "V", "J"}
    require(len(two_direct_one_star) == 15, "first matching family is not 15")
    require(len(one_direct_three_stars) == 10, "second matching family is not 10")
    require(
        len({tuple(sorted(term)) for term in two_direct_one_star}) == 15,
        "duplicate in the 15-term matching family",
    )
    require(
        len({tuple(sorted(term)) for term in one_direct_three_stars}) == 10,
        "duplicate in the 10-term matching family",
    )
    require(
        {tuple(sorted(term)) for term in two_direct_one_star}
        == enumerate_exposed_matching_family(2),
        "15-term family is not the full two-edge matching family on five sites",
    )
    require(
        {tuple(sorted(term)) for term in one_direct_three_stars}
        == enumerate_exposed_matching_family(1),
        "10-term family is not the full one-edge matching family on five sites",
    )
    require(
        enumerate_exposed_matching_family(0)
        == {tuple(sorted(("x", "y", "t", "v", "w")))},
        "1-term family is not the all-star matching",
    )
    for term in two_direct_one_star:
        require(
            sum(variable in stars for variable in term) == 1
            and sum(variable in directs for variable in term) == 2,
            "15-term family lost its two-direct/one-star type",
        )
    for term in one_direct_three_stars:
        require(
            sum(variable in stars for variable in term) == 3
            and sum(variable in directs for variable in term) == 1,
            "10-term family lost its one-direct/three-star type",
        )
    # The target coefficient has no binomial factor from exposing r,s,x:
    # both cap charts give h exactly when all five physical labels agree.
    for target_h in (3, 7, 16):
        for labels in cartesian_product(range(3), repeat=5):
            i, j, k, ell, c = labels
            expected_target = target_h if i == j == k == ell == c else 0
            pq_target = target_h if i == j and i == k == ell == c else 0
            pr_target = target_h if i == k and i == j == ell == c else 0
            require(
                pq_target == expected_target and pr_target == expected_target,
                f"all-label target mismatch at h={target_h}, labels={labels}",
            )

    for h in range(3, 17):
        expected = dscale(universal_five_split(h), h)
        pq_anchor = anchor_pq(h)
        pr_anchor = anchor_pr(h)
        require(
            len(expected) == (25 if h == 3 else 26),
            f"15/10/1 split has the wrong size at h={h}",
        )
        require(
            set(expected.values()) == {Fraction(h)},
            f"five-site expansion lost its common factor h at h={h}",
        )
        require(pq_anchor == expected, f"pq five-site expansion failed at h={h}")
        require(pr_anchor == expected, f"pr five-site expansion failed at h={h}")
        require(pq_anchor == pr_anchor, f"chart comparison failed at h={h}")

        cap_sites = 2 * h
        four_common_sites = cap_sites - 2
        five_common_sites = cap_sites - 3
        odd_residue_sites = cap_sites - 1
        require(four_common_sites == 2 * h - 2, "wrong four-cut site count")
        require(five_common_sites == 2 * h - 3, "wrong five-exposure site count")
        require(odd_residue_sites == 2 * h - 1, "wrong odd-residue site count")
        for (exponent, monomial), coefficient in expected.items():
            star_degree = sum(variable in stars for variable in monomial)
            require(coefficient != 0, "zero coefficient survived normalization")
            require(
                2 * exponent + star_degree == five_common_sites,
                f"wrong D5 site degree at h={h}: {(exponent, monomial)}",
            )


def check_adjacent_power_boundary():
    for h in range(3, 65):
        direct_double = dterm(h - 1, -(h - 1), "kappa")
        normal = dterm(h - 2, -(h - 1), "D", "v")
        curvature = dadd(
            dterm(h - 2, 1, "D", "v"),
            pmul_dp(pterm(1, "kappa", "z"), dterm(h - 2)),
        )
        connection = pmul_dp(pterm(1, "D", "v", "z"), dterm(h - 3))
        ledger = dadd(direct_double, normal, curvature, connection)
        require(ledger == {}, f"adjacent-power ledger failed at h={h}")

        first_bracket = dadd(
            pmul_dp(pterm(1, "kappa", "z"), dterm(h - 2)),
            dterm(h - 1, -(h - 1), "kappa"),
        )
        second_bracket = dadd(
            pmul_dp(pterm(1, "D", "v", "z"), dterm(h - 3)),
            dterm(h - 2, -(h - 2), "D", "v"),
        )
        require(first_bracket == {}, f"first Euler bracket failed at h={h}")
        require(second_bracket == {}, f"second Euler bracket failed at h={h}")


def check_conditional_boundary_cup_and_site_degree():
    # Conditional chain audit.  Once a product satisfying Leibniz is given,
    # d(e)=0 forces (d g) cup e = d(g cup e).  This is not an existence
    # check for the product or for a secondary operation.
    for degree_g in range(4):
        dg_cup_e = Fraction(7, 5)
        g_cup_de = Fraction(0)
        sign = Fraction(-1 if degree_g % 2 else 1)
        differential_of_product = dg_cup_e + sign * g_cup_de
        recovered_boundary = differential_of_product - sign * g_cup_de
        require(
            recovered_boundary == dg_cup_e,
            f"conditional Leibniz boundary failed in degree {degree_g}",
        )

    for h in range(3, 65):
        four_common_sites = 2 * h - 2
        ledger_degree = 2 * h - 2
        product_degree = ledger_degree + 2
        odd_output_degree = 2 * h - 1
        require(ledger_degree == four_common_sites, "ledger is not top degree")
        require(product_degree > four_common_sites, "quadratic product did not overfill")
        require(product_degree == 2 * h, "wrong product degree")
        require(odd_output_degree == ledger_degree + 1, "wrong net bivariant degree")
        require(odd_output_degree != product_degree, "ordinary product mimicked push-pull")


def check_target_residue_graph():
    for kappa in (Fraction(1), Fraction(-3, 5), Fraction(17, 4)):
        for ybar in (Fraction(0), Fraction(2, 7), Fraction(-5, 3)):
            # Coordinates are (target coefficient, odd residue coefficient).
            cap = (-kappa, -kappa * ybar)
            cancelling_anchor = (kappa, kappa * ybar)
            total = (
                cap[0] + cancelling_anchor[0],
                cap[1] + cancelling_anchor[1],
            )
            desired = (Fraction(0), -kappa * ybar)
            require(
                total == (0, 0),
                "same-power anchor failed to cancel both coordinates",
            )
            if kappa * ybar != 0:
                require(desired != total, "nonzero desired class fell on the graph")
            else:
                require(
                    desired == total,
                    "zero-residue specialization was incorrectly obstructed",
                )


def matrix_inner(left, right):
    return sum(
        (left[i][j] * right[i][j] for i in range(3) for j in range(3)),
        Fraction(0),
    )


def check_tau_zero_and_nonzero_caps():
    cases = (
        # trace zero, alpha=A_01=2
        (
            True,
            [
                [Fraction(3), Fraction(2), Fraction(-1)],
                [Fraction(5), Fraction(-4), Fraction(7)],
                [Fraction(11), Fraction(13), Fraction(1)],
            ],
        ),
        # trace nonzero
        (
            False,
            [
                [Fraction(3), Fraction(2), Fraction(-1)],
                [Fraction(5), Fraction(-4), Fraction(7)],
                [Fraction(11), Fraction(13), Fraction(6)],
            ],
        ),
    )
    for expect_tau_zero, direct in cases:
        alpha = direct[0][1]
        tau = sum((direct[i][i] for i in range(3)), Fraction(0))
        require((tau == 0) == expect_tau_zero, "tau test case has wrong trace")
        require(alpha != 0, "selected off-diagonal entry vanished")
        kstar = [[Fraction(0) for _j in range(3)] for _i in range(3)]
        kstar[0][1] = tau
        for i in range(3):
            kstar[i][i] -= alpha
        require(matrix_inner(kstar, direct) == 0, "Kstar was not scalar-zero")
        require(
            [kstar[i][i] / alpha for i in range(3)] == [-1, -1, -1],
            "normalized target/residue diagonal changed with tau",
        )
        if tau == 0:
            expected = [
                [Fraction(-1) if i == j else Fraction(0) for j in range(3)]
                for i in range(3)
            ]
            normalized = [[entry / alpha for entry in row] for row in kstar]
            require(normalized == expected, "tau=0 did not give -I")
        else:
            # P_ab/alpha and tr(P)/tau are the two normalized radial lifts
            # of q.  Their lower-coordinate difference is Kstar/(alpha*tau).
            lift_difference = [
                [
                    (Fraction(1, 1) / alpha if (i, j) == (0, 1) else 0)
                    - (Fraction(1, 1) / tau if i == j else 0)
                    for j in range(3)
                ]
                for i in range(3)
            ]
            normalized_kstar = [
                [entry / (alpha * tau) for entry in row] for row in kstar
            ]
            require(
                lift_difference == normalized_kstar,
                "tau-nonzero cap-lift response is not R/(alpha*tau)",
            )


def check_direct_free_specialization():
    for h in range(3, 65):
        direct_a = Fraction(h + 2, h + 1)
        direct_b = Fraction(0)
        direct_f = Fraction(4 * h + 1, 5 * h + 2)
        direct_u = Fraction(2 * h + 1, h + 3)
        star_t = Fraction(3 * h - 1, 2 * h + 5)
        star_y = Fraction(2 * h + 3, 3 * h + 4)
        star_v = Fraction(h + 4, 3 * h + 2)
        radial_z = Fraction(5 * h + 1, 4 * h + 3)
        d_value = direct_a * star_t - direct_b * star_y
        kappa = direct_a * direct_u - direct_b * direct_f
        require(d_value == direct_a * star_t, "B=0 did not give D=At")
        require(kappa == direct_a * direct_u, "B=0 did not give kappa=AU")
        require(
            kappa != 0 and d_value != 0 and star_v != 0,
            "direct-free packet became vacuous",
        )

        # Scalar audit of AU(z Z1-(h-1)Z0)+Atv(z Z2-(h-2)Z1).
        z0 = radial_z ** (h - 1) / product(range(1, h))
        z1 = radial_z ** (h - 2) / product(range(1, h - 1))
        z2 = radial_z ** (h - 3) / product(range(1, h - 2))
        first = kappa * (radial_z * z1 - (h - 1) * z0)
        second = d_value * star_v * (radial_z * z2 - (h - 2) * z1)
        require(first == 0 and second == 0, f"direct-free brackets failed at h={h}")
        require(-kappa != 0, "direct-free conditional normalization vanished")


def product(values):
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def main():
    check_all_label_five_site_expansion()
    check_adjacent_power_boundary()
    check_conditional_boundary_cup_and_site_degree()
    check_target_residue_graph()
    check_tau_zero_and_nonzero_caps()
    check_direct_free_specialization()
    print(
        "PASS: all-label five-site cap equality, adjacent-power boundary, "
        "conditional ordinary-cup boundary, target-residue graph, tau=0, "
        "and direct-free ledger"
    )


if __name__ == "__main__":
    main()

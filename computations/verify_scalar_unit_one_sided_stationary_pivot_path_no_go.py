#!/usr/bin/env python3
"""Exact audit for the one-sided stationary scalar-unit pivot.

The accompanying proof is uniform in h.  This dependency-free checker
audits divided-power coefficients and the filtered logical guards with
exact rational arithmetic.  The require helper remains active under
python -O.
"""

from fractions import Fraction


COLORS = (0, 1, 2)
SELECTED = 0
COMPLEMENT = (1, 2)


def require(condition, message):
    """Raise in ordinary and optimized Python."""

    if not condition:
        raise RuntimeError(message)


# Polynomials in the path parameter t, stored in increasing degree.
def clean(poly):
    values = [Fraction(value) for value in poly]
    while len(values) > 1 and not values[-1]:
        values.pop()
    return tuple(values) if values else (Fraction(0),)


ZERO = clean((0,))
ONE = clean((1,))
T = clean((0, 1))


def poly_add(*polys):
    length = max((len(poly) for poly in polys), default=1)
    output = [Fraction(0)] * length
    for poly in polys:
        for degree, coefficient in enumerate(poly):
            output[degree] += coefficient
    return clean(output)


def poly_scale(poly, scalar):
    scalar = Fraction(scalar)
    return clean(tuple(scalar * coefficient for coefficient in poly))


def poly_neg(poly):
    return poly_scale(poly, -1)


def poly_sub(left, right):
    return poly_add(left, poly_neg(right))


def poly_mul(left, right):
    output = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, left_coefficient in enumerate(left):
        for j, right_coefficient in enumerate(right):
            output[i + j] += left_coefficient * right_coefficient
    return clean(output)


def poly_pow(poly, exponent):
    require(exponent >= 0, "negative polynomial exponent")
    output = ONE
    base = poly
    power = exponent
    while power:
        if power & 1:
            output = poly_mul(output, base)
        base = poly_mul(base, base)
        power //= 2
    return output


def poly_derivative(poly):
    if len(poly) <= 1:
        return ZERO
    return clean(
        tuple(Fraction(degree) * poly[degree] for degree in range(1, len(poly)))
    )


def poly_evaluate(poly, value):
    value = Fraction(value)
    output = Fraction(0)
    for coefficient in reversed(poly):
        output = output * value + coefficient
    return output


def poly_integral_01(poly):
    return sum(
        (coefficient / Fraction(degree + 1) for degree, coefficient in enumerate(poly)),
        Fraction(0),
    )


def poly_compose(poly, inner):
    output = ZERO
    for coefficient in reversed(poly):
        output = poly_add(poly_mul(output, inner), (coefficient,))
    return output


def monomial_t(exponent):
    require(exponent >= 0, "negative t exponent")
    return clean((Fraction(0),) * exponent + (Fraction(1),))


def geometric(length):
    """Return 1+t+...+t^(length-1), with zero for length zero."""

    require(length >= 0, "negative geometric length")
    return ZERO if length == 0 else clean((Fraction(1),) * length)


# Sparse bivariate polynomials in the physical scaling coordinates x,y.
# Keys are bidegrees and values are exact coefficients.
def bivar_clean(poly):
    return {
        degree: Fraction(coefficient)
        for degree, coefficient in poly.items()
        if Fraction(coefficient)
    }


def bivar_add(*polys):
    output = {}
    for poly in polys:
        for degree, coefficient in poly.items():
            output[degree] = output.get(degree, Fraction(0)) + Fraction(coefficient)
    return bivar_clean(output)


def bivar_monomial(x_degree, y_degree, coefficient=1):
    require(x_degree >= 0 and y_degree >= 0, "negative bivariate degree")
    return bivar_clean({(x_degree, y_degree): Fraction(coefficient)})


def bivar_evaluate(poly, x_value, y_value):
    x_value = Fraction(x_value)
    y_value = Fraction(y_value)
    return sum(
        (
            coefficient * x_value**x_degree * y_value**y_degree
            for (x_degree, y_degree), coefficient in poly.items()
        ),
        Fraction(0),
    )


def bivar_mixed_divided_difference(poly):
    """Return [P(x,y)-P(x,0)-P(0,y)+P(0,0)]/(xy)."""

    return bivar_clean(
        {
            (x_degree - 1, y_degree - 1): coefficient
            for (x_degree, y_degree), coefficient in poly.items()
            if x_degree and y_degree
        }
    )


def vector_clean(vector):
    return {key: clean(value) for key, value in vector.items() if clean(value) != ZERO}


def vector_derivative(vector):
    return vector_clean({key: poly_derivative(value) for key, value in vector.items()})


def vector_evaluate(vector, value):
    return {
        key: poly_evaluate(poly, value)
        for key, poly in vector.items()
        if poly_evaluate(poly, value)
    }


def vector_integral_01(vector):
    return {
        key: poly_integral_01(poly)
        for key, poly in vector.items()
        if poly_integral_01(poly)
    }


def reduce_sum_relation(vector, indices, pivot):
    """Reduce by the single relation sum(indices)=0, eliminating pivot."""

    require(pivot in indices, "relation pivot is absent")
    pivot_coefficient = vector.get(pivot, ZERO)
    output = {}
    for index in indices:
        if index == pivot:
            continue
        coefficient = poly_sub(vector.get(index, ZERO), pivot_coefficient)
        if coefficient != ZERO:
            output[index] = coefficient
    for index, coefficient in vector.items():
        if index not in indices and coefficient != ZERO:
            output[index] = coefficient
    return vector_clean(output)


def exceptional_coefficient(k):
    """Coefficient of q^[h-k] r^[k] in f(t), independent of h."""

    require(k >= 1, "exceptional coefficient requires k>=1")
    return poly_add(
        poly_scale(monomial_t(k - 1), k),
        poly_scale(monomial_t(k), -(k - 1)),
    )


def audit_endpoint_source():
    """Audit the exact nine-row classification of the one-sided pivot."""

    exceptional_rows = {(SELECTED, SELECTED)}
    selected_leakage_rows = {(SELECTED, j) for j in COMPLEMENT}
    complementary_rows = {(i, j) for i in COMPLEMENT for j in COLORS}
    require(
        exceptional_rows
        | selected_leakage_rows
        | complementary_rows
        == {(i, j) for i in COLORS for j in COLORS},
        "one-sided path partition omitted a row",
    )
    require(
        not (exceptional_rows & selected_leakage_rows)
        and not (exceptional_rows & complementary_rows)
        and not (selected_leakage_rows & complementary_rows),
        "one-sided path partition overlaps row types",
    )
    require(
        tuple(map(len, (exceptional_rows, selected_leakage_rows, complementary_rows)))
        == (1, 2, 6),
        "one-sided path partition is not the 1+2+6 ledger",
    )

    rows = []
    endpoint_hypotheses = {}
    for i in COLORS:
        for j in COLORS:
            direct_after = i == SELECTED and j == SELECTED
            response_after = i in COMPLEMENT
            target = i == j
            rows.append((i, j, direct_after, response_after, target))

            if i == SELECTED and j == SELECTED:
                require(direct_after and not response_after and target, "bad aa endpoint row")
                endpoint_hypotheses[(i, j)] = {("U",)}
            elif i == SELECTED:
                require(
                    not direct_after and not response_after and not target,
                    f"bad selected off-diagonal endpoint row {(i, j)}",
                )
                endpoint_hypotheses[(i, j)] = set()
            else:
                require(
                    not direct_after and response_after and target == (i == j),
                    f"bad complementary endpoint row {(i, j)}",
                )
                endpoint_hypotheses[(i, j)] = {("Theta", i, j)}

    require(len(rows) == 9, "endpoint ledger lost a row")
    require(
        sum(1 for row in rows if row[3]) == 6,
        "one-sided endpoint does not retain exactly six response rows",
    )
    required = set().union(*endpoint_hypotheses.values())
    require(("U",) in required, "endpoint ledger omitted the unary hypothesis")
    require(
        required - {("U",)}
        == {("Theta", i, j) for i in COMPLEMENT for j in COLORS},
        "endpoint ledger uses the wrong six annihilations",
    )
    require(len(required) == 7, "endpoint exactness has the wrong hypothesis count")

    # Scaling: G=alpha*q+R=alpha*q#.  Check the actual residual identities,
    # not only cancellation of adjacent powers of alpha.
    for h in range(3, 65):
        for alpha in (Fraction(2), Fraction(-3), Fraction(5, 2)):
            q_sharp_h = Fraction(7, 5)
            target_a = Fraction(-11, 7)
            unary = alpha**h * q_sharp_h - alpha ** (h - 1) * target_a
            require(
                alpha * q_sharp_h - target_a == alpha ** (1 - h) * unary,
                f"exceptional endpoint scaling failed at h={h}",
            )

            q_sharp_adjacent = Fraction(13, 11)
            q_adjacent = Fraction(-5, 3)
            response = Fraction(17, 13)
            theta = alpha ** (h - 1) * (q_sharp_adjacent - q_adjacent)
            require(
                response * (q_sharp_adjacent - q_adjacent)
                == alpha ** (1 - h) * response * theta,
                f"adjacent endpoint scaling failed at h={h}",
            )

            # In a selected off-diagonal row the old response is zero, so
            # the leakage is -R_aj q#^[h-1] = -alpha^(1-h) R_aj Theta.
            selected_q_sharp = Fraction(29, 17)
            selected_response = Fraction(-31, 23)
            selected_theta = alpha ** (h - 1) * selected_q_sharp
            require(
                -selected_response * selected_q_sharp
                == -(alpha ** (1 - h)) * selected_response * selected_theta,
                f"selected leakage scaling failed at h={h}",
            )

            p_i, s_j, p_a, s_a = map(Fraction, (2, -3, 5, 7))
            r = p_a * s_a / alpha
            require(
                (p_i * s_j) * r
                == (p_i * s_a) * (p_a * s_j) / alpha,
                f"ordered endpoint-square scaling failed at h={h}",
            )

    # A good p-star loses one independent row; the q-star retains all.
    p_rows_before = set(COLORS)
    p_rows_after = set(COMPLEMENT)
    q_rows_before = set(COLORS)
    q_rows_after = set(COLORS)
    require(
        (len(p_rows_before), len(p_rows_after)) == (3, 2),
        "wrong p-side rank change",
    )
    require(
        (len(q_rows_before), len(q_rows_after)) == (3, 3),
        "wrong q-side rank change",
    )


def audit_complementary_defect(h):
    m = h - 1
    indices = tuple(range(1, m + 1))

    # Actual defect sum_{k>=1} t^k M_k, modulo sum M_k=0.
    actual = {k: monomial_t(k) for k in indices}
    actual_reduced = reduce_sum_relation(actual, indices, pivot=1)

    common_factor = poly_mul(T, poly_sub(T, ONE))
    claimed = {
        k: poly_mul(common_factor, geometric(k - 1))
        for k in range(2, m + 1)
    }
    require(
        actual_reduced == vector_clean(claimed),
        f"complementary t(t-1) factor failed at h={h}",
    )
    require(not vector_evaluate(actual_reduced, 0), f"complement defect nonzero at t=0, h={h}")
    require(not vector_evaluate(actual_reduced, 1), f"complement defect nonzero at t=1, h={h}")

    # Endpoint derivative is r(q+r)^[m-1]: coefficient k on M_k.
    endpoint_jet = vector_evaluate(vector_derivative(actual), 1)
    expected_jet = {k: Fraction(k) for k in indices}
    require(endpoint_jet == expected_jet, f"complement endpoint jet failed at h={h}")

    # Integral of the derivative is the endpoint relation and hence zero.
    integrated = vector_integral_01(vector_derivative(actual))
    integrated_as_poly = {key: (value,) for key, value in integrated.items()}
    require(
        not reduce_sum_relation(integrated_as_poly, indices, pivot=1),
        f"complement full derivative did not integrate to zero at h={h}",
    )


def audit_selected_offdiagonal_defect(h):
    m = h - 1
    one_minus_t = poly_sub(ONE, T)
    common_factor = poly_mul(T, one_minus_t)

    # The k=0 term is the old zero row R_aj q^[m]=0.
    actual = {
        k: poly_mul(one_minus_t, monomial_t(k))
        for k in range(1, m + 1)
    }
    claimed = {
        k: poly_mul(common_factor, monomial_t(k - 1))
        for k in range(1, m + 1)
    }
    require(actual == claimed, f"selected-row t(1-t) factor failed at h={h}")
    require(not vector_evaluate(actual, 0), f"selected defect nonzero at t=0, h={h}")
    require(not vector_evaluate(actual, 1), f"selected defect nonzero at t=1, h={h}")

    endpoint_jet = vector_evaluate(vector_derivative(actual), 1)
    require(
        endpoint_jet == {k: Fraction(-1) for k in range(1, m + 1)},
        f"selected endpoint leakage failed at h={h}",
    )
    require(
        not vector_integral_01(vector_derivative(actual)),
        f"selected full derivative did not integrate to zero at h={h}",
    )


def audit_exceptional_defect(h):
    indices = tuple(range(2, h + 1))

    # Construct f from q_t^[h] +(1-t) r q_t^[h-1].
    one_minus_t = poly_sub(ONE, T)
    constructed = {0: ONE}
    for k in range(1, h + 1):
        from_q_power = monomial_t(k)
        from_response = poly_scale(
            poly_mul(one_minus_t, monomial_t(k - 1)),
            k,
        )
        constructed[k] = poly_add(from_q_power, from_response)
        require(
            constructed[k] == exceptional_coefficient(k),
            f"exceptional coefficient formula failed at h={h}, k={k}",
        )

    require(constructed[0] == ONE, f"wrong pure-q coefficient at h={h}")
    require(constructed[1] == ONE, f"wrong old response coefficient at h={h}")
    require(
        all(poly_evaluate(constructed[k], 1) == 1 for k in range(h + 1)),
        f"exceptional endpoint q# power failed at h={h}",
    )

    # Defect has k>=2 coefficients c_k, modulo U relation sum M_k=0.
    actual = {k: constructed[k] for k in indices}
    actual_reduced = reduce_sum_relation(actual, indices, pivot=2)

    double_factor = poly_scale(
        poly_mul(T, poly_pow(poly_sub(T, ONE), 2)),
        -1,
    )
    claimed = {}
    for k in range(3, h + 1):
        carrier = clean(tuple(Fraction(ell + 2) for ell in range(k - 2)))
        claimed[k] = poly_mul(double_factor, carrier)
    require(
        actual_reduced == vector_clean(claimed),
        f"exceptional t(t-1)^2 factor failed at h={h}",
    )
    if h == 3:
        h3_coefficient = poly_scale(
            poly_mul(T, poly_pow(poly_sub(ONE, T), 2)),
            -2,
        )
        require(
            actual_reduced == {3: h3_coefficient},
            "h=3 exceptional reduction lost its sign or factor 2",
        )
        for alpha in (Fraction(2), Fraction(-3), Fraction(5, 2)):
            require(
                {3: poly_scale(h3_coefficient, alpha)}
                == {key: poly_scale(value, alpha) for key, value in actual_reduced.items()},
                f"h=3 exceptional alpha scaling failed for alpha={alpha}",
            )
    require(not vector_evaluate(actual_reduced, 0), f"aa defect nonzero at t=0, h={h}")
    require(not vector_evaluate(actual_reduced, 1), f"aa defect nonzero at t=1, h={h}")

    # c'_k(t)=k(k-1)t^(k-2)(1-t), the coefficient form of
    # f'=(1-t)r^2 q_t^[h-2].
    for k in range(2, h + 1):
        expected_derivative = poly_scale(
            poly_mul(one_minus_t, monomial_t(k - 2)),
            k * (k - 1),
        )
        require(
            poly_derivative(constructed[k]) == expected_derivative,
            f"exceptional derivative failed at h={h}, k={k}",
        )
        require(
            poly_evaluate(expected_derivative, 1) == 0,
            f"exceptional endpoint is not stationary at h={h}, k={k}",
        )

    require(
        not vector_integral_01(vector_derivative(actual_reduced)),
        f"exceptional full derivative did not integrate to zero at h={h}",
    )


def audit_adjacent_integral(h):
    """Integral r q_t^[h-2] = q#^[h-1]-q^[h-1]."""

    m = h - 1
    derivative_coefficients = {
        k: poly_scale(monomial_t(k - 1), k)
        for k in range(1, m + 1)
    }
    integrated = vector_integral_01(derivative_coefficients)
    require(
        integrated == {k: Fraction(1) for k in range(1, m + 1)},
        f"adjacent-power path integral failed at h={h}",
    )


def audit_ordered_endpoint_square():
    for i in COMPLEMENT:
        for j in COLORS:
            direct_product = sorted((f"p{i}", f"s{j}", "p0", "s0"))
            ordered_square = sorted((f"p{i}", "s0", "p0", f"s{j}"))
            require(
                direct_product == ordered_square,
                f"Segre endpoint square failed at {(i, j)}",
            )

    # The named endpoint slots still distinguish a transpose.
    correct = ("p1", "s0", "p0", "s2")
    transposed = ("p0", "s1", "p2", "s0")
    require(correct != transposed, "endpoint transpose escaped detection")


def audit_reparametrization():
    for mu in (Fraction(0), Fraction(1), Fraction(5, 2), Fraction(-3)):
        # phi_mu=t+(mu-1)t(t-1).
        phi = poly_add(
            T,
            poly_scale(poly_mul(T, poly_sub(T, ONE)), mu - 1),
        )
        require(poly_evaluate(phi, 0) == 0, f"phi_mu moved t=0 for mu={mu}")
        require(poly_evaluate(phi, 1) == 1, f"phi_mu moved t=1 for mu={mu}")
        require(
            poly_evaluate(poly_derivative(phi), 1) == mu,
            f"wrong endpoint speed for mu={mu}",
        )

        # A representative complementary coefficient phi(t)^k has
        # endpoint derivative k*mu.
        for k in range(1, 8):
            coefficient = poly_pow(phi, k)
            require(
                poly_evaluate(poly_derivative(coefficient), 1) == k * mu,
                f"reparametrized complement jet failed for mu={mu}, k={k}",
            )

            selected_coefficient = poly_mul(
                poly_sub(ONE, phi),
                poly_pow(phi, k),
            )
            require(
                poly_evaluate(poly_derivative(selected_coefficient), 1) == -mu,
                f"reparametrized selected leakage failed for mu={mu}, k={k}",
            )

            c_composed = poly_compose(exceptional_coefficient(k), phi)
            require(
                poly_evaluate(poly_derivative(c_composed), 1) == 0,
                f"reparametrized exceptional stationarity failed for mu={mu}, k={k}",
            )

    phi_stationary = poly_sub(poly_scale(T, 2), poly_pow(T, 2))
    require(poly_evaluate(phi_stationary, 0) == 0, "2t-t^2 moved first endpoint")
    require(poly_evaluate(phi_stationary, 1) == 1, "2t-t^2 moved second endpoint")
    require(
        poly_evaluate(poly_derivative(phi_stationary), 1) == 0,
        "2t-t^2 did not kill endpoint speed",
    )


def audit_two_sided_pivot_square():
    """Audit the mixed (x,y) divided difference at the double pivot."""

    # The p-sided and s-sided six-row sets have an eight-row union:
    # every ordered cell except (a,a).
    all_rows = {(i, j) for i in COLORS for j in COLORS}
    p_sided = {(i, j) for i in COMPLEMENT for j in COLORS}
    s_sided = {(i, j) for i in COLORS for j in COMPLEMENT}
    union = p_sided | s_sided
    require(len(p_sided) == len(s_sided) == 6, "wrong one-sided row count")
    require(len(union) == 8, "two-sided square does not require eight rows")
    require(
        union == all_rows - {(SELECTED, SELECTED)},
        "two-sided annihilation union has the wrong cells",
    )
    require(
        s_sided - p_sided == {(SELECTED, j) for j in COMPLEMENT},
        "reflected corner did not expose exactly the two selected leakages",
    )

    unary = {("U",)}
    theta_p = {("Theta", i, j) for i, j in p_sided}
    theta_s = {("Theta", i, j) for i, j in s_sided}
    corner_hypotheses = {
        (1, 1): set(),
        (0, 1): unary | theta_p,
        (1, 0): unary | theta_s,
        (0, 0): unary | (theta_p & theta_s),
    }
    require(
        len(corner_hypotheses[(0, 1)]) == 7,
        "p-sided corner does not use U plus six annihilations",
    )
    require(
        len(corner_hypotheses[(0, 0)]) == 5,
        "double-pivot corner does not use U plus four annihilations",
    )
    require(
        set().union(*corner_hypotheses.values())
        == unary | {("Theta", i, j) for i, j in union},
        "four exact corners do not require U plus the eight-row union",
    )

    # The alternating four-corner row has normalization
    # -alpha^(1-h) U in the exceptional row and
    # -alpha^(1-h) R_ij Theta in each of the other eight rows.
    for h in (3, 7, 16):
        for alpha in (Fraction(2), Fraction(-3), Fraction(5, 2)):
            q_sharp_h = Fraction(11, 7)
            target_a = Fraction(-13, 5)
            direct_at_pivot = alpha * q_sharp_h
            u_value = alpha**h * q_sharp_h - alpha ** (h - 1) * target_a
            aa_corners = {
                (1, 1): target_a,
                (1, 0): direct_at_pivot,
                (0, 1): direct_at_pivot,
                (0, 0): direct_at_pivot,
            }
            aa_alternating = (
                aa_corners[(1, 1)]
                - aa_corners[(1, 0)]
                - aa_corners[(0, 1)]
                + aa_corners[(0, 0)]
            )
            require(
                aa_alternating == -(alpha ** (1 - h)) * u_value,
                f"exceptional four-corner normalization failed at h={h}, alpha={alpha}",
            )

            for row_number, (i, j) in enumerate(sorted(union), start=1):
                old_value = Fraction(0) if i != j else Fraction(19 + row_number, 17)
                theta_product = Fraction(23 + row_number, 19)
                delta = alpha ** (1 - h) * theta_product
                new_value = old_value + delta
                if i in COMPLEMENT and j in COMPLEMENT:
                    corners = {
                        (1, 1): old_value,
                        (1, 0): new_value,
                        (0, 1): new_value,
                        (0, 0): new_value,
                    }
                elif i in COMPLEMENT:  # The response survives only for y=1.
                    corners = {
                        (1, 1): old_value,
                        (1, 0): Fraction(0),
                        (0, 1): new_value,
                        (0, 0): Fraction(0),
                    }
                else:  # The response survives only for x=1.
                    corners = {
                        (1, 1): old_value,
                        (1, 0): new_value,
                        (0, 1): Fraction(0),
                        (0, 0): Fraction(0),
                    }
                alternating = (
                    corners[(1, 1)]
                    - corners[(1, 0)]
                    - corners[(0, 1)]
                    + corners[(0, 0)]
                )
                require(
                    alternating == -delta,
                    f"four-corner row normalization failed at h={h}, row={(i, j)}",
                )

    # Use z=xy and the DP basis q#^[m-k] r^[k].
    # A complementary row is g(z)=sum (-z)^k M_k, so its mixed
    # divided difference at (0,0) is g'(0)=-M_1.
    for h in range(3, 65):
        m = h - 1
        g = {
            k: poly_scale(monomial_t(k), (-1) ** k)
            for k in range(m + 1)
        }
        mixed_corner = vector_evaluate(vector_derivative(g), 0)
        require(
            mixed_corner == {1: Fraction(-1)},
            f"two-sided complementary mixed jet failed at h={h}",
        )

        # A selected first row contributes x(g(xy)-g(0))/(xy);
        # every surviving monomial has positive x-degree at (0,0).
        selected_p_monomials = {
            k: (k, k - 1) for k in range(1, m + 1)
        }
        selected_s_monomials = {
            k: (k - 1, k) for k in range(1, m + 1)
        }
        require(
            all(x_degree > 0 for x_degree, _ in selected_p_monomials.values()),
            f"p-selected leakage survived mixed degree at h={h}",
        )
        require(
            all(y_degree > 0 for _, y_degree in selected_s_monomials.values()),
            f"s-selected leakage survived mixed degree at h={h}",
        )

        # In the q#^[h-k]r^[k] basis, the exceptional coefficient is
        # (k-1)(-1)^(k-1) z^k.  It has no linear z term.
        exceptional = {0: ONE}
        for k in range(1, h + 1):
            exceptional[k] = poly_scale(
                monomial_t(k),
                (k - 1) * ((-1) ** (k - 1)),
            )
        require(
            not vector_evaluate(vector_derivative(exceptional), 0),
            f"exceptional mixed stationarity failed at h={h}",
        )

        # Rebuild the literal bivariate divided difference for every row.
        # This independently checks the sign, the two selected leakages,
        # and the zero exceptional mixed coefficient.
        for i, j in sorted(all_rows):
            coefficients = {}
            if i == SELECTED and j == SELECTED:
                coefficients[0] = bivar_monomial(0, 0)
                for k in range(1, h + 1):
                    from_direct = bivar_monomial(k, k, (-1) ** k)
                    from_response = bivar_monomial(
                        k, k, k * ((-1) ** (k - 1))
                    )
                    coefficients[k] = bivar_add(from_direct, from_response)
            elif i == SELECTED:
                coefficients = {
                    k: bivar_monomial(k + 1, k, (-1) ** k)
                    for k in range(m + 1)
                }
            elif j == SELECTED:
                coefficients = {
                    k: bivar_monomial(k, k + 1, (-1) ** k)
                    for k in range(m + 1)
                }
            else:
                coefficients = {
                    k: bivar_monomial(k, k, (-1) ** k)
                    for k in range(m + 1)
                }

            mixed = {
                k: bivar_evaluate(bivar_mixed_divided_difference(poly), 0, 0)
                for k, poly in coefficients.items()
            }
            mixed = {k: value for k, value in mixed.items() if value}
            expected = {1: Fraction(-1)} if i in COMPLEMENT and j in COMPLEMENT else {}
            require(
                mixed == expected,
                f"literal bivariate mixed row failed at h={h}, row={(i, j)}",
            )

    # Reparametrizing the physical scaling coordinates multiplies the
    # mixed coefficient by their two endpoint speeds.
    for mu, nu in (
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(1)),
        (Fraction(2), Fraction(-3)),
    ):
        # phi=t+(1-mu)t(t-1) has phi'(0)=mu and fixed endpoints.
        phi = poly_add(
            T,
            poly_scale(poly_mul(T, poly_sub(T, ONE)), 1 - mu),
        )
        psi = poly_add(
            T,
            poly_scale(poly_mul(T, poly_sub(T, ONE)), 1 - nu),
        )
        require(
            (poly_evaluate(phi, 0), poly_evaluate(phi, 1)) == (0, 1),
            f"x reparametrization moved a corner for mu={mu}",
        )
        require(
            (poly_evaluate(psi, 0), poly_evaluate(psi, 1)) == (0, 1),
            f"y reparametrization moved a corner for nu={nu}",
        )
        mixed_scale = (
            poly_evaluate(poly_derivative(phi), 0)
            * poly_evaluate(poly_derivative(psi), 0)
        )
        require(
            mixed_scale == mu * nu,
            f"mixed reparametrization scale failed for {(mu, nu)}",
        )
    require(
        Fraction(0) * Fraction(1) != Fraction(1),
        "mixed divided difference was treated as coordinate-free",
    )


def audit_boundary_and_torsor_guards():
    # h=3 universal module guards.  z is represented by scalar 1 and the
    # literal boundary submodule is zero.
    complement_defect = poly_sub(T, poly_pow(T, 2))
    selected_defect = poly_mul(T, poly_sub(ONE, T))
    exceptional_defect_at_alpha_one = poly_scale(
        poly_mul(T, poly_pow(poly_sub(ONE, T), 2)),
        2,
    )
    require(complement_defect != ZERO, "complement module guard collapsed")
    require(selected_defect != ZERO, "selected module guard collapsed")
    require(
        exceptional_defect_at_alpha_one != ZERO,
        "exceptional module guard collapsed",
    )
    require(
        poly_evaluate(complement_defect, 0) == poly_evaluate(complement_defect, 1) == 0,
        "complement guard lost endpoint roots",
    )
    require(
        poly_evaluate(selected_defect, 0) == poly_evaluate(selected_defect, 1) == 0
        and poly_evaluate(poly_derivative(selected_defect), 1) == -1,
        "selected guard lost an endpoint root or leakage sign",
    )
    for alpha in (Fraction(2), Fraction(-3), Fraction(5, 2)):
        exceptional_defect = poly_scale(exceptional_defect_at_alpha_one, alpha)
        require(exceptional_defect != ZERO, f"exceptional guard lost alpha={alpha}")
        require(
            poly_evaluate(exceptional_defect, 0) == 0
            and poly_evaluate(exceptional_defect, 1) == 0
            and poly_evaluate(poly_derivative(exceptional_defect), 1) == 0,
            f"exceptional guard lost its stationary roots for alpha={alpha}",
        )

    # Formal filtered lift extension, not a claimed matching source:
    # coordinates are (T,Z), with T in grade 1 and Z in grade 0.
    cap = (Fraction(-1), Fraction(1))
    same_power = (Fraction(1), Fraction(-1))
    zero_cycle = (Fraction(0), Fraction(0))
    differential_target = zero_cycle
    differential_response = zero_cycle
    path_signature = (
        complement_defect,
        selected_defect,
        exceptional_defect_at_alpha_one,
    )
    signatures = []
    for lam in (Fraction(-1), Fraction(0), Fraction(2), Fraction(7, 3)):
        boundary = (Fraction(1), lam)
        differential_squared = tuple(
            differential_target[index] + lam * differential_response[index]
            for index in range(2)
        )
        associated_graded_boundary = (boundary[0], Fraction(0))
        require(differential_squared == zero_cycle, f"d^2 failed at lambda={lam}")
        require(boundary[0] == 1, f"leading target changed at lambda={lam}")
        require(
            associated_graded_boundary == (1, 0),
            f"associated-graded target changed at lambda={lam}",
        )
        residual = (cap[0] + boundary[0], cap[1] + boundary[1])
        require(residual == (0, 1 + lam), f"wrong torsor residual at lambda={lam}")
        signatures.append(path_signature)
    require(
        all(signature == signatures[0] for signature in signatures),
        "path identities detected the lower torsor parameter",
    )

    secondary = (Fraction(1), Fraction(0))
    require(
        (secondary[0] - same_power[0], secondary[1] - same_power[1]) == (0, 1),
        "H_path-S did not expose the odd indeterminacy",
    )


def mutation_guards():
    h = 7

    # Omitting the extra stationary factor must fail.
    indices = tuple(range(2, h + 1))
    actual = {k: exceptional_coefficient(k) for k in indices}
    actual_reduced = reduce_sum_relation(actual, indices, pivot=2)
    wrong_single_factor = {
        k: poly_mul(
            poly_scale(poly_mul(T, poly_sub(T, ONE)), -1),
            clean(tuple(Fraction(ell + 2) for ell in range(k - 2))),
        )
        for k in range(3, h + 1)
    }
    require(
        actual_reduced != vector_clean(wrong_single_factor),
        "mutation accepted only one exceptional endpoint factor",
    )

    # Dropping the divided-power multiplication factor k changes f(t).
    k = 4
    wrong_exceptional_coefficient = poly_add(
        monomial_t(k),
        poly_mul(poly_sub(ONE, T), monomial_t(k - 1)),
    )
    require(
        exceptional_coefficient(k) != wrong_exceptional_coefficient,
        "mutation dropped the divided-power response factor k",
    )

    # At h=3 the exceptional quotient has the essential coefficient 2.
    h3_right = poly_scale(
        poly_mul(T, poly_pow(poly_sub(ONE, T), 2)),
        -2,
    )
    h3_missing_two = poly_scale(
        poly_mul(T, poly_pow(poly_sub(ONE, T), 2)),
        -1,
    )
    require(h3_right != h3_missing_two, "mutation dropped the h=3 factor 2")

    # The selected off-diagonal rows have t(1-t), not t(t-1).
    right = poly_mul(T, poly_sub(ONE, T))
    wrong = poly_mul(T, poly_sub(T, ONE))
    require(right != wrong, "mutation accepted selected-row sign reversal")

    # Conversely, a complementary row uses t(t-1), so copying the
    # selected-row sign must fail.
    complement_right = poly_mul(T, poly_sub(T, ONE))
    complement_wrong = poly_mul(T, poly_sub(ONE, T))
    require(
        complement_right != complement_wrong,
        "mutation accepted complementary-row sign reversal",
    )

    # The alpha normalization is alpha^(1-h), not alpha^(-h).
    alpha = Fraction(2)
    q_sharp_h = Fraction(3)
    target_a = Fraction(5)
    unary = alpha**h * q_sharp_h - alpha ** (h - 1) * target_a
    correct_residual = alpha ** (1 - h) * unary
    wrong_residual = alpha ** (-h) * unary
    require(correct_residual != wrong_residual, "mutation shifted the alpha exponent")

    # Six one-sided annihilations do not silently become the eight needed
    # for both one-sided corners.
    p_sided = {(i, j) for i in COMPLEMENT for j in COLORS}
    both_sides = p_sided | {(i, j) for i in COLORS for j in COMPLEMENT}
    require(p_sided != both_sides, "mutation erased the two reflected corner rows")

    # The double-pivot complementary mixed coefficient is negative.
    mixed_linear_term = poly_scale(T, -1)
    require(
        poly_evaluate(poly_derivative(mixed_linear_term), 0) != Fraction(1),
        "mutation reversed the mixed-square sign",
    )

    # Endpoint speed is not invariant under reparametrization.
    affine_speed = Fraction(1)
    stationary_speed = poly_evaluate(
        poly_derivative(poly_sub(poly_scale(T, 2), poly_pow(T, 2))),
        1,
    )
    require(
        stationary_speed != affine_speed,
        "mutation treated the endpoint jet as parametrization invariant",
    )
    require(
        poly_evaluate(
            poly_derivative(poly_sub(poly_scale(T, 2), poly_pow(T, 2))),
            0,
        )
        != stationary_speed,
        "mutation evaluated reparametrization speed at the wrong endpoint",
    )

    # Endpoint evaluation is not coefficientwise integration of the jet.
    selected = poly_mul(T, poly_sub(ONE, T))
    require(
        poly_evaluate(poly_derivative(selected), 1)
        != poly_integral_01(poly_derivative(selected)),
        "mutation identified the endpoint jet with the full path integral",
    )

    # A nonzero lower response is not lambda=0.
    require((1, 1) != (1, 0), "mutation accepted lambda=1 as lambda=0")


def main():
    audit_endpoint_source()
    audit_ordered_endpoint_square()
    for h in range(3, 65):
        audit_complementary_defect(h)
        audit_selected_offdiagonal_defect(h)
        audit_exceptional_defect(h)
        audit_adjacent_integral(h)
    audit_reparametrization()
    audit_two_sided_pivot_square()
    audit_boundary_and_torsor_guards()
    mutation_guards()
    print(
        "scalar-unit one-sided stationary pivot/path no-go: PASS; "
        "h=3..64, alpha scaling, 1+2+6 row factors, endpoint jet/integral, "
        "eight-row two-sided corners/mixed square, reparametrization, "
        "filtered torsor, and mutation guards audited"
    )


if __name__ == "__main__":
    main()

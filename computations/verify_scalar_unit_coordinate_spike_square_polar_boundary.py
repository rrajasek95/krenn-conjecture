#!/usr/bin/env python3
"""Exact checks for the scalar-unit coordinate-spike square-polar boundary."""

from fractions import Fraction
from itertools import product


ZERO = {}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def add(*polys):
    out = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            out[monomial] = out.get(monomial, Fraction(0)) + coefficient
    return clean(out)


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return clean({monomial: scalar * coefficient for monomial, coefficient in poly.items()})


def multiply(left, right):
    out = {}
    for left_monomial, left_coefficient in left.items():
        left_sites = {site for site, _ in left_monomial}
        for right_monomial, right_coefficient in right.items():
            if left_sites.intersection(site for site, _ in right_monomial):
                continue
            monomial = tuple(sorted(left_monomial + right_monomial))
            out[monomial] = out.get(monomial, Fraction(0)) + left_coefficient * right_coefficient
    return clean(out)


def factorial(value):
    out = 1
    for factor in range(2, value + 1):
        out *= factor
    return out


def ordinary_power(poly, exponent):
    out = {(): Fraction(1)}
    for _ in range(exponent):
        out = multiply(out, poly)
    return out


def divided_power(poly, exponent):
    return scale(ordinary_power(poly, exponent), Fraction(1, factorial(exponent)))


def divided_power_path(q, rho, exponent):
    """Coefficients of (q + t*rho)^[exponent] in ascending t-degree."""
    return [
        multiply(
            divided_power(q, exponent - rho_degree),
            divided_power(rho, rho_degree),
        )
        for rho_degree in range(exponent + 1)
    ]


def t_derivative(coefficients):
    return [
        scale(coefficients[degree], degree)
        for degree in range(1, len(coefficients))
    ]


def t_integral_zero_to_one(coefficients):
    return add(*(
        scale(coefficient, Fraction(1, degree + 1))
        for degree, coefficient in enumerate(coefficients)
    ))


def t_evaluate(coefficients, value):
    value = Fraction(value)
    return add(*(
        scale(coefficient, value ** degree)
        for degree, coefficient in enumerate(coefficients)
    ))


def formal_divided_power_path(exponent):
    """Formal t/q/rho ledger in the divided-power basis."""
    return {
        (rho_degree, exponent - rho_degree, rho_degree): Fraction(1)
        for rho_degree in range(exponent + 1)
    }


def formal_t_derivative(ledger):
    out = {}
    for (t_degree, q_degree, rho_degree), coefficient in ledger.items():
        if not t_degree:
            continue
        key = (t_degree - 1, q_degree, rho_degree)
        out[key] = out.get(key, Fraction(0)) + t_degree * coefficient
    return clean(out)


def formal_rho_multiply(ledger):
    """Multiply a divided-power-basis ledger by the ordinary form rho."""
    out = {}
    for (t_degree, q_degree, rho_degree), coefficient in ledger.items():
        key = (t_degree, q_degree, rho_degree + 1)
        out[key] = (
            out.get(key, Fraction(0))
            + (rho_degree + 1) * coefficient
        )
    return clean(out)


def formal_t_evaluate(ledger, value):
    value = Fraction(value)
    out = {}
    for (t_degree, q_degree, rho_degree), coefficient in ledger.items():
        key = (q_degree, rho_degree)
        out[key] = (
            out.get(key, Fraction(0))
            + value ** t_degree * coefficient
        )
    return clean(out)


def formal_t_integral_zero_to_one(ledger):
    out = {}
    for (t_degree, q_degree, rho_degree), coefficient in ledger.items():
        key = (0, q_degree, rho_degree)
        out[key] = (
            out.get(key, Fraction(0))
            + coefficient / (t_degree + 1)
        )
    return clean(out)


def formal_basis_difference(left, right):
    out = dict(left)
    for key, coefficient in right.items():
        out[key] = out.get(key, Fraction(0)) - coefficient
    return clean(out)


def substitute_divided_basis(ledger, q, rho):
    out = ZERO
    for (q_degree, rho_degree), coefficient in ledger.items():
        term = multiply(
            divided_power(q, q_degree),
            divided_power(rho, rho_degree),
        )
        out = add(out, scale(term, coefficient))
    return out


def x(site, colour):
    return {((site, colour),): Fraction(1)}


def word(colours):
    out = {(): Fraction(1)}
    for site, colour in enumerate(colours):
        out = multiply(out, x(site, colour))
    return out


def expected_core_q():
    """Independent exact coefficient fingerprint for the displayed q."""
    a, b = 0, 1
    return {
        tuple(sorted(((0, a), (3, b)))): Fraction(1),
        tuple(sorted(((1, b), (5, a)))): Fraction(1),
        tuple(sorted(((2, a), (4, a)))): Fraction(1),
        tuple(sorted(((3, b), (4, a)))): Fraction(1),
        tuple(sorted(((3, a), (5, a)))): Fraction(1),
    }


def form_vector(poly, site_count=6, colour_count=3):
    return [
        poly.get(((site, colour),), Fraction(0))
        for site in range(site_count)
        for colour in range(colour_count)
    ]


def vector_rank(vectors):
    matrix = [[Fraction(entry) for entry in row] for row in vectors]
    rank = 0
    width = len(matrix[0]) if matrix else 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [entry / pivot_value for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                matrix[row][index] - factor * matrix[rank][index]
                for index in range(width)
            ]
        rank += 1
    return rank


def build_core():
    a, b, c = 0, 1, 2
    q = add(
        multiply(x(0, a), x(3, b)),
        multiply(x(1, b), x(5, a)),
        multiply(x(2, a), x(4, a)),
        multiply(x(3, b), x(4, a)),
        multiply(x(3, a), x(5, a)),
    )
    p_a = x(0, a)
    s_a = add(x(1, a), scale(x(2, a), -1))
    r = multiply(p_a, s_a)
    q2 = divided_power(q, 2)
    top = divided_power(q, 3)
    carrier = add(q, scale(r, Fraction(1, 2)))
    theta = multiply(r, carrier)
    unary = add(q, r)
    targets = {
        a: word((a,) * 6),
        b: word((b,) * 6),
        c: word((c,) * 6),
    }
    radial_word = word((a, b, a, b, a, a))
    return a, b, c, q, p_a, s_a, r, q2, top, carrier, theta, unary, targets, radial_word


def response_table(p, s):
    return {
        (row, column): multiply(p[row], s[column])
        for row in p
        for column in s
    }


def physical_rows(responses, q2, top, targets, a, b, c):
    rows = {}
    for row in (a, b, c):
        for column in (a, b, c):
            lhs = multiply(responses[(row, column)], q2)
            if (row, column) == (a, a):
                lhs = add(top, lhs)
            rows[(row, column)] = lhs
    return rows


def proportional_to(poly, target):
    if not target:
        return Fraction(0) if not poly else None
    first_monomial = next(iter(target))
    scalar = poly.get(first_monomial, Fraction(0)) / target[first_monomial]
    return scalar if poly == scale(target, scalar) else None


def check_common_core():
    a, b, c, q, p_a, s_a, r, q2, top, carrier, theta, unary, targets, radial_word = build_core()
    require(q == expected_core_q(), "common core q/support changed")
    require(top == radial_word, "common core lost its off-target top word")
    require(top not in targets.values(), "common core top word became a pure target")
    require(multiply(r, q2) == add(targets[a], scale(radial_word, -1)),
            "exceptional adjacent-power response changed")
    require(divided_power(r, 2) == ZERO, "common radial response should square to zero")
    require(divided_power(unary, 3) == targets[a], "common unary cap is not clean")
    derived_carrier = t_integral_zero_to_one(divided_power_path(q, r, 1))
    require(carrier == derived_carrier, "Hermite carrier is not q + (1/2)r")
    require(
        theta == multiply(r, derived_carrier),
        "cubic carrier normalization changed",
    )
    require(
        theta == add(divided_power(unary, 2), scale(q2, -1)),
        "carrier identity rH=(q+r)^[2]-q^[2] changed",
    )
    return "common_core"


def check_off_diagonal_guard():
    a, b, c, q, p_a, s_a, r, q2, top, carrier, theta, unary, targets, radial_word = build_core()
    p = {a: p_a, b: x(3, b), c: x(0, b)}
    s = {a: s_a, b: x(0, a), c: x(4, a)}
    require(vector_rank([form_vector(p[label]) for label in (a, b, c)]) == 3,
            "off-diagonal guard p-star is not good")
    require(vector_rank([form_vector(s[label]) for label in (a, b, c)]) == 3,
            "off-diagonal guard s-star is not good")
    responses = response_table(p, s)
    rows = physical_rows(responses, q2, top, targets, a, b, c)
    exact = {
        index
        for index, lhs in rows.items()
        if lhs == (targets[index[0]] if index[0] == index[1] else ZERO)
    }
    expected_exact = {(a, a), (a, b), (a, c), (b, a), (b, c), (c, b)}
    require(exact == expected_exact, "off-diagonal guard is no longer exactly six-of-nine")

    mixed_u = word((b, a, a, a, a, a))
    mixed_v = word((b, b, a, b, a, a))
    require(rows[(b, b)] == radial_word, "off-diagonal bb replacement changed")
    require(rows[(c, c)] == ZERO, "off-diagonal cc replacement changed")
    require(rows[(c, a)] == add(mixed_u, scale(mixed_v, -1)),
            "off-diagonal unselected primitive residual changed")

    lambdas = {
        index: proportional_to(multiply(responses[index], theta), radial_word)
        for index in ((b, b), (b, c), (c, b), (c, c))
    }
    require(lambdas == {(b, b): 0, (b, c): -1, (c, b): 0, (c, c): 0},
            "off-diagonal radial packet is not the claimed coordinate spike")
    require(multiply(responses[(b, a)], q2) == ZERO,
            "off-diagonal selected left primitive row changed")
    require(multiply(responses[(a, c)], q2) == ZERO,
            "off-diagonal selected right primitive row changed")
    require(multiply(multiply(responses[(b, a)], responses[(a, c)]), carrier)
            == scale(radial_word, -1),
            "off-diagonal selected primitive square changed")
    inverse = add(q2, scale(multiply(responses[(b, c)], carrier), -1))
    require(multiply(r, inverse) == targets[a], "off-diagonal pure inverse changed")

    response = add(responses[(b, b)], responses[(c, c)])
    require(multiply(response, theta) == ZERO, "active rank-two response left the radial kernel")
    require(multiply(response, q2) == radial_word, "active response old-power value changed")
    require(divided_power(response, 2) == ZERO, "active response lost square-zero descent boundary")
    require(
        multiply(responses[(b, b)], responses[(c, c)])
        == multiply(responses[(b, c)], responses[(c, b)]),
        "literal complementary Plucker rectangle failed",
    )
    actual_error_coefficient = add(radial_word, scale(targets[b], -1), scale(targets[c], -1))
    for z_value in (Fraction(1), Fraction(-2), Fraction(3, 2)):
        actual_error = add(
            divided_power(add(unary, scale(response, z_value)), 3),
            scale(targets[a], -1),
            scale(targets[b], -z_value),
            scale(targets[c], -z_value),
        )
        require(actual_error == scale(actual_error_coefficient, z_value),
                "off-diagonal cap error is not the claimed linear diagonal-row defect")
    return "off_diagonal_guard"


def check_diagonal_guard():
    a, b, c, q, p_a, s_a, r, q2, top, carrier, theta, unary, targets, radial_word = build_core()
    p = {a: p_a, b: x(0, b), c: x(3, b)}
    s = {a: s_a, b: x(0, a), c: x(4, a)}
    require(vector_rank([form_vector(p[label]) for label in (a, b, c)]) == 3,
            "diagonal guard p-star is not good")
    require(vector_rank([form_vector(s[label]) for label in (a, b, c)]) == 3,
            "diagonal guard s-star is not good")
    responses = response_table(p, s)
    rows = physical_rows(responses, q2, top, targets, a, b, c)
    exact = {
        index
        for index, lhs in rows.items()
        if lhs == (targets[index[0]] if index[0] == index[1] else ZERO)
    }
    expected_exact = {(a, a), (a, b), (a, c), (b, c), (c, a)}
    require(exact == expected_exact, "diagonal guard is no longer exactly five-of-nine")
    mixed_u = word((b, a, a, a, a, a))
    mixed_v = word((b, b, a, b, a, a))
    require(rows[(b, a)] == add(mixed_u, scale(mixed_v, -1)),
            "diagonal unselected primitive residual changed")
    require(rows[(c, b)] == radial_word, "diagonal unselected cross residual changed")
    require(rows[(b, b)] == ZERO and rows[(c, c)] == ZERO,
            "diagonal guard unexpectedly acquired a complementary target")

    lambdas = {
        index: proportional_to(multiply(responses[index], theta), radial_word)
        for index in ((b, b), (b, c), (c, b), (c, c))
    }
    require(lambdas == {(b, b): 0, (b, c): 0, (c, b): 0, (c, c): -1},
            "diagonal radial packet is not the claimed coordinate spike")
    require(multiply(responses[(c, a)], q2) == ZERO,
            "diagonal selected left primitive row changed")
    require(multiply(responses[(a, c)], q2) == ZERO,
            "diagonal selected right primitive row changed")
    require(multiply(multiply(responses[(c, a)], responses[(a, c)]), carrier)
            == scale(radial_word, -1),
            "diagonal selected primitive square changed")
    inverse = add(q2, scale(multiply(responses[(c, c)], carrier), -1))
    require(multiply(r, inverse) == targets[a], "diagonal pure inverse changed")
    return "diagonal_guard"


def check_sparse_stratum_exhaustion():
    a, b, c, q, p_a, s_a, r, q2, top, carrier, theta, unary, targets, radial_word = build_core()
    coordinates = [x(site, colour) for site in range(6) for colour in (a, b, c)]
    names = [(site, colour) for site in range(6) for colour in (a, b, c)]
    vectors = [form_vector(form) for form in coordinates]

    p_good = [
        [vector_rank([form_vector(p_a), vectors[left], vectors[right]]) == 3 for right in range(18)]
        for left in range(18)
    ]
    s_good = [
        [vector_rank([form_vector(s_a), vectors[left], vectors[right]]) == 3 for right in range(18)]
        for left in range(18)
    ]
    old = [
        [multiply(multiply(left, right), q2) for right in coordinates]
        for left in coordinates
    ]
    radial = [
        [
            proportional_to(
                multiply(multiply(left, right), theta), radial_word
            )
            for right in coordinates
        ]
        for left in coordinates
    ]
    left_primitive = [multiply(multiply(left, s_a), q2) == ZERO for left in coordinates]
    right_primitive = [multiply(multiply(p_a, right), q2) == ZERO for right in coordinates]

    best = {"diagonal": -1, "off_diagonal": -1}
    witnesses = {}
    for p_b_index, p_c_index, s_b_index, s_c_index in product(range(18), repeat=4):
        if not p_good[p_b_index][p_c_index] or not s_good[s_b_index][s_c_index]:
            continue
        lambdas = (
            radial[p_b_index][s_b_index],
            radial[p_b_index][s_c_index],
            radial[p_c_index][s_b_index],
            radial[p_c_index][s_c_index],
        )
        if any(value is None for value in lambdas) or sum(bool(value) for value in lambdas) != 1:
            continue
        spike_index = next(index for index, value in enumerate(lambdas) if value)
        spike_type = "diagonal" if spike_index in (0, 3) else "off_diagonal"
        exact_count = 1
        exact_count += right_primitive[s_b_index]
        exact_count += right_primitive[s_c_index]
        exact_count += left_primitive[p_b_index]
        exact_count += left_primitive[p_c_index]
        exact_count += old[p_b_index][s_b_index] == targets[b]
        exact_count += old[p_b_index][s_c_index] == ZERO
        exact_count += old[p_c_index][s_b_index] == ZERO
        exact_count += old[p_c_index][s_c_index] == targets[c]
        if exact_count > best[spike_type]:
            best[spike_type] = exact_count
            witnesses[spike_type] = (
                names[p_b_index], names[p_c_index], names[s_b_index], names[s_c_index]
            )

    require(best == {"diagonal": 5, "off_diagonal": 6},
            "sparse coordinate-spike row maxima changed")
    require(witnesses["off_diagonal"] in {
        ((0, b), (3, b), (4, a), (0, a)),
        ((3, b), (0, b), (0, a), (4, a)),
    }, "unexpected off-diagonal sparse maximizer")
    return "sparse_stratum"


def check_hermite_coefficients():
    # Work in the formal divided-power basis
    # q^[q_degree] rho^[rho_degree].  These two sides are constructed by
    # different operations: formal t-differentiation versus multiplication
    # by the ordinary form rho.
    audited_h = []
    for h in range(3, 13):
        audited_h.append(h)
        n = h - 1
        path_n = formal_divided_power_path(n)
        expected_path = {
            (rho_degree, h - 1 - rho_degree, rho_degree): Fraction(1)
            for rho_degree in range(h)
        }
        require(
            n == h - 1 and path_n == expected_path,
            f"Hermite path degree is not h-1 at h={h}",
        )
        derivative = formal_t_derivative(path_n)
        rho_times_lower_path = formal_rho_multiply(
            formal_divided_power_path(n - 1)
        )
        require(
            derivative == rho_times_lower_path,
            f"Hermite derivative identity failed at h={h}",
        )

        endpoint_jump = formal_basis_difference(
            formal_t_evaluate(path_n, 1),
            formal_t_evaluate(path_n, 0),
        )
        carrier = formal_t_integral_zero_to_one(
            formal_divided_power_path(n - 1)
        )
        carrier_jump = formal_t_evaluate(
            formal_rho_multiply(carrier), 1
        )
        require(
            carrier_jump == endpoint_jump,
            f"Hermite endpoint/carrier identity failed at h={h}",
        )

        # Restoring r=alpha*rho multiplies both sides by alpha^n:
        # r*alpha^(h-2)*integral = G^[h-1]-alpha^(h-1)q^[h-1].
        for alpha in (Fraction(1), Fraction(-2), Fraction(3, 2)):
            left_scale = alpha * alpha ** (h - 2)
            right_scale = alpha ** (h - 1)
            left_hand_side = scale(carrier_jump, left_scale)
            g_power = scale(
                formal_t_evaluate(path_n, 1), right_scale
            )
            alpha_q_power = {(h - 1, 0): right_scale}
            right_hand_side = formal_basis_difference(
                g_power, alpha_q_power
            )
            require(
                left_hand_side == right_hand_side,
                f"Hermite alpha normalization failed at h={h}",
            )
    require(
        audited_h == list(range(3, 13)),
        "Hermite audit did not cover every h from 3 through 12",
    )

    # At h=3, the formal integral must specialize to H=q+(1/2)r in
    # the literal six-site guard.
    a, b, c, q, p_a, s_a, r, q2, top, carrier, theta, unary, targets, radial_word = build_core()
    formal_h3 = formal_t_evaluate(
        formal_t_integral_zero_to_one(formal_divided_power_path(1)), 1
    )
    require(
        formal_h3 == {(1, 0): Fraction(1), (0, 1): Fraction(1, 2)},
        "formal h=3 carrier coefficients changed",
    )
    require(
        substitute_divided_basis(formal_h3, q, r) == carrier,
        "formal h=3 carrier does not specialize to the physical H",
    )

    path_two = divided_power_path(q, r, 2)
    require(
        t_evaluate(path_two, 0) == q2
        and t_evaluate(path_two, 1) == divided_power(unary, 2),
        "physical Hermite endpoints changed",
    )
    require(
        t_derivative(path_two)
        == [multiply(r, coefficient)
            for coefficient in divided_power_path(q, r, 1)],
        "physical Hermite derivative identity changed",
    )

    packets = (
        (
            "off-diagonal",
            {a: p_a, b: x(3, b), c: x(0, b)},
            {a: s_a, b: x(0, a), c: x(4, a)},
            {(b, b): 0, (b, c): -1, (c, b): 0, (c, c): 0},
        ),
        (
            "diagonal",
            {a: p_a, b: x(0, b), c: x(3, b)},
            {a: s_a, b: x(0, a), c: x(4, a)},
            {(b, b): 0, (b, c): 0, (c, b): 0, (c, c): -1},
        ),
    )
    for name, p, s, expected_lambdas in packets:
        responses = response_table(p, s)
        for index, expected_lambda in expected_lambdas.items():
            response_path = [
                multiply(responses[index], coefficient)
                for coefficient in path_two
            ]
            endpoint_zero = t_evaluate(response_path, 0)
            endpoint_one = t_evaluate(response_path, 1)
            endpoint_difference = add(
                endpoint_one, scale(endpoint_zero, -1)
            )
            integrated_derivative = t_integral_zero_to_one(
                t_derivative(response_path)
            )
            require(
                endpoint_difference == integrated_derivative,
                f"{name} Hermite endpoint/integral mismatch at {index}",
            )
            require(
                endpoint_difference
                == multiply(responses[index], theta)
                == scale(radial_word, expected_lambda),
                f"{name} Hermite endpoint jump changed at {index}",
            )
    return "hermite_coefficients"


def main():
    completed = {
        check_common_core(),
        check_off_diagonal_guard(),
        check_diagonal_guard(),
        check_sparse_stratum_exhaustion(),
        check_hermite_coefficients(),
    }
    require(
        completed == {
            "common_core",
            "off_diagonal_guard",
            "diagonal_guard",
            "sparse_stratum",
            "hermite_coefficients",
        },
        "checker coverage manifest is incomplete",
    )
    print("scalar-unit coordinate-spike square-polar boundary checks passed")


if __name__ == "__main__":
    main()

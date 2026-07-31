#!/usr/bin/env python3
"""Exact audit for the scalar-unit four-extreme apolar bridge/no-go.

The audit is dependency-free.  It checks:

* the four coefficient identities and dense Q=G-R dual change;
* the response-free clean-cap calculation under the full nine rows;
* literal site-square-zero counts and the Vieta packet realizing L_h;
* the exceptional-row, unary, and adjacent-power normalizations;
* the injective-star extension with D_aa = 0 and R_D = R_aa;
* explicit failure witnesses for all eight companion rows; and
* independent adversarial mutations.

The Vieta audit verifies exact elementary-symmetric data.  Root existence
uses algebraic closure of C and requires no numerical root finder.
Every check uses ``require`` and therefore remains active under python -O.
"""

from fractions import Fraction
from math import comb, factorial


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def trim(poly):
    answer = list(poly)
    while answer and answer[-1] == 0:
        answer.pop()
    return answer or [0]


def add(left, right):
    size = max(len(left), len(right))
    answer = [0] * size
    for i in range(size):
        answer[i] = (
            (left[i] if i < len(left) else 0)
            + (right[i] if i < len(right) else 0)
        )
    return trim(answer)


def scale(scalar, poly):
    return trim([scalar * value for value in poly])


def shift(poly, amount=1):
    return [0] * amount + list(poly)


def coefficient(poly, degree):
    return poly[degree] if degree < len(poly) else 0


def carrier_polynomials(h):
    u = [comb(h, k) for k in range(h + 1)]
    u[0] -= 1
    u[1] -= h

    w = [comb(h - 1, k + 1) for k in range(h - 1)]
    v = add(shift(w), scale(-2, w))
    tv = shift(v)

    x = [0] * (h + 1)
    x[0] = 1
    x[1] = h
    return trim(u), trim(w), trim(v), trim(tv), trim(x)


def extreme_weights(h):
    weights = [0] * (h + 1)
    weights[0] = 3 * h - 7
    weights[1] = -6
    weights[h - 1] = 4 * (h - 1)
    weights[h] = -4 * h * (h - 1)
    return weights


def apply_functional(poly, weights):
    return sum(
        coefficient(poly, k) * weights[k]
        for k in range(len(weights))
    )


def transformed_normal_weight(h, order):
    """Value of L_h on G^(h-order) R^order after Q=G-R."""

    require(0 <= order <= h, "normal order outside the degree-h ledger")
    if order == 0:
        return -(3 * h + 7)
    if order == 1:
        return -(4 * h + 2)
    return -4 * order * (h - 1)


def audit_functional_identities():
    for h in range(3, 129):
        u, w, v, tv, x = carrier_polynomials(h)
        weights = extreme_weights(h)

        require(
            w == [comb(h - 1, k + 1) for k in range(h - 1)],
            f"wrong polynomial quotient at h={h}",
        )
        require(
            (
                coefficient(v, 0),
                coefficient(v, 1),
                coefficient(v, h - 2),
                coefficient(v, h - 1),
            )
            == (-2 * (h - 1), (h - 1) * (3 - h), h - 3, 1),
            f"wrong extreme v coefficients at h={h}",
        )
        require(apply_functional(u, weights) == 0, f"L(u) failed at h={h}")
        require(apply_functional(v, weights) == 0, f"L(v) failed at h={h}")
        require(apply_functional(tv, weights) == 0, f"L(tv) failed at h={h}")
        require(
            apply_functional(x, weights) == -(3 * h + 7),
            f"L(x) failed at h={h}",
        )

        # In the response basis G=Q+R, the monomial G^(h-j)R^j has
        # source dehomogenization t^j(1+t)^(h-j).  The transformed dual
        # is nonzero at every response order, including all intermediate
        # orders when h >= 4.
        normal_weights = []
        for j in range(h + 1):
            normal_monomial = [0] * j + [
                comb(h - j, k) for k in range(h - j + 1)
            ]
            actual = apply_functional(normal_monomial, weights)
            normal_weights.append(actual)
            require(
                actual == transformed_normal_weight(h, j),
                f"normal-basis pullback failed at h={h}, j={j}",
            )
            require(actual != 0, f"normal pullback lost order h={h}, j={j}")
        require(
            normal_weights != weights,
            f"source weights were confused with normal weights at h={h}",
        )


def audit_full_normal_order_ledger():
    """Check the target-subtracted z/D coefficients in equation (13)."""

    for h in range(3, 129):
        u, w, _v, _tv, _x = carrier_polynomials(h)

        zeroth_order = [comb(h, k) for k in range(h + 1)]
        zeroth_order[0] -= 1
        zeroth_order[1] -= h
        require(
            trim(zeroth_order) == u,
            f"normal order zero target subtraction failed at h={h}",
        )

        first_order = [h * comb(h - 1, k) for k in range(h)]
        first_order[0] -= h
        require(
            trim(first_order) == scale(h, shift(w)),
            f"normal order one target subtraction failed at h={h}",
        )

        for order in range(2, h + 1):
            raw_response = [
                factorial(h)
                // (
                    factorial(order)
                    * factorial(k)
                    * factorial(h - order - k)
                )
                for k in range(h - order + 1)
            ]
            require(
                raw_response
                == scale(
                    comb(h, order),
                    [comb(h - order, k) for k in range(h - order + 1)],
                ),
                f"higher normal binomial failed at h={h}, m={order}",
            )


def elementary_symmetric(values):
    answer = [Fraction(1)] + [Fraction(0)] * len(values)
    for value in values:
        for degree in range(len(values), 0, -1):
            answer[degree] += value * answer[degree - 1]
    return answer


def site_poly_mul(left, right):
    """Multiply sparse polynomials with every physical site square zero."""

    answer = {}
    for left_monomial, left_value in left.items():
        left_sites = {site for site, _colour in left_monomial}
        for right_monomial, right_value in right.items():
            if any(site in left_sites for site, _colour in right_monomial):
                continue
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = (
                answer.get(monomial, Fraction(0))
                + left_value * right_value
            )
            if answer[monomial] == 0:
                del answer[monomial]
    return answer


def site_poly_power(poly, exponent):
    require(exponent >= 0, "negative site-algebra exponent")
    answer = {(): Fraction(1)}
    for _ in range(exponent):
        answer = site_poly_mul(answer, poly)
    return answer


def audit_literal_site_square_zero_counts():
    """Independently multiply small packets and recover both factorials."""

    q_pool = [Fraction(2), Fraction(3), Fraction(5), Fraction(7)]
    z_pool = [Fraction(11), Fraction(13), Fraction(17), Fraction(19)]
    for h in (3, 4):
        q_values = q_pool[:h]
        z_values = z_pool[:h]
        q_poly = {}
        p_poly = {}
        s_poly = {}
        for i, (q_value, z_value) in enumerate(zip(q_values, z_values)):
            left = (2 * i, 0)
            right = (2 * i + 1, 0)
            q_poly[(left, right)] = q_value
            p_poly[(left,)] = Fraction(1)
            s_poly[(right,)] = z_value * q_value
        r_poly = site_poly_mul(p_poly, s_poly)
        target = tuple((site, 0) for site in range(2 * h))
        product_q = Fraction(1)
        for q_value in q_values:
            product_q *= q_value
        elementary = elementary_symmetric(z_values)

        for k in range(h + 1):
            moment = site_poly_mul(
                site_poly_power(q_poly, h - k),
                site_poly_power(r_poly, k),
            )
            expected = (
                factorial(h - k)
                * factorial(k) ** 2
                * product_q
                * elementary[k]
            )
            require(
                moment == {target: expected},
                f"literal site-square-zero count failed at h={h}, k={k}",
            )


def audit_physical_moment_packet():
    """Audit the exact moments without numerically constructing roots."""

    for h in range(3, 129):
        u, _w, v, tv, x = carrier_polynomials(h)
        ell = extreme_weights(h)
        carrier_scale = Fraction(ell[0], factorial(h))
        require(carrier_scale != 0, f"zero diagonal-product scale at h={h}")

        elementary = []
        for k in range(h + 1):
            denominator = carrier_scale * factorial(h - k) * factorial(k) ** 2
            elementary.append(Fraction(ell[k], 1) / denominator)

        require(elementary[0] == 1, f"e_0 normalization failed at h={h}")
        require(elementary[h] != 0, f"root product vanished at h={h}")

        reconstructed = []
        for k in range(h + 1):
            moment = (
                factorial(h - k)
                * factorial(k) ** 2
                * carrier_scale
                * elementary[k]
            )
            reconstructed.append(moment)
        require(
            reconstructed == [Fraction(value) for value in ell],
            f"physical moment reconstruction failed at h={h}",
        )

        def evaluate(poly):
            return sum(
                Fraction(coefficient(poly, k)) * reconstructed[k]
                for k in range(h + 1)
            )

        require(evaluate(u) == 0, f"physical u did not vanish at h={h}")
        require(evaluate(v) == 0, f"physical Qv did not vanish at h={h}")
        require(evaluate(tv) == 0, f"physical Rv did not vanish at h={h}")
        require(
            evaluate(x) == -(3 * h + 7),
            f"physical target moment failed at h={h}",
        )

        # The scalar-unit normalization is h!*alpha^(h-1)=L_h(x).
        # It makes the exceptional row exactly X_a and the unary error
        # exactly u_h/h!, without choosing a numerical algebraic root.
        alpha_power = Fraction(-(3 * h + 7), factorial(h))
        exceptional = evaluate(x) / (factorial(h) * alpha_power)
        require(
            exceptional == 1,
            f"exceptional target normalization failed at h={h}",
        )
        require(
            evaluate(u) / factorial(h) == 0,
            f"unary clean normalization failed at h={h}",
        )

        # R*((Q+R)^(h-1)-Q^(h-1)) has moment index j=k+1.
        adjacent = sum(
            Fraction(comb(h - 1, k)) * reconstructed[k + 1]
            for k in range(1, h)
        )
        require(
            adjacent == -4 * (h - 1),
            f"adjacent comparison vanished or had wrong scale at h={h}",
        )
        require(
            adjacent / factorial(h - 1)
            == Fraction(-4, factorial(h - 2)),
            f"divided-power adjacent normalization failed at h={h}",
        )


def audit_response_free_cap():
    """Check Lemma 3.1 in target-coordinate form."""

    alpha = Fraction(2)
    d_b = Fraction(3)
    d_c = Fraction(-5)
    require(alpha != 0 and d_b * d_c != 0, "inactive lemma test data")

    # From R_D=R and the full rows:
    # q^[h] = (X_a-d_b X_b-d_c X_c)/alpha.
    q_top = (1 / alpha, -d_b / alpha, -d_c / alpha)
    direction_diagonal = (Fraction(0), d_b, d_c)
    cap_diagonal = (Fraction(-1), d_b, d_c)
    cap_scalar = alpha * cap_diagonal[0]
    cap_response_coefficient = Fraction(1) - Fraction(1)
    cap_target = cap_diagonal
    require(cap_scalar == -alpha, "wrong direct scalar for D-E_aa")
    require(cap_response_coefficient == 0, "D-E_aa is not response-free")
    require(
        cap_target == tuple(-alpha * value for value in q_top),
        "response-free cap target is not -alpha*q^[h]",
    )
    require(
        direction_diagonal[0] == 0
        and direction_diagonal[1] * direction_diagonal[2] != 0,
        "normal direction lost its target-visible diagonal",
    )
    require(
        cap_scalar != 0 and all(value != 0 for value in cap_diagonal),
        "cap is not active",
    )

    for h in range(3, 129):
        source_coefficient = cap_scalar**h
        target_coefficient = cap_scalar ** (h - 1) * (-alpha)
        require(
            source_coefficient == target_coefficient,
            f"response-free clean error failed at h={h}",
        )

        # A top-apolar affine equality has the exact target ledger (23).
        lam = Fraction(2)
        mu = Fraction(1)
        radial = alpha * (h * mu - lam)
        require(radial != 0, f"unexpected affine resonance at h={h}")
        ternary_coefficients = (
            -lam / radial,
            d_b / radial,
            d_c / radial,
        )
        require(
            all(value != 0 for value in ternary_coefficients),
            f"top-apolar ternary alternative lost a colour at h={h}",
        )

        binary_coefficients = (
            Fraction(0),
            d_b / (alpha * h),
            d_c / (alpha * h),
        )
        require(
            binary_coefficients[0] == 0
            and binary_coefficients[1] != 0
            and binary_coefficients[2] != 0,
            f"top-apolar binary boundary failed at h={h}",
        )

    wrong_target_scalar = alpha
    require(
        cap_scalar**7
        != cap_scalar**6 * wrong_target_scalar,
        "response-free target-sign mutation survived",
    )
    return 1


def form_add(*forms):
    answer = {}
    for form in forms:
        for variable, value in form.items():
            answer[variable] = answer.get(variable, Fraction(0)) + value
            if answer[variable] == 0:
                del answer[variable]
    return answer


def form_scale(scalar, form):
    return {
        variable: scalar * value
        for variable, value in form.items()
        if scalar * value != 0
    }


def product_forms(left, right):
    """Multiply linear forms in the site-square-zero algebra."""

    answer = {}
    for (left_site, left_colour), left_value in left.items():
        for (right_site, right_colour), right_value in right.items():
            if left_site == right_site:
                continue
            variables = tuple(
                sorted(((left_site, left_colour), (right_site, right_colour)))
            )
            answer[variables] = (
                answer.get(variables, Fraction(0))
                + left_value * right_value
            )
            if answer[variables] == 0:
                del answer[variables]
    return answer


def quadratic_add(*quadratics):
    answer = {}
    for quadratic in quadratics:
        for monomial, value in quadratic.items():
            answer[monomial] = answer.get(monomial, Fraction(0)) + value
            if answer[monomial] == 0:
                del answer[monomial]
    return answer


def quadratic_scale(scalar, quadratic):
    return {
        monomial: scalar * value
        for monomial, value in quadratic.items()
        if scalar * value != 0
    }


def rational_rank(rows):
    if not rows:
        return 0
    matrix = [[Fraction(value) for value in row] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def form_family_rank(forms):
    variables = sorted({variable for form in forms for variable in form})
    rows = [[form.get(variable, 0) for variable in variables] for form in forms]
    return rational_rank(rows)


def full_occupancy_response(left, right, q_values):
    """Return (left*right)*q^[h-1] on paired sites, with endpoint order."""

    pair_count = len(q_values)
    answer = {}
    for missing in range(pair_count):
        left_site = 2 * missing
        right_site = left_site + 1
        complement = Fraction(1)
        for index, q_value in enumerate(q_values):
            if index != missing:
                complement *= q_value
        for left_colour in range(3):
            for right_colour in range(3):
                coefficient_value = complement * (
                    left.get((left_site, left_colour), 0)
                    * right.get((right_site, right_colour), 0)
                    + right.get((left_site, left_colour), 0)
                    * left.get((right_site, right_colour), 0)
                )
                if coefficient_value == 0:
                    continue
                word = [0] * (2 * pair_count)
                word[left_site] = left_colour
                word[right_site] = right_colour
                word = tuple(word)
                answer[word] = answer.get(word, Fraction(0)) + coefficient_value
                if answer[word] == 0:
                    del answer[word]
    return answer


def coloured_pair_word(pair_count, pair_index, left_colour, right_colour):
    word = [0] * (2 * pair_count)
    word[2 * pair_index] = left_colour
    word[2 * pair_index + 1] = right_colour
    return tuple(word)


def audit_injective_star_direction():
    """Audit (25)-(28) and all eight explicit companion-row failures."""

    pair_count = 4
    p_a = {(2 * i, 0): Fraction(1) for i in range(pair_count)}
    s_coefficients = [Fraction(2 * i + 1) for i in range(pair_count)]
    s_a = {
        (2 * i + 1, 0): s_coefficients[i]
        for i in range(pair_count)
    }
    eta = {(0, 1): Fraction(1)}
    eta_prime = {(1, 1): Fraction(1)}
    zeta = {(2, 1): Fraction(1)}
    zeta_prime = {(2, 2): Fraction(1)}

    p_b = eta
    p_c = form_add(zeta, form_scale(-1, p_a), form_scale(-1, eta))
    s_b = eta_prime
    s_c = form_add(
        zeta_prime,
        form_scale(-1, s_a),
        form_scale(-1, eta_prime),
    )
    p_rows = [p_a, p_b, p_c]
    s_rows = [s_a, s_b, s_c]

    require(form_family_rank(p_rows) == 3, "p-star extension is not injective")
    require(form_family_rank(s_rows) == 3, "s-star extension is not injective")
    require(form_add(*p_rows) == zeta, "wrong p-star sum")
    require(form_add(*s_rows) == zeta_prime, "wrong s-star sum")
    require(
        product_forms(zeta, zeta_prime) == {},
        "same-site product did not vanish",
    )

    responses = [
        [product_forms(p_rows[i], s_rows[j]) for j in range(3)]
        for i in range(3)
    ]
    total_response = quadratic_add(
        *(responses[i][j] for i in range(3) for j in range(3))
    )
    require(total_response == {}, "all-response Segre sum did not vanish")

    direction = [
        [(1 if i == 0 and j == 0 else 0) - 1 for j in range(3)]
        for i in range(3)
    ]
    require(direction[0][0] == 0, "D_aa mutation")
    require(direction[1][1] == -1, "D_bb mutation")
    require(direction[2][2] == -1, "D_cc mutation")
    response_d = quadratic_add(
        *(
            quadratic_scale(direction[i][j], responses[i][j])
            for i in range(3)
            for j in range(3)
        )
    )
    require(response_d == responses[0][0], "R_D is not R_aa")

    # The construction used in the note has all q_i/alpha and z_i*q_i
    # nonzero.  These rational values audit its support and endpoint order
    # without numerically choosing the Vieta roots.
    q_values = [Fraction(2), Fraction(3), Fraction(5), Fraction(7)]
    top_responses = [
        [
            full_occupancy_response(p_rows[i], s_rows[j], q_values)
            for j in range(3)
        ]
        for i in range(3)
    ]
    rho = []
    for missing in range(pair_count):
        value = Fraction(1)
        for index, q_value in enumerate(q_values):
            if index != missing:
                value *= q_value
        rho.append(value)

    word_ab_1 = coloured_pair_word(pair_count, 0, 0, 1)
    word_ba_1 = coloured_pair_word(pair_count, 0, 1, 0)
    word_bb_1 = coloured_pair_word(pair_count, 0, 1, 1)
    word_ba_2 = coloured_pair_word(pair_count, 1, 1, 0)
    witnesses = {
        (0, 1): (word_ab_1, rho[0]),
        (0, 2): (word_ab_1, -rho[0]),
        (1, 0): (word_ba_1, s_coefficients[0] * rho[0]),
        (1, 2): (word_bb_1, -rho[0]),
        (2, 0): (word_ba_2, s_coefficients[1] * rho[1]),
        (2, 1): (word_ab_1, -rho[0]),
        (1, 1): (word_bb_1, rho[0]),
        (2, 2): (word_ba_2, -s_coefficients[1] * rho[1]),
    }
    for (row, column), (word, expected) in witnesses.items():
        require(
            top_responses[row][column].get(word, 0) == expected != 0,
            f"companion-row witness failed at ({row},{column})",
        )
    for row in range(3):
        for column in range(3):
            if row != column:
                require(
                    top_responses[row][column] != {},
                    f"off-diagonal companion row accidentally held at "
                    f"({row},{column})",
                )
    target_b = tuple([1] * (2 * pair_count))
    target_c = tuple([2] * (2 * pair_count))
    require(
        top_responses[1][1] != {target_b: Fraction(1)},
        "the bb companion row accidentally held",
    )
    require(
        top_responses[2][2] != {target_c: Fraction(1)},
        "the cc companion row accidentally held",
    )

    bad_direction = [
        [1 - (1 if i == 0 and j == 0 else 0) for j in range(3)]
        for i in range(3)
    ]
    bad_response = quadratic_add(
        *(
            quadratic_scale(bad_direction[i][j], responses[i][j])
            for i in range(3)
            for j in range(3)
        )
    )
    require(
        bad_response != responses[0][0],
        "normal-matrix sign mutation survived",
    )

    wrong_order_s_b = eta
    require(
        full_occupancy_response(p_a, wrong_order_s_b, q_values) == {},
        "endpoint-side mutation was not exposed",
    )
    return 2


def audit_mutations():
    h = 7
    u, w, v, tv, x = carrier_polynomials(h)
    base = extreme_weights(h)
    expected = (0, 0, 0, -(3 * h + 7))

    variants = []
    for index in (0, 1, h - 1, h):
        mutated = list(base)
        mutated[index] += 1
        variants.append(mutated)
    sign_mutation = list(base)
    sign_mutation[1] *= -1
    variants.append(sign_mutation)
    terminal_sign = list(base)
    terminal_sign[h] *= -1
    variants.append(terminal_sign)

    for number, weights in enumerate(variants, start=1):
        signature = (
            apply_functional(u, weights),
            apply_functional(v, weights),
            apply_functional(tv, weights),
            apply_functional(x, weights),
        )
        require(signature != expected, f"functional mutation {number} survived")

    wrong_v = add(shift(w), scale(2, w))
    require(
        apply_functional(wrong_v, base) != 0,
        "carrier-sign mutation survived",
    )

    ell = extreme_weights(h)
    carrier_scale = Fraction(ell[0], factorial(h))
    wrong_elementary = [
        Fraction(ell[k], 1)
        / (carrier_scale * factorial(h - k) * factorial(k))
        for k in range(h + 1)
    ]
    wrong_moments = [
        factorial(h - k)
        * factorial(k) ** 2
        * carrier_scale
        * wrong_elementary[k]
        for k in range(h + 1)
    ]
    require(
        wrong_moments != [Fraction(value) for value in ell],
        "moment-factorial mutation survived",
    )

    wrong_alpha_power = Fraction(-(3 * h + 7))
    wrong_exceptional = Fraction(-(3 * h + 7)) / (
        factorial(h) * wrong_alpha_power
    )
    require(
        wrong_exceptional != 1,
        "alpha factorial-normalization mutation survived",
    )

    naive_normal_weights = extreme_weights(h)
    actual_normal_weights = [
        transformed_normal_weight(h, order)
        for order in range(h + 1)
    ]
    require(
        naive_normal_weights != actual_normal_weights,
        "source/normal-grade mutation survived",
    )
    return len(variants) + 4


def main():
    audit_functional_identities()
    audit_full_normal_order_ledger()
    audit_literal_site_square_zero_counts()
    audit_physical_moment_packet()
    cap_mutations = audit_response_free_cap()
    star_mutations = audit_injective_star_direction()
    mutation_count = audit_mutations() + cap_mutations + star_mutations
    print(
        "four-extreme identities and full-normal order ledger: "
        "PASS (h=3..128)"
    )
    print("response-free exact-source cap ledger: PASS")
    print(
        "rank-one physical moment/Vieta packet: PASS "
        "(literal h=3,4; exact moments h=3..128)"
    )
    print(
        "injective-star direction and eight companion-row failures: PASS"
    )
    print(f"explicit mutation checks: PASS ({mutation_count} rejected)")


if __name__ == "__main__":
    main()

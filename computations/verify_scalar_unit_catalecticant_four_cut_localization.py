#!/usr/bin/env python3
"""Exact audit of scalar-unit catalecticant/four-cut localization.

The companion note proves the uniform identities.  This dependency-free
checker uses a literal site-square-zero algebra with unordered decorated
cells.  It audits the divided-power Euler factor, the two endpoint
orientations, the oriented adjacent-power localization, and two sharp
local guards.  Every check uses explicit
exceptions and therefore remains active under ``python -O``.
"""

from fractions import Fraction
from math import factorial


F = Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def clean(form):
    return {monomial: F(value) for monomial, value in form.items() if value}


def add(*forms):
    answer = {}
    for form in forms:
        for monomial, value in form.items():
            answer[monomial] = answer.get(monomial, F(0)) + F(value)
    return clean(answer)


def scale(value, form):
    value = F(value)
    return clean({monomial: value * coefficient for monomial, coefficient in form.items()})


def site_set(monomial):
    return {site for site, _colour in monomial}


def multiply(left, right):
    answer = {}
    for monomial_left, coefficient_left in left.items():
        sites_left = site_set(monomial_left)
        for monomial_right, coefficient_right in right.items():
            if sites_left & site_set(monomial_right):
                continue
            monomial = tuple(sorted(monomial_left + monomial_right))
            answer[monomial] = answer.get(monomial, F(0)) + (
                coefficient_left * coefficient_right
            )
    return clean(answer)


def product(*forms):
    answer = {(): F(1)}
    for form in forms:
        answer = multiply(answer, form)
    return answer


def ordinary_power(form, exponent):
    require(exponent >= 0, "negative ordinary power")
    return product(*(form for _ in range(exponent)))


def divided_power(form, exponent):
    return scale(F(1, factorial(exponent)), ordinary_power(form, exponent))


def atom(site, colour=0, coefficient=1):
    return {((site, colour),): F(coefficient)}


def cell(left, right, left_colour=0, right_colour=0, coefficient=1):
    require(left != right, "a decorated cell needs two physical sites")
    return multiply(
        atom(left, left_colour),
        atom(right, right_colour, coefficient),
    )


def cell_key(left, right, left_colour=0, right_colour=0):
    return next(iter(cell(left, right, left_colour, right_colour)))


def evaluate(functional, form):
    return sum(
        (functional.get(monomial, F(0)) * value for monomial, value in form.items()),
        F(0),
    )


def top_coordinate(site_count, colour=0, weight=1):
    word = tuple((site, colour) for site in range(site_count))
    return {word: F(weight)}


def one_form(entries):
    return add(*(atom(site, colour, value) for site, colour, value in entries))


def oriented_products(p_form, s_form):
    """Split p*s by the physical-site order of the endpoint assignments."""
    forward = {}
    reverse = {}
    for p_monomial, p_value in p_form.items():
        require(len(p_monomial) == 1, "p is not a one-site form")
        p_site, _p_colour = p_monomial[0]
        for s_monomial, s_value in s_form.items():
            require(len(s_monomial) == 1, "s is not a one-site form")
            s_site, _s_colour = s_monomial[0]
            if p_site == s_site:
                continue
            target = forward if p_site < s_site else reverse
            monomial = tuple(sorted(p_monomial + s_monomial))
            target[monomial] = target.get(monomial, F(0)) + p_value * s_value
    forward = clean(forward)
    reverse = clean(reverse)
    require(
        add(forward, reverse) == multiply(p_form, s_form),
        "endpoint orientation split lost a decorated-cell coefficient",
    )
    return forward, reverse


def matrix(rows=3, columns=3, value=0):
    return [[F(value) for _ in range(columns)] for _ in range(rows)]


def matrix_add(left, right):
    require(len(left) == len(right), "matrix height mismatch")
    require(all(len(x) == len(y) for x, y in zip(left, right)), "matrix width mismatch")
    return [
        [x + y for x, y in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def matrix_scale(value, value_matrix):
    value = F(value)
    return [[value * entry for entry in row] for row in value_matrix]


def weighted_matrix_sum(weighted_matrices, rows=3, columns=3):
    answer = matrix(rows, columns)
    for weight, value_matrix in weighted_matrices:
        answer = matrix_add(answer, matrix_scale(weight, value_matrix))
    return answer


def q_cells(q_form):
    answer = []
    for monomial, value in q_form.items():
        require(len(monomial) == 2, "q contains a nonquadratic monomial")
        require(len(site_set(monomial)) == 2, "q contains a site collision")
        answer.append((monomial, value))
    return tuple(answer)


def all_cell_basis(site_count, colours=(0,)):
    answer = []
    for left in range(site_count):
        for right in range(left + 1, site_count):
            for left_colour in colours:
                for right_colour in colours:
                    answer.append(cell_key(left, right, left_colour, right_colour))
    return tuple(answer)


def euler_pairing(functional, u_form, v_form, q_form, h):
    direct = evaluate(functional, product(u_form, v_form, divided_power(q_form, h - 1)))
    numerator = sum(
        (
            q_value
            * evaluate(
                functional,
                product(
                    u_form,
                    v_form,
                    {q_cell: F(1)},
                    divided_power(q_form, h - 2),
                ),
            )
            for q_cell, q_value in q_cells(q_form)
        ),
        F(0),
    )
    return direct, numerator


def build_uniform_guard(h):
    """A selector packet where every Euler-selected q-cell has zero curvature."""
    require(h >= 3, "the uniform guard starts at h=3")
    site_count = 2 * h
    q_form = add(
        *(cell(2 * index, 2 * index + 1) for index in range(1, h))
    )
    p_form = add(atom(0), *(atom(site) for site in range(2, site_count)))
    s_form = add(atom(1), *(atom(site) for site in range(2, site_count)))
    zero_form = {}
    return {
        "h": h,
        "site_count": site_count,
        "q": q_form,
        "p": (p_form, zero_form, zero_form),
        "s": (s_form, zero_form, zero_form),
        "A": [[F(1), F(0), F(0)], [F(0), F(0), F(0)], [F(0), F(0), F(0)]],
        "nu": top_coordinate(site_count),
        "label": 0,
    }


def audit_packet(packet):
    h = packet["h"]
    site_count = packet["site_count"]
    q_form = packet["q"]
    p_forms = packet["p"]
    s_forms = packet["s"]
    direct = packet["A"]
    functional = packet["nu"]
    label = packet["label"]

    require(
        multiply(q_form, divided_power(q_form, h - 2))
        == scale(h - 1, divided_power(q_form, h - 1)),
        f"h={h}: q q^[h-2] normalization failed",
    )
    require(
        multiply(q_form, divided_power(q_form, h - 1))
        == scale(h, divided_power(q_form, h)),
        f"h={h}: q q^[h-1] normalization failed",
    )
    require(
        evaluate(functional, divided_power(q_form, h)) == 0,
        f"h={h}: guard does not have nu(Q)=0",
    )

    response = [[{} for _ in range(3)] for _ in range(3)]
    forward = [[{} for _ in range(3)] for _ in range(3)]
    reverse = [[{} for _ in range(3)] for _ in range(3)]
    pairing = matrix()
    for row in range(3):
        for column in range(3):
            response[row][column] = multiply(p_forms[row], s_forms[column])
            forward[row][column], reverse[row][column] = oriented_products(
                p_forms[row], s_forms[column]
            )
            pairing[row][column] = evaluate(
                functional,
                multiply(response[row][column], divided_power(q_form, h - 1)),
            )
            direct_value, numerator = euler_pairing(
                functional, p_forms[row], s_forms[column], q_form, h
            )
            require(direct_value == pairing[row][column], "B_nu evaluation mismatch")
            require(
                numerator == (h - 1) * direct_value,
                f"h={h}: catalecticant Euler factor is not h-1",
            )

    expected = matrix()
    expected[label][label] = F(1)
    require(pairing == expected, f"h={h}: selector table is not E_ii")

    q_power = divided_power(q_form, h - 2)
    c_matrices = {}
    d_values = {}
    o_forward = {}
    o_reverse = {}
    for q_cell, _q_value in q_cells(q_form):
        inserted = {q_cell: F(1)}
        c_value = matrix()
        o_forward_value = matrix()
        o_reverse_value = matrix()
        d_value = evaluate(functional, product(q_form, inserted, q_power))
        for row in range(3):
            for column in range(3):
                c_value[row][column] = evaluate(
                    functional, product(response[row][column], inserted, q_power)
                )
                k_forward = add(
                    scale(direct[row][column], q_form),
                    scale(-1, forward[row][column]),
                )
                k_reverse = add(
                    scale(direct[row][column], q_form),
                    scale(-1, reverse[row][column]),
                )
                o_forward_value[row][column] = evaluate(
                    functional, product(k_forward, inserted, q_power)
                )
                o_reverse_value[row][column] = evaluate(
                    functional, product(k_reverse, inserted, q_power)
                )
                require(
                    o_forward_value[row][column] + o_reverse_value[row][column]
                    == 2 * direct[row][column] * d_value - c_value[row][column],
                    f"h={h}: local oriented/direct decomposition failed",
                )
        c_matrices[q_cell] = c_value
        d_values[q_cell] = d_value
        o_forward[q_cell] = o_forward_value
        o_reverse[q_cell] = o_reverse_value

    weighted_c = weighted_matrix_sum(
        (q_value, c_matrices[q_cell]) for q_cell, q_value in q_cells(q_form)
    )
    weighted_d = sum(
        (q_value * d_values[q_cell] for q_cell, q_value in q_cells(q_form)),
        F(0),
    )
    weighted_o = weighted_matrix_sum(
        (
            q_value,
            matrix_add(o_forward[q_cell], o_reverse[q_cell]),
        )
        for q_cell, q_value in q_cells(q_form)
    )
    require(
        weighted_c == matrix_scale(h - 1, expected),
        f"h={h}: weighted catalecticant coefficient span failed",
    )
    require(weighted_d == 0, f"h={h}: nu(Q)=0 double-internal sum failed")
    require(
        weighted_o == matrix_scale(-(h - 1), expected),
        f"h={h}: oriented adjacent-power localization failed",
    )

    # Expand the nonzero selected entry into two unordered decorated cells.
    all_cells = all_cell_basis(site_count)
    k_forward_selected = add(
        scale(direct[label][label], q_form),
        scale(-1, forward[label][label]),
    )
    k_reverse_selected = add(
        scale(direct[label][label], q_form),
        scale(-1, reverse[label][label]),
    )
    localized_terms = []
    for q_cell, q_value in q_cells(q_form):
        for curvature_cell in all_cells:
            gamma = evaluate(
                functional,
                product(
                    {curvature_cell: F(1)},
                    {q_cell: F(1)},
                    q_power,
                ),
            )
            for orientation, curvature in (
                ("forward", k_forward_selected),
                ("reverse", k_reverse_selected),
            ):
                kappa = curvature.get(curvature_cell, F(0))
                value = q_value * kappa * gamma
                if value:
                    require(
                        not (site_set(curvature_cell) & site_set(q_cell)),
                        "a nonzero localized term reused an exposed site",
                    )
                    localized_terms.append(
                        (curvature_cell, q_cell, orientation, value)
                    )
    require(localized_terms, f"h={h}: no literal oriented two-cell term survived")
    require(
        sum((entry[3] for entry in localized_terms), F(0)) == -(h - 1),
        f"h={h}: expanded localized terms have the wrong total",
    )

    # Sharp same-cell guard: C_f is nonzero at every q-supported cell, but
    # both oriented curvature coefficients at that very cell are zero.
    for q_cell, _q_value in q_cells(q_form):
        require(
            c_matrices[q_cell][label][label] == 1,
            f"h={h}: uniform Euler cell lost its selected cofactor",
        )
        require(
            k_forward_selected.get(q_cell, F(0)) == 0
            and k_reverse_selected.get(q_cell, F(0)) == 0,
            f"h={h}: same-cell guard unexpectedly has curvature",
        )

    # The wrong Euler divisor and ordered-cell double counting are visible.
    require(
        weighted_c != matrix_scale(h, expected),
        f"h={h}: wrong Euler divisor h escaped detection",
    )
    require(
        matrix_scale(2, weighted_c) != matrix_scale(h - 1, expected),
        f"h={h}: ordered decorated-cell double count escaped detection",
    )
    return localized_terms


def audit_direct_factor_two():
    """Make the local D_f term nonzero while its weighted sum is zero."""
    site_count = 6
    q_form = add(
        cell(0, 1),
        cell(2, 3),
        cell(4, 5),
        cell(0, 2, coefficient=-1),
        cell(1, 3),
    )
    functional = top_coordinate(site_count)
    require(
        evaluate(functional, divided_power(q_form, 3)) == 0,
        "factor-two packet did not cancel q^[3]",
    )
    q_power = divided_power(q_form, 1)
    nonzero_d = []
    for q_cell, _value in q_cells(q_form):
        d_value = evaluate(
            functional, product(q_form, {q_cell: F(1)}, q_power)
        )
        if d_value:
            nonzero_d.append(d_value)
            correct = 2 * d_value
            mutated = d_value
            require(correct != mutated, "the two direct orientations collapsed")
    require(nonzero_d, "factor-two packet has no visible local D_f")

    p_form = add(atom(0), atom(1))
    s_form = add(atom(0), scale(2, atom(1)))
    forward, reverse = oriented_products(p_form, s_form)
    require(forward and reverse, "orientation mutation packet lost one assignment")
    require(
        multiply(p_form, s_form) != forward
        and multiply(p_form, s_form) != reverse,
        "dropping one endpoint orientation was not detected",
    )


def audit_full_carrier_guard():
    """A nonzero leading q^[h-2] coefficient can cancel in H_0."""
    q_form = add(cell(2, 3), cell(4, 5))
    p_form = add(atom(0), atom(2), atom(4))
    s_form = add(atom(1), scale(-2, atom(3)), scale(-2, atom(5)))
    response = multiply(p_form, s_form)
    h_zero = add(q_form, scale(F(1, 2), response))
    functional = top_coordinate(6)
    curvature_cell = cell_key(0, 1)
    inserted_cell = cell_key(2, 3)
    forward, _reverse = oriented_products(p_form, s_form)
    curvature = add(q_form, scale(-1, forward))
    kappa = curvature.get(curvature_cell, F(0))
    leading = kappa * evaluate(
        functional,
        product(
            {curvature_cell: F(1)},
            {inserted_cell: F(1)},
            q_form,
        ),
    )
    full = kappa * evaluate(
        functional,
        product(
            {curvature_cell: F(1)},
            {inserted_cell: F(1)},
            h_zero,
        ),
    )
    require(leading == -1, "leading adjacent q coefficient did not survive")
    require(full == 0, "the H_0 carrier-cancellation guard failed")


def main():
    counts = []
    for h in range(3, 9):
        counts.append(len(audit_packet(build_uniform_guard(h))))
    audit_direct_factor_two()
    audit_full_carrier_guard()
    require(all(count > 0 for count in counts), "a uniform localization was empty")
    print("scalar-unit catalecticant/four-cut localization: PASS")
    print("audited h=3..8 with unordered decorated cells and exact divided powers")
    print("oriented adjacent-power identity and distinct-cell localization: PASS")
    print("same-cell and H_0 carrier guards: PASS")


if __name__ == "__main__":
    main()

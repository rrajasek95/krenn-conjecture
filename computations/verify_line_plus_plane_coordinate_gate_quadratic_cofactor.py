#!/usr/bin/env python3
"""Audit the exact quadratic cofactor on the two b=2 coordinate gates.

The line-plus-plane clean pencil can fail activity because the rank-two
kernel misses one physical label, or because the rank-one shore is one
fixed physical row.  Perturb in the missing coordinate.  In either case
the response has matching number at most two, and its divided square
factors as twice two local endpoint values times one fixed shore cofactor.

This standard-library checker works in the universal site-square-zero
support algebra after exact rational specialization.  It audits all three
physical labels at residual half-sizes h=3,4,5.  Research evidence only.
"""

from fractions import Fraction as Q
from hashlib import sha256
from math import factorial


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


EXPECTED_DIGEST = "6a8b69aeb4c5225e815412545239b1636949b18eb4f091b0c063ec49b0715f57"


def add(left, right):
    answer = dict(left)
    for support, coefficient in right.items():
        answer[support] = answer.get(support, Q(0)) + coefficient
        if answer[support] == 0:
            del answer[support]
    return answer


def scale(element, coefficient):
    coefficient = Q(coefficient)
    if coefficient == 0:
        return {}
    return {
        support: coefficient * value
        for support, value in element.items()
        if coefficient * value
    }


def multiply(left, right):
    answer = {}
    for left_support, left_coefficient in left.items():
        for right_support, right_coefficient in right.items():
            if left_support & right_support:
                continue
            support = left_support | right_support
            answer[support] = (
                answer.get(support, Q(0))
                + left_coefficient * right_coefficient
            )
            if answer[support] == 0:
                del answer[support]
    return answer


def divided_power(element, power):
    require(power >= 0, ("negative divided power", power))
    answer = {frozenset(): Q(1)}
    for _step in range(power):
        answer = multiply(answer, element)
    return scale(answer, Q(1, factorial(power)))


def linear_element(values):
    return {
        frozenset((site,)): Q(value)
        for site, value in enumerate(values)
        if value
    }


def restrict(element, sites):
    sites = frozenset(sites)
    return {
        support: coefficient
        for support, coefficient in element.items()
        if support <= sites
    }


def linear_combination(rows, coefficients):
    answer = {}
    for row, coefficient in zip(rows, coefficients):
        answer = add(answer, scale(row, coefficient))
    return answer


def local_value(element, site):
    return element.get(frozenset((site,)), Q(0))


def quadratic(sites):
    answer = {}
    for left in sites:
        for right in sites:
            if left >= right:
                continue
            coefficient = Q(
                (left + 2) * (right + 3)
                + (left + right) % 5 + 1
            )
            answer[frozenset((left, right))] = coefficient
    return answer


def scalar(matrix, left, right):
    return sum(
        left[i] * matrix[i][j] * right[j]
        for i in range(3) for j in range(3)
    )


def error(q, response, sigma, h):
    answer = {}
    for power in range(2, h + 1):
        answer = add(answer, scale(
            multiply(
                divided_power(q, h - power),
                divided_power(response, power),
            ),
            Q(sigma) ** (h - power),
        ))
    return answer


def serialize(element):
    return tuple(
        (tuple(sorted(support)), coefficient.numerator,
         coefficient.denominator)
        for support, coefficient in sorted(
            element.items(), key=lambda item: tuple(sorted(item[0]))
        )
    )


def base_rows(h):
    site_count = 2 * h
    a_sites = tuple(range(site_count - 2))
    u, v = site_count - 2, site_count - 1
    all_sites = tuple(range(site_count))
    u_values = tuple(Q((site + 1) * (1 + (site % 3)))
                     for site in all_sites)
    t_values = tuple(Q((site + 2) * (2 + (site % 2)))
                     for site in all_sites)
    r_values = tuple(Q((site + 3) * (3 + ((site + 1) % 3)))
                     for site in all_sites)
    matrix = tuple(
        tuple(Q(2 + 3 * i - 2 * j + i * j) for j in range(3))
        for i in range(3)
    )
    return a_sites, u, v, all_sites, u_values, t_values, r_values, matrix


def gate_one_instance(h, missing, c, parameter):
    """The right kernel has d_missing=0; perturb it by parameter e_missing."""
    (a_sites, u, v, all_sites,
     u_values, t_values, r_values, matrix) = base_rows(h)
    alpha = (Q(1), Q(2), Q(-1))
    require(sum(alpha[i] * c[i] for i in range(3)) == 0,
            ("left vector left the shore kernel", c))

    p_rows = []
    for label in range(3):
        values = [
            alpha[label] * u_values[site]
            if site in a_sites
            else Q((label + 2) * (site + 1) - 3)
            for site in all_sites
        ]
        p_rows.append(linear_element(values))

    other = tuple(label for label in range(3) if label != missing)
    d = [Q(0)] * 3
    d[other[0]], d[other[1]] = Q(2), Q(-3)
    s_rows = [None] * 3
    for label in range(3):
        if label == missing:
            a_values = r_values
        elif label == other[0]:
            a_values = tuple(3 * value for value in t_values)
        else:
            a_values = tuple(2 * value for value in t_values)
        values = [
            a_values[site]
            if site in a_sites
            else Q((label + 4) * (site + 2) + 1)
            for site in all_sites
        ]
        s_rows[label] = linear_element(values)
    require(not restrict(linear_combination(s_rows, d), a_sites),
            ("right shore kernel changed", h, missing))

    perturbed = tuple(
        d[label] + (parameter if label == missing else 0)
        for label in range(3)
    )
    p_c = linear_combination(p_rows, c)
    s_perturbed = linear_combination(s_rows, perturbed)
    require(not restrict(p_c, a_sites),
            ("left shore kernel changed", h, missing, c))
    response = multiply(p_c, s_perturbed)
    response_two = divided_power(response, 2)
    require(not divided_power(response, 3),
            ("gate-one response acquired matching number three",
             h, missing, c, parameter))

    s_missing_a = restrict(s_rows[missing], a_sites)
    local_product = multiply(
        scale(linear_element(
            [Q(1) if site == u else Q(0) for site in all_sites]
        ), local_value(p_c, u)),
        scale(linear_element(
            [Q(1) if site == v else Q(0) for site in all_sites]
        ), local_value(p_c, v)),
    )
    expected_two = scale(
        multiply(local_product, divided_power(s_missing_a, 2)),
        2 * Q(parameter) ** 2,
    )
    require(response_two == expected_two,
            ("gate-one divided-square factor changed",
             h, missing, c, parameter))

    q = quadratic(all_sites)
    q_a = restrict(q, a_sites)
    sigma = scalar(matrix, c, perturbed)
    actual_error = error(q, response, sigma, h)
    expected_error = scale(
        multiply(
            local_product,
            multiply(
                divided_power(s_missing_a, 2),
                divided_power(q_a, h - 2),
            ),
        ),
        2 * Q(parameter) ** 2 * Q(sigma) ** (h - 2),
    )
    require(actual_error == expected_error,
            ("gate-one clean-error factor changed",
             h, missing, c, parameter))
    return actual_error, sigma


def gate_two_instance(h, fixed_row, c_base, parameter):
    """The left shore is one fixed row; perturb c by parameter e_fixed."""
    (a_sites, u, v, all_sites,
     u_values, t_values, r_values, matrix) = base_rows(h)
    require(c_base[fixed_row] == 0,
            ("base vector left the coordinate kernel", c_base))

    p_rows = []
    for label in range(3):
        values = [
            u_values[site] if (
                label == fixed_row and site in a_sites
            ) else (
                Q((label + 2) * (site + 1) - 3)
                if site not in a_sites else Q(0)
            )
            for site in all_sites
        ]
        p_rows.append(linear_element(values))

    d = (Q(1), Q(2), Q(-1))
    s_a_rows = (
        r_values,
        t_values,
        tuple(r_values[site] + 2 * t_values[site]
              for site in all_sites),
    )
    s_rows = []
    for label in range(3):
        values = [
            s_a_rows[label][site]
            if site in a_sites
            else Q((label + 4) * (site + 2) + 1)
            for site in all_sites
        ]
        s_rows.append(linear_element(values))
    require(not restrict(linear_combination(s_rows, d), a_sites),
            ("right shore kernel changed", h, fixed_row))

    c = tuple(
        c_base[label] + (parameter if label == fixed_row else 0)
        for label in range(3)
    )
    p_c = linear_combination(p_rows, c)
    s_d = linear_combination(s_rows, d)
    require(not restrict(s_d, a_sites),
            ("right shore kernel changed", h, fixed_row, c_base))
    response = multiply(p_c, s_d)
    response_two = divided_power(response, 2)
    require(not divided_power(response, 3),
            ("gate-two response acquired matching number three",
             h, fixed_row, c_base, parameter))

    p_fixed_a = restrict(p_rows[fixed_row], a_sites)
    local_product = multiply(
        scale(linear_element(
            [Q(1) if site == u else Q(0) for site in all_sites]
        ), local_value(s_d, u)),
        scale(linear_element(
            [Q(1) if site == v else Q(0) for site in all_sites]
        ), local_value(s_d, v)),
    )
    expected_two = scale(
        multiply(local_product, divided_power(p_fixed_a, 2)),
        2 * Q(parameter) ** 2,
    )
    require(response_two == expected_two,
            ("gate-two divided-square factor changed",
             h, fixed_row, c_base, parameter))

    q = quadratic(all_sites)
    q_a = restrict(q, a_sites)
    sigma = scalar(matrix, c, d)
    actual_error = error(q, response, sigma, h)
    expected_error = scale(
        multiply(
            local_product,
            multiply(
                divided_power(p_fixed_a, 2),
                divided_power(q_a, h - 2),
            ),
        ),
        2 * Q(parameter) ** 2 * Q(sigma) ** (h - 2),
    )
    require(actual_error == expected_error,
            ("gate-two clean-error factor changed",
             h, fixed_row, c_base, parameter))
    return actual_error, sigma


def audit():
    ledger = []
    nonzero_errors = {"missing-kernel-label": 0, "fixed-row": 0}
    c_vectors = (
        (Q(1), Q(1), Q(3)),
        (Q(2), Q(1), Q(4)),
        (Q(1), Q(2), Q(5)),
    )
    parameters = (Q(1), Q(-2))
    for h in (3, 4, 5):
        for label in range(3):
            for c in c_vectors:
                for parameter in parameters:
                    value, sigma = gate_one_instance(
                        h, label, c, parameter
                    )
                    nonzero_errors["missing-kernel-label"] += bool(value)
                    ledger.append((
                        "missing", h, label, c, parameter, sigma,
                        serialize(value),
                    ))
            other = tuple(index for index in range(3) if index != label)
            bases = []
            for first, second in ((1, 2), (2, -1), (-1, 3)):
                vector = [Q(0)] * 3
                vector[other[0]], vector[other[1]] = first, second
                bases.append(tuple(vector))
            for c_base in bases:
                for parameter in parameters:
                    value, sigma = gate_two_instance(
                        h, label, c_base, parameter
                    )
                    nonzero_errors["fixed-row"] += bool(value)
                    ledger.append((
                        "fixed-row", h, label, c_base, parameter, sigma,
                        serialize(value),
                    ))
    require(all(count > 0 for count in nonzero_errors.values()),
            ("the coordinate cofactors became vacuous", nonzero_errors))
    digest = sha256(repr(tuple(ledger)).encode()).hexdigest()
    require(digest == EXPECTED_DIGEST,
            ("the coordinate-gate ledger changed", digest))
    return len(ledger), nonzero_errors, digest


def main():
    count, nonzero_errors, digest = audit()
    print("line-plus-plane coordinate-gate quadratic cofactor: passed")
    print(f"  exact rational instances : {count}")
    print(f"  nonzero error witnesses  : {nonzero_errors}")
    print(f"  aggregate ledger digest  : {digest}")
    print("  conclusion               : both gates reduce to one shore cofactor")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact lightweight guards for synchronized E2 factorization boundaries."""

from fractions import Fraction


def add(*polynomials):
    out = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            out[monomial] = out.get(monomial, Fraction(0)) + coefficient
    return {m: c for m, c in out.items() if c}


def scale(polynomial, scalar):
    return {m: scalar * c for m, c in polynomial.items() if scalar * c}


def multiply(left, right):
    out = {}
    for monomial_left, coefficient_left in left.items():
        sites_left = {site for site, _ in monomial_left}
        for monomial_right, coefficient_right in right.items():
            if sites_left & {site for site, _ in monomial_right}:
                continue
            monomial = tuple(sorted(monomial_left + monomial_right))
            out[monomial] = (
                out.get(monomial, Fraction(0))
                + coefficient_left * coefficient_right
            )
    return {m: c for m, c in out.items() if c}


def atom(site, color, coefficient=1):
    return {((site, color),): Fraction(coefficient)}


def cell(i, color_i, j, color_j, coefficient=1):
    return multiply(atom(i, color_i), atom(j, color_j, coefficient))


def pure_target(sites, color):
    result = {(): Fraction(1)}
    for site in sites:
        result = multiply(result, atom(site, color))
    return result


def restrict(polynomial, allowed_sites):
    allowed_sites = set(allowed_sites)
    return {
        monomial: coefficient
        for monomial, coefficient in polynomial.items()
        if all(site in allowed_sites for site, _ in monomial)
    }


def gauge(quadratic, alpha):
    return {
        monomial: coefficient * sum(alpha[site] for site, _ in monomial)
        for monomial, coefficient in quadratic.items()
        if coefficient * sum(alpha[site] for site, _ in monomial)
    }


def rank(matrix):
    a = [[Fraction(value) for value in row] for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    current = 0
    for col in range(cols):
        pivot = next((r for r in range(current, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[current], a[pivot] = a[pivot], a[current]
        pivot_value = a[current][col]
        a[current] = [value / pivot_value for value in a[current]]
        for r in range(rows):
            if r == current or not a[r][col]:
                continue
            factor = a[r][col]
            a[r] = [x - factor * y for x, y in zip(a[r], a[current])]
        current += 1
    return current


def coefficient_row(linear, sites=(0, 1, 2, 3), colors=(0, 1, 2)):
    return [
        linear.get(((site, color),), Fraction(0))
        for site in sites
        for color in colors
    ]


def audit_three_chart_holonomy():
    sites = set(range(5))
    fan = (0, 1, 2)
    center = add(atom(0, 1), atom(1, 0))
    q = add(cell(0, 1, 2, 0), scale(cell(1, 0, 2, 0), -1))
    alpha = (
        Fraction(1, 2),
        Fraction(-1, 2),
        Fraction(-1, 2),
        Fraction(0),
        Fraction(0),
    )
    assert sum(alpha) == Fraction(-1, 2)
    z = gauge(q, alpha)
    assert z == cell(1, 0, 2, 0)

    endpoint_rows = {
        0: atom(2, 0),
        1: {},
        2: {},
    }
    direct_entries = {0: Fraction(1), 1: Fraction(0), 2: Fraction(0)}
    for u in fan:
        chart = sites - {u}
        product = multiply(restrict(center, chart), endpoint_rows[u])
        assert product == restrict(z, chart)
        assert sum(alpha[i] for i in chart) == -direct_entries[u]
        q_chart = restrict(q, chart)
        assert add(
            multiply(product, q_chart),
            scale(multiply(q_chart, q_chart), direct_entries[u] / 2),
        ) == {}

    # Endpoint-order audit: A_02=E_10 has row 1 nonzero, but its transpose
    # has row 1 zero.  A_12=-E_00 has row 1 zero in both orientations.
    a02 = [[0, 0, 0], [1, 0, 0], [0, 0, 0]]
    a12 = [[-1, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert a02[1] == [1, 0, 0]
    assert [a02[row][1] for row in range(3)] == [0, 0, 0]
    assert a12[1] == [0, 0, 0]
    assert [a12[row][1] for row in range(3)] == [0, 0, 0]

    # No global S: block 02 forces S_2=0, while block 12 requires S_2=e_0.
    assert restrict(z, {0, 2}) == {}
    assert restrict(z, {1, 2}) == cell(1, 0, 2, 0)
    assert restrict(center, {0}) and restrict(center, {1})


def audit_diagonal_inactive_edge_guard():
    sites = (0, 1, 2, 3)
    q = add(
        cell(2, 0, 3, 0),
        cell(1, 1, 3, 1),
        cell(1, 2, 2, 2),
        cell(0, 0, 3, 1),
    )
    p = (
        atom(0, 0),
        atom(2, 1),
        atom(0, 2),
    )
    s = (
        atom(1, 0),
        add(atom(0, 1), atom(3, 1)),
        atom(3, 2),
    )
    assert rank([coefficient_row(row) for row in p]) == 3
    assert rank([coefficient_row(row) for row in s]) == 3

    q_divided_2 = scale(multiply(q, q), Fraction(1, 2))
    expected_q2 = multiply(cell(0, 0, 3, 1), cell(1, 2, 2, 2))
    assert q_divided_2 == expected_q2

    for color in range(3):
        diagonal = multiply(multiply(p[color], s[color]), q)
        assert diagonal == pure_target(sites, color)

    alpha = (1, 0, 0, 0)
    response = multiply(p[0], s[1])
    assert response == cell(0, 0, 3, 1)
    assert gauge(q, alpha) == response
    assert sum(alpha) == 1
    assert add(scale(q_divided_2, -1), multiply(response, q)) == {}

    # The three diagonal-carrying triangle edges are all inactive.
    for i, j in ((1, 2), (1, 3), (2, 3)):
        assert alpha[i] + alpha[j] == 0
    assert alpha[0] + alpha[3] == 1


def audit_dense_threshold():
    support = set(range(5))
    fan = set(range(7))
    for u in fan:
        for v in fan - {u}:
            assert len(support - {u, v}) >= 3


def main():
    audit_three_chart_holonomy()
    audit_diagonal_inactive_edge_guard()
    audit_dense_threshold()
    print(
        "PASS three_chart_physical_holonomy=1 "
        "normalized_diagonal_rows=3 inactive_edge_responses=1"
    )


if __name__ == "__main__":
    main()

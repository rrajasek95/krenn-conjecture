#!/usr/bin/env python3
"""Exact audit of the radial Segre-kernel and binary-cofactor boundary."""

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


def ordinary_power(poly, exponent):
    out = {(): Fraction(1)}
    for _ in range(exponent):
        out = multiply(out, poly)
    return out


def factorial(value):
    out = 1
    for factor in range(2, value + 1):
        out *= factor
    return out


def divided_power(poly, exponent):
    return scale(ordinary_power(poly, exponent), Fraction(1, factorial(exponent)))


def x(site, colour):
    return {((site, colour),): Fraction(1)}


def word(colours):
    out = {(): Fraction(1)}
    for site, colour in enumerate(colours):
        out = multiply(out, x(site, colour))
    return out


def coefficient(poly, coordinates):
    return poly.get(tuple(sorted(coordinates)), Fraction(0))


def form_vector(poly, site_count=6, colour_count=3):
    return [
        coefficient(poly, ((site, colour),))
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


def lambda_value(lam, x_vector, y_vector):
    return sum(
        Fraction(lam[2 * row + column]) * x_vector[row] * y_vector[column]
        for row in range(2)
        for column in range(2)
    )


def open_segre_kernel_point(lam):
    """Construct x,y in (Q*)^2 with x^T Lambda y=0, or return None for a spike."""
    lam = tuple(Fraction(entry) for entry in lam)
    support = sum(bool(entry) for entry in lam)
    if support <= 1:
        return None

    top = lam[:2]
    bottom = lam[2:]
    if not any(bottom):
        # Non-spikeness forces both entries in the top row to be nonzero.
        t = -top[0] / top[1]
        return (Fraction(1), Fraction(1)), (Fraction(1), t)
    if not any(top):
        # Non-spikeness forces both entries in the bottom row to be nonzero.
        t = -bottom[0] / bottom[1]
        return (Fraction(1), Fraction(1)), (Fraction(1), t)

    # Avoid the at most two roots of a(t) and b(t), then solve for s.
    for t_integer in range(1, 8):
        t = Fraction(t_integer)
        a_value = top[0] + top[1] * t
        b_value = bottom[0] + bottom[1] * t
        if a_value and b_value:
            s = -a_value / b_value
            if s:
                return (Fraction(1), s), (Fraction(1), t)
    raise RuntimeError("finite avoidance set unexpectedly exhausted")


def check_open_segre_dichotomy():
    for lam in product(range(-2, 3), repeat=4):
        if not any(lam):
            continue
        support = sum(bool(entry) for entry in lam)
        point = open_segre_kernel_point(lam)
        if support == 1:
            require(point is None, "coordinate spike acquired an open-Segre kernel point")
            continue
        require(point is not None, "non-spike missed the open Segre torus")
        x_vector, y_vector = point
        require(all(x_vector) and all(y_vector), "constructed Segre point left the torus")
        require(lambda_value(lam, x_vector, y_vector) == 0, "constructed point missed ker(lambda)")
        matrix = [
            x_vector[0] * y_vector[0],
            x_vector[0] * y_vector[1],
            x_vector[1] * y_vector[0],
            x_vector[1] * y_vector[1],
        ]
        require(all(matrix), "rank-one kernel matrix lost a complementary entry")
        require(matrix[0] * matrix[3] == matrix[1] * matrix[2], "Segre determinant is nonzero")

    # A diagonal spike has no active kernel matrix; an off-diagonal spike
    # has an active rank-two kernel matrix but no open-Segre point.
    diagonal_spike = (1, 0, 0, 0)
    off_diagonal_spike = (0, 1, 0, 0)
    active_rank_two = (1, 0, 0, 1)
    require(active_rank_two[0] and active_rank_two[3], "test matrix is not active")
    require(sum(diagonal_spike[i] * active_rank_two[i] for i in range(4)) != 0,
            "diagonal spike unexpectedly accepted the active matrix")
    require(sum(off_diagonal_spike[i] * active_rank_two[i] for i in range(4)) == 0,
            "off-diagonal spike lost its active rank-two direction")
    require(active_rank_two[0] * active_rank_two[3] != active_rank_two[1] * active_rank_two[2],
            "off-diagonal spike test direction accidentally became rank one")


def build_guard():
    a, b, c = 0, 1, 2
    q = add(
        multiply(x(1, b), x(2, b)),
        multiply(x(4, b), x(5, b)),
        multiply(x(0, c), x(1, c)),
        multiply(x(3, c), x(4, c)),
    )
    p = {a: x(1, a), b: x(0, b), c: x(5, c)}
    s = {a: x(4, a), b: x(3, b), c: x(2, c)}
    responses = {
        (row, column): multiply(p[row], s[column])
        for row in (a, b, c)
        for column in (a, b, c)
    }
    return a, b, c, q, p, s, responses


def check_guard():
    a, b, c, q, p, s, responses = build_guard()
    require(vector_rank([form_vector(p[label]) for label in (a, b, c)]) == 3,
            "p-star is not good")
    require(vector_rank([form_vector(s[label]) for label in (a, b, c)]) == 3,
            "s-star is not good")

    q2 = divided_power(q, 2)
    q3 = divided_power(q, 3)
    targets = {a: word((a,) * 6), b: word((b,) * 6), c: word((c,) * 6)}
    require(q3 == ZERO, "guard internal quadratic acquired a perfect matching")

    residual_rows = {}
    for row in (a, b, c):
        for column in (a, b, c):
            lhs = multiply(responses[(row, column)], q2)
            if (row, column) == (a, a):
                lhs = add(q3, lhs)
            rhs = targets[row] if row == column else ZERO
            residual_rows[(row, column)] = add(lhs, scale(rhs, -1))
    require(
        {index for index, residual in residual_rows.items() if residual}
        == {(a, a)},
        "guard no longer has exactly one failed physical row",
    )
    require(residual_rows[(a, a)] == scale(targets[a], -1),
            "exceptional-row residual is not -X_a")
    require(multiply(responses[(b, a)], q2) == ZERO,
            "left selected primitive row became nonzero")
    require(multiply(responses[(a, c)], q2) == ZERO,
            "right selected primitive row became nonzero")

    r = responses[(a, a)]
    carrier = add(q, scale(r, Fraction(1, 2)))
    unary_internal = add(q, r)
    p_sum = add(p[b], p[c])
    s_sum = add(s[b], s[c])
    response = multiply(p_sum, s_sum)

    require(multiply(p[b], multiply(s_sum, q2)) == targets[b],
            "first p-side common-cofactor response failed")
    require(multiply(p[c], multiply(s_sum, q2)) == targets[c],
            "second p-side common-cofactor response failed")
    require(multiply(s[b], multiply(p_sum, q2)) == targets[b],
            "first s-side common-cofactor response failed")
    require(multiply(s[c], multiply(p_sum, q2)) == targets[c],
            "second s-side common-cofactor response failed")
    require(multiply(response, q2) == add(targets[b], targets[c]),
            "binary rank-one response is wrong")

    for row in (a, b, c):
        for column in (a, b, c):
            left = multiply(responses[(row, column)], r)
            right = multiply(responses[(row, a)], responses[(a, column)])
            require(left == right, f"Segre square failed at {(row, column)}")

    for row in (b, c):
        for column in (b, c):
            require(multiply(multiply(responses[(row, column)], r), carrier) == ZERO,
                    f"complementary radial jet survived at {(row, column)}")
    require(multiply(multiply(response, r), carrier) == ZERO,
            "rank-one response missed the radial kernel")

    response2 = divided_power(response, 2)
    response3 = divided_power(response, 3)
    expected_response2 = scale(
        multiply(
            multiply(x(0, b), x(2, c)),
            multiply(x(3, b), x(5, c)),
        ),
        2,
    )
    higher_word = word((b, a, c, b, a, c))
    require(response2 == expected_response2, "wrong decomposable response square")
    require(multiply(response2, unary_internal) == scale(higher_word, 2),
            "nonzero second stationary coefficient changed")
    require(response3 == ZERO, "response cube should vanish on four star sites")
    require(divided_power(unary_internal, 3) == ZERO, "guard unexpectedly repaired the unary row")
    require(multiply(response, divided_power(unary_internal, 2)) == add(targets[b], targets[c]),
            "first normal coefficient no longer equals the binary target")

    for z_value in (Fraction(1), Fraction(2), Fraction(-3)):
        actual_error = add(
            divided_power(add(unary_internal, scale(response, z_value)), 3),
            scale(targets[a], -1),
            scale(targets[b], -z_value),
            scale(targets[c], -z_value),
        )
        expected_error = add(
            scale(targets[a], -1),
            scale(higher_word, 2 * z_value * z_value),
        )
        require(actual_error == expected_error, "rootless cap-error polynomial changed")
        require(actual_error != ZERO, "guard acquired a clean active point")

    # Deterministic mutations: deleting either pure-b internal edge breaks
    # the bb row, and changing the pure carrier coefficient breaks (25).
    bad_q = add(q, scale(multiply(x(1, b), x(2, b)), -1))
    require(multiply(responses[(b, b)], divided_power(bad_q, 2)) != targets[b],
            "deleted-edge mutation escaped the bb row audit")
    bad_unary = add(q, scale(r, 2))
    require(multiply(response2, bad_unary) != scale(higher_word, 2),
            "carrier-weight mutation escaped the higher-coefficient audit")


def main():
    check_open_segre_dichotomy()
    check_guard()
    print("scalar-unit radial Segre-kernel binary-cofactor boundary checks passed")


if __name__ == "__main__":
    main()

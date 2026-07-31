#!/usr/bin/env python3
"""Exact audits for the common-coloop diagonal-arm/resultant boundary."""

from __future__ import annotations

from fractions import Fraction as F


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


N = 6
SITES = tuple(range(N))
COLORS = tuple(range(3))
EMPTY = (None,) * N


def clean(terms):
    return {word: value for word, value in terms.items() if value}


def zero():
    return {}


def unit():
    return {EMPTY: F(1)}


def add(*elements):
    out = {}
    for element in elements:
        for word, value in element.items():
            out[word] = out.get(word, F(0)) + value
    return clean(out)


def scale(element, scalar):
    scalar = F(scalar)
    return clean({word: scalar * value for word, value in element.items()})


def mul(left, right):
    out = {}
    for left_word, left_value in left.items():
        for right_word, right_value in right.items():
            if any(
                left_word[site] is not None and right_word[site] is not None
                for site in SITES
            ):
                continue
            word = tuple(
                right_word[site]
                if right_word[site] is not None
                else left_word[site]
                for site in SITES
            )
            out[word] = out.get(word, F(0)) + left_value * right_value
    return clean(out)


def divided_power(element, exponent):
    result = unit()
    for divisor in range(1, exponent + 1):
        result = scale(mul(result, element), F(1, divisor))
    return result


def one_site(site, color, value=1):
    word = [None] * N
    word[site] = color
    return {tuple(word): F(value)} if value else zero()


def cell(left, right, color, value=1):
    return scale(mul(one_site(left, color), one_site(right, color)), value)


def word(text):
    require(len(text) == N, "word length mismatch")
    return tuple(None if symbol == "." else int(symbol) for symbol in text)


def matrix_rank(rows):
    matrix = [[F(value) for value in row] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * normalized
                for value, normalized in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def linear_coordinates(element, exclude_site=None):
    coordinates = []
    for site in SITES:
        if site == exclude_site:
            continue
        for color in COLORS:
            coordinates.append(element.get(next(iter(one_site(site, color))), F(0)))
    return coordinates


def guard_audits():
    x, one, two, three, four, five = SITES
    q = add(
        cell(one, two, 0),
        cell(four, five, 0),
        cell(two, five, 1),
        cell(three, four, 1),
        cell(x, five, 2),
        cell(one, three, 2),
    )
    p = (
        one_site(x, 0),
        one_site(one, 1),
        add(one_site(one, 2), one_site(two, 2)),
    )
    s = (
        one_site(three, 0),
        one_site(x, 1),
        add(one_site(three, 2), one_site(four, 2)),
    )

    q2 = divided_power(q, 2)
    expected_rows = {
        (0, 0): {word("000000"): F(1)},
        (0, 1): {},
        (0, 2): {word("000200"): F(1), word("021221"): F(1)},
        (1, 0): {},
        (1, 1): {word("111111"): F(1)},
        (1, 2): {},
        (2, 0): {},
        (2, 1): {word("121111"): F(1), word("122200"): F(1)},
        (2, 2): {word("222222"): F(1)},
    }
    for i in COLORS:
        for j in COLORS:
            row = mul(mul(p[i], s[j]), q2)
            require(row == expected_rows[(i, j)], f"pair row {(i, j)} mismatch")

    require(divided_power(q, 3) == {word("200112"): F(1)}, "q^[3] mismatch")

    p_rows = [linear_coordinates(element) for element in p]
    s_rows = [linear_coordinates(element) for element in s]
    p_off = [linear_coordinates(element, exclude_site=x) for element in p]
    s_off = [linear_coordinates(element, exclude_site=x) for element in s]
    require(matrix_rank(p_rows) == matrix_rank(s_rows) == 3, "endpoint injectivity failed")
    require(matrix_rank(p_off) == matrix_rank(s_off) == 2, "off-x rank failed")
    require(all(value == 0 for value in p_off[0]), "left kernel is not e_0")
    require(all(value == 0 for value in s_off[1]), "right kernel is not e_1")

    q0 = add(
        cell(one, two, 0),
        cell(four, five, 0),
        cell(two, five, 1),
        cell(three, four, 1),
        cell(one, three, 2),
    )
    rho2 = one_site(five, 2)
    bar_p = p[2]
    bar_s = s[2]
    bar_r = mul(bar_p, bar_s)
    a_power = divided_power(q0, 2)
    y2 = {word(".22222"): F(1)}

    require(mul(mul(mul(rho2, bar_r), q0), unit()) == y2, "curvature anchor failed")
    require(mul(rho2, divided_power(bar_r, 2)) == scale(y2, 2), "second polar failed")
    require(
        mul(bar_s, a_power)
        == {word(".00200"): F(1), word(".21221"): F(1)},
        "right arm A-image mismatch",
    )
    require(
        mul(bar_p, a_power)
        == {word(".21111"): F(1), word(".22200"): F(1)},
        "left arm A-image mismatch",
    )
    require(mul(rho2, a_power) == {word(".00112"): F(1)}, "rho A ledger mismatch")


def affine_resultant_audits():
    # Same-scalar h=3 certificate: dependent rows have zero determinant.
    u1, v1 = F(2), F(-6)
    u2, v2 = F(-1), F(3)
    require(u1 * v2 - u2 * v1 == 0, "same-line resultant should vanish")
    candidate = -v1 / u1
    require(candidate == 3 and u2 * candidate + v2 == 0, "common candidate mismatch")

    # Affine chart transition z_nu=a_nu*tau+b_nu.
    a1, b1, u1, v1 = map(F, (2, 1, 3, -9))
    a2, b2, u2, v2 = map(F, (-1, 4, 5, -15))
    slope1, constant1 = a1 * u1, b1 * u1 + v1
    slope2, constant2 = a2 * u2, b2 * u2 + v2
    require(slope1 * constant2 - slope2 * constant1 == 0, "affine resultant should vanish")
    tau = -constant1 / slope1
    require(slope2 * tau + constant2 == 0, "affine common root mismatch")

    # A genuinely transverse coefficient row excludes a common line root.
    require(F(2) * F(7) - F(3) * F(5) != 0, "transverse determinant vanished")


def trim(polynomial):
    values = [F(value) for value in polynomial]
    while len(values) > 1 and not values[-1]:
        values.pop()
    return values


def determinant(matrix):
    matrix = [[F(value) for value in row] for row in matrix]
    size = len(matrix)
    result = F(1)
    for column in range(size):
        pivot = next((row for row in range(column, size) if matrix[row][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            result = -result
        pivot_value = matrix[column][column]
        result *= pivot_value
        for row in range(column + 1, size):
            if not matrix[row][column]:
                continue
            factor = matrix[row][column] / pivot_value
            for entry in range(column, size):
                matrix[row][entry] -= factor * matrix[column][entry]
    return result


def resultant(left, right):
    left = trim(left)
    right = trim(right)
    left_degree = len(left) - 1
    right_degree = len(right) - 1
    require(left_degree >= 1 and right_degree >= 1, "resultant audit needs nonconstant polynomials")
    left_desc = list(reversed(left))
    right_desc = list(reversed(right))
    size = left_degree + right_degree
    rows = []
    for shift in range(right_degree):
        rows.append([F(0)] * shift + left_desc + [F(0)] * (size - shift - len(left_desc)))
    for shift in range(left_degree):
        rows.append([F(0)] * shift + right_desc + [F(0)] * (size - shift - len(right_desc)))
    return determinant(rows)


def uniform_resultant_audits():
    # Degrees h-2 for 3 <= h <= 8.  A shared factor gives zero resultant;
    # shifting its root gives a nonzero resultant.
    for h in range(3, 9):
        degree = h - 2
        shared_left = [F(-2), F(1)] + [F(0)] * (degree - 1)
        shared_right = [F(6), F(-5), F(1)] if degree >= 2 else [F(-4), F(2)]
        if degree > 2:
            shared_right += [F(0)] * (degree - 2)
        require(resultant(shared_left, shared_right) == 0, f"shared-root resultant failed at h={h}")

        left = [F(-2), F(1)]
        right = [F(-3), F(1)]
        if degree > 1:
            # Preserve distinct roots while reaching the allowed degree.
            for root in range(4, degree + 3):
                new = [F(0)] * (len(left) + 1)
                for index, value in enumerate(left):
                    new[index] -= root * value
                    new[index + 1] += value
                left = new
            for root in range(degree + 4, 2 * degree + 3):
                new = [F(0)] * (len(right) + 1)
                for index, value in enumerate(right):
                    new[index] -= root * value
                    new[index + 1] += value
                right = new
        require(resultant(left, right) != 0, f"separated-root resultant failed at h={h}")


def main():
    guard_audits()
    affine_resultant_audits()
    uniform_resultant_audits()
    print("common-coloop diagonal-arm/resultant boundary: PASS")
    print("literal diagonal-complete 7/9 guard and nonzero second polar: PASS")
    print("same-line h=3 and uniform h=3..8 resultant audits: PASS")


if __name__ == "__main__":
    main()

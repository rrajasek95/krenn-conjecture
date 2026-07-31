#!/usr/bin/env python3
"""Exact checks for the off-target scalar-unit radial quotient normal form."""

from fractions import Fraction
from itertools import product


ZERO = {}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def clean(poly):
    return {m: c for m, c in poly.items() if c}


def add(*polys):
    out = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            out[monomial] = out.get(monomial, Fraction(0)) + coefficient
    return clean(out)


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return clean({m: scalar * c for m, c in poly.items()})


def multiply(left, right):
    out = {}
    for lm, lc in left.items():
        left_sites = {site for site, _ in lm}
        for rm, rc in right.items():
            if left_sites.intersection(site for site, _ in rm):
                continue
            monomial = tuple(sorted(lm + rm))
            out[monomial] = out.get(monomial, Fraction(0)) + lc * rc
    return clean(out)


def ordinary_power(poly, exponent):
    out = {(): Fraction(1)}
    for _ in range(exponent):
        out = multiply(out, poly)
    return out


def factorial(n):
    value = 1
    for k in range(2, n + 1):
        value *= k
    return value


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


def vector_rank(vectors):
    if not vectors:
        return 0
    width = len(vectors[0])
    matrix = [[Fraction(entry) for entry in row] for row in vectors]
    rank = 0
    for column in range(width):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][column]), None)
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
                matrix[row][j] - factor * matrix[rank][j] for j in range(width)
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def nullspace_one_row(row):
    row = [Fraction(value) for value in row]
    pivot = next(i for i, value in enumerate(row) if value)
    basis = []
    for free in range(4):
        if free == pivot:
            continue
        vector = [Fraction(0)] * 4
        vector[free] = Fraction(1)
        vector[pivot] = -row[free] / row[pivot]
        basis.append(vector)
    return basis


def check_target_leakage():
    # Column order is bb, bc, cb, cc.
    for lam in product((-1, 0, 1), repeat=4):
        if not any(lam):
            continue
        kernel = nullspace_one_row(lam)
        require(len(kernel) == 3, "radial functional did not have a 3-space kernel")
        require(
            all(sum(Fraction(lam[i]) * vector[i] for i in range(4)) == 0 for vector in kernel),
            "constructed vector missed the radial kernel",
        )
        diagonal_image = [[vector[0], vector[3]] for vector in kernel]
        actual_rank = vector_rank(diagonal_image)
        expected_rank = 2 if (lam[1] or lam[2]) else 1
        require(actual_rank == expected_rank, "wrong target-leakage rank")

        active_found = False
        for entries in product(range(-2, 3), repeat=4):
            if entries[0] and entries[3] and sum(lam[i] * entries[i] for i in range(4)) == 0:
                active_found = True
                break
        single_diagonal = not lam[1] and not lam[2] and ((bool(lam[0])) != (bool(lam[3])))
        require(active_found == (not single_diagonal), "wrong active-kernel fork")


def local_vector(poly, site, colour_count=3):
    return [coefficient(poly, ((site, colour),)) for colour in range(colour_count)]


def check_pure_factor_kernel_guard():
    a, b = 0, 1
    p = add(x(0, a), x(1, b))
    s = add(x(0, a), x(1, a), scale(x(1, b), -1))
    carrier = {(): Fraction(1)}
    for site in range(2, 6):
        carrier = multiply(carrier, x(site, a))
    target = word((a,) * 6)
    require(multiply(multiply(p, s), carrier) == target, "pure-factor guard failed")

    p_pure = [site for site in range(6) if local_vector(p, site) == [1, 0, 0]]
    s_pure = [site for site in range(6) if local_vector(s, site) == [1, 0, 0]]
    require(p_pure == [0] and s_pure == [0], "guard unexpectedly split its pure sites")

    target_without_zero = {(): Fraction(1)}
    for site in range(1, 6):
        target_without_zero = multiply(target_without_zero, x(site, a))
    kernel_term = add(multiply(s, carrier), scale(target_without_zero, -1))
    require(kernel_term != ZERO, "pure-factor kernel ambiguity vanished")
    require(multiply(p, kernel_term) == ZERO, "kernel ambiguity was not killed by p")


def check_primitive_square_guard():
    q = add(
        multiply(x(0, 0), x(1, 0)),
        multiply(x(2, 0), x(3, 0)),
        multiply(x(4, 0), x(5, 0)),
    )
    left = multiply(add(x(0, 0), x(2, 0)), add(x(1, 0), scale(x(3, 0), -1)))
    right = multiply(add(x(0, 0), x(4, 0)), add(x(1, 0), scale(x(5, 0), -1)))
    q2 = divided_power(q, 2)
    q3 = divided_power(q, 3)
    require(multiply(left, q2) == ZERO, "left primitive response was not q^[2]-null")
    require(multiply(right, q2) == ZERO, "right primitive response was not q^[2]-null")
    require(multiply(multiply(left, right), q) == scale(q3, -1), "primitive square missed q^[3]")


def form_vector(poly, site_count=6, colour_count=3):
    return [
        coefficient(poly, ((site, colour),))
        for site in range(site_count)
        for colour in range(colour_count)
    ]


def check_physical_radial_guard():
    a, b, c = 0, 1, 2
    q = add(
        multiply(x(0, a), x(3, b)),
        multiply(x(1, b), x(5, a)),
        multiply(x(2, a), x(4, a)),
        multiply(x(3, b), x(4, a)),
        multiply(x(3, a), x(5, a)),
        multiply(x(4, a), x(5, a)),
    )
    p = {
        a: x(0, a),
        b: x(1, b),
        c: x(0, c),
    }
    s = {
        a: add(x(1, a), scale(x(2, a), -1)),
        b: x(0, c),
        c: x(3, b),
    }
    require(vector_rank([form_vector(p[i]) for i in (a, b, c)]) == 3, "p-star is not good")
    require(vector_rank([form_vector(s[i]) for i in (a, b, c)]) == 3, "s-star is not good")

    responses = {(i, j): multiply(p[i], s[j]) for i in (a, b, c) for j in (a, b, c)}
    r = responses[(a, a)]
    q2 = divided_power(q, 2)
    q3 = divided_power(q, 3)
    target_a = word((a,) * 6)
    radial_word = word((a, b, a, b, a, a))
    require(q3 == radial_word, "q^[3] is not the claimed off-target word")
    require(q3 not in (target_a, word((b,) * 6), word((c,) * 6)), "radial word became a target")
    require(multiply(r, q2) == add(target_a, scale(radial_word, -1)), "exceptional response is wrong")
    require(divided_power(r, 2) == ZERO, "r^[2] should vanish by site collision")

    g = add(q, r)
    require(divided_power(g, 3) == target_a, "unary cap is not clean")
    carrier = add(q, scale(r, Fraction(1, 2)))
    theta = multiply(r, carrier)
    require(theta == multiply(r, q), "divided-difference carrier normalization is wrong")

    expected_lambda = {(b, b): 0, (b, c): -1, (c, b): 0, (c, c): 0}
    for index, lam in expected_lambda.items():
        jet = multiply(responses[index], theta)
        require(jet == scale(radial_word, lam), f"wrong radial jet at {index}")
    require(multiply(responses[(b, c)], q2) == ZERO, "chosen old off-diagonal row is not zero")
    require(multiply(responses[(b, a)], q2) == scale(radial_word, -1), "left primitive-row guard changed")
    require(multiply(responses[(a, c)], q2) == radial_word, "right primitive-row guard changed")

    segre_left = multiply(responses[(b, c)], r)
    segre_right = multiply(responses[(b, a)], responses[(a, c)])
    require(segre_left == segre_right, "literal Segre square failed")

    localized = (
        coefficient(p[b], ((1, b),))
        * coefficient(s[a], ((2, a),))
        * coefficient(p[a], ((0, a),))
        * coefficient(s[c], ((3, b),))
        * coefficient(carrier, ((4, a), (5, a)))
    )
    require(localized == -1, "four-site carrier localization has wrong coefficient")

    pure_carrier = add(q2, scale(multiply(responses[(b, c)], carrier), -1))
    require(multiply(r, pure_carrier) == target_a, "radial pure-factor identity failed")

    targets = {a: target_a, b: word((b,) * 6), c: word((c,) * 6)}
    exact_rows = set()
    for i in (a, b, c):
        for j in (a, b, c):
            lhs = multiply(responses[(i, j)], q2)
            if (i, j) == (a, a):
                lhs = add(q3, lhs)
            rhs = targets[i] if i == j else ZERO
            if lhs == rhs:
                exact_rows.add((i, j))
    require(
        exact_rows == {(a, a), (a, b), (b, c), (c, b)},
        "physical guard's full-nine boundary changed",
    )

    # Mutating the radial sign must break both the jet and pure-factor normalization.
    bad_carrier = add(q2, multiply(responses[(b, c)], carrier))
    require(multiply(r, bad_carrier) != target_a, "radial-sign mutation escaped detection")


def main():
    check_target_leakage()
    check_pure_factor_kernel_guard()
    check_primitive_square_guard()
    check_physical_radial_guard()
    print("off-target scalar-unit radial quotient checks passed")


if __name__ == "__main__":
    main()

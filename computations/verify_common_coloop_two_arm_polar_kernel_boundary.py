#!/usr/bin/env python3
"""Audit a literal two-arm polar-kernel common-coloop subcase.

The sparse site-square-zero algebra below reconstructs one five-site
quadratic q0 and its consecutive power A=q0^[2].  After a sixth exposed
site is added, it verifies two raw literal response arms a0,a1 with

    a_i A = X_i,        a_i D(z) = 0  (i=0,1),

for the same polar action D(z)=z*bar_r*q0+bar_r^[2].  If both arms survive
the fixed-scalar response quotient, their two nonmissing A-coordinate
rows are independent on ker D, which excludes both A-through-D
interpolation covectors.  The checker also audits the sharp abstract
linear-algebra boundary: consistency, not a forced diagonal, is all that
remains on the span of these arms.

Standard library only; live under -O and -I -S.  Research evidence only.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


N = 6
SITES = tuple(range(N))
COLORS = tuple(range(3))
EXPOSED = 5
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
        for monomial, coefficient in element.items():
            out[monomial] = out.get(monomial, F(0)) + coefficient
    return clean(out)


def scale(element, scalar):
    scalar = F(scalar)
    return clean({monomial: scalar * value for monomial, value in element.items()})


def mul(left, right):
    out = {}
    for left_word, left_value in left.items():
        for right_word, right_value in right.items():
            if any(
                left_word[site] is not None and right_word[site] is not None
                for site in SITES
            ):
                continue
            monomial = tuple(
                right_word[site]
                if right_word[site] is not None
                else left_word[site]
                for site in SITES
            )
            out[monomial] = out.get(monomial, F(0)) + left_value * right_value
    return clean(out)


def divided_power(element, exponent):
    result = unit()
    for divisor in range(1, exponent + 1):
        result = scale(mul(result, element), F(1, divisor))
    return result


def one_site(site, color, value=1):
    monomial = [None] * N
    monomial[site] = color
    return {tuple(monomial): F(value)} if value else zero()


def cell(left, right, color, value=1):
    return scale(mul(one_site(left, color), one_site(right, color)), value)


def word(text):
    require(len(text) == N, "word length mismatch")
    return tuple(None if symbol == "." else int(symbol) for symbol in text)


def coefficient(element, monomial):
    return element.get(monomial, F(0))


def determinant_2_by_2(rows):
    require(len(rows) == 2 and all(len(row) == 2 for row in rows),
            "the arm-coordinate ledger is not 2 by 2")
    return rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]


def matrix_rank(rows):
    work = [[F(value) for value in row] for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        selected = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [entry / pivot for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * normalized
                for entry, normalized in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def linear_coordinates(element, omit_exposed=False):
    coordinates = []
    for site in SITES:
        if omit_exposed and site == EXPOSED:
            continue
        for color in COLORS:
            coordinates.append(coefficient(element, next(iter(one_site(site, color)))))
    return tuple(coordinates)


def tensor_digest(elements):
    rows = []
    for name, element in elements:
        encoded_terms = []
        for monomial, value in sorted(
            element.items(), key=lambda item: tuple(-1 if x is None else x for x in item[0])
        ):
            encoded_word = "".join("." if x is None else str(x) for x in monomial)
            encoded_terms.append(f"{encoded_word}:{value.numerator}/{value.denominator}")
        rows.append(f"{name}=" + ",".join(encoded_terms))
    return sha256("\n".join(rows).encode()).hexdigest()


def literal_two_arm_audits():
    zero_site, one, two, three, four, exposed = SITES

    q0 = add(
        cell(zero_site, one, 0),
        cell(two, three, 0),
        cell(zero_site, two, 1),
        cell(one, four, 1),
        cell(three, four, 2),
    )
    a_power = divided_power(q0, 2)

    y = tuple({word(color * 5 + "."): F(1)} for color in "012")
    lift0 = one_site(four, 0)
    lift1 = one_site(three, 1)
    require(mul(lift0, a_power) == y[0], "the color-0 A-lift changed")
    require(mul(lift1, a_power) == y[1], "the color-1 A-lift changed")

    for site in range(EXPOSED):
        for color in COLORS:
            require(coefficient(mul(one_site(site, color), a_power), next(iter(y[2]))) == 0,
                    f"an unexpected color-2 A-lift appeared at {(site, color)}")

    # These endpoint forms make the two known A-lifts the literal
    # singleton arms.  Swapping the color-2 off-site endpoints relative
    # to the older flat-overlap guard kills all three nonmissing curvature
    # cells while retaining the 22 corner.
    bar_p = (zero(), lift1, one_site(two, 2))
    bar_s = (lift0, zero(), one_site(one, 2))
    local_p = (one_site(exposed, 0), zero(), zero())
    local_s = (zero(), one_site(exposed, 1), zero())
    endpoint_p = tuple(add(bar_p[label], local_p[label]) for label in COLORS)
    endpoint_s = tuple(add(bar_s[label], local_s[label]) for label in COLORS)
    require(matrix_rank(tuple(linear_coordinates(row) for row in endpoint_p)) == 3,
            "the left endpoint map lost injectivity")
    require(matrix_rank(tuple(linear_coordinates(row) for row in endpoint_s)) == 3,
            "the right endpoint map lost injectivity")
    require(matrix_rank(tuple(linear_coordinates(row, True) for row in endpoint_p)) == 2,
            "the left off-site restriction lost rank two")
    require(matrix_rank(tuple(linear_coordinates(row, True) for row in endpoint_s)) == 2,
            "the right off-site restriction lost rank two")

    bar_p2 = bar_p[2]
    bar_s2 = bar_s[2]
    bar_r = mul(bar_p2, bar_s2)
    second_polar = divided_power(bar_r, 2)
    first_polar = mul(bar_r, q0)
    require(second_polar == zero(), "bar_r^[2] should vanish")
    require(first_polar == {word(".2222."): F(1)}, "bar_r*q0 changed")

    arm0 = mul(local_p[0], bar_s[0])
    arm1 = mul(bar_p[1], local_s[1])
    x = tuple({word(color * 6): F(1)} for color in "012")
    arm_a_images = (mul(arm0, a_power), mul(arm1, a_power))
    require(arm_a_images == (x[0], x[1]), "literal arm A-images changed")

    # D(z)=z*first_polar+second_polar.  Checking both coefficients proves
    # arm_i D(z)=0 identically, without choosing or dividing by a scalar.
    arm_d_coefficients = tuple(
        (mul(arm, second_polar), mul(arm, first_polar))
        for arm in (arm0, arm1)
    )
    require(arm_d_coefficients == ((zero(), zero()), (zero(), zero())),
            "a literal arm escaped the polar kernel")

    coordinates = tuple(
        tuple(coefficient(image, next(iter(x[label]))) for label in (0, 1))
        for image in arm_a_images
    )
    require(coordinates == ((F(1), F(0)), (F(0), F(1))),
            "the two nonmissing A-coordinate rows changed")
    require(determinant_2_by_2(coordinates) == 1,
            "the literal arm A-coordinate determinant vanished")

    # The same packet retains the sole missing curvature corner.  This is
    # a source-provenant A/D guard, not a claim that all nine physical rows
    # or a compatible affine residual have been supplied.
    rho = mul(one_site(exposed, 2), one_site(zero_site, 2))
    curvature = {
        (left, right): mul(mul(mul(rho, bar_p[left]), bar_s[right]), q0)
        for left in (1, 2)
        for right in (0, 2)
    }
    require(curvature == {
        (1, 0): zero(),
        (1, 2): zero(),
        (2, 0): zero(),
        (2, 2): x[2],
    }, "the singleton curvature rectangle is not the sole 22 corner")
    require(mul(rho, first_polar) == x[2], "the sole curvature corner changed")

    return (
        ("q0", q0),
        ("A", a_power),
        ("p0", endpoint_p[0]),
        ("p1", endpoint_p[1]),
        ("p2", endpoint_p[2]),
        ("s0", endpoint_s[0]),
        ("s1", endpoint_s[1]),
        ("s2", endpoint_s[2]),
        ("bar_r", bar_r),
        ("bar_r_q0", first_polar),
        ("arm0_A", arm_a_images[0]),
        ("arm1_A", arm_a_images[1]),
        ("arm0_D_constant", arm_d_coefficients[0][0]),
        ("arm0_D_linear", arm_d_coefficients[0][1]),
        ("arm1_D_constant", arm_d_coefficients[1][0]),
        ("arm1_D_linear", arm_d_coefficients[1][1]),
        ("curvature10", curvature[(1, 0)]),
        ("curvature12", curvature[(1, 2)]),
        ("curvature20", curvature[(2, 0)]),
        ("curvature22", curvature[(2, 2)]),
        ("corner", mul(rho, first_polar)),
    )


def quotient_boundary_audits():
    # On R=span(a0,a1), the polar matrix is zero and the two nonmissing
    # anchor coordinates form the identity.  Every consistent fibre has
    # both directions in its kernel, so neither coordinate can be forced.
    polar = ((F(0), F(0)), (F(0), F(0)))
    anchor = ((F(1), F(0)), (F(0), F(1)))
    for direction in ((F(1), F(0)), (F(0), F(1))):
        require(tuple(sum(row[j] * direction[j] for j in range(2)) for row in polar)
                == (F(0), F(0)), "an arm left the abstract polar kernel")
    require(determinant_2_by_2(anchor) == 1, "abstract anchor determinant vanished")

    # Applying a hypothetical Lambda D=partial_i to arm i would give
    # 0=1.  This direct evaluation checks both labelled interpolation
    # systems independently.
    for label, arm in enumerate(((F(1), F(0)), (F(0), F(1)))):
        polar_value = tuple(
            sum(row[j] * arm[j] for j in range(2)) for row in polar
        )
        anchor_value = sum(anchor[label][j] * arm[j] for j in range(2))
        require(polar_value == (F(0), F(0)) and anchor_value == 1,
                f"interpolation contradiction failed for label {label}")

    # Sharp consistency boundary on this two-arm span: im(D)={0}.  A zero
    # residual is consistent, while any nonzero residual has an obvious
    # cokernel detector.  The nonzero vector here is only a quotient-level
    # sharp guard; it is not asserted to be the affine residual of q0.
    residual_zero = (F(0), F(0))
    residual_nonzero = (F(0), F(1))
    require(residual_zero == (F(0), F(0)), "zero residual changed")
    detector = (F(0), F(1))
    require(all(sum(detector[i] * polar[i][j] for i in range(2)) == 0 for j in range(2)),
            "cokernel detector does not annihilate the polar image")
    require(sum(detector[i] * residual_nonzero[i] for i in range(2)) == 1,
            "cokernel detector misses the sharp residual")


def main():
    tensors = literal_two_arm_audits()
    quotient_boundary_audits()
    digest = tensor_digest(tensors)
    print("literal A/D tensor ledger sha256", digest)
    print("two literal polar-kernel arms: verified")
    print("both nonmissing interpolation covectors: excluded")
    print("two-arm-span cokernel boundary: verified")


if __name__ == "__main__":
    main()

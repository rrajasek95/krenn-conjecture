#!/usr/bin/env python3
"""Exact 3x3 permanent-null no-go for reciprocal coordinate-pair descent."""

from collections import defaultdict
from fractions import Fraction as F


VARIABLES = ("c01", "c10", "c02", "c20", "c12", "c21")
ZERO = (0,) * len(VARIABLES)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def constant(value):
    return {} if not value else {ZERO: F(value)}


def variable(name):
    exponent = [0] * len(VARIABLES)
    exponent[VARIABLES.index(name)] = 1
    return {tuple(exponent): F(1)}


def add(*terms):
    answer = defaultdict(F)
    for scale, polynomial in terms:
        for exponent, coefficient in polynomial.items():
            answer[exponent] += F(scale) * coefficient
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def multiply(left, right):
    answer = defaultdict(F)
    for a, x in left.items():
        for b, y in right.items():
            answer[tuple(u + v for u, v in zip(a, b, strict=True))] += x * y
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def scale(value, polynomial):
    return {exponent: F(value) * coefficient for exponent, coefficient in polynomial.items()}


def permanent2(matrix, rows, columns):
    i, k = rows
    j, l = columns
    return matrix[i][j] * matrix[k][l] + matrix[i][l] * matrix[k][j]


def main():
    variables = {name: variable(name) for name in VARIABLES}
    one = constant(1)
    c01, c10 = variables["c01"], variables["c10"]
    c02, c20 = variables["c02"], variables["c20"]
    c12, c21 = variables["c12"], variables["c21"]

    # Principal permanent f01 and two overlapping mixed permanents g1,g2.
    # They are three of the equations forced by universal quadratic
    # cancellation of z(C)^[2].
    f01 = add((1, one), (1, multiply(c01, c10)))
    g1 = add((1, c12), (1, multiply(c02, c10)))
    g2 = add((1, multiply(c01, c12)), (1, c02))

    # Integral ideal certificate:
    #   g2 - c01*g1 + c02*f01 = 2*c02.
    certificate = add(
        (1, g2),
        (-1, multiply(c01, g1)),
        (1, multiply(c02, f01)),
    )
    require(certificate == scale(2, c02), "permanent-null ideal certificate changed")

    # Since diagonal 1 forces c02*c20=-1, c02 is a unit on every candidate
    # chart.  Over characteristic zero the displayed certificate makes the
    # saturated permanent-null ideal the unit ideal.
    f02 = add((1, one), (1, multiply(c02, c20)))
    require(f02, "principal 02 permanent vanished identically")

    # The sign-normalized matrix kills all three principal 2x2 permanents but
    # exhibits the smallest surviving mixed permanent, exactly 2.
    candidate = (
        (F(1), F(1), F(1)),
        (F(-1), F(1), F(1)),
        (F(-1), F(-1), F(1)),
    )
    principal = tuple(
        permanent2(candidate, pair, pair)
        for pair in ((0, 1), (0, 2), (1, 2))
    )
    survivor = permanent2(candidate, (0, 1), (1, 2))
    require(principal == (F(0), F(0), F(0)), "principal permanent normalization changed")
    require(survivor == 2, "mixed permanent survivor changed")

    # Pair-packet linear response.  For a reciprocal off-diagonal block
    # d=-E_10, lambda*c10=1; for a diagonal block d=E_00.  In both cases the
    # candidate diagonal entries reproduce X0+X1+X2 and the selected direct
    # entry cancels the original q^[h] coefficient.  Quadratic insertion is
    # nevertheless nonzero by `survivor`.
    offdiagonal_lambda = F(-1)
    diagonal_lambda = F(1)
    require(offdiagonal_lambda * candidate[1][0] == 1, "offdiagonal q-power cancellation changed")
    require(diagonal_lambda * candidate[0][0] == 1, "diagonal q-power cancellation changed")

    # In contrast, the two-colour completion used by adjacent-cubic descent
    # is possible: its sole 2x2 permanent vanishes.
    two_colour = ((F(1), F(1)), (F(-1), F(1)))
    require(permanent2(two_colour, (0, 1), (0, 1)) == 0, "2x2 completion changed")

    print("reciprocal coordinate-pair permanent-null completion: PASS")
    print(f"integral certificate g2-c01*g1+c02*f01={certificate}")
    print("saturation: f01=g1=g2=0 and c02!=0 force 2=0")
    print(f"principal-normalized candidate={candidate}")
    print(f"principal permanents={principal}; smallest mixed survivor={survivor}")
    print("linear q-power cancellation works for d=-E10 and d=E00, but quadratic port insertion survives")
    print(f"two-colour permanent-null completion={two_colour}")


if __name__ == "__main__":
    main()

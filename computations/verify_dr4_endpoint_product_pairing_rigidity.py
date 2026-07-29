#!/usr/bin/env python3
"""Exact audit of the product-pairing endpoint exception in DR4.

The generic endpoint-span calculation can lose one rank when, after a
permutation and scaling, the anchors are (1,a,b,ab).  A first toric
compatibility equation reduces the remaining case to

    H=(a+1)^2 (b+1)^2 - 16ab = 0.

This script works in Q(a)[b]/(H), constructs the sixteen endpoint
coefficient rows, and uses homogeneous cofactor vectors for two row charts.
The gcd of the norms of their toric binomials is supported only at a=-1,
which is an excluded opposite-anchor specialization.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


A = sp.symbols("a")
BASE = sp.QQ.frac_field(A)
A_BASE = BASE.convert(A)

# On H=0, b satisfies b^2+C_REL*b+1=0.
C_REL = BASE.convert(2 * (A**2 - 6 * A + 1) / (A + 1) ** 2)


class Quad:
    """An element r+s*b of Q(a)[b]/(b^2+C_REL*b+1)."""

    __slots__ = ("r", "s")

    def __init__(self, r=0, s=0):
        self.r = BASE.convert(r)
        self.s = BASE.convert(s)

    def __add__(self, other):
        other = as_quad(other)
        return Quad(self.r + other.r, self.s + other.s)

    __radd__ = __add__

    def __neg__(self):
        return Quad(-self.r, -self.s)

    def __sub__(self, other):
        return self + (-as_quad(other))

    def __rsub__(self, other):
        return as_quad(other) - self

    def __mul__(self, other):
        other = as_quad(other)
        # b^2=-C_REL*b-1.
        return Quad(
            self.r * other.r - self.s * other.s,
            self.r * other.s
            + self.s * other.r
            - C_REL * self.s * other.s,
        )

    __rmul__ = __mul__

    def inverse(self):
        # The conjugate root is b'=-C_REL-b=1/b.
        norm = self.r**2 - C_REL * self.r * self.s + self.s**2
        if not norm:
            raise ZeroDivisionError
        return Quad((self.r - C_REL * self.s) / norm, -self.s / norm)

    def __truediv__(self, other):
        return self * as_quad(other).inverse()

    def __rtruediv__(self, other):
        return as_quad(other) * self.inverse()

    def __pow__(self, exponent: int):
        if exponent < 0:
            return self.inverse() ** (-exponent)
        answer = Quad(1)
        base = self
        while exponent:
            if exponent & 1:
                answer *= base
            base *= base
            exponent //= 2
        return answer

    def is_zero(self) -> bool:
        return not self.r and not self.s

    def norm(self):
        return self.r**2 - C_REL * self.r * self.s + self.s**2


def as_quad(value) -> Quad:
    return value if isinstance(value, Quad) else Quad(value)


SUBSETS = tuple(
    subset
    for degree in range(1, 5)
    for subset in combinations(range(4), degree)
)


def endpoint_rows() -> list[list[Quad]]:
    """Return E_i^+, U_i E_i^+, E_i^-, U_i E_i^- for i=0,...,3."""
    b = Quad(0, 1)
    anchors = (Quad(1), Quad(A_BASE), b, Quad(0, A_BASE))
    rows: list[list[Quad]] = []

    for i, t_i in enumerate(anchors):
        complement = tuple(j for j in range(4) if j != i)
        for sign in (1, -1):
            diagonal: dict[int, Quad] = {}
            for j in complement:
                derivative_diagonal = sum(
                    (
                        1 / (anchors[j] - anchors[k])
                        for k in complement
                        if k != j
                    ),
                    Quad(),
                )
                if sign == 1:
                    shift = -2 / (anchors[j] + t_i)
                else:
                    shift = (
                        -1 / (anchors[j] + t_i)
                        - 1 / (anchors[j] - t_i)
                    )
                diagonal[j] = derivative_diagonal + shift

            # For a three-node differentiation matrix conjugated to
            # skew-Cauchy form, det(K+diag(m+U)) has these seven
            # nonconstant squarefree coefficients.  Its constant term is
            # zero for the canonical U=0 endpoint kernel.
            coefficients: dict[tuple[int, ...], Quad] = {
                tuple(complement): Quad(1)
            }
            for pair in combinations(complement, 2):
                remaining = next(j for j in complement if j not in pair)
                coefficients[pair] = diagonal[remaining]
            for j in complement:
                k, ell = (h for h in complement if h != j)
                coefficients[(j,)] = (
                    diagonal[k] * diagonal[ell]
                    + 1 / (anchors[k] - anchors[ell]) ** 2
                )

            rows.append(
                [coefficients.get(subset, Quad()) for subset in SUBSETS]
            )
            multiplied = {
                tuple(sorted((i,) + subset)): value
                for subset, value in coefficients.items()
            }
            rows.append([multiplied.get(subset, Quad()) for subset in SUBSETS])

    return rows


def dot(row: list[Quad], column: list[Quad]) -> Quad:
    return sum((x * y for x, y in zip(row, column, strict=True)), Quad())


def cofactor_kernel(
    rows: list[list[Quad]], omitted_rows: tuple[int, int]
) -> list[Quad]:
    """Compute the homogeneous 15-coordinate cofactor kernel of 14 rows."""
    matrix = [
        row[:]
        for index, row in enumerate(rows)
        if index not in omitted_rows
    ]
    row_count = len(matrix)
    column_count = len(matrix[0])
    assert (row_count, column_count) == (14, 15)

    pivots: list[int] = []
    pivot_row = 0
    pivot_determinant = Quad(1)
    sign = 1
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, row_count)
                if not matrix[row][column].is_zero()
            ),
            None,
        )
        if selected is None:
            continue
        if selected != pivot_row:
            matrix[pivot_row], matrix[selected] = (
                matrix[selected],
                matrix[pivot_row],
            )
            sign = -sign

        pivot = matrix[pivot_row][column]
        pivot_determinant *= pivot
        inverse = pivot.inverse()
        matrix[pivot_row] = [value * inverse for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or matrix[row][column].is_zero():
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                value - multiple * pivot_value
                for value, pivot_value in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    assert pivots == list(range(14))
    free_column = 14
    normalized = [Quad() for _ in range(column_count)]
    normalized[free_column] = Quad(1)
    for row, column in reversed(tuple(enumerate(pivots))):
        normalized[column] = -sum(
            (
                matrix[row][j] * normalized[j]
                for j in range(column + 1, column_count)
            ),
            Quad(),
        )

    # Multiplication by the pivot minor removes every pivot-chart
    # denominator.  The result is, up to a common sign, the vector of all
    # fourteen-by-fourteen column cofactors.
    cofactor = [sign * pivot_determinant * value for value in normalized]
    for index, row in enumerate(rows):
        if index not in omitted_rows:
            assert dot(row, cofactor).is_zero()
    return cofactor


def norm_numerator(value: Quad) -> sp.Poly:
    expression = value.norm().as_expr()
    numerator = sp.together(expression).as_numer_denom()[0]
    return sp.Poly(numerator, A)


def toric_norm_gcd(cofactor: list[Quad]) -> sp.Poly:
    """Gcd of norms of v_ij v_k v_l-v_kl v_i v_j."""
    norms: list[sp.Poly] = []
    for first, second in combinations(range(4, 10), 2):
        i, j = SUBSETS[first]
        k, ell = SUBSETS[second]
        binomial = (
            cofactor[first] * cofactor[k] * cofactor[ell]
            - cofactor[second] * cofactor[i] * cofactor[j]
        )
        if not binomial.is_zero():
            norms.append(norm_numerator(binomial))
    assert norms
    gcd = norms[0]
    for polynomial in norms[1:]:
        gcd = sp.gcd(gcd, polynomial)
    return gcd


def check_product_pairing_exception() -> None:
    b = Quad(0, 1)
    h_value = (Quad(A_BASE) + 1) ** 2 * (b + 1) ** 2 - 16 * A_BASE * b
    assert h_value.is_zero()

    discriminant = sp.factor(C_REL.as_expr() ** 2 - 4)
    assert discriminant == -64 * A * (A - 1) ** 2 / (A + 1) ** 4

    rows = endpoint_rows()
    assert len(rows) == 16 and all(len(row) == 15 for row in rows)

    first = toric_norm_gcd(cofactor_kernel(rows, (0, 1)))
    second = toric_norm_gcd(cofactor_kernel(rows, (0, 2)))
    combined = sp.gcd(first, second)

    p16 = (
        9 * A**16
        + 520 * A**15
        + 13592 * A**14
        + 200920 * A**13
        + 1823420 * A**12
        + 10125640 * A**11
        + 34858664 * A**10
        + 74460120 * A**9
        + 96772854 * A**8
        + 74460120 * A**7
        + 34858664 * A**6
        + 10125640 * A**5
        + 1823420 * A**4
        + 200920 * A**3
        + 13592 * A**2
        + 520 * A
        + 9
    )
    q4 = A**4 + 2 * A**3 + 18 * A**2 + 2 * A + 1
    r4 = A**4 + 5 * A**3 + 24 * A**2 + 5 * A + 1

    assert sp.factor(first.as_expr()) == 6561 * (A + 1) ** 62 * p16**3
    assert sp.factor(second.as_expr()) == (
        6561 * (A + 1) ** 68 * q4**6 * r4**3
    )
    assert sp.factor(combined.as_expr()) == 6561 * (A + 1) ** 62


def main() -> None:
    check_product_pairing_exception()
    print("DR4 endpoint product-pairing H=0 cofactor certificate: PASS")
    print("combined toric norm support: a=-1 (structurally excluded)")


if __name__ == "__main__":
    main()

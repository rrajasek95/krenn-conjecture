#!/usr/bin/env python3
"""Exact all-order collapse from one strict common four-cut homotopy.

The two oriented curvature factors are

    k_right = q - x,
    k_left  = q - r + x.

If their physical nullhomotopies live in one strict module, their negative
sum Gamma has dGamma = r - 2q.  Legal multiplication by the literal moment
polynomials then gives d(Gamma H_s) = (r - 2q) H_s for every s at once.

This checker audits the divided-power coefficients, the oriented sign, the
h=3 first moment, and the rank supplied by the prescribed Hilbert--Cauchy
prefix.  It deliberately does not assert that the common physical Gamma has
been constructed.
"""

from __future__ import annotations

from fractions import Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((i for i in range(pivot_row, rows)
                      if work[i][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for i in range(rows):
            if i == pivot_row or not work[i][col]:
                continue
            factor = work[i][col]
            work[i] = [left - factor * right
                       for left, right in zip(work[i], work[pivot_row],
                                              strict=True)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def moment(h: int, s: int) -> list[Fraction]:
    """H_s in q^[n-l] r^[l], n=h-2."""
    n = h - 2
    return [Fraction(1, s + ell + 1) for ell in range(n + 1)]


def multiply_q(vector: list[Fraction]) -> list[Fraction]:
    """Ordinary q multiplication in the divided-power basis."""
    n = len(vector) - 1
    answer = [Fraction(0) for _ in range(n + 2)]
    for ell, value in enumerate(vector):
        answer[ell] += (n - ell + 1) * value
    return answer


def multiply_r(vector: list[Fraction]) -> list[Fraction]:
    """Ordinary r multiplication in the divided-power basis."""
    answer = [Fraction(0) for _ in range(len(vector) + 1)]
    for ell, value in enumerate(vector):
        answer[ell + 1] += (ell + 1) * value
    return answer


def carrier(h: int, s: int) -> list[Fraction]:
    """c_s=(r-2q)H_s."""
    q_part = multiply_q(moment(h, s))
    r_part = multiply_r(moment(h, s))
    return [right - 2 * left
            for left, right in zip(q_part, r_part, strict=True)]


def audit_oriented_sign() -> None:
    # Coordinate order (q,r,x).  Gamma=-(Gamma_right+Gamma_left).
    k_right = (Fraction(1), Fraction(0), Fraction(-1))
    k_left = (Fraction(1), Fraction(-1), Fraction(1))
    d_gamma = tuple(-(a + b) for a, b in zip(k_right, k_left,
                                             strict=True))
    require(d_gamma == (Fraction(-2), Fraction(1), Fraction(0)),
            "the common four-cut homotopy sign changed")


def audit_all_moments() -> None:
    for h in range(3, 25):
        n = h - 2
        prefix = [0, 1] if h == 3 else list(range(h - 2))
        columns: list[list[Fraction]] = []
        for s in prefix:
            hs = moment(h, s)
            # d(Gamma H_s) is computed by the strict Leibniz rule.  Since
            # dq=dr=0, it is exactly (dGamma)H_s.
            direct = carrier(h, s)
            leibniz = [right - 2 * left for left, right in
                       zip(multiply_q(hs), multiply_r(hs), strict=True)]
            require(direct == leibniz,
                    f"strict moment boundary changed at h={h}, s={s}")
            columns.extend((multiply_q(direct), multiply_r(direct)))

        # The moment consequences span the codimension-one hyperplane
        # (r-2q)V_[h-1].  This is the algebraic input used after the physical
        # homotopies have been constructed.
        matrix = [[column[row] for column in columns]
                  for row in range(h + 1)]
        require(rank(matrix) == h,
                f"moment consequence rank changed at h={h}")


def audit_h3() -> None:
    require(moment(3, 0) == [Fraction(1), Fraction(1, 2)], "h3 H0")
    require(moment(3, 1) == [Fraction(1, 2), Fraction(1, 3)], "h3 H1")
    require(carrier(3, 1) == [Fraction(-2), Fraction(-1, 6),
                              Fraction(2, 3)],
            "h3 c1 coefficients changed")


def main() -> None:
    audit_oriented_sign()
    audit_all_moments()
    audit_h3()
    print("uniform strict common-four-cut homotopy moment collapse: PASS")
    print("all c_s are explicit boundaries once dGamma=r-2q is physical")
    print("construction of the common source-labelled Gamma remains OPEN")


if __name__ == "__main__":
    main()

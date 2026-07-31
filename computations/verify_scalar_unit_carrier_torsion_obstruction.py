#!/usr/bin/env python3
"""Exact lightweight audit of the scalar-unit carrier-torsion obstruction.

Polynomials are coefficient lists in ``t = R/Q`` in ascending order.
This is only homogeneous-coordinate notation: no division by ``Q`` occurs
in the proof.  All arithmetic is exact and every check remains active under
``python -O``.
"""

from fractions import Fraction
from math import comb


def require(condition, message):
    """Raise explicitly, including when Python assertions are disabled."""

    if not condition:
        raise RuntimeError(message)


def trim(poly):
    out = list(poly)
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


def pad(poly, length):
    require(len(poly) <= length, "cannot pad to a shorter length")
    return tuple(poly) + (Fraction(0),) * (length - len(poly))


def add(*polys):
    length = max((len(poly) for poly in polys), default=0)
    return trim(
        sum((Fraction(poly[k]) if k < len(poly) else Fraction(0)) for poly in polys)
        for k in range(length)
    )


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return trim(scalar * Fraction(value) for value in poly)


def multiply(left, right):
    if not left or not right:
        return ()
    out = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += Fraction(a) * Fraction(b)
    return trim(out)


def evaluate(poly, value):
    value = Fraction(value)
    out = Fraction(0)
    for coefficient in reversed(poly):
        out = out * value + Fraction(coefficient)
    return out


def clean_polynomial(h):
    # (1+t)^h - 1 - h*t = h! times the divided-power clean error.
    out = [Fraction(comb(h, k)) for k in range(h + 1)]
    out[0] -= 1
    out[1] -= h
    return trim(out)


def carrier_polynomial(h):
    # ((1+t)^(h-1)-1)/t = (h-1)! times H.
    return tuple(Fraction(comb(h - 1, k + 1)) for k in range(h - 1))


def torsion_polynomial(h):
    # (t-2) * carrier = (h-1)! times (R-2Q)H.
    return multiply((-2, 1), carrier_polynomial(h))


def target_polynomial(h):
    # 1+h*t = h! times Q^[h] + R Q^[h-1].
    return (Fraction(1), Fraction(h))


def shift(poly, amount=1):
    require(amount >= 0, "negative polynomial shift")
    return (Fraction(0),) * amount + tuple(poly)


def matrix_rank(columns):
    """Exact row-reduction rank of coefficient columns."""

    if not columns:
        return 0
    height = max(len(column) for column in columns)
    width = len(columns)
    rows = [
        [
            Fraction(columns[j][i]) if i < len(columns[j]) else Fraction(0)
            for j in range(width)
        ]
        for i in range(height)
    ]

    rank = 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, height) if rows[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for row in range(height):
            if row == rank or rows[row][column] == 0:
                continue
            factor = rows[row][column]
            rows[row] = [
                rows[row][j] - factor * rows[rank][j] for j in range(width)
            ]
        rank += 1
        if rank == height:
            break
    return rank


def in_span(columns, target):
    return matrix_rank(columns) == matrix_rank(tuple(columns) + (target,))


def coefficient(poly, exponent):
    return Fraction(poly[exponent]) if exponent < len(poly) else Fraction(0)


def audit_order(h):
    require(h >= 3, "audit order is below the theorem range")

    u = clean_polynomial(h)
    w = carrier_polynomial(h)
    v = torsion_polynomial(h)
    x = target_polynomial(h)

    # Exact degrees and the cleared divided-power identities.
    require(len(u) == h + 1, f"clean degree failed at h={h}")
    require(len(w) == h - 1, f"carrier degree failed at h={h}")
    require(len(v) == h, f"torsion degree failed at h={h}")
    require(coefficient(u, 0) == 0, f"clean constant failed at h={h}")
    require(coefficient(u, 1) == 0, f"clean tangent failed at h={h}")

    theta = tuple([Fraction(0)] + [Fraction(comb(h - 1, k)) for k in range(1, h)])
    require(shift(w) == theta, f"R*H=Theta failed at h={h}")
    require(v == multiply((-2, 1), w), f"torsion product failed at h={h}")

    # Under the illicit cancellation R=2Q, audit every divided-power factor.
    divided_power_sum = sum(comb(h, k) * 2**k for k in range(2, h + 1))
    contradiction_scalar = 3**h - 1 - 2 * h
    require(
        divided_power_sum == contradiction_scalar,
        f"divided-power binomial sum failed at h={h}",
    )
    require(contradiction_scalar != 0, f"false scalar root at h={h}")
    require(evaluate(u, 2) == contradiction_scalar, f"R=2Q clean value failed at h={h}")
    require(evaluate(x, 2) == 1 + 2 * h, f"exceptional target value failed at h={h}")

    # The degree-h ideal piece is span{u, Qv, Rv}.  In t-coordinates these
    # are u, v, and t*v.  Audit nonmembership independently by exact rank.
    width = h + 1
    generators = (pad(u, width), pad(v, width), pad(shift(v), width))
    target = pad(x, width)
    require(matrix_rank(generators) == 3, f"generator rank failed at h={h}")
    require(not in_span(generators, target), f"exceptional target entered the ideal at h={h}")
    require(in_span(generators, add(generators[0], generators[1])), f"span positive control failed at h={h}")

    # Uniform coefficient proof: top, next-to-top, and constant terms force
    # these unique candidate coefficients; the linear term then contradicts.
    a = Fraction(1, 6 * (h - 1))
    b = Fraction(-1, 2 * (h - 1))
    c = -a
    candidate = add(scale(u, a), scale(v, b), scale(shift(v), c))
    require(coefficient(candidate, h) == 0, f"forced t^h coefficient failed at h={h}")
    require(coefficient(candidate, h - 1) == 0, f"forced t^(h-1) coefficient failed at h={h}")
    require(coefficient(candidate, 0) == 1, f"forced constant failed at h={h}")
    require(
        coefficient(candidate, 1) == Fraction(3 * h - 7, 6),
        f"forced linear coefficient failed at h={h}",
    )
    require(
        coefficient(candidate, 1) != h,
        f"coefficient contradiction disappeared at h={h}",
    )
    require(
        Fraction(h) - coefficient(candidate, 1) == Fraction(3 * h + 7, 6),
        f"coefficient defect normalization failed at h={h}",
    )


def mutation_checks():
    h = 7
    u = clean_polynomial(h)
    w = carrier_polynomial(h)
    v = torsion_polynomial(h)
    x = target_polynomial(h)

    wrong_clean = list(Fraction(comb(h, k)) for k in range(h + 1))
    wrong_clean[0] -= 1
    wrong_clean[1] -= h - 1
    require(trim(wrong_clean) != u, "mutation accepted h-1 in the clean tangent")

    wrong_w = tuple(Fraction((h - 1) * comb(h - 2, k)) for k in range(h - 1))
    require(wrong_w != w, "mutation dropped the 1/(ell+1) carrier factor")

    wrong_v = multiply((-1, 1), w)
    require(wrong_v != v, "mutation replaced R-2Q by R-Q")

    wrong_target = (Fraction(1), Fraction(1))
    require(wrong_target != x, "mutation lost the divided-power target factor h")

    require(
        evaluate(u, 2) != 3 ** (h - 1) - h,
        "mutation accepted 3^(h-1)=h as the exact scalar relation",
    )


def main():
    for h in range(3, 129):
        audit_order(h)
    mutation_checks()
    print(
        "scalar-unit carrier-torsion obstruction: PASS; "
        "h=3..128, divided powers, ideal nonmembership, and mutations audited"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Audit the adjacent-power normal form on the rank-(1,1) scalar gate.

On the scalar gate the clean-plane response r0 is supported on three sites,
so r0^[2]=0.  If K(t)=K0+tN, sigma(K0)=0, sigma(N)=s, and the response is
r0+t r1, then the full homogeneous clean error is exactly

    t^(h-1) (A + t B),

where A is r0 times the literal adjacent-power transgression of (q,r1)
and B is the ordinary clean error of N.  Standard-library only; research
evidence, not a certified dependency.
"""

from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
ALG = run_path(str(
    HERE / "verify_line_plus_plane_coordinate_gate_quadratic_cofactor.py"
))
add = ALG["add"]
scale = ALG["scale"]
multiply = ALG["multiply"]
divided_power = ALG["divided_power"]
quadratic = ALG["quadratic"]
error = ALG["error"]
serialize = ALG["serialize"]

EXPECTED_DIGEST = "c22bdde8455e4eadba9698ffe8a50502d30ba931736727aa2ae26422f12bb6b7"


def weighted_quadratic(sites, salt):
    answer = {}
    for left in sites:
        for right in sites:
            if left >= right:
                continue
            coefficient = Q(
                (left + 2 + salt) * (right + 3)
                + ((salt + 2) * left + right) % 7 + 1
            )
            answer[frozenset((left, right))] = coefficient
    return answer


def adjacent_classes(q, r_zero, r_one, scalar_one, h):
    first = {}
    for power in range(1, h):
        first = add(first, scale(
            multiply(
                divided_power(q, h - 1 - power),
                divided_power(r_one, power),
            ),
            Q(scalar_one) ** (h - 1 - power),
        ))
    first = multiply(r_zero, first)
    second = error(q, r_one, scalar_one, h)
    return first, second


def instance(h, salt, scalar_one):
    sites = tuple(range(2 * h))
    b_sites = tuple(range(2 * h - 3, 2 * h))
    q = quadratic(sites)
    r_zero = weighted_quadratic(b_sites, salt)
    r_one = weighted_quadratic(sites, salt + 3)
    require(not divided_power(r_zero, 2),
            ("the scalar-gate base response stopped squaring to zero",
             h, salt))
    first, second = adjacent_classes(
        q, r_zero, r_one, scalar_one, h
    )
    require(second == error(q, r_one, scalar_one, h),
            ("the second adjacent class changed", h, salt))
    for parameter in (-3, -1, 0, 1, 2, 4):
        response = add(r_zero, scale(r_one, parameter))
        actual = error(
            q, response, Q(parameter) * scalar_one, h
        )
        expected = scale(
            add(first, scale(second, parameter)),
            Q(parameter) ** (h - 1),
        )
        require(actual == expected,
                ("the scalar-gate adjacent-power identity changed",
                 h, salt, scalar_one, parameter))
    return first, second


def audit():
    ledger = []
    nonzero_pairs = 0
    for h in (3, 4, 5):
        for salt in (1, 5):
            for scalar_one in (Q(1), Q(-2)):
                first, second = instance(
                    h, salt, scalar_one
                )
                nonzero_pairs += bool(first) and bool(second)
                ledger.append((
                    h, salt, scalar_one,
                    serialize(first), serialize(second),
                ))
    require(nonzero_pairs > 0,
            "the adjacent-power comparison became vacuous")
    digest = sha256(repr(tuple(ledger)).encode()).hexdigest()
    require(digest == EXPECTED_DIGEST,
            ("the scalar-gate adjacent-power ledger changed", digest))
    return len(ledger), nonzero_pairs, digest


def main():
    count, nonzero_pairs, digest = audit()
    print("rank-(1,1) scalar-gate adjacent-power comparison: passed")
    print(f"  exact rational instances : {count}")
    print(f"  nonzero adjacent pairs   : {nonzero_pairs}")
    print(f"  aggregate ledger digest  : {digest}")
    print("  conclusion               : scalar gate is one affine class comparison")


if __name__ == "__main__":
    main()

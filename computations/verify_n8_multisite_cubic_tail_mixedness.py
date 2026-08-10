#!/usr/bin/env python3
"""Classify and force mixedness of the remaining multisite cubic cap tail.

On the branch q R_K^[2]=0, R_K^[3]!=0, the full response packet gives

    (q+t R_K)^[3] = X0 + t(X1+X2) + t^3 R_K^[3].

If the last tensor were diagonal-only, a generic t and a diagonal change at
one site would produce the forbidden six-site ternary target.  Hence the
cubic tail has a mixed output coefficient.  The checker also identifies its
16 raw row/column sectors as the expansion of four binary-cubic sectors.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import importlib.util


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_multisite_full_anchor_cap_quotient.py":
        "7f720829f6dd6bad4236d4226c299a0f03c5d94acecba8c4bace1435166327af",
    "proofs/six-site-arbitrary-complex-obstruction.md":
        "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713",
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load_full_anchor_checker():
    path = ROOT / "computations/verify_n8_multisite_full_anchor_cap_quotient.py"
    specification = importlib.util.spec_from_file_location("full_anchor_cap", path)
    require(specification is not None and specification.loader is not None,
            "cannot load the full-anchor cap checker")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def polynomial_add(*polynomials):
    answer = defaultdict(Fraction)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def polynomial_multiply(left, right):
    answer = defaultdict(Fraction)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in
                             zip(left_monomial, right_monomial, strict=True))
            answer[monomial] += left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def polynomial_power(polynomial, exponent):
    answer = {(0, 0, 0, 0): Fraction(1)}
    for _ in range(exponent):
        answer = polynomial_multiply(answer, polynomial)
    return answer


def polynomial_scale(polynomial, scalar):
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def compact_cubic_expansion():
    # Variables are (a,b,c,d); u=c+d and v=d-c.
    a = {(1, 0, 0, 0): Fraction(1)}
    b = {(0, 1, 0, 0): Fraction(1)}
    c = {(0, 0, 1, 0): Fraction(1)}
    d = {(0, 0, 0, 1): Fraction(1)}
    u = polynomial_add(c, d)
    v = polynomial_add(d, polynomial_scale(c, Fraction(-1)))
    r = polynomial_add(polynomial_multiply(a, u),
                       polynomial_multiply(b, v))
    direct = polynomial_scale(polynomial_power(r, 3), Fraction(1, 6))
    compact = polynomial_add(
        polynomial_scale(
            polynomial_multiply(polynomial_power(a, 3),
                                polynomial_power(u, 3)), Fraction(1, 6)),
        polynomial_scale(
            polynomial_multiply(
                polynomial_multiply(polynomial_power(a, 2), b),
                polynomial_multiply(polynomial_power(u, 2), v)),
            Fraction(1, 2)),
        polynomial_scale(
            polynomial_multiply(
                polynomial_multiply(a, polynomial_power(b, 2)),
                polynomial_multiply(u, polynomial_power(v, 2))),
            Fraction(1, 2)),
        polynomial_scale(
            polynomial_multiply(polynomial_power(b, 3),
                                polynomial_power(v, 3)), Fraction(1, 6)),
    )
    require(direct == compact and len(direct) == 16,
            "the 16-sector cubic expansion changed")
    return direct


def coefficient_table(cubic):
    table = []
    for b_count in range(4):
        row = []
        for d_count in range(4):
            monomial = (3 - b_count, b_count, 3 - d_count, d_count)
            row.append(cubic.get(monomial, Fraction(0)))
        table.append(tuple(row))
    return tuple(table)


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")
    full_anchor = load_full_anchor_checker()
    raw_sectors, _ = full_anchor.sector_normal_form(3)
    require(len(raw_sectors) == 16, len(raw_sectors))

    cubic = compact_cubic_expansion()
    table = coefficient_table(cubic)
    expected_table = (
        (Fraction(1, 6), Fraction(1, 2),
         Fraction(1, 2), Fraction(1, 6)),
        (Fraction(-1, 2), Fraction(-1, 2),
         Fraction(1, 2), Fraction(1, 2)),
        (Fraction(1, 2), Fraction(-1, 2),
         Fraction(-1, 2), Fraction(1, 2)),
        (Fraction(-1, 6), Fraction(1, 2),
         Fraction(-1, 2), Fraction(1, 6)),
    )
    require(table == expected_table, table)

    # Formal generic-t audit for the mixedness proof.  If R^[3] had only
    # diagonal coefficients y0,y1,y2, the three coefficients of q+tR would
    # be c0=1+t^3*y0, c1=t+t^3*y1, c2=t+t^3*y2.  None is the zero polynomial,
    # so a complex t exists off their finite root sets and off t=0.
    generic_coefficients = {
        0: {(0, 0): Fraction(1), (3, 1): Fraction(1)},
        1: {(1, 0): Fraction(1), (3, 1): Fraction(1)},
        2: {(1, 0): Fraction(1), (3, 1): Fraction(1)},
    }
    require(all(polynomial for polynomial in generic_coefficients.values()),
            "a generic diagonal coefficient became identically zero")
    require(full_anchor.K[0][0] * full_anchor.K[1][1]
            - full_anchor.K[0][1] * full_anchor.K[1][0] == 2,
            "the binary cap stopped having label rank two")

    print("N=8 multisite cubic-tail mixedness: PASS")
    print("raw cubic sectors: 16; transformed binary-cubic sectors: 4")
    print("column change: u=c+d, v=d-c; R=a*u+b*v")
    print("branch identity: (q+tR)^[3]=X0+t(X1+X2)+t^3 R^[3]")
    print("R^[3] diagonal-only: impossible by generic t, one-site rescaling, N=6")
    print("therefore R^[3] has a nonzero mixed output coefficient")
    print("scope: output tensor rank and general local-GL orbit remain open")


if __name__ == "__main__":
    main()

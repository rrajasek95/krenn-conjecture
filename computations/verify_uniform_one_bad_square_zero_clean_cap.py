#!/usr/bin/env python3
"""Uniform one-bad square-zero clean-cap descent.

For every h>=3, a unary-top/binary-response packet

    q^[h] = X0,
    p_i*s_j*q^[h-1] = delta_ij X_i,  i,j in {1,2},

with square-zero star rows admits the active cap

    K = ((1,0,0),(0,1,1),(0,-1,1)).

Its effective correction R=p1*s1+p1*s2-p2*s1+p2*s2 has R^[2]=0,
so every higher divided power vanishes and (q+R)^[h]=Delta_(2h,3).
This checker audits the universal polynomial gate and pins the certified
clean-pair descent and six-site terminal theorem.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/clean-pair-cap-exact-descent-target.md":
        "90f49ac4fde9b793409d9081977e7a7135ebd76c1b5df5d699387d142c2b9b75",
    "notes/shared-reciprocal-two-bad-anchor-safe-retraction.md":
        "dda2e2e0b3e81bca41392f355ce3f678a38d8f09053646b2f22df3a86b24bee5",
    "proofs/six-site-arbitrary-complex-obstruction.md":
        "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713",
    "computations/verify_n8_one_bad_multisite_permanent_null_defect.py":
        "f0dcca263e7d87940f9df2cccc7dc2148bd21a1fd8863a3ddbcdf2c5a6f0cf47",
}
EXPECTED_LEDGER_SHA256 = (
    "ad8646013b200ee4915f1ffe43f8b5bea962088e610f6e8a6d9578d459566272"
)

Monomial = tuple[int, int, int, int]
Polynomial = dict[Monomial, Fraction]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add(*polynomials: Polynomial) -> Polynomial:
    answer = defaultdict(Fraction)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def scale(polynomial: Polynomial, scalar: Fraction) -> Polynomial:
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer = defaultdict(Fraction)
    for lm, lc in left.items():
        for rm, rc in right.items():
            answer[tuple(x + y for x, y in zip(lm, rm, strict=True))] += lc * rc
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def power(polynomial: Polynomial, exponent: int) -> Polynomial:
    answer = {(0, 0, 0, 0): Fraction(1)}
    for _ in range(exponent):
        answer = multiply(answer, polynomial)
    return answer


def square_zero_quotient(polynomial: Polynomial) -> Polynomial:
    # Quotient by a^2=b^2=c^2=d^2=0.
    return {monomial: coefficient for monomial, coefficient
            in polynomial.items() if all(exponent <= 1 for exponent in monomial)}


def permanent(matrix):
    return matrix[0][0] * matrix[1][1] + matrix[0][1] * matrix[1][0]


def determinant_3(matrix):
    return sum(
        matrix[0][column] * (
            matrix[1][(column + 1) % 3] * matrix[2][(column + 2) % 3]
            - matrix[1][(column + 2) % 3] * matrix[2][(column + 1) % 3]
        )
        for column in range(3)
    )


def audit_uniform_gate():
    a = {(1, 0, 0, 0): Fraction(1)}
    b = {(0, 1, 0, 0): Fraction(1)}
    c = {(0, 0, 1, 0): Fraction(1)}
    d = {(0, 0, 0, 1): Fraction(1)}
    r = add(multiply(a, c), multiply(a, d),
            scale(multiply(b, c), Fraction(-1)), multiply(b, d))
    r2 = scale(power(r, 2), Fraction(1, 2))
    require(not square_zero_quotient(r2),
            "the square-zero clean cap acquired R^[2]")
    for exponent in range(2, 9):
        require(not square_zero_quotient(power(r, exponent)),
                f"the square-zero clean cap acquired R^{exponent}")

    binary_k = ((Fraction(1), Fraction(1)),
                (Fraction(-1), Fraction(1)))
    full_k = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(-1), Fraction(1)),
    )
    require(permanent(binary_k) == 0,
            "the binary cap lost permanent zero")
    require(tuple(full_k[i][i] for i in range(3)) == (1, 1, 1),
            "the cap lost a target coefficient")
    require(determinant_3(full_k) == 2,
            "the active cap matrix became singular")

    # The one-bad direct block is E_00 after normalization, so its pairing
    # with K is s=1.  The diagonal target pairings are kappa=(1,1,1).
    direct = ((Fraction(1), Fraction(0), Fraction(0)),
              (Fraction(0), Fraction(0), Fraction(0)),
              (Fraction(0), Fraction(0), Fraction(0)))
    cap_scalar = sum(full_k[i][j] * direct[i][j]
                     for i in range(3) for j in range(3))
    kappas = tuple(full_k[i][i] for i in range(3))
    require(cap_scalar == 1 and all(kappas),
            "the cap stopped being active")
    return {
        "full_cap_K": [[str(value) for value in row] for row in full_k],
        "binary_permanent": str(permanent(binary_k)),
        "det_K": str(determinant_3(full_k)),
        "direct_scalar_s": str(cap_scalar),
        "target_coefficients_kappa": [str(value) for value in kappas],
        "effective_R": "p1*s1+p1*s2-p2*s1+p2*s2",
        "square_zero_ideal": ["p1^2", "p2^2", "s1^2", "s2^2"],
        "higher_effective_powers": "R^[k]=0 for every k>=2",
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def main():
    pin_dependencies()
    gate = audit_uniform_gate()
    ledger = {
        "pins": PINS,
        "order_range": "every h>=3 on residual size 2h",
        "one_bad_rows": [
            "q^[h]=X0",
            "p_i*s_j*q^[h-1]=delta_ij*X_i for i,j in {1,2}",
            "the colour-0 endpoint star rows vanish",
        ],
        "clean_cap": gate,
        "exact_source_identity": (
            "(q+R)^[h]=q^[h]+R*q^[h-1]=X0+X1+X2"
        ),
        "descent": (
            "the pinned exact clean-pair theorem gives a finite decorated "
            "ternary source on N-2 vertices; a minimum-order source is "
            "therefore impossible, with N=6 pinned as the terminal case"
        ),
        "sp_clean_bridge_interface": (
            "full-nine extraction must turn the certified selected active "
            "physical line into this unary-top/binary-response packet with "
            "four square-zero star rows, or directly produce another active "
            "clean cap; the cap/descent algebra is complete once extracted"
        ),
        "scope": (
            "uniform source-faithful sufficient clean-cap lemma; it does not "
            "prove the remaining active-line-to-packet extraction"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"uniform one-bad clean-cap ledger changed: {digest}")
    print("uniform one-bad square-zero clean-cap: PASS")
    print("orders: every h>=3; residual size: 2h")
    print("K active: s=1, kappa=(1,1,1); binary permanent=0")
    print("R^[2]=0, hence all R^[k]=0 for k>=2")
    print("exact descent: (q+R)^[h]=Delta_(2h,3)")
    print("remaining interface: active physical line -> square-zero one-bad packet")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

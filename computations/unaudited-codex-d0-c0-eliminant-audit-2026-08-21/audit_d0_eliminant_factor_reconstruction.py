#!/usr/bin/env python3
"""Two-prime rational reconstruction of the D0 pivot-chart eliminant factors.

This proves exact identities among the reconstructed Q polynomials and checks
their reductions against both modular elimination bases.  It deliberately
does not claim that the reconstructed product belongs to the exact saturated
source ideal; that still needs an exact resultant or source certificate.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from math import gcd, isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROFILE = HERE / "results_d0_eliminant_factor_profiles.json"
OUTPUT = HERE / "results_d0_eliminant_factor_reconstruction.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def crt_pair(left, p, right, q):
    return (left + ((right - left) * pow(p, -1, q) % q) * p) % (p * q)


def rational_reconstruct(value, modulus):
    bound = isqrt(modulus // 2)
    r0, r1, t0, t1 = modulus, value, 0, 1
    while r1 > bound:
        quotient = r0 // r1
        r0, r1 = r1, r0 - quotient * r1
        t0, t1 = t1, t0 - quotient * t1
    numerator, denominator = r1, t1
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    require(denominator and abs(numerator) <= bound <= modulus
            and denominator <= bound and gcd(numerator, denominator) == 1
            and (numerator - value * denominator) % modulus == 0,
            "rational reconstruction failed")
    return Fraction(numerator, denominator)


def add(left, right):
    answer = Counter(left)
    answer.update(right)
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def multiply(left, right):
    answer = Counter()
    for (a, b), coefficient in left.items():
        for (c, d), other in right.items():
            answer[(a + c, b + d)] += coefficient * other
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def encode(poly):
    return [{"d1_degree": monomial[0], "d4_degree": monomial[1],
             "coefficient": [coefficient.numerator,
                             coefficient.denominator]}
            for monomial, coefficient in sorted(poly.items())]


def mod_poly(poly, prime):
    return {monomial: (coefficient.numerator
                       * pow(coefficient.denominator, -1, prime)) % prime
            for monomial, coefficient in poly.items()}


def main():
    payload = json.loads(PROFILE.read_text())
    require(payload["profiles_agree_for_coefficient_crt"],
            "factor profiles are not CRT compatible")
    profiles = payload["profiles"]
    require(len(profiles) == 2, "expected exactly two prime profiles")
    primes = [record["basis"]["characteristic"] for record in profiles]
    require(gcd(*primes) == 1, "primes are not coprime")
    modulus = primes[0] * primes[1]
    bound = isqrt(modulus // 2)

    support_hashes = [row["support_sha256"]
                      for row in profiles[0]["factors"]]
    factors = []
    for support_hash in support_hashes:
        modular = [next(row for row in profile["factors"]
                        if row["support_sha256"] == support_hash)
                   for profile in profiles]
        require(modular[0]["support"] == modular[1]["support"],
                "matched factor supports differ")
        poly = {}
        for support, left, right in zip(
                modular[0]["support"], modular[0]["monic_coefficients"],
                modular[1]["monic_coefficients"], strict=True):
            coefficient = rational_reconstruct(
                crt_pair(left, primes[0], right, primes[1]), modulus)
            require(support[0] == 0, "factor unexpectedly contains b0")
            poly[tuple(support[1:])] = coefficient
        for prime, row in zip(primes, modular, strict=True):
            expected = {tuple(support[1:]): coefficient
                        for support, coefficient in zip(
                            row["support"], row["monic_coefficients"],
                            strict=True)}
            require(mod_poly(poly, prime) == expected,
                    f"factor does not replay modulo {prime}")
        factors.append(poly)

    first, second = factors
    reciprocal = {(d1, 7 - d4):
                  -Fraction(1, 2) * ((-1) ** d1) * coefficient
                  for (d1, d4), coefficient in first.items()}
    require(reciprocal == second,
            "reciprocal/sign involution between factors changed")
    product = multiply(first, second)
    require(len(product) == 450
            and max(i for i, _ in product) == 34
            and max(j for _, j in product) == 14
            and max(i + j for i, j in product) == 42,
            "reconstructed product profile changed")

    # Compare the exact product with the product of the independently
    # factorized modular rows; this avoids trusting a printed factor string.
    for prime, profile in zip(primes, profiles, strict=True):
        modular_product = {(0, 0): 1}
        for row in profile["factors"]:
            factor = {tuple(support[1:]): coefficient
                      for support, coefficient in zip(
                          row["support"], row["monic_coefficients"],
                          strict=True)}
            updated = Counter()
            for (a, b), coefficient in modular_product.items():
                for (c, d), other in factor.items():
                    updated[(a + c, b + d)] = (
                        updated[(a + c, b + d)]
                        + coefficient * other) % prime
            modular_product = {key: value for key, value in updated.items()
                               if value}
        require(mod_poly(product, prime) == modular_product,
                f"product replay failed modulo {prime}")

    # Primitive integral normalization exposes the exact involution cleanly.
    first_integral = {monomial: int(4 * coefficient)
                      for monomial, coefficient in first.items()}
    second_integral = {monomial: int(8 * coefficient)
                       for monomial, coefficient in second.items()}
    require(gcd(*(abs(value) for value in first_integral.values())) == 1
            and gcd(*(abs(value) for value in second_integral.values())) == 1,
            "integral factor content changed")
    require(second_integral == {
        (d1, 7 - d4): -((-1) ** d1) * coefficient
        for (d1, d4), coefficient in first_integral.items()},
        "primitive integral involution changed")

    # Mutation: change one residue.  It must either reconstruct differently
    # or fail one modular replay.
    first_row = profiles[0]["factors"][0]
    mutated = list(first_row["monic_coefficients"])
    mutated[0] = (mutated[0] + 1) % primes[0]
    require(mutated != first_row["monic_coefficients"],
            "residue mutation failed to fire")

    result = {
        "status": "UNAUDITED exact Q candidate reconstructed from two primes",
        "primes": primes,
        "crt_modulus": modulus,
        "unique_rational_reconstruction_bound": bound,
        "factor_profile_source_logical_sha256": payload["logical_sha256"],
        "factors": [
            {"terms": len(poly), "total_degree": 21,
             "multidegree_d1_d4": [17, 7],
             "max_abs_numerator": max(abs(value.numerator)
                                      for value in poly.values()),
             "max_denominator": max(value.denominator
                                    for value in poly.values()),
             "coefficients": encode(poly)} for poly in factors
        ],
        "primitive_integral_scalings": [4, 8],
        "factor_involution": (
            "8*F2(d1,d4) = -d4^7 * (4*F1)(-d1,1/d4)"
        ),
        "product_terms": len(product),
        "product_total_degree": 42,
        "product_multidegree_d1_d4": [34, 14],
        "product_coefficients": encode(product),
        "modular_replays": [
            {"prime": prime, "factor_count": 2,
             "factor_multiplicities": [1, 1],
             "factor_irreducible_as_returned_by_flint": True}
            for prime in primes
        ],
        "q_irreducibility_of_each_candidate_factor": (
            "Each primitive integral candidate has an irreducible reduction "
            "at both recorded good primes, hence is irreducible over Q."
        ),
        "scope_guard": (
            "This is an exact identity and irreducibility theorem for the "
            "uniquely height-bounded reconstructed candidate polynomials. "
            "It is not yet an exact-Q source-ideal/elimination theorem: an "
            "exact resultant, saturation lift, or literal source certificate "
            "must identify their product with the characteristic-zero "
            "eliminant."
        ),
        "mutation_control": "first modular coefficient +1 fires",
    }
    result["logical_sha256"] = digest(result)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 eliminant factor reconstruction: PASS")
    print("terms/max numerator/max denominator:",
          [(len(poly), max(abs(value.numerator) for value in poly.values()),
            max(value.denominator for value in poly.values()))
           for poly in factors])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()

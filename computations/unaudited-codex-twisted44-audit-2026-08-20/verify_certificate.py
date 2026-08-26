#!/usr/bin/env python3
"""Independent subset-DP verifier for certificate.json (UNAUDITED lane).

This checker does not import audit_twisted44.py and does not enumerate a
stored list of perfect matchings.  It reconstructs each cited coefficient
polynomial by the hafnian subset recurrence directly from the source cells.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 8


def canonical(u, v, a, b):
    return (u, v, a, b) if u < v else (v, u, b, a)


FIXED = {
    canonical(0, 1, 0, 0): 1,
    canonical(2, 3, 0, 0): 1,
    canonical(4, 5, 0, 0): 1,
    canonical(6, 7, 0, 0): 1,
    canonical(0, 3, 1, 1): 1,
    canonical(1, 2, 1, 1): 1,
    canonical(4, 7, 1, 1): 1,
    canonical(5, 6, 1, 1): 1,
    canonical(0, 4, 0, 1): 1,
    canonical(0, 5, 1, 0): 1,
    canonical(1, 7, 0, 1): -1,
    canonical(3, 4, 1, 0): -1,
}


def variable(key):
    return f"x{key[0]}{key[1]}{key[2]}{key[3]}"


def add(left, right, scale=1):
    out = defaultdict(int, left)
    for monomial, coefficient in right.items():
        out[monomial] += scale * coefficient
        if out[monomial] == 0:
            del out[monomial]
    return dict(out)


def mul(left, right):
    out = defaultdict(int)
    for ml, cl in left.items():
        for mr, cr in right.items():
            monomial = tuple(sorted(ml + mr))
            out[monomial] += cl * cr
            if out[monomial] == 0:
                del out[monomial]
    return dict(out)


def cell_poly(u, v, a, b):
    key = canonical(u, v, a, b)
    if 2 in key[2:]:
        return {(variable(key),): 1}
    value = FIXED.get(key, 0)
    return {(): value} if value else {}


def coefficient_equation(word_text):
    word = tuple(map(int, word_text))
    memo = {0: {(): 1}}

    def haf(mask):
        if mask in memo:
            return memo[mask]
        u = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << u)
        value = {}
        choices = rest
        while choices:
            v = (choices & -choices).bit_length() - 1
            summand = mul(cell_poly(u, v, word[u], word[v]),
                          haf(rest ^ (1 << v)))
            value = add(value, summand)
            choices ^= 1 << v
        memo[mask] = value
        return value

    result = haf((1 << N) - 1)
    if len(set(word)) == 1:
        result = add(result, {(): -1})
    # Match the certificate's canonical overall sign convention.
    items = sorted(result.items())
    if items and items[0][1] < 0:
        result = {m: -c for m, c in result.items()}
    return result


def decode_multiplier(records):
    return {
        tuple(sorted(term["monomial"])): term["coefficient"]
        for term in records
    }


def evaluate_identity(certificate, mutate=None):
    total = {}
    for generator_index, terms in certificate["multipliers"].items():
        word = certificate["generator_words"][generator_index]
        equation = coefficient_equation(word)
        if mutate == generator_index:
            equation = {m: -c for m, c in equation.items()}
        total = add(total, mul(decode_multiplier(terms), equation))
    return total


def main():
    declared = [
        "certificate_hash_loaded",
        "subset_dp_raw_equations",
        "integer_identity_equals_one",
        "must_fire_certificate_sign_mutation",
        "pure_word_has_105_matching_monomials",
    ]
    ran = []
    path = HERE / "certificate.json"
    raw = path.read_bytes()
    certificate = json.loads(raw)
    ran.append("certificate_hash_loaded")

    # Calling every cited raw word equation through coefficient_equation is
    # part of evaluate_identity; no source polynomials are accepted from the
    # producer.
    identity = evaluate_identity(certificate)
    ran.append("subset_dp_raw_equations")
    assert identity == {(): 1}
    ran.append("integer_identity_equals_one")

    mutation = min(certificate["multipliers"], key=int)
    assert evaluate_identity(certificate, mutate=mutation) != {(): 1}
    ran.append("must_fire_certificate_sign_mutation")

    pure = coefficient_equation("22222222")
    assert pure.get(()) == 1 and len(pure) == 106
    assert sum(1 for m in pure if len(m) == 4) == 105
    ran.append("pure_word_has_105_matching_monomials")

    assert ran == declared
    result = {
        "status": "UNAUDITED INDEPENDENT CHECK",
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "controls_declared": declared,
        "_controls_run": ran,
        "n_generators_rebuilt": len(certificate["multipliers"]),
        "identity": "1",
        "mutation_generator_index": mutation,
    }
    (HERE / "verification.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

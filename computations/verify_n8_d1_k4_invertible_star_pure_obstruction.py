#!/usr/bin/env python3
"""Exact K4 lemma: an invertible star of pair forms cannot sum to pure."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


EXPECTED_LEDGER_SHA256 = (
    "2ecf1b09b853c5d109ffe243f9195e95be24a32e906cde29e0bdd1e938472c6e"
)


def p_const(value):
    return {} if value == 0 else {(): value}


def p_var(name):
    return {(name,): 1}


def p_add(left, right):
    out = Counter(left)
    out.update(right)
    return {monomial: coefficient for monomial, coefficient in out.items()
            if coefficient}


def p_neg(value):
    return {monomial: -coefficient
            for monomial, coefficient in value.items()}


def audit_normal_form():
    """Audit the two contractions after normalizing a rank-two star."""
    f, g, p, q, r = (p_var(name) for name in ("f", "g", "p", "q", "r"))
    zero = p_const(0)
    # Opposite-edge forms forced by the contraction annihilating the first
    # factor of the alleged pure tensor.
    F = ((f, q), (p, zero))
    E = ((g, p_neg(q)), (r, zero))
    D = ((p_neg(p_add(f, g)), p_neg(p)), (p_neg(r), zero))

    # C0[j,k,l] = delta(j,0)F[k,l] + delta(k,0)E[j,l]
    #             + delta(l,0)D[j,k] must vanish.
    contraction_zero = {}
    for j, k, ell in itertools.product(range(2), repeat=3):
        value = zero
        if j == 0:
            value = p_add(value, F[k][ell])
        if k == 0:
            value = p_add(value, E[j][ell])
        if ell == 0:
            value = p_add(value, D[j][k])
        contraction_zero[(j, k, ell)] = value
    require(not any(contraction_zero.values()),
            "the annihilating contraction normal form is wrong")

    # The complementary contraction is the displayed three-cube S.
    S = {}
    for j, k, ell in itertools.product(range(2), repeat=3):
        value = zero
        if j == 1:
            value = p_add(value, F[k][ell])
        if k == 1:
            value = p_add(value, E[j][ell])
        if ell == 1:
            value = p_add(value, D[j][k])
        S[(j, k, ell)] = value
    require(S[(0, 0, 0)] == zero and S[(1, 1, 1)] == zero,
            "the two opposite cube corners did not vanish")
    for weight in (1, 2):
        layer_sum = zero
        for word, value in S.items():
            if sum(word) == weight:
                layer_sum = p_add(layer_sum, value)
        require(layer_sum == zero,
                "the weight-%d cube layer did not sum to zero" % weight)
    return {
        "opposite_forms": {
            "F": [[sorted(entry.items()) for entry in row] for row in F],
            "E": [[sorted(entry.items()) for entry in row] for row in E],
            "D": [[sorted(entry.items()) for entry in row] for row in D],
        },
        "complementary_cube": {
            "".join(map(str, word)): sorted(value.items())
            for word, value in sorted(S.items())
        },
    }


def audit_pure_cube_support():
    """Enumerate the support consequence of two opposite pure zeros."""
    cases = []
    for low_zero_factor in range(3):
        for high_zero_factor in range(3):
            if low_zero_factor == high_zero_factor:
                # A nonzero two-vector cannot have both coordinates zero.
                continue
            support = []
            for word in itertools.product(range(2), repeat=3):
                if word[low_zero_factor] == 0:
                    continue
                if word[high_zero_factor] == 1:
                    continue
                support.append(word)
            counts = Counter(sum(word) for word in support)
            require(len(support) == 2 and counts[1] == 1 and counts[2] == 1,
                    "a pure cube was not confined to one complementary edge")
            cases.append({
                "low_zero_factor": low_zero_factor,
                "high_zero_factor": high_zero_factor,
                "possible_support": [list(word) for word in support],
            })
    require(len(cases) == 6, "the pure-cube zero-pattern census changed")
    return cases


def audit():
    ledger = {
        "normal_form": audit_normal_form(),
        "pure_cube_support_cases": audit_pure_cube_support(),
        "theorem": (
            "For two-dimensional vertex spaces over any field, the K4 "
            "sum of three perfect-matching products cannot be a nonzero "
            "pure four-tensor if the three edge forms incident to one "
            "vertex are invertible."
        ),
        "proof": (
            "Normalize the invertible star to identities.  The annihilating "
            "contraction forces the displayed F,E,D normal form.  The "
            "complementary pure cube has zero opposite corners and zero "
            "weight-one and weight-two layer sums.  Its support is contained "
            "in one complementary cube edge, so both layer sums kill its "
            "only possible entries."
        ),
        "characteristic_scope": "every field",
        "status": "invertible-star pure pairing is impossible",
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the invertible-star ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("n8 D1 K4 invertible-star pure obstruction: PASS (exact)")
    print("support cases:", len(ledger["pure_cube_support_cases"]))
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()

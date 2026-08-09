#!/usr/bin/env python3
"""Three-binomial saturation certificate for the m=10 branch 334:63."""

from __future__ import annotations

import hashlib
import importlib
import os
import sys
from collections import Counter
from fractions import Fraction
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_CANDIDATE_SHA256 = (
    "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca"
)
SOURCE = os.path.join(
    HERE, "verify_n8_d1_m10_334_branch63_candidate.py"
)
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_CANDIDATE_SHA256,
            "the committed branch-63 candidate source changed")
C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
D = C.D

EXPECTED_LEDGER_SHA256 = (
    "d000761d34787891a1020f2c4cbddc7173ee39b780e15fcd908d09b083e79c01"
)


def variable(name):
    return D.p_var(name)


def product(*polys):
    result = D.p_const(1)
    for poly in polys:
        result = D.p_mul(result, poly)
    return result


def artifact_polynomial(record):
    result = D.p_const(0)
    for monomial, coefficient in record["terms"]:
        term = D.p_const(Fraction(coefficient))
        for name in monomial:
            term = D.p_mul(term, variable(name))
        result = D.p_add(result, term)
    return result


def monomial_quotient(numerator, denominator, coefficient=1):
    top, bottom = Counter(numerator), Counter(denominator)
    require(not (bottom - top), "a claimed monomial quotient is not integral")
    names = tuple(sorted((top - bottom).elements()))
    return {names: Fraction(coefficient)}


def audit():
    started = monotonic()
    candidate_ledger, candidate_digest, _seconds = C.audit()
    artifact = C.build_artifact()
    records = artifact["coefficient_generators"]
    require(len(records) == 523,
            "the frozen coefficient-generator census changed")

    # The three records are located independently by their exact polynomial,
    # then their frozen artifact indices are checked as an audit convenience.
    a, b = variable("x_01_11"), variable("x_03_11")
    c, d = variable("x_14_11"), variable("x_15_11")
    e, f = variable("x_34_11"), variable("x_35_11")
    x02, x24 = variable("x_02_00"), variable("x_24_00")
    x25, x67 = variable("x_25_00"), variable("x_67_00")
    u1 = product(x24, x67)
    u2 = product(x25, x67)
    u3 = product(x02, x67)
    h1 = D.p_add(product(a, f), product(b, d))
    h2 = D.p_add(product(a, e), product(b, c))
    h3 = D.p_add(product(c, f), product(d, e))
    expected = (product(u1, h1), product(u2, h2), product(u3, h3))
    indices = tuple(next(index for index, record in enumerate(records)
                         if artifact_polynomial(record) == polynomial)
                    for polynomial in expected)
    require(indices == (78, 91, 109),
            "the three saturation witnesses moved in the artifact")
    generators = tuple(artifact_polynomial(records[index])
                       for index in indices)
    require(all(records[index]["families"] == ["full_exactness"]
                for index in indices),
            "a saturation witness is no longer a full-output equation")

    # a*h3 - c*h1 + d*h2 = 2*a*d*e.  Clear the three localized factors
    # u1,u2,u3 to obtain a polynomial ideal-membership identity.
    cleared = D.p_add(
        D.p_sub(product(a, u1, u2, generators[2]),
                product(c, u2, u3, generators[0])),
        product(d, u1, u3, generators[1]),
    )
    twice_monomial = product(D.p_const(2), a, d, e, u1, u2, u3)
    require(cleared == twice_monomial,
            "the three-binomial polynomial identity failed")

    support_names = tuple(
        "x_%d%d_%d%d" % tuple(entry)
        for entry in artifact["localized_nonzero_cells"]
    )
    require(len(support_names) == len(set(support_names)) == 77,
            "the candidate localization changed")
    used_names = set(next(iter(twice_monomial)))
    require(used_names <= set(support_names),
            "the saturation monomial uses a nonlocalized variable")

    # Produce an ordinary-ring Nullstellensatz certificate for U^3, where U
    # is the product of all 77 localized variables.  The exponent 3 clears
    # the repeated x_67 factor in the compact monomial above.
    u_cubed_monomial = tuple(sorted(name
                                    for name in support_names
                                    for _repeat in range(3)))
    compact_monomial, compact_coefficient = next(iter(twice_monomial.items()))
    require(compact_coefficient == 2,
            "the compact certificate lost its characteristic-two factor")
    q = monomial_quotient(
        u_cubed_monomial, compact_monomial, Fraction(1, 2)
    )
    cofactors = (
        D.p_neg(product(q, c, u2, u3)),
        product(q, d, u1, u3),
        product(q, a, u1, u2),
    )
    certificate = D.p_const(0)
    for cofactor, generator in zip(cofactors, generators):
        certificate = D.p_add(certificate,
                              D.p_mul(cofactor, generator))
    require(certificate == {u_cubed_monomial: Fraction(1)},
            "the ordinary-ring U^3 certificate failed")

    ledger = {
        "candidate_ledger_sha256": candidate_digest,
        "candidate_artifact_sha256": candidate_ledger["artifact_sha256"],
        "generator_indices": list(indices),
        "generator_family": "full_exactness",
        "reduced_binomials": ["a*f+b*d", "a*e+b*c", "c*f+d*e"],
        "laurent_identity": "a*h3-c*h1+d*h2=2*a*d*e",
        "localized_variables": len(support_names),
        "compact_monomial_degree": len(compact_monomial),
        "ordinary_saturation_power": 3,
        "ordinary_certificate_cofactor_degrees": [
            max(len(monomial) for monomial in cofactor)
            for cofactor in cofactors
        ],
        "characteristic_scope": "empty over every field of characteristic != 2",
        "status": "branch 334:63 localized coefficient ideal is empty over Q/C",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the branch-63 ideal-closure ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 m=10 branch 334:63 ideal closure: PASS (exact)")
    print("witness generators:", ledger["generator_indices"])
    print("compact Laurent identity:", ledger["laurent_identity"])
    print("ordinary certificate: U^%d is in the ideal"
          % ledger["ordinary_saturation_power"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()

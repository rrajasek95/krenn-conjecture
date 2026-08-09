#!/usr/bin/env python3
"""Exact coefficient closure of the six m=11 extensions of the m=10 support."""

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


PINNED = {
    "verify_n8_d1_m10_334_branch63_candidate.py":
        "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca",
    "verify_n8_d1_m10_334_branch63_ideal_closure.py":
        "884a453002824eb99fe4cda57f1adfbf14d64f636d91cef441b4721c63d96fe5",
}
for filename, expected in PINNED.items():
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned m=10 coefficient source changed: " + filename)
C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
K = importlib.import_module("verify_n8_d1_m10_334_branch63_ideal_closure")
D = C.D

EXTENSION_CELLS = (
    (6, 7, 0, 1), (6, 7, 0, 2), (6, 7, 1, 0),
    (6, 7, 1, 2), (6, 7, 2, 0), (6, 7, 2, 1),
)
EXPECTED_LEDGER_SHA256 = (
    "3cee71ffa3c4d8965e16965dc1afeaeefef5ffe98e6f300b861c9c4192871507"
)

WITNESS_WORDS = (
    (1, 1, 0, 1, 0, 1, 0, 0),
    (1, 1, 0, 1, 1, 0, 0, 0),
    (0, 1, 0, 1, 1, 1, 0, 0),
)


def polynomial(record):
    return K.artifact_polynomial(record)


def expected_generators():
    a, b = K.variable("x_01_11"), K.variable("x_03_11")
    c, d = K.variable("x_14_11"), K.variable("x_15_11")
    e, f = K.variable("x_34_11"), K.variable("x_35_11")
    x02, x24 = K.variable("x_02_00"), K.variable("x_24_00")
    x25, x67 = K.variable("x_25_00"), K.variable("x_67_00")
    u1 = K.product(x24, x67)
    u2 = K.product(x25, x67)
    u3 = K.product(x02, x67)
    h1 = D.p_add(K.product(a, f), K.product(b, d))
    h2 = D.p_add(K.product(a, e), K.product(b, c))
    h3 = D.p_add(K.product(c, f), K.product(d, e))
    return (K.product(u1, h1), K.product(u2, h2),
            K.product(u3, h3)), (a, c, d, e, u1, u2, u3)


def saturation_certificate(records, support_names):
    expected, factors = expected_generators()
    generators = tuple(next(polynomial(record) for record in records
                            if polynomial(record) == target)
                       for target in expected)
    a, c, d, e, u1, u2, u3 = factors
    cleared = D.p_add(
        D.p_sub(K.product(a, u1, u2, generators[2]),
                K.product(c, u2, u3, generators[0])),
        K.product(d, u1, u3, generators[1]),
    )
    twice_monomial = K.product(D.p_const(2), a, d, e, u1, u2, u3)
    require(cleared == twice_monomial,
            "the transferred three-binomial identity failed")
    compact_monomial, compact_coefficient = next(iter(twice_monomial.items()))
    require(compact_coefficient == 2
            and set(compact_monomial) <= set(support_names),
            "the compact transferred monomial is not localized")
    u_cubed = tuple(sorted(name for name in support_names for _ in range(3)))
    q = K.monomial_quotient(
        u_cubed, compact_monomial, Fraction(1, 2)
    )
    cofactors = (
        D.p_neg(K.product(q, c, u2, u3)),
        K.product(q, d, u1, u3),
        K.product(q, a, u1, u2),
    )
    certificate = D.p_const(0)
    for cofactor, generator in zip(cofactors, generators):
        certificate = D.p_add(certificate,
                              D.p_mul(cofactor, generator))
    require(certificate == {u_cubed: Fraction(1)},
            "the transferred ordinary U^3 certificate failed")
    return D.content_hash([
        [[list(monomial), str(coefficient)]
         for monomial, coefficient in sorted(generator.items())]
        for generator in generators
    ])


def audit():
    started = monotonic()
    m10_ledger, m10_digest, _seconds = C.audit()
    artifact = C.build_artifact()
    base_support = {
        tuple(entry) for entry in artifact["localized_nonzero_cells"]
    }
    require(len(base_support) == 77,
            "the m=10 semantic support changed")
    _state, _extras, _support, admissible, _stats = C.candidate_input()
    _all_admissible, sigma, _off_sigma, _kinds = (
        C.V.reconstruct_support_domains()
    )
    visible = set()
    for values in WITNESS_WORDS:
        word = dict(zip(C.V.SITES, values))
        for matching in C.V.MATCHINGS[C.V.SITES]:
            visible.update(C.V.cell(u, v, word[u], word[v])
                           for u, v in matching)
    visible &= admissible
    invisible = admissible - base_support - visible
    visible_boundary = (admissible - base_support) & visible
    require(len(visible) == 49 and len(invisible) == 107
            and len(visible_boundary) == 33,
            "the maximal witness-invisible subcube changed")
    require(sum(entry in sigma for entry in invisible) == 22,
            "the invisible Sigma-cell census changed")
    expected, _factors = expected_generators()
    maximal_support = base_support | invisible
    blocks = D.sym_zero_blocks(C.V.SITES)
    for u, v, i, j in sorted(maximal_support):
        D.sym_put(blocks, u, v, i, j,
                  D.p_var("x_%d%d_%d%d" % (u, v, i, j)))
    maximal_polynomials = []
    for values in WITNESS_WORDS:
        word = dict(zip(C.V.SITES, values))
        maximal_polynomials.append(
            D.sym_matching_sum(blocks, C.V.SITES, word)
        )
    require(tuple(maximal_polynomials) == expected,
            "an invisible extension altered a witness generator")
    maximal_records = [
        {"families": ["full_exactness"],
         "terms": [[list(monomial), str(coefficient)]
                   for monomial, coefficient in sorted(poly.items())]}
        for poly in maximal_polynomials
    ]
    maximal_names = tuple("x_%d%d_%d%d" % entry
                          for entry in sorted(maximal_support))
    maximal_witness_digest = saturation_certificate(
        maximal_records, maximal_names
    )
    rows = []
    for extension in EXTENSION_CELLS:
        require(extension not in base_support,
                "an m=11 extension was already in the m=10 support")
        support = frozenset(base_support | {extension})
        shadow = C.support_shadow_audit(support)
        records = C.coefficient_generators(support)
        support_names = tuple("x_%d%d_%d%d" % entry
                              for entry in sorted(support))
        witness_digest = saturation_certificate(records, support_names)
        family_counts = Counter(family for record in records
                                for family in record["families"])
        rows.append({
            "extension": list(extension),
            "localized_variables": len(support),
            "fibres_checked": shadow["fibres_checked"],
            "coefficient_generators": len(records),
            "generator_family_memberships": dict(sorted(family_counts.items())),
            "generator_sha256": D.content_hash(records),
            "three_witness_sha256": witness_digest,
            "ordinary_saturation_power": 3,
        })
    require(len(rows) == 6
            and len({row["three_witness_sha256"] for row in rows}) == 1,
            "the six extensions no longer share one binomial template")
    ledger = {
        "pinned_sources": PINNED,
        "m10_candidate_ledger_sha256": m10_digest,
        "m10_candidate_artifact_sha256": m10_ledger["artifact_sha256"],
        "semantic_supports": len(rows),
        "base_localized_variables": len(base_support),
        "maximal_witness_invisible_subcube": {
            "dimension": len(invisible),
            "off_Sigma_cells": sum(entry not in sigma for entry in invisible),
            "Sigma_cells": sum(entry in sigma for entry in invisible),
            "maximal_localization_variables": len(maximal_support),
            "invisible_cells": [list(entry) for entry in sorted(invisible)],
            "visible_boundary_cells": [
                list(entry) for entry in sorted(visible_boundary)
            ],
            "shared_three_witness_sha256": maximal_witness_digest,
            "conclusion": ("every subset of the 107 invisible cells "
                           "preserves the three-binomial U^3 certificate"),
        },
        "extension_rows": rows,
        "shared_identity": "a*h3-c*h1+d*h2=2*a*d*e",
        "characteristic_scope": "empty over every field of characteristic != 2",
        "status": "all six m=11 semantic extensions have empty localized ideals",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the six-extension closure ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 m=11 six coefficient supports: PASS (exact)")
    print("semantic supports:", ledger["semantic_supports"])
    print("shared identity:", ledger["shared_identity"])
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()

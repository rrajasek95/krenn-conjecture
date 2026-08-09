#!/usr/bin/env python3
"""Exact odd-circuit closure of the 159-cell O4 incidence frontier."""

from __future__ import annotations

import hashlib
import importlib
import itertools
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
    "verify_n8_d1_residue_orbit4_four_star_lemma.py":
        "cffd8ac0c5d54fddd365e4a610f2bed00881683a61733669e2bb41af972ecad1",
    "verify_n8_d1_m10_334_branch63_candidate.py":
        "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca",
    "verify_n8_d1_m10_334_branch63_ideal_closure.py":
        "884a453002824eb99fe4cda57f1adfbf14d64f636d91cef441b4721c63d96fe5",
}
for filename, expected in PINNED.items():
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned D1 coefficient source changed: " + filename)

F = importlib.import_module("verify_n8_d1_residue_orbit4_four_star_lemma")
K = importlib.import_module("verify_n8_d1_m10_334_branch63_ideal_closure")
C, D, V, O, S = F.C, F.D, F.V, F.O, F.S

EXPECTED_GENERATOR_SHA256 = (
    "63b95d63ff5cbffdce8f2644dc58b65112b7af6d586d515decbb90664f507461"
)
EXPECTED_LEDGER_SHA256 = (
    "670d1493b134d970766607d526e38a17eb20463c8ca9d14b391ec2a056042672"
)

# This is copied as exact input rather than imported from the evolving CEGAR
# driver.  Its order is the canonical cell order used in the frozen ledger.
FRONTIER_MISSING = (
    (0, 1, 0, 1), (0, 1, 1, 0), (0, 2, 1, 0), (0, 3, 0, 1),
    (0, 4, 0, 1), (0, 4, 1, 0), (0, 5, 0, 1), (0, 5, 1, 0),
    (0, 6, 0, 1), (0, 6, 1, 0),
    (0, 7, 0, 0), (0, 7, 0, 1), (0, 7, 1, 0), (0, 7, 1, 1),
    (1, 2, 0, 1), (1, 3, 1, 0),
    (1, 6, 0, 0), (1, 6, 0, 1), (1, 6, 1, 0), (1, 6, 1, 1),
    (1, 7, 0, 1), (1, 7, 1, 0),
    (2, 7, 0, 0), (2, 7, 0, 1), (2, 7, 1, 0), (2, 7, 1, 1),
    (2, 7, 2, 0), (2, 7, 2, 1),
    (3, 6, 0, 0), (3, 6, 0, 1), (3, 6, 1, 0), (3, 6, 1, 1),
    (3, 6, 2, 0), (3, 6, 2, 1),
)


def allowed_support():
    _state, _extras, _base, admissible, _stats = C.candidate_input()
    allowed = (set(admissible) - set(O.RESIDUE_HOLES)
               - set(S.BOUNDARY_OMISSIONS))
    require(len(allowed) == 193, "the O4 downset universe changed")
    return frozenset(allowed)


def monomial(*names):
    return tuple(sorted(names))


def monomial_product(*monomials):
    return tuple(sorted(name for factor in monomials for name in factor))


def monomial_poly(names, coefficient=1):
    return {tuple(sorted(names)): Fraction(coefficient)}


def cell_from_name(name):
    require(name.startswith("x_") and len(name) == 7,
            "a certificate variable has an unexpected name")
    return (int(name[2]), int(name[3]), int(name[5]), int(name[6]))


def name_from_cell(cell):
    return "x_%d%d_%d%d" % cell


def transform_cell(cell, site_permutation, colour_permutation):
    u, v, i, j = cell
    return V.cell(site_permutation[u], site_permutation[v],
                  colour_permutation[i], colour_permutation[j])


def transform_name(name, site_permutation, colour_permutation):
    return name_from_cell(transform_cell(
        cell_from_name(name), site_permutation, colour_permutation
    ))


def transform_polynomial(poly, site_permutation, colour_permutation):
    return {
        tuple(sorted(transform_name(name, site_permutation,
                                    colour_permutation)
                     for name in monomial)): coefficient
        for monomial, coefficient in poly.items()
    }


def certificate_data(records):
    a1 = monomial("x_05_11", "x_12_00", "x_37_01", "x_46_00")
    b1 = monomial("x_05_11", "x_14_00", "x_26_00", "x_37_01")
    # The middle generator is deliberately oriented opposite to artifact order.
    a2 = monomial("x_04_11", "x_15_00", "x_26_00", "x_37_01")
    b2 = monomial("x_04_11", "x_12_00", "x_37_01", "x_56_00")
    a3 = monomial("x_02_11", "x_14_00", "x_37_01", "x_56_00")
    b3 = monomial("x_02_11", "x_15_00", "x_37_01", "x_46_00")
    expected = (
        D.p_add(monomial_poly(a1), monomial_poly(b1)),
        D.p_add(monomial_poly(a2), monomial_poly(b2)),
        D.p_add(monomial_poly(a3), monomial_poly(b3)),
    )
    indices = tuple(next(index for index, record in enumerate(records)
                         if K.artifact_polynomial(record) == polynomial)
                    for polynomial in expected)
    require(indices == (3738, 3648, 2471),
            "the frozen odd-circuit record indices changed")
    require(all(records[index]["families"] == ["full_exactness"]
                for index in indices),
            "an odd-circuit record lost its full-output provenance")

    first_product = monomial_product(a1, a2, a3)
    second_product = monomial_product(b1, b2, b3)
    require(first_product == second_product,
            "the oriented odd-circuit exponent sum does not vanish")
    generators = expected
    cofactors = (
        monomial_poly(monomial_product(a2, a3)),
        monomial_poly(monomial_product(b1, a3), -1),
        monomial_poly(monomial_product(b1, b2)),
    )
    compact = D.p_const(0)
    for cofactor, generator in zip(cofactors, generators):
        compact = D.p_add(compact, D.p_mul(cofactor, generator))
    require(compact == monomial_poly(first_product, 2),
            "the compact three-binomial identity failed")
    return indices, generators, cofactors, first_product


def clause_audit():
    """Return the support-faithful face clause for the evolving CEGAR."""
    allowed = allowed_support()
    support = allowed - set(FRONTIER_MISSING)
    records = C.coefficient_generators(support)
    indices, _generators, _cofactors, product = certificate_data(records)
    witnesses = tuple(sorted({cell_from_name(name) for name in product}))
    require(len(witnesses) == 10 and set(witnesses) <= support,
            "the odd-circuit localization witnesses changed")
    require(set(FRONTIER_MISSING).isdisjoint(witnesses),
            "a certificate witness is also a face omission")
    return {
        "positive_cells": [list(cell) for cell in FRONTIER_MISSING],
        "negative_cells": [list(cell) for cell in witnesses],
        "record_indices": list(indices),
    }


def transported_clause_audit():
    """Enumerate all site/colour automorphism transports of the face clause."""
    allowed = allowed_support()
    actions = []
    for site_permutation in itertools.permutations(V.SITES):
        for colour_permutation in itertools.permutations(V.COLORS):
            image = {
                transform_cell(cell, site_permutation, colour_permutation)
                for cell in allowed
            }
            if image == set(allowed):
                actions.append((site_permutation, colour_permutation))
    require(len(actions) == 8,
            "the O4 allowed-universe automorphism census changed")

    base = clause_audit()
    positive = {tuple(cell) for cell in base["positive_cells"]}
    negative = {tuple(cell) for cell in base["negative_cells"]}
    clauses = {}
    for site_permutation, colour_permutation in actions:
        transported_positive = tuple(sorted(
            transform_cell(cell, site_permutation, colour_permutation)
            for cell in positive
        ))
        transported_negative = tuple(sorted(
            transform_cell(cell, site_permutation, colour_permutation)
            for cell in negative
        ))
        key = transported_positive, transported_negative
        clauses.setdefault(key, []).append({
            "site_permutation": list(site_permutation),
            "colour_permutation": list(colour_permutation),
        })
    require(len(clauses) == 4,
            "the distinct odd-circuit clause orbit changed")
    return [{
        "positive_cells": [list(cell) for cell in key[0]],
        "negative_cells": [list(cell) for cell in key[1]],
        "transport_actions": actions_for_clause,
    } for key, actions_for_clause in sorted(clauses.items())]


def audit():
    started = monotonic()
    allowed = allowed_support()
    support = allowed - set(FRONTIER_MISSING)
    require(len(support) == 159, "the frozen incidence frontier changed")
    shadow = C.support_shadow_audit(support)
    records = C.coefficient_generators(support)
    require(len(records) == 4318, "the frontier generator census changed")
    generator_digest = D.content_hash(records)
    require(generator_digest == EXPECTED_GENERATOR_SHA256,
            "the frozen frontier coefficient input changed")
    indices, generators, cofactors, first_product = certificate_data(records)

    support_names = tuple("x_%d%d_%d%d" % cell for cell in sorted(support))
    require(set(first_product) <= set(support_names),
            "the compact identity uses a nonlocalized cell")
    multiplicities = Counter(first_product)
    saturation_power = max(multiplicities.values())
    require(saturation_power == 3,
            "the frozen ordinary saturation exponent changed")
    u_power = tuple(sorted(name for name in support_names
                           for _repeat in range(saturation_power)))
    quotient = K.monomial_quotient(
        u_power, first_product, Fraction(1, 2)
    )
    ordinary = D.p_const(0)
    for cofactor, generator in zip(cofactors, generators):
        ordinary = D.p_add(
            ordinary,
            D.p_mul(D.p_mul(quotient, cofactor), generator),
        )
    require(ordinary == monomial_poly(u_power),
            "the ordinary U^3 saturation certificate failed")

    # Independently reconstruct every distinct automorphism transport.  Each
    # renamed generator must still be an actual full-output equation of its
    # transported face; the saturation identity then follows by renaming.
    transported_clauses = transported_clause_audit()
    transported_rows = []
    for row in transported_clauses:
        positive = {tuple(cell) for cell in row["positive_cells"]}
        transported_support = allowed - positive
        require(set(tuple(cell) for cell in row["negative_cells"])
                <= transported_support,
                "a transported localization witness is missing")
        transported_records = C.coefficient_generators(transported_support)
        available = {C.polynomial_key(K.artifact_polynomial(record))
                     for record in transported_records
                     if record["families"] == ["full_exactness"]}
        action = row["transport_actions"][0]
        transported_generators = [transform_polynomial(
            generator, action["site_permutation"],
            action["colour_permutation"]
        ) for generator in generators]
        require(all(C.polynomial_key(generator) in available
                    for generator in transported_generators),
                "a transported odd-circuit generator is not a full equation")
        transported_rows.append({
            "positive_cells": row["positive_cells"],
            "negative_cells": row["negative_cells"],
            "transport_actions": row["transport_actions"],
            "coefficient_generators": len(transported_records),
            "generator_sha256": D.content_hash(transported_records),
        })

    clause = clause_audit()
    witness_names = sorted({name for name in first_product})
    mutual_arc_cells = {
        V.cell(0, 1, 0, 0), V.cell(0, 1, 1, 1),
        V.cell(6, 7, 2, 2),
    }
    witness_cells = {cell_from_name(name) for name in witness_names}
    ledger = {
        "pinned_sources": PINNED,
        "allowed_cells": len(allowed),
        "frontier_cells": len(support),
        "frontier_shadow": shadow,
        "frontier_generators": len(records),
        "frontier_generator_sha256": generator_digest,
        "full_output_record_indices": list(indices),
        "compact_identity": (
            "(a1+b1)a2a3-b1(a2+b2)a3+b1b2(a3+b3)=2a1a2a3"
        ),
        "compact_monomial_degree": len(first_product),
        "localized_witness_variables": witness_names,
        "ordinary_saturation_power": saturation_power,
        "ordinary_certificate": "U^3 lies in the three-generator ideal",
        "characteristic_scope": "empty over every field of characteristic != 2",
        "support_faithful_clause": clause,
        "allowed_universe_automorphisms": 8,
        "distinct_transported_clauses": transported_rows,
        "supported_only_on_mutual_arc_cells":
            witness_cells <= mutual_arc_cells,
        "status": "exact coefficient-empty O4 incidence frontier",
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256: %s" % digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the frozen odd-circuit ledger changed")
        print("ledger sha256 (frozen): %s" % digest)
    print("records:", ledger["full_output_record_indices"])
    print("ordinary saturation: U^%d" % ledger["ordinary_saturation_power"])
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Three-binomial ordinary saturation on the fourth O4 incidence face."""

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


PINNED_ODD_ENGINE_SHA256 = (
    "95f75391b40d9e006b4580cf2fa5e34e4930ec87facb7bef5391b419af2c3507"
)
SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_incidence_frontier_odd_circuit.py"
)
with open(SOURCE, "rb") as handle:
    source_digest = hashlib.sha256(handle.read()).hexdigest()
require(source_digest == PINNED_ODD_ENGINE_SHA256,
        "the pinned O4 odd-circuit engine changed")
Q = importlib.import_module(
    "verify_n8_d1_residue_orbit4_incidence_frontier_odd_circuit"
)
C, D, K = Q.C, Q.D, Q.K

EXPECTED_GENERATOR_SHA256 = (
    "39314ce73473ee35d02ce4a0dfd0ea586c4cb6f54c2a1b727c2ad76dfad6814f"
)
EXPECTED_LEDGER_SHA256 = (
    "3532d3ed2384dbfd4afe90ea32d4224eb2b0ccdcadef15999a54171220ed9b2b"
)

FRONTIER_MISSING = (
    (0, 1, 0, 1), (0, 1, 1, 0), (0, 3, 0, 1),
    (0, 6, 0, 0), (0, 6, 0, 1), (0, 6, 1, 0), (0, 6, 1, 1),
    (0, 7, 0, 1), (0, 7, 1, 0),
    (1, 2, 0, 1), (1, 2, 1, 0), (1, 3, 1, 0),
    (1, 4, 0, 1), (1, 4, 1, 0), (1, 5, 0, 1), (1, 5, 1, 0),
    (1, 6, 0, 1), (1, 6, 1, 0),
    (1, 7, 0, 0), (1, 7, 0, 1), (1, 7, 1, 0), (1, 7, 1, 1),
    (2, 6, 0, 0), (2, 6, 0, 1), (2, 6, 1, 0), (2, 6, 1, 1),
    (2, 6, 2, 0), (2, 6, 2, 1),
    (3, 7, 0, 0), (3, 7, 0, 1), (3, 7, 1, 0), (3, 7, 1, 1),
    (3, 7, 2, 0), (3, 7, 2, 1),
)


def monomial(*names):
    return tuple(sorted(names))


def monomial_product(*monomials):
    return tuple(sorted(name for factor in monomials for name in factor))


def monomial_poly(names, coefficient=1):
    return {tuple(sorted(names)): Fraction(coefficient)}


def certificate_input():
    support = Q.allowed_support() - set(FRONTIER_MISSING)
    require(len(support) == 159,
            "the fourth incidence frontier changed size")
    records = C.coefficient_generators(support)
    require(len(records) == 4317
            and D.content_hash(records) == EXPECTED_GENERATOR_SHA256,
            "the fourth incidence coefficient input changed")

    a1 = monomial("x_04_00", "x_13_11", "x_27_01", "x_56_00")
    b1 = monomial("x_05_00", "x_13_11", "x_27_01", "x_46_00")
    a2 = monomial("x_03_00", "x_15_11", "x_27_01", "x_46_00")
    b2 = monomial("x_04_00", "x_15_11", "x_27_01", "x_36_00")
    # The third row is used with reversed Laurent orientation.
    a3 = monomial("x_05_00", "x_14_11", "x_27_01", "x_36_00")
    b3 = monomial("x_03_00", "x_14_11", "x_27_01", "x_56_00")
    generators = (
        D.p_add(monomial_poly(a1), monomial_poly(b1)),
        D.p_add(monomial_poly(a2), monomial_poly(b2)),
        D.p_add(monomial_poly(a3), monomial_poly(b3)),
    )
    indices = tuple(next(index for index, record in enumerate(records)
                         if K.artifact_polynomial(record) == generator)
                    for generator in generators)
    require(indices == (3276, 2598, 2496),
            "the fourth incidence circuit records changed")
    require(all(records[index]["families"] == ["full_exactness"]
                for index in indices),
            "a circuit row lost its full-output provenance")

    first_product = monomial_product(a1, a2, a3)
    require(first_product == monomial_product(b1, b2, b3),
            "the fourth incidence odd circuit does not close")
    cofactors = (
        monomial_poly(monomial_product(a2, a3)),
        monomial_poly(monomial_product(b1, a3), -1),
        monomial_poly(monomial_product(b1, b2)),
    )
    compact = D.p_const(0)
    for cofactor, generator in zip(cofactors, generators):
        compact = D.p_add(compact, D.p_mul(cofactor, generator))
    require(compact == monomial_poly(first_product, 2),
            "the fourth incidence compact odd identity failed")

    support_names = tuple("x_%d%d_%d%d" % cell for cell in sorted(support))
    require(set(first_product) <= set(support_names),
            "an odd-circuit monomial variable is not localized")
    saturation_power = max(Counter(first_product).values())
    require(saturation_power == 3,
            "the fourth incidence saturation exponent changed")
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
            "the fourth incidence ordinary U^3 identity failed")
    witnesses = tuple(sorted({Q.cell_from_name(name)
                              for name in first_product}))
    require(len(witnesses) == 10 and set(witnesses) <= support,
            "the fourth incidence circuit witnesses changed")
    return support, records, indices, first_product, witnesses


def transform_clauses(positive, negative):
    allowed = Q.allowed_support()
    clauses = {}
    actions = 0
    for site_permutation in itertools.permutations(Q.V.SITES):
        for colour_permutation in itertools.permutations(Q.V.COLORS):
            if {Q.transform_cell(cell, site_permutation, colour_permutation)
                for cell in allowed} != set(allowed):
                continue
            actions += 1
            transported_positive = tuple(sorted(
                Q.transform_cell(cell, site_permutation, colour_permutation)
                for cell in positive
            ))
            transported_negative = tuple(sorted(
                Q.transform_cell(cell, site_permutation, colour_permutation)
                for cell in negative
            ))
            clauses.setdefault(
                (transported_positive, transported_negative), 0
            )
            clauses[(transported_positive, transported_negative)] += 1
    require(actions == 8,
            "the O4 automorphism census changed")
    return [{
        "positive_cells": [list(cell) for cell in positive_cells],
        "negative_cells": [list(cell) for cell in negative_cells],
        "transport_multiplicity": multiplicity,
    } for (positive_cells, negative_cells), multiplicity
        in sorted(clauses.items())]


def clause_audit():
    _support, _records, indices, _product, witnesses = certificate_input()
    return {
        "positive_cells": [list(cell) for cell in FRONTIER_MISSING],
        "negative_cells": [list(cell) for cell in witnesses],
        "source_records": list(indices),
    }


def transported_clause_audit():
    _support, _records, _indices, _product, witnesses = certificate_input()
    return transform_clauses(set(FRONTIER_MISSING), set(witnesses))


def audit():
    started = monotonic()
    support, records, indices, product, witnesses = certificate_input()
    shadow = C.support_shadow_audit(support)
    transported = transform_clauses(set(FRONTIER_MISSING), set(witnesses))
    ledger = {
        "pinned_odd_engine_sha256": source_digest,
        "localized_cells": len(support),
        "complete_shadow": shadow,
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "full_output_record_indices": list(indices),
        "compact_identity": (
            "(a1+b1)a2a3-b1(a2+b2)a3+b1b2(a3+b3)=2a1a2a3"
        ),
        "compact_monomial_degree": len(product),
        "localized_source_witnesses": [list(cell) for cell in witnesses],
        "ordinary_saturation_power": 3,
        "distinct_transported_clauses": transported,
        "characteristic_scope": "every characteristic except two",
        "status": "fourth 159-cell O4 incidence frontier is coefficient-empty",
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the fourth-incidence odd-circuit ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("records:", ledger["full_output_record_indices"])
    print("ordinary saturation: U^3")
    print("transported clauses:", len(ledger["distinct_transported_clauses"]))
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()

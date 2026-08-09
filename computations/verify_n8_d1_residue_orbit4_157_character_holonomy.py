#!/usr/bin/env python3
"""Exact character-holonomy obstruction on the first 157-cell O4 face."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import importlib
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED = {
    "verify_n8_d1_residue_orbit4_158_direct_batch.py":
        "8bed466723fe37da34136f4c10f5d49e866984effddcb69b56dbdf0bbde6335e",
    "verify_n8_d1_residue_orbit4_158_second_layer_collision.py":
        "5c47e1e72874afcc70ae7e4646e9f20acb2ba3a51a6b36c9451cc24ed1a0c4fa",
    "verify_n8_d1_residue_orbit4_158_character_graph_batch2.py":
        "e31e396c8441bcf08f4bd0f91f8a690fd9315a7c415d1788a8a1c5631b061405",
}
for filename, expected in PINNED.items():
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned 157-cell character source changed: " + filename)

B = importlib.import_module("verify_n8_d1_residue_orbit4_158_direct_batch")
X = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_second_layer_collision"
)
H = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_character_graph_batch2"
)
E, Q, C, D = B.E, B.Q, B.C, B.D

MISSING = (
    (0, 1, 1, 0), (0, 2, 1, 0), (0, 3, 0, 1),
    (0, 6, 0, 0), (0, 6, 0, 1), (0, 6, 1, 0), (0, 6, 1, 1),
    (0, 7, 0, 1), (0, 7, 0, 2), (0, 7, 1, 0),
    (1, 2, 0, 1), (1, 3, 1, 0), (1, 3, 1, 2),
    (1, 4, 0, 1), (1, 4, 1, 0),
    (1, 5, 0, 1), (1, 5, 1, 0),
    (1, 6, 0, 1), (1, 6, 1, 0),
    (1, 7, 0, 0), (1, 7, 0, 1), (1, 7, 1, 0), (1, 7, 1, 1),
    (2, 6, 0, 0), (2, 6, 0, 1), (2, 6, 1, 0), (2, 6, 1, 1),
    (2, 6, 2, 0), (2, 6, 2, 1), (2, 7, 2, 0),
    (3, 7, 0, 0), (3, 7, 0, 1), (3, 7, 1, 0), (3, 7, 1, 1),
    (3, 7, 2, 0), (3, 7, 2, 1),
)
GENERATOR_SHA256 = (
    "45f70f0cb4b3e9e322861b220e2ff4290469ac4bdfe87808f2a0a45df6d8fd27"
)
REDUCED_HISTOGRAM_SHA256 = (
    "d3cd2bf42f252ece6a2744c314f363f3730569a612cd90425497dded3f59c78c"
)
DERIVED_RECORDS_AND_CHARACTERS = (
    (114, "1"),
    (2201, "1"), (2202, "1"), (2203, "1"),
    (2207, "1"), (2208, "1"), (2209, "1"),
    (2213, "1"), (2214, "1"), (2215, "1"),
    (2626, "-1"), (2713, "1"), (2783, "-1"), (2870, "1"),
    (2940, "-1"), (3027, "1"),
    (3066, "1"), (3069, "1"), (3072, "1"),
    (3156, "1"), (3159, "1"), (3162, "1"),
    (3246, "1"), (3249, "1"), (3252, "1"),
)
ODD_DEPENDENCIES = (
    {83: 1, 82: -1},
    {85: 1, 84: -1},
    {87: 1, 86: -1},
)
REPAIR_CELLS = (
    (0, 1, 1, 0), (0, 6, 1, 0), (0, 6, 1, 1), (0, 7, 1, 0),
    (1, 4, 0, 1), (1, 5, 0, 1), (1, 6, 0, 1),
    (1, 7, 0, 0), (3, 7, 0, 0),
)
EXPECTED_LEDGER_SHA256 = (
    "a4e332f4f5562a97412742f2a86968b57a2b99f5c78d67fde9ee15f43c8abad0"
)


def normalized_derived_relation(records, rows, basis, base_relations,
                                record_index, reduced, traces):
    certificate = X.reduced_certificate(
        records, rows, basis, base_relations,
        record_index, reduced, traces,
    )
    (first, first_coefficient), (second, second_coefficient) = sorted(
        reduced.items()
    )
    difference = E.exponent_difference(first, second)
    constant = -second_coefficient / first_coefficient
    certificate = E.certificate_mul(
        certificate,
        E.laurent_monomial(
            E.exponent_scale(second, -1),
            Fraction(1, first_coefficient),
        ),
    )
    integral_difference = tuple(sorted(
        (name, exponent.numerator)
        for name, exponent in difference.items()
    ))
    expected = E.laurent_add(
        E.laurent_monomial(integral_difference),
        E.laurent_monomial((), -constant),
    )
    require(E.evaluate_certificate(certificate, records) == expected,
            "a derived character relation failed source reconstruction")
    return {
        "difference": integral_difference,
        "constant": constant,
        "certificate": certificate,
    }


def certificate_input():
    support = Q.allowed_support() - set(MISSING)
    records = C.coefficient_generators(support)
    require(len(support) == 157 and len(records) == 4105
            and D.content_hash(records) == GENERATOR_SHA256,
            "the first 157-cell coefficient input changed")
    rows = B.initial_rows(records)
    basis, dependencies = E.L.integer_laurent_basis(rows)
    require(len(rows) == 72 and len(basis) == 25
            and len(dependencies) == 47
            and all(E.row_character(dependency, rows) == 1
                    for dependency in dependencies),
            "the first 157-cell initial character changed")
    basis_characters = {
        pivot: E.row_character(representation, rows)
        for pivot, (_basis_row, representation) in basis.items()
    }
    seen = {E.canonical_row(row["difference"], row["constant"])
            for row in rows}
    base_relations = X.base_relations(records, rows)
    derived_rows = []
    derived_relations = []
    histogram = Counter()
    for record_index, record in enumerate(records):
        reduced, traces, _parents = E.reduce_record(
            record, basis, basis_characters
        )
        histogram[len(reduced)] += 1
        if len(reduced) != 2:
            continue
        (first, first_coefficient), (second, second_coefficient) = sorted(
            reduced.items()
        )
        difference = E.exponent_difference(first, second)
        constant = -second_coefficient / first_coefficient
        key = E.canonical_row(difference, constant)
        if key in seen:
            continue
        seen.add(key)
        relation = normalized_derived_relation(
            records, rows, basis, base_relations,
            record_index, reduced, traces,
        )
        derived_rows.append({
            "difference": difference,
            "constant": constant,
            "source_record": record_index,
        })
        derived_relations.append(relation)
    require(D.content_hash({str(classes): count
                            for classes, count in sorted(histogram.items())})
            == REDUCED_HISTOGRAM_SHA256,
            "the first 157-cell reduced histogram changed")
    require(tuple((row["source_record"], str(row["constant"]))
                  for row in derived_rows)
            == DERIVED_RECORDS_AND_CHARACTERS,
            "the 157-cell derived character rows changed")

    augmented_rows = rows + derived_rows
    augmented_relations = base_relations + derived_relations
    augmented_basis, augmented_dependencies = E.L.integer_laurent_basis(
        augmented_rows
    )
    bad = [dependency for dependency in augmented_dependencies
           if E.row_character(dependency, augmented_rows) != 1]
    require(len(augmented_rows) == 97 and len(augmented_basis) == 39
            and len(augmented_dependencies) == 58
            and bad == list(ODD_DEPENDENCIES),
            "the three 157-cell character holonomies changed")

    relations = [E.relation_from_representation(
        dependency, augmented_relations
    ) for dependency in bad]
    require(all(relation["difference"] == ()
                and relation["constant"] == -1
                and E.evaluate_certificate(relation["certificate"], records)
                    == E.laurent_monomial((), 2)
                for relation in relations),
            "an odd dependency failed ordinary-source expansion")
    ordinary = X.clear_to_saturation(
        relations[0]["certificate"], E.laurent_monomial((), 2),
        support, records,
    )
    require(ordinary == {
        "source_records": [
            2497, 2498, 2499, 2500, 2501, 2502, 2506,
            2626, 2713, 3339, 3342, 3345, 3444,
        ],
        "laurent_cofactor_terms": 43,
        "clearing_monomial": [
            ["x_02_22", 1], ["x_05_11", 1], ["x_05_12", 1],
            ["x_13_00", 1], ["x_13_22", 1], ["x_14_00", 1],
            ["x_15_00", 1], ["x_27_00", 1], ["x_36_01", 1],
            ["x_46_00", 1], ["x_46_11", 1], ["x_47_02", 2],
            ["x_47_12", 1], ["x_56_00", 1], ["x_56_01", 1],
            ["x_56_10", 1], ["x_57_12", 1], ["x_57_22", 1],
        ],
        "ordinary_saturation_power": 2,
        "ordinary_cofactor_terms": 43,
        "ordinary_certificate_sha256":
            "dd8159e05eff587d4b6d47886f1363f9faef141b3e8a74556ba8413f8fa43bbd",
        "integral_coefficients": False,
    }, "the selected 157-cell ordinary U^2 certificate changed")
    witnesses = E.source_witnesses(
        records, tuple(ordinary["source_records"])
    )
    require(len(witnesses) == 27 and set(witnesses) <= support,
            "a selected 157-cell source witness changed")
    masks = H.minimal_repair_masks(
        records, ordinary["source_records"], support
    )
    require(masks == frozenset({frozenset((cell,))
                                for cell in REPAIR_CELLS}),
            "the selected 157-cell singleton repair chart changed")
    return (support, records, rows, derived_rows, bad, ordinary,
            witnesses, masks)


def transported_clause_audit():
    *_, witnesses, _masks = certificate_input()
    return E.transform_clauses(set(REPAIR_CELLS), set(witnesses))


def audit():
    started = monotonic()
    (support, records, rows, derived_rows, bad, ordinary,
     witnesses, masks) = certificate_input()
    transported = transported_clause_audit()
    require(len(transported) == 8,
            "the 157-cell repair-chart transport orbit changed")
    ledger = {
        "pinned_sources": PINNED,
        "localized_cells": len(support),
        "complete_shadow": C.support_shadow_audit(support),
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "initial_character": {
            "rows": len(rows), "rank": 25, "dependencies": 47,
            "inconsistent_dependencies": 0,
        },
        "reduced_histogram_sha256": REDUCED_HISTOGRAM_SHA256,
        "derived_two_class_rows": len(derived_rows),
        "augmented_character": {
            "rows": 97, "rank": 39, "dependencies": 58,
            "odd_dependencies": bad,
        },
        "ordinary_saturation_certificate": ordinary,
        "localized_source_witnesses": [list(cell) for cell in witnesses],
        "minimal_repair_masks": [
            [list(cell) for cell in sorted(mask)]
            for mask in sorted(masks, key=lambda row: tuple(sorted(row)))
        ],
        "distinct_transported_clauses": transported,
        "characteristic_scope": "every characteristic except two",
        "status": (
            "first 157-cell face is empty by exact two-class character "
            "holonomy; selected identity persists on a nine-cell repair chart"
        ),
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the 157-cell character-holonomy ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("odd dependencies:", len(ledger[
        "augmented_character"
    ]["odd_dependencies"]))
    print("ordinary saturation: U^%d" % ledger[
        "ordinary_saturation_certificate"
    ]["ordinary_saturation_power"])
    print("singleton repair masks:", len(ledger["minimal_repair_masks"]))
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()

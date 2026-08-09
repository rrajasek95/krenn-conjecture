#!/usr/bin/env python3
"""Exact first-resultant frontier on the torus-consistent 157-cell O4 face."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import importlib
import itertools
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
    "verify_n8_d1_residue_orbit4_157_torus_frontier.py":
        "486be2645282012340d25c28483db3c5986abb5d2a60110216df5e5b1cfe5909",
    "verify_n8_d1_residue_orbit4_157_character_holonomy.py":
        "0214709f908cb095e9a78ce597d45326b96a517d7cb5379c6911e500a097693e",
    "verify_n8_d1_residue_orbit4_158_second_layer_collision.py":
        "5c47e1e72874afcc70ae7e4646e9f20acb2ba3a51a6b36c9451cc24ed1a0c4fa",
}
for filename, expected in PINNED.items():
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned resultant-frontier source changed: " + filename)

T = importlib.import_module(
    "verify_n8_d1_residue_orbit4_157_torus_frontier"
)
H = importlib.import_module(
    "verify_n8_d1_residue_orbit4_157_character_holonomy"
)
X = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_second_layer_collision"
)
E, Q, C, D = T.E, T.Q, T.C, T.D

SELECTED_TRINOMIALS = (2381, 2810, 3569, 3596)
RESULTANT_CERTIFICATE_SHA256 = {
    (2381, 2810):
        "73c7fa507b95697c2c4560d0aa72ffb6689c46d91661e732b8d7ca1d0d34e7cf",
    (2381, 3569):
        "301e0146069aa69324d804dd89a0d14c59efa0b567afb23f549804da137faa16",
    (2381, 3596):
        "164ea2bdcaff340c5162ed9a2ccb961ddce9ad90aec8c669ebb172414fb34122",
    (2810, 3569):
        "612126ac712fd987b502f7125334a62c9bfc98558a78d250edfb2f22cd02b0fb",
    (2810, 3596):
        "c6967d4ed6dd4ffa6adfc0e227654907dbcedf5cf07d00a015bba7d10e255133",
    (3569, 3596):
        "9eda3df6079fe65a5b95b34a586b867730379b2778f15514d7bdd8c547206049",
}
EXTENDED_PARAMETRIZATION_SHA256 = (
    "17a99d19d47b4a5400b969bf03332cedd4168069522c04feb58d37b3ef374432"
)
RESIDUAL_HISTOGRAM_SHA256 = (
    "fc4a9354c560e83eccc89e5062f16f1f44f7236e7251ed51db86c329636b3a83"
)
RESIDUAL_IDEAL_SHA256 = (
    "47e42c702626087533e538c21e2fc72ed7a5fc2187de414ab581a300b5d564ea"
)
ACTIVE_DIFFERENCE_ROWS_SHA256 = (
    "2351c25c098f726a3464dad8f6b79463164163ac293d6d85ddc8eeebf9a988cb"
)
ACTIVE_DIFFERENCE_BASIS_SHA256 = (
    "877582e7989cdb04cb2a30cfda95ae39c68a67c6b8441d96512741a3e86ee334"
)
EXPECTED_LEDGER_SHA256 = (
    "c80555e585d60739a9809404726251ce7a983175746b45a4c4d915991b6c18a0"
)


def native_character_system(records):
    rows = T.B.initial_rows(records)
    basis, dependencies = E.L.integer_laurent_basis(rows)
    require(len(rows) == 72 and len(basis) == 25
            and len(dependencies) == 47
            and all(E.row_character(dependency, rows) == 1
                    for dependency in dependencies),
            "the resultant frontier initial character changed")
    basis_characters = {
        pivot: E.row_character(representation, rows)
        for pivot, (_basis_row, representation) in basis.items()
    }
    seen = {E.canonical_row(row["difference"], row["constant"])
            for row in rows}
    base_relations = X.base_relations(records, rows)
    derived_rows = []
    derived_relations = []
    for record_index, record in enumerate(records):
        reduced, traces, _parents = E.reduce_record(
            record, basis, basis_characters
        )
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
        relation = H.normalized_derived_relation(
            records, rows, basis, base_relations,
            record_index, reduced, traces,
        )
        derived_rows.append({
            "difference": difference,
            "constant": constant,
            "source_record": record_index,
        })
        derived_relations.append(relation)
    require(tuple(row["source_record"] for row in derived_rows)
            == T.DERIVED_RECORDS,
            "the native two-class character rows changed")
    augmented_rows = rows + derived_rows
    augmented_relations = base_relations + derived_relations
    augmented_basis, augmented_dependencies = E.L.integer_laurent_basis(
        augmented_rows
    )
    require(len(augmented_rows) == 91 and len(augmented_basis) == 36
            and len(augmented_dependencies) == 55
            and all(E.row_character(dependency, augmented_rows) == 1
                    for dependency in augmented_dependencies),
            "the native two-class torus changed")
    return augmented_rows, augmented_relations, augmented_basis


def selected_trinomial_certificates(records, rows, relations, basis):
    basis_characters = {
        pivot: E.row_character(representation, rows)
        for pivot, (_basis_row, representation) in basis.items()
    }
    selected = {}
    for record_index in SELECTED_TRINOMIALS:
        reduced, traces, _parents = E.reduce_record(
            records[record_index], basis, basis_characters
        )
        require(len(reduced) == 3,
                "a selected resultant source stopped being trinomial")
        certificate = X.reduced_certificate(
            records, rows, basis, relations,
            record_index, reduced, traces,
        )
        selected[record_index] = (reduced, certificate)
    return selected


def pair_resultant(records, selected, first_index, second_index):
    first, first_certificate = selected[first_index]
    second, second_certificate = selected[second_index]
    candidates = []
    for first_monomial, first_coefficient in sorted(first.items()):
        for second_monomial, second_coefficient in sorted(second.items()):
            shift = E.exponent_add(
                first_monomial,
                E.exponent_scale(second_monomial, -1),
            )
            scale = first_coefficient / second_coefficient
            residual = E.laurent_add(
                first,
                E.laurent_mul(
                    second, E.laurent_monomial(shift, scale)
                ),
                -1,
            )
            if len(residual) != 2:
                continue
            certificate = E.certificate_add(
                first_certificate,
                E.certificate_mul(
                    second_certificate,
                    E.laurent_monomial(shift, scale),
                ),
                -1,
            )
            require(E.evaluate_certificate(certificate, records) == residual,
                    "a trinomial resultant failed source reconstruction")
            candidates.append((
                E.polynomial_trace(residual), shift, scale,
                residual, certificate,
            ))
    candidates.sort(key=lambda row: repr((row[0], row[1], row[2])))
    require(len(candidates) == 2,
            "a selected trinomial pair changed its cancellation census")
    _trace, shift, scale, residual, certificate = candidates[0]
    (first_monomial, first_coefficient), (
        second_monomial, second_coefficient,
    ) = sorted(residual.items())
    difference = E.exponent_difference(first_monomial, second_monomial)
    constant = -second_coefficient / first_coefficient
    normalized_certificate = E.certificate_mul(
        certificate,
        E.laurent_monomial(
            E.exponent_scale(second_monomial, -1),
            Fraction(1, first_coefficient),
        ),
    )
    integral_difference = tuple(sorted(
        (name, exponent.numerator)
        for name, exponent in difference.items()
    ))
    require(E.evaluate_certificate(normalized_certificate, records)
            == E.laurent_add(
                E.laurent_monomial(integral_difference),
                E.laurent_monomial((), -constant),
            ), "a normalized resultant binomial failed")
    pair = (first_index, second_index)
    require(constant == 1
            and D.content_hash(E.certificate_trace(normalized_certificate))
                == RESULTANT_CERTIFICATE_SHA256[pair],
            "a selected resultant certificate changed")
    return ({
        "difference": difference,
        "constant": constant,
        "source_record": -1,
        "source_pair": pair,
    }, {
        "difference": integral_difference,
        "constant": constant,
        "certificate": normalized_certificate,
    }, {
        "source_pair": list(pair),
        "aligning_monomial": [[name, exponent]
                               for name, exponent in shift],
        "aligning_scalar": str(scale),
        "normalized_certificate_sha256":
            RESULTANT_CERTIFICATE_SHA256[pair],
        "source_records": sorted(normalized_certificate),
        "laurent_cofactor_terms": sum(
            len(polynomial) for polynomial in normalized_certificate.values()
        ),
    })


def pair_cancellation_census(trinomials, existing_rows):
    existing_keys = {
        E.canonical_row(row["difference"], row["constant"])
        for row in existing_rows
    }
    zero = 0
    binomial = 0
    new_keys = set()
    for (_first_index, first), (_second_index, second) in itertools.combinations(
            trinomials, 2):
        for first_monomial, first_coefficient in sorted(first.items()):
            for second_monomial, second_coefficient in sorted(second.items()):
                shift = E.exponent_add(
                    first_monomial,
                    E.exponent_scale(second_monomial, -1),
                )
                scale = first_coefficient / second_coefficient
                residual = E.laurent_add(
                    first,
                    E.laurent_mul(
                        second, E.laurent_monomial(shift, scale)
                    ),
                    -1,
                )
                if not residual:
                    zero += 1
                elif len(residual) == 2:
                    binomial += 1
                    (a, ca), (b, cb) = sorted(residual.items())
                    key = E.canonical_row(
                        E.exponent_difference(a, b), -cb / ca
                    )
                    if key not in existing_keys:
                        new_keys.add(key)
    return {
        "laurent_shift_equalities": zero,
        "binomial_cancellations": binomial,
        "new_character_rows": len(new_keys),
    }


def frontier_input():
    support = Q.allowed_support() - set(T.MISSING)
    records = C.coefficient_generators(support)
    require(len(support) == 157 and len(records) == 4321
            and D.content_hash(records) == T.GENERATOR_SHA256,
            "the resultant-frontier coefficient input changed")
    rows, relations, basis = native_character_system(records)
    selected = selected_trinomial_certificates(
        records, rows, relations, basis
    )
    resultants = []
    resultant_relations = []
    resultant_trace = []
    for first_index, second_index in itertools.combinations(
            SELECTED_TRINOMIALS, 2):
        row, relation, trace = pair_resultant(
            records, selected, first_index, second_index
        )
        resultants.append(row)
        resultant_relations.append(relation)
        resultant_trace.append(trace)
    extended_rows = rows + resultants
    extended_relations = relations + resultant_relations
    extended_basis, extended_dependencies = E.L.integer_laurent_basis(
        extended_rows
    )
    require(len(extended_rows) == 97 and len(extended_basis) == 39
            and len(extended_dependencies) == 58
            and all(E.row_character(dependency, extended_rows) == 1
                    for dependency in extended_dependencies),
            "the resultant-extended character system changed")
    parametrization = T.complete_parametrization(
        extended_basis, extended_rows
    )
    require(D.content_hash(parametrization)
            == EXTENDED_PARAMETRIZATION_SHA256,
            "the extended Laurent parametrization changed")
    support_names = {"x_%d%d_%d%d" % cell for cell in support}
    free_parameters = sorted(support_names - set(extended_basis))
    require(len(free_parameters) == 118,
            "the resultant torus dimension changed")

    basis_characters = {
        pivot: E.row_character(representation, extended_rows)
        for pivot, (_basis_row, representation) in extended_basis.items()
    }
    histogram = Counter()
    residual_ideal = []
    trinomials = []
    active_rows = []
    active_seen = set()
    terminal = None
    unit_circle_obstruction = None
    for record_index, record in enumerate(records):
        reduced, traces, parents = E.reduce_record(
            record, extended_basis, basis_characters
        )
        histogram[len(reduced)] += 1
        if reduced:
            residual_ideal.append([record_index, E.polynomial_trace(reduced)])
        if len(reduced) >= 3:
            monomials = sorted(reduced)
            base_monomial = monomials[0]
            for monomial in monomials[1:]:
                difference = E.exponent_difference(monomial, base_monomial)
                key = E.canonical_row(difference, 1)
                if key in active_seen:
                    continue
                active_seen.add(key)
                active_rows.append({
                    "difference": difference,
                    "constant": Fraction(1),
                    "source_record": record_index,
                })
        if len(reduced) == 3:
            trinomials.append((record_index, reduced))
        if record_index == 343:
            terminal = {
                "source_record": record_index,
                "classes": len(reduced),
                "normal_form": E.polynomial_trace(reduced),
                "parents": sorted(parents),
                "trace_sha256": D.content_hash(traces),
            }
        if record_index == 1768:
            unit_circle_obstruction = {
                "source_record": record_index,
                "classes": len(reduced),
                "normal_form": E.polynomial_trace(reduced),
                "absolute_coefficients": sorted(
                    abs(coefficient) for coefficient in reduced.values()
                ),
                "parents": sorted(parents),
                "trace_sha256": D.content_hash(traces),
            }
    require(not histogram[1] and not histogram[2]
            and histogram[3] == 233
            and D.content_hash({str(classes): count for classes, count
                                in sorted(histogram.items())})
                == RESIDUAL_HISTOGRAM_SHA256
            and len(residual_ideal) == 3600
            and D.content_hash(residual_ideal) == RESIDUAL_IDEAL_SHA256,
            "the exact nonlinear residual ideal changed")
    active_basis, active_dependencies = E.L.integer_laurent_basis(active_rows)
    active_row_trace = [
        [[name, str(exponent)]
         for name, exponent in sorted(row["difference"].items())]
        for row in active_rows
    ]
    active_basis_trace = [
        [pivot,
         [[name, str(exponent)] for name, exponent in sorted(row.items())]]
        for pivot, (row, _representation) in sorted(active_basis.items())
    ]
    require(len(active_rows) == 22728 and len(active_basis) == 99
            and len(active_dependencies) == 22629
            and all(row[pivot] == 1
                    for pivot, (row, _representation)
                    in active_basis.items())
            and D.content_hash(active_row_trace)
                == ACTIVE_DIFFERENCE_ROWS_SHA256
            and D.content_hash(active_basis_trace)
                == ACTIVE_DIFFERENCE_BASIS_SHA256,
            "the active residual quotient lattice changed")
    require(terminal["source_record"] == 343
            and terminal["classes"] == 3
            and terminal["normal_form"]
                == T.frontier_input()[-1]["normal_form"]
            and terminal["parents"]
                == [0, 1, 2, 3, 4, 5, 6, 9, 18, 20, 22, 24, 72, 91]
            and terminal["trace_sha256"]
                == "f3d18611689efa4349063b02a95a431ec88fff1e8ac3aca03cececcbfa043741",
            "the selected resultant residual trinomial changed")
    require(unit_circle_obstruction == {
        "source_record": 1768,
        "classes": 4,
        "normal_form": [
            [[
                ["x_02_01", 1], ["x_13_22", 1],
                ["x_45_22", 1], ["x_67_22", 1],
            ], "1"],
            [[
                ["x_02_01", 1], ["x_13_22", 1],
                ["x_46_22", 1], ["x_57_22", 1],
            ], "1"],
            [[
                ["x_02_01", 1], ["x_13_22", 1],
                ["x_47_22", 1], ["x_56_22", 1],
            ], "1"],
            [[
                ["x_06_02", 1], ["x_13_22", 1],
                ["x_26_12", 1], ["x_47_22", 1],
                ["x_57_22", 1], ["x_67_22", -1],
            ], "6"],
        ],
        "absolute_coefficients": [1, 1, 1, 6],
        "parents": [0, 1, 2, 12, 18, 20, 22, 30, 36, 38, 40,
                    48, 91, 92],
        "trace_sha256":
            "0951453bb31fc02743bb9a011bbddd246b48842305d43b336036d1252f16eff6",
    }, "the unit-circle residual obstruction changed")
    cancellation = pair_cancellation_census(trinomials, extended_rows)
    require(cancellation == {
        "laurent_shift_equalities": 5241,
        "binomial_cancellations": 0,
        "new_character_rows": 0,
    }, "the second resultant census changed")
    return (support, records, extended_rows, extended_basis,
            extended_dependencies, parametrization, free_parameters,
            resultant_trace, histogram, terminal, cancellation,
            active_rows, active_basis, unit_circle_obstruction)


def audit():
    started = monotonic()
    (support, records, rows, basis, dependencies, parametrization,
     free_parameters, resultants, histogram, terminal, cancellation,
     active_rows, active_basis, unit_circle_obstruction) = frontier_input()
    ledger = {
        "pinned_sources": PINNED,
        "localized_cells": len(support),
        "complete_shadow": C.support_shadow_audit(support),
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "checked_trinomial_resultants": resultants,
        "extended_character": {
            "rows": len(rows), "rank": len(basis),
            "dependencies": len(dependencies),
            "inconsistent_dependencies": 0,
        },
        "free_torus_parameters": free_parameters,
        "pivot_parametrization": parametrization,
        "residual_generators": sum(histogram.values()) - histogram[0],
        "residual_histogram_sha256": RESIDUAL_HISTOGRAM_SHA256,
        "residual_ideal_sha256": RESIDUAL_IDEAL_SHA256,
        "active_residual_quotient": {
            "ambient_torus_dimension": len(free_parameters),
            "difference_rows": len(active_rows),
            "difference_rank": len(active_basis),
            "inert_torus_dimension": len(free_parameters) - len(active_basis),
            "row_sha256": ACTIVE_DIFFERENCE_ROWS_SHA256,
            "basis_sha256": ACTIVE_DIFFERENCE_BASIS_SHA256,
        },
        "selected_three_class_residual": terminal,
        "second_resultant_census": cancellation,
        "unit_circle_obstruction": unit_circle_obstruction,
        "finite_character_status": (
            "no root-of-unity character of any order: record 1768 has "
            "coefficient magnitudes 1,1,1,6, so the dominant term has "
            "modulus 6 while the other three sum to modulus at most 3"
        ),
        "status": (
            "six exact trinomial resultants extend the torus to rank 39; "
            "the remaining 3600-row nonlinear Laurent ideal is the first "
            "genuinely nontrivial coefficient frontier"
        ),
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the resultant-frontier ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("resultants / torus rank / dimension: %d / %d / %d" % (
        len(ledger["checked_trinomial_resultants"]),
        ledger["extended_character"]["rank"],
        len(ledger["free_torus_parameters"]),
    ))
    print("residual generators:", ledger["residual_generators"])
    print("active quotient rank / inert dimension: %d / %d" % (
        ledger["active_residual_quotient"]["difference_rank"],
        ledger["active_residual_quotient"]["inert_torus_dimension"],
    ))
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()

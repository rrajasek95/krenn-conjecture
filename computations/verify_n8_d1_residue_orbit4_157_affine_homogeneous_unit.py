#!/usr/bin/env python3
"""Affine/homogeneous residue-fibre collision on the nonlinear O4 face."""

from __future__ import annotations

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


PINNED_RESULTANT_FRONTIER_SHA256 = (
    "daef95acc86cd14bdc7b148414de4feb543fd5cbe5a79072f6dcda0f2606ca4a"
)
SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_157_resultant_frontier.py"
)
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_RESULTANT_FRONTIER_SHA256,
            "the pinned nonlinear O4 frontier changed")

R = importlib.import_module(
    "verify_n8_d1_residue_orbit4_157_resultant_frontier"
)
E, Q, C, D, X = R.E, R.Q, R.C, R.D, R.X

AFFINE_RECORD = 5
HOMOGENEOUS_RECORD = 2960
EXPECTED_LEDGER_SHA256 = (
    "ff7ae6d934617526f41c74baba29ba0d5a259670619dc28092e337ee2c8097cb"
)


def extended_character_input(records):
    rows, relations, basis = R.native_character_system(records)
    selected = R.selected_trinomial_certificates(
        records, rows, relations, basis
    )
    resultants = []
    resultant_relations = []
    for first, second in itertools.combinations(R.SELECTED_TRINOMIALS, 2):
        row, relation, _trace = R.pair_resultant(
            records, selected, first, second
        )
        resultants.append(row)
        resultant_relations.append(relation)
    extended_rows = rows + resultants
    extended_relations = relations + resultant_relations
    extended_basis, dependencies = E.L.integer_laurent_basis(extended_rows)
    require(len(extended_rows) == 97 and len(extended_basis) == 39
            and len(dependencies) == 58
            and all(E.row_character(dependency, extended_rows) == 1
                    for dependency in dependencies),
            "the resultant-extended character torus changed")
    characters = {
        pivot: E.row_character(representation, extended_rows)
        for pivot, (_row, representation) in extended_basis.items()
    }
    return extended_rows, extended_relations, extended_basis, characters


def monomial(names, coefficient=1):
    return E.laurent_monomial(
        tuple(sorted((name, 1) for name in names)), Fraction(coefficient)
    )


def transported_clauses(positive, negative):
    """Transport a support implication by the eight D1 chart symmetries."""
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
            clauses[(transported_positive, transported_negative)] = (
                clauses.get((transported_positive, transported_negative), 0)
                + 1
            )
    require(actions == 8, "the D1 chart symmetry group changed")
    return [{
        "positive_cells": [list(cell) for cell in positive_cells],
        "negative_cells": [list(cell) for cell in negative_cells],
        "transport_multiplicity": multiplicity,
    } for (positive_cells, negative_cells), multiplicity
        in sorted(clauses.items())]


def reduced_source_certificate(records, rows, relations, basis, characters,
                               record_index):
    reduced, traces, parents = E.reduce_record(
        records[record_index], basis, characters
    )
    certificate = X.reduced_certificate(
        records, rows, basis, relations,
        record_index, reduced, traces,
    )
    require(E.evaluate_certificate(certificate, records) == reduced,
            "a selected residual failed ordinary-source reconstruction")
    return reduced, certificate, traces, parents


def certificate_input():
    support = Q.allowed_support() - set(R.T.MISSING)
    records = C.coefficient_generators(support)
    require(len(support) == 157 and len(records) == 4321
            and D.content_hash(records) == R.T.GENERATOR_SHA256,
            "the nonlinear O4 coefficient input changed")
    rows, relations, basis, characters = extended_character_input(records)
    affine, affine_certificate, affine_traces, affine_parents = (
        reduced_source_certificate(
            records, rows, relations, basis, characters, AFFINE_RECORD
        )
    )
    homogeneous, homogeneous_certificate, homogeneous_traces, (
        homogeneous_parents
    ) = reduced_source_certificate(
        records, rows, relations, basis, characters, HOMOGENEOUS_RECORD
    )

    residue_sum = {}
    residue_sum = E.laurent_add(
        residue_sum, monomial(("x_45_22", "x_67_22"))
    )
    residue_sum = E.laurent_add(
        residue_sum, monomial(("x_46_22", "x_57_22"))
    )
    residue_sum = E.laurent_add(
        residue_sum, monomial(("x_47_22", "x_56_22"))
    )
    factor = monomial(("x_06_02", "x_13_22", "x_27_01"))
    factor = E.laurent_mul(
        factor, E.laurent_monomial((("x_67_22", -1),))
    )
    require(affine == E.laurent_add(
                residue_sum, E.laurent_monomial((), -1)
            )
            and homogeneous == E.laurent_mul(factor, residue_sum),
            "the affine/homogeneous residue-fibre pair changed")

    inverse_factor = E.laurent_monomial(
        E.exponent_scale(next(iter(factor)), -1)
    )
    unit_certificate = E.certificate_add(
        affine_certificate,
        E.certificate_mul(homogeneous_certificate, inverse_factor),
        -1,
    )
    unit = E.laurent_monomial((), -1)
    require(E.evaluate_certificate(unit_certificate, records) == unit,
            "the affine/homogeneous Laurent unit failed")
    ordinary = X.clear_to_saturation(
        unit_certificate, unit, support, records
    )
    witnesses = E.source_witnesses(
        records, tuple(ordinary["source_records"])
    )
    require(set(witnesses) <= support,
            "an ordinary-source witness is absent on the frozen face")
    # The residue-purity equation already contains all three residue perfect
    # matchings, so upward support additions cannot change it.  Only the nine
    # full-output sources acquire new matching monomials.
    full_sources = [index for index in ordinary["source_records"]
                    if records[index]["families"] == ["full_exactness"]]
    require(len(full_sources) == 9,
            "the affine/homogeneous full-output source census changed")
    repair_masks = R.H.H.minimal_repair_masks(
        records, full_sources, support
    )
    require(repair_masks and all(len(mask) == 1 for mask in repair_masks),
            "the affine/homogeneous upward chart is not singleton-visible")
    repair_cells = {next(iter(mask)) for mask in repair_masks}
    transported = transported_clauses(repair_cells, set(witnesses))
    return {
        "support": support,
        "records": records,
        "rows": rows,
        "basis": basis,
        "affine": affine,
        "homogeneous": homogeneous,
        "factor": factor,
        "affine_trace_sha256": D.content_hash(affine_traces),
        "homogeneous_trace_sha256": D.content_hash(homogeneous_traces),
        "affine_parents": sorted(affine_parents),
        "homogeneous_parents": sorted(homogeneous_parents),
        "laurent_certificate_sha256": D.content_hash(
            E.certificate_trace(unit_certificate)
        ),
        "ordinary": ordinary,
        "witnesses": witnesses,
        "repair_masks": repair_masks,
        "transported_clauses": transported,
    }


def audit():
    started = monotonic()
    data = certificate_input()
    masks = sorted(
        ([list(cell) for cell in sorted(mask)] for mask in data["repair_masks"]),
        key=repr,
    )
    ledger = {
        "pinned_resultant_frontier_sha256":
            PINNED_RESULTANT_FRONTIER_SHA256,
        "localized_cells": len(data["support"]),
        "coefficient_generators": len(data["records"]),
        "extended_character_rows": len(data["rows"]),
        "extended_character_rank": len(data["basis"]),
        "affine_record": AFFINE_RECORD,
        "homogeneous_record": HOMOGENEOUS_RECORD,
        "residue_sum": E.polynomial_trace(E.laurent_add(
            data["affine"], E.laurent_monomial()
        )),
        "homogeneous_factor": E.polynomial_trace(data["factor"]),
        "affine_reduction_trace_sha256": data["affine_trace_sha256"],
        "homogeneous_reduction_trace_sha256":
            data["homogeneous_trace_sha256"],
        "affine_character_parents": data["affine_parents"],
        "homogeneous_character_parents": data["homogeneous_parents"],
        "laurent_unit_certificate_sha256":
            data["laurent_certificate_sha256"],
        "ordinary_saturation_certificate": data["ordinary"],
        "localized_source_witnesses": [list(cell)
                                       for cell in data["witnesses"]],
        "minimal_repair_masks": masks,
        "distinct_transported_clauses": data["transported_clauses"],
        "characteristic_scope": "all characteristics",
        "structural_status": (
            "the same residue three-matching sum is forced to equal one "
            "by record 5 and to vanish after multiplication by a localized "
            "external Laurent monomial by record 2960"
        ),
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
        print("ordinary:", ledger["ordinary_saturation_certificate"])
        print("laurent certificate sha256:",
              ledger["laurent_unit_certificate_sha256"])
        print("witness count:", len(ledger["localized_source_witnesses"]))
        print("repair masks:", ledger["minimal_repair_masks"])
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the affine/homogeneous O4 unit ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("affine / homogeneous records: %d / %d" % (
        AFFINE_RECORD, HOMOGENEOUS_RECORD
    ))
    print("ordinary saturation: U^%d" % ledger[
        "ordinary_saturation_certificate"
    ]["ordinary_saturation_power"])
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()

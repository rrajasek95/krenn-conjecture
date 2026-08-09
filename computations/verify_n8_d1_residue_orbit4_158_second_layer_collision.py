#!/usr/bin/env python3
"""Second-layer Laurent-character collision on the open 158-cell O4 face."""

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
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent.py":
        "290195e979282bee0029a4cf02012b79ecba2212bf87daacb2710ff9cf6edf63",
    "verify_n8_d1_residue_orbit4_158_direct_batch.py":
        "8bed466723fe37da34136f4c10f5d49e866984effddcb69b56dbdf0bbde6335e",
}
for filename, expected in PINNED.items():
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned 158-cell Laurent source changed: " + filename)

E = importlib.import_module(
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent"
)
B = importlib.import_module("verify_n8_d1_residue_orbit4_158_direct_batch")
Q, C, D = E.Q, E.C, E.D

EXPECTED_LEDGER_SHA256 = (
    "0189ecc2eb46cff45126bbb528985d0c77af067c084758fb27d530839f04c062"
)


def base_relations(records, rows):
    relations = []
    for row in rows:
        difference = tuple(sorted(
            (name, exponent.numerator)
            for name, exponent in row["difference"].items()
        ))
        divisor = tuple(sorted(Counter(row["divisor"]).items()))
        certificate = {
            row["source_record"]: E.laurent_monomial(
                E.exponent_scale(divisor, -1)
            )
        }
        expected = E.laurent_add(
            E.laurent_monomial(difference),
            E.laurent_monomial((), -row["constant"]),
        )
        require(E.evaluate_certificate(certificate, records) == expected,
                "an initial normalized binomial certificate failed")
        relations.append({
            "difference": difference,
            "constant": row["constant"],
            "certificate": certificate,
        })
    return relations


def reduced_certificate(records, rows, basis, relations,
                        record_index, reduced, traces):
    difference_certificate = {}
    for (raw_monomial, raw_coefficient), trace in zip(
            records[record_index]["terms"], traces):
        representation = Counter()
        for pivot, multiplier in trace["pivot_multipliers"]:
            _basis_row, basis_representation = basis[pivot]
            for position, scalar in basis_representation.items():
                representation[position] += Fraction(multiplier) * scalar
                if not representation[position]:
                    representation.pop(position)
        relation = E.relation_from_representation(
            dict(representation), relations
        )
        canonical = tuple((name, exponent) for name, exponent
                          in trace["canonical_exponent"])
        original = tuple(sorted(Counter(raw_monomial).items()))
        require(relation["difference"] == E.exponent_add(
            original, E.exponent_scale(canonical, -1)
        ), "a two-class term relation has the wrong exponent")
        require(Fraction(raw_coefficient) * relation["constant"]
                == Fraction(trace["coefficient"]),
                "a two-class term relation has the wrong character")
        difference_certificate = E.certificate_add(
            difference_certificate,
            E.certificate_mul(
                relation["certificate"],
                E.laurent_monomial(canonical, Fraction(raw_coefficient)),
            ),
        )
    certificate = {record_index: E.laurent_monomial()}
    certificate = E.certificate_add(certificate, difference_certificate, -1)
    require(E.evaluate_certificate(certificate, records) == reduced,
            "an expanded two-class certificate failed")
    return certificate


def clear_to_saturation(certificate, target, support, records):
    require(len(target) == 1,
            "the collision target is not a Laurent monomial")
    target_exponent, target_coefficient = next(iter(target.items()))
    minima = Counter(dict(target_exponent))
    for cofactor in certificate.values():
        for exponent in cofactor:
            for name, value in exponent:
                minima[name] = min(minima.get(name, 0), value)
    clearing = tuple(sorted((name, -value) for name, value in minima.items()
                            if value < 0))
    cleared_certificate = E.certificate_mul(
        certificate, E.laurent_monomial(clearing)
    )
    cleared_target = E.exponent_add(target_exponent, clearing)
    require(E.evaluate_certificate(cleared_certificate, records)
            == E.laurent_monomial(cleared_target, target_coefficient),
            "the collision certificate did not clear to the ordinary ring")
    require(all(value >= 0 for cofactor in cleared_certificate.values()
                for monomial in cofactor for _name, value in monomial),
            "a cleared collision cofactor retains a denominator")

    support_names = tuple("x_%d%d_%d%d" % cell for cell in sorted(support))
    target_counter = Counter(dict(cleared_target))
    saturation_power = max(target_counter.values())
    quotient = tuple(sorted((name, saturation_power
                             - target_counter.get(name, 0))
                            for name in support_names
                            if saturation_power - target_counter.get(name, 0)))
    saturation = E.certificate_mul(
        cleared_certificate,
        E.laurent_monomial(quotient, Fraction(1, target_coefficient)),
    )
    u_power = tuple(sorted((name, saturation_power)
                           for name in support_names))
    require(E.evaluate_certificate(saturation, records)
            == E.laurent_monomial(u_power),
            "the collision ordinary U^k identity failed")
    return {
        "source_records": sorted(saturation),
        "laurent_cofactor_terms": sum(len(poly) for poly in certificate.values()),
        "clearing_monomial": [[name, exponent]
                              for name, exponent in clearing],
        "ordinary_saturation_power": saturation_power,
        "ordinary_cofactor_terms": sum(len(poly) for poly in saturation.values()),
        "ordinary_certificate_sha256": D.content_hash(
            E.certificate_trace(saturation)
        ),
        "integral_coefficients": all(
            coefficient.denominator == 1
            for cofactor in saturation.values()
            for coefficient in cofactor.values()
        ),
    }


def certificate_input():
    support = Q.allowed_support() - set(B.OPEN_MISSING)
    records = C.coefficient_generators(support)
    require(len(support) == 158 and len(records) == 4321
            and D.content_hash(records) == B.OPEN_GENERATOR_SHA256,
            "the open 158-cell coefficient input changed")
    rows = B.initial_rows(records)
    basis, dependencies = E.L.integer_laurent_basis(rows)
    require(len(rows) == 54 and len(basis) == 20 and len(dependencies) == 34
            and all(E.row_character(dependency, rows) == 1
                    for dependency in dependencies),
            "the open 158-cell first Laurent layer changed")
    basis_characters = {
        pivot: E.row_character(representation, rows)
        for pivot, (_basis_row, representation) in basis.items()
    }
    selected = []
    for record_index in (1551, 1611):
        reduced, traces, parents = E.reduce_record(
            records[record_index], basis, basis_characters
        )
        require(len(reduced) == 2,
                "a selected second-layer row stopped being binomial")
        selected.append((record_index, reduced, traces, parents))
    first_index, first, first_traces, _first_parents = selected[0]
    second_index, second, second_traces, _second_parents = selected[1]
    require([str(coefficient) for _monomial, coefficient in sorted(first.items())]
            == ["1", "1"]
            and [str(coefficient) for _monomial, coefficient
                 in sorted(second.items())] == ["-1", "1"],
            "the opposite second-layer characters changed")

    relations = base_relations(records, rows)
    first_certificate = reduced_certificate(
        records, rows, basis, relations, first_index, first, first_traces
    )
    second_certificate = reduced_certificate(
        records, rows, basis, relations, second_index, second, second_traces
    )
    (first_lead, _first_coefficient), = tuple(sorted(first.items()))[:1]
    (second_lead, _second_coefficient), = tuple(sorted(second.items()))[:1]
    scaling_exponent = E.exponent_add(
        second_lead, E.exponent_scale(first_lead, -1)
    )
    scaling = E.laurent_monomial(scaling_exponent)
    combined = E.certificate_add(
        E.certificate_mul(first_certificate, scaling), second_certificate
    )
    target = E.laurent_add(E.laurent_mul(first, scaling), second)
    require(len(target) == 1
            and next(iter(target.values())) == Fraction(2),
            "the second-layer collision did not isolate twice a monomial")
    require(E.evaluate_certificate(combined, records) == target,
            "the expanded second-layer collision identity failed")
    ordinary = clear_to_saturation(combined, target, support, records)
    witnesses = E.source_witnesses(
        records, tuple(ordinary["source_records"])
    )
    require(set(witnesses) <= support,
            "a collision source witness is not localized")
    return (support, records, rows, first, second, scaling_exponent,
            ordinary, witnesses)


def transported_clause_audit():
    _support, _records, _rows, _first, _second, _scale, _ordinary, witnesses = (
        certificate_input()
    )
    return E.transform_clauses(set(B.OPEN_MISSING), set(witnesses))


def audit():
    started = monotonic()
    support, records, rows, first, second, scale, ordinary, witnesses = (
        certificate_input()
    )
    shadow = C.support_shadow_audit(support)
    transported = E.transform_clauses(set(B.OPEN_MISSING), set(witnesses))
    ledger = {
        "pinned_sources": PINNED,
        "localized_cells": len(support),
        "complete_shadow": shadow,
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "first_layer_rows": len(rows),
        "first_layer_rank": 20,
        "opposite_character_records": [1551, 1611],
        "first_normal_form": E.polynomial_trace(first),
        "second_normal_form": E.polynomial_trace(second),
        "aligning_laurent_monomial": [[name, exponent]
                                      for name, exponent in scale],
        "ordinary_saturation_certificate": ordinary,
        "localized_source_witnesses": [list(cell) for cell in witnesses],
        "distinct_transported_clauses": transported,
        "characteristic_scope": "every characteristic except two",
        "status": "open 158-cell O4 face is empty by second-layer collision",
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the 158-cell second-layer ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("collision records:", ledger["opposite_character_records"])
    print("ordinary saturation: U^%d" % ledger[
        "ordinary_saturation_certificate"
    ]["ordinary_saturation_power"])
    print("source records:", len(ledger[
        "ordinary_saturation_certificate"
    ]["source_records"]))
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()

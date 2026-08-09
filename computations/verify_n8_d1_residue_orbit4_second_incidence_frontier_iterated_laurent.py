#!/usr/bin/env python3
"""Iterated exact Laurent closure of the second 159-cell O4 frontier."""

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


PINNED_ORACLE_SHA256 = (
    "d2dfc3917f5ea1344ab9c6adbbf1c52a34ef529e0364ec11daf2247012c44291"
)
SOURCE = os.path.join(
    HERE,
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_laurent_oracle.py",
)
with open(SOURCE, "rb") as handle:
    source_digest = hashlib.sha256(handle.read()).hexdigest()
if PINNED_ORACLE_SHA256 != "TO_BE_PINNED":
    require(source_digest == PINNED_ORACLE_SHA256,
            "the pinned second-frontier Laurent oracle changed")
O = importlib.import_module(
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_laurent_oracle"
)
Q, L, C, D = O.Q, O.L, O.C, O.D

EXPECTED_LEDGER_SHA256 = (
    "e1695ba1fc8f4a2dd3cb2f4238273d6849d1228142fb67d48e3ed88e7bd858da"
)


def rational_power(value, exponent):
    require(exponent.denominator == 1,
            "a Laurent character exponent is not integral")
    exponent = exponent.numerator
    return (value ** exponent if exponent >= 0
            else Fraction(1, value ** (-exponent)))


def row_character(representation, rows):
    result = Fraction(1)
    for position, exponent in representation.items():
        result *= rational_power(rows[position]["constant"], exponent)
    return result


def canonical_row(difference, constant):
    difference = {name: Fraction(exponent)
                  for name, exponent in difference.items() if exponent}
    require(difference, "a zero exponent row was offered to the lattice")
    pivot = min(difference)
    if difference[pivot] < 0:
        difference = {name: -exponent
                      for name, exponent in difference.items()}
        constant = Fraction(1, constant)
    require(all(exponent.denominator == 1
                for exponent in difference.values()),
            "a derived Laurent exponent is not integral")
    return (tuple(sorted((name, exponent.numerator)
                         for name, exponent in difference.items())),
            constant)


def exponent_difference(first, second):
    result = Counter(dict(first))
    result.subtract(dict(second))
    return {name: Fraction(exponent) for name, exponent in result.items()
            if exponent}


def reduce_record(record, basis, basis_characters):
    reduced = Counter()
    traces = []
    used_rows = set()
    for monomial, raw_coefficient in record["terms"]:
        exponent = Counter(monomial)
        coefficient = Fraction(raw_coefficient)
        multipliers = []
        # Pivot order is essential: each echelon row contains only variables
        # lexicographically above its pivot, so ascending pivots give a true
        # canonical Laurent normal form without reintroducing an old pivot.
        for pivot, (basis_row, representation) in sorted(basis.items()):
            multiplier = exponent.get(pivot, 0)
            if not multiplier:
                continue
            multipliers.append((pivot, multiplier))
            coefficient *= rational_power(
                basis_characters[pivot], Fraction(multiplier)
            )
            for name, value in basis_row.items():
                require(value.denominator == 1,
                        "a basis row ceased to be integral")
                exponent[name] -= multiplier * value.numerator
                if not exponent[name]:
                    exponent.pop(name, None)
            used_rows.update(position for position, scalar
                             in representation.items()
                             if multiplier * scalar)
        canonical = tuple(sorted(exponent.items()))
        reduced[canonical] += coefficient
        if not reduced[canonical]:
            del reduced[canonical]
        traces.append({
            "input_monomial": list(monomial),
            "canonical_exponent": [[name, value]
                                   for name, value in canonical],
            "coefficient": str(coefficient),
            "pivot_multipliers": [[pivot, multiplier]
                                  for pivot, multiplier in multipliers],
        })

    # Independently reconstruct each term's exponent rewrite and character
    # from the recorded pivot multipliers.
    for (monomial, raw_coefficient), trace in zip(record["terms"], traces):
        direct = Counter(monomial)
        direct.subtract(dict((name, exponent)
                             for name, exponent
                             in trace["canonical_exponent"]))
        direct = {name: Fraction(value) for name, value in direct.items()
                  if value}
        rebuilt = {}
        rebuilt_character = Fraction(raw_coefficient)
        for pivot, multiplier in trace["pivot_multipliers"]:
            basis_row, _representation = basis[pivot]
            L.axpy(rebuilt, Fraction(multiplier), basis_row)
            rebuilt_character *= rational_power(
                basis_characters[pivot], Fraction(multiplier)
            )
        require(rebuilt == direct
                and rebuilt_character == Fraction(trace["coefficient"]),
                "a generalized Laurent rewrite failed reconstruction")
    return dict(reduced), traces, used_rows


def exponent_add(*exponents):
    result = Counter()
    for exponent in exponents:
        result.update(dict(exponent))
    return tuple(sorted((name, value) for name, value in result.items()
                        if value))


def exponent_scale(exponent, scalar):
    return tuple(sorted((name, scalar * value) for name, value in exponent
                        if scalar * value))


def laurent_monomial(exponent=(), coefficient=1):
    coefficient = Fraction(coefficient)
    return ({tuple(exponent): coefficient} if coefficient else {})


def laurent_add(left, right, scalar=1):
    result = dict(left)
    scalar = Fraction(scalar)
    for exponent, coefficient in right.items():
        result[exponent] = result.get(exponent, Fraction(0)) + scalar * coefficient
        if not result[exponent]:
            result.pop(exponent)
    return result


def laurent_mul(left, right):
    result = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = exponent_add(left_exponent, right_exponent)
            result[exponent] = (result.get(exponent, Fraction(0))
                                + left_coefficient * right_coefficient)
            if not result[exponent]:
                result.pop(exponent)
    return result


def certificate_add(left, right, scalar=1):
    result = {source: dict(poly) for source, poly in left.items()}
    for source, poly in right.items():
        result[source] = laurent_add(
            result.get(source, {}), poly, scalar
        )
        if not result[source]:
            result.pop(source)
    return result


def certificate_mul(certificate, polynomial):
    return {source: laurent_mul(cofactor, polynomial)
            for source, cofactor in certificate.items()}


def relation_product(left, right):
    # x^(d+e)-c*f = x^e*(x^d-c)+c*(x^e-f).
    certificate = certificate_add(
        certificate_mul(left["certificate"],
                        laurent_monomial(right["difference"])),
        right["certificate"], left["constant"],
    )
    return {
        "difference": exponent_add(left["difference"], right["difference"]),
        "constant": left["constant"] * right["constant"],
        "certificate": certificate,
    }


def relation_inverse(relation):
    # x^(-d)-c^(-1) = -c^(-1)*x^(-d)*(x^d-c).
    multiplier = laurent_monomial(
        exponent_scale(relation["difference"], -1),
        -Fraction(1, relation["constant"]),
    )
    return {
        "difference": exponent_scale(relation["difference"], -1),
        "constant": Fraction(1, relation["constant"]),
        "certificate": certificate_mul(relation["certificate"], multiplier),
    }


def relation_power(relation, exponent):
    require(exponent.denominator == 1,
            "a relation is raised to a fractional power")
    exponent = exponent.numerator
    if exponent < 0:
        return relation_power(relation_inverse(relation), Fraction(-exponent))
    result = {"difference": (), "constant": Fraction(1), "certificate": {}}
    for _repeat in range(exponent):
        result = relation_product(result, relation)
    return result


def relation_from_representation(representation, base_relations):
    result = {"difference": (), "constant": Fraction(1), "certificate": {}}
    for position, exponent in sorted(representation.items()):
        result = relation_product(
            result, relation_power(base_relations[position], exponent)
        )
    return result


def record_laurent_polynomial(record):
    result = {}
    for monomial, coefficient in record["terms"]:
        exponent = tuple(sorted(Counter(monomial).items()))
        result = laurent_add(
            result, laurent_monomial(exponent, Fraction(coefficient))
        )
    return result


def evaluate_certificate(certificate, records):
    result = {}
    for source, cofactor in certificate.items():
        result = laurent_add(
            result, laurent_mul(cofactor,
                                record_laurent_polynomial(records[source]))
        )
    return result


def polynomial_trace(polynomial):
    return [
        [[[name, exponent] for name, exponent in monomial], str(coefficient)]
        for monomial, coefficient in sorted(polynomial.items())
    ]


def certificate_trace(certificate):
    return [[source, polynomial_trace(cofactor)]
            for source, cofactor in sorted(certificate.items())]


def initial_rows(records):
    rows = []
    seen = set()
    for record_index, record in enumerate(records):
        if len(record["terms"]) != 2:
            continue
        parsed = [(tuple(monomial), Fraction(coefficient))
                  for monomial, coefficient in record["terms"]]
        if {coefficient for _monomial, coefficient in parsed} != {Fraction(1)}:
            continue
        difference = L.exponent_difference(parsed[0][0], parsed[1][0])
        key = canonical_row(difference, Fraction(-1))
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "difference": difference,
            "constant": Fraction(-1),
            "source_record": record_index,
            "parents": (),
            "iteration": 0,
            "divisor": tuple(parsed[1][0]),
        })
    require(len(rows) == 54,
            "the unique initial plus-binomial row census changed")
    return rows, seen


def closure(records, frozen=True):
    rows, seen = initial_rows(records)
    iteration_rows = []
    final = None
    for iteration in range(10):
        basis, dependencies = L.integer_laurent_basis(rows)
        dependency_characters = [row_character(dependency, rows)
                                  for dependency in dependencies]
        require(all(value == 1 for value in dependency_characters),
                "a Laurent character dependency already gives a unit")
        basis_characters = {
            pivot: row_character(representation, rows)
            for pivot, (_basis_row, representation) in basis.items()
        }
        new_rows = []
        reduced_histogram = Counter()
        for record_index, record in enumerate(records):
            reduced, traces, parents = reduce_record(
                record, basis, basis_characters
            )
            reduced_histogram[len(reduced)] += 1
            if len(reduced) == 1:
                final = {
                    "iteration": iteration,
                    "source_record": record_index,
                    "normal_form": [
                        [
                            [[name, exponent]
                             for name, exponent in monomial],
                            str(coefficient),
                        ]
                        for monomial, coefficient in sorted(reduced.items())
                    ],
                    "parents": sorted(parents),
                    "trace_sha256": D.content_hash(traces),
                    "basis_rank": len(basis),
                    "traces": traces,
                }
                break
            if len(reduced) != 2:
                continue
            (first, first_coefficient), (second, second_coefficient) = sorted(
                reduced.items()
            )
            difference = exponent_difference(first, second)
            constant = -second_coefficient / first_coefficient
            key = canonical_row(difference, constant)
            if key in seen:
                continue
            seen.add(key)
            new_rows.append({
                "difference": difference,
                "constant": constant,
                "source_record": record_index,
                "parents": tuple(sorted(parents)),
                "iteration": iteration + 1,
                "normal_form": (
                    (first, first_coefficient),
                    (second, second_coefficient),
                ),
                "trace_sha256": D.content_hash(traces),
            })
        iteration_rows.append({
            "iteration": iteration,
            "input_rows": len(rows),
            "lattice_rank": len(basis),
            "dependencies": len(dependencies),
            "reduced_class_histogram": {
                str(classes): count
                for classes, count in sorted(reduced_histogram.items())
            },
            "new_rows": len(new_rows),
            "new_constants": dict(sorted(Counter(
                str(row["constant"]) for row in new_rows
            ).items())),
            "new_source_records": [row["source_record"] for row in new_rows],
        })
        if final is not None:
            break
        require(new_rows, "the iterated Laurent closure stalled")
        rows.extend(new_rows)
    require(final is not None,
            "the iterated Laurent closure did not reach a unit")
    if frozen:
        require([row["new_rows"] for row in iteration_rows] == [2]
                and [row["lattice_rank"] for row in iteration_rows] == [20],
                "the pivot-ordered Laurent profile changed")
        require(final["iteration"] == 0 and final["source_record"] == 1551,
                "the terminal one-class generator changed")
        require(final["normal_form"] == [[
            [["x_04_00", 1], ["x_15_12", 1], ["x_26_01", 1],
             ["x_37_00", 1], ["x_57_12", 1], ["x_57_22", -1]],
            "1",
        ]], "the terminal Laurent monomial changed")
    return rows, iteration_rows, final


def ordinary_saturation_certificate(records, rows, final, support):
    require(final["iteration"] == 0,
            "the direct certificate unexpectedly uses a derived row")
    basis, dependencies = L.integer_laurent_basis(rows)
    require(all(row_character(dependency, rows) == 1
                for dependency in dependencies),
            "the direct basis has an inconsistent character")

    base_relations = []
    for row in rows:
        difference = tuple(sorted(
            (name, exponent.numerator)
            for name, exponent in row["difference"].items()
        ))
        divisor = tuple(sorted(Counter(row["divisor"]).items()))
        certificate = {
            row["source_record"]: laurent_monomial(
                exponent_scale(divisor, -1)
            )
        }
        relation = {
            "difference": difference,
            "constant": row["constant"],
            "certificate": certificate,
        }
        expected = laurent_add(
            laurent_monomial(difference),
            laurent_monomial((), -row["constant"]),
        )
        require(evaluate_certificate(certificate, records) == expected,
                "an initial normalized binomial certificate failed")
        base_relations.append(relation)

    difference_certificate = {}
    for (raw_monomial, raw_coefficient), trace in zip(
            records[final["source_record"]]["terms"], final["traces"]):
        representation = Counter()
        for pivot, multiplier in trace["pivot_multipliers"]:
            _basis_row, basis_representation = basis[pivot]
            for position, scalar in basis_representation.items():
                representation[position] += Fraction(multiplier) * scalar
                if not representation[position]:
                    representation.pop(position)
        relation = relation_from_representation(
            dict(representation), base_relations
        )
        canonical = tuple((name, exponent)
                          for name, exponent
                          in trace["canonical_exponent"])
        original = tuple(sorted(Counter(raw_monomial).items()))
        require(relation["difference"]
                == exponent_add(original, exponent_scale(canonical, -1)),
                "a terminal term relation has the wrong exponent")
        require(Fraction(raw_coefficient) * relation["constant"]
                == Fraction(trace["coefficient"]),
                "a terminal term relation has the wrong character")
        multiplier = laurent_monomial(
            canonical, Fraction(raw_coefficient)
        )
        difference_certificate = certificate_add(
            difference_certificate,
            certificate_mul(relation["certificate"], multiplier),
        )

    reduced_exponent = tuple((name, exponent) for name, exponent
                             in final["normal_form"][0][0])
    reduced_coefficient = Fraction(final["normal_form"][0][1])
    reduced = laurent_monomial(reduced_exponent, reduced_coefficient)
    # record - reduced = difference_certificate, hence
    # reduced = record - difference_certificate.
    unit_certificate = {final["source_record"]: laurent_monomial()}
    unit_certificate = certificate_add(
        unit_certificate, difference_certificate, -1
    )
    require(evaluate_certificate(unit_certificate, records) == reduced,
            "the explicit Laurent unit certificate failed")

    # Clear every negative cofactor exponent, then enlarge the resulting
    # ordinary monomial to U^k over all localized variables.
    minima = Counter(dict(reduced_exponent))
    for cofactor in unit_certificate.values():
        for exponent in cofactor:
            for name, value in exponent:
                minima[name] = min(minima.get(name, 0), value)
    clearing = tuple(sorted((name, -value) for name, value in minima.items()
                            if value < 0))
    cleared_target = exponent_add(reduced_exponent, clearing)
    cleared_certificate = certificate_mul(
        unit_certificate, laurent_monomial(clearing)
    )
    require(all(exponent >= 0 for cofactor in cleared_certificate.values()
                for monomial in cofactor for _name, exponent in monomial),
            "the Laurent cofactors did not clear to the ordinary ring")
    require(evaluate_certificate(cleared_certificate, records)
            == laurent_monomial(cleared_target, reduced_coefficient),
            "the cleared ordinary monomial certificate failed")

    support_names = tuple("x_%d%d_%d%d" % cell for cell in sorted(support))
    target_counter = Counter(dict(cleared_target))
    require(set(target_counter) <= set(support_names),
            "the ordinary target contains a nonlocalized variable")
    saturation_power = max(target_counter.values())
    u_power = tuple(sorted((name, saturation_power)
                           for name in support_names))
    quotient = tuple(sorted((name, saturation_power
                             - target_counter.get(name, 0))
                            for name in support_names
                            if saturation_power - target_counter.get(name, 0)))
    saturation_certificate = certificate_mul(
        cleared_certificate,
        laurent_monomial(quotient, Fraction(1, reduced_coefficient)),
    )
    require(evaluate_certificate(saturation_certificate, records)
            == laurent_monomial(u_power),
            "the explicit ordinary U^k certificate failed")
    require(all(coefficient.denominator == 1
                for cofactor in saturation_certificate.values()
                for coefficient in cofactor.values()),
            "the ordinary certificate unexpectedly divides an integer")
    return {
        "source_records": sorted(saturation_certificate),
        "laurent_cofactor_terms": sum(len(poly)
                                      for poly in unit_certificate.values()),
        "clearing_monomial": [[name, exponent]
                              for name, exponent in clearing],
        "ordinary_saturation_power": saturation_power,
        "ordinary_cofactor_terms": sum(
            len(poly) for poly in saturation_certificate.values()
        ),
        "ordinary_certificate_sha256": D.content_hash(
            certificate_trace(saturation_certificate)
        ),
    }


def dependency_sources(rows, final):
    needed_rows = set(final["parents"])
    stack = list(needed_rows)
    while stack:
        position = stack.pop()
        for parent in rows[position]["parents"]:
            if parent not in needed_rows:
                needed_rows.add(parent)
                stack.append(parent)
    source_records = {final["source_record"]}
    source_records.update(rows[position]["source_record"]
                          for position in needed_rows)
    return tuple(sorted(needed_rows)), tuple(sorted(source_records))


def source_witnesses(records, source_records):
    names = {
        name for index in source_records
        for monomial, _coefficient in records[index]["terms"]
        for name in monomial
    }
    return tuple(sorted(Q.cell_from_name(name) for name in names))


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
    require(actions == 8 and len(clauses) == 8,
            "the iterated-Laurent face-clause orbit changed")
    return [{
        "positive_cells": [list(cell) for cell in positive_cells],
        "negative_cells": [list(cell) for cell in negative_cells],
        "transport_multiplicity": multiplicity,
    } for (positive_cells, negative_cells), multiplicity
        in sorted(clauses.items())]


def clause_audit():
    support = Q.allowed_support() - set(O.FRONTIER_MISSING)
    records = C.coefficient_generators(support)
    rows, _iterations, final = closure(records)
    needed_rows, _dependency_sources = dependency_sources(rows, final)
    ordinary = ordinary_saturation_certificate(
        records, rows, final, support
    )
    source_records = tuple(ordinary["source_records"])
    witnesses = source_witnesses(records, source_records)
    require(set(witnesses) <= support,
            "a minimized Laurent-chain witness is not localized")
    return {
        "positive_cells": [list(cell) for cell in O.FRONTIER_MISSING],
        "negative_cells": [list(cell) for cell in witnesses],
        "needed_lattice_rows": list(needed_rows),
        "source_records": list(source_records),
    }


def transported_clause_audit():
    base = clause_audit()
    return transform_clauses(
        {tuple(cell) for cell in base["positive_cells"]},
        {tuple(cell) for cell in base["negative_cells"]},
    )


def audit():
    started = monotonic()
    allowed = Q.allowed_support()
    support = allowed - set(O.FRONTIER_MISSING)
    require(len(support) == 159,
            "the second incidence frontier changed size")
    shadow = C.support_shadow_audit(support)
    records = C.coefficient_generators(support)
    require(len(records) == 4321
            and D.content_hash(records) == O.EXPECTED_GENERATOR_SHA256,
            "the second incidence coefficient input changed")
    rows, iterations, final = closure(records)
    needed_rows, dependency_source_records = dependency_sources(rows, final)
    ordinary = ordinary_saturation_certificate(
        records, rows, final, support
    )
    source_records = tuple(ordinary["source_records"])
    require(set(source_records) <= set(dependency_source_records),
            "the explicit certificate uses a source outside its dependency graph")
    witnesses = source_witnesses(records, source_records)
    clause = {
        "positive_cells": [list(cell) for cell in O.FRONTIER_MISSING],
        "negative_cells": [list(cell) for cell in witnesses],
        "needed_lattice_rows": list(needed_rows),
        "source_records": list(source_records),
    }
    transported = transform_clauses(
        set(O.FRONTIER_MISSING), set(witnesses)
    )
    ledger = {
        "pinned_oracle_sha256": source_digest,
        "localized_cells": len(support),
        "complete_shadow": shadow,
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "initial_unique_plus_rows": 54,
        "iterations": iterations,
        "terminal_one_class": {
            key: value for key, value in final.items() if key != "traces"
        },
        "total_laurent_rows_at_terminal": len(rows),
        "minimized_needed_rows": len(needed_rows),
        "minimized_source_records": list(source_records),
        "localized_source_witnesses": [list(cell) for cell in witnesses],
        "ordinary_saturation_certificate": ordinary,
        "support_faithful_clause": clause,
        "distinct_transported_clauses": transported,
        "proof_semantics": (
            "ascending-pivot exact Laurent reduction sends terminal record "
            "1551 to one nonzero monomial; an independently expanded "
            "ordinary cofactor identity puts U^k in the original ideal"
        ),
        "characteristic_scope": "every characteristic; coefficients are integral",
        "status": "second 159-cell O4 incidence frontier is coefficient-empty",
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the iterated Laurent closure ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("derived rows before terminal:",
          [row["new_rows"] for row in ledger["iterations"]])
    print("terminal record:", ledger["terminal_one_class"]["source_record"])
    print("minimized source records:", len(ledger["minimized_source_records"]))
    print("ordinary saturation: U^%d" % ledger[
        "ordinary_saturation_certificate"
    ]["ordinary_saturation_power"])
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()

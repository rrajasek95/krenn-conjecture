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
    "8207c1c0b36fc7437bce616b6c385227ce8210984c540fa9eb13aaad0e70cc56"
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
        for pivot, (basis_row, representation) in basis.items():
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
        })
    require(len(rows) == 54,
            "the unique initial plus-binomial row census changed")
    return rows, seen


def closure(records):
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
    require([row["new_rows"] for row in iteration_rows]
            == [33, 1, 4, 2, 0],
            "the derived-binomial iteration profile changed")
    require([row["lattice_rank"] for row in iteration_rows]
            == [20, 28, 29, 33, 35],
            "the iterated Laurent rank profile changed")
    require(final["iteration"] == 4 and final["source_record"] == 412,
            "the frozen terminal one-class generator changed")
    require(final["normal_form"] == [[
        [["x_06_00", 1], ["x_17_00", 1], ["x_23_10", 1],
         ["x_45_00", 1], ["x_56_20", -1], ["x_56_21", 1]],
        "-1",
    ]], "the terminal Laurent monomial changed")
    return rows, iteration_rows, final


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
    needed_rows, source_records = dependency_sources(rows, final)
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
    needed_rows, source_records = dependency_sources(rows, final)
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
        "terminal_one_class": final,
        "total_laurent_rows_at_terminal": len(rows),
        "minimized_needed_rows": len(needed_rows),
        "minimized_source_records": list(source_records),
        "localized_source_witnesses": [list(cell) for cell in witnesses],
        "support_faithful_clause": clause,
        "distinct_transported_clauses": transported,
        "proof_semantics": (
            "inductively adjoin each exact two-class normal form in the "
            "localized Laurent quotient; terminal record 412 is a nonzero "
            "Laurent monomial, hence the localized ideal is the unit ideal"
        ),
        "characteristic_scope": "characteristic zero (the chain uses 1/2)",
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
    print("derived rows:", [row["new_rows"] for row in ledger["iterations"]])
    print("terminal record:", ledger["terminal_one_class"]["source_record"])
    print("minimized source records:", len(ledger["minimized_source_records"]))
    print("elapsed: %.2fs" % elapsed)


if __name__ == "__main__":
    main()

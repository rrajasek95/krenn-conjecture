#!/usr/bin/env python3
"""CEGAR search for a sparse exact D12 separating dual.

This avoids materializing the full D12 Macaulay component.  It alternates
between solving the currently exposed column equations with target value one
and adding every column incident to the resulting nonzero dual support.
Completion is a global certificate: any unenumerated column has disjoint row
support and therefore zero pairing.
"""

from __future__ import annotations

import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

from audit_affine251_orbit import (
    T, IndependentEngine, build_actions, lift_rational_dual, parse_provider, sha256,
)


def sub_scaled(vector, rhs, source, source_rhs, factor, prime):
    for variable, coefficient in source.items():
        value = (vector.get(variable, 0) - factor * coefficient) % prime
        if value:
            vector[variable] = value
        else:
            vector.pop(variable, None)
    return (rhs - factor * source_rhs) % prime


def solve_fixed_target(columns, integer_vectors, target, prime):
    variables = sorted({row for column in columns for row in integer_vectors[column]} - {target})
    basis = {}
    for column in sorted(columns):
        raw = integer_vectors[column]
        vector = {row: value % prime for row, value in raw.items() if row != target and value % prime}
        rhs = (-raw.get(target, 0)) % prime
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                inverse = pow(vector[pivot], prime - 2, prime)
                vector = {row: value * inverse % prime for row, value in vector.items()}
                rhs = rhs * inverse % prime
                basis[pivot] = vector, rhs
                break
            record, record_rhs = basis[pivot]
            rhs = sub_scaled(vector, rhs, record, record_rhs, vector[pivot], prime)
        else:
            if rhs:
                return None
    solution = {}
    for pivot in sorted(basis, reverse=True):
        record, rhs = basis[pivot]
        value = rhs
        for variable, coefficient in record.items():
            if variable != pivot:
                value = (value - coefficient * solution.get(variable, 0)) % prime
        if value:
            solution[pivot] = value
    solution[target] = 1
    for column in columns:
        assert sum(value * solution.get(row, 0) for row, value in integer_vectors[column].items()) % prime == 0
    return solution


def search(engine, degree, prime, deadline):
    target = (T,) * degree
    support = {target: 1}
    columns = set()
    integer_vectors = {}
    records = []
    for round_index in range(100):
        if time.monotonic() >= deadline:
            return None, records, "WALL_CAP"
        incident = set()
        for row in support:
            if time.monotonic() >= deadline:
                return None, records, "WALL_CAP"
            incident.update(engine.incident(row))
        new_columns = incident - columns
        columns.update(incident)
        for column in new_columns:
            if time.monotonic() >= deadline:
                return None, records, "WALL_CAP"
            integer_vectors[column] = engine.invariant_column_integer(column)
        solution = solve_fixed_target(columns, integer_vectors, target, prime)
        if solution is None:
            return None, records, "CURRENT_COMPONENT_FORCES_TARGET"
        support = {row: value for row, value in solution.items() if value}
        violations = []
        for column in columns:
            pairing = sum(value * support.get(row, 0) for row, value in integer_vectors[column].items()) % prime
            if pairing:
                violations.append(column)
        assert not violations
        next_incident = set()
        for row in support:
            next_incident.update(engine.incident(row))
        records.append({
            "round": round_index + 1,
            "columns": len(columns),
            "new_columns": len(new_columns),
            "dual_support": len(support),
            "new_incident_columns": len(next_incident - columns),
        })
        print(json.dumps({"prime": prime, **records[-1]}, sort_keys=True), flush=True)
        if next_incident <= columns:
            return support, records, None
    return None, records, "ROUND_CAP"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--wall-seconds", type=int, default=600)
    args = parser.parse_args()
    assert 1 <= args.wall_seconds <= 1800
    started = time.monotonic()
    header, polynomials, term_index = parse_provider(args.input)
    engine = IndependentEngine(build_actions(header), polynomials, term_index)
    primes = (1073741827, 1073741789)
    searches = []
    supports = []
    for prime in primes:
        support, rounds, reason = search(engine, 12, prime, started + args.wall_seconds)
        searches.append({"prime": prime, "rounds": rounds, "status": "COMPLETE_DUAL" if support else reason})
        supports.append(support)
        if support is None:
            result = {
                "schema": "KRENN_AFFINE251_D12_SPARSE_DUAL_CEGAR_V1",
                "status": "INCOMPLETE_OR_TARGET_FORCED",
                "input_sha256": sha256(args.input),
                "searches": searches,
                "elapsed_seconds": time.monotonic() - started,
            }
            args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            print(json.dumps(result, indent=2, sort_keys=True))
            return
    all_rows = sorted(set(supports[0]) | set(supports[1]))
    ids = {row: index for index, row in enumerate(all_rows)}
    mod1 = {ids[row]: value for row, value in supports[0].items()}
    mod2 = {ids[row]: value for row, value in supports[1].items()}
    rational_ids = lift_rational_dual(mod1, mod2, primes[0], primes[1])
    rational = {all_rows[row]: value for row, value in rational_ids.items()}
    assert rational[(T,) * 12] == 1
    incident = set()
    for row in rational:
        incident.update(engine.incident(row))
    for column in incident:
        values = engine.invariant_column_integer(column)
        assert sum(value * rational.get(row, Fraction(0)) for row, value in values.items()) == 0
    result = {
        "schema": "KRENN_AFFINE251_D12_SPARSE_DUAL_CEGAR_V1",
        "status": "COMPLETE_EXACT_RATIONAL_DUAL",
        "input_sha256": sha256(args.input),
        "searches": searches,
        "rational_support": len(rational),
        "maximum_denominator": max(value.denominator for value in rational.values()),
        "incident_column_orbits_exactly_checked": len(incident),
        "target_pairing": "1",
        "global_annihilation": True,
        "elapsed_seconds": time.monotonic() - started,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

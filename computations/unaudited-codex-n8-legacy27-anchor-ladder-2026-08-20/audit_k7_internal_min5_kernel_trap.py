#!/usr/bin/env python3
"""Audit the internal minimum-degree-five kernel omitted by a chosen section."""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROBE_PATH = HERE / "probe_legacy27_k6_orbits.py"
SPEC = importlib.util.spec_from_file_location("legacy27_min5_trap", PROBE_PATH)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)
BASE = PROBE.BASE
OUT = HERE / "results_k7_internal_min5_kernel_trap.json"
PRIMES = (1009, 1013)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def degree_tail(column, degree):
    return Counter(
        PROBE.canonical_row(row)
        for row in BASE.column_rows(column)
        if BASE.row_degree(row, PROBE.ANCHORS) == degree
    )


def rank(vectors, prime):
    basis = {}
    for raw in vectors:
        vector = {row: value % prime for row, value in raw.items()
                  if value % prime}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, prime)
                basis[pivot] = {row: entry * inverse % prime
                                for row, entry in vector.items()}
                break
            for row, entry in basis[pivot].items():
                updated = (vector.get(row, 0) - value * entry) % prime
                if updated:
                    vector[row] = updated
                else:
                    vector.pop(row, None)
    return len(basis)


def column_record(column):
    return {
        "word": "".join(map(str, column[0])),
        "multiplier_cell_ids": list(column[1]),
        "multiplier": [BASE.cell_name(BASE.CELLS[cell])
                       for cell in column[1]],
        "column_orbit_size": len(PROBE.column_orbit(column)),
    }


def audit():
    data = PROBE.degree5_orbit_closure()
    singleton_columns = defaultdict(list)
    triples = []
    for column in data["columns5"]:
        outputs = degree_tail(column, 5)
        require(sum(outputs.values()) in (1, 3),
                "degree-five leading mass changed")
        require(all(value == 1 for value in outputs.values()),
                "degree-five leading row-orbit multiplicity changed")
        if len(outputs) == 1:
            singleton_columns[next(iter(outputs))].append(column)
        else:
            triples.append((outputs, column))
    singleton_rows = set(singleton_columns)
    non_rows = tuple(sorted(set(data["rows5"]) - singleton_rows))
    non_index = {row: index for index, row in enumerate(non_rows)}
    projected_triples = [
        Counter({non_index[row]: value for row, value in outputs.items()
                 if row in non_index})
        for outputs, _column in triples
    ]
    projected_triples = [vector for vector in projected_triples if vector]
    ranks = {str(prime): rank(projected_triples, prime) for prime in PRIMES}
    require(ranks == {"1009": 751, "1013": 751},
            "coupled triple rank changed")
    leading_rank = len(singleton_rows) + ranks["1009"]
    internal_nullity = len(data["columns5"]) - leading_rank
    require((leading_rank, internal_nullity) == (44537, 96310),
            "minimum-degree-five rank/nullity changed")

    duplicate_rows = {
        row: tuple(sorted(columns, key=repr))
        for row, columns in singleton_columns.items() if len(columns) >= 2
    }
    require(duplicate_rows, "duplicate singleton columns disappeared")
    witness = None
    for row in sorted(duplicate_rows):
        columns = duplicate_rows[row]
        for left_number, left in enumerate(columns):
            left6 = degree_tail(left, 6)
            for right in columns[left_number + 1:]:
                right6 = degree_tail(right, 6)
                difference = Counter(left6)
                difference.subtract(right6)
                difference = Counter({key: value for key, value in
                                      difference.items() if value})
                if difference:
                    witness = (row, left, right, difference)
                    break
            if witness:
                break
        if witness:
            break
    require(witness is not None,
            "duplicate singleton relation lost its degree-six tail")
    row, left, right, difference = witness
    leading_difference = Counter(degree_tail(left, 5))
    leading_difference.subtract(degree_tail(right, 5))
    leading_difference = Counter({key: value for key, value in
                                  leading_difference.items() if value})
    require(not leading_difference,
            "witness is not an exact internal degree-five kernel relation")
    require(difference, "witness degree-six must-fire tail vanished")

    total_source_columns = len(data["lower_columns"]) + len(data["columns5"])
    full_cutoff_rank = 3864 + leading_rank
    full_cutoff_kernel = total_source_columns - full_cutoff_rank
    require((total_source_columns, full_cutoff_rank, full_cutoff_kernel)
            == (154665, 48401, 106264),
            "full cutoff<6 dimension ledger changed")
    core = {
        "status": "UNAUDITED exact scope audit; no K7 membership claim",
        "zero_based_chart": 30,
        "legacy_one_based_chart": 27,
        "minimum_degree5_row_column_orbits": [
            len(data["rows5"]), len(data["columns5"])
        ],
        "singleton_columns": sum(len(value)
                                 for value in singleton_columns.values()),
        "distinct_singleton_rows": len(singleton_rows),
        "rows_with_duplicate_singleton_columns": len(duplicate_rows),
        "projected_triple_columns": len(projected_triples),
        "projected_triple_rank": ranks,
        "minimum_degree5_leading_rank": leading_rank,
        "minimum_degree5_internal_kernel_dimension": internal_nullity,
        "full_cutoff_source_columns_rank_kernel": [
            total_source_columns, full_cutoff_rank, full_cutoff_kernel
        ],
        "chosen_corrected_lower_kernel_dimension": 9954,
        "omitted_internal_kernel_dimension": internal_nullity,
        "duplicate_singleton_witness": {
            "common_leading_row_hex": row.hex(),
            "left": column_record(left),
            "right": column_record(right),
            "degree5_difference_zero": True,
            "degree6_difference": [[output.hex(), value]
                                   for output, value in sorted(difference.items())],
            "degree6_difference_nnz": len(difference),
            "degree6_difference_sha256": sha256(json.dumps(
                [[output.hex(), value] for output, value in sorted(difference.items())],
                separators=(",", ":")
            ).encode("ascii")).hexdigest(),
        },
        "conclusion": (
            "the 9954 chosen-section transfers are incomplete; a sound K7 "
            "test must include all 106264 cutoff<6 kernel directions or use "
            "the whole cutoff<7 source component"
        ),
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("legacy27 internal min-d5 kernel trap: PASS")
    print("full kernel:",
          result["full_cutoff_source_columns_rank_kernel"][-1])
    print("witness d6 nnz:",
          result["duplicate_singleton_witness"]["degree6_difference_nnz"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact relative incidence audit of the eight new unpivotable c7 rows."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C6_DIR = ROOT / "computations/unaudited-codex-orbit0-k16-c6-schur-boundary-2026-08-23"
C6_SCRIPT = C6_DIR / "audit_k16_c6_schur_boundary.py"
SCHUR = HERE / "results_c6_boundary_schur_lift.json"
OUT = HERE / "results_unpivotable_c7_boundary.json"
TIME_CAP = 175.0
ROW_OCCURRENCE_CAP = 100_000


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def rank_q(vectors):
    basis = {}
    for source in vectors:
        value = {row: Fraction(coefficient)
                 for row, coefficient in enumerate(source) if coefficient}
        while value:
            pivot = min(value)
            if pivot not in basis:
                scale = value[pivot]
                basis[pivot] = {row: coefficient / scale
                                for row, coefficient in value.items()}
                break
            scale = value[pivot]
            for row, coefficient in basis[pivot].items():
                updated = value.get(row, 0) - scale * coefficient
                if updated:
                    value[row] = updated
                else:
                    value.pop(row, None)
    return len(basis)


def primitive(vector):
    divisor = 0
    for value in vector:
        divisor = gcd(divisor, abs(value))
    require(divisor, vector)
    reduced = tuple(value // divisor for value in vector)
    if next(value for value in reduced if value) < 0:
        reduced = tuple(-value for value in reduced)
    return reduced


def parse_fraction(text):
    return Fraction(text)


def main():
    started = time.monotonic()
    C6 = load("unpivotable_c7_c6", C6_SCRIPT)
    HQ, D24 = C6.HQ, C6.D24
    schur = json.loads(SCHUR.read_text())
    records = schur["uncertified_high_rows"]
    require(len(records) == 8, len(records))
    rows = tuple(bytes.fromhex(record["row"]) for record in records)
    row_index = {row: index for index, row in enumerate(rows)}
    require(len(row_index) == 8, len(row_index))
    target = tuple(parse_fraction(record["coefficient"]) for record in records)

    failure_profiles = []
    all_columns = set()
    for record, row in zip(records, rows, strict=True):
        require(C6.eligible_pivot(row) is None, row.hex())
        partition, cycle_ids = C6.graph_data(row)
        incident = D24.incident_degree24_columns(row)
        distinct_cycle_histogram = Counter()
        word_profile_histogram = Counter()
        for word, multiplier in incident:
            remaining = list(row)
            for cell in multiplier:
                remaining.remove(cell)
            require(len(remaining) == 4, (row.hex(), len(remaining)))
            selected_cycles = []
            for cell in remaining:
                u, v, a, b = D24.BASE.CELLS[cell]
                require(cycle_ids[3 * u + a] == cycle_ids[3 * v + b],
                        (row.hex(), cell))
                selected_cycles.append(cycle_ids[3 * u + a])
            distinct_cycle_histogram[len(set(selected_cycles))] += 1
            word_profile_histogram[tuple(sorted(Counter(word).values(),
                                                   reverse=True))] += 1
            all_columns.add((word, multiplier))
        require(max(distinct_cycle_histogram, default=0) < 4,
                (row.hex(), distinct_cycle_histogram))
        failure_profiles.append({
            "row": row.hex(),
            "K_degree": record["K_degree"],
            "cycle_partition": list(partition),
            "incident_mixed_columns": len(incident),
            "selected_distinct_cycle_count_histogram": {
                str(key): value for key, value in sorted(distinct_cycle_histogram.items())
            },
            "maximum_distinct_cycles_in_physical_PM_divisor":
                max(distinct_cycle_histogram, default=0),
            "word_profile_histogram": {
                "+".join(map(str, key)): value
                for key, value in sorted(word_profile_histogram.items())
            },
            "failure": (
                "Every literal mixed physical perfect-matching divisor reuses "
                "at least one port-cycle; none selects four distinct cycles."
            ),
        })

    all_columns = tuple(sorted(all_columns, key=lambda value: (value[0], value[1])))
    column_vectors = []
    column_outputs = []
    parent_incidence = defaultdict(dict)
    raw_occurrences = 0
    unique_projected_rows = set()
    for column_index, column in enumerate(all_columns):
        outputs = D24.degree24_column_rows(column)
        raw_occurrences += len(outputs)
        projected = Counter()
        literal = Counter()
        for output in outputs:
            if D24.row_k_degree(output) > 16:
                continue
            literal[output] += 1
            canonical = HQ.canonical_row(output)
            unique_projected_rows.add(canonical)
            if canonical in row_index:
                projected[row_index[canonical]] += 1
            if len(C6.graph_data(output)[0]) > 7:
                parent_incidence[output][column_index] = (
                    parent_incidence[output].get(column_index, 0) + 1)
        vector = tuple(projected.get(index, 0) for index in range(8))
        column_vectors.append(vector)
        column_outputs.append(literal)
        require(raw_occurrences <= ROW_OCCURRENCE_CAP,
                ("row occurrence cap", raw_occurrences))

    direct_vectors = tuple(sorted(set(column_vectors)))
    direct_rank = rank_q(direct_vectors)
    direct_augmented = rank_q(direct_vectors + (target,))
    direct_coverage = sum(any(vector[index] for vector in direct_vectors)
                          for index in range(8))

    pair_vectors = set()
    common_parents = 0
    pair_count = 0
    for parent, incidence in parent_incidence.items():
        items = sorted(incidence.items())
        if len(items) < 2:
            continue
        common_parents += 1
        for left_position, (left_index, left_coefficient) in enumerate(items):
            for right_index, right_coefficient in items[left_position + 1:]:
                pair_count += 1
                vector = tuple(
                    right_coefficient * column_vectors[left_index][coordinate]
                    - left_coefficient * column_vectors[right_index][coordinate]
                    for coordinate in range(8))
                if any(vector):
                    pair_vectors.add(primitive(vector))
    pair_vectors = tuple(sorted(pair_vectors))
    pair_rank = rank_q(pair_vectors)
    pair_augmented = rank_q(pair_vectors + (target,))
    combined_rank = rank_q(direct_vectors + pair_vectors)
    combined_augmented = rank_q(direct_vectors + pair_vectors + (target,))

    result = {
        "schema": "orbit0-k16-unpivotable-c7-relative-incidence-v1",
        "status": "EXACT_RELATIVE_8_COORDINATE_INTERFACE",
        "boundary_rows": 8,
        "failure_profiles": failure_profiles,
        "distinct_literal_incident_mixed_columns": len(all_columns),
        "literal_output_occurrences_examined": raw_occurrences,
        "unique_H_projected_output_rows": len(unique_projected_rows),
        "direct_projection": {
            "distinct_vectors": len(direct_vectors),
            "coverage": direct_coverage,
            "rank_over_Q": direct_rank,
            "target_augmented_rank_over_Q": direct_augmented,
            "target_in_span": direct_augmented == direct_rank,
        },
        "common_parent_projection": {
            "higher_cycle_literal_common_parents": common_parents,
            "literal_column_pairs": pair_count,
            "distinct_primitive_vectors": len(pair_vectors),
            "rank_over_Q": pair_rank,
            "target_augmented_rank_over_Q": pair_augmented,
            "target_in_span": pair_augmented == pair_rank,
        },
        "combined_projection": {
            "rank_over_Q": combined_rank,
            "target_augmented_rank_over_Q": combined_augmented,
            "target_in_span": combined_augmented == combined_rank,
        },
        "scope": (
            "All literal mixed degree24 columns incident to the eight frozen "
            "c7 H-orbit representatives, plus critical pairs among those columns "
            "that already share a literal c>7 output. Ranks concern only the "
            "eight-coordinate projection; exterior tails and c<=6 rows are not "
            "eliminated, so no global membership conclusion follows."
        ),
        "pinned_schur_logical": schur["logical_sha256"],
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(result)
    logical.pop("elapsed_seconds")
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "columns": len(all_columns),
        "row_occurrences": raw_occurrences,
        "direct": result["direct_projection"],
        "pairs": result["common_parent_projection"],
        "combined": result["combined_projection"],
        "logical_sha256": result["logical_sha256"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

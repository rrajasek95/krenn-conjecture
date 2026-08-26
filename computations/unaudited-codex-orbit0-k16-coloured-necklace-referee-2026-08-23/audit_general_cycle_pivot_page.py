#!/usr/bin/env python3
"""One exact all-cycle distinct-four pivot page on the frozen 884-row residual."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import lcm
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C6_DIR = ROOT / "computations/unaudited-codex-orbit0-k16-c6-schur-boundary-2026-08-23"
C6_SCRIPT = C6_DIR / "audit_k16_c6_schur_boundary.py"
SOURCE_RESULT = HERE / "results_c7_certified_reduction.json"
SOURCE_RESIDUAL = HERE / "c7_certified_reduction_residual.tsv"
OUT = HERE / "results_general_cycle_pivot_page.json"
FINAL = HERE / "general_cycle_pivot_final_residual.tsv"
TIME_CAP = 145.0
ROW_CAP = 100_000


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def remove_cells(row, cells):
    remaining = list(row)
    for cell in cells:
        remaining.remove(cell)
    return bytes(sorted(remaining))


def main():
    started = time.monotonic()
    C6 = load("general_cycle_pivot_c6", C6_SCRIPT)
    HQ, D24 = C6.HQ, C6.D24
    source = json.loads(SOURCE_RESULT.read_text())
    lines = SOURCE_RESIDUAL.read_text().splitlines()
    require(lines[0] == "row\tcoefficient", lines[0])
    residual = Counter()
    for line in lines[1:]:
        row_hex, coefficient = line.split("\t")
        residual[bytes.fromhex(row_hex)] = Fraction(coefficient)
    require(len(residual) == source["remaining_support"] == 884,
            (len(residual), source["remaining_support"]))
    require(sha256(SOURCE_RESIDUAL.read_bytes()).hexdigest() ==
            source["exported_residual_tsv_sha256"], "source residual digest drift")

    eligible_cache = {}

    def eligible(row):
        value = eligible_cache.get(row, False)
        if row not in eligible_cache:
            value = C6.eligible_pivot(row)
            eligible_cache[row] = value
        return value

    def profile(rows, with_pivotability=False):
        answer = Counter()
        for row in rows:
            degree = D24.row_k_degree(row)
            partition = C6.graph_data(row)[0]
            key = (degree, partition, bool(eligible(row))) if with_pivotability else (
                degree, partition)
            answer[key] += 1
        formatted = {}
        for key, count in sorted(answer.items()):
            if with_pivotability:
                degree, partition, pivotable = key
                text = f"K{degree}|{'-'.join(map(str, partition))}|" + (
                    "pivotable" if pivotable else "unpivotable")
            else:
                degree, partition = key
                text = f"K{degree}|{'-'.join(map(str, partition))}"
            formatted[text] = count
        return formatted

    initial_profile = profile(residual, with_pivotability=True)
    initial_pivotable = sum(bool(eligible(row)) for row in residual)
    initial_unpivotable = len(residual) - initial_pivotable

    buckets = defaultdict(set)
    for row in residual:
        if eligible(row):
            buckets[len(C6.graph_data(row)[0])].add(row)

    column_cache = {}

    def projected_column(column):
        value = column_cache.get(column)
        if value is None:
            value = Counter()
            for output in D24.degree24_column_rows(column):
                if D24.row_k_degree(output) <= 16:
                    value[HQ.canonical_row(output)] += 1
            column_cache[column] = value
        return value

    pivot_uses = 0
    output_occurrences = 0
    maximum_support = len(residual)
    pivot_cycle_histogram = Counter()
    while buckets:
        cycle_count = max(buckets)
        if not buckets[cycle_count]:
            del buckets[cycle_count]
            continue
        row = max(buckets[cycle_count])
        buckets[cycle_count].remove(row)
        if not buckets[cycle_count]:
            del buckets[cycle_count]
        if row not in residual:
            continue
        pivot = eligible(row)
        require(pivot is not None, row.hex())
        word, selected = pivot
        column = (word, remove_cells(row, selected))
        value = projected_column(column)
        output_occurrences += sum(value.values())
        parent_coefficient = value[row]
        require(parent_coefficient > 0, (row.hex(), parent_coefficient))
        require(all(len(C6.graph_data(child)[0]) < cycle_count
                    for child in value if child != row),
                ("nontriangular relation", row.hex(), cycle_count))
        factor = residual[row] / parent_coefficient
        for child, coefficient in value.items():
            existed = child in residual
            residual[child] -= factor * coefficient
            if residual[child] == 0:
                residual.pop(child)
                child_cycles = len(C6.graph_data(child)[0])
                buckets[child_cycles].discard(child)
                if child_cycles in buckets and not buckets[child_cycles]:
                    del buckets[child_cycles]
            elif not existed and eligible(child):
                buckets[len(C6.graph_data(child)[0])].add(child)
        pivot_uses += 1
        pivot_cycle_histogram[cycle_count] += 1
        maximum_support = max(maximum_support, len(residual))
        require(len(residual) <= ROW_CAP, ("row cap", len(residual)))
        require(time.monotonic() - started < TIME_CAP,
                ("time cap", pivot_uses, len(residual)))

    require(all(eligible(row) is None for row in residual),
            "pivotable row survived exhaustive page")
    final_profile = profile(residual, with_pivotability=False)
    final_cycle_histogram = Counter(len(C6.graph_data(row)[0]) for row in residual)
    payload = "row\tcoefficient\n" + "".join(
        f"{row.hex()}\t{coefficient}\n"
        for row, coefficient in sorted(residual.items()))
    FINAL.write_text(payload)

    result = {
        "schema": "orbit0-k16-general-four-cycle-pivot-page-v1",
        "status": "EXACT_ONE_PAGE_TO_NONPIVOTABLE_CORE",
        "initial_support": 884,
        "initial_pivotable_rows": initial_pivotable,
        "initial_unpivotable_rows": initial_unpivotable,
        "initial_profile": initial_profile,
        "pivot_uses": pivot_uses,
        "pivot_cycle_count_histogram": {
            str(key): value for key, value in sorted(pivot_cycle_histogram.items())
        },
        "distinct_pivot_columns": len(column_cache),
        "projected_output_occurrences": output_occurrences,
        "maximum_intermediate_support": maximum_support,
        "final_support": len(residual),
        "final_cycle_count_histogram": {
            str(key): value for key, value in sorted(final_cycle_histogram.items())
        },
        "final_profile": final_profile,
        "final_coefficient_l1": str(sum(abs(value) for value in residual.values())),
        "final_max_numerator": max((abs(value.numerator)
                                    for value in residual.values()), default=0),
        "final_lcm_denominator": lcm(
            *(value.denominator for value in residual.values())) if residual else 1,
        "final_residual_tsv_sha256": sha256(payload.encode()).hexdigest(),
        "scope": (
            "One exhaustive descending page using the exact mixed physical-PM "
            "criterion selecting four distinct port cycles, applied at every "
            "cycle count in the K<=16 H-coinvariant quotient. The output is "
            "nonpivotable for this criterion only; no further source closure "
            "or ideal-membership claim is made."
        ),
        "pinned_source_logical": source["logical_sha256"],
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(result)
    logical.pop("elapsed_seconds")
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "initial_pivotable_rows", "initial_unpivotable_rows",
        "pivot_uses", "pivot_cycle_count_histogram",
        "maximum_intermediate_support", "final_support",
        "final_cycle_count_histogram", "logical_sha256", "elapsed_seconds")},
        indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

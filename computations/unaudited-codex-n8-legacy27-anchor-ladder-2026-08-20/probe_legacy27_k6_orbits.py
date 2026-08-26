#!/usr/bin/env python3
"""Exact stabilizer-orbit census for legacy chart 27 at K-anchor degree five.

Zero-based chart 30 is loaded from the pinned raw 31-orbit ledger through the
source-faithful other-27 checker.  The six-element group below is the complete
stabilizer of the twelve *named* anchors.  Orbit reduction in this file is a
finite exact census only; it makes no membership or chart-closure claim.
"""

from __future__ import annotations

from collections import Counter, deque
from functools import lru_cache
from hashlib import sha256
from itertools import permutations
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = (
    HERE.parent / "unaudited-codex-n8-other27-kadic-2026-08-20"
    / "scan_other27_kadic.py"
)
SPEC = importlib.util.spec_from_file_location("legacy27_raw", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
OUT = HERE / "results_k6_orbit_census.json"
CHART = 30
CHARTS, LEGACY, UPSTREAM_SHA256 = BASE.load_charts()
MATCHINGS = CHARTS[CHART]
ANCHORS = BASE.anchor_ids(MATCHINGS)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def transform_cell(cell, site_permutation, colour_permutation):
    u, v, a, b = cell
    pu, pv = site_permutation[u], site_permutation[v]
    pa, pb = colour_permutation[a], colour_permutation[b]
    if pu < pv:
        return pu, pv, pa, pb
    return pv, pu, pb, pa


def build_stabilizer():
    anchor_cells = frozenset(BASE.CELLS[index] for index in ANCHORS)
    answer = []
    for site_permutation in permutations(range(BASE.N)):
        for colour_permutation in permutations(BASE.COLORS):
            image = frozenset(transform_cell(
                cell, site_permutation, colour_permutation
            ) for cell in anchor_cells)
            if image == anchor_cells:
                answer.append((site_permutation, colour_permutation))
    require(len(answer) == 6,
            "legacy27 named-anchor stabilizer is no longer order six")
    return tuple(answer)


STABILIZER = build_stabilizer()
TRANSFORMS = tuple(bytes(
    BASE.CELL_ID[transform_cell(cell, sites, colours)]
    for cell in BASE.CELLS
) for sites, colours in STABILIZER)


@lru_cache(maxsize=None)
def canonical_row(row):
    return min(bytes(sorted(transform[cell] for cell in row))
               for transform in TRANSFORMS)


def transform_column(column, action):
    word, multiplier = column
    sites, colours = STABILIZER[action]
    transformed_word = [None] * BASE.N
    for site, colour in enumerate(word):
        transformed_word[sites[site]] = colours[colour]
    transformed_multiplier = bytes(sorted(
        TRANSFORMS[action][cell] for cell in multiplier
    ))
    return tuple(transformed_word), transformed_multiplier


@lru_cache(maxsize=None)
def column_orbit(column):
    return tuple(sorted({transform_column(column, action)
                         for action in range(len(STABILIZER))}, key=repr))


@lru_cache(maxsize=None)
def canonical_column(column):
    return column_orbit(column)[0]


def column_minimum_degree(column):
    return min(BASE.row_degree(row, ANCHORS)
               for row in BASE.column_rows(column))


def target_exact(degree):
    high = BASE.filtered_target(MATCHINGS, degree + 1)
    low = BASE.filtered_target(MATCHINGS, degree)
    answer = Counter(high)
    answer.subtract(low)
    answer = Counter({row: value for row, value in answer.items() if value})
    require(all(BASE.row_degree(row, ANCHORS) == degree for row in answer),
            "exact target-degree subtraction leaked")
    return answer


def lower_through_degree4():
    anchors, target, rows, columns, truncated = BASE.complete_component(
        MATCHINGS, 5
    )
    require(anchors == ANCHORS, "lower anchor set changed")
    require(all(BASE.row_degree(row, ANCHORS) < 5 for row in rows),
            "lower component leaked degree five")
    require(all(min(BASE.row_degree(row, ANCHORS) for row in outputs) < 5
                for outputs in truncated), "lower column minimum changed")
    return target, rows, columns


def degree5_orbit_closure():
    lower_target, lower_rows, lower_columns_actual = lower_through_degree4()
    lower_columns = tuple(sorted({canonical_column(column)
                                  for column in lower_columns_actual}, key=repr))
    target5 = target_exact(5)
    rows = {canonical_row(row) for row in target5}
    for column in lower_columns:
        rows.update(canonical_row(row) for row in BASE.column_rows(column)
                    if BASE.row_degree(row, ANCHORS) == 5)
    start_count = len(rows)
    frontier = deque(sorted(rows))
    columns = set()
    layers = []
    while frontier:
        layer_size = len(frontier)
        new_rows = set()
        before_columns = len(columns)
        for _ in range(layer_size):
            row = frontier.popleft()
            for raw_column in BASE.incident_columns(row):
                column = canonical_column(raw_column)
                if column in columns:
                    continue
                if column_minimum_degree(column) != 5:
                    continue
                columns.add(column)
                for output in BASE.column_rows(column):
                    if BASE.row_degree(output, ANCHORS) != 5:
                        continue
                    representative = canonical_row(output)
                    if representative not in rows:
                        rows.add(representative)
                        new_rows.add(representative)
        frontier.extend(sorted(new_rows))
        layers.append((len(new_rows), len(columns) - before_columns))
        print(
            f"layer {len(layers)}: new row orbits={len(new_rows)}, "
            f"new column orbits={len(columns) - before_columns}, "
            f"totals={len(rows)}/{len(columns)}",
            flush=True,
        )
    return {
        "lower_target": lower_target,
        "lower_rows_actual": lower_rows,
        "lower_columns_actual": lower_columns_actual,
        "lower_columns": lower_columns,
        "target5": target5,
        "rows5": tuple(sorted(rows)),
        "columns5": tuple(sorted(columns, key=repr)),
        "start_count": start_count,
        "layers": layers,
    }


def audit():
    data = degree5_orbit_closure()
    actual_histogram = Counter()
    orbit_histogram = Counter()
    multiplicity_histogram = Counter()
    for column in data["columns5"]:
        outputs = tuple(row for row in BASE.column_rows(column)
                        if BASE.row_degree(row, ANCHORS) == 5)
        canonical = tuple(canonical_row(row) for row in outputs)
        actual_histogram[len(outputs)] += 1
        orbit_histogram[len(set(canonical))] += 1
        multiplicity_histogram[tuple(sorted(Counter(canonical).values()))] += 1
    core = {
        "status": "UNAUDITED exact orbit census; no membership claim",
        "zero_based_chart": CHART,
        "legacy_one_based_chart": LEGACY[CHART],
        "upstream_raw_matching_sha256": UPSTREAM_SHA256,
        "anchor_names": [BASE.cell_name(BASE.CELLS[cell])
                         for cell in sorted(ANCHORS)],
        "stabilizer_order": len(STABILIZER),
        "lower_actual_rows_through_degree4": len(data["lower_rows_actual"]),
        "lower_actual_columns_through_degree4": len(data["lower_columns_actual"]),
        "lower_column_orbits_through_degree4": len(data["lower_columns"]),
        "degree5_target_actual_rows": len(data["target5"]),
        "degree5_start_row_orbits": data["start_count"],
        "degree5_closed_row_orbits": len(data["rows5"]),
        "degree5_closed_column_orbits": len(data["columns5"]),
        "closure_layers": data["layers"],
        "minimum_degree5_actual_leading_count": {
            str(key): value for key, value in sorted(actual_histogram.items())
        },
        "minimum_degree5_distinct_row_orbit_count": {
            str(key): value for key, value in sorted(orbit_histogram.items())
        },
        "minimum_degree5_row_orbit_multiplicity_patterns": {
            ",".join(map(str, key)): value
            for key, value in sorted(multiplicity_histogram.items())
        },
        "full_chart_controlled": False,
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
    print("legacy27 K6 orbit census: PASS")
    print("row/column orbits:", result["degree5_closed_row_orbits"],
          result["degree5_closed_column_orbits"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()

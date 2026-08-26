#!/usr/bin/env python3
"""Stabilizer-orbit cost probe for the chart-26 K-degree-five frontier.

Chart 26 here is zero-based quotient chart 26, i.e. legacy one-based chart
29.  The script computes the exact row/column orbit closure under the full
stabilizer of its twelve named anchors.  It is a structural census, not a
rank or membership claim.
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
BASE_PATH = HERE / "audit_dangerous_charts.py"
SPEC = importlib.util.spec_from_file_location("dangerous_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
OUT = HERE / "results_degree5_chart26_orbit.json"
CHART = 26
MATCHINGS = BASE.CHARTS[CHART]
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
    require(len(answer) == 16,
            "chart-26 anchor stabilizer is no longer order sixteen")
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


def lower_through_degree4():
    anchors = ANCHORS
    seeds = BASE.seed_columns(MATCHINGS)
    lower = seeds
    records = {}
    for degree in (2, 3, 4):
        target = BASE.filtered_target(MATCHINGS, degree)
        start = set(target)
        for column in lower:
            start.update(row for row in BASE.column_rows(column)
                         if BASE.row_degree(row, anchors) == degree)
        rows, columns = BASE.close_exact_degree(start, anchors, degree)
        records[degree] = (rows, columns)
        lower = lower + tuple(sorted(columns, key=repr))
    return lower, records


def audit():
    lower, records = lower_through_degree4()
    target5 = BASE.filtered_target(MATCHINGS, 5)
    actual_start = set(target5)
    lower_tail_histogram = Counter()
    for column in lower:
        outputs = tuple(row for row in BASE.column_rows(column)
                        if BASE.row_degree(row, ANCHORS) == 5)
        lower_tail_histogram[len(outputs)] += 1
        actual_start.update(outputs)
    rows = {canonical_row(row) for row in actual_start}
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
                if BASE.column_minimum_degree(column, ANCHORS) != 5:
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

    leading_actual_histogram = Counter()
    leading_row_orbit_histogram = Counter()
    for column in columns:
        outputs = tuple(row for row in BASE.column_rows(column)
                        if BASE.row_degree(row, ANCHORS) == 5)
        leading_actual_histogram[len(outputs)] += 1
        leading_row_orbit_histogram[len({canonical_row(row) for row in outputs})] += 1
    core = {
        "status": "UNAUDITED exact orbit census; no rank/membership claim",
        "chart": CHART,
        "legacy_one_based_chart": 29,
        "stabilizer_order": len(STABILIZER),
        "lower_actual_columns_through_degree4": len(lower),
        "degree5_target_actual_rows": len(target5),
        "degree5_start_actual_rows": len(actual_start),
        "degree5_start_row_orbits": len({canonical_row(row) for row in actual_start}),
        "degree5_closed_row_orbits": len(rows),
        "degree5_closed_column_orbits": len(columns),
        "closure_layers": layers,
        "lower_tail_actual_term_histogram": {
            str(k): value for k, value in sorted(lower_tail_histogram.items())
        },
        "minimum_degree5_column_actual_leading_term_histogram": {
            str(k): value for k, value in sorted(leading_actual_histogram.items())
        },
        "minimum_degree5_column_leading_row_orbit_histogram": {
            str(k): value for k, value in sorted(leading_row_orbit_histogram.items())
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
    print("chart26 degree5 orbit census: PASS")
    print("row/column orbits:", result["degree5_closed_row_orbits"],
          result["degree5_closed_column_orbits"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()

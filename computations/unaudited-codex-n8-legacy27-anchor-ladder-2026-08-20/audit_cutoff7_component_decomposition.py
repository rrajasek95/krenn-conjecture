#!/usr/bin/env python3
"""Connected-component and hypergraph census of the cutoff-seven core."""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
INTERFACE = HERE / "legacy27_cutoff7_direct.jsonl"
OUT = HERE / "results_cutoff7_component_decomposition.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def audit():
    with INTERFACE.open() as handle:
        header = json.loads(next(handle))
        row_count = header["row_count"]
        parent = list(range(row_count))
        sizes = [1] * row_count

        def find(value):
            while parent[value] != value:
                parent[value] = parent[parent[value]]
                value = parent[value]
            return value

        def union(left, right):
            left, right = find(left), find(right)
            if left == right:
                return
            if sizes[left] < sizes[right]:
                left, right = right, left
            parent[right] = left
            sizes[left] += sizes[right]

        supports = []
        support_histogram = Counter()
        mass_histogram = Counter()
        multiplicity_columns = 0
        for expected, raw in enumerate(handle):
            record = json.loads(raw)
            require(record["index"] == expected, "column order changed")
            support = tuple(index for index, _value in record["entries"])
            mass = sum(value for _index, value in record["entries"])
            require(len(support) >= 2, "coupled core retained singleton")
            supports.append(support)
            support_histogram[len(support)] += 1
            mass_histogram[mass] += 1
            multiplicity_columns += mass != len(support)
            for row in support[1:]:
                union(support[0], row)
    row_components = Counter(find(row) for row in range(row_count))
    column_components = Counter(find(support[0]) for support in supports)
    target_components = defaultdict(list)
    for index, numerator, denominator in header["target"]:
        require(denominator == 1, "target denominator changed")
        target_components[find(index)].append((index, numerator))
    records = []
    for root, rows in row_components.items():
        records.append({
            "root": root,
            "rows": rows,
            "columns": column_components[root],
            "target_nonzeros": len(target_components[root]),
            "target_absolute_mass": sum(abs(value) for _index, value
                                        in target_components[root]),
        })
    records.sort(key=lambda item: (-item["rows"], item["root"]))
    require(len(records) == len(target_components) == 1,
            "legacy27 coupled core unexpectedly split")
    require(records[0] == {
        "root": records[0]["root"],
        "rows": 44741,
        "columns": 77265,
        "target_nonzeros": 427,
        "target_absolute_mass": 2447,
    }, "legacy27 target component census changed")
    core = {
        "status": "UNAUDITED exact interface incidence census",
        "zero_based_chart": 30,
        "legacy_one_based_chart": 27,
        "components": records,
        "component_count": len(records),
        "target_bearing_component_count": len(target_components),
        "distinct_support_size_histogram": {
            str(key): value for key, value in sorted(support_histogram.items())
        },
        "multiplicity_mass_histogram": {
            str(key): value for key, value in sorted(mass_histogram.items())
        },
        "graph_columns_support_two": support_histogram[2],
        "hypergraph_columns_support_at_least_three": sum(
            value for key, value in support_histogram.items() if key >= 3
        ),
        "hypergraph_columns_support_at_least_four": sum(
            value for key, value in support_histogram.items() if key >= 4
        ),
        "maximum_distinct_support": max(support_histogram),
        "maximum_multiplicity_mass": max(mass_histogram),
        "columns_with_nontrivial_orbit_multiplicity": multiplicity_columns,
        "parallel_component_split_available": False,
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
    print("legacy27 cutoff7 component census: PASS")
    print("components:", result["component_count"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Export the complete legacy27 K^6 augmented orbit system.

Rows consist of every lower (K-degree <5) row orbit plus every exact left
nullvector of the minimum-degree-five coupled quotient.  Columns are all
lower-column orbits.  Counts are literal multiplicities of a representative
column.  The target is scaled by labelled row-orbit sizes, matching group
average expansion.  This JSON is a deterministic interchange for independent
sparse solvers; it is not itself a membership claim.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_legacy27_k6_exact.py"
SPEC = importlib.util.spec_from_file_location("legacy27_exact", AUDIT_PATH)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)
PROBE = AUDIT.PROBE
BASE = AUDIT.BASE
OUT = HERE / "k6_augmented_matrix.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def quotient_data(data):
    singleton = {}
    triples = []
    for column in data["columns5"]:
        outputs = tuple(PROBE.canonical_row(row)
                        for row in BASE.column_rows(column)
                        if BASE.row_degree(row, PROBE.ANCHORS) == 5)
        require(len(outputs) in (1, 3) and len(outputs) == len(set(outputs)),
                "degree-five leading multiplicity split changed")
        if len(outputs) == 1:
            singleton.setdefault(outputs[0], column)
        else:
            triples.append((outputs, column))
    non_rows = tuple(sorted(set(data["rows5"]) - set(singleton)))
    non_set = set(non_rows)
    unary = set()
    edges = set()
    for outputs, _column in triples:
        projected = tuple(sorted(row for row in outputs if row in non_set))
        require(len(projected) <= 2, "projected triple weight changed")
        if len(projected) == 1:
            unary.add(projected[0])
        elif len(projected) == 2:
            edges.add(projected)

    adjacency = defaultdict(set)
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    for row in non_rows:
        adjacency[row]
    unseen = set(non_rows)
    duals = []
    rooted = 0
    nonbipartite = 0
    while unseen:
        start = min(unseen)
        component = {start}
        colour = {start: 1}
        queue = deque((start,))
        bipartite = True
        while queue:
            vertex = queue.popleft()
            for other in adjacency[vertex]:
                if other not in component:
                    component.add(other)
                    colour[other] = -colour[vertex]
                    queue.append(other)
                elif colour[other] == colour[vertex]:
                    bipartite = False
        unseen -= component
        if component & unary:
            rooted += 1
        elif not bipartite:
            nonbipartite += 1
        else:
            duals.append(tuple(sorted((row, colour[row]) for row in component)))
    require(len(duals) == 226,
            f"legacy27 coupled quotient left-nullity changed: {len(duals)}")
    return non_rows, tuple(duals), {
        "literal_singleton_rows": len(singleton),
        "coupled_rows": len(non_rows),
        "unary_rows": len(unary),
        "distinct_edges": len(edges),
        "rooted_components": rooted,
        "nonbipartite_unrooted_components": nonbipartite,
        "bipartite_unrooted_duals": len(duals),
    }


def encode_fraction(value):
    value = Fraction(value)
    return str(value)


def audit():
    data = PROBE.degree5_orbit_closure()
    non_rows, duals, quotient_census = quotient_data(data)
    dual_lookup = {}
    for dual_number, dual in enumerate(duals):
        for row, sign in dual:
            require(row not in dual_lookup,
                    "quotient components unexpectedly overlap")
            dual_lookup[row] = (dual_number, sign)

    lower_rows = tuple(sorted({PROBE.canonical_row(row)
                               for row in data["lower_rows_actual"]}))
    lower_index = {row: number for number, row in enumerate(lower_rows)}
    lower_columns = data["lower_columns"]
    lower_target = AUDIT.target_actual(5)
    target5 = Counter({row: value for row, value in AUDIT.target_actual(6).items()
                       if BASE.row_degree(row, PROBE.ANCHORS) == 5})
    target_entries = Counter()
    for row in lower_rows:
        value = lower_target[row] * AUDIT.row_orbit_size(row)
        if value:
            target_entries[lower_index[row]] = value
    target5_scaled = Counter({
        row: target5[row] * AUDIT.row_orbit_size(row)
        for row in data["rows5"] if target5[row]
    })
    for dual_number, dual in enumerate(duals):
        value = sum(sign * target5_scaled[row] for row, sign in dual)
        if value:
            target_entries[len(lower_rows) + dual_number] = value

    columns = []
    non_set = set(non_rows)
    entry_histogram = Counter()
    for number, column in enumerate(lower_columns):
        vector = Counter()
        for output in BASE.column_rows(column):
            degree = BASE.row_degree(output, PROBE.ANCHORS)
            representative = PROBE.canonical_row(output)
            if degree < 5:
                vector[lower_index[representative]] += 1
            elif degree == 5 and representative in non_set:
                item = dual_lookup.get(representative)
                if item is not None:
                    dual_number, sign = item
                    vector[len(lower_rows) + dual_number] += sign
        vector = Counter({index: value for index, value in vector.items() if value})
        entry_histogram[len(vector)] += 1
        word, multiplier = column
        columns.append({
            "word": "".join(map(str, word)),
            "multiplier_hex": multiplier.hex(),
            "column_orbit_size": len(PROBE.column_orbit(column)),
            "entries": [[index, encode_fraction(value)]
                        for index, value in sorted(vector.items())],
        })
        if (number + 1) % 2000 == 0:
            print(f"encoded {number + 1}/{len(lower_columns)} columns", flush=True)

    matrix = {
        "status": "UNAUDITED exact sparse matrix export; no rank claim",
        "zero_based_chart": 30,
        "legacy_one_based_chart": 27,
        "stabilizer_order": len(PROBE.STABILIZER),
        "scaling_convention": (
            "representative-column literal multiplicities; target actual "
            "coefficient times labelled row-orbit size"
        ),
        "lower_row_orbits": len(lower_rows),
        "quotient_dual_rows": len(duals),
        "total_rows": len(lower_rows) + len(duals),
        "lower_column_orbits": len(lower_columns),
        "quotient_census": quotient_census,
        "column_nonzero_histogram": {
            str(key): value for key, value in sorted(entry_histogram.items())
        },
        "lower_row_representatives_hex": [row.hex() for row in lower_rows],
        "quotient_duals": [
            [[row.hex(), sign] for row, sign in dual] for dual in duals
        ],
        "target": [[index, encode_fraction(value)]
                   for index, value in sorted(target_entries.items())],
        "columns": columns,
    }
    encoded = json.dumps(matrix, sort_keys=True, separators=(",", ":"))
    matrix["matrix_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return matrix


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "rows": result["total_rows"],
        "columns": result["lower_column_orbits"],
        "matrix_sha256": result["matrix_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()

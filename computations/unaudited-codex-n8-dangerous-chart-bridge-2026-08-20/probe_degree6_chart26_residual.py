#!/usr/bin/env python3
"""Residual-led K-degree-six orbit closure for chart 26 / legacy 29.

This probe starts from the exact degree-six tail of the frozen K^6
certificate, not from the three-million-row complete lower frontier.  It
closes only under minimum-K-degree-six source columns, peels literal
singleton pivots, and reports the coupled quotient ranks over two primes.
Finite-field membership is discovery only; no characteristic-zero conclusion
is made unless a later exact replay or dual is supplied.
"""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROBE_PATH = HERE / "probe_degree5_chart26_orbit.py"
SPEC = importlib.util.spec_from_file_location("degree5_probe", PROBE_PATH)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)
BASE = PROBE.BASE
IN_CERT = HERE / "results_degree5_chart26.json"
OUT = HERE / "results_degree6_chart26_residual.json"
MATRIX_OUT = HERE / "degree6_coupled_matrix.jsonl"
PRIMES = (1009, 1013)
PYTHON_ELIMINATION_ROW_LIMIT = 8000


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def row_orbit_size(row):
    return len({bytes(sorted(transform[cell] for cell in row))
                for transform in PROBE.TRANSFORMS})


def frozen_residual():
    data = json.loads(IN_CERT.read_text())
    require(data["result_sha256"]
            == "2c7e35f08ed2932cd99e4df4deb603625f55439281a69ac15759f7ad9b412f5c",
            "pinned K^6 certificate changed")
    current = Counter()
    for item in data["certificate"]["terms"]:
        coefficient = Fraction(item["coefficient_on_orbit_average"])
        column = (
            tuple(map(int, item["word"])),
            bytes(sorted(BASE.NAME_ID[name] for name in item["multiplier"])),
        )
        for row in BASE.column_rows(column):
            if BASE.row_degree(row, PROBE.ANCHORS) == 6:
                current[PROBE.canonical_row(row)] += coefficient
    target = Counter()
    for row, coefficient in BASE.filtered_target(PROBE.MATCHINGS, 6).items():
        representative = PROBE.canonical_row(row)
        if row == representative:
            target[representative] = Fraction(
                coefficient * row_orbit_size(representative)
            )
    residual = {
        row: target[row] - current[row]
        for row in set(target) | set(current)
        if target[row] - current[row]
    }
    require(len(residual) == 12705,
            "frozen K^6 tail residual support changed")
    return residual


def close_residual(residual):
    rows = set(residual)
    frontier = set(rows)
    columns = set()
    layers = []
    while frontier:
        new_rows = set()
        before = len(columns)
        for row in frontier:
            for raw_column in BASE.incident_columns(row):
                column = PROBE.canonical_column(raw_column)
                if column in columns:
                    continue
                if BASE.column_minimum_degree(column, PROBE.ANCHORS) != 6:
                    continue
                columns.add(column)
                for output in BASE.column_rows(column):
                    if BASE.row_degree(output, PROBE.ANCHORS) != 6:
                        continue
                    representative = PROBE.canonical_row(output)
                    if representative not in rows:
                        rows.add(representative)
                        new_rows.add(representative)
        frontier = new_rows
        layers.append((len(new_rows), len(columns) - before))
        print(
            f"layer {len(layers)}: +{len(new_rows)} rows, "
            f"+{len(columns) - before} cols, totals {len(rows)}/{len(columns)}",
            flush=True,
        )
    require((len(rows), len(columns), len(layers)) == (140578, 361406, 22),
            "degree-six residual-led closure changed")
    return rows, columns, layers


def quotient_vectors(rows, columns):
    """Saturate literal singleton peeling and return the sparse 2-core.

    Once a row has a singleton source column it is a free coordinate in the
    source image.  Quotienting by it can turn another column into a singleton,
    so a single pass is not the actual coupled quotient.  The queue below
    performs that peeling to exhaustion.  All coefficients are positive
    integers at this leading degree, hence every pivot is valid over Q.
    """
    ordered_columns = tuple(sorted(columns, key=repr))
    supports = []
    row_to_columns = {row: [] for row in rows}
    leading_histogram = Counter()
    for number, column in enumerate(ordered_columns):
        output_counts = Counter(
            PROBE.canonical_row(row)
            for row in BASE.column_rows(column)
            if BASE.row_degree(row, PROBE.ANCHORS) == 6
        )
        require(sum(output_counts.values()) in (1, 3, 15),
                "degree-six leading term count left 1/3/15")
        leading_histogram[sum(output_counts.values())] += 1
        supports.append(output_counts)
        for row in output_counts:
            row_to_columns[row].append(number)

    queue = deque(number for number, support in enumerate(supports)
                  if len(support) == 1)
    pivot_columns = {}
    initial_singleton_rows = len({next(iter(support)) for support in supports
                                  if len(support) == 1})
    while queue:
        number = queue.popleft()
        support = supports[number]
        if len(support) != 1:
            continue
        row = next(iter(support))
        if row in pivot_columns:
            continue
        pivot_columns[row] = ordered_columns[number]
        for incident in row_to_columns[row]:
            incident_support = supports[incident]
            if row not in incident_support:
                continue
            del incident_support[row]
            if len(incident_support) == 1:
                queue.append(incident)

    non_singleton = tuple(sorted(set(rows) - set(pivot_columns)))
    index = {row: i for i, row in enumerate(non_singleton)}
    vectors = []
    vector_columns = []
    projected_histogram = Counter()
    for support, column in zip(supports, ordered_columns):
        projected_histogram[sum(support.values())] += 1
        if len(support) >= 2:
            vectors.append(Counter({index[row]: value
                                    for row, value in support.items()}))
            vector_columns.append(column)
    return (
        pivot_columns, initial_singleton_rows, non_singleton, vectors,
        vector_columns, leading_histogram, projected_histogram,
    )


def modular_rank_and_remainder(vectors, target, row_count, prime):
    basis = {}
    pivot_sequence = []
    for raw in vectors:
        vector = {i: value % prime for i, value in raw.items()
                  if value % prime}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, prime)
                basis[pivot] = {i: entry * inverse % prime
                                for i, entry in vector.items()}
                pivot_sequence.append(pivot)
                break
            base = basis[pivot]
            for i, entry in base.items():
                new = (vector.get(i, 0) - value * entry) % prime
                if new:
                    vector[i] = new
                else:
                    vector.pop(i, None)
    residual = {i: value % prime for i, value in target.items()
                if value % prime}
    while residual:
        pivot = min(residual)
        if pivot not in basis:
            break
        value = residual[pivot]
        for i, entry in basis[pivot].items():
            new = (residual.get(i, 0) - value * entry) % prime
            if new:
                residual[i] = new
            else:
                residual.pop(i, None)
    return {
        "rank": len(basis),
        "quotient_dimension": row_count - len(basis),
        "target_remainder_nonzeros": len(residual),
        "target_in_image": not residual,
        "pivot_sequence_sha256": sha256(
            json.dumps(pivot_sequence, separators=(",", ":")).encode("ascii")
        ).hexdigest(),
        "remainder_support_sha256": sha256(
            json.dumps(sorted(residual), separators=(",", ":")).encode("ascii")
        ).hexdigest(),
    }


def serialize_interface(rows, vectors, columns, target):
    """Write deterministic sparse input for the Rust accelerator lane."""
    hasher = sha256()
    with MATRIX_OUT.open("w") as handle:
        header = {
            "type": "header",
            "format": "krenn-dangerous-chart26-degree6-coupled-v1",
            "row_count": len(rows),
            "column_count": len(vectors),
            "rows_hex": [row.hex() for row in rows],
            "target": [
                [index, value.numerator, value.denominator]
                for index, value in sorted(target.items()) if value
            ],
        }
        line = json.dumps(header, sort_keys=True, separators=(",", ":")) + "\n"
        handle.write(line)
        hasher.update(line.encode("ascii"))
        for number, (vector, column) in enumerate(zip(vectors, columns)):
            record = {
                "type": "column",
                "index": number,
                "entries": [[index, value]
                            for index, value in sorted(vector.items())],
                "word": BASE.word_name(column[0]),
                "multiplier_cell_ids": list(column[1]),
            }
            line = json.dumps(record, sort_keys=True,
                              separators=(",", ":")) + "\n"
            handle.write(line)
            hasher.update(line.encode("ascii"))
    return hasher.hexdigest(), MATRIX_OUT.stat().st_size


def audit():
    residual = frozen_residual()
    rows, columns, layers = close_residual(residual)
    (pivot_columns, initial_singleton_rows, non_singleton, vectors,
     vector_columns, leading, projected) = quotient_vectors(rows, columns)
    index = {row: i for i, row in enumerate(non_singleton)}
    target = Counter({index[row]: value for row, value in residual.items()
                      if row in index})
    interface_sha, interface_bytes = serialize_interface(
        non_singleton, vectors, vector_columns, target
    )
    print(
        "serialized coupled interface:", len(non_singleton), len(vectors),
        interface_bytes, interface_sha, flush=True,
    )
    modular = {}
    if len(non_singleton) <= PYTHON_ELIMINATION_ROW_LIMIT:
        for prime in PRIMES:
            modular[str(prime)] = modular_rank_and_remainder(
                vectors, target, len(non_singleton), prime
            )
            print("prime", prime, modular[str(prime)], flush=True)
        require(modular["1009"]["rank"] == modular["1013"]["rank"],
                "degree-six quotient rank differs across discovery primes")
    core = {
        "status": "UNAUDITED exact census / modular discovery only",
        "chart": 26,
        "legacy_one_based_chart": 29,
        "frozen_tail_residual_row_orbits": len(residual),
        "closure_row_column_orbits": [len(rows), len(columns)],
        "closure_layers": layers,
        "leading_term_histogram": {
            str(k): value for k, value in sorted(leading.items())
        },
        "initial_singleton_pivot_rows": initial_singleton_rows,
        "singleton_pivot_rows_after_saturation": len(pivot_columns),
        "coupled_row_orbits": len(non_singleton),
        "projected_coupled_column_count": len(vectors),
        "projected_leading_term_histogram": {
            str(k): value for k, value in sorted(projected.items())
        },
        "rust_interface": {
            "path": str(MATRIX_OUT.relative_to(HERE.parent.parent)),
            "format": "krenn-dangerous-chart26-degree6-coupled-v1",
            "bytes": interface_bytes,
            "sha256": interface_sha,
        },
        "modular_discovery": modular,
        "python_elimination_skipped_for_rust": (
            len(non_singleton) > PYTHON_ELIMINATION_ROW_LIMIT
        ),
        "characteristic_zero_membership_or_dual_proved": False,
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
    print("chart26 degree6 residual probe: PASS")
    print("coupled rows:", result["coupled_row_orbits"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Sound lower-kernel transfer probe for chart 26 / legacy chart 29.

The frozen K^6 certificate may be changed by any source combination which
vanishes through K-degree five.  This script constructs that entire
3,274-dimensional kernel (inside the frozen degree-five source component),
including the uniquely chosen minimum-degree-five triple/singleton
corrections, and records its degree-six tails.  Arithmetic is over one
discovery prime at a time; a positive modular result still needs exact-Q
reconstruction and replay.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
D6_PATH = HERE / "probe_degree6_chart26_residual.py"
SPEC = importlib.util.spec_from_file_location("degree6_residual", D6_PATH)
D6 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D6)
PROBE = D6.PROBE
BASE = D6.BASE
OUT_TEMPLATE = "results_degree6_chart26_lower_kernel_p{prime}.json"
STAGE_TEMPLATE = "degree6_lower_kernel_transfers_p{prime}.jsonl"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def clean(vector, prime):
    return Counter({key: value % prime for key, value in vector.items()
                    if value % prime})


def add_scaled(vector, other, scale, prime):
    scale %= prime
    if not scale:
        return
    for key, value in other.items():
        new = (vector.get(key, 0) + scale * value) % prime
        if new:
            vector[key] = new
        else:
            vector.pop(key, None)


def build_basis(vectors, prime):
    """Pivot -> (normalized vector, combination in input vectors)."""
    basis = {}
    for number, raw in enumerate(vectors):
        vector = clean(raw, prime)
        combination = Counter({number: 1})
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, prime)
                vector = clean(Counter({i: x * inverse
                                        for i, x in vector.items()}), prime)
                combination = clean(Counter({i: x * inverse
                                             for i, x in combination.items()}),
                                    prime)
                basis[pivot] = (vector, combination)
                break
            base_vector, base_combination = basis[pivot]
            add_scaled(vector, base_vector, -value, prime)
            add_scaled(combination, base_combination, -value, prime)
    return basis


def reduce_with_usage(raw, basis, prime):
    """Return remainder and c with raw - A*c = remainder."""
    vector = clean(raw, prime)
    usage = Counter()
    for pivot in sorted(basis):
        if pivot not in vector:
            continue
        value = vector[pivot]
        base_vector, base_combination = basis[pivot]
        add_scaled(vector, base_vector, -value, prime)
        add_scaled(usage, base_combination, value, prime)
    return vector, usage


def degree_tail(column, degree):
    return Counter(
        PROBE.canonical_row(row)
        for row in BASE.column_rows(column)
        if BASE.row_degree(row, PROBE.ANCHORS) == degree
    )


def build_frozen_degree5_component(prime):
    lower, records = PROBE.lower_through_degree4()
    lower_columns = tuple(sorted({PROBE.canonical_column(column)
                                  for column in lower}, key=repr))
    require(len(lower_columns) == 4513,
            "frozen lower-column orbit count changed")

    target5 = BASE.filtered_target(PROBE.MATCHINGS, 5)
    rows5 = {PROBE.canonical_row(row) for row in target5}
    for column in lower_columns:
        rows5.update(degree_tail(column, 5))
    frontier = set(rows5)
    columns5 = set()
    layers = []
    while frontier:
        new_rows = set()
        before = len(columns5)
        for row in frontier:
            for raw_column in BASE.incident_columns(row):
                column = PROBE.canonical_column(raw_column)
                if column in columns5:
                    continue
                if BASE.column_minimum_degree(column, PROBE.ANCHORS) != 5:
                    continue
                columns5.add(column)
                for output in degree_tail(column, 5):
                    if output not in rows5:
                        rows5.add(output)
                        new_rows.add(output)
        frontier = new_rows
        layers.append((len(new_rows), len(columns5) - before))
        print("d5 layer", len(layers), "totals", len(rows5), len(columns5),
              flush=True)
    require((len(rows5), len(columns5)) == (16515, 53228),
            "frozen degree-five component changed")
    columns5 = tuple(sorted(columns5, key=repr))
    column5_index = {column: i for i, column in enumerate(columns5)}

    singleton = {}
    triples = []
    for column in columns5:
        outputs = tuple(PROBE.canonical_row(row)
                        for row in BASE.column_rows(column)
                        if BASE.row_degree(row, PROBE.ANCHORS) == 5)
        require(len(outputs) in (1, 3), "d5 leading split changed")
        if len(outputs) == 1:
            singleton.setdefault(outputs[0], column)
        else:
            triples.append((outputs, column))
    non_singleton = tuple(sorted(set(rows5) - set(singleton)))
    non_index = {row: i for i, row in enumerate(non_singleton)}
    triple_vectors = [Counter(non_index[row] for row in outputs
                              if row in non_index)
                      for outputs, _column in triples]
    triple_columns = tuple(column for _outputs, column in triples)
    triple_basis = build_basis(triple_vectors, prime)
    quotient_indices = tuple(i for i in range(len(non_singleton))
                             if i not in triple_basis)
    require((len(non_singleton), len(triple_basis), len(quotient_indices))
            == (257, 215, 42), "d5 triple quotient changed")
    quotient_position = {index: pos
                         for pos, index in enumerate(quotient_indices)}

    lower_rows = {bytes(sorted(PROBE.ANCHORS))}
    for degree in (2, 3, 4):
        lower_rows.update(PROBE.canonical_row(row)
                          for row in records[degree][0])
    lower_rows = tuple(sorted(lower_rows))
    lower_index = {row: i for i, row in enumerate(lower_rows)}
    require(len(lower_rows) == 1201, "lower row-orbit count changed")
    return {
        "lower_columns": lower_columns,
        "lower_rows": lower_rows,
        "lower_index": lower_index,
        "columns5": columns5,
        "column5_index": column5_index,
        "singleton": singleton,
        "non_singleton": non_singleton,
        "non_index": non_index,
        "triple_columns": triple_columns,
        "triple_basis": triple_basis,
        "quotient_position": quotient_position,
        "degree5_layers": layers,
    }


def corrected_lower_columns(component, prime):
    """Replace each lower column by a d5-pivot-corrected generator g_j."""
    lower_columns = component["lower_columns"]
    lower_index = component["lower_index"]
    non_index = component["non_index"]
    quotient_position = component["quotient_position"]
    triple_columns = component["triple_columns"]
    triple_basis = component["triple_basis"]
    singleton = component["singleton"]
    column5_index = component["column5_index"]
    lower_row_count = len(component["lower_rows"])

    tail6_cache = {}
    singleton5_cache = {}

    def tail6(column):
        if column not in tail6_cache:
            tail6_cache[column] = degree_tail(column, 6)
        return tail6_cache[column]

    def singleton5(column):
        if column not in singleton5_cache:
            singleton5_cache[column] = Counter({
                row: value for row, value in degree_tail(column, 5).items()
                if row in singleton
            })
        return singleton5_cache[column]

    augmented_vectors = []
    corrected_tails = []
    corrections = []
    definition_hasher = sha256()
    for number, column in enumerate(lower_columns):
        augmented = Counter()
        for output in BASE.column_rows(column):
            degree = BASE.row_degree(output, PROBE.ANCHORS)
            if degree in (0, 2, 3, 4):
                representative = PROBE.canonical_row(output)
                augmented[lower_index[representative]] += 1

        tail5 = Counter({
            non_index[row]: value
            for row, value in degree_tail(column, 5).items()
            if row in non_index
        })
        remainder, triple_usage = reduce_with_usage(
            tail5, triple_basis, prime
        )
        for index, value in remainder.items():
            require(index in quotient_position,
                    "triple correction left a d5 pivot coordinate")
            augmented[lower_row_count + quotient_position[index]] += value
        augmented = clean(augmented, prime)

        corrected_tail = clean(tail6(column), prime)
        correction = Counter()
        singleton_residual = clean(singleton5(column), prime)
        for triple_number, value in triple_usage.items():
            triple_column = triple_columns[triple_number]
            add_scaled(corrected_tail, tail6(triple_column), -value, prime)
            add_scaled(singleton_residual, singleton5(triple_column),
                       -value, prime)
            correction[column5_index[triple_column]] -= value
        correction = clean(correction, prime)
        for row, value in list(singleton_residual.items()):
            singleton_column = singleton[row]
            add_scaled(corrected_tail, tail6(singleton_column), -value,
                       prime)
            correction[column5_index[singleton_column]] -= value
        correction = clean(correction, prime)

        augmented_vectors.append(augmented)
        corrected_tails.append(corrected_tail)
        corrections.append(correction)
        definition = {
            "index": number,
            "source_word": BASE.word_name(column[0]),
            "source_multiplier": list(column[1]),
            "min5_corrections": sorted(correction.items()),
            "augmented": sorted(augmented.items()),
            "tail6": [[row.hex(), value]
                      for row, value in sorted(corrected_tail.items())],
        }
        definition_hasher.update(json.dumps(
            definition, sort_keys=True, separators=(",", ":")
        ).encode("ascii"))
        if (number + 1) % 500 == 0:
            print("corrected lower", number + 1, "tail cache",
                  len(tail6_cache), flush=True)
    return (augmented_vectors, corrected_tails, corrections,
            definition_hasher.hexdigest())


def lower_kernel_transfers(augmented, tails, prime):
    """Common echelon: carry d6 tails and lower-column provenance."""
    basis = {}
    transfers = []
    relations = []
    for number, raw in enumerate(augmented):
        vector = clean(raw, prime)
        relation = Counter({number: 1})
        tail = clean(tails[number], prime)
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, prime)
                vector = clean(Counter({i: x * inverse
                                        for i, x in vector.items()}), prime)
                relation = clean(Counter({i: x * inverse
                                          for i, x in relation.items()}),
                                 prime)
                tail = clean(Counter({i: x * inverse
                                      for i, x in tail.items()}), prime)
                basis[pivot] = (vector, relation, tail)
                break
            base_vector, base_relation, base_tail = basis[pivot]
            add_scaled(vector, base_vector, -value, prime)
            add_scaled(relation, base_relation, -value, prime)
            add_scaled(tail, base_tail, -value, prime)
        else:
            transfers.append(tail)
            relations.append(relation)
        if (number + 1) % 500 == 0:
            print("lower echelon", number + 1, "rank", len(basis),
                  "kernel", len(transfers), flush=True)
    require((len(basis), len(transfers)) == (1239, 3274),
            "lower augmented rank/nullity changed")
    return basis, transfers, relations


def write_stage(component, corrections, transfers, relations, definition_sha,
                prime):
    path = HERE / STAGE_TEMPLATE.format(prime=prime)
    hasher = sha256()
    with path.open("w") as handle:
        header = {
            "type": "header",
            "format": "krenn-chart26-degree6-lower-kernel-v1",
            "prime": prime,
            "lower_column_count": len(component["lower_columns"]),
            "min5_column_count": len(component["columns5"]),
            "kernel_dimension": len(transfers),
            "corrected_lower_definition_sha256": definition_sha,
        }
        line = json.dumps(header, sort_keys=True,
                          separators=(",", ":")) + "\n"
        handle.write(line)
        hasher.update(line.encode("ascii"))
        for number, (tail, relation) in enumerate(zip(transfers, relations)):
            record = {
                "type": "transfer",
                "index": number,
                "tail6": [[row.hex(), value]
                          for row, value in sorted(tail.items())],
                "corrected_lower_relation": sorted(relation.items()),
            }
            line = json.dumps(record, sort_keys=True,
                              separators=(",", ":")) + "\n"
            handle.write(line)
            hasher.update(line.encode("ascii"))
    return path, path.stat().st_size, hasher.hexdigest()


def audit(prime, write_results):
    component = build_frozen_degree5_component(prime)
    augmented, tails, corrections, definition_sha = corrected_lower_columns(
        component, prime
    )
    basis, transfers, relations = lower_kernel_transfers(
        augmented, tails, prime
    )
    path, stage_bytes, stage_sha = write_stage(
        component, corrections, transfers, relations, definition_sha, prime
    )
    support = set().union(*(set(vector) for vector in transfers))
    zero_transfers = sum(not vector for vector in transfers)
    transfer_nnz = sum(len(vector) for vector in transfers)
    relation_nnz = sum(len(vector) for vector in relations)
    core = {
        "status": "UNAUDITED modular lower-kernel transfer census only",
        "chart": 26,
        "legacy_one_based_chart": 29,
        "prime": prime,
        "lower_augmented_rows_columns_rank_nullity": [
            1243, len(augmented), len(basis), len(transfers)
        ],
        "zero_degree6_transfers": zero_transfers,
        "degree6_transfer_union_row_orbits": len(support),
        "degree6_transfer_total_nnz": transfer_nnz,
        "lower_kernel_relation_total_nnz": relation_nnz,
        "corrected_lower_definition_sha256": definition_sha,
        "stage_interface": {
            "path": str(path.relative_to(HERE.parent.parent)),
            "bytes": stage_bytes,
            "sha256": stage_sha,
        },
        "full_degree6_closure_computed": False,
        "characteristic_zero_membership_or_dual_proved": False,
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if write_results:
        out = HERE / OUT_TEMPLATE.format(prime=prime)
        out.write_text(json.dumps(core, indent=2, sort_keys=True) + "\n")
    print("lower-kernel transfer stage: PASS", flush=True)
    print(json.dumps(core, indent=2, sort_keys=True), flush=True)
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1009)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    audit(args.prime, args.write_results)


if __name__ == "__main__":
    main()

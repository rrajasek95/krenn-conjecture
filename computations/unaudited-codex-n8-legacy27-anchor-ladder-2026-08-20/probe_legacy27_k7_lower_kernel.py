#!/usr/bin/env python3
"""RESTRICTED chosen-section lower-kernel transfers for legacy chart 27.

Each lower generator is first given a
deterministic minimum-degree-five triple/singleton correction.  Common
echelon then transports every lower-kernel relation, with literal orbit
multiplicities, to its degree-six tail.  This omits the large internal kernel
among the 140,847 minimum-degree-five columns and is therefore NOT a sound
full K^7 transfer family.  It is retained only as a documented failed scope.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROBE_PATH = HERE / "probe_legacy27_k6_orbits.py"
SPEC = importlib.util.spec_from_file_location("legacy27_k7_kernel_probe", PROBE_PATH)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)
BASE = PROBE.BASE
MATRIX = HERE / "k6_augmented_matrix.json"
EXPECTED_MATRIX_SHA256 = (
    "78a62528fc5dce57f5c20f4000b3b35bfe0b2f6679ebd1285f7de97fb9d0fb92"
)
OUT_TEMPLATE = "results_k7_lower_kernel_p{prime}.json"
STAGE_TEMPLATE = "k7_lower_kernel_transfers_p{prime}.jsonl"


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
        updated = (vector.get(key, 0) + scale * value) % prime
        if updated:
            vector[key] = updated
        else:
            vector.pop(key, None)


def build_basis(vectors, prime):
    """Complete common echelon with combinations in the input vectors."""
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


def build_degree5_component(prime):
    data = PROBE.degree5_orbit_closure()
    lower_columns = data["lower_columns"]
    columns5 = data["columns5"]
    require((len(lower_columns), len(columns5), len(data["rows5"]))
            == (13818, 140847, 44763), "frozen K6 component changed")
    column5_index = {column: index for index, column in enumerate(columns5)}
    singleton = {}
    triple_records = []
    for column in columns5:
        outputs = tuple(PROBE.canonical_row(row)
                        for row in BASE.column_rows(column)
                        if BASE.row_degree(row, PROBE.ANCHORS) == 5)
        require(len(outputs) in (1, 3), "degree-five leading split changed")
        require(len(outputs) == len(set(outputs)),
                "degree-five row-orbit multiplicity changed")
        if len(outputs) == 1:
            singleton.setdefault(outputs[0], column)
        else:
            triple_records.append((outputs, column))
    non_rows = tuple(sorted(set(data["rows5"]) - set(singleton)))
    non_index = {row: index for index, row in enumerate(non_rows)}
    triple_columns = []
    triple_vectors = []
    for outputs, column in triple_records:
        vector = Counter(non_index[row] for row in outputs if row in non_index)
        if vector:
            triple_columns.append(column)
            triple_vectors.append(vector)
    triple_columns = tuple(triple_columns)
    triple_basis = build_basis(triple_vectors, prime)
    require((len(non_rows), len(triple_vectors), len(triple_basis))
            == (977, 1028, 751),
            "degree-five coupled quotient rank changed")
    return {
        "lower_columns": lower_columns,
        "columns5": columns5,
        "column5_index": column5_index,
        "singleton": singleton,
        "non_rows": non_rows,
        "non_index": non_index,
        "triple_columns": triple_columns,
        "triple_basis": triple_basis,
        "degree5_layers": data["layers"],
    }


def load_augmented_vectors(component, prime):
    payload = json.loads(MATRIX.read_text())
    require(payload["matrix_sha256"] == EXPECTED_MATRIX_SHA256,
            "complete K6 augmented matrix changed")
    require((payload["total_rows"], payload["lower_column_orbits"])
            == (3905, 13818), "K6 augmented dimensions changed")
    vectors = []
    for number, (record, column) in enumerate(zip(
            payload["columns"], component["lower_columns"])):
        word, multiplier = column
        require(record["word"] == "".join(map(str, word))
                and record["multiplier_hex"] == multiplier.hex(),
                f"augmented lower-column order changed at {number}")
        vector = Counter()
        for row, value in record["entries"]:
            integer = int(value)
            vector[row] += integer
        vectors.append(clean(vector, prime))
    return tuple(vectors)


def corrected_lower_columns(component, prime):
    lower_columns = component["lower_columns"]
    non_index = component["non_index"]
    triple_columns = component["triple_columns"]
    triple_basis = component["triple_basis"]
    singleton = component["singleton"]
    column5_index = component["column5_index"]
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

    corrected_tails = []
    remainders5 = []
    definition_hasher = sha256()
    multiplicity_columns = 0
    correction_terms = 0
    for number, column in enumerate(lower_columns):
        full5 = degree_tail(column, 5)
        tail5 = Counter({non_index[row]: value for row, value in full5.items()
                         if row in non_index})
        remainder, triple_usage = reduce_with_usage(
            tail5, triple_basis, prime
        )
        corrected_tail = clean(tail6(column), prime)
        if any(value > 1 for value in degree_tail(column, 6).values()):
            multiplicity_columns += 1
        correction = Counter()
        singleton_residual = clean(Counter({
            row: value for row, value in full5.items() if row in singleton
        }), prime)
        for triple_number, value in triple_usage.items():
            triple_column = triple_columns[triple_number]
            add_scaled(corrected_tail, tail6(triple_column), -value, prime)
            add_scaled(singleton_residual, singleton5(triple_column),
                       -value, prime)
            correction[column5_index[triple_column]] -= value
        correction = clean(correction, prime)
        for row, value in list(singleton_residual.items()):
            singleton_column = singleton[row]
            add_scaled(corrected_tail, tail6(singleton_column), -value, prime)
            correction[column5_index[singleton_column]] -= value
        correction = clean(correction, prime)
        correction_terms += len(correction)
        corrected_tails.append(corrected_tail)
        remainders5.append(remainder)
        definition = {
            "index": number,
            "source_word": "".join(map(str, column[0])),
            "source_multiplier": list(column[1]),
            "min5_corrections": sorted(correction.items()),
            "remainder5": sorted(remainder.items()),
            "tail6": [[row.hex(), value]
                      for row, value in sorted(corrected_tail.items())],
        }
        definition_hasher.update(json.dumps(
            definition, sort_keys=True, separators=(",", ":")
        ).encode("ascii"))
        if (number + 1) % 500 == 0:
            print("corrected lower", number + 1,
                  "tail-cache", len(tail6_cache), flush=True)
    require(correction_terms > 0, "minimum-degree-five correction vanished")
    return (tuple(corrected_tails), tuple(remainders5),
            definition_hasher.hexdigest(), multiplicity_columns,
            correction_terms)


def write_lower_kernel_stage(augmented, tails, remainders5, component,
                             definition_sha, prime):
    path = HERE / STAGE_TEMPLATE.format(prime=prime)
    basis = {}
    transfer_count = 0
    zero_transfers = 0
    transfer_nnz = 0
    relation_nnz = 0
    transfer_support = set()
    hasher = sha256()
    header = {
        "type": "header",
        "format": "krenn-legacy27-degree6-lower-kernel-v1",
        "prime": prime,
        "lower_column_count": len(augmented),
        "min5_column_count": len(component["columns5"]),
        "kernel_dimension": len(augmented) - 3864,
        "corrected_lower_definition_sha256": definition_sha,
        "source_augmented_matrix_sha256": EXPECTED_MATRIX_SHA256,
    }
    with path.open("w") as handle:
        line = json.dumps(header, sort_keys=True, separators=(",", ":")) + "\n"
        handle.write(line)
        hasher.update(line.encode("ascii"))
        for number, raw in enumerate(augmented):
            vector = clean(raw, prime)
            relation = Counter({number: 1})
            tail = clean(tails[number], prime)
            remainder5 = clean(remainders5[number], prime)
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
                    remainder5 = clean(Counter({i: x * inverse
                                                for i, x in remainder5.items()}),
                                       prime)
                    basis[pivot] = (vector, relation, tail, remainder5)
                    break
                base_vector, base_relation, base_tail, base_remainder5 = basis[pivot]
                add_scaled(vector, base_vector, -value, prime)
                add_scaled(relation, base_relation, -value, prime)
                add_scaled(tail, base_tail, -value, prime)
                add_scaled(remainder5, base_remainder5, -value, prime)
            else:
                require(not remainder5,
                        "lower-kernel relation retained a degree-five remainder")
                record = {
                    "type": "transfer",
                    "index": transfer_count,
                    "tail6": [[row.hex(), value]
                              for row, value in sorted(tail.items())],
                    "corrected_lower_relation": sorted(relation.items()),
                }
                line = json.dumps(record, sort_keys=True,
                                  separators=(",", ":")) + "\n"
                handle.write(line)
                hasher.update(line.encode("ascii"))
                transfer_count += 1
                zero_transfers += not tail
                transfer_nnz += len(tail)
                relation_nnz += len(relation)
                transfer_support.update(tail)
            if (number + 1) % 500 == 0:
                print("lower echelon", number + 1, "rank", len(basis),
                      "kernel", transfer_count, flush=True)
    require((len(basis), transfer_count) == (3864, 9954),
            "complete K6 augmented rank/nullity changed")
    return {
        "path": path,
        "bytes": path.stat().st_size,
        "sha256": hasher.hexdigest(),
        "rank": len(basis),
        "kernel": transfer_count,
        "zero_transfers": zero_transfers,
        "transfer_nnz": transfer_nnz,
        "relation_nnz": relation_nnz,
        "support_rows": len(transfer_support),
    }


def audit(prime, write_results):
    component = build_degree5_component(prime)
    augmented = load_augmented_vectors(component, prime)
    (tails, remainders5, definition_sha, multiplicity_columns,
     correction_terms) = corrected_lower_columns(component, prime)
    stage = write_lower_kernel_stage(
        augmented, tails, remainders5, component, definition_sha, prime
    )
    core = {
        "status": (
            "UNAUDITED RESTRICTED chosen-section transfer; INCOMPLETE because "
            "the internal minimum-degree-five kernel is omitted"
        ),
        "zero_based_chart": 30,
        "legacy_one_based_chart": 27,
        "prime": prime,
        "lower_augmented_rows_columns_rank_nullity": [
            3905, len(augmented), stage["rank"], stage["kernel"]
        ],
        "degree5_coupled_rows_triple_rank_quotient": [977, 751, 226],
        "minimum_degree5_correction_terms": correction_terms,
        "lower_columns_with_degree6_row_orbit_multiplicity": multiplicity_columns,
        "zero_degree6_transfers": stage["zero_transfers"],
        "degree6_transfer_union_row_orbits": stage["support_rows"],
        "degree6_transfer_total_nnz": stage["transfer_nnz"],
        "lower_kernel_relation_total_nnz": stage["relation_nnz"],
        "corrected_lower_definition_sha256": definition_sha,
        "stage_interface": {
            "path": str(stage["path"].relative_to(HERE.parent.parent)),
            "bytes": stage["bytes"],
            "sha256": stage["sha256"],
        },
        "degree5_remainder_must_vanish_on_every_kernel_relation": True,
        "internal_minimum_degree5_kernel_included": False,
        "full_sound_degree6_closure_computed": False,
        "characteristic_zero_membership_or_dual_proved": False,
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if write_results:
        (HERE / OUT_TEMPLATE.format(prime=prime)).write_text(
            json.dumps(core, indent=2, sort_keys=True) + "\n"
        )
    print("legacy27 K7 lower-kernel stage: PASS")
    print(json.dumps(core, indent=2, sort_keys=True))
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1009,
                        choices=(1009, 1013))
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    audit(args.prime, args.write_results)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Strict exact merger for disjoint K22 hidden-pair scalar-fold intervals."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


EXPECTED_IDS = ["D14:222|R:2-3-3", "D14:222|R:2-4-2"]
EXPECTED_RECORDS = 101_545_723
EXPECTED_U = 400_591_699_200
EXPECTED_INPUT_SHA256 = "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8"
EXPECTED_PAIR_USES = 511_214_060
EXPECTED_PAIR_WEIGHT = 146_230_609_431_055_564_800
EXPECTED_STABILIZERS = {"1": 99_314_228, "2": 2_212_958, "4": 16_210,
                        "8": 2_099, "16": 224, "32": 4}
SUM_FIELDS = [
    "first_tail_evaluations", "pivotable_intermediate_children",
    "selected_next_pivots", "terminal_K22_occurrences", "full_occurrences",
    "irreducible_occurrences", "pivotable_intermediate_weight_sum_scaled",
    "normalized_next_pivot_weight_sum_scaled", "terminal_K22_weight_sum_scaled",
    "full_charge_scaled", "irreducible_charge_scaled",
]
PROV_SUM_FIELDS = [
    "pivotable_intermediate_children", "signed_intermediate_weight_scaled",
    "selected_next_pivots", "terminal_K22_children", "charge_scaled",
]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(8 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def integer(value: object) -> int:
    require(isinstance(value, (int, str)), (value, type(value)))
    return int(value)


def reduced(value: int) -> str:
    q = Fraction(value, EXPECTED_U)
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def sum_maps(target: dict[str, int], source: dict[str, object]) -> None:
    for key, value in source.items():
        target[key] = target.get(key, 0) + integer(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("shards", nargs="+", type=Path)
    args = parser.parse_args()

    require(len(args.shards) >= 2, "the gated full plan requires at least two intervals")
    loaded = [(path, json.loads(path.read_text())) for path in args.shards]
    loaded.sort(key=lambda item: item[1]["input_interval"][0])
    first = loaded[0][1]

    invariant_keys = [
        "covered_lineage_ids", "scale_U", "input", "input_sha256_expected",
        "input_schema", "input_records_declared",
        "upstream_labelled_p2_uses_before_zero", "universal_terminality",
        "sign_rule", "linearity_scope", "scope",
    ]
    cursor = 0
    for path, data in loaded:
        require(data["status"] == "PASS_BOUNDED_INTERVAL_D14_222_K22_HIDDEN_PAIR_TWO_SINK_CHARGE", path)
        require(data["covered_lineage_ids"] == EXPECTED_IDS, path)
        require(data["input_interval"][0] == cursor, (path, data["input_interval"], cursor))
        require(data["input_interval"][1] > cursor, path)
        require(data["input_records_consumed"] == data["input_interval"][1] - cursor, path)
        require(data["elapsed_seconds"] < 600, (path, data["elapsed_seconds"]))
        require(data["literal_sample_guard"]["global_257_mode"] is True, path)
        for key in invariant_keys:
            require(data[key] == first[key], (path, key))
        cursor = data["input_interval"][1]
    require(cursor == EXPECTED_RECORDS, cursor)
    require(int(first["scale_U"]) == EXPECTED_U, first["scale_U"])
    require(first["input_sha256_expected"] == EXPECTED_INPUT_SHA256, first["input_sha256_expected"])

    input_path = Path(first["input"])
    require(input_path.is_file(), input_path)
    actual_input_sha = sha256(input_path)
    require(actual_input_sha == EXPECTED_INPUT_SHA256, actual_input_sha)

    sinks: dict[str, dict[str, object]] = {}
    for lineage_id in EXPECTED_IDS:
        base = first["sinks"][lineage_id]
        sink: dict[str, object] = {
            key: base[key] for key in
            ("first_tail_degree", "intermediate_degree", "terminal_tail_degree")
        }
        for key in SUM_FIELDS:
            sink[key] = sum(integer(data["sinks"][lineage_id][key]) for _, data in loaded)
        cache = {
            "hits": sum(data["sinks"][lineage_id]["response_cache"]["hits"] for _, data in loaded),
            "misses": sum(data["sinks"][lineage_id]["response_cache"]["misses"] for _, data in loaded),
            "clears": sum(data["sinks"][lineage_id]["response_cache"]["clears"] for _, data in loaded),
            "peak_keys_per_worker_chunk": max(data["sinks"][lineage_id]["response_cache"]["peak_keys_per_worker_chunk"] for _, data in loaded),
            "cache_chunk_pair_records": base["response_cache"]["cache_chunk_pair_records"],
            "hard_max_keys_per_worker_sink": base["response_cache"]["hard_max_keys_per_worker_sink"],
        }
        require(all(data["sinks"][lineage_id]["response_cache"]["cache_chunk_pair_records"] == cache["cache_chunk_pair_records"] for _, data in loaded), lineage_id)
        require(all(data["sinks"][lineage_id]["response_cache"]["hard_max_keys_per_worker_sink"] == cache["hard_max_keys_per_worker_sink"] for _, data in loaded), lineage_id)
        require(cache["peak_keys_per_worker_chunk"] <= cache["hard_max_keys_per_worker_sink"] + 720, lineage_id)
        sink["response_cache"] = cache
        provenance: dict[str, dict[str, int]] = {}
        for _, data in loaded:
            for divisor, values in data["sinks"][lineage_id]["m2_m3_provenance"].items():
                entry = provenance.setdefault(divisor, {key: 0 for key in PROV_SUM_FIELDS})
                for key in PROV_SUM_FIELDS:
                    entry[key] += integer(values[key])
        sink["m2_m3_provenance"] = dict(sorted(provenance.items()))
        sink["full_charge_reduced"] = reduced(integer(sink["full_charge_scaled"]))
        sinks[lineage_id] = sink

    s33, s42 = (sinks[lineage_id] for lineage_id in EXPECTED_IDS)
    require(integer(s33["first_tail_evaluations"]) == 32 * EXPECTED_RECORDS, "R233 first tails")
    require(integer(s33["terminal_K22_occurrences"]) == 32 * integer(s33["selected_next_pivots"]), "R233 terminal tails")
    require(integer(s42["first_tail_evaluations"]) == 60 * EXPECTED_RECORDS, "R242 first tails")
    require(integer(s42["terminal_K22_occurrences"]) == 12 * integer(s42["selected_next_pivots"]), "R242 terminal tails")
    for lineage_id, sink, terminal_count in ((EXPECTED_IDS[0], s33, 32), (EXPECTED_IDS[1], s42, 12)):
        require(sink["full_occurrences"] == sink["irreducible_occurrences"] == sink["terminal_K22_occurrences"], lineage_id)
        require(sink["full_charge_scaled"] == sink["irreducible_charge_scaled"], lineage_id)
        require(integer(sink["normalized_next_pivot_weight_sum_scaled"]) == -integer(sink["pivotable_intermediate_weight_sum_scaled"]), lineage_id)
        require(integer(sink["terminal_K22_weight_sum_scaled"]) == terminal_count * integer(sink["normalized_next_pivot_weight_sum_scaled"]), lineage_id)
        cache = sink["response_cache"]
        require(cache["hits"] + cache["misses"] == sink["selected_next_pivots"], lineage_id)
        folded = {key: sum(integer(values[key]) for values in sink["m2_m3_provenance"].values()) for key in PROV_SUM_FIELDS}
        require(folded["pivotable_intermediate_children"] == sink["pivotable_intermediate_children"], lineage_id)
        require(folded["signed_intermediate_weight_scaled"] == integer(sink["pivotable_intermediate_weight_sum_scaled"]), lineage_id)
        require(folded["selected_next_pivots"] == sink["selected_next_pivots"], lineage_id)
        require(folded["terminal_K22_children"] == sink["terminal_K22_occurrences"], lineage_id)
        require(folded["charge_scaled"] == integer(sink["full_charge_scaled"]), lineage_id)

    stabilizers: dict[str, int] = {}
    for _, data in loaded:
        sum_maps(stabilizers, data["stabilizer_histogram"])
    require(stabilizers == EXPECTED_STABILIZERS, stabilizers)
    pair_uses = sum(data["retained_nonzero_pair_witness_uses"] for _, data in loaded)
    pair_weight = sum(integer(data["pair_weight_sum_scaled"]) for _, data in loaded)
    require(pair_uses == EXPECTED_PAIR_USES, pair_uses)
    require(pair_weight == EXPECTED_PAIR_WEIGHT, pair_weight)

    header: str | None = None
    sample_rows: dict[int, str] = {}
    nonzero33 = nonzero42 = 0
    for _, data in loaded:
        sample_path = Path(data["literal_sample_guard"]["ledger"])
        lines = sample_path.read_text().splitlines()
        require(bool(lines), sample_path)
        if header is None:
            header = lines[0]
        require(lines[0] == header, sample_path)
        require(len(lines) - 1 == data["literal_sample_guard"]["records"], sample_path)
        for line in lines[1:]:
            cells = line.split("\t")
            require(len(cells) == 22, (sample_path, len(cells)))
            index = int(cells[0])
            require(index not in sample_rows, index)
            sample_rows[index] = line
            nonzero33 += cells[-2] == "1"
            nonzero42 += cells[-1] == "1"
    expected_samples = {j * (EXPECTED_RECORDS - 1) // 256 for j in range(257)}
    require(set(sample_rows) == expected_samples, (len(sample_rows), sorted(expected_samples - set(sample_rows))[:3]))
    sample_path = Path(f"{args.output}.samples.tsv")
    sample_text = "\n".join([header or ""] + [sample_rows[index] for index in sorted(sample_rows)]) + "\n"

    result = {
        "status": "PASS_COMPLETE_D14_222_K22_HIDDEN_PAIR_TWO_SINK_CHARGE",
        "covered_lineage_ids": EXPECTED_IDS,
        "scale_U": str(EXPECTED_U),
        "input": first["input"],
        "input_sha256": actual_input_sha,
        "input_schema": first["input_schema"],
        "input_records_declared": EXPECTED_RECORDS,
        "input_interval": [0, EXPECTED_RECORDS],
        "input_records_consumed": EXPECTED_RECORDS,
        "upstream_labelled_p2_uses_before_zero": first["upstream_labelled_p2_uses_before_zero"],
        "retained_nonzero_pair_witness_uses": pair_uses,
        "pair_weight_sum_scaled": str(pair_weight),
        "sinks": sinks,
        "stabilizer_histogram": stabilizers,
        "literal_sample_guard": {
            "records": 257,
            "global_257_mode": True,
            "R233_nonzero_continuations": nonzero33,
            "R242_nonzero_continuations": nonzero42,
            "all_literal_K22_children_nonpivotable": True,
            "all_abstract_literal_cycle_keys_equal": True,
            "ledger": str(sample_path),
        },
        "universal_terminality": first["universal_terminality"],
        "sign_rule": first["sign_rule"],
        "linearity_scope": first["linearity_scope"],
        "execution": {
            "exact_disjoint_interval_shards": [
                {
                    "path": str(path), "sha256": sha256(path),
                    "interval": data["input_interval"],
                    "elapsed_seconds": data["elapsed_seconds"],
                    "workers": data["workers"],
                }
                for path, data in loaded
            ],
            "sum_elapsed_seconds": sum(data["elapsed_seconds"] for _, data in loaded),
            "maximum_shard_elapsed_seconds": max(data["elapsed_seconds"] for _, data in loaded),
            "hard_per_shard_gate_seconds": 600,
        },
        "scope": first["scope"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sample_tmp = Path(f"{sample_path}.tmp")
    output_tmp = Path(f"{args.output}.tmp")
    sample_tmp.write_text(sample_text)
    output_tmp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    sample_tmp.replace(sample_path)
    output_tmp.replace(args.output)
    print(json.dumps({
        "status": result["status"],
        "charges_scaled": {lineage_id: sinks[lineage_id]["full_charge_scaled"] for lineage_id in EXPECTED_IDS},
        "charges_reduced": {lineage_id: sinks[lineage_id]["full_charge_reduced"] for lineage_id in EXPECTED_IDS},
        "sample_records": len(sample_rows),
        "output": str(args.output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()

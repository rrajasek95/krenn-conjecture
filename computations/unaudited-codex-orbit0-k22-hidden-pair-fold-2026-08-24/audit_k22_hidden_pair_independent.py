#!/usr/bin/env python3
"""Independent source/count/hash/sample referee for the merged two-sink fold."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path("computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24")
RESULT = ROOT / "results_hidden_pair_k22_charge.json"
AUDIT = ROOT / "results_hidden_pair_independent_referee.json"
SOURCE = ROOT / "run_k22_hidden_pair_fold.rs"
MERGER = ROOT / "merge_k22_hidden_pair_shards.py"
INPUT = Path("computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin")
K4 = Path("computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin")
CYCLES = Path("computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin")
IDS = ["D14:222|R:2-3-3", "D14:222|R:2-4-2"]
U = 400_591_699_200
N = 101_545_723
HEADER = 80
RECORD = 53
PINS = {
    INPUT: "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8",
    K4: "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
    CYCLES: "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    SOURCE: "a472f2f79c1144d4f58a347c73ef6710089c631b77b31c6d6da024f25df09945",
    MERGER: "9581868e245cb476b9ccf4b0c66e9f3e5722ed8ccf8cdaeef0c95a355d91bcef",
}


def require(condition: bool, context: object) -> None:
    if not condition:
        raise AssertionError(context)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(8 << 20):
            digest.update(block)
    return digest.hexdigest()


def integer(value: object) -> int:
    return int(value)


def reduced(numerator: int) -> str:
    divisor = math.gcd(abs(numerator), U)
    a, b = numerator // divisor, U // divisor
    return str(a) if b == 1 else f"{a}/{b}"


def main() -> None:
    hashes = {str(path): sha256(path) for path in PINS}
    for path, expected in PINS.items():
        require(hashes[str(path)] == expected, (path, hashes[str(path)]))
    result_hash = sha256(RESULT)
    result = json.loads(RESULT.read_text())
    require(result["status"] == "PASS_COMPLETE_D14_222_K22_HIDDEN_PAIR_TWO_SINK_CHARGE", result["status"])
    require(result["covered_lineage_ids"] == IDS, result["covered_lineage_ids"])
    require(integer(result["scale_U"]) == U, result["scale_U"])
    require(result["input_records_declared"] == result["input_records_consumed"] == N, "records")
    require(result["input_interval"] == [0, N], result["input_interval"])
    require(result["input_sha256"] == PINS[INPUT], result["input_sha256"])
    require(result["retained_nonzero_pair_witness_uses"] == 511_214_060, "uses")
    require(integer(result["pair_weight_sum_scaled"]) == 146_230_609_431_055_564_800, "mass")
    require(result["stabilizer_histogram"] == {"1": 99_314_228, "2": 2_212_958,
            "4": 16_210, "8": 2_099, "16": 224, "32": 4}, "stabilizers")

    with INPUT.open("rb") as handle:
        header = handle.read(HEADER)
        require(header[:8] == b"H16ORM1\0", header[:8])
        require(int.from_bytes(header[8:24], "little", signed=True) == U, "header U")
        require(int.from_bytes(header[32:40], "little") == 246, "orbit chunks")
        require(int.from_bytes(header[40:48], "little") == 305, "zero orbits")
        require(int.from_bytes(header[48:56], "little") == N, "header records")
        require(int.from_bytes(header[64:80], "little", signed=True) == 146_230_609_431_055_564_800, "header mass")
    require(INPUT.stat().st_size == HEADER + RECORD * N, INPUT.stat().st_size)

    shards = result["execution"]["exact_disjoint_interval_shards"]
    require([x["interval"] for x in shards] == [[0, 33_848_574], [33_848_574, 67_697_148], [67_697_148, N]], "shards")
    require(all(x["elapsed_seconds"] < 600 for x in shards), "wall gate")
    shard_objects = []
    for metadata in shards:
        path = Path(metadata["path"])
        require(sha256(path) == metadata["sha256"], path)
        shard_objects.append(json.loads(path.read_text()))
    require(sum(x["input_records_consumed"] for x in shard_objects) == N, "shard records")

    for lineage_id, first_count, terminal_count in ((IDS[0], 32, 32), (IDS[1], 60, 12)):
        sink = result["sinks"][lineage_id]
        require(sink["first_tail_evaluations"] == first_count * N, lineage_id)
        require(sink["terminal_K22_occurrences"] == terminal_count * sink["selected_next_pivots"], lineage_id)
        require(sink["full_occurrences"] == sink["irreducible_occurrences"] == sink["terminal_K22_occurrences"], lineage_id)
        require(integer(sink["normalized_next_pivot_weight_sum_scaled"]) == -integer(sink["pivotable_intermediate_weight_sum_scaled"]), lineage_id)
        require(integer(sink["terminal_K22_weight_sum_scaled"]) == terminal_count * integer(sink["normalized_next_pivot_weight_sum_scaled"]), lineage_id)
        require(integer(sink["full_charge_scaled"]) == integer(sink["irreducible_charge_scaled"]), lineage_id)
        require(sink["full_charge_reduced"] == reduced(integer(sink["full_charge_scaled"])), lineage_id)
        cache = sink["response_cache"]
        require(cache["hits"] + cache["misses"] == sink["selected_next_pivots"], lineage_id)
        require(cache["peak_keys_per_worker_chunk"] <= cache["hard_max_keys_per_worker_sink"] + 720, lineage_id)
        provenance = sink["m2_m3_provenance"]
        require(sum(x["pivotable_intermediate_children"] for x in provenance.values()) == sink["pivotable_intermediate_children"], lineage_id)
        require(sum(integer(x["signed_intermediate_weight_scaled"]) for x in provenance.values()) == integer(sink["pivotable_intermediate_weight_sum_scaled"]), lineage_id)
        require(sum(x["selected_next_pivots"] for x in provenance.values()) == sink["selected_next_pivots"], lineage_id)
        require(sum(x["terminal_K22_children"] for x in provenance.values()) == sink["terminal_K22_occurrences"], lineage_id)
        require(sum(integer(x["charge_scaled"]) for x in provenance.values()) == integer(sink["full_charge_scaled"]), lineage_id)
        require(sum(integer(x["sinks"][lineage_id]["full_charge_scaled"]) for x in shard_objects) == integer(sink["full_charge_scaled"]), lineage_id)

    source_text = SOURCE.read_text()
    require(source_text.count("!pivotable_sig(sig22, e)") == 4, "four abstract/literal terminal guards")
    require("assert_eq!(U % ((m2 as i128) * (m3 as i128)), 0);" in source_text, "U divisor guard")
    require(source_text.count("assert_eq!(x.weight_after_p2 %") >= 2, "w2 divisor guards")
    require("let w3 = -x.weight_after_p2" in source_text, "sign guard")

    ledger = Path(result["literal_sample_guard"]["ledger"])
    lines = ledger.read_text().splitlines()
    require(len(lines) == 258, len(lines))
    require(len(lines[0].split("\t")) == 22, lines[0])
    rows = [line.split("\t") for line in lines[1:]]
    require(all(len(row) == 22 for row in rows), "sample width")
    indices = [int(row[0]) for row in rows]
    expected_indices = [j * (N - 1) // 256 for j in range(257)]
    require(indices == expected_indices, "global sample distribution")
    nonzero33 = nonzero42 = 0
    with INPUT.open("rb") as handle:
        for row in rows:
            index = int(row[0])
            handle.seek(HEADER + RECORD * index)
            record = handle.read(RECORD)
            require(len(record) == RECORD, index)
            decoded = [
                str(index), record[:24].hex(), str(record[24]),
                str(int.from_bytes(record[25:41], "little", signed=True)),
                str(int.from_bytes(record[41:49], "little")),
                str(int.from_bytes(record[49:51], "little")),
                str(int.from_bytes(record[51:53], "little")),
            ]
            require(row[:7] == decoded, (index, row[:7], decoded))
            require(int(row[5]) * int(row[6]) == 384, index)
            require(int(row[8]) == 32, (index, "R233 first tails"))
            require(int(row[11]) == 32 * int(row[10]), (index, "R233 terminal tails"))
            require(int(row[14]) == 60, (index, "R242 first tails"))
            require(int(row[17]) == 12 * int(row[16]), (index, "R242 terminal tails"))
            require(int(row[20]) == (int(row[10]) > 0), (index, "R233 flag"))
            require(int(row[21]) == (int(row[16]) > 0), (index, "R242 flag"))
            nonzero33 += int(row[20])
            nonzero42 += int(row[21])
    guard = result["literal_sample_guard"]
    require((nonzero33, nonzero42) == (guard["R233_nonzero_continuations"], guard["R242_nonzero_continuations"]), "sample flags")
    require((nonzero33, nonzero42) == (212, 42), "distributed nonzero witnesses")
    require(guard["all_literal_K22_children_nonpivotable"] is True, guard)
    require(guard["all_abstract_literal_cycle_keys_equal"] is True, guard)

    audit = {
        "status": "PASS_INDEPENDENT_SOURCE_COUNT_HASH_SAMPLE_REFEREE",
        "covered_lineage_ids": IDS,
        "result": str(RESULT),
        "result_sha256": result_hash,
        "source_and_runtime_sha256": hashes,
        "source_ledger": {
            "records": N,
            "bytes": INPUT.stat().st_size,
            "header_schema_mass_pins": True,
            "all_257_sample_records_replayed_from_source_bytes": True,
        },
        "exact_arithmetic": {
            "U": U,
            "all_shard_and_provenance_sums_equal_final_sinks": True,
            "all_count_weight_charge_and_reduced_fraction_identities": True,
            "third_divisor_and_sign_assertions_source_pinned": True,
        },
        "terminality": {
            "four_abstract_literal_producer_guards_source_pinned": True,
            "full_equals_irreducible_both_sinks": True,
        },
        "literal_sample_scope": {
            "records": 257,
            "indices_exactly_global_even_spacing": True,
            "source_records_byte_replayed": True,
            "R233_nonzero_continuations": nonzero33,
            "R242_nonzero_continuations": nonzero42,
            "producer_asserted_literal_vs_abstract_cycle_key_equality": True,
            "producer_asserted_literal_K22_terminality": True,
            "referee_does_not_claim_an_independent_second_full_graph_fold": True,
        },
        "wall_gate": {
            "maximum_shard_elapsed_seconds": max(x["elapsed_seconds"] for x in shards),
            "hard_seconds": 600,
            "all_shards_pass": True,
        },
        "scope": "Independent source/count/hash/sample audit of exactly two K22 scalar sinks; no K23 or conjecture verdict.",
    }
    tmp = Path(f"{AUDIT}.tmp")
    tmp.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    tmp.replace(AUDIT)
    print(json.dumps({"status": audit["status"], "result_sha256": result_hash,
                      "sample_nonzero": [nonzero33, nonzero42]}, sort_keys=True))


if __name__ == "__main__":
    main()

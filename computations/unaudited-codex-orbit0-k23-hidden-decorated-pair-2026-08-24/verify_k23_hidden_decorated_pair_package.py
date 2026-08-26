#!/usr/bin/env python3
"""Independent exact source/evidence/merge/referee checker for the K23 pair."""
import argparse
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
U = 400_591_699_200
TOTAL = 101_545_723
INTERVALS = [[0, 33_848_574], [33_848_574, 67_697_148], [67_697_148, TOTAL]]
IDS = ["D14:222|R:2-3-4", "D14:222|R:2-4-3"]
SOURCE = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin"
SOURCE_SHA = "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8"
HEADER_BYTES = 80
RECORD_BYTES = 53
HEADER = "input_index\tK16_row\tp2\tweight_after_p2\tpair_uses\torbit\tstabilizer\tR234_first_children\tR234_pivotable_intermediate\tR234_selected_p3\tR234_terminal_K23\tR234_terminal_weight_scaled\tR234_charge_scaled\tR243_first_children\tR243_pivotable_intermediate\tR243_selected_p3\tR243_terminal_K23\tR243_terminal_weight_scaled\tR243_charge_scaled\tR234_nonzero\tR243_nonzero"
EXPECTED_CHARGES = {
    IDS[0]: -292_869_665_337_482_477_568,
    IDS[1]: -119_114_845_190_185_844_736,
}


def req(condition, message):
    if not condition:
        raise ValueError(message)


def resolve(path):
    path = Path(path)
    return path if path.is_absolute() else ROOT / path


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("result")
    parser.add_argument("literal_referee")
    parser.add_argument("output")
    args = parser.parse_args()
    result_path = resolve(args.result)
    result = json.loads(result_path.read_text())
    req(result["status"] == "PASS_COMPLETE_K23_HIDDEN_DECORATED_PAIR_TWO_ID_CHARGE", "result status")
    req(result["degree"] == 23 and int(result["scale_U"]) == U, "degree/U")
    req(result["covered_lineage_ids"] == IDS, "strict two-ID scope")
    req(result["input_interval"] == [0, TOTAL] and result["input_records"] == TOTAL, "full input interval")
    req(result["input"] == str(SOURCE.relative_to(ROOT)) and result["input_sha256"] == SOURCE_SHA, "source pin")
    req(result["retained_pair_uses"] == 511_214_060 and int(result["pair_weight_sum_scaled"]) == 146_230_609_431_055_564_800, "source global totals")
    req(result["full_equals_irreducible"] is True, "terminal full/irreducible guard")
    subtotal = 0
    for identifier, first_factor, terminal_factor in ((IDS[0], 32, 60), (IDS[1], 60, 32)):
        sink = result["sinks"][identifier]
        req(int(sink["full_charge_scaled"]) == EXPECTED_CHARGES[identifier], "exact per-ID charge")
        req(sink["full_charge_scaled"] == sink["irreducible_charge_scaled"], "per-ID full/irreducible charge")
        req(Fraction(int(sink["full_charge_scaled"]), U) == Fraction(sink["exact_charge"]), "per-ID rational")
        req(sink["first_tail_evaluations"] == first_factor * TOTAL, "per-ID first tails")
        req(sink["terminal_K23_occurrences"] == terminal_factor * sink["selected_p3"], "per-ID terminal tails")
        req(sink["full_occurrences"] == sink["irreducible_occurrences"] == sink["terminal_K23_occurrences"], "per-ID terminality")
        req(sum(sink["m2_m3_histogram"].values()) == sink["pivotable_intermediate_children"], "per-ID histogram count")
        req(sum(int(key.split("_")[1]) * value for key, value in sink["m2_m3_histogram"].items()) == sink["selected_p3"], "per-ID histogram multiplicity")
        req(int(sink["normalized_p3_weight_scaled"]) == -int(sink["pivotable_weight_scaled"]), "per-ID sign")
        req(int(sink["terminal_weight_scaled"]) == terminal_factor * int(sink["normalized_p3_weight_scaled"]), "per-ID terminal weight")
        req(sink["cache_shard_sums"]["hits"] + sink["cache_shard_sums"]["misses"] == sink["selected_p3"], "per-ID cache accounting")
        req(sink["cache_shard_max_peak_keys"] <= 300_720, "per-ID cache gate")
        subtotal += int(sink["full_charge_scaled"])
    req(subtotal == -411_984_510_527_668_322_304, "exact two-ID scaled subtotal")
    req(int(result["subtotal_scaled_charge"]) == subtotal and Fraction(subtotal, U) == Fraction(result["exact_subtotal"]), "exact subtotal rational")
    req(len(result["shard_evidence"]) == 3 and [item["interval"] for item in result["shard_evidence"]] == INTERVALS, "exact no-gap partition")
    candidates = []
    for evidence in result["shard_evidence"]:
        shard = resolve(evidence["result"])
        samples = resolve(evidence["samples"])
        req(sha(shard) == evidence["result_sha256"] and sha(samples) == evidence["samples_sha256"], "shard evidence hash")
        lines = samples.read_text().splitlines()
        req(lines[0] == HEADER and len(lines) == 258, "shard sample shape")
        candidates.extend((int(line.split("\t", 1)[0]), line) for line in lines[1:])
    req(len(candidates) == 771 and len({index for index, _ in candidates}) == 771, "pooled witness census")
    selected = []
    for ordinal in range(257):
        target = ordinal * (TOTAL - 1) // 256
        selected.append(min(candidates, key=lambda item: (abs(item[0] - target), item[0], item[1])))
    req(len({index for index, _ in selected}) == 257, "merged witness distinctness")
    selected.sort()
    merged_samples = resolve(result["literal_witness_guard"]["ledger"])
    merged_lines = merged_samples.read_text().splitlines()
    req(merged_lines == [HEADER] + [line for _, line in selected], "deterministic merged witness selection")
    req(sha(merged_samples) == result["literal_witness_guard"]["ledger_sha256"], "merged witness hash")
    req(SOURCE.stat().st_size == HEADER_BYTES + RECORD_BYTES * TOTAL and sha(SOURCE) == SOURCE_SHA, "source size/hash")
    with open(SOURCE, "rb") as stream:
        header = stream.read(HEADER_BYTES)
        req(header[:8] == b"H16ORM1\0", "source magic")
        req(int.from_bytes(header[8:24], "little", signed=True) == U, "source U")
        req(int.from_bytes(header[28:30], "little") == RECORD_BYTES, "source record size")
        req(int.from_bytes(header[32:40], "little") == 246 and int.from_bytes(header[40:48], "little") == 305, "source K16 orbit dimensions")
        req(int.from_bytes(header[48:56], "little") == TOTAL, "source record count")
        req(int.from_bytes(header[64:80], "little", signed=True) == 146_230_609_431_055_564_800, "source pair mass")
        for index, line in selected:
            fields = line.split("\t")
            stream.seek(HEADER_BYTES + RECORD_BYTES * index)
            record = stream.read(RECORD_BYTES)
            req(len(record) == RECORD_BYTES and fields[1] == record[:24].hex(), "literal source row")
            req(int(fields[2]) == record[24], "literal p2")
            req(int(fields[3]) == int.from_bytes(record[25:41], "little", signed=True), "literal coefficient")
            req(int(fields[4]) == int.from_bytes(record[41:49], "little"), "literal uses")
            orbit = int.from_bytes(record[49:51], "little")
            stabilizer = int.from_bytes(record[51:53], "little")
            req(int(fields[5]) == orbit and int(fields[6]) == stabilizer and orbit * stabilizer == 384, "literal orbit/stabilizer")
    referee_path = resolve(args.literal_referee)
    referee = json.loads(referee_path.read_text())
    req(referee["status"] == "PASS_INDEPENDENT_K23_HIDDEN_DECORATED_PAIR_LITERAL_REPLAY", "literal referee status")
    req(referee["input_interval"] == [0, TOTAL] and referee["samples"] == 257, "literal referee scope")
    req(referee["sample_index_mode"] == "caller-selected distinct sorted indices", "literal referee index mode")
    req(referee["R234_nonzero"] == 216 and referee["R243_nonzero"] == 41, "literal support census")
    req(referee["all_source_fields_exact"] and referee["all_occurrencewise_U_and_weight_divisions_exact"], "literal exactness")
    req(referee["all_literal_terminal_K23_children_nonpivotable"] and referee["all_abstract_literal_cycle_keys_and_charges_equal"], "literal terminal/cycle replay")
    req(not any(key in result for key in ("rows", "row_output", "K24", "membership", "residual")), "scope contamination")
    audit = {
        "status": "PASS_INDEPENDENT_K23_HIDDEN_DECORATED_PAIR_COMPLETE_REFEREE",
        "degree": 23,
        "covered_lineage_ids": IDS,
        "result_sha256": sha(result_path),
        "source_sha256": SOURCE_SHA,
        "no_gap_intervals_rehashed": 3,
        "pooled_candidate_records": 771,
        "literal_source_records_replayed": 257,
        "literal_referee_sha256": sha(referee_path),
        "subtotal_scaled_charge": str(subtotal),
        "exact_subtotal": str(Fraction(subtotal, U)),
        "full_equals_irreducible": True,
        "no_rows_K24_or_membership_claim": True,
        "scope": "strict two-ID K23 scalar/source/sample referee only; no complete-59 claim",
    }
    output = resolve(args.output)
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()

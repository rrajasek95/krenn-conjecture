#!/usr/bin/env python3
"""Strict exact three-interval merger for the K23 hidden decorated pair."""
import argparse
import hashlib
import json
import os
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
U = 400_591_699_200
TOTAL = 101_545_723
PAIR_USES = 511_214_060
PAIR_WEIGHT = 146_230_609_431_055_564_800
INPUT = "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin"
INPUT_SHA = "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8"
IDS = ["D14:222|R:2-3-4", "D14:222|R:2-4-3"]
INTERVALS = [[0, 33_848_574], [33_848_574, 67_697_148], [67_697_148, TOTAL]]
HEADER = "input_index\tK16_row\tp2\tweight_after_p2\tpair_uses\torbit\tstabilizer\tR234_first_children\tR234_pivotable_intermediate\tR234_selected_p3\tR234_terminal_K23\tR234_terminal_weight_scaled\tR234_charge_scaled\tR243_first_children\tR243_pivotable_intermediate\tR243_selected_p3\tR243_terminal_K23\tR243_terminal_weight_scaled\tR243_charge_scaled\tR234_nonzero\tR243_nonzero"


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


def atomic_json(path, payload):
    temporary = Path(str(path) + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def validate_sink(sink, records, first_factor, terminal_factor):
    req(sink["first_tail_evaluations"] == first_factor * records, "first-tail count")
    req(sink["terminal_K23_occurrences"] == terminal_factor * sink["selected_p3"], "terminal-tail count")
    req(sink["full_occurrences"] == sink["irreducible_occurrences"] == sink["terminal_K23_occurrences"], "terminality count")
    req(sink["full_charge_scaled"] == sink["irreducible_charge_scaled"], "full/irreducible charge")
    histogram = sink["m2_m3_histogram"]
    req(sum(histogram.values()) == sink["pivotable_intermediate_children"], "pivot histogram count")
    req(sum(int(key.split("_")[1]) * value for key, value in histogram.items()) == sink["selected_p3"], "selected-p3 histogram")
    for key in histogram:
        m2, m3 = map(int, key.split("_"))
        req(U % (m2 * m3) == 0, "nonintegral U/(m2*m3)")
    req(int(sink["normalized_p3_weight_scaled"]) == -int(sink["pivotable_weight_scaled"]), "second-pivot sign")
    req(int(sink["terminal_weight_scaled"]) == terminal_factor * int(sink["normalized_p3_weight_scaled"]), "terminal weight")
    cache = sink["cache"]
    req(cache["hits"] + cache["misses"] == sink["selected_p3"], "cache accounting")
    req(cache["peak_keys"] <= 300_720, "cache peak gate")


def validate_shard(doc, interval):
    records = interval[1] - interval[0]
    req(doc["status"] == "PASS_BOUNDED_K23_HIDDEN_DECORATED_PAIR_TWO_SINK", "shard status")
    req(doc["covered_lineage_ids"] == IDS, "strict ID scope")
    req(int(doc["scale_U"]) == U and doc["input"] == INPUT, "U/input")
    req(doc["input_sha256_expected"] == INPUT_SHA, "source hash pin")
    req(doc["input_records_declared"] == TOTAL and doc["input_interval"] == interval, "interval/header count")
    req(doc["input_records_consumed"] == records, "interval record count")
    req(doc["workers"] == 8 and doc["cache_chunk_records"] == 100_000, "worker/cache gate")
    req(sum(doc["stabilizer_histogram"].values()) == records, "stabilizer histogram")
    validate_sink(doc["sinks"][IDS[0]], records, 32, 60)
    validate_sink(doc["sinks"][IDS[1]], records, 60, 32)


def read_samples(doc, interval):
    guard = doc["literal_witness_guard"]
    req(guard["records"] == 257, "local witness count")
    req(guard["all_terminal_K23_nonpivotable"] is True and guard["all_abstract_literal_cycle_keys_equal"] is True, "local witness guard")
    path = resolve(guard["ledger"])
    lines = path.read_text().splitlines()
    req(lines and lines[0] == HEADER and len(lines) == 258, "local witness ledger shape")
    expected = [interval[0] + j * (interval[1] - interval[0] - 1) // 256 for j in range(257)]
    rows = []
    for expected_index, line in zip(expected, lines[1:]):
        fields = line.split("\t")
        req(len(fields) == 21 and int(fields[0]) == expected_index, "local witness distribution")
        req(interval[0] <= expected_index < interval[1], "local witness interval")
        req(int(fields[7]) == 32 and int(fields[10]) == 60 * int(fields[9]), "R234 literal counts")
        req(int(fields[13]) == 60 and int(fields[16]) == 32 * int(fields[15]), "R243 literal counts")
        req(int(fields[19]) == int(int(fields[9]) > 0) and int(fields[20]) == int(int(fields[15]) > 0), "literal support flags")
        rows.append((expected_index, line))
    return path, rows


def merge(shard_names, output_name):
    req(len(shard_names) == 3, "exactly three shards required")
    shards = []
    evidence = []
    candidates = []
    for supplied, interval in zip(shard_names, INTERVALS):
        path = resolve(supplied)
        doc = json.loads(path.read_text())
        validate_shard(doc, interval)
        samples, rows = read_samples(doc, interval)
        shards.append(doc)
        candidates.extend(rows)
        evidence.append({
            "interval": interval,
            "result": str(path.relative_to(ROOT)),
            "result_sha256": sha(path),
            "samples": str(samples.relative_to(ROOT)),
            "samples_sha256": sha(samples),
        })
    req([entry["interval"] for entry in evidence] == INTERVALS, "no-gap interval partition")
    req(len(candidates) == 771 and len({index for index, _ in candidates}) == 771, "candidate census")
    # Freeze 257 globally distributed witnesses without traversing source records again.
    # The tie break is fully deterministic and is independently recomputed by the checker.
    selected = []
    for ordinal in range(257):
        target = ordinal * (TOTAL - 1) // 256
        choice = min(candidates, key=lambda item: (abs(item[0] - target), item[0], item[1]))
        selected.append(choice)
    req(len({index for index, _ in selected}) == 257, "distinct merged witnesses")
    selected.sort()
    output = resolve(output_name)
    sample_path = Path(str(output) + ".samples.tsv")
    temporary = Path(str(sample_path) + ".tmp")
    temporary.write_text(HEADER + "\n" + "\n".join(line for _, line in selected) + "\n")
    os.replace(temporary, sample_path)
    add = lambda field: sum(int(doc[field]) for doc in shards)
    req(add("input_records_consumed") == TOTAL, "global record count")
    req(add("retained_pair_uses") == PAIR_USES, "global pair-use count")
    req(add("pair_weight_sum_scaled") == PAIR_WEIGHT, "global pair weight")
    stabilizers = defaultdict(int)
    for doc in shards:
        for key, value in doc["stabilizer_histogram"].items():
            stabilizers[key] += value
    req(sum(stabilizers.values()) == TOTAL, "global stabilizer count")
    sinks = {}
    for identifier, first_factor, terminal_factor in ((IDS[0], 32, 60), (IDS[1], 60, 32)):
        parts = [doc["sinks"][identifier] for doc in shards]
        histogram = defaultdict(int)
        for part in parts:
            for key, value in part["m2_m3_histogram"].items():
                histogram[key] += value
        total = {}
        for field in ("first_tail_evaluations", "pivotable_intermediate_children", "selected_p3", "terminal_K23_occurrences", "full_occurrences", "irreducible_occurrences"):
            total[field] = sum(part[field] for part in parts)
        for field in ("pivotable_weight_scaled", "normalized_p3_weight_scaled", "terminal_weight_scaled", "full_charge_scaled", "irreducible_charge_scaled"):
            total[field] = str(sum(int(part[field]) for part in parts))
        total["m2_m3_histogram"] = dict(sorted(histogram.items()))
        total["cache_shard_sums"] = {
            field: sum(part["cache"][field] for part in parts)
            for field in ("hits", "misses", "clears")
        }
        total["cache_shard_max_peak_keys"] = max(part["cache"]["peak_keys"] for part in parts)
        validate_sink({**total, "cache": {
            "hits": total["cache_shard_sums"]["hits"],
            "misses": total["cache_shard_sums"]["misses"],
            "clears": total["cache_shard_sums"]["clears"],
            "peak_keys": total["cache_shard_max_peak_keys"],
        }}, TOTAL, first_factor, terminal_factor)
        total["first_tail_degree"] = 4 if first_factor == 60 else 3
        total["terminal_tail_degree"] = 4 if terminal_factor == 60 else 3
        total["exact_charge"] = str(Fraction(int(total["full_charge_scaled"]), U))
        sinks[identifier] = total
    subtotal = sum(int(sinks[identifier]["full_charge_scaled"]) for identifier in IDS)
    result = {
        "status": "PASS_COMPLETE_K23_HIDDEN_DECORATED_PAIR_TWO_ID_CHARGE",
        "degree": 23,
        "scale_U": str(U),
        "covered_lineage_ids": IDS,
        "input": INPUT,
        "input_sha256": INPUT_SHA,
        "input_header_magic": "H16ORM1\\0",
        "input_interval": [0, TOTAL],
        "input_records": TOTAL,
        "retained_pair_uses": PAIR_USES,
        "pair_weight_sum_scaled": str(PAIR_WEIGHT),
        "stabilizer_histogram": dict(sorted(stabilizers.items(), key=lambda item: int(item[0]))),
        "sinks": sinks,
        "subtotal_scaled_charge": str(subtotal),
        "exact_subtotal": str(Fraction(subtotal, U)),
        "shard_evidence": evidence,
        "literal_witness_guard": {
            "candidate_records": 771,
            "selected_records": 257,
            "selection_rule": "for global target floor(j*(N-1)/256), choose pooled candidate minimizing (absolute distance, source index, full TSV line), then sort by source index",
            "ledger": str(sample_path.relative_to(ROOT)),
            "ledger_sha256": sha(sample_path),
        },
        "sign_rule": "w3=-w2/m3 occurrencewise; first-tail sign preserved; U%(m2*m3)=0",
        "full_equals_irreducible": True,
        "scope": "strict two-ID complete K23 scalar fragment only; exact no-gap three-shard merge; no rows, K24, membership, or complete-59 claim",
    }
    atomic_json(output, result)
    print(json.dumps({"status": result["status"], "subtotal_scaled_charge": str(subtotal), "exact_subtotal": result["exact_subtotal"], "witnesses": 257}, sort_keys=True))


def hostile_self_test():
    rejected = 0
    good = {"first_tail_evaluations": 32, "pivotable_intermediate_children": 1, "selected_p3": 2, "terminal_K23_occurrences": 120, "full_occurrences": 120, "irreducible_occurrences": 120, "pivotable_weight_scaled": "6", "normalized_p3_weight_scaled": "-6", "terminal_weight_scaled": "-360", "full_charge_scaled": "1", "irreducible_charge_scaled": "1", "cache": {"hits": 1, "misses": 1, "clears": 1, "peak_keys": 1}, "m2_m3_histogram": {"2_2": 1}}
    for field, value in (("irreducible_occurrences", 119), ("normalized_p3_weight_scaled", "6"), ("selected_p3", 3), ("full_charge_scaled", "2")):
        bad = json.loads(json.dumps(good))
        bad[field] = value
        try:
            validate_sink(bad, 1, 32, 60)
        except (ValueError, KeyError, TypeError):
            rejected += 1
        else:
            raise ValueError("hostile mutation accepted")
    req(rejected == 4, "hostile self-test count")
    print(json.dumps({"status": "PASS_HIDDEN_DECORATED_MERGER_HOSTILE_SELFTEST", "rejected": rejected}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output")
    parser.add_argument("shards", nargs="*")
    args = parser.parse_args()
    if args.self_test:
        hostile_self_test()
    else:
        req(args.output is not None and len(args.shards) == 3, "--output and exactly three shards required")
        merge(args.shards, args.output)


if __name__ == "__main__":
    main()

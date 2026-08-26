#!/usr/bin/env python3
"""Strict two-shard merger for the K23 D14 source-formula fold."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path

U = 400_591_699_200
INTERVALS = [(0, 243), (243, 485)]
IDS = ["D14:222|R:3-2-4", "D14:222|R:3-3-3", "D14:222|R:4-2-3"]
DEGREES = [(3, 2, 4), (3, 3, 3), (4, 2, 3)]
EXPECTED = [
    (6_619_280, 211_816_960, 197_414_400, 815_482_880, 9_785_794_560, 2_969_658_880, 5_075_412_480, 304_524_748_800),
    (6_619_280, 211_816_960, 197_414_400, 815_482_880, 26_095_452_160, 2_687_815_680, 2_687_815_680, 86_010_101_760),
    (6_619_280, 397_156_800, 357_580_800, 910_713_600, 10_928_563_200, 1_375_382_400, 1_375_382_400, 44_012_236_800),
]
SUM_FIELDS = (
    "selected_p1_uses", "first_children", "pivotable_first_children", "selected_p2_uses",
    "second_children", "pivotable_second_children", "selected_p3_uses", "K23_terminal_occurrences",
    "full_occurrences", "irreducible_occurrences",
)
HISTS = ("first_denominator_hist", "second_denominator_hist", "third_denominator_hist", "product_denominator_hist")
CACHE_SUM = (
    ("plan_cache", "first_hits"), ("plan_cache", "first_misses"),
    ("plan_cache", "second_hits"), ("plan_cache", "second_misses"),
    ("literal_preterminal_cache", "hits"), ("literal_preterminal_cache", "misses"),
    ("terminal_profile_cache", "hits"), ("terminal_profile_cache", "misses"),
    ("terminal_profile_cache", "clears_at_hard_cap"),
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def merge_hist(parts: list[dict], field: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for part in parts:
        for key, value in part[field].items():
            out[key] = out.get(key, 0) + value
    return dict(sorted(out.items(), key=lambda item: int(item[0])))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("shards", nargs=2, type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    docs = [json.loads(path.read_text()) for path in args.shards]
    for doc, interval in zip(docs, INTERVALS, strict=True):
        lo, hi = interval
        assert doc["status"] == "PASS_BOUNDED_D14_222_K23_SOURCE_THREE_EVALUATOR"
        assert doc["covered_lineage_ids"] == IDS and doc["scale_U"] == str(U)
        assert doc["R8_record_interval"] == [lo, hi] and not doc["distributed_record_mode"]
        assert doc["R8_records_consumed"] == hi - lo and doc["R8_records_declared"] == 485
        assert doc["source_heads"] == (hi - lo) * 1728
        assert doc["all_realized_cached_K23_responses_terminal"]
        assert list(doc["sinks"]) == IDS

    sinks = {}
    for index, (lineage, degrees, expected) in enumerate(zip(IDS, DEGREES, EXPECTED, strict=True)):
        parts = [doc["sinks"][lineage] for doc in docs]
        out = {
            "first_response_degree": degrees[0],
            "second_response_degree": degrees[1],
            "terminal_response_degree": degrees[2],
        }
        assert all((part["first_response_degree"], part["second_response_degree"], part["terminal_response_degree"]) == degrees for part in parts)
        for field in SUM_FIELDS:
            out[field] = sum(part[field] for part in parts)
        charge = sum(int(part["full_charge_scaled_U"]) for part in parts)
        assert all(part["full_charge_scaled_U"] == part["irreducible_charge_scaled_U"] for part in parts)
        out["full_charge_scaled_U"] = out["irreducible_charge_scaled_U"] = str(charge)
        exact = Fraction(charge, U)
        out["exact_charge"] = f"{exact.numerator}/{exact.denominator}"
        for field in HISTS:
            out[field] = merge_hist(parts, field)
        out["plan_cache"] = {key: sum(part[parent][key] for part in parts) for parent, key in CACHE_SUM if parent == "plan_cache"}
        out["literal_preterminal_cache"] = {
            "hits": sum(part["literal_preterminal_cache"]["hits"] for part in parts),
            "misses": sum(part["literal_preterminal_cache"]["misses"] for part in parts),
            "scope": "one source head, exact Row+terminal-degree key",
        }
        caps = {part["terminal_profile_cache"]["hard_cap_keys_per_worker"] for part in parts}
        assert caps == {3_000_000}
        out["terminal_profile_cache"] = {
            "hits": sum(part["terminal_profile_cache"]["hits"] for part in parts),
            "misses": sum(part["terminal_profile_cache"]["misses"] for part in parts),
            "clears_at_hard_cap": sum(part["terminal_profile_cache"]["clears_at_hard_cap"] for part in parts),
            "hard_cap_keys_per_worker": 3_000_000,
        }
        structural = tuple(out[field] for field in SUM_FIELDS[:8])
        assert structural == expected, (lineage, structural, expected)
        assert out["full_occurrences"] == out["irreducible_occurrences"] == out["K23_terminal_occurrences"]
        sinks[lineage] = out

    # Explicit tail cardinalities avoid confusing response degree with arity.
    assert sinks[IDS[0]]["K23_terminal_occurrences"] == 60 * sinks[IDS[0]]["selected_p3_uses"]
    assert sinks[IDS[1]]["K23_terminal_occurrences"] == 32 * sinks[IDS[1]]["selected_p3_uses"]
    assert sinks[IDS[2]]["K23_terminal_occurrences"] == 32 * sinks[IDS[2]]["selected_p3_uses"]

    header = None
    samples: dict[tuple[str, int], tuple[int, str]] = {}
    sample_inputs = []
    for result_path, doc in zip(args.shards, docs, strict=True):
        path = Path(doc["literal_sample_guard"]["ledger"])
        if not path.is_absolute(): path = Path.cwd() / path
        lines = path.read_text().splitlines(); assert lines
        header = header or lines[0]; assert lines[0] == header
        for line in lines[1:]:
            c = line.split("\t"); assert len(c) == 28
            lineage, bin_index, head_index, r8_index = c[0], int(c[1]), int(c[2]), int(c[3])
            assert lineage in IDS and 0 <= bin_index < 257
            assert bin_index == head_index * 257 // (485 * 1728)
            assert r8_index == head_index // 1728
            key = (lineage, bin_index)
            if key not in samples or head_index < samples[key][0]: samples[key] = (head_index, line)
        sample_inputs.append({"result": str(result_path), "ledger": str(path), "sha256": sha(path)})
    assert set(samples) == {(lineage, bin_index) for lineage in IDS for bin_index in range(257)}
    sample_out = Path(f"{args.output}.samples.tsv")
    sample_tmp = Path(f"{sample_out}.tmp")
    ordered = [samples[(lineage, bin_index)][1] for lineage in IDS for bin_index in range(257)]
    sample_tmp.write_text(header + "\n" + "\n".join(ordered) + "\n")
    os.replace(sample_tmp, sample_out)
    for lineage in IDS: sinks[lineage]["literal_samples"] = 257

    peak = max(doc["terminal_cache_resource_guard"]["peak_keys_per_worker"] for doc in docs)
    assert peak <= 3_000_000
    result = {
        "status": "PASS_COMPLETE_D14_222_K23_SOURCE_THREE_CHARGE",
        "covered_lineage_ids": IDS,
        "scale_U": str(U),
        "source_shards": [list(x) for x in INTERVALS],
        "R8_records_consumed": 485,
        "R8_records_declared": 485,
        "source_heads": 838_080,
        "source_mass_sum": str(sum(int(doc["source_mass_sum"]) for doc in docs)),
        "source_mass_l1": str(sum(int(doc["source_mass_l1"]) for doc in docs)),
        "sinks": sinks,
        "all_realized_cached_K23_responses_terminal": True,
        "literal_sample_guard": {"records": 771, "records_per_sink": [257,257,257], "all_literal_K23_children_terminal": True, "all_abstract_literal_cycle_keys_equal": True, "ledger": str(sample_out)},
        "sample_inputs": sample_inputs,
        "input_result_sha256": {str(path): sha(path) for path in args.shards},
        "sign_rule": docs[0]["sign_rule"],
        "compression_proof": docs[0]["compression_proof"],
        "shared_fold_scope": docs[0]["shared_fold_scope"],
        "terminal_cache_resource_guard": {"hard_cap_keys_per_worker": 3_000_000, "peak_keys_per_worker": peak},
        "elapsed_seconds_sum": sum(doc["elapsed_seconds"] for doc in docs),
        "scope": "exact strict two-shard merge of three named D14 K23 scalar sinks; no row output, K24 scalar, membership, or conjecture claim",
    }
    tmp = Path(f"{args.output}.tmp")
    tmp.write_text(json.dumps(result, indent=2) + "\n")
    os.replace(tmp, args.output)
    print(json.dumps({"status": result["status"], "output": str(args.output), "sha256": sha(args.output), "samples_sha256": sha(sample_out)}, indent=2))


if __name__ == "__main__":
    main()

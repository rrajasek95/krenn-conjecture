#!/usr/bin/env python3
"""Strict two-half structural validator/merger for grouped K24 D16 R2-2-4."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

N = 24_097_095
MID = 12_048_547
U = 400_591_699_200
IDS = [f"D16:{packet}|R:2-2-4" for packet in ("224", "233", "242", "323", "332", "422")]
HEADER = [
    "sample_ordinal", "record_index", "coefficient", "source_row", "K18_row",
    "K20_row", "p1", "t1", "p2", "t2", "p3", "m1", "m2", "m3",
    "terminal_q", "unit_scaled_U", "nonzero_contribution_scaled_U", "final_degree",
]
SUM_FIELDS = [
    "source_rows", "signed_source_coefficient", "l1_source_coefficient",
    "pivotable_K16_rows", "p1_uses", "K18_children", "pivotable_K18_children",
    "p2_uses", "K20_children", "pivotable_K20_children", "p3_uses",
    "K24_terminal_occurrences", "full_occurrences", "irreducible_occurrences",
    "full_charge_scaled_U", "irreducible_charge_scaled_U",
]
PACKET_GUARD = "checkpoint retains collected canonical rows and coefficients but not packet labels; only the grouped six-ID scalar is source-faithful"
SIGN_RULE = "stored v is the direct coefficient in P; three normalized response flips give -v/(m1*m2*m3)"
TERMINALITY = "every K24 K4 child has active-anchor mass 0 and cannot pivot; full equals irreducible"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def number(value, name: str) -> int:
    require(not isinstance(value, bool), f"{name}: bool is not integer")
    try:
        return int(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{name}: bad integer {value!r}") from exc


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_samples(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        require(reader.fieldnames == HEADER, "R2-2-4 sample header")
        rows = list(reader)
    require(all(set(row) == set(HEADER) for row in rows), "R2-2-4 ragged sample row")
    return rows


def validate_shard(result_path: Path, samples_path: Path, start: int, end: int) -> dict:
    require((start, end) in {(0, MID), (MID, N)}, "R2-2-4 interval is not a frozen half")
    result = json.loads(result_path.read_text())
    require(result.get("status") == "PASS_BOUNDED_GROUPED_SIX_D16_R_2_2_4_K24_CHARGE_ONLY_GATE", "R2-2-4 shard status")
    require(result.get("group_id") == "source_D16_R2_2_4" and result.get("ids") == IDS, "R2-2-4 scope")
    require(number(result.get("degree"), "degree") == 24 and number(result.get("scale_U"), "U") == U, "R2-2-4 degree/U")
    require(number(result.get("covered_ids"), "covered") == 6 and result.get("individual_id_charges") is None, "R2-2-4 grouped semantics")
    require(result.get("record_interval") == [start, end] and result.get("distributed_prefix") is False, "R2-2-4 interval/mode")
    require(number(result.get("records_declared"), "declared") == N and number(result.get("source_rows"), "rows") == end - start, "R2-2-4 row count")
    p1 = number(result.get("p1_uses"), "p1")
    p2 = number(result.get("p2_uses"), "p2")
    piv20 = number(result.get("pivotable_K20_children"), "piv20")
    p3 = number(result.get("p3_uses"), "p3")
    require(number(result.get("K18_children"), "K18") == 12 * p1, "R2-2-4 K18 identity")
    require(number(result.get("K20_children"), "K20") == 12 * p2, "R2-2-4 K20 identity")
    terminal = number(result.get("K24_terminal_occurrences"), "terminal")
    require(terminal == 60 * p3 == number(result.get("full_occurrences"), "full") == number(result.get("irreducible_occurrences"), "irreducible"), "R2-2-4 terminal identity")
    require(number(result.get("full_charge_scaled_U"), "charge") == number(result.get("irreducible_charge_scaled_U"), "irreducible charge"), "R2-2-4 charge identity")
    hist = result.get("m1_m2_m3_hist")
    require(isinstance(hist, dict) and sum(map(int, hist.values())) == piv20, "R2-2-4 hist count")
    weighted = 0
    for key, value in hist.items():
        factors = key.split("_")
        require(len(factors) == 3 and all(int(x) > 0 for x in factors), "R2-2-4 hist key")
        m1, m2, m3 = map(int, factors)
        require(U % (m1 * m2 * m3) == 0, "R2-2-4 histogram denominator outside U")
        weighted += m3 * number(value, "hist value")
    require(weighted == p3, "R2-2-4 hist/p3 identity")
    cache = result.get("terminal_cache")
    require(number(cache.get("hits"), "hits") + number(cache.get("misses"), "misses") == p3, "R2-2-4 cache identity")
    require(result.get("packet_grouping_guard") == PACKET_GUARD and result.get("sign_rule") == SIGN_RULE and result.get("terminality") == TERMINALITY, "R2-2-4 provenance/sign/terminality")
    require(Path(result.get("sample_ledger", "")).name == samples_path.name, "R2-2-4 sample path")
    rows = load_samples(samples_path)
    require(number(result.get("literal_samples"), "sample count") == len(rows) and rows, "R2-2-4 sample count")
    bins = set()
    for line_no, row in enumerate(rows, 2):
        slot = number(row["sample_ordinal"], f"sample {line_no} slot")
        index = number(row["record_index"], f"sample {line_no} index")
        require(start <= index < end and slot == min(256, index * 257 // N), f"sample {line_no} interval/bin")
        require(slot not in bins, f"sample {line_no} duplicate bin")
        bins.add(slot)
        require(len(row["source_row"]) == len(row["K18_row"]) == len(row["K20_row"]) == 48, f"sample {line_no} row length")
        int(row["source_row"] + row["K18_row"] + row["K20_row"], 16)
        m1, m2, m3 = (number(row[x], f"sample {line_no} {x}") for x in ("m1", "m2", "m3"))
        require(number(row["unit_scaled_U"], "sample unit") == -U // (m1 * m2 * m3) and U % (m1 * m2 * m3) == 0, f"sample {line_no} sign/unit")
        require(number(row["terminal_q"], "sample q") != 0 and number(row["nonzero_contribution_scaled_U"], "sample contribution") != 0, f"sample {line_no} zero witness")
        require(number(row["final_degree"], "sample degree") == 4, f"sample {line_no} degree")
    return {"result": result, "samples": rows, "bins": sorted(bins), "result_sha256": sha256(result_path), "samples_sha256": sha256(samples_path)}


def merge(first_result: Path, first_samples: Path, second_result: Path, second_samples: Path,
          merged_result_path: Path, merged_samples_path: Path, report_path: Path) -> dict:
    shards = [validate_shard(first_result, first_samples, 0, MID), validate_shard(second_result, second_samples, MID, N)]
    totals = {field: sum(number(shard["result"].get(field), field) for shard in shards) for field in SUM_FIELDS}
    pins = {
        "source_rows": N, "signed_source_coefficient": 1_464_625_152,
        "l1_source_coefficient": 13_978_655_136, "pivotable_K16_rows": 24_003_767,
        "p1_uses": 129_939_187, "K18_children": 1_559_270_244,
        "pivotable_K18_children": 807_499_618, "p2_uses": 2_049_974_172,
        "K20_children": 24_599_690_064, "pivotable_K20_children": 2_745_607_644,
        "p3_uses": 2_745_607_644,
    }
    require(all(totals[key] == value for key, value in pins.items()), "R2-2-4 merged source/global count pin")
    require(totals["K24_terminal_occurrences"] == 60 * totals["p3_uses"] == totals["full_occurrences"] == totals["irreducible_occurrences"], "R2-2-4 merged terminal identity")
    require(totals["full_charge_scaled_U"] == totals["irreducible_charge_scaled_U"], "R2-2-4 merged charge identity")
    merged_hist = Counter()
    for shard in shards:
        merged_hist.update({key: number(value, "hist value") for key, value in shard["result"]["m1_m2_m3_hist"].items()})
    by_bin = {}
    for shard in shards:
        for row in shard["samples"]:
            slot = number(row["sample_ordinal"], "sample slot")
            if slot not in by_bin or number(row["record_index"], "index") < number(by_bin[slot]["record_index"], "index"):
                by_bin[slot] = row
    require(set(by_bin) == set(range(257)), "R2-2-4 merged samples do not cover all global bins")
    with merged_samples_path.with_suffix(merged_samples_path.suffix + ".tmp").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(by_bin[x] for x in range(257))
    merged_samples_path.with_suffix(merged_samples_path.suffix + ".tmp").replace(merged_samples_path)
    cache = {
        "hits": sum(number(s["result"]["terminal_cache"]["hits"], "hits") for s in shards),
        "misses": sum(number(s["result"]["terminal_cache"]["misses"], "misses") for s in shards),
        "peak_keys_per_piece": max(number(s["result"]["terminal_cache"]["peak_keys_per_piece"], "peak") for s in shards),
    }
    result = {
        "status": "PASS_COMPLETE_GROUPED_SIX_D16_R_2_2_4_K24_CHARGE_ONLY",
        "group_id": "source_D16_R2_2_4", "degree": 24, "scale_U": str(U),
        "ids": IDS, "covered_ids": 6, "individual_id_charges": None,
        "record_interval": [0, N], "records_declared": N, "distributed_prefix": False,
        **{key: str(value) if key in {"signed_source_coefficient", "l1_source_coefficient", "full_charge_scaled_U", "irreducible_charge_scaled_U"} else value for key, value in totals.items()},
        "m1_m2_m3_hist": dict(sorted(merged_hist.items())), "terminal_cache": cache,
        "literal_samples": 257, "sample_ledger": str(merged_samples_path),
        "packet_grouping_guard": PACKET_GUARD, "sign_rule": SIGN_RULE, "terminality": TERMINALITY,
        "scope": "strict grouped six-ID K24 R2-2-4 charge-only sink; no individual reconstruction, other sink, rows/columns, or membership claim",
    }
    temp_result = merged_result_path.with_suffix(merged_result_path.suffix + ".tmp")
    temp_result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temp_result.replace(merged_result_path)
    report = {
        "status": "PASS_COMPLETE_K24_K16_R224_TWO_HALF_MERGE_STRUCTURE",
        "intervals": [[0, MID], [MID, N]], "no_gap_no_overlap": True,
        "strict_ids": IDS, "covered_ids": 6, "grouped_scalar_once": True,
        "shard_result_sha256": [s["result_sha256"] for s in shards],
        "shard_samples_sha256": [s["samples_sha256"] for s in shards],
        "merged_result_sha256": sha256(merged_result_path),
        "merged_samples_sha256": sha256(merged_samples_path), "witnesses": 257,
        "charge_scaled_U": str(totals["full_charge_scaled_U"]),
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    shard = sub.add_parser("shard")
    shard.add_argument("--result", type=Path, required=True); shard.add_argument("--samples", type=Path, required=True)
    shard.add_argument("--start", type=int, required=True); shard.add_argument("--end", type=int, required=True); shard.add_argument("--output", type=Path, required=True)
    full = sub.add_parser("merge")
    full.add_argument("--first-result", type=Path, required=True); full.add_argument("--first-samples", type=Path, required=True)
    full.add_argument("--second-result", type=Path, required=True); full.add_argument("--second-samples", type=Path, required=True)
    full.add_argument("--merged-result", type=Path, required=True); full.add_argument("--merged-samples", type=Path, required=True); full.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "shard":
        checked = validate_shard(args.result, args.samples, args.start, args.end)
        report = {"status": "PASS_K24_K16_R224_HALF_STRUCTURE", "interval": [args.start, args.end], "result_sha256": checked["result_sha256"], "samples_sha256": checked["samples_sha256"], "sample_bins": checked["bins"]}
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    else:
        report = merge(args.first_result, args.first_samples, args.second_result, args.second_samples, args.merged_result, args.merged_samples, args.output)
    print(json.dumps({"status": report["status"]}))


if __name__ == "__main__":
    main()

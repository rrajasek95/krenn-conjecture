#!/usr/bin/env python3
"""Fail-closed validator and two-half merger for the two grouped K15 K24 sinks."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

TOTAL = 485
MID = 242
U = 400_591_699_200
HEADS_PER_SLICE = 13_824
SOURCE_SHA = "594701a258a9b9be9b6ec4516ba683eb758b3c4c026ce66b982899d17b2596c9"
BINARY_SHA = "230918d02643e1cdc87c6de3e2f0d4a89ac37099a8449d42d8a3e6b063639b57"
LITERAL_REFEREE_SHA = "e9a79c20293bfaee79b1b421de95444e896ec5be93e8d0719856c5d1d7539b96"
STATUS_GATE = "PASS_BOUNDED_GROUPED_DIRECT_K15_TWO_SINK_K24_GATE"
STATUS_FULL = "PASS_COMPLETE_GROUPED_DIRECT_K15_TWO_SINK_K24_CHARGE"
SCHEMA = "k24_physical_literal_v2_source_head"
PACKET_GUARD = "packet witnesses 322/232/223 retained only as grouped source classes; no individual scalar split"
SIGN_RULE = "direct K15 head is -positive; every selected pivot flips sign and divides by its occurrencewise multiplicity; U is exactly divisible by every recorded denominator product"
TERMINALITY = "every realized final K4 response key is exhaustively expanded; all K24 outputs have anchor-signature mass zero, so full equals irreducible"
SCOPE = "two separate grouped scalar K24 sinks covering exactly 6 IDs; charge only, no rows, columns, membership, span, or conjecture verdict"
HEADER = [
    "sample_bin", "source_index", "group_id", "lineage_scope",
    "source_head_ordinal", "source_head_row", "source_coefficient",
    "denominator_product", "unit_scaled_U", "terminal_K4_charge",
    "contribution_scaled_U", "literal_steps",
]
SINKS = {
    "D15:{223,232,322}|R:2-3-4": {
        "group_id": "source_D15_R2_3_4",
        "ids": [f"D15:{packet}|R:2-3-4" for packet in ("223", "232", "322")],
        "degrees": [2, 3, 4],
    },
    "D15:{223,232,322}|R:3-2-4": {
        "group_id": "source_D15_R3_2_4",
        "ids": [f"D15:{packet}|R:3-2-4" for packet in ("223", "232", "322")],
        "degrees": [3, 2, 4],
    },
}
GLOBAL_SOURCE_PINS = {
    "source_heads": 6_704_640,
    "source_mass": 322_486_272,
    "source_l1": 3_085_516_800,
}
SUM_SCALARS = [
    "source_heads", "source_mass", "source_l1",
    "terminal_response_keys_evaluated", "terminal_K24_occurrences",
    "full_occurrences", "irreducible_occurrences",
    "full_charge_scaled_U", "irreducible_charge_scaled_U",
]
SUM_VECTORS = {
    "stage_pivot_uses": 3,
    "stage_tail_candidates": 3,
    "stage_pivotable_children": 2,
}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def number(value, name: str) -> int:
    require(not isinstance(value, bool), f"{name}: bool is not an integer")
    try:
        return int(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{name}: bad integer {value!r}") from exc


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_bins(start: int, end: int) -> set[int]:
    return {min(256, source_index * 257 // TOTAL) for source_index in range(start, end)}


def load_samples(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        require(reader.fieldnames == HEADER, "K15 sample header/schema")
        rows = list(reader)
    require(all(set(row) == set(HEADER) for row in rows), "K15 ragged sample row")
    return rows


def validate_sample(row: dict[str, str], start: int, end: int, line_no: int) -> tuple[str, int, int]:
    slot = number(row["sample_bin"], f"sample {line_no} bin")
    source_index = number(row["source_index"], f"sample {line_no} source index")
    require(start <= source_index < end, f"sample {line_no} source outside shard")
    require(slot == min(256, source_index * 257 // TOTAL), f"sample {line_no} distributed bin")
    by_group = {spec["group_id"]: spec for spec in SINKS.values()}
    require(row["group_id"] in by_group, f"sample {line_no} foreign group")
    spec = by_group[row["group_id"]]
    require(row["lineage_scope"] == "+".join(spec["ids"]), f"sample {line_no} lineage scope")
    ordinal = number(row["source_head_ordinal"], f"sample {line_no} head ordinal")
    require(0 <= ordinal < HEADS_PER_SLICE, f"sample {line_no} head ordinal range")
    require(len(row["source_head_row"]) == 48, f"sample {line_no} row length")
    try:
        bytes.fromhex(row["source_head_row"])
    except ValueError as exc:
        raise ValueError(f"sample {line_no} row hex") from exc
    coefficient = number(row["source_coefficient"], f"sample {line_no} coefficient")
    denominator = number(row["denominator_product"], f"sample {line_no} denominator")
    unit = number(row["unit_scaled_U"], f"sample {line_no} unit")
    terminal_q = number(row["terminal_K4_charge"], f"sample {line_no} terminal q")
    contribution = number(row["contribution_scaled_U"], f"sample {line_no} contribution")
    require(coefficient != 0 and denominator > 0 and U % denominator == 0, f"sample {line_no} coefficient/denominator")
    require(unit == -coefficient * U // denominator, f"sample {line_no} K15 sign/U")
    require(terminal_q != 0 and contribution == unit * terminal_q, f"sample {line_no} nonzero contribution")
    steps = row["literal_steps"].split(";")
    require(len(steps) == 3, f"sample {line_no} literal step count")
    for depth, (step, degree) in enumerate(zip(steps, spec["degrees"])):
        fields = step.split(":")
        require(len(fields) == 4, f"sample {line_no} step {depth} arity")
        pivot = number(fields[0], f"sample {line_no} step {depth} pivot")
        require(0 <= pivot < 77 and number(fields[2], "step degree") == degree, f"sample {line_no} step {depth} pivot/degree")
        require((depth == 2 and fields[1] == "-") or (depth < 2 and number(fields[1], "tail") >= 0), f"sample {line_no} step {depth} tail marker")
        require(len(fields[3]) == 48, f"sample {line_no} step {depth} row length")
        try:
            bytes.fromhex(fields[3])
        except ValueError as exc:
            raise ValueError(f"sample {line_no} step {depth} row hex") from exc
    return row["group_id"], slot, source_index


def validate_shard(result_path: Path, samples_path: Path, start: int, end: int, frozen_half: bool) -> dict:
    require(0 <= start < end <= TOTAL, "K15 interval range")
    if frozen_half:
        require((start, end) in {(0, MID), (MID, TOTAL)}, "K15 interval is not a frozen half")
    result = json.loads(result_path.read_text())
    require(result.get("status") == STATUS_GATE, "K15 shard status")
    require(number(result.get("scale_U"), "K15 U") == U and number(result.get("degree"), "degree") == 24, "K15 degree/U")
    require(result.get("slice_interval") == [start, end], "K15 interval")
    require(number(result.get("source_slices"), "source slices") == end - start, "K15 source-slice count")
    require(number(result.get("source_heads_per_slice"), "heads per slice") == HEADS_PER_SLICE, "K15 heads-per-slice")
    require(number(result.get("workers"), "workers") == 8, "K15 frozen worker count")
    require(number(result.get("covered_ids"), "covered IDs") == 6 and number(result.get("scalar_groups"), "groups") == 2, "K15 coverage/group count")
    require(result.get("sample_schema") == SCHEMA and Path(result.get("sample_ledger", "")).name == samples_path.name, "K15 sample metadata")
    require(result.get("packet_grouping_guard") == PACKET_GUARD and result.get("sign_rule") == SIGN_RULE, "K15 grouping/sign provenance")
    require(result.get("terminality") == TERMINALITY and result.get("scope") == SCOPE, "K15 terminality/scope")
    require(set(result.get("sinks", {})) == set(SINKS), "K15 exact sink set")
    expected = expected_bins(start, end)
    source_pair = None
    sink_checks = {}
    for name, spec in SINKS.items():
        sink = result["sinks"][name]
        require(sink.get("ids") == spec["ids"] and sink.get("degrees") == spec["degrees"], f"{name}: exact IDs/path")
        require(sink.get("individual_id_charges") is None, f"{name}: grouped scalar must not be split")
        require(number(sink.get("source_heads"), f"{name} heads") == (end - start) * HEADS_PER_SLICE, f"{name}: source heads")
        pair = (number(sink.get("source_mass"), f"{name} mass"), number(sink.get("source_l1"), f"{name} l1"))
        require(pair[1] >= abs(pair[0]), f"{name}: source L1")
        require(source_pair is None or source_pair == pair, f"{name}: two sinks do not share exact source fold")
        source_pair = pair
        vectors = {}
        for field, length in SUM_VECTORS.items():
            vector = sink.get(field)
            require(isinstance(vector, list) and len(vector) == length, f"{name}: {field} length")
            vectors[field] = [number(value, f"{name} {field}") for value in vector]
            require(all(value >= 0 for value in vectors[field]), f"{name}: negative {field}")
        require(all(value > 0 for value in vectors["stage_pivot_uses"]), f"{name}: empty pivot stage")
        terminal = number(sink.get("terminal_K24_occurrences"), f"{name} terminal")
        full = number(sink.get("full_occurrences"), f"{name} full")
        irreducible = number(sink.get("irreducible_occurrences"), f"{name} irreducible")
        require(terminal == vectors["stage_tail_candidates"][2] == full == irreducible, f"{name}: terminal/full/irreducible identity")
        charge = number(sink.get("full_charge_scaled_U"), f"{name} charge")
        require(charge == number(sink.get("irreducible_charge_scaled_U"), f"{name} irreducible charge"), f"{name}: charge identity")
        keys = number(sink.get("terminal_response_keys_evaluated"), f"{name} response keys")
        require(0 < keys <= vectors["stage_pivot_uses"][2], f"{name}: terminal key bound")
        hist = sink.get("denominator_product_hist")
        require(isinstance(hist, dict) and hist, f"{name}: denominator histogram")
        hist_count = 0
        for raw_key, raw_value in hist.items():
            denominator = number(raw_key, f"{name} denominator key")
            value = number(raw_value, f"{name} denominator value")
            require(denominator > 0 and U % denominator == 0 and value > 0, f"{name}: denominator histogram entry")
            hist_count += value
        require(hist_count == vectors["stage_pivot_uses"][2], f"{name}: histogram/final-pivot identity")
        require(number(sink.get("literal_witnesses"), f"{name} witnesses") == len(expected), f"{name}: one witness per realized global bin")
        sink_checks[name] = {"vectors": vectors, "charge": charge, "hist_count": hist_count}
    rows = load_samples(samples_path)
    seen: dict[str, set[int]] = {spec["group_id"]: set() for spec in SINKS.values()}
    for line_no, row in enumerate(rows, 2):
        group, slot, _ = validate_sample(row, start, end, line_no)
        require(slot not in seen[group], f"sample {line_no}: duplicate group/bin")
        seen[group].add(slot)
    require(all(bins == expected for bins in seen.values()), "K15 sample ledger lacks exact per-group realized-bin support")
    require(len(rows) == 2 * len(expected), "K15 sample total")
    return {
        "result": result,
        "samples": rows,
        "bins_by_group": {group: sorted(bins) for group, bins in seen.items()},
        "result_sha256": sha256(result_path),
        "samples_sha256": sha256(samples_path),
        "source_pair": source_pair,
        "sink_checks": sink_checks,
    }


def validate_provenance(path: Path, shard: dict, shard_number: int, start: int, end: int) -> dict:
    provenance = json.loads(path.read_text())
    require(provenance.get("status") == "PASS_FROZEN_K24_K15_HALF_PRODUCTION_AND_INDEPENDENT_REPLAY", "K15 provenance status")
    require(number(provenance.get("shard"), "provenance shard") == shard_number and provenance.get("slice_interval") == [start, end], "K15 provenance interval")
    require(provenance.get("source_sha256") == SOURCE_SHA and provenance.get("binary_sha256") == BINARY_SHA, "K15 provenance producer pins")
    require(provenance.get("literal_referee_sha256") == LITERAL_REFEREE_SHA, "K15 provenance literal-referee pin")
    require(number(provenance.get("workers"), "provenance workers") == 8 and provenance.get("grouped_scalar_once") is True, "K15 provenance execution/group guard")
    require(provenance.get("result_sha256") == shard["result_sha256"] and provenance.get("samples_sha256") == shard["samples_sha256"], "K15 provenance result/sample hashes")
    require(number(provenance.get("literal_witnesses_replayed"), "provenance witnesses") == len(shard["samples"]), "K15 provenance replay count")
    return provenance


def write_atomic(path: Path, text: str) -> None:
    temp = Path(str(path) + ".tmp")
    temp.write_text(text)
    temp.replace(path)


def merge(args: argparse.Namespace) -> dict:
    targets = [args.merged_result, args.merged_samples, args.literal_report, args.fragment, args.output]
    require(all(not target.exists() for target in targets), "K15 merger refuses to overwrite an output")
    require(args.literal_referee.is_file() and sha256(args.literal_referee) == LITERAL_REFEREE_SHA, "K15 merger literal-referee binary pin")
    first = validate_shard(args.first_result, args.first_samples, 0, MID, True)
    second = validate_shard(args.second_result, args.second_samples, MID, TOTAL, True)
    provenances = [
        validate_provenance(args.first_provenance, first, 0, 0, MID),
        validate_provenance(args.second_provenance, second, 1, MID, TOTAL),
    ]
    shards = [first, second]
    merged_sinks = {}
    rows_by_group_bin: dict[tuple[str, int], dict[str, str]] = {}
    for shard in shards:
        for row in shard["samples"]:
            key = (row["group_id"], number(row["sample_bin"], "merged bin"))
            require(key not in rows_by_group_bin, "K15 half ledgers overlap in group/bin")
            rows_by_group_bin[key] = row
    expected_keys = {(spec["group_id"], slot) for spec in SINKS.values() for slot in range(257)}
    require(set(rows_by_group_bin) == expected_keys, "K15 merged ledger is not exact 257-bin coverage per group")
    for name, spec in SINKS.items():
        parts = [shard["result"]["sinks"][name] for shard in shards]
        merged = {
            "ids": spec["ids"], "individual_id_charges": None, "degrees": spec["degrees"],
        }
        for field in SUM_SCALARS:
            total = sum(number(part.get(field), f"{name} {field}") for part in parts)
            merged[field] = str(total) if field in {"source_mass", "source_l1", "full_charge_scaled_U", "irreducible_charge_scaled_U"} else total
        for field, length in SUM_VECTORS.items():
            merged[field] = [sum(number(part[field][index], f"{name} {field}") for part in parts) for index in range(length)]
        hist = Counter()
        for part in parts:
            hist.update({key: number(value, "hist value") for key, value in part["denominator_product_hist"].items()})
        merged["denominator_product_hist"] = dict(sorted(hist.items(), key=lambda item: int(item[0])))
        merged["literal_witnesses"] = 257
        require(all(number(merged[key], key) == value for key, value in GLOBAL_SOURCE_PINS.items()), f"{name}: merged global source pins")
        require(number(merged["terminal_K24_occurrences"], "terminal") == merged["stage_tail_candidates"][2] == number(merged["full_occurrences"], "full") == number(merged["irreducible_occurrences"], "irreducible"), f"{name}: merged terminal identity")
        require(number(merged["full_charge_scaled_U"], "charge") == number(merged["irreducible_charge_scaled_U"], "irreducible charge"), f"{name}: merged charge identity")
        require(sum(map(int, merged["denominator_product_hist"].values())) == merged["stage_pivot_uses"][2], f"{name}: merged histogram identity")
        merged_sinks[name] = merged
    sample_temp = Path(str(args.merged_samples) + ".tmp")
    with sample_temp.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=HEADER, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for spec in SINKS.values():
            for slot in range(257):
                writer.writerow(rows_by_group_bin[(spec["group_id"], slot)])
    merged_result = {
        "status": STATUS_FULL, "scale_U": str(U), "slice_interval": [0, TOTAL],
        "source_slices": TOTAL, "source_heads_per_slice": HEADS_PER_SLICE,
        "workers": 8, "degree": 24, "covered_ids": 6, "scalar_groups": 2,
        "sample_schema": SCHEMA, "sample_ledger": str(args.merged_samples),
        "sinks": merged_sinks, "packet_grouping_guard": PACKET_GUARD,
        "sign_rule": SIGN_RULE, "terminality": TERMINALITY, "scope": SCOPE,
        "source_intervals": [[0, MID], [MID, TOTAL]],
        "grouped_scalar_once": True,
    }
    result_temp = Path(str(args.merged_result) + ".tmp")
    result_temp.write_text(json.dumps(merged_result, indent=2, sort_keys=True) + "\n")
    literal_temp = Path(str(args.literal_report) + ".tmp")
    replay = subprocess.run(
        [str(args.literal_referee), "--family", "k15", "--samples", str(sample_temp), "--output", str(literal_temp)],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    require(replay.returncode == 0, f"K15 independent merged literal replay failed: {replay.stderr}")
    literal = json.loads(literal_temp.read_text())
    require(literal.get("status") == "PASS_INDEPENDENT_K24_LITERAL_REPLAY" and literal.get("family") == "k15", "K15 literal report status/family")
    require(number(literal.get("witnesses_replayed"), "merged witnesses") == 514 and number(literal.get("distinct_group_bins"), "merged bins") == 514, "K15 independent 257-per-group replay")
    sample_temp.replace(args.merged_samples)
    result_temp.replace(args.merged_result)
    literal_temp.replace(args.literal_report)
    fragment = {
        "status": "PASS_COMPLETE_STRICT_GROUPED_K15_SIX_ID_K24_CHARGE_FRAGMENT",
        "degree": 24, "scale_U": str(U), "covered_ids": 6, "scalar_groups": 2,
        "strict_id_set": sorted(item for spec in SINKS.values() for item in spec["ids"]),
        "groups": {
            spec["group_id"]: {
                "ids": spec["ids"], "grouped_scalar_once": True,
                "charge_scaled_U": merged_sinks[name]["full_charge_scaled_U"],
                "full_occurrences": merged_sinks[name]["full_occurrences"],
                "irreducible_occurrences": merged_sinks[name]["irreducible_occurrences"],
            }
            for name, spec in SINKS.items()
        },
        "complete_k24_claim": False,
        "scope": "exactly the two grouped K15 K24 scalar sinks; no individual-ID split and no other K24 family",
        "merged_result_sha256": sha256(args.merged_result),
        "merged_samples_sha256": sha256(args.merged_samples),
        "literal_referee_sha256": sha256(args.literal_report),
    }
    write_atomic(args.fragment, json.dumps(fragment, indent=2, sort_keys=True) + "\n")
    report = {
        "status": "PASS_COMPLETE_K24_K15_TWO_HALF_MERGE_AND_514_LITERAL_REFEREE",
        "intervals": [[0, MID], [MID, TOTAL]], "no_gap": True, "no_overlap": True,
        "source_slices": TOTAL, "source_heads_per_group": GLOBAL_SOURCE_PINS["source_heads"],
        "strict_id_set": fragment["strict_id_set"], "covered_ids": 6,
        "scalar_groups": 2, "grouped_scalar_once": True,
        "shard_result_sha256": [shard["result_sha256"] for shard in shards],
        "shard_samples_sha256": [shard["samples_sha256"] for shard in shards],
        "provenance_sha256": [sha256(args.first_provenance), sha256(args.second_provenance)],
        "merged_result_sha256": fragment["merged_result_sha256"],
        "merged_samples_sha256": fragment["merged_samples_sha256"],
        "literal_referee_sha256": fragment["literal_referee_sha256"],
        "literal_witnesses_replayed": 514, "literal_bins_per_group": 257,
        "charge_scaled_U_by_group": {spec["group_id"]: merged_sinks[name]["full_charge_scaled_U"] for name, spec in SINKS.items()},
        "complete_k24_claim": False,
    }
    write_atomic(args.output, json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("control", "shard"):
        item = sub.add_parser(command)
        item.add_argument("--result", type=Path, required=True)
        item.add_argument("--samples", type=Path, required=True)
        item.add_argument("--start", type=int, required=True)
        item.add_argument("--end", type=int, required=True)
        item.add_argument("--output", type=Path, required=True)
    full = sub.add_parser("merge")
    full.add_argument("--first-result", type=Path, required=True)
    full.add_argument("--first-samples", type=Path, required=True)
    full.add_argument("--first-provenance", type=Path, required=True)
    full.add_argument("--second-result", type=Path, required=True)
    full.add_argument("--second-samples", type=Path, required=True)
    full.add_argument("--second-provenance", type=Path, required=True)
    full.add_argument("--literal-referee", type=Path, required=True)
    full.add_argument("--merged-result", type=Path, required=True)
    full.add_argument("--merged-samples", type=Path, required=True)
    full.add_argument("--literal-report", type=Path, required=True)
    full.add_argument("--fragment", type=Path, required=True)
    full.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command in {"control", "shard"}:
        checked = validate_shard(args.result, args.samples, args.start, args.end, args.command == "shard")
        report = {
            "status": "PASS_K24_K15_BOUNDED_CONTROL_STRUCTURE" if args.command == "control" else "PASS_K24_K15_FROZEN_HALF_STRUCTURE",
            "slice_interval": [args.start, args.end],
            "result_sha256": checked["result_sha256"],
            "samples_sha256": checked["samples_sha256"],
            "sample_bins_by_group": checked["bins_by_group"],
        }
        write_atomic(args.output, json.dumps(report, indent=2, sort_keys=True) + "\n")
    else:
        report = merge(args)
    print(json.dumps({"status": report["status"]}))


if __name__ == "__main__":
    main()

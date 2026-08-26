#!/usr/bin/env python3
"""Fail-closed structural validator/merger for scalar-only K24 charge shards.

This deliberately does not recompute a shard's scalar fold.  The companion
Rust referee independently replays every exported literal continuation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTRACT_PATH = HERE / "k24_charge_referee_contract.json"
U = 400_591_699_200
PHYSICAL = {"k14", "k15", "k16", "direct17"}
HIDDEN = {"hidden18", "hidden_pair"}
PHYSICAL_HEADER = [
    "sample_bin", "source_index", "group_id", "lineage_scope",
    "source_head_ordinal", "source_head_row", "source_coefficient",
    "denominator_product", "unit_scaled_U", "terminal_K4_charge",
    "contribution_scaled_U", "literal_steps",
]
HIDDEN_HEADER = [
    "sample_bin", "source_index", "group_id", "lineage_id",
    "retained_weight_scaled_U", "m_prev", "m_final",
    "preterminal_pivot", "preterminal_tail", "terminal_pivot",
    "unit_scaled_U", "terminal_K4_charge", "contribution_scaled_U",
    "K20_row",
]
FAST_K14_HEADER = [
    "lineage_id", "sample_bin", "head_index", "r8_index", "row14", "source_mass",
    "p1_uses", "first_children", "pivotable_first", "p2_uses", "second_children",
    "pivotable_second", "p3_uses", "K23_children", "charge_scaled_U", "witness_p1",
    "witness_t1", "witness_p2", "witness_t2", "witness_p3", "m1", "m2", "m3",
    "terminal_degree", "witness_terminal_q", "witness_row1", "witness_row2",
    "nonzero_terminal_q",
]
FAST_K16_R44_HEADER = [
    "sample_ordinal", "record_index", "coefficient", "source_row", "intermediate_row",
    "p1", "t1", "p2", "m1", "m2", "first_degree", "final_degree",
    "terminal_q", "unit_scaled_U", "nonzero_contribution_scaled_U",
]
FAST_K16_R44_CANDIDATE_HEADER = [
    "candidate_slot", "support_bin", "record_index", "coefficient", "source_row",
    "intermediate_row", "p1", "t1", "p2", "m1", "m2", "terminal_q",
    "unit_scaled_U", "nonzero_contribution_scaled_U", "final_degree",
]


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def number(value, name: str) -> int:
    require(not isinstance(value, bool), f"{name}: bool is not an integer")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}: invalid integer {value!r}") from exc


def load_contract() -> dict:
    c = json.loads(CONTRACT_PATH.read_text())
    require(number(c["scale_U"], "contract scale") == U, "contract U mismatch")
    dag_path = HERE.parents[1] / c["dag_contract"]["path"]
    require(sha256(dag_path) == c["dag_contract"]["sha256"], "DAG contract hash mismatch")
    dag = json.loads(dag_path.read_text())
    engine_path = HERE.parents[1] / c["literal_engine"]["path"]
    require(sha256(engine_path) == c["literal_engine"]["sha256"], "literal engine hash mismatch")
    for name, pin in c["producer_sources"].items():
        source_path = HERE.parents[1] / pin["path"]
        require(sha256(source_path) == pin["sha256"], f"{name} producer source hash mismatch")
        if "binary_path" in pin:
            binary_path = HERE.parents[1] / pin["binary_path"]
            require(sha256(binary_path) == pin["binary_sha256"], f"{name} producer binary hash mismatch")
    support = c["k16_r44_support"]
    support_path = HERE.parents[1] / support["candidate_ledger_path"]
    require(sha256(support_path) == support["candidate_ledger_sha256"], "K16 R4-4 support ledger hash mismatch")
    frozen = {gid: ids for f in c["families"].values() for gid, ids in f["groups"].items()}
    require(frozen == dag["groups"], "referee family partition differs from frozen DAG")
    require(len(frozen) == 10 and sum(map(len, frozen.values())) == 35, "DAG must be exactly 10 groups/35 IDs")
    return c


def load_samples(path: Path, expected_header: list[str]) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        require(reader.fieldnames == expected_header, f"sample schema mismatch: {reader.fieldnames}")
        rows = list(reader)
    require(all(set(r) == set(expected_header) for r in rows), "ragged sample row")
    return rows


def interval_from_result(result: dict, family: str) -> tuple[int, int]:
    key = "source_interval" if family in PHYSICAL else "input_interval"
    interval = result.get(key)
    require(isinstance(interval, list) and len(interval) == 2, f"bad {key}")
    return number(interval[0], key), number(interval[1], key)


def validate_samples(rows: list[dict[str, str]], family: str, start: int, end: int,
                     groups: dict[str, list[str]], total: int) -> dict:
    seen: set[tuple[str, int]] = set()
    bins: dict[str, set[int]] = defaultdict(set)
    for line_no, row in enumerate(rows, 2):
        gid = row["group_id"]
        require(gid in groups, f"sample {line_no}: wrong group {gid}")
        index = number(row["source_index"], f"sample {line_no} source_index")
        sample_bin = number(row["sample_bin"], f"sample {line_no} bin")
        require(start <= index < end, f"sample {line_no}: source outside shard")
        require(sample_bin == min(256, index * 257 // total), f"sample {line_no}: wrong distributed bin")
        require((gid, sample_bin) not in seen, f"sample {line_no}: duplicate group/bin")
        seen.add((gid, sample_bin))
        bins[gid].add(sample_bin)
        lineage_key = "lineage_scope" if family in PHYSICAL else "lineage_id"
        expected_lineage = "+".join(groups[gid])
        require(row[lineage_key] == expected_lineage, f"sample {line_no}: lineage scope mismatch")
        require(len(row["source_head_row"] if family in PHYSICAL else row["K20_row"]) == 48,
                f"sample {line_no}: row is not 24-byte hex")
        int(row["source_head_row"] if family in PHYSICAL else row["K20_row"], 16)
        unit = number(row["unit_scaled_U"], f"sample {line_no} unit")
        charge = number(row["terminal_K4_charge"], f"sample {line_no} K4 charge")
        contribution = number(row["contribution_scaled_U"], f"sample {line_no} contribution")
        require(unit * charge == contribution, f"sample {line_no}: contribution product mismatch")
        require(charge != 0, f"sample {line_no}: witness is zero")
        if family in PHYSICAL:
            denominator = number(row["denominator_product"], f"sample {line_no} denominator")
            require(denominator > 0 and U % denominator == 0, f"sample {line_no}: denominator does not divide U")
            require(number(row["source_head_ordinal"], f"sample {line_no} ordinal") >= 0,
                    f"sample {line_no}: negative ordinal")
            require(row["literal_steps"], f"sample {line_no}: missing literal steps")
        else:
            require(number(row["m_prev"], "m_prev") > 0 and number(row["m_final"], "m_final") > 0,
                    f"sample {line_no}: nonpositive pivot count")
    return {gid: sorted(v) for gid, v in bins.items()}


def validate_shard(result_path: Path, samples_path: Path, expected_family: str,
                   expected_start: int | None = None, expected_end: int | None = None) -> dict:
    contract = load_contract()
    require(expected_family in contract["families"], f"unknown family {expected_family}")
    spec = contract["families"][expected_family]
    result = json.loads(result_path.read_text())
    family = result.get("family")
    require(family == expected_family, f"family mismatch {family!r}")
    require(number(result.get("degree"), "degree") == 24, "degree must be 24")
    require(number(result.get("scale_U"), "scale_U") == U, "scale U mismatch")
    require(result.get("all_terminal_responses_exhaustive") is True, "terminality flag absent")
    require(result.get("full_equals_irreducible") is True, "full=irreducible flag absent")
    start, end = interval_from_result(result, family)
    total = number(spec["total_source_units"], "total source units")
    require(0 <= start < end <= total, "invalid shard interval")
    if expected_start is not None:
        require(start == expected_start, "unexpected shard start")
    if expected_end is not None:
        require(end == expected_end, "unexpected shard end")
    require(Path(result["literal_witness_ledger"]).name == samples_path.name,
            "result points to a different sample ledger")

    groups = spec["groups"]
    if family in PHYSICAL:
        require(result.get("status") == "PASS_BOUNDED_K24_CHARGE_ONLY_PHYSICAL", "bad physical status")
        require(result.get("sample_schema") == "k24_physical_literal_v2_source_head",
                "physical v1 witnesses are not independently replayable")
        require(result.get("distributed") is False, "distributed pseudo-interval is not shard-valid")
        entries = result.get("groups")
        require(isinstance(entries, list) and len(entries) == len(groups), "wrong physical group count")
        by_gid = {g.get("group_id"): g for g in entries}
        require(len(by_gid) == len(entries) and set(by_gid) == set(groups), "wrong/duplicate physical groups")
        for gid, ids in groups.items():
            g = by_gid[gid]
            require(g.get("ids") == ids, f"{gid}: ID scope mismatch")
            require(g.get("path") == spec["paths"][gid], f"{gid}: path mismatch")
            require(number(g.get("source_units"), "source_units") == end - start, f"{gid}: source count mismatch")
            piv = list(map(int, g.get("stage_pivot_uses", [])))
            tails = list(map(int, g.get("stage_tail_candidates", [])))
            require(len(piv) == 3 and len(tails) == 3, f"{gid}: malformed stage counts")
            last = len(spec["paths"][gid]) - 1
            terminal = number(g.get("terminal_K24_occurrences"), "terminal occurrences")
            require(terminal == tails[last], f"{gid}: final-tail/terminal mismatch")
            require(terminal == number(g.get("full_occurrences"), "full occurrences") == number(g.get("irreducible_occurrences"), "irreducible occurrences"), f"{gid}: terminality count mismatch")
            require(number(g.get("full_charge_scaled_U"), "full charge") == number(g.get("irreducible_charge_scaled_U"), "irreducible charge"), f"{gid}: charge mismatch")
            cache = g.get("terminal_cache", {})
            require(number(cache.get("hits"), "cache hits") + number(cache.get("misses"), "cache misses") == piv[last], f"{gid}: terminal cache identity fails")
            hist = g.get("denominator_product_hist", {})
            require(sum(number(v, "hist count") for v in hist.values()) == piv[last], f"{gid}: denominator histogram sum fails")
            require(all(number(k, "hist denominator") > 0 and U % number(k, "hist denominator") == 0 for k in hist), f"{gid}: denominator outside U")
            if family == "direct17":
                expected = spec["final_pivots_per_source"][gid] * (end - start)
                require(piv[last] == expected, f"{gid}: frozen final-pivot count mismatch")
        rows = load_samples(samples_path, PHYSICAL_HEADER)
        require(len(rows) == sum(number(g["literal_witnesses"], "literal_witnesses") for g in entries), "physical witness count mismatch")
    else:
        require(result.get("status") == "PASS_BOUNDED_K24_CHARGE_ONLY_HIDDEN", "bad hidden status")
        gid, ids = next(iter(groups.items()))
        require(result.get("group_id") == gid and result.get("ids") == ids, "hidden group/ID scope mismatch")
        require(result.get("input_sha256_expected") == spec["input_sha256"], "hidden input hash pin mismatch")
        require(result.get("sign_rule") == spec["sign_rule"], "hidden sign rule mismatch")
        records = number(result.get("input_records"), "input_records")
        require(records == end - start, "hidden input count mismatch")
        first_pivots = number(result.get("first_selected_pivots"), "first pivots")
        first_tails = number(result.get("first_tail_evaluations"), "first tails")
        expected_tail_factor = 12 if family == "hidden18" else 60
        require(first_tails == expected_tail_factor * first_pivots, "hidden first-tail identity fails")
        final_pivots = number(result.get("terminal_selected_pivots"), "terminal pivots")
        require(number(result.get("pivotable_K20_children"), "pivotable children") == final_pivots, "hidden pivotable/final mismatch")
        terminal = number(result.get("terminal_K24_occurrences"), "terminal occurrences")
        require(terminal == 60 * final_pivots, "hidden 60-tail identity fails")
        require(terminal == number(result.get("full_occurrences"), "full occurrences") == number(result.get("irreducible_occurrences"), "irreducible occurrences"), "hidden terminality count mismatch")
        require(number(result.get("full_charge_scaled_U"), "full charge") == number(result.get("irreducible_charge_scaled_U"), "irreducible charge"), "hidden charge mismatch")
        cache = result.get("terminal_cache", {})
        require(number(cache.get("hits"), "cache hits") + number(cache.get("misses"), "cache misses") == final_pivots, "hidden cache identity fails")
        require(sum(number(v, "hist count") for v in result.get("denominator_hist", {}).values()) == final_pivots, "hidden histogram identity fails")
        rows = load_samples(samples_path, HIDDEN_HEADER)
        require(len(rows) == number(result.get("literal_witnesses"), "literal_witnesses"), "hidden witness count mismatch")

    bins = validate_samples(rows, family, start, end, groups, total)
    return {
        "status": "PASS_K24_CHARGE_SHARD_STRUCTURE",
        "family": family,
        "interval": [start, end],
        "result_sha256": sha256(result_path),
        "samples_sha256": sha256(samples_path),
        "groups": groups,
        "sample_bins": bins,
        "sample_count": len(rows),
        "result": result,
        "sample_rows": rows,
    }


def merge_full(family: str, pairs: list[tuple[Path, Path]], output: Path) -> dict:
    contract = load_contract()
    require(family in contract["families"], "unknown family")
    checked = [validate_shard(r, s, family) for r, s in pairs]
    checked.sort(key=lambda x: x["interval"])
    total = contract["families"][family]["total_source_units"]
    cursor = 0
    for item in checked:
        require(item["interval"][0] == cursor, f"gap/overlap at {cursor}")
        cursor = item["interval"][1]
    require(cursor == total, f"incomplete family: stopped at {cursor}/{total}")
    groups = contract["families"][family]["groups"]
    samples: dict[tuple[str, int], dict[str, str]] = {}
    for item in checked:
        for row in item["sample_rows"]:
            key = (row["group_id"], int(row["sample_bin"]))
            old = samples.get(key)
            if old is None or int(row["source_index"]) < int(old["source_index"]):
                samples[key] = row
    for gid in groups:
        require({b for g, b in samples if g == gid} == set(range(257)), f"{gid}: not exactly 257 distributed nonzero bins")

    charges = Counter()
    terminal = Counter()
    for item in checked:
        r = item["result"]
        entries = r["groups"] if family in PHYSICAL else [r]
        for g in entries:
            gid = g["group_id"]
            charges[gid] += number(g["full_charge_scaled_U"], "charge")
            terminal[gid] += number(g["terminal_K24_occurrences"], "terminal")
    merged_samples = output.with_suffix(output.suffix + ".samples.tsv")
    header = PHYSICAL_HEADER if family in PHYSICAL else HIDDEN_HEADER
    with merged_samples.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for key in sorted(samples):
            writer.writerow(samples[key])
    fragment = {
        "status": "PASS_COMPLETE_K24_CHARGE_FAMILY_FRAGMENT",
        "degree": 24,
        "family": family,
        "scale_U": str(U),
        "full_source_interval": [0, total],
        "shards": [{k: item[k] for k in ("interval", "result_sha256", "samples_sha256")} for item in checked],
        "groups": [
            {"group_id": gid, "ids": ids, "terminal_K24_occurrences": terminal[gid],
             "full_charge_scaled_U": str(charges[gid]), "irreducible_charge_scaled_U": str(charges[gid]),
             "literal_witnesses": 257}
            for gid, ids in groups.items()
        ],
        "literal_witness_ledger": str(merged_samples),
        "literal_witness_ledger_sha256": sha256(merged_samples),
        "scope": "complete exact K24 charge family fragment only; no membership or K25 claim",
    }
    output.write_text(json.dumps(fragment, indent=2, sort_keys=True) + "\n")
    return fragment


def validate_fast_direct_full(result_path: Path) -> dict:
    """Validate the frozen fast [0,485) scalar run, explicitly without literals."""
    contract = load_contract()
    spec = contract["families"]["direct17"]
    result = json.loads(result_path.read_text())
    require(result.get("status") == "PASS_BOUNDED_K24_CHARGE_ONLY_DIRECT_D17_D18", "bad fast-direct status")
    require(number(result.get("degree"), "degree") == 24 and number(result.get("scale_U"), "scale_U") == U, "degree/U mismatch")
    require(result.get("source_interval") == [0, 485] and number(result.get("source_slices"), "source_slices") == 485, "not exact full 485-slice interval")
    require(number(result.get("covered_ids"), "covered_ids") == 13 and number(result.get("scalar_groups"), "scalar_groups") == 2, "top-level scope mismatch")
    require(result.get("column_or_row_output") is False, "unexpected row/column output claim")
    entries = result.get("groups")
    require(isinstance(entries, list) and len(entries) == 2, "wrong group count")
    by_gid = {g.get("group_id"): g for g in entries}
    require(len(by_gid) == 2 and set(by_gid) == set(spec["groups"]), "wrong/duplicate groups")
    per_source = {
        "source_D17_R3_4": {"heads": 171008, "p1": 551680, "mid": 17653760, "p2": 1736704},
        "source_D18_R2_4": {"heads": 313920, "p1": 537600, "mid": 6451200, "p2": 476160},
    }
    for gid, ids in spec["groups"].items():
        g = by_gid[gid]
        q = per_source[gid]
        require(g.get("ids") == ids, f"{gid}: ID set mismatch")
        require(number(g.get("source_heads"), "source_heads") == 485 * q["heads"], f"{gid}: source-head count mismatch")
        require(number(g.get("p1_uses"), "p1_uses") == 485 * q["p1"], f"{gid}: p1 count mismatch")
        require(number(g.get("intermediate_children"), "intermediate") == 485 * q["mid"], f"{gid}: intermediate count mismatch")
        p2 = number(g.get("p2_uses"), "p2_uses")
        require(p2 == 485 * q["p2"] == number(g.get("pivotable_intermediate_children"), "pivotable intermediate"), f"{gid}: p2 frozen count mismatch")
        terminal = number(g.get("K24_terminal_occurrences"), "terminal")
        require(terminal == 60 * p2 == number(g.get("full_occurrences"), "full") == number(g.get("irreducible_occurrences"), "irreducible"), f"{gid}: terminal count mismatch")
        require(number(g.get("full_charge_scaled_U"), "full charge") == number(g.get("irreducible_charge_scaled_U"), "irreducible charge"), f"{gid}: charge mismatch")
        hist = g.get("denominator_hist", {})
        require(sum(number(v, "hist") for v in hist.values()) == p2, f"{gid}: histogram count mismatch")
        for key in hist:
            parts = key.split("_")
            require(len(parts) == 2, f"{gid}: malformed denominator key")
            product = number(parts[0], "m1") * number(parts[1], "m2")
            require(product > 0 and U % product == 0, f"{gid}: denominator outside U")
    cache = result.get("cache", {})
    total_p1 = sum(number(g["p1_uses"], "p1") for g in entries)
    total_p2 = sum(number(g["p2_uses"], "p2") for g in entries)
    require(number(cache.get("literal_first_hits"), "first hits") + number(cache.get("literal_first_misses"), "first misses") == total_p1, "first-cache identity mismatch")
    require(number(cache.get("terminal_hits"), "terminal hits") + number(cache.get("terminal_misses"), "terminal misses") == total_p2, "terminal-cache identity mismatch")
    require(number(cache.get("terminality_assertions_on_realized_keys"), "terminality assertions") == 60 * number(cache.get("terminal_misses"), "terminal misses"), "terminality assertion identity mismatch")

    old_prefix = HERE.parents[1] / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_direct_d17_d18_prefix1.json"
    v2_prefix = HERE / "control_direct17_prefix1_v2.json"
    require(sha256(old_prefix) == "3ec4bdbf3b1e0b243875eebfd1f759c005dd095a853d76850cfab999385be06e", "fast prefix1 hash mismatch")
    old = {g["group_id"]: g for g in json.loads(old_prefix.read_text())["groups"]}
    v2 = {g["group_id"]: g for g in json.loads(v2_prefix.read_text())["groups"]}
    for gid in spec["groups"]:
        require(number(old[gid]["full_charge_scaled_U"], "old prefix charge") == number(v2[gid]["full_charge_scaled_U"], "v2 prefix charge"), f"{gid}: independent prefix charge mismatch")
        require(number(old[gid]["p2_uses"], "old prefix p2") == v2[gid]["stage_pivot_uses"][1], f"{gid}: independent prefix p2 mismatch")
        require(number(old[gid]["K24_terminal_occurrences"], "old prefix terminal") == number(v2[gid]["terminal_K24_occurrences"], "v2 prefix terminal"), f"{gid}: independent prefix terminal mismatch")
    return {
        "status": "PASS_K24_FAST_DIRECT_FULL_SCALAR_STRUCTURE_PENDING_LITERAL_LEDGER",
        "family": "direct17",
        "interval": [0, 485],
        "result_sha256": sha256(result_path),
        "groups": spec["groups"],
        "fast_source_sha256": contract["producer_sources"]["fast_direct17_charge_only"]["sha256"],
        "fast_binary_sha256": contract["producer_sources"]["fast_direct17_charge_only"]["binary_sha256"],
        "independent_v2_prefix_control": True,
        "production_literal_ledger_present": False,
        "acceptance": "scalar/count structure only until a separate distributed literal ledger is replayed",
    }


def validate_fast_k14_full(result_path: Path, samples_path: Path) -> dict:
    contract = load_contract()
    result = json.loads(result_path.read_text())
    ids = ["D14:222|R:3-3-4", "D14:222|R:4-2-4"]
    require(result.get("status") == "PASS_COMPLETE_D14_222_K24_CHARGE_ONLY", "bad fast K14 status")
    require(number(result.get("degree"), "degree") == 24 and number(result.get("scale_U"), "U") == U, "fast K14 degree/U mismatch")
    require(result.get("covered_lineage_ids") == ids, "fast K14 lineage scope mismatch")
    require(result.get("R8_record_interval") == [0, 485] and result.get("distributed_record_mode") is False, "fast K14 interval/mode mismatch")
    require(number(result.get("R8_records_consumed"), "records") == 485 == number(result.get("R8_records_declared"), "declared records"), "fast K14 record count mismatch")
    require(number(result.get("source_heads"), "source heads") == 838080, "fast K14 source-head count mismatch")
    require(number(result.get("source_mass_sum"), "source mass") == -40310784, "fast K14 independently derived source mass mismatch")
    require(number(result.get("source_mass_l1"), "source l1") == 385689600, "fast K14 independently derived source l1 mismatch")
    require(result.get("all_realized_cached_K24_responses_terminal") is True, "fast K14 terminality flag")
    expected_degrees = {ids[0]: (3, 3, 4), ids[1]: (4, 2, 4)}
    tail_count = {2: 12, 3: 32, 4: 60}
    sinks = result.get("sinks")
    require(isinstance(sinks, dict) and list(sinks) == ids, "fast K14 sink set/order mismatch")
    for lineage in ids:
        sink = sinks[lineage]
        degrees = tuple(number(sink.get(k), k) for k in ("first_response_degree", "second_response_degree", "terminal_response_degree"))
        require(degrees == expected_degrees[lineage], f"{lineage}: degree path mismatch")
        p1 = number(sink.get("selected_p1_uses"), "p1")
        p2 = number(sink.get("selected_p2_uses"), "p2")
        p3 = number(sink.get("selected_p3_uses"), "p3")
        require(number(sink.get("first_children"), "first children") == tail_count[degrees[0]] * p1, f"{lineage}: first-tail identity")
        require(number(sink.get("second_children"), "second children") == tail_count[degrees[1]] * p2, f"{lineage}: second-tail identity")
        terminal = number(sink.get("K24_terminal_occurrences", sink.get("K23_terminal_occurrences")), "terminal")
        require(terminal == 60 * p3 == number(sink.get("full_occurrences"), "full") == number(sink.get("irreducible_occurrences"), "irreducible"), f"{lineage}: terminal/full identity")
        require(number(sink.get("full_charge_scaled_U"), "full charge") == number(sink.get("irreducible_charge_scaled_U"), "irreducible charge"), f"{lineage}: full/irreducible charge")
        h1, h2, h3, hp = (sink[name] for name in ("first_denominator_hist", "second_denominator_hist", "third_denominator_hist", "product_denominator_hist"))
        require(sum(map(number, h1.values(), ["h1"] * len(h1))) == 838080, f"{lineage}: h1 sum")
        require(sum(number(v, "h2") for v in h2.values()) == number(sink.get("pivotable_first_children"), "pivotable first"), f"{lineage}: h2 sum")
        require(sum(number(k, "m2") * number(v, "h2") for k, v in h2.items()) == p2, f"{lineage}: h2 weighted sum")
        require(sum(number(v, "h3") for v in h3.values()) == number(sink.get("pivotable_second_children"), "pivotable second"), f"{lineage}: h3 sum")
        require(sum(number(k, "m3") * number(v, "h3") for k, v in h3.items()) == p3, f"{lineage}: h3 weighted sum")
        require(sum(number(v, "hp") for v in hp.values()) == number(sink.get("pivotable_second_children"), "pivotable second"), f"{lineage}: product histogram sum")
        require(all(number(k, "product denominator") > 0 and U % number(k, "product denominator") == 0 for k in hp), f"{lineage}: denominator outside U")
        plans = sink["plan_cache"]
        require(number(plans["first_hits"], "first hits") + number(plans["first_misses"], "first misses") == p1, f"{lineage}: first plan identity")
        require(number(plans["second_hits"], "second hits") + number(plans["second_misses"], "second misses") == p2, f"{lineage}: second plan identity")
        literal = sink["literal_preterminal_cache"]
        require(number(literal["hits"], "literal hits") + number(literal["misses"], "literal misses") == number(sink["pivotable_second_children"], "pivotable second"), f"{lineage}: literal cache identity")
        require(number(sink.get("literal_samples"), "literal samples") == 257, f"{lineage}: sample count")
    guard = result.get("literal_sample_guard", {})
    require(number(guard.get("records"), "sample records") == 514 and guard.get("records_per_sink") == [257, 257], "fast K14 sample guard counts")
    require(guard.get("all_literal_K24_children_terminal") is True and guard.get("all_abstract_literal_cycle_keys_equal") is True, "fast K14 literal flags")
    require(Path(guard.get("ledger", "")).name == samples_path.name, "fast K14 ledger path mismatch")
    require(result.get("sign_rule") == "direct D14 coefficient=-M; three normalized response flips give terminal +M/(m1*m2*m3), implemented as source_mass*U/(m1*m2*m3)", "fast K14 sign rule")
    rows = load_samples(samples_path, FAST_K14_HEADER)
    require(len(rows) == 514, "fast K14 ledger length")
    bins = defaultdict(set)
    for i, row in enumerate(rows, 2):
        lineage = row["lineage_id"]
        require(lineage in ids, f"fast K14 sample {i}: wrong lineage")
        head = number(row["head_index"], "head index")
        ri = number(row["r8_index"], "R8 index")
        b = number(row["sample_bin"], "sample bin")
        require(0 <= head < 838080 and head // 1728 == ri and b == head * 257 // 838080, f"fast K14 sample {i}: head/bin provenance")
        require(b not in bins[lineage], f"fast K14 sample {i}: duplicate bin")
        bins[lineage].add(b)
        require(row["nonzero_terminal_q"] in {"0", "1"} and (number(row["witness_terminal_q"], "q") != 0) == (row["nonzero_terminal_q"] == "1"), f"fast K14 sample {i}: nonzero flag")
    require(all(bins[x] == set(range(257)) for x in ids), "fast K14 ledger does not cover 257 bins per sink")
    return {
        "status": "PASS_COMPLETE_K24_FAST_K14_STRUCTURE",
        "family": "k14fast",
        "result_sha256": sha256(result_path),
        "samples_sha256": sha256(samples_path),
        "source_sha256": contract["producer_sources"]["fast_k14_charge_only"]["sha256"],
        "binary_sha256": contract["producer_sources"]["fast_k14_charge_only"]["binary_sha256"],
        "groups": ids,
        "witnesses": 514,
    }


def validate_fast_k16_r44_support_samples(samples_path: Path, contract: dict | None = None) -> dict:
    contract = contract or load_contract()
    support = contract["k16_r44_support"]
    candidate_path = HERE.parents[1] / support["candidate_ledger_path"]
    candidates = load_samples(candidate_path, FAST_K16_R44_CANDIDATE_HEADER)
    require(len(candidates) == 257, "K16 R4-4 frozen candidate count")
    candidate_by_slot = {}
    quotas = Counter()
    for i, candidate in enumerate(candidates, 2):
        slot = number(candidate["candidate_slot"], f"candidate {i} slot")
        support_bin = number(candidate["support_bin"], f"candidate {i} support bin")
        require(slot not in candidate_by_slot and 0 <= slot < 257, f"candidate {i}: duplicate/range")
        require(0 <= support_bin < 37, f"candidate {i}: support bin range")
        require(support_bin == min(256, number(candidate["record_index"], "candidate index") * 257 // 24097095), f"candidate {i}: support bin/index")
        require(number(candidate["terminal_q"], "candidate q") != 0 and number(candidate["nonzero_contribution_scaled_U"], "candidate contribution") != 0, f"candidate {i}: zero")
        candidate_by_slot[slot] = candidate
        quotas[support_bin] += 1
    require(set(candidate_by_slot) == set(range(257)), "K16 R4-4 candidate slots")
    require(quotas == Counter({**{x: 7 for x in range(35)}, 35: 6, 36: 6}), "K16 R4-4 support quota")
    rows = load_samples(samples_path, FAST_K16_R44_HEADER)
    require(len(rows) == 257, "K16 R4-4 sample count")
    slots = set()
    candidate_fields = {
        "record_index": "record_index", "coefficient": "coefficient",
        "source_row": "source_row", "intermediate_row": "intermediate_row",
        "p1": "p1", "t1": "t1", "p2": "p2", "m1": "m1", "m2": "m2",
        "final_degree": "final_degree", "terminal_q": "terminal_q",
        "unit_scaled_U": "unit_scaled_U",
        "nonzero_contribution_scaled_U": "nonzero_contribution_scaled_U",
    }
    for i, row in enumerate(rows, 2):
        slot = number(row["sample_ordinal"], "sample ordinal")
        require(slot in candidate_by_slot and slot not in slots, f"K16 R4-4 sample {i}: candidate slot")
        slots.add(slot)
        candidate = candidate_by_slot[slot]
        for actual_key, candidate_key in candidate_fields.items():
            require(row[actual_key] == candidate[candidate_key], f"K16 R4-4 sample {i}: candidate {actual_key}")
        require(row["first_degree"] == "4", f"K16 R4-4 sample {i}: first degree")
        require(number(row["terminal_q"], "terminal q") != 0 and number(row["nonzero_contribution_scaled_U"], "contribution") != 0, f"K16 R4-4 sample {i}: zero witness")
    require(slots == set(range(257)), "K16 R4-4 not exactly 257 frozen candidate slots")
    return {
        "status": "PASS_K24_FAST_K16_R44_FROZEN_SUPPORT_LEDGER",
        "family": "k16r44",
        "samples_sha256": sha256(samples_path),
        "witnesses": 257,
        "support_candidate_ledger_sha256": support["candidate_ledger_sha256"],
        "realized_support_bins": support["realized_support_bins"],
    }


def validate_fast_k16_r44_candidate_copy(candidate_copy: Path) -> dict:
    contract = load_contract()
    support = contract["k16_r44_support"]
    frozen_path = HERE.parents[1] / support["candidate_ledger_path"]
    frozen = load_samples(frozen_path, FAST_K16_R44_CANDIDATE_HEADER)
    supplied = load_samples(candidate_copy, FAST_K16_R44_CANDIDATE_HEADER)
    require(supplied == frozen, "K16 R4-4 supplied candidate ledger differs bytewise in parsed content")
    require(sha256(candidate_copy) == support["candidate_ledger_sha256"], "K16 R4-4 supplied candidate ledger hash")
    return {
        "status": "PASS_K24_FAST_K16_R44_FROZEN_CANDIDATES",
        "family": "k16r44candidates",
        "candidate_ledger_sha256": sha256(candidate_copy),
        "candidates": len(supplied),
    }


def validate_fast_k16_r44_full(result_path: Path, samples_path: Path) -> dict:
    contract = load_contract()
    result = json.loads(result_path.read_text())
    ids = contract["families"]["k16"]["groups"]["source_D16_R4_4"]
    require(result.get("status") == "PASS_COMPLETE_GROUPED_SIX_D16_K24_R44_CHARGE_ONLY", "bad K16 R4-4 status")
    require(result.get("group_id") == "source_D16_R4_4" and result.get("ids") == ids, "K16 R4-4 scope mismatch")
    require(number(result.get("degree"), "degree") == 24 and number(result.get("scale_U"), "U") == U, "K16 R4-4 degree/U")
    require(number(result.get("covered_ids"), "covered IDs") == 6 and result.get("individual_id_charges") is None, "K16 R4-4 grouped semantics")
    require(result.get("record_interval") == [0, 24097095] and result.get("distributed_prefix") is False, "K16 R4-4 interval/mode")
    require(number(result.get("records_declared"), "records declared") == 24097095 == number(result.get("source_rows"), "source rows"), "K16 R4-4 record count")
    require(number(result.get("signed_source_coefficient"), "source coefficient") == 1464625152, "K16 R4-4 source coefficient pin")
    require(number(result.get("l1_source_coefficient"), "source l1") == 13978655136, "K16 R4-4 source l1 pin")
    require(number(result.get("pivotable_K16_rows"), "pivotable rows") == 24003767, "K16 R4-4 pivotable-row pin")
    p1 = number(result.get("p1_uses"), "p1")
    require(p1 == 129939187 and number(result.get("first_children"), "first children") == 60 * p1, "K16 R4-4 p1/tail pin")
    pivmid = number(result.get("pivotable_intermediate_children"), "pivotable intermediate")
    p2 = number(result.get("p2_uses"), "p2")
    hist = result.get("m1_m2_hist", {})
    require(sum(number(v, "hist") for v in hist.values()) == pivmid, "K16 R4-4 hist count")
    weighted = 0
    for key, value in hist.items():
        parts = key.split("_")
        require(len(parts) == 2, "K16 R4-4 malformed histogram key")
        m1, m2 = map(int, parts)
        require(m1 > 0 and m2 > 0 and U % (m1 * m2) == 0, "K16 R4-4 denominator outside U")
        weighted += m2 * number(value, "hist")
    require(weighted == p2, "K16 R4-4 weighted histogram/p2")
    terminal = number(result.get("K24_terminal_occurrences"), "terminal")
    require(terminal == 60 * p2 == number(result.get("full_occurrences"), "full") == number(result.get("irreducible_occurrences"), "irreducible"), "K16 R4-4 terminal identity")
    require(number(result.get("full_charge_scaled_U"), "full charge") == number(result.get("irreducible_charge_scaled_U"), "irreducible charge"), "K16 R4-4 charge equality")
    cache = result.get("terminal_cache", {})
    require(number(cache.get("hits"), "hits") + number(cache.get("misses"), "misses") == p2, "K16 R4-4 cache identity")
    support_hist = result.get("nonzero_support_record_hist", {})
    require(isinstance(support_hist, dict) and set(map(int, support_hist)) == set(range(37)), "K16 R4-4 realized support histogram keys")
    require(all(number(value, "support histogram count") > 0 for value in support_hist.values()), "K16 R4-4 nonpositive support count")
    require(result.get("nonzero_support_bins") == list(range(37)), "K16 R4-4 realized support bin set")
    require(number(result.get("nonzero_support_records_outside_bins_0_36"), "outside support") == 0, "K16 R4-4 positive support outside bins 0..36")
    require(result.get("candidate_quota_by_support_bin") == {"0_through_34": 7, "35_through_36": 6}, "K16 R4-4 candidate quota histogram")
    require(number(result.get("literal_samples"), "literal samples") == 257 and Path(result.get("sample_ledger", "")).name == samples_path.name, "K16 R4-4 sample declaration")
    support = contract["k16_r44_support"]
    require(result.get("support_candidate_ledger") == support["candidate_ledger_path"], "K16 R4-4 support ledger path")
    require(result.get("support_candidate_ledger_sha256") == support["candidate_ledger_sha256"], "K16 R4-4 support ledger declared hash")
    require(result.get("support_rule") == support["rule"], "K16 R4-4 support rule")
    require(result.get("packet_grouping_guard") == "checkpoint retains collected canonical rows and coefficients but not packet labels; only the grouped six-ID scalar is source-faithful", "K16 R4-4 packet guard")
    require(result.get("sign_rule") == "stored v is the direct coefficient in P; two normalized response flips give +v/(m1*m2)", "K16 R4-4 sign rule")
    support_report = validate_fast_k16_r44_support_samples(samples_path, contract)
    return {
        "status": "PASS_COMPLETE_K24_FAST_K16_R44_STRUCTURE",
        "family": "k16r44",
        "result_sha256": sha256(result_path),
        "samples_sha256": sha256(samples_path),
        "source_sha256": contract["producer_sources"]["fast_k16_r44_charge_only"]["sha256"],
        "binary_sha256": contract["producer_sources"]["fast_k16_r44_charge_only"]["binary_sha256"],
        "input_sha256": contract["producer_sources"]["fast_k16_r44_charge_only"]["input_sha256"],
        "groups": ["source_D16_R4_4"],
        "witnesses": support_report["witnesses"],
        "support_candidate_ledger_sha256": support["candidate_ledger_sha256"],
        "realized_support_bins": support["realized_support_bins"],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    shard = sub.add_parser("shard")
    shard.add_argument("--family", required=True)
    shard.add_argument("--result", type=Path, required=True)
    shard.add_argument("--samples", type=Path, required=True)
    shard.add_argument("--start", type=int, required=True)
    shard.add_argument("--end", type=int, required=True)
    shard.add_argument("--output", type=Path, required=True)
    merge = sub.add_parser("merge")
    merge.add_argument("--family", required=True)
    merge.add_argument("--result", type=Path, action="append", required=True)
    merge.add_argument("--samples", type=Path, action="append", required=True)
    merge.add_argument("--output", type=Path, required=True)
    fast = sub.add_parser("fast-direct-full")
    fast.add_argument("--result", type=Path, required=True)
    fast.add_argument("--output", type=Path, required=True)
    fast_k14 = sub.add_parser("fast-k14-full")
    fast_k14.add_argument("--result", type=Path, required=True)
    fast_k14.add_argument("--samples", type=Path, required=True)
    fast_k14.add_argument("--output", type=Path, required=True)
    fast_k16_r44 = sub.add_parser("fast-k16-r44-full")
    fast_k16_r44.add_argument("--result", type=Path, required=True)
    fast_k16_r44.add_argument("--samples", type=Path, required=True)
    fast_k16_r44.add_argument("--output", type=Path, required=True)
    fast_k16_r44_support = sub.add_parser("fast-k16-r44-support-ledger")
    fast_k16_r44_support.add_argument("--samples", type=Path, required=True)
    fast_k16_r44_support.add_argument("--output", type=Path, required=True)
    fast_k16_r44_candidates = sub.add_parser("fast-k16-r44-candidates")
    fast_k16_r44_candidates.add_argument("--candidates", type=Path, required=True)
    fast_k16_r44_candidates.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.command == "shard":
        report = validate_shard(args.result, args.samples, args.family, args.start, args.end)
        report.pop("result")
        report.pop("sample_rows")
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    elif args.command == "merge":
        require(len(args.result) == len(args.samples), "result/sample arity mismatch")
        report = merge_full(args.family, list(zip(args.result, args.samples)), args.output)
    elif args.command == "fast-direct-full":
        report = validate_fast_direct_full(args.result)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    elif args.command == "fast-k14-full":
        report = validate_fast_k14_full(args.result, args.samples)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    elif args.command == "fast-k16-r44-full":
        report = validate_fast_k16_r44_full(args.result, args.samples)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    elif args.command == "fast-k16-r44-support-ledger":
        report = validate_fast_k16_r44_support_samples(args.samples)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    else:
        report = validate_fast_k16_r44_candidate_copy(args.candidates)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "family": report["family"]}, sort_keys=True))


if __name__ == "__main__":
    main()

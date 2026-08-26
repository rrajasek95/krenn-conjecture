#!/usr/bin/env python3
"""Seal the independent one-pass r1601->r1613 chain audit."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PLAN = json.loads((HERE / "AUDIT_PLAN.json").read_text())
PROD = ROOT / PLAN["production_root"]
REPLAY = json.loads((HERE / "results_round1613_single_pass_replay.json").read_text())
FINAL_SHA = json.loads((HERE / "results_final_large_sha256.json").read_text())


def need(value, message):
    if not value:
        raise SystemExit("REJECT: " + message)


def load(path):
    return json.loads(path.read_text())


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def arg(command, flag):
    need(command.count(flag) == 1, "command " + flag)
    return command[command.index(flag) + 1]


for name, key in (("cap_audit", "cap_audit_sha256"),
                  ("cap_manifest", "cap_manifest_sha256"),
                  ("compaction_record", "compaction_record_sha256")):
    need(sha(ROOT / PLAN["input"][name]) == PLAN["input"][key], key)
cap = load(ROOT / PLAN["input"]["cap_audit"])
need(cap["status"] == "PASS_EXACT_DIRECT_CAP3250_TO_CAP3500_EQUIVALENCE"
     and cap["accepted_candidate"] == "candidate_cap3500", "input cap status")
need(cap["checkpoint_sha256"] == PLAN["input"]["checkpoint_sha256"]
     and cap["vectors_sha256"] == PLAN["input"]["vectors_sha256"],
     "input cap pins")

for name, key in (("PLAN.json", "plan_sha256"),
                  ("PRODUCER_LEDGER.json", "ledger_sha256"),
                  ("REPORT.md", "report_sha256"),
                  ("MANIFEST.sha256", "manifest_sha256")):
    need(sha(PROD / name) == PLAN["producer"][key], "producer " + name)

edge = PLAN["stage01_edge_audit"]
need(sha(ROOT / edge["result"]) == edge["result_sha256"], "stage01 edge result pin")
need(sha(ROOT / edge["manifest"]) == edge["manifest_sha256"], "stage01 edge manifest pin")
edge_result = load(ROOT / edge["result"])
need(edge_result["status"] == "PASS_EXACT_EDGE_HARD_RESOURCE_PASS_COOPERATIVE_NATIVE_OVERSHOOT",
     "stage01 edge status")
need(edge_result["native_timer"]["classification"]
     == "COOPERATIVE_TOP_OF_LOOP_OVERSHOOT_NOT_HARD_RESOURCE_FAILURE",
     "stage01 native classification")

ledger = load(PROD / "PRODUCER_LEDGER.json")
contract = PLAN["contract"]
need(ledger["status"] == "PASS_PRODUCER_HELD_FOR_INDEPENDENT_AUDIT", "producer status")
need(ledger["input"]["amended_plan_sha256"] == PLAN["producer"]["plan_sha256"],
     "amended plan pin")
need((ledger["contract"]["source_sha256"], ledger["contract"]["binary_sha256"],
      ledger["contract"]["watchdog_sha256"])
     == (contract["source_sha256"], contract["binary_sha256"],
         contract["watchdog_sha256"]), "producer contract pins")

manifest = {line.split(maxsplit=1)[1]: line.split(maxsplit=1)[0]
            for line in (PROD / "MANIFEST.sha256").read_text().splitlines()
            if line.strip()}
need(len(manifest) == 47, "producer manifest count")

stages = []
records_all = []
columns = PLAN["input"]["columns"]
small_hashes = {}
for index, (spec, declared) in enumerate(zip(PLAN["stages"],
                                             ledger["accepted_stages"],
                                             strict=True)):
    need(spec["name"] == declared["name"], "stage order")
    directory = PROD / spec["name"]
    result = load(directory / "result.json")
    watchdog = load(directory / "watchdog.json")
    records = result["rounds"]
    need([record["round"] for record in records] == spec["rounds"],
         spec["name"] + " rounds")
    need(result["rounds_completed"] == spec["rounds"][-1]
         and result["cached_vectors_loaded"] == columns
         and result["vectors_materialized_on_restore"] == 0,
         spec["name"] + " restore")
    need((result["workers"], result["pivot_mode"], result["strategy"],
          result["elimination_kernel"], result["incremental_basis"],
          result["column_cap"])
         == (16, "rare", "cold", "hierarchical", False, 3500000),
         spec["name"] + " mode")
    need((result["status"], result["incomplete_reason"])
         == ("INCOMPLETE_SEARCH_CAP", "ROUND_CAP"), spec["name"] + " status")
    for record in records:
        need(record["new_columns"] > 0
             and (record["selected_strategy"], record["selected_pivot"])
             == ("cold", "rare"), spec["name"] + " record")
        columns += record["new_columns"]
        need(record["columns"] == columns, spec["name"] + " column recurrence")
    need((result["column_orbits_exposed"], result["dual_support"])
         == (columns, records[-1]["dual_support"]), spec["name"] + " census")

    need(watchdog["status"] == "PASS" and watchdog["returncode"] == 0
         and watchdog["breach"] is None and watchdog["atomic_outputs_clean"],
         spec["name"] + " watchdog")
    need((watchdog["source_sha256"], watchdog["binary_sha256"],
          watchdog["watchdog_sha256"])
         == (contract["source_sha256"], contract["binary_sha256"],
             contract["watchdog_sha256"]), spec["name"] + " watchdog pins")
    need(watchdog["elapsed_seconds"] < contract["wrapper_wall_seconds"]
         and watchdog["peak_rss_kib"] < contract["rss_limit_kib"]
         and all(sample["rss_kib"] < contract["rss_limit_kib"]
                 for sample in watchdog["samples"]), spec["name"] + " resources")
    if index == 0:
        need(result["elapsed_seconds"] == 126.429282
             and result["elapsed_seconds"] > contract["native_wall_seconds"]
             and watchdog["elapsed_seconds"] == 128.306338,
             "stage01 cooperative overshoot evidence")
    else:
        need(result["elapsed_seconds"] < contract["native_wall_seconds"],
             spec["name"] + " native wall")
    for flag, value in (("--round-cap", str(spec["rounds"][-1])),
                        ("--column-cap", "3500000"),
                        ("--wall-seconds", "120"), ("--workers", "16"),
                        ("--pivot", "rare"), ("--strategy", "cold"),
                        ("--elimination", "hierarchical"),
                        ("--incremental", "no")):
        need(arg(watchdog["command"], flag) == value, spec["name"] + " " + flag)
    need(not list(directory.glob("*.tmp")), spec["name"] + " tmp")

    actual_result = sha(directory / "result.json")
    actual_watchdog = sha(directory / "watchdog.json")
    small_hashes[spec["name"] + "_result"] = actual_result
    small_hashes[spec["name"] + "_watchdog"] = actual_watchdog
    need(actual_result == declared["result_sha256"]
         == manifest[spec["name"] + "/result.json"], spec["name"] + " result pin")
    need(actual_watchdog == declared["watchdog_sha256"]
         == manifest[spec["name"] + "/watchdog.json"], spec["name"] + " watchdog pin")
    need(declared["checkpoint_sha256"]
         == manifest[spec["name"] + "/checkpoint.bin"], spec["name"] + " cp pin")
    need(declared["vector_cache_sha256"]
         == manifest[spec["name"] + "/vectors.bin"], spec["name"] + " cache pin")
    stages.append({
        "stage": spec["name"],
        "input_round": spec["rounds"][0] - 1,
        "output_round": spec["rounds"][-1],
        "rounds": spec["rounds"],
        "input_columns": result["cached_vectors_loaded"],
        "output_columns": columns,
        "support": result["dual_support"],
        "native_elapsed_seconds": result["elapsed_seconds"],
        "watchdog_elapsed_seconds": watchdog["elapsed_seconds"],
        "peak_rss_kib": watchdog["peak_rss_kib"],
    })
    records_all.extend(records)

need([record["round"] for record in records_all] == list(range(1602, 1614)),
     "global round coverage")
blocks = [sum(next(stage["watchdog_elapsed_seconds"] for stage in stages
                   if stage["stage"] == name) for name in block)
          for block in PLAN["blocks"]]
need(blocks == PLAN["expected_block_seconds"] and all(value < 540 for value in blocks),
     "block walls")
need((columns, stages[-1]["support"])
     == (PLAN["target"]["columns"], PLAN["target"]["support"]), "endpoint")

need(REPLAY["status"] == "PASS_ALL_DESCENDANT_EDGES_AND_ALL_COLUMNS",
     "replay status")
need(REPLAY["rounds"] == [1601, 1603] + list(range(1604, 1614)), "replay rounds")
need(REPLAY["columns"] == [PLAN["input"]["columns"]]
     + [stage["output_columns"] for stage in stages], "replay columns")
need(REPLAY["supports"] == [PLAN["input"]["support"]]
     + [stage["support"] for stage in stages], "replay supports")
need(REPLAY["checkpoint_descendant_edges"] == 11
     and REPLAY["cache_descendant_edges"] == 11
     and REPLAY["inherited_vectors_byte_identical"]
     and REPLAY["verification_failures"] == 0
     and REPLAY["target_terms"] == 2
     and REPLAY["candidate_hit_terms"] > 0, "replay exactness")

final = ledger["output"]
need(final["checkpoint_sha256"] == manifest["stage11_cap1613/checkpoint.bin"]
     and final["vector_cache_sha256"] == manifest["stage11_cap1613/vectors.bin"],
     "final manifest pins")
need(FINAL_SHA["status"] == "PASS_FINAL_CHECKPOINT_CACHE_SHA256"
     and FINAL_SHA["checkpoint_sha256"] == final["checkpoint_sha256"]
     and FINAL_SHA["vectors_sha256"] == final["vector_cache_sha256"],
     "independent final large SHA pins")

output = {
    "schema": "KRENN_AFFINE251_D12_V4_1_ROUND1613_CAP3500_CHAIN_AUDIT_V1",
    "status": "PASS_EXACT_ROUND1613_CAP3500_CHAIN_WITH_AUDITED_COOPERATIVE_OVERSHOOT",
    "scope": (
        "Accepted cap-equivalent r1601 state through exact rounds1602..1613; "
        "no r1614 continuation or closure claim."
    ),
    "input": {
        "round": 1601, "columns": PLAN["input"]["columns"],
        "support": PLAN["input"]["support"],
        "checkpoint_sha256": PLAN["input"]["checkpoint_sha256"],
        "vectors_sha256": PLAN["input"]["vectors_sha256"],
    },
    "final": {
        "round": 1613, "columns": columns,
        "new_columns": columns - PLAN["input"]["columns"],
        "support": stages[-1]["support"], "target_coefficient": 1,
        "checkpoint_sha256": final["checkpoint_sha256"],
        "vectors_sha256": final["vector_cache_sha256"],
        "result_sha256": final["result_sha256"],
    },
    "stage_summaries": stages,
    "checkpoint_edges": [{
        "input_round": REPLAY["rounds"][i],
        "output_round": REPLAY["rounds"][i + 1],
        "preserved": REPLAY["columns"][i],
        "new_columns": REPLAY["columns"][i + 1] - REPLAY["columns"][i],
    } for i in range(11)],
    "cache_edges": [{
        "input_round": REPLAY["rounds"][i],
        "output_round": REPLAY["rounds"][i + 1],
        "preserved_byte_identically": REPLAY["columns"][i],
        "new_records": REPLAY["columns"][i + 1] - REPLAY["columns"][i],
        "provider_fingerprint": REPLAY["provider_fingerprint"],
    } for i in range(11)],
    "stage01_native_overshoot": {
        "classification": "ACCEPT_EXACT_STATE_COOPERATIVE_NATIVE_OVERSHOOT",
        "native_elapsed_seconds": 126.429282,
        "hard_watchdog_elapsed_seconds": 128.306338,
        "hard_watchdog_limit_seconds": 150,
        "hard_watchdog_pass": True,
        "independent_edge_audit_sha256": edge["result_sha256"],
        "independent_edge_manifest_sha256": edge["manifest_sha256"],
        "amended_plan_sha256": PLAN["producer"]["plan_sha256"],
        "resource_classification": (
            "native timer is a cooperative top-of-loop signal; hard wrapper and "
            "atomic/RSS contract passed"
        ),
    },
    "resources": {
        "aggregate_block_watchdog_seconds": blocks,
        "each_required_less_than": 540,
        "maximum_peak_rss_kib": max(stage["peak_rss_kib"] for stage in stages),
        "rss_limit_kib": contract["rss_limit_kib"],
    },
    "all_column_replay": REPLAY,
    "independent_final_large_sha256": FINAL_SHA,
    "small_artifact_sha256": small_hashes,
    "pins": {
        "input_cap_audit_sha256": PLAN["input"]["cap_audit_sha256"],
        "input_cap_manifest_sha256": PLAN["input"]["cap_manifest_sha256"],
        "compaction_record_sha256": PLAN["input"]["compaction_record_sha256"],
        "producer_plan_sha256": PLAN["producer"]["plan_sha256"],
        "producer_manifest_sha256": PLAN["producer"]["manifest_sha256"],
        "producer_ledger_sha256": PLAN["producer"]["ledger_sha256"],
        "producer_report_sha256": PLAN["producer"]["report_sha256"],
        "source_sha256": contract["source_sha256"],
        "binary_sha256": contract["binary_sha256"],
        "watchdog_sha256": contract["watchdog_sha256"],
        "scanner_base_source_sha256":
            "27d84ba2d29b8561a4f69a24d9711eb4138762142bac3d408e176ee1349fb446",
        "scanner_generator_sha256": sha(HERE / "generate_scanner.py"),
        "scanner_source_sha256": sha(HERE / "scan_chain_once.rs"),
        "scanner_binary_sha256": sha(HERE / "scan_chain_once"),
        "replay_sha256": sha(HERE / "results_round1613_single_pass_replay.json"),
    },
    "verdict_note": (
        "Round1613 is an exact resumable ROUND_CAP state, not a terminal global "
        "dual; the CEGAR search remains open."
    ),
}
temporary = HERE / "results_round1613_chain_audit.json.tmp"
temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_round1613_chain_audit.json")
print(json.dumps({"status": output["status"], "round": 1613,
                  "columns": columns, "terms": REPLAY["terms_replayed"],
                  "failures": 0, "blocks": blocks}, sort_keys=True))

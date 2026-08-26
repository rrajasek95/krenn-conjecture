#!/usr/bin/env python3
"""Fail-closed small-file seal for the independent r1614->r1626 replay."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PLAN = json.loads((HERE / "AUDIT_PLAN.json").read_text())
PROD = ROOT / PLAN["production_root"]
REPLAY = json.loads((HERE / "results_round1626_single_pass_replay.json").read_text())
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


# Authoritative accepted input and producer package.
for name, key in (("cap_audit", "cap_audit_sha256"),
                  ("cap_manifest", "cap_manifest_sha256")):
    need(sha(ROOT / PLAN["input"][name]) == PLAN["input"][key], key)
cap = load(ROOT / PLAN["input"]["cap_audit"])
need(cap["status"] == "PASS_EXACT_DIRECT_CAP3500_TO_CAP3750_EQUIVALENCE",
     "input cap status")
need(cap["accepted_candidate"] == "candidate_cap3750", "accepted input lane")
need(cap["checkpoint_sha256"] == PLAN["input"]["checkpoint_sha256"]
     and cap["vectors_sha256"] == PLAN["input"]["vectors_sha256"],
     "input checkpoint/cache pins")

for name, key in (("PLAN.json", "plan_sha256"),
                  ("PRODUCER_LEDGER.json", "ledger_sha256"),
                  ("REPORT.md", "report_sha256"),
                  ("MANIFEST.sha256", "manifest_sha256"),
                  (PLAN["producer"]["proactive_compaction"],
                   "proactive_compaction_sha256")):
    need(sha(PROD / name) == PLAN["producer"][key], "producer " + name)

ledger = load(PROD / "PRODUCER_LEDGER.json")
contract = PLAN["contract"]
need(ledger["status"] == "PASS_PRODUCER_HELD_FOR_INDEPENDENT_AUDIT",
     "producer status")
need(ledger["input"]["plan_sha256"] == PLAN["producer"]["plan_sha256"],
     "plan pin")
need((ledger["contract"]["source_sha256"],
      ledger["contract"]["binary_sha256"],
      ledger["contract"]["watchdog_sha256"])
     == (contract["source_sha256"], contract["binary_sha256"],
         contract["watchdog_sha256"]), "execution pins")

manifest = {line.split(maxsplit=1)[1]: line.split(maxsplit=1)[0]
            for line in (PROD / "MANIFEST.sha256").read_text().splitlines()
            if line.strip()}
need(len(manifest) == 52, "producer manifest entry count")

# Small stage records, exact recurrence, commands, resources, and atomicity.
columns = PLAN["input"]["columns"]
stages = []
small_hashes = {}
for index, (name, declared) in enumerate(zip(
        PLAN["stages"], ledger["accepted_stages"], strict=True), start=1):
    need(name == declared["name"], "stage order")
    expected_round = 1614 + index
    directory = PROD / name
    result = load(directory / "result.json")
    watchdog = load(directory / "watchdog.json")
    need(result["rounds_completed"] == expected_round
         and [record["round"] for record in result["rounds"]] == [expected_round],
         name + " exact one-round interval")
    need(result["cached_vectors_loaded"] == columns
         and result["vectors_materialized_on_restore"] == 0,
         name + " inherited cache restore")
    need((result["status"], result["incomplete_reason"])
         == ("INCOMPLETE_SEARCH_CAP", "ROUND_CAP"), name + " terminal reason")
    need((result["prime"], result["workers"], result["pivot_mode"],
          result["strategy"], result["elimination_kernel"],
          result["incremental_basis"], result["column_cap"])
         == (contract["prime"], contract["workers"], contract["pivot"],
             contract["strategy"], contract["elimination"],
             contract["incremental"], contract["column_cap"]), name + " mode")
    record = result["rounds"][0]
    need(record["new_columns"] > 0
         and (record["selected_strategy"], record["selected_pivot"])
         == (contract["strategy"], contract["pivot"]), name + " selected mode")
    columns += record["new_columns"]
    need(record["columns"] == columns
         and result["column_orbits_exposed"] == columns
         and result["dual_support"] == record["dual_support"],
         name + " column/support recurrence")

    need(watchdog["status"] == "PASS" and watchdog["returncode"] == 0
         and watchdog["breach"] is None and watchdog["atomic_outputs_clean"],
         name + " watchdog/atomic")
    need((watchdog["source_sha256"], watchdog["binary_sha256"],
          watchdog["watchdog_sha256"])
         == (contract["source_sha256"], contract["binary_sha256"],
             contract["watchdog_sha256"]), name + " watchdog pins")
    need(result["elapsed_seconds"] < contract["native_wall_seconds"]
         and watchdog["elapsed_seconds"] < contract["wrapper_wall_seconds"]
         and watchdog["peak_rss_kib"] < contract["rss_limit_kib"]
         and all(sample["rss_kib"] < contract["rss_limit_kib"]
                 for sample in watchdog["samples"]), name + " resources")
    for flag, value in (("--round-cap", str(expected_round)),
                        ("--column-cap", str(contract["column_cap"])),
                        ("--wall-seconds", str(contract["native_wall_seconds"])),
                        ("--workers", str(contract["workers"])),
                        ("--pivot", contract["pivot"]),
                        ("--strategy", contract["strategy"]),
                        ("--elimination", contract["elimination"]),
                        ("--incremental", "no")):
        need(arg(watchdog["command"], flag) == value, name + " " + flag)
    need(not list(directory.glob("*.tmp")), name + " no temporary output")

    result_sha = sha(directory / "result.json")
    watchdog_sha = sha(directory / "watchdog.json")
    small_hashes[name + "_result"] = result_sha
    small_hashes[name + "_watchdog"] = watchdog_sha
    need(result_sha == declared["result_sha256"]
         == manifest[name + "/result.json"], name + " result pin")
    need(watchdog_sha == declared["watchdog_sha256"]
         == manifest[name + "/watchdog.json"], name + " watchdog pin")
    need(declared["checkpoint_sha256"] == manifest[name + "/checkpoint.bin"],
         name + " checkpoint manifest pin")
    need(declared["vector_cache_sha256"] == manifest[name + "/vectors.bin"],
         name + " cache manifest pin")
    stages.append({
        "stage": name,
        "input_round": expected_round - 1,
        "output_round": expected_round,
        "input_columns": result["cached_vectors_loaded"],
        "output_columns": columns,
        "new_columns": record["new_columns"],
        "support": result["dual_support"],
        "native_elapsed_seconds": result["elapsed_seconds"],
        "watchdog_elapsed_seconds": watchdog["elapsed_seconds"],
        "peak_rss_kib": watchdog["peak_rss_kib"],
    })

need((columns, stages[-1]["support"])
     == (PLAN["target"]["columns"], PLAN["target"]["support"]), "endpoint")
blocks = [sum(stage["watchdog_elapsed_seconds"] for stage in stages[start:end])
          for start, end in PLAN["blocks"]]
declared_blocks = [block["aggregate_watchdog_seconds"] for block in ledger["blocks"]]
need(blocks == declared_blocks and all(value < 540 for value in blocks),
     "block wall contracts")

# The sole large scan verifies every prefix edge and evaluates every final column.
need(REPLAY["status"] == "PASS_ALL_DESCENDANT_EDGES_AND_ALL_COLUMNS",
     "replay status")
need(REPLAY["rounds"] == list(range(1614, 1627)), "replay rounds")
need(REPLAY["columns"] == [PLAN["input"]["columns"]]
     + [stage["output_columns"] for stage in stages], "replay columns")
need(REPLAY["supports"] == [PLAN["input"]["support"]]
     + [stage["support"] for stage in stages], "replay supports")
need(REPLAY["checkpoint_descendant_edges"] == 12
     and REPLAY["cache_descendant_edges"] == 12
     and REPLAY["inherited_vectors_byte_identical"]
     and REPLAY["verification_failures"] == 0
     and REPLAY["target_terms"] == 2
     and REPLAY["candidate_hit_terms"] > 0, "replay exactness")

final = ledger["output"]
need(final["checkpoint_sha256"] == manifest["stage12_cap1626/checkpoint.bin"]
     and final["vector_cache_sha256"] == manifest["stage12_cap1626/vectors.bin"],
     "final producer manifest pins")
need(FINAL_SHA["status"] == "PASS_FINAL_CHECKPOINT_CACHE_SHA256"
     and FINAL_SHA["checkpoint_sha256"] == final["checkpoint_sha256"]
     and FINAL_SHA["vectors_sha256"] == final["vector_cache_sha256"],
     "independent final hashes")
need(sha(ROOT / PLAN["scanner"]["source"]) == PLAN["scanner"]["source_sha256"]
     and sha(ROOT / PLAN["scanner"]["binary"]) == PLAN["scanner"]["binary_sha256"],
     "scanner pins")

output = {
    "schema": "KRENN_AFFINE251_D12_V4_1_ROUND1626_CAP3750_CHAIN_AUDIT_V1",
    "status": "PASS_EXACT_ROUND1626_CAP3750_CHAIN",
    "scope": "Accepted cap-equivalent r1614 state through exact rounds1615..1626; no r1627 continuation or closure claim.",
    "input": {
        "round": 1614, "columns": PLAN["input"]["columns"],
        "support": PLAN["input"]["support"],
        "checkpoint_sha256": PLAN["input"]["checkpoint_sha256"],
        "vectors_sha256": PLAN["input"]["vectors_sha256"],
    },
    "final": {
        "round": 1626, "columns": columns,
        "new_columns": columns - PLAN["input"]["columns"],
        "support": stages[-1]["support"], "target_coefficient": 1,
        "checkpoint_sha256": final["checkpoint_sha256"],
        "vectors_sha256": final["vector_cache_sha256"],
        "result_sha256": final["result_sha256"],
    },
    "stage_summaries": stages,
    "checkpoint_descendant_edges": 12,
    "cache_descendant_edges": 12,
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
        "producer_plan_sha256": PLAN["producer"]["plan_sha256"],
        "producer_ledger_sha256": PLAN["producer"]["ledger_sha256"],
        "producer_report_sha256": PLAN["producer"]["report_sha256"],
        "producer_manifest_sha256": PLAN["producer"]["manifest_sha256"],
        "proactive_compaction_sha256": PLAN["producer"]["proactive_compaction_sha256"],
        "source_sha256": contract["source_sha256"],
        "binary_sha256": contract["binary_sha256"],
        "watchdog_sha256": contract["watchdog_sha256"],
        "scanner_source_sha256": PLAN["scanner"]["source_sha256"],
        "scanner_binary_sha256": PLAN["scanner"]["binary_sha256"],
        "replay_sha256": sha(HERE / "results_round1626_single_pass_replay.json"),
    },
    "verdict_note": "Round1626 is an exact resumable ROUND_CAP state, not a terminal global dual; the CEGAR search remains open."
}
temporary = HERE / "results_round1626_chain_audit.json.tmp"
temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_round1626_chain_audit.json")
print(json.dumps({"status": output["status"], "round": 1626,
                  "columns": columns, "terms": REPLAY["terms_replayed"],
                  "failures": 0, "blocks": blocks}, sort_keys=True))

#!/usr/bin/env python3
"""Independent fail-closed referee for the frozen v4 warm10 gate."""
from __future__ import annotations

import hashlib, json, os, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROD = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25"
V3 = PROD / "warm10_v3"
V4 = PROD / "warm10_v4"
SOURCE3 = "173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a"
BIN3 = "8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a"
SOURCE4 = "c83c6801ec2c09683c81773607fcf3babb538e34354dfd8f27d03aae0e22f102"
BIN4 = "191eb08843466e263149ccd5688b57a5f5352cbb2dfbc5e1081fca856b2e5c0b"

def need(ok, why):
    if not ok: raise SystemExit("REJECT: " + why)

def load(path): return json.loads(path.read_text())

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""): h.update(block)
    return h.hexdigest()

def semantic_result(value):
    value = json.loads(json.dumps(value))
    for key in ("elapsed_seconds", "peak_rss_kib", "restore_seconds",
                "vector_cache_write_seconds", "checkpoint", "vector_cache", "dual"):
        value.pop(key, None)
    for row in value["rounds"]:
        for key in ("incident_seconds", "materialize_seconds", "solve_seconds"):
            row.pop(key, None)
    return value

def phase_sum(path, field):
    found = [float(x) for x in re.findall(r"(?:^| )" + re.escape(field) + r"=([0-9.]+)s", path.read_text())]
    need(len(found) == 10, f"{field} count")
    return sum(found)

def watchdog(path, source, binary):
    value = load(path)
    need(value["schema"] == "KRENN_AFFINE251_D12_MACOS_RSS_WATCHDOG_V2", "watchdog schema")
    need(value["status"] == "PASS" and value["returncode"] == 0 and value["breach"] is None, "watchdog terminal")
    need(value["atomic_outputs_clean"] is True, "atomic outputs")
    need(value["source_sha256"] == source and value["binary_sha256"] == binary, "watchdog pins")
    limit = 36 * 1024 * 1024
    need(value["rss_limit_kib"] == limit and value["contract_rss_limit_kib"] == limit, "watchdog limit")
    need(value["peak_rss_kib"] < limit and all(s["rss_kib"] < limit for s in value["samples"]), "watchdog RSS")
    need(value["sample_count"] == len(value["samples"]) > 0, "watchdog samples")
    need(value["last_successful_rss_sample"] == value["samples"][-1], "watchdog last sample")
    return {"sha256": sha(path), "peak_rss_kib": value["peak_rss_kib"], "elapsed_seconds": value["elapsed_seconds"]}

def main():
    contract = load(HERE / "AUDIT_CONTRACT_WARM10.json")
    need(contract["status"] == "FROZEN_BEFORE_WARM10_TIMINGS", "contract")
    r3, r4 = load(V3 / "result.json"), load(V4 / "result.json")
    expected_rounds = list(range(951, 961))
    for label, result in (("v3", r3), ("v4", r4)):
        need(result["status"] == "INCOMPLETE_SEARCH_CAP" and result["incomplete_reason"] == "ROUND_CAP", label + " status")
        need(result["rounds_completed"] == 960, label + " final round")
        need([r["round"] for r in result["rounds"]] == expected_rounds, label + " no-gap chain")
        need(result["column_orbits_exposed"] == 576401 and result["dual_support"] == 540, label + " final census")
    need(semantic_result(r3) == semantic_result(r4), "roundwise/final non-timing equality")

    checkpoint3, checkpoint4 = sha(V3 / "checkpoint.bin"), sha(V4 / "checkpoint.bin")
    vectors3, vectors4 = sha(V3 / "vectors.bin"), sha(V4 / "vectors.bin")
    need(checkpoint3 == checkpoint4 == "2e7b7a56ed4af7d98f979d0fe0549bcf15aa7fdf1b32e97688418e5f6f198f4c", "checkpoint bytes")
    need(vectors3 == vectors4 == "76e937520a5cb38e1080fcee637de6f9a54dff826c2644362a0ec2a5dc92ce03", "cache bytes")

    one = PROD / "candidate_v4"
    rebuild = PROD / "rebuild_v4"
    one_checkpoint = sha(one / "checkpoint.bin")
    rebuild_checkpoint = sha(rebuild / "checkpoint.bin")
    one_vectors = sha(one / "vectors.bin")
    rebuild_vectors = sha(rebuild / "vectors.bin")
    need(one_checkpoint == rebuild_checkpoint, "attempt3 rebuild checkpoint")
    need(one_vectors == rebuild_vectors, "attempt3 rebuild cache")
    need(semantic_result(load(one / "result.json")) == semantic_result(load(rebuild / "result.json")), "attempt3 rebuild result")

    elapsed3, elapsed4 = r3["elapsed_seconds"], r4["elapsed_seconds"]
    absolute = elapsed3 - elapsed4
    relative = absolute / elapsed3
    sort3 = phase_sum(V3 / "stderr.log", "ordered_sort")
    commit4 = phase_sum(V4 / "stderr.log", "rare_commit")
    flatten4 = phase_sum(V4 / "stderr.log", "rare_flatten")
    speedup = sort3 / (commit4 + flatten4)
    need(absolute >= .5 and relative >= .05 and speedup >= 1.5, "frozen performance thresholds")

    order = load(HERE / "results_warm10_external_order_gate.json")
    final_order = order["round850"]
    need(order["status"] == "PASS_EXACT_ROUND849_850_ORDER_EQUIVALENCE", "external order status")
    need(final_order["records"] == 576401 and final_order["terms"] == 58615777 and final_order["ranked_rows"] == 32480668, "external order census")
    need(final_order["order_sha256_baseline"] == final_order["order_sha256_index"] == "e87d2920434f84e5409bc20b11e59cc8c35acb56ba618d64444356ea7ea9d75f", "external exact order")
    replay = load(HERE / "results_warm10_all_column_replay.json")
    need(replay["status"] == "PASS_ALL_COLUMNS" and replay["round"] == 960, "replay status")
    need(replay["columns_replayed"] == 576401 and replay["terms_replayed"] == 58615777 and replay["verification_failures"] == 0, "replay census")

    hostiles = load(PROD / "results_hostiles.json")
    need(hostiles["status"] == "PASS" and hostiles["source_sha256"] == SOURCE4 and hostiles["binary_sha256"] == BIN4, "hostile pins/status")
    need(all(x["status"] == "PASS_REJECTED" and x["returncode"] != 0 for x in hostiles["cases"].values()), "hostile cases")
    static = load(HERE / "results_v4_attempt3_static_audit.json")
    need(static["status"] == "PASS_STATIC_V4_RARE_INDEX_INTEGRATION" and static["v4_source_sha256"] == SOURCE4 and static["v4_binary_sha256"] == BIN4, "static audit")

    output = {
      "schema": "KRENN_AFFINE251_D12_V4_RARE_INDEX_WARM10_REFEREE_V1",
      "status": "PASS_PROMOTE_EXACT_V4_RARE_INDEX_WARM10",
      "scope": "Frozen matched round950->960 warm gate; no further continuation.",
      "pins": {"v3_source_sha256": SOURCE3, "v3_binary_sha256": BIN3, "v4_source_sha256": SOURCE4, "v4_binary_sha256": BIN4,
               "v3_result_sha256": sha(V3 / "result.json"), "v4_result_sha256": sha(V4 / "result.json"),
               "checkpoint_sha256": checkpoint3, "vectors_sha256": vectors3,
               "contract_sha256": sha(HERE / "AUDIT_CONTRACT_WARM10.json"),
               "static_audit_sha256": sha(HERE / "results_v4_attempt3_static_audit.json"),
               "external_order_gate_sha256": sha(HERE / "results_warm10_external_order_gate.json"),
               "all_column_replay_sha256": sha(HERE / "results_warm10_all_column_replay.json"),
               "hostiles_sha256": sha(PROD / "results_hostiles.json")},
      "exactness": {"rounds": expected_rounds, "columns": 576401, "support": 540, "terms": 58615777,
                    "order_rows": 32480668, "order_sha256": final_order["order_sha256_index"], "pairing_failures": 0,
                    "checkpoint_byte_identical": True, "cache_byte_identical": True, "attempt3_rebuild_identical": True,
                    "attempt3_round951_checkpoint_sha256": one_checkpoint,
                    "attempt3_round951_vectors_sha256": one_vectors},
      "performance": {"v3_native_seconds": elapsed3, "v4_native_seconds": elapsed4,
                      "absolute_improvement_seconds": absolute, "relative_improvement": relative,
                      "v3_order_seconds_sum": sort3, "v4_commit_seconds_sum": commit4,
                      "v4_flatten_seconds_sum": flatten4, "order_speedup": speedup},
      "resources": {"v3": watchdog(V3 / "watchdog.json", SOURCE3, BIN3), "v4": watchdog(V4 / "watchdog.json", SOURCE4, BIN4)},
      "caveat": "The prior one-round attempt3 comparison remains REJECT_PERFORMANCE; promotion is for the separately frozen ten-round production-amortization gate."
    }
    tmp = HERE / "results_v4_warm10_referee.json.tmp"
    tmp.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, HERE / "results_v4_warm10_referee.json")

if __name__ == "__main__": main()

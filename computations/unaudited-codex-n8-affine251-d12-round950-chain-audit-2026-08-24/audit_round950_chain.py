#!/usr/bin/env python3
"""Independent no-gap audit of D12 round850→950 production."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRODUCER = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24"
PRODUCTION = PRODUCER / "production_from_round850"
INPUT_PACKAGE = ROOT / "computations/unaudited-codex-n8-affine251-d12-round850-portfolio-audit-2026-08-24"
INPUT = INPUT_PACKAGE / "portfolio"
AUDIT = Path(__file__).resolve().parent
FORMAT_SOURCE = (ROOT / "computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24"
                 / "audit_stage01.py")
RSS_LIMIT_KIB = 36 * 1024 * 1024
EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
SOURCE_SHA = "173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a"
BINARY_SHA = "8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a"
WATCHDOG_SHA = "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"

EXPECTED = {
    "format_source": "976dba4bb45d5ae59d9e1350f5231b487f7a2bfb9495db9de0f7585666051b67",
    "input_audit": "7950debc1e97095a835e087fb704cdc20df0448b37acf1e2e267d0a4cd296243",
    "input_manifest": "3c02377581ea40358c503ce17ec3f5a95e2577fa9779361df645c1cccdcbf1b6",
    "input_checkpoint": "c2ea7cc0b72218e06866c3db2bd3a269a7ccdbdbf276132e62415d23a23f0fa7",
    "input_vectors": "df181c0b86de9a2827d1146a318682482b9af2cae66b470fdf5d11fa036d1ec4",
    "stage01_result": "be91f5c18f8cf35fd6d581f123a02fb9bd60773e54e99fcf615c5ad65b26f33c",
    "stage01_checkpoint": "c8fd72320c101a2e37640dcbcf356de63175009ce906a373da9422096ea28762",
    "stage01_vectors": "43bf60dc6957a19cfc22966503df388b1087c5933914af67b49c8a80b5440e55",
    "stage01_watchdog": "fcccb1b387eae4b3b317e2aa5ba2b5b0b233d279ffd108a179395d8c73edaf3f",
    "stage01_stderr": "2b8cbf99ceaeb470e493f7b69842382436e89b1e1b630c4da75bc90f6a9405d6",
    "stage02_result": "faae5fbd37dc95874cf59ef810ae41b302602f4c61a4e9c902556594477bcade",
    "stage02_checkpoint": "792aa4b12b49b02fefe586824bd5db30f034e8a465c2a68f0a9dea96fd9a87c6",
    "stage02_vectors": "56932c40d0645a21eb439426d406ab70cd7b6012a27a71870d81616906ce95c2",
    "stage02_watchdog": "b2fe563dfe3e048b00a9f911d9c0f0f88ee976717ecead5bfa5cf608f8427c9f",
    "stage02_stderr": "9bfc91d91e9265abbb046c5e8bf3f90e0b8e6986c194790adae58a87068e2486",
    "stage03_result": "f9e22d28d46ea4b81a44366b6ddb43439a9311edb7e83b53b60046c48d9f8c12",
    "stage03_checkpoint": "d0dea4b47fa23339f27d62d551375bda39415cc470b2f1024ab5a5f92ed94d7c",
    "stage03_vectors": "7df080b98ea9c108d28bf0803a6533d1c2453a5becf0ee14aaabb6cc7aac6ed5",
    "stage03_watchdog": "e0a6e233ea38fac4aaf34bf96f2aaba2da97fc9a0ec908d8b59aede5c5901806",
    "stage03_stderr": "bd9d58c410a07bb9d2cf86b55cf752d12fb1e138807f5f5529885bc067b2af13",
    "stage04_result": "8c9c501e3aeaacad7c7fa1baf12df375b44c6a5e9d84bbd3fa7159b5283f6750",
    "stage04_checkpoint": "976c2d51add31269563b030e53ef76601e75027943f55cdd2cfa1a38fdbc1330",
    "stage04_vectors": "635031957d98cd1267d8e398951f720c3295a3678c3199a36532f70fc1ed3e54",
    "stage04_watchdog": "7547ff1c0e3e265c725b272f191281214d28ca8fd7022dd48e3b76b357bd179e",
    "stage04_stderr": "6c503afc53c064b60c87a73323d9e27f3ffc4f7846e53089fe5ae94db95ec7a6",
    "stage05_result": "a799c4b7c78305cdc37b6465ad68a97336f1d2200a820ca5a112611e2a08383b",
    "stage05_checkpoint": "8eee9ce80e36b105d1b7d7a733628639b2ecadff302551367c86709804dcbb4b",
    "stage05_vectors": "1a8eeb6fe4467466a99089f833f519665af802b512bead394c86ed953c2c8def",
    "stage05_watchdog": "092a7e3fddcf7a0489d6889069fcc5acf7764eaacb06263ef0bb474be41d0b8b",
    "stage05_stderr": "ef03e0ea9a1531d7278e0e2de64fa003307e6099f06a81ca6e045275f0cf35cb",
    "native_source": SOURCE_SHA, "native_binary": BINARY_SHA,
    "watchdog_v2": WATCHDOG_SHA,
    "final_replay": "96cc92350d475b286abde2e9f44889a018d5da1a261ff42cb1ea3b167e0965e7",
}

STAGES = [
    {"name": "stage01", "input_round": 850, "input_columns": 461_464,
     "output_round": 873, "output_columns": 482_702, "support": 395,
     "records": 23, "status": "INCOMPLETE_RESOURCE_GATE", "reason": "WALL_CAP",
     "samples": 384, "peak": 7_565_808},
    {"name": "stage02", "input_round": 873, "input_columns": 482_702,
     "output_round": 894, "output_columns": 504_463, "support": 393,
     "records": 21, "status": "INCOMPLETE_RESOURCE_GATE", "reason": "WALL_CAP",
     "samples": 384, "peak": 6_894_624},
    {"name": "stage03", "input_round": 894, "input_columns": 504_463,
     "output_round": 915, "output_columns": 527_037, "support": 454,
     "records": 21, "status": "INCOMPLETE_RESOURCE_GATE", "reason": "WALL_CAP",
     "samples": 393, "peak": 7_973_984},
    {"name": "stage04", "input_round": 915, "input_columns": 527_037,
     "output_round": 934, "output_columns": 545_580, "support": 393,
     "records": 19, "status": "INCOMPLETE_RESOURCE_GATE", "reason": "WALL_CAP",
     "samples": 385, "peak": 8_193_568},
    {"name": "stage05", "input_round": 934, "input_columns": 545_580,
     "output_round": 950, "output_columns": 563_342, "support": 518,
     "records": 16, "status": "INCOMPLETE_SEARCH_CAP", "reason": "ROUND_CAP",
     "samples": 322, "peak": 8_291_984},
]


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def pinned(path: Path, label: str) -> str:
    actual = sha256(path)
    require(actual == EXPECTED[label], label + " SHA")
    return actual


def load_format_referee():
    pinned(FORMAT_SOURCE, "format_source")
    spec = importlib.util.spec_from_file_location("stage01_format_referee", FORMAT_SOURCE)
    require(spec is not None and spec.loader is not None, "format referee import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compare_vector_descendant(format_referee, old_path: Path, new_path: Path,
                              old_count: int, new_count: int) -> dict:
    with old_path.open("rb") as old, new_path.open("rb") as new:
        old_header = format_referee.vector_header(old, "input cache")
        new_header = format_referee.vector_header(new, "output cache")
        require((old_header["count"], new_header["count"]) == (old_count, new_count),
                "cache header counts")
        require(old_header["provider_fingerprint"] == new_header["provider_fingerprint"],
                "provider fingerprint drift")
        old_record = format_referee.vector_record(old, "input cache record")
        new_record = format_referee.vector_record(new, "output cache record")
        matched = extras = 0
        while old_record is not None:
            require(new_record is not None, "output cache lost input suffix")
            if new_record[0] < old_record[0]:
                extras += 1
                new_record = format_referee.vector_record(new, "output cache record")
            elif new_record[0] == old_record[0]:
                require(new_record[1] == old_record[1], "persisted vector record changed")
                matched += 1
                old_record = format_referee.vector_record(old, "input cache record")
                new_record = format_referee.vector_record(new, "output cache record")
            else:
                raise Reject("output cache omitted input record")
        while new_record is not None:
            extras += 1
            new_record = format_referee.vector_record(new, "output cache record")
        require(old.read(1) == b"" and new.read(1) == b"", "cache trailing bytes")
    require((matched, extras) == (old_count, new_count - old_count),
            "cache descendant census")
    return {"input_records_preserved_byte_identically": matched,
            "new_records": extras,
            "provider_fingerprint": new_header["provider_fingerprint"],
            "input_vector_fingerprint": old_header["vector_fingerprint"],
            "output_vector_fingerprint": new_header["vector_fingerprint"]}


def validate_stage_result(spec: dict) -> tuple[dict, list[dict], float]:
    result = json.loads((PRODUCTION / spec["name"] / "result.json").read_text())
    require(result.get("schema") == "KRENN_AFFINE251_D12_NATIVE_SPARSE_DUAL_V1",
            spec["name"] + " result schema")
    require((result.get("status"), result.get("incomplete_reason")) ==
            (spec["status"], spec["reason"]), spec["name"] + " result status")
    require((result.get("degree"), result.get("prime"), result.get("group_order")) ==
            (12, 1_073_741_827, 1440), spec["name"] + " math header")
    require((result.get("provider_equations"), result.get("provider_terms_parsed"),
             result.get("provider_distinct_terms")) == (6561, 688908, 688906),
            spec["name"] + " provider census")
    require((result.get("workers"), result.get("pivot_mode"), result.get("strategy"),
             result.get("elimination_kernel"), result.get("incremental_basis")) ==
            (16, "rare", "cold", "hierarchical", False), spec["name"] + " mode")
    require((result.get("portfolio_period"), result.get("portfolio_parallel"),
             result.get("support_cap"), result.get("column_cap"),
             result.get("wall_limit_seconds"), result.get("rss_limit_gib")) ==
            (256, True, 100000, 1000000, 95, 36), spec["name"] + " gate fields")
    require((result.get("rounds_completed"), result.get("column_orbits_exposed"),
             result.get("dual_support"), result.get("cached_vectors_loaded"),
             result.get("vectors_materialized_on_restore")) ==
            (spec["output_round"], spec["output_columns"], spec["support"],
             spec["input_columns"], 0), spec["name"] + " terminal census")
    require(result.get("global_annihilation") is None and
            result.get("target_pairing") is None, spec["name"] + " incomplete claims")
    require(result.get("vector_cache_bytes") ==
            (PRODUCTION / spec["name"] / "vectors.bin").stat().st_size,
            spec["name"] + " cache bytes")
    rounds = result.get("rounds")
    require(isinstance(rounds, list) and len(rounds) == spec["records"],
            spec["name"] + " round count")
    columns = spec["input_columns"]
    for index, record in enumerate(rounds):
        require(record.get("round") == spec["input_round"] + index + 1,
                spec["name"] + " round continuity")
        added = record.get("new_columns")
        require(isinstance(added, int) and added > 0, spec["name"] + " new columns")
        columns += added
        require(record.get("columns") == columns, spec["name"] + " column recurrence")
        require(record.get("selected_strategy") == "cold" and
                record.get("selected_pivot") == "rare", spec["name"] + " round mode")
        require(isinstance(record.get("dual_support"), int) and
                record["dual_support"] > 0, spec["name"] + " support")
        for timer in ("incident_seconds", "materialize_seconds", "solve_seconds"):
            require(isinstance(record.get(timer), (int, float)) and
                    math.isfinite(record[timer]) and record[timer] >= 0,
                    spec["name"] + " timer")
    require(columns == spec["output_columns"] and rounds[-1]["dual_support"] == spec["support"],
            spec["name"] + " terminal round")
    summary = {"round_start": rounds[0]["round"], "round_end": rounds[-1]["round"],
               "records": len(rounds), "input_columns": spec["input_columns"],
               "output_columns": spec["output_columns"],
               "new_columns": spec["output_columns"] - spec["input_columns"],
               "support": spec["support"], "status": result["status"],
               "incomplete_reason": result["incomplete_reason"],
               "native_elapsed_seconds": result["elapsed_seconds"]}
    return summary, rounds, result["elapsed_seconds"]


def command_value(command: list[str], flag: str) -> str:
    positions = [index for index, item in enumerate(command) if item == flag]
    require(len(positions) == 1 and positions[0] + 1 < len(command), flag + " command")
    return command[positions[0] + 1]


def validate_watchdog(spec: dict) -> tuple[dict, float]:
    stage = spec["name"]
    directory = PRODUCTION / stage
    telemetry = json.loads((directory / "watchdog.json").read_text())
    require(telemetry.get("schema") == "KRENN_AFFINE251_D12_MACOS_RSS_WATCHDOG_V2" and
            telemetry.get("status") == "PASS", stage + " watchdog status")
    require(telemetry.get("breach") is None and telemetry.get("returncode") == 0,
            stage + " natural exit")
    require((telemetry.get("source_sha256"), telemetry.get("binary_sha256"),
             telemetry.get("watchdog_sha256")) == (SOURCE_SHA, BINARY_SHA, WATCHDOG_SHA),
            stage + " invocation pins")
    require((telemetry.get("rss_observer"), telemetry.get("rss_limit_kib"),
             telemetry.get("contract_rss_limit_kib"), telemetry.get("wall_limit_seconds"),
             telemetry.get("poll_seconds")) ==
            ("libproc_PROC_PIDTASKINFO", RSS_LIMIT_KIB, RSS_LIMIT_KIB, 105, 0.25),
            stage + " watcher contract")
    command = telemetry.get("command")
    require(command_value(command, "--output") == str((directory / "result.json").relative_to(ROOT)) and
            command_value(command, "--checkpoint") == str((directory / "checkpoint.bin").relative_to(ROOT)) and
            command_value(command, "--vector-cache") == str((directory / "vectors.bin").relative_to(ROOT)),
            stage + " command paths")
    fixed = {"--prime": "1073741827", "--wall-seconds": "95", "--rss-gib": "36",
             "--workers": "16", "--pivot": "rare", "--strategy": "cold",
             "--elimination": "hierarchical", "--incremental": "no",
             "--portfolio-period": "256", "--portfolio-parallel": "yes",
             "--support-cap": "100000", "--column-cap": "1000000", "--round-cap": "950"}
    require(all(command_value(command, flag) == expected for flag, expected in fixed.items()),
            stage + " frozen command")
    samples = telemetry.get("samples")
    require(isinstance(samples, list) and len(samples) == telemetry.get("sample_count") ==
            spec["samples"], stage + " sample count")
    previous = -1.0
    for sample in samples:
        require(sample.get("elapsed_seconds", -1) > previous, stage + " sample order")
        previous = sample["elapsed_seconds"]
        require(isinstance(sample.get("rss_kib"), int) and
                0 <= sample["rss_kib"] < RSS_LIMIT_KIB, stage + " RSS cap")
        require(sample.get("process_group_members", 0) >= 1, stage + " live child")
    peak = max(sample["rss_kib"] for sample in samples)
    require(peak == telemetry.get("peak_rss_kib") == spec["peak"], stage + " peak RSS")
    require(telemetry.get("last_successful_rss_sample") == samples[-1],
            stage + " last sample")
    gap = telemetry["elapsed_seconds"] - samples[-1]["elapsed_seconds"]
    require(0 <= gap <= 0.35, stage + " exit observation gap")
    require(telemetry.get("atomic_outputs_clean") is True and
            telemetry.get("quarantined_abort_paths") == [], stage + " atomic outputs")
    require((telemetry.get("result_sha256"), telemetry.get("stderr_sha256"),
             telemetry.get("stdout_sha256")) ==
            (EXPECTED[stage + "_result"], EXPECTED[stage + "_stderr"], EMPTY_SHA),
            stage + " telemetry artifact hashes")
    temporary = [directory / (name + ".tmp") for name in
                 ("result.json", "checkpoint.bin", "vectors.bin", "stdout.log", "stderr.log")]
    require(not any(path.exists() for path in temporary), stage + " temporary output")
    summary = {"status": "PASS", "sample_count": len(samples), "peak_rss_kib": peak,
               "rss_limit_kib": RSS_LIMIT_KIB, "elapsed_seconds": telemetry["elapsed_seconds"],
               "last_sample_to_exit_gap_seconds": gap, "atomic_outputs_clean": True,
               "breach": None, "returncode": 0}
    return summary, telemetry["elapsed_seconds"]


def validate_input_audit() -> dict:
    result = json.loads((INPUT_PACKAGE / "results_round850_audit.json").read_text())
    require(result.get("schema") == "KRENN_AFF251_D12_ROUND850_PORTFOLIO_AUDIT_V1" and
            result.get("status") == "PASS_EXACT_ONE_ROUND_PORTFOLIO_AUDIT",
            "round850 input audit status")
    require((result.get("output_state", {}).get("round"),
             result.get("output_state", {}).get("columns"),
             result.get("output_state", {}).get("support")) == (850, 461_464, 327),
            "round850 input census")
    require((result.get("portfolio", {}).get("hashes", {}).get("checkpoint.bin"),
             result.get("portfolio", {}).get("hashes", {}).get("vectors.bin")) ==
            (EXPECTED["input_checkpoint"], EXPECTED["input_vectors"]),
            "round850 portfolio pins")
    require(result.get("selected_pivot") == "rare" and
            result.get("selected_strategy") == "cold" and
            result.get("continued_beyond_round850") is False,
            "round850 selected mode/scope")
    return {"status": result["status"], "round": 850, "columns": 461_464,
            "support": 327, "pivot": "rare", "strategy": "cold"}


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n"); stream.flush(); os.fsync(stream.fileno())
    os.replace(temporary, path)


def main() -> None:
    artifacts = {
        "input_audit": INPUT_PACKAGE / "results_round850_audit.json",
        "input_manifest": INPUT_PACKAGE / "MANIFEST.sha256",
        "input_checkpoint": INPUT / "checkpoint.bin", "input_vectors": INPUT / "vectors.bin",
        "native_source": PRODUCER / "sealed_v3/main.rs",
        "native_binary": PRODUCER / "sealed_v3/sparse_d12_dual",
        "watchdog_v2": PRODUCER / "sealed_watchdog_v2/run_with_macos_rss_watchdog_v2.py",
        "final_replay": AUDIT / "results_round950_cache_replay.json",
    }
    for spec in STAGES:
        stage = spec["name"]; directory = PRODUCTION / stage
        for suffix, filename in [("result", "result.json"), ("checkpoint", "checkpoint.bin"),
                                 ("vectors", "vectors.bin"), ("watchdog", "watchdog.json"),
                                 ("stderr", "stderr.log")]:
            artifacts[stage + "_" + suffix] = directory / filename
    hashes = {label: pinned(path, label) for label, path in artifacts.items()}
    input_audit = validate_input_audit()
    format_referee = load_format_referee()
    checkpoints = [format_referee.parse_checkpoint(INPUT / "checkpoint.bin")]
    checkpoints += [format_referee.parse_checkpoint(PRODUCTION / spec["name"] / "checkpoint.bin")
                    for spec in STAGES]
    expected_headers = [(850, 461_464, 327), (873, 482_702, 395),
                        (894, 504_463, 393), (915, 527_037, 454),
                        (934, 545_580, 393), (950, 563_342, 518)]
    for checkpoint, expected in zip(checkpoints, expected_headers):
        require((checkpoint["round"], len(checkpoint["columns"]), checkpoint["support"]) ==
                expected, "checkpoint chain header")
        require(checkpoint["target_coefficient"] == 1, "checkpoint target normalization")
    checkpoint_edges = []
    for left, right in zip(checkpoints, checkpoints[1:]):
        old = set(left["columns"]); new = set(right["columns"])
        require(old <= new and len(new - old) == len(new) - len(old),
                "checkpoint exact descendant")
        checkpoint_edges.append({"input_round": left["round"], "output_round": right["round"],
                                 "input_columns_preserved": len(old),
                                 "new_columns": len(new) - len(old)})
    stage_summaries = []; all_rounds = []; native_wall = 0.0
    for spec in STAGES:
        summary, rounds, elapsed = validate_stage_result(spec)
        stage_summaries.append(summary); all_rounds.extend(rounds); native_wall += elapsed
    require([record["round"] for record in all_rounds] == list(range(851, 951)),
            "100-round no-gap sequence")
    columns = 461_464
    for record in all_rounds:
        columns += record["new_columns"]
        require(record["columns"] == columns, "cross-stage column recurrence")
    require(columns == 563_342 and sum(record["new_columns"] for record in all_rounds) == 101_878,
            "aggregate column census")
    cache_paths = [INPUT / "vectors.bin"] + [PRODUCTION / spec["name"] / "vectors.bin"
                                               for spec in STAGES]
    counts = [461_464, 482_702, 504_463, 527_037, 545_580, 563_342]
    cache_edges = []
    for index, (old_path, new_path, old_count, new_count) in enumerate(
            zip(cache_paths, cache_paths[1:], counts, counts[1:]), start=1):
        edge = compare_vector_descendant(format_referee, old_path, new_path, old_count, new_count)
        cache_edges.append({"edge": index, "input_round": expected_headers[index - 1][0],
                            "output_round": expected_headers[index][0], **edge})
    telemetry = {}; watched_wall = 0.0
    for spec in STAGES:
        summary, elapsed = validate_watchdog(spec)
        telemetry[spec["name"]] = summary; watched_wall += elapsed
    require(watched_wall < 540.0 and native_wall < 540.0, "aggregate wall gate")
    maximum_rss = max(item["peak_rss_kib"] for item in telemetry.values())
    require(maximum_rss < RSS_LIMIT_KIB, "aggregate maximum RSS gate")
    replay = json.loads((AUDIT / "results_round950_cache_replay.json").read_text())
    require(replay.get("schema") == "KRENN_AFFINE251_D12_CACHE_REPLAY_V1" and
            replay.get("status") == "PASS_ALL_COLUMNS", "final replay status")
    require((replay.get("round"), replay.get("columns_replayed"),
             replay.get("terms_replayed"), replay.get("candidate_hit_terms"),
             replay.get("target_terms"), replay.get("verification_failures")) ==
            (950, 563_342, 57_278_657, 1_363, 2, 0), "final replay census")
    output = {
        "schema": "KRENN_AFFINE251_D12_ROUND950_FIVE_STAGE_CHAIN_AUDIT_V1",
        "status": "PASS_EXACT_FULLY_TELEMETERED_ROUND950_CHAIN",
        "scope": "Accepted round850 portfolio through exact rounds851-950; no provider run, elimination, or round951 continuation.",
        "input_audit": input_audit, "round_interval": [851, 950], "round_records": 100,
        "start_columns": 461_464, "final_columns": 563_342,
        "new_columns_total": 101_878, "final_support": 518,
        "final_candidate_target_coefficient": checkpoints[-1]["target_coefficient"],
        "stage_summaries": stage_summaries, "checkpoint_edges": checkpoint_edges,
        "cache_edges": cache_edges, "resource_provenance": telemetry,
        "aggregate_resource_gate": {"status": "PASS", "native_elapsed_seconds_sum": native_wall,
                                    "watchdog_elapsed_seconds_sum": watched_wall,
                                    "required_wall_seconds_less_than": 540,
                                    "maximum_peak_rss_kib": maximum_rss,
                                    "rss_limit_kib": RSS_LIMIT_KIB},
        "final_all_column_replay": replay, "artifact_sha256": hashes,
        "verdict_note": ("The five-stage chain and all resource evidence pass. Round950 remains "
                         "INCOMPLETE_SEARCH_CAP/ROUND_CAP, not a terminal global dual."),
    }
    atomic_json(AUDIT / "results_round950_chain_audit.json", output)


if __name__ == "__main__":
    main()

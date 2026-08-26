#!/usr/bin/env python3
"""Independent no-gap audit of D12 stages round749→849, without continuation."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRODUCER = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24"
PRODUCTION = PRODUCER / "production_from_round749"
AUDIT = Path(__file__).resolve().parent
FORMAT_SOURCE = (ROOT / "computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24"
                 / "audit_stage01.py")
STAGE01_AUDIT = (ROOT / "computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24"
                 / "results_stage01_audit.json")
STAGE02_AUDIT = (ROOT / "computations/unaudited-codex-n8-affine251-d12-stage02-audit-2026-08-24"
                 / "results_stage02_audit.json")
START = PRODUCER / "control_hierarchical_v2"
RSS_LIMIT_KIB = 36 * 1024 * 1024
EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

EXPECTED = {
    "format_source": "976dba4bb45d5ae59d9e1350f5231b487f7a2bfb9495db9de0f7585666051b67",
    "stage01_audit": "f446154cd0b18cd9d2cc2c7c8891e90e3f693d614e5debb05a582ee25f90ceea",
    "stage02_audit": "1d85aea17068ab7ea406575e06b9c144a9dd9c0ee594dc1cbb6eb3a939668f12",
    "round749_checkpoint": "dda7fb5100adfcc24264993899ec2404a3beec0e0f1e96b4f3dd83a2be7d8621",
    "round749_vectors": "93e3eeee9d7a356b4caaf59cae5c5b6671e64508004b448895d0296db0bd2bf1",
    "stage01_result": "e1f6ab7d31f84de44d4b2cee1b156fa6f924cce7e736b680323801d31e6f153d",
    "stage01_checkpoint": "d8463c5aba89f3dde57ed9c92d57a4a8fb11fb2585a504b8e3b7f71078610345",
    "stage01_vectors": "805a5bb3194f146c38a10483203a72847728d1178feca01d835e415dcd6607e5",
    "stage02_result": "5d0d27971f8ddcb11f9e03e96afca5b952b6548e5dcf2de6bc682792b1facc1f",
    "stage02_checkpoint": "7cd46995e665591116cbb0f99fc087cd47688229082e55b92cdabeb7f2546415",
    "stage02_vectors": "c00f86587df398f59476b2fd3478b9ed1e449a65ecd8400ce6a711d68e380e57",
    "stage02_watchdog": "c44df39a18b4e37f2d82b4d96d5ecea1e57486addec45ad9e73e84e311960a25",
    "stage03_result": "37c66605e3fc55c37d25445eae9c46773ccee280d69cf07071dcddf9ce319f53",
    "stage03_checkpoint": "63c48ef7beb77c022d73c9d5912b191e414faab7c33608277f52deb57766e452",
    "stage03_vectors": "b9c2ab1382cfb1e3bcbeb2f814e384ecace292d8a06a45a136da9024d467de51",
    "stage03_watchdog": "fda7a511a221ebdc4f134730c4152467813c55edd87950cc97073a7d6c3e299e",
    "stage03_stderr": "1f5ae98c59e60f42d81333d3c4e4ede138cc892d2d99d8b1683390d39ac00ad2",
    "stage04_result": "ee0764c6496a9837024443c0fdcd6322b5fcba4770e015eaacf34188455832a7",
    "stage04_checkpoint": "ce87c58cf79ddebbc0f9ce39eb36f08b6bf85a8f0f764f7728c3565da13fab49",
    "stage04_vectors": "040b1b59bad7693fbd7ed71d8ff9f760b39b30943c77f452eae3b4047b5ac254",
    "stage04_watchdog": "80284d050ca6cd51e7c14b4d3dfd6ca53dcc0c2a51208a8c5ef7e63df78ebddf",
    "stage04_stderr": "ddcc145e5d43ac7928b601aad7f4c803586e3cdf7aa86fd451a965cb8cfc5a26",
    "native_source": "173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a",
    "native_binary": "8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a",
    "watchdog_v2": "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97",
    "final_replay": "a2ea0f27800bf2d46b0367cf6e7eb5a9dba93af74f2d9400bd4a772cbc60046c",
}

STAGES = [
    {"name": "stage01", "input_round": 749, "input_columns": 334_298,
     "output_round": 778, "output_columns": 368_432, "support": 556,
     "record_count": 29, "status": "INCOMPLETE_RESOURCE_GATE", "reason": "WALL_CAP"},
    {"name": "stage02", "input_round": 778, "input_columns": 368_432,
     "output_round": 805, "output_columns": 405_259, "support": 518,
     "record_count": 27, "status": "INCOMPLETE_RESOURCE_GATE", "reason": "WALL_CAP"},
    {"name": "stage03", "input_round": 805, "input_columns": 405_259,
     "output_round": 829, "output_columns": 442_452, "support": 556,
     "record_count": 24, "status": "INCOMPLETE_RESOURCE_GATE", "reason": "WALL_CAP"},
    {"name": "stage04", "input_round": 829, "input_columns": 442_452,
     "output_round": 849, "output_columns": 460_676, "support": 312,
     "record_count": 20, "status": "INCOMPLETE_SEARCH_CAP", "reason": "ROUND_CAP"},
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


def validate_stage_result(spec: dict) -> tuple[dict, list[dict]]:
    path = PRODUCTION / spec["name"] / "result.json"
    result = json.loads(path.read_text())
    require(result.get("schema") == "KRENN_AFFINE251_D12_NATIVE_SPARSE_DUAL_V1",
            spec["name"] + " result schema")
    require((result.get("status"), result.get("incomplete_reason")) ==
            (spec["status"], spec["reason"]), spec["name"] + " status")
    require((result.get("degree"), result.get("prime"), result.get("group_order")) ==
            (12, 1_073_741_827, 1440), spec["name"] + " math header")
    require((result.get("provider_equations"), result.get("provider_terms_parsed"),
             result.get("provider_distinct_terms")) == (6561, 688908, 688906),
            spec["name"] + " provider census")
    require((result.get("workers"), result.get("pivot_mode"), result.get("strategy"),
             result.get("elimination_kernel"), result.get("incremental_basis")) ==
            (16, "rare", "cold", "hierarchical", False), spec["name"] + " mode")
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
    require(isinstance(rounds, list) and len(rounds) == spec["record_count"],
            spec["name"] + " record count")
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
    return {"round_start": rounds[0]["round"], "round_end": rounds[-1]["round"],
            "records": len(rounds), "input_columns": spec["input_columns"],
            "output_columns": spec["output_columns"],
            "new_columns": spec["output_columns"] - spec["input_columns"],
            "support": spec["support"], "status": result["status"],
            "incomplete_reason": result["incomplete_reason"]}, rounds


def command_value(command: list[str], flag: str) -> str:
    positions = [index for index, item in enumerate(command) if item == flag]
    require(len(positions) == 1 and positions[0] + 1 < len(command), flag + " command")
    return command[positions[0] + 1]


def validate_watchdog(stage: str, expected_peak: int, expected_samples: int,
                      result_sha: str, stderr_sha: str) -> dict:
    directory = PRODUCTION / stage
    telemetry = json.loads((directory / "watchdog.json").read_text())
    require(telemetry.get("schema") == "KRENN_AFFINE251_D12_MACOS_RSS_WATCHDOG_V2" and
            telemetry.get("status") == "PASS", stage + " watchdog status")
    require(telemetry.get("breach") is None and telemetry.get("returncode") == 0,
            stage + " natural exit")
    require((telemetry.get("source_sha256"), telemetry.get("binary_sha256"),
             telemetry.get("watchdog_sha256")) ==
            (EXPECTED["native_source"], EXPECTED["native_binary"], EXPECTED["watchdog_v2"]),
            stage + " invocation pins")
    require((telemetry.get("rss_observer"), telemetry.get("rss_limit_kib"),
             telemetry.get("contract_rss_limit_kib"), telemetry.get("wall_limit_seconds"),
             telemetry.get("poll_seconds")) ==
            ("libproc_PROC_PIDTASKINFO", RSS_LIMIT_KIB, RSS_LIMIT_KIB, 105, 0.25),
            stage + " watcher contract")
    command = telemetry.get("command")
    require(command_value(command, "--output") ==
            str((directory / "result.json").relative_to(ROOT)) and
            command_value(command, "--checkpoint") ==
            str((directory / "checkpoint.bin").relative_to(ROOT)) and
            command_value(command, "--vector-cache") ==
            str((directory / "vectors.bin").relative_to(ROOT)),
            stage + " output command paths")
    fixed = {"--prime": "1073741827", "--wall-seconds": "95", "--rss-gib": "36",
             "--workers": "16", "--pivot": "rare", "--strategy": "cold",
             "--elimination": "hierarchical", "--incremental": "no",
             "--portfolio-period": "256", "--portfolio-parallel": "yes",
             "--support-cap": "100000", "--column-cap": "1000000", "--round-cap": "849"}
    require(all(command_value(command, flag) == expected for flag, expected in fixed.items()),
            stage + " frozen command")
    samples = telemetry.get("samples")
    require(isinstance(samples, list) and len(samples) == telemetry.get("sample_count") ==
            expected_samples, stage + " sample census")
    previous = -1.0
    for sample in samples:
        require(sample.get("elapsed_seconds", -1) > previous, stage + " sample order")
        previous = sample["elapsed_seconds"]
        require(isinstance(sample.get("rss_kib"), int) and
                0 <= sample["rss_kib"] < RSS_LIMIT_KIB, stage + " RSS cap")
        require(sample.get("process_group_members", 0) >= 1, stage + " live member")
    peak = max(sample["rss_kib"] for sample in samples)
    require(peak == telemetry.get("peak_rss_kib") == expected_peak, stage + " peak RSS")
    require(telemetry.get("last_successful_rss_sample") == samples[-1],
            stage + " last sample")
    exit_gap = telemetry["elapsed_seconds"] - samples[-1]["elapsed_seconds"]
    require(0 <= exit_gap <= 0.35, stage + " exit observation gap")
    require(telemetry.get("atomic_outputs_clean") is True and
            telemetry.get("quarantined_abort_paths") == [], stage + " atomic outputs")
    require((telemetry.get("result_sha256"), telemetry.get("stderr_sha256"),
             telemetry.get("stdout_sha256")) == (result_sha, stderr_sha, EMPTY_SHA),
            stage + " telemetry hashes")
    temporary = [directory / (name + ".tmp") for name in
                 ("result.json", "checkpoint.bin", "vectors.bin", "stdout.log", "stderr.log")]
    require(not any(path.exists() for path in temporary), stage + " temporary output")
    return {"status": "PASS", "sample_count": len(samples), "peak_rss_kib": peak,
            "rss_limit_kib": RSS_LIMIT_KIB, "last_sample_to_exit_gap_seconds": exit_gap,
            "breach": None, "returncode": 0, "atomic_outputs_clean": True}


def validate_composed_prior_audits() -> dict:
    stage01 = json.loads(STAGE01_AUDIT.read_text())
    stage02 = json.loads(STAGE02_AUDIT.read_text())
    require(stage01.get("status") == "PASS_ALGEBRAIC_STATE_REJECT_RESOURCE_PROVENANCE" and
            stage01.get("algebraic_state", {}).get("verdict") == "PASS_EXACT_RESUMABLE_STATE" and
            stage01.get("resource_provenance", {}).get("verdict") ==
            "REJECT_QUARANTINE_RESOURCE_PROVENANCE", "stage01 split verdict")
    require(stage02.get("status") == "PASS_EXACT_FULLY_TELEMETERED_RESUMABLE_STATE",
            "stage02 audit verdict")
    return {"stage01": {"algebraic": "PASS_EXACT_RESUMABLE_STATE",
                        "resource_provenance": "REJECT_QUARANTINE_RESOURCE_PROVENANCE"},
            "stage02": "PASS_EXACT_FULLY_TELEMETERED_RESUMABLE_STATE"}


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush(); os.fsync(stream.fileno())
    os.replace(temporary, path)


def main() -> None:
    small_artifacts = {
        "stage01_audit": STAGE01_AUDIT, "stage02_audit": STAGE02_AUDIT,
        "stage03_result": PRODUCTION / "stage03/result.json",
        "stage03_checkpoint": PRODUCTION / "stage03/checkpoint.bin",
        "stage03_watchdog": PRODUCTION / "stage03/watchdog.json",
        "stage03_stderr": PRODUCTION / "stage03/stderr.log",
        "stage04_result": PRODUCTION / "stage04/result.json",
        "stage04_checkpoint": PRODUCTION / "stage04/checkpoint.bin",
        "stage04_watchdog": PRODUCTION / "stage04/watchdog.json",
        "stage04_stderr": PRODUCTION / "stage04/stderr.log",
        "native_source": PRODUCER / "sealed_v3/main.rs",
        "native_binary": PRODUCER / "sealed_v3/sparse_d12_dual",
        "watchdog_v2": PRODUCER / "sealed_watchdog_v2/run_with_macos_rss_watchdog_v2.py",
        "final_replay": AUDIT / "results_round849_cache_replay.json",
    }
    hashes = {label: pinned(path, label) for label, path in small_artifacts.items()}
    # Big cache hashes are independently pinned once here; prior stage01/stage02
    # audit results already pin their respective caches.
    hashes["stage03_vectors"] = pinned(PRODUCTION / "stage03/vectors.bin", "stage03_vectors")
    hashes["stage04_vectors"] = pinned(PRODUCTION / "stage04/vectors.bin", "stage04_vectors")
    prior = validate_composed_prior_audits()
    format_referee = load_format_referee()
    checkpoints = [format_referee.parse_checkpoint(START / "checkpoint.bin")]
    checkpoints += [format_referee.parse_checkpoint(PRODUCTION / spec["name"] / "checkpoint.bin")
                    for spec in STAGES]
    expected_headers = [(749, 334_298, 418), (778, 368_432, 556),
                        (805, 405_259, 518), (829, 442_452, 556),
                        (849, 460_676, 312)]
    for checkpoint, expected in zip(checkpoints, expected_headers):
        require((checkpoint["round"], len(checkpoint["columns"]), checkpoint["support"]) ==
                expected, "checkpoint chain header")
        require(checkpoint["target_coefficient"] == 1, "checkpoint target coefficient")
    checkpoint_edges = []
    for left, right in zip(checkpoints, checkpoints[1:]):
        old = set(left["columns"]); new = set(right["columns"])
        require(old <= new and len(new - old) == len(new) - len(old),
                "checkpoint no-gap descendant")
        checkpoint_edges.append({"input_round": left["round"], "output_round": right["round"],
                                 "input_columns_preserved": len(old),
                                 "new_columns": len(new) - len(old)})
    stage_summaries = []
    all_rounds = []
    for spec in STAGES:
        summary, rounds = validate_stage_result(spec)
        stage_summaries.append(summary); all_rounds.extend(rounds)
    require([record["round"] for record in all_rounds] == list(range(750, 850)),
            "100-round no-gap sequence")
    columns = 334_298
    for record in all_rounds:
        columns += record["new_columns"]
        require(record["columns"] == columns, "cross-stage column recurrence")
    require(columns == 460_676 and sum(record["new_columns"] for record in all_rounds) == 126_378,
            "100-round aggregate census")
    # stage01→02 was exhaustively scanned and sealed by the pinned stage02 audit.
    stage02_prior = json.loads(STAGE02_AUDIT.read_text())
    edge12 = stage02_prior["vector_descendant"]
    require((edge12["input_records_preserved_byte_identically"], edge12["new_records"]) ==
            (368_432, 36_827), "sealed stage01-to02 cache edge")
    cache_edges = [{"input_stage": "stage01", "output_stage": "stage02", **edge12}]
    for old_name, new_name, old_count, new_count in [
            ("stage02", "stage03", 405_259, 442_452),
            ("stage03", "stage04", 442_452, 460_676)]:
        edge = compare_vector_descendant(format_referee,
                                         PRODUCTION / old_name / "vectors.bin",
                                         PRODUCTION / new_name / "vectors.bin",
                                         old_count, new_count)
        cache_edges.append({"input_stage": old_name, "output_stage": new_name, **edge})
    telemetry = {
        "stage01": {"verdict": "REJECT_QUARANTINE_RESOURCE_PROVENANCE",
                    "reason": "No watchdog telemetry; algebraic state separately accepted."},
        "stage02": validate_watchdog("stage02", 7_687_664, 387,
                                     EXPECTED["stage02_result"],
                                     "47e49f02185cca6b431547a9892193b705db0a307c9543201553d4db28d2baae"),
        "stage03": validate_watchdog("stage03", 7_230_160, 387,
                                     EXPECTED["stage03_result"], EXPECTED["stage03_stderr"]),
        "stage04": validate_watchdog("stage04", 7_942_672, 306,
                                     EXPECTED["stage04_result"], EXPECTED["stage04_stderr"]),
    }
    replay = json.loads((AUDIT / "results_round849_cache_replay.json").read_text())
    require(replay.get("schema") == "KRENN_AFFINE251_D12_CACHE_REPLAY_V1" and
            replay.get("status") == "PASS_ALL_COLUMNS", "final replay status")
    require((replay.get("round"), replay.get("columns_replayed"),
             replay.get("terms_replayed"), replay.get("candidate_hit_terms"),
             replay.get("target_terms"), replay.get("verification_failures")) ==
            (849, 460_676, 46_796_079, 800, 2, 0), "final replay census")
    output = {
        "schema": "KRENN_AFFINE251_D12_ROUND849_FOUR_STAGE_CHAIN_AUDIT_V1",
        "status": "PASS_EXACT_ROUND849_CHAIN_WITH_STAGE01_RESOURCE_CAVEAT",
        "scope": "Exact round749-to849 persisted chain; no provider run, elimination, or round850 continuation.",
        "round_interval": [750, 849], "round_records": 100,
        "start_columns": 334_298, "final_columns": 460_676,
        "new_columns_total": 126_378, "final_support": 312,
        "final_candidate_target_coefficient": checkpoints[-1]["target_coefficient"],
        "prior_audit_composition": prior, "stage_summaries": stage_summaries,
        "checkpoint_edges": checkpoint_edges, "cache_edges": cache_edges,
        "resource_provenance": telemetry, "final_all_column_replay": replay,
        "artifact_sha256": hashes,
        "verdict_note": ("The algebraic chain is exact and resumable through round849. Stages02-04 "
                         "are fully telemetered PASS; stage01 retains its non-retroactive resource/"
                         "provenance quarantine. Round849 is INCOMPLETE_SEARCH_CAP/ROUND_CAP, not a "
                         "terminal global dual."),
    }
    atomic_json(AUDIT / "results_round849_chain_audit.json", output)


if __name__ == "__main__":
    main()

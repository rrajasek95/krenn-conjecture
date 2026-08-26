#!/usr/bin/env python3
"""Fail-closed, read-only audit of supplied D12 stage02 (round778→805)."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRODUCER = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24"
INPUT = PRODUCER / "production_from_round749/stage01"
STAGE = PRODUCER / "production_from_round749/stage02"
AUDIT = Path(__file__).resolve().parent
PREVIOUS_AUDIT = ROOT / "computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24"
REPLAY_BINARY = (ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-integration-audit-2026-08-24"
                 / "target/release/d12-hierarchical-integration-audit")
PROVIDER = (ROOT / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22"
            / "canonical_triangle_pair_offdiag_full_p1073741827.ms")

INPUT_ROUND = 778
INPUT_COLUMNS = 368_432
OUTPUT_ROUND = 805
OUTPUT_COLUMNS = 405_259
OUTPUT_SUPPORT = 518
RSS_LIMIT_KIB = 36 * 1024 * 1024
EXPECTED = {
    "input_checkpoint": "d8463c5aba89f3dde57ed9c92d57a4a8fb11fb2585a504b8e3b7f71078610345",
    "input_vectors": "805a5bb3194f146c38a10483203a72847728d1178feca01d835e415dcd6607e5",
    "stage_result": "5d0d27971f8ddcb11f9e03e96afca5b952b6548e5dcf2de6bc682792b1facc1f",
    "stage_checkpoint": "7cd46995e665591116cbb0f99fc087cd47688229082e55b92cdabeb7f2546415",
    "stage_vectors": "c00f86587df398f59476b2fd3478b9ed1e449a65ecd8400ce6a711d68e380e57",
    "stage_stderr": "47e49f02185cca6b431547a9892193b705db0a307c9543201553d4db28d2baae",
    "stage_stdout": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "stage_watchdog": "c44df39a18b4e37f2d82b4d96d5ecea1e57486addec45ad9e73e84e311960a25",
    "native_source": "173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a",
    "native_binary": "8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a",
    "watchdog_v2": "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97",
    "provider": "daa427528bbbeece064b09396023b66f32b804ba6d304178d19ced13e9b38a4e",
    "previous_audit_source": "976dba4bb45d5ae59d9e1350f5231b487f7a2bfb9495db9de0f7585666051b67",
    "replay_binary": "8d20a62772748db2dee47b651acbab738b90f4bc40ef531001b66396010ec639",
    "cache_replay": "404f67b3178c187d23381d1972e7cc3cbfc793fb5abc616ad218d4d962b0443d",
}


def load_format_referee():
    source = PREVIOUS_AUDIT / "audit_stage01.py"
    require(sha256(source) == EXPECTED["previous_audit_source"], "format referee source SHA")
    spec = importlib.util.spec_from_file_location("stage01_format_referee", source)
    require(spec is not None and spec.loader is not None, "format referee import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def compare_vector_descendant(format_referee) -> dict:
    with (INPUT / "vectors.bin").open("rb") as old, (STAGE / "vectors.bin").open("rb") as new:
        old_header = format_referee.vector_header(old, "stage01 cache")
        new_header = format_referee.vector_header(new, "stage02 cache")
        require(old_header["count"] == INPUT_COLUMNS, "stage01 cache count")
        require(new_header["count"] == OUTPUT_COLUMNS, "stage02 cache count")
        require(old_header["provider_fingerprint"] == new_header["provider_fingerprint"],
                "provider fingerprint drift")
        old_record = format_referee.vector_record(old, "stage01 cache record")
        new_record = format_referee.vector_record(new, "stage02 cache record")
        matched = extras = 0
        while old_record is not None:
            require(new_record is not None, "stage02 cache lost stage01 suffix")
            if new_record[0] < old_record[0]:
                extras += 1
                new_record = format_referee.vector_record(new, "stage02 cache record")
            elif new_record[0] == old_record[0]:
                require(new_record[1] == old_record[1], "persisted vector record changed")
                matched += 1
                old_record = format_referee.vector_record(old, "stage01 cache record")
                new_record = format_referee.vector_record(new, "stage02 cache record")
            else:
                raise Reject("stage02 cache omitted stage01 record")
        while new_record is not None:
            extras += 1
            new_record = format_referee.vector_record(new, "stage02 cache record")
        require(old.read(1) == b"" and new.read(1) == b"", "cache trailing bytes")
    require((matched, extras) == (INPUT_COLUMNS, OUTPUT_COLUMNS - INPUT_COLUMNS),
            "cache descendant census")
    return {
        "input_records_preserved_byte_identically": matched,
        "new_records": extras,
        "provider_fingerprint": new_header["provider_fingerprint"],
        "input_vector_fingerprint": old_header["vector_fingerprint"],
        "output_vector_fingerprint": new_header["vector_fingerprint"],
    }


def validate_result() -> dict:
    result = json.loads((STAGE / "result.json").read_text())
    require(result.get("schema") == "KRENN_AFFINE251_D12_NATIVE_SPARSE_DUAL_V1",
            "result schema")
    require((result.get("status"), result.get("incomplete_reason")) ==
            ("INCOMPLETE_RESOURCE_GATE", "WALL_CAP"), "result status")
    require((result.get("degree"), result.get("prime"), result.get("group_order")) ==
            (12, 1_073_741_827, 1440), "mathematical header")
    require((result.get("provider_equations"), result.get("provider_terms_parsed"),
             result.get("provider_distinct_terms")) == (6561, 688908, 688906),
            "provider census")
    require((result.get("workers"), result.get("pivot_mode"), result.get("strategy"),
             result.get("elimination_kernel"), result.get("incremental_basis")) ==
            (16, "rare", "cold", "hierarchical", False), "native mode")
    require(result.get("portfolio_period") == 256 and
            result.get("portfolio_parallel") is True, "portfolio mode")
    require((result.get("support_cap"), result.get("column_cap"),
             result.get("wall_limit_seconds"), result.get("rss_limit_gib")) ==
            (100000, 1000000, 95, 36), "resource fields")
    require((result.get("rounds_completed"), result.get("column_orbits_exposed"),
             result.get("dual_support"), result.get("cached_vectors_loaded"),
             result.get("vectors_materialized_on_restore")) ==
            (OUTPUT_ROUND, OUTPUT_COLUMNS, OUTPUT_SUPPORT, INPUT_COLUMNS, 0),
            "terminal census")
    require(result.get("global_annihilation") is None and
            result.get("target_pairing") is None, "incomplete terminal claims")
    require(result.get("vector_cache_bytes") == (STAGE / "vectors.bin").stat().st_size,
            "cache byte count")
    rounds = result.get("rounds")
    require(isinstance(rounds, list) and len(rounds) == OUTPUT_ROUND - INPUT_ROUND,
            "27-round chain length")
    columns = INPUT_COLUMNS
    for index, record in enumerate(rounds):
        require(record.get("round") == INPUT_ROUND + index + 1, "round continuity")
        added = record.get("new_columns")
        require(isinstance(added, int) and added > 0, "new columns")
        columns += added
        require(record.get("columns") == columns, "column recurrence")
        require(record.get("selected_strategy") == "cold" and
                record.get("selected_pivot") == "rare", "round mode")
        require(isinstance(record.get("dual_support"), int) and
                record["dual_support"] > 0, "round support")
        for timer in ("incident_seconds", "materialize_seconds", "solve_seconds"):
            require(isinstance(record.get(timer), (int, float)) and
                    math.isfinite(record[timer]) and record[timer] >= 0, "round timer")
    require(columns == OUTPUT_COLUMNS and rounds[-1]["dual_support"] == OUTPUT_SUPPORT,
            "terminal round")
    require(sum(record["new_columns"] for record in rounds) ==
            OUTPUT_COLUMNS - INPUT_COLUMNS, "new-column sum")
    require(result.get("elapsed_seconds", 0) >= 95, "native wall gate consistency")
    return {"status": result["status"], "incomplete_reason": result["incomplete_reason"],
            "round_start": 779, "round_end": 805, "round_records": len(rounds),
            "new_columns_sum": OUTPUT_COLUMNS - INPUT_COLUMNS,
            "elapsed_seconds": result["elapsed_seconds"]}


def value(command: list[str], flag: str) -> str:
    positions = [index for index, item in enumerate(command) if item == flag]
    require(len(positions) == 1 and positions[0] + 1 < len(command), "command " + flag)
    return command[positions[0] + 1]


def validate_watchdog() -> dict:
    telemetry = json.loads((STAGE / "watchdog.json").read_text())
    require(telemetry.get("schema") == "KRENN_AFFINE251_D12_MACOS_RSS_WATCHDOG_V2" and
            telemetry.get("status") == "PASS", "watchdog status")
    require(telemetry.get("breach") is None and telemetry.get("returncode") == 0,
            "natural child exit")
    require(telemetry.get("source_sha256") == EXPECTED["native_source"] and
            telemetry.get("binary_sha256") == EXPECTED["native_binary"] and
            telemetry.get("watchdog_sha256") == EXPECTED["watchdog_v2"],
            "watchdog invocation pins")
    require(telemetry.get("rss_observer") == "libproc_PROC_PIDTASKINFO",
            "RSS observer")
    require((telemetry.get("rss_limit_kib"), telemetry.get("contract_rss_limit_kib")) ==
            (RSS_LIMIT_KIB, RSS_LIMIT_KIB), "RSS limit")
    require(telemetry.get("wall_limit_seconds") == 105 and
            telemetry.get("poll_seconds") == 0.25, "wrapper timing contract")
    command = telemetry.get("command")
    require(isinstance(command, list) and command[0] == str((PRODUCER / "sealed_v3/sparse_d12_dual").relative_to(ROOT)),
            "command binary")
    expected_values = {
        "--input": str(PROVIDER.relative_to(ROOT)),
        "--output": str((STAGE / "result.json").relative_to(ROOT)),
        "--checkpoint": str((STAGE / "checkpoint.bin").relative_to(ROOT)),
        "--vector-cache": str((STAGE / "vectors.bin").relative_to(ROOT)),
        "--dual": str((STAGE / "dual.tsv").relative_to(ROOT)),
        "--prime": "1073741827", "--wall-seconds": "95", "--rss-gib": "36",
        "--workers": "16", "--pivot": "rare", "--strategy": "cold",
        "--elimination": "hierarchical", "--incremental": "no",
        "--portfolio-period": "256", "--portfolio-parallel": "yes",
        "--support-cap": "100000", "--column-cap": "1000000", "--round-cap": "849",
    }
    require(all(value(command, flag) == expected for flag, expected in expected_values.items()),
            "frozen command")
    samples = telemetry.get("samples")
    require(isinstance(samples, list) and len(samples) == telemetry.get("sample_count") == 387,
            "RSS sample census")
    previous = -1.0
    for sample in samples:
        elapsed = sample.get("elapsed_seconds")
        rss = sample.get("rss_kib")
        require(isinstance(elapsed, (int, float)) and elapsed > previous,
                "RSS sample time order")
        require(isinstance(rss, int) and 0 <= rss < RSS_LIMIT_KIB,
                "RSS sample below cap")
        require(isinstance(sample.get("process_group_members"), int) and
                sample["process_group_members"] >= 1, "observed child membership")
        previous = elapsed
    peak = max(sample["rss_kib"] for sample in samples)
    require(peak == telemetry.get("peak_rss_kib") == 7_687_664, "RSS peak")
    require(telemetry.get("last_successful_rss_sample") == samples[-1],
            "terminal RSS sample")
    gap = telemetry.get("elapsed_seconds") - samples[-1]["elapsed_seconds"]
    require(0 <= gap <= 0.35, "natural-exit observation gap")
    require(telemetry.get("atomic_outputs_clean") is True and
            telemetry.get("quarantined_abort_paths") == [], "atomic output status")
    require(telemetry.get("result_sha256") == EXPECTED["stage_result"] and
            telemetry.get("stderr_sha256") == EXPECTED["stage_stderr"] and
            telemetry.get("stdout_sha256") == EXPECTED["stage_stdout"],
            "telemetry artifact hashes")
    temporary_paths = [
        STAGE / "result.json.tmp", STAGE / "checkpoint.bin.tmp", STAGE / "vectors.bin.tmp",
        STAGE / "stdout.log.tmp", STAGE / "stderr.log.tmp",
    ]
    require(not any(path.exists() for path in temporary_paths), "temporary output remains")
    return {"status": "PASS_FULL_TELEMETRY", "sample_count": len(samples),
            "peak_rss_kib": peak, "rss_limit_kib": RSS_LIMIT_KIB,
            "last_sample_elapsed_seconds": samples[-1]["elapsed_seconds"],
            "child_exit_elapsed_seconds": telemetry["elapsed_seconds"],
            "last_sample_to_exit_gap_seconds": gap,
            "atomic_outputs_clean": True, "breach": None, "returncode": 0}


def validate_replay() -> dict:
    replay = json.loads((AUDIT / "results_stage02_cache_replay.json").read_text())
    require(replay.get("schema") == "KRENN_AFFINE251_D12_CACHE_REPLAY_V1" and
            replay.get("status") == "PASS_ALL_COLUMNS", "cache replay status")
    require((replay.get("round"), replay.get("columns_replayed"),
             replay.get("verification_failures")) ==
            (OUTPUT_ROUND, OUTPUT_COLUMNS, 0), "cache replay census")
    require(isinstance(replay.get("terms_replayed"), int) and
            replay["terms_replayed"] > OUTPUT_COLUMNS, "cache term census")
    require(isinstance(replay.get("candidate_hit_terms"), int) and
            replay["candidate_hit_terms"] > 0, "candidate cache incidence")
    return replay


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def main() -> None:
    artifacts = {
        "input_checkpoint": INPUT / "checkpoint.bin", "input_vectors": INPUT / "vectors.bin",
        "stage_result": STAGE / "result.json", "stage_checkpoint": STAGE / "checkpoint.bin",
        "stage_vectors": STAGE / "vectors.bin", "stage_stderr": STAGE / "stderr.log",
        "stage_stdout": STAGE / "stdout.log", "stage_watchdog": STAGE / "watchdog.json",
        "native_source": PRODUCER / "sealed_v3/main.rs",
        "native_binary": PRODUCER / "sealed_v3/sparse_d12_dual",
        "watchdog_v2": PRODUCER / "sealed_watchdog_v2/run_with_macos_rss_watchdog_v2.py",
        "provider": PROVIDER, "previous_audit_source": PREVIOUS_AUDIT / "audit_stage01.py",
        "replay_binary": REPLAY_BINARY,
        "cache_replay": AUDIT / "results_stage02_cache_replay.json",
    }
    hashes = {label: pinned(path, label) for label, path in artifacts.items()}
    format_referee = load_format_referee()
    input_checkpoint = format_referee.parse_checkpoint(INPUT / "checkpoint.bin")
    output_checkpoint = format_referee.parse_checkpoint(STAGE / "checkpoint.bin")
    require((input_checkpoint["round"], len(input_checkpoint["columns"])) ==
            (INPUT_ROUND, INPUT_COLUMNS), "input checkpoint census")
    require((output_checkpoint["round"], len(output_checkpoint["columns"]),
             output_checkpoint["support"], output_checkpoint["target_coefficient"]) ==
            (OUTPUT_ROUND, OUTPUT_COLUMNS, OUTPUT_SUPPORT, 1), "output checkpoint census")
    input_columns = set(input_checkpoint["columns"])
    output_columns = set(output_checkpoint["columns"])
    require(input_columns <= output_columns and
            len(output_columns - input_columns) == OUTPUT_COLUMNS - INPUT_COLUMNS,
            "checkpoint exact input descendant")
    result_chain = validate_result()
    vector_descendant = compare_vector_descendant(format_referee)
    replay = validate_replay()
    telemetry = validate_watchdog()
    output = {
        "schema": "KRENN_AFFINE251_D12_STAGE02_FULL_AUDIT_V1",
        "status": "PASS_EXACT_FULLY_TELEMETERED_RESUMABLE_STATE",
        "scope": "Supplied round778-to805 stage only; no provider run, elimination, or continuation.",
        "round": OUTPUT_ROUND, "columns": OUTPUT_COLUMNS, "support": OUTPUT_SUPPORT,
        "candidate_target_coefficient": output_checkpoint["target_coefficient"],
        "checkpoint_input_columns_preserved": len(input_columns),
        "checkpoint_new_columns": len(output_columns - input_columns),
        "result_chain": result_chain, "vector_descendant": vector_descendant,
        "all_column_replay": replay, "resource_provenance": telemetry,
        "artifact_sha256": hashes,
        "verdict_note": ("This accepts an exact fully telemetered continuation checkpoint at round805; "
                         "the native result remains INCOMPLETE_RESOURCE_GATE/WALL_CAP and is not a "
                         "terminal global dual."),
    }
    atomic_json(AUDIT / "results_stage02_audit.json", output)


if __name__ == "__main__":
    main()

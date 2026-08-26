#!/usr/bin/env python3
"""Independent, fail-closed audit of the supplied D12 stage01 state.

This performs no provider evaluation, elimination, or continuation.  It checks
the native persisted formats, the exact round chain, the complete cache replay
summary, and that every round-749 cache record survives byte-for-byte in the
round-778 cache.  Resource/provenance evidence is deliberately judged apart
from algebraic state validity.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import struct


ROOT = Path(__file__).resolve().parents[2]
PRODUCER = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24"
STAGE = PRODUCER / "production_from_round749/stage01"
AUDIT = Path(__file__).resolve().parent
INPUT = PRODUCER / "control_hierarchical_v2"
INTEGRATION_AUDIT = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-integration-audit-2026-08-24"

PRIME = 1_073_741_827
TARGET = bytes([251]) * 12
CHECKPOINT_MAGIC = b"AFF12CEG1\0\0\0"
VECTOR_MAGIC = b"AFF12VEC1\0\0\0"
INPUT_ROUND = 749
INPUT_COLUMNS = 334_298
OUTPUT_ROUND = 778
OUTPUT_COLUMNS = 368_432
OUTPUT_SUPPORT = 556
EXPECTED = {
    "input_checkpoint": "dda7fb5100adfcc24264993899ec2404a3beec0e0f1e96b4f3dd83a2be7d8621",
    "input_vectors": "93e3eeee9d7a356b4caaf59cae5c5b6671e64508004b448895d0296db0bd2bf1",
    "stage_result": "e1f6ab7d31f84de44d4b2cee1b156fa6f924cce7e736b680323801d31e6f153d",
    "stage_checkpoint": "d8463c5aba89f3dde57ed9c92d57a4a8fb11fb2585a504b8e3b7f71078610345",
    "stage_vectors": "805a5bb3194f146c38a10483203a72847728d1178feca01d835e415dcd6607e5",
    "stage_stderr_tmp": "6119505476cc898c291738cb6a18d5fd778044d06c1cd810958dc79dc3713771",
    "stage_stdout_tmp": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "native_source": "173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a",
    "native_binary": "8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a",
    "cache_replay": "ad903b2b072d9935daabcfd6adcb1a374d67b3a74ee179a0f51ce122923ffb75",
    "cache_replay_binary": "8d20a62772748db2dee47b651acbab738b90f4bc40ef531001b66396010ec639",
    "watchdog_v2": "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97",
    "watchdog_v2_fixture": "575dc2a0bb6c17d8a981601c2b2d3eb371a7b157be214e207088fecb4ebf80df",
    "watchdog_v2_test": "18302cb9e42f269a5ee7dcdc72227c49f3da5856f80dcc95d96b74b169d391df",
    "watchdog_v2_hostiles": "8551887a2073f5c6ba1241f272b29381542c3bdeeb488baebb16301d2d315693",
}


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
    require(actual == EXPECTED[label], f"{label} SHA")
    return actual


def exact(stream, size: int, label: str) -> bytes:
    value = stream.read(size)
    require(len(value) == size, f"truncated {label}")
    return value


def u64(stream, label: str) -> int:
    return struct.unpack("<Q", exact(stream, 8, label))[0]


def mono(stream, degree: int, label: str) -> bytes:
    actual_degree = exact(stream, 1, label + " degree")[0]
    ids = exact(stream, 12, label + " ids")
    require(actual_degree == degree, label + " degree")
    require(all(ids[index] <= ids[index + 1] for index in range(degree - 1)),
            label + " canonical")
    require(ids[degree:] == bytes(12 - degree), label + " padding")
    return ids[:degree]


def parse_checkpoint(path: Path) -> dict:
    with path.open("rb") as stream:
        require(exact(stream, 12, "checkpoint magic") == CHECKPOINT_MAGIC,
                "checkpoint schema magic")
        prime, round_index, count, support = (
            u64(stream, "prime"), u64(stream, "round"),
            u64(stream, "count"), u64(stream, "support"))
        require(prime == PRIME, "checkpoint prime")
        columns = []
        previous = None
        for _ in range(count):
            word = struct.unpack("<H", exact(stream, 2, "word"))[0]
            multiplier = mono(stream, 8, "column multiplier")
            key = (word, multiplier)
            require(word < 6561, "word range")
            require(previous is None or previous < key, "column total order")
            previous = key
            columns.append(key)
        candidate = {}
        previous_row = None
        for _ in range(support):
            row = mono(stream, 12, "candidate row")
            value = u64(stream, "candidate value")
            require(previous_row is None or previous_row < row,
                    "candidate total order")
            require(0 < value < PRIME and row not in candidate,
                    "candidate entry")
            previous_row = row
            candidate[row] = value
        require(stream.read(1) == b"", "checkpoint trailing bytes")
    require(candidate.get(TARGET) == 1, "candidate target coefficient")
    return {"round": round_index, "columns": columns, "support": support,
            "target_coefficient": candidate[TARGET]}


def vector_header(stream, label: str) -> dict:
    require(exact(stream, 12, label + " magic") == VECTOR_MAGIC,
            label + " schema magic")
    prime = u64(stream, label + " prime")
    provider = u64(stream, label + " provider fingerprint")
    fingerprint = u64(stream, label + " vector fingerprint")
    count = u64(stream, label + " count")
    require(prime == PRIME, label + " prime")
    return {"provider_fingerprint": provider,
            "vector_fingerprint": fingerprint, "count": count}


def vector_record(stream, label: str):
    key_bytes = stream.read(15)
    if not key_bytes:
        return None
    require(len(key_bytes) == 15, "truncated " + label + " key")
    word = struct.unpack("<H", key_bytes[:2])[0]
    require(key_bytes[2] == 8 and key_bytes[11:] == b"\0\0\0\0",
            label + " multiplier schema")
    ids = key_bytes[3:11]
    require(all(ids[i] <= ids[i + 1] for i in range(7)),
            label + " multiplier canonical")
    size_bytes = exact(stream, 8, label + " size")
    size = struct.unpack("<Q", size_bytes)[0]
    require(0 < size <= 700_000, label + " size range")
    digest = hashlib.sha256(key_bytes + size_bytes)
    remaining = size * 21
    while remaining:
        block = exact(stream, min(remaining, 8 << 20), label + " body")
        digest.update(block)
        remaining -= len(block)
    return (word, ids), digest.hexdigest()


def compare_vector_descendant(input_path: Path, output_path: Path) -> dict:
    with input_path.open("rb") as old, output_path.open("rb") as new:
        old_header = vector_header(old, "input cache")
        new_header = vector_header(new, "output cache")
        require(old_header["count"] == INPUT_COLUMNS, "input cache count")
        require(new_header["count"] == OUTPUT_COLUMNS, "output cache count")
        require(old_header["provider_fingerprint"] ==
                new_header["provider_fingerprint"], "provider fingerprint drift")
        old_record = vector_record(old, "input cache record")
        new_record = vector_record(new, "output cache record")
        matched = extras = 0
        while old_record is not None:
            require(new_record is not None, "output cache lost input suffix")
            if new_record[0] < old_record[0]:
                extras += 1
                new_record = vector_record(new, "output cache record")
            elif new_record[0] == old_record[0]:
                require(new_record[1] == old_record[1],
                        "persisted vector record changed")
                matched += 1
                old_record = vector_record(old, "input cache record")
                new_record = vector_record(new, "output cache record")
            else:
                raise Reject("output cache omitted input record")
        while new_record is not None:
            extras += 1
            new_record = vector_record(new, "output cache record")
        require(old.read(1) == b"" and new.read(1) == b"", "cache trailing bytes")
    require(matched == INPUT_COLUMNS and extras == OUTPUT_COLUMNS - INPUT_COLUMNS,
            "cache descendant census")
    return {"input_records_preserved_byte_identically": matched,
            "new_records": extras,
            "provider_fingerprint": new_header["provider_fingerprint"],
            "input_vector_fingerprint": old_header["vector_fingerprint"],
            "output_vector_fingerprint": new_header["vector_fingerprint"]}


def validate_result(path: Path) -> dict:
    result = json.loads(path.read_text())
    require(result.get("schema") == "KRENN_AFFINE251_D12_NATIVE_SPARSE_DUAL_V1",
            "result schema")
    require((result.get("status"), result.get("incomplete_reason")) ==
            ("INCOMPLETE_RESOURCE_GATE", "WALL_CAP"), "result status")
    require((result.get("degree"), result.get("prime"), result.get("group_order")) ==
            (12, PRIME, 1440), "result mathematical header")
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
            (100000, 1000000, 95, 36), "resource contract fields")
    require((result.get("rounds_completed"), result.get("column_orbits_exposed"),
             result.get("dual_support"), result.get("cached_vectors_loaded")) ==
            (OUTPUT_ROUND, OUTPUT_COLUMNS, OUTPUT_SUPPORT, INPUT_COLUMNS),
            "terminal census")
    require(result.get("global_annihilation") is None and
            result.get("target_pairing") is None, "incomplete result final claims")
    require(result.get("vectors_materialized_on_restore") == 0,
            "cache-only restore")
    require(result.get("vector_cache_bytes") == (STAGE / "vectors.bin").stat().st_size,
            "vector byte census")
    require(result.get("checkpoint") == str(STAGE.relative_to(ROOT) / "checkpoint.bin") and
            result.get("vector_cache") == str(STAGE.relative_to(ROOT) / "vectors.bin"),
            "output paths")
    rounds = result.get("rounds")
    require(isinstance(rounds, list) and len(rounds) == OUTPUT_ROUND - INPUT_ROUND,
            "29-round chain length")
    columns = INPUT_COLUMNS
    for index, record in enumerate(rounds):
        expected_round = INPUT_ROUND + index + 1
        require(record.get("round") == expected_round, "round continuity")
        added = record.get("new_columns")
        require(isinstance(added, int) and added > 0, "new-column census")
        columns += added
        require(record.get("columns") == columns, "column recurrence")
        require(record.get("selected_strategy") == "cold" and
                record.get("selected_pivot") == "rare", "round mode")
        require(isinstance(record.get("dual_support"), int) and
                record["dual_support"] > 0, "round support")
        for timer in ("incident_seconds", "materialize_seconds", "solve_seconds"):
            require(isinstance(record.get(timer), (int, float)) and
                    math.isfinite(record[timer]) and record[timer] >= 0,
                    "round timer")
    require(columns == OUTPUT_COLUMNS and rounds[-1]["dual_support"] == OUTPUT_SUPPORT,
            "terminal round consistency")
    require(sum(record["new_columns"] for record in rounds) ==
            OUTPUT_COLUMNS - INPUT_COLUMNS, "round delta sum")
    require(result.get("elapsed_seconds", 0) >= result["wall_limit_seconds"],
            "wall-gate status/timer consistency")
    return {"round_start": rounds[0]["round"], "round_end": rounds[-1]["round"],
            "round_records": len(rounds), "new_columns_sum": OUTPUT_COLUMNS - INPUT_COLUMNS,
            "elapsed_seconds": result["elapsed_seconds"],
            "native_wall_limit_seconds": result["wall_limit_seconds"]}


def validate_replay() -> dict:
    path = AUDIT / "results_stage01_cache_replay.json"
    replay = json.loads(path.read_text())
    require(replay.get("schema") == "KRENN_AFFINE251_D12_CACHE_REPLAY_V1" and
            replay.get("status") == "PASS_ALL_COLUMNS", "cache replay status")
    require((replay.get("round"), replay.get("columns_replayed"),
             replay.get("verification_failures")) ==
            (OUTPUT_ROUND, OUTPUT_COLUMNS, 0), "cache replay census")
    require(replay.get("terms_replayed") == 37_387_100 and
            replay.get("candidate_hit_terms") == 1453 and
            replay.get("target_terms") == 2, "cache replay term census")
    return replay


def validate_watchdog_v2_hostiles() -> dict:
    hostile = json.loads((PRODUCER / "results_watchdog_v2_hostiles.json").read_text())
    require(hostile.get("schema") ==
            "KRENN_AFFINE251_D12_MACOS_WATCHDOG_V2_HOSTILES_V1" and
            hostile.get("status") == "PASS", "watchdog hostile status")
    require(hostile.get("wrapper_sha256") == EXPECTED["watchdog_v2"] and
            hostile.get("fixture_sha256") == EXPECTED["watchdog_v2_fixture"],
            "watchdog hostile pins")
    records = hostile.get("records")
    require([record.get("case") for record in records] ==
            ["fast_exit", "poll_exit_race_x32", "rss_overrun"],
            "watchdog hostile cases")
    require(all(record.get("status") == "PASS" for record in records),
            "watchdog hostile verdicts")
    require(len(records[1].get("sample_counts", [])) == 32 and
            all(value > 0 for value in records[1]["sample_counts"]),
            "watchdog race samples")
    require(records[2].get("peak_rss_kib", 0) >= records[2].get("rss_limit_kib", 1) and
            records[2].get("final_output_absent") is True,
            "watchdog overrun rejection")
    return {"status": "PASS_FIXED_WRAPPER_ONLY",
            "fast_exit": True, "poll_exit_race_repeats": 32,
            "rss_overrun_rejected": True,
            "not_retroactive_to_stage01": True}


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
        "input_checkpoint": INPUT / "checkpoint.bin",
        "input_vectors": INPUT / "vectors.bin",
        "stage_result": STAGE / "result.json",
        "stage_checkpoint": STAGE / "checkpoint.bin",
        "stage_vectors": STAGE / "vectors.bin",
        "stage_stderr_tmp": STAGE / "stderr.log.tmp",
        "stage_stdout_tmp": STAGE / "stdout.log.tmp",
        "native_source": PRODUCER / "sealed_v3/main.rs",
        "native_binary": PRODUCER / "sealed_v3/sparse_d12_dual",
        "cache_replay": AUDIT / "results_stage01_cache_replay.json",
        "cache_replay_binary": INTEGRATION_AUDIT / "target/release/d12-hierarchical-integration-audit",
        "watchdog_v2": PRODUCER / "run_with_macos_rss_watchdog_v2.py",
        "watchdog_v2_fixture": PRODUCER / "watchdog_fixture.py",
        "watchdog_v2_test": PRODUCER / "test_watchdog_v2.py",
        "watchdog_v2_hostiles": PRODUCER / "results_watchdog_v2_hostiles.json",
    }
    hashes = {label: pinned(path, label) for label, path in artifacts.items()}
    result_chain = validate_result(STAGE / "result.json")
    input_checkpoint = parse_checkpoint(INPUT / "checkpoint.bin")
    output_checkpoint = parse_checkpoint(STAGE / "checkpoint.bin")
    require((input_checkpoint["round"], len(input_checkpoint["columns"])) ==
            (INPUT_ROUND, INPUT_COLUMNS), "input checkpoint census")
    require((output_checkpoint["round"], len(output_checkpoint["columns"]),
             output_checkpoint["support"]) ==
            (OUTPUT_ROUND, OUTPUT_COLUMNS, OUTPUT_SUPPORT), "output checkpoint census")
    input_columns = set(input_checkpoint["columns"])
    output_columns = set(output_checkpoint["columns"])
    require(len(input_columns) == INPUT_COLUMNS and input_columns <= output_columns,
            "checkpoint descendant relation")
    require(len(output_columns - input_columns) == OUTPUT_COLUMNS - INPUT_COLUMNS,
            "checkpoint new-column census")
    vector_descendant = compare_vector_descendant(INPUT / "vectors.bin", STAGE / "vectors.bin")
    replay = validate_replay()
    wrapper = validate_watchdog_v2_hostiles()
    expected_temporary = [STAGE / "result.json.tmp", STAGE / "checkpoint.bin.tmp",
                          STAGE / "vectors.bin.tmp"]
    require(not any(path.exists() for path in expected_temporary),
            "native output temporary remains")
    resource = {
        "verdict": "REJECT_QUARANTINE_RESOURCE_PROVENANCE",
        "watchdog_telemetry_present": (STAGE / "watchdog.json").is_file(),
        "stdout_final_present": (STAGE / "stdout.log").is_file(),
        "stderr_final_present": (STAGE / "stderr.log").is_file(),
        "stdout_tmp_present": (STAGE / "stdout.log.tmp").is_file(),
        "stderr_tmp_present": (STAGE / "stderr.log.tmp").is_file(),
        "native_peak_rss_kib": 0,
        "native_atomic_temporaries_absent": True,
        "reason": ("No watchdog.json and logs remain .tmp; therefore no artifact binds the "
                   "stage invocation to the sealed source/binary/input hashes or proves live "
                   "36-GiB observation through natural child exit. Parsed final native outputs "
                   "are clean, but that is not substitute resource telemetry."),
    }
    require(resource["watchdog_telemetry_present"] is False and
            resource["stdout_tmp_present"] and resource["stderr_tmp_present"],
            "unexpected stage01 resource evidence changed")
    audit = {
        "schema": "KRENN_AFFINE251_D12_STAGE01_SPLIT_AUDIT_V1",
        "status": "PASS_ALGEBRAIC_STATE_REJECT_RESOURCE_PROVENANCE",
        "scope": "Supplied round749-to778 stage only; no provider run, elimination, or continuation.",
        "algebraic_state": {
            "verdict": "PASS_EXACT_RESUMABLE_STATE",
            "round": OUTPUT_ROUND,
            "columns": OUTPUT_COLUMNS,
            "support": OUTPUT_SUPPORT,
            "candidate_target_coefficient": output_checkpoint["target_coefficient"],
            "checkpoint_input_columns_preserved": len(input_columns),
            "checkpoint_new_columns": len(output_columns - input_columns),
            "result_chain": result_chain,
            "vector_descendant": vector_descendant,
            "all_column_replay": replay,
        },
        "resource_provenance": resource,
        "fixed_wrapper_v2": wrapper,
        "artifact_sha256": hashes,
        "binding_note": ("The sealed source/binary hashes are verified as files and the state is "
                         "content-descended from the pinned round749 inputs. Because stage01 lacks "
                         "wrapper telemetry, those executable pins are not invocation-bound."),
    }
    atomic_json(AUDIT / "results_stage01_audit.json", audit)


if __name__ == "__main__":
    main()

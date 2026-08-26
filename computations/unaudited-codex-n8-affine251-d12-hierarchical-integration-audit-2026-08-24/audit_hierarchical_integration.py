#!/usr/bin/env python3
"""Fail-closed audit for the generic D12 hierarchical integration.

This audit never evaluates provider columns or runs an elimination.  It parses
the native checkpoint/cache formats independently, replays the candidate on
every persisted column, and checks an integration control against the sealed
round-748 state byte for byte.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import resource
import struct
import sys
import time
from pathlib import Path


PRIME = 1_073_741_827
ROUND = 748
COLUMNS = 333_199
SUPPORT = 436
TARGET = bytes([251]) * 12
PARENT_SOURCE_SHA = "241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0"
BASELINE_RESULT_SHA = "d205ff7685e10d1381f6b2b6b248ae91d2e417de0769117a3da8b8535e43b538"
BASELINE_CHECKPOINT_SHA = "fe44b33e74b7e9ce00a7654fe8f027b0024b15e464bbaa372ec85ea92bc097c6"
BASELINE_VECTORS_SHA = "7af04cecc244e158af1df5b782cbe5b2e23d191b4d06b43a1c0c33911e5c6cab"
BASELINE_VECTOR_BYTES = 717_361_393
CHECKPOINT_MAGIC = b"AFF12CEG1\0\0\0"
VECTOR_MAGIC = b"AFF12VEC1\0\0\0"
FNV_OFFSET = 14_695_981_039_346_656_037
FNV_PRIME = 1_099_511_628_211
MASK64 = (1 << 64) - 1
RSS_LIMIT_BYTES = 36 * 1024**3


class Rejection(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Rejection(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def files_equal(left: Path, right: Path) -> bool:
    if left.resolve() == right.resolve() or left.stat().st_size != right.stat().st_size:
        return left.resolve() == right.resolve()
    with left.open("rb") as a, right.open("rb") as b:
        while True:
            aa = a.read(8 << 20)
            bb = b.read(8 << 20)
            if aa != bb:
                return False
            if not aa:
                return True


def read_exact(stream, count: int, label: str) -> bytes:
    value = stream.read(count)
    require(len(value) == count, f"truncated {label}")
    return value


def read_u64(stream, label: str) -> int:
    return struct.unpack("<Q", read_exact(stream, 8, label))[0]


def read_mono(stream, expected_degree: int, label: str) -> bytes:
    degree = read_exact(stream, 1, label + " degree")[0]
    ids = read_exact(stream, 12, label + " ids")
    require(degree == expected_degree, f"{label} degree")
    require(all(ids[i] <= ids[i + 1] for i in range(expected_degree - 1)),
            f"{label} is not canonical")
    require(all(value == 0 for value in ids[expected_degree:]), f"{label} padding")
    return ids[:expected_degree]


def parse_checkpoint(path: Path, expected_sha: str | None = None) -> dict:
    if expected_sha is not None:
        require(sha256_file(path) == expected_sha, f"checkpoint SHA: {path}")
    with path.open("rb") as stream:
        require(read_exact(stream, 12, "checkpoint magic") == CHECKPOINT_MAGIC,
                "checkpoint magic")
        prime = read_u64(stream, "checkpoint prime")
        round_index = read_u64(stream, "checkpoint round")
        column_count = read_u64(stream, "checkpoint column count")
        support = read_u64(stream, "checkpoint support")
        require(prime == PRIME, "checkpoint prime")
        columns: list[tuple[int, bytes]] = []
        previous = None
        for index in range(column_count):
            word = struct.unpack("<H", read_exact(stream, 2, "checkpoint word"))[0]
            multiplier = read_mono(stream, 8, "checkpoint multiplier")
            column = (word, multiplier)
            require(word < 6561, "checkpoint word range")
            require(previous is None or previous < column, "checkpoint column total order")
            previous = column
            columns.append(column)
        candidate: dict[bytes, int] = {}
        previous_row = None
        for _ in range(support):
            row = read_mono(stream, 12, "checkpoint candidate row")
            value = read_u64(stream, "checkpoint candidate value")
            require(previous_row is None or previous_row < row,
                    "checkpoint candidate total order")
            require(0 < value < PRIME and row not in candidate,
                    "checkpoint candidate entry")
            previous_row = row
            candidate[row] = value
        require(stream.read(1) == b"", "checkpoint trailing bytes")
    require(candidate.get(TARGET) == 1, "checkpoint target normalization")
    return {
        "prime": prime,
        "round": round_index,
        "columns": columns,
        "candidate": candidate,
        "support": support,
    }


def fnv_update(hash_value: int, data: bytes) -> int:
    for byte in data:
        hash_value ^= byte
        hash_value = (hash_value * FNV_PRIME) & MASK64
    return hash_value


def replay_vectors(path: Path, checkpoint: dict, expected_sha: str | None = None) -> dict:
    started = time.monotonic()
    if expected_sha is not None:
        require(sha256_file(path) == expected_sha, f"vector SHA: {path}")
    candidate: dict[bytes, int] = checkpoint["candidate"]
    columns: list[tuple[int, bytes]] = checkpoint["columns"]
    failures = 0
    terms = 0
    hit_terms = 0
    target_terms = 0
    hash_value = FNV_OFFSET
    with path.open("rb") as stream:
        require(read_exact(stream, 12, "vector magic") == VECTOR_MAGIC, "vector magic")
        prime_bytes = read_exact(stream, 8, "vector prime")
        prime = struct.unpack("<Q", prime_bytes)[0]
        provider_fingerprint = read_u64(stream, "provider fingerprint")
        expected_fingerprint = read_u64(stream, "vector fingerprint")
        count = read_u64(stream, "vector count")
        require(prime == PRIME, "vector prime")
        require(count == len(columns), "vector/checkpoint count")
        previous_column = None
        for index in range(count):
            word_bytes = read_exact(stream, 2, "vector word")
            word = struct.unpack("<H", word_bytes)[0]
            degree_byte = read_exact(stream, 1, "vector multiplier degree")
            multiplier_ids = read_exact(stream, 12, "vector multiplier ids")
            require(degree_byte == b"\x08", "vector multiplier degree")
            multiplier = multiplier_ids[:8]
            require(all(multiplier[i] <= multiplier[i + 1] for i in range(7)),
                    "vector multiplier canonical")
            require(multiplier_ids[8:] == b"\0\0\0\0", "vector multiplier padding")
            column = (word, multiplier)
            require(word < 6561 and column == columns[index],
                    "vector/checkpoint column mismatch")
            require(previous_column is None or previous_column < column,
                    "vector column total order")
            previous_column = column
            size_bytes = read_exact(stream, 8, "vector size")
            size = struct.unpack("<Q", size_bytes)[0]
            require(0 < size <= 700_000, "vector size")
            hash_value = fnv_update(hash_value, word_bytes + degree_byte + multiplier_ids + size_bytes)
            pairing = 0
            previous_row = None
            for _ in range(size):
                degree_byte = read_exact(stream, 1, "vector row degree")
                row_ids = read_exact(stream, 12, "vector row ids")
                value_bytes = read_exact(stream, 8, "vector value")
                value = struct.unpack("<Q", value_bytes)[0]
                require(degree_byte == b"\x0c", "vector row degree")
                require(all(row_ids[i] <= row_ids[i + 1] for i in range(11)),
                        "vector row canonical")
                require(previous_row is None or previous_row < row_ids,
                        "vector row total order")
                require(0 < value < PRIME, "vector value")
                previous_row = row_ids
                hash_value = fnv_update(hash_value, degree_byte + row_ids + value_bytes)
                candidate_value = candidate.get(row_ids)
                if candidate_value is not None:
                    pairing = (pairing + value * candidate_value) % PRIME
                    hit_terms += 1
                target_terms += int(row_ids == TARGET)
                terms += 1
            failures += int(pairing != 0)
        require(stream.read(1) == b"", "vector trailing bytes")
    require(hash_value == expected_fingerprint, "vector internal FNV fingerprint")
    require(failures == 0, "candidate violates cached columns")
    return {
        "columns_replayed": count,
        "terms_replayed": terms,
        "candidate_hit_terms": hit_terms,
        "target_terms": target_terms,
        "verification_failures": failures,
        "provider_fingerprint": provider_fingerprint,
        "vector_fingerprint": expected_fingerprint,
        "seconds": time.monotonic() - started,
    }


def validate_replay_summary(path: Path) -> dict:
    replay = json.loads(path.read_text())
    require(replay.get("schema") == "KRENN_AFFINE251_D12_CACHE_REPLAY_V1",
            "cache replay schema")
    require(replay.get("status") == "PASS_ALL_COLUMNS", "cache replay status")
    require((replay.get("round"), replay.get("columns_replayed"),
             replay.get("verification_failures")) == (ROUND, COLUMNS, 0),
            "cache replay census")
    require(isinstance(replay.get("terms_replayed"), int) and replay["terms_replayed"] > COLUMNS,
            "cache replay term census")
    require(isinstance(replay.get("candidate_hit_terms"), int) and
            replay["candidate_hit_terms"] > 0, "cache replay candidate hits")
    require(isinstance(replay.get("seconds"), (int, float)) and
            math.isfinite(replay["seconds"]) and replay["seconds"] >= 0,
            "cache replay timer")
    return replay


def validate_baseline(result_path: Path, source_path: Path, checkpoint_path: Path,
                      vectors_path: Path, replay_path: Path) -> tuple[dict, dict]:
    require(sha256_file(source_path) == PARENT_SOURCE_SHA, "restored parent source SHA")
    require(sha256_file(result_path) == BASELINE_RESULT_SHA, "accepted result SHA")
    require(checkpoint_path.stat().st_size == 5_007_185, "accepted checkpoint byte size")
    require(vectors_path.stat().st_size == BASELINE_VECTOR_BYTES, "accepted vector byte size")
    result = json.loads(result_path.read_text())
    require(result.get("schema") == "KRENN_AFFINE251_D12_NATIVE_SPARSE_DUAL_V1",
            "accepted result schema")
    require(result.get("status") == "INCOMPLETE_RESOURCE_GATE" and
            result.get("incomplete_reason") == "WALL_CAP", "accepted result status")
    require((result.get("prime"), result.get("rounds_completed"),
             result.get("column_orbits_exposed"), result.get("dual_support")) ==
            (PRIME, ROUND, COLUMNS, SUPPORT), "accepted result census")
    require((result.get("pivot_mode"), result.get("strategy"),
             result.get("elimination_kernel"), result.get("incremental_basis")) ==
            ("rare", "cold", "tree", False), "accepted mode")
    checkpoint = parse_checkpoint(checkpoint_path, BASELINE_CHECKPOINT_SHA)
    require((checkpoint["round"], len(checkpoint["columns"]), checkpoint["support"]) ==
            (ROUND, COLUMNS, SUPPORT), "accepted checkpoint census")
    replay = validate_replay_summary(replay_path)
    return checkpoint, replay


def validate_integration(result: dict, integration_source: Path, integration_binary: Path,
                         baseline_checkpoint: Path, baseline_vectors: Path,
                         output_checkpoint: Path, output_vectors: Path,
                         baseline_candidate: dict[bytes, int]) -> dict:
    require(result.get("schema") ==
            "KRENN_AFFINE251_D12_HIERARCHICAL_GENERIC_INTEGRATION_V1",
            "integration schema")
    require(result.get("status") ==
            "PASS_EXACT_GENERIC_HIERARCHICAL_ROUND748_RESUME_CONTROL",
            "integration status")
    require(result.get("base_source_sha256") == PARENT_SOURCE_SHA, "base source pin")
    require(result.get("integration_source_sha256") == sha256_file(integration_source),
            "integration source pin")
    require(result.get("integration_binary_sha256") == sha256_file(integration_binary),
            "integration binary pin")
    require(result.get("input_checkpoint_sha256") == BASELINE_CHECKPOINT_SHA and
            result.get("input_vectors_sha256") == BASELINE_VECTORS_SHA,
            "integration input pins")
    require(result.get("output_checkpoint_sha256") == sha256_file(output_checkpoint) ==
            BASELINE_CHECKPOINT_SHA, "output checkpoint SHA")
    require(result.get("output_vectors_sha256") == sha256_file(output_vectors) ==
            BASELINE_VECTORS_SHA, "output cache SHA")
    require(files_equal(baseline_checkpoint, output_checkpoint),
            "output checkpoint is not byte-identical")
    require(files_equal(baseline_vectors, output_vectors),
            "output cache is not byte-identical")
    require((result.get("input_round"), result.get("output_round"),
             result.get("columns"), result.get("candidate_support")) ==
            (ROUND, ROUND, COLUMNS, SUPPORT), "integration census")
    require(result.get("candidate_byte_identical") is True and
            result.get("checkpoint_byte_identical") is True and
            result.get("vector_cache_byte_identical") is True,
            "byte identity declarations")
    require(result.get("schema_preserved") is True and
            result.get("arbitrary_resume_supported") is True,
            "schema/resume declarations")
    require(result.get("pivot_order") == "(exposed_frequency,row)_ascending_total_order" and
            result.get("column_order") == "native_sorted_columns_ascending",
            "total ordering contract")
    require((result.get("workers"), result.get("pivot_mode"), result.get("strategy"),
             result.get("elimination_kernel"), result.get("incremental_basis")) ==
            (16, "rare", "cold", "hierarchical", False), "integration mode")
    require(result.get("all_columns_verified") is True and
            result.get("verification_failures") == 0, "producer all-column replay")
    require(result.get("hard_rss_bytes") == RSS_LIMIT_BYTES and
            0 <= result.get("peak_rss_bytes", RSS_LIMIT_BYTES + 1) < RSS_LIMIT_BYTES,
            "36 GiB hard resource contract")
    hostile = result.get("hostile_mode_rejections")
    required_hostiles = {
        "pivot_first", "pivot_last", "pivot_auto", "strategy_repair", "strategy_best",
        "incremental_yes", "workers_not_16", "portfolio_parallel", "unknown_elimination",
    }
    require(isinstance(hostile, dict) and required_hostiles <= hostile.keys() and
            all(hostile[name] is True for name in required_hostiles),
            "hostile mode rejection ledger")
    output = parse_checkpoint(output_checkpoint, BASELINE_CHECKPOINT_SHA)
    require(output["candidate"] == baseline_candidate, "candidate map identity")
    return output


def expect_reject(callable_, label: str) -> None:
    try:
        callable_()
    except (Rejection, KeyError, TypeError, json.JSONDecodeError):
        return
    raise Rejection(f"hostile accepted: {label}")


def run_result_hostiles(result: dict, validate) -> list[str]:
    checks = []
    mutations = {
        "schema": ("schema", "STALE_V0"),
        "base_source": ("base_source_sha256", "0" * 64),
        "pivot_order": ("pivot_order", "frequency_only"),
        "candidate_identity": ("candidate_byte_identical", False),
        "all_column_replay": ("verification_failures", 1),
        "rss_contract": ("hard_rss_bytes", 8 * 1024**3),
    }
    for label, (field, value) in mutations.items():
        hostile = copy.deepcopy(result)
        hostile[field] = value
        expect_reject(lambda hostile=hostile: validate(hostile), label)
        checks.append(label)
    hostile = copy.deepcopy(result)
    hostile["hostile_mode_rejections"]["pivot_first"] = False
    expect_reject(lambda: validate(hostile), "mode_rejection")
    checks.append("mode_rejection")
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-result", type=Path, required=True)
    parser.add_argument("--parent-source", type=Path, required=True)
    parser.add_argument("--baseline-checkpoint", type=Path, required=True)
    parser.add_argument("--baseline-vectors", type=Path, required=True)
    parser.add_argument("--baseline-replay", type=Path, required=True)
    parser.add_argument("--integration-result", type=Path)
    parser.add_argument("--integration-source", type=Path)
    parser.add_argument("--integration-binary", type=Path)
    parser.add_argument("--output-checkpoint", type=Path)
    parser.add_argument("--output-vectors", type=Path)
    parser.add_argument("--audit-output", type=Path, required=True)
    args = parser.parse_args()
    integration_args = [args.integration_result, args.integration_source, args.integration_binary,
                        args.output_checkpoint, args.output_vectors]
    require(all(item is None for item in integration_args) or all(item is not None for item in integration_args),
            "integration arguments must be supplied together")

    checkpoint, replay = validate_baseline(args.baseline_result, args.parent_source,
                                           args.baseline_checkpoint, args.baseline_vectors,
                                           args.baseline_replay)
    audit = {
        "schema": "KRENN_AFFINE251_D12_HIERARCHICAL_INTEGRATION_AUDIT_V1",
        "status": "PASS_ACCEPTED_ROUND748_BASELINE_ONLY",
        "parent_source_sha256": PARENT_SOURCE_SHA,
        "accepted_result_sha256": BASELINE_RESULT_SHA,
        "accepted_checkpoint_sha256": BASELINE_CHECKPOINT_SHA,
        "accepted_vectors_sha256": BASELINE_VECTORS_SHA,
        "accepted_round": ROUND,
        "accepted_columns": COLUMNS,
        "accepted_support": SUPPORT,
        "source_annihilation_replay": replay,
        "integration_verdict": "PENDING_ARTIFACTS_FAIL_CLOSED",
        "scope": "Read-only exact audit; no elimination, continuation, or provider evaluation.",
    }
    if args.integration_result is not None:
        result = json.loads(args.integration_result.read_text())

        def validate(value):
            return validate_integration(value, args.integration_source, args.integration_binary,
                                        args.baseline_checkpoint, args.baseline_vectors,
                                        args.output_checkpoint, args.output_vectors,
                                        checkpoint["candidate"])

        validate(result)
        hostiles = run_result_hostiles(result, validate)
        # Output files are independently compared byte-for-byte above, so the
        # accepted all-column replay transfers without a redundant second scan.
        output_replay = dict(replay)
        audit.update({
            "status": "PASS_INDEPENDENT_EXACT_GENERIC_HIERARCHICAL_INTEGRATION_AUDIT",
            "integration_result_sha256": sha256_file(args.integration_result),
            "integration_source_sha256": sha256_file(args.integration_source),
            "integration_binary_sha256": sha256_file(args.integration_binary),
            "output_checkpoint_sha256": BASELINE_CHECKPOINT_SHA,
            "output_vectors_sha256": BASELINE_VECTORS_SHA,
            "candidate_checkpoint_cache_byte_identical": True,
            "schema_preserved": True,
            "arbitrary_round748_resume": True,
            "total_pivot_order_contract": "(exposed_frequency,row) ascending; native sorted columns",
            "output_source_annihilation_replay": output_replay,
            "hostile_result_checks": hostiles,
            "integration_verdict": "PASS",
        })
    raw_peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak = raw_peak if sys.platform == "darwin" else raw_peak * 1024
    require(peak < RSS_LIMIT_BYTES, "auditor exceeded 36 GiB")
    audit["auditor_peak_rss_bytes"] = peak
    temporary = args.audit_output.with_suffix(args.audit_output.suffix + ".tmp")
    temporary.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, args.audit_output)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()

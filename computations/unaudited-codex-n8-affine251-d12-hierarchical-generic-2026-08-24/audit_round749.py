#!/usr/bin/env python3
"""Independent byte/schema and every-column annihilation replay for round 749."""

import hashlib
import json
import os
from pathlib import Path
import re
import struct
import time


ROOT = Path(__file__).resolve().parent
SEQUENTIAL = ROOT / "control_sequential"
HIERARCHICAL = ROOT / "control_hierarchical"
SOURCE_INPUT = ROOT.parent / "unaudited-codex-star-tautology-triangle-replacement-2026-08-22" / "canonical_triangle_pair_offdiag_full_p1073741827.ms"
START_ROOT = ROOT.parent / "unaudited-codex-n8-affine251-d12-portfolio-gate-2026-08-24"
PRIME = 1_073_741_827
START_CHECKPOINT_SHA256 = "fe44b33e74b7e9ce00a7654fe8f027b0024b15e464bbaa372ec85ea92bc097c6"
START_VECTORS_SHA256 = "7af04cecc244e158af1df5b782cbe5b2e23d191b4d06b43a1c0c33911e5c6cab"
SOURCE_SHA256 = "173828021430f51a51324a73c12e0cd351c072c2a458b4dadc019672ca72f69a"
BINARY_SHA256 = "8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a"
WATCHDOG_SHA256 = "a1e6104726303960b256c9a9f6217299a71a4be5c00bb77fe451bf62935ed19b"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def exact(stream, size: int) -> bytes:
    value = stream.read(size)
    require(len(value) == size, "unexpected EOF")
    return value


def u64(stream) -> int:
    return struct.unpack("<Q", exact(stream, 8))[0]


def mono(stream, expected_length: int) -> bytes:
    length = exact(stream, 1)[0]
    identifiers = exact(stream, 12)
    require(length == expected_length, "monomial length mismatch")
    return identifiers


def checkpoint(path: Path):
    with path.open("rb", buffering=4 << 20) as stream:
        require(exact(stream, 12) == b"AFF12CEG1\0\0\0", "checkpoint magic")
        require(u64(stream) == PRIME, "checkpoint prime")
        round_index, column_count, support = u64(stream), u64(stream), u64(stream)
        columns = []
        previous = None
        for _ in range(column_count):
            column = (struct.unpack("<H", exact(stream, 2))[0], mono(stream, 8))
            require(previous is None or previous < column, "checkpoint column order")
            previous = column
            columns.append(column)
        candidate = {}
        previous = None
        for _ in range(support):
            row, value = mono(stream, 12), u64(stream)
            require(previous is None or previous < row, "checkpoint candidate order")
            require(0 < value < PRIME and row not in candidate, "checkpoint candidate residue")
            previous = row
            candidate[row] = value
        require(stream.read(1) == b"", "checkpoint trailing bytes")
    require(candidate.get(bytes([251]) * 12) == 1, "target normalization")
    return round_index, columns, candidate


def fnv(hash_value: int, value: bytes) -> int:
    for byte in value:
        hash_value ^= byte
        hash_value = hash_value * 1_099_511_628_211 & ((1 << 64) - 1)
    return hash_value


def replay_vectors(path: Path, columns, candidate):
    started = time.monotonic()
    failures = 0
    terms = 0
    hit_terms = 0
    fingerprint = 14_695_981_039_346_656_037
    with path.open("rb", buffering=16 << 20) as stream:
        require(exact(stream, 12) == b"AFF12VEC1\0\0\0", "vector magic")
        require(u64(stream) == PRIME, "vector prime")
        provider_fingerprint = u64(stream)
        expected_fingerprint = u64(stream)
        count = u64(stream)
        require(count == len(columns), "vector/checkpoint column count")
        previous_column = None
        for index in range(count):
            word_bytes = exact(stream, 2)
            word = struct.unpack("<H", word_bytes)[0]
            multiplier = mono(stream, 8)
            column = (word, multiplier)
            require(column == columns[index], "vector/checkpoint column mismatch")
            require(previous_column is None or previous_column < column, "vector column order")
            previous_column = column
            size_bytes = exact(stream, 8)
            size = struct.unpack("<Q", size_bytes)[0]
            require(0 < size <= 700_000, "vector record size")
            fingerprint = fnv(fingerprint, word_bytes)
            fingerprint = fnv(fingerprint, bytes([8]))
            fingerprint = fnv(fingerprint, multiplier)
            fingerprint = fnv(fingerprint, size_bytes)
            pairing = 0
            previous_row = None
            for _ in range(size):
                length_byte = exact(stream, 1)
                row = exact(stream, 12)
                value_bytes = exact(stream, 8)
                value = struct.unpack("<Q", value_bytes)[0]
                require(length_byte == b"\x0c", "vector row length")
                require(previous_row is None or previous_row < row, "vector row order")
                require(0 < value < PRIME, "vector residue")
                previous_row = row
                fingerprint = fnv(fingerprint, length_byte)
                fingerprint = fnv(fingerprint, row)
                fingerprint = fnv(fingerprint, value_bytes)
                coefficient = candidate.get(row)
                if coefficient is not None:
                    pairing = (pairing + coefficient * value) % PRIME
                    hit_terms += 1
                terms += 1
            failures += pairing != 0
        require(stream.read(1) == b"", "vector trailing bytes")
    require(fingerprint == expected_fingerprint, "vector FNV fingerprint")
    require(failures == 0, "candidate does not annihilate every exposed column")
    return {
        "columns_replayed": count,
        "source_terms_replayed": terms,
        "candidate_hit_terms": hit_terms,
        "verification_failures": failures,
        "provider_fingerprint": provider_fingerprint,
        "vector_fingerprint": fingerprint,
        "seconds": round(time.monotonic() - started, 6),
    }


def main() -> None:
    started = time.monotonic()
    start_checkpoint = START_ROOT / "fixed4_checkpoint.bin"
    start_vectors = START_ROOT / "fixed4_vectors.bin"
    require(sha256(start_checkpoint) == START_CHECKPOINT_SHA256, "start checkpoint pin")
    require(sha256(start_vectors) == START_VECTORS_SHA256, "start vector pin")
    require(sha256(ROOT / "sealed_v3/main.rs") == SOURCE_SHA256, "source pin")
    require(sha256(ROOT / "sealed_v3/sparse_d12_dual") == BINARY_SHA256, "binary pin")
    require(sha256(ROOT / "sealed_v3/run_with_macos_rss_watchdog.py") == WATCHDOG_SHA256,
            "watchdog pin")

    sequential_checkpoint_sha = sha256(SEQUENTIAL / "checkpoint.bin")
    hierarchical_checkpoint_sha = sha256(HIERARCHICAL / "checkpoint.bin")
    sequential_vectors_sha = sha256(SEQUENTIAL / "vectors.bin")
    hierarchical_vectors_sha = sha256(HIERARCHICAL / "vectors.bin")
    require(sequential_checkpoint_sha == hierarchical_checkpoint_sha,
            "checkpoint bytes differ by SHA-256")
    require(sequential_vectors_sha == hierarchical_vectors_sha,
            "vector-cache bytes differ by SHA-256")
    round_index, columns, candidate = checkpoint(HIERARCHICAL / "checkpoint.bin")
    require(round_index == 749 and len(columns) == 334_298 and len(candidate) == 418,
            "round749 checkpoint census")
    replay = replay_vectors(HIERARCHICAL / "vectors.bin", columns, candidate)

    sequential = json.loads((SEQUENTIAL / "result.json").read_text())
    hierarchical = json.loads((HIERARCHICAL / "result.json").read_text())
    watchdog = json.loads((HIERARCHICAL / "watchdog.json").read_text())
    stable_fields = [
        "schema", "status", "incomplete_reason", "degree", "prime", "group_order",
        "provider_equations", "provider_terms_parsed", "provider_distinct_terms",
        "seed_support", "column_orbits_exposed", "dual_support", "rounds_completed",
        "global_annihilation", "target_pairing", "workers", "pivot_mode", "strategy",
        "incremental_basis", "portfolio_period", "portfolio_parallel", "support_cap",
        "column_cap", "wall_limit_seconds", "rss_limit_gib", "cached_vectors_loaded",
        "vectors_materialized_on_restore", "vector_cache_bytes",
    ]
    for field in stable_fields:
        require(sequential[field] == hierarchical[field], f"result field differs: {field}")
    require(sequential["elimination_kernel"] == "tree", "sequential kernel")
    require(hierarchical["elimination_kernel"] == "hierarchical", "hierarchical kernel")
    require(len(sequential["rounds"]) == len(hierarchical["rounds"]) == 1,
            "one-round scope")
    for field in ("round", "columns", "new_columns", "dual_support", "new_support_rows",
                  "selected_strategy", "selected_pivot"):
        require(sequential["rounds"][0][field] == hierarchical["rounds"][0][field],
                f"round field differs: {field}")
    require(watchdog["status"] == "PASS" and watchdog["breach"] is None,
            "watchdog status")
    require(watchdog["binary_sha256"] == BINARY_SHA256
            and watchdog["source_sha256"] == SOURCE_SHA256,
            "watchdog evidence pins")
    require(watchdog["peak_rss_kib"] < watchdog["rss_limit_kib"], "RSS cap")
    require(watchdog["elapsed_seconds"] < watchdog["wall_limit_seconds"], "wall cap")
    require(watchdog["atomic_outputs_clean"], "atomic output guard")

    phase_text = (HIERARCHICAL / "stderr.log").read_text()
    match = re.search(
        r"ordered_sort=([0-9.]+)s rank_map=([0-9.]+)s materialize=([0-9.]+)s "
        r"rank_shard_min=([0-9]+) rank_shard_max=([0-9]+) "
        r"local_eliminate_critical=([0-9.]+)s local_wall=([0-9.]+)s "
        r"merge=([0-9.]+)s backsolve=([0-9.]+)s verify=([0-9.]+)s", phase_text)
    require(match is not None, "phase timing record")
    names = ("ordered_sort", "rank_map", "materialize", "rank_shard_min",
             "rank_shard_max", "local_eliminate_critical", "local_wall",
             "merge", "backsolve", "verify")
    phases = dict(zip(names, map(float, match.groups())))
    sequential_solve = sequential["rounds"][0]["solve_seconds"]
    hierarchical_solve = hierarchical["rounds"][0]["solve_seconds"]
    result = {
        "schema": "KRENN_AFFINE251_D12_HIERARCHICAL_GENERIC_ROUND749_AUDIT_V2",
        "status": "PASS_INDEPENDENT_EXACT_GENERIC_ROUND749_V3",
        "scope": "One fixed cold/rare/16-worker round 748 to 749; no continuation.",
        "start_checkpoint_sha256": START_CHECKPOINT_SHA256,
        "start_vectors_sha256": START_VECTORS_SHA256,
        "source_input_sha256": sha256(SOURCE_INPUT),
        "source_sha256": SOURCE_SHA256,
        "binary_sha256": BINARY_SHA256,
        "watchdog_sha256": WATCHDOG_SHA256,
        "sequential_checkpoint_sha256": sequential_checkpoint_sha,
        "hierarchical_checkpoint_sha256": hierarchical_checkpoint_sha,
        "checkpoint_byte_identical": True,
        "sequential_vectors_sha256": sequential_vectors_sha,
        "hierarchical_vectors_sha256": hierarchical_vectors_sha,
        "vector_cache_byte_identical": True,
        "round": round_index,
        "columns": len(columns),
        "candidate_support": len(candidate),
        "candidate_byte_identical": True,
        "full_replay": replay,
        "sequential_solve_seconds": sequential_solve,
        "hierarchical_solve_seconds": hierarchical_solve,
        "solve_speedup": round(sequential_solve / hierarchical_solve, 9),
        "hierarchical_phase_seconds": phases,
        "watchdog_peak_rss_kib": watchdog["peak_rss_kib"],
        "watchdog_elapsed_seconds": watchdog["elapsed_seconds"],
        "audit_elapsed_seconds": round(time.monotonic() - started, 6),
    }
    path = ROOT / "results_independent_replay.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


if __name__ == "__main__":
    main()

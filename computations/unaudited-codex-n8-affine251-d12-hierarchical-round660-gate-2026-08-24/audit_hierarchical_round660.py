#!/usr/bin/env python3
"""Independent exact audit of the one-round D12 hierarchical solve gate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import mmap
import os
import struct
import time
from pathlib import Path

PRIME = 1_073_741_827
ROUND = 660
EQUATIONS = 246_321
SUPPORT = 352
WORKERS = 16
TARGET = bytes([251]) * 12
VECTOR_SHA = "ecbcb26bcb8d2ecbb38cff4cce56457a960b2f11ba944536cd7bcf8d15b01275"
CHECKPOINT_SHA = "92185737bc273f112f91240ee58eb8d0b4cd842739490838ebd30c870b8b6155"
SOURCE_SHA = "d289bc12ba16759c10dc5335057e8c8ed8edb476abbacb228af5c44871672579"
BINARY_SHA = "89ae110e58ebbf478ead404d4f69662abc32db6e081cc37958fd808c646875aa"
SEQUENTIAL_SECONDS = 8.726527
VECTOR_MAGIC = b"AFF12VEC1\0\0\0"
CHECKPOINT_MAGIC = b"AFF12CEG1\0\0\0"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def u64(data, offset: int) -> int:
    return struct.unpack_from("<Q", data, offset)[0]


def validate_structure(result: dict, vectors: Path, sequential_checkpoint: Path,
                       output_checkpoint: Path, source: Path, binary: Path) -> None:
    require(result.get("schema") == "KRENN_AFFINE251_D12_HIERARCHICAL_ROUND660_V1",
            "result schema")
    require(result.get("status") ==
            "PASS_EXACT_PARALLEL_HIERARCHICAL_ROUND660_PROMOTION_GATE", "status")
    require(result.get("source_sha256") == SOURCE_SHA == sha256_file(source), "source pin")
    require(result.get("binary_sha256") == BINARY_SHA == sha256_file(binary), "binary pin")
    require(result.get("vectors", {}).get("sha256") == VECTOR_SHA == sha256_file(vectors),
            "vectors pin")
    require(result.get("sequential_checkpoint", {}).get("sha256") == CHECKPOINT_SHA ==
            sha256_file(sequential_checkpoint), "sequential checkpoint pin")
    require(result.get("output_checkpoint", {}).get("sha256") == CHECKPOINT_SHA ==
            sha256_file(output_checkpoint), "output checkpoint pin")
    require(result["output_checkpoint"].get("byte_identical") is True and
            sequential_checkpoint.read_bytes() == output_checkpoint.read_bytes(),
            "checkpoint not byte-identical")
    require((result.get("round"), result.get("prime"), result.get("workers"),
             result.get("equations")) == (ROUND, PRIME, WORKERS, EQUATIONS), "scope census")
    require(result.get("source_variable_terms") == 24_950_813, "source term census")
    require(result.get("distinct_variables") == 16_179_918, "variable census")
    require(result.get("candidate_support") == SUPPORT and
            result.get("candidate_identical") is True, "candidate identity")
    require(result.get("all_equations_verified") is True and
            result.get("verification_failures") == 0, "verification fields")
    require(result.get("frontier_comparison") ==
            "IDENTICAL_CANDIDATE_AND_COLUMNS_IMPLY_IDENTICAL_NEXT_FRONTIER",
            "frontier identity theorem")
    require(result.get("promotion_threshold") == 2.0, "threshold")
    require(result.get("sequential_solve_seconds") == SEQUENTIAL_SECONDS,
            "sequential baseline")
    timings = result.get("timings_seconds")
    require(isinstance(timings, dict), "timings object")
    for field in ("source_hash", "parse_and_frequency", "rare_rank_and_materialize",
                  "hierarchical_elimination_backsolve_verify", "checkpoint_write_hash", "total"):
        require(isinstance(timings.get(field), (int, float)) and
                math.isfinite(timings[field]) and timings[field] >= 0, f"timing {field}")
    fair = (timings["rare_rank_and_materialize"] +
            timings["hierarchical_elimination_backsolve_verify"])
    require(math.isclose(result.get("hierarchical_solve_seconds"), fair, rel_tol=1e-12),
            "fair solve timer excludes preparation")
    require(math.isclose(result.get("hierarchical_elimination_backsolve_verify_seconds"),
                         timings["hierarchical_elimination_backsolve_verify"], rel_tol=1e-12),
            "elimination timer identity")
    speedup = SEQUENTIAL_SECONDS / fair
    require(math.isclose(result.get("solve_speedup"), speedup, rel_tol=1e-6),
            "speedup identity after producer decimal rounding")
    require(speedup >= 2.0, "promotion speed below 2x")
    require(result.get("hard_wall_seconds") == 120 and
            result.get("hard_rss_bytes") == 8 * 1024**3, "resource thresholds")
    require(timings["total"] < 120 and result.get("peak_rss_bytes", 1 << 70) < 8 * 1024**3,
            "resource gate")
    require(result.get("scope") ==
            "One exact round-660 cold/rare solve only; no CEGAR continuation, closure, rank, Krylov, or higher-degree run.",
            "scope changed")

    workers = result.get("worker_records")
    require(isinstance(workers, list) and len(workers) == WORKERS, "worker record count")
    cursor = 0
    worker_basis = []
    for index, record in enumerate(workers):
        require(record.get("worker") == index and record.get("begin") == cursor,
                "worker order/gap")
        expected_count = EQUATIONS // WORKERS + int(index < EQUATIONS % WORKERS)
        require(record.get("equations") == expected_count and
                record.get("end") == cursor + expected_count, "worker interval")
        require(record.get("inconsistent") is False, "local inconsistency")
        require(0 < record.get("basis_records", 0) <= expected_count and
                record.get("basis_terms", 0) >= record["basis_records"], "local basis census")
        require(record.get("seconds", -1) >= 0, "local timer")
        worker_basis.append(record["basis_records"])
        cursor = record["end"]
    require(cursor == EQUATIONS, "worker terminal coverage")

    merges = result.get("merge_records")
    require(isinstance(merges, list) and len(merges) == WORKERS - 1, "merge record count")
    previous = worker_basis
    position = 0
    for level, count in enumerate((8, 4, 2, 1)):
        outputs = []
        for pair in range(count):
            record = merges[position]
            position += 1
            require((record.get("level"), record.get("pair")) == (level, pair),
                    "merge order")
            require((record.get("left_records"), record.get("right_records")) ==
                    (previous[2 * pair], previous[2 * pair + 1]), "merge ancestry")
            require(record.get("inconsistent") is False, "merge inconsistency")
            require(max(record["left_records"], record["right_records"]) <=
                    record.get("output_records", -1) <=
                    record["left_records"] + record["right_records"], "merge rank census")
            require(record.get("output_terms", 0) >= record["output_records"] and
                    record.get("seconds", -1) >= 0, "merge term/time census")
            outputs.append(record["output_records"])
        previous = outputs
    require(position == len(merges) and len(previous) == 1, "merge tree completion")
    require(merges[-1]["output_terms"] == result.get("final_basis_terms"),
            "final basis term identity")


def checkpoint_candidate_and_columns(path: Path) -> tuple[list[tuple[int, bytes]], dict[bytes, int]]:
    data = path.read_bytes()
    require(data[:12] == CHECKPOINT_MAGIC, "checkpoint magic")
    require((u64(data, 12), u64(data, 20), u64(data, 28), u64(data, 36)) ==
            (PRIME, ROUND, EQUATIONS, SUPPORT), "checkpoint header")
    position = 44
    columns = []
    previous_column = None
    for _ in range(EQUATIONS):
        word = struct.unpack_from("<H", data, position)[0]
        require(data[position + 2] == 8, "checkpoint multiplier degree")
        multiplier = bytes(data[position + 3:position + 15])
        column = (word, multiplier)
        require(previous_column is None or previous_column < column, "checkpoint column order")
        previous_column = column
        columns.append(column)
        position += 15
    candidate = {}
    previous_row = None
    for _ in range(SUPPORT):
        require(data[position] == 12, "checkpoint candidate degree")
        row = bytes(data[position + 1:position + 13])
        value = u64(data, position + 13)
        require(previous_row is None or previous_row < row, "checkpoint candidate order")
        require(0 < value < PRIME and row not in candidate, "checkpoint candidate entry")
        previous_row = row
        candidate[row] = value
        position += 21
    require(position == len(data), "checkpoint trailing bytes")
    require(candidate.get(TARGET) == 1, "target normalization")
    return columns, candidate


def replay_source(vectors: Path, checkpoint_columns: list[tuple[int, bytes]],
                  candidate: dict[bytes, int]) -> dict:
    started = time.monotonic()
    candidate_integer = {int.from_bytes(row, "little"): value
                         for row, value in candidate.items()}
    source_variable_terms = 0
    candidate_hit_terms = 0
    target_terms = 0
    failures = 0
    with vectors.open("rb") as stream:
        data = mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ)
        require(data[:12] == VECTOR_MAGIC, "vector magic")
        require(u64(data, 12) == PRIME and u64(data, 20) == 9_218_588_987_274_412_661 and
                u64(data, 36) == EQUATIONS, "vector header")
        position = 44
        for index in range(EQUATIONS):
            word = struct.unpack_from("<H", data, position)[0]
            require(data[position + 2] == 8, "vector multiplier degree")
            multiplier = bytes(data[position + 3:position + 15])
            require((word, multiplier) == checkpoint_columns[index], "vector/checkpoint column mismatch")
            size = u64(data, position + 15)
            require(0 < size <= 700_000, "vector size")
            position += 23
            pairing = 0
            previous_row = None
            for _ in range(size):
                require(data[position] == 12, "vector row degree")
                row = data[position + 1:position + 13]
                require(previous_row is None or previous_row < row, "vector row order")
                previous_row = row
                value = u64(data, position + 13)
                require(0 < value < PRIME, "vector residue")
                if row == TARGET:
                    target_terms += 1
                else:
                    source_variable_terms += 1
                candidate_value = candidate_integer.get(int.from_bytes(row, "little"))
                if candidate_value is not None:
                    pairing = (pairing + value * candidate_value) % PRIME
                    candidate_hit_terms += 1
                position += 21
            failures += int(pairing != 0)
        require(position == len(data), "vector trailing bytes")
        data.close()
    require(source_variable_terms == 24_950_813, "source variable-term recount")
    require(failures == 0, "candidate violates source columns")
    return {
        "columns_replayed": EQUATIONS,
        "source_variable_terms_replayed": source_variable_terms,
        "target_terms": target_terms,
        "candidate_hit_terms": candidate_hit_terms,
        "verification_failures": failures,
        "seconds": time.monotonic() - started,
    }


def expect_reject(result: dict, vectors: Path, sequential: Path, output: Path,
                  source: Path, binary: Path, label: str) -> None:
    try:
        validate_structure(result, vectors, sequential, output, source, binary)
    except (ValueError, KeyError, TypeError):
        return
    raise ValueError(f"hostile accepted: {label}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vectors", type=Path, required=True)
    parser.add_argument("--sequential-checkpoint", type=Path, required=True)
    parser.add_argument("--output-checkpoint", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--audit-output", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads(args.result.read_text())
    validate_structure(result, args.vectors, args.sequential_checkpoint,
                       args.output_checkpoint, args.source, args.binary)
    columns, candidate = checkpoint_candidate_and_columns(args.output_checkpoint)
    replay = replay_source(args.vectors, columns, candidate)

    hostile = copy.deepcopy(result)
    hostile["solve_speedup"] = 1.999
    expect_reject(hostile, args.vectors, args.sequential_checkpoint, args.output_checkpoint,
                  args.source, args.binary, "speedup")
    hostile = copy.deepcopy(result)
    hostile["worker_records"][4]["begin"] += 1
    expect_reject(hostile, args.vectors, args.sequential_checkpoint, args.output_checkpoint,
                  args.source, args.binary, "worker gap")
    hostile = copy.deepcopy(result)
    hostile["merge_records"].pop()
    expect_reject(hostile, args.vectors, args.sequential_checkpoint, args.output_checkpoint,
                  args.source, args.binary, "missing merge")
    hostile = copy.deepcopy(result)
    hostile["frontier_comparison"] = "UNSCORED"
    expect_reject(hostile, args.vectors, args.sequential_checkpoint, args.output_checkpoint,
                  args.source, args.binary, "frontier proof")
    hostile = copy.deepcopy(result)
    hostile["timings_seconds"]["rare_rank_and_materialize"] = 0.0
    expect_reject(hostile, args.vectors, args.sequential_checkpoint, args.output_checkpoint,
                  args.source, args.binary, "unfair solve timer")

    audit = {
        "status": "PASS_INDEPENDENT_EXACT_HIERARCHICAL_ROUND660_AUDIT",
        "schema": "KRENN_AFFINE251_D12_HIERARCHICAL_ROUND660_AUDIT_V1",
        "result_sha256": sha256_file(args.result),
        "vectors_sha256": VECTOR_SHA,
        "checkpoint_sha256": CHECKPOINT_SHA,
        "source_sha256": SOURCE_SHA,
        "binary_sha256": BINARY_SHA,
        "worker_intervals_checked": WORKERS,
        "pairwise_merges_checked": WORKERS - 1,
        "checkpoint_byte_identical": True,
        "source_annihilation_replay": replay,
        "hostile_checks": ["speedup", "worker_gap", "missing_merge", "frontier_proof",
                           "unfair_solve_timer"],
        "scope": "Independent audit of one sealed round-660 solve only; no continuation.",
    }
    temporary = args.audit_output.with_suffix(args.audit_output.suffix + ".tmp")
    temporary.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, args.audit_output)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent exact structural/source audit for the round-635 Metal block gate."""

from __future__ import annotations

import argparse
import array
import copy
import hashlib
import json
import math
import mmap
import os
import struct
import sys
import time
from pathlib import Path

MATRIX_SHA = "30ff854947b1b0f76ff01b07297b6aef8797ae44c0fca3b1b11ffae60e0d0439"
VECTOR_SHA = "dd74d7392a005fb9c7726d9a0cc5c86e5b16d987bcb707d1c3a0f90e6e4d9e40"
CHECKPOINT_SHA = "761804372a3f7e12b1915dd2718f7f69ef00b799dc6f90cd083b2fa7d2fc3c88"
PRIME_PLUS = 1_073_741_827
PRIME_MINUS = 1_073_741_789
ROWS = 14_814_562
COLUMNS = 222_676
NNZ = 22_539_257
SUPPORT = 315
VECTOR_MAGIC = b"AFF12VEC1\0\0\0"
CHECKPOINT_MAGIC = b"AFF12CEG1\0\0\0"
MATRIX_MAGIC = b"D12CSRCSCV1\0\0\0\0\0"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def u32(data, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def u64(data, offset: int) -> int:
    return struct.unpack_from("<Q", data, offset)[0]


def validate_result(result: dict, matrix: Path, shader: Path, source: Path,
                    binary: Path) -> dict[tuple[str, int, int, str], dict]:
    require(result.get("schema") == "KRENN_AFFINE251_D12_ROUND635_METAL_BLOCK_GATE_V1",
            "bad result schema")
    require(result.get("matrix_sha256") == MATRIX_SHA == sha256_file(matrix), "matrix pin")
    require(result.get("shader_sha256") == sha256_file(shader), "shader pin")
    require(result.get("swift_source_sha256") == sha256_file(source), "Swift pin")
    require(result.get("binary_sha256") == sha256_file(binary), "binary pin")
    require((result.get("rows"), result.get("columns"), result.get("nnz")) ==
            (ROWS, COLUMNS, NNZ), "matrix census")
    require(result.get("widths") == [1, 8, 16], "width scope")
    require(result.get("primes") == [PRIME_PLUS, PRIME_MINUS], "prime scope")
    require(result.get("modes") == ["regular", "max_residue"], "mode scope")
    require(result.get("directions") == ["A", "AT"], "direction scope")
    require(result.get("all_cpu_metal_byte_exact") is True, "byte equality")
    require(result.get("byte_flip_hostile_rejected") is True, "byte hostile")
    require(result.get("production_ready_threshold") == 3.0, "promotion threshold")
    require(result.get("hard_wall_seconds") == 180.0, "wall gate")
    require(result.get("hard_rss_bytes") == 6 * 1024**3, "RSS gate")
    require(result.get("total_gate_seconds", math.inf) < 180.0, "wall exceeded")
    require(result.get("peak_rss_bytes", 1 << 70) < 6 * 1024**3, "RSS exceeded")
    require(result.get("resource_gate_pass") is True, "resource gate Boolean")
    require(result.get("scope") ==
            "Exact resident round-635 A/A^T block operators only; no closure, rank, Krylov, membership, or higher-degree launch.",
            "scope changed")
    cases = result.get("cases")
    require(isinstance(cases, list) and len(cases) == 24, "case count")
    expected = {(direction, width, prime, mode)
                for direction in ("A", "AT") for width in (1, 8, 16)
                for prime in (PRIME_PLUS, PRIME_MINUS)
                for mode in ("regular", "max_residue")}
    keyed = {}
    for case in cases:
        key = (case.get("direction"), case.get("width"),
               case.get("prime"), case.get("mode"))
        require(key in expected and key not in keyed, "unexpected/duplicate case")
        require(case.get("byte_exact_equal") is True, "case byte mismatch")
        direction, width, prime, _ = key
        input_entities = COLUMNS if direction == "A" else ROWS
        output_entities = ROWS if direction == "A" else COLUMNS
        require(case.get("input_values") == input_entities * width, "input census")
        require(case.get("output_values") == output_entities * width, "output census")
        for field in ("input_build_seconds", "input_upload_output_allocation_seconds",
                      "cpu_operator_seconds", "metal_warm_end_to_end_seconds",
                      "metal_gpu_seconds", "warm_operator_speedup"):
            require(isinstance(case.get(field), (int, float)) and
                    math.isfinite(case[field]) and case[field] >= 0, f"bad {field}")
        require(case["cpu_operator_seconds"] > 0 and
                case["metal_warm_end_to_end_seconds"] > 0, "zero operator timer")
        require(math.isclose(case["warm_operator_speedup"],
                             case["cpu_operator_seconds"] /
                             case["metal_warm_end_to_end_seconds"], rel_tol=1e-12),
                "speedup identity")
        require(isinstance(case.get("output_sha256"), str) and
                len(case["output_sha256"]) == 64, "output hash encoding")
        keyed[key] = case
    require(set(keyed) == expected, "case set mismatch")
    block_minimum = min(case["warm_operator_speedup"] for key, case in keyed.items()
                        if key[1] >= 8)
    require(math.isclose(result["block_width_8_16_minimum_warm_speedup"], block_minimum,
                         rel_tol=1e-12), "block minimum identity")
    ready = block_minimum >= 3.0
    require(result.get("production_ready_for_future_block_operators") is ready,
            "readiness Boolean")
    expected_status = ("PASS_PRODUCTION_READY_EXACT_METAL_BLOCK_OPERATORS" if ready else
                       "PASS_EXACT_METAL_BLOCK_OPERATORS_NOT_PRODUCTION_READY")
    require(result.get("status") == expected_status, "readiness status")
    candidate = result.get("candidate_annihilation")
    require(isinstance(candidate, dict), "candidate result")
    require(candidate.get("checkpoint_round") == 635 and
            candidate.get("support") == SUPPORT and candidate.get("dense_present") == SUPPORT,
            "candidate census")
    require(candidate.get("prime") == PRIME_PLUS and candidate.get("nonzero_outputs") == 0,
            "candidate nonzero output")
    require(candidate.get("byte_exact_equal") is True, "candidate byte equality")
    require(candidate.get("output_sha256") ==
            hashlib.sha256(bytes(COLUMNS * 4)).hexdigest(), "candidate zero digest")
    return keyed


def exact_matrix_transpose_audit(path: Path) -> dict:
    started = time.monotonic()
    with path.open("rb") as stream:
        data = mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ)
        require(data[:16] == MATRIX_MAGIC, "matrix magic")
        require(u32(data, 16) == 1 and u32(data, 20) == PRIME_PLUS, "matrix version/prime")
        require((u64(data, 24), u64(data, 32), u64(data, 40)) ==
                (ROWS, COLUMNS, NNZ), "matrix dimensions")
        require((u64(data, 48), u64(data, 56), u64(data, 96)) ==
                (SUPPORT, SUPPORT, 635), "matrix candidate/round")
        require(data[104:136].hex() == VECTOR_SHA and
                data[136:168].hex() == CHECKPOINT_SHA, "matrix source pins")
        offsets = [u64(data, offset) for offset in range(176, 225, 8)]
        require(offsets == sorted(offsets) and offsets[0] == 256 and
                u64(data, 232) == len(data), "matrix offsets/length")
        csc_ptr = memoryview(data)[offsets[0]:offsets[1]].cast("I")
        csc_rows = memoryview(data)[offsets[1]:offsets[2]].cast("I")
        csc_values = memoryview(data)[offsets[2]:offsets[3]].cast("i")
        csr_ptr = memoryview(data)[offsets[3]:offsets[4]].cast("I")
        csr_columns = memoryview(data)[offsets[4]:offsets[5]].cast("I")
        csr_values = memoryview(data)[offsets[5]:offsets[6]].cast("i")
        require((len(csc_ptr), len(csc_rows), len(csc_values)) ==
                (COLUMNS + 1, NNZ, NNZ), "CSC section lengths")
        require((len(csr_ptr), len(csr_columns), len(csr_values)) ==
                (ROWS + 1, NNZ, NNZ), "CSR section lengths")
        require(csc_ptr[0] == 0 and csc_ptr[-1] == NNZ and
                csr_ptr[0] == 0 and csr_ptr[-1] == NNZ, "pointer endpoints")
        positions = array.array("I")
        positions.frombytes(memoryview(data)[offsets[3]:offsets[4] - 4])
        coefficient_min = 1 << 31
        coefficient_max = -(1 << 31)
        previous_csc_end = 0
        for column in range(COLUMNS):
            begin, end = csc_ptr[column], csc_ptr[column + 1]
            require(begin == previous_csc_end and begin <= end, "CSC pointer gap/order")
            previous_csc_end = end
            previous_row = -1
            for edge in range(begin, end):
                row = csc_rows[edge]
                value = csc_values[edge]
                require(previous_row < row < ROWS, "CSC row order/range")
                require(value != 0 and abs(value) <= 1440, "CSC coefficient bound")
                previous_row = row
                position = positions[row]
                require(position < csr_ptr[row + 1], "CSR scatter overflow")
                require(csr_columns[position] == column and csr_values[position] == value,
                        "CSR is not exact transpose of CSC")
                positions[row] = position + 1
                coefficient_min = min(coefficient_min, value)
                coefficient_max = max(coefficient_max, value)
        require(previous_csc_end == NNZ, "CSC terminal coverage")
        require(all(positions[row] == csr_ptr[row + 1] for row in range(ROWS)),
                "CSR scatter incomplete")
        candidate_records = []
        previous_row = None
        for index in range(SUPPORT):
            base = offsets[6] + 24 * index
            dense, value = struct.unpack_from("<II", data, base)
            require(dense < ROWS and 0 < value < PRIME_PLUS, "matrix candidate entry")
            require(data[base + 8] == 12 and data[base + 21:base + 24] == b"\0\0\0",
                    "matrix candidate encoding")
            row = bytes(data[base + 9:base + 21])
            require(previous_row is None or previous_row < row, "matrix candidate order")
            previous_row = row
            candidate_records.append((row, value, dense))
        require(offsets[6] + 24 * SUPPORT == len(data), "matrix candidate terminal")
        del csc_ptr, csc_rows, csc_values, csr_ptr, csr_columns, csr_values, positions
        data.close()
    return {
        "transpose_edge_records_checked": NNZ,
        "rows_completed": ROWS,
        "columns_completed": COLUMNS,
        "coefficient_min": coefficient_min,
        "coefficient_max": coefficient_max,
        "candidate_records": candidate_records,
        "seconds": time.monotonic() - started,
    }


def read_checkpoint_candidate(path: Path) -> tuple[list[tuple[bytes, int]], int]:
    data = path.read_bytes()
    require(data[:12] == CHECKPOINT_MAGIC, "checkpoint magic")
    require((u64(data, 12), u64(data, 20), u64(data, 28), u64(data, 36)) ==
            (PRIME_PLUS, 635, COLUMNS, SUPPORT), "checkpoint header")
    position = 44 + COLUMNS * 15
    candidate = []
    for _ in range(SUPPORT):
        require(data[position] == 12, "checkpoint candidate degree")
        row = bytes(data[position + 1:position + 13])
        value = u64(data, position + 13)
        require(0 < value < PRIME_PLUS, "checkpoint candidate value")
        candidate.append((row, value))
        position += 21
    require(position == len(data), "checkpoint trailing bytes")
    require(all(a[0] < b[0] for a, b in zip(candidate, candidate[1:])),
            "checkpoint candidate order")
    return candidate, position


def replay_candidate_from_source(vectors_path: Path, candidate: list[tuple[bytes, int]]) -> dict:
    started = time.monotonic()
    candidate_map = {int.from_bytes(row, "little"): value for row, value in candidate}
    require(len(candidate_map) == SUPPORT, "candidate duplicate")
    hit_terms = 0
    nonzero_pairings = 0
    with vectors_path.open("rb") as stream:
        data = mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ)
        require(data[:12] == VECTOR_MAGIC, "vector magic")
        require((u64(data, 12), u64(data, 36)) == (PRIME_PLUS, COLUMNS), "vector header")
        position = 44
        previous_column = None
        for column_index in range(COLUMNS):
            word = struct.unpack_from("<H", data, position)[0]
            require(data[position + 2] == 8, "vector multiplier degree")
            multiplier = bytes(data[position + 3:position + 15])
            column = (word, multiplier)
            require(previous_column is None or previous_column < column, "vector column order")
            previous_column = column
            size = u64(data, position + 15)
            require(0 < size <= 700_000, "vector size")
            position += 23
            pairing = 0
            previous_row = None
            for _ in range(size):
                require(data[position] == 12, "vector row degree")
                row_bytes = data[position + 1:position + 13]
                if previous_row is not None:
                    require(previous_row < row_bytes, "vector row order")
                previous_row = row_bytes
                candidate_value = candidate_map.get(int.from_bytes(row_bytes, "little"))
                residue = u64(data, position + 13)
                require(0 < residue < PRIME_PLUS, "vector residue")
                if candidate_value is not None:
                    pairing = (pairing + residue * candidate_value) % PRIME_PLUS
                    hit_terms += 1
                position += 21
            if pairing:
                nonzero_pairings += 1
        require(position == len(data), "vector trailing bytes")
        data.close()
    require(nonzero_pairings == 0, "source current-candidate annihilation failed")
    return {
        "source_vectors_replayed": COLUMNS,
        "source_nnz_scanned": NNZ,
        "candidate_hit_terms": hit_terms,
        "nonzero_pairings": nonzero_pairings,
        "seconds": time.monotonic() - started,
    }


def expect_reject(result: dict, matrix: Path, shader: Path, source: Path,
                  binary: Path, label: str) -> None:
    try:
        validate_result(result, matrix, shader, source, binary)
    except ValueError:
        return
    raise ValueError(f"hostile accepted: {label}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--vectors", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--shader", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--audit-output", type=Path, required=True)
    args = parser.parse_args()
    require(sys.byteorder == "little", "little-endian audit required")
    require(sha256_file(args.vectors) == VECTOR_SHA, "vector source pin")
    require(sha256_file(args.checkpoint) == CHECKPOINT_SHA, "checkpoint source pin")
    result = json.loads(args.result.read_text())
    validate_result(result, args.matrix, args.shader, args.source, args.binary)
    transpose = exact_matrix_transpose_audit(args.matrix)
    checkpoint_candidate, _ = read_checkpoint_candidate(args.checkpoint)
    require([(row, value) for row, value, _ in transpose["candidate_records"]] ==
            checkpoint_candidate, "matrix/checkpoint candidate mismatch")
    source_replay = replay_candidate_from_source(args.vectors, checkpoint_candidate)

    hostile = copy.deepcopy(result)
    hostile["production_ready_for_future_block_operators"] = False
    expect_reject(hostile, args.matrix, args.shader, args.source, args.binary, "readiness")
    hostile = copy.deepcopy(result)
    hostile["cases"].pop()
    expect_reject(hostile, args.matrix, args.shader, args.source, args.binary, "missing case")
    hostile = copy.deepcopy(result)
    hostile["peak_rss_bytes"] = 6 * 1024**3
    expect_reject(hostile, args.matrix, args.shader, args.source, args.binary, "RSS boundary")
    hostile = copy.deepcopy(result)
    hostile["cases"][0]["mode"] = "regular"
    hostile["cases"][1]["mode"] = "regular"
    expect_reject(hostile, args.matrix, args.shader, args.source, args.binary, "duplicate case")

    candidate_records_count = len(transpose.pop("candidate_records"))
    audit = {
        "status": "PASS_INDEPENDENT_EXACT_ROUND635_METAL_BLOCK_GATE_AUDIT",
        "schema": "KRENN_AFFINE251_D12_ROUND635_METAL_BLOCK_GATE_AUDIT_V1",
        "result_sha256": sha256_file(args.result),
        "matrix_sha256": MATRIX_SHA,
        "vectors_sha256": VECTOR_SHA,
        "checkpoint_sha256": CHECKPOINT_SHA,
        "shader_sha256": sha256_file(args.shader),
        "swift_source_sha256": sha256_file(args.source),
        "binary_sha256": sha256_file(args.binary),
        "matrix_transpose_audit": transpose,
        "candidate_records_checked": candidate_records_count,
        "source_candidate_replay": source_replay,
        "case_set_checked": 24,
        "hostile_checks": ["readiness_boolean", "missing_case", "rss_boundary",
                           "duplicate_case"],
        "scope": "Exact structural/source referee only; no closure, rank, Krylov, or membership run.",
    }
    temporary = args.audit_output.with_suffix(args.audit_output.suffix + ".tmp")
    temporary.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, args.audit_output)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()

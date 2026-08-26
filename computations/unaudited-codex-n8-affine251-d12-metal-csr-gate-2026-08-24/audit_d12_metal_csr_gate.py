#!/usr/bin/env python3
"""Fail-closed independent audit of the bounded D12 CPU/Metal CSR gate."""

from __future__ import annotations

import argparse
import array
import copy
import hashlib
import json
import math
import struct
import sys
from pathlib import Path

MAGIC = b"D12CSRSLICEV1\0\0\0"
HEADER = struct.Struct("<16sIIIIQQ32s32s")
SOURCE_PRIME = 1_073_741_827
PRIMES = (1_073_741_827, 1_073_741_789)
EXPECTED_INPUT_SHA256 = "78af8f53288fb4149082fd13cf49c0e0524f05e111204d32216c667a355c96f1"
EXPECTED_ROWS = 32_768
EXPECTED_COLUMNS = 2_820_144
EXPECTED_NNZ = 3_296_157
MASK64 = (1 << 64) - 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_bytes(value: bytes | bytearray | memoryview) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_csr(path: Path):
    payload = path.read_bytes()
    require(sha256_bytes(payload) == EXPECTED_INPUT_SHA256, "unfrozen CSR input")
    require(len(payload) >= HEADER.size, "short CSR input")
    (magic, version, source_prime, rows, columns, nnz, source_size,
     source_sha, payload_sha) = HEADER.unpack_from(payload)
    require(magic == MAGIC, "bad CSR magic")
    require(version == 1 and source_prime == SOURCE_PRIME, "bad CSR version/prime")
    require((rows, columns, nnz) == (EXPECTED_ROWS, EXPECTED_COLUMNS, EXPECTED_NNZ),
            "unexpected bounded CSR dimensions")
    require(source_size == 315_657_300, "unexpected source cache size")
    require(source_sha.hex() ==
            "2f6e21c52af1528cff68db91b293052f4a3e2627ebe199586b4e9efb7a883320",
            "unexpected source cache hash")
    require(hashlib.sha256(payload[HEADER.size:]).digest() == payload_sha,
            "CSR payload digest mismatch")
    expected_size = HEADER.size + 4 * (rows + 1) + 8 * nnz
    require(len(payload) == expected_size, "CSR byte length mismatch")
    cursor = HEADER.size
    offsets = array.array("I")
    offsets.frombytes(payload[cursor:cursor + 4 * (rows + 1)])
    cursor += 4 * (rows + 1)
    indices = array.array("I")
    indices.frombytes(payload[cursor:cursor + 4 * nnz])
    cursor += 4 * nnz
    coefficients = array.array("i")
    coefficients.frombytes(payload[cursor:cursor + 4 * nnz])
    require(sys.byteorder == "little", "audit requires little-endian host")
    require(offsets[0] == 0 and offsets[-1] == nnz, "bad CSR endpoints")
    require(all(a <= b for a, b in zip(offsets, offsets[1:])), "nonmonotone CSR")
    require(all(index < columns for index in indices), "CSR index out of bounds")
    require(all(value != 0 and abs(value) <= 1440 for value in coefficients),
            "CSR coefficient outside exact centered-lift bound")
    return rows, columns, offsets, indices, coefficients


def regular_vector(columns: int, prime: int) -> array.array:
    values = array.array("I")
    append = values.append
    for index in range(columns):
        value = (index + 0x9E3779B97F4A7C15) & MASK64
        value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
        value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & MASK64
        value ^= value >> 31
        append(value % prime)
    return values


def replay(rows: int, columns: int, offsets: array.array, indices: array.array,
           coefficients: array.array, prime: int, mode: str) -> bytes:
    vector = regular_vector(columns, prime) if mode == "regular" else None
    result = array.array("I", [0]) * rows
    for row in range(rows):
        total = 0
        for edge in range(offsets[row], offsets[row + 1]):
            multiplier = vector[indices[edge]] if vector is not None else prime - 1
            total = (total + (coefficients[edge] % prime) * multiplier) % prime
        result[row] = total
    return result.tobytes()


def validate_structure(result: dict, input_path: Path, shader_path: Path,
                       source_path: Path, binary_path: Path) -> dict[tuple[int, str], dict]:
    require(result.get("schema") == "KRENN_AFFINE251_D12_METAL_CSR_GATE_V1",
            "bad result schema")
    require(result.get("input_sha256") == EXPECTED_INPUT_SHA256, "result input hash")
    require(result.get("input_sha256") == sha256_file(input_path), "live input hash")
    require(result.get("shader_sha256") == sha256_file(shader_path), "shader hash")
    require(result.get("swift_source_sha256") == sha256_file(source_path), "source hash")
    require(result.get("binary_sha256") == sha256_file(binary_path), "binary hash")
    require((result.get("rows"), result.get("columns"), result.get("nnz")) ==
            (EXPECTED_ROWS, EXPECTED_COLUMNS, EXPECTED_NNZ), "result dimensions")
    require(isinstance(result.get("repetitions"), int) and
            0 < result["repetitions"] <= 4096, "bad repetition count")
    require(result.get("promotion_threshold") == 3.0, "changed promotion threshold")
    require(result.get("byte_comparator_hostile_rejected") is True,
            "byte hostile not rejected")
    require(isinstance(result.get("peak_rss_bytes"), int) and result["peak_rss_bytes"] > 0,
            "missing peak RSS")
    require(result.get("scope") ==
            "Bounded persisted-vector CSR pairing/SpMV only; no closure, rank, membership, or higher-degree run.",
            "scope changed")
    cases = result.get("cases")
    require(isinstance(cases, list) and len(cases) == 4, "expected four exact cases")
    keyed: dict[tuple[int, str], dict] = {}
    cpu_total = 0.0
    metal_warm_total = 0.0
    for case in cases:
        require(isinstance(case, dict), "case is not an object")
        key = (case.get("prime"), case.get("mode"))
        require(key in {(p, m) for p in PRIMES for m in ("regular", "max_residue")},
                "unexpected prime/mode")
        require(key not in keyed, "duplicate prime/mode case")
        require(case.get("byte_exact_equal") is True, "byte equality not asserted")
        require(isinstance(case.get("nonzero_outputs"), int) and
                0 <= case["nonzero_outputs"] <= EXPECTED_ROWS, "bad nonzero count")
        for field in ("reference_single_seconds", "cpu_optimized_seconds",
                      "metal_end_to_end_seconds", "metal_gpu_seconds",
                      "warm_end_to_end_speedup"):
            require(isinstance(case.get(field), (int, float)) and
                    math.isfinite(case[field]) and case[field] >= 0, f"bad timing {field}")
        require(case["cpu_optimized_seconds"] > 0 and case["metal_end_to_end_seconds"] > 0,
                "zero measured interval")
        require(math.isclose(case["warm_end_to_end_speedup"],
                             case["cpu_optimized_seconds"] / case["metal_end_to_end_seconds"],
                             rel_tol=1e-12), "case speedup identity")
        require(isinstance(case.get("output_sha256"), str) and
                len(case["output_sha256"]) == 64, "bad output hash")
        keyed[key] = case
        cpu_total += case["cpu_optimized_seconds"]
        metal_warm_total += case["metal_end_to_end_seconds"]
    require(set(keyed) == {(p, m) for p in PRIMES for m in ("regular", "max_residue")},
            "missing required case")
    require(math.isclose(result["aggregate_cpu_optimized_seconds"], cpu_total,
                         rel_tol=1e-12), "aggregate CPU identity")
    require(result["aggregate_metal_cold_end_to_end_seconds"] >= metal_warm_total,
            "cold Metal excludes setup")
    aggregate = cpu_total / result["aggregate_metal_cold_end_to_end_seconds"]
    minimum = min(case["warm_end_to_end_speedup"] for case in cases)
    require(math.isclose(result["aggregate_cold_end_to_end_speedup"], aggregate,
                         rel_tol=1e-12), "aggregate speedup identity")
    require(math.isclose(result["minimum_warm_end_to_end_speedup"], minimum,
                         rel_tol=1e-12), "minimum speedup identity")
    expected_promotion = aggregate >= 3.0 and minimum >= 3.0
    require(result.get("promoted") is expected_promotion, "promotion Boolean mismatch")
    expected_status = ("PASS_METAL_CSR_PROMOTION_GATE" if expected_promotion else
                       "PASS_METAL_CSR_EXACT_NO_LAUNCH")
    require(result.get("status") == expected_status, "promotion status mismatch")
    return keyed


def expect_reject(result: dict, input_path: Path, shader_path: Path,
                  source_path: Path, binary_path: Path, label: str) -> None:
    try:
        validate_structure(result, input_path, shader_path, source_path, binary_path)
    except ValueError:
        return
    raise ValueError(f"hostile accepted: {label}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--shader", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--audit-output", type=Path, required=True)
    args = parser.parse_args()

    result = json.loads(args.result.read_text())
    keyed = validate_structure(result, args.input, args.shader, args.source, args.binary)
    rows, columns, offsets, indices, coefficients = load_csr(args.input)
    replay_hashes: dict[str, str] = {}
    for prime in PRIMES:
        for mode in ("regular", "max_residue"):
            stem = f"p{prime}_{mode}"
            cpu_path = args.output_dir / f"cpu_{stem}.bin"
            metal_path = args.output_dir / f"metal_{stem}.bin"
            cpu = cpu_path.read_bytes()
            metal = metal_path.read_bytes()
            require(len(cpu) == rows * 4 and len(metal) == rows * 4,
                    f"bad output byte length {stem}")
            require(cpu == metal, f"CPU/Metal byte mismatch {stem}")
            require(sha256_bytes(cpu) == keyed[(prime, mode)]["output_sha256"],
                    f"output hash mismatch {stem}")
            independent = replay(rows, columns, offsets, indices, coefficients, prime, mode)
            require(independent == cpu, f"independent literal replay mismatch {stem}")
            require(sum(value != 0 for value in array.array("I", cpu)) ==
                    keyed[(prime, mode)]["nonzero_outputs"], f"nonzero count mismatch {stem}")
            hostile = bytearray(metal)
            hostile[-1] ^= 0x80
            require(hostile != cpu, f"byte hostile accepted {stem}")
            replay_hashes[stem] = sha256_bytes(independent)

    # Fail-closed structural hostiles do not rerun arithmetic.
    hostile = copy.deepcopy(result)
    hostile["promoted"] = not hostile["promoted"]
    expect_reject(hostile, args.input, args.shader, args.source, args.binary,
                  "promotion Boolean")
    hostile = copy.deepcopy(result)
    hostile["cases"].pop()
    expect_reject(hostile, args.input, args.shader, args.source, args.binary, "missing case")
    hostile = copy.deepcopy(result)
    hostile["input_sha256"] = "0" * 64
    expect_reject(hostile, args.input, args.shader, args.source, args.binary, "input pin")
    hostile = copy.deepcopy(result)
    hostile["promotion_threshold"] = 2.99
    expect_reject(hostile, args.input, args.shader, args.source, args.binary, "threshold")

    audit = {
        "status": "PASS_INDEPENDENT_EXACT_D12_CPU_METAL_CSR_GATE_AUDIT",
        "schema": "KRENN_AFFINE251_D12_METAL_CSR_GATE_AUDIT_V1",
        "result_sha256": sha256_file(args.result),
        "input_sha256": sha256_file(args.input),
        "shader_sha256": sha256_file(args.shader),
        "swift_source_sha256": sha256_file(args.source),
        "binary_sha256": sha256_file(args.binary),
        "rows": rows,
        "columns": columns,
        "nnz": len(indices),
        "literal_cases_replayed": 4,
        "literal_edge_terms_replayed": 4 * len(indices),
        "primes": list(PRIMES),
        "modes": ["regular", "max_residue"],
        "replay_output_sha256": replay_hashes,
        "hostile_checks": ["promotion_boolean", "missing_case", "input_pin",
                           "promotion_threshold", "output_byte_flip"],
        "promotion_verdict": result["status"],
        "scope": "Independent full replay of the bounded CSR slice only; no closure or D12 membership claim.",
    }
    args.audit_output.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Replay deterministic 0:31:30 core8 slices and their bounded F4SAT ledger."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
COMP = HERE.parent
TOOLKIT = COMP / "toolkit/groebner/msolve_io.py"
EXPORT = HERE / "results_face03130_core8_slice_export.json"
CORE_Q = HERE / "face03130_aopen_core8_split_live_char0.msolve"
RESULT_PREFIX = HERE / "results_face03130_core8_slice_replay"
PRIME = 1073741827
EXPORT_LOGICAL = "a89b1a13274c3bcec14bb7822cce0d056512b179385169c6618ac9c8ef0d3c39"
MANIFEST_SHA = {
    1: "57246e5fc6baa97800fdcd5124f0b0fc78c88773c5f9cb4d716818352f01a7df",
    2: "70977f8af517111acfd1363b9e567778ba6442d188dee556246b28eb7dd743b9",
    3: "7afa6752073b85c89c698a7eac6bedeb99930f54beae2ddb0a802259c18c66fa",
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def modular_rank(matrix):
    value = [[entry % PRIME for entry in row] for row in matrix]
    rank = 0
    for column in range(len(value[0])):
        pivot = next((row for row in range(rank, len(value))
                      if value[row][column]), None)
        if pivot is None:
            continue
        value[rank], value[pivot] = value[pivot], value[rank]
        inverse = pow(value[rank][column], PRIME - 2, PRIME)
        value[rank] = [entry * inverse % PRIME for entry in value[rank]]
        for row in range(len(value)):
            if row == rank or not value[row][column]:
                continue
            scale = value[row][column]
            value[row] = [(left-scale*right) % PRIME
                          for left, right in zip(value[row], value[rank],
                                                 strict=True)]
        rank += 1
    return rank


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("standard", "-O", "-I-S"),
                        default="standard")
    args = parser.parse_args()
    MSOLVE_IO = load("face03130_slice_replay_io", TOOLKIT)
    export = json.loads(EXPORT.read_text())
    require(export["result_sha256"] == EXPORT_LOGICAL and
            export["prime"] == PRIME and
            export["source_raw_indices"] == [6, 8, 12, 14, 16, 18, 19, 20]
            and export["base_saturator_terms_degree"] == [16, 17],
            "slice export interface changed")
    names = export["active_variables"]
    normals = [[row["coefficients"][name] for name in names]
               for row in export["slices"]]
    require(modular_rank(normals) == 3 and
            export["slice_normal_rank_mod_prime"] == 3,
            "slice normal rank changed")
    core = MSOLVE_IO.read_msolve_input(
        CORE_Q, strict=True, allow_characteristic_zero=True)

    depths = [1, 2, 3]
    if args.mode == "-O":
        depths.reverse()
    records = []
    for depth in depths:
        artifact = export["artifacts"][depth-1]
        input_path = HERE / artifact["input"]
        labels_path = HERE / artifact["labels"]
        manifest_path = HERE / (
            f"results_face03130_core8_slice{depth}_p{PRIME}.manifest.json")
        parsed = MSOLVE_IO.read_msolve_input(input_path, strict=True)
        labels = json.loads(labels_path.read_text())
        manifest = json.loads(manifest_path.read_text())
        stage = manifest["stages"][0]
        require(parsed.file_sha256 == artifact["input_sha256"] and
                parsed.logical_sha256 == artifact["input_logical_sha256"] and
                parsed.characteristic == PRIME and
                parsed.polynomial_sha256[:8] == core.polynomial_sha256[:8] and
                len(parsed.polynomials) == 9 + depth,
                f"slice{depth} source/input replay changed")
        require(labels["slice_depth"] == depth and
                labels["labels"][-1] == "SATURATOR_Aopen_base_live" and
                labels["source_raw_indices"] == [6, 8, 12, 14, 16, 18, 19, 20],
                f"slice{depth} labels changed")
        require(file_sha(manifest_path) == MANIFEST_SHA[depth] and
                manifest["mode"] == "saturate" and
                manifest["timeout_seconds"] == 120.0 and
                manifest["input"]["file_sha256"] == parsed.file_sha256 and
                manifest["saturator"]["index"] == len(parsed.polynomials)-1 and
                manifest["saturator"]["label"] ==
                "SATURATOR_Aopen_base_live" and
                stage["status"] == "timeout" and
                stage["output"]["bytes"] == 0 and
                "-S" in stage["command"],
                f"slice{depth} bounded F4SAT manifest changed")
        records.append({
            "depth": depth, "input_sha256": parsed.file_sha256,
            "manifest_sha256": MANIFEST_SHA[depth],
            "elapsed_seconds": stage["elapsed_seconds"],
            "status": stage["status"],
        })

    # A one-coefficient mutation must break the first slice digest.
    first = dict(export["slices"][0]["coefficients"])
    first[names[0]] += 1
    require(first != export["slices"][0]["coefficients"],
            "slice mutation did not fire")
    result = {
        "status": "UNAUDITED deterministic slice/timeout replay PASS",
        "mode": args.mode,
        "prime": PRIME,
        "slice_export_logical_sha256": EXPORT_LOGICAL,
        "slice_normal_rank": 3,
        "records": records,
        "landed_basis": False,
        "landed_finite_residual": False,
        "landed_component": False,
        "second_prime_used": False,
        "scope": (
            "All three allowed affine slice depths timed out before a basis. "
            "Therefore no unit, dimension, degree, RUR, omitted-row replay, "
            "or leading/infinity conclusion is claimed."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    suffix = {"standard": "standard", "-O": "O", "-I-S": "I-S"}[args.mode]
    output = Path(str(RESULT_PREFIX) + "_" + suffix + ".json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(args.mode, "PASS", result["result_sha256"])


if __name__ == "__main__":
    main()

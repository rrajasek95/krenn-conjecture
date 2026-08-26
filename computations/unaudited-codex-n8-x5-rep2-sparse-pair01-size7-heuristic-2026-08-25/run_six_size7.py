#!/usr/bin/env python3
"""Run the six fixed-base-minimum supports as movable-base heuristic Q charts."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep2-sparse-pair01-quadruple-hitting-design-2026-08-25"
BOUNDARY = ROOT / "computations/unaudited-codex-n8-x5-rep2-sparse-pair01-boundary-2026-08-25"
PINS = {
    DESIGN / "MANIFEST.sha256": "c695ff1a5b5f7f57f2eb15c9bc6dd00b1d4ff3dc4458e7f343f08ff552fe5f00",
    DESIGN / "hitting_support_ledger.json": "10e4d17195c82c01e2ff8b194f29c1453535684538cc154534d1a5a90c27b9da",
    BOUNDARY / "generate_sparse_pair01.py": "635049c3df63a3a078c1b03a0e99c20867e97acf3ce8c405d0641715242b42b9",
    Path("/usr/local/bin/Singular"): "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main():
    assert __debug__
    for path, digest in PINS.items():
        assert sha256(path) == digest, path
    design = json.loads((DESIGN / "hitting_support_ledger.json").read_text())
    supports = design["minimum_fixed_base_hitting_supports"]
    assert design["minimum_fixed_base_hitting_size"] == 7
    assert design["minimum_fixed_base_hitting_support_count"] == len(supports) == 6
    generator = load(BOUNDARY / "generate_sparse_pair01.py")
    generator.HERE = HERE
    attempts = []
    for index, support in enumerate(supports):
        label = f"size7_{index}"
        generated = generator.build(generator.BASE_LIVE | set(support), label)
        destination = HERE / generated["path"]
        started = time.monotonic()
        process = subprocess.run(
            ["gtimeout", "10", "Singular", str(destination)], capture_output=True,
            text=True, timeout=12,
        )
        wall = time.monotonic() - started
        stdout = process.stdout + process.stderr
        if process.returncode == 0 and "STATUS=NONUNIT" in stdout:
            status = "NONUNIT"
        elif process.returncode == 0 and "STATUS=UNIT_IDEAL" in stdout:
            status = "UNIT_IDEAL"
        else:
            status = "FAIL_CLOSED_TIMEOUT_OR_PROCESS"
        stdout_path = HERE / f"stdout_size7_{index}.txt"
        temporary = stdout_path.with_suffix(".txt.tmp")
        temporary.write_text(stdout)
        os.replace(temporary, stdout_path)
        attempts.append({
            "index": index,
            "support": support,
            "input": destination.name,
            "input_sha256": sha256(destination),
            "stdout": stdout_path.name,
            "stdout_sha256": sha256(stdout_path),
            "returncode": process.returncode,
            "wall_seconds": wall,
            "status": status,
            "input_generators": int(re.search(r"INPUT_GENERATORS=(\d+)", stdout).group(1))
                if re.search(r"INPUT_GENERATORS=(\d+)", stdout) else None,
            "groebner_size": int(re.search(r"GROEBNER_SIZE=(\d+)", stdout).group(1))
                if re.search(r"GROEBNER_SIZE=(\d+)", stdout) else None,
            "unit_remainder": re.search(r"UNIT_REMAINDER=([^\n]+)", stdout).group(1).strip()
                if re.search(r"UNIT_REMAINDER=([^\n]+)", stdout) else None,
        })
        if status == "FAIL_CLOSED_TIMEOUT_OR_PROCESS":
            break
    complete = len(attempts) == 6 and all(item["status"] != "FAIL_CLOSED_TIMEOUT_OR_PROCESS" for item in attempts)
    nonunit = [item for item in attempts if item["status"] == "NONUNIT"]
    result = {
        "schema": "KRENN_X5_REP2_SIZE7_HEURISTIC_MOVABLE_BASE_RUN_V1",
        "status": (
            "PASS_TERMINAL_WITH_NONUNIT" if complete and nonunit
            else "PASS_ALL_SIX_UNIT" if complete
            else "FAIL_CLOSED_INCOMPLETE"
        ),
        "pins": {str(path): digest for path, digest in PINS.items()},
        "attempts": attempts,
        "unit_count": sum(item["status"] == "UNIT_IDEAL" for item in attempts),
        "nonunit_count": len(nonunit),
        "failure_count": sum(item["status"].startswith("FAIL") for item in attempts),
        "per_lane_wall_cap_seconds": 10,
        "scope": {
            "base_coordinates_movable": True,
            "fixed_base_hitting_theorem_used_as_filter": False,
            "selection_only": "six heuristic supports came from the fixed-base theorem",
            "equations": "full257 pair01 amplitudes only; guard/adjoint/incidence/rank excluded",
        },
    }
    atomic_json(HERE / "results_size7.json", result)
    print(json.dumps({
        "status": result["status"],
        "unit": result["unit_count"],
        "nonunit": result["nonunit_count"],
        "failure": result["failure_count"],
        "walls": [round(item["wall_seconds"], 4) for item in attempts],
    }, sort_keys=True))


if __name__ == "__main__":
    main()

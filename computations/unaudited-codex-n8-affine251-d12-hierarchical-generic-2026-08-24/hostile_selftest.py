#!/usr/bin/env python3
"""Parser-level fail-closed tests for the generic hierarchical interface."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent
BINARY = ROOT / "sealed_v3/sparse_d12_dual"
BINARY_SHA256 = "8625721373d2880432ca5bdc18b277ca474adedf3a451d321c5ca65e6db3727a"
REQUIRED = "hierarchical elimination requires explicit --workers 16 --pivot rare --strategy cold --incremental no"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if sha256(BINARY) != BINARY_SHA256:
        raise AssertionError("binary pin")
    cases = [
        ("workers", "--workers", "8", REQUIRED),
        ("pivot", "--pivot", "auto", REQUIRED),
        ("strategy", "--strategy", "repair", REQUIRED),
        ("incremental", "--incremental", "yes",
         "incremental mode requires tree elimination"),
        ("bad_kernel", "--elimination", "hierarchicalx",
         "bad sparse elimination kernel"),
    ]
    records = []
    with tempfile.TemporaryDirectory(prefix="d12-hierarchical-hostile-") as temporary:
        work = Path(temporary)
        base = [
            str(BINARY), "--input", str(work / "absent.ms"),
            "--output", str(work / "result.json"),
            "--checkpoint", str(work / "checkpoint.bin"),
            "--vector-cache", str(work / "vectors.bin"),
            "--dual", str(work / "dual.tsv"),
            "--prime", "1073741827", "--wall-seconds", "120",
            "--rss-gib", "36", "--workers", "16", "--pivot", "rare",
            "--strategy", "cold", "--elimination", "hierarchical",
            "--incremental", "no", "--portfolio-period", "256",
            "--portfolio-parallel", "yes", "--support-cap", "100000",
            "--column-cap", "1000000", "--round-cap", "749",
        ]
        for name, flag, replacement, expected in cases:
            command = base.copy()
            position = command.index(flag)
            command[position + 1] = replacement
            run = subprocess.run(command, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True, check=False)
            if run.returncode == 0 or expected not in run.stderr:
                raise AssertionError(f"hostile did not fail closed: {name}: {run.stderr}")
            if any(work.iterdir()):
                raise AssertionError(f"hostile wrote output: {name}")
            records.append({"case": name, "returncode": run.returncode,
                            "expected_guard": expected, "wrote_output": False})
    result = {
        "schema": "KRENN_AFFINE251_D12_HIERARCHICAL_GENERIC_HOSTILES_V1",
        "status": "PASS",
        "scope": "Parser-level hierarchical selection guards; no solve.",
        "binary_sha256": BINARY_SHA256,
        "cases": records,
    }
    path = ROOT / "results_hostile_selftest.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


if __name__ == "__main__":
    main()

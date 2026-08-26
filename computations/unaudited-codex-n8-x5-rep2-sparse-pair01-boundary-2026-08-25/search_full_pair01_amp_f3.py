#!/usr/bin/env python3
"""Exact F3 model search for amplitude-only full pair01, used to seed support."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-seven-block-rep2-tensor-flattening-2026-08-25"


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    source_path = PARENT / "search_pair01_fp.py"
    assert sha256(source_path) == "2e0396f924cc6baeb184a2e2a7eddc88148463f48a152d1def2c8f3bacb479ee"
    source = load(source_path)
    full, variables, labels = source.build(3)
    lines = []
    selected = []
    for line in full.splitlines():
        if line.startswith("(set-logic") or line.startswith("(declare-const") or "(bvult" in line:
            lines.append(line)
        elif line.startswith("(assert") and "; amp_" in line:
            lines.append(line)
            selected.append(line.rsplit("; ", 1)[1])
    assert len(selected) == 257
    lines.extend(("(check-sat)", "(get-model)"))
    smt = HERE / "rep2_full_pair01_amp_f3.smt2"
    temporary = smt.with_suffix(".smt2.tmp")
    temporary.write_text("\n".join(lines) + "\n")
    os.replace(temporary, smt)
    process = subprocess.run(
        ["z3", "-T:60", str(smt)], capture_output=True, text=True, timeout=65
    )
    stdout = process.stdout + process.stderr
    output = HERE / "rep2_full_pair01_amp_f3.stdout"
    temporary = output.with_suffix(".stdout.tmp")
    temporary.write_text(stdout)
    os.replace(temporary, output)
    status = next((line for line in stdout.splitlines() if line in {"sat", "unsat", "unknown"}), "WALL_CAP")
    result = {
        "schema": "KRENN_X5_REP2_FULL_PAIR01_AMPLITUDE_F3_SEARCH_V1",
        "status": status,
        "returncode": process.returncode,
        "equations": len(selected),
        "variables": len(variables),
        "wall_cap_seconds": 60,
        "scope": "amplitude-only full pair01; no guard, adjoint, incidence, or rank assertion",
    }
    path = HERE / "results_full_pair01_amp_f3.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Search the exact 43-amplitude F2 core over an odd prime."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name):
    path = HERE / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=3)
    parser.add_argument("--wall", type=int, default=60)
    args = parser.parse_args()
    source = load_module("search_pair01_fp.py")
    full, variables, _ = source.build(args.prime)
    core = json.loads((HERE / "results_f2_core43.json").read_text())
    labels = {"amp_" + word for word in core["amplitude_words"]}
    lines = []
    selected = []
    for line in full.splitlines():
        if line.startswith("(set-logic") or line.startswith("(declare-const") or "(bvult" in line:
            lines.append(line)
        elif line.startswith("(assert") and "; amp_" in line:
            label = line.rsplit("; ", 1)[1]
            if label in labels:
                lines.append(line)
                selected.append(label)
    assert set(selected) == labels and len(selected) == 43
    lines.extend(("(check-sat)", "(get-model)"))
    smt = HERE / f"rep2_core43_f{args.prime}.smt2"
    temporary = smt.with_suffix(".smt2.tmp")
    temporary.write_text("\n".join(lines) + "\n")
    os.replace(temporary, smt)
    try:
        process = subprocess.run(
            ["z3", f"-T:{args.wall}", str(smt)], capture_output=True, text=True,
            timeout=args.wall + 5,
        )
        output = process.stdout + process.stderr
        returncode = process.returncode
    except subprocess.TimeoutExpired as exception:
        output = (exception.stdout or "") + (exception.stderr or "")
        returncode = 124
    stdout = HERE / f"rep2_core43_f{args.prime}.stdout"
    temporary = stdout.with_suffix(".stdout.tmp")
    temporary.write_text(output)
    os.replace(temporary, stdout)
    status = next((line for line in output.splitlines() if line in {"sat", "unsat", "unknown"}), "WALL_CAP")
    result = {
        "schema": "KRENN_X5_REP2_CORE43_ODD_PRIME_SEARCH_V1",
        "field": args.prime,
        "variables": len(variables),
        "equations": len(selected),
        "status": status,
        "returncode": returncode,
        "wall_cap_seconds": args.wall,
        "scope": "deletion-minimal 43 amplitude equations only",
    }
    path = HERE / f"results_core43_f{args.prime}.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

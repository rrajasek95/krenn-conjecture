#!/usr/bin/env python3
"""Exact F3 sparse-support seed search for full pair01 amplitudes."""

from __future__ import annotations

import argparse
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=int, required=True)
    parser.add_argument("--wall", type=int, default=60)
    args = parser.parse_args()
    assert 0 <= args.cap <= 70
    fp = load(PARENT / "search_pair01_fp.py")
    generator = load(HERE / "generate_sparse_pair01.py")
    full, variables, _ = fp.build(3)
    zero = sorted(set(variables) - set(generator.BASE_LIVE))
    # DUAL/incidence variables do not occur in the amplitude-only system and
    # are excluded from the support cap.  Use precisely the 87 amplitude vars.
    core = generator.load_core()
    amplitude_vars = set(core.SOURCE.values()) | set(core.U) | set(core.V)
    zero = sorted(amplitude_vars - generator.BASE_LIVE)
    assert len(zero) == 70
    lines = []
    selected = 0
    for line in full.splitlines():
        if line.startswith("(set-logic") or line.startswith("(declare-const") or "(bvult" in line:
            lines.append(line)
        elif line.startswith("(assert") and "; amp_" in line:
            lines.append(line)
            selected += 1
    assert selected == 257
    nonzero = [f"(not (= {name} #x00))" for name in zero]
    lines.append(f"(assert ((_ at-most {args.cap}) {' '.join(nonzero)}))")
    lines.extend(("(check-sat)", "(get-model)"))
    smt = HERE / f"rep2_pair01_amp_f3_sparse_cap{args.cap}.smt2"
    temporary = smt.with_suffix(".smt2.tmp")
    temporary.write_text("\n".join(lines) + "\n")
    os.replace(temporary, smt)
    process = subprocess.run(
        ["z3", f"-T:{args.wall}", str(smt)], capture_output=True, text=True,
        timeout=args.wall + 5,
    )
    stdout = process.stdout + process.stderr
    stdout_path = HERE / f"rep2_pair01_amp_f3_sparse_cap{args.cap}.stdout"
    temporary = stdout_path.with_suffix(".stdout.tmp")
    temporary.write_text(stdout)
    os.replace(temporary, stdout_path)
    status = next((line for line in stdout.splitlines() if line in {"sat", "unsat", "unknown"}), "WALL_CAP")
    result = {
        "schema": "KRENN_X5_REP2_PAIR01_AMP_F3_SPARSE_SEARCH_V1",
        "status": status,
        "field": 3,
        "extra_coordinate_cap": args.cap,
        "amplitude_equations": selected,
        "base_live_count": len(generator.BASE_LIVE),
        "candidate_zero_count": len(zero),
        "returncode": process.returncode,
        "wall_cap_seconds": args.wall,
        "scope": "diagnostic seed only; characteristic-three result is not a Q theorem",
    }
    path = HERE / f"results_sparse_cap{args.cap}_f3.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

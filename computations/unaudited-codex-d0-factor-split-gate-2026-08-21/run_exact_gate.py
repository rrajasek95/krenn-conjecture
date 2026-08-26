#!/usr/bin/env python3
"""Run the one canonical exact-Q D0 residual gate with a hard time cap."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time


HERE = Path(__file__).resolve().parent
INPUT = HERE / "d0_A_U2_three_cofactor_pivot_open_char0.msolve"
OUTPUT = HERE / "d0_A_U2_three_cofactor_pivot_open_char0.out"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    command = ["msolve", "-f", str(INPUT), "-o", str(OUTPUT),
               "-t", "8", "-g", "1", "-v", "1", "-l", "2"]
    start = time.monotonic()
    run = subprocess.run(command, capture_output=True, text=True, timeout=600,
                         cwd=HERE)
    elapsed = time.monotonic() - start
    stdout_path = HERE / "d0_A_U2_three_cofactor_pivot_open_char0.stdout.log"
    stderr_path = HERE / "d0_A_U2_three_cofactor_pivot_open_char0.stderr.log"
    stdout_path.write_text(run.stdout)
    stderr_path.write_text(run.stderr)
    if run.returncode != 0:
        raise SystemExit(f"msolve failed with exit code {run.returncode}")
    if not OUTPUT.exists() or "[1]:" not in OUTPUT.read_text():
        raise SystemExit("exact output is not the unit basis [1]")
    record = {
        "command": command,
        "timeout_seconds": 600,
        "elapsed_seconds": elapsed,
        "returncode": run.returncode,
        "input_sha256": digest(INPUT),
        "output_sha256": digest(OUTPUT),
        "stdout_sha256": digest(stdout_path),
        "stderr_sha256": digest(stderr_path),
        "status": "exact characteristic-zero unit basis [1]",
        "scope": ("A=U2=0 representative on the selected-pivot-open D0/C0 "
                  "chart, with the literal Cof(1,3),Cof(2,3),Cof(3,3) packet."),
    }
    (HERE / "results_d0_factor_split_exact_run.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n")
    print("exact D0 factor-split gate PASS", f"{elapsed:.3f}s", digest(OUTPUT))


if __name__ == "__main__":
    main()

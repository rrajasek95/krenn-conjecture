#!/usr/bin/env python3
"""Run the exact R0=R1 gate under a hard 600-second cap."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time


HERE = Path(__file__).resolve().parent
INPUT = HERE / "d0_pivot_zero_R0_R1_char0.msolve"
OUTPUT = HERE / "d0_pivot_zero_R0_R1_char0.out"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    command = ["msolve", "-f", str(INPUT), "-o", str(OUTPUT),
               "-t", "8", "-g", "1", "-v", "1", "-l", "2"]
    started = time.monotonic()
    try:
        run = subprocess.run(command, capture_output=True, text=True,
                             timeout=600, cwd=HERE)
        status = "completed"
    except subprocess.TimeoutExpired as error:
        run, status = error, "timeout"
    elapsed = time.monotonic()-started
    stdout, stderr = run.stdout or "", run.stderr or ""
    if isinstance(stdout, bytes): stdout = stdout.decode(errors="replace")
    if isinstance(stderr, bytes): stderr = stderr.decode(errors="replace")
    stdout_path = HERE / "d0_pivot_zero_R0_R1_char0.stdout.log"
    stderr_path = HERE / "d0_pivot_zero_R0_R1_char0.stderr.log"
    stdout_path.write_text(stdout); stderr_path.write_text(stderr)
    returncode = getattr(run, "returncode", None)
    unit = OUTPUT.exists() and "[1]:" in OUTPUT.read_text()
    result = {
        "command": command, "timeout_seconds": 600,
        "elapsed_seconds": elapsed, "process_status": status,
        "returncode": returncode, "unit_basis": unit,
        "input_sha256": digest(INPUT),
        "output_sha256": digest(OUTPUT) if OUTPUT.exists() else None,
        "stdout_sha256": digest(stdout_path), "stderr_sha256": digest(stderr_path),
        "scope": "Corrected O1 R0=R1; guaranteed Delta/base localization only; R2 unrestricted.",
    }
    (HERE / "results_d0_pivot_zero_R0_R1_exact_run.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 pivot-zero R0/R1 gate", status, f"{elapsed:.3f}s",
          "unit", unit, "returncode", returncode)
    if status != "completed" or returncode != 0 or not unit:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

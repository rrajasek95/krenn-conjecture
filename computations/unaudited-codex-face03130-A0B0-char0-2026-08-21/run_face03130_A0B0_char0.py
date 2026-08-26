#!/usr/bin/env python3
"""Run the single exact stage-1 A=B=0 gate under a 600-second cap."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time


HERE = Path(__file__).resolve().parent
INPUT = HERE / "face03130_A0B0_base_live_char0.msolve"
OUTPUT = HERE / "face03130_A0B0_base_live_char0.out"
RESULT = HERE / "results_face03130_A0B0_base_live_exact_run.json"


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
    elapsed = time.monotonic() - started
    stdout, stderr = run.stdout or "", run.stderr or ""
    if isinstance(stdout, bytes):
        stdout = stdout.decode(errors="replace")
    if isinstance(stderr, bytes):
        stderr = stderr.decode(errors="replace")
    stdout_path = HERE / "face03130_A0B0_base_live_char0.stdout.log"
    stderr_path = HERE / "face03130_A0B0_base_live_char0.stderr.log"
    stdout_path.write_text(stdout); stderr_path.write_text(stderr)
    returncode = getattr(run, "returncode", None)
    output_text = OUTPUT.read_text() if OUTPUT.exists() else ""
    unit = "[1]:" in output_text or output_text.strip() == "[-1]"
    positive_dimensional = ("[1,5,-1,[]]" in output_text or
                            "dimension" in output_text.lower() and
                            "positive" in output_text.lower())
    result = {
        "command": command, "timeout_seconds": 600,
        "elapsed_seconds": elapsed, "process_status": status,
        "returncode": returncode, "unit_basis": unit,
        "positive_dimensional_envelope": positive_dimensional,
        "input_sha256": digest(INPUT),
        "output_sha256": digest(OUTPUT) if OUTPUT.exists() else None,
        "output_bytes": OUTPUT.stat().st_size if OUTPUT.exists() else 0,
        "stdout_sha256": digest(stdout_path), "stderr_sha256": digest(stderr_path),
        "scope": ("Exact-Q 0:31:30 A=B=0 with all 16 literal rows and only "
                  "the original selected-base/both-live/c live product; H not localized."),
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("face03130 A=B=0 stage1", status, f"{elapsed:.3f}s",
          "rc", returncode, "unit", unit, "posdim", positive_dimensional,
          "bytes", result["output_bytes"])
    if status != "completed" or returncode != 0:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run the single bounded modular isolated-support F4SAT gate."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
INPUT = HERE / "isolated_support_full_live_p1073741827.msolve"
STDOUT = HERE / "isolated_support_full_live_p1073741827.gb.out"
STDERR = HERE / "isolated_support_full_live_p1073741827.stderr.log"
MANIFEST = HERE / "results_isolated_support_f4sat_manifest.json"
PIDFILE = HERE / "isolated_support_f4sat.pid"
MSOLVE = Path("/usr/local/bin/msolve")
CAP_SECONDS = 300
MEMORY_BYTES = 12 * 1024**3


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    command = [str(MSOLVE), "-f", str(INPUT), "-S", "-g", "2", "-t", "4"]
    started = time.monotonic()
    status = "UNKNOWN"
    returncode = None
    with STDOUT.open("wb") as stdout, STDERR.open("wb") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr)
        PIDFILE.write_text(str(process.pid) + "\n")
        try:
            process.wait(timeout=CAP_SECONDS)
            status = "COMPLETED"
        except subprocess.TimeoutExpired:
            status = "TIMEOUT"
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        returncode = process.returncode
    PIDFILE.unlink(missing_ok=True)
    elapsed = time.monotonic() - started
    output = STDOUT.read_text(errors="replace")
    unit = ("#length of basis:      1 element" in output
            and output.rstrip().endswith("[1]:"))
    if status == "COMPLETED" and returncode == 0 and unit:
        status = "MODULAR_UNIT"
    elif status == "COMPLETED" and returncode == 0:
        status = "MODULAR_COMPLETED_NONUNIT_OR_UNPARSED"
    manifest = {
        "format": "n8-chart1-isolated-support-f4sat-run-v1",
        "status": status,
        "scope": (
            "One prime-field native F4SAT discovery gate. MODULAR_UNIT would "
            "exclude this support over the displayed prime only until an "
            "exact-Q source certificate is reconstructed. Timeout/nonunit is "
            "not a feasibility result."
        ),
        "command": command,
        "hard_cap_seconds": CAP_SECONDS,
        "memory_cap_requested_bytes": MEMORY_BYTES,
        "memory_cap_enforcement": (
            "workspace sandbox rejects setrlimit and process RSS inspection; "
            "the requested 12GB cap could not be independently enforced"
        ),
        "elapsed_seconds": elapsed,
        "returncode": returncode,
        "unit_basis_parsed": unit,
        "files": {
            INPUT.name: {"bytes": INPUT.stat().st_size, "sha256": digest(INPUT)},
            STDOUT.name: {"bytes": STDOUT.stat().st_size, "sha256": digest(STDOUT)},
            STDERR.name: {"bytes": STDERR.stat().st_size, "sha256": digest(STDERR)},
        },
    }
    logical = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    manifest["logical_sha256"] = sha256(logical.encode()).hexdigest()
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

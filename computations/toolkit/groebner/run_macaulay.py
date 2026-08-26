#!/usr/bin/env python3
"""Manifested wrapper for the anchor-k-echelon modular Macaulay solver."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import subprocess
import time

from msolve_io import file_sha256
from run_msolve import process_rss_kb


TOOLKIT_VERSION = "1"


def atomic_json(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--prime", action="append", type=int, required=True)
    parser.add_argument("--timeout", type=float)
    parser.add_argument("--source", action="append", type=Path, default=[])
    parser.add_argument("--scope", required=True)
    args = parser.parse_args()

    if not args.input.is_file() or not args.solver.is_file():
        raise SystemExit("missing Macaulay input or solver")
    if len(set(args.prime)) != len(args.prime):
        raise SystemExit("duplicate --prime")
    args.output_prefix.parent.mkdir(parents=True, exist_ok=True)
    manifest_path = Path(str(args.output_prefix) + ".manifest.json")
    manifest = {
        "toolkit_version": TOOLKIT_VERSION,
        "proof_status": "modular_discovery_requires_independent_replay",
        "scope": args.scope,
        "created_unix": time.time(),
        "host": platform.platform(), "cwd": os.getcwd(),
        "solver": {"path": str(args.solver),
                   "sha256": file_sha256(args.solver)},
        "input": {"path": str(args.input),
                  "bytes": args.input.stat().st_size,
                  "sha256": file_sha256(args.input)},
        "sources": [{"path": str(path), "sha256": file_sha256(path)}
                    for path in args.source],
        "primes": args.prime, "timeout_seconds": args.timeout,
        "runs": [],
    }
    atomic_json(manifest_path, manifest)

    for prime in args.prime:
        output = Path(str(args.output_prefix) + f".p{prime}.json")
        stdout_path = Path(str(args.output_prefix) + f".p{prime}.stdout.log")
        stderr_path = Path(str(args.output_prefix) + f".p{prime}.stderr.log")
        command = [str(args.solver), "solve", str(args.input),
                   str(output), str(prime)]
        started = time.monotonic()
        peak_rss_kb = 0
        timed_out = False
        with stdout_path.open("w") as stdout, stderr_path.open("w") as stderr:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                       text=True)
            while process.poll() is None:
                rss = process_rss_kb(process.pid)
                if rss is not None:
                    peak_rss_kb = max(peak_rss_kb, rss)
                if (args.timeout is not None and
                        time.monotonic() - started >= args.timeout):
                    timed_out = True
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                    break
                time.sleep(0.5)
        valid_json = False
        json_error = None
        if output.is_file() and output.stat().st_size:
            try:
                json.loads(output.read_text())
                valid_json = True
            except Exception as error:
                json_error = f"{type(error).__name__}: {error}"
        status = ("timeout" if timed_out else
                  "process_error" if process.returncode != 0 else
                  "invalid_output" if not valid_json else "completed")
        record = {
            "prime": prime, "command": command, "status": status,
            "elapsed_seconds": time.monotonic() - started,
            "peak_rss_kb": peak_rss_kb, "returncode": process.returncode,
            "stdout": {"path": str(stdout_path),
                       "sha256": file_sha256(stdout_path)},
            "stderr": {"path": str(stderr_path),
                       "sha256": file_sha256(stderr_path)},
            "output": {"path": str(output),
                       "bytes": output.stat().st_size if output.exists() else 0,
                       "sha256": file_sha256(output) if valid_json else None},
            "json_error": json_error,
        }
        manifest["runs"].append(record)
        atomic_json(manifest_path, manifest)
        if status != "completed":
            raise SystemExit(f"Macaulay run p={prime} failed: {status}")

    logical = {
        "toolkit_version": manifest["toolkit_version"],
        "proof_status": manifest["proof_status"],
        "scope": manifest["scope"],
        "solver_sha256": manifest["solver"]["sha256"],
        "input_sha256": manifest["input"]["sha256"],
        "source_sha256": [item["sha256"] for item in manifest["sources"]],
        "runs": [{"prime": run["prime"], "status": run["status"],
                  "output_sha256": run["output"]["sha256"]}
                 for run in manifest["runs"]],
    }
    manifest["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    manifest["status"] = "completed_modular_discovery"
    atomic_json(manifest_path, manifest)
    print(f"Macaulay runs: PASS ({manifest['logical_sha256']})")


if __name__ == "__main__":
    main()

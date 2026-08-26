#!/usr/bin/env python3
"""Manifested SpaSM runner with mandatory source-level solution replay."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
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
    parser.add_argument("export_manifest", type=Path)
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--spasm-solve", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--dense-block-size", type=int, default=10000)
    parser.add_argument("--timeout", type=float)
    parser.add_argument("--scope", required=True)
    args = parser.parse_args()
    if args.threads <= 0 or args.dense_block_size <= 0:
        raise SystemExit("threads and dense block size must be positive")

    exported = json.loads(args.export_manifest.read_text())
    if exported.get("format") != "krenn-macaulay-spasm-export-v1":
        raise SystemExit("unsupported SpaSM export manifest")
    matrix = Path(exported["matrix"])
    rhs = Path(exported["rhs"])
    source = Path(exported["source"])
    expected_hashes = ((matrix, exported["matrix_sha256"]),
                       (rhs, exported["rhs_sha256"]),
                       (source, exported["source_sha256"]))
    for path, expected in expected_hashes:
        if not path.is_file() or file_sha256(path) != expected:
            raise SystemExit(f"missing or hash-mismatched input: {path}")
    if not args.spasm_solve.is_file():
        raise SystemExit("SpaSM solve binary missing")

    prefix = args.output_prefix
    prefix.parent.mkdir(parents=True, exist_ok=True)
    manifest_path = Path(str(prefix) + ".manifest.json")
    solution = Path(str(prefix) + ".solution.sms")
    audit = Path(str(prefix) + ".audit.json")
    stdout_path = Path(str(prefix) + ".stdout.log")
    stderr_path = Path(str(prefix) + ".stderr.log")
    command = [str(args.spasm_solve), "-p", str(exported["prime"]),
               f"--dense-block-size={args.dense_block_size}",
               "-m", str(matrix), "-r", str(rhs), "-o", str(solution)]
    environment = os.environ.copy()
    environment.update({"OMP_NUM_THREADS": str(args.threads),
                        "OMP_PROC_BIND": "spread", "OMP_PLACES": "cores"})
    manifest = {
        "toolkit_version": TOOLKIT_VERSION,
        "proof_status": "modular_certificate_requires_exact_Q_lift",
        "scope": args.scope,
        "created_unix": time.time(),
        "host": platform.platform(),
        "python": sys.version,
        "cwd": os.getcwd(),
        "export_manifest": {"path": str(args.export_manifest),
                            "sha256": file_sha256(args.export_manifest)},
        "source_sha256": exported["source_sha256"],
        "matrix_sha256": exported["matrix_sha256"],
        "rhs_sha256": exported["rhs_sha256"],
        "prime": exported["prime"],
        "shape": exported["original_shape"],
        "matrix_nnz": exported["matrix_nnz"],
        "solver": {"path": str(args.spasm_solve),
                   "sha256": file_sha256(args.spasm_solve)},
        "threads": args.threads,
        "dense_block_size": args.dense_block_size,
        "timeout_seconds": args.timeout,
        "command": command,
        "status": "running",
    }
    atomic_json(manifest_path, manifest)

    started = time.monotonic()
    peak_rss_kb = 0
    run_status = "running"
    process = None
    try:
        with stdout_path.open("w") as stdout, stderr_path.open("w") as stderr:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                       text=True, env=environment,
                                       start_new_session=True)
            next_update = started + 60
            while process.poll() is None:
                rss = process_rss_kb(process.pid)
                if rss is not None:
                    peak_rss_kb = max(peak_rss_kb, rss)
                now = time.monotonic()
                if args.timeout is not None and now - started >= args.timeout:
                    run_status = "timeout"
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                    break
                if now >= next_update:
                    print(f"[spasm] elapsed={now-started:.1f}s "
                          f"rss={peak_rss_kb/1024/1024:.2f}GiB", flush=True)
                    next_update += 60
                time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        run_status = "interrupted"
        if process is not None and process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=10)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()

    elapsed = time.monotonic() - started
    status = (run_status if run_status != "running" else
              "process_error" if process.returncode != 0 else
              "missing_solution" if not solution.is_file() or not solution.stat().st_size
              else "solution_pending_replay")
    replay = None
    if status == "solution_pending_replay":
        verifier = Path(__file__).with_name("verify_spasm_solution.py")
        completed = subprocess.run(
            [sys.executable, str(verifier), str(source), str(solution),
             str(audit), str(exported["prime"])],
            text=True, capture_output=True, timeout=600, check=False,
        )
        replay = {"command_stdout": completed.stdout,
                  "command_stderr": completed.stderr,
                  "returncode": completed.returncode}
        if completed.returncode == 0 and audit.is_file():
            replay["audit"] = json.loads(audit.read_text())
            replay["audit_sha256"] = file_sha256(audit)
            status = "completed_verified_modular_solution"
        else:
            status = "solution_replay_failed"

    manifest.update({
        "status": status,
        "elapsed_seconds": elapsed,
        "peak_rss_kb": peak_rss_kb,
        "returncode": process.returncode,
        "stdout": {"path": str(stdout_path), "sha256": file_sha256(stdout_path)},
        "stderr": {"path": str(stderr_path), "sha256": file_sha256(stderr_path)},
        "solution": {"path": str(solution),
                     "bytes": solution.stat().st_size if solution.exists() else 0,
                     "sha256": file_sha256(solution) if solution.exists() else None},
        "replay": replay,
    })
    logical = {
        "status": status, "scope": args.scope,
        "source_sha256": exported["source_sha256"],
        "matrix_sha256": exported["matrix_sha256"],
        "rhs_sha256": exported["rhs_sha256"],
        "solver_sha256": manifest["solver"]["sha256"],
        "prime": exported["prime"],
        "solution_sha256": manifest["solution"]["sha256"],
        "audit_sha256": replay.get("audit_sha256") if replay else None,
    }
    manifest["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    atomic_json(manifest_path, manifest)
    print(f"SpaSM run: {status} ({manifest['logical_sha256']})")
    if status != "completed_verified_modular_solution":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Manifested parallel LinBox/Wiedemann runner with source-level replay."""

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


def sms_shape(path: Path) -> tuple[int, int]:
    with path.open() as stream:
        fields = stream.readline().split()
    if len(fields) != 3 or fields[2] != "M":
        raise SystemExit(f"invalid SMS header: {path}")
    return int(fields[0]), int(fields[1])


def stop_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("export_manifest", type=Path)
    parser.add_argument("--forward-matrix", type=Path, required=True,
                        help="SMS matrix in original equation-by-column orientation")
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--timeout", type=float)
    parser.add_argument("--scope", required=True)
    args = parser.parse_args()
    if args.threads <= 0:
        raise SystemExit("threads must be positive")

    exported = json.loads(args.export_manifest.read_text())
    if exported.get("format") != "krenn-macaulay-spasm-export-v1":
        raise SystemExit("unsupported Macaulay/SMS export manifest")
    transpose = Path(exported["matrix"])
    rhs = Path(exported["rhs"])
    source = Path(exported["source"])
    for path, expected in ((transpose, exported["matrix_sha256"]),
                           (rhs, exported["rhs_sha256"]),
                           (source, exported["source_sha256"])):
        if not path.is_file() or file_sha256(path) != expected:
            raise SystemExit(f"missing or hash-mismatched input: {path}")
    if not args.forward_matrix.is_file() or not args.solver.is_file():
        raise SystemExit("forward matrix or solver missing")
    forward_shape = sms_shape(args.forward_matrix)
    transpose_shape = sms_shape(transpose)
    if forward_shape != tuple(reversed(transpose_shape)):
        raise SystemExit("forward and transpose SMS dimensions disagree")
    if sms_shape(rhs) != (1, forward_shape[0]):
        raise SystemExit("RHS dimensions disagree with forward matrix")

    prefix = args.output_prefix
    prefix.parent.mkdir(parents=True, exist_ok=True)
    manifest_path = Path(str(prefix) + ".manifest.json")
    solution = Path(str(prefix) + ".solution.sms")
    audit = Path(str(prefix) + ".audit.json")
    stdout_path = Path(str(prefix) + ".stdout.log")
    stderr_path = Path(str(prefix) + ".stderr.log")
    command = [str(args.solver), str(args.forward_matrix), str(transpose),
               str(rhs), str(solution), str(exported["prime"])]
    environment = os.environ.copy()
    environment.update({"OMP_NUM_THREADS": str(args.threads),
                        "OMP_PROC_BIND": "spread", "OMP_PLACES": "cores"})
    manifest = {
        "toolkit_version": TOOLKIT_VERSION,
        "proof_status": "modular_certificate_requires_exact_Q_lift",
        "scope": args.scope,
        "created_unix": time.time(),
        "host": platform.platform(), "python": sys.version, "cwd": os.getcwd(),
        "export_manifest": {"path": str(args.export_manifest),
                            "sha256": file_sha256(args.export_manifest)},
        "source_sha256": exported["source_sha256"],
        "forward_matrix": {"path": str(args.forward_matrix),
                           "sha256": file_sha256(args.forward_matrix)},
        "transpose_matrix": {"path": str(transpose),
                             "sha256": exported["matrix_sha256"]},
        "rhs_sha256": exported["rhs_sha256"],
        "prime": exported["prime"], "shape": list(forward_shape),
        "matrix_nnz": exported["matrix_nnz"],
        "solver": {"path": str(args.solver), "sha256": file_sha256(args.solver)},
        "threads": args.threads, "timeout_seconds": args.timeout,
        "command": command, "status": "running",
    }
    atomic_json(manifest_path, manifest)

    started = time.monotonic()
    peak_rss_kb = 0
    status = "running"
    process: subprocess.Popen[str] | None = None
    returncode: int | None = None
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
                    status = "timeout"
                    stop_process(process)
                    break
                if now >= next_update:
                    print(f"[linbox] elapsed={now-started:.1f}s "
                          f"rss={peak_rss_kb/1024/1024:.2f}GiB", flush=True)
                    next_update += 60
                time.sleep(0.5)
            returncode = process.returncode
    except (KeyboardInterrupt, SystemExit):
        status = "interrupted"
        if process is not None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=10)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
            returncode = process.returncode

    elapsed = time.monotonic() - started
    if status == "running":
        status = ("process_error" if returncode != 0 else
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
        "status": status, "elapsed_seconds": elapsed,
        "peak_rss_kb": peak_rss_kb, "returncode": returncode,
        "stdout": {"path": str(stdout_path),
                   "sha256": file_sha256(stdout_path) if stdout_path.exists() else None},
        "stderr": {"path": str(stderr_path),
                   "sha256": file_sha256(stderr_path) if stderr_path.exists() else None},
        "solution": {"path": str(solution),
                     "bytes": solution.stat().st_size if solution.exists() else 0,
                     "sha256": file_sha256(solution) if solution.exists() else None},
        "replay": replay,
    })
    logical = {key: manifest[key] for key in
               ("status", "scope", "source_sha256", "rhs_sha256", "prime")}
    logical.update({"forward_sha256": manifest["forward_matrix"]["sha256"],
                    "transpose_sha256": manifest["transpose_matrix"]["sha256"],
                    "solver_sha256": manifest["solver"]["sha256"],
                    "solution_sha256": manifest["solution"]["sha256"],
                    "audit_sha256": replay.get("audit_sha256") if replay else None})
    manifest["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    atomic_json(manifest_path, manifest)
    print(f"LinBox run: {status} ({manifest['logical_sha256']})")
    if status != "completed_verified_modular_solution":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

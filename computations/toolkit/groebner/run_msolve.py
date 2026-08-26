#!/usr/bin/env python3
"""Deterministic, guarded msolve runner for modular proof discovery.

This runner never upgrades a modular result to a theorem.  It records exact
inputs, source files, commands, resources, and parsed basis metadata.  Native
F4 saturation and block elimination are staged because msolve 0.10.1 aborts
when ``-S`` and ``-e`` are combined.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

from msolve_io import (file_sha256, read_msolve_basis, read_msolve_input,
                       write_input_from_full_basis)


TOOLKIT_VERSION = "1"
RECOMMENDED_SATURATION_PRIME = 1073741827


def atomic_json(path: Path, value: dict) -> None:
    encoded = json.dumps(value, indent=2, sort_keys=True) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(encoded)
    temporary.replace(path)


def command_version(executable: str) -> str:
    completed = subprocess.run([executable, "-V"], text=True,
                               capture_output=True, timeout=10, check=False)
    return (completed.stdout + completed.stderr).strip()


def process_rss_kb(pid: int) -> int | None:
    # Sandboxed executors may be allowed to launch msolve while forbidding a
    # nested ps(1).  Resource telemetry must never turn an otherwise valid
    # algebra run into a process failure.
    try:
        completed = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)],
                                   text=True, capture_output=True, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    value = completed.stdout.strip()
    return int(value) if value.isdigit() else None


def run_stage(*, name: str, command: list[str], output: Path,
              log_prefix: Path, timeout: float | None) -> dict:
    stdout_path = Path(str(log_prefix) + ".stdout.log")
    stderr_path = Path(str(log_prefix) + ".stderr.log")
    started = time.monotonic()
    peak_rss_kb = 0
    timed_out = False
    with stdout_path.open("w") as stdout, stderr_path.open("w") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                   text=True)
        next_update = started + 60
        while process.poll() is None:
            rss = process_rss_kb(process.pid)
            if rss is not None:
                peak_rss_kb = max(peak_rss_kb, rss)
            now = time.monotonic()
            if timeout is not None and now - started >= timeout:
                timed_out = True
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                break
            if now >= next_update:
                print(f"[{name}] elapsed={now-started:.1f}s "
                      f"rss={peak_rss_kb/1024/1024:.2f}GiB",
                      flush=True)
                next_update += 60
            time.sleep(0.25)
        returncode = process.returncode
    elapsed = time.monotonic() - started
    output_exists = output.exists()
    output_size = output.stat().st_size if output_exists else 0
    parsed = None
    parse_error = None
    if returncode == 0 and output_size > 0:
        try:
            parsed = read_msolve_basis(output).manifest()
        except Exception as error:  # manifest the failure, never hide it
            parse_error = f"{type(error).__name__}: {error}"
    status = ("timeout" if timed_out else
              "process_error" if returncode != 0 else
              "invalid_zero_byte_output" if output_size == 0 else
              "invalid_basis_output" if parse_error else "completed")
    return {
        "name": name,
        "status": status,
        "command": command,
        "elapsed_seconds": elapsed,
        "peak_rss_kb": peak_rss_kb,
        "returncode": returncode,
        "stdout": {
            "path": str(stdout_path),
            "sha256": file_sha256(stdout_path),
            "bytes": stdout_path.stat().st_size,
        },
        "stderr": {
            "path": str(stderr_path),
            "sha256": file_sha256(stderr_path),
            "bytes": stderr_path.stat().st_size,
        },
        "output": {
            "path": str(output),
            "exists": output_exists,
            "bytes": output_size,
            "sha256": file_sha256(output) if output_size else None,
        },
        "basis": parsed,
        "parse_error": parse_error,
    }


def load_labels(path: Path | None, count: int) -> tuple[str, ...] | None:
    if path is None:
        return None
    value = json.loads(path.read_text())
    labels = value["labels"] if isinstance(value, dict) else value
    if not isinstance(labels, list) or any(not isinstance(x, str)
                                           for x in labels):
        raise ValueError("labels must be a JSON string list")
    if len(labels) != count:
        raise ValueError("label count does not match input polynomial count")
    return tuple(labels)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--mode", choices=("basis", "saturate", "eliminate",
                                            "saturate-eliminate"), required=True)
    parser.add_argument("--eliminate", type=int)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--timeout", type=float)
    parser.add_argument("--linear-algebra", choices=(1, 2, 42, 44),
                        type=int, default=2)
    parser.add_argument(
        "--full-basis", action="store_true",
        help="request -g 2 for standalone basis/saturate modes")
    parser.add_argument("--msolve", default="msolve")
    parser.add_argument("--labels", type=Path)
    parser.add_argument("--source", action="append", type=Path, default=[])
    parser.add_argument("--scope", required=True)
    parser.add_argument("--saturator-label")
    args = parser.parse_args()

    if args.threads <= 0:
        raise SystemExit("--threads must be positive")
    needs_elimination = args.mode in {"eliminate", "saturate-eliminate"}
    if needs_elimination and args.eliminate is None:
        raise SystemExit("elimination mode requires --eliminate")
    if not needs_elimination and args.eliminate is not None:
        raise SystemExit("--eliminate is only valid in elimination modes")

    source_input = read_msolve_input(args.input, strict=True)
    labels = load_labels(args.labels, len(source_input.polynomials))
    saturating = args.mode in {"saturate", "saturate-eliminate"}
    warnings: list[str] = []
    if saturating and source_input.characteristic < 65537:
        raise SystemExit(
            "msolve 0.10.1 F4SAT rejects small primes (including 1009); "
            f"export exact rows at a large prime such as "
            f"{RECOMMENDED_SATURATION_PRIME}")
    if saturating:
        saturator = source_input.polynomials[-1]
        saturator_record = {
            "index": len(source_input.polynomials) - 1,
            "label": args.saturator_label or
                     (labels[-1] if labels else "last_input_row"),
            "sha256": source_input.polynomial_sha256[-1],
            "passed_as_final_S_row": True,
        }
    else:
        saturator_record = None

    prefix = args.output_prefix
    prefix.parent.mkdir(parents=True, exist_ok=True)
    manifest_path = Path(str(prefix) + ".manifest.json")
    manifest = {
        "toolkit_version": TOOLKIT_VERSION,
        "proof_status": "modular_discovery_only",
        "scope": args.scope,
        "created_unix": time.time(),
        "host": platform.platform(),
        "python": sys.version,
        "cwd": os.getcwd(),
        "engine": {"path": args.msolve,
                   "version": command_version(args.msolve)},
        "mode": args.mode,
        "threads": args.threads,
        "linear_algebra": args.linear_algebra,
        "full_basis_requested": args.full_basis,
        "timeout_seconds": args.timeout,
        "input": source_input.manifest(labels),
        "saturator": saturator_record,
        "sources": [
            {"path": str(path), "sha256": file_sha256(path)}
            for path in args.source
        ],
        "warnings": warnings,
        "stages": [],
    }
    atomic_json(manifest_path, manifest)

    def command(input_path: Path, output_path: Path, *, saturation: bool,
                eliminate: int | None, full_basis: bool) -> list[str]:
        value = [args.msolve, "-f", str(input_path), "-o", str(output_path),
                 "-t", str(args.threads), "-g", "2" if full_basis else "1",
                 "-v", "1", "-l", str(args.linear_algebra)]
        if saturation:
            value.append("-S")
        if eliminate is not None:
            value.extend(["-e", str(eliminate)])
        return value

    if args.mode == "basis":
        suffix = ".full.gb.out" if args.full_basis else ".gb.out"
        plans = [("basis", args.input, Path(str(prefix) + suffix),
                  False, None, args.full_basis)]
    elif args.mode == "saturate":
        suffix = ".sat.full.gb.out" if args.full_basis else ".sat.gb.out"
        plans = [("saturate", args.input, Path(str(prefix) + suffix),
                  True, None, args.full_basis)]
    elif args.mode == "eliminate":
        plans = [("eliminate", args.input,
                  Path(str(prefix) + ".elim.gb.out"), False,
                  args.eliminate, True)]
    else:
        plans = [("saturate", args.input,
                  Path(str(prefix) + ".sat.full.gb.out"), True, None, True)]

    for name, input_path, output_path, saturation, eliminate, full in plans:
        stage = run_stage(
            name=name,
            command=command(input_path, output_path,
                            saturation=saturation,
                            eliminate=eliminate, full_basis=full),
            output=output_path,
            log_prefix=Path(str(prefix) + f".{name}"),
            timeout=args.timeout,
        )
        manifest["stages"].append(stage)
        atomic_json(manifest_path, manifest)
        if stage["status"] != "completed":
            raise SystemExit(f"{name} failed: {stage['status']}")

    if args.mode == "saturate-eliminate":
        saturated_path = Path(str(prefix) + ".sat.full.gb.out")
        saturated_basis = read_msolve_basis(saturated_path, require_full=True)
        staged_input = Path(str(prefix) + ".sat.stage2.msolve")
        write_input_from_full_basis(saturated_basis, staged_input)
        staged = read_msolve_input(staged_input, strict=True)
        manifest["stage2_input"] = staged.manifest()
        stage = run_stage(
            name="eliminate",
            command=command(staged_input,
                            Path(str(prefix) + ".elim.full.gb.out"),
                            saturation=False, eliminate=args.eliminate,
                            full_basis=True),
            output=Path(str(prefix) + ".elim.full.gb.out"),
            log_prefix=Path(str(prefix) + ".eliminate"),
            timeout=args.timeout,
        )
        manifest["stages"].append(stage)
        atomic_json(manifest_path, manifest)
        if stage["status"] != "completed":
            raise SystemExit(f"eliminate failed: {stage['status']}")

    logical = {
        "toolkit_version": manifest["toolkit_version"],
        "proof_status": manifest["proof_status"],
        "scope": manifest["scope"],
        "engine_version": manifest["engine"]["version"],
        "mode": manifest["mode"],
        "linear_algebra": manifest["linear_algebra"],
        "full_basis_requested": manifest["full_basis_requested"],
        "input_logical_sha256": manifest["input"]["logical_sha256"],
        "input_row_sha256": [row["sha256"]
                              for row in manifest["input"]["polynomials"]],
        "saturator": manifest["saturator"],
        "source_sha256": [source["sha256"]
                           for source in manifest["sources"]],
        "stages": [{
            "name": stage["name"],
            "status": stage["status"],
            "basis_kind": (stage["basis"] or {}).get("kind"),
            "basis_unit": (stage["basis"] or {}).get("unit"),
            "basis_polynomial_sha256":
                (stage["basis"] or {}).get("polynomial_sha256"),
            "basis_leading_monomials":
                (stage["basis"] or {}).get("leading_monomials"),
        } for stage in manifest["stages"]],
    }
    logical_encoded = json.dumps(logical, sort_keys=True,
                                 separators=(",", ":")).encode("utf-8")
    manifest["logical_sha256"] = sha256(logical_encoded).hexdigest()
    manifest["status"] = "completed_modular_discovery"
    atomic_json(manifest_path, manifest)
    print(f"manifest: {manifest_path}")
    print(f"logical sha256: {manifest['logical_sha256']}")


if __name__ == "__main__":
    main()

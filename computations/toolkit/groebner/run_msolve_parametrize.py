#!/usr/bin/env python3
"""Guarded msolve zero-dimensional parametrization runner.

This is a discovery interface: a modular rational parametrization must still
be lifted/replayed against the literal characteristic-zero source equations.
"""

from __future__ import annotations

import argparse
import ast
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import re
import signal
import subprocess
import sys
import time

from msolve_io import (file_sha256, read_msolve_basis, read_msolve_input,
                       write_input_from_full_basis)
from run_msolve import atomic_json, command_version, process_rss_kb


TOOLKIT_VERSION = "1"


def parse_parametrization(path: Path, characteristic: int,
                          variable_count: int) -> dict:
    text = path.read_text().strip()
    if not text.endswith(":"):
        raise ValueError("msolve solution output must end with ':'")
    body = text[:-1].strip()
    if characteristic == 0:
        if body == "[-1]":
            return {"kind": "empty", "degree": 0,
                    "variable_count": variable_count}
        if body.startswith("[1,"):
            return {"kind": "positive_dimensional", "degree": None,
                    "variable_count": variable_count}
        depth = 0
        quote = None
        escaped = False
        for character in body:
            if quote is not None:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == quote:
                    quote = None
            elif character in "'\"":
                quote = character
            elif character == "[":
                depth += 1
            elif character == "]":
                depth -= 1
                if depth < 0:
                    raise ValueError("unbalanced characteristic-zero output")
        if depth != 0 or quote is not None:
            raise ValueError("unbalanced characteristic-zero output")
        header = re.match(r"^\[0,\s*\[0,\s*(\d+),\s*(\d+),", body)
        if header is None:
            raise ValueError("unrecognized characteristic-zero RUR envelope")
        parsed_variables, degree = map(int, header.groups())
        if parsed_variables != variable_count:
            raise ValueError("solution variable count disagrees with input")
        return {"kind": "characteristic_zero_parametrization",
                "degree": degree, "variable_count": variable_count,
                "payload_sha256": sha256(body.encode()).hexdigest(),
                "includes_real_root_isolation": True}
    try:
        value = ast.literal_eval(body)
    except (SyntaxError, ValueError, MemoryError, RecursionError) as error:
        raise ValueError(f"invalid msolve solution syntax: {error}") from error
    if value == [-1]:
        return {"kind": "empty", "degree": 0, "variable_count": variable_count}
    if (isinstance(value, list) and len(value) == 4 and value[0] == 1 and
            value[1] == variable_count and value[2] == -1 and value[3] == []):
        return {"kind": "positive_dimensional", "degree": None,
                "variable_count": variable_count}
    if not (isinstance(value, list) and len(value) == 2 and value[0] == 0 and
            isinstance(value[1], list) and len(value[1]) >= 4):
        raise ValueError("unrecognized msolve parametrization envelope")
    payload = value[1]
    if payload[0] != characteristic:
        raise ValueError("solution characteristic disagrees with input")
    if payload[1] != variable_count:
        raise ValueError("solution variable count disagrees with input")
    degree = payload[2]
    variables = payload[3]
    if not isinstance(degree, int) or degree < 0:
        raise ValueError("invalid zero-dimensional degree")
    if (not isinstance(variables, list) or len(variables) != variable_count or
            any(not isinstance(variable, str) for variable in variables)):
        raise ValueError("invalid parametrization variable list")
    return {"kind": "zero_dimensional_parametrization", "degree": degree,
            "variable_count": variable_count, "variables": variables,
            "payload_sha256": sha256(json.dumps(
                value, sort_keys=False, separators=(",", ":")).encode()).hexdigest()}


def terminate_group(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=10)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--input-kind", choices=("source", "full-basis"),
                        default="source")
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--timeout", type=float)
    parser.add_argument("--linear-algebra", choices=(1, 2, 42, 44),
                        type=int, default=2)
    parser.add_argument("--genericity", choices=(0, 1, 2), type=int, default=2)
    parser.add_argument("--normal-forms", choices=(0, 1, 2, 3, 4),
                        type=int, default=2)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--msolve", default="msolve")
    parser.add_argument("--source", action="append", type=Path, default=[])
    parser.add_argument("--scope", required=True)
    args = parser.parse_args()
    if args.threads <= 0 or args.random_seed < 0:
        raise SystemExit("threads must be positive and random seed nonnegative")

    prefix = args.output_prefix
    prefix.parent.mkdir(parents=True, exist_ok=True)
    input_record: dict
    if args.input_kind == "full-basis":
        basis = read_msolve_basis(args.input, require_full=True)
        staged_input = Path(str(prefix) + ".parametrize.input.msolve")
        write_input_from_full_basis(basis, staged_input)
        parsed_input = read_msolve_input(staged_input, strict=True)
        input_record = {"kind": "strict_full_basis_seed",
                        "path": str(args.input),
                        "sha256": file_sha256(args.input),
                        "basis": basis.manifest(),
                        "staged_path": str(staged_input),
                        "staged_sha256": file_sha256(staged_input)}
        actual_input = staged_input
    else:
        parsed_input = read_msolve_input(
            args.input, strict=True, allow_characteristic_zero=True)
        input_record = {"kind": "literal_source_input",
                        "path": str(args.input),
                        "sha256": file_sha256(args.input),
                        "parsed": parsed_input.manifest()}
        actual_input = args.input

    output = Path(str(prefix) + ".param.out")
    stdout_path = Path(str(prefix) + ".stdout.log")
    stderr_path = Path(str(prefix) + ".stderr.log")
    manifest_path = Path(str(prefix) + ".manifest.json")
    command = [args.msolve, "-f", str(actual_input), "-o", str(output),
               "-t", str(args.threads), "-v", "1",
               "-l", str(args.linear_algebra),
               "-c", str(args.genericity), "-d", str(args.normal_forms),
               "--random-seed", str(args.random_seed)]
    if parsed_input.characteristic == 0:
        if args.input_kind != "source":
            raise SystemExit("characteristic-zero full-basis seeding is not supported")
        command.extend(["-P", "1"])
    success_status = ("completed_characteristic_zero_parametrization"
                      if parsed_input.characteristic == 0 else
                      "completed_modular_parametrization")
    manifest = {
        "toolkit_version": TOOLKIT_VERSION,
        "proof_status": ("exact_characteristic_zero_parametrization_requires_"
                         "literal_source_replay"
                         if parsed_input.characteristic == 0 else
                         "modular_parametrization_discovery_only"),
        "scope": args.scope, "created_unix": time.time(),
        "host": platform.platform(), "python": sys.version, "cwd": os.getcwd(),
        "engine": {"path": args.msolve, "version": command_version(args.msolve)},
        "input": input_record,
        "input_logical_sha256": parsed_input.manifest()["logical_sha256"],
        "sources": [{"path": str(path), "sha256": file_sha256(path)}
                    for path in args.source],
        "threads": args.threads, "timeout_seconds": args.timeout,
        "linear_algebra": args.linear_algebra,
        "genericity": args.genericity, "normal_forms": args.normal_forms,
        "random_seed": args.random_seed,
        "characteristic_zero_explicit_opt_in": parsed_input.characteristic == 0,
        "command": command, "status": "running",
    }
    atomic_json(manifest_path, manifest)

    process: subprocess.Popen[str] | None = None
    started = time.monotonic()
    peak_rss_kb = 0
    status = "running"
    try:
        with stdout_path.open("w") as stdout, stderr_path.open("w") as stderr:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                       text=True, start_new_session=True)
            next_update = started + 60
            while process.poll() is None:
                rss = process_rss_kb(process.pid)
                if rss is not None:
                    peak_rss_kb = max(peak_rss_kb, rss)
                now = time.monotonic()
                if args.timeout is not None and now - started >= args.timeout:
                    status = "timeout"
                    terminate_group(process)
                    break
                if now >= next_update:
                    print(f"[parametrize] elapsed={now-started:.1f}s "
                          f"rss={peak_rss_kb/1024/1024:.2f}GiB", flush=True)
                    next_update += 60
                time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        status = "interrupted"
        if process is not None:
            terminate_group(process)

    elapsed = time.monotonic() - started
    returncode = process.returncode if process is not None else None
    solution = None
    parse_error = None
    if status == "running":
        if returncode != 0:
            status = "process_error"
        elif not output.is_file() or not output.stat().st_size:
            status = "invalid_zero_byte_output"
        else:
            try:
                solution = parse_parametrization(
                    output, parsed_input.characteristic,
                    len(parsed_input.variables))
                status = success_status
            except Exception as error:
                parse_error = f"{type(error).__name__}: {error}"
                status = "invalid_parametrization_output"

    manifest.update({
        "status": status, "elapsed_seconds": elapsed,
        "peak_rss_kb": peak_rss_kb, "returncode": returncode,
        "stdout": {"path": str(stdout_path),
                   "sha256": file_sha256(stdout_path) if stdout_path.exists() else None},
        "stderr": {"path": str(stderr_path),
                   "sha256": file_sha256(stderr_path) if stderr_path.exists() else None},
        "output": {"path": str(output),
                   "bytes": output.stat().st_size if output.exists() else 0,
                   "sha256": file_sha256(output) if output.exists() else None},
        "solution": solution, "parse_error": parse_error,
    })
    logical = {
        "status": status, "scope": args.scope,
        "engine_version": manifest["engine"]["version"],
        "input_logical_sha256": manifest["input_logical_sha256"],
        "source_sha256": [source["sha256"] for source in manifest["sources"]],
        "linear_algebra": args.linear_algebra, "genericity": args.genericity,
        "normal_forms": args.normal_forms, "random_seed": args.random_seed,
        "output_sha256": manifest["output"]["sha256"], "solution": solution,
    }
    manifest["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    atomic_json(manifest_path, manifest)
    print(f"msolve parametrization: {status} ({manifest['logical_sha256']})")
    if status != success_status:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

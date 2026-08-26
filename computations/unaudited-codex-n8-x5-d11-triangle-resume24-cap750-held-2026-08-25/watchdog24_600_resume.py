#!/usr/bin/env python3
"""Fail-closed 24-GiB/600-second watchdog for one cap-750k D11 triangle resume."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def argument_value(command, name):
    positions = [index for index, value in enumerate(command) if value == name]
    if len(positions) != 1 or positions[0] + 1 >= len(command):
        raise ValueError(f"command must contain exactly one {name}")
    return command[positions[0] + 1]


class ProcTaskInfo(ctypes.Structure):
    _fields_ = [
        ("virtual_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64),
        ("total_user", ctypes.c_uint64), ("total_system", ctypes.c_uint64),
        ("threads_user", ctypes.c_uint64), ("threads_system", ctypes.c_uint64),
        ("policy", ctypes.c_int32), ("faults", ctypes.c_int32),
        ("pageins", ctypes.c_int32), ("cow_faults", ctypes.c_int32),
        ("messages_sent", ctypes.c_int32), ("messages_received", ctypes.c_int32),
        ("syscalls_mach", ctypes.c_int32), ("syscalls_unix", ctypes.c_int32),
        ("csw", ctypes.c_int32), ("threadnum", ctypes.c_int32),
        ("numrunning", ctypes.c_int32), ("priority", ctypes.c_int32),
    ]


def group_rss_kib(process_group):
    library = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
    proc_pidinfo = library.proc_pidinfo
    proc_pidinfo.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64,
                             ctypes.c_void_p, ctypes.c_int]
    proc_pidinfo.restype = ctypes.c_int
    list_pids = library.proc_listpids
    list_pids.argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_int]
    list_pids.restype = ctypes.c_int
    needed = list_pids(1, 0, None, 0)
    if needed <= 0:
        raise OSError("proc_listpids size failed")
    identifiers = (ctypes.c_int * (needed // ctypes.sizeof(ctypes.c_int) + 32))()
    returned = list_pids(1, 0, identifiers, ctypes.sizeof(identifiers))
    if returned <= 0:
        raise OSError("proc_listpids failed")
    total = 0
    members = 0
    for pid in identifiers[:returned // ctypes.sizeof(ctypes.c_int)]:
        if pid <= 0:
            continue
        try:
            if os.getpgid(pid) != process_group:
                continue
        except (ProcessLookupError, PermissionError):
            continue
        information = ProcTaskInfo()
        size = ctypes.sizeof(information)
        if proc_pidinfo(pid, 4, 0, ctypes.byref(information), size) == size:
            total += information.resident_size // 1024
            members += 1
    if members == 0:
        raise OSError("no observable process-group members")
    return total, members


def terminate_group(process):
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        return
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rss-gib", type=int, required=True)
    parser.add_argument("--wall-seconds", type=int, required=True)
    parser.add_argument("--poll-seconds", type=float, default=0.25)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--expected-source-sha256", required=True)
    parser.add_argument("--expected-binary-sha256", required=True)
    parser.add_argument("--telemetry", type=Path, required=True)
    parser.add_argument("--stdout", type=Path, required=True)
    parser.add_argument("--stderr", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command or args.rss_gib != 24 or not 1 <= args.wall_seconds <= 600:
        raise SystemExit("watchdog accepts only the sealed 24-GiB, <=600-second cap-750k D11 resume")
    if not 0 < args.poll_seconds <= 1:
        raise SystemExit("bad watchdog polling interval")
    binary = Path(command[0])
    if sha256(args.source) != args.expected_source_sha256:
        raise SystemExit("frozen source SHA-256 mismatch")
    if sha256(binary) != args.expected_binary_sha256:
        raise SystemExit("frozen binary SHA-256 mismatch")
    if int(argument_value(command, "--wall-seconds")) > args.wall_seconds:
        raise SystemExit("native wall cap exceeds wrapper wall cap")
    result_path = Path(argument_value(command, "--output"))
    selected_path = Path(argument_value(command, "--selected"))
    dual_path = Path(argument_value(command, "--dual"))
    for path in (result_path, selected_path, dual_path, args.telemetry, args.stdout, args.stderr):
        if path.exists():
            raise SystemExit(f"refuse pre-existing output {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
    stdout_tmp = args.stdout.with_suffix(args.stdout.suffix + ".tmp")
    stderr_tmp = args.stderr.with_suffix(args.stderr.suffix + ".tmp")
    started = time.monotonic()
    samples = []
    breach = None
    with stdout_tmp.open("wb") as stdout, stderr_tmp.open("wb") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                   start_new_session=True)
        while process.poll() is None:
            elapsed = time.monotonic() - started
            try:
                rss_kib, members = group_rss_kib(process.pid)
                samples.append({"elapsed_seconds": round(elapsed, 6),
                                "rss_kib": rss_kib,
                                "process_group_members": members})
                if rss_kib > args.rss_gib * 1024 * 1024:
                    breach = "RSS_CAP"
            except OSError:
                pass
            if elapsed >= args.wall_seconds:
                breach = "WALL_CAP"
            if breach is not None:
                terminate_group(process)
                break
            time.sleep(args.poll_seconds)
        returncode = process.wait()
    os.replace(stdout_tmp, args.stdout)
    os.replace(stderr_tmp, args.stderr)
    result_exists = result_path.exists()
    engine_status = None
    if result_exists:
        try:
            engine_status = json.loads(result_path.read_text())["status"]
        except (OSError, KeyError, TypeError, json.JSONDecodeError):
            engine_status = None
    status_class = {
        "COMPLETE_MODULAR_DUAL_DIAGNOSTIC": "TERMINAL_MODULAR_DUAL",
        "MODULAR_MEMBER_REQUIRES_EXACT_RATIONAL_REPLAY": "TERMINAL_EXACT_REPLAY_REQUIRED",
        "INCOMPLETE_WALL_CAP": "RESTART_CHECKPOINT_ONLY",
    }.get(engine_status)
    restart_pair_available = selected_path.exists() and dual_path.exists()
    peak = max((sample["rss_kib"] for sample in samples), default=0)
    status = (
        "PASS_TERMINAL" if breach is None and returncode == 0 and result_exists
        and status_class is not None and status_class.startswith("TERMINAL_")
        else "PASS_RESTART_CHECKPOINT" if breach is None and returncode == 0
        and result_exists and status_class == "RESTART_CHECKPOINT_ONLY" and restart_pair_available
        else "FAIL_CLOSED_CHECKPOINT_AVAILABLE" if breach is not None and restart_pair_available
        else "FAIL_CLOSED"
    )
    telemetry = {
        "schema": "KRENN_X5_D11_TRIANGLE_CAP750_RESUME_WATCHDOG_24G_600_V1",
        "status": status,
        "breach": breach,
        "returncode": returncode,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "rss_limit_kib": args.rss_gib * 1024 * 1024,
        "wall_limit_seconds": args.wall_seconds,
        "poll_seconds": args.poll_seconds,
        "peak_rss_kib": peak,
        "samples": samples,
        "source": str(args.source),
        "source_sha256": sha256(args.source),
        "binary": str(binary),
        "binary_sha256": sha256(binary),
        "command": command,
        "result_exists": result_exists,
        "engine_status": engine_status,
        "engine_status_class": status_class,
        "result_sha256": sha256(result_path) if result_exists else None,
        "restart_pair_available": restart_pair_available,
        "restart_selected_sha256": sha256(selected_path) if selected_path.exists() else None,
        "restart_selected_bytes": selected_path.stat().st_size if selected_path.exists() else None,
        "restart_dual_sha256": sha256(dual_path) if dual_path.exists() else None,
        "restart_dual_bytes": dual_path.stat().st_size if dual_path.exists() else None,
        "stdout_sha256": sha256(args.stdout),
        "stderr_sha256": sha256(args.stderr),
    }
    atomic_json(args.telemetry, telemetry)
    return 0 if status.startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Small fail-closed process-group watchdog for the D11 representation microgate."""

import argparse
import ctypes
import json
import os
from pathlib import Path
import signal
import subprocess
import time


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


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


def group_rss_kib(group: int) -> tuple[int, int]:
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
            if os.getpgid(pid) != group:
                continue
        except (ProcessLookupError, PermissionError):
            continue
        information = ProcTaskInfo()
        size = ctypes.sizeof(information)
        if proc_pidinfo(pid, 4, 0, ctypes.byref(information), size) == size:
            total += information.resident_size // 1024
            members += 1
    if members == 0:
        raise OSError("no observable group member")
    return total, members


def terminate(process: subprocess.Popen) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--telemetry", type=Path, required=True)
    parser.add_argument("--stdout", type=Path, required=True)
    parser.add_argument("--stderr", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        raise SystemExit("missing command")
    for path in (args.telemetry, args.stdout, args.stderr):
        if path.exists():
            raise SystemExit(f"refuse pre-existing output {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
    stdout_tmp = args.stdout.with_suffix(args.stdout.suffix + ".tmp")
    stderr_tmp = args.stderr.with_suffix(args.stderr.suffix + ".tmp")
    started = time.monotonic()
    samples = []
    breach = None
    with stdout_tmp.open("wb") as stdout, stderr_tmp.open("wb") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr, start_new_session=True)
        while process.poll() is None:
            elapsed = time.monotonic() - started
            try:
                rss, members = group_rss_kib(process.pid)
                samples.append({"elapsed_seconds": round(elapsed, 6), "rss_kib": rss,
                                "members": members})
                if rss > 4 * 1024 * 1024:
                    breach = "RSS_CAP"
            except (OSError, subprocess.SubprocessError, ValueError):
                pass
            if elapsed >= 120:
                breach = "WALL_CAP"
            if breach:
                terminate(process)
                break
            time.sleep(0.01)
        returncode = process.wait()
    os.replace(stdout_tmp, args.stdout)
    os.replace(stderr_tmp, args.stderr)
    status = "PASS" if breach is None and returncode == 0 else "FAIL_CLOSED"
    atomic_json(args.telemetry, {
        "schema": "KRENN_X5_D11_COMPACT_MICROGATE_WATCHDOG_V1",
        "status": status,
        "breach": breach,
        "returncode": returncode,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "peak_rss_kib": max((sample["rss_kib"] for sample in samples), default=0),
        "rss_cap_kib": 4 * 1024 * 1024,
        "wall_cap_seconds": 120,
        "samples": samples,
        "command": command,
    })
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

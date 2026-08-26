#!/usr/bin/env python3
"""Fail-closed macOS RSS/wall watchdog for one native atomic D12 round."""

import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def argument_value(command: list[str], name: str) -> str:
    positions = [index for index, value in enumerate(command) if value == name]
    if len(positions) != 1 or positions[0] + 1 >= len(command):
        raise ValueError(f"command must contain exactly one {name}")
    return command[positions[0] + 1]


def terminate_group(process: subprocess.Popen[bytes]) -> None:
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


def libproc_group_rss_kib(process_group: int) -> tuple[int, int]:
    library = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
    function = library.proc_pidinfo
    function.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64,
                         ctypes.c_void_p, ctypes.c_int]
    function.restype = ctypes.c_int
    list_pids = library.proc_listpids
    list_pids.argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_int]
    list_pids.restype = ctypes.c_int
    needed = list_pids(1, 0, None, 0)  # PROC_ALL_PIDS
    if needed <= 0:
        raise OSError(ctypes.get_errno(), "proc_listpids size failed")
    identifiers = (ctypes.c_int * (needed // ctypes.sizeof(ctypes.c_int) + 32))()
    returned = list_pids(1, 0, identifiers, ctypes.sizeof(identifiers))
    if returned <= 0:
        raise OSError(ctypes.get_errno(), "proc_listpids failed")
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
        if function(pid, 4, 0, ctypes.byref(information), size) == size:
            total += information.resident_size // 1024
            members += 1
    if members == 0:
        raise OSError("no observable process-group members")
    return total, members


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rss-gib", type=int, required=True)
    parser.add_argument("--wall-seconds", type=int, required=True)
    parser.add_argument("--poll-seconds", type=float, default=0.25)
    parser.add_argument("--test-rss-limit-kib", type=int)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--expected-source-sha256", required=True)
    parser.add_argument("--expected-binary-sha256", required=True)
    parser.add_argument("--telemetry", type=Path, required=True)
    parser.add_argument("--stdout", type=Path, required=True)
    parser.add_argument("--stderr", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command or args.rss_gib != 36 or args.wall_seconds > 120:
        raise SystemExit("watchdog accepts only the sealed 36-GiB, <=120-second gate")
    if args.poll_seconds <= 0 or args.poll_seconds > 1:
        raise SystemExit("watchdog poll interval must be in (0,1]")
    if args.test_rss_limit_kib is not None:
        if (os.environ.get("KRENN_WATCHDOG_SELFTEST") != "1"
                or not 1 <= args.test_rss_limit_kib < args.rss_gib * 1024 * 1024):
            raise SystemExit("test RSS limit is selftest-only and must tighten the cap")
    binary = Path(command[0])
    source_sha = sha256(args.source)
    binary_sha = sha256(binary)
    if source_sha != args.expected_source_sha256 or binary_sha != args.expected_binary_sha256:
        raise SystemExit("frozen source/binary SHA-256 mismatch")
    if argument_value(command, "--rss-gib") != "36":
        raise SystemExit("native command must retain --rss-gib 36")
    if int(argument_value(command, "--wall-seconds")) > args.wall_seconds:
        raise SystemExit("native wall cap exceeds watchdog wall cap")
    result_path = Path(argument_value(command, "--output"))
    if result_path.exists():
        raise SystemExit("refusing to overwrite a pre-existing result")
    for path in (args.telemetry, args.stdout, args.stderr):
        if path.exists():
            raise SystemExit(f"refusing to overwrite {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
    stdout_tmp = args.stdout.with_suffix(args.stdout.suffix + ".tmp")
    stderr_tmp = args.stderr.with_suffix(args.stderr.suffix + ".tmp")
    try:
        preflight = subprocess.run(
            ["/bin/ps", "-o", "rss=", "-p", str(os.getpid())],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False, text=True,
        )
        ps_available = preflight.returncode == 0 and bool(preflight.stdout.strip())
    except OSError:
        ps_available = False
    rss_limit_bytes = args.rss_gib << 30
    rss_limit_kib = (args.test_rss_limit_kib if args.test_rss_limit_kib is not None
                     else args.rss_gib * 1024 * 1024)

    started = time.monotonic()
    samples: list[dict[str, int | float]] = []
    breach = None
    with stdout_tmp.open("wb") as stdout, stderr_tmp.open("wb") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                   start_new_session=True)
        while process.poll() is None:
            elapsed = time.monotonic() - started
            if ps_available:
                try:
                    observation = subprocess.run(
                        ["/bin/ps", "-o", "rss=", "-p", str(process.pid)],
                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                        check=False, text=True,
                    )
                    rss_kib = int(observation.stdout.strip())
                    member_count = 1
                except (OSError, ValueError):
                    breach = "RSS_OBSERVER_FAILURE"
                    terminate_group(process)
                    break
            else:
                try:
                    rss_kib, member_count = libproc_group_rss_kib(process.pid)
                except OSError:
                    # The child can exit between poll() and proc_listpids().
                    # Give waitpid a short grace to observe that terminal
                    # status; a confirmed exit is not an observer failure or
                    # a signal target.
                    try:
                        process.wait(timeout=max(0.05, args.poll_seconds * 2))
                        break
                    except subprocess.TimeoutExpired:
                        pass
                    breach = "RSS_OBSERVER_FAILURE"
                    terminate_group(process)
                    break
            if rss_kib < 0:
                breach = "RSS_OBSERVER_FAILURE"
                terminate_group(process)
                break
            samples.append({"elapsed_seconds": round(elapsed, 6), "rss_kib": rss_kib,
                            "process_group_members": member_count})
            if rss_kib >= rss_limit_kib:
                breach = "RSS_CAP"
                terminate_group(process)
                break
            if elapsed >= args.wall_seconds:
                breach = "WALL_CAP"
                terminate_group(process)
                break
            time.sleep(args.poll_seconds)
        returncode = process.wait()
        stdout.flush(); os.fsync(stdout.fileno())
        stderr.flush(); os.fsync(stderr.fileno())
    os.replace(stdout_tmp, args.stdout)
    os.replace(stderr_tmp, args.stderr)
    temporary_paths = [
        Path(argument_value(command, flag)).with_suffix(
            Path(argument_value(command, flag)).suffix + ".tmp")
        for flag in ("--output", "--checkpoint", "--vector-cache")
    ]
    quarantined = []
    if breach is not None:
        for path in [result_path, *temporary_paths]:
            if path.exists():
                rejected = path.with_name(path.name + ".aborted")
                os.replace(path, rejected)
                quarantined.append(str(rejected))
    atomic_clean = (breach is None and result_path.is_file()
                    and not any(path.exists() for path in temporary_paths))
    status = "PASS" if breach is None and returncode == 0 and atomic_clean else "FAIL"
    telemetry = {
        "schema": "KRENN_AFFINE251_D12_MACOS_RSS_WATCHDOG_V2",
        "status": status,
        "scope": "One child process; ps resident-set polling; atomic native outputs.",
        "command": command,
        "source": str(args.source),
        "source_sha256": source_sha,
        "binary": str(binary),
        "binary_sha256": binary_sha,
        "watchdog_sha256": sha256(Path(__file__)),
        "rss_limit_kib": rss_limit_kib,
        "contract_rss_limit_kib": args.rss_gib * 1024 * 1024,
        "wall_limit_seconds": args.wall_seconds,
        "poll_seconds": args.poll_seconds,
        "rss_observer": "ps" if ps_available else "libproc_PROC_PIDTASKINFO",
        "rlimit_as_bytes": None,
        "rlimit_as_unavailable_reason": (None if ps_available else
            "sandbox rejected preexec_fn setrlimit(RLIMIT_AS); live libproc RSS kill used"),
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "peak_rss_kib": max((sample["rss_kib"] for sample in samples), default=None),
        "sample_count": len(samples),
        "samples": samples,
        "last_successful_rss_sample": samples[-1] if samples else None,
        "breach": breach,
        "returncode": returncode,
        "atomic_outputs_clean": atomic_clean,
        "abort_final_output_absent": breach is None or not result_path.exists(),
        "quarantined_abort_paths": quarantined,
        "result_sha256": sha256(result_path) if result_path.is_file() else None,
        "stdout_sha256": sha256(args.stdout),
        "stderr_sha256": sha256(args.stderr),
    }
    atomic_json(args.telemetry, telemetry)
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())

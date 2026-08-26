#!/usr/bin/env python3
"""One-shot macOS libproc watchdog for the approved exact-Q Singular lane."""

from __future__ import annotations

import ctypes
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "rectangle_rank3_adjugate_Q.sing"
SINGULAR = Path("/usr/local/Cellar/singular/4.4.1p5_3/bin/Singular")
GTIMEOUT = Path("/usr/local/Cellar/coreutils/9.11/bin/gtimeout")
STDOUT = HERE / "stdout.log"
STDERR = HERE / "stderr.log"
TELEMETRY = HERE / "watchdog.json"
NATIVE_WALL_SECONDS = 480
WRAPPER_WALL_SECONDS = 510
RSS_LIMIT_KIB = 8 * 1024 * 1024
POLL_SECONDS = 0.25
EXPECTED = {
    SOURCE: "e2739688ea9986d59c56e17e6f0058154d9ddb7930bf9617a1d3a3a8167538f5",
    SINGULAR: "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    GTIMEOUT: "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
    HERE.parent / "EXACT_Q_HELD_PLAN.json": "56618e1848b7809db58f86103f1c9a3a33a31d3f8fd97b3a1b744eff15d52faa",
    HERE.parent / "FINAL_MANIFEST.sha256": "45fad912e746c13792dfa0b35e92ffa975266d6bb01732cbef8101a324bec6f6",
    HERE.parent.parent / "unaudited-codex-n8-x5-rectangle-rank3-adjugate-ideal-referee-2026-08-25/MANIFEST.sha256": "c2fbb2ba00a1dc854b66ea7791cfb0fdad7b3b1747ee71b01e7c9f62a65ee8e5",
    HERE.parent.parent / "unaudited-codex-n8-x5-rectangle-rank3-adjugate-independent-referee-2026-08-25/FINAL_MANIFEST.sha256": "873d47c348464c0f03dbd8011463d7bcef9df2732c4b6fecafa56e7e121b0a42",
}


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
    info = library.proc_pidinfo
    info.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64,
                     ctypes.c_void_p, ctypes.c_int]
    info.restype = ctypes.c_int
    list_pids = library.proc_listpids
    list_pids.argtypes = [ctypes.c_uint32, ctypes.c_uint32,
                          ctypes.c_void_p, ctypes.c_int]
    list_pids.restype = ctypes.c_int
    needed = list_pids(1, 0, None, 0)
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
        task = ProcTaskInfo()
        size = ctypes.sizeof(task)
        if info(pid, 4, 0, ctypes.byref(task), size) == size:
            total += task.resident_size // 1024
            members += 1
    if members == 0:
        raise OSError("no observable process-group members")
    return total, members


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


def main() -> int:
    for path, expected in EXPECTED.items():
        actual = sha256(path)
        if actual != expected:
            raise SystemExit(f"frozen SHA mismatch: {path}: {actual}")
    for path in (STDOUT, STDERR, TELEMETRY,
                 STDOUT.with_suffix(".log.tmp"), STDERR.with_suffix(".log.tmp"),
                 TELEMETRY.with_suffix(".json.tmp")):
        if path.exists():
            raise SystemExit(f"refusing to overwrite {path}")
    command = [str(GTIMEOUT), "--signal=TERM", "--kill-after=10", "480",
               str(SINGULAR), "-q", str(SOURCE)]
    stdout_tmp = STDOUT.with_suffix(".log.tmp")
    stderr_tmp = STDERR.with_suffix(".log.tmp")
    started = time.monotonic()
    samples: list[dict[str, int | float]] = []
    breach = None
    with stdout_tmp.open("wb") as stdout, stderr_tmp.open("wb") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                   start_new_session=True)
        while process.poll() is None:
            elapsed = time.monotonic() - started
            try:
                rss_kib, members = libproc_group_rss_kib(process.pid)
            except OSError:
                try:
                    process.wait(timeout=max(0.05, POLL_SECONDS * 2))
                    break
                except subprocess.TimeoutExpired:
                    breach = "RSS_OBSERVER_FAILURE"
                    terminate_group(process)
                    break
            samples.append({"elapsed_seconds": round(elapsed, 6),
                            "rss_kib": rss_kib,
                            "process_group_members": members})
            if rss_kib >= RSS_LIMIT_KIB:
                breach = "RSS_CAP"
                terminate_group(process)
                break
            if elapsed >= WRAPPER_WALL_SECONDS:
                breach = "WRAPPER_WALL_CAP"
                terminate_group(process)
                break
            time.sleep(POLL_SECONDS)
        returncode = process.wait()
        stdout.flush(); os.fsync(stdout.fileno())
        stderr.flush(); os.fsync(stderr.fileno())
    os.replace(stdout_tmp, STDOUT)
    os.replace(stderr_tmp, STDERR)
    output = STDOUT.read_text(encoding="utf-8", errors="replace")
    parsed = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if key in {"INPUT_VARIABLES", "INPUT_GENERATORS", "GROEBNER_SIZE",
                       "UNIT_REMAINDER", "STATUS"}:
                parsed[key] = value
    terminal_reason = breach
    if terminal_reason is None and returncode == 124:
        terminal_reason = "NATIVE_WALL_CAP"
    elif terminal_reason is None and returncode != 0:
        terminal_reason = "SINGULAR_NONZERO"
    status = "PASS" if terminal_reason is None else "TERMINAL_DIAGNOSTIC"
    telemetry = {
        "schema": "KRENN_X5_RECTANGLE_RANK3_ADJUGATE_EXACT_Q_WATCHDOG_V1",
        "status": status,
        "scope": "Exactly one exact-Q Singular lane; no second lane or relaunch.",
        "command": command,
        "source_sha256": sha256(SOURCE),
        "singular_sha256": sha256(SINGULAR),
        "gtimeout_sha256": sha256(GTIMEOUT),
        "exact_q_plan_sha256": sha256(HERE.parent / "EXACT_Q_HELD_PLAN.json"),
        "exact_q_referee_manifest_sha256": sha256(HERE.parent / "FINAL_MANIFEST.sha256"),
        "producer_manifest_sha256": sha256(HERE.parent.parent / "unaudited-codex-n8-x5-rectangle-rank3-adjugate-ideal-referee-2026-08-25/MANIFEST.sha256"),
        "independent_manifest_sha256": sha256(HERE.parent.parent / "unaudited-codex-n8-x5-rectangle-rank3-adjugate-independent-referee-2026-08-25/FINAL_MANIFEST.sha256"),
        "field": "Q",
        "native_wall_seconds": NATIVE_WALL_SECONDS,
        "wrapper_wall_seconds": WRAPPER_WALL_SECONDS,
        "rss_limit_kib": RSS_LIMIT_KIB,
        "rss_observer": "libproc_PROC_PIDTASKINFO_process_group",
        "poll_seconds": POLL_SECONDS,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "returncode": returncode,
        "terminal_reason": terminal_reason,
        "peak_rss_kib": max((sample["rss_kib"] for sample in samples), default=None),
        "last_successful_rss_sample": samples[-1] if samples else None,
        "sample_count": len(samples),
        "samples": samples,
        "logs_atomic": (STDOUT.is_file() and STDERR.is_file()
                        and not stdout_tmp.exists() and not stderr_tmp.exists()),
        "stdout_sha256": sha256(STDOUT),
        "stderr_sha256": sha256(STDERR),
        "parsed_stdout": parsed,
        "q_lane_launched": True,
        "second_lane_launched": False,
        "automatic_relaunch": False,
    }
    atomic_json(TELEMETRY, telemetry)
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""One-shot group15 exact-Q runner. Requires a fresh sealed clearance."""
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

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "rep1_group15_Q.sing"
PLAN = ROOT / "computations/unaudited-codex-n8-x5-rep1-group15-direct-libproc-held-plan-2026-08-25/HELD_GROUP15_PLAN.json"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep1-group15-direct-libproc-held-plan-referee-2026-08-25/FINAL_MANIFEST.sha256"
HELD_MANIFEST = HERE / "HELD_RUNNER_MANIFEST.sha256"
CLEARANCE = HERE / "FRESH_CLEARANCE.json"
SCHEMA = HERE / "FRESH_CLEARANCE.schema.json"
ATTEMPT = HERE / "attempt_group15"
SINGULAR = Path("/usr/local/Cellar/singular/4.4.1p5_3/bin/Singular")
GTIMEOUT = Path("/usr/local/Cellar/coreutils/9.11/bin/gtimeout")
SOURCE_SHA = "1611c16c73323e7a85ee730ba055f9f2092873841698e8fcc4f5799571ccab04"
SOURCE_BYTES = 1841468
NATIVE_WALL = 240
WRAPPER_WALL = 250
RSS_LIMIT_KIB = 8 * 1024 * 1024
POLL_SECONDS = 0.25
PROC_PIDTASKINFO = 4
EXPECTED = {
    PLAN: "e778f68f78c087a2d63f4491e0d67d9920302dc55cd2d39e80abc380f66c6ce4",
    REFEREE: "b1714d0a1d689ebae04017bf6ccb5120861996160cc4a37892542e3592e36761",
    SOURCE: SOURCE_SHA,
    SINGULAR: "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    GTIMEOUT: "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_bytes(path: Path, payload: bytes) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def atomic_json(path: Path, value: object) -> None:
    atomic_bytes(path, (json.dumps(value, indent=2, sort_keys=True) + "\n").encode())


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


LIBPROC = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
LISTPIDS = LIBPROC.proc_listpids
LISTPIDS.argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_int]
LISTPIDS.restype = ctypes.c_int
PIDPATH = LIBPROC.proc_pidpath
PIDPATH.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
PIDPATH.restype = ctypes.c_int
PIDINFO = LIBPROC.proc_pidinfo
PIDINFO.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_int]
PIDINFO.restype = ctypes.c_int


def all_pids() -> list[int]:
    needed = LISTPIDS(1, 0, None, 0)
    if needed <= 0:
        raise OSError(ctypes.get_errno(), "proc_listpids size failed")
    values = (ctypes.c_int * (needed // ctypes.sizeof(ctypes.c_int) + 64))()
    returned = LISTPIDS(1, 0, values, ctypes.sizeof(values))
    if returned <= 0:
        raise OSError(ctypes.get_errno(), "proc_listpids failed")
    return [pid for pid in values[:returned // ctypes.sizeof(ctypes.c_int)] if pid > 0]


def pid_path(pid: int) -> str:
    buffer = ctypes.create_string_buffer(4096)
    returned = PIDPATH(pid, buffer, len(buffer))
    return buffer.value.decode(errors="replace") if returned > 0 else ""


def fresh_process_census() -> dict:
    matches = []
    for pid in all_pids():
        if pid == os.getpid():
            continue
        path = pid_path(pid)
        base = Path(path).name.lower()
        if "singular" in base or "sparse_d12" in base:
            matches.append({"pid": pid, "path": path})
    return {"observer": "Darwin libproc proc_listpids plus proc_pidpath", "matches": matches, "pass": not matches}


def process_group_rss_kib(process_group: int) -> tuple[int, int]:
    total = members = 0
    for pid in all_pids():
        try:
            if os.getpgid(pid) != process_group:
                continue
        except (ProcessLookupError, PermissionError):
            continue
        task = ProcTaskInfo()
        size = ctypes.sizeof(task)
        if PIDINFO(pid, PROC_PIDTASKINFO, 0, ctypes.byref(task), size) == size:
            total += task.resident_size // 1024
            members += 1
    if members == 0:
        raise OSError("no observable process-group member")
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


def validate_clearance() -> dict:
    assert CLEARANCE.is_file(), "held: FRESH_CLEARANCE.json is absent"
    value = json.loads(CLEARANCE.read_text())
    required = {
        "schema", "status", "group_id", "plan_sha256", "independent_manifest_sha256",
        "held_runner_manifest_sha256", "manager_clearance", "resource_clearance",
        "no_overlap_confirmed", "launch_exactly_once", "nonce",
        "issued_unix_seconds", "expires_unix_seconds",
    }
    assert set(value) == required
    assert value["schema"] == "KRENN_X5_REP1_GROUP15_FRESH_CLEARANCE_V1"
    assert value["status"] == "EXPLICIT_MANAGER_AND_RESOURCE_CLEARANCE"
    assert value["group_id"] == 15
    assert value["plan_sha256"] == EXPECTED[PLAN]
    assert value["independent_manifest_sha256"] == EXPECTED[REFEREE]
    assert value["held_runner_manifest_sha256"] == sha(HELD_MANIFEST)
    assert value["manager_clearance"] is value["resource_clearance"] is True
    assert value["no_overlap_confirmed"] is value["launch_exactly_once"] is True
    assert isinstance(value["nonce"], str) and len(value["nonce"]) >= 16
    now = time.time()
    assert value["issued_unix_seconds"] <= now <= value["expires_unix_seconds"]
    assert value["expires_unix_seconds"] - value["issued_unix_seconds"] <= 900
    return value


def held_check() -> int:
    for path, expected in EXPECTED.items():
        assert sha(path) == expected, (path, sha(path), expected)
    assert SOURCE.stat().st_size == SOURCE_BYTES
    assert SCHEMA.is_file() and HELD_MANIFEST.is_file()
    assert not CLEARANCE.exists() and not ATTEMPT.exists()
    print(json.dumps({"status": "HELD_NOT_LAUNCHED", "source_sha256": sha(SOURCE), "clearance_absent": True, "attempt_absent": True}, sort_keys=True))
    return 0


def launch() -> int:
    for path, expected in EXPECTED.items():
        assert sha(path) == expected, (path, sha(path), expected)
    assert SOURCE.stat().st_size == SOURCE_BYTES
    clearance = validate_clearance()
    ATTEMPT.mkdir()
    census = fresh_process_census()
    atomic_json(ATTEMPT / "preflight.json", {"schema": "KRENN_X5_REP1_GROUP15_PREFLIGHT_V1", "group_id": 15, "clearance_sha256": sha(CLEARANCE), "census": census})
    if not census["pass"]:
        atomic_json(ATTEMPT / "result.json", {"schema": "KRENN_X5_REP1_GROUP15_RESULT_V1", "status": "STOPPED_COMPETING_PROCESS_ZERO_ARITHMETIC", "group_id": 15, "unit_ideal": False})
        return 2
    attempt_source = ATTEMPT / SOURCE.name
    atomic_bytes(attempt_source, SOURCE.read_bytes())
    assert sha(attempt_source) == SOURCE_SHA and attempt_source.stat().st_size == SOURCE_BYTES
    stdout_path, stderr_path = ATTEMPT / "stdout.log", ATTEMPT / "stderr.log"
    stdout_tmp, stderr_tmp = ATTEMPT / "stdout.log.tmp", ATTEMPT / "stderr.log.tmp"
    command = [str(GTIMEOUT), "--signal=TERM", "--kill-after=10", str(NATIVE_WALL), str(SINGULAR), "-q", str(attempt_source)]
    started = time.monotonic()
    samples = []
    breach = None
    with stdout_tmp.open("xb") as stdout, stderr_tmp.open("xb") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr, start_new_session=True)
        while process.poll() is None:
            elapsed = time.monotonic() - started
            try:
                rss_kib, members = process_group_rss_kib(process.pid)
            except OSError:
                try:
                    process.wait(timeout=0.5)
                    break
                except subprocess.TimeoutExpired:
                    breach = "RSS_OBSERVER_FAILURE"
                    terminate_group(process)
                    break
            samples.append({"elapsed_seconds": round(elapsed, 6), "rss_kib": rss_kib, "members": members})
            if rss_kib >= RSS_LIMIT_KIB:
                breach = "RSS_CAP"
                terminate_group(process)
                break
            if elapsed >= WRAPPER_WALL:
                breach = "WRAPPER_WALL_CAP"
                terminate_group(process)
                break
            time.sleep(POLL_SECONDS)
        returncode = process.wait()
        stdout.flush(); os.fsync(stdout.fileno())
        stderr.flush(); os.fsync(stderr.fileno())
    os.replace(stdout_tmp, stdout_path)
    os.replace(stderr_tmp, stderr_path)
    text = stdout_path.read_text(errors="replace")
    parsed = {}
    for line in text.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if key in {"INPUT_GENERATORS", "GROEBNER_SIZE", "UNIT_REMAINDER", "STATUS"}:
                parsed[key] = value
    if breach is None and returncode == 124:
        breach = "NATIVE_WALL_CAP"
    elif breach is None and returncode != 0:
        breach = "SINGULAR_NONZERO"
    unit = breach is None and returncode == 0 and parsed == {"INPUT_GENERATORS": "6577", "GROEBNER_SIZE": "1", "UNIT_REMAINDER": "0", "STATUS": "UNIT_IDEAL"}
    telemetry = {
        "schema": "KRENN_X5_REP1_GROUP15_WATCHDOG_V1", "status": "PASS" if breach is None else "TERMINAL_FAILURE",
        "group_id": 15, "command": command, "source_sha256": sha(attempt_source),
        "native_wall_seconds": NATIVE_WALL, "wrapper_wall_seconds": WRAPPER_WALL,
        "rss_limit_kib": RSS_LIMIT_KIB, "elapsed_seconds": round(time.monotonic() - started, 6),
        "returncode": returncode, "breach": breach,
        "peak_rss_kib": max((sample["rss_kib"] for sample in samples), default=None),
        "samples": samples, "stdout_sha256": sha(stdout_path), "stderr_sha256": sha(stderr_path),
        "logs_atomic": not stdout_tmp.exists() and not stderr_tmp.exists(),
        "automatic_relaunch": False, "second_lane": False,
    }
    atomic_json(ATTEMPT / "watchdog.json", telemetry)
    result = {
        "schema": "KRENN_X5_REP1_GROUP15_RESULT_V1",
        "status": "UNIT_IDEAL_EXACT_Q_GROUP15" if unit else "TERMINAL_NONUNIT_OR_FAILURE",
        "group_id": 15, "field": "Q", "unit_ideal": unit,
        "group_closed": unit, "representative_1_closed": False,
        "source_sha256": sha(attempt_source), "source_bytes": attempt_source.stat().st_size,
        "parsed_stdout": parsed, "returncode": returncode, "breach": breach,
        "watchdog_sha256": sha(ATTEMPT / "watchdog.json"),
        "preflight_sha256": sha(ATTEMPT / "preflight.json"),
        "clearance_sha256": sha(CLEARANCE), "clearance_nonce": clearance["nonce"],
        "automatic_relaunch": False, "second_lane": False, "group17_or_group25": False,
        "independent_terminal_audit_required": True,
    }
    atomic_json(ATTEMPT / "result.json", result)
    return 0 if unit else 2


if __name__ == "__main__":
    if sys.argv == [sys.argv[0], "--check-held"]:
        raise SystemExit(held_check())
    if sys.argv == [sys.argv[0], "--launch"]:
        raise SystemExit(launch())
    raise SystemExit("usage: run_group15_direct_libproc.py --check-held | --launch")

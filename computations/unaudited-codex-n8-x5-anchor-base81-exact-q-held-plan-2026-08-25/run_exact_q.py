#!/usr/bin/env python3
"""Fail-closed, one-shot exact-Q base81/6561 Singular lane."""
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
SOURCE = HERE / "base81_exact_Q.sing"
EPILOGUE = ROOT / "computations/unaudited-codex-n8-x5-anchor-no-rectangle-base81-p32003-held-pilot-2026-08-25/SOLVER_EPILOGUE.sing"
PLAN = HERE / "HELD_EXACT_Q_PLAN.json"
MANIFEST = HERE / "MANIFEST.sha256"
CLEARANCE = HERE / "FRESH_CLEARANCE.json"
ATTEMPT = HERE / "attempt_exact_q"
REFUSAL = HERE / "refusal.json"
SINGULAR = Path("/usr/local/Cellar/singular/4.4.1p5_3/bin/Singular")
GTIMEOUT = Path("/usr/local/Cellar/coreutils/9.11/bin/gtimeout")
SOURCE_SHA = "85f75e489e80a12109a82da607d6d1e21498f825f17eea8486f41078b73b39bc"
SOURCE_BYTES = 420121
PLAN_SHA = "053763f0e5534ce6e13a859d6bed1d137de3be0157e0cf42581df2a7a44907d8"
SINGULAR_SHA = "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"
GTIMEOUT_SHA = "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"
NATIVE_WALL = 480
WRAPPER_WALL = 510
RSS_LIMIT_KIB = 8 * 1024 * 1024
POLL_SECONDS = 0.25
PROC_PIDTASKINFO = 4


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
        name = Path(path).name.lower()
        if "singular" in name or "sparse_d12" in name:
            matches.append({"pid": pid, "path": path})
    return {
        "observer": "Darwin libproc proc_listpids plus proc_pidpath",
        "matches": matches,
        "pass": not matches,
    }


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


def refuse(reason: str, details: dict) -> int:
    if ATTEMPT.exists() or REFUSAL.exists():
        raise RuntimeError("package already consumed; refusal/attempt will not be overwritten")
    atomic_json(REFUSAL, {
        "schema": "KRENN_X5_ANCHOR_BASE81_EXACT_Q_REFUSAL_V1",
        "status": "REFUSED_ZERO_ARITHMETIC_NO_RELAUNCH",
        "pilot_id": "anchor_no_rectangle_base81_exact_q",
        "reason": reason,
        "arithmetic_process_started": False,
        "details": details,
    })
    return 2


def root_relative_file(value: str) -> Path:
    path = (ROOT / value).resolve()
    path.relative_to(ROOT.resolve())
    assert path.is_file()
    return path


def validate_clearance() -> dict:
    if not CLEARANCE.is_file():
        raise ValueError("MISSING_OR_INVALID_CLEARANCE")
    value = json.loads(CLEARANCE.read_text())
    required = {
        "schema", "status", "pilot_id", "held_plan_sha256",
        "held_package_manifest_sha256", "independent_plan_audit_result_path",
        "independent_plan_audit_result_sha256", "independent_plan_audit_manifest_path",
        "independent_plan_audit_manifest_sha256", "manager_clearance",
        "resource_clearance", "no_overlap_confirmed", "launch_exactly_once",
        "nonce", "issued_unix_seconds", "expires_unix_seconds",
    }
    if set(value) != required:
        raise ValueError("MISSING_OR_INVALID_CLEARANCE")
    if value["schema"] != "KRENN_X5_ANCHOR_BASE81_EXACT_Q_FRESH_CLEARANCE_V1":
        raise ValueError("MISSING_OR_INVALID_CLEARANCE")
    if value["status"] != "EXPLICIT_MANAGER_AND_RESOURCE_CLEARANCE":
        raise ValueError("MISSING_OR_INVALID_CLEARANCE")
    if value["pilot_id"] != "anchor_no_rectangle_base81_exact_q":
        raise ValueError("MISSING_OR_INVALID_CLEARANCE")
    if value["held_plan_sha256"] != PLAN_SHA or value["held_package_manifest_sha256"] != sha(MANIFEST):
        raise ValueError("HELD_PACKAGE_PIN_MISMATCH")
    if not all(value[key] is True for key in ("manager_clearance", "resource_clearance", "no_overlap_confirmed", "launch_exactly_once")):
        raise ValueError("MISSING_OR_INVALID_CLEARANCE")
    if not isinstance(value["nonce"], str) or len(value["nonce"]) < 16:
        raise ValueError("MISSING_OR_INVALID_CLEARANCE")
    now = time.time()
    if not (value["issued_unix_seconds"] <= now <= value["expires_unix_seconds"]):
        raise ValueError("CLEARANCE_EXPIRED")
    if value["expires_unix_seconds"] - value["issued_unix_seconds"] > 900:
        raise ValueError("MISSING_OR_INVALID_CLEARANCE")
    audit_result = root_relative_file(value["independent_plan_audit_result_path"])
    audit_manifest = root_relative_file(value["independent_plan_audit_manifest_path"])
    if sha(audit_result) != value["independent_plan_audit_result_sha256"] or sha(audit_manifest) != value["independent_plan_audit_manifest_sha256"]:
        raise ValueError("INDEPENDENT_AUDIT_PIN_MISMATCH")
    return value


def verify_static_pins() -> None:
    assert sha(SOURCE) == SOURCE_SHA and SOURCE.stat().st_size == SOURCE_BYTES
    assert sha(PLAN) == PLAN_SHA
    assert sha(SINGULAR) == SINGULAR_SHA and sha(GTIMEOUT) == GTIMEOUT_SHA
    source = SOURCE.read_text()
    assert source.count("ring r=0,") == 1 and "ring r=32003," not in source
    assert source.endswith(EPILOGUE.read_text())
    assert source.count("ideal G=slimgb(I);") == 1
    assert source.count("poly remainder=reduce(1,G);") == 1


def held_check() -> int:
    verify_static_pins()
    assert MANIFEST.is_file()
    assert not CLEARANCE.exists() and not ATTEMPT.exists() and not REFUSAL.exists()
    assert not list(HERE.glob("*.tmp"))
    print(json.dumps({
        "status": "READY_HELD_ZERO_RUNS",
        "source_sha256": SOURCE_SHA,
        "source_bytes": SOURCE_BYTES,
        "clearance_absent": True,
        "attempt_absent": True,
        "refusal_absent": True,
    }, sort_keys=True))
    return 0


def launch() -> int:
    if ATTEMPT.exists() or REFUSAL.exists():
        raise RuntimeError("package already consumed; no overwrite or relaunch")
    try:
        verify_static_pins()
        clearance = validate_clearance()
    except (AssertionError, OSError) as error:
        return refuse("SOURCE_OR_SOLVER_PIN_MISMATCH", {"error": repr(error)})
    except (ValueError, json.JSONDecodeError) as error:
        reason = str(error) if str(error) in {
            "MISSING_OR_INVALID_CLEARANCE", "CLEARANCE_EXPIRED",
            "INDEPENDENT_AUDIT_PIN_MISMATCH", "HELD_PACKAGE_PIN_MISMATCH",
        } else "MISSING_OR_INVALID_CLEARANCE"
        return refuse(reason, {"error": repr(error)})
    try:
        census = fresh_process_census()
    except OSError as error:
        return refuse("LIBPROC_OBSERVER_FAILURE", {"error": repr(error)})
    if not census["pass"]:
        return refuse("PROCESS_CENSUS_NONEMPTY", {"census": census})

    ATTEMPT.mkdir()
    atomic_json(ATTEMPT / "preflight.json", {
        "schema": "KRENN_X5_ANCHOR_BASE81_EXACT_Q_PREFLIGHT_V1",
        "clearance_sha256": sha(CLEARANCE),
        "census": census,
        "source_sha256": SOURCE_SHA,
        "singular_sha256": SINGULAR_SHA,
        "gtimeout_sha256": GTIMEOUT_SHA,
    })
    attempt_source = ATTEMPT / SOURCE.name
    atomic_bytes(attempt_source, SOURCE.read_bytes())
    assert sha(attempt_source) == SOURCE_SHA
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
                    breach = "LIBPROC_OBSERVER_FAILURE"
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
    stdout_text = stdout_path.read_text(errors="replace")
    parsed = {}
    for line in stdout_text.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if key in {"INPUT_VARIABLES", "INPUT_GENERATORS", "GROEBNER_SIZE", "UNIT_REMAINDER", "STATUS"}:
                parsed[key] = value
    if breach is None and returncode == 124:
        breach = "NATIVE_WALL_CAP"
    elif breach is None and returncode != 0:
        breach = "SINGULAR_NONZERO"
    unit = breach is None and returncode == 0 and parsed == {
        "INPUT_VARIABLES": "81", "INPUT_GENERATORS": "6561",
        "GROEBNER_SIZE": "1", "UNIT_REMAINDER": "0", "STATUS": "UNIT_IDEAL",
    }
    atomic_json(ATTEMPT / "watchdog.json", {
        "schema": "KRENN_X5_ANCHOR_BASE81_EXACT_Q_WATCHDOG_V1",
        "status": "PASS" if breach is None else "TERMINAL_FAILURE",
        "command": command, "source_sha256": SOURCE_SHA,
        "native_wall_seconds": NATIVE_WALL, "wrapper_wall_seconds": WRAPPER_WALL,
        "rss_limit_kib": RSS_LIMIT_KIB, "elapsed_seconds": round(time.monotonic() - started, 6),
        "returncode": returncode, "breach": breach,
        "peak_rss_kib": max((sample["rss_kib"] for sample in samples), default=None),
        "samples": samples, "stdout_sha256": sha(stdout_path), "stderr_sha256": sha(stderr_path),
        "logs_atomic": not stdout_tmp.exists() and not stderr_tmp.exists(),
        "automatic_relaunch": False, "second_lane": False,
    })
    atomic_json(ATTEMPT / "result.json", {
        "schema": "KRENN_X5_ANCHOR_BASE81_EXACT_Q_RESULT_V1",
        "status": "UNIT_IDEAL_EXACT_Q_BASE81" if unit else "TERMINAL_NONUNIT_OR_FAILURE",
        "field": "Q", "same_chart_only": True, "unit_ideal": unit,
        "input_variables": 81, "input_generators": 6561,
        "source_sha256": SOURCE_SHA, "parsed_stdout": parsed,
        "returncode": returncode, "breach": breach,
        "watchdog_sha256": sha(ATTEMPT / "watchdog.json"),
        "preflight_sha256": sha(ATTEMPT / "preflight.json"),
        "clearance_sha256": sha(CLEARANCE), "clearance_nonce": clearance["nonce"],
        "automatic_relaunch": False, "second_lane": False, "q_lane": True,
        "independent_terminal_audit_required": True,
    })
    return 0 if unit else 2


if __name__ == "__main__":
    if sys.argv == [sys.argv[0], "--check-held"]:
        raise SystemExit(held_check())
    if sys.argv == [sys.argv[0], "--launch"]:
        raise SystemExit(launch())
    raise SystemExit("usage: run_pilot.py --check-held | --launch")

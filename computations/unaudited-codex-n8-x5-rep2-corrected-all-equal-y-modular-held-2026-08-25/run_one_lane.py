#!/usr/bin/env python3
"""Refusal-by-default runner for one independently cleared rep2 modular lane."""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import signal
import subprocess
import time
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "rep2_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
SINGULAR = Path("/usr/local/bin/Singular")
GTIMEOUT = Path("/usr/local/bin/gtimeout")
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25"
PINS = {
    DESIGN / "MANIFEST.sha256": "ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2",
    DESIGN / "rep2_corrected_guard_minor_tiny_y_Q.sing": "0285c34fcae56db7dc60830197d645799f5f1c90d84467868436ee453916aedf",
    SINGULAR: "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    GTIMEOUT: "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}
NATIVE_WALL = 180
WRAPPER_WALL = 195
RSS_CAP = 8 * 1024**3
POLL_SECONDS = 0.1
TERM_THEN_KILL_SECONDS = 5


class RUsageInfoV2(ctypes.Structure):
    _fields_ = [
        ("uuid", ctypes.c_uint8 * 16), ("user_time", ctypes.c_uint64),
        ("system_time", ctypes.c_uint64), ("pkg_idle_wkups", ctypes.c_uint64),
        ("interrupt_wkups", ctypes.c_uint64), ("pageins", ctypes.c_uint64),
        ("wired_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64),
        ("phys_footprint", ctypes.c_uint64), ("proc_start_abstime", ctypes.c_uint64),
        ("proc_exit_abstime", ctypes.c_uint64), ("child_user_time", ctypes.c_uint64),
        ("child_system_time", ctypes.c_uint64), ("child_pkg_idle_wkups", ctypes.c_uint64),
        ("child_interrupt_wkups", ctypes.c_uint64), ("child_pageins", ctypes.c_uint64),
        ("child_elapsed_abstime", ctypes.c_uint64), ("diskio_bytesread", ctypes.c_uint64),
        ("diskio_byteswritten", ctypes.c_uint64),
    ]


LIBPROC = ctypes.CDLL("/usr/lib/libproc.dylib")
LIBPROC.proc_pid_rusage.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
LIBPROC.proc_pid_rusage.restype = ctypes.c_int


def rss_bytes(pid):
    record = RUsageInfoV2()
    return record.resident_size if LIBPROC.proc_pid_rusage(pid, 2, ctypes.byref(record)) == 0 else 0


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def require_clearance():
    manifest = HERE / "MANIFEST.sha256"
    referee_path = HERE / "independent_referee_acceptance.json"
    clearance_path = HERE / "launch_clearance.json"
    assert manifest.exists() and referee_path.exists() and clearance_path.exists(), "HELD: referee acceptance and explicit launch clearance are both required"
    manifest_sha = sha256(manifest)
    source_sha = sha256(SOURCE)
    runner_sha = sha256(Path(__file__))
    referee = json.loads(referee_path.read_text())
    assert referee == {
        "schema": "KRENN_X5_REP2_ALL_EQUAL_Y_INDEPENDENT_ACCEPTANCE_V1",
        "status": "PASS_APPROVE_ONE_MODULAR_DIAGNOSTIC_ONLY",
        "held_manifest_sha256": manifest_sha,
        "source_sha256": source_sha,
        "runner_sha256": runner_sha,
        "singular_sha256": PINS[SINGULAR],
        "gtimeout_sha256": PINS[GTIMEOUT],
        "variables": 91,
        "generators": 6577,
        "maximum_lane_count": 1,
        "exact_Q_authorized": False,
        "second_lane_authorized": False,
        "automatic_relaunch_authorized": False,
    }
    clearance = json.loads(clearance_path.read_text())
    assert clearance == {
        "schema": "KRENN_X5_REP2_ALL_EQUAL_Y_EXPLICIT_LAUNCH_CLEARANCE_V1",
        "status": "CLEARED_ONE_MODULAR_DIAGNOSTIC_ONLY",
        "held_manifest_sha256": manifest_sha,
        "independent_referee_acceptance_sha256": sha256(referee_path),
        "source_sha256": source_sha,
        "maximum_lane_count": 1,
        "native_wall_seconds": NATIVE_WALL,
        "wrapper_wall_seconds": WRAPPER_WALL,
        "rss_cap_bytes": RSS_CAP,
        "gtimeout_sha256": PINS[GTIMEOUT],
        "exact_Q_authorized": False,
        "second_lane_authorized": False,
        "automatic_relaunch_authorized": False,
    }
    return manifest_sha, sha256(referee_path), sha256(clearance_path), source_sha, runner_sha


for path, expected in PINS.items():
    assert sha256(path) == expected, (path, sha256(path), expected)
assert not (HERE / "result.json").exists(), "fresh atomic output required; no relaunch"
held_manifest_sha, referee_sha, clearance_sha, source_sha, runner_sha = require_clearance()

started = time.monotonic()
process = subprocess.Popen(
    [str(SINGULAR), str(SOURCE)], cwd=HERE, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
)
print(json.dumps({"event": "STARTED", "singular_pid": process.pid}), flush=True)
peak = 0
termination = None
while process.poll() is None:
    peak = max(peak, rss_bytes(process.pid))
    elapsed = time.monotonic() - started
    if peak > RSS_CAP:
        termination = "RSS_CAP_8GIB"
    elif elapsed > NATIVE_WALL:
        termination = "NATIVE_WALL_CAP_180"
    if termination:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        deadline = time.monotonic() + TERM_THEN_KILL_SECONDS
        while process.poll() is None and time.monotonic() < deadline:
            time.sleep(POLL_SECONDS)
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        break
    time.sleep(POLL_SECONDS)

stdout, stderr = process.communicate()
wall = time.monotonic() - started
unit = termination is None and process.returncode == 0 and "STATUS=UNIT_IDEAL" in stdout and "UNIT_REMAINDER=0" in stdout
nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
status = (
    "UNIT_IDEAL_MODULAR_DIAGNOSTIC" if unit else
    "NONUNIT_MODULAR_DIAGNOSTIC" if nonunit else
    "FAIL_CLOSED_RESOURCE_GATE" if termination else
    "FAIL_CLOSED_PROCESS_OR_SCHEMA"
)
result = {
    "schema": "KRENN_X5_REP2_ALL_EQUAL_Y_ONE_LANE_RESULT_V1",
    "status": status,
    "diagnostic_only": True,
    "mathematical_coverage": False,
    "chart": "all-equal-y/i0/p00/x0/y0/d01",
    "field": "F_32003",
    "native_wall_cap_seconds": NATIVE_WALL,
    "wrapper_wall_cap_seconds": WRAPPER_WALL,
    "rss_cap_bytes": RSS_CAP,
    "wall_seconds": wall,
    "observed_peak_rss_bytes": peak,
    "termination": termination,
    "returncode": process.returncode,
    "held_manifest_sha256": held_manifest_sha,
    "independent_referee_acceptance_sha256": referee_sha,
    "launch_clearance_sha256": clearance_sha,
    "source_sha256": source_sha,
    "runner_sha256": runner_sha,
    "singular_sha256": PINS[SINGULAR],
    "stdout": stdout,
    "stderr": stderr,
    "second_lane_launched": False,
    "exact_Q_launched": False,
    "automatic_relaunch": False,
}
atomic_json(HERE / "result.json", result)
print(json.dumps({"event": "TERMINAL", "status": status, "wall": wall, "peak": peak}, sort_keys=True))

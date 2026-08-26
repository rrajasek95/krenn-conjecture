#!/usr/bin/env python3
"""Refusal-by-default runner for exactly one independently cleared rep5 lane."""
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
SOURCE = HERE / "rep5_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
SINGULAR = Path("/usr/local/bin/Singular")
GTIMEOUT = Path("/usr/local/bin/gtimeout")
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-referee-2026-08-25"
PINS = {
    DESIGN / "MANIFEST.sha256": "33ae759fb235518412c33d36d621ccce09b8a9e05e9ece05b6d1aaf7f2d8c40c",
    DESIGN / "rep5_guard_minor_tiny_y_p32003.sing": "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97",
    REFEREE / "FINAL_MANIFEST.sha256": "ad86daeae93aaa154ef9ade124c719c8e683c3ae1b95130f948a2d90c0fc495a",
    REFEREE / "HELD_MODULAR_PILOT.json": "0df5f63b08cb3f601a5d77d22f07293e557f6dae6b7e727849916d943e5b70c7",
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


def rss_bytes(pid: int) -> int:
    record = RUsageInfoV2()
    return record.resident_size if LIBPROC.proc_pid_rusage(pid, 2, ctypes.byref(record)) == 0 else 0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def require_clearance() -> tuple[str, str, str, str, str]:
    manifest = HERE / "MANIFEST.sha256"
    acceptance_path = HERE / "independent_referee_acceptance.json"
    clearance_path = HERE / "launch_clearance.json"
    assert manifest.exists(), "HELD: sealed MANIFEST.sha256 required"
    assert acceptance_path.exists(), "HELD: exact independent referee acceptance required"
    assert clearance_path.exists(), "HELD: explicit launch clearance required"
    manifest_sha = sha256(manifest)
    source_sha = sha256(SOURCE)
    runner_sha = sha256(Path(__file__))

    # Acceptance is intentionally byte-identical to the independent rep5
    # referee's held pilot.  Rep2 material is neither read nor accepted.
    assert sha256(acceptance_path) == PINS[REFEREE / "HELD_MODULAR_PILOT.json"]
    assert acceptance_path.read_bytes() == (REFEREE / "HELD_MODULAR_PILOT.json").read_bytes()
    acceptance = json.loads(acceptance_path.read_text())
    assert acceptance["schema"] == "KRENN_X5_REP5_GUARD_MINOR_HELD_MODULAR_PILOT_V1"
    assert acceptance["status"] == "HELD_NOT_LAUNCHED"
    assert acceptance["source"]["sha256"] == source_sha
    assert acceptance["source"]["variables"] == 91
    assert acceptance["source"]["generators"] == 6577
    assert acceptance["source"]["chart"] == [0, 0, 0, 0, "y", 0, 0, 1]
    assert acceptance["scope"] == {"ideal_runs": 0, "launched": False}

    clearance = json.loads(clearance_path.read_text())
    assert clearance == {
        "schema": "KRENN_X5_REP5_ALL_EQUAL_Y_EXPLICIT_LAUNCH_CLEARANCE_V1",
        "status": "CLEARED_ONE_MODULAR_DIAGNOSTIC_ONLY",
        "held_manifest_sha256": manifest_sha,
        "independent_referee_final_manifest_sha256": PINS[REFEREE / "FINAL_MANIFEST.sha256"],
        "independent_referee_acceptance_sha256": sha256(acceptance_path),
        "source_sha256": source_sha,
        "runner_sha256": runner_sha,
        "singular_sha256": PINS[SINGULAR],
        "gtimeout_sha256": PINS[GTIMEOUT],
        "maximum_lane_count": 1,
        "native_wall_seconds": NATIVE_WALL,
        "wrapper_wall_seconds": WRAPPER_WALL,
        "rss_cap_bytes": RSS_CAP,
        "exact_Q_authorized": False,
        "second_lane_authorized": False,
        "automatic_relaunch_authorized": False,
    }
    return manifest_sha, sha256(acceptance_path), sha256(clearance_path), source_sha, runner_sha


for pinned_path, expected in PINS.items():
    assert sha256(pinned_path) == expected, (pinned_path, sha256(pinned_path), expected)
assert sha256(SOURCE) == PINS[DESIGN / "rep5_guard_minor_tiny_y_p32003.sing"]
assert not (HERE / "result.json").exists(), "fresh atomic output required; no relaunch"
held_manifest_sha, acceptance_sha, clearance_sha, source_sha, runner_sha = require_clearance()

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
    "schema": "KRENN_X5_REP5_ALL_EQUAL_Y_ONE_LANE_RESULT_V1",
    "status": status,
    "diagnostic_only": True,
    "mathematical_coverage": False,
    "representative": "rep5",
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
    "independent_referee_acceptance_sha256": acceptance_sha,
    "launch_clearance_sha256": clearance_sha,
    "source_sha256": source_sha,
    "runner_sha256": runner_sha,
    "singular_sha256": PINS[SINGULAR],
    "stdout": stdout,
    "stderr": stderr,
    "second_lane_launched": False,
    "exact_Q_launched": False,
    "automatic_relaunch": False,
    "rep2_equivalence_used": False,
}
atomic_json(HERE / "result.json", result)
print(json.dumps({"event": "TERMINAL", "status": status, "wall": wall, "peak": peak}, sort_keys=True))

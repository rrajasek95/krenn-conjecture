#!/usr/bin/env python3
"""Single-use, refusal-by-default rep5 runner with internal wrapper enforcement."""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import re
import signal
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "rep5_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"
SINGULAR = Path("/usr/local/bin/Singular")
GTIMEOUT = Path("/usr/local/bin/gtimeout")
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"
SOURCE_REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-referee-2026-08-25"
REJECTION = ROOT / "computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-referee-2026-08-25"
PRIOR_HELD = ROOT / "computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-2026-08-25"
PINS = {
    DESIGN / "MANIFEST.sha256": "33ae759fb235518412c33d36d621ccce09b8a9e05e9ece05b6d1aaf7f2d8c40c",
    DESIGN / "rep5_guard_minor_tiny_y_p32003.sing": "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97",
    SOURCE_REFEREE / "FINAL_MANIFEST.sha256": "ad86daeae93aaa154ef9ade124c719c8e683c3ae1b95130f948a2d90c0fc495a",
    SOURCE_REFEREE / "HELD_MODULAR_PILOT.json": "0df5f63b08cb3f601a5d77d22f07293e557f6dae6b7e727849916d943e5b70c7",
    REJECTION / "FINAL_MANIFEST.sha256": "02adea071c6f3eef5a4623ec25afb12f06dd38cec5426a7eed6ced74ff194dbb",
    REJECTION / "results_referee.json": "90ba1b91d1c7b27509227c74be7b03e0bb72aeac7ea8ab3a24ede4f39b500c14",
    PRIOR_HELD / "MANIFEST.sha256": "dcacfb67e77a36a3eeab2caff442b22695cf62ebce49f231c8151a52439985bc",
    SINGULAR: "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    GTIMEOUT: "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}
NATIVE_WALL = 180
WRAPPER_WALL = 195
RSS_CAP = 8 * 1024**3
POLL_SECONDS = 0.1
TERM_THEN_KILL_SECONDS = 5
MAX_CLEARANCE_LIFETIME_SECONDS = 600
SOURCE_SHA = "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97"
FORBIDDEN_EXECUTABLE_BASENAMES = (
    "Singular", "gtimeout", "sparse_d12_dual", "sparse_d12_dual_v4_1",
    "sparse_d12_dual_fixed_lane", "sparse_d12_dual_portfolio_audit",
)


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
LIBPROC.proc_listpgrppids.argtypes = [ctypes.c_uint32, ctypes.c_void_p, ctypes.c_int]
LIBPROC.proc_listpgrppids.restype = ctypes.c_int
LIBPROC.proc_listallpids.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIBPROC.proc_listallpids.restype = ctypes.c_int
LIBPROC.proc_pidpath.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
LIBPROC.proc_pidpath.restype = ctypes.c_int


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def exclusive_json(path: Path, value: object) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w") as stream:
            stream.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        raise


def all_pids() -> list[int]:
    buffer = (ctypes.c_int * 65536)()
    count = LIBPROC.proc_listallpids(ctypes.byref(buffer), ctypes.sizeof(buffer))
    assert 0 <= count < len(buffer), "fail closed: all-process census failed or overflowed"
    return [buffer[index] for index in range(count) if buffer[index] > 0]


def pid_path(pid: int) -> str | None:
    buffer = ctypes.create_string_buffer(4096)
    length = LIBPROC.proc_pidpath(pid, ctypes.byref(buffer), ctypes.sizeof(buffer))
    return buffer.value[:length].decode("utf-8", "strict") if length > 0 else None


def fresh_process_census() -> dict:
    matches = []
    observed = 0
    unobservable = 0
    for pid in all_pids():
        if pid == os.getpid():
            continue
        path = pid_path(pid)
        if path is None:
            unobservable += 1
            continue
        observed += 1
        if Path(path).name in FORBIDDEN_EXECUTABLE_BASENAMES:
            matches.append({"pid": pid, "path": path})
    policy = {
        "method": "libproc proc_listallpids + proc_pidpath",
        "forbidden_executable_basenames": list(FORBIDDEN_EXECUTABLE_BASENAMES),
        "self_pid_excluded": True,
    }
    return {
        "policy": policy,
        "policy_sha256": canonical_sha(policy),
        "observed_paths": observed,
        "unobservable_pids": unobservable,
        "matches": matches,
        "match_count": len(matches),
        "captured_unix_seconds": time.time(),
    }


def process_group_pids(pgid: int) -> list[int]:
    buffer = (ctypes.c_int * 4096)()
    count = LIBPROC.proc_listpgrppids(pgid, ctypes.byref(buffer), ctypes.sizeof(buffer))
    if not (0 <= count < len(buffer)):
        raise RuntimeError("process-group census failure")
    return [buffer[index] for index in range(count) if buffer[index] > 0]


def process_rss_bytes(pid: int) -> int | None:
    record = RUsageInfoV2()
    return record.resident_size if LIBPROC.proc_pid_rusage(pid, 2, ctypes.byref(record)) == 0 else None


def process_group_rss_bytes(pgid: int, wrapper_alive: bool) -> tuple[int, int]:
    members = process_group_pids(pgid)
    if wrapper_alive and not members:
        raise RuntimeError("live wrapper has no observable process-group members")
    total = 0
    for pid in members:
        rss = process_rss_bytes(pid)
        if rss is None:
            # Ignore only a proven exit race.  A still-listed unobservable member
            # makes the resource observer fail closed.
            if pid in process_group_pids(pgid):
                raise RuntimeError(f"rusage observation failure for live group member {pid}")
            continue
        total += rss
    return total, len(members)


def parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert parsed.tzinfo is not None
    return parsed.astimezone(timezone.utc)


def clearance_and_census() -> tuple[dict, dict, str, str, str, str, str]:
    manifest = HERE / "MANIFEST.sha256"
    acceptance_path = HERE / "independent_referee_acceptance.json"
    clearance_path = HERE / "launch_clearance.json"
    assert manifest.is_file() and acceptance_path.is_file() and clearance_path.is_file(), "HELD: referee acceptance and fresh clearance required"
    manifest_sha = sha256(manifest)
    source_sha = sha256(SOURCE)
    runner_sha = sha256(Path(__file__))
    acceptance = json.loads(acceptance_path.read_text())
    assert acceptance == {
        "schema": "KRENN_X5_REP5_ALL_EQUAL_Y_V2_INDEPENDENT_ACCEPTANCE_V1",
        "status": "PASS_APPROVE_ONE_HARDENED_MODULAR_DIAGNOSTIC_ONLY",
        "held_manifest_sha256": manifest_sha,
        "source_sha256": source_sha,
        "runner_sha256": runner_sha,
        "source_referee_manifest_sha256": PINS[SOURCE_REFEREE / "FINAL_MANIFEST.sha256"],
        "rejection_manifest_sha256": PINS[REJECTION / "FINAL_MANIFEST.sha256"],
        "singular_sha256": PINS[SINGULAR],
        "gtimeout_sha256": PINS[GTIMEOUT],
        "variables": 91, "generators": 6577, "maximum_lane_count": 1,
        "exact_Q_authorized": False, "second_lane_authorized": False,
        "automatic_relaunch_authorized": False,
    }
    clearance = json.loads(clearance_path.read_text())
    assert set(clearance) == {
        "schema", "status", "held_manifest_sha256", "independent_referee_acceptance_sha256",
        "source_sha256", "runner_sha256", "singular_sha256", "gtimeout_sha256",
        "nonce", "issued_at_utc", "expires_at_utc", "maximum_lane_count",
        "native_wall_seconds", "wrapper_wall_seconds", "rss_cap_bytes",
        "no_overlap_confirmed", "manager_clearance_confirmed", "resource_clearance_confirmed",
        "census_policy_sha256", "expected_census_match_count", "exact_Q_authorized",
        "second_lane_authorized", "automatic_relaunch_authorized",
    }
    assert clearance["schema"] == "KRENN_X5_REP5_ALL_EQUAL_Y_V2_EXPLICIT_LAUNCH_CLEARANCE_V1"
    assert clearance["status"] == "CLEARED_ONE_HARDENED_MODULAR_DIAGNOSTIC_ONLY"
    assert clearance["held_manifest_sha256"] == manifest_sha
    assert clearance["independent_referee_acceptance_sha256"] == sha256(acceptance_path)
    assert clearance["source_sha256"] == source_sha and clearance["runner_sha256"] == runner_sha
    assert clearance["singular_sha256"] == PINS[SINGULAR] and clearance["gtimeout_sha256"] == PINS[GTIMEOUT]
    assert re.fullmatch(r"[0-9a-f]{32}", clearance["nonce"])
    issued, expires, now = parse_utc(clearance["issued_at_utc"]), parse_utc(clearance["expires_at_utc"]), datetime.now(timezone.utc)
    assert issued <= now < expires and 0 < (expires - issued).total_seconds() <= MAX_CLEARANCE_LIFETIME_SECONDS
    assert clearance["maximum_lane_count"] == 1
    assert clearance["native_wall_seconds"] == NATIVE_WALL and clearance["wrapper_wall_seconds"] == WRAPPER_WALL
    assert clearance["rss_cap_bytes"] == RSS_CAP
    assert clearance["no_overlap_confirmed"] is True
    assert clearance["manager_clearance_confirmed"] is True and clearance["resource_clearance_confirmed"] is True
    assert clearance["expected_census_match_count"] == 0
    assert clearance["exact_Q_authorized"] is False and clearance["second_lane_authorized"] is False
    assert clearance["automatic_relaunch_authorized"] is False
    census = fresh_process_census()
    assert clearance["census_policy_sha256"] == census["policy_sha256"]
    assert census["match_count"] == 0, census["matches"]
    return clearance, census, manifest_sha, sha256(acceptance_path), sha256(clearance_path), source_sha, runner_sha


for pinned_path, expected in PINS.items():
    assert sha256(pinned_path) == expected, (pinned_path, sha256(pinned_path), expected)
assert sha256(SOURCE) == SOURCE_SHA
for stale in ("ATTEMPT.json", "result.json", "result.json.tmp", "stdout.log", "stderr.log", "watchdog.json"):
    assert not (HERE / stale).exists(), f"single-use terminal refusal: stale {stale} exists"
assert not any(HERE.glob("*.tmp")), "single-use terminal refusal: stale temporary exists"
clearance, census, manifest_sha, acceptance_sha, clearance_sha, source_sha, runner_sha = clearance_and_census()
attempt = {
    "schema": "KRENN_X5_REP5_ALL_EQUAL_Y_V2_ATTEMPT_V1", "status": "ATTEMPT_CONSUMED",
    "nonce": clearance["nonce"], "created_at_utc": datetime.now(timezone.utc).isoformat(),
    "manifest_sha256": manifest_sha, "clearance_sha256": clearance_sha,
    "source_sha256": source_sha, "runner_sha256": runner_sha, "prelaunch_census": census,
    "relaunch_forbidden_even_if_no_result": True,
}
exclusive_json(HERE / "ATTEMPT.json", attempt)

command = [str(GTIMEOUT), "--signal=TERM", f"--kill-after={TERM_THEN_KILL_SECONDS}s", f"{WRAPPER_WALL}s", str(SINGULAR), str(SOURCE)]
started = time.monotonic()
try:
    process = subprocess.Popen(command, cwd=HERE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
except BaseException as error:
    atomic_json(HERE / "result.json", {
        "schema": "KRENN_X5_REP5_ALL_EQUAL_Y_V2_ONE_LANE_RESULT_V1",
        "status": "FAIL_CLOSED_POPEN", "diagnostic_only": True, "mathematical_coverage": False,
        "error": repr(error), "attempt_consumed": True, "automatic_relaunch": False,
    })
    raise
print(json.dumps({"event": "STARTED", "wrapper_pid": process.pid, "nonce": clearance["nonce"]}), flush=True)
peak = 0
peak_members = 0
termination = None
while process.poll() is None:
    try:
        current_rss, current_members = process_group_rss_bytes(process.pid, True)
    except RuntimeError as error:
        termination = "RESOURCE_OBSERVER_FAILURE:" + str(error)
        current_rss, current_members = peak, peak_members
    if current_rss > peak:
        peak, peak_members = current_rss, current_members
    elapsed = time.monotonic() - started
    if termination is None and peak > RSS_CAP:
        termination = "RSS_CAP_8GIB"
    elif termination is None and elapsed > NATIVE_WALL:
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
    "schema": "KRENN_X5_REP5_ALL_EQUAL_Y_V2_ONE_LANE_RESULT_V1", "status": status,
    "diagnostic_only": True, "mathematical_coverage": False, "attempt_consumed": True,
    "nonce": clearance["nonce"], "field": "F_32003", "variables": 91, "generators": 6577,
    "command": command, "internal_wrapper_enforced_seconds": WRAPPER_WALL,
    "native_wall_cap_seconds": NATIVE_WALL, "rss_cap_bytes": RSS_CAP,
    "wall_seconds": wall, "observed_peak_group_rss_bytes": peak,
    "observed_peak_group_members": peak_members, "termination": termination,
    "wrapper_returncode": process.returncode, "prelaunch_census": census,
    "held_manifest_sha256": manifest_sha, "independent_referee_acceptance_sha256": acceptance_sha,
    "launch_clearance_sha256": clearance_sha, "source_sha256": source_sha,
    "runner_sha256": runner_sha, "stdout": stdout, "stderr": stderr,
    "exact_Q_launched": False, "second_lane_launched": False,
    "automatic_relaunch": False, "rep2_equivalence_used": False,
}
atomic_json(HERE / "result.json", result)
print(json.dumps({"event": "TERMINAL", "status": status, "wall": wall, "peak": peak}, sort_keys=True))

#!/usr/bin/env python3
"""Single-use refusal-locked rep2 group16 combined p32003 diagnostic runner."""
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
SOURCE = HERE / "rep2_group016_torus_zerozero_guardpivot_k0_p32003.sing"
SINGULAR = Path("/usr/local/bin/Singular")
GTIMEOUT = Path("/usr/local/bin/gtimeout")
SOURCE_SHA = "66bdb9277c9bff605e0d8a808ca65beb5967afaaf8ae494193286a60338355c6"
SOURCE_DERIVATION_SHA = "1e08d3d13f7c069a3991e6a2871838c7960ba31dc2a923ac673270207fa297ad"
TIMEOUT_FINAL = ROOT / "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256"
TORUS_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-decomposition-design-2026-08-26/MANIFEST.sha256"
COMPARISON_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26/MANIFEST.sha256"
GUARD_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-isomorphism-guard-pivot-design-2026-08-26/MANIFEST.sha256"
TIMEOUT_FINAL_SHA = "066347c8af9a579b8f09d1c1eebf0197e819753da839f30708616287c4336196"
TORUS_MANIFEST_SHA = "1492e69373819fda0c50afc4f1366e2d6da90e857c26f73c03c0212ffd879282"
COMPARISON_MANIFEST_SHA = "1a2dcba289d5f31e39be48c4f98ff44a6b0c6891841fd345df52f06abfd5525a"
GUARD_MANIFEST_SHA = "6a781149041e8808d58a53af77059253fe0a0d4295052bfe34756a0f994a0aee"
SINGULAR_SHA = "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"
GTIMEOUT_SHA = "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"
NATIVE_WALL = 240
WRAPPER_WALL = 255
RSS_CAP = 8 * 1024**3
POLL_SECONDS = 0.1
KILL_AFTER = 5
MAX_CLEARANCE_LIFETIME_SECONDS = 600
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
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def exclusive_json(path: Path, value: object) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


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
        "policy": policy, "policy_sha256": canonical_sha(policy),
        "observed_paths": observed, "unobservable_pids": unobservable,
        "matches": matches, "match_count": len(matches),
        "captured_unix_seconds": time.time(),
    }


def process_group_pids(pgid: int) -> list[int]:
    buffer = (ctypes.c_int * 4096)()
    count = LIBPROC.proc_listpgrppids(pgid, ctypes.byref(buffer), ctypes.sizeof(buffer))
    if not 0 <= count < len(buffer):
        raise RuntimeError("process-group census failure")
    return [buffer[index] for index in range(count) if buffer[index] > 0]


def process_group_rss_bytes(pgid: int, wrapper_alive: bool) -> tuple[int, int]:
    members = process_group_pids(pgid)
    if wrapper_alive and not members:
        raise RuntimeError("live wrapper has no observable process-group members")
    total = 0
    for pid in members:
        record = RUsageInfoV2()
        if LIBPROC.proc_pid_rusage(pid, 2, ctypes.byref(record)) != 0:
            if pid in process_group_pids(pgid):
                raise RuntimeError(f"rusage observation failure for live group member {pid}")
            continue
        total += record.resident_size
    return total, len(members)


def parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert parsed.tzinfo is not None
    return parsed.astimezone(timezone.utc)


assert sha256(SOURCE) == SOURCE_SHA
assert sha256(HERE / "source_derivation.json") == SOURCE_DERIVATION_SHA
assert sha256(TIMEOUT_FINAL) == TIMEOUT_FINAL_SHA
assert sha256(TORUS_MANIFEST) == TORUS_MANIFEST_SHA
assert sha256(COMPARISON_MANIFEST) == COMPARISON_MANIFEST_SHA
assert sha256(GUARD_MANIFEST) == GUARD_MANIFEST_SHA
assert sha256(SINGULAR) == SINGULAR_SHA and sha256(GTIMEOUT) == GTIMEOUT_SHA
for stale in ("ATTEMPT.json", "result.json", "result.json.tmp", "stdout.log", "stderr.log", "watchdog.json", "RUN_EXCLUSIVE.lock"):
    assert not (HERE / stale).exists(), f"single-use terminal refusal: stale {stale} exists"
assert not any(HERE.glob("*.tmp"))
manifest = HERE / "MANIFEST.sha256"
acceptance_path = HERE / "independent_referee_acceptance.json"
clearance_path = HERE / "launch_clearance.json"
assert manifest.is_file() and acceptance_path.is_file() and clearance_path.is_file(), "HELD: independent acceptance and fresh explicit clearance required"
manifest_sha = sha256(manifest)
runner_sha = sha256(Path(__file__))
acceptance = json.loads(acceptance_path.read_text())
assert acceptance == {
    "schema": "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_INDEPENDENT_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_ONE_COMBINED_P32003_DIAGNOSTIC_ONLY",
    "held_manifest_sha256": manifest_sha,
    "source_derivation_sha256": SOURCE_DERIVATION_SHA,
    "source_sha256": SOURCE_SHA,
    "runner_sha256": runner_sha,
    "timeout_final_manifest_sha256": TIMEOUT_FINAL_SHA,
    "torus_producer_manifest_sha256": TORUS_MANIFEST_SHA,
    "comparison_referee_manifest_sha256": COMPARISON_MANIFEST_SHA,
    "guard_pivot_manifest_sha256": GUARD_MANIFEST_SHA,
    "torus_stratum": "A67=A12=0", "guard_pivot_k": 0,
    "variables": 67, "generators": 6574, "maximum_lane_count": 1,
    "exact_Q_authorized": False, "other_chart_authorized": False,
    "automatic_relaunch_authorized": False,
}
clearance = json.loads(clearance_path.read_text())
assert set(clearance) == {
    "schema", "status", "held_manifest_sha256", "independent_referee_acceptance_sha256",
    "source_sha256", "runner_sha256", "singular_sha256", "gtimeout_sha256", "nonce",
    "issued_at_utc", "expires_at_utc", "maximum_lane_count", "native_wall_seconds",
    "wrapper_wall_seconds", "rss_cap_bytes", "no_overlap_confirmed",
    "manager_clearance_confirmed", "resource_clearance_confirmed", "census_policy_sha256",
    "expected_census_match_count", "exact_Q_authorized", "other_chart_authorized",
    "automatic_relaunch_authorized",
}
assert clearance["schema"] == "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_EXPLICIT_CLEARANCE_V1"
assert clearance["status"] == "CLEARED_ONE_COMBINED_P32003_DIAGNOSTIC_ONLY"
assert clearance["held_manifest_sha256"] == manifest_sha
assert clearance["independent_referee_acceptance_sha256"] == sha256(acceptance_path)
assert clearance["source_sha256"] == SOURCE_SHA and clearance["runner_sha256"] == runner_sha
assert clearance["singular_sha256"] == SINGULAR_SHA and clearance["gtimeout_sha256"] == GTIMEOUT_SHA
assert re.fullmatch(r"[0-9a-f]{32}", clearance["nonce"])
issued = parse_utc(clearance["issued_at_utc"])
expires = parse_utc(clearance["expires_at_utc"])
now = datetime.now(timezone.utc)
assert issued <= now < expires and 0 < (expires - issued).total_seconds() <= MAX_CLEARANCE_LIFETIME_SECONDS
assert clearance["maximum_lane_count"] == 1
assert clearance["native_wall_seconds"] == NATIVE_WALL and clearance["wrapper_wall_seconds"] == WRAPPER_WALL
assert clearance["rss_cap_bytes"] == RSS_CAP
assert clearance["no_overlap_confirmed"] is clearance["manager_clearance_confirmed"] is clearance["resource_clearance_confirmed"] is True
assert clearance["expected_census_match_count"] == 0
assert clearance["exact_Q_authorized"] is clearance["other_chart_authorized"] is clearance["automatic_relaunch_authorized"] is False
census = fresh_process_census()
assert clearance["census_policy_sha256"] == census["policy_sha256"] and census["match_count"] == 0, census["matches"]
exclusive_json(HERE / "RUN_EXCLUSIVE.lock", {"nonce": clearance["nonce"], "manifest_sha256": manifest_sha, "runner_sha256": runner_sha})
exclusive_json(HERE / "ATTEMPT.json", {
    "schema": "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_ATTEMPT_V1",
    "status": "ATTEMPT_CONSUMED", "nonce": clearance["nonce"],
    "manifest_sha256": manifest_sha, "acceptance_sha256": sha256(acceptance_path),
    "clearance_sha256": sha256(clearance_path), "source_sha256": SOURCE_SHA,
    "runner_sha256": runner_sha, "prelaunch_census": census,
    "relaunch_forbidden_even_if_no_result": True,
})

command = [str(GTIMEOUT), "--signal=TERM", f"--kill-after={KILL_AFTER}s", f"{WRAPPER_WALL}s", str(SINGULAR), str(SOURCE)]
started = time.monotonic()
try:
    process = subprocess.Popen(command, cwd=HERE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
except BaseException as error:
    atomic_json(HERE / "result.json", {
        "schema": "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_RESULT_V1",
        "status": "FAIL_CLOSED_POPEN", "error": repr(error), "attempt_consumed": True,
        "diagnostic_only": True, "mathematical_coverage": False, "automatic_relaunch": False,
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
        termination = "NATIVE_WALL_CAP_240"
    if termination:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        deadline = time.monotonic() + KILL_AFTER
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
unit = termination is None and process.returncode == 0 and all(token in stdout for token in (
    "INPUT_VARIABLES=67", "INPUT_GENERATORS=6574", "GROEBNER_SIZE=1",
    "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL",
))
nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
status = "UNIT_IDEAL_MODULAR_DIAGNOSTIC" if unit else "NONUNIT_MODULAR_DIAGNOSTIC" if nonunit else "FAIL_CLOSED_RESOURCE_GATE" if termination else "FAIL_CLOSED_PROCESS_OR_SCHEMA"
result = {
    "schema": "KRENN_X5_REP2_GROUP16_COMBINED_SMALLEST_MODULAR_RESULT_V1",
    "status": status, "diagnostic_only": True, "mathematical_coverage": False,
    "attempt_consumed": True, "field": "F_32003", "torus_stratum": "A67=A12=0",
    "guard_pivot_k": 0, "variables": 67, "generators": 6574, "command": command,
    "native_wall_cap_seconds": NATIVE_WALL, "wrapper_wall_seconds": WRAPPER_WALL,
    "rss_cap_bytes": RSS_CAP, "wall_seconds": wall, "peak_group_rss_bytes": peak,
    "peak_group_members": peak_members, "termination": termination,
    "returncode": process.returncode, "source_sha256": SOURCE_SHA,
    "runner_sha256": runner_sha, "stdout": stdout, "stderr": stderr,
    "exact_Q_launched": False, "other_chart_launched": False,
    "prior_timeout_reused": False, "automatic_relaunch": False,
}
atomic_json(HERE / "result.json", result)
print(json.dumps({"event": "TERMINAL", "status": status, "wall": wall, "peak": peak}, sort_keys=True))

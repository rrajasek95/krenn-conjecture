#!/usr/bin/env python3
"""Single-use refusal-locked rep5 torus-smallest exact-Q conditional runner."""
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

from verify_future_dependency import verify_dependency

if not __debug__:
    raise RuntimeError("fail closed: assertions required")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "rep5_k2_t1_torus_smallest_Q.sing"
SINGULAR = Path("/usr/local/bin/Singular")
GTIMEOUT = Path("/usr/local/bin/gtimeout")
SOURCE_SHA = "4c788634af62bf0a98a2e8ddc2ab337baca292081ecc48f955c3622b87aff637"
PRODUCER_MANIFEST_SHA = "2b220f91ffa21c28506f5112a3a3e7fe791c7e3c783c1e7a319186628743659e"
REFEREE_MANIFEST_SHA = "20f24c8de6e7edb0818c30c11df4716e983fd5f8bf5778ee36d6d3bccf27d0ff"
PRIOR_TERMINAL_MANIFEST_SHA = "0cb2ba3080ddda143ac01e4fd9f8714876c070ee86e7e574415c22cae4cac4ff"
MODULAR_HELD_MANIFEST_SHA = "21df0017be41a8ec9e4035b0902649cf9c8ed97d43c65c88a93d1db7f8bf6d72"
MODULAR_REFEREE_MANIFEST_SHA = "16a32d07221def48a9e8388ca1e8b716cd71dfb44c2dc0cbea0bb22ab91203ab"
ASSIGNMENT = {"yn1": 1, "yn2": 1, "t0": 1, "t2": 0}
PRODUCER_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26/MANIFEST.sha256"
REFEREE_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-referee-2026-08-26/MANIFEST.sha256"
PRIOR_TERMINAL_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256"
MODULAR_HELD_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-torus-cover-smallest-modular-held-2026-08-26/MANIFEST.sha256"
MODULAR_REFEREE_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-torus-cover-smallest-modular-held-referee-2026-08-26/MANIFEST.sha256"
SINGULAR_SHA = "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"
GTIMEOUT_SHA = "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"
NATIVE_WALL = 480
WRAPPER_WALL = 510
RSS_CAP = 8 * 1024**3
POLL_SECONDS = 0.1
KILL_AFTER = 5
MAX_CLEARANCE_LIFETIME_SECONDS = 600
FORBIDDEN_EXECUTABLE_BASENAMES = ("Singular", "gtimeout", "sparse_d12_dual", "sparse_d12_dual_v4_1", "sparse_d12_dual_fixed_lane", "sparse_d12_dual_portfolio_audit")


class RUsageInfoV2(ctypes.Structure):
    _fields_ = [("uuid", ctypes.c_uint8 * 16), ("user_time", ctypes.c_uint64), ("system_time", ctypes.c_uint64), ("pkg_idle_wkups", ctypes.c_uint64), ("interrupt_wkups", ctypes.c_uint64), ("pageins", ctypes.c_uint64), ("wired_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64), ("phys_footprint", ctypes.c_uint64), ("proc_start_abstime", ctypes.c_uint64), ("proc_exit_abstime", ctypes.c_uint64), ("child_user_time", ctypes.c_uint64), ("child_system_time", ctypes.c_uint64), ("child_pkg_idle_wkups", ctypes.c_uint64), ("child_interrupt_wkups", ctypes.c_uint64), ("child_pageins", ctypes.c_uint64), ("child_elapsed_abstime", ctypes.c_uint64), ("diskio_bytesread", ctypes.c_uint64), ("diskio_byteswritten", ctypes.c_uint64)]


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
    policy = {"method": "libproc proc_listallpids + proc_pidpath", "forbidden_executable_basenames": list(FORBIDDEN_EXECUTABLE_BASENAMES), "self_pid_excluded": True}
    return {"policy": policy, "policy_sha256": canonical_sha(policy), "observed_paths": observed, "unobservable_pids": unobservable, "matches": matches, "match_count": len(matches), "captured_unix_seconds": time.time()}


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
assert sha256(SINGULAR) == SINGULAR_SHA and sha256(GTIMEOUT) == GTIMEOUT_SHA
assert sha256(PRODUCER_MANIFEST) == PRODUCER_MANIFEST_SHA
assert sha256(REFEREE_MANIFEST) == REFEREE_MANIFEST_SHA
assert sha256(PRIOR_TERMINAL_MANIFEST) == PRIOR_TERMINAL_MANIFEST_SHA
assert sha256(MODULAR_HELD_MANIFEST) == MODULAR_HELD_MANIFEST_SHA
assert sha256(MODULAR_REFEREE_MANIFEST) == MODULAR_REFEREE_MANIFEST_SHA
for stale in ("ATTEMPT.json", "result.json", "result.json.tmp", "stdout.log", "stderr.log", "watchdog.json", "RUN_EXCLUSIVE.lock"):
    assert not (HERE / stale).exists(), f"single-use terminal refusal: stale {stale} exists"
assert not any(HERE.glob("*.tmp"))
manifest = HERE / "MANIFEST.sha256"
acceptance_path = HERE / "independent_referee_acceptance.json"
clearance_path = HERE / "launch_clearance.json"
dependency_path = HERE / "future_modular_unit_dependency.json"
assert manifest.is_file() and acceptance_path.is_file() and clearance_path.is_file() and dependency_path.is_file(), "HELD: future modular UNIT seal, independent acceptance, and fresh explicit clearance required"
manifest_sha = sha256(manifest)
runner_sha = sha256(Path(__file__))
dependency = verify_dependency(dependency_path)
acceptance = json.loads(acceptance_path.read_text())
assert acceptance == {
    "schema": "KRENN_X5_REP5_K2_T1_TORUS_SMALLEST_SAME_CHART_EXACT_Q_INDEPENDENT_ACCEPTANCE_V1", "status": "PASS_APPROVE_ONE_TORUS_SMALLEST_EXACT_Q_ONLY_AFTER_INDEPENDENT_MODULAR_UNIT",
    "held_manifest_sha256": manifest_sha, "future_dependency_sha256": sha256(dependency_path), "source_sha256": SOURCE_SHA, "runner_sha256": runner_sha,
    "producer_manifest_sha256": PRODUCER_MANIFEST_SHA, "referee_manifest_sha256": REFEREE_MANIFEST_SHA, "prior_consumed_terminal_manifest_sha256": PRIOR_TERMINAL_MANIFEST_SHA,
    "modular_held_manifest_sha256": MODULAR_HELD_MANIFEST_SHA, "modular_referee_manifest_sha256": MODULAR_REFEREE_MANIFEST_SHA,
    "assignment": ASSIGNMENT, "variables": 73, "generators": 6561, "maximum_lane_count": 1,
    "exact_Q_authorized": True, "other_chart_authorized": False, "automatic_relaunch_authorized": False,
}
clearance = json.loads(clearance_path.read_text())
assert set(clearance) == {"schema", "status", "held_manifest_sha256", "independent_referee_acceptance_sha256", "future_dependency_sha256", "source_sha256", "runner_sha256", "singular_sha256", "gtimeout_sha256", "nonce", "issued_at_utc", "expires_at_utc", "maximum_lane_count", "native_wall_seconds", "wrapper_wall_seconds", "rss_cap_bytes", "no_overlap_confirmed", "manager_clearance_confirmed", "resource_clearance_confirmed", "census_policy_sha256", "expected_census_match_count", "exact_Q_authorized", "other_chart_authorized", "automatic_relaunch_authorized"}
assert clearance["schema"] == "KRENN_X5_REP5_K2_T1_TORUS_SMALLEST_SAME_CHART_EXACT_Q_EXPLICIT_CLEARANCE_V1"
assert clearance["status"] == "CLEARED_ONE_TORUS_SMALLEST_EXACT_Q_ONLY"
assert clearance["held_manifest_sha256"] == manifest_sha and clearance["independent_referee_acceptance_sha256"] == sha256(acceptance_path)
assert clearance["future_dependency_sha256"] == sha256(dependency_path) == dependency["binding_sha256"]
assert clearance["source_sha256"] == SOURCE_SHA and clearance["runner_sha256"] == runner_sha
assert clearance["singular_sha256"] == SINGULAR_SHA and clearance["gtimeout_sha256"] == GTIMEOUT_SHA
assert re.fullmatch(r"[0-9a-f]{32}", clearance["nonce"])
issued, expires, now = parse_utc(clearance["issued_at_utc"]), parse_utc(clearance["expires_at_utc"]), datetime.now(timezone.utc)
assert issued <= now < expires and 0 < (expires - issued).total_seconds() <= MAX_CLEARANCE_LIFETIME_SECONDS
assert clearance["maximum_lane_count"] == 1 and clearance["native_wall_seconds"] == NATIVE_WALL and clearance["wrapper_wall_seconds"] == WRAPPER_WALL and clearance["rss_cap_bytes"] == RSS_CAP
assert clearance["no_overlap_confirmed"] is clearance["manager_clearance_confirmed"] is clearance["resource_clearance_confirmed"] is True
assert clearance["expected_census_match_count"] == 0
assert clearance["exact_Q_authorized"] is True and clearance["other_chart_authorized"] is clearance["automatic_relaunch_authorized"] is False
census = fresh_process_census()
assert clearance["census_policy_sha256"] == census["policy_sha256"] and census["match_count"] == 0, census["matches"]
exclusive_json(HERE / "RUN_EXCLUSIVE.lock", {"nonce": clearance["nonce"], "manifest_sha256": manifest_sha, "runner_sha256": runner_sha})
exclusive_json(HERE / "ATTEMPT.json", {"schema": "KRENN_X5_REP5_K2_T1_TORUS_SMALLEST_SAME_CHART_EXACT_Q_ATTEMPT_V1", "status": "ATTEMPT_CONSUMED", "nonce": clearance["nonce"], "manifest_sha256": manifest_sha, "acceptance_sha256": sha256(acceptance_path), "clearance_sha256": sha256(clearance_path), "future_dependency_sha256": sha256(dependency_path), "source_sha256": SOURCE_SHA, "runner_sha256": runner_sha, "prelaunch_census": census, "relaunch_forbidden_even_if_no_result": True})

command = [str(GTIMEOUT), "--signal=TERM", f"--kill-after={KILL_AFTER}s", f"{WRAPPER_WALL}s", str(SINGULAR), str(SOURCE)]
started = time.monotonic()
try:
    process = subprocess.Popen(command, cwd=HERE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
except BaseException as error:
    atomic_json(HERE / "result.json", {"schema": "KRENN_X5_REP5_K2_T1_TORUS_SMALLEST_SAME_CHART_EXACT_Q_RESULT_V1", "status": "FAIL_CLOSED_POPEN", "error": repr(error), "attempt_consumed": True, "mathematical_coverage": False, "automatic_relaunch": False})
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
        termination = "NATIVE_WALL_CAP_480"
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
unit = termination is None and process.returncode == 0 and all(token in stdout for token in ("INPUT_VARIABLES=73", "INPUT_GENERATORS=6561", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"))
nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
status = "UNIT_IDEAL_EXACT_Q" if unit else "NONUNIT_EXACT_Q" if nonunit else "FAIL_CLOSED_RESOURCE_GATE" if termination else "FAIL_CLOSED_PROCESS_OR_SCHEMA"
result = {"schema": "KRENN_X5_REP5_K2_T1_TORUS_SMALLEST_SAME_CHART_EXACT_Q_RESULT_V1", "status": status, "mathematical_coverage": unit, "attempt_consumed": True, "field": "Q", "assignment": ASSIGNMENT, "variables": 73, "generators": 6561, "command": command, "native_wall_cap_seconds": NATIVE_WALL, "wrapper_wall_seconds": WRAPPER_WALL, "rss_cap_bytes": RSS_CAP, "wall_seconds": wall, "peak_group_rss_bytes": peak, "peak_group_members": peak_members, "termination": termination, "returncode": process.returncode, "source_sha256": SOURCE_SHA, "runner_sha256": runner_sha, "future_dependency_sha256": sha256(dependency_path), "stdout": stdout, "stderr": stderr, "strong_transcript_required": True, "exact_Q_launched": True, "other_chart_launched": False, "prior_timeout_reused": False, "automatic_relaunch": False}
atomic_json(HERE / "result.json", result)
print(json.dumps({"event": "TERMINAL", "status": status, "wall": wall, "peak": peak}, sort_keys=True))

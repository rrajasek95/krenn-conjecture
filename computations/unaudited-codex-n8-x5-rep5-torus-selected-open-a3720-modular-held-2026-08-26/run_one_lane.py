#!/usr/bin/env python3
"""Refusal-locked one-shot p32003 runner for the rep5 open a37_20=1 chart."""
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

assert __debug__, "assertions are load-bearing"
H = Path(__file__).resolve().parent
ROOT = H.parents[1]
SOURCE = H / "rep5_torus_selected_open_a37_201_p32003.sing"
SINGULAR = Path("/usr/local/bin/Singular")
GTIMEOUT = Path("/usr/local/bin/gtimeout")
SOURCE_SHA = "0fab67ef88a8674a161814094c6b553857e685ce311c5a42419812c71a939003"
DERIVATION_SHA = "3b14df5d70220330c768bcaefbaebbd5c679367badf3237604b9c2bb6d90a75e"
PINS = {
    ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-torus-cover-smallest-modular-held-2026-08-26/MANIFEST.sha256": "21df0017be41a8ec9e4035b0902649cf9c8ed97d43c65c88a93d1db7f8bf6d72",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-torus-cover-smallest-modular-held-referee-2026-08-26/MANIFEST.sha256": "16a32d07221def48a9e8388ca1e8b716cd71dfb44c2dc0cbea0bb22ab91203ab",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26/MANIFEST.sha256": "2b220f91ffa21c28506f5112a3a3e7fe791c7e3c783c1e7a319186628743659e",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-referee-2026-08-26/MANIFEST.sha256": "20f24c8de6e7edb0818c30c11df4716e983fd5f8bf5778ee36d6d3bccf27d0ff",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-torus-selected-further-reduction-design-2026-08-26/MANIFEST.sha256": "a1be34a89dae7597ab06efe6eaba6e0e4fc12256949f667ac8124ee93c35690e",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-torus-selected-further-reduction-design-referee-2026-08-26/FINAL_MANIFEST.sha256": "d87fe6724f8d1f4bf628eb01986339c86705e55adf9b471cfeed140e725b123e",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256": "0cb2ba3080ddda143ac01e4fd9f8714876c070ee86e7e574415c22cae4cac4ff",
}
SINGULAR_SHA = "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"
GTIMEOUT_SHA = "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"
NATIVE = 240
WRAPPER = 255
RSS_CAP = 8 * 1024**3
POLL = 0.1
KILL_AFTER = 5
MAX_CLEARANCE = 600
FORBIDDEN = ("Singular", "gtimeout", "sparse_d12_dual", "sparse_d12_dual_v4_1", "sparse_d12_dual_fixed_lane", "sparse_d12_dual_portfolio_audit")


class RUsage(ctypes.Structure):
    _fields_ = [("uuid", ctypes.c_uint8 * 16), ("user_time", ctypes.c_uint64), ("system_time", ctypes.c_uint64), ("pkg_idle_wkups", ctypes.c_uint64), ("interrupt_wkups", ctypes.c_uint64), ("pageins", ctypes.c_uint64), ("wired_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64), ("phys_footprint", ctypes.c_uint64), ("proc_start_abstime", ctypes.c_uint64), ("proc_exit_abstime", ctypes.c_uint64), ("child_user_time", ctypes.c_uint64), ("child_system_time", ctypes.c_uint64), ("child_pkg_idle_wkups", ctypes.c_uint64), ("child_interrupt_wkups", ctypes.c_uint64), ("child_pageins", ctypes.c_uint64), ("child_elapsed_abstime", ctypes.c_uint64), ("diskio_bytesread", ctypes.c_uint64), ("diskio_byteswritten", ctypes.c_uint64)]


LIB = ctypes.CDLL("/usr/lib/libproc.dylib")
LIB.proc_pid_rusage.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
LIB.proc_pid_rusage.restype = ctypes.c_int
LIB.proc_listpgrppids.argtypes = [ctypes.c_uint32, ctypes.c_void_p, ctypes.c_int]
LIB.proc_listpgrppids.restype = ctypes.c_int
LIB.proc_listallpids.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB.proc_listallpids.restype = ctypes.c_int
LIB.proc_pidpath.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
LIB.proc_pidpath.restype = ctypes.c_int


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canon(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def exclusive(path: Path, value: object) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def allpids() -> list[int]:
    buffer = (ctypes.c_int * 65536)()
    count = LIB.proc_listallpids(ctypes.byref(buffer), ctypes.sizeof(buffer))
    if not 0 <= count < len(buffer):
        raise RuntimeError("all-process census failure")
    return [buffer[index] for index in range(count) if buffer[index] > 0]


def pidpath(pid: int) -> str | None:
    buffer = ctypes.create_string_buffer(4096)
    count = LIB.proc_pidpath(pid, ctypes.byref(buffer), ctypes.sizeof(buffer))
    return buffer.value[:count].decode() if count > 0 else None


def census() -> dict:
    matches = []
    observed = unobservable = 0
    for pid in allpids():
        if pid == os.getpid():
            continue
        path = pidpath(pid)
        if path is None:
            unobservable += 1
            continue
        observed += 1
        if Path(path).name in FORBIDDEN:
            matches.append({"pid": pid, "path": path})
    policy = {"method": "libproc proc_listallpids + proc_pidpath", "forbidden_executable_basenames": list(FORBIDDEN), "self_pid_excluded": True}
    return {"policy": policy, "policy_sha256": canon(policy), "observed_paths": observed, "unobservable_pids": unobservable, "matches": matches, "match_count": len(matches), "captured_unix_seconds": time.time()}


def grouppids(pgid: int) -> list[int]:
    buffer = (ctypes.c_int * 4096)()
    count = LIB.proc_listpgrppids(pgid, ctypes.byref(buffer), ctypes.sizeof(buffer))
    if not 0 <= count < len(buffer):
        raise RuntimeError("process-group census failure")
    return [buffer[index] for index in range(count) if buffer[index] > 0]


def grouprss(pgid: int) -> tuple[int, int]:
    members = grouppids(pgid)
    if not members:
        raise RuntimeError("live wrapper has no observable group members")
    total = 0
    for pid in members:
        record = RUsage()
        if LIB.proc_pid_rusage(pid, 2, ctypes.byref(record)) != 0:
            if pid in grouppids(pgid):
                raise RuntimeError(f"rusage failure for live pid {pid}")
            continue
        total += record.resident_size
    return total, len(members)


def utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert parsed.tzinfo
    return parsed.astimezone(timezone.utc)


assert sha(SOURCE) == SOURCE_SHA and sha(H / "source_derivation.json") == DERIVATION_SHA
for path, expected in PINS.items():
    assert path.is_file() and sha(path) == expected
assert sha(SINGULAR) == SINGULAR_SHA and sha(GTIMEOUT) == GTIMEOUT_SHA
for name in ("ATTEMPT.json", "result.json", "result.json.tmp", "stdout.log", "stderr.log", "watchdog.json", "RUN_EXCLUSIVE.lock"):
    assert not (H / name).exists(), f"single-use terminal refusal: stale {name}"
assert not list(H.glob("*.tmp"))
manifest = H / "MANIFEST.sha256"
acceptance = H / "independent_referee_acceptance.json"
clearance = H / "launch_clearance.json"
assert manifest.is_file() and acceptance.is_file() and clearance.is_file(), "HELD: independent acceptance and fresh explicit clearance required"
manifest_sha = sha(manifest)
runner_sha = sha(Path(__file__))
a = json.loads(acceptance.read_text())
assert a == {
    "schema": "KRENN_X5_REP5_TORUS_SELECTED_OPEN_A3720_MODULAR_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_ONE_OPEN_A3720_P32003_DIAGNOSTIC_ONLY",
    "held_manifest_sha256": manifest_sha,
    "source_derivation_sha256": DERIVATION_SHA,
    "source_sha256": SOURCE_SHA,
    "runner_sha256": runner_sha,
    "selected73_held_manifest_sha256": PINS[list(PINS)[0]],
    "selected73_referee_manifest_sha256": PINS[list(PINS)[1]],
    "torus_design_manifest_sha256": PINS[list(PINS)[2]],
    "torus_referee_manifest_sha256": PINS[list(PINS)[3]],
    "further_reduction_manifest_sha256": PINS[list(PINS)[4]],
    "further_reduction_referee_manifest_sha256": PINS[list(PINS)[5]],
    "prior_timeout_referee_manifest_sha256": PINS[list(PINS)[6]],
    "chart": {"coordinate": "a37_20", "locus": "D(a37_20)", "normalization": "a37_20=1"},
    "variables": 72,
    "generators": 6561,
    "maximum_lane_count": 1,
    "exact_Q_authorized": False,
    "closed_branch_authorized": False,
    "automatic_relaunch_authorized": False,
}
c = json.loads(clearance.read_text())
assert set(c) == {"schema", "status", "held_manifest_sha256", "independent_referee_acceptance_sha256", "source_sha256", "runner_sha256", "singular_sha256", "gtimeout_sha256", "nonce", "issued_at_utc", "expires_at_utc", "maximum_lane_count", "native_wall_seconds", "wrapper_wall_seconds", "rss_cap_bytes", "no_overlap_confirmed", "manager_clearance_confirmed", "resource_clearance_confirmed", "census_policy_sha256", "expected_census_match_count", "exact_Q_authorized", "closed_branch_authorized", "automatic_relaunch_authorized"}
assert c["schema"] == "KRENN_X5_REP5_TORUS_SELECTED_OPEN_A3720_MODULAR_CLEARANCE_V1" and c["status"] == "CLEARED_ONE_OPEN_A3720_P32003_DIAGNOSTIC_ONLY"
assert c["held_manifest_sha256"] == manifest_sha and c["independent_referee_acceptance_sha256"] == sha(acceptance)
assert c["source_sha256"] == SOURCE_SHA and c["runner_sha256"] == runner_sha and c["singular_sha256"] == SINGULAR_SHA and c["gtimeout_sha256"] == GTIMEOUT_SHA
assert re.fullmatch(r"[0-9a-f]{32}", c["nonce"])
issued, expires, now = utc(c["issued_at_utc"]), utc(c["expires_at_utc"]), datetime.now(timezone.utc)
assert issued <= now < expires and 0 < (expires - issued).total_seconds() <= MAX_CLEARANCE
assert c["maximum_lane_count"] == 1 and c["native_wall_seconds"] == NATIVE and c["wrapper_wall_seconds"] == WRAPPER and c["rss_cap_bytes"] == RSS_CAP
assert c["no_overlap_confirmed"] is c["manager_clearance_confirmed"] is c["resource_clearance_confirmed"] is True
assert c["expected_census_match_count"] == 0 and c["exact_Q_authorized"] is c["closed_branch_authorized"] is c["automatic_relaunch_authorized"] is False
pre = census()
assert c["census_policy_sha256"] == pre["policy_sha256"] and pre["match_count"] == 0, pre["matches"]
exclusive(H / "RUN_EXCLUSIVE.lock", {"nonce": c["nonce"], "manifest_sha256": manifest_sha, "runner_sha256": runner_sha})
exclusive(H / "ATTEMPT.json", {"schema": "KRENN_X5_REP5_TORUS_SELECTED_OPEN_A3720_MODULAR_ATTEMPT_V1", "status": "ATTEMPT_CONSUMED", "nonce": c["nonce"], "manifest_sha256": manifest_sha, "acceptance_sha256": sha(acceptance), "clearance_sha256": sha(clearance), "source_sha256": SOURCE_SHA, "runner_sha256": runner_sha, "prelaunch_census": pre, "relaunch_forbidden_even_if_no_result": True})
command = [str(GTIMEOUT), "--signal=TERM", f"--kill-after={KILL_AFTER}s", f"{WRAPPER}s", str(SINGULAR), str(SOURCE)]
started = time.monotonic()
try:
    process = subprocess.Popen(command, cwd=H, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
except BaseException as error:
    atomic(H / "result.json", {"schema": "KRENN_X5_REP5_TORUS_SELECTED_OPEN_A3720_MODULAR_RESULT_V1", "status": "FAIL_CLOSED_POPEN", "error": repr(error), "attempt_consumed": True, "diagnostic_only": True, "mathematical_coverage": False, "automatic_relaunch": False})
    raise
print(json.dumps({"event": "STARTED", "wrapper_pid": process.pid, "nonce": c["nonce"]}), flush=True)
peak = members = 0
termination = None
while process.poll() is None:
    try:
        current, count = grouprss(process.pid)
    except RuntimeError as error:
        termination = "RESOURCE_OBSERVER_FAILURE:" + str(error)
        current, count = peak, members
    if current > peak:
        peak, members = current, count
    elapsed = time.monotonic() - started
    if termination is None and peak > RSS_CAP:
        termination = "RSS_CAP_8GIB"
    elif termination is None and elapsed > NATIVE:
        termination = "NATIVE_WALL_CAP_240"
    if termination:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        deadline = time.monotonic() + KILL_AFTER
        while process.poll() is None and time.monotonic() < deadline:
            time.sleep(POLL)
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        break
    time.sleep(POLL)
stdout, stderr = process.communicate()
wall = time.monotonic() - started
unit = termination is None and process.returncode == 0 and all(token in stdout for token in ("INPUT_VARIABLES=72", "INPUT_GENERATORS=6561", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"))
nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
status = "UNIT_IDEAL_MODULAR_DIAGNOSTIC" if unit else "NONUNIT_MODULAR_DIAGNOSTIC" if nonunit else "FAIL_CLOSED_RESOURCE_GATE" if termination else "FAIL_CLOSED_PROCESS_OR_SCHEMA"
result = {"schema": "KRENN_X5_REP5_TORUS_SELECTED_OPEN_A3720_MODULAR_RESULT_V1", "status": status, "diagnostic_only": True, "mathematical_coverage": False, "attempt_consumed": True, "field": "F_32003", "chart": {"coordinate": "a37_20", "locus": "D(a37_20)", "normalization": "a37_20=1"}, "variables": 72, "generators": 6561, "command": command, "native_wall_cap_seconds": NATIVE, "wrapper_wall_seconds": WRAPPER, "rss_cap_bytes": RSS_CAP, "wall_seconds": wall, "peak_group_rss_bytes": peak, "peak_group_members": members, "termination": termination, "returncode": process.returncode, "source_sha256": SOURCE_SHA, "runner_sha256": runner_sha, "stdout": stdout, "stderr": stderr, "exact_Q_launched": False, "closed_branch_launched": False, "prior_timeout_reused": False, "automatic_relaunch": False}
atomic(H / "result.json", result)
print(json.dumps({"event": "TERMINAL", "status": status, "wall": wall, "peak": peak}, sort_keys=True))

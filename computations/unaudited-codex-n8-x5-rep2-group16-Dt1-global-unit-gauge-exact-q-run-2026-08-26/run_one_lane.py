#!/usr/bin/env python3
"""Single-use direct-libproc runner for the rep2 D(t1) 61-variable slice."""
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
SOURCE = HERE / "rep2_group16_Dt1_global_unit_gauge_runtime_Q.sing"
PLAN = HERE / "PLAN.json"
INPUT_MANIFEST = HERE / "RUNNER_INPUT_MANIFEST.sha256"
ACCEPTANCE = HERE / "independent_referee_acceptance.json"
CLEARANCE = HERE / "launch_clearance.json"
SINGULAR = Path("/usr/local/bin/Singular")
GTIMEOUT = Path("/usr/local/bin/gtimeout")
SOURCE_SHA = "686ceb9529ba9487fe093845c770c237371c8866a54be5aeba6629f7ba640537"
PLAN_SHA = "3c0c50362205ad7ba13a9729460bf100a0f429b313684d14f488ec8551e701ea"
HELD_PLAN = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-referee-2026-08-26/HELD_PLAN.json"
HELD_PLAN_SHA = "a9a9ea0f5c53b3914ff58be17824c58c4e44fab1cab87c25e9107c5eaf1d0a49"
REF_RESULT = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-referee-2026-08-26/results_referee.json"
REF_RESULT_SHA = "5a2d4b1ce4639a139c7bc5886de60dcac5ffcdbccb170ebe1426bec97e879326"
REF_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-referee-2026-08-26/FINAL_MANIFEST.sha256"
REF_MANIFEST_SHA = "b98c1d04e4327731f272a8e885fff5480816243fead3051d44b4ae8e36dc84ff"
SINGULAR_SHA = "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"
GTIMEOUT_SHA = "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"
NATIVE_WALL = 480
WRAPPER_WALL = 510
RSS_CAP = 8 * 1024**3
POLL_SECONDS = 0.1
KILL_AFTER = 5
FORBIDDEN = ("Singular", "gtimeout", "sparse_d12_dual", "sparse_d12_dual_v4_1", "sparse_d12_dual_fixed_lane", "sparse_d12_dual_portfolio_audit")


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


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, value) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def exclusive_json(path: Path, value) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def all_pids() -> list[int]:
    buffer = (ctypes.c_int * 65536)()
    count = LIBPROC.proc_listallpids(ctypes.byref(buffer), ctypes.sizeof(buffer))
    assert 0 <= count < len(buffer)
    return [buffer[index] for index in range(count) if buffer[index] > 0]


def pid_path(pid: int) -> str | None:
    buffer = ctypes.create_string_buffer(4096)
    length = LIBPROC.proc_pidpath(pid, ctypes.byref(buffer), ctypes.sizeof(buffer))
    return buffer.value[:length].decode("utf-8", "strict") if length > 0 else None


def process_census() -> dict:
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
        if Path(path).name in FORBIDDEN:
            matches.append({"pid": pid, "path": path})
    return {"method": "libproc", "observed": observed, "unobservable": unobservable, "matches": matches, "match_count": len(matches)}


def group_pids(pgid: int) -> list[int]:
    buffer = (ctypes.c_int * 4096)()
    count = LIBPROC.proc_listpgrppids(pgid, ctypes.byref(buffer), ctypes.sizeof(buffer))
    if not 0 <= count < len(buffer):
        raise RuntimeError("process-group census failure")
    return [buffer[index] for index in range(count) if buffer[index] > 0]


def group_rss(pgid: int, wrapper_alive: bool) -> tuple[int, int]:
    members = group_pids(pgid)
    if wrapper_alive and not members:
        raise RuntimeError("live wrapper has no observable group members")
    total = 0
    for pid in members:
        record = RUsageInfoV2()
        if LIBPROC.proc_pid_rusage(pid, 2, ctypes.byref(record)) != 0:
            if pid in group_pids(pgid):
                raise RuntimeError(f"rusage failed for live pid {pid}")
            continue
        total += record.resident_size
    return total, len(members)


assert sha(SOURCE) == SOURCE_SHA
assert sha(PLAN) == PLAN_SHA
assert sha(HELD_PLAN) == HELD_PLAN_SHA and sha(REF_RESULT) == REF_RESULT_SHA and sha(REF_MANIFEST) == REF_MANIFEST_SHA
assert sha(SINGULAR) == SINGULAR_SHA and sha(GTIMEOUT) == GTIMEOUT_SHA
for stale in ("ATTEMPT.json", "result.json", "result.json.tmp", "RUN_EXCLUSIVE.lock", "TERMINAL_MANIFEST.sha256"):
    assert not (HERE / stale).exists(), f"single-use refusal: {stale}"
assert not any(HERE.glob("*.tmp"))
assert INPUT_MANIFEST.is_file() and ACCEPTANCE.is_file() and CLEARANCE.is_file()
runner_sha = sha(Path(__file__))
input_manifest_sha = sha(INPUT_MANIFEST)
acceptance = json.loads(ACCEPTANCE.read_text())
assert acceptance == {
    "schema": "KRENN_X5_REP2_GROUP16_DT1_GLOBAL_UNIT_GAUGE_EXACT_Q_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_ONE_LANE",
    "input_manifest_sha256": input_manifest_sha,
    "source_sha256": SOURCE_SHA,
    "runner_sha256": runner_sha,
    "held_plan_sha256": HELD_PLAN_SHA,
    "referee_result_sha256": REF_RESULT_SHA,
    "referee_manifest_sha256": REF_MANIFEST_SHA,
    "variables": 61,
    "generators": 6568,
    "maximum_lane_count": 1,
    "other_chart_authorized": False,
    "automatic_relaunch_authorized": False,
}
clearance = json.loads(CLEARANCE.read_text())
assert clearance["schema"] == "KRENN_X5_REP2_GROUP16_DT1_GLOBAL_UNIT_GAUGE_EXACT_Q_CLEARANCE_V1"
assert clearance["status"] == "CLEARED_ONE_LANE_ONLY"
assert clearance["input_manifest_sha256"] == input_manifest_sha
assert clearance["acceptance_sha256"] == sha(ACCEPTANCE)
assert clearance["source_sha256"] == SOURCE_SHA and clearance["runner_sha256"] == runner_sha
assert clearance["native_wall_seconds"] == NATIVE_WALL and clearance["wrapper_wall_seconds"] == WRAPPER_WALL and clearance["rss_cap_bytes"] == RSS_CAP
assert clearance["maximum_lane_count"] == 1
assert clearance["manager_clearance_confirmed"] is clearance["resource_clearance_confirmed"] is clearance["no_overlap_confirmed"] is True
assert clearance["other_chart_authorized"] is clearance["automatic_relaunch_authorized"] is False
assert re.fullmatch(r"[0-9a-f]{32}", clearance["nonce"])
issued = datetime.fromisoformat(clearance["issued_at_utc"].replace("Z", "+00:00"))
expires = datetime.fromisoformat(clearance["expires_at_utc"].replace("Z", "+00:00"))
now = datetime.now(timezone.utc)
assert issued <= now < expires and 0 < (expires - issued).total_seconds() <= 900
census = process_census()
assert census["match_count"] == 0, census["matches"]

exclusive_json(HERE / "RUN_EXCLUSIVE.lock", {"nonce": clearance["nonce"], "runner_sha256": runner_sha, "input_manifest_sha256": input_manifest_sha})
exclusive_json(HERE / "ATTEMPT.json", {"schema": "KRENN_X5_REP2_GROUP16_DT1_GLOBAL_UNIT_GAUGE_EXACT_Q_ATTEMPT_V1", "status": "ATTEMPT_CONSUMED", "nonce": clearance["nonce"], "source_sha256": SOURCE_SHA, "runner_sha256": runner_sha, "acceptance_sha256": sha(ACCEPTANCE), "clearance_sha256": sha(CLEARANCE), "prelaunch_census": census, "automatic_relaunch": False})

command = [str(GTIMEOUT), "--signal=TERM", f"--kill-after={KILL_AFTER}s", f"{WRAPPER_WALL}s", str(SINGULAR), str(SOURCE)]
started = time.monotonic()
process = subprocess.Popen(command, cwd=HERE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
print(json.dumps({"event": "STARTED", "wrapper_pid": process.pid}), flush=True)
peak = 0
peak_members = 0
termination = None
while process.poll() is None:
    try:
        current, members = group_rss(process.pid, True)
    except RuntimeError as error:
        termination = "RESOURCE_OBSERVER_FAILURE:" + str(error)
        current, members = peak, peak_members
    if current > peak:
        peak, peak_members = current, members
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
required = ("INPUT_VARIABLES=61", "INPUT_GENERATORS=6568", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL")
unit = termination is None and process.returncode == 0 and all(token in stdout for token in required)
nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNCERTIFIED" in stdout
status = "UNIT_IDEAL_EXACT_Q" if unit else "NONUNIT_EXACT_Q" if nonunit else "FAIL_CLOSED_RESOURCE_GATE" if termination else "FAIL_CLOSED_PROCESS_OR_SCHEMA"
result = {"schema": "KRENN_X5_REP2_GROUP16_DT1_GLOBAL_UNIT_GAUGE_EXACT_Q_RESULT_V1", "status": status, "mathematical_coverage": unit, "attempt_consumed": True, "field": "Q", "variables": 61, "generators": 6568, "command": command, "native_wall_cap_seconds": NATIVE_WALL, "wrapper_wall_seconds": WRAPPER_WALL, "rss_cap_bytes": RSS_CAP, "wall_seconds": wall, "peak_group_rss_bytes": peak, "peak_group_members": peak_members, "termination": termination, "returncode": process.returncode, "source_sha256": SOURCE_SHA, "runner_sha256": runner_sha, "stdout": stdout, "stderr": stderr, "strong_transcript_required": True, "other_chart_launched": False, "automatic_relaunch": False}
atomic_json(HERE / "result.json", result)
print(json.dumps({"event": "TERMINAL", "status": status, "wall": wall, "peak": peak}, sort_keys=True), flush=True)

#!/usr/bin/env python3
"""Single-use strict exact-Q executor for the three complementary t-strata."""
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
LEDGER = HERE / "source_ledger.json"
SINGULAR = Path("/usr/local/bin/Singular")
GTIMEOUT = Path("/usr/local/bin/gtimeout")
SINGULAR_SHA = "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"
GTIMEOUT_SHA = "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"
NATIVE_WALL = 480
WRAPPER_WALL = 510
RSS_CAP = 8 * 1024**3
POLL = 0.1
KILL_AFTER = 5


class RUsage(ctypes.Structure):
    _fields_ = [
        ("uuid", ctypes.c_uint8 * 16), ("user_time", ctypes.c_uint64), ("system_time", ctypes.c_uint64),
        ("pkg_idle_wkups", ctypes.c_uint64), ("interrupt_wkups", ctypes.c_uint64), ("pageins", ctypes.c_uint64),
        ("wired_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64), ("phys_footprint", ctypes.c_uint64),
        ("proc_start_abstime", ctypes.c_uint64), ("proc_exit_abstime", ctypes.c_uint64),
        ("child_user_time", ctypes.c_uint64), ("child_system_time", ctypes.c_uint64),
        ("child_pkg_idle_wkups", ctypes.c_uint64), ("child_interrupt_wkups", ctypes.c_uint64),
        ("child_pageins", ctypes.c_uint64), ("child_elapsed_abstime", ctypes.c_uint64),
        ("diskio_bytesread", ctypes.c_uint64), ("diskio_byteswritten", ctypes.c_uint64),
    ]


LIB = ctypes.CDLL("/usr/lib/libproc.dylib")
LIB.proc_pid_rusage.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
LIB.proc_pid_rusage.restype = ctypes.c_int
LIB.proc_listpgrppids.argtypes = [ctypes.c_uint32, ctypes.c_void_p, ctypes.c_int]
LIB.proc_listpgrppids.restype = ctypes.c_int


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path, value):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def exclusive(path, value):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def members(pgid):
    buffer = (ctypes.c_int * 4096)()
    count = LIB.proc_listpgrppids(pgid, ctypes.byref(buffer), ctypes.sizeof(buffer))
    if not 0 <= count < len(buffer):
        raise RuntimeError("process-group census failure")
    return [buffer[index] for index in range(count) if buffer[index] > 0]


def group_rss(pgid, alive):
    pids = members(pgid)
    if alive and not pids:
        raise RuntimeError("live wrapper has no observable process-group member")
    total = 0
    for pid in pids:
        record = RUsage()
        if LIB.proc_pid_rusage(pid, 2, ctypes.byref(record)) != 0:
            if pid in members(pgid):
                raise RuntimeError(f"rusage failure for live member {pid}")
            continue
        total += record.resident_size
    return total, len(pids)


def terminate(process):
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.monotonic() + KILL_AFTER
    while process.poll() is None and time.monotonic() < deadline:
        time.sleep(POLL)
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


ledger = json.loads(LEDGER.read_text())
lanes = ledger["lanes"]
assert [lane["ordinal"] for lane in lanes] == [1, 2, 3]
assert [lane["variables"] for lane in lanes] == [63, 64, 64]
assert all(lane["generators"] == 6569 for lane in lanes)
for lane in lanes:
    source = HERE / lane["source_path"]
    assert source.is_file() and sha(source) == lane["source_sha256"] and source.stat().st_size == lane["source_bytes"]
assert sha(SINGULAR) == SINGULAR_SHA and sha(GTIMEOUT) == GTIMEOUT_SHA
for stale in ("BATCH_ATTEMPT.json", "batch_result.json", "results"):
    assert not (HERE / stale).exists(), f"single-use refusal: {stale} exists"
manifest = HERE / "MANIFEST.sha256"
acceptance_path = HERE / "independent_referee_acceptance.json"
clearance_path = HERE / "launch_clearance.json"
assert manifest.is_file() and acceptance_path.is_file() and clearance_path.is_file(), "HELD: acceptance and fresh clearance required"
acceptance = json.loads(acceptance_path.read_text())
runner_sha = sha(Path(__file__))
assert acceptance == {
    "schema": "KRENN_X5_REP2_GROUP16_TCOVER_COMPLEMENT3_EXACT_Q_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_THREE_COMPLEMENTARY_T_CHARTS_ONLY",
    "held_manifest_sha256": sha(manifest),
    "source_ledger_sha256": sha(LEDGER),
    "runner_sha256": runner_sha,
    "source_sha256": [lane["source_sha256"] for lane in lanes],
    "maximum_lane_count": 3,
    "exact_Q_authorized": True,
    "other_chart_authorized": False,
    "automatic_relaunch_authorized": False,
}
clearance = json.loads(clearance_path.read_text())
assert clearance == {
    "schema": "KRENN_X5_REP2_GROUP16_TCOVER_COMPLEMENT3_EXACT_Q_CLEARANCE_V1",
    "status": "CLEARED_THREE_COMPLEMENTARY_T_CHARTS_ONLY",
    "held_manifest_sha256": sha(manifest),
    "acceptance_sha256": sha(acceptance_path),
    "source_ledger_sha256": sha(LEDGER),
    "runner_sha256": runner_sha,
    "singular_sha256": SINGULAR_SHA,
    "gtimeout_sha256": GTIMEOUT_SHA,
    "native_wall_seconds_each": NATIVE_WALL,
    "wrapper_wall_seconds_each": WRAPPER_WALL,
    "rss_cap_bytes_each": RSS_CAP,
    "no_overlap_confirmed": True,
    "maximum_lane_count": 3,
    "exact_Q_authorized": True,
    "other_chart_authorized": False,
    "automatic_relaunch_authorized": False,
}
ps = subprocess.run(["ps", "-axo", "pid=,command="], text=True, capture_output=True, check=True).stdout.splitlines()
heavy = [line for line in ps if "/usr/local/bin/Singular" in line or "libSingular" in line]
assert not heavy, ("overlap", heavy)
exclusive(HERE / "BATCH_ATTEMPT.json", {"status": "CONSUMED_SINGLE_USE", "manifest_sha256": sha(manifest), "acceptance_sha256": sha(acceptance_path), "clearance_sha256": sha(clearance_path)})
(HERE / "results").mkdir()
completed = []
stop = None
for lane in lanes:
    source = HERE / lane["source_path"]
    started = time.monotonic()
    termination = None
    peak = peak_members = 0
    command = [str(GTIMEOUT), "--signal=TERM", f"--kill-after={KILL_AFTER}s", f"{WRAPPER_WALL}s", str(SINGULAR), str(source)]
    process = subprocess.Popen(command, cwd=HERE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    while process.poll() is None:
        try:
            rss, count = group_rss(process.pid, True)
        except RuntimeError as error:
            termination = "RESOURCE_OBSERVER_FAILURE:" + str(error)
            rss, count = peak, peak_members
        if rss > peak:
            peak, peak_members = rss, count
        if termination is None and peak > RSS_CAP:
            termination = "RSS_CAP_8GIB"
        elif termination is None and time.monotonic() - started > NATIVE_WALL:
            termination = "NATIVE_WALL_CAP_480"
        if termination:
            terminate(process)
            break
        time.sleep(POLL)
    stdout, stderr = process.communicate()
    wall = time.monotonic() - started
    required = {f"INPUT_VARIABLES={lane['variables']}", "INPUT_GENERATORS=6569", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"}
    unit = termination is None and process.returncode == 0 and required <= set(stdout.splitlines())
    nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout.splitlines()
    status = "UNIT_IDEAL_EXACT_Q" if unit else "NONUNIT_EXACT_Q" if nonunit else "FAIL_CLOSED_RESOURCE" if termination else "FAIL_CLOSED_PROCESS_OR_SCHEMA"
    record = {"schema": "KRENN_X5_REP2_GROUP16_TCOVER_COMPLEMENT3_LANE_RESULT_V1", "status": status, "ordinal": lane["ordinal"], "name": lane["name"], "logical_stratum": lane["logical_stratum"], "variables": lane["variables"], "generators": lane["generators"], "source_sha256": lane["source_sha256"], "wall_seconds": wall, "peak_group_rss_bytes": peak, "peak_group_members": peak_members, "termination": termination, "returncode": process.returncode, "stdout": stdout, "stderr": stderr, "automatic_relaunch": False}
    result_path = HERE / "results" / f"lane{lane['ordinal']}_{lane['name']}.json"
    atomic(result_path, record)
    completed.append({"ordinal": lane["ordinal"], "name": lane["name"], "status": status, "result_sha256": sha(result_path)})
    if not unit:
        stop = {"ordinal": lane["ordinal"], "name": lane["name"], "status": status}
        break
batch = {"schema": "KRENN_X5_REP2_GROUP16_TCOVER_COMPLEMENT3_BATCH_RESULT_V1", "status": "PASS_ALL_THREE_UNIT" if stop is None else "STOPPED_FAIL_CLOSED", "completed": completed, "stop": stop, "skipped_after_stop": [lane["name"] for lane in lanes[len(completed):]], "strict_order": [lane["name"] for lane in lanes], "parallel": False, "relaunch": False}
atomic(HERE / "batch_result.json", batch)
print(json.dumps({"event": "TERMINAL", "status": batch["status"], "completed": len(completed)}, sort_keys=True))

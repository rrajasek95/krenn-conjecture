#!/usr/bin/env python3
"""Refusal-locked strict sequential executor for the sealed rep2 first-25 ledger."""
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
LEDGER_SHA = "20737fd8197335f98214222bc5caa4c3d8c1ba2b2fcc283065d865befcf6389e"
SINGULAR_SHA = "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"
GTIMEOUT_SHA = "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"
CLOSED_MANIFEST_SHA = "c9298394d37022b384e8117280bfcdc39422ca24f57173da699a39dac11fb62a"
CLOSED_SECOND_REFEREE_SHA = "c856fae641e355a94684c1c9304ead831d213ecc90f579c0a751c93002c10562"
NATIVE_WALL = 240
WRAPPER_WALL = 250
RSS_CAP = 8 * 1024**3
POLL = 0.1
KILL_AFTER = 5
SELECTED = tuple(range(1, 26))


class RUsageInfoV2(ctypes.Structure):
    _fields_ = [("uuid", ctypes.c_uint8 * 16), ("user_time", ctypes.c_uint64), ("system_time", ctypes.c_uint64), ("pkg_idle_wkups", ctypes.c_uint64), ("interrupt_wkups", ctypes.c_uint64), ("pageins", ctypes.c_uint64), ("wired_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64), ("phys_footprint", ctypes.c_uint64), ("proc_start_abstime", ctypes.c_uint64), ("proc_exit_abstime", ctypes.c_uint64), ("child_user_time", ctypes.c_uint64), ("child_system_time", ctypes.c_uint64), ("child_pkg_idle_wkups", ctypes.c_uint64), ("child_interrupt_wkups", ctypes.c_uint64), ("child_pageins", ctypes.c_uint64), ("child_elapsed_abstime", ctypes.c_uint64), ("diskio_bytesread", ctypes.c_uint64), ("diskio_byteswritten", ctypes.c_uint64)]


LIBPROC = ctypes.CDLL("/usr/lib/libproc.dylib")
LIBPROC.proc_pid_rusage.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
LIBPROC.proc_pid_rusage.restype = ctypes.c_int
LIBPROC.proc_listpgrppids.argtypes = [ctypes.c_uint32, ctypes.c_void_p, ctypes.c_int]
LIBPROC.proc_listpgrppids.restype = ctypes.c_int


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def exclusive(path: Path, value: object) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def members(pgid: int) -> list[int]:
    buffer = (ctypes.c_int * 4096)()
    count = LIBPROC.proc_listpgrppids(pgid, ctypes.byref(buffer), ctypes.sizeof(buffer))
    if not 0 <= count < len(buffer):
        raise RuntimeError("process-group census failure")
    return [buffer[index] for index in range(count) if buffer[index] > 0]


def group_rss(pgid: int, alive: bool) -> tuple[int, int]:
    pids = members(pgid)
    if alive and not pids:
        raise RuntimeError("live wrapper has no observable group members")
    total = 0
    for pid in pids:
        record = RUsageInfoV2()
        if LIBPROC.proc_pid_rusage(pid, 2, ctypes.byref(record)) != 0:
            if pid in members(pgid):
                raise RuntimeError(f"rusage failure for live member {pid}")
            continue
        total += record.resident_size
    return total, len(pids)


def terminate(process: subprocess.Popen) -> None:
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


assert sha256(LEDGER) == LEDGER_SHA
assert sha256(SINGULAR) == SINGULAR_SHA and sha256(GTIMEOUT) == GTIMEOUT_SHA
ledger = json.loads(LEDGER.read_text())
lanes = ledger["lanes"]
assert ledger["closed_dependency"]["group_id"] == 0
assert ledger["closed_dependency"]["first_seal_manifest_sha256"] == CLOSED_MANIFEST_SHA
assert ledger["closed_dependency"]["second_referee_manifest_sha256"] == CLOSED_SECOND_REFEREE_SHA
assert [lane["group_id"] for lane in lanes] == list(SELECTED)
assert [lane["ordinal"] for lane in lanes] == list(range(1, 26))
for lane in lanes:
    source = HERE / lane["source_path"]
    assert sha256(source) == lane["source_sha256"] and source.stat().st_size == lane["source_bytes"]
for stale in ("BATCH_ATTEMPT.json", "batch_result.json", "batch_result.json.tmp", "results"):
    assert not (HERE / stale).exists(), f"no relaunch/partial reuse: {stale} exists"
assert not any(HERE.glob("*.tmp"))
manifest = HERE / "MANIFEST.sha256"
acceptance = HERE / "independent_referee_acceptance.json"
clearance = HERE / "launch_clearance.json"
assert manifest.is_file() and acceptance.is_file() and clearance.is_file(), "HELD: independent acceptance and fresh explicit batch clearance required"
accept = json.loads(acceptance.read_text())
clear = json.loads(clearance.read_text())
runner_sha = sha256(Path(__file__))
assert accept == {
    "schema": "KRENN_X5_REP2_FIRST25_EXACT_Q_INDEPENDENT_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_STRICT_REP2_FIRST25_BATCH_ONLY",
    "held_manifest_sha256": sha256(manifest),
    "source_ledger_sha256": LEDGER_SHA,
    "runner_sha256": runner_sha,
    "already_closed_group_id": 0,
    "closed_manifest_sha256": CLOSED_MANIFEST_SHA,
    "closed_second_referee_manifest_sha256": CLOSED_SECOND_REFEREE_SHA,
    "selected_group_ids": list(SELECTED),
    "maximum_lane_count": 25,
    "exact_Q_authorized": True,
    "parallel_authorized": False,
    "skip_reorder_relaunch_authorized": False,
}
assert clear == {
    "schema": "KRENN_X5_REP2_FIRST25_EXACT_Q_EXPLICIT_CLEARANCE_V1",
    "status": "CLEARED_STRICT_REP2_FIRST25_BATCH_ONLY",
    "held_manifest_sha256": sha256(manifest),
    "independent_referee_acceptance_sha256": sha256(acceptance),
    "source_ledger_sha256": LEDGER_SHA,
    "runner_sha256": runner_sha,
    "singular_sha256": SINGULAR_SHA,
    "gtimeout_sha256": GTIMEOUT_SHA,
    "already_closed_group_id": 0,
    "closed_manifest_sha256": CLOSED_MANIFEST_SHA,
    "closed_second_referee_manifest_sha256": CLOSED_SECOND_REFEREE_SHA,
    "selected_group_ids": list(SELECTED),
    "native_wall_seconds_each": NATIVE_WALL,
    "wrapper_wall_seconds_each": WRAPPER_WALL,
    "rss_cap_bytes_each": RSS_CAP,
    "no_overlap_confirmed": True,
    "maximum_lane_count": 25,
    "parallel_authorized": False,
    "skip_reorder_relaunch_authorized": False,
}
exclusive(HERE / "BATCH_ATTEMPT.json", {"schema": "KRENN_X5_REP2_FIRST25_BATCH_ATTEMPT_V1", "status": "CONSUMED_SINGLE_USE", "group_ids": list(SELECTED), "manifest_sha256": sha256(manifest), "acceptance_sha256": sha256(acceptance), "clearance_sha256": sha256(clearance)})
(HERE / "results").mkdir()
batch = []
stop = None
for lane in lanes:
    group_id = lane["group_id"]
    source = HERE / lane["source_path"]
    started = time.monotonic()
    termination = None
    peak = 0
    peak_members = 0
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
        elapsed = time.monotonic() - started
        if termination is None and peak > RSS_CAP:
            termination = "RSS_CAP_8GIB"
        elif termination is None and elapsed > NATIVE_WALL:
            termination = "NATIVE_WALL_CAP_240"
        if termination:
            terminate(process)
            break
        time.sleep(POLL)
    stdout, stderr = process.communicate()
    wall = time.monotonic() - started
    unit = termination is None and process.returncode == 0 and all(token in stdout for token in ("INPUT_GENERATORS=6577", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"))
    nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
    status = "UNIT_IDEAL_EXACT_Q" if unit else "NONUNIT_EXACT_Q" if nonunit else "FAIL_CLOSED_RESOURCE" if termination else "FAIL_CLOSED_PROCESS_OR_MISMATCH"
    record = {"schema": "KRENN_X5_REP2_FIRST25_LANE_RESULT_V1", "status": status, "ordinal": lane["ordinal"], "group_id": group_id, "chart": lane["canonical_chart"], "source_sha256": lane["source_sha256"], "wall_seconds": wall, "peak_group_rss_bytes": peak, "peak_group_members": peak_members, "termination": termination, "wrapper_returncode": process.returncode, "stdout": stdout, "stderr": stderr, "diagnostic_scope_one_group": True, "automatic_relaunch": False}
    result_path = HERE / "results" / f"group{group_id:03d}.json"
    atomic(result_path, record)
    batch.append({"group_id": group_id, "status": status, "result_sha256": sha256(result_path)})
    if not unit:
        stop = {"group_id": group_id, "status": status}
        break
assert [entry["group_id"] for entry in batch] == list(SELECTED[:len(batch)])
batch_result = {"schema": "KRENN_X5_REP2_FIRST25_BATCH_RESULT_V1", "status": "PASS_ALL_25_UNIT" if stop is None else "STOPPED_FAIL_CLOSED", "strict_order": list(SELECTED), "completed": batch, "stop": stop, "skipped_after_stop": list(SELECTED[len(batch):]), "parallel": False, "relaunch": False}
atomic(HERE / "batch_result.json", batch_result)
print(json.dumps({"event": "TERMINAL", "status": batch_result["status"], "completed": len(batch)}, sort_keys=True))

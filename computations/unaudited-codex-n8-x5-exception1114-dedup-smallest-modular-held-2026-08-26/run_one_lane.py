#!/usr/bin/env python3
"""Refusal-locked one-shot p32003 runner for exception1114 58/6533."""

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
    raise RuntimeError("assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "rep1114_rank1_z1_fulltorus_dedup_p32003.sing"
SINGULAR = Path("/usr/local/bin/Singular")
GTIMEOUT = Path("/usr/local/bin/gtimeout")
SOURCE_SHA = "4789b9cef4c3db41eb63819d66c7bd86f24f46a647a2665daf65c0b2b15beda3"
DERIVATION_SHA = "7d2817c82cc0cfcbc6785fa8f47c2d122e84cc0523d72aea5c0240bd30baf34d"
PINS = {
    ROOT / "computations/unaudited-codex-n8-x5-exception1114-rank1-refinement-design-2026-08-26/MANIFEST.sha256": "aea0841b7b1b6fe0773cfb5087a930329c4da5d94951ad23d559de6d61cddb46",
    ROOT / "computations/unaudited-codex-n8-x5-exception1114-rank1-symbolic-reduction-design-2026-08-26/MANIFEST.sha256": "785ec6cb6a5d790ece4fa3aed3801b48c3c51423e4378cd761ad8b50cd2d22b9",
}
SINGULAR_SHA = "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"
GTIMEOUT_SHA = "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95"
NATIVE = 300
WRAPPER = 315
RSS_CAP = 8 * 1024**3
KILL_AFTER = 5
POLL = 0.1
MAX_CLEARANCE = 600
FORBIDDEN = (
    "Singular", "gtimeout", "cadical", "drat-trim", "kissat",
    "sparse_d12_dual", "sparse_d12_dual_v4_1", "sparse_d12_dual_fixed_lane",
    "sparse_d12_dual_portfolio_audit",
)


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
LIB.proc_listallpids.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB.proc_listallpids.restype = ctypes.c_int
LIB.proc_pidpath.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
LIB.proc_pidpath.restype = ctypes.c_int


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def canon(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def exclusive(path, value):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def allpids():
    buffer = (ctypes.c_int * 65536)()
    count = LIB.proc_listallpids(ctypes.byref(buffer), ctypes.sizeof(buffer))
    if not 0 <= count < len(buffer):
        raise RuntimeError("all-process census failure")
    return [buffer[index] for index in range(count) if buffer[index] > 0]


def pidpath(pid):
    buffer = ctypes.create_string_buffer(4096)
    count = LIB.proc_pidpath(pid, ctypes.byref(buffer), ctypes.sizeof(buffer))
    return buffer.value[:count].decode() if count > 0 else None


def census():
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
    policy = {
        "method": "libproc proc_listallpids + proc_pidpath",
        "forbidden_executable_basenames": list(FORBIDDEN),
        "self_pid_excluded": True,
    }
    return {
        "policy": policy, "policy_sha256": canon(policy), "observed_paths": observed,
        "unobservable_pids": unobservable, "matches": matches, "match_count": len(matches),
        "captured_unix_seconds": time.time(),
    }


def grouppids(pgid):
    buffer = (ctypes.c_int * 4096)()
    count = LIB.proc_listpgrppids(pgid, ctypes.byref(buffer), ctypes.sizeof(buffer))
    if not 0 <= count < len(buffer):
        raise RuntimeError("process-group census failure")
    return [buffer[index] for index in range(count) if buffer[index] > 0]


def grouprss(pgid):
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


def utc(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise RuntimeError("naive clearance timestamp")
    return parsed.astimezone(timezone.utc)


if sha(SOURCE) != SOURCE_SHA or sha(HERE / "source_derivation.json") != DERIVATION_SHA:
    raise RuntimeError("source pins")
for path, expected in PINS.items():
    if not path.is_file() or sha(path) != expected:
        raise RuntimeError(("dependency pin", path))
if sha(SINGULAR) != SINGULAR_SHA or sha(GTIMEOUT) != GTIMEOUT_SHA:
    raise RuntimeError("binary pins")
for name in ("ATTEMPT.json", "result.json", "result.json.tmp", "RUN_EXCLUSIVE.lock", "stdout.log", "stderr.log", "watchdog.json"):
    if (HERE / name).exists():
        raise RuntimeError(f"single-use terminal refusal: stale {name}")
if list(HERE.glob("*.tmp")):
    raise RuntimeError("stale temporary file")

manifest = HERE / "MANIFEST.sha256"
acceptance = HERE / "independent_referee_acceptance.json"
clearance = HERE / "launch_clearance.json"
if not manifest.is_file() or not acceptance.is_file() or not clearance.is_file():
    raise RuntimeError("HELD: independent acceptance and fresh explicit clearance required")
manifest_sha = sha(manifest)
runner_sha = sha(Path(__file__))
a = json.loads(acceptance.read_text())
expected_acceptance = {
    "schema": "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_ONE_P32003_DIAGNOSTIC_ONLY",
    "held_manifest_sha256": manifest_sha,
    "source_derivation_sha256": DERIVATION_SHA,
    "source_sha256": SOURCE_SHA,
    "runner_sha256": runner_sha,
    "rank1_refinement_manifest_sha256": list(PINS.values())[0],
    "symbolic_reduction_manifest_sha256": list(PINS.values())[1],
    "prime": 32003,
    "variables": 58,
    "generators": 6533,
    "maximum_lane_count": 1,
    "exact_Q_authorized": False,
    "automatic_relaunch_authorized": False,
}
if a != expected_acceptance:
    raise RuntimeError("independent acceptance schema/pins mismatch")
c = json.loads(clearance.read_text())
expected_keys = {
    "schema", "status", "held_manifest_sha256", "independent_referee_acceptance_sha256",
    "source_sha256", "runner_sha256", "singular_sha256", "gtimeout_sha256", "nonce",
    "issued_at_utc", "expires_at_utc", "maximum_lane_count", "native_wall_seconds",
    "wrapper_wall_seconds", "rss_cap_bytes", "no_overlap_confirmed", "manager_clearance_confirmed",
    "resource_clearance_confirmed", "census_policy_sha256", "expected_census_match_count",
    "exact_Q_authorized", "automatic_relaunch_authorized",
}
if set(c) != expected_keys:
    raise RuntimeError("clearance key set")
if c["schema"] != "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_CLEARANCE_V1" or c["status"] != "CLEARED_ONE_P32003_DIAGNOSTIC_ONLY":
    raise RuntimeError("clearance status")
if c["held_manifest_sha256"] != manifest_sha or c["independent_referee_acceptance_sha256"] != sha(acceptance):
    raise RuntimeError("clearance lineage")
if c["source_sha256"] != SOURCE_SHA or c["runner_sha256"] != runner_sha or c["singular_sha256"] != SINGULAR_SHA or c["gtimeout_sha256"] != GTIMEOUT_SHA:
    raise RuntimeError("clearance pins")
if not re.fullmatch(r"[0-9a-f]{32}", c["nonce"]):
    raise RuntimeError("clearance nonce")
issued, expires, now = utc(c["issued_at_utc"]), utc(c["expires_at_utc"]), datetime.now(timezone.utc)
if not (issued <= now < expires and 0 < (expires - issued).total_seconds() <= MAX_CLEARANCE):
    raise RuntimeError("clearance expiry")
if c["maximum_lane_count"] != 1 or c["native_wall_seconds"] != NATIVE or c["wrapper_wall_seconds"] != WRAPPER or c["rss_cap_bytes"] != RSS_CAP:
    raise RuntimeError("resource geometry")
if not (c["no_overlap_confirmed"] is c["manager_clearance_confirmed"] is c["resource_clearance_confirmed"] is True):
    raise RuntimeError("clearance booleans")
if c["expected_census_match_count"] != 0 or c["exact_Q_authorized"] is not False or c["automatic_relaunch_authorized"] is not False:
    raise RuntimeError("clearance scope")
pre = census()
if c["census_policy_sha256"] != pre["policy_sha256"] or pre["match_count"] != 0:
    raise RuntimeError(("process overlap", pre["matches"]))

exclusive(HERE / "RUN_EXCLUSIVE.lock", {"nonce": c["nonce"], "manifest_sha256": manifest_sha, "runner_sha256": runner_sha})
exclusive(HERE / "ATTEMPT.json", {
    "schema": "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_ATTEMPT_V1",
    "status": "ATTEMPT_CONSUMED", "nonce": c["nonce"], "manifest_sha256": manifest_sha,
    "acceptance_sha256": sha(acceptance), "clearance_sha256": sha(clearance),
    "source_sha256": SOURCE_SHA, "runner_sha256": runner_sha, "prelaunch_census": pre,
    "relaunch_forbidden_even_if_no_result": True,
})
command = [str(GTIMEOUT), "--signal=TERM", f"--kill-after={KILL_AFTER}s", f"{WRAPPER}s", str(SINGULAR), str(SOURCE)]
started = time.monotonic()
try:
    process = subprocess.Popen(command, cwd=HERE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
except BaseException as error:
    atomic(HERE / "result.json", {
        "schema": "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_RESULT_V1", "status": "FAIL_CLOSED_POPEN",
        "error": repr(error), "attempt_consumed": True, "diagnostic_only": True,
        "mathematical_coverage": False, "automatic_relaunch": False,
    })
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
        termination = "NATIVE_WALL_CAP_300"
    if termination is not None:
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

def lines(token):
    return re.findall(rf"(?m)^{re.escape(token)}=(.*)$", stdout)

shape_ok = lines("INPUT_VARIABLES") == ["58"] and lines("INPUT_GENERATORS") == ["6533"]
unit = termination is None and process.returncode == 0 and shape_ok and lines("GROEBNER_SIZE") == ["1"] and lines("UNIT_REMAINDER") == ["0"] and lines("STATUS") == ["UNIT_IDEAL"]
nonunit = termination is None and process.returncode == 0 and shape_ok and len(lines("GROEBNER_SIZE")) == 1 and len(lines("UNIT_REMAINDER")) == 1 and lines("STATUS") == ["NONUNIT_OR_UNRESOLVED"]
status = "UNIT_IDEAL_MODULAR_DIAGNOSTIC" if unit else "NONUNIT_MODULAR_DIAGNOSTIC" if nonunit else "FAIL_CLOSED_RESOURCE_GATE" if termination else "FAIL_CLOSED_PROCESS_OR_SCHEMA"
result = {
    "schema": "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_RESULT_V1", "status": status,
    "diagnostic_only": True, "mathematical_coverage": False, "attempt_consumed": True,
    "field": "F_32003", "variables": 58, "generators": 6533, "command": command,
    "native_wall_cap_seconds": NATIVE, "wrapper_wall_seconds": WRAPPER, "rss_cap_bytes": RSS_CAP,
    "wall_seconds": wall, "peak_group_rss_bytes": peak, "peak_group_members": members,
    "termination": termination, "returncode": process.returncode, "source_sha256": SOURCE_SHA,
    "runner_sha256": runner_sha, "stdout": stdout, "stderr": stderr,
    "exact_Q_launched": False, "automatic_relaunch": False,
}
atomic(HERE / "result.json", result)
print(json.dumps({"event": "TERMINAL", "status": status, "wall": wall, "peak": peak}, sort_keys=True))

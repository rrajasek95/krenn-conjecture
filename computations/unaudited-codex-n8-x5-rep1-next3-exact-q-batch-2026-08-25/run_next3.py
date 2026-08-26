#!/usr/bin/env python3
"""Run the cleared rep1 exact-Q groups 15, 17, 25 sequentially."""

from __future__ import annotations

import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
CENSUS = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25"
CENSUS_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25"
GROUP13 = ROOT / "computations/unaudited-codex-n8-x5-rep1-group13-exact-q-pilot-2026-08-25"
GROUP13_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-group13-exact-q-referee-2026-08-25"
PLAN = GROUP13_REF / "NEXT3_EXACT_Q_HELD_PLAN.json"
SINGULAR = Path("/usr/local/Cellar/singular/4.4.1p5_3/bin/Singular")
GTIMEOUT = Path("/usr/local/Cellar/coreutils/9.11/bin/gtimeout")
NATIVE_WALL = 240
WRAPPER_WALL = 250
RSS_LIMIT_KIB = 8 * 1024 * 1024
POLL_SECONDS = 0.25
LANES = [
    (15, (0, 0, 0, 1, "z", 1, 0, 2),
     "1611c16c73323e7a85ee730ba055f9f2092873841698e8fcc4f5799571ccab04", 1841468),
    (17, (0, 0, 0, 1, "z", 2, 0, 2),
     "b608247fa31d05805fe44bfc8cc7319365cffcbf3328726da48fef7e92b7ed1c", 1841468),
    (25, (0, 0, 1, 0, "z", 0, 1, 2),
     "89061675406dd8a8b5b7ba3779ce0d97c7178cd2b3864bbf264e6a9eba35b364", 1841468),
]
PINS = {
    PLAN: "8549c4e52ef4f3e6e48997a14b7e0473d8c4fbdf3536be97d4278182f24d4224",
    GROUP13 / "MANIFEST.sha256": "4cf21dec8926b66934fecf998616a31bc06f990b35662a2c48a67d3343dcb5a8",
    GROUP13_REF / "FINAL_MANIFEST.sha256": "aa7e6ef6457d18b8020dc1ece2566b83155a4f6d44bb569242e56c345f60a16e",
    CENSUS / "MANIFEST.sha256": "6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1",
    CENSUS / "results_canonical_census.json": "5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161",
    CENSUS_REF / "FINAL_MANIFEST.sha256": "f4779fdf166f008ac6ddf98b64a76cae1d1f81cccca1b51ef4b9a9a824b8cd5a",
    BASE / "MANIFEST.sha256": "4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
    BASE / "generate_minor_quotient.py": "63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8",
    SINGULAR: "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    GTIMEOUT: "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_text(path: Path, text: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def atomic_json(path: Path, value: object) -> None:
    atomic_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


class ProcTaskInfo(ctypes.Structure):
    _fields_ = [
        ("virtual_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64),
        ("total_user", ctypes.c_uint64), ("total_system", ctypes.c_uint64),
        ("threads_user", ctypes.c_uint64), ("threads_system", ctypes.c_uint64),
        ("policy", ctypes.c_int32), ("faults", ctypes.c_int32),
        ("pageins", ctypes.c_int32), ("cow_faults", ctypes.c_int32),
        ("messages_sent", ctypes.c_int32), ("messages_received", ctypes.c_int32),
        ("syscalls_mach", ctypes.c_int32), ("syscalls_unix", ctypes.c_int32),
        ("csw", ctypes.c_int32), ("threadnum", ctypes.c_int32),
        ("numrunning", ctypes.c_int32), ("priority", ctypes.c_int32),
    ]


def group_rss_kib(process_group: int) -> tuple[int, int]:
    library = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
    info = library.proc_pidinfo
    info.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64,
                     ctypes.c_void_p, ctypes.c_int]
    info.restype = ctypes.c_int
    list_pids = library.proc_listpids
    list_pids.argtypes = [ctypes.c_uint32, ctypes.c_uint32,
                          ctypes.c_void_p, ctypes.c_int]
    list_pids.restype = ctypes.c_int
    needed = list_pids(1, 0, None, 0)
    if needed <= 0:
        raise OSError("proc_listpids size failed")
    identifiers = (ctypes.c_int * (needed // ctypes.sizeof(ctypes.c_int) + 32))()
    returned = list_pids(1, 0, identifiers, ctypes.sizeof(identifiers))
    if returned <= 0:
        raise OSError("proc_listpids failed")
    total = members = 0
    for pid in identifiers[:returned // ctypes.sizeof(ctypes.c_int)]:
        if pid <= 0:
            continue
        try:
            if os.getpgid(pid) != process_group:
                continue
        except (ProcessLookupError, PermissionError):
            continue
        task = ProcTaskInfo()
        size = ctypes.sizeof(task)
        if info(pid, 4, 0, ctypes.byref(task), size) == size:
            total += task.resident_size // 1024
            members += 1
    if not members:
        raise OSError("no observable process-group members")
    return total, members


def terminate_group(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        return
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass


def fresh_census(group_id: int, lane_dir: Path) -> dict:
    observation = subprocess.run(
        ["/bin/ps", "-axo", "pid=,ppid=,rss=,etime=,command="],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    assert observation.returncode == 0, ("process census failed", observation.stderr)
    pattern = re.compile(r"Singular|sparse_d12_dual|run_with_macos_rss_watchdog|run_group13\.py", re.I)
    matches = []
    for line in observation.stdout.splitlines():
        fields = line.strip().split(None, 4)
        if len(fields) == 5 and int(fields[0]) != os.getpid() and pattern.search(fields[4]):
            matches.append(line.strip())
    disk = os.statvfs(HERE)
    record = {
        "schema": "KRENN_X5_REP1_NEXT3_FRESH_RESOURCE_CENSUS_V1",
        "group_id": group_id,
        "recorded_unix_seconds": time.time(),
        "matching_heavy_processes": matches,
        "heavy_process_count": len(matches),
        "free_bytes": disk.f_bavail * disk.f_frsize,
        "rss_limit_kib": RSS_LIMIT_KIB,
        "native_wall_seconds": NATIVE_WALL,
        "wrapper_wall_seconds": WRAPPER_WALL,
        "manager_batch_clearance": True,
        "pass": not matches,
    }
    atomic_json(lane_dir / "preflight.json", record)
    assert not matches, ("competing heavy process", matches)
    return record


def load_generator():
    spec = importlib.util.spec_from_file_location(
        "sealed_minor", BASE / "generate_minor_quotient.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_lane(group_id: int, chart: tuple, expected_sha: str,
             expected_bytes: int, minor, base, ledger: dict) -> dict:
    lane_dir = HERE / f"group{group_id}"
    lane_dir.mkdir()
    census = fresh_census(group_id, lane_dir)
    record = ledger[group_id]
    assert record["canonical_chart"] == list(chart)
    assert record["exact_Q_source_sha256"] == expected_sha
    assert record["exact_Q_source_bytes"] == expected_bytes
    coordinate, p, q, r, kind, s, a, b = chart
    chart_input = {"coordinate": coordinate, "outside": (p, q),
                   "x_pivot": r, "q_kind": kind, "q_pivot": s,
                   "minor_pair": (a, b)}
    program = minor.build_program(base, chart_input, "0")
    encoded = program.encode()
    assert len(encoded) == expected_bytes
    assert hashlib.sha256(encoded).hexdigest() == expected_sha
    source = lane_dir / f"rep1_group{group_id}_Q.sing"
    atomic_text(source, program)
    assert sha256(source) == expected_sha
    stdout_path, stderr_path = lane_dir / "stdout.log", lane_dir / "stderr.log"
    stdout_tmp, stderr_tmp = lane_dir / "stdout.log.tmp", lane_dir / "stderr.log.tmp"
    command = [str(GTIMEOUT), "--signal=TERM", "--kill-after=10", "240",
               str(SINGULAR), "-q", str(source)]
    started = time.monotonic()
    samples = []
    termination = None
    with stdout_tmp.open("wb") as stdout, stderr_tmp.open("wb") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                   start_new_session=True)
        print(json.dumps({"event": "STARTED", "group_id": group_id,
                          "wrapper_pid": os.getpid(), "child_pid": process.pid}),
              flush=True)
        while process.poll() is None:
            elapsed = time.monotonic() - started
            try:
                rss_kib, members = group_rss_kib(process.pid)
            except OSError:
                try:
                    process.wait(timeout=max(0.05, POLL_SECONDS * 2))
                    break
                except subprocess.TimeoutExpired:
                    termination = "RSS_OBSERVER_FAILURE"
                    terminate_group(process)
                    break
            samples.append({"elapsed_seconds": round(elapsed, 6),
                            "rss_kib": rss_kib,
                            "process_group_members": members})
            if rss_kib >= RSS_LIMIT_KIB:
                termination = "RSS_CAP_8GIB"
                terminate_group(process)
                break
            if elapsed >= WRAPPER_WALL:
                termination = "WRAPPER_WALL_CAP_250"
                terminate_group(process)
                break
            time.sleep(POLL_SECONDS)
        returncode = process.wait()
        stdout.flush(); os.fsync(stdout.fileno())
        stderr.flush(); os.fsync(stderr.fileno())
    os.replace(stdout_tmp, stdout_path)
    os.replace(stderr_tmp, stderr_path)
    stdout_text = stdout_path.read_text(encoding="utf-8", errors="replace")
    parsed = {}
    for line in stdout_text.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if key in {"INPUT_GENERATORS", "GROEBNER_SIZE", "UNIT_REMAINDER", "STATUS"}:
                parsed[key] = value
    if termination is None and returncode == 124:
        termination = "NATIVE_WALL_CAP_240"
    elif termination is None and returncode != 0:
        termination = "SINGULAR_NONZERO"
    unit = (termination is None and returncode == 0
            and parsed == {"INPUT_GENERATORS": "6577", "GROEBNER_SIZE": "1",
                           "UNIT_REMAINDER": "0", "STATUS": "UNIT_IDEAL"})
    nonunit = (termination is None and returncode == 0
               and parsed.get("STATUS") == "NONUNIT_OR_UNRESOLVED")
    status = ("UNIT_IDEAL_EXACT_Q" if unit else
              "NONUNIT_EXACT_Q_DIAGNOSTIC" if nonunit else
              "FAIL_CLOSED_RESOURCE_OR_PROCESS")
    telemetry = {
        "schema": "KRENN_X5_REP1_NEXT3_LANE_WATCHDOG_V1",
        "group_id": group_id, "command": command,
        "native_wall_seconds": NATIVE_WALL,
        "wrapper_wall_seconds": WRAPPER_WALL,
        "rss_limit_kib": RSS_LIMIT_KIB,
        "rss_observer": "libproc_PROC_PIDTASKINFO_process_group",
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "returncode": returncode, "termination": termination,
        "peak_rss_kib": max((sample["rss_kib"] for sample in samples), default=None),
        "last_successful_rss_sample": samples[-1] if samples else None,
        "sample_count": len(samples), "samples": samples,
        "logs_atomic": (stdout_path.is_file() and stderr_path.is_file()
                        and not stdout_tmp.exists() and not stderr_tmp.exists()),
        "stdout_sha256": sha256(stdout_path),
        "stderr_sha256": sha256(stderr_path),
    }
    atomic_json(lane_dir / "watchdog.json", telemetry)
    result = {
        "schema": "KRENN_X5_REP1_NEXT3_EXACT_Q_LANE_V1",
        "status": status, "group_id": group_id,
        "canonical_chart": list(chart), "field": "Q",
        "source_sha256": expected_sha, "source_bytes": expected_bytes,
        "variables": 91, "input_generators": 6577,
        "parsed_stdout": parsed, "unit_ideal": unit,
        "group_closed": unit, "representative_1_closed": False,
        "returncode": returncode, "termination": termination,
        "watchdog_sha256": sha256(lane_dir / "watchdog.json"),
        "stdout_sha256": sha256(stdout_path),
        "stderr_sha256": sha256(stderr_path),
        "preflight_sha256": sha256(lane_dir / "preflight.json"),
        "fresh_process_census_pass": census["pass"],
        "second_attempt": False, "automatic_relaunch": False,
    }
    atomic_json(lane_dir / "result.json", result)
    print(json.dumps({"event": "TERMINAL", "group_id": group_id,
                      "status": status,
                      "elapsed_seconds": telemetry["elapsed_seconds"],
                      "peak_rss_kib": telemetry["peak_rss_kib"]}, sort_keys=True),
          flush=True)
    return result


def main() -> int:
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)
    assert not (HERE / "BATCH_RESULT.json").exists()
    plan = json.loads(PLAN.read_text())
    assert plan["status"] == "HELD_NOT_RUN_REQUIRES_EXPLICIT_CLEARANCE"
    assert [lane["group_id"] for lane in plan["lanes"]] == [15, 17, 25]
    census_records = json.loads((CENSUS / "results_canonical_census.json").read_text())["enumeration"]["records"]
    ledger = {record["group_id"]: record for record in census_records}
    minor = load_generator()
    base = minor.load_base()
    results = []
    stopped_early = False
    for group_id, chart, expected_sha, expected_bytes in LANES:
        result = run_lane(group_id, chart, expected_sha, expected_bytes,
                          minor, base, ledger)
        results.append(result)
        if not result["unit_ideal"]:
            stopped_early = True
            break
    batch = {
        "schema": "KRENN_X5_REP1_NEXT3_EXACT_Q_BATCH_V1",
        "status": ("PASS_ALL_THREE_UNIT_IDEALS" if len(results) == 3
                   and all(result["unit_ideal"] for result in results)
                   else "STOPPED_FAIL_CLOSED"),
        "requested_groups": [15, 17, 25],
        "launched_groups": [result["group_id"] for result in results],
        "unit_groups": [result["group_id"] for result in results if result["unit_ideal"]],
        "stopped_early": stopped_early,
        "maximum_lane_count": 3,
        "automatic_relaunch": False,
        "further_groups_launched": False,
        "representative_1_closed": False,
        "plan_sha256": PINS[PLAN],
        "group13_audit_manifest_sha256": PINS[GROUP13_REF / "FINAL_MANIFEST.sha256"],
        "census_referee_manifest_sha256": PINS[CENSUS_REF / "FINAL_MANIFEST.sha256"],
        "lane_result_sha256": {
            str(result["group_id"]): sha256(HERE / f"group{result['group_id']}" / "result.json")
            for result in results
        },
    }
    atomic_json(HERE / "BATCH_RESULT.json", batch)
    return 0 if batch["status"] == "PASS_ALL_THREE_UNIT_IDEALS" else 2


if __name__ == "__main__":
    sys.exit(main())

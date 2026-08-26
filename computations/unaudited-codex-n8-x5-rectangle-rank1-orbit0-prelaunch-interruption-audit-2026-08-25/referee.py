#!/usr/bin/env python3
"""Audit the interrupted rank1/orbit0 p32003 pilot without launching it."""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import time
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PILOT = ROOT / "computations/unaudited-codex-n8-x5-rectangle-rank1-orbit0-p32003-pilot-2026-08-25"
SUPER = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-rank1-orbit0-solver-source-supersession-2026-08-25"
OLD = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-referee-2026-08-25"
RESOURCE = ROOT / "computations/unaudited-codex-n8-x5-rep1-next3-exact-q-batch-2026-08-25"
TRANSCRIPT = Path("/Users/rishi/.codex/sessions/2026/08/24/rollout-2026-08-24T01-40-35-01a0303f-14a8-7e52-b30a-a9988e6e266e.jsonl")

FILES = {
    "EXECUTION_SOURCE_AMENDMENT.json": ("dbe489cc5e63e2793917aaa83f7f8e76e4d6427a42809da8d32ea014616fb154", 722),
    "LAUNCH_BINDING.json": ("6b4ce0d85bf5387bc9900f3678af575cb3048299c2fe5f150637524f5e24520c", 673),
    "SUPERSEDING_RESOURCE_CLEAR.json": ("dd1583583bb950484116113525a477595f99e3f5594093c206ed93b5e0e03edc", 409),
    "prepare_execution_source.py": ("7172e551e2d83f3f1ed4e7b6f23324f4bbf542603ee51a04131d318a2b4be187", 2190),
    "rank1_orbit0_p32003_execute.sing": ("7c34d1efbf74220f01a6ea150ede232b9f51f9168f15dd997ed2b204e8aacf9c", 519401),
    "run_pilot.py": ("bf92688cdf807776971834dcd3d3a84c90de738145edf3f618c09e7798640b19", 4828),
}
PINS = {
    SUPER / "FINAL_MANIFEST.sha256": "304ec4a83b5ff1c09894e5e17d100b581b849de360b1cb3242bba3e653fe095b",
    SUPER / "SUPERSEDING_STAGED_HELD_PLAN.json": "3d7f1018e313ecae9eaa14f57bd07a4eb4243bb8009920dd76732c888c8ccd40",
    OLD / "STAGED_PILOT_HELD_PLAN.json": "95120b83be0d16fb16b7814556c676caa7a01c1436e85ed884db98a210571c34",
    RESOURCE / "MANIFEST.sha256": "e7d3e6bb528cf3614690aaf0b8f246975c87d9f6c8a681a8bc2f5c536037af32",
}
REQUEST_LINE = 28285
ABORT_LINE = 28286
REQUEST_SHA = "8a29e47e423aa653b5f77457e339d34205f40bf5c9ac32b69cc676e2f5b4cbc8"
ABORT_SHA = "8cf567dbb6aeab87b7a01eb99e6255e42d3fca93d1b0871be752c36ed117aeb7"
PREFIX_SHA = "08b45ea4406e4ef36984f7e21b751db153fa618f1cf5008cf1954ecfd6d4bf0a"
CALL_ID = "call_cP7Nj4Rt1QmuCgFbkzSbSkS9"
LAUNCH_COMMAND = "/opt/homebrew/bin/gtimeout 195 python3 run_pilot.py"


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def current_solver_census():
    library = ctypes.CDLL("/usr/lib/libproc.dylib")
    list_pids = library.proc_listpids
    list_pids.argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_int]
    list_pids.restype = ctypes.c_int
    pid_path = library.proc_pidpath
    pid_path.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
    pid_path.restype = ctypes.c_int
    needed = list_pids(1, 0, None, 0)
    assert needed > 0
    identifiers = (ctypes.c_int * (needed // ctypes.sizeof(ctypes.c_int) + 32))()
    returned = list_pids(1, 0, identifiers, ctypes.sizeof(identifiers))
    assert returned > 0
    matches = []
    for pid in identifiers[:returned // ctypes.sizeof(ctypes.c_int)]:
        if pid <= 0:
            continue
        buffer = ctypes.create_string_buffer(4096)
        if pid_path(pid, buffer, 4096) <= 0:
            continue
        value = buffer.value.decode(errors="replace")
        if "Singular" in value or value.endswith("/run_pilot.py"):
            matches.append({"pid": pid, "path": value})
    return matches


def command_text(record):
    item = record.get("payload", {}).get("item", {})
    command = item.get("command", [])
    return command[2] if len(command) >= 3 else ""


def main():
    for path, expected in PINS.items():
        assert sha(path) == expected, (path, sha(path), expected)
    actual_names = {path.name for path in PILOT.iterdir()}
    assert actual_names == set(FILES), sorted(actual_names)
    inventory = {}
    for name, (expected, size) in FILES.items():
        path = PILOT / name
        stat = path.stat()
        assert path.is_file() and sha(path) == expected and stat.st_size == size
        inventory[name] = {"sha256": expected, "bytes": size,
                           "birth_unix_seconds": stat.st_birthtime,
                           "mtime_unix_seconds": stat.st_mtime}
    forbidden = [path.name for path in PILOT.iterdir()
                 if path.suffix == ".tmp" or path.suffix == ".log"
                 or "result" in path.name.lower() or "watchdog" in path.name.lower()
                 or "stdout" in path.name.lower() or "stderr" in path.name.lower()
                 or "telemetry" in path.name.lower()]
    assert forbidden == []

    lines = TRANSCRIPT.read_bytes().splitlines(keepends=True)
    assert len(lines) >= ABORT_LINE
    request_raw, abort_raw = lines[REQUEST_LINE - 1], lines[ABORT_LINE - 1]
    assert sha_bytes(request_raw) == REQUEST_SHA
    assert sha_bytes(abort_raw) == ABORT_SHA
    assert sha_bytes(b"".join(lines[:ABORT_LINE])) == PREFIX_SHA
    request = json.loads(request_raw)
    abort = json.loads(abort_raw)
    assert request["payload"]["type"] == "custom_tool_call"
    assert request["payload"]["call_id"] == CALL_ID
    request_input = request["payload"]["input"]
    assert LAUNCH_COMMAND in request_input
    assert '"sandbox_permissions":"require_escalated"' in request_input
    assert abort["payload"]["type"] == "custom_tool_call_output"
    assert abort["payload"]["call_id"] == CALL_ID
    assert abort["payload"]["output"] == "aborted by user after 361.5s"

    records = [json.loads(line) for line in lines[:ABORT_LINE]]
    executed_launches = [record for record in records
                         if record.get("type") == "event_msg"
                         and record.get("payload", {}).get("item", {}).get("type") == "CommandExecution"
                         and command_text(record).strip().startswith(LAUNCH_COMMAND)]
    direct_singular = [record for record in records
                       if record.get("type") == "event_msg"
                       and record.get("payload", {}).get("item", {}).get("type") == "CommandExecution"
                       and "/usr/local/bin/Singular" in command_text(record)
                       and "rank1_orbit0_p32003_execute.sing" in command_text(record)]
    assert executed_launches == [] and direct_singular == []
    between = records[REQUEST_LINE - 1:ABORT_LINE]
    assert not any(record.get("type") == "event_msg"
                   and record.get("payload", {}).get("item", {}).get("type") == "CommandExecution"
                   for record in between)

    amendment = json.loads((PILOT / "EXECUTION_SOURCE_AMENDMENT.json").read_text())
    clearance = json.loads((PILOT / "SUPERSEDING_RESOURCE_CLEAR.json").read_text())
    binding = json.loads((PILOT / "LAUNCH_BINDING.json").read_text())
    assert amendment["solver_launches"] == 0
    assert amendment["status"] == "PREPARED_NOT_RUN_REQUIRES_SUPERSEDING_CLEARANCE"
    assert clearance["status"] == binding["status"] == "EXPLICIT_SUPERSEDING_RESOURCE_CLEAR"
    assert binding["runner_sha256"] == FILES["run_pilot.py"][0]
    assert binding["execution_source_sha256"] == FILES["rank1_orbit0_p32003_execute.sing"][0]

    runner = (PILOT / "run_pilot.py").read_text()
    plan = json.loads((SUPER / "SUPERSEDING_STAGED_HELD_PLAN.json").read_text())
    runner_contract = {
        "one_child_creation_site": runner.count("subprocess.Popen(") == 1,
        "child_creation_not_reached": len(executed_launches) == 0,
        "rss_observes_only_child_pid": "rss(process.pid)" in runner,
        "rss_observer_failure_returns_zero": "else 0" in runner,
        "separate_atomic_logs_emitted": ".log" in runner,
        "separate_watchdog_emitted": "watchdog" in runner.lower(),
        "plan_requires_process_group_rss": plan["direct_libproc_process_group_rss"],
        "plan_requires_atomic_logs_watchdog": plan["atomic_source_result_logs_watchdog"],
    }
    assert runner_contract["one_child_creation_site"]
    assert runner_contract["child_creation_not_reached"]
    assert runner_contract["rss_observes_only_child_pid"]
    assert runner_contract["rss_observer_failure_returns_zero"]
    assert not runner_contract["separate_atomic_logs_emitted"]
    assert not runner_contract["separate_watchdog_emitted"]

    current = current_solver_census()
    assert current == []
    result = {
        "schema": "KRENN_X5_RECTANGLE_RANK1_ORBIT0_PRELAUNCH_INTERRUPTION_AUDIT_V1",
        "status": "PASS_PRELAUNCH_INTERRUPTED_ZERO_COVERAGE",
        "pilot_directory": str(PILOT.relative_to(ROOT)),
        "inventory": inventory,
        "inventory_count": len(inventory),
        "forbidden_artifacts": forbidden,
        "transcript": {
            "path": str(TRANSCRIPT), "prefix_lines": ABORT_LINE,
            "prefix_sha256": PREFIX_SHA, "request_line": REQUEST_LINE,
            "request_line_sha256": REQUEST_SHA, "abort_line": ABORT_LINE,
            "abort_line_sha256": ABORT_SHA, "call_id": CALL_ID,
            "launch_requests": 1, "command_execution_events": len(executed_launches),
            "direct_singular_execution_events": len(direct_singular),
            "terminal_output": "aborted by user after 361.5s"
        },
        "process_evidence": {
            "singular_child_created": False,
            "runner_process_created": False,
            "started_event_observed": False,
            "current_direct_libproc_matches": current,
            "census_unix_seconds": time.time(),
        },
        "coverage": {"arithmetic_started": False, "accepted_coverage": 0,
                     "modular_orbit_closed": False, "exact_Q_closed": False,
                     "representative_closed": False},
        "clearance": {
            "artifact_present": True,
            "consumed_by_arithmetic": False,
            "authorization_request_disposition": "ABORTED_BEFORE_COMMAND_EXECUTION",
            "old_clearance_reusable": False,
        },
        "pins": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
        "runner_contract_audit": runner_contract,
        "fresh_status": "HELD_NOT_MANAGER_CLEARANCE_READY_RUNNER_REPAIR_REQUIRED",
        "fresh_status_reason": [
            "runner observes only the direct child, while the sealed plan requires process-group RSS",
            "RSS observer failure maps to zero instead of terminating fail-closed",
            "runner emits no separate atomic stdout, stderr, or watchdog artifacts required by the sealed plan"
        ],
        "scope": {"read_only_source_audit": True, "solver_launches": 0,
                  "new_clearance_issued": False},
    }
    atomic_json(HERE / "results_prelaunch_interruption_audit.json", result)
    fresh = {
        "schema": "KRENN_X5_RECTANGLE_RANK1_ORBIT0_FRESH_CLEARANCE_STATUS_V1",
        "status": result["fresh_status"],
        "zero_coverage_interruption_audit_required": "results_prelaunch_interruption_audit.json",
        "old_clearance_consumed": False,
        "old_clearance_reusable": False,
        "source_ready": True,
        "runner_ready": False,
        "required_before_fresh_manager_clearance": [
            "new runner with direct libproc process-group RSS and fail-closed observer",
            "atomic stdout, stderr, result, and watchdog telemetry",
            "independent source/runner/hostile audit and fresh process/resource census"
        ],
        "launch_authorized": False,
        "solver_launches": 0,
    }
    atomic_json(HERE / "FRESH_MANAGER_CLEARANCE_STATUS.json", fresh)
    print(json.dumps({"status": result["status"], "coverage": 0,
                      "old_clearance_consumed": False,
                      "fresh_status": fresh["status"], "solver_launches": 0}, sort_keys=True))


if __name__ == "__main__":
    main()

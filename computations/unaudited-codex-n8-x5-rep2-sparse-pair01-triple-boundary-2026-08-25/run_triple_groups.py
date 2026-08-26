#!/usr/bin/env python3
"""Sequential fail-closed exact-Q run of canonical triple groups."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
LEDGER = HERE / "triple_group_ledger.json"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main():
    ledger = json.loads(LEDGER.read_text())
    assert ledger["status"] == "PASS_ENUMERATION_ONLY_NO_IDEALS_RUN"
    assert ledger["normalized_group_count"] == 3366
    assert ledger["launch_gate"]["ready_under_requested_gate"] is True
    groups = ledger["groups"]
    result_path = HERE / "results_triple_groups.json"
    attempts = []
    started_global = time.monotonic()
    terminal_reason = None
    winner = None
    for index, group in enumerate(groups):
        elapsed = time.monotonic() - started_global
        if elapsed >= 900:
            terminal_reason = "AGGREGATE_WALL_CAP"
            break
        input_path = HERE / group["canonical_input"]
        assert sha256(input_path) == group["canonical_input_sha256"]
        started = time.monotonic()
        try:
            process = subprocess.run(
                ["gtimeout", "2", "Singular", str(input_path)],
                capture_output=True, text=True, timeout=3,
            )
            stdout = process.stdout + process.stderr
            returncode = process.returncode
        except subprocess.TimeoutExpired as exception:
            stdout = (exception.stdout or "") + (exception.stderr or "")
            returncode = 124
        wall = time.monotonic() - started
        if returncode == 0 and "STATUS=NONUNIT" in stdout:
            status = "NONUNIT"
        elif returncode == 0 and "STATUS=UNIT_IDEAL" in stdout:
            status = "UNIT_IDEAL"
        else:
            status = "FAIL_CLOSED_TIMEOUT_OR_PROCESS"
        stdout_path = HERE / f"stdout_group_{index:05d}.txt"
        temporary = stdout_path.with_suffix(".txt.tmp")
        temporary.write_text(stdout)
        os.replace(temporary, stdout_path)
        record = {
            "group_index": index,
            "normalized_sha256": group["normalized_sha256"],
            "representative": group["representative"],
            "member_count": len(group["members"]),
            "input": input_path.name,
            "input_sha256": group["canonical_input_sha256"],
            "stdout": stdout_path.name,
            "stdout_sha256": sha256(stdout_path),
            "returncode": returncode,
            "wall_seconds": wall,
            "status": status,
            "input_generators": int(re.search(r"INPUT_GENERATORS=(\d+)", stdout).group(1))
                if re.search(r"INPUT_GENERATORS=(\d+)", stdout) else None,
            "groebner_size": int(re.search(r"GROEBNER_SIZE=(\d+)", stdout).group(1))
                if re.search(r"GROEBNER_SIZE=(\d+)", stdout) else None,
            "unit_remainder": re.search(r"UNIT_REMAINDER=([^\n]+)", stdout).group(1).strip()
                if re.search(r"UNIT_REMAINDER=([^\n]+)", stdout) else None,
        }
        attempts.append(record)
        if status == "NONUNIT":
            winner = record
            terminal_reason = "FIRST_NONUNIT"
        elif status != "UNIT_IDEAL":
            terminal_reason = "FIRST_FAILURE"
        if terminal_reason is not None:
            break
        if (index + 1) % 100 == 0:
            atomic_json(result_path, {
                "schema": "KRENN_X5_REP2_SPARSE_TRIPLE_GROUP_RUN_V1",
                "status": "IN_PROGRESS_ATOMIC_CHECKPOINT",
                "attempt_count": len(attempts),
                "attempts": attempts,
                "winner": None,
                "per_lane_wall_cap_seconds": 2,
                "aggregate_wall_cap_seconds": 900,
            })
    aggregate_wall = time.monotonic() - started_global
    all_unit = len(attempts) == len(groups) and all(item["status"] == "UNIT_IDEAL" for item in attempts)
    if winner is not None:
        status = "PASS_FOUND_FIRST_NONUNIT"
    elif all_unit:
        status = "PASS_ALL_TRIPLE_GROUPS_UNIT"
        terminal_reason = "EXHAUSTED_ALL_UNIT"
    else:
        status = "FAIL_CLOSED_INCOMPLETE"
    result = {
        "schema": "KRENN_X5_REP2_SPARSE_TRIPLE_GROUP_RUN_V1",
        "status": status,
        "terminal_reason": terminal_reason,
        "per_lane_wall_cap_seconds": 2,
        "aggregate_wall_cap_seconds": 900,
        "aggregate_wall_seconds": aggregate_wall,
        "group_count": len(groups),
        "attempt_count": len(attempts),
        "attempted_raw_chart_coverage": sum(item["member_count"] for item in attempts),
        "unit_count": sum(item["status"] == "UNIT_IDEAL" for item in attempts),
        "nonunit_count": sum(item["status"] == "NONUNIT" for item in attempts),
        "failure_count": sum(item["status"].startswith("FAIL") for item in attempts),
        "max_lane_wall_seconds": max((item["wall_seconds"] for item in attempts), default=0),
        "winner": winner,
        "attempts": attempts,
        "scope": "full pair01 amplitude ideals only; stop-first NONUNIT/failure policy",
    }
    atomic_json(result_path, result)
    print(json.dumps({
        "status": status,
        "reason": terminal_reason,
        "attempts": len(attempts),
        "unit": result["unit_count"],
        "nonunit": result["nonunit_count"],
        "failure": result["failure_count"],
        "winner": winner["representative"] if winner else None,
        "wall": aggregate_wall,
    }, sort_keys=True))


if __name__ == "__main__":
    main()

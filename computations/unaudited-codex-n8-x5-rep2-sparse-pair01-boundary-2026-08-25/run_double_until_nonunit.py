#!/usr/bin/env python3
"""Search normalized two-coordinate charts for the first terminal NONUNIT."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    ledger = json.loads((HERE / "double_relaxation_ledger.json").read_text())
    groups = sorted(
        ledger["groups"], key=lambda item: (-((HERE / item["input"]).stat().st_size), item["normalized_sha256"])
    )
    attempts = []
    winner = None
    global_started = time.monotonic()
    for group in groups:
        if time.monotonic() - global_started > 120:
            break
        path = HERE / group["input"]
        started = time.monotonic()
        try:
            process = subprocess.run(
                ["gtimeout", "10", "Singular", str(path)], capture_output=True,
                text=True, timeout=12,
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
            status = "FAIL_CLOSED_RESOURCE_OR_PROCESS"
        output = HERE / f"stdout_double_{len(attempts):03d}.txt"
        temporary = output.with_suffix(".txt.tmp")
        temporary.write_text(stdout)
        os.replace(temporary, output)
        record = {
            "representative": group["representative"],
            "member_count": len(group["members"]),
            "normalized_sha256": group["normalized_sha256"],
            "input": path.name,
            "input_sha256": sha256(path),
            "stdout": output.name,
            "stdout_sha256": sha256(output),
            "wall_seconds": wall,
            "returncode": returncode,
            "status": status,
            "input_generators": int(re.search(r"INPUT_GENERATORS=(\d+)", stdout).group(1))
                if re.search(r"INPUT_GENERATORS=(\d+)", stdout) else None,
            "groebner_size": int(re.search(r"GROEBNER_SIZE=(\d+)", stdout).group(1))
                if re.search(r"GROEBNER_SIZE=(\d+)", stdout) else None,
        }
        attempts.append(record)
        if status == "NONUNIT":
            winner = record
            break
    complete_all_unit = (
        winner is None and len(attempts) == len(groups)
        and all(item["status"] == "UNIT_IDEAL" for item in attempts)
    )
    result = {
        "schema": "KRENN_X5_REP2_SPARSE_DOUBLE_RELAXATION_SEARCH_V1",
        "status": (
            "PASS_FOUND_TERMINAL_NONUNIT_DOUBLE_CHART" if winner
            else "PASS_ALL_DOUBLE_GROUPS_UNIT" if complete_all_unit
            else "FAIL_CLOSED_INCOMPLETE_DOUBLE_GATE"
        ),
        "global_wall_cap_seconds": 120,
        "per_chart_wall_cap_seconds": 10,
        "attempt_count": len(attempts),
        "attempts": attempts,
        "winner": winner,
        "minimum_extra_coordinate_count_with_nonunit": 2 if winner else None,
        "exact_lower_bound_on_extra_coordinates": 3 if complete_all_unit else None,
        "scope": "Q amplitude ideals only; complete all-UNIT coverage proves no point on any <=2-extra chart",
    }
    output = HERE / "results_double_search.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({
        "status": result["status"],
        "attempts": len(attempts),
        "winner": winner["representative"] if winner else None,
        "winner_groebner": winner["groebner_size"] if winner else None,
    }, sort_keys=True))


if __name__ == "__main__":
    main()

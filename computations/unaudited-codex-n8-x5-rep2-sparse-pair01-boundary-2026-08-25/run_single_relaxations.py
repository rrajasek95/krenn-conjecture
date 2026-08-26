#!/usr/bin/env python3
"""Run the base and 28 normalized single-coordinate Q charts sequentially."""

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


def run(path, label):
    started = time.monotonic()
    try:
        process = subprocess.run(
            ["gtimeout", "30", "Singular", str(path)], capture_output=True,
            text=True, timeout=35,
        )
        stdout = process.stdout + process.stderr
        returncode = process.returncode
    except subprocess.TimeoutExpired as exception:
        stdout = (exception.stdout or "") + (exception.stderr or "")
        returncode = 124
    wall = time.monotonic() - started
    if "STATUS=UNIT_IDEAL" in stdout and returncode == 0:
        status = "UNIT_IDEAL"
    elif "STATUS=NONUNIT" in stdout and returncode == 0:
        status = "NONUNIT"
    else:
        status = "FAIL_CLOSED_RESOURCE_OR_PROCESS"
    output = HERE / f"stdout_{label}.txt"
    temporary = output.with_suffix(".txt.tmp")
    temporary.write_text(stdout)
    os.replace(temporary, output)
    groebner = re.search(r"GROEBNER_SIZE=(\d+)", stdout)
    generators = re.search(r"INPUT_GENERATORS=(\d+)", stdout)
    return {
        "label": label,
        "input": path.name,
        "input_sha256": sha256(path),
        "stdout": output.name,
        "stdout_sha256": sha256(output),
        "returncode": returncode,
        "wall_seconds": wall,
        "status": status,
        "input_generators": int(generators.group(1)) if generators else None,
        "groebner_size": int(groebner.group(1)) if groebner else None,
    }


def main():
    ledger = json.loads((HERE / "single_relaxation_ledger.json").read_text())
    base = run(HERE / "rep2_pair01_base17_Q.sing", "base17")
    assert base["status"] == "UNIT_IDEAL"
    record_by_extra = {item["extra"]: item for item in ledger["records"]}
    groups = []
    for index, group in enumerate(ledger["normalized_polynomial_groups"]):
        representative = group["representative"]
        source = record_by_extra[representative]
        result = run(HERE / source["input"], f"single_{index:02d}_{representative}")
        result.update({
            "normalized_sha256": group["normalized_sha256"],
            "representative": representative,
            "members": group["members"],
            "member_count": len(group["members"]),
        })
        groups.append(result)
        assert result["status"] != "FAIL_CLOSED_RESOURCE_OR_PROCESS", result
    nonunit = [group for group in groups if group["status"] == "NONUNIT"]
    unit = [group for group in groups if group["status"] == "UNIT_IDEAL"]
    result = {
        "schema": "KRENN_X5_REP2_SPARSE_SINGLE_RELAXATION_RUN_V1",
        "status": "PASS_TERMINAL_ALL_NORMALIZED_SINGLE_COORDINATE_GROUPS",
        "base": base,
        "groups": groups,
        "group_count": len(groups),
        "unit_group_count": len(unit),
        "nonunit_group_count": len(nonunit),
        "nonunit_coordinates": sorted(
            member for group in nonunit for member in group["members"]
        ),
        "minimum_extra_coordinate_count_with_nonunit": 1 if nonunit else None,
        "scope": "amplitude ideal only; NONUNIT means a point over algebraic closure until a literal Q point is replayed",
    }
    output = HERE / "results_single_relaxations.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({
        "status": result["status"],
        "groups": len(groups),
        "unit": len(unit),
        "nonunit": len(nonunit),
        "nonunit_coordinates": result["nonunit_coordinates"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()

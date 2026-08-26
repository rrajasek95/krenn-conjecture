#!/usr/bin/env python3
"""Frozen single-branch D9 resume runner; never advances to another branch."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

if not __debug__:
    raise RuntimeError("fail closed: runner requires assertions enabled")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def classify(engine_status):
    return {
        "COMPLETE_MODULAR_DUAL_DIAGNOSTIC": "TERMINAL_MODULAR_DUAL",
        "MODULAR_MEMBER_REQUIRES_EXACT_RATIONAL_REPLAY": "TERMINAL_EXACT_REPLAY_REQUIRED",
        "INCOMPLETE_WALL_CAP": "RESTART_CHECKPOINT_ONLY",
    }.get(engine_status, "REJECT")


def selftest():
    expected = {
        "COMPLETE_MODULAR_DUAL_DIAGNOSTIC": "TERMINAL_MODULAR_DUAL",
        "MODULAR_MEMBER_REQUIRES_EXACT_RATIONAL_REPLAY": "TERMINAL_EXACT_REPLAY_REQUIRED",
        "INCOMPLETE_WALL_CAP": "RESTART_CHECKPOINT_ONLY",
        "INCOMPLETE_COLUMN_CAP": "REJECT",
        None: "REJECT",
        "PASS": "REJECT",
    }
    assert {key: classify(key) for key in expected} == expected
    result = {
        "schema": "KRENN_X5_D9_SINGLE_RESUME_RUNNER_SELFTEST_V1",
        "status": "PASS",
        "cases": len(expected),
        "restart_is_not_terminal": classify("INCOMPLETE_WALL_CAP") == "RESTART_CHECKPOINT_ONLY",
        "multi_branch_advancement": False,
    }
    print(json.dumps(result, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--run", action="store_true")
    modes.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return

    schedule = json.loads((HERE / "SCHEDULE.json").read_text())
    assert schedule["status"] == "FROZEN_HELD_NO_PRODUCTION_LAUNCH"
    engine = schedule["engine"]
    inputs = schedule["inputs"]
    source = HERE / engine["source"]
    binary = HERE / engine["binary"]
    watchdog = HERE / schedule["watchdog"]["path"]
    provider = REPO / inputs["provider"]
    resume_selected = REPO / inputs["resume_selected"]
    resume_dual = REPO / inputs["resume_dual"]
    for path, expected in (
        (source, engine["source_sha256"]),
        (binary, engine["binary_sha256"]),
        (watchdog, schedule["watchdog"]["sha256"]),
        (provider, inputs["provider_sha256"]),
        (resume_selected, inputs["resume_selected_sha256"]),
        (resume_dual, inputs["resume_dual_sha256"]),
    ):
        assert sha256(path) == expected

    output_dir = HERE / "held_slice_triangle_p1073741827"
    assert not output_dir.exists(), "refuse pre-existing output directory"
    output_dir.mkdir()
    command = [
        str(binary),
        "--branch", "triangle_endpoint_colour",
        "--input", str(provider),
        "--resume-selected", str(resume_selected),
        "--resume-dual", str(resume_dual),
        "--resume-round-offset", str(inputs["resume_round_offset"]),
        "--output", str(output_dir / "result.json"),
        "--selected", str(output_dir / "selected.tsv"),
        "--dual", str(output_dir / "dual.tsv"),
        "--prime", "1073741827",
        "--column-cap", str(engine["column_cap"]),
        "--wall-seconds", str(engine["native_wall_seconds"]),
    ]
    wrapper = [
        sys.executable, str(watchdog),
        "--rss-gib", "8", "--wall-seconds", str(engine["wrapper_wall_seconds"]),
        "--poll-seconds", "0.25", "--source", str(source),
        "--expected-source-sha256", engine["source_sha256"],
        "--expected-binary-sha256", engine["binary_sha256"],
        "--telemetry", str(output_dir / "watchdog.json"),
        "--stdout", str(output_dir / "stdout.log"),
        "--stderr", str(output_dir / "stderr.log"),
        "--", *command,
    ]
    completed = subprocess.run(wrapper, cwd=REPO, check=False)
    result_path = output_dir / "result.json"
    watchdog_path = output_dir / "watchdog.json"
    result = json.loads(result_path.read_text()) if result_path.exists() else {}
    telemetry = json.loads(watchdog_path.read_text()) if watchdog_path.exists() else {}
    semantic_class = classify(result.get("status"))
    accepted = (
        completed.returncode == 0
        and semantic_class != "REJECT"
        and telemetry.get("status") in {"PASS_TERMINAL", "PASS_RESTART_CHECKPOINT"}
        and telemetry.get("engine_status_class") == semantic_class
        and result.get("schema") == "KRENN_X5_FOUR_BLOCKER_D9_RESUMABLE_RESULT_V1"
        and result.get("branch") == "triangle_endpoint_colour"
        and result.get("prime") == 1073741827
        and result.get("degree") == 9
        and result.get("resumed_columns") == inputs["resume_selected_columns"]
        and result.get("resume_dual_exact_match") is True
        and result.get("selected_columns", 0) > inputs["resume_selected_columns"]
    )
    record = {
        "schema": "KRENN_X5_D9_SINGLE_RESUME_RUNNER_RESULT_V1",
        "status": "PASS_ATOMIC_SINGLE_SLICE" if accepted else "FAIL_CLOSED",
        "returncode": completed.returncode,
        "engine_status": result.get("status"),
        "semantic_class": semantic_class,
        "accepted_for_mathematics": semantic_class.startswith("TERMINAL_"),
        "accepted_as_restart_checkpoint_only": semantic_class == "RESTART_CHECKPOINT_ONLY",
        "result_sha256": sha256(result_path) if result_path.exists() else None,
        "selected_sha256": sha256(output_dir / "selected.tsv") if (output_dir / "selected.tsv").exists() else None,
        "dual_sha256": sha256(output_dir / "dual.tsv") if (output_dir / "dual.tsv").exists() else None,
        "watchdog_sha256": sha256(watchdog_path) if watchdog_path.exists() else None,
        "another_branch_launched": False,
        "degree_ten_launched": False,
    }
    target = HERE / "runner_result.json"
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, target)
    print(json.dumps(record, sort_keys=True))
    if not accepted:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

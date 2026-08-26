#!/usr/bin/env python3
"""Run the three portability modes and retain stdout/result hashes."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def digest_file(path):
    return digest_bytes(path.read_bytes())


def main():
    jobs = (
        {
            "name": "binary_pool_join",
            "script": HERE / "audit_binary_pool_join.py",
            "arguments": [],
            "result": HERE / "results_binary_pool_join.json",
            "timeout": 180,
        },
        {
            "name": "cycle012_certificate",
            "script": HERE / "audit_cycle012_equivariant.py",
            "arguments": [],
            "result": HERE / "certificate_cycle012.json",
            "timeout": 120,
        },
        {
            "name": "equivariant_sweep",
            "script": HERE / "sweep_equivariant_actions.py",
            "arguments": ["--max-variables", "33", "--decision-timeout", "10",
                          "--lift-timeout", "30"],
            "result": HERE / "results_equivariant_sweep.json",
            "timeout": 240,
        },
    )
    modes = {
        "standard": ["python3"],
        "optimized": ["python3", "-O"],
        "isolated_no_site": ["python3", "-I", "-S"],
    }
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    records = {}
    for job in jobs:
        rows = {}
        for mode, prefix in modes.items():
            command = prefix + [str(job["script"])] + job["arguments"]
            completed = subprocess.run(
                command, cwd=ROOT, env=environment, text=True,
                capture_output=True, timeout=job["timeout"], check=False,
            )
            if completed.returncode != 0:
                raise RuntimeError({
                    "job": job["name"], "mode": mode,
                    "returncode": completed.returncode,
                    "stdout": completed.stdout[-2000:],
                    "stderr": completed.stderr[-2000:],
                })
            rows[mode] = {
                "command": command,
                "stdout": completed.stdout,
                "stdout_sha256": digest_bytes(completed.stdout.encode()),
                "stderr": completed.stderr,
                "result_sha256": digest_file(job["result"]),
            }
            print(job["name"], mode, rows[mode]["stdout_sha256"], flush=True)
        stdout_hashes = {row["stdout_sha256"] for row in rows.values()}
        result_hashes = {row["result_sha256"] for row in rows.values()}
        if len(stdout_hashes) != 1 or len(result_hashes) != 1:
            raise RuntimeError((job["name"], stdout_hashes, result_hashes))
        records[job["name"]] = {
            "modes": rows,
            "byte_identical_stdout": True,
            "byte_identical_result": True,
        }
    output = {
        "status": "PASS",
        "modes": list(modes),
        "jobs": records,
        "declared_jobs": [job["name"] for job in jobs],
        "executed_jobs": list(records),
    }
    (HERE / "replay_results.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n"
    )
    print("PORTABILITY PASS", len(records), "jobs x", len(modes), "modes")


if __name__ == "__main__":
    main()

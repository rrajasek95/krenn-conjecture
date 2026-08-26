#!/usr/bin/env python3
"""Replay the fast exact Cof13 factor/branch/certificate pipeline."""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SCRIPTS = (
    "build_cofactor13_b0_resultants_flint.py",
    "build_cofactor13_b0_minor_determinants_flint.py",
    "export_cofactor13_h_branch.py",
    "build_cofactor13_h_branch_certificate.py",
)
RESULTS = (
    "results_cofactor13_qg_resultant_flint.json",
    "results_cofactor13_b0_minor_determinants_flint.json",
    "results_cofactor13_h_branch_export.json",
    "certificate_cofactor13_h_branch_live_power.json",
    "results_cofactor13_h_branch_certificate_audit.json",
)
OUT = HERE / "results_three_mode_replay.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    modes = (
        ("standard", []),
        ("optimized", ["-O"]),
        ("isolated_no_site", ["-I", "-S"]),
    )
    records = []
    for name, flags in modes:
        env = dict(os.environ)
        env["PYTHONHASHSEED"] = "0"
        for script in SCRIPTS:
            run = subprocess.run([sys.executable, *flags, str(HERE/script)],
                                 capture_output=True, text=True,
                                 timeout=120, env=env, check=False)
            require(run.returncode == 0,
                    f"{name}/{script} failed: {run.stderr[-1000:]}")
        hashes = {path: json.loads((HERE/path).read_text())["result_sha256"]
                  for path in RESULTS}
        records.append({"mode": name, "logical_hashes": hashes})
    require(all(record["logical_hashes"] == records[0]["logical_hashes"]
                for record in records[1:]), "three-mode logical mismatch")
    source_result = json.loads(
        (HERE/"results_cofactor13_reduced_source_audit.json").read_text())
    result = {
        "status": "UNAUDITED three-mode exact pipeline replay PASS",
        "modes": records,
        "source_replay_logical_sha256": source_result["result_sha256"],
        "source_replay_mode_note": (
            "The slower raw-source Cof13 reconstruction was separately "
            "run in standard/-O/-I-S with the displayed stable logical "
            "hash; this runner replays the subsequent fast exact pipeline."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Cof13 three-mode replay: PASS")
    print("logical hashes:", records[0]["logical_hashes"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()

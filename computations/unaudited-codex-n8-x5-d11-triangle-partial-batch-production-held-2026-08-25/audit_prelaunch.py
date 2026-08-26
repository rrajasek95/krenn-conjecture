#!/usr/bin/env python3
"""Fail-closed small-file audit of the held production contract."""

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DESIGN = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-partial-batch-held-2026-08-25"
PINS = {
    "acceptance": "cdfe4d47dcc9d11e05be0bfb65bda269ca5ec5f5d9003ae7fc57db19da4c90c0",
    "design_manifest": "54c4d29df4c77ffc3b678d72e01a60ac694a866f29c280501108314ab3365e7a",
    "source": "261f03cfcf9bd86de1e97e2f56221e51d8597ed3f2aa9f7ab30aa092b18be889",
    "binary": "72c8a091a2a58a444121fc178ea1b71a16e580d49546e54a996e2508685b7e98",
    "watchdog": "4c703cbd748fabeff19e3daf790808de02d69a96048090f41f19112c9d4621a5",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def arg(command, name):
    positions = [index for index, value in enumerate(command) if value == name]
    assert len(positions) == 1 and positions[0] + 1 < len(command)
    return command[positions[0] + 1]


def validate_acceptance(data):
    assert data["schema"] == "KRENN_X5_D11_TRIANGLE_PARTIAL_BATCH_PRODUCTION_ACCEPTANCE_V1"
    assert data["status"] == "HELD_PENDING_D12_RESOURCE_CLEAR"
    assert data["sealed_patch_manifest_sha256"] == PINS["design_manifest"]
    assert data["source_sha256"] == PINS["source"] and data["binary_sha256"] == PINS["binary"]
    assert data["watchdog_sha256"] == PINS["watchdog"]
    assert data["branch"] == "triangle_endpoint_colour" and data["prime"] == 1_073_741_827
    assert data["seed_selected_columns"] == 913_636 and data["seed_dual_support"] == 924_170
    assert data["column_cap"] == 1_250_001 and data["remaining_capacity"] == 336_365
    resources = data["resource_contract"]
    assert resources == {"native_wall_seconds": 590, "wrapper_wall_seconds": 600,
                         "rss_gib": 38, "one_process_family_only": True,
                         "automatic_relaunch": False}
    command = data["command"]
    separator = command.index("--")
    wrapper, engine = command[:separator], command[separator + 1:]
    assert arg(wrapper, "--rss-gib") == "38"
    assert arg(wrapper, "--wall-seconds") == "600"
    assert arg(engine, "--branch") == "triangle_endpoint_colour"
    assert arg(engine, "--prime") == "1073741827"
    assert arg(engine, "--column-cap") == "1250001"
    assert arg(engine, "--wall-seconds") == "590"
    assert "1000000007" not in command and "--automatic-relaunch" not in command
    acceptance = data["acceptance"]
    assert acceptance["full_incident_scan_required"] is True
    assert acceptance["incident_columns_checked"] == 762_110
    assert acceptance["violations_observed"] == 730_426
    assert acceptance["canonical_partial_batch"] is True
    assert acceptance["violations_accepted"] == 336_365
    assert acceptance["selected_columns"] == 1_250_001
    assert acceptance["all_output_selected_pairings"] == 0
    assert acceptance["output_target_coefficient"] == 1
    assert acceptance["mathematical_verdict"] is None
    assert all(data["forbidden"].values())


def main() -> None:
    assert sha(HERE / "LAUNCH_ACCEPTANCE.json") == PINS["acceptance"]
    assert sha(DESIGN / "MANIFEST.sha256") == PINS["design_manifest"]
    assert sha(DESIGN / "src/main.rs") == PINS["source"]
    assert sha(DESIGN / "x5_d11_partial_batch") == PINS["binary"]
    assert sha(HERE / "watchdog38_600.py") == PINS["watchdog"]
    design_audit = json.loads((DESIGN / "results_design_audit.json").read_text())
    assert design_audit["status"] == "PASS_HELD_DIAGNOSTIC_ONLY"
    assert design_audit["full_frontier_required_before_prefix_acceptance"] is True
    assert design_audit["hostile_mutations_rejected"] == 6
    base = json.loads((HERE / "LAUNCH_ACCEPTANCE.json").read_text())
    validate_acceptance(base)
    mutations = []
    for path, value in (
        (("resource_contract", "native_wall_seconds"), 591),
        (("resource_contract", "wrapper_wall_seconds"), 601),
        (("resource_contract", "rss_gib"), 39),
        (("column_cap",), 1_250_002),
        (("branch",), "third_colour"),
        (("prime",), 1_000_000_007),
        (("acceptance", "canonical_partial_batch"), False),
        (("acceptance", "violations_accepted"), 336_364),
        (("resource_contract", "automatic_relaunch"), True),
    ):
        mutated = copy.deepcopy(base)
        target = mutated
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        mutations.append(mutated)
    rejected = 0
    for mutated in mutations:
        try:
            validate_acceptance(mutated)
        except AssertionError:
            rejected += 1
    assert rejected == len(mutations)
    assert not (HERE / "CLEARANCE.json").exists()
    assert not (HERE / "production_partial_batch_p107").exists()
    refusal = subprocess.run(["python3", HERE / "run_when_cleared.py"],
                             cwd=REPO, check=False, capture_output=True, text=True)
    assert refusal.returncode != 0
    assert refusal.stderr.strip() == "HELD: awaiting explicit D12_RESOURCE_CLEAR after r1587 hashing"
    result = {
        "schema": "KRENN_X5_D11_TRIANGLE_PARTIAL_BATCH_PRODUCTION_PRELAUNCH_AUDIT_V1",
        "status": "PASS_HELD_PENDING_D12_RESOURCE_CLEAR",
        "launch_acceptance_sha256": PINS["acceptance"],
        "sealed_patch_manifest_sha256": PINS["design_manifest"],
        "source_sha256": PINS["source"],
        "binary_sha256": PINS["binary"],
        "watchdog_sha256": PINS["watchdog"],
        "hostile_contract_mutations_rejected": rejected,
        "hostile_contract_mutations_total": len(mutations),
        "runner_refused_without_clearance": True,
        "production_output_absent": True,
        "automatic_relaunch": False,
        "second_prime": False,
        "other_branch": False,
        "degree_twelve_read": False,
    }
    temporary = HERE / "results_prelaunch_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_prelaunch_audit.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

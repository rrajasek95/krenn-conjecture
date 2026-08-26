#!/usr/bin/env python3
"""Fail-closed metadata/config audit for the held cap-1.6m continuation."""

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
PARENT_SOURCE = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-partial-batch-held-2026-08-25/src/main.rs"
SOURCE = HERE / "src/main.rs"
BINARY = HERE / "x5_d11_partial_batch_cap1600"
PINS = {
    "source": "a5d91a457e1cfdac45b033e31b32a52f65ff1d7f3f86fa229e28f68e20f21e5f",
    "binary": "224f5d0ad9043b62946fc68a70d18b9885f59c4cf1262d9417f5b160e82ae1a8",
    "parent_source": "261f03cfcf9bd86de1e97e2f56221e51d8597ed3f2aa9f7ab30aa092b18be889",
    "parent_manifest": "6a392f8f65d9ef921227b57d3fcb560e85f327eeb3b03d5750ee26d9d9bbe88b",
    "acceptance": "c17c8dc7b1fcd9506e35a84ede66a2770dc4f094bddd783f68a277c99dd2fd5b",
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


def validate_contract(data):
    assert data["status"] == "HELD_NO_CLEARANCE"
    assert data["parent_production_manifest_sha256"] == PINS["parent_manifest"]
    assert data["source_sha256"] == PINS["source"] and data["binary_sha256"] == PINS["binary"]
    assert data["branch"] == "triangle_endpoint_colour" and data["prime"] == 1_073_741_827
    assert data["seed_selected_columns"] == 1_250_001 and data["seed_dual_support"] == 1_378_456
    assert data["column_cap"] == 1_600_000 and data["remaining_capacity"] == 349_999
    assert data["resource_contract"] == {
        "native_wall_seconds": 590, "wrapper_wall_seconds": 600,
        "rss_gib": 38, "one_process_only": True, "automatic_relaunch": False}
    separator = data["command"].index("--")
    wrapper, engine = data["command"][:separator], data["command"][separator + 1:]
    assert arg(wrapper, "--rss-gib") == "38" and arg(wrapper, "--wall-seconds") == "600"
    assert arg(engine, "--branch") == "triangle_endpoint_colour"
    assert arg(engine, "--prime") == "1073741827"
    assert arg(engine, "--column-cap") == "1600000" and arg(engine, "--wall-seconds") == "590"
    assert all(data["forbidden"].values())


def main() -> None:
    assert sha(SOURCE) == PINS["source"] and sha(BINARY) == PINS["binary"]
    assert sha(PARENT_SOURCE) == PINS["parent_source"]
    parent, child = PARENT_SOURCE.read_text(), SOURCE.read_text()
    child_normalized = child.replace(
        '    if branch != "triangle_endpoint_colour" {\n'
        '        fail("cap-1.6m engine accepts only the triangle branch");\n'
        '    }',
        '    if !matches!(\n'
        '        branch.as_str(),\n'
        '        "direct" | "triangle_endpoint_colour" | "third_colour" | "cap_endpoint_colour"\n'
        '    ) {\n'
        '        fail("seeded recovery engine accepts only the three coloured branches");\n'
        '    }')
    child_normalized = child_normalized.replace(
        "    if prime != 1_073_741_827 || column_cap == 0 || column_cap > 1_600_000",
        "    if !matches!(prime, 1_073_741_827 | 1_000_000_007) || column_cap == 0 || column_cap > 1_250_001")
    assert child_normalized == parent
    for token in ("retain_canonical_prefix", "BTreeMap::<Column", "column < largest",
                  "truncated: violations_observed > limit", "solver.add_vector(&vector)",
                  "candidate = solver.candidate()", "incremental dual verification failed"):
        assert token in child
    selftest = json.loads(subprocess.run([BINARY, "--selftest"], check=True,
                                         capture_output=True, text=True).stdout)
    assert selftest["status"] == "PASS" and selftest["partial_refinement_replay"] is True

    base_args = ["--branch", "triangle_endpoint_colour", "--input", "missing", "--output", "o",
                 "--selected", "s", "--dual", "d", "--resume-selected", "rs",
                 "--resume-dual", "rd", "--resume-round-offset", "1", "--prime", "1073741827",
                 "--column-cap", "1600000", "--wall-seconds", "590"]
    hostiles = []
    for key, value in (("--branch", "third_colour"), ("--prime", "1000000007"),
                       ("--column-cap", "1600001"), ("--wall-seconds", "591")):
        args = base_args.copy()
        args[args.index(key) + 1] = value
        hostiles.append(args)
    for args in hostiles:
        attempt = subprocess.run([BINARY, *args], check=False, capture_output=True, text=True)
        assert attempt.returncode != 0 and "outside frozen contract" in attempt.stderr or \
            "accepts only the triangle branch" in attempt.stderr

    model = json.loads((HERE / "RESOURCE_MODEL.json").read_text())
    projection = model["projection"]
    assert model["next_gate"]["column_cap"] == 1_600_000
    assert projection["conservative_peak_rss_kib"] < model["hard_rss_limit_kib"]
    assert projection["headroom_to_hard_limit_gib"] > 3.0
    assert projection["two_scale_wall_projection_seconds"] < 590
    acceptance = json.loads((HERE / "LAUNCH_ACCEPTANCE.json").read_text())
    assert sha(HERE / "LAUNCH_ACCEPTANCE.json") == PINS["acceptance"]
    validate_contract(acceptance)
    mutations = []
    for path, value in ((('column_cap',), 1_600_001), (('prime',), 1_000_000_007),
                        (('branch',), 'third_colour'), (('resource_contract', 'rss_gib'), 39),
                        (('resource_contract', 'automatic_relaunch'), True)):
        mutated = copy.deepcopy(acceptance)
        target = mutated
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        mutations.append(mutated)
    rejected = 0
    for mutated in mutations:
        try:
            validate_contract(mutated)
        except AssertionError:
            rejected += 1
    assert rejected == len(mutations)
    assert not (HERE / "CLEARANCE.json").exists()
    assert not (HERE / "production_cap1600_p107").exists()
    result = {
        "schema": "KRENN_X5_D11_TRIANGLE_PARTIAL_BATCH_CAP1600_DESIGN_AUDIT_V1",
        "status": "PASS_HELD_NO_LAUNCH",
        "source_sha256": PINS["source"],
        "binary_sha256": PINS["binary"],
        "parent_source_sha256": PINS["parent_source"],
        "source_diff_scope": "BRANCH_RESTRICTION_AND_PRIME_CAP_CONFIG_ONLY",
        "selftest": selftest,
        "hostile_binary_configs_rejected": len(hostiles),
        "hostile_contracts_rejected": rejected,
        "resource_model_recomputed": True,
        "conservative_peak_rss_gib": projection["conservative_peak_rss_gib"],
        "hard_rss_limit_gib": 38,
        "useful_progress_plausible": True,
        "launch_authorized": False,
        "degree_twelve_read": False,
        "second_prime": False,
        "other_branch": False,
    }
    temporary = HERE / "results_design_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_design_audit.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

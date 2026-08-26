#!/usr/bin/env python3
"""Pure fail-closed contract hostiles; never invokes Singular."""
from __future__ import annotations

import copy
import json
from pathlib import Path

H = Path(__file__).resolve().parent
acceptance_schema = json.loads((H / "independent_referee_acceptance.schema.json").read_text())
clearance_schema = json.loads((H / "launch_clearance.schema.json").read_text())


def check_schema(value: dict, schema: dict) -> None:
    assert set(value) == set(schema["required"])
    for key, rule in schema["properties"].items():
        if "const" in rule:
            assert value[key] == rule["const"]
        if rule.get("type") == "object":
            check_schema(value[key], rule)


acceptance = {
    "schema": "KRENN_X5_REP5_TORUS_SELECTED_OPEN_A3720_MODULAR_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_ONE_OPEN_A3720_P32003_DIAGNOSTIC_ONLY",
    "held_manifest_sha256": "0" * 64,
    "source_derivation_sha256": "3b14df5d70220330c768bcaefbaebbd5c679367badf3237604b9c2bb6d90a75e",
    "source_sha256": "0fab67ef88a8674a161814094c6b553857e685ce311c5a42419812c71a939003",
    "runner_sha256": "2dfb2af4dfd6458692c564bec3da9104abde0af3f8ae5b885ba7b4e1dab0df6d",
    "selected73_held_manifest_sha256": "21df0017be41a8ec9e4035b0902649cf9c8ed97d43c65c88a93d1db7f8bf6d72",
    "selected73_referee_manifest_sha256": "16a32d07221def48a9e8388ca1e8b716cd71dfb44c2dc0cbea0bb22ab91203ab",
    "torus_design_manifest_sha256": "2b220f91ffa21c28506f5112a3a3e7fe791c7e3c783c1e7a319186628743659e",
    "torus_referee_manifest_sha256": "20f24c8de6e7edb0818c30c11df4716e983fd5f8bf5778ee36d6d3bccf27d0ff",
    "further_reduction_manifest_sha256": "a1be34a89dae7597ab06efe6eaba6e0e4fc12256949f667ac8124ee93c35690e",
    "further_reduction_referee_manifest_sha256": "d87fe6724f8d1f4bf628eb01986339c86705e55adf9b471cfeed140e725b123e",
    "prior_timeout_referee_manifest_sha256": "0cb2ba3080ddda143ac01e4fd9f8714876c070ee86e7e574415c22cae4cac4ff",
    "chart": {"coordinate": "a37_20", "locus": "D(a37_20)", "normalization": "a37_20=1"},
    "variables": 72,
    "generators": 6561,
    "maximum_lane_count": 1,
    "exact_Q_authorized": False,
    "closed_branch_authorized": False,
    "automatic_relaunch_authorized": False,
}
clearance = {
    "schema": "KRENN_X5_REP5_TORUS_SELECTED_OPEN_A3720_MODULAR_CLEARANCE_V1",
    "status": "CLEARED_ONE_OPEN_A3720_P32003_DIAGNOSTIC_ONLY",
    "held_manifest_sha256": "0" * 64,
    "independent_referee_acceptance_sha256": "1" * 64,
    "source_sha256": acceptance["source_sha256"],
    "runner_sha256": acceptance["runner_sha256"],
    "singular_sha256": "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    "gtimeout_sha256": "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
    "nonce": "2" * 32,
    "issued_at_utc": "2026-08-26T00:00:00+00:00",
    "expires_at_utc": "2026-08-26T00:05:00+00:00",
    "maximum_lane_count": 1,
    "native_wall_seconds": 240,
    "wrapper_wall_seconds": 255,
    "rss_cap_bytes": 8589934592,
    "no_overlap_confirmed": True,
    "manager_clearance_confirmed": True,
    "resource_clearance_confirmed": True,
    "census_policy_sha256": "bc690865397e276cba8d5d1d82445462c70203f1144df76f817cf361ec2ebf3b",
    "expected_census_match_count": 0,
    "exact_Q_authorized": False,
    "closed_branch_authorized": False,
    "automatic_relaunch_authorized": False,
}
check_schema(acceptance, acceptance_schema)
check_schema(clearance, clearance_schema)
hostiles = [
    ("acceptance_extra", acceptance, "extra", True),
    ("acceptance_missing_source", acceptance, "source_sha256", None),
    ("acceptance_wrong_shape", acceptance, "variables", 73),
    ("acceptance_wrong_chart", acceptance, "chart", {"coordinate": "a37_20", "locus": "V(a37_20)", "normalization": "a37_20=0"}),
    ("acceptance_exact_Q", acceptance, "exact_Q_authorized", True),
    ("acceptance_closed_branch", acceptance, "closed_branch_authorized", True),
    ("acceptance_relaunch", acceptance, "automatic_relaunch_authorized", True),
    ("clearance_extra", clearance, "extra", True),
    ("clearance_wrong_source", clearance, "source_sha256", "f" * 64),
    ("clearance_wall", clearance, "native_wall_seconds", 241),
    ("clearance_overlap", clearance, "no_overlap_confirmed", False),
    ("clearance_second_lane", clearance, "maximum_lane_count", 2),
]
results = []
for name, base, key, value in hostiles:
    candidate = copy.deepcopy(base)
    if value is None:
        candidate.pop(key)
    else:
        candidate[key] = value
    schema = acceptance_schema if base is acceptance else clearance_schema
    rejected = False
    try:
        check_schema(candidate, schema)
    except (AssertionError, KeyError, TypeError):
        rejected = True
    assert rejected, name
    results.append({"name": name, "status": "PASS_REJECTED"})
(H / "results_hostiles.json").write_text(json.dumps({"status": "PASS_ALL_12_HOSTILES", "tests": results, "solver_runs": 0}, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": "PASS_ALL_12_HOSTILES", "count": len(results), "solver_runs": 0}, sort_keys=True))

#!/usr/bin/env python3
"""Fail-closed audit of representative-2 design, exact quotients, and bounded failures."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "21f351085e1650dcf64889103813c869853f47b74a432596a9147d3324536acf"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def verify_inputs(metadata, inputs):
    count = 0
    stack = [inputs]
    while stack:
        item = stack.pop()
        if isinstance(item, dict) and set(item) >= {"path", "sha256"}:
            path = HERE / item["path"]
            assert sha256(path) == item["sha256"]
            count += 1
        elif isinstance(item, dict):
            stack.extend(item.values())
    return count


def load_result(name, status):
    path = HERE / name
    result = json.loads(path.read_text())
    assert result["status"] == status
    assert result["mathematical_coverage"] is False
    return result, sha256(path)


def main():
    assert sha256(PARENT_MANIFEST) == PARENT_SHA256
    gate = json.loads((HERE / "rep2_gate_metadata.json").read_text())
    split = json.loads((HERE / "rep2_rank1_split_metadata.json").read_text())
    subset = json.loads((HERE / "rep2_incidence_subset_metadata.json").read_text())
    contracted = json.loads((HERE / "rep2_contracted_incidence_metadata.json").read_text())
    pivot = json.loads((HERE / "rep2_incidence_pivot_metadata.json").read_text())

    assert gate["representative_id"] == 2
    assert gate["support"]["added"] == ["06", "14", "17", "23", "26", "56", "57"]
    assert gate["stored_edge_guard"]["at_identity"] == [
        "A06*A57^T=0", "A57^T+A17*A56^T=0", "A26*A57^T+A56^T=0",
    ]
    assert gate["candidate_star"]["cap"] == "45" and gate["candidate_star"]["center"] == 1
    assert gate["candidate_star"]["factorization"] == "A04*K*[A35^T|A56|A57]"
    assert gate["parameterized_core"]["supported_representatives"] == [0, 2]
    assert gate["parameterized_core"]["not_claimed_for_other_representatives"] == [1, 3, 4, 5]
    input_files = verify_inputs(gate, gate["inputs"])
    input_files += verify_inputs(split, split["inputs"])
    input_files += verify_inputs(subset, subset["inputs"])
    input_files += verify_inputs(contracted, contracted["inputs"])
    input_files += verify_inputs(pivot, pivot["inputs"])

    rank1_p, rank1_p_sha = load_result("results_rep2_rank1_p32003.json", "PASS_MODULAR_UNIT_DIAGNOSTIC")
    assert rank1_p["unit_ideal"] is True
    q120, q120_sha = load_result("results_rep2_rank1_Q.json", "INCOMPLETE_WALL_GATE")
    q300, q300_sha = load_result("results_rep2_rank1_Q_retry300.json", "INCOMPLETE_RESOURCE_GATE")
    assert q120["input_sha256"] == q300["input_sha256"]
    assert q300["termination"] == "NATIVE_WALL_CAP"
    assert q300["observed_peak_rss_bytes"] == 3101962240
    split_p, split_p_sha = load_result("results_rep2_rank1split_all_equal_p32003.json", "INCOMPLETE_WALL_GATE")
    cap45, cap45_sha = load_result("results_rep2_subset_cap45_star1_three_term_p32003.json", "INCOMPLETE_WALL_GATE")
    cap03, cap03_sha = load_result("results_rep2_subset_cap03_star6_two_sandwich_p32003.json", "INCOMPLETE_WALL_GATE")
    ladder_pure, ladder_pure_sha = load_result("results_rep2_ladder_pure_p32003.json", "INCOMPLETE_WALL_GATE")
    ladder_dist, ladder_dist_sha = load_result("results_rep2_ladder_distinguished_p32003.json", "INCOMPLETE_WALL_GATE")
    contracted_pure, contracted_pure_sha = load_result("results_rep2_contracted_pure_block_p32003.json", "INCOMPLETE_RESOURCE_GATE")
    pivot_pair, pivot_pair_sha = load_result("results_rep2_pivot_pair01_rho0_sigma0_p32003.json", "INCOMPLETE_RESOURCE_GATE")
    assert contracted_pure["termination"] == "NATIVE_WALL_CAP"
    assert pivot_pair["termination"] == "NATIVE_WALL_CAP"
    preflight = json.loads((HERE / "results_retry_watchdog_preflight_failure.json").read_text())
    assert preflight["status"] == "FAIL_CLOSED_ZERO_COVERAGE"
    assert preflight["mathematical_coverage"] is False

    assert contracted["records"]["pure"]["block"]["active_variables"] == 84
    assert contracted["records"]["pure"]["block"]["equations_after_adjoint_contraction"] == 15
    assert contracted["records"]["distinguished"]["block"]["active_variables"] == 90
    assert contracted["records"]["distinguished"]["block"]["equations_after_adjoint_contraction"] == 21
    assert pivot["chart_count"] == 18
    assert pivot["residual_colour_swap_orbits"]["orbit_count"] == 10
    assert pivot["residual_colour_swap_orbits"]["smallest_representative"] == "rho0_sigma0"
    assert pivot["residual_colour_swap_orbits"]["smallest_counts"] == {
        "active_variables": 80, "equations": 265,
    }
    assert pivot_pair["input_sha256"] == pivot["inputs"]["pair01"]["rho0_sigma0"]["sha256"]

    run_hashes = {
        "rank1_modular_unit_diagnostic": rank1_p_sha,
        "rank1_Q120_failure": q120_sha,
        "rank1_Q300_failure": q300_sha,
        "rank1_split_modular_failure": split_p_sha,
        "cap45_subset_modular_failure": cap45_sha,
        "cap03_subset_modular_failure": cap03_sha,
        "ladder_pure_failure": ladder_pure_sha,
        "ladder_distinguished_failure": ladder_dist_sha,
        "contracted_pure_failure": contracted_pure_sha,
        "pivot_pair01_failure": pivot_pair_sha,
    }
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP2_AUDIT_V1",
        "status": "PASS_DESIGN_AND_FAIL_CLOSED_REP2_REMAINS_UNRESOLVED",
        "parent_manifest_sha256": PARENT_SHA256,
        "representative": {
            "id": 2,
            "support_added": gate["support"]["added"],
            "guard_outside_factor": "A57",
            "primary_star": "cap45/center1",
            "alternate_star": "cap03/center6",
            "not_a_transport_of_rep0": True,
        },
        "exact_progress": {
            "rank_zero": (
                "closed structurally: A57=A56=0 makes L67 zero, while nonzero A67 is live on its full kernel"
            ),
            "rank_one": "unresolved; no exact-Q unit and no accepted modular proof",
            "rank_two": "generated but not run because rank one did not clear",
        },
        "exact_quotients": {
            "A67_graph": "nine monic adjoint variables eliminated by a quotient isomorphism",
            "incidence_charts": "18 localizations cover all nonzero rho and (sigma,tau) witnesses",
            "colour_swap_orbits": 10,
            "smallest_pair01_chart": {"id": "rho0_sigma0", "variables": 80, "equations": 265},
            "logical_sufficiency": "UNIT on a literal X5 subset chart suffices for that full chart; no run returned UNIT",
        },
        "bounded_runs": run_hashes,
        "generated_inputs_verified": input_files,
        "failure_policy": {
            "all_failures_zero_coverage": True,
            "Q_not_promoted_from_modular": True,
            "no_rank2_run": True,
            "no_automatic_widening": True,
            "geometry_stopped_after_smallest_pair01_timeout": True,
        },
        "scope": {
            "rep0_closed_elsewhere": True,
            "rep2_closed": False,
            "reps1_3_4_5": False,
            "all_six_full_family": False,
            "all_64": False,
            "D12_read": False,
        },
        "next_obligation": (
            "rep2 requires a different algebraic geometry (multigraded/resultant or a new carrier identity), not a "
            "wider repeat of these dp/slimgb ideals"
        ),
    }
    output = HERE / "results_rep2_audit.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({
        "status": result["status"], "verified_inputs": input_files,
        "rep2_closed": False, "zero_coverage_failures": len(run_hashes),
    }, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fail-closed validator for the successive-minimal X5 layer."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-four-cell-colour-escalation-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "adff4a4a49f5493a542b5042fabdcd3871777bfa91c88ab4f721b1cc3842ee02"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert result["status"] == "PASS_NONTERMINAL_MINIMAL_LAYER_CLASSIFIED"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    assert result["six_cell_input"]["one_cell_repair_exists"] is False
    first = result["colour_one_minimal_repairs"]
    assert first["two_missing_cell_matchings"] == 12
    assert first["pure_preserving_patterns"] == 6
    assert len(first["accepted_matching_names"]) == len(first["patterns"]) == 6
    assert all(item["coefficient_constraint"] == "product=-1" for item in first["patterns"])
    second = result["colour_two_layer"]
    assert second["minimum_new_cells_after_any_colour_one_repair"] == 2
    assert second["pure_preserving_patterns_per_colour_one_branch"] == 6
    assert second["matching_names"] == first["accepted_matching_names"]
    lower = result["four_cell_lower_bound"]
    assert lower["matching_pairs_with_union_at_most_three"] == 14
    assert lower["union_size_census"] == {"2": 6, "3": 8}
    assert lower["forced_pure_amplitudes"] == [0,1,1]
    continuation = result["smallest_nonminimal_continuations"]
    assert continuation["additional_cells"] == 4
    assert continuation["total_new_cells_over_base_physical_source"] == 10
    assert continuation["branch_count"] == 36
    assert continuation["outside_response_census"] == {"0": 9, "1": 21, "2": 6}
    assert continuation["common_forced_word"] == "01000010"
    assert continuation["common_forced_amplitude"] == 1
    assert continuation["minimum_cells_for_next_repair"] == 2
    assert result["finite_colour_layer_monovariant"]["values"] == [2,1,0]
    assert result["finite_colour_layer_monovariant"]["global_all_minimal_repairs_proved"] is False
    assert result["scope"]["terminality_at_six_cells"] is False
    assert result["scope"]["first_nonminimal_layer_exhaustive"] is True
    assert result["scope"]["active_clean_cap_proved"] is False
    assert evidence["lower_bound"]["minimum_additional_cells_for_both_colours"] == 4
    assert evidence["scope"]["full_conjecture_claim"] is False
    return True


def must_reject(mutator, result, evidence):
    candidate_result = copy.deepcopy(result)
    candidate_evidence = copy.deepcopy(evidence)
    mutator(candidate_result, candidate_evidence)
    try:
        check(candidate_result, candidate_evidence)
    except (AssertionError, KeyError, TypeError):
        return True
    raise AssertionError("hostile mutation accepted")


def main():
    result = json.loads((HERE / "results_successive_minimal_chain.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r,e: r["colour_one_minimal_repairs"].update(pure_preserving_patterns=7),
        lambda r,e: r["colour_two_layer"].update(minimum_new_cells_after_any_colour_one_repair=1),
        lambda r,e: r["four_cell_lower_bound"].update(forced_pure_amplitudes=[1,1,1]),
        lambda r,e: r["smallest_nonminimal_continuations"].update(branch_count=35),
        lambda r,e: r["smallest_nonminimal_continuations"].update(common_forced_amplitude=0),
        lambda r,e: r["finite_colour_layer_monovariant"].update(global_all_minimal_repairs_proved=True),
        lambda r,e: r["scope"].update(active_clean_cap_proved=True),
        lambda r,e: e["lower_bound"].update(minimum_additional_cells_for_both_colours=3),
        lambda r,e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_SUCCESSIVE_MINIMAL_CHAIN_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "first four-cell non-one-cell repair layer",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()


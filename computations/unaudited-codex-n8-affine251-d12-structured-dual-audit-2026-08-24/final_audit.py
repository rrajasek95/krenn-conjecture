#!/usr/bin/env python3
"""Strict fail-closed audit of the round659/660 structural diagnosis."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20): h.update(block)
    return h.hexdigest()


def validate(result: dict, resource: dict) -> None:
    assert result["schema"] == "KRENN_AFFINE251_D12_ROUND660_STRUCTURED_DUAL_AUDIT_V1"
    assert result["status"] == "PASS_NEGATIVE_STRUCTURAL_DIAGNOSIS"
    assert (result["prime"], result["round"], result["cached_columns"]) == (1_073_741_827, 660, 246_321)
    assert result["candidate_support"] == 352 and result["old_shifted_overlap"] == 4
    assert result["t_exponent_histogram"] == {"0":335, "1":9, "4":5, "8":2, "12":1}
    prior = result["round659_comparison"]
    assert prior["support"] == 384 and prior["cached_columns"] == 245_290
    assert (prior["support_overlap"], prior["same_coefficients"], prior["lost_rows"], prior["gained_rows"]) == (143,139,241,209)
    assert prior["high_t_eight_identical"] is True
    templates = {x["name"]: x for x in result["templates"]}
    full = templates["round660_full_candidate"]
    assert (full["support"], full["incident"], full["cached_incident"], full["missing_incident"]) == (352,1354,430,924)
    assert full["cached_bad"] == 0 and full["global_bad"] == 913
    old = templates["shifted_d8_seven"]
    assert old["support"] == 7 and old["cached_bad"] == old["global_bad"] == 10
    assert "numerator_over_2=-4" in old["first_bad"]
    high = templates["round660_high_t_eight"]
    assert high["support"] == 8 and high["cached_bad"] == high["global_bad"] == 13
    assert "numerator_over_2=-32" in high["first_bad"]
    assert result["global_incidence_closed"] is False
    for item in result["ansatz"]:
        assert item["candidate_constant_on_groups"] is False
        assert item["cached_consistent"] is False and item["global_consistent"] is False
    assert [x["groups"] for x in result["ansatz"]] == [5, 9, 83]
    assert result["full_closure_run"] is False and result["second_prime_run"] is False
    assert resource["status"] == "PASS" and resource["wall_limit_seconds"] == 120
    assert resource["elapsed_seconds"] < 120 and resource["peak_rss_bytes"] < 4 * 1024**3
    assert resource["mathematical_output_equal_excluding_elapsed"] is True
    assert resource["primary_sha256"] == sha(HERE / "results_structured_dual_audit.json")


def main() -> None:
    result = json.loads((HERE / "results_structured_dual_audit.json").read_text())
    resource = json.loads((HERE / "results_resource_replay.json").read_text())
    validate(result, resource)
    mutations = []
    forged = copy.deepcopy(result); forged["global_incidence_closed"] = True; mutations.append((forged, resource))
    forged = copy.deepcopy(result); forged["templates"][0]["global_bad"] = 0; mutations.append((forged, resource))
    forged = copy.deepcopy(result); forged["templates"][1]["cached_bad"] = 0; mutations.append((forged, resource))
    forged = copy.deepcopy(result); forged["templates"][2]["cached_bad"] = 0; mutations.append((forged, resource))
    forged = copy.deepcopy(result); forged["ansatz"][2]["cached_consistent"] = True; mutations.append((forged, resource))
    forged = copy.deepcopy(result); forged["round659_comparison"]["high_t_eight_identical"] = False; mutations.append((forged, resource))
    forged = copy.deepcopy(result); forged["full_closure_run"] = True; mutations.append((forged, resource))
    forged = copy.deepcopy(result); forged["second_prime_run"] = True; mutations.append((forged, resource))
    forged_resource = copy.deepcopy(resource); forged_resource["peak_rss_bytes"] = 4 * 1024**3; mutations.append((result, forged_resource))
    rejected = 0
    for forged_result, forged_resource in mutations:
        try: validate(forged_result, forged_resource)
        except AssertionError: rejected += 1
    assert rejected == len(mutations)
    audit = {
        "schema": "KRENN_AFFINE251_D12_ROUND660_STRUCTURED_FINAL_AUDIT_V1",
        "status": "PASS_NEGATIVE_DIAGNOSIS_SEALED",
        "result_sha256": sha(HERE / "results_structured_dual_audit.json"),
        "resource_sha256": sha(HERE / "results_resource_replay.json"),
        "hostile_mutations_rejected": rejected,
        "conclusion": "no tested low-dimensional or high-t template bypasses sequential CEGAR",
    }
    (HERE / "results_final_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__": main()

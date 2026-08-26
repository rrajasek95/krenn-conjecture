#!/usr/bin/env python3
"""Fail-closed replay of the sealed eight-block support interface."""

from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def require(condition, detail="validation failure"):
    if not condition:
        raise ValueError(detail)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check(result, check_pins=True):
    require(result["status"] == "PASS_EXACT_EIGHT_BLOCK_CENSUS_FINITE_MINIMAL_INTERFACE_NO_SOLVE", "status")
    e = result["enumeration"]
    require(e["eight_added_supports"] == 125970)
    require(e["fixed_identity_closed"] == 66752)
    require(e["fixed_identity_evaders"] == 59218)
    require(e["guard_reduced_size_census"] == {"2": 9, "3": 754, "4": 7104, "5": 20092, "6": 21307, "7": 8684, "8": 1268})
    require(e["stable_eight_supports"] == 1268)
    require(e["stable_variable_strata"] == 20288)
    require(e["classification_census"] == {"fixed_identity_cap": 16427, "nonidentity_hyperplane_cap": 3245, "unresolved_coefficient_locus": 616})
    require(e["unresolved_strata"] == 616 and e["unresolved_guard_symmetry_orbits"] == 308)
    require(e["unresolved_parent_count_census"] == {"0": 104, "1": 472, "2": 40})
    require(e["unresolved_with_no_seven_unresolved_parent"] == 104)
    records = result["unresolved_records"]
    require(len(records) == 616)
    require(Counter(len(r["seven_unresolved_parents"]) for r in records) == {0: 104, 1: 472, 2: 40})
    logical_hash = hashlib.sha256(json.dumps(records, sort_keys=True).encode()).hexdigest()
    require(logical_hash == e["unresolved_records_sha256"], "record hash")
    interface = result["first_unproved_induction_interface"]
    require(interface["smallest_new_rank_key"] == [8, 1, 66])
    require(interface["smallest_new_records"] == 4 and interface["smallest_new_guard_orbits"] == 2)
    require(len(interface["minimal_orbits"]) == 2)
    for orbit in interface["minimal_orbits"]:
        require(len(orbit["members"]) == 2)
        require(len(orbit["supported_perfect_matchings"]) == 8)
        reduction = orbit["full_x5_reduction"]
        require(reduction["base_equals_normalized_GHZ"] is False)
        require(reduction["base_word_support"] == 81 and reduction["pure_words"] == 3 and reduction["mixed_base_words"] == 78)
        decision = orbit["finite_exact_decision"]
        require(decision["total_exact_Q_systems"] == 8)
        require(decision["pairing_failure_variables"] == 180 and decision["pairing_failure_generators"] == 6579)
        require(decision["each_diagonal_failure_variables"] == 171 and decision["each_diagonal_failure_generators"] == 6576)
        carrier = orbit["selected_two_response_carrier"]
        require(carrier["cap"] == "01" and carrier["kind"] == "star" and carrier["center"] == 3)
        require(len(carrier["forbidden_nonzero_responses"]) == 2)
        require(all(len(v) == 1 for v in orbit["source_product_terms"].values()))
    lemma = result["unconditional_two_sandwich_activity_lemma"]
    require(lemma["historical_sparse_certificate_required"] is False)
    require("finite union of proper linear hyperplanes" in lemma["proof"][3])
    scope = result["scope"]
    require(scope["heavy_solver_runs"] == scope["singular_runs"] == scope["d12_reads"] == 0)
    require(scope["eight_block_layer_closed"] is False and scope["full_conjecture_claim"] is False)
    if check_pins:
        for pin in result["pins"].values():
            path = REPO / pin["path"]
            require(path.is_file(), pin["path"])
            require(sha(path) == pin["sha256"], pin["path"])


def hostiles(result):
    cases = []
    def rejects(name, mutation):
        bad = copy.deepcopy(result)
        mutation(bad)
        try:
            check(bad, check_pins=False)
        except (ValueError, KeyError):
            cases.append({"name": name, "rejected": True})
        else:
            raise ValueError("hostile accepted: " + name)
    rejects("false_closure_status", lambda x: x.__setitem__("status", "PASS_EIGHT_BLOCK_CLOSED"))
    rejects("wrong_support_total", lambda x: x["enumeration"].__setitem__("eight_added_supports", 125969))
    rejects("wrong_stable_count", lambda x: x["enumeration"].__setitem__("stable_eight_supports", 1267))
    rejects("wrong_unresolved_count", lambda x: x["enumeration"].__setitem__("unresolved_strata", 615))
    rejects("delete_record", lambda x: x["unresolved_records"].pop())
    rejects("fake_monotone_parent", lambda x: x["enumeration"]["unresolved_parent_count_census"].__setitem__("0", 0))
    rejects("wrong_minimal_rank", lambda x: x["first_unproved_induction_interface"].__setitem__("smallest_new_rank_key", [7, 1, 2]))
    rejects("drop_minimal_matching", lambda x: x["first_unproved_induction_interface"]["minimal_orbits"][0]["supported_perfect_matchings"].pop())
    rejects("wrong_finite_system_count", lambda x: x["first_unproved_induction_interface"]["minimal_orbits"][0]["finite_exact_decision"].__setitem__("total_exact_Q_systems", 4))
    rejects("restore_sparse_dependency", lambda x: x["unconditional_two_sandwich_activity_lemma"].__setitem__("historical_sparse_certificate_required", True))
    rejects("false_eight_block_claim", lambda x: x["scope"].__setitem__("eight_block_layer_closed", True))
    rejects("false_conjecture_claim", lambda x: x["scope"].__setitem__("full_conjecture_claim", True))
    return cases


def main():
    result = json.loads((HERE / "results_eight_block_interface.json").read_text())
    check(result)
    cases = hostiles(result)
    recorded = json.loads((HERE / "results_hostiles.json").read_text())
    require(recorded == {"schema": "KRENN_X5_EIGHT_BLOCK_INTERFACE_HOSTILES_V1", "status": "PASS", "cases": cases})
    print(json.dumps({"status": "PASS_EXACT_REPLAY", "result_sha256": sha(HERE / "results_eight_block_interface.json"), "records": 616, "hostiles": len(cases)}, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fail-closed validator for the residual-538 design."""

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_residual538_design.json"


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def validate_schema(data, check_file=True):
    require(data["schema"] == "n8-x5-nine-block-residual538-max17-held-design-v1")
    require(data["status"] == "PASS_DESIGN_ONLY_ZERO_HEAVY_RUN")
    ledger = data["residual_ledger"]
    require(ledger == {"input_records": 538, "exact17_degree4_records": 534, "exact16_without_degree4_records": 4, "accepted_coverage_now": 0, "remaining_now": 538})
    e17 = data["exact17_degree4"]
    require(e17["records"] == 534)
    require(e17["literal_guard_orbits"] == 267)
    require(e17["unlabelled_graph_classes"] == 50)
    require(e17["new_minimal_records"] == 80)
    require(len(e17["record_indices"]) == 534 and len(e17["guard_orbits"]) == 267 and len(e17["graph_classes"]) == 50)
    require(e17["graph_class_size_census"] == {"4": 5, "8": 26, "10": 1, "12": 3, "16": 14, "36": 1})
    if check_file:
        require(sha(HERE / e17["held_contract"]) == e17["held_contract_sha256"])
        held = json.loads((HERE / e17["held_contract"]).read_text())
        require(held["status"] == "HELD_ZERO_MATERIALIZATION_NO_CLEARANCE")
        require(all(value is None for value in held["scheduling_dependencies"].values() if not isinstance(value, str)))
        require(held["covered_current_nine_records_if_terminal"] == 534)
        require(held["refusal"].startswith("do not generate or read"))
    exc = data["exact16_no_degree4"]
    require(exc["records"] == 4 and exc["formal_guard_orbits"] == 2 and exc["unlabelled_graph_classes"] == 1)
    require(exc["full_source_site_transport_orbits"] == 1 and exc["source_site_transport_group_order"] == 8)
    require(exc["representative_record"] == 1114)
    require(set(exc["transport_from_representative"]) == {"1114", "1978", "2014", "2036"})
    require(len(exc["records_detail"]) == 4)
    require(all(r["degree_sequence"] == [3, 3, 3, 3, 5, 5, 5, 5] for r in exc["records_detail"]))
    require(all(len(r["supported_perfect_matchings"]) == 15 for r in exc["records_detail"]))
    require(all(r["carrier_census"]["minimum_load"] == 2 and len(r["carrier_census"]["minimum_carriers"]) == 16 for r in exc["records_detail"]))
    known = exc["known_interface_tests"]
    require(known["degree4_max16_or_max17"].startswith("NOT_APPLICABLE"))
    require(known["four_regular"].startswith("NOT_APPLICABLE"))
    require(known["five_regular"].startswith("NOT_APPLICABLE"))
    require(known["degree3_exact18_or_exact19"].startswith("NOT_APPLICABLE"))
    require(known["max_degree5_balanced_all_bridge"].startswith("PREMISE_MISSING"))
    require(exc["selected_two_term_carriers"]["hard_boundary"].startswith("all minimum-load carriers"))
    scope = data["scope"]
    require(scope["large_cnf_materialized_or_read"] is False)
    require(scope["sat_or_drat_runs"] == 0 and scope["singular_runs"] == 0)
    require(scope["external_theorem_promoted"] is False and scope["residual_closed"] is False and scope["full_conjecture_claim"] is False)


def main():
    observed = json.loads(RESULT.read_text())
    validate_schema(observed)
    if __debug__:
        spec = importlib.util.spec_from_file_location("builder", HERE / "build_design.py")
        require(spec is not None and spec.loader is not None)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        rebuilt = module.make_result()
        require(json.dumps(observed, sort_keys=True, separators=(",", ":")) == json.dumps(rebuilt, sort_keys=True, separators=(",", ":")), "semantic rebuild mismatch")
    print(json.dumps({"status": "PASS", "result_sha256": sha(RESULT)}, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent referee package for the exact d9 seed-row theorem."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FULL = HERE / "results_y10_d9_staged_blocks.json"
SEED_CHECKER = (
    ROOT / "computations/unaudited-codex-n8-y10-degree9-seeds-2026-08-23"
    / "audit_degree9_seeds.py"
)
SEED_REPORT = SEED_CHECKER.with_name("REPORT.md")
OUTPUT = HERE / "results_y10_d9_referee.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    spec = importlib.util.spec_from_file_location("d9_seed_referee", SEED_CHECKER)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "cannot load d9 seed checker")
    spec.loader.exec_module(module)
    seed = module.audit()
    require(seed["logical_sha256"]
            == "fee70f071e6123712a6d060c5dd2aadc4f9e7c79efc082b660343fb77d1238de",
            "d9 seed theorem changed")
    combined = seed["combined"]
    require(combined["primitive_columns"] == 160
            and combined["one_shell_columns"] == 1689
            and combined["top_rows"] == 9976,
            "d9 restricted matrix census changed")
    require(combined["one_shell_peeled_columns"] == 945
            and combined["one_shell_residual_columns"] == 744
            and combined["one_shell_residual_seed_columns"] == 0,
            "d9 restricted peel theorem changed")

    full = json.loads(FULL.read_text())
    require(full["status"] == "D9_CAP_UNRESOLVED_DURING_COMPONENT_CLOSURE",
            "full d9 control changed terminal status")
    require(full["seed_components_completed"] == 21
            and full["seed_columns_accounted"] == 23
            and full["aggregate_closed_columns"] == 70_785
            and full["aggregate_closed_rows"] == 3_673_533,
            "full d9 partial closure census changed")
    require(all(item["singleton_residual_columns"] == 0
                for item in full["component_records"]),
            "a completed full d9 component retained a core")

    result = {
        "format": "n8-orbit26-y10-d9-referee-v1",
        "status": "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D9",
        "authoritative_seed_theorem_logical_sha256": seed["logical_sha256"],
        "restricted_top_matrix": {
            "target_seeds": combined["primitive_columns"],
            "all_literal_owners": combined["one_shell_columns"],
            "seed_top_rows": combined["top_rows"],
            "peeled_columns": combined["one_shell_peeled_columns"],
            "residual_nonseed_columns": combined[
                "one_shell_residual_columns"
            ],
            "residual_seed_columns": combined[
                "one_shell_residual_seed_columns"
            ],
        },
        "referee_logic": (
            "Restrict any full y9-head relation to the 9,976 top rows of the "
            "160 target-touching seeds. The enumerated 1,689 columns are every "
            "global original/quintic owner of those rows, so omitted columns are "
            "identically zero on the restriction. Exact leaf elimination forces "
            "the coefficient of every seed to zero; the 744-column remainder "
            "contains no seed and is irrelevant to target feed. Positive-t d9 "
            "columns lie in t*M8 and frozen d8 standardness excludes them."
        ),
        "full_closure_control": {
            "status": full["status"],
            "completed_components": full["seed_components_completed"],
            "accounted_seeds": full["seed_columns_accounted"],
            "unprocessed_seeds": full["seed_columns_unprocessed"],
            "closed_columns": full["aggregate_closed_columns"],
            "closed_rows": full["aggregate_closed_rows"],
            "completed_component_residual_columns": 0,
            "cap_reason": full["bounded_stop"]["reason"],
            "active_seed": full["bounded_stop"]["active_seed"],
            "active_columns_discovered": full["bounded_stop"][
                "columns_discovered"
            ],
            "active_columns_processed": full["bounded_stop"][
                "columns_processed"
            ],
            "active_rows_discovered": full["bounded_stop"][
                "rows_discovered"
            ],
        },
        "scope": (
            "exact target standardness through total degree nine in frozen "
            "chart26/t-last order; the broad full inverse closure capped and is "
            "only a consistent control, not the proof; no d10 claim"
        ),
        "source_sha256": {
            str(SEED_CHECKER.relative_to(ROOT)):
                sha256(SEED_CHECKER.read_bytes()).hexdigest(),
            str(SEED_REPORT.relative_to(ROOT)):
                sha256(SEED_REPORT.read_bytes()).hexdigest(),
            str(FULL.relative_to(ROOT)): sha256(FULL.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("y10 d9 referee package: PASS")
    print("restricted rows/cols/peeled/residual-seeds:", 9976, 1689, 945, 0)
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()

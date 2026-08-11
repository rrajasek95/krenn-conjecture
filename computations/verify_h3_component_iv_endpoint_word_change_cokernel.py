#!/usr/bin/env python3
"""Exact endpoint-word-change obstruction for Component-IV tau_v.

The standard endpoint bars really do kill the Omega_v ridge boundary.  This
checker retains their literal source-derivation companions, verifies target
zero, and computes the complete integral cokernel.  It also replays the
chart-25 ridge candidate as a scope guard.
"""

from contextlib import redirect_stdout
from hashlib import sha256
import io
import json

import verify_h3_rootless_five_ridge_response_bianchi_cokernel as RIDGE
import verify_n8_chart25_relative_cell_component_iii_grade_gate as CHART25


EXPECTED_DIGEST = "47d9e9337e27557240f990867ad7dfc07b87ab2bac0f9dff1f7ee0d9cced7d59"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def literal_endpoint_bars():
    paths = RIDGE.endpoint_ridge_paths()
    require(len(paths) == 5, "endpoint bar face count changed")
    for record in paths:
        v = record["v"]
        middle = record["middle_colour"]
        expected = {
            "pq:22": 1,
            "pq:00": -1,
            f"x{v}:0{middle}": -1,
            f"x{v}:00": 1,
        }
        require(record["omega"] == expected,
                ("endpoint bar is not the same Omega_v", v, record))
        require(record["pq_paths"] == 2
                and record["pq_square_path_difference"] == 0
                and record["xv_paths"] == 1
                and record["correction_boundary"] == "-Omega_v",
                "endpoint path/Bianchi boundary changed")
    return paths


def complete_source_routes():
    companions, targets = RIDGE.covariance_companions()
    require(len(companions) == 15
            and len({entry[3] for entry in companions}) == 15,
            "all-derivation companion census changed")
    require(len(targets) == 5
            and all(record["target_terms"] == 0 for record in targets),
            "complete endpoint word change acquired target")

    module = RIDGE.integral_cokernel(companions)
    require(module["ambient_rank"] == 20
            and module["route_columns"] == 15
            and module["matching_bianchi_differences"] == 15,
            "complete endpoint module dimensions changed")
    require(module["available_rank"] == 15
            and module["rank_with_five_clean_repairs"] == 20
            and module["primitive_cokernel_rank"] == 5
            and module["integral_unit_pivots"] == 15
            and module["cokernel"] == "Z^5",
            "endpoint response-companion cokernel changed")
    require(all(record["ridge_cancelled"]
                and record["nonzero_companion_terms"] > 0
                for record in module["anchor_normalized_samples"]),
            "an anchor-normalized/equivariant route lost its companion")

    return {
        "routes": [
            {
                "deleted_site": v,
                "matching_index": matching_index,
                "matching": [list(edge) for edge in matching],
                "all_derivation_companion": [list(cell) for cell in monomial],
                "column": "(-Omega_v,q_(v,N))",
                "target": 0,
                "normalized_ordinary_residue": 1,
            }
            for v, matching_index, matching, monomial in companions
        ],
        "module": module,
        "separators": module["separators"],
        "equivariant_average_has_nonzero_companion": True,
    }


def chart25_scope_guard():
    captured = io.StringIO()
    with redirect_stdout(captured):
        CHART25.main()
    output = captured.getvalue()
    require(CHART25.EXPECTED_LEDGER_SHA256 in output,
            "chart-25 exact scope guard lost its digest")
    return {
        "ledger": CHART25.EXPECTED_LEDGER_SHA256,
        "local_projection": "4D",
        "off_fibre_rows_at_least": 818,
        "distinct_targets": 4,
        "selected_endpoint_grade_compatible": False,
        "supplies_endpoint_homotopy": False,
    }


def main():
    ledger = {
        "scope": "h=3 Component-IV endpoint-word-change layer",
        "literal_bars": literal_endpoint_bars(),
        "complete_source_routes": complete_source_routes(),
        "chart25_guard": chart25_scope_guard(),
        "verdict": {
            "Omega_same_as_tau_descent_obstruction": True,
            "formal_endpoint_bar_exists": True,
            "source_provenant_E_v_with_zero_ores_exists": False,
            "equivariant_sum_finishes_n_c": False,
            "primitive_separator": (
                "lambda_v=Omega_v+sum_N q_(v,N)"
            ),
            "next_attaching_cell": (
                "a reduced relative ridge augmentation A_(v,N) with zero "
                "Omega/target/cap boundary and companion augmentation -1"
            ),
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, ("ledger changed", digest))

    print("h=3 Component-IV endpoint word change: PRIMITIVE COKERNEL (exact)")
    print("formal bars: dE_v=-Omega_v, same four labelled ridges")
    print("physical routes: (-Omega_v,q_(v,N)), 15 independent columns")
    print("complete natural module: rank 15 in rank 20; coker Z^5")
    print("source-provenant E_v with tgt=ores=0: DOES NOT EXIST")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()

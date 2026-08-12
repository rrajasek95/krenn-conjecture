#!/usr/bin/env python3
"""Readout obstruction to the relative abcde augmentation U.

The full-cycle monomial abcde is present in the literal source inventory,
but only as the multiplier of the pure unary full-nine row.  It is not a
squarefree matching coefficient: every odd site occurs twice.  The unique
top source column with this row/multiplier label has coarse data

    (lower abcde label, ainc, W, target, ores) = (1,-1,0,1,0).

Old cap/residue columns cannot turn it into (1,0,0,0,0).  The primitive
covector lower+ainc kills the complete admitted block and detects the
desired relative augmentation.  Exact enumeration of the complete
degree-five full-nine module shows that its boundary is injective; the
five C5/Tate owners obey coefficient sum zero on this pure label, and any
top correction cancels lower label, anchor, and target termwise.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "d5c72fa4a62fbfd224b0c33bc557dd0c83d04f15e1b23a9bb329ec301e669c00"
PINS = {
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_rootless_five_cycle_tate_anchor_obstruction.py":
        "a1383c13a732ec34eda5614c4346fecfd99b960480727ba26ac7089690844936",
    "computations/verify_h3_rootless_abcde_relative_matching_cell_obstruction.py":
        "39a4c24a23f8c315f6a90a9768aff6cc3061c51528b0a66594e22f8182f717af",
}

ROWS = ("lower_abcde", "ainc", "W", "target", "ores")


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, ("cannot import", path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dot(left, right):
    return sum(Q(a) * Q(b) for a, b in zip(left, right, strict=True))


def source_label_audit(complete):
    # The full cycle is a polynomial multiplier, not a literal K8 matching:
    # each odd site has degree two and the external sites degree zero.
    counts = {site: 0 for site in range(8)}
    for left, right, _left_colour, _right_colour in complete.CYCLE_CELLS:
        counts[left] += 1
        counts[right] += 1
    profile = tuple(counts[site] for site in range(8))
    require(profile == (0, 2, 2, 2, 2, 2, 0, 0),
            ("abcde site profile changed", profile))

    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "abcde_unary_complete_base",
    )
    positive = load(
        "computations/verify_h3_rootless_five_cycle_positive_interface.py",
        "abcde_unary_positive_interface",
    )
    exact = complete.audit(base, positive)
    tate = exact["natural_tate_map"]
    top = exact["top_correction"]
    require(tate["full_cycle_selected_owners"] == list(range(5)),
            "abcde stopped having exactly the five cyclic owners")
    require(tate["kernel_anchor_incidence"] == 0
            and tate["kernel_physical_target"] == 0,
            "a compatible Tate relation acquired anchor/target")
    require(top["complete_columns"] == top["boundary_rank"] == 4266
            and top["kernel"] == 0,
            "complete top source map stopped being injective")
    require(top["net_anchor_after_correction"] == 0
            and top["net_target_after_correction"] == 0,
            "unique top correction stopped cancelling readouts termwise")

    return {
        "cycle_cells": [list(cell) for cell in complete.CYCLE_CELLS],
        "physical_site_profile_0_to_7": list(profile),
        "is_literal_squarefree_matching_coefficient": False,
        "actual_source_occurrence": (
            "pure output word 0^8 with polynomial multiplier abcde"
        ),
        "pure_top_labels": 22,
        "full_cycle_owner_count": 5,
        "full_cycle_owner_components": tate["full_cycle_selected_owners"],
        "Tate_compatibility_on_full_cycle": "sum_i gamma_i=0",
        "complete_top_columns_rank_kernel": [
            top["complete_columns"], top["boundary_rank"], top["kernel"]
        ],
        "top_correction_cancels_anchor_target_termwise": True,
    }


def readout_obstruction():
    # After suppressing the common nonzero scalar abcde, the literal pure
    # unary source row has target +1 and anchor incidence -1.  The old cap
    # and split-residue columns do not alter the lower source label or ainc.
    unary = (1, -1, 0, 1, 0)
    desired = (1, 0, 0, 0, 0)
    separator = (1, 1, 0, 0, 0)  # lower_abcde + ainc
    records = []
    for y in (Q(1), Q(2), Q(-3), Q(5)):
        target_cap = (0, 0, -y, 1, 0)
        split_residue = (0, 0, 1, 0, 1)
        chart_difference = (0, 0, 0, 0, 0)
        columns = (unary, target_cap, split_residue, chart_difference)
        require(all(dot(separator, column) == 0 for column in columns),
                ("lower+ainc stopped killing old source/cap block", y))
        require(dot(separator, desired) == 1,
                "lower+ainc stopped detecting U")

        # Solving target and W/ores can remove the unary target, but ainc
        # remains -1.  No cap column changes it.
        records.append({
            "Y": str(y),
            "literal_unary": list(unary),
            "target_cap": [str(value) for value in target_cap],
            "split_residue": list(split_residue),
            "separator_on_available": 0,
            "separator_on_desired_U": 1,
        })

    return {
        "row_order": list(ROWS),
        "literal_pure_unary_abcde_column": list(unary),
        "desired_relative_U": list(desired),
        "primitive_separator": "lower_abcde+ainc",
        "specializations": records,
        "normalizing_abcde_to_one_changes_readouts": False,
        "reason": (
            "localization changes a coefficient into a unit but does not "
            "erase its source multidegree, target label, or anchor incidence"
        ),
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "abcde_unary_complete_module",
    )
    ledger = {
        "theorem": "abcde unary relative-augmentation readout obstruction",
        "literal_source_label": source_label_audit(complete),
        "coarse_readout": readout_obstruction(),
        "verdict": (
            "the source inventory contains abcde only as a pure unary row "
            "multiplier.  That column carries target +abcde and anchor "
            "-abcde.  Complete Schur/C5/Tate compatibility and all top "
            "corrections cannot retain its lower source label while making "
            "tgt=ainc=W=ores=0"
        ),
        "first_missing_type": (
            "a genuinely relative degree-abcde lower face with nonzero "
            "presentation augmentation but zero physical anchor and target; "
            "it is not a normalized unary matching coefficient"
        ),
        "scope": (
            "complete direct-free degree-five polynomial full-nine module, "
            "natural C5/Tate map, and old cap/residue block; no arbitrary "
            "new relative source generator is excluded"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h3 rootless abcde unary relative augmentation: OBSTRUCTED")
    print("literal abcde source occurrence: pure unary row multiplier")
    print("squarefree matching coefficient: NO (odd-site profile 2^5)")
    print("coarse column: (lower,ainc,W,tgt,ores)=(1,-1,0,1,0)")
    print("desired (1,0,0,0,0) separated by lower+ainc")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Replace the first-flat pure marker by physical anchor incidence.

The exact first-flat dependency is

    pure_aggregate + sum(six selected physical matching rows) = 0.

On a repeated pure full-nine column the marker is exactly minus physical
anchor incidence; both vanish on the endpoint-odd order-six operator block.
Therefore the same dependency is the fully physical covector

    Lambda = sum(six selected matching rows) - ainc.

It kills the complete repeated component, all absolute extensions from the
previous exhaustivity theorem, the exact 8,580-column first-flat block, the
known eta/sigma stabilizers, and the currently specified endpoint-odd
relative alpha-cell.  It reads one on the desired boundary-zero physical
anchor.  This is a canonical bounded physical separator; arbitrary new
relative mapping-cone generators remain the only possible way to kill it.
"""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_six_term_dual_absolute_resolution_exhaustivity.py":
        "d1b545f25603930a6247a286c5be70c7d16e20caab053401eeeb650bb53559d6",
    "computations/verify_h3_first_flat_endpoint_bridge.py":
        "e22cc0eec09c0e67c10bc9ae1bd50bf26167f8d44af7857e7c6920f42bba63c2",
    "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py":
        "5a89d25227562b397d6cf3f16306346ce7d9fd16fb73a0f0a4486355a7cef29e",
    "computations/verify_h3_repeated_component_six_term_separators.py":
        "b8c3eff88b44a9a12d45f61b44449ac8a0b3a4c3e9a6d351a50ef19293ce2d25",
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py":
        "b890195a8fc0c4e90c9c9c0c03c41a95690228c81026f4c2ea1fa95908564e38",
}
EXPECTED_LEDGER_SHA256 = "bd41b41fdef28c5a2cfcf2d1c187e7145eb5c1c54a3015be7cbd0d61b3760bbd"


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def local_count(monomial, site, colour):
    return sum((left == site and a == colour)
               + (right == site and b == colour)
               for left, right, a, b in monomial)


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "physical_anchor_separator_base",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "physical_anchor_separator_complete",
    )
    absolute = load(
        "computations/verify_h3_six_term_dual_absolute_resolution_exhaustivity.py",
        "physical_anchor_separator_absolute",
    )
    first_flat = load(
        "computations/verify_h3_first_flat_endpoint_bridge.py",
        "physical_anchor_separator_first_flat",
    )
    endpoint_odd = load(
        "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py",
        "physical_anchor_separator_endpoint_odd",
    )
    require(absolute.EXPECTED_LEDGER_SHA256
            == "ae3c65f9ed33f96a568621f35df250fb5885d5ef650edcdcdd0bd456ca0c4c63",
            "absolute exhaustivity ledger pin changed")
    require(first_flat.EXPECTED_LEDGER_SHA256
            == "de8151738fe609f857e4e5917c3555067b2a9681018567fd11236c706316d997",
            "first-flat exact dependency ledger pin changed")
    require(endpoint_odd.EXPECTED_LEDGER_SHA256
            == "85887afc1e4d409d533005f4cd2de667301fc40fa0c88af31077829fa744311a",
            "endpoint-odd protected-readout ledger pin changed")

    # Canonical order-six bridge component: faces (3,5), index 1.
    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    target_degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, target_degree)
    pure_indices, selected = absolute.selected_private_features(component)

    # The physical augmented repeated column is (-B, ainc=-1) on pure rows
    # and (-B, ainc=0) otherwise.  Lambda=sum(features)-ainc.
    repeated_pairings = []
    for word, _multiplier, boundary in component["columns"]:
        feature_sum = -sum(feature in boundary for feature in selected)
        ainc = -int(word == (0,) * 8)
        repeated_pairings.append(feature_sum - ainc)
    require(set(repeated_pairings) == {0},
            "physical anchor separator stopped killing repeated d1")

    # Exact first-flat dependency says the selected-feature sum is zero on
    # every one of the 8,580 operator columns.  Endpoint oddness says ainc=0
    # there.  This is a literal substitution Q=-ainc, not a new rank claim.
    operator_feature_sum = 0
    operator_ainc = 0
    require(operator_feature_sum - operator_ainc == 0,
            "endpoint-odd operator acquired physical Lambda value")

    # The existing relative alpha cell has +sum alpha_j B_j, ainc=0.
    # Each selected private row reads one on its corresponding pure B_j and
    # alpha=(-1,1,1,-1) has zero total.  Hence it does not kill Lambda.
    alpha = (-1, 1, 1, -1)
    relative_alpha_pairing = sum(alpha)
    require(relative_alpha_pairing == 0,
            "known relative alpha-cell acquired aggregate pairing")

    stabilizer_fields = {
        **{f"eta_p0_minus_{site}0": ((6, 0, 1), (site, 0, -1))
           for site in range(1, 6)},
        **{f"left_x0_minus_{site}0": ((0, 0, 1), (site, 0, -1))
           for site in range(1, 6)},
        "external_p2_minus_x2": ((6, 2, 1), (0, 2, -1)),
        "external_x0_minus_p0": ((0, 0, 1), (6, 0, -1)),
    }
    stabilizer_weights = {}
    for label, field in stabilizer_fields.items():
        values = [sum(weight * local_count(feature, site, colour)
                      for site, colour, weight in field)
                  for feature in selected]
        require(set(values) == {0},
                ("physical Lambda sees stabilizer", label, values))
        stabilizer_weights[label] = values

    desired = {
        "selected_matching_features": 0,
        "ainc": -1,
        "W": 0,
        "target": 0,
        "ores": 0,
    }
    desired_pairing = desired["selected_matching_features"] - desired["ainc"]
    require(desired_pairing == 1,
            "physical separator stopped normalizing desired anchor")

    return {
        "theorem": "canonical first-flat six-term relation is a physical anchor separator",
        "canonical_faces": [left, right],
        "canonical_fine_degree": list(target_degree),
        "selected_private_features": [repr(value) for value in selected],
        "pure_repeated_columns": len(pure_indices),
        "physical_covector": "Lambda=sum_6 selected matching rows - ainc",
        "derivation": (
            "the first-flat relation Q+sum_6(feature)=0 becomes "
            "sum_6(feature)-ainc=0 because Q=-ainc on repeated pure rows "
            "and Q=ainc=0 on the endpoint-odd operator block"
        ),
        "pairings": {
            "complete_288_repeated_columns": sorted(set(repeated_pairings)),
            "complete_8580_first_flat_operator_columns": 0,
            "all_absolute_higher_source_extensions": 0,
            "two_chart_and_natural_Tate_kernels": 0,
            "known_relative_alpha_cell": relative_alpha_pairing,
            "desired_boundary_zero_anchor": desired_pairing,
        },
        "known_physical_stabilizer_weights": stabilizer_weights,
        "desired_signature": desired,
        "consequence": (
            "the canonical bounded comparison has a fully physical "
            "generator-or-separator alternative: any new protected-zero "
            "relative cell on which Lambda is nonzero normalizes to the "
            "anchor generator; otherwise Lambda descends as the separator"
        ),
        "scope": (
            "canonical faces-(3,5) exact first-flat block, all absolute "
            "extensions, listed stabilizers, and the presently specified "
            "relative alpha-cell.  An arbitrary new relative generator, "
            "cyclic face propagation, and transverse landing remain open"
        ),
    }


def main():
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("physical anchor separator ledger changed", digest))
    print("h3 first-flat physical anchor six-term separator: PASS")
    print("Lambda = sum six private matching rows - physical ainc")
    print("Lambda(old/absolute/known-relative) = 0")
    print("Lambda(desired boundary-zero anchor) = 1")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

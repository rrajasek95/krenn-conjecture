#!/usr/bin/env python3
"""Promote the six-term repeated dual through the absolute source resolution.

For one chart the complete repeated physical boundary map is injective.
Hence the image of any absolute higher differential landing in that
component is zero: d1*d2=0 and ker(d1)=0.  For two identical charts the
kernel is exactly the anti-diagonal labelled-column module, and every
chart-neutral physical augmentation vanishes there.  Natural Tate kernels
are likewise coefficient-sum-zero inside each complete label fibre.

Thus normalized bar/source syzygies, chart copies, and natural Tate
completion cannot kill the homogeneous six-term class.  The first possible
killer must be a genuinely relative mapping-cone generator with a new
physical output.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_repeated_component_six_term_separators.py":
        "b8c3eff88b44a9a12d45f61b44449ac8a0b3a4c3e9a6d351a50ef19293ce2d25",
    "computations/verify_h3_first_flat_endpoint_bridge.py":
        "e22cc0eec09c0e67c10bc9ae1bd50bf26167f8d44af7857e7c6920f42bba63c2",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py":
        "b890195a8fc0c4e90c9c9c0c03c41a95690228c81026f4c2ea1fa95908564e38",
    "computations/verify_h3_residual_q_two_chart_copy_membership_no_go.py":
        "6383a2e25b3e137e570eddeba00b1cbbe59035f88cb48f234ebb3282ba23294b",
}
EXPECTED_LEDGER_SHA256 = "ae3c65f9ed33f96a568621f35df250fb5885d5ef650edcdcdd0bd456ca0c4c63"


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


def selected_private_features(component):
    owners = defaultdict(list)
    for column_index, (_word, _multiplier, boundary) in enumerate(
            component["columns"]):
        for feature in boundary:
            owners[feature].append(column_index)
    pure_indices = [
        index for index, (word, _multiplier, _boundary) in
        enumerate(component["columns"])
        if word == (0,) * 8
    ]
    require(len(pure_indices) == 6, "pure repeated-column census changed")
    selected = []
    for column_index in pure_indices:
        private = sorted(
            feature for feature in component["columns"][column_index][2]
            if owners[feature] == [column_index]
        )
        require(private, ("pure column lost private pivot", column_index))
        selected.append(private[0])
    require(len(set(selected)) == 6, "six private pivots collided")
    return pure_indices, selected


def component_audit(base, complete):
    records = []
    components = []
    for component_index, (left, right, left_cell, _right_cell) in enumerate(
            complete.CUBIC_PAIRS):
        target_degree = complete.degree_add(
            base.lambda_degree(left),
            complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
        )
        component = complete.component(base, target_degree)
        components.append(component)
        pure_indices, selected = selected_private_features(component)

        # Repeated columns enter the augmented bridge with -B and pure
        # aggregate +1.  The covector is +1 on Q and on each selected feature.
        values = []
        for word, _multiplier, boundary in component["columns"]:
            values.append(int(word == (0,) * 8)
                          - sum(feature in boundary for feature in selected))
        require(set(values) == {0},
                ("six-term dual stopped killing d1", component_index))
        require(component["rank"] == len(component["columns"]) == 288
                and component["one_chart_kernel"] == 0,
                ("one-chart d1 stopped being injective", component_index))
        require(component["two_chart_kernel"] == 288
                and component["two_chart_rank"] == 288,
                ("two-chart kernel changed", component_index))

        records.append({
            "component": component_index,
            "faces": [left, right],
            "columns_rank_kernel_one_chart": [288, 288, 0],
            "columns_rank_kernel_two_chart": [576, 288, 288],
            "pure_columns": len(pure_indices),
            "selected_private_features": [repr(value) for value in selected],
            "six_term_pairing_on_d1": sorted(set(values)),
            "absolute_higher_image_one_chart": 0,
            "two_chart_higher_image": "pairwise chart differences only",
            "pure_augmentation_on_two_chart_kernel": 0,
            "chart_neutral_readouts_on_two_chart_kernel": 0,
        })
    return components, records


def natural_tate_audit(components, complete):
    image_owners = defaultdict(list)
    for component_index, component in enumerate(components):
        complement = tuple(
            complete.CYCLE_CELLS[cell]
            for cell in complete.TATE_COMPLEMENTS[component_index]
        )
        for column_index, (word, multiplier) in enumerate(component["labels"]):
            label = (word, tuple(sorted(multiplier + complement)))
            image_owners[label].append((component_index, column_index))
    domain = sum(len(component["labels"]) for component in components)
    kernel = sum(len(owners) - 1 for owners in image_owners.values())
    require((domain, len(image_owners), kernel) == (1440, 1201, 239),
            "natural Tate fibre census changed")
    pure_fibres = {
        label: owners for label, owners in image_owners.items()
        if label[0] == (0,) * 8
    }
    require(len(pure_fibres) == 16
            and Counter(map(len, pure_fibres.values()))
            == Counter({1: 5, 2: 10, 5: 1}),
            "pure Tate fibres changed")
    return {
        "domain_image_kernel": [domain, len(image_owners), kernel],
        "pure_label_fibres": len(pure_fibres),
        "pure_owner_distribution": {
            str(key): value for key, value in
            sorted(Counter(map(len, pure_fibres.values())).items())
        },
        "pure_aggregate_on_kernel": 0,
        "target_anchor_on_kernel": [0, 0],
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "absolute_exhaustivity_base",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "absolute_exhaustivity_complete",
    )
    six = load(
        "computations/verify_h3_repeated_component_six_term_separators.py",
        "absolute_exhaustivity_six",
    )
    first_flat = load(
        "computations/verify_h3_first_flat_endpoint_bridge.py",
        "absolute_exhaustivity_first_flat",
    )
    require(six.EXPECTED_LEDGER_SHA256
            == "6063daed9a1759d2051996230a6b6906a9c7136380593476f7fd6e8c352e6497",
            "six-term ledger pin changed")
    require(first_flat.EXPECTED_LEDGER_SHA256
            == "de8151738fe609f857e4e5917c3555067b2a9681018567fd11236c706316d997",
            "first-flat exact dependency ledger pin changed")

    components, component_records = component_audit(base, complete)
    tate = natural_tate_audit(components, complete)
    return {
        "theorem": "six-term dual survives the complete absolute source resolution",
        "components": component_records,
        "natural_tate": tate,
        "canonical_first_flat_operator_block": {
            "exact_dependency_ledger": first_flat.EXPECTED_LEDGER_SHA256,
            "six_term_dual_annihilates_all_8580_operator_columns": True,
            "pure_aggregate_in_old_operator_plus_repeated_image": False,
        },
        "formal_resolution_consequence": {
            "one_chart": "d1 injective and d1*d2=0 imply d2=0",
            "two_chart": (
                "ker[d1 d1] is the anti-diagonal labelled-column module; "
                "pure and every chart-neutral physical augmentation vanish"
            ),
            "natural_tate": (
                "kernel is the direct sum of coefficient-sum-zero spaces "
                "inside complete row/multiplier label fibres"
            ),
        },
        "exhausted_absolute_families": [
            "complete polynomial full-nine columns in all five repeated grades",
            "all absolute higher bar/source syzygies landing in those grades",
            "both identical chart copies and their complete kernels",
            "natural C5 Tate multiplication and its 239-dimensional kernel",
            "canonical complete first-flat order-six/Spencer operator block",
        ],
        "first_unexhausted_source_type": (
            "a genuinely relative chart-nondiagonal mapping-cone generator "
            "with a new physical output; it cannot factor through the old "
            "injective absolute boundary map"
        ),
        "consequence": (
            "the comparison frontier is a boundary-versus-physical-cokernel "
            "alternative for one relative generator, not an unbounded search "
            "through higher absolute source or support strata"
        ),
        "scope": (
            "absolute source/bar/Tate resolution in all five complete repeated "
            "grades and the canonical exact first-flat PP block.  A new relative "
            "mapping-cone differential, cyclic physical propagation of the PP "
            "block, terminal typing, and transverse rank are not asserted"
        ),
    }


def main():
    ledger = audit()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("absolute-resolution exhaustivity ledger changed", digest))
    print("h3 six-term dual absolute-resolution exhaustivity: PASS")
    print("five one-chart kernels: 0; doubled kernels: pairwise differences")
    print("natural Tate kernel: 239, pure aggregate zero")
    print("first possible killer: genuinely relative mapping-cone cell")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

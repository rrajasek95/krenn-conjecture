#!/usr/bin/env python3
"""Construct the five homogeneous six-term repeated-component duals.

Each rootless C5 repeated ``P3+K2`` component has six pure-word
row/multiplier columns.  The complete literal boundary audit gives each
column private matching features.  Selecting one private feature per pure
column makes the pure aggregate factor through six physical boundary
coordinates with integral coefficients.  This checker constructs that dual
in all five components, proves the five fine grades are distinct, and tests
the physical diagonal stabilizer fields which killed the earlier coarse
Omega aggregate.

The canonical faces-(3,5) dual is the one appearing in the exact first-flat
order-six bridge theorem.  Cyclic physical propagation of the order-six
comparison is not asserted here; the other four records are the exact
componentwise Fredholm candidates waiting for that propagation.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_first_flat_endpoint_bridge.py":
        "e22cc0eec09c0e67c10bc9ae1bd50bf26167f8d44af7857e7c6920f42bba63c2",
    "computations/verify_h3_order6_covariance_bridge_cyclic_aggregate.py":
        "01d4d504c0d5d9ac8fd643e06a38b35d75962c859e41908bff3161d10c7cbc13",
    "computations/verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py":
        "a98c6e0e90127e81e869c68342f3999abbbd8898d2b2eeafbeccbad06575a324",
}
EXPECTED_LEDGER_SHA256 = "6063daed9a1759d2051996230a6b6906a9c7136380593476f7fd6e8c352e6497"


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


def degree(monomial):
    return tuple(local_count(monomial, site, colour)
                 for site in range(8) for colour in range(3))


def stabilizer_fields():
    return {
        **{f"eta_p0_minus_{site}0": ((6, 0, 1), (site, 0, -1))
           for site in range(1, 6)},
        **{f"left_x0_minus_{site}0": ((0, 0, 1), (site, 0, -1))
           for site in range(1, 6)},
        "external_p2_minus_x2": ((6, 2, 1), (0, 2, -1)),
        "external_x0_minus_p0": ((0, 0, 1), (6, 0, -1)),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "six_term_base",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "six_term_complete",
    )

    records = []
    target_degrees = []
    for component_index, (left, right, left_cell, _right_cell) in enumerate(
            complete.CUBIC_PAIRS):
        target_degree = complete.degree_add(
            base.lambda_degree(left),
            complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
        )
        target_degrees.append(target_degree)
        component = complete.component(base, target_degree)
        owners = defaultdict(list)
        for column_index, (_word, _multiplier, boundary) in enumerate(
                component["columns"]):
            for feature in boundary:
                owners[feature].append(column_index)
        pure_indices = [
            index for index, (word, _multiplier, _boundary) in
            enumerate(component["columns"])
            if word == complete.PURE_WORD
        ]
        require(len(pure_indices) == 6,
                ("pure repeated columns changed", component_index))
        selected = []
        for column_index in pure_indices:
            boundary = component["columns"][column_index][2]
            private = sorted(feature for feature in boundary
                             if owners[feature] == [column_index])
            require(private, ("pure column lost private feature",
                              component_index, column_index))
            selected.append(private[0])
        require(len(set(selected)) == 6,
                ("selected private features collided", component_index))

        # In the augmented sign convention the repeated boundary is
        # -boundary and the pure aggregate is +1.  Hence
        # Q + sum(selected feature rows)=0 on every column.
        pairings = []
        for column_index, (word, _multiplier, boundary) in enumerate(
                component["columns"]):
            value = int(word == complete.PURE_WORD)
            value -= sum(feature in boundary for feature in selected)
            pairings.append(value)
        require(set(pairings) == {0},
                ("six-term dual stopped killing the component",
                 component_index))

        degrees = {degree(feature) for feature in selected}
        require(degrees == {target_degree},
                ("six-term dual lost its repeated fine grade",
                 component_index, degrees))
        weights = {}
        for label, field in stabilizer_fields().items():
            values = tuple(sum(
                weight * local_count(feature, site, colour)
                for site, colour, weight in field
            ) for feature in selected)
            require(set(values) == {0},
                    ("six-term dual sees physical stabilizer",
                     component_index, label, values))
            weights[label] = list(values)

        records.append({
            "component": component_index,
            "faces": [left, right],
            "columns": len(component["columns"]),
            "pure_columns": len(pure_indices),
            "selected_private_features": [repr(value) for value in selected],
            "selected_feature_owner_counts": [len(owners[value])
                                               for value in selected],
            "integral_dual": "pure_aggregate + sum_6 signed boundary features",
            "dual_pairing_on_all_columns": sorted(set(pairings)),
            "fine_degree": list(target_degree),
            "known_physical_stabilizer_weights": weights,
        })

    require(len(set(target_degrees)) == 5,
            "five repeated-component separator grades collided")
    face_pairs = [tuple(record["faces"]) for record in records]
    require(face_pairs == [(1, 3), (3, 5), (5, 2), (2, 4), (4, 1)],
            ("C5 face order changed", face_pairs))

    return {
        "theorem": "five homogeneous six-term repeated-component duals",
        "face_order": face_pairs,
        "records": records,
        "five_distinct_fine_grades": True,
        "formal_face_pairing_matrix": "I_5 after primitive normalization",
        "canonical_order6_bridge_component": 1,
        "canonical_order6_dual_proved_by": "94b027d",
        "remaining_physical_step": (
            "transport the canonical physical comparison through the four "
            "cyclic faces or construct the relative cell; componentwise "
            "old-source and known-stabilizer obstructions are already killed"
        ),
        "scope": (
            "complete old repeated full-nine boundary in all five cubic "
            "grades and the listed physical diagonal stabilizers.  Only the "
            "canonical faces-(3,5) dual is yet checked against the exact "
            "first-flat order-six operator block; no exhaustive relative-cone "
            "or transverse-rank conclusion"
        ),
    }


def main():
    ledger = audit()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("six-term separator ledger changed", digest))
    print("h3 repeated-component six-term separators: PASS")
    print("five components; six private features each; formal pairing I5")
    print("known eta/left/external stabilizer weights: zero")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Separate the endpoint-even Gate-II cap problem from the odd PSQJet lane.

The six AugP2 cells have twelve ordered P/S parent candidates.  Endpoint
forgetting has a six-dimensional odd kernel, but the Gate-II packet belongs
to the endpoint-even summand: chi_w, R01, L01, its paired first-PP boundary,
U_C4 and the 0102 private carrier are all fixed by endpoint reversal.  Over
Q the Reynolds operator (1+s)/2 is a chain section, so no absolute odd
PSQJet is required for this packet.

This removes only the endpoint-orientation debt.  Retaining operation, Eq
and target labels leaves the response/cap boundary separator (1,-1), the two
root Hom characters, and the two mixed-target normals.  Equivalently, the
current cap data do not yet make r0 a cyclic module over the complete
trigger/divided-Hasse operator algebra: the Eq and target relations in the
annihilator of the response generator do not act trivially at r0.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_augp2_six_cell_parent_augmentation_gate.py":
        "26259bb67476a30c4237c20f8e393ec919e934f95bab0d0c6845adc9295c3132",
    "computations/verify_h3_psqjet01_divided_hasse_relative_dga_gate.py":
        "35ff02f00b3babe7710319f184894681a08d6c035435be949eccb2579aa8d978",
    "computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py":
        "6f791c41e743a94279ccf9e4924af11a42c278baa7737a5eed108bf85136f499",
    "computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py":
        "d5628f66ffbf94e2de37318ab136adda96af5e114e2bea8dce22542ec9f30cb1",
    "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py":
        "59babf6e706973f2eaa8a8fdd7cdb624ddf88560c08243c5fcd05c3a5425a5d7",
    "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py":
        "01e36f89b4df4bb020607d2f00871deb96775a7e58b42e85eaef76c20097e5cf",
}
NOTE_PINS = {
    "notes/h2-p2-0102-private-parity-reinsertion-gate.md":
        "endpoint-even",
    "notes/h3-gate-ii-psidelta-same-grade-extension-chain.md":
        "labelled endpoint-even Spencer face",
    "notes/h3-h2-chart-scalar-capped-c4-augmented-gate.md":
        "U_C4[D,Q01;2345]",
}
EXPECTED_LEDGER_SHA256 = (
    "36c37bb5fbc5c736f75711412f28f245538d94d6c03fa2ba739c788324285dcc"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    for relative, phrase in NOTE_PINS.items():
        require(phrase in (ROOT / relative).read_text(),
                ("scope phrase changed", relative, phrase))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def permute(vector: tuple[Q, ...], permutation: tuple[int, ...]) \
        -> tuple[Q, ...]:
    return tuple(vector[index] for index in permutation)


def endpoint_character_and_packet_audit(character_gate, curvature_gate) \
        -> dict[str, object]:
    character = character_gate.character_audit()
    root_only = tuple(map(Q,
        character["characters"]["root_only_missing"]))
    endpoint_only = tuple(map(Q,
        character["characters"]["endpoint_only_granted"]))
    mixed = tuple(map(Q,
        character["characters"]["endpoint_odd_Cartan_mixed"]))

    # Corner order 1,w,s,sw.  Left multiplication by s exchanges 1<->s
    # and w<->sw.
    endpoint_swap = (2, 3, 0, 1)
    require(permute(root_only, endpoint_swap) == root_only
            and permute(endpoint_only, endpoint_swap) == tuple(-x for x in endpoint_only)
            and permute(mixed, endpoint_swap) == tuple(-x for x in mixed),
            "endpoint character eigenvalues changed")

    # Local coefficient order A,B,C; endpoint reversal exchanges B and C.
    swap_bc = (0, 2, 1)
    r01 = tuple(map(Q, (1, 1, 1)))
    l01 = tuple(map(Q, (2, -1, -1)))
    bc_cap = tuple(map(Q, (0, 1, 1)))
    b_minus_c = tuple(map(Q, (0, 1, -1)))
    require(all(permute(vector, swap_bc) == vector
                for vector in (r01, l01, bc_cap))
            and permute(b_minus_c, swap_bc) == tuple(-x for x in b_minus_c),
            "local Gate-II endpoint parity changed")

    # Check the literal 18 direction-factor labels.  Reversal 0<->1 fixes
    # the A=D*q01 direction and exchanges the B,C directions: there are six
    # fixed labels and six nontrivial pairs, and dL01 is invariant labelwise.
    (_matchings, _directions, _tails, l01_values,
     _r01_values, _ah_values) = curvature_gate.polynomial_data()
    d_l01 = curvature_gate.differential(l01_values)
    selected_sites = {0, 1, 6, 7}
    direction_half = {
        label: value for label, value in d_l01.items()
        if set(label[1]).issubset(selected_sites)
    }

    def swap_edge(edge):
        vertex = {0: 1, 1: 0}
        return tuple(sorted((vertex.get(edge[0], edge[0]),
                             vertex.get(edge[1], edge[1]))))

    def swap_label(label):
        matching, edge = label
        return (tuple(sorted(swap_edge(item) for item in matching)),
                swap_edge(edge))

    fixed = sum(swap_label(label) == label for label in direction_half)
    nontrivial_orbits = (len(direction_half) - fixed) // 2
    require(len(direction_half) == 18 and fixed == 6
            and nontrivial_orbits == 6
            and all(direction_half.get(swap_label(label)) == value
                    for label, value in direction_half.items()),
            "the literal 18-face reversal action changed")
    return {
        "endpoint_reversal": "s: (1,w,s,sw)->(s,sw,1,w)",
        "chi_w_eigenvalue": 1,
        "chi_ws_eigenvalue": -1,
        "local_swap": "B<->C, A fixed",
        "R01_endpoint_even": True,
        "L01_equals_2A_minus_B_minus_C_endpoint_even": True,
        "balanced_B_plus_C_cap_shadow_endpoint_even": True,
        "U_C4_fixed_window_endpoint_even": True,
        "dL01_direction_faces": {
            "literal_faces": 18,
            "fixed_labels": fixed,
            "nontrivial_endpoint_reversal_pairs": nontrivial_orbits,
            "literal_weighted_packet_endpoint_even": True,
        },
        "word_0102_private_and_dq_reinsertion_endpoint_even": True,
        "Gate_II_packet_requires_endpoint_odd_data": False,
    }


def reynolds_section_audit(cap_gate, psq_gate) -> dict[str, object]:
    cap_ledger, cap_digest = cap_gate.audit()
    require(cap_digest == cap_gate.EXPECTED_LEDGER_SHA256, cap_digest)
    parent = cap_ledger["literal_parent_candidates"]
    require(parent["ordered_parent_candidates"] == 12
            and parent["endpoint_forgetting_rank"] == 6
            and parent["endpoint_odd_kernel_dimension"] == 6,
            parent)

    # Coordinates are M_0^+,M_0^-,...,M_5^+,M_5^-.  q forgets orientation;
    # j is the Reynolds half-sum.  q*j=1, s*j=j and every odd difference is
    # killed.  Among sections alpha M+ +(1-alpha)M-, s-equivariance forces
    # alpha=1/2 independently in all six blocks.
    quotient = tuple(
        tuple(Q(position in (2 * index, 2 * index + 1))
              for position in range(12))
        for index in range(6)
    )
    section = tuple(
        tuple(Q(1, 2) if position in (2 * index, 2 * index + 1) else Q(0)
              for position in range(12))
        for index in range(6)
    )
    odd = tuple(
        tuple(Q(position == 2 * index) - Q(position == 2 * index + 1)
              for position in range(12))
        for index in range(6)
    )
    endpoint_swap = tuple(index ^ 1 for index in range(12))
    composite = tuple(tuple(dot(qrow, scol) for scol in section)
                      for qrow in quotient)
    identity = tuple(tuple(Q(row == column) for column in range(6))
                     for row in range(6))
    require(composite == identity
            and all(permute(column, endpoint_swap) == column
                    for column in section)
            and all(dot(kernel, column) == 0
                    for kernel in odd for column in section)
            and rank(section) == rank(odd) == 6,
            "the endpoint Reynolds splitting changed")

    physical = psq_gate.physical_psqjet_product_rule_audit()
    relative = psq_gate.relative_kahler_totalization_audit()
    residual = relative["after_granting_all_six_endpoint_pairs"]
    require(physical["top_type"] == "endpoint-odd P4+2K2"
            and relative["rank_after_relative_PSQJet"]
                == relative["relative_graph_even_rank"] == 45
            and relative["rank_after_absolute_PSQJet"] == 46
            and residual["rank_before_after_absolute_jet"] == [51, 52]
            and residual["normalized_dual_on_relative_and_absolute"]
                == {"relative_jet": "0", "absolute_jet": "1"},
            (physical, relative))
    return {
        "ordered_parent_coordinates": 12,
        "endpoint_even_parent_quotient_dimension": 6,
        "endpoint_odd_kernel_dimension": 6,
        "Reynolds_section": "j([M])=(M+sM)/2",
        "quotient_after_section_is_identity": True,
        "section_is_endpoint_swap_equivariant": True,
        "unique_equivariant_block_coefficient": "1/2",
        "physical_chain_status": (
            "a literal Q-linear chain section in the endpoint-even category; "
            "it is not a choice of one ordered parent basis element"
        ),
        "PSQJet_01_endpoint_parity": "odd",
        "PSQJet_01_Reynolds_projection": 0,
        "relative_PSQJet_rank_before_after": [45, 45],
        "hypothetical_absolute_odd_PSQJet_rank_before_after": [45, 46],
        "consequence": (
            "the missing absolute odd PSQJet is required only to lift back "
            "to a termwise ordered P/S parent; it is irrelevant to the "
            "endpoint-even Gate-II comparison"
        ),
    }


def operator_module_residual_audit(cap_gate, lower_gate) -> dict[str, object]:
    cap_ledger, cap_digest = cap_gate.audit()
    require(cap_digest == cap_gate.EXPECTED_LEDGER_SHA256, cap_digest)
    boundary = cap_ledger["word_root_paths_and_first_chain_boundary"]
    require(boundary["missing_root_Hom_dimension"] == 2
            and boundary["generated_Hom_response_cap"] == 0
            and boundary["dG0"] == [1, 0]
            and boundary["dr0"] == [0, 1]
            and boundary["primitive_boundary_separator"] == [1, -1],
            boundary)

    lower_ledger, lower_digest = lower_gate.audit()
    require(lower_digest == lower_gate.EXPECTED_LEDGER_SHA256, lower_digest)
    target = lower_ledger["physical_target_gate"]
    require(target["rank_local_diagonal_lines"] == 2
            and target["rank_after_two_mixed_normals"] == 4
            and target["mixed_target_cokernel_rank"] == 2
            and not target["combined_sigma_even_normal_zero"],
            target)

    response_boundary = (Q(1), Q(0))
    cap_boundary = (Q(0), Q(1))
    separator = (Q(1), Q(-1))
    require(dot(separator, response_boundary) == 1
            and dot(separator, cap_boundary) == -1
            and rank((response_boundary, cap_boundary)) == 2,
            "the protected Eq separator changed")
    return {
        "cyclic_operator_module_test": (
            "an A-linear map A*e_R -> C with e_R->r0 exists only if every "
            "full-star/trigger relation annihilating e_R also annihilates r0"
        ),
        "endpoint_even_coefficient_A_action": "constructed by Reynolds splitting",
        "full_trigger_divided_Hasse_A_action_on_cap": "not constructed",
        "PSQJet_supplies_missing_even_A_action": False,
        "root_operation_stage": {
            "existing_corner": boundary["existing_operation_corner"],
            "generated_Hom_response_cap": 0,
            "surviving_covectors": boundary["root_Hom_covectors"],
        },
        "first_protected_annihilator_violation": {
            "coordinates": ["(H-u)_response", "(H-u)_Eq_cap"],
            "dG0": [1, 0],
            "dr0": [0, 1],
            "primitive_covector": [1, -1],
            "cokernel_rank": 1,
        },
        "next_protected_annihilator_violations": {
            "local_diagonal_rank": 2,
            "rank_with_mixed_target_normals": 4,
            "cokernel_rank": 2,
            "covectors": ["X_00211122^*", "X_00111222^*"],
            "pairing_matrix": [[2, 0], [0, 2]],
            "sigma_even_sum_survives": True,
        },
        "A_linear_epsilon_C_exists_in_current_inventory": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    cap_gate = load(
        "computations/verify_h3_augp2_six_cell_parent_augmentation_gate.py",
        "gate_ii_even_cap_parent",
    )
    psq_gate = load(
        "computations/verify_h3_psqjet01_divided_hasse_relative_dga_gate.py",
        "gate_ii_even_psq",
    )
    character_gate = load(
        "computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py",
        "gate_ii_even_character",
    )
    curvature_gate = load(
        "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py",
        "gate_ii_even_curvature",
    )
    lower_gate = load(
        "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py",
        "gate_ii_even_lower_target",
    )
    ledger = {
        "theorem": "h3 Gate-II endpoint-even cap/operator-module gate",
        "pins": PINS,
        "desired_packet_parity":
            endpoint_character_and_packet_audit(character_gate, curvature_gate),
        "six_parent_reynolds_section":
            reynolds_section_audit(cap_gate, psq_gate),
        "operator_module_residual":
            operator_module_residual_audit(cap_gate, lower_gate),
        "verdict": (
            "PAComp/Gate-II only needs the endpoint-even quotient.  The "
            "canonical half-sum of each P/S-reversed parent pair is therefore "
            "a legitimate rational chain section, and the six odd kernel "
            "directions and missing absolute PSQJet are irrelevant.  This "
            "does not construct the cap comparison: the AB/AC operation Hom "
            "characters remain absent, and after granting them the first "
            "protected failure is (H-u)_response versus (H-u)_Eq_cap, "
            "detected by (1,-1), followed by the two mixed-target normals"
        ),
        "shortest_positive_datum": (
            "one endpoint-even, two-root A-module cap action sending the "
            "response cyclic generator to r0 and killing the Eq separator "
            "(1,-1); its next two faces must realize the sigma-paired target "
            "normals X_00211122^* and X_00111222^*.  No endpoint-odd filler "
            "is part of this datum"
        ),
        "scope": (
            "exact over Q for the six AugP2 parent pairs, V4 endpoint/root "
            "characters, paired 18-face boundary, protected Eq ledger, and "
            "two-cut target ledger.  It does not assert a termwise ordered "
            "P/S augmentation or construct the missing AB/AC A-action"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("endpoint-even cap ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    if arguments.mode == "structural":
        pin_dependencies()
        print("h3 Gate-II endpoint-even cap structural gate: PASS")
        return
    ledger, digest = audit()
    if arguments.mode == "exhaustive":
        # All 2^6 termwise endpoint choices have the same even projection.
        for mask in range(1 << 6):
            for block in range(6):
                chosen = tuple(Q(position == 2 * block + ((mask >> block) & 1))
                               for position in range(12))
                swapped = tuple(chosen[index ^ 1] for index in range(12))
                projected = tuple((left + right) / 2
                                  for left, right in
                                  zip(chosen, swapped, strict=True))
                expected = tuple(
                    Q(1, 2) if position in (2 * block, 2 * block + 1)
                    else Q(0)
                    for position in range(12)
                )
                require(projected == expected,
                        ("Reynolds enumeration", mask, block))
    if arguments.json:
        print(json.dumps({"ledger": ledger, "sha256": digest},
                         indent=2, sort_keys=True))
    else:
        residual = ledger["operator_module_residual"]
        print("h3 Gate-II endpoint-even cap/operator-module gate: PASS")
        print("endpoint-odd parent debt: DISMISSED IN EVEN QUOTIENT")
        print("first protected residual:",
              residual["first_protected_annihilator_violation"]
                  ["primitive_covector"])
        print("mixed-target residual rank:",
              residual["next_protected_annihilator_violations"]
                  ["cokernel_rank"])
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

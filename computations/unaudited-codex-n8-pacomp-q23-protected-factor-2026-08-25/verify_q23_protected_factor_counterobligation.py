#!/usr/bin/env python3
"""Trace Q23-PROTECTED-FACTOR to its first unmatched labelled term.

This is a bounded exact-symbolic checker.  It does not search for a new
operation.  It expands the two intrinsic q23 composites on every marked
q23 descendant, extracts the canonical selected branch, carries its B1
augmentation to the hidden (lower, Eq, ores) rows, cancels the strongest
pinned endpoint inventory, and reports the first remaining coordinate.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "computations/verify_h3_eqsystem_divided_root_restriction_chain_commutator_intrinsic_gate.py":
        "6db24fc6c3f5bb42c7e30185e4887d4a06758154730de0e7c734f131725504be",
    "computations/verify_h3_divided_root_marked_deletion_p2_naturality.py":
        "fd90cee45e302193bc1cc38f23d643818761451c26064001f3eef1d966ab11b8",
    "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py":
        "01e36f89b4df4bb020607d2f00871deb96775a7e58b42e85eaef76c20097e5cf",
    "computations/verify_h3_cplus_hidden_debt_cartan_mv_root_bar_span.py":
        "7eef9d440fefbae174d2adc61b6f8bdc270351353884ba24e277d36714a9a364",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py":
        "8be3bc5bf85f8d633e77e2a0bdd18aea6d481c81f5fb6a6a947cbaf82f862302",
}

SELECTED_PARENT = ((0, 1), (2, 3), (4, 5), (6, 7))
SELECTED_BRANCH = ((0, 7), (2, 3), (4, 5), (6, 7))
Q23 = (2, 3)
Q45 = (4, 5)
SITE_SIGMA = (0, 1, 5, 4, 3, 2, 6, 7)
ROOT_SIGMA = (1, 0, 3, 2)
PURE_SIGMA = (5, 4, 0, 2, 1, 3)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_inputs() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(value, vector):
    return tuple(Q(value) * Q(entry) for entry in vector)


def unit(width: int, index: int):
    return tuple(Q(position == index) for position in range(width))


def rank(columns) -> int:
    columns = tuple(columns)
    if not columns:
        return 0
    height = len(columns[0])
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(height):
            if row == pivot_row or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right
                         for left, right in zip(rows[row], rows[pivot_row],
                                                strict=True)]
        pivot_row += 1
    return pivot_row


def move_decorated_cell(cell, permutation):
    left, right, left_colour, right_colour = cell
    moved_left, moved_right = permutation[left], permutation[right]
    if moved_left < moved_right:
        return moved_left, moved_right, left_colour, right_colour
    return moved_right, moved_left, right_colour, left_colour


def move_decorated_monomial(monomial, permutation):
    return tuple(sorted(move_decorated_cell(cell, permutation)
                        for cell in monomial))


def serialize_monomial(monomial):
    return [list(cell) for cell in monomial]


def audit():
    pin_inputs()
    intrinsic = load(
        "computations/verify_h3_eqsystem_divided_root_restriction_chain_commutator_intrinsic_gate.py",
        "q23_intrinsic",
    )
    marked = load(
        "computations/verify_h3_divided_root_marked_deletion_p2_naturality.py",
        "q23_marked",
    )
    lower = load(
        "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py",
        "q23_lower",
    )
    hidden = load(
        "computations/verify_h3_cplus_hidden_debt_cartan_mv_root_bar_span.py",
        "q23_hidden",
    )
    comparison = load(
        "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py",
        "q23_comparison",
    )
    sections = load(
        "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py",
        "q23_sections",
    )

    # The existing literal operation algebra has no response-to-cap corner.
    operation = comparison.literal_idempotent_hom_audit()
    section_quotient = sections.literal_two_root_section_audit()
    require(operation["Hom_degree0_response_to_cap_in_current_grammar"] == 0
            and section_quotient["cokernel_dimension_before_sections"] == 2,
            (operation, section_quotient))

    # Expand both intrinsic composites on every marked q23 descendant.
    q23_descendants = []
    for _parent_index, parent, missing, doubled, branch in marked.branches():
        if Q23 not in branch:
            continue
        source = intrinsic.decorated_monomial(intrinsic.RESPONSE_WORD, branch)
        target = intrinsic.decorated_monomial(intrinsic.CAP_WORD, branch)
        left = intrinsic.o_b_after_d(source, Q23)
        right = intrinsic.d_after_o_e(source, Q23)
        require(left == right == Counter({target: Q(1)}),
                ("q23 intrinsic term mismatch", parent, missing, doubled,
                 branch, left, right))
        q23_descendants.append((parent, missing, doubled, branch))
    require(len(q23_descendants) == 90, len(q23_descendants))

    selected = next(row for row in q23_descendants
                    if row[0] == SELECTED_PARENT and row[3] == SELECTED_BRANCH)
    _parent, missing, doubled, branch = selected
    source_top = intrinsic.decorated_monomial(intrinsic.RESPONSE_WORD, branch)
    target_top = intrinsic.decorated_monomial(intrinsic.CAP_WORD, branch)
    source_q = intrinsic.decorated_cell(intrinsic.RESPONSE_WORD, Q23)
    target_q = intrinsic.decorated_cell(intrinsic.CAP_WORD, Q23)
    source_lower = tuple(cell for cell in source_top if cell != source_q)
    target_lower = tuple(cell for cell in target_top if cell != target_q)
    root_orders = {
        str(site): intrinsic.site_multiplicity(source_lower, site)
        for site in intrinsic.CHANGED
    }
    require((missing, doubled) == (1, 7)
            and root_orders == {"0": 1, "2": 0, "4": 1,
                                "5": 1, "6": 1, "7": 2},
            (missing, doubled, root_orders))
    require(intrinsic.apply_divided_roots(
                Counter({source_lower: Q(1)}), intrinsic.CHANGED)
            == Counter({target_lower: Q(1)}),
            (source_lower, target_lower))

    # The pinned lower quotient canonically names this marked face B1.
    iota = lower.coefficient_iota_audit()
    q23_label = iota["cut_maps"][0]
    require(q23_label["cut"] == "0112/q23:21"
            and q23_label["marked_hole_image"] == "B1",
            q23_label)
    c1 = add(scale(6, unit(6, 1)), scale(-1, (Q(1),) * 6))
    cut23_image = scale(Q(1, 8), c1)

    # Split the pinned root-even debt E=D_root tensor (B1+B4) cutwise.
    b1, b4 = unit(6, 1), unit(6, 4)
    e23 = hidden.tensor(hidden.D_ROOT, b1)
    e45 = hidden.tensor(hidden.D_ROOT, b4)
    combined = scale(2, hidden.tensor(hidden.D_ROOT, hidden.V))
    require(combined == add(e23, e45), (combined, e23, e45))

    h23 = hidden.vector(lower=scale(-1, e23), ores=e23)
    m23 = hidden.vector(lower=e23, eq=e23)
    k23 = hidden.vector(ores=e23)
    c_eq23 = hidden.vector(eq=e23)
    require(h23 == add(scale(-1, m23), k23, c_eq23),
            "q23 hidden decomposition changed")

    # Grant arbitrary tied M_u and arbitrary residue K_u, plus every pinned
    # root/cut endpoint bar.  This is stronger than the physical inventory.
    grant = []
    for index in range(hidden.N):
        basis = unit(hidden.N, index)
        grant.append(hidden.vector(lower=basis, eq=basis))
        grant.append(hidden.vector(ores=basis))
    bars = []
    for endpoint in grant:
        moved = hidden.vector(
            lower=hidden.permute_label_vector(
                endpoint[hidden.LOWER], ROOT_SIGMA, PURE_SIGMA),
            eq=hidden.permute_label_vector(
                endpoint[hidden.EQ], ROOT_SIGMA, PURE_SIGMA),
            ores=hidden.permute_label_vector(
                endpoint[hidden.ORES], ROOT_SIGMA, PURE_SIGMA),
        )
        bars.append(add(moved, scale(-1, endpoint)))
    grant_rank = rank(grant + bars)
    require(grant_rank == 48
            and rank(grant + bars + [c_eq23]) == 49,
            (grant_rank, rank(grant + bars + [c_eq23])))

    # List the exact unmatched Eq-only entries; lexicographically first is
    # root word 0, B1, coefficient -1.
    unmatched = []
    for root in range(4):
        index = root * 6 + 1
        coefficient = c_eq23[hidden.EQ.start + index]
        if coefficient:
            unmatched.append({
                "root_word_index": root,
                "pure_label": "B1",
                "protected_row": "Eq",
                "coefficient": str(coefficient),
                "lower": "0",
                "ores": "0",
            })
    require([row["coefficient"] for row in unmatched]
            == ["-1", "1", "-1", "1"], unmatched)

    first_index = 1
    first_dual = hidden.vector(
        lower=unit(hidden.N, first_index),
        eq=scale(-1, unit(hidden.N, first_index)),
    )
    require(all(hidden.dot(first_dual, column) == 0
                for column in grant + bars)
            and hidden.dot(first_dual, c_eq23) == 1,
            "first q23 unmatched dual changed")

    # Site-level q23->q45 transport is monic.  At the root/pure-labelled
    # hidden level, the pinned root permutation reverses D_root while the
    # pure-label transition swaps B1 and B4, hence sigma(E23)=-E45.
    q45_lower = tuple(cell for cell in target_top
                      if cell != intrinsic.decorated_cell(
                          intrinsic.CAP_WORD, Q45))
    require(move_decorated_monomial(target_lower, SITE_SIGMA) == q45_lower,
            (target_lower, q45_lower))
    moved_e23 = hidden.permute_label_vector(e23, ROOT_SIGMA, PURE_SIGMA)
    require(moved_e23 == scale(-1, e45), (moved_e23, e45))

    result = {
        "schema": "q23-protected-factor-counterobligation-v1",
        "status": "PASS_FIRST_UNMATCHED_TERM_NOT_A_PROOF_OF_FACTOR",
        "pins": PINS,
        "existing_operation_corner": {
            "generated_e_C_A_e_R_dimension": 0,
            "missing_root_labelled_section_dimension": 2,
        },
        "intrinsic_q23": {
            "marked_descendants_checked": len(q23_descendants),
            "selected_parent": "01|23|45|67",
            "selected_branch": "07|23|45|67",
            "source_top": serialize_monomial(source_top),
            "target_top": serialize_monomial(target_top),
            "source_q23_cell": list(source_q),
            "target_q23_cell": list(target_q),
            "source_lower": serialize_monomial(source_lower),
            "target_lower": serialize_monomial(target_lower),
            "remaining_divided_root_orders": root_orders,
            "I_c_D_c_Phi_d": {"term": serialize_monomial(target_top),
                                "coefficient": "1"},
            "d_I_c_Phi_hat_D_r": {"term": serialize_monomial(target_top),
                                    "coefficient": "1"},
            "termwise_difference": 0,
        },
        "marked_augmentation": {
            "physical_face": "0112/q23:21",
            "coefficient_label": "B1",
            "normalized_cut_image_c1_plus_over_8":
                [str(value) for value in cut23_image],
            "protected_actual": "(c1_plus/8,c1_plus/8)",
            "protected_required": "(c1_plus/8,0)",
            "protected_residual_required_minus_actual": "(0,-c1_plus/8)",
        },
        "hidden_face_expansion": {
            "D_root": [str(value) for value in hidden.D_ROOT],
            "E23": "D_root tensor B1",
            "E23_nonzero_coefficients": [str(hidden.D_ROOT[root])
                                           for root in range(4)],
            "required_H23": "(-E23,0,+E23) in (lower,Eq,ores)",
            "covered_decomposition": "H23=-M_E23+K_E23+C_Eq23",
            "M_E23": "(E23,E23,0)",
            "K_E23": "(0,0,E23)",
            "first_unmatched_object": "C_Eq23=(0,E23,0)",
            "first_unmatched_terms": unmatched,
            "lexicographically_first_unmatched_term": unmatched[0],
            "strong_grant_rank_before_after_C_Eq23": [48, 49],
            "primitive_dual": "lambda_(root0,B1)=lower_(root0,B1)-Eq_(root0,B1)",
            "primitive_dual_value_on_first_unmatched": "1",
        },
        "covariance": {
            "site_sigma": "(2 5)(3 4)",
            "site_level_target_q23_to_q45_coefficient": "1",
            "root_sigma": "(0 1)(2 3)",
            "pure_transition": "(B0 B5 B3 B2)(B1 B4)",
            "root_pure_hidden_transport": "sigma(E23)=-E45",
            "required_orientation_character_for_missing_cell": "-1",
            "orientation_character_supplied_by_existing_e_C_A_e_R_action": False,
        },
        "minimal_counter_obligation": (
            "construct a source-labelled response-to-cap cell X23 in e_C A e_R "
            "whose selected-grade augmented boundary contributes "
            "C_Eq23=D_root tensor B1 tensor (H0-u)e_Eq with zero lower, "
            "ores, W, target and anchor components; its cut mate must carry "
            "the pinned sigma orientation sigma(X23)=-X45, and separate AB/AC "
            "root naturality must be proved"
        ),
        "scope_guard": (
            "This is an exact first-unmatched-term theorem for the canonical "
            "h=3 q23 marked carrier and the pinned current operation inventory. "
            "It neither proves nonexistence of an unregistered physical cell "
            "nor proves PAComp(3), uniform PAComp(h), or terminal promotion."
        ),
    }
    digest = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return result, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    result, digest = audit()
    if arguments.json:
        print(json.dumps({"result": result, "logical_sha256": digest},
                         indent=2, sort_keys=True))
    else:
        print("Q23 protected factor trace: PASS FIRST UNMATCHED TERM")
        print("intrinsic q23 marked descendants: 90 termwise equal")
        print("first unmatched: C_Eq23[root0,B1]=-1 (Eq only)")
        print("strong endpoint grant rank: 48 -> 49")
        print("sigma(E23)=-E45; missing orientation not source-provenant")
        print("logical_sha256", digest)


if __name__ == "__main__":
    main()

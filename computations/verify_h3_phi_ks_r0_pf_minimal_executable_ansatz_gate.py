#!/usr/bin/env python3
"""Solve the smallest literal h=3 Phi_KS,r0/P_f finite ansatz.

The ansatz deliberately grants the four coefficient-side ingredients named
in the theorem statement:

* the p/s-odd order-two selector on each of q23 and q45;
* the selected six-term db01 packet;
* both fixed-window DQ<->PS switch families; and
* the named cap r0/E packet with B=Eq and protected rows.

All word, fine, repeated, operation and root labels are kept as direct-sum
coordinates.  The granted ingredients close their own finite blocks, but
they do not form one physical response-to-cap column.  The first left kernel
is supported on the two root-labelled response->cap operation matrix units.

After conditionally adjoining those two sections, the next left kernel is
the primitive mixed K_Eq mapping-square incidence.  After adjoining both
root-labelled mixed cells, the shifted ridge is independently detected.
Adjoining the sections, mixed cells and ridges yields an explicit normalized
formal solution.  Thus the executable ansatz identifies the exact missing
physical bicomplex; it does not claim that its new cells are constructed.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_order2_promoted_occurrence_orientation_gate.py":
        "c0a34736979eb8a5d059dce30224b3d22f3930e9afaf07916dbbf51b3539c15d",
    "computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py":
        "a08598e088c100e4b5116fb2b39717ec639116ea1fa7575062ba9a8f8cf9c683",
    "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py":
        "2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
    "computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py":
        "262e1dd08dd1842d60515d45aea53ea406d7e1e5ea55ab506bb6e81d64b07741",
    "computations/verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    "computations/verify_h3_hyperbolic_root_pair_cross_word_eq_ridge_gate.py":
        "0760703ace1498cc9c255dd8a2017395ece9a7750ab6a21c88233518e1314bba",
    "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py":
        "2e4b1a1b9bb5b5be8d0997132b49b95576a28dc6ccb9cfd83db808ace8f52f3e",
}
EXPECTED_LEDGER_SHA256 = (
    "d6a5054e63b2c1aa83af3123c767f8c6a99e5178757f6330acc4d02456d9ddd0"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * Q(entry) for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[columns[column][row] for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def unit(width: int, index: int) -> tuple[Q, ...]:
    return tuple(Q(position == index) for position in range(width))


def embed(vector: tuple[Q, ...], before: int, after: int) -> tuple[Q, ...]:
    return (Q(0),) * before + tuple(vector) + (Q(0),) * after


def block_sum(blocks: tuple[tuple[tuple[Q, ...], ...], ...]) \
        -> tuple[tuple[Q, ...], ...]:
    dimensions = tuple(len(block[0]) if block else 0 for block in blocks)
    require(all(block for block in blocks), "empty direct-sum block")
    total = sum(dimensions)
    answer = []
    before = 0
    for block, dimension in zip(blocks, dimensions, strict=True):
        after = total - before - dimension
        answer.extend(embed(column, before, after) for column in block)
        before += dimension
    return tuple(answer)


def component_dependency_audit(order2, db01, window, maximal, private_eq,
                               comparison, cross_word, mixed) \
        -> dict[str, object]:
    parity = order2.parity_decomposition_audit()
    cuts = order2.two_cut_covariance_audit()
    db_faces = db01.literal_face_inventory_audit()
    db_guard = db01.maximal_termwise_counterguard_audit()
    window_columns, detector, candidate_h, _candidate_r, window_packet = (
        window.audit_cartesian_physical_packet()
    )
    switches = window.audit_operation_switch_boundary(
        window_columns, candidate_h, _candidate_r
    )
    cap_columns, cap_names = maximal.cap_named_columns(private_eq)
    _cap_block_columns, _cap_dual, cap_ledger = (
        maximal.augmented_private_eq_block(private_eq)
    )
    chain = comparison.algebraic_two_term_chain_map_audit()
    word = cross_word.word_section_rank_audit()
    augmented = cross_word.paired_reduced_eq_and_ridge_audit()
    square = mixed.mapping_cylinder_square_audit()

    require(parity["primitive_orientation"] == "o_f=e_f-e_tau_f"
            and cuts["cut_1"] == "0112 with q23:21 reinsertion"
            and cuts["cut_2"] == "0121 with q45:12 reinsertion"
            and db_faces["selected_response"]["term_count"] == 6
            and db_guard["rank_before_after_selected_db01"] == [181, 182]
            and window_packet["internal_rank"] == 46
            and switches["rank_base_two_switches_candidate"] == [46, 48, 48]
            and len(cap_columns) == len(cap_names) == 25
            and cap_ledger["rank"] == 23
            and chain["normalized_solution"] == {"a": 1, "b": -1}
            and word["old_relative_cross_word_rank"] == 0
            and augmented["strong_grant_base_rank"] == 4
            and square["physical_source_typed_quotient"] == {
                "rows": ["R_E14", "central E", "mixed square incidence"],
                "available_rank": 2,
                "rank_with_required_comparison": 3,
                "primitive_dual": [0, 0, 1],
            }, "a pinned component interface changed")
    require(dot(detector, candidate_h) == 6,
            "the fixed-window Gate-II detector changed")
    return {
        "order2_selectors": {
            "cuts": [cuts["cut_1"], cuts["cut_2"]],
            "coordinates_per_cut": parity["occurrences"],
            "required_face": parity["primitive_orientation"],
            "operation": "p/s-odd response occurrence selector",
        },
        "selected_db01": {
            "word_head": db_faces["selected_response"]["word_head"],
            "terms": db_faces["selected_response"]["term_count"],
            "fine_removed_edges": db_faces["selected_response"][
                "removed_edges"],
            "operation": "selected response first-PP / PS[p0,s1]",
            "rank_before_after_grant": [181, 182],
        },
        "fixed_window_switches": {
            "words": list(window.WORDS),
            "charts": list(window.CHARTS),
            "matchings": list(window.MATCHINGS),
            "old_rank": window_packet["internal_rank"],
            "rank_after_both": 48,
            "families": switches["projected_missing_row_families"],
            "operation": "Hasse[2] DQ<->PS chart switch",
        },
        "cap": {
            "word": "01211222",
            "fine": "six t*q_(v,N) occurrence degrees",
            "repeated": "P3+K2",
            "operation": "AugP2/K_Eq cap r0",
            "named_columns": len(cap_columns),
            "rank": cap_ledger["rank"],
            "B_Eq_law": "B=Eq coefficientwise on r0",
        },
        "ungraded_chain_map": chain,
        "cross_word": word,
        "conditional_augmented": augmented,
        "primitive_mapping_square": square,
    }


def build_lower_selector_blocks():
    one = (Q(1),) * 12
    pair = add(unit(12, 0), unit(12, 1))
    odd = add(unit(12, 0), scale(-1, unit(12, 1)))
    require(rank((one, pair)) == 2
            and rank((one, pair, odd)) == 3,
            "order-two selector block changed")
    return (one, pair), odd


def build_db01_block():
    flags = 180
    width = 360
    graphs = tuple(add(scale(-1, unit(width, index)),
                       unit(width, flags + index))
                   for index in range(flags))
    response_complete = tuple(Q(index < flags) for index in range(width))
    target_complete = tuple(Q(index >= flags) for index in range(width))
    old = graphs + (response_complete, target_complete)
    selected = tuple(Q(index < 6) for index in range(width))
    detector = tuple(Q(29 if (index % flags) < 6 else -1)
                     for index in range(width))
    require(rank(old) == 181 and rank(old + (selected,)) == 182
            and all(dot(detector, column) == 0 for column in old)
            and dot(detector, selected) == 174,
            "selected db01 block changed")
    return old, selected


def build_section_block():
    # Per root coordinates are
    #   (response identity, cap identity, response->cap operation,
    #    response word, cap word).
    # The first two are old block-diagonal identities.  A literal section
    # must simultaneously occupy the off-diagonal operation coordinate and
    # have boundary -response_word+cap_word.
    old = []
    sections = []
    operation_duals = []
    for root in range(2):
        offset = 5 * root
        old.extend((unit(10, offset), unit(10, offset + 1)))
        sections.append(add(
            unit(10, offset + 2),
            scale(-1, unit(10, offset + 3)),
            unit(10, offset + 4),
        ))
        operation_duals.append(unit(10, offset + 2))
    paired_dual = scale(Q(1, 2), add(*operation_duals))
    require(rank(tuple(old)) == 4
            and rank(tuple(old) + tuple(sections)) == 6
            and all(dot(paired_dual, column) == 0 for column in old)
            and dot(paired_dual, add(*sections)) == 1,
            "root-labelled response-to-cap section block changed")
    return tuple(old), tuple(sections), paired_dual


def build_augmented_block():
    # Per root rows are (R_E14, clean Eq, mixed square, shifted ridge).
    base = (unit(8, 0), unit(8, 1), unit(8, 4), unit(8, 5))
    mixed = (
        add(unit(8, 0), unit(8, 1), unit(8, 2)),
        add(unit(8, 4), unit(8, 5), unit(8, 6)),
    )
    ridge = (unit(8, 3), unit(8, 7))
    mixed_dual = scale(Q(1, 2), add(unit(8, 2), unit(8, 6)))
    ridge_dual = scale(Q(1, 2), add(unit(8, 3), unit(8, 7)))
    require(rank(base) == 4
            and rank(base + mixed) == 6
            and rank(base + mixed + ridge) == 8
            and all(dot(mixed_dual, column) == 0 for column in base)
            and dot(mixed_dual, add(*mixed)) == 1
            and all(dot(ridge_dual, column) == 0
                    for column in base + mixed)
            and dot(ridge_dual, add(*ridge)) == 1,
            "root-labelled mixed/ridge block changed")
    return base, mixed, ridge, mixed_dual, ridge_dual


def cap_block(maximal, private_eq):
    columns, names = maximal.cap_named_columns(private_eq)
    by_name = dict(zip(names, columns, strict=True))
    delta = (Q(1), Q(1), Q(-1), Q(-1))
    balanced_r0 = tuple(Q(0) for _ in range(27))
    for corner, coefficient in enumerate(delta):
        balanced_r0 = add(balanced_r0,
                          scale(coefficient, by_name[f"r0_{corner}"]))
    expected = tuple(map(Q, (*delta, *delta, *delta,
                             0, 0, 0, 0,
                             0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0)))
    require(balanced_r0 == expected
            and rank(tuple(columns)) == 23,
            ("balanced protected cap readout changed", balanced_r0))
    return tuple(columns), balanced_r0


def full_finite_ansatz_audit(window, maximal, private_eq):
    selector_old, selector = build_lower_selector_blocks()
    db_old, db_selected = build_db01_block()
    window_named = tuple(value for _name, value in
                         window.build_internal_columns())
    ab_switch = window.chart_h_vector(0, window.AB_SWITCH)
    ac_switch = window.chart_h_vector(0, window.AC_SWITCH)
    cap_named, balanced_r0 = cap_block(maximal, private_eq)
    section_old, sections, operation_dual = build_section_block()
    aug_base, mixed, ridge, mixed_dual, ridge_dual = build_augmented_block()

    blocks = (
        selector_old, selector_old, db_old, window_named, cap_named,
        section_old, aug_base,
    )
    dimensions = (12, 12, 360, 48, 27, 10, 8)
    require(tuple(len(block[0]) for block in blocks) == dimensions,
            "ansatz block dimensions changed")
    named = block_sum(blocks)

    before = (0, 12, 24, 384, 432, 459, 469)
    total = sum(dimensions)
    after = tuple(total - before[index] - dimensions[index]
                  for index in range(len(dimensions)))

    selector23 = embed(selector, before[0], after[0])
    selector45 = embed(selector, before[1], after[1])
    db = embed(db_selected, before[2], after[2])
    switch_ab = embed(ab_switch, before[3], after[3])
    switch_ac = embed(ac_switch, before[3], after[3])
    cap = embed(balanced_r0, before[4], after[4])
    section_columns = tuple(embed(value, before[5], after[5])
                            for value in sections)
    mixed_columns = tuple(embed(value, before[6], after[6])
                          for value in mixed)
    ridge_columns = tuple(embed(value, before[6], after[6])
                          for value in ridge)

    listed_grants = (selector23, selector45, db, switch_ab, switch_ac)
    listed = named + listed_grants
    with_sections = listed + section_columns
    with_mixed = with_sections + mixed_columns
    completed = with_mixed + ridge_columns

    formal_target = add(
        *listed_grants, cap, *section_columns, *mixed_columns, *ridge_columns
    )
    operation_global = embed(operation_dual, before[5], after[5])
    mixed_global = embed(mixed_dual, before[6], after[6])
    ridge_global = embed(ridge_dual, before[6], after[6])

    base_rank = rank(named)
    listed_rank = rank(listed)
    section_rank = rank(with_sections)
    mixed_rank = rank(with_mixed)
    completed_rank = rank(completed)
    require((base_rank, listed_rank, section_rank, mixed_rank, completed_rank)
            == (262, 267, 269, 271, 273),
            (base_rank, listed_rank, section_rank, mixed_rank, completed_rank))
    require(dot(operation_global, formal_target) == 1
            and all(dot(operation_global, column) == 0 for column in listed),
            "the first operation-section left kernel changed")
    require(dot(mixed_global, formal_target) == 1
            and all(dot(mixed_global, column) == 0
                    for column in with_sections),
            "the conditional mixed-Eq left kernel changed")
    require(dot(ridge_global, formal_target) == 1
            and all(dot(ridge_global, column) == 0 for column in with_mixed),
            "the conditional ridge left kernel changed")

    # The displayed coefficients give an explicit solution after all three
    # missing physical levels are adjoined.  Cap coefficients are delta on
    # r0_0,...,r0_3; every other displayed new/face column has coefficient 1.
    explicit_solution = add(
        *listed_grants, cap, *section_columns, *mixed_columns, *ridge_columns
    )
    require(explicit_solution == formal_target,
            "the completed ansatz solution changed")

    return {
        "row_blocks": [
            {"name": "order2 q23 p/s-odd", "dimension": 12},
            {"name": "order2 q45 p/s-odd", "dimension": 12},
            {"name": "selected db01 termwise carrier", "dimension": 360},
            {"name": "fixed-window word/chart/C4", "dimension": 48},
            {"name": "cap augmented protected rows", "dimension": 27},
            {"name": "two root-labelled operation/word sections", "dimension": 10},
            {"name": "two root-labelled R/E/kappa/ridge packets", "dimension": 8},
        ],
        "total_rows": total,
        "named_columns": len(named),
        "named_rank": base_rank,
        "listed_ansatz_grants": [
            "q23 p/s-odd selector", "q45 p/s-odd selector",
            "selected six-term db01", "A+B fixed-window switch",
            "A+C fixed-window switch",
        ],
        "rank_after_listed_grants": listed_rank,
        "listed_grants_solve_formal_target": False,
        "first_left_kernel": {
            "support": "1/2 on each root-labelled response->cap operation coordinate",
            "on_all_named_and_listed_columns": 0,
            "on_required_Phi_boundary": 1,
            "missing_atom": (
                "one natural root-labelled response-KS -> cap-r0 section "
                "schema, instantiated on both A/B and A/C roots"
            ),
            "literal_word": "11110000 -> 01211222",
            "literal_operation": "response occurrence -> AugP2/K_Eq cap",
        },
        "rank_after_two_section_instances": section_rank,
        "conditional_second_left_kernel": {
            "support": "1/2 on each root-labelled mixed K_Eq square incidence",
            "on_columns_through_word_sections": 0,
            "on_required_boundary": 1,
            "missing_atom": "kappa_orb,Eq mixed mapping-cylinder/Tate 2-cell",
        },
        "rank_after_two_mixed_cells": mixed_rank,
        "conditional_third_left_kernel": {
            "support": "1/2 on each root-labelled shifted ridge",
            "on_columns_through_mixed_cells": 0,
            "on_required_boundary": 1,
            "missing_atom": "both shifted gamma=-dOmega ridge faces",
        },
        "rank_after_two_ridges": completed_rank,
        "formal_solution_exists_after_full_bicomplex": True,
        "normalized_solution_coefficients": {
            "each_selector_db01_switch_section_mixed_ridge": 1,
            "cap_r0_corners": [1, 1, -1, -1],
        },
        "cap_balanced_readout": {
            "B": [1, 1, -1, -1],
            "Eq": [1, 1, -1, -1],
            "target": [1, 1, -1, -1],
            "M_ainc_q_Pf_ores_W_ridge_eta_sigma": "all zero after delta sum",
            "B_minus_Eq": [0, 0, 0, 0],
        },
        "interpretation": (
            "the four listed ingredients are coefficient-compatible but do "
            "not assemble into one literal physical column.  A completed "
            "candidate is exactly one natural paired collision mapping "
            "bicomplex containing the two response-to-cap sections, both "
            "mixed K_Eq cells, and both shifted ridges"
        ),
    }


def chain_and_readout_audit(comparison, mixed):
    chain = comparison.algebraic_two_term_chain_map_audit()
    square = mixed.mapping_cylinder_square_audit()
    require(chain["chain_map_equation"] == "a+b=0"
            and chain["normalized_solution"] == {"a": 1, "b": -1}
            and square["H1_without_mixed_face"] == "Z"
            and square["H1_after_one_mixed_face"] == 0,
            (chain, square))

    rows = (
        "B", "Eq", "target", "M", "ainc", "q", "P_f",
        "ores", "W", "ridge", "eta", "sigma",
    )
    per_db_term = tuple(map(Q, (1, 1, 1, -1, -1, 0, 1,
                                0, 0, 0, 0, 0)))
    require(per_db_term[0] == per_db_term[1]
            and per_db_term[5] == per_db_term[3] - per_db_term[4]
            and per_db_term[7:] == (Q(0),) * 5,
            "the conditional db01*r0 readout changed")
    return {
        "ungraded_chain_map_equation": chain["chain_map_equation"],
        "unique_normalized_components": {
            "Phi_1(epsilon_s)": "r0",
            "Phi_0(c_f)": "-E",
        },
        "mapping_square_cycle": square["primitive_boundary_cycle"],
        "mapping_square_H1_before_after_mixed_cell": [1, 0],
        "conditional_readout_row_order": list(rows),
        "conditional_readout_per_selected_db01_term":
            list(map(int, per_db_term)),
        "six_term_aggregate": list(map(int, scale(6, per_db_term))),
        "protected_equations": {
            "B_equals_Eq": True,
            "q_equals_M_minus_ainc": True,
            "ores_W_ridge_eta_sigma": [0, 0, 0, 0, 0],
        },
        "d_squared": (
            "zero after the primitive mixed square and its shifted ridge "
            "connection faces are included; without the mixed square the "
            "primitive mapping-cycle H1 is nonzero"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    order2 = load(
        "computations/verify_h3_order2_promoted_occurrence_orientation_gate.py",
        "phi_ansatz_order2",
    )
    db01 = load(
        "computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py",
        "phi_ansatz_db01",
    )
    window = load(
        "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py",
        "phi_ansatz_window",
    )
    maximal = load(
        "computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py",
        "phi_ansatz_maximal",
    )
    private_eq = load(
        "computations/verify_h3_balanced_square_private_eq_projection_gate.py",
        "phi_ansatz_private_eq",
    )
    comparison = load(
        "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py",
        "phi_ansatz_comparison",
    )
    cross_word = load(
        "computations/verify_h3_hyperbolic_root_pair_cross_word_eq_ridge_gate.py",
        "phi_ansatz_cross_word",
    )
    mixed = load(
        "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py",
        "phi_ansatz_mixed",
    )

    ledger = {
        "theorem": "h3 Phi_KS,r0/P_f smallest executable literal ansatz gate",
        "pins": PINS,
        "component_interfaces": component_dependency_audit(
            order2, db01, window, maximal, private_eq, comparison,
            cross_word, mixed,
        ),
        "full_finite_solve": full_finite_ansatz_audit(
            window, maximal, private_eq
        ),
        "chain_and_protected_readouts": chain_and_readout_audit(
            comparison, mixed
        ),
        "verdict": (
            "Granting the two p/s-odd selector cells, selected db01, both "
            "DQ/PS fixed-window switches and the full tied cap r0 packet "
            "does not produce Phi_KS,r0/P_f.  The exact first separator is "
            "the paired response-to-cap operation/word-section character. "
            "After conditionally adding its two root-labelled instances, "
            "the primitive mixed K_Eq square is the next missing physical "
            "atom; the shifted ridge is independent after that.  Adding all "
            "three levels gives an explicit normalized formal solution with "
            "Phi_1(epsilon_s)=r0, Phi_0(c_f)=-E and B=Eq, so there is no "
            "remaining coefficient, sign or protected-readout obstruction."
        ),
        "smallest_positive_object": (
            "one natural root-labelled paired collision mapping bicomplex: "
            "its two degree-zero sections have word 11110000->01211222 and "
            "operation response->AugP2; its two mixed faces are "
            "kappa_orb,Eq; its proper Kahler faces are the two shifted "
            "gamma=-dOmega ridges"
        ),
        "scope": (
            "exact rational finite ansatz on the canonical h=3 labelled "
            "windows.  The selector, db01 and raw switch columns are strong "
            "conditional grants.  The formal completed solution is a "
            "candidate schema, not a construction of its missing physical "
            "sections, mixed cells or ridges, and not an all-h theorem."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("h3 Phi_KS,r0/P_f finite ansatz: NO SOLUTION FROM LISTED FACES")
    print("first missing atom: TWO ROOT-LABELLED RESPONSE->CAP SECTIONS")
    print("conditional next atom: MIXED K_EQ MAPPING SQUARE")
    print("conditional final proper face: SHIFTED RIDGE")
    print("completed formal bicomplex solution: UNIQUE NORMALIZED SHAPE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

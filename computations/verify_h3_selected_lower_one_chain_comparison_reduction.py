#!/usr/bin/env python3
"""Reduce Gate I to one typed chain equation on the selected lower cycle.

The marked filtered lift uses one collision vector

    l = u_024-u_012

on the 15 physical ``(matching,repeated edge)`` labels.  Its three shared
repeated-02 coordinates are zero.  Hence a chain map on the whole U_15
module is sufficient but not necessary: for this lift it is enough to find
one physical cell C and one protected output comparison A with

    J_3 C = A J_col(l).

The committed support collapse gives the exact candidate.  On the twelve
nonzero labels its normalized image is B0+B2-B3-B5, whose complete literal
boundary has 360 features; the already physical M_v=-O_alpha+K has exactly
that boundary and all augmented output rows correctly typed.  Values on the
three shared labels cannot change this one-vector image.

This is not yet a construction of the displayed equation.  The input audit
exposes only the occurrence projection of J_col(l), not its complete
protected/source-labelled boundary.  An exact hidden-row counterguard keeps
all committed occurrence data fixed while changing the one-chain equation.
Thus the reduced frontier is one full-row equality, not the two shared-loop
images.  The latter are needed only to extend the result to a map on U_15.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py":
        "ea45c09a8347c312ea9721475d54a4b4f9aad21d8d51cb9d4d297aeaa99ba429",
    "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py":
        "db23eb4e760dd84934426a80516aad355486e947626da1849454718b512efb2d",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_filtered_common_tail_marked_kernel_lift.py":
        "d7cc4cdbee64cd33f9c351b4ef4fdab8e81dfacc099ce5d917bbdf9c3da1b2d2",
    "computations/verify_h3_cut_swap_shared_loop_hasse_cross_term_gate.py":
        "cc551585391a990060f78b49486c05af6c3b4a301058c855a422ae9d54fe5be5",
}
EXPECTED_LEDGER_SHA256 = (
    "328a8cdb2fed59cc115a218b8ba68d131b764335fed96e06c093d986c74117a1"
)

PHI_VALUES = (4, 2, 4, 1, 5, 3)
TARGET_ALPHA = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))


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


def mat_vec(matrix, vector):
    return tuple(sum(Q(a) * Q(b) for a, b in zip(row, vector, strict=True))
                 for row in matrix)


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    lower = load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "one_chain_lower",
    )
    tangent = load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "one_chain_tangent",
    )
    support = load(
        "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py",
        "one_chain_support",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "one_chain_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "one_chain_base",
    )
    mv = load(
        "computations/verify_h3_literal_mv_cap_cartan_composition.py",
        "one_chain_mv",
    )
    filtered = load(
        "computations/verify_h3_filtered_common_tail_marked_kernel_lift.py",
        "one_chain_filtered",
    )
    cross = load(
        "computations/verify_h3_cut_swap_shared_loop_hasse_cross_term_gate.py",
        "one_chain_cross",
    )

    key = lambda label: (label[1], label[2])
    base_labels = frozenset(map(
        key, lower.lower_labels(tangent, (0, 1, 2))))
    other_labels = frozenset(map(
        key, lower.lower_labels(tangent, (0, 2, 4))))
    labels = tuple(sorted(base_labels | other_labels))
    shared = tuple(sorted(base_labels & other_labels))
    lower_vector = tuple(
        Q(int(label in other_labels) - int(label in base_labels))
        for label in labels
    )
    support_indices = tuple(index for index, value in enumerate(lower_vector)
                            if value)
    shared_indices = tuple(labels.index(label) for label in shared)
    require(len(labels) == 15 and len(shared) == 3
            and len(support_indices) == 12
            and all(lower_vector[index] == 0 for index in shared_indices),
            "the selected 15/12/3 lower packet changed")

    # Reconstruct the canonical six pure multiplier columns and the exact
    # partial collapse on the twelve nonzero labels.
    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, degree)
    pure = tuple((multiplier, boundary)
                 for word, multiplier, boundary in component["columns"]
                 if word == complete.PURE_WORD)
    graph_index = {support.graph(multiplier): index
                   for index, (multiplier, _boundary) in enumerate(pure)}
    require((left, right) == (3, 5) and len(pure) == len(graph_index) == 6,
            "the canonical pure target changed")

    phi = dict(enumerate(PHI_VALUES))
    partial_map = [[Q(0)] * len(labels) for _ in range(6)]
    for index in support_indices:
        image = support.collapse_graph(tangent, labels[index], phi)
        require(image in graph_index,
                ("a nonzero lower label left the pure target", labels[index]))
        partial_map[graph_index[image]][index] = Q(1)
    raw_image = mat_vec(tuple(map(tuple, partial_map)), lower_vector)
    normalized_image = tuple(value / 2 for value in raw_image)
    require(raw_image == tuple(2 * value for value in TARGET_ALPHA)
            and normalized_image == TARGET_ALPHA,
            ("the selected lower image changed", raw_image))

    # Arbitrary shared-label values do not affect this one vector.  Use two
    # inequivalent extensions, including augmentation-one Hasse choices.
    zero_extension = tuple(map(tuple, partial_map))
    repaired_map = [row[:] for row in partial_map]
    shared_targets = (1, 4, 5)
    for source_index, target_index in zip(
            shared_indices, shared_targets, strict=True):
        repaired_map[target_index][source_index] = Q(1)
    repaired_extension = tuple(map(tuple, repaired_map))
    require(mat_vec(zero_extension, lower_vector) == raw_image
            and mat_vec(repaired_extension, lower_vector) == raw_image,
            "shared-label extension changed the selected lower image")

    literal_boundary = defaultdict(Q)
    for coefficient, (_multiplier, boundary) in zip(
            TARGET_ALPHA, pure, strict=True):
        for feature in boundary:
            literal_boundary[feature] += coefficient
    literal_boundary = {feature: value for feature, value
                        in literal_boundary.items() if value}
    require(len(literal_boundary) == 360
            and {len(feature) for feature in literal_boundary} == {7},
            "the one-chain candidate lost its literal full-nine boundary")

    mv_ledger, mv_digest = mv.audit()
    require(mv_digest == mv.EXPECTED_LEDGER_SHA256,
            "the literal M_v construction changed")
    mv_packet = mv_ledger["composition"]["M_v_equals_minus_O_plus_K"]
    require(mv_packet["literal_boundary_support"] == 360
            and mv_packet["ordinary_residue"] == [0, 0, 0, 0]
            and mv_packet["D_W_target_ainc"] == [0, 0, 0, 0]
            and mv_packet["eta_z"] == "1+delta_(vz)*u_z/t"
            and mv_packet["sigma"] == "-q_pq^22",
            "the one-chain output stopped having exact augmented typing")

    support_ledger, support_digest = support.audit()
    require(support_digest == support.EXPECTED_LEDGER_SHA256
            and support_ledger["positive_support_construction"]
                ["literal_boundary_support"] == 360,
            "the twelve-label collapse theorem changed")
    filtered_ledger, filtered_digest = filtered.audit()
    require(filtered_digest == filtered.EXPECTED_LEDGER_SHA256
            and "nullhomotopy of the lower collision profile -v"
                in filtered_ledger["descent_interface"],
            "the marked filtered descent interface changed")
    cross_ledger, cross_digest = cross.audit()
    require(cross_digest == cross.EXPECTED_LEDGER_SHA256
            and cross_ledger["literal_C4_resolution"]
                ["occurrence_augmentation"] == 1,
            "the shared Hasse occurrence theorem changed")

    # Exact insufficiency guard.  The disclosed occurrence projection is
    # the first fifteen rows.  Two complete input boundaries have identical
    # disclosed rows but differ on one hidden physical/private row.  The
    # selected lower detects that row, so occurrence equality cannot decide
    # the full one-chain equation.
    occurrence_rows = tuple(
        tuple(Q(int(row == column)) for column in range(len(labels)))
        for row in range(len(labels))
    )
    hidden_zero = (Q(0),) * len(labels)
    detecting_index = next(index for index, value in enumerate(lower_vector)
                           if value == 1)
    hidden_private = tuple(Q(int(index == detecting_index))
                           for index in range(len(labels)))
    good_boundary = occurrence_rows + (hidden_zero,)
    bad_boundary = occurrence_rows + (hidden_private,)
    good_value = mat_vec(good_boundary, lower_vector)
    bad_value = mat_vec(bad_boundary, lower_vector)
    require(good_value[:-1] == bad_value[:-1] == lower_vector
            and good_value[-1] == 0 and bad_value[-1] == 1,
            "the full-row insufficiency counterguard changed")

    ledger = {
        "theorem": "selected-lower one-chain reduction of Gate I",
        "pins": PINS,
        "homological_sufficiency": {
            "selected_lower": "l=u_024-u_012",
            "physical_collision_labels": len(labels),
            "nonzero_coefficients": len(support_indices),
            "shared_repeated_02_coefficients": [
                str(lower_vector[index]) for index in shared_indices
            ],
            "full_map_equations": 15,
            "selected_one_chain_equations": 1,
            "sufficient_equation": "J_3 C=A J_col(l)",
            "reason": (
                "the filtered top/lower cycle already has opposite boundary; "
                "one cell satisfying the displayed equation cancels the "
                "selected lower while retaining its ordinary marked top"
            ),
        },
        "exact_candidate": {
            "support_collapse": list(PHI_VALUES),
            "raw_image": [str(value) for value in raw_image],
            "normalized_image": [str(value) for value in normalized_image],
            "shared_extension_changes_selected_image": False,
            "literal_boundary_features": len(literal_boundary),
            "literal_boundary_edge_degree": 7,
            "physical_cell": "M_v=-O_alpha+K",
            "ordinary_residue": mv_packet["ordinary_residue"],
            "D_W_target_ainc": mv_packet["D_W_target_ainc"],
            "eta_z": mv_packet["eta_z"],
            "sigma": mv_packet["sigma"],
        },
        "shared_Hasse_scope": {
            "fixed_pair_cells_have_occurrence_augmentation": 1,
            "coefficient_on_selected_lower": 0,
            "needed_for_selected_one_chain": False,
            "needed_for_full_U15_extension": True,
            "consequence": (
                "alternating Cartan/Spencer caps for the shared loops may "
                "construct a reusable Phi, but they cannot be an obligation "
                "for nullhomotoping this one signed lower vector"
            ),
        },
        "first_unproved_full_row": {
            "equation": "J_3(M_v)=A J_col(l)",
            "known_left_side": (
                "360 literal seven-edge features, four Eq entries, zero "
                "ordinary residue/D/W/target/ainc, and the eta/sigma ridge"
            ),
            "known_right_side": (
                "only the occurrence/collapse projection; the complete "
                "protected and source-labelled J_col(l) row is not exposed"
            ),
            "hidden_row_counterguard": {
                "same_disclosed_occurrence_rows": True,
                "good_hidden_value_on_l": str(good_value[-1]),
                "bad_hidden_value_on_l": str(bad_value[-1]),
            },
            "source_valid_one_chain_constructed": False,
        },
        "frontier_shift": (
            "for the selected determinant-dark marked lift, replace the two "
            "shared-loop source cells/full-U15 Phi by one exact full-row "
            "Cartan-Spencer nullhomotopy equation.  A full Phi remains needed "
            "only for uniform reuse, inactive/Rees propagation, or q transport "
            "on arbitrary protected kernel vectors"
        ),
        "scope": (
            "exact rational h=3 selected-cycle reduction and complete output "
            "typing.  It does not assert the missing input full-row equality, "
            "nor eliminate shared repairs from a theorem on all U15 labels"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("selected-lower one-chain ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 Gate-I selected lower: ONE-CHAIN REDUCTION")
    print("shared repeated-02 coefficients: 0,0,0")
    print("candidate image: B0+B2-B3-B5 -> physical M_v (360 features)")
    print("full-row equality J3(M_v)=A Jcol(l): STILL OPEN")
    print("full U15 shared-loop extension needed for this lift: NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

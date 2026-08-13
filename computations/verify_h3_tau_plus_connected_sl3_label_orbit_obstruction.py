#!/usr/bin/env python3
"""Test the connected two-root SL3 shortcut for the last tau_plus orbit.

Local SL3 root unipotents do give an explicit physical Cartan homotopy: the
perfect-matching tensor is equivariant, and the signed Weyl element factors
through root unipotents.  But every local colour operation preserves the
underlying site matching, multiplier graph, and repeated-edge label.  On the
six canonical pure columns its label action is therefore the identity; rho
adds only (B0 B5)(B2 B3), fixing B1 and B4.

The actual omitted-25 product-rule bypass lies in

    O = <B0,B2,B3,B5>,

whereas the desired even landing v=(B1+B4)/2 lies in the complementary
fixed-label plane.  The connected orbit cannot cross this decomposition.
Starting instead from the formal shared-02 fixed resolution gives B1/B4,
but local SL3 preserves its repeated-02 source label and cannot move it to
the actual omitted 01/04 rho-pair.

Thus the connected group constructs the root/word decoration of a correctly
placed column, not the missing placement.  The same label separator detects
delta_plus, the root-decorated mixed target and Eq packet, and labelled
ordinary residue.  Endpoint-even symmetrization also does not force the
endpoint-even W readout to vanish.  Beta=0 remains separate.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "computations/verify_h3_sl2_weyl_cartan_prism.py":
        "1024864418fea8f7f4ca6c77015972febd236f2a9822112daf20e1cf979bddaa",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_oriented_shared_loop_resolution_unification.py":
        "e6819e5437d967ec9bb0f32a24836c70c34e5b35bbd4f9e3ebd38b0a5c4fb714",
    "computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py":
        "24ec9e3c1d1f9b689fa5a47faf9900c16724dc215fee0a41a0b653f410427fb3",
}
EXPECTED_LEDGER_SHA256 = (
    "ad34db2ac949510f41d877c24679e532c9b2db28f31ce35cd32ec1b7283517a4"
)

RHO_B = (5, 1, 3, 2, 4, 0)
ROOT_SITES = (2, 5)
COLOURS = (0, 1, 2)


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


def add(*vectors):
    return tuple(sum(Q(vector[index]) for vector in vectors)
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(entry) for entry in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def tensor(left, right):
    return tuple(Q(a) * Q(b) for a in left for b in right)


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def underlying_graph(monomial):
    return tuple(sorted((left, right) for left, right, _a, _b in monomial))


def root_derivative_terms(monomial, site, old, new):
    """Infinitesimal E_(new,old) action on a decorated monomial."""
    answer = Counter()
    for position, cell in enumerate(monomial):
        left, right, left_colour, right_colour = cell
        changed = None
        if left == site and left_colour == old:
            changed = (left, right, new, right_colour)
        elif right == site and right_colour == old:
            changed = (left, right, left_colour, new)
        if changed is None:
            continue
        next_cells = list(monomial)
        next_cells[position] = changed
        answer[tuple(sorted(next_cells))] += 1
    return answer


def audit_connected_action_on_literal_columns():
    oriented = load(
        "computations/verify_h3_oriented_shared_loop_resolution_unification.py",
        "tau_sl3_oriented",
    )
    support = load(
        "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py",
        "tau_sl3_support",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "tau_sl3_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "tau_sl3_base",
    )

    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, degree)
    pure = tuple((multiplier, boundary) for word, multiplier, boundary
                 in component["columns"] if word == complete.PURE_WORD)
    require((left, right) == (3, 5) and len(pure) == 6,
            "the canonical six pure columns changed")

    multiplier_graphs = tuple(underlying_graph(multiplier)
                              for multiplier, _boundary in pure)
    require(len(set(multiplier_graphs)) == 6,
            "two canonical B labels acquired the same multiplier graph")

    # Check every off-diagonal sl3 root direction at both selected sites on
    # all 540 complete boundary features.  Every nonzero derivative term has
    # exactly the original underlying site multigraph.  The multiplier tag
    # is part of the source coordinate and is separately unchanged.
    feature_direction_checks = 0
    nonzero_derivative_terms = 0
    for b_index, (multiplier, boundary) in enumerate(pure):
        multiplier_graph = underlying_graph(multiplier)
        require(multiplier_graph == multiplier_graphs[b_index],
                "a pure multiplier graph changed during enumeration")
        for feature in boundary:
            graph = underlying_graph(feature)
            for site in ROOT_SITES:
                for old in COLOURS:
                    for new in COLOURS:
                        if old == new:
                            continue
                        image = root_derivative_terms(feature, site, old, new)
                        require(all(underlying_graph(term) == graph
                                    for term in image),
                                ("an sl3 root changed site incidence",
                                 b_index, site, old, new))
                        feature_direction_checks += 1
                        nonzero_derivative_terms += sum(image.values())
    require(feature_direction_checks == 6 * 90 * 2 * 6
            and nonzero_derivative_terms > 0,
            "the complete sl3 root-action census changed")

    # Re-use the frozen oriented loop computation to pin the action of rho
    # on the six B labels and the actual-vs-shared source-grade split.
    oriented_ledger, oriented_digest = oriented.audit()
    require(oriented_digest == oriented.EXPECTED_LEDGER_SHA256,
            "the oriented loop-resolution theorem changed")
    alignment = oriented_ledger["generic_even_target_alignment"]
    require(alignment["actual_tau_plus_loop"] == "25 -> 44"
            and alignment["local_tau_plus_targets"] == "B0,B2,B3,B5 only",
            "the actual tau_plus local orbit changed")

    return {
        "complete_component": "faces (3,5), six B multiplier labels",
        "pure_boundary_features": 6 * 90,
        "local_sl3_root_directions_per_site": 6,
        "selected_root_sites": list(ROOT_SITES),
        "feature_direction_checks": feature_direction_checks,
        "nonzero_derivative_terms": nonzero_derivative_terms,
        "root_action_on_uncoloured_multiplier_label": "identity",
        "rho_action_on_B_labels": list(RHO_B),
        "generated_B_label_orbits": [[0, 5], [1], [2, 3], [4]],
        "structural_reason": (
            "root unipotents and their Weyl products recolour coefficient "
            "variables but never change an underlying site edge or the "
            "source multiplier tag"
        ),
    }


def audit_label_separation():
    local = (Q(1, 4), Q(0), Q(1, 4),
             Q(1, 4), Q(0), Q(1, 4))
    v = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    delta = add(v, scale(-1, local))
    local_units = tuple(tuple(Q(int(position == index))
                              for position in range(6))
                        for index in (0, 2, 3, 5))
    fixed_dual = (Q(0), Q(1), Q(0), Q(0), Q(1), Q(0))
    require(tuple(local[index] for index in RHO_B) == local
            and tuple(v[index] for index in RHO_B) == v
            and all(dot(fixed_dual, unit) == 0 for unit in local_units)
            and dot(fixed_dual, local) == 0
            and dot(fixed_dual, v) == dot(fixed_dual, delta) == 1
            and rank(local_units) == 4
            and rank(local_units + (v,)) == 5,
            "the connected B-label separator changed")

    root_defect = (Q(-1), Q(1), Q(-1), Q(1))
    mixed = scale(-2, tensor(root_defect, v))
    reduced_eq = scale(2, tensor(root_defect, v))
    root_coordinate = (Q(1), Q(0), Q(0), Q(0))
    decorated_dual = tensor(root_coordinate, fixed_dual)
    require(dot(decorated_dual, mixed) == 2
            and dot(decorated_dual, reduced_eq) == -2,
            "the fixed-label dual stopped seeing the decorated packets")
    return {
        "connected_orbit_label_span": "<B0,B2,B3,B5>",
        "desired_fixed_plane": "<B1,B4>",
        "primitive_fixed_label_dual": [int(value) for value in fixed_dual],
        "dual_on_local_Bianchi_average": 0,
        "dual_on_v": 1,
        "dual_on_delta_plus": 1,
        "decorated_dual_on_mixed_target": 2,
        "decorated_dual_on_reduced_Eq": -2,
        "dual_on_labelled_ores_v": 1,
    }


def audit_source_grade_separation():
    support = load(
        "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py",
        "tau_sl3_source_support",
    )
    tangent = load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "tau_sl3_tangent",
    )
    lower = load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "tau_sl3_lower",
    )
    key = lambda label: (label[1], label[2])
    cut_012 = frozenset(map(key, lower.lower_labels(tangent, (0, 1, 2))))
    cut_024 = frozenset(map(key, lower.lower_labels(tangent, (0, 2, 4))))
    shared = tuple(sorted(cut_012 & cut_024))
    shared_fixed = shared[1]
    omitted = ((2, (0, 1)), (10, (0, 4)))
    require(shared_fixed == (4, (0, 2))
            and support.rho_label(tangent, shared_fixed) == shared_fixed
            and support.rho_label(tangent, omitted[0]) == omitted[1]
            and support.rho_label(tangent, omitted[1]) == omitted[0],
            "the shared/omitted source-label orbits changed")
    require(shared_fixed not in omitted,
            "the shared fixed grade became an actual tau_plus omitted grade")
    return {
        "formal_fixed_product_rule_seed": {
            "source_label": [shared_fixed[0], list(shared_fixed[1])],
            "rho_orbit_size": 1,
            "resolutions": "B1 or B4",
        },
        "actual_tau_plus_omitted_orbit": [
            [matching, list(edge)] for matching, edge in omitted
        ],
        "rho_orbit_size": 2,
        "local_sl3_changes_matching_or_repeated_edge": False,
        "consequence": (
            "starting from the B1/B4 shared-02 occurrence does not solve "
            "the actual 01/04 omitted-pair placement"
        ),
    }


def audit_cartan_scope():
    # The connected group statement is positive on word decoration.  The
    # signed Weyl is a product of root unipotents, hence its Cartan prism is
    # source-provenant.  But endpoint-even projection is not the annihilator
    # of endpoint-even readouts: (1+s) doubles them, whereas (1-s) kills them.
    endpoint_swap = (
        (0, 1, 0, 0),
        (1, 0, 0, 0),
        (0, 0, 0, 1),
        (0, 0, 1, 0),
    )
    one = tuple(tuple(Q(int(row == column)) for column in range(4))
                for row in range(4))
    even = tuple(tuple(one[row][column] + endpoint_swap[row][column]
                       for column in range(4)) for row in range(4))
    odd = tuple(tuple(one[row][column] - endpoint_swap[row][column]
                      for column in range(4)) for row in range(4))
    endpoint_even_rows = (
        (Q(1), Q(1), Q(0), Q(0)),
        (Q(0), Q(0), Q(1), Q(1)),
    )

    def row_matrix(row, matrix):
        return tuple(sum(row[index] * matrix[index][column]
                         for index in range(4)) for column in range(4))

    require(all(row_matrix(row, odd) == (0, 0, 0, 0)
                for row in endpoint_even_rows)
            and any(row_matrix(row, even) != (0, 0, 0, 0)
                    for row in endpoint_even_rows),
            "the endpoint even/odd protection split changed")
    return {
        "connected_group_positive": (
            "the local signed Weyl and H_w are explicit products/homotopies "
            "of physical SL3 root unipotents, so a correctly placed source "
            "column acquires its mixed root-word target without a new "
            "abstract group operation"
        ),
        "what_it_does_not_change": [
            "uncoloured B multiplier label",
            "matching/repeated-edge source grade",
        ],
        "W_zero_from_endpoint_even_parity": False,
        "reason": (
            "endpoint-even readouts are killed by 1-rho, not by the "
            "required root-even operator 1+rho"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    ledger = {
        "theorem": "connected SL3 label-orbit obstruction for tau_plus",
        "pins": PINS,
        "literal_connected_action": audit_connected_action_on_literal_columns(),
        "target_label_separator": audit_label_separation(),
        "source_repeated_grade_separator": audit_source_grade_separation(),
        "Cartan_scope": audit_cartan_scope(),
        "beta_zero": {
            "status": "separate",
            "remaining": "1 in theta(Z), or the selected D0 dual",
        },
        "verdict": (
            "the explicit connected two-root SL3/Weyl Cartan homotopy "
            "constructs root-word decoration but not the last tau_plus "
            "orbit.  From the actual omitted grade it remains in "
            "<B0,B2,B3,B5>; from the formal B1/B4 seed it remains in the "
            "wrong shared-02 repeated grade.  Hence it cannot supply "
            "delta_plus, the B1/B4-labelled mixed target/Eq/residue packet, "
            "or W=0 without the same relative placement/product-rule cell "
            "isolated by the full-interface gate"
        ),
        "connected_group_closes_even_interface": False,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("connected SL3 tau_plus ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 tau_plus connected SL3 shortcut: LABEL-ORBIT OBSTRUCTED")
    print("root/Weyl homotopy: physical and explicit")
    print("B-label action: roots identity; rho=(B0 B5)(B2 B3)")
    print("actual orbit <B0,B2,B3,B5> misses v=(B1+B4)/2")
    print("shared B1/B4 seed: wrong repeated-02 source grade")
    print("beta=0: independent D0 membership or dual")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

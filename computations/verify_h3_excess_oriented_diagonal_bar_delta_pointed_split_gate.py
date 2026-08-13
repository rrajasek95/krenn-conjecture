#!/usr/bin/env python3
"""Audit the oriented-diagonal bar on the excess loop-label kernel.

The five source loop labels map to one target excess normal.  Abstractly the
normalized bar of their pair groupoid contracts the rank-four augmentation
kernel; four tree edges suffice, and the selected rho-even delta-plus line
is one aggregate bar boundary.

Physical descent is not automatic.  The endpoint/Bianchi bar realizes this
boundary in the bare Q_tail row.  The desired tau-plus correction is a pure
full-nine boundary with 540 private features and Eq zero.  Existing complete
rows and M_v packets tie each private B_i pivot to Eq_i, so the primitive
rho-even dual chi_D reads 12 on the desired bridge and zero on the known
image.  The minimal selected new cell is therefore a common-tail comparison
J_D with (pure,Eq,Q_tail)=(D,0,-D), all protected/ridge/W rows zero, in the
actual tau-plus word/fine/repeated grade.  Adding the known Q_tail bar gives
the required (D,0,0).

J_D cannot also be the pointed d(u_f-u) cell: D has augmentation zero and
the bridge is anchor/protected zero, whereas the pointed conormal reads one
on the marked tangent.  They are independent and occupy different filtered
degrees.  One pointed comparison morphism may contain both, but its minimal
source extension has two homogeneous generators: the degree-one Koszul
generator of the degree-zero pointed diagonal relation, and the next
oriented common-tail bridge (plus forced word/ridge caps).
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py":
        "9e60fb8410288a192b8be3b59938e5e7ba4ea42b455fee67b94ca6ef37777fde",
    "computations/verify_h3_tau_plus_delta_literal_same_grade_gate.py":
        "f5d34986e086055dcba26e347c5a7f7470d9ec62a1346c9c872a8e828ec7b266",
    "computations/verify_h3_tau_plus_bianchi_tail_chain_typing_guard.py":
        "0733c4e93a729cf530c8725e03857a7a6af56e5e3577273524330d31250b6000",
    "computations/verify_h3_anchor_conormal_functoriality_bridge.py":
        "83879756547765878c36944c1ab14827ab77a1f217931bc05db0c72cb0af32a8",
    "computations/verify_h3_selected_lower_excess_orbit_pointed_comparison_gate.py":
        "057ca135e410ccf597a90a034e08868b3c901223981ca68662d6ad72414e4759",
}
EXPECTED_LEDGER_SHA256 = "a47be3990418d2b7a4f0082ef4ede2bb7e21a343e990b5f0aec497560b05dc69"

D = (Q(-1), Q(2), Q(-1), Q(-1), Q(2), Q(-1))
DELTA = tuple(value / 4 for value in D)
RHO_B = (5, 1, 3, 2, 4, 0)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


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


def unit(index: int, size: int):
    return tuple(Q(position == index) for position in range(size))


def abstract_loop_bar_audit():
    # Vertices are source loops 02,03,05,23,25.  Target excess forgets the
    # vertex, so its kernel is the augmentation-zero lattice.  A star tree
    # based at 25 gives an integral basis of bar boundaries.
    labels = ("02", "03", "05", "23", "25")
    augmentation = (Q(1),) * len(labels)
    tree_edges = tuple(add(unit(index, 5), scale(-1, unit(4, 5)))
                       for index in range(4))
    require(rank(tree_edges) == 4
            and all(dot(augmentation, edge) == 0 for edge in tree_edges),
            "the oriented loop-label bar stopped contracting the kernel")
    for vector in (
        (Q(1), Q(-1), Q(0), Q(0), Q(0)),
        (Q(2), Q(-3), Q(4), Q(-5), Q(2)),
    ):
        require(sum(vector, Q(0)) == 0
                and rank(tree_edges + (vector,)) == 4,
                "a zero-sum loop vector left the bar boundary span")
    return {
        "loop_labels": list(labels),
        "target_excess_direction": "2e4",
        "augmentation_kernel_rank": 4,
        "normalized_tree_bar_edges": 4,
        "full_loop_label_kernel_abstractly_contractible": True,
        "selected_even_line_needs_aggregate_bar_generators": 1,
    }


def selected_delta_bar_audit():
    # The shared-02 and local tau-plus resolutions differ by delta_plus.
    v = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    local = (Q(1, 4), Q(0), Q(1, 4),
             Q(1, 4), Q(0), Q(1, 4))
    require(add(v, scale(-1, local)) == DELTA
            and tuple(DELTA[index] for index in RHO_B) == DELTA
            and sum(DELTA, Q(0)) == 0,
            "the selected oriented delta bar changed")

    # Four source-valid endpoint differences factor the integral D in the
    # bare Q_tail row.
    b = tuple(unit(index, 6) for index in range(6))
    endpoint_factorization = add(
        add(b[1], scale(-1, b[0])),
        add(b[1], scale(-1, b[2])),
        add(b[4], scale(-1, b[3])),
        add(b[4], scale(-1, b[5])),
    )
    require(endpoint_factorization == D,
            "the four endpoint bars stopped factoring D")
    return {
        "shared_02_even_tail": [str(value) for value in v],
        "actual_tau_plus_local_tail": [str(value) for value in local],
        "delta_plus": [str(value) for value in DELTA],
        "integral_D": [int(value) for value in D],
        "rho_even": True,
        "augmentation": 0,
        "bare_Q_tail_factorization": (
            "(B1-B0)+(B1-B2)+(B4-B3)+(B4-B5)"
        ),
        "endpoint_Omega_ores_target_ainc_W": [0, 0, 0, 0, 0],
    }


def physical_row_type_and_dual_audit():
    # Rows are (private_B_6, Eq_6, Q_tail_6).  Old complete/M_v columns are
    # diagonal in private/Eq.  Endpoint bars occupy Q_tail only.
    diagonal = []
    for index in range(6):
        e = unit(index, 6)
        diagonal.append(e + e + (Q(0),) * 6)
    q_columns = tuple((Q(0),) * 12 + unit(index, 6)
                      for index in range(6))
    known = tuple(diagonal) + q_columns
    desired_pure = D + (Q(0),) * 12
    endpoint_q = (Q(0),) * 12 + D
    comparison = D + (Q(0),) * 6 + tuple(-value for value in D)
    chi = D + tuple(-value for value in D) + (Q(0),) * 6
    require(all(dot(chi, column) == 0 for column in known)
            and dot(chi, desired_pure) == dot(chi, comparison) == 12
            and add(comparison, endpoint_q) == desired_pure,
            "the pure/Eq/Q-tail comparison obstruction changed")
    require(rank(known + (desired_pure,)) == rank(known) + 1,
            "the selected physical bridge stopped being one new class")
    return {
        "row_order": ["private_B_6", "Eq_6", "Q_tail_6"],
        "known_complete_and_Mv_type": "(x,x,0)",
        "known_endpoint_bar_type": "(0,0,q)",
        "desired_integral_pure_bridge": "(D,0,0)",
        "minimal_common_tail_cell_J_D": "(D,0,-D)",
        "identity": "J_D+(0,0,D)=(D,0,0)",
        "primitive_dual": "chi_D=sum_i D_i(private_i-Eq_i)",
        "chi_D_on_known_image": 0,
        "chi_D_on_J_D": 12,
        "rank_jump": 1,
        "literal_desired_boundary_features": 540,
        "required_protected_rows": (
            "target=ainc=W=ores=ridge=wrong-word=0"
        ),
        "required_source_grade": (
            "actual tau-plus word/fine/repeated grade, rho-even"
        ),
    }


def pointed_independence_audit():
    # Abstract quotient coordinates are (selected delta bridge, pointed
    # conormal).  The first must be anchor/protected zero; the second pairs
    # one with the marked tangent.  They are independent target classes.
    delta_class = (Q(1), Q(0))
    pointed_class = (Q(0), Q(1))
    require(rank((delta_class, pointed_class)) == 2,
            "delta and pointed comparison classes met")

    # The integral delta coefficient has zero occurrence augmentation, so
    # no linear combination internal to that bar can acquire the marked
    # coefficient-one pointed value while preserving its required anchor=0.
    require(sum(D, Q(0)) == 0,
            "the delta bar acquired occurrence augmentation")
    return {
        "delta_bar_occurrence_augmentation": 0,
        "delta_bar_required_anchor": 0,
        "pointed_conormal": "d(u_f-u)",
        "pointed_conormal_on_marked_tangent": 1,
        "quotient_rank": 2,
        "one_homogeneous_cell_supplies_both": False,
        "reason": (
            "J_D is a rho-even augmentation-zero degree-one bar cell with "
            "protected anchor zero.  The pointed diagonal is a degree-zero "
            "source-presentation relation with nonzero marked cotangent"
        ),
        "one_comparison_morphism_can_package_both": True,
        "minimal_homogeneous_source_generators": [
            "P_f: degree-one Koszul/graph generator for the degree-zero relation u_f-u",
            "J_D: oriented common-tail bar in the next filtered degree",
        ],
    }


def word_ridge_guard():
    # The known endpoint differences cancel their local Omega/W rows.  This
    # does not prove that a cross-grade bar has no proper word/ridge faces.
    # Pin the first literal values from 5e4a6b8.
    source = (ROOT / (
        "computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py"
    )).read_text()
    require('"formal_even_residual_word": "012112"' in source
            and '"ridge_mismatch_rank": 6' in source
            and '"primitive_Omega_rank": 5' in source,
            "the oriented-bar word/ridge guard changed")
    return {
        "endpoint_difference_local_Omega_W": 0,
        "cross_grade_oriented_bar_word": "012112",
        "selected_midpoint_hit": False,
        "ridge_mismatch_rank": 6,
        "primitive_Omega_rank": 5,
        "consequence": (
            "J_D must be adjoined together with its source-labelled "
            "word-change and ridge/Omega caps; endpoint cancellation alone "
            "does not prove those proper faces vanish"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "excess oriented-diagonal bar / delta-pointed split gate",
        "pins": PINS,
        "abstract_loop_bar": abstract_loop_bar_audit(),
        "selected_delta_factorization": selected_delta_bar_audit(),
        "physical_row_type_and_dual": physical_row_type_and_dual_audit(),
        "word_ridge_W_guard": word_ridge_guard(),
        "pointed_independence": pointed_independence_audit(),
        "positive_conditional_assembly": (
            "adjoin J_D with boundary (pure,Eq,Q_tail)=(D,0,-D) in "
            "the actual tau-plus grade and cap its word/ridge proper faces. "
            "Adding the already source-valid endpoint bar (0,0,D) yields "
            "the protected pure bridge (D,0,0), so the local excess lift "
            "moves from w_local to v and closes delta_plus"
        ),
        "smallest_full_source_extension": {
            "selected_even_delta_only": (
                "one rho-even oriented common-tail cell J_D, plus its "
                "forced word/ridge caps"
            ),
            "uniform_all_loop_labels": (
                "four tree-edge cells before symmetry reduction"
            ),
            "pointed_full_comparison": (
                "J_D plus the independent marked/global diagonal generator"
            ),
        },
        "verdict": (
            "the relative oriented-diagonal bar kills the excess label "
            "kernel abstractly and factors delta_plus source-validly in the "
            "bare Q_tail row.  It does not kill the physical obstruction: "
            "one primitive pure-column/Eq comparison class J_D remains, "
            "with additional literal word/ridge caps.  J_D cannot itself "
            "supply d(u_f-u), although one pointed comparison morphism can "
            "contain both independent homogeneous components"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("oriented delta/pointed ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 excess oriented-diagonal bar: ABSTRACT YES / PHYSICAL ONE CLASS")
    print("full loop-label kernel: four tree bars; selected delta: one aggregate")
    print("minimal physical cell: J_D=(pure D, Eq 0, Q_tail -D)")
    print("chi_D(J_D)=12; word/ridge caps still required")
    print("pointed d(u_f-u): independent homogeneous generator")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

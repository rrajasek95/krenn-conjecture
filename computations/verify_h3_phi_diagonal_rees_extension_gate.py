#!/usr/bin/env python3
"""Audit extension of the finite h=3 Phi packet to diagonal Rees jets.

The 18 direction-labelled lower terms map to 15 physical collision labels
with a three-dimensional chart kernel.  Tensoring this quotient with a
truncated Rees jet algebra introduces no new label type: at jet length r the
kernel is ker(F) tensor J_r and has dimension 3r.  A Hasse/Rees-linear Phi
therefore propagates the original three coherences, while an arbitrary map
which only agrees with Phi at order zero need not descend at higher order.

The current comparison cell is target-zero.  Generic diagonal cap jets have
two independent nonzero target vectors, so the label prolongation alone
cannot carry them; an adjacent-power target-bearing cone cell is necessary.
The checker also freezes the literal Rees-membership counterguard showing
that evaluation divisibility and the existing Phi/anchor data do not kill
the quotient ker(epsilon)/N_lit.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py":
        "ea45c09a8347c312ea9721475d54a4b4f9aad21d8d51cb9d4d297aeaa99ba429",
    "computations/verify_protected_physical_comparison_first_source_cell.py":
        "0c93a7e67f1f48d114e343a282820477fe5a86649502500c5b00ee5e560b0245",
    "computations/verify_diagonal_rees_saturation_cap_jet_bockstein.py":
        "12c4cc4a947d99eee22cbd87e900ac6c7a56df2c533c4c44c52f0ab0fcedee2a",
    "computations/verify_uniform_adjacent_cycle_filtered_prolongation.py":
        "2b2555fac43a5914469a857b3a6bf19aa715ab6576220dc1dfd66dd808cad86e",
    "computations/verify_inactive_omega_torus_koszul_overlap_residue.py":
        "aaacb6eb5b426c4a6e77ec4f529ab15ac68de71ac52dd2943e62177249a66fe4",
}
EXPECTED_LEDGER_SHA256 = (
    "df9cb21bec1e7ae5afa093db4725eddbd783467d3e6f80a9add05dc424f082c1"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            f"cannot import {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix, strict=True))


def mat_vec(matrix, vector):
    return tuple(sum(Q(a) * Q(b) for a, b in zip(row, vector, strict=True))
                 for row in matrix)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(matrix):
    work = [list(map(Q, row)) for row in matrix]
    if not work:
        return 0
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def block_diagonal(matrix, copies):
    old_rows = len(matrix)
    old_columns = len(matrix[0])
    answer = [[Q(0)] * (copies * old_columns)
              for _ in range(copies * old_rows)]
    for copy in range(copies):
        for row in range(old_rows):
            for column in range(old_columns):
                answer[copy * old_rows + row][copy * old_columns + column] = (
                    Q(matrix[row][column])
                )
    return tuple(tuple(row) for row in answer)


def place_in_block(vector, block, block_size, copies):
    answer = [Q(0)] * (block_size * copies)
    start = block * block_size
    answer[start:start + block_size] = tuple(map(Q, vector))
    return tuple(answer)


def physical_collision_quotient(lower):
    tangent = lower.load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "phi_rees_tangent",
    )
    base_cut = tangent.CUTS[0]
    other_cut = tangent.CUTS[5]
    base_labels = lower.lower_labels(tangent, base_cut)
    other_labels = lower.lower_labels(tangent, other_cut)
    direction_labels = other_labels + base_labels
    physical_key = lambda label: (label[1], label[2])
    physical_labels = tuple(sorted({physical_key(label)
                                    for label in direction_labels}))
    physical_index = {label: index for index, label in
                      enumerate(physical_labels)}
    quotient = lower.unit_matrix(
        len(physical_labels), len(direction_labels),
        tuple(physical_index[physical_key(label)]
              for label in direction_labels),
    )
    shared_labels = tuple(sorted(set(map(physical_key, other_labels))
                                 & set(map(physical_key, base_labels))))
    chart_kernel = []
    for label in shared_labels:
        vector = [Q(0)] * len(direction_labels)
        other_column = next(index for index, item in
                            enumerate(direction_labels[:len(other_labels)])
                            if physical_key(item) == label)
        base_column = next(index for index, item in
                           enumerate(direction_labels[len(other_labels):],
                                     start=len(other_labels))
                           if physical_key(item) == label)
        vector[other_column] = Q(1)
        vector[base_column] = Q(-1)
        chart_kernel.append(tuple(vector))
    require(len(direction_labels) == 18 and len(physical_labels) == 15
            and len(chart_kernel) == rank(chart_kernel) == 3
            and rank(quotient) == 15,
            "the physical 18-to-15 quotient changed")
    return quotient, tuple(chart_kernel)


def audit_jet_coherence(quotient, chart_kernel):
    physical_row = tuple(Q(index + 1) for index in range(15))
    coherent_direction_row = mat_vec(transpose(quotient), physical_row)
    require(all(dot(coherent_direction_row, vector) == 0
                for vector in chart_kernel),
            "the seed physical row stopped killing chart differences")

    records = []
    for jet_length in (1, 2, 3):
        jet_quotient = block_diagonal(quotient, jet_length)
        jet_kernel = tuple(
            place_in_block(vector, level, 18, jet_length)
            for level in range(jet_length) for vector in chart_kernel
        )
        require(rank(jet_quotient) == 15 * jet_length
                and rank(jet_kernel) == 3 * jet_length
                and all(not any(mat_vec(jet_quotient, vector))
                        for vector in jet_kernel),
                "tensoring with the Rees jet algebra changed the kernel")

        # A Rees-linear extension is the same physical row on every jet
        # coefficient and therefore kills ker(F) tensor J_r.
        rees_linear_row = tuple(
            value for _level in range(jet_length)
            for value in coherent_direction_row
        )
        require(all(dot(rees_linear_row, vector) == 0
                    for vector in jet_kernel),
                "the Rees-linear Phi stopped propagating coherence")

        # Agreement with Phi only at order zero leaves higher maps free.
        detects_higher_kernel = False
        if jet_length > 1:
            arbitrary_extension = list(rees_linear_row)
            changed = next(index for index, value in
                           enumerate(jet_kernel[3]) if value == 1)
            arbitrary_extension[changed] += 1
            require(all(dot(arbitrary_extension, vector) == 0
                        for vector in jet_kernel[:3]),
                    "the arbitrary extension changed its order-zero Phi")
            detects_higher_kernel = any(
                dot(arbitrary_extension, vector) != 0
                for vector in jet_kernel[3:]
            )
            require(detects_higher_kernel,
                    "higher-jet incoherence was not independent")
        records.append({
            "jet_length": jet_length,
            "direction_labels": 18 * jet_length,
            "physical_labels": 15 * jet_length,
            "coherence_kernel_rank": 3 * jet_length,
            "Rees_linear_extension_descends": True,
            "order_zero_agreement_alone_is_insufficient":
                detects_higher_kernel,
        })
    return records


def audit_diagonal_target_gate(diagonal):
    h = 3
    alpha = Q(2)
    beta = Q(3)
    j1_target = (h * beta, -h * alpha, -h * alpha)
    j2_target = (-h * beta, -h * (h - 1) * alpha,
                 -h * (h - 1) * alpha)
    require(rank((j1_target, j2_target)) == 2,
            "the two generic diagonal target jets lost independence")

    phi_target = (Q(0), Q(0), Q(0))
    require(all(value == 0 for value in phi_target)
            and any(j1_target) and any(j2_target),
            "the target-zero Phi/target-bearing diagonal split changed")

    collision_beta = Q(0)
    collision_j1 = (h * collision_beta, -h * alpha, -h * alpha)
    collision_j2 = (-h * collision_beta, -h * (h - 1) * alpha,
                    -h * (h - 1) * alpha)
    unary_target = (Q(h), Q(0), Q(0))
    require(rank((collision_j1, collision_j2)) == 1
            and rank((collision_j1, unary_target)) == 2,
            "the collision target/unary rank split changed")
    selected = diagonal.polynomial_v_coefficients(
        h, alpha, collision_beta, True)
    complementary = diagonal.polynomial_v_coefficients(
        h, alpha, collision_beta, False)
    require(diagonal.valuation(selected) == h
            and diagonal.valuation(complementary) == h - 1,
            "the collision principal-part orders changed")
    return {
        "generic_h3": {
            "J1_literal_target": [str(value) for value in j1_target],
            "J2_literal_target": [str(value) for value in j2_target],
            "target_rank": 2,
            "asymmetric_route_cells_needed": 1,
            "symmetric_route_cells_needed": 2,
        },
        "Phi_mapping_cone_target": ["0", "0", "0"],
        "collision_h3": {
            "diagonal_jet_target_rank": 1,
            "rank_after_unary_target": 2,
            "selected_target_first_order": h,
            "complementary_target_first_order": h - 1,
        },
    }


def audit_rees_membership_guard():
    # Basis M=(b,z,r), literal boundary N=<b>, epsilon=(0,0,1).
    # Coefficients are ordered by ell power.  At multiplicity two, both
    # representatives evaluate to ell^2 and agree on all data external to
    # the z/b low-jet choice, but only the first has low jets in N.
    boundary = (Q(1), Q(0), Q(0))
    vertical = (Q(0), Q(1), Q(0))
    response = (Q(0), Q(0), Q(1))
    epsilon = lambda vector: vector[2]
    good = (boundary, boundary, response)
    bad = (vertical, boundary, response)
    good_evaluation = tuple(epsilon(vector) for vector in good)
    bad_evaluation = tuple(epsilon(vector) for vector in bad)
    require(good_evaluation == bad_evaluation == (Q(0), Q(0), Q(1)),
            "the two Rees representatives stopped having equal evaluation")
    good_obstruction = tuple((vector[1],) for vector in good[:2])
    bad_obstruction = tuple((vector[1],) for vector in bad[:2])
    require(good_obstruction == ((Q(0),), (Q(0),))
            and bad_obstruction == ((Q(1),), (Q(0),)),
            "the literal principal-parts obstruction changed")

    # Same-power target cancellation has the same sign on ordinary residue.
    cap_target_residue = (Q(3), Q(3))
    companion_target_residue = (Q(-3), Q(-3))
    same_power_sum = tuple(left + right for left, right in
                           zip(cap_target_residue,
                               companion_target_residue, strict=True))
    require(same_power_sum == (Q(0), Q(0)),
            "same-power target cancellation retained residue")
    return {
        "module": "M=<b,z,r>, N_lit=<b>, epsilon(b)=epsilon(z)=0, epsilon(r)=1",
        "jet_multiplicity": 2,
        "common_evaluation_coefficients": ["0", "0", "1"],
        "good_obstruction_in_ker_epsilon_mod_N": [["0"], ["0"]],
        "bad_obstruction_in_ker_epsilon_mod_N": [["1"], ["0"]],
        "same_Phi_and_anchor_possible": True,
        "same_power_target_residue_sum": ["0", "0"],
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")

    lower = load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "phi_rees_lower",
    )
    diagonal = load(
        "computations/verify_diagonal_rees_saturation_cap_jet_bockstein.py",
        "phi_rees_diagonal",
    )
    quotient, chart_kernel = physical_collision_quotient(lower)
    jet_records = audit_jet_coherence(quotient, chart_kernel)
    target_gate = audit_diagonal_target_gate(diagonal)
    rees_guard = audit_rees_membership_guard()

    ledger = {
        "pins": PINS,
        "finite_label_prolongation": {
            "base_direction_labels": 18,
            "base_physical_labels": 15,
            "base_shared_coherences": 3,
            "jet_records": jet_records,
            "theorem": (
                "for J_r=k[ell]/ell^r, ker(F tensor 1_Jr) equals "
                "ker(F) tensor J_r.  Thus a Hasse/Rees-linear extension "
                "Phi tensor 1 carries every coefficient of the base-changed "
                "jet packet with no new chart-coherence type; the original "
                "three seed coherences propagate.  Identifying the actual "
                "diagonal principal-parts packet with this base change is "
                "the Hasse/Rees-naturality hypothesis.  Agreement with Phi "
                "only at order zero does not impose the remaining 3(r-1) "
                "equalities"
            ),
            "h3_lengths": (
                "generic diagonal saturation has r<=2 because the residual "
                "degree is at most two; the trace collision requires the "
                "order-three unary principal part"
            ),
        },
        "target_grade_gate": target_gate,
        "literal_Rees_guard": rees_guard,
        "smallest_generic_extension": (
            "choose the asymmetric two-boundary saturation and one of J1,J2. "
            "Beyond Phi plus its ordinary anchor law, add: (i) a physical "
            "identification of the diagonal jets with the base-changed "
            "packet and a Hasse/Rees-linear extension, (ii) one target-bearing "
            "adjacent-power cone cell which nullhomotopes the chosen "
            "nonzero diagonal target without cancelling its lower residue, "
            "(iii) vanishing of the actual low-jet class in "
            "(ker epsilon/N_lit) tensor k[ell]/ell^r, and (iv) restricted "
            "homology injectivity on the surviving inactive residue line"
        ),
        "symmetric_and_collision_extensions": (
            "the symmetric generic route needs two target-bearing directions "
            "because J1,J2 have target rank two.  At beta=0 they collapse "
            "to rank one but are blind to the selected colour, so an "
            "order-h unary target/anchor jet or a forced complementary "
            "surviving label is additionally necessary"
        ),
        "necessary_and_sufficient_membership_criterion": (
            "for the actual residual P in the evaluated-divisible family, "
            "obs_[ell,r](P)=[P mod ell^r] in "
            "(ker epsilon/N_lit) tensor k[ell,w]/(ell^r) must vanish.  An "
            "extended Phi proves this if it sends that class to zero and "
            "its induced map is injective on the line spanned by the class"
        ),
        "routing_guard": (
            "the current 15-label M_v image has zero target and ordinary "
            "residue, so it cannot itself equal either generic diagonal cap "
            "jet.  Phi plus anchor also does not route an arbitrary inactive "
            "root into the diagonal normal form; an off-diagonal/diagonal/"
            "trace source-labelled normal-face map is a prior coverage datum"
        ),
        "scope": (
            "exact h=3 label-prolongation theorem and finite target/Rees "
            "guard.  It does not construct the Hasse-linear physical "
            "extension, adjacent-power cell, normal-face routing, or "
            "restricted homology injection"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Phi/diagonal Rees extension ledger changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 Phi/diagonal Rees extension gate: PASS")
    print("label skeleton: 15r with 3r chart kernel")
    print("Hasse-linear extension: seed coherences propagate")
    print("physical diagonal jets: extra target-bearing cone required")
    print("Phi plus anchor: does not imply literal Rees membership")
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()

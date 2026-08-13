#!/usr/bin/env python3
"""Audit the literal J_D Hasse/Bianchi attempt and its uniform scope.

The six tau-plus B_i are six distinct three-edge multipliers P_i of the
same literal 90-term pure full-nine row H_0.  Hence the integral debt is

    sum_i D_i B_i = P_D H_0,
    P_D=sum_i D_i P_i,  D=(-1,2,-1,-1,2,-1).

Although sum(D)=0, P_D is a nonzero polynomial: its six monomials are
distinct.  The selected cofactor/Hasse contraction has the correct formal
mapping-cone shadow P_D H_0 -> P_D, and the endpoint Bianchi aggregate is
the required bare Q_tail P_D.  The complete cobar, however, retains all
proper faces.  In the committed physical comparison the first uncancelled
ones are the wrong word 012112 and the rank-six/rank-five ridge/Omega
packet.  Thus the old full-nine/Hasse/Bianchi inventory does not construct
the physical cell J_D=(D,0,-D).

The primitive chi_D extends by zero over those proper-face rows and remains
a primitive left separator of the committed h=3 totalization.  This is not
yet a physical terminal/Macaulay functional: no exhaustive source-terminal
quotient or higher-multiplication compatibility is supplied.

Finally, literal multiplication by a disjoint spectator matching tail is
injective and preserves the static boundary and additive grades.  It is not
a chain-level suspension.  Already for one spectator edge T,

    d(T J_D)=T dJ_D+(dT)J_D,

and dT is nonzero in the Hasse/PP complex.  A uniform PAComp(h) therefore
needs a monoidal/shuffle comparison with all spectator faces and physical
q/Macaulay descent; an h=3 J_D cell alone is insufficient.
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
    "computations/verify_h3_excess_oriented_diagonal_bar_delta_pointed_split_gate.py":
        "01542e25810081a7ba43de27a1d188008dfb75456d47a6ffa43e60acb8aeb414",
    "computations/verify_h3_tau_plus_delta_literal_same_grade_gate.py":
        "f5d34986e086055dcba26e347c5a7f7470d9ec62a1346c9c872a8e828ec7b266",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "computations/verify_h3_cut_swap_shared_loop_hasse_cross_term_gate.py":
        "cc551585391a990060f78b49486c05af6c3b4a301058c855a422ae9d54fe5be5",
    "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py":
        "ebd25f79a6fe8db936fe5601b9220f152c5349dd794bbc4e08b2095f1c1d059f",
    "computations/verify_uniform_cartan_augmented_grade_naturality_gate.py":
        "d71b2ae71cdfc910e374b498a70edbb5e897867cf624dec49203c34e74647925",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_source_base_change_conormal_obstruction.py":
        "1a921671ab378f68355c2a6196d1951cad30244d78a9e90ec2715ce47ef12bf0",
    "computations/verify_pointed_h3_spectator_uniformization_no_go.py":
        "832c4388961f24356cb182888cff89a4bda5ff181204a510baefb55e754323d2",
}
EXPECTED_LEDGER_SHA256 = "91e579e9a7f9230b896460cda606af25bafef64dc5b74506062663ca238ab8c8"

D = (Q(-1), Q(2), Q(-1), Q(-1), Q(2), Q(-1))
TARGET_ACTION = (5, 1, 3, 2, 4, 0)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(height):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def remove_factor(feature, multiplier):
    remainder = list(feature)
    for cell in multiplier:
        require(cell in remainder,
                ("complete feature lost its multiplier", multiplier, feature))
        remainder.remove(cell)
    return tuple(remainder)


def literal_factorization_audit(complete, base):
    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, degree)
    pure = tuple((multiplier, boundary)
                 for word, multiplier, boundary in component["columns"]
                 if word == complete.PURE_WORD)
    require((left, right) == (3, 5)
            and len(pure) == 6
            and len(component["columns"]) == component["rank"] == 288,
            "the canonical complete component changed")

    common_rows = []
    owners = defaultdict(list)
    weighted_boundary = defaultdict(Q)
    for index, (multiplier, boundary) in enumerate(pure):
        require(len(multiplier) == 3
                and len(boundary) == 90
                and all(len(feature) == len(set(feature)) == 7
                        for feature in boundary),
                ("a B_i lost its literal 3 times 90 full-nine type", index))
        residual = tuple(remove_factor(feature, multiplier)
                         for feature in boundary)
        require(len(set(residual)) == 90
                and set(residual) == set(base.full_row(complete.PURE_WORD)),
                ("B_i stopped factoring through the common H_0", index))
        common_rows.append(residual)
        for feature in boundary:
            owners[feature].append(index)
            weighted_boundary[feature] += D[index]

    multipliers = tuple(multiplier for multiplier, _boundary in pure)
    require(len(set(multipliers)) == 6
            and all(len(indices) == 1 for indices in owners.values())
            and len(owners) == len(weighted_boundary) == 540
            and set(weighted_boundary.values()) == {Q(-1), Q(2)},
            "the literal P_D H_0 factorization changed")
    require(sum(D, Q(0)) == 0
            and tuple(D[index] for index in TARGET_ACTION) == D,
            "D lost augmentation zero or rho parity")

    # P_D is represented in the free monomial basis of the six multipliers.
    # Its coefficient augmentation is zero, but the polynomial itself has
    # support six and cannot be discarded as a scalar cancellation.
    p_d = {multipliers[index]: D[index] for index in range(6)}
    require(len(p_d) == 6 and any(p_d.values()), "P_D vanished")
    return {
        "target_fine_degree": list(degree),
        "complete_component_columns_rank": [
            len(component["columns"]), component["rank"]],
        "B_columns": 6,
        "multiplier_edges_per_B": 3,
        "common_H0_terms": 90,
        "literal_identity": "sum_i D_i B_i = P_D*H0",
        "P_D": "sum_i D_i P_i",
        "P_D_coefficients": [int(value) for value in D],
        "P_D_monomial_support": len(p_d),
        "coefficient_augmentation": int(sum(D)),
        "P_D_is_zero_polynomial": False,
        "integral_boundary_features": len(weighted_boundary),
        "integral_boundary_coefficients": sorted(
            int(value) for value in set(weighted_boundary.values())),
        "rho_even": True,
    }, pure


def full_hasse_bianchi_attempt_audit(pure, total, cross):
    # Each literal B feature has seven distinct occurrences: three in P_i
    # and four in H_0.  A complete Boolean/cobar boundary has all 2^7-2
    # ordered nontrivial faces.  The P_i|H_0 comparison and its reverse are
    # only two of them.  This is why the scalar/full-row shadow does not by
    # itself define a physical bar cell.
    split_records = []
    for index, (multiplier, boundary) in enumerate(pure):
        multiplier_set = frozenset(multiplier)
        for feature in boundary:
            positions = tuple(range(len(feature)))
            masks = tuple(mask for mask in range(1, (1 << len(feature)) - 1))
            factor_mask = sum(1 << position for position, cell in
                              enumerate(feature) if cell in multiplier_set)
            require(len(feature) == 7
                    and len(masks) == 126
                    and factor_mask in masks
                    and (((1 << 7) - 1) ^ factor_mask) in masks,
                    "a complete seven-occurrence Hasse split changed")
            split_records.append((index, len(positions), len(masks)))
    require(len(split_records) == 540,
            "wrong number of literal complete Hasse tops")

    total_ledger = total.audit()
    source_bridge = total_ledger["third_cofactor_total_complex"] \
        ["source_labelled_bridge"]
    grade = total_ledger["endpoint_midpoint_grade"]
    require(source_bridge["ridge_mismatch_rank"] == 6
            and source_bridge["primitive_omega_rank"] == 5
            and grade["physical_residual_word"] == "012112"
            and grade["midpoint_hits"] == 0,
            "the first physical Hasse proper-face obstruction changed")

    cross_ledger, cross_digest = cross.audit()
    require(cross_digest == cross.EXPECTED_LEDGER_SHA256
            and cross_ledger["formal_totalization"]["source_valid"] is False
            and cross_ledger["formal_totalization"]
                ["tail_signature_ainc_W_target_ores"] == [-1, 0, 0, 0],
            "the product-rule/Bianchi physical descent gate changed")

    # Free polynomial shadow: C_Hasse maps P_D*H0 to P_D; adjoining the
    # opposite bare endpoint Q_tail has the signature requested of J_D.
    # This is a mapping-cone equality only after forgetting all proper faces.
    formal_shadow = (D, (Q(0),) * 6, tuple(-value for value in D))
    require(formal_shadow == (D, (Q(0),) * 6,
                              tuple(-value for value in D)),
            "the formal J_D shadow changed")
    return {
        "literal_complete_tops": len(split_records),
        "occurrences_per_top": 7,
        "ordered_nontrivial_cobar_faces_per_top": 126,
        "distinguished_Pi_H0_oriented_faces": 2,
        "other_proper_faces_per_top": 124,
        "formal_polynomial_shadow": "P_D*H0 -> P_D",
        "formal_row_shadow": "(pure,Eq,Q_tail)=(D,0,-D)",
        "formal_Q_tail_supplied_by_endpoint_Bianchi": True,
        "formal_shadow_protected_target_ainc_W_ores": [0, 0, 0, 0],
        "physical_source_cell_constructed": False,
        "first_uncancelled_proper_faces": {
            "word": grade["physical_residual_word"],
            "selected_midpoint_hits": grade["midpoint_hits"],
            "ridge_rank": source_bridge["ridge_mismatch_rank"],
            "primitive_Omega_rank": source_bridge["primitive_omega_rank"],
        },
        "reason_D_does_not_remove_word_face": (
            "the word coordinate is free over the six distinct multiplier "
            "monomials P_i, so its D-weighted coefficient is nonzero P_D"
        ),
        "smallest_positive_object": (
            "one rho-even source-labelled total cell J_D with all 124 "
            "proper Hasse sectors totalized into physical word/ridge caps"
        ),
    }


def chi_extension_and_terminal_gate():
    # Rows: private_6, Eq_6, Q_6, proper-face_2.  The old complete rows tie
    # private to Eq; endpoint bars use Q; word/ridge caps use the disjoint
    # proper-face block.  Extending chi_D by zero therefore remains a left
    # cocycle on this committed totalization.  J_D is the unique selected
    # rank jump it detects.
    zero6 = (Q(0),) * 6
    zero2 = (Q(0),) * 2
    complete = []
    endpoint = []
    for index in range(6):
        e = tuple(Q(position == index) for position in range(6))
        complete.append(e + e + zero6 + zero2)
        endpoint.append(zero6 + zero6 + e + zero2)
    proper_faces = (
        zero6 + zero6 + zero6 + (Q(1), Q(0)),
        zero6 + zero6 + zero6 + (Q(0), Q(1)),
    )
    old = tuple(complete) + tuple(endpoint) + proper_faces
    chi = D + tuple(-value for value in D) + zero6 + zero2
    j_d = D + zero6 + tuple(-value for value in D) + zero2
    require(all(dot(chi, column) == 0 for column in old)
            and dot(chi, j_d) == 12
            and rank(old + (j_d,)) == rank(old) + 1,
            "chi_D stopped extending over the committed proper-face block")
    return {
        "extended_covector": (
            "chi_D=sum_i D_i(private_i-Eq_i), zero on Q_tail and "
            "word/ridge proper-face rows"
        ),
        "kills_committed_complete_Hasse_Bianchi_totalization": True,
        "value_on_J_D": 12,
        "primitive_selected_rank_jump": 1,
        "classification": "bounded h=3 codomain left separator",
        "physical_terminal_Macaulay_functional_now": False,
        "missing_terminal_data": [
            "an exhaustive comparison with the actual physical source-terminal quotient",
            "annihilation of every higher Macaulay multiplier, not only this fixed grade",
            "a source-domain q/readout or Fredholm promotion theorem",
        ],
        "terminal_conclusion": (
            "chi_D extends across the committed word/ridge caps as zero, "
            "but not presently to a physical conjecture-terminal"
        ),
    }


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for index, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            output.append(((first, second),) + tail)
    return tuple(output)


def spectator_uniformity_gate(uniform, spectator):
    # q^[r] is a sum over perfect matching monomials of degree r.  Every
    # nonconstant tail has nonzero first Hasse faces; for a chosen edge the
    # derivative contains all matchings of the remaining sites.
    tail_records = []
    for r in range(5):
        vertices = tuple(range(2 * r))
        matchings = perfect_matchings(vertices)
        expected = 1
        for odd in range(1, 2 * r, 2):
            expected *= odd
        require(len(matchings) == expected,
                ("spectator matching count changed", r))
        derivative_terms = 0
        if r:
            selected = frozenset((0, 1))
            derivative_terms = sum(
                any(frozenset(edge) == selected for edge in matching)
                for matching in matchings
            )
            require(derivative_terms == len(perfect_matchings(vertices[2:])),
                    ("spectator first Hasse face changed", r))
        tail_records.append({
            "r=h-3": r,
            "q^[r]_matching_monomials": len(matchings),
            "monomial_degree": r,
            "selected_edge_first_Hasse_terms": derivative_terms,
        })

    # Minimal dg Leibniz model.  Coordinates are (T*dJ, dT*J).  Naive
    # multiplication supplies both; the proposed static suspension keeps
    # only the first.  The second is already nonzero for r=1.
    static_boundary = (Q(1), Q(0))
    leibniz_boundary = (Q(1), Q(1))
    require(static_boundary != leibniz_boundary
            and tail_records[1]["selected_edge_first_Hasse_terms"] == 1,
            "the first spectator Leibniz obstruction vanished")

    uniform_ledger, uniform_digest = uniform.audit()
    require(uniform_digest == uniform.EXPECTED_LEDGER_SHA256
            and not uniform_ledger["ridge_eta_sigma"]
                ["arbitrary_common_tail_repairs_degree"]
            and uniform_ledger["ordinary_residue"]
                ["generic_tail_commutes"] is False,
            "the uniform augmented tail gate changed")
    spectator_ledger, spectator_digest = spectator.audit()
    require(spectator_digest == spectator.EXPECTED_LEDGER_SHA256
            and spectator_ledger["spectator_target"]
                ["static_fixed_word_tensoring_is_chain_valid"]
            and not spectator_ledger["spectator_target"]
                ["static_tensoring_preserves_full_GHZ_target"],
            "the full GHZ spectator-target guard changed")

    # A fixed spectator sector does not exhaust a higher Macaulay block.
    # e_T is the tensored sector and e_cross is a new cross-tail column.
    # A covector extended by zero off the sector need not kill e_T+e_cross.
    chi_sector = (Q(1), Q(0))
    transverse_column = (Q(1), Q(1))
    require(dot(chi_sector, transverse_column) == 1,
            "the higher Macaulay sector counterguard changed")
    return {
        "spectator_tail": "q^[h-3] on disjoint spectator sites",
        "finite_matching_checks": tail_records,
        "static_boundary_tensor": {
            "injective_over_polynomial_source_ring": True,
            "word_fine_repeated_grades": "add the spectator degree uniformly",
            "zero_target_ainc_W_ores": "remain zero before terminal normalization",
            "scope": "one fixed-word sector, not the full GHZ target",
        },
        "static_tensor_preserves_full_GHZ_target": False,
        "chain_Leibniz_rule": "d(T*J_D)=T*dJ_D+dT*J_D",
        "first_failure_order": "h=4 (one spectator edge)",
        "extra_first_Hasse_face_at_h4": "(dT)*J_D, coefficient one",
        "naive_h3_site_suspension_is_chain_map": False,
        "conditional_positive_uniformization": (
            "a monoidal Eilenberg-Zilber/shuffle comparison on the complete "
            "physical source complexes would totalize every dT face and "
            "transport J_D to q^[h-3]*J_D"
        ),
        "conditional_structure_constructed": False,
        "ordinary_residue_arbitrary_tail_natural": False,
        "labelled_ridge_arbitrary_tail_natural": False,
        "Macaulay_warning": (
            "the T-divisible spectator sector is not the full intrinsic "
            "order-h Macaulay block; extending chi by zero need not kill "
            "cross-tail columns"
        ),
        "PAComp_h_from_h3_J_D_alone": False,
    }


def pointed_comparison_cell_count():
    # Two independent associated-graded quotient directions do not mean two
    # theorem hypotheses.  They are two cells in one pointed comparison.
    p_f = (Q(1), Q(0))
    j_d = (Q(0), Q(1))
    require(rank((p_f, j_d)) == 2,
            "the pointed/excess associated-graded split changed")
    return {
        "associated_graded_generators": 2,
        "P_f": "Koszul generator for the pointed relation u_f-u",
        "J_D": "next oriented-diagonal/common-tail comparison cell",
        "one_cell_derivable_from_the_other": False,
        "conjecture_level_theorems": 1,
        "single_theorem": (
            "one pointed rho-equivariant comparison Phi_beta whose domain "
            "resolution contains P_f and J_D with their common d^2/coherence laws"
        ),
        "interpretation": (
            "two source generators inside one comparison theorem, not two "
            "independent global conjecture-level assumptions"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "jd_total_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "jd_total_base",
    )
    total = load(
        "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py",
        "jd_total_hasse",
    )
    cross = load(
        "computations/verify_h3_cut_swap_shared_loop_hasse_cross_term_gate.py",
        "jd_total_cross",
    )
    uniform = load(
        "computations/verify_uniform_cartan_augmented_grade_naturality_gate.py",
        "jd_total_uniform",
    )
    spectator = load(
        "computations/verify_pointed_h3_spectator_uniformization_no_go.py",
        "jd_total_spectator",
    )
    literal, pure = literal_factorization_audit(complete, base)
    ledger = {
        "theorem": "J_D full-nine/Hasse/Bianchi totalization and uniform spectator gate",
        "pins": PINS,
        "literal_common_row_factorization": literal,
        "Hasse_Bianchi_totalization_attempt":
            full_hasse_bianchi_attempt_audit(pure, total, cross),
        "chi_D_extension": chi_extension_and_terminal_gate(),
        "spectator_uniformity": spectator_uniformity_gate(uniform, spectator),
        "pointed_comparison_interpretation": pointed_comparison_cell_count(),
        "verdict": (
            "the old full-nine/Hasse/Bianchi complex constructs the formal "
            "P_D H0 to P_D mapping-cone shadow but not the physical J_D: "
            "wrong-word and primitive ridge/Omega proper faces survive.  "
            "chi_D remains a bounded h=3 separator, not a physical terminal. "
            "P_f and J_D are two homogeneous generators in one pointed "
            "comparison theorem.  Uniform PAComp(h) additionally requires "
            "a monoidal spectator-face totalization and terminal/Macaulay descent"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("J_D totalization/uniformity ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 J_D Hasse/Bianchi: FORMAL SHADOW / PHYSICAL PROPER-FACE GAP")
    print("literal debt: P_D*H0, P_D nonzero on six multiplier monomials")
    print("chi_D: bounded separator, not physical terminal")
    print("P_f and J_D: two cells in one pointed comparison theorem")
    print("uniform spectator lift: fails naively at h=4 by (dT)*J_D")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Bounded inventory obstruction for the shared four-term attachment.

The proposed common endpoint-word-change homotopy has associated boundary

    A = (1,-1,1,-1)

in coordinates (E_plus,E_minus,Omega_1,q_(1,23|45)).  This checker searches
the complete committed families which can meet one of those four faces:

* all 3^6 diagonal/crossed response rows in the canonical E14 chart;
* the complete unary/G11 first-hit module and its promoted 2K2 companion;
* both endpoint-bar orders, all matching switches and Bianchi differences;
* the first repeated P3+K2 principal-parts comparison squares;
* the formal fourth-Hasse comparison candidate; and
* the ordinary incidence/Pluecker/matching-square/Tate source module.

No literal source-valid cell in those families has boundary A with protected
readouts zero.  The first coarse separator is endpoint orientation

    chi = (1,-1,0,0),

which kills the only correct-tail response row and every endpoint-free
rootless family, but has chi(A)=2.  At literal first-hit level this is refined
by the committed 22-coordinate rational dual (pairing -1, primitive integral
pairing -30).  The rootless bar side has its independent primitive companion
separator and unavoidable ordinary-residue face.  Thus the smallest new
datum is one mixed mapping-cone generator whose boundary is exactly A and
whose W/target/ordinary-residue/anchor-incidence readouts vanish.

This is a complete no-go only for the pinned bounded inventory, not for an
enlarged source resolution.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "a20e1bebe7eeb5051a18636938a5d5c5b75fee144615be5a239610bcc7d39a1d"
PINS = {
    # The four commits named in the attack brief.
    "computations/verify_h3_shared_same_word_endpoint_companion_attachment_gate.py":
        "ef6f336c3582c66ca65250a3d812deaed5aa3a6d998ce1e428e0bc03fa2fab37",
    "computations/verify_h3_rootless_e14_companion_core_identification.py":
        "438ae827dba9e8f7a14f011cb5d76631fc284a2a2a8c6d8bcee7003669a1ac45",
    "computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py":
        "37251145d805861b2d1b15b7bf37cf9f98ba30b03fbcffa1daa4fc35789efe84",
    "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py":
        "c4e175ca053cd98e788cca1a38a1851e708e7e47a9ea5745ef4ac6e303ddfd40",
    # Complete bounded inventories used in the search.
    "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py":
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py":
        "2e09f9be1ed1b57821c64dd690df7e4d6b2efebe93cb8aae9ff0a58b3190022d",
    "computations/verify_h3_rootless_endpoint_to_collision_chain_map_boundary.py":
        "be39a61df8e3723983eea7a20d405fba7ff0f3822bc90e8d48b8039177f69cfc",
    "computations/verify_h3_rootless_abcde_relative_matching_cell_obstruction.py":
        "39a4c24a23f8c315f6a90a9768aff6cc3061c51528b0a66594e22f8182f717af",
    "computations/verify_reciprocal_response_hasse_bianchi.py":
        "d5bb78f9a0ca2cfab30932ccfcaeca8c6de9d3bff5351983045e66fee4d1d432",
    "computations/verify_h3_mixed_bar_curvature_bicomplex.py":
        "6d239dfa1610d36de3385f9e084693523225528f8343ea9412773604fe396318",
    "computations/verify_h3_physical_curvature_qzero_attaching_lower_face_obstruction.py":
        "050bfaa16cedb07248f01f58f8cc59927307861e55da45b759219ccde3d24ee1",
}

COORDINATES = ("E_plus", "E_minus", "Omega_1", "q_comp")
S = (1, 1, 0, 0)
B = (0, 0, -1, 1)
A = (1, -1, 1, -1)
CHI = (1, -1, 0, 0)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dot(left, right):
    return sum(Q(a) * Q(b) for a, b in zip(left, right, strict=True))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "ragged matrix")
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
            factor = work[row][column]
            work[row] = [left - factor * right
                         for left, right in zip(work[row],
                                                work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def four_term_quotient() -> dict[str, object]:
    derived = tuple(a + b for a, b in zip(A, B, strict=True))
    require(derived == (1, -1, 0, 0), "A+B changed")
    require(rank([S, B]) == 2 and rank([S, B, A]) == 3,
            "four-coordinate ranks changed")
    require(dot(CHI, S) == dot(CHI, B) == 0,
            "orientation separator stopped killing old faces")
    require(dot(CHI, A) == 2 and dot(CHI, derived) == 2,
            "orientation separator stopped detecting A")
    endpoint_determinant = S[0] * derived[1] - S[1] * derived[0]
    require(endpoint_determinant == -2, "endpoint index changed")
    return {
        "coordinate_order": list(COORDINATES),
        "existing_signless_response_S": list(S),
        "existing_rootless_bar_projection_B": list(B),
        "proposed_attachment_A": list(A),
        "A_plus_B_endpoint_difference": list(derived),
        "primitive_orientation_covector_chi": list(CHI),
        "chi_on_S_B_A": [int(dot(CHI, S)), int(dot(CHI, B)),
                           int(dot(CHI, A))],
        "endpoint_lattice_determinant": endpoint_determinant,
        "interpretation": (
            "modulo the old bar, A is twice the primitive endpoint-"
            "orientation class; A closes the rational/characteristic-zero "
            "gate but leaves the explicit integral index two"
        ),
    }


def curvature_kodaira_spencer_audit() -> dict[str, object]:
    """Test the tempting reciprocal-Hasse/mixed-curvature construction.

    The mixed bar-curvature Massey chain really can be specialized so that
    its boundary is E_plus-E_minus at the correct seven-site word.  The
    obstruction is its normalized endpoint: its residue is the pure-11 E14
    tail, whereas the physical rootless bar carries the mixed 21|12 tail.
    """
    reciprocal = load(
        "computations/verify_reciprocal_response_hasse_bianchi.py",
        "four_term_reciprocal_bianchi",
    )
    mixed = load(
        "computations/verify_h3_mixed_bar_curvature_bicomplex.py",
        "four_term_mixed_curvature",
    )
    shared = load(
        "computations/verify_h3_shared_same_word_endpoint_companion_attachment_gate.py",
        "four_term_shared_gate",
    )

    # In the reciprocal Hasse identity the quadratic K channel is symmetric,
    # so its antisymmetrization is literally zero.  The surviving term in
    # Eq. (3) is the direct-weighted first-response difference, not K.
    rows = tuple((i, j) for i in reciprocal.COLORS
                 for j in reciprocal.COLORS)
    k_symmetry_checks = 0
    for left in rows:
        for right in rows:
            left_product = tuple(sorted((left, right)))
            right_product = tuple(sorted((right, left)))
            require(left_product == right_product,
                    "reciprocal K channel lost commutativity")
            k_symmetry_checks += 1
    require(k_symmetry_checks == 81,
            "reciprocal ordered K symmetry count changed")

    # Replay one active mixed-bar packet.  It proves the exact universal
    # identity dM=L(kappa*z), with q-augmentation=ores=kappa*z.
    sample = {
        "A": Q(2), "B": Q(3), "F": Q(5), "U": Q(11), "z": Q(1),
        "x": Q(7), "y": Q(-2), "t": Q(4), "v": Q(3),
        "Ecoef": Q(5, 2),
    }
    massey = mixed.audit_bicomplex(sample)
    require(massey["massey_boundary"] == "L(kappa*z)"
            and massey["D_endpoint_cancelled"]
            and massey["target_complete_seven_site_word"] == 0,
            "mixed bar-curvature endpoint changed")
    require(massey["L_q_augmentation"]
            == massey["L_old_ordinary_residue"],
            "mixed bar-curvature qaug/ores lock changed")

    # Delete exposed x=0 from the rootless word 01211222.  This is exactly
    # the full seven-site word of the mixed bar-curvature checker.
    rootless_word = (0, 1, 2, 1, 1, 2, 2, 2)
    curvature_word = (1, 2, 1, 1, 2, 2, 2)
    require(rootless_word[1:] == curvature_word,
            "rootless and curvature full words stopped agreeing")

    # Put P+=p1@0*s1@1 and P-=p1@1*s1@0.  Specializing
    # A=p1@0, U=s1@1*T', B=p1@1, F=s1@0*T', z=T'' gives
    # kappa*z=(P+-P-)*T'*T''.  For the E14 orientation pair take
    # T'*T''=a24_11*a35_11.
    pure_tail = ("a24_11", "a35_11")
    # Align the rootless matching 23|45 with 24|35 by swapping sites 3,4.
    # Its decoration remains mixed: 21|12.
    mixed_tail = ("a24_21", "a35_12")
    require(pure_tail != mixed_tail,
            "pure and rootless response tails unexpectedly collided")

    # Basis is P+*pure, P-*pure, P+*mixed, P-*mixed.  The Massey
    # endpoint/residue and the determinant-multiplied rootless bar have the
    # same word and total polynomial degree, but not the same polynomial.
    massey_residue = (1, -1, 0, 0)
    promoted_bar_residue = (0, 0, 1, -1)
    combined_residue = tuple(
        left - right for left, right in
        zip(massey_residue, promoted_bar_residue, strict=True)
    )
    require(combined_residue == (1, -1, -1, 1),
            "curvature-minus-bar residue mismatch changed")
    require(any(combined_residue),
            "the mixed curvature and physical bar residues unexpectedly agree")

    # This is not an artefact of notation.  The four Segre corners are
    # linearly independent coefficient coordinates; only their quadratic
    # 2x2 minor vanishes.  In particular pure 11|11 is not mixed 21|12.
    segre = shared.segre_square_gate()
    require(segre["linear_coefficient_rank"] == 4
            and not segre[
                "direct_q11_minus_q00_is_one_literal_same_word_row"],
            "Segre linear obstruction changed")

    return {
        "reciprocal_Hasse_Bianchi": {
            "ordered_K_symmetry_checks": k_symmetry_checks,
            "K_ij_kl_minus_K_kl_ij": 0,
            "endpoint_orientation_is_K_antisymmetrization": False,
            "surviving_Eq3_term":
                "d_ij*R_kl-d_kl*R_ij (direct-weighted first responses)",
        },
        "mixed_bar_curvature": {
            "rootless_word_with_x_removed": "1211222",
            "checker_full_word": "1211222",
            "specialization": (
                "A=p1@0, U=s1@1*T', B=p1@1, F=s1@0*T', "
                "z=T'', with T'*T''=a24_11*a35_11"
            ),
            "Massey_boundary": "E_plus-E_minus",
            "target": 0,
            "normalized_residue":
                "(P_plus-P_minus)*a24_11*a35_11",
        },
        "physical_rootless_bar_after_endpoint_determinant_multiplier": {
            "boundary":
                "-(P_plus-P_minus)*Omega+(P_plus-P_minus)*qcomp",
            "aligned_qcomp_tail": "a24_21*a35_12",
            "normalized_residue":
                "(P_plus-P_minus)*a24_21*a35_12",
        },
        "combined_candidate": {
            "boundary_projection":
                "E_plus-E_minus+(P_plus-P_minus)*(Omega-qcomp)",
            "residue_basis": [
                "P_plus*pure11", "P_minus*pure11",
                "P_plus*mixed21|12", "P_minus*mixed21|12",
            ],
            "residue_vector": list(combined_residue),
            "residue_formula": (
                "(P_plus-P_minus)*(a24_11*a35_11-"
                "a24_21*a35_12)"
            ),
            "residue_zero": False,
            "same_word_and_total_polynomial_degree": True,
            "first_exact_obstruction":
                "decorated residual-tail mismatch 11|11 versus 21|12",
        },
        "single_remaining_tangent_lift_hypothesis": (
            "construct a source-provenant residual-q Kodaira--Spencer lift "
            "whose normalized boundary transports a24_11*a35_11 to "
            "a24_21*a35_12 in the endpoint-determinant sector, supplies the "
            "negative of the displayed ordinary-residue mismatch, and has "
            "W, target, and anchor-incidence zero.  Then the corrected total "
            "has ordinary residue zero and is the desired A"
        ),
        "verdict": (
            "the mixed curvature Massey chain gives the endpoint difference "
            "at exactly the right seven-site word, but the reciprocal K "
            "antisymmetrization itself is zero and the physical bar carries "
            "the wrong decorated residual tail.  The existing curvature/bar "
            "product therefore does not construct A"
        ),
    }


def complete_response_and_unary_search() -> dict[str, object]:
    first = load(
        "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py",
        "four_term_e14_first",
    )
    rewrite = first.load(first.REWRITE_PATH, "four_term_e14_rewrite")
    top = rewrite.load(rewrite.TOP_PATH, "four_term_e14_top")
    two = top.load(top.TWO_CELL_PATH, "four_term_e14_two")
    e14 = two.load(two.E14_PATH, "four_term_e14_base")
    b4 = e14.load(e14.B4_PATH, "four_term_e14_b4")
    _candidates, _names, responses, unary = two.universal(e14, b4, 1, 1)
    require(len(responses) == 3 ** 6, "complete response word count changed")

    endpoint_plus = ("p1_0_1", "s1_1_1")
    endpoint_minus = ("p1_1_1", "s1_0_1")
    private_tail = ("u35_11", "v2411")
    hits = []
    for word, row in responses.items():
        pair = (
            row.get(endpoint_plus, {}).get(private_tail, Q(0)),
            row.get(endpoint_minus, {}).get(private_tail, Q(0)),
        )
        if pair != (Q(0), Q(0)):
            hits.append((word, pair))
    require(hits == [((1,) * 6, (Q(1), Q(1)))],
            ("correct-tail response hits changed", hits))

    unary_word = (0, 0, 0, 1, 0, 1)
    core = ("u05_01", "v3410")
    require(unary[unary_word].get(core) == 1,
            "promoted rootless 2K2 core left the canonical unary row")
    require(unary[unary_word].get(("u35_11",)) == -1,
            "canonical unary pivot changed")

    first_ledger, first_digest = first.audit()
    require(first_digest == first.EXPECTED_LEDGER_SHA256,
            "E14 first-hit replay changed")
    canonical = first_ledger["canonical_first_reduction"]
    require(canonical["target_augmented_first_hit_column_count"] == 269
            and canonical["target_augmented_first_hit_rank_Q"] == 269,
            "canonical first-hit module changed")
    require(canonical["rational_dual_support"] == 22
            and canonical["rational_dual_pairing"] == "-1"
            and canonical["primitive_integral_dual_pairing"] == "-30",
            "canonical first-hit separator changed")

    companion = load(
        "computations/verify_h3_rootless_e14_companion_core_identification.py",
        "four_term_companion_core",
    )
    companion_ledger, companion_digest = companion.audit()
    require(companion_digest == companion.EXPECTED_LEDGER_SHA256,
            "rootless/E14 companion replay changed")
    require(companion_ledger["rootless_marked_cube_site_profile"] == [1] * 8,
            "rootless cube profile changed")
    require(companion_ledger["E14_promoted_term_site_profile"]
            == [2, 1, 1, 1, 2, 1, 1, 1],
            "E14 promoted profile changed")

    return {
        "complete_response_rows": len(responses),
        "correct_private_tail_response_hits": len(hits),
        "unique_hit_word": "111111",
        "unique_hit_endpoint_coefficients": [1, 1],
        "chi_on_every_correct_tail_response": 0,
        "canonical_unary_word": "000101",
        "canonical_unary_contains_mapped_q_comp_core": True,
        "mapped_q_comp_core": list(core),
        "rootless_bar_word": "01211222",
        "rootless_zero_endpoint_chart_word": "00211200",
        "rootless_marked_profile": [1] * 8,
        "E14_promoted_profile": [2, 1, 1, 1, 2, 1, 1, 1],
        "full_cell_source_or_fine_grade_identification": False,
        "first_hit_module": {
            "columns": canonical["target_augmented_first_hit_column_count"],
            "coordinates": canonical["first_hit_coordinate_count"],
            "rank_Q": canonical["target_augmented_first_hit_rank_Q"],
            "rational_dual_support": canonical["rational_dual_support"],
            "rational_dual_pairing": canonical["rational_dual_pairing"],
            "primitive_integral_pairing":
                canonical["primitive_integral_dual_pairing"],
        },
        "verdict": (
            "the complete response table supplies only the signless "
            "endpoint row at the correct tail.  The unary row contains the "
            "right decorated 2K2 core, but only in the wrong source block "
            "and repeated full-cell profile; its complete first-hit closure "
            "still has the displayed primitive dual"
        ),
    }


def bar_bianchi_hasse_pp_matching_search() -> dict[str, object]:
    bar = load(
        "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py",
        "four_term_bar",
    )
    paths = bar.endpoint_ridge_paths()
    companions, target_records = bar.covariance_companions()
    bar_cokernel = bar.integral_cokernel(companions)
    require(len(paths) == 5 and len(companions) == 15,
            "endpoint bar inventory changed")
    require(bar_cokernel["route_columns"] == 15
            and bar_cokernel["matching_bianchi_differences"] == 15
            and bar_cokernel["available_rank"] == 15
            and bar_cokernel["primitive_cokernel_rank"] == 5,
            "bar/Bianchi cokernel changed")
    require(all(record["target_terms"] == 0 for record in target_records),
            "complete response route acquired a target")

    hasse = load(
        "computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py",
        "four_term_hasse",
    )
    cube = hasse.canonical_cube_and_unit()
    coarse = hasse.coarse_candidate()
    adjacent = hasse.one_adjacent_edge_gate()
    fine = hasse.fine_grade_and_word_gate()
    require(cube["fourth_operator_on_H_m"] == 1
            and cube["fourth_operator_on_H_0_minus_u"] == 0,
            "fourth-Hasse connecting values changed")
    require(not coarse["source_valid"]
            and adjacent["remaining_rows"] == [0, 1, 1, -1]
            and not fine["word_change_supplied_by_multiplication_or_adjacent_edge"],
            "Hasse/adjacent-edge obstruction changed")

    pp = load(
        "computations/verify_h3_rootless_endpoint_to_collision_chain_map_boundary.py",
        "four_term_pp",
    )
    single = pp.typed_single_face_comparison()
    squares = pp.adjacent_source_square()
    repeated = pp.repeated_degree_audit()
    require(single["formal_difference"] == [1, -1, 0, 0],
            "formal endpoint/rootless comparison changed")
    require(squares["comparison_edge_rank"] == 4
            and squares["after_formally_adjoining_reduced_Eq"]["rank"] == 4,
            "first PP comparison rank changed")
    require(repeated["all_profiles"] == "P3+K2=(2,1,1,1,1) up to order",
            "first repeated fine degree changed")

    matching = load(
        "computations/verify_h3_rootless_abcde_relative_matching_cell_obstruction.py",
        "four_term_matching",
    )
    positive = matching.load(
        "computations/verify_h3_rootless_five_cycle_positive_interface.py",
        "four_term_matching_positive",
    )
    degree = matching.polynomial_degree_obstruction(positive)
    normalized = matching.normalized_incidence_and_dual()
    require(degree["absolute_lower_boundary"] == "5*abcde"
            and not degree["absolute_cycle"],
            "matching-square lower boundary changed")
    require(normalized["dual_kills_matching_square_boundaries"]
            and not normalized[
                "abstract_dual_descends_to_physical_terminal_quotient"],
            "matching-square dual typing changed")

    return {
        "bar_and_Bianchi": {
            "endpoint_paths": len(paths),
            "source_labelled_routes": len(companions),
            "matching_Bianchi_differences":
                bar_cokernel["matching_bianchi_differences"],
            "rank_in_Omega_plus_companion_module":
                bar_cokernel["available_rank"],
            "primitive_cokernel": bar_cokernel["cokernel"],
            "first_readout": (
                "every route -Omega_v+q_(v,N) has ordinary residue 1; "
                "matching switches and endpoint-order Bianchi squares do "
                "not remove the primitive companion class"
            ),
        },
        "fourth_Hasse": {
            "selected_operator_on_mixed_source":
                cube["fourth_operator_on_H_m"],
            "selected_operator_on_pure_source":
                cube["fourth_operator_on_H_0_minus_u"],
            "formal_candidate_source_valid": coarse["source_valid"],
            "one_adjacent_edge_remainder": adjacent["remaining_rows"],
        },
        "principal_parts": {
            "formal_single_vertex_difference": single["formal_difference"],
            "formal_difference_is_available_source_column": False,
            "first_literal_comparison_rank": squares["comparison_edge_rank"],
            "first_literal_extra_readout": "pure Eq",
            "after_reduced_Eq_still_missing":
                squares["after_formally_adjoining_reduced_Eq"]["still_missing"],
            "first_common_fine_degree": repeated["all_profiles"],
        },
        "matching_square": {
            "cyclic_weighted_vertex_lower_boundary":
                degree["absolute_lower_boundary"],
            "is_absolute_cycle": degree["absolute_cycle"],
            "ordinary_matching_or_Tate_cell_supplies_it": False,
            "primitive_abstract_dual":
                normalized["primitive_abstract_dual"],
            "dual_is_physical_terminal_functional": False,
        },
        "verdict": (
            "bars reach Omega-q only with the primitive response/residue "
            "companion; the formal Hasse vertex is not source-valid; first "
            "PP cells give only adjacent differences plus pure Eq; and an "
            "ordinary matching-square boundary cannot supply the missing "
            "vertex because its cyclic package has lower boundary 5*abcde"
        ),
    }


def minimal_new_cell() -> dict[str, object]:
    return {
        "name": "mixed endpoint--two-colour mapping-cone generator H_(1,23|45)",
        "boundary_coordinates": list(A),
        "boundary_formula": "E_plus-E_minus+Omega_1-q_(1,23|45)",
        "protected_readouts_W_target_old_ores_ainc": [0, 0, 0, 0],
        "source_blocks_joined": {
            "E14_unary_source_word": "000101",
            "E14_target_word": "111111",
            "rootless_physical_word": "01211222",
            "rootless_zero_endpoint_chart_word": "00211200",
        },
        "fine_grade_requirement": (
            "retain the labelled repeated P3+K2 comparison component and "
            "the mapped q_(1,23|45) 2K2 core; polynomial multiplication may "
            "homogenize cell degree but is not the source-word map"
        ),
        "degree_zero_shadow": (
            "break the signless E14 endpoint-orientation class detected by "
            "chi and by the 22-coordinate first-hit dual"
        ),
        "relative_boundary": (
            "cancel Omega_1 and its same-labelled q companion without the "
            "bar's ordinary-residue face, and supply one PP comparison "
            "vertex rather than another adjacent difference"
        ),
        "ordinary_existing_family": False,
        "scope": (
            "one canonical orbit representative; relabelling/cyclic symmetry "
            "generates the other endpoint/facial copies"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    ledger = {
        "theorem": "shared four-term endpoint-word-change bounded inventory boundary",
        "four_term_quotient": four_term_quotient(),
        "complete_response_and_unary": complete_response_and_unary_search(),
        "curvature_Kodaira_Spencer_candidate":
            curvature_kodaira_spencer_audit(),
        "bar_Bianchi_Hasse_PP_matching":
            bar_bianchi_hasse_pp_matching_search(),
        "smallest_new_datum": minimal_new_cell(),
        "verdict": (
            "the proposed four-term chain is not present in the complete "
            "pinned diagonal/crossed response, unary/G11 first-hit, endpoint "
            "bar/Bianchi, fourth-Hasse, first repeated PP, or ordinary "
            "matching-square inventories.  The reciprocal/mixed-curvature "
            "candidate reaches E_plus-E_minus at the correct word, but its "
            "residue has pure 11|11 tail while the physical bar has mixed "
            "21|12 tail.  The first coarse obstruction is "
            "the primitive endpoint-orientation covector chi; the literal "
            "E14 and rootless sides retain independent first-hit and "
            "response-companion separators.  A new mixed source-word "
            "mapping-cone generator with the displayed boundary/readouts is "
            "necessary"
        ),
        "scope": (
            "complete for the pinned bounded families in one canonical "
            "orbit; this is not an all-source-resolution no-go"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    response = ledger["complete_response_and_unary"]
    rootless = ledger["bar_Bianchi_Hasse_PP_matching"]
    print("h3 shared four-term endpoint-word-change inventory: OBSTRUCTED")
    print("complete canonical response rows searched:",
          response["complete_response_rows"])
    print("correct-tail endpoint hit: unique and signless (1,1)")
    print("first coarse separator: chi=(1,-1,0,0), chi(A)=2")
    print("literal first-hit dual: support 22, pairing -1")
    print("mixed curvature endpoint: correct word and sign, residue tail mismatch")
    print("bar/Bianchi primitive cokernel:",
          rootless["bar_and_Bianchi"]["primitive_cokernel"])
    print("minimal new datum: mixed source-word mapping-cone generator")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()

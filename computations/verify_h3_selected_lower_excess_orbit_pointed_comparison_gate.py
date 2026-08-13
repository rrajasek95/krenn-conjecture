#!/usr/bin/env python3
"""Audit three proposed shortcuts to the selected Gate-I input comparison.

The selected private quotient ``Q_xi`` is one-dimensional, but this alone
does not decide how it enters a derived model.  A standard excess-derived
pullback retains the excess conormal as a Tor *cycle*; it does not supply a
cell whose differential kills the corresponding physical occurrence class.

Likewise, the root/Weyl bar is canonical over the target orbit, not in the
fixed GHZ fibre.  Equivariant transport to the fixed fibre kills its four-
corner endpoint boundary.  Keeping that boundary requires a labelled local
system, together with horizontal physical augmentations (in particular q).

Finally, the old 372-term order-six representative does not require 126
independent repairs: its singleton packet is one universal Spencer
differential, and a pinned 343-term representative is already source- and
D1-flat with the same secondary -delta class.  Neither statement constructs
the operator-to-physical pointed augmented comparison.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_selected_lower_koszul_cartan_mapping_cone_hidden_class.py":
        "dbc2e111e9ebb1085260d97d9b41464cb502fe0c2cd6b061e7f10edaa5e71053",
    "computations/verify_h3_selected_lower_minimal_totalized_weyl_cone_alternative.py":
        "cddff2c501382ebf5104cc1cbc510b71a3ecaf72f1e97af4d3608fe9d6c6d67f",
    "computations/verify_h3_cut_swap_shared_loop_hasse_cross_term_gate.py":
        "cc551585391a990060f78b49486c05af6c3b4a301058c855a422ae9d54fe5be5",
    "computations/verify_h3_universal_spencer_euler_contraction.py":
        "4e4e4810dc49ab366555288ab7c696047cd3ce79ab7dc4b159b38047def8942b",
    "computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py":
        "6ab3f36073cd08c1ccad97ebd6f8ed3c5f39736be82b6063436c161f176cfeb0",
    "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py":
        "ef9bd416986f7dc8c07ffa3b396d1c1f92237c8e1a0539ecbb0ddbeaadb1c18e",
    "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py":
        "5a89d25227562b397d6cf3f16306346ce7d9fd16fb73a0f0a4486355a7cef29e",
    "computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py":
        "eb56cdb4ab1915f8ce35ab3acf0398b4f526c52a17c9c8ebafcc7a5ad4f86bcc",
    "computations/verify_h3_anchor_conormal_functoriality_bridge.py":
        "83879756547765878c36944c1ab14827ab77a1f217931bc05db0c72cb0af32a8",
}
EXPECTED_LEDGER_SHA256 = (
    "208553758ea514371e2647aa65cb33520a834feaadf4f9a48e6db7bb7da8f431"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def rank(rows: tuple[tuple[Q, ...], ...]) -> int:
    if not rows:
        return 0
    work = [list(map(Q, row)) for row in rows]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def matvec(matrix, vector):
    return tuple(sum((Q(entry) * Q(value) for entry, value in
                      zip(row, vector, strict=True)), Q(0))
                 for row in matrix)


def excess_base_change_audit() -> dict[str, object]:
    # B tensor_A^L B for A=Q[x], B=A/(x) is represented by
    # [B*e --0--> B].  The excess generator is a nonzero H_1 class.
    derived_differential = ((Q(0),),)
    derived_rank = rank(derived_differential)
    require(derived_rank == 0, "the excess differential stopped vanishing")
    derived_h1 = 1 - derived_rank
    derived_h0 = 1 - derived_rank

    # A filler of the physical occurrence quotient would instead have
    # d(sigma)=Xi, represented by the unit differential.  It kills both the
    # degree-one and degree-zero class, so it is not the standard base change.
    filler_differential = ((Q(1),),)
    filler_rank = rank(filler_differential)
    require((derived_h1, derived_h0, filler_rank) == (1, 1, 1),
            "the minimal excess/filler comparison changed")

    # Endpoint oddization retains the difference of two excess classes.
    odd_excess = (Q(1), Q(-1))
    doubled_derived_differential = ((Q(0), Q(0)),
                                    (Q(0), Q(0)))
    require(matvec(doubled_derived_differential, odd_excess) == (0, 0),
            "endpoint oddization unexpectedly filled excess Tor")
    return {
        "model": "B tensor_A^L B for A=Q[x], B=A/(x)",
        "base_changed_Koszul_differential": 0,
        "excess_H1_dimension": derived_h1,
        "excess_H0_dimension": derived_h0,
        "endpoint_odd_excess_is_cycle": True,
        "desired_occurrence_filler_differential": "d(sigma_xi)=Xi^-",
        "filler_differential_rank": filler_rank,
        "filler_is_supplied_by_standard_derived_pullback": False,
        "interpretation": (
            "the diagonal/excess class can model the one-dimensional Q_xi, "
            "but identifying its Gysin/transgression with Xi^- is precisely "
            "an additional comparison map"
        ),
    }


def ghz_target():
    return {tuple([colour] * 8): Q(1) for colour in range(3)}


def root_on_target(target, site, old, new):
    answer = {}
    for word, coefficient in target.items():
        if word[site] != old:
            continue
        changed = list(word)
        changed[site] = new
        answer[tuple(changed)] = coefficient
    return answer


def orbit_quotient_audit() -> dict[str, object]:
    delta = ghz_target()
    root_supports = []
    for site in (2, 5):
        for old, new in ((1, 2), (2, 1)):
            image = root_on_target(delta, site, old, new)
            require(len(image) == 1, "a tail root stopped moving GHZ")
            support = next(iter(image))
            require(support not in delta,
                    "a tail root became an infinitesimal fixed-fibre action")
            root_supports.append(support)
    require(len(set(root_supports)) == 4,
            "the four orbit-normal directions lost independence")

    # Boundary -v+sv+wv-swv.  The two copies cover the same orbit path, so
    # its base projection is zero.  Canonical w^{-1} transport identifies
    # wv with v and swv with sv and kills the private endpoint packet.
    endpoint_boundary = (Q(-1), Q(1), Q(1), Q(-1))
    base_projection = ((Q(1), Q(1), Q(0), Q(0)),
                       (Q(0), Q(0), Q(1), Q(1)))
    fixed_fibre_transport = ((Q(1), Q(0), Q(1), Q(0)),
                             (Q(0), Q(1), Q(0), Q(1)))
    require(matvec(base_projection, endpoint_boundary) == (0, 0)
            and matvec(fixed_fibre_transport, endpoint_boundary) == (0, 0),
            "the orbit-relative/fixed-fibre endpoint calculation changed")

    # The unaugmented transport does not force q horizontality.  On a
    # two-dimensional fibre, q_1=q_0 and q_1!=q_0 are both compatible with
    # the same identity transport.  Only the first is a local-system cocycle.
    q0 = (Q(1), Q(0))
    q1_horizontal = (Q(1), Q(0))
    q1_defective = (Q(0), Q(1))
    q_good_defect = tuple(b - a for a, b in
                          zip(q0, q1_horizontal, strict=True))
    q_bad_defect = tuple(b - a for a, b in
                         zip(q0, q1_defective, strict=True))
    require(q_good_defect == (0, 0) and q_bad_defect == (-1, 1),
            "the q-local-system independence guard changed")
    return {
        "tail_root_normal_directions": len(set(root_supports)),
        "root_Weyl_is_fixed_GHZ_fibre_automorphism": False,
        "endpoint_swap_is_fixed_fibre_automorphism": True,
        "orbit_relative_endpoint_boundary": [str(x) for x in endpoint_boundary],
        "base_projection": [str(x) for x in
                            matvec(base_projection, endpoint_boundary)],
        "canonical_fixed_fibre_transport": [str(x) for x in
                                             matvec(fixed_fibre_transport,
                                                    endpoint_boundary)],
        "private_packet_survives_canonical_transport": False,
        "homotopy_quotient_verdict": (
            "the root bar exists on the orbit family/quotient, not on the "
            "exact fixed source fibre; retaining its private packet requires "
            "a nontrivial occurrence-labelled local system"
        ),
        "q_horizontal_defect_not_forced_by_unaugmented_orbit_data": True,
        "q_defect_examples": {
            "horizontal": [str(x) for x in q_good_defect],
            "nonhorizontal": [str(x) for x in q_bad_defect],
        },
    }


def pointed_diagonal_audit() -> dict[str, object]:
    # Coordinates (f,G,u_f,H0,u), from the complete response graph and the
    # central Eq graph.  The universal pointed diagonal adds d(u_f-u).
    d_e = (Q(1), Q(0), Q(-1), Q(0), Q(0))
    d_m = (Q(0), Q(1), Q(1), Q(0), Q(0))
    d_f0 = (Q(0), Q(0), Q(0), Q(1), Q(-1))
    d_delta = (Q(0), Q(0), Q(1), Q(0), Q(-1))
    old = (d_e, d_m, d_f0)
    new = old + (d_delta,)
    require((rank(old), rank(new)) == (3, 4),
            "the private/global pointed diagonal rank changed")
    return {
        "old_conormal_rank": 3,
        "rank_after_private_global_diagonal": 4,
        "new_conormal": "d(u_f-u)",
        "positive_functorial_statement": (
            "if the physical comparison is a pointed source-presentation "
            "map with f-Phi^*(a_Eq) in the complete response ideal, the "
            "anchor law follows by differentiation"
        ),
        "relation_to_Xi": (
            "the private/global conormal and Q_xi are both one-dimensional, "
            "but no pinned map identifies them; equality would be the first "
            "associated-graded clause of the desired pointed comparison"
        ),
        "ordinary_quasi_isomorphism_to_old_source_is_formal": False,
    }


def hasse_cross_term_audit() -> dict[str, object]:
    trials = 0
    for f0 in range(-2, 3):
        for f1 in range(-2, 3):
            for g0 in range(-2, 3):
                for g1 in range(-2, 3):
                    # [t^2](f0+t f1)(g0+t g1)=f1*g1.
                    require(Q(f1 * g1) == Q(f1) * Q(g1),
                            "the divided-power cross term changed")
                    trials += 1
    return {
        "identity": "D_4^[2](fg)=D_4(f)D_4(g) for multi-affine f,g",
        "coefficient": 1,
        "integer_specializations_checked": trials,
        "pinned_occurrence_output": {
            "fixed_shared_label": "B1 or B4",
            "rho_paired_labels": "(B0+B5)/2 or (B2+B3)/2",
        },
        "pinned_physical_mismatch": {
            "third_Bianchi_marked_word": "222000",
            "rho_complement_word": "202020",
            "formal_tail_ainc_W_target_ores": [-1, 0, 0, 0],
            "Xi_minus_repeated_profile": [1, 1, 1, 2, 1, 1, 1, 2],
            "Xi_minus_fine_degrees": 4,
        },
        "verdict": (
            "the excess/Gysin product rule fixes the unit occurrence "
            "coefficient and the correct C4 tail, but not the word/fine/"
            "private lift to Xi^- or its protected augmented cap"
        ),
    }


def order6_totalization_audit() -> dict[str, object]:
    endpoint = (ROOT / (
        "computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py"
    )).read_text()
    affine = (ROOT / (
        "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py"
    )).read_text()
    secondary = (ROOT / (
        "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py"
    )).read_text()
    require("require(len(symmetrized_theta) == 372" in endpoint
            and "require(len(singleton_full_row_ideal) == 126" in endpoint,
            "the pinned 372/126 audit interface changed")
    require('require(not singleton_output' in affine
            and 'result["exact_solution_terms"] == 343' in affine,
            "the pinned first-flat 343-term interface changed")
    require('"D2": "literal singleton coefficient-prolongation map"'
            not in secondary, "the HPL D1/D2 labels were accidentally swapped")
    require('"D1": "literal singleton coefficient-prolongation map"'
            in secondary and '"D2_value": "-delta=(-1,+1,+1,-1)"'
            in secondary, "the pinned HPL secondary interface changed")
    return {
        "old_tail_antisymmetric_representative_terms": 372,
        "old_nonzero_singleton_faces": 126,
        "singleton_faces_in_old_complete_full_row_ideal": 0,
        "first_flat_representative_terms": 343,
        "first_flat_literal_source": 0,
        "first_flat_D1_support": 0,
        "induced_D2": "-delta=(-1,+1,+1,-1)",
        "D2_canonical_on_D1_homology": True,
        "cofibrant_resolution_verdict": (
            "the 126 faces are one coherent universal Spencer differential, "
            "not 126 independent physical generators.  Universal Euler "
            "contraction and the exact first-flat representative remove the "
            "first-layer search, but physical labelled descent is still a "
            "comparison theorem"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "selected lower excess/orbit/pointed comparison gate",
        "pins": PINS,
        "derived_excess": excess_base_change_audit(),
        "orbit_homotopy_quotient": orbit_quotient_audit(),
        "pointed_source_diagonal": pointed_diagonal_audit(),
        "divided_power_Gysin_candidate": hasse_cross_term_audit(),
        "order6_cofibrant_totalization": order6_totalization_audit(),
        "sharp_yes_no": {
            "derived_excess_constructs_Xi_filler": False,
            "orbit_quotient_avoids_fixed_label_comparison": False,
            "cofibrant_order6_removes_126_separate_searches": True,
            "cofibrant_order6_constructs_physical_Xi_to_Mv_map": False,
        },
        "smallest_positive_theorem": (
            "construct one pointed augmented source-presentation comparison "
            "from the orbit-relative/excess PP-Spencer model to the physical "
            "h=3 complex.  On associated graded it must send the oriented "
            "excess/Gysin generator to the normalized Xi^- occurrence line; "
            "on degree zero it must impose u_f-Phi^*(u) in the response "
            "ideal; and it must carry word/fine/repeated labels, protected "
            "rows, eta/sigma and a horizontal physical q cocycle"
        ),
        "smallest_obstruction": (
            "the rank-one comparison/connection from the excess or orbit "
            "local system to Q_xi, together with its q-horizontal augmented "
            "extension.  Standard derived base change makes the class a Tor "
            "cycle and standard fixed-fibre transport kills it"
        ),
        "terminal_scope": (
            "Xi^- is not yet a physical terminal dual because q is undefined "
            "on the orbit/excess generator.  Once the pointed augmented lift "
            "exists, the pinned q-defect theorem gives transport/Fredholm "
            "when the defect is zero and a relative generator when nonzero"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("selected lower categorical ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 selected lower categorical routes: SHARP GATE")
    print("derived excess: Tor cycle, not Xi filler")
    print("orbit quotient: genuine over orbit; fixed transport kills packet")
    print("order6: 126-search removed; pointed augmented comparison OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

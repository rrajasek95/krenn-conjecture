#!/usr/bin/env python3
"""Locate the first unfilled face of the sole cross-word cap/Eq attachment."""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_selected_fibre_graph_keq_koszul_gate.py":
        "9d57cbcfaeebb8d7f67d6efea87a124b4a46ad1dc054d5fc0954ab0c2338b157",
    "notes/h3-e14-selected-fibre-graph-keq-koszul-gate.md":
        "98cae28b58267abcffc47b571e52581a354950ef684df5f28b58dca88c60c6e7",
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "notes/h3-centered-projector-literal-first-hasse-eq-incidence-gate.md":
        "242a0a148c782c73540f060ef4e685902888f6d0e95da2d050b0e46dec5baf9d",
    "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py":
        "2e4b1a1b9bb5b5be8d0997132b49b95576a28dc6ccb9cfd83db808ace8f52f3e",
    "notes/h3-e14-pointed-orbit-keq-mapping-cylinder-gate.md":
        "f5008f5b7e892b5ce5270faacee4ec9f2bffc2630b8dd15a55cb8f5c6800cb21",
    "computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py":
        "42bf68eeb963d568d1c8d9156d4176bec31a114b6fe804744833364fe3633475",
    "notes/h3-e14-cap-graph-two-parameter-flat-transport-gate.md":
        "61c093eed30cd2fff1be086e6069d344e76a583ee31f93528a31aebe76c5c5d6",
    "computations/verify_h3_cylinder_theta_groupoid_frontier_correction.py":
        "3cdd19a68f0acafb975cb3d8d1660aaabde485af5aacb4672cb1fe2e5febe2cb",
    "notes/h3-cylinder-theta-groupoid-frontier-correction.md":
        "631caffa650b43eec817a8daa6588ee65618971c9f353fbda5c3623fd9b44a66",
}
EXPECTED_LEDGER_SHA256 = "a0bb53ea0c5c3f683c2e815c2d8e83a2afa63857d0e945b1fc80b32d13bf50d8"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def rank(vectors: tuple[tuple[Q, ...], ...]) -> int:
    basis: dict[int, tuple[Q, ...]] = {}
    for vector in vectors:
        values = list(vector)
        for pivot in sorted(basis):
            if values[pivot]:
                coefficient = values[pivot]
                values = [a-coefficient*b for a, b in
                          zip(values, basis[pivot], strict=True)]
        pivot = next((i for i, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        coefficient = values[pivot]
        basis[pivot] = tuple(value/coefficient for value in values)
    return len(basis)


def dot(left, right) -> Q:
    return sum((Q(a)*Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))


def selected_fibre_audit() -> dict[str, object]:
    # Coordinates (b01, other 29 fibres, z01).
    response = (Q(1), Q(1), Q(0))
    graph = (Q(-1), Q(0), Q(1))
    selected = (Q(1), Q(0), Q(0))
    dual = (Q(1), Q(-1), Q(1))
    require(rank((response, graph)) == 2
            and rank((response, graph, selected)) == 3,
            "the selected fibre rank gate changed")
    require(dot(dual, response) == dot(dual, graph) == 0
            and dot(dual, selected) == 1,
            "the selected fibre dual changed")

    # Coefficient count: 90 occurrences, 30 ordered endpoint fibres, three
    # residual matchings per fibre.
    c_f = [Q(-1)]*90
    c_f[0] = Q(89)
    c01 = [Q(-1)]*30
    c01[0] = Q(29)
    matching_image = []
    for fibre in range(30):
        matching_image.append(sum(c_f[3*fibre:3*fibre+3], Q(0)))
    require(tuple(matching_image) == tuple(Q(3)*value for value in c01),
            "M(c_f)=3c01 changed")
    return {
        "coefficient_identity": "(A+I)c_f=3c_01",
        "selected_fibre": "c_01=30b_01-R",
        "graph_rows_rank": 2,
        "rank_after_b01": 3,
        "primitive_dual": [1, -1, 1],
        "first_literal_PP_face": (
            "db_01=p0*s1*sum_(three K4 matchings) d(q_edge)*q_mate"
        ),
        "db01_in_old_complete_response_PP_span": False,
        "meaning": (
            "the centered c_f attachment must itself supply this selected "
            "six-term face; a graph coordinate does not"
        ),
    }


def formal_factorization_audit() -> dict[str, object]:
    return {
        "conditional_input": (
            "a multiplicative, matching/D4-natural physical epsilon_cf with "
            "d epsilon_cf=c_f"
        ),
        "matching_step": "epsilon_c01=(A+I)epsilon_cf/3",
        "selected_section": "epsilon_01=(epsilon_R+epsilon_c01)/30, d= b_01",
        "central_cell": (
            "kappa_01=epsilon_01 wedge theta, with "
            "d kappa_01=b_01*theta-epsilon_01*(H0-u)e_Eq"
        ),
        "D4_step": "the marked pure-00 occurrence reaches R_E14 on v04=0",
        "cap_step": (
            "T+rho is a closed target/residue normalizer and is flat in the "
            "formal occurrence x D4 tensor presentation"
        ),
        "theta_step": "conjugate endpoint half automatic; not reopened",
        "conclusion": (
            "there is no second abstract selected-fibre or central-Koszul "
            "generator after one multiplicative c_f attachment"
        ),
    }


def mixed_square_audit() -> dict[str, object]:
    # Four alternatingly oriented edges of the pointed/D4/K_Eq square.
    edges = (
        (Q(-1), Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(-1), Q(0)),
        (Q(0), Q(0), Q(-1), Q(1)),
        (Q(-1), Q(0), Q(0), Q(1)),
    )
    cycle = (Q(1), Q(-1), Q(1), Q(-1))
    boundary = tuple(sum((cycle[j]*edges[j][i] for j in range(4)), Q(0))
                     for i in range(4))
    require(rank(edges) == 3 and boundary == (0, 0, 0, 0),
            "the primitive mixed square changed")

    # Shadow coordinates (P_f, cap, R_E14, central E, ridge).
    projector = (Q(1), 0, 0, 0, 0)
    cap = (0, Q(1), 0, 0, 0)
    d4 = (0, 0, Q(1), 0, 0)
    required = (0, 0, Q(1), Q(1), 0)
    central_dual = (0, 0, 0, Q(1), 0)
    require(rank((projector, cap, d4)) == 3
            and rank((projector, cap, d4, required)) == 4,
            "the central incidence rank changed")
    require(all(dot(central_dual, value) == 0
                for value in (projector, cap, d4))
            and dot(central_dual, required) == 1,
            "the central incidence dual changed")
    return {
        "edge_skeleton_rank": 3,
        "H1": "Z generated by (1,-1,1,-1)",
        "mixed_two_cell_in_current_literal_inventory": False,
        "central_shadow_dual": [0, 0, 0, 1, 0],
        "dual_kills": ["P_f", "primitive cap", "D4 top", "cap graph"],
        "dual_reads": "Phi_orb((H0-u)e_Eq)=R_E14",
        "why_formal_wedge_is_not_yet_physical": (
            "epsilon_cf/epsilon_01 has not been placed across the response, cap "
            "and E14 word/fine/repeated summands"
        ),
    }


def first_proper_face_audit() -> dict[str, object]:
    face_to_labels = ((Q(0), Q(1)), (Q(1), Q(0)))
    cap_residue = ((Q(-1), Q(0)), (Q(0), Q(-1)))
    composite = tuple(tuple(sum((face_to_labels[i][k]*cap_residue[k][j]
                                 for k in range(2)), Q(0))
                            for j in range(2)) for i in range(2))
    require(composite == ((0, -1), (-1, 0)),
            "the rooted face label matrix changed")
    return {
        "after_granting_mixed_square_coefficient": (
            "the first codimension-one physical face is the marked D3/root-lower "
            "map face3->B4, face5->B1"
        ),
        "required_even_image": "-(B1+B4)=-2*d_even",
        "label_times_cap_residue_matrix": [list(map(int, row))
                                            for row in composite],
        "determinant": -1,
        "coefficient_kernel": 0,
        "current_source_provenance": False,
        "interpretation": (
            "once the literal two face maps exist, rooted d_even is forced; "
            "the issue is the same mixed attachment's physical proper face, not "
            "another scalar theorem"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 cross-word cap/central attachment first-face gate",
        "pins": PINS,
        "selected_fibre": selected_fibre_audit(),
        "formal_factorization": formal_factorization_audit(),
        "mixed_square": mixed_square_audit(),
        "first_physical_proper_face": first_proper_face_audit(),
        "verdict": (
            "The path c_f -> c01 -> selected b01 Koszul square -> D4/R_E14, "
            "with T+rho normalization, is an exact formal factorization once one "
            "multiplicative c_f attachment is granted.  Current literal PP/Hasse "
            "rows do not supply that attachment: the first selected face db01 has "
            "a primitive fibre dual, and after optimistically granting it the "
            "pointed/D4/K_Eq edge skeleton still has the primitive mixed incidence "
            "Phi_orb(E)=R_E14.  A physical mixed two-cell would fill it; its first "
            "uncancelled codimension-one face is the D3 label map face3->B4, "
            "face5->B1, forcing -2d_even.  These are nested faces of the one "
            "cross-word cap/central attachment, not additional theorem branches."
        ),
        "scope": (
            "canonical h=3 grade g; theta return is pinned as automatic and is not "
            "part of this frontier"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("c_f -> 3c01 -> selected Koszul square: FORMALLY EXACT")
    print("first literal selected PP face db01: NOT IN OLD SPAN")
    print("first cross-summand dual: CENTRAL E->R_E14 INCIDENCE")
    print("first physical proper face after mixed cell: D3 -> B4/B1")
    print("ledger_sha256="+digest)


if __name__ == "__main__":
    main()

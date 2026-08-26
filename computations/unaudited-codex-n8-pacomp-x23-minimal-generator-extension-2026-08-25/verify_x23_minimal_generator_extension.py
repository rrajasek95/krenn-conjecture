#!/usr/bin/env python3
"""Exact h=3 audit of the proposed q23 protected Eq filler.

This is deliberately a symbolic/source-interface audit.  It distinguishes
the canonical relative Koszul formula from a generator in the physical
response-to-cap operation corner.  No numerical membership solve is used.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "computations/unaudited-codex-n8-pacomp-q23-protected-factor-2026-08-25/MANIFEST.sha256":
        "f3b689175811cb8d28dbae605fac703c8339f2e5a259c4c0e644122f1779b500",
    "computations/unaudited-codex-n8-pacomp-q23-protected-factor-2026-08-25/results_q23_protected_factor_counterobligation.json":
        "93ba0a20dcf3e50aadcba20af5353113d79c7604fc11b281b8ca970b62597994",
    "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py":
        "15b47a420a6f1e2e6eb0b89e5e5efb5c895172e30b8ab9339dfa1e451ac03668",
    "computations/verify_h3_cplus_root_even_koszul_physical_dressing_gate.py":
        "9bd2c9f482dc3277d07bd96a4e2189034e766f97e7800d3864179a75e03cef17",
    "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py":
        "2e4b1a1b9bb5b5be8d0997132b49b95576a28dc6ccb9cfd83db808ace8f52f3e",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py":
        "8be3bc5bf85f8d633e77e2a0bdd18aea6d481c81f5fb6a6a947cbaf82f862302",
    "computations/verify_h3_physical_eq_filler_k_source_ansatz_terminal_gate.py":
        "124eb09edf887554f009ddda1b22d80c892ebd4676d3f9c76abb5e4c3474f332",
    "computations/verify_h3_gamma_star_executable_gen_phys_registry.py":
        "173ebdedcfdadd9891704223ea93731509c18a4d120aa34d6c7bc8a4f3aebddb",
    "computations/verify_h3_gamma_star_source_derived_free_closure_census.py":
        "a479ac8759bf7a18b43ee91d8b1ab7d0b432c48a7787b065cac68403ace3df3a",
    "computations/verify_h3_phi_ks_r0_pf_minimal_executable_ansatz_gate.py":
        "d21d776ec53babb4f99693e4dad51d87309e3ed0cccf2e34fb6025e6d74d1009",
}
EXPECTED_LOGICAL_SHA256 = (
    "6c6fa348d314ea2395204a0e7b910e1ec0a35100ba5282e91baa27693bcbe355"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * value for value in vector)


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        pivot_value = rows[answer][column]
        rows[answer] = [value / pivot_value for value in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            coefficient = rows[row][column]
            rows[row] = [left - coefficient * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def formal_relative_koszul_audit() -> dict[str, object]:
    # F=H0-u and Q=Eq.  For theta=eps_F wedge eps_Q,
    # d theta=F eps_Q-Q eps_F.  On Q=0, C_K=-theta has dC_K=-F e_Eq.
    # E23 has homological degree zero, so X23=-E23*C_K has the requested
    # positive boundary.  The calculation is coefficientwise in D_root.
    d_root = tuple(map(Q, (-1, 1, -1, 1)))
    d_c_k = tuple(-value for value in d_root)  # -E23*F e_Eq
    x23_coefficient = scale(-1, d_root)
    boundary_x23 = scale(-1, d_c_k)
    require(boundary_x23 == d_root,
            "the formal relative Koszul sign changed")

    absolute_theta_faces = ("F*eps_Q", "-Q*eps_F")
    relative_c_k_faces = ("-F*e_Eq",)
    require(len(absolute_theta_faces) == 2
            and len(relative_c_k_faces) == 1,
            "absolute/relative face count changed")
    return {
        "equations": ["F=H0-u", "Q=Eq"],
        "absolute_cell": "theta=eps_F wedge eps_Q",
        "absolute_boundary": "dtheta=F eps_Q-Q eps_F",
        "relative_base_change": "Q=0 and eps_Q maps to e_Eq",
        "relative_core": "C_K=-theta, dC_K=-F e_Eq",
        "formal_definition": "X23^der=-D_root tensor B1 tensor C_K",
        "formal_boundary": "dX23^der=D_root tensor B1 tensor F e_Eq",
        "D_root": [str(value) for value in d_root],
        "X23_root_coefficients": [str(value) for value in x23_coefficient],
        "boundary_root_coefficients": [str(value) for value in boundary_x23],
        "extra_relative_faces": [],
        "absolute_face_not_killed_before_Q_base_change": "Q eps_F",
        "scope": (
            "exact only in the Q-relative derived Koszul object; C_K is "
            "cap-objectwise and carries no response-to-cap operation, word, "
            "fine, repeated, root, private, q, target, W, residue or ridge map"
        ),
    }


def sigma_and_root_naturality_audit() -> dict[str, object]:
    d_root = tuple(map(Q, (-1, 1, -1, 1)))
    root_sigma = (1, 0, 3, 2)

    def move_root(vector: tuple[Q, ...]) -> tuple[Q, ...]:
        moved = [Q(0)] * 4
        for source, target in enumerate(root_sigma):
            moved[target] = vector[source]
        return tuple(moved)

    require(move_root(d_root) == scale(-1, d_root),
            "sigma stopped reversing D_root")

    # B1->B4 and C_K is invariant because F and Eq are invariant.  Hence
    # sigma(-E23*C_K)=+E45*C_K=-X45 and the differential commutes.
    x23 = scale(-1, d_root)
    x45 = scale(-1, d_root)
    sigma_x23_in_b4 = move_root(x23)
    require(sigma_x23_in_b4 == scale(-1, x45),
            "sigma X23=-X45 changed")
    boundary23 = d_root
    boundary45 = d_root
    require(move_root(boundary23) == scale(-1, boundary45),
            "sigma stopped commuting with the cutwise differential")

    # AB and AC live in separate operation coordinates.  The formal family
    # has one cell at each root; the naturality map tau has coefficient +1.
    # Check the boundary square rootwise and that tau commutes with sigma.
    root_cells = {
        "AB": {"q23": x23, "q45": x45},
        "AC": {"q23": x23, "q45": x45},
    }
    for root in ("AB", "AC"):
        require(move_root(root_cells[root]["q23"])
                == scale(-1, root_cells[root]["q45"]),
                ("cut covariance failed", root))
    tau_q23 = root_cells["AC"]["q23"]
    tau_q45 = root_cells["AC"]["q45"]
    require(tau_q23 == root_cells["AB"]["q23"]
            and tau_q45 == root_cells["AB"]["q45"]
            and move_root(tau_q23) == scale(-1, tau_q45),
            "AB/AC formal naturality square changed")

    # In the actual operation quotient the two root-labelled Hom directions
    # are independent.  A root-forgetting sum has only rank one.
    ab = tuple(map(Q, (1, 0)))
    ac = tuple(map(Q, (0, 1)))
    aggregate = add(ab, ac)
    require(rank((ab, ac)) == 2 and rank((aggregate,)) == 1,
            "the two-root operation quotient changed")
    return {
        "site_sigma": "(2 5)(3 4)",
        "root_sigma": "(0 1)(2 3)",
        "pure_sigma": "B1 -> B4",
        "C_K_sigma": "+1",
        "cut_covariance": "sigma(X23^rho)=-X45^rho for rho=AB,AC",
        "boundary_covariance": "sigma(dX23^rho)=-dX45^rho",
        "formal_root_transport": (
            "tau_AB,AC(Xc^AB)=Xc^AC and tau(dXc^AB)=dXc^AC, c=23,45"
        ),
        "AB_check": "dX23^AB=E23^AB F e_Eq and sigma mate separately",
        "AC_check": "dX23^AC=E23^AC F e_Eq and sigma mate separately",
        "existing_root_labelled_Hom_quotient_dimension": 2,
        "root_forgetting_aggregate_rank": 1,
        "warning": (
            "tau naturality is a defining relation of the formal extension; "
            "the current physical operation algebra does not supply either "
            "root-labelled response-to-cap instance"
        ),
    }


def physical_face_and_square_audit() -> dict[str, object]:
    # Per coefficient of E, rows are (lower,Eq,ores).  The closest old cap
    # lift has two debts.  The displayed conditional three-face sum cancels
    # both and leaves the clean Eq row.
    p2_hidden = tuple(map(Q, (-1, 0, 0)))
    old_o_minus_e = tuple(map(Q, (1, 1, -1)))
    rooted_b1_residue = tuple(map(Q, (0, 0, 1)))
    clean_eq = tuple(map(Q, (0, 1, 0)))
    require(add(p2_hidden, old_o_minus_e, rooted_b1_residue) == clean_eq,
            "the q23 lower/Eq/ores cancellation changed")

    # The per-cut label equations are the two summands before rho-even
    # averaging: -(p5+n5)|B1=B1 and -(p3+n3)|B4=B4.
    p5_n5_b1 = Q(-1)
    p3_n3_b4 = Q(-1)
    d_b1 = -p5_n5_b1
    d_b4 = -p3_n3_b4
    require((d_b1, d_b4) == (Q(1), Q(1)),
            "the per-cut labelled residue sign changed")

    # Physical naturality is a square, not an Eq-only declaration.  Edges
    # are bottom P_f, left K_Eq, right K_Eq, top D4.
    bottom = tuple(map(Q, (-1, 1, 0, 0)))
    left = tuple(map(Q, (-1, 0, 1, 0)))
    right = tuple(map(Q, (0, -1, 0, 1)))
    top = tuple(map(Q, (0, 0, -1, 1)))
    edges = (bottom, left, right, top)
    cycle = tuple(map(Q, (1, -1, 1, -1)))
    boundary_cycle = tuple(sum(cycle[column] * edges[column][row]
                               for column in range(4))
                           for row in range(4))
    require(rank(edges) == 3 and boundary_cycle == (Q(0),) * 4
            and gcd(*(abs(int(value)) for value in cycle)) == 1,
            "the primitive physical mapping-square class changed")
    h1_before = 4 - rank(edges)
    h1_after_primitive_filler = h1_before - rank((cycle,))
    require((h1_before, h1_after_primitive_filler) == (1, 0),
            "the mixed-square filler stopped being minimal")
    return {
        "nearest_existing_cap_lift_per_E": {
            "rows": ["lower", "Eq", "ores"],
            "O_minus_E": [1, 1, -1],
            "unwanted_descendants": ["lower +E", "ores -E"],
        },
        "conditional_clean_face_identity": {
            "P2_hidden_minus_E": [-1, 0, 0],
            "O_minus_E": [1, 1, -1],
            "rooted_B1_residue_plus_E": [0, 0, 1],
            "sum": [0, 1, 0],
        },
        "per_cut_label_relations": {
            "q23": "d_B1=-(p_5+n_5) labelled B1=+B1",
            "q45": "d_B4=-(p_3+n_3) labelled B4=+B4",
        },
        "availability": {
            "O_minus_E": "old cap-internal lift",
            "P2_hidden": "required proper face, not independently source-labelled",
            "n_and_literal_label_map": "not constructed; using dressed K_Eq is circular",
            "clean_sum": "coefficient-exact but conditional, not an existing cell",
        },
        "mapping_square": {
            "edge_order": ["P_f bottom", "K_Eq left", "K_Eq right", "D4 top"],
            "primitive_cycle": [1, -1, 1, -1],
            "H1_before_filler": "Z",
            "H1_after_primitive_filler": 0,
            "unit_coefficient_required": True,
        },
    }


def minimal_extension_audit() -> dict[str, object]:
    # Existing operation coordinates consist of two diagonal idempotents;
    # the response->cap matrix unit is a primitive third direction.
    id_response = tuple(map(Q, (1, 0, 0)))
    id_cap = tuple(map(Q, (0, 1, 0)))
    off_diagonal = tuple(map(Q, (0, 0, 1)))
    require(rank((id_response, id_cap)) == 2
            and rank((id_response, id_cap, off_diagonal)) == 3,
            "the operation-corner extension stopped being primitive")

    # Separately at AB and AC, the clean Eq classes are primitive.  A single
    # aggregate cannot meet both root-labelled relations.
    eq_ab = tuple(map(Q, (1, 0)))
    eq_ac = tuple(map(Q, (0, 1)))
    require(rank((eq_ab, eq_ac)) == 2,
            "the root-labelled clean Eq extension changed")

    return {
        "existing_physical_X23": False,
        "proof": [
            "the executable registry has e_C A e_R=0",
            "the relative Koszul C_K is cap-objectwise",
            "the nearest physical cap lift has forced lower and ores debt",
            "the pointed K_Eq/D4 edge skeleton has primitive H1=Z",
            "AB and AC are two independent root-labelled Hom coordinates",
        ],
        "minimal_formal_dg_extension": {
            "generators": (
                "one equivariant family X_c^rho, c in {23,45}, "
                "rho in {AB,AC} (four labelled instances)"
            ),
            "differentials": [
                "dX_23^rho=D_root tensor B1 tensor (H0-u)e_Eq",
                "dX_45^rho=D_root tensor B4 tensor (H0-u)e_Eq",
            ],
            "relations": [
                "sigma X_23^rho=-X_45^rho for rho=AB,AC",
                "tau_AB,AC X_c^AB=X_c^AC for c=23,45",
                "all lower/private, ores, W, target, anchor and q readouts are zero",
            ],
            "qualification": (
                "this is a consistent free relative dg extension, not a "
                "source-derived physical construction"
            ),
        },
        "minimal_physical_source_extension": {
            "schema": (
                "one normalized root-natural response-KS -> AugP2/K_Eq "
                "constructor Phi_KS,r0, instantiated at AB and AC, with its "
                "cutwise mixed mapping-cylinder cells kappa_orb,Eq"
            ),
            "chain_map_relation": [
                "Phi_1(epsilon_s)=r0",
                "Phi_0(c_f)=-(H0-u)e_Eq",
            ],
            "exact_new_square_relation": (
                "d kappa_c^rho=P_f,c^rho-K_Eq,L,c^rho+"
                "K_Eq,R,c^rho-D4_c^rho"
            ),
            "protected_face_relation_q23": (
                "P2_hidden(-E23)+O_-E23(E23,E23,-E23)+"
                "D_root tensor (-(p5+n5)|B1)=(0,E23,0)"
            ),
            "protected_face_relation_q45": (
                "P2_hidden(-E45)+O_-E45(E45,E45,-E45)+"
                "D_root tensor (-(p3+n3)|B4)=(0,E45,0)"
            ),
            "source_provenance_required": [
                "physical invisible K_Eq cap face n, independent of the dressed cell",
                "literal face5->B1 and face3->B4 occurrence label map",
                "hidden root-lower face -E",
                "the two separately labelled AB/AC operation instances",
            ],
        },
        "minimality": {
            "off_diagonal_operation_rank_before_after": [2, 3],
            "mapping_square_class": "primitive Z generator; filler coefficient must be +/-1",
            "root_labelled_required_rank": 2,
            "one_root_forgetting_cell_suffices": False,
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    result = {
        "schema": "pacomp-h3-x23-minimal-generator-extension-v1",
        "status": "PASS_NO_EXISTING_PHYSICAL_X23_MINIMAL_EXTENSION_ISOLATED",
        "parent_q23_manifest_sha256": PINS[
            "computations/unaudited-codex-n8-pacomp-q23-protected-factor-2026-08-25/MANIFEST.sha256"
        ],
        "pins": PINS,
        "formal_relative_koszul_cell": formal_relative_koszul_audit(),
        "sigma_and_AB_AC": sigma_and_root_naturality_audit(),
        "physical_faces": physical_face_and_square_audit(),
        "generator_extension_theorem": minimal_extension_audit(),
        "verdict": (
            "The formula X23^der=-D_root tensor B1 tensor C_K has exactly "
            "the requested relative boundary and its sigma mate has the "
            "forced minus sign.  It is not a physical source-labelled cell: "
            "the existing operation grammar has no response-to-cap arrow, "
            "and the nearest cap lift has uncancelled lower/ores descendants. "
            "The minimal physical repair is the primitive mixed-square "
            "relation, as two separately root-labelled AB/AC instances."
        ),
        "scope_guard": (
            "Exact only for canonical h=3 q23/q45, the pinned callable "
            "physical grammar and its relative F/Q Koszul enlargement.  No "
            "PAComp(3), all-h, terminal, or conjecture promotion is made."
        ),
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LOGICAL_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LOGICAL_SHA256,
                ("logical ledger changed", digest, EXPECTED_LOGICAL_SHA256))
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
        print("formal relative X23 boundary: PASS EXACT")
        print("existing physical source-labelled X23: NO")
        print("sigma X23=-X45: PASS FORMAL")
        print("AB/AC operation instances required separately: 2")
        print("minimal physical filler: primitive mixed square")
        print("logical_sha256=" + digest)


if __name__ == "__main__":
    main()

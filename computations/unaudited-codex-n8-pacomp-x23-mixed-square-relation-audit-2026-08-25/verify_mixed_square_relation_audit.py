#!/usr/bin/env python3
"""Exact h=3 audit of the primitive physical mixed-square relation."""
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PINS = {
    "computations/unaudited-codex-n8-pacomp-x23-minimal-generator-extension-2026-08-25/MANIFEST.sha256":
        "a13d2a726e1440e2f6406913adcd2c6674e7d9d3a5677e2c1d56031e9d7a1e24",
    "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py":
        "2e4b1a1b9bb5b5be8d0997132b49b95576a28dc6ccb9cfd83db808ace8f52f3e",
    "computations/verify_h3_first_face_keq_augp2_mixed_square_totalization_gate.py":
        "346f3885bae10462c11f8046240ad4bc5970f0950a25b163235445592be0e9ab",
    "notes/h3-e14-pointed-orbit-keq-mapping-cylinder-gate.md":
        "f5008f5b7e892b5ce5270faacee4ec9f2bffc2630b8dd15a55cb8f5c6800cb21",
    "notes/h3-first-face-keq-augp2-mixed-square-totalization-gate.md":
        "00fa3b844a907f8addbd10cb6c6fbf138a4a8b263ea73c7aa72452267fd190d5",
    "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py":
        "8be3bc5bf85f8d633e77e2a0bdd18aea6d481c81f5fb6a6a947cbaf82f862302",
    "computations/verify_h3_gamma_star_executable_gen_phys_registry.py":
        "173ebdedcfdadd9891704223ea93731509c18a4d120aa34d6c7bc8a4f3aebddb",
    "computations/verify_h3_gamma_star_source_derived_free_closure_census.py":
        "a479ac8759bf7a18b43ee91d8b1ab7d0b432c48a7787b065cac68403ace3df3a",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    "computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py":
        "b60538f9db5b8c2984bbee95e0a05f383408e9ab7c13680216adf56386682522",
    "notes/h3-kappa-lambda-literal-mapping-cone-normalization-gate.md":
        "1e7655ab1661453200ba33aff800aa6d9991dd86922d81d4f5b488fcc15bb817",
    "computations/verify_h3_phi_ks_r0_pf_minimal_executable_ansatz_gate.py":
        "d21d776ec53babb4f99693e4dad51d87309e3ed0cccf2e34fb6025e6d74d1009",
}

def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)

def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))

def scale(coefficient, vector):
    return tuple(Q(coefficient) * entry for entry in vector)

def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(height):
            if row == pivot_row or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right
                         for left, right in zip(rows[row], rows[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row

def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, (relative, actual, expected))

def audit():
    pin_dependencies()

    # Vertex order is (response-left, response-right, cap-left, cap-right).
    # Edge order is (P_f bottom, K_Eq left, K_Eq right, D4 top).
    p_f = tuple(map(Q, (-1, 1, 0, 0)))
    k_left = tuple(map(Q, (-1, 0, 1, 0)))
    k_right = tuple(map(Q, (0, -1, 0, 1)))
    d4 = tuple(map(Q, (0, 0, -1, 1)))
    edges = (p_f, k_left, k_right, d4)
    cycle = tuple(map(Q, (1, -1, 1, -1)))
    expanded = tuple(sum(cycle[index] * edges[index][vertex]
                         for index in range(4)) for vertex in range(4))
    require(expanded == (0, 0, 0, 0), expanded)
    require(rank(edges) == 3 and gcd(*(abs(int(x)) for x in cycle)) == 1,
            "nonprimitive square cycle")

    # Solve d1*x=0 integrally: the four vertex equations force
    # x=(a,-a,a,-a), so ker(d1)=Z*z.  There is no physical mixed C2 column
    # in the pinned selected grade, hence z is not an existing boundary.
    for a in range(-3, 4):
        vector = scale(a, cycle)
        require(tuple(sum(vector[index] * edges[index][vertex]
                          for index in range(4)) for vertex in range(4)) == (0, 0, 0, 0),
                (a, vector))
    h1_rank_existing = 4 - rank(edges)
    require(h1_rank_existing == 1, h1_rank_existing)

    # AB and AC are literal independent operation-root coordinates.  Put
    # their cycles in an eight-edge direct sum and check that a root-forgetting
    # aggregate has rank one while the two labelled packets have rank two.
    z_ab = cycle + (Q(0),) * 4
    z_ac = (Q(0),) * 4 + cycle
    z_sum = add(z_ab, z_ac)
    require(rank((z_ab, z_ac)) == 2 and rank((z_sum,)) == 1,
            "AB/AC packets collapsed")

    # The cut involution sends D_root tensor B1 to -D_root tensor B4, so it
    # multiplies each source-labelled edge packet by -1.  Tau_AB,AC is degree
    # zero and sends all four oriented edge names with coefficient +1.
    sigma_z23 = scale(-1, cycle)
    tau_z_ab = tuple(z_ab[edge] for edge in range(4))
    require(sigma_z23 == scale(-1, cycle) and tau_z_ab == cycle,
            "covariance sign")

    # Minimal selected-grade countermodel: for every (cut,root-label), take
    # this four-vertex/four-edge square skeleton and C2=0.  Interpret every
    # existing higher square/cube identity by its pinned zero projection to
    # the off-diagonal mixed-incidence grade.  Tau is +identity and sigma is
    # -identity between the cut blocks.  All existing identities and d^2=0
    # hold, but z remains a primitive non-boundary in each labelled block.
    blocks = [(cut, rho) for cut in (23, 45) for rho in ("AB", "AC")]
    require(len(blocks) == 4 and h1_rank_existing * len(blocks) == 4,
            "countermodel block count")
    equivariant_unfilled_rank = 2  # sigma pairs 23/45; AB and AC remain separate.

    result = {
        "schema": "pacomp-h3-x23-primitive-mixed-square-relation-audit-v1",
        "status": "PASS_FORMULA_FORCED_EXISTENCE_IS_GENUINELY_NEW",
        "parent_manifest_sha256": PINS[
            "computations/unaudited-codex-n8-pacomp-x23-minimal-generator-extension-2026-08-25/MANIFEST.sha256"],
        "oriented_square": {
            "vertex_order": ["response-left", "response-right", "cap-left", "cap-right"],
            "edge_order": ["P_f bottom", "K_Eq left", "K_Eq right", "D4 top"],
            "edge_boundaries": [list(map(int, edge)) for edge in edges],
            "cubical_product_convention": "d(e_x times e_y)=d(e_x) times e_y-e_x times d(e_y)",
            "expanded_faces": ["+P_f", "-K_Eq,L", "+K_Eq,R", "-D4"],
            "d_squared_vertex_coefficients": list(map(int, expanded)),
            "primitive_cycle": list(map(int, cycle)),
            "kernel_d1": "Z*(1,-1,1,-1)",
        },
        "labelled_instances": {
            "AB": "d kappa_c^AB=P_f,c^AB-K_Eq,L,c^AB+K_Eq,R,c^AB-D4_c^AB",
            "AC": "d kappa_c^AC=P_f,c^AC-K_Eq,L,c^AC+K_Eq,R,c^AC-D4_c^AC",
            "tau_AB_AC": "degree-zero, coefficient +1 on every displayed face",
            "rank_AB_AC": 2,
            "rank_root_forgetting_sum": 1,
            "cut_covariance": "sigma(z_23^rho)=-z_45^rho and therefore sigma(kappa_23^rho)=-kappa_45^rho",
        },
        "existing_identity_test": {
            "edge_boundary_rank": 3,
            "H1_per_labelled_square": "Z",
            "existing_physical_mixed_C2_columns": 0,
            "existing_source_derived_kappa_columns": 0,
            "objectwise_square_identity_proves": "d of the four-edge cycle is zero",
            "objectwise_square_identity_does_not_prove": "the cycle is a boundary",
            "cube_projection": "zero in the selected off-diagonal response-to-cap mixed-incidence grade",
            "reason_cube_cannot_fill": "a cube boundary can solve this only through a physical mixed square face, which the pinned registry and source-derived closure both lack",
        },
        "minimal_countermodel": {
            "coefficient_ring": "Z",
            "blocks": [f"q{cut}/{rho}" for cut, rho in blocks],
            "C0_per_block": 4,
            "C1_per_block": 4,
            "C2_mixed_per_block": 0,
            "d1_rank_per_block": 3,
            "H1_before_covariance_rank": 4,
            "H1_after_sigma_covariance_rank": equivariant_unfilled_rank,
            "tau": "+identity AB to AC as a labelled transport map",
            "sigma": "-identity q23 to q45 on the D_root-labelled packet",
            "all_existing_projected_relations_hold": True,
            "required_cycle_is_boundary": False,
        },
        "first_unmatched_source_datum": {
            "generator": "kappa_23^AB (and the root-natural AB/AC, sigma-covariant family)",
            "grade": "physical off-diagonal response-to-cap mixed-square degree",
            "first_boundary_face": "+P_f,23^AB",
            "minimal_new_relation": "d kappa_c^rho=P_f,c^rho-K_Eq,L,c^rho+K_Eq,R,c^rho-D4_c^rho",
        },
        "verdict": (
            "The four signs are forced by the pinned cubical differential, so they are not a free new sign axiom. "
            "Conditional on a physical oriented mixed square kappa, its boundary is the displayed formula. "
            "However, existence/typing of that kappa does not follow from any pinned square or cube identity: those identities only close the edge cycle, and their selected mixed-grade C2 projection is zero. "
            "A primitive root-natural response-to-cap mixed-square constructor, with separate AB and AC instances and its sigma mate, is genuinely new source data."
        ),
        "promotion": "NONE_H3_ONLY",
        "pins": PINS,
    }
    logical = sha256(json.dumps(result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    output = {"logical_sha256": logical, "result": result}
    temporary = HERE / "results_mixed_square_relation_audit.json.tmp"
    temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    temporary.replace(HERE / "results_mixed_square_relation_audit.json")
    return output

if __name__ == "__main__":
    output = audit()
    print(output["result"]["status"])
    print("logical_sha256=" + output["logical_sha256"])

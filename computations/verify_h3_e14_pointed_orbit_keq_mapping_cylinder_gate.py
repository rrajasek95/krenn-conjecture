#!/usr/bin/env python3
"""Audit the pointed-orbit/central-Eq mapping-cylinder obstruction.

Coefficientwise, the moving-target D4 top and the clean central K_Eq edge
add to the desired E14 placement.  This does not yet define a physical
source map: the bottom pointed conormal, the two objectwise Eq edges, and
the D4 top form the boundary of a square.  Before a mixed comparison face
is adjoined, that boundary is the primitive H_1 of the square skeleton.

The checker also composes the physical C-plus identity.  The D4 occurrence
top is not the hidden root-lower face -E.  The latter is a proper face of
the sought mixed cell.  Rooted d_even is not produced by D4 plus the cap
graph alone; it becomes composite only after primitive cap p, physical
K_Eq descent n, and the literal face3/5 -> B4/B1 label map are all present.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from math import gcd
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_anchor_conormal_functoriality_bridge.py":
        "83879756547765878c36944c1ab14827ab77a1f217931bc05db0c72cb0af32a8",
    "notes/h3-anchor-conormal-functoriality-bridge.md":
        "ff21fee754b3de39788dca5c6d024a6a7f539648fb3cc9473c2690239c8bbac8",
    "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py":
        "67d33b03ec52c619f29e76c917fdba9b7e28380b4349291fa37b6b7d511e241c",
    "notes/h3-e14-orbit-relative-d4-target-cone-gate.md":
        "6268689c54144cc09b6be596b81d8b4aa741e0590a83e664ec3f6e65b89187bf",
    "computations/verify_h3_e14_t12_orbit_unary_companion_cycle_gate.py":
        "28a0baf3e6930e9336ceb5632e0abb8509a21ddaa1446eb7e93482831c35bc42",
    "notes/h3-e14-t12-orbit-unary-companion-cycle-gate.md":
        "9d04e359afb3a47b4e547797a00c29f7559a060aa51a69fdda984c0e988f2765",
    "computations/verify_h3_cplus_conditional_physical_dressing_assembly.py":
        "e8014fdfd2263a8eb6bffff11e31c339b5b7965989a61324f8d118a91f791f46",
    "notes/h3-cplus-conditional-physical-dressing-assembly.md":
        "b3afd746e6c275ca23e0b3ee5f26dfbc763301ed7371be4377612709904c19c0",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "notes/h3-augmented-p2-section-shortest-conditional-gate.md":
        "ee5da6f0911feb06707106cc6207161bbac7cabd31885f554321698dfbb989d8",
}
EXPECTED_LEDGER_SHA256 = (
    "12cfdfac6b8c3b76b2445a443404e0575ee61aa2d8b7ad816cc154151e2ccf21"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
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


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in vector)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def mapping_cylinder_square_audit() -> dict[str, object]:
    # Four vertices are the two presentation rows at the two D4 endpoints.
    # Edges are ordered (bottom P_f, left Eq, right Eq, top D4).  Objectwise
    # functoriality gives the four edges.  A derived natural transformation
    # additionally needs the square filler.
    bottom_pf = tuple(map(Q, (-1, 1, 0, 0)))
    left_eq = tuple(map(Q, (-1, 0, 1, 0)))
    right_eq = tuple(map(Q, (0, -1, 0, 1)))
    top_d4 = tuple(map(Q, (0, 0, -1, 1)))
    edge_boundaries = (bottom_pf, left_eq, right_eq, top_d4)
    square_cycle = tuple(map(Q, (1, -1, 1, -1)))
    boundary_of_cycle = tuple(
        sum(square_cycle[column] * edge_boundaries[column][row]
            for column in range(4))
        for row in range(4)
    )
    require(rank(edge_boundaries) == 3
            and boundary_of_cycle == (0, 0, 0, 0)
            and gcd(*(abs(int(value)) for value in square_cycle)) == 1,
            ("the primitive mapping-square cycle changed", boundary_of_cycle))

    # With no C2 face, H1 has rank 4-rank(d1)=1.  Adjoining exactly one
    # mixed face with this boundary kills it.  This is integral, hence its
    # base change to Z[beta], its generic fibre, and its beta=0 fibre all
    # retain the same one-dimensional obstruction until the integral face
    # is supplied.
    h1_before = 4 - rank(edge_boundaries)
    h1_after = h1_before - rank((square_cycle,))
    require((h1_before, h1_after) == (1, 0),
            "the mapping-square homology changed")

    # After forgetting source idempotents, only (private return R,
    # central Eq incidence E) remain.  Here D4+K_Eq is coefficient-exact.
    orbit_top = (Q(1), Q(0))
    clean_keq = (Q(0), Q(1))
    required_shadow = (Q(1), Q(1))
    cap_graph = (Q(0), Q(0))
    require(add(orbit_top, clean_keq) == required_shadow
            and rank((orbit_top, clean_keq)) == 2,
            "the coefficient-level D4/K_Eq assembly changed")

    # Restore the primitive square-homology coordinate.  Separate edge
    # data have zero mixed incidence; the actual physical comparison has
    # incidence one.  The last coordinate is the cotangent/excess class.
    orbit_typed = (Q(1), Q(0), Q(0))
    keq_typed = (Q(0), Q(1), Q(0))
    cap_typed = (Q(0), Q(0), Q(0))
    required_typed = (Q(1), Q(1), Q(1))
    excess_dual = (Q(0), Q(0), Q(1))
    require(rank((orbit_typed, keq_typed, cap_typed)) == 2
            and rank((orbit_typed, keq_typed, required_typed)) == 3
            and dot(excess_dual, orbit_typed) == 0
            and dot(excess_dual, keq_typed) == 0
            and dot(excess_dual, cap_typed) == 0
            and dot(excess_dual, required_typed) == 1,
            "the primitive physical excess dual changed")

    return {
        "two_presentation_rows": [
            "bottom pointed occurrence/conormal row",
            "top moving-target D4 occurrence row",
        ],
        "edge_order": ["P_f bottom", "K_Eq left", "K_Eq right", "D4 top"],
        "d1_rank": 3,
        "primitive_boundary_cycle": [1, -1, 1, -1],
        "H1_without_mixed_face": "Z",
        "H1_after_one_mixed_face": 0,
        "coefficient_forgetful_quotient": {
            "rows": ["private return R_E14", "central Eq incidence E"],
            "D4_top": [1, 0],
            "clean_K_Eq": [0, 1],
            "required_shadow": [1, 1],
            "D4_plus_K_Eq_equals_shadow": True,
        },
        "physical_source_typed_quotient": {
            "rows": ["R_E14", "central E", "mixed square incidence"],
            "available_rank": 2,
            "rank_with_required_comparison": 3,
            "primitive_dual": [0, 0, 1],
        },
        "functoriality_verdict": (
            "a full pointed derived-algebra natural transformation includes "
            "the mixed square and then forces the equality; objectwise "
            "pointed algebra functoriality supplies only the edges and does "
            "not construct the square"
        ),
        "beta_scope": (
            "the primitive H1 is free over Z, so it persists over Z[beta], "
            "the generic fibre, and beta=0; only an integral mixed face "
            "supplies the Bockstein-compatible comparison"
        ),
    }


def coupled_physical_face_audit() -> dict[str, object]:
    assembly = load(
        "computations/verify_h3_cplus_conditional_physical_dressing_assembly.py",
        "pointed_orbit_cplus_assembly",
    )
    core = assembly.core_assembly_audit()
    require(core["clean_K_Eq_factorization"] == (
        "P2_hidden(-E,0,0)+O_-E(E,E,-E)+"
        "2D_root*d_even(0,0,E)=(0,E,0)"
    ), "the coupled physical K_Eq identity changed")

    # Normalize one nonzero coefficient of E and retain
    # (D4 return, root lower, root Eq, rooted ores).  The D4 occurrence top
    # and P2 hidden face occupy different direct-sum rows.
    d4_top = tuple(map(Q, (1, 0, 0, 0)))
    p2_hidden = tuple(map(Q, (0, -1, 0, 0)))
    old_o_minus_e = tuple(map(Q, (0, 1, 1, -1)))
    rooted_d_even = tuple(map(Q, (0, 0, 0, 1)))
    clean_root_eq = tuple(map(Q, (0, 0, 1, 0)))
    require(add(p2_hidden, old_o_minus_e, rooted_d_even) == clean_root_eq
            and rank((d4_top, p2_hidden)) == 2,
            "D4 top and hidden P2 face became incorrectly identified")
    hidden_dual = tuple(map(Q, (0, 1, 0, 0)))
    require(dot(hidden_dual, d4_top) == 0
            and dot(hidden_dual, p2_hidden) == -1,
            "the hidden-root-lower separator changed")

    # The D4 codimension-one signs do equal D_root.  Turning this sign
    # coincidence into the hidden physical packet needs the additional
    # labelled face map D3 occurrence -> -(B1+B4)=-2*d_even.
    top = (0, 1, 2, 3)
    d3_faces = tuple(combinations(top, 3))
    d4_signs = []
    for face in d3_faces:
        missing = next(index for index in top if index not in face)
        position = tuple(sorted(face + (missing,))).index(missing)
        d4_signs.append(Q((-1) ** position))
    d_root = tuple(map(Q, (-1, 1, -1, 1)))
    v = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
    e = tuple(2 * root * label for root in d_root for label in v)
    d3_label = tuple(-2 * label for label in v)
    transported_hidden = tuple(root * label for root in d4_signs
                               for label in d3_label)
    require(tuple(d4_signs) == d_root
            and d3_label == tuple(map(Q, (0, -1, 0, 0, -1, 0)))
            and transported_hidden == scale(-1, e),
            "the D4-sign/B1-B4 hidden transfer changed")

    # D4 and the horizontal cap graph have no rooted labelled-residue row.
    # Thus they cannot by themselves give d_even.  This does not make
    # d_even an independent theorem once p+n and the literal label map are
    # included; the next calculation records that exact composition.
    d4_reduced = tuple(map(Q, (1, 0, 0)))
    cap_graph_reduced = tuple(map(Q, (0, 1, 0)))
    labelled_residue = tuple(map(Q, (0, 0, 1)))
    residue_dual = tuple(map(Q, (0, 0, 1)))
    require(rank((d4_reduced, cap_graph_reduced)) == 2
            and rank((d4_reduced, cap_graph_reduced,
                      labelled_residue)) == 3
            and dot(residue_dual, d4_reduced) == 0
            and dot(residue_dual, cap_graph_reduced) == 0
            and dot(residue_dual, labelled_residue) == 1,
            "D4+cap unexpectedly constructed rooted labelled residue")

    aug = load(
        "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py",
        "pointed_orbit_augp2",
    )
    d_even = aug.d_even_composition_audit()
    require(d_even["formula"] == (
        "d_even=-1/2[(p_3+n_3) labelled B4+"
        "(p_5+n_5) labelled B1]=(B1+B4)/2"
    ) and not d_even["separate_d_even_hypothesis_after_these_faces"],
            "the p+n+label d_even composition changed")

    # The cap identity itself: z_cap=p+n.  It needs both inputs.  The
    # horizontal cap graph only normalizes target/residue after placement;
    # it does not manufacture either source-labelled input.
    primitive_p = tuple(map(Q, (-1, -1)))
    invisible_n = tuple(map(Q, (1, 0)))
    z_cap = add(primitive_p, invisible_n)
    require(z_cap == (0, -1), "z_cap=p+n changed")

    return {
        "normalized_rows": [
            "D4 private return", "root lower", "root Eq", "root ores"
        ],
        "D4_top": [1, 0, 0, 0],
        "P2_hidden": [0, -1, 0, 0],
        "D4_top_is_literal_P2_hidden": False,
        "D4_codimension_one_signs": [-1, 1, -1, 1],
        "D4_signs_equal_D_root": True,
        "missing_D3_label_map_for_hidden_face": (
            "each marked D3 occurrence -> -(B1+B4)=-2*d_even in the "
            "physical repeated grade"
        ),
        "conditional_D3_transfer": "D_root tensor (-(B1+B4))=-E",
        "primitive_hidden_dual": [0, 1, 0, 0],
        "physical_clean_Eq_identity": (
            "P2_hidden(-E)+O_-E(E,E,-E)+rooted_d_even(+E)="
            "clean root Eq(+E)"
        ),
        "D4_plus_horizontal_cap_constructs_rooted_d_even": False,
        "D4_cap_first_missing_dual": "root-labelled ores coordinate",
        "z_cap": "p+n=(0,-ores_cap)",
        "rooted_d_even_composite_if_fully_typed": d_even["formula"],
        "rooted_d_even_requires": d_even["requires"],
        "circularity_guard": (
            "using d_even to dress K_Eq and then citing that dressed K_Eq "
            "as the n input of p+n does not construct d_even; n must be "
            "the independently source-labelled physical K_Eq descent and "
            "the B4/B1 label map must be part of the comparison"
        ),
    }


def cap_label_transfer_matrix_audit() -> dict[str, object]:
    # Source order is (face3,face5), target order is (B1,B4).  Each physical
    # p_i+n_i has scalar residue -1, hence F=-I.  The literal occurrence
    # label map swaps the two positions: face3->B4 and face5->B1.  Therefore
    # LF is the signed swap.  It is an integral isomorphism, with no hidden
    # coefficient kernel.
    face_residue = (
        (Q(-1), Q(0)),
        (Q(0), Q(-1)),
    )
    label_swap = (
        (Q(0), Q(1)),
        (Q(1), Q(0)),
    )

    def multiply(left, right):
        return tuple(tuple(sum(left[row][middle] * right[middle][column]
                               for middle in range(2))
                           for column in range(2))
                     for row in range(2))

    transfer = multiply(label_swap, face_residue)
    require(transfer == ((Q(0), Q(-1)), (Q(-1), Q(0)))
            and rank(tuple(zip(*transfer, strict=True))) == 2,
            ("the face-to-label transfer changed", transfer))
    determinant = transfer[0][0] * transfer[1][1] - (
        transfer[0][1] * transfer[1][0]
    )
    even = (Q(1), Q(1))
    odd = (Q(1), Q(-1))

    def act(matrix, vector):
        return tuple(sum(matrix[row][column] * vector[column]
                         for column in range(2)) for row in range(2))

    require(determinant == -1
            and act(transfer, even) == scale(-1, even)
            and act(transfer, odd) == odd,
            "the LF determinant/eigenspaces changed")

    # The normalized even Hasse aggregate is -1/2 times the transfer of the
    # equal face vector.  This gives exactly (B1+B4)/2.
    normalized_even = scale(Q(-1, 2), act(transfer, even))
    require(normalized_even == (Q(1, 2), Q(1, 2)),
            "the normalized d_even sign changed")
    return {
        "source_order": ["face3", "face5"],
        "target_order": ["B1", "B4"],
        "F_face_residue": [[-1, 0], [0, -1]],
        "L_literal_label_swap": [[0, 1], [1, 0]],
        "LF_signed_transfer": [[0, -1], [-1, 0]],
        "rank_LF": 2,
        "determinant_LF": -1,
        "eigenlines": {
            "even_(1,1)": -1,
            "odd_(1,-1)": 1,
        },
        "normalized_even_formula": (
            "-1/2 LF(1,1)=(1/2,1/2)=d_even in (B1,B4)"
        ),
        "coefficient_kernel": 0,
        "interpretation": (
            "if both source-labelled face sections and L are supplied, "
            "the cap-to-d_even transfer is forced and has no further scalar "
            "kernel.  A single rho-even orbit top supplies only the even "
            "line; it does not construct the odd face difference or the "
            "literal label map, though neither is an extra coefficient "
            "needed for d_even"
        ),
    }


def minimal_physical_generator_audit() -> dict[str, object]:
    # After the simultaneous p+n and face3/5 equations, four homogeneous
    # face types remain independently detected.  They may be packaged by
    # one AugP2 schema, but no one bare column implies the other three.
    p_f = tuple(map(Q, (1, 0, 0, 0)))
    primitive_cap = tuple(map(Q, (0, 1, 0, 0)))
    mixed_orbit_keq = tuple(map(Q, (0, 0, 1, 0)))
    shifted_ridge = tuple(map(Q, (0, 0, 0, 1)))
    faces = (p_f, primitive_cap, mixed_orbit_keq, shifted_ridge)
    require(rank(faces) == 4,
            "the four AugP2 homogeneous face types became dependent")

    return {
        "minimal_new_central_generator": {
            "name": "kappa_orb,Eq",
            "type": "one mixed mapping-cylinder/Tate 2-cell",
            "boundary": (
                "the primitive P_f/K_Eq/D4 naturality-square cycle, with "
                "source-labelled principal image R_E14"
            ),
            "required_equality": "Phi_orb((H0-u)e_Eq)=R_E14",
            "proper_faces": [
                "hidden root-lower -E",
                "physical invisible K_Eq cap face n",
                "literal face3/5 occurrence-to-B4/B1 label transport",
                "complete T12 face supplied afterward by the old unary row",
            ],
        },
        "independent_homogeneous_face_count_after_simultaneous_equations": 4,
        "four_face_types": [
            "P_f pointed conormal",
            "one cap base face (equivalently p or z_cap after n)",
            "mixed orbit/K_Eq cell kappa_orb,Eq",
            "shifted Kahler ridge gamma=-dOmega",
        ],
        "cap_basis_change": (
            "because n is a proper face of kappa_orb,Eq and z_cap=p+n, "
            "the bases (p,kappa) and (z_cap,kappa) differ triangularly "
            "with determinant one; the independent face count stays four"
        ),
        "not_additional_after_full_typing": {
            "z_cap": "p+n",
            "d_even": "-1/2 of the labelled face3/5 p+n sum",
            "P2_hidden": "a mandatory proper face of kappa_orb,Eq",
            "T12": "old unary U plus R_E14",
            "dq": "Leibniz consequence of a PP-module map",
        },
        "grading_scope": {
            "bottom_cap_object": (
                "word 01211222, fine t*q_(v,N), repeated P3+K2"
            ),
            "P2_lower_objects": (
                "words 0112/q23:21 and 0121/q45:12 with root decoration"
            ),
            "D4_response_orbit": "110000 -> G11[111111]",
            "E14_unary_output": "word 000101",
            "consequence": (
                "kappa_orb,Eq is an off-diagonal word/fine/repeated-grade "
                "comparison; polynomial multiplication or same-word "
                "functoriality cannot supply it"
            ),
        },
        "ridge_scope": (
            "the central cell does not construct the shifted pq/xv Kahler "
            "placement; gamma remains an independent homogeneous face, "
            "after which eta/sigma are forced by contraction"
        ),
        "beta_scope": (
            "canonical h=3 and beta-independent at the primitive square; "
            "the beta=0/D0 branch closes only if the entire mixed cell and "
            "its proper faces are defined integrally over k[beta]"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "pointed orbit/K_Eq mapping-cylinder excess gate",
        "pins": PINS,
        "mapping_cylinder": mapping_cylinder_square_audit(),
        "coupled_physical_faces": coupled_physical_face_audit(),
        "cap_label_transfer_matrix": cap_label_transfer_matrix_audit(),
        "minimal_generator_and_scope": minimal_physical_generator_audit(),
        "verdict": (
            "D4 top plus clean K_Eq gives the desired coefficient shadow, "
            "but objectwise pointed functoriality does not fill the "
            "primitive mapping-square H1.  The exact remaining datum is one "
            "source-labelled mixed 2-cell kappa_orb,Eq.  Its physical proper "
            "faces include, but are not equal to, P2_hidden and the labelled "
            "cap descent."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("coefficient shadow D4+K_Eq: CLOSED")
    print("physical pointed mapping square H1: Z")
    print("D4 top is P2 hidden -E: NO")
    print("d_even from D4+cap alone: NO")
    print("d_even from typed p+n+face3/5 labels: YES")
    print("minimal new central datum: one mixed mapping-cylinder 2-cell")
    print("independent AugP2 homogeneous face types after composition: 4")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

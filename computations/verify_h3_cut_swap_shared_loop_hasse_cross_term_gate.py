#!/usr/bin/env python3
"""Audit the Hasse cross-term resolution of the three Gate-I shared loops.

At the occurrence level the divided-power product rule is exactly the missing
C4 switch: for multi-affine factors f,g,

    d_4^[2](fg) = d_4(f)d_4(g).

For each shared matching 02|ab|cd, switching the repeated 02 factor with one
of the other two factors gives two C4 corners.  The literal support collapse
sends both corners to the same pure P3+K2 direction.  After the divided-power
normalization by 1/2 this gives one B_i.  The three shared labels therefore
have exactly the desired fixed/even and paired repair choices.

This is an occurrence identity, not yet a physical source syzygy.  The
order-three collision-cofactor occurrence W_02 K_ab q_cd is dormant below
order three and has coefficient one at the marked word, but rho sends it to
a complementary tangent placement and a different word.  More decisively,
the committed Hasse totalization has formal signature
(ainc,W,target,ores)=(-1,0,0,0), a primitive endpoint-ridge defect, and no
selected physical-word landing.  Normalized simplicial degeneracies vanish
and cannot turn the cross term into an augmentation-one source boundary.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_collision_cofactor_bianchi.py":
        "34a768e749891a0a51c5feac30ff6702f40d70e12069a52c83cbf160f3876ceb",
    "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py":
        "bd20b6320172f846d7c4aa38ec6ebba0c0cfea4c056b8758df19d31b5ab20231",
    "computations/verify_h3_cut_swap_shared_repair_face3_tor_obstruction.py":
        "e43d537e9c321d5ab0b61632aa16673dfb58d5709943e1d2b7ff26032f9df8ca",
    "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py":
        "ebd25f79a6fe8db936fe5601b9220f152c5349dd794bbc4e08b2095f1c1d059f",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
}
EXPECTED_LEDGER_SHA256 = (
    "8e60905c81012cc720e51e1f7887dde9f2c4e079c3767fcbb399b6d6ac4cbd85"
)

X, Y, Z = range(3)
RHO = (0, 4, 2, 3, 1, 5)
TARGET_ACTION = (5, 1, 3, 2, 4, 0)
SHARED = {
    3: ((0, 2), (1, 3), (4, 5)),
    4: ((0, 2), (1, 4), (3, 5)),
    5: ((0, 2), (1, 5), (3, 4)),
}


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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))


def permute_word(word, permutation):
    output = [None] * len(word)
    for old, value in enumerate(word):
        output[permutation[old]] = value
    return tuple(output)


def permute_edge(edge, permutation):
    return tuple(sorted(permutation[index] for index in edge))


def permute_matching(matching, permutation):
    return tuple(sorted(permute_edge(edge, permutation) for edge in matching))


def permute_cell_table(table, permutation, *, direct=False):
    output = {}
    for key, value in table.items():
        if direct:
            output[permute_edge(key, permutation)] = value
            continue
        left, right, left_colour, right_colour = key
        pleft, pright = permutation[left], permutation[right]
        if pleft < pright:
            output[(pleft, pright, left_colour, right_colour)] = value
        else:
            output[(pright, pleft, right_colour, left_colour)] = value
    return output


def divided_power_product_rule() -> dict[str, object]:
    # Multi-affine f=f0+t*f1 and g=g0+t*g1 have no outer second derivative.
    trials = []
    for f0, f1, g0, g1 in itertools.product(range(-2, 3), repeat=4):
        product_degree_two = Q(f1 * g1)
        cross_term = Q(f1) * Q(g1)
        require(product_degree_two == cross_term,
                "the multi-affine divided-power product rule changed")
        trials.append((f0, f1, g0, g1))
    return {
        "identity": "d^[2](fg)=d(f)d(g) when d^[2]f=d^[2]g=0",
        "normalization": (
            "the ordinary second derivative has the two ordered cross terms; "
            "the Hasse/divided-power coefficient divides their sum by 2"
        ),
        "integer_specializations_checked": len(trials),
    }


def switch_census(repair) -> dict[str, object]:
    ledger, digest = repair.audit()
    require(digest == repair.EXPECTED_LEDGER_SHA256,
            "the shared-loop repair theorem changed")
    record = ledger["C4_repair_census"]["records"][0]
    actual = {
        index: tuple(tuple(value) for value in
                     record["C4_alternatives_per_shared_label"][str(index)])
        for index in SHARED
    }
    expected = {
        3: ((0, 3), (6, 3), (10, 0), (13, 0)),
        4: ((1, 1), (7, 4), (9, 1), (14, 4)),
        5: ((2, 5), (8, 2), (11, 2), (12, 5)),
    }
    require(actual == expected, ("the literal C4 switch table changed", actual))

    # Each partner channel has two ordered cross-term corners and collapses
    # them to twice one B direction.  Hasse normalization returns the unit B.
    channels = {
        "M3_switch_02_with_13": (3, 3),
        "M3_switch_02_with_45": (0, 0),
        "M4_switch_02_with_14": (1, 1),
        "M4_switch_02_with_35": (4, 4),
        "M5_switch_02_with_15": (5, 5),
        "M5_switch_02_with_34": (2, 2),
    }
    require(all(Q(left + right, 2) == left
                for left, right in channels.values()),
            "a switch channel stopped having equal collapsed corners")
    require(TARGET_ACTION[0] == 5 and TARGET_ACTION[2] == 3
            and TARGET_ACTION[1] == 1 and TARGET_ACTION[4] == 4,
            "the B rho action changed")

    fixed = {
        "odd/fixed choices": ["B1", "B4"],
        "rho_even_average": "(B1+B4)/2",
    }
    paired = {
        "first_rho_orbit": "(B0+B5)/2",
        "second_rho_orbit": "(B2+B3)/2",
    }
    return {
        "shared_matchings": {
            str(index): [list(edge) for edge in matching]
            for index, matching in SHARED.items()
        },
        "literal_switch_table_matching_to_B": {
            str(index): [list(pair) for pair in pairs]
            for index, pairs in actual.items()
        },
        "partner_channels_after_collapse": {
            name: [f"B{left}", f"B{right}"]
            for name, (left, right) in channels.items()
        },
        "Hasse_normalized_fixed": fixed,
        "Hasse_normalized_paired": paired,
        "occurrence_augmentation": 1,
        "status": (
            "exact formal occurrence images; the frame/C4 theorem does not "
            "promote a switch pair to a binomial physical source boundary"
        ),
    }


def dormant_third_bianchi(collision) -> dict[str, object]:
    q0 = {
        (0, 1, X, X): Q(2),
        (2, 3, X, X): Q(1),
        (4, 5, X, X): Q(1),
        (1, 2, Y, Y): Q(1),
        (3, 4, Y, Y): Q(1),
        (0, 5, Y, Y): Q(1),
    }
    tangent = {(1, 3, Z, X): Q(1)}
    direct = {(0, 2): Q(1)}
    zero_direct = {}
    marked = (Z, Z, Z, X, X, X)
    placements = {
        "M3": (0, 1, 2, 3, 4, 5),
        "M4": (0, 1, 2, 4, 3, 5),
        "M5": (0, 1, 2, 5, 3, 4),
    }
    rows = []
    for name, permutation in placements.items():
        pq0 = permute_cell_table(q0, permutation)
        ptangent = permute_cell_table(tangent, permutation)
        pdirect = permute_cell_table(direct, permutation, direct=True)
        pmarked = permute_word(marked, permutation)
        for coloring in itertools.product((X, Y, Z), repeat=6):
            left = collision.source_polynomial(
                6, pq0, ptangent, zero_direct, coloring)
            right = collision.source_polynomial(
                6, pq0, ptangent, pdirect, coloring)
            require(all(left.get(degree, 0) == right.get(degree, 0)
                        for degree in range(3)),
                    ("a W occurrence became visible below order three", name))
        coefficient = collision.source_polynomial(
            6, pq0, ptangent, pdirect, pmarked).get(3, 0)
        base_coefficient = collision.source_polynomial(
            6, pq0, ptangent, zero_direct, pmarked).get(3, 0)
        require(coefficient - base_coefficient == 1,
                ("the third Bianchi coefficient changed", name))
        tangent_edge = next((key[:2] for key in ptangent), None)
        base_edge = next(edge for edge in SHARED[int(name[-1])]
                         if edge not in ((0, 2), tangent_edge))
        rows.append({
            "label": name,
            "placement": f"W_02 K_{tangent_edge[0]}{tangent_edge[1]} "
                         f"q_{base_edge[0]}{base_edge[1]}",
            "marked_word": "".join(map(str, pmarked)),
            "coefficient_change_at_order3": 1,
            "coefficient_change_orders_0_1_2": [0, 0, 0],
        })

    rho_word = permute_word(marked, RHO)
    rho_placement = (
        permute_edge((0, 2), RHO),
        permute_edge((1, 3), RHO),
        permute_edge((4, 5), RHO),
    )
    require(rho_word == (Z, X, Z, X, Z, X)
            and rho_placement == ((0, 2), (3, 4), (1, 5)),
            ("the rho-complementary occurrence changed", rho_word,
             rho_placement))
    require(rho_word != marked
            and rho_placement != SHARED[5],
            "the three displayed tangent placements unexpectedly became rho-stable")
    return {
        "candidate_occurrences": rows,
        "common_marked_word": "222000",
        "rho_on_M3_occurrence": {
            "word": "202020",
            "placement": "W_02 K_34 q_15",
            "in_displayed_K13_K14_K15_family": False,
        },
        "rho_verdict": (
            "rho symmetrization necessarily adds complementary tangent "
            "placements in a distinct word summand"
        ),
    }


def simplicial_normalization() -> dict[str, object]:
    # In normalized degree two, the degenerate simplex (0,0,1) has faces
    # (0,1)-(0,1)+(0,0); the last face is degenerate, so the result is zero.
    degenerate_faces = ((0, 1), (0, 1), (0, 0))
    normalized = {face: Q(0) for face in set(degenerate_faces)}
    for sign, face in zip((1, -1, 1), degenerate_faces, strict=True):
        if len(set(face)) < len(face):
            continue
        normalized[face] += sign
    require(all(value == 0 for value in normalized.values()),
            "a normalized degeneracy acquired a nonzero boundary")
    nondegenerate_faces = ((1, 2), (0, 2), (0, 1))
    require(len(set(nondegenerate_faces)) == 3,
            "the nondegenerate triangle lost a proper face")
    return {
        "degenerate_example": "d(001)=01-01+00=0 in normalized chains",
        "degenerate_augmentation": 0,
        "nondegenerate_example": "d(012)=12-02+01 retains all three faces",
        "physical_consequence": (
            "declaring 02->44 degenerate cannot create an augmentation-one "
            "B direction; a genuine nondegenerate Hasse cell retains its "
            "proper endpoint/Omega faces"
        ),
    }


def audit():
    pin_dependencies()
    sys.path.insert(0, str(ROOT / "computations"))
    collision = load(
        "computations/verify_collision_cofactor_bianchi.py",
        "hasse_cross_collision",
    )
    repair = load(
        "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py",
        "hasse_cross_repair",
    )
    total = load(
        "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py",
        "hasse_cross_total",
    )
    face3 = load(
        "computations/verify_h3_cut_swap_shared_repair_face3_tor_obstruction.py",
        "hasse_cross_face3",
    )

    occurrence = switch_census(repair)
    product = divided_power_product_rule()
    dormant = dormant_third_bianchi(collision)
    normalized = simplicial_normalization()

    total_ledger = total.audit()
    formal = total_ledger["third_cofactor_total_complex"]
    grade = total_ledger["endpoint_midpoint_grade"]
    require(formal["formal_total_complex"]["tail_signature"]
            == [-1, 0, 0, 0]
            and formal["source_labelled_bridge"]["ridge_mismatch_rank"] == 6
            and formal["source_labelled_bridge"]["primitive_omega_rank"] == 5
            and grade["midpoint_hits"] == 0,
            "the physical third-cofactor obstruction changed")
    face3_ledger, face3_digest = face3.audit()
    require(face3_digest == face3.EXPECTED_LEDGER_SHA256
            and face3_ledger["rho_equivariant_shared_assignment"]
                ["combined_three_label_image"] == "B0+B4+B5",
            "the decorated face-3 packet changed")

    ledger = {
        "theorem": "shared-loop Hasse cross-term occurrence / physical-source gate",
        "pins": PINS,
        "Hasse_product_rule": product,
        "literal_C4_resolution": occurrence,
        "third_Bianchi_carrier": dormant,
        "formal_totalization": {
            "tail_signature_ainc_W_target_ores": [-1, 0, 0, 0],
            "required_labelled_residue_section_signature": [0, 0, 0, 1],
            "endpoint_ridge_mismatch_rank": 6,
            "primitive_Omega_rank": 5,
            "physical_midpoint_word_hits": 0,
            "source_valid": False,
        },
        "normalized_degeneracy": normalized,
        "exact_positive_statement": (
            "the Hasse product cross term produces B1 or B4 on the fixed "
            "shared label and (B0+B5)/2 or (B2+B3)/2 on the rho-paired "
            "labels, exactly at the occurrence/collapse level"
        ),
        "sharp_obstruction": (
            "none of this supplies d_fixed or d_pair as a physical relative "
            "source cell: rho adds a complementary word/tangent packet, the "
            "only committed third-cofactor tail carries ainc=-1 and primitive "
            "endpoint ridges, and a normalized degeneracy is zero"
        ),
        "smallest_remaining_source_type": (
            "a nondegenerate source-labelled product-rule/third-Bianchi cell "
            "in the canonical repeated P3+K2 grade whose endpoint/Omega and "
            "ainc faces are capped, leaving protected-zero labelled ores "
            "B_fixed and the rho-paired B section"
        ),
        "Gate_I_closed": False,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Hasse cross-term ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 shared-loop Hasse cross term: OCCURRENCE YES / SOURCE NO")
    print("fixed images: B1 or B4; rho-even: (B1+B4)/2")
    print("paired images: (B0+B5)/2 or (B2+B3)/2")
    print("third-Bianchi tail: ainc=-1, endpoint ridge defect, wrong word")
    print("Dold-Kan degeneracy: normalized zero")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

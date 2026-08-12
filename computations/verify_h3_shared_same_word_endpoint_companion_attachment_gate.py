#!/usr/bin/env python3
"""Compare the rootless q companion with the E14 endpoint-orientation cycle.

The two obstructions have isomorphic *uncoloured* two-edge tails.  This
checker verifies that no site relabelling together with a global colour
permutation identifies their decorated tails, and that their source-operation
grades are different.  The two missing colour changes form a Segre square:
there is a quadratic binomial but no linear same-word comparison.

It also records the smallest sufficient attachment.  In coordinates

    (E_plus, E_minus, Omega, q_comp),

the existing E14 signless row is S=(1,1,0,0), and the rootless bar is
B=(0,0,-1,1).  A literal same-word cell

    A=(1,-1,1,-1)

would give D=A+B=(1,-1,0,0); together S and D isolate both endpoint
orientations after inverting 2.  The present inventories do not contain A.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "809408d026ad9d29966d816002bd8984819972875c37ece5298081756bfd38c7"
PINS = {
    "computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py":
        "37251145d805861b2d1b15b7bf37cf9f98ba30b03fbcffa1daa4fc35789efe84",
    "notes/h3-rootless-one-face-third-cofactor-comparison-vertex-gate.md":
        "f510e17ea2cfc72452b28e982530a59d60276eb193be6b0fdb7d4e29e4246739",
    "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py":
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "notes/h3-c6-e14-unary-spair-first-reduction-boundary.md":
        "9d3af91f0e97079c8e2bd2dd76db110fdde45e71eed0d21805bdd4575a683c4f",
}

RESIDUAL_SITES = (2, 3, 4, 5)
E14_MATCHING = frozenset({frozenset({2, 4}), frozenset({3, 5})})
ROOTLESS_MATCHING = frozenset({frozenset({2, 3}), frozenset({4, 5})})
E14_COLOURS = {2: 1, 3: 1, 4: 1, 5: 1}
ROOTLESS_COLOURS = {2: 2, 3: 1, 4: 1, 5: 2}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def rank(columns) -> int:
    """Exact column rank over Q for small dense vectors."""
    if not columns:
        return 0
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(len(columns[0]))]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [left - factor * right
                           for left, right in zip(matrix[row],
                                                  matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def mapped_matching(site_map, matching):
    return frozenset(
        frozenset(site_map[site] for site in edge)
        for edge in matching
    )


def relabelling_gate():
    matching_maps = []
    decorated_maps = []
    for image in permutations(RESIDUAL_SITES):
        site_map = dict(zip(RESIDUAL_SITES, image))
        if mapped_matching(site_map, E14_MATCHING) != ROOTLESS_MATCHING:
            continue
        matching_maps.append(tuple(site_map[site] for site in RESIDUAL_SITES))
        for colour_image in permutations((0, 1, 2)):
            colour_map = dict(zip((0, 1, 2), colour_image))
            transported = {
                site_map[site]: colour_map[E14_COLOURS[site]]
                for site in RESIDUAL_SITES
            }
            if transported == ROOTLESS_COLOURS:
                decorated_maps.append((site_map, colour_map))

    require(len(matching_maps) == 8,
            ("uncoloured matching-map count changed", len(matching_maps)))
    require(not decorated_maps,
            "a global colour/site relabelling unexpectedly identifies tails")
    require(len(set(E14_COLOURS.values())) == 1
            and len(set(ROOTLESS_COLOURS.values())) == 2,
            "colour-multiplicity obstruction changed")
    return {
        "e14_tail": "24:11|35:11",
        "rootless_tail": "23:21|45:12",
        "uncoloured_site_relabellings": len(matching_maps),
        "example_site_map_3_swap_4": [2, 4, 3, 5],
        "decorated_site_plus_global_colour_relabellings": 0,
        "obstruction": (
            "a global colour permutation preserves constant colouring; "
            "1111 cannot become 2112"
        ),
    }


def segre_square_gate():
    # Coordinates record whether sites 2 and 5 have been changed 1 -> 2.
    monomials = {
        "q00": ("a23_11", "a45_11"),
        "q10": ("a23_21", "a45_11"),
        "q01": ("a23_11", "a45_12"),
        "q11": ("a23_21", "a45_12"),
    }
    require(len(set(monomials.values())) == 4,
            "the four Segre-square monomials collided")

    # Distinct monomials are a four-dimensional coefficient basis.  The only
    # elementary relation appears after multiplication (the 2x2 minor).
    coefficient_columns = [tuple(int(row == column) for row in range(4))
                           for column in range(4)]
    require(rank(coefficient_columns) == 4,
            "the Segre corners acquired a linear relation")
    left = tuple(sorted(monomials["q00"] + monomials["q11"]))
    right = tuple(sorted(monomials["q10"] + monomials["q01"]))
    require(left == right, "Segre binomial stopped being tautological")

    # The edge differences span the sum-zero hyperplane, but q11-q00 reaches
    # it only through q10 or q01: these are separate decorated source words.
    q00, q10, q01, q11 = range(4)
    edge_columns = []
    for head, tail in ((q10, q00), (q11, q01),
                       (q01, q00), (q11, q10)):
        column = [0] * 4
        column[head], column[tail] = 1, -1
        edge_columns.append(tuple(column))
    require(rank(edge_columns) == 3,
            "colour-square edge boundary rank changed")
    direct = [-1, 0, 0, 1]
    path = [edge_columns[0][row] + edge_columns[3][row]
            for row in range(4)]
    require(path == direct, "two-step colour path changed")
    return {
        "corner_order": ["q00", "q10", "q01", "q11"],
        "corners": {key: list(value) for key, value in monomials.items()},
        "linear_coefficient_rank": 4,
        "colour_edge_boundary_rank": 3,
        "quadratic_relation": "q00*q11-q10*q01=0",
        "direct_q11_minus_q00_is_one_literal_same_word_row": False,
        "reason": (
            "the two-edge path passes through q10 or q01, whose decorated "
            "output/source word differs from both endpoints"
        ),
    }


def grade_gate():
    e14 = {
        "endpoint_p_degree": 1,
        "endpoint_s_degree": 1,
        "internal_q_degree": 2,
        "endpoint_orientation": "p1@0*s1@1 versus p1@1*s1@0",
        "tail_word": "1111",
        "target_word": "111111",
    }
    rootless = {
        "endpoint_p_degree": 0,
        "endpoint_s_degree": 0,
        "internal_q_degree": 2,
        "physical_word": "01211222",
        "zero_endpoint_chart_word": "00211200",
        "tail_word": "2112",
        "bar_boundary": "-Omega_1+q_(1,N)",
    }
    require((e14["endpoint_p_degree"], e14["endpoint_s_degree"])
            != (rootless["endpoint_p_degree"],
                rootless["endpoint_s_degree"]),
            "endpoint-use grades unexpectedly agree")
    return {
        "e14": e14,
        "rootless": rootless,
        "polynomial_multiplier_repairs_endpoint_grade": False,
        "polynomial_multiplier_repairs_source_word": False,
        "existing_endpoint_word_change_required": True,
    }


def sufficient_attachment_theorem():
    # Coordinate order: E+, E-, Omega, qcomp.
    S = (1, 1, 0, 0)
    B = (0, 0, -1, 1)
    A = (1, -1, 1, -1)
    D = tuple(A[index] + B[index] for index in range(4))
    require(D == (1, -1, 0, 0), "A+B stopped cancelling ridge/companion")
    require(rank([S, B]) == 2, "existing two-column rank changed")
    require(rank([S, B, A]) == 3, "attachment stopped increasing rank")
    plus = tuple(Q(S[index] + D[index], 2) for index in range(4))
    minus = tuple(Q(S[index] - D[index], 2) for index in range(4))
    require(plus == (1, 0, 0, 0) and minus == (0, 1, 0, 0),
            "endpoint orientations stopped being isolated")
    determinant = S[0] * D[1] - S[1] * D[0]
    require(determinant == -2, "integral endpoint index changed")
    return {
        "coordinate_order": ["E_plus", "E_minus", "Omega", "q_comp"],
        "existing_signless_endpoint_row_S": list(S),
        "existing_rootless_bar_B": list(B),
        "required_same_word_attachment_A": list(A),
        "derived_endpoint_difference_D=A+B": list(D),
        "endpoint_lattice_determinant": determinant,
        "after_inverting_2": {
            "E_plus=(S+D)/2": [str(value) for value in plus],
            "E_minus=(S-D)/2": [str(value) for value in minus],
        },
        "protected_readout_requirement": (
            "A must be one literal source-labelled row in the common fine "
            "word and have zero target, old-ores, anchor-incidence, and W"
        ),
        "present_inventory_contains_A": False,
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")
    ledger = {
        "theorem": "shared same-word endpoint/companion attachment gate",
        "uncoloured_and_decorated_relabelling": relabelling_gate(),
        "two_colour_segre_square": segre_square_gate(),
        "source_operation_grade": grade_gate(),
        "smallest_sufficient_attachment": sufficient_attachment_theorem(),
        "verdict": (
            "the rootless q_(1,N) and E14 endpoint cycle share an uncoloured "
            "two-edge matching, but no decorated/source-graded relabelling. "
            "Their common closure needs the new literal mixed boundary "
            "E_plus-E_minus+Omega-q_comp; the current rows supply only its "
            "signless endpoint and rootless-bar faces"
        ),
        "scope": (
            "one canonical E14 orientation pair and rootless face v=1, "
            "N=23|45; this is an exact attachment interface/no-existing-"
            "relabeling result, not an all-source no-go"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h3 shared endpoint/companion attachment gate: MISSING")
    print("uncoloured tail relabellings: 8")
    print("decorated/source-grade relabellings: 0")
    print("existing rows span signless endpoint + rootless bar only")
    print("minimal new boundary: E_plus-E_minus+Omega-q_comp")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()

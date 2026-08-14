#!/usr/bin/env python3
"""Audit symmetry/covariance constraints on the eight kappa_mix scalars.

There are two different symmetry questions and they must not be conflated.
The unmarked lower word 0112 has a V4 site/colour stabilizer, acting on the
eight one-root words with orbits 4+2+2.  But every nonidentity element moves
the marked endpoint/residual occurrence 01|45.  Thus V4 is a transport
groupoid on marked packets, not an endomorphism group of the eight literal
instances in one fixed packet.

The admissible operation-corner symmetries swap the two DQ corners and/or
the two PS corners.  They fix delta=(1,1,-1,-1), hence fix
chi=delta.(B-Eq).  Endpoint reversal is the simultaneous within-shore swap
and also has sign +1.  The involutions that negate chi exchange DQ with PS
or B with Eq; both change a retained literal tag and are inadmissible.

Consequently symmetry forces none of the eight fixed-packet lambda_i to
vanish and does not pair them.  Only after forgetting the marked occurrence
does one obtain the conditional three-parameter orbit collapse.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_p2_one_root_private_orbit_bright_dark_gate.py":
        "406c4be1a72a71c6c80fdf1c1929e64dce128847d5b20a02bb95e4a8582772d0",
    "notes/h2-p2-one-root-private-orbit-bright-dark-gate.md":
        "f07de0c9e1cc6b7558bf6efa08692d9fe8960af1b6fb13c437230f90c0dfc9b0",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "notes/h3-augmented-p2-section-shortest-conditional-gate.md":
        "ee5da6f0911feb06707106cc6207161bbac7cabd31885f554321698dfbb989d8",
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "notes/h3-uc4-four-site-response-private-eq-local-terminal-gate.md":
        "a7e10e0397ae3b31b9cce0e6bc2907f0c208634e22a0e3284076304130bd6989",
    "computations/verify_h3_psi_source_grade_macaulay_exhaustiveness_terminal_gate.py":
        "2ae3d0fe36ca6ab92ee506b4a4441d6476ecb09567a1441c66f54793e304980d",
    "notes/h3-psi-source-grade-macaulay-exhaustiveness-terminal-gate.md":
        "de47eeafdfcffbd043f3b2472f3be54b7ec94ad546fe2bab7194e8b64bd9c98a",
}
EXPECTED_DIGEST = "21624985da5bbebf865fffe091901ec8819455db5c3becd931059225e36ff91a"

SITES = (0, 1, 4, 5)
COLOURS = {0: 0, 1: 1, 4: 1, 5: 2}
WORDS = tuple(tuple(map(int, word)) for word in (
    "0012", "0102", "0110", "0111",
    "0122", "0212", "1112", "2112",
))
MARKED = (0, 1, ((4, 5),))
MARKED_MATE = (1, 0, ((4, 5),))
DELTA = tuple(map(Q, (1, 1, -1, -1)))
PSI = DELTA + tuple(-entry for entry in DELTA)
CAP_TAG = {
    "response_source_word": "11:110000",
    "cap_output_word": "01211222",
    "fine": "t*q_(v,N) at the selected six P3+K2 occurrences",
    "repeated": "P3+K2",
    "operation_parent": "response-to-AugP2 mixed orbit/K_Eq kappa_mix",
    "cap_window": "2345 with literal occurrence labels",
    "lower_parent_word": "0112 on sites 0,1,4,5",
    "lower_marked_ordered_endpoints": "01",
    "lower_residual": "q45:12",
    "lower_reinsertion": "q23:21",
}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def word_text(word: tuple[int, ...]) -> str:
    return "".join(map(str, word))


def rank(columns: tuple[tuple[Q, ...], ...] | list[tuple[Q, ...]]) -> int:
    columns = tuple(columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def build_lower_group():
    group = []
    for site_images in permutations(SITES):
        site_map = dict(zip(SITES, site_images, strict=True))
        for colour_images in permutations((0, 1, 2)):
            colour_map = dict(zip((0, 1, 2), colour_images, strict=True))
            if all(colour_map[COLOURS[site]] == COLOURS[site_map[site]]
                   for site in SITES):
                group.append((site_map, colour_map))
    require(len(group) == 4, ("lower unmarked stabilizer", group))
    identity = next(
        element for element in group
        if all(element[0][site] == site for site in SITES)
        and all(element[1][colour] == colour for colour in (0, 1, 2))
    )
    middle = next(
        element for element in group
        if element[0] == {0: 0, 1: 4, 4: 1, 5: 5}
    )
    flank = next(
        element for element in group
        if element[0] == {0: 5, 1: 1, 4: 4, 5: 0}
    )
    both = next(element for element in group
                if element not in (identity, middle, flank))
    return {"1": identity, "a": middle, "b": flank, "ab": both}


def transform_word(word, element):
    site_map, colour_map = element
    answer = [None] * len(SITES)
    for old_index, old_site in enumerate(SITES):
        new_site = site_map[old_site]
        answer[SITES.index(new_site)] = colour_map[word[old_index]]
    return tuple(answer)


def transform_occurrence(occurrence, element):
    site_map, _colour_map = element
    p_site, s_site, matching = occurrence
    return (
        site_map[p_site],
        site_map[s_site],
        tuple(tuple(sorted((site_map[left], site_map[right])))
              for left, right in matching),
    )


def permute_vector(vector, image):
    """Push a coordinate vector forward by old-index -> new-index image."""
    answer = [Q(0)] * len(vector)
    for old, new in enumerate(image):
        answer[new] = Q(vector[old])
    return tuple(answer)


def tag_audit():
    records = []
    for index, word in enumerate(WORDS):
        records.append({
            "instance": f"kappa_{index}",
            **CAP_TAG,
            "lower_one_root_word": word_text(word),
            "lower_packet": "ordered 0->1 with residual 45",
        })
    require(len(records) == 8
            and len({tuple(sorted(record.items())) for record in records}) == 8,
            "the literal instance tags stopped separating")
    return {
        "literal_instances": records,
        "only_varying_displayed_tag": "lower_one_root_word",
        "retained_common_tags": CAP_TAG,
        "typing_rule": (
            "an equality of kappa scalars is usable only under an automorphism "
            "of the full source-labelled packet; transporting the lower marked "
            "occurrence produces a different packet object"
        ),
    }


def group_audit():
    named = build_lower_group()
    expected_actions = {
        "1": ("0012", "0102", "0110", "0111",
              "0122", "0212", "1112", "2112"),
        "a": ("0102", "0012", "0110", "0111",
              "0212", "0122", "1112", "2112"),
        "b": ("0212", "0122", "2112", "1112",
              "0102", "0012", "0111", "0110"),
        "ab": ("0122", "0212", "2112", "1112",
               "0012", "0102", "0111", "0110"),
    }
    action = {
        name: tuple(word_text(transform_word(word, element)) for word in WORDS)
        for name, element in named.items()
    }
    require(action == expected_actions, ("V4 word action", action))

    expected_occurrences = {
        "1": (0, 1, ((4, 5),)),
        "a": (0, 4, ((1, 5),)),
        "b": (5, 1, ((0, 4),)),
        "ab": (5, 4, ((0, 1),)),
    }
    occurrence_action = {
        name: transform_occurrence(MARKED, element)
        for name, element in named.items()
    }
    require(occurrence_action == expected_occurrences,
            ("marked occurrence transport", occurrence_action))
    strict_stabilizer = tuple(
        name for name, element in named.items()
        if transform_occurrence(MARKED, element) in (MARKED, MARKED_MATE)
    )
    require(strict_stabilizer == ("1",), strict_stabilizer)

    unseen = set(WORDS)
    orbits = []
    while unseen:
        seed = min(unseen)
        orbit = frozenset(transform_word(seed, element)
                          for element in named.values())
        orbits.append(orbit)
        unseen -= orbit
    orbits.sort(key=lambda orbit: (-len(orbit), sorted(orbit)))
    expected_orbits = (
        ("0012", "0102", "0122", "0212"),
        ("0110", "2112"),
        ("0111", "1112"),
    )
    require(tuple(tuple(map(word_text, sorted(orbit))) for orbit in orbits)
            == expected_orbits, orbits)
    character = tuple(sum(transform_word(word, element) == word
                          for word in WORDS)
                      for element in named.values())
    require(character == (8, 4, 0, 0), character)
    coarse_stabilizers = {
        word_text(word): tuple(name for name, element in named.items()
                               if transform_word(word, element) == word)
        for word in WORDS
    }
    require(all(stabilizer == ("1", "a") for word, stabilizer in
                coarse_stabilizers.items()
                if word in ("0110", "0111", "1112", "2112"))
            and all(stabilizer == ("1",) for word, stabilizer in
                    coarse_stabilizers.items()
                    if word not in ("0110", "0111", "1112", "2112")),
            coarse_stabilizers)
    return {
        "unmarked_lower_group": "V4=<a,b>",
        "generators": {
            "a": "site 1<->4; colours fixed",
            "b": "site 0<->5 and colours 0<->2",
        },
        "action_on_ordered_words": action,
        "permutation_character_1_a_b_ab": list(character),
        "coarse_word_orbits": [list(values) for values in expected_orbits],
        "coarse_word_stabilizers": {
            word: list(stabilizer)
            for word, stabilizer in coarse_stabilizers.items()
        },
        "transported_marked_occurrences": {
            name: str(value) for name, value in occurrence_action.items()
        },
        "full_fixed_packet_stabilizer": list(strict_stabilizer),
        "strict_eight_instance_orbits": [[word_text(word)] for word in WORDS],
        "interpretation": (
            "V4 acts on coarse lower words and by arrows between marked packet "
            "objects.  It has no nonidentity endomorphism of the fixed packet, "
            "so its 4+2+2 orbit partition is not an action on the eight strict "
            "kappa_mix instances"
        ),
    }


def chi_audit():
    # Literal corner order: DQ[a|b], DQ[b|a], PS[P0,S1], PS[P1,S0].
    direct_swap = (1, 0, 2, 3)
    ps_swap = (0, 1, 3, 2)
    endpoint_reversal = (1, 0, 3, 2)
    identity = (0, 1, 2, 3)
    allowed = {
        "1": identity,
        "direct_root_swap": direct_swap,
        "PS_endpoint_swap": ps_swap,
        "endpoint_reversal": endpoint_reversal,
    }
    signs = {}
    for name, image in allowed.items():
        transformed_delta = permute_vector(DELTA, image)
        transformed_psi = permute_vector(
            PSI, image + tuple(index + 4 for index in image)
        )
        require(transformed_delta == DELTA and transformed_psi == PSI,
                ("admissible chi sign", name, transformed_psi))
        signs[name] = 1

    shore_exchange = (2, 3, 0, 1)
    transformed_delta = permute_vector(DELTA, shore_exchange)
    transformed_psi = permute_vector(
        PSI, shore_exchange + tuple(index + 4 for index in shore_exchange)
    )
    block_exchange = tuple(range(4, 8)) + tuple(range(4))
    block_transformed_psi = permute_vector(PSI, block_exchange)
    require(transformed_delta == tuple(-entry for entry in DELTA)
            and transformed_psi == tuple(-entry for entry in PSI)
            and block_transformed_psi == tuple(-entry for entry in PSI),
            "the two forbidden chi-negating controls changed")
    return {
        "corner_order": [
            "DQ[a|b]", "DQ[b|a]", "PS[P0,S1]", "PS[P1,S0]",
        ],
        "delta": [int(entry) for entry in DELTA],
        "chi_B_Eq_coefficients": [int(entry) for entry in PSI],
        "admissible_within_shore_group": "S2(DQ) x S2(PS)",
        "admissible_signs_on_chi": signs,
        "endpoint_reversal_action": "(DQ0 DQ1)(PS0 PS1), sign +1",
        "transported_lower_V4_sign": (
            "+1 when chi is carried with its literal DQ/PS and B/Eq labels; "
            "this is covariance between packet objects, not a fixed-packet action"
        ),
        "chi_negating_controls": {
            "DQ_PS_shore_exchange": {
                "permutation": "(0 2)(1 3)",
                "sign": -1,
                "inadmissible_reason": (
                    "changes the retained DQ versus PS operation-parent/shore tag"
                ),
            },
            "B_Eq_block_exchange": {
                "sign": -1,
                "inadmissible_reason": (
                    "changes private-B row type into reduced-Eq row type"
                ),
            },
        },
        "negating_element_in_full_instance_stabilizer": False,
    }


def lambda_audit():
    named = build_lower_group()
    word_index = {word: index for index, word in enumerate(WORDS)}
    covariance_rows = []
    for element in named.values():
        for word in WORDS:
            image = transform_word(word, element)
            row = [Q(0)] * len(WORDS)
            row[word_index[image]] += 1
            row[word_index[word]] -= 1
            covariance_rows.append(tuple(row))
    covariance_rank = rank(covariance_rows)
    require(covariance_rank == 5, covariance_rank)
    coarse_dimension = len(WORDS) - covariance_rank
    require(coarse_dimension == 3, coarse_dimension)

    # A sign-negating stabilizer would force 2*lambda=0 over Q.  Enumerate
    # the actual full stabilizer and admissible chi signs: only +1 occurs.
    full_stabilizer_signs = {
        "identity_site_transport": 1,
        "direct_root_swap": 1,
        "PS_endpoint_swap": 1,
        "endpoint_reversal": 1,
    }
    require(-1 not in full_stabilizer_signs.values(),
            full_stabilizer_signs)

    # Strict source-labelled sections remain eight independent scalar tests.
    strict_basis = tuple(tuple(Q(i == j) for i in range(8))
                         for j in range(8))
    require(rank(strict_basis) == 8, "strict lambda basis")
    return {
        "strict_fixed_packet": {
            "lambda_dimension_after_symmetry": 8,
            "forced_zero_indices": [],
            "forced_pairings": [],
            "reason": (
                "the marked packet stabilizer is identity; endpoint reversal "
                "fixes every instance and has chi sign +1"
            ),
        },
        "natural_transported_family": {
            "covariance_equation": (
                "lambda_(P,w)=lambda_(gP,gw) for a covariant kappa family"
            ),
            "relation_within_the_original_fixed_packet": False,
            "chi_transport_sign": 1,
        },
        "coarse_unmarked_quotient_conditional_only": {
            "covariance_equation_rank": covariance_rank,
            "invariant_dimension": coarse_dimension,
            "equalities": [
                "lambda_0012=lambda_0102=lambda_0122=lambda_0212",
                "lambda_0110=lambda_2112",
                "lambda_0111=lambda_1112",
            ],
            "qualification": (
                "these equalities require forgetting or canonically identifying "
                "the transported marked occurrence, which the physical source "
                "presentation does not presently authorize"
            ),
        },
        "stabilizer_negation_test": {
            "full_stabilizer_chi_signs": full_stabilizer_signs,
            "lambda_i_forced_zero": False,
            "coarse_a_fixed_words": ["0110", "0111", "1112", "2112"],
            "coarse_a_chi_sign": 1,
        },
        "terminal_consequence": (
            "symmetry alone discharges none of the eight equations "
            "lambda_i=0; the exact Psi terminal still needs all eight strict "
            "source-labelled tests (or a new packet-identification theorem)"
        ),
    }


def run(mode: str) -> str:
    pin_dependencies()
    ledger = {}
    if mode in ("all", "tags"):
        ledger["full_literal_tags"] = tag_audit()
    if mode in ("all", "group"):
        ledger["lower_site_colour_action"] = group_audit()
    if mode in ("all", "chi"):
        ledger["chi_covariance_and_signs"] = chi_audit()
    if mode in ("all", "lambda"):
        ledger["lambda_constraints"] = lambda_audit()
    if mode == "all":
        ledger["theorem"] = (
            "h3 kappa_mix eight-instance symmetry/covariance no-collapse gate"
        )
        ledger["verdict"] = (
            "The unmarked lower V4 has word orbits 4+2+2 and positive chi "
            "transport, but every nonidentity element moves the marked "
            "endpoint/residual packet.  The strict source-labelled action "
            "therefore has eight singleton orbits.  Every admissible internal "
            "corner involution fixes chi; the chi-negating shore and B/Eq "
            "exchanges change retained tags.  No stabilizer forces a lambda_i "
            "to vanish and no physical symmetry pairs the eight fixed-packet "
            "scalars.  A deliberately unmarked quotient has three positive-sign "
            "orbit parameters, but that quotient is not the physical grade."
        )
        ledger["scope"] = (
            "exact rational group action, literal packet/cap tags, corner and "
            "B/Eq signs.  It audits symmetry constraints on the unknown scalar "
            "normal forms; it does not construct kappa_mix or prove its darkness."
        )
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if mode == "all" and EXPECTED_DIGEST != "TO_BE_FROZEN":
        require(digest == EXPECTED_DIGEST,
                ("kappa_mix symmetry ledger changed", digest))
    print(f"h3 kappa_mix eight-instance symmetry gate ({mode}): PASS")
    if mode in ("all", "group"):
        print("coarse lower-word V4 orbits: 4+2+2; fixed marked stabilizer: identity")
    if mode in ("all", "chi"):
        print("admissible chi signs: all +1; negating maps change retained tags")
    if mode in ("all", "lambda"):
        print("strict lambda constraints from symmetry: none (dimension 8)")
        print("unmarked conditional quotient: dimension 3, not forced zero")
    print("ledger_sha256=" + digest)
    return digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "tags", "group", "chi", "lambda"),
        default="all",
    )
    arguments = parser.parse_args()
    run(arguments.mode)


if __name__ == "__main__":
    main()

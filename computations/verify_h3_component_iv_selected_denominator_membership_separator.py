#!/usr/bin/env python3
"""Exact coordinate separator for the five Component-IV memberships.

For m=12112, the m-word coordinate of the denominator column

    b(d_(v,m_v)) = e_(m_v)^(v) q^[2]

is the three-term deleted-face hafnian h_v.  The same coordinate is
identically zero on all ten unselected columns.  Consequently the physical
membership b(d_(v,m_v)) in im(b_oth) forces h_v=0 after every base change.

This checker proves that symbolic statement, its site-equivariance, and the
sharp converse counterguards.  It does not assert that h_v=0 is sufficient
or that the full-source quotient is nonzero.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path

import verify_h3_denominator_tor_transgression_fitting_gate as TRANS


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DIGEST = "ad428d2499c5df769a3f63b80436a588805c692ab27a0291554e9920757764b5"
PINS = {
    "computations/verify_h3_component_iv_reduced_companion_tor_gate.py":
        "5bf7e0960b413c4e5d587b3c8f46d51493010bb73413682d7705bb28070d0935",
    "computations/verify_h3_denominator_tor_transgression_fitting_gate.py":
        "33cd6ac3de85f83ee16189601930938d73f35f2fef5db20253380801bdd78459",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))


def edge_cell(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return left, right, left_colour, right_colour


def deleted_face_hafnian(site, word):
    """Return the three generic monomials in Haf(q|_(D minus site))."""
    remaining = tuple(vertex for vertex in TRANS.SITES if vertex != site)
    monomials = []
    for matching in TRANS.matchings(remaining):
        monomial = tuple(sorted(
            edge_cell(left, right, word[left - 1], word[right - 1])
            for left, right in matching
        ))
        monomials.append(monomial)
    return tuple(sorted(monomials))


def word_coefficient(label, word):
    """Symbolic word coefficient of one universal denominator column."""
    site, colour = label
    if word[site - 1] != colour:
        return ()
    return deleted_face_hafnian(site, word)


def symbolic_separator():
    word = TRANS.MIXED
    selected = set(TRANS.SELECTED)
    faces = {}
    for site, label in zip(TRANS.SITES, TRANS.SELECTED):
        support = word_coefficient(label, word)
        require(len(support) == 3, ("deleted-face hafnian changed", site, support))
        faces[site] = support

    unselected = tuple(label for label in TRANS.LABELS if label not in selected)
    require(len(unselected) == 10, "unselected column count changed")
    require(all(word_coefficient(label, word) == () for label in unselected),
            "an unselected column acquired the selected word")

    # A generic two-edge matching monomial determines its four occupied
    # vertices, hence its deleted face.  The five supports are disjoint.
    flat = [monomial for support in faces.values() for monomial in support]
    require(len(set(flat)) == 15, "two deleted faces share a generic monomial")
    return {
        "word": "".join(map(str, word)),
        "selected_columns": [f"d_({site},{colour})"
                             for site, colour in TRANS.SELECTED],
        "unselected_columns": len(unselected),
        "selected_word_coordinate_on_b_oth": "identically zero",
        "selected_word_coordinate_on_face_v": {
            str(site): [
                [f"q_{left}{right}^{left_colour}{right_colour}"
                 for left, right, left_colour, right_colour in monomial]
                for monomial in support
            ]
            for site, support in faces.items()
        },
        "face_support_sizes": [len(faces[site]) for site in TRANS.SITES],
        "pairwise_disjoint_face_monomials": True,
        "ring_consequence": (
            "b(d_(v,m_v)) in im(b_oth) over S implies h_v=0 in S"
        ),
        "localized_consequence": (
            "over S[h_v^-1], membership is impossible unless 1=0"
        ),
        "five_face_consequence": (
            "surjectivity of tau forces h_1=h_2=h_3=h_4=h_5=0"
        ),
    }


def permute_word(word, permutation):
    answer = [None] * len(word)
    for old, new in zip(TRANS.SITES, permutation):
        answer[new - 1] = word[old - 1]
    return tuple(answer)


def permute_monomial(monomial, permutation):
    image = dict(zip(TRANS.SITES, permutation))
    return tuple(sorted(
        edge_cell(image[left], image[right], left_colour, right_colour)
        for left, right, left_colour, right_colour in monomial
    ))


def symmetry_audit():
    word = TRANS.MIXED
    checked = 0
    stabilizer = []
    for permutation in permutations(TRANS.SITES):
        transported_word = permute_word(word, permutation)
        if transported_word == word:
            stabilizer.append(permutation)
        image = dict(zip(TRANS.SITES, permutation))
        for site in TRANS.SITES:
            transported_support = tuple(sorted(
                permute_monomial(monomial, permutation)
                for monomial in deleted_face_hafnian(site, word)
            ))
            require(
                transported_support
                == deleted_face_hafnian(image[site], transported_word),
                ("site transport changed the face hafnian", permutation, site),
            )
            checked += 1

    require(len(stabilizer) == 12, "fixed-word stabilizer changed")
    orbits = []
    unseen = set(TRANS.SITES)
    while unseen:
        seed = min(unseen)
        orbit = sorted({dict(zip(TRANS.SITES, permutation))[seed]
                        for permutation in stabilizer})
        orbits.append(orbit)
        unseen.difference_update(orbit)
    require(orbits == [[1, 3, 4], [2, 5]], ("stabilizer orbits changed", orbits))
    return {
        "site_permutations_checked": 120,
        "face_transports_checked": checked,
        "equivariance": "epsilon_(pi m) b(d_(pi v,(pi m)_(pi v)))=pi(h_v)",
        "fixed_word_stabilizer_order": len(stabilizer),
        "fixed_word_face_orbits": orbits,
        "interpretation": (
            "the family is S5-equivariant; at the fixed word 12112 there "
            "are two stabilizer orbits, but the same coordinate proof "
            "applies literally to every face"
        ),
    }


def converse_counterguards():
    direct_free = TRANS.packet_audit("direct_free")
    tilted = TRANS.packet_audit("tilted")
    require(direct_free["h_values"] == ["0"] * 5
            and tilted["h_values"] == ["0"] * 5,
            "the scalar-zero counterguards changed")
    require(direct_free["individual_classes_hit"]
            == [True, False, True, False, False]
            and tilted["individual_classes_hit"]
            == [True, False, True, False, False],
            "individual membership counterguards changed")
    return {
        "warning": "these rational packets are not full-source points",
        "direct_free": {
            "h_values": direct_free["h_values"],
            "individual_memberships": direct_free["individual_classes_hit"],
            "transgression_rank": direct_free["transgression_rank"],
            "primitive_cokernel_covector": direct_free["cokernel_covectors"],
        },
        "tilted": {
            "h_values": tilted["h_values"],
            "individual_memberships": tilted["individual_classes_hit"],
            "transgression_rank": tilted["transgression_rank"],
            "primitive_cokernel_covectors": tilted["cokernel_covectors"],
        },
        "converse": "h_1=...=h_5=0 does not imply the five memberships",
    }


def main():
    pin_dependencies()
    ledger = {
        "scope": "h=3 selected denominator-column memberships",
        "exact_coordinate_separator": symbolic_separator(),
        "symmetry": symmetry_audit(),
        "sharp_converse_counterguards": converse_counterguards(),
        "verdict": {
            "membership_decided_on_nonzero_face_charts": "NO",
            "all_five_memberships_force_scalar_zero_locus": True,
            "memberships_decided_on_full_scalar_zero_source_locus": False,
            "remaining_ring": (
                "((R/J_full-nine)[kappa^-1])/(h_1,...,h_5)"
            ),
            "not_claimed": (
                "existence or nonexistence of a nonzero full-source point "
                "on the remaining scalar-zero locus"
            ),
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, ("ledger changed", digest))

    print("h=3 selected denominator membership separator: PASS")
    print("epsilon_12112(b_oth)=0 and epsilon_12112(b_sel,v)=h_v for all five faces")
    print("membership on an h_v-nonzero chart: impossible unless the source quotient is zero")
    print("all h_v=0: necessary, not sufficient (packet ranks 4 and 3)")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()

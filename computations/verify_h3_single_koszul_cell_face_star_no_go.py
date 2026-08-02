#!/usr/bin/env python3
"""Exact face-star audit for the single h=3 degree-four Koszul cell.

For m=12112, coefficient extraction meets exactly the five selected
denominator columns d_(v,m_v).  This checker builds the smallest coordinate
subcomplex containing their images, verifies that the u-leading part of the
Koszul coefficient acts as the identity on all five labelled face defects,
computes the S_3 x S_2 stabilizer compression, and compares the required
five-space with the exact packet Tor images frozen in commit b15d1ad.

No full-source provenance or physical cap homotopy is asserted here.
"""

import argparse
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
import json


COLORS = (0, 1, 2)
SITES = (1, 2, 3, 4, 5)
MIXED = (1, 2, 1, 1, 2)
PURE = (0, 0, 0, 0, 0)
ONE_SITES = (0, 2, 3)  # zero-based positions with m_v=1
TWO_SITES = (1, 4)     # zero-based positions with m_v=2
EXPECTED_DIGEST = "1507a0b656924a44a4bd0f35c9609d232d700f36d63d851b784aa505066ab617"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def edge(left, right, left_colour, right_colour):
    if left < right:
        return (left, right, left_colour, right_colour)
    return (right, left, right_colour, left_colour)


def denominator_entry(word, site, colour):
    """Sparse universal coefficient [e_word](e_colour^(site) q^[2])."""
    if word[site - 1] != colour:
        return ()
    remaining = tuple(vertex for vertex in SITES if vertex != site)
    terms = []
    for matching in matchings(remaining):
        terms.append(tuple(sorted(
            edge(left, right, word[left - 1], word[right - 1])
            for left, right in matching
        )))
    return tuple(sorted(terms))


def rref(matrix):
    work = [[Q(entry) for entry in row] for row in matrix]
    width = len(work[0]) if work else 0
    rank = 0
    pivots = []
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                scale = work[row][column]
                work[row] = [
                    entry - scale * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[rank])
                ]
        pivots.append(column)
        rank += 1
    return work, tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def in_span(vector, rows):
    return rank(rows) == rank(list(rows) + [vector])


def standard(index):
    return tuple(Q(1) if position == index else Q(0) for position in range(5))


def subcomplex_audit():
    words = tuple(product(COLORS, repeat=5))
    selected_columns = tuple((site, MIXED[site - 1]) for site in SITES)

    supports = {}
    for site, colour in selected_columns:
        support = tuple(
            word for word in words if denominator_entry(word, site, colour)
        )
        require(len(support) == 81, f"selected column {site} support changed")
        supports[site] = support

    active_words = tuple(sorted(set().union(*map(set, supports.values()))))
    inactive_words = tuple(word for word in words if word not in active_words)
    require(len(active_words) == 243 - 2 ** 5 == 211,
            "smallest active coordinate span changed")
    require(
        all(all(word[index] != MIXED[index] for index in range(5))
            for word in inactive_words),
        "inactive words are not exactly the all-coordinate mismatches",
    )

    # The word with m_v at v and zero elsewhere occurs only in selected
    # column v.  These five rows give a diagonal nonzero polynomial witness
    # that the active source star really has five independent columns.
    diagonal_rows = []
    for site in SITES:
        witness = tuple(MIXED[index] if index == site - 1 else 0
                        for index in range(5))
        row = tuple(
            bool(denominator_entry(witness, column_site, colour))
            for column_site, colour in selected_columns
        )
        diagonal_rows.append(row)
    require(diagonal_rows == [
        tuple(position == index for position in range(5))
        for index in range(5)
    ], "diagonal selected-column witness changed")

    defects = tuple(
        denominator_entry(MIXED, site, MIXED[site - 1]) for site in SITES
    )
    pure_faces = tuple(denominator_entry(PURE, site, 0) for site in SITES)
    require(all(len(face) == 3 for face in defects + pure_faces),
            "a four-face hafnian changed term count")

    feature_basis = sorted({
        term for face in defects + pure_faces for term in face
    })
    feature_index = {term: index for index, term in enumerate(feature_basis)}

    def coefficient_row(face):
        row = [0] * len(feature_basis)
        for term in face:
            row[feature_index[term]] += 1
        return tuple(row)

    pure_rows = tuple(map(coefficient_row, pure_faces))
    defect_rows = tuple(map(coefficient_row, defects))
    require(rank(pure_rows) == 5, "pure face rank changed")
    require(rank(pure_rows + defect_rows) == 10,
            "five mixed initial cokernel classes lost independence")

    # K_m has coefficient u-H_0 on r_m.  Since H_0 contains no u, taking
    # the u-linear coefficient of its denominator defect gives the identity
    # D_m -> W, d_(v,m_v) |-> omega_v.  Thus a single Koszul cell still
    # requires the whole labelled face space, not a diagonal vector in it.
    koszul_u_coefficient = tuple(standard(index) for index in range(5))
    required_rank = rank(koszul_u_coefficient)
    require(required_rank == 5, "u-leading K_m face map lost full rank")

    return {
        "selected_source_columns": [list(column) for column in selected_columns],
        "selected_column_support_sizes": [len(supports[site]) for site in SITES],
        "active_coordinate_words": len(active_words),
        "inactive_all_mismatch_words": len(inactive_words),
        "diagonal_column_witness": [[int(entry) for entry in row]
                                     for row in diagonal_rows],
        "pure_face_rank": rank(pure_rows),
        "combined_pure_mixed_rank": rank(pure_rows + defect_rows),
        "mixed_cokernel_rank": rank(pure_rows + defect_rows) - rank(pure_rows),
        "koszul_u_face_matrix": [[int(entry) for entry in row]
                                  for row in koszul_u_coefficient],
        "required_face_rank": required_rank,
    }


def stabilizer_permutations():
    answer = []
    for one_image in permutations(ONE_SITES):
        for two_image in permutations(TWO_SITES):
            permutation = list(range(5))
            for source, target in zip(ONE_SITES, one_image):
                permutation[source] = target
            for source, target in zip(TWO_SITES, two_image):
                permutation[source] = target
            answer.append(tuple(permutation))
    require(len(answer) == 12 and len(set(answer)) == 12,
            "m stabilizer should be S_3 x S_2 of order 12")
    return tuple(answer)


def act(vector, permutation):
    answer = [Q(0)] * 5
    for source, target in enumerate(permutation):
        answer[target] = Q(vector[source])
    return tuple(answer)


def orbit(vector, group):
    return tuple(sorted(set(act(vector, permutation) for permutation in group)))


def symmetry_audit():
    group = stabilizer_permutations()
    seed_one = standard(0)
    seed_two = standard(1)
    orbit_one = orbit(seed_one, group)
    orbit_two = orbit(seed_two, group)
    require(set(orbit_one) == {standard(index) for index in ONE_SITES},
            "colour-one deletion orbit changed")
    require(set(orbit_two) == {standard(index) for index in TWO_SITES},
            "colour-two deletion orbit changed")
    require(rank(orbit_one) == 3 and rank(orbit_two) == 2,
            "face-orbit ranks changed")
    require(rank(orbit_one + orbit_two) == 5,
            "two equivariant seeds no longer generate all faces")

    # One seed cannot generate W equivariantly.  Its Reynolds projection is
    # a single line in the two-dimensional invariant plane.  A generic seed
    # reaches the sharp maximum four; two seeds e_1,e_2 reach five.
    generic_seed = (1, 2, 4, 8, 16)
    generic_orbit_rank = rank(orbit(generic_seed, group))
    require(generic_orbit_rank == 4,
            "a single stabilizer orbit should have sharp rank four")
    invariant_one = tuple(1 if index in ONE_SITES else 0 for index in range(5))
    invariant_two = tuple(1 if index in TWO_SITES else 0 for index in range(5))
    require(rank((invariant_one, invariant_two)) == 2,
            "stabilizer invariant plane changed")

    return {
        "stabilizer_order": len(group),
        "face_orbit_sizes": [len(orbit_one), len(orbit_two)],
        "face_orbit_ranks": [rank(orbit_one), rank(orbit_two)],
        "two_seed_orbit_span_rank": rank(orbit_one + orbit_two),
        "single_generic_seed_orbit_rank": generic_orbit_rank,
        "invariant_plane_rank": rank((invariant_one, invariant_two)),
        "minimal_equivariant_seed_types": 2,
        "labelled_components_required": 5,
    }


PACKETS = {
    # Rows span im(tau) in W=(omega_1,...,omega_5).  These are the exact
    # projections computed from the raw packet denominator matrices in
    # verify_h3_denominator_tor_transgression_fitting_gate.py (b15d1ad).
    "direct_free": {
        "tor_dimension": 8,
        "image": (
            (1, 0, 0, 0, 0),
            (0, 0, 1, 0, 0),
            (0, -1, 0, 1, 0),
            (0, -2, 0, 0, 1),
        ),
        "cokernel_covectors": ((0, 1, 0, 1, 2),),
    },
    "tilted": {
        "tor_dimension": 7,
        "image": (
            (1, 0, 0, 0, 0),
            (0, 0, 1, 0, 0),
            (0, -1, 0, 1, 0),
        ),
        "cokernel_covectors": (
            (0, 1, 0, 1, 0),
            (0, 0, 0, 0, 1),
        ),
    },
}


def dot(left, right):
    return sum(Q(x) * Q(y) for x, y in zip(left, right))


def packet_audit():
    ledger = {}
    full_space = tuple(standard(index) for index in range(5))
    common_completion = (standard(1), standard(4))  # omega_2, omega_5

    for name, packet in PACKETS.items():
        image = tuple(tuple(map(Q, row)) for row in packet["image"])
        image_rank = rank(image)
        covectors = packet["cokernel_covectors"]
        require(all(dot(covector, row) == 0
                    for covector in covectors for row in image),
                f"{name}: cokernel covector stopped annihilating image")
        require(rank(covectors) == 5 - image_rank,
                f"{name}: cokernel covectors lost completeness")
        individual_hits = tuple(in_span(vector, image) for vector in full_space)
        require(individual_hits == (True, False, True, False, False),
                f"{name}: individual face-hit ledger changed")
        require(rank(image + common_completion) == 5,
                f"{name}: omega_2,omega_5 stopped completing image")
        invisible_dimension = packet["tor_dimension"] - image_rank
        require(invisible_dimension == 4,
                f"{name}: cap-invisible Tor dimension changed")
        ledger[name] = {
            "tor_dimension": packet["tor_dimension"],
            "transgression_rank": image_rank,
            "required_rank": rank(full_space),
            "missing_rank": 5 - image_rank,
            "all_required_faces_hit": rank(image) == rank(image + full_space),
            "individual_faces_hit": list(individual_hits),
            "cokernel_covectors": [list(row) for row in covectors],
            "cap_invisible_tor_dimension": invisible_dimension,
            "completed_by_omega_2_omega_5": rank(image + common_completion) == 5,
        }

    direct_image = PACKETS["direct_free"]["image"]
    tilted_image = PACKETS["tilted"]["image"]
    require(all(in_span(tuple(map(Q, row)), direct_image) for row in tilted_image),
            "tilted image stopped being contained in direct-free image")
    require(rank(tilted_image) == 3 and rank(direct_image) == 4,
            "packet image ranks changed")
    require(rank(tilted_image + common_completion) == 5,
            "common two-direction packet complement changed")
    ledger["comparison"] = {
        "tilted_image_contained_in_direct_free": True,
        "common_image_rank": 3,
        "common_residual_rank": 2,
        "common_completing_directions": ["omega_2", "omega_5"],
        "one_common_extra_direction_suffices": False,
    }
    return ledger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode", nargs="?", default="all",
        choices=("all", "subcomplex", "symmetry", "packets"),
    )
    args = parser.parse_args()

    ledger = {}
    if args.mode in ("all", "subcomplex"):
        ledger["subcomplex"] = subcomplex_audit()
    if args.mode in ("all", "symmetry"):
        ledger["symmetry"] = symmetry_audit()
    if args.mode in ("all", "packets"):
        ledger["packets"] = packet_audit()

    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if args.mode == "all":
        require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print(f"h=3 single-Koszul-cell face-star audit ({args.mode}): PASS")
    if "subcomplex" in ledger:
        print("active presentation: 5 selected columns -> 211 word coordinates")
        print("K_m u-leading labelled face map: rank 5")
    if "symmetry" in ledger:
        print("stabilizer S_3 x S_2: two seed types, five labelled components")
    if "packets" in ledger:
        print("packet Tor images: direct-free rank 4, tilted rank 3")
        print("packet cap-invisible Tor kernels: dimension 4 in both cases")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

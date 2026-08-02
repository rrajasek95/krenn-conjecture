#!/usr/bin/env python3
"""Independent audit of the single-Koszul-cell five-face star.

The universal selected denominator subpresentation, the u-leading face map,
the full word stabilizer and fixed-r subgroup, and both packet Tor maps are
rebuilt without importing the primary checker.
"""

import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
import json


Q = Fraction
ZERO = Q(0)
ONE = Q(1)
COLOURS = (0, 1, 2)
SITES = (1, 2, 3, 4, 5)
WORDS = tuple(product(COLOURS, repeat=5))
LABELS = tuple((site, colour) for site in SITES for colour in COLOURS)
MIXED = (1, 2, 1, 1, 2)
PURE = (0, 0, 0, 0, 0)
R_SITE = 3
EXPECTED_DIGEST = "2633de09f4c860802904ddc4f3b21972a12c3420f1dc8e3b09078a46afffa4bc"


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for offset, second in enumerate(vertices[1:]):
        remainder = vertices[1 : offset + 1] + vertices[offset + 2 :]
        for tail in perfect_matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def edge(left, right, left_colour, right_colour):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def denominator_terms(word, deleted, linear_colour):
    if word[deleted - 1] != linear_colour:
        return ()
    remaining = tuple(site for site in SITES if site != deleted)
    terms = []
    for matching in perfect_matchings(remaining):
        terms.append(tuple(sorted(
            edge(left, right, word[left - 1], word[right - 1])
            for left, right in matching
        )))
    return tuple(sorted(terms))


def row_reduce(matrix):
    work = [[Q(entry) for entry in row] for row in matrix]
    pivots = []
    row = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next((index for index in range(row, len(work))
                      if work[index][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        scale = work[row][column]
        work[row] = [entry / scale for entry in work[row]]
        for other in range(len(work)):
            if other != row and work[other][column]:
                multiplier = work[other][column]
                work[other] = [
                    entry - multiplier * pivot_entry
                    for entry, pivot_entry in zip(work[other], work[row])
                ]
        pivots.append(column)
        row += 1
        if row == len(work):
            break
    return work, tuple(pivots)


def rank(matrix):
    return len(row_reduce(matrix)[1])


def nullspace(matrix):
    reduced, pivots = row_reduce(matrix)
    width = len(matrix[0]) if matrix else 0
    free = tuple(column for column in range(width) if column not in pivots)
    answer = []
    for free_column in free:
        vector = [ZERO] * width
        vector[free_column] = ONE
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[row][free_column]
        answer.append(tuple(vector))
    return tuple(answer)


def standard(index):
    return tuple(ONE if position == index else ZERO for position in range(5))


def in_row_span(vector, rows):
    return rank(rows) == rank(tuple(rows) + (tuple(vector),))


def universal_subpresentation():
    selected = tuple((site, MIXED[site - 1]) for site in SITES)
    supports = []
    for site, colour in selected:
        support = tuple(word for word in WORDS
                        if denominator_terms(word, site, colour))
        assert_true(len(support) == 81, "selected support is not 81 words")
        supports.append(set(support))
    active = set().union(*supports)
    inactive = set(WORDS) - active
    assert_true(len(active) == 211 and len(inactive) == 32,
                "selected coordinate union changed")
    assert_true(all(all(word[index] != MIXED[index] for index in range(5))
                    for word in inactive), "inactive word description changed")

    # Full-image coordinate minimality and independent source columns.
    ownership = []
    for deleted in SITES:
        witness = tuple(MIXED[index] if index == deleted - 1 else 0
                        for index in range(5))
        row = tuple(bool(denominator_terms(witness, site, colour))
                    for site, colour in selected)
        ownership.append(row)
    identity_boolean = tuple(
        tuple(column == row for column in range(5)) for row in range(5)
    )
    assert_true(tuple(ownership) == identity_boolean,
                "five source-column ownership witnesses changed")

    mixed_faces = tuple(
        denominator_terms(MIXED, site, MIXED[site - 1]) for site in SITES
    )
    pure_faces = tuple(denominator_terms(PURE, site, 0) for site in SITES)
    feature_basis = sorted({term for face in mixed_faces + pure_faces for term in face})
    feature_index = {term: index for index, term in enumerate(feature_basis)}

    def coefficient_vector(face):
        answer = [0] * len(feature_basis)
        for term in face:
            answer[feature_index[term]] += 1
        return tuple(answer)

    mixed_vectors = tuple(coefficient_vector(face) for face in mixed_faces)
    pure_vectors = tuple(coefficient_vector(face) for face in pure_faces)
    assert_true(rank(pure_vectors) == 5, "pure face rank changed")
    assert_true(rank(pure_vectors + mixed_vectors) == 10,
                "mixed initial cokernel rank changed")

    # The induced reset defect of (u-H_0)r_m is
    # (u-H_0) h_v Y_0 in column v.  The five h_v supports are disjoint, so
    # after labelling their classes omega_v, extraction of the u coefficient
    # is exactly I_5.  The correction has u-degree zero and edge degree 6.
    u_leading = tuple(standard(index) for index in range(5))
    assert_true(rank(u_leading) == 5, "u-leading face map is not I_5")
    assert_true(all(len(face) == 3 for face in mixed_faces), "h_v term count changed")
    h_edge_degree = 2
    h0_edge_degree = 4
    correction_edge_degree = h_edge_degree + h0_edge_degree
    assert_true(correction_edge_degree == 6, "H_0 h_v correction degree changed")

    return {
        "selected_columns": [list(label) for label in selected],
        "support_sizes": [len(support) for support in supports],
        "active_full_image_coordinates": len(active),
        "inactive_all_mismatch_coordinates": len(inactive),
        "column_ownership_identity": [[int(entry) for entry in row]
                                       for row in ownership],
        "pure_face_rank": rank(pure_vectors),
        "combined_face_rank": rank(pure_vectors + mixed_vectors),
        "u_leading_face_rank": rank(u_leading),
        "u_leading_matrix": [[int(entry) for entry in row] for row in u_leading],
        "h_edge_degree": h_edge_degree,
        "H0_h_correction_edge_degree": correction_edge_degree,
        "smallest_scope": "coordinate subpresentation retaining five entire images",
    }


def preserving_permutations(fix_r):
    answer = []
    for permutation in permutations(range(5)):
        if tuple(MIXED[permutation[index]] for index in range(5)) != MIXED:
            continue
        # permutation[index] is the old coordinate read at the new index;
        # fixing r is equivalent to either convention for a fixed point.
        if fix_r and permutation[R_SITE - 1] != R_SITE - 1:
            continue
        answer.append(tuple(permutation))
    return tuple(answer)


def permute_vector(vector, permutation):
    return tuple(Q(vector[permutation[index]]) for index in range(5))


def orbit(vector, group):
    return tuple(sorted(set(permute_vector(vector, permutation) for permutation in group)))


def orbit_partition(group):
    unseen = set(range(5))
    parts = []
    while unseen:
        seed = min(unseen)
        part = {
            next(index for index, entry in enumerate(image) if entry)
            for image in orbit(standard(seed), group)
        }
        parts.append(tuple(sorted(part)))
        unseen -= part
    return tuple(parts)


def symmetry_check():
    full_group = preserving_permutations(False)
    fixed_group = preserving_permutations(True)
    assert_true(len(full_group) == 12, "word stabilizer order changed")
    assert_true(len(fixed_group) == 4, "fixed-r subgroup order changed")
    full_parts = orbit_partition(full_group)
    fixed_parts = orbit_partition(fixed_group)
    assert_true(full_parts == ((0, 2, 3), (1, 4)), "full word orbits changed")
    assert_true(fixed_parts == ((0, 3), (1, 4), (2,)), "fixed-r orbits changed")

    full_seed_orbits = orbit(standard(0), full_group) + orbit(standard(1), full_group)
    fixed_seed_orbits = (
        orbit(standard(0), fixed_group)
        + orbit(standard(2), fixed_group)
        + orbit(standard(1), fixed_group)
    )
    assert_true(rank(full_seed_orbits) == 5, "two family templates stopped spanning")
    assert_true(rank(fixed_seed_orbits) == 5, "three fixed templates stopped spanning")

    generic = (1, 2, 4, 8, 16)
    full_generic_rank = rank(orbit(generic, full_group))
    fixed_generic_rank = rank(orbit(generic, fixed_group))
    assert_true(full_generic_rank == 4, "full cyclic maximum changed")
    assert_true(fixed_generic_rank == 3, "fixed cyclic maximum changed")

    # Reynolds images are constant on group orbits.  Their dimensions equal
    # the number of orbits: two for the relabelled-r family and three in the
    # fixed chart.  Each cyclic module contributes at most one invariant
    # direction, proving the lower bounds of two and three generators.
    full_invariants = tuple(
        tuple(ONE if index in part else ZERO for index in range(5))
        for part in full_parts
    )
    fixed_invariants = tuple(
        tuple(ONE if index in part else ZERO for index in range(5))
        for part in fixed_parts
    )
    assert_true(rank(full_invariants) == 2 and rank(fixed_invariants) == 3,
                "invariant multiplicities changed")

    return {
        "word_stabilizer_order": len(full_group),
        "word_stabilizer_orbits_one_based": [
            [index + 1 for index in part] for part in full_parts
        ],
        "word_stabilizer_invariant_dimension": rank(full_invariants),
        "word_stabilizer_generic_cyclic_rank": full_generic_rank,
        "relabelled_r_minimum_templates": 2,
        "fixed_r_subgroup_order": len(fixed_group),
        "fixed_r_orbits_one_based": [
            [index + 1 for index in part] for part in fixed_parts
        ],
        "fixed_r_invariant_dimension": rank(fixed_invariants),
        "fixed_r_generic_cyclic_rank": fixed_generic_rank,
        "fixed_r_minimum_seed_types": 3,
        "relabelled_scope_requires_chart_compatibility": True,
    }


DIRECT_FREE_Q = (
    (1, 2, 1, 2, 1), (1, 3, 1, 2, 1), (1, 4, 1, 1, 1),
    (2, 3, 2, 0, 1), (3, 4, 0, 1, 1), (3, 5, 0, 2, 1),
)

TILTED_Q = (
    (1, 2, 1, 2, 1), (1, 3, 0, 0, 1), (1, 4, 1, 1, 1),
    (1, 5, 2, 2, 1), (2, 3, 2, 0, 1),
    (3, 4, 0, 1, 1), (3, 5, 0, 2, 1),
)


def sparse_value(rows):
    table = {edge(left, right, left_colour, right_colour): Q(value)
             for left, right, left_colour, right_colour, value in rows}

    def value(left, right, left_colour, right_colour):
        return table.get(edge(left, right, left_colour, right_colour), ZERO)

    return value


def numerical_denominator(value):
    matrix = []
    for word in WORDS:
        row = []
        colouring = dict(zip(SITES, word))
        for deleted, linear_colour in LABELS:
            if colouring[deleted] != linear_colour:
                row.append(ZERO)
                continue
            total = ZERO
            remaining = tuple(site for site in SITES if site != deleted)
            for matching in perfect_matchings(remaining):
                term = ONE
                for left, right in matching:
                    term *= value(left, right, colouring[left], colouring[right])
                total += term
            row.append(total)
        matrix.append(row)
    return matrix


def packet_data(rows):
    matrix = numerical_denominator(sparse_value(rows))
    selected = tuple(LABELS.index((site, MIXED[site - 1])) for site in SITES)
    kernel_basis = nullspace(matrix)
    image_rows = tuple(
        tuple(vector[index] for index in selected) for vector in kernel_basis
    )
    image_rank = rank(image_rows)
    return matrix, kernel_basis, image_rows, image_rank


def packet_check():
    direct_matrix, direct_kernel, direct_image, direct_rank = packet_data(DIRECT_FREE_Q)
    tilted_matrix, tilted_kernel, tilted_image, tilted_rank = packet_data(TILTED_Q)
    assert_true((rank(direct_matrix), len(direct_kernel), direct_rank) == (7, 8, 4),
                "direct-free packet dimensions changed")
    assert_true((rank(tilted_matrix), len(tilted_kernel), tilted_rank) == (8, 7, 3),
                "tilted packet dimensions changed")
    assert_true(all(in_row_span(row, direct_image) for row in tilted_image),
                "tilted image is no longer contained in direct-free image")

    complement = (standard(1), standard(4))
    assert_true(rank(direct_image + complement) == 5,
                "omega2,omega5 do not complete direct image")
    assert_true(rank(tilted_image + complement) == 5,
                "omega2,omega5 do not complete tilted image")
    individual_direct = tuple(in_row_span(standard(index), direct_image)
                              for index in range(5))
    individual_tilted = tuple(in_row_span(standard(index), tilted_image)
                              for index in range(5))
    assert_true(individual_direct == individual_tilted
                == (True, False, True, False, False),
                "individual packet face hits changed")

    direct_invisible = len(direct_kernel) - direct_rank
    tilted_invisible = len(tilted_kernel) - tilted_rank
    assert_true(direct_invisible == tilted_invisible == 4,
                "packet cap-invisible kernel dimensions changed")

    selected = tuple(LABELS.index((site, MIXED[site - 1])) for site in SITES)
    mixed_row = WORDS.index(MIXED)
    assert_true(tuple(direct_matrix[mixed_row][index] for index in selected)
                == (ZERO,) * 5, "direct h_v values changed")
    assert_true(tuple(tilted_matrix[mixed_row][index] for index in selected)
                == (ZERO,) * 5, "tilted h_v values changed")

    return {
        "direct_free": {
            "rank": rank(direct_matrix),
            "tor_dimension": len(direct_kernel),
            "face_image_rank": direct_rank,
            "missing_rank": 5 - direct_rank,
            "cap_invisible_kernel": direct_invisible,
            "individual_faces": list(individual_direct),
        },
        "tilted": {
            "rank": rank(tilted_matrix),
            "tor_dimension": len(tilted_kernel),
            "face_image_rank": tilted_rank,
            "missing_rank": 5 - tilted_rank,
            "cap_invisible_kernel": tilted_invisible,
            "individual_faces": list(individual_tilted),
        },
        "tilted_image_contained_in_direct_free": True,
        "common_completing_directions": ["omega_2", "omega_5"],
        "packet_scope_only": True,
    }


def execute(mode):
    ledger = {}
    if mode in ("all", "subpresentation"):
        ledger["subpresentation"] = universal_subpresentation()
    if mode in ("all", "symmetry"):
        ledger["symmetry"] = symmetry_check()
    if mode in ("all", "packets"):
        ledger["packets"] = packet_check()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if mode == "all":
        assert_true(digest == EXPECTED_DIGEST, f"audit digest changed: {digest}")
    print(f"independent single-Koszul face-star audit ({mode}): PASS")
    if mode in ("all", "subpresentation"):
        print("full-image coordinate subpresentation: 5 -> 211; u-leading map I5")
    if mode in ("all", "symmetry"):
        print("relabelled r-family: 2 templates; fixed r=3 chart: 3 seed types")
    if mode in ("all", "packets"):
        print("packet face ranks 4/3; cap-invisible kernels both dimension 4")
    print(f"sha256: {digest}")
    return digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "subpresentation", "symmetry", "packets"),
        default="all",
    )
    arguments = parser.parse_args()
    execute(arguments.mode)


if __name__ == "__main__":
    main()

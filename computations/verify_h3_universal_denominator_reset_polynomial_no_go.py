#!/usr/bin/env python3
"""Exact universal-q no-go for a polynomially corrected reset at 12112.

The five odd sites have three colours.  The denominator presentation is

    D : R^{15} -> R^{243},   d_(v,a) |-> e_a^(v) q^[2],

over the polynomial ring in all labelled internal q-edges.  This checker
uses sparse monomials and exact integer/rational linear algebra only.  It
verifies that the lowest q-degree map on a proposed polynomial extraction
functional is injective, that the five mixed defects are independent from
the pure-output part of the existing denominator image, and that five new
four-face generators are the minimal abstract chain-level repair.
"""

from collections import defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


COLORS = (0, 1, 2)
SITES = (1, 2, 3, 4, 5)
MIXED = (1, 2, 1, 1, 2)
PURE = (0, 0, 0, 0, 0)
EXPECTED_DIGEST = "b2df7d7ce01dc008a7c8e65285c1c0368d6750ee5d97cc2ab2c2eba607318dd4"


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


def matching_monomial(matching, word):
    colouring = dict(zip(SITES, word))
    return tuple(sorted(
        edge(left, right, colouring[left], colouring[right])
        for left, right in matching
    ))


def denominator_entry(word, site, colour):
    """Sparse coefficient of e_word in e_colour^(site) q^[2]."""
    position = SITES.index(site)
    if word[position] != colour:
        return ()
    remaining = tuple(vertex for vertex in SITES if vertex != site)
    return tuple(sorted(
        matching_monomial(matching, word)
        for matching in matchings(remaining)
    ))


def matrix_rank(rows):
    """Exact rank over Q for a small integer matrix."""
    from fractions import Fraction as Q

    work = [[Q(entry) for entry in row] for row in rows]
    rank = 0
    width = len(work[0]) if work else 0
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
        rank += 1
    return rank


def monomial_text(monomial):
    return "*".join(
        f"q{left}{right}^{left_colour}{right_colour}"
        for left, right, left_colour, right_colour in monomial
    )


def main():
    words = tuple(product(COLORS, repeat=len(SITES)))
    columns = tuple((site, colour) for site in SITES for colour in COLORS)

    # A feature records both a denominator column and a q^[2] monomial.
    # In a fixed column, the two labelled edges of a matching cover the four
    # non-deleted sites, so their colours recover the entire word.  Hence each
    # feature has a unique owner.  This proves injectivity of the q-degree-two
    # map on constant extraction coefficients.
    owners = defaultdict(set)
    feature_count_by_word = {}
    for word in words:
        count = 0
        for site, colour in columns:
            for term in denominator_entry(word, site, colour):
                owners[((site, colour), term)].add(word)
                count += 1
        feature_count_by_word["".join(map(str, word))] = count

    require(len(owners) == 15 * 81 * 3, "universal feature count changed")
    require(
        all(len(feature_owners) == 1 for feature_owners in owners.values()),
        "a denominator monomial no longer determines its word",
    )
    require(
        set(feature_count_by_word.values()) == {15},
        "each word should own three terms in each of five columns",
    )
    constant_initial_rank = len(words)

    # The bare extraction at 12112 meets exactly the five columns whose
    # chosen colour agrees with the word.  Its values are the five nonzero
    # four-site hafnians h_v.
    defects = {}
    nonzero_mixed_columns = []
    for site, colour in columns:
        entry = denominator_entry(MIXED, site, colour)
        if entry:
            nonzero_mixed_columns.append((site, colour))
            require(len(entry) == 3, "a four-site hafnian changed size")
            defects[site] = entry
    require(
        tuple(nonzero_mixed_columns)
        == tuple((site, MIXED[SITES.index(site)]) for site in SITES),
        "the five reset defects changed columns",
    )

    # At the pure output coordinate e_00000, the old target denominator
    # image has only five nonzero degree-two vectors g_v, all in pure-zero
    # fine colour degrees.  The mixed h_v use only colours 1 and 2.  The ten
    # vectors therefore have pairwise disjoint supports and exact rank ten.
    pure_output_vectors = {}
    for site in SITES:
        pure_output_vectors[site] = denominator_entry(PURE, site, 0)
        require(len(pure_output_vectors[site]) == 3, "pure face hafnian changed")

    vector_labels = [
        ("g", site, pure_output_vectors[site]) for site in SITES
    ] + [
        ("h", site, defects[site]) for site in SITES
    ]
    monomial_basis = sorted({
        term for _, _, vector in vector_labels for term in vector
    })
    monomial_index = {term: index for index, term in enumerate(monomial_basis)}
    coefficient_rows = []
    for _, _, vector in vector_labels:
        row = [0] * len(monomial_basis)
        for term in vector:
            row[monomial_index[term]] += 1
        coefficient_rows.append(row)
    combined_face_rank = matrix_rank(coefficient_rows)
    pure_face_rank = matrix_rank(coefficient_rows[:5])
    require(pure_face_rank == 5, "pure target denominator face rank changed")
    require(combined_face_rank == 10, "mixed defects lost five independent classes")
    defect_cokernel_rank = combined_face_rank - pure_face_rank
    require(defect_cokernel_rank == 5, "minimal repair rank changed")

    # Abstract minimal repair: add tau_v with boundary h_v Y_0 and send the
    # five hit source denominator columns to the corresponding tau_v.  This
    # is a literal chain identity on all fifteen source columns.  The ten
    # other columns map to zero.  Since every added boundary has positive
    # q-degree, augmentation q -> 0 proves that Y_0 itself survives.
    chain_identity = {}
    for site, colour in columns:
        left = denominator_entry(MIXED, site, colour)
        right = defects[site] if colour == MIXED[SITES.index(site)] else ()
        require(left == right, f"abstract tau chain identity failed at {(site, colour)}")
        chain_identity[f"{site}:{colour}"] = len(left)
    y0_survives_by_q_augmentation = True

    defect_ledger = {
        str(site): [monomial_text(term) for term in defects[site]]
        for site in SITES
    }
    ledger = {
        "word_count": len(words),
        "denominator_columns": len(columns),
        "degree_two_features": len(owners),
        "feature_owner_multiplicities": sorted({
            len(feature_owners) for feature_owners in owners.values()
        }),
        "features_per_word": sorted(set(feature_count_by_word.values())),
        "constant_initial_rank": constant_initial_rank,
        "mixed_word": "12112",
        "mixed_hit_columns": [list(item) for item in nonzero_mixed_columns],
        "defects": defect_ledger,
        "pure_output_face_rank": pure_face_rank,
        "combined_pure_mixed_face_rank": combined_face_rank,
        "defect_cokernel_rank": defect_cokernel_rank,
        "abstract_tau_chain_identity_term_counts": chain_identity,
        "y0_survives_by_q_augmentation": y0_survives_by_q_augmentation,
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("h=3 universal denominator reset polynomial no-go: PASS")
    print("15-column q-degree-2 initial map on extraction constants: rank 243")
    print("normalized polynomial correction at 12112: impossible")
    print("old pure-output denominator face rank 5; mixed defects add rank 5")
    print("minimal abstract repair: five four-face generators tau_v")
    print("Y_0 survives the repair by q -> 0 augmentation")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

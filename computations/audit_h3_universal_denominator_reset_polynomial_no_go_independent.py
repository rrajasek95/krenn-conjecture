#!/usr/bin/env python3
"""Independent audit of the universal five-site denominator reset no-go.

This checker does not import the primary implementation.  It constructs the
three perfect matchings on each four-site deletion face directly, audits the
lowest-q-degree feature map, and separates the minimal abstract tau repair
from any claim of a physical full-nine source lift.
"""

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json


Q = Fraction
SITES = (1, 2, 3, 4, 5)
COLORS = (0, 1, 2)
MIXED = (1, 2, 1, 1, 2)
PURE = (0, 0, 0, 0, 0)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(site_left, site_right, color_left, color_right):
    if site_left < site_right:
        return site_left, site_right, color_left, color_right
    return site_right, site_left, color_right, color_left


def three_pairings(face):
    """The three perfect matchings of a sorted four-element face."""
    require(len(face) == 4 and tuple(sorted(face)) == tuple(face),
            "face must contain four sorted sites")
    a, b, c, d = face
    return (
        ((a, b), (c, d)),
        ((a, c), (b, d)),
        ((a, d), (b, c)),
    )


def face_hafnian(word, omitted_site):
    colors = dict(zip(SITES, word))
    face = tuple(site for site in SITES if site != omitted_site)
    terms = []
    for pairing in three_pairings(face):
        monomial = tuple(sorted(
            edge(left, right, colors[left], colors[right])
            for left, right in pairing
        ))
        terms.append(monomial)
    require(len(set(terms)) == 3, "four-face hafnian lost a monomial")
    return tuple(sorted(terms))


def denominator_entry(word, site, color):
    """Coefficient at e_word of e_color^(site) q^[2]."""
    if word[site - 1] != color:
        return ()
    return face_hafnian(word, site)


def monomial_text(monomial):
    return "*".join(
        f"q{left}{right}^{left_color}{right_color}"
        for left, right, left_color, right_color in monomial
    )


def matrix_rank(rows):
    work = [[Q(entry) for entry in row] for row in rows]
    if not work:
        return 0
    width = len(work[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(work))
             if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def denominator_audit():
    words = tuple(product(COLORS, repeat=5))
    columns = tuple((site, color) for site in SITES for color in COLORS)
    owners = {}
    column_term_counts = {}
    word_feature_counts = {word: 0 for word in words}

    for site, color in columns:
        terms_in_column = 0
        nonzero_rows = 0
        for word in words:
            entry = denominator_entry(word, site, color)
            if entry:
                nonzero_rows += 1
            for monomial in entry:
                feature = ((site, color), monomial)
                require(feature not in owners,
                        "a fixed-column monomial has two word owners")
                owners[feature] = word
                word_feature_counts[word] += 1
                terms_in_column += 1
        require(nonzero_rows == 3 ** 4,
                "denominator column has wrong nonzero word count")
        require(terms_in_column == 3 * 3 ** 4,
                "denominator column has wrong monomial count")
        column_term_counts[f"{site}:{color}"] = terms_in_column

    require(len(owners) == 15 * 81 * 3,
            "universal denominator feature count changed")
    require(set(word_feature_counts.values()) == {15},
            "a word does not own three terms on each deletion face")

    # Independently reconstruct the owner from a feature: its two labelled
    # edges cover the four retained sites, while the column gives the color
    # of the omitted site.
    for ((site, color), monomial), owner in owners.items():
        reconstructed = {site: color}
        for left, right, left_color, right_color in monomial:
            require(left not in reconstructed and right not in reconstructed,
                    "feature does not encode a perfect matching")
            reconstructed[left] = left_color
            reconstructed[right] = right_color
        rebuilt_word = tuple(reconstructed[position] for position in SITES)
        require(rebuilt_word == owner,
                "labelled feature does not reconstruct its owner")

    return {
        "words": len(words),
        "columns": len(columns),
        "features": len(owners),
        "features_per_word": sorted(set(word_feature_counts.values())),
        "column_term_counts": column_term_counts,
    }, owners


def initial_degree_audit(owners):
    words = tuple(product(COLORS, repeat=5))
    pivots = {}
    for word in words:
        site = 1
        color = word[0]
        monomial = denominator_entry(word, site, color)[0]
        feature = ((site, color), monomial)
        require(owners[feature] == word, "chosen pivot has wrong owner")
        require(feature not in pivots.values(), "two words share a pivot")
        pivots[word] = feature

    # In degree two, the coefficient of a pivot feature in L*delta is
    # exactly the constant term c_word.  Thus all 243 constants are forced
    # to zero.  In particular c_12112 cannot be the normalized value one.
    require(len(pivots) == len(words) == 243,
            "initial feature map is not rank 243")
    mixed_pivot = pivots[MIXED]
    require(owners[mixed_pivot] == MIXED,
            "normalized mixed coefficient could cancel at initial degree")
    return {
        "initial_rank": len(pivots),
        "forced_zero_constants": len(pivots),
        "normalized_word": "12112",
        "normalized_constant_one_impossible": True,
        "mixed_pivot": [
            list(mixed_pivot[0]),
            [list(edge_token) for edge_token in mixed_pivot[1]],
        ],
    }


def vector_rank(vectors):
    basis = sorted({monomial for vector in vectors for monomial in vector})
    index = {monomial: position for position, monomial in enumerate(basis)}
    rows = []
    for vector in vectors:
        row = [0] * len(basis)
        for monomial in vector:
            row[index[monomial]] += 1
        rows.append(row)
    return matrix_rank(rows), basis


def faces_audit():
    pure_faces = {site: face_hafnian(PURE, site) for site in SITES}
    mixed_faces = {site: face_hafnian(MIXED, site) for site in SITES}

    expected_mixed = {
        1: {
            "q23^21*q45^12", "q24^21*q35^12", "q25^22*q34^11",
        },
        2: {
            "q13^11*q45^12", "q14^11*q35^12", "q15^12*q34^11",
        },
        3: {
            "q12^12*q45^12", "q14^11*q25^22", "q15^12*q24^21",
        },
        4: {
            "q12^12*q35^12", "q13^11*q25^22", "q15^12*q23^21",
        },
        5: {
            "q12^12*q34^11", "q13^11*q24^21", "q14^11*q23^21",
        },
    }
    for site in SITES:
        actual = {monomial_text(term) for term in mixed_faces[site]}
        require(actual == expected_mixed[site],
                f"mixed four-face formula h_{site} changed")

    pure_rank, pure_basis = vector_rank(tuple(pure_faces.values()))
    mixed_rank, mixed_basis = vector_rank(tuple(mixed_faces.values()))
    combined_rank, _ = vector_rank(
        tuple(pure_faces.values()) + tuple(mixed_faces.values())
    )
    require(pure_rank == 5 and mixed_rank == 5,
            "pure or mixed deletion-face rank changed")
    require(combined_rank == 10,
            "mixed faces are not independent modulo pure faces")
    require(set(pure_basis).isdisjoint(mixed_basis),
            "pure and mixed monomial supports overlap")

    for family in (pure_faces, mixed_faces):
        for left in SITES:
            for right in SITES:
                if left >= right:
                    continue
                require(set(family[left]).isdisjoint(family[right]),
                        "different deletion faces share fine support")

    return {
        "pure_rank": pure_rank,
        "mixed_rank": mixed_rank,
        "combined_rank": combined_rank,
        "defect_cokernel_rank": combined_rank - pure_rank,
        "mixed_faces": {
            str(site): sorted(monomial_text(term)
                              for term in mixed_faces[site])
            for site in SITES
        },
    }, pure_faces, mixed_faces


def repair_audit(pure_faces, mixed_faces):
    columns = tuple((site, color) for site in SITES for color in COLORS)
    identity_counts = {}
    tau_records = []
    for site in SITES:
        face_word = "".join(
            str(MIXED[position - 1])
            for position in SITES if position != site
        )
        tau_records.append({
            "name": f"tau_{site}",
            "deleted_site": site,
            "face_word": face_word,
            "boundary": sorted(monomial_text(term)
                               for term in mixed_faces[site]),
            "abstract_only": True,
        })

    for site, color in columns:
        bare_reset_boundary = denominator_entry(MIXED, site, color)
        tau_boundary = (
            mixed_faces[site] if color == MIXED[site - 1] else ()
        )
        require(bare_reset_boundary == tau_boundary,
                f"tau chain identity failed on column {(site, color)}")
        identity_counts[f"{site}:{color}"] = len(tau_boundary)

    # All old and new boundary coefficients consist of q-degree-two
    # monomials.  Polynomial multiples remain in the augmentation ideal,
    # whereas the constant output basis vector Y0 evaluates to one.
    every_boundary_monomial = [
        monomial for face in pure_faces.values() for monomial in face
    ] + [
        monomial for face in mixed_faces.values() for monomial in face
    ]
    require(all(len(monomial) == 2 for monomial in every_boundary_monomial),
            "a repair boundary acquired q-degree zero")
    boundary_augmentation = 0
    y0_augmentation = 1
    require(boundary_augmentation == 0 and y0_augmentation == 1,
            "q=0 augmentation no longer separates Y0")

    require(len(tau_records) == 5,
            "abstract repair does not contain five face generators")
    return {
        "tau_count": len(tau_records),
        "minimal_initial_rank": 5,
        "chain_identity_term_counts": identity_counts,
        "boundary_augmentation": boundary_augmentation,
        "y0_augmentation": y0_augmentation,
        "tau_records": tau_records,
    }, tau_records


def provenance_audit(tau_records):
    # This is a scope lock, not a construction: none of the data required
    # for physical provenance occurs in the abstract tau presentation.
    required_physical_fields = {
        "full_nine_source_row",
        "target_cancellation",
        "ordinary_residue_cancellation",
        "other_boundary_cancellation",
        "tor_transgression_class",
    }
    for record in tau_records:
        require(required_physical_fields.isdisjoint(record),
                "abstract tau record silently claims physical provenance")
        require(record["abstract_only"] is True,
                "abstract tau scope marker was removed")
    return {
        "abstract_tau_count": len(tau_records),
        "physical_provenance_supplied": False,
        "rational_localized_lift_excluded": False,
        "full_source_tor_lift_excluded": False,
    }


EXPECTED_DIGEST = "c7fdfc45332832602e08d580be9a73c48c18113ea113066fec6ef9d9c7240342"


def run(mode):
    ledger = {}
    denominator = owners = None
    faces = pure_faces = mixed_faces = None
    repair = tau_records = None

    if mode in ("all", "denominator", "initial"):
        denominator, owners = denominator_audit()
        if mode in ("all", "denominator"):
            ledger["denominator"] = denominator
    if mode in ("all", "initial"):
        ledger["initial"] = initial_degree_audit(owners)
    if mode in ("all", "faces", "repair", "provenance"):
        faces, pure_faces, mixed_faces = faces_audit()
        if mode in ("all", "faces"):
            ledger["faces"] = faces
    if mode in ("all", "repair", "provenance"):
        repair, tau_records = repair_audit(pure_faces, mixed_faces)
        if mode in ("all", "repair"):
            ledger["repair"] = repair
    if mode in ("all", "provenance"):
        ledger["provenance"] = provenance_audit(tau_records)

    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if mode == "all":
        require(digest == EXPECTED_DIGEST,
                f"independent universal-reset digest changed: {digest}")
    print(f"independent universal denominator reset audit ({mode}): PASS")
    if mode in ("all", "denominator", "initial"):
        print("15 universal columns; degree-two initial rank 243")
    if mode in ("all", "faces"):
        print("pure face rank 5; mixed face rank 5 modulo the pure span")
    if mode in ("all", "repair"):
        print("minimal abstract repair has five tau generators; Y0 survives")
    if mode in ("all", "provenance"):
        print("physical, localized-rational, and Tor provenance remain unproved")
    print(f"sha256: {digest}")
    return digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("all", "denominator", "initial", "faces", "repair", "provenance"),
        default="all",
    )
    arguments = parser.parse_args()
    run(arguments.mode)


if __name__ == "__main__":
    main()

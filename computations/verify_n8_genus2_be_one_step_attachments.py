#!/usr/bin/env python3
"""Classify the first physical attachments to the genus-two BE rows.

The direct Pfaffian probe leaves one doubled physical site in every odd
principal Buchsbaum--Eisenbud row.  This checker exhausts the two already
audited one-step physical operations on those rows:

* insert one labelled physical edge (the direct/diagonal full-nine move), or
* contract one physical pair (the pair-deletion/cofactor move).

Insertion never removes the double incidence.  A contraction removes it only
when the contracted edge joins the doubled site to another site of the odd
principal set.  The result is duplicate-free, but has respectively six, four,
or two holes for odd sizes three, five, or seven.  Hence no one-step result is
an eight-site squarefree source row.  The decorated-word and spin-character
audits independently show that none couples a pure anchor to the crossed row.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path

import verify_n8_genus2_arf_fullnine_syzygy_probe as base


EXPECTED_PARENT_SHA256 = (
    "06c8aebe01e06d03f17203b617be65c5c7b9ff899a040209e27ee252e735d70e"
)
EXPECTED_LEDGER_SHA256 = (
    "fbf8d2003280d9a0d909dba8291bd1ea2d8b37842cf1e53682759331bd92796a"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def kasteleyn_edge_labels():
    """Reconstruct the pinned four-bit edge labels from the parent probe."""
    faces = base.face_walks()
    face_rows = []
    for face in faces:
        row = 0
        for u, v in face:
            row ^= 1 << base.EDGE_INDEX[base.edge(u, v)]
        face_rows.append(row)

    cocycles = base.gf2_nullspace(face_rows, len(base.EDGES))
    coboundaries = []
    for vertex in base.VERTICES[:-1]:
        coboundaries.append(sum(
            1 << base.EDGE_INDEX[base.edge(vertex, other)]
            for other in base.VERTICES if other != vertex
        ))
    quotient_basis = []
    span = list(coboundaries)
    for cocycle in cocycles:
        if base.gf2_rank(span + [cocycle], len(base.EDGES)) > len(span):
            span.append(cocycle)
            quotient_basis.append(cocycle)
    require(len(quotient_basis) == 4,
            "the pinned spin-coordinate dimension changed")
    return {
        physical_edge: sum(
            (((cocycle >> base.EDGE_INDEX[physical_edge]) & 1) << coordinate)
            for coordinate, cocycle in enumerate(quotient_basis)
        )
        for physical_edge in base.EDGES
    }


def is_squarefree(degree):
    return all(value <= 1 for value in degree)


def restricted_word_grade(word, support):
    return frozenset((site, word[site]) for site in support)


def main():
    parent = Path(__file__).with_name(
        "verify_n8_genus2_arf_fullnine_syzygy_probe.py"
    )
    parent_sha = sha256(parent.read_bytes()).hexdigest()
    require(parent_sha == EXPECTED_PARENT_SHA256,
            f"the parent Pfaffian probe changed: {parent_sha}")

    edge_labels = kasteleyn_edge_labels()
    edge_label_histogram = Counter(edge_labels.values())
    require(edge_label_histogram[0] == 12
            and sum(edge_label_histogram.values()) == 28,
            f"the edge-character census changed: {edge_label_histogram}")
    require(edge_labels[(0, 1)] == edge_labels[(0, 2)] == 13,
            "the two pinned chart edges changed spin coordinates")

    be_rows_by_size = Counter()
    insertion_by_character = Counter()
    insertion_by_arf_label = Counter()
    insertion_degree_signatures = {size: Counter() for size in (3, 5, 7)}
    inserted_squarefree = 0
    chart_insertions = Counter()
    valid_contractions_by_size = Counter()
    valid_contractions_by_arf_label = Counter()
    contraction_degree_signatures = {size: Counter() for size in (3, 5, 7)}
    duplicate_free_by_size = Counter()
    duplicate_free_by_holes = Counter()
    duplicate_free_by_character = Counter()
    duplicate_free_by_arf_label = Counter()
    fully_squarefree_k8 = 0

    # Exhaust all 504 odd-principal rows and all 28 physical operations.
    for odd_size in (3, 5, 7):
        for subset_tuple in itertools.combinations(base.VERTICES, odd_size):
            subset = frozenset(subset_tuple)
            for doubled_site in subset_tuple:
                be_rows_by_size[odd_size] += 1
                degree = [
                    2 if site == doubled_site else 1 if site in subset else 0
                    for site in base.VERTICES
                ]

                for physical_edge in base.EDGES:
                    # A labelled full-nine insertion is multiplication by a
                    # cell on this physical edge.  Colour labels do not alter
                    # its physical occupancy effect.
                    inserted = degree[:]
                    for site in physical_edge:
                        inserted[site] += 1
                    inserted_squarefree += int(is_squarefree(inserted))
                    insertion_degree_signatures[odd_size][
                        tuple(sorted(inserted))
                    ] += 1
                    character = ("trivial" if edge_labels[physical_edge] == 0
                                 else "nontrivial")
                    insertion_by_character[character] += 1
                    insertion_by_arf_label[edge_labels[physical_edge]] += 1
                    if physical_edge in ((0, 1), (0, 2)):
                        chart_insertions[character] += 1

                    # The audited cofactor contraction is defined only when
                    # both endpoint incidences occur.  It removes one at each.
                    u, v = physical_edge
                    if not degree[u] or not degree[v]:
                        continue
                    valid_contractions_by_size[odd_size] += 1
                    valid_contractions_by_arf_label[
                        edge_labels[physical_edge]
                    ] += 1
                    contracted = degree[:]
                    contracted[u] -= 1
                    contracted[v] -= 1
                    contraction_degree_signatures[odd_size][
                        tuple(sorted(contracted))
                    ] += 1
                    if is_squarefree(contracted):
                        duplicate_free_by_size[odd_size] += 1
                        holes = sum(value == 0 for value in contracted)
                        duplicate_free_by_holes[holes] += 1
                        duplicate_free_by_character[character] += 1
                        duplicate_free_by_arf_label[
                            edge_labels[physical_edge]
                        ] += 1
                        require(doubled_site in physical_edge,
                                "a contraction away from the double site "
                                "became duplicate-free")
                        other = v if u == doubled_site else u
                        require(other in subset - {doubled_site},
                                "an invalid contraction became duplicate-free")
                    fully_squarefree_k8 += int(
                        all(value == 1 for value in contracted)
                    )

    require(be_rows_by_size == Counter({3: 168, 5: 280, 7: 56}),
            f"the BE row census changed: {be_rows_by_size}")
    require(inserted_squarefree == 0,
            "one physical insertion removed the doubled incidence")
    require(insertion_by_character
            == Counter({"trivial": 6048, "nontrivial": 8064}),
            f"the insertion-character census changed: {insertion_by_character}")
    require(insertion_by_arf_label == Counter({
        0: 6048, 13: 1512, 12: 1512, 6: 1008, 2: 1008, 4: 1008,
        15: 504, 7: 504, 1: 504, 8: 504,
    }), f"the insertion Arf-label census changed: {insertion_by_arf_label}")
    require(chart_insertions == Counter({"nontrivial": 1008}),
            f"the literal chart insertion census changed: {chart_insertions}")

    require(valid_contractions_by_size
            == Counter({3: 504, 5: 2800, 7: 1176}),
            f"the valid contraction census changed: {valid_contractions_by_size}")
    require(valid_contractions_by_arf_label == Counter({
        0: 1920, 13: 480, 12: 480, 6: 320, 2: 320, 4: 320,
        15: 160, 7: 160, 1: 160, 8: 160,
    }), f"the valid contraction Arf-label census changed: "
        f"{valid_contractions_by_arf_label}")
    require(duplicate_free_by_size
            == Counter({3: 336, 5: 1120, 7: 336}),
            f"the duplicate-free contraction census changed: "
            f"{duplicate_free_by_size}")
    require(duplicate_free_by_holes
            == Counter({6: 336, 4: 1120, 2: 336}),
            f"the post-contraction hole census changed: "
            f"{duplicate_free_by_holes}")
    require(duplicate_free_by_character
            == Counter({"trivial": 768, "nontrivial": 1024}),
            f"the contraction-character census changed: "
            f"{duplicate_free_by_character}")
    require(duplicate_free_by_arf_label == Counter({
        0: 768, 13: 192, 12: 192, 6: 128, 2: 128, 4: 128,
        15: 64, 7: 64, 1: 64, 8: 64,
    }), f"the duplicate-free Arf-label census changed: "
        f"{duplicate_free_by_arf_label}")
    expected_insertion_signature_counts = {
        3: sorted((168, 336, 840, 1680, 1680)),
        5: sorted((840, 840, 1120, 1680, 3360)),
        7: sorted((56, 336, 336, 840)),
    }
    require({size: sorted(histogram.values())
             for size, histogram in insertion_degree_signatures.items()}
            == expected_insertion_signature_counts,
            f"the insertion degree signatures changed: "
            f"{insertion_degree_signatures}")
    expected_contraction_signature_counts = {
        3: sorted((336, 168)),
        5: sorted((1120, 1680)),
        7: sorted((336, 840)),
    }
    require({size: sorted(histogram.values())
             for size, histogram in contraction_degree_signatures.items()}
            == expected_contraction_signature_counts,
            f"the contraction degree signatures changed: "
            f"{contraction_degree_signatures}")
    require(fully_squarefree_k8 == 0,
            "one pair contraction reached the full eight-site grade")

    # The three literal target words remain separated after every possible
    # duplicate-free BE contraction.  This is stronger than comparing only
    # identical pair deletions: compare all surviving supports at once.
    words = {
        "diagonal_00": (0,) * 8,
        "diagonal_11": (1,) * 8,
        "crossed_01_over_2": (0, 1, 2, 2, 2, 2, 2, 2),
    }
    contracted_word_grades = {label: set() for label in words}
    for odd_size in (3, 5, 7):
        for subset_tuple in itertools.combinations(base.VERTICES, odd_size):
            subset = frozenset(subset_tuple)
            for doubled_site in subset_tuple:
                for other in subset - {doubled_site}:
                    surviving_support = subset - {other}
                    for label, word in words.items():
                        contracted_word_grades[label].add(
                            restricted_word_grade(word, surviving_support)
                        )
    grade_intersections = {}
    for left, right in itertools.combinations(words, 2):
        overlap = contracted_word_grades[left] & contracted_word_grades[right]
        grade_intersections[f"{left}|{right}"] = len(overlap)
        require(not overlap,
                f"a contracted anchor/crossed grade collided: {left}, {right}")

    # A nontrivial edge character is not constant on the sixteen sectors,
    # so it cannot be a scalar multiple of the untwisted Arf aggregate.
    nontrivial_characters = sorted(set(edge_labels.values()) - {0})
    for character in nontrivial_characters:
        signs = {
            (-1) ** ((sector & character).bit_count() & 1)
            for sector in range(16)
        }
        require(signs == {-1, 1},
                "a nontrivial edge character became sector-constant")
    require(len(nontrivial_characters) == 9,
            "the nontrivial character count changed")

    ledger = {
        "parent_probe_sha256": parent_sha,
        "operations": {
            "be_rows_by_size": dict(be_rows_by_size),
            "insertions": {
                "candidates": sum(insertion_by_character.values()),
                "squarefree": inserted_squarefree,
                "by_arf_character": dict(insertion_by_character),
                "by_arf_label": dict(insertion_by_arf_label),
                "degree_signatures_by_size": {
                    size: {str(signature): count
                           for signature, count in histogram.items()}
                    for size, histogram in insertion_degree_signatures.items()
                },
                "literal_chart_01_02": dict(chart_insertions),
            },
            "contractions": {
                "valid_by_size": dict(valid_contractions_by_size),
                "duplicate_free_by_size": dict(duplicate_free_by_size),
                "duplicate_free_by_holes": dict(duplicate_free_by_holes),
                "duplicate_free_by_arf_character": dict(
                    duplicate_free_by_character
                ),
                "valid_by_arf_label": dict(valid_contractions_by_arf_label),
                "duplicate_free_by_arf_label": dict(
                    duplicate_free_by_arf_label
                ),
                "degree_signatures_by_size": {
                    size: {str(signature): count
                           for signature, count in histogram.items()}
                    for size, histogram in contraction_degree_signatures.items()
                },
                "full_k8_squarefree": fully_squarefree_k8,
            },
        },
        "decorated_grade_intersections": grade_intersections,
        "edge_characters": {
            "trivial_edges": edge_label_histogram[0],
            "nontrivial_edges": 28 - edge_label_histogram[0],
            "distinct_nontrivial": len(nontrivial_characters),
            "chart_01": edge_labels[(0, 1)],
            "chart_02": edge_labels[(0, 2)],
        },
        "verdict": (
            "no single labelled insertion or single pair/cofactor contraction "
            "turns a BE row into a full eight-site squarefree source row, and "
            "no duplicate-free lower cofactor couples either diagonal anchor "
            "to the crossed row"
        ),
        "consequence": (
            "this complete one-step layer reaches neither the literal "
            "Component-III residual annihilator nor the scalar-zero "
            "pure-diagonal/single-edge-response cap landing"
        ),
        "scope": (
            "all odd-principal BE rows of sizes 3,5,7 in the pinned genus-2 "
            "K8 expansion; exactly one physical insertion or exactly one "
            "pair-deletion/cofactor contraction, never their composition"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the one-step attachment ledger changed: {digest}")

    print("N=8 genus-2 BE one-step attachment classification: PASS")
    print("insertions: 14,112 checked; 0 squarefree")
    print("contractions: 4,480 valid; 1,792 duplicate-free lower cofactors")
    print("full eight-site squarefree contractions: 0")
    print("decorated anchor/crossed contraction-grade intersections: 0")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

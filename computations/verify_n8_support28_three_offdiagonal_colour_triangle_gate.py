#!/usr/bin/env python3
"""Classify and exclude parity-minimal three-cell colour triangles.

The packet has three disjoint physical edges, one off-diagonal cell of each
unordered colour type 01, 12, and 20, and arbitrary endpoint orientations.
Its colour-incidence graph is a triangle and hence Eulerian, so this is the
first three-cell packet that can enter an all-even diagonal row.

For both affine support-28 target charts, classify every packet under the
actual fixed-support stabilizer and compute exactly which of the 96
permanent-triangle certificates it can change.  A packet fixes six endpoint
colours, leaving only one diagonal physical edge; this gives the covering
bound used below and by larger-packet audits.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = (
    "computations/verify_n8_support28_two_offdiagonal_euler_packet_gate.py"
)
DEPENDENCY_SHA256 = (
    "c5770af65c5f068207c8149f0285b7aebd062cef795a9598160db90869c8bd73"
)
EXPECTED_LEDGER_SHA256 = (
    "25c50e3537cc1b9e724a55a6a663a08b9a28a8ca7ca8e1ad7ca317576d860c22"
)
COLOUR_PAIRS = ((0, 1), (0, 2), (1, 2))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    path = ROOT / relative
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def packets(base):
    answer = []
    for physical_edges in combinations(base.EDGES, 3):
        if len(set().union(*map(set, physical_edges))) != 6:
            continue
        for assigned_pairs in permutations(COLOUR_PAIRS):
            for reversals in product((False, True), repeat=3):
                cells = []
                for endpoints, colours, reversed_orientation in zip(
                        physical_edges, assigned_pairs, reversals, strict=True):
                    orientation = (tuple(reversed(colours))
                                   if reversed_orientation else colours)
                    cells.append((endpoints, orientation))
                answer.append(tuple(sorted(cells)))
    require(len(answer) == 20160, len(answer))
    require(len(set(answer)) == len(answer), "three-cell packet duplicated")
    return tuple(answer)


def packet_words(base, support, packet):
    """All even words containing this packet and one diagonal last edge."""
    word = [None] * len(base.VERTICES)
    occupied = set()
    for endpoints, ordered_colours in packet:
        for vertex, colour in zip(endpoints, ordered_colours, strict=True):
            require(vertex not in occupied, ("packet edges met", packet))
            occupied.add(vertex)
            word[vertex] = colour
    remainder = tuple(vertex for vertex in base.VERTICES if vertex not in occupied)
    require(len(remainder) == 2, (packet, remainder))
    last_edge = tuple(sorted(remainder))
    answer = []
    for colour in support[last_edge]:
        completed = list(word)
        for vertex in remainder:
            completed[vertex] = colour
        completed = tuple(completed)
        require(all(completed.count(item) % 2 == 0 for item in base.COLORS),
                (packet, colour, completed))
        answer.append(completed)
    return tuple(answer), last_edge


def certificate_registry(one, base, support):
    triangles = base.permanent_triangles(support)
    require(len(triangles) == 96, len(triangles))
    records = []
    word_to_certificates = defaultdict(set)
    for index, triangle in enumerate(triangles):
        words = one.triangle_words(base, triangle)
        unit = base.audit_selected_unit(
            triangle,
            support,
            expected_shape=triangle[:3],
            expected_words=words,
        )
        require(unit["rhs_coefficient"] == 2, (index, unit))
        records.append((triangle, words, unit))
        for word in words:
            word_to_certificates[word].add(index)
    incidence_histogram = Counter(
        len(certificates) for certificates in word_to_certificates.values()
    )
    require(sum(size * count for size, count in incidence_histogram.items())
            == 96 * 3, incidence_histogram)
    return tuple(records), word_to_certificates, incidence_histogram


def chart_audit(two, one, base, chart, support, all_packets):
    actions = two.support_stabilizer(base, support, chart)
    orbits = two.orbit_registry(all_packets, actions)
    certificates, word_incidence, incidence_histogram = certificate_registry(
        one, base, support
    )
    maximum_word_incidence = max(map(len, word_incidence.values()))

    packet_word_count_histogram = Counter()
    spoiled_histogram = Counter()
    minimum_untouched = len(certificates)
    worst_records = []
    for packet in all_packets:
        words, last_edge = packet_words(base, support, packet)
        packet_word_count_histogram[len(words)] += 1
        spoiled = set().union(
            *(word_incidence.get(word, set()) for word in words)
        )
        untouched = tuple(index for index in range(len(certificates))
                          if index not in spoiled)
        require(untouched,
                ("three-cell packet covered every certificate", chart, packet))
        spoiled_histogram[len(spoiled)] += 1
        if len(untouched) < minimum_untouched:
            minimum_untouched = len(untouched)
            worst_records = []

        # The packet can enter precisely the enumerated words: six endpoint
        # colours are fixed and the final physical edge must be diagonal.
        for word in words:
            augmented = two.augmented_hafnian(base, word, support, packet)
            new_monomials = tuple(
                monomial for monomial in augmented
                if any(variable.startswith("z") for variable in monomial)
            )
            require(len(new_monomials) == 1,
                    ("packet word lacks its unique three-cell monomial",
                     chart, packet, word, new_monomials))

        selected_index = untouched[0]
        triangle, selected_words, unit = certificates[selected_index]
        require(all(
            two.augmented_hafnian(base, word, support, packet)
            == base.hafnian_coefficient(word, support)
            for word in selected_words
        ), ("selected certificate changed", chart, packet, selected_words))
        if len(untouched) == minimum_untouched:
            worst_records.append({
                "source_labelled_packet": packet,
                "last_diagonal_edge": last_edge,
                "packet_words": tuple("".join(map(str, word))
                                      for word in words),
                "spoiled_certificates": len(spoiled),
                "surviving_certificate_words": unit["words"],
                "surviving_certificate_shape": triangle[:3],
            })

    maximum_packet_words = max(packet_word_count_histogram)
    require(len(certificates) - minimum_untouched
            <= maximum_word_incidence * maximum_packet_words,
            (chart, minimum_untouched, maximum_word_incidence,
             maximum_packet_words))
    certificate_word_cover_lower_bound = (
        len(certificates) + maximum_word_incidence - 1
    ) // maximum_word_incidence
    require(certificate_word_cover_lower_bound == 24,
            (chart, certificate_word_cover_lower_bound))
    return {
        "chart": chart,
        "support_stabilizer_order": len(actions),
        "labelled_packets": len(all_packets),
        "orbit_registry": orbits,
        "certificate_word_incidence_histogram": sorted(
            incidence_histogram.items()
        ),
        "maximum_certificates_containing_one_word": maximum_word_incidence,
        "certificate_word_cover_lower_bound":
            certificate_word_cover_lower_bound,
        "packet_word_count_histogram": sorted(
            packet_word_count_histogram.items()
        ),
        "spoiled_certificate_count_histogram": sorted(
            spoiled_histogram.items()
        ),
        "minimum_untouched_certificates": minimum_untouched,
        "worst_packet_records": worst_records,
        "covering_lemma": (
            "a fixed packet P spoils only the union of certificate incidence "
            "sets of its literal compatible word set W(P), hence at most "
            "max_word_incidence times |W(P)| certificates; any simultaneous "
            "off-axis repair must generate at least 24 distinct certificate "
            "words"
        ),
        "consequence": (
            "every parity-minimal three-cell colour triangle leaves a "
            "permanent-triangle Laurent unit unchanged"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    arguments = parser.parse_args()
    actual = sha256((ROOT / DEPENDENCY).read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            ("pinned dependency changed", actual, DEPENDENCY_SHA256))
    two = load(DEPENDENCY, "n8_support28_three_cell_two_cell_dependency")
    one = two.load(
        two.DEPENDENCY,
        "n8_support28_three_cell_one_cell_dependency",
    )
    one.pin_dependencies()
    base = one.load(
        "computations/audit_n8_support28_cube_cut_permanent_triangle_unit_independent.py",
        "n8_support28_three_cell_base",
    )
    pair_support = one.cut_support(base, base.CUBE_BITS)
    full_support = one.cut_support(base, one.FULL_TARGET_CUBE_BITS)
    all_packets = packets(base)
    charts = (
        chart_audit(two, one, base, "pair-target-12", pair_support, all_packets),
        chart_audit(two, one, base, "full-target-012", full_support, all_packets),
    )

    ledger = {
        "mode_independent": True,
        "dependency": {DEPENDENCY: DEPENDENCY_SHA256},
        "packet_definition": (
            "three disjoint ordered off-diagonal cells, one for each "
            "unordered colour pair 01, 02, 12"
        ),
        "charts": charts,
        "theorem": (
            "every parity-minimal three-cell colour triangle leaves a "
            "literal three-row Laurent unit on both affine support-28 "
            "target charts; exact source implies smaller diagonal support "
            "or a larger simultaneous off-axis support"
        ),
        "scalable_interface": (
            "associate to any off-axis packet its finite compatible even-word "
            "set W(P); permanent triangles survive unless the union of the "
            "corresponding word-incidence sets covers all 96 certificates"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))

    print("N=8 support-28 three-offdiagonal colour-triangle gate: PASS")
    print("mode", arguments.mode)
    for chart in charts:
        registry = chart["orbit_registry"]
        print(chart["chart"], "stabilizer / orbits / sizes",
              chart["support_stabilizer_order"], registry["orbits"],
              registry["orbit_size_histogram"])
        print("  word incidence / packet words",
              chart["certificate_word_incidence_histogram"],
              chart["packet_word_count_histogram"])
        print("  min untouched / spoiled hist",
              chart["minimum_untouched_certificates"],
              chart["spoiled_certificate_count_histogram"])
        print("  worst packets",
              len(chart["worst_packet_records"]),
              [record["source_labelled_packet"]
               for record in chart["worst_packet_records"][:4]])
    print("consequence: Laurent unit or diagonal support <= 47")
    print("sha256:", digest)


if __name__ == "__main__":
    main()

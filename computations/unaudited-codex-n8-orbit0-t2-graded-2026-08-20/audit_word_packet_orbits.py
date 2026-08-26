#!/usr/bin/env python3
"""Exact orbit census for the degree-24 / K-degree-16 T^2 source words.

This is a representation-level census only.  It derives the K grading of a
degree-20 multiplier times an eight-site hafnian generator and quotients the
word and (word, hafnian-term) packets by the full orbit-0 stabilizer.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
EXPORT_PATH = BRIDGE / "export_orbit0_cutoff_seed.py"
SPEC = importlib.util.spec_from_file_location("orbit0_export", EXPORT_PATH)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
BASE = EXPORT.BASE
OUT = HERE / "results_word_packet_orbits.json"

SELECTED = (
    (0, 0, 0, 0, 0, 0, 1, 1),
    (0, 0, 0, 0, 1, 1, 1, 1),
    (0, 0, 0, 0, 1, 1, 2, 2),
)


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def transform_word(word, action):
    sites, colours = EXPORT.STABILIZER[action]
    moved = [None] * BASE.N
    for site, colour in enumerate(word):
        moved[sites[site]] = colours[colour]
    return tuple(moved)


def word_orbit(word):
    return frozenset(transform_word(word, action)
                     for action in range(len(EXPORT.STABILIZER)))


def transform_matching(matching, action):
    sites, _colours = EXPORT.STABILIZER[action]
    return tuple(sorted(tuple(sorted((sites[left], sites[right])))
                        for left, right in matching))


def transform_packet(packet, action):
    word, matching = packet
    return transform_word(word, action), transform_matching(matching, action)


def packet_orbit(packet):
    return frozenset(transform_packet(packet, action)
                     for action in range(len(EXPORT.STABILIZER)))


def term_degree(word, matching):
    term = BASE.term_ids(word, matching)
    return BASE.row_degree(term, EXPORT.ANCHORS)


def equal_anchor_pairs(word):
    return sum(word[left] == word[right] for left, right in EXPORT.M0)


def name(word):
    return "".join(map(str, word))


def word_profile(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def main():
    require(len(EXPORT.STABILIZER) == 2304, "orbit-0 stabilizer changed")
    mixed_words = {tuple(word) for word in product(BASE.COLORS, repeat=BASE.N)
                   if len(set(word)) > 1}
    require(len(mixed_words) == 3**8 - 3, "mixed-word census changed")

    unseen = set(mixed_words)
    word_records = []
    word_to_representative = {}
    while unseen:
        seed = min(unseen)
        orbit = word_orbit(seed)
        require(orbit <= mixed_words, "mixed word orbit reached a pure word")
        representative = min(orbit)
        for word in orbit:
            word_to_representative[word] = representative
        histogram = Counter(term_degree(representative, matching)
                            for matching in BASE.PM8)
        equal_pairs = equal_anchor_pairs(representative)
        require(min(histogram) == 4 - equal_pairs,
                "minimum hafnian K-degree is not 4-equal-anchor-pairs")
        word_records.append({
            "representative": name(representative),
            "orbit_size": len(orbit),
            "word_profile": list(word_profile(representative)),
            "equal_anchor_pairs": equal_pairs,
            "hafnian_K_degree_histogram": dict(sorted(histogram.items())),
            "leading_hafnian_K_degree": min(histogram),
            "degree20_multiplier_K_degree_for_total_16": 16 - min(histogram),
        })
        unseen.difference_update(orbit)

    all_packets = {(word, matching) for word in mixed_words
                   for matching in BASE.PM8}
    unseen_packets = set(all_packets)
    packet_records = []
    word_packet_histogram = defaultdict(Counter)
    while unseen_packets:
        seed = min(unseen_packets)
        orbit = packet_orbit(seed)
        require(orbit <= all_packets, "packet orbit left source family")
        representative = min(orbit)
        word_rep = word_to_representative[representative[0]]
        degree = term_degree(*representative)
        packet_records.append({
            "word_orbit_representative": name(word_rep),
            "packet_representative_word": name(representative[0]),
            "packet_representative_matching": [list(edge)
                                                for edge in representative[1]],
            "orbit_size": len(orbit),
            "hafnian_K_degree": degree,
        })
        word_packet_histogram[name(word_rep)][degree] += 1
        unseen_packets.difference_update(orbit)

    selected = {}
    for template in SELECTED:
        representative = word_to_representative[template]
        record = next(item for item in word_records
                      if item["representative"] == name(representative))
        selected[name(template)] = {
            "canonical_word_orbit_representative": name(representative),
            "word_orbit_size": record["orbit_size"],
            "word_profile": record["word_profile"],
            "equal_anchor_pairs": record["equal_anchor_pairs"],
            "hafnian_K_degree_histogram":
                record["hafnian_K_degree_histogram"],
            "packet_orbit_histogram_by_K_degree": dict(sorted(
                word_packet_histogram[name(representative)].items())),
            "packet_orbits_total": sum(
                word_packet_histogram[name(representative)].values()),
        }

    leading_word_orbit_histogram = Counter(
        item["leading_hafnian_K_degree"] for item in word_records
    )
    result = {
        "status": "UNAUDITED exact finite stabilizer/source-family census",
        "ordinary_target_degree": 24,
        "ordinary_hafnian_degree": 4,
        "ordinary_multiplier_degree": 20,
        "target_port_degree": 2,
        "multiplier_port_degree_rule": (
            "degree 1 at (v,w_v), degree 2 at the other two ports"
        ),
        "target_K_degree": 16,
        "associated_graded_rule": (
            "for multiplier K-degree d, retain the hafnian component of "
            "K-degree 16-d; an individual leading column has "
            "d=16-min_K_degree(H_w)"
        ),
        "warning": (
            "individual leading columns do not include hidden initial forms "
            "from kernels in lower K-degrees; a sound full membership test "
            "must preserve those lower-kernel transfers or eliminate the "
            "whole degree-24 filtration"
        ),
        "stabilizer_order": len(EXPORT.STABILIZER),
        "mixed_words": len(mixed_words),
        "mixed_word_orbits": len(word_records),
        "word_orbits_by_leading_hafnian_K_degree": dict(sorted(
            leading_word_orbit_histogram.items())),
        "word_orbits": sorted(word_records,
                              key=lambda item: item["representative"]),
        "word_hafnian_term_packets": len(all_packets),
        "word_hafnian_term_packet_orbits": len(packet_records),
        "selected_cutoff8_word_orbits": selected,
        "packet_orbits": sorted(packet_records, key=lambda item: (
            item["word_orbit_representative"],
            item["hafnian_K_degree"],
            item["packet_representative_word"],
            item["packet_representative_matching"],
        )),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 T^2 word/packet census: PASS")
    print("mixed word orbits:", len(word_records))
    print("word-term packet orbits:", len(packet_records))
    print("selected:", json.dumps(selected, sort_keys=True))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()

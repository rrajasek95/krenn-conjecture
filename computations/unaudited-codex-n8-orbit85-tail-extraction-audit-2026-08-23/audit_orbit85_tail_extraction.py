#!/usr/bin/env python3
"""Exact bounded provenance audit for the orbit-85 diagonal-to-tail interface."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CERT = (ROOT / "computations" /
        "unaudited-codex-n8-diagonal-orbit85-extended-certificate-2026-08-23" /
        "certificate_dag.json")
GENERATOR = CERT.with_name("generate_certificate.py")
ENCODER = ROOT / "computations" / "verify_eight_site_diagonal_obstruction.py"
TAIL_REPORT = (ROOT / "computations" /
               "unaudited-codex-tail-polar-source-lift-2026-08-21" /
               "REPORT.md")
OUT = HERE / "results_orbit85_tail_extraction.json"
EXPECTED = {
    CERT: "d5effbf6447c7b74b8bcd9ae1370bc2e498f15cd8e95fae60576cf657907db96",
    GENERATOR: "70a1060e9410c763579883d07ff1ad4ec798c97e0412d6184cf936da129390ac",
    ENCODER: "b7540367b6c28da13b4dce5b3e9fe4658acfef162a268c4ffc7cb6d15dc51b2a",
    TAIL_REPORT: "e9b23050985929d0ed1776c26341fd50782bee1ef7e60ff18bc9983a7dbd2c6d",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            answer.append(((first, second),) + matching)
    return tuple(answer)


MATCHINGS = perfect_matchings(range(8))


def word_from_masks(masks):
    word = [None] * 8
    for colour, mask in enumerate(masks):
        for site in range(8):
            if mask & (1 << site):
                require(word[site] is None, (masks, site))
                word[site] = colour
    require(all(colour is not None for colour in word), masks)
    return tuple(word)


def matching_census(word):
    degree_counts = Counter()
    signatures = defaultdict(set)
    for matching in MATCHINGS:
        crossing = []
        for left, right in matching:
            if word[left] != word[right]:
                crossing.append(tuple(sorted((word[left], word[right]))))
        degree_counts[len(crossing)] += 1
        signatures[len(crossing)].add(tuple(sorted(crossing)))
    return dict(sorted(degree_counts.items())), {
        str(degree): [["".join(map(str, pair)) for pair in signature]
                      for signature in sorted(values)]
        for degree, values in sorted(signatures.items())
    }


def profile_from_masks(masks):
    return tuple(sorted((mask.bit_count() for mask in masks), reverse=True))


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    certificate = json.loads(CERT.read_text())
    if mutate:
        certificate["tail_interface"]["first_possible_order"] = 1

    require(certificate["stats"]["antecedent_equations"] == 13670,
            "antecedent count drift")
    require(certificate["tail_interface"]["first_possible_order"] == 2,
            "tail-order mutation/source drift")
    antecedents = {row["id"]: row for row in certificate["antecedents"]}
    antecedent_counts = Counter(row["kind"] for row in antecedents.values())
    require(antecedent_counts == Counter({
        "boolean_axiom": 5592,
        "laplace_witness_definition": 5208,
        "mixed_diagonal_amplitude": 1638,
        "inside_free_product_zero": 448,
        "selector_zero_link": 384,
        "selector_guarded_inverse": 384,
        "unguarded_open_localizer": 9,
        "outside_free_complement_localizer": 7,
    }), antecedent_counts)

    core_families = Counter()
    reference_kinds = Counter()
    amplitude_references = []
    for node in certificate["proof_nodes"]:
        if node["op"] != "compile_clause":
            continue
        core_families[node["compiler"]["schema"]] += 1
        for reference in node["compiler"]["antecedents"]:
            kind = antecedents[reference]["kind"]
            reference_kinds[kind] += 1
            if kind == "mixed_diagonal_amplitude":
                amplitude_references.append(reference)
    require(core_families == Counter({
        "A3g": 308, "FR": 93, "A3": 59, "A2": 25, "XF": 6,
        "C0": 5, "Ch": 3, "A1": 2, "Cnz": 1,
    }), core_families)
    require((len(amplitude_references), len(set(amplitude_references)))
            == (569, 185), "amplitude reference census drift")

    representative_words = {
        "620": (0, 0, 0, 0, 0, 0, 1, 1),
        "440": (0, 0, 0, 0, 1, 1, 1, 1),
        "422": (0, 0, 0, 0, 1, 1, 2, 2),
        "611": (0, 1, 2, 2, 2, 2, 2, 2),
        "332": (0, 0, 0, 1, 1, 1, 2, 2),
        "71": (0, 0, 0, 0, 0, 0, 0, 1),
    }
    representative_census = {}
    for name, word in representative_words.items():
        counts, signatures = matching_census(word)
        representative_census[name] = {
            "word": "".join(map(str, word)),
            "tail_degree_counts": {str(key): value
                                   for key, value in counts.items()},
            "cross_colour_signatures": signatures,
        }
    require(representative_census["620"]["tail_degree_counts"]
            == {"0": 15, "2": 90}, "620 census drift")
    require(representative_census["440"]["tail_degree_counts"]
            == {"0": 9, "2": 72, "4": 24}, "440 census drift")
    require(representative_census["422"]["tail_degree_counts"]
            == {"0": 3, "2": 30, "3": 48, "4": 24}, "422 census drift")
    require(representative_census["611"]["tail_degree_counts"]
            == {"1": 15, "2": 90}, "611 census drift")
    require(representative_census["332"]["tail_degree_counts"]
            == {"1": 9, "2": 18, "3": 42, "4": 36}, "332 census drift")
    require(representative_census["71"]["tail_degree_counts"]
            == {"1": 105}, "71 census drift")

    distinct_profiles = Counter()
    occurrence_profiles = Counter()
    for identifier in set(amplitude_references):
        masks = tuple(map(int, identifier.split(":")[1:]))
        distinct_profiles[profile_from_masks(masks)] += 1
        counts, _ = matching_census(word_from_masks(masks))
        require(1 not in counts and counts.get(2, 0) > 0,
                f"bad even leaf tail order: {identifier}/{counts}")
    for identifier in amplitude_references:
        masks = tuple(map(int, identifier.split(":")[1:]))
        occurrence_profiles[profile_from_masks(masks)] += 1
    require(distinct_profiles == Counter({(4, 2, 2): 154,
                                          (6, 2, 0): 22,
                                          (4, 4, 0): 9}), distinct_profiles)
    require(occurrence_profiles == Counter({(4, 2, 2): 514,
                                            (6, 2, 0): 46,
                                            (4, 4, 0): 9}), occurrence_profiles)

    result = {
        "status": "PASS bounded orbit85 diagonal-to-tail provenance audit",
        "antecedent_epsilon_orders": {
            "mixed_diagonal_amplitude": {
                "count": 1638,
                "constant_term": "product of diagonal colour-class Hafnians",
                "first_positive_order": 2,
                "reason": "all three colour-class sizes are even",
            },
            "boolean_axiom": {"count": 5592, "tail_dependence": "none"},
            "selector_zero_link": {"count": 384, "tail_dependence": "none"},
            "selector_guarded_inverse": {"count": 384, "tail_dependence": "none"},
            "laplace_witness_definition": {"count": 5208,
                                             "tail_dependence": "none"},
            "inside_free_product_zero": {
                "count": 448,
                "tail_dependence": "none in the fixed constructible branch",
                "scope_guard": (
                    "these are diagonal branch equations P_j=0, not full "
                    "eight-site X5 amplitude leaves; replacing them by full "
                    "amplitudes would require a separate localized source derivation"
                ),
            },
            "outside_free_complement_localizer": {"count": 7,
                                                   "tail_dependence": "none"},
            "unguarded_open_localizer": {"count": 9,
                                          "tail_dependence": "none"},
        },
        "core_compilation": {
            "clause_family_counts": dict(sorted(core_families.items())),
            "antecedent_reference_counts": dict(sorted(reference_kinds.items())),
            "tail_sensitive_clause_families": {
                "A2": 25, "C0": 5, "XF_via_C0": 6,
            },
            "mixed_amplitude_occurrences": len(amplitude_references),
            "distinct_mixed_amplitude_leaves": len(set(amplitude_references)),
            "distinct_profile_counts": {
                "+".join(map(str, key)): value
                for key, value in sorted(distinct_profiles.items())
            },
            "occurrence_profile_counts": {
                "+".join(map(str, key)): value
                for key, value in sorted(occurrence_profiles.items())
            },
        },
        "representative_matching_census": representative_census,
        "tail2": {
            "formula": (
                "sum over matchings with exactly two cross-colour edges of "
                "the two T cells times the two remaining diagonal edge factors"
            ),
            "terms_per_leaf_profile": {"6+2+0": 90,
                                       "4+4+0": 72,
                                       "4+2+2": 30},
            "colour_incidence": (
                "two parallel edges in one unordered colour pair; every colour "
                "has even crossing degree"
            ),
        },
        "comparison_with_frozen_tail_packets": {
            "matches_611_332_or_carrier_initial_packet": False,
            "reason": (
                "the frozen 7+1, 6+1+1, and 3+3+2 response rows have odd "
                "colour-count parity and begin at epsilon order 1; orbit85 "
                "uses all-even 6+2+0, 4+4+0, 4+2+2 rows and begins at order 2"
            ),
            "611_quadratic_guard": (
                "the quadratic remainder of a 6+1+1 row has a two-edge colour "
                "path (02,12), whereas every orbit85 Tail2 monomial has a "
                "doubled/parallel colour pair (01,01), (02,02), or (12,12)"
            ),
            "closest_existing_description": (
                "the all-even second-tail/second-fundamental layer of the "
                "zero-tail 620/440/422 packet, not the 380-row polar matrix"
            ),
        },
        "global_circuit_guard": (
            "The certificate freezes a high-level order-2 circuit but not an "
            "expanded nonzero C2 polynomial. Thus order 2 is the first possible "
            "global correction; cancellation inside the complete DAG has not "
            "been excluded by this bounded audit."
        ),
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.check_results:
        require(OUT.exists() and json.loads(OUT.read_text()) == result,
                "stored result drift")
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print("amplitude leaves", result["core_compilation"]["mixed_amplitude_occurrences"],
          result["core_compilation"]["distinct_mixed_amplitude_leaves"])
    print("first possible epsilon order 2; matches frozen polar packet false")
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()

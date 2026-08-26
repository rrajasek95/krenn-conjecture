#!/usr/bin/env python3
"""Support-only diagonal-packet filter for all monomial-prime orbits.

This checker deliberately does not solve coefficients.  It only uses the
literal monomial supports of the six permanent rows, four triangle rows,
and the three already-imposed zero cofactors h_c,06.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
UPSTREAM = HERE / "results_single_boundary_monomial_primes.json"
OUT = HERE / "results_prime_support_filter.json"
VERTICES = tuple(range(8))
SUPER_EDGES = tuple(combinations(range(4), 2))
TRIPLES = tuple(combinations(range(4), 3))
COMPLEMENT = (1, 2, 3, 4, 5, 7)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        answer.extend((((first, second),) + tail
                       for tail in perfect_matchings(rest)))
    return tuple(answer)


def physical_edge(i, j, clone_i, clone_j):
    return tuple(sorted((2*i + clone_i, 2*j + clone_j)))


def parse_generator(label):
    # The sites are single decimal digits throughout this N=8 artifact.
    require(label[0] == "g" and label[1].isdigit()
            and label[2] == "_" and len(label) == 5,
            ("unexpected generator label", label))
    return int(label[1]), tuple(sorted((int(label[3]), int(label[4]))))


def live(term, zeros):
    return not any(edge in zeros for edge in term)


def support_test(record):
    zeros_by_colour = {colour: set() for colour in range(3)}
    for label in record["prime_generators"]:
        colour, edge = parse_generator(label)
        zeros_by_colour[colour].add(edge)

    failures = []
    diagnostics = {}
    for colour, zeros in zeros_by_colour.items():
        permanent_counts = []
        for i, j in SUPER_EDGES:
            terms = (
                (physical_edge(i, j, 0, 0),
                 physical_edge(i, j, 1, 1)),
                (physical_edge(i, j, 0, 1),
                 physical_edge(i, j, 1, 0)),
            )
            count = sum(live(term, zeros) for term in terms)
            permanent_counts.append(count)
            if count == 0:
                failures.append(f"g{colour}:permanent_{i}{j}:zero_live")

        triangle_counts = []
        for i, j, k in TRIPLES:
            terms = tuple((
                physical_edge(i, j, ci, cj),
                physical_edge(i, k, 1-ci, ck),
                physical_edge(j, k, 1-cj, 1-ck),
            ) for ci, cj, ck in product((0, 1), repeat=3))
            count = sum(live(term, zeros) for term in terms)
            triangle_counts.append(count)
            if count == 0:
                failures.append(f"g{colour}:triangle_{i}{j}{k}:zero_live")

        cofactor_terms = tuple(tuple(tuple(sorted(edge)) for edge in matching)
                               for matching in perfect_matchings(COMPLEMENT))
        cofactor_count = sum(live(term, zeros) for term in cofactor_terms)
        if cofactor_count == 1:
            failures.append(f"g{colour}:h_06:one_live")
        diagnostics[str(colour)] = {
            "permanent_live_term_counts": permanent_counts,
            "triangle_live_term_counts": triangle_counts,
            "h_06_live_term_count": cofactor_count,
        }
    # The chart is not merely h2_06=0: it inverts the other eleven h2_at.
    # A zero live-term count therefore rejects the support before any
    # coefficient solve.  Keep this separate from the packet filter so the
    # unique pre-localization survivor remains visible in the ledger.
    localized_h2_counts = {}
    localization_failures = []
    zeros = zeros_by_colour[2]
    for tail in (6, 7):
        for site in range(6):
            remaining = tuple(vertex for vertex in VERTICES
                              if vertex not in (site, tail))
            terms = tuple(tuple(tuple(sorted(edge)) for edge in matching)
                          for matching in perfect_matchings(remaining))
            count = sum(live(term, zeros) for term in terms)
            label = f"h2_{site}{tail}"
            localized_h2_counts[label] = count
            if (site, tail) != (0, 6) and count == 0:
                localization_failures.append(label + ":zero_support_but_inverted")
    return (failures, diagnostics, localization_failures,
            localized_h2_counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()

    upstream = json.loads(UPSTREAM.read_text())
    require(upstream["logical_sha256"] ==
            "af23ec140df2b126af7195b65aff62f9f489805e4509328794438c98a80efc8c",
            "minimal-prime upstream digest changed")
    records = upstream["site_stabilizer_quotient"]["orbit_representatives"]
    require(len(records) == 527, "site-orbit count changed")

    packet_survivors = []
    localized_survivors = []
    rejected = []
    localization_rejected = []
    rejection_reason_histogram = Counter()
    for record in records:
        (failures, diagnostics, localization_failures,
         localized_h2_counts) = support_test(record)
        row = {
            "full_prime_height": record["full_prime_height"],
            "orbit_size": record["orbit_size"],
            "prime_generators": record["prime_generators"],
            "diagnostics": diagnostics,
            "localized_h2_live_term_counts": localized_h2_counts,
        }
        if failures:
            row["failures"] = failures
            rejected.append(row)
            rejection_reason_histogram.update(failure.split(":", 1)[1]
                                              for failure in failures)
        else:
            packet_survivors.append(row)
            if localization_failures:
                row["localization_failures"] = localization_failures
                localization_rejected.append(row)
            else:
                localized_survivors.append(row)

    survivor_orbits_by_height = Counter(
        row["full_prime_height"] for row in packet_survivors)
    survivor_labelled_primes_by_height = Counter()
    for row in packet_survivors:
        survivor_labelled_primes_by_height[row["full_prime_height"]] += (
            row["orbit_size"])
    rejected_orbits_by_height = Counter(
        row["full_prime_height"] for row in rejected)
    require(len(packet_survivors) == 1
            and len(localization_rejected) == 1
            and not localized_survivors,
            "support/localization survivor census changed")
    require(packet_survivors[0]["localized_h2_live_term_counts"] == {
        "h2_06": 0, "h2_16": 6, "h2_26": 6,
        "h2_36": 0, "h2_46": 6, "h2_56": 0,
        "h2_07": 6, "h2_17": 12, "h2_27": 12,
        "h2_37": 6, "h2_47": 12, "h2_57": 6,
    }, "last-orbit cofactor support profile changed")

    result = {
        "status": "PASS exact support-only diagonal packet filter",
        "input_site_orbits": len(records),
        "filter": {
            "nonzero_target_rows": (
                "for each colour, reject if either-term permanent support "
                "or eight-term reduced triangle support is empty"),
            "zero_target_rows": (
                "for each colour, reject if the imposed 15-term h_c,06 "
                "support has exactly one live monomial"),
            "coefficient_solves": 0,
        },
        "rejected_orbit_count": len(rejected),
        "packet_survivor_orbit_count_before_Dhat": len(packet_survivors),
        "Dhat_rejected_orbit_count": len(localization_rejected),
        "survivor_orbit_count_on_declared_chart": len(localized_survivors),
        "survivor_orbits_by_full_height": {
            str(height): count for height, count
            in sorted(survivor_orbits_by_height.items())
        },
        "survivor_labelled_primes_by_full_height": {
            str(height): count for height, count
            in sorted(survivor_labelled_primes_by_height.items())
        },
        "rejected_orbits_by_full_height": {
            str(height): count for height, count
            in sorted(rejected_orbits_by_height.items())
        },
        "rejection_reason_histogram": dict(
            sorted(rejection_reason_histogram.items())),
        "packet_survivor_orbit_representatives": packet_survivors,
        "localized_survivor_orbit_representatives": localized_survivors,
        "Dhat_terminal": (
            "The sole packet survivor has identically zero h2_36 and h2_56 "
            "support, whereas Dhat inverts both; hence no minimal-prime "
            "orbit meets the declared single-cofactor chart."),
        "scope_guard": (
            "Support compatibility is only necessary. A surviving orbit "
            "has not been shown to admit coefficients satisfying the rows."),
        "source_hashes": {"minimal_prime_result": file_hash(UPSTREAM)},
    }
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("prime support filter: PASS", result["logical_sha256"])
    print("packet/localized orbit survivors", len(packet_survivors),
          len(localized_survivors), "of", len(records))
    print("survivor orbits by height", dict(sorted(
        survivor_orbits_by_height.items())))
    print("survivor labelled primes by height", dict(sorted(
        survivor_labelled_primes_by_height.items())))


if __name__ == "__main__":
    main()

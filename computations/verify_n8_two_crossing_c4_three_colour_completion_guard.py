#!/usr/bin/env python3
"""Close the first two-crossing nonlift under literal C4 source rows.

The first nonlift in the conditioned SP-K6 gate is

    a01^00 a23^00 (a45^01 a67^22 + a46^02 a57^12).

The canonical parent packet already contains a45^00 and a45^21.  Their
literal output rows are singletons unless the C4 is enlarged.  This checker
enumerates the complete ordered-endpoint-colour C4 fibre, the minimum
singleton-free enlargements after adding the third matching, and every
support-minimum three-pure completion at order eight.

The minimum mixed closure has two binomial rows and one contaminated
trinomial row.  It has an all-unit point and is not the K2,3 permanent
triangle.  Every one of its 3,150 support-minimum pure completions has a
mixed singleton (at least nine), so any full GHZ completion must leave the
minimum stratum by adding a further labelled mate.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_c6_transverse_seed_spk6_certificate_lift_gate.py":
        "a46d212cc4ac1ddbd794c0e3eb163b342fccbd040619c0e9e6fe3fbe5d355270",
    "notes/2026-08-14-c6-transverse-seed-conditioned-spk6-certificate-lift.md":
        "bfa3b69d5287d8e4b13de32a844b305806d8cc1d74b41a6b173dc3d3e68236a5",
    "computations/verify_uniform_permanent_triangle_common_tail_unit_lemma.py":
        "1431e0aebfe1ce0a85f4e38aec6ff66c6efc0cc75d0caae2c5c9341b5fb50900",
    "notes/uniform-permanent-triangle-common-tail-unit-lemma.md":
        "404f468fc9fd642af4dba13b8d96c8ce9bd39ad8fee05133e05f2b16de4a298e",
}

COLOURS = tuple(range(3))
SITES = tuple(range(8))
LOCAL_SITES = (4, 5, 6, 7)
TAIL = {(0, 1, 0, 0), (2, 3, 0, 0)}

P0 = ((4, 5), (6, 7))
P1 = ((4, 6), (5, 7))
P2 = ((4, 7), (5, 6))
LOCAL_MATCHINGS = (P0, P1, P2)

# Ordered endpoint colours: a45^21 means colour 2 at site 4 and colour 1
# at site 5.  Sorting these pairs would change the physical source word.
BASE_LOCAL = {
    (4, 5, 0, 0),
    (4, 5, 0, 1),
    (4, 5, 2, 1),
    (6, 7, 2, 2),
    (4, 6, 0, 2),
    (5, 7, 1, 2),
}
THIRD_MATCHING = {
    (4, 7, 0, 2),
    (5, 6, 1, 2),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(SITES)))


def cell_name(cell):
    left, right, alpha, beta = cell
    return f"a{left}{right}^{alpha}{beta}"


def word_name(word):
    return "".join(map(str, word))


def matching_name(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def occurrence_cells(matching, word):
    return {(left, right, word[left], word[right])
            for left, right in matching}


def local_fibres(support):
    fibres = {}
    for local_word in product(COLOURS, repeat=4):
        word = {site: local_word[site - 4] for site in LOCAL_SITES}
        live = []
        for index, matching in enumerate(LOCAL_MATCHINGS):
            cells = {(left, right, word[left], word[right])
                     for left, right in matching}
            if cells <= support:
                live.append(index)
        if live:
            fibres[word_name(local_word)] = tuple(live)
    return fibres


def occurrence_counts(support):
    """Count all supported eight-site occurrences without scanning 3^8."""
    decorations = defaultdict(list)
    for left, right, alpha, beta in support:
        decorations[(left, right)].append((alpha, beta))
    counts = Counter()
    fines = defaultdict(list)
    for matching in MATCHINGS:
        choices = [decorations[edge] for edge in matching]
        if any(not choice for choice in choices):
            continue
        for colours in product(*choices):
            word = [None] * 8
            for (left, right), (alpha, beta) in zip(
                    matching, colours, strict=True):
                word[left] = alpha
                word[right] = beta
            word = tuple(word)
            counts[word] += 1
            fines[word].append(matching_name(matching))
    return counts, fines


def mixed_closure():
    base_fibres = local_fibres(BASE_LOCAL)
    require(base_fibres == {
        "0022": (0,),
        "0122": (0, 1),
        "2122": (0,),
    }, base_fibres)

    with_third = BASE_LOCAL | THIRD_MATCHING
    third_fibres = local_fibres(with_third)
    require(third_fibres == {
        "0022": (0,),
        "0122": (0, 1, 2),
        "2122": (0,),
    }, third_fibres)

    universe = {
        (left, right, alpha, beta)
        for left, right in ((4, 5), (4, 6), (4, 7),
                            (5, 6), (5, 7), (6, 7))
        for alpha in COLOURS for beta in COLOURS
    }
    candidates = tuple(sorted(universe - with_third))

    solutions = []
    completion_counts = {}
    for size in range(3):
        current = []
        for additions in combinations(candidates, size):
            fibres = local_fibres(with_third | set(additions))
            if all(len(live) != 1 for live in fibres.values()):
                current.append(additions)
        completion_counts[size] = len(current)
        if current:
            solutions = current
            break
    expected_solutions = (
        ((4, 6, 2, 2), (5, 6, 0, 2)),
        ((4, 7, 2, 2), (5, 7, 0, 2)),
    )
    require(tuple(solutions) == expected_solutions, solutions)
    require(completion_counts == {0: 0, 1: 0, 2: 2}, completion_counts)

    canonical = with_third | set(solutions[0])
    canonical_fibres = local_fibres(canonical)
    require(canonical_fibres == {
        "0022": (0, 2),
        "0122": (0, 1, 2),
        "2122": (0, 1),
    }, canonical_fibres)

    # The three complete mixed rows after factoring the unit tail T are
    # AD+GJ, BD+EF+GH, CD+IF.  The following point keeps every cell nonzero.
    point = {
        "A": Fraction(-1), "B": Fraction(-2), "C": Fraction(-1),
        "D": Fraction(1), "E": Fraction(1), "F": Fraction(1),
        "G": Fraction(1), "H": Fraction(1), "I": Fraction(1),
        "J": Fraction(1),
    }
    row_values = (
        point["A"] * point["D"] + point["G"] * point["J"],
        point["B"] * point["D"] + point["E"] * point["F"]
        + point["G"] * point["H"],
        point["C"] * point["D"] + point["I"] * point["F"],
    )
    require(row_values == (0, 0, 0), row_values)
    require(all(point.values()), point)

    # Permanent-triangle rows have four variables each and empty triple
    # intersection.  Here D occurs in all three rows, and the middle row has
    # six variables.  More decisively, the displayed Laurent point exists.
    candidate_rows = (
        frozenset(("A", "D", "G", "J")),
        frozenset(("B", "D", "E", "F", "G", "H")),
        frozenset(("C", "D", "I", "F")),
    )
    permanent_rows = (
        frozenset(("a", "e", "b", "d")),
        frozenset(("a", "f", "c", "d")),
        frozenset(("b", "f", "c", "e")),
    )
    incidence = {
        "candidate_row_sizes": tuple(map(len, candidate_rows)),
        "candidate_triple_intersection": len(set.intersection(
            *map(set, candidate_rows))),
        "permanent_row_sizes": tuple(map(len, permanent_rows)),
        "permanent_triple_intersection": len(set.intersection(
            *map(set, permanent_rows))),
    }
    require(incidence == {
        "candidate_row_sizes": (4, 6, 4),
        "candidate_triple_intersection": 1,
        "permanent_row_sizes": (4, 4, 4),
        "permanent_triple_intersection": 0,
    }, incidence)

    full_support = TAIL | canonical
    counts, fines = occurrence_counts(full_support)
    nonempty = {
        word_name(word): (count, tuple(sorted(fines[word])))
        for word, count in sorted(counts.items())
    }
    expected_nonempty = {
        "00000022": (2, ("01|23|45|67", "01|23|47|56")),
        "00000122": (3, ("01|23|45|67", "01|23|46|57",
                           "01|23|47|56")),
        "00002122": (2, ("01|23|45|67", "01|23|46|57")),
    }
    require(nonempty == expected_nonempty, nonempty)

    return {
        "base_ordered_endpoint_cells": tuple(map(cell_name,
                                                   sorted(BASE_LOCAL))),
        "base_complete_source_rows": base_fibres,
        "third_matching_cells": tuple(map(cell_name,
                                            sorted(THIRD_MATCHING))),
        "rows_after_third_matching": third_fibres,
        "minimum_no_singleton_additions": 2,
        "minimum_completion_counts": completion_counts,
        "minimum_completions": tuple(
            tuple(map(cell_name, solution)) for solution in solutions),
        "canonical_complete_rows": canonical_fibres,
        "global_word_fine_rows": nonempty,
        "factored_equations": (
            "T*(A*D + G*J)",
            "T*(B*D + E*F + G*H)",
            "T*(C*D + I*F)",
        ),
        "variable_dictionary": {
            "T": "a01^00*a23^00", "A": "a45^00",
            "B": "a45^01", "C": "a45^21", "D": "a67^22",
            "E": "a46^02", "F": "a57^12", "G": "a47^02",
            "H": "a56^12", "I": "a46^22", "J": "a56^02",
        },
        "all_unit_point": {key: str(value) for key, value in point.items()},
        "all_unit_row_values": tuple(map(str, row_values)),
        "permanent_triangle_comparison": incidence,
        "verdict": (
            "the other endpoint-colour rows force repairs; their minimum "
            "closed packet reproduces two operation-labelled C4 "
            "anti-diagonals around one contaminated anti-diagonal, not the "
            "K2,3 permanent triangle"
        ),
    }, tuple(TAIL | canonical for canonical in (
        with_third | set(solutions[0]),
        with_third | set(solutions[1]),
    ))


EXPECTED_PURE_HISTOGRAM = {
    9: 32, 10: 64, 11: 112, 12: 232, 13: 208, 14: 232,
    15: 240, 16: 152, 17: 192, 18: 192, 19: 224, 20: 112,
    21: 144, 22: 168, 23: 80, 24: 134, 25: 64, 26: 48,
    27: 134, 28: 64, 29: 16, 30: 70, 31: 8, 32: 8, 33: 26,
    35: 8, 36: 32, 39: 24, 42: 30, 45: 32, 47: 6, 48: 16,
    51: 8, 52: 6, 54: 8, 57: 10, 60: 8, 78: 3, 87: 1,
    96: 1, 105: 1,
}


def pure_completion_census(mixed_supports):
    records = []
    histograms = []
    for section, support in enumerate(mixed_supports):
        candidates = []
        missing_counts = []
        for colour in COLOURS:
            choices = []
            for matching in MATCHINGS:
                additions = {
                    (left, right, colour, colour)
                    for left, right in matching
                } - support
                choices.append((len(additions), matching, additions))
            minimum = min(item[0] for item in choices)
            candidates.append(tuple((matching, additions)
                                    for size, matching, additions in choices
                                    if size == minimum))
            missing_counts.append(minimum)
        require(tuple(map(len, candidates)) == (1, 105, 30),
                tuple(map(len, candidates)))
        require(tuple(missing_counts) == (1, 4, 3), missing_counts)

        histogram = Counter()
        section_records = []
        for matching0, additions0 in candidates[0]:
            for matching1, additions1 in candidates[1]:
                for matching2, additions2 in candidates[2]:
                    completed = support | additions0 | additions1 | additions2
                    counts, fines = occurrence_counts(completed)
                    pure_counts = tuple(counts[(colour,) * 8]
                                        for colour in COLOURS)
                    require(pure_counts == (1, 1, 1), pure_counts)
                    singletons = tuple(sorted(
                        word for word, count in counts.items()
                        if count == 1 and len(set(word)) > 1
                    ))
                    require(singletons, (section, matching1, matching2))
                    histogram[len(singletons)] += 1
                    first = singletons[0]
                    section_records.append({
                        "pure1": matching_name(matching1),
                        "pure2": matching_name(matching2),
                        "mixed_singletons": len(singletons),
                        "first_word": word_name(first),
                        "first_fine": fines[first][0],
                    })
        require(dict(sorted(histogram.items())) == EXPECTED_PURE_HISTOGRAM,
                (section, histogram))
        require(len(section_records) == 3150, len(section_records))
        histograms.append(dict(sorted(histogram.items())))
        records.append({
            "section": section,
            "completion_count": len(section_records),
            "minimum_new_diagonal_cells_by_colour": tuple(missing_counts),
            "pure_matching_choice_counts": tuple(map(len, candidates)),
            "minimum_mixed_singletons": min(histogram),
            "canonical_minimum_record": min(
                section_records,
                key=lambda item: (item["mixed_singletons"], item["pure1"],
                                  item["pure2"], item["first_word"]),
            ),
        })
    require(histograms[0] == histograms[1], histograms)
    serialized = json.dumps(records, sort_keys=True, separators=(",", ":"))
    return {
        "two_minimum_mixed_sections": tuple(records),
        "singleton_histogram_each_section": histograms[0],
        "support_minimum_full_GHZ_verdict": (
            "all 3150 minimum pure completions in each mixed section have "
            "a mixed singleton, so they generate a localized unit"
        ),
        "nonminimum_escape": (
            "an arbitrary full source can add further cancellation cells; "
            "the first displayed singleton requires a new labelled P1 or "
            "P2 mate and is the remaining repair branch"
        ),
        "record_sha256": sha256(serialized.encode()).hexdigest(),
    }


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    closure, mixed_supports = mixed_closure()
    pure = pure_completion_census(mixed_supports)
    return {
        "theorem": "two-crossing C4 three-colour completion guard",
        "pins": PINS,
        "mixed_C4_completion": closure,
        "support_minimum_pure_completion": pure,
        "scope": (
            "exact for all occurrence-labelled rows supported on the named "
            "12-cell packet and for every support-minimum pure completion; "
            "not a proof against arbitrary nonminimum repairs and not an "
            "active-cap or full tensor descent theorem"
        ),
    }


EXPECTED_LEDGER_SHA256 = "a8802aee3f284196caf7708c95730744ce5e4916a6e0d8bec3d80ce9db74a50a"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    args = parser.parse_args()
    ledger = build_ledger()
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    print("N8 two-crossing C4 three-colour completion guard: PASS")
    print("mode", args.mode)
    print("ledger_sha256", digest)
    print("minimum mixed closure: 10 C4 cells, two sections")
    print("permanent triangle: no; all-unit contaminated anti-diagonal guard")
    print("minimum pure completions: 3150 per section, singleton minimum 9")


if __name__ == "__main__":
    main()

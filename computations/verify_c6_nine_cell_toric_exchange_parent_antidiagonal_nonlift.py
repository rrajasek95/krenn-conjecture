#!/usr/bin/env python3
"""Toric exchange versus physical EqSystem on the exact nine-cell guard.

The unlabelled K6 edge torus has a very short exchange chain between the
long cap parent M0, the short cap parent M1, and the cap-avoiding escape N.
This checker enumerates the complete degree-three and degree-four toric
fibres, the minimal C4 chain, every one of the 729 physical coefficient
rows, and the literal word/fine/operation labels.

The first exchange does not lift.  The toric C4 binomial is M0-M1, while
the hafnian mixed row is the signless sum M0+M1.  The binomial evaluates to
4 on the exact rational guard.  No pointwise-vanishing degree-three toric
edge or live degree-four multiple is incident to any of M0,M1,N.  Hence the
parent anti-diagonal is present only after adjoining a nonphysical toric
equation, not as an EqSystem row.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_forced_pure_escape_alternating_potential.py":
        "3cdf461b422f8b29af5f9cd8948132ac1edb8dfd92798f6678e5644e4d2fb514",
    "notes/2026-08-14-forced-pure-escape-alternating-potential.md":
        "b3a10f916b27cb655f9f4f92504d5a771e667dca84beecfe728e9a2532d14868",
    "computations/verify_escape_parent_selector_marked_carrier_comparison.py":
        "8b33515eebc4ae3460a083bb5e6c0966926ce1d83bddd6895dd59f20412f937a",
    "notes/2026-08-14-escape-parent-selector-marked-carrier-comparison.md":
        "c1626482c0bf944e16c8c4b58b173b0a168668192d0a5afe6969edf13598e452",
}


N = 6
COLOURS = tuple(range(3))
VERTICES = tuple(range(N))
WORDS = tuple(product(COLOURS, repeat=N))
EDGES = tuple((left, right) for left in VERTICES
              for right in VERTICES if left < right)
EDGE_INDEX = {endpoints: index for index, endpoints in enumerate(EDGES)}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return

    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(VERTICES)))
M0 = tuple(sorted((edge(0, 5), edge(1, 2), edge(3, 4))))
M1 = tuple(sorted((edge(0, 1), edge(2, 5), edge(3, 4))))
ESCAPE = tuple(sorted((edge(0, 1), edge(2, 3), edge(4, 5))))
LIVE_MATCHINGS = (M0, M1, ESCAPE)


def matching_name(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def word_name(word):
    return "".join(map(str, word))


def rational_rank(rows):
    matrix = [list(map(Fraction, row)) for row in rows]
    if not matrix:
        return 0
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(rank, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [left - scale * right
                           for left, right in zip(matrix[row], matrix[rank],
                                                  strict=True)]
        rank += 1
    return rank


def cell(endpoints, colour):
    return endpoints, colour


def guard_weights():
    return {
        cell(edge(3, 4), 0): Fraction(1),
        cell(edge(3, 4), 1): Fraction(1),
        cell(edge(3, 4), 2): Fraction(1),
        cell(edge(0, 5), 1): Fraction(2),
        cell(edge(1, 2), 1): Fraction(1),
        cell(edge(0, 1), 1): Fraction(-2),
        cell(edge(2, 5), 1): Fraction(1),
        cell(edge(2, 3), 1): Fraction(-1, 2),
        cell(edge(4, 5), 1): Fraction(1),
    }


def occurrence_cells(matching, word):
    if any(word[left] != word[right] for left, right in matching):
        return None
    return tuple(cell(endpoints, word[endpoints[0]])
                 for endpoints in matching)


def complete_eqsystem_rows(weights):
    rows = {}
    for word in WORDS:
        occurrences = []
        for matching in MATCHINGS:
            cells = occurrence_cells(matching, word)
            if cells is None or not all(selected in weights for selected in cells):
                continue
            value = Fraction(1)
            for selected in cells:
                value *= weights[selected]
            occurrences.append((matching, cells, value))
        target = Fraction(int(len(set(word)) == 1))
        total = sum((item[2] for item in occurrences), Fraction(0))
        rows[word] = {
            "occurrences": tuple(occurrences),
            "lhs": total,
            "target": target,
            "equation_value": total - target,
        }
    return rows


def physical_row_audit():
    weights = guard_weights()
    rows = complete_eqsystem_rows(weights)
    nonempty = tuple(word for word, row in rows.items()
                     if row["occurrences"])
    require(tuple(map(word_name, nonempty)) ==
            ("111001", "111111", "111221"), nonempty)
    expected = {
        "111001": ((M1, Fraction(-2)), (M0, Fraction(2))),
        "111111": ((ESCAPE, Fraction(1)),
                   (M1, Fraction(-2)), (M0, Fraction(2))),
        "111221": ((M1, Fraction(-2)), (M0, Fraction(2))),
    }
    for word in nonempty:
        actual = tuple((item[0], item[2])
                       for item in rows[word]["occurrences"])
        require(actual == expected[word_name(word)],
                (word, actual, expected[word_name(word)]))
    require(tuple(rows[tuple(map(int, name))]["equation_value"]
                  for name in ("111001", "111111", "111221")) ==
            (Fraction(0), Fraction(0), Fraction(0)), rows)

    row_vectors = {
        "coefficient:111001": (1, 1, 0),
        "coefficient:111111": (1, 1, 1),
        "coefficient:111221": (1, 1, 0),
    }
    antidiagonal = (1, -1, 0)
    short_tail = (0, 1, 1)
    require(rational_rank(tuple(row_vectors.values())) == 2,
            row_vectors)
    require(rational_rank(tuple(row_vectors.values()) + (antidiagonal,)) == 3,
            (row_vectors, antidiagonal))
    require(rational_rank(tuple(row_vectors.values()) + (short_tail,)) == 3,
            (row_vectors, short_tail))

    # Polynomial-ideal separation, not merely linear row separation.  The
    # map m0->t, m1->-t, n->1 kills m0+m1 and m0+m1+n-1, but sends the parent
    # anti-diagonal to 2t.  Therefore delta is not in the ideal generated by
    # the physically available local rows, even with arbitrary multipliers.
    quotient_images = {
        "mixed_m0_plus_m1": "0",
        "pure_m0_plus_m1_plus_n_minus_1": "0",
        "parent_antidiagonal_m0_minus_m1": "2*t",
    }

    missing_anchors = tuple(word_name(word) for word in WORDS
                            if len(set(word)) == 1
                            and not rows[word]["occurrences"])
    require(missing_anchors == ("000000", "222222"), missing_anchors)
    require(all(rows[tuple(map(int, name))]["equation_value"] == -1
                for name in missing_anchors), missing_anchors)
    return {
        "all_word_rows_checked": len(rows),
        "nonempty_lhs_words": tuple(map(word_name, nonempty)),
        "physical_row_vectors_M0_M1_N": row_vectors,
        "physical_row_rank": 2,
        "rank_with_parent_antidiagonal": 3,
        "rank_with_short_tail_selector": 3,
        "quotient_nonmembership_certificate": quotient_images,
        "missing_full_GHZ_anchors": missing_anchors,
        "full_specialized_target_ideal_warning": (
            "contains -1 and is the unit ideal; unrestricted membership on "
            "this non-full guard is vacuous"
        ),
    }


def symmetric_difference_size(first, second):
    return len(set(first) ^ set(second))


def shortest_c4_paths(start, finish):
    adjacency = {
        matching: tuple(other for other in MATCHINGS
                        if other != matching
                        and symmetric_difference_size(matching, other) == 4)
        for matching in MATCHINGS
    }
    distance = {start: 0}
    queue = deque((start,))
    while queue:
        matching = queue.popleft()
        for other in adjacency[matching]:
            if other not in distance:
                distance[other] = distance[matching] + 1
                queue.append(other)
    length = distance[finish]
    paths = tuple((start, middle, finish)
                  for middle in adjacency[start]
                  if finish in adjacency[middle] and length == 2)
    return length, paths


def live_matching_weight(weights, matching):
    value = Fraction(1)
    for endpoints in matching:
        selected = cell(endpoints, 1)
        if selected not in weights:
            return Fraction(0)
        value *= weights[selected]
    return value


def exchange_record(first, second, operation):
    common = tuple(sorted(set(first) & set(second)))
    difference = tuple(sorted(set(first) ^ set(second)))
    values = (live_matching_weight(guard_weights(), first),
              live_matching_weight(guard_weights(), second))
    return {
        "operation": operation,
        "from_fine": matching_name(first),
        "to_fine": matching_name(second),
        "common_tail": tuple(f"{left}{right}" for left, right in common),
        "alternating_cycle_length": len(difference),
        "parent_monomial_degree": 3,
        "toric_orientation": "from-minus-to",
        "guard_values": tuple(map(str, values)),
        "binomial_value": str(values[0] - values[1]),
        "physical_zero_on_guard": values[0] == values[1],
    }


def exchange_chain_audit():
    length, paths = shortest_c4_paths(M0, ESCAPE)
    require(length == 2 and len(paths) == 3, (length, paths))
    live_edges = frozenset(endpoints for endpoints, colour in guard_weights()
                           if colour == 1)
    live_paths = tuple(path for path in paths
                       if all(set(matching) <= live_edges for matching in path))
    require(live_paths == ((M0, M1, ESCAPE),), live_paths)
    other_intermediates = tuple(path[1] for path in paths if path not in live_paths)
    require(tuple(map(matching_name, other_intermediates)) ==
            ("03|12|45", "05|14|23"), other_intermediates)

    first = exchange_record(M0, M1,
                            "toric_C4_exchange:0125|common_tail_34")
    second = exchange_record(M1, ESCAPE,
                             "toric_C4_exchange:2345|common_tail_01")
    direct = exchange_record(M0, ESCAPE,
                             "toric_C6_exchange:012345|no_common_tail")
    require((first["binomial_value"], second["binomial_value"],
             direct["binomial_value"]) == ("4", "-3", "1"),
            (first, second, direct))
    require(not any(item["physical_zero_on_guard"]
                    for item in (first, second, direct)),
            (first, second, direct))
    return {
        "elementary_C4_distance_M0_to_escape": length,
        "all_shortest_C4_paths": tuple(
            tuple(map(matching_name, path)) for path in paths
        ),
        "unique_live_support_path": tuple(map(matching_name, live_paths[0])),
        "live_chain": (first, second),
        "primitive_direct_exchange": direct,
        "first_nonlift": (
            "M0-M1 is the parent anti-diagonal, but coefficient:111001 "
            "and coefficient:111221 contain M0+M1"
        ),
        "second_nonlift": (
            "M1-N changes cap-containing to cap-avoiding; the tail-01 "
            "restriction is the signless sub-sum M1+N, not an EqSystem row"
        ),
    }


def incidence_degree(monomial):
    degree = [0] * N
    for edge_index in monomial:
        for vertex in EDGES[edge_index]:
            degree[vertex] += 1
    return tuple(degree)


def toric_fibre_census():
    census = {}
    fibre_registry = {}
    for degree in (3, 4):
        fibres = defaultdict(list)
        for monomial in combinations_with_replacement(range(len(EDGES)), degree):
            fibres[incidence_degree(monomial)].append(monomial)
        histogram = Counter(map(len, fibres.values()))
        census[degree] = {
            "monomials": sum(map(len, fibres.values())),
            "incidence_fibres": len(fibres),
            "nontrivial_fibres": sum(len(items) > 1
                                     for items in fibres.values()),
            "binomial_pairs": sum(len(items) * (len(items) - 1) // 2
                                   for items in fibres.values()),
            "fibre_size_histogram": tuple(sorted(histogram.items())),
        }
        fibre_registry[degree] = fibres
    require(census[3] == {
        "monomials": 680, "incidence_fibres": 336,
        "nontrivial_fibres": 121, "binomial_pairs": 825,
        "fibre_size_histogram": ((1, 215), (3, 90), (6, 30), (15, 1)),
    }, census[3])
    require(census[4] == {
        "monomials": 3060, "incidence_fibres": 951,
        "nontrivial_fibres": 486, "binomial_pairs": 8955,
        "fibre_size_histogram": (
            (1, 465), (3, 270), (6, 135), (10, 66), (21, 15)
        ),
    }, census[4])

    weights = guard_weights()
    matching_values = {matching: live_matching_weight(weights, matching)
                       for matching in MATCHINGS}
    require(tuple(matching_values[matching] for matching in LIVE_MATCHINGS) ==
            (Fraction(2), Fraction(-2), Fraction(1)), matching_values)
    require(sum(value != 0 for value in matching_values.values()) == 3,
            matching_values)
    vanishing_pairs = 0
    live_incident_vanishing = 0
    for index, first in enumerate(MATCHINGS):
        for second in MATCHINGS[index + 1:]:
            if matching_values[first] == matching_values[second]:
                vanishing_pairs += 1
                if first in LIVE_MATCHINGS or second in LIVE_MATCHINGS:
                    live_incident_vanishing += 1
    require((vanishing_pairs, live_incident_vanishing) == (66, 0),
            (vanishing_pairs, live_incident_vanishing))

    # Every degree-four monomial M*x_e has site degrees 2 at the endpoints
    # of e and 1 elsewhere.  It is off the squarefree EqSystem word grade.
    live_colour_one_edges = tuple(endpoints for endpoints, colour in weights
                                  if colour == 1)
    degree_four_live_tests = 0
    pointwise_vanishing_degree_four = 0
    degree_four_fibres = fibre_registry[4]
    for matching in LIVE_MATCHINGS:
        for multiplier in live_colour_one_edges:
            monomial = tuple(sorted(
                tuple(EDGE_INDEX[endpoints] for endpoints in matching)
                + (EDGE_INDEX[multiplier],)
            ))
            site_degree = incidence_degree(monomial)
            require(sorted(site_degree) == [1, 1, 1, 1, 2, 2],
                    (matching, multiplier, site_degree))
            value = matching_values[matching] * weights[cell(multiplier, 1)]
            require(value != 0, (matching, multiplier, value))
            same_value = tuple(other for other in degree_four_fibres[site_degree]
                               if other != monomial
                               and monomial_value(other, weights) == value)
            if same_value:
                pointwise_vanishing_degree_four += len(same_value)
            degree_four_live_tests += 1
    require((degree_four_live_tests, pointwise_vanishing_degree_four) == (21, 0),
            (degree_four_live_tests, pointwise_vanishing_degree_four))
    return {
        "degree_census": census,
        "degree_three_perfect_matching_fibre_size": 15,
        "degree_three_PM_binomials": 105,
        "pointwise_vanishing_PM_binomials": vanishing_pairs,
        "pointwise_vanishing_edges_incident_to_live_parent": 0,
        "degree_four_live_parent_times_live_cell_tests": degree_four_live_tests,
        "pointwise_vanishing_degree_four_incident_exchanges": 0,
        "degree_four_typing": (
            "site multidegree (2,2,1,1,1,1) up to permutation; off the "
            "squarefree K6 coefficient-word grade"
        ),
        "homogeneous_degree_guard": (
            "degree-four generators cannot produce a degree-three parent "
            "anti-diagonal without division by an edge cell"
        ),
    }


def monomial_value(monomial, weights):
    value = Fraction(1)
    for edge_index in monomial:
        endpoints = EDGES[edge_index]
        selected = cell(endpoints, 1)
        if selected not in weights:
            return Fraction(0)
        value *= weights[selected]
    return value


def label_gate():
    return {
        "coordinate_order": ("M0_long_C6", "M1_short_C4", "N_escape"),
        "parent_antidiagonal": (1, -1, 0),
        "M0_M1_physical_words": ("111001", "111111", "111221"),
        "M1_N_common_word": "111111",
        "M0_M1_common_cap_window": "34",
        "M1_N_common_tail": "01",
        "M1_N_cap_status": ("contains:34", "avoids:34"),
        "toric_operation": "edge-incidence-kernel binomial",
        "physical_operations": (
            "coefficient:111001", "coefficient:111111", "coefficient:111221"
        ),
        "operation_labels_match": False,
        "verdict": (
            "unlabelled toric membership is true by adjoining M0-M1; "
            "source-labelled EqSystem generation is false at the first C4 edge"
        ),
    }


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    return {
        "theorem": "nine-cell toric exchange parent-antidiagonal nonlift",
        "pins": PINS,
        "minimal_exchange_chain": exchange_chain_audit(),
        "toric_degree_three_four_census": toric_fibre_census(),
        "full_eqsystem_row_audit": physical_row_audit(),
        "word_fine_operation_gate": label_gate(),
        "scope": (
            "exact selected three-row nine-cell guard; full 729-row inventory. "
            "The guard is not a full GHZ source, so its two missing target "
            "anchors cannot be used as a nonvacuous ideal-membership proof."
        ),
    }


EXPECTED_LEDGER_SHA256 = "967ae124bd1b980010110386590a5bd4fa82f4dfdc086341f7a9f915f6d7deeb"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                ("nine-cell toric ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("C6 nine-cell toric exchange / parent anti-diagonal: PASS")
    print("mode", arguments.mode)
    print("ledger_sha256", digest)
    print("unlabelled toric chain: M0 -> M1 -> N")
    print("first physical nonlift: M0-M1 versus signless Eq row M0+M1")


if __name__ == "__main__":
    main()

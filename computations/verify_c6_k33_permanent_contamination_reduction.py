#!/usr/bin/env python3
"""Reduce tail-free C6 contamination to one full six-term permanent.

Fix the K3,3 underlying the signed recurrence of eaff4ab.  Every one of the
nine other K6 perfect matchings has two same-shore edges and one cross edge;
it therefore shares a literal cross-edge tail with exactly two K3,3
permutation matchings, through C4 moves.

Conversely, a tail-free three-channel family inside K3,3 is one of its two
parity factorisations.  On every endpoint-coloured word its three live
occurrences cover all nine decorated cross edges, so occurrence closure is
exactly all six permutation matchings.  There is no same-word 3/4/5-term
intermediate.  The remaining six-term permanent is not a unit by itself: an
explicit all-nonzero 3x3 matrix has permanent zero.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_c6_terminal_orbit_offdiagonal_signed_exit_gate.py":
        "8bbcb614856f947ed8287f93e33c02d6e171464590eec21d75b816345e20f37d",
    "notes/c6-terminal-orbit-offdiagonal-signed-exit-gate.md":
        "b6625d952c11f0bdc877d941e5c770f70305e0c0a12fb99db6e4924a0c8087b0",
    "computations/verify_c6_thirteen_exit_k33_shared_star_guard.py":
        "04b631cee46de29d8b4228aad777a414ae75aa021444bbc9ffc39852442592e2",
    "notes/2026-08-15-c6-thirteen-exit-k33-shared-star-guard.md":
        "6cbafc38ad54f8100170188765acbe2750c776f4b484f4f5c7330c0247094993",
}
EXPECTED_LEDGER_SHA256 = (
    "fb4eeb08058596d58d964ff55aa2b985ed3d381b230c333c31d5f7351ff97552"
)

SITES = tuple(range(6))
COLOURS = tuple(range(3))
LEFT = (0, 2, 4)
RIGHT = (1, 3, 5)


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
            yield tuple(sorted((edge(first, second),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(SITES)))


def matching_name(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def matching_permutation(matching):
    right_index = {vertex: index for index, vertex in enumerate(RIGHT)}
    neighbours = {}
    for first, second in matching:
        if first in LEFT and second in RIGHT:
            neighbours[first] = second
        elif second in LEFT and first in RIGHT:
            neighbours[second] = first
        else:
            return None
    require(set(neighbours) == set(LEFT), (matching, neighbours))
    return tuple(right_index[neighbours[vertex]] for vertex in LEFT)


def parity(permutation):
    return sum(
        permutation[left] > permutation[right]
        for left in range(3) for right in range(left + 1, 3)
    ) % 2


def decorated_occurrence(matching, word):
    return frozenset(
        (endpoints, word[endpoints[0]], word[endpoints[1]])
        for endpoints in matching
    )


def permanent(matrix):
    return sum(
        matrix[0][permutation[0]]
        * matrix[1][permutation[1]]
        * matrix[2][permutation[2]]
        for permutation in permutations(range(3))
    )


def permanent2(matrix, deleted_row, deleted_column):
    rows = tuple(index for index in range(3) if index != deleted_row)
    columns = tuple(index for index in range(3)
                    if index != deleted_column)
    return (
        matrix[rows[0]][columns[0]] * matrix[rows[1]][columns[1]]
        + matrix[rows[0]][columns[1]] * matrix[rows[1]][columns[0]]
    )


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    k33 = tuple(matching for matching in MATCHINGS
                if matching_permutation(matching) is not None)
    outside = tuple(matching for matching in MATCHINGS if matching not in k33)
    require((len(MATCHINGS), len(k33), len(outside)) == (15, 6, 9),
            (len(MATCHINGS), len(k33), len(outside)))

    outside_records = []
    for matching in outside:
        left_edges = tuple(item for item in matching
                           if set(item) <= set(LEFT))
        right_edges = tuple(item for item in matching
                            if set(item) <= set(RIGHT))
        cross_edges = tuple(item for item in matching
                            if len(set(item) & set(LEFT)) == 1)
        require(tuple(map(len, (left_edges, right_edges, cross_edges))) ==
                (1, 1, 1), matching)
        tail = cross_edges[0]
        mates = tuple(item for item in k33 if tail in item)
        require(len(mates) == 2, (matching, tail, mates))
        for mate in mates:
            require(set(matching) & set(mate) == {tail},
                    (matching, mate, tail))
            require(len(set(matching) ^ set(mate)) == 4,
                    (matching, mate))
        outside_records.append({
            "fine": matching_name(matching),
            "same_shore_edges": (
                f"{left_edges[0][0]}{left_edges[0][1]}",
                f"{right_edges[0][0]}{right_edges[0][1]}",
            ),
            "cross_tail": f"{tail[0]}{tail[1]}",
            "C4_permutation_mates": tuple(map(matching_name, mates)),
        })

    factor_triples = tuple(
        family for family in combinations(k33, 3)
        if all(not (set(first) & set(second))
               for first, second in combinations(family, 2))
    )
    require(len(factor_triples) == 2, factor_triples)
    cross_edges = {edge(left, right) for left in LEFT for right in RIGHT}
    factor_records = []
    closure_histogram = Counter()
    for family in factor_triples:
        require(set().union(*(set(item) for item in family)) == cross_edges,
                family)
        family_parities = tuple(parity(matching_permutation(item))
                                for item in family)
        require(len(set(family_parities)) == 1,
                (family, family_parities))
        for word in product(COLOURS, repeat=6):
            support = frozenset().union(
                *(decorated_occurrence(item, word) for item in family)
            )
            require(len(support) == 9, (family, word, support))
            closure = tuple(
                item for item in MATCHINGS
                if decorated_occurrence(item, word) <= support
            )
            closure_histogram[len(closure)] += 1
            require(set(closure) == set(k33),
                    (family, word, tuple(map(matching_name, closure))))
        factor_records.append({
            "parity": family_parities[0],
            "fines": tuple(map(matching_name, family)),
            "edge_union": tuple(
                f"{first}{second}" for first, second in sorted(cross_edges)
            ),
            "endpoint_coloured_words_replayed": 3 ** 6,
            "same_word_occurrence_closure": 6,
        })
    require(closure_histogram == Counter({6: 2 * 3 ** 6}),
            closure_histogram)

    # The topology reduction cannot turn the full permanent into a unit.
    # This torus point also keeps every complementary 2x2 permanent nonzero.
    matrix = (
        (Q(-2), Q(1), Q(1)),
        (Q(1), Q(1), Q(1)),
        (Q(1), Q(1), Q(1)),
    )
    require(all(entry for row in matrix for entry in row), matrix)
    require(permanent(matrix) == 0, permanent(matrix))
    cofactors = tuple(permanent2(matrix, row, column)
                      for row in range(3) for column in range(3))
    require(all(cofactors), cofactors)

    return {
        "theorem": "C6 K3,3 permanent-contamination reduction",
        "pins": PINS,
        "bipartition": (LEFT, RIGHT),
        "matching_census": {
            "all_K6_fines": len(MATCHINGS),
            "K3,3_permutation_fines": len(k33),
            "outside_fines": len(outside),
        },
        "outside_fine_C4_routing": tuple(outside_records),
        "tail_free_factor_triples": tuple(factor_records),
        "same_word_closure_histogram": tuple(sorted(
            closure_histogram.items()
        )),
        "no_partial_permanent_branch": (
            "a live tail-free factor triple covers all nine decorated cross "
            "edges, hence forces all six permutation occurrences"
        ),
        "full_permanent_torus_guard": {
            "matrix": tuple(tuple(map(str, row)) for row in matrix),
            "permanent": "0",
            "permanental_2x2_cofactors": tuple(map(str, cofactors)),
            "verdict": (
                "the six-term permanent-only row is coefficient-compatible; "
                "pure normalization/mate recursion is still required"
            ),
        },
        "uniform_tail_scope": (
            "a single row-independent nonzero spectator matching tail "
            "factors throughout; changing spectator tails are not reduced"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("C6 K3,3 permanent-contamination reduction: PASS")
    print("mode", arguments.mode)
    print("outside fines -> C4 tail routes", len(ledger["outside_fine_C4_routing"]))
    print("tail-free factor triples / same-word closure", 2, 6)
    print("full permanent torus guard", ledger["full_permanent_torus_guard"]["verdict"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()

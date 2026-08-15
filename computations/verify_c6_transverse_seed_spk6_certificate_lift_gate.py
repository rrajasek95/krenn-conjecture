#!/usr/bin/env python3
"""Condition the certified SP-K6 obstruction on the transverse seed.

The ten-cell transverse packet is rejected before the SP-K6 rank-stratum
census: it has no pure matching, and its active rank-one graph has degree
two at every site.  Each of its 225 support-minimum three-pure completions
is rejected even more concretely by support principle (4): a mixed word has
exactly one supported perfect matching.

The mixed-singleton certificate is occurrence-linear and lifts through an
arbitrary nonzero spectator tail exactly when global occurrences factor as
{local singleton} x {tail occurrences}.  The checker verifies forced tails
and a three-term nonmonomial tail, then exhibits the first nonlift: two
crossing edges create a second global matching not divisible by either the
local singleton or the spectator tail.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_c6_parent_spair_thirteen_exit_trichotomy_guard.py":
        "01d5b591880d7d94706546f1db4248345b2041a0139a4a51c39e04b3cb0dce1b",
    "notes/2026-08-14-c6-parent-spair-thirteen-exit-trichotomy-guard.md":
        "8fb5cfb5b3101b89c717b0531d98ec44f4fd8a4925fc82af354e3db58ff2d755",
    "proofs/six-site-arbitrary-complex-obstruction.md":
        "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713",
    "notes/slice-cover.md":
        "dd4b99ca9c75c7081682e8de57c9915984395bf642ab4ababb4037711d6ed989",
    "computations/verify_uniform_permanent_triangle_common_tail_reinsertion.py":
        "cc5b03dc01e74b0881ec993d814c4b1147b9dfcf52cb09db4f445ed113bb7743",
    "notes/2026-08-14-uniform-permanent-triangle-common-tail-reinsertion.md":
        "f3b1d4a3f7eef1476a45bdcdfa800674f0acfa11ad4b88adc9afbad289a918fc",
}

COLOURS = tuple(range(3))
LOCAL_SITES = tuple(range(6))
LOCAL_WORDS = tuple(product(COLOURS, repeat=6))


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


LOCAL_MATCHINGS = tuple(sorted(perfect_matchings(LOCAL_SITES)))
TRANSVERSE_A = tuple(sorted(((0, 2), (1, 3), (4, 5))))
TRANSVERSE_B = tuple(sorted(((0, 3), (1, 5), (2, 4))))
WORD0 = (1, 1, 1, 0, 0, 1)
WORD2 = (1, 1, 1, 2, 2, 1)
PURE1_FINE = tuple(sorted(((0, 2), (1, 5), (3, 4))))


def word_name(word):
    return "".join(map(str, word))


def matching_name(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def cell_name(cell):
    left, right, alpha, beta = cell
    return f"a{left}{right}^{alpha}{beta}"


def occurrence_cells(matching, word):
    return tuple((left, right, word[left], word[right])
                 for left, right in matching)


def seed_weights():
    weights = {}
    for word in (WORD0, WORD2):
        for cell in occurrence_cells(TRANSVERSE_A, word):
            weights[cell] = Fraction(1)
        for cell in occurrence_cells(TRANSVERSE_B, word):
            weights[cell] = Fraction(1)
    weights[(1, 5, 1, 1)] = Fraction(-1)
    require(len(weights) == 10, weights)
    return weights


def live_matchings(word, support, vertices=LOCAL_SITES):
    return tuple(matching for matching in perfect_matchings(vertices)
                 if set(occurrence_cells(matching, word)) <= support)


def matrix_rank(matrix):
    rows = [list(map(Fraction, row)) for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((row for row in range(rank, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [entry / scale for entry in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [left - scale * right
                         for left, right in zip(rows[row], rows[rank],
                                                strict=True)]
        rank += 1
    return rank


def seed_certificate():
    weights = seed_weights()
    support = set(weights)
    pure_counts = {
        colour: len(live_matchings((colour,) * 6, support))
        for colour in COLOURS
    }
    require(pure_counts == {0: 0, 1: 0, 2: 0}, pure_counts)

    edge_ranks = {}
    for left in LOCAL_SITES:
        for right in LOCAL_SITES:
            if left >= right:
                continue
            matrix = [[weights.get((left, right, alpha, beta), Fraction(0))
                       for beta in COLOURS] for alpha in COLOURS]
            edge_ranks[(left, right)] = matrix_rank(matrix)
    rank_one_edges = tuple(edge for edge, rank in edge_ranks.items()
                           if rank == 1)
    require(set(rank_one_edges) ==
            set(TRANSVERSE_A) | set(TRANSVERSE_B), rank_one_edges)
    degrees = tuple(sum(site in edge for edge in rank_one_edges)
                    for site in LOCAL_SITES)
    require(degrees == (2,) * 6, degrees)
    return {
        "support_cells": len(support),
        "first_exact_SP_K6_clause": (
            "support principle 3: every pure target word must have a "
            "supported perfect matching"
        ),
        "pure_matching_counts": pure_counts,
        "secondary_slice_cover_failure": {
            "active_rank_one_edges": tuple(matching_name((edge,))
                                           for edge in rank_one_edges),
            "rank_one_degrees": degrees,
            "required_minimum_degree": 3,
            "failure_at_every_site": True,
        },
        "rank_stratum_status": (
            "not reached: nine rank-not-one blocks exceed the derived "
            "|F|<=6 budget because the pure target hypotheses already fail"
        ),
        "lift_scope": (
            "absence of a local pure occurrence is not stable under an "
            "uncontrolled larger-source embedding; cross-window matchings "
            "may supply the missing pure coefficient"
        ),
    }


def completion_support(pure0, pure2):
    support = set(seed_weights())
    support.update(occurrence_cells(pure0, (0,) * 6))
    support.update(occurrence_cells(PURE1_FINE, (1,) * 6))
    support.update(occurrence_cells(pure2, (2,) * 6))
    require(len(support) == 17, (pure0, pure2, support))
    return support


def word_profile(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def minimum_completion_certificates():
    records = []
    singleton_histogram = Counter()
    all_profile_histogram = Counter()
    first_profile_histogram = Counter()
    for pure0 in LOCAL_MATCHINGS:
        for pure2 in LOCAL_MATCHINGS:
            support = completion_support(pure0, pure2)
            pure_counts = tuple(len(live_matchings((colour,) * 6, support))
                                for colour in COLOURS)
            require(pure_counts == (1, 1, 1),
                    (pure0, pure2, pure_counts))
            singletons = []
            for word in LOCAL_WORDS:
                if len(set(word)) == 1:
                    continue
                live = live_matchings(word, support)
                if len(live) == 1:
                    singletons.append((word, live[0]))
                    all_profile_histogram[word_profile(word)] += 1
            require(singletons, (pure0, pure2))
            singleton_histogram[len(singletons)] += 1
            first = min(singletons)
            first_profile_histogram[word_profile(first[0])] += 1
            records.append({
                "pure0": matching_name(pure0),
                "pure2": matching_name(pure2),
                "singleton_count": len(singletons),
                "first_word": word_name(first[0]),
                "first_fine": matching_name(first[1]),
                "first_cells": tuple(cell_name(cell) for cell in
                                     occurrence_cells(first[1], first[0])),
                "first_operation": f"coefficient:{word_name(first[0])}",
            })

    expected_singletons = Counter({
        9: 8, 10: 15, 11: 6, 12: 10, 13: 26, 14: 22, 15: 24,
        16: 4, 17: 16, 18: 14, 20: 26, 21: 4, 22: 5, 23: 8,
        25: 4, 26: 9, 27: 2, 28: 4, 29: 6, 33: 8, 38: 2, 44: 2,
    })
    expected_profiles = Counter({
        (3, 2, 1): 1512, (4, 2): 960, (2, 2, 2): 450,
        (5, 1): 360, (4, 1, 1): 360, (3, 3): 360,
    })
    expected_first_profiles = Counter({
        (4, 2): 108, (5, 1): 99, (3, 3): 12,
        (2, 2, 2): 3, (3, 2, 1): 3,
    })
    require(singleton_histogram == expected_singletons,
            singleton_histogram)
    require(all_profile_histogram == expected_profiles,
            all_profile_histogram)
    require(first_profile_histogram == expected_first_profiles,
            first_profile_histogram)
    require(len(records) == 225, len(records))
    serialized = json.dumps(records, sort_keys=True, separators=(",", ":"))
    canonical = min(records,
                    key=lambda item: (item["singleton_count"],
                                      item["pure0"], item["pure2"]))
    require((canonical["first_word"], canonical["first_fine"]) ==
            ("000001", "01|23|45"), canonical)
    return {
        "minimum_completions": len(records),
        "first_exact_SP_K6_certificate": (
            "support principle 4: a mixed coefficient fibre may not have "
            "exactly one supported perfect matching"
        ),
        "certificate_stage": (
            "pre-rank-stratum support clause; no defect graph, Laurent "
            "lattice, rectangle minor, or LRAT branch is needed"
        ),
        "singleton_count_histogram": dict(sorted(singleton_histogram.items())),
        "all_singleton_word_profile_histogram": {
            "+".join(map(str, profile)): count
            for profile, count in sorted(all_profile_histogram.items())
        },
        "first_certificate_profile_histogram": {
            "+".join(map(str, profile)): count
            for profile, count in sorted(first_profile_histogram.items())
        },
        "certificate_record_sha256": sha256(serialized.encode()).hexdigest(),
        "canonical_certificate": canonical,
    }, canonical


def extend_matching(matching, extra_edges):
    return tuple(sorted(tuple(matching) + tuple(extra_edges)))


def common_tail_lift(canonical):
    pure0 = next(matching for matching in LOCAL_MATCHINGS
                 if matching_name(matching) == canonical["pure0"])
    pure2 = next(matching for matching in LOCAL_MATCHINGS
                 if matching_name(matching) == canonical["pure2"])
    support = completion_support(pure0, pure2)
    local_word = tuple(map(int, canonical["first_word"]))
    local_fine = next(matching for matching in LOCAL_MATCHINGS
                      if matching_name(matching) == canonical["first_fine"])
    require(live_matchings(local_word, support) == (local_fine,),
            (local_word, local_fine))

    forced_tail_records = []
    for pairs in range(1, 4):
        tail_edges = tuple((6 + 2 * index, 7 + 2 * index)
                           for index in range(pairs))
        extended_word = local_word + (2,) * (2 * pairs)
        extended_support = set(support)
        for edge in tail_edges:
            extended_support.add((edge[0], edge[1], 2, 2))
        vertices = tuple(range(6 + 2 * pairs))
        live = live_matchings(extended_word, extended_support, vertices)
        expected = (extend_matching(local_fine, tail_edges),)
        require(live == expected, (pairs, live, expected))
        forced_tail_records.append({
            "spectator_pairs": pairs,
            "order": len(vertices),
            "global_occurrences": len(live),
            "fine": matching_name(live[0]),
        })

    # A genuinely nonmonomial tail: complete K4 on sites 6,7,8,9 has three
    # perfect matchings.  Disjoint support makes the global occurrence set
    # the Cartesian product of the local singleton and those three tails.
    tail_vertices = (6, 7, 8, 9)
    tail_matchings = tuple(sorted(perfect_matchings(tail_vertices)))
    extended_word = local_word + (2,) * 4
    extended_support = set(support)
    for left in tail_vertices:
        for right in tail_vertices:
            if left < right:
                extended_support.add((left, right, 2, 2))
    live = live_matchings(extended_word, extended_support, tuple(range(10)))
    expected = tuple(sorted(extend_matching(local_fine, tail)
                            for tail in tail_matchings))
    require(live == expected, (live, expected))
    return {
        "local_word": word_name(local_word),
        "local_singleton_fine": matching_name(local_fine),
        "forced_matching_tail_tests": tuple(forced_tail_records),
        "nonmonomial_tail_test": {
            "tail_vertices": tail_vertices,
            "tail_occurrences": len(tail_matchings),
            "global_occurrences": len(live),
            "cartesian_bijection": True,
        },
        "uniform_statement": (
            "if the global occurrence fibre is {local singleton} times one "
            "common labelled tail family, then F=m*T; the mixed target is "
            "zero and support localization at m plus T!=0 gives a unit"
        ),
        "common_tail_requirement": (
            "word/fine/operation-preserving Cartesian occurrence bijection; "
            "equality only after an unlabelled projection is insufficient"
        ),
    }, (support, local_word, local_fine)


def first_crossing_nonlift(local_data):
    support, local_word, local_fine = local_data
    require((word_name(local_word), matching_name(local_fine)) ==
            ("000001", "01|23|45"), (local_word, local_fine))
    extended_word = local_word + (2, 2)
    tail = (6, 7)
    crossing_edges = ((4, 6), (5, 7))
    extended_support = set(support)
    extended_support.add((6, 7, 2, 2))
    extended_support.add((4, 6, local_word[4], 2))
    extended_support.add((5, 7, local_word[5], 2))
    live = live_matchings(extended_word, extended_support, tuple(range(8)))
    intended = extend_matching(local_fine, (tail,))
    crossing = tuple(sorted(((0, 1), (2, 3), (4, 6), (5, 7))))
    require(live == (intended, crossing), (live, intended, crossing))

    weights = {cell: Fraction(1) for cell in extended_support}
    weights[(5, 7, local_word[5], 2)] = Fraction(-1)
    values = []
    for matching in live:
        value = Fraction(1)
        for cell in occurrence_cells(matching, extended_word):
            value *= weights[cell]
        values.append(value)
    require(tuple(values) == (Fraction(1), Fraction(-1)), values)
    require(sum(values) == 0, values)
    shared_edges = tuple(sorted(set(intended) & set(crossing)))
    require(shared_edges == ((0, 1), (2, 3)), shared_edges)
    return {
        "order": 8,
        "word": word_name(extended_word),
        "intended_operation": "local-singleton x spectator-tail",
        "intended_fine": matching_name(intended),
        "first_crossing_operation": "two-edge window/tail crossing",
        "crossing_fine": matching_name(crossing),
        "crossing_cells": tuple(cell_name(cell) for cell in
                                occurrence_cells(crossing, extended_word)
                                if cell[0] >= 4),
        "coefficient_factorization": (
            "a01^00*a23^00*(a45^01*a67^22 + a46^02*a57^12)"
        ),
        "all_unit_cancellation_values": tuple(map(str, values)),
        "minimum_crossing_edges": 2,
        "shared_partial_tail": tuple(f"{u}{v}" for u, v in shared_edges),
        "first_nonlift": (
            "the crossing term is divisible by neither the full local "
            "singleton a01*a23*a45 nor the spectator tail a67; the global "
            "fibre is no longer local x tail and can cancel exactly"
        ),
    }


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    completions, canonical = minimum_completion_certificates()
    tail_lift, local_data = common_tail_lift(canonical)
    return {
        "theorem": "SP-K6 certificate conditioned on transverse seed",
        "pins": PINS,
        "ten_cell_seed": seed_certificate(),
        "two_hundred_twenty_five_minimum_completions": completions,
        "occurrence_linear_common_tail_lift": tail_lift,
        "first_nonlift_term": first_crossing_nonlift(local_data),
        "verdict": (
            "minimum completions are closed by the literal mixed-singleton "
            "support clause, before any SP-K6 rank stratum.  This certificate "
            "is uniformly liftable under exact common-tail occurrence "
            "factorization; two window/tail crossing edges are the first "
            "possible and actual obstruction."
        ),
    }


EXPECTED_LEDGER_SHA256 = "4d89d7b8a5dfccbe20ee3756a1853ecf5245c6d56688ad038b7c715f9702a846"


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
                ("conditioned SP-K6 ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("C6 transverse seed conditioned SP-K6 certificate: PASS")
    print("mode", arguments.mode)
    print("ledger_sha256", digest)
    print("minimum completion certificate: pre-stratum mixed singleton")
    print("uniform lift: common-tail yes; first nonlift: two crossing edges")


if __name__ == "__main__":
    main()

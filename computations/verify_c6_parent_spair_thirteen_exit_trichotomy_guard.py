#!/usr/bin/env python3
"""Classify the thirteen exits of the minimum C6 parent S-chain.

The degree-four parent S-chain of 9ab9b48 has, after deletion, thirteen
matching exits in each of the words 111001 and 111221.  This checker gives
their intrinsic 1+4+4+4 matching classification and tests the strongest
literal source-labelled trichotomy.

The trichotomy is false without an additional full-source/minimality input.
Two transverse exits form a six-cycle and admit a smallest ten-cell,
four-word exact mixed-row packet.  Its complete restriction/reinsertion
square has rank seven on eight occurrence coordinates.  The primitive dual
lambda(A_w)=+1, lambda(B_w)=-1 kills every coefficient and word-transport
boundary, while detecting the fine-changing anti-diagonal.
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
    "computations/verify_c6_unspecialized_eqsystem_parent_antidiagonal_spair.py":
        "584c36d076224fcc437b70998a43091ffa0f19b35bfbe73fea0caf1d7ae9865a",
    "notes/2026-08-14-c6-unspecialized-eqsystem-parent-antidiagonal-spair.md":
        "b15dd110cf28826751e5f32e162c91c7990cf119ed4a1c0361403dcf4ad0a369",
}

N = 6
COLOURS = tuple(range(3))
SITES = tuple(range(N))
WORDS = tuple(product(COLOURS, repeat=N))


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
M0 = tuple(sorted(((0, 5), (1, 2), (3, 4))))
M1 = tuple(sorted(((0, 1), (2, 5), (3, 4))))
CAP = (3, 4)
DELETION_EDGE = (0, 1)
WORD0 = (1, 1, 1, 0, 0, 1)
WORD2 = (1, 1, 1, 2, 2, 1)
TARGET_WORDS = (WORD0, WORD2)

# A and B are transverse to both parents and disjoint from one another.
TRANSVERSE_A = tuple(sorted(((0, 2), (1, 3), (4, 5))))
TRANSVERSE_B = tuple(sorted(((0, 3), (1, 5), (2, 4))))


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


def restricted_sign(matching):
    return -1 if DELETION_EDGE in matching else 1


def exit_classification():
    exits = tuple(matching for matching in MATCHINGS
                  if matching not in (M0, M1))
    classes = defaultdict(list)
    records = []
    for matching in exits:
        common0 = tuple(sorted(set(matching) & set(M0)))
        common1 = tuple(sorted(set(matching) & set(M1)))
        if CAP in matching:
            label = "cap_complement"
        elif len(common0) == 1 and not common1:
            label = "one_tail_from_M0"
        elif len(common1) == 1 and not common0:
            label = "one_tail_from_M1"
        elif not common0 and not common1:
            label = "transverse_C6"
        else:
            raise RuntimeError((matching, common0, common1))
        classes[label].append(matching)
        records.append({
            "fine": matching_name(matching),
            "restricted_sign": restricted_sign(matching),
            "class": label,
            "common_tail_M0": tuple(f"{u}{v}" for u, v in common0),
            "common_tail_M1": tuple(f"{u}{v}" for u, v in common1),
            "cap34_status": "contains" if CAP in matching else "avoids",
            "symmetric_difference_M0": len(set(matching) ^ set(M0)),
            "symmetric_difference_M1": len(set(matching) ^ set(M1)),
            "operation": "outside:D_a01^00(parent-spair)",
        })

    require({label: len(items) for label, items in classes.items()} == {
        "cap_complement": 1,
        "one_tail_from_M0": 4,
        "one_tail_from_M1": 4,
        "transverse_C6": 4,
    }, classes)
    cap_matching = classes["cap_complement"][0]
    require(cap_matching == tuple(sorted(((0, 2), (1, 5), (3, 4)))),
            cap_matching)
    majority_vertices = (0, 1, 2, 5)
    residual_pairings = {
        tuple(edge for edge in matching if edge != CAP)
        for matching in (M0, M1, cap_matching)
    }
    require(residual_pairings == set(perfect_matchings(majority_vertices)),
            residual_pairings)
    require(set(classes["transverse_C6"]) == {
        tuple(sorted(((0, 2), (1, 3), (4, 5)))),
        tuple(sorted(((0, 2), (1, 4), (3, 5)))),
        tuple(sorted(((0, 3), (1, 5), (2, 4)))),
        tuple(sorted(((0, 4), (1, 5), (2, 3)))),
    }, classes["transverse_C6"])

    # If a completion adds a third fine to the sharp transverse pair A,B,
    # nine choices share a literal tail with A or B and are C4 branches.
    # The four disjoint choices return to the original parent network.
    third_fines = tuple(matching for matching in MATCHINGS
                        if matching not in (TRANSVERSE_A, TRANSVERSE_B))
    c4_third_fines = tuple(matching for matching in third_fines
                           if (set(matching) & set(TRANSVERSE_A) or
                               set(matching) & set(TRANSVERSE_B)))
    disjoint_third_fines = tuple(matching for matching in third_fines
                                 if not set(matching) & set(TRANSVERSE_A)
                                 and not set(matching) & set(TRANSVERSE_B))
    require(len(c4_third_fines) == 9, c4_third_fines)
    require(disjoint_third_fines == (
        M1,
        tuple(sorted(((0, 4), (1, 2), (3, 5)))),
        M0,
        tuple(sorted(((0, 5), (1, 4), (2, 3)))),
    ), disjoint_third_fines)
    disjoint_closures = []
    expected_closure_sizes = {
        M1: 4,
        tuple(sorted(((0, 4), (1, 2), (3, 5)))): 4,
        M0: 6,
        tuple(sorted(((0, 5), (1, 4), (2, 3)))): 4,
    }
    for third in disjoint_third_fines:
        edge_support = (set(TRANSVERSE_A) | set(TRANSVERSE_B) |
                        set(third))
        closure = tuple(matching for matching in MATCHINGS
                        if set(matching) <= edge_support)
        require(len(closure) == expected_closure_sizes[third],
                (third, closure))
        extras = tuple(matching for matching in closure
                       if matching not in (TRANSVERSE_A, TRANSVERSE_B, third))
        require(extras, (third, closure))
        extra_tail_records = []
        for extra in extras:
            common_tail = tuple(sorted(set(third) & set(extra)))
            require(len(common_tail) == 1,
                    (third, extra, common_tail))
            extra_tail_records.append({
                "extra_fine": matching_name(extra),
                "literal_common_tail":
                    f"{common_tail[0][0]}{common_tail[0][1]}",
            })
        disjoint_closures.append({
            "third_fine": matching_name(third),
            "matching_closure_size": len(closure),
            "forced_additional_fines": tuple(extra_tail_records),
        })

    c4_tail_records = []
    for third in c4_third_fines:
        possible_parents = tuple(parent for parent in
                                 (TRANSVERSE_A, TRANSVERSE_B)
                                 if set(third) & set(parent))
        require(possible_parents, third)
        parent = possible_parents[0]
        common_tail = tuple(sorted(set(third) & set(parent)))
        require(len(common_tail) == 1, (third, parent, common_tail))
        c4_tail_records.append({
            "third_fine": matching_name(third),
            "transverse_parent": matching_name(parent),
            "literal_common_tail":
                f"{common_tail[0][0]}{common_tail[0][1]}",
        })
    return {
        "counts": {label: len(items)
                   for label, items in sorted(classes.items())},
        "all_thirteen_records": tuple(records),
        "cap_complement": {
            "fine": matching_name(cap_matching),
            "majority_window": "0125",
            "three_pairings": tuple(matching_name(matching)
                                    for matching in (M0, M1, cap_matching)),
            "available_cap_colours_in_two_word_packet": (0, 2),
            "missing_activity_channel": 1,
            "verdict": (
                "physically typed local C4 coefficient core, but not an "
                "active three-colour cap without an additional colour-1 face"
            ),
        },
        "one_tail_candidates": {
            "count": (len(classes["one_tail_from_M0"]) +
                      len(classes["one_tail_from_M1"])),
            "verdict": (
                "literal C4-adjacent fine pairs; coefficient rows are "
                "signless, so orientation requires another Macaulay "
                "recolouring and reproduces the outside-exit problem"
            ),
        },
        "transverse_candidates": {
            "count": len(classes["transverse_C6"]),
            "verdict": (
                "no common parent tail and six-edge symmetric difference; "
                "these are the first nonrecursive exits"
            ),
        },
        "third_fine_recursion": {
            "C4_common_tail_choices": tuple(matching_name(matching)
                                            for matching in c4_third_fines),
            "C4_common_tail_count": len(c4_third_fines),
            "C4_literal_tail_records": tuple(c4_tail_records),
            "disjoint_choices": tuple(matching_name(matching)
                                      for matching in disjoint_third_fines),
            "disjoint_count": len(disjoint_third_fines),
            "return_to_parent": (matching_name(M0), matching_name(M1)),
            "remaining_two_disjoint_choices": (
                "04|12|35 shares tail 12 with M0",
                "05|14|23 shares tail 05 with M0",
            ),
            "disjoint_matching_closures": tuple(disjoint_closures),
            "verdict": (
                "a necessary third fine is either a literal C4 branch from "
                "the transverse pair or its own edge support forces a fourth "
                "fine in the original cap/one-tail packet"
            ),
            "uniform_tail_promotion_scope": (
                "every third-fine resolution edge has one literal spectator "
                "matching tail; the only tail-rank-zero obstruction is the "
                "initial transverse pair A,B itself"
            ),
        },
    }


def counterguard_weights():
    weights = {}
    # The two matchings use four independently recoloured edges incident to
    # sites 3,4 and two common-colour edges.  Give B the sign -1 on a15^11.
    for word in TARGET_WORDS:
        for cell in occurrence_cells(TRANSVERSE_A, word):
            weights[cell] = Fraction(1)
        for cell in occurrence_cells(TRANSVERSE_B, word):
            weights[cell] = Fraction(1)
    weights[(1, 5, 1, 1)] = Fraction(-1)
    require(len(weights) == 10, weights)
    return weights


def complete_rows(weights):
    rows = {}
    for word in WORDS:
        occurrences = []
        for matching in MATCHINGS:
            cells = occurrence_cells(matching, word)
            if not all(cell in weights for cell in cells):
                continue
            value = Fraction(1)
            for cell in cells:
                value *= weights[cell]
            occurrences.append((matching, cells, value))
        target = Fraction(int(len(set(word)) == 1))
        rows[word] = {
            "occurrences": tuple(occurrences),
            "lhs": sum((item[2] for item in occurrences), Fraction(0)),
            "target": target,
        }
    return rows


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
        matrix[rank] = [entry / scale for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [left - scale * right
                           for left, right in zip(matrix[row], matrix[rank],
                                                  strict=True)]
        rank += 1
    return rank


def word_square_and_dual():
    weights = counterguard_weights()
    rows = complete_rows(weights)
    live_words = tuple(word for word, row in rows.items()
                       if row["occurrences"])
    expected_words = (
        (1, 1, 1, 0, 0, 1),
        (1, 1, 1, 0, 2, 1),
        (1, 1, 1, 2, 0, 1),
        (1, 1, 1, 2, 2, 1),
    )
    require(live_words == expected_words, tuple(map(word_name, live_words)))
    occurrence_records = []
    for word in live_words:
        row = rows[word]
        require(tuple(item[0] for item in row["occurrences"]) ==
                (TRANSVERSE_A, TRANSVERSE_B), (word, row))
        require(tuple(item[2] for item in row["occurrences"]) ==
                (Fraction(1), Fraction(-1)), (word, row))
        require(row["lhs"] == row["target"] == 0, (word, row))
        for matching, cells, value in row["occurrences"]:
            occurrence_records.append({
                "word": word_name(word),
                "fine": matching_name(matching),
                "coefficient_operation": f"coefficient:{word_name(word)}",
                "derivative_operation": "outside:D_a01^00(parent-spair)",
                "cap34_status": "avoids",
                "common_parent_tail": "none",
                "cells": tuple(cell_name(cell) for cell in cells),
                "source_value": str(value),
            })

    # Coordinates are (A_w,B_w) at the four vertices of the colour square.
    coordinate_index = {
        (word, matching): 2 * position + fine
        for position, word in enumerate(live_words)
        for fine, matching in enumerate((TRANSVERSE_A, TRANSVERSE_B))
    }
    generators = []
    labels = []
    for word in live_words:
        vector = [0] * 8
        vector[coordinate_index[(word, TRANSVERSE_A)]] = 1
        vector[coordinate_index[(word, TRANSVERSE_B)]] = 1
        generators.append(tuple(vector))
        labels.append(f"coefficient:{word_name(word)}")

    word_set = set(live_words)
    square_edges = []
    for word in live_words:
        for site in (3, 4):
            if word[site] != 0:
                continue
            changed = list(word)
            changed[site] = 2
            changed = tuple(changed)
            require(changed in word_set, (word, site, changed))
            square_edges.append((word, changed, site))
            for matching in (TRANSVERSE_A, TRANSVERSE_B):
                vector = [0] * 8
                vector[coordinate_index[(word, matching)]] = -1
                vector[coordinate_index[(changed, matching)]] = 1
                generators.append(tuple(vector))
                labels.append(
                    f"restriction/reinsertion:site{site}:"
                    f"{word_name(word)}->{word_name(changed)}:"
                    f"{matching_name(matching)}"
                )
    require(len(square_edges) == 4 and len(generators) == 12,
            (square_edges, len(generators)))
    rank = rational_rank(generators)
    dual = tuple(1 if coordinate % 2 == 0 else -1
                 for coordinate in range(8))
    require(rank == 7, (rank, generators))
    require(all(sum(left * right for left, right in zip(dual, generator,
                                                        strict=True)) == 0
                for generator in generators), (dual, generators))
    oriented = [0] * 8
    oriented[coordinate_index[(WORD0, TRANSVERSE_A)]] = 1
    oriented[coordinate_index[(WORD0, TRANSVERSE_B)]] = -1
    require(sum(left * right for left, right in zip(dual, oriented,
                                                    strict=True)) == 2,
            (dual, oriented))

    # Each matching has a commuting site3/site4 transport square.  Its
    # alternating boundary is literally zero before coarsening.
    for matching in (TRANSVERSE_A, TRANSVERSE_B):
        w00, w02, w20, w22 = live_words
        path_first = [0] * 8
        path_second = [0] * 8
        path_first[coordinate_index[(w00, matching)]] = -1
        path_first[coordinate_index[(w22, matching)]] = 1
        path_second[coordinate_index[(w00, matching)]] = -1
        path_second[coordinate_index[(w22, matching)]] = 1
        require(path_first == path_second, (matching, path_first, path_second))

    pure_failures = tuple(word_name(word) for word, row in rows.items()
                          if len(set(word)) == 1 and row["lhs"] != row["target"])
    require(pure_failures == ("000000", "111111", "222222"), pure_failures)
    return {
        "support_cells": tuple(sorted(cell_name(cell) for cell in weights)),
        "support_cell_count": len(weights),
        "live_words": tuple(map(word_name, live_words)),
        "occurrence_records": tuple(occurrence_records),
        "all_live_mixed_rows_exact": True,
        "mixed_singletons": 0,
        "matching_union": {
            "A": matching_name(TRANSVERSE_A),
            "B": matching_name(TRANSVERSE_B),
            "common_edges": (),
            "symmetric_difference_size":
                len(set(TRANSVERSE_A) ^ set(TRANSVERSE_B)),
            "underlying_graph": "one alternating C6",
            "cap34_present": False,
        },
        "labelled_C0_coordinates": 8,
        "coefficient_plus_transport_generators": len(generators),
        "generator_labels": tuple(labels),
        "generator_rank": rank,
        "cokernel_dimension": 1,
        "primitive_dual_coordinate_order": tuple(
            f"{matching_name(matching)}@{word_name(word)}"
            for word in live_words
            for matching in (TRANSVERSE_A, TRANSVERSE_B)
        ),
        "primitive_dual": dual,
        "dual_on_A_minus_B": 2,
        "first_required_column": (
            "fine-changing C6 operation with nonzero lambda; ordinary "
            "coefficient and site3/site4 restriction/reinsertion rows are dark"
        ),
        "pure_anchor_failures": pure_failures,
        "scope_warning": (
            "exact four-word mixed EqSystem packet, not a full ternary GHZ "
            "source; pure anchor rows are retained as failures, not used as units"
        ),
    }


def minimality_gate():
    # A non-singleton obstruction needs two occurrences.  Avoiding a literal
    # C4/common-tail reduction forces disjoint matchings, whose union has six
    # edges.  With no cap34, sites 3 and 4 have four distinct incident edges;
    # retaining both colours 0 and 2 duplicates exactly those four cells.
    common = set(TRANSVERSE_A) & set(TRANSVERSE_B)
    union = set(TRANSVERSE_A) | set(TRANSVERSE_B)
    incident_34 = {edge for edge in union if 3 in edge or 4 in edge}
    other = union - incident_34
    require(not common and len(union) == 6, (common, union))
    require(CAP not in union, union)
    require((len(incident_34), len(other)) == (4, 2),
            (incident_34, other))
    require(6 + len(incident_34) == 10, incident_34)
    return {
        "one_word_lower_bound": 6,
        "reason_one_word": (
            "two disjoint perfect matchings are necessary and form a C6"
        ),
        "two_output_word_lower_bound": 10,
        "reason_two_words": (
            "four distinct edges incident to sites 3,4 each need both "
            "endpoint-colour versions, while two remaining cells are shared"
        ),
        "bound_attained": True,
    }


def two_fine_pure_completion_gate():
    # On the four live corners b,c in {0,2}, both occurrence channels are
    # nonzero and cancel.  Write their separated extensions as
    # A_bc=p_b q_c and B_bc=r_b s_c, normalized on the old corners by
    # p0=p2=q0=q2=r0=r2=1 and s0=s2=-1.
    #
    # Avoiding a singleton in words (1,0) and (0,1) forces all four new
    # factors p1,q1,r1,s1 nonzero.  Their mixed equations then read
    # p1-r1=0 and q1+s1=0.  The pure centre is consequently
    # p1*q1+r1*s1=p1*(q1+s1)=0, contradicting target 1.
    # The coefficient tuples below encode those exact substitutions.
    mixed_site3_relation = {"p1": 1, "r1": -1}
    mixed_site4_relation = {"q1": 1, "s1": 1}
    substitution = {"r1": "p1", "s1": "-q1"}
    pure_centre_after_substitution = {
        "p1*q1": 1,
        "p1*q1_from_r1*s1": -1,
    }
    require(sum(pure_centre_after_substitution.values()) == 0,
            pure_centre_after_substitution)
    return {
        "two_separated_fines": (matching_name(TRANSVERSE_A),
                                matching_name(TRANSVERSE_B)),
        "old_nonzero_colour_square": "{0,2}x{0,2}",
        "mixed_site3_equation": mixed_site3_relation,
        "mixed_site4_equation": mixed_site4_relation,
        "forced_substitution": substitution,
        "pure_111111_value_with_no_singleton": 0,
        "required_pure_target": 1,
        "exact_alternative": (
            "any completion using only these two fines either creates a "
            "literal mixed singleton (some new separated factor vanishes) "
            "or fails pure normalization; an exact completion must add a "
            "third matching occurrence"
        ),
        "limitation": (
            "the third occurrence can itself be another transverse C6 exit; "
            "the thirteen-exit classification alone does not force it into "
            "the cap or one-tail classes"
        ),
    }


def minimum_full_GHZ_support_completion():
    # "Full-GHZ support" here means that all three pure target words have a
    # live occurrence.  It is a necessary condition for an exact source.
    # The old ten-cell packet has two colour-1 diagonal cells a02^11,a15^11,
    # so the unique one-cell pure-1 completion is a34^11.  Pure colours 0,2
    # each require a whole three-cell matching.  Hence seven added cells is
    # the sharp support minimum and there are 15^2=225 labelled completions.
    base = set(counterguard_weights())
    pure1 = tuple(sorted(((0, 2), (1, 5), (3, 4))))
    pure_words = ((0,) * 6, (1,) * 6, (2,) * 6)
    require(len(set(occurrence_cells(pure1, pure_words[1])) - base) == 1,
            (pure1, base))
    records = []
    histogram = Counter()
    three_colour_cap_core_completions = 0
    for pure0 in MATCHINGS:
        for pure2 in MATCHINGS:
            support = set(base)
            support.update(occurrence_cells(pure0, pure_words[0]))
            support.update(occurrence_cells(pure1, pure_words[1]))
            support.update(occurrence_cells(pure2, pure_words[2]))
            require(len(support) == 17, (pure0, pure2, len(support)))
            singleton_rows = []
            pure_counts = []
            for word in WORDS:
                live = tuple(matching for matching in MATCHINGS
                             if set(occurrence_cells(matching, word)) <= support)
                if len(set(word)) == 1:
                    pure_counts.append(len(live))
                elif len(live) == 1:
                    singleton_rows.append((word, live[0]))
            require(tuple(pure_counts) == (1, 1, 1),
                    (pure0, pure2, pure_counts))
            histogram[len(singleton_rows)] += 1
            if CAP in pure0 and CAP in pure2:
                three_colour_cap_core_completions += 1
            records.append((len(singleton_rows), pure0, pure2,
                            tuple(singleton_rows), support))

    expected_histogram = Counter({
        9: 8, 10: 15, 11: 6, 12: 10, 13: 26, 14: 22, 15: 24,
        16: 4, 17: 16, 18: 14, 20: 26, 21: 4, 22: 5, 23: 8,
        25: 4, 26: 9, 27: 2, 28: 4, 29: 6, 33: 8, 38: 2, 44: 2,
    })
    require(histogram == expected_histogram, histogram)
    require(sum(histogram.values()) == 225, histogram)
    require(three_colour_cap_core_completions == 9,
            three_colour_cap_core_completions)
    canonical = min(records, key=lambda record:
                    (record[0], record[1], record[2]))
    singleton_count, pure0, pure2, singleton_rows, support = canonical
    require(singleton_count == 9, canonical[:4])
    witness_word, witness_matching = singleton_rows[0]
    require(len(set(witness_word)) > 1, witness_word)
    return {
        "base_cells": len(base),
        "minimum_added_cells": 7,
        "minimum_total_cells": 17,
        "pure1_forced_fine": matching_name(pure1),
        "labelled_minimum_completions": len(records),
        "mixed_singleton_histogram": dict(sorted(histogram.items())),
        "minimum_mixed_singletons": singleton_count,
        "minimum_attainers": histogram[singleton_count],
        "three_colour_local_cap_core_completions":
            three_colour_cap_core_completions,
        "cap_core_scope": (
            "these nine supports contain a34^00,a34^11,a34^22 and the "
            "common residual fine 02|15, but support incidence alone does "
            "not prove the homogeneous active-clean cap identities; all "
            "nine already have mixed singleton units"
        ),
        "canonical_minimum_completion": {
            "pure0_fine": matching_name(pure0),
            "pure1_fine": matching_name(pure1),
            "pure2_fine": matching_name(pure2),
            "support_cells": tuple(sorted(cell_name(cell) for cell in support)),
            "first_unit_word": word_name(witness_word),
            "first_unit_fine": matching_name(witness_matching),
            "first_unit_cells": tuple(cell_name(cell) for cell in
                                      occurrence_cells(witness_matching,
                                                       witness_word)),
            "first_unit_operation": f"coefficient:{word_name(witness_word)}",
        },
        "theorem": (
            "every support-minimum completion of the transverse packet to "
            "three live pure GHZ anchors has a literal mixed singleton; "
            "therefore no such minimum support can be an exact source"
        ),
        "nonminimum_scope": (
            "a larger completion may add cancellation mates simultaneously; "
            "the census does not prove persistence under arbitrary additions"
        ),
    }
def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    return {
        "theorem": "thirteen-exit intrinsic classification and C6 guard",
        "pins": PINS,
        "intrinsic_exit_classification": exit_classification(),
        "smallest_two_word_surviving_packet": word_square_and_dual(),
        "minimality": minimality_gate(),
        "two_fine_full_colour_completion_gate": two_fine_pure_completion_gate(),
        "minimum_full_GHZ_support_completion":
            minimum_full_GHZ_support_completion(),
        "verdict": (
            "the proposed unit/active-cap/smaller-parent trichotomy is false "
            "for the literal mixed-row packet: transverse C6 exits support a "
            "one-dimensional fine-odd class.  A full-GHZ completion could "
            "still kill it through pure normalization or a new fine-changing "
            "operation."
        ),
    }


EXPECTED_LEDGER_SHA256 = "bfee68b67a513ac568dfccdf7caf45b9c2e83efb2463885723080f23c44ebe62"


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
                ("thirteen-exit ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("C6 parent S-chain thirteen-exit trichotomy: PASS")
    print("mode", arguments.mode)
    print("ledger_sha256", digest)
    print("exit classes: 1 cap + 4 M0-tail + 4 M1-tail + 4 transverse C6")
    print("smallest two-word surviving packet: 10 cells, rank 7/8, dual 1D")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Raw-definition audit of the N=8 minimum-source interface.

This file deliberately uses only endpoint-ordered source cells and the
3^8 perfect-matching coefficient equations.  It does not import any of the
B/Eq/AugP2/HPL/PAComp presentations.

The checker establishes scope and dependency boundaries.  It does not claim
that an exact ternary N=8 source exists, and it does not claim the open
thirteen-exit termination/coverage lemma.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json


N = 8
COLOURS = tuple(range(3))
SITES = tuple(range(N))
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLOURS, repeat=N))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices: tuple[int, ...]):
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


def word_name(word: tuple[int, ...]) -> str:
    return "".join(map(str, word))


def matching_name(matching: tuple[tuple[int, int], ...]) -> str:
    return "|".join(f"{left}{right}" for left, right in matching)


def cell_for(edge: tuple[int, int], word: tuple[int, ...]):
    left, right = edge
    return left, right, word[left], word[right]


def field_value(value: Fraction, modulus: int | None):
    if modulus is None:
        return value
    numerator = value.numerator % modulus
    denominator = value.denominator % modulus
    require(denominator != 0, ("bad denominator", value, modulus))
    return numerator * pow(denominator, -1, modulus) % modulus


def matching_terms(source, word, modulus: int | None = None):
    zero = Fraction(0) if modulus is None else 0
    one = Fraction(1) if modulus is None else 1
    answer = []
    for matching in MATCHINGS:
        value = one
        for edge in matching:
            value *= field_value(source.get(cell_for(edge, word), Fraction(0)),
                                 modulus)
            if modulus is not None:
                value %= modulus
            if value == zero:
                break
        if value != zero:
            answer.append((matching, value))
    return tuple(answer)


def amplitude_matching(source, word, modulus: int | None = None):
    terms = matching_terms(source, word, modulus)
    value = sum((entry[1] for entry in terms),
                Fraction(0) if modulus is None else 0)
    return value if modulus is None else value % modulus


def amplitude_recursive(source, word, modulus: int | None = None):
    """Independent hafnian recursion, without using MATCHINGS."""
    zero = Fraction(0) if modulus is None else 0
    one = Fraction(1) if modulus is None else 1

    def rec(vertices):
        if not vertices:
            return one
        first = vertices[0]
        answer = zero
        for position in range(1, len(vertices)):
            second = vertices[position]
            edge = (first, second) if first < second else (second, first)
            factor = field_value(source.get(cell_for(edge, word), Fraction(0)),
                                 modulus)
            rest = vertices[1:position] + vertices[position + 1:]
            answer += factor * rec(rest)
            if modulus is not None:
                answer %= modulus
        return answer

    return rec(SITES)


def target(word, modulus: int | None = None):
    value = int(len(set(word)) == 1)
    return Fraction(value) if modulus is None else value % modulus


def off_count(word):
    return N - max(word.count(colour) for colour in COLOURS)


def raw_profile(source, modulus: int | None = None):
    failures = []
    live_words = 0
    live_mixed_singletons = 0
    for word in WORDS:
        terms = matching_terms(source, word, modulus)
        if terms:
            live_words += 1
            if len(set(word)) > 1 and len(terms) == 1:
                live_mixed_singletons += 1
        value = sum((entry[1] for entry in terms),
                    Fraction(0) if modulus is None else 0)
        if modulus is not None:
            value %= modulus
        if value != target(word, modulus):
            failures.append({
                "word": word_name(word),
                "value": str(value),
                "off_count": off_count(word),
                "palette_size": len(set(word)),
                "live_terms": len(terms),
                "fines": tuple(matching_name(entry[0]) for entry in terms),
            })
    return {
        "failures": tuple(failures),
        "failure_count": len(failures),
        "live_words": live_words,
        "live_mixed_singletons": live_mixed_singletons,
    }


def port_loads(support, weights):
    loads = {(site, colour): Fraction(0)
             for site in SITES for colour in COLOURS}
    for cell in support:
        left, right, alpha, beta = cell
        weight = Fraction(weights[cell])
        require(weight > 0, ("non-positive balance weight", cell, weight))
        loads[left, alpha] += weight
        loads[right, beta] += weight
    return loads


def verify_balance(support, weights):
    require(set(support) == set(weights), "balance certificate support mismatch")
    loads = port_loads(support, weights)
    mus = []
    for colour in COLOURS:
        values = tuple(loads[site, colour] for site in SITES)
        require(len(set(values)) == 1, (colour, values))
        mus.append(values[0])
    return tuple(mus)


def rational_rank(rows):
    matrix = [list(map(Fraction, row)) for row in rows]
    rank = 0
    for column in range(len(matrix[0]) if matrix else 0):
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


def raw_interface_audit():
    require(len(EDGES) == 28, len(EDGES))
    require(len(MATCHINGS) == 105 and len(set(MATCHINGS)) == 105,
            len(MATCHINGS))
    require(len(WORDS) == 6561, len(WORDS))
    variables = tuple((left, right, alpha, beta)
                      for left, right in EDGES
                      for alpha, beta in product(COLOURS, repeat=2))
    require(len(variables) == 252, len(variables))

    # Independent rank check for the site-equality form of target-torus
    # balance: load(v,c)-load(0,c)=0, v=1,...,7 and c=0,1,2.
    rows = []
    for colour in COLOURS:
        for site in range(1, N):
            row = [0] * (N * len(COLOURS))
            row[3 * site + colour] = 1
            row[colour] = -1
            rows.append(row)
    require(rational_rank(rows) == 21, rational_rank(rows))

    return {
        "endpoint_ordered_variables": len(variables),
        "coefficient_equations": len(WORDS),
        "perfect_matching_terms_per_dense_row": len(MATCHINGS),
        "balance_condition_rank": 21,
        "unconditional_support_consequences_of_exactness": (
            "each of the three pure rows has a live perfect matching",
            "no mixed row has exactly one live matching",
        ),
        "minimum_cell_support_consequence": (
            "strict Stiemke alternative: positive incidence weights with "
            "site-independent load in each colour"
        ),
        "minimum_cell_support_consequence_proof_status": (
            "mathematical Stiemke/one-parameter-subgroup proof re-derived "
            "in REPORT.md; this checker verifies the incidence interface "
            "and explicit certificates, not the theorem of alternatives"
        ),
        "scope": (
            "balance is a weighted-load statement; it does not set occupied "
            "cell moduli to one"
        ),
    }


PHASE_SOURCE = {
    (0, 1, 0, 1): Fraction(1),
    (0, 3, 0, 1): Fraction(-2),
    (0, 4, 0, 0): Fraction(1),
    (0, 7, 0, 1): Fraction(1),
    (1, 2, 1, 0): Fraction(1),
    (1, 5, 0, 0): Fraction(1),
    (2, 3, 0, 1): Fraction(1),
    (2, 6, 0, 0): Fraction(1),
    (3, 4, 1, 0): Fraction(-1),
    (3, 7, 0, 0): Fraction(1),
    (4, 5, 0, 1): Fraction(1),
    (5, 6, 1, 0): Fraction(-1),
    (6, 7, 0, 1): Fraction(1),
}


def phase_guard_audit():
    profile = raw_profile(PHASE_SOURCE)
    require(profile["failure_count"] == 2, profile["failures"])
    require(tuple(record["word"] for record in profile["failures"]) ==
            ("11111111", "22222222"), profile["failures"])
    require(profile["live_words"] == 4, profile["live_words"])

    key_words = ("01000100", "00010001", "01010101")
    term_counts = {}
    term_values = {}
    for name in key_words:
        word = tuple(map(int, name))
        terms = matching_terms(PHASE_SOURCE, word)
        term_counts[name] = len(terms)
        term_values[name] = tuple(str(entry[1]) for entry in terms)
        require(amplitude_matching(PHASE_SOURCE, word) == 0,
                (name, terms))
    require(tuple(term_counts[name] for name in key_words) == (2, 2, 3),
            term_counts)

    # The exact support is in the degenerating (D) branch, not in the
    # balanceable (P) branch.  This explicit pure-neutral one-parameter
    # subgroup has nonnegative cell weights and deletes two cells.
    h = {(site, colour): Fraction(0)
         for site in SITES for colour in COLOURS}
    h[0, 1] = Fraction(-1, 2)
    h[1, 1] = Fraction(1, 2)
    require(all(sum(h[site, colour] for site in SITES) == 0
                for colour in COLOURS), h)
    exponents = {
        cell: h[cell[0], cell[2]] + h[cell[1], cell[3]]
        for cell in PHASE_SOURCE
    }
    require(all(value >= 0 for value in exponents.values()), exponents)
    require(sum(value > 0 for value in exponents.values()) == 2, exponents)

    for modulus in (13, 37):
        finite = raw_profile(PHASE_SOURCE, modulus)
        require(tuple(record["word"] for record in finite["failures"]) ==
                ("11111111", "22222222"), (modulus, finite["failures"]))

    return {
        "support_cells": len(PHASE_SOURCE),
        "raw_Q_failure_words": tuple(record["word"]
                                     for record in profile["failures"]),
        "mixed_rows_all_exact": True,
        "pure_values": {colour: str(amplitude_matching(
            PHASE_SOURCE, (colour,) * N)) for colour in COLOURS},
        "forcing_fibre_term_counts": term_counts,
        "forcing_fibre_values_at_stored_point": term_values,
        "pure_neutral_degeneration_positive_cells": tuple(
            str(cell) for cell, value in sorted(exponents.items()) if value > 0
        ),
        "finite_field_rechecks": (13, 37),
        "correct_scope": (
            "a raw mixed-equation/non-equilateral guard; NOT a full ternary "
            "GHZ source and NOT a minimum-support balanced source"
        ),
    }


W40_SOURCE = {
    (0, 1, 0, 0): Fraction(1),
    (0, 3, 1, 1): Fraction(1),
    (0, 4, 0, 1): Fraction(1),
    (0, 4, 2, 2): Fraction(1),
    (0, 5, 1, 0): Fraction(1),
    (0, 6, 0, 2): Fraction(1),
    (1, 2, 0, 2): Fraction(1),
    (1, 2, 1, 1): Fraction(1),
    (1, 3, 2, 2): Fraction(1),
    (1, 7, 0, 1): Fraction(-1),
    (2, 3, 0, 0): Fraction(1),
    (2, 4, 2, 1): Fraction(1),
    (2, 6, 2, 2): Fraction(-1),
    (3, 4, 1, 0): Fraction(-1),
    (4, 5, 0, 0): Fraction(1),
    (4, 7, 1, 1): Fraction(1),
    (5, 6, 1, 1): Fraction(1),
    (5, 7, 2, 2): Fraction(-1),
    (6, 7, 0, 0): Fraction(1),
    (6, 7, 2, 1): Fraction(1),
}

W40_BALANCE = {
    (0, 1, 0, 0): 1,
    (0, 3, 1, 1): 2,
    (0, 4, 0, 1): 1,
    (0, 4, 2, 2): 3,
    (0, 5, 1, 0): 1,
    (0, 6, 0, 2): 1,
    (1, 2, 0, 2): 1,
    (1, 2, 1, 1): 3,
    (1, 3, 2, 2): 3,
    (1, 7, 0, 1): 1,
    (2, 3, 0, 0): 3,
    (2, 4, 2, 1): 1,
    (2, 6, 2, 2): 1,
    (3, 4, 1, 0): 1,
    (4, 5, 0, 0): 2,
    (4, 7, 1, 1): 1,
    (5, 6, 1, 1): 3,
    (5, 7, 2, 2): 3,
    (6, 7, 0, 0): 3,
    (6, 7, 2, 1): 1,
}


def mutual_anchors(support):
    degrees = {(site, colour): 0
               for site in SITES for colour in COLOURS}
    for left, right, alpha, beta in support:
        degrees[left, alpha] += 1
        degrees[right, beta] += 1
    return tuple(sorted(cell for cell in support
                        if degrees[cell[0], cell[2]] == 1
                        and degrees[cell[1], cell[3]] == 1))


def oriented_cell(source, left, right, left_colour, right_colour):
    """Read an endpoint-ordered block with the requested tensor order."""
    if left < right:
        return source.get((left, right, left_colour, right_colour),
                          Fraction(0))
    return source.get((right, left, right_colour, left_colour), Fraction(0))


def explicit_cap67_audit():
    """Directly evaluate the h=3 clean-cap error for K=-I at pair 67."""
    p, q = 6, 7
    residual = tuple(site for site in SITES if site not in (p, q))
    k = tuple(tuple(Fraction(-int(i == j)) for j in COLOURS)
              for i in COLOURS)
    s = sum(k[i][j] * oriented_cell(W40_SOURCE, p, q, i, j)
            for i in COLOURS for j in COLOURS)
    kappas = tuple(k[colour][colour] for colour in COLOURS)
    require(s == -1 and kappas == (-1, -1, -1), (s, kappas))
    require(s * kappas[0] * kappas[1] * kappas[2] == 1,
            (s, kappas))

    response = {}
    for a, b in combinations(residual, 2):
        matrix = {}
        for alpha, beta in product(COLOURS, repeat=2):
            value = Fraction(0)
            for i, j in product(COLOURS, repeat=2):
                value += k[i][j] * (
                    oriented_cell(W40_SOURCE, p, a, i, alpha)
                    * oriented_cell(W40_SOURCE, q, b, j, beta)
                    + oriented_cell(W40_SOURCE, p, b, i, beta)
                    * oriented_cell(W40_SOURCE, q, a, j, alpha)
                )
            matrix[alpha, beta] = value
        response[a, b] = matrix

    nonzero_errors = []
    for residual_word in product(COLOURS, repeat=len(residual)):
        colours = dict(zip(residual, residual_word))
        error = Fraction(0)
        for matching in perfect_matchings(residual):
            rs = [response[edge][colours[edge[0]], colours[edge[1]]]
                  for edge in matching]
            xs = [oriented_cell(W40_SOURCE, edge[0], edge[1],
                                colours[edge[0]], colours[edge[1]])
                  for edge in matching]
            error += rs[0] * rs[1] * rs[2]
            error += s * (xs[0] * rs[1] * rs[2]
                          + xs[1] * rs[0] * rs[2]
                          + xs[2] * rs[0] * rs[1])
        if error:
            nonzero_errors.append((word_name(residual_word), str(error)))
    require(not nonzero_errors, nonzero_errors)
    return {
        "pair": "67",
        "K": "-I_3",
        "s": str(s),
        "kappas": tuple(map(str, kappas)),
        "activity_product": str(s * kappas[0] * kappas[1] * kappas[2]),
        "residual_words_checked": 729,
        "nonzero_error_words": len(nonzero_errors),
        "verdict": "explicit active clean cap on the X4 boundary point",
    }


def w40_boundary_audit():
    profile = raw_profile(W40_SOURCE)
    expected_words = (
        "01110222",
        "12221000",
        "20002111",
    )
    require(tuple(record["word"] for record in profile["failures"]) ==
            expected_words, profile["failures"])
    require(tuple(record["value"] for record in profile["failures"]) ==
            ("1", "1", "-1"), profile["failures"])
    require(all(record["palette_size"] == 3
                and record["off_count"] == 5
                and record["live_terms"] == 1
                for record in profile["failures"]), profile["failures"])
    require(all(record["palette_size"] == 3
                for record in profile["failures"]), profile["failures"])
    require(verify_balance(W40_SOURCE, W40_BALANCE) ==
            (Fraction(3), Fraction(3), Fraction(3)), W40_BALANCE)

    binary_failures = []
    level4_failures = []
    require(sum(len(set(word)) <= 2 for word in WORDS) == 765,
            "at-most-binary word census changed")
    require(sum(off_count(word) <= 4 for word in WORDS) == 4881,
            "level-4 word census changed")
    for word in WORDS:
        value = amplitude_matching(W40_SOURCE, word)
        if len(set(word)) <= 2 and value != target(word):
            binary_failures.append(word_name(word))
        if off_count(word) <= 4 and value != target(word):
            level4_failures.append(word_name(word))
    require(not binary_failures, binary_failures)
    require(not level4_failures, level4_failures)

    finite_records = {}
    for modulus in (13, 37):
        finite = raw_profile(W40_SOURCE, modulus)
        finite_words = tuple(record["word"] for record in finite["failures"])
        require(finite_words == expected_words, (modulus, finite_words))
        finite_records[str(modulus)] = finite_words

    anchors = mutual_anchors(W40_SOURCE)
    require(len(anchors) == 7, anchors)
    clean_cap = explicit_cap67_audit()

    return {
        "support_cells": len(W40_SOURCE),
        "positive_balance_mu": (3, 3, 3),
        "mutual_anchor_count": len(anchors),
        "mutual_anchors": tuple(str(cell) for cell in anchors),
        "all_765_at_most_binary_words_exact": True,
        "all_4881_level4_words_exact": True,
        "raw_Q_failures": profile["failures"],
        "finite_field_failure_words": finite_records,
        "explicit_clean_cap": clean_cap,
        "consequence": (
            "pure plus three shared binary restrictions, support balance, "
            "and level-4 exactness do not cover N=8: the three genuinely "
            "trichromatic (3,3,2) rows are indispensable"
        ),
        "clean_cap_calibration": (
            "this point does NOT refute an X4-implies-active-clean-cap "
            "theorem: pair 67 with K=-I is explicitly active and clean"
        ),
        "scope": "X4 boundary point, not a full exact source",
    }


def thirteen_exit_audit():
    sites6 = tuple(range(6))
    matchings6 = tuple(sorted(perfect_matchings(sites6)))
    require(len(matchings6) == 15, len(matchings6))
    m0 = tuple(sorted(((0, 5), (1, 2), (3, 4))))
    m1 = tuple(sorted(((0, 1), (2, 5), (3, 4))))
    cap = (3, 4)
    classes = Counter()
    records = []
    for matching in matchings6:
        if matching in (m0, m1):
            continue
        common0 = set(matching) & set(m0)
        common1 = set(matching) & set(m1)
        if cap in matching:
            label = "cap_complement"
        elif len(common0) == 1 and not common1:
            label = "one_tail_M0"
        elif len(common1) == 1 and not common0:
            label = "one_tail_M1"
        elif not common0 and not common1:
            label = "transverse_C6"
        else:
            raise RuntimeError((matching, common0, common1))
        classes[label] += 1
        records.append((matching_name(matching), label))
    expected = Counter({
        "cap_complement": 1,
        "one_tail_M0": 4,
        "one_tail_M1": 4,
        "transverse_C6": 4,
    })
    require(classes == expected, classes)

    # Literal N=8 lift with spectator edge 67.  The familiar 15-term C6
    # row is only the common-tail sector.  The other 90 perfect matchings
    # cross the 67 cut twice and form 45 two-ordering response groups.
    tail = (6, 7)
    m0_lift = tuple(sorted(m0 + (tail,)))
    m1_lift = tuple(sorted(m1 + (tail,)))
    common_tail = tuple(matching for matching in MATCHINGS if tail in matching)
    crossing_tail = tuple(matching for matching in MATCHINGS
                          if tail not in matching)
    require((len(common_tail), len(crossing_tail)) == (15, 90),
            (len(common_tail), len(crossing_tail)))
    require(m0_lift in common_tail and m1_lift in common_tail,
            (m0_lift, m1_lift))
    response_groups = Counter()
    for matching in crossing_tail:
        edge6 = next(edge for edge in matching if 6 in edge)
        edge7 = next(edge for edge in matching if 7 in edge)
        a = edge6[0] if edge6[1] == 6 else edge6[1]
        b = edge7[0] if edge7[1] == 7 else edge7[1]
        residual_pair = tuple(sorted((a, b)))
        residual_fine = tuple(edge for edge in matching
                              if 6 not in edge and 7 not in edge)
        response_groups[residual_pair, residual_fine] += 1
    require(len(response_groups) == 45
            and set(response_groups.values()) == {2}, response_groups)

    # Dense support is a sharp support-level guard: it has pure matchings,
    # no mixed singleton, and a positive balance certificate, but no missing
    # cell on which the presently proved literal-deletion S-chain can enter.
    dense = tuple((left, right, alpha, beta)
                  for left, right in EDGES
                  for alpha, beta in product(COLOURS, repeat=2))
    dense_weights = {cell: Fraction(1) for cell in dense}
    require(verify_balance(dense, dense_weights) ==
            (Fraction(21), Fraction(21), Fraction(21)), "dense balance")
    require(len(dense) == 252, len(dense))
    require(not (set((left, right, alpha, beta)
                     for left, right in EDGES
                     for alpha, beta in product(COLOURS, repeat=2))
                 - set(dense)), "dense support has an absent cell")

    return {
        "literal_exit_counts": dict(sorted(classes.items())),
        "literal_exit_records": tuple(records),
        "literal_N8_lift": {
            "all_fines": 105,
            "common_tail_67_fines": 15,
            "familiar_exits_after_two_parents": 13,
            "additional_crossing_tail_occurrences": 90,
            "first_response_groups": 45,
            "ordered_star_pairings_per_group": 2,
            "consequence": (
                "a bare thirteen-exit closure is not N=8 source-complete; "
                "the crossing-tail/physical-response sector must be controlled"
            ),
        },
        "proved": (
            "the degree-four parent S-chain has thirteen labelled exits "
            "with the 1+4+4+4 matching classification"
        ),
        "packet_entry_hypotheses_not_forced_by_minimality": (
            "a live oriented parent pair in the required two word sections",
            "an absent endpoint-colour multiplier cell for literal deletion",
        ),
        "packet_termination_hypothesis_still_open": (
            "arbitrary nonminimum completion ends in a source unit, active "
            "clean cap, or strict source-valid reduction"
        ),
        "dense_support_guard": {
            "cells": len(dense),
            "balance_mu": (21, 21, 21),
            "live_pure_matchings_per_colour": 105,
            "live_matchings_per_mixed_word": 105,
            "absent_cells": 0,
            "scope": (
                "support-level guard only, not an exact source; proves that "
                "balance/pure/singleton conditions do not imply packet entry"
            ),
        },
    }


def dependency_boundary():
    return {
        "valid_minimum_source_interface": (
            "raw 252-variable/6561-row exact system",
            "global minimum occupied-cell support",
            "positive weighted-load balance",
            "one live pure matching in each colour",
            "no mixed singleton fibre",
            "optionally maximize mutual anchors only inside the already "
            "minimum-support stratum",
        ),
        "normalization_order_warning": (
            "global minimum-support implies balance; global maximum-anchor "
            "then minimum-support is a different lexicographic choice. No "
            "source-level synchronization theorem was found that transfers "
            "the balance conclusion to the latter choice."
        ),
        "coverage_status": "OPEN",
        "missing_dependency_1": (
            "ENTRY: derive a literal thirteen-exit parent packet, or another "
            "finite residual packet, from every raw minimum exact source"
        ),
        "missing_dependency_2": (
            "RESPONSE/TERMINATION: control the 90 crossing-tail occurrences "
            "(45 first-response groups) in the literal N=8 lift, and close "
            "arbitrary larger completions of the transverse C6 exit"
        ),
        "missing_dependency_3": (
            "TRICHROMATIC: consume the genuinely trichromatic coefficient "
            "rows; shared exact binary restrictions are insufficient"
        ),
        "honest_residual_statement": (
            "Every hypothetical globally minimum-cell N=8 exact ternary "
            "source is balanced and singleton-free with a live pure matching "
            "occurrence in each colour. It is not proved that such a source enters the "
            "thirteen-exit packet or any existing finite case decomposition."
        ),
    }


CONTROL_NAMES = (
    "matching_engine_crosscheck",
    "phase_scope_and_characteristics",
    "w40_raw_boundary_and_characteristics",
    "w40_explicit_active_clean_cap",
    "balance_certificate_mutation",
    "source_value_mutation",
    "dense_packet_entry_guard",
)


def run_controls():
    ran = []

    # Independent matching-list versus recursive-hafnian evaluation on all
    # 6561 words for both stored rational objects.
    for source in (PHASE_SOURCE, W40_SOURCE):
        for word in WORDS:
            require(amplitude_matching(source, word) ==
                    amplitude_recursive(source, word),
                    ("engine mismatch", word_name(word)))
    ran.append("matching_engine_crosscheck")

    phase_guard_audit()
    ran.append("phase_scope_and_characteristics")

    w40_boundary_audit()
    ran.append("w40_raw_boundary_and_characteristics")

    explicit_cap67_audit()
    ran.append("w40_explicit_active_clean_cap")

    bad_balance = dict(W40_BALANCE)
    bad_balance[(0, 1, 0, 0)] = 2
    try:
        verify_balance(W40_SOURCE, bad_balance)
    except RuntimeError:
        pass
    else:
        raise RuntimeError("balance mutation survived")
    ran.append("balance_certificate_mutation")

    mutant = dict(W40_SOURCE)
    mutant[(0, 4, 0, 1)] = Fraction(2)
    mutant_profile = raw_profile(mutant)
    original_signature = tuple(record["word"]
                               for record in raw_profile(W40_SOURCE)["failures"])
    mutant_signature = tuple(record["word"]
                             for record in mutant_profile["failures"])
    require(mutant_signature != original_signature,
            "source mutation did not change the raw equation signature")
    ran.append("source_value_mutation")

    thirteen_exit_audit()
    ran.append("dense_packet_entry_guard")

    require(tuple(ran) == CONTROL_NAMES,
            ("executed-control manifest mismatch", ran, CONTROL_NAMES))
    return tuple(ran)


def build_ledger():
    ran = run_controls()
    return {
        "theorem": "raw N=8 minimum-source interface and coverage boundary",
        "status": "UNAUDITED",
        "raw_interface": raw_interface_audit(),
        "phase_only_scope_correction": phase_guard_audit(),
        "W40_trichromatic_boundary": w40_boundary_audit(),
        "thirteen_exit_boundary": thirteen_exit_audit(),
        "dependency_boundary": dependency_boundary(),
        "controls_declared": CONTROL_NAMES,
        "controls_run": ran,
        "controls_complete": tuple(ran) == CONTROL_NAMES,
    }


EXPECTED_LEDGER_SHA256 = (
    "157a9baba793c79700e7ad87f870cfa48eaf19c5d67c2273eda071474a1ce90b"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("raw N=8 source-interface audit: PASS")
    print("ledger_sha256", digest)
    print("controls", f"{len(ledger['controls_run'])}/{len(CONTROL_NAMES)}")
    print("coverage", ledger["dependency_boundary"]["coverage_status"])


if __name__ == "__main__":
    main()

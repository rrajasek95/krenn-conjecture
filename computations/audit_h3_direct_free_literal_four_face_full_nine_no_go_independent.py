#!/usr/bin/env python3
"""Independent audit of the strict four-face full-nine no-go.

This checker imports nothing from the primary executable.  It brute-forces
the compatible global words from the fine slot degree, reconstructs every
quadratic multiplier as a pairing of the four missing slots, builds all five
48-column sparse polynomial blocks, and audits the chart partitions and five
external second polars exactly.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


Q = Fraction
ZERO = Q(0)
ONE = Q(1)
COLOURS = (0, 1, 2)
ALL_SITES = tuple(range(8))
X_SITE = 0
ODD_SITES = (1, 2, 3, 4, 5)
P_SITE = 6
Q_SITE = 7
R_SITE = 3
RESET = (1, 2, 1, 1, 2)
PURE = (0,) * 8
EXPECTED_DIGEST = "4fc5b2bc9bdc32e3b558aa7fe83ae0ca588447591d58131dc04dad9f8229314b"


EXPECTED_COUNTS = {
    1: (3564, 2880, 60),
    2: (3564, 2880, 60),
    3: (3672, 3072, 64),
    4: (3564, 2880, 60),
    5: (3564, 2880, 60),
}


def check(condition, message):
    if not condition:
        raise AssertionError(message)


@lru_cache(maxsize=None)
def pairings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:]):
        remainder = vertices[1 : index + 1] + vertices[index + 2 :]
        for tail in pairings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def labelled_edge(left, right, left_colour, right_colour):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def topology_has(matching, left, right):
    wanted = frozenset((left, right))
    return any(frozenset(edge) == wanted for edge in matching)


def matching_term(matching, word):
    return tuple(sorted(
        labelled_edge(left, right, word[left], word[right])
        for left, right in matching
    ))


@lru_cache(maxsize=None)
def direct_free_hafnian(word):
    terms = []
    for matching in pairings(ALL_SITES):
        if topology_has(matching, P_SITE, R_SITE):
            continue
        terms.append(matching_term(matching, word))
    check(len(terms) == 90, "direct-free eight-site hafnian changed size")
    check(len(set(terms)) == 90, "direct-free hafnian acquired monomial collision")
    return tuple(sorted(terms))


def slot_degree_of_word(word):
    return Counter((site, word[site]) for site in ALL_SITES)


def slot_degree_of_edges(edges):
    degree = Counter()
    for left, right, left_colour, right_colour in edges:
        degree[(left, left_colour)] += 1
        degree[(right, right_colour)] += 1
    return degree


def lambda_degree(deleted):
    face = tuple(site for site in ODD_SITES if site != deleted)
    degree = Counter((site, 0) for site in (X_SITE, deleted, P_SITE, Q_SITE))
    for site in face:
        degree[(site, 0)] += 1
        degree[(site, RESET[site - 1])] += 1
    return degree


def compatible_words_by_bruteforce(deleted):
    target_degree = lambda_degree(deleted)
    words = []
    for word in product(COLOURS, repeat=8):
        degree = slot_degree_of_word(word)
        if all(degree[key] <= target_degree[key] for key in degree):
            words.append(word)
    check(len(words) == 16, f"face {deleted}: compatible-word count changed")
    return tuple(words)


def missing_slots(target_degree, word):
    remaining = target_degree - slot_degree_of_word(word)
    slots = []
    for slot, multiplicity in remaining.items():
        slots.extend([slot] * multiplicity)
    check(len(slots) == 4, "fine-degree deficit is not four slots")
    check(len({site for site, _colour in slots}) == 4,
          "fine-degree deficit repeated a site")
    return tuple(sorted(slots))


def multipliers_from_missing_slots(slots):
    candidates = []
    for pairing in pairings(tuple(range(4))):
        edges = []
        for left_index, right_index in pairing:
            left_site, left_colour = slots[left_index]
            right_site, right_colour = slots[right_index]
            edges.append(labelled_edge(
                left_site, right_site, left_colour, right_colour
            ))
        candidates.append(tuple(sorted(edges)))
    check(len(set(candidates)) == 3, "quadratic deficit multipliers changed")
    return tuple(sorted(candidates))


def face_hafnian(deleted):
    face = tuple(site for site in ODD_SITES if site != deleted)
    word = {site: RESET[site - 1] for site in face}
    return tuple(sorted(
        tuple(sorted(
            labelled_edge(left, right, word[left], word[right])
            for left, right in matching
        ))
        for matching in pairings(face)
    ))


def build_block(deleted):
    target_degree = lambda_degree(deleted)
    labels = []
    columns = []
    for word in compatible_words_by_bruteforce(deleted):
        slots = missing_slots(target_degree, word)
        for multiplier in multipliers_from_missing_slots(slots):
            check(
                slot_degree_of_word(word) + slot_degree_of_edges(multiplier)
                == target_degree,
                f"face {deleted}: multiplier has wrong fine degree",
            )
            coefficient_counter = Counter(
                tuple(sorted(row_term + multiplier))
                for row_term in direct_free_hafnian(word)
            )
            check(len(coefficient_counter) == 90, "multiplied column collided")
            check(set(coefficient_counter.values()) == {1}, "bad feature coefficient")
            labels.append((word, multiplier))
            columns.append(frozenset(coefficient_counter))
    check(len(columns) == 48, f"face {deleted}: block is not 48 columns")
    return tuple(labels), tuple(columns)


def block_checks():
    records = []
    for deleted in ODD_SITES:
        labels, columns = build_block(deleted)
        owners = defaultdict(set)
        for column_index, column in enumerate(columns):
            for feature in column:
                owners[feature].add(column_index)

        unique_by_column = []
        pivot_features = []
        for column_index, column in enumerate(columns):
            unique = sorted(
                feature for feature in column
                if owners[feature] == {column_index}
            )
            check(unique, f"face {deleted}: column {column_index} has no pivot")
            unique_by_column.append(len(unique))
            pivot_features.append(unique[0])
        check(len(set(pivot_features)) == 48, "unique pivot features collided")

        feature_count = len(owners)
        unique_total = sum(len(owner_set) == 1 for owner_set in owners.values())
        expected_feature_count, expected_unique, expected_per_column = EXPECTED_COUNTS[deleted]
        check(feature_count == expected_feature_count, f"face {deleted}: feature count changed")
        check(unique_total == expected_unique, f"face {deleted}: unique count changed")
        check(set(unique_by_column) == {expected_per_column},
              f"face {deleted}: unique-per-column count changed")

        # The pure row has exactly the three multipliers h_v.  Since the
        # one-chart block is injective, these target initials cannot occur in
        # a nonzero strict one-chart syzygy.
        pure_multipliers = {
            multiplier for word, multiplier in labels if word == PURE
        }
        check(pure_multipliers == set(face_hafnian(deleted)),
              f"face {deleted}: pure target multipliers are not h_v")

        # For the doubled boundary [C C], injectivity of C gives precisely
        # ker = {(a,-a)}.  Any readout of the form rho(a)+rho(b), including
        # any readout descended from the common global coefficient, vanishes
        # identically on this kernel.  This is an algebraic implication, not
        # a classification of non-diagonal relative readouts.
        one_chart_rank = 48
        doubled_rank = 48
        doubled_kernel = 96 - doubled_rank
        check(doubled_kernel == 48, "doubled comparison kernel changed")

        records.append({
            "deleted": deleted,
            "compatible_words": len({word for word, _ in labels}),
            "multipliers_per_word": 3,
            "columns": len(columns),
            "features": feature_count,
            "unique_features": unique_total,
            "unique_per_column": sorted(set(unique_by_column)),
            "one_chart_rank": one_chart_rank,
            "doubled_rank": doubled_rank,
            "doubled_kernel": doubled_kernel,
            "pure_target_multiplier_terms": len(pure_multipliers),
            "common_coefficient_readout_rank_on_kernel": 0,
        })
    return records


def chart_checks():
    surviving = []
    pq_direct = []
    pq_two_star = []
    pr_direct = []
    pr_two_star = []
    for matching in pairings(ALL_SITES):
        if topology_has(matching, P_SITE, R_SITE):
            continue
        surviving.append(matching)
        if topology_has(matching, P_SITE, Q_SITE):
            pq_direct.append(matching)
        else:
            pq_two_star.append(matching)
        if topology_has(matching, P_SITE, R_SITE):
            pr_direct.append(matching)
        else:
            pr_two_star.append(matching)
    check((len(surviving), len(pq_direct), len(pq_two_star),
           len(pr_direct), len(pr_two_star)) == (90, 15, 75, 0, 90),
          "chart topology counts changed")
    check(set(pq_direct).isdisjoint(pq_two_star), "pq sectors overlap")
    check(set(pq_direct) | set(pq_two_star) == set(surviving), "pq union changed")
    check(set(pr_direct) | set(pr_two_star) == set(surviving), "pr union changed")

    # Edge labels are assigned only after the topology partition.  Every
    # matching covers all sites, so labelled terms stay distinct for every
    # one of the 6561 words.  Reconstruct the rows anyway to audit that the
    # two chart unions and their pure targets agree word by word.
    digest = sha256()
    pure_targets = 0
    for word in product(COLOURS, repeat=8):
        global_terms = {matching_term(matching, word) for matching in surviving}
        pq_terms = {
            matching_term(matching, word)
            for matching in pq_direct + pq_two_star
        }
        pr_terms = {
            matching_term(matching, word)
            for matching in pr_direct + pr_two_star
        }
        check(len(global_terms) == 90, "a labelled global row collided")
        check(pq_terms == pr_terms == global_terms, "chart equations differ")
        target = word[0] if all(colour == word[0] for colour in word) else None
        pure_targets += target is not None
        digest.update(bytes(word))
        digest.update(len(global_terms).to_bytes(2, "big"))
    check(pure_targets == 3, "global target count changed")
    return {
        "words": 3 ** 8,
        "surviving_matchings": len(surviving),
        "pq": [len(pq_direct), len(pq_two_star)],
        "pr": [len(pr_direct), len(pr_two_star)],
        "pure_targets": pure_targets,
        "wordwise_union_digest": digest.hexdigest(),
    }


def differentiate_squarefree(terms, variables):
    variables = tuple(variables)
    result = Counter()
    for term in terms:
        remainder = list(term)
        for variable in variables:
            if variable not in remainder:
                break
            remainder.remove(variable)
        else:
            result[tuple(sorted(remainder))] += 1
    return result


def polar_checks():
    records = []
    supports = []
    for deleted in ODD_SITES:
        word = [0] * 8
        for site in ODD_SITES:
            if site != deleted:
                word[site] = RESET[site - 1]
        word = tuple(word)
        check(word != PURE, "polar row acquired physical target")

        external = (
            labelled_edge(X_SITE, deleted, 0, 0),
            labelled_edge(P_SITE, Q_SITE, 0, 0),
        )
        polar = differentiate_squarefree(direct_free_hafnian(word), external)
        expected = Counter({term: 1 for term in face_hafnian(deleted)})
        check(polar == expected, f"face {deleted}: second polar is not h_v")

        # Partition the already direct-free row by the marked chart edge.
        pq_direct_terms = []
        pq_star_terms = []
        pr_direct_terms = []
        pr_star_terms = []
        for matching in pairings(ALL_SITES):
            if topology_has(matching, P_SITE, R_SITE):
                continue
            term = matching_term(matching, word)
            (pq_direct_terms if topology_has(matching, P_SITE, Q_SITE)
             else pq_star_terms).append(term)
            (pr_direct_terms if topology_has(matching, P_SITE, R_SITE)
             else pr_star_terms).append(term)
        check(differentiate_squarefree(pq_direct_terms, external) == polar,
              f"face {deleted}: pq direct polar changed")
        check(not differentiate_squarefree(pq_star_terms, external),
              f"face {deleted}: pq star sector contributes")
        check(not differentiate_squarefree(pr_direct_terms, external),
              f"face {deleted}: pr direct sector contributes")
        check(differentiate_squarefree(pr_star_terms, external) == polar,
              f"face {deleted}: pr star polar changed")

        support = frozenset(polar)
        check(all(support.isdisjoint(previous) for previous in supports),
              "polar supports on distinct deletion faces overlap")
        supports.append(support)
        records.append({
            "deleted": deleted,
            "global_word": "".join(map(str, word)),
            "face_word": "".join(
                str(RESET[site - 1]) for site in ODD_SITES if site != deleted
            ),
            "target": 0,
            "external_edges": [list(edge) for edge in external],
            "polar_terms": len(polar),
            "pq_sector": "direct",
            "pr_sector": "two_star",
        })
    return records


def execute(mode):
    ledger = {}
    if mode in ("all", "charts"):
        ledger["charts"] = chart_checks()
    if mode in ("all", "blocks"):
        ledger["blocks"] = block_checks()
    if mode in ("all", "polars"):
        ledger["polars"] = polar_checks()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if mode == "all":
        check(digest == EXPECTED_DIGEST, f"independent audit digest changed: {digest}")
    print(f"independent strict four-face full-nine audit ({mode}): PASS")
    if mode in ("all", "charts"):
        print("6561 chart rows independently reconstructed: 15+75 = 0+90")
    if mode in ("all", "blocks"):
        print("all five fine blocks: 48 unique pivots; comparison kernel dimension 48")
    if mode in ("all", "polars"):
        print("five external second polars equal the five three-term h_v")
    print("scope: only readouts factoring through the common coefficient vanish")
    print(f"sha256: {digest}")
    return digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "charts", "blocks", "polars"), default="all"
    )
    arguments = parser.parse_args()
    execute(arguments.mode)


if __name__ == "__main__":
    main()

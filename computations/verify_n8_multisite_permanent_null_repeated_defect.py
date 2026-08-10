#!/usr/bin/env python3
"""Classify the multisite defect of the binary permanent-null cap.

For K=((1,1),(-1,1)), expand R_K^[2] by formal row/column provenance and
then realize its surviving repeated-label sectors in the exact six-site
one-anchor packet.  The latter satisfies all nine response equations (one
diagonal target and eight zero rows), so it is a literal counterguard to
reducing the higher defect from response rows alone.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_h3_one_anchor_selector_four_cut_guard as one_anchor  # noqa: E402


K = ((Fraction(1), Fraction(1)),
     (Fraction(-1), Fraction(1)))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def formal_divided_square():
    """Coefficients on raw p_i p_k s_j s_l products in R_K^[2]."""
    entries = tuple((i, j) for i in range(2) for j in range(2))
    answer = defaultdict(Fraction)
    provenance = defaultdict(list)
    for left_position, (i, j) in enumerate(entries):
        for right_position in range(left_position, len(entries)):
            k, l = entries[right_position]
            coefficient = K[i][j] * K[k][l]
            if right_position == left_position:
                coefficient /= 2
            key = (tuple(sorted((i, k))), tuple(sorted((j, l))))
            answer[key] += coefficient
            provenance[key].append(((i, j), (k, l), coefficient))
    return {key: value for key, value in answer.items() if value}, provenance


def class_name(left, right):
    _, i, j, _ = left
    _, k, l, _ = right
    if i == k and j == l:
        return "same_entry"
    if i == k:
        return "repeated_row"
    if j == l:
        return "repeated_column"
    return "distinct_row_column"


def canonical_component(left_site, left_colour, right_site, right_colour):
    if one_anchor.POS[left_site] < one_anchor.POS[right_site]:
        return left_site, left_colour, right_site, right_colour
    return right_site, right_colour, left_site, left_colour


def labelled_cap_components():
    components = []
    for i in range(2):
        for j in range(2):
            for (left_site, left_colour), left_weight in one_anchor.P[i].items():
                for (right_site, right_colour), right_weight in one_anchor.S[j].items():
                    if left_site == right_site:
                        continue
                    edge = canonical_component(
                        left_site, left_colour, right_site, right_colour
                    )
                    components.append((edge, i, j,
                                       K[i][j] * left_weight * right_weight))
    return tuple(components)


def physical_second_defect():
    """Enumerate q^1 R_K^2 with cap labels retained until summation."""
    q_components = tuple(
        (canonical_component(u, a, v, b), weight)
        for u, a, v, b, weight in one_anchor.Q_EDGES
    )
    cap_components = labelled_cap_components()
    output = defaultdict(lambda: defaultdict(Fraction))
    for q_edge, q_weight in q_components:
        q_sites = {q_edge[0], q_edge[2]}
        for left, right in combinations(cap_components, 2):
            left_edge, _, _, left_weight = left
            right_edge, _, _, right_weight = right
            cap_sites = {
                left_edge[0], left_edge[2], right_edge[0], right_edge[2]
            }
            if len(cap_sites) != 4 or cap_sites & q_sites:
                continue
            word = [None] * len(one_anchor.SITES)
            for edge in (q_edge, left_edge, right_edge):
                word[one_anchor.POS[edge[0]]] = edge[1]
                word[one_anchor.POS[edge[2]]] = edge[3]
            output[tuple(word)][class_name(left, right)] += (
                q_weight * left_weight * right_weight
            )
    return {
        word: {kind: coefficient for kind, coefficient in classes.items()
               if coefficient}
        for word, classes in output.items()
        if any(classes.values())
    }


def aggregate_matching_check():
    family = {}
    for u, a, v, b, weight in one_anchor.Q_EDGES:
        one_anchor.add_edge(family, u, a, v, b, {(1, 0): weight})
    for i in range(2):
        for j in range(2):
            one_anchor.add_outer(
                family, one_anchor.P[i], one_anchor.S[j],
                {(0, 1): K[i][j]},
            )
    tensor = one_anchor.matching_tensor(family)
    return {
        word: polynomial[(1, 2)]
        for word, polynomial in tensor.items()
        if polynomial.get((1, 2))
    }


def main() -> None:
    require(K[0][0] * K[1][1] + K[0][1] * K[1][0] == 0,
            "K lost permanent zero")
    formal, provenance = formal_divided_square()
    expected_formal = {
        ((0, 0), (0, 0)): Fraction(1, 2),
        ((0, 0), (0, 1)): Fraction(1),
        ((0, 0), (1, 1)): Fraction(1, 2),
        ((0, 1), (0, 0)): Fraction(-1),
        ((0, 1), (1, 1)): Fraction(1),
        ((1, 1), (0, 0)): Fraction(1, 2),
        ((1, 1), (0, 1)): Fraction(-1),
        ((1, 1), (1, 1)): Fraction(1, 2),
    }
    require(formal == expected_formal, formal)
    distinct_key = ((0, 1), (0, 1))
    require(distinct_key not in formal
            and sum(item[2] for item in provenance[distinct_key]) == 0,
            "distinct-row/column permanent sector stopped cancelling")

    # All nine literal responses of the one-anchor packet are audited before
    # using it as a quotient counterguard.
    x0 = (0,) * len(one_anchor.SITES)
    response_ledger = {
        (i, j): one_anchor.pair_row(i, j)
        for i in range(3) for j in range(3)
    }
    require(response_ledger[(0, 0)] == {x0: Fraction(1)},
            "the retained diagonal response changed")
    require(all(response_ledger[i, j] == {}
                for i in range(3) for j in range(3) if (i, j) != (0, 0)),
            "a zero response row changed")

    physical = physical_second_defect()
    expected_physical = {
        (0, 0, 1, 0, 0, 1): {"repeated_row": Fraction(2)},
        (0, 1, 0, 0, 1, 0): {"same_entry": Fraction(2)},
        (0, 1, 0, 1, 1, 0): {"same_entry": Fraction(2)},
    }
    require(physical == expected_physical, physical)
    aggregate = aggregate_matching_check()
    require(aggregate == {
        word: sum(classes.values()) for word, classes in physical.items()
    }, aggregate)

    print("N=8 multisite permanent-null repeated defect: PASS")
    print("formal R_K^[2] sectors: 8 repeated / 1 permanent sector cancelled")
    print("literal response rows: one diagonal target + eight exact zeros")
    print("physical q*R_K^[2] normal form: 3 mixed words, coefficients 2,2,2")
    print("provenance: 1 repeated-row word + 2 same-entry words")
    print("scope: response-row counterguard, not a full-three-target source")


if __name__ == "__main__":
    main()

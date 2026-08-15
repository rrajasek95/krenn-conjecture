#!/usr/bin/env python3
"""Audit the forced-pure-escape recurrence after bad70ef.

The positive part is a uniform alternating-cycle normal form: relative to a
cap-containing parent matching, any cap-avoiding escape has a unique
alternating component through the cap.  Flipping only that component gives a
live escape with one cycle, a literal common matching tail, and a smaller
lexicographic occurrence potential whenever the original difference had
other components.

The negative part is source naturality.  A nine-cell rational packet satisfies
the selected mixed zero rows and pure normalization, but the shortest C4
escape comparison is only a sub-sum of the pure coefficient, not a physical
row.  This freezes the first exact guard to promoting occurrence-level
potential decrease without an occurrence selector/restriction operation.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product


COLOURS = tuple(range(3))


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


def alternating_components(first, second):
    difference = set(first) ^ set(second)
    adjacency = {}
    for left, right in difference:
        adjacency.setdefault(left, []).append(right)
        adjacency.setdefault(right, []).append(left)
    require(all(len(neighbours) == 2 for neighbours in adjacency.values()),
            (first, second, adjacency))
    components = []
    unseen = set(adjacency)
    while unseen:
        start = min(unseen)
        stack = [start]
        component = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(adjacency[vertex])
        unseen -= component
        component_edges = frozenset(
            endpoints for endpoints in difference
            if endpoints[0] in component
        )
        require(len(component_edges) == len(component)
                and len(component) % 2 == 0,
                (first, second, component, component_edges))
        components.append((tuple(sorted(component)), component_edges))
    return tuple(sorted(components))


def flip_component(matching, component_edges):
    return tuple(sorted(set(matching) ^ set(component_edges)))


def audit_escape_normal_form(order):
    vertices = tuple(range(order))
    matchings = tuple(sorted(perfect_matchings(vertices)))
    profile = Counter()
    checked = 0
    reductions = 0
    for parent in matchings:
        for cap in parent:
            for escape in matchings:
                if cap in escape:
                    continue
                components = alternating_components(parent, escape)
                cap_components = tuple(
                    item for item in components
                    if set(cap) <= set(item[0])
                )
                require(len(cap_components) == 1,
                        (parent, cap, escape, components))
                cap_vertices, cap_edges = cap_components[0]
                reduced_escape = flip_component(parent, cap_edges)
                require(reduced_escape in matchings and cap not in reduced_escape,
                        (parent, cap, escape, reduced_escape))
                require(set(reduced_escape) <= set(parent) | set(escape),
                        (parent, escape, reduced_escape))
                reduced_components = alternating_components(
                    parent, reduced_escape
                )
                require(len(reduced_components) == 1
                        and reduced_components[0][0] == cap_vertices,
                        (parent, escape, reduced_escape, reduced_components))
                common_tail = set(parent) & set(reduced_escape)
                require(len(common_tail) == order // 2 - len(cap_vertices) // 2,
                        (parent, reduced_escape, cap_vertices, common_tail))
                old_potential = (len(cap_vertices),
                                 sum(len(item[0]) for item in components),
                                 len(components))
                new_potential = (len(cap_vertices), len(cap_vertices), 1)
                require(new_potential <= old_potential,
                        (old_potential, new_potential))
                if len(components) > 1:
                    require(new_potential < old_potential,
                            (old_potential, new_potential))
                    reductions += 1
                profile[(tuple(sorted(len(item[0]) for item in components)),
                         len(cap_vertices))] += 1
                checked += 1
    expected = {
        6: Counter({((6,), 6): 360, ((4,), 4): 180}),
        8: Counter({
            ((8,), 8): 20160,
            ((6,), 6): 10080,
            ((4, 4), 4): 5040,
            ((4,), 4): 2520,
        }),
    }[order]
    require(profile == expected, (order, profile, expected))
    return {
        "order": order,
        "matchings": len(matchings),
        "labelled_parent_cap_escape_triples": checked,
        "multi_cycle_strict_reductions": reductions,
        "profiles": tuple(sorted(profile.items())),
    }


def occurrence_cells(matching, word):
    if any(word[left] != word[right] for left, right in matching):
        return None
    return tuple((endpoints, word[endpoints[0]]) for endpoints in matching)


def coefficient_ledger(support, weights):
    matchings = tuple(sorted(perfect_matchings(range(6))))
    rows = {}
    for word in product(COLOURS, repeat=6):
        terms = []
        for matching in matchings:
            cells = occurrence_cells(matching, word)
            if cells is None or not set(cells) <= support:
                continue
            value = Fraction(1)
            for cell in cells:
                value *= weights[cell]
            terms.append((matching, cells, value))
        if terms:
            rows[word] = tuple(terms)
    return rows


def word_name(word):
    return "".join(map(str, word))


def matching_name(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def exact_escape_selector_guard():
    """A selected exact three-row packet whose shortest flip is not a row."""
    cap = edge(3, 4)
    parent_long = tuple(sorted((edge(0, 5), edge(1, 2), cap)))
    parent_short = tuple(sorted((edge(0, 1), edge(2, 5), cap)))
    escape = tuple(sorted((edge(0, 1), edge(2, 3), edge(4, 5))))

    weights = {
        (cap, 0): Fraction(1),
        (cap, 1): Fraction(1),
        (cap, 2): Fraction(1),
        (edge(0, 5), 1): Fraction(2),
        (edge(1, 2), 1): Fraction(1),
        (edge(0, 1), 1): Fraction(-2),
        (edge(2, 5), 1): Fraction(1),
        (edge(2, 3), 1): Fraction(-1, 2),
        (edge(4, 5), 1): Fraction(1),
    }
    support = frozenset(weights)
    require(len(support) == 9, support)
    rows = coefficient_ledger(support, weights)
    expected_words = {
        (1, 1, 1, colour, colour, 1) for colour in COLOURS
    }
    require(set(rows) == expected_words, rows)
    totals = {word: sum(term[2] for term in terms)
              for word, terms in rows.items()}
    require(totals == {
        (1, 1, 1, 0, 0, 1): 0,
        (1, 1, 1, 1, 1, 1): 1,
        (1, 1, 1, 2, 2, 1): 0,
    }, totals)
    mixed_terms = rows[(1, 1, 1, 0, 0, 1)]
    require(tuple((item[0], item[2]) for item in mixed_terms) == (
        (parent_short, Fraction(-2)),
        (parent_long, Fraction(2)),
    ), mixed_terms)
    pure_terms = rows[(1, 1, 1, 1, 1, 1)]
    require(tuple((item[0], item[2]) for item in pure_terms) == (
        (escape, Fraction(1)),
        (parent_short, Fraction(-2)),
        (parent_long, Fraction(2)),
    ), pure_terms)

    long_components = alternating_components(parent_long, escape)
    short_components = alternating_components(parent_short, escape)
    require(tuple(map(len, (long_components[0][0],
                            short_components[0][0]))) == (6, 4),
            (long_components, short_components))
    require(set(parent_short) & set(escape) == {edge(0, 1)},
            (parent_short, escape))
    require(not (set(parent_long) & set(escape)),
            (parent_long, escape))

    # The occurrence-shortest restriction selects the terms containing 01.
    # Its value is -2+1=-1, neither a source zero nor the normalized pure
    # value.  It is a proper sub-sum, not one of the three physical rows.
    selected_common_tail = edge(0, 1)
    selected_terms = tuple(term for term in pure_terms
                           if selected_common_tail in term[0])
    selected_total = sum(term[2] for term in selected_terms)
    require(tuple(item[0] for item in selected_terms) ==
            (escape, parent_short), selected_terms)
    require(selected_total == -1
            and selected_total not in set(totals.values()) - {-1},
            (selected_total, totals))

    # The valid source combination pure - mixed isolates the escape weight
    # 1, but does not transport the other 3^(N-2) output rows needed for a
    # contraction.  Record the distinction explicitly.
    require(totals[(1, 1, 1, 1, 1, 1)]
            - totals[(1, 1, 1, 0, 0, 1)] == 1, totals)
    return {
        "cells": len(support),
        "physical_cap": "34",
        "word_rows": tuple(sorted(
            (word_name(word), tuple(
                (matching_name(term[0]), str(term[2])) for term in terms
            ), str(totals[word]))
            for word, terms in rows.items()
        )),
        "escape_parent_cycle_sizes": {
            matching_name(parent_long): 6,
            matching_name(parent_short): 4,
        },
        "short_common_tail": "01",
        "short_restriction_value": str(selected_total),
        "physical_row_values": tuple(sorted(set(map(str, totals.values())))),
        "missing_map": "full-word occurrence selector/restriction",
        "first_unmet_pure_rows": ("000000", "222222"),
    }


def main():
    order6 = audit_escape_normal_form(6)
    order8 = audit_escape_normal_form(8)
    guard = exact_escape_selector_guard()
    print("uniform forced-pure-escape alternating potential: PASS")
    print("alternating normal form", order6)
    print("alternating normal form", order8)
    print("exact source-naturality guard", guard)
    print("terminal criterion: common-tail projector, singleton, or labelled core descent")


if __name__ == "__main__":
    main()

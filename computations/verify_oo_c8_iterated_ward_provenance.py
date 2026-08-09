#!/usr/bin/env python3
"""Iterated site-colour Ward provenance on the 47 Hamming-one OO profiles.

For each selected active output word, recolour every non-1 site to colour 1.
The corresponding site Ward operators commute and form a shortest word from
the mixed coefficient to the pure X_1 coefficient.  We expand the action by
physical perfect matching, so a term never silently changes its matching
provenance during the Ward iteration.
"""

from collections import Counter
from fractions import Fraction as F

import verify_oo_c8_color_raising_ward as ward
import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def canonical_matching(matching):
    return tuple(sorted(tuple(sorted(edge)) for edge in matching))


def selected_word(record):
    residual = tuple(v for v in base.VERTICES if v not in frontier.ARMS[0])
    colours = dict(zip(residual, record["word"], strict=True))
    colours[base.P] = 1
    colours[base.Q] = 0
    return tuple(colours[v] for v in base.VERTICES)


def selected_matching(record):
    return canonical_matching(((base.P, base.Q),) + tuple(record["matching"]))


def specialize_matching(blocks, support, matching, word):
    """Specialize one universal matching monomial to the sparse chart."""

    support_index = {cell: index for index, cell in enumerate(support)}
    mask = 0
    coefficient = F(1)
    for u, v in matching:
        cell = base.key(u, v, word[u], word[v])
        if cell in blocks:
            coefficient *= blocks[cell]
        elif cell in support_index:
            mask |= 1 << support_index[cell]
        else:
            return {}
    return {mask: coefficient}


def specialized_matching_terms(blocks, support, word):
    return tuple(
        (canonical_matching(matching), polynomial)
        for matching in base.perfect_matchings(base.VERTICES)
        if (polynomial := specialize_matching(blocks, support, matching, word))
    )


def aggregate(terms):
    answer = {}
    for _matching, polynomial in terms:
        for mask, coefficient in polynomial.items():
            answer[mask] = answer.get(mask, F(0)) + coefficient
    return {mask: coefficient for mask, coefficient in answer.items() if coefficient}


def recolour(word, sites):
    answer = list(word)
    for site in sites:
        answer[site] = 1
    return tuple(answer)


def absent_cells(matching, word, blocks, support):
    occupied = set(blocks) | set(support)
    return tuple(
        base.key(u, v, word[u], word[v])
        for u, v in matching
        if base.key(u, v, word[u], word[v]) not in occupied
    )


def symmetric_difference_cycles(first, second):
    difference = set(first) ^ set(second)
    if not difference:
        return ()
    adjacency = {v: [] for v in base.VERTICES}
    for u, v in difference:
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen = set()
    lengths = []
    for start in base.VERTICES:
        if start in seen or not adjacency[start]:
            continue
        stack = [start]
        vertices = set()
        while stack:
            vertex = stack.pop()
            if vertex in vertices:
                continue
            vertices.add(vertex)
            stack.extend(adjacency[vertex])
        require(all(len(adjacency[v]) == 2 for v in vertices), "matching difference is not cycles")
        seen.update(vertices)
        lengths.append(len(vertices))
    return tuple(sorted(lengths))


def main():
    blocks = base.build_packet()
    profiles = ward.main_profiles(blocks)
    require(
        all(
            sum(a != b for a, b in zip(records[0]["common"], records[1]["common"], strict=True)) == 1
            for _support, records, _face, _hessians in profiles
        ),
        "the 47-profile sector is no longer common-word Hamming one",
    )

    length_census = Counter()
    active_death_census = Counter()
    pure_birth_census = Counter()
    overlap_census = Counter()
    cycle_census = Counter()
    double_changed_edge_census = Counter()
    laurent_certificate_census = Counter()
    first_provenance_guard = None
    first_laurent_failure = None

    for support, records, face, active_hessians in profiles:
        word = selected_word(records[0])
        active_matching = selected_matching(records[0])
        changed = tuple(site for site, colour in enumerate(word) if colour != 1)
        require(changed, "selected word became pure")
        length_census[len(changed)] += 1

        # Distinct-site Ward fields commute.  The increasing-site order is a
        # canonical shortest word; every proper prefix remains mixed.
        words = tuple(recolour(word, changed[:step]) for step in range(len(changed) + 1))
        require(all(len(set(current)) > 1 for current in words[:-1]), "Ward prefix became pure early")
        require(words[-1] == (1,) * 8, "Ward word did not end at X_1")

        tensor = frontier.tensor_polynomials(blocks, support)
        for step, current in enumerate(words):
            terms = specialized_matching_terms(blocks, support, current)
            require(aggregate(terms) == tensor.get(current, {}), "matching Ward expansion changed")
            target = F(1) if step == len(changed) else F(0)
            require(target == (F(1) if len(set(current)) == 1 else F(0)), "full-nine target reduction changed")

        active_trace = tuple(
            specialize_matching(blocks, support, active_matching, current)
            for current in words
        )
        require(
            active_trace[0].get(records[0]["mask"], 0)
            == active_hessians[0].get(records[0]["mask"], 0),
            "localized active matching lost its leader coefficient",
        )
        death = next((step for step, value in enumerate(active_trace) if not value), None)
        require(death is not None and death > 0, "active matching survived to a pure matching")
        active_death_census[(len(changed), death)] += 1

        pure_terms = specialized_matching_terms(blocks, support, (1,) * 8)
        require(len(pure_terms) == 1, "pure X_1 coefficient is not a unique matching term")
        pure_matching, pure_polynomial = pure_terms[0]
        require(len(pure_polynomial) == 1, "pure X_1 matching is not a monomial")
        pure_mask, pure_coefficient = next(iter(pure_polynomial.items()))
        require(pure_coefficient == 1, "pure X_1 normalization changed")
        pure_trace = tuple(
            specialize_matching(blocks, support, pure_matching, current)
            for current in words
        )
        birth = next(step for step, value in enumerate(pure_trace) if value)
        require(birth > 0, "pure matching was already present in the selected mixed word")
        pure_birth_census[(len(changed), birth)] += 1

        active_mask = records[0]["mask"]
        common_degree = (active_mask & pure_mask).bit_count()
        overlap_census[(active_mask.bit_count(), common_degree, pure_mask.bit_count())] += 1
        cycles = symmetric_difference_cycles(active_matching, pure_matching)
        cycle_census[cycles] += 1
        double_changed = sum(u in changed and v in changed for u, v in pure_matching)
        double_changed_edge_census[double_changed] += 1

        # The sparse chart has a Laurent monomial certificate exactly when
        # the active leader divides the pure anchor monomial.  Record this
        # separately from Ward provenance: the two terms can use different
        # physical matchings even when their support-variable masks divide.
        divides = (active_mask & pure_mask) == active_mask
        coefficient = active_hessians[0].get(active_mask, 0)
        laurent_certificate_census[(divides, coefficient)] += 1
        if divides:
            quotient_mask = pure_mask ^ active_mask
            require(
                coefficient in (F(1), F(-1)),
                "active Laurent certificate coefficient ceased to be a unit",
            )
        else:
            quotient_mask = None

        if not divides and first_laurent_failure is None:
            first_laurent_failure = {
                "support": support,
                "word": word,
                "ward_sites": changed,
                "active_matching": active_matching,
                "active_trace": active_trace,
                "pure_matching": pure_matching,
                "pure_trace": pure_trace,
                "pure_initial_absent_cells": absent_cells(
                    pure_matching, word, blocks, support
                ),
                "cycles": cycles,
                "active_mask": active_mask,
                "pure_mask": pure_mask,
                "active_only_mask": active_mask & ~pure_mask,
                "pure_only_mask": pure_mask & ~active_mask,
                "double_changed_edges": tuple(
                    edge for edge in pure_matching
                    if edge[0] in changed and edge[1] in changed
                ),
            }

        if first_provenance_guard is None:
            first_provenance_guard = {
                "support": support,
                "word": word,
                "ward_sites": changed,
                "active_matching": active_matching,
                "active_trace": active_trace,
                "pure_matching": pure_matching,
                "pure_trace": pure_trace,
                "pure_initial_absent_cells": absent_cells(
                    pure_matching, word, blocks, support
                ),
                "cycles": cycles,
                "active_mask": active_mask,
                "pure_mask": pure_mask,
                "quotient_mask": quotient_mask,
                "double_changed_edges": tuple(
                    edge for edge in pure_matching
                    if edge[0] in changed and edge[1] in changed
                ),
            }

    require(length_census == Counter({3: 28, 5: 12, 6: 3, 4: 2, 7: 2}), "Ward length census changed")
    require(
        laurent_certificate_census
        == Counter({(True, F(1)): 35, (False, F(1)): 12}),
        f"sparse Laurent certificate census changed: {laurent_certificate_census}",
    )
    require(
        active_death_census
        == Counter({(3, 1): 28, (5, 1): 12, (6, 1): 3, (4, 2): 2, (7, 1): 2}),
        f"active matching death census changed: {active_death_census}",
    )

    guard = first_provenance_guard
    require(guard["word"] == (1, 1, 0, 2, 2, 1, 1, 1), "canonical Ward word changed")
    require(guard["ward_sites"] == (2, 3, 4), "canonical shortest Ward sites changed")
    require(guard["active_matching"] == ((0, 2), (1, 7), (3, 4), (5, 6)), "active matching changed")
    require(guard["pure_matching"] == ((0, 3), (1, 7), (2, 4), (5, 6)), "pure matching changed")
    require(guard["pure_initial_absent_cells"] == ((0, 3, 1, 2), (2, 4, 0, 2)), "absent Ward provenance changed")
    require(guard["cycles"] == (4,), "canonical matching exchange ceased to be C4")
    require(guard["active_mask"] == 12 and guard["pure_mask"] == 14, "canonical masks changed")
    require(guard["quotient_mask"] == 2, "canonical Laurent quotient changed")
    require(guard["double_changed_edges"] == ((2, 4),), "canonical double-Ward edge changed")

    print("alternating-C8 iterated Ward provenance: PASS")
    print(f"Hamming-one profiles={len(profiles)}")
    print(f"shortest Ward length census={dict(sorted(length_census.items()))}")
    print(f"active matching death step={dict(sorted(active_death_census.items()))}")
    print(f"pure matching birth step={dict(sorted(pure_birth_census.items()))}")
    print(f"active/pure mask overlap={dict(sorted(overlap_census.items()))}")
    print(f"active-to-pure matching cycle types={dict(sorted(cycle_census.items()))}")
    print(f"pure matching double-changed edges={dict(sorted(double_changed_edge_census.items()))}")
    print(f"sparse Laurent certificate census={dict(laurent_certificate_census)}")
    print(f"first multi-site provenance guard={guard}")
    print(f"first nondivisible active/pure provenance={first_laurent_failure}")


if __name__ == "__main__":
    main()

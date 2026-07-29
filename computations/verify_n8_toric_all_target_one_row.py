#!/usr/bin/env python3
"""Independent completeness audit for target-specific one-row pure zeros.

The production generator starts from a forced pure matching and a second pure
matching.  This verifier inverts the construction: it starts from every pair
of possible mixed matchings, reconstructs a compatible second pure matching
from their exponent difference, and enumerates the colors only on their
common edges.  Equality of the two sets therefore checks both directions of
the one-row classification rather than merely replaying its loop order.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_toric_binomial_lazy_cegar as toric


TARGETS = (
    ((0, 1), (2, 3), (4, 5), (6, 7)),
    ((0, 2), (1, 3), (4, 6), (5, 7)),
    ((0, 4), (1, 5), (2, 6), (3, 7)),
)


def decorate(coloring, matching):
    return tuple(
        (u, v, coloring[u], coloring[v]) for u, v in matching
    )


def canonical_difference(left, right):
    positive = frozenset(set(left) - set(right))
    negative = frozenset(set(right) - set(left))
    forward = (tuple(sorted(positive)), tuple(sorted(negative)))
    backward = (forward[1], forward[0])
    return min(forward, backward)


def independently_enumerated_schemas(matchings):
    """Enumerate from mixed pairs, inverse to the production construction."""

    matching_set = frozenset(matchings)
    schemas = set()
    for color, raw_target in enumerate(TARGETS):
        target = frozenset(raw_target)
        for unordered_first, unordered_second in combinations(matchings, 2):
            common = unordered_first & unordered_second
            if not common:
                # No common mixed edge leaves no vertex on which the coloring
                # can differ from the pure color.
                continue
            common_vertices = tuple(sorted({
                vertex for edge in common for vertex in edge
            }))
            for first, second in (
                (unordered_first, unordered_second),
                (unordered_second, unordered_first),
            ):
                first_only = first - second
                second_only = second - first
                if not first_only <= target:
                    continue
                other = frozenset((target - first_only) | second_only)
                if other == target or other not in matching_set:
                    continue
                assert target - other == first_only
                assert other - target == second_only
                for assigned in product(
                    range(signed.Q), repeat=len(common_vertices)
                ):
                    coloring = [color] * signed.N
                    for vertex, value in zip(common_vertices, assigned):
                        coloring[vertex] = value
                    if all(value == color for value in coloring):
                        continue
                    coloring = tuple(coloring)
                    guard = frozenset(
                        decorate(coloring, first)
                        + decorate(coloring, second)
                    )
                    schemas.add((
                        guard,
                        color,
                        frozenset((target, other)),
                    ))
    return schemas


def independently_completed_schemas(base_schemas, matchings):
    """Complete pure fibres by quotient pairs derived from each mixed row."""

    targets = tuple(map(frozenset, TARGETS))
    pair_cache = {}
    schemas = set()
    for guard, color, base_pair in base_schemas:
        vertex_colors = [None] * signed.N
        for u, v, a, b in guard:
            assert vertex_colors[u] in (None, a)
            assert vertex_colors[v] in (None, b)
            vertex_colors[u] = a
            vertex_colors[v] = b
        coloring = tuple(vertex_colors)
        mixed_terms = [
            decorate(coloring, matching)
            for matching in matchings
            if set(decorate(coloring, matching)) <= guard
        ]
        assert len(mixed_terms) == 2
        difference = canonical_difference(*mixed_terms)
        cache_key = color, difference
        if cache_key not in pair_cache:
            pure_coloring = (color,) * signed.N
            pairs = tuple(
                frozenset((left, right))
                for left, right in combinations(matchings, 2)
                if canonical_difference(
                    decorate(pure_coloring, left),
                    decorate(pure_coloring, right),
                ) == difference
            )
            assert len({matching for pair in pairs for matching in pair}) == (
                2 * len(pairs)
            )
            pair_cache[cache_key] = pairs
        pairs = pair_cache[cache_key]
        assert base_pair in pairs
        assert targets[color] in base_pair
        assert len(pairs) in (1, 3)
        optional = tuple(pair for pair in pairs if pair != base_pair)
        for included in product((False, True), repeat=len(optional)):
            present = set(base_pair)
            for use_pair, pair in zip(included, optional):
                if use_pair:
                    present.update(pair)
            schemas.add((guard, color, frozenset(present)))
    assert len(pair_cache) == 132
    return schemas


def main():
    matchings = tuple(
        frozenset(matching)
        for matching in signed.core.perfect_matchings(tuple(range(signed.N)))
    )
    assert len(matchings) == 105

    # The elementary matching counts behind 9,408 are checked directly:
    # relative to a fixed target, 32 matchings share one edge and 12 share
    # two.  They contribute 32*(3^2-1)=256 and
    # 12*3*(3^4-1)=2,880 schemas per color.
    for target in map(frozenset, TARGETS):
        shared = Counter(
            len(target & other) for other in matchings if other != target
        )
        assert shared == {0: 60, 1: 32, 2: 12}
    assert 3 * (32 * (3 ** 2 - 1) + 12 * 3 * (3 ** 4 - 1)) == 9408

    production = set(toric.target_one_row_pure_zero_schemas(TARGETS))
    independent = independently_enumerated_schemas(matchings)
    assert production == independent
    assert len(production) == 9408
    assert Counter(len(schema[0]) for schema in production) == {
        6: 8640,
        7: 768,
    }

    complete_production = set(
        toric.target_complete_one_row_pure_zero_schemas(TARGETS)
    )
    complete_independent = independently_completed_schemas(
        independent, matchings
    )
    assert complete_production == complete_independent
    assert len(complete_production) == 35328
    assert Counter(len(schema[2]) for schema in complete_production) == {
        2: 9408,
        4: 17280,
        6: 8640,
    }
    assert Counter(len(schema[0]) for schema in complete_production) == {
        6: 34560,
        7: 768,
    }
    exact_fibre_triggers = {
        (color, present)
        for _guard, color, present in complete_production
    }
    assert len(exact_fibre_triggers) == 204
    assert Counter(len(present) for _color, present in exact_fibre_triggers) == {
        2: 132,
        4: 36,
        6: 36,
    }

    # Independently reduce every distinct exact pure fibre in the signed
    # quotient of one representative mixed row.  All 204 must be the zero
    # Laurent polynomial, not merely admit a visual pairing.
    cells = tuple(
        (u, v, a, b)
        for u in range(signed.N)
        for v in range(u + 1, signed.N)
        for a, b in product(range(signed.Q), repeat=2)
    )
    cell_index = {cell: index for index, cell in enumerate(cells)}
    matching_index = {
        matching: number for number, matching in enumerate(matchings)
    }
    representative_guard = {}
    for guard, color, present in complete_production:
        representative_guard.setdefault((color, present), guard)
    assert set(representative_guard) == exact_fibre_triggers
    for (color, present), guard in representative_guard.items():
        vertex_colors = [None] * signed.N
        for u, v, a, b in guard:
            vertex_colors[u] = a
            vertex_colors[v] = b
        coloring = tuple(vertex_colors)
        mixed_terms = [
            decorate(coloring, matching)
            for matching in matchings
            if set(decorate(coloring, matching)) <= guard
        ]
        assert len(mixed_terms) == 2
        row = signed.core.exponent_row(
            mixed_terms[0], mixed_terms[1], cell_index, len(cells)
        )
        consistent, lattice = signed.core.signed_quotient_lattice(
            [row], len(cells)
        )
        assert consistent
        pure_coloring = (color,) * signed.N
        fibres = {
            pure_coloring: tuple(
                (
                    matching_index[matching],
                    decorate(pure_coloring, matching),
                )
                for matching in sorted(
                    present, key=lambda item: tuple(sorted(item))
                )
            )
        }
        remainder, _classes = signed.core.reduced_constant_product(
            signed.N,
            fibres,
            lattice,
            cells,
            cell_index,
            colors=(color,),
        )
        assert not remainder

    # Audit every schema at the exponent-row level.  Its guard supports
    # exactly two terms in one nonconstant coloring, and their difference is
    # the pure-pair difference up to orientation.
    target_sets = tuple(map(frozenset, TARGETS))
    for guard, color, pure_pair in production:
        assert target_sets[color] in pure_pair
        vertex_colors = [None] * signed.N
        for u, v, a, b in guard:
            assert vertex_colors[u] in (None, a)
            assert vertex_colors[v] in (None, b)
            vertex_colors[u] = a
            vertex_colors[v] = b
        assert all(value is not None for value in vertex_colors)
        coloring = tuple(vertex_colors)
        assert len(set(coloring)) > 1
        mixed_terms = [
            decorate(coloring, matching)
            for matching in matchings
            if set(decorate(coloring, matching)) <= guard
        ]
        assert len(mixed_terms) == 2
        pure_terms = [
            decorate((color,) * signed.N, matching)
            for matching in pure_pair
        ]
        assert canonical_difference(*mixed_terms) == canonical_difference(
            *pure_terms
        )

    forced = frozenset(
        (u, v, color, color)
        for color, target in enumerate(TARGETS)
        for u, v in target
    )
    reduced = {
        (guard - forced, color, pure_pair)
        for guard, color, pure_pair in production
    }
    assert len(reduced) == 9408
    assert Counter(len(schema[0]) for schema in reduced) == {
        2: 24,
        3: 960,
        4: 8424,
    }

    old_global = set(toric.global_one_row_pure_zero_schemas())
    assert len(production & old_global) == 144
    assert len(production - old_global) == 9264

    # Fixed regression from the dense full-formula CEGAR search.  This chart
    # satisfied every zero-or-two structural constraint and had two pure terms
    # in each color.  It evaded the old global orbit completely, yet contains
    # five members of the complete target-specific family.
    checkpoint_path = Path(__file__).with_name(
        "n8_orbit40_pre_target9408_round6_structural.json"
    )
    checkpoint = json.loads(checkpoint_path.read_text())
    assert tuple(
        tuple(tuple(edge) for edge in matching)
        for matching in checkpoint["targets"]
    ) == TARGETS
    selected = frozenset(
        tuple(record["cell"]) for record in checkpoint["selected_cells"]
    )
    assert len(selected) == 83
    fibres = signed.core.exact_fibres(signed.N, selected, matchings)
    mixed = {
        coloring: terms
        for coloring, terms in fibres.items()
        if len(set(coloring)) > 1
    }
    assert len(mixed) == checkpoint["mixed_fibres"] == 3687
    assert all(len(terms) == 2 for terms in mixed.values())
    pure_matching_sets = {
        color: frozenset(
            matchings[matching_number]
            for matching_number, _decorated
            in fibres[(color,) * signed.N]
        )
        for color in range(signed.Q)
    }
    assert tuple(map(len, pure_matching_sets.values())) == (2, 2, 2)

    def hits(schemas):
        return [
            schema
            for schema in schemas
            if schema[0] <= selected
            and pure_matching_sets[schema[1]] == schema[2]
        ]

    old_hits = hits(old_global)
    new_hits = hits(production)
    assert not old_hits
    assert len(new_hits) == checkpoint["pre_target_specific_schema_hits"] == 5
    for guard, color, pure_pair in new_hits:
        vertex_colors = [None] * signed.N
        for u, v, a, b in guard:
            assert vertex_colors[u] in (None, a)
            assert vertex_colors[v] in (None, b)
            vertex_colors[u] = a
            vertex_colors[v] = b
        coloring = tuple(vertex_colors)
        actual_mixed = [
            decorated for _number, decorated in fibres[coloring]
        ]
        actual_pure = [
            decorated
            for number, decorated in fibres[(color,) * signed.N]
            if matchings[number] in pure_pair
        ]
        assert len(actual_mixed) == len(actual_pure) == 2
        assert canonical_difference(*actual_mixed) == canonical_difference(
            *actual_pure
        )

    print(
        "PASS: independently complete target two-term family has 9,408 "
        "schemas (8,640 six-cell + 768 seven-cell), 9,264 new beyond the "
        "old orbit; forced guards reduce distinctly to sizes 2--4; fixed "
        "83-cell chart has old/new hit counts 0/5; all pure sizes 2/4/6 "
        "give 35,328 complete one-row zeros with 204 exact-fibre triggers "
        "and 204 exact zero quotient reductions"
    )


if __name__ == "__main__":
    main()

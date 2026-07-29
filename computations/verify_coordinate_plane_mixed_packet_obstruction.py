#!/usr/bin/env python3
"""Exact audit for the coordinate-plane mixed-packet obstruction.

The companion note proves that double quotienting the nine responses makes
the three same-class four-site cofactors entirely pure and makes every
nonzero mixed-class cofactor carry a zero response matrix.  This checker
audits the finite incidence table, replays the existing exact pure-K4
extension/apex certificates, classifies the possible disconnected cofactor
graphs, and verifies the sharp two-triangle common-power model.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

import sympy as sp

from verify_common_annihilator_planes import (
    audit_disconnected_apex_propagation,
    audit_pure_extension_annihilators,
)


U = tuple(range(6))
COLOURS = tuple(range(3))
PAIRS = {colour: (2 * colour, 2 * colour + 1) for colour in COLOURS}
LABEL = {u: colour for colour, pair in PAIRS.items() for u in pair}
EDGES = tuple(combinations(U, 2))
MIXED_EDGES = tuple(edge for edge in EDGES if LABEL[edge[0]] != LABEL[edge[1]])


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(remainder):
            yield ((first, second),) + tail


def audit_double_quotient_table():
    """Check which missing-pair and target sectors survive two quotients."""

    checked = 0
    for quotient_pair in EDGES:
        for missing_pair in EDGES:
            # F_Q occupies U\Q.  Both quotient sites avoid F_Q exactly when
            # the quotient pair is contained in Q; equal cardinalities make
            # this equality.
            survives = set(quotient_pair) <= set(missing_pair)
            assert survives == (quotient_pair == missing_pair)
            checked += 1

        surviving_targets = tuple(
            colour
            for colour in COLOURS
            if all(LABEL[u] == colour for u in quotient_pair)
        )
        if LABEL[quotient_pair[0]] == LABEL[quotient_pair[1]]:
            assert quotient_pair == PAIRS[LABEL[quotient_pair[0]]]
            assert surviving_targets == (LABEL[quotient_pair[0]],)
        else:
            assert surviving_targets == ()

    # The three response-side matrix factors are genuinely independent.
    diagonal_units = tuple(
        sp.eye(3).col(i) * sp.eye(3).col(i).T for i in COLOURS
    )
    flattened = sp.Matrix.hstack(
        *(sp.Matrix(9, 1, tuple(matrix)) for matrix in diagonal_units)
    )
    assert flattened.rank() == 3
    return checked


def audit_no_isolated_incidence():
    """Replay the set incidences in the analytic no-isolated proof."""

    checked = 0
    for isolated in U:
        isolated_class = LABEL[isolated]
        mate = next(u for u in PAIRS[isolated_class] if u != isolated)
        pure_complement = tuple(
            u for u in U if u not in PAIRS[isolated_class]
        )

        # Deleting the isolated site and v leaves mate plus three sites of
        # the pure complement.  Every matching has one mate-star edge and
        # one edge internal to the complement, exactly a component of q*ell.
        for deleted in pure_complement:
            four_set = tuple(
                u for u in U if u not in (isolated, deleted)
            )
            assert mate in four_set
            for matching in matchings(four_set):
                mate_edge = next(edge for edge in matching if mate in edge)
                partner = next(u for u in mate_edge if u != mate)
                assert partner in pure_complement and partner != deleted
                other_edge = next(edge for edge in matching if edge != mate_edge)
                assert set(other_edge) <= set(pure_complement)
                checked += 1

        # Each of the two other pure K4s consists of the isolated class and
        # one other class.  Its two cross matchings both use a mate-star edge
        # at the other class, so quotienting that class by the forced e_c line
        # leaves only the two internal edges.  The two target colours differ.
        forced_internal_colours = []
        for target_colour in COLOURS:
            if target_colour == isolated_class:
                continue
            other_class = 3 - isolated_class - target_colour
            four_set = tuple(sorted(PAIRS[isolated_class] + PAIRS[other_class]))
            matching_list = tuple(matchings(four_set))
            internal = tuple(
                matching
                for matching in matching_list
                if all(LABEL[u] == LABEL[v] for u, v in matching)
            )
            cross = tuple(matching for matching in matching_list if matching not in internal)
            assert len(internal) == 1 and len(cross) == 2
            assert all(
                any(
                    mate in edge
                    and LABEL[next(u for u in edge if u != mate)] == other_class
                    for edge in matching
                )
                for matching in cross
            )
            forced_internal_colours.append(target_colour)
        assert len(set(forced_internal_colours)) == 2

    return checked


def components(edge_set):
    adjacency = {u: set() for u in U}
    for u, v in edge_set:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(U)
    answer = []
    while unseen:
        root = min(unseen)
        reached = {root}
        frontier = [root]
        while frontier:
            u = frontier.pop()
            for v in adjacency[u] - reached:
                reached.add(v)
                frontier.append(v)
        unseen -= reached
        answer.append(frozenset(reached))
    return tuple(sorted(answer, key=lambda part: (len(part), tuple(part))))


def audit_graph_component_frontier():
    """Enumerate all 2^12 possible mixed-cofactor graphs."""

    disconnected_no_isolated = 0
    patterns = Counter()
    three_three_signatures = Counter()
    two_plus_four_full_classes = 0
    two_two_two_types = 0

    for mask in range(1 << len(MIXED_EDGES)):
        edge_set = {
            edge for index, edge in enumerate(MIXED_EDGES) if (mask >> index) & 1
        }
        degree = Counter(u for edge in edge_set for u in edge)
        if any(degree[u] == 0 for u in U):
            continue
        parts = components(edge_set)
        if len(parts) == 1:
            continue
        disconnected_no_isolated += 1
        sizes = tuple(sorted(map(len, parts)))
        patterns[sizes] += 1
        assert sizes in ((2, 4), (3, 3), (2, 2, 2))

        if sizes == (2, 4):
            small, large = parts
            assert LABEL[min(small)] != LABEL[max(small)]
            full_classes = tuple(
                colour for colour, pair in PAIRS.items() if set(pair) <= set(large)
            )
            assert len(full_classes) == 1
            two_plus_four_full_classes += 1
        elif sizes == (3, 3):
            signature = tuple(sorted(Counter(LABEL[u] for u in parts[0]).values()))
            assert signature in ((1, 1, 1), (1, 2))
            three_three_signatures[signature] += 1
        else:
            # A connected two-vertex component is a mixed edge.  Using all
            # two sites of every class forces one component of each class-pair.
            class_pairs = Counter(
                tuple(sorted(LABEL[u] for u in part)) for part in parts
            )
            assert class_pairs == Counter({(0, 1): 1, (0, 2): 1, (1, 2): 1})
            two_two_two_types += 1

    assert disconnected_no_isolated
    assert set(patterns) == {(2, 4), (3, 3), (2, 2, 2)}
    assert set(three_three_signatures) == {(1, 1, 1), (1, 2)}
    assert two_plus_four_full_classes
    assert two_two_two_types
    return disconnected_no_isolated, dict(sorted(patterns.items()))


def audit_two_plus_four_response_matrix():
    """A split class matrix cannot be a different diagonal unit."""

    f = tuple(sp.eye(3).col(i) for i in COLOURS)
    x = sp.Matrix(sp.symbols("x0:3"))
    y = sp.Matrix(sp.symbols("y0:3"))
    checked = 0
    for full_colour in COLOURS:
        supported = f[full_colour] * x.T + y * f[full_colour].T
        for split_colour in COLOURS:
            if split_colour == full_colour:
                continue
            assert supported[split_colour, split_colour] == 0
            assert (f[split_colour] * f[split_colour].T)[
                split_colour, split_colour
            ] == 1
            checked += 1
    assert checked == 6


def tensor_hafnian(vertices, blocks):
    vertices = tuple(sorted(vertices))
    output = Counter()
    for matching in matchings(vertices):
        partial = {(): 1}
        for u, v in matching:
            edge = (u, v) if u < v else (v, u)
            cells = blocks.get(edge, {})
            next_partial = Counter()
            for word, coefficient in partial.items():
                assigned = dict(word)
                for (cu, cv), value in cells.items():
                    new = dict(assigned)
                    new[u], new[v] = cu, cv
                    next_partial[tuple(sorted(new.items()))] += coefficient * value
            partial = dict(next_partial)
        for word, coefficient in partial.items():
            colors = tuple(dict(word)[u] for u in vertices)
            output[colors] += coefficient
    return {word: value for word, value in output.items() if value}


def audit_two_triangle_sharp_model():
    """Three pure slices plus q^[3]=0 do not suffice without responses."""

    blocks = {}
    for left_class, right_class in combinations(COLOURS, 2):
        third = 3 - left_class - right_class
        for index in range(2):
            u = PAIRS[left_class][index]
            v = PAIRS[right_class][index]
            edge = (u, v) if u < v else (v, u)
            blocks[edge] = {(third, third): 1}

    # Two disjoint odd triangles have no six-site perfect matching.
    assert tensor_hafnian(U, blocks) == {}

    mixed_graph = set()
    for hole in EDGES:
        complement = tuple(u for u in U if u not in hole)
        cofactor = tensor_hafnian(complement, blocks)
        if hole in PAIRS.values():
            colour = LABEL[hole[0]]
            target = tuple(colour for _ in complement)
            assert cofactor == {target: 1}
        elif cofactor:
            mixed_graph.add(hole)

    assert len(mixed_graph) == 6
    assert tuple(map(len, components(mixed_graph))) == (6,)
    assert all(
        sum(u in edge for edge in mixed_graph) == 2 for u in U
    )
    return len(mixed_graph)


def main():
    quotient_checks = audit_double_quotient_table()
    isolated_incidence_checks = audit_no_isolated_incidence()
    extension_nullities = audit_pure_extension_annihilators()
    disconnected_certificate = audit_disconnected_apex_propagation()
    graph_frontier = audit_graph_component_frontier()
    audit_two_plus_four_response_matrix()
    sharp_edges = audit_two_triangle_sharp_model()
    print("coordinate-plane mixed-packet obstruction: PASS")
    print("double-quotient pair checks:", quotient_checks)
    print("no-isolated matching incidences:", isolated_incidence_checks)
    print("pure-extension nullities:", extension_nullities)
    print("disconnected apex certificate:", disconnected_certificate)
    print("disconnected graph frontier:", graph_frontier)
    print("sharp two-triangle mixed-cofactor edges:", sharp_edges)
    print("q^[3] used by obstruction: no")


if __name__ == "__main__":
    main()

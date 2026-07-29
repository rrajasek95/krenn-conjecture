#!/usr/bin/env python3
"""Exact all-fibre countermodule to odd-cut monotonicity of stub rewrites."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


N = 6
COLORS = tuple(range(3))
VERTICES = tuple(range(N))

P0 = ((0, 4), (1, 2), (3, 5))
P1 = ((0, 5), (1, 4), (2, 3))
P2 = ((0, 3), (1, 5), (2, 4))
SELECTED = (P0, P1, P2)
R = ((0, 4), (1, 5), (2, 3))
PRISM = frozenset(edge for matching in SELECTED for edge in matching)
SHORE = frozenset((0, 3, 5))


def perfect_matchings(vertices=VERTICES, support=None):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        edge = (u, v) if u < v else (v, u)
        if support is not None and edge not in support:
            continue
        remaining = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remaining, support):
            yield tuple(sorted((edge,) + tail))


def edge_weight(edge):
    return Fraction(-3 if edge == (1, 2) else 1)


def gauge(vertex, color):
    return Fraction(-1, 3) if (vertex, color) == (0, 0) else Fraction(1)


def entry(occurrence):
    u, v, a, b = occurrence
    return edge_weight((u, v)) * gauge(u, a) * gauge(v, b)


def decorate(matching, coloring):
    return frozenset((u, v, coloring[u], coloring[v]) for u, v in matching)


def term_value(matching, coloring):
    value = Fraction(1)
    for occurrence in decorate(matching, coloring):
        value *= entry(occurrence)
    return value


def state_weight(state):
    value = Fraction(1)
    for occurrence in state:
        value *= entry(occurrence)
    return value


def endpoint_stubs(occurrence):
    u, v, a, b = occurrence
    return ((u, a), (v, b))


def assert_stub_state(state):
    stubs = sorted(stub for occurrence in state for stub in endpoint_stubs(occurrence))
    assert stubs == [(vertex, color) for vertex in VERTICES for color in COLORS]


def crossing_count(state, shore=SHORE):
    return sum((u in shore) != (v in shore) for u, v, _a, _b in state)


def components(state):
    unseen = set(VERTICES)
    answer = []
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        component = {seed}
        frontier = [seed]
        while frontier:
            vertex = frontier.pop()
            for u, v, _a, _b in state:
                if u == vertex and v in unseen:
                    unseen.remove(v)
                    component.add(v)
                    frontier.append(v)
                elif v == vertex and u in unseen:
                    unseen.remove(u)
                    component.add(u)
                    frontier.append(u)
        answer.append(frozenset(component))
    return tuple(answer)


def bridges(state):
    state = tuple(state)
    answer = []
    for index, occurrence in enumerate(state):
        deleted = state[:index] + state[index + 1 :]
        if len(components(deleted)) > 1:
            answer.append(occurrence)
    return tuple(answer)


def main():
    prism_matchings = tuple(perfect_matchings(support=PRISM))
    assert set(prism_matchings) == {P0, P1, P2, R}
    assert tuple(sorted(edge_weight_product(matching) for matching in prism_matchings)) == (
        Fraction(-3),
        Fraction(1),
        Fraction(1),
        Fraction(1),
    )

    # Every one of the 3^6 coloring fibres is the same four-term scalar
    # relation times its common endpoint gauge.  Thus the complete
    # homogeneous coefficient system vanishes, not merely one chosen fibre.
    for coloring in product(COLORS, repeat=N):
        values = tuple(term_value(matching, coloring) for matching in prism_matchings)
        common_gauge = product_fraction(gauge(vertex, coloring[vertex]) for vertex in VERTICES)
        assert sorted(values) == sorted(
            (-3 * common_gauge, common_gauge, common_gauge, common_gauge)
        )
        assert sum(values, Fraction(0)) == 0

    # The three selected constant monomials themselves are normalized to one.
    for color, matching in enumerate(SELECTED):
        assert term_value(matching, (color,) * N) == 1

    selected_state = frozenset(
        occurrence
        for color, matching in enumerate(SELECTED)
        for occurrence in decorate(matching, (color,) * N)
    )
    assert len(selected_state) == 9
    assert_stub_state(selected_state)
    assert not bridges(selected_state)
    assert crossing_count(selected_state) == 3
    assert state_weight(selected_state) == 1

    # R uses one selected occurrence at every site and has mixed coloring.
    r_occurrences = frozenset(
        occurrence
        for occurrence in selected_state
        if occurrence[:2] in R
    )
    assert len(r_occurrences) == 3
    coloring = [-1] * N
    for occurrence in r_occurrences:
        for vertex_color in endpoint_stubs(occurrence):
            vertex, color = vertex_color
            coloring[vertex] = color
    coloring = tuple(coloring)
    assert coloring == (0, 2, 1, 1, 0, 2)
    assert len(set(coloring)) == 3
    assert decorate(R, coloring) == r_occurrences

    q_state = selected_state - r_occurrences
    assert len(q_state) == 6
    assert crossing_count(q_state) == 0
    assert state_weight(q_state) == -3

    alternatives = []
    for matching in SELECTED:
        mate = decorate(matching, coloring)
        replacement = frozenset(q_state | mate)
        assert len(replacement) == 9
        assert_stub_state(replacement)
        assert len(components(replacement)) == 1
        assert crossing_count(replacement) == 1
        bridge = bridges(replacement)
        assert len(bridge) == 1
        assert bridge[0] in mate

        # Audit the general cut identity and odd parity on every odd shore,
        # not only on the bridge witness SHORE.
        for shore_size in (1, 3, 5):
            for shore_tuple in combinations(VERTICES, shore_size):
                shore = frozenset(shore_tuple)
                selected_cut = crossing_count(selected_state, shore)
                r_cut = crossing_count(r_occurrences, shore)
                mate_cut = crossing_count(mate, shore)
                replacement_cut = crossing_count(replacement, shore)
                assert selected_cut % 2 == r_cut % 2 == mate_cut % 2 == 1
                assert replacement_cut % 2 == 1
                assert replacement_cut == selected_cut - r_cut + mate_cut
        alternatives.append((mate, replacement))

    # The exact selected-state rewrite is 1-3+1+1=0.  All four state
    # monomials have the same valuation if every supported cell is assigned
    # valuation -1, so a minimum-valuation rule cannot discard any mate.
    replacement_weights = tuple(state_weight(state) for _mate, state in alternatives)
    assert sorted(replacement_weights) == [Fraction(-3), Fraction(1), Fraction(1)]
    assert state_weight(selected_state) + sum(replacement_weights, Fraction(0)) == 0
    assert all(len(state) == 9 for _mate, state in alternatives)

    # Reversibility is literal: every bridged state contains its mate, and
    # replacing it by R restores the selected state.
    for mate, replacement in alternatives:
        assert frozenset((replacement - mate) | r_occurrences) == selected_state

    print("verified all 729 homogeneous coefficient fibres vanish over Q")
    print("verified three selected constant monomials are individually 1")
    print("verified exact rewrite 1-3+1+1=0 on one global valuation plateau")
    print("verified every cancellation mate changes odd-cut size 3 to 1 and creates a bridge")


def edge_weight_product(matching):
    return product_fraction(edge_weight(edge) for edge in matching)


def product_fraction(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


if __name__ == "__main__":
    main()

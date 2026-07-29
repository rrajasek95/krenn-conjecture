#!/usr/bin/env python3
"""Exact audits for occurrence-bridge rewrites and the degree-two boundary.

The first model satisfies three normalized constant equations and one mixed
four-term equation.  The second model satisfies every homogeneous fibre
equation, with exactly two nonzero terms in every fibre.  All arithmetic is
over ``fractions.Fraction``.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product


VERTICES = tuple(range(6))
COLORS = tuple(range(3))
SHORE = frozenset((0, 3, 5))

P0 = ((0, 4), (1, 2), (3, 5))
P1 = ((0, 5), (1, 4), (2, 3))
P2 = ((0, 3), (1, 5), (2, 4))
SELECTED = (P0, P1, P2)
R = ((0, 4), (1, 5), (2, 3))
MIXED_COLORING = (0, 2, 1, 1, 0, 2)


def perfect_matchings(vertices=VERTICES):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        remaining = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remaining):
            yield tuple(sorted(((u, v),) + tail))


PERFECT_MATCHINGS = tuple(perfect_matchings())
assert len(PERFECT_MATCHINGS) == 15


def decorate(matching, coloring):
    return frozenset((u, v, coloring[u], coloring[v]) for u, v in matching)


def state_value(state, weights):
    answer = Fraction(1)
    for occurrence in state:
        answer *= weights[occurrence]
    return answer


def fibre(coloring, weights):
    answer = []
    for matching in PERFECT_MATCHINGS:
        state = decorate(matching, coloring)
        if state <= weights.keys():
            answer.append((matching, state, state_value(state, weights)))
    return tuple(answer)


def endpoint_stubs(occurrence):
    u, v, a, b = occurrence
    return ((u, a), (v, b))


def assert_locally_rainbow(state):
    stubs = sorted(stub for occurrence in state for stub in endpoint_stubs(occurrence))
    assert stubs == [(v, a) for v in VERTICES for a in COLORS]


def components(state):
    adjacency = {v: set() for v in VERTICES}
    for u, v, _a, _b in state:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(VERTICES)
    answer = []
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        component = {seed}
        frontier = [seed]
        while frontier:
            vertex = frontier.pop()
            for neighbor in adjacency[vertex] & unseen:
                unseen.remove(neighbor)
                component.add(neighbor)
                frontier.append(neighbor)
        answer.append(frozenset(component))
    return tuple(answer)


def bridges(state):
    """Return bridge occurrences, retaining multiplicities in ``state``."""

    state = tuple(state)
    base_components = len(components(state))
    answer = []
    for index, occurrence in enumerate(state):
        deleted = state[:index] + state[index + 1 :]
        if len(components(deleted)) > base_components:
            answer.append(occurrence)
    return tuple(answer)


def crossing_count(state, shore=SHORE):
    return sum((u in shore) != (v in shore) for u, v, _a, _b in state)


def occurrence_perfect_matchings(state):
    """Enumerate occurrence submatchings; ``state`` is square-free here."""

    state = tuple(state)
    answer = []
    for indices in combinations(range(len(state)), 3):
        candidate = frozenset(state[index] for index in indices)
        endpoints = sorted(x for occurrence in candidate for x in occurrence[:2])
        if endpoints == list(VERTICES):
            answer.append(candidate)
    return tuple(answer)


def occurrence_coloring(matching):
    coloring = [-1] * len(VERTICES)
    for u, v, a, b in matching:
        coloring[u] = a
        coloring[v] = b
    assert -1 not in coloring
    return tuple(coloring)


def underlying_matching(state):
    return tuple(sorted(occurrence[:2] for occurrence in state))


def selected_state():
    return frozenset(
        occurrence
        for color, matching in enumerate(SELECTED)
        for occurrence in decorate(matching, (color,) * len(VERTICES))
    )


def connected_pair_graph(pair_support, retained):
    retained = set(retained)
    if not retained:
        return True
    seen = {min(retained)}
    frontier = list(seen)
    while frontier:
        vertex = frontier.pop()
        for edge in pair_support:
            if vertex not in edge:
                continue
            neighbor = edge[0] if edge[1] == vertex else edge[1]
            if neighbor in retained - seen:
                seen.add(neighbor)
                frontier.append(neighbor)
    return seen == retained


def verify_normalized_local_model():
    """Three normalized constants plus one exact bridge-rewrite fibre."""

    weights = {
        occurrence: Fraction(1)
        for color, matching in enumerate(SELECTED)
        for occurrence in decorate(matching, (color,) * len(VERTICES))
    }
    weights.update(
        {
            (1, 2, 2, 1): Fraction(-1, 3),
            (3, 5, 1, 2): Fraction(1),
            (0, 5, 0, 2): Fraction(-1, 3),
            (1, 4, 2, 0): Fraction(1),
            (0, 3, 0, 1): Fraction(-1, 3),
            (2, 4, 1, 0): Fraction(1),
        }
    )
    assert len(weights) == 15

    u_state = selected_state()
    r_state = decorate(R, MIXED_COLORING)
    q_state = u_state - r_state
    mates = tuple(decorate(matching, MIXED_COLORING) for matching in SELECTED)
    bridge_states = tuple(frozenset(q_state | mate) for mate in mates)

    assert state_value(u_state, weights) == 1
    assert state_value(r_state, weights) == 1
    assert state_value(q_state, weights) == 1
    assert tuple(state_value(mate, weights) for mate in mates) == (
        Fraction(-1, 3),
        Fraction(-1, 3),
        Fraction(-1, 3),
    )

    # The three constant fibres are singleton fibres with coefficient one.
    for color, matching in enumerate(SELECTED):
        coloring = (color,) * len(VERTICES)
        terms = fibre(coloring, weights)
        assert terms == ((matching, decorate(matching, coloring), Fraction(1)),)

    # The chosen mixed fibre is exactly 1-1/3-1/3-1/3=0.
    mixed_terms = fibre(MIXED_COLORING, weights)
    assert {matching for matching, _state, _value in mixed_terms} == {
        R,
        P0,
        P1,
        P2,
    }
    assert sorted(value for _matching, _state, value in mixed_terms) == [
        Fraction(-1, 3),
        Fraction(-1, 3),
        Fraction(-1, 3),
        Fraction(1),
    ]
    assert sum((value for _matching, _state, value in mixed_terms), Fraction(0)) == 0

    # This is deliberately a local subsystem, not a Krenn countermodel.
    term_count_histogram = Counter()
    nonzero_mixed = []
    for coloring in product(COLORS, repeat=len(VERTICES)):
        terms = fibre(coloring, weights)
        term_count_histogram[len(terms)] += 1
        coefficient = sum((value for _m, _s, value in terms), Fraction(0))
        if len(set(coloring)) > 1 and coefficient:
            nonzero_mixed.append((coloring, coefficient))
    assert term_count_histogram == Counter({0: 719, 1: 9, 4: 1})
    assert len(nonzero_mixed) == 6

    # Every one of the three cancellation alternatives has a unique bridge
    # across the same odd shore, and every occurrence-PM uses that bridge.
    expected_bridges = (
        (0, 4, 0, 0),
        (2, 3, 1, 1),
        (1, 5, 2, 2),
    )
    for state, expected_bridge in zip(bridge_states, expected_bridges):
        assert_locally_rainbow(state)
        assert len(components(state)) == 1
        assert crossing_count(state) == 1
        assert bridges(state) == (expected_bridge,)
        state_matchings = occurrence_perfect_matchings(state)
        assert len(state_matchings) == 4
        assert all(expected_bridge in matching for matching in state_matchings)

    # Multiplying the mixed fibre by Q gives the exact state relation.
    u_value = state_value(u_state, weights)
    bridge_values = tuple(state_value(state, weights) for state in bridge_states)
    assert bridge_values == (Fraction(-1, 3),) * 3
    assert u_value + sum(bridge_values, Fraction(0)) == 0

    # Degree doubling removes all literal graph bridges but not odd-cut
    # capacity.  Six perfect matchings would cross an odd cut at least six
    # times, whereas every G_i G_j has only two crossing occurrences.
    for matching in PERFECT_MATCHINGS:
        plain_state = tuple((u, v, 0, 0) for u, v in matching)
        assert crossing_count(plain_state) % 2 == 1
        assert crossing_count(plain_state) >= 1
    for left in bridge_states:
        for right in bridge_states:
            doubled_state = tuple(left) + tuple(right)
            degrees = Counter(vertex for occurrence in doubled_state for vertex in occurrence[:2])
            assert degrees == Counter({vertex: 6 for vertex in VERTICES})
            assert crossing_count(doubled_state) == 2 < 6
            assert not bridges(doubled_state)

    # Exact square-level dual: evaluation at this rational point kills all
    # four multiples of u+g0+g1+g2 in the quadratic state space, while it
    # takes u^2 to one.  The same point kills F_0-1,F_1-1,F_2-1 and F_c.
    state_values = (u_value,) + bridge_values
    assert sum(state_values, Fraction(0)) == 0
    quadratic_dual = {
        (i, j): state_values[i] * state_values[j]
        for i in range(4)
        for j in range(i, 4)
    }
    for multiplier in range(4):
        pairing = sum(
            (quadratic_dual[tuple(sorted((summand, multiplier)))] for summand in range(4)),
            Fraction(0),
        )
        assert pairing == 0
    assert quadratic_dual[(0, 0)] == 1
    assert u_value**2 == sum(bridge_values, Fraction(0)) ** 2 == 1

    # A second, non-evaluation dual isolates the monomial-cone failure.  In
    # the span of products of u,g0,g1,g2, only u^2 has enough cut capacity
    # even to be a union of six perfect matchings.  The rank-one quadratic
    # functional alpha_i alpha_j with alpha=(0,1,-1,0) kills u^2 and all
    # four multiples of the rewrite relation, but detects g0^2.
    alpha = (Fraction(0), Fraction(1), Fraction(-1), Fraction(0))
    cone_dual = {
        (i, j): alpha[i] * alpha[j]
        for i in range(4)
        for j in range(i, 4)
    }
    for multiplier in range(4):
        pairing = sum(
            (cone_dual[tuple(sorted((summand, multiplier)))] for summand in range(4)),
            Fraction(0),
        )
        assert pairing == 0
    assert cone_dual[(0, 0)] == 0
    assert cone_dual[(1, 1)] == 1

    pair_support = frozenset(occurrence[:2] for occurrence in weights)
    prism_support = frozenset(edge for matching in SELECTED for edge in matching)
    assert pair_support == prism_support

    return term_count_histogram, tuple(nonzero_mixed)


FULL_SUPPORT_SPEC = {
    (0, 1): "12",
    (0, 2): "10 11 12",
    (0, 3): "00 01 02 20 21 22",
    (0, 4): "00 01 02 20 21 22",
    (0, 5): "00 01 10 11 20 21",
    (1, 2): "00 02 10 12 20 21 22",
    (1, 4): "00 01 02 10 11 12",
    (1, 5): "01 02 11 12 21 22",
    (2, 3): "10 11 12",
    (2, 4): "00 01 02 20 21 22",
    (2, 5): "10 12",
    (3, 4): "00 01 02 10 11 12 20 21 22",
    (3, 5): "00 02 10 12 20 22",
}

BASE_NEGATIVE_CELLS = frozenset(
    {
        (1, 5, 0, 1),
        (1, 5, 1, 1),
        (1, 5, 2, 1),
        (2, 5, 1, 0),
        (2, 5, 1, 2),
        (3, 5, 0, 0),
        (3, 5, 0, 2),
        (3, 5, 1, 0),
        (3, 5, 1, 2),
        (3, 5, 2, 0),
        (3, 5, 2, 2),
    }
)


def full_binomial_weights():
    """The 67-cell sign model, after normalizing the selected P0 term."""

    weights = {}
    for (u, v), labels in FULL_SUPPORT_SPEC.items():
        for labels_at_ends in labels.split():
            a, b = map(int, labels_at_ends)
            occurrence = (u, v, a, b)
            value = -1 if occurrence in BASE_NEGATIVE_CELLS else 1
            # Endpoint gauge at the port (0,0).  It preserves every zero
            # fibre sum and changes the selected P0 monomial from -1 to +1.
            if u == 0 and a == 0:
                value = -value
            weights[occurrence] = Fraction(value)
    assert len(weights) == 67
    return weights


def verify_full_binomial_model():
    """All 729 fibres vanish, but the three constant coefficients are zero."""

    weights = full_binomial_weights()
    fibre_count = 0
    for coloring in product(COLORS, repeat=len(VERTICES)):
        terms = fibre(coloring, weights)
        assert len(terms) == 2
        assert sorted(value for _m, _s, value in terms) == [Fraction(-1), Fraction(1)]
        assert sum((value for _m, _s, value in terms), Fraction(0)) == 0
        fibre_count += 1
    assert fibre_count == 3**6

    # The selected pure monomials can all be gauged to +1 even though each
    # complete pure coefficient has a second term and hence equals zero.
    for color, matching in enumerate(SELECTED):
        coloring = (color,) * len(VERTICES)
        assert state_value(decorate(matching, coloring), weights) == 1
        assert sum((value for _m, _s, value in fibre(coloring, weights)), Fraction(0)) == 0

    u_state = selected_state()
    r_state = decorate(R, MIXED_COLORING)
    q_state = u_state - r_state
    n_state = decorate(P0, MIXED_COLORING)
    bridge_state = frozenset(q_state | n_state)
    bridge = (0, 4, 0, 0)
    assert_locally_rainbow(bridge_state)
    assert crossing_count(bridge_state) == 1
    assert bridges(bridge_state) == (bridge,)

    state_matchings = occurrence_perfect_matchings(bridge_state)
    assert len(state_matchings) == 4
    assert all(bridge in matching for matching in state_matchings)
    assert {occurrence_coloring(matching) for matching in state_matchings} == {
        (0, 0, 0, 0, 0, 0),
        (0, 0, 0, 1, 0, 2),
        (0, 2, 1, 0, 0, 0),
        MIXED_COLORING,
    }

    # Audit the unique all-fibre mate of each mixed occurrence-PM in the
    # bridged state.  Two moves retain cut size one and merely move the
    # bridge; the reversible move restores U and cut size three.
    expected = {
        (0, 0, 0, 1, 0, 2): (P2, 1, ((1, 5, 0, 2),)),
        (0, 2, 1, 0, 0, 0): (((0, 5), (1, 2), (3, 4)), 1, ((3, 4, 0, 0),)),
        MIXED_COLORING: (R, 3, ()),
    }
    replacement_audit = {}
    for matching in state_matchings:
        coloring = occurrence_coloring(matching)
        if len(set(coloring)) == 1:
            continue
        terms = fibre(coloring, weights)
        assert len(terms) == 2
        mate = next(state for _underlying, state, _value in terms if state != matching)
        replacement = frozenset((bridge_state - matching) | mate)
        expected_matching, expected_cut, expected_bridges = expected[coloring]
        assert underlying_matching(mate) == expected_matching
        assert crossing_count(matching) == 1
        assert crossing_count(replacement) == expected_cut
        assert bridges(replacement) == expected_bridges
        replacement_audit[coloring] = (
            crossing_count(matching),
            crossing_count(mate),
            crossing_count(replacement),
        )
    assert replacement_audit == {
        (0, 0, 0, 1, 0, 2): (1, 1, 1),
        (0, 2, 1, 0, 0, 0): (1, 1, 1),
        MIXED_COLORING: (1, 3, 3),
    }

    # The full pair support is dense and has no pair-level bridge or
    # nontrivial tight cut: it is K6 with two edges removed.
    all_pairs = frozenset(combinations(VERTICES, 2))
    pair_support = frozenset(occurrence[:2] for occurrence in weights)
    assert pair_support == all_pairs - {(1, 3), (4, 5)}
    assert sum((u in SHORE) != (v in SHORE) for u, v in pair_support) == 7
    for deleted_size in range(3):
        for deleted in combinations(VERTICES, deleted_size):
            retained = set(VERTICES) - set(deleted)
            assert connected_pair_graph(pair_support, retained)
    supported_pair_matchings = tuple(
        matching for matching in PERFECT_MATCHINGS if set(matching) <= pair_support
    )
    assert all(any(edge in matching for matching in supported_pair_matchings) for edge in pair_support)
    for shore_tuple in combinations(VERTICES, 3):
        shore = frozenset(shore_tuple)
        cut_counts = {
            sum((u in shore) != (v in shore) for u, v in matching)
            for matching in supported_pair_matchings
        }
        assert cut_counts != {1}

    # A nonzero signed solution of every binomial directly rules out an odd
    # Laurent sign circuit on this support.
    assert all(value in (Fraction(-1), Fraction(1)) for value in weights.values())

    return replacement_audit, len(supported_pair_matchings)


def main():
    local_histogram, local_errors = verify_normalized_local_model()
    replacement_audit, pair_matching_count = verify_full_binomial_model()
    print("verified normalized 15-cell model: three constants and one mixed fibre")
    print(f"local fibre term-count histogram: {dict(sorted(local_histogram.items()))}")
    print(f"local model has exactly {len(local_errors)} other nonzero mixed fibres")
    print("verified every doubled bridge product is bridge-free but has cut multiplicity 2 < 6")
    print("verified exact quadratic dual evaluation: (u,g0,g1,g2)=(1,-1/3,-1/3,-1/3)")
    print("verified cone-separating quadratic dual: alpha=(0,1,-1,0)")
    print("verified 67-cell model: all 729 fibres are opposite-sign binomials")
    print(f"full pair support has {pair_matching_count} perfect matchings and is 3-connected")
    print(f"mixed bridge replacement cut audit: {replacement_audit}")


if __name__ == "__main__":
    main()

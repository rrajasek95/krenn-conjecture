#!/usr/bin/env python3
"""Exact N=8 r=4 matching-frontier packet and its first repair.

The packet is not a GHZ source.  It certifies that essential/head-axis and
the sitewise four-cover do not reduce the minimum reciprocal count below
four.  Its smallest displayed pure-support repair, however, creates curved
rank-one good wedges by the exact flat-wedge rank theorem.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product


N = 8
COLORS = range(3)
GENERIC = (1, 1, 1)

# Four reciprocal pairs and sixteen singly oriented pairs.
ARCS = {
    (0, 1), (0, 3), (0, 5),
    (1, 0), (1, 2), (1, 3),
    (2, 3), (2, 5), (2, 7),
    (3, 2), (3, 4), (3, 5),
    (4, 1), (4, 5), (4, 7),
    (5, 4), (5, 6), (5, 7),
    (6, 1), (6, 3), (6, 7),
    (7, 0), (7, 1), (7, 6),
}

# The colour of every selected outgoing witness arc.
LABEL = dict([
    ((0, 1), 0), ((0, 3), 1), ((0, 5), 2),
    ((1, 0), 0), ((1, 2), 2), ((1, 3), 1),
    ((2, 3), 1), ((2, 5), 0), ((2, 7), 2),
    ((3, 2), 1), ((3, 4), 2), ((3, 5), 0),
    ((4, 1), 2), ((4, 5), 0), ((4, 7), 1),
    ((5, 4), 0), ((5, 6), 2), ((5, 7), 1),
    ((6, 1), 0), ((6, 3), 2), ((6, 7), 1),
    ((7, 0), 2), ((7, 1), 0), ((7, 6), 1),
])

# Endpoint incidences, not directed witness arcs.
ESSENTIAL = {
    (0, 1), (0, 7), (1, 3), (1, 4),
    (2, 1), (2, 3), (3, 5), (3, 6),
    (4, 3), (4, 5), (5, 0), (5, 7),
    (6, 5), (6, 7), (7, 1), (7, 2),
}

# The two generic/generic blocks are not selected witnesses.  They are the
# displayed termwise pure-support repair and create no new carrier arc.
REPAIR = {(0, 2), (4, 6)}


def edge(u, v):
    return (u, v) if u < v else (v, u)


def axis(colour):
    return tuple(int(index == colour) for index in COLORS)


def rank(rows):
    matrix = [list(map(Fraction, row)) for row in rows if any(row)]
    pivot = 0
    for column in COLORS:
        found = next((row for row in range(pivot, len(matrix))
                      if matrix[row][column]), None)
        if found is None:
            continue
        matrix[pivot], matrix[found] = matrix[found], matrix[pivot]
        value = matrix[pivot][column]
        matrix[pivot] = [entry / value for entry in matrix[pivot]]
        for row in range(len(matrix)):
            if row != pivot and matrix[row][column]:
                value = matrix[row][column]
                matrix[row] = [left - value * right
                               for left, right in zip(matrix[row],
                                                      matrix[pivot])]
        pivot += 1
    return pivot


def perfect_matchings(vertices, support):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for second in vertices[1:]:
        if edge(first, second) not in support:
            continue
        rest = tuple(vertex for vertex in vertices
                     if vertex not in (first, second))
        for tail in perfect_matchings(rest, support):
            yield ((first, second),) + tail


def build_endpoint_lines():
    selected = {edge(*arc) for arc in ARCS}
    endpoint = {}

    # Incoming selected arcs fix their head endpoint to the labelled axis.
    for tail, head in ARCS:
        endpoint[(head, tail)] = axis(LABEL[(tail, head)])

    common = {}
    for site in range(N):
        neighbours = [other for other in range(N)
                      if edge(site, other) in selected]
        nonessential = [other for other in neighbours
                        if (site, other) not in ESSENTIAL]
        fixed = {endpoint[(site, other)] for other in nonessential
                 if (site, other) in endpoint}
        if fixed:
            assert len(fixed) == 1
            common[site] = next(iter(fixed))
        else:
            common[site] = GENERIC
        for other in nonessential:
            endpoint[(site, other)] = common[site]

        # A free essential tail factor may be generic.  The fixed essential
        # head axes plus this line are checked below to span dimension three.
        for other in neighbours:
            if (site, other) in ESSENTIAL:
                endpoint.setdefault((site, other), GENERIC)

    # The repair blocks use the already determined common line at each end.
    for left, right in REPAIR:
        endpoint[(left, right)] = common[left]
        endpoint[(right, left)] = common[right]
    return selected, selected | REPAIR, common, endpoint


def audit_selected_witnesses(selected, common, endpoint):
    assert len(ARCS) == 24 and len(selected) == 20
    for site in range(N):
        outgoing = [(head, LABEL[(site, head)])
                    for tail, head in ARCS if tail == site]
        assert len(outgoing) == 3
        assert {colour for _head, colour in outgoing} == set(COLORS)
        assert len({head for head, _colour in outgoing}) == 3
        for head, colour in outgoing:
            assert endpoint[(head, site)] == axis(colour)

    reciprocal = {pair for pair in selected
                  if pair in ARCS and pair[::-1] in ARCS}
    assert reciprocal == {(0, 1), (2, 3), (4, 5), (6, 7)}

    counts = Counter(tail for tail, _head in ESSENTIAL)
    assert counts == Counter({site: 2 for site in range(N)})
    good_selected = {pair for pair in selected
                     if pair not in ESSENTIAL and pair[::-1] not in ESSENTIAL}
    assert good_selected == {(0, 3), (1, 6), (2, 5), (4, 7)}
    assert good_selected.isdisjoint(reciprocal)

    # The line flags realize exactly the named essential incidences.
    for site in range(N):
        neighbours = [other for other in range(N)
                      if edge(site, other) in selected]
        rows = [endpoint[(site, other)] for other in neighbours]
        assert rank(rows) == 3
        for other in neighbours:
            deleted_rank = rank([endpoint[(site, third)]
                                 for third in neighbours if third != other])
            assert (deleted_rank < 3) == ((site, other) in ESSENTIAL)
    assert {site for site, line in common.items() if line != GENERIC} == {
        1, 3, 5, 7
    }
    return reciprocal, good_selected


def carrier_options(support, endpoint):
    options = {}
    for site in range(N):
        colour_lists = []
        for colour in COLORS:
            colour_lists.append([
                other for other in range(N)
                if edge(site, other) in support
                and endpoint[(other, site)] == axis(colour)
            ])
        choices = []
        for local in product(*colour_lists):
            if len(set(local)) == 3:
                choices.append(local)
        assert choices
        options[site] = tuple(choices)
    return options


def audit_minimum_reciprocity(support, endpoint):
    options = carrier_options(support, endpoint)
    histogram = Counter()
    best = N * N
    total = 0
    for choices in product(*(options[site] for site in range(N))):
        arcs = {(site, head) for site, local in enumerate(choices)
                for head in local}
        reciprocal = {edge(tail, head) for tail, head in arcs
                      if (head, tail) in arcs}
        value = len(reciprocal)
        histogram[value] += 1
        best = min(best, value)
        total += 1
    # Four generic-head sites have two admissible local carrier triples;
    # the four axis-head sites have one.  The repair blocks are not carriers.
    assert total == 16
    assert best == 4
    return best, dict(sorted(histogram.items()))


def audit_pure_support_and_curvature(support, endpoint, good_selected):
    pure = {}
    for colour in COLORS:
        terms = [matching for matching in perfect_matchings(range(N), support)
                 if all(endpoint[(left, right)][colour]
                        and endpoint[(right, left)][colour]
                        for left, right in matching)]
        assert terms
        pure[colour] = terms

    expected_witnesses = {
        0: ((0, 2), (1, 7), (3, 5), (4, 6)),
        1: ((0, 2), (1, 3), (4, 6), (5, 7)),
        2: ((0, 5), (1, 4), (2, 7), (3, 6)),
    }
    for colour, witness in expected_witnesses.items():
        assert witness in pure[colour]

    good_physical = good_selected | REPAIR
    assert good_physical == {
        (0, 2), (0, 3), (2, 5),
        (1, 6), (4, 6), (4, 7),
    }
    # Each adjacent good wedge has a nonzero rank-one opposite chord.  The
    # exact flat-wedge theorem would require that chord to have rank >=2;
    # hence every exact source on this packet has a curved rank-one overlap.
    wedges = {
        (3, 0, 2): (2, 3),
        (0, 2, 5): (0, 5),
        (1, 6, 4): (1, 4),
        (6, 4, 7): (6, 7),
    }
    for (_left, _centre, _right), chord in wedges.items():
        assert chord in support
        assert rank([endpoint[(chord[0], chord[1])]]) == 1
        assert rank([endpoint[(chord[1], chord[0])]]) == 1
    return {colour: len(terms) for colour, terms in pure.items()}, wedges


def audit_pairwise_four_cover(support, endpoint, reciprocal):
    ledger = {}
    for pair in sorted(reciprocal):
        residual = sorted(set(range(N)) - set(pair))
        counts = []
        site_cover = {}
        for colour in COLORS:
            count = 0
            for site in residual:
                rows = [endpoint[(site, other)] for other in residual
                        if other != site and edge(site, other) in support]
                if rank(rows + [axis(colour)]) == rank(rows):
                    count += 1
            counts.append(count)
        for site in residual:
            rows = [endpoint[(site, other)] for other in residual
                    if other != site and edge(site, other) in support]
            site_cover[site] = tuple(colour for colour in COLORS
                                     if rank(rows + [axis(colour)]) == rank(rows))
            assert site_cover[site]
        assert min(counts) >= 4
        ledger[pair] = (tuple(counts), site_cover)
    return ledger


def main():
    selected, support, common, endpoint = build_endpoint_lines()
    reciprocal, good_selected = audit_selected_witnesses(
        selected, common, endpoint
    )
    minimum, histogram = audit_minimum_reciprocity(support, endpoint)
    pure_counts, wedges = audit_pure_support_and_curvature(
        support, endpoint, good_selected
    )
    covers = audit_pairwise_four_cover(support, endpoint, reciprocal)

    print("N=8 r=4 matching incidence frontier: PASS")
    print("selected/physical blocks:", len(selected), len(support))
    print("minimum reciprocity over carrier reselections:", minimum)
    print("reselection histogram:", histogram)
    print("pure matching-term counts:", pure_counts)
    print("forced curved good wedges:", wedges)
    print("pairwise four-cover counts:",
          {pair: data[0] for pair, data in covers.items()})
    print("scope: structural packet, not a GHZ source")


if __name__ == "__main__":
    main()

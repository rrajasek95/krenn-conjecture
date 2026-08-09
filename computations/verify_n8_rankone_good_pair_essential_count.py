#!/usr/bin/env python3
"""Exact audit of the N=8 essential-count rank-one good-pair theorem.

The first half checks the universal counting ledger.  The second constructs
sharp endpoint-support data with 24 nonreciprocal, colour-labelled rank-one
witnesses, 17 bad pairs, and seven good pairs.  That construction is a sharp
counterguard for the incidence argument, not an exact matching source.
"""

from __future__ import annotations

from itertools import combinations


N = 8
COLORS = (0, 1, 2)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(u, v):
    require(u != v, "loop is not a physical pair")
    return tuple(sorted((u, v)))


def universal_count_ledger():
    """Audit the worst essential-incidence budget by complement size."""

    lower_bounds = []
    for missing_rank_one_edges in range(5):
        rank_one_edges = len(tuple(combinations(range(N), 2))) - missing_rank_one_edges

        # Three essential neighbours force rank-one degree exactly three,
        # hence four missing R-edges at the vertex.  It is impossible if
        # fewer than four R-edges are missing, and at most one such vertex
        # exists when exactly four are missing.
        max_three_essential_vertices = int(missing_rank_one_edges == 4)
        essential_budget = (
            3 * max_three_essential_vertices
            + 2 * (N - max_three_essential_vertices)
        )
        lower_bounds.append(rank_one_edges - essential_budget)

    require(lower_bounds == [12, 11, 10, 9, 7],
            "rank-one good-pair lower-bound ledger changed")

    # Two vertices cannot both have four incident edges inside a graph with
    # at most four edges: their two four-edge stars overlap in at most uv.
    all_edges = set(combinations(range(N), 2))
    for missing in combinations(all_edges, 4):
        missing = set(missing)
        degree_four = [
            u for u in range(N)
            if sum(u in pair for pair in missing) == 4
        ]
        require(len(degree_four) <= 1,
                "four-edge complement acquired two degree-four vertices")
    return lower_bounds


def sharp_support_counterguard():
    """Realize equality in the 17-bad/7-good support-incidence ledger."""

    # R is K7 on 1,...,7 plus the three edges 01,02,03.  Orient K7 as the
    # regular cyclic tournament, with steps 1,2,3 carrying colours 0,1,2.
    arcs = []
    for tail in range(1, 8):
        for color, step in enumerate((1, 2, 3)):
            head = 1 + ((tail - 1 + step) % 7)
            arcs.append((tail, head, color))
    arcs.extend((0, head, head - 1) for head in (1, 2, 3))

    require(len(arcs) == 24 and len(set(arcs)) == 24,
            "sharp witness arc count changed")
    directed = {(tail, head) for tail, head, _color in arcs}
    require(all((head, tail) not in directed for tail, head in directed),
            "sharp witness orientation acquired a reciprocal pair")
    for tail in range(N):
        outgoing = [(head, color) for source, head, color in arcs
                    if source == tail]
        require(len(outgoing) == 3, "witness outdegree changed")
        require({color for _head, color in outgoing} == set(COLORS),
                "one tail lost a target colour witness")

    rank_one_edges = {edge(tail, head) for tail, head, _color in arcs}
    require(len(rank_one_edges) == 24,
            "nonreciprocal arcs did not give 24 physical pairs")
    all_edges = set(combinations(range(N), 2))
    missing = all_edges - rank_one_edges
    require(missing == {(0, 4), (0, 5), (0, 6), (0, 7)},
            "sharp complement is no longer the four-edge star")

    # Store the one-dimensional mode support of each nonzero block at both
    # endpoints.  At a witness head it is the required coordinate axis.
    # At an outer witness tail all three free tail factors use one repeated
    # axis.  The three centre-tail factors use the three independent axes.
    repeated_axis = {1: 0, 2: 1, 3: 2, 4: 0, 5: 0, 6: 0, 7: 0}
    local_axis = {}
    for tail, head, color in arcs:
        pair = edge(tail, head)
        require(pair not in local_axis, "physical witness edge repeated")
        tail_axis = color if tail == 0 else repeated_axis[tail]
        local_axis[pair] = {tail: tail_axis, head: color}
        require(local_axis[pair][head] == color,
                "head coordinate factor lost its source colour")

    def rank_at(u, omitted_neighbor=None):
        axes = {
            local_axis[pair][u]
            for pair in rank_one_edges
            if u in pair and omitted_neighbor not in pair
        }
        return len(axes)

    essential = {}
    for u in range(N):
        require(rank_at(u) == 3, "endpoint supports do not span dimension 3")
        essential[u] = {
            v for v in range(N) if v != u
            and rank_at(u, omitted_neighbor=v) < 3
        }

        # A zero block has zero support and its deletion cannot lower rank.
        for v in range(N):
            if v != u and edge(u, v) in missing:
                require(v not in essential[u], "zero block became essential")

    require(essential[0] == {1, 2, 3},
            "centre equality case lost its three essentials")
    require(all(len(essential[u]) == 2 for u in range(1, 8)),
            "outer equality case no longer has two essentials")
    essential_incidences = {(u, v) for u in range(N) for v in essential[u]}
    require(len(essential_incidences) == 17,
            "sharp essential-incidence budget changed")

    bad = {
        pair for pair in rank_one_edges
        if (pair[0], pair[1]) in essential_incidences
        or (pair[1], pair[0]) in essential_incidences
    }
    good = rank_one_edges - bad
    require(len(bad) == 17 and len(good) == 7,
            "sharp bad/good rank-one split changed")
    require(all(
        not ({(u, v), (v, u)} <= essential_incidences)
        for u, v in rank_one_edges
    ), "sharp support model double-counted an essential edge")
    return missing, essential, good


def main():
    lower_bounds = universal_count_ledger()
    missing, essential, good = sharp_support_counterguard()
    print("good rank-one lower bounds for 0..4 missing R-edges:", lower_bounds)
    print("sharp complement:", sorted(missing))
    print("essential counts:", tuple(len(essential[u]) for u in range(N)))
    print("sharp good rank-one pairs:", sorted(good))
    print("N=8 essential-count rank-one good-pair theorem: PASS")


if __name__ == "__main__":
    main()

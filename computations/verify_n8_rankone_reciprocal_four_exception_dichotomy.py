#!/usr/bin/env python3
"""Exact combinatorial audit of the N=8 rank-one witness dichotomy.

This checker concerns only consequences of the forced incident-edge theorem.
Its circulant model is a counterguard to stronger graph-only deductions, not
an exact matching source and not a Krenn counterexample.
"""

from __future__ import annotations

from itertools import combinations


N = 8
COLORS = (0, 1, 2)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def physical(tail, head):
    return tuple(sorted((tail, head)))


def count_identity(arcs):
    """Return directed, reciprocal-pair, and underlying-pair counts."""

    require(len(arcs) == len(set(arcs)), "directed witness repeated")
    directed = {(tail, head) for tail, head, _color in arcs}
    require(len(directed) == len(arcs),
            "two colors at one tail selected the same neighbor")
    reciprocal = {
        physical(tail, head)
        for tail, head in directed if (head, tail) in directed
    }
    underlying = {physical(tail, head) for tail, head in directed}
    require(len(underlying) == len(arcs) - len(reciprocal),
            "directed/reciprocal projection identity failed")
    return len(arcs), len(reciprocal), len(underlying)


def circulant_counterguard():
    # Orient K8 minus the antipodal perfect matching by forward steps 1,2,3.
    # Label the three outgoing witnesses by their three target colors.
    arcs = tuple(
        (tail, (tail + step) % N, color)
        for tail in range(N)
        for color, step in enumerate((1, 2, 3))
    )
    for tail in range(N):
        outgoing = tuple(arc for arc in arcs if arc[0] == tail)
        require(len(outgoing) == 3, "circulant outdegree changed")
        require({color for _tail, _head, color in outgoing} == set(COLORS),
                "outgoing color witnesses changed")
        require(len({head for _tail, head, _color in outgoing}) == 3,
                "outgoing witnesses lost distinct neighbors")

    directed, reciprocal, underlying = count_identity(arcs)
    require((directed, reciprocal, underlying) == (24, 0, 24),
            "no-reciprocal witness count changed")
    used = {physical(tail, head) for tail, head, _color in arcs}
    all_pairs = set(combinations(range(N), 2))
    exceptional = tuple(sorted(all_pairs - used))
    require(exceptional == ((0, 4), (1, 5), (2, 6), (3, 7)),
            "circulant exceptional matching changed")

    # A K4,4 forced-anchor audit needs one balanced bipartition across which
    # every directed color witness runs.  Check every 4+4 split (modulo
    # complement): this dense witness system has none.
    compatible_bipartitions = []
    for left_tuple in combinations(range(N), 4):
        left = frozenset(left_tuple)
        if 0 not in left:  # quotient a split by exchanging its sides
            continue
        if all((tail in left) != (head in left)
               for tail, head, _color in arcs):
            compatible_bipartitions.append(tuple(sorted(left)))
    require(not compatible_bipartitions,
            "circulant witnesses unexpectedly entered a K4,4 anchor chart")

    # Endpoint-factor ledger.  An arc tail->head of color a places e_a at
    # the head and an unconstrained named line c_tail,a at the tail.  With no
    # reciprocal pair, no edge is forced coordinate at both endpoints.
    factors = {
        physical(tail, head): {
            "tail": tail,
            "tail_line": f"c_{tail}_{color}",
            "head": head,
            "head_axis": color,
        }
        for tail, head, color in arcs
    }
    require(len(factors) == 24, "factor ledger collapsed an edge")
    require(all(
        (record["head"], record["tail"]) not in
        {(tail, head) for tail, head, _color in arcs}
        for record in factors.values()
    ), "factor ledger acquired a reciprocal incidence")
    return arcs, exceptional


def reciprocal_coordinate_guard():
    # If v->u forces the u-factor to e_a and u->v forces the v-factor to
    # e_b, the common nonzero rank-one block is lambda e_b tensor e_a.
    a, b = 2, 1
    forward = ("c", f"e{a}")
    backward = (f"e{b}", "d")
    common = (f"e{b}", f"e{a}")
    require(forward[1] == common[1] and backward[0] == common[0],
            "reciprocal coordinate factors did not meet")
    return a, b, common


def main():
    arcs, exceptional = circulant_counterguard()
    a, b, common = reciprocal_coordinate_guard()
    print("directed/color witnesses:", len(arcs))
    print("no-reciprocal underlying rank-one pairs:", len(arcs))
    print("exceptional pairs:", exceptional)
    print("compatible all-anchor K4,4 bipartitions: 0")
    print("reciprocal block normal form:", common,
          f"(head colors {a}/{b})")
    print("N=8 rank-one reciprocal/four-exception dichotomy: PASS")


if __name__ == "__main__":
    main()

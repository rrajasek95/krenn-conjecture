#!/usr/bin/env python3
"""Audit a cone-free K-degree-nine row with no leading incident column.

The example shows that the 4+2 pair-switch/cone collapse is not a global
theorem for every row below degree sixteen.  It is not asserted to occur in
the support propagated from P^2.
"""

from __future__ import annotations

import sys

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])

import lift_power2_offdiag2 as L


def node_degrees(row):
    degrees = {(v, a): 0 for v in range(6) for a in range(3)}
    off, gs = row
    for i in off:
        u, v, a, b = L.OFF_VARS[i]
        degrees[u, a] += 1
        degrees[v, b] += 1
    for a, z in enumerate(gs):
        for i, multiplicity in enumerate(L.decode(z)):
            if multiplicity:
                u, v = L.EDGES[i]
                degrees[u, a] += multiplicity
                degrees[v, a] += multiplicity
    return degrees


def main():
    # Each color has a diagonal triangle on vertices 0,1,2.
    diagonal = []
    for _a in range(3):
        exponents = [0] * len(L.EDGES)
        for edge in ((0, 1), (0, 2), (1, 2)):
            exponents[L.EDGE_INDEX[edge]] = 1
        diagonal.append(L.encode(exponents))

    # On the other nine vertex/color nodes, use a bichromatic 9-cycle.
    cycle = (
        (3, 0),
        (4, 1),
        (5, 2),
        (3, 1),
        (4, 2),
        (5, 0),
        (3, 2),
        (4, 0),
        (5, 1),
    )
    off = []
    for (u, a), (v, b) in zip(cycle, cycle[1:] + cycle[:1]):
        if u > v:
            u, v, a, b = v, u, b, a
        assert u != v and a != b
        off.append(L.OFF_INDEX[u, v, a, b])

    row = L.canonical_row(tuple(sorted(off)), tuple(diagonal))
    assert len(row[0]) == 9
    assert set(node_degrees(row).values()) == {2}
    assert not L.monomial_killed(row)
    assert not L.incident_leading_columns(row)

    # In fact the underlying support is the disjoint union of two triangles,
    # so it contains no perfect matching and cannot occur in any Macaulay
    # column at any filtration degree.
    underlying = set()
    for i in row[0]:
        underlying.add(L.OFF_VARS[i][:2])
    for z in row[1]:
        for i, multiplicity in enumerate(L.decode(z)):
            if multiplicity:
                underlying.add(L.EDGES[i])
    assert not any(set(pm) <= underlying for pm in L.PM)
    print("verified isolated K-degree-nine row")
    print(row)


if __name__ == "__main__":
    main()

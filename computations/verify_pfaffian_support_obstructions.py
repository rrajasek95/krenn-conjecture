#!/usr/bin/env python3
"""Exact finite checks for the Pfaffian-support reduction obstructions.

The script checks three independent graph facts used in
``notes/pfaffian-support-six-reduction.md``:

* the standard six-vertex Pfaffian signs have a multiplicative holonomy
  which no edge rescaling (even over C*) can remove;
* a planar, 3-connected, matching-covered eight-vertex graph has a
  two-vertex Pfaffian Schur pivot whose six-vertex support contains K_3,3;
* K_4,4 has no nontrivial tight cut, while each conformal K_3,3 obtained by
  deleting one vertex from each shore has six contaminating cross edges.
"""

from __future__ import annotations

import itertools

import networkx as nx
import sympy as sp


def perfect_matchings(graph, vertices=None):
    vertices = frozenset(graph if vertices is None else vertices)
    if not vertices:
        yield ()
        return
    u = min(vertices)
    for v in sorted(graph[u] & vertices):
        edge = (min(u, v), max(u, v))
        for tail in perfect_matchings(graph, vertices - {u, v}):
            yield (edge,) + tail


def pfaffian_sign(matching):
    edges = sorted(matching)
    crossings = sum(
        u < x < v < y or x < u < y < v
        for index, (u, v) in enumerate(edges)
        for x, y in edges[index + 1 :]
    )
    return -1 if crossings % 2 else 1


def check_six_vertex_sign_holonomy():
    positive = (
        ((0, 1), (2, 5), (3, 4)),
        ((0, 2), (1, 4), (3, 5)),
        ((0, 3), (1, 5), (2, 4)),
    )
    negative = (
        ((0, 1), (2, 4), (3, 5)),
        ((0, 2), (1, 5), (3, 4)),
        ((0, 3), (1, 4), (2, 5)),
    )
    assert [pfaffian_sign(matching) for matching in positive] == [1, 1, 1]
    assert [pfaffian_sign(matching) for matching in negative] == [-1, -1, -1]
    left_edges = sorted(edge for matching in positive for edge in matching)
    right_edges = sorted(edge for matching in negative for edge in matching)
    assert left_edges == right_edges


def check_planar_pivot_creates_nonpfaffian_support():
    p, q = 6, 7
    graph = nx.Graph()
    graph.add_edges_from((i, (i + 1) % 6) for i in range(6))
    graph.add_edges_from((p, i) for i in (0, 1, 2))
    graph.add_edges_from((q, i) for i in (3, 4, 5))
    graph.add_edge(p, q)

    planar, _embedding = nx.check_planarity(graph)
    assert planar
    assert nx.node_connectivity(graph) == 3
    matchings = tuple(perfect_matchings({u: set(graph[u]) for u in graph}))
    used_edges = {edge for matching in matchings for edge in matching}
    assert used_edges == {tuple(sorted(edge)) for edge in graph.edges()}

    # Pivot P=(p,q).  Give pq weight one, all six star edges weight one,
    # and the boundary C6 edges weight two.  With
    # M=[[0,1],[-1,0]], the Schur term is nonzero on every pair joining
    # {0,1,2} to {3,4,5}.
    M = sp.Matrix([[0, 1], [-1, 0]])
    inverse = M.inv()
    columns = {
        r: sp.Matrix([1, 0]) if r < 3 else sp.Matrix([0, 1])
        for r in range(6)
    }
    N = sp.zeros(6, 6)
    cycle = {tuple(sorted((i, (i + 1) % 6))) for i in range(6)}
    for r, s in itertools.combinations(range(6), 2):
        direct = 2 if (r, s) in cycle else 0
        value = direct + (columns[r].T * inverse * columns[s])[0]
        N[r, s] = value
        N[s, r] = -value
    assert all(N[r, s] for r in range(3) for s in range(3, 6))

    # The six K_3,3 determinant terms split into three even and three odd
    # permutations.  Both triples use every cross edge exactly once, so the
    # opposite sign products cannot be corrected by edge scalars.
    even, odd = [], []
    for permutation in itertools.permutations(range(3, 6)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
        matching = tuple((i, permutation[i]) for i in range(3))
        (odd if inversions % 2 else even).append(matching)
    assert len(even) == len(odd) == 3
    assert sorted(e for m in even for e in m) == sorted(e for m in odd for e in m)


def check_k44_contamination():
    left = frozenset(range(4))
    right = frozenset(range(4, 8))
    adjacency = {
        vertex: (set(right) if vertex in left else set(left))
        for vertex in left | right
    }
    matchings = tuple(perfect_matchings(adjacency))
    assert len(matchings) == 24

    # Every nontrivial odd shore may be represented by a three-set.  Its
    # crossing number is not constantly one over the perfect matchings.
    for shore in itertools.combinations(range(8), 3):
        shore = frozenset(shore)
        counts = {
            sum((u in shore) != (v in shore) for u, v in matching)
            for matching in matchings
        }
        assert counts != {1}

    # Deleting one vertex on each shore leaves a conformal K_3,3 and one
    # complementary edge, but exactly six support edges cross between them.
    for x in left:
        for y in right:
            inside = (left - {x}) | (right - {y})
            outside = {x, y}
            assert y in adjacency[x]
            cross = {
                tuple(sorted((u, v)))
                for u in inside
                for v in outside
                if v in adjacency[u]
            }
            assert len(cross) == 6


def main():
    check_six_vertex_sign_holonomy()
    print("verified nonremovable six-vertex Pfaffian sign holonomy")
    check_planar_pivot_creates_nonpfaffian_support()
    print("verified planar 3-connected pivot with non-Pfaffian K3,3 response")
    check_k44_contamination()
    print("verified K4,4 conformal-minor contamination and tight-cut freeness")


if __name__ == "__main__":
    main()

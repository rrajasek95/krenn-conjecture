#!/usr/bin/env python3
"""Exact exhaustive check of the monomial rank-one n=6, q=3 ansatz.

Every nonzero aggregate edge matrix is assumed to have exactly one nonzero
coordinate.  Three nonzero constant coefficients then select three
edge-disjoint perfect matchings, whose two colored isomorphism types are the
triangular prism and K_3,3.  Once those nine entries are fixed, the six
remaining pairs have 9^6 possible ordered endpoint-color labels.

For every labeling this verifier finds a mixed output basis tensor supported
by exactly one perfect matching, so no choice of nonzero scalar weights can
cancel all mixed coefficients.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product


N = 6
Q = 3
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for pos in range(1, len(vertices)):
        v = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            yield tuple(sorted(((u, v),) + matching))


MATCHINGS = tuple(perfect_matchings(VERTICES))


def relabel_matching(matching, permutation):
    return tuple(sorted(
        (min(permutation[u], permutation[v]), max(permutation[u], permutation[v]))
        for u, v in matching
    ))


def canonical_colored_triple(triple):
    forms = []
    for vertex_permutation in permutations(VERTICES):
        relabeled = [relabel_matching(matching, vertex_permutation)
                     for matching in triple]
        for color_permutation in permutations(range(Q)):
            forms.append(tuple(relabeled[color_permutation[color]]
                               for color in range(Q)))
    return min(forms)


def colored_triple_orbits():
    representatives = {}
    for triple in combinations(MATCHINGS, Q):
        if len(set().union(*map(set, triple))) != 9:
            continue
        canonical = canonical_colored_triple(triple)
        representatives.setdefault(canonical, triple)
    return tuple(representatives.values())


def output_coloring(matching, labels):
    coloring = [-1] * N
    for u, v in matching:
        coloring[u], coloring[v] = labels[(u, v)]
    return tuple(coloring)


def check_representative(target_matchings):
    labels = {
        edge: (color, color)
        for color, matching in enumerate(target_matchings)
        for edge in matching
    }
    free_edges = tuple(edge for edge in EDGES if edge not in labels)
    assert len(free_edges) == 6

    minimum_singletons = len(MATCHINGS)
    minimizing_assignment = None
    for encoded in product(range(Q * Q), repeat=len(free_edges)):
        for edge, value in zip(free_edges, encoded):
            labels[edge] = divmod(value, Q)
        fibers = Counter(output_coloring(matching, labels)
                         for matching in MATCHINGS)
        singleton_mixed = sum(
            multiplicity == 1 and len(set(coloring)) > 1
            for coloring, multiplicity in fibers.items()
        )
        if singleton_mixed < minimum_singletons:
            minimum_singletons = singleton_mixed
            minimizing_assignment = encoded
    assert minimum_singletons > 0
    return minimum_singletons, free_edges, minimizing_assignment


def main():
    representatives = colored_triple_orbits()
    assert len(representatives) == 2, len(representatives)
    results = []
    for representative in representatives:
        supported_in_union = sum(
            set(matching) <= set().union(*map(set, representative))
            for matching in MATCHINGS
        )
        minimum, free_edges, assignment = check_representative(representative)
        results.append((supported_in_union, minimum))
        print("target matchings:", representative)
        print("perfect matchings in their union:", supported_in_union)
        print("minimum singleton mixed fibers:", minimum)
        print("one minimizing free-edge assignment:",
              tuple(zip(free_edges, map(lambda z: divmod(z, Q), assignment))))
    assert sorted(results) == [(4, 6), (6, 4)]
    print("verified both colored isomorphism types exactly")


if __name__ == "__main__":
    main()

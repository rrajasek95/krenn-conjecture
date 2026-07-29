#!/usr/bin/env python3
"""Enumerate active pure-color binary supports on six vertices.

An edge has one of two diagonal colors, and every supported perfect matching
must be monochromatic.  For every closed union support, this script finds
the components of the perfect-matching intersection graph, assigns them to
both colors, and numerically computes the least squared edge norm needed for
the two scalar hafnians to equal one.

The optimization is only a discovery aid; small extremizers printed here
should subsequently be proved exactly.
"""

from __future__ import annotations

import itertools

import numpy as np

from verify_binary_spinflip_cycle_identity import perfect_matchings


N = 6
EDGES = tuple(itertools.combinations(range(N), 2))
INDEX = {e: i for i, e in enumerate(EDGES)}
MATCHINGS = tuple(
    frozenset(INDEX[e] for e in matching)
    for matching in perfect_matchings(tuple(range(N)))
)


def components(matchings):
    unseen = set(range(len(matchings)))
    answer = []
    while unseen:
        todo = [unseen.pop()]
        component = []
        while todo:
            i = todo.pop()
            component.append(i)
            neighbors = [j for j in unseen if matchings[i] & matchings[j]]
            for j in neighbors:
                unseen.remove(j)
                todo.append(j)
        answer.append(tuple(component))
    return tuple(answer)


def spectral_value(edge_set, matching_set, seed=0):
    """Maximum of sum_M prod_e x_e on the positive unit sphere."""
    edges = tuple(sorted(edge_set))
    local = {e: i for i, e in enumerate(edges)}
    triples = tuple(tuple(local[e] for e in matching) for matching in matching_set)
    rng = np.random.default_rng(seed)
    best_value = 0.0
    best_x = None
    starts = [np.ones(len(edges))]
    starts += [rng.random(len(edges)) for _ in range(24)]
    # Include all individual matching faces, which catch boundary maxima.
    for triple in triples:
        x = np.zeros(len(edges))
        x[list(triple)] = 1
        starts.append(x)
    for x in starts:
        x = x / np.linalg.norm(x)
        for _ in range(10000):
            grad = np.zeros_like(x)
            for a, b, c in triples:
                grad[a] += x[b] * x[c]
                grad[b] += x[a] * x[c]
                grad[c] += x[a] * x[b]
            norm = np.linalg.norm(grad)
            if not norm:
                break
            y = grad / norm
            if np.linalg.norm(y - x) < 1e-13:
                x = y
                break
            x = y
        value = sum(x[a] * x[b] * x[c] for a, b, c in triples)
        if value > best_value:
            best_value = value
            best_x = x.copy()
    return best_value, edges, best_x


def main():
    closed = {}
    for mask in range(1 << len(EDGES)):
        allowed = tuple(M for M in MATCHINGS if all(mask >> e & 1 for e in M))
        if len(allowed) < 2:
            continue
        active = frozenset().union(*allowed)
        if mask != sum(1 << e for e in active):
            continue
        key = tuple(sorted(tuple(sorted(M)) for M in allowed))
        closed[key] = (active, allowed)

    cache = {}
    records = []
    for active, allowed in closed.values():
        comps = components(allowed)
        if len(comps) < 2:
            continue
        # Quotient by swapping colors: require component zero in color zero.
        for assignment in range(1 << (len(comps) - 1)):
            chosen = {0}
            chosen.update(i + 1 for i in range(len(comps) - 1) if assignment >> i & 1)
            if len(chosen) == len(comps):
                continue
            colors = []
            for side in (chosen, set(range(len(comps))) - chosen):
                mids = tuple(i for c in side for i in comps[c])
                matching_set = tuple(allowed[i] for i in mids)
                edge_set = frozenset().union(*matching_set)
                key = tuple(sorted(tuple(sorted(M)) for M in matching_set))
                if key not in cache:
                    cache[key] = spectral_value(edge_set, matching_set, seed=len(cache))
                value, edges, x = cache[key]
                energy = value ** (-2 / 3)
                colors.append((energy, matching_set, edges, x))
            total = colors[0][0] + colors[1][0]
            records.append((total, colors, allowed))

    records.sort(key=lambda record: record[0])
    print("closed supports", len(closed), "colored records", len(records))
    for total, colors, allowed in records[:20]:
        print("total", round(total, 12), "allowed", [sorted(M) for M in allowed])
        for energy, matchings, edges, x in colors:
            print(
                " energy", round(energy, 12),
                "matchings", [sorted(M) for M in matchings],
                "weights", [(EDGES[e], round(float(w), 8)) for e, w in zip(edges, x)],
            )


if __name__ == "__main__":
    main()

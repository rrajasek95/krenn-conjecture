"""All six-site support graphs, with exact realizations of the survivors."""

from collections import Counter
from itertools import combinations
import stars  # Initialize the pinned exact-algebra import path.
from algebra import (ZERO, ONE, OMEGA, require, matchings, four_outputs, five_ground)


def check():
    edges = list(combinations(range(6), 2))
    ix = {edge: i for i, edge in enumerate(edges)}
    quartet_masks = [[sum(1 << ix[edge] for edge in matching) for matching in matchings(U)]
                     for U in combinations(range(6), 4)]
    counts = Counter()
    for mask in range(1 << len(edges)):
        if any(sum((mask & m) == m for m in ms) == 1 for ms in quartet_masks):
            counts["unique_matching_rejected"] += 1
            continue
        support = {edge for i, edge in enumerate(edges) if mask & (1 << i)}
        active = {v for edge in support for v in edge}
        neighbors = {v: {w for edge in support if v in edge for w in edge if w != v}
                     for v in range(6)}
        if any(len(neighbors[v]) >= 3 and not active <= ({v} | neighbors[v]) for v in range(6)):
            counts["closed_neighborhood_rejected"] += 1
            continue
        is_star = any(all(v in edge for edge in support) for v in range(6))
        weights = {edge: ONE for edge in support}
        if len(active) <= 4:
            counts["at_most_four_active"] += 1
            if len(active) == 4:
                ms = [matching for matching in matchings(tuple(sorted(active)))
                      if all(edge in support for edge in matching)]
                if ms:
                    require(len(ms) in (2, 3), "A surviving quartet can cancel")
                    targets = [ONE, -ONE] if len(ms) == 2 else [ONE, OMEGA, OMEGA*OMEGA]
                    for matching, target in zip(ms, targets):
                        weights[matching[0]] = target
        elif is_star:
            counts["larger_star"] += 1
        elif len(active) == 5 and len(support) == 10:
            counts["five_clique"] += 1
            vertices = sorted(active)
            weights = {(vertices[i], vertices[j]): z for (i, j), z in five_ground().items()}
        else:
            # Section 4 of the proof excludes these using the maximum degree.
            require(max(map(len, neighbors.values())) >= 4,
                    "The remaining rejection falls under the star/scalar-core lemmas")
            counts["star_or_scalar_core_rejected"] += 1
            continue
        require(set(weights) == support and all(weights.values()), "Exact requested support")
        source = {(*edge, 0, 0): z for edge, z in weights.items()}
        require(not four_outputs(source, 6, 1), "Every survivor has an exact flat realization")
    expected = dict(unique_matching_rejected=31954, closed_neighborhood_rejected=390,
                    star_or_scalar_core_rejected=76, at_most_four_active=306,
                    larger_star=36, five_clique=6)
    require(dict(counts) == expected, "Complete six-site support census")
    require(sum(counts.values()) == 32768, "All graphs accounted for")
    return dict(total_graphs=32768, counts=dict(counts), realized_supports=348)

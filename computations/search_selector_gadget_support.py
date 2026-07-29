#!/usr/bin/env python3
"""Enumerate same-color three-terminal selector-gadget supports.

For an odd vertex set, choose three edge-disjoint near-perfect matchings
P_r leaving terminal r and color every edge of P_r by r.  For each boundary
state r, enumerate all matchings of the union leaving r.  A mixed coloring
with exactly one matching is an exact obstruction for every nonzero choice
of edge weights.  This is a finite support-level discovery/audit tool.
"""

from __future__ import annotations

import argparse
import itertools


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for index, v in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield ((min(u, v), max(u, v)),) + tail


def analyze(order: int) -> None:
    vertices = tuple(range(order))
    terminals = (0, 1, 2)
    families = {
        r: tuple(perfect_matchings(tuple(v for v in vertices if v != r)))
        for r in terminals
    }
    tested = 0
    disjoint = 0
    best = None
    survivors = []
    for p0 in families[0]:
        s0 = set(p0)
        for p1 in families[1]:
            s1 = set(p1)
            if s0 & s1:
                continue
            for p2 in families[2]:
                tested += 1
                s2 = set(p2)
                if (s0 | s1) & s2:
                    continue
                disjoint += 1
                colored = {
                    edge: color
                    for color, matching in enumerate((p0, p1, p2))
                    for edge in matching
                }
                fiber_sizes = {}
                for missing in terminals:
                    remaining = tuple(v for v in vertices if v != missing)
                    for matching in perfect_matchings(remaining):
                        if not all(edge in colored for edge in matching):
                            continue
                        coloring = tuple(
                            colored[edge]
                            for v in remaining
                            for edge in matching
                            if v in edge
                        )
                        # The loop above follows matching order, not vertex
                        # order; rebuild the canonical coloring explicitly.
                        at_vertex = {}
                        for edge in matching:
                            for v in edge:
                                at_vertex[v] = colored[edge]
                        coloring = tuple(at_vertex[v] for v in remaining)
                        key = (missing, coloring)
                        fiber_sizes[key] = fiber_sizes.get(key, 0) + 1
                singleton_mixed = sum(
                    size == 1 and len(set(coloring)) > 1
                    for (missing, coloring), size in fiber_sizes.items()
                )
                score = (singleton_mixed, len(fiber_sizes))
                if best is None or score < best[0]:
                    best = (score, (p0, p1, p2), fiber_sizes)
                if singleton_mixed == 0:
                    survivors.append(((p0, p1, p2), fiber_sizes))
                    print(
                        f"survivor {len(survivors)} fibers={len(fiber_sizes)} "
                        f"matchings={(p0, p1, p2)}",
                        flush=True,
                    )
                    if len(survivors) >= 20:
                        break
            if len(survivors) >= 20:
                break
        if len(survivors) >= 20:
            break
    print(
        f"order={order} tested={tested} disjoint={disjoint} "
        f"best_singletons={best[0][0] if best else None} "
        f"survivors={len(survivors)}"
    )
    if best is not None:
        print("best matchings", best[1])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, choices=(5, 7, 9), default=7)
    args = parser.parse_args()
    analyze(args.order)


if __name__ == "__main__":
    main()

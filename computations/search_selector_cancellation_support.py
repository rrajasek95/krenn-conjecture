#!/usr/bin/env python3
"""Search support-only repairs of the sparse 8-vertex selector construction."""

import itertools
from collections import defaultdict


def perfect_matchings(vertices):
    vertices = frozenset(vertices)
    if not vertices:
        yield ()
        return
    u = min(vertices)
    for v in sorted(vertices - {u}):
        for rest in perfect_matchings(vertices - {u, v}):
            yield tuple(sorted(((u, v),) + rest))


PMS = list(perfect_matchings(range(8)))
P0 = ((0, 1), (2, 3), (4, 5), (6, 7))
P1 = ((0, 2), (1, 4), (3, 6), (5, 7))
P2 = ((0, 3), (1, 5), (2, 6), (4, 7))


def cells_for(matching, coloring):
    return {
        (u, v, coloring[u], coloring[v])
        for u, v in matching
    }


BASE = cells_for(P0, (0,) * 8) | cells_for(P1, (1,) * 8) | cells_for(P2, (2,) * 8)


def fibers(cells):
    by_edge = defaultdict(set)
    for u, v, a, b in cells:
        by_edge[u, v].add((a, b))
    out = defaultdict(int)
    for matching in PMS:
        choices = [by_edge[e] for e in matching]
        if any(not choice for choice in choices):
            continue
        for decorations in itertools.product(*choices):
            coloring = [None] * 8
            for (u, v), (a, b) in zip(matching, decorations):
                coloring[u] = a
                coloring[v] = b
            out[tuple(coloring)] += 1
    return out


base_fibers = fibers(BASE)
mixed = [c for c, count in base_fibers.items() if len(set(c)) > 1]
assert len(mixed) == 2 and all(base_fibers[c] == 1 for c in mixed)
C3, C4 = mixed
print("bad colorings", C3, C4)

best = None
survivors = []
for i, n3 in enumerate(PMS):
    add3 = cells_for(n3, C3)
    for n4 in PMS:
        cells = BASE | add3 | cells_for(n4, C4)
        fs = fibers(cells)
        singletons = [c for c, count in fs.items() if len(set(c)) > 1 and count == 1]
        score = (len(singletons), len(cells), len(fs))
        if best is None or score < best[0]:
            best = (score, n3, n4, singletons[:4])
        if not singletons and all(fs[(r,) * 8] for r in range(3)):
            survivors.append((n3, n4, len(cells), len(fs), fs))
            print("survivor", n3, n4, len(cells), len(fs))
            raise SystemExit
print("best", best)


def singleton_mixed(fs):
    return tuple(sorted(c for c, count in fs.items() if len(set(c)) > 1 and count == 1))


beam = {frozenset(BASE)}
seen = set(beam)
for depth in range(1, 9):
    candidates = []
    for state in beam:
        fs = fibers(state)
        bad = singleton_mixed(fs)
        if not bad:
            print("beam survivor", depth - 1, len(state), len(fs), sorted(state))
            raise SystemExit
        color = bad[0]
        existing_matchings = set()
        for matching in PMS:
            if cells_for(matching, color) <= state:
                existing_matchings.add(matching)
        for matching in PMS:
            if matching in existing_matchings:
                continue
            nxt = frozenset(set(state) | cells_for(matching, color))
            if nxt in seen:
                continue
            seen.add(nxt)
            nfs = fibers(nxt)
            nbad = singleton_mixed(nfs)
            score = (len(nbad), len(nxt), len(nfs))
            candidates.append((score, nxt))
    candidates.sort(key=lambda item: item[0])
    beam = {state for _, state in candidates[:300]}
    print("depth", depth, "states", len(beam), "best", candidates[0][0] if candidates else None)
    if not beam:
        break
for state in beam:
    fs = fibers(state)
    if not singleton_mixed(fs):
        print("beam survivor", len(state), len(fs), sorted(state))
        break

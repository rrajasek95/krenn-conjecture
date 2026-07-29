#!/usr/bin/env python3
"""Enumerate the torus-forced two-extra rectangle charts at small orders."""

from __future__ import annotations

import argparse
import itertools

from verify_binary_spinflip_cycle_identity import perfect_matchings


def union_is_hamilton(first, second, n):
    adjacency = {v: [] for v in range(n)}
    for occurrence in tuple(first) + tuple(second):
        u, v = occurrence
        adjacency[u].append(v)
        adjacency[v].append(u)
    # Parallel differently colored occurrences form a 2-cycle component.
    seen = set()
    stack = [0]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        stack.extend(v for v in adjacency[u] if v not in seen)
    return len(seen) == n


def bipartition(first, second, n):
    adjacency = {v: [] for v in range(n)}
    for u, v in tuple(first) + tuple(second):
        adjacency[u].append(v)
        adjacency[v].append(u)
    sign = {0: 0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if v not in sign:
                sign[v] = 1 - sign[u]
                stack.append(v)
            else:
                assert sign[v] != sign[u]
    return sign


def cycle_positions(first, second, n):
    adjacency = {v: [] for v in range(n)}
    for u, v in tuple(first) + tuple(second):
        adjacency[u].append(v)
        adjacency[v].append(u)
    order = [0]
    previous = None
    current = 0
    while True:
        following = next(v for v in adjacency[current] if v != previous)
        if following == 0:
            break
        order.append(following)
        previous, current = current, following
    assert len(order) == n
    return {v: i for i, v in enumerate(order)}


def chords_interlace(first, second, positions):
    n = len(positions)

    def inside(value, start, end):
        return 0 < (value - start) % n < (end - start) % n

    a, b = (positions[v] for v in first)
    c, d = (positions[v] for v in second)
    return inside(c, a, b) != inside(d, a, b)


def has_opposite_shore_interlace(chords, sign, positions):
    same_shore = [edge for edge in chords if sign[edge[0]] == sign[edge[1]]]
    return any(
        sign[first[0]] != sign[second[0]] and chords_interlace(first, second, positions)
        for first, second in itertools.combinations(same_shore, 2)
    )


def occurrence_matchings(occurrences, n):
    by_vertex = {v: [] for v in range(n)}
    for index, (edge, colors) in enumerate(occurrences):
        u, v = edge
        by_vertex[u].append(index)
        by_vertex[v].append(index)

    def rec(uncovered, chosen):
        if not uncovered:
            yield tuple(chosen)
            return
        u = min(uncovered)
        for index in by_vertex[u]:
            edge, _ = occurrences[index]
            v = edge[1] if edge[0] == u else edge[0]
            if v not in uncovered:
                continue
            yield from rec(uncovered - {u, v}, chosen + [index])

    yield from rec(set(range(n)), [])


def fibers(occurrences, n):
    answer = {}
    for chosen in occurrence_matchings(occurrences, n):
        coloring = [None] * n
        underlying = []
        valid = True
        for index in chosen:
            (u, v), (a, b) = occurrences[index]
            if coloring[u] not in (None, a) or coloring[v] not in (None, b):
                valid = False
                break
            coloring[u], coloring[v] = a, b
            underlying.append((u, v))
        if valid:
            key = tuple(coloring)
            answer.setdefault(key, set()).add(tuple(sorted(underlying)))
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, choices=(6, 8, 10))
    parser.add_argument("--stop-after", type=int, default=1)
    parser.add_argument("--hard-only", action="store_true")
    parser.add_argument("--very-hard", action="store_true")
    parser.add_argument("--no-interlace-a", action="store_true")
    args = parser.parse_args()
    n = args.n
    matchings = tuple(tuple(m) for m in perfect_matchings(tuple(range(n))))
    pc = set(matchings[0])
    hamilton = [set(p) for p in matchings if union_is_hamilton(pc, set(p), n)]
    charts = 0
    support_survivors = []
    displayed = 0
    for pa in hamilton:
        sign_ac = bipartition(pa, pc, n)
        for pb in hamilton:
            if not union_is_hamilton(pa, pb, n):
                continue
            sign_ab = bipartition(pa, pb, n)
            sign_bc = bipartition(pb, pc, n)
            positions_bc = cycle_positions(pb, pc, n)
            positions_ac = cycle_positions(pa, pc, n)
            base = [
                (edge, (color, color))
                for color, factor in enumerate((pa, pb, pc))
                for edge in factor
            ]
            for u, up in pa:
                for v, vp in pb:
                    for vv, vvp in ((v, vp), (vp, v)):
                        if u == vv or up == vvp:
                            continue
                        # Extra a-b cells are allowed by both minimal-pair
                        # defect lemmas only when their endpoints share both
                        # relevant shore signs.
                        if sign_ac[u] != sign_ac[vv] or sign_ac[up] != sign_ac[vvp]:
                            continue
                        if sign_bc[u] != sign_bc[vv] or sign_bc[up] != sign_bc[vvp]:
                            continue
                        if sign_ab[u] != sign_ab[vv] or sign_ab[up] != sign_ab[vvp]:
                            continue
                        if args.hard_only or args.very_hard:
                            cross_a = sum(sign_bc[x] != sign_bc[y] for x, y in pa)
                            cross_b = sum(sign_ac[x] != sign_ac[y] for x, y in pb)
                            if cross_a != 1 or cross_b != 1:
                                continue
                        if args.very_hard:
                            if has_opposite_shore_interlace(pa, sign_bc, positions_bc):
                                continue
                            if has_opposite_shore_interlace(pb, sign_ac, positions_ac):
                                continue
                        elif args.no_interlace_a:
                            if has_opposite_shore_interlace(pa, sign_bc, positions_bc):
                                continue
                        extras = [
                            (tuple(sorted((u, vv))), (0, 1) if u < vv else (1, 0)),
                            (tuple(sorted((up, vvp))), (0, 1) if up < vvp else (1, 0)),
                        ]
                        if extras[0][0] == extras[1][0]:
                            continue
                        occurrences = tuple(base + extras)
                        charts += 1
                        fs = fibers(occurrences, n)
                        singleton = next(
                            (
                                (coloring, next(iter(terms)))
                                for coloring, terms in fs.items()
                                if len(set(coloring)) > 1 and len(terms) == 1
                            ),
                            None,
                        )
                        if singleton is not None and displayed < 5:
                            print("WITNESS", "pa", sorted(pa), "pb", sorted(pb),
                                  "extras", extras, "fiber", singleton)
                            displayed += 1
                        if singleton is None:
                            support_survivors.append((pa, pb, pc, extras, fs))
                            print("SURVIVOR", pa, pb, extras)
                            if len(support_survivors) >= args.stop_after:
                                print("charts", charts, "survivors", len(support_survivors))
                                return
    print("charts", charts, "survivors", len(support_survivors))


if __name__ == "__main__":
    main()

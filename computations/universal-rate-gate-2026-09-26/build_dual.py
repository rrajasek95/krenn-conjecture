#!/usr/bin/env python3
"""Construct a sparse separating functional; verifier uses full ideal multiples.

Writes JSON to stdout. Uses only Python's standard library.
"""
import itertools as it
import json
from collections import defaultdict


def matchings(vertices):
    if not vertices:
        yield ()
        return
    for j in range(1, len(vertices)):
        for matching in matchings(vertices[1:j] + vertices[j + 1:]):
            yield ((vertices[0], vertices[j]),) + matching


def main():
    ms = list(matchings(tuple(range(6))))
    rows = set(it.product(range(15), repeat=3))
    dead = {row for row in rows
            if any(len(set(sum(edges, ()))) == 6 for edges in it.product(*(ms[i] for i in row)))}
    relations = []
    for i, j, k in it.permutations(range(3)):
        for edge in it.combinations(range(6), 2):
            group = [z for z, matching in enumerate(ms) if edge in matching]
            for mi in group:
                for mk in range(15):
                    relation = set()
                    for mj in group:
                        row = [0] * 3
                        row[i], row[j], row[k] = mi, mj, mk
                        relation.add(tuple(row))
                    relations.append(relation)
    while True:
        new = {next(iter(r - dead)) for r in relations if len(r - dead) == 1}
        if not new:
            break
        dead |= new
    adjacency = defaultdict(set)
    for relation in relations:
        live = sorted(relation - dead)
        if len(live) == 2:
            a, b = live
            adjacency[a].add(b)
            adjacency[b].add(a)
        elif len(live) > 2:
            raise ValueError("unexpected residual relation size")
    root = min(rows - dead)
    signs = {root: 1}
    stack = [root]
    while stack:
        a = stack.pop()
        for b in sorted(adjacency[a]):
            if b in signs:
                if signs[b] != -signs[a]:
                    raise ValueError("component is not bipartite")
            else:
                signs[b] = -signs[a]
                stack.append(b)
    if not sum(signs.values()):
        raise ValueError("functional does not separate target")
    print(json.dumps({"matching_order": ms,
                      "functional": [{"triple": row, "value": signs[row]} for row in sorted(signs)],
                      "target_value": sum(signs.values())}, indent=2))


if __name__ == "__main__":
    main()

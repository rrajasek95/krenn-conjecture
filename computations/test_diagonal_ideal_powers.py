#!/usr/bin/env python3
"""Exact low-degree ideal tests in the diagonal n=6,q=3 specialization.

At degree 9, target-graded monomials are ordered triples of vertex perfect
matchings, one for each color (15^3 rows).  Only mixed colorings of types
4+2 and 2+2+2 have nonzero diagonal matching polynomials.  This constructs
the complete unaveraged Macaulay matrix for P=h_0 h_1 h_2.
"""

from __future__ import annotations

import itertools
from collections import defaultdict


def pms(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        for tail in pms(vertices[1:k] + vertices[k + 1 :]):
            yield (tuple(sorted((u, v))),) + tail


V = tuple(range(6))
PM = tuple(tuple(sorted(m)) for m in pms(V))
PM_INDEX = {m: i for i, m in enumerate(PM)}


def row_index(ms):
    return (PM_INDEX[ms[0]] * 15 + PM_INDEX[ms[1]]) * 15 + PM_INDEX[ms[2]]


def all_subset_matchings(s):
    return tuple(tuple(sorted(m)) for m in pms(tuple(sorted(s))))


def build_columns():
    columns = []
    for c in itertools.product(range(3), repeat=6):
        counts = tuple(c.count(a) for a in range(3))
        if counts in ((6, 0, 0), (0, 6, 0), (0, 0, 6)):
            continue
        # A diagonal F_c is zero unless every color class has even size.
        if any(z % 2 for z in counts):
            continue
        classes = [tuple(v for v in V if c[v] == a) for a in range(3)]
        f_terms = []
        for parts in itertools.product(*(all_subset_matchings(s) for s in classes)):
            f_terms.append(parts)

        # The multiplier uses, for each color, the complementary vertices.
        comps = [tuple(v for v in V if c[v] != a) for a in range(3)]
        for mult in itertools.product(*(all_subset_matchings(s) for s in comps)):
            rows = []
            for term in f_terms:
                full = [tuple(sorted(mult[a] + term[a])) for a in range(3)]
                rows.append(row_index(full))
            columns.append(tuple(rows))
    assert len(columns) == 6480
    assert sum(len(c) for c in columns) == 14580
    return columns


def rank_and_target(columns, prime=1009):
    pivots = {}

    def reduce(v):
        while v:
            r = min(v)
            a = v[r] % prime
            if not a:
                del v[r]
                continue
            if r not in pivots:
                inv = pow(a, prime - 2, prime)
                pivots[r] = {k: z * inv % prime for k, z in v.items() if z % prime}
                return True
            p = pivots[r]
            for k, z in p.items():
                w = (v.get(k, 0) - a * z) % prime
                if w:
                    v[k] = w
                elif k in v:
                    del v[k]
        return False

    for col in columns:
        v = defaultdict(int)
        for r in col:
            v[r] += 1
        reduce(dict(v))
    rank = len(pivots)
    target = {r: 1 for r in range(15**3)}
    aug = rank + reduce(target)
    print(f"GF({prime}): rank={rank}, augmented rank={aug}, P in span={aug == rank}")
    return rank, aug


if __name__ == "__main__":
    cols = build_columns()
    for p in (1009, 1013, 10007):
        rank_and_target(cols, p)

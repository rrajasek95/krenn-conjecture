#!/usr/bin/env python3
"""Test P^2 in the diagonal n=6,q=3 mixed-coefficient ideal.

This is the complete target-multigraded degree-18 Macaulay map, reduced
losslessly by S_6 x S_3.  A color graph is a loopless multigraph on six
vertices; target monomials have degree two at every vertex in each color.
"""

from __future__ import annotations

import itertools
import pickle
from collections import Counter
from functools import lru_cache
from pathlib import Path

import numpy as np


N = 6
EDGES = tuple((u, v) for u in range(N) for v in range(u + 1, N))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}


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


PM = tuple(tuple(sorted(m)) for m in pms(range(N)))
VERTEX_PERMS = tuple(itertools.permutations(range(N)))
COLOR_PERMS = tuple(itertools.permutations(range(3)))
EDGE_MAPS = []
for vp in VERTEX_PERMS:
    em = []
    for u, v in EDGES:
        e = tuple(sorted((vp[u], vp[v])))
        em.append(EDGE_INDEX[e])
    EDGE_MAPS.append(tuple(em))


def encode(exponents):
    z = 0
    mul = 1
    for a in exponents:
        z += a * mul
        mul *= 3
    return z


@lru_cache(None)
def decode(z):
    out = []
    for _ in EDGES:
        out.append(z % 3)
        z //= 3
    return tuple(out)


@lru_cache(None)
def transform_graph(z, vp_index):
    out = [0] * len(EDGES)
    for i, a in enumerate(decode(z)):
        out[EDGE_MAPS[vp_index][i]] = a
    return encode(out)


@lru_cache(None)
def graph_monomials(degrees):
    degrees = tuple(degrees)

    @lru_cache(None)
    def rec(k, ds):
        ds = list(ds)
        if k == len(EDGES):
            return ((),) if not any(ds) else ()
        u, v = EDGES[k]
        out = []
        for a in range(min(ds[u], ds[v]) + 1):
            ds[u] -= a
            ds[v] -= a
            for tail in rec(k + 1, tuple(ds)):
                out.append((a,) + tail)
            ds[u] += a
            ds[v] += a
        return tuple(out)

    return tuple(encode(x) for x in rec(0, degrees))


def transform_coloring(c, vp, cp):
    out = [None] * N
    for v in range(N):
        out[vp[v]] = cp[c[v]]
    return tuple(out)


def transform_triple(gs, vp_index, cp):
    out = [None] * 3
    for a in range(3):
        out[cp[a]] = transform_graph(gs[a], vp_index)
    return tuple(out)


def add_matching(z, matching):
    x = list(decode(z))
    for e in matching:
        x[EDGE_INDEX[e]] += 1
        assert x[EDGE_INDEX[e]] <= 2
    return encode(x)


COLOR_TYPES = ((0, 0, 0, 0, 1, 1), (0, 0, 1, 1, 2, 2))


def build_matrix(cache: Path | None):
    if cache and cache.exists():
        with cache.open("rb") as fh:
            d = pickle.load(fh)
        if d.get("version") == 2:
            return d

    columns = []
    raw_rows = set()
    for c in COLOR_TYPES:
        stabilizer = []
        for vi, vp in enumerate(VERTEX_PERMS):
            for cp in COLOR_PERMS:
                if transform_coloring(c, vp, cp) == c:
                    stabilizer.append((vi, cp))
        assert len(stabilizer) == 48

        choices = []
        classes = []
        for a in range(3):
            degrees = tuple(1 if c[v] == a else 2 for v in range(N))
            choices.append(graph_monomials(degrees))
            classes.append(tuple(v for v in range(N) if c[v] == a))
        unseen = set(itertools.product(*choices))
        reps = []
        while unseen:
            gs = next(iter(unseen))
            orb = {transform_triple(gs, vi, cp) for vi, cp in stabilizer}
            unseen.difference_update(orb)
            reps.append(min(orb))
        print(f"type {tuple(c.count(a) for a in range(3))}: column orbits={len(reps)}")

        f_terms = tuple(itertools.product(*(tuple(pms(s)) for s in classes)))
        for gs in reps:
            outputs = []
            for term in f_terms:
                outputs.append(tuple(add_matching(gs[a], term[a]) for a in range(3)))
            columns.append((c, gs, tuple(outputs)))
            raw_rows.update(outputs)

    # Canonicalize the modest set of rows reached from column representatives.
    row_canon = {}
    row_size = {}
    remaining = set(raw_rows)
    while remaining:
        gs = next(iter(remaining))
        orb = set()
        for vi in range(len(VERTEX_PERMS)):
            moved = tuple(transform_graph(z, vi) for z in gs)
            orb.update(itertools.permutations(moved))
        can = min(orb)
        row_size[can] = len(orb)
        met = remaining.intersection(orb)
        for z in met:
            row_canon[z] = can
        remaining.difference_update(met)
        if len(row_size) % 500 == 0:
            print(f"row orbits={len(row_size)}, raw remaining={len(remaining)}")

    row_reps = tuple(sorted(row_size))
    row_index = {z: i for i, z in enumerate(row_reps)}
    entries = []
    for j, (_, _, outputs) in enumerate(columns):
        counts = Counter(row_index[row_canon[z]] for z in outputs)
        entries.extend((i, j, a) for i, a in counts.items())

    # h^2 has coefficient one on doubled perfect matchings and coefficient two
    # on unions of two distinct matchings.
    h2 = Counter()
    zero = encode((0,) * len(EDGES))
    for m1 in PM:
        z1 = add_matching(zero, m1)
        for m2 in PM:
            h2[add_matching(z1, m2)] += 1
    assert len(h2) == 120 and sum(h2.values()) == 225

    b = np.zeros(len(row_reps), dtype=np.int64)
    for i, gs in enumerate(row_reps):
        coeff = h2.get(gs[0], 0) * h2.get(gs[1], 0) * h2.get(gs[2], 0)
        if coeff:
            b[i] = row_size[gs] * coeff
    represented = int(b.sum())
    print(
        f"matrix={len(row_reps)}x{len(columns)}, nnz={len(entries)}, "
        f"target orbits={np.count_nonzero(b)}, target mass={represented}/{225**3}"
    )

    d = {
        "version": 2,
        "shape": (len(row_reps), len(columns)),
        "entries": entries,
        "b": b,
        "complete_target": represented == 225**3,
        "column_reps": tuple((c, gs) for c, gs, _ in columns),
        "row_reps": row_reps,
        "row_sizes": tuple(row_size[z] for z in row_reps),
    }
    if cache:
        with cache.open("wb") as fh:
            pickle.dump(d, fh, protocol=pickle.HIGHEST_PROTOCOL)
    return d


def modular_membership(d, prime, return_solution=False):
    nr, nc = d["shape"]
    cols = [dict() for _ in range(nc)]
    for i, j, a in d["entries"]:
        cols[j][i] = a % prime
    pivots = {}
    pivot_combos = {}
    pivot_sources = {}

    def reduce(v, install, combo=None):
        while v:
            r = min(v)
            a = v[r] % prime
            if not a:
                del v[r]
                continue
            if r not in pivots:
                if install:
                    inv = pow(a, prime - 2, prime)
                    pivots[r] = {k: z * inv % prime for k, z in v.items() if z % prime}
                    pivot_sources[r] = j
                    if combo is not None:
                        pivot_combos[r] = {
                            k: z * inv % prime for k, z in combo.items() if z % prime
                        }
                return False
            p = pivots[r]
            pc = pivot_combos.get(r)
            for k, z in p.items():
                w = (v.get(k, 0) - a * z) % prime
                if w:
                    v[k] = w
                elif k in v:
                    del v[k]
            if combo is not None and pc is not None:
                for k, z in pc.items():
                    w = (combo.get(k, 0) - a * z) % prime
                    if w:
                        combo[k] = w
                    elif k in combo:
                        del combo[k]
        return True

    for j, v in enumerate(cols):
        reduce(v, True, {j: 1} if return_solution else None)
        if (j + 1) % 1000 == 0:
            print(f"columns {j+1}/{nc}, rank={len(pivots)}")
    rhs = {i: int(z % prime) for i, z in enumerate(d["b"]) if z % prime}
    if return_solution:
        solution = {}
        # Reduce b by the normalized pivot columns and accumulate their
        # original-column representations.
        while rhs:
            r = min(rhs)
            a = rhs[r] % prime
            if r not in pivots:
                break
            for k, z in pivots[r].items():
                w = (rhs.get(k, 0) - a * z) % prime
                if w:
                    rhs[k] = w
                elif k in rhs:
                    del rhs[k]
            for k, z in pivot_combos[r].items():
                w = (solution.get(k, 0) + a * z) % prime
                if w:
                    solution[k] = w
                elif k in solution:
                    del solution[k]
        inside = d["complete_target"] and not rhs
    else:
        solution = None
        inside = d["complete_target"] and reduce(rhs, False)
    print(f"GF({prime}): rank={len(pivots)}, P^2 in span={inside}")
    if solution is not None:
        # Direct sparse audit.
        image = Counter()
        for i, j, a in d["entries"]:
            if j in solution:
                image[i] = (image[i] + solution[j] * a) % prime
        assert all(image.get(i, 0) == int(d["b"][i]) % prime for i in range(nr))
        print(f"solution support={len(solution)}")
    return inside, solution, tuple(pivot_sources.values())


if __name__ == "__main__":
    cache = Path(__file__).with_name("diagonal_power2_orbits.pkl")
    d = build_matrix(cache)
    modular_membership(d, 1009)

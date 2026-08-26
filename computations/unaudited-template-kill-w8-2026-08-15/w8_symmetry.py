#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- fast exact canonical form under S_8 x S_3.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

The group acting on templates is S_8 (sites) x S_3 (colours), order 241920.
A template is a 28-tuple of 9-bit cell masks; the action permutes edges,
transposes the mask when the edge's endpoint order flips, and permutes the
colour indices.  canonical_fast returns the lexicographic minimum over the
whole group with precomputed tables (~10 us per image).  Pure integers.
"""

from __future__ import annotations

from itertools import permutations

import w8_core as C

_TABLES = {}


def tables(geo):
    key = geo.size
    if key in _TABLES:
        return _TABLES[key]
    # mask transformations: for each colour permutation and flip flag
    mask_map = {}
    for cp in permutations(range(3)):
        for flip in (0, 1):
            table = [0] * 512
            for mask in range(512):
                new = 0
                for c in range(9):
                    if (mask >> c) & 1:
                        i, j = divmod(c, 3)
                        a, b = cp[i], cp[j]
                        if flip:
                            a, b = b, a
                        new |= 1 << (3 * a + b)
                table[mask] = new
            mask_map[(cp, flip)] = table
    # edge transformations
    edge_map = []
    for perm in permutations(range(geo.size)):
        target = [0] * len(geo.edges)
        flips = [0] * len(geo.edges)
        for e, (u, v) in enumerate(geo.edges):
            pu, pv = perm[u], perm[v]
            if pu < pv:
                target[e] = geo.index[(pu, pv)]
                flips[e] = 0
            else:
                target[e] = geo.index[(pv, pu)]
                flips[e] = 1
        edge_map.append((tuple(target), tuple(flips)))
    _TABLES[key] = (edge_map, mask_map, tuple(permutations(range(3))))
    return _TABLES[key]


def canonical_fast(geo, template):
    edge_map, mask_map, colour_perms = tables(geo)
    n = len(geo.edges)
    best = None
    for target, flips in edge_map:
        for cp in colour_perms:
            t0 = mask_map[(cp, 0)]
            t1 = mask_map[(cp, 1)]
            image = [0] * n
            for e in range(n):
                mask = template[e]
                if mask:
                    image[target[e]] = t1[mask] if flips[e] else t0[mask]
            image = tuple(image)
            if best is None or image < best:
                best = image
    return best


def orbit_size(geo, template):
    edge_map, mask_map, colour_perms = tables(geo)
    n = len(geo.edges)
    seen = set()
    for target, flips in edge_map:
        for cp in colour_perms:
            t0 = mask_map[(cp, 0)]
            t1 = mask_map[(cp, 1)]
            image = [0] * n
            for e in range(n):
                mask = template[e]
                if mask:
                    image[target[e]] = t1[mask] if flips[e] else t0[mask]
            seen.add(tuple(image))
    return len(seen)

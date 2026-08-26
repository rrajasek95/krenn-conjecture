#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- isomorphism classes of support graphs on 8 sites.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

The whole template problem is S_8 x S_3 equivariant, so a template and its
image under any site relabelling are killed or not killed together.  Splitting
the exhaustion over ISOMORPHISM CLASSES OF THE SUPPORT GRAPH is therefore both
sound and complete, and it partitions the space (unlike a witness-triple split,
which overlaps).

NECESSARY CONDITIONS used to prune the class list (both proved here in code):
  * (SC) forces min degree >= 3: a vertex p needs, for each of the three
    colours r, an incident edge whose block is nonzero and supported in far
    colour r, and one edge can serve at most one colour at a given endpoint.
  * a nonempty constant fibre forces the support graph to contain a perfect
    matching.

Canonical form = the minimum, over all 8! = 40320 vertex permutations, of the
28-bit edge mask.  Exact, no heuristics, computed by a batched matrix product.
Class lists are built by DELETION BFS from K_8 (every class with k edges is
obtained from some class with k+1 edges by deleting one edge).
"""

from __future__ import annotations

from itertools import permutations

import numpy as np

import w18_core as C

PERMS = list(permutations(range(C.N)))                       # 40320
PERM_EDGE = np.zeros((len(PERMS), C.NE), dtype=np.int64)
for _p, _perm in enumerate(PERMS):
    for _e, (_u, _v) in enumerate(C.EDGES):
        _a, _b = _perm[_u], _perm[_v]
        PERM_EDGE[_p, _e] = C.EIDX[(min(_a, _b), max(_a, _b))]

_POW2 = (1 << np.arange(C.NE, dtype=np.int64)).astype(np.float64)
# W[p, f] = 2^e where PERM_EDGE[p, e] == f;  bits @ W.T gives the image masks.
_W = np.zeros((len(PERMS), C.NE), dtype=np.float64)
_rows = np.repeat(np.arange(len(PERMS)), C.NE)
_W[_rows, PERM_EDGE.ravel()] = np.tile(_POW2, len(PERMS))
_WT = np.ascontiguousarray(_W.T)                             # (28, 40320)


def canon_batch(masks, chunk=256):
    """Canonical (minimum-image) 28-bit mask for each mask in `masks`."""
    out = []
    masks = list(masks)
    for s in range(0, len(masks), chunk):
        blk = masks[s:s + chunk]
        bits = np.zeros((len(blk), C.NE), dtype=np.float64)
        for r, mask in enumerate(blk):
            for e in range(C.NE):
                if (mask >> e) & 1:
                    bits[r, e] = 1.0
        img = bits @ _WT                                     # (B, 40320)
        out.extend(int(x) for x in img.min(axis=1))
    return out


def edges_of(mask):
    return [e for e in range(C.NE) if (mask >> e) & 1]


def degrees(mask):
    deg = [0] * C.N
    for e in edges_of(mask):
        u, v = C.EDGES[e]
        deg[u] += 1
        deg[v] += 1
    return deg


def has_perfect_matching(mask):
    for M in C.PM_EIDX:
        if all((mask >> e) & 1 for e in M):
            return True
    return False


def classes_by_deletion(mmin):
    """{m: [canonical masks]} for m from 28 down to mmin."""
    full = (1 << C.NE) - 1
    level = {full}
    out = {C.NE: sorted(level)}
    m = C.NE
    while m > mmin:
        nxt = set()
        cand = []
        for mask in level:
            for e in edges_of(mask):
                cand.append(mask & ~(1 << e))
        for c in canon_batch(sorted(set(cand))):
            nxt.add(c)
        m -= 1
        level = nxt
        out[m] = sorted(level)
    return out


def admissible_classes(mask_list):
    """Keep only classes that can carry an (SC)-admissible template."""
    keep = []
    for mask in mask_list:
        if min(degrees(mask)) < 3:
            continue
        if not has_perfect_matching(mask):
            continue
        keep.append(mask)
    return keep


def automorphisms(mask):
    """Vertex permutations fixing the graph (as tuples)."""
    bits = np.zeros(C.NE, dtype=np.float64)
    for e in edges_of(mask):
        bits[e] = 1.0
    img = bits @ _WT
    return [PERMS[p] for p in np.nonzero(img == float(mask))[0]]

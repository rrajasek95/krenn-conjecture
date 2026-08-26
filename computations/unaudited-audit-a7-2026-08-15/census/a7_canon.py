"""A7: own graph canonicaliser = min over all 8! = 40320 vertex permutations
of the 28-bit edge mask.  Brute force on purpose (no refinement heuristics),
so that correctness is self-evident.
"""

import itertools

import numpy as np

import a7_core as C

PERMS = list(itertools.permutations(range(8)))
assert len(PERMS) == 40320

# PERM_EDGE[p, e] = index of the image of edge e under permutation p
PERM_EDGE = np.zeros((len(PERMS), 28), dtype=np.int64)
for _pi, _p in enumerate(PERMS):
    for _e, (_u, _v) in enumerate(C.EDGES):
        PERM_EDGE[_pi, _e] = C.edge_index(_p[_u], _p[_v])

POW = (np.int64(1) << PERM_EDGE)              # (40320, 28) int64


def mask_of(edge_idx):
    m = 0
    for e in edge_idx:
        m |= 1 << e
    return m


def edges_of(mask):
    return [e for e in range(28) if (mask >> e) & 1]


def orbit_masks(mask):
    """All 40320 images of the edge-mask under vertex permutations."""
    bits = edges_of(mask)
    if not bits:
        return np.zeros(len(PERMS), dtype=np.int64)
    return np.bitwise_or.reduce(POW[:, bits], axis=1)


def canon(mask):
    return int(orbit_masks(mask).min())


def canon_and_auts(mask):
    om = orbit_masks(mask)
    return int(om.min()), np.nonzero(om == mask)[0]


def edge_orbits(mask):
    """Orbits of the 28 edge slots under Aut(G).  Returns list of lists."""
    _, auts = canon_and_auts(mask)
    parent = list(range(28))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    for p in auts:
        row = PERM_EDGE[p]
        for e in range(28):
            union(e, int(row[e]))
    groups = {}
    for e in range(28):
        groups.setdefault(find(e), []).append(e)
    return list(groups.values()), auts


def canon_weak(mask, k):
    """MUTATION CONTROL: canonicalise using only the first k permutations."""
    bits = edges_of(mask)
    if not bits:
        return 0
    return int(np.bitwise_or.reduce(POW[:k, bits], axis=1).min())

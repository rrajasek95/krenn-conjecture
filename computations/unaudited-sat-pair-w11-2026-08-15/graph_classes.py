"""UNAUDITED (W11).  Isomorphism classes of support graphs on 8 vertices.

The whole decision problem is equivariant for the S_8 x S_3 action (relabel
vertices / permute colours), so the answer for a support graph G equals the
answer for any graph isomorphic to G.  `transport_check` in symmetry_check.py
verifies that equivariance experimentally before it is relied on.

Canonical form = minimum, over all 8! = 40320 vertex permutations, of the
28-bit edge-incidence mask.  Exact, no heuristics.

Enumeration is by edge-addition BFS from the empty graph: every class with
k+1 edges arises from some class with k edges by adding one edge, so trying
all 28 additions from every representative is complete.
"""

from itertools import permutations

import numpy as np

import krenn_core as K

PERMS = list(permutations(range(8)))              # 40320
# PERM_EDGE[p][e] = index of the image of edge e under permutation p
PERM_EDGE = np.zeros((len(PERMS), K.NE), dtype=np.int64)
for pi, p in enumerate(PERMS):
    for e, (u, v) in enumerate(K.EDGES):
        a, b = p[u], p[v]
        PERM_EDGE[pi, e] = K.EIDX[(min(a, b), max(a, b))]
POW2 = (1 << np.arange(K.NE, dtype=np.int64))

# WEIGHT[p, f] = 2^e for the unique e with PERM_EDGE[p, e] == f, so that
#   sum_f bits[f] * WEIGHT[p, f] = sum_e bits[PERM_EDGE[p, e]] * 2^e
# is exactly the bitmask of the image graph.  float64 is exact below 2^53.
WEIGHT = np.zeros((len(PERMS), K.NE), dtype=np.float64)
_rows = np.repeat(np.arange(len(PERMS)), K.NE)
WEIGHT[_rows, PERM_EDGE.ravel()] = np.tile(POW2, len(PERMS)).astype(np.float64)
WEIGHT_T = np.ascontiguousarray(WEIGHT.T)              # (28, 40320)


def canon_batch(masks):
    """masks: (B,) int64 edge bitmasks -> (B,) canonical bitmasks."""
    bits = ((np.asarray(masks, dtype=np.int64)[:, None] >> np.arange(K.NE))
            & 1).astype(np.float64)                    # (B, 28)
    vals = bits @ WEIGHT_T                             # (B, 40320)
    return vals.min(axis=1).astype(np.int64)


def canon(mask):
    return int(canon_batch(np.array([mask]))[0])


def degrees(mask):
    d = [0] * 8
    for e in range(K.NE):
        if (mask >> e) & 1:
            u, v = K.EDGES[e]
            d[u] += 1
            d[v] += 1
    return d


def enumerate_classes(max_edges=28, batch=64, verbose=True):
    """levels[k] = sorted list of canonical masks with exactly k edges."""
    levels = {0: [0]}
    cur = [0]
    for k in range(max_edges):
        cand = []
        for g in cur:
            for e in range(K.NE):
                if not (g >> e) & 1:
                    cand.append(g | (1 << e))
        cand = np.unique(np.array(cand, dtype=np.int64))
        out = set()
        for i in range(0, len(cand), batch):
            out.update(int(x) for x in canon_batch(cand[i:i + batch]))
        cur = sorted(out)
        levels[k + 1] = cur
        if verbose:
            print("  |E|=%2d : %5d classes (%d raw)" % (k + 1, len(cur),
                                                        len(cand)), flush=True)
    return levels


def mindeg3(masks):
    return [g for g in masks if min(degrees(g)) >= 3]


def edges_of(mask):
    return [e for e in range(K.NE) if (mask >> e) & 1]


def perfect_matchings_in(mask):
    return [mi for mi, M in enumerate(K.MATCHINGS)
            if all((mask >> ei) & 1 for ei in M)]


if __name__ == "__main__":
    import json
    import sys
    levels = enumerate_classes()
    total = sum(len(v) for v in levels.values())
    print("total classes over all edge counts:", total, "(expect 12346)")
    md = {k: mindeg3(v) for k, v in levels.items()}
    for k in sorted(md):
        if md[k]:
            print("  |E|=%2d : %5d classes with min degree >= 3" %
                  (k, len(md[k])))
    json.dump({str(k): v for k, v in levels.items()},
              open("graph_classes.json", "w"))
    json.dump({str(k): v for k, v in md.items() if v},
              open("graph_classes_mindeg3.json", "w"))

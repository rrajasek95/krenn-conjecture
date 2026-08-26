#!/usr/bin/env python3
"""UNAUDITED REPAIR PROBE -- item 4 (A, sensitivity) HEAD 7d57c552a3ef.

Which placements of the ONE physically constructed endpoint-odd Cartan
residue packet and the ONE physically placed M_v alpha packet make the
25-row cone reach rank 24 (= ker nu) once each is transported around the
order-6 label group realized by literal source automorphisms?

The repo pins two mutually inconsistent placement conventions:
  scope guard  verify_h3_cut_swap_shared_repair_source_scope_guard.py:186
      cartan_line = (1,0,1,-1,0,-1)
  dichotomy    verify_h3_cut_swap_shared_repair_anchor_fibre_dichotomy.py:190
      ALPHA=(-1,1,1,-1) placed in increasing label order on a 4-subset
The answer to item 4 depends on which is right, so we sweep all placements.
"""
from __future__ import annotations

import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

HEAD = "7d57c552a3ef57d3a95c3bc933af547ad55e087d"
N, ROWS = 6, 25
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))
LABEL_GROUP = ((0, 1, 2, 3, 4, 5), (0, 2, 1, 3, 5, 4), (4, 2, 3, 1, 5, 0),
               (4, 3, 2, 1, 0, 5), (5, 1, 3, 2, 4, 0), (5, 3, 1, 2, 0, 4))


def vec(lower=None, ainc=0, w=None, target=None, ores=None):
    a = [Q(0)] * ROWS
    for off, val in ((0, lower), (7, w), (13, target), (19, ores)):
        if val:
            for i, x in enumerate(val):
                a[off + i] += Q(x)
    a[6] += Q(ainc)
    return tuple(a)


def e(i):
    return tuple(Q(int(j == i)) for j in range(N))


def perm(v, p):
    out = [Q(0)] * N
    for i, x in enumerate(v):
        out[p[i]] += x
    return tuple(out)


def rank2(cols):
    m = len(cols)
    rows = [[cols[j][i] for j in range(m)] for i in range(ROWS)]
    r = 0
    for c in range(m):
        p = next((i for i in range(r, ROWS) if rows[i][c]), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        v = rows[r][c]
        rows[r] = [t / v for t in rows[r]]
        for i in range(ROWS):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == ROWS:
            break
    return r


core = ([vec(lower=e(i), ainc=-1, target=e(i)) for i in range(N)]
        + [vec(w=tuple(-t for t in e(i)), target=e(i)) for i in range(N)]
        + [vec(w=e(i), ores=e(i)) for i in range(N)]
        + [vec(ores=(Q(1),) * N)])

# every sign-and-order placement of the 4-vector (-1,1,1,-1) on 4 of 6 labels
placements = []
for sel in combinations(range(N), 4):
    al = [Q(0)] * N
    for a, i in zip(ALPHA, sel):
        al[i] += a
    placements.append((f"ALPHA@{sel}", tuple(al)))
    al2 = [Q(0)] * N
    for a, i in zip((Q(1), Q(1), Q(-1), Q(-1)), sel):
        al2[i] += a
    placements.append((f"(+,+,-,-)@{sel}", tuple(al2)))

results = {}
for mn, mvec in placements:
    for cn, cvec in placements:
        cols = (core
                + [vec(lower=v) for v in {perm(mvec, p) for p in LABEL_GROUP}]
                + [vec(ores=v) for v in {perm(cvec, p) for p in LABEL_GROUP}])
        results[(mn, cn)] = rank2(cols)

by_rank = {}
for k, v in results.items():
    by_rank.setdefault(v, 0)
    by_rank[v] += 1

# the two pinned conventions
SG = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
sg_name = next(n for n, v in placements if v == SG)
dich = placements[0]

def rank_for(mvec, cvec):
    return rank2(core
                 + [vec(lower=v) for v in {perm(mvec, p) for p in LABEL_GROUP}]
                 + [vec(ores=v) for v in {perm(cvec, p) for p in LABEL_GROUP}])

# marginal: cartan placement alone (Mv granted at all 15)
mv15 = [vec(lower=v) for _, v in placements[:1]]
mv_all = []
for sel in combinations(range(N), 4):
    al = [Q(0)] * N
    for a, i in zip(ALPHA, sel):
        al[i] += a
    mv_all.append(vec(lower=tuple(al)))

cartan_only = {}
for cn, cvec in placements:
    orbit = {perm(cvec, p) for p in LABEL_GROUP}
    cartan_only[cn] = {
        "orbit_size": len(orbit),
        "ores_block_rank_with_aggregate": rank2(
            [vec(ores=(Q(1),) * N)] + [vec(ores=v) for v in orbit]),
        "cone_rank_with_all_15_Mv": rank2(
            core + mv_all + [vec(ores=v) for v in orbit]),
        "cone_rank_with_Mv_orbit_same_placement": rank_for(cvec, cvec),
    }

report = {
    "head": HEAD,
    "label_group_order": len(LABEL_GROUP),
    "placements_swept": len(placements),
    "pairs_swept": len(results),
    "rank_histogram_over_(Mv_placement, Cartan_placement)": {
        str(k): v for k, v in sorted(by_rank.items())},
    "pairs_reaching_rank_24": sum(1 for v in results.values() if v == 24),
    "fraction_reaching_rank_24":
        f"{sum(1 for v in results.values() if v == 24)}/{len(results)}",
    "scope_guard_cartan_placement_name": sg_name,
    "rank_scope_guard_cartan_x_dichotomy_Mv": rank_for(dich[1], SG),
    "rank_dichotomy_cartan_x_dichotomy_Mv": rank_for(dich[1], dich[1]),
    "per_cartan_placement": cartan_only,
}
print(json.dumps(report, indent=2))
Path(__file__).with_name("out_a5.json").write_text(json.dumps(report, indent=2))

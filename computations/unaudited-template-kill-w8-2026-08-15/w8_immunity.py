#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- explicit FIE-admissible templates that NO monomial
/ lattice certificate can kill (the upper obstruction to the template-kill
programme).

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

PROPOSITION (immunity).  Let T be a template with
   (i)  every constant fibre nonempty, and
   (ii) every mixed fibre of size != 1 and != 2.
Then w8_core.analyse(T) returns "survivor", in cell coordinates and in the
strictly stronger rank-one coordinates alike.

Proof.  K0 passes by (i) and O2 by (ii).  The binomial list is empty, so the
character lattice L is 0: value(d) is None for every d != 0.  Distinct
matchings use distinct edges, hence distinct exponent vectors, so no two
terms of a fibre merge: every class has coefficient 1.  A mixed fibre then
has |fibre| >= 3 live classes, so neither the one-live-class kill nor the
two-live-class propagation fires and no relation is ever created; a constant
fibre has all classes live with coefficient 1, so its class sum is |fibre|
!= 0 and K3 does not fire.  Hence "survivor".  []

CONSTRUCTION.  12 single-cell edges on a 3-regular graph, cells chosen so
that the 24 forced-incidence demands are served exactly once each, PLUS
f >= 8 nine-cell ("full") edges carrying a subgraph with at least three
perfect matchings.  Every word is then compatible with at least three
matchings, so (i) and (ii) hold.  The template is FIE-admissible, meets the
J.1d floor beta >= 3N - m with equality-or-better, and exists for every
support m = 20, ..., 28.

The script also certifies the sharp counting fact behind "m >= 20": a
matching compatible with EVERY word must consist of nine-cell blocks, three
such matchings need >= 8 nine-cell blocks, and FIE forces
    2*beta + h >= 24,  beta + h + fat = m   =>   fat <= m - 12.

Run: python3 w8_immunity.py
"""

from __future__ import annotations

import json
import sys
from itertools import combinations

import w8_core as C
from w8_symmetry import canonical_fast


CUBE = [(0, 4), (1, 5), (2, 6), (3, 7), (0, 5), (1, 6), (2, 7), (3, 4),
        (0, 6), (1, 7), (2, 4), (3, 5)]


def fie_single_cells(geo, edges):
    """Assign one cell per edge so that all 24 demands are served exactly once.

    Demand (p,r) is served by pj when the cell's colour at the FAR end j is r.
    Each vertex's three incident edges get far-colours 0,1,2; the constraints
    at different vertices touch disjoint incidence variables, so any bijection
    works.
    """
    far = {}
    for p in range(geo.size):
        incident = sorted(e for e in edges if p in e)
        assert len(incident) == 3, "not 3-regular"
        for r, e in enumerate(incident):
            j = e[0] if e[1] == p else e[1]
            far[(p, j)] = r
    template = [0] * len(geo.edges)
    for u, v in edges:
        i = far[(v, u)]        # colour at u, demanded by v
        j = far[(u, v)]        # colour at v, demanded by u
        template[geo.index[(u, v)]] = 1 << (3 * i + j)
    return template


def add_full(geo, template, edges):
    for u, v in edges:
        e = geo.index[tuple(sorted((u, v)))]
        assert template[e] == 0, "overlapping construction"
        template[e] = C.FULL
    return template


def perfect_matchings_of(geo, edges):
    edgeset = {geo.index[tuple(sorted(e))] for e in edges}
    return [n for n, m in enumerate(geo.matching_edges)
            if all(e in edgeset for e in m)]


def main():
    geo = C.geometry(8)
    results = []

    # the two 4-cycles are edge-disjoint from the cube graph CUBE
    base_full = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4)]
    extra_pool = [e for e in (tuple(sorted(x)) for x in combinations(range(8), 2))
                  if e not in {tuple(sorted(x)) for x in CUBE + base_full}]

    for m in range(20, 29):
        template = fie_single_cells(geo, CUBE)
        template = add_full(geo, template, base_full)
        for e in extra_pool[:m - 20]:
            template[geo.index[e]] = C.FULL
        template = tuple(template)
        compat = C.compat_matrix(geo, template)
        audit = C.audit(geo, template, compat)
        universal = perfect_matchings_of(geo, base_full)
        cell, rank1 = C.analyse_best(geo, template, compat=compat)
        row = {"m": m, "audit": audit,
               "universal_matchings": len(universal),
               "min_mixed_fibre": min(audit["fibre_histogram"]),
               "verdict_cell": cell["verdict"],
               "verdict_rank1": None if rank1 is None else rank1["verdict"],
               "template": list(template)}
        results.append(row)
        print(f"  m={m:2d}  Sigma={audit['sigma']:3d}  beta={audit['beta']:2d} "
              f"thin={audit['thin']} fat={audit['fat']:2d}  FIE={audit['fie']} "
              f"const={audit['constants']}  singletons="
              f"{audit['mixed_singletons']}  min fibre={row['min_mixed_fibre']}"
              f"  -> {row['verdict_cell']} / rank1 {row['verdict_rank1']}",
              flush=True)

    # sharpness: the same construction at m = 19 is impossible with >= 3
    # universally compatible matchings (fat <= m - 12 = 7 < 8)
    note = {"fat_bound": "fat <= m - 12 from 2*beta + h >= 24",
            "min_full_blocks_for_3_universal_matchings": 8,
            "hence_min_m_for_this_construction": 20}

    print("\nsanity: three perfect matchings inside a graph need >= 8 edges "
          "when the graph is a union of two 4-cycles (4 matchings) or K_4 plus"
          " a matching (3 matchings); 7 edges give at most 2.")
    counts = {}
    for size in (6, 7, 8):
        best = 0
        for edges in combinations(range(len(geo.edges)), size):
            edgeset = set(edges)
            k = sum(1 for m in geo.matching_edges
                    if all(e in edgeset for e in m))
            best = max(best, k)
        counts[size] = best
        print(f"  max #perfect matchings inside {size} edges of K_8: {best}")
    note["max_matchings_by_edge_count"] = counts

    canon = {}
    for row in results:
        canon[row["m"]] = str(canonical_fast(geo, tuple(row["template"])))[:60]

    json.dump({"results": results, "note": note}, open("results_immunity.json",
                                                       "w"), indent=1)
    print("wrote results_immunity.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

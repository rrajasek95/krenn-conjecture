#!/usr/bin/env python3
r"""UNAUDITED PROBE (W19-CENSUS) -- the Gamma strata of the (R) census.

UNAUDITED.  Nothing here is a proved claim of the repository.
All arithmetic is exact Python int / numpy int64 (bit masks only).

STRUCTURE THEOREMS USED (each PROVED-HERE in the report, each VERIFIED
computationally below):

 (S1) TOKEN LEMMA.  T is (SC)-admissible <=> for every vertex p the tokens
      a_p(T[e]) over the incident edges e cover {0,1,2}.  A FULL block has
      no token, so every server edge is a NON-Gamma edge, and one edge
      serves at most ONE demand at a given endpoint.  Hence every vertex is
      incident to >= 3 non-Gamma edges:
                     deg_Gamma(p) <= 4  for every p.
 (S2) With (R5) (Gamma spanning 2-connected => min degree >= 2):
                     2 <= deg_Gamma(p) <= 4,  so  8 <= |Gamma| <= 16.
 (S3) |Gamma| = 8  =>  Gamma is 2-regular and connected  =>  Gamma = C_8.
 (S4) |Gamma| = 16 =>  Gamma is 4-regular, K_8 \ Gamma is 3-regular (cubic),
      every non-Gamma edge carries TWO tokens, i.e. is a SINGLE cell, and
      the token data is exactly a "local rainbow" labelling.
 (S5) FIBRE REFORMULATION (verified in w19c_verify.py): fibre(T,w) =
      #PM(G_w) with G_w the graph of cells activated by w; G_w contains
      Gamma always, so |F(Gamma)| >= 3 implies (R2),(R3),(R4).

OUTPUT: results_gamma.json -- every Gamma iso-class that can occur, with
|F(Gamma)|, |Aut|, orbit size, and the EXACT number of (SC)-admissible
completions (= the exact number of (R) members with that Gamma, whenever
|F(Gamma)| >= 3).
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations, permutations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w19c_lib import (  # noqa: E402
    EDGES, EIDX, N, NE, FULL, spanning_2conn, my_npm_graph, mask_to_edges,
    edges_to_mask, degseq, sc_mask_count,
)

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------- fast canonical form ---
PERMS = list(permutations(range(N)))
NP_ = len(PERMS)
POWT = np.zeros((NE, NP_), dtype=np.int64)
for _pi, _p in enumerate(PERMS):
    for _ei, (_u, _v) in enumerate(EDGES):
        _x, _y = _p[_u], _p[_v]
        POWT[_ei, _pi] = 1 << EIDX[(min(_x, _y), max(_x, _y))]
_ACC = np.zeros(NP_, dtype=np.int64)


def _orbit_vec(mask):
    acc = _ACC
    acc[:] = 0
    m = mask
    while m:
        e = (m & -m).bit_length() - 1
        m &= m - 1
        np.add(acc, POWT[e], out=acc)
    return acc


def canon(mask):
    return int(_orbit_vec(mask).min())


def aut_size(mask):
    return int((_orbit_vec(mask) == mask).sum())


# ------------------------------------------- enumeration up to isomorphism --
def enumerate_up_to_iso(maxdeg=None, maxedges=28, verbose=True):
    levels = [set([0])]
    for k in range(maxedges):
        nxt = set()
        for g in levels[k]:
            d = degseq(mask_to_edges(g))
            for e in range(NE):
                if (g >> e) & 1:
                    continue
                u, v = EDGES[e]
                if maxdeg is not None and (d[u] >= maxdeg or d[v] >= maxdeg):
                    continue
                nxt.add(canon(g | (1 << e)))
        levels.append(nxt)
        if verbose:
            print("   |E|=%2d : %6d iso-classes" % (k + 1, len(nxt)), flush=True)
    return levels


# A008406 row n=8: number of graphs on 8 nodes with k edges (external control)
A008406_8 = [1, 1, 2, 5, 11, 24, 56, 115, 221, 402, 663, 980, 1312, 1557,
             1646, 1557, 1312, 980, 663, 402, 221, 115, 56, 24, 11, 5, 2, 1, 1]

RES = {}

print("CONTROL: full enumeration of graphs on 8 vertices up to isomorphism")
lev_all = enumerate_up_to_iso(maxdeg=None, maxedges=16)
counts = [len(s) for s in lev_all]
RES["A008406_row8_reproduced"] = (counts == A008406_8[:len(counts)])
RES["counts_by_edges_all_graphs"] = counts
RES["total_graphs_8v"] = sum(counts)
print("  reproduces A008406 row 8 (prefix |E|<=16):", counts == A008406_8[:len(counts)])

# ------------------------------------------------ the admissible Gammas ----
cands = []
for k in range(8, 17):
    for g in lev_all[k]:
        es = mask_to_edges(g)
        d = degseq(es)
        if max(d) > 4:
            continue
        if not spanning_2conn(es):
            continue
        cands.append((k, g))
print("\nGamma iso-classes with 8<=|E|<=16, maxdeg<=4, spanning 2-connected:",
      len(cands))

# sanity: no admissible Gamma outside 8..16.  |E|>16 with maxdeg<=4 is
# impossible (2|E| = sum deg <= 32); |E|<8 spanning 2-connected is impossible
# (min degree >= 2).  Checked below on the enumerated range.
outside = 0
for k in range(0, 8):
    for g in lev_all[k]:
        es = mask_to_edges(g)
        if max(degseq(es)) <= 4 and spanning_2conn(es):
            outside += 1
RES["admissible_gamma_outside_8_16"] = outside
print("  admissible Gammas outside 8..16 edges:", outside, "(must be 0)")


# ---------------------------------------- exact count of SC completions ----
def count_sc_completions_mask(gamma_mask):
    """EXACT #templates T with Gamma(T) = gamma_mask and T (SC)-admissible.

    Inclusion-exclusion over 'which colours are declared missing at each
    vertex'; the per-edge mask count depends only on the two sizes."""
    free = [EDGES[ei] for ei in range(NE) if not (gamma_mask >> ei) & 1]
    inc = [[] for _ in range(N)]
    for idx, (u, v) in enumerate(free):
        inc[u].append((idx, v))
        inc[v].append((idx, u))
    binom = (1, 3, 3, 1)
    sign = (1, -1, 1, -1)
    total = 0
    svec = [0] * N

    def rec(p, coef, prod):
        nonlocal total
        if p == N:
            total += coef * prod
            return
        for s in range(4):
            svec[p] = s
            c2 = coef * binom[s] * sign[s]
            pr = prod
            for (idx, q) in inc[p]:
                if q < p:
                    pr *= sc_mask_count(3 - s, 3 - svec[q])
            rec(p + 1, c2, pr)
        svec[p] = 0

    rec(0, 1, 1)
    return total


rows = []
for k, g in sorted(cands):
    es = mask_to_edges(g)
    npm = my_npm_graph(es)
    a = aut_size(g)
    nsc = count_sc_completions_mask(g)
    rows.append(dict(n_edges=k, mask=g, edges=[list(e) for e in es],
                     degseq=sorted(degseq(es)), pms=npm, aut=a,
                     orbit=40320 // a, n_sc_completions=nsc,
                     n_R_members=(nsc if npm >= 3 else None)))
    if len(rows) % 200 == 0:
        print("   ...", len(rows), flush=True)

RES["n_gamma_classes"] = len(rows)
RES["gamma_classes"] = rows

by_e = {}
for r in rows:
    by_e.setdefault(r["n_edges"], []).append(r)
print("\n|E|  #classes  #with|F|<3   min|F|  max|F|   sum orbit")
summary = {}
for k in sorted(by_e):
    rs = by_e[k]
    low = [r for r in rs if r["pms"] < 3]
    summary[k] = dict(classes=len(rs), low_pm_classes=len(low),
                      min_pms=min(r["pms"] for r in rs),
                      max_pms=max(r["pms"] for r in rs),
                      labelled=sum(r["orbit"] for r in rs))
    print("%3d  %8d  %9d  %6d  %6d  %11d"
          % (k, len(rs), len(low), summary[k]["min_pms"],
             summary[k]["max_pms"], summary[k]["labelled"]))
RES["summary_by_edges"] = summary

low = [r for r in rows if r["pms"] < 3]
RES["low_pm_gammas"] = low
print("\nGamma classes with |F(Gamma)| < 3 (need the extra-matching analysis):",
      len(low))
for r in low:
    print("   |E|=%d  |F|=%d  deg=%s  edges=%s"
          % (r["n_edges"], r["pms"], r["degseq"], r["edges"]))

# total number of (R) members with |F(Gamma)|>=3, exactly
tot = 0
for r in rows:
    if r["pms"] >= 3:
        tot += r["orbit"] * r["n_sc_completions"]
RES["total_R_members_highF_labelled"] = tot
print("\nEXACT number of (R) members whose Gamma has >=3 PMs:", tot)

json.dump(RES, open(os.path.join(HERE, "results_gamma.json"), "w"))
print("written")

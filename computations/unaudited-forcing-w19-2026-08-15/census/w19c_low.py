#!/usr/bin/env python3
r"""UNAUDITED PROBE (W19-CENSUS) -- the low-|F(Gamma)| strata, esp. |Gamma|=8.

UNAUDITED.  Nothing here is a proved claim of the repository.
Exact integer arithmetic only.

THE MONOTONE REDUCTION (PROVED-HERE, used everywhere below).  Let T be in
(R) with Gamma(T) = Gamma.  Pick, at each vertex p, three incident edges
carrying three distinct tokens (possible by (SC)).  Enlarge every non-Gamma
block to the LARGEST mask compatible with its selected token(s):
    two selected tokens  -> the single cell itself      (1 mask)
    one selected token   -> the full column / full row  (1 mask)
    no selected token    -> any 8-cell mask             (9 masks)
Every enlargement keeps (SC) (the selected tokens survive), keeps
Gamma (no mask reaches 511) and can only increase fibres.  Hence

    (R) has a member with this Gamma  <=>  a MAXIMAL configuration does.

THE DOWNGRADE CONSTRUCTION (this file's engine).  Start from a |Gamma|=16
member (Gamma_16 = complement of a cubic graph C, 12 singles on C).  Choose
a spanning 2-connected subgraph H of Gamma_16 and knock ONE cell out of each
block of D = Gamma_16 \ H.  The result has Gamma = H, phi = |D| fat blocks,
and is in (R) iff every mixed fibre is still >= 3.  With H a Hamilton cycle
this lands exactly in the |Gamma| = 8 stratum.
"""
from __future__ import annotations

import json
import os
import random
import sys
from itertools import combinations, permutations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w19c_lib import (  # noqa: E402
    EDGES, EIDX, N, NE, FULL, WORDS, MIXED_POS, CONST_POS,
    in_R, sc_ok, spanning_2conn, my_npm_graph, my_sc_ok, fast_in_R,
    fibres_all_words, fast_audit, mask_to_edges, edges_to_mask, degseq,
    pms_inside, block_class,
)
from w19c_verify import (  # noqa: E402
    CUBE, build_cubic_template, diag_sigma, proper_colouring, random_sigma,
    incidences,
)

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(31337)
RES = {}


# ------------------------------------------------------------ cubic graphs --
def cubic_graphs_labelled():
    """all 3-regular graphs on 8 LABELLED vertices."""
    out = []
    alle = list(EDGES)

    def rec(i, deg, chosen):
        if len(chosen) == 12:
            if all(d == 3 for d in deg):
                out.append(list(chosen))
            return
        if i == len(alle):
            return
        # prune
        if sum(3 - d for d in deg) > 2 * (len(alle) - i):
            return
        u, v = alle[i]
        if deg[u] < 3 and deg[v] < 3:
            deg[u] += 1
            deg[v] += 1
            chosen.append((u, v))
            rec(i + 1, deg, chosen)
            chosen.pop()
            deg[u] -= 1
            deg[v] -= 1
        rec(i + 1, deg, chosen)

    rec(0, [0] * N, [])
    return out


def hamilton_cycles(edges):
    """all Hamilton cycles (as edge sets) of the graph, up to direction."""
    adj = {v: set() for v in range(N)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    out = set()
    path = [0]
    seen = {0}

    def rec():
        if len(path) == N:
            if path[0] in adj[path[-1]]:
                es = frozenset(
                    (min(path[i], path[(i + 1) % N]), max(path[i], path[(i + 1) % N]))
                    for i in range(N))
                out.add(es)
            return
        for b in adj[path[-1]]:
            if b in seen:
                continue
            seen.add(b)
            path.append(b)
            rec()
            path.pop()
            seen.discard(b)

    rec()
    return [sorted(e) for e in out]


# --------------------------------------------------- the downgrade search --
def downgrade(T16, D, dead):
    """knock cell dead[k] out of block D[k] (which must be FULL in T16)."""
    T = list(T16)
    for k, e in enumerate(D):
        ei = EIDX[e]
        assert T[ei] == FULL
        T[ei] = FULL ^ (1 << dead[k])
    return T


def n_bad(T):
    f = fibres_all_words(T)
    return int((f[MIXED_POS] < 3).sum()) + int((f[CONST_POS] < 1).sum())


def search_dead(T16, D, tries=4000, restarts=40):
    """hill-climb on the dead-cell choice; returns (best_bad, dead)."""
    best = None
    for _ in range(restarts):
        dead = [rng.randrange(9) for _ in D]
        cur = n_bad(downgrade(T16, D, dead))
        if best is None or cur < best[0]:
            best = (cur, list(dead))
        if cur == 0:
            return best
        for _ in range(tries):
            k = rng.randrange(len(D))
            old = dead[k]
            new = rng.randrange(9)
            if new == old:
                continue
            dead[k] = new
            v = n_bad(downgrade(T16, D, dead))
            if v <= cur:
                cur = v
                if v < best[0]:
                    best = (v, list(dead))
                if v == 0:
                    return best
            else:
                dead[k] = old
    return best


print("=== stratum (i): |Gamma| = 8 (Gamma = C_8) ===", flush=True)

# --- PROOF STEP: a spanning 2-connected graph on 8 vertices with 8 edges is
# exactly a Hamilton cycle.  Verified exhaustively over all 8-edge graphs.
allC8 = []
n8 = 0
for es in combinations(EDGES, 8):
    d = degseq(es)
    if min(d) < 2:
        continue
    n8 += 1
    if spanning_2conn(list(es)):
        allC8.append(es)
ham_ok = all(sorted(degseq(es)) == [2] * 8 for es in allC8)
# and each such graph is connected 2-regular = a single 8-cycle
RES["S3_8edge_spanning2conn_are_2regular"] = ham_ok
RES["S3_n_8edge_spanning2conn_labelled"] = len(allC8)
print("8-edge spanning 2-connected graphs: %d, all 2-regular: %s  (7!/2 = %d)"
      % (len(allC8), ham_ok, 5040 // 2 * 1))

# ---- the engine: try every cubic skeleton x Hamilton cycle of its complement
cub = cubic_graphs_labelled()
print("labelled cubic graphs on 8 vertices:", len(cub), "(known 19355)", flush=True)
RES["n_labelled_cubic"] = len(cub)

found = []
tested = 0
# canonical representatives of the 6 cubic iso-classes
from w19c_lib import canon_mask as canon, aut_size_mask as aut_size  # noqa: E402
reps = {}
for C in cub:
    k = canon(edges_to_mask(C))
    if k not in reps:
        reps[k] = C
print("cubic iso-classes:", len(reps), flush=True)
RES["n_cubic_iso_classes"] = len(reps)

for k, C in reps.items():
    Cs = set((min(u, v), max(u, v)) for (u, v) in C)
    G16 = [e for e in EDGES if e not in Cs]
    hams = hamilton_cycles(G16)
    chi = proper_colouring(C)
    sigmas = []
    if chi is not None:
        sigmas.append(("diag", diag_sigma(C, chi)))
    for t in range(3):
        sigmas.append(("rand%d" % t, random_sigma(C, rng)))
    print("\ncubic class mask=%d: |Ham(G16)|=%d  3-edge-colourable=%s"
          % (k, len(hams), chi is not None), flush=True)
    for snm, sig in sigmas:
        T16 = build_cubic_template(C, sig)
        if not fast_in_R(T16):
            print("   %s: base |Gamma|=16 template NOT in (R)?!" % snm)
            continue
        for H in hams[:6]:
            D = [e for e in G16 if tuple(e) not in set(map(tuple, H))]
            assert len(D) == 8 and len(H) == 8
            tested += 1
            bb, dead = search_dead(T16, [tuple(e) for e in D])
            print("   %-6s H=%s  best #bad words = %d"
                  % (snm, [list(e) for e in H][:3], bb), flush=True)
            if bb == 0:
                T = downgrade(T16, [tuple(e) for e in D], dead)
                assert in_R(T), "explicit w19_core.in_R check failed"
                found.append(dict(cubic=[list(e) for e in C], sigma=snm,
                                  H=[list(e) for e in H],
                                  D=[list(e) for e in D], dead=dead,
                                  template=[int(x) for x in T],
                                  audit=fast_audit(T)))
                break
        if found:
            break
    if found:
        break

RES["stratum_i_members"] = found
RES["stratum_i_nonempty"] = bool(found)
print("\n|Gamma|=8 members found:", len(found), flush=True)
if found:
    print("TEMPLATE:", found[0]["template"])
    print("AUDIT:", {k: v for k, v in found[0]["audit"].items() if k != "gamma"})

json.dump(RES, open(os.path.join(HERE, "results_low.json"), "w"), indent=1)

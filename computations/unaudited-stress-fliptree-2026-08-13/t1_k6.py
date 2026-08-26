#!/usr/bin/env python3
"""T1 -- K_6 flip graph, spanning tree, and the contraction identity.

Tests, in order:
  1a  build the 2-switch flip graph on the 15 perfect matchings of K_6;
      report connectivity, degree profile, edge count, cycle rank.
  1b  BFS spanning tree T rooted at the lex-min matching.
  1c  the ELEMENTARY chain complex  C_1 --d--> C_0  with
      d(e_{M->N}) = [N] - [M]   (the additive shadow of the Laurent binomial
      m_chi(N)/m_chi(M)), H_T([M]) = signed sum of tree edges root->M.
      Check  d H_T = 1 - P_root  on C_0  (exact) and, crucially, what
      H_T d  equals on C_1 -- i.e. what the "projection" really is.
  1d  the PROVENANCE-CARRYING (multiplicative) version: every H_T matrix
      entry is the product of the edge Laurent ratios along the tree path.
      Check that this product is PATH-INDEPENDENT (telescoping) and equals
      m_chi(M)/m_chi(root).
  1e  fill 2-cells (all triangles + squares of the flip graph) and recompute
      H_1: does the flip 2-complex contract to a point?

Exact arithmetic throughout.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations
import json

import fliptree_lib as F

out = {"pinned_head": open("PINNED_HEAD.txt").read().strip()}

# ---------------------------------------------------------------- 1a
MATCHINGS = F.all_matchings(6)
out["n_matchings_K6"] = len(MATCHINGS)
adj = F.flip_graph(MATCHINGS, F.two_switch_neighbours)
E = F.undirected_edges(adj)
out["connected"] = F.is_connected(adj)
out["n_edges_2switch"] = len(E)
deg = sorted(Counter(len(v) for v in adj.values()).items())
out["degree_profile"] = [[d, c] for d, c in deg]
out["cycle_rank_b1"] = len(E) - len(MATCHINGS) + 1
# general alternating-cycle exchanges, for reference
adj_all = F.flip_graph(MATCHINGS, F.alternating_cycle_neighbours)
out["n_edges_all_alternating_cycles"] = len(F.undirected_edges(adj_all))
out["all_alt_is_complete_graph"] = (
    len(F.undirected_edges(adj_all)) == len(MATCHINGS) * (len(MATCHINGS) - 1) // 2)

ROOT = min(MATCHINGS)
out["root_lexmin"] = repr(ROOT)

# ---------------------------------------------------------------- 1b
parent, depth, order = F.bfs_tree(adj, ROOT)
TE = F.tree_edges(parent)
out["tree_edges"] = len(TE)
out["tree_spans_all"] = len(parent) == len(MATCHINGS)
out["tree_depth_profile"] = [[d, c] for d, c in
                             sorted(Counter(depth.values()).items())]
out["non_tree_edges"] = len(E) - len(TE)

# ---------------------------------------------------------------- 1c
# orient every edge (A,B) with A < B ; C_1 basis = E, C_0 basis = MATCHINGS
Eidx = {e: i for i, e in enumerate(E)}


def d1(chain1):
    """C_1 -> C_0 ; d(A,B) = [B] - [A]."""
    o = defaultdict(Q)
    for (A, B), c in chain1.items():
        o[B] += c
        o[A] -= c
    return F.clean(o)


def H0(M):
    """C_0 -> C_1 : the oriented tree path root -> M."""
    o = defaultdict(Q)
    v = M
    while parent[v] is not None:
        p = parent[v]
        if p < v:
            o[(p, v)] += Q(1)          # traversed forwards
        else:
            o[(v, p)] -= Q(1)          # traversed backwards
        v = p
    return F.clean(o)


# check  d1 H0 [M] = [M] - [root]  for every M
bad = []
for M in MATCHINGS:
    lhs = d1(H0(M))
    rhs = F.clean({M: Q(1), ROOT: Q(-1)}) if M != ROOT else {}
    if lhs != rhs:
        bad.append(repr(M))
out["degree0_identity_dH_eq_1_minus_Proot"] = (not bad)
out["degree0_identity_failures"] = bad

# what is H0 d1 on C_1?
resid_tree, resid_nontree = [], []
for e in E:
    A, B = e
    lhs = F.sub(H0(B), H0(A))                       # H0 d1 (e)
    r = F.sub({e: Q(1)}, lhs)                       # (1 - H0 d1)(e)
    if e in set(TE):
        resid_tree.append((e, r))
    else:
        resid_nontree.append((e, r))
out["degree1_residual_zero_on_tree_edges"] = all(not r for _e, r in resid_tree)
out["degree1_residual_nonzero_on_all_nontree_edges"] = all(
    r for _e, r in resid_nontree)
resid_span = F.rref([{k: v for k, v in r.items()} for _e, r in resid_nontree])
out["degree1_residual_span_rank"] = len(resid_span)
out["degree1_residual_span_rank_equals_b1"] = (
    len(resid_span) == out["cycle_rank_b1"])
# residuals are cycles: d1 of each residual must vanish
out["degree1_residuals_are_cycles"] = all(
    not d1(r) for _e, r in resid_nontree)

# ---------------------------------------------------------------- 1d
# provenance: multiplicative transport along the tree path, for a word chi
CHI = (0, 0, 1, 1, 2, 2)          # a genuinely mixed 6-site colouring
out["chi"] = list(CHI)


def transport(path_vertices):
    """product of edge Laurent ratios along a vertex path (dict cell->exp)."""
    acc = {}
    for a, b in zip(path_vertices, path_vertices[1:]):
        acc = F.ratio_mul(acc, F.laurent_ratio(a, b, CHI))
    return acc


bad_tel, entries = [], {}
for M in MATCHINGS:
    p = list(reversed(F.path_to_root(parent, M)))    # root -> M
    tr = transport(p)
    direct = F.ratio_mul(
        {c: 1 for c in F.monomial_of(M, CHI)},
        {c: -1 for c in F.monomial_of(ROOT, CHI)})
    direct = {c: k for c, k in direct.items() if k}
    if tr != direct:
        bad_tel.append(repr(M))
    entries[repr(M)] = len(tr)
out["provenance_transport_telescopes_to_m(M)/m(root)"] = (not bad_tel)
out["provenance_failures"] = bad_tel
out["max_transport_support"] = max(entries.values())

# path independence: compare with a DFS tree and with 200 random walks
p2, d2, _o2 = F.dfs_tree(adj, ROOT)
mismatch = []
for M in MATCHINGS:
    a = transport(list(reversed(F.path_to_root(parent, M))))
    b = transport(list(reversed(F.path_to_root(p2, M))))
    if a != b:
        mismatch.append(repr(M))
out["transport_is_tree_independent(exponent_local_system)"] = (not mismatch)
out["transport_tree_mismatches"] = mismatch

# holonomy of every cycle in the exponent local system must be trivial
hol_nontrivial = []
for e in E:
    if e in set(TE):
        continue
    A, B = e
    loop = (list(reversed(F.path_to_root(parent, A)))
            + [B] + F.path_to_root(parent, B)[1:])
    h = transport(loop)
    if h:
        hol_nontrivial.append(repr(e))
out["exponent_holonomy_trivial_on_all_fundamental_cycles"] = (
    not hol_nontrivial)
out["exponent_holonomy_failures"] = hol_nontrivial

# ---------------------------------------------------------------- 1e
# 2-cells: every triangle and every 4-cycle of the flip graph
adjset = {M: set(v) for M, v in adj.items()}
two_cells = []
for A, B in E:
    for Cv in adjset[A] & adjset[B]:
        tri = tuple(sorted((A, B, Cv)))
        two_cells.append(("tri", tri))
two_cells = sorted(set(two_cells))
squares = set()
for A in MATCHINGS:
    for B, D in combinations(sorted(adjset[A]), 2):
        for Cv in (adjset[B] & adjset[D]) - {A}:
            if Cv in adjset[A]:
                continue                      # degenerate (already a triangle)
            squares.add(tuple(sorted((A, B, Cv, D))) + (("sq",) if False else ()))
out["n_triangles"] = len(two_cells)
out["n_chordless_squares"] = len(squares)


def cell_boundary_tri(t):
    A, B, Cv = t
    o = defaultdict(Q)
    for (x, y), s in (((A, B), 1), ((B, Cv), 1), ((A, Cv), -1)):
        e = (x, y) if x < y else (y, x)
        o[e] += Q(s) if x < y else Q(-s)
    return F.clean(o)


bnd2 = [cell_boundary_tri(t) for _k, t in two_cells]
# squares: need the actual 4-cycle order; recover it
sq_bnd = []
for q in squares:
    A, B, Cv, D = q
    # find a cyclic order
    verts = [A, B, Cv, D]
    found = None
    for perm in ((0, 1, 2, 3), (0, 1, 3, 2), (0, 2, 1, 3)):
        cyc = [verts[i] for i in perm]
        if all(cyc[(i + 1) % 4] in adjset[cyc[i]] for i in range(4)):
            found = cyc
            break
    if found is None:
        continue
    o = defaultdict(Q)
    for i in range(4):
        x, y = found[i], found[(i + 1) % 4]
        e = (x, y) if x < y else (y, x)
        o[e] += Q(1) if x < y else Q(-1)
    sq_bnd.append(F.clean(o))

img_tri = F.rref(bnd2)
img_all = F.rref(bnd2 + sq_bnd)
out["rank_d2_triangles_only"] = len(img_tri)
out["rank_d2_triangles_plus_squares"] = len(img_all)
# H_1 = ker d1 / im d2 ; dim ker d1 = b1
out["H1_after_triangles"] = out["cycle_rank_b1"] - len(img_tri)
out["H1_after_triangles_and_squares"] = out["cycle_rank_b1"] - len(img_all)
out["flip_2complex_is_simply_connected(H1=0)"] = (
    out["H1_after_triangles_and_squares"] == 0)

json.dump(out, open("t1_k6.json", "w"), indent=1, sort_keys=True)
for k in sorted(out):
    print(f"{k}: {out[k]}")

#!/usr/bin/env python3
"""T2 -- holonomy as the consistency obstruction, and where it actually lives.

N = 6, palette {0,1,2}.  Two supports:

  S_odd  the committed 3P2 chart of notes/generalized-laurent-elimination.md
         Sec 2: exceptional edges F = {01,23,45} fully supported, the twelve
         RANK-ONE edges with the factor supports of display (6).  Rank-one
         means a_uv = x y^T, which contributes 2x2-minor relations
         a(i,j)a(i',j') = a(i,j')a(i',j)  --  binomials with sign +1.
  S_bip  a support whose CELL graph is bipartite: cells are allowed only
         between colour class {1} and colour class {0,2}, so every cell
         joins the two sides.  Repo criterion: bipartite => no odd handcuff.

Forced relations, exactly:
  * two-term mixed fibre  {A,B}:  m(A) + m(B) = 0  =>  x^lambda = -1,
    lambda = exp(A) - exp(B)                                   [sign -1]
  * rank-one 2x2 minor (S_odd only):        x^mu = +1           [sign +1]

Consistency (= existence of a pairing scheme / sign lift) is the GF(2)
system  Lambda^T s = eps.  Solvable  <=>  no integer dependency
sum n_r lambda_r = 0 with sum over the eps = -1 relations odd.

Tests run:
  (a) S_bip: character consistent?  is the tree-fixed lift the SAME character
      for three different spanning trees of the cell graph?
  (b) S_odd: exhibit an odd dependency (1 = -1) and show the lift fails for
      EVERY tree; localise the failure on the odd loops.
  (c) localisation: how many forced relations does a single colouring fibre
      carry?  (If <= 1, no fibre's flip graph can carry a sign cycle, and the
      obstruction is necessarily CROSS-fibre.)
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
import json

import fliptree_lib as F

out = {"pinned_head": open("PINNED_HEAD.txt").read().strip()}
N = 6
SITES = tuple(range(N))
PALETTE = (0, 1, 2)
MATCHINGS = F.all_matchings(N)

# --------------------------------------------------------------- supports
RANK_ONE = {                      # display (6)
    (0, 2): ((0,), (0,)),
    (0, 3): ((2,), (2,)),
    (0, 4): ((0,), (1,)),
    (0, 5): ((0, 1, 2), (0, 1, 2)),
    (1, 2): ((1,), (0,)),
    (1, 3): ((0, 1, 2), (0, 1, 2)),
    (1, 4): ((2,), (2,)),
    (1, 5): ((1,), (1,)),
    (2, 4): ((0, 1, 2), (0, 1, 2)),
    (2, 5): ((2,), (2,)),
    (3, 4): ((1,), (1,)),
    (3, 5): ((0,), (0,)),
}
EXCEPTIONAL = [(0, 1), (2, 3), (4, 5)]

S_ODD = frozenset(
    [(u, v, i, j) for (u, v) in EXCEPTIONAL
     for i, j in product(PALETTE, repeat=2)]
    + [(u, v, i, j) for (u, v), (L, R) in RANK_ONE.items()
       for i in L for j in R])

# bipartite cell graph: colour 1 on one side, colours {0,2} on the other
S_BIP = frozenset(
    (u, v, i, j) for u, v in combinations(SITES, 2)
    for i, j in product(PALETTE, repeat=2)
    if (i == 1) != (j == 1))


def minor_relations(rank_one_table, support):
    """2x2 minors of each rank-one block: x^mu = +1."""
    rels = []
    for (u, v), (L, R) in rank_one_table.items():
        if len(L) < 2 or len(R) < 2:
            continue
        for i, ip in combinations(L, 2):
            for j, jp in combinations(R, 2):
                mu = {(u, v, i, j): 1, (u, v, ip, jp): 1,
                      (u, v, i, jp): -1, (u, v, ip, j): -1}
                assert all(c in support for c in mu)
                rels.append(("minor", (u, v), mu, +1))
    return rels


# ----------------------------------------------------------------- fibres
def forced_relations(S):
    live = defaultdict(list)
    for chi in product(PALETTE, repeat=N):
        for M in MATCHINGS:
            if all(F.cell(u, v, chi) in S for u, v in M):
                live[chi].append(M)
    rels, stats = [], {}
    sizes = Counter()
    one_term = []
    for chi in sorted(live):
        Ms = sorted(live[chi])
        if len(set(chi)) == 1:
            continue                       # constant fibre: target 1, no relation
        sizes[len(Ms)] += 1
        if len(Ms) == 1:
            one_term.append(chi)
        if len(Ms) == 2:
            A, B = Ms
            lam = F.laurent_ratio(B, A, chi)         # x^lam = -1
            rels.append(("fibre", chi, lam, -1))
    stats["mixed_fibre_size_profile"] = sorted(sizes.items())
    stats["one_term_mixed_fibres"] = len(one_term)
    stats["colourings_with_live_occurrence"] = len(live)
    stats["total_live_occurrences"] = sum(len(v) for v in live.values())
    stats["constant_fibres_live"] = sorted(
        "".join(map(str, c)) for c in live if len(set(c)) == 1)
    return rels, stats, live


# ------------------------------------------------- integer kernel (col HNF)
def integer_kernel(A):
    m, n = len(A), (len(A[0]) if A else 0)
    M = [row[:] for row in A]
    T = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    col_start = 0
    for row in range(m):
        if col_start >= n:
            break
        while True:
            nz = [c for c in range(col_start, n) if M[row][c]]
            if len(nz) <= 1:
                break
            nz.sort(key=lambda c: abs(M[row][c]))
            p = nz[0]
            for c in nz[1:]:
                q = M[row][c] // M[row][p]
                if q:
                    for i in range(m):
                        M[i][c] -= q * M[i][p]
                    for i in range(n):
                        T[i][c] -= q * T[i][p]
        nz = [c for c in range(col_start, n) if M[row][c]]
        if nz:
            p = nz[0]
            if p != col_start:
                for i in range(m):
                    M[i][p], M[i][col_start] = M[i][col_start], M[i][p]
                for i in range(n):
                    T[i][p], T[i][col_start] = T[i][col_start], T[i][p]
            col_start += 1
    ker = []
    for c in range(col_start, n):
        assert all(M[i][c] == 0 for i in range(m)), "column HNF failed"
        ker.append([T[i][c] for i in range(n)])
    for k in ker:
        for i in range(m):
            assert sum(A[i][j] * k[j] for j in range(n)) == 0, "kernel wrong"
    return ker


# ------------------------------------------------------------- GF(2) solve
def gf2_solve(rows, rhs, ncols, forced=None):
    """Solve  R s = rhs  over GF(2).  `forced` is {col: bit} pinned in advance
    (the spanning-tree gauge).  Returns (solvable, solution, free_dim)."""
    R = [set(r) for r in rows]
    b = list(rhs)
    if forced:
        for i in range(len(R)):
            for c, bit in forced.items():
                if c in R[i]:
                    R[i].discard(c)
                    b[i] ^= bit
        # pin the forced columns by explicit equations
        for c, bit in forced.items():
            R.append({c})
            b.append(bit)
    pivots = {}
    for i in range(len(R)):
        while True:
            cand = R[i] & set(pivots)
            if not cand:
                break
            p = min(cand)
            R[i] ^= R[pivots[p]]
            b[i] ^= b[pivots[p]]
        if R[i]:
            pivots[min(R[i])] = i
        elif b[i]:
            return False, None, None
    sol = {}
    for p in sorted(pivots, reverse=True):
        i = pivots[p]
        v = b[i]
        for c in R[i]:
            if c != p:
                v ^= sol.get(c, 0)
        sol[p] = v
    return True, sol, ncols - len(pivots)


# ------------------------------------------------------- cell-graph trees
def cell_graph(S):
    adj = defaultdict(set)
    for (u, v, i, j) in S:
        adj[(u, i)].add((v, j))
        adj[(v, j)].add((u, i))
    return {k: sorted(v) for k, v in adj.items()}


def spanning_tree_cells(S, rule, key):
    """Spanning tree of the cell graph; returns the set of CELLS used."""
    adj = cell_graph(S)
    root = min(adj, key=key)
    fn = {"bfs": F.bfs_tree, "dfs": F.dfs_tree, "dij": F.dijkstra_tree}[rule]
    parent, _d, _o = fn(adj, root, key=key)
    cells = set()
    for x, p in parent.items():
        if p is None:
            continue
        (u, i), (v, j) = x, p
        if u > v:
            (u, i), (v, j) = (v, j), (u, i)
        cells.add((u, v, i, j))
    return cells, len(parent), len(adj)


# --------------------------------------------------------------- per support
def analyse(name, S, use_minors):
    rec = {"support_name": name, "support_cells": len(S)}
    cg = cell_graph(S)
    rec["cell_graph_vertices"] = len(cg)
    # bipartite?
    colour, bip = {}, True
    for s in sorted(cg):
        if s in colour:
            continue
        colour[s] = 0
        stack = [s]
        while stack:
            x = stack.pop()
            for y in cg[x]:
                if y not in colour:
                    colour[y] = 1 - colour[x]
                    stack.append(y)
                elif colour[y] == colour[x]:
                    bip = False
    rec["cell_graph_bipartite"] = bip
    rec["cell_graph_connected"] = F.is_connected(cg)

    rels, stats, live = forced_relations(S)
    rec.update(stats)
    rec["forced_two_term_relations"] = len(rels)
    per_fibre = Counter(r[1] for r in rels)
    rec["max_forced_relations_in_ONE_fibre"] = (
        max(per_fibre.values()) if per_fibre else 0)
    allrels = list(rels)
    if use_minors:
        mrs = minor_relations(RANK_ONE, S)
        rec["rank_one_minor_relations"] = len(mrs)
        allrels += [(k, tag, mu, +1) for (k, tag, mu, sg) in mrs]
    else:
        rec["rank_one_minor_relations"] = 0
    rec["total_relations"] = len(allrels)
    if not allrels:
        rec["verdict"] = "no forced relations"
        return rec

    cells = sorted({c for r in allrels for c in r[2]})
    cidx = {c: k for k, c in enumerate(cells)}
    rec["cells_touched_by_relations"] = len(cells)
    # exponent matrix, rows = cells, cols = relations
    A = [[0] * len(allrels) for _ in cells]
    for r, rel in enumerate(allrels):
        for c, e in rel[2].items():
            A[cidx[c]][r] = e
    rec["lattice_rank_over_Q"] = F.rank(
        [{i: Q(A[i][r]) for i in range(len(cells)) if A[i][r]}
         for r in range(len(allrels))])

    K = integer_kernel(A)
    rec["integer_kernel_dim"] = len(K)
    sigma = [1 if rel[3] == -1 else 0 for rel in allrels]
    odd = [k for k in K if sum(n * s for n, s in zip(k, sigma)) % 2]
    rec["kernel_basis_vectors_with_odd_sign_sum"] = len(odd)
    rec["odd_dependency_exists (O1: 1 = -1)"] = bool(odd)
    if odd:
        best = min(odd, key=lambda k: (sum(1 for x in k if x),
                                       max(map(abs, k))))
        chk = defaultdict(int)
        for r, n in enumerate(best):
            if n:
                for c, e in allrels[r][2].items():
                    chk[c] += n * e
        assert not {c: e for c, e in chk.items() if e}, "dependency not exact"
        used = [r for r, n in enumerate(best) if n]
        sgn = [r for r in used if allrels[r][3] == -1]
        rec["certificate"] = {
            "relations_used": len(used),
            "of_which_sign_minus_one": len(sgn),
            "sign_sum_parity": sum(best[r] for r in sgn) % 2,
            "distinct_colourings_used": len(
                {allrels[r][1] for r in sgn}),
            "colourings": sorted("".join(map(str, allrels[r][1]))
                                 for r in sgn),
            "coefficients_on_signed_relations": [best[r] for r in sgn],
            "verified_exact_dependency": True,
        }

    # ---- pairing-scheme lift = GF(2) system, gauge-fixed by a spanning tree
    rows = [set(c for c, e in rel[2].items() if e % 2) for rel in allrels]
    rows = [{cidx[c] for c in r} for r in rows]
    rhs = sigma
    ok, _sol, freed = gf2_solve(rows, rhs, len(cells))
    rec["lift_exists_ungauged"] = ok
    rec["lift_free_dim_ungauged"] = freed

    tree_results = []
    keys = {"lex": (lambda z: z),
            "revlex": (lambda z: tuple(-t for t in z)),
            "hash": (lambda z: (hash((z, 20260813)) & 0xffff, z))}
    for rule in ("bfs", "dfs", "dij"):
        for kname, key in keys.items():
            tcells, reached, nv = spanning_tree_cells(S, rule, key)
            forced_bits = {cidx[c]: 0 for c in tcells if c in cidx}
            ok2, sol2, freed2 = gf2_solve(rows, rhs, len(cells), forced_bits)
            char = None
            if ok2:
                # read the induced character on every relation (must be sigma)
                char = all(
                    (sum(sol2.get(cidx[c], 0) for c, e in rel[2].items()
                         if e % 2) % 2) == sigma[r]
                    for r, rel in enumerate(allrels))
            tree_results.append({
                "rule": rule, "tiebreak": kname,
                "tree_cells": len(tcells), "vertices_reached": reached,
                "cell_graph_vertices": nv,
                "lift_exists": ok2,
                "residual_free_dim": freed2,
                "reproduces_character": char,
                "solution_signature": (
                    tuple(sorted(c for c, b in sol2.items() if b))
                    if ok2 else None),
            })
    rec["tree_gauge_fixed_lifts"] = [
        {k: v for k, v in t.items() if k != "solution_signature"}
        for t in tree_results]
    sigs = {t["solution_signature"] for t in tree_results if t["lift_exists"]}
    rec["distinct_tree_fixed_lifts"] = len(sigs)
    rec["all_trees_give_same_character"] = all(
        t["reproduces_character"] for t in tree_results if t["lift_exists"])
    rec["every_tree_lift_exists"] = all(t["lift_exists"] for t in tree_results)
    return rec


results = [analyse("S_odd (repo 3P2 chart, with rank-one minors)",
                   S_ODD, True),
           analyse("S_odd (two-term fibres only, no minors)", S_ODD, False),
           analyse("S_bip (bipartite cell graph)", S_BIP, False)]
out["supports"] = results
out["per_fibre_max_forced_relations"] = {
    r["support_name"]: r["max_forced_relations_in_ONE_fibre"] for r in results}
out["obstruction_is_cross_fibre (needs >=2 colourings)"] = {
    r["support_name"]: r.get("certificate", {}).get(
        "distinct_colourings_used") for r in results}

json.dump(out, open("t2_holonomy.json", "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))

#!/usr/bin/env python3
"""T2(c) -- the mechanism test: does spanning-tree transport of a SIGN local
system behave as claimed (tree-independent iff balanced; differences localised
on the -1 loops)?  And: can such a sign system arise on the flip graph from
the equations at all?

Part 1 (mechanism).  On the K_6 2-switch flip graph put eps: E -> {+-1}.
  * balanced eps (eps = sigma(M) sigma(M') for some sigma: V -> +-1):
    every spanning tree gives the SAME transported sign, up to the value at
    the root.  Verified for 6 trees (3 rules x 2 tie-breaks).
  * unbalanced eps (one non-tree edge negated): H_T differs between trees;
    the vertex set where they differ is computed and compared with the set of
    vertices whose fundamental cycle has holonomy -1.

Part 2 (provenance).  A bounded search over N = 6 cell supports for a support
whose FORCED relations (two-term mixed fibres, sign -1, plus rank-one minors,
sign +1) are inconsistent, i.e. carry an O1 (1 = -1).  Reports whether any
such inconsistency is ever supported inside ONE colouring fibre.
"""
from collections import defaultdict
from itertools import combinations, product
import json
import random

import fliptree_lib as F

out = {"pinned_head": open("PINNED_HEAD.txt").read().strip()}

# =============================================================== Part 1
MATCHINGS = F.all_matchings(6)
adj = F.flip_graph(MATCHINGS, F.two_switch_neighbours)
E = F.undirected_edges(adj)
ROOT = min(MATCHINGS)

KEYS = {"lex": (lambda M: M),
        "revlex": (lambda M: tuple(tuple(-x for x in p) for p in M)),
        "hash": (lambda M: (hash((M, 20260813)) & 0xffff, M))}
RULES = {"bfs": F.bfs_tree, "dfs": F.dfs_tree, "dij": F.dijkstra_tree}


def trees():
    for rn, rf in RULES.items():
        for kn, kf in KEYS.items():
            parent, depth, _o = rf(adj, ROOT, key=kf)
            yield f"{rn}/{kn}", parent, depth


def transported_sign(parent, eps, M):
    s = 1
    v = M
    while parent[v] is not None:
        p = parent[v]
        s *= eps[(min(v, p), max(v, p))]
        v = p
    return s


def holonomy(parent, depth, eps, e):
    """sign holonomy of the fundamental cycle of non-tree edge e."""
    A, B = e
    return (eps[e] * transported_sign(parent, eps, A)
            * transported_sign(parent, eps, B))


def report(name, eps):
    rec = {"sign_system": name}
    sigs, per_tree = {}, []
    for tname, parent, depth in trees():
        sig = tuple(transported_sign(parent, eps, M) for M in MATCHINGS)
        sigs.setdefault(sig, []).append(tname)
        TE = set(F.tree_edges(parent))
        hol = {e: holonomy(parent, depth, eps, e) for e in E if e not in TE}
        per_tree.append({"tree": tname,
                         "nontree_edges": len(hol),
                         "holonomy_minus_one_cycles":
                             sum(1 for v in hol.values() if v == -1)})
    rec["trees_tested"] = len(per_tree)
    rec["distinct_transported_sign_vectors"] = len(sigs)
    rec["tree_independent"] = len(sigs) == 1
    rec["per_tree"] = per_tree
    # localisation: which vertices differ between the first two distinct sigs
    keys = list(sigs)
    if len(keys) > 1:
        a, b = keys[0], keys[1]
        diff = [repr(M) for M, x, y in zip(MATCHINGS, a, b) if x != y]
        rec["vertices_where_two_trees_disagree"] = len(diff)
        # a vertex can only disagree if some cycle through it has holonomy -1
        parent0, depth0 = None, None
        for tname, parent, depth in trees():
            parent0, depth0 = parent, depth
            break
        TE = set(F.tree_edges(parent0))
        neg = [e for e in E if e not in TE
               and holonomy(parent0, depth0, eps, e) == -1]
        rec["negative_fundamental_cycles"] = len(neg)
        # vertices lying on some negative fundamental cycle
        onneg = set()
        for e in neg:
            A, B = e
            onneg |= set(F.tree_path(parent0, depth0, A, B))
        rec["vertices_on_negative_cycles"] = len(onneg)
        rec["disagreement_contained_in_negative_cycle_support"] = set(
            diff) <= {repr(M) for M in onneg}
    return rec


part1 = []
# (i) balanced: switching of the all-plus system
rng = random.Random(20260813)
sigma = {M: rng.choice((1, -1)) for M in MATCHINGS}
eps_bal = {e: sigma[e[0]] * sigma[e[1]] for e in E}
part1.append(report("balanced (switching class of all-plus)", eps_bal))
# sanity: balanced <=> no negative cycle
p0, d0, _ = F.bfs_tree(adj, ROOT)
TE0 = set(F.tree_edges(p0))
part1[-1]["is_balanced_check_no_negative_fundamental_cycle"] = all(
    holonomy(p0, d0, eps_bal, e) == 1 for e in E if e not in TE0)

# (ii) unbalanced: negate ONE non-tree edge of the lex BFS tree
bad = [e for e in E if e not in TE0][0]
eps_unb = dict(eps_bal)
eps_unb[bad] = -eps_unb[bad]
r = report("unbalanced (one non-tree edge negated)", eps_unb)
r["negated_edge"] = repr(bad)
part1.append(r)

# (iii) all-plus (trivially balanced) for contrast
part1.append(report("all-plus", {e: 1 for e in E}))
out["part1_mechanism"] = part1

# =============================================================== Part 2
N = 6
PALETTE = (0, 1, 2)
PAIRS = list(combinations(range(N), 2))
COLPAIRS = list(product(PALETTE, repeat=2))


def forced_system(S):
    """Return (relations, one_term_kill).  relation = (tag, lambda dict, sign)."""
    live = defaultdict(list)
    for chi in product(PALETTE, repeat=N):
        for M in MATCHINGS:
            if all(F.cell(u, v, chi) in S for u, v in M):
                live[chi].append(M)
    if not all(tuple([c] * N) in live for c in PALETTE):
        return None, "constant fibre empty"
    rels = []
    for chi, Ms in live.items():
        if len(set(chi)) == 1:
            continue
        if len(Ms) == 1:
            return None, "one-term mixed fibre (O2)"
        if len(Ms) == 2:
            A, B = sorted(Ms)
            rels.append((chi, F.laurent_ratio(B, A, chi), -1))
    return rels, None


def inconsistent(rels):
    """GF(2) consistency of  prod s(c)^{lambda_c} = sign."""
    cells = sorted({c for _t, lam, _s in rels for c in lam})
    cidx = {c: i for i, c in enumerate(cells)}
    rows = [({cidx[c] for c, e in lam.items() if e % 2}, 1 if sg == -1 else 0)
            for _t, lam, sg in rels]
    piv = {}
    witness = None
    for R, b in rows:
        R = set(R)
        while True:
            common = R & set(piv)
            if not common:
                break
            p = min(common)
            R ^= piv[p][0]
            b ^= piv[p][1]
        if R:
            piv[min(R)] = (R, b)
        elif b:
            witness = True
            break
    return witness is True


found = []
rng2 = random.Random(4242)
TRIES = 400
for t in range(TRIES):
    S = set()
    for (u, v) in PAIRS:
        k = rng2.randint(1, 9)
        for cp in rng2.sample(COLPAIRS, k):
            S.add((u, v, cp[0], cp[1]))
    S = frozenset(S)
    rels, why = forced_system(S)
    if rels is None or len(rels) < 2:
        continue
    if inconsistent(rels):
        percol = defaultdict(int)
        for chi, _l, _s in rels:
            percol[chi] += 1
        found.append({"cells": len(S), "relations": len(rels),
                      "max_relations_in_one_fibre": max(percol.values()),
                      "distinct_colourings": len(percol)})
out["part2_search"] = {
    "random_supports_tried": TRIES,
    "supports_with_O1_inconsistency": len(found),
    "examples": found[:5],
    "max_forced_relations_in_ONE_fibre_over_all_found": (
        max(f["max_relations_in_one_fibre"] for f in found) if found else None),
}

json.dump(out, open("t2c_signed_tree.json", "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))

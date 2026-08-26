#!/usr/bin/env python3
"""T3 -- K_8, the two-row inventory, and K_tree.

MUST be run from a snapshot directory: a `git archive` of the pinned HEAD
plus PINNED_HEAD.txt, plus common.py from
computations/unaudited-repair1-k-chain-map-2026-08-13/ and fliptree_lib.py
from this directory.  (See run_t3.sh.)

Steps:
  1  flip graph on the 105 perfect matchings of K_8 (2-switch); and the
     induced graph on the 90 matchings that avoid base.DIRECT_FREE_PAIR --
     the ones carrying the committed 90-term presentation rows.
  2  the TWO-ROW OCCURRENCE GRAPH: nodes = the 180 monomials of the
     pure+mixed inventory (MIXED = w . PURE), edges =
        horizontal: a 2-switch inside one word,          sign +1
        vertical:   (M, PURE) -- (M, MIXED),             sign = the physical
                    w_act sign at M   (a literal edge binomial of the
                    equations: sigma_e . [target] - [source])
  3  rooted spanning trees, three tree rules x three tie-break orders.
  4  K_tree readouts, each a SUM OF EDGE BINOMIALS along tree paths:
        V1 telescoping   :  (1-s)( sigma.[w c0] - [c0] )        [root-free]
        V2 plain path    :  (1-s) sum_i ( sigma_i [v_{i+1}] - [v_i] )
        V3 alternating   :  (1-s) sum_i (-1)^{k-1-i}( sigma_i [v_{i+1}] - [v_i] )
        V4 root-based    :  (1-s)( B_T(root->w c0) - B_T(root->c0) )
     all four collapse to K_phys = (1-s)(w-1)[c0] when the tree path from
     c0 to w.c0 is the single vertical edge.
  5  tests  (a) shadow_2(K_tree) == D2 target and corners == alpha
            (b) K_tree - K_phys inside the committed-readout freedom
            (c) canonicity across tie-breaks; span of differences vs freedom.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
import json

import common as C
import fliptree_lib as F

out = {"pinned_head": open("PINNED_HEAD.txt").read().strip()}

m = C.modules()
base, cm = m["base"], m["commutator"]
PURE, MIXED = cm.PURE_WORD, cm.MIXED_WORD
CORNERS = cm.CORNERS
ALPHA = cm.ALPHA
out["pure_word"] = "".join(map(str, PURE))
out["mixed_word"] = "".join(map(str, MIXED))
out["direct_free_pair"] = sorted(base.DIRECT_FREE_PAIR)

# MIXED must be w . PURE for the two-row inventory to be a w-orbit
wm, _sg = C.w_act(tuple(sorted((u, v, PURE[u], PURE[v])
                               for u, v in [(0, 1), (2, 3), (4, 5), (6, 7)])))
out["mixed_is_w_of_pure"] = (
    tuple(2 if i in (2, 5) else 1 for i in range(8)) == MIXED)

# ------------------------------------------------------------------ step 1
ALLM = F.all_matchings(8)
out["n_matchings_K8"] = len(ALLM)
adj_full = F.flip_graph(ALLM, F.two_switch_neighbours)
E_full = F.undirected_edges(adj_full)
out["K8_flip_connected"] = F.is_connected(adj_full)
out["K8_flip_edges"] = len(E_full)
out["K8_flip_degree_profile"] = sorted(
    Counter(len(v) for v in adj_full.values()).items())
out["K8_flip_cycle_rank"] = len(E_full) - len(ALLM) + 1

DFP = tuple(sorted(base.DIRECT_FREE_PAIR))
SUB = [M for M in ALLM if DFP not in M]
out["n_matchings_avoiding_direct_free_pair"] = len(SUB)
adj_sub = F.flip_graph(SUB, F.two_switch_neighbours)
out["subgraph_connected"] = F.is_connected(adj_sub)
out["subgraph_edges"] = len(F.undirected_edges(adj_sub))
out["subgraph_degree_profile"] = sorted(
    Counter(len(v) for v in adj_sub.values()).items())
out["subgraph_cycle_rank"] = (out["subgraph_edges"] - len(SUB) + 1
                              if out["subgraph_connected"] else None)

# ------------------------------------------------------------------ step 2
pure_row = C.physical_row(base, PURE)
mixed_row = C.physical_row(base, MIXED)
INV = list(pure_row)
seen = set(INV)
for mo in mixed_row:
    if mo not in seen:
        seen.add(mo)
        INV.append(mo)
out["inventory_monomials"] = len(INV)
IIDX = {mo: i for i, mo in enumerate(INV)}


def matching_of(mo):
    return tuple(sorted((c[0], c[1]) for c in mo))


def word_of(mo):
    w = [None] * 8
    for (u, v, a, b) in mo:
        w[u], w[v] = a, b
    return tuple(w)


out["inventory_words"] = sorted({"".join(map(str, word_of(mo))) for mo in INV})
out["inventory_matchings_per_word"] = len(
    {matching_of(mo) for mo in INV if word_of(mo) == PURE})
out["inventory_matchings_equal_subgraph"] = (
    {matching_of(mo) for mo in INV if word_of(mo) == PURE} == set(SUB))

# occurrence graph
node = {mo: mo for mo in INV}
oadj = defaultdict(list)
edge_sign = {}


def put(a, b, sg):
    oadj[a].append(b)
    oadj[b].append(a)
    edge_sign[(a, b)] = sg
    edge_sign[(b, a)] = sg


hor = ver = 0
by_word = defaultdict(dict)
for mo in INV:
    by_word[word_of(mo)][matching_of(mo)] = mo
for w, tab in by_word.items():
    for M, mo in tab.items():
        for Nn in F.two_switch_neighbours(M):
            if Nn in tab and M < Nn:
                put(mo, tab[Nn], 1)
                hor += 1
for M, mo in by_word[PURE].items():
    img, sg = C.w_act(mo)
    assert img in IIDX, "w does not preserve the two-row inventory"
    put(mo, img, sg)
    ver += 1
out["occurrence_graph_horizontal_edges"] = hor
out["occurrence_graph_vertical_edges"] = ver
oadj = {k: sorted(set(v)) for k, v in oadj.items()}
out["occurrence_graph_nodes"] = len(oadj)
out["occurrence_graph_connected"] = F.is_connected(oadj)
out["vertical_edge_signs"] = sorted(
    Counter(edge_sign[(mo, C.w_act(mo)[0])] for mo in by_word[PURE].values()
            ).items())

# ------------------------------------------------------------------ K_phys
c0 = CORNERS[0]
assert c0 in IIDX, "corner not in the two-row inventory"
seed = Counter({c0: Q(1)})
stepc = C.act_on_chain(seed, C.w_act)
stepc.subtract(seed)
stepc = Counter({k: v for k, v in stepc.items() if v})
K_phys = Counter(stepc)
K_phys.subtract(C.act_on_chain(stepc, C.s_act))
K_phys = Counter({k: v for k, v in K_phys.items() if v})
out["K_phys_terms"] = len(K_phys)
out["K_phys_corner_values"] = [str(K_phys.get(c, Q(0))) for c in CORNERS]
out["K_phys_equals_alpha_on_corners"] = (
    tuple(K_phys.get(c, Q(0)) for c in CORNERS) == tuple(ALPHA))
TARGET = {(2, p): Q(v) for p, v in cm.expected_second_shadow().items()}
out["shadow2_target_terms"] = len(TARGET)
out["shadow2_K_phys_matches_target"] = (
    {k: Q(v) for k, v in C.shadow2(K_phys).items()} == TARGET)

# ------------------------------------------------------------ the freedom
cols = [{(2, p): Q(1) for p in C.shadow2_of_monomial(mo)} for mo in INV]
feas, sol, kernel, rk, sep = C.solve_exact(cols, TARGET)
out["shadow2_feasible_on_two_row_inventory"] = feas
out["shadow2_rank"] = rk
out["raw_kernel_dim"] = len(kernel)

families = {}
rows, seenk = [], set()
for mo in INV:
    img, _sg = C.s_act(mo)
    key = tuple(sorted((mo, img)))
    if key in seenk:
        continue
    seenk.add(key)
    f = Counter({mo: Q(1)})
    f[img] += Q(1)
    f = {k: v for k, v in f.items() if v}
    if f:
        rows.append(f)
families["s_odd"] = rows
rows, seenk = [], set()
for mo in INV:
    img, sg = C.w_act(mo)
    key = tuple(sorted((mo, img)))
    if key in seenk:
        continue
    seenk.add(key)
    f = Counter({mo: Q(1)})
    f[img] += Q(sg)
    f = {k: v for k, v in f.items() if v}
    if f:
        rows.append(f)
families["w_odd"] = rows
rows, seenk = [], set()
for mo in INV:
    img, _sg = C.s_act(mo)
    key = tuple(sorted((mo, img)))
    if key in seenk:
        continue
    seenk.add(key)
    rows.append({mo: Q(1), img: Q(1)} if img != mo else {mo: Q(1)})
families["endpoint_even_augmentations"] = rows
families["ordinary_residue_corners"] = [{c: Q(1)} for c in CORNERS]
families["row_augmentations"] = [
    {mo: Q(1) for mo in C.physical_row(base, w)} for w in (PURE, MIXED)]
buck = defaultdict(dict)
for mo in INV:
    buck[base.fine_degree_of_edge_monomial(mo)][mo] = Q(1)
families["fine_degree_gradings"] = list(buck.values())
cb = defaultdict(dict)
for mo in INV:
    for cl in mo:
        cb[cl][mo] = Q(1)
families["single_cell_shadow"] = list(cb.values())

allrows = [f for fam in families.values() for f in fam]


def restrict(constraints):
    mrows = []
    for f in constraints:
        row = {}
        for i, kv in enumerate(kernel):
            val = sum(co * kv.get(IIDX[mo], Q(0)) for mo, co in f.items())
            if val:
                row[i] = val
        if row:
            mrows.append(row)
    return mrows


out["freedom_after_family"] = {}
for fn, fam in families.items():
    r = F.rank(restrict(fam))
    out["freedom_after_family"][fn] = {"rank_on_freedom": r,
                                       "residual": len(kernel) - r}
mrows = restrict(allrows)
basis_all = F.rref(mrows)
RESIDUAL = len(kernel) - len(basis_all)
out["freedom_after_ALL_families"] = {"rank_on_freedom": len(basis_all),
                                     "residual_freedom": RESIDUAL}

# ---- explicit basis of the residual freedom, computed as a NULLSPACE over
# the 180 inventory coordinates (integer pivot order throughout).
def nullspace(rows, n):
    """rows: sparse dicts col->Q over columns 0..n-1.  Returns a Q-basis of
    {x : rows . x = 0} as sparse dicts."""
    piv = {}
    for r in rows:
        v = {k: Q(x) for k, x in r.items() if x}
        while v:
            p = min(v)
            if p not in piv:
                inv = Q(1) / v[p]
                piv[p] = {k: x * inv for k, x in v.items()}
                break
            c = v[p]
            for k, x in piv[p].items():
                y = v.get(k, Q(0)) - c * x
                if y:
                    v[k] = y
                else:
                    v.pop(k, None)
    free = [j for j in range(n) if j not in piv]
    out_b = []
    for f in free:
        v = {f: Q(1)}
        for p in sorted(piv, reverse=True):
            row = piv[p]
            val = -sum(x * v.get(k, Q(0)) for k, x in row.items() if k != p)
            if val:
                v[p] = val
        out_b.append(v)
    return out_b, len(piv)


constraint_rows = []
pairidx = {}
for i, mo in enumerate(INV):
    for p in C.shadow2_of_monomial(mo):
        pairidx.setdefault(p, {})[i] = pairidx.setdefault(p, {}).get(i, 0) + 1
for p, col in pairidx.items():
    constraint_rows.append({i: Q(v) for i, v in col.items()})
for f in allrows:
    constraint_rows.append({IIDX[mo]: Q(co) for mo, co in f.items()})
FREEDOM, crank = nullspace(constraint_rows, len(INV))
out["constraint_rows"] = len(constraint_rows)
out["constraint_rank"] = crank
out["explicit_freedom_dim"] = len(FREEDOM)
ok = True
for ch in FREEDOM:
    chain = Counter({INV[i]: v for i, v in ch.items()})
    if C.shadow2(chain):
        ok = False
    if any(chain.get(c, Q(0)) for c in CORNERS):
        ok = False
    for f in allrows:
        if sum(co * chain.get(mo, Q(0)) for mo, co in f.items()):
            ok = False
out["freedom_vectors_verified_zero_on_all_committed_readouts"] = ok


def free_reduce(vec):
    """residual of vec after reducing against FREEDOM (integer pivot order)."""
    piv = {}
    for r in FREEDOM:
        v = {k: Q(x) for k, x in r.items() if x}
        while v:
            p = min(v)
            if p not in piv:
                inv = Q(1) / v[p]
                piv[p] = {k: x * inv for k, x in v.items()}
                break
            c = v[p]
            for k, x in piv[p].items():
                y = v.get(k, Q(0)) - c * x
                if y:
                    v[k] = y
                else:
                    v.pop(k, None)
    v = {k: Q(x) for k, x in vec.items() if x}
    while True:
        common = set(v) & set(piv)
        if not common:
            return v
        p = min(common)
        c = v[p]
        for k, x in piv[p].items():
            y = v.get(k, Q(0)) - c * x
            if y:
                v[k] = y
            else:
                v.pop(k, None)

# ------------------------------------------------------------ trees + K_tree
KEYS = {"lex": (lambda mo: mo),
        "revlex": (lambda mo: tuple(tuple(-x for x in c) for c in mo)),
        "hash": (lambda mo: (hash((mo, 20260813)) & 0xffffff, mo))}
RULES = {"bfs": F.bfs_tree, "dfs": F.dfs_tree, "dij": F.dijkstra_tree}
ROOT = min(INV)
out["root_lexmin_occurrence"] = repr(ROOT)


def _sum(chains):
    o = defaultdict(Q)
    for ch in chains:
        for k, v in ch.items():
            o[k] += v
    return F.clean(dict(o))


def edge_binomial(a, b):
    """sigma_e . [b] - [a]  as a chain."""
    return {b: Q(edge_sign[(a, b)]), a: Q(-1)}


def path_chains(path):
    return [edge_binomial(path[i], path[i + 1]) for i in range(len(path) - 1)]


def apply_1_minus_s(chain):
    ch = Counter({k: Q(v) for k, v in chain.items()})
    ch.subtract(C.act_on_chain(ch, C.s_act))
    return F.clean(dict(ch))


results = []
wc0 = C.w_act(c0)[0]
for rn, rf in RULES.items():
    for kn, kf in KEYS.items():
        parent, depth, _o = rf(oadj, ROOT, key=kf)
        assert len(parent) == len(INV), "tree does not span the inventory"
        p = F.tree_path(parent, depth, c0, wc0)
        chains = path_chains(p)
        k = len(chains)
        V1 = apply_1_minus_s({wc0: Q(edge_sign[(c0, wc0)]), c0: Q(-1)})
        V2 = apply_1_minus_s(
            {kk: v for kk, v in _sum(chains).items()}) if chains else {}
        V3 = apply_1_minus_s(_sum(
            [F.scale(ch, Q((-1) ** (k - 1 - i))) for i, ch in enumerate(chains)]))
        B_root_w = _sum(path_chains(list(reversed(F.path_to_root(parent, wc0)))))
        B_root_c = _sum(path_chains(list(reversed(F.path_to_root(parent, c0)))))
        V4 = apply_1_minus_s(F.sub(B_root_w, B_root_c))
        rec = {"tree_rule": rn, "tiebreak": kn,
               "tree_path_c0_to_wc0_length": k,
               "path_is_single_vertical_edge": (k == 1),
               "vertical_edge_in_tree": (
                   parent.get(wc0) == c0 or parent.get(c0) == wc0)}
        for name, K in (("V1_telescoping", V1), ("V2_plain_path", V2),
                        ("V3_alternating", V3), ("V4_root_based", V4)):
            chain = Counter({kk: v for kk, v in K.items()})
            sh = {kk: Q(v) for kk, v in C.shadow2(chain).items()}
            diff = F.sub({IIDX[kk]: v for kk, v in K.items()},
                         {IIDX[kk]: Q(v) for kk, v in K_phys.items()})
            rec[name] = {
                "terms": len(K),
                "equals_K_phys": (dict(chain) ==
                                  {kk: Q(v) for kk, v in K_phys.items()}),
                "shadow2_matches_D2_target": sh == TARGET,
                "corners": [str(K.get(c, Q(0))) for c in CORNERS],
                "corners_match_alpha": (
                    tuple(K.get(c, Q(0)) for c in CORNERS) == tuple(ALPHA)),
                "diff_from_Kphys_in_freedom": (not free_reduce(diff)),
                "diff_from_Kphys_is_zero": not diff,
                "diff_from_Kphys_terms": len(diff),
                "diff_has_zero_shadow": not C.shadow2(
                    Counter({INV[i]: v for i, v in diff.items()})),
            }
            rec[name]["_diff"] = diff
        results.append(rec)

# ------------------------------------------------------ (c) CANONICITY
canon = {}
for nm in ("V1_telescoping", "V2_plain_path", "V3_alternating",
           "V4_root_based"):
    Ks = [r[nm]["_diff"] for r in results]          # K_tree - K_phys
    uniq = []
    for d in Ks:
        if not any(not F.sub(d, u) and not F.sub(u, d) for u in uniq):
            uniq.append(d)
    # span of pairwise differences between the tree outputs
    base_d = Ks[0]
    diffs = [F.sub(d, base_d) for d in Ks[1:]]
    diffs = [d for d in diffs if d]
    span = F.rref(diffs)
    exits = []
    for d in diffs:
        res = free_reduce(d)
        if res:
            exits.append({"terms": len(d), "residual_terms": len(res),
                          "residual_shadow_terms": len(C.shadow2(Counter(
                              {INV[i]: v for i, v in res.items()}))),
                          "residual_corner_values": [
                              str(res.get(IIDX[c], Q(0))) for c in CORNERS]})
    canon[nm] = {
        "distinct_K_tree_over_9_trees": len(uniq),
        "canonical (all trees agree)": len(uniq) == 1,
        "span_of_tree_differences_dim": len(span),
        "tree_differences_inside_freedom": not exits,
        "exit_directions": exits[:4],
        "freedom_dim": len(FREEDOM),
    }
out["canonicity"] = canon

for r in results:
    for nm in ("V1_telescoping", "V2_plain_path", "V3_alternating",
               "V4_root_based"):
        r[nm].pop("_diff", None)
out["trees"] = results
json.dump(out, open("t3_k8.json", "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))

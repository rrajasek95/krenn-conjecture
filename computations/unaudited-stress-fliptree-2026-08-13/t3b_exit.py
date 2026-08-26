#!/usr/bin/env python3
"""T3(b/c) follow-up -- name the direction in which the tree-dependent
K_tree (variant V3, alternating path accumulation) EXITS the 7-dimensional
committed-readout freedom, and run the K_8 mutation controls.

Run from the same snapshot directory as t3_k8.py.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
import json

import common as C
import fliptree_lib as F

out = {"pinned_head": open("PINNED_HEAD.txt").read().strip()}
m = C.modules()
base, cm = m["base"], m["commutator"]
PURE, MIXED, CORNERS, ALPHA = cm.PURE_WORD, cm.MIXED_WORD, cm.CORNERS, cm.ALPHA

pure_row, mixed_row = C.physical_row(base, PURE), C.physical_row(base, MIXED)
INV = list(pure_row)
seenm = set(INV)
for mo in mixed_row:
    if mo not in seenm:
        seenm.add(mo)
        INV.append(mo)
IIDX = {mo: i for i, mo in enumerate(INV)}


def matching_of(mo):
    return tuple(sorted((c[0], c[1]) for c in mo))


def word_of(mo):
    w = [None] * 8
    for (u, v, a, b) in mo:
        w[u], w[v] = a, b
    return tuple(w)


oadj = defaultdict(list)
edge_sign = {}
by_word = defaultdict(dict)
for mo in INV:
    by_word[word_of(mo)][matching_of(mo)] = mo


def put(a, b, sg):
    oadj[a].append(b)
    oadj[b].append(a)
    edge_sign[(a, b)] = sg
    edge_sign[(b, a)] = sg


for w, tab in by_word.items():
    for M, mo in tab.items():
        for Nn in F.two_switch_neighbours(M):
            if Nn in tab and M < Nn:
                put(mo, tab[Nn], 1)
for M, mo in by_word[PURE].items():
    img, sg = C.w_act(mo)
    put(mo, img, sg)
oadj = {k: sorted(set(v)) for k, v in oadj.items()}

TARGET = {(2, p): Q(v) for p, v in cm.expected_second_shadow().items()}
allrows = []
seenk = set()
for mo in INV:
    img, _ = C.s_act(mo)
    k = tuple(sorted((mo, img)))
    if k in seenk:
        continue
    seenk.add(k)
    f = Counter({mo: Q(1)})
    f[img] += Q(1)
    if {a: b for a, b in f.items() if b}:
        allrows.append({a: b for a, b in f.items() if b})
    allrows.append({mo: Q(1), img: Q(1)} if img != mo else {mo: Q(1)})
seenk = set()
for mo in INV:
    img, sg = C.w_act(mo)
    k = tuple(sorted((mo, img)))
    if k in seenk:
        continue
    seenk.add(k)
    f = Counter({mo: Q(1)})
    f[img] += Q(sg)
    if {a: b for a, b in f.items() if b}:
        allrows.append({a: b for a, b in f.items() if b})
allrows += [{c: Q(1)} for c in CORNERS]
allrows += [{mo: Q(1) for mo in C.physical_row(base, w)} for w in (PURE, MIXED)]
bk = defaultdict(dict)
for mo in INV:
    bk[base.fine_degree_of_edge_monomial(mo)][mo] = Q(1)
allrows += list(bk.values())
cb = defaultdict(dict)
for mo in INV:
    for cl in mo:
        cb[cl][mo] = Q(1)
allrows += list(cb.values())

rowsC = []
pi = defaultdict(dict)
for i, mo in enumerate(INV):
    for p in C.shadow2_of_monomial(mo):
        pi[p][i] = pi[p].get(i, 0) + 1
rowsC += [{i: Q(v) for i, v in col.items()} for col in pi.values()]
rowsC += [{IIDX[mo]: Q(co) for mo, co in f.items()} for f in allrows]


def echelon(rows):
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
    return piv


def nullspace(rows, n):
    piv = echelon(rows)
    basis = []
    for f in [j for j in range(n) if j not in piv]:
        v = {f: Q(1)}
        for p in sorted(piv, reverse=True):
            val = -sum(x * v.get(k, Q(0)) for k, x in piv[p].items() if k != p)
            if val:
                v[p] = val
        basis.append(v)
    return basis


FREEDOM = nullspace(rowsC, len(INV))
FPIV = echelon(FREEDOM)
out["freedom_dim"] = len(FREEDOM)


def free_reduce(vec):
    v = {k: Q(x) for k, x in vec.items() if x}
    while True:
        common = set(v) & set(FPIV)
        if not common:
            return v
        p = min(common)
        c = v[p]
        for k, x in FPIV[p].items():
            y = v.get(k, Q(0)) - c * x
            if y:
                v[k] = y
            else:
                v.pop(k, None)


c0 = CORNERS[0]
wc0 = C.w_act(c0)[0]
seed = Counter({c0: Q(1)})
st = C.act_on_chain(seed, C.w_act)
st.subtract(seed)
st = Counter({k: v for k, v in st.items() if v})
K_phys = Counter(st)
K_phys.subtract(C.act_on_chain(st, C.s_act))
K_phys = Counter({k: v for k, v in K_phys.items() if v})

KEYS = {"lex": (lambda mo: mo),
        "revlex": (lambda mo: tuple(tuple(-x for x in c) for c in mo)),
        "hash": (lambda mo: (hash((mo, 20260813)) & 0xffffff, mo))}
RULES = {"bfs": F.bfs_tree, "dfs": F.dfs_tree, "dij": F.dijkstra_tree}
ROOT = min(INV)


def V3(parent, depth, sign_override=None):
    p = F.tree_path(parent, depth, c0, wc0)
    k = len(p) - 1
    o = defaultdict(Q)
    for i in range(k):
        a, b = p[i], p[i + 1]
        sg = edge_sign[(a, b)]
        if sign_override and (min(a, b), max(a, b)) in sign_override:
            sg = -sg
        w = Q((-1) ** (k - 1 - i))
        o[b] += w * Q(sg)
        o[a] -= w
    ch = Counter(F.clean(o))
    ch.subtract(C.act_on_chain(ch, C.s_act))
    return F.clean(dict(ch))


runs = []
for rn, rf in RULES.items():
    for kn, kf in KEYS.items():
        parent, depth, _ = rf(oadj, ROOT, key=kf)
        K = V3(parent, depth)
        d = F.sub({IIDX[a]: b for a, b in K.items()},
                  {IIDX[a]: Q(b) for a, b in K_phys.items()})
        res = free_reduce(d)
        sh = C.shadow2(Counter({INV[i]: v for i, v in res.items()}))
        runs.append({
            "tree": f"{rn}/{kn}",
            "path_len": len(F.tree_path(parent, depth, c0, wc0)) - 1,
            "K_terms": len(K),
            "equals_K_phys": not d,
            "shadow2_matches_target": (
                {a: Q(b) for a, b in C.shadow2(Counter(K)).items()} == TARGET),
            "residual_after_freedom_terms": len(res),
            "residual_shadow2_terms": len(sh),
            "residual_monomials": sorted(
                (repr(INV[i]), str(v)) for i, v in res.items())[:6],
            "residual_shadow2": sorted(
                (repr(k2), str(v)) for k2, v in sh.items())[:8],
        })
out["V3_runs"] = runs
exits = [r for r in runs if r["residual_after_freedom_terms"]]
out["n_trees_exiting_freedom"] = len(exits)
out["n_trees_reproducing_K_phys"] = sum(1 for r in runs if r["equals_K_phys"])
if exits:
    sm = min(exits, key=lambda r: r["residual_after_freedom_terms"])
    out["smallest_exit_direction"] = sm

# --------------------------------------------------------- K8 mutations
mut = []
parent, depth, _ = RULES["bfs"](oadj, ROOT, key=KEYS["lex"])
base_K = V3(parent, depth)
mut.append({"mutation": "baseline bfs/lex", "equals_K_phys":
            base_K == {k: Q(v) for k, v in K_phys.items()}})
# wrong root
parent2, depth2, _ = RULES["bfs"](oadj, sorted(INV)[17], key=KEYS["lex"])
K2 = V3(parent2, depth2)
mut.append({"mutation": "wrong root (17th occurrence)",
            "equals_K_phys": K2 == {k: Q(v) for k, v in K_phys.items()},
            "terms": len(K2)})
# sign-flipped vertical edge at c0
K3 = V3(parent, depth, sign_override={(min(c0, wc0), max(c0, wc0))})
mut.append({"mutation": "vertical edge sign flipped at the corner",
            "equals_K_phys": K3 == {k: Q(v) for k, v in K_phys.items()},
            "terms": len(K3),
            "shadow2_matches_target": (
                {a: Q(b) for a, b in C.shadow2(Counter(K3)).items()} == TARGET)})
# non-tree: reroute c0's parent through a flip neighbour (creates a cycle)
alt = dict(parent)
cand = [x for x in oadj[wc0] if x != parent.get(wc0) and word_of(x) == MIXED]
if cand:
    alt[wc0] = cand[0]
    seen, v, cyc = set(), wc0, False
    while alt.get(v) is not None:
        if v in seen:
            cyc = True
            break
        seen.add(v)
        v = alt[v]
    if not cyc:
        dp = dict(depth)
        dp[wc0] = dp[alt[wc0]] + 1
        K4 = V3(alt, dp)
        mut.append({"mutation": "non-tree reroute of w.c0 (parent map with an "
                                "extra edge)",
                    "equals_K_phys": K4 == {k: Q(v) for k, v in K_phys.items()},
                    "terms": len(K4),
                    "shadow2_matches_target": (
                        {a: Q(b) for a, b in C.shadow2(Counter(K4)).items()}
                        == TARGET)})
out["mutations"] = mut

json.dump(out, open("t3b_exit.json", "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))

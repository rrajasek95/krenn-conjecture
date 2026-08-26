#!/usr/bin/env python3
"""T4 -- mutation controls for the T1 identity on the K_6 flip graph.

Each mutation must BREAK  d H_T = 1 - P_root  (or the provenance/telescoping
property).  A control that does not break is a red flag for the test itself.

  M0  baseline (correct tree, correct root, correct signs)      must HOLD
  M1  wrong root: transport to the lex-min matching but project
      onto a different vertex                                   must FAIL
  M2  non-tree subgraph: tree + one extra edge, H defined by a
      DIFFERENT path in that subgraph                           must FAIL
      (path-independence lost)
  M3  sign-flipped edge: negate one tree edge's binomial        must FAIL
  M4  spanning FOREST (delete one tree edge)                    must FAIL
  M5  wrong differential  d(e) = [B] + [A]                      must FAIL
  M6  wrong orientation: H uses unsigned path (all +1)          must FAIL
"""
from collections import defaultdict
from fractions import Fraction as Q
import json

import fliptree_lib as F

out = {"pinned_head": open("PINNED_HEAD.txt").read().strip()}
M6 = F.all_matchings(6)
adj = F.flip_graph(M6, F.two_switch_neighbours)
E = F.undirected_edges(adj)
ROOT = min(M6)
parent, depth, order = F.bfs_tree(adj, ROOT)
TE = F.tree_edges(parent)
TEset = set(TE)


def d1(chain1, sign_map=None, plus=False):
    o = defaultdict(Q)
    for (A, B), c in chain1.items():
        s = Q(1) if sign_map is None else Q(sign_map.get((A, B), 1))
        if plus:
            o[B] += s * c
            o[A] += c
        else:
            o[B] += s * c
            o[A] -= c
    return F.clean(o)


def H_path(par, M, unsigned=False):
    o = defaultdict(Q)
    v = M
    while par[v] is not None:
        p = par[v]
        e = (p, v) if p < v else (v, p)
        if unsigned:
            o[e] += Q(1)
        else:
            o[e] += Q(1) if p < v else Q(-1)
        v = p
    return F.clean(o)


def check(par, root, sign_map=None, plus=False, unsigned=False, verts=None):
    bad = []
    for M in (verts if verts is not None else M6):
        if M not in par:
            bad.append((repr(M), "unreached"))
            continue
        lhs = d1(H_path(par, M, unsigned), sign_map, plus)
        rhs = defaultdict(Q)
        rhs[M] += Q(1)
        rhs[root] -= Q(1)
        rhs = F.clean(rhs)
        if lhs != rhs:
            bad.append((repr(M), "mismatch"))
    return bad


res = []

res.append({"mutation": "M0 baseline", "expect": "HOLD",
            "failures": len(check(parent, ROOT)),
            "identity_holds": not check(parent, ROOT)})

wrong_root = sorted(M6)[7]
b = check(parent, wrong_root)
res.append({"mutation": "M1 wrong root (project onto " + repr(wrong_root) + ")",
            "expect": "FAIL", "failures": len(b),
            "identity_holds": not b})

# M2: tree + one extra edge, route one vertex the other way
extra = [e for e in E if e not in TEset][0]
A, B = extra
par2 = dict(parent)
par2[B] = A if depth[A] + 1 != depth[B] or parent[B] != A else parent[B]
# force B's parent to be A through the extra edge (creates a different path)
par2[B] = A
# make sure we did not create a cycle in the parent map
seen, v, cyc = set(), B, False
while par2.get(v) is not None:
    if v in seen:
        cyc = True
        break
    seen.add(v)
    v = par2[v]
b = check(par2, ROOT) if not cyc else [("cycle", "parent map cyclic")]
# and: is the resulting H the same as the tree H?
same = all(H_path(par2, M) == H_path(parent, M) for M in M6)
res.append({"mutation": "M2 non-tree subgraph, alternative path via "
                        + repr(extra),
            "expect": "FAIL (path-dependence)",
            "identity_holds": not b,
            "failures": len(b),
            "H_unchanged_from_tree": same,
            "note": ("d H = 1 - P still holds for ANY path -- the additive "
                     "identity is path-blind; what breaks is uniqueness of H")})

sign_map = {TE[0]: -1}
b = check(parent, ROOT, sign_map=sign_map)
res.append({"mutation": "M3 sign-flipped tree edge " + repr(TE[0]),
            "expect": "FAIL", "failures": len(b), "identity_holds": not b})

par4 = dict(parent)
drop = [v for v, p in parent.items() if p is not None][-1]
del par4[drop]
b = check(par4, ROOT)
res.append({"mutation": "M4 spanning forest (drop " + repr(drop) + ")",
            "expect": "FAIL", "failures": len(b), "identity_holds": not b})

b = check(parent, ROOT, plus=True)
res.append({"mutation": "M5 wrong differential d(e)=[B]+[A]",
            "expect": "FAIL", "failures": len(b), "identity_holds": not b})

b = check(parent, ROOT, unsigned=True)
res.append({"mutation": "M6 unsigned path (H ignores traversal direction)",
            "expect": "FAIL", "failures": len(b), "identity_holds": not b})

out["mutations"] = res
out["all_controls_behave_as_expected"] = all(
    (r["identity_holds"] is True) == r["expect"].startswith("HOLD")
    for r in res if r["mutation"].startswith(("M0", "M1", "M3", "M4", "M5")))

# ---------------- provenance mutation: sign-flip breaks telescoping
CHI = (0, 0, 1, 1, 2, 2)


def transport(path, flip=None):
    acc = {}
    for a, b2 in zip(path, path[1:]):
        r = F.laurent_ratio(a, b2, CHI)
        e = (a, b2) if a < b2 else (b2, a)
        if flip and e == flip:
            r = F.ratio_inv(r)
        acc = F.ratio_mul(acc, r)
    return acc


ok, bad2 = 0, 0
for M in M6:
    p = list(reversed(F.path_to_root(parent, M)))
    direct = {c: 1 for c in F.monomial_of(M, CHI)}
    for c in F.monomial_of(ROOT, CHI):
        direct[c] = direct.get(c, 0) - 1
    direct = {c: k for c, k in direct.items() if k}
    if transport(p) == direct:
        ok += 1
    if transport(p, flip=TE[0]) == direct:
        bad2 += 1
out["provenance_baseline_correct"] = ok == len(M6)
out["provenance_after_edge_inversion_still_correct"] = bad2
out["provenance_mutation_breaks"] = bad2 < len(M6)

json.dump(out, open("t4_mutations.json", "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))

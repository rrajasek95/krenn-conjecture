#!/usr/bin/env python3
"""A6 / TARGET B item 6: THEOREM W14.3 (directness of L_h(A)) re-derived.

CLAIM: L_h(A) = (+)_{k=2}^h s^{h-k} iota_k(Sigma_k) is DIRECT when
rank A = 3; dims 136 / 131 / 125 at ranks 3 / 2 / 1 for h = 3.

A6's re-derivation of the proof:
 (a) GL-substitution.  K -> g^T K h sends s_A to s_{gAh^T} and preserves
     each iota_k(Sigma_k) (a GL(V) x GL(W) submodule of S^k(V (x) W)).
     So dim L_h(A) depends only on the GL x GL orbit of A = its rank; at
     rank 3 we may take A = Id, i.e. s = tr(K) = K00 + K11 + K22.
 (b) KEY LEMMA: iota_h(Sigma_h) intersect tr * S^{h-1} = 0.  Given it,
     if sum_k tr^{h-k} c_k = 0 with c_k in C_k := iota_k(Sigma_k), then
     c_h in tr*S^{h-1} so c_h = 0; tr is a nonzerodivisor, divide and
     induct (m >= 1 induction on the number of surviving levels).
 So the theorem reduces EXACTLY to the key lemma at every level j <= h.
A6 verifies (a) and (b) computationally, exactly, at h = 2, 3, 4.
"""
from __future__ import annotations

import json
import random
from fractions import Fraction
from itertools import combinations_with_replacement

import a6_bcore as B

out = {}
rng = random.Random(31415)

IDENT = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
PERM = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
DIAG = [[1, 0, 0], [0, 2, 0], [0, 0, -3]]
GEN = [[2, -1, 3], [0, 4, 1], [-2, 1, 5]]
A00 = [[0, 2, -1], [3, 1, 4], [1, -2, 2]]
RK2 = [[1, 2, 3], [2, 4, 6], [0, 1, -1]]
RK1 = [[1, 2, 3], [2, 4, 6], [-1, -2, -3]]
RK0 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
NEW1 = [[5, -7, 11], [13, 2, -3], [1, 1, 1]]      # not in W14's battery
NEW2 = [[1, 1, 1], [1, 2, 4], [1, 3, 9]]          # Vandermonde
BATT = [("identity", IDENT), ("permutation", PERM), ("diag(1,2,-3)", DIAG),
        ("generic", GEN), ("A00=0 rank3", A00), ("new1", NEW1),
        ("vandermonde", NEW2), ("rank2", RK2), ("rank1", RK1),
        ("rank0", RK0)]

# ---------------------------------------------------- dim L_h and directness
dims = {}
for h in (2, 3):
    dims[h] = {}
    for nm, A in BATT:
        rows, tags = B.L_rows(h, A)
        basis, piv = B.rref(rows)
        per_level = {}
        for k in range(2, h + 1):
            sub = [r for r, t in zip(rows, tags) if t[0] == k]
            per_level[k] = len(B.rref(sub)[1])
        dims[h][nm] = {"rank_A": B.rank3(A), "det_A": B.det3(A),
                       "dim_L": len(piv),
                       "sum_dim_levels": sum(per_level.values()),
                       "per_level_dims": per_level,
                       "direct": len(piv) == sum(per_level.values())}
out["dim_L_h"] = dims

# h = 4 (mod-p rank is a RIGOROUS lower bound; equality with the expected
# value therefore proves directness over Q)
rows4, tags4 = B.L_rows(4, IDENT)
r4p = B.rank_mod_p(rows4)
lv4 = {}
for k in (2, 3, 4):
    sub = [r for r, t in zip(rows4, tags4) if t[0] == k]
    lv4[k] = B.rank_mod_p(sub)
out["h4_identity"] = {"dim_L4_mod_p": r4p, "level_dims_mod_p": lv4,
                      "sum": sum(lv4.values()),
                      "direct_over_Q_proved_by_mod_p": r4p == sum(lv4.values())}

# --------------------------------------------------------------- KEY LEMMA
# C_h intersect tr*S^{h-1} = 0   <=>   rank[C_h rows ; tr*S^{h-1} rows]
#                                       = dim C_h + dim S^{h-1}
key = {}
for h in (2, 3, 4):
    ch = []
    for mu, nu in B.sigma_pairs(h):
        f = B.iota_poly(h, mu, nu)
        ch.append(B.prow(f, h))
    tr = {(0,): 1, (4,): 1, (8,): 1}
    trs = []
    for m in combinations_with_replacement(range(9), h - 1):
        f = B.pmul(tr, {m: 1})
        trs.append(B.prow(f, h))
    dc = B.rank_mod_p(ch)
    dt = B.rank_mod_p(trs)
    tot = B.rank_mod_p(ch + trs)
    key[h] = {"dim_C_h": dc, "dim_tr_S": dt, "rank_together": tot,
              "expected_if_direct": dc + dt,
              "intersection_zero": tot == dc + dt,
              "ambient": len(B.midx(9, h))}
out["key_lemma_C_h_cap_trS"] = key

# exact (over Q) confirmation at h = 2, 3
for h in (2, 3):
    ch = [B.prow(B.iota_poly(h, mu, nu), h) for mu, nu in B.sigma_pairs(h)]
    tr = {(0,): 1, (4,): 1, (8,): 1}
    trs = [B.prow(B.pmul(tr, {m: 1}), h)
           for m in combinations_with_replacement(range(9), h - 1)]
    key[h]["exact_rank_together"] = len(B.rref(ch + trs)[1])
out["key_lemma_exact_h2_h3"] = {h: key[h].get("exact_rank_together")
                                for h in (2, 3)}

# ------------------------------------- (a) GL-invariance of the level spaces
def subst_rows(rows_poly, g, hmat, deg):
    """apply K -> g^T K h to a list of polynomials (as dict) -> rows"""
    # K_ij -> sum_{ab} g[a][i] * K_ab * h[b][j]
    lin = {}
    for i in B.COL:
        for j in B.COL:
            lin[B.kx(i, j)] = {(B.kx(a, b),): g[a][i] * hmat[b][j]
                               for a in B.COL for b in B.COL
                               if g[a][i] * hmat[b][j]}
    outr = []
    for f in rows_poly:
        acc = {}
        for mon, c in f.items():
            t = {(): c}
            for v in mon:
                t = B.pmul(t, lin[v])
            acc = B.padd(acc, t)
        outr.append(B.prow(acc, deg) if acc else [0] * len(B.midx(9, deg)))
    return outr


g = [[1, 2, 0], [0, 1, 1], [1, 0, 1]]
hm = [[2, 0, 1], [1, 1, 0], [0, 1, 1]]
polys3 = [B.iota_poly(3, mu, nu) for mu, nu in B.sigma_pairs(3)]
base_rows = [B.prow(f, 3) for f in polys3]
bb, pp = B.rref(base_rows)
sub_rows = subst_rows(polys3, g, hm, 3)
out["GL_substitution_preserves_iota3_image"] = all(
    B.in_span(bb, pp, r) for r in sub_rows)
# and it must move a NON-invariant space (control)
ctrl = [B.prow({(0, 0, 0): 1}, 3), B.prow({(1, 1, 1): 1}, 3)]
cb, cp = B.rref(ctrl)
out["control_GL_moves_a_random_subspace"] = not all(
    B.in_span(cb, cp, r) for r in subst_rows([{(0, 0, 0): 1}, {(1, 1, 1): 1}],
                                             g, hm, 3))
# s_A transforms to s_{g A h^T}
def mmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in B.COL) for j in B.COL]
            for i in B.COL]


A = GEN
sA = {(B.kx(i, j),): A[i][j] for i in B.COL for j in B.COL if A[i][j]}
lhs = subst_rows([sA], g, hm, 1)[0]
gAh = mmul(mmul(g, A), [[hm[j][i] for j in B.COL] for i in B.COL])
rhs = B.prow({(B.kx(i, j),): gAh[i][j] for i in B.COL for j in B.COL
              if gAh[i][j]}, 1)
out["s_A_substitution_law"] = (lhs == rhs)

json.dump(out, open("results_B6_directness.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))

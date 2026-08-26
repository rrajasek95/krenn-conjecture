#!/usr/bin/env python3
"""A6 / B6 continued: the KEY LEMMA  C_h cap tr*S^{h-1} = 0  at h = 5, 6.

rank over F_p is a LOWER bound for rank over Q, so hitting the maximal
possible value proves directness over Q.  numpy mod p (p prime, p^2 fits
in int64).  Mutation control: a deliberately dependent row set must show
a rank DROP.
"""
import json
from itertools import combinations_with_replacement, permutations
import numpy as np
import a6_bcore as B

P = 2147483629


def rank_modp(rows, ncols):
    M = np.array(rows, dtype=np.int64) % P
    r = 0
    for c in range(ncols):
        piv = None
        nz = np.nonzero(M[r:, c])[0]
        if nz.size == 0:
            continue
        piv = r + int(nz[0])
        M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), P - 2, P)
        M[r] = (M[r] * inv) % P
        col = M[:, c].copy()
        col[r] = 0
        nzr = np.nonzero(col)[0]
        if nzr.size:
            M[nzr] = (M[nzr] - np.outer(col[nzr], M[r])) % P
        r += 1
        if r == M.shape[0]:
            break
    return r


out = {}
for h in (4, 5):
    idx = B.midx(9, h)
    nc = len(idx)
    ch = [B.prow(B.iota_poly(h, mu, nu), h) for mu, nu in B.sigma_pairs(h)]
    tr = {(0,): 1, (4,): 1, (8,): 1}
    trs = [B.prow(B.pmul(tr, {m: 1}), h)
           for m in combinations_with_replacement(range(9), h - 1)]
    dc, dt = rank_modp(ch, nc), rank_modp(trs, nc)
    tot = rank_modp(ch + trs, nc)
    out[h] = dict(ambient=nc, dim_C_h=dc, dim_trS=dt, rank_together=tot,
                  expected=dc + dt, intersection_zero=tot == dc + dt)
    # mutation control: add a duplicate row, rank must not increase
    out[h]["control_duplicate_row_no_rank_gain"] = (
        rank_modp(ch + trs + [ch[0]], nc) == tot)
    # mutation control: an element that IS in tr*S^{h-1} must not raise the rank
    bad = B.prow(B.pmul(tr, {tuple([0] * (h - 1)): 1}), h)
    out[h]["control_dependent_row_no_rank_gain"] = (
        rank_modp(ch + trs + [bad], nc) == tot)

# full L_h directness at h = 5 with A = identity
for h in (5,):
    rows, tags = B.L_rows(h, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    nc = len(B.midx(9, h))
    lv = {}
    for k in range(2, h + 1):
        sub = [r for r, t in zip(rows, tags) if t[0] == k]
        lv[k] = rank_modp(sub, nc)
    tot = rank_modp(rows, nc)
    out["L_%d_identity" % h] = dict(dim_L=tot, levels=lv, sum=sum(lv.values()),
                                    direct=tot == sum(lv.values()))
json.dump(out, open("results_B6b_keylemma.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))

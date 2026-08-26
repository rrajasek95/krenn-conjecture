#!/usr/bin/env python3
"""STEP 7: global rank bookkeeping for the operator block (control on S).

rank(M) = rank(pi_constraint M) + dim( pi_shadow ( ker pi_constraint M ) )
so dim S is pinned by two ranks.  Dense modular elimination with numpy.
"""
import json
import numpy as np

import common as C

PRIMES = [1_000_003, 999_983]


def rank_dense(rows_index, cols, p):
    rows = sorted(rows_index, key=repr)
    ri = {r: i for i, r in enumerate(rows)}
    M = np.zeros((len(rows), len(cols)), dtype=np.int64)
    for j, (_md, col) in enumerate(cols):
        for r, v in col.items():
            if r in ri:
                M[ri[r], j] = v % p
    M %= p
    rank = 0
    nrows, ncols = M.shape
    for c in range(ncols):
        if rank >= nrows:
            break
        piv = None
        col = M[rank:, c]
        nz = np.nonzero(col)[0]
        if nz.size == 0:
            continue
        piv = rank + int(nz[0])
        if piv != rank:
            M[[rank, piv]] = M[[piv, rank]]
        inv = pow(int(M[rank, c]), p - 2, p)
        M[rank] = (M[rank] * inv) % p
        below = np.nonzero(M[rank + 1:, c])[0]
        if below.size:
            idx = below + rank + 1
            M[idx] = (M[idx] - np.outer(M[idx, c], M[rank])) % p
        rank += 1
    return rank


m = C.modules()
cols, _shifts = C.build_operator_columns(m, verbose=False)
all_rows = {r for _md, c in cols for r in c}
crows = {r for r in all_rows if r[0] < 2}
srows = {r for r in all_rows if r[0] == 2}
print("rows", len(all_rows), len(crows), len(srows), flush=True)

out = []
for p in PRIMES:
    full = rank_dense(all_rows, cols, p)
    print("full", full, flush=True)
    constraint = rank_dense(crows, cols, p)
    print("constraint", constraint, flush=True)
    shadow = rank_dense(srows, cols, p)
    rec = {"prime": p,
           "rank_full_block": full,
           "rank_constraint_projection_source_plus_D1": constraint,
           "rank_shadow_projection": shadow,
           "dim_attainable_D2_on_ker(source,D1)": full - constraint}
    print(json.dumps(rec, sort_keys=True), flush=True)
    out.append(rec)
json.dump(out, open("step7_ranks.json", "w"), indent=1, sort_keys=True)

#!/usr/bin/env python3
"""A5 / claim 2 + 3: THEOREM W13.2 (the law) and the tightness claim.

My Sigma_k is built ONLY from powers (u^T K v)^k at rational u,v -- a
different construction from W13's permanent/iota rows.  The permanent rows are
then checked to lie in that span (and to span it), which is the independent
verification of the "Perm_k = iota_k" identification.
"""
from __future__ import annotations
import json, random, sys, time
from itertools import combinations, permutations, product
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15/"
res = {}


def perm_row(us, vs, k):
    """Perm_k([<K, u_a (x) v_b>]) as a degree-k coefficient vector."""
    acc = {}
    for sigma in permutations(range(k)):
        term = dict(A.ONE)
        for t in range(k):
            u, v = us[t], vs[sigma[t]]
            term = A.pmul(term, A.var_poly([u[i] * v[j] for i in A.C3 for j in A.C3]))
        acc = A.padd(acc, term)
    return A.poly_vec(acc, k)


# ---------------------------------------------------------------- Sigma_k dims
rng = random.Random(4242)
res["sigma"] = []
sig_ech = {}
for k in (2, 3, 4):
    rows = A.sigma_rows_powers(k, rng)
    ech, piv = A.int_echelon(rows)
    r = len(piv)
    want = ((k + 1) * (k + 2) // 2) ** 2
    sig_ech[k] = (ech, piv)
    # permanent rows: in the span?  do they span it?
    prows = []
    for _ in range(want + 10):
        us = [[rng.randint(-4, 4) for _ in A.C3] for _ in range(k)]
        vs = [[rng.randint(-4, 4) for _ in A.C3] for _ in range(k)]
        prows.append(perm_row(us, vs, k))
    inside = all(A.in_span_exact(ech, piv, pr) for pr in prows)
    prank = len(A.int_echelon(prows)[1])
    # negative control: a random degree-k vector should NOT be in Sigma_k
    junk = [rng.randint(-9, 9) for _ in range(len(A.deg_monoms(k)))]
    junk_in = A.in_span_exact(ech, piv, junk)
    print(f"Sigma_{k}: rank(powers)={r} (want {want}); perm rows in span={inside}; "
          f"rank(perm rows)={prank}; random vector in Sigma_k={junk_in}")
    res["sigma"].append({"k": k, "rank_powers": r, "want": want,
                         "perm_rows_in_power_span": inside, "rank_perm_rows": prank,
                         "control_random_vec_in_sigma": junk_in})

# --------------------------------------------------------------- dim L_h(A)
res["dimL"] = []
for h in (2, 3, 4):
    for tag, svec in [("generic", [rng.randint(-6, 6) for _ in range(9)]),
                      ("identity", [1, 0, 0, 0, 1, 0, 0, 0, 1]),
                      ("rank1 uv^T", [1 * 1, 1 * 2, 1 * 3, 2 * 1, 2 * 2, 2 * 3, 3 * 1, 3 * 2, 3 * 3]),
                      ("rank2 diag(1,1,0)", [1, 0, 0, 0, 1, 0, 0, 0, 0]),
                      ("all-ones J", [1] * 9),
                      ("single cell E22", [0, 0, 0, 0, 0, 0, 0, 0, 1]),
                      ("zero", [0] * 9)]:
        t0 = time.time()
        rows = A.L_rows(h, svec, rng)
        r = len(A.int_echelon(rows)[1])
        ub = sum(((k + 1) * (k + 2) // 2) ** 2 for k in range(2, h + 1))
        amb = len(A.deg_monoms(h))
        print(f"h={h} A={tag:18s} dim L_h={r:4d}  (sum dim Sigma_k={ub}, ambient={amb}) "
              f"[{time.time()-t0:.1f}s]")
        res["dimL"].append({"h": h, "A": tag, "s": svec, "dim": r,
                            "sum_dim_sigma": ub, "ambient": amb})
json.dump(res, open(OUT + "results_t2_law_part1.json", "w"), indent=1)

#!/usr/bin/env python3
"""A6 / B6: the two standard inputs to A6's proof of W14.3, verified.
 (1) iota_h(Sigma_h) = span{ (v^T K w)^h } (h-th powers of rank-one forms)
 (2) that span is the apolar perp of (I_2x2minors)_h  (dim + orthogonality)
"""
import json, random
from itertools import combinations, combinations_with_replacement
from fractions import Fraction
import a6_bcore as B

rng = random.Random(4242)
res = {}


def power_of_rank_one(v, w, h):
    lin = {(B.kx(i, j),): v[i] * w[j] for i in B.COL for j in B.COL
           if v[i] * w[j]}
    return B.ppow(lin, h)


def minors_dual():
    out = []
    for (i, k) in combinations(range(3), 2):
        for (j, l) in combinations(range(3), 2):
            out.append({tuple(sorted((B.kx(i, j), B.kx(k, l)))): 1,
                        tuple(sorted((B.kx(i, l), B.kx(k, j)))): -1})
    return out


def apolar(f, g):
    """<f,g> = f(d/dK) g  on equal-degree forms (exact)"""
    tot = 0
    for m, c in f.items():
        if m not in g:
            continue
        cnt = {}
        for v in m:
            cnt[v] = cnt.get(v, 0) + 1
        mult = 1
        for e in cnt.values():
            for t in range(2, e + 1):
                mult *= t
        tot += c * g[m] * mult
    return tot


for h in (2, 3, 4):
    rows = []
    for _ in range(400):
        v = [rng.randint(-4, 4) for _ in B.COL]
        w = [rng.randint(-4, 4) for _ in B.COL]
        p = power_of_rank_one(v, w, h)
        if p:
            rows.append(B.prow(p, h))
    r_pow = B.rank_mod_p(rows)
    iot = [B.prow(B.iota_poly(h, mu, nu), h) for mu, nu in B.sigma_pairs(h)]
    r_io = B.rank_mod_p(iot)
    r_both = B.rank_mod_p(rows + iot)
    # ideal of 2x2 minors in degree h
    gens = []
    for m in minors_dual():
        for u in combinations_with_replacement(range(9), h - 2):
            gens.append(B.prow(B.pmul(m, {u: 1}), h))
    r_id = B.rank_mod_p(gens)
    # orthogonality of iota_h(Sigma_h) against every ideal generator
    ok = True
    for mu, nu in B.sigma_pairs(h)[:40]:
        f = B.iota_poly(h, mu, nu)
        for m in minors_dual():
            for u in combinations_with_replacement(range(9), h - 2):
                if apolar(f, B.pmul(m, {u: 1})) != 0:
                    ok = False
                    break
    res[h] = {"dim_span_rank_one_powers": r_pow, "dim_iota_Sigma_h": r_io,
              "same_space": r_both == r_io == r_pow,
              "dim_ideal_degree_h": r_id, "ambient": len(B.midx(9, h)),
              "dims_add_up": r_io + r_id == len(B.midx(9, h)),
              "iota_perp_to_ideal(sampled)": ok}
json.dump(res, open("results_B6d_apolarity.json", "w"), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))

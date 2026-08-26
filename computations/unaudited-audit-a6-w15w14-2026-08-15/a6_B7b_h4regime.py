#!/usr/bin/env python3
"""A6 / B7 extra: is the counterexample REGIME non-vacuous at h = 4?
(W14 logs this but its membership verdict timed out.)  A6 only checks the
regime: colour-c slice CLEAN (all words), A_pq(c,c) = 0, some G_j != 0.
"""
import json, random
from itertools import product
import a6_bcore as B

rng = random.Random(24680)
H = 4
_, _, U = B.sites(H)
out = {}


def fix_pair(src, c, zero_diag):
    while True:
        A = [[rng.randint(-4, 4) for _ in B.COL] for _ in B.COL]
        if zero_diag:
            A[c][c] = 0
        elif A[c][c] == 0:
            continue
        if B.rank3(A) == 3 and all(any(A[i][j] for j in B.COL) for i in B.COL) \
                and all(any(A[i][j] for i in B.COL) for j in B.COL):
            src[(0, 1)] = A
            return A


def build(kind, c, zero_diag):
    src = B.rnd_source(H, rng)
    if kind == "F2":
        for a in U[:len(U) - 2]:
            for cv in B.COL:
                src[(0, a)][c][cv] = 0
    elif kind == "F3":
        a = U[0]
        for cv in B.COL:
            src[(0, a)][c][cv] = 0
            src[(1, a)][c][cv] = 0
    fix_pair(src, c, zero_diag)
    return src


recs = []
allwords = list(product(range(3), repeat=2 * H))
sample = [allwords[i] for i in rng.sample(range(len(allwords)), 400)]
sample += [tuple([c] * (2 * H)) for c in B.COL]
for kind in ("F2", "F3"):
    for zd in (True, False):
        src = build(kind, 0, zd)
        c = 0
        sc = src[(0, 1)][c][c]
        dc = [1, 0, 0]
        Gs = {j: [B.G_level(src, H, w, dc, dc, j) for w in sample]
              for j in range(H - 1)}
        err = [sum(sc ** j * Gs[j][n] for j in range(H - 1))
               for n in range(len(sample))]
        # exact polynomial cross-check on a few words
        pt = [1 if n == 0 else 0 for n in range(9)]
        poly_err = [B.pev(B.Ew_matchings(src, H, w), pt) for w in sample[:12]]
        recs.append(dict(kind=kind, A_cc=sc, rank_A=B.rank3(src[(0, 1)]),
                         words_sampled=len(sample),
                         slice_clean_on_sample=all(x == 0 for x in err),
                         G_nonzero={j: any(x != 0 for x in Gs[j])
                                    for j in range(H - 1)},
                         poly_matches_G=all(
                             poly_err[i] == err[i] for i in range(12))))
out["h4_regime"] = recs
json.dump(out, open("results_B7b_h4regime.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))

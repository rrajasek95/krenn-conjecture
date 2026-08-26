#!/usr/bin/env python3
"""W16 -- Step A by EXACT LINEAR ALGEBRA (independent of the Groebner run).

For FIXED A56, A67 the 81 equations

    D[a][b] A67[c][d] + E[a][d] A56[b][c] = 0        (a,b,c,d in {0,1,2})

are LINEAR in the 18 unknowns (D, E).  Step A says: if all 18 cells of
A56, A67 are nonzero and vertex 6 does NOT factor (i.e. the 3x6 matrix M6
with row c = (A56[0][c],A56[1][c],A56[2][c],A67[c][0],A67[c][1],A67[c][2])
has rank >= 2), then the solution space is ZERO.  And if vertex 6 DOES
factor the solution space is nonzero (so the dichotomy is sharp, not
vacuous).  Both directions are checked here on exact rational instances,
plus the structured near-miss families.
"""
from __future__ import annotations
import os, sys, json, itertools
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))


def nullity(rows, ncols):
    """exact rank/nullity over Q"""
    rows = [list(map(Fraction, r)) for r in rows]
    rank = 0
    piv = 0
    for c in range(ncols):
        sel = None
        for i in range(rank, len(rows)):
            if rows[i][c]:
                sel = i
                break
        if sel is None:
            continue
        rows[rank], rows[sel] = rows[sel], rows[rank]
        pv = rows[rank][c]
        rows[rank] = [v / pv for v in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][c]:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return ncols - rank


def system(A56, A67):
    rows = []
    for a, b, c, d in itertools.product(range(3), repeat=4):
        r = [0] * 18
        r[3 * a + b] += A67[c][d]           # D[a][b]
        r[9 + 3 * a + d] += A56[b][c]       # E[a][d]
        rows.append(r)
    return rows


def rank_M6(A56, A67):
    rows = [[A56[0][c], A56[1][c], A56[2][c],
             A67[c][0], A67[c][1], A67[c][2]] for c in range(3)]
    return 3 - nullity([list(map(Fraction, r)) for r in
                        [[rows[i][j] for i in range(3)] for j in range(6)]], 3)


def lcg(seed):
    s = seed
    while True:
        s = (1103515245 * s + 12345) % (1 << 31)
        yield s


def main():
    res = {"generic": [], "factoring": [], "rank1_A56_only": []}
    # (i) generic A56, A67 (vertex 6 does NOT factor) -> nullity must be 0
    for seed in range(1, 41):
        r = lcg(seed)
        def rn():
            return Fraction((next(r) % 17) - 8 or 5, (next(r) % 4) + 1)
        A56 = [[rn() for _ in range(3)] for _ in range(3)]
        A67 = [[rn() for _ in range(3)] for _ in range(3)]
        if any(v == 0 for M in (A56, A67) for row in M for v in row):
            continue
        res["generic"].append(dict(rank_M6=rank_M6(A56, A67),
                                   nullity=nullity(system(A56, A67), 18)))
    # (ii) vertex 6 factors: A56 = beta (x) gamma, A67 = gamma (x) k
    for seed in range(1, 21):
        r = lcg(seed * 7 + 1)
        def rn():
            return Fraction((next(r) % 17) - 8 or 5, (next(r) % 4) + 1)
        beta = [rn() for _ in range(3)]
        gam = [rn() for _ in range(3)]
        kk = [rn() for _ in range(3)]
        A56 = [[beta[i] * gam[j] for j in range(3)] for i in range(3)]
        A67 = [[gam[i] * kk[j] for j in range(3)] for i in range(3)]
        if any(v == 0 for M in (A56, A67) for row in M for v in row):
            continue
        res["factoring"].append(dict(rank_M6=rank_M6(A56, A67),
                                     nullity=nullity(system(A56, A67), 18)))
    # (iii) NEAR MISS: A56 rank 1 and A67 rank 1 but 6-vectors NOT parallel
    for seed in range(1, 21):
        r = lcg(seed * 13 + 5)
        def rn():
            return Fraction((next(r) % 17) - 8 or 5, (next(r) % 4) + 1)
        beta = [rn() for _ in range(3)]
        gam = [rn() for _ in range(3)]
        gam2 = [rn() for _ in range(3)]
        kk = [rn() for _ in range(3)]
        A56 = [[beta[i] * gam[j] for j in range(3)] for i in range(3)]
        A67 = [[gam2[i] * kk[j] for j in range(3)] for i in range(3)]
        if any(v == 0 for M in (A56, A67) for row in M for v in row):
            continue
        res["rank1_A56_only"].append(
            dict(rank_M6=rank_M6(A56, A67),
                 nullity=nullity(system(A56, A67), 18)))
    for k, v in res.items():
        print("%-16s instances=%d  rank(M6) values=%s  nullity values=%s"
              % (k, len(v), sorted(set(x["rank_M6"] for x in v)),
                 sorted(set(x["nullity"] for x in v))))
    ok = (all(x["nullity"] == 0 for x in res["generic"])
          and all(x["nullity"] > 0 for x in res["factoring"])
          and all(x["nullity"] == 0 for x in res["rank1_A56_only"]))
    print("STEP A dichotomy consistent on all instances:", ok)
    res["verdict"] = ok
    json.dump(res, open(os.path.join(HERE, "results_stepA_lin.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()

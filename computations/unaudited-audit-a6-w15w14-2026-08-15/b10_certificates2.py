#!/usr/bin/env python3
"""AUDIT A6-B10: wider rational hunt for the 3 witness pairs whose rank-one
witness was not found in the small integer box.

WLOG normalisation: the witness condition is invariant under u -> lam u and
v -> mu v (E_w is bihomogeneous, and s*k00*k11*k22 != 0 only gets rescaled),
and u0 v0 = K_00 != 0 forces u0 != 0 != v0, so we may set u0 = v0 = 1 and
search u = (1,a,b), v = (1,c,d) over an integer grid (which, after clearing
denominators, covers all rationals of the corresponding heights).
"""
from __future__ import annotations

from fractions import Fraction
import json
import sys

HERE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a6-w15w14-2026-08-15")
P2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-p2-2026-08-15")
sys.path.insert(0, HERE)
import b10_core as B  # noqa: E402

TARGETS = [(1002, (2, 5)), (1005, (0, 4)), (1008, (0, 5))]
GRID = [x for x in range(-6, 7) if x != 0]


def hunt(pd):
    p, q, U = pd.p, pd.q, pd.U
    # integer/Fraction block columns
    Mp = {a: [[B.block(pd.blocks, p, a, i, c) for c in range(3)]
              for i in range(3)] for a in U}
    Mq = {a: [[B.block(pd.blocks, q, a, j, c) for c in range(3)]
              for j in range(3)] for a in U}
    Apq = [[B.block(pd.blocks, p, q, i, j) for j in range(3)] for i in range(3)]
    matchings = B.matchings_of(U)
    words = pd.words
    pos = pd.pos
    for a1 in GRID:
        for b1 in GRID:
            u = [Fraction(1), Fraction(a1), Fraction(b1)]
            alpha = {a: [sum(u[i] * Mp[a][i][c] for i in range(3))
                         for c in range(3)] for a in U}
            for c1 in GRID:
                for d1 in GRID:
                    v = [Fraction(1), Fraction(c1), Fraction(d1)]
                    sval = sum(u[i] * Apq[i][j] * v[j]
                               for i in range(3) for j in range(3))
                    if sval == 0:
                        continue
                    beta = {a: [sum(v[j] * Mq[a][j][c] for j in range(3))
                                for c in range(3)] for a in U}
                    good = True
                    for w in words:
                        tot = 0
                        for (e, f) in matchings:
                            ra = (alpha[e[0]][w[pos[e[0]]]]
                                  * beta[e[1]][w[pos[e[1]]]]
                                  + alpha[e[1]][w[pos[e[1]]]]
                                  * beta[e[0]][w[pos[e[0]]]])
                            rb = (alpha[f[0]][w[pos[f[0]]]]
                                  * beta[f[1]][w[pos[f[1]]]]
                                  + alpha[f[1]][w[pos[f[1]]]]
                                  * beta[f[0]][w[pos[f[0]]]])
                            tot += ra * rb
                        if tot != 0:
                            good = False
                            break
                    if good:
                        return u, v, sval
    return None


def main():
    p2 = json.load(open(P2 + "/results_a.json"))
    modes = {r["seed"]: r["mode"] for r in p2["results"]}
    out = []
    for seed, pq in TARGETS:
        pd = B.Pair(B.gen_source(seed, modes[seed]), pq[0], pq[1])
        res = hunt(pd)
        if res is None:
            print(f"{seed} {pq}: no rational rank-one witness of height <= 6 "
                  f"(Singular says YES over C)")
            out.append({"seed": seed, "pair": list(pq), "certificate": None})
            continue
        u, v, sval = res
        # full re-verification against the 81 stored quadrics
        K = [u[i] * v[j] for i in range(3) for j in range(3)]
        ok = all(sum(c * K[m] * K[n] for (m, n), c in Q.items()) == 0
                 for Q in pd.quadrics)
        kap = [K[0], K[4], K[8]]
        print(f"{seed} {pq}: u={[str(x) for x in u]} v={[str(x) for x in v]} "
              f"s={sval} kappas={[str(x) for x in kap]} "
              f"all-81-quadrics-vanish={ok}")
        out.append({"seed": seed, "pair": list(pq),
                    "certificate": {"u": [str(x) for x in u],
                                    "v": [str(x) for x in v],
                                    "s": str(sval),
                                    "kappas": [str(x) for x in kap],
                                    "verified_all_quadrics": ok}})
    json.dump(out, open(HERE + "/b10_certificates2.json", "w"), indent=1)


if __name__ == "__main__":
    main()

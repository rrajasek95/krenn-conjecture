#!/usr/bin/env python3
"""AUDIT A6-B10: Singular-free point certificate for the rank-one witness
verdicts, by exhaustive search over a small finite field.

For a prime p, search u = (1,a,b), v = (1,c,d) in F_p and check
   E_w(u (x) v) = 0 (mod p) for all 81 words,  u_i v_i != 0,  u^T A v != 0.
A hit proves the rank-one witness system has a solution over F_p-bar, hence
1 is NOT in the Rabinowitsch ideal mod p, hence (barring bad reduction at p)
not over Q either -- i.e. the "rank-one witness exists" verdict, obtained
with no Groebner basis at all.

Run on the 5 featured WITNESS pairs, on the one pair with no low-height
rational point, and -- as a negative control -- on the 5 featured BLOCKED
pairs, where NO hit may ever be found for any p.
"""
from __future__ import annotations

import json
import sys

HERE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a6-w15w14-2026-08-15")
P2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-p2-2026-08-15")
sys.path.insert(0, HERE)
import b10_core as B  # noqa: E402

WIT = [(1002, (2, 5)), (1005, (0, 5)), (1005, (4, 5)), (1008, (0, 3)),
       (1008, (1, 2)), (1005, (0, 4))]
BLK = [(1000, (0, 1)), (1001, (2, 3)), (1003, (1, 4)), (1006, (0, 5)),
       (1007, (3, 4))]
PRIMES = [11, 13, 17]


def to_fp(x, p):
    return (x.numerator % p) * pow(x.denominator % p, p - 2, p) % p


def search(pd, p):
    U, pos = pd.U, pd.pos
    Mp = {a: [[to_fp(B.block(pd.blocks, pd.p, a, i, c), p) for c in range(3)]
              for i in range(3)] for a in U}
    Mq = {a: [[to_fp(B.block(pd.blocks, pd.q, a, j, c), p) for c in range(3)]
              for j in range(3)] for a in U}
    Apq = [[to_fp(B.block(pd.blocks, pd.p, pd.q, i, j), p) for j in range(3)]
           for i in range(3)]
    matchings = B.matchings_of(U)
    words = pd.words
    for a1 in range(1, p):
        for b1 in range(1, p):
            u = (1, a1, b1)
            alpha = {a: [sum(u[i] * Mp[a][i][c] for i in range(3)) % p
                         for c in range(3)] for a in U}
            for c1 in range(1, p):
                for d1 in range(1, p):
                    v = (1, c1, d1)
                    sval = sum(u[i] * Apq[i][j] * v[j] for i in range(3)
                               for j in range(3)) % p
                    if sval == 0:
                        continue
                    beta = {a: [sum(v[j] * Mq[a][j][c] for j in range(3)) % p
                                for c in range(3)] for a in U}
                    ok = True
                    for w in words:
                        tot = 0
                        for (e, f) in matchings:
                            ra = (alpha[e[0]][w[pos[e[0]]]]
                                  * beta[e[1]][w[pos[e[1]]]]
                                  + alpha[e[1]][w[pos[e[1]]]]
                                  * beta[e[0]][w[pos[e[0]]]]) % p
                            rb = (alpha[f[0]][w[pos[f[0]]]]
                                  * beta[f[1]][w[pos[f[1]]]]
                                  + alpha[f[1]][w[pos[f[1]]]]
                                  * beta[f[0]][w[pos[f[0]]]]) % p
                            tot += ra * rb
                        if tot % p != 0:
                            ok = False
                            break
                    if ok:
                        return {"p": p, "u": list(u), "v": list(v),
                                "s": sval}
    return None


def main():
    p2 = json.load(open(P2 + "/results_a.json"))
    modes = {r["seed"]: r["mode"] for r in p2["results"]}
    out = []
    for label, group in (("witness", WIT), ("blocked", BLK)):
        for seed, pq in group:
            pd = B.Pair(B.gen_source(seed, modes[seed]), pq[0], pq[1])
            hit = None
            for p in PRIMES:
                hit = search(pd, p)
                if hit:
                    break
            out.append({"class": label, "seed": seed, "pair": list(pq),
                        "modp_point": hit})
            print(f"[{label}] {seed} {pq}: {hit}", flush=True)
    wit_ok = all(r["modp_point"] for r in out if r["class"] == "witness")
    blk_ok = all(r["modp_point"] is None for r in out if r["class"] == "blocked")
    print(f"\nwitness pairs all have a mod-p rank-one point: {wit_ok}")
    print(f"blocked pairs have NO mod-p rank-one point (primes {PRIMES}): "
          f"{blk_ok}")
    json.dump({"witness_all_have_point": wit_ok,
               "blocked_none_have_point": blk_ok, "primes": PRIMES,
               "rows": out},
              open(HERE + "/b10_modp_point.json", "w"), indent=1)


if __name__ == "__main__":
    main()

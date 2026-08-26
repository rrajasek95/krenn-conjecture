#!/usr/bin/env python3
"""W21-M2-SING: INDEPENDENT EXHAUSTIVE check of THEOREM W21-M2 over F_5.

F_3 is USELESS for this problem: 4! = 24 and the 3x3 permanent multiplicity 6
are both 0 mod 3, so per vanishes on tuples where it does not vanish over Q
(verified: V = span{(1,1,1,0),(0,0,0,1)} gives per values {0,6}).  F_5 keeps
24 and 6 invertible.

ALGORITHM.  per vanishes on V_0 x V_1 x V_2 x V_3  iff  for every
(v_2,v_3) in V_2 x V_3 the symmetric zero-diagonal matrix
A(v_2,v_3)[i][k] = v_2[p]v_3[q] + v_2[q]v_3[p]  ({p,q} = complement of {i,k})
vanishes on V_0 x V_1, i.e. colspace(A) is inside Ann(V_0) and rowspace(A) is
inside Ann(V_1).  Since dim V_0 >= 2, dim Ann(V_0) <= 2, so EVERY A must have
rank <= 2.  That is a cheap filter on the pair (V_2,V_3); the survivors are
then checked completely (all V_0, V_1).
"""
from __future__ import annotations

import json
import sys
import time
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

P = int(sys.argv[1]) if len(sys.argv) > 1 else 5
COORDS = (0, 1, 2, 3)
BIJ = tuple(permutations(COORDS))


def rank_basis(rows):
    m = [list(r) for r in rows]
    r = 0
    for c in range(4):
        piv = None
        for i in range(r, len(m)):
            if m[i][c] % P:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = pow(m[r][c], P - 2, P)
        m[r] = [(x * inv) % P for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] % P:
                f = m[i][c]
                m[i] = [(a - f * b) % P for a, b in zip(m[i], m[r])]
        r += 1
        if r == 4:
            break
    return r, [tuple(x) for x in m[:r]]


def all_subspaces():
    """RREF enumeration of every subspace of F_P^4 of dim 2 or 3."""
    out = []
    for d in (2, 3):
        for piv in combinations(COORDS, d):
            free = []
            for r in range(d):
                for c in COORDS:
                    if c > piv[r] and c not in piv:
                        free.append((r, c))
            for vals in product(range(P), repeat=len(free)):
                m = [[0] * 4 for _ in range(d)]
                for r in range(d):
                    m[r][piv[r]] = 1
                for (rc, v) in zip(free, vals):
                    m[rc[0]][rc[1]] = v
                b = tuple(tuple(r) for r in m)
                if not any(all(u[i] == 0 for u in b) for i in COORDS):
                    out.append((b, d))
    return out


def Amat(v2, v3):
    A = [[0] * 4 for _ in range(4)]
    for (i, k) in combinations(COORDS, 2):
        p, q = sorted(set(COORDS) - {i, k})
        A[i][k] = A[k][i] = (v2[p] * v3[q] + v2[q] * v3[p]) % P
    return A


def matrank(A):
    return rank_basis(A)[0]


def per4(vs):
    t = 0
    for s in BIJ:
        t = (t + vs[0][s[0]] * vs[1][s[1]] * vs[2][s[2]] * vs[3][s[3]]) % P
    return t % P


if __name__ == "__main__":
    t0 = time.time()
    subs = all_subspaces()
    byb = {b: d for b, d in subs}
    print("F_%d: %d subspaces of dim 2 or 3 outside every coordinate "
          "hyperplane" % (P, len(subs)), flush=True)
    # For per to vanish, colspace(A(v2,v3)) must sit inside Ann(V_0) for every
    # basis pair, so the TOTAL column span W of all those A must have rank <=2,
    # and then V_0, V_1 are both inside W^perp.
    cex = []
    npairs = fil = full = 0
    for i2 in range(len(subs)):
        b2, d2 = subs[i2]
        for i3 in range(i2, len(subs)):
            b3, d3 = subs[i3]
            npairs += 1
            cols = []
            for u2 in b2:
                for u3 in b3:
                    A = Amat(u2, u3)
                    cols.extend(A)
            r, _ = rank_basis(cols)
            if r > 2:
                continue
            fil += 1
            # W^perp
            rW, bW = rank_basis(cols)
            perp = []
            for v in product(range(P), repeat=4):
                if any(v) and all(sum(a * b for a, b in zip(w, v)) % P == 0
                                  for w in bW):
                    perp.append(v)
            rp, bp = rank_basis(perp) if perp else (0, [])
            if rp < 2:
                continue
            cands = [b for b, d in subs
                     if all(any(all((x - y) % P == 0 for x, y in zip(u, pv))
                                for pv in perp) for u in b)]
            for b0 in cands:
                for b1 in cands:
                    full += 1
                    if all(per4((u0, u1, u2, u3)) == 0 for u0 in b0
                           for u1 in b1 for u2 in b2 for u3 in b3):
                        cex.append((b0, b1, b2, b3))
    print("  pairs (V_2,V_3): %d ; passing the rank(W)<=2 filter: %d ; "
          "full 4-tuple checks: %d" % (npairs, fil, full), flush=True)
    print("  COUNTEREXAMPLES over F_%d: %d   (%.1fs)"
          % (P, len(cex), time.time() - t0), flush=True)
    for c in cex[:4]:
        print("   ", c)
    json.dump({"p": P, "nsubs": len(subs), "pairs": npairs, "filtered": fil,
               "full_checks": full, "counterexamples": len(cex),
               "examples": [str(c) for c in cex[:4]]},
              open("results_ff%d.json" % P, "w"), indent=1)

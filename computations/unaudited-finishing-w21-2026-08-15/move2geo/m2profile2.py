#!/usr/bin/env python3
"""W21-M2-GEO step 5b: FAST exhaustive classification of the per-null
quadruples, recording the FULL coincidence graph of every slot.

Algorithm (complete, no sampling).  Fix (V_6,V_7).  For u in P^3 the condition
per == 0 on span(u) x V_5 x V_6 x V_7 is LINEAR in the second slot:
        N(u) = { w : P_6^T B_{u,w} P_7 = 0 }.
Any solution must have N(u) != 0 for every u in V_4, so V_4 is a subspace
contained in the cone U = {u : N(u) != 0}; and then V_5 <= intersection of the
N(u).  Enumerating the subspaces inside U is cheap because U is small.
Slot 6 is taken in a (torus x S_4)-orbit representative -- legitimate because
the per == 0 condition is symmetric in the four slots.

Output: for every solution, the tuple of (dim V_j, coincidence graph C(V_j)).
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PERM4 = list(permutations(range(4)))
PAIRS = list(combinations(range(4), 2))


def make_field(q):
    inv = [0] * q
    for a in range(1, q):
        for b in range(1, q):
            if a * b % q == 1:
                inv[a] = b
    return inv


def rref(rows, q, inv):
    M = [list(r) for r in rows]
    if not M:
        return ()
    n = len(M[0])
    r = 0
    for c in range(n):
        p = None
        for i in range(r, len(M)):
            if M[i][c]:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        f = inv[M[r][c]]
        M[r] = [(x * f) % q for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                g = M[i][c]
                M[i] = [(x - g * y) % q for x, y in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return tuple(tuple(row) for row in M[:r] if any(row))


def perp(basis, q, inv):
    R = rref(basis, q, inv)
    if not R:
        return tuple(tuple(1 if k == i else 0 for k in range(4))
                     for i in range(4))
    piv = [next(c for c in range(4) if row[c]) for row in R]
    free = [c for c in range(4) if c not in piv]
    out = []
    for f in free:
        v = [0] * 4
        v[f] = 1
        for row, p in zip(R, piv):
            v[p] = (-row[f]) % q
        out.append(tuple(v))
    return rref(out, q, inv)


def meet(A, B, q, inv):
    return perp(list(perp(A, q, inv)) + list(perp(B, q, inv)), q, inv)


def valid(V):
    return bool(V) and all(any(row[r] for row in V) for r in range(4))


def cgraph(V, q, inv):
    return tuple((r, t) for r, t in PAIRS
                 if len(rref([(row[r], row[t]) for row in V], q, inv)) <= 1)


def Bmat(u, w, q):
    B = [[0] * 4 for _ in range(4)]
    for k in range(4):
        for l in range(4):
            if k != l:
                p, s = [t for t in range(4) if t not in (k, l)]
                B[k][l] = (u[p] * w[s] + u[s] * w[p]) % q
    return B


def per4(cols, q):
    return sum(cols[0][p[0]] * cols[1][p[1]] * cols[2][p[2]] * cols[3][p[3]]
               for p in PERM4) % q


def per_null(Vs, q):
    return all(per4(c, q) == 0 for c in product(*Vs))


def all_subspaces(q, inv):
    pts = [v for v in product(range(q), repeat=4) if any(v)]
    d1 = sorted({rref([v], q, inv) for v in pts})
    d2 = sorted({rref([a, b], q, inv) for a in pts for b in pts
                 if len(rref([a, b], q, inv)) == 2})
    d3 = sorted({perp(list(V), q, inv) for V in d1})
    return d1, d2, d3


def main(q=5, only_dim2=False):
    inv = make_field(q)
    d1, d2, d3 = all_subspaces(q, inv)
    P3 = [V[0] for V in d1]
    allV = [V for V in (d1 + d2 + d3) if valid(V)]
    G = [((1,) + d, p) for d in product(range(1, q), repeat=3)
         for p in permutations(range(4))]

    def act(g, V):
        dd, p = g
        return rref([tuple(dd[k] * row[p[k]] % q for k in range(4))
                     for row in V], q, inv)

    seen, reps = set(), []
    for V in allV:
        if V in seen:
            continue
        seen |= {act(g, V) for g in G}
        reps.append(V)
    print("q=%d valid subspaces %d, orbit reps %d %s"
          % (q, len(allV), len(reps), [len(r) for r in reps]), flush=True)

    sols = {}
    examples = {}
    # precompute the projective point set of every subspace
    def points_of(V):
        pts = set()
        k = len(V)
        for coef in product(range(q), repeat=k):
            if not any(coef):
                continue
            v = tuple(sum(coef[i] * V[i][m] for i in range(k)) % q
                      for m in range(4))
            pts.add(rref([v], q, inv)[0])
        return frozenset(pts)

    PTS = {V: points_of(V) for V in (d1 + d2 + d3)}
    SUB2 = [V for V in d2]
    SUB3 = [V for V in d3]
    for V6 in reps:
        for V7 in allV:
            pairs67 = [(r6, r7) for r6 in V6 for r7 in V7]
            # gamma[t][(p,s)] : r6^T B_{u,w} r7 = sum_{p<s} gamma_ps m_ps(u,w)
            gam = []
            for (r6, r7) in pairs67:
                g = {}
                for p, s in combinations(range(4), 2):
                    k, l = [z for z in range(4) if z not in (p, s)]
                    g[(p, s)] = (r6[k] * r7[l] + r6[l] * r7[k]) % q
                    g[(s, p)] = g[(p, s)]
                gam.append(g)
            NU = {}
            for u in P3:
                rows = []
                for g in gam:
                    rows.append(tuple(sum(g[(p, m)] * u[p]
                                          for p in range(4) if p != m) % q
                                      for m in range(4)))
                N = perp(rows, q, inv)
                if N:
                    NU[u] = N
            if not NU:
                continue
            NUset = frozenset(NU)
            cands = [rref([u], q, inv) for u in NU]
            for V in SUB2 + SUB3:
                if PTS[V] <= NUset:
                    cands.append(V)
            for V4 in cands:
                if not valid(V4):
                    continue
                V5 = None
                for row in V4:
                    key = rref([row], q, inv)[0]
                    V5 = NU[key] if V5 is None else meet(V5, NU[key], q, inv)
                    if not V5:
                        break
                if not V5 or not valid(V5):
                    continue
                if only_dim2 and (len(V4) != 2 or len(V6) != 2 or
                                  len(V7) != 2):
                    continue
                assert per_null([V4, V5, V6, V7], q), "inconsistent"
                sig = tuple(sorted(((len(V), cgraph(V, q, inv))
                                    for V in (V4, V5, V6, V7)),
                                   key=lambda z: (z[0], len(z[1]), z[1])))
                sols[sig] = sols.get(sig, 0) + 1
                if sig not in examples:
                    examples[sig] = [[list(r) for r in V]
                                     for V in (V4, V5, V6, V7)]
        print("   V6 rep dim %d done, %d signature classes"
              % (len(V6), len(sols)), flush=True)

    print("q=%d  SIGNATURES (dim, coincidence graph) of per-null quadruples "
          "with no V_j in a coordinate hyperplane [V_5 maximal]:" % q)
    for sig in sorted(sols, key=lambda s: ([z[0] for z in s],
                                           [len(z[1]) for z in s])):
        print("   %s : %d" % (str([(d, list(g)) for d, g in sig]), sols[sig]))
    res = {"q": q, "signatures": {str(k): v for k, v in sols.items()},
           "examples": {str(k): v for k, v in examples.items()}}
    json.dump(res, open(os.path.join(HERE, "results_profile2_q%d.json" % q),
                        "w"), indent=1, default=str)
    return sols


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5)

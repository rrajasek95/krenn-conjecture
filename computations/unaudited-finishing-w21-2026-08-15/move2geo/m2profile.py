#!/usr/bin/env python3
"""W21-M2-GEO step 5: EXHAUSTIVE CLASSIFICATION of the per-null quadruples.

THE GATE.  For one L-free word x the whole content of its 81 permanent
equations is
        per == 0 identically on V_4 x V_5 x V_6 x V_7,
        V_j = column span of M_j^x  <=  C^4,
and the template guarantees  pi_r(V_j) != 0 for every r in L  ("no V_j inside a
coordinate hyperplane": a whole ROW of M_j^x would have to vanish, but every
cross block has at most one dead cell).

This module classifies EXHAUSTIVELY, over F_q (q = 5, 7 -- structured strata
per ledger 12; q > 3 so that 4! is invertible), every such quadruple, and
records the dimension profile and the COINCIDENCE GRAPH
        C(V) = { {r,t} : dim pi_{rt}(V) <= 1 }
        ( {r,t} in C(V)  <=>  rows r,t of M are proportional
                          <=>  the transversal points r and t COINCIDE ).
Completeness: the condition is symmetric in the four slots, so one slot may be
taken in a representative of the (torus x S_4)-orbit; for the other three the
sweep is over ALL valid subspaces; V_5 is taken MAXIMAL (any valid subspace of
a valid V_5 is again a solution, so no solution is missed).
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PERM4 = list(permutations(range(4)))
FULL = tuple(tuple(1 if k == i else 0 for k in range(4)) for i in range(4))


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
        return FULL
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


def meet(A, Bs, q, inv):
    return perp(list(perp(A, q, inv)) + list(perp(Bs, q, inv)), q, inv)


def subspaces(q, inv):
    pts = [v for v in product(range(q), repeat=4) if any(v)]
    d1 = sorted({rref([v], q, inv) for v in pts})
    d2 = sorted({rref([a, b], q, inv) for a in pts for b in pts
                 if len(rref([a, b], q, inv)) == 2})
    d3 = sorted({perp(list(V), q, inv) for V in d1})
    return {1: d1, 2: d2, 3: d3}


def valid(V):
    return bool(V) and all(any(row[r] for row in V) for r in range(4))


def coincidence_graph(V, q, inv):
    return tuple((r, t) for r, t in combinations(range(4), 2)
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
    for c in product(*Vs):
        if per4(c, q) != 0:
            return False
    return True


def group_elements(q):
    return [((1,) + d, p) for d in product(range(1, q), repeat=3)
            for p in permutations(range(4))]


def act(g, V, q, inv):
    dd, p = g
    return rref([tuple(dd[k] * row[p[k]] % q for k in range(4)) for row in V],
                q, inv)


def orbit_reps(lst, q, inv, G):
    seen, reps = set(), []
    for V in lst:
        if V in seen:
            continue
        seen |= {act(g, V, q, inv) for g in G}
        reps.append(V)
    return reps


def main(q=5):
    inv = make_field(q)
    S = subspaces(q, inv)
    allV = [V for d in (1, 2, 3) for V in S[d] if valid(V)]
    G = group_elements(q)
    reps = orbit_reps(allV, q, inv, G)
    print("q=%d  valid subspaces %d ; |G| %d ; orbit reps %d %s"
          % (q, len(allV), len(G), len(reps), [len(r) for r in reps]),
          flush=True)
    P3 = [V[0] for V in S[1]]
    found, examples = {}, {}
    for V6 in reps:
        for V7 in allV:
            # N(u) = { w : P6^T B_{u,w} P7 = 0 }
            N = {}
            pairs = [(r6, r7) for r6 in V6 for r7 in V7]
            for u in P3:
                cols = []
                for wb in range(4):
                    ew = tuple(1 if k == wb else 0 for k in range(4))
                    B = Bmat(u, ew, q)
                    cols.append([sum(r6[k] * B[k][l] * r7[l]
                                     for k in range(4) for l in range(4)) % q
                                 for (r6, r7) in pairs])
                rows = [tuple(cols[wb][t] for wb in range(4))
                        for t in range(len(pairs))]
                N[u] = perp(rows, q, inv)      # { w : all equations vanish }
            for V4 in allV:
                V5 = FULL
                for row in V4:
                    key = rref([row], q, inv)[0]
                    V5 = meet(V5, N[key], q, inv)
                    if not V5:
                        break
                if not valid(V5):
                    continue
                assert per_null([V4, V5, V6, V7], q), "internal inconsistency"
                prof = tuple(sorted([len(V4), len(V5), len(V6), len(V7)]))
                cg = tuple(sorted(len(coincidence_graph(V, q, inv))
                                  for V in (V4, V5, V6, V7)))
                key2 = (prof, cg)
                found[key2] = found.get(key2, 0) + 1
                if key2 not in examples:
                    examples[key2] = [[list(r) for r in V]
                                      for V in (V4, V5, V6, V7)]
        print("   ...V6 rep dim %d done (%d classes so far)"
              % (len(V6), len(found)), flush=True)
    print("q=%d  per-null quadruples, NO V_j in a coordinate hyperplane, "
          "V_5 maximal:" % q)
    for key in sorted(found):
        print("   dims %s  #coincidence-edges %s : %d" % (key[0], key[1],
                                                          found[key]))
    res = {"q": q, "n_valid_subspaces": len(allV), "n_orbit_reps": len(reps),
           "profiles": {str(k): v for k, v in found.items()},
           "examples": {str(k): v for k, v in examples.items()}}
    json.dump(res, open(os.path.join(HERE, "results_profile_q%d.json" % q),
                        "w"), indent=1, default=str)
    return res


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5)

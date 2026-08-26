#!/usr/bin/env python3
"""W21-M2-GEO step 9: TARGETED exhaustive search -- an independent re-derivation
of the kill, and its cross-characteristic check.

For a given L-free word the dead cells restrict, at each site j, the coincidence
graph C(V_j) to a subgraph of the allowed graph A_j.  This script searches
EXHAUSTIVELY over F_q for a per-null quadruple obeying those restrictions --
without going through the signature list of m2profile2.py, so it is a genuinely
independent check of the same statement.

Controls built in:
  * relaxing the restrictions to "everything allowed" MUST find solutions;
  * a word known to survive MUST be found to survive.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import m2profile2 as P                                              # noqa: E402

PAIRS = list(combinations(range(4), 2))
FULLG = frozenset(PAIRS)


def subspaces_inside(V, q, inv, cache={}):
    """all nonzero subspaces of the subspace V."""
    key = (V, q)
    if key in cache:
        return cache[key]
    k = len(V)
    pts = set()
    for coef in product(range(q), repeat=k):
        if any(coef):
            v = tuple(sum(coef[i] * V[i][m] for i in range(k)) % q
                      for m in range(4))
            pts.add(P.rref([v], q, inv)[0])
    out = {P.rref([p], q, inv) for p in pts}
    for a, b in combinations(sorted(pts), 2):
        W = P.rref([a, b], q, inv)
        if len(W) == 2:
            out.add(W)
    for a, b, c in combinations(sorted(pts), 3):
        W = P.rref([a, b, c], q, inv)
        if len(W) == 3:
            out.add(W)
    out.add(V)
    cache[key] = sorted(out)
    return cache[key]


def search(q, allowed, verbose=True):
    """allowed = list of 4 frozensets of pairs (site order 4,5,6,7).
    Returns a witness quadruple or None."""
    inv = P.make_field(q)
    d1, d2, d3 = P.all_subspaces(q, inv)
    P3 = [V[0] for V in d1]
    allV = [V for V in (d1 + d2 + d3) if P.valid(V)]
    CG = {V: frozenset(P.cgraph(V, q, inv)) for V in allV}
    Lst = [[V for V in allV if CG[V] <= allowed[s]] for s in range(4)]
    if verbose:
        print("q=%d candidate subspaces per site: %s"
              % (q, [len(t) for t in Lst]), flush=True)
    torus = [(1,) + d for d in product(range(1, q), repeat=3)]

    def act(dd, V):
        return P.rref([tuple(dd[k] * row[k] % q for k in range(4))
                       for row in V], q, inv)

    seen, reps6 = set(), []
    for V in Lst[2]:                       # site 6 reduced by the torus
        if V in seen:
            continue
        seen |= {act(dd, V) for dd in torus}
        reps6.append(V)
    if verbose:
        print("q=%d site-6 torus orbit representatives: %d"
              % (q, len(reps6)), flush=True)
    PTS = {}
    for V in allV:
        s = set()
        for coef in product(range(q), repeat=len(V)):
            if any(coef):
                v = tuple(sum(coef[i] * V[i][m] for i in range(len(V)))
                          % q for m in range(4))
                s.add(P.rref([v], q, inv)[0])
        PTS[V] = frozenset(s)
    for ii, V6 in enumerate(reps6):
        for V7 in Lst[3]:
            gam = []
            for r6 in V6:
                for r7 in V7:
                    g = {}
                    for p, s in PAIRS:
                        k, l = [z for z in range(4) if z not in (p, s)]
                        g[(p, s)] = (r6[k] * r7[l] + r6[l] * r7[k]) % q
                        g[(s, p)] = g[(p, s)]
                    gam.append(g)
            NU = {}
            for u in P3:
                rows = [tuple(sum(g[(p, m)] * u[p]
                                  for p in range(4) if p != m) % q
                              for m in range(4)) for g in gam]
                N = P.perp(rows, q, inv)
                if N:
                    NU[u] = N
            if not NU:
                continue
            NUset = frozenset(NU)
            for V4 in Lst[0]:
                if not PTS[V4] <= NUset:
                    continue
                V5m = None
                for row in V4:
                    key = P.rref([row], q, inv)[0]
                    V5m = NU[key] if V5m is None else P.meet(V5m, NU[key],
                                                             q, inv)
                    if not V5m:
                        break
                if not V5m:
                    continue
                for V5 in subspaces_inside(V5m, q, inv):
                    if not P.valid(V5) or not CG[V5] <= allowed[1]:
                        continue
                    assert P.per_null([V4, V5, V6, V7], q)
                    return [[list(r) for r in V] for V in (V4, V5, V6, V7)]
        if verbose:
            print("   site-6 rep %d/%d done" % (ii + 1, len(reps6)),
                  flush=True)
    return None


def allowed_for_word(x):
    import m2kill as K
    return [K.allowed_R(x, j) for j in (4, 5, 6, 7)]


def main():
    import m2kill as K
    res = {"_header": "UNAUDITED W21-M2-GEO targeted exhaustive search."}
    qs = [int(a) for a in sys.argv[1:]] or [5]
    words = [(1, 1, 2, 2), (1, 0, 2, 2), (1, 0, 0, 2)]
    for q in qs:
        for x in words:
            al = allowed_for_word(x)
            print("=== q=%d  word %s  allowed %s" % (q, x,
                                                     [sorted(a) for a in al]),
                  flush=True)
            w = search(q, al)
            print("q=%d word %s : %s" % (q, x,
                                         "SURVIVES (witness found)" if w
                                         else "NO per-null quadruple EXISTS"),
                  flush=True)
            res["q%d_%s" % (q, "".join(map(str, x)))] = w if w else "EMPTY"
        # CONTROL: no restriction at all must produce a witness
        w = search(q, [FULLG] * 4, verbose=False)
        print("q=%d CONTROL (no restriction): %s (want a witness)"
              % (q, "witness" if w else "EMPTY -- BUG"), flush=True)
        res["q%d_control_unrestricted" % q] = w if w else "EMPTY"
    json.dump(res, open(os.path.join(HERE, "results_targeted.json"), "w"),
              indent=1, default=str)
    print("done")


if __name__ == "__main__":
    main()

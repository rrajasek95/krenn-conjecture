#!/usr/bin/env python3
"""W21-M2-SING: INDEPENDENT EXHAUSTIVE check of THEOREM W21-M2 over F_3.

Enumerates EVERY subspace of F_3^4 of dimension 2 or 3 that is not contained
in a coordinate hyperplane, and every 4-tuple of them (with V_0 reduced modulo
the coordinate-permutation symmetry of per, which is legitimate because per is
invariant under simultaneous permutation of the four coordinates).  For each
tuple it tests whether per vanishes identically on the product.

This is EXACT but over F_3, so it is strong INDEPENDENT EVIDENCE for the
char-0 theorem, not a proof of it (the proof is the Q-Groebner verification in
m2steps / m2stepBD / m2stepII / m2thm_sweep2).  A counterexample here would
have been an immediate red flag.
"""
from __future__ import annotations

import json
import sys
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

P = 3
COORDS = (0, 1, 2, 3)
BIJ = tuple(permutations(COORDS))


def vecs():
    return [v for v in product(range(P), repeat=4) if any(v)]


def norm(v):
    for a in v:
        if a:
            inv = pow(a, P - 2, P)
            return tuple((x * inv) % P for x in v)
    return v


def rank(rows):
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
    return r, m[:r]


def subspaces(d):
    seen = {}
    V = vecs()
    for combo in combinations(V, d):
        r, basis = rank(combo)
        if r != d:
            continue
        key = tuple(tuple(b) for b in basis)
        seen[key] = key
    return list(seen)


def in_coord_hyperplane(basis):
    return any(all(b[i] == 0 for b in basis) for i in COORDS)


def per4(vs):
    t = 0
    for sig in BIJ:
        p = 1
        for k in range(4):
            p = (p * vs[k][sig[k]]) % P
        t = (t + p) % P
    return t % P


def perm_apply(basis, pi):
    r, b = rank([tuple(v[pi[i]] for i in COORDS) for v in basis])
    return tuple(tuple(x) for x in b)


if __name__ == "__main__":
    subs = []
    for d in (2, 3):
        for b in subspaces(d):
            if not in_coord_hyperplane(b):
                subs.append(b)
    print("F_%d: %d subspaces of dim 2 or 3 not inside a coordinate hyperplane"
          % (P, len(subs)))
    # orbit representatives of V_0 under coordinate permutations
    reps, seen = [], set()
    for b in subs:
        if b in seen:
            continue
        orb = {perm_apply(b, pi) for pi in BIJ}
        seen |= orb
        reps.append(b)
    print("  V_0 orbit representatives under S_4(coords): %d" % len(reps))

    cex = []
    tested = 0
    for b0 in reps:
        for b1 in subs:
            for b2 in subs:
                # linear conditions on v_3 from all basis triples
                rows = []
                for u0 in b0:
                    for u1 in b1:
                        for u2 in b2:
                            f = [0] * 4
                            for sig in BIJ:
                                p = (u0[sig[0]] * u1[sig[1]] * u2[sig[2]]) % P
                                if p:
                                    f[sig[3]] = (f[sig[3]] + p) % P
                            if any(f):
                                rows.append(tuple(f))
                r, _ = rank(rows) if rows else (0, [])
                if 4 - r < 2:
                    continue
                # solution space has dim >= 2: does it contain a valid V_3?
                sol = [v for v in vecs()
                       if all(sum(a * b for a, b in zip(f, v)) % P == 0
                              for f in rows)]
                for b3 in subs:
                    if all(tuple(u) in set(map(tuple, sol)) for u in b3):
                        tested += 1
                        ok = all(per4((u0, u1, u2, u3)) == 0
                                 for u0 in b0 for u1 in b1
                                 for u2 in b2 for u3 in b3)
                        if ok:
                            cex.append((b0, b1, b2, b3))
    print("  candidate tuples fully checked: %d ; COUNTEREXAMPLES: %d"
          % (tested, len(cex)))
    for c in cex[:5]:
        print("   ", c)
    json.dump({"p": P, "nsubs": len(subs), "nreps": len(reps),
               "checked": tested, "counterexamples": len(cex),
               "examples": [str(c) for c in cex[:5]]},
              open("results_ff%d.json" % P, "w"), indent=1)

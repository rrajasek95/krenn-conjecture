#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- Task 2 (R1b): the UNIFORM Perm-K_{2,3} circuit for
BOTH singleton-free families, checked as proof output at many orders.

THEOREM W13.6 (proved in REPORT; this script is its proof-output checker).
Write n = N/2.

  F_n   (n even >= 4, N = 0 mod 4):  put  v = (n-3, n-2, n-1) in X,
                                          u = (2n-2, 2n-1) in Y.
  F'_n  (n odd  >= 5, N = 2 mod 4):  put  v = (n-3, n-2, n-1) in A,
                                          u = (2n-3, 2n-2) in B.

In both cases the six edges v_x u_y all carry colour 0, and for each of the
three pairs {v_x, v_y} the word

    colour 0 on {v_x, v_y, u_1, u_2};
    colour 2 on the two vertices orphaned by deleting v_x, v_y from the
              colour-1 matching, and on the two orphaned in the u-part;
    colour 1 on everything else

has fibre EXACTLY 2 -- the two cross pairings of {v_x,v_y} with {u_1,u_2} --
because colour 1 is a perfect matching (so its induced subgraphs carry at most
one matching), the colour-2 part is two disjoint edges, and colour 0 induces
K_{2,2} on the four marked vertices.  The three difference vectors are

  d_xy = e_{v_x u_1} + e_{v_y u_2} - e_{v_x u_2} - e_{v_y u_1},

and d_{12} + d_{23} + d_{31} = 0 with THREE terms: an odd relation, i.e.
1 = -1.  Hence F_n and F'_n die by O1 for every n, so R1b holds on every
explicitly known singleton-free object at every even N >= 8.

The checker verifies, from the definitions and with exact integer counts:
(a) the six edges are colour 0; (b) each of the three words has fibre size
exactly 2 and the two members are the predicted cross pairings; (c) the three
difference vectors sum to zero, giving a 3-term (odd) relation.
"""

from __future__ import annotations

import json
import sys
from itertools import combinations

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w13_task2_families import family_F, family_Fprime, matchings_of

OUT = {"F": [], "Fprime": []}


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


def predicted_k23(kind, n):
    if kind == "F":
        N, cs = family_F(n)
        v = (n - 3, n - 2, n - 1)
        u = (2 * n - 2, 2 * n - 1)
        # partner of x in the colour-1 matching
        def partner(x):
            return x + 1 if x % 2 == 0 else x - 1
        marks = {}
    else:
        N, cs, marks = family_Fprime(n)
        v = (n - 3, n - 2, n - 1)
        u = (2 * n - 3, 2 * n - 2)
        def partner(x):
            if x == 0:
                return n
            if x == n:
                return 0
            if x < n:
                return x + 1 if x % 2 == 1 else x - 1
            y = x - n
            return x + 1 if y % 2 == 1 else x - 1
    return N, cs, v, u, partner, marks


def fibre_of_word(N, cs, word):
    sets = [set(map(tuple, s)) for s in cs]
    parts = [[x for x in range(N) if word[x] == r] for r in range(3)]
    per = [matchings_of(parts[r], sets[r]) for r in range(3)]
    out = []
    for m0 in per[0]:
        for m1 in per[1]:
            for m2 in per[2]:
                out.append(tuple(sorted(m0 + m1 + m2)))
    return out, [len(p) for p in per]


def check(kind, n):
    N, cs, v, u, partner, marks = predicted_k23(kind, n)
    sets = [set(map(tuple, s)) for s in cs]
    # colour 1 must be a perfect matching of V, and `partner` must describe it
    require(len(sets[1]) == N // 2, ("colour 1 not a perfect matching", n))
    cov = sorted(x for e in sets[1] for x in e)
    require(cov == list(range(N)), ("colour 1 does not cover V", n))
    for x in range(N):
        e = tuple(sorted((x, partner(x))))
        require(e in sets[1], ("partner map wrong", kind, n, x, e))

    # (a) six colour-0 edges
    for x in v:
        for y in u:
            require(tuple(sorted((x, y))) in sets[0],
                    ("(a) missing colour-0 edge", kind, n, x, y))

    diffs = []
    words = []
    for x, y in ((v[0], v[1]), (v[1], v[2]), (v[2], v[0])):
        word = [1] * N
        for z in (x, y, u[0], u[1]):
            word[z] = 0
        orphans = []
        for z in (x, y, u[0], u[1]):
            p = partner(z)
            if p not in (x, y, u[0], u[1]):
                orphans.append(p)
        # the orphans pair up inside their own part, in colour 2
        require(len(orphans) % 2 == 0, ("odd orphan count", kind, n, orphans))
        pairs = []
        left = [z for z in orphans if z < n]
        right = [z for z in orphans if z >= n]
        for grp in (left, right):
            require(len(grp) in (0, 2), ("orphan grouping", kind, n, grp))
            if len(grp) == 2:
                e = tuple(sorted(grp))
                require(e in sets[2], ("(b) orphan edge not colour 2",
                                       kind, n, e))
                pairs.append(e)
                for z in grp:
                    word[z] = 2
        fib, per = fibre_of_word(N, cs, tuple(word))
        require(len(fib) == 2, ("(b)(c) fibre size != 2", kind, n, x, y,
                                len(fib), per))
        require(per[1] == 1 and per[0] == 2 and per[2] == 1,
                ("factor profile", kind, n, per))
        cross1 = {tuple(sorted((x, u[0]))), tuple(sorted((y, u[1])))}
        cross2 = {tuple(sorted((x, u[1]))), tuple(sorted((y, u[0]))) }
        got = [set(m) & (cross1 | cross2) for m in fib]
        require({frozenset(cross1), frozenset(cross2)} ==
                {frozenset(g) for g in got},
                ("(b) fibre members are not the two cross pairings",
                 kind, n, got))
        d = {}
        for e in cross1:
            d[e] = d.get(e, 0) + 1
        for e in cross2:
            d[e] = d.get(e, 0) - 1
        diffs.append(d)
        words.append(list(word))

    # (c) the three difference vectors sum to zero
    total = {}
    for d in diffs:
        for e, c in d.items():
            total[e] = total.get(e, 0) + c
    require(all(c == 0 for c in total.values()),
            ("(c) the three differences do not cancel", kind, n, total))
    rec = {"kind": kind, "n": n, "N": N, "v": list(v), "u": list(u),
           "support": sum(len(s) for s in cs),
           "words": words, "relation_length": 3, "relation_coeff_sum": 3,
           "verified": True}
    print(f"  {kind}_{n}: N={N:3d}  K_2,3 on v={v} u={u} in colour 0; "
          f"three binomial fibres verified; d1+d2+d3 = 0 (3 terms, odd) "
          f"=> 1 = -1")
    return rec


def main():
    print("== proof-output check of THEOREM W13.6 ==")
    print("F_n (N = 0 mod 4):")
    for n in range(4, 25, 2):
        OUT["F"].append(check("F", n))
    print("F'_n (N = 2 mod 4):")
    for n in range(5, 26, 2):
        OUT["Fprime"].append(check("Fprime", n))
    print(f"\n  verified for N = 8, 12, ..., {2 * 24} (F_n) and "
          f"N = 10, 14, ..., {2 * 25} (F'_n): every even N in [8, 50]")
    with open(__file__.rsplit("/", 1)[0] + "/results_task2_k23.json",
              "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("wrote results_task2_k23.json")


if __name__ == "__main__":
    main()

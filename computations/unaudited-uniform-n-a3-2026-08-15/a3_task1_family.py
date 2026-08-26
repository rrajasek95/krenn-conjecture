#!/usr/bin/env python3
"""A3 Task 1 -- the singleton lemma fails for EVERY N = 0 mod 4, N >= 8.

Builds the family F_n (n even >= 4, N = 2n):

    V = X u Y,  |X| = |Y| = n,
    M_X, M_Y  perfect matchings of X, of Y,
    E_1 = M_X u M_Y                       (colour 1)
    E_2 = (K_X \\ M_X) u (K_Y \\ M_Y)      (colour 2)
    E_0 = K_{X,Y}                          (colour 0)

all edges live, all labels diagonal.  n = 4 reproduces the committed
K_8 counterexample of notes/monomial-fiber-counterexample.md verbatim.

Checks, all exact:
  (a) the three constant fibres are nonempty;
  (b) NO mixed fibre is a singleton;
  (c) the fibre census;
  (d) the K_{2,3} odd circuit exists: three binomial fibres whose exponent
      differences d_12 + d_23 - d_13 = 0, giving 1 = -1.
Controls: direct enumeration of all (N-1)!! matchings vs the product
formula, at N = 8 and 12; and mutations that must break the properties.
"""

from __future__ import annotations

import json
import sys
from itertools import combinations

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a3_core import (DiagonalTemplate, colour_partitions, fibre_profile,
                     fibres, geometry, odd_circuit, binomial_diffs)


def family(n):
    """F_n on N = 2n sites.  X = evens 0,2,..; Y = odds 1,3,.. (n=4 gives the
    committed labelling 0..7 with X={0,2,4,6}, Y={1,3,5,7})."""
    N = 2 * n
    X = [2 * i for i in range(n)]
    Y = [2 * i + 1 for i in range(n)]
    MX = [tuple(sorted((X[2 * i], X[2 * i + 1]))) for i in range(n // 2)]
    MY = [tuple(sorted((Y[2 * i], Y[2 * i + 1]))) for i in range(n // 2)]
    E1 = set(MX) | set(MY)
    E2 = set()
    for S in (X, Y):
        for a, b in combinations(sorted(S), 2):
            if (a, b) not in E1:
                E2.add((a, b))
    E0 = {tuple(sorted((x, y))) for x in X for y in Y}
    return N, DiagonalTemplate(N, [E0, E1, E2]), dict(X=X, Y=Y, MX=MX, MY=MY)


def committed_n8():
    """The template of notes/monomial-fiber-counterexample.md, (1)."""
    E1 = {(0, 2), (1, 3), (4, 6), (5, 7)}
    E2 = {(0, 4), (0, 6), (1, 5), (1, 7), (2, 4), (2, 6), (3, 5), (3, 7)}
    E0 = {e for e in combinations(range(8), 2) if e not in E1 and e not in E2}
    return DiagonalTemplate(8, [E0, E1, E2])


def k23_circuit(n, tpl, data):
    """Exhibit the three binomial fibres of the K_{2,3} circuit and verify
    d_12 + d_23 - d_13 = 0 exactly (so the three '-1's give 1 = -1).

    Hubs u1,u2 in Y, spokes v1,v2,v3 in X.  For the pair {i,j} the word is:
    colour 0 on {u1,u2,vi,vj}, colour 1 on the M-pairs fully outside, and
    colour 2 on the two leftover halves of the broken M-pairs."""
    X, Y, MX, MY = data["X"], data["Y"], data["MX"], data["MY"]
    N = 2 * n
    geo = geometry(N)
    u1, u2 = MY[0]                       # a whole M_Y pair as the two hubs
    # three spokes taken from three DIFFERENT M_X pairs when possible
    spokes = [MX[k % len(MX)][k // len(MX)] for k in range(3)]
    if len(set(spokes)) != 3:
        spokes = sorted(X)[:3]
    words = {}
    for i, j in combinations(range(3), 2):
        vi, vj = spokes[i], spokes[j]
        T = {u1, u2, vi, vj}
        word = [None] * N
        for v in T:
            word[v] = 0
        broken = [p for p in MX if (p[0] in T) ^ (p[1] in T)]
        leftovers = [v for p in broken for v in p if v not in T]
        for p in MX + MY:
            if p[0] in T or p[1] in T:
                continue
            word[p[0]] = word[p[1]] = 1
        for v in leftovers:
            word[v] = 2
        assert all(w is not None for w in word), (word, T, leftovers)
        words[(i, j)] = tuple(word)
    # exact fibres of the three words by DIRECT enumeration
    labels = tpl.labels()
    table = fibres(geo, labels)
    out = {}
    diffs = {}
    for key, w in words.items():
        mem = table.get(w, [])
        assert len(mem) == 2, (key, w, len(mem))
        a, b = geo.exponent(mem[0]), geo.exponent(mem[1])
        d = tuple(p - q for p, q in zip(a, b))
        # orient: put the matching containing (u1,vi) first
        vi, vj = spokes[key[0]], spokes[key[1]]
        e = geo.index[tuple(sorted((u1, vi)))]
        if d[e] < 0:
            d = tuple(-t for t in d)
        diffs[key] = d
        out[str(key)] = dict(word=list(w),
                             matchings=[list(map(list, geo.matchings[k]))
                                        for k in mem])
    r = tuple(a + b - c for a, b, c in
              zip(diffs[(0, 1)], diffs[(1, 2)], diffs[(0, 2)]))
    circuit_ok = all(t == 0 for t in r)
    return dict(hubs=[u1, u2], spokes=spokes, fibres=out,
                relation="d01 + d12 - d02", relation_is_zero=circuit_ok,
                parity_of_coefficient_sum=(1 + 1 - 1) % 2)


def _factorial(k):
    r = 1
    for i in range(2, k + 1):
        r *= i
    return r


def family_singletons_factorised(n, tpl, X, Y):
    """Exact number of mixed singleton fibres of F_n, and the pure sizes,
    computed by splitting each word into its X-half and its Y-half.

    A side-pattern on X is a map X -> {0,1,2}; it contributes
    (a = |S_0 n X|, p1 = pm(G_1[S_1 n X]), p2 = pm(G_2[S_2 n X])).
    Same on Y.  The fibre size of the assembled word is
        a! * (p1^X p1^Y) * (p2^X p2^Y)      if |S_0 n X| = |S_0 n Y| = a
        0                                    otherwise.
    """
    N = 2 * n
    pmX = [tpl.pm[r] for r in range(3)]

    def side(S):
        """{(a, p1, p2, mono): multiplicity} over the 3^|S| side patterns.
        mono = the colour if the pattern is constant on S, else -1."""
        agg = {}
        for k in range(3 ** len(S)):
            t, masks = k, [0, 0, 0]
            for v in S:
                r = t % 3
                t //= 3
                masks[r] |= 1 << v
            p1 = pmX[1][masks[1]]
            p2 = pmX[2][masks[2]]
            if p1 == 0 or p2 == 0:
                continue
            a = bin(masks[0]).count("1")
            mono = -1
            for r in range(3):
                if bin(masks[r]).count("1") == len(S):
                    mono = r
            key = (a, p1, p2, mono)
            agg[key] = agg.get(key, 0) + 1
        return agg

    sx, sy = side(X), side(Y)
    byA_y = {}
    for (a, p1, p2, mono), c in sy.items():
        byA_y.setdefault(a, []).append((p1, p2, mono, c))
    singles = 0
    pures = [0, 0, 0]
    for (a, p1, p2, mono), cx in sx.items():
        for (q1, q2, mono_y, cy) in byA_y.get(a, ()):
            size = _factorial(a) * p1 * q1 * p2 * q2
            if mono >= 0 and mono == mono_y:      # a constant word
                pures[mono] = size
                continue
            if size == 1:
                singles += cx * cy
    return singles, pures


def main():
    parts_cache = {}
    results = {}

    # ---- control: committed N=8 example vs the n=4 member of the family
    c = committed_n8()
    _, f4, _ = family(4)
    same = [set(map(tuple, c.colour_edges[r])) == set(map(tuple, f4.colour_edges[r]))
            for r in range(3)]
    results["committed_n8_equals_F4"] = same
    print("committed K_8 example == F_4 (colour by colour):", same)

    # ---- control: product formula vs direct enumeration, N = 8 and 12
    for n in (4, 6):
        N, tpl, _ = family(n)
        geo = geometry(N)
        table = fibres(geo, tpl.labels())
        s_direct, hist_direct = fibre_profile(table)
        if N not in parts_cache:
            parts_cache[N] = colour_partitions(N)
        s_prod, hist_prod, pures, _ = tpl.census(parts_cache[N])
        pures_direct = [len(table.get(tuple([r] * N), [])) for r in range(3)]
        ok = (s_direct == s_prod and hist_direct == hist_prod
              and pures == pures_direct)
        results[f"control_product_vs_direct_N{N}"] = dict(
            ok=ok, singletons=s_direct, hist=hist_direct, pures=pures)
        print(f"N={N}: direct-vs-product agree={ok} singletons={s_direct} "
              f"pures={pures} hist={hist_direct}")

    # ---- the family, by the product formula (full 3^N scan)
    fam = {}
    for n in (4, 6):
        N, tpl, data = family(n)
        if N not in parts_cache:
            parts_cache[N] = colour_partitions(N)
        s, hist, pures, sw = tpl.census(parts_cache[N])
        fam[N] = dict(n=n, singletons=s, pures=pures,
                      mixed_fibre_histogram=hist,
                      support=sum(len(e) for e in tpl.colour_edges),
                      full_support=N * (N - 1) // 2, method="full 3^N scan")
        print(f"F_{n}: N={N} pures={pures} singletons={s} "
              f"mixed sizes={ {k: v for k, v in list(hist.items())[:8]} }"
              f"{' ...' if len(hist) > 8 else ''}")

    # ---- larger n: the SAME exact count, factorised over X and Y.
    #   G_1,G_2 live inside K_X u K_Y and G_0 = K_{X,Y}, so for a word with
    #   parts (S_0,S_1,S_2):   pm_0 = k! (k = |S_0 n X| = |S_0 n Y|, else 0),
    #   pm_r = pm(G_r[S_r n X]) * pm(G_r[S_r n Y]) for r = 1,2.
    #   Enumerating the 3^n side-patterns on X and on Y is exact and cheap.
    for n in (8, 10, 12):
        N, tpl, data = family(n)
        X, Y = data["X"], data["Y"]
        s, pures = family_singletons_factorised(n, tpl, X, Y)
        fam[N] = dict(n=n, singletons=s, pures=pures,
                      support=N * (N - 1) // 2,
                      full_support=N * (N - 1) // 2,
                      method="factorised over X,Y (exact)")
        print(f"F_{n}: N={N} pures={pures} singletons={s} (factorised)")
    results["family"] = fam

    # ---- the K_{2,3} odd circuit (direct enumeration; N = 8, 12)
    circ = {}
    for n in (4, 6):
        N, tpl, data = family(n)
        circ[N] = k23_circuit(n, tpl, data)
        print(f"F_{n}: K_23 circuit relation d01+d12-d02 = 0 ->",
              circ[N]["relation_is_zero"],
              "hubs", circ[N]["hubs"], "spokes", circ[N]["spokes"])
    results["k23_circuit"] = circ

    # ---- odd-circuit search over ALL binomial fibres (independent engine)
    for n in (4, 6):
        N, tpl, data = family(n)
        geo = geometry(N)
        table = fibres(geo, tpl.labels())
        bd = binomial_diffs(geo, table)
        rel = odd_circuit([d for _, d in bd])
        results[f"odd_circuit_all_binomials_N{N}"] = dict(
            binomials=len(bd), found=rel is not None,
            coefficient_sum_parity=(sum(rel) % 2) if rel else None,
            support=[i for i, v in enumerate(rel) if v] if rel else None)
        print(f"N={N}: {len(bd)} binomial fibres; odd relation found:",
              rel is not None)

    # ---- mutation controls: break the construction, singletons must appear
    mut = {}
    N, tpl, data = family(4)
    X, Y, MX, MY = data["X"], data["Y"], data["MX"], data["MY"]
    parts = parts_cache[8]
    # M1: recolour one M_X edge from 1 to 2
    e = MX[0]
    E0, E1, E2 = [set(s) for s in tpl.colour_edges]
    E1.discard(e); E2.add(e)
    m = DiagonalTemplate(8, [E0, E1, E2]).census(parts)
    mut["recolour_MX_edge_1to2"] = dict(singletons=m[0], pures=m[2])
    # M2: delete one E_0 edge
    E0, E1, E2 = [set(s) for s in tpl.colour_edges]
    E0.discard(sorted(E0)[0])
    m = DiagonalTemplate(8, [E0, E1, E2]).census(parts)
    mut["delete_one_E0_edge"] = dict(singletons=m[0], pures=m[2])
    # M3: swap one E_2 edge to colour 0
    E0, E1, E2 = [set(s) for s in tpl.colour_edges]
    f = sorted(E2)[0]
    E2.discard(f); E0.add(f)
    m = DiagonalTemplate(8, [E0, E1, E2]).census(parts)
    mut["recolour_E2_edge_2to0"] = dict(singletons=m[0], pures=m[2])
    results["mutations"] = mut
    for k, v in mut.items():
        print("mutation", k, "->", v)

    with open(__file__.rsplit("/", 1)[0] + "/results_task1_family.json", "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    print("\nwrote results_task1_family.json")


if __name__ == "__main__":
    main()

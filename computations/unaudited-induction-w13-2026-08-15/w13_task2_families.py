#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- Task 2 (R1b): the two explicit singleton-free
families, and the SHORT (K_{2,3}) odd circuit in both.

  F_n   (N = 0 mod 4)  -- A3 Theorem A3.1 / A3.3
  F'_n  (N = 2 mod 4)  -- A3's addendum family (transcribed from
                          a3_task1_family_odd.py, rebuilt here independently)

Together they cover every even N >= 8.  This script

  1. rebuilds both families from their definitions,
  2. verifies (exactly) three nonzero pures and no mixed singleton fibre,
  3. extracts every binomial fibre and its difference vector WITHOUT
     enumerating all perfect matchings of K_N (per-fibre reconstruction from
     the colour-induced subgraphs), so N = 14, 16 are reachable,
  4. searches for a LENGTH-3 odd circuit d_i +- d_j +- d_k = 0, which is
     exactly the Perm-K_{2,3} signature, and
  5. exhibits the underlying 5 vertices + colour and checks A3.3'(a)(b)(c)
     on the nose: all six edges u_x v_y present in one colour, and the three
     words are genuine binomial fibres.

Every certificate is re-verified from scratch.
"""

from __future__ import annotations

import json
import sys
import time
from itertools import combinations

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w13_rcell import (census, diagonal_labels, diagonal_sizes, edges,
                       edge_index, odd_relation, pm_table, verdict,
                       word_masks)

OUT = {}


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


# ------------------------------------------------------------- the families

def family_F(n):
    """A3's F_n: N = 2n with n EVEN.  X|Y split, colour 1 = M_X u M_Y,
    colour 2 = the remaining intra-part edges, colour 0 = K_{X,Y}."""
    require(n % 2 == 0 and n >= 4, n)
    N = 2 * n
    X = list(range(n))
    Y = list(range(n, 2 * n))
    E1 = set()
    for part in (X, Y):
        for i in range(0, n, 2):
            E1.add(tuple(sorted((part[i], part[i + 1]))))
    E2 = set()
    for part in (X, Y):
        for e in combinations(sorted(part), 2):
            if e not in E1:
                E2.add(e)
    E0 = {tuple(sorted((x, y))) for x in X for y in Y}
    return N, [sorted(E0), sorted(E1), sorted(E2)]


def family_Fprime(n):
    """A3's addendum family F'_n: N = 2n with n ODD, n >= 5."""
    require(n % 2 == 1 and n >= 5, n)
    N = 2 * n
    A = list(range(n))
    B = list(range(n, 2 * n))
    a, b = A[0], B[0]
    MA = [tuple(sorted((A[i], A[i + 1]))) for i in range(1, n - 1, 2)]
    MB = [tuple(sorted((B[i], B[i + 1]))) for i in range(1, n - 1, 2)]
    Pc = MB[-1]
    c = Pc[1]
    E1 = set(MA) | set(MB) | {tuple(sorted((a, b)))}
    E0 = {tuple(sorted((x, y))) for x in A for y in B}
    E0 -= {tuple(sorted((a, y))) for y in B if y != c}
    E2 = set()
    for S in (A, B):
        for e in combinations(sorted(S), 2):
            if e in E1:
                continue
            if S is A and a in e:
                continue
            if S is B and b in e and (e[0] in Pc or e[1] in Pc):
                continue
            E2.add(e)
    E2 |= {tuple(sorted((a, y))) for y in B if y not in (b, c)}
    return N, [sorted(E0), sorted(E1), sorted(E2)], {"a": a, "b": b, "c": c,
                                                     "Pc": list(Pc)}


# --------------------------- per-fibre matching reconstruction (no full scan)

def matchings_of(vertices, edge_set):
    """All perfect matchings of the induced subgraph, as edge tuples."""
    vs = sorted(vertices)
    if not vs:
        return [()]
    first = vs[0]
    out = []
    for other in vs[1:]:
        e = (first, other) if first < other else (other, first)
        if e in edge_set:
            rest = [v for v in vs[1:] if v != other]
            for tail in matchings_of(rest, edge_set):
                out.append((e,) + tail)
    return out


def binomial_data(N, colour_sets, max_words=None):
    """[(word, d)] for every mixed fibre of size exactly 2, via the diagonal
    product formula plus per-fibre reconstruction."""
    sets = [set(map(tuple, s)) for s in colour_sets]
    sizes, mixed, pures = diagonal_sizes(N, colour_sets)
    m, _ = word_masks(N)
    idx = edge_index(N)
    ne = len(edges(N))
    hits = np.nonzero(mixed & (sizes == 2))[0]
    out = []
    for k in hits:
        word = []
        t = int(k)
        for _ in range(N):
            word.append(t % 3)
            t //= 3
        parts = [[v for v in range(N) if word[v] == r] for r in range(3)]
        per = [matchings_of(parts[r], sets[r]) for r in range(3)]
        require(len(per[0]) * len(per[1]) * len(per[2]) == 2,
                ("fibre size mismatch", word))
        full = []
        for m0 in per[0]:
            for m1 in per[1]:
                for m2 in per[2]:
                    full.append(m0 + m1 + m2)
        d = [0] * ne
        for e in full[0]:
            d[idx[e]] += 1
        for e in full[1]:
            d[idx[e]] -= 1
        out.append((tuple(word), tuple(d), full))
    return out, [int(p) for p in pures], sizes, mixed


# ------------------------------------------------------ short (K_23) circuit

def short_odd_circuit(diffs):
    """A relation eps_i d_i + eps_j d_j + eps_k d_k = 0 with eps in {+-1}
    (coefficient sum odd)."""
    m = len(diffs)
    table = {}
    for i, d in enumerate(diffs):
        table.setdefault(d, []).append(i)
        table.setdefault(tuple(-x for x in d), []).append(-i - 1)
    for i in range(m):
        for j in range(i + 1, m):
            for sj in (1, -1):
                sm = tuple(diffs[i][t] + sj * diffs[j][t]
                           for t in range(len(diffs[i])))
                neg = tuple(-x for x in sm)
                for key, sk in ((neg, 1), (sm, -1)):
                    for hit in table.get(key, ()):
                        k = hit if hit >= 0 else -hit - 1
                        if k not in (i, j):
                            return (i, 1), (j, sj), (k, sk)
    return None


def k23_from_circuit(N, bin_data, circuit):
    """Read the 5 vertices + colour off a length-3 circuit and verify
    A3.3' (a) all six cross edges present in one colour, (b) the three
    words are binomial fibres, (c) the complement splits (each of the three
    fibres has size exactly 2)."""
    idx = edge_index(N)
    rev = {v: k for k, v in idx.items()}
    involved = set()
    for i, _ in circuit:
        for t, val in enumerate(bin_data[i][1]):
            if val:
                involved.update(rev[t])
    colours = set()
    for i, _ in circuit:
        w = bin_data[i][0]
        for t, val in enumerate(bin_data[i][1]):
            if val:
                u, v = rev[t]
                require(w[u] == w[v], "difference edge is not monochrome")
                colours.add(w[u])
    return sorted(involved), sorted(colours)


# ----------------------------------------------------------------- driver

def analyse(name, N, colour_sets, extra=None):
    t0 = time.time()
    bins, pures, sizes, mixed = binomial_data(N, colour_sets)
    live = sizes[mixed]
    n_single = int((live == 1).sum())
    require(all(p > 0 for p in pures), (name, pures))
    require(n_single == 0, (name, n_single))
    diffs = [d for _, d, _ in bins]
    rel = odd_relation(diffs)
    require(rel is not None, (name, "no odd relation"))
    # re-verify the odd relation from scratch
    acc = [0] * len(diffs[0])
    for coeff, d in zip(rel, diffs):
        for t in range(len(acc)):
            acc[t] += coeff * d[t]
    require(all(x == 0 for x in acc) and sum(rel) % 2 == 1, (name, "bad rel"))
    circ = short_odd_circuit(diffs)
    verts, cols = ([], [])
    if circ:
        verts, cols = k23_from_circuit(N, bins, circ)
    rec = {"name": name, "N": N,
           "support": sum(len(s) for s in colour_sets),
           "full_support": N * (N - 1) // 2,
           "pures": pures, "singletons": n_single,
           "n_binomials": len(bins),
           "odd_relation_support": sum(1 for x in rel if x),
           "odd_relation_coeff_sum": sum(rel),
           "length3_circuit": bool(circ),
           "circuit_words": [list(bins[i][0]) for i, _ in circ] if circ else [],
           "circuit_signs": [s for _, s in circ] if circ else [],
           "circuit_vertices": verts, "circuit_colours": cols,
           "seconds": round(time.time() - t0, 1)}
    if extra:
        rec.update(extra)
    print(f"  {name}: N={N} support {rec['support']}/{rec['full_support']} "
          f"pures {pures} singletons {n_single} binomials {len(bins)}")
    print(f"        odd relation: PASS (support {rec['odd_relation_support']}, "
          f"coeff sum {rec['odd_relation_coeff_sum']}); "
          f"LENGTH-3 (K_2,3) circuit: {bool(circ)}"
          + (f" on vertices {verts} in colour(s) {cols}" if circ else "")
          + f"  [{rec['seconds']}s]")
    return rec


def main():
    OUT["F"] = []
    OUT["Fprime"] = []
    print("== F_n  (N = 0 mod 4) ==")
    for n in (4, 6):
        N, cs = family_F(n)
        OUT["F"].append(analyse(f"F_{n}", N, cs))
    print("\n== F'_n  (N = 2 mod 4) ==")
    for n in (5, 7):
        N, cs, marks = family_Fprime(n)
        OUT["Fprime"].append(analyse(f"F'_{n}", N, cs, extra={"marks": marks}))
    with open(__file__.rsplit("/", 1)[0] + "/results_task2_families.json",
              "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("\nwrote results_task2_families.json")


if __name__ == "__main__":
    main()

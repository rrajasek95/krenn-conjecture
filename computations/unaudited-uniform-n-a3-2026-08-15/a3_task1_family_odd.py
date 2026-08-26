#!/usr/bin/env python3
"""A3 -- the N = 2 mod 4 companion family F'_n, read off the certified
N = 10 (support 39) singleton-free template and generalised in closed form.

n = N/2 ODD, n >= 5.  V = A u B with |A| = |B| = n.  Distinguish a in A and
two distinct b, c in B.  Let M_A be a perfect matching of A\{a}, M_B one of
B\{b}, and P_c the M_B-pair containing c.  Then

    G_1 = {ab} u M_A u M_B                              (a perfect matching)
    G_0 = K_{A,B} \ ( {a} x (B\{c}) )                   (a keeps only ac)
    G_2 = (K_A \ (M_A u {a}x(A\{a})))
        u (K_B \ (M_B u {b}xP_c))
        u ( {a} x (B\{b,c}) )
    dead: {a} x (A\{a})  and  {b} x P_c .
"""
import json, sys
from itertools import combinations
sys.path.insert(0, '.')
from a3_core import DiagonalTemplate, colour_partitions
import numpy as np


def family_odd(n):
    assert n % 2 == 1 and n >= 5
    N = 2 * n
    A = list(range(n)); B = list(range(n, 2 * n))
    a = A[0]; b = B[0]
    MA = [tuple(sorted((A[i], A[i + 1]))) for i in range(1, n - 1, 2)]
    MB = [tuple(sorted((B[i], B[i + 1]))) for i in range(1, n - 1, 2)]
    Pc = MB[-1]; c = Pc[1]
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
    return N, [E0, E1, E2]


def census_fast(N, ce):
    tpl = DiagonalTemplate(N, ce)
    parts = colour_partitions(N)
    m0 = np.array([p[1] for p in parts]); m1 = np.array([p[2] for p in parts])
    m2 = np.array([p[3] for p in parts])
    p0 = np.array(tpl.pm[0], dtype=object); p1 = np.array(tpl.pm[1], dtype=object)
    p2 = np.array(tpl.pm[2], dtype=object)
    size = p0[m0] * p1[m1] * p2[m2]
    full = (1 << N) - 1
    const = (m0 == full) | (m1 == full) | (m2 == full)
    pures = [int(p0[full]), int(p1[full]), int(p2[full])]
    sing = int(np.count_nonzero((size == 1) & ~const))
    hist = {}
    for s in size[~const]:
        if s: hist[int(s)] = hist.get(int(s), 0) + 1
    return sing, pures, dict(sorted(hist.items())), sum(len(x) for x in ce)


def main():
  out = {}
  for n in (5, 7):
    N, ce = family_odd(n)
    sing, pures, hist, sup = census_fast(N, ce)
    out[f"N={N}"] = dict(n=n, singletons=sing, pures=pures, support=sup,
                         full_support=N * (N - 1) // 2,
                         histogram={str(k): v for k, v in list(hist.items())[:10]})
    print(f"F'_{n}: N={N} support={sup}/{N*(N-1)//2} pures={pures} "
          f"singletons={sing}")
  json.dump(out, open('results_family_odd.json', 'w'), indent=1)
  print('wrote results_family_odd.json')


if __name__ == "__main__":
    main()

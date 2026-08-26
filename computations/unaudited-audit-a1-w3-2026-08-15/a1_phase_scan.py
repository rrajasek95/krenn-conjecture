"""AUDIT A1 / claim 4 -- how often does the obstruction mechanism actually
fire on the objects the campaign searches?

For a support S:
  * every 2-term mixed fibre {M, M'} forces  arg t_M - arg t_M' = pi  AND
    |t_M| = |t_M'|;  record d = 1_M - 1_M'.
  * for a mixed fibre with k >= 3 terms, if a pair (M_i, M_j) has
    1_{M_i} - 1_{M_j} equal to a sum of an EVEN number of elements of +-D,
    the two terms are forced PARALLEL with equal moduli, so the fibre cannot
    be equilateral -- all-moduli-1 is then infeasible on S.
    (An ODD number forces them antiparallel with equal moduli, i.e. the two
    terms cancel: the fibre must then close up on its remaining terms.)

Here we look for the cheap cases: g in +-D (parity 1) and g = d1 + d2
(parity 2).
"""

from __future__ import annotations

import itertools
import random
import sys

from a1_core import cellkey
from a1_phase import fibres, is_mixed

N = 8
E = list(itertools.combinations(range(N), 2))


def diffs(terms, Sl):
    idx = {s: i for i, s in enumerate(Sl)}
    vecs = []
    for M in terms:
        v = [0] * len(Sl)
        for k in M:
            v[idx[k]] = 1
        vecs.append(tuple(v))
    return vecs


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scan(S):
    Sl = sorted(S)
    fib = fibres(N, S)
    two, many = [], []
    for w, t in fib.items():
        if not is_mixed(w):
            continue
        if len(t) == 2:
            two.append(diffs(t, Sl))
        elif len(t) >= 3:
            many.append((w, diffs(t, Sl)))
    D = set()
    for v in two:
        d = sub(v[0], v[1])
        D.add(d)
        D.add(tuple(-x for x in d))
    Dl = sorted(D)
    par1 = par2 = 0
    hits = []
    for w, vs in many:
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                g = sub(vs[i], vs[j])
                if g in D:
                    par1 += 1
                    hits.append((w, i, j, 1))
                    continue
                found = False
                for d1 in Dl:
                    if add(d1, g) is None:
                        continue
                    need = sub(g, d1)
                    if need in D:
                        found = True
                        break
                if found:
                    par2 += 1
                    hits.append((w, i, j, 2))
    return len(two), len(many), len(D), par1, par2, hits


def anchor_chart(rng, nedges=18):
    while True:
        es = rng.sample(E, nedges)
        deg = [0] * N
        for u, v in es:
            deg[u] += 1
            deg[v] += 1
        if min(deg) >= 3:
            break
    return frozenset((u, v, c, c) for (u, v), c in
                     zip(es, [rng.randrange(3) for _ in es]))


if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
    print("AUDIT A1 -- forced-parallel scan on anchor charts (n=8, |E|=18)")
    tot2 = tot1 = 0
    for t in range(int(sys.argv[2]) if len(sys.argv) > 2 else 15):
        S = anchor_chart(rng)
        n2, nm, nd, p1, p2, hits = scan(S)
        tot1 += p1
        tot2 += p2
        print(f"  chart {t:2d}: 2-term fibres={n2:3d}  >=3-term fibres={nm:3d} "
              f"|D|={nd:3d}  antiparallel-forced pairs={p1:3d}  "
              f"PARALLEL-forced pairs={p2:3d}")
    print(f"TOTAL antiparallel-forced {tot1}, PARALLEL-forced {tot2} "
          f"(any parallel-forced pair in a 3-term fibre kills all-moduli-1)")

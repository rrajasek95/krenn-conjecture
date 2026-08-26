#!/usr/bin/env python3
"""W40 probe: is the D5 background + a PURE colour-2 PM an X_4 point, and
does it survive FULL exactness (the 1680 trichromatic off-count-5 words that
X_4 omits)?  Exploratory -- no verdicts stored."""
from __future__ import annotations

import itertools
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    EDG, N, PMS, d5_point, ekey, haf, haf_pm, off,
)

D5 = d5_point()


def build(m2, weights=None):
    src = {e: [[Fraction(0)] * 3 for _ in range(3)] for e in EDG}
    for e in EDG:
        for a in range(2):
            for b in range(2):
                src[e][a][b] = D5[e][a][b]
    for i, e in enumerate(m2):
        src[ekey(*e)][2][2] = Fraction(1) if weights is None else weights[i]
    return src


def audit(src):
    bad4, bad5 = [], []
    for w in itertools.product(range(3), repeat=N):
        tgt = 1 if len(set(w)) == 1 else 0
        v = haf(src, w, n=N, sample=Fraction(0))
        if v != tgt:
            (bad4 if off(w) <= 4 else bad5).append((w, v))
    return bad4, bad5


def ham(ma, mb):
    adj = {i: [] for i in range(N)}
    for e in list(ma) + list(mb):
        adj[e[0]].append(e[1])
        adj[e[1]].append(e[0])
    cur, prev, seen = 0, None, [0]
    for _ in range(N - 1):
        nxt = [x for x in adj[cur] if x != prev]
        if not nxt:
            return False
        prev, cur = cur, nxt[0]
        if cur in seen:
            return False
        seen.append(cur)
    return len(seen) == N


M0 = [(0, 1), (2, 3), (4, 5), (6, 7)]
M1 = [(0, 3), (1, 2), (4, 7), (5, 6)]
cands = []
for M in PMS:
    S = set(M)
    if S & set(M0) or S & set(M1):
        continue
    cands.append((list(M), ham(M0, M), ham(M1, M)))
print("PMs disjoint from M0,M1:", len(cands),
      "| both unions Hamiltonian:", sum(1 for c in cands if c[1] and c[2]))

for M, h0, h1 in cands:
    src = build(M)
    b4, b5 = audit(src)
    tag = "X4-POINT" if not b4 else f"k4bad={len(b4)}"
    print(f"M2={M} ham({h0},{h1}) {tag} off5bad={len(b5)}")

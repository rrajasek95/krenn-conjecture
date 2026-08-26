#!/usr/bin/env python3
"""W40 probe: extract an EXPLICIT point of the D5 level-4 (X_4) variety.

Structure first: with all colour-2 cross cells zero (lam = 0) the hafnian
factorises, H_w = haf(q | S) * haf(B | V - S, w) where S = w^{-1}(2), so the
X_4 system becomes a pure combinatorial system in the 28 weights q.
Exploratory -- no verdicts stored."""
from __future__ import annotations

import itertools
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    EDG, N, Sym, build_variables, cell_forms, completion_generators,
    d5_point, haf, haf_sym, kernel_bases, off, require, singular_decide,
    words3,
)

bg = d5_point()
kb = kernel_bases(bg)
names, lamidx, qidx = build_variables(kb)
cf = cell_forms(bg, kb, lamidx, qidx)
g4, m4 = completion_generators(cf, 4)

lam_gens = [Sym.var(lamidx[key]) for key in sorted(lamidx)]
print("--- I_4 + (lam = 0) ---")
o = singular_decide(g4 + lam_gens, names, 0, 900, want_dim=True)
print("  over Q:", o, flush=True)

# which even subsets S must have haf(q|S) = 0 ?
need_zero, ok_free = set(), set()
for w in words3(4):
    if 2 not in w:
        continue
    S = tuple(i for i in range(N) if w[i] == 2)
    if len(S) == N:
        continue
    rest = [i for i in range(N) if w[i] != 2]
    hb = haf(bg, {i: w[i] for i in rest}, sites=rest, sample=Fraction(0))
    if hb != 0:
        need_zero.add(S)
    else:
        ok_free.add(S)
print("subsets S forced haf(q|S)=0:", len(need_zero),
      "| S appearing only with vanishing cofactor:", len(ok_free - need_zero))
by_size = {}
for S in need_zero:
    by_size[len(S)] = by_size.get(len(S), 0) + 1
print("  by |S|:", sorted(by_size.items()))
allS = {tuple(s) for k in (0, 2, 4, 6)
        for s in itertools.combinations(range(N), k)}
print("  total even proper subsets:", len(allS),
      "free:", len(allS - need_zero))
free_by_size = {}
for S in allS - need_zero:
    free_by_size[len(S)] = free_by_size.get(len(S), 0) + 1
print("  free by |S|:", sorted(free_by_size.items()))
print("  free |S|=2 (edges q_e unconstrained by a 2-subset eq):",
      sorted(S for S in allS - need_zero if len(S) == 2))

#!/usr/bin/env python3
"""W40 probe: the D5 completion at level 5 (= FULL exactness at N=8, since
off(w) <= 5 always) and structure of the level-4 variety.  Exploratory."""
from __future__ import annotations

import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    N, build_variables, cell_forms, completion_generators, d5_point,
    kernel_bases, singular_decide, words3,
)

bg = d5_point()
kb = kernel_bases(bg)
names, lamidx, qidx = build_variables(kb)
cf = cell_forms(bg, kb, lamidx, qidx)
print("nvars", len(names), "lam", len(lamidx), "q", len(qidx))
print("words: off<=4", len(words3(4)), " all", len(words3(5)))

g5, m5 = completion_generators(cf, 5)
print("k=5 gens", len(g5), "monomials", sum(len(x.t) for x in g5))
t0 = time.time()
o = singular_decide(g5, names, 0, 3600, want_dim=True)
print("D5 FULL(k=5) over Q:", o, f"{time.time() - t0:.1f}s", flush=True)
t0 = time.time()
o2 = singular_decide(g5, names, "integer", 3600)
print("D5 FULL(k=5) over ZZ:", o2, f"{time.time() - t0:.1f}s", flush=True)

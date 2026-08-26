#!/usr/bin/env python3
"""W40 sizing probe (no verdicts): how big is the D5 completion system?"""
from __future__ import annotations

import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    N, build_variables, cell_forms, completion_generators, d5_point,
    delta2_point, kernel_bases, words3,
)

for name, bg in (("D5", d5_point()), ("Delta2", delta2_point())):
    t0 = time.time()
    kb = kernel_bases(bg)
    names, lamidx, qidx = build_variables(kb)
    cf = cell_forms(bg, kb, lamidx, qidx)
    print(f"[{name}] kernel profile {[kb[j]['dim'] for j in range(N)]} "
          f"nvars {len(names)} (lam {len(lamidx)} + q {len(qidx)})")
    for k in (3, 4):
        g, meta = completion_generators(cf, k)
        nm = sum(len(x.t) for x in g)
        deg = max((x.ndeg() for x in g), default=0)
        uniq = len({tuple(sorted(x.t.items())) for x in g})
        print(f"   k={k}: words {len(words3(k))} gens {len(g)} "
              f"uniq {uniq} monomials {nm} maxdeg {deg} "
              f"({time.time() - t0:.1f}s)")

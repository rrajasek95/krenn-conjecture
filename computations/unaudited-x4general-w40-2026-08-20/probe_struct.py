#!/usr/bin/env python3
"""W40 probe: structure of the D5 level-4 (X_4) variety -- which variables
are forced to vanish, and an explicit point.  Exploratory."""
from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    EDG, N, build_variables, cell_forms, completion_generators, d5_point,
    kernel_bases, no_shadow_guard, run_singular,
)

bg = d5_point()
kb = kernel_bases(bg)
names, lamidx, qidx = build_variables(kb)
cf = cell_forms(bg, kb, lamidx, qidx)
g4, _ = completion_generators(cf, 4)
body = ",\n ".join(g.to_singular(names) for g in g4)
nv = len(names)

script = (f"ring R = 0, (zzv(1..{nv})), dp;\n"
          f"ideal zzI = {body};\n"
          "ideal zzG = std(zzI);\n"
          '"UNIT:", 0;\n'
          "int zzi;\n"
          "string zzs = \"\";\n"
          "for (zzi = 1; zzi <= %d; zzi++) {\n"
          "  if (reduce(zzv(zzi), zzG) == 0) { zzs = zzs + string(zzi) + \",\"; }\n"
          "}\n"
          '"INIDEAL:", zzs;\n'
          '"DIM:", dim(zzG);\n'
          '"DEG:", degree(zzG);\n') % nv
no_shadow_guard(script, set(names))
t0 = time.time()
txt = run_singular(script, timeout=1800)
print(txt.strip(), f"\n({time.time() - t0:.1f}s)")

inv = {v: k for k, v in lamidx.items()}
inq = {v: k for k, v in qidx.items()}
for ln in txt.splitlines():
    if ln.strip().startswith("INIDEAL:"):
        s = ln.split(":", 1)[1].strip().rstrip(",")
        idx = [int(x) - 1 for x in s.split(",") if x.strip()]
        print("variables IN the ideal (forced to 0):", len(idx), "of", nv)
        print("  lam:", sorted(inv[i] for i in idx if i in inv))
        print("  q  :", sorted(inq[i] for i in idx if i in inq))
        print("SURVIVING lam:", sorted(inv[i] for i in range(nv)
                                       if i in inv and i not in idx))
        print("SURVIVING q  :", sorted(inq[i] for i in range(nv)
                                       if i in inq and i not in idx))

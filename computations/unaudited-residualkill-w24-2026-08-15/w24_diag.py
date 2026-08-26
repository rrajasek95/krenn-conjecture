#!/usr/bin/env python3
"""W24 -- diagnostics: WHICH rows kill, at exact stored clean points.
UNAUDITED.  Exact only."""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w24_core as C                                              # noqa: E402
import w24_pts as P                                               # noqa: E402
import w24_resid as RS                                            # noqa: E402

out = {"_header": "UNAUDITED W24 residual-system diagnostics (independent)."}
pts = P.stored_points()
print("stored exact clean points found:", len(pts))
rows = []
for m, tag, bl in pts:
    T = C.TEMPLATES[m]
    gam = C.gamma_edges(T)
    gam_set = set(gam)
    clean = P.w21_clean(m)
    cv = sum(1 for w in clean if C.phi(bl, gam_set, w) != 0)
    nz = all(bl[e][i][j] != 0 for e in gam for i in range(3) for j in range(3))
    d = RS.verdict(m, bl, want_detail=True)
    rows.append(dict(m=m, tag=tag, clean_violations=cv, all_nonzero=nz, **d))
    print("m=%d %-28s cleanviol=%d nz=%-5s | rows %4d rank %2d INCONS=%-5s "
          "forced=%d pure=%d badconst=%d KILLED=%s"
          % (m, tag[:28], cv, nz, d["n_rows"], d["rank"], d["inconsistent"],
             len(d["forced_zero"]), d["n_pure_monomial"],
             d["n_zero_row_nonzero_const"], d["killed"]), flush=True)
out["rows"] = rows
out["summary"] = dict(
    n=len(rows), killed=sum(1 for r in rows if r["killed"]),
    inconsistent=sum(1 for r in rows if r["inconsistent"]),
    clean_ok=sum(1 for r in rows if r["clean_violations"] == 0))
print("SUMMARY", out["summary"])
json.dump(out, open(os.path.join(HERE, "results_diag.json"), "w"),
          indent=1, default=str)

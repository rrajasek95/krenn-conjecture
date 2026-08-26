#!/usr/bin/env python3
"""W24 -- the GLOBAL vanishing dichotomy.  For each stored exact clean
point: on how many of the 6561 words is Phi = haf_Gamma nonzero?
UNAUDITED.  Exact only."""
from __future__ import annotations

import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w24_core as C                                              # noqa: E402
import w24_pts as P                                               # noqa: E402
import w24_resid as RS                                            # noqa: E402

out = {"_header": "UNAUDITED W24 global vanishing of haf_Gamma at clean pts."}
rows = []
for m, tag, bl in P.stored_points():
    gam_set = set(C.gamma_edges(C.TEMPLATES[m]))
    nz = [w for w in C.WORDS if C.phi(bl, gam_set, w) != 0]
    d = RS.verdict(m, bl)
    rows.append(dict(m=m, tag=tag, n_phi_nonzero=len(nz),
                     nonzero_examples=[list(w) for w in nz[:4]],
                     inconsistent=d["inconsistent"],
                     n_forced=len(d["forced_zero"]), killed=d["killed"]))
    print("m=%d %-30s Phi!=0 on %4d/6561 words | INCONS=%-5s forced=%2d"
          % (m, tag[:30], len(nz), d["inconsistent"], len(d["forced_zero"])),
          flush=True)
out["rows"] = rows
json.dump(out, open(os.path.join(HERE, "results_global.json"), "w"),
          indent=1, default=str)

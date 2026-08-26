#!/usr/bin/env python3
"""W30 quick pass: EXHAUSTIVE vertex analysis of the 39 stored exact points
(no descent needed -- they are read from disk).  UNAUDITED.  Exact only."""
from __future__ import annotations

import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w26_disj as DJ                                             # noqa: E402
import w26_pts as PT                                              # noqa: E402

RES = os.path.join(HERE, "results_quick.json")
OUT = {"_header": "UNAUDITED W30 exhaustive analysis of the 39 stored points",
       "recs": []}


def main():
    t0 = time.time()
    for i, (m, tag, bl) in enumerate(PT.stored_points()):
        r26 = DJ.analyse(m, bl)
        r30 = L.full_report(m, bl, stop_early=False)
        d26 = [l for l in L.VERTS if not r26[l]['DELIVERS']]
        rec = dict(m=m, tag=str(tag)[:40],
                   van=PT.vanishing_stratum(m, bl),
                   allnz=L.all_cells_nonzero(m, bl),
                   fails26=d26, fails30=r30['fails'],
                   nidx={l: r30[l]['n_idx'] for l in L.VERTS},
                   nzs={l: r30[l]['n_zero_scale'] for l in L.VERTS},
                   ndel={l: r30[l]['n_deliver'] for l in L.VERTS},
                   ncol={l: r30[l]['n_collapse'] for l in L.VERTS})
        bad = [l for l in L.VERTS
               if r26[l]['DELIVERS'] and not r30[l]['DELIVERS']]
        rec['C1_violation'] = bad
        OUT["recs"].append(rec)
        print("[%2d] m=%d %-30s van=%-5s allnz=%-5s  fails26=%-24s "
              "fails30=%-20s  C1bad=%s (%.0fs)"
              % (i, m, rec['tag'][:30], rec['van'], rec['allnz'],
                 ",".join(d26) or "-", ",".join(r30['fails']) or "-",
                 bad, time.time() - t0), flush=True)
        json.dump(OUT, open(RES, "w"), indent=1, default=str)
    nb = sum(1 for r in OUT["recs"] if r['C1_violation'])
    OUT["C1_violations"] = nb
    OUT["n"] = len(OUT["recs"])
    json.dump(OUT, open(RES, "w"), indent=1, default=str)
    print("DONE n=%d C1 violations=%d  %.0fs"
          % (len(OUT["recs"]), nb, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()

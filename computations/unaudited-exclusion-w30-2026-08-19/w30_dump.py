#!/usr/bin/env python3
"""W30: dump the 39 W20/W21 stored exact points to disk once.  UNAUDITED."""
from __future__ import annotations
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w26_pts as PT                                              # noqa: E402
import w26_fast as FA                                             # noqa: E402

out = {"_header": "UNAUDITED W30: W20/W21 stored exact points", "points": []}
res = os.path.join(HERE, "points_stored.json")
mdls = {}
for m, tag, bl in PT.stored_points():
    if m not in mdls:
        mdls[m] = FA.Model(m)
    out["points"].append(dict(
        m=m, tag=str(tag), van=mdls[m].vanishing(bl),
        allnz=mdls[m].allnz(bl),
        point={str(k): [[str(z) for z in r] for r in v]
               for k, v in bl.items()}))
    json.dump(out, open(res, "w"), indent=1)
    print("dumped %d  m=%d %s van=%s" % (len(out["points"]), m, tag,
                                         out["points"][-1]["van"]), flush=True)
out["done"] = True
json.dump(out, open(res, "w"), indent=1)
print("DONE %d points, off-stratum %d"
      % (len(out["points"]), sum(1 for p in out["points"] if not p["van"])),
      flush=True)

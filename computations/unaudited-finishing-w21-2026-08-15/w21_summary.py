#!/usr/bin/env python3
"""W21 -- collect every W21 result file into one index (UNAUDITED)."""
import json, os, glob
out = {"_header": "UNAUDITED W21 index of results (2026-08-15). Exact-arithmetic verdicts only."}
for p in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_*.json"))):
    try:
        d = json.load(open(p))
        out[os.path.basename(p)] = d.get("_header", "(no header)")
    except Exception as e:
        out[os.path.basename(p)] = "unreadable: %s" % e
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_index.json"), "w"), indent=1)
print(json.dumps(out, indent=1))

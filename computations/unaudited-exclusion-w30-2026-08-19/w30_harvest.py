#!/usr/bin/env python3
"""W30: harvest every hunter checkpoint into one points file. UNAUDITED."""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
out = {"_header": "UNAUDITED W30 harvested hunter points", "points": []}
seen = set()
for f in sorted(glob.glob(os.path.join(HERE, "results_hunt_*.json"))):
    d = json.load(open(f))
    p = 0 if d.get("field") == "Q" else int(d.get("field", 0) or 0)
    for rec in ([d["best"]] if d.get("best") else []) + d.get("hits", []):
        if rec.get("van") or not rec.get("allnz"):
            continue
        key = json.dumps(rec["point"], sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        out["points"].append(dict(m=d["m"], p=p, van=False,
                                  tag="%s|s%s|%s" % (os.path.basename(f),
                                                     rec.get("step"),
                                                     ",".join(rec["fails"])),
                                  fails_hunter=rec["fails"],
                                  point=rec["point"]))
json.dump(out, open(os.path.join(HERE, "points_hunt.json"), "w"), indent=1)
print("harvested", len(out["points"]), "off-stratum all-nonzero points")
for r in out["points"]:
    print("   m=%d p=%d fails=%s" % (r["m"], r["p"], ",".join(r["fails_hunter"]) or "-"))

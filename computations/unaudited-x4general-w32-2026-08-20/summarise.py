#!/usr/bin/env python3
"""Assemble every task checkpoint into results_SUMMARY.json."""
import glob, json, os
H = os.path.dirname(os.path.abspath(__file__))
out = {"lane": "W32 general X_4-emptiness at N=8",
       "pinned_head": open(os.path.join(H, "PINNED_HEAD.txt")).read().strip(),
       "status": "UNAUDITED", "tasks": {}}
for f in sorted(glob.glob(os.path.join(H, "results_t*.json"))):
    k = os.path.basename(f)[len("results_"):-len(".json")]
    try:
        d = json.load(open(f))
    except Exception as e:
        d = {"unreadable": str(e)}
    # keep the big ones summarised
    if k == "t17":
        d = {kk: (vv if kk != "done" else {"n_decided": len(vv)})
             for kk, vv in d.items()}
        for kk in ("m1", "m2"):
            if kk in d and isinstance(d[kk], dict):
                d[kk] = {a: (b if a != "survivors" else len(b))
                         for a, b in d[kk].items()}
    if k == "t19":
        d = {"m0_ZZ": [r.get("ZZ") for r in d.get("m0", [])],
             "m0_chars": [r.get("verdicts") for r in d.get("m0", [])],
             "m1_cases": len(d.get("m1", [])),
             "m1_all_ZZ_unit": all(r.get("ZZ") is True for r in d.get("m1", [])),
             "unchecked": d.get("unchecked", [])}
    if k == "t11":
        d = {kk: (vv if kk != "m1" else
                  {a: (b if a != "cases" else len(b)) for a, b in vv.items()})
             for kk, vv in d.items()}
    if k in ("t7", "t15"):
        d = {kk: (vv if kk not in ("celltypes", "strata", "k4_hits")
                  else (len(vv) if isinstance(vv, (list, dict)) else vv))
             for kk, vv in d.items()}
    if k == "t8":
        d = {kk: vv for kk, vv in d.items()}
    out["tasks"][k] = d
with open(os.path.join(H, "results_SUMMARY.json"), "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print("wrote results_SUMMARY.json with", len(out["tasks"]), "task blocks")

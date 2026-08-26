#!/usr/bin/env python3
"""A10 -- TARGETED mutation control for the m=28 (L2,R5) co-failure.
UNAUDITED AUDIT LANE.  A verdict-level mutation test: perturbing ONE cell
must be able to destroy the co-failure verdict at every audited point.
"""
import json, os, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import a10_lib as A
W30 = os.path.join(os.path.dirname(HERE), "unaudited-exclusion-w30-2026-08-19")
d = json.load(open(os.path.join(W30, "results_verify_hunt.json")))
OUT = {"_header": "UNAUDITED A10 targeted mutation control",
       "_controls_declared": ["M1_cofailure_flips"], "_controls_run": [], "recs": []}
t0 = time.time()
for i, e in enumerate(d["verified"]):
    if e["m"] != 28 or e["p"] != 31:
        continue
    p = 31; K = A.Fp(p)
    bl = {eval(k): [[int(z) for z in r] for r in v] for k, v in e["point"].items()}
    base = ('L2' in e["checks"]["V5_w30_exhaustive"] and 'R5' in e["checks"]["V5_w30_exhaustive"])
    flipped = None; ncell = 0
    for edge in A.S(28).gamma:
        for a in range(3):
            for b in range(3):
                for delta in (1, 2):
                    b2 = {ee: [r[:] for r in bl[ee]] for ee in bl}
                    b2[edge][a][b] = (b2[edge][a][b] + delta) % p
                    if b2[edge][a][b] == 0:
                        continue
                    ncell += 1
                    co = (A.vertex_verdict(28, b2, 'L', 2, K)['FAIL_primary'] and
                          A.vertex_verdict(28, b2, 'R', 5, K)['FAIL_primary'])
                    if co != base:
                        okc, bad = A.is_clean_point(28, b2, K)
                        flipped = dict(edge=str(edge), cell=[a, b], delta=delta,
                                       cofail_after=co, still_clean=okc,
                                       n_clean_violations=len(bad))
                        break
                if flipped: break
            if flipped: break
        if flipped: break
    OUT["recs"].append(dict(i=i, base_cofailure=base, n_mutations_tried=ncell,
                            flip=flipped))
    print("[%2d] base_cofail=%s flipped=%s after %d mutations (%.0fs)"
          % (i, base, bool(flipped), ncell, time.time()-t0), flush=True)
    json.dump(OUT, open(os.path.join(HERE, "results_mut.json"), "w"), indent=1, default=str)
OUT["M1_cofailure_flips"] = dict(n=len(OUT["recs"]),
    ok=all(r["flip"] for r in OUT["recs"]))
OUT["_controls_run"].append("M1_cofailure_flips")
missing = [c for c in OUT["_controls_declared"] if c not in OUT["_controls_run"]]
OUT["_manifest_ok"] = missing == []
json.dump(OUT, open(os.path.join(HERE, "results_mut.json"), "w"), indent=1, default=str)
assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
print("MANIFEST OK", OUT["_controls_run"], flush=True)

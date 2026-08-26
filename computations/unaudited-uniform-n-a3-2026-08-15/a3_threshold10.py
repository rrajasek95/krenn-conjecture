#!/usr/bin/env python3
"""A3 -- bracket the LOWEST support at N=10 carrying an (SC)-admissible,
singleton-free DIAGONAL monomial template with three live pures.

Every hit is certified twice (product formula + direct enumeration of all 945
matchings) and cross-checked with W2's independent kill engine, and its
(SC)-admissibility and min live degree are recorded.
"""
import json, random, sys
sys.path.insert(0, '.')
import a3_task2_reach as R
import a3_task1_certify10 as C
import a3_admissibility as AD

fr = R.Frame(10)
steps = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 14
out = {}
for m in range(24, 45):
    hit = None
    for seed in range(restarts):
        rng = random.Random(1000 * m + seed)
        v, st = R.anneal_at_support(fr, rng, m, steps)
        if v == 0:
            cert = C.certify(st, fr)
            ce = [[tuple(e) for e in cert["colour_edges"][r]] for r in range(3)]
            ok, bad = AD.sc_admissible(ce)
            deg = AD.live_degrees(ce)
            geo, lab = AD.to_labels(ce)
            import w2_monomial as W2
            verdict = W2.analyse(geo, lab)["verdict"]
            hit = dict(support=m, pures=cert["pures_product"],
                       singletons=cert["singletons_product"],
                       both_methods_agree=cert["two_methods_agree"],
                       SC_admissible=ok, SC_violations=bad,
                       min_live_degree=min(deg),
                       W2_verdict=verdict,
                       odd_circuit=cert["odd_circuit_found"],
                       colour_edges=cert["colour_edges"])
            break
    out[str(m)] = hit
    print(f"m={m:3d}: " + ("NO singleton-free template found" if hit is None
          else f"HIT pures={hit['pures']} (SC)={hit['SC_admissible']} "
               f"mindeg={hit['min_live_degree']} W2={hit['W2_verdict']}"),
          flush=True)
json.dump(out, open("results_threshold10.json", "w"), indent=1)
hits = sorted(int(k) for k, v in out.items() if v)
print("supports with a certified singleton-free template:", hits)
print("lowest:", hits[0] if hits else None)

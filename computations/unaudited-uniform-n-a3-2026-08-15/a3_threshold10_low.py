#!/usr/bin/env python3
"""A3 -- push the N=10 singleton-free threshold DOWN: heavy budget at the
supports where the first sweep found nothing (24..32), plus a re-check of the
N=8 analogue at 12..27 with the same engine (which must find nothing)."""
import json, random, sys
sys.path.insert(0, '.')
import a3_task2_reach as R, a3_task1_certify10 as C, a3_admissibility as AD
import w2_monomial as W2

out = {}
fr10 = R.Frame(10)
for m in range(24, 33):
    hit = None
    for seed in range(40):
        rng = random.Random(77000 + 100 * m + seed)
        v, st = R.anneal_at_support(fr10, rng, m, 20000)
        if v == 0:
            cert = C.certify(st, fr10)
            ce = [[tuple(e) for e in cert["colour_edges"][r]] for r in range(3)]
            ok, bad = AD.sc_admissible(ce)
            deg = AD.live_degrees(ce)
            geo, lab = AD.to_labels(ce)
            hit = dict(support=m, pures=cert["pures_product"],
                       both_methods_agree=cert["two_methods_agree"],
                       SC_admissible=ok, min_live_degree=min(deg),
                       W2_verdict=W2.analyse(geo, lab)["verdict"],
                       colour_edges=cert["colour_edges"])
            break
    out[f"N10_m{m}"] = hit
    print(f"N=10 m={m:3d}: " + ("none" if hit is None else
          f"HIT pures={hit['pures']} (SC)={hit['SC_admissible']} "
          f"mindeg={hit['min_live_degree']} W2={hit['W2_verdict']}"), flush=True)
json.dump(out, open("results_threshold10_low.json", "w"), indent=1)
hits = [k for k, v in out.items() if v]
print("hits:", hits)

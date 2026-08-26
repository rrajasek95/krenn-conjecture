#!/usr/bin/env python3
"""W29 G2 -- the encoder control at scale: MANY real X_3 diagonal sources at
N = 8, each pushed through the pipeline from all 8 solve sites at k = 3.

Any three pairwise disjoint perfect matchings M_0,M_1,M_2 of K_8, with
arbitrary nonzero weights whose product is 1 on each M_c, is an exact X_3
diagonal source: haf(t^c|V) = prod w^c = 1, and haf(t^c|V-{a,b}) is nonzero
only for {a,b} in M_c, where the disjointness gives t^d_{ab} = 0 for d != c.
(X_2 = X_3 here: at N = 8 the even profiles with off-count <= 3 are exactly
those with off-count <= 2, namely (8,0,0) and (6,2,0).)

Every one of these objects MUST satisfy every clause the encoder emits for its
own case.  A single violation means the encoder over-constrains.
"""
import json, random, sys, time
from fractions import Fraction
BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
sys.path.insert(0, BASE)
import w29_core as C
import run_c2_unified as U
import run_g1_x3control as G1
N, OUT = 8, f"{BASE}/results_g2_x3mass.json"
RES = {"n": N, "objects": 0, "site_checks": 0, "violations": 0,
       "no_normal_form": 0, "not_x3": 0, "cases_seen": {}, "examples": []}
pms = C.pm_list(tuple(range(N)))
rng = random.Random(20260819)
ntarget = int(sys.argv[1]) if len(sys.argv) > 1 else 150
t0 = time.time()
tries = 0
while RES["objects"] < ntarget and tries < 40000:
    tries += 1
    i, j, k = rng.sample(range(len(pms)), 3)
    Ms = [pms[i], pms[j], pms[k]]
    if len({e for M in Ms for e in M}) != 12:
        continue
    ts = [{}, {}, {}]
    for c, M in enumerate(Ms):
        ws = [Fraction(rng.randint(1, 6), rng.randint(1, 4)) for _ in M[:-1]]
        p = Fraction(1)
        for w in ws:
            p *= w
        ws.append(1 / p)
        for e, w in zip(M, ws):
            ts[c][e] = w
    if G1.x3_violations(ts):
        RES["not_x3"] += 1
        continue
    RES["objects"] += 1
    for z in range(N):
        co = U.case_of(ts, N, z, kmax=3)
        if co is None:
            RES["no_normal_form"] += 1
            continue
        ts2 = U.relabel(ts, co["perm"])
        Rs = tuple(tuple(x) for x in co["Rs"])
        key = str([list(r) for r in Rs])
        RES["cases_seen"][key] = RES["cases_seen"].get(key, 0) + 1
        van = U.build_van(N, Rs, kmax=3, z=N - 1)
        viol = U.z_assign(van, ts2)
        RES["site_checks"] += 1
        if viol:
            RES["violations"] += len(viol)
            if len(RES["examples"]) < 5:
                RES["examples"].append({"Rs": co["Rs"], "z": z,
                                        "viol": viol[:3]})
    if RES["objects"] % 25 == 0:
        print(f"  ... {RES['objects']} objects, {RES['site_checks']} site "
              f"checks, {RES['violations']} violations "
              f"({round(time.time()-t0,1)}s)", flush=True)
        json.dump(RES, open(OUT, "w"), indent=1, default=str)
RES["PASS"] = (RES["violations"] == 0 and RES["no_normal_form"] == 0
               and RES["objects"] >= 1)
RES["secs"] = round(time.time() - t0, 1)
json.dump(RES, open(OUT, "w"), indent=1, default=str)
print(f">>> {RES['objects']} X_3 objects x 8 sites = {RES['site_checks']} "
      f"encoder checks; violations {RES['violations']}; normal-form "
      f"failures {RES['no_normal_form']}; PASS {RES['PASS']}")

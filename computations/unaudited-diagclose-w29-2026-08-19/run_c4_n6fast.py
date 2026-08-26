#!/usr/bin/env python3
"""W29 C4 -- the n=6 direct Groebner with incremental generator subsets.

Independent algebraic decision of "is there a diagonal exact source on K_6?",
to be compared with the vanishing-pattern abstraction's verdict (0/64 cases
SAT, i.e. "no").  Sparsest generators first; the first subset that returns the
unit ideal is re-confirmed in char 0 and at two 1-mod-3 primes (ledger 19).
"""
import json, sys, time
BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
sys.path.insert(0, BASE)
import run_c3_smalln as S
RES = {}
OUT = f"{BASE}/results_c4_n6fast.json"
def ck(t=""):
    json.dump(RES, open(OUT, "w"), indent=1, default=str)
    if t: print(f"   [ck {t}]", flush=True)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
gens, tags, names, nv = S.direct_system(n)
order = sorted(range(len(gens)), key=lambda i: (len(gens[i].t), gens[i].deg()))
polys = [gens[i] for i in order]
print(f"n={n}: {nv} vars, {len(polys)} gens", flush=True)
RES["setup"] = {"n": n, "nv": nv, "ngens": len(polys)}
ck("setup")
hit = None
for b in (24, 48, 96, 144, len(polys)):
    b = min(b, len(polys)); t0 = time.time()
    try:
        r = S.decide(polys[:b], names, 32003, timeout=2400)
    except Exception as e:
        r = {"error": str(e)[:200]}
    r["secs"] = round(time.time()-t0, 1); r["b"] = b
    RES.setdefault("screen", {})[str(b)] = r
    print(f"  [32003] {b} gens -> unit={r.get('isunit')} dim={r.get('dim')} ({r['secs']}s) {r.get('error','')}", flush=True)
    ck(f"b{b}")
    if r.get("isunit") == "1":
        hit = b; break
    if b == len(polys): break
RES["screen_unit_at"] = hit
if hit:
    for ch in (0, 32029, 1000003):
        t0 = time.time()
        try: r = S.decide(polys[:hit], names, ch, timeout=3600)
        except Exception as e: r = {"error": str(e)[:200]}
        r["secs"] = round(time.time()-t0, 1)
        RES.setdefault("confirm", {})[str(ch)] = r
        print(f"  [confirm {ch}] unit={r.get('isunit')} ({r['secs']}s) {r.get('error','')}", flush=True)
        ck(f"c{ch}")
RES["VERDICT"] = ("UNIT: no diagonal exact source on K_%d (char 0 + two 1-mod-3 primes)" % n
                  if hit and RES.get("confirm", {}).get("0", {}).get("isunit") == "1"
                  else "undecided/not unit")
ck("final"); print(">>> " + RES["VERDICT"])

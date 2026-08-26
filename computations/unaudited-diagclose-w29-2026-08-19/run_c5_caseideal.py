#!/usr/bin/env python3
"""W29 C5 -- the INDEPENDENT ALGEBRAIC run of the SAME case ledger.

Same hypotheses as the abstraction, but decided by Groebner bases instead of
SAT.  For each case (R_0,R_1,R_2) of the W29-B2 ledger at order n, in the
variables t^c_e (e an edge of K_n, with the star entries t^c_{z y}, y not in
F_c, deleted -- they are 0 by W28-FREE) plus three Rabinowitsch variables:

    haf(t^c|V) - 1                                            c = 0,1,2
    haf(t^0|S_0) haf(t^1|S_1) haf(t^2|S_2)      all even partitions, not
                                                all-in-one
    haf(t^d|S_1) haf(t^e|S_2)                   y in F_c, even splits of
                                                V - z - y       (W28-FREE)
    zr_c * t^c_{z y_c} * haf(t^c|V-z-y_c) - 1   (the choice of y_c)

"unit for every case" is exactly the same theorem, proved by a different
engine.  At n = 4 the single case MUST be non-unit (a source exists).

argv: n [timeout]
"""
import json, sys, time
from itertools import combinations
BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
W28 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-x4empty-w28-2026-08-18")
for p in (BASE, W28): sys.path.insert(0, p)
import w28_core as K
import w29_core as C
import run_c3_smalln as S
import run_h1_higher as H
n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
tmo = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
PRIMES = (32029, 1000003)
OUT = f"{BASE}/results_c5_caseideal_n{n}.json"
RES = {"n": n, "cases": {}}
V = tuple(range(n)); z = n - 1; VP = tuple(range(n - 1))
E = list(combinations(V, 2)); ne = len(E)


def build(Rs):
    nv = 3 * ne + 3
    names = [f"zt{c}_{a}{b}" for c in range(3) for (a, b) in E] + \
            [f"zr{c}" for c in range(3)]
    W = [{e: K.Poly.var(nv, c * ne + E.index(e)) for e in E} for c in range(3)]
    F = [set([c]) | set(Rs[c]) for c in range(3)]
    zero, one = K.Poly.const(nv, 0), K.Poly.const(nv, 1)
    # W28-FREE: the star entries outside F_c vanish
    sub = {}
    for c in range(3):
        for y in VP:
            if y not in F[c]:
                W[c][C.ekey(z, y)] = zero
                sub[c * ne + E.index(C.ekey(z, y))] = True
    hf = {}
    def h(c, Sx):
        Sx = tuple(sorted(Sx))
        if (c, Sx) not in hf:
            hf[(c, Sx)] = C.haf(W[c], Sx, zero, one)
        return hf[(c, Sx)]
    gens = []
    for c in range(3):
        gens.append(h(c, V) - one)
    for m0 in range(0, n + 1, 2):
        for S0 in combinations(V, m0):
            R = [x for x in V if x not in S0]
            for m1 in range(0, len(R) + 1, 2):
                for S1 in combinations(R, m1):
                    S2 = tuple(x for x in R if x not in S1)
                    if max(len(S0), len(S1), len(S2)) == n: continue
                    g = h(0, S0) * h(1, S1) * h(2, S2)
                    if g.t: gens.append(g)
    for c in range(3):
        d, e = [x for x in range(3) if x != c]
        for y in sorted(F[c]):
            Wy = tuple(x for x in VP if x != y)
            for m in range(0, len(Wy) + 1, 2):
                for S1 in combinations(Wy, m):
                    S2 = tuple(x for x in Wy if x not in S1)
                    g = h(d, S1) * h(e, S2)
                    if g.t: gens.append(g)
        g = K.Poly.var(nv, 3 * ne + c) * W[c][C.ekey(z, c)] \
            * h(c, tuple(x for x in VP if x != c)) - one
        gens.append(g)
    keep = [i for i in range(nv) if i not in sub]
    idx = {v: i for i, v in enumerate(keep)}
    def sq(p):
        return K.Poly(len(keep), {tuple(k2[v] for v in keep): val
                                  for k2, val in p.t.items()})
    return [sq(p) for p in gens], [names[v] for v in keep]


Q = tuple(range(3, n - 1))
profs = H.profiles(len(Q))
t0 = time.time(); nnon = 0
for i, pr in enumerate(profs):
    Rs = H.triple_of(pr, Q)
    polys, names = build(Rs)
    polys.sort(key=lambda p: (len(p.t), p.deg()))
    rec = {"Rs": [list(r) for r in Rs], "nv": len(names), "ngens": len(polys)}
    for ch in (32003, 0) + PRIMES:
        try: r = S.decide(polys, names, ch, timeout=tmo)
        except Exception as ex: r = {"error": str(ex)[:160], "char": ch}
        rec[str(ch)] = r
        if r.get("isunit") != "1": break
    rec["UNIT"] = all(rec.get(str(c), {}).get("isunit") == "1"
                      for c in (0,) + PRIMES)
    if not rec["UNIT"]: nnon += 1
    RES["cases"][str(rec["Rs"])] = rec
    print(f"  case {i+1}/{len(profs)} Rs={rec['Rs']}: {rec['nv']} vars, "
          f"{rec['ngens']} gens -> unit(char0)="
          f"{rec.get('0',{}).get('isunit')} UNIT={rec['UNIT']}", flush=True)
    json.dump(RES, open(OUT, "w"), indent=1, default=str)
RES["n_cases"] = len(profs); RES["n_not_unit"] = nnon
RES["secs"] = round(time.time() - t0, 1)
RES["VERDICT"] = ("ALL CASES UNIT -- no diagonal exact source at N=%d, by "
                  "Groebner, independently of the SAT abstraction" % n
                  if nnon == 0 else f"{nnon} case(s) not unit")
json.dump(RES, open(OUT, "w"), indent=1, default=str)
print(">>> " + RES["VERDICT"])

#!/usr/bin/env python3
"""W29 C3 -- the INDEPENDENT ALGEBRAIC cross-check of the abstraction, at the
orders where the same system is small enough to decide by Groebner basis.

The direct diagonal system on K_n (no site solve, no case split, no
abstraction), in 3*C(n,2) variables:

    haf(t^c|V) - 1                                          c = 0,1,2
    haf(t^0|S_0) haf(t^1|S_1) haf(t^2|S_2)   for every ordered partition of V
                                             into three EVEN parts, not
                                             all-in-one.

n = 4 MUST be NOT unit (the three perfect matchings of K_4 are an exact
source).  n = 6 is decided here.  Whatever Singular says at n = 6 must AGREE
with the vanishing-pattern abstraction at n = 6 -- an algebra-vs-combinatorics
cross-check on a real instance of exactly the shape of the N = 8 claim.

argv: [n ...]
"""
from __future__ import annotations

import json
import sys
import time
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
W28 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-x4empty-w28-2026-08-18")
for p in (BASE, W28):
    if p not in sys.path:
        sys.path.insert(0, p)
import w28_core as K                                                # noqa: E402
import w29_core as C                                                # noqa: E402
import w29_k8van as KV                                              # noqa: E402
import run_c2_unified as U                                          # noqa: E402

RES, RAN = {}, []
OUT = f"{BASE}/results_c3_smalln.json"


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def direct_system(n):
    V = tuple(range(n))
    E = list(combinations(V, 2))
    nv = 3 * len(E)
    names = [f"zt{c}_{a}{b}" for c in range(3) for (a, b) in E]

    def idx(c, e):
        return c * len(E) + E.index(C.ekey(*e))

    W = [{e: K.Poly.var(nv, idx(c, e)) for e in E} for c in range(3)]
    zero, one = K.Poly.const(nv, 0), K.Poly.const(nv, 1)
    hf = {}

    def h(c, S):
        S = tuple(sorted(S))
        if (c, S) not in hf:
            hf[(c, S)] = C.haf(W[c], S, zero, one)
        return hf[(c, S)]

    gens, tags = [], []
    for c in range(3):
        gens.append(h(c, V) - one)
        tags.append(("PURE", c))
    for m0 in range(0, n + 1, 2):
        for S0 in combinations(V, m0):
            R = [x for x in V if x not in S0]
            for m1 in range(0, len(R) + 1, 2):
                for S1 in combinations(R, m1):
                    S2 = tuple(x for x in R if x not in S1)
                    if max(len(S0), len(S1), len(S2)) == n:
                        continue
                    g = h(0, S0) * h(1, S1) * h(2, S2)
                    if g.t:
                        gens.append(g)
                        tags.append(("MIX", S0, S1, S2))
    return gens, tags, names, nv


def emit(polys, names, char):
    polys = K.clear_denoms(list(polys))[0]
    lines = [f"ring zzR = {char}, ({','.join(names)}), dp;",
             "option(redSB);",
             "ideal zzJ = " + ",\n ".join(p.sing(names) for p in polys) + ";",
             "ideal zzG = std(zzJ);",
             '"NGENS "; size(zzG);',
             '"ISUNIT "; int zzu = 0; if (size(zzG)==1 and zzG[1]==1)'
             ' { zzu = 1; } zzu;',
             '"DIM "; dim(zzG);']
    sc = "\n".join(lines)
    C.no_shadow_guard(sc, set(names))
    return sc


def decide(polys, names, char, timeout=3000):
    out = C.run_singular(emit(polys, names, char), timeout=timeout)
    tk = out.split()
    return {"isunit": tk[tk.index("ISUNIT") + 1],
            "dim": tk[tk.index("DIM") + 1],
            "ngens_std": tk[tk.index("NGENS") + 1], "char": char}


def van_all_cases(n, kmax=None):
    """The unified abstraction over the whole free-set ledger at order n."""
    Q = tuple(range(3, n - 1))
    allR = [tuple(S) for k in range(len(Q) + 1) for S in combinations(Q, k)]
    nsat, tot, sats = 0, 0, []
    for R0 in allR:
        for R1 in allR:
            for R2 in allR:
                van = U.build_van(n, (R0, R1, R2), kmax=kmax)
                tot += 1
                if not van.is_unsat():
                    nsat += 1
                    if len(sats) < 10:
                        sats.append([list(R0), list(R1), list(R2)])
    return {"n_cases": tot, "n_sat": nsat, "sat_examples": sats}


def main():
    ns = [int(a) for a in sys.argv[1:]] or [4, 6]
    for n in ns:
        t0 = time.time()
        print(f"=== C3 order n = {n} ===", flush=True)
        gens, tags, names, nv = direct_system(n)
        print(f"  direct system: {nv} variables, {len(gens)} generators",
              flush=True)
        rec = {"n": n, "nv": nv, "n_gens": len(gens)}
        va = van_all_cases(n)
        rec["abstraction"] = va
        print(f"  abstraction over the free-set ledger: {va['n_cases']} "
              f"cases, {va['n_sat']} SAT", flush=True)
        RES.setdefault("orders", {})[str(n)] = rec
        RAN.append(f"n{n}_abstraction")
        ck(f"n{n}_van")
        order = sorted(range(len(gens)), key=lambda i: (len(gens[i].t),
                                                        gens[i].deg()))
        polys = [gens[i] for i in order]
        for char in (32003, 0):
            try:
                r = decide(polys, names, char,
                           timeout=2400 if n <= 6 else 5400)
            except Exception as exc:
                r = {"error": str(exc)[:220], "char": char}
            r["secs"] = round(time.time() - t0, 1)
            rec.setdefault("groebner", {})[str(char)] = r
            print(f"  [char {char}] unit={r.get('isunit')} dim={r.get('dim')}"
                  f" {r.get('error','')} ({r['secs']}s)", flush=True)
            ck(f"n{n}_char{char}")
            if r.get("isunit") == "0":
                break
        gv = rec.get("groebner", {}).get("0", {}).get("isunit")
        rec["AGREEMENT"] = {
            "groebner_says_no_source": gv == "1",
            "abstraction_says_no_source": va["n_sat"] == 0,
            "AGREE": (gv == "1") == (va["n_sat"] == 0) if gv else None}
        print(f"  >>> n={n}: Groebner unit={gv}; abstraction SAT="
              f"{va['n_sat']}; agree={rec['AGREEMENT']['AGREE']}", flush=True)
        RAN.append(f"n{n}_groebner")
        ck(f"n{n}_final")
    ck("final")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""W28 T1h -- THE THREE-FREE-SITE ELIMINATION (the whole diagonal family).

W28-FREE applied to all three colours at once: an X_4 point at N = 8 whose
background at the solve site z is DIAGONAL needs, for each colour c, a site
y_c in V' = V - z with

    haf(t^d|S_1) haf(t^e|S_2) = 0   for EVERY even split (S_1,S_2) of V' - y_c
                                    ({d,e} = the other two colours)
    and  haf(t^c | V' - y_c) != 0,

and the three y_c are DISTINCT (the second condition at y_c contradicts the
first at y_d for d != c).  Up to relabelling the sites (the diagonal family is
S_7-invariant) we may take y_0, y_1, y_2 = 0, 1, 2.  So the WHOLE diagonal
family is killed as soon as

    1  in  < the 3 x 32 split equations >  +  < zt_c * haf(t^c|V' - y_c) - 1 >

-- 63 weight parameters plus three Rabinowitsch variables, but 96 highly
structured equations.  This ideal uses ONLY the (6,2,0) and (4,2,2) word
conditions; it does not even need (4,4,0).

argv: [mode] [timeout]
"""
from __future__ import annotations

import json
import sys
import time
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
sys.path.insert(0, BASE)
import w28_core as K                                              # noqa: E402
import run_t1d_diagelim as D                                      # noqa: E402

NS = 7
VP = tuple(range(NS))
RES = {}
OUT = None


def ck(tag=""):
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def even_splits(W):
    out = []
    for m in range(0, len(W) + 1, 2):
        for S1 in combinations(W, m):
            out.append((S1, tuple(x for x in W if x not in S1)))
    return out


def main():
    global OUT
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    tmo = int(sys.argv[2]) if len(sys.argv) > 2 else 1800
    ys = tuple(int(c) for c in (sys.argv[3] if len(sys.argv) > 3 else "012"))
    OUT = f"{BASE}/results_t1h_triplefree_{mode}_{''.join(map(str,ys))}.json"
    t, names0, nv0, xoff = D.build_symbolic(mode)
    names0 = names0[:xoff]
    nv = xoff + 3

    def lift(p):
        return K.Poly(nv, {k2 + (0, 0, 0): v for k2, v in p.t.items()})

    hc = {}

    def haf_c(c, Sset):
        key = (c, Sset)
        if key not in hc:
            hc[key] = lift(D.haf_poly(t[c], Sset, xoff))
        return hc[key]

    gens = []
    tags = []
    for c in range(3):
        d, e = [x for x in range(3) if x != c]
        y = ys[c]
        W = tuple(x for x in VP if x != y)
        for (S1, S2) in even_splits(W):
            P = haf_c(d, S1) * haf_c(e, S2)
            if P.t:
                gens.append(P)
                tags.append(("FREE", c, y, S1, S2))
    # the three "constant row nonzero" side conditions, Rabinowitsch
    rab = []
    for c in range(3):
        W = tuple(x for x in VP if x != ys[c])
        rab.append(haf_c(c, W) * K.Poly.var(nv, xoff + c)
                   - K.Poly.const(nv, 1))
    names = names0 + ["zt0", "zt1", "zt2"]
    polys = K.clear_denoms(gens + rab)[0]
    used = set()
    for p in polys:
        for k2 in p.t:
            for i, e2 in enumerate(k2):
                if e2:
                    used.add(i)
    used = sorted(used)
    nvc = len(used)

    def squash(p):
        return K.Poly(nvc, {tuple(k2[v] for v in used): val
                            for k2, val in p.t.items()})
    polys = [squash(p) for p in polys]
    nm = [names[v] for v in used]
    print(f"mode {mode}, free sites {ys}: {len(polys)} generators, "
          f"{nv} -> {nvc} variables after compression")
    RES["setup"] = {"mode": mode, "free_sites": list(ys), "nparam": xoff,
                    "n_generators": len(polys), "nvars": nvc}
    ck("setup")
    # everything is homogeneous-free: put the three Rabinowitsch relations
    # first (they are the only inhomogeneous ones)
    ce = polys[-1]
    rest = polys[:-1]
    rest.sort(key=lambda p: (len(p.t), p.deg()))
    for char in (32003, 1000003, 0):
        t1 = time.time()
        try:
            r = D.decide(rest, ce, nm, char, timeout=tmo)
        except Exception as exc:
            r = {"error": str(exc)[:250]}
        r["secs"] = round(time.time() - t1, 1)
        print(f"   [char {char}] -> {r}", flush=True)
        RES.setdefault("verdict", {})[str(char)] = r
        ck(f"char{char}")
        if r.get("isunit") == "0":
            break
    v = RES.get("verdict", {}).get("0", {}).get("isunit")
    RES["conclusion"] = (
        "NO DIAGONAL BACKGROUND AT N=8 IS X_4-FEASIBLE FOR ALL THREE COLOURS "
        "[proved, char 0]" if v == "1" else
        "not decided in char 0" if v is None else
        "the three-free-site relaxation admits points -- inconclusive, the "
        "finer conditions are needed")
    print(f">>> {RES['conclusion']}")
    RES["seconds"] = round(time.time() - t0, 1)
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()

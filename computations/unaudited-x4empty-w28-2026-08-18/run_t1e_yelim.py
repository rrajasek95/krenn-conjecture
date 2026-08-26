#!/usr/bin/env python3
"""W28 T1e -- THE DIAGONAL-BACKGROUND ELIMINATION, case-split by the free site.

W28-DEC (run_t1d) reduced the colour-0 system at z on a DIAGONAL background to
seven unknowns x_y (y in V' = V - z) with generators, one per partition
V' = S_0 + S_1 + S_2 with |S_0| odd and |S_1|,|S_2| even,

    P(S_1,S_2) * q(S_0) = 0,   P = haf(t^1|S_1) haf(t^2|S_2),
                               q(S_0) = sum_{y in S_0} haf(t^0|S_0 - y) x_y,
    and the inhomogeneous  q(V') = 1.

W28-FREE [PROVED-HERE].  The partitions with |S_0| = 1 have q({y}) = x_y
(haf over the empty set is 1), so each of them reads P(S_1,S_2) * x_y = 0.
Hence x_y = 0 as soon as ONE even split (S_1,S_2) of W_y := V' - y has
haf(t^1|S_1) haf(t^2|S_2) != 0.  Since q(V') = 1 needs some x_y != 0:

    FEASIBLE  ==>  there is a site y in V' -- the FREE SITE -- with
        haf(t^1|S_1) haf(t^2|S_2) = 0 for EVERY even split of W_y
    (in particular haf(t^1|W_y) = haf(t^2|W_y) = 0),  and haf(t^0|W_y) != 0.

Applying the same to the colour-1 and colour-2 systems gives THREE DISTINCT
free sites y_0, y_1, y_2 (distinct because haf(t^c|W_{y_c}) != 0 while
haf(t^c|W_{y_d}) = 0 for d != c).

So the decision becomes: for each y, is
    I_y = < the 32 split equations at y > + < all mixed generators >
          + < q(V') - 1 >
the unit ideal?   INFEASIBLE EVERYWHERE  <=>  1 in I_y for every y.
For the FULL diagonal family the site relabelling S_7 is a symmetry, so ONE y
suffices; for the sigma-slice the sigma-orbits {0,1,2},{3,4,5},{6} give three.

argv: <mode> <kmax> <ylist|auto> [timeout]
"""
from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
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
    W = tuple(W)
    for m in range(0, len(W) + 1, 2):
        for S1 in combinations(W, m):
            out.append((S1, tuple(x for x in W if x not in S1)))
    return out


def main():
    global OUT
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "sigma"
    kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    ysel = sys.argv[3] if len(sys.argv) > 3 else "auto"
    tmo = int(sys.argv[4]) if len(sys.argv) > 4 else 1200
    OUT = f"{BASE}/results_t1e_yelim_{mode}_k{kmax}.json"
    t, names, nv, xoff = D.build_symbolic(mode)
    gens, const_eq = D.build_generators(t, nv, xoff, kmax)
    print(f"mode {mode} kmax {kmax}: {xoff} weight parameters + {NS} unknowns "
          f"= {nv} variables; {len(gens)} mixed generators")
    RES["setup"] = {"mode": mode, "kmax": kmax, "nparam": xoff, "nv": nv,
                    "n_mixed": len(gens)}
    ck("setup")

    if ysel == "auto":
        ys = [6] if mode == "full" else ([0, 3, 6] if mode == "sigma"
                                         else [0])
    else:
        ys = [int(c) for c in ysel]
    print(f"   free-site cases to decide: {ys} "
          f"({'S_7 relabelling makes one case enough' if mode == 'full' else 'one per orbit of the slice symmetry'})")

    ce = K.clear_denoms([const_eq])[0][0]
    allv = {}
    for y in ys:
        W = tuple(x for x in VP if x != y)
        split = []
        for (S1, S2) in even_splits(W):
            P = D.haf_poly(t[1], S1, nv) * D.haf_poly(t[2], S2, nv)
            if P.t:
                split.append(P)
        # mixed generators, ordered  |S_0| ascending then sparsity
        mixed = sorted(gens, key=lambda g: (len(g[0]), len(g[3].t)))
        polys = split + [g[3] for g in mixed]
        polys = K.clear_denoms(polys)[0]
        print(f"   y={y}: {len(split)} split equations + {len(mixed)} mixed",
              flush=True)
        res = {}
        for char in (32003, 1000003, 0):
            found = None
            for b in (len(polys), len(split) + 128, len(split) + 32,
                      len(split)):
                b = min(b, len(polys))
                t1 = time.time()
                try:
                    r = D.decide(polys[:b], ce, names, char, timeout=tmo)
                except Exception as exc:
                    print(f"      [y{y} char {char}] {b} gens FAILED "
                          f"{str(exc)[:140]}", flush=True)
                    res.setdefault(str(char), {})[str(b)] = {
                        "error": str(exc)[:250]}
                    RES.setdefault("cases", {})[str(y)] = res
                    ck(f"y{y}c{char}b{b}")
                    break
                r["ngens_used"] = b
                r["secs"] = round(time.time() - t1, 1)
                print(f"      [y{y} char {char}] {b} gens -> dim {r['dim']} "
                      f"unit {r['isunit']} ({r['secs']}s)", flush=True)
                res.setdefault(str(char), {})[str(b)] = r
                RES.setdefault("cases", {})[str(y)] = res
                ck(f"y{y}c{char}b{b}")
                if r["isunit"] == "1":
                    found = b
                    continue        # shrink further: hunt a small certificate
                if b == len(polys):
                    break           # the FULL ideal is not unit -> decided
                break               # a subset failed; keep the last success
            res.setdefault("verdict", {})[str(char)] = (
                f"UNIT with {found} generators" if found else "NOT unit")
            RES.setdefault("cases", {})[str(y)] = res
            ck(f"y{y}char{char}")
        allv[y] = res.get("verdict", {})
    RES["summary"] = {str(k): v for k, v in allv.items()}
    ok = all(v.get("0", "").startswith("UNIT") for v in allv.values())
    RES["verdict"] = ("DIAGONAL BACKGROUNDS ARE X_4-INFEASIBLE EVERYWHERE "
                      "[proved, char 0]" if ok else "not decided")
    print(f">>> {RES['verdict']}")
    RES["seconds"] = round(time.time() - t0, 1)
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""A8 T4 -- the free-set ideals of W28-T1, MY OWN encoding.

usage: run_t4_ideals.py <kmax> <tag> <Y-list, e.g. 0|01|0123> [timeout]
Each Y is decided in char 0 and char 1000003 (= 1 mod 3, ledger 19) and 32003.
"""
import json
import sys
import time

BASE = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a8-2026-08-19"
sys.path.insert(0, BASE)
import a8_sym as S
from a8_sing import decide_unit

kmax = int(sys.argv[1])
tag = sys.argv[2]
Ys = [tuple(int(c) for c in s) for s in sys.argv[3].split("|")]
TMO = int(sys.argv[4]) if len(sys.argv) > 4 else 900
CHARS = [0, 1000003, 32003]

OUT = f"{BASE}/results_t4_ideals_{tag}_k{kmax}.json"
RES = {"kmax": kmax, "cases": {}}


def emit(Y):
    t = S.sym_t()
    gens, tags, ce, nv = S.build_ideal(t, S.NPAR, Y, kmax)
    polys = gens + [ce]
    used = sorted({i for p in polys for k in p.t for i, e in enumerate(k) if e})
    ridx = {v: i for i, v in enumerate(used)}
    nvc = len(used)

    def squash(p):
        return S.P(nvc, {tuple(k[v] for v in used): val for k, val in p.t.items()})

    names = []
    for v in used:
        names.append(f"zza{v}" if v < S.NPAR else f"zzx{v - S.NPAR}")
    sq = [squash(p) for p in polys]
    return names, [p.to_singular(names) for p in sq], nvc, len(gens)


for Y in Ys:
    t0 = time.time()
    names, polys, nvc, ng = emit(Y)
    rec = dict(Y=list(Y), nvars=nvc, ngens=ng + 1, names=names)
    print(f"=== Y={Y}  k={kmax}: {ng+1} generators in {nvc} variables", flush=True)
    for ch in CHARS:
        r = decide_unit(names, polys, char=ch, timeout=TMO)
        rec[f"char{ch}"] = r
        print(f"    char {ch:>7}: {r.get('status')} unit={r.get('unit')} "
              f"dim={r.get('dim')} ({time.time()-t0:.0f}s)", flush=True)
        RES["cases"][str(Y)] = rec
        with open(OUT, "w") as fh:
            json.dump(RES, fh, indent=1, default=str)
    RES["cases"][str(Y)] = rec
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
print("wrote", OUT)

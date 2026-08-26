#!/usr/bin/env python3
"""W28 T1g -- the diagonal elimination CASE-SPLIT ON THE FREE-SITE SET.

By W28-FREE the colour-0 star x is supported on the FREE SITES
F = {y : every even split (S_1,S_2) of V' - y has haf(t^1|S_1)haf(t^2|S_2) = 0}
and q(V') = 1 forces F != empty.  So, writing Y for the (unknown) free set,

    FEASIBLE  <=>  for SOME nonempty Y subset V':  I_Y has a solution,

    I_Y = < haf(t^1|S_1) haf(t^2|S_2) : y in Y, (S_1,S_2) an even split of
                                        V' - y >                    (Y is free)
        + < P(S_1,S_2) * sum_{y in S_0 cap Y} haf(t^0|S_0 - y) x_y >   (mixed)
        + < sum_{y in Y} haf(t^0|V' - y) x_y  -  1 >               (constant)

in nparam + |Y| variables -- for |Y| = 1 that is 21 + 1 = 22 on the sigma
slice, against 28 for the uncollapsed system, and the 32 "Y is free"
equations cut the variety hard.  INFEASIBLE EVERYWHERE <=> 1 in I_Y for every
nonempty Y (127 sets, far fewer up to the slice symmetry).

Each I_Y is a RELAXATION of the true case (we do not impose that sites outside
Y are non-free, which is a disjunction), so "1 in I_Y" is a sound kill.

argv: <mode> <sizes, e.g. 1 or 12 or 123> [timeout]
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
import w28_sym as S                                               # noqa: E402
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


def orbit_reps(mode, size, allsets=False):
    """Subsets Y of V' of the given size, one per orbit of the slice group.

    CAUTION (soundness): the sigma-slice symmetry carries the colour-0 system
    at Y to the colour-rho(0) system at sigma(Y), NOT to the colour-0 system,
    so the orbit reduction is NOT valid for a single-colour ideal on that
    slice -- pass allsets=True there.  For the FULL diagonal family the site
    relabelling S_7 acts with trivial colour action, so one Y per size is
    sound."""
    if allsets:
        return list(combinations(VP, size))
    if mode == "full":
        return [tuple(range(size))]                 # S_7 acts transitively
    sl = {"sigma": S.slice_sigma, "z7": S.slice_z7,
          "f21": S.slice_f21}[mode]()
    seen, reps = set(), []
    for Y in combinations(VP, size):
        if Y in seen:
            continue
        for (pi, rho) in sl.group:
            seen.add(tuple(sorted(pi[y] for y in Y)))
        reps.append(Y)
    return reps


def build_case(t, nv0, Y, kmax=4):
    """(generators, const_eq, names_extra) for the case 'free set contains Y'.

    Variables: the weight parameters (already in t) plus |Y| star unknowns
    appended AFTER them."""
    nv = nv0 + len(Y)
    pos = {y: nv0 + i for i, y in enumerate(Y)}

    def lift(p):
        return K.Poly(nv, {k2 + (0,) * len(Y): v for k2, v in p.t.items()})

    hc = {}

    def haf_c(c, Sset):
        key = (c, Sset)
        if key not in hc:
            hc[key] = lift(D.haf_poly(t[c], Sset, nv0))
        return hc[key]

    gens = []
    for y in Y:
        W = tuple(x for x in VP if x != y)
        for (S1, S2) in even_splits(W):
            # only splits whose word is actually CONSTRAINED at this rung may
            # be used to declare y free (at kmax = 4 that is all 32 of them;
            # at kmax = 3 only (6,0) and (0,6) survive)
            w = [0] * 8
            for u in S1:
                w[u] = 1
            for u in S2:
                w[u] = 2
            if K.offcount(tuple(w)) > kmax:
                continue
            P = haf_c(1, S1) * haf_c(2, S2)
            if P.t:
                gens.append(("FREE", y, S1, S2, P))
    const_eq = None
    for s in range(1, NS + 1, 2):
        for S0 in combinations(VP, s):
            inY = [y for y in S0 if y in pos]
            if not inY and s < NS:
                continue
            T = [x for x in VP if x not in S0]
            for m in range(0, len(T) + 1, 2):
                for S1 in combinations(T, m):
                    S2 = tuple(x for x in T if x not in S1)
                    w = [0] * 8
                    for y in S1:
                        w[y] = 1
                    for y in S2:
                        w[y] = 2
                    if K.offcount(tuple(w)) > kmax:
                        continue
                    q = K.Poly.const(nv, 0)
                    for y in inY:
                        q = q + haf_c(0, tuple(x for x in S0 if x != y)) \
                            * K.Poly.var(nv, pos[y])
                    if s == NS:
                        const_eq = q - K.Poly.const(nv, 1)
                        continue
                    if not q.t:
                        continue
                    P = haf_c(1, S1) * haf_c(2, S2)
                    if not P.t:
                        continue
                    g = P * q
                    if g.t:
                        gens.append(("MIX", S0, S1, S2, g))
    assert const_eq is not None
    return gens, const_eq, nv


def main():
    global OUT
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "sigma"
    sizes = [int(c) for c in (sys.argv[2] if len(sys.argv) > 2 else "1")]
    tmo = int(sys.argv[3]) if len(sys.argv) > 3 else 900
    kmax = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    allsets = (len(sys.argv) > 5 and sys.argv[5] == "all")
    OUT = (f"{BASE}/results_t1g_freeelim_{mode}_"
           f"{''.join(map(str,sizes))}_k{kmax}"
           f"{'_all' if allsets else ''}.json")
    t, names0, nv0, xoff = D.build_symbolic(mode)
    names0 = names0[:xoff]                # drop the 7 x-names; we add our own
    print(f"mode {mode}: {xoff} weight parameters")
    RES["setup"] = {"mode": mode, "nparam": xoff, "sizes": sizes,
                    "kmax": kmax}
    ck("setup")
    allk = {}
    for size in sizes:
        reps = orbit_reps(mode, size, allsets)
        print(f"=== |Y| = {size}: {len(reps)} cases up to the slice symmetry")
        for Y in reps:
            gens, ce, nv = build_case(t, xoff, Y, kmax)
            names = names0 + [f"zx{y}" for y in Y]
            polys = [g[-1] for g in gens]
            polys = K.clear_denoms(polys)[0]
            polys.sort(key=lambda p: (len(p.t), p.deg()))
            ce = K.clear_denoms([ce])[0][0]
            # RING COMPRESSION: only the variables that actually occur.  For
            # |Y| = {y} this drops every weight on an edge meeting y, so the
            # case really lives on the 6-set V' - y.
            used = set()
            for p in polys + [ce]:
                for k2 in p.t:
                    for i, e2 in enumerate(k2):
                        if e2:
                            used.add(i)
            used = sorted(used)
            ridx = {v: i for i, v in enumerate(used)}
            nvc = len(used)

            def squash(p):
                return K.Poly(nvc, {tuple(k2[v] for v in used): val
                                    for k2, val in p.t.items()})
            polys = [squash(p) for p in polys]
            ce = squash(ce)
            names = [names[v] for v in used]
            print(f"   Y={Y}: {len(polys)} generators, {nv} -> {nvc} "
                  f"variables after compression", flush=True)
            rec = {}
            for char in (32003, 0):
                t1 = time.time()
                try:
                    r = D.decide(polys, ce, names, char, timeout=tmo)
                except Exception as exc:
                    r = {"error": str(exc)[:200]}
                r["secs"] = round(time.time() - t1, 1)
                print(f"      [char {char}] -> {r}", flush=True)
                rec[str(char)] = r
                RES.setdefault("cases", {})[f"{size}:{Y}"] = rec
                ck(f"Y{Y}c{char}")
                if r.get("isunit") == "0":
                    break     # not unit: this case admits a point
            allk[f"{size}:{Y}"] = rec
    RES["summary"] = allk
    RES["seconds"] = round(time.time() - t0, 1)
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""W28 T1d -- THE DIAGONAL-BACKGROUND ELIMINATION (upgrades the 16,384-point
sigma-symmetric pattern grid to ALL COMPLEX WEIGHTS).

W28-DEC [PROVED-HERE].  If the background B on V' = V - {z} is DIAGONAL
(B_uv[i][j] = 0 for i != j, B_uv[c][c] =: t^c_uv) then the colour-0 system at
z DECOUPLES.  Indeed the cofactor of a word u on V' is

        C_y(u) = prod_c haf(t^c | S_c(u) - y),      S_c(u) = u^{-1}(c),

which vanishes unless every |S_c(u) - y| is even.  |S_0|+|S_1|+|S_2| = 7 is
odd, so either exactly one part is odd -- and then only y in that part
survives, putting the whole row in ONE of the three 7-column blocks -- or all
three are odd and the row is identically zero.  The constant word has the odd
part S_0 = V', so the right-hand side lives in the colour-0 block and the
colour-1/2 blocks carry only homogeneous rows (solved by x = 0).  Hence

    colour-0 feasible  <=>  exists x in C^{V'} with
        haf(t^1|S_1) haf(t^2|S_2) * ( sum_{y in S_0} haf(t^0|S_0 - y) x_y ) = 0
        for every partition V' = S_0 + S_1 + S_2 with |S_0| odd (>= 1, proper),
        |S_1|, |S_2| even,   AND   sum_y haf(t^0|V' - y) x_y = 1.

SEVEN unknowns, 546 mixed generators, all of degree 3 in the weights and 1 in
x -- and NO Rabinowitsch variable is needed (the constant equation is already
inhomogeneous).  Unit ideal  <=>  no such background exists over ANY field
extension of Q.

modes:  sigma (sigma-symmetric diagonal backgrounds: 21 weight parameters)
        z7 / f21 (9 / 3 parameters)
        full  (ALL diagonal backgrounds: 63 parameters -- the stretch goal)
argv: <mode> <kmax> [maxgens]
"""
from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
sys.path.insert(0, BASE)
import w28_core as K                                              # noqa: E402
import w28_sym as S                                               # noqa: E402

NS = 7
VP = tuple(range(NS))
RES = {}
RAN = []
OUT = None


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def build_symbolic(mode):
    """(t[c] as dict edge->Poly, names, nv, xoff)."""
    if mode == "full":
        nprm = 3 * len(list(combinations(VP, 2)))
        nv = nprm + NS
        names = []
        t = [{}, {}, {}]
        i = 0
        for (a, b) in combinations(VP, 2):
            for c in range(3):
                names.append(f"zt{c}_{a}{b}")
                t[c][(a, b)] = K.Poly.var(nv, i)
                i += 1
        names += [f"zx{y}" for y in range(NS)]
        return t, names, nv, nprm
    sl = {"sigma": S.slice_sigma, "z7": S.slice_z7,
          "f21": S.slice_f21}[mode]()
    nprm = 3 * sl.nblocks
    nv = nprm + NS
    names = [f"zp{b}{c}" for b in range(sl.nblocks) for c in range(3)]
    names += [f"zx{y}" for y in range(NS)]
    blocks = []
    for b in range(sl.nblocks):
        M = [[K.Poly.const(nv, 0)] * 3 for _ in range(3)]
        M = [[K.Poly.const(nv, 0) for _ in range(3)] for _ in range(3)]
        for c in range(3):
            M[c][c] = K.Poly.var(nv, 3 * b + c)
        blocks.append(M)
    src7 = sl.build(blocks)
    t = [{}, {}, {}]
    for (a, b) in combinations(VP, 2):
        for c in range(3):
            t[c][(a, b)] = src7[(a, b)][c][c]
    return t, names, nv, nprm


def haf_poly(tc, sites, nv):
    zero, one = K.Poly.const(nv, 0), K.Poly.const(nv, 1)

    def wt(i, j):
        return tc[(i, j) if i < j else (j, i)]

    v = K.haf_rec(wt, tuple(sorted(sites)), {}, one, zero)
    return v if isinstance(v, K.Poly) else K.Poly.const(nv, v)


def build_generators(t, nv, xoff, kmax=4):
    """[(S_0, S_1, S_2, poly)] plus the inhomogeneous constant equation."""
    q = {}          # q[S_0] = sum_y haf(t^0|S_0-y) x_y
    gens = []
    const_eq = None
    hafc = {}

    def haf_c(c, S):
        key = (c, S)
        if key not in hafc:
            hafc[key] = haf_poly(t[c], S, nv)
        return hafc[key]

    for s in range(1, NS + 1, 2):
        for S0 in combinations(VP, s):
            qq = K.Poly.const(nv, 0)
            for y in S0:
                qq = qq + haf_c(0, tuple(x for x in S0 if x != y)) \
                    * K.Poly.var(nv, xoff + y)
            q[S0] = qq
    for s in range(1, NS + 1, 2):
        for S0 in combinations(VP, s):
            T = [x for x in VP if x not in S0]
            for m in range(len(T) + 1):
                for S1 in combinations(T, m):
                    if m % 2:
                        continue
                    S2 = tuple(x for x in T if x not in S1)
                    # off-count of the extended word must be <= kmax
                    w = [0] * 8
                    for y in S1:
                        w[y] = 1
                    for y in S2:
                        w[y] = 2
                    if K.offcount(tuple(w)) > kmax:
                        continue
                    if s == NS:
                        const_eq = q[S0] - K.Poly.const(nv, 1)
                        continue
                    P = haf_c(1, S1) * haf_c(2, S2)
                    if not P.t:
                        continue
                    g = P * q[S0]
                    if g.t:
                        gens.append((S0, S1, S2, g))
    assert const_eq is not None
    return gens, const_eq


def emit(gens, const_eq, names, char):
    lines = ['LIB "elim.lib";',
             f"ring zzR = {char}, ({','.join(names)}), dp;",
             f"ideal zzJ = {const_eq.sing(names)}"]
    for g in gens:
        lines.append(f"  , {g.sing(names)}")
    lines.append(";")
    lines.append("option(redSB);")
    lines.append("ideal zzG = std(zzJ);")
    lines.append('"NGENS "; size(zzG);')
    lines.append('"DIM "; dim(zzG);')
    lines.append('"ISUNIT "; int zzu = 0; if (size(zzG)==1 and zzG[1]==1)'
                 ' { zzu = 1; } zzu;')
    sc = "\n".join(lines)
    K.no_shadow_guard(sc, set(names))
    return sc


def decide(gens, const_eq, names, char, timeout=2400):
    out = K.run_singular(emit(gens, const_eq, names, char), timeout=timeout)
    tk = out.split()
    return {"dim": tk[tk.index("DIM") + 1], "isunit": tk[tk.index("ISUNIT") + 1],
            "ngens_std": tk[tk.index("NGENS") + 1]}


def main():
    global OUT
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "sigma"
    kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    maxg = int(sys.argv[3]) if len(sys.argv) > 3 else 600
    OUT = f"{BASE}/results_t1d_diagelim_{mode}_k{kmax}.json"
    print(f"mode {mode}, kmax {kmax}")
    t, names, nv, xoff = build_symbolic(mode)
    print(f"   {xoff} weight parameters + {NS} unknowns = {nv} variables")
    gens, const_eq = build_generators(t, nv, xoff, kmax)
    print(f"   {len(gens)} mixed generators (nonzero), constant equation "
          f"{len(const_eq.t)} terms")
    RES["setup"] = {"mode": mode, "kmax": kmax, "nparam": xoff, "nv": nv,
                    "n_generators": len(gens),
                    "gen_degrees": sorted(set(g[3].deg() for g in gens))}
    ck("setup")
    polys = [g[3] for g in gens]
    polys, L = K.clear_denoms(polys)
    order = sorted(range(len(polys)), key=lambda i: (len(polys[i].t),
                                                     polys[i].deg()))
    polys = [polys[i] for i in order]
    tags = [gens[i][:3] for i in order]
    ce = K.clear_denoms([const_eq])[0][0]

    for char in (32003, 1000003, 0):
        found = None
        for b in (2, 4, 8, 16, 32, 64, 128, 256, min(600, len(polys)),
                  len(polys)):
            b = min(b, len(polys))
            t1 = time.time()
            try:
                r = decide(polys[:b], ce, names, char)
            except Exception as exc:
                print(f"      [char {char}] {b} gens FAILED "
                      f"{str(exc)[:160]}", flush=True)
                RES.setdefault("verdicts", {}).setdefault(str(char), {})[
                    str(b)] = {"error": str(exc)[:300]}
                ck(f"c{char}b{b}")
                break
            r["ngens_used"] = b
            r["secs"] = round(time.time() - t1, 1)
            print(f"      [char {char}] {b} gens -> dim {r['dim']} unit "
                  f"{r['isunit']} ({r['secs']}s)", flush=True)
            RES.setdefault("verdicts", {}).setdefault(str(char), {})[str(b)] = r
            ck(f"c{char}b{b}")
            if r["isunit"] == "1":
                found = {"ngens": b, "certificate_words":
                         [str(x) for x in tags[:b]]}
                break
            if b == len(polys):
                break
        RES.setdefault("certificate", {})[str(char)] = found
        print(f"   >>> char {char}: "
              f"{'INFEASIBLE EVERYWHERE (unit ideal)' if found else 'NOT unit'}"
              f" {found['ngens'] if found else ''}", flush=True)
        ck(f"char{char}")
    RES["seconds"] = round(time.time() - t0, 1)
    RAN.append(f"T1d_{mode}_k{kmax}")
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()

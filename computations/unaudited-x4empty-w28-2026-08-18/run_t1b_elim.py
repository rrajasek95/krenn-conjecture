#!/usr/bin/env python3
"""W28 T1b -- THE SYMMETRIC-SLICE ELIMINATION (the named feasible attack).

By W28-SYM (run_t1a) the colour-c system at z on a background invariant under a
colour-trivial transitive site group has an INVARIANT solution if it has any,
so it collapses to THREE unknowns (x_0, x_1, x_2), and after the (licensed)
normalisation x_0 = 1 to TWO.  Hence for the slice

    feasible at a background  <=>  the affine system
          A_0(u) + A_1(u) x_1 + A_2(u) x_2 = 0     (u mixed, constrained)
    is consistent AND the constant coefficient A_0(const) != 0,

where A_d(u) = sum_{y : u_y = d} Haf_{V' - y}(B)_u is a POLYNOMIAL in the
free block entries of the slice (degree 3: the hafnian of 6 sites).

So the whole slice is decided by ONE ideal-membership question

    1 in < A_0(u) + A_1(u) x_1 + A_2(u) x_2 ;  zt * A_0(const) - 1 >   ?

(Rabinowitsch for the "constant row nonzero" side condition.)  If YES the
slice is INFEASIBLE EVERYWHERE over every field extension of Q -- a theorem.
If NO, V(J) is nonempty over C and the slice CONTAINS an X_4 point at N = 8.

Slices: F21 (1 free block, 9 parameters) and Z7 (3 free blocks, 27).
Ladder calibration: the SAME pipeline is run at k = 1, 2, 3, 4; k = 1 is known
to have feasible symmetric backgrounds, so a pipeline that reports "empty"
there would be broken (ledger 18/20).

argv: <slice> <kmin> <kmax> [maxgens]
"""
from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from itertools import product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
sys.path.insert(0, BASE)
import w28_core as K                                              # noqa: E402
import w28_sym as S                                               # noqa: E402

NS = 7
RES = {}
RAN = []
OUT = None


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


# ------------------------------------------------------ symbolic background

def symbolic_slice(sl):
    """Background whose entries are Poly variables m<bi><i><j>; returns
    (src7, names, nv)."""
    nv = 9 * sl.nblocks + 2                     # + x1, x2
    names = [f"zm{b}{i}{j}" for b in range(sl.nblocks)
             for i in range(3) for j in range(3)] + ["zx1", "zx2"]
    blocks = []
    for b in range(sl.nblocks):
        blocks.append([[K.Poly.var(nv, 9 * b + 3 * i + j) for j in range(3)]
                       for i in range(3)])
    return sl.build(blocks), names, nv


def sym_haf(src, word, sites, nv):
    zero = K.Poly.const(nv, 0)
    one = K.Poly.const(nv, 1)

    def wt(i, j):
        return K.oriented(src, i, j)[word[i]][word[j]]

    v = K.haf_rec(wt, tuple(sorted(sites)), {}, one, zero)
    return v if isinstance(v, K.Poly) else K.Poly.const(nv, v)


def rows_symbolic(src7, c, k, nv):
    """[(u, A_0, A_1, A_2)] for the constrained words, constant word first."""
    uord = S.constrained_u(c, k)
    out = []
    for u in uord:
        A = [K.Poly.const(nv, 0) for _ in range(3)]
        for y in range(NS):
            Sy = tuple(x for x in range(NS) if x != y)
            cof = sym_haf(src7, {a: u[a] for a in Sy}, Sy, nv)
            A[u[y]] = A[u[y]] + cof
        out.append((u, A[0], A[1], A[2]))
    return out


# --------------------------------------------------------------- Singular

def emit(gens, kpoly, names, nv, char=0, extra=""):
    ring = f"ring zzR = {char}, ({','.join(names)},zt), dp;"
    lines = [f'LIB "elim.lib";', ring]
    lines.append(f"poly zzK = {kpoly.sing(names)};")
    lines.append("ideal zzJ = zt*zzK-1")
    for g in gens:
        lines.append(f"  , {g.sing(names)}")
    lines.append(";")
    lines.append("option(redSB);")
    lines.append("ideal zzG = std(zzJ);")
    lines.append('"NGENS "; size(zzG);')
    lines.append('"DIM "; dim(zzG);')
    lines.append('"ISUNIT "; int zzu = 0; if (size(zzG)==1 and zzG[1]==1)'
                 ' { zzu = 1; } zzu;')
    lines.append(extra)
    script = "\n".join(lines)
    K.no_shadow_guard(script, set(names) | {"zt"})
    return script


def decide(gens, kpoly, names, nv, char=0, timeout=1800):
    script = emit(gens, kpoly, names, nv, char)
    out = K.run_singular(script, timeout=timeout)
    toks = out.split()
    def grab(tag):
        i = toks.index(tag)
        return toks[i + 1]
    return {"dim": grab("DIM"), "isunit": grab("ISUNIT"),
            "ngens_std": grab("NGENS"), "raw": out[-400:]}


def incremental_decide(polys, kpoly, names, nv, char=0, batches=None,
                       timeout=1800, label=""):
    """Add generators in batches until the ideal is the unit ideal; returns the
    smallest batch prefix that already proves it (certificate size)."""
    if batches is None:
        batches = [4, 8, 16, 32, 64, 128, 256, 512, len(polys)]
    prev = None
    for b in batches:
        b = min(b, len(polys))
        t0 = time.time()
        r = decide(polys[:b], kpoly, names, nv, char, timeout)
        r["ngens_used"] = b
        r["secs"] = round(time.time() - t0, 1)
        print(f"      [{label} char {char}] {b} generators -> dim {r['dim']} "
              f"unit {r['isunit']} ({r['secs']}s)", flush=True)
        prev = r
        if r["isunit"] == "1":
            return r
        if b == len(polys):
            return r
    return prev


def main():
    global OUT
    t0 = time.time()
    which = sys.argv[1] if len(sys.argv) > 1 else "F21"
    kmin = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    kmax = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    maxg = int(sys.argv[4]) if len(sys.argv) > 4 else 400
    OUT = f"{BASE}/results_t1b_elim_{which}.json"
    sl = {"F21": S.slice_f21, "Z7": S.slice_z7, "sigma": S.slice_sigma}[which]()
    print(f"slice {sl.name}: |G| {len(sl.group)}, free blocks {sl.nblocks}, "
          f"{sl.nparam} background parameters")
    src7, names, nv = symbolic_slice(sl)
    RES["slice"] = {"name": sl.name, "group_order": len(sl.group),
                    "free_blocks": sl.nblocks, "nparam": sl.nparam,
                    "variables": names}

    for k in range(kmin, kmax + 1):
        print("=" * 74)
        print(f"(k = {k})  building the symbolic averaged system")
        print("=" * 74)
        t1 = time.time()
        rs = rows_symbolic(src7, 0, k, nv)
        const = rs[0]
        assert const[0] == (0,) * NS, const[0]
        kpoly = const[1]
        assert const[2].t == {} and const[3].t == {}, "constant row not pure"
        # dedupe mixed rows up to a rational scalar
        seen = {}
        polys = []
        for (u, a0, a1, a2) in rs[1:]:
            if not (a0.t or a1.t or a2.t):
                continue
            key = []
            for p in (a0, a1, a2):
                key.append(tuple(sorted(p.t.items())))
            key = tuple(key)
            if key in seen:
                continue
            seen[key] = u
            polys.append((u, a0 + a1 * K.Poly.var(nv, nv - 2)
                          + a2 * K.Poly.var(nv, nv - 1)))
        polys.sort(key=lambda t: (len(t[1].t), t[1].deg()))
        gens = [p for (u, p) in polys][:maxg]
        gens, L = K.clear_denoms(gens)
        kpoly, L2 = K.clear_denoms([kpoly])
        kpoly = kpoly[0]
        print(f"   constrained words {len(rs)}; distinct mixed rows "
              f"{len(polys)}; using {len(gens)}; K = {len(kpoly.t)} terms, "
              f"deg {kpoly.deg()} ({round(time.time()-t1,1)}s)")
        RES.setdefault("systems", {})[str(k)] = {
            "n_words": len(rs), "n_distinct_rows": len(polys),
            "n_used": len(gens), "K_terms": len(kpoly.t),
            "gen_degrees": sorted(set(g.deg() for g in gens))}
        ck(f"build{k}")

        res = {}
        for char in (32003, 1000003, 0):
            try:
                r = incremental_decide(gens, kpoly, names, nv, char,
                                       label=f"{sl.name} k={k}")
            except Exception as exc:
                r = {"error": str(exc)[:400]}
                print(f"      [char {char}] FAILED: {str(exc)[:200]}",
                      flush=True)
            res[str(char)] = r
            RES.setdefault("verdicts", {}).setdefault(str(k), {})[str(char)] = r
            ck(f"k{k}c{char}")
        v0 = res.get("0", {}).get("isunit")
        verdict = ("SLICE INFEASIBLE EVERYWHERE [proved]" if v0 == "1"
                   else "FEASIBLE OVER C -- ESCALATE" if v0 == "0"
                   else "undecided")
        print(f"   >>> k = {k}: char-0 unit ideal = {v0}  ({verdict})")
        RES.setdefault("verdicts", {}).setdefault(str(k), {})["char0"] = verdict
        control(f"T1b_k{k}")

    RES["seconds"] = round(time.time() - t0, 1)
    RES["manifest"] = {"declared": [f"T1b_k{k}" for k in range(kmin, kmax + 1)],
                       "ran": RAN,
                       "missing": [f"T1b_k{k}" for k in range(kmin, kmax + 1)
                                   if f"T1b_k{k}" not in RAN]}
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()

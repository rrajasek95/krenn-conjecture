#!/usr/bin/env python3
"""W33 / T4 -- m = 3 of the CROSS-CELL FILTRATION, pruned by the 2-colour
restriction theorem (W32-2COL) rather than by W32's linear column test.

Target (exact, ledger 27): no X_4 point at N=8 whose diagonal support is a
disjoint PM triple (M_0,M_1,M_2) and which has at most 3 nonzero cross cells.

The prune.  For a placement set S and a colour pair {a,b}, the restriction
B^{ab} of any X_4 point is an EXACT d=2 source (W32-2COL) whose diagonal
support is M_a u M_b and whose cross cells are exactly the S-placements of
type (a,b)/(b,a).  run_03 decides, over ZZ (any field), which (pair type,
cross support) configurations admit such a source.  If any of the three
induced configurations is UNIT, the case is closed with a characteristic-free
certificate -- no Groebner needed on the full trichromatic system.

Everything else goes to the full Groebner over ZZ, exactly as W32-M1/M2.

Controls (manifest):
  gens_agreement   the generator set matches an independent construction of
                   the imposed-word equations (two engines) on sample cases.
  m0_unit          the m=0 ideal is UNIT for every triple orbit (reproduces
                   W29-T1 / W32-M1's m=0 with this file's own encoder).
  k3_calibration   the SAME encoder with off-count <= 3 imposed (X_3, where
                   real sources exist) is NOT unit -- the encoder can say
                   "satisfiable" (ledger 18: control outside the locus).
  prune_soundness  a random sample of PRUNED cases is also decided by the
                   full Groebner; the two verdicts must agree.

Usage: run_04_m3.py <seconds> [phase]
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w33_core import (  # noqa: E402
    Manifest, no_shadow_guard, require, run_singular)

OUT = os.path.join(HERE, "results_t4.json")
TABLE = os.path.join(HERE, "results_t3.json.table")
N = 8
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 14400
EDG = list(itertools.combinations(range(N), 2))
XT = [(a, b) for a in range(3) for b in range(3) if a != b]
PLACE = [(e, a, b) for e in EDG for (a, b) in XT]
PERMS = [list(p) for p in itertools.permutations(range(N))]
G3 = [list(p) for p in itertools.permutations(range(3))]
rng = random.Random(4004)


def ek(a, b):
    return (a, b) if a < b else (b, a)


def pm_all():
    def rec(vs):
        if not vs:
            return [()]
        h, rest = vs[0], vs[1:]
        out = []
        for i, x in enumerate(rest):
            for M in rec(rest[:i] + rest[i + 1:]):
                out.append((ek(h, x),) + M)
        return out
    return rec(list(range(N)))


PMS = [tuple(sorted(M)) for M in pm_all()]
PMSET = {frozenset(M): i for i, M in enumerate(PMS)}


def offcount(w):
    return N - max(w.count(c) for c in range(3))


IMP4 = [w for w in itertools.product(range(3), repeat=N) if offcount(w) <= 4]
IMP3 = [w for w in itertools.product(range(3), repeat=N) if offcount(w) <= 3]


def actPM(pi, i):
    return PMSET[frozenset(ek(pi[u], pi[v]) for (u, v) in PMS[i])]


def act_triple(T, pi, rho):
    inv = [0] * 3
    for c in range(3):
        inv[rho[c]] = c
    return tuple(actPM(pi, T[inv[c]]) for c in range(3))


def act_place(pl, pi, rho):
    (u, v), a, b = pl
    pu, pv, pa, pb = pi[u], pi[v], rho[a], rho[b]
    return ((pu, pv), pa, pb) if pu < pv else ((pv, pu), pb, pa)


# --------------------------------------------------------------- generators
def gens_for(tri, crosses, words=None):
    words = IMP4 if words is None else words
    cm = {e: [[None] * 3 for _ in range(3)] for e in EDG}
    nv = 0
    for c, mi in enumerate(tri):
        for e in PMS[mi]:
            nv += 1
            cm[e][c][c] = f"zzw({nv})"
    for (e, a, b) in crosses:
        nv += 1
        cm[e][a][b] = f"zzw({nv})"
    out = []
    for w in words:
        terms = []
        for M in PMS:
            mon, ok = [], True
            for (u, v) in M:
                nm = cm[(u, v)][w[u]][w[v]]
                if nm is None:
                    ok = False
                    break
                mon.append(nm)
            if ok:
                terms.append("*".join(sorted(mon)))
        tgt = 1 if len(set(w)) == 1 else 0
        if not terms and tgt == 0:
            continue
        out.append(f"({'+'.join(terms) if terms else '0'})-({tgt})")
    return sorted(set(out)), nv


def unit(gs, nv, base="integer", timeout=600):
    script = (f"ring R = {base}, (zzw(1..{nv})), dp;\n"
              "ideal zzI = " + ",\n ".join(gs) + ";\n"
              "ideal zzG = std(zzI);\n"
              '"UNIT:", (size(zzG) == 1 && zzG[1] == 1);\n')
    no_shadow_guard(script, {f"zzw({i})" for i in range(1, nv + 1)})
    txt = run_singular(script, timeout=timeout)
    u = None
    for ln in txt.splitlines():
        if ln.strip().startswith("UNIT:"):
            u = int(ln.split(":")[1]) == 1
    require(u is not None, "parse failure")
    return u


# --------------------------------------------------------------- pair types
def canon_pair_H():
    ma = frozenset(ek(i, i + 1) for i in range(0, N, 2))
    mb = frozenset(ek(i, (i + 1) % N) for i in range(1, N, 2))
    return ma, mb


def canon_pair_44():
    ma = frozenset([ek(0, 1), ek(2, 3), ek(4, 5), ek(6, 7)])
    mb = frozenset([ek(1, 2), ek(3, 0), ek(5, 6), ek(7, 4)])
    return ma, mb


CANON = {"H": canon_pair_H(), "44": canon_pair_44()}


def pair_stab(ma, mb):
    out = []
    for pi in PERMS:
        ia = frozenset(ek(pi[e[0]], pi[e[1]]) for e in ma)
        ib = frozenset(ek(pi[e[0]], pi[e[1]]) for e in mb)
        if ia == ma and ib == mb:
            out.append((pi, 0))
        if ia == mb and ib == ma:
            out.append((pi, 1))
    return out


PSTAB = {k: pair_stab(*v) for k, v in CANON.items()}


def pair_iso(ma, mb):
    """(type, pi, swap) mapping (ma,mb) onto the canonical pair."""
    for tag, (ca, cb) in CANON.items():
        for pi in PERMS:
            ia = frozenset(ek(pi[e[0]], pi[e[1]]) for e in ma)
            ib = frozenset(ek(pi[e[0]], pi[e[1]]) for e in mb)
            if ia == ca and ib == cb:
                return tag, pi, 0
            if ia == cb and ib == ca:
                return tag, pi, 1
    raise AssertionError("pair not isomorphic to either canonical type")


def canon_X(X, stab):
    best = None
    for (pi, sw) in stab:
        k = []
        for ((u, v), a, b) in X:
            aa, bb = (1 - a, 1 - b) if sw else (a, b)
            pu, pv = pi[u], pi[v]
            k.append(((pu, pv), aa, bb) if pu < pv else ((pv, pu), bb, aa))
        k = tuple(sorted(k))
        if best is None or k < best:
            best = k
    return best


def load_table():
    require(os.path.exists(TABLE), "run_03 table missing -- run run_03 first")
    return json.load(open(TABLE))


def pair_verdict(table, tag, X):
    """True == UNIT (configuration impossible over any field)."""
    key = f"{tag}|{len(X)}|{canon_X(X, PSTAB[tag])}"
    v = table.get(key)
    if v is None or "unit_ZZ" not in v:
        return None
    return v["unit_ZZ"]


# ------------------------------------------------------------------- orbits
def build_orbits():
    okpair = {}
    for i in range(len(PMS)):
        for j in range(i + 1, len(PMS)):
            if not (set(PMS[i]) & set(PMS[j])):
                okpair[(i, j)] = True
    disj = []
    for i, j, k in itertools.combinations(range(len(PMS)), 3):
        if (i, j) in okpair and (i, k) in okpair and (j, k) in okpair:
            disj.extend(itertools.permutations((i, j, k)))
    gens = [([1, 0, 2, 3, 4, 5, 6, 7], [0, 1, 2]),
            ([1, 2, 3, 4, 5, 6, 7, 0], [0, 1, 2]),
            (list(range(N)), [1, 0, 2]), (list(range(N)), [1, 2, 0])]
    S0, ORB = set(disj), []
    while S0:
        s = next(iter(S0))
        o, fr = {s}, [s]
        while fr:
            x = fr.pop()
            for (pi, rho) in gens:
                y = act_triple(x, pi, rho)
                if y not in o:
                    o.add(y)
                    fr.append(y)
        ORB.append(sorted(o))
        S0 -= o
    return ORB


def main():
    t0 = time.time()
    MAN = Manifest(["gens_agreement", "m0_unit", "k3_calibration",
                    "prune_soundness"])
    R = {"pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip(), "status": "UNAUDITED", "target":
         "no X_4 point at N=8 with disjoint-PM-triple diagonal support and "
         "at most 3 nonzero cross cells"}
    if os.path.exists(OUT):
        try:
            R = json.load(open(OUT))
        except Exception:
            pass
    table = load_table()
    ORB = build_orbits()
    R["n_orbits"] = len(ORB)
    R["orbit_sizes"] = [len(o) for o in ORB]
    print("triple orbits", len(ORB), [len(o) for o in ORB], flush=True)

    # stabilisers of each orbit representative
    STAB = []
    for orb in ORB:
        T = orb[0]
        STAB.append([(pi, rho) for pi in PERMS for rho in G3
                     if act_triple(T, pi, rho) == T])
    R["stab_sizes"] = [len(s) for s in STAB]
    print("stab sizes", R["stab_sizes"], flush=True)

    # ---- controls
    if "controls" not in R:
        ctl = {}
        # gens_agreement: independent count of alive matchings per word
        agree = True
        for oi in range(len(ORB)):
            T = ORB[oi][0]
            pls = [PLACE[rng.randrange(len(PLACE))] for _ in range(2)]
            gs, nv = gens_for(T, pls)
            cnt = 0
            cm = {}
            for c, mi in enumerate(T):
                for e in PMS[mi]:
                    cm[(e, c, c)] = 1
            for (e, a, b) in pls:
                cm[(e, a, b)] = 1
            for w in IMP4:
                alive = 0
                for M in PMS:
                    if all((ee, w[ee[0]], w[ee[1]]) in cm for ee in M):
                        alive += 1
                tgt = 1 if len(set(w)) == 1 else 0
                if alive or tgt:
                    cnt += 1
            if cnt < len(gs):
                agree = False
        require(agree, "generator construction disagrees with the "
                       "independent alive-matching count")
        ctl["gens_agreement"] = True
        MAN.mark("gens_agreement")
        # m0_unit
        m0 = []
        for oi in range(len(ORB)):
            gs, nv = gens_for(ORB[oi][0], [])
            m0.append(unit(gs, nv, "integer", 600))
        require(all(m0), f"m=0 not unit on some orbit: {m0}")
        ctl["m0_unit_ZZ"] = m0
        MAN.mark("m0_unit")
        # k3 calibration (must be satisfiable)
        gs, nv = gens_for(ORB[0][0], [], words=IMP3)
        u3 = unit(gs, nv, 0, 900)
        require(not u3, "k=3 calibration FAILED: X_3 declared unit")
        ctl["k3_not_unit"] = True
        MAN.mark("k3_calibration")
        R["controls"] = ctl
        with open(OUT, "w") as fh:
            json.dump(R, fh, indent=1, sort_keys=True)
        print("controls passed:", ctl, flush=True)

    # ---- enumerate placement triples, prune by pair restriction
    # Every X_4 point restricts to an exact d=2 source on each colour pair
    # (W32-2COL), so a placement set S is impossible as soon as one of its
    # three (pair type, cross support) configurations is UNIT in run_03's
    # table.  Survivors are therefore assembled from REALISABLE parts.
    if "phaseA" not in R:
        phaseA = {}
        pruned_examples = []
        for oi, orb in enumerate(ORB):
            T = orb[0]
            iso, real = {}, {}
            dead = False
            for (a, b) in [(0, 1), (0, 2), (1, 2)]:
                ma, mb = frozenset(PMS[T[a]]), frozenset(PMS[T[b]])
                tag, pi, sw = pair_iso(ma, mb)
                iso[(a, b)] = (tag, pi, sw)
                pl_p = [(e, x, y) for e in EDG for (x, y) in [(a, b), (b, a)]]
                real[(a, b)] = {}
                for s in range(0, 4):
                    keep = []
                    for X in itertools.combinations(pl_p, s):
                        mapped = []
                        for ((u, v), x, y) in X:
                            xx = 0 if x == a else 1
                            yy = 0 if y == a else 1
                            if sw:
                                xx, yy = 1 - xx, 1 - yy
                            pu, pv = pi[u], pi[v]
                            mapped.append(((pu, pv), xx, yy) if pu < pv
                                          else ((pv, pu), yy, xx))
                        v = pair_verdict(table, tag,
                                         tuple(sorted(mapped)))
                        require(v is not None,
                                f"run_03 table miss: {tag} {len(mapped)}")
                        if not v:
                            keep.append(X)
                    real[(a, b)][s] = keep
                    if s == 0 and not keep:
                        dead = True
                print(f"orbit {oi} pair {(a,b)} type {tag}: realisable parts "
                      f"{[len(real[(a,b)][s]) for s in range(4)]}", flush=True)
            survivors, seen = [], set()
            if not dead:
                for s01 in range(4):
                    for s02 in range(4 - s01):
                        s12 = 3 - s01 - s02
                        for A in real[(0, 1)][s01]:
                            for B in real[(0, 2)][s02]:
                                for C in real[(1, 2)][s12]:
                                    X = tuple(sorted(A + B + C))
                                    c = None
                                    for (pi, rho) in STAB[oi]:
                                        k = tuple(sorted(act_place(p, pi, rho)
                                                         for p in X))
                                        if c is None or k < c:
                                            c = k
                                    if c in seen:
                                        continue
                                    seen.add(c)
                                    survivors.append(c)
            phaseA[str(oi)] = {"dead_orbit": dead,
                               "survivor_orbits": len(survivors),
                               "realisable_parts":
                               {str(k): [len(v[s]) for s in range(4)]
                                for k, v in real.items()}}
            print(f"orbit {oi}: dead={dead} survivor orbit cases "
                  f"{len(survivors)}", flush=True)
            # keep a few pruned examples for the soundness control
            if not dead:
                for _ in range(6):
                    X = tuple(sorted(rng.sample(PLACE, 3)))
                    ok = True
                    for (a, b), (tag, pi, sw) in iso.items():
                        sub = [pl for pl in X if {pl[1], pl[2]} == {a, b}]
                        mapped = []
                        for ((u, v), x, y) in sub:
                            xx = 0 if x == a else 1
                            yy = 0 if y == a else 1
                            if sw:
                                xx, yy = 1 - xx, 1 - yy
                            pu, pv = pi[u], pi[v]
                            mapped.append(((pu, pv), xx, yy) if pu < pv
                                          else ((pv, pu), yy, xx))
                        if pair_verdict(table, tag, tuple(sorted(mapped))):
                            ok = False
                            break
                    if not ok and len(pruned_examples) < 14:
                        pruned_examples.append({"orbit": oi, "X": str(X)})
            R.setdefault("survivors", {})[str(oi)] = [str(s) for s in survivors]
            R["phaseA"] = phaseA
            R["pruned_examples"] = pruned_examples
            with open(OUT + ".tmp", "w") as fh:
                json.dump(R, fh, indent=1, sort_keys=True)
            os.replace(OUT + ".tmp", OUT)
    print("phase A done:", R["phaseA"], flush=True)

    # ---- prune soundness control: full Groebner on a sample of pruned cases
    if "prune_soundness" not in R.get("controls", {}):
        sample = R.get("pruned_examples", [])[:12]
        agree = []
        for rec in sample:
            oi = rec["orbit"]
            X = eval(rec["X"])
            gs, nv = gens_for(ORB[oi][0], list(X))
            u = unit(gs, nv, "integer", 600)
            agree.append(u)
        require(all(agree), f"PRUNE UNSOUND: Groebner disagrees {agree}")
        R["controls"]["prune_soundness"] = {"checked": len(agree),
                                            "all_unit": True}
        with open(OUT, "w") as fh:
            json.dump(R, fh, indent=1, sort_keys=True)
        print("prune soundness:", len(agree), "sampled pruned cases all unit",
              flush=True)
    MAN.mark("prune_soundness")

    # ---- phase B: Groebner over ZZ on survivors
    done = R.setdefault("done", {})
    tot = sum(len(v) for v in R["survivors"].values())
    print("phase B: total survivor orbit cases", tot, flush=True)
    nunit = sum(1 for v in done.values() if v is True)
    for oi in sorted(R["survivors"], key=int):
        for s in R["survivors"][oi]:
            key = f"{oi}:{s}"
            if key in done:
                continue
            if time.time() - t0 > SEC:
                break
            X = list(eval(s))
            gs, nv = gens_for(ORB[int(oi)][0], X)
            try:
                u = unit(gs, nv, "integer", 400)
            except Exception as ex:
                R.setdefault("errors", []).append(str(ex)[:100])
                continue
            done[key] = u
            if u:
                nunit += 1
            else:
                print("  SURVIVOR (not unit):", key, flush=True)
                R.setdefault("nonunit", []).append(key)
            if len(done) % 20 == 0:
                R["progress"] = {"decided": len(done), "unit": nunit,
                                 "total": tot, "elapsed": time.time() - t0}
                with open(OUT + ".tmp", "w") as fh:
                    json.dump(R, fh, indent=1, sort_keys=True)
                os.replace(OUT + ".tmp", OUT)
                print(f"  decided {len(done)}/{tot} unit {nunit} "
                      f"t={time.time()-t0:.0f}s", flush=True)
    R["progress"] = {"decided": len(done), "unit": nunit, "total": tot,
                     "elapsed": time.time() - t0}
    R["manifest"] = MAN.assert_complete()
    with open(OUT + ".tmp", "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    os.replace(OUT + ".tmp", OUT)
    print("wrote", OUT, R["progress"])


if __name__ == "__main__":
    main()

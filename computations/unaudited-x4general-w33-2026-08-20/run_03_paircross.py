#!/usr/bin/env python3
"""W33 / T3 -- CLASSIFICATION of the exact d=2 sources whose diagonal support
is a PM pair, with at most 3 cross cells (a stratum-level classification, and
the sound pruning instrument for the m=3 cross-cell filtration).

Why this stratum.  W32-2COL: every 2-colour restriction B^{ab} of an X_4 point
is an EXACT d=2 source.  In the cross-cell filtration the diagonal support is a
disjoint PM triple (M_0,M_1,M_2), so B^{ab} has diagonal support M_a u M_b and
its cross cells are exactly the placements of S of type (a,b)/(b,a).  Hence a
placement set S is IMPOSSIBLE as soon as one of the three induced (PM-pair,
cross-support) configurations admits no exact d=2 source.  That is a
characteristic-free, theorem-grade prune (no relaxation: it tests the exact
2-colour condition, ledger 27).

Structure of a PM pair on K_8: M_a u M_b is a disjoint union of even cycles of
length >= 4, so it is an 8-cycle ("H") or two 4-cycles ("44").

Decision procedure per (pair type, cross support X): variables = 8 diagonal
weights + |X| cross cells; equations = all 256 words of {0,1}^8 (target 1 on
the two constant words, 0 otherwise); Rabinowitsch variable forces EVERY
variable nonzero (the diagonal weights are forced nonzero anyway by the
constant words).  Verdict UNIT => no such source over ANY field.  Run over ZZ
first (any-field) and over Q as a cross-check.

Usage: run_03_paircross.py <seconds> [maxsize]
"""
from __future__ import annotations

import itertools
import json
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w33_core import (  # noqa: E402
    Manifest, cycle_pm_pair, edges, is_exact2, no_shadow_guard, require,
    run_singular, setcell, zero_source)

OUT = os.path.join(HERE, "results_t3.json")
N = 8
EDG = edges(N)
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 7200
MAXSZ = int(sys.argv[2]) if len(sys.argv) > 2 else 3
XT = [(0, 1), (1, 0)]                      # cross types inside a colour pair
PLACE = [(e, a, b) for e in EDG for (a, b) in XT]
PERMS = [list(p) for p in itertools.permutations(range(N))]


def ek(a, b):
    return (a, b) if a < b else (b, a)


# ------------------------------------------------------------- pair types
def pair_H():
    ma = [ek(i, i + 1) for i in range(0, N, 2)]
    mb = [ek(i, (i + 1) % N) for i in range(1, N, 2)]
    return frozenset(ma), frozenset(mb)


def pair_44():
    ma = [ek(0, 1), ek(2, 3), ek(4, 5), ek(6, 7)]
    mb = [ek(1, 2), ek(3, 0), ek(5, 6), ek(7, 4)]
    return frozenset(ma), frozenset(mb)


PAIRS = {"H": pair_H(), "44": pair_44()}


def act_edge(pi, e):
    return ek(pi[e[0]], pi[e[1]])


def act_place(pl, pi, sw):
    (u, v), a, b = pl
    if sw:
        a, b = 1 - a, 1 - b
    pu, pv = pi[u], pi[v]
    return ((pu, pv), a, b) if pu < pv else ((pv, pu), b, a)


def stabiliser(ma, mb):
    """(pi, swap) with pi(M_a)=M_a, pi(M_b)=M_b (swap=0) or exchanging them."""
    out = []
    for pi in PERMS:
        ia = frozenset(act_edge(pi, e) for e in ma)
        ib = frozenset(act_edge(pi, e) for e in mb)
        if ia == ma and ib == mb:
            out.append((pi, 0))
        if ia == mb and ib == ma:
            out.append((pi, 1))
    return out


# --------------------------------------------------------------- Singular
def gens_for(ma, mb, X):
    cm = {e: [[None] * 2 for _ in range(2)] for e in EDG}
    nv = 0
    order = []
    for e in sorted(ma):
        nv += 1
        cm[e][0][0] = f"zzw({nv})"
        order.append(("w", e))
    for e in sorted(mb):
        nv += 1
        cm[e][1][1] = f"zzw({nv})"
        order.append(("w", e))
    for (e, a, b) in X:
        nv += 1
        cm[e][a][b] = f"zzw({nv})"
        order.append(("x", (e, a, b)))
    gs = []
    for w in itertools.product(range(2), repeat=N):
        terms = []
        for M in PMLIST:
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
        gs.append(f"({'+'.join(terms) if terms else '0'})-({tgt})")
    return sorted(set(gs)), nv, order


def pm_all(n):
    def rec(vs):
        if not vs:
            return [()]
        h, rest = vs[0], vs[1:]
        out = []
        for i, x in enumerate(rest):
            for M in rec(rest[:i] + rest[i + 1:]):
                out.append((ek(h, x),) + M)
        return out
    return rec(list(range(n)))


PMLIST = pm_all(N)


def decide(ma, mb, X, base="integer", timeout=300):
    """UNIT?  (no exact d=2 source with this diagonal support and ALL the
    cross cells of X nonzero, over any field if base=integer)."""
    gs, nv, _order = gens_for(ma, mb, X)
    prod = "*".join(f"zzw({i})" for i in range(1, nv + 1))
    script = (f"ring R = {base}, (zzw(1..{nv}), zzt), dp;\n"
              "ideal zzI = " + ",\n ".join(gs) + f",\n zzt*{prod}-1;\n"
              "ideal zzG = std(zzI);\n"
              '"UNIT:", (size(zzG) == 1 && zzG[1] == 1);\n')
    rv = {"zzt"} | {f"zzw({i})" for i in range(1, nv + 1)}
    no_shadow_guard(script, rv)
    txt = run_singular(script, timeout=timeout)
    u = None
    for ln in txt.splitlines():
        ln = ln.strip()
        if ln.startswith("UNIT:"):
            u = int(ln.split(":")[1]) == 1
    require(u is not None, "parse failure in decide")
    return u


# ----------------------------------------------------------------- controls
MAN = Manifest(["explicit_point_H", "must_fire_44", "chord_point",
                "crossing_chord_unit", "engine_agreement"])


def controls(R):
    ma, mb = PAIRS["H"]
    # C1 explicit point OUTSIDE the asserted locus (ledger 18): the empty
    # cross support on an 8-cycle IS realisable -- the verdict must be
    # NOT-unit, and the explicit rational point must satisfy the system.
    u = decide(ma, mb, [])
    src = cycle_pm_pair(N)
    require(is_exact2(src, N)[0], "Delta^2 not exact -- engine error")
    require(not u, "explicit-point control FAILED: 8-cycle declared unit "
                   "while an explicit exact source exists")
    R["explicit_point_H"] = {"unit": u, "explicit_point_exact": True}
    MAN.mark("explicit_point_H")
    # C2 the mutation that must fire: two 4-cycles admit NO exact source
    ma4, mb4 = PAIRS["44"]
    src4 = zero_source(N, 2)
    for e in ma4:
        src4[e][0][0] = Fraction(1)
    for e in mb4:
        src4[e][1][1] = Fraction(1)
    require(not is_exact2(src4, N)[0], "4+4 diagonal unexpectedly exact")
    u44 = decide(ma4, mb4, [])
    require(u44, "must-fire control FAILED: 4+4 with no cross cell not unit")
    R["must_fire_44"] = {"unit": u44}
    MAN.mark("must_fire_44")
    # C3 a same-parity chord cell is realisable (explicit point) and the
    # decision must say NOT unit
    ch = ((0, 2), 0, 1)
    s = cycle_pm_pair(N)
    setcell(s, 0, 2, 0, 1, Fraction(3))
    require(is_exact2(s, N)[0], "same-parity chord point not exact")
    uc = decide(ma, mb, [ch])
    require(not uc, "chord_point control FAILED (declared unit but a point "
                    "exists)")
    R["chord_point"] = {"unit": uc}
    MAN.mark("chord_point")
    # C4 a crossing chord / cycle-edge cell must be unit (the k=1 lemma)
    res = {}
    for pl in [((0, 3), 0, 1), ((1, 4), 1, 0), ((0, 1), 0, 1),
               ((1, 2), 1, 0)]:
        res[str(pl)] = decide(ma, mb, [pl])
    require(all(res.values()), f"crossing_chord_unit FAILED: {res}")
    R["crossing_chord_unit"] = res
    MAN.mark("crossing_chord_unit")
    # C5 engine agreement: Q verdict == ZZ verdict on this control set
    agree = {}
    for pl, exp in [(((0, 2), 0, 1), False), (((0, 3), 0, 1), True)]:
        agree[str(pl)] = (decide(ma, mb, [pl], base=0) == exp)
    require(all(agree.values()), f"Q/ZZ disagreement: {agree}")
    R["engine_agreement"] = agree
    MAN.mark("engine_agreement")
    print("T3 controls passed:", json.dumps(R, sort_keys=True)[:300])


# ------------------------------------------------------------------- main
def canon(X, stab):
    best = None
    for (pi, sw) in stab:
        k = tuple(sorted(act_place(p, pi, sw) for p in X))
        if best is None or k < best:
            best = k
    return best


def main():
    t0 = time.time()
    R = {"pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip(), "status": "UNAUDITED"}
    controls(R)
    R["controls_manifest"] = MAN.assert_complete()
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    table = {}
    if os.path.exists(OUT + ".table"):
        table = json.load(open(OUT + ".table"))
    for tag, (ma, mb) in PAIRS.items():
        stab = stabiliser(ma, mb)
        print(tag, "stabiliser size", len(stab), flush=True)
        R[f"stab_{tag}"] = len(stab)
        for size in range(0, MAXSZ + 1):
            reps, seen = [], set()
            for X in itertools.combinations(PLACE, size):
                c = canon(X, stab)
                if c in seen:
                    continue
                seen.add(c)
                reps.append(c)
            print(f"  {tag} |X|={size}: {len(reps)} orbit reps", flush=True)
            R[f"reps_{tag}_{size}"] = len(reps)
            done = 0
            for X in reps:
                key = f"{tag}|{size}|{X}"
                if key in table:
                    continue
                if time.time() - t0 > SEC:
                    break
                try:
                    u = decide(ma, mb, list(X), base="integer", timeout=240)
                    table[key] = {"unit_ZZ": u}
                except Exception as ex:
                    table[key] = {"error": str(ex)[:120]}
                done += 1
                if done % 25 == 0:
                    with open(OUT + ".table.tmp", "w") as fh:
                        json.dump(table, fh, sort_keys=True)
                    os.replace(OUT + ".table.tmp", OUT + ".table")
                    print(f"    {tag} size {size}: {done}/{len(reps)}"
                          f" t={time.time()-t0:.0f}s", flush=True)
            with open(OUT + ".table.tmp", "w") as fh:
                json.dump(table, fh, sort_keys=True)
            os.replace(OUT + ".table.tmp", OUT + ".table")
            nu = sum(1 for k, v in table.items()
                     if k.startswith(f"{tag}|{size}|") and v.get("unit_ZZ"))
            nn = sum(1 for k, v in table.items()
                     if k.startswith(f"{tag}|{size}|")
                     and v.get("unit_ZZ") is False)
            R[f"verdicts_{tag}_{size}"] = {"unit": nu, "realisable": nn,
                                           "reps": len(reps)}
            print(f"  {tag} |X|={size}: unit {nu}, realisable {nn}",
                  flush=True)
            with open(OUT, "w") as fh:
                json.dump(R, fh, indent=1, sort_keys=True)
    R["elapsed"] = time.time() - t0
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""adv2 -- THE OTHER ROUTE TO killed=False:  make c_e VANISH IDENTICALLY.

UNAUDITED.  EXACT ONLY (Fraction).

C.verdict forces z_e = 0 only when z_e actually appears in the residual
system.  A single e whose coefficient c_e vanishes at EVERY word where e
is active contributes no row at all, so z_e stays free and may be given
any nonzero value.  So the primary target can also be reached by
    (a) a few singles genuinely surviving (nonzero constant ratio), plus
    (b) all the others having c_e == 0 identically,
    (c) and Phi = 0 at every degree-<=1 word (else a constant-only row
        makes the system inconsistent).
This script measures how many singles can have c_e == 0 identically at a
clean point with every Gamma cell nonzero.

c_e = haf_Gamma(V - e) does not involve the blocks at e's own endpoints,
and is LINEAR in the blocks at any other vertex t, splitting by the letter
w_t -- exactly like the clean layer.  So "clean AND c_e == 0 for e in E0"
is again a homogeneous linear system at each site, and a site solve at t
cannot break the conditions for singles e with t in e.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2lib as A                                                 # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
OUT = {"_header": "UNAUDITED adv2 -- identically vanishing c_e"}


def active_words(m, e):
    """one word per assignment of the six letters off e (the active set)."""
    G = A.Geo(m)
    a, b = G.sing[e]
    rest = [v for v in range(8) if v not in e]
    out = []
    for tup in product(range(3), repeat=6):
        w = [0] * 8
        w[e[0]], w[e[1]] = a, b
        for k, v in enumerate(rest):
            w[v] = tup[k]
        out.append(tuple(w))
    return out


def site_solve(m, bl, t, E0, rng, tries=400):
    """re-solve vertex t's blocks: clean layer + c_e == 0 for e in E0."""
    G = A.Geo(m)
    nb = sorted({u for e in G.gam for u in e if t in e} - {t})
    nc = 3 * len(nb)
    tab = {}
    for u in nb:
        tab[u] = tuple(v for v in range(8) if v != t and v != u)
    rows = {0: [], 1: [], 2: []}

    def add(w, target_verts):
        r = [F(0)] * nc
        for k, u in enumerate(nb):
            if u not in target_verts:
                continue
            vs = tuple(v for v in target_verts if v != t and v != u)
            r[3 * k + w[u]] += C.haf_on(bl, G.gs, vs, w)
        if any(r):
            rows[w[t]].append(r)

    allv = tuple(range(8))
    for w in G.clean:
        add(w, allv)
    for e in E0:
        if t in e:
            continue
        vs = tuple(v for v in range(8) if v not in e)
        for w in active_words(m, e):
            add(w, vs)
    newv = {}
    for c in range(3):
        K = A.kernel_g(rows[c], nc, F(0), F(1))
        if not K:
            return False
        got = None
        for _ in range(tries):
            co = [F(rng.randint(-5, 5)) for _ in K]
            v = [sum((co[i] * K[i][j] for i in range(len(K))), F(0))
                 for j in range(nc)]
            if all(x != 0 for x in v):
                got = v
                break
        if got is None:
            return False
        newv[c] = got
    for k, u in enumerate(nb):
        e = (min(t, u), max(t, u))
        for c in range(3):
            for d in range(3):
                if e[0] == t:
                    bl[e][c][d] = newv[c][3 * k + d]
                else:
                    bl[e][d][c] = newv[c][3 * k + d]
    return True


def c_identically_zero(m, bl, e):
    G = A.Geo(m)
    return all(A.coef2(bl, G, e, w) == 0 for w in active_words(m, e))


def attempt(m, E0, rng, passes=4):
    G = A.Geo(m)
    bl = {e: [[F(rng.randint(-6, 6) or 3, rng.randint(1, 3))
               for _ in range(3)] for _ in range(3)] for e in G.gam}
    for _p in range(passes):
        for t in range(8):
            site_solve(m, bl, t, E0, rng)
    if not A.all_cells_nonzero(bl, G):
        return None
    if not A.is_clean(m, bl):
        return None
    ok = [e for e in E0 if c_identically_zero(m, bl, e)]
    return bl, ok


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    OUT["m"] = m
    fn = os.path.join(HERE, "results_czero_m%d.json" % m)
    G = A.Geo(m)
    recs = []
    print("=" * 74)
    print("(1) can a SINGLE c_e vanish identically at a clean point? m=%d"
          % m)
    print("=" * 74)
    doable = []
    for e in G.live:
        got = None
        for s in range(6):
            rng = random.Random(1000 * s + hash(e) % 997)
            r = attempt(m, [e], rng)
            if r and e in r[1]:
                got = r
                break
        print("  c_%-8s == 0 identically at a clean point: %s"
              % (e, "YES" if got else "no"))
        recs.append(dict(kind="single", e=str(e), found=bool(got),
                         stratum=(A.on_stratum(m, got[0]) if got else None)))
        if got:
            doable.append(e)
            recs[-1]["point"] = A.dump(got[0])
        OUT["records"] = recs
        json.dump(OUT, open(fn, "w"), indent=1, default=str)
    print("  singles achievable one at a time: %s" % [str(e) for e in doable])

    print()
    print("=" * 74)
    print("(2) how many simultaneously?  (greedy)")
    print("=" * 74)
    best = []
    for s in range(8):
        rng = random.Random(77 + 13 * s)
        order = list(doable)
        rng.shuffle(order)
        E0 = []
        for e in order:
            r = attempt(m, E0 + [e], rng)
            if r and all(f in r[1] for f in E0 + [e]):
                E0 = E0 + [e]
        r = attempt(m, E0, rng) if E0 else None
        okk = r[1] if r else []
        print("  greedy pass %d: |E0|=%d  %s  (clean point rebuilt: %s)"
              % (s, len(E0), [str(e) for e in E0], bool(r)))
        if len(okk) > len(best):
            best = okk
            if r:
                OUT["best_point"] = A.dump(r[0])
                OUT["best_E0"] = [str(e) for e in okk]
                OUT["best_stratum"] = A.on_stratum(m, r[0])
                vd = A.full_verdict(m, r[0])
                OUT["best_verdict"] = {k: vd[k] for k in
                                       ("n_unknowns", "n_rows", "rank",
                                        "inconsistent", "killed")}
                OUT["best_forced_zero"] = vd.get("forced_zero")
                print("     verdict at that point: killed=%s forced=%s"
                      % (vd["killed"], vd.get("forced_zero")))
        json.dump(OUT, open(fn, "w"), indent=1, default=str)
    print("\nMAX simultaneous identically-vanishing c_e: %d  (%s)"
          % (len(best), [str(e) for e in best]))
    OUT["max_simultaneous"] = len(best)
    json.dump(OUT, open(fn, "w"), indent=1, default=str)
    print("wrote %s" % fn)


if __name__ == "__main__":
    main()

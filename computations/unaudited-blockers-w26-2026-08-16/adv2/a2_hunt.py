#!/usr/bin/env python3
"""adv2 -- THE HUNT.  Randomised multi-start refinement climbs looking for
a point of  W = {H_w = 0 at all 6558 mixed words}  with as many z_e != 0
as possible.  12 of 12 would be the PRIMARY TARGET.

UNAUDITED.  EXACT ONLY (Fraction); the tangent test is exact mod p.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2ans as AN                                                # noqa: E402
import a2lib as A                                                 # noqa: E402
import a2jac as J                                                 # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
OUT = {"_header": "UNAUDITED adv2 -- randomised climb hunt"}


def fire_letters(m, v):
    G = A.Geo(m)
    return sorted({G.sing[e][0 if e[0] == v else 1]
                   for e in G.live if v in e})


def seed(m, p, j, rng, tries=120):
    a, b = A.Geo(m).sing[(p, j)]
    gr = [AN.SEP[:] for _ in range(8)]
    gr[p] = AN.two(a)
    gr[j] = AN.two(b)
    an = AN.Ans(m, gr)
    for _ in range(tries):
        th = an.rand_theta(rng)
        z = {e: F(0) for e in an.tsing}
        ok = True
        for t in (p, j, p, j):
            if not an.site_solve(th, z, t, rng):
                ok = False
                break
        if not ok or an.defect(th, z) != 0:
            continue
        if any(z[e] == 0 for e in an.tsing):
            continue
        bl = an.blocks(th)
        if not A.all_cells_nonzero(bl, A.Geo(m)) or A.on_stratum(m, bl):
            continue
        return an, th, z
    return None


def wander(an, th, z, rng, steps):
    """random site-solves that keep H = 0 and every cell / z nonzero."""
    for _ in range(steps):
        t = rng.randrange(8)
        sv = (list(th), dict(z))
        if not an.site_solve(th, z, t, rng):
            th[:], z = sv[0], dict(sv[1])
            continue
        if an.defect(th, z) != 0 or not A.all_cells_nonzero(
                an.blocks(th), A.Geo(an.m)):
            th[:], z = sv[0], dict(sv[1])
    return th, z


def step(an, th, z, v, newg, rng, rounds=10):
    an2, th2, z2 = AN.refine(an, th, z, v, newg)
    if an2.defect(th2, z2) != 0:
        return None
    order = [v] + list(range(8))
    best = (sum(1 for e in an2.tsing if z2[e] != 0), list(th2), dict(z2))
    for _r in range(rounds):
        rng.shuffle(order)
        for t in [v] + order:
            sv = (list(th2), dict(z2))
            if not an2.site_solve(th2, z2, t, rng):
                th2[:], z2 = sv[0], dict(sv[1])
                continue
            if an2.defect(th2, z2) != 0 or not A.all_cells_nonzero(
                    an2.blocks(th2), A.Geo(an2.m)):
                th2[:], z2 = sv[0], dict(sv[1])
                continue
            k = sum(1 for e in an2.tsing if z2[e] != 0)
            if k > best[0]:
                best = (k, list(th2), dict(z2))
            if k == len(an2.tsing):
                return an2, list(th2), dict(z2)
    return an2, best[1], best[2]


def run_one(m, rng, maxsteps=10):
    G = A.Geo(m)
    e0 = G.live[rng.randrange(len(G.live))]
    r = seed(m, e0[0], e0[1], rng)
    if r is None:
        return None
    an, th, z = r
    hist = ["seed %s" % (e0,)]
    for _s in range(maxsteps):
        cand = []
        for v in range(8):
            fl = fire_letters(m, v)
            cur = len(an.groups[v])
            for ng in ([AN.two(c) for c in fl] if cur == 1 else []) + \
                      ([AN.FULL] if cur < 3 else []):
                if ng == an.groups[v]:
                    continue
                a2 = AN.Ans(m, [list(g) if u != v else list(ng)
                                for u, g in enumerate(an.groups)])
                gain = len(a2.tsing) - len(an.tsing)
                if gain > 0 or cur == 1:
                    cand.append((gain, v, ng))
        if not cand:
            break
        cand.sort(key=lambda t: -t[0])
        top = [c for c in cand if c[0] == cand[0][0]]
        _, v, ng = top[rng.randrange(len(top))]
        th, z = wander(an, th, z, rng, 3)
        out = step(an, th, z, v, ng, rng)
        if out is None:
            break
        an, th, z = out
        hist.append("v%d->%d st: z on %d/%d" %
                    (v, len(ng), sum(1 for e in an.tsing if z[e] != 0),
                     len(an.tsing)))
    nz = sorted(str(e) for e in an.tsing if z[e] != 0)
    return an, th, z, nz, hist


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    nruns = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    s0 = int(sys.argv[3]) if len(sys.argv) > 3 else 555
    OUT["m"] = m
    fn = os.path.join(HERE, "results_hunt_m%d_s%d.json" % (m, s0))
    best = 0
    recs = []
    for it in range(nruns):
        rng = random.Random(s0 + 977 * it)
        try:
            out = run_one(m, rng)
        except Exception as ex:                                    # noqa
            print("  run %d: %s %s" % (it, type(ex).__name__, ex))
            continue
        if out is None:
            print("  run %d: no seed" % it)
            continue
        an, th, z, nz, hist = out
        bl = an.blocks(th)
        surv = [str(e) for e in A.Geo(m).live
                if A.solo_verdict(m, bl, e)["survives"]]
        vd = A.full_verdict(m, bl)
        rec = dict(run=it, n_z_nonzero=len(nz), z_nonzero=nz,
                   solo_survivors=surv, hist=hist,
                   stratum=A.on_stratum(m, bl), clean=A.is_clean(m, bl),
                   killed=vd["killed"], inconsistent=vd.get("inconsistent"),
                   groups=[len(g) for g in an.groups])
        print("  run %2d: z on %2d singles %s ; solo survivors %s ; "
              "verdict killed=%s" % (it, len(nz), nz, surv, vd["killed"]))
        if len(nz) >= max(3, best):
            best = len(nz)
            T = C.TEMPLATES[m]
            zz = {e: z.get(e, F(0)) for e in C.single_edges(T)}
            bad = sum(1 for w in C.MIXED if C.H_word(bl, T, zz, w) != 0)
            cons = [str(C.H_word(bl, T, zz, (c,) * 8)) for c in range(3)]
            rec["raw_mixed_nonzero"] = bad
            rec["raw_H_constants"] = cons
            rec["point"] = A.dump(bl)
            rec["z"] = {str(e): str(v) for e, v in z.items()}
            t = J.tangent(m, bl, z, 10007, sample=400,
                          rng=random.Random(7))
            rec["tangent"] = t
            print("      RAW: H!=0 at %d/6558 mixed ; H(const)=%s ; "
                  "tangent z LIVE=%s" % (bad, cons, t["z_live"]))
            if len(nz) == 12 and bad == 0:
                print("  *** PRIMARY TARGET CANDIDATE ***")
                OUT["PRIMARY"] = rec
        recs.append(rec)
        OUT["records"] = recs
        OUT["best_n_z"] = best
        json.dump(OUT, open(fn, "w"), indent=1, default=str)
    print("\nBEST: %d simultaneous nonzero z's" % best)
    json.dump(OUT, open(fn, "w"), indent=1, default=str)
    print("wrote %s" % fn)


if __name__ == "__main__":
    main()

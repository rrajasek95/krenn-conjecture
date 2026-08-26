#!/usr/bin/env python3
"""adv2 -- IS THE SURVIVOR SET ALWAYS A STAR?

Every survivor set seen so far -- {(1,6),(2,6)} (adv/), {(0,4),(2,4),(3,4)}
and {(1,5),(1,6)} (adv2) -- is a STAR: all its singles share one vertex.
A star has at most 3 members, so if that is forced then the PRIMARY
target (all 12 z_e nonzero) is impossible.  This script attacks the
conjecture directly: for each ORDERED pair of singles that do NOT share a
vertex, try to build a point of W = {H_w = 0 at all mixed w} with BOTH
z's nonzero.

UNAUDITED.  EXACT ONLY (Fraction).
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2ans as AN                                                # noqa: E402
import a2lib as A                                                 # noqa: E402
import a2jac as J                                                 # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
OUT = {"_header": "UNAUDITED adv2 -- star conjecture / disjoint pairs"}


def solve_site(an, th, z, t, rng, need, tries=900):
    """kernel vector with every PARAM nonzero and every z in `need`
    nonzero (other z's may be anything)."""
    pk, zk, rows, K = an.site_kernel(th, z, t)
    if not K:
        return False
    npk = len(pk)
    req = list(range(npk)) + [npk + i for i, e in enumerate(zk)
                              if e in need]
    for _ in range(tries):
        co = [F(rng.randint(-6, 6)) for _ in K]
        v = [sum((co[i] * K[i][j] for i in range(len(K))), F(0))
             for j in range(npk + len(zk))]
        if all(v[i] != 0 for i in req):
            an.write_site(th, z, t, pk, zk, v)
            return True
    return False


def groups_for(m, singles, extra_full=()):
    """the coarsest grouping in which every single in `singles` is legal."""
    G = A.Geo(m)
    need = {v: set() for v in range(8)}
    for e in singles:
        need[e[0]].add(G.sing[e][0])
        need[e[1]].add(G.sing[e][1])
    gr = []
    for v in range(8):
        s = need[v] | (set(range(3)) if v in extra_full else set())
        if not s:
            gr.append(AN.SEP[:])
        elif len(s) == 1:
            gr.append(AN.two(next(iter(s))))
        else:
            gr.append(AN.FULL[:])
    return gr


def build(m, targets, rng, rounds=14, tries=8):
    """climb to a point of W with z nonzero on every single in targets."""
    G = A.Geo(m)
    for _t in range(tries):
        # ---- seed on the first target only
        e0 = targets[0]
        gr = groups_for(m, [e0])
        an = AN.Ans(m, gr)
        th = an.rand_theta(rng)
        z = {e: F(0) for e in an.tsing}
        ok = False
        for _ in range(60):
            th = an.rand_theta(rng)
            z = {e: F(0) for e in an.tsing}
            good = True
            for t in (e0[0], e0[1], e0[0], e0[1]):
                if not solve_site(an, th, z, t, rng, {e0}):
                    good = False
                    break
            if not good or an.defect(th, z) != 0:
                continue
            bl = an.blocks(th)
            if not A.all_cells_nonzero(bl, A.Geo(m)):
                continue
            # cheap off-stratum test: under a grouping ansatz Phi depends
            # only on the pattern, so the representative words suffice.
            if all(A.phi2(bl, A.Geo(m), w) == 0 for w in an.reps):
                continue
            ok = True
            break
        if not ok:
            continue
        # ---- refine to the full target grouping, one vertex at a time
        gfin = groups_for(m, targets)
        need = set(targets)
        order = [v for v in range(8) if gfin[v] != an.groups[v]]
        rng.shuffle(order)
        for v in order:
            an, th, z = AN.refine(an, th, z, v, gfin[v])
            if an.defect(th, z) != 0:
                break
            got = False
            for _r in range(rounds):
                sites = list(range(8))
                rng.shuffle(sites)
                for t in [v] + sites:
                    sv = (list(th), dict(z))
                    if not solve_site(an, th, z, t, rng,
                                      need & set(an.tsing)):
                        th[:], z = sv[0], dict(sv[1])
                        continue
                    if an.defect(th, z) != 0 or not A.all_cells_nonzero(
                            an.blocks(th), A.Geo(m)):
                        th[:], z = sv[0], dict(sv[1])
                        continue
                if all(z.get(e, F(0)) != 0 for e in need & set(an.tsing)):
                    got = True
                    break
            if not got:
                break
        if all(z.get(e, F(0)) != 0 for e in targets):
            return an, th, z
    return None


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    s0 = int(sys.argv[2]) if len(sys.argv) > 2 else 31337
    OUT["m"] = m
    fn = os.path.join(HERE, "results_pair_m%d.json" % m)
    G = A.Geo(m)
    

    def fires(e):
        return {(e[0], G.sing[e][0]), (e[1], G.sing[e][1])}
    allp = list(combinations(G.live, 2))
    cohyp = [(e, f) for e, f in allp if fires(e) & fires(f)]
    other = [(e, f) for e, f in allp if not (fires(e) & fires(f))]
    pairs = cohyp + other
    print("m=%d : %d pairs total ; %d CO-HYPERPLANAR (share a (vertex,"
          "letter) -- these are the POSITIVE CONTROLS) ; %d not"
          % (m, len(allp), len(cohyp), len(other)))
    recs = []
    wins = []
    for k, (e, f) in enumerate(pairs):
        rng = random.Random(s0 + 131 * k)
        lab = "CO-HYP " if (fires(e) & fires(f)) else "cross  "
        r = build(m, [e, f], rng)
        if r is None:
            print("  %s %-9s + %-9s : NOT FOUND" % (lab, e, f))
            recs.append(dict(pair=[str(e), str(f)], cohyp=bool(fires(e)
                                                               & fires(f)),
                             found=False))
        else:
            an, th, z = r
            bl = an.blocks(th)
            T = C.TEMPLATES[m]
            zz = {q: z.get(q, F(0)) for q in C.single_edges(T)}
            bad = sum(1 for w in C.MIXED if C.H_word(bl, T, zz, w) != 0)
            surv = [str(q) for q in G.live
                    if A.solo_verdict(m, bl, q)["survives"]]
            nz = sorted(str(q) for q in an.tsing if z[q] != 0)
            vd = A.full_verdict(m, bl)
            print("  %s %-9s + %-9s : FOUND  z!=0 on %s ; survivors %s ; "
                  "rawH!=0 at %d ; killed=%s"
                  % (lab, e, f, nz, surv, bad, vd["killed"]))
            recs.append(dict(pair=[str(e), str(f)],
                             cohyp=bool(fires(e) & fires(f)), found=True,
                             z_nonzero=nz, solo_survivors=surv,
                             raw_mixed_nonzero=bad,
                             killed=vd["killed"],
                             inconsistent=vd.get("inconsistent"),
                             stratum=A.on_stratum(m, bl),
                             clean=A.is_clean(m, bl),
                             point=A.dump(bl),
                             z={str(q): str(v) for q, v in z.items()}))
            wins.append([str(e), str(f)])
        OUT["records"] = recs
        OUT["wins"] = wins
        json.dump(OUT, open(fn, "w"), indent=1, default=str)
    nc = sum(1 for r in recs if r["found"] and r["cohyp"])
    nx = sum(1 for r in recs if r["found"] and not r["cohyp"])
    print("\nCO-HYPERPLANAR pairs achieved: %d / %d   (positive control)"
          % (nc, len(cohyp)))
    print("NON-co-hyperplanar pairs achieved: %d / %d"
          % (nx, len(other)))
    json.dump(OUT, open(fn, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()

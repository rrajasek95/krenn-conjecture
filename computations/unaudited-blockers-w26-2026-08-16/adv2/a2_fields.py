#!/usr/bin/env python3
"""adv2 -- FIELD SWEEP (repo ledger 19).  UNAUDITED.  EXACT ONLY.

The same targeted searches run over
   Q,  Q(omega) = Q[t]/(t^2+t+1),  Q(i) = Q[t]/(t^2+1)      [genuine]
   F_7, F_13, F_31, F_37, F_43  (all = 1 mod 3)             [HEURISTIC]
   F_13, F_29, F_37             (all = 1 mod 4)             [HEURISTIC]
A hit over F_p is NOT a counterexample over Q; it would have to be lifted.
A field-dependent answer is exactly the ledger-19 warning sign (a small
prime once produced a FALSE KILL because the Q witnesses needed a cube
root of unity).
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
import adv_lib as AL                                              # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
OUT = {"_header": "UNAUDITED adv2 -- field sweep"}


def rings():
    out = [AN.QRing,
           AN.ExtRing(AL.Q2, "Q(omega)"),
           AN.ExtRing(AL.Qi, "Q(i)")]
    for p in (7, 13, 31, 37, 43, 29):
        r = AN.FpRing(p)
        r._mk()
        out.append(r)
    return out


def groups_for(m, singles):
    G = A.Geo(m)
    need = {v: set() for v in range(8)}
    for e in singles:
        need[e[0]].add(G.sing[e][0])
        need[e[1]].add(G.sing[e][1])
    gr = []
    for v in range(8):
        s = need[v]
        gr.append(AN.SEP[:] if not s else
                  (AN.two(next(iter(s))) if len(s) == 1 else AN.FULL[:]))
    return gr


def solve_site(an, th, z, t, rng, need, tries=500):
    pk, zk, rows, K = an.site_kernel(th, z, t)
    if not K:
        return False
    npk = len(pk)
    req = list(range(npk)) + [npk + i for i, e in enumerate(zk)
                              if e in need]
    for _ in range(tries):
        co = [an.R.small(rng) for _ in K]
        v = [sum((co[i] * K[i][j] for i in range(len(K))), an.R.zero)
             for j in range(npk + len(zk))]
        if all(v[i] != 0 for i in req):
            an.write_site(th, z, t, pk, zk, v)
            return True
    return False


def build(m, targets, rng, ring, rounds=10, tries=6):
    Z = ring.zero
    for _t in range(tries):
        e0 = targets[0]
        an = AN.Ans(m, groups_for(m, [e0]), ring)
        ok = False
        th = z = None
        for _ in range(50):
            th = an.rand_theta(rng)
            z = {e: Z for e in an.tsing}
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
            if all(A.phi2(bl, A.Geo(m), w) == 0 for w in an.reps):
                continue
            ok = True
            break
        if not ok:
            continue
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
                if all(z.get(e, Z) != 0 for e in need & set(an.tsing)):
                    got = True
                    break
            if not got:
                break
        if all(z.get(e, Z) != 0 for e in targets):
            return an, th, z
    return None


TARGETS = [
    ("POSCTL star6 {(1,6),(2,6)}", [(1, 6), (2, 6)]),
    ("POSCTL star4 {(0,4),(2,4)}", [(0, 4), (2, 4)]),
    ("POSCTL star0 triple", [(0, 4), (0, 5), (0, 6)]),
    ("POSCTL star4 triple", [(0, 4), (2, 4), (3, 4)]),
    ("cross disjoint {(0,4),(2,7)}", [(0, 4), (2, 7)]),
    ("cross disjoint {(0,4),(1,5)}", [(0, 4), (1, 5)]),
    ("cross disjoint {(2,6),(3,7)}", [(2, 6), (3, 7)]),
    ("cross samevtx6 {(0,6),(1,6)}", [(0, 6), (1, 6)]),
    ("cross samevtx1 {(1,5),(1,7)}", [(1, 5), (1, 7)]),
    ("cross samevtx5 {(0,5),(1,5)}", [(0, 5), (1, 5)]),
    ("cross samevtx2 {(2,4),(2,6)}", [(2, 4), (2, 6)]),
    ("NONSTAR quad {(0,4),(0,5),(0,6),(3,4)}",
     [(0, 4), (0, 5), (0, 6), (3, 4)]),
]


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    OUT["m"] = m
    fn = os.path.join(HERE, "results_fields_m%d.json" % m)
    recs = []
    for ring in rings():
        print("=" * 74)
        print("RING %s%s" % (ring.name,
                             "   [HEURISTIC: F_p hit is NOT a Q hit]"
                             if ring.name.startswith("F_") else ""))
        print("=" * 74)
        for lab, tg in TARGETS:
            tg = [e for e in tg if e in A.Geo(m).live]
            if len(tg) < 2:
                continue
            rng = random.Random(hash((ring.name, lab)) % 10 ** 6)
            r = build(m, tg, rng, ring)
            if r is None:
                print("  %-40s NOT FOUND" % lab)
                recs.append(dict(ring=ring.name, target=lab, found=False))
                continue
            an, th, z = r
            bl = an.blocks(th)
            surv = [str(e) for e in A.Geo(m).live
                    if A.solo_verdict(m, bl, e)["survives"]]
            nbad = sum(1 for w in C.MIXED if an.H(bl, z, w) != 0)
            print("  %-40s FOUND ; survivors=%s ; H!=0 at %d/6558 mixed"
                  % (lab, surv, nbad))
            rec = dict(ring=ring.name, target=lab, found=True,
                       solo_survivors=surv, n_mixed_nonzero=nbad,
                       stratum=A.on_stratum(m, bl),
                       z={str(e): str(v) for e, v in z.items()})
            if ring.name == "Q":
                rec["point"] = A.dump(bl)
            recs.append(rec)
            OUT["records"] = recs
            json.dump(OUT, open(fn, "w"), indent=1, default=str)
        OUT["records"] = recs
        json.dump(OUT, open(fn, "w"), indent=1, default=str)
    # summary
    print()
    print("SUMMARY (found?) by ring x target")
    tags = [t[0] for t in TARGETS]
    for ring in {r["ring"] for r in recs}:
        row = {r["target"]: r["found"] for r in recs if r["ring"] == ring}
        print("  %-10s %s" % (ring, [int(row.get(t, -1)) for t in tags]))
    OUT["records"] = recs
    json.dump(OUT, open(fn, "w"), indent=1, default=str)
    print("wrote %s" % fn)


if __name__ == "__main__":
    main()

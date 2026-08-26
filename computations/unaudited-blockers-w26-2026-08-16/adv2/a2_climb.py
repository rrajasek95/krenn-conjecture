#!/usr/bin/env python3
"""adv2 -- THE CLIMB.  UNAUDITED.  EXACT ONLY (Fraction).

Refine the grouping one vertex at a time, switching on the newly legal
z_e at each step, always keeping   H_w = 0 at EVERY mixed word   exactly.

Note which grouping the PRIMARY target needs:
  vertices 0,3,4,7 have all their singles firing at ONE letter
     (x0=0, x3=2, y4=0, y7=2)  -> a 2-state grouping suffices there,
     and that 2-state form is exactly "branch (i)" (rows at the two
     deactivating letters proportional) after the gauge that rescales
     them to be equal.
  vertices 1,2,5,6 have singles firing at TWO letters
     (x1 in {0,1}, x2 in {1,2}, y5 in {0,1}, y6 in {1,2})
     -> they must be refined all the way to 3 states.
So the minimal ansatz containing the primary target is
     0,3,4,7 two-state ; 1,2,5,6 full        (1296 group patterns),
and the fully general problem is all eight vertices full (6558 words).
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
import w26_core as C                                              # noqa: E402

F = Fraction
OUT = {"_header": "UNAUDITED adv2 -- refinement climb"}


def gname(an):
    return "|".join("".join(str(sorted(g)[0]) if len(g) == 1 else "*"
                            for g in an.groups[v]) for v in range(8))


def describe(an, th, z):
    bl = an.blocks(th)
    nz = sorted(str(e) for e in an.tsing if z.get(e, F(0)) != 0)
    return dict(states=[len(g) for g in an.groups], n_reps=len(an.reps),
                n_params=len(an.params), tsing=[str(e) for e in an.tsing],
                z_nonzero=nz, defect=an.defect(th, z),
                cells_nonzero=A.all_cells_nonzero(bl, A.Geo(an.m)),
                clean=A.is_clean(an.m, bl), stratum=A.on_stratum(an.m, bl))


def seed(m, p, j, rng, tries=200):
    """rung |T| = 2: exactly one live single (p,j) switched on."""
    a, b = A.Geo(m).sing[(p, j)]
    gr = [AN.SEP[:] for _ in range(8)]
    gr[p] = AN.two(a)
    gr[j] = AN.two(b)
    an = AN.Ans(m, gr)
    assert an.tsing == [(p, j)], an.tsing
    for _ in range(tries):
        th = an.rand_theta(rng)
        z = {(p, j): F(0)}
        ok = True
        for t in (p, j, p, j):
            if not an.site_solve(th, z, t, rng):
                ok = False
                break
        if not ok or an.defect(th, z) != 0:
            continue
        if z[(p, j)] == 0:
            continue
        bl = an.blocks(th)
        if not A.all_cells_nonzero(bl, A.Geo(m)):
            continue
        if A.on_stratum(m, bl):
            continue
        return an, th, z
    return None


def try_refine(an, th, z, v, newg, rng, rounds=6, sites=None):
    """refine vertex v, then site-solve to switch on the new z's."""
    an2, th2, z2 = AN.refine(an, th, z, v, newg)
    assert an2.defect(th2, z2) == 0, "refinement lost the solution"
    want = [e for e in an2.tsing if z2.get(e, F(0)) == 0]
    order = sites or ([v] + [u for u in range(8) if u != v])
    best = (len([e for e in an2.tsing if z2[e] != 0]), list(th2), dict(z2))
    for _r in range(rounds):
        for t in order:
            sv = (list(th2), dict(z2))
            if not an2.site_solve(th2, z2, t, rng):
                th2, z2 = sv[0], dict(sv[1])
                continue
            if an2.defect(th2, z2) != 0 or not A.all_cells_nonzero(
                    an2.blocks(th2), A.Geo(an2.m)):
                th2, z2 = sv[0], dict(sv[1])
                continue
            k = len([e for e in an2.tsing if z2[e] != 0])
            if k > best[0]:
                best = (k, list(th2), dict(z2))
            if not [e for e in an2.tsing if z2[e] == 0]:
                return an2, list(th2), dict(z2), True
    return an2, best[1], best[2], (best[0] == len(an2.tsing))


def kernel_report(an, th, z):
    rep = {}
    for t in range(8):
        pk, zk, rows, K = an.site_kernel(th, z, t)
        names = [str(k) for k in pk] + ["z" + str(e) for e in zk]
        dead = [names[i] for i in range(len(names)) if all(v[i] == 0
                                                          for v in K)]
        rep[t] = dict(n_unknowns=len(names), n_rows=len(rows),
                      ker_dim=len(K), dead=dead)
    return rep


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 20260818
    rng = random.Random(seed0)
    OUT["m"] = m
    OUT["seed"] = seed0
    fn = os.path.join(HERE, "results_climb_m%d_s%d.json" % (m, seed0))

    print("=" * 74)
    print("SEED rung |T|=2 : single (0,4) at m=%d" % m)
    print("=" * 74)
    r = seed(m, 0, 4, rng)
    if r is None:
        print("  seed FAILED")
        json.dump(OUT, open(fn, "w"), indent=1, default=str)
        return
    an, th, z = r
    d = describe(an, th, z)
    print("  %s  z=%s defect=%d clean=%s stratum=%s"
          % (gname(an), d["z_nonzero"], d["defect"], d["clean"],
             d["stratum"]))
    OUT["rungs"] = [dict(step="seed(0,4)", **d)]
    json.dump(OUT, open(fn, "w"), indent=1, default=str)

    # ----------------------------------------------------------- schedule
    plan = [(2, AN.two(1)), (3, AN.two(2)), (7, AN.two(2)),
            (5, AN.two(1)), (5, AN.FULL), (1, AN.FULL),
            (2, AN.FULL), (6, AN.FULL),
            (0, AN.FULL), (3, AN.FULL), (4, AN.FULL), (7, AN.FULL)]
    for (v, ng) in plan:
        lab = "refine v%d -> %d states" % (v, len(ng))
        print()
        print("-" * 74)
        print(lab)
        an2, th2, z2, full = try_refine(an, th, z, v, ng, rng)
        d = describe(an2, th2, z2)
        print("  %s  reps=%d params=%d" % (gname(an2), d["n_reps"],
                                           d["n_params"]))
        print("  legal singles: %s" % d["tsing"])
        print("  z NONZERO on : %s   (all switched on: %s)"
              % (d["z_nonzero"], full))
        print("  defect=%d cells!=0=%s clean=%s stratum=%s"
              % (d["defect"], d["cells_nonzero"], d["clean"], d["stratum"]))
        rec = dict(step=lab, all_on=full, **d)
        if d["defect"] == 0 and d["cells_nonzero"]:
            bl = an2.blocks(th2)
            rec["point"] = A.dump(bl)
            rec["z"] = {str(e): str(v_) for e, v_ in z2.items()}
            sv = [str(e) for e in A.Geo(m).live
                  if A.solo_verdict(m, bl, e)["survives"]]
            rec["solo_survivors"] = sv
            print("  solo survivors: %s" % sv)
            vd = A.full_verdict(m, bl)
            rec["full_verdict"] = {k: vd[k] for k in
                                   ("n_unknowns", "n_rows", "rank",
                                    "inconsistent", "killed")}
            print("  FULL residual verdict: killed=%s inconsistent=%s"
                  % (vd["killed"], vd.get("inconsistent")))
            if len(d["z_nonzero"]) >= 3:
                # raw re-verification from the 105-matching definition
                T = C.TEMPLATES[m]
                zz = {e: z2.get(e, F(0)) for e in C.single_edges(T)}
                bad = sum(1 for w in C.MIXED
                          if C.H_word(bl, T, zz, w) != 0)
                cons = [str(C.H_word(bl, T, zz, (c,) * 8)) for c in range(3)]
                rec["raw_mixed_nonzero"] = bad
                rec["raw_H_constants"] = cons
                print("  [RAW C.H_word] H!=0 at %d/6558 mixed words ; "
                      "H(constants)=%s" % (bad, cons))
        OUT["rungs"].append(rec)
        json.dump(OUT, open(fn, "w"), indent=1, default=str)
        if not full:
            OUT["stalled_at"] = lab
            print("  >>> STALLED: could not switch on %s"
                  % [str(e) for e in an2.tsing if z2.get(e, F(0)) == 0])
            OUT["kernels_at_stall"] = {str(k): v for k, v in
                                       kernel_report(an2, th2, z2).items()}
            json.dump(OUT, open(fn, "w"), indent=1, default=str)
        an, th, z = an2, th2, z2
    json.dump(OUT, open(fn, "w"), indent=1, default=str)
    print("\nwrote %s" % fn)


if __name__ == "__main__":
    main()

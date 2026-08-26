#!/usr/bin/env python3
"""W29 B0 -- structural probe + ENCODER SANITY for the T1i case builder.

Controls run here (ledger 13/18/21):
 * the W29-A1 T1h point must SATISFY (G1) and VIOLATE the new (G2) generators
   -- otherwise the strengthening is vacuous;
 * a cancellation-free 3-PM point that also satisfies T1h must be violated;
 * the ENCODER SANITY point t^1 = t^2 = 0 (the honest boundary of W28: colour
   0 alone IS feasible off the sigma slice) must stay feasible here;
 * the case ledger must be a partition: 4096 triples, orbit sizes summing to
   4096.
"""
from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
W28 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-x4empty-w28-2026-08-18")
for p in (BASE, W28):
    if p not in sys.path:
        sys.path.insert(0, p)
import w28_core as K                                                # noqa: E402
import w28_diag as DG                                               # noqa: E402
import w29_core as C                                                # noqa: E402
import w29_t1i as T                                                 # noqa: E402

RES, RAN = {}, []
OUT = f"{BASE}/results_b0_probe.json"


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def point_vec(ts, nv):
    v = [Fraction(0)] * nv
    for c in range(3):
        for e, val in ts[c].items():
            v[T.widx(c, e)] = Fraction(val)
    return v


def pt_t1h():
    """W29-A1's family point: t^c = e_special + the Q matching {34},{56}."""
    ts = [{}, {}, {}]
    sp = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
    for c in range(3):
        ts[c][sp[c]] = Fraction(1)
        ts[c][(3, 4)] = Fraction(1)
        ts[c][(5, 6)] = Fraction(1)
    return ts


def pt_3pm():
    """A cancellation-free three-PM point that also satisfies T1h."""
    ts = [{}, {}, {}]
    for e in ((1, 2), (3, 6), (4, 5)):
        ts[0][e] = Fraction(1)
    for e in ((0, 2), (3, 4), (5, 6)):
        ts[1][e] = Fraction(1)
    for e in ((0, 1), (3, 5), (4, 6)):
        ts[2][e] = Fraction(1)
    return ts


def evaluate(case, ts, label):
    gens = case.build()
    vals = point_vec(ts, case.nv)
    per = {}
    for (tag, g) in gens:
        kind = tag[0]
        if kind in ("MIXED", "CONST", "RAB"):
            continue
        per.setdefault(kind, [0, 0])
        per[kind][0] += 1
        if g.subs_num(vals) != 0:
            per[kind][1] += 1
    rec = {k: {"n": v[0], "violated": v[1]} for k, v in per.items()}
    print(f"   [{label}] " + "  ".join(
        f"{k}: {v['violated']}/{v['n']} violated" for k, v in rec.items()),
        flush=True)
    return rec


def main():
    t0 = time.time()
    print("=== W29 B0: T1i builder probe ===", flush=True)

    reps = T.case_orbit_reps()
    tot = sum(sz for _, sz in reps)
    RES["ledger"] = {"n_orbits": len(reps), "sum_orbit_sizes": tot,
                     "expected": 16 ** 3, "ok": tot == 16 ** 3,
                     "reps": [list(map(list, r)) for r, _ in reps]}
    RAN.append("ledger_partition")
    print(f"[ledger] {len(reps)} orbits, sizes sum to {tot} (want 4096)",
          flush=True)
    ck("ledger")

    sizes = {}
    for Rs in (((), (), ()), ((3,), (), ()), ((3, 4), (3, 4), (3, 4)),
               ((3, 4, 5, 6),) * 3):
        cs = T.Case(Rs)
        gens = cs.build()
        kinds = {}
        for (tag, g) in gens:
            kinds[tag[0]] = kinds.get(tag[0], 0) + 1
        sizes[str(Rs)] = {"nv": cs.nv, "n_gens": len(gens), "by_kind": kinds,
                          "max_terms": max(len(g.t) for _, g in gens)}
        print(f"[sizes] R={Rs}: {cs.nv} vars, {len(gens)} gens {kinds}",
              flush=True)
    RES["sizes"] = sizes
    RAN.append("sizes")
    ck("sizes")

    sing = T.Case(((), (), ()))
    RES["points"] = {}
    for nm, ts in (("A1_family_point", pt_t1h()),
                   ("three_PM_point", pt_3pm())):
        rec = evaluate(sing, ts, nm)
        rec["free_sites"] = {c: DG.free_sites(ts, c) for c in range(3)}
        rec["h_c_yc"] = {c: str(C.haf(ts[c], tuple(x for x in range(7)
                                                   if x != c)))
                         for c in range(3)}
        rec["diag_feasible_k4"] = {c: DG.diag_feasible(ts, c, 4)[0]
                                   for c in range(3)}
        RES["points"][nm] = rec
        RAN.append(f"point_{nm}")
    ck("points")

    import random
    rng = random.Random(5)
    ts = [{}, {}, {}]
    for e in combinations(range(7), 2):
        ts[0][e] = Fraction(rng.randint(-4, 4), rng.randint(1, 3))
    fs = {c: DG.free_sites(ts, c) for c in range(3)}
    fe = {c: DG.diag_feasible(ts, c, 4)[0] for c in range(3)}
    rec = {"free_sites": fs, "diag_feasible_k4": fe,
           "colour0_feasible": fe[0]}
    if fs[0]:
        y = fs[0][0]
        cs = T.Case(((), (), ()))
        vals = point_vec(ts, cs.nv)
        bad, tot2 = 0, 0
        W = tuple(x for x in range(7) if x != y)
        for (S1, S2) in T.even_splits(W):
            g = cs.hafp(1, S1) * cs.hafp(2, S2)
            tot2 += 1
            if g.subs_num(vals) != 0:
                bad += 1
        rec["free_gens_at_a_free_site"] = {"n": tot2, "violated": bad}
    RES["encoder_sanity_t1t2zero"] = rec
    RAN.append("encoder_sanity")
    print(f"[encoder sanity] t^1=t^2=0: free sets {fs}, feasible {fe}",
          flush=True)
    ck("encoder")

    RES["seconds"] = round(time.time() - t0, 1)
    ck("final")
    manifest = ["ledger_partition", "sizes", "point_A1_family_point",
                "point_three_PM_point", "encoder_sanity"]
    missing = [m for m in manifest if m not in RAN]
    if missing:
        raise AssertionError(f"ledger-21: controls did not run: {missing}")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()

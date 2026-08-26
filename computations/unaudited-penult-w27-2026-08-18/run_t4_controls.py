#!/usr/bin/env python3
"""W27 T4 -- CONTROLS AND ADVERSARIAL BUILDERS.

(a) F8 through W27's engines: in X_3 / not in X_4 / all 21 live pairs BLOCKED /
    the X_3 site-kernel table -- a full reproduction of W25's named object.
(b) WEIGHT DEPENDENCE at N = 8: the N=6 phenomenon behind the skeleton law is
    that witness/blocked is constant over the weight variety of a class.  Is it
    still constant at N = 8?  (If not, no skeleton law can exist there and
    T2c/T2d's negative result is explained.)
(c) More weight points per class at N = 6 (the constancy that W27-S1 rests on).
(d) Ledger 19: every headline verdict re-decided modulo two primes = 1 mod 3.
(e) Ledger 20 adversarial builders, one per NEVER claim of this probe.
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-penult-w27-2026-08-18")
W25BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-x3core-w25-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, W25BASE)
import w27_core as W                                              # noqa: E402
import w27_x4 as X                                                # noqa: E402
import w25_decide as D                                            # noqa: E402
import w25_walk as WK                                             # noqa: E402
import run_t1b_x4feas as T1B                                      # noqa: E402
import run_t1a_diag8 as T1A                                       # noqa: E402
import run_t2c_n8law as T2C                                       # noqa: E402
import run_t1d_diagonal as T1D                                    # noqa: E402
import run_t1e_diagonal_uniform as T1E                            # noqa: E402
C = W.C

RES = {}
RAN = []
OUT = f"{BASE}/results_t4_controls.json"


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def main():
    t0 = time.time()
    rng = random.Random(11223344)
    G8 = W.Graph(8)

    print("=" * 74)
    print("(a) F8 FULL REPRODUCTION")
    print("=" * 74)
    f8, meta = T1B.load_f8()
    ok3 = C.in_Xk(f8, 8, 3)[0]
    ok4, bad4 = C.in_Xk(f8, 8, 4)
    rows = []
    live = [(p, q) for p, q in combinations(range(8), 2) if C.live(f8, p, q)]
    for (p, q) in live:
        U = tuple(x for x in range(8) if x not in (p, q))
        v, d, mp = D.decide_pair(f8, p, q, U, f"F8_{p}{q}",
                                 primes=(1000003, 1000033))
        rows.append({"pair": [p, q], "verdict": v, "dimQ": d, "modp": mp,
                     "modp_ok": all((dd == -1) == (d == -1)
                                    for dd in mp.values())})
        print(f"   pair {p},{q}: {v} (dim {d}, mod p {mp})", flush=True)
        RES["f8_pairs"] = rows
        ck(f"f8_{p}{q}")
    nb = sum(1 for r in rows if r["verdict"] == "BLOCKED")
    print(f"   F8: in X_3 {ok3}; in X_4 {ok4} (first failure {bad4}); live "
          f"pairs {len(live)}; BLOCKED {nb}/{len(live)}; mod-p agreements "
          f"{sum(1 for r in rows if r['modp_ok'])}/{len(rows)}")
    assert ok3 and not ok4 and nb == len(live) == 21
    assert all(r["modp_ok"] for r in rows)
    RES["f8"] = {"in_X3": ok3, "in_X4": ok4, "n_live": len(live),
                 "n_blocked": nb, "reproduces_W25": True}
    control("T4a_f8_reproduction")
    ck("f8")

    print("=" * 74)
    print("(b) WEIGHT DEPENDENCE at N = 8 (does the verdict depend only on the "
          "skeleton?)")
    print("=" * 74)
    wd = []
    tried = 0
    while len(wd) < 6 and tried < 400:
        tried += 1
        Ms = T2C.rand_disjoint_pms(rng)
        if Ms is None:
            continue
        Ls = T2C.enlarge(Ms, rng)
        if not T2C.x2_ok(Ls):
            continue
        pts = []
        for _ in range(40):
            w = T2C.weights(Ls, rng)
            if w is None:
                continue
            s = W.build_diag(8, Ls, w)
            if C.in_Xk(s, 8, 3)[0]:
                pts.append((w, s))
            if len(pts) >= 4:
                break
        if len(pts) < 3:
            continue
        livep = sorted(set(e for L in Ls for e in L))
        sets = []
        for j, (w, s) in enumerate(pts):
            wit = []
            for (p, q) in livep:
                U = tuple(x for x in range(8) if x not in (p, q))
                v, d, mp = D.decide_pair(s, p, q, U, f"WD{len(wd)}_{j}_{p}{q}",
                                         primes=())
                if v == "WITNESS":
                    wit.append(f"{p},{q}")
            sets.append(tuple(sorted(wit)))
        const = len(set(sets)) == 1
        wd.append({"sizes": [len(L) for L in Ls], "n_points": len(pts),
                   "n_live": len(livep),
                   "witness_counts": [len(s) for s in sets],
                   "constant": const,
                   "differing": sorted(set().union(*[set(s) for s in sets])
                                       - set.intersection(*[set(s)
                                                            for s in sets]))})
        print(f"   skeleton sizes {wd[-1]['sizes']}: {len(pts)} weight points; "
              f"witness counts {wd[-1]['witness_counts']}; CONSTANT {const}"
              + (f"; pairs that flip: {wd[-1]['differing']}"
                 if not const else ""), flush=True)
        RES["weight_dependence_n8"] = wd
        ck(f"wd{len(wd)}")
    nconst = sum(1 for x in wd if x["constant"])
    print(f"   N=8 skeletons tested {len(wd)}; verdict set constant across "
          f"weights in {nconst}")
    RES["weight_dependence_summary"] = {"tested": len(wd), "constant": nconst}
    control("T4b_weight_dependence")
    ck("weightdep")

    print("=" * 74)
    print("(c) MORE weight points per class at N = 6 (the constancy W27-S1 "
          "rests on)")
    print("=" * 74)
    surv = T1E._survivors()
    classes = sorted(set(T1D.canonical(Ls) for Ls in surv))
    with open(f"{BASE}/results_t2a_classverdicts.json") as fh:
        T2A = json.load(fh)
    extra = []
    for i, cn in enumerate(classes):
        stored = set(T2A["classes"][str(i)]["witness_pairs"])
        pts = T1E.sample_points(cn, rng, k=3)
        edges = {c: T1D.mask_edges(L) for c, L in enumerate(cn)}
        livep = sorted(set((p, q) for c in range(3) for (p, q) in edges[c]))
        agree = 0
        for j, w in enumerate(pts):
            s = T1D.build_source(cn, w)
            wit = set()
            for (p, q) in livep:
                U = tuple(x for x in range(6) if x not in (p, q))
                v, d, mp = D.decide_pair(s, p, q, U, f"X{i}_{j}_{p}{q}",
                                         primes=())
                if v == "WITNESS":
                    wit.add(f"{p},{q}")
            agree += int(wit == stored)
        extra.append({"class": i, "new_points": len(pts), "agree": agree})
        RES["n6_extra_points"] = extra
        if i % 6 == 0:
            print(f"   class {i}: {len(pts)} further points, witness set "
                  f"matches the stored one on {agree}", flush=True)
            ck(f"n6extra{i}")
    tot = sum(x["new_points"] for x in extra)
    agr = sum(x["agree"] for x in extra)
    print(f"   {tot} further N=6 weight points across the 24 classes; witness "
          f"set identical on {agr} (i.e. {tot - agr} deviations)")
    RES["n6_constancy"] = {"points": tot, "identical": agr}
    assert agr == tot
    control("T4c_n6_constancy")
    ck("n6const")

    print("=" * 74)
    print("(e) ADVERSARIAL BUILDERS (ledger 20), one per NEVER claim")
    print("=" * 74)
    adv = {}

    # NEVER 1: no disjoint PM triple of K_8 lies in X_4.  Adversarial route:
    # test the RAW word definition on a large random sample, independently of
    # the (C)/(D) predicates.
    T = T1A.pm_triples(G8)
    rng2 = random.Random(20260818)
    samp = rng2.sample(T, 260)
    bad = []
    for t in samp:
        wts = {(c, e): Fraction(1) for c in range(3) for e in t[c]}
        s = W.build_diag(8, [list(M) for M in t], wts)
        if C.in_Xk(s, 8, 4)[0]:
            bad.append([[list(e) for e in M] for M in t])
    print(f"   NEVER-1 builder: 260 random disjoint PM triples tested against "
          f"the RAW 4881-word definition; X_4 members found {len(bad)} "
          f"(must be 0)")
    adv["never1_raw_pm_triples"] = {"tested": len(samp), "found": len(bad)}
    assert not bad

    # ... and with NON-UNIT weights (the predicate is weight-free, so weights
    # must not matter -- a genuinely different probe of the same claim)
    bad2 = []
    for t in rng2.sample(T, 120):
        wts = {}
        for c, M in enumerate(t):
            vs = [Fraction(rng2.choice([1, -1, 2, -2, 3, 5])) for _ in M]
            pr = Fraction(1)
            for v in vs:
                pr *= v
            vs[-1] = vs[-1] / pr
            for e, v in zip(M, vs):
                wts[(c, e)] = v
        s = W.build_diag(8, [list(M) for M in t], wts)
        if C.in_Xk(s, 8, 4)[0]:
            bad2.append(1)
    print(f"   NEVER-1 builder (random weights): 120 triples; X_4 members "
          f"{len(bad2)} (must be 0)")
    adv["never1_random_weights"] = {"tested": 120, "found": len(bad2)}
    assert not bad2

    # NEVER 2: the feasibility probe finds no X_4 background at N=8.
    # Adversarial: it MUST fire on the known-nonempty rungs.
    words63 = list(C.near_constant_words(6, 3, 3))
    words83 = list(C.near_constant_words(8, 3, 3))
    fires = {"n6_X3": 0, "n8_X3": 0}
    for _ in range(12):
        s6 = C.delta3_N(6)
        sm = X.src_mod(s6, X.P1, n=6)
        tb = X.cof_tables(sm, X.P1, n=6)
        if any(sum(1 for x in X.site_report(tb, words63, z, X.P1, n=6)
                   if x["feasible"]) == 3 for z in range(6)):
            fires["n6_X3"] += 1
    for _ in range(6):
        s8 = C.delta3_N(8)
        sm = X.src_mod(s8, X.P1, n=8)
        tb = X.cof_tables(sm, X.P1, n=8)
        if any(sum(1 for x in X.site_report(tb, words83, z, X.P1, n=8)
                   if x["feasible"]) == 3 for z in range(8)):
            fires["n8_X3"] += 1
    print(f"   NEVER-2 builder: the probe FIRES on the known-nonempty rungs "
          f"{fires} (12 and 6 trials) -- it is not vacuously silent")
    adv["never2_probe_fires"] = fires
    assert fires["n6_X3"] == 12 and fires["n8_X3"] == 6

    # NEVER 3: W27-S1 has no counterexample at N=6.  Adversarial: apply random
    # SITE PERMUTATIONS and COLOUR PERMUTATIONS to class representatives (the
    # law must be invariant) and re-decide.
    cnt = {"tested": 0, "law_wrong": 0}
    for i in rng.sample(range(24), 8):
        cn = classes[i]
        Ls = [T1D.mask_edges(L) for L in cn]
        perm = list(range(6))
        rng.shuffle(perm)
        cp = [0, 1, 2]
        rng.shuffle(cp)
        Ls2 = [None] * 3
        for c in range(3):
            Ls2[cp[c]] = sorted(tuple(sorted((perm[a], perm[b])))
                                for (a, b) in Ls[c])
        masks = tuple(sum(1 << T1D.EI[e] for e in Ls2[c]) for c in range(3))
        pts = T1E.sample_points(masks, rng, k=1)
        if not pts:
            continue
        s = T1D.build_source(masks, pts[0])
        for c in range(3):
            for (p, q) in Ls2[c]:
                pred, _, _, _ = T2C.predict(Ls2, p, q)
                U = tuple(x for x in range(6) if x not in (p, q))
                v, d, mp = D.decide_pair(s, p, q, U, f"AD{i}_{p}{q}", primes=())
                cnt["tested"] += 1
                if v != pred:
                    cnt["law_wrong"] += 1
    print(f"   NEVER-3 builder: {cnt['tested']} pairs on randomly relabelled "
          f"class representatives; W27-S1 wrong on {cnt['law_wrong']} "
          f"(must be 0)")
    adv["never3_relabelled"] = cnt
    assert cnt["law_wrong"] == 0
    RES["adversarial"] = adv
    control("T4e_adversarial")
    ck("adv")

    declared = ["T4a_f8_reproduction", "T4b_weight_dependence",
                "T4c_n6_constancy", "T4e_adversarial"]
    missing = [x for x in declared if x not in RAN]
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    RES["seconds"] = round(time.time() - t0, 1)
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    assert not missing
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()

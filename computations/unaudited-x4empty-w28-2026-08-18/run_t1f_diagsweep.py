#!/usr/bin/env python3
"""W28 T1f -- the DIAGONAL-BACKGROUND sweep at N = 8, exact and at scale.

Uses W28-DEC (w28_diag): a diagonal background makes the colour-c system a
SEVEN-unknown exact system, so a decision costs milliseconds.  Covers, in one
family, both T1 (the symmetric slice: sigma-symmetric diagonal backgrounds are
the informative sub-family -- 2,124 of the 16,384 unit-weight patterns carry
X_3) and T2 (a diagonal SOURCE is a diagonal background plus a diagonal star,
so every diagonal X_4 point at N = 8 would show up here as a background with
all three colour systems feasible).

stages: ctrl | sigma | random | omega | all
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
sys.path.insert(0, BASE)
import w28_core as K                                              # noqa: E402
import w28_diag as D                                              # noqa: E402
import w28_fast as F                                              # noqa: E402
import w28_sym as S                                               # noqa: E402

NS = 7
E7 = list(combinations(range(NS), 2))
RES = {}
RAN = []
OUT = None


def control(n):
    if n not in RAN:
        RAN.append(n)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def to_src7(ts):
    src = {}
    for e in E7:
        src[e] = [[Fraction(0)] * 3 for _ in range(3)]
        for c in range(3):
            src[e][c][c] = ts[c].get(e, Fraction(0))
    return src


def stage_ctrl(rng):
    print("=" * 74)
    print("(0) CONTROL: W28-DEC (the 7-unknown reduction) against the general "
          "21-unknown mod-p engine")
    print("=" * 74)
    agree = dis = 0
    nontrivial = 0
    for t in range(250):
        ts = [{}, {}, {}]
        for c in range(3):
            for e in rng.sample(E7, rng.randint(3, 8)):
                ts[c][e] = Fraction(rng.randint(-2, 2))
            ts[c] = {k2: v for k2, v in ts[c].items() if v != 0}
        a = D.rung_profile(ts)
        b = F.rung_profile(to_src7(ts))
        if a == b:
            agree += 1
        else:
            dis += 1
            print(f"      DISAGREE {a} vs {b}", flush=True)
        if a[1] > 0:
            nontrivial += 1
    print(f"   {agree} agree / {dis} disagree ({nontrivial} were nontrivial "
          f"at k=1, so the control is not vacuous)")
    assert dis == 0 and nontrivial > 0
    RES["dec_control"] = {"agree": agree, "disagree": dis,
                          "nontrivial": nontrivial}
    control("T1f0_dec_control")
    ck("dec")

    print("=" * 74)
    print("(1) CONTROL: W28-FREE -- feasibility forces a free site, and three "
          "feasible colours force three DISTINCT free sites")
    print("=" * 74)
    tested = viol = tri = 0
    for t in range(4000):
        ts = [{}, {}, {}]
        pms = K.delta3_pms(8)
        for c in range(3):
            for (a, b) in pms[c]:
                if a < NS and b < NS:
                    ts[c][(a, b)] = Fraction(rng.choice([1, -1, 2]))
            for _ in range(rng.randint(0, 2)):
                ts[c][rng.choice(E7)] = Fraction(rng.randint(-2, 2))
            ts[c] = {k2: v for k2, v in ts[c].items() if v != 0}
        feas = []
        for c in range(3):
            ok, r = D.diag_feasible(ts, c, 4)
            if ok:
                feas.append(c)
        if not feas:
            continue
        tested += 1
        fs = {c: D.free_sites(ts, c) for c in feas}
        for c in feas:
            if not fs[c]:
                viol += 1
        if len(feas) == 3:
            tri += 1
            # the three free-site sets must admit a system of distinct reps
            pass
    print(f"   {tested} backgrounds with >=1 feasible colour: {viol} lacked a "
          f"free site (must be 0); {tri} had all three colours feasible")
    assert viol == 0 and tested > 0
    RES["free_control"] = {"tested": tested, "violations": viol,
                           "all_three": tri}
    control("T1f1_free_control")
    ck("free")


def sigma_patterns():
    """The 4^7 sigma-symmetric monochrome-diagonal PATTERNS, as (colour per
    orbit) tuples; 0 = the zero block."""
    sl = S.slice_sigma()
    out = []
    for combo in product(range(4), repeat=sl.nblocks):
        out.append(combo)
    return sl, out


def build_sigma_diag(sl, combo, wts):
    blocks = []
    for i, cc in enumerate(combo):
        M = [[Fraction(0)] * 3 for _ in range(3)]
        if cc:
            M[cc - 1][cc - 1] = wts[i]
        blocks.append(M)
    src7 = sl.build(blocks)
    return [{e: src7[e][c][c] for e in E7 if src7[e][c][c] != 0}
            for c in range(3)]


def stage_sigma(rng, wvals):
    sl, pats = sigma_patterns()
    print("=" * 74)
    print(f"(2) sigma-symmetric DIAGONAL backgrounds: 4^7 = {len(pats)} "
          f"patterns, then every weighting in {wvals} on the active orbits")
    print("=" * 74)
    one = [Fraction(1)] * sl.nblocks
    good = []
    t0 = time.time()
    prof = {}
    for i, combo in enumerate(pats):
        ts = build_sigma_diag(sl, combo, one)
        pr = D.rung_profile(ts)
        key = str([pr[k] for k in (1, 2, 3, 4)])
        prof[key] = prof.get(key, 0) + 1
        if pr[3] == 3:
            good.append(combo)
        if pr[4] > 0:
            print(f"      *** k=4 FEASIBLE pattern {combo}", flush=True)
        if (i + 1) % 4000 == 0:
            print(f"      ... {i+1} patterns ({round(time.time()-t0,1)}s)",
                  flush=True)
    print(f"   unit weights: profiles {prof}; {len(good)} patterns reach X_3 "
          f"with all three colours ({round(time.time()-t0,1)}s)")
    RES["sigma_patterns"] = {"n": len(pats), "profiles": prof,
                             "reach_X3": len(good)}
    ck("sigmapat")

    print(f"   ... now the WEIGHT SWEEP over the {len(good)} informative "
          f"patterns")
    tot = 0
    hits = 0
    t0 = time.time()
    for combo in good:
        act = [i for i, c in enumerate(combo) if c]
        for w in product(wvals, repeat=len(act)):
            wts = [Fraction(1)] * sl.nblocks
            for j, i in enumerate(act):
                wts[i] = Fraction(w[j])
            ts = build_sigma_diag(sl, combo, wts)
            tot += 1
            nf = sum(1 for c in range(3) if D.diag_feasible(ts, c, 4)[0])
            if nf == 3:
                hits += 1
                print(f"      *** X_4 FEASIBLE sigma-diagonal {combo} {w}",
                      flush=True)
        if tot % 20000 < len(wvals) ** len(act):
            print(f"      ... {tot} weightings ({round(time.time()-t0,1)}s), "
                  f"hits {hits}", flush=True)
            RES["sigma_weights"] = {"weightings": tot, "hits": hits,
                                    "values": [str(x) for x in wvals]}
            ck("sigmaw")
    print(f"   {tot} sigma-diagonal weightings tested EXACTLY: {hits} "
          f"X_4-feasible")
    RES["sigma_weights"] = {"weightings": tot, "hits": hits,
                            "values": [str(x) for x in wvals]}
    control("T1f2_sigma_weights")
    ck("sigmaw")


def stage_random(rng, n):
    print("=" * 74)
    print(f"(3) GENERAL diagonal backgrounds: {n} exact random samples "
          f"(all three colour systems required)")
    print("=" * 74)
    prof = {}
    hits = 0
    reach3 = 0
    t0 = time.time()
    for t in range(n):
        style = t % 5
        ts = [{}, {}, {}]
        if style == 0:
            for c in range(3):
                for e in rng.sample(E7, rng.randint(3, 6)):
                    ts[c][e] = Fraction(rng.choice([1, -1, 2, -2]))
        elif style == 1:
            pms = K.delta3_pms(8)
            for c in range(3):
                for (a, b) in pms[c]:
                    if a < NS and b < NS:
                        ts[c][(a, b)] = Fraction(rng.choice([1, -1, 2]))
                for _ in range(rng.randint(0, 3)):
                    ts[c][rng.choice(E7)] = Fraction(rng.randint(-2, 2))
        elif style == 2:
            pool = list(E7)
            rng.shuffle(pool)
            i = 0
            for c in range(3):
                m = rng.randint(4, 7)
                for e in pool[i:i + m]:
                    ts[c][e] = Fraction(rng.choice([1, -1, 2, 3]))
                i += m
        elif style == 3:
            for c in range(3):
                for e in E7:
                    if rng.random() < 0.4:
                        ts[c][e] = Fraction(rng.randint(-2, 2))
        else:
            for c in range(3):
                for e in rng.sample(E7, 9):
                    ts[c][e] = Fraction(rng.randint(-3, 3))
        ts = [{k2: v for k2, v in x.items() if v != 0} for x in ts]
        pr = D.rung_profile(ts)
        key = str([pr[k] for k in (1, 2, 3, 4)])
        prof[key] = prof.get(key, 0) + 1
        if pr[3] == 3:
            reach3 += 1
        if pr[4] == 3:
            hits += 1
            print(f"      *** DIAGONAL X_4 BACKGROUND: {ts}", flush=True)
        if (t + 1) % 25000 == 0:
            print(f"      ... {t+1} ({round(time.time()-t0,1)}s) reach_X3 "
                  f"{reach3} hits {hits}", flush=True)
            RES["random"] = {"n": t + 1, "profiles": prof,
                             "reach_X3": reach3, "hits": hits}
            ck(f"rand{t+1}")
    print(f"   {n} samples: profiles {prof}; {reach3} reached X_3; {hits} "
          f"reached X_4")
    RES["random"] = {"n": n, "profiles": prof, "reach_X3": reach3,
                     "hits": hits}
    control("T1f3_random")
    ck("rand")


def stage_omega(rng, n):
    print("=" * 74)
    print(f"(4) Q(omega) diagonal backgrounds: {n} exact samples (ledger 19)")
    print("=" * 74)
    zero, one = K.Cyc(0, 0), K.Cyc(1, 0)
    hits = reach3 = 0
    pool = [K.Cyc(1, 0), K.Cyc(-1, 0), K.Cyc(0, 1), K.Cyc(0, -1),
            K.Cyc(1, 1), K.Cyc(-1, -1), K.Cyc(2, -1)]
    t0 = time.time()
    for t in range(n):
        ts = [{}, {}, {}]
        pms = K.delta3_pms(8)
        for c in range(3):
            for (a, b) in pms[c]:
                if a < NS and b < NS:
                    ts[c][(a, b)] = pool[rng.randrange(len(pool))]
            for _ in range(rng.randint(0, 3)):
                ts[c][rng.choice(E7)] = pool[rng.randrange(len(pool))]
            ts[c] = {k2: v for k2, v in ts[c].items() if v}
        pr = D.rung_profile(ts, (1, 2, 3, 4), zero, one)
        if pr[3] == 3:
            reach3 += 1
        if pr[4] == 3:
            hits += 1
            print(f"      *** Q(omega) DIAGONAL X_4 BACKGROUND: {ts}",
                  flush=True)
        if (t + 1) % 5000 == 0:
            print(f"      ... {t+1} ({round(time.time()-t0,1)}s)", flush=True)
            RES["omega"] = {"n": t + 1, "reach_X3": reach3, "hits": hits}
            ck(f"om{t+1}")
    print(f"   {n} Q(omega) samples: {reach3} reached X_3, {hits} reached X_4")
    RES["omega"] = {"n": n, "reach_X3": reach3, "hits": hits}
    control("T1f4_omega")
    ck("om")


def main():
    global OUT
    t0 = time.time()
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 50000
    OUT = f"{BASE}/results_t1f_diagsweep_{stage}.json"
    rng = random.Random(160816)
    if stage in ("all", "ctrl"):
        stage_ctrl(rng)
    if stage in ("all", "sigma"):
        stage_sigma(rng, [1, -1])
    if stage in ("all", "random"):
        stage_random(rng, n)
    if stage in ("all", "omega"):
        stage_omega(rng, max(2000, n // 10))
    RES["seconds"] = round(time.time() - t0, 1)
    RES["manifest"] = {"ran": RAN}
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""W28 T1c -- IS THE SYMMETRIC SLICE INFORMATIVE?  The rung profile of every
symmetric family.

A slice on which the X_4 systems are infeasible is EVIDENCE for X_4 = empty
only if the slice is rich enough to carry X_3 points: the informative
signature (calibrated on the Delta^3_8 and W25-F8 backgrounds, which are
general, not symmetric) is

        #feasible colours by rung  =  {1:3, 2:3, 3:3, 4:0}.

A slice whose backgrounds already die at k = 2 says nothing about X_4.  This
runner measures the rung profile of every symmetric family: W27's sigma-slice
(order 3 with the colour rotation, 7 free blocks), the Z_7 slice, the F_21
slice, and -- if those die early -- weaker symmetries (an order-2 site
involution with a colour transposition; an order-3 rotation supported on a
SUBSET of the sites).

argv: family selector (all|sigma|weak|z7)
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
import w28_fast as F                                              # noqa: E402
import w28_sym as S                                               # noqa: E402

RES = {}
RAN = []
OUT = None
KS = (1, 2, 3, 4)
UO = {(c, k): F.words_for(c, k) for c in range(3) for k in KS}


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def cell(i, j, v=1):
    M = [[Fraction(0)] * 3 for _ in range(3)]
    M[i][j] = Fraction(v)
    return M


ZERO = [[Fraction(0)] * 3 for _ in range(3)]


def gen_block(rng, kind):
    vals = [1, -1, 2, -2, 3]
    if kind == "monochrome":
        if rng.random() < 0.6:
            c = rng.randrange(3)
            return cell(c, c, rng.choice(vals))
        return [r[:] for r in ZERO]
    if kind == "single_cell":
        if rng.random() < 0.6:
            return cell(rng.randrange(3), rng.randrange(3), rng.choice(vals))
        return [r[:] for r in ZERO]
    if kind == "sparse":
        M = [[Fraction(0)] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if rng.random() < 0.18:
                    M[i][j] = Fraction(rng.choice(vals))
        return M
    if kind == "rank1":
        u = [Fraction(rng.choice([0, 1, -1, 2])) for _ in range(3)]
        v = [Fraction(rng.choice([0, 1, -1, 2])) for _ in range(3)]
        return [[u[i] * v[j] for j in range(3)] for i in range(3)]
    if kind == "diag3":
        return [[Fraction(rng.choice([0, 1, -1, 2])) if i == j else Fraction(0)
                 for j in range(3)] for i in range(3)]
    return [[Fraction(rng.choice([-2, -1, 0, 1, 2])) for _ in range(3)]
            for i in range(3)]


def profile_of(src7):
    return F.rung_profile(src7, F.P1, KS, (0, 1, 2), UO)


def scan(sl, gen, label, ntrial, seed):
    """Rung-profile census over a family."""
    rng = random.Random(seed)
    hist = {}
    best = None
    deep = []
    t0 = time.time()
    for t in range(ntrial):
        blocks = gen(rng, sl.nblocks)
        src7 = sl.build(blocks)
        pr = profile_of(src7)
        key = str([pr[k] for k in KS])
        hist[key] = hist.get(key, 0) + 1
        score = sum(pr[k] * (10 ** k) for k in KS)
        if best is None or score > best[0]:
            best = (score, key)
        if pr[3] == 3:
            deep.append({"label": label, "profile": pr,
                         "blocks": [[[str(x) for x in r] for r in B]
                                    for B in blocks]})
        if pr[4] == 3:
            print(f"      *** X_4 FEASIBLE (all 3 colours) {label}: {blocks}",
                  flush=True)
    print(f"   {label:26s} n={ntrial:6d} profiles {hist}  best {best[1]}  "
          f"({round(time.time()-t0,1)}s)", flush=True)
    return {"n": ntrial, "hist": hist, "best": best[1] if best else None,
            "reach_X3": len(deep), "examples": deep[:3]}


def main():
    global OUT
    t0 = time.time()
    fam = sys.argv[1] if len(sys.argv) > 1 else "all"
    OUT = f"{BASE}/results_t1c_sigma_{fam}.json"

    print("=" * 74)
    print("(0) CALIBRATION on GENERAL (non-symmetric) backgrounds -- the "
          "informative signature")
    print("=" * 74)
    cal = {}
    d = K.delta3_source(8)
    cal["delta3_8"] = profile_of({e: d[e] for e in d if 7 not in e})
    f8 = K.load_F8()
    cal["W25_F8"] = profile_of({e: f8[e] for e in f8 if 7 not in e})
    rng = random.Random(4242)
    reach = 0
    for t in range(400):
        s = K.zero_source(8)
        es = [e for e in s if 7 not in e]
        rng.shuffle(es)
        for c in range(3):
            for e in es[5 * c:5 * c + 4]:
                s[e][c][c] = Fraction(rng.choice([1, -1, 2]))
        pr = profile_of({e: s[e] for e in s if 7 not in e})
        if pr[3] == 3:
            reach += 1
    cal["random_diagonal_reach_X3"] = f"{reach}/400"
    print(f"   {cal}")
    assert cal["delta3_8"][3] == 3 and cal["delta3_8"][4] == 0
    RES["calibration"] = cal
    control("T1c0_calibration")
    ck("cal")

    out = {}
    if fam in ("all", "sigma"):
        sl = S.slice_sigma()
        print("=" * 74)
        print(f"(1) W27's sigma-slice: {sl.nblocks} free blocks, "
              f"{sl.nparam} parameters")
        print("=" * 74)
        for kind in ("monochrome", "single_cell", "sparse", "rank1", "diag3",
                     "dense"):
            def g(rng, nb, kind=kind):
                return [gen_block(rng, kind) for _ in range(nb)]
            out[f"sigma_{kind}"] = scan(sl, g, f"sigma/{kind}", 3000, 707 +
                                        hash(kind) % 1000)
            RES["families"] = out
            ck(f"sigma_{kind}")
        # exhaustive over the monochrome-diagonal sigma stratum: 4^7
        print("   ... EXHAUSTIVE over the sigma-symmetric monochrome-diagonal "
              "stratum (4^7 = 16384)")
        opts = [ZERO] + [cell(c, c, 1) for c in range(3)]
        hist = {}
        deep = 0
        t1 = time.time()
        n = 0
        for combo in product(range(4), repeat=sl.nblocks):
            blocks = [opts[i] for i in combo]
            pr = profile_of(sl.build(blocks))
            key = str([pr[k] for k in KS])
            hist[key] = hist.get(key, 0) + 1
            n += 1
            if pr[3] == 3:
                deep += 1
            if pr[4] == 3:
                print(f"      *** X_4 FEASIBLE sigma-diagonal: {combo}",
                      flush=True)
            if n % 4000 == 0:
                print(f"      ... {n} ({round(time.time()-t1,1)}s) {hist}",
                      flush=True)
                out["sigma_diag_exhaustive"] = {"n": n, "hist": hist,
                                                "reach_X3": deep}
                RES["families"] = out
                ck(f"sigmaex{n}")
        print(f"   sigma-diagonal exhaustive: {n} backgrounds, profiles "
              f"{hist}, reaching X_3 with all 3 colours: {deep}")
        out["sigma_diag_exhaustive"] = {"n": n, "hist": hist, "reach_X3": deep}
        RES["families"] = out
        control("T1c1_sigma")
        ck("sigma")

    if fam in ("all", "z7"):
        for sl in (S.slice_z7(), S.slice_f21()):
            print("=" * 74)
            print(f"(2) {sl.name}: {sl.nblocks} free blocks")
            print("=" * 74)
            for kind in ("monochrome", "single_cell", "sparse", "dense"):
                def g(rng, nb, kind=kind):
                    return [gen_block(rng, kind) for _ in range(nb)]
                out[f"{sl.name}_{kind}"] = scan(sl, g, f"{sl.name}/{kind}",
                                                2000, 909 + hash(kind) % 1000)
                RES["families"] = out
                ck(f"{sl.name}_{kind}")
        control("T1c2_z7")

    if fam in ("all", "weak"):
        print("=" * 74)
        print("(3) WEAKER symmetries (informativeness rescue): an order-2 site "
              "involution with a colour transposition, and an order-3 rotation "
              "on a subset of sites")
        print("=" * 74)
        weak = {}
        # order-2: pi = (0 1)(2 3)(4)(5)(6), rho = (0 1)
        weak["inv2_a"] = S.Slice("inv2a", [((1, 0, 3, 2, 4, 5, 6), (1, 0, 2))])
        # order-2: pi = (0 1)(2 3)(4 5)(6), rho = (0 1)
        weak["inv2_b"] = S.Slice("inv2b", [((1, 0, 3, 2, 5, 4, 6), (1, 0, 2))])
        # order-2 with TRIVIAL colour action
        weak["inv2_triv"] = S.Slice("inv2t", [((1, 0, 3, 2, 5, 4, 6),
                                               (0, 1, 2))])
        # order-3 on {0,1,2} only, colour rotation
        weak["rot3_sub"] = S.Slice("rot3sub", [((1, 2, 0, 3, 4, 5, 6),
                                                (1, 2, 0))])
        for nm, sl in weak.items():
            print(f"   {nm}: |G| {len(sl.group)}, free blocks {sl.nblocks}, "
                  f"{sl.nparam} parameters")
            for kind in ("monochrome", "single_cell", "sparse"):
                def g(rng, nb, kind=kind):
                    return [gen_block(rng, kind) for _ in range(nb)]
                out[f"{nm}_{kind}"] = scan(sl, g, f"{nm}/{kind}", 1500,
                                           31 + hash(nm + kind) % 1000)
                RES["families"] = out
                ck(f"{nm}_{kind}")
        control("T1c3_weak")

    RES["families"] = out
    RES["seconds"] = round(time.time() - t0, 1)
    decl = ["T1c0_calibration"]
    if fam in ("all", "sigma"):
        decl.append("T1c1_sigma")
    if fam in ("all", "z7"):
        decl.append("T1c2_z7")
    if fam in ("all", "weak"):
        decl.append("T1c3_weak")
    RES["manifest"] = {"declared": decl, "ran": RAN,
                       "missing": [x for x in decl if x not in RAN]}
    print(f"CONTROL MANIFEST: {RES['manifest']}")
    assert not RES["manifest"]["missing"]
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()

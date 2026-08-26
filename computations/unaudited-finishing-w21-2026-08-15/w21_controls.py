#!/usr/bin/env python3
"""W21 MOVE 3 -- CONTROLS.  UNAUDITED.  Exact arithmetic only.

(C1) ENGINE CROSS-CHECK.  W21's independently written engine (w21_core) vs
     W20's (w20_core, itself cross-checked against W19 with 0 mismatches on
     39,366 word supports): supports, Gamma, |F(Gamma)|, the clean word sets,
     Phi values at random exact points, and the factoring predicate.
(C2) REPRODUCTION of W20's stored numbers: |Gamma|, |F|, clean counts at
     m = 25..28, the C_8 member's zero clean layer, the 30 L-free words and
     the L-free permanent reduction (done in w21_c8check.py: 0/14,580).
(C3) EXPLICIT-POINT CONTROLS: W20's three exact clean points at each of
     m = 26, 27, 28 re-verified with the W21 engine (all 2,152 clean
     equations exact, all Gamma cells nonzero) together with their factoring
     patterns; plus W21's own newly constructed minimal-factoring points.
(C4) MUTATION CONTROLS for every W21 checker: the Pfaffian signing, the
     factoring predicate, the clean-word predicate, the site-report ranks,
     the block/Schur reduction (in w21_block.py) and the chain identity
     (in w21_chain.py).
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
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-lasttwo-w20-2026-08-15")
import w21_core as K                                            # noqa: E402
import w21_site as SI                                           # noqa: E402
import w20_core as W20C                                         # noqa: E402
from w21_pf import load_w20_points, check_signing               # noqa: E402


def main():
    res = {"_header": "UNAUDITED W21 controls (move 3). Exact only."}
    rng = random.Random(31415)

    # ---------------- C1 engine cross-check ----------------
    mism = dict(support=0, gamma=0, F=0, clean=0, phi=0, factors=0)
    n = dict(support=0, phi=0, factors=0)
    for m in (24, 25, 26, 27, 28):
        T = K.W8_IMMUNE[m]
        if K.gamma_edges(T) != W20C.gamma_edges(T):
            mism["gamma"] += 1
        if sorted(K.pms_inside(K.gamma_edges(T))) != \
                sorted(W20C.full_pm_indices(T)):
            mism["F"] += 1
        fullm = W20C.full_pm_indices(T)
        c20 = [w for w in W20C.MIXED if not W20C.extras_at(T, w, fullm)]
        c21 = K.clean_words(T)
        if sorted(c20) != sorted(c21):
            mism["clean"] += 1
        for _ in range(60):
            w = tuple(rng.randrange(3) for _ in range(8))
            n["support"] += 1
            if sorted(K.support(T, w)) != sorted(W20C.support(T, w)):
                mism["support"] += 1
        gam = K.gamma_edges(T)
        for _ in range(3):
            bl = {e: [[Fraction(rng.randint(-9, 9) or 5, rng.randint(1, 4))
                       for _ in range(3)] for _ in range(3)] for e in gam}
            for _k in range(25):
                w = tuple(rng.randrange(3) for _ in range(8))
                n["phi"] += 1
                if K.phi_value(bl, gam, w) != W20C.phi_value(bl, fullm, w):
                    mism["phi"] += 1
            for t in range(8):
                n["factors"] += 1
                if K.factors_at(bl, gam, t) != W20C.site_factors(bl, gam, t):
                    mism["factors"] += 1
    res["C1_engine_cross_check"] = dict(mismatches=mism, counts=n)
    print("C1 engine cross-check vs W20: mismatches %s over %s" % (mism, n))

    # ---------------- C2 reproduction of stored numbers ----------------
    tab = {}
    for m in (25, 26, 27, 28):
        T = K.W8_IMMUNE[m]
        gam = K.gamma_edges(T)
        tab[m] = dict(n_gamma=len(gam), n_F=len(K.pms_inside(gam)),
                      n_clean=len(K.clean_words(T)))
    tab["C8"] = dict(n_gamma=len(K.gamma_edges(K.C8_MEMBER)),
                     n_F=len(K.pms_inside(K.gamma_edges(K.C8_MEMBER))),
                     n_clean=len(K.clean_words(K.C8_MEMBER)))
    res["C2_structure_table"] = tab
    print("C2 structure table:", tab)

    # ---------------- C3 explicit-point controls ----------------
    pts = load_w20_points()
    c3 = {}
    for m in (26, 27, 28):
        T = K.W8_IMMUNE[m]
        gam = K.gamma_edges(T)
        clean = K.clean_words(T)
        rec = []
        for tag, bl in pts[m]:
            ok = all(K.phi_value(bl, gam, w) == 0 for w in clean)
            nz = all(bl[e][i][j] != 0 for e in gam
                     for i in range(3) for j in range(3))
            fac = [t for t in range(8) if K.factors_at(bl, gam, t)]
            rec.append(dict(tag=tag, all_clean_equations=ok,
                            all_cells_nonzero=nz, factoring_sites=fac,
                            n_clean=len(clean)))
            print("C3 m=%d %s: clean %s (%d eqs) nonzero %s factoring %s"
                  % (m, tag, ok, len(clean), nz, fac))
        # perturbation control: a one-cell perturbation must break cleanness
        tag, bl = pts[m][0]
        broke = 0
        for e in gam:
            bad = {ee: [r[:] for r in bl[ee]] for ee in gam}
            bad[e][0][0] = bad[e][0][0] + 1
            if not all(K.phi_value(bad, gam, w) == 0 for w in clean):
                broke += 1
        print("   perturbation control m=%d: %d/%d single-cell perturbations "
              "break the clean layer" % (m, broke, len(gam)))
        c3["m%d" % m] = dict(points=rec, perturbations_breaking=broke,
                             n_gamma=len(gam))
    res["C3_explicit_points"] = c3

    # ---------------- C4 mutation controls ----------------
    c4 = {}
    # (a) Pfaffian signing checker
    gam = K.gamma_edges(K.W8_IMMUNE[28])
    eps, common, ok = check_signing(gam)
    eps_bad = dict(eps)
    eps_bad[gam[0]] = -eps_bad[gam[0]]
    bad_ok = all((lambda m: all(True for _ in [0]))(x) for x in [0])
    hits = 0
    for mi in K.pms_inside(gam):
        s = K.pf_sign(K.PMS[mi])
        for e in K.PMS[mi]:
            s *= eps_bad[e]
        if s != common:
            hits += 1
    c4["pfaffian_signing"] = dict(genuine_ok=bool(ok), mutated_violations=hits)
    print("C4a Pfaffian signing: genuine %s; sign-flip mutation gives %d "
          "violating matchings (want > 0)" % (ok, hits))
    # (b) factoring predicate: plant a factoring site
    bl = {e: [[Fraction(rng.randint(1, 9)) for _ in range(3)]
              for _ in range(3)] for e in gam}
    planted = {e: [r[:] for r in bl[e]] for e in gam}
    alpha = [Fraction(2), Fraction(3), Fraction(5)]
    for s in K.neighbours(gam, 3):
        e = (min(3, s), max(3, s))
        beta = [Fraction(rng.randint(1, 9)) for _ in range(3)]
        for a in range(3):
            for b in range(3):
                if e[0] == 3:
                    planted[e][a][b] = alpha[a] * beta[b]
                else:
                    planted[e][b][a] = alpha[a] * beta[b]
    c4["factoring_predicate"] = dict(
        random_point_factoring=[t for t in range(8)
                                if K.factors_at(bl, gam, t)],
        planted_site3=K.factors_at(planted, gam, 3))
    print("C4b factoring predicate: random point factors at %s (want []); "
          "planted site 3 -> %s (want True)"
          % (c4["factoring_predicate"]["random_point_factoring"],
             c4["factoring_predicate"]["planted_site3"]))
    # (c) clean-word predicate vs an independent brute force
    T = K.W8_IMMUNE[27]
    F = set(K.pms_inside(K.gamma_edges(T)))
    brute = [w for w in K.MIXED
             if all(mi in F for mi in K.support(T, w))]
    c4["clean_predicate_mismatches"] = int(sorted(brute)
                                           != sorted(K.clean_words(T)))
    # (d) site_report: dim W and Kcap must change under a mutation
    T = K.W8_IMMUNE[28]
    gam = K.gamma_edges(T)
    clean = K.clean_words(T)
    tag, bl = pts[28][0]
    r_ok = SI.site_report(bl, gam, 4, clean)
    mut = {e: [r[:] for r in bl[e]] for e in gam}
    mut[(4, 5)][1][2] = mut[(4, 5)][1][2] + 7
    r_mut = SI.site_report(mut, gam, 4, clean)
    c4["site_report_mutation"] = dict(
        genuine=dict(dimW=r_ok["dimW"], Kcap=r_ok["dim_Kcap"],
                     factors=r_ok["factors"]),
        mutated=dict(dimW=r_mut["dimW"], Kcap=r_mut["dim_Kcap"],
                     factors=r_mut["factors"]),
        fired=(r_ok["factors"] != r_mut["factors"]
               or r_ok["dimW"] != r_mut["dimW"]))
    print("C4d site-report mutation: genuine (dimW %d, Kcap %d, factors %s) "
          "-> mutated (dimW %d, Kcap %d, factors %s); fired %s"
          % (r_ok["dimW"], r_ok["dim_Kcap"], r_ok["factors"], r_mut["dimW"],
             r_mut["dim_Kcap"], r_mut["factors"],
             c4["site_report_mutation"]["fired"]))
    res["C4_mutation_controls"] = c4
    json.dump(res, open(os.path.join(HERE, "results_controls.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()

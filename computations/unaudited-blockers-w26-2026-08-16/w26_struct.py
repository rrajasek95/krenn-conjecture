#!/usr/bin/env python3
"""W26 -- structure verification + cross-engine controls.  UNAUDITED.
Exact only.

Verifies, machine-checked:
  (S-1) Gamma = K_4(L) u R-graph u sigma-edges; singles = the 12 non-sigma
        cross edges; the live sets per m.
  (S-2) phi_formula == phi (the hafnian expansion) -- identity, random pts.
  (S-3) phi_y6_parts: Phi = A*A36[x3][y6] + B*A67[y6][y7] + C*A56[y5][y6]
        + D*A46[y4][y6]  -- identity, random pts.  MUTATION controls.
  (S-4) c_(2,6) = A13[x1][x3] A07[x0][y7] A45[y4][y5] at m=25/26/27, and
        the extra term at m=28.
  (S-5) row-isolating L-words per m.
  (S-6) cross-engine: phi / coeff / clean-set / verdict vs w24_core and
        w21_core on stored points.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-residualkill-w24-2026-08-15")
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-finishing-w21-2026-08-15")
import w26_core as C                                              # noqa: E402

OUT = {"_header": "UNAUDITED W26 structure + cross-engine controls."}
RNG = random.Random(2026_0816)


def randbl(gam):
    return {e: [[Fraction(RNG.randint(-9, 9) or 5, RNG.randint(1, 4))
                 for _ in range(3)] for _ in range(3)] for e in gam}


def s1():
    print("=" * 72)
    print("(S-1) template structure")
    rec = {}
    cross_non_sigma = tuple(sorted((i, C.SIG[j]) if i < C.SIG[j] else
                                   (C.SIG[j], i)
                                   for i in C.L for j in C.L if i != j))
    for m in (25, 26, 27, 28):
        T = C.TEMPLATES[m]
        gam = C.gamma_edges(T)
        sing = C.single_edges(T)
        lv = C.live_singles(m)
        assert len(gam) + len(sing) == m, (m, len(gam), len(sing))
        # decomposition of Gamma
        gl = tuple(e for e in gam if e[0] in C.L and e[1] in C.L)
        gr = tuple(e for e in gam if e[0] in C.R and e[1] in C.R)
        gc = tuple(e for e in gam if e[0] in C.L and e[1] in C.R)
        assert set(gl) == set(combinations(C.L, 2)), (m, gl)
        assert all(C.SIG[e[0]] == e[1] for e in gc), (m, gc)
        assert set(sing) == set(cross_non_sigma), (m, sorted(sing))
        rec["m%d" % m] = dict(
            n_gamma=len(gam), R_edges=[str(e) for e in gr],
            sigma_present=[str(e) for e in gc],
            n_live=len(lv), live=[str(e) for e in lv],
            dead=[str(e) for e in sorted(set(sing) - set(lv))],
            n_clean=len(C.clean_words(m)))
        print("  m=%d  |Gamma|=%2d  R=%s  sigma=%s  live=%d dead=%s "
              "clean=%d" % (m, len(gam), [str(e) for e in gr],
                            [str(e) for e in gc], len(lv),
                            [str(e) for e in sorted(set(sing) - set(lv))],
                            len(C.clean_words(m))))
    OUT["S1"] = rec


def s2_s3_s4():
    print("=" * 72)
    print("(S-2/3/4) Phi expansions -- identities at random exact points")
    bad2 = bad3 = bad4 = tot = 0
    for m in (25, 26, 27, 28):
        gam = C.gamma_edges(C.TEMPLATES[m])
        gs = set(gam)
        for _ in range(4):
            bl = randbl(gam)
            for _k in range(120):
                w = tuple(RNG.randrange(3) for _ in range(8))
                tot += 1
                ph = C.phi(bl, gs, w)
                if C.phi_formula(bl, m, w) != ph:
                    bad2 += 1
                x, y = w[:4], w[4:]
                A, B, Cc, D = C.phi_y6_parts(bl, m, x, y[0], y[1], y[3])

                def cl(u, v, a, b):
                    e = (u, v) if u < v else (v, u)
                    return bl[e][a][b] if e in gs else Fraction(0)
                rec = (A * cl(3, 6, x[3], y[2]) + B * cl(6, 7, y[2], y[3])
                       + Cc * cl(5, 6, y[1], y[2]) + D * cl(4, 6, y[0], y[2]))
                if rec != ph:
                    bad3 += 1
                # (S-4) the (2,6) coefficient
                c = C.coeff(bl, gs, (2, 6), w)
                mono = (cl(1, 3, x[1], x[3]) * cl(0, 7, x[0], y[3])
                        * cl(4, 5, y[0], y[1]))
                extra = (cl(0, 3, x[0], x[3]) * cl(1, 4, x[1], y[0])
                         * cl(5, 7, y[1], y[3]))
                if c != mono + extra:
                    bad4 += 1
    print("  (S-2) phi_formula      : %d/%d mismatches" % (bad2, tot))
    print("  (S-3) y6 decomposition : %d/%d mismatches" % (bad3, tot))
    print("  (S-4) c_(2,6) formula  : %d/%d mismatches" % (bad4, tot))
    OUT["S2_mismatch"], OUT["S3_mismatch"], OUT["S4_mismatch"] = \
        bad2, bad3, bad4
    OUT["S234_tests"] = tot
    # at m=25/26/27 the extra term is identically absent -> monomial
    for m in (25, 26, 27):
        gs = set(C.gamma_edges(C.TEMPLATES[m]))
        assert (5, 7) not in gs
    print("  (S-4) (5,7) absent at m=25/26/27  => c_(2,6) is a MONOMIAL")

    # ---- MUTATION controls on the asserted decomposition (S-3)
    muts = {}
    gam = C.gamma_edges(C.TEMPLATES[27])
    gs = set(gam)
    for name, sw in (("B<->C swapped", "BC"), ("A term dropped", "dropA"),
                     ("D term dropped", "dropD"), ("correct", "ok")):
        fails = t2 = 0
        for _ in range(3):
            bl = randbl(gam)
            for _k in range(30):
                w = tuple(RNG.randrange(3) for _ in range(8))
                x, y = w[:4], w[4:]
                A, B, Cc, D = C.phi_y6_parts(bl, 27, x, y[0], y[1], y[3])

                def cl(u, v, a, b):
                    e = (u, v) if u < v else (v, u)
                    return bl[e][a][b] if e in gs else Fraction(0)
                if sw == "BC":
                    B, Cc = Cc, B
                elif sw == "dropA":
                    A = Fraction(0)
                elif sw == "dropD":
                    D = Fraction(0)
                rec = (A * cl(3, 6, x[3], y[2]) + B * cl(6, 7, y[2], y[3])
                       + Cc * cl(5, 6, y[1], y[2]) + D * cl(4, 6, y[0], y[2]))
                t2 += 1
                fails += (rec != C.phi(bl, gs, w))
        muts[name] = "%d/%d" % (fails, t2)
        print("  MUTATION %-16s fails %d/%d  %s"
              % (name, fails, t2, "(want 0)" if sw == "ok" else "(want >0)"))
    OUT["S3_mutations"] = muts


def s5():
    print("=" * 72)
    print("(S-5) row-isolating L-words")
    rec = {}
    for m in (25, 26, 27, 28):
        T = C.TEMPLATES[m]
        sing = C.single_edges(T)
        lv = set(C.live_singles(m))
        grp = {}
        for x in product(range(3), repeat=4):
            can = tuple(sorted(e for e in lv if x[e[0]] == sing[e][0]))
            if not can:
                continue
            if len({e[0] for e in can}) != 1:
                continue
            grp.setdefault(can, []).append(x)
        rec["m%d" % m] = {"|".join(str(e) for e in k):
                          [list(x) for x in v] for k, v in grp.items()}
        print("  m=%d" % m)
        for k, v in sorted(grp.items()):
            print("     %-2d|%-30s  %d L-words  e.g. %s"
                  % (k[0][0], ",".join(str(e) for e in k), len(v), v[0]))
    OUT["S5"] = rec


def s6():
    print("=" * 72)
    print("(S-6) cross-engine controls vs w24_core / w21_core")
    import w24_core as C24                                        # noqa
    import w24_pts as P24                                         # noqa
    import w24_resid as R24                                       # noqa
    ok_t = all(C.TEMPLATES[m] == C24.TEMPLATES[m] for m in (24, 25, 26, 27, 28))
    print("  templates identical to w24_core:", ok_t)
    try:
        import w21_core as C21                                    # noqa
        w8 = getattr(C21, "W8_IMMUNE", None)
        ok21 = None
        if isinstance(w8, dict):
            ok21 = all(list(C.TEMPLATES[m]) == list(w8[m])
                       for m in w8 if m in C.TEMPLATES)
        print("  templates identical to w21_core.W8_IMMUNE:", ok21)
        OUT["S6_w21_templates"] = ok21
    except Exception as ex:                                        # noqa
        print("  w21_core import note:", type(ex).__name__, ex)
        OUT["S6_w21_templates"] = "n/a"
    OUT["S6_w24_templates"] = ok_t
    # clean sets and phi/coeff agreement
    badphi = badc = badclean = 0
    for m in (25, 26, 27, 28):
        gam = C.gamma_edges(C.TEMPLATES[m])
        gs = set(gam)
        if set(P24.w21_clean(m)) != set(C.clean_words(m)):
            badclean += 1
        for _ in range(2):
            bl = randbl(gam)
            for _k in range(60):
                w = tuple(RNG.randrange(3) for _ in range(8))
                if C.phi(bl, gs, w) != C24.phi(bl, gs, w):
                    badphi += 1
                for e in C.live_singles(m)[:3]:
                    import w24_ident as ID24                        # noqa
                    if C.coeff(bl, gs, e, w) != ID24.coeff(bl, gs, e, w):
                        badc += 1
    print("  clean-set disagreements per m: %d/4" % badclean)
    print("  phi disagreements: %d ; coeff disagreements: %d"
          % (badphi, badc))
    OUT["S6_clean_disagree"] = badclean
    OUT["S6_phi_disagree"] = badphi
    OUT["S6_coeff_disagree"] = badc
    # verdict agreement on stored points
    pts = P24.stored_points()
    agree = tot = 0
    for m, tag, bl in pts:
        v26 = C.verdict(m, bl)
        v24 = R24.verdict(m, bl)
        tot += 1
        agree += (v26["killed"] == v24["killed"])
    print("  stored points: %d ; verdict agreement %d/%d" % (len(pts),
                                                             agree, tot))
    OUT["S6_stored_points"] = tot
    OUT["S6_verdict_agree"] = agree
    # H_word consistency: build z from the residual solution on a killed pt
    print("  (H_word definition sanity)")
    m = 27
    gam = C.gamma_edges(C.TEMPLATES[m])
    bl = randbl(gam)
    z = {e: Fraction(RNG.randint(1, 5)) for e in C.single_edges(C.TEMPLATES[m])}
    w = (0, 1, 2, 0, 1, 2, 0, 1)
    direct = C.H_word(bl, C.TEMPLATES[m], z, w)
    gs = set(gam)
    lin = C.phi(bl, gs, w)
    for e in C.active_live(m, w):
        lin += z[e] * C.coeff(bl, gs, e, w)
    print("     H_word=%s  vs  Phi+sum c_e z_e=%s  (deg<=1 word)"
          % (direct, lin))
    OUT["S6_Hword_check"] = (str(direct), str(lin))


def main():
    s1()
    s2_s3_s4()
    s5()
    s6()
    json.dump(OUT, open(os.path.join(HERE, "results_struct.json"), "w"),
              indent=1, default=str)
    print("=" * 72)
    print("wrote results_struct.json")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""W26 ADVERSARIAL LANE -- OBJECT (ii): a constant-nonzero-ratio point at
m=26 / m=27 whose (2,6)-solo family SURVIVES, OFF the identically-
vanishing stratum.  UNAUDITED probe.  EXACT ONLY.

DERIVATION (machine-verified below; nothing taken on faith).
Write x=(x0..x3), y=(y4..y7).  With Gamma at m=26 (resp. 27):
  Phi = A67[y6][y7]*P + A56[y5][y6]*Q + A36[x3][y6]*Aa (+ A46[y4][y6]*Dd)
  P  = hafL*A45 + A03*A14*A25      Q  = hafL*A47 + A23*A07*A14
  Aa = A01*A47*A25 + A12*A45*A07 + A07*A14*A25
  Dd = hafL*A57 + A13*A07*A25  =  A13*A07*A25   (A57 absent at m<=27)
Take every Gamma block rank one in the "tensor" pattern
  A01=tau(x)B  A02=tau(x)Cc  A03=tau(x)g  A07=tau(x)v  A12=mvec(x)sigma
  A13=h(x)g    A14=rho(x)a   A23=eps(x)g  A25=sigma(x)u
  A45=alpha a(x)u   A47=beta a(x)v
  A56=u(x)(mu,cp,1) A67=(mu,cp+c,1)(x)v  A36=g(x)(mu*phi, cp*phi-c, phi)
  A46=a(x)(mu*d0, cp*d0, d0)   [m=27 only]
Then, with  Lam = B*eps + Cc*h + mvec*sigma  (a function of (x1,x2)),
  hafL     = tau[x0] g[x3] Lam(x1,x2)
  P        = a u tau g * Om,   Om  = alpha*Lam + rho*sigma
  Q        = a v tau g * Ps,   Ps  = beta*Lam  + eps*rho
  Aa       = a u v tau sigma * Xi, Xi = beta*B + alpha*mvec + rho
  Dd       = h g tau v sigma u
  Phi(w)   = a[y4]u[y5]v[y7]tau[x0]g[x3] * K_{y6}(x1,x2)
  K_0 = mu*K_2 ;  K_2 = Om+Ps+sigma(phi*Xi + d0*h) ;
  K_1 = cp*K_2 + c*(Om - sigma*Xi)          (d46 chosen with d46_1=cp*d0)
So: K_2 = 0 identically  =>  Phi = 0 at EVERY word with y6 in {0,2};
    K_1 = 0 for x1!=1, x2!=2  =>  Phi = 0 at every CLEAN word (the only
      clean words with y6=1 have x1!=1 and x2!=2, singles (1,6),(2,6));
    K_1 = -kappa'*h[x1] for x2=2 =>  on the whole (2,6)-solo family
      -Phi/c_(2,6) = c*kappa'/alpha =: kappa, ONE NONZERO CONSTANT,
      because c_(2,6) = A13[x1][x3]A07[x0][y7]A45[y4][y5]
                      = h g tau v alpha a u   is the same monomial.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(HERE)
sys.path.insert(0, UP)
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402
import w26_pts as PT                                             # noqa: E402
import w26_sub as SB                                             # noqa: E402
import adv_lib as AL                                             # noqa: E402
import adv_ansatz as AA                                          # noqa: E402

F = Fraction
OUT = {"_header": "UNAUDITED W26 adversarial lane -- object (ii) "
                  "(2,6)-solo survivor at m=26/27."}
RAN = []


def solve_params(free, m=26):
    """turn the free parameters into the full SOLO26/27 parameter dict.
    Returns (params, kappa_expected) or raises ValueError if degenerate."""
    al, be = free["alpha"], free["beta"]
    th, nu, kp, ph = free["theta"], free["nu"], free["kprime"], free["phi"]
    mu, cp, c = free["mu"], free["cp"], free["c"]
    sg, h, tau, g = free["sigma"], free["h"], free["tau"], free["g"]
    v, u, a, B1 = free["v"], free["u"], free["a"], free["B1"]
    eps2 = free["eps2"]
    d0 = free.get("d46_0", 0) if m == 27 else 0
    s = al + be
    if s == 0 or al == 0 or be == 0:
        raise ValueError("alpha/beta degenerate")
    if s + ph * al == 0:
        raise ValueError("s + phi*alpha = 0")
    eps = [nu * sg[0], nu * sg[1], eps2]
    Dl = eps2 - nu * sg[2]
    if Dl == 0:
        raise ValueError("Delta = 0")
    Cc = [th * (eps[j] - be * sg[j] / al) for j in range(2)]
    Cc.append(th * (eps2 - be * sg[2] / al) - kp / al)
    B = [-th * h[0], B1, -th * h[2]]
    psi = th - kp / (al * Dl)
    rho = [-s * (B[i] + psi * h[i]) for i in range(3)]
    Zreq = [s * h[i] * (th * be - nu * kp / Dl) / al for i in range(3)]
    mvec = [(Zreq[i] - d0 * h[i] - rho[i] * (1 + ph) - ph * be * B[i])
            / (s + ph * al) for i in range(3)]
    P = dict(tau=tau, B=B, Cc=Cc, g=g, v=v, mvec=mvec, sigma=sg, h=h,
             rho=rho, a=a, eps=eps, u=u, mu=mu, cp=cp, c=c, phi=ph,
             alpha=al, beta=be)
    if m == 27:
        P["d46"] = [d0, cp * d0]
    kappa = c * kp / al
    return P, kappa


def build(free, m=26):
    P, kappa = solve_params(free, m)
    bl = AA.solo26(P, m=m)
    return bl, kappa, P


def default_free(m=26):
    fr = dict(alpha=F(1), beta=F(1), theta=F(1), nu=F(2), kprime=F(1),
              phi=F(1), mu=F(1), cp=F(1), c=F(2), eps2=F(1),
              sigma=[F(1), F(2), F(3)], h=[F(1), F(2), F(3)],
              tau=[F(1), F(2), F(3)], g=[F(1), F(2), F(3)],
              v=[F(1), F(2), F(3)], u=[F(1), F(2), F(3)],
              a=[F(1), F(2), F(3)], B1=F(1))
    if m == 27:
        fr["d46_0"] = F(1)
    return fr


def full_report(tag, m, bl, kappa):
    rec = {"tag": tag, "m": m, "kappa_predicted": str(kappa)}
    rec["all_cells_nonzero"] = AL.all_nonzero(bl)
    rec["is_clean_point"] = PT.is_clean_point(m, bl)
    rec["vanishing_stratum"] = PT.vanishing_stratum(m, bl)
    print("  %-22s cells!=0=%s clean=%s van=%s"
          % (tag, rec["all_cells_nonzero"], rec["is_clean_point"],
             rec["vanishing_stratum"]))
    sr = {}
    for e in C.live_singles(m):
        r = SB.solo_report(m, bl, e)
        sr[str(e)] = r
    rec["solo"] = sr
    rec["solo_survives"] = [k for k, r in sr.items() if r["survives"]]
    rec["solo_killed"] = {k: r["killed"] for k, r in sr.items()}
    print("     solo families SURVIVING: %s" % rec["solo_survives"])
    for k, r in sorted(sr.items()):
        print("       %-8s n_solo=%3d pure=%3d badconst=%3d "
              "distinct_ratios=%d survives=%s ratios=%s"
              % (k, r["n_solo"], r["n_pure"], r["n_badconst"],
                 r["n_distinct_ratios"], r["survives"], r["ratios"][:3]))
    # independent raw-definition verification
    print("  --- independent re-verification from C.H_word (105 matchings)")
    raw, phis = AL.independent_verify(m, bl)
    rec["raw"] = raw
    bad, badc, ncmp = AL.cross_check_helpers(m, bl)
    print("  [cross-check] C.phi vs H_word over 6561 words: %d mismatches"
          % bad)
    print("  [cross-check] C.coeff vs H_word over %d active pairs: %d "
          "mismatches" % (ncmp, badc))
    rec["helper_mismatch"] = [bad, badc, ncmp]
    # the (2,6) ratio recomputed ENTIRELY from H_word
    T = C.TEMPLATES[m]
    z0 = {e: F(0) for e in C.single_edges(T)}
    z1 = dict(z0)
    z1[(2, 6)] = F(1)
    rats = set()
    ncz = 0
    for w in SB.solo_words(m, (2, 6)):
        h0 = C.H_word(bl, T, z0, w)
        h1 = C.H_word(bl, T, z1, w)
        ce = h1 - h0
        if ce == 0:
            ncz += 1
            continue
        rats.add(-h0 / ce)
    print("  [H_word raw] (2,6)-solo family: %d words, c_e=0 at %d, "
          "distinct -Phi/c_e ratios: %s"
          % (len(SB.solo_words(m, (2, 6))), ncz,
             sorted(str(r) for r in rats)))
    rec["raw_26_ratios"] = sorted(str(r) for r in rats)
    rec["raw_26_c_zero"] = ncz
    # z_(2,6) = kappa actually zeroes H on the whole solo family
    if len(rats) == 1:
        kk = list(rats)[0]
        zk = dict(z0)
        zk[(2, 6)] = kk
        nbad = sum(1 for w in SB.solo_words(m, (2, 6))
                   if C.H_word(bl, T, zk, w) != 0)
        print("  [H_word raw] setting z_(2,6)=%s kills H_w on %d/%d solo "
              "words (bad: %d)" % (kk, len(SB.solo_words(m, (2, 6))) - nbad,
                                   len(SB.solo_words(m, (2, 6))), nbad))
        rec["raw_z26_zeroes_solo_bad"] = nbad
        rec["kappa_observed"] = str(kk)
    v = C.verdict(m, bl)
    rec["full_verdict"] = dict(v)
    subs = SB.all_sub_verdicts(m, bl)
    rec["subs"] = {k: (None if s is None else s["killed"])
                   for k, s in subs.items()}
    print("  full residual verdict: killed=%s inconsistent=%s forced=%s"
          % (v["killed"], v["inconsistent"], v.get("forced_zero")))
    print("  six sub-systems killed?:", rec["subs"])
    rec["n_pure_rows"] = len(C.pure_rows(m, bl))
    rec["point"] = AL.dump_point(bl)
    return rec


def main():
    for m in (26, 27):
        print("=" * 78)
        print("OBJECT (ii)  m=%d  SOLO26 tensor ansatz" % m)
        print("=" * 78)
        RAN.append("solo_default_m%d" % m)
        bl, kappa, P = build(default_free(m), m)
        rec = full_report("SOLO%d default" % m, m, bl, kappa)
        OUT["m%d" % m] = rec
        assert rec["is_clean_point"], "m=%d point not clean" % m
        assert not rec["vanishing_stratum"], "m=%d point on stratum" % m

    # ---------------------------------------------------------- controls
    print()
    print("=" * 78)
    print("CONTROLS")
    print("=" * 78)
    ctl = {}

    # (C-a) MUTATION control
    RAN.append("mutation")
    bl26, k26, _ = build(default_free(26), 26)
    nmut = nbroke = 0
    free_cells = []
    for e in sorted(bl26):
        for i in range(3):
            for j in range(3):
                nb = AL.mutate(bl26, e, i, j, F(1))
                nmut += 1
                if not PT.is_clean_point(26, nb):
                    nbroke += 1
                else:
                    free_cells.append("%s[%d][%d]" % (str(e), i, j))
    print("(C-a) mutation: %d/%d single-cell +1 perturbations destroy "
          "cleanliness; survivors: %s" % (nbroke, nmut, free_cells))
    ctl["mutation"] = dict(broke=nbroke, total=nmut, free=free_cells)
    # a mutation that keeps cleanliness must still be checked for the
    # SOLO property -- the target is the pair (clean, solo survives)
    nsolo_broke = 0
    for e in sorted(bl26):
        for i in range(3):
            for j in range(3):
                nb = AL.mutate(bl26, e, i, j, F(1))
                if PT.is_clean_point(26, nb):
                    if not SB.solo_report(26, nb, (2, 6))["survives"]:
                        nsolo_broke += 1
    print("     of the still-clean perturbations, %d also destroy the "
          "(2,6)-solo survival" % nsolo_broke)
    ctl["mutation_solo_broke"] = nsolo_broke

    # (C-b) POSITIVE control: plant a stratum point in the same family
    RAN.append("positive_vanishing")
    # c = 0 makes K_1 = cp*K_2 = 0 as well, so Phi vanishes at ALL 6561
    # words while every Gamma cell stays nonzero: a planted stratum point.
    # (kappa' = 0 instead would zero rho and hence the block A14.)
    fr = default_free(26)
    fr["c"] = F(0)
    blv, kv, _ = build(fr, 26)
    okv = PT.is_clean_point(26, blv)
    vanv = PT.vanishing_stratum(26, blv)
    rawv, _ = AL.independent_verify(26, blv, verbose=False)
    srv = SB.solo_report(26, blv, (2, 6))
    print("(C-b) positive control c=0: all_cells_nonzero=%s clean=%s "
          "stratum=%s (raw-def %s) (2,6)-solo survives=%s (must be False: "
          "the ratio is 0)" % (AL.all_nonzero(blv), okv, vanv,
                               rawv["identically_vanishing_rawdef"],
                               srv["survives"]))
    ctl["positive_vanishing"] = dict(clean=okv, stratum=vanv, raw=rawv,
                                     cells=AL.all_nonzero(blv),
                                     solo26=srv)
    assert AL.all_nonzero(blv), "planted point must have all cells nonzero"
    assert okv and vanv, "c=0 must be a clean point ON the stratum"
    assert rawv["identically_vanishing_rawdef"], "raw-def stratum flag"
    # also plant a point where the ratio is a DIFFERENT nonzero constant,
    # to show kappa really tracks the parameters
    for kp in (F(3), F(-1, 2)):
        fr2 = default_free(26)
        fr2["kprime"] = kp
        b2, k2, _ = build(fr2, 26)
        r2 = SB.solo_report(26, b2, (2, 6))
        print("     kappa'=%s -> predicted kappa=%s ; observed ratios=%s "
              "clean=%s" % (kp, k2, r2["ratios"], PT.is_clean_point(26, b2)))
        assert r2["ratios"] == [str(k2)], "kappa mismatch"

    # (C-c) non-vacuity of solo_report's 'survives' flag (ledger 18):
    #       exhibit a NON-clean point whose (2,6)-solo family survives, and
    #       a clean point whose (2,6)-solo family does NOT survive.
    RAN.append("solo_predicate_nonvacuous")
    rng = random.Random(20260816)
    gam = C.gamma_edges(C.TEMPLATES[26])
    junk = {e: [[F(rng.randint(1, 9)) for _ in range(3)] for _ in range(3)]
            for e in gam}
    r_junk = SB.solo_report(26, junk, (2, 6))
    print("(C-c) random non-clean point: clean=%s (2,6)-solo survives=%s "
          "(distinct ratios %d)" % (PT.is_clean_point(26, junk),
                                    r_junk["survives"],
                                    r_junk["n_distinct_ratios"]))
    # a clean point from the repo's own descent, for contrast
    fresh = PT.fresh_points(26, 1, seed0=4242, passes=4)
    if fresh:
        rf = SB.solo_report(26, fresh[0], (2, 6))
        print("     independent-descent clean point: clean=%s van=%s "
              "(2,6)-solo survives=%s (pure=%d badconst=%d ratios=%d)"
              % (PT.is_clean_point(26, fresh[0]),
                 PT.vanishing_stratum(26, fresh[0]), rf["survives"],
                 rf["n_pure"], rf["n_badconst"], rf["n_distinct_ratios"]))
        ctl["descent_clean_point_solo"] = rf
    ctl["random_point_solo"] = r_junk

    # (C-d) family sweep over random parameters
    RAN.append("family_sweep")
    print("(C-d) family sweep over random SOLO26/27 parameters")
    sweep = {}
    for m in (26, 27):
        nok = nsurv = ntry = nvan = 0
        surv_sets = {}
        for s in range(120):
            r2 = random.Random(900000 + 7 * s + m)

            def rv_():
                return F(r2.randint(-6, 6) or 2, r2.randint(1, 3))
            fr2 = dict(alpha=rv_(), beta=rv_(), theta=rv_(), nu=rv_(),
                       kprime=rv_(), phi=rv_(), mu=rv_(), cp=rv_(),
                       c=rv_(), eps2=rv_(),
                       sigma=[rv_() for _ in range(3)],
                       h=[rv_() for _ in range(3)],
                       tau=[rv_() for _ in range(3)],
                       g=[rv_() for _ in range(3)],
                       v=[rv_() for _ in range(3)],
                       u=[rv_() for _ in range(3)],
                       a=[rv_() for _ in range(3)], B1=rv_())
            if m == 27:
                fr2["d46_0"] = rv_()
            try:
                b2, k2, _ = build(fr2, m)
            except (ValueError, ZeroDivisionError, AssertionError):
                continue
            if not AL.all_nonzero(b2):
                continue
            ntry += 1
            if not PT.is_clean_point(m, b2):
                continue
            nok += 1
            if PT.vanishing_stratum(m, b2):
                nvan += 1
            ss = tuple(str(e) for e in C.live_singles(m)
                       if SB.solo_report(m, b2, e)["survives"])
            surv_sets[ss] = surv_sets.get(ss, 0) + 1
            if "(2, 6)" in ss:
                nsurv += 1
        print("   m=%d : %d admissible draws, %d clean (%d on stratum), "
              "%d with (2,6)-solo surviving" % (m, ntry, nok, nvan, nsurv))
        print("        survivor-set histogram: %s"
              % {str(k): v for k, v in sorted(surv_sets.items(),
                                              key=lambda t: -t[1])[:6]})
        sweep["m%d" % m] = dict(n_admissible=ntry, n_clean=nok,
                                n_stratum=nvan, n_26_survive=nsurv,
                                hist={str(k): v for k, v in
                                      surv_sets.items()})
    ctl["family_sweep"] = sweep

    # (C-e) extension fields
    RAN.append("extension_fields")
    print("(C-e) the same family over Q(omega) and Q(i)")
    ext = {}
    for nm, Ring in (("Q(omega)", AL.Q2), ("Q(i)", AL.Qi)):
        def R(z):
            return Ring(z, 0)
        w1 = Ring(0, 1)
        fr3 = dict(alpha=R(1), beta=R(1), theta=R(1), nu=R(2) + w1,
                   kprime=R(1), phi=R(1), mu=w1, cp=R(1), c=R(2),
                   eps2=R(1), sigma=[R(1), R(2), R(3)],
                   h=[R(1), w1, R(3)], tau=[R(1), R(2), w1],
                   g=[R(1), R(2), R(3)], v=[R(1), w1, R(3)],
                   u=[R(1), R(2), R(3)], a=[R(1), R(2), R(3)], B1=R(1))
        try:
            P3, k3 = solve_params(fr3, 26)
            b3 = AA.solo26(P3, m=26)
            okc = AL.is_clean_g(26, b3)
            nz = AL.all_nonzero(b3)
            van = AL.vanishing_g(26, b3)
            sr = AL.solo_report_g(26, b3, (2, 6))
            print("     %-9s cells!=0=%s clean=%s van=%s (2,6)survives=%s "
                  "ratios=%s" % (nm, nz, okc, van, sr["survives"],
                                 sr["ratios"][:2]))
            ext[nm] = dict(cells=nz, clean=okc, van=van,
                           survives=sr["survives"], ratios=sr["ratios"],
                           kappa=str(k3))
        except Exception as ex:                                    # noqa
            print("     %-9s degenerate: %s %s" % (nm, type(ex).__name__, ex))
            ext[nm] = "degenerate %s" % ex
    ctl["extension_fields"] = ext

    OUT["controls"] = ctl
    declared = ["solo_default_m26", "solo_default_m27", "mutation",
                "positive_vanishing", "solo_predicate_nonvacuous",
                "family_sweep", "extension_fields"]
    missing = [d for d in declared if d not in RAN]
    print()
    print("CONTROL MANIFEST: declared=%s ran=%s" % (declared, RAN))
    assert not missing, "CONTROL DID NOT RUN: %s" % missing
    OUT["control_manifest"] = dict(declared=declared, ran=RAN)
    json.dump(OUT, open(os.path.join(HERE, "results_solo.json"), "w"),
              indent=1, default=str)
    print("wrote results_solo.json")


if __name__ == "__main__":
    main()

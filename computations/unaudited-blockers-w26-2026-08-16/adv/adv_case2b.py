#!/usr/bin/env python3
"""W26 ADVERSARIAL LANE -- OBJECT (i): a Case-2b clean point at m=25.
UNAUDITED probe.  EXACT ONLY.

Target: clean point at m=25 (all 117 Gamma cells nonzero, Phi=0 on all
2624 clean words) with SB.case2b(25,bl) == (True, 9, 0), preferably OFF
the identically-vanishing stratum.
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
OUT = {"_header": "UNAUDITED W26 adversarial lane -- object (i) m=25 "
                  "Case-2b clean point."}
RAN = []


def check(tag, bl, want_c2b=True, verbose=True):
    """full battery on one candidate point."""
    rec = {"tag": tag}
    rec["all_cells_nonzero"] = AL.all_nonzero(bl)
    rec["is_clean_point"] = PT.is_clean_point(25, bl)
    c2b, n02, n01 = SB.case2b(25, bl)
    rec["case2b"] = c2b
    rec["n_par02"] = n02
    rec["n_par01"] = n01
    rec["case2b_structure"] = str(SB.case2b_structure(bl))
    rec["vanishing_stratum"] = PT.vanishing_stratum(25, bl)
    if verbose:
        print("  %-26s cells!=0=%s clean=%s case2b=%s (par02=%d par01=%d) "
              "van=%s" % (tag, rec["all_cells_nonzero"], rec["is_clean_point"],
                          c2b, n02, n01, rec["vanishing_stratum"]))
    return rec


def full_report(tag, bl):
    rec = check(tag, bl)
    gs = set(C.gamma_edges(C.TEMPLATES[25]))
    # independent raw-definition verification
    print("  --- independent re-verification from C.H_word (105 matchings)")
    raw, phis = AL.independent_verify(25, bl)
    rec["raw"] = raw
    bad, badc, ncmp = AL.cross_check_helpers(25, bl)
    print("  [cross-check] C.phi vs H_word mismatches over 6561 words: %d"
          % bad)
    print("  [cross-check] C.coeff vs H_word mismatches over %d "
          "active(e,w) pairs: %d" % (ncmp, badc))
    rec["helper_phi_mismatch"] = bad
    rec["helper_coeff_mismatch"] = [badc, ncmp]
    # where is Phi nonzero?
    nz = [w for w in C.WORDS if phis[w] != 0]
    rec["n_words_Phi_nonzero"] = len(nz)
    if nz:
        pat = {}
        for w in nz:
            pat.setdefault((w[6],), 0)
            pat[(w[6],)] += 1
        rec["Phi_nonzero_by_y6"] = {str(k): v for k, v in sorted(pat.items())}
        print("  Phi != 0 at %d/6561 words; by y6 letter: %s"
              % (len(nz), rec["Phi_nonzero_by_y6"]))
        print("  example word with Phi!=0 :", list(nz[0]), "Phi =",
              str(phis[nz[0]]))
        rec["example_nonzero_word"] = [list(nz[0]), str(phis[nz[0]])]
    # downstream verdicts (informational -- not part of the target)
    v = C.verdict(25, bl)
    rec["full_verdict"] = {k: (v[k] if not isinstance(v[k], list)
                               else v[k]) for k in v}
    subs = SB.all_sub_verdicts(25, bl)
    rec["subs"] = {k: (None if s is None else s["killed"])
                   for k, s in subs.items()}
    rec["subs_detail"] = {k: (None if s is None else
                              {kk: s[kk] for kk in s}) for k, s in subs.items()}
    solo = {str(e): SB.solo_report(25, bl, e) for e in C.live_singles(25)}
    rec["solo_killed"] = {k: s["killed"] for k, s in solo.items()}
    rec["solo_survives"] = [k for k, s in solo.items() if s["survives"]]
    rec["solo_detail"] = solo
    print("  full residual verdict: killed=%s inconsistent=%s forced=%s"
          % (v["killed"], v["inconsistent"], v.get("forced_zero")))
    print("  six sub-systems killed?:", rec["subs"])
    print("  solo families surviving:", rec["solo_survives"])
    rec["point"] = AL.dump_point(bl)
    return rec


def main():
    print("=" * 78)
    print("OBJECT (i)  m=25 Case-2b clean point -- SPLIT25 ansatz")
    print("=" * 78)
    RAN.append("split25_default")
    Pm = AA.split25_params()
    bl = AA.split25(Pm)
    rec = full_report("SPLIT25 default", bl)
    OUT["main"] = rec

    # ---------------------------------------------------------- controls
    print()
    print("=" * 78)
    print("CONTROLS")
    print("=" * 78)
    ctl = {}

    # (C-a) MUTATION control: perturb one cell -> must stop being clean
    RAN.append("mutation")
    print("(C-a) mutation control: perturb one cell of the claimed point")
    nmut = nbroke = 0
    survive_cells = []
    for e in sorted(bl):
        for i in range(3):
            for j in range(3):
                nb = AL.mutate(bl, e, i, j, F(1))
                nmut += 1
                if not PT.is_clean_point(25, nb):
                    nbroke += 1
                else:
                    survive_cells.append("%s[%d][%d]" % (str(e), i, j))
    print("     %d/%d single-cell +1 perturbations destroy cleanliness"
          % (nbroke, nmut))
    print("     cells whose perturbation KEEPS cleanliness (= the free "
          "directions of the ansatz): %s" % survive_cells)
    ctl["mutation_broke"] = [nbroke, nmut]
    ctl["mutation_free_cells"] = survive_cells
    # the free cells must be exactly the ansatz's free parameters
    expect_free = set()
    for x0 in range(3):
        expect_free.add("(0, 1)[%d][1]" % x0)
        expect_free.add("(0, 2)[%d][2]" % x0)
    for x2 in range(3):
        expect_free.add("(1, 2)[1][%d]" % x2)
    for x1 in (0, 2):
        expect_free.add("(1, 2)[%d][2]" % x1)
    for j in range(3):
        expect_free.add("(1, 3)[1][%d]" % j)
        expect_free.add("(1, 4)[1][%d]" % j)
        expect_free.add("(5, 6)[%d][1]" % j)
        expect_free.add("(6, 7)[1][%d]" % j)
    print("     predicted free set == observed free set: %s"
          % (set(survive_cells) == expect_free))
    ctl["mutation_free_matches_prediction"] = (set(survive_cells)
                                               == expect_free)
    ctl["mutation_free_predicted_only"] = sorted(expect_free
                                                 - set(survive_cells))
    ctl["mutation_free_observed_only"] = sorted(set(survive_cells)
                                                - expect_free)
    # a CONSTRAINED cell must break cleanliness for many deltas, not just +1
    nb2 = 0
    for d in (F(1), F(-1), F(1, 7), F(5), F(-3, 2)):
        if not PT.is_clean_point(25, AL.mutate(bl, (0, 3), 1, 1, d)):
            nb2 += 1
    print("     constrained cell (0,3)[1][1]: %d/5 deltas break cleanliness"
          % nb2)
    ctl["mutation_constrained_cell"] = nb2

    # (C-b) POSITIVE control: a point ON the identically-vanishing stratum
    RAN.append("positive_vanishing")
    print("(C-b) positive control: plant a point ON the identically-"
          "vanishing stratum and confirm the machinery flags it")
    Pv = AA.split25_params(p=[F(3), F(6), F(9)], q=[F(3), F(9), F(15)])
    # p = 3u and q = 3v  =>  u[y5]q[y7]-v[y7]p[y5] = 0 identically
    blv = AA.split25(Pv)
    rv = check("SPLIT25 p=3u,q=3v", blv)
    rawv, _ = AL.independent_verify(25, blv)
    rv["raw"] = rawv
    ctl["positive_vanishing"] = rv
    assert rv["is_clean_point"], "planted point must be clean"
    assert rv["vanishing_stratum"], "planted point must be on the stratum"
    assert rawv["identically_vanishing_rawdef"], "raw-def stratum flag"
    print("     planted stratum point: clean=%s stratum=%s (raw-def %s) "
          "case2b=%s" % (rv["is_clean_point"], rv["vanishing_stratum"],
                         rawv["identically_vanishing_rawdef"], rv["case2b"]))

    # (C-c) EXPLICIT POINT OUTSIDE THE ASSERTED LOCUS (ledger 18):
    #       a point that is NOT clean but DOES satisfy the Case-2b predicate,
    #       proving the predicate test is not vacuously false.
    RAN.append("predicate_nonvacuous")
    print("(C-c) non-vacuity of the Case-2b predicate: a NON-clean point "
          "that satisfies it")
    rng = random.Random(20260816)
    gam = C.gamma_edges(C.TEMPLATES[25])
    junk = {e: [[F(rng.randint(1, 9)) for _ in range(3)] for _ in range(3)]
            for e in gam}
    uu = [F(1), F(2), F(5)]
    vv = [F(3), F(1), F(7)]
    # col0 = 2 col2 and row0 = 2 row2  (mu = 2)  ->  v0 || v2 at all nine;
    # col1 = u and row1 = 2v  ->  ratio sets {1} vs {2} disjoint -> no
    # (y5,y7) has v1 || v0.
    junk[(5, 6)] = [[F(2) * uu[i], uu[i], uu[i]] for i in range(3)]
    junk[(6, 7)] = [[F(2) * vv[j] for j in range(3)],
                    [F(2) * vv[j] for j in range(3)],
                    [vv[j] for j in range(3)]]
    rj = check("random blocks + case2b (5,6),(6,7)", junk)
    ctl["predicate_nonvacuous"] = rj
    assert rj["case2b"], "control point must satisfy the Case-2b predicate"
    assert not rj["is_clean_point"], "control point must NOT be clean"

    # (C-d) equivalence of the closed form and the nine-parallelism test
    RAN.append("case2b_closed_form")
    print("(C-d) equivalence: 'v0||v2 at all nine' <=> col0(A56)=mu col2 and "
          "row0(A67)=mu row2")
    nbad = ntest = 0
    for _ in range(4000):
        U = [[F(rng.randint(-4, 4) or 1) for _ in range(3)] for _ in range(3)]
        V = [[F(rng.randint(-4, 4) or 1) for _ in range(3)] for _ in range(3)]
        tb = {(5, 6): U, (6, 7): V}
        n02 = sum(1 for y5 in range(3) for y7 in range(3)
                  if U[y5][0] * V[2][y7] - U[y5][2] * V[0][y7] == 0)
        cf = SB.case2b_structure(tb)
        lhs = (n02 == 9)
        rhs = (cf is not None and cf[0])
        ntest += 1
        if lhs != rhs:
            nbad += 1
    print("     mismatches over %d random (A56,A67) with all cells nonzero: "
          "%d" % (ntest, nbad))
    ctl["closed_form_mismatch"] = [nbad, ntest]

    # (C-e) parameter sweep: many DIFFERENT Case-2b clean points
    RAN.append("family_sweep")
    print("(C-e) family sweep: random parameters in the SPLIT25 ansatz")
    nok = nvan = ntry = 0
    fails = []
    deep = []
    for s in range(200):
        r2 = random.Random(700000 + s)

        def rv_():
            return F(r2.randint(-7, 7) or 3, r2.randint(1, 3))
        Pm2 = AA.split25_params(
            u=[rv_() for _ in range(3)], v=[rv_() for _ in range(3)],
            p=[rv_() for _ in range(3)], q=[rv_() for _ in range(3)],
            a=[rv_() for _ in range(3)], tau=[rv_() for _ in range(3)],
            sigma=[rv_() for _ in range(3)], g=[rv_() for _ in range(3)],
            mu=rv_(), alpha=rv_(),
            rho={0: rv_(), 2: rv_()}, r1=[rv_() for _ in range(3)],
            h={0: rv_(), 2: rv_()}, A13row1=[rv_() for _ in range(3)],
            k=[F(0), rv_(), rv_()], B0={0: rv_(), 2: rv_()},
            C0={0: rv_(), 1: rv_()},
            A01col1=[rv_() for _ in range(3)],
            A02col2=[rv_() for _ in range(3)],
            A12row1=[rv_() for _ in range(3)],
            A12col2={0: rv_(), 2: rv_()})
        try:
            b2 = AA.split25(Pm2)
        except (ZeroDivisionError, AssertionError):
            continue
        if not AL.all_nonzero(b2):
            continue
        ntry += 1
        cl = PT.is_clean_point(25, b2)
        c2, a2, b2n = SB.case2b(25, b2)
        van = PT.vanishing_stratum(25, b2)
        if cl and c2:
            nok += 1
            if van:
                nvan += 1
            if nok <= 25:
                vv2 = C.verdict(25, b2)
                sv = [str(e) for e in C.live_singles(25)
                      if SB.solo_report(25, b2, e)["survives"]]
                sub2 = SB.all_sub_verdicts(25, b2)
                deep.append(dict(seed=s, van=van, killed=vv2["killed"],
                                 inconsistent=vv2["inconsistent"],
                                 forced=vv2["forced_zero"],
                                 subs_all_kill=all(x["killed"]
                                                   for x in sub2.values()
                                                   if x is not None),
                                 solo_surv=sv))
        else:
            fails.append((s, cl, c2, a2, b2n))
    print("     %d admissible parameter draws: %d are Case-2b clean points, "
          "%d of those on the vanishing stratum" % (ntry, nok, nvan))
    if fails[:5]:
        print("     non-hits (seed, clean, case2b, par02, par01):", fails[:5])
    nk = sum(1 for d in deep if not d["killed"])
    nallsub = sum(1 for d in deep if not d["subs_all_kill"])
    print("     of the first %d hits: %d have full residual verdict "
          "NOT killed; %d have some sub-system not killing; solo survivors "
          "seen: %s" % (len(deep), nk, nallsub,
                        sorted({e for d in deep for e in d["solo_surv"]})))
    ctl["family_sweep"] = dict(n_admissible=ntry, n_case2b_clean=nok,
                               n_on_stratum=nvan, deep=deep,
                               first_failures=[list(map(str, f))
                                               for f in fails[:5]])

    # (C-f) the same ansatz over the extensions Q(omega) and Q(i)
    #       (repo ledger 19: never conclude from Q or F_p alone)
    RAN.append("extension_fields")
    print("(C-f) instantiate the ansatz over Q(omega)=Q[t]/(t^2+t+1) and "
          "Q(i)=Q[t]/(t^2+1)")
    ext = {}
    for nm, Ring in (("Q(omega)", AL.Q2), ("Q(i)", AL.Qi)):
        w1 = Ring(0, 1)              # omega  resp.  i
        Pe = AA.split25_params(ring=lambda z: Ring(z, 0))
        Pe["u"] = [Ring(1, 0), Ring(0, 1), Ring(1, 1)]
        Pe["v"] = [Ring(1, 0), Ring(2, 1), Ring(1, 2)]
        Pe["p"] = [Ring(1, 0) * x for x in Pe["u"]]      # ratio 1
        Pe["q"] = [w1 * x for x in Pe["v"]]              # ratio omega resp i
        Pe["mu"] = Ring(1, 1)
        Pe["a"] = [Ring(1, 0), Ring(1, 1), Ring(0, 1)]
        be = AA.split25(Pe)
        okc = AL.is_clean_g(25, be)
        c2e = AL.case2b_g(25, be)
        vane = AL.vanishing_g(25, be)
        print("     %-9s clean=%s case2b=%s van=%s"
              % (nm, okc, c2e, vane))
        ext[nm] = dict(clean=okc, case2b=list(map(str, c2e)),
                       vanishing=vane,
                       point={str(e): [[str(x) for x in r] for r in be[e]]
                              for e in sorted(be)})
    ctl["extension_fields"] = ext

    OUT["controls"] = ctl

    # -------------------------------------------------- manifest assertion
    declared = ["split25_default", "mutation", "positive_vanishing",
                "predicate_nonvacuous", "case2b_closed_form", "family_sweep",
                "extension_fields"]
    missing = [d for d in declared if d not in RAN]
    print()
    print("CONTROL MANIFEST: declared=%s ran=%s" % (declared, RAN))
    assert not missing, "CONTROL DID NOT RUN: %s" % missing
    OUT["control_manifest"] = dict(declared=declared, ran=RAN, missing=missing)
    json.dump(OUT, open(os.path.join(HERE, "results_case2b.json"), "w"),
              indent=1, default=str)
    print("wrote results_case2b.json")


if __name__ == "__main__":
    main()

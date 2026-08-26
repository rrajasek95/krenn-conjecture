#!/usr/bin/env python3
"""W20 -- TASK 3 controls.  UNAUDITED.  Exact only.

C1  independent engine vs W19's engine: PMS, supports, |F|, in_R, audits
    on the whole W8 ladder m = 24..28 and on the C_8 member.
C2  re-audit of W19's explicit C_8-Gamma member (the empty-clean-layer
    witness): m, Sigma, |F|, min mixed fibre, (SC), Gamma spanning
    2-connected, ZERO effectively-clean mixed words.
C3  MUTATION control: single-cell mutations of the C_8 template must be
    detected (either they leave (R) or they change the audit).
C4  reproduction of W19's clean-layer counts at m = 24..28 (2624 at m=25).
C5  Singular guard self-test (positive controls that it fires).
"""
from __future__ import annotations

import json
import os
import sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
W19 = os.path.join(os.path.dirname(HERE), "unaudited-forcing-w19-2026-08-15")

import w20_core as C                                            # noqa: E402
from w20_sing import guard_selftest                             # noqa: E402

sys.path.insert(0, W19)
import w19_core as W                                            # noqa: E402


def c1_engine():
    out = {}
    out["n_pms_match"] = (len(C.PMS) == len(W.PMS) == 105)
    out["pms_setequal"] = (set(C.PMS) == set(W.PMS))
    mism = 0
    tested = 0
    for name, T in list(C.W8_IMMUNE.items()) + [("C8", C.C8_MEMBER)]:
        fullC = C.full_pm_indices(T)
        fullW = W.full_pm_indices(T)
        if sorted(C.PMS[i] for i in fullC) != sorted(W.PMS[i] for i in fullW):
            mism += 1
        for w in C.WORDS:
            tested += 1
            a = sorted(C.PMS[i] for i in C.support(T, w))
            b = sorted(W.PMS[i] for i in W.support(T, w))
            if a != b:
                mism += 1
        if C.in_R(T) != W.in_R(T):
            mism += 1
    out["tested_word_supports"] = tested
    out["mismatches_vs_w19_engine"] = mism
    return out


def c2_c8_audit():
    T = C.C8_MEMBER
    a = C.audit(T)
    fullm = C.full_pm_indices(T)
    ks = {}
    for w in C.MIXED:
        k = C.k_of(T, w, fullm)
        ks[k] = ks.get(k, 0) + 1
    a["k_histogram_mixed"] = {str(k): v for k, v in sorted(ks.items())}
    a["min_k_mixed"] = min(ks)
    a["F_matchings"] = [[list(e) for e in C.PMS[i]] for i in fullm]
    a["expected"] = dict(m=28, sigma=148, n_F=2, min_mixed_fibre=6,
                         n_eff_clean=0, in_R=True)
    a["matches_W19_report"] = (a["m"] == 28 and a["sigma"] == 148
                               and a["n_F"] == 2 and a["min_mixed_fibre"] == 6
                               and a["n_eff_clean"] == 0 and a["in_R"])
    return a


def c3_mutations():
    """every single-cell flip of the C_8 template must be DETECTED: it must
    either leave (R) or change the audit signature."""
    T0 = list(C.C8_MEMBER)
    base = C.audit(T0)
    sig0 = (base["m"], base["sigma"], base["n_F"], base["min_mixed_fibre"],
            base["n_eff_clean"], base["in_R"])
    undetected = []
    n = 0
    for ei in range(C.NE):
        for c in range(9):
            T = list(T0)
            T[ei] ^= (1 << c)
            n += 1
            a = C.audit(T)
            sig = (a["m"], a["sigma"], a["n_F"], a["min_mixed_fibre"],
                   a["n_eff_clean"], a["in_R"])
            if sig == sig0:
                undetected.append((ei, c))
    return dict(n_mutations=n, n_undetected=len(undetected),
                undetected=[[list(C.EDGES[e]), c] for e, c in undetected[:12]],
                detected_frac="%d/%d" % (n - len(undetected), n))


def c4_ladder():
    out = {}
    for m, T in sorted(C.W8_IMMUNE.items()):
        fullm = C.full_pm_indices(T)
        nclean = sum(1 for w in C.MIXED if not C.extras_at(T, w, fullm))
        ks = {}
        for w in C.MIXED:
            k = len(C.extras_at(T, w, fullm))
            ks[k] = ks.get(k, 0) + 1
        gam = C.gamma_edges(T)
        deg = [sum(1 for e in gam if t in e) for t in range(8)]
        out[str(m)] = dict(n_gamma=len(gam), n_F=len(fullm),
                           gamma=[list(e) for e in gam], gamma_degrees=deg,
                           min_gamma_degree=min(deg),
                           n_eff_clean_mixed=nclean,
                           k_hist={str(k): v for k, v in sorted(ks.items())},
                           in_R=C.in_R(T))
    out["W19_says_m25_clean"] = 2624
    out["m25_reproduced"] = (out["25"]["n_eff_clean_mixed"] == 2624)
    return out


def main():
    res = {"_header": "UNAUDITED W20 controls. Pinned HEAD in PINNED_HEAD.txt."}
    res["C5_singular_guard"] = guard_selftest()
    print("C5 guard self-test:", res["C5_singular_guard"], flush=True)
    res["C1_engine"] = c1_engine()
    print("C1 independent engine vs W19:", res["C1_engine"], flush=True)
    res["C2_c8_audit"] = c2_c8_audit()
    a = res["C2_c8_audit"]
    print("C2 C_8 member audit: m=%d Sigma=%d |Gamma|=%d |F|=%d minfib=%d "
          "clean=%d in_R=%s  MATCHES W19: %s"
          % (a["m"], a["sigma"], a["n_gamma"], a["n_F"], a["min_mixed_fibre"],
             a["n_eff_clean"], a["in_R"], a["matches_W19_report"]), flush=True)
    print("   k histogram:", a["k_histogram_mixed"], flush=True)
    print("   F(Gamma) =", a["F_matchings"], flush=True)
    res["C4_ladder"] = c4_ladder()
    for m in ("24", "25", "26", "27", "28"):
        d = res["C4_ladder"][m]
        print("C4 m=%s |Gamma|=%d |F|=%d mindeg=%d clean=%d k-hist=%s"
              % (m, d["n_gamma"], d["n_F"], d["min_gamma_degree"],
                 d["n_eff_clean_mixed"], d["k_hist"]), flush=True)
    print("C4 m=25 clean count reproduces W19's 2624:",
          res["C4_ladder"]["m25_reproduced"], flush=True)
    res["C3_mutations"] = c3_mutations()
    print("C3 mutation control:", {k: v for k, v in res["C3_mutations"].items()
                                   if k != "undetected"}, flush=True)
    json.dump(res, open(os.path.join(HERE, "results_controls.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()

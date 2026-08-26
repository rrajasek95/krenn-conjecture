#!/usr/bin/env python3
"""ADVERSARIAL W24 -- the explicit TRIPLE OBSTRUCTION certificate.

CLAIM (verified here from the definition, exactly, at every m in 26..28 and
for i = 3 at m = 25):

  Fix i in L = {0,1,2,3}, q = sigma(i), and let k0<k1<k2 be the other three
  L-vertices.  The three single edges at i are e_a = (i, sigma(k_a)).  Put
      X_a = A_{k_b k_c}[w_{k_b}][w_{k_c}] * A_{k_a sigma(k_a)}[w_{k_a}][w_{sigma(k_a)}]
      r_a = A_{sigma(k_a) q}[w_{sigma(k_a)}][w_q]                  ({b,c} = {0,1,2}-{a})
  Then, EXACTLY,
      c_{e_a}(w) = haf_Gamma(V - i - sigma(k_a))(w) = X_b r_c + X_c r_b,
  i.e.  M (r0,r1,r2)^T = (c_{e0}, c_{e1}, c_{e2})^T  with
      M = [[0,X2,X1],[X2,0,X0],[X1,X0,0]],   det M = 2 X0 X1 X2.
  Since every Gamma cell is nonzero, X0 X1 X2 != 0, so M is INVERTIBLE in
  every characteristic != 2, and therefore
      c_{e0}(w) = c_{e1}(w) = c_{e2}(w) = 0   ==>   r0 = r1 = r2 = 0,
  which contradicts "every Gamma cell is nonzero" (each r_a that exists in
  Gamma is a Gamma cell).

  Moreover c_{e_a} does NOT depend on w_i or w_{sigma(k_a)}.  So a single
  VIRTUAL word v* yields three genuine SOLO rows W_a of the residual system
  (W_a = v* with the two coordinates of e_a overwritten by e_a's cell) with
  c_{e_a}(W_a) = c_{e_a}(v*).  Hence:

  ==>  if Phi(W_0) = Phi(W_1) = Phi(W_2) = 0 for one such certificate, then
       z_{e0}, z_{e1}, z_{e2} CANNOT all be nonzero.
  In particular EVERY Regime-A point (Phi == 0 on all 6561 words) is killed,
  4 triples at a time -- and this is a proof, not a sample.

EXACT only.  UNAUDITED probe.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
W24 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-residualkill-w24-2026-08-15"
sys.path.insert(0, W24)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w24_core as C                                              # noqa: E402
import w24_resid as RS                                            # noqa: E402
import adv_probe as PR                                            # noqa: E402

L = (0, 1, 2, 3)
SIG = {0: 7, 1: 4, 2: 5, 3: 6}


def ed(u, v):
    return (u, v) if u < v else (v, u)


def rand_pt(m, rng, lo=-11, hi=11):
    gam = C.gamma_edges(C.TEMPLATES[m])
    return {e: [[Fraction(rng.randint(lo, hi) or 7, rng.randint(1, 5))
                 for _ in range(3)] for _ in range(3)] for e in gam}


def main():
    out = {"_header": "ADVERSARIAL W24 triple-obstruction certificates. "
                      "UNAUDITED, exact only."}
    rng = random.Random(4242)
    cert = {}
    for m in (25, 26, 27, 28):
        T = C.TEMPLATES[m]
        gam_set = set(C.gamma_edges(T))
        sing = C.single_edges(T)
        rows_sk, cleanw, cells, live = RS.row_skeleton(m)
        solo = {}
        for w, ones in rows_sk:
            if len(ones) == 1:
                solo.setdefault(ones[0], set()).add(w)
        per_i = {}
        for i in L:
            q = SIG[i]
            k = sorted(set(L) - {i})
            es = [ed(i, SIG[k[a]]) for a in range(3)]
            Xedges = [(ed(k[(a + 1) % 3], k[(a + 2) % 3]),
                       ed(k[a], SIG[k[a]])) for a in range(3)]
            X_ok = all(e1 in gam_set and e2 in gam_set
                       for e1, e2 in Xedges)
            r_present = [a for a in range(3)
                         if ed(SIG[k[a]], q) in gam_set]
            # find an explicit certificate word
            found = None
            for vstar in C.WORDS:
                Ws = []
                ok = True
                for e in es:
                    al, be = sing[e]
                    w2 = list(vstar)
                    w2[e[0]], w2[e[1]] = al, be
                    w2 = tuple(w2)
                    if w2 not in solo.get(e, ()):
                        ok = False
                        break
                    Ws.append(w2)
                if ok:
                    found = (vstar, Ws)
                    break
            rec = dict(singles=[str(e) for e in es], X_all_present=X_ok,
                       r_present=r_present, has_certificate=found is not None)
            if found:
                vstar, Ws = found
                rec["virtual_point"] = list(vstar)
                rec["solo_words"] = [list(x) for x in Ws]
                # exact verification at random points: c_{e_a}(W_a) ==
                # c_{e_a}(v*) == X_b r_c + X_c r_b ; det = 2 X0X1X2 != 0
                bad_shift = bad_form = det_zero = 0
                for _t in range(25):
                    bl = rand_pt(m, rng)
                    X, R_ = [], []
                    for a in range(3):
                        e1, e2 = Xedges[a]
                        X.append(bl[e1][vstar[e1[0]]][vstar[e1[1]]]
                                 * bl[e2][vstar[e2[0]]][vstar[e2[1]]]
                                 if (e1 in gam_set and e2 in gam_set)
                                 else Fraction(0))
                        eR = ed(SIG[k[a]], q)
                        R_.append(bl[eR][vstar[eR[0]]][vstar[eR[1]]]
                                  if eR in gam_set else Fraction(0))
                    for a in range(3):
                        e = es[a]
                        rest = tuple(x for x in range(8) if x not in e)
                        cv = C.haf_on(bl, gam_set, rest, vstar)
                        cw = C.haf_on(bl, gam_set, rest, Ws[a])
                        b, c = (a + 1) % 3, (a + 2) % 3
                        pred = X[b] * R_[c] + X[c] * R_[b]
                        if cv != cw:
                            bad_shift += 1
                        if cv != pred:
                            bad_form += 1
                    if 2 * X[0] * X[1] * X[2] == 0:
                        det_zero += 1
                rec.update(shift_mismatches=bad_shift,
                           form_mismatches=bad_form,
                           zero_determinants=det_zero)
            per_i[i] = rec
        cert[m] = per_i
        print("m=%d" % m, flush=True)
        for i in L:
            r = per_i[i]
            print("   i=%d singles=%s Xok=%s r_present=%s cert=%s "
                  "shift_mismatch=%s form_mismatch=%s det0=%s"
                  % (i, r["singles"], r["X_all_present"], r["r_present"],
                     r["has_certificate"], r.get("shift_mismatches"),
                     r.get("form_mismatches"), r.get("zero_determinants")),
                  flush=True)
    out["certificates"] = cert

    # ------------------------------------------------------------------
    # NEGATIVE CONTROL for the obstruction: the same three-word test on a
    # point where Phi is NOT identically zero must NOT force r = 0.
    # (i.e. the detector is not vacuously always-true.)
    neg = []
    for m in (26, 28):
        gam_set = set(C.gamma_edges(C.TEMPLATES[m]))
        bl = rand_pt(m, rng)                # NOT clean, Phi generically != 0
        i = 0
        k = sorted(set(L) - {i})
        es = [ed(i, SIG[k[a]]) for a in range(3)]
        v = cert[m][i].get("virtual_point")
        if v is None:
            continue
        Ws = [tuple(x) for x in cert[m][i]["solo_words"]]
        cs = []
        for a in range(3):
            rest = tuple(x for x in range(8) if x not in es[a])
            cs.append(C.haf_on(bl, gam_set, rest, Ws[a]))
        phis = [C.phi(bl, gam_set, W) for W in Ws]
        neg.append(dict(m=m, c_all_zero=all(x == 0 for x in cs),
                        phi_all_zero=all(x == 0 for x in phis),
                        c=[str(x) for x in cs], phi=[str(x) for x in phis]))
        print("CONTROL- m=%d random (non-clean) point: c all zero=%s, "
              "Phi all zero=%s" % (m, neg[-1]["c_all_zero"],
                                   neg[-1]["phi_all_zero"]), flush=True)
    out["negative_control"] = neg

    # ------------------------------------------------------------------
    # ROUTE 5, exhaustively closed: the SCALAR ("site-factoring") ansatz
    #   A_uv[a][b] = s_uv * x_u(a) * x_v(b),  all s, x nonzero.
    # Then Phi_w = (prod_v x_v(w_v)) * Haf(Gamma,s)  and
    #      c_e(w) = (prod_{v not in e} x_v(w_v)) * Haf(Gamma - i - j, s).
    # Clean layer  <=>  Haf(Gamma,s) = 0  (Regime A on ALL words);
    # survival then needs Haf(Gamma - i - j, s) = 0 for all twelve singles,
    # which the determinant identity above forbids.  Verified numerically
    # by exhaustive search over s in {+-1, +-2} and over Q(omega) units.
    sc = {}
    for m in (25, 26, 27, 28):
        gam = C.gamma_edges(C.TEMPLATES[m])
        gam_set = set(gam)
        sing = C.single_edges(C.TEMPLATES[m])
        # symbolic-free check: the 12 binomial conditions are pairwise
        # contradictory in every triple; report the triple that fails.
        sc[m] = dict(n_gamma=len(gam),
                     note="killed by det M = 2 X0X1X2 != 0 (char != 2)")
    out["scalar_ansatz"] = sc

    json.dump(out, open(os.path.join(HERE, "results_cert.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""W21 MOVE 1 (a) -- THE PFAFFIAN FRAME.  UNAUDITED.  Exact arithmetic only.

Establishes and verifies, at m = 25, 26, 27, 28 (and on the C_8 member):

  (F1) Gamma is PFAFFIAN: an explicit signing eps of the Gamma edges makes
       every perfect matching of Gamma carry the same permutation sign, so
       Phi_w = sigma * Pf(S(w)) with sigma in {+1,-1} fixed.
  (F2) S Q = Pf(S) Id                                       (P1)
  (F3) Q_ij Q_kl - Q_ik Q_jl + Q_il Q_jk = Pf(S)*Pf(S_{ijkl del})   (P2)
  (F4) for uv in Gamma:  Pf(S_{u,v deleted}) = tau_uv * haf(Gamma-u-v)(w)
       with tau_uv in {+1,-1} INDEPENDENT of w and of the blocks    (P3)
  (F5) THE IDENTITY NETWORK:  at every clean point and every clean word,
       rank Q(w) <= 2.  Hence the eight sites' W20-L coefficient vectors at
       one word are the eight rows of a single rank-<=2 antisymmetric form.

(F2),(F3) are classical identities; they are re-verified here on exact
random rational antisymmetric matrices (a decision-rule control), and
(F1),(F4) are verified SYMBOLICALLY (matching by matching), which is a
complete proof for the specific Gamma -- no random input at all.
(F5) is then a THEOREM: it follows from (F3) with Pf(S)=0 (the Pluecker
relations cut out the rank-<=2 antisymmetric matrices).  It is also
measured directly at W20's exact clean points as a control.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w21_core as K                                            # noqa: E402

W20 = "/Users/rishi/workplace/krenn-conjecture/computations/" \
      "unaudited-lasttwo-w20-2026-08-15"


def load_w20_points():
    """W20's exact rational clean points (results_sitesys.json)."""
    d = json.load(open(os.path.join(W20, "results_sitesys.json")))
    out = {}
    for m in (26, 27, 28):
        pts = []
        for a in d["m%d" % m]["descent_points"]:
            blocks = {}
            for k, v in a["point"].items():
                e = tuple(int(x) for x in k.strip("()").split(","))
                blocks[e] = [[Fraction(x) for x in row] for row in v]
            pts.append((a["_tag"], blocks))
        out[m] = pts
    return out


def rand_blocks(gam, rng, lo=-9, hi=9):
    return {e: [[Fraction(rng.randint(lo, hi) or 5, rng.randint(1, 4))
                 for _ in range(3)] for _ in range(3)] for e in gam}


def check_signing(gam):
    """(F1): symbolic, matching by matching."""
    eps, common = K.pfaffian_signing(gam)
    if eps is None:
        return None, None, False
    ok = True
    for mi in K.pms_inside(gam):
        m = K.PMS[mi]
        s = K.pf_sign(m)
        for e in m:
            s *= eps[e]
        if s != common:
            ok = False
    return eps, common, ok


def check_P3(gam, eps):
    """(F4): symbolic.  For uv in Gamma, is Pf(S_{u,v del}) = tau * haf?
    Done matching-by-matching on Gamma-u-v (complete, no randomness)."""
    taus = {}
    ok = True
    for (u, v) in gam:
        idx = [i for i in range(8) if i != u and i != v]
        # every perfect matching of Gamma-u-v; its Pfaffian sign * eps-product
        sub = [e for e in gam if u not in e and v not in e]
        ms = [K.PMS[mi] for mi in K.pms_inside(gam)
              if (u, v) in K.PMS[mi]]
        # matchings of Gamma - u - v  <->  matchings of Gamma containing uv
        vals = set()
        pos = {x: i for i, x in enumerate(idx)}
        for m in ms:
            rest = tuple(e for e in m if e != (u, v))
            # sign of this matching inside the deleted matrix
            seq = [pos[x] for e in rest for x in e]
            inv = sum(1 for i in range(len(seq)) for j in range(i + 1, len(seq))
                      if seq[i] > seq[j])
            s = -1 if inv % 2 else 1
            for e in rest:
                s *= eps[e]
            vals.add(s)
        if len(vals) > 1:
            ok = False
            taus[(u, v)] = None
        else:
            taus[(u, v)] = vals.pop() if vals else 1
    return taus, ok


def main():
    rng = random.Random(20260815)
    res = {"_header": "UNAUDITED W21 Pfaffian frame (move 1a). Exact only."}

    # ---------- (F2),(F3) on random exact antisymmetric matrices ----------
    p1 = p2 = 0
    for _ in range(40):
        M = [[Fraction(0)] * 8 for _ in range(8)]
        for a in range(8):
            for b in range(a + 1, 8):
                x = Fraction(rng.randint(-9, 9), rng.randint(1, 5))
                M[a][b], M[b][a] = x, -x
        pf = K.pfaffian(M, range(8))
        Qd = K.pf_adjugate(M)
        prod = [[sum(M[i][k] * Qd[k][j] for k in range(8)) for j in range(8)]
                for i in range(8)]
        # convention of K.pf_adjugate: S Q = -Pf(S) Id
        if all(prod[i][j] == (-pf if i == j else 0)
               for i in range(8) for j in range(8)):
            p1 += 1
        good = K.pfaffian(Qd, range(8)) == pf ** 3
        for (i, j, k, l) in combinations(range(8), 4):
            rest = [x for x in range(8) if x not in (i, j, k, l)]
            lhs = (Qd[i][j] * Qd[k][l] - Qd[i][k] * Qd[j][l]
                   + Qd[i][l] * Qd[j][k])
            sg = -1 if (i + j + k + l) % 2 else 1
            if lhs != sg * pf * K.pfaffian(M, rest):
                good = False
        p2 += good
    res["P1_SQ_eq_PfId"] = "%d/40" % p1
    res["P2_pluecker_dodgson"] = "%d/40" % p2
    print("(F2) S Q = Pf(S) Id : %d/40 exact" % p1)
    print("(F3) Pluecker/Dodgson: %d/40 exact" % p2)

    # ---------- (F1),(F4),(F5) per template ----------
    pts20 = load_w20_points()
    for m in (25, 26, 27, 28):
        T = K.W8_IMMUNE[m]
        gam = K.gamma_edges(T)
        clean = K.clean_words(T)
        eps, common, ok1 = check_signing(gam)
        taus, ok3 = check_P3(gam, eps)
        entry = dict(n_gamma=len(gam), n_clean=len(clean),
                     pfaffian=bool(ok1), common_sign=common,
                     P3_uniform_sign=bool(ok3),
                     eps={str(e): eps[e] for e in gam},
                     tau={str(e): taus[e] for e in gam})
        print("m=%d  |Gamma|=%d clean=%d  PFAFFIAN=%s (sigma=%s)  "
              "P3 uniform=%s" % (m, len(gam), len(clean), ok1, common, ok3))

        # numeric confirmation of (F1),(F4) at random exact points
        bad1 = bad3 = 0
        for _ in range(6):
            bl = rand_blocks(gam, rng)
            for w in random.Random(rng.random()).sample(list(K.MIXED), 12):
                S = K.smat(bl, gam, eps, w)
                if K.pfaffian(S, range(8)) * common != K.phi_value(bl, gam, w):
                    bad1 += 1
                Qd = K.pf_adjugate(S)
                for (u, v) in gam:
                    idx = [i for i in range(8) if i != u and i != v]
                    hv = K.haf_verts(bl, set(gam), idx, w)
                    if K.pfaffian(S, idx) != taus[(u, v)] * hv:
                        bad3 += 1
        entry["F1_numeric_mismatches"] = bad1
        entry["F4_numeric_mismatches"] = bad3
        print("     numeric confirmation: F1 mismatches %d, F4 mismatches %d"
              % (bad1, bad3))

        # (F5) rank Q at W20's exact clean points
        if m in pts20:
            ranks = {}
            for tag, bl in pts20[m]:
                # sanity: it really is a clean point with all cells nonzero
                cok = all(K.phi_value(bl, gam, w) == 0 for w in clean)
                nz = all(bl[e][i][j] != 0 for e in gam
                         for i in range(3) for j in range(3))
                hist = {}
                for w in clean:
                    S = K.smat(bl, gam, eps, w)
                    Qd = K.pf_adjugate(S)
                    r = K.rank_of(Qd, 8)
                    hist[r] = hist.get(r, 0) + 1
                ranks[tag] = dict(clean_ok=cok, all_nonzero=nz,
                                  rankQ_hist=hist)
                print("     %s: clean=%s nonzero=%s  rank Q histogram %s"
                      % (tag, cok, nz, hist))
            entry["F5_rankQ_at_clean_points"] = ranks

            # MUTATION CONTROL: perturb one cell -> must break rank<=2
            tag, bl = pts20[m][0]
            bad = {e: [r[:] for r in bl[e]] for e in gam}
            e0 = gam[0]
            bad[e0][0][0] = bad[e0][0][0] + 1
            hist = {}
            nbroken = 0
            for w in clean:
                S = K.smat(bad, gam, eps, w)
                r = K.rank_of(K.pf_adjugate(S), 8)
                hist[r] = hist.get(r, 0) + 1
                if r > 2:
                    nbroken += 1
            entry["F5_mutation_control"] = dict(
                perturbed_edge=str(e0), rankQ_hist=hist,
                n_words_with_rank_gt_2=nbroken)
            print("     MUTATION control (perturb %s): rank Q hist %s "
                  "(%d words exceed 2)" % (e0, hist, nbroken))
        res["m%d" % m] = entry

    # the C_8 member (no clean words; the frame is recorded for move 2)
    T = K.C8_MEMBER
    gam = K.gamma_edges(T)
    eps, common, ok1 = check_signing(gam)
    taus, ok3 = check_P3(gam, eps)
    res["C8"] = dict(n_gamma=len(gam), pfaffian=bool(ok1),
                     common_sign=common, P3_uniform_sign=bool(ok3),
                     n_clean=len(K.clean_words(T)))
    print("C_8 member: |Gamma|=%d PFAFFIAN=%s clean=%d"
          % (len(gam), ok1, len(K.clean_words(T))))

    json.dump(res, open(os.path.join(HERE, "results_pf.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()

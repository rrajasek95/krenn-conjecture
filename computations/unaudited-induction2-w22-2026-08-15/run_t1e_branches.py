#!/usr/bin/env python3
"""W22 T1e -- the NON-VACUOUS branches of Theorem W22-T, by CONSTRUCTION.

Random draws never produce a degenerate site (T1d histogram: 2230 draws with
0 degenerate sites, 11 with one, none with >= 2) -- ledger item 12 exactly.
So the interesting branches are built:

  prescribe u, v and scalars sigma_a; set A_pa random invertible,
      alpha_a = A_pa^T u,   w_a = sigma_a alpha_a,
      A_qa^T := M_a = w_a v^T + N_a ( <v,v> I - v v^T )   (N_a random)
  so   beta_a = M_a v = <v,v> w_a = <v,v> sigma_a alpha_a,
  i.e. site a is DEGENERATE with alpha_a = rho_a beta_a, rho_a proportional
  to 1/sigma_a.  No division is used, so the construction runs verbatim over
  Z[omega] (Eisenstein integers) -- which branch (ii) needs.

  Conditions (in terms of sigma, after clearing):
     4-fold coincidence:  e_2(sigma) = 0
     3-fold coincidence:  e_1(sigma) = e_2(sigma) = 0  <=>  sigma ~ (1, w, w^2)
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-induction2-w22-2026-08-15")
sys.path.insert(0, BASE)
import w22_core as W                                        # noqa: E402
from w22_core import Eis, OMEGA                             # noqa: E402

RES = {}
N = 6
P, Q = 0, 1
U = (2, 3, 4, 5)


def build(rng, u, v, sigma, coincident, zero=0, one=1):
    """sigma: dict site -> scalar for the COINCIDENT sites; the others get a
    random (generically non-degenerate) A_qa."""
    src = {e: [[zero] * 3 for _ in range(3)]
           for e in combinations(range(N), 2)}
    vv = sum(v[i] * v[i] for i in range(3))
    for e in combinations(range(N), 2):
        src[e] = [[one * rng.randint(-3, 3) for _ in range(3)]
                  for _ in range(3)]
    for a in U:
        Apa = [[one * rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
        # store A_pa (P < a always)
        src[(P, a)] = Apa
        alpha = [sum(u[i] * Apa[i][c] for i in range(3)) for c in range(3)]
        if a in coincident:
            w = [sigma[a] * alpha[c] for c in range(3)]
            Nr = [[one * rng.randint(-2, 2) for _ in range(3)]
                  for _ in range(3)]
            # M = w v^T + Nr (vv I - v v^T)
            M = [[w[i] * v[j]
                  + sum(Nr[i][k] * ((vv if k == j else zero) - v[k] * v[j])
                        for k in range(3))
                  for j in range(3)] for i in range(3)]
            # A_qa^T = M  =>  A_qa = M^T   (Q < a always)
            src[(Q, a)] = [[M[j][i] for j in range(3)] for i in range(3)]
    return src


def report(src, u, v, tag):
    alpha, beta = W.alpha_beta(src, P, Q, u, v, U)
    ranks = {a: W.site_rank(alpha[a], beta[a]) for a in U}
    err = W.cap_error_direct(src, P, Q, W.outer_K(u, v), U)
    s = W.cap_s(src, P, Q, W.outer_K(u, v))
    kap = [u[c] * v[c] for c in range(3)]
    return {"tag": tag, "ranks": {str(a): ranks[a] for a in U},
            "n_degenerate": sum(1 for a in U if ranks[a] <= 1),
            "E_zero": len(err) == 0, "n_nonzero_components": len(err),
            "s_nonzero": s != 0,
            "kappas_nonzero": all(k != 0 for k in kap),
            "admissible": s != 0 and all(k != 0 for k in kap)}


def main():
    rng = random.Random(555111)
    rows = []

    # ---------- BRANCH (i): four-fold coincidence over Q ------------------
    ok = ctrl = 0
    for trial in range(40):
        u = [rng.randint(1, 4) for _ in range(3)]
        v = [rng.randint(1, 4) for _ in range(3)]
        if sum(x * x for x in v) == 0:
            continue
        s1, s2, s3 = (Fraction(rng.randint(1, 5)) for _ in range(3))
        e1 = s1 + s2 + s3
        if e1 == 0:
            continue
        s4 = -(s1 * s2 + s1 * s3 + s2 * s3) / e1
        if s4 == 0:
            continue
        sig = dict(zip(U, [s1, s2, s3, s4]))
        src = build(rng, u, v, sig, set(U))
        r = report(src, u, v, "branch(i) 4-fold e_2(sigma)=0")
        rows.append(r)
        if r["n_degenerate"] == 4 and r["E_zero"]:
            ok += 1
        # CONTROL: perturb sigma_4 -- must break E = 0
        sig2 = dict(sig)
        sig2[U[3]] = s4 + 1
        src2 = build(rng, u, v, sig2, set(U))
        r2 = report(src2, u, v, "branch(i) CONTROL perturbed sigma_4")
        rows.append(r2)
        if r2["n_degenerate"] == 4 and not r2["E_zero"]:
            ctrl += 1
    RES["branch_i"] = {"constructed": 40, "witness_confirmed": ok,
                       "control_fired": ctrl}
    print(f"[branch (i)] 4-fold coincidence with e_2(sigma)=0: "
          f"E = 0 in {ok} constructions; perturbation control fired {ctrl}")

    # ---------- BRANCH (ii): three-fold coincidence over Z[omega] ---------
    ok = ctrl = 0
    okadm = 0
    for trial in range(20):
        u = [Eis(rng.randint(1, 3), rng.randint(0, 2)) for _ in range(3)]
        v = [Eis(rng.randint(1, 3), rng.randint(0, 2)) for _ in range(3)]
        vv = sum((v[i] * v[i] for i in range(3)), Eis(0, 0))
        if vv == 0:
            continue
        sig = {U[0]: Eis(1, 0), U[1]: OMEGA, U[2]: OMEGA * OMEGA}
        src = build(rng, u, v, sig, {U[0], U[1], U[2]},
                    zero=Eis(0, 0), one=Eis(1, 0))
        r = report(src, u, v, "branch(ii) 3-fold sigma = (1,w,w^2)")
        rows.append(r)
        if r["n_degenerate"] == 3 and r["E_zero"]:
            ok += 1
            if r["admissible"]:
                okadm += 1
        # CONTROL: replace omega^2 by omega -- must break E = 0
        sig2 = {U[0]: Eis(1, 0), U[1]: OMEGA, U[2]: OMEGA}
        src2 = build(rng, u, v, sig2, {U[0], U[1], U[2]},
                     zero=Eis(0, 0), one=Eis(1, 0))
        r2 = report(src2, u, v, "branch(ii) CONTROL sigma = (1,w,w)")
        rows.append(r2)
        if not r2["E_zero"]:
            ctrl += 1
    RES["branch_ii"] = {"constructed": 20, "witness_confirmed": ok,
                        "admissible_witnesses": okadm,
                        "control_fired": ctrl}
    print(f"[branch (ii)] 3-fold coincidence with sigma = (1,w,w^2) over "
          f"Z[omega]: E = 0 in {ok} constructions ({okadm} fully admissible); "
          f"control (1,w,w) fired {ctrl}")

    # ---------- rational 3-fold must FAIL (the complex-only statement) ----
    fail = tot = 0
    for trial in range(40):
        u = [rng.randint(1, 4) for _ in range(3)]
        v = [rng.randint(1, 4) for _ in range(3)]
        if sum(x * x for x in v) == 0:
            continue
        s1, s2 = Fraction(rng.randint(1, 5)), Fraction(rng.randint(1, 5))
        # solve e_1 = e_2 = 0 over Q: s3 = -(s1+s2) and s1 s2 + s3(s1+s2) = 0
        s3 = -(s1 + s2)
        sig = {U[0]: s1, U[1]: s2, U[2]: s3}
        e2 = s1 * s2 + s1 * s3 + s2 * s3
        src = build(rng, u, v, sig, {U[0], U[1], U[2]})
        r = report(src, u, v, f"rational 3-fold e_1=0, e_2={e2}")
        rows.append({**r, "e2_sigma": str(e2)})
        tot += 1
        if e2 != 0 and not r["E_zero"]:
            fail += 1
    RES["rational_three_fold"] = {"tested": tot, "correctly_nonzero": fail}
    print(f"[complex-only] rational sigma with e_1 = 0 always has "
          f"e_2 != 0 and E != 0: {fail}/{tot}")

    RES["rows"] = rows
    with open(f"{BASE}/results_t1e_branches.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)


if __name__ == "__main__":
    main()

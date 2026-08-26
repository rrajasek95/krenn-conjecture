#!/usr/bin/env python3
"""W22 T1f -- THEOREM W22-X: what exactness + all-blocked forces.

(X1) STAR INJECTIVITY.  For an exact source, for every vertex p,
        intersection over y != p of ker(A_py^T)  =  0.
     Proof: the one-off-colour words give (Lemma W22-S)
        sum_{y != p} C^{(c)}_{py} A_py(., c) = e_c   in V_p,
     and pairing with u gives  sum_y C^{(c)}_{py} (A_py^T u)_c = u_c.
     If A_py^T u = 0 for every y then u_c = 0 for every c.

(X2) DETACHMENT => WITNESS.  If u in V_p has all coordinates nonzero and
     W(u) := {y != p : A_py^T u != 0} has |W(u)| <= 2, pick q in W(u).  Then
     alpha_a = 0 for every a in U = B\\{p,q} except at most one, so the
     R-support graph is a star and Lemma W22-M gives E_pq(u (x) v) = 0 for
     EVERY v; and A_pq^T u != 0 supplies an admissible v.  So (p,q) carries a
     witness.  Hence:

     ALL-BLOCKED + EXACT  =>  for every p and every u with u_0 u_1 u_2 != 0,
                              |W(u)| >= 3.
     Equivalently: for every S of size >= N-3 in B\\{p}, the common left
     kernel of {A_pa : a in S} lies in ONE coordinate hyperplane of V_p.

Verified here: (X1) on exact sources; (X2) by explicit construction (build a
source with a prescribed detached star and check the witness), with a
mutation control.
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
import w22_sitelin as SL                                    # noqa: E402

RES = {}


def delta43():
    src = {e: [[0] * 3 for _ in range(3)] for e in combinations(range(4), 2)}
    for c, M in enumerate([((0, 1), (2, 3)), ((0, 2), (1, 3)),
                           ((0, 3), (1, 2))]):
        for e in M:
            src[e][c][c] = 1
    return src


def delta_n2(n):
    cyc = list(range(n))
    edges = [(cyc[i], cyc[(i + 1) % n]) for i in range(n)]
    src = {e: [[0, 0], [0, 0]] for e in combinations(range(n), 2)}
    for i in range(0, n, 2):
        src[W.ekey(*edges[i])][0][0] = 1
    for i in range(1, n, 2):
        src[W.ekey(*edges[i])][1][1] = 1
    return src


def star_kernel(src, p, n, ncol=3, sites=None):
    """basis of the common left kernel of {A_py^T : y in sites}."""
    ys = [y for y in range(n) if y != p] if sites is None else list(sites)
    rows = []
    for y in ys:
        M = W.oriented(src, p, y, ncol)
        for c in range(ncol):
            rows.append([Fraction(M[i][c]) for i in range(ncol)])
    part, kern = SL.solve_linear(rows, [Fraction(0)] * len(rows))
    return kern


def main():
    rng = random.Random(246810)

    # ---------------- (X1) star injectivity on EXACT sources ---------------
    rows = []
    src = delta43()
    for p in range(4):
        k = star_kernel(src, p, 4)
        rows.append({"source": "Delta_{4,3}", "p": p, "dim_ker": len(k)})
    for n in (6, 8, 10):
        s2 = delta_n2(n)
        for p in range(n):
            k = star_kernel(s2, p, n, ncol=2)
            rows.append({"source": f"Delta_{{{n},2}}", "p": p,
                         "dim_ker": len(k)})
    bad = [r for r in rows if r["dim_ker"] != 0]
    RES["X1_star_injectivity"] = {"checked": len(rows), "violations": len(bad),
                                  "rows": rows}
    print(f"[X1] star injectivity on exact sources: {len(rows)} vertices, "
          f"{len(bad)} with nonzero common star kernel")

    # CONTROL: a NON-exact source generally has a vertex with nonzero kernel
    ctrl = 0
    tot = 0
    for _ in range(200):
        n = 6
        s = {e: [[0] * 3 for _ in range(3)] for e in combinations(range(n), 2)}
        p = 0
        # deliberately give p a rank-2 star
        u = [1, 1, 1]
        for y in range(1, n):
            M = [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
            # project rows so that M^T u = 0  (u in left kernel)
            for c in range(3):
                col = [M[i][c] for i in range(3)]
                sh = sum(u[i] * col[i] for i in range(3))
                M[0][c] -= sh          # u = (1,1,1): subtract from row 0
            s[(0, y)] = M
        for e in combinations(range(1, n), 2):
            s[e] = [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
        tot += 1
        if len(star_kernel(s, 0, n)) >= 1:
            ctrl += 1
    RES["X1_control"] = {"trials": tot, "kernel_nonzero": ctrl}
    print(f"[X1 control] deliberately detached stars have nonzero kernel: "
          f"{ctrl}/{tot} (the property is not automatic)")

    # ---------------- (X2) detachment => witness, by construction ----------
    n = 8
    made = ok = adm = 0
    ctrlfired = 0
    for trial in range(60):
        u = [rng.randint(1, 4) for _ in range(3)]
        p, q = 0, 1
        Uset = tuple(range(2, n))
        src = {e: [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
               for e in combinations(range(n), 2)}
        # detach every site of U except a0 from p:  A_pa^T u = 0
        a0 = Uset[0]
        for a in Uset:
            if a == a0:
                continue
            M = [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
            for c in range(3):
                sh = sum(u[i] * M[i][c] for i in range(3))
                # u_0 != 0, so adjust row 0
                M[0][c] = Fraction(M[0][c]) - Fraction(sh, u[0])
            src[W.ekey(p, a)] = M if p < a else [[M[j][i] for j in range(3)]
                                                 for i in range(3)]
        made += 1
        # admissible v
        w = [sum(u[i] * W.oriented(src, p, q)[i][c] for i in range(3))
             for c in range(3)]
        if all(x == 0 for x in w):
            continue
        v = None
        for _ in range(40):
            cand = [rng.randint(1, 5) for _ in range(3)]
            if sum(w[c] * cand[c] for c in range(3)) != 0:
                v = cand
                break
        if v is None:
            continue
        K = W.outer_K(u, v)
        err = W.cap_error_direct(src, p, q, K, Uset)
        gr, ga = W.support_graphs(src, p, q, K, Uset)
        if len(err) == 0:
            ok += 1
        if W.is_admissible(src, p, q, K):
            adm += 1
        # CONTROL: undo the detachment at one site -> E must become nonzero
        src2 = {e: [r[:] for r in m] for e, m in src.items()}
        a1 = Uset[1]
        src2[W.ekey(p, a1)] = [[rng.randint(1, 4) for _ in range(3)]
                               for _ in range(3)]
        if len(W.cap_error_direct(src2, p, q, K, Uset)) > 0:
            ctrlfired += 1
    RES["X2_detachment"] = {"constructed": made, "E_zero": ok,
                            "admissible": adm, "control_fired": ctrlfired}
    print(f"[X2] detached star (|W(u)| = 1) at N=8 gives E = 0: {ok}/{made} "
          f"({adm} admissible); re-attaching one site breaks it "
          f"{ctrlfired}/{made}")

    with open(f"{BASE}/results_t1f_forcing.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)


if __name__ == "__main__":
    main()

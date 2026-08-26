#!/usr/bin/env python3
"""A6-B9 / adversarial sweep for CLAIM C2.

Hunts for a full-rank A that breaks any part of the phi law:
    codim_{S^4} J_4(A) = 1,   perp = span{phi_A},   phi_A = q_A^2 - 4 shat det,
    exclusion table = {m : <phi_A, m> != 0},   e_2(N)^2 - 4 e_1 e_3 = det(A)^2 phi_A.
70+ matrices: random dense, random small-entry (degenerate cofactor structure
is much more likely there), and hand-built structured families.
All exact (integer row reduction over Q, integer apolar pairings).
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-audit-a6-w15w14-2026-08-15")
import b9_core as B                                            # noqa: E402

HERE = "/Users/rishi/workplace/krenn-conjecture/computations/" \
       "unaudited-audit-a6-w15w14-2026-08-15"


def battery():
    out = []
    rng = random.Random(20260815)          # NOT W14's seed 9081726
    n = 0
    while n < 40:
        A = [[rng.randint(-9, 9) for _ in range(3)] for _ in range(3)]
        if B.rank_num(A) == 3:
            out.append((f"rand9_{n}", A))
            n += 1
    n = 0
    while n < 20:
        A = [[rng.randint(-2, 2) for _ in range(3)] for _ in range(3)]
        if B.rank_num(A) == 3:
            out.append((f"rand2_{n}", A))
            n += 1
    # structured full-rank families
    import itertools
    for p in itertools.permutations(range(3)):
        out.append((f"perm{p}", [[1 if j == p[i] else 0 for j in range(3)]
                                 for i in range(3)]))
    out += [
        ("diag(1,1,1)", [[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        ("diag(2,2,3)", [[2, 0, 0], [0, 2, 0], [0, 0, 3]]),
        ("diag(1,-1,1)", [[1, 0, 0], [0, -1, 0], [0, 0, 1]]),
        ("upper triangular", [[1, 5, 7], [0, 2, 9], [0, 0, 3]]),
        ("I + nilpotent", [[1, 1, 0], [0, 1, 1], [0, 0, 1]]),
        ("symmetric", [[2, 3, 5], [3, 7, 11], [5, 11, 4]]),
        ("companion", [[0, 0, 6], [1, 0, -11], [0, 1, 6]]),
        ("cof_00 = 0", [[1, 2, 3], [4, 2, 1], [7, 4, 2]]),
        ("cof_11 = 0", [[2, 3, 1], [5, 1, 7], [4, 9, 2]]),
        ("cof_22 = 0", [[1, 2, 5], [2, 4, 3], [7, 1, 6]]),
        ("cof_01 = 0", [[3, 1, 2], [2, 5, 4], [1, 7, 2]]),
        ("zero 2x2 block", [[1, 2, 3], [4, 0, 0], [5, 0, 7]]),
        ("zero diagonal", [[0, 1, 2], [3, 0, 4], [5, 6, 0]]),
        ("det 1, big", [[1000, 999, 1], [999, 998, 1], [1, 1, 1]]),
        ("one zero row entry", [[0, 1, 1], [1, 0, 1], [1, 1, 0]]),
        ("A = adj-like", [[2, 0, 0], [0, 3, 0], [0, 0, 5]]),
        ("all ones + I", [[2, 1, 1], [1, 2, 1], [1, 1, 2]]),
        ("skew + I", [[1, 5, -2], [-5, 1, 7], [2, -7, 1]]),
        ("rational", [[Fraction(1, 3), 2, Fraction(-1, 5)],
                      [4, Fraction(7, 2), 1], [0, Fraction(1, 7), 3]]),
    ]
    return [(lab, A) for lab, A in out if B.rank_num(A) == 3]


def int_vec(v):
    from math import gcd
    den = 1
    for x in v:
        den = den * Fraction(x).denominator // gcd(den,
                                                   Fraction(x).denominator)
    out = [int(Fraction(x) * den) for x in v]
    g = 0
    for x in out:
        g = gcd(g, abs(x))
    return [x // g for x in out] if g > 1 else out


def main():
    t0 = time.time()
    bat = battery()
    print(f"== B9 / C2 adversarial sweep: {len(bat)} full-rank matrices ==\n")
    fails, recs = [], []
    for lab, A in bat:
        L3 = B.L_gens(3, A)
        J4 = B.J_gens(3, 1, A, gens=L3)
        E3 = B.IntEchelon(165)
        for g in L3:
            E3.add(int_vec(B.to_vec(g, 3)))
        E4 = B.IntEchelon(495)
        for g in J4:
            E4.add(int_vec(B.to_vec(g, 4)))
        c3, c4 = 165 - E3.rank(), 495 - E4.rank()
        phi = B.phi_form(A)
        inperp = all(B.apolar(phi, g) == 0 for g in J4)
        law = True
        for a, b in B.l_monomials(4):
            m = B.lmono_poly(a, b, A)
            truth = True if not m else E4.contains(int_vec(B.to_vec(m, 4)))
            if truth != (B.apolar(phi, m) == 0):
                law = False
                break
        N = B.matmul_poly(True, B.adj_num(A))
        disc = B.padd(B.pmul(B.char_e(N, 2), B.char_e(N, 2)),
                      B.pscale(B.pmul(B.char_e(N, 1), B.char_e(N, 3)), -4))
        d2 = Fraction(B.det_num(A)) ** 2
        idok = (disc == {m: c * d2 for m, c in phi.items()})
        ok = (c3 == 29 and c4 == 1 and inperp and bool(phi) and law and idok)
        recs.append({"label": lab, "A": [[str(x) for x in r] for r in A],
                     "det": str(B.det_num(A)), "codim3": c3, "codim4": c4,
                     "phi_in_perp": inperp, "phi_nonzero": bool(phi),
                     "phi_law": law, "disc_identity_detA2": idok, "ok": ok})
        if not ok:
            fails.append(recs[-1])
            print(f"  !! {lab}: codim3 {c3} codim4 {c4} perp {inperp} "
                  f"law {law} ident {idok}  A={A}")
    # structural extras: scale invariance of the layer, phi homogeneity
    A = [[3, -7, 2], [5, 1, -4], [-6, 8, 9]]
    E = B.IntEchelon(165)
    for g in B.L_gens(3, A):
        E.add(B.to_vec(g, 3))
    scale_ok = all(E.contains(B.to_vec(g, 3))
                   for g in B.L_gens(3, [[7 * x for x in r] for r in A]))
    phiA, phi7 = B.phi_form(A), B.phi_form([[7 * x for x in r] for r in A])
    hom_ok = (phi7 == {m: 49 * c for m, c in phiA.items()})
    print(f"\n  L_3(7A) inside L_3(A): {scale_ok}   phi_(7A) = 49 phi_A: "
          f"{hom_ok}")
    summary = {"matrices": len(bat), "failures": len(fails),
               "all_codim4_eq_1": all(r["codim4"] == 1 for r in recs),
               "all_codim3_eq_29": all(r["codim3"] == 29 for r in recs),
               "all_phi_in_perp": all(r["phi_in_perp"] for r in recs),
               "all_phi_law": all(r["phi_law"] for r in recs),
               "all_disc_identity": all(r["disc_identity_detA2"]
                                        for r in recs),
               "layer_scale_invariant": scale_ok,
               "phi_degree2_homogeneous_in_A": hom_ok,
               "seconds": round(time.time() - t0, 1)}
    print("  SUMMARY:", json.dumps(summary))
    with open(HERE + "/b9_c2_sweep.json", "w") as fh:
        json.dump({"summary": summary, "failures": fails, "results": recs},
                  fh, indent=1)
    print("  wrote b9_c2_sweep.json")


if __name__ == "__main__":
    main()

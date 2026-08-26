#!/usr/bin/env python3
"""A6-B9 / addendum: the structural facts behind C1 and C2.

  (i)   at h = 2 the layer carries NO A-dependence at all: L_2(A) =
        iota_2(Sigma_2) literally has the same generator list for every A
        (s enters with exponent h-k = 0), so "perp = span{det K}
        independently of A" is a definitional, not an empirical, statement;
  (ii)  the Cauchy maps are injective: dim iota_2(Sigma_2) = 36,
        dim iota_3(Sigma_3) = 100;
  (iii) dim L_3(A) by rank(A) -- W14's directness claim 136 / 131 / 125;
  (iv)  what perp(J_4(A)) contains at rank <= 2 (phi_A stays in the perp but
        no longer spans it; at rank 0 phi_A vanishes identically).
All exact.
"""

from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-audit-a6-w15w14-2026-08-15")
import b9_core as B                                            # noqa: E402

HERE = "/Users/rishi/workplace/krenn-conjecture/computations/" \
       "unaudited-audit-a6-w15w14-2026-08-15"

MATS = [("identity", [[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        ("generic", [[3, -7, 2], [5, 1, -4], [-6, 8, 9]]),
        ("W14 generic", [[-1, 2, -5], [-5, -4, -4], [-1, -5, -4]]),
        ("large", [[71, -13, 29], [0, 5, -23], [104, 3, -1]]),
        ("rank2", [[1, 2, 3], [4, 5, 6], [5, 7, 9]]),
        ("rank1", [[2, -4, 6], [-1, 2, -3], [3, -6, 9]]),
        ("zero", [[0, 0, 0], [0, 0, 0], [0, 0, 0]])]


def main():
    out = {}
    base = B.L_gens(2, MATS[0][1])
    same = all(B.L_gens(2, A) == base for _, A in MATS)
    out["L2_generator_list_identical_for_all_A"] = same
    print(f"(i)   L_2(A) generator list identical for all 7 test matrices: "
          f"{same}  ({len(base)} generators)")

    E = B.IntEchelon(45)
    for g in base:
        E.add(B.to_vec(g, 2))
    d2 = E.rank()
    E = B.IntEchelon(165)
    for mu, nu in B.sigma_basis(3):
        E.add(B.to_vec(dict(B.iota(3, mu, nu)), 3))
    d3 = E.rank()
    out["dim_iota2_Sigma2"] = d2
    out["dim_iota3_Sigma3"] = d3
    print(f"(ii)  dim iota_2(Sigma_2) = {d2} (basis 36), "
          f"dim iota_3(Sigma_3) = {d3} (basis 100)")

    tab = {}
    for lab, A in MATS:
        E = B.IntEchelon(165)
        for g in B.L_gens(3, A):
            E.add(B.to_vec(g, 3))
        tab[lab] = {"rank_A": B.rank_num(A), "dim_L3": E.rank(),
                    "direct_sum_dim": 136}
        print(f"(iii) {lab:12s} rank {tab[lab]['rank_A']}: dim L_3(A) = "
              f"{E.rank()}   (direct would be 136)")
    out["dim_L3_by_matrix"] = tab

    perp = {}
    for lab, A in MATS:
        J4 = B.J_gens(3, 1, A)
        E = B.IntEchelon(495)
        for g in J4:
            E.add(B.to_vec(g, 4))
            if E.rank() == 495:
                break
        phi = B.phi_form(A)
        perp[lab] = {"rank_A": B.rank_num(A), "codim4": 495 - E.rank(),
                     "phi_nonzero": bool(phi),
                     "phi_in_perp": all(B.apolar(phi, g) == 0 for g in J4)}
        print(f"(iv)  {lab:12s} rank {perp[lab]['rank_A']}: codim(J_4) = "
              f"{perp[lab]['codim4']}, phi nonzero {perp[lab]['phi_nonzero']}, "
              f"phi in perp {perp[lab]['phi_in_perp']}")
    out["perp_by_matrix"] = perp
    with open(HERE + "/b9_addendum.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote b9_addendum.json")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""A6-B9 / CLAIM C1:  h = 2 DET LAW.

Claim under test (W14 REPORT item 4):
    J_3(A) = S^1 * iota_2(Sigma_2) has perp = span{det K} for every A, hence
    an L-monomial m of degree 3 lies in J_3(A)  <=>  det(d/dK) m = 0,
    and the codimensions of the h=2 layer are {2: 9, 3: 1, 4: 0, 5: 0}.

Three INDEPENDENT membership engines are compared for every (A, m):
    E1  exact integer row reduction over Q (my IntEchelon)  -- "is m in the
        row space of the generator matrix of J_3(A)?"
    E2  Singular over Q: reduce(m, std(ideal(L_2 gens))) == 0
    E3  the det(d/dK) m == 0 criterion (the claim itself)
E1 and E2 are ground truth; E3 is the claim.  Codimensions come from exact
integer rank (never modular).
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-audit-a6-w15w14-2026-08-15")
import b9_core as B                                            # noqa: E402

HERE = "/Users/rishi/workplace/krenn-conjecture/computations/" \
       "unaudited-audit-a6-w15w14-2026-08-15"

# ---------------------------------------------------------------- battery
# "new" = NOT in W14's results_task2_layers.json battery (which is exactly
# the 9 matrices: generic [[-1,2,-5],[-5,-4,-4],[-1,-5,-4]], rank2
# [[-7,-6,-5],[13,18,23],[-8,-9,-10]], rank1 [[4,-2,-1],[12,-6,-3],[-8,4,2]],
# zero, identity, perm(0 1 2->1 2 0), [[2,4,6],[1,15,5],[5,3,1]],
# [[0,6,5],[6,2,2],[3,4,2]], [[6,1,2],[2,0,0],[5,0,0]]).
BATTERY = [
    ("identity",                 [[1, 0, 0], [0, 1, 0], [0, 0, 1]],      False),
    ("permutation(012->120)",    [[0, 1, 0], [0, 0, 1], [1, 0, 0]],      False),
    ("diag(1,2,-3)",             [[1, 0, 0], [0, 2, 0], [0, 0, -3]],     True),
    ("generic full rank (new)",  [[3, -7, 2], [5, 1, -4], [-6, 8, 9]],   True),
    ("rank 2, det 0 (new)",      [[1, 2, 3], [4, 5, 6], [5, 7, 9]],      True),
    ("rank 1 (new)",             [[2, -4, 6], [-1, 2, -3], [3, -6, 9]],  True),
    ("zero matrix",              [[0, 0, 0], [0, 0, 0], [0, 0, 0]],      False),
    ("W14 generic (cross-chk)",  [[-1, 2, -5], [-5, -4, -4], [-1, -5, -4]],
                                                                         False),
    ("large entries (new)",      [[71, -13, 29], [0, 5, -23], [104, 3, -1]],
                                                                         True),
    ("antisymmetric + I (new)",  [[1, 2, 3], [-2, 1, 4], [-3, -4, 1]],   True),
    ("all row sums 0 (new)",     [[1, 2, -3], [4, -9, 5], [-2, 7, -5]],  True),
    ("zero first row (new)",     [[0, 0, 0], [1, 2, 3], [4, 5, 7]],      True),
]


def singular_membership(h, A, degree, gens):
    """Engine 2: exact ideal membership over Q inside Singular."""
    lines = [f'ring R=0,({",".join(B.SVARS)}),dp;',
             "ideal I=" + ",".join(B.sing_poly(g) for g in gens) + ";",
             "ideal G=std(I);",
             f'"KBASE "+string(size(kbase(G,{degree})));']
    names = []
    for a, b in B.l_monomials(degree):
        p = B.lmono_poly(a, b, A)
        nm = B.lmono_name(a, b)
        names.append(nm)
        lines.append(f'"MEM {nm} "+string(reduce({B.sing_poly(p)},G)==0);')
    out = B.run_singular("\n".join(lines))
    mem, kb = {}, None
    for line in out.splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == "KBASE":
            kb = int(f[1])
        elif f[0] == "MEM":
            mem[f[1]] = (f[2] == "1")
    B.check(kb is not None and len(mem) == len(names),
            f"singular parse: kbase={kb} mem={len(mem)}/{len(names)}")
    return mem, kb


def main():
    t0 = time.time()
    dp = B.det_poly()
    results = []
    print("== B9 / C1: the h = 2 determinant law ==")
    print("   ambient dims: deg2 45, deg3 165, deg4 495, deg5 1287\n")
    for label, A, is_new in BATTERY:
        t1 = time.time()
        rec = {"label": label, "A": A, "new_vs_W14": is_new,
               "rank_A": B.rank_num(A), "det_A": B.det_num(A)}
        L2 = B.L_gens(2, A)
        rec["dim_L2_gens"] = len(L2)

        # ---- exact codimension of the layer in degrees 2..5 (integer RREF)
        codim = {}
        for d in (2, 3, 4, 5):
            amb = len(B.expos(d))
            gens = B.J_gens(2, d - 2, A, gens=L2)
            E = B.IntEchelon(amb)
            for g in gens:
                E.add(B.to_vec(g, d))
                if E.rank() == amb:
                    break
            codim[d] = amb - E.rank()
            if d == 3:
                E3, gens3 = E, gens
        rec["codim_exact"] = codim

        # ---- perp of J_3 contains det K?  (exact, every generator)
        pairs = [B.apolar(dp, g) for g in gens3]
        rec["det_perp_to_all_J3_generators"] = all(x == 0 for x in pairs)
        rec["n_J3_generators"] = len(gens3)
        # perp dim 1 + det in perp + det != 0  =>  perp = span{det}
        rec["perp_is_span_det"] = (codim[3] == 1
                                   and rec["det_perp_to_all_J3_generators"])

        # ---- membership of the 20 degree-3 L-monomials, three engines
        sing_mem, sing_kb = singular_membership(2, A, 3, L2)
        table = {}
        agree_e1e2 = agree_e1e3 = True
        for a, b in B.l_monomials(3):
            nm = B.lmono_name(a, b)
            m = B.lmono_poly(a, b, A)
            zero = not m
            e1 = True if zero else E3.contains(B.to_vec(m, 3))
            e2 = sing_mem[nm]
            dop = B.apply_op(dp, m)                  # det(d/dK) m  (a scalar)
            e3 = (dop == {})
            # cross-check: <det, m> must equal det(d/dK) m for degree-3 m
            B.check(B.apolar(dp, m) == dop.get(B.ZERO, 0),
                    "apolar(det,m) != det(d)m")
            table[nm] = {"zero_poly": zero, "E1_exact_rref": e1,
                         "E2_singular": e2, "E3_det_criterion": e3,
                         "det_of_m": dop.get(B.ZERO, 0)}
            agree_e1e2 &= (e1 == e2)
            agree_e1e3 &= (e1 == e3)
        rec["membership"] = table
        rec["E1_equals_E2"] = agree_e1e2
        rec["DET_LAW_HOLDS"] = agree_e1e3
        rec["singular_kbase_deg3"] = sing_kb
        rec["singular_kbase_matches_exact_codim"] = (sing_kb == codim[3])
        rec["n_in_layer"] = sum(1 for v in table.values() if v["E1_exact_rref"])
        rec["excluded"] = sorted(k for k, v in table.items()
                                 if not v["E1_exact_rref"])
        results.append(rec)
        print(f"  {label:26s} rank {rec['rank_A']} det {rec['det_A']:>7}: "
              f"codim {codim}  det in perp {rec['det_perp_to_all_J3_generators']}"
              f"  E1=E2 {agree_e1e2}  DET LAW {rec['DET_LAW_HOLDS']}  "
              f"excluded {rec['excluded']}  [{time.time()-t1:.1f}s]")

    w14_codim = {"2": 9, "3": 1, "4": 0, "5": 0}
    same = all(all(r["codim_exact"][d] == w14_codim[str(d)]
                   for d in (2, 3, 4, 5)) for r in results)
    summary = {"claim": "C1 h=2 det law",
               "matrices": len(results),
               "all_det_laws_hold": all(r["DET_LAW_HOLDS"] for r in results),
               "all_E1_equals_E2": all(r["E1_equals_E2"] for r in results),
               "all_perp_is_span_det": all(r["perp_is_span_det"]
                                           for r in results),
               "all_codims_match_W14_{2:9,3:1,4:0,5:0}": same,
               "seconds": round(time.time() - t0, 1)}
    print("\n  SUMMARY:", json.dumps(summary))
    with open(HERE + "/b9_c1_detlaw.json", "w") as fh:
        json.dump({"summary": summary, "results": results}, fh, indent=1)
    print("  wrote b9_c1_detlaw.json")


if __name__ == "__main__":
    main()

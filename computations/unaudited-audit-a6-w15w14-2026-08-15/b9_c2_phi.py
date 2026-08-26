#!/usr/bin/env python3
"""A6-B9 / CLAIM C2:  h = 3 PHI LAW  (and C3: the det law at h = 3).

Claim under test (W14 REPORT item 4):
    at full rank, J_4(A) = S^1 * L_3(A) has codim 1 in S^4(C^9) (dim 495) and
    perp(J_4(A)) = span{phi_A},  phi_A = q_A^2 - 4 shat_A det K,
        q_A(K)    = sum_ij A_ij cof_ij(K)          (quadratic)
        shat_A(K) = sum_ij cof_ij(A) K_ij          (linear)
    equivalently phi_A = e_2(N)^2 - 4 e_1(N) e_3(N),  N = K adj(A);
    perp dims at rank(A) = 2, 1, 0 are 6, 15, 45.

Engines, all exact:
    E1  exact integer row reduction over Q  -> rank/codim and membership
    E2  Singular over Q: kbase(std(I), d) and reduce(m, std(I)) == 0
    E3  the closed form phi_A: membership <=> <phi_A, m> = 0
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from math import gcd

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-audit-a6-w15w14-2026-08-15")
import b9_core as B                                            # noqa: E402

HERE = "/Users/rishi/workplace/krenn-conjecture/computations/" \
       "unaudited-audit-a6-w15w14-2026-08-15"

F = Fraction

# ---------------------------------------------------------------- battery
# NEW  = used by neither W14 run (their taxonomy battery of 9 in
#        results_task2_layers.json, nor their 6 seed-9081726 random matrices
#        in results_task2_closedform.json).
BATTERY = [
    ("diag(1,2,-3)",            [[1, 0, 0], [0, 2, 0], [0, 0, -3]],       "NEW"),
    ("generic full rank",       [[3, -7, 2], [5, 1, -4], [-6, 8, 9]],     "NEW"),
    ("antisymmetric + I",       [[1, 2, 3], [-2, 1, 4], [-3, -4, 1]],     "NEW"),
    ("large entries",           [[71, -13, 29], [0, 5, -23], [104, 3, -1]],
                                                                          "NEW"),
    ("row0 sums to 0, rank 3",  [[1, 2, -3], [4, -9, 5], [-2, 7, 1]],     "NEW"),
    ("rational entries",        [[F(1, 2), F(-3), F(2, 3)],
                                 [F(1), F(0), F(-5, 7)],
                                 [F(4), F(1, 3), F(1)]],                  "NEW"),
    ("identity",                [[1, 0, 0], [0, 1, 0], [0, 0, 1]],        "W14"),
    ("permutation(012->120)",   [[0, 1, 0], [0, 0, 1], [1, 0, 0]],        "W14"),
    ("W14 taxonomy generic",    [[-1, 2, -5], [-5, -4, -4], [-1, -5, -4]], "W14"),
    ("W14 closedform rand#1",   [[3, 3, 3], [0, 3, -4], [-3, 1, -1]],     "W14"),
    ("rank 2 (new)",            [[1, 2, 3], [4, 5, 6], [5, 7, 9]],        "NEW"),
    ("rank 2 (W14 taxonomy)",   [[-7, -6, -5], [13, 18, 23], [-8, -9, -10]],
                                                                          "W14"),
    ("rank 1 (new)",            [[2, -4, 6], [-1, 2, -3], [3, -6, 9]],    "NEW"),
    ("rank 1 (W14 taxonomy)",   [[4, -2, -1], [12, -6, -3], [-8, 4, 2]],  "W14"),
    ("rank 0 (zero matrix)",    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],        "W14"),
]


def int_vec(v):
    """Clear denominators of a rational vector (row scaling: same row space,
    same membership question)."""
    den = 1
    out = []
    for x in v:
        x = F(x)
        den = den * x.denominator // gcd(den, x.denominator)
    for x in v:
        out.append(int(F(x) * den))
    g = 0
    for x in out:
        g = gcd(g, abs(x))
    return [x // g for x in out] if g > 1 else out


def singular_query(A, gens, degrees, mono_degree):
    lines = [f'ring R=0,({",".join(B.SVARS)}),dp;',
             "ideal I=" + ",".join(B.sing_poly(g) for g in gens) + ";",
             "ideal G=std(I);"]
    for d in degrees:
        lines.append(f'"KB {d} "+string(size(kbase(G,{d})));')
    for a, b in B.l_monomials(mono_degree):
        p = B.lmono_poly(a, b, A)
        lines.append(f'"MEM {B.lmono_name(a, b)} "'
                     f"+string(reduce({B.sing_poly(p)},G)==0);")
    out = B.run_singular("\n".join(lines))
    kb, mem = {}, {}
    for line in out.splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == "KB":
            kb[int(f[1])] = int(f[2])
        elif f[0] == "MEM":
            mem[f[1]] = (f[2] == "1")
    return kb, mem


def main():
    t0 = time.time()
    results = []
    print("== B9 / C2: the h = 3 quartic obstruction phi_A ==")
    print("   ambient dims: deg3 165, deg4 495, deg5 1287\n")
    for label, A, prov in BATTERY:
        t1 = time.time()
        rk, dt = B.rank_num(A), B.det_num(A)
        rec = {"label": label, "provenance": prov,
               "A": [[str(x) for x in row] for row in A],
               "rank_A": rk, "det_A": str(dt)}
        L3 = B.L_gens(3, A)
        J4 = B.J_gens(3, 1, A, gens=L3)
        rec["n_L3_gens"], rec["n_J4_gens"] = len(L3), len(J4)

        # ---------- exact codimensions (integer row reduction over Q)
        codim, E4 = {}, None
        for d in (3, 4):
            amb = len(B.expos(d))
            gens = L3 if d == 3 else B.J_gens(3, d - 3, A, gens=L3)
            E = B.IntEchelon(amb)
            for g in gens:
                E.add(int_vec(B.to_vec(g, d)))
                if E.rank() == amb:
                    break
            codim[d] = amb - E.rank()
            if d == 4:
                E4 = E
        # degree 5: modular rank is a RIGOROUS LOWER bound on rank_Q, i.e. a
        # rigorous UPPER bound on the codimension; Singular's kbase (below)
        # supplies the exact value over Q.
        rows5 = [int_vec(B.to_vec(g, 5)) for g in B.J_gens(3, 2, A, gens=L3)]
        codim[5] = 1287 - B.rank_mod_p(rows5, 1287)
        rec["codim_deg5_is_modular_upper_bound"] = True
        rec["codim_exact"] = codim
        rec["dim_L3"] = 165 - codim[3]

        # ---------- (b,c) phi_A in the perp, and nonzero
        phi = B.phi_form(A)
        rec["phi_nonzero"] = bool(phi)
        rec["phi_n_terms"] = len(phi)
        bad = [i for i, g in enumerate(J4) if B.apolar(phi, g) != 0]
        rec["phi_perp_to_all_J4_generators"] = (not bad)
        rec["n_phi_pairings_checked"] = len(J4)
        rec["phi_spans_perp"] = (codim[4] == 1 and not bad and bool(phi))

        # ---------- the e_i(K adj A) identity
        N = B.matmul_poly(True, B.adj_num(A))
        e1, e2, e3 = (B.char_e(N, r) for r in (1, 2, 3))
        disc = B.padd(B.pmul(e2, e2), B.pscale(B.pmul(e1, e3), -4))
        ratio, ident = None, None
        if phi:
            ks = set(disc) | set(phi)
            r0 = None
            ok = True
            for k in ks:
                a_, b_ = F(phi.get(k, 0)), F(disc.get(k, 0))
                if a_ == 0 and b_ == 0:
                    continue
                if a_ == 0:
                    ok = False
                    break
                r_ = b_ / a_
                if r0 is None:
                    r0 = r_
                elif r_ != r0:
                    ok = False
                    break
            ident, ratio = ok, (None if r0 is None else str(r0))
        rec["disc_eq_scalar_times_phi"] = ident
        rec["disc_over_phi_ratio"] = ratio
        rec["detA_squared"] = str(F(dt) ** 2)
        rec["ratio_equals_detA_squared"] = (ratio is not None
                                            and F(ratio) == F(dt) ** 2)

        # ---------- membership of the 35 degree-4 L-monomials, 3 engines
        kb, sing_mem = singular_query(A, L3, (3, 4, 5), 4)
        rec["singular_kbase"] = kb
        rec["singular_matches_exact_codim"] = all(
            kb.get(d) == codim[d] for d in (3, 4, 5))
        table, ag12, ag13 = {}, True, True
        for a, b in B.l_monomials(4):
            nm = B.lmono_name(a, b)
            m = B.lmono_poly(a, b, A)
            zero = not m
            e1_ = True if zero else E4.contains(int_vec(B.to_vec(m, 4)))
            e2_ = sing_mem[nm]
            pv = B.apolar(phi, m)
            e3_ = (pv == 0)
            table[nm] = {"zero_poly": zero, "E1_exact_rref": e1_,
                         "E2_singular": e2_, "E3_phi_criterion": e3_,
                         "phi_pairing": str(pv)}
            ag12 &= (e1_ == e2_)
            ag13 &= (e1_ == e3_)
        rec["membership"] = table
        rec["E1_equals_E2"] = ag12
        rec["PHI_LAW_HOLDS"] = ag13
        rec["excluded_true"] = sorted(k for k, v in table.items()
                                      if not v["E1_exact_rref"])
        rec["excluded_by_phi"] = sorted(k for k, v in table.items()
                                        if not v["E3_phi_criterion"])

        # ---------- C3: does the DET law survive at h = 3, degree 4?
        dp = B.det_poly()
        detmatch, wit_a, wit_b = True, [], []
        for a, b in B.l_monomials(4):
            nm = B.lmono_name(a, b)
            m = B.lmono_poly(a, b, A)
            dcrit = (B.apply_op(dp, m) == {})
            truth = table[nm]["E1_exact_rref"]
            if dcrit != truth:
                detmatch = False
                (wit_a if (dcrit and not truth) else wit_b).append(nm)
        rec["det_criterion_matches_degree4"] = detmatch
        rec["det_says_in_but_is_out"] = sorted(wit_a)
        rec["det_says_out_but_is_in"] = sorted(wit_b)

        results.append(rec)
        print(f"  {label:24s} [{prov}] rank {rk} det {str(dt):>7}: "
              f"codim {codim}  phi in perp {rec['phi_perp_to_all_J4_generators']}"
              f"  phi spans {rec['phi_spans_perp']}  E1=E2 "
              f"{ag12}  PHI LAW {ag13}  disc/phi {ratio}"
              f"  detlaw@4 {detmatch}  [{time.time()-t1:.1f}s]")

    full = [r for r in results if r["rank_A"] == 3]
    summary = {
        "claim": "C2 h=3 phi law + C3 det law at h=3",
        "matrices": len(results), "full_rank": len(full),
        "full_rank_all_codim4_eq_1": all(r["codim_exact"][4] == 1
                                         for r in full),
        "full_rank_all_phi_in_perp": all(r["phi_perp_to_all_J4_generators"]
                                         for r in full),
        "full_rank_all_phi_spans": all(r["phi_spans_perp"] for r in full),
        "full_rank_all_phi_law_holds": all(r["PHI_LAW_HOLDS"] for r in full),
        "all_E1_equals_E2": all(r["E1_equals_E2"] for r in results),
        "all_singular_codim_agrees": all(r["singular_matches_exact_codim"]
                                         for r in results),
        "all_disc_identity_up_to_detA2": all(
            r["ratio_equals_detA_squared"] for r in full),
        "codim4_by_rank": {r["label"]: [r["rank_A"], r["codim_exact"][4]]
                           for r in results},
        "det_law_at_h3_deg4_holds_anywhere": any(
            r["det_criterion_matches_degree4"] for r in results),
        "seconds": round(time.time() - t0, 1)}
    print("\n  SUMMARY:", json.dumps(summary, indent=1))
    with open(HERE + "/b9_c2_phi.json", "w") as fh:
        json.dump({"summary": summary, "results": results}, fh, indent=1)
    print("  wrote b9_c2_phi.json")


if __name__ == "__main__":
    main()

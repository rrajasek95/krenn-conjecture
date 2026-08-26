#!/usr/bin/env python3
"""AUDIT A6-B10 check 3: mandatory mutation-control ledger.

(i)   rank-one query WITHOUT the Rabinowitsch saturation factor -> answer must
      change on at least one pair (saturation is load-bearing).
(ii)  corrupt one quadric (a) add a constant, (b) drop one of the 3 matchings
      from every E_w -> verdict must flip on at least one pair.
(iii) Singular dim() convention: dim(std(ideal(1))) == -1, dim(std(ideal(0)))
      == nvars, and a homogeneous non-unit ideal has dim >= 0.
(iv)  hand-made source with an OBVIOUS rank-one witness (all R_ab killed by a
      rank-one cap) -> checker must say YES, and the witness is verified by
      direct exact evaluation in Python, independently of Singular.
"""
from __future__ import annotations

from fractions import Fraction
import json
import sys

HERE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a6-w15w14-2026-08-15")
P2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-p2-2026-08-15")
sys.path.insert(0, HERE)
import b10_core as B  # noqa: E402

WITNESS_PAIRS = [(1002, (2, 5)), (1005, (0, 5)), (1005, (4, 5)),
                 (1008, (0, 3)), (1008, (1, 2))]
BLOCKED_PAIRS = [(1000, (0, 1)), (1001, (2, 3)), (1003, (1, 4)),
                 (1006, (0, 5)), (1007, (3, 4))]


def load_pair(seed, pq, modes):
    return B.Pair(B.gen_source(seed, modes[seed]), pq[0], pq[1])


def main():
    p2 = json.load(open(P2 + "/results_a.json"))
    modes = {r["seed"]: r["mode"] for r in p2["results"]}
    ledger = {}

    # ---------------- (iii) dim() convention controls (do these first)
    conv = []
    out, dt, st = B.run_singular(
        'ring RC=0,(x,y,z),dp;\n'
        'ideal one=1;      "CTRL unit "+string(dim(std(one)));\n'
        'ideal zed=0;      "CTRL zero "+string(dim(std(zed)));\n'
        'ideal hom=x*y,y*z; "CTRL hom "+string(dim(std(hom)));\n'
        'ideal pt=x-1,y-2,z-3; "CTRL point "+string(dim(std(pt)));\n'
        'ideal emp=x-1,x;  "CTRL inconsistent "+string(dim(std(emp)));')
    for line in out.splitlines():
        f = line.split()
        if f and f[0] == "CTRL":
            conv.append((f[1], int(f[-1])))
    conv = dict(conv)
    ledger["iii_dim_convention"] = {
        "raw": conv,
        "unit_ideal_is_minus1": conv.get("unit") == -1,
        "zero_ideal_is_nvars": conv.get("zero") == 3,
        "point_is_0": conv.get("point") == 0,
        "inconsistent_is_minus1": conv.get("inconsistent") == -1,
        "homogeneous_nonunit_geq0": conv.get("hom", -99) >= 0}
    print("[iii] dim convention:", ledger["iii_dim_convention"])

    # ---------------- (i) saturation is load-bearing
    sat_rows = []
    for seed, pq in BLOCKED_PAIRS + WITNESS_PAIRS:
        pd = load_pair(seed, pq, modes)
        tag = f"{seed}_{pq[0]}{pq[1]}"
        with_sat, d1, t1, _ = B.decide(pd, tag, "rk1", saturate=True)
        no_sat, d2, t2, _ = B.decide(pd, tag, "rk1", saturate=False)
        sat_rows.append({"seed": seed, "pair": list(pq),
                         "rank_one_with_saturation": with_sat, "dim_sat": d1,
                         "rank_one_without_saturation": no_sat,
                         "dim_nosat": d2, "changed": with_sat != no_sat})
        print(f"[i] {seed} {pq}: rk1 sat={with_sat}(dim {d1}) "
              f"nosat={no_sat}(dim {d2}) changed={with_sat != no_sat}")
    ledger["i_saturation"] = {"rows": sat_rows,
                              "n_changed": sum(r["changed"] for r in sat_rows),
                              "passes": any(r["changed"] for r in sat_rows)}

    # ---------------- (ii) corrupted quadrics
    mut_rows = []
    for seed, pq in WITNESS_PAIRS + BLOCKED_PAIRS:
        pd = load_pair(seed, pq, modes)
        tag = f"{seed}_{pq[0]}{pq[1]}"
        base_g, _, _, _ = B.decide(pd, tag, "gen")
        base_r, _, _, _ = B.decide(pd, tag, "rk1")
        # (a) add a constant +1 to the first quadric
        mutA = [dict(Q) for Q in pd.quadrics]
        if mutA:
            mutA[0][None] = Fraction(1)
        # (b) drop the third matching from every word
        mutB = []
        for w in pd.words:
            quad = {}
            for e in B.matchings_of(pd.U)[:2]:
                f1 = pd.R_lin(e[0][0], e[0][1], w)
                f2 = pd.R_lin(e[1][0], e[1][1], w)
                if B.lin_zero(f1) or B.lin_zero(f2):
                    continue
                B.quad_add(quad, B.lin_prod(f1, f2))
            if quad:
                mutB.append(quad)
        a_g = a_r = None
        if mutA:
            a_g, _, _, _ = B.decide(pd, tag, "gen", quadrics=mutA)
            a_r, _, _, _ = B.decide(pd, tag, "rk1", quadrics=mutA)
        b_g, _, _, _ = B.decide(pd, tag, "gen", quadrics=mutB)
        b_r, _, _, _ = B.decide(pd, tag, "rk1", quadrics=mutB)
        row = {"seed": seed, "pair": list(pq),
               "base_general": base_g, "base_rank_one": base_r,
               "addconst_general": a_g, "addconst_rank_one": a_r,
               "dropmatch_general": b_g, "dropmatch_rank_one": b_r,
               "addconst_flips": (a_g != base_g) or (a_r != base_r),
               "dropmatch_flips": (b_g != base_g) or (b_r != base_r)}
        mut_rows.append(row)
        print(f"[ii] {seed} {pq}: base(g={base_g},r={base_r}) "
              f"+const(g={a_g},r={a_r}) dropM(g={b_g},r={b_r}) "
              f"flips: const={row['addconst_flips']} "
              f"drop={row['dropmatch_flips']}")
    ledger["ii_mutations"] = {
        "rows": mut_rows,
        "n_addconst_flips": sum(r["addconst_flips"] for r in mut_rows),
        "n_dropmatch_flips": sum(r["dropmatch_flips"] for r in mut_rows),
        "passes": any(r["addconst_flips"] or r["dropmatch_flips"]
                      for r in mut_rows)}

    # ---------------- (iv) hand-made source with an obvious rank-one witness
    #  p=0, q=1, U={2,3,4,5}.  Take u = v = (1,1,1).
    #  Kill every R_ab by making v^T (oriented block q->a) = 0, i.e. every
    #  column of block(q,a,.,.) sums to zero.  Blocks p->a stay generic, so the
    #  quadrics are NOT identically zero.  A_pq = identity => u^T A v = 3 != 0.
    p, q = 0, 1
    blocks = {pr: [[Fraction(0)] * 3 for _ in range(3)] for pr in B.ALLPAIRS}
    blocks[(0, 1)] = [[Fraction(1), Fraction(0), Fraction(0)],
                      [Fraction(0), Fraction(1), Fraction(0)],
                      [Fraction(0), Fraction(0), Fraction(1)]]
    colkill = [[Fraction(1), Fraction(2), Fraction(-3)],
               [Fraction(-1), Fraction(1), Fraction(1)],
               [Fraction(0), Fraction(-3), Fraction(2)]]   # columns sum to 0
    pblocks = [[Fraction(1), Fraction(2), Fraction(3)],
               [Fraction(0), Fraction(1), Fraction(-1)],
               [Fraction(2), Fraction(1), Fraction(1)]]
    for a in (2, 3, 4, 5):
        # block q->a oriented (row = colour at q): columns must sum to zero
        blocks[(min(q, a), max(q, a))] = (
            colkill if q < a else [[colkill[j][i] for j in range(3)]
                                   for i in range(3)])
        blocks[(min(p, a), max(p, a))] = (
            pblocks if p < a else [[pblocks[j][i] for j in range(3)]
                                   for i in range(3)])
    # a nonzero block among the U-sites, to be sure x_e are alive (unused at h=2)
    blocks[(2, 3)] = [[Fraction(1), Fraction(1), Fraction(0)],
                      [Fraction(0), Fraction(1), Fraction(1)],
                      [Fraction(1), Fraction(0), Fraction(1)]]
    pd = B.Pair(blocks, p, q)
    u = [Fraction(1)] * 3
    v = [Fraction(1)] * 3
    K = [u[i] * v[j] for i in range(3) for j in range(3)]
    direct = all(sum(c * K[m] * K[n] for (m, n), c in Q.items()) == 0
                 for Q in pd.quadrics)
    s_val = sum(pd.s[n] * K[n] for n in range(9))
    kappas = [K[0], K[4], K[8]]
    g, gd, _, _ = B.decide(pd, "handmade", "gen")
    r, rd, _, _ = B.decide(pd, "handmade", "rk1")
    ledger["iv_handmade"] = {
        "n_quadrics": len(pd.quadrics),
        "quadrics_nonempty": len(pd.quadrics) > 0,
        "explicit_K_kills_all_quadrics_in_python": direct,
        "s_at_K": str(s_val), "kappas_at_K": [str(x) for x in kappas],
        "b10_general_verdict": g, "b10_rank_one_verdict": r,
        "dims": [gd, rd],
        "passes": bool(direct and len(pd.quadrics) > 0 and r and g
                       and s_val != 0 and all(k != 0 for k in kappas))}
    print("[iv] hand-made:", ledger["iv_handmade"])

    # negative twin of (iv): same source but A_pq made orthogonal to u,v so
    # that s(K) = 0 at the obvious cap -> the obvious cap is NOT a witness.
    blocks2 = {k: [row[:] for row in m] for k, m in blocks.items()}
    blocks2[(0, 1)] = [[Fraction(1), Fraction(-1), Fraction(0)],
                       [Fraction(0), Fraction(1), Fraction(-1)],
                       [Fraction(-1), Fraction(0), Fraction(1)]]
    pd2 = B.Pair(blocks2, p, q)
    s2 = sum(pd2.s[n] * K[n] for n in range(9))
    g2, _, _, _ = B.decide(pd2, "handmade2", "gen")
    r2, _, _, _ = B.decide(pd2, "handmade2", "rk1")
    ledger["iv_handmade_twin"] = {"s_at_obvious_K": str(s2),
                                  "general": g2, "rank_one": r2}
    print("[iv-twin] s(K)=0 variant:", ledger["iv_handmade_twin"])

    ledger["ALL_CONTROLS_PASS"] = bool(
        ledger["i_saturation"]["passes"] and ledger["ii_mutations"]["passes"]
        and ledger["iii_dim_convention"]["unit_ideal_is_minus1"]
        and ledger["iv_handmade"]["passes"])
    print("\nALL_CONTROLS_PASS:", ledger["ALL_CONTROLS_PASS"])
    json.dump(ledger, open(HERE + "/b10_controls.json", "w"), indent=1,
              default=str)
    print("wrote b10_controls.json")


if __name__ == "__main__":
    main()

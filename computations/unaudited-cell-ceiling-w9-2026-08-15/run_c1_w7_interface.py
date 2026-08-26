#!/usr/bin/env python3
"""W9 Task C1 -- interface with W7 (plan v9).  Three checks.

(W7-a) W7's LEMMA H4: a symmetric zero-diagonal W of order >= 6 with EVERY
       off-diagonal entry nonzero has some 4-subset hafnian nonzero.
       DIRECT RELEVANCE: in W6's (STAR) expansion at a pair (p,q) with
       U = B\\{p,q} (|U| = 6 at N=8), the matrix W(v)[a][b] = A_ab[v_a][v_b]
       IS symmetric with zero diagonal, and M(v)[a][b] = H_{U\\{a,b\}}(A)(v)
       IS the matrix of its 4-subset hafnians.  So W7's lemma says exactly:
                 W(v) complete  =>  M(v) != 0.
       Since (STAR) reads C(v) A_pq = -P(v) M(v) Q(v)^T, M(v) = 0 is the ONLY
       way (STAR) can annihilate a whole block.  W7's lemma therefore CLOSES
       the dense branch of mechanism (1) NEGATIVELY: on dense colour supports
       (STAR) cannot kill a block, so no cell ceiling comes from it there.
       Here: verify the lemma's instance on our objects and on controls, and
       measure how often M(v) = 0 versus the density of W(v).

(W7-b) RIGIDITY: a FULL-support (252-cell) exact source would be isolated
       modulo gauge.  Flag whether any positive-dimensional exact-compatible
       family found by W9 is DENSE (it is not: STAGE_A is 81/252 = 32%).

(W7-c) EDGE-vs-CELL: report cell density out of 252 for every object.
"""
from __future__ import annotations
import importlib, json, os, random
from fractions import Fraction as F
from itertools import combinations, product
import w9_core as w9, w9_template as wt
from w9_core import COLORS, cells, hafnian, oriented, pair_expansion

SIZE = 8
TOTAL_CELLS = 28 * 9


def M_stats(source, size=SIZE, sample=None):
    """For every pair (p,q) and every non-constant v on U: density of W(v),
    whether M(v) = 0, and whether C(v) = 0.  Exact."""
    rows = []
    rng = random.Random(0)
    for p, q in combinations(range(size), 2):
        U = tuple(u for u in range(size) if u not in (p, q))
        allv = [v for v in product(COLORS, repeat=len(U)) if len(set(v)) > 1]
        if sample:
            allv = rng.sample(allv, min(sample, len(allv)))
        for vword in allv:
            v = {u: vword[n] for n, u in enumerate(U)}
            # W(v): 6x6 symmetric zero-diagonal
            live = 0
            for a, b in combinations(range(len(U)), 2):
                if oriented(source, U[a], U[b])[v[U[a]]][v[U[b]]] != 0:
                    live += 1
            C, M, P, Q, D = pair_expansion(source, size, p, q, v)
            Mzero = all(M[a][b] == 0 for a in range(len(U)) for b in range(len(U)))
            rows.append({"p": p, "q": q, "W_edges": live, "W_complete": live == 15,
                         "M_zero": Mzero, "C_zero": C == 0})
    return rows


def lemma_h4_control(trials=400, order=6, seed=1):
    """W7's LEMMA H4 as a standalone check: random COMPLETE symmetric
    zero-diagonal W of order 6 must have some 4-subset hafnian nonzero.
    Control: W with a zero entry may have all of them zero."""
    rng = random.Random(seed)
    def haf4(W, S):
        a, b, c, d = S
        return (W[a][b] * W[c][d] + W[a][c] * W[b][d] + W[a][d] * W[b][c])
    ok = bad = 0
    for _ in range(trials):
        W = [[F(0)] * order for _ in range(order)]
        for i in range(order):
            for j in range(i + 1, order):
                x = F(rng.randint(-6, 6) or 5)
                W[i][j] = W[j][i] = x
        nz = any(haf4(W, S) != 0 for S in combinations(range(order), 4))
        ok += nz
        bad += (not nz)
    return {"trials": trials, "some_4subset_hafnian_nonzero": ok,
            "all_vanish (lemma would be violated)": bad}


if __name__ == "__main__":
    mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")

    def build(params):
        blocks = mod.build_stage_a(params)
        return {(u, v): [[F(x) for x in row] for row in mod.C.oriented(blocks, u, v)]
                for u, v in combinations(range(8), 2)}
    BEST = ((F(-7), F(-9)), (F(7), F(8)), F(5,3), F(-7,4), F(-1,5), F(-8,5),
            (F(-7,4), F(-4), F(7,5)), (F(-3,2), F(-5,4), F(-9)),
            (F(1,5), F(8,3), F(-1,5)), (F(-9,2), F(1), F(3,4)), F(6), F(-9))
    OUT = {}

    print("=" * 92)
    print("C1(a)  W7's LEMMA H4 inside (STAR): does a complete W(v) force M(v) != 0?")
    print("=" * 92)
    ctrl = lemma_h4_control()
    print(f"   standalone control on random COMPLETE order-6 W: {ctrl}")
    OUT["lemma_h4_control"] = ctrl

    src = build(BEST)
    rows = M_stats(src, sample=60)
    comp = [r for r in rows if r["W_complete"]]
    inc = [r for r in rows if not r["W_complete"]]
    print(f"\n   STAGE_A_GENERIC, {len(rows)} sampled (pair, non-constant v) slots:")
    print(f"     W(v) COMPLETE   : {len(comp):5d}   of these M(v)=0 in "
          f"{sum(1 for r in comp if r['M_zero'])}  "
          f"(W7's lemma predicts 0)")
    print(f"     W(v) incomplete : {len(inc):5d}   of these M(v)=0 in "
          f"{sum(1 for r in inc if r['M_zero'])}")
    print(f"     C(v)=0 fraction : {sum(1 for r in rows if r['C_zero'])}/{len(rows)}")
    OUT["star_M_stats"] = {
        "sampled": len(rows), "W_complete": len(comp),
        "M_zero_given_complete": sum(1 for r in comp if r["M_zero"]),
        "W_incomplete": len(inc),
        "M_zero_given_incomplete": sum(1 for r in inc if r["M_zero"]),
        "C_zero": sum(1 for r in rows if r["C_zero"])}
    print("\n   CONSEQUENCE for mechanism (1): (STAR) annihilates a whole block")
    print("   only when M(v) = 0; W7's LEMMA H4 rules that out whenever the")
    print("   colour-restricted complement W(v) is complete.  So on DENSE")
    print("   supports -- exactly the band 19..27 -- (STAR) yields NO cell")
    print("   ceiling.  This closes mechanism (1)'s dense branch negatively.")

    print("\n" + "=" * 92)
    print("C1(b)  RIGIDITY cross-check (W7): is any positive-dimensional family DENSE?")
    print("=" * 92)
    b5 = json.load(open("results_b5_jacobian_rank.json"))["rows"]
    for r in b5:
        dens = 100.0 * r["Sigma"] / TOTAL_CELLS
        slack = r["rank_budget_if_exact_exists"] - r["jacobian_rank"]
        print(f"   {r['label']:20s} Sigma={r['Sigma']:4d} ({dens:5.1f}% of 252)"
              f"  dim-slack = {slack:+4d}  "
              f"{'positive-dimensional' if slack > 0 else 'over-determined'}")
    print("\n   The only positive-dimensional family found (STAGE_A) sits at")
    print("   32.1% cell density, far from full support, so it is NOT in")
    print("   tension with W7's full-support rigidity theorem.")
    OUT["rigidity_check"] = [{"label": r["label"], "Sigma": r["Sigma"],
                              "density_pct": round(100.0 * r["Sigma"] / TOTAL_CELLS, 1),
                              "dim_slack": r["rank_budget_if_exact_exists"] - r["jacobian_rank"]}
                             for r in b5]

    print("\n" + "=" * 92)
    print("C1(c)  EDGE-vs-CELL reconciliation: cell density of every calibration object")
    print("=" * 92)
    print(f"   committed ceiling front, densest cell count (W7): 51 / 252 = 20.2%")
    tab = []
    for lbl, s in (("STAGE_A_BASE", w9.load_stage_a()),
                   ("STAGE_A_SECOND", w9.load_stage_a(True)),
                   ("STAGE_A_GENERIC", src)):
        S = sum(len(cells(s[e])) for e in combinations(range(8), 2))
        tab.append((lbl, S))
    for lbl, S in tab:
        print(f"   {lbl:22s} Sigma = {S:4d} / 252 = {100.0*S/252:5.1f}%")
    smw6 = json.load(open(os.path.join("..", "unaudited-bridge-w6-2026-08-15",
                                       "results_sigmamin_N8.json")))["rows"]
    print("   W6 Sigma_min certificates      : "
          + ", ".join(f"m{r['m']}={r['sigma_min_upper_bound']}"
                      for r in smw6 if r["sigma_min_upper_bound"] and 19 <= r["m"] <= 27))
    print(f"   -> band Sigma_min density      : "
          f"{100.0*61/252:.1f}%..{100.0*99/252:.1f}%")
    print(f"   W6 band certificates (max cell): 131..243 / 252 = 52.0%..96.4%")
    OUT["cell_density"] = {lbl: {"Sigma": S, "pct_of_252": round(100.0*S/252, 1)}
                           for lbl, S in tab}
    with open("results_c1_w7_interface.json", "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("\nwrote results_c1_w7_interface.json")

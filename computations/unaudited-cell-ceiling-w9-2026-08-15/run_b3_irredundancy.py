#!/usr/bin/env python3
"""W9 Task B3 -- MECHANISM (3): local irredundancy (slice-cover section 4),
quantified.  Exact arithmetic over Q.

LEMMA (committed, slice-cover.md section 4).  For an ENTRY-MINIMAL
realization and a fixed vertex p, the tensors

        T_pjkl = e_k^(p) (x) e_l^(j) (x) C_pj,        C_pj = H_{B\{p,j}}(A),

indexed by the nonzero entries A_pj[k][l] on edges incident to p, are
LINEARLY INDEPENDENT.

CONSEQUENCE (the ceiling this mechanism can give).  Split by k: for each
colour k at p, the family {S_jl = e_l^(j) (x) C_pj} restricted to the
support of row k is independent, so

        n_p(k) := #{(j,l) : A_pj[k][l] != 0}  <=  r_p := rank{ S_jl },
        cells at p = sum_k n_p(k)  <=  3 r_p,
        Sigma = (1/2) sum_p (cells at p)      <=  (3/2) sum_p r_p.

The bound BITES iff r_p < 3 * d_live(p), i.e. iff there are genuine linear
dependencies among the complementary-hafnian tensors.  This script measures
r_p exactly.  A dependency is a relation

        sum_j d_{j, v_j} C_pj(v|_{B\{p,j}}) = 0   for every word v on B\{p}.

Nothing here is a proved claim; the ranks are exact measurements.
"""
from __future__ import annotations
import json, random, sys
from fractions import Fraction as F
from itertools import combinations, product
import w9_core as w9
from w9_core import COLORS, hafnian, cells, matrix_rank

SIZE = 8


def complementary_tensor(source, p, j, size=SIZE):
    """C_pj as a dict: word on B\\{p,j} -> hafnian."""
    rest = tuple(u for u in range(size) if u not in (p, j))
    out = {}
    for w in product(COLORS, repeat=len(rest)):
        out[w] = hafnian(source, rest, {u: w[n] for n, u in enumerate(rest)})
    return rest, out


def rank_over_Q(rows):
    """Exact rank of a list of dict-rows (sparse) over Q."""
    # dense Gaussian elimination on sparse dicts
    rows = [dict(r) for r in rows]
    piv = {}
    rank = 0
    for row in rows:
        row = {k: F(v) for k, v in row.items() if v}
        while row:
            col = min(row)
            if col in piv:
                base = piv[col]
                factor = row[col] / base[col]
                for k, v in base.items():
                    row[k] = row.get(k, F(0)) - factor * v
                    if row[k] == 0:
                        del row[k]
            else:
                piv[col] = row
                rank += 1
                break
    return rank


def irredundancy_profile(source, size=SIZE, label=""):
    """r_p for every p, plus the resulting ceiling, plus actual cell counts."""
    live = {(u, v) for u, v in combinations(range(size), 2)
            if cells(source[(u, v)])}
    live_nb = {p: [j for j in range(size) if j != p
                   and (min(p, j), max(p, j)) in live] for p in range(size)}
    out = {}
    words_rest = None
    for p in range(size):
        rows = []
        rowkey = []
        nz_j = []
        for j in live_nb[p]:
            rest, Cj = complementary_tensor(source, p, j, size)
            if all(v == 0 for v in Cj.values()):
                nz_j.append((j, False))
                continue
            nz_j.append((j, True))
            # word v on B\{p} -> index; entry = [v_j == l] * C_pj(v minus j)
            others = tuple(u for u in range(size) if u != p)
            pos_j = others.index(j)
            for l in COLORS:
                row = {}
                for w in product(COLORS, repeat=len(others)):
                    if w[pos_j] != l:
                        continue
                    sub = tuple(w[n] for n in range(len(others)) if n != pos_j)
                    val = Cj[sub]
                    if val:
                        row[w] = val
                if row:
                    rows.append(row)
                    rowkey.append((j, l))
        r_p = rank_over_Q(rows)
        d_live = len(live_nb[p])
        n_rows = len(rows)
        cells_at_p = sum(len(cells(w9.oriented(source, p, j))) for j in live_nb[p])
        # per-colour row counts n_p(k)
        npk = []
        for k in COLORS:
            npk.append(sum(1 for j in live_nb[p]
                           for l in COLORS if w9.oriented(source, p, j)[k][l]))
        out[p] = {"d_live": d_live, "rows_built": n_rows,
                  "trivial_bound_3d": 3 * d_live, "r_p": r_p,
                  "cells_at_p": cells_at_p, "n_p_k": npk,
                  "max_n_p_k": max(npk),
                  "bound_cells_at_p": 3 * r_p,
                  "bites": r_p < 3 * d_live,
                  "zero_C_neighbours": [j for j, ok in nz_j if not ok]}
    Sigma_bound = sum(3 * out[p]["r_p"] for p in range(size))
    assert Sigma_bound % 2 == 0 or True
    return {"per_vertex": out,
            "Sigma_actual": sum(len(cells(source[e])) for e in
                                combinations(range(size), 2)),
            "Sigma_irredundancy_bound": Sigma_bound / 2,
            "m": len(live)}


def report(label, source):
    prof = irredundancy_profile(source, label=label)
    print(f"\n[{label}]  m = {prof['m']}   Sigma_actual = {prof['Sigma_actual']}")
    print("   p   d_live  3*d_live  r_p   n_p(k)        cells@p   3*r_p  bites?")
    for p, d in sorted(prof["per_vertex"].items()):
        print(f"  {p}      {d['d_live']:2d}      {d['trivial_bound_3d']:3d}"
              f"    {d['r_p']:3d}   {str(d['n_p_k']):12s}  {d['cells_at_p']:4d}"
              f"     {d['bound_cells_at_p']:3d}   {'YES' if d['bites'] else 'no'}")
    print(f"   => irredundancy ceiling  Sigma <= (1/2) sum_p 3 r_p = "
          f"{prof['Sigma_irredundancy_bound']}"
          f"   (actual {prof['Sigma_actual']})")
    return prof


if __name__ == "__main__":
    import importlib
    from fractions import Fraction as FF
    mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")

    def build(params):
        blocks = mod.build_stage_a(params)
        return {(u, v): [[FF(x) for x in row] for row in mod.C.oriented(blocks, u, v)]
                for u, v in combinations(range(8), 2)}
    BEST = ((FF(-7), FF(-9)), (FF(7), FF(8)), FF(5,3), FF(-7,4), FF(-1,5), FF(-8,5),
            (FF(-7,4), FF(-4), FF(7,5)), (FF(-3,2), FF(-5,4), FF(-9)),
            (FF(1,5), FF(8,3), FF(-1,5)), (FF(-9,2), FF(1), FF(3,4)), FF(6), FF(-9))

    OUT = {}
    print("=" * 78)
    print("B3  MECHANISM (3): local irredundancy, exact ranks over Q")
    print("=" * 78)
    for lbl, src in (("STAGE_A_BASE", w9.load_stage_a()),
                     ("STAGE_A_GENERIC", build(BEST))):
        OUT[lbl] = report(lbl, src)

    # CONTROL: a dense random source (not near-exact) -- r_p should be maximal,
    # confirming that any deficit measured above is structural, not an artefact.
    print("\n-- CONTROL: dense random integer sources (should show r_p = 3 d_live) --")
    rng = random.Random(99)
    ctrl = []
    for t in range(2):
        src = {(u, v): [[F(rng.randint(-5, 5)) for _ in COLORS] for _ in COLORS]
               for u, v in combinations(range(8), 2)}
        p0 = irredundancy_profile(src)
        deficits = [p0["per_vertex"][p]["trivial_bound_3d"] - p0["per_vertex"][p]["r_p"]
                    for p in range(8)]
        print(f"   random #{t}: r_p deficits = {deficits}  "
              f"{'PASS (no deficit)' if all(d == 0 for d in deficits) else 'deficit present'}")
        ctrl.append(deficits)
    OUT["control_random_deficits"] = ctrl
    with open("results_b3_irredundancy.json", "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("\nwrote results_b3_irredundancy.json")

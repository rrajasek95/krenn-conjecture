#!/usr/bin/env python3
"""W9 Task A4 -- cell census of W1's 37 stall points (N = 6).

NOTE ON W1's FIELD NAMES: in results_push.json, structure.support_size counts
CELLS (values 11..61 at N=6, where there are only 15 edges); the block count
is the sum of structure.kinds over the non-'zero' classes.  So for W1's data
        Sigma = structure.support_size,   m = 15 - kinds['zero'].

This is the direct empirical test of H4's intuition ("exactness forces cell
sparsity"): plot Sigma against the number of mixed equations satisfied.
"""
from __future__ import annotations
import json, os
W1 = os.path.join("..", "unaudited-witness-splitting-w1-2026-08-15")
blob = json.load(open(os.path.join(W1, "results_push.json")))
print("=" * 104)
print("A4  W1 stall points (N=6): Sigma vs mixed satisfaction  [726 mixed equations]")
print("=" * 104)
print(f"{'id':12s} {'stratum':9s} {'m':>3} {'Sigma':>6} {'Sigma/m':>8}"
      f" {'mixed sat':>10} {'frac':>7} {'singletons':>11} {'suppMixed':>10}")
rows = []
for rec in sorted(blob["results"], key=lambda r: r["base"]["structure"]["support_size"]):
    st, ex = rec["base"]["structure"], rec["base"]["exactness"]
    m = sum(v for k, v in st["kinds"].items() if k != "zero")
    S = st["support_size"]
    rows.append({"id": rec["id"], "stratum": rec["stratum"], "m": m, "Sigma": S,
                 "sigma_over_m": round(S / m, 3),
                 "mixed_satisfied": ex["mixed_satisfied"],
                 "mixed_fraction": ex["mixed_satisfied_fraction"],
                 "singletons": ex["singleton_mixed_fibres"],
                 "supported_mixed_words": ex.get("supported_mixed_words"),
                 "kinds": st["kinds"]})
    print(f"{rec['id']:12s} {rec['stratum']:9s} {m:3d} {S:6d} {S/m:8.2f}"
          f" {ex['mixed_satisfied']:10d} {ex['mixed_satisfied_fraction']:7.3f}"
          f" {ex['singleton_mixed_fibres']:11d}"
          f" {str(ex.get('supported_mixed_words')):>10}")

lo = [r for r in rows if r["Sigma"] <= 25]
hi = [r for r in rows if r["Sigma"] >= 50]
print(f"\ncell-POOR  (Sigma <= 25, n={len(lo)}): mean mixed satisfaction "
      f"{sum(r['mixed_fraction'] for r in lo)/max(1,len(lo)):.3f}, "
      f"mean Sigma/m {sum(r['sigma_over_m'] for r in lo)/max(1,len(lo)):.2f}")
print(f"cell-RICH  (Sigma >= 50, n={len(hi)}): mean mixed satisfaction "
      f"{sum(r['mixed_fraction'] for r in hi)/max(1,len(hi)):.3f}, "
      f"mean Sigma/m {sum(r['sigma_over_m'] for r in hi)/max(1,len(hi)):.2f}")
print("\nREADING.  The trade-off H4 hopes for is REAL but far too soft: at N=6")
print("the cell-poorest objects reach 95-99.9% of the mixed system while the")
print("cell-richest reach 0.4-52%.  Nothing here caps Sigma; what it caps is")
print("the ACHIEVED SATISFACTION, i.e. it is the overdetermination effect of")
print("task B4/B5, not a cell ceiling.")
with open("results_a4_w1_census.json", "w") as fh:
    json.dump({"stall_points": rows}, fh, indent=1, default=str)
print("\nwrote results_a4_w1_census.json")

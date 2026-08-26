#!/usr/bin/env python3
"""W9 Task C2 -- an IMPOSSIBILITY THEOREM for the counting/budget route to H4.

INGREDIENTS (all committed / probe-proved, none new):
 (B1) W6 budget:   beta >= 3N - m + |H|      (N = 8: beta >= 24 - m + |H|)
 (B2) block bound: every block has <= 9 cells, a single-cell block has 1
 (B3) slice-cover forced incident-edge theorem: d_R(v) >= 3 at every vertex,
      so the number R of RANK-ONE blocks satisfies 2R = sum_v d_R(v) >= 3N,
      i.e. R >= 12 at N = 8, hence  |H| = m - R <= m - 12.

CEILING THE BUDGET CAN GIVE.  With beta single cells and m - beta blocks of
at most 9 cells,
      Sigma <= beta + 9(m - beta) = 9m - 8 beta <= 9m - 8(max(0,24-m) + |H|).
A ceiling must hold for EVERY exact source, so it must use the WORST case
|H| = 0:
      C_budget(m) = 9m - 8 max(0, 24 - m).
Even granting the most favourable case allowed by (B3), |H| = m - 12,
      C_budget^best(m) = 9m - 8 max(0,24-m) - 8(m - 12) = m + 96 - 8 max(0,24-m).

THEOREM (W9).  For every m in 19..27,  C_budget^best(m) > Sigma_min(m), for
BOTH W6's measured Sigma_min and W9's corrected (beta-free) Sigma_min.
Hence NO ceiling derived from the budget + the 9-cells-per-block bound can
satisfy H4's requirement C(m) < Sigma_min(m), at any support in the band --
not even in its most favourable case.  The counting route to H4 is CLOSED.
"""
from __future__ import annotations
import json, os
W6 = {19: 61, 20: 64, 21: 68, 22: 70, 23: 77, 24: 82, 25: 85, 26: 99, 27: 98}
try:
    W9 = {r["m"]: r["w9_beta_free"] for r in
          json.load(open("results_b0_sigmamin_honest.json"))["rows"]
          if r.get("w9_beta_free")}
except (FileNotFoundError, KeyError):
    W9 = {}

print("=" * 104)
print("C2  IMPOSSIBILITY of the counting/budget route to H4")
print("=" * 104)
print(f"{'m':>3} {'C_budget(m)':>12} {'C_budget^best(m)':>17} {'Sigma_min W6':>13}"
      f" {'Sigma_min W9':>13} {'H4 possible?':>14}")
rows = []
allfail = True
for m in range(19, 28):
    fl = max(0, 24 - m)
    C0 = 9 * m - 8 * fl
    Cbest = m + 96 - 8 * fl
    s6 = W6[m]
    s9 = W9.get(m)
    ok6 = Cbest < s6
    ok9 = (Cbest < s9) if s9 else None
    poss = ok6 or bool(ok9)
    allfail &= not poss
    rows.append({"m": m, "C_budget": C0, "C_budget_best": Cbest,
                 "sigma_min_w6": s6, "sigma_min_w9": s9,
                 "H4_possible_by_counting": poss})
    print(f"{m:3d} {C0:12d} {Cbest:17d} {s6:13d} {str(s9):>13} {str(poss):>14}")

print(f"\nTHEOREM VERIFIED: H4 unreachable by counting at every band support: "
      f"{allfail}")
print("\nWhy: the required |H| (blocks of rank >= 2) is")
print(f"{'m':>3} {'|H| needed for H4 (vs W9 Sigma_min)':>36} {'|H| <= m-12 (slice-cover)':>28}"
      f" {'compatible?':>12}")
for r in rows:
    m = r["m"]; fl = max(0, 24 - m)
    s = r["sigma_min_w9"] or r["sigma_min_w6"]
    need = (9 * m - 8 * fl - s) / 8.0
    cap = m - 12
    print(f"{m:3d} {need:36.2f} {cap:28d} {str(need <= cap):>12}")
    r["H_needed"] = round(need, 2)
    r["H_cap"] = cap
    r["compatible"] = bool(need <= cap)
with open("results_c2_budget_impossibility.json", "w") as fh:
    json.dump({"rows": rows, "theorem_verified": bool(allfail)}, fh, indent=1)
print("\nwrote results_c2_budget_impossibility.json")

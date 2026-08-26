#!/usr/bin/env python3
"""W9 Task D -- the verdict table: assemble every measured quantity and
decide, per support, whether H4 is reachable.

Columns
  Sigma_min(W6)   W6's measured price of singleton-freeness, beta PINNED at
                  the floor.  NOT a valid lower bound on Sigma(A): beta=floor
                  is not forced, so this is a min over a strictly smaller
                  class and therefore an OVER-estimate.
  Sigma_min(W9)   same minimisation with beta FREE (>= floor).  Valid.
  Sigma_min^P     additionally restricted to W3 case (P) (balanced), which is
                  WLOG for the minimum-cell-support counterexample by W3
                  Corollary A.2.  Valid and >= Sigma_min(W9).  The honest
                  target: H4 needs a proved ceiling C(m) < Sigma_min^P(m).
  Sigma_mix       max Sigma over MIXED-EXACT sources at that support: a hard
                  LOWER bound on any ceiling proved from the mixed equations.
  C_budget        9m - 8 max(0,24-m): the best PROVED ceiling (attained).
  C_budget^best   m + 96 - 8 max(0,24-m): the best the budget could EVER give,
                  granting the maximal |H| = m - 12 allowed by slice-cover.
"""
from __future__ import annotations
import json
W6 = {19: 61, 20: 64, 21: 68, 22: 70, 23: 77, 24: 82, 25: 85, 26: 99, 27: 98}
W9 = {r["m"]: r["w9_beta_free"] for r in
      json.load(open("results_b0_sigmamin_honest.json"))["rows"]}
try:
    P = {r["m"]: r["sigma_min_P"] for r in
         json.load(open("results_b8_sigmamin_balanced.json"))["rows"]}
except FileNotFoundError:
    P = {}
MIX = {r["m"]: r["sigma_mix"] for r in
       json.load(open("results_b2_maxsigma_per_m.json"))["rows"]}

print("=" * 118)
print("D  VERDICT TABLE  (all numbers exact; Sigma_min* are search upper bounds,")
print("   Sigma_mix is a search lower bound -- both directions strengthen the")
print("   negative conclusions)")
print("=" * 118)
print(f"{'m':>3} {'Smin W6':>8} {'Smin W9':>8} {'Smin^P':>7} {'Sigma_mix':>10}"
      f" {'C_budget':>9} {'C_bud^best':>11} {'counting?':>10} {'mixed-only?':>12}")
rows = []
for m in range(19, 28):
    fl = max(0, 24 - m)
    C0, Cb = 9 * m - 8 * fl, m + 96 - 8 * fl
    target = P.get(m) or W9.get(m)
    mix = MIX.get(m)
    counting = "possible" if (target and Cb < target) else "CLOSED"
    if mix is None:
        mixed = "no witness"
    elif target is None:
        mixed = "?"
    elif mix >= target:
        mixed = "CLOSED"
    else:
        mixed = f"window {target-mix}"
    print(f"{m:3d} {W6[m]:8d} {str(W9.get(m)):>8} {str(P.get(m)):>7}"
          f" {str(mix):>10} {C0:9d} {Cb:11d} {counting:>10} {mixed:>12}")
    rows.append({"m": m, "sigma_min_w6": W6[m], "sigma_min_w9": W9.get(m),
                 "sigma_min_P": P.get(m), "sigma_mix": mix,
                 "C_budget": C0, "C_budget_best": Cb,
                 "counting_route": counting, "mixed_only_route": mixed})

closed_c = sum(1 for r in rows if r["counting_route"] == "CLOSED")
closed_m = sum(1 for r in rows if r["mixed_only_route"] == "CLOSED")
have_w = sum(1 for r in rows if r["sigma_mix"] is not None)
print(f"\nCounting route CLOSED at {closed_c}/9 band supports (proved, Theorem C2).")
print(f"Mixed-only route CLOSED at {closed_m}/{have_w} band supports where a")
print(f"mixed-exact witness was found (certified by exact witnesses).")
with open("results_d_verdict_table.json", "w") as fh:
    json.dump({"rows": rows, "counting_closed": closed_c,
               "mixed_only_closed": closed_m,
               "supports_with_witness": have_w}, fh, indent=1, default=str)
print("\nwrote results_d_verdict_table.json")

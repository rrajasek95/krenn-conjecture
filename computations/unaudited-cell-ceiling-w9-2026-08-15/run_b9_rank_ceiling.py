#!/usr/bin/env python3
"""W9 Task B9 -- MECHANISM (4): the honest constant from RANK ARITHMETIC,
and the proof that it is TIGHT (hence not improvable by counting).

What rank arithmetic actually gives.
  * a rank-r 3x3 block needs >= r cells -- a LOWER bound, useless for a ceiling;
  * a rank-ONE block can still carry all 9 cells (a (x) b with a,b full), so
    rank gives NO upper bound per block;
  * the only proved UPPER-bound ingredient is W6's budget
        beta >= 3N - m + |H| single-cell blocks   (N=8: beta >= 24 - m + |H|),
    giving
        Sigma <= 1*beta + 9*(m - beta) = 9m - 8 beta
              <= 9m - 8*max(0, 24 - m + |H|)
              =  17m - 192 - 8|H|   (m <= 24),      9m   (m >= 24).
  * W5's "<= 16 full-rank pairs" holds only in the DIAGONAL regime, which
    W6 already kills at every support 12..27 -- so it adds nothing here.
  * W9/B3's local-irredundancy ranks give (3/2) sum_p r_p; with only the
    proved inequality r_p <= 3 d_live(p) this is exactly the trivial 9m
    (the measured deficits, 192 at STAGE_A, are not a theorem).

TIGHTNESS TEST.  W6's own band certificates are the maximal-cell templates
at floor beta.  If they are ADMISSIBLE (singleton-free, three pure fibres,
all 24 slots, min degree >= 3) then the ceiling 9m - 8*beta_floor is
ATTAINED, so no sharpening of the counting argument can lower it.
"""
from __future__ import annotations
import json, os, sys
from fractions import Fraction as F
from itertools import combinations
import w9_core as w9
import w9_template as wt

EDGES = tuple(combinations(range(8), 2))
SIGMA_MIN_W6 = w9.SIGMA_MIN


def proved_ceiling(m, H=0):
    beta = max(0, 24 - m + H)
    return 9 * m - 8 * beta


print("=" * 100)
print("B9  MECHANISM (4): the honest proved cell ceiling, and its tightness")
print("=" * 100)
print(f"{'m':>3} {'proved C(m)=9m-8*beta_floor':>28} {'Sigma_min (W6)':>15}"
      f" {'ratio C/Sigma_min':>18} {'H4 needs C <':>13}")
rows = []
for m in range(19, 28):
    C = proved_ceiling(m)
    sm = SIGMA_MIN_W6[m]
    rows.append({"m": m, "proved_ceiling": C, "sigma_min_w6": sm,
                 "ratio": round(C / sm, 3)})
    print(f"{m:3d} {C:28d} {sm:15d} {C/sm:18.2f} {sm:13d}")

print("\n-- TIGHTNESS: are W6's band certificates (the max-cell templates at")
print("   floor beta) ADMISSIBLE?  If yes the ceiling is attained. --")
band = json.load(open(os.path.join("..", "unaudited-bridge-w6-2026-08-15",
                                   "results_band_certificates.json")))


def walk(o):
    if isinstance(o, dict):
        if isinstance(o.get("template"), list) and len(o["template"]) == 28:
            yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


print(f"{'m':>3} {'Sigma':>6} {'proved C(m)':>12} {'attained?':>10}"
      f" {'singleton-free':>15} {'pure fibres':>16} {'slots':>7} {'minDeg':>7}")
tight = []
seen = set()
for o in walk(band):
    T = {EDGES[n]: frozenset(tuple(c) for c in s)
         for n, s in enumerate(o["template"])}
    a = wt.audit(T)
    m = a["m"]
    if m in seen or not (19 <= m <= 27):
        continue
    seen.add(m)
    C = proved_ceiling(m)
    att = a["Sigma"] == C
    ok = (a["S_singleton_free"] and not a["T4_missing_pures"]
          and a["T5_min_degree_ok"] and a["T6_slots_ok"])
    print(f"{m:3d} {a['Sigma']:6d} {C:12d} {str(att):>10}"
          f" {str(a['S_singleton_free']):>15} {str(a['T4_pure_fibres']):>16}"
          f" {a['slots_covered']:4d}/24 {a['min_degree']:7d}")
    tight.append({"m": m, "Sigma": a["Sigma"], "proved_ceiling": C,
                  "attained": bool(att), "admissible": bool(ok),
                  "singleton_free": a["S_singleton_free"],
                  "pure_fibres": a["T4_pure_fibres"],
                  "slots": a["slots_covered"], "min_degree": a["min_degree"]})

good = [t for t in tight if t["attained"] and t["admissible"]]
print(f"\n=> the proved ceiling is ATTAINED by an ADMISSIBLE template at "
      f"{len(good)} of {len(tight)} supports in the band: "
      f"{sorted(t['m'] for t in good)}")
print("   At those supports no sharpening of the counting argument can lower")
print("   C(m) below 9m - 8*beta_floor, so H4 is out of reach by counting alone.")
with open("results_b9_rank_ceiling.json", "w") as fh:
    json.dump({"ceiling_table": rows, "tightness": tight}, fh, indent=1, default=str)
print("\nwrote results_b9_rank_ceiling.json")

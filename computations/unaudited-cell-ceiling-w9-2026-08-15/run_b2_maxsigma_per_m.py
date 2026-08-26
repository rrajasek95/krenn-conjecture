#!/usr/bin/env python3
"""W9 Task B2 -- Sigma_mix(m) := max Sigma over MIXED-EXACT eight-site sources
of support m.  This is the exact obstruction number for H4:

  any ceiling C(m) proved from the MIXED equations alone (that is: (STAR)
  pinning, W5's L1/L2 laws and attachment criterion, W6's support criterion,
  the h=3 permanent dictionary -- every tool in the campaign that does not
  use the three PURE equations at the VALUE level) must satisfy
            C(m) >= Sigma_mix(m),
  while H4 demands C(m) <= Sigma_min(m) - 1.
  So H4 is UNREACHABLE by mixed-only arguments at every m with
            Sigma_mix(m) >= Sigma_min(m).

Search: the STAGE_A closed-form family (12 exact rational parameters), whose
every member is mixed-exact by construction (verified per point, exactly).
Parameter choice is a search (labelled); every verdict is exact arithmetic.
"""
from __future__ import annotations
import importlib, json, random, sys
from fractions import Fraction as F
from itertools import combinations
import w9_core as w9, w9_template as wt
from w9_core import COLORS, cells

mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")


def build(params):
    blocks = mod.build_stage_a(params)
    return {(u, v): [[F(x) for x in row] for row in mod.C.oriented(blocks, u, v)]
            for u, v in combinations(range(8), 2)}


def mk(rng, zero_bias=0.0):
    """Random exact rational parameters; zero_bias injects zeros to lower m."""
    def r():
        if rng.random() < zero_bias:
            return F(0)
        return F(rng.randint(-9, 9) or 3, rng.randint(1, 4))
    def rnz():
        while True:
            x = r()
            if x:
                return x
    return ((r(), r()), (r(), r()), rnz(), rnz(), rnz(), rnz(),
            (r(), r(), r()), (r(), r(), r()),
            (r(), r(), r()), (r(), r(), r()), rnz(), rnz())


SIGMA_MIN = w9.SIGMA_MIN
best = {}
rng = random.Random(11)
TRIALS = 4000
print("=" * 78)
print(f"B2  Sigma_mix(m): max Sigma over mixed-exact sources ({TRIALS} exact points)")
print("=" * 78)
for t in range(TRIALS):
    zb = [0.0, 0.15, 0.3, 0.45][t % 4]
    p = mk(rng, zb)
    try:
        src = build(p)
    except ZeroDivisionError:
        continue
    c = w9.full_census(src)
    m, S = c["m"], c["Sigma"]
    if m not in best or S > best[m][0]:
        best[m] = (S, p, c)

print("\n   m   Sigma_mix(found)  Sigma_min(W6)  Sigma_mix - Sigma_min   VERDICT at m")
rows = []
for m in sorted(best):
    S, p, c = best[m]
    sm = SIGMA_MIN.get(m)
    if sm is None:
        print(f"  {m:2d}      {S:4d}            --")
        continue
    d = S - sm
    verdict = ("H4 UNREACHABLE by mixed-only args" if d >= 0
               else f"window [{S},{sm-1}] width {sm - S}")
    print(f"  {m:2d}      {S:4d}            {sm:4d}          {d:+4d}"
          f"          {verdict}")
    rows.append({"m": m, "sigma_mix": S, "sigma_min_w6": sm, "delta": d,
                 "verdict": verdict})

# ---- exact verification of every recorded maximum ------------------------
print("\n-- EXACT verification of each Sigma_mix witness --")
detail = {}
for m in sorted(best):
    S, p, c = best[m]
    src = build(p)
    defs = w9.defect_words(src)
    mixed_bad = sum(1 for w in defs if len(set(w)) > 1)
    tpl = wt.template_of(src)
    aud = wt.audit(tpl)
    print(f"  m={m:2d} Sigma={S:3d} | mixed defects {mixed_bad} | pure fibres "
          f"{aud['T4_pure_fibres']} | singleton-free {aud['S_singleton_free']}"
          f" | slots {aud['slots_covered']}/24 | beta {aud['beta']}"
          f" | minDeg {aud['min_degree']}")
    detail[str(m)] = {"Sigma": S, "params": str(p), "mixed_defects": mixed_bad,
                      "defect_words": sorted("".join(map(str, w)) for w in defs),
                      "audit": {k: v for k, v in aud.items()
                                if k != "mixed_fibre_histogram"},
                      "kinds": c["kinds"],
                      "cell_histogram": {str(k): v for k, v in c["cell_histogram"].items()}}

with open("results_b2_maxsigma_per_m.json", "w") as fh:
    json.dump({"rows": rows, "detail": detail, "trials": TRIALS}, fh,
              indent=1, default=str)
print("\nwrote results_b2_maxsigma_per_m.json")

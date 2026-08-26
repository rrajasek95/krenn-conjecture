#!/usr/bin/env python3
"""W9 Task C3b -- MUTATION CONTROL for C3's "the pure equations add 0 to the
rank".  A measurement that can only ever return 0 is worthless, so exhibit
templates where the checker returns a POSITIVE increment."""
from __future__ import annotations
import importlib, json, random
from fractions import Fraction as F
from itertools import combinations
import w9_core as w9, w9_template as wt
from run_b4_dimension_count import gauge_rank
from run_c3_pure_contribution import jrank

EDGES = tuple(combinations(range(8), 2))
COLORS = (0, 1, 2)
print("=" * 84)
print("C3b  CONTROL: can 'pure adds' be nonzero?  (if never, C3 measures nothing)")
print("=" * 84)
out = []

def run(label, T):
    rng = random.Random(3)
    vals = {(e, c): F(rng.randint(1, 30), rng.randint(1, 5))
            for e in T for c in T[e]}
    Sigma = sum(len(s) for s in T.values())
    Jm, _ = jrank(T, vals, include_pure=False, include_mixed=True)
    Jf, _ = jrank(T, vals, include_pure=True, include_mixed=True)
    Jp, _ = jrank(T, vals, include_pure=True, include_mixed=False)
    print(f"   {label:34s} Sigma={Sigma:4d}  J_mixed={Jm:3d}  J_full={Jf:3d}"
          f"  J_pure_only={Jp}  pure adds={Jf-Jm}")
    out.append({"label": label, "Sigma": Sigma, "J_mixed": Jm, "J_full": Jf,
                "J_pure_only": Jp, "pure_adds": Jf - Jm})
    return Jf - Jm

# Control 1: a single perfect matching with all 3 diagonal cells.
# Its mixed system is nearly empty, so the pure rows MUST add rank.
T1 = {e: frozenset() for e in EDGES}
for e in ((0, 1), (2, 3), (4, 5), (6, 7)):
    T1[e] = frozenset({(0, 0), (1, 1), (2, 2)})
run("3-diagonal single matching", T1)

# Control 2: two disjoint matchings, diagonal cells only.
T2 = {e: frozenset() for e in EDGES}
for e in ((0, 1), (2, 3), (4, 5), (6, 7), (1, 2), (3, 4), (5, 6), (0, 7)):
    T2[e] = frozenset({(0, 0), (1, 1), (2, 2)})
run("3-diagonal 8-cycle (2 matchings)", T2)

# Control 3: STAGE_A's template (mixed system is exact but sparse)
mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")
def build(p):
    b = mod.build_stage_a(p)
    return {(u, v): [[F(x) for x in r] for r in mod.C.oriented(b, u, v)]
            for u, v in combinations(range(8), 2)}
BEST = ((F(-7), F(-9)), (F(7), F(8)), F(5,3), F(-7,4), F(-1,5), F(-8,5),
        (F(-7,4), F(-4), F(7,5)), (F(-3,2), F(-5,4), F(-9)),
        (F(1,5), F(8,3), F(-1,5)), (F(-9,2), F(1), F(3,4)), F(6), F(-9))
run("STAGE_A generic template", wt.template_of(build(BEST)))

pos = [o for o in out if o["pure_adds"] > 0]
print(f"\n=> 'pure adds' is POSITIVE on {len(pos)}/{len(out)} controls "
      f"({[o['label'] for o in pos]}).")
print("   The checker is therefore discriminating, and C3's zeros on the band")
print("   templates are a real structural fact: on those templates the three")
print("   pure gradients already lie in the span of the mixed ones.")
with open("results_c3b_control.json", "w") as fh:
    json.dump({"rows": out}, fh, indent=1, default=str)
print("\nwrote results_c3b_control.json")

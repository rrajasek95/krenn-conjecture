#!/usr/bin/env python3
"""W9 Task A3 -- audit STAGE_A's TEMPLATE against W6's Sigma_min conditions.

THEOREM (trivial but decisive).  If a source is mixed-exact (H_w = 0 for
every non-constant w) then its template has NO mixed singleton: a singleton
fibre would make H_w the single nonzero product of nonzero cells.
So every mixed-exact source's template is an admissible witness for the
"cell price of singleton-freeness" -- IF it also meets W6's other
feasibility conditions.  This script checks which ones it meets.
"""
from __future__ import annotations
import importlib, json, random
from fractions import Fraction as F
from itertools import combinations
import w9_core as w9, w9_template as wt
from w9_core import COLORS

mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")

def build(params):
    blocks = mod.build_stage_a(params)
    return {(u, v): [[F(x) for x in row] for row in mod.C.oriented(blocks, u, v)]
            for u, v in combinations(range(8), 2)}

BEST = ((F(-7), F(-9)), (F(7), F(8)), F(5,3), F(-7,4), F(-1,5), F(-8,5),
        (F(-7,4), F(-4), F(7,5)), (F(-3,2), F(-5,4), F(-9)),
        (F(1,5), F(8,3), F(-1,5)), (F(-9,2), F(1), F(3,4)), F(6), F(-9))

OUT = {}
print("="*76)
print("A3  TEMPLATE audit: is a mixed-exact source an admissible Sigma_min witness?")
print("="*76)

for label, src in (("STAGE_A_BASE", w9.load_stage_a()),
                   ("STAGE_A_SECOND", w9.load_stage_a(True)),
                   ("STAGE_A_GENERIC(max Sigma)", build(BEST))):
    tpl = wt.template_of(src)
    a = wt.audit(tpl)
    # cross-check: mixed exactness of the numeric source
    mixed_bad = w9.mixed_defect_count(src)
    print(f"\n[{label}]")
    print(f"   numeric mixed defects        : {mixed_bad}  (0 == mixed-exact)")
    print(f"   m = {a['m']}   Sigma = {a['Sigma']}   beta = {a['beta']}")
    print(f"   (S)  mixed singletons        : {a['S_mixed_singletons']}"
          f"   -> singleton-free = {a['S_singleton_free']}")
    print(f"   (T4) pure fibre counts       : {a['T4_pure_fibres']}"
          f"   missing pures = {a['T4_missing_pures']}")
    print(f"   (T5) min degree              : {a['min_degree']} (>=3? {a['T5_min_degree_ok']})")
    print(f"   (T6) slots covered           : {a['slots_covered']}/{a['slots_needed']}"
          f"  ok = {a['T6_slots_ok']}")
    print(f"   mixed fibre histogram        : {a['mixed_fibre_histogram']}")
    sm = w9.SIGMA_MIN.get(a['m'])
    print(f"   Sigma_min({a['m']}) as measured by W6 = {sm}"
          f"   ;  this object's Sigma = {a['Sigma']}")
    if a['S_singleton_free'] and a['T5_min_degree_ok'] and a['T6_slots_ok']:
        if not a['T4_missing_pures']:
            print(f"   >>> FULLY ADMISSIBLE: improves Sigma_min({a['m']}) to <= {a['Sigma']}"
                  if sm and a['Sigma'] < sm else
                  f"   >>> FULLY ADMISSIBLE (Sigma {a['Sigma']} vs measured {sm})")
        else:
            print(f"   >>> admissible except (T4): it is MISSING pures {a['T4_missing_pures']}")
    a["numeric_mixed_defects"] = mixed_bad
    a["sigma_min_measured"] = sm
    OUT[label] = a

with open("results_a3_template_audit.json", "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
print("\nwrote results_a3_template_audit.json")

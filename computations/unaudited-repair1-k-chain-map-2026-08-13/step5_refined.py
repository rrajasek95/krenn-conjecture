#!/usr/bin/env python3
"""STEP 5: the fine-shift-REFINED comparison, and what would pin K.

The operator solution's D2 shadow is not just a total: it splits over the
fine shifts of the operator block (the committed checker already reports
nonzero_fine_shift_shadow_count = 2).  The physical side splits over the
fine degrees (= words) of the presentation.  Here we
  (a) compute both splittings and test whether they MATCH cross-module;
  (b) redo the membership problem against the refined target;
  (c) test which further readouts collapse the residual freedom.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations
import json
import pickle

import common as C

m = C.modules()
base, cm = m["base"], m["commutator"]
CORNERS = cm.CORNERS
PURE, MIXED = cm.PURE_WORD, cm.MIXED_WORD

state = pickle.load(open("operator_state.pkl", "rb"))
cols, shifts = state["columns"], state["shifts"]
solution = {k: Q(a, b) for k, (a, b) in state["solution"].items()}

# (a) operator-side fine-shift resolution of D2(u)
shadow_by_shift = defaultdict(Counter)
for idx, coeff in solution.items():
    sh = repr(shifts[idx])
    for row, val in cols[idx][1].items():
        if row[0] == 2:
            shadow_by_shift[sh][row[1]] += coeff * val
shadow_by_shift = {k: Counter({p: v for p, v in c.items() if v})
                   for k, c in shadow_by_shift.items()}
shadow_by_shift = {k: c for k, c in shadow_by_shift.items() if c}

out = {"operator_nonzero_fine_shift_components": len(shadow_by_shift),
       "operator_component_supports": sorted(len(c) for c in
                                             shadow_by_shift.values())}

# (b) physical-side word-graded shadow of K_phys
K_phys = Counter({c: Q(a) for c, a in zip(CORNERS, cm.ALPHA)})
pure_part = Counter({k: v for k, v in K_phys.items()
                     if k in set(C.physical_row(base, PURE))})
mixed_part = Counter({k: v for k, v in K_phys.items()
                      if k in set(C.physical_row(base, MIXED))})
phys_components = {}
for name, part in (("pure_word_grade", pure_part),
                   ("mixed_word_grade", mixed_part)):
    sh = C.shadow2(part)
    phys_components[name] = Counter({p: v for (_k, p), v in sh.items()})
out["physical_component_supports"] = {k: len(v) for k, v in
                                      phys_components.items()}

# do the two splittings agree as unordered sets of components?
op_set = sorted((sorted((repr(p), str(v)) for p, v in c.items())
                 for c in shadow_by_shift.values()), key=repr)
ph_set = sorted((sorted((repr(p), str(v)) for p, v in c.items())
                 for c in phys_components.values()), key=repr)
out["fine_shift_splitting_matches_word_grade_splitting"] = op_set == ph_set
out["component_pairing"] = []
for sh, comp in sorted(shadow_by_shift.items()):
    match = [name for name, pc in phys_components.items() if pc == comp]
    out["component_pairing"].append({"operator_fine_shift": sh,
                                     "support": len(comp),
                                     "matching_physical_grade": match})

# (c) refined membership: solve grade by grade in the two-row inventory
def solve_block(words, target_pairs):
    mons, seen = [], set()
    for w in words:
        for mon in C.physical_row(base, w):
            if mon not in seen:
                seen.add(mon)
                mons.append(mon)
    colsW = [{(2, p): Q(1) for p in C.shadow2_of_monomial(mon)}
             for mon in mons]
    tgt = {(2, p): Q(v) for p, v in target_pairs.items()}
    feas, sol, kern, rank, sep = C.solve_exact(colsW, tgt)
    return mons, colsW, feas, sol, kern, rank, sep


refined = {}
total_free = 0
free_blocks = {}
for name, word in (("pure_word_grade", PURE), ("mixed_word_grade", MIXED)):
    mons, colsW, feas, sol, kern, rank, sep = solve_block(
        [word], phys_components[name])
    refined[name] = {"monomials": len(mons), "rank": rank,
                     "feasible": feas,
                     "freedom": len(kern) if feas else None}
    total_free += len(kern) if feas else 0
    free_blocks[name] = (mons, kern)
out["refined_grade_by_grade"] = refined
out["refined_total_freedom"] = total_free

# (d) what pins?  test further readout families on the refined freedom
def test_families(mons, kern):
    index = {mon: j for j, mon in enumerate(mons)}

    def rank_of(constraints):
        rows = []
        for f in constraints:
            row = {}
            for i, kv in enumerate(kern):
                val = sum(c * kv.get(index[mon], Q(0))
                          for mon, c in f.items() if mon in index)
                if val:
                    row[i] = val
            if row:
                rows.append(row)
        r, _ = C.rref_rank(rows)
        return r

    fam = {}
    # triple-cell shadow (subsets of size three)
    buckets = defaultdict(dict)
    for mon in mons:
        for tri in combinations(mon, 3):
            buckets[tuple(sorted(tri))][mon] = Q(1)
    fam["triple_cell_shadow"] = list(buckets.values())
    # single cells
    buckets = defaultdict(dict)
    for mon in mons:
        for cell in mon:
            buckets[cell][mon] = Q(1)
    fam["single_cell_shadow"] = list(buckets.values())
    # underlying (uncoloured) matching readout
    buckets = defaultdict(dict)
    for mon in mons:
        buckets[tuple(sorted((a, b) for a, b, _c, _d in mon))][mon] = Q(1)
    fam["uncoloured_matching_readout"] = list(buckets.values())
    # literal full-nine boundary features (base-file constructor, one
    # multiplier): monomial -> sorted(multiplier + monomial); injective.
    mult = base.matching_monomial(((1, 2), (3, 4)), {1: 0, 2: 0, 3: 0, 4: 0})
    buckets = defaultdict(dict)
    for mon in mons:
        buckets[tuple(sorted(mult + mon))][mon] = Q(1)
    fam["literal_full_nine_boundary_feature"] = list(buckets.values())
    return {k: {"rows": len(v), "rank_on_freedom": rank_of(v),
                "residual_freedom": len(kern) - rank_of(v)}
            for k, v in fam.items()}


out["pinning_tests"] = {}
for name, (mons, kern) in free_blocks.items():
    if kern:
        out["pinning_tests"][name] = test_families(mons, kern)

json.dump(out, open("step5_refined.json", "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))

#!/usr/bin/env python3
"""STEP 6: characterise the residual freedom and the operator's own split.

(1) Exhibit the residual freedom of the membership problem after ALL
    committed readout families, with explicit vectors.
(2) Ask whether the operator's two fine-shift D2 components are even
    PHYSICALLY REALISABLE separately (a pair of cells coming from a
    matching monomial must be disjoint and colour-consistent).
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

out = {}

# ---------------------------------------------------------------- (1)
mons, seen = [], set()
for w in (PURE, MIXED):
    for mon in C.physical_row(base, w):
        if mon not in seen:
            seen.add(mon)
            mons.append(mon)
index = {mon: j for j, mon in enumerate(mons)}
cols = [{(2, p): Q(1) for p in C.shadow2_of_monomial(mon)} for mon in mons]
target = {(2, p): Q(v) for p, v in cm.expected_second_shadow().items()}
feas, sol, kern, rank, sep = C.solve_exact(cols, target)
assert feas

families = []
# s-odd, w-odd, corner residue, row augmentation, fine-degree, single cell
seenp = set()
for mon in mons:
    img, _ = C.s_act(mon)
    key = tuple(sorted((mon, img)))
    if key in seenp:
        continue
    seenp.add(key)
    f = Counter({mon: Q(1)})
    f[img] += Q(1)
    families.append({k: v for k, v in f.items() if v})
seenp = set()
for mon in mons:
    img, sg = C.w_act(mon)
    key = tuple(sorted((mon, img)))
    if key in seenp:
        continue
    seenp.add(key)
    f = Counter({mon: Q(1)})
    f[img] += Q(sg)
    families.append({k: v for k, v in f.items() if v})
for c in CORNERS:
    families.append({c: Q(1)})
for w in (PURE, MIXED):
    families.append({mon: Q(1) for mon in C.physical_row(base, w)})
buckets = defaultdict(dict)
for mon in mons:
    for cell in mon:
        buckets[cell][mon] = Q(1)
families.extend(buckets.values())

# restrict the kernel to the joint null space of all families
# Restrict the freedom to the joint null space of every committed readout.
# Columns are indexed by kernel coordinate, rows by readout functional.
constraint_columns = []
for i, kv in enumerate(kern):
    col = {}
    for fi, f in enumerate(families):
        val = sum(c * kv.get(index[mon], Q(0)) for mon, c in f.items())
        if val:
            col[("readout", fi)] = val
    constraint_columns.append(col)
ok, _p, nullbasis, r, _sep = C.solve_exact(constraint_columns, {})
assert ok
resid = []
for vec in nullbasis:
    chain = Counter()
    for i, x in vec.items():
        for j, y in kern[i].items():
            chain[mons[j]] += x * y
    chain = Counter({k: v for k, v in chain.items() if v})
    assert chain, "degenerate residual vector"
    resid.append(chain)

out["raw_freedom"] = len(kern)
out["rank_of_all_committed_readouts_on_freedom"] = r
out["residual_freedom_after_all_readouts"] = len(resid)
out["residual_vectors"] = []
for chain in resid:
    dens = {v.denominator for v in chain.values()}
    sh = C.shadow2(chain)
    sK = C.act_on_chain(chain, C.s_act)
    wK = C.act_on_chain(chain, C.w_act)
    out["residual_vectors"].append({
        "support": len(chain),
        "denominators": sorted(dens),
        "shadow2_is_zero": not sh,
        "s_odd": sK == Counter({k: -v for k, v in chain.items()}),
        "w_odd": wK == Counter({k: -v for k, v in chain.items()}),
        "corner_values": [str(chain.get(c, Q(0))) for c in CORNERS],
        "pure_row_terms": sum(1 for k in chain
                              if k in set(C.physical_row(base, PURE))),
        "mixed_row_terms": sum(1 for k in chain
                               if k in set(C.physical_row(base, MIXED))),
    })
example = resid[0]
out["example_residual_vector"] = sorted(
    (repr(k), str(v)) for k, v in example.items())
# sanity: K_phys + example has the identical compared signature
K_phys = Counter({c: Q(a) for c, a in zip(CORNERS, cm.ALPHA)})
alt = Counter(K_phys)
alt.update(example)
alt = Counter({k: v for k, v in alt.items() if v})
out["alternative_K_has_identical_shadow"] = (
    C.shadow2(alt) == C.shadow2(K_phys))
out["alternative_K_support"] = len(alt)
out["alternative_K_is_s_odd_and_w_odd"] = (
    C.act_on_chain(alt, C.s_act) == Counter({k: -v for k, v in alt.items()})
    and C.act_on_chain(alt, C.w_act) == Counter({k: -v for k, v in alt.items()}))
out["alternative_K_corner_residue"] = [str(alt.get(c, Q(0))) for c in CORNERS]

# ---------------------------------------------------------------- (2)
state = pickle.load(open("operator_state.pkl", "rb"))
cols_op, shifts = state["columns"], state["shifts"]
solution = {k: Q(a, b) for k, (a, b) in state["solution"].items()}
by_shift = defaultdict(Counter)
for idx, coeff in solution.items():
    for row, val in cols_op[idx][1].items():
        if row[0] == 2:
            by_shift[repr(shifts[idx])][row[1]] += coeff * val
by_shift = {k: Counter({p: v for p, v in c.items() if v})
            for k, c in by_shift.items()}
by_shift = {k: c for k, c in by_shift.items() if c}


def pair_is_physical(pair):
    (a1, b1, _c1, _d1), (a2, b2, _c2, _d2) = pair
    if len({a1, b1, a2, b2}) != 4:
        return False
    if frozenset((a1, b1)) == base.DIRECT_FREE_PAIR:
        return False
    if frozenset((a2, b2)) == base.DIRECT_FREE_PAIR:
        return False
    return True


comp = []
for key, c in sorted(by_shift.items()):
    phys = sum(1 for p in c if pair_is_physical(p))
    comp.append({
        "fine_shift": key,
        "support": len(c),
        "physically_realisable_pairs": phys,
        "non_physical_pairs": len(c) - phys,
        "values": sorted({str(v) for v in c.values()}),
    })
out["operator_fine_shift_components"] = comp
total = Counter()
for c in by_shift.values():
    total.update(c)
total = Counter({k: v for k, v in total.items() if v})
out["operator_total_support"] = len(total)
out["operator_total_all_pairs_physical"] = all(pair_is_physical(p)
                                               for p in total)

json.dump(out, open("step6_characterise.json", "w"), indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in out.items()
                  if k != "example_residual_vector"},
                 indent=1, sort_keys=True))

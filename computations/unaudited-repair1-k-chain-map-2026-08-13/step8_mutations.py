#!/usr/bin/env python3
"""STEP 8: mutation controls.

Every positive claim above is re-run against a deliberately corrupted input;
a claim that survives its own mutation is content-free.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations
import json
import pickle
import random

import common as C

m = C.modules()
base, cm = m["base"], m["commutator"]
CORNERS = cm.CORNERS
PURE, MIXED = cm.PURE_WORD, cm.MIXED_WORD
K_phys = Counter({c: Q(a) for c, a in zip(CORNERS, cm.ALPHA)})
op_d2 = {k: Q(a, b) for k, (a, b) in
         {k: v for k, v in pickle.load(open("operator_state.pkl", "rb"))["d2"].items()}.items()}
# rebuild row keys from repr is unsafe; recompute the operator D2 directly
state = pickle.load(open("operator_state.pkl", "rb"))
cols_op = state["columns"]
solution = {k: Q(a, b) for k, (a, b) in state["solution"].items()}
D2 = Counter()
for idx, co in solution.items():
    for row, val in cols_op[idx][1].items():
        if row[0] == 2:
            D2[row] += co * val
D2 = Counter({k: v for k, v in D2.items() if v})

out = {}

# --- M1 mutate alpha -------------------------------------------------------
res = []
for mut in ((-1, 1, 1, 1), (1, 1, 1, -1), (-1, 1, -1, 1), (-2, 1, 1, -1)):
    ch = Counter({c: Q(a) for c, a in zip(CORNERS, mut)})
    res.append({"alpha": list(mut),
                "shadow_equals_operator_D2": C.shadow2(ch) == D2})
out["M1_mutated_alpha"] = res

# --- M2 mutate the involution ---------------------------------------------
res = []
for a, b in combinations(range(8), 2):
    swap = {a: b, b: a}
    img, _ = C.s_act(CORNERS[0], swap)
    seed = Counter({CORNERS[0]: Q(1)})
    step = C.act_on_chain(seed, C.w_act)
    step.subtract(seed)
    step = Counter({k: v for k, v in step.items() if v})
    K = Counter(step)
    K.subtract(C.act_on_chain(step, lambda mon: C.s_act(mon, swap)))
    K = Counter({k: v for k, v in K.items() if v})
    ok = (K == K_phys)
    stays_in_presentation = all(
        mon in set(C.physical_row(base, PURE)) | set(C.physical_row(base, MIXED))
        for mon in K)
    res.append({"transposition": [a, b], "reproduces_K_phys": ok,
                "image_in_two_active_rows": stays_in_presentation,
                "K_support": len(K)})
out["M2_mutated_endpoint_involution"] = {
    "transpositions_reproducing_K_phys": [r["transposition"] for r in res
                                          if r["reproduces_K_phys"]],
    "count_reproducing": sum(1 for r in res if r["reproduces_K_phys"]),
    "count_total": len(res),
    "detail": res,
}

# --- M3 mutate the tail Weyl sign -----------------------------------------
def w_unsigned(mon):
    img, _sg = C.w_act(mon)
    return img, 1


seed = Counter({CORNERS[0]: Q(1)})
step = C.act_on_chain(seed, w_unsigned)
step.subtract(seed)
step = Counter({k: v for k, v in step.items() if v})
Kbad = Counter(step)
Kbad.subtract(C.act_on_chain(step, C.s_act))
Kbad = Counter({k: v for k, v in Kbad.items() if v})
out["M3_unsigned_weyl"] = {
    "reproduces_K_phys": Kbad == K_phys,
    "alpha": [str(Kbad.get(c, Q(0))) for c in CORNERS],
}

# --- M4/M5 mutated membership targets (negative control on the solver) ----
mons, seen = [], set()
for w in (PURE, MIXED):
    for mon in C.physical_row(base, w):
        if mon not in seen:
            seen.add(mon)
            mons.append(mon)
cols = [{(2, p): Q(1) for p in C.shadow2_of_monomial(mon)} for mon in mons]
target = {k: v for k, v in D2.items()}

trials = []
random.seed(20260813)
# (a) flip the sign of one target entry
keys = sorted(target, key=repr)
for k in keys[:4]:
    t = dict(target)
    t[k] = -t[k]
    feas, _s, kern, rank, sep = C.solve_exact(cols, t)
    trials.append({"mutation": "sign flip on " + repr(k), "feasible": feas,
                   "separator_support": None if feas else len(sep)})
# (b) delete one target entry
for k in keys[:2]:
    t = {kk: vv for kk, vv in target.items() if kk != k}
    feas, _s, kern, rank, sep = C.solve_exact(cols, t)
    trials.append({"mutation": "delete " + repr(k), "feasible": feas,
                   "separator_support": None if feas else len(sep)})
# (c) random target on the same rows
allrows = sorted({r for c in cols for r in c}, key=repr)
for _ in range(3):
    t = {r: Q(random.randint(-2, 2)) for r in random.sample(allrows, 16)}
    t = {r: v for r, v in t.items() if v}
    feas, _s, kern, rank, sep = C.solve_exact(cols, t)
    trials.append({"mutation": "random 16-term target", "feasible": feas,
                   "separator_support": None if feas else len(sep)})
out["M4_membership_negative_controls"] = trials

# --- M6 mutate the shadow functor -----------------------------------------
def shadow3(chain):
    o = Counter()
    for mon, co in chain.items():
        for tri in combinations(mon, 3):
            o[(3, tuple(sorted(tri)))] += co
    return Counter({k: v for k, v in o.items() if v})


out["M6_wrong_shadow_degree"] = {
    "shadow3_of_K_phys_equals_operator_D2": shadow3(K_phys) == D2,
    "shadow3_support": len(shadow3(K_phys)),
}

# --- M7 a different physical chain with the same corner residue -----------
alt = Counter(K_phys)
other = [mon for mon in mons if mon not in CORNERS][:4]
for i, mon in enumerate(other):
    alt[mon] += Q(1 if i % 2 == 0 else -1)
out["M7_perturbed_physical_chain"] = {
    "shadow_equals_operator_D2": C.shadow2(alt) == D2}

json.dump(out, open("step8_mutations.json", "w"), indent=1, sort_keys=True)
print(json.dumps({k: (v if k != "M2_mutated_endpoint_involution"
                      else {kk: vv for kk, vv in v.items() if kk != "detail"})
                  for k, v in out.items()}, indent=1, sort_keys=True))

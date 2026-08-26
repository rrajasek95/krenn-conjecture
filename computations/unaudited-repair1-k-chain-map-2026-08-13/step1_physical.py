#!/usr/bin/env python3
"""STEP 1: rebuild the physical side and the four-corner chain K_phys.

No literal (-1,1,1,-1) is typed here as an input to a comparison: alpha is
taken from the committed constructor and, separately, DERIVED from the
prism identity (1-s)(w-1) acting on the physical corner E+T0.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
import json

import common as C

m = C.modules()
base, cm = m["base"], m["commutator"]

PURE = cm.PURE_WORD
MIXED = cm.MIXED_WORD
CORNERS = cm.CORNERS

out = {}

# --- the committed presentation --------------------------------------------
pure_row = C.physical_row(base, PURE)
mixed_row = C.physical_row(base, MIXED)
assert len(set(pure_row)) == len(set(mixed_row)) == 90
out["pure_row_terms"] = len(pure_row)
out["mixed_row_terms"] = len(mixed_row)
out["corners"] = [repr(c) for c in CORNERS]
out["corner_in_pure_row"] = [c in set(pure_row) for c in CORNERS]
out["corner_in_mixed_row"] = [c in set(mixed_row) for c in CORNERS]

# --- DERIVE alpha physically from (1-s)(w-1) on the corner E+T0 ------------
# The four corners are a single s x w orbit; compute the orbit action on
# the physical matching monomials rather than on a 4x4 typed matrix.
c0 = CORNERS[0]
s_img, s_sign = C.s_act(c0)
w_img, w_sign = C.w_act(c0)
out["s_orbit_of_E+T0"] = repr(s_img)
out["s_sign"] = s_sign
out["w_orbit_of_E+T0"] = repr(w_img)
out["w_sign"] = w_sign
assert s_img == CORNERS[1], "endpoint swap does not carry E+T0 to E-T0"
assert w_img == CORNERS[2], "tail Weyl does not carry E+T0 to E+T1"

# K = (1-s)(w-1) applied to the physical monomial E+T0
seed = Counter({c0: Q(1)})
step = C.act_on_chain(seed, C.w_act)
step.subtract(seed)                    # (w-1)
step = Counter({k: v for k, v in step.items() if v})
K_phys = Counter(step)
K_phys.subtract(C.act_on_chain(step, C.s_act))   # (1-s)
K_phys = Counter({k: v for k, v in K_phys.items() if v})

derived_alpha = tuple(K_phys.get(c, Q(0)) for c in CORNERS)
out["derived_alpha_from_(1-s)(w-1)_on_physical_corner"] = [
    str(v) for v in derived_alpha]
out["K_phys_support"] = len(K_phys)
out["K_phys_equals_alpha_corners"] = (
    K_phys == Counter({c: Q(a) for c, a in zip(CORNERS, cm.ALPHA)}))
out["committed_alpha"] = [str(v) for v in cm.ALPHA]

# --- committed equivariance readouts on K_phys -----------------------------
sK = C.act_on_chain(K_phys, C.s_act)
wK = C.act_on_chain(K_phys, C.w_act)
out["s_odd"] = sK == Counter({k: -v for k, v in K_phys.items()})
out["w_odd"] = wK == Counter({k: -v for k, v in K_phys.items()})

# --- the grade-forgotten pair shadow ---------------------------------------
sh = C.shadow2(K_phys)
expected = {(2, pair): Q(v) for pair, v in cm.expected_second_shadow().items()}
out["shadow2_K_phys_support"] = len(sh)
out["shadow2_K_phys_equals_expected_second_shadow"] = (
    {k: Q(v) for k, v in sh.items()} == expected)
out["expected_second_shadow_support"] = len(expected)

json.dump(out, open("step1_physical.json", "w"), indent=1, sort_keys=True)
for k, v in sorted(out.items()):
    print(f"{k}: {v}")

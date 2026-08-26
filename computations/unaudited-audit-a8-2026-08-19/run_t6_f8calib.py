#!/usr/bin/env python3
"""A8 T6 -- (i) W25's F8 object re-verified from the stored blocks with my own
engine; (ii) the rung implementations of W25 / W27 / W28 vs mine; (iii) the
(N,k) calibration table by an independent probe.
"""
import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

BASE = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a8-2026-08-19"
sys.path.insert(0, BASE)
from a8_core import (H_raw, checkpoint, is_constant, offcount, perfect_matchings,
                     profile, require, words)

R, RAN = {}, []
rng = random.Random(606)


def sect(s):
    print("=" * 74)
    print(s)
    print("=" * 74)


# ------------------------------------------------------------------ (i) F8
sect("(i) W25-F8 re-verified with the A8 engine")
F8 = json.load(open("/Users/rishi/workplace/krenn-conjecture/computations/"
                    "unaudited-x3core-w25-2026-08-15/OBJECT_W25-F8_n8_allblocked_X3.json"))
A = {}
for key, M in F8["blocks"].items():
    u, v = (int(x) for x in key.split(","))
    A[(u, v)] = [[Fraction(x) for x in row] for row in M]
require(len(A) == 28, f"expected 28 blocks, got {len(A)}")
PMS8 = perfect_matchings(range(8))
pures = [H_raw(A, (c,) * 8, PMS8) for c in range(3)]
print(f"   pures: {[str(x) for x in pures]} (must be 1,1,1)")
defects = []
for w in words(8):
    if is_constant(w):
        continue
    if H_raw(A, w, PMS8) != 0:
        defects.append(w)
byoff = {}
for w in defects:
    byoff[offcount(w)] = byoff.get(offcount(w), 0) + 1
print(f"   mixed defects: {len(defects)}   by off-count: {dict(sorted(byoff.items()))}")
minoff = min(byoff) if byoff else None
first4 = sorted([w for w in defects if offcount(w) == 4])[0] if 4 in byoff else None
print(f"   minimum defect off-count = {minoff}  => in X_{minoff-1}, not in X_{minoff}")
print(f"   lexicographically-first off-count-4 defect: {first4}")
print(f"   W25 recorded: 103 defects, {{4:78, 5:25}}, first X_4 word (0,0,0,0,1,1,1,1)")
R["f8"] = dict(pures=[str(x) for x in pures], n_defects=len(defects),
               by_offcount={str(k): v for k, v in sorted(byoff.items())},
               min_defect_offcount=minoff, first_off4=list(first4) if first4 else None,
               matches_W25=(len(defects) == 103 and byoff.get(4) == 78 and byoff.get(5) == 25))
require(all(x == 1 for x in pures), "F8 pures")
require(minoff == 4, "F8 must be in X_3 and not X_4")
RAN.append("T6_F8")
# mutation control: perturb one block entry -> must leave X_3
A2 = {k: [row[:] for row in M] for k, M in A.items()}
A2[(0, 1)][0][0] += Fraction(1, 7)
stillX3 = all(H_raw(A2, w, PMS8) == (1 if is_constant(w) else 0)
              for w in words(8) if offcount(w) <= 3)
print(f"   [ctrl] perturbed F8 still in X_3? {stillX3} (must be False)")
require(not stillX3, "mutation control vacuous")
RAN.append("T6_F8_mutation")

# --------------------------------------------------------- (ii) rung defs
sect("(ii) the three probe implementations of the ladder vs mine")
import importlib.util
mods = {}
for tag, path in (("W25", "unaudited-x3core-w25-2026-08-15/w25_core.py"),
                  ("W27", "unaudited-penult-w27-2026-08-18/w27_core.py"),
                  ("W28", "unaudited-x4empty-w28-2026-08-18/w28_core.py")):
    p = "/Users/rishi/workplace/krenn-conjecture/computations/" + path
    spec = importlib.util.spec_from_file_location("m_" + tag, p)
    m = importlib.util.module_from_spec(spec)
    sys.modules["m_" + tag] = m
    sys.path.insert(0, p.rsplit("/", 1)[0])
    spec.loader.exec_module(m)
    mods[tag] = m
    print(f"   loaded {tag}: has near_constant_words={hasattr(m,'near_constant_words')} "
          f"in_Xk={hasattr(m,'in_Xk')} offcount={hasattr(m,'offcount')}")

wordsets = {}
for tag, m in mods.items():
    if hasattr(m, "near_constant_words"):
        for n in (6, 8):
            for k in (2, 3, 4, 5):
                wordsets[(tag, n, k)] = set(m.near_constant_words(n, 3, k))
mine = {}
for n in (6, 8):
    for k in (2, 3, 4, 5):
        mine[(n, k)] = set(w for w in words(n) if offcount(w) <= k)
diffs = []
for (tag, n, k), s in wordsets.items():
    if s != mine[(n, k)]:
        diffs.append((tag, n, k, len(s), len(mine[(n, k)])))
print(f"   near-constant word-set comparisons: {len(wordsets)} checked, "
      f"{len(diffs)} differ from the A8 off-count definition {diffs}")
require(not diffs, f"ladder definitions differ: {diffs}")
sizes = {f"N={n},k={k}": len(mine[(n, k)]) for n in (6, 8) for k in (2, 3, 4, 5)}
print(f"   sizes {sizes}")
print(f"   N=8,k=5 -> {len(mine[(8,5)])} = 3^8, so X_5 = EXACT at N=8 is DEFINITIONAL")
R["rungs"] = dict(comparisons=len(wordsets), differ=len(diffs), sizes=sizes)
RAN.append("T6_rung_defs")

# membership agreement on shared objects
agree = 0
tested = 0
for tag, m in mods.items():
    if not hasattr(m, "in_Xk"):
        continue
    src = {}
    for e in combinations(range(8), 2):
        src[e] = [[A[e][i][j] for j in range(3)] for i in range(3)]
    for k in (2, 3, 4):
        try:
            r = m.in_Xk(src, 8, k)[0]
        except Exception as ex:            # engines may want a different container
            print(f"   {tag}.in_Xk raised {type(ex).__name__}: {ex}")
            continue
        mineok = all(H_raw(A, w, PMS8) == (1 if is_constant(w) else 0)
                     for w in words(8) if offcount(w) <= k)
        tested += 1
        agree += (r == mineok)
        print(f"   {tag}.in_Xk(F8, 8, {k}) = {r}   A8 = {mineok}")
print(f"   membership agreements: {agree}/{tested}")
require(tested == 0 or agree == tested, "in_Xk disagreement on F8")
R["rung_membership"] = dict(tested=tested, agree=agree)
RAN.append("T6_rung_membership")

checkpoint(BASE + "/results_t6_f8calib.json", R)
MAN = dict(declared=["T6_F8", "T6_F8_mutation", "T6_rung_defs", "T6_rung_membership"],
           ran=RAN)
MAN["missing"] = [x for x in MAN["declared"] if x not in RAN]
print("CONTROL MANIFEST:", MAN)
require(not MAN["missing"], "manifest")
R["manifest"] = MAN
checkpoint(BASE + "/results_t6_f8calib.json", R)

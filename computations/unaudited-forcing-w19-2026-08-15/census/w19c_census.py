#!/usr/bin/env python3
r"""UNAUDITED PROBE (W19-CENSUS) -- the census totals and STRATUM (iii).

UNAUDITED.  Nothing here is a proved claim of the repository.
Exact integer arithmetic only (Python ints throughout; no floats).

MASK CENSUS (brute forced in w19c_verify.py V6/V6a).  Of the 511 masks a
NON-Gamma block may carry (0..510):
     1 zero,  9 single (both tokens),  12 col-thin + 12 row-thin (one
     token),  477 fat-non-full (no token).
So with k_u (resp. k_v) the number of colours a_u (a_v) is allowed to take,
   f(k_u,k_v) = 1 + 477 + 4 k_u + 4 k_v + k_u k_v = 478 + 4k_u + 4k_v + k_u k_v
masks are compatible, and the number of (SC)-admissible completions of a
given Gamma is the inclusion-exclusion sum over "declared-missing" colour
sets.  Restricting the per-edge weight picks out sub-strata:
   z_thin = z_fat = 0  ->  members with h = 0 and phi = 0  ("W16 shape")
   z_fat  = 0          ->  members with phi = 0
   z_thin = 0          ->  members with h = 0
STRATUM (iii) = the complement of {h = 0 and phi = 0}.

SIGMA BOUND [PROVED-HERE].  maxcells(token pair) is 8 / 3 / 3 / 1 for
0 / 1 / 1 / 2 tokens, so the cell loss is 0 / 5 / 5 / 7 and, with
2 beta + h >= 24, loss >= min{7 beta + 5 h : 2 beta + h >= 24} = 84.  Hence
    Sigma  <=  9|Gamma| + 8(28-|Gamma|) - 84  =  |Gamma| + 140  <=  156,
with equality iff |Gamma| = 16 and all twelve non-Gamma blocks are singles
(stratum (ii)).  m <= 28 and m >= |Gamma| + 12 >= 20.
"""
from __future__ import annotations

import json
import os
import random
import sys
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w19c_lib import (  # noqa: E402
    EDGES, EIDX, N, NE, FULL, fast_in_R, fast_audit, in_R, mask_to_edges,
    my_sc_ok, block_class, canon_mask, fibres_all_words, MIXED_POS,
)

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(4242)
RES = {}
G = json.load(open(os.path.join(HERE, "results_gamma.json")))
ROWS = G["gamma_classes"]


def count_sc(gamma_mask, w_zero=1, w_single=1, w_thin=1, w_fat=1):
    """EXACT weighted count of (SC)-admissible completions of Gamma."""
    free = [EDGES[ei] for ei in range(NE) if not (gamma_mask >> ei) & 1]
    inc = [[] for _ in range(N)]
    for (u, v) in free:
        inc[u].append(v)
        inc[v].append(u)
    binom = (1, 3, 3, 1)
    sign = (1, -1, 1, -1)
    svec = [0] * N
    total = 0

    def f(ku, kv):
        return (w_zero + 477 * w_fat + 4 * ku * w_thin + 4 * kv * w_thin
                + ku * kv * w_single)

    def rec(p, coef, prod):
        nonlocal total
        if p == N:
            total += coef * prod
            return
        for s in range(4):
            svec[p] = s
            pr = prod
            for q in inc[p]:
                if q < p:
                    pr *= f(3 - s, 3 - svec[q])
            rec(p + 1, coef * binom[s] * sign[s], pr)
        svec[p] = 0

    rec(0, 1, 1)
    return total


# control: the unweighted count must reproduce results_gamma.json
bad = [r["mask"] for r in ROWS[:40]
       if count_sc(r["mask"]) != r["n_sc_completions"]]
RES["count_sc_reproduces_gamma_json"] = not bad
print("control: weighted counter reproduces results_gamma.json:", not bad)

# ------------------------------------------------------------ the totals ---
tot_all = 0
tot_high = 0
tot_high_iii = 0
tot_high_W16shape = 0
tot_low_upper = 0
per_e = {}
for r in ROWS:
    gm = r["mask"]
    n = r["n_sc_completions"]
    n00 = count_sc(gm, w_thin=0, w_fat=0)
    lab = r["orbit"]
    tot_all += lab * n
    d = per_e.setdefault(r["n_edges"], dict(classes=0, labelled_sc=0,
                                            labelled_R=0, labelled_W16shape=0))
    d["classes"] += 1
    d["labelled_sc"] += lab * n
    if r["pms"] >= 3:
        tot_high += lab * n
        tot_high_W16shape += lab * n00
        tot_high_iii += lab * (n - n00)
        d["labelled_R"] += lab * n
        d["labelled_W16shape"] += lab * n00
    else:
        tot_low_upper += lab * n

RES["labelled_sc_admissible_total"] = tot_all
RES["labelled_R_highF"] = tot_high
RES["labelled_R_highF_stratum_iii"] = tot_high_iii
RES["labelled_R_highF_W16shape"] = tot_high_W16shape
RES["labelled_lowF_upper_bound"] = tot_low_upper
RES["per_edges"] = per_e
print("\n(SC)-admissible templates with an admissible Gamma :", tot_all)
print("  of which |F(Gamma)|>=3  => ALL in (R)               :", tot_high)
print("     of these, h=phi=0 ('W16 shape', singles+zeros)   :", tot_high_W16shape)
print("     of these, stratum (iii) (some thin or fat block) :", tot_high_iii)
print("  |F(Gamma)|<=2: in (R) only for some completions, <= :", tot_low_upper)
print("\nSo  %d  <=  |(R)|  <=  %d   (labelled templates)"
      % (tot_high, tot_all))
RES["R_bracket"] = [tot_high, tot_all]

print("\n|E(Gamma)|   classes   labelled (SC)      labelled in (R)"
      "     of which W16-shape")
for k in sorted(per_e):
    d = per_e[k]
    print("%6d %9d %18d %18d %18d"
          % (k, d["classes"], d["labelled_sc"], d["labelled_R"],
             d["labelled_W16shape"]))

# ------------------------------------------- explicit points for stratum iii
print("\nEXPLICIT POINTS for stratum (iii):")
pts = {}
D = json.load(open(os.path.join(HERE, "results_decide.json")))
# (a) a member with a THIN block: take a |Gamma|=15 Gamma and give one free
#     edge a full column (thin) as its single server.
made = 0
for r in ROWS:
    if r["n_edges"] != 15 or r["pms"] < 3:
        continue
    gm = r["mask"]
    free = [ei for ei in range(NE) if not (gm >> ei) & 1]
    inc = {p: [ei for ei in free if p in EDGES[ei]] for p in range(N)}
    T = [FULL if (gm >> ei) & 1 else 0 for ei in range(NE)]
    # greedy: at each vertex give the three demands to three distinct edges
    served = {p: set() for p in range(N)}
    req = {ei: {} for ei in free}
    ok = True
    for p in range(N):
        cand = [e for e in inc[p]]
        if len(cand) < 3:
            ok = False
            break
        for r2, ei in zip(range(3), cand[:3]):
            req[ei][p] = r2
    if not ok:
        continue
    COL = [(1 | 8 | 64) << j for j in range(3)]
    ROW = [7 << (3 * i) for i in range(3)]
    for ei in free:
        u, v = EDGES[ei]
        au, av = req[ei].get(u), req[ei].get(v)
        if au is not None and av is not None:
            T[ei] = 1 << (3 * av + au)
        elif au is not None:
            T[ei] = COL[au]           # THIN
        elif av is not None:
            T[ei] = ROW[av]           # THIN
        else:
            T[ei] = FULL ^ 1          # FAT non-full
    a = fast_audit(T)
    if a["in_R"] and a["classes"]["thin"] > 0:
        assert in_R(T)
        pts["thin_member"] = dict(template=[int(x) for x in T], audit=a)
        print("   thin-block member: |Gamma|=%d h=%d phi=%d m=%d Sigma=%d"
              % (a["n_gamma"], a["classes"]["thin"], a["classes"]["fat"],
                 a["m"], a["sigma"]))
        made = 1
        break
RES["explicit_points"] = pts
RES["thin_member_found"] = bool(made)

# ------------------------------------------------------ extremal m / Sigma --
# Sigma <= |Gamma| + 140 <= 156, verified on every member we possess
allT = []
for k, T in D["reps"].items():
    allT.append(T)
L = json.load(open(os.path.join(HERE, "results_low.json")))
for mem in L.get("stratum_i_members", []):
    allT.append(mem["template"])
if "thin_member" in pts:
    allT.append(pts["thin_member"]["template"])
viol = []
mm = []
for T in allT:
    a = fast_audit(T)
    if not a["in_R"]:
        continue
    mm.append((a["m"], a["sigma"], a["n_gamma"], a["gamma_pms"]))
    if a["sigma"] > a["n_gamma"] + 140:
        viol.append(T)
RES["sigma_bound_violations"] = len(viol)
RES["m_range_over_members"] = [min(x[0] for x in mm), max(x[0] for x in mm)]
RES["sigma_range_over_members"] = [min(x[1] for x in mm), max(x[1] for x in mm)]
RES["gamma_range_over_members"] = [min(x[2] for x in mm), max(x[2] for x in mm)]
RES["F_range_over_members"] = [min(x[3] for x in mm), max(x[3] for x in mm)]
print("\nover the %d members in hand: m in %s, Sigma in %s, |Gamma| in %s,"
      " |F| in %s ; Sigma<=|Gamma|+140 violations: %d"
      % (len(mm), RES["m_range_over_members"], RES["sigma_range_over_members"],
         RES["gamma_range_over_members"], RES["F_range_over_members"],
         len(viol)))

# minimise m: strip free blocks to zero while staying in (R)
best = None
for T0 in allT[:120]:
    T = list(T0)
    if not fast_in_R(T):
        continue
    order = list(range(NE))
    rng.shuffle(order)
    for ei in order:
        if T[ei] == 0 or T[ei] == FULL:
            continue
        save = T[ei]
        T[ei] = 0
        if not fast_in_R(T):
            T[ei] = save
    a = fast_audit(T)
    if a["in_R"] and (best is None or a["m"] < best[0]):
        best = (a["m"], a["sigma"], list(T), a)
RES["min_m_found"] = best[0] if best else None
RES["min_m_template"] = [int(x) for x in best[2]] if best else None
RES["min_m_audit"] = best[3] if best else None
print("smallest m reached by greedy stripping:", best[0] if best else None,
      "(theoretical floor m >= |Gamma|+12 >= 20)")

# ---------------------------------------------- W16's "seven skeletons" ----
CUBIC_NAMED = {
 "cube_K44_minus_PM":
   [(0,4),(1,5),(2,6),(3,7),(0,5),(1,6),(2,7),(3,4),(0,6),(1,7),(2,4),(3,5)],
 "K4+K4":
   [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3),(4,5),(4,6),(4,7),(5,6),(5,7),(6,7)],
 "WagnerV8":
   [(i,(i+1)%8) for i in range(8)] + [(0,4),(1,5),(2,6),(3,7)],
 "Q3":
   [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)],
 "C8+short":
   [(i,(i+1)%8) for i in range(8)] + [(0,2),(1,3),(4,6),(5,7)],
 "twistedC8":
   [(i,(i+1)%8) for i in range(8)] + [(0,3),(1,6),(2,5),(4,7)],
 "C8+3chords":
   [(i,(i+1)%8) for i in range(8)] + [(0,5),(1,4),(2,7),(3,6)],
}
can = {}
for nm, C in CUBIC_NAMED.items():
    m0 = 0
    for (u, v) in C:
        m0 |= 1 << EIDX[(min(u, v), max(u, v))]
    can.setdefault(canon_mask(m0), []).append(nm)
RES["W16_named_skeleton_classes"] = {str(k): v for k, v in can.items()}
print("\nW16's 7 named cubic skeletons fall into %d isomorphism classes:"
      % len(can))
for k, v in can.items():
    print("   ", v)

json.dump(RES, open(os.path.join(HERE, "results_census.json"), "w"))
print("\nwritten results_census.json")

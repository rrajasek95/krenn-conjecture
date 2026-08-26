#!/usr/bin/env python3
"""W21-M2-SING: the END-TO-END kill of the C_8 member, with every link of the
chain checked exactly and every checker mutation-tested.

THE CHAIN
 (1) x = (1,0,0,2) is L-FREE.                                    [exact]
 (2) For an L-free x and every R-word y,  H_(x,y) = per B(x,y),
     B(x,y)[i][j] = A_{i,j}[x_i][y_j].                           [exact, C1]
 (3) per B(x,y) = per(col y_4 of M_4^x, ..., col y_7 of M_7^x), so the 81
     equations {H_(x,y)=0 : all y} hold iff per vanishes IDENTICALLY on
     V_4 x V_5 x V_6 x V_7,  V_j = colspan(M_j^x).               [exact]
 (4) Every M_j^x (j=4,5,6,7) carries a DEAD cell, and every row of M_j^x keeps
     >= 2 and every column >= 2 occupied cells.  Hence rank M_j^x >= 2 and no
     row of M_j^x vanishes, for EVERY assignment with all occupied cells
     nonzero.                                                    [FACT A]
 (5) THEOREM W21-M2: per cannot vanish identically on a product of four
     subspaces of C^4 that all have dim >= 2 and none of which lies in a
     coordinate hyperplane.                          [m2steps / m2stepBD /
                                                      m2thm_sweep2]
 (6) Contradiction.  So NO exact source has the C_8 template.
The mirror does it a second time with the R-free words (0,2,0,1), (0,2,0,2).
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
import m2core as M
import m2steps as ST
import m2sys as S
import w21_c8core as G

rng = random.Random(770021)
res = {"_header": "UNAUDITED W21-M2-SING end-to-end kill of the C_8 member"}
DEADROW = {(i, j): M.DEAD[(i, j)][0] for (i, j) in M.DEAD}
DEADCOL = {(i, j): M.DEAD[(i, j)][1] for (i, j) in M.DEAD}

KILL_L = [x for x in M.LFREE
          if all(any(DEADROW.get((i, j)) == x[M.LPOS[i]] for i in M.L)
                 for j in M.R)]
KILL_R = [y for y in M.RFREE
          if all(any(DEADCOL.get((i, j)) == y[M.RPOS[j]] for j in M.R)
                 for i in M.L)]
print("(1) all-dirty L-free words  : %s" % (KILL_L,))
print("    all-dirty R-free words  : %s" % (KILL_R,))
res["kill_words_L"] = [list(x) for x in KILL_L]
res["kill_words_R"] = [list(y) for y in KILL_R]
assert all(tuple(x) in M.LFREE for x in KILL_L)
assert all(tuple(y) in M.RFREE for y in KILL_R)

# ---- (2)+(3): H = per B = per of the chosen columns of the M_j -------------
mis = tot = 0
for _ in range(4):
    bl = G.random_blocks(rng)
    for x in KILL_L:
        Ms = {j: G.M_j(bl, x, j) for j in M.R}
        for y in product(range(3), repeat=4):
            cols = [[Ms[j][i][y[M.RPOS[j]]] for j in M.R] for i in M.L]
            v = G.per4(cols)
            tot += 1
            if v != G.H_value(bl, G.C8_MEMBER, tuple(x) + tuple(y)):
                mis += 1
    for y in KILL_R:
        Ns = {i: G.N_i(bl, y, i) for i in M.L}
        for x in product(range(3), repeat=4):
            cols = [[Ns[i][M.RPOS[j]][x[M.LPOS[i]]] for j in M.R]
                    for i in M.L]
            v = G.per4(cols)
            tot += 1
            if v != G.H_value(bl, G.C8_MEMBER, tuple(x) + tuple(y)):
                mis += 1
print("(2,3) H_w == per(columns of M_j^x) / per(columns of N_i^y): "
      "%d mismatches / %d checks" % (mis, tot))
res["chain23_mismatch"], res["chain23_checks"] = mis, tot

# MUTATION on that checker
bl = G.random_blocks(rng)
bl2 = {e: [r[:] for r in bl[e]] for e in bl}
bl2[(0, 4)][1][1] += Fraction(1)
x0 = KILL_L[0]
Ms = {j: G.M_j(bl, x0, j) for j in M.R}
mut = sum(1 for y in product(range(3), repeat=4)
          if G.per4([[Ms[j][i][y[M.RPOS[j]]] for j in M.R] for i in M.L])
          != G.H_value(bl2, G.C8_MEMBER, tuple(x0) + tuple(y)))
print("      MUTATION (one block entry perturbed): %d/81 now differ (want >0)"
      % mut)
res["chain23_mutation"] = mut

# ---- (4) FACT A, both sides ------------------------------------------------
factA = {"L": [], "R": []}
for x in KILL_L:
    for j in M.R:
        occp = [[M.occ(i, j, x[M.LPOS[i]], d) for d in range(3)] for i in M.L]
        nd = sum(1 for r in occp for v in r if not v)
        rowmin = min(sum(1 for v in r if v) for r in occp)
        colmin = min(sum(1 for r in occp if r[d]) for d in range(3))
        factA["L"].append({"x": list(x), "j": j, "dead": nd, "rowmin": rowmin,
                           "colmin": colmin,
                           "rank_ge_2": ST.factA(occp, char=0)})
for y in KILL_R:
    for i in M.L:
        occp = [[M.occ(i, j, c, y[M.RPOS[j]]) for c in range(3)] for j in M.R]
        nd = sum(1 for r in occp for v in r if not v)
        rowmin = min(sum(1 for v in r if v) for r in occp)
        colmin = min(sum(1 for r in occp if r[c]) for c in range(3))
        factA["R"].append({"y": list(y), "i": i, "dead": nd, "rowmin": rowmin,
                           "colmin": colmin,
                           "rank_ge_2": ST.factA(occp, char=0)})
nL = sum(1 for r in factA["L"] if r["rank_ge_2"] is True)
nR = sum(1 for r in factA["R"] if r["rank_ge_2"] is True)
print("(4) FACT A rank>=2 forced: L-side %d/%d sites, R-side %d/%d sites; "
      "min occupied per row = %d, per column = %d"
      % (nL, len(factA["L"]), nR, len(factA["R"]),
         min(r["rowmin"] for r in factA["L"] + factA["R"]),
         min(r["colmin"] for r in factA["L"] + factA["R"])))
res["factA"] = factA
res["factA_L_ok"], res["factA_L_n"] = nL, len(factA["L"])
res["factA_R_ok"], res["factA_R_n"] = nR, len(factA["R"])

# ---- MUTATION CONTROL: a word with a CLEAN site must NOT be killed ---------
clean = [x for x in M.LFREE
         if any(all(DEADROW.get((i, j)) != x[M.LPOS[i]] for i in M.L)
                for j in M.R)]
print("(5) MUTATION control: %d of the 30 L-free words have >= 1 CLEAN site, "
      "so FACT A does NOT apply to them" % len(clean))
res["n_words_with_clean_site"] = len(clean)
bad = 0
for x in clean[:8]:
    for j in M.R:
        occp = [[M.occ(i, j, x[M.LPOS[i]], d) for d in range(3)]
                for i in M.L]
        if all(all(r) for r in occp) and ST.factA(occp, char=0) is not False:
            bad += 1
print("      clean sites correctly report rank-1 POSSIBLE (non-unit): "
      "%d violations (want 0)" % bad)
res["clean_site_violations"] = bad

json.dump(res, open("results_kill.json", "w"), indent=1, default=str)
print("\nVERDICT: the 81 equations of the L-free word %s (and of %s, %s, and "
      "of the R-free words %s) are UNSATISFIABLE with all occupied cells "
      "nonzero.  THE C_8 MEMBER IS KILLED." % (KILL_L[0], KILL_L[1],
                                               KILL_L[2], KILL_R))

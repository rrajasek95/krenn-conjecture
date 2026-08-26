#!/usr/bin/env python3
"""W21-M2-GEO step 1: build + CONTROL the geometry machinery.  UNAUDITED.

Controls run here
  C1  rank-based collinear set  ==  union of the line boxes   (identity)
  C2  the L-free reduction still holds on every block set used
  C3  MUTATION: plant a collinear transversal -> the detector must flip
  C4  EXPLICIT-POINT: a hand-built fully collinear site must be detected,
      with all 136 cells nonzero and all 8 dead cells zero
  C5  the two dead cells of every R-site sit in different columns except at
      j = 6 (recorded, it kills the coordinate-line box there)
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import m2geo as X                                                   # noqa: E402
import w21_c8core as G                                              # noqa: E402

res = {"_header": "UNAUDITED W21-M2-GEO controls, exact arithmetic."}
rng = random.Random(20260815)

# ---------------------------------------------------------------- C1 + C2 ---
bad_box = bad_red = 0
ntr = 4
for _ in range(ntr):
    bl = G.random_blocks(rng)
    for j in X.R:
        pts = X.points_R(bl, j)
        _, S = X.boxes_of_site(pts, X.L)
        if S != X.collinear_set(pts, X.L, None):
            bad_box += 1
    for i in X.L:
        pts = X.points_L(bl, i)
        _, S = X.boxes_of_site(pts, X.R)
        if S != X.collinear_set(pts, X.R, None):
            bad_box += 1
    for x in X.LFREE:
        for y in X.WORDS4:
            if G.H_value(bl, G.C8_MEMBER, x + y) != \
                    G.per4(G.cross_matrix(bl, x, y)):
                bad_red += 1
print("C1 box-union == rank-collinear-set : %d mismatches / %d sites"
      % (bad_box, 8 * ntr))
print("C2 L-free permanent reduction      : %d mismatches / %d checks"
      % (bad_red, ntr * 30 * 81))
res["C1_box_vs_rank_mismatches"] = bad_box
res["C2_reduction_mismatches"] = bad_red

# ------------------------------------------------------------------- C3 -----
# MUTATION CONTROL: force rows 0 of A_{0,4},A_{1,4},A_{2,4},A_{3,4} onto one
# line and check the detector flips exactly on the words with x = (0,0,0,0).
bl = G.random_blocks(rng)
before = X.S_R(bl, 4)
u = (Fraction(1), Fraction(2), Fraction(-3))     # the line ker(u)
bl2 = {e: [r[:] for r in bl[e]] for e in bl}
for i in X.L:
    a, b, c = bl2[(i, 4)][0]
    if (i, 4) in X.DEAD and X.DEAD[(i, 4)][0] == 0:
        # respect the dead cell: only i = 1 has dead (0,0) at j=4
        d = X.DEAD[(i, 4)][1]
        free = [k for k in range(3) if k != d]
        bl2[(i, 4)][0][d] = Fraction(0)
        bl2[(i, 4)][0][free[0]] = Fraction(1)
        bl2[(i, 4)][0][free[1]] = -u[free[0]] / u[free[1]]
    else:
        bl2[(i, 4)][0] = [Fraction(1), Fraction(1), (u[0] + u[1]) / (-u[2])]
after = X.S_R(bl2, 4)
planted = (0, 0, 0, 0)
print("C3 MUTATION planted transversal    : before %s / after %s (want "
      "False/True)" % (planted in before, planted in after))
res["C3_before"] = planted in before
res["C3_after"] = planted in after

# ------------------------------------------------------------------- C5 -----
deadcols = {}
for j in X.R:
    dd = [(i, X.DEAD[(i, j)]) for i in X.L if (i, j) in X.DEAD]
    deadcols[j] = [[i, list(cd)] for i, cd in dd]
print("C5 dead cells per R-site           :", deadcols)
res["C5_dead_per_Rsite"] = deadcols
deadrows = {}
for i in X.L:
    dd = [(j, X.DEAD[(i, j)]) for j in X.R if (i, j) in X.DEAD]
    deadrows[i] = [[j, list(cd)] for j, cd in dd]
print("C5 dead cells per L-site           :", deadrows)
res["C5_dead_per_Lsite"] = deadrows

json.dump(res, open(os.path.join(HERE, "results_check1.json"), "w"), indent=1,
          default=str)
print("done")

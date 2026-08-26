#!/usr/bin/env python3
"""W21-M2-SING run 1: the FIXED-y slices.

For a FIXED R-word y, the 30 equations  {per B(x,y) = 0 : x L-free}  involve
ONLY the cells A_{i,j}[c][y_j] (at most 48 of them).  This is a genuine
subsystem of the 3,960 L-free permanent equations, so:
    INFEASIBLE (all cells nonzero)  ==>  the C_8 member is KILLED.
It uses ALL THIRTY L-free words at once, which is what single-word analysis
cannot do, and it is by far the smallest such combined system.

Selection rule for y: maximise the number of GROUPS i in L that are hit by a
forced zero.  Group i is the triple of vectors g[i][c] = (A_{i,j}[c][y_j])_j
in C^4; if group i has no forced zero it can be made rank one
(g[i][c] = alpha_{i,c} f^(i)) and then all 30 permanents collapse to the single
condition per(f^(0),..,f^(3)) = 0, which is solvable with all cells nonzero.
So a slice can only be infeasible if EVERY group carries a forced zero.
Exactly four y give 4 groups hit with 5 forced zeros: 0101, 0200, 0201, 1101.
"""
import json
import sys

sys.dont_write_bytecode = True
import m2core as M
import m2sys as S

CHAR = int(sys.argv[1]) if len(sys.argv) > 1 else 32003
TMO = int(sys.argv[2]) if len(sys.argv) > 2 else 900
YS = sys.argv[3].split(",") if len(sys.argv) > 3 else \
    ["0101", "0200", "0201", "1101", "0100", "2020"]

res = {"_header": "UNAUDITED W21-M2-SING fixed-y slices", "char": CHAR,
       "timeout": TMO}
for ys in YS:
    y = tuple(int(ch) for ch in ys)
    e, cl, lb = S.sys_fixed_y(y)
    r = S.run_system("y%s_c%d" % (ys, CHAR), e, cl, char=CHAR, timeout=TMO)
    r["y"] = ys
    res.setdefault("runs", []).append(r)
    json.dump(res, open("results_run_y_c%d.json" % CHAR, "w"), indent=1,
              default=str)

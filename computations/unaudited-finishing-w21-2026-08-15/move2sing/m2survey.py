#!/usr/bin/env python3
"""W21-M2-SING: size survey of the candidate systems + selection rules."""
import json
import sys
from itertools import product

sys.dont_write_bytecode = True
import m2core as M
import m2sys as S

out = {"_header": "UNAUDITED W21-M2-SING system size survey"}

# ---- which L-free words touch dead cells, and where -------------------------
# row u[i][c][j] of block (i,j) contains a dead cell iff DEAD[(i,j)]=(c,*)
DEADROW = {(i, j): M.DEAD[(i, j)][0] for (i, j) in M.DEAD}
DEADCOL = {(i, j): M.DEAD[(i, j)][1] for (i, j) in M.DEAD}


def dirty_sites_L(x):
    """R-sites j at which some row of M_j^x hits a dead cell."""
    return tuple(j for j in M.R
                 if any(DEADROW.get((i, j)) == x[M.LPOS[i]] for i in M.L))


def dirty_sites_R(y):
    return tuple(i for i in M.L
                 if any(DEADCOL.get((i, j)) == y[M.RPOS[j]] for j in M.R))


print("L-free words by number of DIRTY R-sites (sites whose 4x3 matrix M_j^x")
print("contains a dead cell -- these are the sites where the rank-1 escape")
print("A_{i,j}=K(x)s is impossible):")
byd = {}
for x in M.LFREE:
    d = dirty_sites_L(x)
    byd.setdefault(len(d), []).append((x, d))
for k in sorted(byd):
    print("  %d dirty sites: %2d words  e.g. %s"
          % (k, len(byd[k]), byd[k][0]))
out["Lfree_by_ndirty"] = {str(k): len(v) for k, v in byd.items()}
out["Lfree_dirty"] = {''.join(map(str, x)): list(d) for x in M.LFREE
                      for d in [dirty_sites_L(x)]}

print("\nR-free words by number of dirty L-sites:")
byd2 = {}
for y in M.RFREE:
    d = dirty_sites_R(y)
    byd2.setdefault(len(d), []).append((y, d))
for k in sorted(byd2):
    print("  %d dirty sites: %2d words  e.g. %s" % (k, len(byd2[k]),
                                                    byd2[k][0]))
out["Rfree_by_ndirty"] = {str(k): len(v) for k, v in byd2.items()}

# ---- the FIXED-y slices ------------------------------------------------------
# variables z[i][j][c] = A_{i,j}[c][y_j]; group i = the 3 vectors g[i][c] in C^4
# forced zero at (i,j,c) iff DEAD[(i,j)] == (c, y_j).
print("\nFIXED-y slices (30 L-free permanents, cells A_ij[c][y_j] only):")
rows = []
for y in product(range(3), repeat=4):
    zeros = [(i, j, c) for (i, j) in M.DEAD for c in [DEADROW[(i, j)]]
             if DEADCOL[(i, j)] == y[M.RPOS[j]]]
    groups = sorted({i for (i, j, c) in zeros})
    e, cl, lb = S.sys_fixed_y(y)
    tree, free, nn, nc = S.gauge_fix(cl)
    rows.append((len(zeros), len(groups), y, len(cl), len(tree), len(free),
                 len(e)))
rows.sort(key=lambda r: (-r[1], -r[0]))
for r in rows[:8]:
    print("  y=%s zeros=%d groups_hit=%d cells=%d gauge=%d freevars=%d eqs=%d"
          % (''.join(map(str, r[2])), r[0], r[1], r[3], r[4], r[5], r[6]))
out["fixed_y_top"] = [{"y": ''.join(map(str, r[2])), "zeros": r[0],
                       "groups_hit": r[1], "cells": r[3], "gauge": r[4],
                       "freevars": r[5], "eqs": r[6]} for r in rows[:12]]

# ---- the multi-word systems -------------------------------------------------
X1, X2 = (0, 2, 1, 0), (0, 2, 1, 1)
print("\nMulti-word (full 81-per-word) systems:")
for tag, lw, rw in [("a  x1,x2", [X1, X2], []),
                    ("b3 x1,x2,+1dirty", [X1, X2, (1, 0, 2, 1)], []),
                    ("b4 x1,x2,+2dirty", [X1, X2, (1, 0, 2, 1), (2, 1, 0, 2)],
                     []),
                    ("cR 2 R-free", [], list(M.RFREE)[:2]),
                    ("c  x1,x2 + 2 R-free", [X1, X2], list(M.RFREE)[:2])]:
    lw = [w for w in lw if tuple(w) in M.LFREE]
    e, cl, lb = S.sys_words(lwords=lw, rwords=rw)
    tree, free, nn, nc = S.gauge_fix(cl)
    print("  %-22s eqs=%4d cells=%3d gauge=%2d freevars=%3d"
          % (tag, len(e), len(cl), len(tree), len(free)))
    out.setdefault("multiword", []).append(
        {"tag": tag, "eqs": len(e), "cells": len(cl), "gauge": len(tree),
         "freevars": len(free)})

json.dump(out, open("results_survey.json", "w"), indent=1, default=str)

#!/usr/bin/env python3
"""W21-M2-GEO step 10: final identities, EXPLICIT-POINT controls in
characteristic ZERO, and the codimension accounting.  UNAUDITED.  Exact.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import combinations, permutations, product

import sympy as sp

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import m2geo as X                                                   # noqa: E402

P4 = list(permutations(range(4)))
res = {"_header": "UNAUDITED W21-M2-GEO final identities + controls, exact."}


def per4(cols):
    return sum(sp.prod([cols[j][p[j]] for j in range(4)]) for p in P4)


# ---------------------------------------------------------------- identity
u = sp.symbols('u0:4')
w = sp.symbols('w0:4')
B = sp.zeros(4, 4)
for k in range(4):
    for l in range(4):
        if k != l:
            p, s = [t for t in range(4) if t not in (k, l)]
            B[k, l] = u[p] * w[s] + u[s] * w[p]
E_uw = sum(u[k] * sp.prod([w[l] for l in range(4) if l != k]) for k in range(4))
E_wu = sum(w[k] * sp.prod([u[l] for l in range(4) if l != k]) for k in range(4))
PU = sp.prod(u)
PW = sp.prod(w)
ident = sp.simplify(sp.expand(B.det() + 4 * (E_uw * E_wu - 4 * PU * PW)))
print("IDENTITY  det B = -4 [ E(u,w) E(w,u) - 4 (prod u)(prod w) ] :",
      ident == 0)
res["detB_E_identity"] = bool(ident == 0)

# ------------------------------------- EXPLICIT char-0 per-null quadruple --
# V4 = V6 = V7 = {(a,b,b,a)},  V5 = {(a,b,-b,-a)}:  the m_03 = m_12 = 0
# perfect-matching family.  NO V_j lies in a coordinate hyperplane.
def mk(rows):
    return [tuple(Fraction(z) for z in r) for r in rows]


V = {4: mk([(1, 0, 0, 1), (0, 1, 1, 0)]),
     5: mk([(1, 0, 0, -1), (0, 1, -1, 0)]),
     6: mk([(1, 0, 0, 1), (0, 1, 1, 0)]),
     7: mk([(1, 0, 0, 1), (0, 1, 1, 0)])}
bad = 0
for c in product(range(2), repeat=4):
    cols = [V[j][c[k]] for k, j in enumerate((4, 5, 6, 7))]
    if per4(cols) != 0:
        bad += 1
print("EXPLICIT char-0 per-null quadruple (PM family): %d/16 permanents "
      "nonzero (want 0); no V_j in a coordinate hyperplane: %s"
      % (bad, all(any(r[k] for r in V[j]) for j in V for k in range(4))))
res["char0_pernull_failures"] = bad
res["char0_pernull_example"] = {str(j): [[str(z) for z in r] for r in V[j]]
                                for j in V}

# MUTATION CONTROL: break the negation in V5 and the permanents must fire
V5bad = mk([(1, 0, 0, 1), (0, 1, -1, 0)])
bad2 = sum(1 for c in product(range(2), repeat=4)
           if per4([V[4][c[0]], V5bad[c[1]], V[6][c[2]], V[7][c[3]]]) != 0)
print("MUTATION control (negation broken): %d/16 permanents nonzero "
      "(want > 0)" % bad2)
res["char0_mutation_failures"] = bad2

# --------------------------------------------------- codimension accounting
# 136 cross cells (144 - 8 dead), gauge dim 24 with a 1-dimensional
# redundancy => 113 effective parameters.
ncells = sum(bin(X.G.C8_MEMBER[X.G.EIDX[(i, j)]]).count("1")
             for i in X.L for j in X.R)
print("cross cells occupied: %d ; gauge 24 - 1 = 23 ; effective %d"
      % (ncells, ncells - 23))
res["cross_cells"] = ncells
res["effective_parameters"] = ncells - 23

# cheapest configurations satisfying the collinearity obligations
# (line with k of the 12 points costs k-2; a fully degenerate site costs 10)
res["cost_one_degenerate_site"] = 10
res["cost_all_eight_sites_degenerate"] = 80
print("codim cost: a fully collinear site = 12-2 = 10; all eight sites = 80 "
      "<= 113 -- the budget alone CANNOT close the case")

# a coincidence of two points of P^2 costs 2; the killed word needs none
res["cost_point_coincidence"] = 2

json.dump(res, open(os.path.join(HERE, "results_final.json"), "w"), indent=1,
          default=str)
print("done")

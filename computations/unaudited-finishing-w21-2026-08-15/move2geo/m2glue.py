#!/usr/bin/env python3
"""W21-M2-GEO step 6: the COINCIDENCE (gluing) layer.  UNAUDITED.  Exact.

The exhaustive F_5 classification (m2profile.py) plus the proved lemmas say
that for EVERY L-free word x the four transversals cannot merely be collinear:

  * at most TWO of the V_j^x are hyperplanes                        [LEMMA B]
  * if exactly two are, the OTHER TWO have dim 1, i.e. ALL FOUR transversal
    points COINCIDE at both of those sites                      [LEMMA C-str]
  * if exactly one is, some collinear site has dim 1                    [F_5]
  * if none is, at least two sites carry a transversal COINCIDENCE      [F_5]

so every L-free word forces point coincidences.  This module computes what the
DEAD CELLS allow.

KEY OBSERVATION [PROVED-HERE].  P^j_{r,c} = P^j_{t,c'} means row c of A_{r,j}
is proportional to row c' of A_{t,j}; proportional rows have the SAME zero
pattern.  Every cross block has at most one dead cell, so a row carrying a dead
cell in column d can only be proportional to another row carrying its dead cell
in the SAME column d.  Each R-site has exactly two fat blocks:

     site 4:  (1,4) dead (0,0)  and (2,4) dead (2,1)   -- columns 0 and 1
     site 5:  (1,5) dead (1,1)  and (3,5) dead (2,2)   -- columns 1 and 2
     site 6:  (0,6) dead (1,0)  and (2,6) dead (0,0)   -- columns 0 and 0  (!)
     site 7:  (0,7) dead (2,0)  and (3,7) dead (2,1)   -- columns 0 and 1

so at sites 4, 5 and 7 the two "dead" labels are GLUEABLE TO NOTHING AT ALL,
and at site 6 the two dead labels ((0,1) and (2,0)) can only be glued to each
other.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations, product

import sympy as sp

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import m2geo as X                                                   # noqa: E402
import w21_c8core as G                                              # noqa: E402

L, R = X.L, X.R
res = {"_header": "UNAUDITED W21-M2-GEO gluing layer, exact."}

# ------------------------------------------------------------------------ 1
# STRENGTHENED LEMMA C: in the two-hyperplane case the minimal edge cover E
# cannot be a PERFECT MATCHING.  With rows 1,2 and rows 3,4 proportional at
# both collinear sites and the negated ratios forced by m_12 = m_34 = 0,
#      B = [[0,0,m24,m23],[0,0,m14,m13],[m24,m14,0,0],[m23,m13,0,0]]
# has rank 2*rank C, C = [[m24,m23],[m14,m13]], and det C = -4 k l u1 u3 w1 w3
# which is NOT the zero polynomial -- so rank B = 4 > 2.  Verified symbolically.
u1, u3, w1, w3, kk, ll = sp.symbols('u1 u3 w1 w3 k l')
u = [u1, kk * u1, u3, ll * u3]
w = [w1, -kk * w1, w3, -ll * w3]


def mm(a, b):
    return sp.expand(u[a] * w[b] + u[b] * w[a])


m12, m34 = mm(0, 1), mm(2, 3)
C = sp.Matrix([[mm(1, 3), mm(1, 2)], [mm(0, 3), mm(0, 2)]])
detC = sp.factor(sp.expand(C.det()))
print("LEMMA C-str: m_12 = %s, m_34 = %s, det C = %s"
      % (m12, m34, detC))
res["lemmaCstr_m12"] = str(m12)
res["lemmaCstr_m34"] = str(m34)
res["lemmaCstr_detC"] = str(detC)
res["lemmaCstr_detC_is_zero_poly"] = bool(sp.simplify(detC) == 0)

# MUTATION CONTROL: with the SAME (not negated) ratios m_12, m_34 do not vanish
w_same = [w1, kk * w1, w3, ll * w3]
m12s = sp.expand(u[0] * w_same[1] + u[1] * w_same[0])
print("LEMMA C-str MUTATION (ratios not negated): m_12 = %s (want != 0)"
      % sp.factor(m12s))
res["lemmaCstr_mutation_m12"] = str(sp.factor(m12s))

# ------------------------------------------------------------------------ 2
# glueability of labels, forced by the dead cells
def dead_col(j, i, c):
    """the column of the dead cell if it lies in row c of block (i,j)."""
    d = X.DEAD.get((i, j))
    if d is not None and d[0] == c:
        return d[1]
    return None


LABELS = [(i, c) for i in L for c in range(3)]
glue_ok = {}
for j in R:
    ok = {}
    for a, b in combinations(LABELS, 2):
        if a[0] == b[0]:
            continue
        da, db = dead_col(j, a[0], a[1]), dead_col(j, b[0], b[1])
        ok[(a, b)] = (da == db)
    glue_ok[j] = ok
    lonely = [a for a in LABELS
              if not any(ok.get((a, b), ok.get((b, a), False))
                         for b in LABELS if b[0] != a[0])]
    print("site %d: labels glueable to NOTHING: %s" % (j, lonely))
    res["lonely_labels_site_%d" % j] = [list(a) for a in lonely]

# D_j = words whose whole transversal can possibly be one point at site j
D = {}
for j in R:
    Dj = set()
    for x in X.WORDS4:
        lab = [(i, x[i]) for i in L]
        if all(glue_ok[j].get((a, b), glue_ok[j].get((b, a), False))
               for a, b in combinations(lab, 2)):
            Dj.add(x)
    D[j] = Dj
    print("site %d: words that CAN have all four transversal points coincident"
          " : %d of 81  (%d of the 30 L-free)"
          % (j, len(Dj), len(Dj & set(X.LFREE))))
    res["D_site_%d_size" % j] = len(Dj)
    res["D_site_%d_Lfree" % j] = len(Dj & set(X.LFREE))

nowhere = [x for x in X.LFREE if not any(x in D[j] for j in R)]
print("L-free words that can have a fully coincident transversal at NO site: "
      "%d  %s" % (len(nowhere), nowhere))
res["Lfree_in_no_D"] = [list(x) for x in nowhere]

nowhereR = None
# mirror
def dead_row(i, j, d):
    dd = X.DEAD.get((i, j))
    if dd is not None and dd[1] == d:
        return dd[0]
    return None


LABELS_R = [(j, d) for j in R for d in range(3)]
DR = {}
for i in L:
    ok = {}
    for a, b in combinations(LABELS_R, 2):
        if a[0] == b[0]:
            continue
        ok[(a, b)] = (dead_row(i, a[0], a[1]) == dead_row(i, b[0], b[1]))
    Di = set()
    for y in X.WORDS4:
        lab = [(R[k], y[k]) for k in range(4)]
        if all(ok.get((a, b), ok.get((b, a), False))
               for a, b in combinations(lab, 2)):
            Di.add(y)
    DR[i] = Di
    print("L-site %d: words that CAN be fully coincident: %d of 81 (%d of 30 "
          "R-free)" % (i, len(Di), len(Di & set(X.RFREE))))
    res["DR_site_%d_Rfree" % i] = len(Di & set(X.RFREE))
nowhereR = [y for y in X.RFREE if not any(y in DR[i] for i in L)]
print("R-free words with no fully coincident site: %d %s"
      % (len(nowhereR), nowhereR))
res["Rfree_in_no_DR"] = [list(y) for y in nowhereR]

# ------------------------------------------------------------------------ 3
# EXPLICIT-POINT CONTROL: the glueability predicate must ACCEPT a genuine
# proportional pair.  Build one and check the rank/point test agrees.
from fractions import Fraction
rngbl = G.random_blocks(__import__('random').Random(4242))
rngbl[(0, 4)][1] = [Fraction(2) * z for z in rngbl[(3, 4)][2]]
pts = X.points_R(rngbl, 4)
same = X.proj_eq(pts[(0, 1)], pts[(3, 2)])
print("CONTROL: planted proportional rows detected as one point of P^2:", same)
res["control_planted_coincidence"] = bool(same)
# and a dead-cell pair must be REJECTED by construction
print("CONTROL: glueability of the two dead labels at site 4 ((1,0),(2,2)):",
      glue_ok[4].get(((1, 0), (2, 2))))
res["control_dead_pair_site4"] = bool(glue_ok[4].get(((1, 0), (2, 2))))
print("CONTROL: glueability of the two dead labels at site 6 ((0,1),(2,0)):",
      glue_ok[6].get(((0, 1), (2, 0))))
res["control_dead_pair_site6"] = bool(glue_ok[6].get(((0, 1), (2, 0))))

json.dump(res, open(os.path.join(HERE, "results_glue.json"), "w"), indent=1,
          default=str)
print("done")

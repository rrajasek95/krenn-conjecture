#!/usr/bin/env python3
"""W21-M2-SING controls for m2core.py.  All exact.

C1  per_poly == H_w  (independent engine in w21_c8core) for every L-free x /
    every y and every R-free y / every x, on random exact rational blocks.
C2  MUTATION: per_poly must DISAGREE with H on words that are neither L-free
    nor R-free (otherwise the reduction claim would be vacuous).
C3  MUTATION: perturbing one coefficient of one generated polynomial must make
    C1 fail (the checker must be able to say 'no').
C4  GAUGE validity: for a random all-nonzero point and the spanning forest of
    any cell set, gauge_to_slice produces lam,mu making every forest cell 1,
    the gauged point is still all-nonzero, and every per_poly is multiplied by
    the predicted monomial in lam,mu (so vanishing is preserved exactly).
C5  the forest has exactly (#nodes - #components) cells => the slice uses the
    full effective torus.
"""
import json
import random
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
import m2core as M
import w21_c8core as G

rng = random.Random(20260815)
res = {"_header": "UNAUDITED W21-M2-SING controls"}


def rand_blocks():
    return G.random_blocks(rng)


def blocks_to_val(bl):
    return {(i, j, c, d): bl[(i, j)][c][d] for (i, j, c, d) in M.CELLS}


# ---------------------------------------------------------------- C1
mis = tot = 0
for _ in range(3):
    bl = rand_blocks()
    val = blocks_to_val(bl)
    for x in M.LFREE:
        for y in product(range(3), repeat=4):
            tot += 1
            if M.p_eval(M.per_poly(x, y), val) != G.H_value(bl, G.C8_MEMBER,
                                                            tuple(x) + tuple(y)):
                mis += 1
    for y in M.RFREE:
        for x in product(range(3), repeat=4):
            tot += 1
            if M.p_eval(M.per_poly(x, y), val) != G.H_value(bl, G.C8_MEMBER,
                                                            tuple(x) + tuple(y)):
                mis += 1
print("C1 per_poly vs independent H engine: %d mismatches / %d checks"
      % (mis, tot))
res["C1_mismatch"], res["C1_checks"] = mis, tot

# ---------------------------------------------------------------- C2 mutation
bl = rand_blocks()
val = blocks_to_val(bl)
nonfree = [w for w in product(range(3), repeat=8)
           if not G.lfree(w[:4]) and not G.rfree(w[4:])]
diff = sum(1 for w in nonfree[:500]
           if M.p_eval(M.per_poly(w[:4], w[4:]), val)
           != G.H_value(bl, G.C8_MEMBER, w))
print("C2 MUTATION (non-free words must differ): %d/500 differ (want >0)"
      % diff)
res["C2_nonfree_differ"] = diff

# ---------------------------------------------------------------- C3 mutation
x0, y0 = M.LFREE[0], (0, 1, 2, 0)
p = M.per_poly(x0, y0)
mon0 = sorted(p)[0]
pbad = dict(p)
pbad[mon0] += 1
c3 = (M.p_eval(pbad, val) != G.H_value(bl, G.C8_MEMBER, tuple(x0) + tuple(y0)))
print("C3 MUTATION (planted +1 coefficient must break the match): %s" % c3)
res["C3_planted_breaks"] = bool(c3)

# ---------------------------------------------------------------- C4/C5 gauge
tree, nnodes, ncomp = M.spanning_forest(M.CELLS)
print("C5 full-cell gauge forest: %d cells, %d nodes, %d components "
      "(want cells = nodes - comps = %d)"
      % (len(tree), nnodes, ncomp, nnodes - ncomp))
res["C5_tree_cells"] = len(tree)
res["C5_nodes"] = nnodes
res["C5_components"] = ncomp
assert len(tree) == nnodes - ncomp

bl = rand_blocks()
val = blocks_to_val(bl)
lam, mu = M.gauge_to_slice(val, tree)
val2 = M.gauge_apply(val, lam, mu)
ok_ones = all(val2[c] == 1 for c in tree)
ok_nz = all(v != 0 for v in val2.values())
print("C4a gauge slice: all %d forest cells == 1 : %s ; still all-nonzero: %s"
      % (len(tree), ok_ones, ok_nz))
res["C4_tree_all_one"] = bool(ok_ones)
res["C4_all_nonzero"] = bool(ok_nz)

badcov = 0
ncov = 0
for x in list(M.LFREE)[:6]:
    for y in list(product(range(3), repeat=4))[:9]:
        pp = M.per_poly(x, y)
        a = M.p_eval(pp, val)
        b = M.p_eval(pp, val2)
        fac = Fraction(1)
        for k, i in enumerate(M.L):
            fac *= lam[(i, x[k])]
        for k, j in enumerate(M.R):
            fac *= mu[(j, y[k])]
        ncov += 1
        if b != fac * a:
            badcov += 1
print("C4b gauge covariance per_poly -> (prod lam)(prod mu) * per_poly: "
      "%d violations / %d" % (badcov, ncov))
res["C4_covariance_violations"] = badcov
res["C4_covariance_checks"] = ncov

# C4c MUTATION on the covariance checker: a wrong factor must be detected
badfac = sum(1 for x in list(M.LFREE)[:2] for y in [(0, 0, 0, 0)]
             if M.p_eval(M.per_poly(x, y), val2)
             != 2 * M.p_eval(M.per_poly(x, y), val))
print("C4c MUTATION (deliberately wrong gauge factor detected): %s"
      % (badfac > 0))
res["C4_mutation_detected"] = bool(badfac > 0)

json.dump(res, open("results_verify.json", "w"), indent=1, default=str)
print("\nALL CONTROLS WRITTEN to results_verify.json")

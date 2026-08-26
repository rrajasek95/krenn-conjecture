#!/usr/bin/env python3
"""W21 MOVE 2 -- CONTROL: reproduce W20's L-free/R-free permanent reduction
(0 / 4,860 mismatches) with an independent engine, plus mutation controls."""
import sys, os, json, random
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w21_c8core as G
from fractions import Fraction
from itertools import product

rng = random.Random(210815)
res = {"_header": "UNAUDITED W21 move-2 control: L-free/R-free permanent reduction."}
mis = tot = 0
for trial in range(3):
    bl = G.random_blocks(rng)
    for x in G.LFREE:
        for y in product(range(3), repeat=4):
            tot += 1
            if G.H_value(bl, G.C8_MEMBER, x + y) != G.per4(G.cross_matrix(bl, x, y)):
                mis += 1
    for y in G.RFREE:
        for x in product(range(3), repeat=4):
            tot += 1
            if G.H_value(bl, G.C8_MEMBER, x + y) != G.per4(G.cross_matrix(bl, x, y)):
                mis += 1
print("L-free/R-free reduction: %d mismatches / %d checks (%d per trial)" % (mis, tot, tot//3))
res["reduction_mismatches"] = mis
res["reduction_checks"] = tot

# MUTATION CONTROL 1: the reduction must FAIL on a non-free word
bl = G.random_blocks(rng)
nonfree = [w for w in product(range(3), repeat=8)
           if not G.lfree(w[:4]) and not G.rfree(w[4:])]
bad = sum(1 for w in nonfree[:400]
          if G.H_value(bl, G.C8_MEMBER, w) != G.per4(G.cross_matrix(bl, w[:4], w[4:])))
print("MUTATION control (non-free words): %d/400 differ from per (want >0)" % bad)
res["mutation_nonfree_differ"] = bad

# MUTATION CONTROL 2: planting a nonzero value in a dead cell must break it
bl2 = {e: [r[:] for r in bl[e]] for e in bl}
bl2[(0, 6)][1][0] = Fraction(7)
bad2 = sum(1 for x in G.LFREE for y in product(range(3), repeat=4)
           if G.H_value(bl2, G.C8_MEMBER, x + y) != G.per4(G.cross_matrix(bl2, x, y)))
print("MUTATION control (dead cell filled): %d/2430 mismatches (want 0 -- the "
      "reduction is about matchings, not the dead cell)" % bad2)
res["mutation_deadcell"] = bad2

# CONTROL 3: the L-free count and dead-cell-free words match W20
res["n_LFREE"] = len(G.LFREE); res["n_RFREE"] = len(G.RFREE)
res["deadfree_L"] = [list(x) for x in G.DEADFREE_L]
print("L-free %d  R-free %d  dead-cell-free L words %s"
      % (len(G.LFREE), len(G.RFREE), G.DEADFREE_L))
json.dump(res, open("results_c8check.json", "w"), indent=1, default=str)

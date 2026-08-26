#!/usr/bin/env python3
"""TIGHTNESS CONTROL for the kill.  The 81-equation system of the all-dirty
word x=(1,0,0,2) must be SATISFIABLE once zeros are allowed -- otherwise the
system would be trivially broken and the 'kill' would prove nothing about the
all-cells-nonzero requirement.  Zeroing the single L-row i=1 of every M_j^x
(11 occupied cells) puts every V_j inside the coordinate hyperplane {v_1=0},
which makes every 4x4 permanent vanish."""
import sys, json, random
from fractions import Fraction
sys.dont_write_bytecode = True
import m2core as M, m2sys as S
rng = random.Random(4242)
x=(1,0,0,2)
eqs, cells, labels = S.sys_words(lwords=[x])
val = {c: Fraction(rng.randint(1,9), rng.randint(1,4)) for c in cells}
zeroed = [c for c in cells if c[0]==1]          # L-site i=1 rows of every M_j
for c in zeroed: val[c]=Fraction(0)
bad = sum(1 for p in eqs if M.p_eval(p,val)!=0)
nz  = sum(1 for c in cells if val[c]==0)
print("x=%s : %d equations, %d cells"%(x,len(eqs),len(cells)))
print("  zeroing the %d occupied cells of L-row i=1 : violated equations = %d / %d ; zero cells = %d"
      %(len(zeroed), bad, len(eqs), nz))
# MUTATION: zero only PART of that row -> must NOT satisfy everything
val2 = dict(val)
for c in zeroed[:4]: val2[c]=Fraction(7)
bad2 = sum(1 for p in eqs if M.p_eval(p,val2)!=0)
print("  MUTATION (4 of those cells put back nonzero): violated = %d / %d (want >0)"%(bad2,len(eqs)))
json.dump({"word":list(x),"neqs":len(eqs),"ncells":len(cells),
           "zeroed_cells":len(zeroed),"violated_with_zero_row":bad,
           "mutation_violated":bad2}, open("results_tight.json","w"), indent=1)

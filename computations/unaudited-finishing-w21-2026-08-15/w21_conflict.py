#!/usr/bin/env python3
"""W21 -- RESOLVE THE MOVE-2 CONFLICT.  UNAUDITED.  Exact only.

Sub-probe SING claims THEOREM W21-M2: 'per cannot vanish identically on
V_4 x V_5 x V_6 x V_7 (subspaces of C^4) when all dim >= 2 and none lies in a
coordinate hyperplane.'
Sub-probe GEO claims an explicit COUNTEREXAMPLE over Q(omega), omega a
primitive cube root of unity:
   V_4 = V_5 = span{(1,0,1,b), (0,1,g,-w b g)}
   V_6 = V_7 = span{(1,0,w,w^2 b), (0,1,w^2 g,-w^2 b g)}
Exactly one can be right.  Arithmetic here is EXACT in Q(omega) = Q[w]/(w^2+w+1).
"""
import json, os, sys
from fractions import Fraction as Fr
from itertools import permutations, product
sys.dont_write_bytecode = True

# ---- exact arithmetic in Q(omega),  w^2 = -1 - w ----
class W:
    __slots__=("a","b")
    def __init__(s,a=0,b=0): s.a=Fr(a); s.b=Fr(b)
    def __add__(s,o): o=cw(o); return W(s.a+o.a, s.b+o.b)
    __radd__=__add__
    def __neg__(s): return W(-s.a,-s.b)
    def __sub__(s,o): return s+(-cw(o))
    def __rsub__(s,o): return cw(o)+(-s)
    def __mul__(s,o):
        o=cw(o)
        # (a+bw)(c+dw) = ac + (ad+bc)w + bd w^2 ; w^2 = -1-w
        ac=s.a*o.a; bd=s.b*o.b; mid=s.a*o.b+s.b*o.a
        return W(ac-bd, mid-bd)
    __rmul__=__mul__
    def __eq__(s,o): o=cw(o); return s.a==o.a and s.b==o.b
    def __repr__(s): return "(%s+%sw)"%(s.a,s.b)
    def iszero(s): return s.a==0 and s.b==0
def cw(x): return x if isinstance(x,W) else W(x,0)
OM=W(0,1)
# control: w^3 = 1 and w^2+w+1 = 0
assert (OM*OM*OM)==W(1,0) and (OM*OM+OM+W(1,0)).iszero()

def per4(cols):
    """permanent of the 4x4 matrix whose COLUMNS are cols[0..3]."""
    tot=W(0,0)
    for p in permutations(range(4)):
        t=W(1,0)
        for i in range(4): t=t*cols[p[i]][i]
        tot=tot+t
    return tot

def check_family(b,g,w):
    V45=[[W(1),W(0),W(1),cw(b)],[W(0),W(1),cw(g),-(w*cw(b)*cw(g))]]
    w2=w*w
    V67=[[W(1),W(0),w,w2*cw(b)],[W(0),W(1),w2*cw(g),-(w2*cw(b)*cw(g))]]
    bad=[]
    for i4 in range(2):
        for i5 in range(2):
            for i6 in range(2):
                for i7 in range(2):
                    v=per4([V45[i4],V45[i5],V67[i6],V67[i7]])
                    if not v.iszero(): bad.append(((i4,i5,i6,i7),repr(v)))
    return V45,V67,bad

res={"_header":"UNAUDITED W21 resolution of the move-2 conflict (Thm W21-M2 vs the cube-root family). Exact in Q(omega)."}
for (b,g) in ((1,1),(2,3),(Fr(1,2),5),(7,Fr(2,3))):
    V45,V67,bad=check_family(b,g,OM)
    print("b=%s g=%s : nonvanishing basis permanents %d/16" % (b,g,len(bad)))
    if bad: print("     first:",bad[0])
    res["family_b%s_g%s"%(b,g)]=dict(nonvanishing=len(bad),sample=bad[:2])
# MUTATION CONTROL: replace omega by 1 -> must NOT vanish
V45,V67,bad1=check_family(2,3,W(1,0))
print("MUTATION control (omega -> 1): nonvanishing basis permanents %d/16 (want > 0)"%len(bad1))
res["mutation_omega_to_1_nonvanishing"]=len(bad1)
# coordinate-hyperplane check: does some V lie in {v_i = 0}?
def in_coord_hyp(V):
    return [i for i in range(4) if all(v[i].iszero() for v in V)]
V45,V67,_=check_family(2,3,OM)
res["V45_coord_hyperplanes"]=in_coord_hyp(V45)
res["V67_coord_hyperplanes"]=in_coord_hyp(V67)
print("V45 lies in coordinate hyperplanes:",in_coord_hyp(V45),
      "| V67:",in_coord_hyp(V67),"(empty = none, so Thm W21-M2's hypotheses hold)")
json.dump(res,open("results_conflict.json","w"),indent=1,default=str)

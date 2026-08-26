#!/usr/bin/env python3
"""W21 MOVE 1 -- THE RANK-PRODUCT INEQUALITIES (from the K_4 tensor identity).
UNAUDITED.  Exact only.

For 3x3 matrices M_ab and the identity  M_12(x)M_34 + M_13(x)M_24 + M_14(x)M_23 = 0
regroup the 4-tensor as a 9x9 matrix.  In the grouping (a,b)|(c,d) the term
M_ab (x) M_cd has rank 1, while the other two terms are Kronecker-type
matrices of rank equal to the PRODUCT of the two factors' ranks.  Hence for
each of the three groupings the two Kronecker-type terms differ by a rank-<=1
matrix, giving

   |r_13 r_24 - r_14 r_23| <= 1,  |r_12 r_34 - r_14 r_23| <= 1,
   |r_12 r_34 - r_13 r_24| <= 1        (r_ab = rank M_ab)

i.e. THE THREE RANK PRODUCTS ARE PAIRWISE WITHIN 1 OF EACH OTHER.
At m = 26 the two absent R-edges (4,6) and (5,7) are exactly the images of
the L-pairs (1,3) and (0,2), which form ONE pairing; both those M's are
outright rank <= 1, so that product is <= 1 and the other two products are
<= 2:   rank M_(0,1) * rank M_(2,3) <= 2  and  rank M_(0,3) * rank M_(1,2) <= 2.
At m = 27 only (5,7) is absent, so only M_(0,2) is forced rank <= 1.
"""
import json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from itertools import product
import w21_core as K, w21_block as B
from w21_pf import load_w20_points

def kron_rank(M, Nn): return K.rank_of(M,3)*K.rank_of(Nn,3)

res={"_header":"UNAUDITED W21 rank-product inequalities. Exact only."}
pts=load_w20_points()
# (1) verify on RANDOM solutions of the identity?  none available a priori --
#     instead verify the PROOF STEP: the 9x9 regrouping ranks, on random M's.
import random
rng=random.Random(99)
bad=0
for _ in range(30):
    Ms={pr:[[Fraction(rng.randint(-6,6)) for _ in range(3)] for _ in range(3)] for pr in B.LPAIRS}
    # build the 9x9 matrices for grouping (0,1)|(2,3) and check ranks
    A=Ms[(0,1)]; D=Ms[(2,3)]; Bm=Ms[(0,2)]; Cm=Ms[(1,3)]
    N1=[[A[a][b]*D[c][d] for c in range(3) for d in range(3)] for a in range(3) for b in range(3)]
    N2=[[Bm[a][c]*Cm[b][d] for c in range(3) for d in range(3)] for a in range(3) for b in range(3)]
    if K.rank_of(N1,9)!=1: bad+=1
    if K.rank_of(N2,9)!=kron_rank(Bm,Cm): bad+=1
res["regrouping_rank_checks_bad"]=bad
print("regrouping rank facts (rank-1 term, Kronecker rank = product): %d bad / 60" % bad)

# (2) at the exact clean points: the three products at every full-box x
for m in (26,27,28):
    T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T); clean=K.clean_words(T)
    out=[]
    for tag,bl in pts[m][:1]:
        for x in B.full_box_words():
            P=B.hafL(bl,x)
            if P==0: continue
            Ms={pr:B.M_of(bl,gam,x,pr[0],pr[1],P) for pr in B.LPAIRS}
            prods=[K.rank_of(Ms[a],3)*K.rank_of(Ms[b],3) for a,b in B.PAIRINGS]
            ok=max(prods)-min(prods)<=1
            out.append(dict(x=list(x),products=prods,within_one=ok))
            print("m=%d x=%s: rank products over the three pairings %s (pairwise within 1: %s)" % (m,x,prods,ok))
    res["m%d"%m]=out
json.dump(res,open("results_rankprod.json","w"),indent=1,default=str)

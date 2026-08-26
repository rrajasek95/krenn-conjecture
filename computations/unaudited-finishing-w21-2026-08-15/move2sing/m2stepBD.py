#!/usr/bin/env python3
"""STEP BD (direct): for 2-dim V6,V7 with no zero row, the symmetric
zero-diagonal matrix A(v6,v7)[i][k] = v6[p]v7[q]+v6[q]v7[p] ({p,q} = comp{i,k})
CANNOT have rank <= 1 for every (v6,v7) in V6 x V7.
This is branch I of the (2,2,2,2) case of the W21-M2 theorem, verified in one
Singular computation per chart pair (8 variables)."""
import sys, json
from itertools import combinations, product
sys.dont_write_bytecode = True
import m2core as M, m2steps as S
COORDS=(0,1,2,3)
def run(rows6, rows7, char=0, tmo=300):
    N6,_,k = S.chart_mat(rows6,2,0)
    N7,_,k = S.chart_mat(rows7,2,k)
    polys=[]
    for a in range(2):
        for b in range(2):
            # A as a dict of string entries
            A={}
            for (i,kk) in combinations(COORDS,2):
                p,q = sorted(set(COORDS)-{i,kk})
                t1=S.mulstr(N6[p][a],N7[q][b]); t2=S.mulstr(N6[q][a],N7[p][b])
                s="+".join(x for x in (t1,t2) if x)
                A[(i,kk)]=A[(kk,i)]= s if s else "0"
            for i in COORDS: A[(i,i)]="0"
            for (r1,r2) in combinations(COORDS,2):
                for (c1,c2) in combinations(COORDS,2):
                    t1=S.mulstr("(%s)"%A[(r1,c1)] if A[(r1,c1)]!="0" else "0",
                                "(%s)"%A[(r2,c2)] if A[(r2,c2)]!="0" else "0")
                    t2=S.mulstr("(%s)"%A[(r1,c2)] if A[(r1,c2)]!="0" else "0",
                                "(%s)"%A[(r2,c1)] if A[(r2,c1)]!="0" else "0")
                    if t1 is None and t2 is None: continue
                    s = (t1 if t1 else "") + ("-"+t2 if t2 else "")
                    if s.startswith("-") and not t1: s = "-"+t2
                    polys.append(s)
    sat=[[N6[i][0],N6[i][1]] for i in COORDS if i not in rows6] + \
        [[N7[i][0],N7[i][1]] for i in COORDS if i not in rows7]
    return S.unit_test(k, polys, sat, char=char, timeout=tmo)
if __name__=="__main__":
    char=int(sys.argv[1]) if len(sys.argv)>1 else 0
    ok=bad=0; res=[]
    for r6 in combinations(COORDS,2):
        for r7 in combinations(COORDS,2):
            v=run(r6,r7,char=char)
            res.append({"rows6":list(r6),"rows7":list(r7),"unit":v})
            if v is True: ok+=1
            else:
                bad+=1; print("  *** STEP BD non-unit rows6=%s rows7=%s -> %s"%(r6,r7,v), flush=True)
    print("STEP BD (branch I of the (2,2,2,2) case): %d/%d chart pairs UNIT, %d not"%(ok,ok+bad,bad))
    json.dump(res, open("results_stepBD_c%d.json"%char,"w"), indent=1, default=str)

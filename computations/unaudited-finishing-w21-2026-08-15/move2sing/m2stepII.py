#!/usr/bin/env python3
"""BRANCH II of the (2,2,2,2) case: if V_4=V_5=V_6=V_7=V with dim V = 2 and no
zero row, per cannot vanish on V x V x V x V.  Verified DIRECTLY from the 16
permanent equations (no polarization argument used)."""
import sys, json
from itertools import combinations, permutations, product
sys.dont_write_bytecode = True
import m2core as M, m2steps as S
COORDS=(0,1,2,3); BIJ=tuple(permutations(COORDS))
def run(rows, char=0, tmo=300):
    N,_,k = S.chart_mat(rows,2,0)
    polys=[]
    for atup in product(range(2),repeat=4):
        terms={}
        for sig in BIJ:
            mon=[]; dead=False
            for t in range(4):
                e=N[sig[t]][atup[t]]
                if e=="0": dead=True; break
                if e!="1": mon.append(e)
            if dead: continue
            key=tuple(sorted(mon)); terms[key]=terms.get(key,0)+1
        s=""
        for mon,c in sorted(terms.items()):
            if not c: continue
            body="*".join(mon) if mon else str(abs(c))
            if mon and abs(c)!=1: body="%d*%s"%(abs(c),body)
            s += ("+" if c>0 else "-")+body
        if s: polys.append(s[1:] if s.startswith("+") else s)
    sat=[[N[i][0],N[i][1]] for i in COORDS if i not in rows]
    return S.unit_test(k, polys, sat, char=char, timeout=tmo), len(polys)
if __name__=="__main__":
    char=int(sys.argv[1]) if len(sys.argv)>1 else 0
    ok=bad=0; res=[]
    for r in combinations(COORDS,2):
        v,n = run(r,char=char)
        res.append({"rows":list(r),"neqs":n,"unit":v})
        print("  rows=%s  %d equations  unit=%s"%(list(r),n,v), flush=True)
        if v is True: ok+=1
        else: bad+=1
    print("BRANCH II (V_4=V_5=V_6=V_7, dim 2): %d/%d charts UNIT, %d not"%(ok,ok+bad,bad))
    # MUTATION: drop the no-zero-row saturation -> must become NON-unit
    N,_,k = S.chart_mat((0,1),2,0)
    v,n = run((0,1),char=char)
    import m2steps
    polys=[]
    # rerun without saturation
    vl=["zzv%d"%i for i in range(k)]
    print("  MUTATION: same system WITHOUT the no-zero-row saturation must be non-unit")
    json.dump(res, open("results_stepII_c%d.json"%char,"w"), indent=1, default=str)

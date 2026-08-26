import sys, json
from itertools import combinations, permutations, product
sys.dont_write_bytecode = True
import m2steps as S, m2stepII as II, m2stepBD as BD
COORDS=(0,1,2,3)
out={}
# MUTATION 1: branch II WITHOUT the no-zero-row saturation must be NON-unit
# (V inside a coordinate hyperplane IS a genuine solution).
import m2core as M
def run_nosat(rows, char=0):
    N,_,k = S.chart_mat(rows,2,0)
    polys=[]
    BIJ=tuple(permutations(COORDS))
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
    return S.unit_test(k, polys, [], char=char)
r = run_nosat((0,1))
print("MUTATION branchII no-saturation: unit=%s (want False -- V in a coordinate hyperplane IS a solution)"%r)
out["mut_branchII_nosat_unit"]=r
# MUTATION 2: branch I (STEP BD) without saturation must be non-unit
import m2steps
def bd_nosat(r6,r7,char=0):
    N6,_,k = S.chart_mat(r6,2,0); N7,_,k = S.chart_mat(r7,2,k)
    polys=[]
    for a in range(2):
        for b in range(2):
            A={}
            for (i,kk) in combinations(COORDS,2):
                p,q = sorted(set(COORDS)-{i,kk})
                t1=S.mulstr(N6[p][a],N7[q][b]); t2=S.mulstr(N6[q][a],N7[p][b])
                s="+".join(x for x in (t1,t2) if x); A[(i,kk)]=A[(kk,i)]= s if s else "0"
            for i in COORDS: A[(i,i)]="0"
            for (r1,r2) in combinations(COORDS,2):
                for (c1,c2) in combinations(COORDS,2):
                    t1=S.mulstr("(%s)"%A[(r1,c1)] if A[(r1,c1)]!="0" else "0","(%s)"%A[(r2,c2)] if A[(r2,c2)]!="0" else "0")
                    t2=S.mulstr("(%s)"%A[(r1,c2)] if A[(r1,c2)]!="0" else "0","(%s)"%A[(r2,c1)] if A[(r2,c1)]!="0" else "0")
                    if t1 is None and t2 is None: continue
                    s=(t1 if t1 else "")+("-"+t2 if t2 else "")
                    if s.startswith("-") and not t1: s="-"+t2
                    polys.append(s)
    return S.unit_test(k, polys, [], char=char)
r2 = bd_nosat((0,1),(0,1))
print("MUTATION branchI(BD) no-saturation: unit=%s (want False)"%r2)
out["mut_branchBD_nosat_unit"]=r2
# MUTATION 3: FACT A with the dead cell REMOVED but a fake dead cell elsewhere
json.dump(out, open("results_mutations.json","w"), indent=1, default=str)

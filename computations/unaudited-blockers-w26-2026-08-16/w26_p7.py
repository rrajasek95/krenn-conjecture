#!/usr/bin/env python3
"""W26 -- diagnose the p=7, m=25 det-M failures.  UNAUDITED.  Exact (F_p).

HYPOTHESIS.  The det M = 0 lemma is UNCONDITIONAL only where the
coefficient vector Psi cannot vanish.  Per w26_psi.py:
   m=25, k=7 : Psi[D0] = D1 l23 r56          -- a MONOMIAL, never 0  => unconditional
   m=25, k=5 : Psi[D2] = D1 l03 r67          -- a MONOMIAL, never 0  => unconditional
   m=25, k=4 : Psi[D1] = D0 l23 r56 + D2 l03 r67  -- NOT a monomial;
               Psi[r45] = h r67, Psi[r47] = h r56, so the all-zero branch
               needs h = hafL = 0 together with D0 l23 r56 + D2 l03 r67 = 0.
               That branch is REACHABLE, so det M = 0 is NOT unconditional
               at m=25, k=4.
   m=26, all k : the l02 l13 contradiction makes every k unconditional.
So the failures should ALL be at k=4 (R4) and should ALL have h = 0.
"""
import json, os, random, sys
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import w26_core as C
import w26_charp as CP
RES=os.path.join(HERE,"results_p7.json")
OUT={"_header":"UNAUDITED W26 diagnosis of the p=7 m=25 det-M failures."}
def ck(): json.dump(OUT,open(RES,"w"),indent=1,default=str)

def main():
    recs=[]
    for p in (7,13,31,37,43,29):
        for m in (25,26,27):
            gam=C.gamma_edges(C.TEMPLATES[m]); gs=set(gam); clean=C.clean_words(m)
            per={"R7":[0,0],"R4":[0,0]}    # [tests, nonzero]
            hzero_at_fail=0; fails=[]
            npts=0
            for kk in range(3000):
                rng=random.Random(101_000+p*1000+m*17+kk)
                bl=CP.seed_p(gam,gs,rng,p)
                if bl is None: continue
                order=list(range(8)); rng.shuffle(order)
                for _ps in range(4):
                    for t in order: CP.site_p(bl,gs,gam,t,clean,rng,p)
                if any(CP.hafp(bl,gs,tuple(range(8)),w,p)!=0 for w in clean): continue
                if not all(bl[e][i][j]%p!=0 for e in gam for i in range(3) for j in range(3)): continue
                npts+=1
                for lab,fn,fire in CP.V3[m]:
                    for a in range(3):
                        for b in range(3):
                            for c in range(3):
                                M=fn(bl,a,b,c); per[lab][0]+=1
                                if CP.det3p(M,p)!=0:
                                    per[lab][1]+=1
                                    # is hafL = 0 at the relevant L-word?
                                    # k=4: the L-word is x=(x0,a,x2,x3); we
                                    # only know x1=a, so test ALL x with x1=a
                                    hz=all(_haf(bl,(x0,a,x2,x3),p)==0
                                           for x0 in range(3) for x2 in range(3)
                                           for x3 in range(3)) if lab=="R4" else None
                                    fails.append((lab,a,b,c,hz))
                if npts>=12: break
            nh=sum(1 for f in fails if f[0]=="R4")
            rec=dict(p=p,m=m,n_points=npts,
                     R7_tests=per["R7"][0],R7_nonzero=per["R7"][1],
                     R4_tests=per["R4"][0],R4_nonzero=per["R4"][1],
                     n_fail=len(fails),n_fail_at_R4=nh,
                     all_fails_at_R4=(len(fails)==nh),
                     sample=fails[:4])
            recs.append(rec); OUT["records"]=recs; ck()
            print("p=%2d m=%d pts=%2d | R7 nonzero %d/%d | R4 nonzero %d/%d | all fails at R4: %s"
                  %(p,m,npts,per["R7"][1],per["R7"][0],per["R4"][1],per["R4"][0],
                    len(fails)==nh),flush=True)
    ck(); print("DONE")

def _haf(bl,x,p):
    L=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    g=lambda a,b: bl[(a,b)][x[a]][x[b]]%p
    return (g(0,1)*g(2,3)+g(0,2)*g(1,3)+g(0,3)*g(1,2))%p

if __name__=="__main__": main()

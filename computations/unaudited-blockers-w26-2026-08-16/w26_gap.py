#!/usr/bin/env python3
"""W26 -- the EXACT RESIDUAL GAP in Theorem W26-K.  UNAUDITED.  Exact only.

Theorem W26-K reduces the kill at a 3-block single-letter vertex v (firing
letter t*) to:  the firing row of the slice matrix M lies in the span of
the two clean rows.  det M = 0 is PROVED (m=25,26; and m=27 at R7 in the
det-branch).  det M = 0 gives the conclusion UNLESS the two clean rows are
PROPORTIONAL while the firing row is outside their line -- the GAP.

This file measures the gap directly, over ALL index choices (not a sample):
  GAPHIT(v) := exists (free indices) with  rank{clean rows} = 1  and
               rank{clean rows, firing row} = 2.
It also reports, for every point, whether det M = 0 everywhere and whether
Phi vanishes at every firing-letter word of v.
"""
import json, os, random, sys
from fractions import Fraction
from itertools import product
sys.dont_write_bytecode = True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import w26_core as C, w26_fast as F, w26_sub as SB
RES=os.path.join(HERE,"results_gap.json"); OUT={"_header":
  "UNAUDITED W26 residual-gap measurement for Theorem W26-K."}
def ck(): json.dump(OUT,open(RES,"w"),indent=1,default=str)

# 3-block single-letter vertices, per m.  (label, blocks as (edge, which
# index of the edge carries the slice letter), free index descriptors)
def slices_R7(bl,m,x0,y4,y6):
    return [[bl[(0,7)][x0][t], bl[(4,7)][y4][t], bl[(6,7)][y6][t]] for t in range(3)]
def slices_R4(bl,m,x1,y5,y7):
    return [[bl[(1,4)][x1][t], bl[(4,5)][t][y5], bl[(4,7)][t][y7]] for t in range(3)]
def slices_L3(bl,m,x0,x1,x2):     # blocks A_03,A_13,A_23 (+A_36 if present)
    return [[bl[(0,3)][x0][t], bl[(1,3)][x1][t], bl[(2,3)][x2][t]] for t in range(3)]

VERT3={25:[("R7",slices_R7,2),("R4",slices_R4,0),("L3",slices_L3,2)],
       26:[("R7",slices_R7,2),("R4",slices_R4,0)],
       27:[("R7",slices_R7,2)],
       28:[]}
def rk(rows):
    R,p=C.rref([list(r) for r in rows],len(rows[0])); return len(p)
def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
           -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
           +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
def analyse(m,bl):
    rec={}
    for lab,fn,fire in VERT3[m]:
        nd=bd=gap=rank1=0; n=0
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    M=fn(bl,m,a,b,c); n+=1
                    if det3(M)!=0: bd+=1
                    cl=[M[t] for t in range(3) if t!=fire]
                    rc=rk(cl); ra=rk(cl+[M[fire]])
                    if rc==1: rank1+=1
                    if rc==1 and ra==2: gap+=1
        rec[lab]=dict(n=n,det_nonzero=bd,clean_rows_rank1=rank1,GAP=gap)
    return rec
def main():
    import w26_pts as PT
    ADV=os.path.join(HERE,"adv"); OUT["battery"]={}
    for name,m,path,keys in [("P1_m25",25,os.path.join(ADV,"results_case2b.json"),("main","point")),
                             ("P2_m26",26,os.path.join(ADV,"results_solo.json"),("m26","point")),
                             ("P3_m27",27,os.path.join(ADV,"results_solo.json"),("m27","point"))]:
        if not os.path.exists(path): continue
        d=json.load(open(path))
        for k in keys: d=d[k]
        bl={tuple(int(t) for t in k.strip("()").split(",")):[[Fraction(x) for x in r] for r in v] for k,v in d.items()}
        r=analyse(m,bl); OUT["battery"][name]=r
        print("%-8s m=%d  %s"%(name,m,r),flush=True); ck()
    OUT["stored"]=[]
    for m,tag,bl in PT.stored_points():
        r=analyse(m,bl); r.update(m=m,tag=tag)
        OUT["stored"].append(r); print("stored m=%d %-20s %s"%(m,tag[:20],
            {k:(v["det_nonzero"],v["clean_rows_rank1"],v["GAP"]) for k,v in r.items() if k in ("R7","R4","L3")}),flush=True); ck()
    OUT["fresh"]=[]
    for m in (25,26,27):
        mdl=F.Model(m); got=0
        for kk in range(800):
            rng=random.Random(66_000_000+1000*m+kk); order=list(range(8)); rng.shuffle(order)
            bl=F.make_point(mdl,rng,passes=4,order=order)
            if bl is None: continue
            r=analyse(m,bl); r.update(m=m,tag="fresh%d"%kk,van=mdl.vanishing(bl))
            OUT["fresh"].append(r)
            print("fresh m=%d #%-4d van=%-5s %s"%(m,kk,r["van"],
                {k:(v["det_nonzero"],v["clean_rows_rank1"],v["GAP"]) for k,v in r.items() if k in ("R7","R4","L3")}),flush=True)
            ck(); got+=1
            if got>=10: break
    # OUT-OF-LOCUS control
    nb=0
    for m in (25,26,27):
        gam=C.gamma_edges(C.TEMPLATES[m]); rng=random.Random(5150+m)
        for _ in range(4):
            bl={e:[[Fraction(rng.randint(-9,9) or 5,rng.randint(1,4)) for _ in range(3)] for _ in range(3)] for e in gam}
            r=analyse(m,bl); nb += any(v["det_nonzero"]>0 for v in r.values())
    print("OUT-OF-LOCUS CONTROL: random non-clean points with det M != 0: %d/12 (want 12)"%nb)
    OUT["out_of_locus"]=nb; ck(); print("DONE")
if __name__=="__main__": main()

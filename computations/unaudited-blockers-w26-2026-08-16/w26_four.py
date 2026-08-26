#!/usr/bin/env python3
"""W26 -- THE FOUR SINGLE-LETTER VERTICES.  UNAUDITED.  Exact only.

Four vertices have ALL their singles firing at ONE letter of ONE coordinate:
    R-vertex 4 : (0,4),(2,4),(3,4)  all at y4 = 0   (triggers x0=0,x2=1,x3=2)
    R-vertex 7 : (1,7),(2,7),(3,7)  all at y7 = 2   (triggers x1=0,x2=1,x3=2)
    L-vertex 0 : (0,4),(0,5),(0,6)  all at x0 = 0   (triggers y4=0,y5=1,y6=2)
    L-vertex 3 : (3,4),(3,5),(3,7)  all at x3 = 2   (triggers y4=0,y5=1,y7=2)
For each, Phi restricted to the three letters of that coordinate is
<Psivec, row_t(M)> with M the 3 x (#Gamma blocks at the vertex) slice
matrix.  This file measures, at exact clean points: rank M, whether the
firing row lies in the span of the clean rows, and whether the singles at
that vertex in fact all have ALL-PURE solo families.
"""
import json, os, random, sys
from fractions import Fraction
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import w26_core as C, w26_fast as F, w26_sub as SB

RES = os.path.join(HERE, "results_four.json"); OUT = {"_header":
    "UNAUDITED W26 four single-letter vertices."}
def ck(): json.dump(OUT, open(RES,"w"), indent=1, default=str)

# (label, kind, coordinate, firing letter, singles)
VERT = [("R4","R",4,0,[(0,4),(2,4),(3,4)]), ("R7","R",7,2,[(1,7),(2,7),(3,7)]),
        ("L0","L",0,0,[(0,4),(0,5),(0,6)]), ("L3","L",3,2,[(3,4),(3,5),(3,7)])]

def blocks_at(m, kind, v):
    gs = set(C.gamma_edges(C.TEMPLATES[m])); out=[]
    if kind=="R":
        p=C.SIGINV[v]
        if (p,v) in gs: out.append((p,v))
        for u in C.R:
            if u!=v:
                e=(min(u,v),max(u,v))
                if e in gs: out.append(e)
    else:
        if (v,C.SIG[v]) in gs: out.append((v,C.SIG[v]))
        for u in C.L:
            if u!=v:
                e=(min(u,v),max(u,v))
                if e in gs: out.append(e)
    return out

def rank_of(rows):
    R,p = C.rref([list(r) for r in rows], len(rows[0])); return len(p)

def analyse(m, bl):
    gs=set(C.gamma_edges(C.TEMPLATES[m])); T=C.TEMPLATES[m]
    sing=C.single_edges(T); lv=set(C.live_singles(m)); rec={}
    for lab,kind,v,fire,ss in VERT:
        bks=blocks_at(m,kind,v); nb=len(bks)
        clean_rows=[t for t in range(3) if t!=fire]
        stats={"n":0,"rank1":0,"rank2":0,"rank3":0,"fire_in_span":0,
               "n_blocks":nb}
        # sample the free indices of the slice matrix
        rng=random.Random(11)
        for _ in range(60):
            # random assignment of the OTHER coordinates
            w=[rng.randrange(3) for _ in range(8)]
            def slice_vec(e):
                # the vector over the letter t of the coordinate at v
                out=[]
                for t in range(3):
                    ww=list(w); 
                    if kind=="R": ww[v]=t
                    else: ww[v]=t
                    out.append(bl[e][ww[e[0]]][ww[e[1]]])
                return out
            M=[[slice_vec(e)[t] for e in bks] for t in range(3)]
            r=rank_of(M); stats["n"]+=1; stats["rank%d"%min(r,3)]+=1
            cr=[M[t] for t in clean_rows]
            rc=rank_of(cr) if any(any(x for x in row) for row in cr) else 0
            rall=rank_of(cr+[M[fire]])
            stats["fire_in_span"] += (rall==rc)
        # do the singles at this vertex actually have all-pure solo families?
        pur={}
        for e in ss:
            if e not in lv: continue
            r=SB.solo_report(m,bl,e)
            pur[str(e)]=dict(n_solo=r["n_solo"],n_pure=r["n_pure"],
                             all_pure=(r["n_pure"]==r["n_solo"]),
                             any_pure=(r["n_pure"]>0),survives=r["survives"])
        stats["singles"]=pur
        stats["any_single_has_pure"]=any(v2["any_pure"] for v2 in pur.values())
        rec[lab]=stats
    rec["some_vertex_delivers"]=any(rec[l]["any_single_has_pure"] for l,_,_,_,_ in VERT)
    return rec

def main():
    import w26_pts as PT
    ADV=os.path.join(HERE,"adv")
    OUT["battery"]={}
    for name,m,path,keys in [("P1_m25",25,os.path.join(ADV,"results_case2b.json"),("main","point")),
                             ("P2_m26",26,os.path.join(ADV,"results_solo.json"),("m26","point")),
                             ("P3_m27",27,os.path.join(ADV,"results_solo.json"),("m27","point"))]:
        if not os.path.exists(path): continue
        d=json.load(open(path))
        for k in keys: d=d[k]
        bl={tuple(int(t) for t in k.strip("()").split(",")):[[Fraction(x) for x in r] for r in v] for k,v in d.items()}
        r=analyse(m,bl); OUT["battery"][name]=r
        print("%-8s m=%d  %s"%(name,m," | ".join(
            "%s:blk%d rk(%d/%d/%d) firespan %d/%d pure=%s"%(l,r[l]["n_blocks"],
              r[l]["rank1"],r[l]["rank2"],r[l]["rank3"],r[l]["fire_in_span"],r[l]["n"],
              r[l]["any_single_has_pure"]) for l,_,_,_,_ in VERT)),flush=True)
        ck()
    OUT["stored"]=[]
    for m,tag,bl in PT.stored_points():
        r=analyse(m,bl); r.update(m=m,tag=tag,van=PT.vanishing_stratum(m,bl))
        OUT["stored"].append(r)
        print("stored m=%d %-20s van=%-5s deliver=%s  %s"%(m,tag[:20],r["van"],r["some_vertex_delivers"],
            " ".join("%s=%s"%(l,r[l]["any_single_has_pure"]) for l,_,_,_,_ in VERT)),flush=True)
        ck()
    OUT["fresh"]=[]
    for m in (25,26,27,28):
        mdl=F.Model(m); got=0
        for kk in range(600):
            rng=random.Random(88_000_000+1000*m+kk); order=list(range(8)); rng.shuffle(order)
            bl=F.make_point(mdl,rng,passes=4,order=order)
            if bl is None: continue
            r=analyse(m,bl); r.update(m=m,tag="fresh%d"%kk,van=mdl.vanishing(bl))
            OUT["fresh"].append(r)
            print("fresh m=%d #%-4d van=%-5s deliver=%s  %s"%(m,kk,r["van"],r["some_vertex_delivers"],
                " ".join("%s=%s"%(l,r[l]["any_single_has_pure"]) for l,_,_,_,_ in VERT)),flush=True)
            ck(); got+=1
            if got>=8: break
    print("DONE")
if __name__=="__main__": main()

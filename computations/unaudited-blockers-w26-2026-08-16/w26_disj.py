#!/usr/bin/env python3
"""W26 -- THE VERTEX DISJUNCTION.  UNAUDITED.  Exact only.

By Theorem W26-M (R-vertices) and W26-M* (L-vertices), at EVERY vertex v of
the model and every support m, Phi restricted to the three letters of v's
coordinate satisfies a THREE-vector equation

    R-vertex k (p = sigma^-1 k):   h * Phi(t) = sum_{q != p} Psi_q W_q(t),
        W_q(t) = D_q l_ij * A_{p,k}[x_p][t]  +  h * A_{k,sigma q}-slice(t)
    L-vertex p:                 hafR * Phi(s) = sum_{a != p} Xi_a V_a(s),
        V_a(s) = D_a r_{sigma b sigma c} * A_{p,sigma p}[s][y] + hafR * A_pa-slice(s)

Let T_c = letters at which the word is CLEAN and T_f = letters at which some
single into v fires.  The coefficient vector is orthogonal to {row_t : t in
T_c}.  Say the vertex DELIVERS at this index choice if

        row_{t_f}  in  span{ row_t : t in T_c }   for every t_f in T_f,

because then Phi(t_f) = 0, i.e. a PURE ROW, which kills.

This file computes, exactly, for all EIGHT vertices at every point:
  * whether the vertex delivers at some index choice (DELIVERS),
  * the LETTER COLLAPSE flag (two clean rows proportional at every index
    choice -- the side-condition that made Theorem W26-K's m=27 case fail),
  * whether h (resp. hafR) vanishes identically over the family,
and then tests the DISJUNCTION: some vertex always delivers.
"""
import json, os, random, sys
from fractions import Fraction
from itertools import combinations, product
sys.dont_write_bytecode = True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import w26_core as C, w26_fast as F, w26_sub as SB

RES=os.path.join(HERE,"results_disj.json")
OUT={"_header":"UNAUDITED W26 vertex disjunction (W26-M / W26-M* at all 8 vertices)."}
def ck(): json.dump(OUT,open(RES,"w"),indent=1,default=str)

SING={}
def singles_at(m):
    if m in SING: return SING[m]
    T=C.TEMPLATES[m]; sg=C.single_edges(T); lv=set(C.live_singles(m))
    d={}
    for e,(a,b) in sg.items():
        if e not in lv: continue
        d.setdefault(('R',e[1]),[]).append((e,e[0],a,b))   # trigger x_{e0}=a, letter y_{e1}=b
        d.setdefault(('L',e[0]),[]).append((e,e[1],b,a))   # trigger y_{e1}=b, letter x_{e0}=a
    SING[m]=d; return d

def rk(rows):
    rows=[r for r in rows]
    if not rows: return 0
    R,p=C.rref([list(r) for r in rows],len(rows[0])); return len(p)

def analyse(m,bl,nsample=40,seed=5):
    gs=set(C.gamma_edges(C.TEMPLATES[m])); T=C.TEMPLATES[m]
    sg=C.single_edges(T); lv=set(C.live_singles(m)); sat=singles_at(m)
    rng=random.Random(seed); rec={}
    def cl(u,v,a,b):
        e=(u,v) if u<v else (v,u)
        if e not in gs: return Fraction(0)
        return bl[e][a][b] if u<v else bl[e][b][a]
    for kind,v in [('R',4),('R',5),('R',6),('R',7),('L',0),('L',1),('L',2),('L',3)]:
        lab="%s%d"%(kind,v)
        delivered=False; ncollapse=0; nidx=0; nzero_scale=0; ndeliver=0
        for _ in range(nsample):
            w=[rng.randrange(3) for _ in range(8)]
            # which singles at this vertex are triggered by the OTHER coords?
            fire=set()
            for (e,trig,tv,letter) in sat.get((kind,v),[]):
                if kind=='R':
                    if w[trig]==tv: fire.add(letter)
                else:
                    if w[trig]==tv: fire.add(letter)
            if not fire: continue
            # the words at the other letters must be clean: check directly
            def word(t):
                ww=list(w); ww[v]=t; return tuple(ww)
            clean_ts=[t for t in range(3) if t not in fire]
            # verify those really are clean words (no OTHER single active)
            okfam=True
            for t in clean_ts:
                ww=word(t)
                if len(set(ww))==1: okfam=False; break
                act=[f for f in lv if ww[f[0]]==sg[f][0] and ww[f[1]]==sg[f][1]]
                if act: okfam=False; break
            if not okfam: continue
            # also the firing words must have ONLY singles at v active
            for t in fire:
                ww=word(t)
                if len(set(ww))==1: okfam=False; break
                act=[f for f in lv if ww[f[0]]==sg[f][0] and ww[f[1]]==sg[f][1]]
                if any((f[1] if kind=='R' else f[0])!=v for f in act): okfam=False; break
            if not okfam: continue
            nidx+=1
            # build the three W (or V) vectors
            x,y=w[:4],w[4:]
            ll={(a,b):cl(a,b,x[a],x[b]) for a,b in combinations(range(4),2)}
            h=ll[(0,1)]*ll[(2,3)]+ll[(0,2)]*ll[(1,3)]+ll[(0,3)]*ll[(1,2)]
            hR=(cl(4,5,y[0],y[1])*cl(6,7,y[2],y[3])+cl(4,6,y[0],y[2])*cl(5,7,y[1],y[3])
                +cl(4,7,y[0],y[3])*cl(5,6,y[1],y[2]))
            rows=[]
            if kind=='R':
                p=C.SIGINV[v]
                if h==0: nzero_scale+=1; continue
                cols=[]
                for q in range(4):
                    if q==p: continue
                    i,j=[t for t in range(4) if t not in (p,q)]
                    lij=ll[(min(i,j),max(i,j))]
                    Dq=cl(q,C.SIG[q],x[q],y[C.SIG[q]-4])
                    colv=[]
                    for t in range(3):
                        gsl=cl(p,v,x[p],t)
                        u2=C.SIG[q]
                        e2=(min(v,u2),max(v,u2))
                        if e2 in gs:
                            la=t if e2[0]==v else y[e2[0]-4]
                            lb=t if e2[1]==v else y[e2[1]-4]
                            rsl=bl[e2][la][lb]
                        else: rsl=Fraction(0)
                        colv.append(Dq*lij*gsl+h*rsl)
                    cols.append(colv)
            else:
                p=v
                if hR==0: nzero_scale+=1; continue
                cols=[]
                for a in range(4):
                    if a==p: continue
                    b,c=[t for t in range(4) if t not in (p,a)]
                    rbc=cl(C.SIG[b],C.SIG[c],y[C.SIG[b]-4],y[C.SIG[c]-4])
                    Da=cl(a,C.SIG[a],x[a],y[C.SIG[a]-4])
                    colv=[]
                    for s in range(3):
                        sg2=cl(p,C.SIG[p],s,y[C.SIG[p]-4])
                        e2=(min(p,a),max(p,a))
                        lsl=bl[e2][s][x[a]] if e2[0]==p else bl[e2][x[a]][s]
                        colv.append(Da*rbc*sg2+hR*lsl)
                    cols.append(colv)
            rows=[[cols[j][t] for j in range(3)] for t in range(3)]
            cleanrows=[rows[t] for t in clean_ts]
            rc=rk(cleanrows)
            if rc<=1 and len(clean_ts)>1: ncollapse+=1
            ok=all(rk(cleanrows+[rows[t]])==rc for t in fire)
            if ok: ndeliver+=1; delivered=True
        rec[lab]=dict(n_idx=nidx,n_deliver=ndeliver,n_collapse=ncollapse,
                      n_zero_scale=nzero_scale,DELIVERS=delivered)
    # ground truth: which singles actually have pure rows
    pr={}
    for e in C.live_singles(m):
        r=SB.solo_report(m,bl,e); pr[str(e)]=r["n_pure"]
    rec["pure_rows"]=pr
    rec["some_pure"]=any(v2>0 for v2 in pr.values())
    rec["DISJUNCTION_holds"]=any(rec[l]["DELIVERS"] for l in
        ["R4","R5","R6","R7","L0","L1","L2","L3"])
    return rec

def main():
    import w26_pts as PT
    import w26_wide as W
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
        print("%-8s m=%d DISJ=%s delivering=%s"%(name,m,r["DISJUNCTION_holds"],
            [l for l in ["R4","R5","R6","R7","L0","L1","L2","L3"] if r[l]["DELIVERS"]]),flush=True); ck()
    OUT["stored"]=[]
    for m,tag,bl in PT.stored_points():
        r=analyse(m,bl); r.update(m=m,tag=tag,van=PT.vanishing_stratum(m,bl))
        OUT["stored"].append(r)
        print("stored m=%d %-20s van=%-5s DISJ=%s deliver=%s"%(m,tag[:20],r["van"],r["DISJUNCTION_holds"],
            "".join("1" if r[l]["DELIVERS"] else "0" for l in ["R4","R5","R6","R7","L0","L1","L2","L3"])),flush=True); ck()
    OUT["fresh"]=[]
    for m in (25,26,27,28):
        mdl=F.Model(m); got=0
        for kk in range(4000):
            rng=random.Random(31_000_000+1000*m+kk); order=list(range(8)); rng.shuffle(order)
            bl=W.make(mdl,rng,passes=4,order=order)
            if bl is None: continue
            r=analyse(m,bl); r.update(m=m,tag="fresh%d"%kk,van=mdl.vanishing(bl))
            OUT["fresh"].append(r)
            print("fresh m=%d #%-4d van=%-5s DISJ=%s deliver=%s some_pure=%s"%(m,kk,r["van"],
                r["DISJUNCTION_holds"],
                "".join("1" if r[l]["DELIVERS"] else "0" for l in ["R4","R5","R6","R7","L0","L1","L2","L3"]),
                r["some_pure"]),flush=True); ck()
            got+=1
            if got>=25: break
    ck(); print("DONE")
if __name__=="__main__": main()

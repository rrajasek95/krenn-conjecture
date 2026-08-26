#!/usr/bin/env python3
"""W20 -- RESIDUAL 2: the constants-pinned feasibility probe, OPTIMISED.
UNAUDITED.  FLOATS ARE USED FOR SEARCH ONLY -- no verdict rests on them.

Same scheme as w20_c8search2.py (alternating constrained least squares on the
site-linear systems, with H_{c^8} pinned to 1 -- a legitimate gauge
normalisation), but with the matching structure precomputed once.

CONTROLS
  negative: W8's m=24 (dead, W15/A6) and m=25 (dead, W19) -- must NOT converge;
  positive: the same template with an under-determined random word subset.
"""
from __future__ import annotations
import os,sys,json
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import w20_core as C
from w20_c8search import site_unknowns, build_index

def precompute(T, words):
    idx=build_index(T); n=len(idx)
    sup={w:C.support(T,w) for w in words}
    mon={}
    for w in words:
        mon[w]=[tuple(idx[(e,C.cell_index(e,w))] for e in C.PM_E[mi]) for mi in sup[w]]
    su={t:site_unknowns(T,t) for t in range(8)}
    # per (t,c): list of (row index list) -> for each word, list of (unk_pos, other_idx tuple)
    tables={}
    for t in range(8):
        for c in range(3):
            unk=su[t][c]
            if not unk: continue
            gpos={idx[u]:k for k,u in enumerate(unk)}
            rows=[]
            for w in words:
                if w[t]!=c: continue
                ent=[]
                for mm in mon[w]:
                    key=None; rest=[]
                    for g in mm:
                        if g in gpos: key=g
                        else: rest.append(g)
                    if key is not None: ent.append((gpos[key],tuple(rest)))
                if ent: rows.append(ent)
            cw=(c,)*8
            aent=[]
            cwmon=[tuple(idx[(e,C.cell_index(e,cw))] for e in C.PM_E[mi])
                   for mi in C.support(T,cw)]
            if True:
                for mm in cwmon:
                    key=None; rest=[]
                    for g in mm:
                        if g in gpos: key=g
                        else: rest.append(g)
                    if key is not None: aent.append((gpos[key],tuple(rest)))
            tables[(t,c)]=(len(unk),[idx[u] for u in unk],rows,aent)
    return idx,n,mon,tables

def build(rows,nu,vals):
    M=np.zeros((len(rows),nu))
    for r,ent in enumerate(rows):
        for k,rest in ent:
            p=1.0
            for g in rest: p*=vals[g]
            M[r,k]+=p
    return M

def resid(mon,words,vals):
    tot=0.0
    for w in words:
        s=0.0
        for mm in mon[w]:
            p=1.0
            for g in mm: p*=vals[g]
            s+=p
        tot+=s*s
    return tot

def probe(T,words,seed,iters=80,ridge=1e-11,pre=None):
    idx,n,mon,tables = pre if pre else precompute(T,words)
    rng=np.random.default_rng(seed)
    vals=rng.normal(size=n); vals[np.abs(vals)<0.3]=0.7
    hist=[]
    for it in range(iters):
        for (t,c),(nu,gl,rows,aent) in tables.items():
            if not rows or not aent: continue
            M=build(rows,nu,vals)
            a=build([aent],nu,vals)[0]
            if not np.any(a): continue
            A=M.T@M+ridge*np.eye(nu)
            try: z=np.linalg.solve(A,a)
            except np.linalg.LinAlgError: continue
            den=a@z
            if abs(den)<1e-300 or not np.all(np.isfinite(z)): continue
            v=z/den
            for k,g in enumerate(gl): vals[g]=v[k]
        r=resid(mon,words,vals); hist.append(r)
        if r<1e-22: break
    consts=[]
    for w in C.CONSTS:
        s=0.0
        for mi in C.support(T,w):
            p=1.0
            for e in C.PM_E[mi]: p*=vals[idx[(e,C.cell_index(e,w))]]
            s+=p
        consts.append(float(s))
    return dict(seed=seed,min_residual=float(min(hist)),final_residual=float(hist[-1]),
                n_iters=len(hist),min_abs_cell=float(np.min(np.abs(vals))),
                constants=consts,converged=bool(min(hist)<1e-18))

def run(T,words,tag,seeds,iters=80):
    pre=precompute(T,words); out=[]
    for s in seeds:
        r=probe(T,words,s,iters=iters,pre=pre); out.append(r)
        print("   %-26s seed %d: min residual %.4e | min|cell| %.2e | constants %s | converged=%s"
              %(tag,s,r["min_residual"],r["min_abs_cell"],["%.3f"%x for x in r["constants"]],r["converged"]),flush=True)
    return out

def main():
    res={"_header":"UNAUDITED W20 constants-pinned feasibility probe (optimised). FLOATS FOR SEARCH ONLY."}
    rng=np.random.default_rng(0)
    sub=[C.MIXED[i] for i in rng.choice(len(C.MIXED),60,replace=False)]
    print("POSITIVE CONTROL (under-determined: 60 random mixed words):",flush=True)
    res["positive_control"]=run(C.C8_MEMBER,sub,"C8/60 words",(1,2,3),iters=60)
    print("NEGATIVE CONTROLS (already proved dead):",flush=True)
    res["neg_m24"]=run(C.W8_IMMUNE[24],list(C.MIXED),"m=24 dead",(1,2,3))
    res["neg_m25"]=run(C.W8_IMMUNE[25],list(C.MIXED),"m=25 dead",(1,2,3))
    print("THE C_8 MEMBER (all 6558 mixed words):",flush=True)
    res["C8"]=run(C.C8_MEMBER,list(C.MIXED),"C_8 member",(1,2,3,4,5,6,7,8,9,10,11,12))
    res["C8_best"]=min(r["min_residual"] for r in res["C8"])
    res["C8_any_converged"]=any(r["converged"] for r in res["C8"])
    print("C_8 member: best residual %.4e over %d restarts; any converged = %s"
          %(res["C8_best"],len(res["C8"]),res["C8_any_converged"]),flush=True)
    json.dump(res,open(os.path.join(HERE,"results_probe.json"),"w"),indent=1,default=str)

if __name__=="__main__": main()

#!/usr/bin/env python3
"""W20 -- RESIDUAL 1: does the L/R asymmetry survive a REVERSED site order?
UNAUDITED.  Exact rational arithmetic only."""
from __future__ import annotations
import os, sys, json, random
from fractions import Fraction
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import w20_core as C
from w20_forcing import kernel_basis, site_system, blocks_from_site, factors_at, jpoint, rref

def run(m, order, seed, passes=4):
    T=C.W8_IMMUNE[m]; gam=C.gamma_edges(T); fullm=C.full_pm_indices(T)
    clean=[w for w in C.MIXED if not C.extras_at(T,w,fullm)]
    rng=random.Random(seed); _,blocks=jpoint(gam,rng)
    trace=[]
    for it in range(passes):
        for site in order:
            nbr,colid,ncols,rows=site_system(blocks,gam,site,clean)
            Ks=[kernel_basis(rows[c],ncols) for c in range(3)]
            if any(not K for K in Ks): continue
            best=None
            for _ in range(80):
                vs=[]; ok=True
                for c in range(3):
                    for _ in range(40):
                        co=[Fraction(rng.randint(-7,7)) for _ in Ks[c]]
                        v=[sum(co[i]*Ks[c][i][j] for i in range(len(Ks[c]))) for j in range(ncols)]
                        if all(x!=0 for x in v): break
                    else: ok=False; break
                    vs.append(v)
                if not ok: break
                rk=len(rref(vs,ncols)[0])
                if best is None or rk>best[0]: best=(rk,vs)
                if best[0]==3: break
            if best is None: continue
            blocks_from_site(blocks,gam,site,nbr,{c:best[1][c] for c in range(3)})
        trace.append(dict(pas=it,dims=None,fac=[s for s in range(8) if factors_at(blocks,gam,s)]))
    fac=[s for s in range(8) if factors_at(blocks,gam,s)]
    ok=all(C.phi_value(blocks,fullm,w)==0 for w in clean)
    nz=all(blocks[e][i][j]!=0 for e in gam for i in range(3) for j in range(3))
    return dict(m=m,order=list(order),seed=seed,final_factoring=fac,clean_ok=ok,all_nonzero=nz,trace=trace,
                block_ranks={str(e):C.rank_of(blocks[e]) for e in gam})

def main():
    res={"_header":"UNAUDITED W20 site-order dependence (residual 1). Exact only."}
    orders={"L_first":[0,1,2,3,4,5,6,7],"R_first":[4,5,6,7,0,1,2,3],
            "interleave":[0,4,1,5,2,6,3,7],"reverse":[7,6,5,4,3,2,1,0]}
    for m in (26,28):
        for nm,o in orders.items():
            for seed in (11,23):
                r=run(m,o,seed)
                res["m%d_%s_s%d"%(m,nm,seed)]=r
                print("m=%d order=%-10s seed=%d -> factoring %s | clean=%s nz=%s | trace %s"
                      %(m,nm,seed,r["final_factoring"],r["clean_ok"],r["all_nonzero"],
                        [t["fac"] for t in r["trace"]]),flush=True)
    json.dump(res,open(os.path.join(HERE,"results_order.json"),"w"),indent=1,default=str)

if __name__=="__main__": main()

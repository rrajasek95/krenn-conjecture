#!/usr/bin/env python3
"""W21 (RE-AIMED) -- the residual linear test at m = 24 and 25, including
AUDIT A7's m=25 REFUTATION WITNESS (the mandated calibration negative).
UNAUDITED.  Exact only."""
import importlib.util, json, os, random, sys
sys.dont_write_bytecode = True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from fractions import Fraction
import w21_core as K, w21_site as SI
from w21_resid import residual_linear_test

A7="/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a7-2026-08-15"
spec=importlib.util.spec_from_file_location("a7w", os.path.join(A7,"a7_witness25.py"))
sys.path.insert(0,A7)
a7w=importlib.util.module_from_spec(spec); spec.loader.exec_module(a7w)

res={"_header":"UNAUDITED W21 residual linear test at m=24,25 incl. A7's witness."}
rows=[]
# --- A7's witness family ---
T=K.W8_IMMUNE[25]; gam=K.gamma_edges(T); clean=K.clean_words(T)
for f in (2,3,4):
  for s in ((1,2,3),(2,3,5)):
    for t in ((1,2,3),(1,3,5)):
        A,B=a7w.build(f=f,s=s,t=t)
        bl={e:[[B[e][i][j] for j in range(3)] for i in range(3)] for e in gam}
        cv=sum(1 for w in clean if K.phi_value(bl,gam,w)!=0)
        nz=all(bl[e][i][j]!=0 for e in gam for i in range(3) for j in range(3))
        fac=[t2 for t2 in range(8) if K.factors_at(bl,gam,t2)]
        r=residual_linear_test(T,bl)
        fz=r.get("forced_zero_cells") or []
        killed = r["inconsistent"] or bool(fz)
        rows.append(dict(m=25,tag="A7 witness f=%s s=%s t=%s"%(f,s,t),clean_violations=cv,
                         nonzero=nz,factoring=fac,killed=killed,**r))
        print("m=25 A7 witness f=%s s=%s t=%s: clean viol %d, nonzero %s, factoring %s | "
              "linear eqs %d rank %s INCONSISTENT=%s forced-zero cells %d => KILLED=%s"
              %(f,s,t,cv,nz,fac,r["n_linear"],r.get("rank"),r["inconsistent"],len(fz),killed),flush=True)
# --- fresh m=25 and m=24 clean points from descent ---
for m in (25,24):
    T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T); clean=K.clean_words(T)
    for seed in (3,11,29,57):
        rng=random.Random(700+seed*7+m)
        order=list(range(8)); rng.shuffle(order)
        bl=SI.descent(gam,clean,rng,order=order,passes=3)
        if bl is None: continue
        if any(K.phi_value(bl,gam,w)!=0 for w in clean): continue
        nz=all(bl[e][i][j]!=0 for e in gam for i in range(3) for j in range(3))
        fac=[t2 for t2 in range(8) if K.factors_at(bl,gam,t2)]
        r=residual_linear_test(T,bl)
        fz=r.get("forced_zero_cells") or []
        killed=r["inconsistent"] or bool(fz)
        rows.append(dict(m=m,tag="descent %d"%seed,nonzero=nz,factoring=fac,killed=killed,**r))
        print("m=%d descent %d: nonzero %s factoring %-16s | unknowns %d linear eqs %d rank %s "
              "INCONSISTENT=%s forced-zero %d => KILLED=%s"
              %(m,seed,nz,fac,r["n_unknowns"],r["n_linear"],r.get("rank"),r["inconsistent"],len(fz),killed),flush=True)
res["rows"]=rows
res["killed"]="%d/%d"%(sum(1 for r in rows if r["killed"]),len(rows))
print("KILLED: %s"%res["killed"])
json.dump(res,open("results_resid25.json","w"),indent=1,default=str)

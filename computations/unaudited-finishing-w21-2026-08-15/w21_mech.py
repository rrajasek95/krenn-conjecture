#!/usr/bin/env python3
"""W21 MOVE 1 -- PROPOSITION W21-F (the non-factoring mechanism).
UNAUDITED.  Exact only.

PROPOSITION.  Let t be a site and suppose EVERY far site u of t (u != t,
u not in N(t)) factors.  Then for every pattern p, dim U^t(p) = 1.
PROOF.  If u factors, A_{uv}[c][d] = alpha^u_c beta^{uv}_d, so expanding
haf(Gamma-t-s) at u gives haf(Gamma-t-s)(w) = alpha^u_{w_u} * (a sum with no
w_u), the SAME scalar for every s in N(t).  Iterating over all far sites,
zeta^t(w) = (prod over far u of alpha^u_{w_u}) * zeta^t(w0) for a reference
colouring w0 of the far sites.  Since a pattern class differs only in the far
colours, U^t(p) is spanned by one vector.  QED
CONSEQUENCE: site t is then unconstrained beyond ONE linear equation per
pattern; rank B^t(p) can be as large as deg(t) - 1 = 3.  This is exactly the
configuration W20's descent produces (an entire side factoring) and it PROVES
that no argument which looks only at one site can work.
The converse FAILS: non-factoring at t does NOT require all far sites to
factor (break seed 777 at m=28: site 5 is non-factoring while none of its
far sites 0,1,3 factors).  Both facts are measured below.
"""
import json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
import w21_core as K, w21_site as SI
from w21_chain import far_sites, zeta
from w21_pf import load_w20_points

res={"_header":"UNAUDITED W21 non-factoring mechanism (Prop W21-F). Exact."}
pts=load_w20_points(); extra={}
if os.path.exists('results_break.json'):
    d=json.load(open('results_break.json'))
    for m in (26,27,28):
        for rec in d.get('m%d'%m,[]):
            if 'point' in rec:
                bl={}
                for k,v in rec['point'].items():
                    e=tuple(int(z) for z in k.strip('()').split(','))
                    bl[e]=[[Fraction(z) for z in row] for row in v]
                extra.setdefault(m,[]).append(("break seed %d"%rec['seed'],bl))
rows=[]
for m in (26,27,28):
    T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T); clean=K.clean_words(T)
    for tag,bl in [pts[m][0]]+extra.get(m,[]):
        fac=set(t for t in range(8) if K.factors_at(bl,gam,t))
        for t in range(8):
            far=far_sites(gam,t)
            allfar = all(u in fac for u in far)
            cw=SI.common_words(clean,t); nb=K.neighbours(gam,t)
            bypat={}
            for w in cw: bypat.setdefault(tuple(w[s] for s in nb),[]).append(w)
            dims={K.rank_of([zeta(bl,gam,t,w) for w in ws],len(nb)) for ws in bypat.values()}
            rows.append(dict(m=m,tag=tag,site=t,factors=(t in fac),
                             all_far_factor=allfar,dimU=sorted(dims),
                             prop_ok=(not allfar) or dims=={1}))
            print("m=%d %-16s site %d fac=%-5s all-far-factor=%-5s dimU set %s  Prop holds %s"
                  % (m,tag,t,t in fac,allfar,sorted(dims),rows[-1]["prop_ok"]))
res["rows"]=rows
res["proposition_violations"]=sum(1 for r in rows if not r["prop_ok"])
res["counterexamples_to_converse"]=[r for r in rows if (not r["factors"]) and (not r["all_far_factor"])][:4]
print("Proposition W21-F violations: %d / %d site-point pairs" % (res["proposition_violations"],len(rows)))
json.dump(res,open("results_mech.json","w"),indent=1,default=str)

#!/usr/bin/env python3
"""W26 -- THE VERTEX-FAILURE EXCLUSION.  UNAUDITED.  Exact only.

FAILURE, formalised.  At a vertex v with letter-coordinate c(v), let T_f be
the letters at which some live single into v fires and T_c = {0,1,2} \\ T_f
the clean letters.  By W26-M / W26-M* the three-vector slice equation gives
h*Phi(t) = <coef, row_t(M)> (resp. hafR*Phi), coef independent of t.  The
vertex DELIVERS at an index choice iff

      row_{t_f}  in  span{ row_t : t in T_c }   for all t_f in T_f,

since then Phi(t_f) = 0 -- a PURE ROW, which kills.  The vertex FAILS iff it
delivers at NO admissible index choice.  Because det M = 0 wherever some
coefficient is forced nonzero, failure then means exactly

      rank{clean rows} = 1   AND   rank{clean rows, firing row} = 2      (*)

i.e. LETTER COLLAPSE (the clean rows are proportional) together with the
firing row outside the collapsed line.

FORCED-NONZERO COEFFICIENTS (from w26_psi.py; this is what makes det M = 0
unconditional, and it is m-dependent -- the m=25 vertex-4 lesson):
   m=25: k=5  Psi[D2] = D1 l03 r67 (monomial);  k=7  Psi[D0] = D1 l23 r56
         k=4  NOT forced (needs hafL != 0);     k=6  NOT forced
   m=26: every k forced (the l02 l13 contradiction)
   m=27: k=4, k=6 forced (Psi[r46] = D0 D2 l13, since (5,7) is absent)
         k=5, k=7 NOT forced
   m=28: NONE forced
   L-vertices: Xi_a = r_{sigma p sigma a} D_b D_c + l_bc hafR; when the
         R-edge is absent this is l_bc*hafR, which vanishes iff hafR = 0 --
         so NO L-vertex is ever unconditionally forced.  Stated explicitly.

CANDIDATE THEOREM (from the 142-point census): the three vertices
R5, R6, L2 are PAIRWISE EXCLUSIVE -- at most one of them fails at any clean
point.  Any ONE of those three pairwise exclusions implies the disjunction.
This file stress-tests the candidate, hardest over F_p where letter collapse
is far more frequent than over Q.
"""
import json, os, random, sys
from fractions import Fraction
from itertools import combinations
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import w26_core as C, w26_fast as F, w26_disj as DJ
import w26_charp as CP

RES=os.path.join(HERE,"results_excl.json")
OUT={"_header":"UNAUDITED W26 vertex-failure exclusion {R5,R6,L2}."}
def ck(): json.dump(OUT,open(RES,"w"),indent=1,default=str)
V=['R4','R5','R6','R7','L0','L1','L2','L3']
TRI=['R5','R6','L2']

def collapse_flags(bl,m):
    """the explicit closed-form LETTER-COLLAPSE conditions.
    R7 (clean letters 0,1): col_0 = lam*col_1 for A07, A47, A67 (index y7).
    R4 (clean letters 1,2): col_1 = lam*col_2 for A14, A45, A47 (index y4).
    Reported as booleans; these are the polynomial conditions (*) in closed
    form, and are checked against the sampled rank test."""
    gs=set(C.gamma_edges(C.TEMPLATES[m]))
    def ratio_const(vecs):
        # vecs: list of (u,v) pairs of 3-vectors; is u = lam*v with ONE lam?
        lams=set()
        for u,vv in vecs:
            for a,b in zip(u,vv):
                if b==0: return None
                lams.add(Fraction(a,1)/b if not isinstance(a,int) else Fraction(a,b))
        return (len(lams)==1, [str(x) for x in sorted(lams)][:3])
    out={}
    # R7: blocks A07 (x0 x y7), A47 (y4 x y7), A67 (y6 x y7); letter = 2nd index
    vecs=[]
    for e in [(0,7),(4,7),(6,7)]:
        for i in range(3):
            vecs.append(([bl[e][i][0]],[bl[e][i][1]]))
    out["R7_collapse"]=ratio_const(vecs)
    # R4: blocks A14 (x1 x y4), A45 (y4 x y5), A47 (y4 x y7); letter index varies
    vecs=[]
    for i in range(3): vecs.append(([bl[(1,4)][i][1]],[bl[(1,4)][i][2]]))
    for j in range(3): vecs.append(([bl[(4,5)][1][j]],[bl[(4,5)][2][j]]))
    for j in range(3): vecs.append(([bl[(4,7)][1][j]],[bl[(4,7)][2][j]]))
    out["R4_collapse"]=ratio_const(vecs)
    return out

def census(recs,tag):
    from collections import Counter
    pat=Counter(); co=Counter(); solo=Counter(); tri_bad=0
    for r in recs:
        f=tuple(l for l in V if not r[l]['DELIVERS'])
        pat[f]+=1
        for l in f: solo[l]+=1
        for a,b in combinations(f,2): co[(a,b)]+=1
        if len([l for l in TRI if l in f])>=2: tri_bad+=1
    return dict(tag=tag,n=len(recs),
        disj_holds=sum(1 for r in recs if r['DISJUNCTION_holds']),
        per_vertex_failures=dict(solo),
        never_together=[str(p) for p in combinations(V,2) if co[p]==0],
        max_simultaneous=max((len(k) for k in pat),default=0),
        TRIANGLE_violations=tri_bad,
        patterns={",".join(k) if k else "(none)":v for k,v in pat.most_common(12)})

def main():
    import w26_pts as PT
    import w26_wide as W
    # ---- (A) re-census the existing Q data, broken down by m
    old=json.load(open(os.path.join(HERE,"results_disj.json")))
    allr=old.get('stored',[])+old.get('fresh',[])+list(old.get('battery',{}).values())
    OUT["Q_census_all"]=census(allr,"Q all")
    for m in (25,26,27,28):
        OUT["Q_census_m%d"%m]=census([r for r in allr if r.get('m')==m],"Q m=%d"%m)
    print("Q census:",json.dumps(OUT["Q_census_all"],default=str)[:400]); ck()
    for m in (25,26,27,28):
        c=OUT["Q_census_m%d"%m]
        print("  m=%d n=%d disj=%d triangle_viol=%d maxsim=%d fails=%s"%(m,c['n'],
            c['disj_holds'],c['TRIANGLE_violations'],c['max_simultaneous'],c['per_vertex_failures']),flush=True)
    ck()
    # ---- (B) FRESH Q points, larger sample
    OUT["Q_fresh"]=[]
    for m in (25,26,27,28):
        mdl=F.Model(m); got=0
        for kk in range(6000):
            rng=random.Random(52_000_000+1000*m+kk); order=list(range(8)); rng.shuffle(order)
            bl=W.make(mdl,rng,passes=4,order=order)
            if bl is None: continue
            r=DJ.analyse(m,bl,nsample=60,seed=17)
            r2=dict(m=m,tag="q%d"%kk,van=mdl.vanishing(bl),
                    DISJUNCTION_holds=r['DISJUNCTION_holds'],
                    fails=[l for l in V if not r[l]['DELIVERS']],
                    collapse=collapse_flags(bl,m))
            for l in V: r2[l]={'DELIVERS':r[l]['DELIVERS']}
            OUT["Q_fresh"].append(r2)
            tri=len([l for l in TRI if l in r2['fails']])
            print("Qfresh m=%d #%-5d van=%-5s disj=%s TRIviol=%s fails=%s"%(m,kk,r2['van'],
                r2['DISJUNCTION_holds'],tri>=2,r2['fails']),flush=True); ck()
            got+=1
            if got>=20: break
    OUT["Q_fresh_census"]=census(OUT["Q_fresh"],"Q fresh")
    ck()
    # ---- (C) F_p stress test: collapse is MUCH more frequent in small char
    OUT["Fp"]=[]
    for p in (7,13,31):
        for m in (25,26,27,28):
            gam=C.gamma_edges(C.TEMPLATES[m]); gs=set(gam); clean=C.clean_words(m)
            got=0
            for kk in range(3000):
                rng=random.Random(303_000+p*1000+m*17+kk)
                bl=CP.seed_p(gam,gs,rng,p)
                if bl is None: continue
                order=list(range(8)); rng.shuffle(order)
                for _ps in range(4):
                    for t in order: CP.site_p(bl,gs,gam,t,clean,rng,p)
                if any(CP.hafp(bl,gs,tuple(range(8)),w,p)!=0 for w in clean): continue
                if not all(bl[e][i][j]%p!=0 for e in gam for i in range(3) for j in range(3)): continue
                blf={e:[[Fraction(bl[e][i][j]) for j in range(3)] for i in range(3)] for e in gam}
                r=DJ.analyse_modp(m,bl,p,nsample=60,seed=23) if hasattr(DJ,'analyse_modp') else None
                if r is None:
                    got+=1
                    OUT["Fp"].append(dict(p=p,m=m,note="analyse_modp unavailable"))
                    break
                OUT["Fp"].append(dict(p=p,m=m,tag="p%d_%d"%(p,kk),
                    DISJUNCTION_holds=r['DISJUNCTION_holds'],
                    fails=[l for l in V if not r[l]['DELIVERS']]))
                print("Fp p=%d m=%d #%-4d disj=%s fails=%s"%(p,m,kk,r['DISJUNCTION_holds'],
                    [l for l in V if not r[l]['DELIVERS']]),flush=True); ck()
                got+=1
                if got>=8: break
    ck(); print("DONE")
if __name__=="__main__": main()

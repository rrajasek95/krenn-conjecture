#!/usr/bin/env python3
"""W21 -- CAN THE ZERO-FACTORING CLEAN POINTS EXTEND TO AN EXACT SOURCE?
UNAUDITED.  Exact only.

With the 16 Gamma blocks FIXED at a zero-factoring clean point of m=28, the
remaining unknowns are the twelve SINGLE cells s_e (one scalar per
non-matching cross edge).  Every mixed word w then gives a polynomial
equation H_w(s) = 0 of degree <= 4 in those twelve scalars, and the three
constant words must be nonzero.  This script builds all 6,558 + 3 polynomials
EXACTLY and decides the system by linear propagation + contradiction search.
An all-nonzero solution would be a COUNTEREXAMPLE to Krenn-Gu at N = 8.
"""
import json, os, sys, glob
sys.dont_write_bytecode = True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from fractions import Fraction
import w21_core as K

T=K.W8_IMMUNE[28]; gam=set(K.gamma_edges(T))
SING=[K.EDGES[i] for i,t in enumerate(T) if t not in (0,511)]
SCELL={e:[(c//3,c%3) for c in range(9) if (T[K.EIDX[e]]>>c)&1][0] for e in SING}
SID={e:i for i,e in enumerate(SING)}
print("singles:", [(str(e),SCELL[e]) for e in SING])

def load(path):
    d=json.load(open(path))
    def walk(o):
        if isinstance(o,dict):
            ks=list(o.keys())
            if ks and all(k.startswith("(") and "," in k for k in ks):
                try: return {tuple(int(z) for z in k.strip("()").split(",")):
                             [[Fraction(x) for x in row] for row in v] for k,v in o.items()}
                except Exception: pass
            for v in o.values():
                r=walk(v)
                if r: return r
        if isinstance(o,list):
            for v in o:
                r=walk(v)
                if r: return r
        return None
    return walk(d)

def poly_of(bl, w):
    """H_w as dict: sorted tuple of single-ids -> coefficient."""
    out={}
    for M in K.PMS:
        coef=Fraction(1); mon=[]
        ok=True
        for (u,v) in M:
            if (u,v) in gam:
                coef*=bl[(u,v)][w[u]][w[v]]
            elif (u,v) in SID:
                if SCELL[(u,v)]!=(w[u],w[v]): ok=False; break
                mon.append(SID[(u,v)])
            else:
                ok=False; break
        if not ok or coef==0: continue
        k=tuple(sorted(mon))
        out[k]=out.get(k,Fraction(0))+coef
        if out[k]==0: del out[k]
    return out

res={"_header":"UNAUDITED W21 extension test for the zero-factoring points."}
for path in sorted(glob.glob(os.path.join(HERE,"tensor","results_zero*.json"))):
    bl=load(path)
    polys={w:poly_of(bl,w) for w in K.MIXED}
    # (1) constant equations: H_w == 0 with no single variables at all
    impossible=[w for w,p in polys.items() if p and all(k==() for k in p)]
    # (2) equations that are identically satisfied
    trivial=sum(1 for p in polys.values() if not p)
    # (3) equations linear in ONE single with a nonzero constant term
    print("=== %s" % os.path.basename(path))
    print("   mixed equations: %d total, %d identically 0, %d IMPOSSIBLE "
          "(nonzero constant, no single variables)"
          % (len(polys), trivial, len(impossible)))
    deg={}
    for p in polys.values():
        d=max([len(k) for k in p], default=-1)
        deg[d]=deg.get(d,0)+1
    print("   degree histogram (max monomial degree, -1 = identically zero):",
          sorted(deg.items()))
    if impossible:
        print("   VERDICT: NO extension exists -- %d mixed words already fail "
              "with the Gamma blocks alone (their H_w does not involve any "
              "single cell).  Example words: %s"
              % (len(impossible), impossible[:5]))
    res[os.path.basename(path)]=dict(
        n_mixed=len(polys), n_identically_zero=trivial,
        n_impossible=len(impossible), example_impossible=[list(w) for w in impossible[:8]],
        degree_hist={str(k):v for k,v in sorted(deg.items())},
        verdict=("NO EXTENSION (unconditional)" if impossible else "needs solving"))
json.dump(res,open(os.path.join(HERE,"results_extend.json"),"w"),indent=1,default=str)

# ---- solve the LINEAR part of the single-cell system exactly ----
print("\n=== LINEAR SUBSYSTEM (degree-1 equations in the 12 single scalars) ===")
res2={}
for path in sorted(glob.glob(os.path.join(HERE,"tensor","results_zero*.json"))):
    bl=load(path)
    rows=[]; consts=[]
    for w in K.MIXED:
        p=poly_of(bl,w)
        if not p: continue
        if max(len(k) for k in p)>1: continue
        r=[Fraction(0)]*12; c=Fraction(0)
        for k,v in p.items():
            if k==(): c=v
            else: r[k[0]]=v
        rows.append(r+[-c])
    R,piv=K.rref(rows,13)
    # inconsistent?  a pivot in the last column
    incons = 12 in piv
    # solution space of the homogeneous+inhomogeneous system
    freedim = 12-len([p for p in piv if p<12])
    print("%s: %d linear equations, rank %d, inconsistent=%s, solution dim=%s"
          % (os.path.basename(path), len(rows), len(piv), incons,
             "n/a" if incons else freedim))
    sol=None
    if not incons:
        sol=[Fraction(0)]*12
        for i,pc in enumerate(piv):
            if pc<12: sol[pc]=R[i][12]
        nz=[SING[i] for i in range(12) if sol[i]!=0]
        print("   unique/particular solution has %d nonzero singles: %s"
              % (len(nz), [str(e) for e in nz]))
        print("   ALL-ZERO forced: %s" % (all(x==0 for x in sol) and freedim==0))
    res2[os.path.basename(path)]=dict(n_linear=len(rows), rank=len(piv),
        inconsistent=bool(incons), solution_dim=(None if incons else freedim),
        solution=[str(x) for x in sol] if sol else None)
d=json.load(open(os.path.join(HERE,"results_extend.json")))
d["linear_subsystem"]=res2
json.dump(d,open(os.path.join(HERE,"results_extend.json"),"w"),indent=1,default=str)

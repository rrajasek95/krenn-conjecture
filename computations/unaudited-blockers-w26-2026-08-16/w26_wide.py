#!/usr/bin/env python3
"""W26 -- WIDE battery: proper point generation (rank-one seeding, as in
W24) + Theorem W26-K tests + MULTI-CHARACTERISTIC.  UNAUDITED.  Exact only.

Ledger 19: every NEVER-claim is tested over Q AND over F_p for at least two
primes p = 1 mod 3 (cube roots of unity present) and p = 1 mod 4.
The NEVER-claim under test is:  det M = 0 at every clean point (Thm W26-K
step 1), and GAP = 0 (the residual gap never fires).
"""
import json, os, random, sys
from fractions import Fraction
from itertools import combinations
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import w26_core as C, w26_fast as F
RES=os.path.join(HERE,"results_wide.json"); OUT={"_header":
  "UNAUDITED W26 wide battery + multi-characteristic."}
def ck(): json.dump(OUT,open(RES,"w"),indent=1,default=str)

# ---------- exact field wrappers -------------------------------------
class GF:
    def __init__(s,p): s.p=p
    def zero(s): return 0
    def one(s): return 1
def inv(a,p): return pow(a,p-2,p)

def seed_point(mdl,rng,tries=800):
    """W24-style rank-one seed: all cells of a block equal, one block solved."""
    gam,gs=mdl.gam,mdl.gs
    for _ in range(tries):
        t={e:Fraction(rng.randint(-9,9) or 3,rng.randint(1,4)) for e in gam}
        e0=gam[rng.randrange(len(gam))]; a=b=Fraction(0)
        for M in C.PMS:
            if not all(e in gs for e in M): continue
            p=Fraction(1); has=False
            for e in M:
                if e==e0: has=True
                else: p*=t[e]
            if has: a+=p
            else: b+=p
        if a==0: continue
        t[e0]=-b/a
        if all(v!=0 for v in t.values()):
            return {e:[[t[e]]*3 for _ in range(3)] for e in gam}
    return None

def make(mdl,rng,passes=4,order=None):
    bl=seed_point(mdl,rng)
    if bl is None: return None
    order=list(range(8)) if order is None else list(order)
    for _ in range(passes):
        for t in order: F.site_solve(mdl,bl,t,rng)
    if mdl.clean_ok(bl) and mdl.allnz(bl): return bl
    return None

def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
           -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
           +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
def rkq(rows):
    R,p=C.rref([list(r) for r in rows],len(rows[0])); return len(p)
def slicesR7(bl,a,b,c): return [[bl[(0,7)][a][t],bl[(4,7)][b][t],bl[(6,7)][c][t]] for t in range(3)]
def slicesR4(bl,a,b,c): return [[bl[(1,4)][a][t],bl[(4,5)][t][b],bl[(4,7)][t][c]] for t in range(3)]
V3={25:[("R7",slicesR7,2),("R4",slicesR4,0)],26:[("R7",slicesR7,2),("R4",slicesR4,0)],
    27:[("R7",slicesR7,2)],28:[]}

def test(m,bl):
    rec={}
    for lab,fn,fire in V3[m]:
        bd=gap=0
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    M=fn(bl,a,b,c)
                    if det3(M)!=0: bd+=1
                    cl=[M[t] for t in range(3) if t!=fire]
                    if rkq(cl)==1 and rkq(cl+[M[fire]])==2: gap+=1
        rec[lab]=(bd,gap)
    # does some single at R7/R4 get an all-pure solo family?
    import w26_sub as SB
    pr={}
    for e in C.live_singles(m):
        if e[1] in (4,7):
            r=SB.solo_report(m,bl,e); pr[str(e)]=(r["n_solo"],r["n_pure"])
    rec["v47_pure"]=pr
    rec["some_pure"]=any(v[1]>0 for v in pr.values())
    return rec

def main():
    OUT["Q"]={}
    for m in (25,26,27,28):
        mdl=F.Model(m); recs=[]; tried=0; got=0
        for kk in range(4000):
            tried+=1
            rng=random.Random(31_000_000+1000*m+kk); order=list(range(8)); rng.shuffle(order)
            bl=make(mdl,rng,passes=4,order=order)
            if bl is None: continue
            r=test(m,bl); r["van"]=mdl.vanishing(bl); recs.append(r); got+=1
            print("m=%d #%-4d van=%-5s %s some_pure=%s"%(m,kk,r["van"],
                {k:v for k,v in r.items() if k in ("R7","R4")},r["some_pure"]),flush=True)
            OUT["Q"]["m%d"%m]=dict(n=got,tried=tried,recs=recs,
                n_off_stratum=sum(1 for x in recs if not x["van"]),
                total_det_nonzero=sum(v[0] for x in recs for k,v in x.items() if k in ("R7","R4")),
                total_gap=sum(v[1] for x in recs for k,v in x.items() if k in ("R7","R4")),
                all_have_pure=all(x["some_pure"] for x in recs))
            ck()
            if got>=25: break
    # ---------------- multi-characteristic -----------------------------
    OUT["charp"]={}
    for p in (7,13,31,37,43,29):
        res={}
        for m in (25,26,27):
            mdl=F.Model(m); gs=mdl.gs; gam=mdl.gam
            nz=nd=bad=0
            rng=random.Random(999+p+m)
            # exhaustive-ish random sweep of CLEAN points over F_p via
            # site-solve in F_p
            for kk in range(400):
                bl={e:[[rng.randrange(1,p) for _ in range(3)] for _ in range(3)] for e in gam}
                # site-resolve mod p
                ok=True
                for _ps in range(4):
                    for t in range(8):
                        nb=sorted({s for e in gam for s in e if t in e and s!=t})
                        ncols=3*len(nb); rows={0:[],1:[],2:[]}
                        for w in mdl.clean:
                            r=[0]*ncols
                            for k2,s in enumerate(nb):
                                vs=tuple(v for v in range(8) if v!=t and v!=s)
                                r[3*k2+w[s]]=(r[3*k2+w[s]]+C.haf_on(bl,gs,vs,w,0,1))%p
                            if any(r): rows[w[t]].append(r)
                        newv={}
                        for c in range(3):
                            Kb=kerp(rows[c],ncols,p)
                            if not Kb: ok=False; break
                            v=None
                            for _t2 in range(200):
                                co=[rng.randrange(p) for _ in Kb]
                                vv=[sum(co[i]*Kb[i][j] for i in range(len(Kb)))%p for j in range(ncols)]
                                if all(z!=0 for z in vv): v=vv; break
                            if v is None: ok=False; break
                            newv[c]=v
                        if not ok: break
                        for k2,s in enumerate(nb):
                            e=(min(t,s),max(t,s))
                            for c in range(3):
                                for d in range(3):
                                    if e[0]==t: bl[e][c][d]=newv[c][3*k2+d]
                                    else: bl[e][d][c]=newv[c][3*k2+d]
                    if not ok: break
                if not ok: continue
                if any(C.haf_on(bl,gs,tuple(range(8)),w,0,1)%p!=0 for w in mdl.clean): continue
                if not all(bl[e][i][j]%p!=0 for e in gam for i in range(3) for j in range(3)): continue
                nz+=1
                for lab,fn,fire in V3[m]:
                    for a in range(3):
                        for b in range(3):
                            for c2 in range(3):
                                M=fn(bl,a,b,c2); nd+=1
                                if det3(M)%p!=0: bad+=1
                if nz>=6: break
            res["m%d"%m]=dict(n_points=nz,n_det=nd,det_nonzero=bad)
            print("p=%d m=%d : %d clean F_p points, det M nonzero %d/%d"%(p,m,nz,bad,nd),flush=True)
            OUT["charp"]["p%d"%p]=res; ck()
    print("DONE"); ck()

def kerp(rows,n,p):
    M=[list(r) for r in rows]; piv=[]; r=0
    for c in range(n):
        sel=None
        for i in range(r,len(M)):
            if M[i][c]%p: sel=i; break
        if sel is None: continue
        M[r],M[sel]=M[sel],M[r]
        iv=pow(M[r][c],p-2,p); M[r]=[(x*iv)%p for x in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]%p:
                f=M[i][c]; M[i]=[(a-f*b)%p for a,b in zip(M[i],M[r])]
        piv.append(c); r+=1
        if r==len(M): break
    out=[]
    for f in [c for c in range(n) if c not in piv]:
        v=[0]*n; v[f]=1
        for i,pc in enumerate(piv): v[pc]=(-M[i][f])%p
        out.append(v)
    return out
if __name__=="__main__": main()

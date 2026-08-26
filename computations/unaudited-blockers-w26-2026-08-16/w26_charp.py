#!/usr/bin/env python3
"""W26 -- MULTI-CHARACTERISTIC sweep for the det-M claim (ledger 19).
UNAUDITED.  Exact only (F_p arithmetic, no floats).

FIX vs the failed attempt in w26_wide.py: that version seeded with fully
random blocks over F_p and site-solved, which never converged (0 clean
points at every prime -- the control was VACUOUS).  Here we use the SAME
rank-one seeding that fixed the rational case: set every cell of every
Gamma block to one scalar t_e, choose one edge e0 and solve the single
scalar equation haf_Gamma = 0 for t_{e0}; then site-resolve.

CLAIM UNDER TEST (a NEVER claim, hence ledger 19):
   at every clean point with all Gamma cells nonzero,
   det M = 0, where M is the 3-block slice matrix at R-vertex 7 (rows
   indexed by the letter of y7, columns A07[x0][.], A47[y4][.], A67[y6][.]),
   and likewise at R-vertex 4; and the side-condition GAP never fires.
Primes: 7, 13, 31, 37, 43 (all = 1 mod 3, so primitive cube roots of unity
EXIST -- the residue class whose absence produced a false kill in W21),
and 13, 29, 37 (= 1 mod 4, so i exists).  Characteristic 3 is excluded
(degenerate) and characteristic 2 is excluded (W24-C fails there).
"""
import json, os, random, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import w26_core as C

RES = os.path.join(HERE, "results_charp.json")
OUT = {"_header": "UNAUDITED W26 multi-characteristic sweep (ledger 19), "
                  "rank-one seeded."}
def ck(): json.dump(OUT, open(RES, "w"), indent=1, default=str)

def hafp(bl, gs, verts, w, p):
    verts = tuple(sorted(verts))
    if not verts: return 1
    a = verts[0]; tot = 0
    for i in range(1, len(verts)):
        b = verts[i]; e = (a,b) if a<b else (b,a)
        if e not in gs: continue
        c = bl[e][w[e[0]]][w[e[1]]] % p
        if c == 0: continue
        tot = (tot + c*hafp(bl, gs, verts[1:i]+verts[i+1:], w, p)) % p
    return tot % p

def kerp(rows, n, p):
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

def rankp(rows,p):
    if not rows: return 0
    n=len(rows[0]); M=[list(r) for r in rows]; piv=0; r=0
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
        r+=1
        if r==len(M): break
    return r

def seed_p(gam, gs, rng, p, tries=900):
    """rank-one seed over F_p (the fix)."""
    for _ in range(tries):
        t={e: rng.randrange(1,p) for e in gam}
        e0=gam[rng.randrange(len(gam))]; a=b=0
        for M in C.PMS:
            if not all(e in gs for e in M): continue
            pr=1; has=False
            for e in M:
                if e==e0: has=True
                else: pr=(pr*t[e])%p
            if has: a=(a+pr)%p
            else: b=(b+pr)%p
        if a%p==0: continue
        t[e0]=((-b)*pow(a,p-2,p))%p
        if all(v%p!=0 for v in t.values()):
            return {e: [[t[e]]*3 for _ in range(3)] for e in gam}
    return None

def site_p(bl, gs, gam, t, clean, rng, p):
    nb=sorted({s for e in gam for s in e if t in e and s!=t})
    ncols=3*len(nb); rows={0:[],1:[],2:[]}
    for w in clean:
        r=[0]*ncols
        for k,s in enumerate(nb):
            vs=tuple(v for v in range(8) if v!=t and v!=s)
            r[3*k+w[s]]=(r[3*k+w[s]]+hafp(bl,gs,vs,w,p))%p
        if any(r): rows[w[t]].append(r)
    newv={}
    for c in range(3):
        Kb=kerp(rows[c],ncols,p)
        if not Kb: return False
        v=None
        for _ in range(300):
            co=[rng.randrange(p) for _ in Kb]
            vv=[sum(co[i]*Kb[i][j] for i in range(len(Kb)))%p for j in range(ncols)]
            if all(z%p!=0 for z in vv): v=vv; break
        if v is None: return False
        newv[c]=v
    save={e:[r[:] for r in bl[e]] for e in gam}
    for k,s in enumerate(nb):
        e=(min(t,s),max(t,s))
        for c in range(3):
            for d in range(3):
                if e[0]==t: bl[e][c][d]=newv[c][3*k+d]
                else: bl[e][d][c]=newv[c][3*k+d]
    if any(hafp(bl,gs,tuple(range(8)),w,p)!=0 for w in clean):
        for e in gam: bl[e]=save[e]
        return False
    return True

def det3p(M,p):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
           -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
           +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))%p

def sR7(bl,a,b,c): return [[bl[(0,7)][a][t],bl[(4,7)][b][t],bl[(6,7)][c][t]] for t in range(3)]
def sR4(bl,a,b,c): return [[bl[(1,4)][a][t],bl[(4,5)][t][b],bl[(4,7)][t][c]] for t in range(3)]
V3={25:[("R7",sR7,2),("R4",sR4,0)],26:[("R7",sR7,2),("R4",sR4,0)],27:[("R7",sR7,2)],28:[]}

def main():
    PRIMES=[7,13,31,37,43,29]
    for p in PRIMES:
        OUT["p%d"%p]={}
        for m in (25,26,27):
            gam=C.gamma_edges(C.TEMPLATES[m]); gs=set(gam); clean=C.clean_words(m)
            npts=nd=bad=gap=nvan=0; tried=0
            for kk in range(3000):
                tried+=1
                rng=random.Random(101_000+p*1000+m*17+kk)
                bl=seed_p(gam,gs,rng,p)
                if bl is None: continue
                order=list(range(8)); rng.shuffle(order)
                for _ps in range(4):
                    for t in order: site_p(bl,gs,gam,t,clean,rng,p)
                if any(hafp(bl,gs,tuple(range(8)),w,p)!=0 for w in clean): continue
                if not all(bl[e][i][j]%p!=0 for e in gam for i in range(3) for j in range(3)): continue
                npts+=1
                if all(hafp(bl,gs,tuple(range(8)),w,p)==0 for w in C.WORDS): nvan+=1
                for lab,fn,fire in V3[m]:
                    for a in range(3):
                        for b in range(3):
                            for c in range(3):
                                M=fn(bl,a,b,c); nd+=1
                                if det3p(M,p)!=0: bad+=1
                                cl=[M[t] for t in range(3) if t!=fire]
                                if rankp(cl,p)==1 and rankp(cl+[M[fire]],p)==2: gap+=1
                OUT["p%d"%p]["m%d"%m]=dict(n_points=npts,tried=tried,n_vanishing=nvan,
                    n_det_tests=nd,det_nonzero=bad,GAP=gap)
                ck()
                if npts>=12: break
            print("p=%2d m=%d : %2d clean F_p points (%d on stratum) | det M nonzero %d/%d | GAP %d"
                  %(p,m,npts,nvan,bad,nd,gap),flush=True)
            ck()
    # POSITIVE CONTROL: the claim must FAIL at random non-clean F_p points
    OUT["out_of_locus"]={}
    for p in PRIMES:
        nb=0
        for m in (25,26,27):
            gam=C.gamma_edges(C.TEMPLATES[m]); rng=random.Random(7*p+m)
            for _ in range(6):
                bl={e:[[rng.randrange(1,p) for _ in range(3)] for _ in range(3)] for e in gam}
                hit=False
                for lab,fn,fire in V3[m]:
                    for a in range(3):
                        for b in range(3):
                            for c in range(3):
                                if det3p(fn(bl,a,b,c),p)!=0: hit=True
                nb+=hit
        OUT["out_of_locus"]["p%d"%p]="%d/18"%nb
        print("OUT-OF-LOCUS p=%d: random non-clean points with det M != 0: %d/18 (want 18)"%(p,nb),flush=True)
        ck()
    OUT["control_manifest"]=dict(declared=["charp_sweep","out_of_locus"],
                                 ran=["charp_sweep","out_of_locus"])
    ck(); print("DONE")

if __name__=="__main__": main()

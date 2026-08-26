#!/usr/bin/env python3
"""W20 -- structural reconnaissance of the ladder m=26,27,28 and the C_8
member.  UNAUDITED, exact integer arithmetic only."""
from __future__ import annotations
import os, sys, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import w20_core as C

def clean_boxes(T, fullm, Lsites=(0,1,2,3)):
    """for each L-word x, the effectively-clean y-set; is it a product box?"""
    Rs = [s for s in range(8) if s not in Lsites]
    boxes, isbox, nclean = {}, True, 0
    for x in itertools.product(range(3), repeat=len(Lsites)):
        ys = []
        for y in itertools.product(range(3), repeat=len(Rs)):
            w = [0]*8
            for k,s in enumerate(Lsites): w[s] = x[k]
            for k,s in enumerate(Rs): w[s] = y[k]
            w = tuple(w)
            if len(set(w)) == 1:      # constants are not "mixed equations"
                continue
            if not C.extras_at(T, w, fullm):
                ys.append(y)
        nclean += len(ys)
        proj = [sorted({y[k] for y in ys}) for k in range(len(Rs))] if ys else [[]]*len(Rs)
        n = 1
        for p in proj: n *= len(p)
        if n != len(ys): isbox = False
        boxes[x] = (proj, len(ys))
    return boxes, isbox, nclean

def pfaffian_orientation(gam):
    """does there exist s: E -> {+-1} with sgn(M) * prod_{e in M} s_e constant
    over all PMs M inside gam?  GF(2) linear system."""
    pms = C.pms_inside(gam)
    if not pms: return dict(n_pms=0, pfaffian=None)
    eidx = {e:i for i,e in enumerate(sorted(gam))}
    def pfsign(m):
        perm = []
        for (u,v) in m: perm += [u,v]
        # sign of the permutation perm of 0..7
        seen=[False]*8; sgn=1
        pos={v:i for i,v in enumerate(perm)}
        p=list(perm); 
        for i in range(8):
            if seen[i]: continue
            j=i; L=0
            while not seen[j]:
                seen[j]=True; j=p[j]; L+=1
            if L%2==0: sgn=-sgn
        return sgn
    rows=[]; rhs=[]
    base = C.PMS[pms[0]]
    b0 = 0 if pfsign(base)==1 else 1
    v0 = [0]*len(eidx)
    for e in base: v0[eidx[tuple(sorted(e))]] = 1
    for mi in pms[1:]:
        m = C.PMS[mi]
        v = [0]*len(eidx)
        for e in m: v[eidx[tuple(sorted(e))]] ^= 1
        for k in range(len(v)): v[k] ^= v0[k]
        rows.append(v)
        rhs.append(((0 if pfsign(m)==1 else 1) ^ b0))
    # solve over GF(2)
    n=len(eidx); M=[r[:]+[rhs[i]] for i,r in enumerate(rows)]
    r=0
    for c in range(n):
        piv=None
        for i in range(r,len(M)):
            if M[i][c]: piv=i;break
        if piv is None: continue
        M[r],M[piv]=M[piv],M[r]
        for i in range(len(M)):
            if i!=r and M[i][c]:
                M[i]=[a^b for a,b in zip(M[i],M[r])]
        r+=1
    ok = all(any(row[:n]) or row[n]==0 for row in M)
    return dict(n_pms=len(pms), pfaffian=ok)

def main():
    res={}
    for m in (25,26,27,28):
        T=C.W8_IMMUNE[m]; fullm=C.full_pm_indices(T); gam=C.gamma_edges(T)
        boxes,isbox,nclean = clean_boxes(T, fullm)
        deg=[sum(1 for e in gam if t in e) for t in range(8)]
        nfullbox = sum(1 for x,(p,n) in boxes.items() if n>0)
        res[str(m)] = dict(n_gamma=len(gam), gamma=[list(e) for e in gam],
            n_F=len(fullm), degrees=deg, n_clean_mixed=nclean,
            clean_is_product_box=isbox, n_Lwords_with_clean=nfullbox,
            pfaffian=pfaffian_orientation(gam),
            box_profile={str(x):[p,n] for x,(p,n) in list(boxes.items()) if n>0})
        print("m=%d |Gamma|=%d |F|=%d deg=%s clean=%d box=%s Lwords=%d pf=%s"
              % (m,len(gam),len(fullm),deg,nclean,isbox,nfullbox,
                 res[str(m)]["pfaffian"]), flush=True)
    T=C.C8_MEMBER; gam=C.gamma_edges(T)
    res["C8"]=dict(n_gamma=len(gam), gamma=[list(e) for e in gam],
                   n_F=len(C.pms_inside(gam)), pfaffian=pfaffian_orientation(gam))
    print("C8:", res["C8"], flush=True)
    json.dump(res, open(os.path.join(HERE,"results_struct.json"),"w"), indent=1, default=str)

if __name__=="__main__": main()

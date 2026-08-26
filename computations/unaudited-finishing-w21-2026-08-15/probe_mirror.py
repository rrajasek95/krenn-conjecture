import sys, json; sys.dont_write_bytecode=True; sys.path.insert(0,'.')
from fractions import Fraction
from itertools import product
import w21_core as K, w21_block as B
from w21_pf import load_w20_points

SIGI={v:k for k,v in B.SIG.items()}   # R-site -> L-site
def box_R(y):
    """X_i(y) for i in L."""
    out={i:set(range(3)) for i in B.L}
    for (i,j),(a,b) in B.SINGLES.items():
        if y[j-4]==b: out[i].discard(a)
    return out
FBY=[y for y in product(range(3),repeat=4) if all(len(v)==3 for v in box_R(y).values())]
print("full-box R words:",FBY)

def hafR_full(bl,gam,y): return B.hafR(bl,gam,y)
def N_of(bl,gam,y,i,j,P):
    """mirror modified L-block N_{ij}, indexed [x_i][x_j]."""
    e=(min(i,j),max(i,j))
    Ap=[[bl[e][r][s] for s in range(3)] for r in range(3)]
    k,l=[z for z in B.L if z not in (i,j)]
    a,b=B.SIG[k],B.SIG[l]; e2=(min(a,b),max(a,b))
    coef = bl[e2][y[e2[0]-4]][y[e2[1]-4]] if e2 in set(gam) else Fraction(0)
    ci=[bl[(i,B.SIG[i])][r][y[B.SIG[i]-4]] for r in range(3)]
    cj=[bl[(j,B.SIG[j])][r][y[B.SIG[j]-4]] for r in range(3)]
    g=coef/P
    return [[Ap[r][s]+g*ci[r]*cj[s] for s in range(3)] for r in range(3)]

def hafK4_N(Ns,x):
    t=Fraction(0)
    for (i,j),(k,l) in B.PAIRINGS:
        t+=Ns[(i,j)][x[i]][x[j]]*Ns[(k,l)][x[k]][x[l]]
    return t

pts=load_w20_points()
for m in (26,27,28):
    T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T); clean=K.clean_words(T)
    tag,bl=pts[m][0]
    print("=== m=%d %s  factoring %s" % (m,tag,[t for t in range(8) if K.factors_at(bl,gam,t)]))
    # L-clique column spans at each L-site (original blocks only)
    for i in B.L:
        cols=[]
        for j in B.L:
            if j==i: continue
            e=(min(i,j),max(i,j))
            if e[0]==i: cols+=[[bl[e][r][s] for r in range(3)] for s in range(3)]
            else: cols+=[[bl[e][s][r] for r in range(3)] for s in range(3)]
        print("   L-site %d: clique-column span dim = %d" % (i, K.rank_of(cols,3)))
    for y in FBY:
        P=hafR_full(bl,gam,y)
        if P==0: print("   y=%s hafR=0"%(y,)); continue
        Ns={(i,j):N_of(bl,gam,y,i,j,P) for (i,j) in B.LPAIRS}
        nz=sum(1 for x in product(range(3),repeat=4) if hafK4_N(Ns,x)!=0)
        rk={(i,j):K.rank_of(Ns[(i,j)],3) for (i,j) in B.LPAIRS}
        sd={}
        for i in B.L:
            cols=[]
            for j in B.L:
                if j==i: continue
                key=(min(i,j),max(i,j)); Nn=Ns[key]
                if key[0]==i: cols+=[[Nn[r][s] for r in range(3)] for s in range(3)]
                else: cols+=[[Nn[s][r] for r in range(3)] for s in range(3)]
            sd[i]=K.rank_of(cols,3)
        print("   y=%s mirror ident fails %d/81 | rank N %s | L-site col-dims %s" % (y,nz,sorted(rk.items()),sorted(sd.items())))

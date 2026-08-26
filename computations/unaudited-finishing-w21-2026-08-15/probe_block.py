import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.')
import w21_core as K
from itertools import product
for m in (26,27,28):
    T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T)
    L=[0,1,2,3]; R=[4,5,6,7]
    print("=== m=%d  Gamma edges within L:"%m, [e for e in gam if e[0] in L and e[1] in L],
          " within R:", [e for e in gam if e[0] in R and e[1] in R],
          " cross:", [e for e in gam if (e[0] in L)!=(e[1] in L)])
    # non-Gamma nonzero blocks
    forb={}
    for ei,e in enumerate(K.EDGES):
        if T[ei] not in (0,511):
            cells=[(c//3,c%3) for c in range(9) if (T[ei]>>c)&1]
            forb[e]=cells
    print("   non-full nonzero blocks:", {str(k):v for k,v in forb.items()})
    # test: clean(x,y) <=> for each non-full block e=(u,v) with single cell (a,b): not(w_u==a and w_v==b)
    clean=set(K.clean_words(T))
    ok=True; nbad=0
    for w in K.MIXED:
        pred = all(not (w[u]==a and w[v]==b) for (u,v),cs in forb.items() for (a,b) in cs)
        if pred != (w in clean): nbad+=1
    print("   forbidden-pair characterisation mismatches: %d / %d" % (nbad, len(K.MIXED)))

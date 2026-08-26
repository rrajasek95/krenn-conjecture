import sys, json; sys.dont_write_bytecode=True; sys.path.insert(0,'.')
from fractions import Fraction
from itertools import product
import w21_core as K, w21_block as B
d=json.load(open('results_break.json'))
for m in (26,27,28):
    T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T); clean=K.clean_words(T)
    for rec in d.get('m%d'%m,[]):
        if 'point' not in rec: continue
        bl={}
        for k,v in rec['point'].items():
            e=tuple(int(z) for z in k.strip('()').split(','))
            bl[e]=[[Fraction(z) for z in row] for row in v]
        assert all(K.phi_value(bl,gam,w)==0 for w in clean)
        print("m=%d seed %d factoring %s" % (m, rec['seed'], rec['factoring']))
        for x in B.full_box_words():
            P=B.hafL(bl,x)
            if P==0: print("   x=%s hafL=0"%(x,)); continue
            Ms={(i,j):B.M_of(bl,gam,x,i,j,P) for (i,j) in B.LPAIRS}
            nz=sum(1 for y in product(range(3),repeat=4) if B.hafK4_M(Ms,y)!=0)
            rk={(B.SIG[i],B.SIG[j]):K.rank_of(Ms[(i,j)],3) for (i,j) in B.LPAIRS}
            # per-R-site: dim of span of the columns of the three incident M's
            sitedim={}
            for i in B.L:
                cols=[]
                for j in B.L:
                    if j==i: continue
                    key=(min(i,j),max(i,j))
                    Mm=Ms[key]
                    if key[0]==i: cols += [[Mm[r][s] for r in range(3)] for s in range(3)]
                    else: cols += [[Mm[s][r] for r in range(3)] for s in range(3)]
                sitedim[B.SIG[i]]=K.rank_of(cols,3)
            print("   x=%s ident fails %d/81 | rank M %s | site col-dims %s" % (x,nz,sorted(rk.items()),sorted(sitedim.items())))

import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.')
import w21_core as K
from itertools import permutations, product
SINGLES = {(0,4):(0,0),(0,5):(0,1),(0,6):(0,2),(1,5):(1,0),(1,6):(1,1),
           (1,7):(0,2),(2,4):(1,0),(2,6):(2,1),(2,7):(1,2),(3,4):(2,0),
           (3,5):(2,1),(3,7):(2,2)}
FPD=dict(SINGLES)
def graph_auts(gam):
    E=set(gam)
    return [s for s in permutations(range(8))
            if all((min(s[u],s[v]),max(s[u],s[v])) in E for (u,v) in gam)]
def comps(partial):
    return [p for p in permutations(range(3)) if all(p[k]==v for k,v in partial.items())]
for m in (26,27,28):
    T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T); clean=set(K.clean_words(T))
    sigs={}
    for s in graph_auts(gam):
        part={v:{} for v in range(8)}; ok=True
        for (i,j),(a,b) in FPD.items():
            ii,jj=s[i],s[j]
            key=(ii,jj) if (ii,jj) in FPD else ((jj,ii) if (jj,ii) in FPD else None)
            if key is None: ok=False;break
            aa,bb=FPD[key]
            ti,tj=(aa,bb) if key==(ii,jj) else (bb,aa)
            if part[i].get(a,ti)!=ti or part[j].get(b,tj)!=tj: ok=False;break
            part[i][a]=ti; part[j][b]=tj
        if not ok: continue
        opts=[comps(part[v]) for v in range(8)]
        if any(not o for o in opts): continue
        n=0
        for pis in product(*opts):
            good=True
            for w in clean:
                w2=[0]*8
                for v in range(8): w2[s[v]]=pis[v][w[v]]
                if tuple(w2) not in clean: good=False;break
            n+=good
        if n: sigs[s]=n
    print("m=%d: site-permutations realised: %d, total group order %d" % (m,len(sigs),sum(sigs.values())))
    for s,n in sigs.items(): print("     sigma=%s  x %d colour choices" % (list(s),n))

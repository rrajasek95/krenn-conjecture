import sys; sys.dont_write_bytecode=True
sys.path.insert(0,'.')
import w21_core as K
from itertools import product, permutations
T=K.C8_MEMBER; L=(0,1,2,3); R=(4,5,6,7)
def cls(mask):
    if mask==0: return "zero"
    cs=[(c//3,c%3) for c in range(9) if (mask>>c)&1]
    if len(cs)==1: return "single"
    if mask==511: return "full"
    rows={i for i,_ in cs}; cols={j for _,j in cs}
    return "thin" if (len(rows)==1 or len(cols)==1) else "fat"
print("BLOCKS:")
for ei,(u,v) in enumerate(K.EDGES):
    m=T[ei]
    if m==0: continue
    cs=[(c//3,c%3) for c in range(9) if (m>>c)&1]
    dead=[(c//3,c%3) for c in range(9) if not (m>>c)&1]
    side = "cross" if (u in L)!=(v in L) else ("LL" if u in L else "RR")
    print("  e=%s %-5s %-6s mask=%3d  %s" % ((u,v), side, cls(m), m,
        ("dead="+str(dead)) if cls(m)=="fat" else ("cell="+str(cs[0]) if cls(m)=="single" else "")))
# L-free words
def singles(side):
    out={}
    for ei,(u,v) in enumerate(K.EDGES):
        if u in side and v in side and cls(T[ei])=="single":
            out[(u,v)]=[(c//3,c%3) for c in range(9) if (T[ei]>>c)&1][0]
    return out
LS=singles(L); RS=singles(R)
print("L singles:",LS); print("R singles:",RS)
def freew(side,sing):
    out=[]
    pos={s:k for k,s in enumerate(side)}
    for z in product(range(3),repeat=4):
        ok=True
        for (u,v),(i,j) in sing.items():
            if z[pos[u]]==i and z[pos[v]]==j: ok=False;break
        if ok: out.append(z)
    return out
LF=freew(L,LS); RF=freew(R,RS)
print("n L-free",len(LF),"n R-free",len(RF))
# dead-cell-free L-words: for all i,j,d the cell (x_i,d) of block (i,j) occupied
def deadfree_L(x):
    for i in L:
        for j in R:
            ei=K.EIDX[(i,j)]
            for d in range(3):
                if not (T[ei]>>(3*x[L.index(i)]+d))&1: return False
    return True
print("dead-cell-free L-free words:",[x for x in LF if deadfree_L(x)])
def deadfree_R(y):
    for j in R:
        for i in L:
            ei=K.EIDX[(i,j)]
            for c in range(3):
                if not (T[ei]>>(3*c+y[R.index(j)]))&1: return False
    return True
print("dead-cell-free R-free words:",[y for y in RF if deadfree_R(y)])
print("LF list:",LF)

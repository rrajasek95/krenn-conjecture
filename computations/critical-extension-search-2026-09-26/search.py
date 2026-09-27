"""Finite-field exploration of simultaneous quadratic and cubic cancellation.

This discovers candidates only. No finite-field result is a complex proof.
"""
from itertools import combinations, product
from pathlib import Path
from random import Random
import sys
import json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'critical-cone-2026-09-26'))
import probe

P=probe.P
CELLS=tuple((i,j,a,b) for i,j in combinations(range(6),2) for a,b in product(range(2),repeat=2))
INDEX={c:i for i,c in enumerate(CELLS)}
WORDS=tuple(product(range(2),repeat=6))


def matchings(vertices):
    if not vertices:
        yield ()
        return
    for j in range(1,len(vertices)):
        for rest in matchings(vertices[1:j]+vertices[j+1:]):
            yield ((vertices[0],vertices[j]),)+rest


TERMS=np.array([[[INDEX[i,j,w[i],w[j]] for i,j in M] for M in matchings(tuple(range(6)))] for w in WORDS])
BASE=np.array([probe.Q.get((i,j),0) if a==b==0 else 0 for i,j,a,b in CELLS],dtype=np.int64)


def solve(matrix,rhs):
    a=np.column_stack((matrix,rhs)).copy()%P
    r=0; pivots=[]
    for col in range(matrix.shape[1]):
        options=np.flatnonzero(a[r:,col])
        if not len(options):continue
        p=r+int(options[0]); a[[r,p]]=a[[p,r]]
        a[r]=a[r]*pow(int(a[r,col]),-1,P)%P
        factors=a[:,col].copy(); factors[r]=0
        a=(a-factors[:,None]*a[r])%P
        pivots.append(col);r+=1
        if r==len(a):break
    if np.any(np.all(a[:,:-1]==0,axis=1)&(a[:,-1]!=0)):
        return None,r
    solution=np.zeros(matrix.shape[1],dtype=np.int64)
    for i,col in enumerate(pivots):solution[col]=a[i,-1]
    return solution,r


def extension(first):
    mat=np.zeros((64,60),dtype=np.int64)
    for k in range(3):
        i,j=[v for v in range(3) if v!=k]
        values=BASE[TERMS[:,:,i]]*first[TERMS[:,:,j]]+BASE[TERMS[:,:,j]]*first[TERMS[:,:,i]]
        for wi in range(64):np.add.at(mat[wi],TERMS[wi,:,k],values[wi])
    cubic=np.prod(first[TERMS],axis=2).sum(axis=1)%P
    solution,rank=solve(mat%P,-cubic)
    if solution is not None and np.any((mat@solution+cubic)%P):
        raise ValueError('Exact modular extension reconstruction failed')
    return solution,rank


def main():
    rng=Random(260927)
    counts={'directions':0,'nonzero_quartic':0,'cubic_extendable':0,'extendable_nonzero_quartic':0,
            'nonzero_quartic_after_low_a_gate':0}
    sections=[]; hits=[]
    for nb in range(6):
        for na in (0,1,2,5):
            active_b=rng.sample(range(5),nb);active_a=rng.sample(range(5),na)
            row={(i,h):rng.randrange(1,P) if i in (active_a if h==0 else active_b) else 0 for i,h in probe.ROWS}
            kernel=probe.nullspace(probe.matrix(row))
            passed=0
            for trial in range(40):
                weights=[rng.randrange(P) for _ in kernel]
                core=[sum(c*b[j] for c,b in zip(weights,kernel))%P for j in range(40)]
                source=dict(zip(probe.CELLS,core));source.update({(i,5,h,1):v for (i,h),v in row.items()})
                first=np.array([source.get(c,0) for c in CELLS],dtype=np.int64)
                f=probe.quartic(row,dict(zip(probe.CELLS,core)))
                cubic=np.prod(first[TERMS],axis=2).sum(axis=1)%P
                low_a=any(int(value) for word,value in zip(WORDS,cubic) if word.count(0)<=1)
                second,rank=extension(first)
                counts['directions']+=1;counts['nonzero_quartic']+=bool(f)
                counts['nonzero_quartic_after_low_a_gate']+=bool(f) and not low_a
                counts['cubic_extendable']+=second is not None
                passed+=second is not None
                if f and second is not None:
                    counts['extendable_nonzero_quartic']+=1
                    hits.append(dict(root_row=[row[k] for k in probe.ROWS],core=core,second=second.tolist(),quartic=f))
            sections.append(dict(root_a_support=na,root_b_support=nb,kernel_dimension=len(kernel),cubic_extendable=passed))
    print(json.dumps(dict(status='EXPLORATORY',prime=P,omega=probe.W,counts=counts,sections=sections,hits=hits,
                         limitation='Binary finite-field sections only; no exhaustive complex or ternary conclusion'),indent=2,sort_keys=True))


if __name__=='__main__':main()

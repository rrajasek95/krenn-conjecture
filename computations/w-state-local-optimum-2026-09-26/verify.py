#!/usr/bin/env python3
"""Exact constrained second variation of the six-site W design.

Coordinates rescale the 40 non-root cells by sqrt(26), leaving a rational
matching map and the positive norm metric diag(26,...,26,1,...,1).
"""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'computations/boundary-structure-2026-09-26'))
from exact import require, matchings


def nullspace(matrix):
    a=[[Q(x) for x in row] for row in matrix]
    n=len(a[0]);r=0;pivots=[]
    for col in range(n):
        pivot=next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        d=a[r][col];a[r]=[x/d for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][col]:
                d=a[i][col];a[i]=[x-d*y for x,y in zip(a[i],a[r])]
        pivots.append(col);r+=1
        if r==len(a):break
    basis=[]
    for free in range(n):
        if free in pivots:continue
        v=[Q(0)]*n;v[free]=Q(1)
        for i,col in enumerate(pivots):v[col]=-a[i][free]
        require(all(sum(x*y for x,y in zip(row,v))==0 for row in matrix),'Exact tangent null vector')
        basis.append(v)
    return basis,pivots


def restrict(matrix,basis):
    images=[[sum(a*b for a,b in zip(row,v)) for row in matrix] for v in basis]
    return [[sum(a*b for a,b in zip(v,w)) for w in images] for v in basis]


def inertia_psd(matrix):
    a=[list(row) for row in matrix]
    require(all(a[i][j]==a[j][i] for i in range(len(a)) for j in range(len(a))),'Symmetric rational form')
    pivots=[]
    while a:
        require(all(a[i][i]>=0 for i in range(len(a))),'No negative diagonal in an exact Schur complement')
        p=next((i for i in range(len(a)) if a[i][i]),None)
        if p is None:
            require(not any(x for row in a for x in row),'Zero-diagonal remainder is actually zero')
            return pivots,len(a)
        order=[p]+[i for i in range(len(a)) if i!=p]
        a=[[a[i][j] for j in order] for i in order]
        d=a[0][0];require(d>0,'Positive exact pivot');pivots.append(d)
        a=[[a[i][j]-a[i][0]*a[0][j]/d for j in range(1,len(a))] for i in range(1,len(a))]
    return pivots,0


def check():
    cells=tuple((i,j,a,b) for i,j in combinations(range(6),2) for a,b in product(range(2),repeat=2))
    index={c:i for i,c in enumerate(cells)}
    words=tuple(product(range(2),repeat=6))
    terms=[tuple(tuple(index[i,j,w[i],w[j]] for i,j in M) for M in matchings(tuple(range(6)))) for w in words]
    z=[Q(1) if j<5 and a==b==0 else Q(5) if j==5 and (a,b)==(1,0)
       else Q(1) if j==5 and (a,b)==(0,1) else Q(0) for i,j,a,b in cells]
    metric=[Q(26) if j<5 else Q(1) for i,j,a,b in cells]
    h=[sum(z[i]*z[j]*z[k] for i,j,k in terms_w) for terms_w in terms]
    require(h==[15 if sum(w)==1 else 0 for w in words],'Exact W output in rational coordinates')
    energy=sum(g*x*x for g,x in zip(metric,z))
    require(energy==390 and Q(6*390**2,390**3)==Q(1,65),'Physical norm and rate')
    jacobian=[[Q(0)]*60 for _ in words]
    for wi,terms_w in enumerate(terms):
        for t in terms_w:
            for p in range(3):
                i,j=[q for q in range(3) if q!=p]
                jacobian[wi][t[p]]+=z[t[i]]*z[t[j]]
    dual=[Q(1,3) if w==(0,0,0,0,0,1) else Q(5,3) if sum(w)==1 else Q(0) for w in words]
    require(all(sum(y*row[j] for y,row in zip(dual,jacobian))==metric[j]*z[j] for j in range(60)),
            'Exact stationarity for the norm subject to the complete output tensor')
    interaction=[[Q(0)]*60 for _ in range(60)]
    for y,terms_w in zip(dual,terms):
        if not y:continue
        for t in terms_w:
            for p,q in combinations(range(3),2):
                value=y*z[t[3-p-q]]
                interaction[t[p]][t[q]]+=value
                interaction[t[q]][t[p]]+=value
    basis,pivots=nullspace(jacobian)
    require(len(pivots)==32 and len(basis)==28,'Full binary tangent dimension')
    real=[[metric[i]*(i==j)-interaction[i][j] for j in range(60)] for i in range(60)]
    imag=[[metric[i]*(i==j)+interaction[i][j] for j in range(60)] for i in range(60)]
    rp,rz=inertia_psd(restrict(real,basis));ip,iz=inertia_psd(restrict(imag,basis))
    require(len(rp)==28 and rz==0,'Real tangent form is positive definite')
    require(len(ip)==23 and iz==5,'Imaginary tangent form has exactly five zero directions')
    gauges=[]
    for vertex in range(5):
        theta=[int(i==vertex)-int(i==5) for i in range(6)]
        v=[(theta[i]+theta[j])*weight for (i,j,a,b),weight in zip(cells,z)]
        require(all(sum(a*b for a,b in zip(row,v))==0 for row in jacobian),'Vertex phase preserves every target coefficient')
        require(sum(v[i]*imag[i][j]*v[j] for i in range(60) for j in range(60))==0,'Phase gauge lies in the imaginary kernel')
        gauges.append(v)
    _,gauge_pivots=nullspace([list(row) for row in zip(*gauges)])
    require(len(gauge_pivots)==5,'All five phase directions are independent')
    corrupt=list(dual);corrupt[words.index((1,0,0,0,0,0))]+=1
    require(any(sum(y*row[j] for y,row in zip(corrupt,jacobian))!=metric[j]*z[j] for j in range(60)),
            'Corrupt stationarity multiplier is rejected')
    # Changing the final positive pivot to its negative must not pass PSD.
    try:
        inertia_psd([[Q(-1)]])
    except ValueError:
        negative='REJECTED'
    else:
        raise ValueError('Negative form was accepted')
    return dict(binary_source_variables=60,output_constraints=64,jacobian_rank=32,tangent_complex_dimension=28,
                real_positive_pivots=list(map(str,rp)),imaginary_positive_pivots=list(map(str,ip)),
                imaginary_nullity=iz,phase_gauge_dimension=5,physical_source_norm_squared='390',
                output_amplitude='390',rate='1/65',negative_controls={'corrupt_multiplier':'REJECTED','negative_form':negative},
                consequence='Strict local minimum of source norm modulo vertex phases; arbitrary extra colors cannot improve it',
                limitation='Local, not global; no explicit neighborhood radius is supplied')


def main():
    dependencies=json.loads((HERE/'dependencies.json').read_text())
    for name,expected in dependencies.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,'Pinned dependency: '+name)
    result=dict(status='PASS',evidence_status='Exact second-variation certificate with written local proof; independent audit pending',
                certificate=check(),dependencies=dependencies)
    files=sorted(p for p in HERE.iterdir() if p.suffix in ('.py','.json','.md') and p.name!='results.json')
    files.append(ROOT/'notes/w-state-unrestricted-local-optimum-2026-09-26.md')
    result['sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()

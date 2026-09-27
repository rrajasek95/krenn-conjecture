"""Exact site scaling, support pruning, and four-site response identities."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'computations/boundary-structure-2026-09-26'))
from exact import E, ZERO, ONE, OMEGA, require, outputs, matchings, cell


def energy_degrees(source,n=6):
    weights={}
    for (i,j,a,b),z in source.items():
        weights[i,j]=weights.get((i,j),Q(0))+z.abs2()
    degree=[sum(w for e,w in weights.items() if i in e) for i in range(n)]
    return sum(weights.values()),degree,weights


def scale(source,factors):
    require(all(x>0 for x in factors),'Positive site factors')
    p=Q(1)
    for x in factors:p*=x
    require(p==1,'Product of site factors must equal one')
    return {c:z*factors[c[0]]*factors[c[1]] for c,z in source.items()}


def prune(source,n=6):
    _,_,weights=energy_degrees(source,n)
    support={e for e,w in weights.items() if w}
    surviving=set()
    for matching in matchings(tuple(range(n))):
        if all(e in support for e in matching):surviving.update(matching)
    return {c:z for c,z in source.items() if c[:2] in surviving}


def certify_scaling(source,factors,n=6):
    """Check an exact finite scaling certificate; reject approximate balance."""
    before,_,_=energy_degrees(source,n)
    reduced=prune(source,n)
    require(bool(reduced),'At least one supported perfect matching')
    balanced=scale(reduced,factors)
    after,degrees,_=energy_degrees(balanced,n)
    require(all(d==Q(2,n)*after for d in degrees),'Every site has exactly equal incident strength')
    require(after<=before,'Certified norm does not increase')
    # Global minimality within the pruned scaling orbit follows from the
    # convexity proof; this finite check certifies its exact hypotheses.
    return balanced,dict(original_energy=str(before),balanced_energy=str(after),
                         rate_gain=str((before/after)**(n//2)),
                         removed_cells=len(source)-len(reduced),minimum_scope='Positive scaling orbit of the pruned source')


def block(source,i,j,colors):
    return [[source.get(cell(i,j,a,b),ZERO) if i!=j else ZERO for b in range(colors)] for a in range(colors)]


def gram(left,right):
    return [[sum((x*y.conjugate() for x,y in zip(row,col)),ZERO) for col in right] for row in left]


def norm2(matrix):
    return sum(x.abs2() for row in matrix for x in row)


def trace_product(left,right):
    z=sum((left[i][j]*right[j][i] for i in range(len(left)) for j in range(len(left))),ZERO)
    require(z.b==0,'Trace of a product of Hermitian matrices is real')
    return z.a


def response_identity(source,n=6,colors=3):
    S,degrees,weights=energy_degrees(source,n)
    getw=lambda i,j:weights.get(tuple(sorted((i,j))),Q(0))
    blocks={(i,j):block(source,i,j,colors) for i in range(n) for j in range(n) if i!=j}
    rho={e:gram(B,B) for e,B in blocks.items()}
    angular=Q(0)
    for i in range(n):
        for j,k in combinations([v for v in range(n) if v!=i],2):
            term=getw(i,j)*getw(i,k)-trace_product(rho[i,j],rho[i,k])
            require(term>=0,'Every local Gram slack is nonnegative')
            angular+=term
    off=Q(0)
    for i,j in combinations(range(n),2):
        B=[[ZERO]*colors for _ in range(colors)]
        for k in range(n):
            if k in (i,j):continue
            term=gram(blocks[i,k],blocks[j,k])
            B=[[x+y for x,y in zip(row,col)] for row,col in zip(B,term)]
        off+=norm2(B)
    cofactor_norms=[]
    for vertices in combinations(range(n),4):
        ix={v:i for i,v in enumerate(vertices)}
        selected={(ix[i],ix[j],a,b):z for (i,j,a,b),z in source.items() if i in ix and j in ix}
        h=outputs(selected,n=4,colors=colors)
        cofactor_norms.append(sum(z.abs2() for z in h.values()))
    T=sum(cofactor_norms)
    rhs=S*S/2-Q(3,4)*sum(d*d for d in degrees)+sum(w*w for w in weights.values())+(angular+off)/2
    require(T==rhs,'Exact four-site response norm identity')
    balanced=all(d==Q(2,n)*S for d in degrees)
    if n==6:
        variance=sum((d-S/3)**2 for d in degrees)
        edge_variance=sum((getw(i,j)-S/15)**2 for i,j in combinations(range(n),2))
        require(T+Q(3,4)*variance==S*S/15+edge_variance+(angular+off)/2,'Robust six-site sum of nonnegative terms')
    if n==6 and balanced:
        require(T>=S*S/15,'Sharp balanced four-site lower bound')
        require(max(cofactor_norms)>=S*S/225,'An individual response column has norm at least S/15')
    return dict(energy=str(S),degrees=list(map(str,degrees)),four_site_norm_squared=str(T),
                edge_square_sum=str(sum(w*w for w in weights.values())),local_gram_slack=str(angular),
                off_diagonal_gram_norm_squared=str(off),balanced=balanced,
                maximum_four_site_norm_squared=str(max(cofactor_norms)))

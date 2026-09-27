"""Exact triangle response ranks and explicit polynomial kernel certificates."""
from pathlib import Path
from itertools import combinations, product
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'computations/boundary-structure-2026-09-26'))
from exact import E, ZERO, ONE, OMEGA, Q, require, cell, outputs, rank, hafnian


def response(source,colors=3):
    matrix=[]
    for word in product(range(colors),repeat=3):
        row=[]
        for i,h in product(range(3),range(colors)):
            j,k=[v for v in range(3) if v!=i]
            row.append(source.get((j,k,word[j],word[k]),ZERO) if word[i]==h else ZERO)
        matrix.append(row)
    return matrix


def kernel(matrix):
    a=[row[:] for row in matrix];rows=len(a);cols=len(a[0]);pivots=[]
    r=0
    for c in range(cols):
        p=next((i for i in range(r,rows) if a[i][c]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r];d=a[r][c];a[r]=[x/d for x in a[r]]
        for i in range(rows):
            if i!=r and a[i][c]:
                d=a[i][c];a[i]=[x-d*y for x,y in zip(a[i],a[r])]
        pivots.append(c);r+=1
    basis=[]
    for c in range(cols):
        if c in pivots:continue
        v=[ZERO]*cols;v[c]=ONE
        for i,p in enumerate(pivots):v[p]=-a[i][c]
        require(all(not sum((x*y for x,y in zip(row,v)),ZERO) for row in matrix),'Exact kernel vector')
        basis.append(v)
    return basis


def determinant_source(x,y,colors=3):
    out={}
    for i,j in combinations(range(3),2):
        sign=-1 if (i,j)==(0,2) else 1
        for a,b in product(range(colors),repeat=2):
            z=sign*(x[i*colors+a]*y[j*colors+b]-y[i*colors+a]*x[j*colors+b])
            if z:out[i,j,a,b]=z
    return out


def classify(source,colors=3):
    require(all(any(z for (u,v,a,b),z in source.items() if (u,v)==(i,j)) for i,j in combinations(range(3),2)),
            'All three triangle edge blocks must be nonzero')
    U=response(source,colors);K=kernel(U)
    require(len(K)<=2,'At most two independent triangle kernel directions')
    if len(K)==1:
        support=[i for i in range(3) if any(K[0][i*colors:(i+1)*colors])]
        require(len(support)==2,'A one-dimensional kernel uses exactly two sites')
        kind='shared_rank_one_pair'
    elif len(K)==2:
        candidate=determinant_source(K[0],K[1],colors)
        first=next(c for c,z in source.items() if z)
        require(first in candidate,'Nonzero determinant certificate')
        factor=source[first]/candidate[first]
        require(all(source.get(c,ZERO)==factor*candidate.get(c,ZERO) for c in set(source)|set(candidate)),
                'All three edge blocks are proportional to the cross-product minors')
        kind='determinantal'
    else:kind='regular'
    return dict(rank=3*colors-len(K),kernel_dimension=len(K),kind=kind)


def fixtures():
    regular={(0,1,0,0):ONE,(0,2,1,1):ONE,(1,2,2,2):ONE}
    shared={(0,1,1,1):ONE,(0,2,0,0):-ONE,(1,2,0,0):ONE}
    scalar={(i,j,0,0):ONE for i,j in combinations(range(3),2)}
    x=[ONE,ZERO,ZERO]*3;y=[ZERO,ONE,ZERO]*3
    singlets=determinant_source(x,y)
    dense_x=[E(1+i%3,i%2) for i in range(9)]
    dense_y=[E((2*i+1)%3,1-(i%3)) for i in range(9)]
    dense=determinant_source(dense_x,dense_y)
    return {'regular':regular,'shared_pair':shared,'scalar':scalar,'singlets':singlets,'dense_determinantal':dense}


def jacobian_rank(source,colors=3):
    cells=[(i,j,a,b) for i,j in combinations(range(6),2) for a,b in product(range(colors),repeat=2)]
    rows={}
    for i,j in combinations(range(6),2):
        vertices=[v for v in range(6) if v not in (i,j)];mapping={v:k for k,v in enumerate(vertices)}
        reduced={(mapping[u],mapping[v],a,b):z for (u,v,a,b),z in source.items() if u in mapping and v in mapping}
        H=outputs(reduced,n=4,colors=colors)
        for a,b in product(range(colors),repeat=2):
            col=cells.index((i,j,a,b))
            for word,z in H.items():
                full=[None]*6;full[i]=a;full[j]=b
                for v,h in zip(vertices,word):full[v]=h
                rows.setdefault(tuple(full),[ZERO]*len(cells))[col]=z
    return rank(list(rows.values()))


def check():
    fs=fixtures();classes={name:classify(A) for name,A in fs.items()}
    require([classes[n]['rank'] for n in ('regular','shared_pair','scalar','singlets','dense_determinantal')]==[9,8,7,7,7],
            'Every possible response rank and both determinant degenerations')
    pairs={}
    names=['regular','shared_pair','scalar']
    for p,left in enumerate(names):
        for right in names[p:]:
            A=dict(fs[left]);A.update({(i+3,j+3,a,b):z for (i,j,a,b),z in fs[right].items()})
            require(not outputs(A),'No perfect matching across two disconnected triangles')
            r=jacobian_rank(A)
            require(r==classes[left]['rank']*classes[right]['rank'],'Full six-site Jacobian agrees with the tensor-product response rank')
            pairs[left+' / '+right]=r
    # A supported-matching cancellation limit, outside the two-triangle class.
    ground={(0,1):ONE,(2,3):ONE,(0,2):OMEGA,(1,3):OMEGA,
            (0,3):OMEGA*OMEGA,(1,2):OMEGA*OMEGA,(4,5):E(-2)}
    ground.update({(i,j):ONE for i in range(4) for j in (4,5)})
    A={(i,j,0,0):z for (i,j),z in ground.items()}
    require(not outputs(A),'Complete-support cancellation example has zero output')
    C={(i,j):hafnian(ground,tuple(v for v in range(6) if v not in (i,j))) for i,j in combinations(range(6),2)}
    require({e for e,z in C.items() if z}=={(0,2),(0,3),(1,2),(1,3)},'Cofactor support is a four-cycle')
    require(jacobian_rank(A)==25,'Supported-matching cancellation has derivative rank 25')
    t=(Q(-1,4),Q(1,4))  # t = (sqrt(13)-1)/4.
    t2=(t[0]*t[0]+13*t[1]*t[1],2*t[0]*t[1])
    require((4*t2[0]+2*t[0]-3,4*t2[1]+2*t[1])==(0,0),'Exact balance equation for the algebraic representative')
    try:classify({c:z for c,z in fs['scalar'].items() if c[:2]!=(0,1)})
    except ValueError:negative='REJECTED'
    else:raise ValueError('Missing triangle block was accepted')
    return dict(triangles=classes,two_triangle_jacobian_ranks=pairs,
                negative_control_missing_edge=negative,
                complete_support_example={'source_energy':18,'derivative_rank':25,'isolated_cofactor_rows':[4,5],
                                          'balanced_representative':'Exists by finite site scaling; same output and Jacobian rank'})

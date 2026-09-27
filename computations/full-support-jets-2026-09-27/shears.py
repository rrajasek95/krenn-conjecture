"""Exact W-preserving shear formulas and a norm obstruction."""
from jets import *


def shear(source,s):
    require(sum(s,ZERO)==ZERO,'W-preserving shear parameters sum to zero')
    out={}
    for i,j in combinations(range(6),2):
        D=source.get((i,j,0,0),ZERO)
        u=source.get((i,j,1,0),ZERO)
        v=source.get((i,j,0,1),ZERO)
        Y=source.get((i,j,1,1),ZERO)
        entries={(0,0):D+s[i]*u+s[j]*v+s[i]*s[j]*Y,
                 (1,0):u+s[j]*Y,(0,1):v+s[i]*Y,(1,1):Y}
        out.update({(i,j,a,b):z for (a,b),z in entries.items() if z})
    return out


def energy(source):
    return sum(z.abs2() for z in source.values())


def example():
    A={(i,j,0,0):ONE for i in (2,3) for j in (4,5)}
    for i in range(2,6):
        sign=1 if i in (2,3) else -1
        A[0,i,0,0]=E(Q(-sign,2));A[1,i,0,0]=E(Q(1,2))
        A[0,i,0,1]=E(Q(1,2));A[1,i,0,1]=E(Q(sign,2))
    A[0,1,0,1]=A[0,1,1,0]=E(Q(1,2))
    return A


def check():
    A=example();W={tuple(int(v==i) for v in range(6)):ONE for i in range(6)}
    require(outputs(A)==W and energy(A)==Q(17,2),'Exact original W source')
    # M sends arbitrary shear parameters to the change in ground entries.
    M=[];d=[]
    for i,j in combinations(range(6),2):
        row=[ZERO]*6
        row[i]=A.get((i,j,1,0),ZERO);row[j]=A.get((i,j,0,1),ZERO)
        M.append(row);d.append(A.get((i,j,0,0),ZERO))
    require(all(not sum((row[k].conjugate()*z for row,z in zip(M,d)),ZERO) for k in range(6)),
            'Ground vector is orthogonal to every shear direction')
    for i,j in product(range(6),repeat=2):
        got=sum((row[i].conjugate()*row[j] for row in M),ZERO)
        expected=E(Q(1,4)) if i<2 and j<2 else E(Q(1,2)) if i==j else ZERO
        require(got==expected,'Universal Hermitian Gram certificate for all complex shears')
    parameters=[OMEGA,-OMEGA,ONE,ONE,-ONE,-ONE]
    moved=shear(A,parameters)
    require(outputs(moved)==W,'Complex W-stabilizer covariance')
    require(energy(moved)==Q(21,2),'Every root-0 isolation has exact source cost 21/2')
    require(all(not moved.get((0,j,0,0),ZERO) for j in range(1,6)),'Ground root 0 is isolated')
    for root,sign in ((0,1),(1,-1)):
        s=[ZERO,ZERO,E(sign),E(sign),E(-sign),E(-sign)]
        changed=shear(A,s)
        require(outputs(changed)==W and energy(changed)==Q(21,2),'Both possible isolated roots have the same higher cost')
        require(all(not changed.get(cell(root,j,0,0),ZERO) for j in range(6) if j!=root),'Required ground row vanishes')
    # A core site's unit ground edges are invariant because both mixed cells vanish.
    for i in range(2,6):
        j=4 if i in (2,3) else 2
        require(A[cell(i,j,0,0)]==ONE and not A.get(cell(i,j,1,0),ZERO) and not A.get(cell(i,j,0,1),ZERO),
                'Core sites cannot be ground-isolated by any shear')
    return dict(original_energy='17/2',minimum_shear_orbit_energy='17/2',
                ground_isolating_energy='21/2',original_rate='48/4913',
                ground_isolating_rate='16/3087',
                scope='All complex upper-triangular local shears preserving W; excludes additional transformations',
                negative_control='Ground isolation by shears alone need not preserve or improve rate')

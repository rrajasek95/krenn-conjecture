#!/usr/bin/env python3
"""Exact supporting checks for the all-even two-root W optimum."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, prod
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'computations/higher-order-2026-09-26'))
from shared import E, ZERO, ONE, OMEGA, require, outputs, hafnian, mv, dot, solve


def odd(k):
    return prod(range(1, k+1, 2))


def constants(n):
    m, N = n//2, n-2
    B = F(odd(n-1)**2, comb(n, 2)**m)
    optimum = n*B/((n-1)**2+1)
    K = F(odd(N-3)**2, comb(N, 2)**(m-3))
    upper = F(2*n*(N-2)*(m-2)**(m-2), m**m*N**3)*K
    d = (m-1)*(2*m-3)
    simplified = F(m-2, m-1)*(1+F(3*m-2, d))*(1-F(1, d))**(m-2)
    gap = 1-F(1, (m-1)*(2*m*m-4*m+1))
    require(upper/optimum == simplified, 'Original all-orders constant equals the simplified ratio')
    require(simplified <= gap < 1, 'Strict disconnected gap at this checked order')
    return optimum, upper, gap


def polynomial_checks():
    def mul(p, q):
        out = {}
        for i, x in p.items():
            for j, y in q.items():
                out[i+j] = out.get(i+j, 0)+x*y
        return {i:x for i,x in out.items() if x}
    denominator = mul({1:1, 0:-1}, {2:2, 1:-4, 0:1})
    numerator = mul({1:1, 0:-2}, {2:2, 1:-2, 0:1})
    difference = {i:denominator.get(i,0)-numerator.get(i,0) for i in denominator.keys() | numerator.keys()}
    require({i:x for i,x in difference.items() if x} == {0:1}, 'Denominator minus numerator is identically one')
    # d(d+r) - (d-1)(d+r+1) = r+1, certifying the induction step
    # (1-1/d)^r <= d/(d+r) for every integer r>=0 and real d>1.
    def mul2(p,q):
        out={}
        for (i,j),x in p.items():
            for (k,l),y in q.items():
                out[i+k,j+l]=out.get((i+k,j+l),0)+x*y
        return {key:z for key,z in out.items() if z}
    left=mul2({(1,0):1},{(1,0):1,(0,1):1})
    right=mul2({(1,0):1,(0,0):-1},{(1,0):1,(0,1):1,(0,0):1})
    difference = {key:left.get(key,0)-right.get(key,0) for key in left.keys() | right.keys()}
    require({key:x for key,x in difference.items() if x} == {(0,1):1,(0,0):1}, 'Reciprocal-power bound induction identity')
    return dict(gap_identity='denominator - numerator = 1', power_bound_identity='d(d+r)-(d-1)(d+r+1)=r+1')


def disconnected_example(n):
    vertices = tuple(range(2, n))
    D = {(i, i+1): ONE for i in range(2, n, 2)}
    C = {(i,j):hafnian(D, tuple(v for v in vertices if v not in (i,j))) for i,j in combinations(vertices,2)}
    require({e for e,z in C.items() if z} == set(D), 'Disconnected matching cofactor support')
    source = {(i,j,0,0):z for (i,j),z in D.items()}
    for i in vertices:
        source[0,i,0,1] = source[1,i,0,0] = ONE
    source[0,1,1,0] = source[0,1,0,1] = ONE
    expected = {tuple(int(i==j) for j in range(n)):ONE for i in range(n)}
    require(outputs(source,n=n) == expected, 'Every output of the disconnected W fixture')
    energy = sum(z.abs2() for z in source.values())
    rate = F(n)/energy**(n//2)
    optimum, upper, gap = constants(n)
    require(rate <= upper < optimum, 'Fixture respects the uniform disconnected upper bound')
    return dict(sites=n, components=len(D), source_energy=str(energy), actual_rate=str(rate),
                disconnected_upper=str(upper), optimum=str(optimum))


def four_site_example():
    # Check the mixed connected reduction also at the smallest nontrivial core.
    C = [[ZERO,ONE],[ONE,ZERO]]
    signs = (1,-1)
    u = [ONE,OMEGA]
    z = solve(C, [ONE/a for a in u])
    r, k, root_k = F(3,4)*OMEGA, F(25,16), F(5,4)
    x = [-r.conjugate()*s*a/k for s,a in zip(signs,z)]
    y = [a/k for a in z]
    source = {(2,3,0,0):E(2)}
    for i,xx,yy,uu,sgn in zip((2,3),x,y,u,signs):
        source[0,i,0,0],source[1,i,0,0] = xx,yy
        source[0,i,0,1],source[1,i,0,1] = uu,r*sgn*uu
    source[0,1,1,0] = source[0,1,0,1] = E(F(1,2))
    require(dot(x,mv(C,y)) == ZERO, 'No ground output in the mixed fixture')
    reduced = {(2,3,0,0):E(2),(0,1,1,0):E(F(1,2)),(0,1,0,1):E(F(1,2))}
    for i,uu,zz in zip((2,3),u,z):
        reduced[0,i,0,1],reduced[1,i,0,0] = root_k*uu,zz/root_k
    expected = {tuple(int(i==j) for j in range(4)):ONE for i in range(4)}
    require(outputs(source,n=4)==expected and outputs(reduced,n=4)==expected, 'Four-site exact connected reduction')
    require(sum(z.abs2() for z in source.values()) == sum(z.abs2() for z in reduced.values()), 'Balanced reduction preserves norm')
    return dict(sites=4, output_words=81, optimum='1/10', reduction='PASS')


def main():
    dependencies = json.loads((HERE/'dependencies.json').read_text())
    for relative,expected in dependencies.items():
        require(hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==expected, 'Pinned dependency: '+relative)
    table = []
    for n in range(6, 102, 2):
        optimum, upper, gap = constants(n)
        if n <= 14:
            table.append(dict(sites=n,optimum=str(optimum),disconnected_ratio_upper=str(gap)))
    result = dict(status='PASS', evidence_status='Written all-orders theorem with exact supporting checks; independent audit pending',
                  polynomial_identities=polynomial_checks(), constant_orders_checked=48, rate_table=table,
                  four_site=four_site_example(), disconnected_examples=[disconnected_example(n) for n in (6,8,10)],
                  scope='All even site counts in the two-root architecture with a scalar ground-color core',
                  unresolved='Arbitrary colored cores and unrestricted W-state optimality', dependencies=dependencies)
    files = sorted(p for p in HERE.iterdir() if p.suffix in ('.py','.json','.md') and p.name!='results.json')
    files.append(ROOT/'notes/w-state-two-root-optimum-2026-09-26.md')
    result['sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()

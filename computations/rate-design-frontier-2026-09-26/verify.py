#!/usr/bin/env python3
"""Replay exact research certificates; not an independent audit or Lean proof."""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import core
import boundary

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C, ZERO, ONE = core.C, core.ZERO, core.ONE


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value


def output(source, word):
    terms = []
    for matching in core.matchings(tuple(range(6))):
        value = ONE
        for p, q in matching:
            value *= source.get((p, q, word[p], word[q]), ZERO)
        terms.append(value)
    return sum(terms, ZERO), terms


def prism_source(t, physical_scale=ONE):
    source = {}
    for p, q, h in [(0,1,0),(3,4,0),(1,2,1),(4,5,1),(0,2,2),(3,5,2)]:
        source[p,q,h,h] = physical_scale
    for p,q,h in [(2,5,0),(0,3,1),(1,4,2)]:
        source[p,q,h,h] = physical_scale*t
    return source


def aggregate_checks():
    source = prism_source(Q(1,10))
    u = Q(1,10000)
    source[2,3,1,1],source[2,4,1,1],source[3,5,1,1] = C(u*u),C(u),C(-u)
    actual = {}
    p2, e2 = Q(0), Q(0)
    cancelled = 0
    for w in boundary.WORDS:
        value, terms = output(source,w)
        actual[w] = value
        if len(set(w)) > 1 and all(w.count(h)%2 == 0 for h in range(3)):
            core.require(all(not z.im for z in terms), 'Chosen envelope is rational')
            envelope = sum(abs(z.re) for z in terms)
            p2 += envelope**2
            e2 += value.abs2()
            cancelled += bool(envelope and not value)
    core.require(actual[0,0,1,1,1,1] == 0 and cancelled > 0, 'Minimum cancellation margin is zero')
    pure = [actual[(h,)*6] for h in range(3)]
    core.require(pure == [C(Q(1,10))]*3, 'Pure amplitudes unchanged')
    norm2 = sum(z.abs2() for z in actual.values())
    fidelity = Q(3,100)/norm2
    core.require(fidelity > Q(9999,10000), 'High-fidelity strict-extension witness')
    core.require(e2 > Q(99,100)**2*p2, 'Aggregate cancellation margin exceeds .99')
    source_norm = sum(z.abs2() for z in source.values())
    pure_product2 = pure[0].abs2()*pure[1].abs2()*pure[2].abs2()
    core.require(pure_product2 <= Q(41,1440)*source_norm**6*p2, 'Positive envelope inequality on witness')
    return dict(minimum_margin='0', completely_cancelled_mixed_words=cancelled,
                fidelity=str(fidelity), aggregate_margin_squared=str(e2/p2),
                aggregate_margin_lower='99/100')


def optimizer_checks():
    payloads = json.loads((HERE/'certificates.json').read_text())
    payloads.append(json.loads((HERE/'complex-certificate.json').read_text()))
    reports=[]
    for p in payloads:
        row=core.verify_certificate(p)
        core.require(Q(row['relative_gap']) < Q(1,20_000_000), 'Relative primal-dual gap below 5e-8')
        core.require(Q(row['fixed_core_fidelity_ceiling']) == (Q(2)+1/(1+Q(1,10)**4))/3,
                     'Prism core fidelity ceiling')
        reports.append(row)
    cycle=core.verify_certificate(json.loads((HERE/'cycle-certificate.json').read_text()))
    core.require(Q(cycle['fixed_core_fidelity_ceiling'])==Q(2,3),'Cycle exact feasibility ceiling')
    core.require(Q(cycle['rate_lower'])==Q(4,675),'Cycle constant-Gram optimum is attained exactly')
    bad=json.loads((HERE/'cycle-certificate.json').read_text());bad['fidelity_floor']='9/10'
    try: core.verify_certificate(bad)
    except ValueError: pass
    else: raise ValueError('Infeasible fixed-core fidelity accepted')
    bad=copy.deepcopy(payloads[0]);bad['upper_eigenvalue']='0'
    try: core.verify_certificate(bad)
    except ValueError: pass
    else: raise ValueError('Corrupted optimizer upper certificate accepted')
    bad=copy.deepcopy(payloads[0]);bad['witness']=[['0','0']]*45
    try: core.verify_certificate(bad)
    except ValueError: pass
    else: raise ValueError('Zero-output optimizer witness accepted')
    # Independently compare root expansion with direct full matchings, over Q(i).
    source=core.read_source(payloads[-1]['core']);root=payloads[-1]['root']
    data=core.matrices(source,root)
    v=[core.decode(z) for z in payloads[-1]['witness']]
    vertices=tuple(i for i in range(6) if i!=root)
    for h in range(3):
        for j,(p,i) in enumerate(product(vertices,range(3))):
            key=(p,root,i,h) if p<root else (root,p,h,i)
            source[key]=v[15*h+j]
    words=list(product(range(3),repeat=5))
    direct_norm=Q(0)
    for w in boundary.WORDS:
        r=words.index(tuple(w[i] for i in vertices))
        direct,_=output(source,w)
        response=sum((x*y for x,y in zip(data['T'][r],v[15*w[root]:15*(w[root]+1)])),ZERO)
        core.require(direct==response,'Literal fixed-core matching formula')
        direct_norm+=direct.abs2()
    core.require(direct_norm==core.quadratic(data['K'],v),'Incident Gram equals full output norm')
    # Exact scale derivative: d[t/(a+t)^3]/dt = (a-2t)/(a+t)^4.
    for a in (Q(1,7),Q(201,50),Q(12)):
        optimum=Q(4,27)/a**2
        for t in (a/8,a/2,a,3*a):
            core.require(t/(a+t)**3 <= optimum,'Source-norm allocation maximum')
    return dict(certificates=reports, degenerate_top_eigenspace=cycle, direct_complex_words=729,
                corrupted_upper='REJECTED', zero_output_witness='REJECTED', infeasible_fidelity='REJECTED')


def prism_checks():
    rows=[]
    for t in (Q(1,2),Q(1,10),Q(1,100)):
        source=prism_source(t)
        actual={w: output(source,w)[0] for w in boundary.WORDS}
        expected={(h,)*6:C(t) for h in range(3)}
        expected[(1,2,0)*2]=C(t**3)
        core.require({w:z for w,z in actual.items() if z}==expected,'Weighted prism expansion')
        S=6+3*t*t; R=(3*t*t+t**6)/S**3; F=Q(3)/(3+t**4)
        r=t*t
        core.require(R==r*(3+r*r)/(27*(2+r)**3),'Balanced exact frontier attained')
        delta=1-F
        # Square the asymptotic ratio to avoid irrational arithmetic.
        ratio2=R*R/delta
        rows.append(dict(t=str(t),F=str(F),R=str(R),squared_rate_over_sqrt_error=str(ratio2)))
        # Physical weights x=y=1/sqrt(3), z=t/sqrt(3): all probabilities rational.
        physical=Q(2,3)**6*(1-t*t/3)**3*(3*t*t+t**6)/27
        core.require(physical>0, 'Physical achievability family')
    core.require(Q(3,72**2)==Q(1,1728),'Sharp normalized coefficient squared')
    core.require(Q(64**2*3,6561**2)==Q(4096,14348907),'Sharp physical coefficient squared')
    # Polynomial positivity in x^2: 4/27 - x^2(1-x^2)^2
    # = (x^2-1/3)^2(4/3-x^2), nonnegative on [0,1].
    for q in [Q(i,100) for i in range(101)]:
        core.require(Q(4,27)-q*(1-q)**2==(q-Q(1,3))**2*(Q(4,3)-q),
                     'Physical single-edge maximum factorization')
    return dict(sharp_normalized_coefficient_squared='1/1728',
                sharp_physical_coefficient_squared='4096/14348907', balanced_examples=rows)


def singular_checks():
    payload=json.loads((HERE/'singular-certificate.json').read_text())
    result=boundary.verify(payload)
    previous=module('frontier_old_boundary','computations/rate-boundary-gate-2026-09-26/verify.py')
    source={(0,q,h,h):1 for q in range(2,6) for h in range(3)}
    source.update({(1,q,h,h):1 for q in (2,3) for h in range(3)})
    ranks=[]
    for root in range(6):
        T,G=previous.core_response(source,root)
        ranks.append([previous.rank(T),previous.rank([a+b for a,b in zip(T,G)])])
    core.require(ranks==[[0,3],[0,3],[6,9],[6,9],[9,12],[9,12]],'Old rank filter passes new base')
    result['old_response_and_augmented_ranks']=ranks
    full,L,M=boundary.maps()
    # Direct complex check of the kernel lift and both crossing block orders.
    K=[C(Q(i-4,11),Q((i*i)%5-2,13)) for i in range(9)]
    U=[C(Q(i%7-3,17),Q(i%5-2,19)) for i in range(18)]
    actual={key:C(v) for key,v in source.items()}
    for i,j in product(range(3),repeat=2): actual[2,3,i,j]=K[3*i+j]
    for t,h,k in product(range(2),range(3),range(3)): actual[1,4+t,h,k]=U[9*t+3*h+k]
    tensor=[x*y for x in K for y in U]
    for row,w in zip(M,boundary.WORDS):
        value,_=output(actual,w)
        core.require(value==sum((c*z for c,z in zip(row,tensor)),ZERO),'Literal complex kernel lift')
    visible=[ZERO if c<9 else C(Q(c%7-3,23),Q(c%5-2,29)) for c in range(54)]
    actual={key:C(value) for key,value in source.items()}
    actual.update({cell:value for cell,value in zip(boundary.CELLS,visible)})
    for row,w in zip(full,boundary.WORDS):
        value,_=output(actual,w)
        core.require(value==sum((c*z for c,z in zip(row,visible)),ZERO),'Literal complex singular linear response')
    bad=copy.deepcopy(payload);bad['projection_solve'][0][2]='999'
    try: boundary.verify(bad)
    except ValueError: result['projection_mutation']='REJECTED'
    else: raise ValueError('Corrupt singular projection certificate accepted')
    # Without the index swap, the alleged identity lower bound is false.
    coupling=boundary.cross(L,M)
    X=boundary.sparse_decode(45,162,payload['projection_solve'])
    correction=boundary.multiply(boundary.transpose(coupling),X)
    MM=boundary.cross(M,M)
    wrong=[[C(MM[i][j]-correction[i][j]-(i==j)) for j in range(162)] for i in range(162)]
    try: core.psd(wrong)
    except ValueError: result['unrestricted_tensor_lower_bound']='REJECTED AS REQUIRED'
    else: raise ValueError('Missing product-vector scope guard')
    J=[[wrong[i][j]+(i==j) for j in range(162)] for i in range(162)]
    partial=[[J[(j//18)*18+i%18][(i//18)*18+j%18] for j in range(162)] for i in range(162)]
    conjugated=[core.conj(x)*y for x in K for y in U]
    observed=core.quadratic(J,tensor)
    core.require(observed==core.quadratic(partial,conjugated),'Complex partial-transpose product identity')
    core.require(observed>=core.dot(K,K).re*core.dot(U,U).re,'Complex product lower bound')
    result['direct_complex_linear_and_bilinear_words']=1458
    return result


def pins():
    previous=ROOT/'computations/rate-sharpness-followup-2026-09-26/results.json'
    old=json.loads(previous.read_text())
    for rel,expected in old['sha256'].items():
        core.require(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==expected,'Earlier pinned dependency: '+rel)
    names=['verify.py','core.py','boundary.py','search.py','certificates.json','complex-certificate.json',
           'singular-certificate.json','prism-core.json','cycle-certificate.json']
    files=[HERE/name for name in names]+[previous,
        ROOT/'notes/rate-design-frontier-2026-09-26.md',
        ROOT/'notes/prism-optimal-rate-2026-09-26.md',
        ROOT/'notes/singular-kernel-rate-exclusion-2026-09-26.md',
        ROOT/'computations/rate-boundary-gate-2026-09-26/verify.py',
        ROOT/'computations/universal-rate-gate-2026-09-26/verify.py']
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,help='Verify a user-supplied fixed-core certificate instead')
    args=parser.parse_args()
    if args.certificate:
        print(json.dumps(core.verify_certificate(json.loads(args.certificate.read_text())),indent=2));return
    hashes=pins()
    gate=module('frontier_positive_cover','computations/universal-rate-gate-2026-09-26/verify.py')
    vertices,edges,ms,_=gate.setup()
    result=dict(status='PASS',evidence_status='WRITTEN RESEARCH; NOT INDEPENDENTLY AUDITED',
                scope='Exact finite certificates support the separate analytic arguments; not a Lean proof.',
                aggregate_cancellation=aggregate_checks(),
                inherited_positive_cover=gate.check_positive_cover(vertices,edges,ms),
                fixed_core_optimizer=optimizer_checks(),prism_optimality=prism_checks(),
                singular_boundary=singular_checks(),sha256=hashes)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()

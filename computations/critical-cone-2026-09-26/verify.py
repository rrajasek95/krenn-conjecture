#!/usr/bin/env python3
"""Check the saved characteristic-zero cone direction and cubic obstruction."""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'computations/higher-order-2026-09-26'))
from shared import E, ZERO, ONE, OMEGA, require, critical_core, outputs, matchings, hafnian


def quadratic(base, first, word):
    value = ZERO
    for matching in matchings(tuple(range(6))):
        keys = [(i,j,word[i],word[j]) for i,j in matching]
        for p in range(3):
            q = base.get(keys[p], ZERO)
            if q:
                i,j = [k for k in range(3) if k != p]
                value += q*first.get(keys[i],ZERO)*first.get(keys[j],ZERO)
    return value


def linear_third(base, first, word):
    """Coefficients of every free second-jet cell in [Q B C]_word."""
    out = {}
    for matching in matchings(tuple(range(6))):
        keys = [(i,j,word[i],word[j]) for i,j in matching]
        for p in range(3):
            q = base.get(keys[p],ZERO)
            if not q:
                continue
            for j in range(3):
                if j == p:
                    continue
                b = first.get(keys[j],ZERO)
                if b:
                    k = 3-p-j
                    out[keys[k]] = out.get(keys[k],ZERO)+q*b
    return out


def main():
    dependencies = json.loads((HERE/'dependencies.json').read_text())
    for name,expected in dependencies.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected, 'Pinned dependency: '+name)
    fixture=json.loads((HERE/'fixture.json').read_text())
    first={tuple(map(int,c.split(','))):E(*z) for c,z in fixture['first_jet'].items()}
    dual={tuple(map(int,w)):E(*z) for w,z in fixture['obstruction'].items()}
    q=critical_core()
    base={(i,j,0,0):z for (i,j),z in q.items()}
    require(all(hafnian(q,vertices)==ZERO for vertices in combinations(range(6),4)),
            'All four-site base tensors vanish, so the next source jet has no cubic contribution')
    require(all(quadratic(base,first,w)==ZERO for w in product(range(3),repeat=6)), 'All 729 quadratic outputs vanish')
    cubic=outputs(first)
    quartic=ZERO
    for (i,j),z in q.items():
        word=[1]*6
        word[i]=word[j]=0
        quartic += first.get((i,j,1,1),ZERO)*cubic.get(tuple(word),ZERO)/(2*z)
    require(quartic == -OMEGA == E(*fixture['quartic']), 'Quartic expression is nonzero over Q(omega)')
    cells=tuple((i,j,a,b) for i,j in combinations(range(6),2) for a,b in product(range(3),repeat=2))
    coefficients={w:linear_third(base,first,w) for w in dual}
    require(all(sum((weight*coefficients[w].get(c,ZERO) for w,weight in dual.items()),ZERO)==ZERO for c in cells),
            'Four-word witness annihilates every one of the 135 free second-jet columns')
    pairing=sum((weight*cubic.get(w,ZERO) for w,weight in dual.items()),ZERO)
    require(pairing==2*OMEGA and -pairing==E(*fixture['obstruction_pairing']), 'Unavoidable cubic error is exactly 2 omega')
    require(sum(z.abs2() for z in dual.values())==4 and pairing.abs2()==4, 'Cubic error norm is at least one')
    require(all(len(set(w))>1 for w in dual), 'Witness uses only off-target outputs')
    corrupt=dict(first)
    corrupt[0,1,1,1] += ONE
    require(any(quadratic(base,corrupt,w) for w in product(range(2),repeat=6)), 'Corrupt direction fails the quadratic gate')
    bad=dict(dual)
    bad[next(iter(bad))] += ONE
    require(any(sum((weight*coefficients[w].get(c,ZERO) for w,weight in bad.items()),ZERO) for c in cells),
            'Corrupt left-null witness is detected')
    result=dict(status='PASS',evidence_status='Exact rejection certificate; analytic interpretation awaiting independent audit',
                first_jet_nonzero_cells=len(first),quadratic_words_checked=729,quartic='-omega',
                cubic_obstruction_words=len(dual),second_jet_columns_checked=len(cells),unavoidable_cubic_pairing='2*omega',
                cubic_error_norm_lower='1',
                negative_controls={'corrupt_direction':'REJECTED','corrupt_witness':'REJECTED'},
                conclusion='The quadratic cone does not force quartic vanishing; this exact direction nevertheless fails the next extension equation',
                unresolved='Other directions and higher-order arcs; no counterexample to the square-root rate law',dependencies=dependencies)
    files=sorted(p for p in HERE.iterdir() if p.suffix in ('.py','.md','.json') and p.name!='results.json')
    files.append(ROOT/'notes/critical-cone-extension-obstruction-2026-09-26.md')
    result['sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()

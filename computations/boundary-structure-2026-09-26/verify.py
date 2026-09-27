#!/usr/bin/env python3
"""Reproduce finite evidence for the boundary-structure proofs.

Standard library only; all acceptance checks remain enabled with python -O.
The analytic theorems require independent audit and are not Lean formalized.
"""
import hashlib
import json
from pathlib import Path
from itertools import combinations, product
from fractions import Fraction as Q
from exact import E, ZERO, ONE, OMEGA, require, outputs, hafnian
import graphs
import examples
import prism_jets

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def arithmetic_checks():
    values = [E(a, b) for a, b in product(range(-2, 3), repeat=2)]
    for x in values:
        require(x.conjugate().conjugate() == x, 'Conjugation involution')
        require(x*x.conjugate() == E(x.abs2()), 'Exact complex norm')
        if x:
            require(x/x == ONE, 'Field inversion')
        for y in values:
            require((x*y).abs2() == x.abs2()*y.abs2(), 'Multiplicative norm')
    return dict(field='Q(omega), omega^2+omega+1=0', tested_elements=len(values), norm_products=len(values)**2)


def negative_controls():
    out = {}
    q = examples.critical_core()
    q[0, 1] += ONE
    require(any(hafnian(q, [j for j in range(5) if j != i]) for i in range(5)), 'Corrupt critical core is detected')
    out['corrupt_critical_core'] = 'REJECTED'
    support = set(combinations(range(5), 2))
    p, weights = graphs.cover(6, support)
    require(p == [Q(1, 4)]*5+[Q(-1, 4)], 'Explicit star-complement potential')
    weights[0, 1] += 1
    require(any(sum(weights.get(e, 0) for e in matching) != 1 for matching in graphs.matchings(tuple(range(6)))),
            'Corrupt matching cover is detected')
    out['corrupt_cover'] = 'REJECTED'
    cycle = {(0, 2), (0, 3), (1, 2), (1, 3)}
    comp = graphs.components(4, cycle)
    require(len(comp) == 1 and comp[0]['bipartite'], 'Bipartite exception is not classified as an odd-cycle graph')
    u, v = [ONE]*4, [ONE, ONE, -ONE, -ONE]
    require(all(u[i]*v[j]+u[j]*v[i] == ZERO for i, j in cycle), 'Nonzero vectors survive on a bipartite graph')
    out['dropping_odd_cycle_hypothesis'] = 'REJECTED'
    # A graph-independent claim that the critical source is fully excluded
    # would go beyond the checked hypotheses; the receipt explicitly retains it.
    return out


def main():
    dependencies = json.loads((HERE/'dependencies.json').read_text())
    for relative, expected in dependencies.items():
        require(hashlib.sha256((ROOT/relative).read_bytes()).hexdigest() == expected,
                'Pinned dependency unchanged: '+relative)
    result = dict(status='PASS', evidence_status='Written analytic proofs with exact supporting checks; awaiting independent audit',
                  arithmetic=arithmetic_checks(), support_census=graphs.census(),
                  critical_diagonal_boundary=examples.check_critical(),
                  mixed_output_identity=examples.diagonal_identity(),
                  four_site_identities=examples.four_site_identities(),
                  regular_triangles=examples.regular_triangles(), prism_jet_obstruction=prism_jets.verify(),
                  two_root_W=examples.w_two_roots(), negative_controls=negative_controls(),
                  dependencies=dependencies,
                  open_cases=['Unrestricted full-complex square-root law',
                              'Rank-deficient triangle limits and limits without a zero-crossing triangle split',
                              'Full-complex neighborhoods of the critical monochromatic core',
                              'W-state optimality for bipartite or disconnected cofactor graphs'])
    require(result['support_census']['excluded_supports'] == 6510, 'Support census count')
    files = sorted(p for p in HERE.iterdir() if p.suffix in ('.py', '.json', '.md') and p.name != 'results.json')
    files += [ROOT/'notes'/name for name in ('regular-triangle-rate-classification-2026-09-26.md',
              'diagonal-support-rate-exclusions-2026-09-26.md', 'two-root-w-state-reduction-2026-09-26.md')]
    result['sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

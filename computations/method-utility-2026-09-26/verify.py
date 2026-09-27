#!/usr/bin/env python3
"""Exact supporting replay; this is not an independent audit or a Lean proof."""
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from shared import ROOT, C, Q, ZERO, ONE, core, require
import examples
import polynomial
import quality

HERE = Path(__file__).resolve().parent


def reject(function, message):
    try:
        function()
    except ValueError:
        return 'REJECTED'
    raise ValueError(message)


def matrix_product(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), ZERO)
             for j in range(len(b[0]))] for i in range(len(a))]


def three_constraint_gap():
    I = [[ONE, ZERO], [ZERO, ONE]]
    pauli = [[[ZERO, ONE], [ONE, ZERO]],
             [[ZERO, C(0, -1)], [C(0, 1), ZERO]],
             [[ONE, ZERO], [ZERO, C(-1)]]]
    K = [[3*I[i][j]-sum((p[i][j] for p in pauli), ZERO) for j in range(2)] for i in range(2)]
    core.psd(K)
    require(all(matrix_product(p, p) == I for p in pauli), 'Pauli squares')
    for i in range(3):
        for j in range(i):
            a, b = matrix_product(pauli[i], pauli[j]), matrix_product(pauli[j], pauli[i])
            require(all(a[r][s]+b[r][s] == ZERO for r in range(2) for s in range(2)),
                    'Pauli anticommutation')
    v = [ONE, ZERO]
    require([core.quadratic(p, v) for p in pauli] == [0, 0, 1], 'Feasible pure witness')
    require(core.quadratic(K, v) == 2, 'Pure optimum witness')
    require((K[0][0]+K[1][1])/2 == C(3), 'Mixed witness gives three')
    require(all(3*I[i][j]-K[i][j]-sum((p[i][j] for p in pauli), ZERO) == ZERO
                for i in range(2) for j in range(2)), 'Exact zero dual slack')
    return dict(pure_optimum='2', relaxed_optimum='3',
                analytic_ingredient='Pure Bloch vectors have length one; positive octant has coordinate sum >= 1')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--quality', type=Path)
    group.add_argument('--integral', type=Path)
    group.add_argument('--arc', type=Path)
    args = parser.parse_args()
    for path, function in ((args.quality, quality.verify), (args.integral, polynomial.verify_integral),
                           (args.arc, polynomial.arc_outputs)):
        if path:
            print(json.dumps(function(json.loads(path.read_text())), indent=2, sort_keys=True))
            return
    pinned = json.loads((HERE/'dependencies.json').read_text())
    for name, expected in pinned.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected,
                'Unchanged pinned dependency: '+name)
    payload = json.loads((HERE/'two-quality-certificate.json').read_text())
    result = dict(evidence_status='Exact supporting calculations; analytic proofs await independent audit',
                  two_quality=quality.verify(payload), W=examples.verify_w(),
                  weighted_W=examples.verify_weighted_w(), three_constraint_gap=three_constraint_gap(),
                  robust_core_ball=quality.robust_upper(payload, '1/1000000', '20049/10000', '201/100', '2'),
                  integral_examples={name: polynomial.verify_integral(value) for name, value in
                                     [('genuine_integral_dependence', examples.toy_integral()),
                                      ('restricted_prism', examples.prism_integral())]},
                  arcs=[polynomial.arc_outputs(arc) for arc in
                        [examples.prism_arc(), examples.prism_arc(2), examples.prism_arc(cancellation=True)]])
    require(Q(result['two_quality']['relative_gap']) < Q(1, 10000), 'Useful two-quality interval')
    require(all(item['error_to_target_order'] == '3' and not item['violates_square_root'] for item in result['arcs']),
            'All saved arcs have the sharp prism exponent')
    # Recompute every old obstruction column: a receipt alone is not evidence.
    old = ROOT/'computations/complex-rate-bound-2026-09-26'
    spec = importlib.util.spec_from_file_location('utility_nonmembership', old/'verify.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    result['holomorphic_SOS_obstruction_dependency'] = module.check_dual(json.loads((old/'balanced-dual.json').read_text()))
    mutations = {}
    bad = deepcopy(payload)
    bad['upper_eigenvalue'] = '0'
    mutations['false_upper'] = reject(lambda: quality.verify(bad), 'False upper accepted')
    bad = deepcopy(payload)
    bad['qualities'][1]['threshold'] = '0'
    mutations['unmet_second_requirement'] = reject(lambda: quality.verify(bad), 'Unmet second requirement accepted')
    bad = deepcopy(payload)
    bad['witness'] = [['0', '0']]*45
    mutations['zero_output'] = reject(lambda: quality.verify(bad), 'Zero output accepted')
    bad = examples.toy_integral()
    bad['coefficients'][1][0]['multiplier'][0]['coefficient'] = ['1', '0']
    mutations['false_integral_identity'] = reject(lambda: polynomial.verify_integral(bad), 'False integral identity accepted')
    bad = examples.toy_integral()
    bad['coefficients'][1][0]['errors'] = [0]
    mutations['wrong_ideal_power'] = reject(lambda: polynomial.verify_integral(bad), 'Wrong ideal power accepted')
    bad = examples.toy_integral()
    bad['norm_constant'] = '1/2'
    mutations['false_norm_majorant'] = reject(lambda: polynomial.verify_integral(bad), 'False majorant accepted')
    mutations['false_response_norm'] = reject(lambda: quality.robust_upper(payload, '1/1000000',
                                                   '20049/10000', '201/100', '0'), 'False response norm accepted')
    # The toy nonnegative polynomial has an indefinite holomorphic Gram matrix.
    mutations['invalid_holomorphic_SOS'] = reject(lambda: core.psd([[C(1),ZERO,ZERO],
                                         [ZERO,C(-2),ZERO],[ZERO,ZERO,C(1)]]), 'Indefinite Gram accepted')
    result['negative_controls'] = mutations
    result['pinned_dependencies'] = pinned
    files = sorted(p for p in HERE.iterdir() if p.suffix in ('.py', '.json', '.md') and p.name != 'results.json')
    files += [ROOT/'notes'/name for name in ('w-state-optimal-design-2026-09-26.md',
              'integral-rate-certificates-2026-09-26.md', 'reusable-response-certificates-2026-09-26.md')]
    result['source_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

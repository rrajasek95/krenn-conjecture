#!/usr/bin/env python3
"""Propose two-quality certificates; exact validation precedes exclusive write.

Requires NumPy and SciPy for discovery only. No guarantee of finding a witness
at a nonsmooth dual optimum; failure is not an impossibility certificate.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from shared import C, Q, core
import quality


def numeric(matrix):
    return np.array([[complex(float(z.re), float(z.im)) for z in row] for row in matrix])


def find(payload):
    work = deepcopy(payload)
    for q in work['qualities']:
        shift = Q(1, 10**10)*(1 if q['sense'] == 'min' else -1)
        q['threshold'] = str(Q(q['threshold'])+shift)
    data, matrices, _ = quality.problem(work)
    K, matrices = numeric(data['K']), [numeric(m) for m in matrices]

    def objective(mu):
        eig, vec = np.linalg.eigh(K+sum(x*m for x, m in zip(mu, matrices)))
        v = vec[:, -1]
        return eig[-1], np.array([(v.conj()@m@v).real for m in matrices])

    result = minimize(objective, np.ones(len(matrices)), jac=True, method='L-BFGS-B',
                      bounds=[(0, None)]*len(matrices),
                      options=dict(ftol=1e-15, gtol=1e-13, maxiter=3000, maxls=60))
    # A small direct constrained refinement corrects optimizer tolerances.
    _, vecs = np.linalg.eigh(K+sum(x*m for x, m in zip(result.x, matrices)))
    v = vecs[:, -1]
    def unpack(x):
        return x[:45]+1j*x[45:]
    def quadratic(m, x):
        z = unpack(x)
        return (z.conj()@m@z).real
    constraints = [dict(type='eq', fun=lambda x: np.dot(x, x)-1)]
    constraints += [dict(type='ineq', fun=lambda x, m=m: quadratic(m, x)) for m in matrices]
    primal = minimize(lambda x: -quadratic(K, x), np.r_[v.real, v.imag],
                      method='SLSQP', constraints=constraints,
                      options=dict(ftol=1e-14, maxiter=1000))
    v = unpack(primal.x)
    # At an eigenvalue crossing the dual gradient need not exist. Recover
    # candidate multipliers from stationarity of the actual primal vector;
    # retain them only when they improve the numerical upper bound.
    columns = np.column_stack([m@v for m in matrices]+[-v])
    rhs = -K@v
    fit = np.linalg.lstsq(np.r_[columns.real, columns.imag], np.r_[rhs.real, rhs.imag], rcond=None)[0]
    proposed = fit[:-1]
    best_mu = result.x
    if np.all(proposed >= 0) and objective(proposed)[0] < objective(best_mu)[0]:
        best_mu = proposed
    multipliers = [Q(round(float(x)*10**10), 10**10) for x in best_mu]
    _, original, _ = quality.problem(payload)
    upper_float = np.linalg.eigvalsh(K+sum(float(mu)*numeric(m)
                                         for mu, m in zip(multipliers, original)))[-1]
    upper = Q(int(np.ceil(upper_float*10**12))+100, 10**12)
    witness = [core.encode(C(Q(round(z.real*10**12), 10**12),
                             Q(round(z.imag*10**12), 10**12))) for z in v]
    out = {**payload, 'multipliers': list(map(str, multipliers)),
           'upper_eigenvalue': str(upper), 'witness': witness}
    return out, quality.verify(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('problem', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out, receipt = find(json.loads(args.problem.read_text()))
    with args.output.open('x') as handle:
        json.dump(out, handle, indent=2)
        handle.write('\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()

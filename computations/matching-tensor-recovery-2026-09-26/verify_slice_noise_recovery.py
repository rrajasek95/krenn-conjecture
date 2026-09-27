#!/usr/bin/env python3
"""Replay noisy-direction certificates without floating-point solvers.

Rebuilds exterior entries and planted matching tensors separately. Exact
bound acceptance is shared with slice_noise_recovery.certify; this is a
replay with independent assembly, not an independent implementation of
every inequality in the proof.
"""

import copy
from fractions import Fraction as F
import itertools
import json
import math
from pathlib import Path

import numpy as np
from flint import fmpz_mat

from audit_pair_observation import moments
from blind_mean_search import scalar_bound
import slice_noise_recovery as noise


def direct_slices(tensor):
    tail = tensor.ndim-1
    size = 3**tail
    choices = np.asarray(list(itertools.product([0, 1], repeat=tail)))
    other_coordinates = np.array([[1, 2], [0, 2], [0, 1]])
    sign_table = np.array([[0, 1, -1], [-1, 0, 1], [1, -1, 0]])
    powers = 3**np.arange(tail-1, -1, -1)
    result = []
    for a in range(3):
        matrix = np.zeros((size, size), dtype=np.int64)
        flat = tensor[a].reshape(-1)
        for row, word in enumerate(itertools.product(range(3), repeat=tail)):
            left = np.asarray(word)
            right = other_coordinates[left, choices]
            third = 3-left-right
            sign = np.prod(sign_table[left, right], axis=1)
            matrix[row, right@powers] = sign*flat[third@powers]
        assert np.array_equal(matrix, matrix.T)
        result.append(matrix)
    return result


def matching_source_check(case):
    n, comparison = case['sites'], case['test_comparison_only']
    # Means are scaled by 3 and edges by 9, making the whole tensor scale by 3^n.
    means = [[3, 0, 0]] + [[0, 0, 0] for _ in range(n-1)]
    edges = {e: [[0]*3 for _ in range(3)] for e in itertools.combinations(range(n), 2)}
    for k, rotation in enumerate(comparison['pair_rotation_numerators']):
        rotation = np.asarray(rotation, dtype=np.int64)
        assert np.array_equal(rotation.T@rotation, 9*np.eye(3, dtype=np.int64))
        i, j = 2*k+1, 2*k+2
        vector = rotation[:, 0]
        means[i] = means[j] = vector.tolist()
        edges[i, j] = (9*np.eye(3, dtype=np.int64)-np.outer(vector, vector)).tolist()
        for site in [i, j]:
            edges[0, site][1] = (3*3**k*rotation[:, 1]).tolist()
            edges[0, site][2] = (3*rotation[:, 2]).tolist()
    bound = scalar_bound(means, edges)
    values = moments(means, edges, 2*bound+1)
    values = [x if x <= bound else x-2*bound-1 for x in values]
    clean = comparison['clean_tensor_numerator']
    assert values == [3**n//9*x for x in clean]
    observed = case['observed_numerator']
    denominator = case['observed_denominator']
    errors = [F(y, denominator)-F(x, 9) for x, y in zip(clean, observed)]
    assert errors == [F(x, comparison['noise_denominator']) for x in comparison['noise_numerators']]
    assert sum(x*x for x in errors) <= F(case['epsilon'])**2
    expected = comparison['expected_mean_lines']
    assert all(all(a*e[0] == e[j]*row[0] for j, a in enumerate(row))
               for row, e in zip(means, expected))


def augmented_gram_check(case):
    """Build the actual stacked matrix and its Gram in a separate expression."""
    proposal, certificate = case['proposal'], case['certificate']
    a, scale = noise.decode(proposal['A'])
    b, _ = noise.decode(proposal['B'])
    z, _ = noise.decode(proposal['tail_vector'])
    p, _ = noise.decode(proposal['preconditioner'])
    a, b, p = fmpz_mat(a), fmpz_mat(b), fmpz_mat(p)
    c = a*b-b*a
    ca = c*a
    stack = fmpz_mat((c*scale).tolist()+ca.tolist())
    z = fmpz_mat([[x] for x in z[0]])
    z_squared = int((z.transpose()*z)[0, 0])
    gram = (stack.transpose()*stack)*z_squared + (z*z.transpose())*scale**6
    transformed = p.transpose()*gram*p
    target = z_squared*scale**8
    squared = sum((int(transformed[i, j])-(target if i == j else 0))**2
                  for i in range(a.nrows()) for j in range(a.nrows()))
    assert str(squared) == certificate['gram_residual_frobenius_squared']
    upper = int(certificate['gram_residual_frobenius_upper'])
    assert upper*upper >= squared and upper < target


def direction_comparison(case):
    comparison, certificate = case['test_comparison_only'], case['certificate']
    tails, _ = noise.decode(case['proposal']['tail_lines'])
    lines = [[F(x) for x in certificate['first_line_estimate']]] + tails
    squared = []
    for expected, recovered, bound in zip(comparison['expected_mean_lines'], lines,
                                         certificate['local_mean_line_sine_bounds']):
        # Cross-product formula, separate from the generator's dot-product identity.
        numerator = sum((expected[i]*recovered[j]-expected[j]*recovered[i])**2
                        for i, j in itertools.combinations(range(3), 2))
        value = F(numerator, sum(x*x for x in expected)*sum(x*x for x in recovered))
        assert value <= F(bound)**2
        squared.append(str(value))
    assert squared == comparison['actual_line_sine_squared']


def reject_bad_proposals(case):
    n = case['sites']
    observed = np.asarray(case['observed_numerator'], dtype=np.int64).reshape((3,)*n)
    denominator = case['observed_denominator']
    rejected = []
    for field in ['inverse', 'preconditioner']:
        bad = copy.deepcopy(case['proposal'])
        rows, scale = noise.decode(bad[field])
        bad[field] = noise.encode([[0 for _ in row] for row in rows], scale)
        try:
            noise.certify(observed, denominator, F(case['epsilon']), bad, direct_slices)
        except AssertionError:
            rejected.append(field)
        else:
            raise AssertionError(f'Invalid {field} was accepted')
    try:
        noise.certify(observed, denominator, F(1), case['proposal'], direct_slices)
    except AssertionError:
        rejected.append('excessive_error_budget')
    else:
        raise AssertionError('This excessive noise budget was accepted')
    return rejected


def run():
    data = json.loads(Path(__file__).with_name('slice-noise-recovery-certificate.json').read_text())

    def forbidden(*args, **kwargs):
        raise AssertionError('Replay attempted a floating-point proposal')

    noise.propose = noise.eigh = noise.solve = noise.svd = forbidden
    reports = []
    for case in data['cases']:
        n = case['sites']
        observed = np.asarray(case['observed_numerator'], dtype=np.int64).reshape((3,)*n)
        rebuilt = noise.certify(observed, case['observed_denominator'], F(case['epsilon']),
                                case['proposal'], direct_slices)
        assert rebuilt == case['certificate']
        matching_source_check(case)
        augmented_gram_check(case)
        direction_comparison(case)
        reports.append({'sites': n, 'all_exterior_entries_rebuilt_separately': True,
                        'clean_tensor_checked_by_scalar_matching_sums': True,
                        'actual_noise_norm_checked_exactly': True,
                        'augmented_gram_rebuilt_from_stacked_operator': True,
                        'exact_bounds_replayed_without_numerical_solvers': True,
                        'actual_local_line_errors_checked_exactly': True})
    return {'cases': reports, 'invalid_proposals_rejected': reject_bad_proposals(data['cases'][0]),
            'scope': 'Independent tensor/matrix assembly and exact acceptance replay; shares the bound-acceptance function and integer matrix library with the generator.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))

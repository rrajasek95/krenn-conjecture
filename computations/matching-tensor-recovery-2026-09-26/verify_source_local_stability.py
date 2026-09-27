#!/usr/bin/env python3
"""Replay saved source-stability witnesses without numerical eigensolvers.

All accepted inequalities use integers or fractions. A separate scalar,
per-word matching recurrence checks every forward and Jacobian entry.
"""

import base64
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import itertools
import json
import math
from pathlib import Path
import zlib

import numpy as np
from flint import fmpz_mat, nmod_mat

from audit_pair_observation import moments
from blind_mean_search import scalar_bound
import source_local_stability as source


def check_jacobian(means, edges, tensor, jacobian, keys):
    """Use scalar matching sums, independently of the tensor recurrence."""
    n = len(means)
    absolute_bound = scalar_bound(means, edges)
    modulus = 2 * absolute_bound + 1

    @lru_cache(None)
    def complement(sites):
        local_means = [means[i] for i in sites]
        local_edges = {(a, b): edges[i, j]
                       for a, i in enumerate(sites)
                       for b, j in enumerate(sites) if a < b}
        values = moments(local_means, local_edges, modulus)
        return np.asarray([x if x <= absolute_bound else x - modulus
                           for x in values], dtype=np.int64).reshape((3,) * len(sites))

    assert np.array_equal(tensor, complement(tuple(range(n))).reshape(-1))
    for column, key in enumerate(keys):
        sites, colours = ((key[1:2], key[2:3]) if key[0] == 'mu'
                          else (key[1:3], key[3:5]))
        expected = np.zeros((3,) * n, dtype=np.int64)
        index = [slice(None)] * n
        for i, a in zip(sites, colours):
            index[i] = a
        expected[tuple(index)] = complement(tuple(i for i in range(n) if i not in sites))
        assert np.array_equal(expected.reshape(-1), jacobian[:, column])


def check_witness(gram, certificate, mean_count):
    size = len(gram)
    assert certificate['dimension'] == size
    assert certificate['mean_parameters'] == mean_count
    assert certificate['covariance_parameters'] == size - mean_count
    encoded = certificate['preconditioner']
    assert encoded['encoding'] == 'zlib+base64; little-endian signed int64; row-major'
    packed = zlib.decompress(base64.b64decode(encoded['data']))
    assert len(packed) == 8 * size * size
    assert hashlib.sha256(packed).hexdigest() == encoded['sha256']
    witness = np.frombuffer(packed, dtype='<i8').reshape(size, size).tolist()
    matrix = fmpz_mat(witness)
    denominator = int(encoded['scale'])
    assert denominator > 0
    exact = matrix.transpose() * fmpz_mat(gram.tolist()) * matrix
    residual_squared = sum((int(exact[i, j]) - (denominator**2 if i == j else 0))**2
                           for i in range(size) for j in range(size))
    residual_upper = int(certificate['residual_frobenius_upper'])
    assert str(residual_squared) == certificate['residual_frobenius_squared']
    assert residual_upper >= 0 and residual_upper**2 >= residual_squared
    alpha = denominator**2 - residual_upper
    assert alpha > 0
    mean_squared = sum(x*x for row in witness[:mean_count] for x in row)
    covariance_squared = sum(x*x for row in witness[mean_count:] for x in row)
    for name, numerator in [('full', mean_squared + covariance_squared),
                            ('mean', mean_squared), ('covariance', covariance_squared)]:
        assert F(certificate[name + '_inverse_squared_bound']) == F(numerator, alpha)
    assert certificate['gram_determinant_prime'] == source.PRIME
    determinant = int(nmod_mat(gram.tolist(), source.PRIME).det())
    assert determinant != 0 and determinant == certificate['gram_determinant_residue']
    assert certificate['exact_residual_inequality_verified'] is True


def independent_curvature(means, edges):
    """Build the positive majorant from every matching, not the recurrence."""
    n = len(means)
    monomers = [max(map(abs, row)) + 1 for row in means]
    pairs = {edge: max(abs(x) for row in block for x in row) + 1
             for edge, block in edges.items()}

    @lru_cache(None)
    def matching_value(sites):
        # A subset of edges is a matching exactly when its endpoints are distinct.
        total = 0
        available = list(itertools.combinations(sites, 2))
        for count in range(len(sites)//2 + 1):
            for matching in itertools.combinations(available, count):
                used = [i for edge in matching for i in edge]
                if len(set(used)) != 2 * count:
                    continue
                total += (math.prod(pairs[e] for e in matching)
                          * math.prod(monomers[i] for i in sites if i not in used))
        return total

    # Coordinate multiplicities are derived from the free-parameter list.
    supports = [frozenset([i]) for i in range(n) for _ in range(3)]
    supports += [frozenset([i, j]) for i, j in edges for a in range(3) for b in range(3)
                 if not (i == 0 and a == b == 0)]
    multiplicities = {}
    for first in supports:
        for second in supports:
            if first.isdisjoint(second):
                rest = tuple(i for i in range(n) if i not in first | second)
                multiplicities[rest] = multiplicities.get(rest, 0) + 1
    return sum(count * 3**len(rest) * matching_value(rest)**2
               for rest, count in multiplicities.items())


def verify_case(case):
    n, count = case['sites'], case['outputs']
    means = case['source_means']
    assert len(means) == count and all(len(mu) == n for mu in means)
    edges = {tuple(e['sites']): e['weights'] for e in case['source_edges']}
    assert list(edges) == list(itertools.combinations(range(n), 2))
    assert case['fixed_covariance_entries'] == [[0, j, 0, 0, edges[0, j][0][0]]
                                               for j in range(1, n)]
    jacobians, grams = [], []
    for index, mu in enumerate(means):
        tensor, jacobian, keys = source.source_jacobian(mu, edges)
        check_jacobian(mu, edges, tensor, jacobian, keys)
        assert hashlib.sha256(json.dumps(tensor.tolist()).encode()).hexdigest() == case['tensor_hashes'][index]
        gram = source.exact_gram(jacobian)
        check_witness(gram, case['individual_certificates'][index], 3*n)
        jacobians.append(jacobian)
        grams.append(gram)
    q = 9*n*(n-1)//2 - (n-1)
    assert case['per_output_parameter_count'] == 3*n + q
    assert case['joint_parameter_count'] == 3*n*count + q
    joint = np.zeros((count*3**n, 3*n*count + q), dtype=np.int64)
    for j, matrix in enumerate(jacobians):
        joint[j*3**n:(j+1)*3**n, j*3*n:(j+1)*3*n] = matrix[:, :3*n]
        joint[j*3**n:(j+1)*3**n, 3*n*count:] = matrix[:, 3*n:]
    joint_gram = source.exact_gram(joint)
    # Audit every block against the separate-output formula, including zeros.
    expected = np.zeros_like(joint_gram)
    for j, gram in enumerate(grams):
        mean_slice = slice(j*3*n, (j+1)*3*n)
        expected[mean_slice, mean_slice] = gram[:3*n, :3*n]
        expected[mean_slice, 3*n*count:] = gram[:3*n, 3*n:]
        expected[3*n*count:, mean_slice] = gram[3*n:, :3*n]
        expected[3*n*count:, 3*n*count:] += gram[3*n:, 3*n:]
    assert np.array_equal(expected, joint_gram)
    if count > 1:
        joint_certificate = case['joint_certificate']
        check_witness(joint_gram, joint_certificate, 3*n*count)
    else:
        assert case['joint_certificate'] == {'reference': 'individual_certificates[0]'}
        joint_certificate = case['individual_certificates'][0]
    individual_bounds = [F(c['covariance_inverse_squared_bound'])
                         for c in case['individual_certificates']]
    harmonic = 1 / sum(1/x for x in individual_bounds)
    assert harmonic == F(case['shared_covariance_inverse_squared_bound'])
    if count > 1:
        assert harmonic < min(individual_bounds)
    curvature = sum(independent_curvature(mu, edges) for mu in means)
    bounds = case['finite_noise_bounds']
    assert int(bounds['curvature_squared_bound_on_unit_ball']) == curvature
    assert source.finite_noise_bounds(joint_certificate, curvature) == bounds
    assert source.mean_span_certificate(means, bounds) == case['mean_span']
    return {'sites': n, 'outputs': count, 'parameters': len(joint_gram),
            'all_forward_and_jacobian_entries_independently_checked': True,
            'preconditioner_witnesses_verified_using_integer_arithmetic': True,
            'curvature_bound_independently_checked_by_matching_enumeration': True,
            'finite_noise_and_observed_span_bounds_verified': True,
            'floating_point_estimates_used_for_acceptance': False}


def run():
    path = Path(__file__).with_name('source-local-stability-certificate.json')
    certificate = json.loads(path.read_text())
    return {'certificate': path.name, 'cases': [verify_case(c) for c in certificate['cases']]}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))

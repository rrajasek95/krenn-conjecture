#!/usr/bin/env python3
"""Exact replay of product-measurement local and secant certificates."""

from functools import lru_cache
import hashlib
import json
from pathlib import Path

import numpy as np
from flint import nmod_mat

import product_measurements as product
import source_local_stability as stability
from verify_source_local_stability import check_witness


def independent_curvature(means, edges, probes):
    n = len(means)
    supports = [frozenset(k[1:2] if k[0] == 'mu' else k[1:3])
                for k in product.parameter_keys(n)]
    coefficients = {}
    for first in supports:
        for second in supports:
            if first.isdisjoint(second):
                mask = sum(1 << i for i in range(n) if i not in first | second)
                coefficients[mask] = coefficients.get(mask, 0) + 1
    total = 0
    for probe in probes:
        monomers = [abs(sum(x*y for x, y in zip(mu, u))) + 2
                    for mu, u in zip(means, probe)]
        pairs = {(i, j): abs(sum(probe[i][a]*block[a][b]*probe[j][b]
                                 for a in range(3) for b in range(3))) + 3
                 for (i, j), block in edges.items()}

        @lru_cache(None)
        def majorant(mask):
            if not mask:
                return 1
            i = mask.bit_length() - 1
            rest = mask ^ (1 << i)
            value = monomers[i] * majorant(rest)
            for j in range(i):
                if rest & (1 << j):
                    value += pairs[j, i] * majorant(rest ^ (1 << j))
            return value

        total += sum(coefficient * majorant(mask)**2 for mask, coefficient in coefficients.items())
    return total


def verify_case(case):
    n, d = case['sites'], case['parameter_dimension']
    means = case['source_means']
    edges = {tuple(e['sites']): e['weights'] for e in case['source_edges']}
    codes = case['probe_codes']
    assert len(codes) == len(set(codes)) == 2*d
    assert all(0 <= code < 4**n for code in codes)
    probes = [[[1, 1 if code & (1 << (2*i)) else -1,
                1 if code & (1 << (2*i+1)) else -1] for i in range(n)] for code in codes]
    data, jacobian, bound = product.forward_jacobian(means, edges, probes)
    product.scalar_audit(means, edges, probes, data, jacobian)
    assert d == 3*n + 9*n*(n-1)//2 - (n-1)
    assert case['full_tensor_entries'] == 3**n and case['measurements'] == 2*d
    assert case['local_dimension'] == 3
    assert data.tolist() == case['measurement_values']
    assert str(bound) == case['integer_subset_moment_absolute_bound']
    assert hashlib.sha256(json.dumps(jacobian.tolist()).encode()).hexdigest() == case['jacobian_sha256']
    assert [c['measurements'] for c in case['rank_certificates']] == [d, d+1, 2*d]
    for certificate in case['rank_certificates']:
        rows = certificate['rows']
        assert len(rows) == len(set(rows)) == certificate['rank'] == d
        assert all(0 <= i < certificate['measurements'] for i in rows)
        assert certificate['prime'] == stability.PRIME
        value = int(nmod_mat(jacobian[rows].tolist(), stability.PRIME).det())
        assert value != 0 and value == certificate['minor_determinant']
    gram = product.gram_exact(jacobian)
    check_witness(gram, case['conditioning_certificate'], 3*n)
    curvature = independent_curvature(means, edges, probes)
    assert stability.finite_noise_bounds(case['conditioning_certificate'], curvature) == case['finite_noise_bounds']
    witness = case['secant_dimension_witness']
    second_means = witness['second_source_means']
    second_edges = {tuple(e['sites']): e['weights'] for e in witness['second_source_edges']}
    second_data, second_jacobian, _ = product.forward_jacobian(second_means, second_edges, probes)
    product.scalar_audit(second_means, second_edges, probes, second_data, second_jacobian)
    difference = np.concatenate([jacobian, -second_jacobian], axis=1)
    determinant = int(nmod_mat(difference.tolist(), stability.PRIME).det())
    assert witness['difference_jacobian_dimension'] == 2*d
    assert witness['prime'] == stability.PRIME
    assert determinant != 0 and determinant == witness['difference_jacobian_determinant']
    assert case['global_injectivity_of_saved_probe_list_certified'] is False
    return {'sites': n, 'parameters': d, 'probes': 2*d,
            'minimum_measurement_local_rank_verified': d,
            'difference_variety_dimension_verified': 2*d,
            'all_scalar_values_and_jacobian_entries_independently_checked': True,
            'conditioning_and_curvature_witnesses_verified_exactly': True,
            'full_tensor_constructed_in_this_replay': False,
            'global_injectivity_of_saved_probe_list_certified': False}


def run():
    certificate = json.loads(Path(__file__).with_name('product-measurement-certificate.json').read_text())
    return {'cases': [verify_case(c) for c in certificate['cases']],
            'numerical_estimates_used_for_acceptance': False}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))

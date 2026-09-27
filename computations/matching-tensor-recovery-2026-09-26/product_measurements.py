#!/usr/bin/env python3
"""Local certificates using products of local scalar measurements.

The forward map and its Jacobian do not build the full tensor. These
supplied-point certificates do not prove global uniqueness of the saved
finite probe lists. The generic measurement theorem is proved separately.
"""

from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import random

import numpy as np
from flint import fmpz_mat, nmod_mat

from blind_mean_search import scalar_bound
from restricted_source_inverse import serialize_edges
import source_local_stability as stability
from two_direction import pivot_columns
from verify_source_local_stability import check_witness


def parameter_keys(n):
    return ([('mu', i, a) for i in range(n) for a in range(3)]
            + [('R', i, j, a, b) for i, j in itertools.combinations(range(n), 2)
               for a in range(3) for b in range(3)
               if not (i == 0 and a == b == 0)])


def projected_parameters(means, edges, probes):
    u = np.asarray(probes, dtype=np.int64)
    monomers = np.sum(u * np.asarray(means)[None], axis=2)
    pairs = {(i, j): np.sum((u[:, i] @ np.asarray(block)) * u[:, j], axis=1)
             for (i, j), block in edges.items()}
    return u, monomers, pairs


def subset_moments(monomers, pairs):
    n = monomers.shape[1]
    bound = scalar_bound([[int(max(abs(monomers[:, i])))] for i in range(n)],
                         {e: [[int(max(abs(v)))]] for e, v in pairs.items()})
    assert bound < 2**63

    @lru_cache(None)
    def evaluate(sites):
        if not sites:
            return np.ones(len(monomers), dtype=np.int64)
        i, *rest = sites
        value = monomers[:, i] * evaluate(tuple(rest))
        for j in rest:
            value = value + pairs[i, j] * evaluate(tuple(k for k in rest if k != j))
        return value

    return evaluate, bound


def forward_jacobian(means, edges, probes):
    n = len(means)
    u, monomers, pairs = projected_parameters(means, edges, probes)
    evaluate, bound = subset_moments(monomers, pairs)
    keys = parameter_keys(n)
    # The stored probes have entries +/-1, so insertion factors cannot grow.
    assert np.all(abs(u) == 1)
    jacobian = np.empty((len(probes), len(keys)), dtype=np.int64)
    for column, key in enumerate(keys):
        if key[0] == 'mu':
            _, i, a = key
            sites, coefficient = (i,), u[:, i, a]
        else:
            _, i, j, a, b = key
            sites, coefficient = (i, j), u[:, i, a] * u[:, j, b]
        jacobian[:, column] = coefficient * evaluate(tuple(i for i in range(n) if i not in sites))
    return evaluate(tuple(range(n))), jacobian, bound


def scalar_audit(means, edges, probes, data, jacobian):
    """Independent Python-integer recurrence, with one probe at a time."""
    n = len(means)
    keys = parameter_keys(n)
    for row, probe in enumerate(probes):
        monomers = [sum(x*y for x, y in zip(mu, u)) for mu, u in zip(means, probe)]
        pairs = {(i, j): sum(probe[i][a]*block[a][b]*probe[j][b]
                             for a in range(3) for b in range(3))
                 for (i, j), block in edges.items()}

        @lru_cache(None)
        def moment(mask):
            if mask == 0:
                return 1
            i = mask.bit_length() - 1
            rest = mask ^ (1 << i)
            value = monomers[i] * moment(rest)
            for j in range(i):
                if rest & (1 << j):
                    value += pairs[j, i] * moment(rest ^ (1 << j))
            return value

        full = (1 << n) - 1
        assert moment(full) == int(data[row])
        for column, key in enumerate(keys):
            if key[0] == 'mu':
                _, i, a = key
                value = probe[i][a] * moment(full ^ (1 << i))
            else:
                _, i, j, a, b = key
                value = probe[i][a]*probe[j][b]*moment(full ^ (1 << i) ^ (1 << j))
            assert value == int(jacobian[row, column])


def curvature_squared(means, edges, probes):
    """Matching majorant for the measured map on the unit parameter ball."""
    n = len(means)
    u, monomers, pairs = projected_parameters(means, edges, probes)
    assert np.all(abs(u) == 1)
    # Squared insertion weights: 3 per mean, 8 or 9 per free edge block.
    # Integer upper bounds for their square roots are respectively 2 and 3.
    majorant, _ = subset_moments(abs(monomers) + 2,
                                 {e: abs(v) + 3 for e, v in pairs.items()})
    total = 0
    for removed_count in [2, 3, 4]:
        for removed in itertools.combinations(range(n), removed_count):
            if removed_count == 2:
                weight = 18
            elif removed_count == 3:
                weight = 150 if 0 in removed else 162
            else:
                weight = 432 if 0 in removed else 486
            values = majorant(tuple(i for i in range(n) if i not in removed))
            total += weight * sum(int(v)**2 for v in values)
    return total


def gram_exact(jacobian):
    if jacobian.shape[0]*int(np.max(abs(jacobian)))**2 < 2**63:
        return stability.exact_gram(jacobian)
    matrix = fmpz_mat(jacobian.tolist())
    return np.asarray((matrix.transpose()*matrix).tolist(), dtype=object)


def rank_certificate(jacobian):
    matrix = nmod_mat(jacobian.tolist(), stability.PRIME)
    rows = pivot_columns(matrix.transpose())
    assert len(rows) == jacobian.shape[1]
    minor = nmod_mat(jacobian[rows].tolist(), stability.PRIME)
    determinant = int(minor.det())
    assert determinant
    return {'measurements': len(jacobian), 'rank': len(rows), 'rows': rows,
            'prime': stability.PRIME, 'minor_determinant': determinant}


def tensor_contraction_audit(means, edges, probes, data, jacobian):
    """Full tensors are used only in this separate seven/nine-site audit."""
    n = len(means)
    tensor, full_jacobian, _ = stability.source_jacobian(means, edges)
    for row in [0, 1, len(probes)//2, len(probes)-1]:
        weights = np.array([1], dtype=np.int64)
        for local in probes[row]:
            weights = np.kron(weights, local)
        assert 3**n * max(int(max(abs(tensor))), int(np.max(abs(full_jacobian)))) < 2**63
        assert int(weights @ tensor) == int(data[row])
        assert np.array_equal(weights @ full_jacobian, jacobian[row])


def run_case(n):
    source_path = Path(__file__).with_name('source-local-stability-certificate.json')
    saved = {c['sites']: c for c in json.loads(source_path.read_text())['cases']}
    rng = random.Random(272100 + n)
    if n in saved:
        means = saved[n]['source_means'][0]
        edges = {tuple(e['sites']): e['weights'] for e in saved[n]['source_edges']}
    else:
        choices = [-2, -1, 1, 2]
        means = [[rng.choice(choices) for _ in range(3)] for _ in range(n)]
        edges = {e: [[rng.choice(choices) for _ in range(3)] for _ in range(3)]
                 for e in itertools.combinations(range(n), 2)}
    d = len(parameter_keys(n))
    codes = rng.sample(range(4**n), 2*d)
    probes = [[[1, 1 if (code >> (2*i)) & 1 else -1,
                1 if (code >> (2*i+1)) & 1 else -1] for i in range(n)] for code in codes]
    data, jacobian, bound = forward_jacobian(means, edges, probes)
    scalar_audit(means, edges, probes, data, jacobian)
    if n <= 9:
        tensor_contraction_audit(means, edges, probes, data, jacobian)
    ranks = [rank_certificate(jacobian[:k]) for k in [d, d+1, 2*d]]
    gram = gram_exact(jacobian)
    certificate = stability.conditioning_certificate(gram, 3*n)
    check_witness(gram, certificate, 3*n)
    curvature = curvature_squared(means, edges, probes)
    choices = [-2, -1, 1, 2]
    second_means = [[rng.choice(choices) for _ in range(3)] for _ in range(n)]
    second_edges = {e: [[rng.choice(choices) for _ in range(3)] for _ in range(3)] for e in edges}
    second_data, second_jacobian, _ = forward_jacobian(second_means, second_edges, probes)
    scalar_audit(second_means, second_edges, probes, second_data, second_jacobian)
    difference_jacobian = np.concatenate([jacobian, -second_jacobian], axis=1)
    secant_determinant = int(nmod_mat(difference_jacobian.tolist(), stability.PRIME).det())
    assert secant_determinant
    return {'sites': n, 'local_dimension': 3, 'parameter_dimension': d,
            'full_tensor_entries': 3**n, 'measurements': len(probes),
            'source_means': means, 'source_edges': serialize_edges(edges),
            'probe_encoding': 'Local row i is (1, sign(bit 2i), sign(bit 2i+1)), where sign(0)=-1 and sign(1)=1.',
            'probe_codes': codes, 'measurement_values': data.tolist(),
            'integer_subset_moment_absolute_bound': str(bound),
            'jacobian_sha256': hashlib.sha256(json.dumps(jacobian.tolist()).encode()).hexdigest(),
            'rank_certificates': ranks, 'conditioning_certificate': certificate,
            'finite_noise_bounds': stability.finite_noise_bounds(certificate, curvature),
            'secant_dimension_witness': {
                'second_source_means': second_means, 'second_source_edges': serialize_edges(second_edges),
                'difference_jacobian_dimension': 2*d, 'prime': stability.PRIME,
                'difference_jacobian_determinant': secant_determinant,
                'second_jacobian_independently_checked': True},
            'all_scalar_measurements_and_jacobian_entries_independently_checked': True,
            'selected_full_tensor_contractions_checked': n <= 9,
            'full_tensor_constructed_only_for_separate_audit': n <= 9,
            'global_injectivity_of_saved_probe_list_certified': False}


if __name__ == '__main__':
    print(json.dumps({'cases': [run_case(n) for n in [7, 9, 11]],
                      'scope': 'Supplied-point local rank and finite-noise certificates. No blind recovery or global injectivity certificate for these finite probe lists.'}, indent=2))

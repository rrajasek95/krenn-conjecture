#!/usr/bin/env python3
"""Audit the saved slice certificates with separate tensor and matrix assembly.

Default: all exact forward, rational-source, quotient, and small symbolic
checks; modular slice ranks through seven sites. --full also rebuilds and
checks the 6561-square slice operators of the retained nine-site example.
No source parameter is used to assemble the observable slice operators.
"""

import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np
import sympy as sp
from flint import nmod_mat

from audit_pair_observation import moments
from blind_mean_search import scalar_bound


def eps(a, b, c):
    return int((a, b, c) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]) - int(
        (a, b, c) in [(0, 2, 1), (2, 1, 0), (1, 0, 2)])


def integer_moments(means, edges):
    bound = scalar_bound(means, edges)
    modulus = 2*bound+1
    return [x if x <= bound else x-modulus for x in moments(means, edges, modulus)]


def pair_check(saved):
    words = list(itertools.product(range(3), repeat=2))

    def exterior(d):
        return sp.Matrix([[sum(eps(r, s, a)*eps(t, u, b)*d[a, b] for a, b in words)
                           for s, u in words] for r, t in words])

    h = sp.Matrix(saved['H'])
    a, b = sp.Matrix(saved['twice_A'])/2, sp.Matrix(saved['twice_B'])/2
    e, f = sp.zeros(3), sp.zeros(3)
    e[0, 1] = e[1, 0] = 1
    f[0, 2] = f[2, 0] = 1
    assert h == exterior(sp.eye(3)) and h.det() == saved['H_determinant'] == -2
    assert h*a == exterior(e) and h*b == exterior(f)
    c = a*b-b*a
    z = sp.Symbol('lambda')
    assert c.charpoly().as_expr() == sp.expand(z**3*(z*z+1)*(z*z+4)**2)
    assert c**5+5*c**3+4*c == sp.zeros(9)
    u = sp.Matrix(saved['commutator_kernel_basis'])
    assert u.rank() == 3 and c.rank() == 6 and c*u == sp.zeros(9, 3)
    images = c*a*u
    assert images == sp.Matrix(saved['CA_on_kernel_basis']) and images.rank() == 2
    assert images[:, 0] == sp.zeros(9, 1)
    rows, columns = saved['stack_minor_rows'], saved['stack_minor_columns']
    assert c.col_join(c*a)[rows, columns].det() == saved['stack_minor_determinant'] == 8


def quotient_check(tensor, lines):
    # Independent quotient equations, rather than the generator's exterior maps.
    value = tensor.astype(object)
    for row in lines:
        pivot = next(a for a, x in enumerate(row) if x)
        outside = [a for a in range(3) if a != pivot]
        q = np.zeros((2, 3), dtype=object)
        for k, a in enumerate(outside):
            q[k, a], q[k, pivot] = row[pivot], -row[a]
        value = np.tensordot(value, q.T, axes=(0, 0))
    assert all(x == 0 for x in value.reshape(-1))


def direct_slices(tensor, prime):
    tail, size = tensor.ndim-1, 3**(tensor.ndim-1)
    choices = np.array(list(itertools.product([0, 1], repeat=tail)), dtype=np.int64)
    complements = np.array([[1, 2], [0, 2], [0, 1]], dtype=np.int64)
    powers = 3**np.arange(tail-1, -1, -1)
    sign_table = np.array([[eps(a, b, 3-a-b) if a != b else 0 for b in range(3)]
                           for a in range(3)], dtype=np.int64)
    matrices = []
    for colour in range(3):
        dense = np.zeros((size, size), dtype=np.int64)
        values = tensor[colour].reshape(-1) % prime
        for index, word in enumerate(itertools.product(range(3), repeat=tail)):
            left = np.asarray(word)
            right = complements[left, choices]
            remaining = 3-left-right
            signs = np.prod(sign_table[left, right], axis=1)
            dense[index, right@powers] = signs*values[remaining@powers] % prime
        matrix = nmod_mat(dense.tolist(), prime)
        assert matrix == matrix.transpose()
        matrices.append(matrix)
    return matrices


def rank_check(tensor, lines, saved):
    prime = saved['prime']
    matrices = direct_slices(tensor, prime)
    reference = saved['reference_slice']
    for attempt in saved['slice_chart_attempts'][:-1]:
        try:
            matrices[attempt['reference']].inv()
        except ZeroDivisionError:
            continue
        raise AssertionError('An allegedly singular chart is invertible')
    inverse = matrices[reference].inv()
    other = [a for a in range(3) if a != reference]
    a, b = inverse*matrices[other[0]], inverse*matrices[other[1]]
    del inverse, matrices
    c = a*b-b*a
    basis, count = c.nullspace()
    assert count == saved['initial_commutator_nullity']
    k = nmod_mat([[int(basis[i, j]) for j in range(count)] for i in range(c.ncols())], prime)
    restriction = c*(a*k)
    assert restriction.rank() == count-1
    rows, columns = saved['restriction_minor_rows'], saved['restriction_minor_columns']
    minor = nmod_mat([[int(restriction[i, j]) for j in columns] for i in rows], prime)
    assert len(rows) == len(columns) == count-1
    assert int(minor.det()) == saved['restriction_minor_determinant'] != 0
    # Verify the recovered rational product without computing a new candidate.
    product = [math.prod(lines[i+1][x] for i, x in enumerate(word)) % prime
               for word in itertools.product(range(3), repeat=tensor.ndim-1)]
    vector = nmod_mat([[x] for x in product], prime)
    assert any(product) and lines[0][reference] % prime
    for operator, colour in [(a, other[0]), (b, other[1])]:
        assert (operator*vector)*lines[0][reference] == vector*lines[0][colour]


def three_site_check(case, saved):
    means = case['source_means']
    edges = {tuple(e['sites']): e['weights'] for e in case['source_edges']}
    words = list(itertools.product(range(3), repeat=3))
    columns = []
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        for a in range(3):
            columns.append([int(w[i] == a)*(means[j][w[j]]*means[k][w[k]]+edges[j, k][w[j]][w[k]])
                            for w in words])
    for i, j in edges:
        k = next(x for x in range(3) if x not in [i, j])
        for a, b in itertools.product(range(3), repeat=2):
            if i == 0 and a == b == 0:
                continue
            columns.append([int(w[i] == a and w[j] == b)*means[k][w[k]] for w in words])
    jacobian = sp.Matrix(columns).T
    assert jacobian.shape == (27, saved['gauge_fixed_parameter_count']) == (27, 34)
    minor = jacobian[saved['minor_rows'], saved['minor_columns']]
    assert minor.rows == minor.cols == saved['jacobian_rank'] == 25
    assert int(minor.det()) % saved['prime'] == saved['minor_determinant'] != 0
    # For fixed e0 lines, the edge-to-tensor map has exactly eight redundancies.
    phi_columns = []
    for i, j in itertools.combinations(range(3), 2):
        k = next(x for x in range(3) if x not in [i, j])
        for a, b in itertools.product(range(3), repeat=2):
            phi_columns.append([int(w[i] == a and w[j] == b and w[k] == 0) for w in words])
    assert sp.Matrix(phi_columns).rank() == 19


def rational_source_check(tensor, case):
    means = [[F(x) for x in row] for row in case['recovered_means']]
    edges = {tuple(e['sites']): [[F(x) for x in row] for row in e['weights']]
             for e in case['recovered_edges']}
    gains = [F(x) for x in case['comparison_site_gains']]
    assert math.prod(gains) == 1
    original = {tuple(e['sites']): e['weights'] for e in case['source_edges']}
    assert all(means[i][a] == gains[i]*case['source_means'][i][a]
               for i in range(len(means)) for a in range(3))
    assert all(edges[i, j][a][b] == gains[i]*gains[j]*original[i, j][a][b]
               for i, j in edges for a, b in itertools.product(range(3), repeat=2))
    denominator = math.lcm(*(x.denominator for row in means for x in row),
                           *(x.denominator for block in edges.values() for row in block for x in row))
    scaled_means = [[int(denominator*x) for x in row] for row in means]
    scaled_edges = {e: [[int(denominator**2*x) for x in row] for row in block]
                    for e, block in edges.items()}
    rebuilt = integer_moments(scaled_means, scaled_edges)
    assert rebuilt == [denominator**len(means)*int(x) for x in tensor.reshape(-1)]


def run(full=False):
    path = Path(__file__).with_name('slice-mean-recovery-certificate.json')
    certificate = json.loads(path.read_text())
    pair_check(certificate['pair_calculation'])
    three_site_check(certificate['cases'][0], certificate['three_site_dimension'])
    reports = []
    for case in certificate['cases']:
        n = case['sites']
        edges = {tuple(e['sites']): e['weights'] for e in case['source_edges']}
        flat = integer_moments(case['source_means'], edges)
        assert hashlib.sha256(json.dumps(flat).encode()).hexdigest() == case['tensor_sha256']
        tensor = np.asarray(flat, dtype=np.int64).reshape((3,)*n)
        lines = case['recovered_mean_lines']
        quotient_check(tensor, lines)
        if case['full_source_recovered']:
            rational_source_check(tensor, case)
        if n <= 7 or full:
            rank_check(tensor, lines, case['mean_recovery'])
        if case['paired_witness']:
            assert case['mean_recovery']['initial_commutator_nullity'] == 3**((n-1)//2)
        if case['retained_nonlinear_failure']:
            old = json.loads(path.with_name('blind-mean-search-certificate.json').read_text())
            retained = next(c for c in old['cases'] if c['sites'] == n and c['edge_scale'] == 30)
            assert retained['tensor_sha256'] == case['tensor_sha256']
            assert not retained['mean_search']['accepted']
        reports.append({'sites': n, 'paired_witness': case['paired_witness'],
                        'every_input_entry_rebuilt_independently': True,
                        'integer_quotient_equations_verified': True,
                        'rational_full_source_verified': case['full_source_recovered'],
                        'slice_ranks_rebuilt_independently': n <= 7 or full})
        print(f'Audited {n}-site case; paired={case["paired_witness"]}; ranks={n <= 7 or full}',
              file=sys.stderr, flush=True)
    return {'pair_lemma_verified_over_Q': True, 'three_site_dimension_minor_verified': True,
            'cases': reports, 'full_rank_replay': full}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action='store_true')
    arguments = parser.parse_args()
    print(json.dumps(run(arguments.full), indent=2))

#!/usr/bin/env python3
"""Blind exact mean-line recovery from three observable tensor slices.

The source is not supplied to recover_lines. A modular rank certificate
and an exact integer tensor-contraction check certify the rational answer.
The default replay includes the retained nine-site nonlinear-search failure.
Use --quick to omit that case (the dense matrices take several minutes).
"""

import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import sys
import time

import numpy as np
import sympy as sp
from flint import nmod_mat

import blind_mean_search as blind
from restricted_source_inverse import serialize_edges
from two_direction import pivot_columns

PRIME = 1000003


def epsilon(a, b, c):
    return 0 if len({a, b, c}) < 3 else (-1)**sum(x > y for x, y in itertools.combinations([a, b, c], 2))


def pair_calculation():
    words = list(itertools.product(range(3), repeat=2))

    def exterior(matrix):
        return sp.Matrix([[sum(matrix[c, d]*epsilon(a, x, c)*epsilon(b, y, d)
                               for c, d in words) for x, y in words] for a, b in words])

    e, f = sp.zeros(3), sp.zeros(3)
    e[0, 1] = e[1, 0] = 1
    f[0, 2] = f[2, 0] = 1
    h = exterior(sp.eye(3))
    a, b = h.inv()*exterior(e), h.inv()*exterior(f)
    c = a*b-b*a
    assert h.det() == -2 and c**5+5*c**3+4*c == sp.zeros(9)
    u = sp.zeros(9, 3)
    u[0, 0] = 1
    u[5, 1], u[7, 1] = -1, 1
    u[4, 2] = u[8, 2] = 1
    assert c*u == sp.zeros(9, 3) and c.rank() == 6
    images = c*a*u
    expected = sp.zeros(9, 3)
    expected[1, 1], expected[3, 1] = 1, -1
    expected[2, 2] = expected[6, 2] = 2
    assert images == expected
    rows = [1, 2, 3, 4, 5, 6, 10, 11]
    determinant = c.col_join(c*a)[rows, list(range(1, 9))].det()
    assert determinant == 8
    report = {'H': [[int(x) for x in row] for row in h.tolist()],
              'twice_A': [[int(x) for x in row] for row in (2*a).tolist()],
              'twice_B': [[int(x) for x in row] for row in (2*b).tolist()],
              'H_determinant': -2, 'commutator_characteristic_polynomial': str(sp.factor(c.charpoly().as_expr())),
              'squarefree_annihilator': 'z^5+5*z^3+4*z',
              'commutator_kernel_basis': [[int(x) for x in row] for row in u.tolist()],
              'CA_on_kernel_basis': [[int(x) for x in row] for row in images.tolist()],
              'stack_minor_rows': rows, 'stack_minor_columns': list(range(1, 9)),
              'stack_minor_determinant': int(determinant)}
    return report


def exterior_slices(tensor, prime):
    tail = tensor.ndim - 1
    size = 3**tail
    steps = np.asarray(list(itertools.product([1, 2], repeat=tail)), dtype=np.int64)
    signs = np.asarray([(-1)**sum(x == 2 for x in row) for row in steps], dtype=np.int64)
    powers = 3**np.arange(tail-1, -1, -1, dtype=np.int64)
    values = tensor.reshape(3, size) % prime
    result = []
    for s in range(3):
        rows = np.zeros((size, size), dtype=np.int64)
        for index, word in enumerate(itertools.product(range(3), repeat=tail)):
            word = np.asarray(word)
            columns = ((word+steps) % 3) @ powers
            coefficients = ((word-steps) % 3) @ powers
            rows[index, columns] = signs*values[s, coefficients] % prime
        matrix = nmod_mat(rows.tolist(), prime)
        # Independent Levi-Civita audit, including nonzero sparse positions.
        for row in [0, size//3, size//2, size-1]:
            left = [(row // int(p)) % 3 for p in powers]
            for offset in [0, len(steps)//2, len(steps)-1]:
                right = [(a+int(t)) % 3 for a, t in zip(left, steps[offset])]
                remaining = [3-a-b for a, b in zip(left, right)]
                column = sum(b*int(p) for b, p in zip(right, powers))
                entry = math.prod(epsilon(a, b, c) for a, b, c in zip(left, right, remaining))
                entry *= int(tensor[(s, *remaining)])
                assert int(matrix[row, column]) == entry % prime
            assert int(matrix[row, row]) == 0
        result.append(matrix)
    return result


def kernel(matrix, prime):
    vectors, count = matrix.nullspace()
    return nmod_mat([[int(vectors[i, j]) for j in range(count)]
                     for i in range(vectors.nrows())], prime)


def primitive(row):
    denominator = math.lcm(*(x.denominator for x in row))
    integers = [int(denominator*x) for x in row]
    divisor = math.gcd(*integers)
    if next(x for x in integers if x) < 0:
        divisor = -divisor
    return [x//divisor for x in integers]


def exact_product_check(tensor, lines, reference):
    """Use tensor contractions, independently of the exterior slice assembly."""
    maps = [np.asarray([[sum(epsilon(a, b, c)*row[b] for b in range(3))
                         for c in range(3)] for a in range(3)], dtype=object)
            for row in lines[1:]]
    values = []
    for a in range(3):
        values.append(blind.contract(tensor[a].astype(object), maps))
    for a in range(3):
        assert np.all(lines[0][reference]*values[a] == lines[0][a]*values[reference])


def recover_lines(tensor, prime=PRIME):
    """Input is an integer tensor only; outputs primitive rational mean lines."""
    assert tensor.ndim >= 3 and tensor.ndim % 2 and all(d == 3 for d in tensor.shape)
    assert np.issubdtype(tensor.dtype, np.integer)
    start = time.monotonic()
    slices = exterior_slices(tensor, prime)
    attempts = []
    for reference in range(3):
        try:
            inverse = slices[reference].inv()
        except ZeroDivisionError:
            attempts.append({'reference': reference, 'invertible': False})
            continue
        attempts.append({'reference': reference, 'invertible': True})
        break
    else:
        raise ValueError('No invertible coordinate slice; try a new local chart or a different prime')
    order = [reference] + [a for a in range(3) if a != reference]
    a, b = inverse*slices[order[1]], inverse*slices[order[2]]
    del inverse, slices
    commutator = a*b-b*a
    first = kernel(commutator, prime)
    restriction = commutator*(a*first)
    correction = kernel(restriction, prime)
    assert correction.ncols() == 1, 'The two-kernel criterion is not certified at this input and prime'
    common = first*correction
    av, bv = a*common, b*common
    vector = [int(common[i, 0]) for i in range(common.nrows())]
    pivot = next(i for i, value in enumerate(vector) if value)
    inverse_pivot = pow(vector[pivot], -1, prime)
    first_line = [0]*3
    first_line[reference] = 1
    first_line[order[1]] = int(av[pivot, 0])*inverse_pivot % prime
    first_line[order[2]] = int(bv[pivot, 0])*inverse_pivot % prime
    assert av == common*first_line[order[1]] and bv == common*first_line[order[2]]
    tail = tensor.ndim-1
    pivot_word = [(pivot//3**i) % 3 for i in reversed(range(tail))]
    modular_lines = [first_line]
    for i in range(tail):
        place = 3**(tail-1-i)
        modular_lines.append([vector[pivot+(colour-pivot_word[i])*place]*inverse_pivot % prime
                              for colour in range(3)])
    product = np.array([1], dtype=np.int64)
    for row in modular_lines[1:]:
        product = np.kron(product, row) % prime
    assert all(vector[i] == vector[pivot]*int(product[i]) % prime for i in range(len(vector)))
    lines = [primitive([blind.rational_reconstruct(x, prime) for x in row]) for row in modular_lines]
    exact_product_check(tensor, lines, reference)
    selected_columns = pivot_columns(restriction)
    selected = nmod_mat([[int(restriction[i, j]) for j in selected_columns]
                         for i in range(restriction.nrows())], prime)
    selected_rows = pivot_columns(selected.transpose())
    square = nmod_mat([[int(restriction[i, j]) for j in selected_columns] for i in selected_rows], prime)
    assert len(selected_columns) == first.ncols()-1 and int(square.det())
    report = {'prime': prime, 'slice_size': common.nrows(), 'slice_chart_attempts': attempts,
              'reference_slice': reference, 'initial_commutator_nullity': first.ncols(),
              'two_kernel_nullity': correction.ncols(),
              'restriction_minor_rows': selected_rows, 'restriction_minor_columns': selected_columns,
              'restriction_minor_determinant': int(square.det()),
              'common_eigenvector_and_tail_product_verified_mod_prime': True,
              'product_kernel_verified_over_integers': True,
              'global_mean_line_uniqueness_certified_for_matching_representations': True,
              'elapsed_seconds': time.monotonic()-start}
    return lines, report


def paired_source(m):
    n = 2*m+1
    means = [[1, 0, 0] for _ in range(n)]
    edges = {e: [[0]*3 for _ in range(3)] for e in itertools.combinations(range(n), 2)}
    for k in range(m):
        i, j = 2*k+1, 2*k+2
        edges[i, j][1][1] = edges[i, j][2][2] = 1
        for site in [i, j]:
            edges[0, site][1][1] = 3**k
            edges[0, site][2][2] = 1
    return means, edges


def paired_slice_check(m):
    """Check the witness slice formula before applying any exterior map."""
    means, edges = paired_source(m)
    tensor = blind.integer_tensor(means, edges).reshape(3, -1)
    identity = np.eye(3, dtype=np.int64).reshape(-1)
    e, f = np.zeros((3, 3), dtype=np.int64), np.zeros((3, 3), dtype=np.int64)
    e[0, 1] = e[1, 0] = f[0, 2] = f[2, 0] = 1

    def product(factors):
        result = np.array([1], dtype=np.int64)
        for factor in factors:
            result = np.kron(result, factor)
        return result

    expected = [product([identity]*m), np.zeros(9**m, dtype=np.int64),
                np.zeros(9**m, dtype=np.int64)]
    for k in range(m):
        for a, factor, coefficient in [(1, e, 3**k), (2, f, 1)]:
            factors = [identity]*m
            factors[k] = factor.reshape(-1)
            expected[a] += coefficient*product(factors)
    assert np.array_equal(tensor, expected)
    return {'pairs': m, 'every_slice_entry_matches_tensor_product_formula': True}


def three_site_dimension(case):
    """Record a nonzero source-Jacobian minor for the three-site corollary."""
    from source_local_stability import source_jacobian
    edges = {tuple(e['sites']): e['weights'] for e in case['source_edges']}
    _, jacobian, _ = source_jacobian(case['source_means'], edges)
    matrix = nmod_mat(jacobian.tolist(), PRIME)
    columns = pivot_columns(matrix)
    selected = nmod_mat([[int(matrix[i, j]) for j in columns] for i in range(27)], PRIME)
    rows = pivot_columns(selected.transpose())
    determinant = int(nmod_mat([[int(matrix[i, j]) for j in columns] for i in rows], PRIME).det())
    assert len(rows) == len(columns) == 25 and determinant
    return {'prime': PRIME, 'gauge_fixed_parameter_count': 34, 'jacobian_rank': 25,
            'minor_rows': rows, 'minor_columns': columns, 'minor_determinant': determinant,
            'generic_fiber_dimension_mod_site_gauge': 9}


def run_case(n, paired=False, retained_failure=False, full_inverse=False):
    if retained_failure:
        old = json.loads(Path(__file__).with_name('blind-mean-search-certificate.json').read_text())
        saved = next(c for c in old['cases'] if c['sites'] == n and c['edge_scale'] == 30)
        means = saved['source_means']
        edges = {tuple(e['sites']): e['weights'] for e in saved['source_edges']}
    elif paired:
        means, edges = paired_source((n-1)//2)
    else:
        rng = random.Random(273000+n)
        choices = [-2, -1, 1, 2]
        means = [[rng.choice(choices) for _ in range(3)] for _ in range(n)]
        edges = {e: [[rng.choice(choices) for _ in range(3)] for _ in range(3)]
                 for e in itertools.combinations(range(n), 2)}
    tensor = blind.integer_tensor(means, edges)
    digest = hashlib.sha256(json.dumps(tensor.reshape(-1).tolist()).encode()).hexdigest()
    if retained_failure:
        assert digest == saved['tensor_sha256'] and not saved['mean_search']['accepted']
    lines, report = recover_lines(tensor)
    if paired:
        assert report['initial_commutator_nullity'] == 3**((n-1)//2)
    assert all(lines[i][a]*means[i][b] == lines[i][b]*means[i][a]
               for i in range(n) for a in range(3) for b in range(3))
    result = {'sites': n, 'paired_witness': paired, 'retained_nonlinear_failure': retained_failure,
              'source_means': means, 'source_edges': serialize_edges(edges), 'tensor_sha256': digest,
              'recovered_mean_lines': lines, 'mean_recovery': report,
              'matches_planted_mean_lines': True, 'full_source_recovered': False}
    if full_inverse:
        rational_lines = [[F(x) for x in row] for row in lines]
        permutations = [[next(a for a, x in enumerate(row) if x)] for row in lines]
        permutations = [row+[a for a in range(3) if a != row[0]] for row in permutations]
        mu, recovered, recovery = blind.recover_source(tensor, rational_lines, permutations)
        gains = [mu[i][permutations[i][0]]/means[i][permutations[i][0]] for i in range(n)]
        assert math.prod(gains) == 1
        assert all(mu[i][a] == gains[i]*means[i][a] for i in range(n) for a in range(3))
        assert all(recovered[i, j][a][b] == gains[i]*gains[j]*edges[i, j][a][b]
                   for i, j in edges for a in range(3) for b in range(3))
        result.update({'full_source_recovered': True, 'recovery': recovery,
                       'recovered_means': [[str(x) for x in row] for row in mu],
                       'recovered_edges': serialize_edges({e: [[str(x) for x in row] for row in block]
                                                          for e, block in recovered.items()}),
                       'comparison_site_gains': [str(x) for x in gains]})
    return result


def run(quick=False):
    cases = []
    specifications = [(3, False, False, False), (5, False, False, False),
                      (7, False, False, True), (7, True, False, False)]
    if not quick:
        specifications.append((9, False, True, True))
    for n, paired, retained, full in specifications:
        cases.append(run_case(n, paired, retained, full))
        print(f'Verified {n}-site case; paired={paired}; retained failure={retained}', file=sys.stderr, flush=True)
    return {'pair_calculation': pair_calculation(), 'cases': cases,
            'paired_slice_checks': [paired_slice_check(m) for m in [1, 2, 3]],
            'three_site_dimension': three_site_dimension(cases[0]),
            'scope': 'Exact blind mean-line recovery and global uniqueness certificates for these inputs; full covariance recovery where recorded. No noisy-data or compressed-data inversion guarantee.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true')
    arguments = parser.parse_args()
    print(json.dumps(run(arguments.quick), indent=2))

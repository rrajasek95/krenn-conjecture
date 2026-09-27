#!/usr/bin/env python3
"""Observable rational certificates for noisy recovery of local mean lines.

Numerics propose inverse/operator matrices, a tail vector, and a Gram
preconditioner. Integer arithmetic certifies all accepted error bounds.
The estimator and acceptance function receive no planted source data.
"""

import argparse
import base64
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
import random
import sys
import time
import zlib

import numpy as np
from scipy.linalg import eigh, solve, svd
from flint import fmpz_mat

BITS = 44
SCALE = 2**BITS


def sqrt_upper(value, bits=70):
    value = F(value)
    scale = 2**bits
    numerator, denominator = value.numerator*scale*scale, value.denominator
    root = math.isqrt(numerator//denominator)
    root += int(root*root*denominator < numerator)
    return F(root, scale)


def encode(rows, scale=SCALE):
    array = np.asarray(rows, dtype='<i8')
    assert array.tolist() == rows
    packed = array.tobytes()
    return {'shape': list(array.shape), 'scale': str(scale),
            'encoding': 'zlib+base64; little-endian signed int64; row-major',
            'sha256': hashlib.sha256(packed).hexdigest(),
            'data': base64.b64encode(zlib.compress(packed, 9)).decode()}


def decode(saved):
    assert saved['encoding'] == 'zlib+base64; little-endian signed int64; row-major'
    raw = zlib.decompress(base64.b64decode(saved['data']))
    assert hashlib.sha256(raw).hexdigest() == saved['sha256']
    assert len(raw) == math.prod(saved['shape'])*8
    return np.frombuffer(raw, dtype='<i8').reshape(saved['shape']).tolist(), int(saved['scale'])


def quantize(array):
    return [[int(round(float(x)*SCALE)) for x in row] for row in np.atleast_2d(array)]


def slices(tensor):
    tail = tensor.ndim-1
    size = 3**tail
    offsets = np.asarray(list(itertools.product([1, 2], repeat=tail)))
    signs = (-1)**np.sum(offsets == 2, axis=1)
    powers = 3**np.arange(tail-1, -1, -1)
    result = []
    for colour in range(3):
        matrix = np.zeros((size, size), dtype=np.int64)
        flat = tensor[colour].reshape(-1)
        for row, word in enumerate(itertools.product(range(3), repeat=tail)):
            word = np.asarray(word)
            matrix[row, ((word+offsets) % 3)@powers] = signs*flat[((word-offsets) % 3)@powers]
        result.append(matrix)
    return result


def norm_bound(matrix, denominator=1):
    rows, columns = matrix.nrows(), matrix.ncols()
    row_max = max(sum(abs(int(matrix[i, j])) for j in range(columns)) for i in range(rows))
    col_max = max(sum(abs(int(matrix[i, j])) for i in range(rows)) for j in range(columns))
    return sqrt_upper(F(row_max*col_max, denominator**2))


def propose(observed, denominator, reference=0):
    matrices = [a.astype(float)/denominator for a in slices(observed)]
    size = matrices[0].shape[0]
    other = [a for a in range(3) if a != reference]
    inverse = solve(matrices[reference], np.eye(size), assume_a='sym')
    a = solve(matrices[reference], matrices[other[0]], assume_a='sym')
    b = solve(matrices[reference], matrices[other[1]], assume_a='sym')
    ia, ib = quantize(a), quantize(b)
    a, b = np.asarray(ia, dtype=float)/SCALE, np.asarray(ib, dtype=float)/SCALE
    c = a@b-b@a
    stack = np.concatenate([c, c@a])
    _, values, vh = svd(stack, full_matrices=False)
    z = vh[-1]
    iz = quantize(z)[0]
    z = np.asarray(iz, dtype=float)
    z /= np.linalg.norm(z)
    lines = []
    for site in range(observed.ndim-1):
        matrix = np.moveaxis(z.reshape((3,)*(observed.ndim-1)), site, 0).reshape(3, -1)
        u, _, _ = svd(matrix, full_matrices=False)
        lines.append(quantize(u[:, 0])[0])
    gram = stack.T@stack + np.outer(z, z)
    eigenvalues, vectors = eigh(gram)
    assert eigenvalues[0] > 0
    preconditioner = (vectors/np.sqrt(eigenvalues))@vectors.T
    return {'reference_slice': reference, 'inverse': encode(quantize(inverse)),
            'A': encode(ia), 'B': encode(ib), 'tail_vector': encode([iz]),
            'tail_lines': encode(lines), 'preconditioner': encode(quantize(preconditioner)),
            'smallest_stack_singular_value_estimate': float(values[-1]),
            'second_smallest_stack_singular_value_estimate': float(values[-2])}


def certify(observed, denominator, epsilon, proposal, builder=slices):
    n, size = observed.ndim, 3**(observed.ndim-1)
    assert n >= 3 and n % 2 == 1 and observed.shape == (3,)*n
    assert denominator > 0 and F(epsilon) >= 0
    assert np.issubdtype(observed.dtype, np.integer)
    matrices = [fmpz_mat(a.tolist()) for a in builder(observed)]
    reference = proposal['reference_slice']
    other = [a for a in range(3) if a != reference]
    decoded = {name: decode(proposal[name]) for name in ['inverse', 'A', 'B', 'tail_vector', 'tail_lines', 'preconditioner']}
    assert all(scale == SCALE for _, scale in decoded.values())
    inverse, a, b, preconditioner = [fmpz_mat(decoded[name][0]) for name in ['inverse', 'A', 'B', 'preconditioner']]
    z = fmpz_mat([[x] for x in decoded['tail_vector'][0][0]])
    z_squared = int((z.transpose()*z)[0, 0])
    assert z_squared > 0
    identity = fmpz_mat([[int(i == j) for j in range(size)] for i in range(size)])
    inverse_residual = identity*(denominator*SCALE)-inverse*matrices[reference]
    beta = norm_bound(inverse_residual, denominator*SCALE)
    assert beta < 1
    nu = norm_bound(inverse, SCALE)/(1-beta)
    alpha, beta_operator = norm_bound(a, SCALE), norm_bound(b, SCALE)
    rho_a = norm_bound(matrices[reference]*a-matrices[other[0]]*SCALE, denominator*SCALE)
    rho_b = norm_bound(matrices[reference]*b-matrices[other[1]]*SCALE, denominator*SCALE)
    c = a*b-b*a
    ca = c*a
    c_norm = norm_bound(c, SCALE**2)
    delta = 2**((n-1)//2)*F(epsilon)
    assert nu*delta < 1
    true_inverse_bound = nu/(1-nu*delta)
    error_a = true_inverse_bound*(rho_a+delta*(1+alpha))
    error_b = true_inverse_bound*(rho_b+delta*(1+beta_operator))
    error_c = 2*(beta_operator*error_a+alpha*error_b+error_a*error_b)
    error_ca = c_norm*error_a+error_c*(alpha+error_a)
    eta = sqrt_upper(error_c**2+error_ca**2)
    # Stack numerator is [SCALE*C; C*A], with denominator SCALE**3.
    stack_scale = SCALE**3
    stack_gram = (c.transpose()*c)*SCALE**2 + ca.transpose()*ca
    gram_scale = stack_scale**2*z_squared
    gram = stack_gram*z_squared + (z*z.transpose())*stack_scale**2
    tested = preconditioner.transpose()*gram*preconditioner
    expected_diagonal = SCALE**2*gram_scale
    residual_squared = sum((int(tested[i, j])-(expected_diagonal if i == j else 0))**2
                           for i in range(size) for j in range(size))
    residual_upper = math.isqrt(residual_squared)
    residual_upper += int(residual_upper**2 < residual_squared)
    gap = expected_diagonal-residual_upper
    assert gap > 0
    preconditioner_squared = sum(int(preconditioner[i, j])**2 for i in range(size) for j in range(size))
    inverse_squared_bound = F(gram_scale*preconditioner_squared, gap)
    g = sqrt_upper(inverse_squared_bound)
    cz, caz = c*z, ca*z
    vector_residual_squared = F(sum(int(cz[i, 0])**2*SCALE**2+int(caz[i, 0])**2
                                    for i in range(size)), stack_scale**2*z_squared)
    residual = sqrt_upper(vector_residual_squared)
    q = g*(eta+residual)
    assert q < F(1, 4), 'Noise/roundoff bound too large for the recorded recovery guarantee'
    estimates = [F(int((z.transpose()*operator*z)[0, 0]), SCALE*z_squared) for operator in [a, b]]
    first_line = [F(0)]*3
    first_line[reference] = F(1)
    for colour, estimate in zip(other, estimates):
        first_line[colour] = estimate
    first_bound = sqrt_upper((error_a+2*alpha*q)**2+(error_b+2*beta_operator*q)**2)
    # Division by ||first_line|| would improve this conservative bound.
    direction_bounds = [first_bound]
    product_residuals = []
    tensor_z = np.asarray(decoded['tail_vector'][0][0], dtype=object).reshape((3,)*(n-1))
    for i, row in enumerate(decoded['tail_lines'][0]):
        local_norm = sum(x*x for x in row)
        matrix = np.moveaxis(tensor_z, i, 0).reshape(3, -1)
        contraction = [sum(row[a]*int(matrix[a, j]) for a in range(3)) for j in range(matrix.shape[1])]
        squared = F(1)-F(sum(x*x for x in contraction), local_norm*z_squared)
        assert squared >= 0
        residual_i = sqrt_upper(squared)
        product_residuals.append(residual_i)
        direction_bounds.append(residual_i+2*q)
    assert all(bound < 1 for bound in direction_bounds)
    values = {'noise_bound': F(epsilon), 'inverse_residual_bound': beta,
              'observed_inverse_norm_bound': nu, 'A_norm_bound': alpha, 'B_norm_bound': beta_operator,
              'C_norm_bound': c_norm, 'A_solve_residual_bound': rho_a, 'B_solve_residual_bound': rho_b,
              'slice_perturbation_bound': delta, 'A_error_bound': error_a, 'B_error_bound': error_b,
              'stack_perturbation_bound': eta, 'augmented_gram_inverse_squared_bound': inverse_squared_bound,
              'perpendicular_inverse_bound': g, 'tail_vector_residual_bound': residual,
              'tail_line_sine_bound': q}
    return {'bounds': {k: str(v) for k, v in values.items()},
            'gram_residual_frobenius_squared': str(residual_squared),
            'gram_residual_frobenius_upper': str(residual_upper),
            'tail_factor_residual_bounds': [str(x) for x in product_residuals],
            'local_mean_line_sine_bounds': [str(x) for x in direction_bounds],
            'first_line_estimate': [str(x) for x in first_line],
            'scope': 'All compression tensors within the recorded data-error ball; all matching representations of any such tensor have nonzero means and obey these local-line angle bounds.'}


def paired_rotated_tensor(m):
    identity = np.eye(3, dtype=np.int64)
    e, f = np.zeros((3, 3), dtype=np.int64), np.zeros((3, 3), dtype=np.int64)
    e[0, 1] = e[1, 0] = f[0, 2] = f[2, 0] = 1

    def product(factors):
        result = np.array([1], dtype=np.int64)
        for factor in factors:
            result = np.kron(result, factor.reshape(-1))
        return result

    tensor = np.zeros((3, 9**m), dtype=np.int64)
    tensor[0] = 9*product([identity]*m)
    rotations = []
    for k in range(m):
        w = np.array([1, (-1)**k, (-1)**(k//2)])
        rotation = 3*identity-2*np.outer(w, w)
        assert np.array_equal(rotation.T@rotation, 9*identity)
        rotations.append(rotation.tolist())
        for colour, matrix, coefficient in [(1, e, 3**k), (2, f, 1)]:
            factors = [identity]*m
            factors[k] = rotation@matrix@rotation.T
            tensor[colour] += coefficient*product(factors)
    return tensor.reshape((3,)*(2*m+1)), rotations


def run_case(n):
    start = time.monotonic()
    clean, rotations = paired_rotated_tensor((n-1)//2)
    rng = random.Random(274000+n)
    noise_scale = 2**40
    noise = np.asarray([rng.choice([-1, 1]) for _ in range(3**n)], dtype=np.int64).reshape(clean.shape)
    observed, denominator = clean*noise_scale+9*noise, 9*noise_scale
    epsilon = F(math.isqrt(3**n)+1, noise_scale)
    proposal = propose(observed, denominator)
    print(f'Proposed {n}-site noisy inverse; checking integers', file=sys.stderr, flush=True)
    certificate = certify(observed, denominator, epsilon, proposal)
    expected = [[1, 0, 0]]
    for rotation in rotations:
        expected.extend([[row[0] for row in rotation]]*2)
    decoded_lines, _ = decode(proposal['tail_lines'])
    recovered = [[F(x) for x in certificate['first_line_estimate']]] + [[F(x) for x in row] for row in decoded_lines]
    actual_squared = []
    for actual, found, bound in zip(expected, recovered, certificate['local_mean_line_sine_bounds']):
        squared = 1-sum(a*b for a, b in zip(actual, found))**2/(sum(a*a for a in actual)*sum(b*b for b in found))
        assert 0 <= squared <= F(bound)**2
        actual_squared.append(str(squared))
    print(f'Certified {n} sites; worst sine bound {max(map(lambda x: float(F(x)), certificate["local_mean_line_sine_bounds"])):.4g}', file=sys.stderr, flush=True)
    return {'sites': n, 'observed_numerator': observed.reshape(-1).tolist(),
            'observed_denominator': denominator, 'epsilon': str(epsilon),
            'proposal': proposal, 'certificate': certificate,
            'test_comparison_only': {'clean_tensor_numerator': clean.reshape(-1).tolist(),
                                     'clean_tensor_denominator': 9, 'pair_rotation_numerators': rotations,
                                     'rotation_denominator': 3, 'noise_numerators': noise.reshape(-1).tolist(),
                                     'noise_denominator': noise_scale, 'expected_mean_lines': expected,
                                     'actual_line_sine_squared': actual_squared},
            'elapsed_seconds': time.monotonic()-start}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true')
    args = parser.parse_args()
    print(json.dumps({'cases': [run_case(n) for n in ([3, 5] if args.quick else [3, 5, 7])],
                      'scope': 'Certified noisy local mean directions, without a supplied source or initial mean guess. No covariance-error or compressed-measurement inversion certificate.'}, indent=2))

#!/usr/bin/env python3
"""Exact checks for near-ambiguity, shared calibration, and setting design.

Polynomial proofs establish all orders. Full integer tensor checks cover
seven and nine sites. Numerical singular values illustrate exact exponents.
"""

from fractions import Fraction as F
from functools import lru_cache
import hashlib
import itertools
import json
import math
import random

import numpy as np
import sympy as sp

from audit_pair_observation import moments
from blind_mean_search import integer_tensor, scalar_bound
from restricted_source_inverse import serialize_edges


def involution_coefficient(q):
    return (-1)**q * sum(F(math.factorial(2*q + 1), math.factorial(2*q + 1 - 2*j) * math.factorial(j))
                        * F(-1, 3)**j for j in range(q + 1))


def integer_layers(means, edges):
    assert scalar_bound(means, edges) < 2**63

    @lru_cache(None)
    def rec(sites):
        if not sites:
            return np.array([1], dtype=np.int64)
        i, *rest = sites
        result = np.zeros((len(sites)//2 + 1,) + (3,)*len(sites), dtype=np.int64)
        old = rec(tuple(rest))
        result[:len(old)] = np.asarray(means[i]).reshape((1, 3) + (1,)*len(rest)) * old[:, None]
        for position, j in enumerate(rest, 1):
            old = rec(tuple(k for k in rest if k != j))
            pair = np.asarray(edges[i, j]).reshape((1, 3, 3) + (1,)*(len(rest) - 1))
            result[1:len(old) + 1] += np.moveaxis(pair * old[:, None, None], 2, position + 1)
        return result
    return rec(tuple(range(len(means)))).reshape((len(means)//2 + 1, -1))


def moment_directional_derivative(means, edges, dmeans, dedges):
    bound_means = [[abs(x)+abs(y) for x,y in zip(row,drow)] for row,drow in zip(means,dmeans)]
    bound_edges = {edge:[[abs(x)+abs(y) for x,y in zip(row,drow)]
                        for row,drow in zip(block,dedges[edge])] for edge,block in edges.items()}
    assert scalar_bound(bound_means,bound_edges) < 2**63

    @lru_cache(None)
    def rec(sites):
        if not sites:
            return np.array(1,dtype=np.int64),np.array(0,dtype=np.int64)
        i,*rest=sites
        old,dold=rec(tuple(rest))
        mu=np.asarray(means[i]).reshape((3,)+(1,)*len(rest))
        dmu=np.asarray(dmeans[i]).reshape((3,)+(1,)*len(rest))
        value,derivative=mu*old[None],dmu*old[None]+mu*dold[None]
        for position,j in enumerate(rest,1):
            old,dold=rec(tuple(k for k in rest if k!=j))
            pair=np.asarray(edges[i,j]).reshape((3,3)+(1,)*(len(rest)-1))
            dpair=np.asarray(dedges[i,j]).reshape((3,3)+(1,)*(len(rest)-1))
            value=value+np.moveaxis(pair*old[None,None],1,position)
            derivative=derivative+np.moveaxis(dpair*old[None,None]+pair*dold[None,None],1,position)
        return value,derivative
    return rec(tuple(range(len(means))))


def full_tensor_case(n):
    seed = 272020 + n
    rng = random.Random(seed)
    values = [-2, -1, 1, 2]
    means = [[rng.choice(values) for _ in range(3)] for _ in range(n)]
    edges = {edge: [[rng.choice(values) for _ in range(3)] for _ in range(3)]
             for edge in itertools.combinations(range(n), 2)}
    t, denominator, sign = F(1, 2), 12, (-1)**((n - 1)//2)
    first_means = [[int(denominator*t*x) for x in row] for row in means]
    first_edges = {edge: [[denominator**2*x for x in row] for row in block] for edge, block in edges.items()}
    other_means = [[sign*x for x in row] for row in first_means]
    other_edges = {(i, j): [[-first_edges[i, j][a][b]
                            - int(F(2, 3)*denominator**2*t*t*means[i][a]*means[j][b])
                            for b in range(3)] for a in range(3)] for i, j in edges}
    first, other = integer_tensor(first_means, first_edges), integer_tensor(other_means, other_edges)
    layers = integer_layers(means, edges)
    assert np.array_equal(layers.sum(axis=0), integer_tensor(means, edges).reshape(-1))
    expected = np.zeros(3**n, dtype=object)
    coefficients = []
    m = (n - 1)//2
    for q in range(m + 1):
        multiplier = denominator**n * (involution_coefficient(q) - 1) * t**(2*q + 1)
        assert multiplier.denominator == 1
        expected += multiplier.numerator * layers[m - q].astype(object)
        coefficients.append(str(multiplier))
    difference = other.reshape(-1).astype(object) - first.reshape(-1).astype(object)
    assert np.array_equal(difference, expected)
    # Differentiate the actual rational path parameterized by covariance scale a.
    dmeans = [[-m*x for x in row] for row in first_means]
    dedges = {(i,j):[[first_edges[i,j][a][b]+int(F(n,3)*denominator**2*t*t*means[i][a]*means[j][b])
                     for b in range(3)] for a in range(3)] for i,j in edges}
    check_first, derivative = moment_directional_derivative(first_means,first_edges,dmeans,dedges)
    assert np.array_equal(check_first,first)
    expected_derivative=np.zeros(3**n,dtype=object)
    for q in range(m+1):
        coefficient=denominator**n*F(2*n,3)*q*(q-1)*t**(2*q+1)
        assert coefficient.denominator==1
        expected_derivative+=coefficient.numerator*layers[m-q].astype(object)
    assert np.array_equal(derivative.reshape(-1).astype(object),expected_derivative)
    bound = max(scalar_bound(first_means, first_edges), scalar_bound(other_means, other_edges))
    modulus = 2*bound + 1
    for mu, covariance, tensor in [(first_means, first_edges, first), (other_means, other_edges, other)]:
        assert moments(mu, covariance, modulus) == [int(x) % modulus for x in tensor.reshape(-1)]
    cycle = [(i, i + 1) for i in range(n - 1)] + [(0, n - 1)]
    cycle_first = math.prod(edges[edge][0][0] for edge in cycle)
    cycle_other = math.prod(F(other_edges[edge][0][0], denominator**2) for edge in cycle)
    assert cycle_first and cycle_other != cycle_first
    nonzero = next(i for i, x in enumerate(layers[m - 3]) if x)
    return {"sites": n, "seed": seed, "mean_multiplier": str(t), "involution_mean_sign": sign,
            "source_mean_direction": means, "source_edges": serialize_edges(edges),
            "common_variable_scaling_denominator": denominator,
            "integer_difference_layer_coefficients": coefficients,
            "all_tensor_entries_checked_against_response_formula": True,
            "actual_source_directional_derivative_checked_entrywise": True,
            "both_integer_tensors_checked_by_independent_recursion": True,
            "integer_absolute_bound": bound, "integer_check_modulus": modulus,
            "first_tensor_sha256": hashlib.sha256(json.dumps(first.reshape(-1).tolist()).encode()).hexdigest(),
            "other_tensor_sha256": hashlib.sha256(json.dumps(other.reshape(-1).tolist()).encode()).hexdigest(),
            "nonzero_seventh_response_entry": {"index": nonzero, "value": int(layers[m - 3, nonzero])},
            "cycle_invariant_original": str(cycle_first), "cycle_invariant_other": str(cycle_other),
            "cycle_invariant_other_limit_at_zero_mean": str(-cycle_first)}


def symbolic_checks():
    x, t, z, beta, k, z1, z2 = sp.symbols('x t z beta k z1 z2')
    series = sp.series(sp.exp(x*x/3)*sp.sin(x), x, 0, 16).removeO().expand()
    coefficient_table = []
    for q in range(7):
        coefficient = involution_coefficient(q)
        assert sp.factorial(2*q + 1)*series.coeff(x, 2*q + 1) == sp.Rational(coefficient.numerator, coefficient.denominator)
        coefficient_table.append({"mean_degree": 2*q + 1, "transformed_coefficient": str(coefficient)})
    polynomials = []
    for q in range(6):
        polynomial = sum(sp.factorial(2*q + 1) / (2**ell*sp.factorial(ell)*sp.factorial(2*q + 1 - 2*ell))
                         * beta**(q - ell)*z**(2*q + 1 - 2*ell)*k**ell for ell in range(q + 1))
        polynomials.append(polynomial)
        transformed = sp.expand(polynomial.subs({beta: -1, k: 2*z*z/3}))
        assert sp.simplify(transformed - sp.Rational(str(involution_coefficient(q)))*z**(2*q + 1)) == 0
        derivative = sp.diff(polynomial.subs(k, (1-beta)*z*z/3), beta).subs(beta, 1)
        assert sp.simplify(derivative + sp.Rational(2, 3)*q*(q-1)*z**(2*q + 1)) == 0
    single = sp.Matrix(polynomials[:3]).jacobian([z, k, beta]).subs({z: t, k: 0, beta: 1})
    single_det = sp.factor(single.det())
    assert single_det == -4*t**6
    pair = sp.Matrix([z1, z2, beta*z1**3+3*z1*k, beta*z2**3+3*z2*k]).jacobian([z1,z2,k,beta])
    pair_det = sp.factor(pair.det())
    assert sp.expand(pair_det - 3*z1*z2*(z2*z2-z1*z1)) == 0
    scaling = []
    for n in [7, 9, 11]:
        for denominator in [2, 4, 8, 16, 32]:
            small = 1/denominator
            rows = []
            for q in range((n+1)//2):
                rows.append([(2*q+1)*small**(2*q), q*(2*q+1)*small**(2*q-1) if q else 0,
                             q*small**(2*q+1)])
            sigma_single = float(np.linalg.svd(np.array(rows), compute_uv=False)[-1])
            rows = []
            for j, value in enumerate([small, 2*small]):
                for q in range((n+1)//2):
                    row = [0.,0.,q*(2*q+1)*value**(2*q-1) if q else 0.,q*value**(2*q+1)]
                    row[j] = (2*q+1)*value**(2*q)
                    rows.append(row)
            sigma_pair = float(np.linalg.svd(np.array(rows), compute_uv=False)[-1])
            scaling.append({"sites":n, "mean_scale":str(F(1,denominator)),
                            "single_sigma_over_t5":sigma_single/small**5,
                            "pair_sigma_over_t3":sigma_pair/small**3})
    return {"involution_coefficients":coefficient_table,
            "single_local_minor":str(single_det), "shared_local_minor":str(pair_det),
            "cubic_and_fifth_matching_checked_symbolically":True,
            "local_path_derivatives_checked_through_mean_degree":11,
            "illustrative_singular_value_scaling":scaling}


def frobenius(first, second):
    return sum(x*y for a,b in zip(first,second) for x,y in zip(a,b))


def shared_calibration_check():
    directions = [[F(1),F(0)],[F(0),F(1)],[F(3,5),F(4,5)],[F(-4,5),F(3,5)]]
    z = [[x/2 for x in row] for row in directions]
    matrices = [[[x*y for y in row] for x in row] for row in z]
    count = len(z)
    average = [[sum(matrix[a][b] for matrix in matrices)/count for b in range(2)] for a in range(2)]
    centered = [[[matrix[a][b]-average[a][b] for b in range(2)] for a in range(2)] for matrix in matrices]
    variance = sum(frobenius(matrix,matrix) for matrix in centered)
    assert variance == F(1,8)
    beta = F(5,3)
    k = [[F(1,7),F(2,11)],[F(2,11),F(-1,5)]]
    outputs = [[[k[a][b]+beta*matrix[a][b]/3 for b in range(2)] for a in range(2)] for matrix in matrices]
    estimate = 3*sum(frobenius(c,s) for c,s in zip(centered,outputs))/variance
    assert estimate == beta
    recovered_k = [[sum(s[a][b] for s in outputs)/count-estimate*average[a][b]/3
                    for b in range(2)] for a in range(2)]
    assert recovered_k == k
    noise = [[[x/1000 for x in row] for row in matrix] for matrix in centered]
    observed = [[[s[a][b]+e[a][b] for b in range(2)] for a in range(2)] for s,e in zip(outputs,noise)]
    perturbed = 3*sum(frobenius(c,s) for c,s in zip(centered,observed))/variance
    noise_squared = sum(frobenius(e,e) for e in noise)
    assert (perturbed-beta)**2 == 9*noise_squared/variance
    # Equal-norm design: the displayed four directions form two orthonormal bases.
    design_operator = [[sum(row[a]*row[b] for row in directions) for b in range(2)] for a in range(2)]
    assert design_operator == [[F(2),F(0)],[F(0),F(2)]]
    degenerate = [z[0], [-x for x in z[0]]]
    degenerate_matrices = [[[x*y for y in row] for x in row] for row in degenerate]
    assert degenerate_matrices[0] == degenerate_matrices[1]
    return {"mean_coordinate_vectors":[[str(x) for x in row] for row in z],
            "outer_product_variance":str(variance), "true_beta":str(beta),
            "recovered_beta":str(estimate), "perturbed_beta":str(perturbed),
            "recovered_mean_quadratic":[[str(x) for x in row] for row in recovered_k],
            "noise_squared_norm":str(noise_squared), "sharp_error_bound_attained":True,
            "tight_frame_design_bound_attained":True,
            "identical_or_sign_reversed_settings_have_zero_variance":True}


if __name__ == '__main__':
    print(json.dumps({"symbolic":symbolic_checks(), "full_tensor_cases":[full_tensor_case(7),full_tensor_case(9)],
                      "shared_calibration":shared_calibration_check(),
                      "scope":"All-orders identities proved in the note; finite computations check formulas."
                      " Calibration stability assumes a fixed response frame and covariance class."},indent=2))

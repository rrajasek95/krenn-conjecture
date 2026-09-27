#!/usr/bin/env python3
"""Blind numerical mean-line search followed by exact verification.

Successful seven/nine-site cases also recover the entire source over Q.
The eleven-site case checks lines only. A harder failed search is retained.
No convergence guarantee is inferred from solver termination or examples.
"""

from contextlib import contextmanager
from fractions import Fraction
from functools import lru_cache
import hashlib
import itertools
import json
import math
import random

import numpy as np
import scipy
from scipy.optimize import least_squares
from flint import fmpq_mat, fmpz_mat, nmod_mat

import restricted_source_inverse as inverse
import three_outside_certificate as outside_certificate
from audit_pair_observation import moments

PRIME = 1000003


def scalar_bound(means, edges):
    """An integer bound on every entry of every nonempty subset moment."""
    @lru_cache(None)
    def rec(sites):
        if not sites:
            return 1
        i, *rest = sites
        total = max(abs(x) for x in means[i]) * rec(tuple(rest))
        for j in rest:
            total += max(abs(x) for row in edges[i, j] for x in row) * rec(tuple(k for k in rest if k != j))
        return total
    return max(rec(sites) for count in range(len(means) + 1)
               for sites in itertools.combinations(range(len(means)), count))


def integer_tensor(means, edges):
    assert scalar_bound(means, edges) < 2**63

    @lru_cache(None)
    def rec(sites):
        if not sites:
            return np.array(1, dtype=np.int64)
        i, *rest = sites
        out = np.asarray(means[i]).reshape((3,) + (1,) * len(rest)) * rec(tuple(rest))[None]
        for position, j in enumerate(rest, 1):
            pair = np.asarray(edges[i, j]).reshape((3, 3) + (1,) * (len(rest) - 1))
            term = pair * rec(tuple(k for k in rest if k != j))[None, None]
            out = out + np.moveaxis(term, 1, position)
        return out
    return rec(tuple(range(len(means))))


def contract(tensor, maps, skip=None):
    out = tensor
    for i, matrix in enumerate(maps):
        if i != skip:
            out = np.moveaxis(np.tensordot(matrix, out, axes=(1, i)), 0, i)
    return out


def numerical_problem(tensor, initial_lines=None):
    n = tensor.ndim
    scale = float(np.linalg.norm(tensor))
    tensor = tensor / scale
    permutations, start = [], []
    for i in range(n):
        if initial_lines is None:
            flat = np.moveaxis(tensor, i, 0).reshape(3, -1)
            _, vectors = np.linalg.eigh(flat @ flat.T)
            vector = vectors[:, -1]
        else:
            vector = initial_lines[i]
        pivot = int(np.argmax(abs(vector)))
        permutation = [pivot] + [a for a in range(3) if a != pivot]
        permutations.append(permutation)
        start.extend((vector[permutation[1:]] / vector[pivot]).tolist())
    for i, permutation in enumerate(permutations):
        tensor = np.take(tensor, permutation, axis=i)
    last, result = None, None

    def residual_and_jacobian(h):
        nonlocal last, result
        if last is not None and np.array_equal(last, h):
            return result
        maps, derivatives = [], []
        for v in h.reshape(n, 2):
            r = np.sqrt(1 + v @ v)
            c = 1 / (r * (r + 1))
            dc = -(2 * r + 1) / (2 * r**3 * (r + 1)**2)
            q = np.column_stack([-v, np.eye(2)])
            w = np.eye(2) - c * np.outer(v, v)
            maps.append(w @ q)
            local = []
            for a in range(2):
                e = np.eye(2)[a]
                dw = -c * (np.outer(e, v) + np.outer(v, e)) - 2 * v[a] * dc * np.outer(v, v)
                dq = np.zeros((2, 3))
                dq[a, 0] = -1
                local.append(dw @ q + w @ dq)
            derivatives.append(local)
        residual = contract(tensor, maps).reshape(-1)
        columns = []
        for i in range(n):
            part = contract(tensor, maps, skip=i)
            for matrix in derivatives[i]:
                columns.append(np.moveaxis(np.tensordot(matrix, part, axes=(1, i)), 0, i).reshape(-1))
        result = residual, np.array(columns).T
        last = h.copy()
        return result

    return np.array(start), permutations, residual_and_jacobian, scale


def exact_line_check(tensor, lines, permutations):
    maps, derivative_scales = [], []
    for row, permutation in zip(lines, permutations):
        matrix = np.zeros((2, 3), dtype=object)
        scales = []
        for a, colour in enumerate(permutation[1:]):
            value = row[colour]
            matrix[a, colour] = value.denominator
            matrix[a, permutation[0]] = -value.numerator
            scales.append(value.denominator)
        maps.append(matrix)
        derivative_scales.append(scales)
    exact_tensor = tensor.astype(object)
    if any(contract(exact_tensor, maps).reshape(-1)):
        return None
    columns = []
    for i, permutation in enumerate(permutations):
        partial = -np.take(contract(exact_tensor, maps, skip=i), permutation[0], axis=i)
        for a in range(2):
            column = np.zeros((2,) * tensor.ndim, dtype=object)
            index = [slice(None)] * tensor.ndim
            index[i] = a
            column[tuple(index)] = derivative_scales[i][a] * partial
            columns.append([int(x) for x in column.reshape(-1)])
    integer_rows = list(map(list, zip(*columns)))
    matrix = nmod_mat(integer_rows, PRIME)
    rows = inverse.base.pivot_columns(matrix.transpose())
    if len(rows) != 2 * tensor.ndim:
        return None
    square = nmod_mat([[int(matrix[i, j]) for j in range(matrix.ncols())] for i in rows], PRIME)
    integer_jacobian = fmpz_mat(integer_rows)
    gram_inverse = fmpq_mat(integer_jacobian.transpose() * integer_jacobian).inv()
    inverse_trace = sum(Fraction(str(gram_inverse[i, i])) for i in range(gram_inverse.nrows()))
    norm_product = math.prod(sum(x * x for x in row) for row in lines)
    denominator_product = math.prod(max(scales)**2 for scales in derivative_scales)
    tensor_norm_squared = sum(int(x)**2 for x in tensor.reshape(-1))
    amplification_squared = tensor_norm_squared * norm_product * denominator_product * inverse_trace
    sigma_squared_lower = 1 / amplification_squared
    assert sigma_squared_lower > 0
    return {"integer_quotient_residual_is_zero": True,
            "projective_tangent_rank": len(rows), "tangent_minor_rows": rows,
            "tangent_minor_prime": PRIME, "tangent_minor_determinant": int(square.det()),
            "integer_tangent_gram_inverse_trace": str(inverse_trace),
            "normalized_jacobian_sigma_squared_lower_bound": str(sigma_squared_lower),
            "relative_first_order_amplification_squared_upper_bound": str(amplification_squared)}


def search_lines(tensor, seed=271990, attempts=16):
    """Uses only an integer tensor; returns only exactly checked rational lines."""
    assert np.issubdtype(tensor.dtype, np.integer), "Exact acceptance requires integer input entries"
    start, original_permutations, original_problem, scale = numerical_problem(tensor)
    problem = original_problem
    # A directional finite-difference audit of the analytic Jacobian.
    direction = np.arange(1, len(start) + 1, dtype=float)
    direction /= np.linalg.norm(direction)
    step = 1e-6
    finite_difference = (problem(start + step * direction)[0] - problem(start - step * direction)[0]) / (2 * step)
    analytic = problem(start)[1] @ direction
    derivative_error = float(np.linalg.norm(finite_difference - analytic))
    assert derivative_error < 1e-7
    rng = random.Random(seed)
    reports = []
    for attempt in range(attempts):
        permutations, problem = original_permutations, original_problem
        initial = start if not attempt else np.array([rng.gauss(0, 1) for _ in start])
        evaluations = 0
        for chart_round in range(4):
            fit = least_squares(lambda h: problem(h)[0], initial, jac=lambda h: problem(h)[1],
                                method="lm", x_scale="jac", max_nfev=300,
                                ftol=1e-13, xtol=1e-13, gtol=1e-13)
            evaluations += fit.nfev
            if max(abs(fit.x)) <= 4 or chart_round == 3:
                break
            floating_lines = []
            for i, permutation in enumerate(permutations):
                line = np.zeros(3)
                line[permutation[0]] = 1
                line[permutation[1:]] = fit.x[2 * i:2 * i + 2]
                floating_lines.append(line)
            initial, permutations, problem, _ = numerical_problem(tensor, floating_lines)
        norm = float(np.linalg.norm(fit.fun))
        reports.append({"attempt": attempt, "function_evaluations": evaluations,
                        "chart_changes": chart_round,
                        "normalized_residual_norm": norm, "solver_success": bool(fit.success)})
        if norm > 1e-10:
            continue
        lines = []
        for i, permutation in enumerate(permutations):
            line = [Fraction(0)] * 3
            line[permutation[0]] = Fraction(1)
            for a, colour in enumerate(permutation[1:]):
                line[colour] = Fraction(float(fit.x[2 * i + a])).limit_denominator(10000)
            lines.append(line)
        exact = exact_line_check(tensor, lines, permutations)
        if exact is None:
            continue
        sigma = float(np.linalg.svd(problem(fit.x)[1], compute_uv=False)[-1])
        assert float(Fraction(exact["normalized_jacobian_sigma_squared_lower_bound"])) <= sigma**2 * (1 + 1e-10)
        return lines, {"accepted": True, "permutations": permutations, "attempts": reports,
                       "jacobian_directional_check_error": derivative_error,
                       "normalized_jacobian_sigma_min_estimate": sigma,
                       "tensor_frobenius_norm": scale, **exact}
    return None, {"accepted": False, "permutations": permutations, "attempts": reports,
                  "jacobian_directional_check_error": derivative_error,
                  "reason": "No exactly verified simple rational mean tuple found within the search budget."}


@contextmanager
def covariance_field(prime):
    """Temporarily configure the earlier scripts' shared field constants."""
    modules = [inverse, inverse.single, inverse.calibrated, inverse.calibrated.many,
               inverse.base, outside_certificate]
    previous = [module.P for module in modules]
    try:
        for module in modules:
            module.P = prime
        yield
    finally:
        for module, value in zip(modules, previous):
            module.P = value


def rational_reconstruct(value, modulus):
    """Unique bounded rational reconstruction, or fail without an answer."""
    bound = math.isqrt((modulus - 1) // 2)
    old_r, r, old_t, t = modulus, value % modulus, 0, 1
    while abs(r) > bound:
        q = old_r // r
        old_r, r, old_t, t = r, old_r - q * r, t, old_t - q * t
    if not t or abs(t) > bound or math.gcd(r, t) != 1:
        raise ValueError("A larger prime is needed for rational reconstruction")
    answer = Fraction(r, t)
    assert (answer.numerator - value * answer.denominator) % modulus == 0
    return answer


def recover_source(tensor, lines, permutations):
    assert np.issubdtype(tensor.dtype, np.integer), "Exact output verification requires integer input entries"
    n = tensor.ndim
    modular_lines = [[x.numerator * pow(x.denominator, -1, PRIME) % PRIME for x in row] for row in lines]
    with covariance_field(PRIME):
        mu, edges, report = inverse.recover([int(x) % PRIME for x in tensor.reshape(-1)], modular_lines)
    gains = [pow(mu[i][permutations[i][0]], -1, PRIME) for i in range(n - 1)]
    gains.append(pow(math.prod(gains) % PRIME, -1, PRIME))
    mu = [[rational_reconstruct(gains[i] * x % PRIME, PRIME) for x in row] for i, row in enumerate(mu)]
    edges = {(i, j): [[rational_reconstruct(gains[i] * gains[j] * x % PRIME, PRIME) for x in row]
                       for row in block] for (i, j), block in edges.items()}
    denominator = math.lcm(*(x.denominator for row in mu for x in row),
                           *(x.denominator for block in edges.values() for row in block for x in row))
    scaled_mu = [[int(denominator * x) for x in row] for row in mu]
    scaled_edges = {edge: [[int(denominator**2 * x) for x in row] for row in block] for edge, block in edges.items()}
    bound = max(scalar_bound(scaled_mu, scaled_edges),
                denominator**n * max(abs(int(x)) for x in tensor.reshape(-1)))
    # Independent recurrence; the bound turns this congruence into equality over Z.
    check_modulus = 2 * bound + 1
    expected = [denominator**n * int(x) % check_modulus for x in tensor.reshape(-1)]
    assert moments(scaled_mu, scaled_edges, check_modulus) == expected
    report.update({"field_prime": PRIME, "rational_lift_bound": math.isqrt((PRIME - 1) // 2),
                   "canonical_site_gains": gains, "common_denominator": denominator,
                   "integer_absolute_entry_bound": bound, "integer_check_modulus": check_modulus,
                   "every_tensor_entry_verified_over_Q": True})
    return mu, edges, report


def run_case(n, edge_scale, full_inverse):
    seed = 271960 + n + edge_scale
    rng = random.Random(seed)
    means = [[rng.choice([-2, -1, 1, 2]) for _ in range(3)] for _ in range(n)]
    edges = {edge: [[rng.randint(-edge_scale, edge_scale) for _ in range(3)] for _ in range(3)]
             for edge in itertools.combinations(range(n), 2)}
    tensor = integer_tensor(means, edges)
    lines, report = search_lines(tensor)
    answer = {"sites": n, "edge_scale": edge_scale, "source_seed": seed,
              "source_means": means, "source_edges": inverse.serialize_edges(edges),
              "tensor_sha256": hashlib.sha256(json.dumps(tensor.reshape(-1).tolist()).encode()).hexdigest(),
              "mean_search": report}
    if lines is None:
        answer["full_source_recovered"] = False
        # Postmortem only: never passed back into the blind search or inverse.
        diagnostic_lines = [[Fraction(x, means[i][report["permutations"][i][0]]) for x in row]
                            for i, row in enumerate(means)]
        diagnostic = exact_line_check(tensor, diagnostic_lines, report["permutations"])
        assert diagnostic is not None
        answer["postmortem_at_planted_lines"] = diagnostic
        answer["postmortem_scope"] = "Known source used only after failure to check local regularity; not a blind recovery."
        return answer
    assert all(lines[i][a] * means[i][b] == lines[i][b] * means[i][a]
               for i in range(n) for a in range(3) for b in range(3))
    answer["recovered_mean_lines"] = [[str(x) for x in row] for row in lines]
    answer["matches_planted_mean_lines"] = True
    if full_inverse:
        mu, recovered, recovery = recover_source(tensor, lines, report["permutations"])
        gains = [mu[i][0] / means[i][0] for i in range(n)]
        assert math.prod(gains) == 1
        assert all(mu[i][a] == gains[i] * means[i][a] for i in range(n) for a in range(3))
        assert all(recovered[i, j][a][b] == gains[i] * gains[j] * edges[i, j][a][b]
                   for i, j in edges for a in range(3) for b in range(3))
        answer.update({"full_source_recovered": True, "recovery": recovery,
                       "recovered_means": [[str(x) for x in row] for row in mu],
                       "recovered_edges": inverse.serialize_edges({edge: [[str(x) for x in row] for row in block]
                                                                    for edge, block in recovered.items()}),
                       "source_comparison_site_scalars": [str(x) for x in gains]})
    else:
        answer["full_source_recovered"] = False
        answer["scope"] = "Mean lines only; no covariance reconstruction attempted."
    return answer


if __name__ == "__main__":
    cases = [run_case(7, 3, True), run_case(9, 3, True), run_case(11, 3, False), run_case(9, 30, False)]
    assert cases[0]["full_source_recovered"] and cases[1]["full_source_recovered"]
    print(json.dumps({"scipy_version": scipy.__version__, "search_seed": 271990, "cases": cases,
                      "scope": "Heuristic blind search with exact acceptance; no global convergence guarantee."
                      " Tangent minors certify local simplicity, not global uniqueness of an individual input."}, indent=2))

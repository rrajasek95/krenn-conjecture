#!/usr/bin/env python3
"""Calibrate reconstructed response spans at arbitrary odd orders.

The inverse functions take actual tensors, a recovered mean frame, and a
recovered covariance-class representative. Examples reuse the previously
certified blind span reconstructions. Requires python-flint and numpy
(the latter is imported by the independent moment-recursion module).
"""

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

from flint import nmod_mat

from audit_pair_observation import moments
import many_direction as many

base, P = many.base, many.P


def symbolic_identities():
    """Expand exact Gaussian odd moments after Q=S-u/3, u=beta*Z^2."""
    expected = {
        1: {(0, 1): Fraction(3)},
        2: {(0, 2): Fraction(15), (2, 0): Fraction(-2, 3)},
        3: {(0, 3): Fraction(105), (2, 1): Fraction(-14), (3, 0): Fraction(16, 9)},
    }
    answers = {}
    for m in [1, 2, 3]:
        polynomial = {}
        for pairs in range(m + 1):
            coefficient = Fraction(math.factorial(2 * m + 1),
                                   2**pairs * math.factorial(pairs) * math.factorial(2 * m + 1 - 2 * pairs))
            for u_count in range(pairs + 1):
                powers = (m - pairs + u_count, pairs - u_count)
                term = coefficient * math.comb(pairs, u_count) * Fraction(-1, 3)**u_count
                polynomial[powers] = polynomial.get(powers, Fraction(0)) + term
        polynomial = {key: value for key, value in polynomial.items() if value}
        assert polynomial == expected[m]
        answers[str(2 * m + 1)] = [{"u_degree": u, "S_degree": s, "coefficient": str(value)}
                                  for (u, s), value in sorted(polynomial.items())]
    # G_5 / mu = u^2/120 + uR/6 + R^2/2 is fixed by R -> -R-u/3.
    transformed_u2 = Fraction(1, 120) - Fraction(1, 18) + Fraction(1, 18)
    transformed_uR = -Fraction(1, 6) + Fraction(1, 3)
    assert transformed_u2 == Fraction(1, 120) and transformed_uR == Fraction(1, 6)
    return {"odd_moments_divided_by_Z_after_substitution": answers,
            "fifth_order_covariance_involution_checked_over_Q": True}


def monomial(z, powers):
    return math.prod(pow(a, p, P) for a, p in zip(z, powers)) % P


def cubic_rows(z):
    r = len(z)
    result = []
    for powers in many.compositions(3, r):
        row = []
        for s, t in itertools.combinations_with_replacement(range(r), 2):
            count = math.comb(powers[s], 2) if s == t else powers[s] * powers[t]
            if not count:
                row.append(0)
                continue
            remainder = list(powers)
            remainder[s] -= 1
            remainder[t] -= 1
            row.append(count * monomial(z, remainder) % P)
        result.append(row)
    return result


def solve_full_column_rank(rows, values):
    matrix, target = nmod_mat(rows, P), nmod_mat([[x] for x in values], P)
    chosen = base.pivot_columns(matrix.transpose())
    assert len(chosen) == matrix.ncols()
    square = nmod_mat([rows[i] for i in chosen], P)
    solution = square.inv() * nmod_mat([[values[i]] for i in chosen], P)
    assert (matrix * solution - target).rank() == 0
    return [int(solution[i, 0]) for i in range(solution.nrows())], base.full_rank_minor(matrix)


def response_coordinates(inputs, means, edges):
    _, keys, layers = many.responses(means, edges)
    basis = base.columns([layers[key] for key in keys])
    rows = base.pivot_columns(basis.transpose())
    assert len(rows) == len(keys)
    square = nmod_mat([[int(basis[i, j]) for j in range(len(keys))] for i in rows], P)
    values = square.inv() * nmod_mat([[tensor[i] for tensor in inputs] for i in rows], P)
    assert (basis * values - base.columns(inputs)).rank() == 0
    r = len(means)
    units = [tuple(int(s == t) for s in range(r)) for t in range(r)]
    z = [[int(values[keys.index(unit), j]) for unit in units] for j in range(len(inputs))]
    return keys, values, z


def two_output_parameters(keys, coordinates, z):
    r = len(z[0])
    first = next(i for i, v in enumerate(z) if any(v))
    second = next(i for i, v in enumerate(z) if any(v) and
                  any(v[s] * v[t] % P != z[first][s] * z[first][t] % P
                      for s, t in itertools.combinations_with_replacement(range(r), 2)))
    equations, values = [], []
    for j in [first, second]:
        for powers, row in zip(many.compositions(3, r), cubic_rows(z[j])):
            equations.append([monomial(z[j], powers)] + row)
            values.append(int(coordinates[keys.index(powers), j]))
    solution, minor = solve_full_column_rank(equations, values)
    assert solution[0]
    return solution[0], solution[1:], {"selected_outputs": [first, second], "calibration_minor": minor}


def one_output_parameters(keys, coordinates, z, output=0):
    """Use response degrees 1,3,5,7 of one actual output; no root solving."""
    r = len(z[output])
    h = next(i for i, value in enumerate(z[output]) if value)
    values = [int(coordinates[keys.index(powers), output]) for powers in many.compositions(3, r)]
    symmetric, minor = solve_full_column_rank(cubic_rows(z[output]), values)
    pairs = list(itertools.combinations_with_replacement(range(r), 2))
    scalar_z, scalar_s = z[output][h], symmetric[pairs.index((h, h))]
    key5 = tuple(5 if i == h else 0 for i in range(r))
    key7 = tuple(7 if i == h else 0 for i in range(r))
    fifth, seventh = int(coordinates[keys.index(key5), output]), int(coordinates[keys.index(key7), output])
    beta2 = 3 * pow(2, -1, P) * (15 * scalar_z * scalar_s**2 - fifth) * pow(pow(scalar_z, 5, P), -1, P) % P
    beta3 = 9 * pow(16, -1, P) * (seventh - 105 * scalar_z * scalar_s**3 + 14 * beta2 * scalar_z**5 * scalar_s) * pow(pow(scalar_z, 7, P), -1, P) % P
    assert beta2 and beta3 * beta3 % P == pow(beta2, 3, P)
    beta = beta3 * pow(beta2, -1, P) % P
    covariance = [(value - beta * pow(3, -1, P) * z[output][s] * z[output][t]) % P
                  for value, (s, t) in zip(symmetric, pairs)]
    return beta, covariance, {"selected_output": output, "scalar_coordinate": h,
                              "cubic_division_minor": minor, "beta_squared": beta2,
                              "beta_cubed": beta3, "beta": beta}


def rational_source(z, means, edges, beta, covariance):
    n, r = len(means[0]), len(means)
    m = (n - 1) // 2
    local = len(means[0][0])
    actual_means = [[[(pow(beta, m, P) if i == n - 1 else 1)
                      * sum(setting[s] * means[s][i][a] for s in range(r)) % P
                      for a in range(local)] for i in range(n)] for setting in z]
    edge_keys = [(i, j, a, b) for i, j in edges for a in range(local) for b in range(local)]
    quadratics = many.mean_quadratics(means, edge_keys)
    vector = [((pow(beta, m - 1, P) if j == n - 1 else pow(beta, -1, P))
               * (edges[i, j][a][b] + sum(k * q[index] for k, q in zip(covariance, quadratics)))) % P
              for index, (i, j, a, b) in enumerate(edge_keys)]
    return actual_means, base.edge_dictionary(vector, edge_keys)


def run_case(certificate, filename, case_index=None):
    means = certificate["source_mean_directions"]
    edges = {tuple(e["sites"]): e["weights"] for e in certificate["source_edges"]}
    r, n, local = len(means), len(means[0]), len(means[0][0])
    if r == 2:
        reconstruction = certificate["blind_edge_reconstruction"]
        frame = reconstruction["recovered_mean_directions"]
        representative = {tuple(e["sites"]): e["weights"] for e in reconstruction["recovered_edge_representative"]}
    else:
        frame = certificate["recovered_mean_directions"]
        representative = {tuple(e["sites"]): e["weights"] for e in certificate["recovered_edges"]}
    words, keys, layers = many.responses(means, edges)
    count = len(keys)
    settings = [[j, pow(j, n + 2, P)] if r == 2 else [pow(j, (n + 1)**s, P) for s in range(r)]
                for j in range(1, count + 1)]
    observations = [[sum(monomial(t, key) * layers[key][i] for key in keys) % P
                     for i in range(len(words))] for t in settings]
    assert base.columns(observations).rank() == count
    recovered_keys, coordinates, z = response_coordinates(observations, frame, representative)
    beta, covariance, calibration = two_output_parameters(recovered_keys, coordinates, z)
    recovered_means, recovered_edges = rational_source(z, frame, representative, beta, covariance)
    # A different recurrence checks every full tensor after calibration.
    assert [moments(mu, recovered_edges, P) for mu in recovered_means] == observations
    actual_means = [[[sum(t[s] * means[s][i][a] for s in range(r)) % P
                      for a in range(local)] for i in range(n)] for t in settings]
    gains = []
    for i in range(n):
        j, a = next((j, a) for j in range(count) for a in range(local) if actual_means[j][i][a])
        gains.append(recovered_means[j][i][a] * pow(actual_means[j][i][a], -1, P) % P)
    assert math.prod(gains) % P == 1
    assert all(recovered_means[j][i][a] == gains[i] * actual_means[j][i][a] % P
               for j in range(count) for i in range(n) for a in range(local))
    assert all(recovered_edges[i, j][a][b] == gains[i] * gains[j] * edges[i, j][a][b] % P
               for i, j in edges for a in range(local) for b in range(local))
    report = {"sites": n, "directions": r, "local_dimension": local, "observed_outputs": count,
              "prior_certificate": filename, "prior_case_index": case_index,
              "prior_certificate_sha256": hashlib.sha256(Path(__file__).with_name(filename).read_bytes()).hexdigest(),
              "two_output_calibration": calibration, "beta": beta, "covariance_coefficients": covariance,
              "all_observed_tensors_reproduced": True, "source_comparison_site_scalars": gains,
              "site_scalar_product": math.prod(gains) % P}
    if n >= 7:
        beta_one, covariance_one, one = one_output_parameters(recovered_keys, coordinates, z)
        assert (beta_one, covariance_one) == (beta, covariance)
        report["one_output_calibration"] = one
        report["one_output_equals_two_output_calibration"] = True
    if n == 5:
        mu = recovered_means[0]
        involuted = {(i, j): [[(-recovered_edges[i, j][a][b] - 2 * pow(3, -1, P) * mu[i][a] * mu[j][b]) % P
                              for b in range(local)] for a in range(local)] for i, j in edges}
        assert involuted != recovered_edges
        assert moments(mu, involuted, P) == observations[0]
        assert moments(recovered_means[1], involuted, P) != observations[1]
        report["fifth_order_involution"] = {"first_output_preserved": True, "second_output_changed": True,
                                            "mean_unchanged": True, "covariance_changed": True}
    if n == 3:
        values = [int(coordinates[recovered_keys.index(p), 0]) for p in many.compositions(3, r)]
        symmetric, _ = solve_full_column_rank(cubic_rows(z[0]), values)
        alternative_beta = next(value for value in range(1, P) if value != beta)
        alternative_covariance = [(value - alternative_beta * pow(3, -1, P) * z[0][s] * z[0][t]) % P
                                  for value, (s, t) in zip(symmetric, itertools.combinations_with_replacement(range(r), 2))]
        alternative_means, alternative_edges = rational_source([z[0]], frame, representative, alternative_beta, alternative_covariance)
        assert moments(alternative_means[0], alternative_edges, P) == observations[0]
        report["third_order_free_calibration"] = {"alternative_beta": alternative_beta, "first_output_preserved": True}
    return report


def run():
    directory = Path(__file__).parent
    cases = []
    for filename in ["two-direction-certificate.json", "two-direction-seven-certificate.json"]:
        cases.append(run_case(json.loads((directory / filename).read_text()), filename))
    filename = "many-direction-certificate.json"
    for i, case in enumerate(json.loads((directory / filename).read_text())["cases"]):
        cases.append(run_case(case, filename, i))
    return {"prime": P, "symbolic_identities": symbolic_identities(), "cases": cases}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

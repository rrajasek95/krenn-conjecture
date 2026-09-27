#!/usr/bin/env python3
"""Recover a response space and a calibrated Gaussian source from two tensors.

Five four-dimensional sites; exact arithmetic modulo 1009. Requires numpy
and python-flint via the repository .venv. Prints JSON and writes no files.
"""

import itertools
import json
import math
import random

import numpy as np
from flint import nmod_mat

import many_direction as many

base = many.base
P = many.P


def levi_tensor():
    tensor = np.zeros((16, 16), dtype=np.int64)
    for permutation in itertools.permutations(range(4)):
        sign = (-1) ** sum(permutation[i] > permutation[j] for i in range(4) for j in range(i + 1, 4))
        a, b, c, d = permutation
        tensor[4 * a + b, 4 * c + d] = sign
    return tensor


def pair_matrix(first, second, n):
    """Tensor-product exterior contraction, with local volume epsilon_0123=1."""
    size = 4**n
    # The signed integer contraction is bounded by 2^n (P-1)^2 per entry.
    # For the recorded cases this is well within signed int64 arithmetic.
    assert 2**n * (P - 1)**2 < 2**63
    matrix = np.outer(np.array(first, dtype=np.int64), np.array(second, dtype=np.int64))
    matrix = matrix.reshape([4] * (2 * n)).transpose([j for i in range(n) for j in (i, n + i)]).reshape([16] * n)
    epsilon = levi_tensor()
    for i in range(n):
        matrix = np.moveaxis(matrix, i, 0)
        matrix = np.tensordot(epsilon, matrix, axes=(1, 0))
        matrix = np.moveaxis(matrix, 0, i)
    matrix = matrix.reshape([4] * (2 * n)).transpose(list(range(0, 2 * n, 2)) + list(range(1, 2 * n, 2))).reshape(size, size) % P
    assert np.all((matrix + matrix.transpose()) % P == 0)
    return nmod_mat(matrix.tolist(), P)


def direct_entry(first, second, a, b):
    if any(x == y for x, y in zip(a, b)):
        return 0
    epsilon = levi_tensor()
    choices = [tuple(c for c in range(4) if c not in (x, y)) for x, y in zip(a, b)]
    total = 0
    for bits in itertools.product(range(2), repeat=len(a)):
        c_index, d_index, sign = 0, 0, 1
        for i, bit in enumerate(bits):
            c, d = choices[i][bit], choices[i][1 - bit]
            c_index = 4 * c_index + c
            d_index = 4 * d_index + d
            sign *= int(epsilon[4 * a[i] + b[i], 4 * c + d])
        total += sign * first[c_index] * second[d_index]
    return total % P


def exterior_pair(first, second, n):
    """B_2 in lexicographic local exterior bases (01,02,03,12,13,23)."""
    assert 2**n * (P - 1)**2 < 2**63
    value = np.outer(np.array(first, dtype=np.int64), np.array(second, dtype=np.int64))
    value = value.reshape([4] * (2 * n)).transpose([j for i in range(n) for j in (i, n + i)]).reshape([16] * n)
    wedge = np.zeros((6, 16), dtype=np.int64)
    for row, (a, b) in enumerate(itertools.combinations(range(4), 2)):
        wedge[row, 4 * a + b], wedge[row, 4 * b + a] = 1, -1
    for i in range(n):
        value = np.moveaxis(value, i, 0)
        value = np.tensordot(wedge, value, axes=(1, 0))
        value = np.moveaxis(value, 0, i)
    return (value.reshape(-1) % P).tolist()


def audit_alternative_means(inputs, terminal, means, ws):
    """Data-only ranks used to exclude alternative degenerate mean pairs."""
    n = len(ws[0])
    terminal_matrix = base.columns(terminal)
    lines, reports = [], []
    for tensor in inputs:
        restricted = base.columns([exterior_pair(tensor, vector, n) for vector in terminal])
        kernel = base.kernel_columns(restricted)
        assert len(kernel) == 1
        product = terminal_matrix * base.columns(kernel)
        vector = [int(product[i, 0]) for i in range(product.nrows())]
        assert all(len(many.local_supports([vector], ws, [i], 4)) == 1 for i in range(n))
        lines.append(vector)
        reports.append({"restricted_exterior_minor": base.full_rank_minor(restricted),
                        "kernel_terminal_coordinates": kernel[0],
                        "kernel_is_product_line": True})
    assert base.columns(lines).rank() == 2
    mean_tensors = base.pure_mean_tensors(means, ws)
    assert base.columns(mean_tensors).rank() == 2**n
    assert base.columns(mean_tensors + inputs).rank() == 2**n + 2
    return {"single_output_terminal_kernels": reports,
            "terminal_product_lines_distinct": True,
            "local_mean_tensor_space_dimension": 2**n,
            "dimension_after_adjoining_outputs": 2**n + 2}


def recover_edge_class(observations, means, ws):
    n, local = len(ws[0]), len(means[0][0])
    dimension = ((n + 1) // 2) * ((n + 3) // 2)
    cycle_count = (n - 1) * (n - 2) // 2
    zero = {(i, j): [[0] * local for _ in range(local)] for i, j in itertools.combinations(range(n), 2)}
    edge_keys, top, _ = base.edge_maps(means, zero, ws)
    project, _, _ = base.projector(observations)
    near = base.stack([project(g) for g in top])
    candidates = base.kernel_columns(near)
    assert len(candidates) == cycle_count + 4
    cycles, quadratics = base.cycle_vectors(means, edge_keys), base.mean_quadratics(means, edge_keys)
    invisible = cycles + quadratics
    assert base.columns(invisible).rank() == cycle_count + 3
    initial = next(q for q in candidates if base.columns(invisible + [q]).rank() == cycle_count + 4)
    initial_edges = base.edge_dictionary(initial, edge_keys)
    _, keys, initial_layers = many.responses(means, initial_edges)
    augmented = observations + base.pure_mean_tensors(means, ws)
    chosen = base.pivot_columns(base.columns(augmented))
    augmented = [augmented[i] for i in chosen]
    assert len(augmented) == dimension + 2**n - (n + 1)
    quotient, _, _ = base.projector(augmented)
    _, _, derivative = base.edge_maps(means, initial_edges, ws)
    coefficient = base.stack([quotient(g * base.columns(cycles)) for g in derivative])
    second_keys = [(n - 4 - a, a) for a in range(n - 3)]
    target = base.stack([quotient(base.columns([initial_layers[key]])) for key in second_keys])
    rows = base.pivot_columns(coefficient.transpose())
    assert len(rows) == cycle_count
    square = nmod_mat([[int(coefficient[i, j]) for j in range(cycle_count)] for i in rows], P)
    correction = square.inv() * nmod_mat([[-int(target[i, 0])] for i in rows], P)
    assert (coefficient * correction + target).rank() == 0
    vector = [(initial[z] + sum(cycles[j][z] * int(correction[j, 0]) for j in range(cycle_count))) % P
              for z in range(len(edge_keys))]
    edges = base.edge_dictionary(vector, edge_keys)
    _, _, recovered_layers = many.responses(means, edges)
    assert base.columns(observations + list(recovered_layers.values())).rank() == dimension
    return edges, {
        "near_terminal_constraint_minor": base.full_rank_minor(near),
        "cycle_correction_minor": base.full_rank_minor(coefficient),
        "response_space_reconstructed": True,
    }


def calibrate(first, second, means, edges, ws):
    n, local = len(ws[0]), len(means[0][0])
    m = (n - 1) // 2
    _, keys, layers = many.responses(means, edges)
    basis = base.columns([layers[key] for key in keys])
    rows = base.pivot_columns(basis.transpose())
    square = nmod_mat([[int(basis[i, j]) for j in range(len(keys))] for i in rows], P)
    observed = nmod_mat([[first[i], second[i]] for i in rows], P)
    coordinates = square.inv() * observed
    assert (basis * coordinates - base.columns([first, second])).rank() == 0
    z = [[int(coordinates[keys.index(key), j]) for key in [(1, 0), (0, 1)]] for j in range(2)]
    equations, values = [], []
    for j in range(2):
        for a, b in many.compositions(3, 2):
            powers = [a, b]
            row = [pow(z[j][0], a, P) * pow(z[j][1], b, P) % P]
            for s, t in itertools.combinations_with_replacement(range(2), 2):
                count = math.comb(powers[s], 2) if s == t else powers[s] * powers[t]
                if not count:
                    row.append(0)
                    continue
                remainder = powers[:]
                remainder[s] -= 1
                remainder[t] -= 1
                row.append(count * pow(z[j][0], remainder[0], P) * pow(z[j][1], remainder[1], P) % P)
            equations.append(row)
            values.append([int(coordinates[keys.index((a, b)), j])])
    coefficient, target = nmod_mat(equations, P), nmod_mat(values, P)
    rows = base.pivot_columns(coefficient.transpose())
    assert len(rows) == 4
    square = nmod_mat([equations[i] for i in rows], P)
    solution = square.inv() * nmod_mat([values[i] for i in rows], P)
    assert (coefficient * solution - target).rank() == 0
    beta, k00, k01, k11 = [int(solution[i, 0]) for i in range(4)]
    assert beta
    # A product-one site gauge removes the apparent n-th-root choice:
    # means have factors 1,...,1,beta^m, and edges have factors beta^-1
    # off the last site, beta^(m-1) at the last site.
    calibrated_means = [[[(pow(beta, m, P) if i == n - 1 else 1)
                          * sum(z[j][s] * means[s][i][a] for s in range(2)) % P
                          for a in range(local)] for i in range(n)] for j in range(2)]
    edge_keys = [(i, j, a, b) for i, j in edges for a in range(local) for b in range(local)]
    quadratics = base.mean_quadratics(means, edge_keys)
    corrected = [((pow(beta, m - 1, P) if j == n - 1 else pow(beta, -1, P))
                  * (edges[i, j][a][b] + k00 * quadratics[0][q] + k01 * quadratics[1][q] + k11 * quadratics[2][q])) % P
                 for q, (i, j, a, b) in enumerate(edge_keys)]
    calibrated_edges = base.edge_dictionary(corrected, edge_keys)
    _, recovered_keys, recovered_layers = many.responses(calibrated_means, calibrated_edges)
    recovered = [[sum(recovered_layers[key][q] for key in recovered_keys if key[1 - j] == 0) % P
                  for q in range(len(ws))] for j in range(2)]
    assert recovered == [first, second]
    return calibrated_means, calibrated_edges, {
        "degree_one_response_coordinates": z,
        "calibration_linear_system_minor": base.full_rank_minor(coefficient),
        "beta": beta, "mean_covariance_correction": [[k00, k01], [k01, k11]],
        "rational_calibration_distinguished_site": n - 1,
        "no_root_extraction_used": True,
        "both_input_tensors_reproduced_exactly": True,
    }


def recover_pair(inputs, n=5):
    """Blind inverse procedure: only the two tensors and their shape enter."""
    assert n == 5, "Generic kernel saturation is certified here at five sites."
    ws = list(itertools.product(range(4), repeat=n))
    matrix = pair_matrix(*inputs, n)
    kernel = base.kernel_columns(matrix)
    assert len(kernel) == 12
    principal_indices = base.pivot_columns(matrix)
    principal = nmod_mat([[int(matrix[i, j]) for j in principal_indices] for i in principal_indices], P)
    determinant = int(principal.det())
    assert determinant
    for i, j in [(0, 1023), (19, 917), (37, 498), (101, 678), (299, 704), (514, 411)]:
        assert int(matrix[i, j]) == direct_entry(*inputs, ws[i], ws[j])
    terminal, terminal_report = many.recover_terminal(kernel, ws, 2, all_sites=True)
    recovered_frame, synchronization = many.recover_means(terminal, ws, 2)
    alternative_audit = audit_alternative_means(inputs, terminal, recovered_frame, ws)
    recovered_class, edge_report = recover_edge_class(kernel, recovered_frame, ws)
    calibrated_means, calibrated_edges, calibration = calibrate(*inputs, recovered_frame, recovered_class, ws)
    return calibrated_means, calibrated_edges, {
        "number_of_observed_tensors": 2,
        "pair_exterior_matrix_rank": len(ws) - len(kernel),
        "pair_exterior_kernel_dimension": len(kernel),
        "principal_minor_indices": principal_indices,
        "principal_minor_determinant": determinant,
        "terminal_recovery": terminal_report, "mean_synchronization": synchronization,
        "alternative_mean_audit": alternative_audit,
        "edge_class_recovery": edge_report, "calibration": calibration,
    }


def run():
    n, local, seed = 5, 4, 281927
    rng = random.Random(seed)
    means = [[[rng.randrange(P) for _ in range(local)] for _ in range(n)] for _ in range(2)]
    edges = {(i, j): [[rng.randrange(P) for _ in range(local)] for _ in range(local)]
             for i, j in itertools.combinations(range(n), 2)}
    ws, keys, layers = many.responses(means, edges)
    settings = [(1, 2), (3, 5)]
    inputs = [[sum(pow(t, a, P) * pow(s, b, P) * layers[a, b][q] for a, b in keys) % P
               for q in range(len(ws))] for t, s in settings]
    calibrated_means, calibrated_edges, report = recover_pair(inputs, n)
    # Now use the original parameters to independently compare the answer.
    source_span = [layers[key] for key in keys]
    assert base.columns(source_span).rank() == 12
    assert (pair_matrix(*inputs, n) * base.columns(source_span)).rank() == 0
    actual_means = [[[sum(setting[s] * means[s][i][a] for s in range(2)) % P
                     for a in range(local)] for i in range(n)] for setting in settings]
    site_scalars = []
    for i in range(n):
        j, a = next((j, a) for j in range(2) for a in range(local) if actual_means[j][i][a])
        scalar = calibrated_means[j][i][a] * pow(actual_means[j][i][a], -1, P) % P
        assert scalar
        assert all(calibrated_means[j][i][a] == scalar * actual_means[j][i][a] % P
                   for j in range(2) for a in range(local))
        site_scalars.append(scalar)
    assert math.prod(site_scalars) % P == 1
    assert all(calibrated_edges[i, j][a][b] == site_scalars[i] * site_scalars[j] * edges[i, j][a][b] % P
               for i, j in edges for a in range(local) for b in range(local))
    return {
        "sites": n, "local_dimension": local, "prime": P, "seed": seed,
        **report,
        "kernel_is_exact_response_space": True,
        "source_comparison_site_scalars": site_scalars,
        "site_scalar_product": math.prod(site_scalars) % P,
        "source_recovered_up_to_product_one_site_scalings": True,
        "input_tensors": inputs,
        "source_mean_basis": means, "source_input_settings": settings,
        "source_edges": [{"sites": list(edge), "weights": value} for edge, value in edges.items()],
        "recovered_actual_means": calibrated_means,
        "recovered_actual_edges": [{"sites": list(edge), "weights": value} for edge, value in calibrated_edges.items()],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

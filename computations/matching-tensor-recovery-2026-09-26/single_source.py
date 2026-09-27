#!/usr/bin/env python3
"""Recover one-direction covariances from response spans and single outputs.

Five and seven three-dimensional sites; exact arithmetic modulo 1009.
Requires numpy and python-flint. Prints JSON, writes no files.
"""

import itertools
import json
import math
import random

import numpy as np
from flint import nmod_mat

import many_direction as many
import calibrated_span as calibrated
from audit_pair_observation import moments

base, P = many.base, many.P


def transform_columns(vectors, maps):
    n, local, count = len(maps), maps[0].ncols(), len(vectors)
    values = np.array(list(zip(*vectors)), dtype=np.int64).reshape([local] * n + [count])
    for i, linear in enumerate(maps):
        values = np.moveaxis(values, i, 0)
        values = np.tensordot(np.array(linear.tolist(), dtype=np.int64), values, axes=(1, 0)) % P
        values = np.moveaxis(values, 0, i)
    values = values.reshape(-1, count)
    return [values[:, j].tolist() for j in range(count)]


def edge_data(n, local=3):
    words = list(itertools.product(range(local), repeat=n))
    index = {word: i for i, word in enumerate(words)}
    keys = [(i, j, a, b) for i, j in itertools.combinations(range(n), 2)
            for a in range(local) for b in range(local)]
    key_index = {key: q for q, key in enumerate(keys)}
    phi = [[0] * len(keys) for _ in words]
    for q, (i, j, a, b) in enumerate(keys):
        word = [0] * n
        word[i], word[j] = a, b
        phi[index[tuple(word)]][q] = 1
    flows = []
    for i in range(n):
        other = [j for j in range(n) if j != i]
        anchor = other[0]
        for colour in range(1, local):
            for j in other[1:]:
                vector = [0] * len(keys)
                for k, sign in [(j, 1), (anchor, -1)]:
                    key = (i, k, colour, 0) if i < k else (k, i, 0, colour)
                    vector[key_index[key]] = sign % P
                flows.append(vector)
    mean_indices = [key_index[i, j, 0, 0] for i, j in itertools.combinations(range(n), 2)]
    mean_kernel = []
    for q in mean_indices[1:]:
        vector = [0] * len(keys)
        vector[q], vector[mean_indices[0]] = 1, P - 1
        mean_kernel.append(vector)
    mean_square = [int(a == 0 and b == 0) for i, j, a, b in keys]
    return words, index, keys, nmod_mat(phi, P), flows, mean_kernel, mean_square


def derivative(vector, n, data):
    words, index, keys, _, _, _, _ = data
    rows = [[0] * len(keys) for _ in words]
    nonzero = [(key, value) for key, value in zip(keys, vector) if value]
    for q, (i, j, a, b) in enumerate(keys):
        for (k, l, c, d), value in nonzero:
            if len({i, j, k, l}) < 4:
                continue
            word = [0] * n
            word[i], word[j], word[k], word[l] = a, b, c, d
            w = index[tuple(word)]
            rows[w][q] = (rows[w][q] + value) % P
    return nmod_mat(rows, P)


def correct(matrix, target):
    rows = base.pivot_columns(matrix.transpose())
    assert len(rows) == matrix.ncols()
    square = nmod_mat([[int(matrix[i, j]) for j in range(matrix.ncols())] for i in rows], P)
    solution = square.inv() * nmod_mat([[-int(target[i, 0])] for i in rows], P)
    assert (matrix * solution + target).rank() == 0
    return solution


def recover_edges(response_space, n):
    data = edge_data(n)
    words, _, keys, phi, flows, mean_kernel, mean_square = data
    project, _, _ = base.projector(response_space)
    constraints = project(phi)
    candidates = base.kernel_columns(constraints)
    invisible = [mean_square] + flows + mean_kernel
    expected = 2 + len(flows) + len(mean_kernel)
    assert len(candidates) == expected
    assert base.columns(invisible).rank() == expected - 1
    initial = next(v for v in candidates if base.columns(invisible + [v]).rank() == expected)
    # Quotient first by all coordinates with at most two outside-mean factors.
    high = [i for i, word in enumerate(words) if sum(a != 0 for a in word) >= 3]
    high_space = [[v[i] for i in high] for v in response_space]
    chosen = base.pivot_columns(base.columns(high_space))
    assert len(chosen) == len(response_space) - 2
    high_project, _, _ = base.projector([high_space[i] for i in chosen])

    def project_high(matrix):
        restricted = nmod_mat([[int(matrix[i, j]) for j in range(matrix.ncols())] for i in high], P)
        return high_project(restricted)

    initial_derivative = derivative(initial, n, data)
    flow_matrix = project_high(initial_derivative * base.columns(flows))
    target = project_high(initial_derivative * base.columns([initial]) * pow(2, -1, P))
    correction = correct(flow_matrix, target)
    vector = [(value + sum(flow[q] * int(correction[j, 0]) for j, flow in enumerate(flows))) % P
              for q, value in enumerate(initial)]
    second_derivative = derivative(vector, n, data)
    mean_matrix = project(second_derivative * base.columns(mean_kernel))
    target = project(second_derivative * base.columns([vector]) * pow(2, -1, P))
    correction = correct(mean_matrix, target)
    final = [(value + sum(kernel[q] * int(correction[j, 0]) for j, kernel in enumerate(mean_kernel))) % P
             for q, value in enumerate(vector)]
    edges = base.edge_dictionary(final, keys)
    frame = [[[1, 0, 0] for _ in range(n)]]
    _, _, layers = many.responses(frame, edges)
    assert base.columns(response_space + list(layers.values())).rank() == len(response_space)
    return edges, {"one_edge_constraint_minor": base.full_rank_minor(constraints),
                   "one_outside_flow_dimension": len(flows),
                   "flow_correction_minor": base.full_rank_minor(flow_matrix),
                   "pure_mean_kernel_dimension": len(mean_kernel),
                   "mean_correction_minor": base.full_rank_minor(mean_matrix),
                   "response_space_reconstructed": True}


def recover(tensor, n):
    words = list(itertools.product(range(3), repeat=n))
    exterior = nmod_mat(base.exterior.dense(base.exterior.exterior_sparse(tensor, words, P)), P)
    kernel = base.kernel_columns(exterior)
    principal_indices = base.pivot_columns(exterior)
    principal = nmod_mat([[int(exterior[i, j]) for j in principal_indices] for i in principal_indices], P)
    principal_determinant = int(principal.det())
    assert principal_determinant
    terminal, terminal_report = many.recover_terminal(kernel, words, 1, all_sites=True)
    factors = [many.local_supports(terminal, words, [i], 3)[0] for i in range(n)]
    bases = []
    for factor in factors:
        pivot = next(i for i, value in enumerate(factor) if value)
        basis = base.columns([factor] + [[int(a == c) for a in range(3)] for c in range(3) if c != pivot])
        assert basis.det()
        bases.append(basis)
    changed = transform_columns(kernel + [tensor], [b.inv() for b in bases])
    transformed_kernel, transformed_tensor = changed[:-1], changed[-1]
    outside_rows = [i for i, word in enumerate(words) if all(a != 0 for a in word)]
    outside = nmod_mat([[v[i] for v in transformed_kernel] for i in outside_rows], P)
    remaining = base.kernel_columns(outside)
    assert len(remaining) == (n + 1) // 2
    response_matrix = base.columns(transformed_kernel) * base.columns(remaining)
    response_space = [[int(response_matrix[i, j]) for i in range(len(words))] for j in range(len(remaining))]
    assert max(sum(a != 0 for a in word) for word, value in zip(words, transformed_tensor) if value) == n - 1
    representative, edge_report = recover_edges(response_space, n)
    frame = [[[1, 0, 0] for _ in range(n)]]
    keys, coordinates, z = calibrated.response_coordinates([transformed_tensor], frame, representative)
    candidates = []
    if n >= 7:
        beta, covariance, calibration_report = calibrated.one_output_parameters(keys, coordinates, z)
        mu, edges = calibrated.rational_source(z, frame, representative, beta, covariance)
        candidates.append((mu[0], edges))
    else:
        assert n == 5
        scalar = z[0][0]
        s = int(coordinates[keys.index((3,)), 0]) * pow(3 * scalar, -1, P) % P
        fifth = int(coordinates[keys.index((5,)), 0])
        beta2 = 3 * pow(2, -1, P) * (15 * scalar * s**2 - fifth) * pow(pow(scalar, 5, P), -1, P) % P
        roots = [a for a in range(1, P) if a * a % P == beta2]
        assert len(roots) == 2
        for beta in roots:
            k = (s - beta * pow(3, -1, P) * scalar * scalar) % P
            mu, edges = calibrated.rational_source(z, frame, representative, beta, [k])
            candidates.append((mu[0], edges))
        calibration_report = {"beta_squared": beta2, "beta_roots": roots,
                              "actual_means_identical_between_branches": candidates[0][0] == candidates[1][0]}
    restored = []
    for mu, edges in candidates:
        assert moments(mu, edges, P) == transformed_tensor
        original_means = [[int(value[0]) for value in (bases[i] * nmod_mat([[a] for a in mu[i]], P)).tolist()]
                          for i in range(n)]
        original_edges = {(i, j): (bases[i] * nmod_mat(block, P) * bases[j].transpose()).tolist()
                          for (i, j), block in edges.items()}
        original_edges = {edge: [[int(a) for a in row] for row in block] for edge, block in original_edges.items()}
        assert moments(original_means, original_edges, P) == tensor
        restored.append((original_means, original_edges))
    return restored, {"exterior_kernel_dimension": len(kernel),
                      "exterior_principal_minor_indices": principal_indices,
                      "exterior_principal_minor_determinant": principal_determinant,
                      "terminal_recovery": terminal_report,
                      "all_outside_constraint_rank": outside.rank(),
                      "all_outside_constraint_minor": base.full_rank_minor(outside),
                      "completed_one_direction_response_dimension": len(response_space),
                      "edge_recovery": edge_report, "calibration": calibration_report,
                      "all_candidate_outputs_reproduced": True}


def run(n):
    rng = random.Random(90127)
    means = [[rng.randrange(P) for _ in range(3)] for _ in range(n)]
    edges = {(i, j): [[rng.randrange(P) for _ in range(3)] for _ in range(3)]
             for i, j in itertools.combinations(range(n), 2)}
    tensor = moments(means, edges, P)
    answers, report = recover(tensor, n)
    comparisons = []
    for recovered_means, recovered_edges in answers:
        gains = []
        for i in range(n):
            a = next(a for a in range(3) if means[i][a])
            gain = recovered_means[i][a] * pow(means[i][a], -1, P) % P
            assert all(recovered_means[i][a] == gain * means[i][a] % P for a in range(3))
            gains.append(gain)
        assert math.prod(gains) % P == 1
        original = all(recovered_edges[i, j][a][b] == gains[i] * gains[j] * edges[i, j][a][b] % P
                       for i, j in edges for a in range(3) for b in range(3))
        involution = all(recovered_edges[i, j][a][b] == gains[i] * gains[j] * (-edges[i, j][a][b] - 2 * pow(3, -1, P) * means[i][a] * means[j][b]) % P
                        for i, j in edges for a in range(3) for b in range(3))
        assert original or (n == 5 and involution)
        comparisons.append({"site_scalars": gains, "site_scalar_product": math.prod(gains) % P,
                            "matches_original_covariance": original, "matches_fifth_order_involution": involution})
    assert sum(c["matches_original_covariance"] for c in comparisons) == 1
    return {"sites": n, "local_dimension": 3, "seed": 90127, "prime": P,
            **report, "source_comparisons": comparisons,
            "source_means": means, "source_edges": [{"sites": list(k), "weights": v} for k, v in edges.items()],
            "recovered_candidates": [{"means": mu, "edges": [{"sites": list(k), "weights": v} for k, v in es.items()]}
                                     for mu, es in answers]}


if __name__ == "__main__":
    print(json.dumps({"cases": [run(5), run(7)]}, indent=2))

#!/usr/bin/env python3
"""Exact experiments for recovering a two-direction response space.

Run with .venv/bin/python (python-flint). Prints JSON; writes no files.
"""

import itertools
import json
from pathlib import Path
import random
import sys

from flint import nmod_mat

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "matching-tensor-exterior-2026-09-26"))
import verify as exterior

P = 1009


def source(n=5, seed=72109):
    rng = random.Random(seed)
    means = [[[rng.randrange(P) for _ in range(3)] for _ in range(n)] for _ in range(2)]
    edges = {
        e: [[rng.randrange(P) for _ in range(3)] for _ in range(3)]
        for e in itertools.combinations(range(n), 2)
    }
    return means, edges


def monomer_polynomial(means, sites, word):
    polynomial = [1]
    for i in sites:
        updated = [0] * (len(polynomial) + 1)
        for a, value in enumerate(polynomial):
            updated[a] = (updated[a] + value * means[1][i][word[i]]) % P
            updated[a + 1] = (updated[a + 1] + value * means[0][i][word[i]]) % P
        polynomial = updated
    return polynomial


def responses(means, edges):
    n = len(means[0])
    ws = exterior.words(n)
    keys = [(a, k - a) for k in range(1, n + 1, 2) for a in range(k + 1)]
    layers = {key: [0] * len(ws) for key in keys}
    for singles, pairs in exterior.matchings(list(range(n))):
        for z, word in enumerate(ws):
            value = 1
            for i, j in pairs:
                value = value * edges[i, j][word[i]][word[j]] % P
            for a, coefficient in enumerate(monomer_polynomial(means, singles, word)):
                key = (a, len(singles) - a)
                layers[key][z] = (layers[key][z] + value * coefficient) % P
    return ws, keys, layers


def columns(vectors):
    return nmod_mat(list(map(list, zip(*vectors))), P)


def pivot_columns(matrix):
    reduced, rank = matrix.rref()
    return [next(j for j in range(matrix.ncols()) if reduced[i, j]) for i in range(rank)]


def kernel_columns(matrix):
    kernel, dimension = matrix.nullspace()
    return [[int(kernel[i, j]) for i in range(kernel.nrows())] for j in range(dimension)]


def projector(basis):
    """Return a map to a quotient chart, and the chart's pivot rows."""
    matrix = columns(basis)
    rows = pivot_columns(matrix.transpose())
    assert len(rows) == len(basis)
    square = nmod_mat([[int(matrix[i, j]) for j in range(matrix.ncols())] for i in rows], P)
    interpolation = matrix * square.inv()

    def project(other):
        selected = nmod_mat([[int(other[i, j]) for j in range(other.ncols())] for i in rows], P)
        return other - interpolation * selected

    return project, rows, int(square.det())


def independent_rows(rows):
    """Yield indices of independent rows, with incremental exact elimination."""
    echelon = {}
    for index, row in enumerate(rows):
        residual = [x % P for x in row]
        for pivot, previous in sorted(echelon.items()):
            factor = residual[pivot]
            if factor:
                residual = [(x - factor * y) % P for x, y in zip(residual, previous)]
        pivot = next((j for j, value in enumerate(residual) if value), None)
        if pivot is not None:
            inverse = pow(residual[pivot], -1, P)
            echelon[pivot] = [x * inverse % P for x in residual]
            yield index


def recover_terminal(observations, ws):
    """Input consists only of tensors, with no source parameters or labels."""
    d = len(observations)
    n = len(ws[0])
    assert columns(observations).rank() == d
    monomials = list(itertools.combinations_with_replacement(range(d), 2))
    target_rank = len(monomials) - (2 * n + 1)
    tails = 3 ** (n - 1)
    selected, labels = [], []
    echelon = {}
    for i, j in itertools.combinations(range(3), 2):
        for c, e in itertools.combinations(range(tails), 2):
            ix = (i * tails + c, i * tails + e, j * tails + c, j * tails + e)
            row = []
            for h, k in monomials:
                value = observations[h][ix[0]] * observations[k][ix[3]] - observations[h][ix[1]] * observations[k][ix[2]]
                if h != k:
                    value += observations[k][ix[0]] * observations[h][ix[3]] - observations[k][ix[1]] * observations[h][ix[2]]
                row.append(value % P)
            residual = row[:]
            for pivot, previous in sorted(echelon.items()):
                factor = residual[pivot]
                if factor:
                    residual = [(x - factor * y) % P for x, y in zip(residual, previous)]
            pivot = next((z for z, value in enumerate(residual) if value), None)
            if pivot is not None:
                inv = pow(residual[pivot], -1, P)
                echelon[pivot] = [value * inv % P for value in residual]
                selected.append(row)
                labels.append([i, j, c, e])
            if len(selected) == target_rank:
                break
        if len(selected) == target_rank:
            break
    assert len(selected) == target_rank
    coefficient_matrix = nmod_mat(selected, P)
    qbasis = kernel_columns(coefficient_matrix)
    image_columns = []
    for q in qbasis:
        symmetric = [[0] * d for _ in range(d)]
        for (i, j), value in zip(monomials, q):
            symmetric[i][j] = symmetric[j][i] = value
        image_columns.extend(list(map(list, zip(*symmetric))))
    chosen = pivot_columns(columns(image_columns))
    coordinates = [image_columns[i] for i in chosen]
    assert len(coordinates) == n + 1
    terminal_matrix = columns(observations) * columns(coordinates)
    terminal = [[int(terminal_matrix[i, j]) for i in range(len(ws))] for j in range(n + 1)]
    minor_columns = pivot_columns(coefficient_matrix)
    square = nmod_mat([[row[j] for j in minor_columns] for row in selected], P)
    return terminal, {
        "observation_dimension": d,
        "quadratic_columns": len(monomials),
        "quadratic_coefficient_rank": target_rank,
        "quadratic_kernel_dimension": len(qbasis),
        "recovered_terminal_dimension": len(terminal),
        "selected_flattening_minor_labels": labels,
        "selected_coefficient_columns": minor_columns,
        "coefficient_minor_determinant": int(square.det()),
    }


def edge_maps(means, edges, ws):
    """One-edge response maps and derivatives of the two-edge layers."""
    n = len(means[0])
    edge_keys = [(i, j, a, b) for i, j in edges for a in range(3) for b in range(3)]
    edge_index = {key: z for z, key in enumerate(edge_keys)}
    top = [[[0] * len(edge_keys) for _ in ws] for _ in range(n - 1)]
    for z, word in enumerate(ws):
        for i, j in edges:
            coefficient = monomer_polynomial(means, [v for v in range(n) if v not in (i, j)], word)
            c = edge_index[i, j, word[i], word[j]]
            for a, value in enumerate(coefficient):
                top[a][z][c] = value
    derivative = [[[0] * len(edge_keys) for _ in ws] for _ in range(n - 3)]
    for singles, pairs in exterior.matchings(list(range(n))):
        if len(singles) != n - 4:
            continue
        for z, word in enumerate(ws):
            polynomial = monomer_polynomial(means, singles, word)
            for which, (u, v) in enumerate(pairs):
                x, y = pairs[1 - which]
                c = edge_index[u, v, word[u], word[v]]
                for s, coefficient in enumerate(reversed(polynomial)):
                    derivative[s][z][c] = (derivative[s][z][c] + coefficient * edges[x, y][word[x]][word[y]]) % P
    return edge_keys, [nmod_mat(x, P) for x in top], [nmod_mat(x, P) for x in derivative]


def local_supports(terminal, ws, sites):
    """Span of contractions onto a chosen set of tensor factors."""
    other = [i for i in range(len(ws[0])) if i not in sites]
    local_words = list(itertools.product(range(3), repeat=len(sites)))
    other_words = list(itertools.product(range(3), repeat=len(other)))
    word_index = {word: z for z, word in enumerate(ws)}
    contractions = []
    for tensor in terminal:
        for tail in other_words:
            vector = []
            for head in local_words:
                word = [0] * len(ws[0])
                for i, c in zip(sites, head):
                    word[i] = c
                for i, c in zip(other, tail):
                    word[i] = c
                vector.append(tensor[word_index[tuple(word)]])
            contractions.append(vector)
    chosen = pivot_columns(columns(contractions))
    return [contractions[i] for i in chosen]


def recover_means(terminal, ws):
    """Recover synchronized local two-planes, up to individual site scalars."""
    n = len(ws[0])
    supports = [local_supports(terminal, ws, [i]) for i in range(n)]
    assert all(len(basis) == 2 for basis in supports)
    local_matrices = [columns(basis) for basis in supports]
    inverses = []
    selected_rows = []
    for matrix in local_matrices:
        rows = pivot_columns(matrix.transpose())
        square = nmod_mat([[int(matrix[i, j]) for j in range(2)] for i in rows], P)
        inverses.append(square.inv())
        selected_rows.append(rows)
    synchronized = [local_matrices[0]]
    form_determinants = []
    for i in range(1, n):
        pair_support = local_supports(terminal, ws, [0, i])
        assert len(pair_support) == 3
        coefficient_rows = []
        for vector in pair_support:
            square = nmod_mat([[vector[a * 3 + b] for b in selected_rows[i]] for a in selected_rows[0]], P)
            coefficient_matrix = inverses[0] * square * inverses[i].transpose()
            coefficient_rows.append([int(coefficient_matrix[a, b]) for a in range(2) for b in range(2)])
        annihilator = kernel_columns(nmod_mat(coefficient_rows, P))
        assert len(annihilator) == 1
        bilinear = nmod_mat([annihilator[0][:2], annihilator[0][2:]], P)
        assert bilinear.det()
        form_determinants.append(int(bilinear.det()))
        rotation = nmod_mat([[0, -1], [1, 0]], P)
        synchronized.append(local_matrices[i] * rotation * bilinear.transpose())
    means = [[[int(synchronized[i][a, s]) for a in range(3)] for i in range(n)] for s in range(2)]
    zero_edges = {(i, j): [[0] * 3 for _ in range(3)] for i, j in itertools.combinations(range(n), 2)}
    _, keys, layers = responses(means, zero_edges)
    generated = [layers[k] for k in keys if sum(k) == n]
    assert columns(terminal + generated).rank() == n + 1
    return means, {"local_support_dimensions": [len(b) for b in supports],
                   "pair_annihilator_determinants": form_determinants,
                   "synchronized_terminal_space_matches": True}


def cycle_vectors(means, edge_keys):
    cycles = []
    for a, b in itertools.combinations(range(1, len(means[0])), 2):
        flow = {(0, a): 1, (a, b): 1, (0, b): -1}
        cycles.append([
            flow.get((i, j), 0) * (means[0][i][c] * means[1][j][d] - means[1][i][c] * means[0][j][d]) % P
            for i, j, c, d in edge_keys
        ])
    return cycles


def mean_quadratics(means, edge_keys):
    return [
        [(means[0][i][c] * means[0][j][d]) % P for i, j, c, d in edge_keys],
        [(means[0][i][c] * means[1][j][d] + means[1][i][c] * means[0][j][d]) % P for i, j, c, d in edge_keys],
        [(means[1][i][c] * means[1][j][d]) % P for i, j, c, d in edge_keys],
    ]


def edge_dictionary(vector, edge_keys):
    edges = {(i, j): [[0] * 3 for _ in range(3)] for i, j, _, _ in edge_keys}
    for value, (i, j, a, b) in zip(vector, edge_keys):
        edges[i, j][a][b] = value % P
    return edges


def pure_mean_tensors(means, ws):
    vectors = []
    for bits in itertools.product(range(2), repeat=len(ws[0])):
        tensor = []
        for word in ws:
            value = 1
            for i, colour in enumerate(word):
                value = value * means[bits[i]][i][colour] % P
            tensor.append(value)
        vectors.append(tensor)
    return vectors


def stack(matrices):
    return nmod_mat([list(map(int, row)) for matrix in matrices for row in matrix.tolist()], P)


def full_rank_minor(matrix):
    cols = pivot_columns(matrix)
    rows = pivot_columns(matrix.transpose())
    assert len(cols) == len(rows)
    square = nmod_mat([[int(matrix[i, j]) for j in cols] for i in rows], P)
    return {"rank": len(cols), "rows": rows, "columns": cols, "determinant": int(square.det())}


def recover_edges(observations, recovered_means, ws):
    """Recover a quadratic representative using only linear solves.

    Its scale and three mean-quadratic terms are not observable from the span.
    """
    n = len(ws[0])
    dimension = ((n + 1) // 2) * ((n + 3) // 2)
    cycle_count = (n - 1) * (n - 2) // 2
    zero = {(i, j): [[0] * 3 for _ in range(3)] for i, j in itertools.combinations(range(n), 2)}
    edge_keys, top, _ = edge_maps(recovered_means, zero, ws)
    project, _, _ = projector(observations)
    near = stack([project(g) for g in top])
    near_basis = kernel_columns(near)
    assert len(near_basis) == cycle_count + 4
    cycles = cycle_vectors(recovered_means, edge_keys)
    quadratics = mean_quadratics(recovered_means, edge_keys)
    invisible = cycles + quadratics
    assert columns(invisible).rank() == cycle_count + 3
    initial = next(q for q in near_basis if columns(invisible + [q]).rank() == cycle_count + 4)
    initial_edges = edge_dictionary(initial, edge_keys)
    _, keys, initial_layers = responses(recovered_means, initial_edges)
    augmented = observations + pure_mean_tensors(recovered_means, ws)
    chosen = pivot_columns(columns(augmented))
    augmented = [augmented[i] for i in chosen]
    assert len(augmented) == dimension + 2**n - (n + 1)
    quotient, _, _ = projector(augmented)
    _, _, derivative = edge_maps(recovered_means, initial_edges, ws)
    cycle_matrix = columns(cycles)
    coefficient_matrix = stack([quotient(g * cycle_matrix) for g in derivative])
    second_keys = [(n - 4 - a, a) for a in range(n - 3)]
    target = stack([quotient(columns([initial_layers[key]])) for key in second_keys])
    rows = pivot_columns(coefficient_matrix.transpose())
    assert len(rows) == cycle_count
    square = nmod_mat([[int(coefficient_matrix[i, j]) for j in range(cycle_count)] for i in rows], P)
    rhs = nmod_mat([[-int(target[i, 0])] for i in rows], P)
    solution = square.inv() * rhs
    assert (coefficient_matrix * solution + target).rank() == 0
    recovered = [
        (initial[z] + sum(cycles[j][z] * int(solution[j, 0]) for j in range(cycle_count))) % P
        for z in range(len(edge_keys))
    ]
    edges = edge_dictionary(recovered, edge_keys)
    _, _, final_layers = responses(recovered_means, edges)
    assert columns(observations + list(final_layers.values())).rank() == dimension
    return edges, {
        "near_terminal_constraint_minor": full_rank_minor(near),
        "cycle_removal_minor": full_rank_minor(coefficient_matrix),
        "cycle_correction": [int(solution[j, 0]) for j in range(cycle_count)],
        "reconstructed_response_space_matches": True,
        "recovered_mean_directions": recovered_means,
        "recovered_edge_representative": [{"sites": list(edge), "weights": value} for edge, value in edges.items()],
    }


def verify_gauge(source_means, source_edges, recovered_means, recovered_edges):
    """Independent comparison after the blind reconstruction has finished."""
    n = len(source_means[0])
    original = [columns([source_means[s][i] for s in range(2)]) for i in range(n)]
    recovered = [columns([recovered_means[s][i] for s in range(2)]) for i in range(n)]
    rows = pivot_columns(original[0].transpose())
    a = nmod_mat([[int(original[0][i, j]) for j in range(2)] for i in rows], P)
    b = nmod_mat([[int(recovered[0][i, j]) for j in range(2)] for i in rows], P)
    change = a.inv() * b
    scalars = []
    for i in range(n):
        expected = original[i] * change
        u, v = next((u, v) for u in range(3) for v in range(2) if expected[u, v])
        scalar = int(recovered[i][u, v]) * pow(int(expected[u, v]), -1, P) % P
        assert scalar and (recovered[i] - expected * scalar).rank() == 0
        scalars.append(scalar)
    edge_keys = [(i, j, a, b) for i, j in source_edges for a in range(3) for b in range(3)]
    transformed = [scalars[i] * scalars[j] * source_edges[i, j][a][b] % P for i, j, a, b in edge_keys]
    answer = [recovered_edges[i, j][a][b] for i, j, a, b in edge_keys]
    gauge_matrix = columns([transformed] + mean_quadratics(recovered_means, edge_keys))
    rows = pivot_columns(gauge_matrix.transpose())
    assert len(rows) == 4
    square = nmod_mat([[int(gauge_matrix[i, j]) for j in range(4)] for i in rows], P)
    rhs = nmod_mat([[answer[i]] for i in rows], P)
    coefficients = square.inv() * rhs
    assert coefficients[0, 0] and (gauge_matrix * coefficients - columns([answer])).rank() == 0
    return {"common_mean_basis_change": [[int(change[i, j]) for j in range(2)] for i in range(2)],
            "site_scalars": scalars,
            "quadratic_scale_and_three_mean_quadratic_coefficients": [int(coefficients[i, 0]) for i in range(4)],
            "reconstruction_differs_only_by_proved_gauges": True}


def run(n=5):
    means, edges = source(n)
    ws, keys, layers = responses(means, edges)
    basis = [layers[key] for key in keys]
    d = len(keys)
    evaluation = nmod_mat([[pow(j, a + (n + 2) * b, P) for a, b in keys] for j in range(1, d + 1)], P)
    assert evaluation.det()
    output_matrix = columns(basis) * evaluation.transpose()
    observations = [[int(output_matrix[i, j]) for i in range(len(ws))] for j in range(d)]
    terminal, recovery = recover_terminal(observations, ws)
    actual_terminal = [layers[k] for k in keys if sum(k) == n]
    assert columns(terminal + actual_terminal).rank() == n + 1
    recovery["terminal_space_matches_source"] = True
    recovery["evaluation_matrix_determinant"] = int(evaluation.det())
    recovered_means, mean_report = recover_means(terminal, ws)
    recovered_edges, blind_edge_report = recover_edges(observations, recovered_means, ws)
    gauge_report = verify_gauge(means, edges, recovered_means, recovered_edges)

    project, chart_rows, chart_det = projector(basis)
    edge_keys, top, derivative = edge_maps(means, edges, ws)
    constraints = [project(g) for g in top]
    near = stack(constraints)
    all_constraints = constraints + [project(g) for g in derivative]
    tangent = stack(all_constraints)
    raw_top = stack(top)
    cycles = cycle_vectors(means, edge_keys)
    cycle_count = (n - 1) * (n - 2) // 2
    assert columns(cycles).rank() == cycle_count
    assert all((g * columns(cycles)).rank() == 0 for g in top)
    augmented = basis + pure_mean_tensors(means, ws)
    chosen = pivot_columns(columns(augmented))
    augmented = [augmented[i] for i in chosen]
    quotient, _, _ = projector(augmented)
    detection = stack([quotient(g * columns(cycles)) for g in derivative])
    assert detection.rank() == cycle_count
    edge_report = {
        "edge_parameters": len(edge_keys),
        "near_terminal_constraint_rank": near.rank(),
        "near_terminal_ambiguity_dimension": len(edge_keys) - near.rank(),
        "raw_near_terminal_map_kernel_dimension": len(edge_keys) - raw_top.rank(),
        "one_and_two_edge_response_tangent_rank": tangent.rank(),
        "one_and_two_edge_response_tangent_kernel_dimension": len(edge_keys) - tangent.rank(),
        "response_chart_rows": chart_rows,
        "response_chart_determinant": chart_det,
        "cycle_detection_after_discarding_all_mean_only_tensors": full_rank_minor(detection),
    }
    return {
        "prime": P, "seed": 72109, "sites": n,
        "two_direction_recovery": recovery,
        "mean_synchronization": mean_report,
        "blind_edge_reconstruction": blind_edge_report,
        "independent_source_comparison": gauge_report,
        "edge_recovery": edge_report,
        "source_mean_directions": means,
        "source_edges": [{"sites": list(edge), "weights": value} for edge, value in edges.items()],
    }


if __name__ == "__main__":
    print(json.dumps(run(int(sys.argv[1]) if len(sys.argv) > 1 else 5), indent=2))

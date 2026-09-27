#!/usr/bin/env python3
"""Blind reconstruction with three or more mean directions.

Uses python-flint via the repository .venv. Prints JSON, writes no files.
Default examples: (sites, directions) = (3, 3), (3, 4), and (5, 3).
"""

import argparse
import itertools
import json
import math
import random

from flint import nmod_mat

import two_direction as base

P = base.P


def compositions(k, r):
    if r == 1:
        yield (k,)
    else:
        for a in range(k + 1):
            for rest in compositions(k - a, r - 1):
                yield (a,) + rest


def monomer_polynomial(means, sites, word):
    r = len(means)
    polynomial = {(0,) * r: 1}
    for i in sites:
        updated = {}
        for powers, coefficient in polynomial.items():
            for s in range(r):
                key = list(powers)
                key[s] += 1
                key = tuple(key)
                updated[key] = (updated.get(key, 0) + coefficient * means[s][i][word[i]]) % P
        polynomial = updated
    return polynomial


def responses(means, edges):
    r, n, local = len(means), len(means[0]), len(means[0][0])
    ws = list(itertools.product(range(local), repeat=n))
    keys = [p for k in range(n % 2, n + 1, 2) for p in compositions(k, r)]
    layers = {key: [0] * len(ws) for key in keys}
    for singles, pairs in base.exterior.matchings(list(range(n))):
        for z, word in enumerate(ws):
            edge_value = 1
            for i, j in pairs:
                edge_value = edge_value * edges[i, j][word[i]][word[j]] % P
            for key, value in monomer_polynomial(means, singles, word).items():
                layers[key][z] = (layers[key][z] + edge_value * value) % P
    return ws, keys, layers


def recover_terminal(observations, ws, r, all_sites=False):
    n, d, local = len(ws[0]), len(observations), max(ws[-1]) + 1
    monomials = list(itertools.combinations_with_replacement(range(d), 2))
    nullity = math.comb(2 * n + r - 1, r - 1)
    target = len(monomials) - nullity
    tails = local ** (n - 1)
    sites = range(n) if all_sites else [0]
    word_index = {word: z for z, word in enumerate(ws)}
    reordered = {}
    for site in sites:
        permutation = []
        for colour in range(local):
            for tail in itertools.product(range(local), repeat=n - 1):
                word = tail[:site] + (colour,) + tail[site:]
                permutation.append(word_index[word])
        reordered[site] = [[tensor[z] for z in permutation] for tensor in observations]
    selected, labels, batch, batch_labels = [], [], [], []

    def compress():
        nonlocal selected, labels, batch, batch_labels
        rows = selected + batch
        row_labels = labels + batch_labels
        chosen = base.pivot_columns(nmod_mat(rows, P).transpose())
        selected = [rows[z] for z in chosen]
        labels = [row_labels[z] for z in chosen]
        batch, batch_labels = [], []

    # Interleave row pairs, so a large column block cannot monopolize the scan.
    for c, e in itertools.combinations(range(tails), 2):
        for site, (i, j) in itertools.product(sites, itertools.combinations(range(local), 2)):
            flattened = reordered[site]
            ix = (i * tails + c, i * tails + e, j * tails + c, j * tails + e)
            row = []
            for h, k in monomials:
                value = flattened[h][ix[0]] * flattened[k][ix[3]] - flattened[h][ix[1]] * flattened[k][ix[2]]
                if h != k:
                    value += flattened[k][ix[0]] * flattened[h][ix[3]] - flattened[k][ix[1]] * flattened[h][ix[2]]
                row.append(value % P)
            batch.append(row)
            batch_labels.append([site, i, j, c, e] if all_sites else [i, j, c, e])
            if len(batch) == 128:
                compress()
                assert len(selected) <= target
                if len(selected) == target:
                    break
        if len(selected) == target:
            break
    if len(selected) < target and batch:
        compress()
    assert len(selected) == target
    coefficient_matrix = nmod_mat(selected, P)
    quadratic_basis = base.kernel_columns(coefficient_matrix)
    assert len(quadratic_basis) == nullity
    image_columns = []
    for q in quadratic_basis:
        symmetric = [[0] * d for _ in range(d)]
        for (i, j), value in zip(monomials, q):
            symmetric[i][j] = symmetric[j][i] = value
        image_columns.extend(list(map(list, zip(*symmetric))))
    chosen = base.pivot_columns(base.columns(image_columns))
    coordinates = [image_columns[i] for i in chosen]
    assert len(coordinates) == math.comb(n + r - 1, r - 1)
    matrix = base.columns(observations) * base.columns(coordinates)
    terminal = [[int(matrix[i, j]) for i in range(len(ws))] for j in range(len(coordinates))]
    return terminal, {
        "quadratic_columns": len(monomials),
        "quadratic_kernel_dimension": nullity,
        "terminal_dimension": len(terminal),
        "quadratic_coefficient_minor": base.full_rank_minor(coefficient_matrix),
        "selected_flattening_minor_labels": labels,
    }


def local_supports(terminal, ws, sites, local):
    other = [i for i in range(len(ws[0])) if i not in sites]
    local_words = list(itertools.product(range(local), repeat=len(sites)))
    other_words = list(itertools.product(range(local), repeat=len(other)))
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
    chosen = base.pivot_columns(base.columns(contractions))
    return [contractions[i] for i in chosen]


def recover_means(terminal, ws, r):
    n, local = len(ws[0]), max(ws[-1]) + 1
    supports = [local_supports(terminal, ws, [i], local) for i in range(n)]
    assert all(len(basis) == r for basis in supports)
    matrices = [base.columns(basis) for basis in supports]
    inverses, selected_rows = [], []
    for matrix in matrices:
        rows = base.pivot_columns(matrix.transpose())
        square = nmod_mat([[int(matrix[i, j]) for j in range(r)] for i in rows], P)
        inverses.append(square.inv())
        selected_rows.append(rows)
    synchronized, reports = [matrices[0]], []
    for i in range(1, n):
        pair_support = local_supports(terminal, ws, [0, i], local)
        assert len(pair_support) == r * (r + 1) // 2
        pair_rows = []
        for vector in pair_support:
            square = nmod_mat([[vector[a * local + b] for b in selected_rows[i]] for a in selected_rows[0]], P)
            coefficient = inverses[0] * square * inverses[i].transpose()
            pair_rows.append([int(coefficient[a, b]) for a in range(r) for b in range(r)])
        annihilators = base.kernel_columns(nmod_mat(pair_rows, P))
        assert len(annihilators) == r * (r - 1) // 2
        equations = []
        for vector in annihilators:
            a = [vector[j * r:(j + 1) * r] for j in range(r)]
            for u, v in itertools.combinations_with_replacement(range(r), 2):
                row = [0] * (r * r)
                for k in range(r):
                    row[k * r + v] += a[u][k]
                    if u != v:
                        row[k * r + u] += a[v][k]
                equations.append([x % P for x in row])
        solutions = base.kernel_columns(nmod_mat(equations, P))
        assert len(solutions) == 1
        transform = nmod_mat([solutions[0][j * r:(j + 1) * r] for j in range(r)], P)
        assert transform.det()
        synchronized.append(matrices[i] * transform)
        reports.append({"site": i, "map_determinant": int(transform.det()),
                        "synchronization_constraint_rank": len(equations[0]) - 1})
    means = [[[int(synchronized[i][a, s]) for a in range(local)] for i in range(n)] for s in range(r)]
    zero = {(i, j): [[0] * local for _ in range(local)] for i, j in itertools.combinations(range(n), 2)}
    _, keys, layers = responses(means, zero)
    generated = [layers[key] for key in keys if sum(key) == n]
    assert base.columns(terminal + generated).rank() == len(terminal)
    return means, reports


def mean_quadratics(means, edge_keys):
    return [[
        (means[s][i][a] * means[t][j][b] + (means[t][i][a] * means[s][j][b] if s != t else 0)) % P
        for i, j, a, b in edge_keys
    ] for s, t in itertools.combinations_with_replacement(range(len(means)), 2)]


def recover_edges(observations, means, ws):
    r, n, local = len(means), len(ws[0]), len(means[0][0])
    pairs = list(itertools.combinations(range(n), 2))
    edge_keys = [(i, j, a, b) for i, j in pairs for a in range(local) for b in range(local)]
    edge_index = {key: z for z, key in enumerate(edge_keys)}
    keys = list(compositions(n - 2, r))
    top = {key: [[0] * len(edge_keys) for _ in ws] for key in keys}
    for z, word in enumerate(ws):
        for i, j in pairs:
            polynomial = monomer_polynomial(means, [v for v in range(n) if v not in (i, j)], word)
            c = edge_index[i, j, word[i], word[j]]
            for key, value in polynomial.items():
                top[key][z][c] = value
    maps = [nmod_mat(top[key], P) for key in keys]
    raw = base.stack(maps)
    assert raw.rank() == len(edge_keys)
    project, _, _ = base.projector(observations)
    constraints = base.stack([project(g) for g in maps])
    candidates = base.kernel_columns(constraints)
    quadratics = mean_quadratics(means, edge_keys)
    assert len(candidates) == 1 + len(quadratics)
    assert base.columns(quadratics).rank() == len(quadratics)
    chosen = next(v for v in candidates if base.columns(quadratics + [v]).rank() == len(candidates))
    edges = {(i, j): [[0] * local for _ in range(local)] for i, j in pairs}
    for (i, j, a, b), value in zip(edge_keys, chosen):
        edges[i, j][a][b] = value
    _, _, recovered_layers = responses(means, edges)
    assert base.columns(observations + list(recovered_layers.values())).rank() == len(observations)
    return edges, {
        "edge_parameters": len(edge_keys), "ambiguity_dimension": len(candidates),
        "raw_one_edge_map_minor": base.full_rank_minor(raw),
        "edge_constraint_minor": base.full_rank_minor(constraints),
        "reconstructed_response_space_matches": True,
    }


def compare_sources(means, edges, recovered_means, recovered_edges):
    r, n, local = len(means), len(means[0]), len(means[0][0])
    original = [base.columns([means[s][i] for s in range(r)]) for i in range(n)]
    recovered = [base.columns([recovered_means[s][i] for s in range(r)]) for i in range(n)]
    rows = base.pivot_columns(original[0].transpose())
    a = nmod_mat([[int(original[0][i, j]) for j in range(r)] for i in rows], P)
    b = nmod_mat([[int(recovered[0][i, j]) for j in range(r)] for i in rows], P)
    change = a.inv() * b
    scalars = []
    for i in range(n):
        expected = original[i] * change
        u, v = next((u, v) for u in range(local) for v in range(r) if expected[u, v])
        scalar = int(recovered[i][u, v]) * pow(int(expected[u, v]), -1, P) % P
        assert scalar and (recovered[i] - expected * scalar).rank() == 0
        scalars.append(scalar)
    edge_keys = [(i, j, a, b) for i, j in edges for a in range(local) for b in range(local)]
    transformed = [scalars[i] * scalars[j] * edges[i, j][a][b] % P for i, j, a, b in edge_keys]
    answer = [recovered_edges[i, j][a][b] for i, j, a, b in edge_keys]
    gauge = base.columns([transformed] + mean_quadratics(recovered_means, edge_keys))
    rows = base.pivot_columns(gauge.transpose())
    square = nmod_mat([[int(gauge[i, j]) for j in range(gauge.ncols())] for i in rows], P)
    coefficients = square.inv() * nmod_mat([[answer[i]] for i in rows], P)
    assert coefficients[0, 0] and (gauge * coefficients - base.columns([answer])).rank() == 0
    return {"common_mean_basis_change": [[int(change[i, j]) for j in range(r)] for i in range(r)],
            "site_scalars": scalars,
            "quadratic_scale_and_mean_quadratic_coefficients": [int(coefficients[i, 0]) for i in range(coefficients.nrows())],
            "reconstruction_differs_only_by_proved_gauges": True}


def run(r, n=3, local=None, graph=None):
    local, seed = local or r + 1, 270927
    rng = random.Random(seed)
    means = [[[rng.randrange(P) for _ in range(local)] for _ in range(n)] for _ in range(r)]
    edges = {(i, j): [[rng.randrange(P) for _ in range(local)] for _ in range(local)]
             for i, j in itertools.combinations(range(n), 2)}
    if graph is not None:
        graph = {tuple(sorted(edge)) for edge in graph}
        for edge in edges:
            if edge not in graph:
                edges[edge] = [[0] * local for _ in range(local)]
    ws, keys, layers = responses(means, edges)
    keys = [key for key in keys if any(layers[key])]
    basis = [layers[key] for key in keys]
    d = len(keys)
    exponents = [sum(a * (n + 1) ** s for s, a in enumerate(key)) for key in keys]
    evaluation = nmod_mat([[pow(j, e, P) for e in exponents] for j in range(1, d + 1)], P)
    assert evaluation.det()
    output = base.columns(basis) * evaluation.transpose()
    observations = [[int(output[i, j]) for i in range(len(ws))] for j in range(d)]
    assert base.columns(observations).rank() == d
    terminal, terminal_report = recover_terminal(observations, ws, r, all_sites=graph is not None)
    actual_terminal = [layers[key] for key in keys if sum(key) == n]
    assert base.columns(terminal + actual_terminal).rank() == len(terminal)
    recovered_means, synchronization = recover_means(terminal, ws, r)
    recovered_edges, edge_report = recover_edges(observations, recovered_means, ws)
    comparison = compare_sources(means, edges, recovered_means, recovered_edges)
    return {
        "sites": n, "mean_directions": r, "local_dimension": local,
        "seed": seed, "prime": P, "response_dimension": d,
        "evaluation_determinant": int(evaluation.det()),
        "terminal_recovery": terminal_report, "local_synchronization": synchronization,
        "edge_recovery": edge_report, "independent_source_comparison": comparison,
        "source_mean_directions": means,
        "source_edges": [{"sites": list(edge), "weights": value} for edge, value in edges.items()],
        "recovered_mean_directions": recovered_means,
        "recovered_edges": [{"sites": list(edge), "weights": value} for edge, value in recovered_edges.items()],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minimal-local", action="store_true",
                        help="Check three directions in three-dimensional sites at n=3 and n=5.")
    args = parser.parse_args()
    cases = [run(3, 3, local=3), run(3, 5, local=3)] if args.minimal_local else [run(3), run(4), run(3, 5)]
    print(json.dumps({"cases": cases}, indent=2))

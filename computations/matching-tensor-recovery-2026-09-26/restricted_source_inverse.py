#!/usr/bin/env python3
"""Recover a source from its tensor and mean lines, without a full kernel.

Exact arithmetic modulo 1009. Mean lines are INPUT, not inferred here.
The covariance and actual mean scales are reconstructed, and every output
entry is checked by an independent matching recurrence. Prints JSON only.
"""

from functools import lru_cache
import hashlib
import itertools
import json
import math
import random

import numpy as np
from flint import nmod_mat

import calibrated_span as calibrated
import single_source as single
from audit_pair_observation import moments
from three_outside_certificate import direct_entry

base, P = single.base, single.P


class ExteriorAction:
    """Sparse columns: each column has at most 2**n nonzero entries."""

    def __init__(self, tensor, n):
        self.n = n
        self.tensor = np.asarray(tensor, dtype=np.int64)
        self.powers = np.array([3**i for i in reversed(range(n))])
        self.bits = np.array(list(itertools.product([0, 1], repeat=n)))
        self.sign = np.where((n - self.bits.sum(axis=1)) % 2, -1, 1)
        self.cache = {}

    def column(self, index):
        if index not in self.cache:
            b = index // self.powers % 3
            a = (b + 1 + self.bits) % 3
            c = 3 - a - b
            rows = a @ self.powers
            values = self.sign * self.tensor[c @ self.powers] % P
            self.cache[index] = rows, values
        return self.cache[index]

    def apply(self, polynomials):
        result = np.zeros((3**self.n, len(polynomials)), dtype=np.int64)
        for j, polynomial in enumerate(polynomials):
            for index, coefficient in polynomial.items():
                if coefficient % P:
                    rows, values = self.column(index)
                    result[rows, j] = (result[rows, j] + coefficient * values) % P
        return nmod_mat(result.tolist(), P)


def response_layers(means, edges):
    """Subset tensor recurrence, recording the number of matching edges."""

    @lru_cache(None)
    def visit(sites):
        if not sites:
            return np.array([1], dtype=np.int64)
        i, *rest = sites
        result = np.zeros((len(sites) // 2 + 1,) + (3,) * len(sites), dtype=np.int64)
        old = visit(tuple(rest))
        result[:len(old)] = np.array(means[i]).reshape((1, 3) + (1,) * len(rest)) * old[:, None] % P
        for position, j in enumerate(rest, 1):
            old = visit(tuple(k for k in rest if k != j))
            pair = np.asarray(edges[i, j]).reshape((1, 3, 3) + (1,) * (len(rest) - 1))
            term = pair * old[:, None, None] % P
            term = np.moveaxis(term, 2, position + 1)
            result[1:len(old) + 1] = (result[1:len(old) + 1] + term) % P
        return result

    return visit(tuple(range(len(means)))).reshape((len(means) // 2 + 1, -1)).tolist()


def edge_setup(n):
    keys = [(i, j, a, b) for i, j in itertools.combinations(range(n), 2)
            for a in range(3) for b in range(3)]
    index = {key: q for q, key in enumerate(keys)}
    powers = [3**(n - 1 - i) for i in range(n)]
    codes = [a * powers[i] + b * powers[j] for i, j, a, b in keys]
    masks = [(1 << i) | (1 << j) for i, j, _, _ in keys]
    flows = []
    for i in range(n):
        others = [j for j in range(n) if j != i]
        for a in [1, 2]:
            for j in others[1:]:
                row = {}
                for k, value in [(j, 1), (others[0], P - 1)]:
                    key = (i, k, a, 0) if i < k else (k, i, 0, a)
                    row[index[key]] = value
                flows.append(row)
    pure = [index[i, j, 0, 0] for i, j in itertools.combinations(range(n), 2)]
    mean_kernel = [{q: 1, pure[0]: P - 1} for q in pure[1:]]

    def product(left, right):
        result = {}
        for q, x in left.items():
            for r, y in right.items():
                if not masks[q] & masks[r]:
                    code = codes[q] + codes[r]
                    result[code] = (result.get(code, 0) + x * y) % P
        return {code: value for code, value in result.items() if value}

    return keys, index, codes, flows, mean_kernel, product


def linear_solve(matrix, target):
    rows = base.pivot_columns(matrix.transpose())
    assert len(rows) == matrix.ncols(), "correction matrix is not injective"
    square = nmod_mat([[int(matrix[i, j]) for j in range(matrix.ncols())] for i in rows], P)
    solution = square.inv() * nmod_mat([[-int(target[i, 0])] for i in rows], P)
    assert (matrix * solution + target).rank() == 0, "inconsistent correction equations"
    return [int(solution[i, 0]) for i in range(solution.nrows())], {
        "rank": matrix.ncols(), "rows": rows, "determinant": int(square.det()),
        "all_equation_rows_verified": True,
    }


def add_correction(vector, basis, coefficients):
    answer = dict(vector)
    for row, coefficient in zip(basis, coefficients):
        for q, value in row.items():
            answer[q] = (answer.get(q, 0) + value * coefficient) % P
    return {q: value for q, value in answer.items() if value}


def recover(tensor, mean_lines):
    """The only inputs are one observed tensor and local line representatives."""
    n = len(mean_lines)
    assert n >= 7 and n % 2
    bases = []
    for line in mean_lines:
        pivot = next(i for i, x in enumerate(line) if x)
        basis = base.columns([line] + [[int(a == c) for a in range(3)] for c in range(3) if c != pivot])
        assert basis.det()
        bases.append(basis)
    transformed = single.transform_columns([tensor], [b.inv() for b in bases])[0]
    action = ExteriorAction(transformed, n)
    keys, indices, codes, flows, mean_kernel, product = edge_setup(n)
    f2 = sorted(set(codes))
    exterior = action.apply([{code: 1} for code in f2])
    kernel = base.kernel_columns(exterior)
    assert len(kernel) == 2
    f2_minor = base.full_rank_minor(exterior)
    decode = lambda code: tuple(code // 3**i % 3 for i in reversed(range(n)))
    independent_minor = nmod_mat([[direct_entry(transformed, decode(i), decode(f2[j]))
                                   for j in f2_minor["columns"]]
                                  for i in f2_minor["rows"]], P)
    assert int(independent_minor.det()) == f2_minor["determinant"] != 0
    outside = [j for j, code in enumerate(f2)
               if sum(code // 3**i % 3 != 0 for i in range(n)) == 2]
    one_edge = next(v for v in kernel if any(v[j] for j in outside))
    # A fixed section of Phi: first edge contributing each tensor coordinate.
    section = {}
    for q, code in enumerate(codes):
        section.setdefault(code, q)
    initial = {section[code]: value for code, value in zip(f2, one_edge) if value}
    nuisance_columns = base.pivot_columns(exterior)
    nuisance = nmod_mat([[int(exterior[i, j]) for j in nuisance_columns]
                         for i in range(exterior.nrows())], P)

    first = action.apply([product(initial, flow) for flow in flows])
    combined = nmod_mat([a + b for a, b in zip(first.tolist(), nuisance.tolist())], P)
    target = action.apply([{code: value * pow(2, -1, P) % P
                            for code, value in product(initial, initial).items()}])
    correction, first_report = linear_solve(combined, target)
    middle = add_correction(initial, flows, correction[:len(flows)])
    second = action.apply([product(middle, row) for row in mean_kernel])
    target = action.apply([{code: value * pow(2, -1, P) % P
                            for code, value in product(middle, middle).items()}])
    correction, second_report = linear_solve(second, target)
    final = add_correction(middle, mean_kernel, correction)
    representative = base.edge_dictionary([final.get(q, 0) for q in range(len(keys))], keys)

    frame = [[1, 0, 0] for _ in range(n)]
    layers = response_layers(frame, representative)
    response_basis = base.columns(list(reversed(layers)))
    rows = base.pivot_columns(response_basis.transpose())
    assert len(rows) == len(layers)
    square = nmod_mat([[int(response_basis[i, j]) for j in range(len(layers))] for i in rows], P)
    coordinates = square.inv() * nmod_mat([[transformed[i]] for i in rows], P)
    assert (response_basis * coordinates - base.columns([transformed])).rank() == 0
    response_keys = [(degree,) for degree in range(1, n + 1, 2)]
    z = [[int(coordinates[0, 0])]]
    beta, covariance, calibration = calibrated.one_output_parameters(response_keys, coordinates, z)
    mus, recovered = calibrated.rational_source(z, [frame], representative, beta, covariance)
    mu = mus[0]
    recovered_means = [[int(x[0]) for x in (bases[i] * nmod_mat([[a] for a in mu[i]], P)).tolist()]
                       for i in range(n)]
    recovered_edges = {(i, j): [[int(a) for a in row] for row in
                              (bases[i] * nmod_mat(block, P) * bases[j].transpose()).tolist()]
                       for (i, j), block in recovered.items()}
    assert moments(recovered_means, recovered_edges, P) == tensor
    return recovered_means, recovered_edges, {
        "supplied_mean_lines": mean_lines,
        "f2_dimension": len(f2), "f2_kernel_dimension": len(kernel),
        "f2_rank_minor": f2_minor, "f2_minor_rebuilt_entrywise": True,
        "flow_dimension": len(flows), "flow_and_nuisance_minor": first_report,
        "pure_mean_dimension": len(mean_kernel), "pure_mean_minor": second_report,
        "response_dimension": len(layers), "response_pivot_rows": rows,
        "response_minor_determinant": int(square.det()), "calibration": calibration,
        "all_response_coordinates_verified": True,
        "all_observed_entries_reproduced_independently": True,
        "full_exterior_kernel_computed": False, "f3_rank_matrix_computed": False,
    }


def compare_source(means, edges, mu, recovered):
    gains = []
    for old, new in zip(means, mu):
        pivot = next(a for a in range(3) if old[a])
        g = new[pivot] * pow(old[pivot], -1, P) % P
        assert all(new[a] == g * old[a] % P for a in range(3))
        gains.append(g)
    assert math.prod(gains) % P == 1
    assert all(recovered[i, j][a][b] == gains[i] * gains[j] * block[a][b] % P
               for (i, j), block in edges.items() for a in range(3) for b in range(3))
    return gains


def serialize_edges(edges):
    return [{"sites": list(edge), "weights": block} for edge, block in edges.items()]


def run(n, count=1):
    seed = 271952
    rng = random.Random(seed + n)
    edges = {e: [[rng.randrange(P) for _ in range(3)] for _ in range(3)]
             for e in itertools.combinations(range(n), 2)}
    records, actual, answers = [], [], []
    for output in range(count):
        means = [[rng.randrange(1, P) for _ in range(3)] for _ in range(n)]
        actual.append(means)
        lines = [[x * pow(row[0], -1, P) % P for x in row] for row in means]
        tensor = moments(means, edges, P)
        layers = response_layers(means, edges)
        assert (np.array(layers).sum(axis=0) % P).tolist() == tensor
        mu, recovered, report = recover(tensor, lines)
        gains = compare_source(means, edges, mu, recovered)
        answers.append((mu, recovered))
        records.append({"output": output, "source_means": means,
                        "tensor_sha256": hashlib.sha256(json.dumps(tensor).encode()).hexdigest(),
                        "recovered_means": mu, "recovered_edges": serialize_edges(recovered),
                        "source_comparison_site_scalars": gains, **report})
    alignment = []
    first_means, first_edges = answers[0]
    aligned = [first_means]
    for mu, recovered in answers[1:]:
        ratios = {}
        for edge, block in recovered.items():
            a, b = next((a, b) for a in range(3) for b in range(3) if block[a][b])
            ratio = first_edges[edge][a][b] * pow(block[a][b], -1, P) % P
            assert all(first_edges[edge][a][b] == ratio * block[a][b] % P
                       for a in range(3) for b in range(3))
            ratios[edge] = ratio
        gains = []
        for i in range(n):
            rest = [j for j in range(n) if j != i]
            matching = list(zip(rest[::2], rest[1::2]))
            gains.append(pow(math.prod(ratios[edge] for edge in matching) % P, -1, P))
        assert math.prod(gains) % P == 1
        assert all(ratios[i, j] == gains[i] * gains[j] % P for i, j in ratios)
        aligned.append([[gains[i] * x % P for x in row] for i, row in enumerate(mu)])
        alignment.append(gains)
    common = records[0]["source_comparison_site_scalars"]
    assert all(aligned[k][i][a] == common[i] * actual[k][i][a] % P
               for k in range(count) for i in range(n) for a in range(3))
    observed_rank = base.columns([[x for row in mu for x in row] for mu in aligned]).rank()
    assert observed_rank == count
    local_ranks = [base.columns([mu[i] for mu in aligned]).rank() for i in range(n)]
    assert all(rank == min(3, count) for rank in local_ranks)
    return {"sites": n, "outputs": count, "seed": seed + n,
            "source_edges": serialize_edges(edges), "cases": records,
            "alignment_site_scalars": alignment, "shared_covariance_alignment_verified": True,
            "observed_mean_span_dimension": observed_rank,
            "local_mean_span_dimensions": local_ranks}


if __name__ == "__main__":
    print(json.dumps({"prime": P, "cases": [run(7), run(9, count=4)],
                      "scope": "Mean lines supplied; covariance and actual mean scales recovered."
                      " No blind mean-direction algorithm or noisy estimation guarantee."}, indent=2))

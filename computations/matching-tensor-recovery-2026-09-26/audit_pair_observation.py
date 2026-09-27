#!/usr/bin/env python3
"""Independent entry construction and Pfaffian audit of the pair certificate.

Uses numpy, without importing the reconstruction code or python-flint.
Reads pair-observation-certificate.json beside this script; prints JSON.
"""

from functools import lru_cache
import itertools
import json
from pathlib import Path

import numpy as np


def moments(means, edges, p):
    n = len(means)
    result = []
    for word in itertools.product(*(range(len(row)) for row in means)):
        @lru_cache(None)
        def recurse(sites):
            if not sites:
                return 1
            i, *rest = sites
            value = means[i][word[i]] * recurse(tuple(rest))
            for j in rest:
                value += edges[i, j][word[i]][word[j]] * recurse(tuple(k for k in rest if k != j))
            return value % p
        result.append(recurse(tuple(range(n))))
    return result


def direct_matrix(first, second, n, p):
    words = list(itertools.product(range(4), repeat=n))
    indices = {word: i for i, word in enumerate(words)}
    matrix = np.zeros((len(words), len(words)), dtype=np.int64)
    complement = {}
    for a in range(4):
        for b in range(4):
            if a == b:
                continue
            c, d = (i for i in range(4) if i not in (a, b))
            permutation = (a, b, c, d)
            sign = (-1)**sum(permutation[i] > permutation[j] for i in range(4) for j in range(i + 1, 4))
            complement[a, b] = ((c, d, sign), (d, c, -sign))
    for row, a in enumerate(words):
        for b in itertools.product(*(tuple(i for i in range(4) if i != x) for x in a)):
            column = indices[b]
            if column <= row:
                continue
            total = 0
            for choices in itertools.product(*(complement[x, y] for x, y in zip(a, b))):
                c_index, d_index, sign = 0, 0, 1
                for c, d, factor in choices:
                    c_index, d_index, sign = 4 * c_index + c, 4 * d_index + d, sign * factor
                total += sign * first[c_index] * second[d_index]
            matrix[row, column] = total % p
            matrix[column, row] = -total % p
    return matrix


def pfaffian(matrix, p):
    matrix = matrix.copy()
    size, result = matrix.shape[0], 1
    assert size % 2 == 0 and np.all((matrix + matrix.T) % p == 0)
    for k in range(0, size, 2):
        candidates = np.flatnonzero(matrix[k, k + 1:])
        if not len(candidates):
            return 0
        j = k + 1 + int(candidates[0])
        if j != k + 1:
            matrix[[k + 1, j], :] = matrix[[j, k + 1], :]
            matrix[:, [k + 1, j]] = matrix[:, [j, k + 1]]
            result = -result
        pivot = int(matrix[k, k + 1])
        result = result * pivot % p
        u, v = matrix[k, k + 2:], matrix[k + 1, k + 2:]
        correction = (np.outer(v, u) - np.outer(u, v)) * pow(pivot, -1, p)
        matrix[k + 2:, k + 2:] = (matrix[k + 2:, k + 2:] + correction) % p
    return result


def run():
    certificate = json.loads(Path(__file__).with_name("pair-observation-certificate.json").read_text())
    n, p = certificate["sites"], certificate["prime"]
    edges = {tuple(entry["sites"]): entry["weights"] for entry in certificate["source_edges"]}
    basis = certificate["source_mean_basis"]
    inputs = []
    for setting in certificate["source_input_settings"]:
        means = [[sum(setting[s] * basis[s][i][a] for s in range(2)) % p for a in range(4)] for i in range(n)]
        inputs.append(moments(means, edges, p))
    assert inputs == certificate["input_tensors"]
    recovered_edges = {tuple(entry["sites"]): entry["weights"] for entry in certificate["recovered_actual_edges"]}
    assert [moments(mean, recovered_edges, p) for mean in certificate["recovered_actual_means"]] == inputs
    matrix = direct_matrix(*inputs, n, p)
    indices = certificate["principal_minor_indices"]
    value = pfaffian(matrix[np.ix_(indices, indices)], p)
    assert value and value * value % p == certificate["principal_minor_determinant"]
    return {"prime": p, "sites": n, "input_moments_checked_by_independent_recursion": True,
            "reconstructed_moments_checked_by_independent_recursion": True,
            "exterior_matrix_constructed_entrywise": True,
            "principal_minor_order": len(indices), "pfaffian": value,
            "determinant": value * value % p}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

#!/usr/bin/env python3
"""Structured single-output exterior kernels and low-degree constraints.

Exploratory exact examples, not all-orders covariance-recovery proofs.
Full kernels are computed only at five and seven sites. The nine-site
checks apply the exterior map to tensors with at most two outside-mean
factors; they do not form a 3^9 by 3^9 matrix. Prints JSON, writes no files.
"""

import itertools
import json
import math
import random

import numpy as np
from flint import nmod_mat

import single_source as single
from audit_pair_observation import moments
from audit_single_source import exterior_matrix

P, base = single.P, single.base


def source(n, family, seed):
    rng = random.Random(seed)
    cycle = {(i, i + 1) for i in range(n - 1)} | {(0, n - 1)}
    path = {(i, i + 1) for i in range(n - 1)}
    edges = {}
    for e in itertools.combinations(range(n), 2):
        block = [[rng.randrange(P) for _ in range(3)] for _ in range(3)]
        if family == "uniform_outside":
            block = [[int(a == b and a != 0) for b in range(3)] for a in range(3)]
        if family in ["outside_complete", "outside_cycle"]:
            block = [[block[a][b] if a and b else 0 for b in range(3)] for a in range(3)]
        if family == "block_complete":
            block = [[block[a][b] if (a == 0) == (b == 0) else 0 for b in range(3)] for a in range(3)]
        if family == "diagonal_outside":
            block = [[block[a][b] if a == b and a else 0 for b in range(3)] for a in range(3)]
        if family == "scalar_outside":
            block = [[block[1][1] * int(a == b and a != 0) for b in range(3)] for a in range(3)]
        if ((family in ["full_cycle", "outside_cycle"] and e not in cycle)
                or (family == "full_path" and e not in path)):
            block = [[0] * 3 for _ in range(3)]
        edges[e] = block
    return [[1, 0, 0] for _ in range(n)], edges


def exterior_columns(tensor, n, words):
    powers = [3**(n - 1 - i) for i in range(n)]
    matrix = np.zeros((3**n, len(words)), dtype=np.int64)
    for col, b in enumerate(words):
        for a in itertools.product(*(tuple(x for x in range(3) if x != y) for y in b)):
            row = sum(x * p for x, p in zip(a, powers))
            complement = sum((3 - x - y) * p for x, y, p in zip(a, b, powers))
            sign = math.prod(1 if y == (x + 1) % 3 else -1 for x, y in zip(a, b))
            matrix[row, col] = sign * tensor[complement] % P
    return nmod_mat(matrix.tolist(), P)


def full_probe(n, family):
    seed = 271930
    means, edges = source(n, family, seed)
    tensor = moments(means, edges, P)
    matrix = nmod_mat(exterior_matrix(tensor, n, P).tolist(), P)
    kernel = base.kernel_columns(matrix)
    words = list(itertools.product(range(3), repeat=n))
    rows = [i for i, word in enumerate(words) if all(word)]
    outside_rank = nmod_mat([[v[i] for v in kernel] for i in rows], P).rank()
    return {"sites": n, "family": family, "seed": seed,
            "exterior_kernel_dimension": len(kernel),
            "all_outside_rank": outside_rank,
            "completed_dimension": len(kernel) - outside_rank,
            "response_count": (n + 1) // 2}


def low_probe(n, family):
    seed = 271932
    means, edges = source(n, family, seed)
    tensor = moments(means, edges, P)
    words = [w for w in itertools.product(range(3), repeat=n) if sum(a != 0 for a in w) <= 2]
    matrix = exterior_columns(tensor, n, words)
    # Independently assemble the terminal and one-edge responses in F_2.
    terminal, edge_response = [], []
    for word in words:
        terminal.append(int(not any(word)))
        edge_response.append(sum(block[word[i]][word[j]]
                                 for (i, j), block in edges.items()
                                 if all(word[k] == 0 for k in range(n) if k not in (i, j))) % P)
    responses = base.columns([terminal, edge_response])
    assert responses.rank() == 2 and (matrix * responses).rank() == 0
    return {"sites": n, "family": family, "seed": seed,
            "domain_dimension": len(words), "kernel_dimension": len(words) - matrix.rank(),
            "terminal_and_one_edge_responses_annihilated": True}


if __name__ == "__main__":
    print(json.dumps({"prime": P,
                      "full_kernels": [full_probe(n, family) for n in [5, 7]
                                       for family in ["full_cycle", "full_path", "outside_complete",
                                                      "block_complete", "full_complete"]],
                      "restricted_kernels": [low_probe(n, family) for n in [5, 7, 9]
                                             for family in ["uniform_outside", "diagonal_outside",
                                                            "scalar_outside", "outside_cycle", "full_cycle"]]},
                     indent=2))

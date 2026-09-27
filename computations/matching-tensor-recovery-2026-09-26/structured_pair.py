#!/usr/bin/env python3
"""Exploratory exact pair-kernel ranks for structured source families.

These are fixed-format examples, not an all-orders saturation proof.
Requires numpy and python-flint. Prints JSON, writes no files.
"""

import itertools
import json
import random

import pair_observation as pair


def run(n, kind, seed):
    rng, p = random.Random(seed), pair.P
    means = [[[int(a == s) for a in range(4)] for _ in range(n)] for s in range(2)]
    uniform = [[rng.randrange(p) for _ in range(4)] for _ in range(4)]
    uniform = [[uniform[min(a, b)][max(a, b)] for b in range(4)] for a in range(4)]
    cycle = {(i, i + 1) for i in range(n - 1)} | {(0, n - 1)}
    path = {(i, i + 1) for i in range(n - 1)}
    edges = {}
    for i, j in itertools.combinations(range(n), 2):
        block = [[rng.randrange(p) for _ in range(4)] for _ in range(4)]
        if kind == "uniform_complete":
            block = uniform
        if kind == "diagonal_complete":
            block = [[block[a][b] if a == b else 0 for b in range(4)] for a in range(4)]
        if kind in ["block_complete", "block_cycle"]:
            block = [[block[a][b] if (a < 2) == (b < 2) else 0 for b in range(4)] for a in range(4)]
        if (kind in ["full_cycle", "block_cycle"] and (i, j) not in cycle) or (kind == "full_path" and (i, j) not in path):
            block = [[0] * 4 for _ in range(4)]
        edges[i, j] = block
    ws, keys, layers = pair.many.responses(means, edges)
    inputs = [[sum(layers[key][i] for key in keys if key[1 - j] == 0) % p for i in range(len(ws))] for j in range(2)]
    matrix = pair.pair_matrix(*inputs, n)
    response = pair.base.columns(list(layers.values()))
    assert (matrix * response).rank() == 0
    return {"sites": n, "family": kind, "seed": seed,
            "response_dimension": response.rank(), "pair_kernel_dimension": 4**n - matrix.rank()}


if __name__ == "__main__":
    cases = [run(n, kind, 301930 + i) for n in [3, 5]
             for i, kind in enumerate(["uniform_complete", "diagonal_complete", "block_complete", "full_cycle", "block_cycle", "full_path"])]
    print(json.dumps({"prime": pair.P, "cases": cases}, indent=2))

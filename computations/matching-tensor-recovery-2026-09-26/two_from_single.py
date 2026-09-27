#!/usr/bin/env python3
"""Recover a five-site shared source from two three-dimensional outputs.

Uses the two covariance candidates supplied by each single output.
Requires numpy and python-flint. Prints JSON, writes no files.
"""

import itertools
import json
import math
import random

from flint import nmod_mat

from audit_pair_observation import moments
from single_source import P, recover


def align(first, second, n):
    ratios = {}
    for edge, block in first.items():
        a, b = next((a, b) for a in range(3) for b in range(3) if block[a][b])
        ratio = second[edge][a][b] * pow(block[a][b], -1, P) % P
        if not ratio or any(second[edge][a][b] != ratio * block[a][b] % P for a in range(3) for b in range(3)):
            return None
        ratios[edge] = ratio
    gains = []
    for i in range(n):
        others = [j for j in range(n) if j != i]
        product = math.prod(ratios[others[k], others[k + 1]] for k in range(0, n - 1, 2)) % P
        gains.append(pow(product, -1, P))
    if math.prod(gains) % P != 1 or any(gains[i] * gains[j] % P != value for (i, j), value in ratios.items()):
        return None
    return gains


def run():
    n, seed = 5, 90127
    rng = random.Random(seed)
    first_mean = [[rng.randrange(P) for _ in range(3)] for _ in range(n)]
    edges = {(i, j): [[rng.randrange(P) for _ in range(3)] for _ in range(3)]
             for i, j in itertools.combinations(range(n), 2)}
    second_mean = [[rng.randrange(P) for _ in range(3)] for _ in range(n)]
    means = [first_mean, second_mean]
    observations = [moments(mu, edges, P) for mu in means]
    answers = [recover(tensor, n) for tensor in observations]
    compatible, comparisons = [], []
    for i, j in itertools.product(range(2), repeat=2):
        first, second = answers[0][0][i], answers[1][0][j]
        gains = align(first[1], second[1], n)
        comparisons.append({"candidate_indices": [i, j], "compatible": gains is not None})
        if gains is not None:
            second_aligned = [[value * pow(gains[k], -1, P) % P for value in row]
                              for k, row in enumerate(second[0])]
            compatible.append(([first[0], second_aligned], first[1], gains, [i, j]))
    assert len(compatible) == 1
    recovered_means, recovered_edges, alignment, selected = compatible[0]
    assert [moments(mu, recovered_edges, P) for mu in recovered_means] == observations
    gains = []
    for i in range(n):
        a = next(a for a in range(3) if first_mean[i][a])
        gains.append(recovered_means[0][i][a] * pow(first_mean[i][a], -1, P) % P)
    assert math.prod(gains) % P == 1
    assert all(recovered_means[j][i][a] == gains[i] * means[j][i][a] % P
               for j in range(2) for i in range(n) for a in range(3))
    assert all(recovered_edges[i, j][a][b] == gains[i] * gains[j] * edges[i, j][a][b] % P
               for i, j in edges for a in range(3) for b in range(3))
    determinant = int(nmod_mat(edges[0, 1], P).det())
    assert determinant
    assert any(first_mean[0][a] * first_mean[1][b] % P != second_mean[0][a] * second_mean[1][b] % P
               for a in range(3) for b in range(3))
    return {"sites": n, "local_dimension": 3, "prime": P, "seed": seed,
            "single_output_reports": [answer[1] for answer in answers],
            "candidate_compatibility": comparisons, "selected_candidates": selected,
            "second_to_first_comparison_site_scalars": alignment,
            "original_source_comparison_site_scalars": gains, "site_scalar_product": math.prod(gains) % P,
            "generic_edge_rank_three_determinant": determinant,
            "both_output_tensors_reproduced": True,
            "source_means": means, "source_edges": [{"sites": list(k), "weights": v} for k, v in edges.items()],
            "recovered_means": recovered_means,
            "recovered_edges": [{"sites": list(k), "weights": v} for k, v in recovered_edges.items()]}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

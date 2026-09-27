#!/usr/bin/env python3
"""Recover two sources' shared blocks using overlapping four-coordinate views.

Five sites of dimensions (5,5,4,4,4); exact arithmetic modulo 1009.
Requires numpy and python-flint. Prints JSON, writes no files.
"""

import itertools
import json
import math
import random

from audit_pair_observation import moments
from pair_observation import P, recover_pair


def recover(inputs, dimensions):
    n = len(dimensions)
    words = list(itertools.product(*(range(d) for d in dimensions)))
    index = {word: i for i, word in enumerate(words)}
    baseline = [list(range(4)) for _ in dimensions]
    views = [baseline]
    for i, d in enumerate(dimensions):
        for a in range(4, d):
            view = [row[:] for row in baseline]
            view[i][-1] = a
            views.append(view)
    for i, j in itertools.combinations(range(n), 2):
        for a, b in itertools.product(range(4, dimensions[i]), range(4, dimensions[j])):
            view = [row[:] for row in baseline]
            view[i][-1], view[j][-1] = a, b
            views.append(view)
    mean_result = [[[None] * d for d in dimensions] for _ in range(2)]
    edge_result = {(i, j): [[None] * dimensions[j] for _ in range(dimensions[i])]
                   for i, j in itertools.combinations(range(n), 2)}
    reports, anchor = [], None
    for view in views:
        projected = [[tensor[index[word]] for word in itertools.product(*view)] for tensor in inputs]
        means, edges, report = recover_pair(projected)
        if anchor is None:
            anchor = [means[0][i][0] for i in range(n)]
        gains = [anchor[i] * pow(means[0][i][0], -1, P) % P for i in range(n)]
        assert math.prod(gains) % P == 1
        for setting, i in itertools.product(range(2), range(n)):
            for a, coordinate in enumerate(view[i]):
                value = gains[i] * means[setting][i][a] % P
                previous = mean_result[setting][i][coordinate]
                assert previous is None or previous == value
                mean_result[setting][i][coordinate] = value
        for i, j in edges:
            for a, b in itertools.product(range(4), repeat=2):
                value = gains[i] * gains[j] * edges[i, j][a][b] % P
                x, y = view[i][a], view[j][b]
                previous = edge_result[i, j][x][y]
                assert previous is None or previous == value
                edge_result[i, j][x][y] = value
        reports.append({"coordinate_view": view, "alignment_site_scalars": gains,
                        "pair_rank": report["pair_exterior_matrix_rank"],
                        "principal_determinant": report["principal_minor_determinant"],
                        "terminal_constraint_minor": report["terminal_recovery"]["quadratic_coefficient_minor"]["determinant"],
                        "cycle_constraint_minor": report["edge_class_recovery"]["cycle_correction_minor"]["determinant"],
                        "calibration_minor": report["calibration"]["calibration_linear_system_minor"]["determinant"]})
    assert all(x is not None for mean in mean_result for row in mean for x in row)
    assert all(x is not None for block in edge_result.values() for row in block for x in row)
    assert [moments(mean, edge_result, P) for mean in mean_result] == inputs
    return mean_result, edge_result, reports


def run():
    dimensions, seed = [5, 5, 4, 4, 4], 291927
    rng = random.Random(seed)
    means = [[[rng.randrange(P) for _ in range(d)] for d in dimensions] for _ in range(2)]
    edges = {(i, j): [[rng.randrange(P) for _ in range(dimensions[j])] for _ in range(dimensions[i])]
             for i, j in itertools.combinations(range(len(dimensions)), 2)}
    inputs = [moments(mean, edges, P) for mean in means]
    recovered_means, recovered_edges, views = recover(inputs, dimensions)
    gains = [recovered_means[0][i][0] * pow(means[0][i][0], -1, P) % P for i in range(len(dimensions))]
    assert math.prod(gains) % P == 1
    assert all(recovered_means[j][i][a] == gains[i] * means[j][i][a] % P
               for j in range(2) for i, d in enumerate(dimensions) for a in range(d))
    assert all(recovered_edges[i, j][a][b] == gains[i] * gains[j] * edges[i, j][a][b] % P
               for i, j in edges for a in range(dimensions[i]) for b in range(dimensions[j]))
    return {"local_dimensions": dimensions, "prime": P, "seed": seed,
            "observed_tensors": 2, "four_coordinate_views": views,
            "all_overlap_entries_agree": True, "all_full_tensor_entries_reproduced": True,
            "original_source_comparison_site_scalars": gains, "site_scalar_product": math.prod(gains) % P,
            "source_means": means, "recovered_means": recovered_means,
            "source_edges": [{"sites": list(edge), "weights": value} for edge, value in edges.items()],
            "recovered_edges": [{"sites": list(edge), "weights": value} for edge, value in recovered_edges.items()]}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

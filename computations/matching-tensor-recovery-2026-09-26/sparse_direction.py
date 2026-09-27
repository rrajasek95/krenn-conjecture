#!/usr/bin/env python3
"""Recover a sparse source graph without giving the graph to the inverse map.

The graph is used to generate test data and to compare the final answer only.
Uses python-flint, prints JSON, and writes no files.
"""

import argparse
import itertools
import json
import math

from flint import nmod_mat

import many_direction as many

P = many.P


def recover_sparse_representative(means, edge_class):
    """Only the reconstructed mean frame and edge class enter this routine."""
    r, n, local = len(means), len(means[0]), len(means[0][0])
    frames = [many.base.columns([means[s][i] for s in range(r)]) for i in range(n)]
    inverses = []
    for a in frames:
        rows = many.base.pivot_columns(a.transpose())
        assert len(rows) == r
        square = nmod_mat([[int(a[i, j]) for j in range(r)] for i in rows], P)
        inverse = square.inv()
        select = nmod_mat([[int(j == i) for j in range(local)] for i in rows], P)
        left_inverse = inverse * select
        inverses.append(left_inverse)
    graph, missing = [], []
    for i, j in itertools.combinations(range(n), 2):
        block = nmod_mat(edge_class[i, j], P)
        coefficient = inverses[i] * block * inverses[j].transpose()
        symmetric = (coefficient + coefficient.transpose()) * pow(2, -1, P)
        outside = block - frames[i] * symmetric * frames[j].transpose()
        (graph if outside.rank() else missing).append((i, j))
    assert missing, "This recovery uses the promise that an edge is absent."
    i, j = missing[0]
    mean_quadratic = inverses[i] * nmod_mat(edge_class[i, j], P) * inverses[j].transpose()
    assert (mean_quadratic - mean_quadratic.transpose()).rank() == 0
    recovered = {}
    for i, j in itertools.combinations(range(n), 2):
        block = nmod_mat(edge_class[i, j], P) - frames[i] * mean_quadratic * frames[j].transpose()
        recovered[i, j] = [[int(block[a, b]) for b in range(local)] for a in range(local)]
        assert bool(block.rank()) == ((i, j) in graph)
    return recovered, {
        "recovered_graph": [list(edge) for edge in graph],
        "missing_edge_used_to_fix_mean_quadratic": list(missing[0]),
        "removed_mean_quadratic_matrix": [[int(mean_quadratic[i, j]) for j in range(r)] for i in range(r)],
        "all_predicted_missing_edges_vanish_after_correction": True,
        "corrected_edges": [{"sites": list(edge), "weights": weights} for edge, weights in recovered.items()],
    }


def finish_case(case):
    source_edges = {tuple(e["sites"]): e["weights"] for e in case["source_edges"]}
    edge_class = {tuple(e["sites"]): e["weights"] for e in case["recovered_edges"]}
    fixed, report = recover_sparse_representative(case["recovered_mean_directions"], edge_class)
    n = len(case["recovered_mean_directions"][0])
    r = len(case["recovered_mean_directions"])
    matching_sizes = [nu for nu in range(n // 2 + 1)
                      if sum(math.comb(n - 2 * k + r - 1, r - 1) for k in range(nu + 1))
                      == case["response_dimension"]]
    assert len(matching_sizes) == 1
    report["matching_number_from_response_dimension"] = matching_sizes[0]
    # The source is consulted only after the blind graph and edge recovery.
    expected_graph = [list(edge) for edge, block in source_edges.items() if any(x for row in block for x in row)]
    assert report["recovered_graph"] == expected_graph
    support = {tuple(edge) for edge in report["recovered_graph"]}
    graph_matching_number = max(len(pairs) for _, pairs in many.base.exterior.matchings(list(range(n)))
                                if all(pair in support for pair in pairs))
    assert graph_matching_number == matching_sizes[0]
    comparison = many.compare_sources(case["source_mean_directions"], source_edges,
                                      case["recovered_mean_directions"], fixed)
    coefficients = comparison["quadratic_scale_and_mean_quadratic_coefficients"]
    assert coefficients[0] and not any(coefficients[1:])
    report["source_comparison_after_sparse_correction"] = comparison
    report["only_quadratic_scale_remains_after_mean_alignment"] = True
    case["sparse_reconstruction"] = report
    return case


def run():
    star = [(0, j) for j in range(1, 5)]
    cycle = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)]
    four_star = [(0, j) for j in range(1, 4)]
    return {"cases": [finish_case(many.run(3, 5, graph=star)),
                      finish_case(many.run(3, 5, graph=cycle)),
                      finish_case(many.run(3, 4, graph=four_star))]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minimal-local", action="store_true",
                        help="Check four- and five-site stars with three-dimensional local spaces.")
    args = parser.parse_args()
    result = {"cases": [finish_case(many.run(3, n, local=3, graph=[(0, j) for j in range(1, n)]))
                         for n in [4, 5]]} if args.minimal_local else run()
    print(json.dumps(result, indent=2))

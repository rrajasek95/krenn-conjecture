#!/usr/bin/env python3
"""Independent moment construction and exterior-Pfaffian audit.

Rebuilds moments by matching enumeration (the recovery uses recursion),
and the exterior matrix by its unique complementary colour at each site.
"""

import itertools
import json
from pathlib import Path

import numpy as np

from audit_pair_observation import pfaffian
import many_direction as many


def full_moment(means, edges):
    _, _, layers = many.responses([means], edges)
    return [sum(values) % many.P for values in zip(*layers.values())]


def exterior_matrix(tensor, n, p):
    words = list(itertools.product(range(3), repeat=n))
    index = {word: i for i, word in enumerate(words)}
    matrix = np.zeros((len(words), len(words)), dtype=np.int64)
    for row, a in enumerate(words):
        for b in itertools.product(*(tuple(c for c in range(3) if c != colour) for colour in a)):
            column = index[b]
            if column <= row:
                continue
            complement, sign = 0, 1
            for x, y in zip(a, b):
                complement = 3 * complement + 3 - x - y
                sign *= 1 if y == (x + 1) % 3 else -1
            value = sign * tensor[complement] % p
            matrix[row, column], matrix[column, row] = value, -value % p
    return matrix


def run():
    saved = json.loads(Path(__file__).with_name("single-source-certificate.json").read_text())
    reports = []
    for case in saved["cases"]:
        p, n = case["prime"], case["sites"]
        edges = {tuple(e["sites"]): e["weights"] for e in case["source_edges"]}
        tensor = full_moment(case["source_means"], edges)
        for answer in case["recovered_candidates"]:
            recovered_edges = {tuple(e["sites"]): e["weights"] for e in answer["edges"]}
            assert full_moment(answer["means"], recovered_edges) == tensor
        matrix = exterior_matrix(tensor, n, p)
        indices = case["exterior_principal_minor_indices"]
        value = pfaffian(matrix[np.ix_(indices, indices)], p)
        assert value and value * value % p == case["exterior_principal_minor_determinant"]
        reports.append({"sites": n, "prime": p, "independent_matching_expansion_passed": True,
                        "principal_minor_order": len(indices), "pfaffian": value,
                        "determinant": value * value % p})
    return {"cases": reports}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

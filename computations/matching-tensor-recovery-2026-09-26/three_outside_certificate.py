#!/usr/bin/env python3
"""Exact low-degree exterior certificates for single-output covariance recovery.

Computes ker A(T) restricted to F_3, not the full exterior kernel. Source
means define the F_3 chart for the rank witness; this is not a blind inverse
implementation. The all-orders direction theorem and the written rigidity
argument supply the remaining identifiability steps.
"""

import itertools
import json
import math
import random

from flint import nmod_mat

import single_source as single
import single_kernel_probes as probes
from audit_pair_observation import moments

P, base = single.P, single.base


def outside_flow_matrix(n, edges):
    labels = [(i, a, j) for i in range(n) for a in [1, 2]
              for j in [k for k in range(n) if k != i][1:]]
    rows = []
    for sites in itertools.combinations(range(n), 3):
        for colours in itertools.product([1, 2], repeat=3):
            word = dict(zip(sites, colours))
            row = []
            for i, a, j in labels:
                if i not in sites or word[i] != a:
                    row.append(0)
                    continue
                k, l = [site for site in sites if site != i]
                anchor = next(site for site in range(n) if site != i)
                coefficient = int(anchor in (k, l)) - int(j in (k, l))
                row.append(coefficient * edges[k, l][word[k]][word[l]] % P)
            rows.append(row)
    return nmod_mat(rows, P)


def direct_entry(tensor, row_word, column_word):
    if any(a == b for a, b in zip(row_word, column_word)):
        return 0
    complement, sign = 0, 1
    for a, b in zip(row_word, column_word):
        complement = 3 * complement + 3 - a - b
        # Explicit alternating-symbol lookup, independently of column assembly.
        sign *= 1 if (a, b, 3 - a - b) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)] else -1
    return sign * tensor[complement] % P


def run(n):
    seed = 271940
    rng = random.Random(seed)
    means = [[1, 0, 0] for _ in range(n)]
    edges = {e: [[rng.randrange(P) for _ in range(3)] for _ in range(3)]
             for e in itertools.combinations(range(n), 2)}
    tensor = moments(means, edges, P)
    all_words = list(itertools.product(range(3), repeat=n))
    words = [word for word in all_words if sum(a != 0 for a in word) <= 3]
    matrix = probes.exterior_columns(tensor, n, words)
    terminal = [int(not any(word)) for word in words]
    one_edge = [sum(block[word[i]][word[j]] for (i, j), block in edges.items()
                    if all(word[k] == 0 for k in range(n) if k not in (i, j))) % P
                for word in words]
    response = base.columns([terminal, one_edge])
    assert response.rank() == 2 and (matrix * response).rank() == 0
    minor = base.full_rank_minor(matrix)
    assert minor["rank"] == len(words) - 2
    # Rebuild every selected minor entry without the sparse-column routine.
    independent = nmod_mat([[direct_entry(tensor, all_words[i], words[j]) for j in minor["columns"]]
                            for i in minor["rows"]], P)
    assert int(independent.det()) == minor["determinant"] != 0
    flow = outside_flow_matrix(n, edges)
    flow_minor = base.full_rank_minor(flow)
    assert flow_minor["rank"] == 2 * n * (n - 2)
    assert all(any(block[a][b] for a in [1, 2] for b in [1, 2]) for block in edges.values())
    top_indices = [i for i, word in enumerate(all_words) if sum(a != 0 for a in word) == n - 1 and tensor[i]]
    assert top_indices
    # Independent matching enumeration checks representative input entries.
    sample_indices = sorted(set([0, 1, len(tensor) // 2, len(tensor) - 1, top_indices[0]]
                                + [rng.randrange(len(tensor)) for _ in range(20)]))
    for index in sample_indices:
        word, value = all_words[index], 0
        for singles, pairs in base.exterior.matchings(list(range(n))):
            term = math.prod(means[i][word[i]] for i in singles)
            term *= math.prod(edges[i, j][word[i]][word[j]] for i, j in pairs)
            value = (value + term) % P
        assert value == tensor[index]
    return {"sites": n, "local_dimension": 3, "seed": seed, "prime": P,
            "source_means": means,
            "source_edges": [{"sites": list(e), "weights": block} for e, block in edges.items()],
            "f3_dimension": len(words), "restricted_kernel_dimension": 2,
            "restricted_exterior_minor": minor,
            "selected_minor_rebuilt_entrywise": True,
            "outside_flow_minor": flow_minor,
            "nonzero_top_outside_entry": {"word": list(all_words[top_indices[0]]), "value": tensor[top_indices[0]]},
            "independent_matching_entry_indices": sample_indices,
            "scope": "Generic rank witness, not a full blind reconstruction or a full-kernel computation."}


if __name__ == "__main__":
    print(json.dumps({"cases": [run(n) for n in [5, 7, 9]]}, indent=2))

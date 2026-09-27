#!/usr/bin/env python3
"""Exact tests of the three-copy identity for a two-dimensional mean space.

Uses only the standard library; prints JSON and writes no files.
"""

import itertools
import json
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "matching-tensor-exterior-2026-09-26"))
import verify as exterior

P = 1009


def cubic(u, v, w, ws):
    rows = exterior.exterior_sparse(w, ws, P)
    image = [sum(value * v[j] for j, value in row) % P for row in rows]
    return sum(x * y for x, y in zip(u, image)) % P


def run():
    rng = random.Random(175)
    reports = []
    for n in (3, 5):
        ws = exterior.words(n)
        means = [[[rng.randrange(P) for _ in range(3)] for _ in range(n)] for _ in range(3)]
        edges = {
            (i, j): [[rng.randrange(P) for _ in range(3)] for _ in range(3)]
            for i, j in itertools.combinations(range(n), 2)
        }
        layers = {(a, k - a): [0] * len(ws) for k in range(1, n + 1, 2) for a in range(k + 1)}
        for unmatched, matching in exterior.matchings(list(range(n))):
            for z, w in enumerate(ws):
                edge_value = 1
                for i, j in matching:
                    edge_value = edge_value * edges[i, j][w[i]][w[j]] % P
                polynomial = [1]
                for i in unmatched:
                    updated = [0] * (len(polynomial) + 1)
                    for a, value in enumerate(polynomial):
                        updated[a] = (updated[a] + value * means[1][i][w[i]]) % P
                        updated[a + 1] = (updated[a + 1] + value * means[0][i][w[i]]) % P
                    polynomial = updated
                for a, value in enumerate(polynomial):
                    key = (a, len(unmatched) - a)
                    layers[key][z] = (layers[key][z] + edge_value * value) % P
        values = list(layers.values())
        checks = 0
        for i, j, k in itertools.combinations(range(len(values)), 3):
            assert cubic(values[i], values[j], values[k], ws) == 0
            checks += 1
        span_dimension = exterior.rank(values, P)
        assert span_dimension == len(values)
        # Three independent root directions can violate the two-direction identity.
        root_responses = []
        for mean in means:
            tensor = [0] * len(ws)
            for unmatched, matching in exterior.matchings(list(range(n))):
                if len(unmatched) != 1:
                    continue
                for z, w in enumerate(ws):
                    i = unmatched[0]
                    value = mean[i][w[i]]
                    for i, j in matching:
                        value = value * edges[i, j][w[i]][w[j]] % P
                    tensor[z] = (tensor[z] + value) % P
            root_responses.append(tensor)
        obstruction = cubic(*root_responses, ws)
        assert obstruction == {3: 729, 5: 594}[n]
        reports.append({
            "sites": n,
            "two_direction_response_dimension": span_dimension,
            "triples_checked": checks,
            "all_two_direction_cubics_zero": True,
            "three_direction_root_response_cubic": obstruction,
            "source_mean_directions": means,
            "source_edges": [{"sites": list(edge), "weights": value} for edge, value in edges.items()],
        })
    return {"prime": P, "seed": 175, "cases": reports,
            "scope": "Zero identities are proved analytically; samples check implementation. Nonzero residues certify explicit joint-model obstructions over C."}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

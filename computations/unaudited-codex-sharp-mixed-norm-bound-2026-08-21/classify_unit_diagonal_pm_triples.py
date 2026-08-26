#!/usr/bin/env python3
"""Exact S8 x S3 classification of unit diagonal one-factor triples on K8."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_unit_diagonal_pm_triples.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(u, v):
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(u, v),) + tail))


PMS = tuple(perfect_matchings(range(8)))
M0 = ((0, 1), (2, 3), (4, 5), (6, 7))


def colored_profile(triple):
    edge_colours = defaultdict(list)
    for colour, matching in enumerate(triple):
        for e in matching:
            edge_colours[e].append(colour)
    amplitudes = Counter()
    coloured_terms = 0
    physical_matchings = 0
    for matching in PMS:
        choices = [edge_colours[e] for e in matching]
        if not all(choices):
            continue
        physical_matchings += 1
        for colours in product(*choices):
            word = [None] * 8
            for (u, v), colour in zip(matching, colours):
                word[u] = word[v] = colour
            word = tuple(word)
            amplitudes[word] += 1
            coloured_terms += len(set(word)) > 1
    require([amplitudes[(colour,) * 8] for colour in range(3)] == [1, 1, 1],
            (triple, amplitudes))
    mixed = {word: value for word, value in amplitudes.items()
             if len(set(word)) > 1}
    return {
        "P": sum(value * value for value in mixed.values()),
        "mixed_words": len(mixed),
        "mixed_coloured_terms": coloured_terms,
        "max_mixed_amplitude": max(mixed.values(), default=0),
        "physical_matchings": physical_matchings,
    }


def cycle_type(left, right):
    adjacency = defaultdict(list)
    common = set(left) & set(right)
    for matching in (left, right):
        for u, v in matching:
            if (u, v) in common:
                continue
            adjacency[u].append(v)
            adjacency[v].append(u)
    unseen = set(adjacency)
    lengths = []
    while unseen:
        root = next(iter(unseen))
        stack = [root]
        component = set()
        while stack:
            u = stack.pop()
            if u in component:
                continue
            component.add(u)
            stack.extend(adjacency[u])
        unseen -= component
        lengths.append(len(component))
    return (len(common), tuple(sorted(lengths)))


def transform_matching(matching, permutation):
    return tuple(sorted(edge(permutation[u], permutation[v]) for u, v in matching))


def stabilizer_m0():
    answer = []
    for edge_order in permutations(range(4)):
        for flips in product(range(2), repeat=4):
            permutation = [None] * 8
            for source_index, (u, v) in enumerate(M0):
                target = M0[edge_order[source_index]]
                if flips[source_index]:
                    target = target[::-1]
                permutation[u], permutation[v] = target
            answer.append(tuple(permutation))
    require(len(set(answer)) == 384, len(set(answer)))
    return tuple(answer)


STABILIZER = stabilizer_m0()


def one_map_to_m0(matching):
    permutation = [None] * 8
    for (u, v), (a, b) in zip(sorted(matching), M0):
        permutation[u], permutation[v] = a, b
    permutation = tuple(permutation)
    require(transform_matching(matching, permutation) == M0, matching)
    return permutation


def compose(left, right):
    return tuple(left[right[index]] for index in range(8))


def canonical_full(triple):
    candidates = []
    for distinguished in range(3):
        first_map = one_map_to_m0(triple[distinguished])
        others = [index for index in range(3) if index != distinguished]
        for symmetry in STABILIZER:
            permutation = compose(symmetry, first_map)
            pair = sorted(transform_matching(triple[index], permutation)
                          for index in others)
            candidates.append(tuple(pair))
    return min(candidates)


def union_invariants(triple):
    edges = set().union(*map(set, triple))
    adjacency = defaultdict(set)
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    triangles = sum(
        all(edge in edges for edge in combinations(vertices, 2))
        for vertices in combinations(range(8), 3)
    )
    return {
        "distinct_physical_edges": len(edges),
        "degree_sequence": tuple(sorted(map(len, adjacency.values()))),
        "triangles": triangles,
        "pair_cycle_types": tuple(sorted(cycle_type(*pair)
                                         for pair in combinations(triple, 2))),
    }


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-minimum", action="store_true")
    args = parser.parse_args()
    distribution = Counter()
    term_distribution = Counter()
    minimizers = []
    residual = []
    for m1 in PMS:
        for m2 in PMS:
            triple = (M0, m1, m2)
            data = colored_profile(triple)
            distribution[data["P"]] += 1
            term_distribution[data["mixed_coloured_terms"]] += 1
            pair_types = tuple(cycle_type(*pair) for pair in combinations(triple, 2))
            if all(common == 0 and cycles == (8,) for common, cycles in pair_types):
                residual.append((triple, data))
            if not minimizers or data["P"] < minimizers[0][1]["P"]:
                minimizers = [(triple, data)]
            elif data["P"] == minimizers[0][1]["P"]:
                minimizers.append((triple, data))

    minimum = minimizers[0][1]["P"] + int(args.mutate_minimum)
    require(minimum == 2, minimum)
    require(len(minimizers) == 864, len(minimizers))
    require(all(data["mixed_coloured_terms"] == 2 and data["mixed_words"] == 2
                and data["max_mixed_amplitude"] == 1
                for _, data in minimizers), "minimizer collision")
    minimizer_pair_types = Counter(
        tuple(sorted(cycle_type(*pair) for pair in combinations(triple, 2)))
        for triple, _ in minimizers
    )

    orbit_groups = defaultdict(list)
    for triple, data in minimizers:
        orbit_groups[canonical_full(triple)].append((triple, data))

    residual_distribution = Counter(data["P"] for _, data in residual)
    print("ordered triples", len(PMS) ** 2)
    print("P minimum/count", minimum, len(minimizers))
    print("minimum pair-type distribution", dict(minimizer_pair_types))
    print("P distribution", dict(sorted(distribution.items())))
    print("pairwise-Hamiltonian residual", len(residual),
          dict(sorted(residual_distribution.items())))
    print("minimum S8xS3 orbits", len(orbit_groups))
    orbit_rows = []
    for index, (key, records) in enumerate(sorted(orbit_groups.items()), 1):
        triple = (M0,) + key
        print("orbit", index, "fixed-M0 ordered count", len(records),
              "profile", records[0][1], "invariants", union_invariants(triple),
              "representative", triple)
        orbit_rows.append({
            "fixed_M0_ordered_count": len(records),
            "full_S8xS3_orbit_size": 105 * len(records),
            "profile": records[0][1],
            "invariants": {
                **union_invariants(triple),
                "degree_sequence": list(union_invariants(triple)["degree_sequence"]),
                "pair_cycle_types": [str(value) for value in union_invariants(triple)["pair_cycle_types"]],
            },
            "representative": [[list(edge) for edge in matching] for matching in triple],
        })
    payload = {
        "status": "PASS exact unit-diagonal balanced PM-triple theorem",
        "fixed_factor_ordered_triples": len(PMS) ** 2,
        "minimum_P_mixed": minimum,
        "minimum_fixed_factor_count": len(minimizers),
        "minimum_S8xS3_orbits": len(orbit_groups),
        "P_distribution": {str(key): value for key, value in sorted(distribution.items())},
        "pairwise_Hamiltonian_residual": {
            "count": len(residual),
            "P_distribution": {str(key): value for key, value in sorted(residual_distribution.items())},
        },
        "equality_orbits": orbit_rows,
        "phase_independence": (
            "Moment zero makes the four cells in each colour factor have one "
            "magnitude; pure product one makes it unit. A word uniquely "
            "determines its matching, so phases cannot cancel and P is the "
            "number of non-pure supported coloured matchings."
        ),
        "proof_split": (
            "Two independent alternating components in any pair give two "
            "mixed switches. The pairwise-Hamiltonian residue has 960 records, "
            "closed by the exact finite census: 576 at P=2 and 384 at P=3."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()

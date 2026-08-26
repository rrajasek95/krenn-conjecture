#!/usr/bin/env python3
"""Exhaustive finite checker for the balanced-row cycle-Morse pivot lemma."""

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = (ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
          / "audit_orbit0_t2_pivot_setup.py")
OUT = HERE / "results_cycle_morse_pivot_lemma.json"
M0 = ((0, 1), (2, 3), (4, 5), (6, 7))
ANCHORS = {(u, v, c, c) for u, v in M0 for c in range(3)}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    u = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        v = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(tuple(sorted(((u, v),) + tail)))
    return tuple(sorted(set(answer)))


PM8 = perfect_matchings(tuple(range(8)))


def connection_partition(left, right):
    """Cycle sizes in the 2-regular multigraph left union right.

    Size counts left-matching edges (contracted deleted-cycle paths), not
    physical endpoint vertices.  Parallel left/right edges give a 1-cycle.
    """
    adjacency = [[] for _ in range(8)]
    for edge_id, (u, v) in enumerate(left + right):
        adjacency[u].append((edge_id, v))
        adjacency[v].append((edge_id, u))
    seen = set()
    parts = []
    for seed in range(8):
        if seed in seen:
            continue
        stack = [seed]
        seen.add(seed)
        vertices = 0
        while stack:
            u = stack.pop()
            vertices += 1
            for _edge, v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        require(vertices % 2 == 0, (left, right, vertices))
        parts.append(vertices // 2)
    return tuple(sorted(parts))


def term(word, matching):
    return tuple((u, v, word[u], word[v]) for u, v in matching)


def k_degree(matching_term):
    return sum(cell not in ANCHORS for cell in matching_term)


def main():
    require(len(PM8) == 105, len(PM8))
    connection_types = Counter()
    cycle_counts = Counter()
    unique_top = 0
    for selected in PM8:
        local_top = []
        for completion in PM8:
            partition = connection_partition(selected, completion)
            connection_types[partition] += 1
            cycle_counts[len(partition)] += 1
            if len(partition) == 4:
                local_top.append(completion)
        require(local_top == [selected], (selected, local_top))
        unique_top += 1
    require(connection_types == {
        (1, 1, 1, 1): 105,
        (1, 1, 2): 1260,
        (1, 3): 3360,
        (2, 2): 1260,
        (4,): 5040,
    }, connection_types)

    word_profiles = Counter()
    selected_k = Counter()
    k_increase = Counter()
    mixed_words = 0
    decorated_selected_terms = 0
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        mixed_words += 1
        word_profiles[tuple(sorted(Counter(word).values(), reverse=True))] += 1
        degrees = tuple(k_degree(term(word, matching)) for matching in PM8)
        require(max(degrees) == 4, (word, degrees))
        for degree in degrees:
            selected_k[degree] += 1
            k_increase[max(degrees) - degree] += 1
            decorated_selected_terms += 1
    require(mixed_words == 6558 and decorated_selected_terms == 688590,
            (mixed_words, decorated_selected_terms))
    require(k_increase == {0: 569736, 1: 107472, 2: 10656,
                           3: 648, 4: 78}, k_increase)

    # Hostile guard: when the deleted paths are not paired by the selected
    # PM (the combinatorial signature of selecting >=2 edges on one old
    # cycle), the selected completion need not be the unique maximum.
    path_pairing = PM8[0]
    selected = PM8[1]
    selected_cycles = len(connection_partition(path_pairing, selected))
    peers = [completion for completion in PM8
             if len(connection_partition(path_pairing, completion))
             == selected_cycles]
    require(len(peers) > 1, "hostile non-distinct-cycle mutation did not fire")

    result = {
        "status": "PASS exhaustive cycle-Morse pivot lemma",
        "literal_physical_matchings": len(PM8),
        "ordered_connection_checks": len(PM8) ** 2,
        "connection_partition_histogram": {
            "+".join(map(str, key)): value
            for key, value in sorted(connection_types.items())
        },
        "output_cycle_count_histogram": dict(sorted(cycle_counts.items())),
        "unique_top_completions": unique_top,
        "mixed_words": mixed_words,
        "decorated_selected_terms": decorated_selected_terms,
        "selected_term_K_degree_histogram": dict(sorted(selected_k.items())),
        "maximum_K_increase_histogram": dict(sorted(k_increase.items())),
        "K_formula": "K(U+N)=K(R)-K(M)+K(N)",
        "K16_full_column_condition": "max_N K(N)-K(M) <= 16-K(R)",
        "K16_projection_condition": "K(R)<=16; terms of K>16 vanish modulo K^17",
        "hostile_non_distinct_cycle_peer_completions": len(peers),
        "source_provider_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("cycle-Morse pivot lemma: PASS")
    print("connection/cycle histograms:", connection_types, cycle_counts)
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()

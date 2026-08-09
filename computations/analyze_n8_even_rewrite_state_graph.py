#!/usr/bin/env python3
"""Bounded census of the source-faithful even-complement rewrite graph.

This is an exploratory theorem-extraction tool.  A state is a canonical
24-port matching (twelve endpoint-colour cells).  A rewrite removes a mixed
vertex perfect matching whose eight-edge complement consists only of even
cycles, and inserts any matching term from the same output fibre.  Such a
state remains in the three-one-factor sector because the even complement
splits into two vertex matchings.

The script deliberately caps breadth/depth.  Its purpose is to test proposed
well-founded statistics and to expose the smallest plateau/sink families;
reachability alone is not an ideal-membership proof.
"""

from __future__ import annotations

from collections import Counter, deque
import argparse
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "verify_n8_target_triple_localization_orbits.py"
SPEC = importlib.util.spec_from_file_location("n8_target_charts", SOURCE_PATH)
CHARTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHARTS)
SOURCE = CHARTS.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def component_sizes(edges):
    adjacency = [set() for _ in range(8)]
    for first, second in edges:
        left, right = first // 3, second // 3
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(range(8))
    answer = []
    while unseen:
        root = min(unseen)
        component = {root}
        queue = [root]
        while queue:
            vertex = queue.pop()
            for other in adjacency[vertex]:
                if other not in component:
                    component.add(other)
                    queue.append(other)
        unseen -= component
        answer.append(len(component))
    return tuple(sorted(answer, reverse=True))


def diagonal_count(row):
    return sum(
        first % 3 == second % 3
        for first, second in SOURCE.mate_edges(SOURCE.decode_key(row))
    )


def even_columns(row):
    for column in SOURCE.incident_columns(row):
        complement = SOURCE.mate_edges(SOURCE.decode_key(column))
        cycles = component_sizes(complement)
        require(sum(cycles) == 8, "rewrite complement lost a vertex")
        if all(size % 2 == 0 for size in cycles):
            yield column, cycles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--layers", type=int, default=2)
    parser.add_argument("--state-cap", type=int, default=200000)
    arguments = parser.parse_args()

    roots = tuple(sorted(SOURCE.target_orbit_rows()))
    require(len(roots) == 31, "target chart count changed")
    root_index = {row: index + 1 for index, row in enumerate(roots)}
    distance = {row: 0 for row in roots}
    queue = deque(roots)
    transitions = set()
    cycle_types = Counter()
    delta_diagonal = Counter()
    plateau_edges = 0
    truncated = False

    while queue:
        row = queue.popleft()
        layer = distance[row]
        if layer >= arguments.layers:
            continue
        before = diagonal_count(row)
        for column, cycles in even_columns(row):
            cycle_types[cycles] += 1
            outputs = set(SOURCE.column_outputs(column))
            require(row in outputs, "incident rewrite fibre lost its source state")
            for other in outputs:
                if other == row:
                    continue
                edge = (row, column, other)
                transitions.add(edge)
                after = diagonal_count(other)
                delta_diagonal[after - before] += 1
                plateau_edges += after == before
                if other in distance:
                    continue
                if len(distance) >= arguments.state_cap:
                    truncated = True
                    continue
                distance[other] = layer + 1
                queue.append(other)

    layer_histogram = Counter(distance.values())
    diagonal_histogram = Counter(map(diagonal_count, distance))
    root_reach = Counter(
        root_index[row] for row in distance if row in root_index
    )
    # Rewriting a pure anchor moves toward larger purity defect, hence toward
    # *fewer* diagonal endpoint-colour cells.  Record every discovered
    # nonroot state with no outgoing strict decrease inside the audited
    # layers; these are the counterfrontier for this first Morse statistic.
    decreasing_sources = {
        row for row, _column, other in transitions
        if diagonal_count(other) < diagonal_count(row)
    }
    audited_nonroots = {
        row for row, layer in distance.items()
        if row not in root_index and layer < arguments.layers
    }
    diagonal_sinks = audited_nonroots - decreasing_sources

    print("roots:", len(roots))
    print("layers/state cap/truncated:",
          arguments.layers, arguments.state_cap, truncated)
    print("state layers:", dict(sorted(layer_histogram.items())))
    print("states/transitions:", len(distance), len(transitions))
    print("even complement cycle types:", dict(sorted(cycle_types.items())))
    print("diagonal-cell histogram:", dict(sorted(diagonal_histogram.items())))
    print("rewrite delta diagonal:", dict(sorted(delta_diagonal.items())))
    print("plateau transitions:", plateau_edges)
    print("audited strict-diagonal-decrease sinks:", len(diagonal_sinks))
    print("target roots retained:", dict(sorted(root_reach.items())))
    print("scope: bounded support rewrite census, not a Morse certificate")


if __name__ == "__main__":
    main()

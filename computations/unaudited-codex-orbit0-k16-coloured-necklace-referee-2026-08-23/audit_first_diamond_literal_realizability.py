#!/usr/bin/env python3
"""Literal 24-port realization of the first coloured-necklace diamond."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = (ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
          / "audit_coloured_necklace_target_reduction.py")
OUT = HERE / "results_first_diamond_literal_realizability.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


SPEC = importlib.util.spec_from_file_location("necklace_literal_source", SOURCE)
NECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(NECK)


# Each entry is (physical site, colour).  Every colour uses each site once.
CYCLES = (
    ((0, 0), (1, 0)),
    ((2, 0), (3, 0)),
    ((4, 1), (5, 1), (6, 1), (7, 1),
     (0, 2), (1, 2), (2, 2), (5, 2)),
    ((6, 0), (7, 0), (4, 0), (5, 0),
     (0, 1), (1, 1), (2, 1), (3, 1),
     (4, 2), (3, 2), (6, 2), (7, 2)),
)


def edge(left, right):
    require(left[0] != right[0], (left, right, "physical loop"))
    return tuple(sorted((left, right)))


def cycle_edges(cycle):
    return tuple(edge(cycle[index - 1], cycle[index])
                 for index in range(len(cycle)))


def project(edges):
    adjacency = {port: [] for site in range(8) for port in
                 ((site, 0), (site, 1), (site, 2))}
    for edge_id, (left, right) in enumerate(edges):
        adjacency[left].append((edge_id, right))
        adjacency[right].append((edge_id, left))
    require(set(map(len, adjacency.values())) == {2},
            Counter(map(len, adjacency.values())))
    used = set()
    necklaces = []
    for seed_edge in range(len(edges)):
        if seed_edge in used:
            continue
        start, _ = edges[seed_edge]
        vertex = start
        current = seed_edge
        word = []
        while True:
            require(current not in used, (current, edges[current]))
            used.add(current)
            word.append(vertex[1])
            left, right = edges[current]
            next_vertex = right if vertex == left else left
            choices = [edge_id for edge_id, _ in adjacency[next_vertex]
                       if edge_id != current]
            require(len(choices) == 1, (next_vertex, adjacency[next_vertex]))
            vertex, current = next_vertex, choices[0]
            if current == seed_edge:
                require(vertex == start, (vertex, start))
                break
        necklaces.append(tuple(word))
    return NECK.canonical_state(necklaces)


def literal_column(cuts):
    multiplier = []
    endpoint_ports = []
    for cycle, cut in zip(CYCLES, cuts, strict=True):
        edges = cycle_edges(cycle)
        multiplier.extend(value for index, value in enumerate(edges)
                          if index != cut)
        path = cycle[cut:] + cycle[:cut]
        endpoint_ports.extend((path[0], path[-1]))
    require(len(multiplier) == 20, len(multiplier))
    endpoint_by_site = {port[0]: port for port in endpoint_ports}
    require(len(endpoint_by_site) == 8, endpoint_ports)
    word = tuple(endpoint_by_site[site][1] for site in range(8))
    require(len(set(word)) > 1, word)

    outputs = Counter()
    literal_rows = Counter()
    for matching in NECK.PM8:
        added = tuple(edge(endpoint_ports[left], endpoint_ports[right])
                      for left, right in matching)
        row = tuple(sorted(multiplier + list(added)))
        literal_rows[row] += 1
        outputs[project(row)] += 1
    require(sum(outputs.values()) == 105, sum(outputs.values()))
    require(sum(literal_rows.values()) == 105, sum(literal_rows.values()))
    return {
        "cuts": cuts,
        "word": word,
        "multiplier": tuple(sorted(multiplier)),
        "endpoint_ports": tuple(endpoint_ports),
        "outputs": outputs,
        "literal_rows": literal_rows,
    }


def encode_edge(value):
    return f"{value[0][0]}:{value[0][1]}-{value[1][0]}:{value[1][1]}"


def main():
    ports_by_colour = Counter(port[1] for cycle in CYCLES for port in cycle)
    require(ports_by_colour == {0: 8, 1: 8, 2: 8}, ports_by_colour)
    for colour in range(3):
        require({port[0] for cycle in CYCLES for port in cycle
                 if port[1] == colour} == set(range(8)), colour)
    parent_edges = tuple(sorted(edge_value for cycle in CYCLES
                                for edge_value in cycle_edges(cycle)))
    parent = project(parent_edges)
    require(NECK.state_text(parent) == "00.00.11112222.000011112222",
            NECK.state_text(parent))

    first = literal_column((0, 0, 0, 0))
    second = literal_column((0, 0, 0, 1))
    require(first["word"] == (0, 0, 0, 0, 1, 2, 0, 2), first["word"])
    require(second["word"] == (0, 0, 0, 0, 1, 2, 0, 0), second["word"])
    require(first["literal_rows"][parent_edges] == 1,
            first["literal_rows"][parent_edges])
    require(second["literal_rows"][parent_edges] == 1,
            second["literal_rows"][parent_edges])

    for column in (first, second):
        abstract = Counter({parent: 1})
        abstract.update(dict(NECK.relation_children(
            parent, (0, 1, 2, 3), column["cuts"])))
        require(column["outputs"] == abstract,
                (column["cuts"], column["outputs"] - abstract,
                 abstract - column["outputs"]))

    require(first["multiplier"] != second["multiplier"],
            "the two literal source columns unexpectedly coincide")
    # Both source columns contain the same parent row with coefficient one;
    # subtracting them is a literal source syzygy with that row cancelled.
    difference = Counter(first["literal_rows"])
    for row, coefficient in second["literal_rows"].items():
        difference[row] -= coefficient
    difference = Counter({row: coefficient for row, coefficient in difference.items()
                          if coefficient != 0})
    require(parent_edges not in difference, "common leading row did not cancel")

    result = {
        "schema": "orbit0-k16-first-necklace-diamond-literal-v1",
        "status": "PASS_LITERAL_SOURCE_SYZYGY__ABSTRACT_DIAMOND_IS_REAL",
        "parent_state": NECK.state_text(parent),
        "parent_literal_edges": [encode_edge(value) for value in parent_edges],
        "columns": [{
            "cuts": list(column["cuts"]),
            "mixed_word": "".join(map(str, column["word"])),
            "endpoint_ports": [f"{site}:{colour}"
                               for site, colour in column["endpoint_ports"]],
            "multiplier_degree": len(column["multiplier"]),
            "literal_output_terms_with_multiplicity":
                sum(column["literal_rows"].values()),
            "distinct_literal_output_rows": len(column["literal_rows"]),
            "projected_necklace_output_states": len(column["outputs"]),
            "parent_multiplicity": column["literal_rows"][parent_edges],
        } for column in (first, second)],
        "literal_difference": {
            "support": len(difference),
            "l1": sum(abs(value) for value in difference.values()),
            "parent_coefficient": difference.get(parent_edges, 0),
        },
        "theorem_scope": (
            "The first failed critical pair is not an artifact of forgetting "
            "physical sites: the displayed 24-port labelling makes both cut "
            "choices literal mixed source columns, each with the exact 105-term "
            "matching expansion and the same coefficient-one parent. Their "
            "difference is an actual source syzygy."
        ),
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "words": ["".join(map(str, column["word"]))
                  for column in (first, second)],
        "literal_difference_support": len(difference),
        "logical_sha256": logical,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

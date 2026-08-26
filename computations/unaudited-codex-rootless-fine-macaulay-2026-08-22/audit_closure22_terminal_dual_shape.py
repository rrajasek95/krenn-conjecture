#!/usr/bin/env python3
"""Exact combinatorial profile of the terminal 100-column CEGAR dual."""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import permutations
from pathlib import Path
import hashlib
import json
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_closure22_integer_dual_shape import (  # noqa: E402
    EDGES, PAIRS, degree_sequence, rank,
)
from audit_closure22_joint_semigroup import (  # noqa: E402
    PM8, key_add, matching_term, semigroup_key,
)
from audit_physical_graph_quotient import holonomy  # noqa: E402


INPUT = HERE / "results_closure22_joint_cegar.json"
NEW_WORD_INPUT = HERE / "results_terminal_separator_new_x5_words.json"


def components(matrix):
    adjacency = defaultdict(set)
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value:
                adjacency[("G", i)].add(("H", j))
                adjacency[("H", j)].add(("G", i))
    seen = set()
    out = []
    for vertex in adjacency:
        if vertex in seen:
            continue
        stack = [vertex]
        seen.add(vertex)
        current = []
        while stack:
            item = stack.pop()
            current.append(item)
            for neighbour in adjacency[item]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        gs = {index for kind, index in current if kind == "G"}
        hs = {index for kind, index in current if kind == "H"}
        support = sum(matrix[i][j] != 0 for i in gs for j in hs)
        out.append((len(gs), len(hs), support))
    return sorted(out, reverse=True)


def run_audit():
    source = json.loads(INPUT.read_text())
    new_words = json.loads(NEW_WORD_INPUT.read_text())
    dual = source["terminal_integer_dual"]
    columns = [tuple(item["column"]) for item in dual]
    coefficients = [item["coefficient"] for item in dual]
    assert len(columns) == 100
    assert source["terminal_integer_is_full_semigroup_separator"]
    assert source["terminal_integer_crossing_translations"] == 0
    assert source["terminal_integer_target_pairing"] == 1

    graphs = []
    histograms = []
    for column in columns:
        if column[:28] not in graphs:
            graphs.append(column[:28])
        if column[28:] not in histograms:
            histograms.append(column[28:])
    assert len(graphs) == 28
    assert len(histograms) == 14
    assert {degree_sequence(graph) for graph in graphs} == {
        (2, 2, 2, 4, 4, 4, 4, 4)
    }
    assert all(sum(graph) == 13 for graph in graphs)
    assert all(sum(histogram) == 13 for histogram in histograms)

    matrix = [[0] * len(histograms) for _ in graphs]
    for item, column in zip(dual, columns):
        matrix[graphs.index(column[:28])][histograms.index(column[28:])] = (
            item["coefficient"]
        )

    physical_affine_rank = rank([
        [value - graphs[0][j] for j, value in enumerate(graph)]
        for graph in graphs[1:]
    ])
    colour_affine_rank = rank([
        [value - histograms[0][j] for j, value in enumerate(histogram)]
        for histogram in histograms[1:]
    ])
    joint_affine_rank = rank([
        [value - columns[0][j] for j, value in enumerate(column)]
        for column in columns[1:]
    ])
    assert (physical_affine_rank, colour_affine_rank, joint_affine_rank) == (
        9, 5, 14
    )

    histogram_marginals = [sum(row[j] for row in matrix) for j in range(14)]
    assert histogram_marginals == [0] * 13 + [-1]
    component_profile = components(matrix)
    assert component_profile == [(21, 13, 93), (7, 1, 7)]

    first_moment = [
        sum(coefficient * column[j] for coefficient, column in zip(coefficients, columns))
        for j in range(37)
    ]
    assert sum(coefficients) == -1
    assert sum(value != 0 for value in first_moment) == 22

    # The simple cut-colour equation of the initial 16-column separator is
    # not a relation on the terminal support.
    edge01 = EDGES.index((0, 1))
    h01 = 28 + PAIRS.index((0, 1))
    h11 = 28 + PAIRS.index((1, 1))
    h12 = 28 + PAIRS.index((1, 2))
    initial_cut_failures = sum(
        2 * column[edge01]
        != 2 * column[h01] + column[h11] + column[h12] - 4
        for column in columns
    )
    assert initial_cut_failures == 62

    orbit_profiles = []
    for index, histogram in enumerate(histograms):
        orbit = {
            tuple(
                histogram[3 * permutation[a] + permutation[b]]
                for a in range(3) for b in range(3)
            )
            for permutation in permutations(range(3))
        }
        transpose = tuple(
            histogram[3 * b + a] for a in range(3) for b in range(3)
        )
        orbit_profiles.append({
            "histogram": index + 1,
            "global_s3_orbit_size": len(orbit),
            "transpose_histogram": (
                histograms.index(transpose) + 1
                if transpose in histograms else None
            ),
        })
    assert all(item["global_s3_orbit_size"] == 6 for item in orbit_profiles)

    # Only the last three supported columns meet the target; this is the
    # seven-leaf isolated H14 component inherited from the first separator.
    cone = semigroup_key(matching_term((0,) * 8, PM8[0]))
    target = {}
    for term, coefficient in holonomy().items():
        key = key_add(cone, semigroup_key(term))
        target[key] = (target.get(key, 0) + coefficient) % 32003
    target_hits = []
    for index, (coefficient, column) in enumerate(zip(coefficients, columns), 1):
        target_coefficient = target.get(column, 0)
        if target_coefficient > 16001:
            target_coefficient -= 32003
        if target_coefficient:
            target_hits.append((index, coefficient, target_coefficient))
    assert target_hits == [(98, 1, 1), (99, -1, 2), (100, 1, 2)]

    census = new_words["census"]
    family = new_words["minimal_new_symmetry_family"]
    generator = new_words["minimal_new_word_generator"]
    literal_killer = new_words["minimal_new_literal_killer"]
    assert (
        census["new_crossing_words"],
        census["new_crossing_translated_rows"],
        census["existing_closure22_crossing_words"],
    ) == (4294, 44127, 0)
    assert census["shape_census"][0] == {
        "shape": [7, 1],
        "full_S8xS3_orbit_size": 48,
        "crossing_words": 7,
        "crossing_translated_rows": 87,
    }
    assert family["additional_words_to_complete_orbit"] == 40
    assert len(family["already_present_closure22_words"]) == 8
    assert generator == {
        "already_in_closure22": False,
        "crossing_translations": 4,
        "full_S8xS3_orbit_size": 48,
        "pairing_histogram": {"-1": 4},
        "shape": [7, 1],
        "word": "00000200",
    }

    record = {
        "status": "PASS terminal closure22 integer-dual shape",
        "scope": (
            "Full separator for every abstract degree-13 joint-semigroup "
            "translation of the 22 closure words; not a higher-degree or "
            "literal decorated-ring ideal certificate."
        ),
        "support": len(columns),
        "coefficient_profile": dict(sorted(Counter(coefficients).items())),
        "coefficient_sum": sum(coefficients),
        "physical_graphs": len(graphs),
        "colour_histograms": len(histograms),
        "physical_degree_sequence": list(degree_sequence(graphs[0])),
        "physical_affine_rank": physical_affine_rank,
        "colour_affine_rank": colour_affine_rank,
        "joint_affine_rank": joint_affine_rank,
        "nonconstant_marginal_intersection_dimension": (
            physical_affine_rank + colour_affine_rank - joint_affine_rank
        ),
        "coefficient_matrix_rank": rank(matrix),
        "support_component_profile_G_H_columns": component_profile,
        "histogram_marginals": histogram_marginals,
        "histogram_orbits": orbit_profiles,
        "initial_cut_colour_formula_failures": initial_cut_failures,
        "toric_circuit_first_moment_zero": False,
        "first_moment_nonzero_coordinates": sum(value != 0 for value in first_moment),
        "target_hits_index_dualcoeff_targetcoeff": target_hits,
        "recognition": (
            "A 93-term rank-6 relative edge-colour correction with zero "
            "colour marginal, plus a seven-term rank-1 H14 graph residue. "
            "It is not one signed minor, cycle, or cut functional."
        ),
        "terminal_full_semigroup_separator": True,
        "terminal_target_pairing": source["terminal_integer_target_pairing"],
        "new_word_counterguard": {
            "crossing_words": census["new_crossing_words"],
            "crossing_translations": census["new_crossing_translated_rows"],
            "smallest_shape": census["shape_census"][0],
            "cheapest_new_generator": generator,
            "orbit_already_present": len(family["already_present_closure22_words"]),
            "orbit_additional_words": family["additional_words_to_complete_orbit"],
            "sparsest_literal_killer_word": literal_killer["word"],
            "sparsest_literal_killer_pairing": literal_killer["pairing"],
        },
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    record["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return record


def main():
    print(json.dumps(run_audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

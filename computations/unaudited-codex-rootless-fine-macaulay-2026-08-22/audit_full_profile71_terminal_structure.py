#!/usr/bin/env python3
"""Exact structure and next-word audit for the full profile71 Z dual."""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations, product
from math import factorial
from pathlib import Path
import json
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_closure22_integer_dual_shape import EDGES, degree_sequence, rank
from audit_physical_graph_quotient import PM8


DUAL_FILE = HERE / "results_closure22_plus_full_profile71_rational_dual.json"
SOURCE_FILE = HERE / "results_closure22_plus_full_profile71_joint_cegar_rust_p32003.json"
RESULT_FILE = HERE / "results_full_profile71_terminal_structure.json"


def word_shape(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def orbit_size(shape):
    site_orbit = factorial(8)
    for count in shape:
        site_orbit //= factorial(count)
    colour_orbit = factorial(3) // factorial(3 - len(shape))
    for multiplicity in Counter(shape).values():
        colour_orbit //= factorial(multiplicity)
    return site_orbit * colour_orbit


def components(matrix):
    adjacency = defaultdict(set)
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value:
                adjacency[("G", i)].add(("H", j))
                adjacency[("H", j)].add(("G", i))
    seen = set()
    answer = []
    for vertex in adjacency:
        if vertex in seen:
            continue
        stack = [vertex]
        seen.add(vertex)
        vertices = []
        while stack:
            item = stack.pop()
            vertices.append(item)
            for neighbour in adjacency[item]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        gs = sorted(index for kind, index in vertices if kind == "G")
        hs = sorted(index for kind, index in vertices if kind == "H")
        block = [[matrix[i][j] for j in hs] for i in gs]
        answer.append({
            "physical_graphs": len(gs),
            "colour_histograms": len(hs),
            "support": sum(value != 0 for row in block for value in row),
            "rank": rank(block),
        })
    return sorted(answer, key=lambda item: tuple(item.values()), reverse=True)


def compatible_columns(dual):
    edge_index = {edge: index for index, edge in enumerate(EDGES)}
    answer = []
    for matching in PM8:
        indices = [edge_index[edge] for edge in matching]
        current = []
        for column, coefficient in dual.items():
            if not all(column[index] for index in indices):
                continue
            physical = list(column[:28])
            for index in indices:
                physical[index] -= 1
            current.append((tuple(physical), column[28:], coefficient))
        answer.append(current)
    assert sum(map(len, answer)) == 339
    return answer


def word_pairings(word, compatible):
    pairings = defaultdict(int)
    for matching, columns in zip(PM8, compatible):
        histogram = [0] * 9
        for u, v in matching:
            histogram[3 * word[u] + word[v]] += 1
        for physical, colour, coefficient in columns:
            if all(colour[i] >= histogram[i] for i in range(9)):
                quotient = physical + tuple(
                    colour[i] - histogram[i] for i in range(9)
                )
                pairings[quotient] += coefficient
    return {quotient: value for quotient, value in pairings.items() if value}


def serialize_translation(translation):
    return {
        "physical_edges": [
            [u, v, value]
            for (u, v), value in zip(EDGES, translation[:28]) if value
        ],
        "ordered_colour_pairs": [
            [index // 3, index % 3, value]
            for index, value in enumerate(translation[28:]) if value
        ],
    }


def literal_multiplier(translation):
    edges = [
        edge for edge, multiplicity in zip(EDGES, translation[:28])
        for _ in range(multiplicity)
    ]
    pairs = [
        (index // 3, index % 3)
        for index, multiplicity in enumerate(translation[28:])
        for _ in range(multiplicity)
    ]
    assert len(edges) == len(pairs) == 9
    return [[u, v, a, b] for (u, v), (a, b) in zip(edges, pairs)]


def audit():
    dual_record = json.loads(DUAL_FILE.read_text())
    source = json.loads(SOURCE_FILE.read_text())
    assert dual_record["status"] == "PASS exact characteristic-zero separator"
    assert dual_record["translation_crossings"] == 0
    assert dual_record["target_pairing"] == 2
    assert len(source["source_words"]) == 62
    dual = {
        tuple(item["column"]): item["coefficient"]
        for item in dual_record["dual"]
    }
    assert len(dual) == 196
    columns = list(dual)
    coefficients = [dual[column] for column in columns]

    graphs = []
    histograms = []
    for column in columns:
        if column[:28] not in graphs:
            graphs.append(column[:28])
        if column[28:] not in histograms:
            histograms.append(column[28:])
    assert (len(graphs), len(histograms)) == (61, 15)
    assert {degree_sequence(graph) for graph in graphs} == {
        (2, 2, 2, 4, 4, 4, 4, 4)
    }
    matrix = [[0] * len(histograms) for _ in graphs]
    for column, coefficient in dual.items():
        matrix[graphs.index(column[:28])][histograms.index(column[28:])] = coefficient
    component_profile = components(matrix)
    assert component_profile == [{
        "physical_graphs": 61,
        "colour_histograms": 15,
        "support": 196,
        "rank": 7,
    }]
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
        14, 5, 19
    )
    first_moment = [
        sum(coefficient * column[j] for column, coefficient in dual.items())
        for j in range(37)
    ]
    assert sum(coefficients) == -2
    assert sum(value != 0 for value in first_moment) == 28

    histogram_set = set(histograms)
    histogram_orbit_intersections = []
    for histogram in histograms:
        orbit = {
            tuple(
                histogram[3 * permutation[a] + permutation[b]]
                for a in range(3) for b in range(3)
            )
            for permutation in permutations(range(3))
        }
        histogram_orbit_intersections.append(len(orbit.intersection(histogram_set)))
    assert Counter(histogram_orbit_intersections) == {1: 15}

    compatible = compatible_columns(dual)
    admitted = set(source["source_words"])
    source_shape_counts = Counter(word_shape(tuple(map(int, word))) for word in admitted)
    census = defaultdict(lambda: {
        "crossing_words": 0,
        "crossing_translations": 0,
        "one_translation_words": 0,
        "minimum_crossings": None,
        "lex_first_minimum_word": None,
        "pairing_histogram": Counter(),
    })
    total_crossing_words = 0
    total_crossing_translations = 0
    global_minimum = None
    killer_pairings = None
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        shape = word_shape(word)
        pairings = word_pairings(word, compatible)
        if not pairings:
            continue
        label = "".join(map(str, word))
        count = len(pairings)
        item = census[shape]
        item["crossing_words"] += 1
        item["crossing_translations"] += count
        item["one_translation_words"] += count == 1
        item["pairing_histogram"].update(pairings.values())
        candidate = (count, label)
        current = (
            item["minimum_crossings"], item["lex_first_minimum_word"]
        ) if item["minimum_crossings"] is not None else None
        if current is None or candidate < current:
            item["minimum_crossings"], item["lex_first_minimum_word"] = candidate
        if global_minimum is None or candidate < global_minimum:
            global_minimum = candidate
            killer_pairings = pairings
        total_crossing_words += 1
        total_crossing_translations += count
    assert (total_crossing_words, total_crossing_translations) == (4932, 151027)
    assert global_minimum == (1, "00202112")
    assert sum(item["one_translation_words"] for item in census.values()) == 35
    assert len(killer_pairings) == 1
    killer_translation, killer_pairing = next(iter(killer_pairings.items()))
    assert killer_pairing == 1

    shape_census = []
    for shape, item in sorted(census.items()):
        full_size = orbit_size(shape)
        shape_census.append({
            "shape": list(shape),
            "full_orbit_size": full_size,
            "currently_admitted_words": source_shape_counts[shape],
            "additional_words_to_complete": full_size - source_shape_counts[shape],
            "crossing_words": item["crossing_words"],
            "crossing_translations": item["crossing_translations"],
            "one_translation_words": item["one_translation_words"],
            "minimum_crossings": item["minimum_crossings"],
            "lex_first_minimum_word": item["lex_first_minimum_word"],
            "pairing_histogram": {
                str(key): value
                for key, value in sorted(item["pairing_histogram"].items())
            },
        })
    assert [item for item in shape_census if item["shape"] == [6, 2]][0][
        "additional_words_to_complete"
    ] == 159

    killer_shape = word_shape(tuple(map(int, global_minimum[1])))
    assert killer_shape == (3, 3, 2)
    killer_orbit_size = orbit_size(killer_shape)
    assert killer_orbit_size == 1680
    stabilizer_order = factorial(8) * factorial(3) // killer_orbit_size
    assert stabilizer_order == 144
    translation_serialized = serialize_translation(killer_translation)
    assert sum(value for _, _, value in translation_serialized["physical_edges"]) == 9
    assert sum(value for _, _, value in translation_serialized["ordered_colour_pairs"]) == 9

    result = {
        "status": "PASS full-profile71 terminal dual structural audit",
        "terminal_dual": {
            "support": len(dual),
            "coefficient_histogram": {
                str(key): value for key, value in sorted(Counter(coefficients).items())
            },
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
            "component_profile": component_profile,
            "colour_histogram_orbit_intersection_profile": dict(
                Counter(histogram_orbit_intersections)
            ),
            "first_moment_nonzero_coordinates": sum(value != 0 for value in first_moment),
            "recognition": (
                "one connected rank-7 relative edge-colour cocycle; not a "
                "marginal, toric circuit, signed cut, cycle, or single minor"
            ),
        },
        "all_mixed_word_census": {
            "crossing_words": total_crossing_words,
            "crossing_translations": total_crossing_translations,
            "one_translation_words": 35,
            "crossed_shape_orbits": len(census),
            "shape_census": shape_census,
        },
        "cheapest_crossing_word": {
            "word": global_minimum[1],
            "shape": list(killer_shape),
            "crossing_translations": global_minimum[0],
            "pairing": killer_pairing,
            "full_S8xS3_orbit_size": killer_orbit_size,
            "stabilizer_order": stabilizer_order,
            "stabilizer_shape": "((S3 x S3) semidirect C2) x S2, order 144",
            "permutation_module": "Ind_H^(S8 x S3)(1), dimension 1680",
            "S8_restriction": (
                "3*(S[8] + 2*S[7,1] + 3*S[6,2] + S[6,1,1] + "
                "3*S[5,3] + 2*S[5,2,1] + S[4,4] + "
                "2*S[4,3,1] + S[4,2,2] + S[3,3,2])"
            ),
            "S3_restriction": "280 copies of the regular S3 representation",
            "degree_nine_translation": translation_serialized,
            "literal_multiplier_cells": literal_multiplier(killer_translation),
        },
        "module_completion_verdict": {
            "general_exactness_theorem": False,
            "reason": (
                "the 37-coordinate quotient is not S8-equivariant, the "
                "dual hits all eight remaining word-shape orbits, and 35 "
                "one-row killers occur in five different orbits; the lex "
                "choice 00202112 is pivot/chart dependent"
            ),
            "cheapest_full_orbit_by_added_word_count": {
                "shape": [6, 2],
                "full_orbit_size": 168,
                "currently_admitted_words": source_shape_counts[(6, 2)],
                "additional_words_to_complete": 159,
                "minimum_crossing_translations": 2,
            },
            "actionable_prediction": (
                "Adding the (3,3,2) orbit certainly kills this dual but is "
                "likely to expose another relative class.  If orbit "
                "completion is retained as a heuristic, complete (6,2) "
                "first; it is the smallest crossed incomplete orbit and an "
                "immediate one-site refinement of (7,1)."
            ),
        },
        "source_sha256": {
            DUAL_FILE.name: sha256(DUAL_FILE.read_bytes()).hexdigest(),
            SOURCE_FILE.name: sha256(SOURCE_FILE.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    return result


def main():
    result = audit()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        RESULT_FILE.write_text(text)
    if "--check-results" in sys.argv:
        assert RESULT_FILE.read_text() == text
    print(text, end="")


if __name__ == "__main__":
    main()

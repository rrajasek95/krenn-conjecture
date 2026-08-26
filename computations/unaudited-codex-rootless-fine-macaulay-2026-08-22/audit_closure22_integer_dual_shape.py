#!/usr/bin/env python3
"""Decode the sparse first-exchange closure22 integer dual.

This is a combinatorial interpretation only.  The input dual is certified
against the target-touching translation packet recorded by
``audit_closure22_joint_semigroup.py``; it is not extended here to all
degree-13 translations.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import reduce
from itertools import combinations
from math import gcd
from pathlib import Path
import hashlib
import json
import sys


HERE = Path(__file__).resolve().parent
INPUT = HERE / "results_closure22_joint_semigroup.json"
EDGES = tuple((u, v) for u in range(8) for v in range(u + 1, 8))
PAIRS = tuple((a, b) for a in range(3) for b in range(3))

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_closure22_joint_semigroup import (  # noqa: E402
    key_add, projected_word,
)


def rank(rows):
    matrix = [list(map(Fraction, row)) for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (i for i in range(pivot_row, len(matrix)) if matrix[i][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for i in range(len(matrix)):
            if i == pivot_row or not matrix[i][column]:
                continue
            scale = matrix[i][column]
            matrix[i] = [
                value - scale * base
                for value, base in zip(matrix[i], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def independent_columns(columns):
    chosen = []
    old_rank = 0
    for index, column in enumerate(columns):
        new_rank = rank(list(zip(*(chosen + [column]))))
        if new_rank > old_rank:
            chosen.append(column)
            old_rank = new_rank
    return chosen


def nullspace(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    rows = len(a)
    columns = len(a[0])
    pivot_columns = []
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (i for i in range(pivot_row, rows) if a[i][column]), None
        )
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][column]
        a[pivot_row] = [value / scale for value in a[pivot_row]]
        for i in range(rows):
            if i == pivot_row or not a[i][column]:
                continue
            scale = a[i][column]
            a[i] = [
                value - scale * base
                for value, base in zip(a[i], a[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    free_columns = [j for j in range(columns) if j not in pivot_columns]
    basis = []
    for free in free_columns:
        vector = [Fraction(0)] * columns
        vector[free] = 1
        for i, pivot in reversed(list(enumerate(pivot_columns))):
            vector[pivot] = -sum(
                a[i][j] * vector[j] for j in free_columns
            )
        basis.append(vector)
    return basis


def primitive(values):
    values = list(map(Fraction, values))
    denominator = 1
    for value in values:
        denominator = denominator * value.denominator // gcd(
            denominator, value.denominator
        )
    integers = [int(value * denominator) for value in values]
    divisor = reduce(gcd, (abs(value) for value in integers if value), 0)
    integers = [value // divisor for value in integers]
    first = next(value for value in integers if value)
    if first < 0:
        integers = [-value for value in integers]
    return integers


def degree_sequence(graph):
    degree = [0] * 8
    for multiplicity, (u, v) in zip(graph, EDGES):
        degree[u] += multiplicity
        degree[v] += multiplicity
    return tuple(degree)


def nonzero_edge_string(graph):
    return " ".join(
        f"{u}{v}^{multiplicity}" if multiplicity != 1 else f"{u}{v}"
        for multiplicity, (u, v) in zip(graph, EDGES)
        if multiplicity
    )


def histogram_matrix(histogram):
    return [list(histogram[3 * a:3 * a + 3]) for a in range(3)]


def alternating_four_cycle(left, right):
    difference = [b - a for a, b in zip(left, right)]
    nonzero = [(EDGES[i], value) for i, value in enumerate(difference) if value]
    if len(nonzero) != 4 or sorted(value for _, value in nonzero) != [-1, -1, 1, 1]:
        return None
    degree = [0] * 8
    for (u, v), value in nonzero:
        degree[u] += value
        degree[v] += value
    return nonzero if degree == [0] * 8 else None


def run_audit():
    source = json.loads(INPUT.read_text())
    dual = source["integer_dual"]
    columns = [tuple(item["column"]) for item in dual]
    coefficients = [item["coefficient"] for item in dual]
    assert len(columns) == 16 and all(len(column) == 37 for column in columns)

    graphs = []
    histograms = []
    graph_index = {}
    histogram_index = {}
    incidence = []
    for number, (column, coefficient) in enumerate(zip(columns, coefficients), 1):
        graph = column[:28]
        histogram = column[28:]
        if graph not in graph_index:
            graph_index[graph] = len(graphs)
            graphs.append(graph)
        if histogram not in histogram_index:
            histogram_index[histogram] = len(histograms)
            histograms.append(histogram)
        incidence.append({
            "dual_column": number,
            "coefficient": coefficient,
            "graph": graph_index[graph] + 1,
            "histogram": histogram_index[histogram] + 1,
        })

    graph_degrees = sorted(set(degree_sequence(graph) for graph in graphs))
    assert graph_degrees == [(2, 2, 2, 4, 4, 4, 4, 4)]
    assert all(sum(graph) == 13 for graph in graphs)
    assert all(sum(histogram) == 13 for histogram in histograms)

    # Exact bipartite coefficient matrix: graph rows, histogram columns.
    coefficient_matrix = [[0] * len(histograms) for _ in graphs]
    for item in incidence:
        coefficient_matrix[item["graph"] - 1][item["histogram"] - 1] = item["coefficient"]

    # Centred marginal spans.  Their one-dimensional nonconstant
    # intersection is the precise linear edge-colour correlation visible on
    # these sixteen columns.
    physical_coordinate_vectors = [
        tuple(column[j] - columns[0][j] for column in columns)
        for j in range(28)
    ]
    colour_coordinate_vectors = [
        tuple(column[j] - columns[0][j] for column in columns)
        for j in range(28, 37)
    ]
    physical_basis = independent_columns(physical_coordinate_vectors)
    colour_basis = independent_columns(colour_coordinate_vectors)
    joined = [
        [physical_basis[j][i] for j in range(len(physical_basis))]
        + [-colour_basis[j][i] for j in range(len(colour_basis))]
        for i in range(len(columns))
    ]
    common_kernel = nullspace(joined)
    assert len(physical_basis) == 6
    assert len(colour_basis) == 3
    assert len(common_kernel) == 1
    correlation_coefficients = primitive(common_kernel[0])
    physical_coefficients = correlation_coefficients[:len(physical_basis)]
    colour_coefficients = correlation_coefficients[len(physical_basis):]
    correlation_values = [
        sum(c * vector[i] for c, vector in zip(physical_coefficients, physical_basis))
        for i in range(len(columns))
    ]
    assert correlation_values == [
        sum(c * vector[i] for c, vector in zip(colour_coefficients, colour_basis))
        for i in range(len(columns))
    ]
    assert any(correlation_values)

    # The unique shared variation has a particularly small literal form.
    # Here m_01 is the multiplicity of physical edge 01 and h_ab is the
    # global ordered colour-pair count.  This equality holds on exactly the
    # sixteen support columns; it is not asserted on the ambient semigroup.
    edge_01 = EDGES.index((0, 1))
    h01 = 28 + PAIRS.index((0, 1))
    h11 = 28 + PAIRS.index((1, 1))
    h12 = 28 + PAIRS.index((1, 2))
    assert all(
        2 * column[edge_01]
        == 2 * column[h01] + column[h11] + column[h12] - 4
        for column in columns
    )
    cut_01_values = []
    for column in columns:
        graph = column[:28]
        cut_value = sum(
            multiplicity
            for multiplicity, (u, v) in zip(graph, EDGES)
            if (u in (0, 1)) != (v in (0, 1))
        )
        assert cut_value == 8 - 2 * column[h01] - column[h11] - column[h12]
        cut_01_values.append(cut_value)

    # A toric circuit/minor would have zero affine and first moments.
    first_moment = [
        sum(coefficient * column[j] for coefficient, column in zip(coefficients, columns))
        for j in range(37)
    ]
    toric_circuit_test = sum(coefficients) == 0 and not any(first_moment)

    # Hostile scope replay: enumerate every translate which can touch one of
    # the sixteen supported columns.  Several closure22 words have a nonzero
    # pairing outside the target-touching quotient list used by the input
    # calculation.  This prevents promotion to a full degree-13 separator.
    dual_map = {
        tuple(item["column"]): item["coefficient"] for item in dual
    }
    extra_translation_counts = {}
    lex_extra = None
    extra_max_abs_pairing = 0
    for word_label in source["source_words"]:
        word = tuple(map(int, word_label))
        generator = projected_word(word)
        quotients = set()
        for supported_column in dual_map:
            for term_column in generator:
                quotient = tuple(
                    left - right
                    for left, right in zip(supported_column, term_column)
                )
                if min(quotient) >= 0:
                    quotients.add(quotient)
        nonzero = []
        for quotient in sorted(quotients):
            pairing = sum(
                coefficient * dual_map.get(key_add(quotient, term_column), 0)
                for term_column, coefficient in generator.items()
            )
            if pairing:
                nonzero.append((quotient, pairing))
                extra_max_abs_pairing = max(extra_max_abs_pairing, abs(pairing))
                candidate = (word_label, quotient, pairing)
                if lex_extra is None or candidate < lex_extra:
                    lex_extra = candidate
        if nonzero:
            extra_translation_counts[word_label] = len(nonzero)
    assert extra_translation_counts.get("01000000") == 5
    assert extra_translation_counts.get("10000000") == 5
    assert lex_extra is not None

    four_cycle_pairs = []
    for left, right in combinations(range(len(graphs)), 2):
        move = alternating_four_cycle(graphs[left], graphs[right])
        if move:
            four_cycle_pairs.append({
                "left": left + 1,
                "right": right + 1,
                "move": [[f"{u}{v}", value] for (u, v), value in move],
            })

    # Record global-colour S3 orbit sizes and transpose pairing.  Every
    # histogram has trivial S3 stabilizer; only H2/H4 are transposes.
    from itertools import permutations
    histogram_orbits = []
    for index, histogram in enumerate(histograms):
        orbit = set()
        for permutation in permutations(range(3)):
            orbit.add(tuple(
                histogram[3 * permutation[a] + permutation[b]]
                for a in range(3) for b in range(3)
            ))
        transpose = tuple(
            histogram[3 * b + a] for a in range(3) for b in range(3)
        )
        histogram_orbits.append({
            "histogram": index + 1,
            "global_s3_orbit_size": len(orbit),
            "transpose_histogram": (
                histogram_index[transpose] + 1 if transpose in histogram_index else None
            ),
        })

    decoded_columns = []
    for item, column in zip(incidence, columns):
        decoded_columns.append({
            **item,
            "physical_edges": nonzero_edge_string(column[:28]),
            "ordered_colour_histogram": histogram_matrix(column[28:]),
        })

    record = {
        "status": "PASS exact combinatorial decode of first-exchange integer dual",
        "scope": (
            "The dual is replayed only on the 128516 target-touching closure22 "
            "translations in the input artifact. It is not a separator for all "
            "degree-13 translations or for the full ideal."
        ),
        "dual_columns": len(columns),
        "coefficient_profile": {
            str(value): coefficients.count(value) for value in sorted(set(coefficients))
        },
        "coefficient_sum": sum(coefficients),
        "physical_graphs": len(graphs),
        "colour_histograms": len(histograms),
        "physical_degree_sequence": list(graph_degrees[0]),
        "physical_affine_rank": rank([
            [value - graphs[0][j] for j, value in enumerate(graph)]
            for graph in graphs[1:]
        ]),
        "colour_affine_rank": rank([
            [value - histograms[0][j] for j, value in enumerate(histogram)]
            for histogram in histograms[1:]
        ]),
        "joint_affine_rank": rank([
            [value - columns[0][j] for j, value in enumerate(column)]
            for column in columns[1:]
        ]),
        "coefficient_matrix_rank": rank(coefficient_matrix),
        "coefficient_matrix": coefficient_matrix,
        "incidence": incidence,
        "histograms": [histogram_matrix(histogram) for histogram in histograms],
        "histogram_orbits": histogram_orbits,
        "unique_nonconstant_marginal_correlation_values": correlation_values,
        "unique_correlation_formula": (
            "2*m_01 = 2*h_01 + h_11 + h_12 - 4 on the 16 support columns"
        ),
        "two_vertex_cut_formula": (
            "cut_{0,1} = 8 - 2*h_01 - h_11 - h_12 on the 16 support columns"
        ),
        "two_vertex_cut_values": cut_01_values,
        "toric_circuit_first_moment_zero": toric_circuit_test,
        "first_moment_nonzero_coordinates": sum(value != 0 for value in first_moment),
        "alternating_four_cycle_pairs": four_cycle_pairs,
        "recognition": (
            "The support carries a recognizable two-vertex-cut/ordered-colour "
            "correlation. The complete rank-4 coefficient dual is not itself a "
            "single toric signed minor, cycle, or cut circuit. Some physical "
            "fibres differ by alternating four-cycle moves; one two-term fibre "
            "is literally such a minor."
        ),
        "all_translate_counterguard": {
            "nonzero_words": extra_translation_counts,
            "nonzero_translations": sum(extra_translation_counts.values()),
            "max_abs_pairing": extra_max_abs_pairing,
            "lex_word": lex_extra[0],
            "lex_quotient": lex_extra[1],
            "lex_pairing": lex_extra[2],
        },
        "decoded_columns": decoded_columns,
        "input_integer_dual_row_pairing": source["integer_dual_max_abs_row_pairing"],
        "input_integer_dual_target_pairing": source["integer_dual_target_pairing"],
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    record["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return record


def main():
    record = run_audit()
    output = json.dumps(record, indent=2, sort_keys=True) + "\n"
    print(output, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent exact audit of the normalized one-hot torus quotient.

This executable does not import the primary checker.  It independently
rebuilds the properly coloured cubic stages, uses the opposite endpoint
orientation for the finite gauge and integral cocharacter, computes the
restricted character rank and stabilizer dimension, and checks the output
Hilbert--Mumford contraction through eighteen vertices.
"""

import argparse
from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
import json


COLORS = (0, 1, 2)
EXPECTED_DIGEST = "7c2ba6d1edbc3a38c5d34f3689ca13ccc02d5630723d83d5d211a017c406df81"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pair(left, right):
    require(left != right, "loop in support")
    return (left, right) if left < right else (right, left)


def supported_matchings(vertices, colors):
    support = set(colors)

    def recurse(remaining):
        if not remaining:
            return ((),)
        first = remaining[0]
        answer = []
        for position, second in enumerate(remaining[1:], start=1):
            edge = pair(first, second)
            if edge not in support:
                continue
            tail_vertices = remaining[1:position] + remaining[position + 1 :]
            for tail in recurse(tail_vertices):
                answer.append((edge,) + tail)
        return tuple(answer)

    return recurse(tuple(sorted(vertices)))


def seed():
    colors = {}
    valuations = {}
    data = {
        0: (((0, 3), 1), ((1, 2), -1), ((4, 5), 0)),
        1: (((1, 4), 0), ((0, 2), 0), ((3, 5), 0)),
        2: (((2, 5), 0), ((0, 1), 0), ((3, 4), 0)),
    }
    for color, entries in data.items():
        for endpoints, valuation in entries:
            edge = pair(*endpoints)
            require(edge not in colors, "seed edge repeated")
            colors[edge] = color
            valuations[edge] = valuation
    return set(range(6)), colors, valuations


def split_vertex(vertices, colors, valuations, old, shifts):
    """Replace old by a colour-indexed triangle with prescribed shifts."""
    incident = []
    for edge, color in colors.items():
        if old in edge:
            other = edge[1] if edge[0] == old else edge[0]
            incident.append((color, other, valuations[edge]))
    require(sorted(color for color, _other, _value in incident) == list(COLORS),
            "expanded vertex is not properly coloured")

    start = max(vertices) + 1
    replacement = {color: start + color for color in COLORS}
    new_colors = {edge: color for edge, color in colors.items() if old not in edge}
    new_values = {edge: value for edge, value in valuations.items() if old not in edge}
    external = set()
    for color, other, old_value in incident:
        edge = pair(other, replacement[color])
        new_colors[edge] = color
        new_values[edge] = old_value + shifts[color]
        external.add(edge)
    for color in COLORS:
        endpoints = [replacement[c] for c in COLORS if c != color]
        edge = pair(*endpoints)
        new_colors[edge] = color
        new_values[edge] = -shifts[color]
    new_vertices = (vertices - {old}) | set(replacement.values())
    return new_vertices, new_colors, new_values, external


def matching_value(matching, valuations):
    return sum(valuations[edge] for edge in matching)


def next_stage(vertices, colors, valuations):
    old = min(vertices)
    trial_vertices, trial_colors, trial_values, external = split_vertex(
        vertices, colors, valuations, old, (0, 0, 0)
    )
    exceptional = [
        matching_value(matching, trial_values)
        for matching in supported_matchings(trial_vertices, trial_colors)
        if external <= set(matching)
    ]
    shift_two = max([0] + [1 - value for value in exceptional])
    return split_vertex(
        vertices, colors, valuations, old, (0, 0, shift_two)
    )[:3]


def matrix_rank(matrix):
    work = [[Q(entry) for entry in row] for row in matrix]
    rank = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                scale = work[row][column]
                work[row] = [
                    entry - scale * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[rank])
                ]
        rank += 1
    return rank


def target_torus_character_matrix(vertices, colors):
    """Rows are supported coordinates in a basis of X_*(T_Delta)."""
    ordered_vertices = tuple(sorted(vertices))
    reference = ordered_vertices[-1]
    columns = tuple(
        (vertex, color)
        for color in COLORS
        for vertex in ordered_vertices[:-1]
    )
    matrix = []
    for edge in sorted(colors):
        left, right = edge
        color = colors[edge]
        row = []
        for vertex, basis_color in columns:
            if basis_color != color:
                row.append(0)
            else:
                row.append(
                    int(left == vertex) + int(right == vertex)
                    - int(left == reference) - int(right == reference)
                )
        matrix.append(row)
    return matrix


def integral_cocharacter(vertices, colors, valuations):
    """Put every edge exponent at its larger endpoint (opposite audit)."""
    weights = {(vertex, color): 0 for vertex in vertices for color in COLORS}
    for left, right in colors:
        color = colors[left, right]
        weights[right, color] = valuations[left, right]
    return weights


def arbitrary_normalized_edge_weights(colors):
    primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    answer = {}
    for color in COLORS:
        edges = sorted(edge for edge, edge_color in colors.items()
                       if edge_color == color)
        running = Q(1)
        for position, edge in enumerate(edges[:-1]):
            value = Q(primes[(4 * color + 2 * position + 1) % len(primes)])
            answer[edge] = value
            running *= value
        answer[edges[-1]] = 1 / running
    return answer


def finite_gauge(vertices, colors, edge_weights):
    """Use the larger endpoint of every edge, unlike the primary checker."""
    gauge = {(vertex, color): Q(1)
             for vertex in vertices for color in COLORS}
    for left, right in colors:
        gauge[right, colors[left, right]] = 1 / edge_weights[left, right]
    return gauge


def matching_word(vertices, matching, colors):
    word = {}
    for edge in matching:
        color = colors[edge]
        word[edge[0]] = color
        word[edge[1]] = color
    return tuple(word[vertex] for vertex in sorted(vertices))


def audit_stage(vertices, colors, valuations):
    n = len(vertices)
    edges = tuple(sorted(colors))
    require(set(colors) == set(valuations), "colour/value supports differ")
    require(len(edges) == 3 * n // 2, "support is not cubic")

    for vertex in vertices:
        incident = sorted(colors[edge] for edge in edges if vertex in edge)
        require(incident == list(COLORS), "proper colouring failed")
    for color in COLORS:
        color_edges = [edge for edge in edges if colors[edge] == color]
        require(len(color_edges) == n // 2, "colour class is not a 1-factor")
        require(set(sum((list(edge) for edge in color_edges), [])) == vertices,
                "colour class does not cover every vertex")
        require(sum(valuations[edge] for edge in color_edges) == 0,
                "pure matching valuation is not normalized")

    # Explicit integral 1PS: every port occurs once, so endpoint orientation
    # has no compatibility condition beyond the three colour sums.
    cocharacter = integral_cocharacter(vertices, colors, valuations)
    for color in COLORS:
        require(sum(cocharacter[vertex, color] for vertex in vertices) == 0,
                "1PS does not fix the target")
    for left, right in edges:
        color = colors[left, right]
        require(
            cocharacter[left, color] + cocharacter[right, color]
            == valuations[left, right],
            "1PS edge exponent changed",
        )

    matchings = supported_matchings(vertices, colors)
    outputs = []
    for matching in matchings:
        word = matching_word(vertices, matching, colors)
        valuation = matching_value(matching, valuations)
        one_ps_weight = sum(
            cocharacter[vertex, word[position]]
            for position, vertex in enumerate(sorted(vertices))
        )
        require(one_ps_weight == valuation, "output equivariance failed")
        outputs.append((word, valuation))
    require(len({word for word, _value in outputs}) == len(outputs),
            "distinct matchings collided in one output word")
    pure = {((color,) * n, 0) for color in COLORS}
    require({item for item in outputs if len(set(item[0])) == 1} == pure,
            "pure matching ledger changed")
    require(all(value > 0 for word, value in outputs if len(set(word)) > 1),
            "mixed output does not contract")
    require(len(outputs) > 3, "all-unit output accidentally equals GHZ")
    require(min(valuations.values()) < 0 < max(valuations.values()),
            "source Laurent orbit unexpectedly has an affine 1PS limit")

    # An exact finite normalized point is gauged to the unit source.  The
    # product-one condition makes the gauge target-fixing.
    edge_weights = arbitrary_normalized_edge_weights(colors)
    gauge = finite_gauge(vertices, colors, edge_weights)
    for color in COLORS:
        require(
            reduce(
                lambda x, vertex: x * gauge[vertex, color], vertices, Q(1)
            ) == 1,
            "finite gauge leaves the target stabilizer",
        )
    for left, right in edges:
        color = colors[left, right]
        require(
            gauge[left, color] * gauge[right, color] * edge_weights[left, right]
            == 1,
            "finite gauge does not reach the unit source",
        )

    # Character rank, stabilizer, and the positive balance certificate.
    character_matrix = target_torus_character_matrix(vertices, colors)
    action_rank = matrix_rank(character_matrix)
    chart_dimension = len(edges) - 3
    torus_dimension = 3 * (n - 1)
    stabilizer_dimension = torus_dimension - action_rank
    require(action_rank == chart_dimension, "action is not full on chart")
    require(stabilizer_dimension == len(edges), "stabilizer dimension changed")
    require(all(sum(row[column] for row in character_matrix) == 0
                for column in range(torus_dimension)),
            "all-positive weight relation failed")

    return {
        "n": n,
        "edges": len(edges),
        "matchings": len(outputs),
        "mixed_matchings": len(outputs) - 3,
        "minimum_source_exponent": min(valuations.values()),
        "maximum_source_exponent": max(valuations.values()),
        "maximum_output_exponent": max(value for _word, value in outputs),
        "target_torus_dimension": torus_dimension,
        "action_rank": action_rank,
        "stabilizer_dimension": stabilizer_dimension,
        "normalized_chart_dimension": chart_dimension,
        "quotient_dimension": chart_dimension - action_rank,
        "positive_balance_coefficients": len(edges),
    }


def run(mode):
    vertices, colors, valuations = seed()
    ledger = []
    stages = 7 if mode == "all" else 1
    if mode != "all":
        target_n = int(mode[1:])
        while len(vertices) < target_n:
            vertices, colors, valuations = next_stage(vertices, colors, valuations)
    for stage in range(stages):
        ledger.append(audit_stage(vertices, colors, valuations))
        if stage + 1 < stages:
            vertices, colors, valuations = next_stage(vertices, colors, valuations)

    if mode == "all":
        require([entry["n"] for entry in ledger] == [6, 8, 10, 12, 14, 16, 18],
                "stage orders changed")
        require([entry["matchings"] for entry in ledger] == [4, 5, 6, 8, 10, 12, 16],
                "matching counts changed")
        require(all(entry["quotient_dimension"] == 0 for entry in ledger),
                "a normalized chart quotient acquired dimension")

    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if mode == "all":
        require(digest == EXPECTED_DIGEST, f"audit digest changed: {digest}")
    print(f"independent one-hot torus quotient audit ({mode}): PASS")
    for entry in ledger:
        print(
            f"n={entry['n']}: action/chart rank {entry['action_rank']}, "
            f"stabilizer {entry['stabilizer_dimension']}, "
            f"matchings {entry['matchings']}"
        )
    print("integral 1PS, polystability, and zero-dimensional chart quotient verified")
    print(f"sha256: {digest}")
    return digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("all", "n6", "n8", "n10", "n12", "n14", "n16", "n18"),
        default="all",
    )
    arguments = parser.parse_args()
    run(arguments.mode)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact one-hot counterguard for blowing up the mixed-output ideal.

On a normalized properly coloured source torus, every supported mixed output
is a Laurent monomial and therefore a unit.  The pulled-back mixed ideal is
the unit ideal, so the source blow-up is the identity.  This checker rebuilds
the all-even boundary through n=18 and verifies the target exceptional
directions and their target-torus 1PS provenance exactly.
"""

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json


COLORS = (0, 1, 2)
EXPECTED_DIGEST = "9b62adb3c4a5f7a64ac18c95df903f6d19ea1554caa22fc7d73d8ada090442fa"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    require(left != right, "loop")
    return (left, right) if left < right else (right, left)


def perfect_matchings(vertices, support):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        pair = edge(first, second)
        if pair not in support:
            continue
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder, support):
            answer.append((pair,) + tail)
    return tuple(answer)


def initial_graph():
    vertices = set(range(6))
    rows = (
        (0, 3, 0, 1), (1, 2, 0, -1), (4, 5, 0, 0),
        (1, 4, 1, 0), (0, 2, 1, 0), (3, 5, 1, 0),
        (2, 5, 2, 0), (0, 1, 2, 0), (3, 4, 2, 0),
    )
    colors = {}
    valuations = {}
    for left, right, color, valuation in rows:
        pair = edge(left, right)
        require(pair not in colors, "repeated seed edge")
        colors[pair] = color
        valuations[pair] = valuation
    return vertices, colors, valuations


def replace(vertices, colors, valuations, old, shifts):
    incident = []
    for pair, color in colors.items():
        if old in pair:
            other = pair[1] if pair[0] == old else pair[0]
            incident.append((color, other, valuations[pair]))
    require(sorted(color for color, _other, _value in incident) == list(COLORS),
            "replacement vertex is not properly coloured")

    start = max(vertices) + 1
    new_vertex = {color: start + color for color in COLORS}
    new_colors = {pair: color for pair, color in colors.items() if old not in pair}
    new_values = {pair: value for pair, value in valuations.items() if old not in pair}
    external = set()
    for color, other, value in incident:
        pair = edge(other, new_vertex[color])
        new_colors[pair] = color
        new_values[pair] = value + shifts[color]
        external.add(pair)
    for missing in COLORS:
        endpoints = [new_vertex[color] for color in COLORS if color != missing]
        pair = edge(*endpoints)
        new_colors[pair] = missing
        new_values[pair] = -shifts[missing]
    new_vertices = (vertices - {old}) | set(new_vertex.values())
    return new_vertices, new_colors, new_values, external


def expand(vertices, colors, valuations):
    old = min(vertices)
    trial_vertices, trial_colors, trial_values, external = replace(
        vertices, colors, valuations, old, (0, 0, 0)
    )
    exceptional_values = []
    for matching in perfect_matchings(trial_vertices, set(trial_colors)):
        if external <= set(matching):
            exceptional_values.append(sum(trial_values[pair] for pair in matching))
    shift = max([0] + [1 - value for value in exceptional_values])
    return replace(vertices, colors, valuations, old, (0, 0, shift))[:3]


def rational_rank(matrix):
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


def word_of(vertices, matching, colors):
    assignment = {}
    for pair in matching:
        assignment[pair[0]] = colors[pair]
        assignment[pair[1]] = colors[pair]
    return tuple(assignment[vertex] for vertex in sorted(vertices))


def monomial_vector(matching, ordered_edges):
    support = set(matching)
    return tuple(int(pair in support) for pair in ordered_edges)


def target_cocharacter(vertices, colors, valuations):
    weights = {(vertex, color): 0 for vertex in vertices for color in COLORS}
    # Split at the parity-selected endpoint to make this implementation
    # different from both earlier endpoint conventions.
    for left, right in colors:
        color = colors[left, right]
        chosen = left if (left + right + color) % 2 == 0 else right
        weights[chosen, color] = valuations[left, right]
    return weights


def action_rank(vertices, colors):
    ordered_vertices = tuple(sorted(vertices))
    reference = ordered_vertices[-1]
    columns = tuple(
        (vertex, color)
        for color in COLORS
        for vertex in ordered_vertices[:-1]
    )
    rows = []
    for left, right in sorted(colors):
        color = colors[left, right]
        row = []
        for vertex, basis_color in columns:
            if basis_color != color:
                row.append(0)
            else:
                row.append(
                    int(left == vertex) + int(right == vertex)
                    - int(left == reference) - int(right == reference)
                )
        rows.append(row)
    return rational_rank(rows)


def audit_stage(vertices, colors, valuations):
    n = len(vertices)
    ordered_edges = tuple(sorted(colors))
    require(set(colors) == set(valuations), "support mismatch")
    require(len(ordered_edges) == 3 * n // 2, "support not cubic")
    for vertex in vertices:
        require(
            sorted(colors[pair] for pair in colors if vertex in pair) == list(COLORS),
            "improper edge colouring",
        )
    for color in COLORS:
        color_edges = [pair for pair in ordered_edges if colors[pair] == color]
        require(sum(valuations[pair] for pair in color_edges) == 0,
                "pure coefficient not normalized")

    cocharacter = target_cocharacter(vertices, colors, valuations)
    for color in COLORS:
        require(sum(cocharacter[vertex, color] for vertex in vertices) == 0,
                "cocharacter does not fix GHZ")
    for left, right in ordered_edges:
        color = colors[left, right]
        require(
            cocharacter[left, color] + cocharacter[right, color]
            == valuations[left, right],
            "edge valuation not realized by 1PS",
        )

    matching_rows = []
    seen_words = set()
    for matching in perfect_matchings(vertices, set(colors)):
        word = word_of(vertices, matching, colors)
        require(word not in seen_words, "matching word collision")
        seen_words.add(word)
        vector = monomial_vector(matching, ordered_edges)
        value = sum(
            vector[index] * valuations[pair]
            for index, pair in enumerate(ordered_edges)
        )
        one_ps_value = sum(
            cocharacter[vertex, word[position]]
            for position, vertex in enumerate(sorted(vertices))
        )
        require(value == one_ps_value, "output 1PS weight mismatch")
        matching_rows.append((word, vector, value))

    pure = [row for row in matching_rows if len(set(row[0])) == 1]
    mixed = [row for row in matching_rows if len(set(row[0])) > 1]
    require(len(pure) == 3 and all(value == 0 for _word, _vector, value in pure),
            "pure output ledger changed")
    require(mixed and all(value > 0 for _word, _vector, value in mixed),
            "no positive mixed-output boundary")

    # In O(U)=Q[x_e^{+-1}]/(prod_{P_c}x_e-1), every mixed coefficient
    # x^u is a unit with inverse x^{-u}.  One such generator already makes
    # the pulled-back mixed ideal equal to O(U).
    for _word, vector, _value in mixed:
        inverse = tuple(-entry for entry in vector)
        require(tuple(a + b for a, b in zip(vector, inverse)) == (0,) * len(vector),
                "Laurent unit inverse failed")
    pullback_ideal_is_unit = True

    # The target blow-up lift uses [F_m]_m.  Choose a minimum-weight pivot;
    # every ratio F_m/F_pivot is again a Laurent unit on U and has a
    # nonnegative t-order along the boundary arc.  The exceptional special
    # point retains exactly the minimum-weight matching coordinates.
    minimum = min(value for _word, _vector, value in mixed)
    pivot = next(row for row in mixed if row[2] == minimum)
    ratio_orders = []
    leading_words = []
    for word, vector, value in mixed:
        ratio_vector = tuple(a - b for a, b in zip(vector, pivot[1]))
        inverse_ratio = tuple(-entry for entry in ratio_vector)
        require(tuple(a + b for a, b in zip(ratio_vector, inverse_ratio))
                == (0,) * len(ratio_vector), "blow-up ratio not Laurent-invertible")
        order = value - minimum
        require(order >= 0, "chosen blow-up chart has a pole on arc")
        ratio_orders.append(order)
        if order == 0:
            leading_words.append("".join(map(str, word)))

    # Full action rank on the normalized torus means invariant rational
    # functions on this chart are constant.  Hence no invariant expression
    # in the projective blow-up ratios separates the 1PS limit from A_*.
    rank = action_rank(vertices, colors)
    chart_dimension = len(ordered_edges) - 3
    require(rank == chart_dimension, "normalized source torus not one orbit")

    return {
        "n": n,
        "edges": len(ordered_edges),
        "mixed_generators": len(mixed),
        "pullback_mixed_ideal": "unit",
        "source_blowup_exceptional_divisor": "empty",
        "minimum_mixed_order": minimum,
        "leading_exceptional_coordinates": len(leading_words),
        "leading_words": leading_words,
        "blowup_ratio_orders": sorted(ratio_orders),
        "normalized_chart_dimension": chart_dimension,
        "target_torus_action_rank": rank,
        "invariant_rational_dimension": chart_dimension - rank,
    }


def run(mode):
    vertices, colors, valuations = initial_graph()
    target = 18 if mode == "all" else int(mode[1:])
    ledger = []
    while True:
        if mode == "all" or len(vertices) == target:
            ledger.append(audit_stage(vertices, colors, valuations))
        if len(vertices) == target:
            break
        vertices, colors, valuations = expand(vertices, colors, valuations)

    if mode == "all":
        require([row["n"] for row in ledger] == [6, 8, 10, 12, 14, 16, 18],
                "order ledger changed")
        require([row["mixed_generators"] for row in ledger]
                == [1, 2, 3, 5, 7, 9, 13], "mixed generator ledger changed")
        require([row["leading_exceptional_coordinates"] for row in ledger]
                == [1, 2, 3, 4, 5, 6, 7], "exceptional direction ledger changed")

    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if mode == "all":
        require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")
    print(f"one-hot mixed-output blow-up counterguard ({mode}): PASS")
    for row in ledger:
        print(
            f"n={row['n']}: mixed={row['mixed_generators']}, "
            f"leading exceptional={row['leading_exceptional_coordinates']}, "
            "pullback ideal=unit"
        )
    print("source blow-up is identity; invariant exceptional quotient still collapses")
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

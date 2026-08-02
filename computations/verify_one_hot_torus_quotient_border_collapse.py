#!/usr/bin/env python3
"""Exact audit of the proper-colour one-hot torus-quotient counterguard.

The checker builds the all-even Laurent boundary through n=18.  At every
stage it constructs the target-fixing port-torus cocharacter whose orbit of
the all-unit source is the Laurent family, checks all matching/output
weights, and computes the rank of the port-torus action on the normalized
sparse chart.  A separate rational-weight test audits transitivity away from
the particular Laurent one-parameter subgroup.
"""

from fractions import Fraction
from hashlib import sha256
import json


COLORS = (0, 1, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(u, v):
    require(u != v, "loop")
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices, support):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        pair = edge(first, second)
        if pair not in support:
            continue
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest, support):
            yield (pair,) + tail


def seed():
    vertices = set(range(6))
    edges = {
        (0, 3): (0, 1),
        (1, 2): (0, -1),
        (4, 5): (0, 0),
        (1, 4): (1, 0),
        (0, 2): (1, 0),
        (3, 5): (1, 0),
        (2, 5): (2, 0),
        (0, 1): (2, 0),
        (3, 4): (2, 0),
    }
    return vertices, edges


def replace_vertex(vertices, edges, old, shifts):
    incident = []
    for pair, (color, valuation) in edges.items():
        if old in pair:
            other = pair[1] if pair[0] == old else pair[0]
            incident.append((color, other, valuation))
    require(sorted(x[0] for x in incident) == list(COLORS), "bad expansion")

    first = max(vertices) + 1
    new_vertex = {color: first + color for color in COLORS}
    result = {pair: data for pair, data in edges.items() if old not in pair}
    external = set()
    for color, other, valuation in incident:
        pair = edge(other, new_vertex[color])
        result[pair] = (color, valuation + shifts[color])
        external.add(pair)
    for missing in COLORS:
        remaining = [color for color in COLORS if color != missing]
        pair = edge(new_vertex[remaining[0]], new_vertex[remaining[1]])
        result[pair] = (missing, -shifts[missing])
    new_vertices = (vertices - {old}) | set(new_vertex.values())
    return new_vertices, result, external


def matching_data(matching, edges, vertices):
    word = {}
    valuation = 0
    for pair in matching:
        color, amount = edges[pair]
        valuation += amount
        word[pair[0]] = color
        word[pair[1]] = color
    return tuple(word[v] for v in sorted(vertices)), valuation


def expand(vertices, edges):
    trial_vertices, trial_edges, external = replace_vertex(
        vertices, edges, min(vertices), (0, 0, 0)
    )
    three_external = []
    for matching in perfect_matchings(trial_vertices, trial_edges):
        if external <= set(matching):
            three_external.append(
                matching_data(matching, trial_edges, trial_vertices)[1]
            )
    last_shift = max([0] + [1 - value for value in three_external])
    new_vertices, new_edges, _ = replace_vertex(
        vertices, edges, min(vertices), (0, 0, last_shift)
    )
    return new_vertices, new_edges


def rational_rank(matrix):
    work = [[Fraction(entry) for entry in row] for row in matrix]
    if not work:
        return 0
    row = 0
    for column in range(len(work[0])):
        pivot = next((r for r in range(row, len(work)) if work[r][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for other in range(len(work)):
            if other == row or not work[other][column]:
                continue
            value = work[other][column]
            work[other] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(work[other], work[row])
            ]
        row += 1
        if row == len(work):
            break
    return row


def restricted_action_rank(vertices, edges):
    ordered_vertices = sorted(vertices)
    ordered_edges = sorted(edges)
    columns = []
    reference = ordered_vertices[-1]
    for color in COLORS:
        for vertex in ordered_vertices[:-1]:
            column = []
            for u, v in ordered_edges:
                edge_color, _ = edges[u, v]
                value = 0
                if edge_color == color:
                    value += int(u == vertex) + int(v == vertex)
                    value -= int(u == reference) + int(v == reference)
                column.append(value)
            columns.append(column)
    # Equal positive coefficients on all supported source weights give the
    # zero character of the target-fixing torus.  This is the exact toric
    # polystability certificate for the all-unit point.
    require(all(sum(column) == 0 for column in columns),
            "equal support weights are not target-torus balanced")
    matrix = [list(row) for row in zip(*columns)]
    return rational_rank(matrix)


def border_cocharacter(vertices, edges):
    """Split each edge valuation onto its lower endpoint."""
    weights = {(v, color): 0 for v in vertices for color in COLORS}
    for (u, _v), (color, valuation) in edges.items():
        weights[u, color] = valuation
    return weights


def arbitrary_normalized_weights(vertices, edges):
    """An unrelated rational point of the normalized sparse source torus."""
    primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)
    result = {}
    for color in COLORS:
        color_edges = sorted(pair for pair, data in edges.items() if data[0] == color)
        product = Fraction(1)
        for position, pair in enumerate(color_edges[:-1]):
            value = Fraction(primes[(color * 5 + position) % len(primes)])
            result[pair] = value
            product *= value
        result[color_edges[-1]] = 1 / product
    return result


def transitivity_gauge(vertices, edges, source_weights):
    gauge = {(v, color): Fraction(1) for v in vertices for color in COLORS}
    for (u, _v), (color, _valuation) in edges.items():
        gauge[u, color] = 1 / source_weights[u, _v]
    return gauge


def audit_stage(vertices, edges):
    n = len(vertices)
    require(len(edges) == 3 * n // 2, "support is not cubic")
    for vertex in vertices:
        incident_colors = sorted(
            color for pair, (color, _valuation) in edges.items() if vertex in pair
        )
        require(incident_colors == list(COLORS), "support is not properly colored")

    color_sums = {
        color: sum(value for edge_color, value in edges.values()
                   if edge_color == color)
        for color in COLORS
    }
    require(color_sums == {color: 0 for color in COLORS}, "unnormalized colors")

    cocharacter = border_cocharacter(vertices, edges)
    require(
        {color: sum(cocharacter[v, color] for v in vertices) for color in COLORS}
        == {color: 0 for color in COLORS},
        "cocharacter does not fix GHZ",
    )
    for (u, v), (color, valuation) in edges.items():
        require(cocharacter[u, color] + cocharacter[v, color] == valuation,
                "cocharacter does not recover edge valuation")

    terms = []
    for matching in perfect_matchings(vertices, edges):
        word, valuation = matching_data(matching, edges, vertices)
        output_weight = sum(
            cocharacter[v, word[position]]
            for position, v in enumerate(sorted(vertices))
        )
        require(output_weight == valuation, "equivariance weight failed")
        terms.append((word, valuation))
    require(len({word for word, _ in terms}) == len(terms), "word collision")
    pure = {((color,) * n, 0) for color in COLORS}
    require(set(term for term in terms if term[1] == 0) == pure, "wrong limit")
    require(all(value > 0 for word, value in terms if len(set(word)) > 1),
            "mixed term is not contracted")

    # Audit transitivity on a rational normalized point unrelated to the
    # border exponents.  The constructed target-fixing gauge sends every
    # supported edge weight to one.
    source_weights = arbitrary_normalized_weights(vertices, edges)
    gauge = transitivity_gauge(vertices, edges, source_weights)
    for color in COLORS:
        product = Fraction(1)
        for vertex in vertices:
            product *= gauge[vertex, color]
        require(product == 1, "finite gauge does not fix GHZ")
    for (u, v), (color, _valuation) in edges.items():
        require(gauge[u, color] * gauge[v, color] * source_weights[u, v] == 1,
                "finite normalized source did not gauge to the unit source")

    action_rank = restricted_action_rank(vertices, edges)
    expected_rank = len(edges) - len(COLORS)
    require(action_rank == expected_rank, "normalized-chart action rank")

    return {
        "n": n,
        "edges": len(edges),
        "matchings": len(terms),
        "mixed": len(terms) - 3,
        "maximum_border_weight": max(value for _word, value in terms),
        "target_torus_dimension": 3 * (n - 1),
        "normalized_chart_dimension": expected_rank,
        "action_rank": action_rank,
        "quotient_dimension": expected_rank - action_rank,
    }


def main():
    vertices, edges = seed()
    ledger = []
    for stage in range(7):
        ledger.append(audit_stage(vertices, edges))
        if stage < 6:
            vertices, edges = expand(vertices, edges)

    require([entry["n"] for entry in ledger] == [6, 8, 10, 12, 14, 16, 18],
            "order ledger")
    require([entry["matchings"] for entry in ledger] == [4, 5, 6, 8, 10, 12, 16],
            "matching ledger")
    require(all(entry["quotient_dimension"] == 0 for entry in ledger),
            "normalized chart did not collapse")

    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == "ceeab3be40bba8ce8456c3feb5ab59176d762ab55a160709d85b191aa15ed632",
            f"ledger digest changed: {digest}")

    print("one-hot target-torus quotient border collapse: PASS")
    for entry in ledger:
        print(
            f"n={entry['n']}: matchings={entry['matchings']}, "
            f"chart/action rank={entry['action_rank']}, quotient dimension=0"
        )
    print("every Laurent family is one target-fixing torus orbit of its unit source")
    print("its finite output and GHZ have the same affine target quotient point")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

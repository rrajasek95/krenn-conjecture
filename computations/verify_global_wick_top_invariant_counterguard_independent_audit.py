#!/usr/bin/env python3
"""Independent audit of the global-Wick Laurent counterguard.

This file deliberately does not import the primary checker.  It uses a
bit-mask perfect-matching enumerator, reconstructs every local triangle split
and contraction, and computes the full covariance determinant by independent
exact elimination.  It also enumerates the Bell-chain projection and its
accepted internal occupation patterns.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product


COLOURS = (0, 1, 2)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pair(u, v):
    require(u != v, ("loop", u, v))
    return (u, v) if u < v else (v, u)


def seed_graph():
    rows = {
        0: ((0, 3, 1), (1, 2, -1), (4, 5, 0)),
        1: ((1, 4, 0), (0, 2, 0), (3, 5, 0)),
        2: ((2, 5, 0), (0, 1, 0), (3, 4, 0)),
    }
    graph = {}
    for colour, entries in rows.items():
        for u, v, valuation in entries:
            edge = pair(u, v)
            require(edge not in graph, ("repeated seed edge", edge))
            graph[edge] = (colour, valuation)
    return tuple(range(6)), graph


def perfect_matchings(vertices, graph):
    """Enumerate via a vertex bit mask, independently of the primary DFS."""
    ordered = tuple(sorted(vertices))
    index = {vertex: position for position, vertex in enumerate(ordered)}
    incident = {vertex: [] for vertex in ordered}
    for edge in graph:
        u, v = edge
        incident[u].append((v, edge))
        incident[v].append((u, edge))

    full = (1 << len(ordered)) - 1
    memo = {}

    def visit(mask):
        if mask == full:
            return ((),)
        if mask in memo:
            return memo[mask]
        position = next(i for i in range(len(ordered)) if not mask & (1 << i))
        vertex = ordered[position]
        answer = []
        for neighbour, edge in sorted(incident[vertex]):
            other = index[neighbour]
            if mask & (1 << other):
                continue
            new_mask = mask | (1 << position) | (1 << other)
            for tail in visit(new_mask):
                answer.append(tuple(sorted((edge,) + tail)))
        memo[mask] = tuple(answer)
        return memo[mask]

    return visit(0)


def matching_data(matching, vertices, graph):
    local_colours = {}
    valuation = 0
    for edge in matching:
        colour, exponent = graph[edge]
        valuation += exponent
        for vertex in edge:
            require(vertex not in local_colours, ("not a matching", matching))
            local_colours[vertex] = colour
    require(set(local_colours) == set(vertices), ("not perfect", matching))
    word = tuple(local_colours[vertex] for vertex in sorted(vertices))
    return word, valuation


def verify_three_factorisation(vertices, graph):
    by_colour = {colour: set() for colour in COLOURS}
    at_port = {(vertex, colour): 0 for vertex in vertices for colour in COLOURS}
    for edge, (colour, _) in graph.items():
        by_colour[colour].add(edge)
        for vertex in edge:
            at_port[vertex, colour] += 1
    require(all(count == 1 for count in at_port.values()),
            ("not properly cubic and edge-coloured", at_port))
    for colour in COLOURS:
        require(len(by_colour[colour]) == len(vertices) // 2,
                ("colour class is not perfect", colour, by_colour[colour]))
        require(sum(graph[edge][1] for edge in by_colour[colour]) == 0,
                ("colour product not normalized", colour))
    return by_colour


def determinant(matrix):
    work = [[Fraction(entry) for entry in row] for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        require(pivot is not None, ("singular covariance", column))
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column]
        result *= pivot_value
        for j in range(column, len(work)):
            work[column][j] /= pivot_value
        for row in range(column + 1, len(work)):
            multiple = work[row][column]
            if multiple:
                for j in range(column, len(work)):
                    work[row][j] -= multiple * work[column][j]
    return result


def covariance_determinant(vertices, graph, t=Fraction(3, 2)):
    """Build all 3n ports, using colour-major order to expose no shortcut."""
    ports = tuple((vertex, colour)
                  for colour in COLOURS for vertex in sorted(vertices))
    location = {port: i for i, port in enumerate(ports)}
    matrix = [[Fraction(0) for _ in ports] for _ in ports]
    for (u, v), (colour, exponent) in graph.items():
        weight = t ** exponent
        i, j = location[u, colour], location[v, colour]
        matrix[i][j] = weight
        matrix[j][i] = weight
    return determinant(matrix)


def split_vertex(vertices, graph, chosen, shifts):
    require(len(shifts) == 3, ("shift arity", shifts))
    incident = {}
    retained = {}
    for edge, data in graph.items():
        if chosen not in edge:
            retained[edge] = data
            continue
        colour, valuation = data
        neighbour = edge[0] if edge[1] == chosen else edge[1]
        require(colour not in incident, ("duplicate incident colour", chosen))
        incident[colour] = (neighbour, valuation)
    require(set(incident) == set(COLOURS), ("missing incident colour", chosen))

    first = max(vertices) + 1
    triangle = tuple(first + colour for colour in COLOURS)
    external = {}
    internal = {}
    for colour in COLOURS:
        neighbour, valuation = incident[colour]
        edge = pair(neighbour, triangle[colour])
        retained[edge] = (colour, valuation + shifts[colour])
        external[colour] = edge
        other = tuple(c for c in COLOURS if c != colour)
        edge = pair(triangle[other[0]], triangle[other[1]])
        retained[edge] = (colour, -shifts[colour])
        internal[colour] = edge
    new_vertices = tuple(sorted((set(vertices) - {chosen}) | set(triangle)))
    metadata = (triangle, external, internal, incident)
    return new_vertices, retained, metadata


def choose_and_audit_split(vertices, graph, chosen):
    old_matchings = set(perfect_matchings(vertices, graph))
    trial_vertices, trial_graph, trial_meta = split_vertex(
        vertices, graph, chosen, (0, 0, 0)
    )
    _, trial_external, _, _ = trial_meta
    trial_external_set = set(trial_external.values())
    triple_base = []
    for matching in perfect_matchings(trial_vertices, trial_graph):
        if trial_external_set <= set(matching):
            triple_base.append(matching_data(matching, trial_vertices,
                                              trial_graph)[1])
    lift = max(0, 1 - min(triple_base)) if triple_base else 0
    new_vertices, new_graph, metadata = split_vertex(
        vertices, graph, chosen, (0, 0, lift)
    )
    triangle, external, internal, incident = metadata
    external_set = set(external.values())
    contracted = set()
    triple_count = 0

    for matching in perfect_matchings(new_vertices, new_graph):
        selected_external = external_set & set(matching)
        require(len(selected_external) in (1, 3),
                ("triangle parity classification", matching))
        if len(selected_external) == 3:
            triple_count += 1
            require(matching_data(matching, new_vertices, new_graph)[1] >= 1,
                    ("unraised three-external matching", matching, lift))
            continue

        colour = next(c for c in COLOURS if external[c] in matching)
        require(internal[colour] in matching,
                ("opposite internal edge missing", colour, matching))
        neighbour, _ = incident[colour]
        old_edge = pair(chosen, neighbour)
        collapsed = tuple(sorted(
            (set(matching) - {external[colour], internal[colour]}) | {old_edge}
        ))
        require(collapsed in old_matchings,
                ("local contraction is not an old matching", collapsed))
        old_word, old_value = matching_data(collapsed, vertices, graph)
        new_word, new_value = matching_data(matching, new_vertices, new_graph)
        require(new_value == old_value,
                ("one-external valuation changed", old_value, new_value))
        old_at = dict(zip(sorted(vertices), old_word))
        new_at = dict(zip(sorted(new_vertices), new_word))
        require(all(new_at[s] == old_at[chosen] for s in triangle),
                ("triangle is not diagonal", chosen, old_at, new_at))
        require(all(new_at[v] == old_at[v]
                    for v in vertices if v != chosen),
                ("unchanged output colour moved", chosen, old_at, new_at))
        require(collapsed not in contracted,
                ("two lifts of one old matching", collapsed))
        contracted.add(collapsed)

    require(contracted == old_matchings,
            ("one-external lift is not bijective", chosen,
             len(contracted), len(old_matchings)))
    return new_vertices, new_graph, lift, triple_count


def audit_graph(vertices, graph):
    colour_classes = verify_three_factorisation(vertices, graph)
    matchings = perfect_matchings(vertices, graph)
    data = tuple(sorted(matching_data(m, vertices, graph) for m in matchings))
    require(len({word for word, _ in data}) == len(data),
            ("colour word does not determine matching", len(vertices)))
    expected_zero = tuple(((colour,) * len(vertices), 0)
                          for colour in COLOURS)
    require(tuple(item for item in data if item[1] == 0) == expected_zero,
            ("wrong valuation-zero output", len(vertices), data))
    require(all(value >= 0 for _, value in data),
            ("Laurent pole survived in top tensor", len(vertices), data))
    require(all(value > 0 for word, value in data
                if len(set(word)) != 1),
            ("mixed word has nonpositive valuation", len(vertices), data))

    predicted = Fraction((-1) ** (3 * len(vertices) // 2))
    direct = covariance_determinant(vertices, graph)
    require(direct == predicted,
            ("full exact determinant disagrees", len(vertices), direct, predicted))
    # This is the closed-form calculation used for all n: each colour block
    # is a weighted perfect matching with normalized total exponent.
    formula = Fraction(1)
    for colour in COLOURS:
        exponent_sum = sum(graph[e][1] for e in colour_classes[colour])
        formula *= (-1) ** (len(vertices) // 2) * Fraction(3, 2) ** (2 * exponent_sum)
    require(formula == predicted == direct,
            ("matching-block determinant formula", len(vertices), formula))
    return data, direct


def multiply_series(left, right):
    answer = {}
    for i, a in left.items():
        for j, b in right.items():
            answer[i + j] = answer.get(i + j, 0) + a * b
    return {degree: coefficient for degree, coefficient in answer.items()
            if coefficient}


def audit_closure_substitution(data):
    """Audit the universal constant-term step for coordinate monomials."""
    coordinate_series = {}
    for word, valuation in data:
        series = coordinate_series.setdefault(word, {})
        series[valuation] = series.get(valuation, 0) + 1
    # Add a coordinate absent from the family, so zero target coordinates are
    # represented as well as the three pure coordinates.
    arity = len(data[0][0])
    absent = next(word for word in product(COLOURS, repeat=arity)
                  if word not in coordinate_series)
    coordinate_series[absent] = {}
    series_list = list(coordinate_series.values())
    for degree in range(5):
        for factors in product(range(len(series_list)), repeat=degree):
            composed = {0: 1}
            target_value = 1
            for position in factors:
                factor = series_list[position]
                composed = multiply_series(composed, factor)
                target_value *= factor.get(0, 0)
            require(composed.get(0, 0) == target_value,
                    ("polynomial substitution constant term", degree, factors))
    require(all(min(series, default=0) >= 0 for series in series_list),
            "output coordinate has a negative Laurent exponent")
    return tuple(sorted((word, tuple(sorted(series.items())))
                        for word, series in coordinate_series.items()))


def bits(label):
    return (label // 2, label % 2)


def project_two_bells_per_link(arity):
    amplitudes = {}
    for links in product(range(4), repeat=arity - 1):
        # Endpoint maps kill 11 and retain the three codewords.
        if links[0] not in COLOURS or links[-1] not in COLOURS:
            continue
        internal_output = []
        accepted = True
        for site in range(1, arity - 1):
            incoming, outgoing = links[site - 1], links[site]
            if incoming != outgoing or incoming not in COLOURS:
                accepted = False
                break
            internal_output.append(incoming)
        if not accepted:
            continue
        word = (links[0],) + tuple(internal_output) + (links[-1],)
        amplitudes[word] = amplitudes.get(word, 0) + 1
    return amplitudes


def audit_bell_projection():
    accepted_internal = tuple(bits(c) + bits(c) for c in COLOURS)
    require(accepted_internal == ((0, 0, 0, 0),
                                  (0, 1, 0, 1),
                                  (1, 0, 1, 0)),
            ("wrong internal projection support", accepted_internal))
    require(all(sum(pattern) != 1 for pattern in accepted_internal),
            ("Bell internal map accidentally is one-hot", accepted_internal))
    counts = []
    for arity in range(3, 10):
        output = project_two_bells_per_link(arity)
        expected = {(colour,) * arity: 1 for colour in COLOURS}
        require(output == expected, ("projected Bell chain", arity, output))
        counts.append((arity, 4 ** (arity - 1), len(output)))
    return accepted_internal, tuple(counts)


def main():
    digest = sha256()
    vertices, graph = seed_graph()
    summaries = []
    seed_data = None
    final_data = None
    for stage in range(8):
        data, det = audit_graph(vertices, graph)
        if stage == 0:
            seed_data = data
            require(seed_data == (
                ((0, 0, 0, 0, 0, 0), 0),
                ((0, 1, 2, 0, 1, 2), 1),
                ((1, 1, 1, 1, 1, 1), 0),
                ((2, 2, 2, 2, 2, 2), 0),
            ), ("six-site Laurent seed", seed_data))
        final_data = data
        summary = (len(vertices), len(graph), len(data), int(det))
        summaries.append(summary)
        digest.update(repr((summary, tuple(sorted(graph.items())), data)).encode())
        if stage != 7:
            vertices, graph, lift, triple_count = choose_and_audit_split(
                vertices, graph, min(vertices)
            )
            require(lift >= 0 and triple_count >= 0,
                    ("invalid propagation data", lift, triple_count))
            digest.update(repr((lift, triple_count)).encode())

    require(tuple(n for n, _, _, _ in summaries) ==
            tuple(range(6, 22, 2)), ("even arities", summaries))
    closure_ledger = audit_closure_substitution(final_data)
    bell_ledger = audit_bell_projection()
    digest.update(repr((closure_ledger, bell_ledger)).encode())
    result = digest.hexdigest()
    require(result == "7bf07ad7e7e3a697ebfc32088c36ec600c6b4fca6fbede532072f1a2cd08e1bb",
            ("unexpected audit digest", result))

    print("independent global Wick top-invariant audit: PASS")
    for n, edge_count, matching_count, det in summaries:
        print(f"n={n}: edges={edge_count}, matchings={matching_count}, det={det}")
    print("triangle contraction: bijective old sector; new sector positive")
    print("Bell projection: exact GHZ_3; internal support is not one-hot")
    print(f"sha256: {result}")


if __name__ == "__main__":
    main()

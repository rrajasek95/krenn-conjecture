#!/usr/bin/env python3
"""Exact counterguard for polynomial invariants of the top Wick tensor.

This is an independent, standard-library audit of the Laurent degeneration
used in ``notes/global-wick-top-invariant-counterguard.md``.  An edge stores
one colour and one integral exponent of a formal parameter t.  Consequently
every edge block is rank-one and same-colour, while the complete port
covariance is symmetric.

The audit checks, through order 18:

* the triangular-prism seed has top tensor GHZ_3 plus one positive-order
  mixed word;
* vertex-to-triangle expansion preserves the three valuation-zero colour
  factors and leaves every other perfect matching at positive valuation;
* every port (vertex, colour) has exactly one covariance mate, so the global
  3n by 3n covariance is nonsingular;
* at t=2, independent exact Fraction elimination gives determinant
  (-1)^(3n/2), hence determinant +1 or -1 throughout the Laurent family.

Finite enumeration audits the construction, while the accompanying note
proves the expansion and invariant no-go for every even n >= 6.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product


COLORS = (0, 1, 2)


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def edge_key(u: int, v: int) -> tuple[int, int]:
    require(u != v, ("loop edge", u, v))
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices, edges):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        edge = (u, v)
        if edge not in edges:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest, edges):
            yield (edge,) + tail


def matching_term(matching, edges, vertices):
    word = {}
    exponent = 0
    for edge in matching:
        colour, valuation = edges[edge]
        exponent += valuation
        word[edge[0]] = colour
        word[edge[1]] = colour
    require(set(word) == set(vertices), ("matching missed vertices", matching))
    return tuple(word[v] for v in sorted(vertices)), exponent


def prism_seed():
    """The three coloured factors of a prism and its sole extra matching."""
    vertices = set(range(6))
    edges = {}
    for edge, exponent in (((0, 3), 1), ((1, 2), -1), ((4, 5), 0)):
        edges[edge] = (0, exponent)
    for edge in ((1, 4), (0, 2), (3, 5)):
        edges[edge] = (1, 0)
    for edge in ((2, 5), (0, 1), (3, 4)):
        edges[edge] = (2, 0)
    return vertices, edges


def build_expansion(vertices, edges, vertex, shifts):
    incident = []
    for edge, (colour, exponent) in edges.items():
        if vertex in edge:
            neighbour = edge[1] if edge[0] == vertex else edge[0]
            incident.append((colour, neighbour, exponent))
    require(
        sorted(colour for colour, _, _ in incident) == list(COLORS),
        ("expanded vertex is not properly three-coloured", vertex, incident),
    )

    first = max(vertices) + 1
    triangle = {colour: first + colour for colour in COLORS}
    expanded = {edge: data for edge, data in edges.items() if vertex not in edge}
    external = set()
    for colour, neighbour, exponent in incident:
        edge = edge_key(neighbour, triangle[colour])
        expanded[edge] = (colour, exponent + shifts[colour])
        external.add(edge)
    for missing in COLORS:
        other = [colour for colour in COLORS if colour != missing]
        edge = edge_key(triangle[other[0]], triangle[other[1]])
        expanded[edge] = (missing, -shifts[missing])

    expanded_vertices = (set(vertices) - {vertex}) | set(triangle.values())
    return expanded_vertices, expanded, external


def expand_vertex(vertices, edges, vertex):
    """Choose the last shift so every new three-external state is positive."""
    trial_vertices, trial_edges, external = build_expansion(
        vertices, edges, vertex, (0, 0, 0)
    )
    base_exponents = []
    for matching in perfect_matchings(trial_vertices, trial_edges):
        if external <= set(matching):
            _, exponent = matching_term(matching, trial_edges, trial_vertices)
            base_exponents.append(exponent)
    shift = max((1 - exponent for exponent in base_exponents), default=0)
    shift = max(0, shift)
    expanded_vertices, expanded_edges, _ = build_expansion(
        vertices, edges, vertex, (0, 0, shift)
    )
    return expanded_vertices, expanded_edges, shift


def port_pairing(vertices, edges):
    """Return the unique same-colour covariance mate of every port."""
    mates = {}
    exponent_sums = {colour: 0 for colour in COLORS}
    for (u, v), (colour, exponent) in edges.items():
        left = (u, colour)
        right = (v, colour)
        require(
            left not in mates and right not in mates,
            ("a colour port has two covariance mates", left, right),
        )
        mates[left] = (right, exponent)
        mates[right] = (left, exponent)
        exponent_sums[colour] += exponent
    expected_ports = {(v, colour) for v in vertices for colour in COLORS}
    require(set(mates) == expected_ports, "some colour port has no covariance mate")
    require(
        exponent_sums == {colour: 0 for colour in COLORS},
        ("constant-colour products are not normalized", exponent_sums),
    )
    return mates


def exact_determinant(matrix):
    """Fraction Gaussian elimination with row swaps."""
    work = [list(row) for row in matrix]
    size = len(work)
    determinant = Fraction(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        require(pivot is not None, ("singular exact covariance", column))
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        value = work[column][column]
        determinant *= value
        for entry in range(column, size):
            work[column][entry] /= value
        for row in range(column + 1, size):
            scale = work[row][column]
            if not scale:
                continue
            for entry in range(column, size):
                work[row][entry] -= scale * work[column][entry]
    return determinant


def covariance_at_two(vertices, edges):
    ordered = sorted(vertices)
    port_index = {
        (vertex, colour): 3 * position + colour
        for position, vertex in enumerate(ordered)
        for colour in COLORS
    }
    size = 3 * len(vertices)
    matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for (u, v), (colour, exponent) in edges.items():
        weight = Fraction(2**exponent) if exponent >= 0 else Fraction(1, 2 ** (-exponent))
        i = port_index[u, colour]
        j = port_index[v, colour]
        matrix[i][j] = matrix[j][i] = weight
    return matrix


def audit_stage(vertices, edges):
    require(
        len(edges) == 3 * len(vertices) // 2,
        ("not cubic", len(vertices), len(edges)),
    )
    terms = sorted(
        matching_term(matching, edges, vertices)
        for matching in perfect_matchings(vertices, edges)
    )
    zero_terms = [(word, exponent) for word, exponent in terms if exponent == 0]
    expected = [((colour,) * len(vertices), 0) for colour in COLORS]
    require(zero_terms == expected, ("wrong constant term", zero_terms, expected))
    require(
        all(exponent >= 0 for _, exponent in terms),
        ("negative output valuation", terms),
    )
    require(
        sum(exponent > 0 for _, exponent in terms) == len(terms) - 3,
        "a non-pure perfect matching is not at positive valuation",
    )

    # A word determines its matching: at a vertex there is only one incident
    # edge of the requested colour.  The exact enumeration checks this too.
    require(
        len({word for word, _ in terms}) == len(terms),
        "two perfect matchings induce the same colour word",
    )

    mates = port_pairing(vertices, edges)
    require(len(mates) == 3 * len(vertices), "port pairing has wrong size")
    determinant = exact_determinant(covariance_at_two(vertices, edges))
    predicted = Fraction((-1) ** (3 * len(vertices) // 2))
    require(
        determinant == predicted,
        ("wrong exact covariance determinant", len(vertices), determinant, predicted),
    )
    return terms, determinant


def project_bell_chain(arity):
    """Apply the three-codeword block maps to two Bell pairs per link.

    A link label is its two retained/deleted bits, encoded by 0,1,2,3.  A
    product of two Bell signatures sums independently over all four labels.
    Endpoint maps accept labels 0,1,2.  An internal block accepts exactly
    equal incoming/outgoing labels in 0,1,2.  Accepted label c maps to e_c.
    """
    require(arity >= 2, ("Bell chain arity", arity))
    output = defaultdict(int)
    for links in product(range(4), repeat=arity - 1):
        if links[0] not in COLORS or links[-1] not in COLORS:
            continue
        if any(
            links[site - 1] != links[site]
            for site in range(1, arity - 1)
        ):
            continue
        word = (links[0],) + tuple(links[site] for site in range(arity - 2)) + (
            links[-1],
        )
        require(len(word) == arity, ("projected word length", arity, word))
        output[word] += 1
    return dict(output)


def audit_endpoint_dependent_projection_no_go():
    """GHZ is an exact blockwise image of a planar matchgate at every arity."""
    counts = []
    for arity in range(3, 11):
        output = project_bell_chain(arity)
        expected = {(colour,) * arity: 1 for colour in COLORS}
        require(output == expected, ("Bell-chain image is not GHZ", arity, output))
        counts.append((arity, 4 ** (arity - 1), len(output)))
    return counts


def main():
    digest = sha256()
    vertices, edges = prism_seed()
    stage_summaries = []
    for stage in range(7):
        terms, determinant = audit_stage(vertices, edges)
        n = len(vertices)
        if n == 6:
            require(terms == [
                ((0, 0, 0, 0, 0, 0), 0),
                ((0, 1, 2, 0, 1, 2), 1),
                ((1, 1, 1, 1, 1, 1), 0),
                ((2, 2, 2, 2, 2, 2), 0),
            ], ("wrong prism tensor", terms))
        minimum_error = min(exponent for _, exponent in terms if exponent > 0)
        require(minimum_error >= 1, ("nonpositive error gap", n, minimum_error))
        summary = (n, len(edges), len(terms), minimum_error, int(determinant))
        stage_summaries.append(summary)
        digest.update(repr((summary, sorted(edges.items()), terms)).encode())
        if stage < 6:
            vertices, edges, shift = expand_vertex(vertices, edges, min(vertices))
            require(shift >= 0, ("negative triangle shift", n, shift))

    expected_summaries = [
        (6, 9, 4, 1, -1),
        (8, 12, 5, 1, 1),
        (10, 15, 6, 1, -1),
        (12, 18, 8, 1, 1),
        (14, 21, 10, 1, -1),
        (16, 24, 12, 1, 1),
        (18, 27, 16, 1, -1),
    ]
    require(
        stage_summaries == expected_summaries,
        ("unexpected expansion summaries", stage_summaries),
    )
    projection_counts = audit_endpoint_dependent_projection_no_go()
    digest.update(repr(projection_counts).encode())
    result = digest.hexdigest()
    require(
        result == "d5d3199b39bfa81cfba33ebaf38144846488e6cc051cc6a6be12d5ac649bd07c",
        ("unexpected exact audit digest", result),
    )
    print("global Wick top-invariant counterguard: PASS")
    for n, edge_count, matching_count, gap, determinant in stage_summaries:
        print(
            f"n={n}: edges={edge_count}, matchings={matching_count}, "
            f"positive gap={gap}, det(Z)={determinant}"
        )
    print("exact Bell-pair block projection to GHZ_3: arities 3 through 10")
    print(f"sha256: {result}")


if __name__ == "__main__":
    main()

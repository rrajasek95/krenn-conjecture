#!/usr/bin/env python3
"""Exact combinatorial verifier for the prism border degeneration.

An edge stores (color, integer t-valuation).  The verifier enumerates perfect
matchings, checks the six-vertex formula, and tests several iterations of the
vertex-to-triangle expansion used in notes/tensor-route.md.
"""


def key(u, v):
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices, edges):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for v in vertices[1:]:
        e = key(u, v)
        if e not in edges:
            continue
        rest = tuple(x for x in vertices if x not in (u, v))
        for matching in perfect_matchings(rest, edges):
            yield (e,) + matching


def matching_data(matching, edges, vertices):
    coloring = {}
    valuation = 0
    for e in matching:
        color, exponent = edges[e]
        valuation += exponent
        coloring[e[0]] = color
        coloring[e[1]] = color
    return tuple(coloring[v] for v in sorted(vertices)), valuation


def prism():
    edges = {}
    for e, exponent in (((1, 4), 1), ((2, 3), -1), ((5, 6), 0)):
        edges[key(*e)] = (1, exponent)
    for e in ((2, 5), (1, 3), (4, 6)):
        edges[key(*e)] = (2, 0)
    for e in ((3, 6), (1, 2), (4, 5)):
        edges[key(*e)] = (3, 0)
    return set(range(1, 7)), edges


def expand_vertex(vertices, edges, v):
    """Expand v to a colored triangle and choose an exact safe exponent L."""
    incident = []
    for e, (color, exponent) in edges.items():
        if v in e:
            neighbor = e[0] if e[1] == v else e[1]
            incident.append((color, neighbor, exponent, e))
    assert sorted(color for color, _, _, _ in incident) == [1, 2, 3]

    first = max(vertices) + 1
    triangle = {1: first, 2: first + 1, 3: first + 2}

    def build(L):
        a = {1: 0, 2: 0, 3: L}
        new_edges = {
            e: value
            for e, value in edges.items()
            if v not in e
        }
        external = set()
        for color, neighbor, exponent, _ in incident:
            e = key(neighbor, triangle[color])
            new_edges[e] = (color, exponent + a[color])
            external.add(e)
        for missing in (1, 2, 3):
            others = [c for c in (1, 2, 3) if c != missing]
            e = key(triangle[others[0]], triangle[others[1]])
            new_edges[e] = (missing, -a[missing])
        new_vertices = (vertices - {v}) | set(triangle.values())
        return new_vertices, new_edges, external

    # At L=0, find the least valuation among the all-three-external states.
    trial_vertices, trial_edges, external = build(0)
    base_values = []
    for matching in perfect_matchings(trial_vertices, trial_edges):
        if external.issubset(matching):
            _, exponent = matching_data(matching, trial_edges, trial_vertices)
            base_values.append(exponent)
    L = 0 if not base_values else max(0, 1 - min(base_values))
    return build(L)[:2]


vertices, edges = prism()
data = sorted(
    matching_data(m, edges, vertices)
    for m in perfect_matchings(vertices, edges)
)
assert data == [
    ((1, 1, 1, 1, 1, 1), 0),
    ((1, 2, 3, 1, 2, 3), 1),
    ((2, 2, 2, 2, 2, 2), 0),
    ((3, 3, 3, 3, 3, 3), 0),
]

print("n=6: verified Delta_3 + t*(1,2,3,1,2,3)")

for _ in range(3):
    v = min(vertices)
    vertices, edges = expand_vertex(vertices, edges, v)
    terms = [
        matching_data(m, edges, vertices)
        for m in perfect_matchings(vertices, edges)
    ]
    constant_zero = {
        coloring
        for coloring, exponent in terms
        if exponent == 0
    }
    expected = {
        tuple(color for _ in vertices)
        for color in (1, 2, 3)
    }
    assert constant_zero == expected
    assert all(
        exponent == 0 or exponent > 0
        for _, exponent in terms
    )
    assert sum(exponent == 0 for _, exponent in terms) == 3
    print(
        f"n={len(vertices)}: verified 3 valuation-zero color classes and "
        f"{len(terms) - 3} positive-valuation matchings"
    )

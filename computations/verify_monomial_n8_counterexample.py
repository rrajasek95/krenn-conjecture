#!/usr/bin/env python3
"""Verify the smallest no-singleton monomial labeling and its weight obstruction.

The complete graph K_8 is endpoint-labeled by the same color at both ends.
It has three constant-color perfect matchings, but every mixed coloring has a
two-element perfect-matching fiber.  Thus the tempting ``mixed singleton``
lemma is false at n=8.

The example still cannot realize a GHZ tensor with nonzero edge weights.  A
three-fiber multiplicative certificate makes the binomial cancellation
equations inconsistent over C^*: if R_j is the ratio of the two matching
monomials in fiber j, then R_6 R_10 / R_1 = 1 identically, whereas cancelling
the three fibers would require all three ratios to equal -1.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations


N = 8
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))

# Every edge uv has ordered endpoint label (EDGE_COLOR[uv], EDGE_COLOR[uv]).
COLOR_ONE = frozenset({(0, 2), (1, 3), (4, 6), (5, 7)})
COLOR_TWO = frozenset(
    {(0, 4), (0, 6), (1, 5), (1, 7),
     (2, 4), (2, 6), (3, 5), (3, 7)}
)
EDGE_COLOR = {
    edge: 1 if edge in COLOR_ONE else 2 if edge in COLOR_TWO else 0
    for edge in EDGES
}


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + matching))


MATCHINGS = tuple(perfect_matchings(VERTICES))


def induced_coloring(matching):
    coloring = [-1] * N
    for u, v in matching:
        coloring[u] = coloring[v] = EDGE_COLOR[u, v]
    return tuple(coloring)


def exponent_difference(first, second):
    """Exponent vector of matching monomial(first)/monomial(second)."""

    return tuple(int(edge in first) - int(edge in second) for edge in EDGES)


def main() -> None:
    assert len(MATCHINGS) == 105
    fibers = defaultdict(list)
    for matching in MATCHINGS:
        fibers[induced_coloring(matching)].append(matching)

    sizes = Counter(map(len, fibers.values()))
    assert sizes == Counter({2: 38, 24: 1, 1: 1, 4: 1})
    assert [len(fibers[(color,) * N]) for color in range(3)] == [24, 1, 4]
    mixed = [(coloring, matchings) for coloring, matchings in fibers.items()
             if len(set(coloring)) > 1]
    assert len(mixed) == 38
    assert all(len(matchings) == 2 for _, matchings in mixed)

    # A small exact inconsistency certificate.  The ordering here is the
    # deterministic insertion ordering induced by MATCHINGS above.
    certificate_indices = (1, 6, 10)
    certificate = [mixed[index] for index in certificate_indices]
    expected = (
        (
            (0, 0, 2, 2, 2, 2, 0, 0),
            (((0, 1), (2, 4), (3, 5), (6, 7)),
             ((0, 7), (1, 6), (2, 4), (3, 5))),
        ),
        (
            (0, 0, 2, 2, 0, 2, 2, 0),
            (((0, 1), (2, 6), (3, 5), (4, 7)),
             ((0, 7), (1, 4), (2, 6), (3, 5))),
        ),
        (
            (1, 0, 1, 2, 0, 2, 0, 0),
            (((0, 2), (1, 4), (3, 5), (6, 7)),
             ((0, 2), (1, 6), (3, 5), (4, 7))),
        ),
    )
    assert tuple((coloring, tuple(matchings))
                 for coloring, matchings in certificate) == expected

    d1, d6, d10 = (
        exponent_difference(matchings[0], matchings[1])
        for _, matchings in certificate
    )
    # Hence R_6 R_10 / R_1 = 1 for every assignment of nonzero edge weights.
    assert all(-a + b + c == 0 for a, b, c in zip(d1, d6, d10))

    print("verified K8 fiber distribution:", dict(sorted(sizes.items())))
    print("constant-color fiber sizes: 24, 1, 4")
    print("all 38 mixed fibers have size two")
    print("weight obstruction: -d_1 + d_6 + d_10 = 0, coefficient sum = 1")


if __name__ == "__main__":
    main()

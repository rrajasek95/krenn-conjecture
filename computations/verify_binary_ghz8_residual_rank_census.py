#!/usr/bin/env python3
"""Exact residual differential-rank census for sparse binary GHZ8 sources.

Research evidence only.  This is not a classification of binary GHZ8
sources and does not prove a rank bound.  It independently reconstructs four
sparse exact source families already implicit in the repository, verifies all 256
coefficients of each matching tensor, and computes the rank of dPsi after
all 28 endpoint-pair deletions.

The sources are the alternating cycle, the two-matching switch over both
Q(sqrt(2)) and Q(sqrt(3)), the rational cancellation source used by the pair
cap obstruction, and a two-vertex subdivision of the active-rank-two K6
gadget.  Their maximum six-site differential ranks are respectively
22, 26, 31, and 26, below the open rank-55 L0 stratum.  In every deletion
the rank after removing the two pure output rows is exactly two smaller, as
is necessary for an actual binary endpoint completion.

Standard library only; every check remains live under python -O and
python -I -S.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class Quadratic:
    """An element a+b*sqrt(d) of Q(sqrt(d))."""

    __slots__ = ("a", "b", "d")

    def __init__(self, a=0, b=0, d=2):
        self.a = Q(a)
        self.b = Q(b)
        self.d = int(d)

    def _coerce(self, other):
        if isinstance(other, Quadratic):
            require(other.d == self.d, "mixed quadratic fields")
            return other
        return Quadratic(other, 0, self.d)

    def __add__(self, other):
        other = self._coerce(other)
        return Quadratic(self.a + other.a, self.b + other.b, self.d)

    __radd__ = __add__

    def __neg__(self):
        return Quadratic(-self.a, -self.b, self.d)

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __mul__(self, other):
        other = self._coerce(other)
        return Quadratic(
            self.a * other.a + self.d * self.b * other.b,
            self.a * other.b + self.b * other.a,
            self.d,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self._coerce(other)
        norm = other.a * other.a - self.d * other.b * other.b
        require(norm != 0, "division by zero in quadratic field")
        return Quadratic(
            (self.a * other.a - self.d * self.b * other.b) / norm,
            (self.b * other.a - self.a * other.b) / norm,
            self.d,
        )

    def __rtruediv__(self, other):
        return self._coerce(other) / self

    def __bool__(self):
        return bool(self.a or self.b)

    def __eq__(self, other):
        other = self._coerce(other)
        return self.a == other.a and self.b == other.b

    def __repr__(self):
        return f"Quadratic({self.a!r}, {self.b!r}, {self.d!r})"


VERTICES = tuple(range(8))
SITES = tuple(range(6))
COLOURS = (0, 1)
LOCAL_EDGES = tuple(combinations(SITES, 2))
CELLS = tuple(
    (u, v, a, b)
    for u, v in LOCAL_EDGES
    for a, b in product(COLOURS, repeat=2)
)
WORDS6 = tuple(product(COLOURS, repeat=6))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = {
    vertices: perfect_matchings(vertices)
    for size in (0, 2, 4, 6, 8)
    for vertices in combinations(VERTICES, size)
}


def put(edges, u, v, cells):
    require(u < v, "edge orientation is not increasing")
    edges[u, v] = dict(cells)


def entry(edges, u, v, a, b):
    if u < v:
        return edges.get((u, v), {}).get((a, b), 0)
    return edges.get((v, u), {}).get((b, a), 0)


def coefficient(edges, vertices, word):
    local = dict(zip(vertices, word))
    answer = 0
    for matching in MATCHINGS[tuple(vertices)]:
        term = 1
        for u, v in matching:
            term *= entry(edges, u, v, local[u], local[v])
        answer += term
    return answer


def matching_tensor(edges):
    answer = {}
    for word in product(COLOURS, repeat=8):
        value = coefficient(edges, VERTICES, word)
        if value:
            answer[word] = value
    return answer


def residual_packet(edges, deleted):
    remaining = tuple(v for v in VERTICES if v not in deleted)
    return {
        (u, v, a, b): entry(edges, remaining[u], remaining[v], a, b)
        for u, v in LOCAL_EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def local_cofactor(packet, word, u, v):
    remaining = tuple(site for site in SITES if site not in (u, v))
    answer = 0
    for matching in perfect_matchings(remaining):
        term = 1
        for r, s in matching:
            term *= packet[r, s, word[r], word[s]]
        answer += term
    return answer


def differential_matrix(packet):
    return [
        [
            local_cofactor(packet, word, u, v)
            if (word[u], word[v]) == (a, b) else 0
            for u, v, a, b in CELLS
        ]
        for word in WORDS6
    ]


def field_rank(matrix):
    rows = [list(row) for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(rows))
             if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for index in range(rank + 1, len(rows)):
            multiple = rows[index][column]
            if multiple:
                rows[index] = [
                    left - multiple * right
                    for left, right in zip(rows[index], rows[rank])
                ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def alternating_cycle_source():
    edges = {}
    for vertex in range(0, 8, 2):
        put(edges, vertex, vertex + 1, {(0, 0): Q(1)})
    for vertex in range(1, 7, 2):
        put(edges, vertex, vertex + 1, {(1, 1): Q(1)})
    put(edges, 0, 7, {(1, 1): Q(1)})
    return edges


def switched_source(radicand, first_weight, second_weight):
    """Two colour-zero matchings on a switched C4 and one colour-one cycle."""

    edges = {}
    for edge in ((0, 1), (2, 3)):
        put(edges, *edge, {(0, 0): first_weight})
    for edge in ((0, 2), (1, 3)):
        put(edges, *edge, {(0, 0): second_weight})
    for edge in ((4, 5), (6, 7)):
        put(edges, *edge, {(0, 0): Quadratic(1, 0, radicand)})
    for edge in ((1, 2), (3, 4), (5, 6), (0, 7)):
        put(edges, *edge, {(1, 1): Quadratic(1, 0, radicand)})
    return edges


def rational_cancellation_source():
    edges = {}
    put(edges, 0, 1, {(0, 0): Q(1), (1, 0): Q(1)})
    put(edges, 2, 3, {(0, 0): Q(1)})
    put(edges, 1, 3, {(0, 0): Q(1)})
    put(edges, 0, 2, {(1, 0): Q(-1)})
    put(edges, 0, 5, {(1, 1): Q(1)})
    put(edges, 1, 2, {(1, 1): Q(1)})
    put(edges, 3, 4, {(1, 1): Q(3, 4)})
    put(edges, 0, 4, {(1, 1): Q(1, 2)})
    put(edges, 3, 5, {(1, 1): Q(1, 2)})
    put(edges, 4, 6, {(0, 0): Q(1)})
    put(edges, 5, 7, {(0, 0): Q(1)})
    put(edges, 6, 7, {(1, 1): Q(1)})
    return edges


def subdivided_rank_two_source():
    """Subdivide the separating (2,3,0,0) cell in the exact K6 gadget."""

    edges = {}
    put(edges, 0, 1, {(0, 0): Q(1)})
    put(edges, 2, 3, {(1, 1): Q(1)})
    put(edges, 0, 2, {(0, 1): Q(-1)})
    put(edges, 1, 3, {(0, 1): Q(1)})
    put(edges, 4, 5, {(0, 0): Q(1)})
    put(edges, 0, 5, {(1, 1): Q(1)})
    put(edges, 1, 2, {(1, 1): Q(1)})
    put(edges, 3, 4, {(1, 1): Q(1)})
    put(edges, 2, 6, {(0, 0): Q(1)})
    put(edges, 3, 7, {(0, 0): Q(1)})
    put(edges, 6, 7, {(1, 1): Q(1)})
    return edges


EXPECTED = {
    "alternating cycle": Counter({
        (22, 20): 8, (12, 10): 8, (14, 12): 8, (16, 14): 4,
    }),
    "two-matching switch": Counter({
        (20, 18): 6, (22, 20): 5, (14, 12): 5,
        (26, 24): 5, (18, 16): 4, (16, 14): 3,
    }),
    "rational cancellation": Counter({
        (28, 26): 6, (18, 16): 6, (19, 17): 6, (21, 19): 3,
        (26, 24): 2, (31, 29): 2, (14, 12): 1, (17, 15): 1,
        (29, 27): 1,
    }),
    "subdivided rank-two": Counter({
        (26, 24): 6, (22, 20): 5, (16, 14): 4, (20, 18): 3,
        (25, 23): 2, (14, 12): 2, (18, 16): 2, (15, 13): 2,
        (12, 10): 2,
    }),
}


def audit_source(name, edges, expected):
    target = {(0,) * 8: 1, (1,) * 8: 1}
    require(matching_tensor(edges) == target, (name, "not binary GHZ8"))

    ranks = []
    for deleted in combinations(VERTICES, 2):
        matrix = differential_matrix(residual_packet(edges, deleted))
        full_rank = field_rank(matrix)
        mixed_rank = field_rank(matrix[1:-1])
        require(full_rank - mixed_rank == 2,
                (name, deleted, full_rank, mixed_rank))
        ranks.append((full_rank, mixed_rank))
    histogram = Counter(ranks)
    require(histogram == expected, (name, histogram))
    return max(full for full, _mixed in ranks)


def main():
    sqrt_two_half = Quadratic(0, Q(1, 2), 2)
    sqrt_three_half = Quadratic(0, Q(1, 2), 3)
    sources = (
        ("alternating cycle", alternating_cycle_source(),
         EXPECTED["alternating cycle"]),
        ("Q(sqrt(2)) switch", switched_source(
            2, sqrt_two_half, sqrt_two_half
        ), EXPECTED["two-matching switch"]),
        ("Q(sqrt(3)) switch", switched_source(
            3, Quadratic(Q(1, 2), 0, 3), sqrt_three_half
        ), EXPECTED["two-matching switch"]),
        ("rational cancellation", rational_cancellation_source(),
         EXPECTED["rational cancellation"]),
        ("subdivided rank-two", subdivided_rank_two_source(),
         EXPECTED["subdivided rank-two"]),
    )
    maxima = {}
    for name, edges, expected in sources:
        maxima[name] = audit_source(name, edges, expected)

    require(maxima == {
        "alternating cycle": 22,
        "Q(sqrt(2)) switch": 26,
        "Q(sqrt(3)) switch": 26,
        "rational cancellation": 31,
        "subdivided rank-two": 26,
    }, maxima)
    print("PASS: five exact binary GHZ8 sources, all 256 coefficients each")
    print("PASS: 140 endpoint deletions, exact full/mixed rank gap two")
    print("maximum residual ranks:", maxima)
    print("audited sparse-source maximum 31; no global rank bound is asserted")


if __name__ == "__main__":
    main()

"""Exact checks for notes/finite-obstruction.md.

This verifies the triangular-prism matching list, the SL/target-stabilizer
one-parameter subgroup, and the degree-nine Nullstellensatz certificate.
All calculations are over the integers (or symbolic Laurent monomials).
"""

from __future__ import annotations

import itertools

import sympy as sp


VERTICES = tuple(range(6))
M0 = frozenset({(0, 4), (1, 2), (3, 5)})
M1 = frozenset({(0, 5), (1, 4), (2, 3)})
M2 = frozenset({(0, 3), (1, 5), (2, 4)})
H = frozenset({(0, 4), (1, 5), (2, 3)})
PRISM = M0 | M1 | M2


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield frozenset()
        return
    u = vertices[0]
    for position in range(1, len(vertices)):
        v = vertices[position]
        edge = tuple(sorted((u, v)))
        if edge not in PRISM:
            continue
        remainder = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(remainder):
            yield matching | {edge}


assert set(perfect_matchings(VERTICES)) == {M0, M1, M2, H}

# Rows are vertices and columns are colors.
h = (
    (0, -1, 1),
    (1, -1, 0),
    (0, 1, -1),
    (-1, 1, 0),
    (0, 0, 0),
    (0, 0, 0),
)
assert all(sum(row) == 0 for row in h)  # local SL(3)
assert all(sum(h[v][color] for v in VERTICES) == 0 for color in range(3))


def edge_exponent(edge: tuple[int, int], color: int) -> int:
    u, v = edge
    return h[u][color] + h[v][color]


expected = {
    (0, (0, 4)): 0,
    (0, (1, 2)): 1,
    (0, (3, 5)): -1,
    (1, (0, 5)): -1,
    (1, (1, 4)): -1,
    (1, (2, 3)): 2,
    (2, (0, 3)): 1,
    (2, (1, 5)): 0,
    (2, (2, 4)): -1,
}
assert {
    (color, edge): edge_exponent(edge, color)
    for color, matching in enumerate((M0, M1, M2))
    for edge in matching
} == expected
assert sum(edge_exponent(edge, color) for color, edge in ((0, (0, 4)), (2, (1, 5)), (1, (2, 3)))) == 2


def epsilon(colors: tuple[int, int, int]) -> int:
    if len(set(colors)) < 3:
        return 0
    inversions = sum(
        colors[left] > colors[right]
        for left in range(3)
        for right in range(left + 1, 3)
    )
    return -1 if inversions % 2 else 1


# The cubic output epsilon invariant is 6 both on Delta and on Delta+E.
error_coloring = (0, 2, 1, 1, 0, 2)
output_support = ((0,) * 6, (1,) * 6, (2,) * 6, error_coloring)
output_epsilon_invariant = sum(
    sp.prod(epsilon((first[v], second[v], third[v])) for v in VERTICES)
    for first in output_support
    for second in output_support
    for third in output_support
)
assert output_epsilon_invariant == 6

a04, a12, a35, b05, b14, b23, c03, c15, c24 = sp.symbols(
    "a04 a12 a35 b05 b14 b23 c03 c15 c24"
)
p0 = a04 * a12 * a35
p1 = b05 * b14 * b23
p2 = c03 * c15 * c24
r = a04 * c15 * b23
q = a12 * a35 * b05 * b14 * c03 * c24
f0, f1, f2 = p0 - 1, p1 - 1, p2 - 1
certificate = -f0 - p0 * f1 - p0 * p1 * f2 + q * r
assert sp.expand(certificate) == 1
assert sp.expand(p0 * p1 * p2 - q * r) == 0

# Substitution of the Laurent border family.
t = sp.symbols("t", nonzero=True)
border = {
    a04: 1,
    a12: t,
    a35: t**-1,
    b05: t**-1,
    b14: t**-1,
    b23: t**2,
    c03: t,
    c15: 1,
    c24: t**-1,
}
assert tuple(sp.simplify(p.subs(border)) for p in (p0, p1, p2, r, q)) == (
    1,
    1,
    1,
    t**2,
    t**-2,
)

print("finite-obstruction checks passed exactly")

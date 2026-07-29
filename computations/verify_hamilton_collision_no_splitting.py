#!/usr/bin/env python3
"""Combinatorial audit of the least-cell collision no-splitting theorem.

For n=4,6,8,10,12 this checks, without floating point arithmetic:

* the weighted alternating cycle realizes 2 X + Y;
* deleting equal-parity vertices has zero cofactor, while deleting
  opposite-parity vertices has one coordinate cofactor;
* all active one-z derivative atoms at a fixed z site are distinct;
* same-shore tangent-kernel cells cannot make the required two-z/all-x
  Hessian coefficient.

The proof in the accompanying note works for every even n >= 4; these
finite cases audit its exact combinatorial assertions.
"""

from __future__ import annotations

from itertools import combinations
from fractions import Fraction


X, Y, Z = "x", "y", "z"


def canonical(edge):
    u, v = edge
    return (u, v) if u < v else (v, u)


def cycle_source(n):
    px = tuple((i, i + 1) for i in range(0, n, 2))
    py = tuple((i, i + 1) for i in range(1, n - 1, 2)) + ((0, n - 1),)
    # Scalar integer weights.  The x product is 2 and the y product is 1.
    cells = {}
    for position, edge in enumerate(px):
        cells[canonical(edge)] = (X, 2 if position == 0 else 1)
    for edge in py:
        cells[canonical(edge)] = (Y, 1)
    return px, py, cells


def supported_matchings(vertices, cells):
    """Enumerate matchings using the underlying edges in ``cells``."""
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        edge = canonical((u, v))
        if edge not in cells:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in supported_matchings(rest, cells):
            yield (edge,) + tail


def matching_tensor(matching, cells, n, removed=()):
    coloring = [None] * n
    weight = 1
    for edge in matching:
        color, scalar = cells[edge]
        weight *= scalar
        for vertex in edge:
            coloring[vertex] = color
    for vertex in removed:
        assert coloring[vertex] is None
    return tuple(coloring), weight


def cofactor_terms(n, cells, i, j):
    remaining = tuple(v for v in range(n) if v not in (i, j))
    return [
        matching_tensor(matching, cells, n, removed=(i, j))
        for matching in supported_matchings(remaining, cells)
    ]


def audit(n):
    px, py, cells = cycle_source(n)
    px_set = {canonical(edge) for edge in px}

    full = [
        matching_tensor(matching, cells, n)
        for matching in supported_matchings(range(n), cells)
    ]
    assert sorted(full) == sorted([((X,) * n, 2), ((Y,) * n, 1)])

    active_atoms = {}
    for i, j in combinations(range(n), 2):
        terms = cofactor_terms(n, cells, i, j)
        if i % 2 == j % 2:
            assert terms == []
        else:
            assert len(terms) == 1
            coloring, weight = terms[0]
            assert weight != 0
            for z_site, companion in ((i, j), (j, i)):
                for companion_color in (X, Y):
                    atom = list(coloring)
                    atom[z_site] = Z
                    atom[companion] = companion_color
                    key = (z_site, companion, companion_color)
                    active_atoms[key] = tuple(atom)

    # At fixed z_site, all opposite-shore x/y derivative atoms are distinct.
    for i in range(n):
        atoms = [
            coloring
            for (z_site, _companion, _color), coloring in active_atoms.items()
            if z_site == i
        ]
        assert len(atoms) == n
        assert len(set(atoms)) == n

    # The exact-one-z tangent kernel therefore only uses same-shore
    # companions.  Two such cells at equal-parity z sites cannot leave an
    # all-x P_x completion.
    checked_pairs = 0
    candidate_products = 0
    for i, j in combinations(range(n), 2):
        if i % 2 != j % 2:
            continue
        checked_pairs += 1
        assert cofactor_terms(n, cells, i, j) == []  # every Y2 correction

        same_i = [u for u in range(n) if u != i and u % 2 == i % 2]
        same_j = [v for v in range(n) if v != j and v % 2 == j % 2]
        for u in same_i:
            for v in same_j:
                if len({i, j, u, v}) < 4:
                    continue  # the product of source cells is squarefree-zero
                candidate_products += 1
                removed = {i, j, u, v}
                # An all-x completion is a subset of P_x covering exactly
                # the remaining vertices.
                remaining = set(range(n)) - removed
                completion = {
                    vertex
                    for edge in px_set
                    if set(edge).issubset(remaining)
                    for vertex in edge
                }
                assert completion != remaining

    assert checked_pairs == 2 * ((n // 2) * (n // 2 - 1) // 2)
    print(
        f"n={n}: H=2X+Y; {n*(n-1)//2} cofactors audited; "
        f"{checked_pairs} same-shore X2 coefficients vanish; "
        f"{candidate_products} disjoint kernel-cell products rejected"
    )


def audit_four_site_transport_obstruction():
    """The exact K4 collision arc has a nonliftable base star kernel."""
    n = 4
    minus = ((0, 1), (2, 3))
    y_matching = ((0, 2), (1, 3))
    plus = ((0, 3), (1, 2))

    q0 = {}
    q1 = {}
    for edge in minus:
        edge = canonical(edge)
        q0[edge] = X
        for vertex in edge:
            q1[(edge, vertex)] = Fraction(-1, 2)
    for edge in y_matching:
        q0[canonical(edge)] = Y
    for edge in plus:
        edge = canonical(edge)
        q0[edge] = X
        for vertex in edge:
            q1[(edge, vertex)] = Fraction(1, 2)

    def incident(matching, p):
        return canonical(next(edge for edge in matching if p in edge))

    for p in range(n):
        minus_edge = incident(minus, p)
        plus_edge = incident(plus, p)
        y_edge = incident(y_matching, p)
        z_site = next(v for v in y_edge if v != p)

        # D0 has +1 on the minus xx cell and -1 on the plus xx cell.
        defect = Fraction(0)
        for star_edge, d0_coefficient in (
            (minus_edge, Fraction(1)),
            (plus_edge, Fraction(-1)),
        ):
            complement = canonical(
                tuple(v for v in range(n) if v not in star_edge)
            )
            defect += d0_coefficient * q1[(complement, z_site)]
        assert defect == -1

        # A p-star cell producing the target with its z at z_site must lie
        # on the p--z_site edge.  Its complementary q0 edge is the other
        # y-matching edge, so F0 has zero all-x coefficient there.
        complement = canonical(tuple(v for v in range(n) if v not in y_edge))
        assert q0[complement] == Y

    print("n=4: verified nonzero first transport cokernel class at every star")


def main():
    for n in (4, 6, 8, 10, 12):
        audit(n)
    audit_four_site_transport_obstruction()
    print("verified Hamilton least-cell collision no-splitting combinatorics")


if __name__ == "__main__":
    main()

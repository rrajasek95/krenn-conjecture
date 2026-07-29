#!/usr/bin/env python3
"""Exact audit for the Fourier root-of-unity lifting note.

The coefficient field is Q(omega), omega^2 + omega + 1 = 0.  We verify the
six-site member of the connected active-edge counterfamily:

* its divided third power is
      3 Z_4 tensor (sum_s f_s tensor f_(-s));
* this output is fixed by the global charge action g;
* (gq-q)(q^2+q(gq)+(gq)^2)=0 in the site-square-zero algebra;
* the support graph is connected and every aggregate edge has a nonzero
  four-site cofactor; and
* gq is not an ordinary vertex-scalar gauge of q.

We also construct the first inductive attachment through eight sites and verify
their claimed matching tensors, connectedness, edge activity, and failure of
vertex-scalar lifting.  The output flattening has rank three at every site,
and the quadratic itself has nonzero parts in all three global charge sectors.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class E:
    """a+b*omega in Q(omega), with omega^2=-1-omega."""

    a: int = 0
    b: int = 0

    def __add__(self, other: "E") -> "E":
        return E(self.a + other.a, self.b + other.b)

    def __neg__(self) -> "E":
        return E(-self.a, -self.b)

    def __sub__(self, other: "E") -> "E":
        return self + (-other)

    def __mul__(self, other: "E") -> "E":
        # (a+bw)(c+dw)=(ac-bd)+(ad+bc-bd)w.
        return E(
            self.a * other.a - self.b * other.b,
            self.a * other.b + self.b * other.a - self.b * other.b,
        )

    def __rmul__(self, integer: int) -> "E":
        return E(integer * self.a, integer * self.b)

    def __bool__(self) -> bool:
        return self.a != 0 or self.b != 0


ZERO = E()
ONE = E(1, 0)
OMEGA = E(0, 1)
OMEGA2 = E(-1, -1)
ROOTS = (ONE, OMEGA, OMEGA2)


def outer(left: tuple[E, ...], right: tuple[E, ...]) -> tuple[tuple[E, ...], ...]:
    return tuple(tuple(x * y for y in right) for x in left)


F0 = (ONE, ZERO, ZERO)
F1 = (ZERO, ONE, ZERO)
CHARGE_ZERO = tuple(
    tuple(ONE if (a + b) % 3 == 0 else ZERO for b in range(3))
    for a in range(3)
)
U = (
    (ONE, ONE, ONE),
    (ONE, OMEGA, OMEGA2),
    (ONE, OMEGA2, OMEGA),
)


Matrix = tuple[tuple[E, ...], ...]
Edges = dict[tuple[int, int], Matrix]


def set_edge(edges: Edges, u: int, v: int, matrix: Matrix) -> None:
    assert u < v
    assert any(matrix[a][b] for a in range(3) for b in range(3))
    edges[(u, v)] = matrix


def build_counterfamily(n: int) -> Edges:
    assert n >= 6 and n % 2 == 0
    edges: Edges = {}

    # Fourier transform of the exact three-one-factor source on K_4.
    for r, matching in enumerate((((0, 1), (2, 3)),
                                  ((0, 2), (1, 3)),
                                  ((0, 3), (1, 2)))):
        matrix = outer(U[r], U[r])
        for u, v in matching:
            set_edge(edges, u, v, matrix)

    # Each new pair has a charge-zero base edge.  Its two possible cross
    # matchings through old vertices 0,1 have equal and opposite tensors.
    for a in range(4, n, 2):
        b = a + 1
        set_edge(edges, a, b, CHARGE_ZERO)
        set_edge(edges, 0, a, outer(F0, F1))
        set_edge(edges, 0, b, outer(F0, F1))
        set_edge(edges, 1, a, tuple(tuple(-z for z in row) for row in outer(F1, F1)))
        set_edge(edges, 1, b, outer(F1, F1))
    return edges


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for pos in range(1, len(vertices)):
        v = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            yield ((u, v),) + matching


def edge_entry(edges: Edges, u: int, v: int, a: int, b: int) -> E:
    if u < v:
        matrix = edges.get((u, v))
        return ZERO if matrix is None else matrix[a][b]
    matrix = edges.get((v, u))
    return ZERO if matrix is None else matrix[b][a]


def hafnian_coeff(edges: Edges, vertices: tuple[int, ...], colors: tuple[int, ...]) -> E:
    color = dict(zip(vertices, colors))
    total = ZERO
    for matching in perfect_matchings(vertices):
        term = ONE
        for u, v in matching:
            term = term * edge_entry(edges, u, v, color[u], color[v])
            if not term:
                break
        total = total + term
    return total


def matching_tensor(edges: Edges, vertices: tuple[int, ...]) -> dict[tuple[int, ...], E]:
    return {
        colors: coefficient
        for colors in product(range(3), repeat=len(vertices))
        if (coefficient := hafnian_coeff(edges, vertices, colors))
    }


def charge_transform(edges: Edges) -> Edges:
    transformed: Edges = {}
    for edge, matrix in edges.items():
        transformed[edge] = tuple(
            tuple(ROOTS[(a + b) % 3] * matrix[a][b] for b in range(3))
            for a in range(3)
        )
    return transformed


# A square-zero polynomial is keyed by a tuple with -1 at unoccupied sites.
Polynomial = dict[tuple[int, ...], E]


def quadratic_polynomial(edges: Edges, n: int) -> Polynomial:
    result: Polynomial = {}
    for (u, v), matrix in edges.items():
        for a in range(3):
            for b in range(3):
                if matrix[a][b]:
                    key = [-1] * n
                    key[u], key[v] = a, b
                    result[tuple(key)] = result.get(tuple(key), ZERO) + matrix[a][b]
    return {key: value for key, value in result.items() if value}


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for key, value in right.items():
        result[key] = result.get(key, ZERO) + value
        if not result[key]:
            del result[key]
    return result


def poly_scale(poly: Polynomial, scalar: E) -> Polynomial:
    return {key: scalar * value for key, value in poly.items() if scalar * value}


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    if not left or not right:
        return {}
    n = len(next(iter(left)))
    result: Polynomial = {}
    for key_l, value_l in left.items():
        for key_r, value_r in right.items():
            if any(key_l[v] >= 0 and key_r[v] >= 0 for v in range(n)):
                continue
            key = tuple(key_l[v] if key_l[v] >= 0 else key_r[v] for v in range(n))
            result[key] = result.get(key, ZERO) + value_l * value_r
    return {key: value for key, value in result.items() if value}


def poly_pow(poly: Polynomial, exponent: int, n: int) -> Polynomial:
    unit = {tuple([-1] * n): ONE}
    result = unit
    for _ in range(exponent):
        result = poly_mul(result, poly)
    return result


def support_connected(edges: Edges, n: int) -> bool:
    adjacency = {v: set() for v in range(n)}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    seen = {0}
    frontier = [0]
    while frontier:
        u = frontier.pop()
        for v in adjacency[u] - seen:
            seen.add(v)
            frontier.append(v)
    return len(seen) == n


def all_edges_active(edges: Edges, n: int) -> bool:
    for u, v in edges:
        remainder = tuple(w for w in range(n) if w not in (u, v))
        if not matching_tensor(edges, remainder):
            return False
    return True


def expected_counterfamily_tensor(n: int) -> dict[tuple[int, ...], E]:
    return {
        colors: E(3, 0)
        for colors in product(range(3), repeat=n)
        if sum(colors[:4]) % 3 == 0
        and all((colors[a] + colors[a + 1]) % 3 == 0 for a in range(4, n, 2))
    }


def mode_concise_from_disjoint_slices(
    tensor: dict[tuple[int, ...], E], n: int
) -> bool:
    """Certify rank three by nonempty, pairwise-disjoint row supports."""
    for site in range(n):
        supports = []
        for color in range(3):
            support = {
                key[:site] + key[site + 1 :]
                for key, value in tensor.items()
                if value and key[site] == color
            }
            if not support:
                return False
            supports.append(support)
        if any(supports[a] & supports[b] for a in range(3) for b in range(a + 1, 3)):
            return False
    return True


def source_charge_sectors(edges: Edges) -> set[int]:
    return {
        (a + b) % 3
        for matrix in edges.values()
        for a in range(3)
        for b in range(3)
        if matrix[a][b]
    }


def not_vertex_scalar_lift(edges: Edges) -> bool:
    # A vertex-scalar lift would make gA_01 a constant multiple of A_01.
    matrix = edges[(0, 1)]
    transformed = charge_transform({(0, 1): matrix})[(0, 1)]
    # The (0,0) and (1,0) entries of A_01 are both one, whereas their
    # transformed entries are 1 and omega.
    return (
        matrix[0][0] == ONE
        and matrix[1][0] == ONE
        and transformed[0][0] == ONE
        and transformed[1][0] == OMEGA
        and transformed[0][0] * matrix[1][0]
        != transformed[1][0] * matrix[0][0]
    )


def audit_n6_root_identity() -> None:
    n = 6
    edges = build_counterfamily(n)
    transformed = charge_transform(edges)
    tensor = matching_tensor(edges, tuple(range(n)))
    assert tensor == expected_counterfamily_tensor(n)
    assert matching_tensor(transformed, tuple(range(n))) == tensor

    q = quadratic_polynomial(edges, n)
    gq = quadratic_polynomial(transformed, n)
    q2 = poly_mul(q, q)
    qgq = poly_mul(q, gq)
    gq2 = poly_mul(gq, gq)
    comparison = poly_add(poly_add(q2, qgq), gq2)
    difference = poly_add(gq, poly_scale(q, E(-1, 0)))
    assert difference
    assert not poly_mul(difference, comparison)
    assert poly_pow(q, 3, n) == poly_pow(gq, 3, n)


def main() -> None:
    audit_n6_root_identity()
    # Full coefficient enumeration at n=8 already audits the inductive step;
    # the proof in the note then repeats the identical attachment at all
    # larger even orders.
    for n in (6, 8):
        edges = build_counterfamily(n)
        vertices = tuple(range(n))
        tensor = matching_tensor(edges, vertices)
        assert tensor == expected_counterfamily_tensor(n)
        assert matching_tensor(charge_transform(edges), vertices) == tensor
        assert support_connected(edges, n)
        assert all_edges_active(edges, n)
        assert not_vertex_scalar_lift(edges)
        assert mode_concise_from_disjoint_slices(tensor, n)
        assert source_charge_sectors(edges) == {0, 1, 2}
        # This globally zero-sum word is deliberately absent: the first
        # four sites have sum one and the first added pair has sum two.
        missing = (1, 0, 0, 0, 1, 1) + (0,) * (n - 6)
        assert sum(missing) % 3 == 0 and missing not in tensor
        print(
            f"n={n}: {len(edges)} active edges, connected support, "
            f"mode-concise invariant output with {len(tensor)} nonzero coefficients",
            flush=True,
        )
    print("PASS: Fourier symmetry lifting obstruction and counterfamily")


if __name__ == "__main__":
    main()

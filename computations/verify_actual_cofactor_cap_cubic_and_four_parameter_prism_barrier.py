#!/usr/bin/env python3
"""Exact audit of the actual-cofactor cap cubic and common-edge prism barrier.

The audit performs three independent checks.

1. It expands the formal denominator-cleared cofactor cubic and the
   two-site-cap factorization.
2. It enumerates every supported matching of the explicit ten-site
   aggregate edge family in the companion note.
3. It constructs every six-site pair cofactor from that same edge family,
   contracts the top tensor, and verifies the unit-saturation prism
   formula over Q[z0,z1,z2,t].
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from itertools import product

import sympy as sp


W = ("p", "q", "r", "s")
U = ("x0", "x1", "x2", "y0", "y1", "y2")
ALL = W + U
POS = {v: i for i, v in enumerate(ALL)}

# Each physical pair stores sparse aggregate-matrix cells in canonical
# endpoint order: (left_color, right_color, coefficient).
EDGES: dict[tuple[str, str], list[tuple[int, int, sp.Expr]]] = defaultdict(list)


def add_cell(u: str, v: str, cu: int, cv: int, coeff: sp.Expr = sp.Integer(1)) -> None:
    if POS[u] < POS[v]:
        EDGES[(u, v)].append((cu, cv, coeff))
    else:
        EDGES[(v, u)].append((cv, cu, coeff))


def edge_cells(u: str, v: str) -> list[tuple[int, int, sp.Expr]]:
    if POS[u] < POS[v]:
        return EDGES.get((u, v), [])
    return [(cv, cu, a) for cu, cv, a in EDGES.get((v, u), [])]


def build_source() -> None:
    # The two perfect matchings of the capped four-set.
    add_cell("p", "q", 0, 0)
    add_cell("r", "s", 0, 0)
    add_cell("p", "r", 1, 1)
    add_cell("q", "s", 2, 2)

    # Canonical ternary K4 module on p,x0,x1,x2.
    for i in range(3):
        add_cell("p", f"x{i}", i, i)
    add_cell("x1", "x2", 0, 0)
    add_cell("x0", "x2", 1, 1)
    add_cell("x0", "x1", 2, 2)

    # The identical module on q,y0,y1,y2.
    for i in range(3):
        add_cell("q", f"y{i}", i, i)
    add_cell("y1", "y2", 0, 0)
    add_cell("y0", "y2", 1, 1)
    add_cell("y0", "y1", 2, 2)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[str, ...]) -> tuple[tuple[tuple[str, str], ...], ...]:
    if not vertices:
        return ((),)
    u = vertices[0]
    out = []
    for j in range(1, len(vertices)):
        v = vertices[j]
        rest = vertices[1:j] + vertices[j + 1 :]
        for tail in perfect_matchings(rest):
            out.append(((u, v),) + tail)
    return tuple(out)


def matching_tensor(vertices: tuple[str, ...]) -> dict[tuple[int, ...], sp.Expr]:
    """Enumerate the aggregate matching tensor in the supplied site order."""

    index = {v: i for i, v in enumerate(vertices)}
    out: dict[tuple[int, ...], sp.Expr] = defaultdict(lambda: sp.Integer(0))
    for matching in perfect_matchings(vertices):
        choices = [edge_cells(u, v) for u, v in matching]
        if any(not cells for cells in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(vertices)
            coeff = sp.Integer(1)
            for ((u, v), (cu, cv, a)) in zip(matching, selected):
                word[index[u]] = cu
                word[index[v]] = cv
                coeff *= a
            out[tuple(word)] += coeff
    return {w: sp.expand(a) for w, a in out.items() if a != 0}


z0, z1, z2, t = sp.symbols("z0 z1 z2 t")
Z = (z0, z1, z2)


def cap_value(word: tuple[int, int, int, int]) -> sp.Expr:
    """The four-parameter cap K_(z,t), in p,q,r,s order."""

    p, q, r, s = word
    if r == 0 and s == 0:
        if p == q:
            return Z[p]
        return sp.Integer(0)
    if word == (1, 1, 1, 1):
        return z1
    if word == (2, 2, 2, 2):
        return z2
    if word == (1, 2, 1, 2):
        return t
    return sp.Integer(0)


def contract_cap(
    tensor: dict[tuple[int, ...], sp.Expr], boundary_size: int
) -> dict[tuple[int, ...], sp.Expr]:
    out: dict[tuple[int, ...], sp.Expr] = defaultdict(lambda: sp.Integer(0))
    for word, coeff in tensor.items():
        kval = cap_value(word[:4])
        if kval:
            out[word[4 : 4 + boundary_size]] += coeff * kval
    return {w: sp.expand(a) for w, a in out.items() if sp.expand(a) != 0}


def cofactor_edge_family() -> dict[tuple[str, str], dict[tuple[int, int], sp.Expr]]:
    out = {}
    for i, u in enumerate(U):
        for v in U[i + 1 :]:
            tensor = matching_tensor(W + (u, v))
            out[(u, v)] = contract_cap(tensor, 2)
    return out


def cofactor_cells(
    family: dict[tuple[str, str], dict[tuple[int, int], sp.Expr]], u: str, v: str
) -> list[tuple[int, int, sp.Expr]]:
    if POS[u] < POS[v]:
        data = family.get((u, v), {})
        return [(cu, cv, a) for (cu, cv), a in data.items()]
    data = family.get((v, u), {})
    return [(cv, cu, a) for (cu, cv), a in data.items()]


def hafnian_of_cofactor(
    family: dict[tuple[str, str], dict[tuple[int, int], sp.Expr]]
) -> dict[tuple[int, ...], sp.Expr]:
    index = {v: i for i, v in enumerate(U)}
    out: dict[tuple[int, ...], sp.Expr] = defaultdict(lambda: sp.Integer(0))
    for matching in perfect_matchings(U):
        choices = [cofactor_cells(family, u, v) for u, v in matching]
        if any(not cells for cells in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(U)
            coeff = sp.Integer(1)
            for ((u, v), (cu, cv, a)) in zip(matching, selected):
                word[index[u]] = cu
                word[index[v]] = cv
                coeff *= a
            out[tuple(word)] += coeff
    return {
        w: sp.factor(a)
        for w, a in out.items()
        if sp.expand(a) != 0
    }


def assert_tensor_equal(
    actual: dict[tuple[int, ...], sp.Expr],
    expected: dict[tuple[int, ...], sp.Expr],
) -> None:
    keys = set(actual) | set(expected)
    bad = {
        key: sp.expand(actual.get(key, 0) - expected.get(key, 0))
        for key in keys
        if sp.expand(actual.get(key, 0) - expected.get(key, 0)) != 0
    }
    assert not bad, bad


def audit_formal_identities() -> None:
    s, x, c2, c4, c6, r = sp.symbols("s x c2 c4 c6 r")

    top = c6 + c4 * x + c2 * x**2 / 2 + s * x**3 / 6
    cofactor_hafnian = (s * x + c2) ** 3 / 6
    discrepancy = sp.expand(6 * (s**2 * top - cofactor_hafnian))
    expected = 6 * s**2 * (c6 + c4 * x) - 3 * s * c2**2 * x - c2**3
    assert sp.expand(discrepancy - expected) == 0

    pair_top = s * x**3 / 6 + r * x**2 / 2
    pair_discrepancy = sp.expand(6 * s**2 * pair_top - (s * x + r) ** 3)
    assert sp.expand(pair_discrepancy + r**2 * (3 * s * x + r)) == 0


def audit_common_edge_barrier() -> None:
    build_source()

    # The capped internal tensor has exactly the two advertised matchings.
    internal = matching_tensor(W)
    assert internal == {
        (0, 0, 0, 0): sp.Integer(1),
        (1, 2, 1, 2): sp.Integer(1),
    }
    scalar = sum(coeff * cap_value(word) for word, coeff in internal.items())
    assert sp.expand(scalar - (z0 + t)) == 0
    sform = z0 + t

    # The full source has exactly nine block-GHZ matching terms.
    full = matching_tensor(ALL)
    expected_full = {}
    for i in range(3):
        for j in range(3):
            expected_full[(i, j, 0, 0, i, i, i, j, j, j)] = sp.Integer(1)
    assert full == expected_full

    # On the four-dimensional cap slice, the complete top tensor is GHZ.
    top = contract_cap(full, 6)
    expected_top = {(i,) * 6: Z[i] for i in range(3)}
    assert_tensor_equal(top, expected_top)

    # The target forms are independent: their coefficient matrix in
    # coordinates (z0,z1,z2,t) has determinant one.
    active_matrix = sp.Matrix(
        [
            [1, 0, 0, 1],  # s=z0+t
            [1, 0, 0, 0],  # kappa_0=z0
            [0, 1, 0, 0],  # kappa_1=z1
            [0, 0, 1, 0],  # kappa_2=z2
        ]
    )
    assert abs(active_matrix.det()) == 1

    family = cofactor_edge_family()
    expected_family: dict[tuple[str, str], dict[tuple[int, int], sp.Expr]] = {}

    def put(u: str, v: str, color: int, coeff: sp.Expr) -> None:
        key = (u, v) if POS[u] < POS[v] else (v, u)
        cell = (color, color)
        expected_family.setdefault(key, {})[cell] = coeff

    put("x1", "x2", 0, sform)
    put("x0", "x2", 1, sform)
    put("x0", "x1", 2, sform)
    put("y1", "y2", 0, sform)
    put("y0", "y2", 1, sform)
    put("y0", "y1", 2, sform)
    for i in range(3):
        put(f"x{i}", f"y{i}", i, Z[i])

    for pair in family:
        assert_tensor_equal(family[pair], expected_family.get(pair, {}))

    six_hafnian = hafnian_of_cofactor(family)
    mixed = (0, 1, 2, 0, 1, 2)
    expected_six = {(i,) * 6: sp.factor(sform**2 * Z[i]) for i in range(3)}
    expected_six[mixed] = z0 * z1 * z2
    assert_tensor_equal(six_hafnian, expected_six)

    discrepancy = {}
    for word in set(top) | set(six_hafnian):
        discrepancy[word] = sp.expand(
            6 * (sform**2 * top.get(word, 0) - six_hafnian.get(word, 0))
        )
    discrepancy = {word: a for word, a in discrepancy.items() if a != 0}
    assert_tensor_equal(discrepancy, {mixed: -6 * z0 * z1 * z2})

    # The nonzero coordinate ideal is (z0*z1*z2), and the active product is
    # already in it.  Hence the first colon by h is the unit ideal.
    generator = z0 * z1 * z2
    h = sform * z0 * z1 * z2
    assert sp.rem(h, generator, z0) == 0
    assert sp.expand(h - sform * generator) == 0

    print("full ten-site supported matchings:", len(full))
    print("nonzero cofactor blocks:", sum(bool(v) for v in family.values()))
    print("six-site prism words:", len(six_hafnian))
    print("active-form determinant:", active_matrix.det())
    print("cap cubic:", discrepancy[mixed])


def main() -> None:
    audit_formal_identities()
    audit_common_edge_barrier()
    print("PASS: actual cofactor cubic and four-parameter common-edge barrier")


if __name__ == "__main__":
    main()

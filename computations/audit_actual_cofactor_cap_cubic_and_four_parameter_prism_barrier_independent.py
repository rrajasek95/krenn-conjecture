#!/usr/bin/env python3
"""Clean-room audit of the actual cofactor cap cubic and prism barrier.

This program does not import the primary checker.  Its source enumeration uses
subset dynamic programming, a small exact four-variable polynomial ring, and a
separate square-free boundary algebra.  A deliberately asymmetric two-cap
probe exercises physical endpoint order independently of the diagonal prism.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from typing import Callable, Generic, Iterable, TypeVar

import sympy as sy


EXPECTED_LEDGER_SHA256 = "2f33bfcb5be0bab24e61fcf5aeab6e97064fcb53887fe4a48c7e709470c5bd56"
VARIABLE_NAMES = ("z0", "z1", "z2", "t")
Exponent = tuple[int, int, int, int]


@dataclass(frozen=True)
class Poly4:
    """Sparse polynomial over Q in z0,z1,z2,t."""

    terms: tuple[tuple[Exponent, Fraction], ...]

    @staticmethod
    def make(data: dict[Exponent, Fraction | int]) -> "Poly4":
        clean = {
            exponent: Fraction(coefficient)
            for exponent, coefficient in data.items()
            if Fraction(coefficient) != 0
        }
        return Poly4(tuple(sorted(clean.items())))

    @staticmethod
    def constant(value: Fraction | int) -> "Poly4":
        return Poly4.make({(0, 0, 0, 0): Fraction(value)})

    @staticmethod
    def variable(index: int) -> "Poly4":
        exponent = [0, 0, 0, 0]
        exponent[index] = 1
        return Poly4.make({tuple(exponent): Fraction(1)})

    def dictionary(self) -> dict[Exponent, Fraction]:
        return dict(self.terms)

    @staticmethod
    def coerce(value: "Poly4 | Fraction | int") -> "Poly4":
        return value if isinstance(value, Poly4) else Poly4.constant(value)

    def __add__(self, other: "Poly4 | Fraction | int") -> "Poly4":
        data = self.dictionary()
        for exponent, coefficient in Poly4.coerce(other).terms:
            data[exponent] = data.get(exponent, Fraction(0)) + coefficient
        return Poly4.make(data)

    def __radd__(self, other: "Poly4 | Fraction | int") -> "Poly4":
        return self + other

    def __neg__(self) -> "Poly4":
        return Poly4.make({exponent: -coefficient for exponent, coefficient in self.terms})

    def __sub__(self, other: "Poly4 | Fraction | int") -> "Poly4":
        return self + (-Poly4.coerce(other))

    def __rsub__(self, other: "Poly4 | Fraction | int") -> "Poly4":
        return Poly4.coerce(other) - self

    def __mul__(self, other: "Poly4 | Fraction | int") -> "Poly4":
        right = Poly4.coerce(other)
        data: dict[Exponent, Fraction] = {}
        for left_exp, left_coefficient in self.terms:
            for right_exp, right_coefficient in right.terms:
                exponent = tuple(a + b for a, b in zip(left_exp, right_exp))
                data[exponent] = (
                    data.get(exponent, Fraction(0))
                    + left_coefficient * right_coefficient
                )
        return Poly4.make(data)

    def __rmul__(self, other: "Poly4 | Fraction | int") -> "Poly4":
        return self * other

    def __pow__(self, exponent: int) -> "Poly4":
        assert exponent >= 0
        out = Poly4.constant(1)
        for _ in range(exponent):
            out = out * self
        return out

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (int, Fraction)):
            return self.terms == Poly4.constant(other).terms
        if isinstance(other, Poly4):
            return self.terms == other.terms
        return False

    def evaluate(self, values: tuple[Fraction, Fraction, Fraction, Fraction]) -> Fraction:
        total = Fraction(0)
        for exponent, coefficient in self.terms:
            term = coefficient
            for value, power in zip(values, exponent):
                term *= value**power
            total += term
        return total

    def canonical(self) -> str:
        if not self.terms:
            return "0"
        pieces = []
        for exponent, coefficient in self.terms:
            monomial = "*".join(
                name if power == 1 else f"{name}^{power}"
                for name, power in zip(VARIABLE_NAMES, exponent)
                if power
            ) or "1"
            pieces.append(f"{coefficient}:{monomial}")
        return ";".join(pieces)


Z0, Z1, Z2, T = (Poly4.variable(i) for i in range(4))
Z = (Z0, Z1, Z2)


Coefficient = TypeVar("Coefficient", Fraction, Poly4)


class EdgeSource(Generic[Coefficient]):
    """Endpoint-ordered sparse aggregate edge matrices."""

    def __init__(self, vertices: tuple[str, ...]):
        self.vertices = vertices
        self.position = {vertex: index for index, vertex in enumerate(vertices)}
        self.data: dict[tuple[str, str], list[tuple[int, int, Coefficient]]] = {}

    def add(self, u: str, v: str, cu: int, cv: int, coefficient: Coefficient) -> None:
        assert u != v
        if self.position[u] < self.position[v]:
            key = (u, v)
            cell = (cu, cv, coefficient)
        else:
            key = (v, u)
            cell = (cv, cu, coefficient)
        self.data.setdefault(key, []).append(cell)

    def cells(self, u: str, v: str) -> tuple[tuple[int, int, Coefficient], ...]:
        if self.position[u] < self.position[v]:
            return tuple(self.data.get((u, v), ()))
        return tuple(
            (cv, cu, coefficient)
            for cu, cv, coefficient in self.data.get((v, u), ())
        )


def is_zero(value: Fraction | Poly4) -> bool:
    return value == 0


def subset_hafnian_tensor(
    vertices: tuple[str, ...],
    cells: Callable[[str, str], Iterable[tuple[int, int, Coefficient]]],
    zero: Coefficient,
    one: Coefficient,
) -> dict[tuple[int, ...], Coefficient]:
    """Exact matching tensor via a least-bit subset recurrence."""

    size = len(vertices)
    empty_word = (-1,) * size

    @lru_cache(maxsize=None)
    def recurse(mask: int) -> tuple[tuple[tuple[int, ...], Coefficient], ...]:
        if mask == 0:
            return ((empty_word, one),)
        first_bit = mask & -mask
        i = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        accumulated: dict[tuple[int, ...], Coefficient] = {}
        jmask = remainder
        while jmask:
            next_bit = jmask & -jmask
            j = next_bit.bit_length() - 1
            tail_mask = remainder ^ next_bit
            for cu, cv, edge_coefficient in cells(vertices[i], vertices[j]):
                for tail_word, tail_coefficient in recurse(tail_mask):
                    word = list(tail_word)
                    word[i] = cu
                    word[j] = cv
                    word_tuple = tuple(word)
                    value = tail_coefficient * edge_coefficient
                    accumulated[word_tuple] = accumulated.get(word_tuple, zero) + value
            jmask ^= next_bit
        return tuple(
            sorted(
                (word, coefficient)
                for word, coefficient in accumulated.items()
                if not is_zero(coefficient)
            )
        )

    return dict(recurse((1 << size) - 1))


def cap_contract(
    tensor: dict[tuple[int, ...], Fraction],
    cap_size: int,
    cap: Callable[[tuple[int, ...]], Coefficient],
    zero: Coefficient,
) -> dict[tuple[int, ...], Coefficient]:
    out: dict[tuple[int, ...], Coefficient] = {}
    for word, coefficient in tensor.items():
        value = coefficient * cap(word[:cap_size])
        boundary_word = word[cap_size:]
        out[boundary_word] = out.get(boundary_word, zero) + value
    return {word: coefficient for word, coefficient in out.items() if not is_zero(coefficient)}


def canonical_tensor(tensor: dict[tuple[int, ...], Fraction | Poly4]) -> list[list[str]]:
    result = []
    for word, coefficient in sorted(tensor.items()):
        value = coefficient.canonical() if isinstance(coefficient, Poly4) else str(coefficient)
        result.append(["".join(str(entry) for entry in word), value])
    return result


def assert_tensor_equal(
    left: dict[tuple[int, ...], Fraction | Poly4],
    right: dict[tuple[int, ...], Fraction | Poly4],
) -> None:
    keys = set(left) | set(right)
    residual = {
        word: left.get(word, 0) - right.get(word, 0)
        for word in keys
        if left.get(word, 0) - right.get(word, 0) != 0
    }
    assert not residual, residual


@dataclass(frozen=True)
class BoundaryTensor:
    """Six-site square-free tensor algebra over Q."""

    terms: tuple[tuple[tuple[int, ...], Fraction], ...]

    @staticmethod
    def make(data: dict[tuple[int, ...], Fraction | int]) -> "BoundaryTensor":
        clean = {
            word: Fraction(coefficient)
            for word, coefficient in data.items()
            if Fraction(coefficient) != 0
        }
        return BoundaryTensor(tuple(sorted(clean.items())))

    @staticmethod
    def zero() -> "BoundaryTensor":
        return BoundaryTensor(())

    @staticmethod
    def basis(assignments: dict[int, int], coefficient: Fraction | int = 1) -> "BoundaryTensor":
        word = [-1] * 6
        for site, colour in assignments.items():
            assert word[site] == -1
            word[site] = colour
        return BoundaryTensor.make({tuple(word): coefficient})

    def dictionary(self) -> dict[tuple[int, ...], Fraction]:
        return dict(self.terms)

    def __add__(self, other: "BoundaryTensor") -> "BoundaryTensor":
        data = self.dictionary()
        for word, coefficient in other.terms:
            data[word] = data.get(word, Fraction(0)) + coefficient
        return BoundaryTensor.make(data)

    def __neg__(self) -> "BoundaryTensor":
        return self.scale(-1)

    def __sub__(self, other: "BoundaryTensor") -> "BoundaryTensor":
        return self + (-other)

    def scale(self, scalar: Fraction | int) -> "BoundaryTensor":
        return BoundaryTensor.make(
            {word: coefficient * Fraction(scalar) for word, coefficient in self.terms}
        )

    def __mul__(self, other: "BoundaryTensor") -> "BoundaryTensor":
        out: dict[tuple[int, ...], Fraction] = {}
        for left_word, left_coefficient in self.terms:
            for right_word, right_coefficient in other.terms:
                if any(a != -1 and b != -1 for a, b in zip(left_word, right_word)):
                    continue
                word = tuple(a if a != -1 else b for a, b in zip(left_word, right_word))
                out[word] = out.get(word, Fraction(0)) + left_coefficient * right_coefficient
        return BoundaryTensor.make(out)

    def __pow__(self, exponent: int) -> "BoundaryTensor":
        assert exponent >= 1
        out = self
        for _ in range(exponent - 1):
            out = out * self
        return out

    def canonical(self) -> list[list[str]]:
        return [
            ["".join("-" if entry == -1 else str(entry) for entry in word), str(coefficient)]
            for word, coefficient in self.terms
        ]


def embed_boundary_tensor(
    tensor: dict[tuple[int, ...], Fraction], sites: tuple[int, ...]
) -> BoundaryTensor:
    out = BoundaryTensor.zero()
    for word, coefficient in tensor.items():
        out = out + BoundaryTensor.basis(dict(zip(sites, word)), coefficient)
    return out


def audit_formal_cubic() -> dict[str, object]:
    s, x, c2, c4, c6, r = sy.symbols("s x C2 C4 C6 r")
    top = c6 + c4 * x + c2 * x**2 / 2 + s * x**3 / 6
    cofactor_sum = s * x + c2
    d_source = sy.expand(6 * (s**2 * top - cofactor_sum**3 / 6))
    cumulant = sy.expand(6 * s**2 * (c6 + c4 * x) - 3 * s * c2**2 * x - c2**3)
    assert sy.expand(d_source - cumulant) == 0

    two_top = s * x**3 / 6 + r * x**2 / 2
    two_d = sy.expand(6 * (s**2 * two_top - (s * x + r) ** 3 / 6))
    two_factor = -r**2 * (3 * s * x + r)
    assert sy.expand(two_d - two_factor) == 0

    return {
        "D_source": str(sy.factor(d_source)),
        "cumulant_residual": str(sy.expand(d_source - cumulant)),
        "two_site_factor": str(sy.factor(two_d)),
        "two_site_residual": str(sy.expand(two_d - two_factor)),
    }


def build_asymmetric_two_cap_probe() -> tuple[EdgeSource[Fraction], tuple[str, ...], dict[tuple[int, int], Fraction]]:
    cap_vertices = ("p", "q")
    boundary = tuple(f"u{i}" for i in range(6))
    source: EdgeSource[Fraction] = EdgeSource(cap_vertices + boundary)

    # Both orientations occur and the cap is deliberately nonsymmetric.
    source.add("p", "q", 0, 2, Fraction(3))
    source.add("q", "p", 0, 2, Fraction(7))  # canonical cell is (2,0).
    source.add("u0", "p", 1, 0, Fraction(2))
    source.add("q", "u1", 2, 0, Fraction(3))
    source.add("p", "u2", 2, 2, Fraction(5))
    source.add("u3", "q", 1, 0, Fraction(7))
    source.add("u4", "p", 2, 1, Fraction(11))
    source.add("q", "u5", 1, 2, Fraction(13))

    for i in range(6):
        for j in range(i + 1, 6):
            source.add(
                boundary[j],
                boundary[i],
                (2 * j + i) % 3,
                (i + 2 * j + 1) % 3,
                Fraction((i + 1) * (j + 2) - 1),
            )

    cap = {
        (0, 2): Fraction(2),
        (2, 0): Fraction(-3),
        (1, 1): Fraction(5),
        (0, 0): Fraction(17),
    }
    assert source.cells("p", "u0") == ((0, 1, Fraction(2)),)
    assert source.cells("u0", "p") == ((1, 0, Fraction(2)),)
    assert source.cells("p", "q") == (
        (0, 2, Fraction(3)),
        (2, 0, Fraction(7)),
    )
    return source, boundary, cap


def audit_asymmetric_two_cap() -> dict[str, object]:
    source, boundary, cap_values = build_asymmetric_two_cap_probe()

    def cap(word: tuple[int, ...]) -> Fraction:
        assert len(word) == 2
        return cap_values.get((word[0], word[1]), Fraction(0))

    internal = subset_hafnian_tensor(("p", "q"), source.cells, Fraction(0), Fraction(1))
    scalar = sum(coefficient * cap(word) for word, coefficient in internal.items())
    assert scalar == Fraction(-15)  # 3*K(0,2)+7*K(2,0), in p,q order.

    full = subset_hafnian_tensor(("p", "q") + boundary, source.cells, Fraction(0), Fraction(1))
    top_dict = cap_contract(full, 2, cap, Fraction(0))
    top = embed_boundary_tensor(top_dict, tuple(range(6)))

    family: dict[tuple[str, str], dict[tuple[int, int], Fraction]] = {}
    for i, u in enumerate(boundary):
        for j in range(i + 1, 6):
            v = boundary[j]
            tensor = subset_hafnian_tensor(("p", "q", u, v), source.cells, Fraction(0), Fraction(1))
            family[(u, v)] = cap_contract(tensor, 2, cap, Fraction(0))

    def family_cells(u: str, v: str) -> tuple[tuple[int, int, Fraction], ...]:
        i, j = boundary.index(u), boundary.index(v)
        if i < j:
            return tuple((cu, cv, a) for (cu, cv), a in family[(u, v)].items())
        return tuple((cv, cu, a) for (cu, cv), a in family[(v, u)].items())

    cofactor_hafnian_dict = subset_hafnian_tensor(boundary, family_cells, Fraction(0), Fraction(1))
    cofactor_hafnian = embed_boundary_tensor(cofactor_hafnian_dict, tuple(range(6)))

    # x is the aggregate internal boundary quadratic.
    x = BoundaryTensor.zero()
    for i, u in enumerate(boundary):
        for j in range(i + 1, 6):
            v = boundary[j]
            for cu, cv, coefficient in source.cells(u, v):
                x = x + BoundaryTensor.basis({i: cu, j: cv}, coefficient)

    # r keeps p,q endpoint colours in that order and boundary colours at u,v.
    r = BoundaryTensor.zero()
    for i, u in enumerate(boundary):
        for p_colour, u_colour, p_coefficient in source.cells("p", u):
            for j, v in enumerate(boundary):
                for q_colour, v_colour, q_coefficient in source.cells("q", v):
                    kval = cap_values.get((p_colour, q_colour), Fraction(0))
                    if kval and i != j:
                        r = r + BoundaryTensor.basis(
                            {i: u_colour, j: v_colour},
                            p_coefficient * q_coefficient * kval,
                        )

    # These coefficients distinguish K(0,2) from K(2,0).
    r_terms = r.dictionary()
    assert r_terms[(1, 0, -1, -1, -1, -1)] == Fraction(12)
    assert r_terms[(-1, -1, 2, 1, -1, -1)] == Fraction(-105)

    expected_top = x**3
    expected_top = expected_top.scale(Fraction(scalar, 6)) + (r * (x**2)).scale(Fraction(1, 2))
    assert top == expected_top

    aggregate_cofactor = BoundaryTensor.zero()
    for i, u in enumerate(boundary):
        for j in range(i + 1, 6):
            aggregate_cofactor = aggregate_cofactor + embed_boundary_tensor(
                family[(u, boundary[j])], (i, j)
            )
    assert aggregate_cofactor == x.scale(scalar) + r

    d_actual = top.scale(6 * scalar**2) - cofactor_hafnian.scale(6)
    d_factor = (r**2 * (x.scale(3 * scalar) + r)).scale(-1)
    assert d_actual == d_factor

    return {
        "s": str(scalar),
        "r_term_count": len(r.terms),
        "ordered_K_02_coefficient": "12",
        "ordered_K_20_coefficient": "-105",
        "top_term_count": len(top.terms),
        "D_term_count": len(d_actual.terms),
        "D_factor_residual": [],
    }


W = ("p", "q", "r", "s")
U = ("x0", "x1", "x2", "y0", "y1", "y2")
ALL = W + U


def build_prism_source() -> EdgeSource[Fraction]:
    source: EdgeSource[Fraction] = EdgeSource(ALL)
    source.add("p", "q", 0, 0, Fraction(1))
    source.add("s", "r", 0, 0, Fraction(1))
    source.add("p", "r", 1, 1, Fraction(1))
    source.add("s", "q", 2, 2, Fraction(1))

    for i in range(3):
        source.add("p", f"x{i}", i, i, Fraction(1))
    source.add("x2", "x1", 0, 0, Fraction(1))
    source.add("x0", "x2", 1, 1, Fraction(1))
    source.add("x1", "x0", 2, 2, Fraction(1))

    # Insert the second module mostly in reverse physical endpoint order.
    for i in range(3):
        source.add(f"y{i}", "q", i, i, Fraction(1))
    source.add("y2", "y1", 0, 0, Fraction(1))
    source.add("y0", "y2", 1, 1, Fraction(1))
    source.add("y1", "y0", 2, 2, Fraction(1))
    return source


def prism_cap(word: tuple[int, ...]) -> Poly4:
    assert len(word) == 4
    p, q, r, s = word
    if r == 0 and s == 0:
        return Z[p] if p == q else Poly4.constant(0)
    if word == (1, 1, 1, 1):
        return Z1
    if word == (2, 2, 2, 2):
        return Z2
    if word == (1, 2, 1, 2):
        return T
    return Poly4.constant(0)


def audit_prism_barrier() -> dict[str, object]:
    source = build_prism_source()
    internal = subset_hafnian_tensor(W, source.cells, Fraction(0), Fraction(1))
    expected_internal = {
        (0, 0, 0, 0): Fraction(1),
        (1, 2, 1, 2): Fraction(1),
    }
    assert_tensor_equal(internal, expected_internal)
    scalar = sum(coefficient * prism_cap(word) for word, coefficient in internal.items())
    assert scalar == Z0 + T

    full = subset_hafnian_tensor(ALL, source.cells, Fraction(0), Fraction(1))
    expected_full = {
        (i, j, 0, 0, i, i, i, j, j, j): Fraction(1)
        for i in range(3)
        for j in range(3)
    }
    assert_tensor_equal(full, expected_full)

    top = cap_contract(full, 4, prism_cap, Poly4.constant(0))
    expected_top = {(i,) * 6: Z[i] for i in range(3)}
    assert_tensor_equal(top, expected_top)

    # Build the actual 81-by-4 coordinate matrix of the cap slice.
    unit_exponents = []
    for variable in range(4):
        exponent = [0, 0, 0, 0]
        exponent[variable] = 1
        unit_exponents.append(tuple(exponent))
    cap_rows = []
    for word in product(range(3), repeat=4):
        polynomial = prism_cap(word)
        assert all(sum(exponent) == 1 for exponent, _ in polynomial.terms)
        data = polynomial.dictionary()
        cap_rows.append([data.get(exponent, Fraction(0)) for exponent in unit_exponents])
    cap_coordinate_matrix = sy.Matrix(cap_rows)
    assert cap_coordinate_matrix.rank() == 4
    active_matrix = sy.Matrix(
        [
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
        ]
    )
    assert active_matrix.det() == -1

    family: dict[tuple[str, str], dict[tuple[int, int], Poly4]] = {}
    for i, u in enumerate(U):
        for v in U[i + 1 :]:
            tensor = subset_hafnian_tensor(W + (u, v), source.cells, Fraction(0), Fraction(1))
            family[(u, v)] = cap_contract(tensor, 4, prism_cap, Poly4.constant(0))

    expected_family: dict[tuple[str, str], dict[tuple[int, int], Poly4]] = {}

    def put(u: str, v: str, colour: int, coefficient: Poly4) -> None:
        expected_family[(u, v)] = {(colour, colour): coefficient}

    sform = Z0 + T
    put("x0", "x1", 2, sform)
    put("x0", "x2", 1, sform)
    put("x1", "x2", 0, sform)
    put("y0", "y1", 2, sform)
    put("y0", "y2", 1, sform)
    put("y1", "y2", 0, sform)
    for i in range(3):
        put(f"x{i}", f"y{i}", i, Z[i])

    for pair, tensor in family.items():
        assert_tensor_equal(tensor, expected_family.get(pair, {}))

    u_position = {vertex: index for index, vertex in enumerate(U)}

    def family_cells(u: str, v: str) -> tuple[tuple[int, int, Poly4], ...]:
        if u_position[u] < u_position[v]:
            return tuple((cu, cv, a) for (cu, cv), a in family[(u, v)].items())
        return tuple((cv, cu, a) for (cu, cv), a in family[(v, u)].items())

    cofactor_hafnian = subset_hafnian_tensor(
        U, family_cells, Poly4.constant(0), Poly4.constant(1)
    )
    mixed_word = (0, 1, 2, 0, 1, 2)
    expected_hafnian = {(i,) * 6: sform**2 * Z[i] for i in range(3)}
    generator = Z0 * Z1 * Z2
    expected_hafnian[mixed_word] = generator
    assert_tensor_equal(cofactor_hafnian, expected_hafnian)

    discrepancy = {
        word: 6 * (sform**2 * top.get(word, Poly4.constant(0)) - coefficient)
        for word, coefficient in cofactor_hafnian.items()
    }
    for word, coefficient in top.items():
        discrepancy.setdefault(word, 6 * sform**2 * coefficient)
    discrepancy = {word: coefficient for word, coefficient in discrepancy.items() if coefficient != 0}
    assert_tensor_equal(discrepancy, {mixed_word: -6 * generator})

    h = sform * generator
    assert h == sform * generator
    assert h.evaluate((Fraction(1), Fraction(1), Fraction(1), Fraction(0))) == 1
    assert generator.evaluate((Fraction(1), Fraction(1), Fraction(1), Fraction(0))) == 1

    # Exact saturation certificate: h is itself in I=(generator), so
    # 1*h belongs to I and I:h is already the unit ideal.  The independent
    # Groebner elimination check gives the same Rabinowitsch certificate.
    z0, z1, z2, tt, aux = sy.symbols("z0 z1 z2 t aux")
    g_sy = z0 * z1 * z2
    h_sy = (z0 + tt) * g_sy
    basis = sy.groebner([g_sy, 1 - aux * h_sy], aux, z0, z1, z2, tt, order="lex")
    assert list(basis) == [sy.Integer(1)]

    # Scope guard: the actual ten-site tensor is not Delta_10.  It contains
    # eight mixed block words, only one global pure word, and misses X1,X2.
    global_target = {(i,) * 10: Fraction(1) for i in range(3)}
    assert full != global_target
    actual_global_pure = [word for word in full if len(set(word)) == 1]
    actual_global_mixed = [word for word in full if len(set(word)) > 1]
    missing_target = [word for word in global_target if word not in full]
    assert len(actual_global_pure) == 1
    assert len(actual_global_mixed) == 8
    assert len(missing_target) == 2

    return {
        "internal_W": canonical_tensor(internal),
        "s": scalar.canonical(),
        "top": canonical_tensor(top),
        "cap_map_rank": int(cap_coordinate_matrix.rank()),
        "active_form_determinant": int(active_matrix.det()),
        "nonzero_cofactor_blocks": sum(bool(tensor) for tensor in family.values()),
        "cofactor_hafnian": canonical_tensor(cofactor_hafnian),
        "D": canonical_tensor(discrepancy),
        "coordinate_ideal_generator": generator.canonical(),
        "h": h.canonical(),
        "saturation_basis": [str(item) for item in basis],
        "active_test": [1, 1, 1, 0],
        "global_source": {
            "supported_words": len(full),
            "pure_words": len(actual_global_pure),
            "mixed_words": len(actual_global_mixed),
            "missing_target_words": len(missing_target),
            "is_global_GHZ": False,
        },
    }


def audit_universal_radical_exponents() -> dict[str, object]:
    s, k0, k1, k2 = sy.symbols("s k0 k1 k2")
    product = k0 * k1 * k2
    h = s * product
    residuals = []
    for exponent in range(1, 7):
        radical_pullback = (s**6 * product) ** exponent
        multiplier = product ** (5 * exponent)
        residual = sy.expand(radical_pullback * multiplier - h ** (6 * exponent))
        assert residual == 0
        residuals.append(str(residual))
    return {
        "tested_N": list(range(1, 7)),
        "h_power": "h^(6N)",
        "residuals": residuals,
    }


def main() -> None:
    ledger = {
        "formal": audit_formal_cubic(),
        "asymmetric_two_cap": audit_asymmetric_two_cap(),
        "prism": audit_prism_barrier(),
        "universal_radical": audit_universal_radical_exponents(),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    print("independent semantic ledger SHA-256:", digest)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        assert digest == EXPECTED_LEDGER_SHA256, (digest, EXPECTED_LEDGER_SHA256)
    print("two-cap ordered scalar:", ledger["asymmetric_two_cap"]["s"])
    print("ten-site supported/mixed words:", ledger["prism"]["global_source"]["supported_words"], ledger["prism"]["global_source"]["mixed_words"])
    print("active-form determinant:", ledger["prism"]["active_form_determinant"])
    print("cap cubic:", ledger["prism"]["D"])
    print("PASS: independent actual-cofactor prism-barrier audit")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""UNAUDITED STRESS-TEST library.  Independent reimplementation.

Nothing here imports the repository checkers: every combinatorial object
(perfect matchings, two-switch adjacency, occurrences, insertion charts)
is rebuilt from the written definitions in

  notes/uniform-centered-occurrence-matching-eigenspace-correction.md
  notes/uniform-centered-occurrence-endpoint-association-projector.md
  notes/2026-08-13-three-interface-proof-frontier.md

so that agreement with the committed checkers is evidence, not tautology.
All arithmetic is exact (int / fractions.Fraction).
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations


# ----------------------------------------------------------------- matchings

def edge(a: int, b: int) -> tuple[int, int]:
    assert a != b
    return (a, b) if a < b else (b, a)


def perfect_matchings(vertices):
    """All perfect matchings of the given vertex tuple, as sorted edge tuples."""
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


def double_factorial_odd(n: int) -> int:
    answer = 1
    while n > 0:
        answer *= n
        n -= 2
    return answer


def mate_map(matching):
    partner = {}
    for a, b in matching:
        partner[a] = b
        partner[b] = a
    return partner


def coset_type(left, right) -> tuple[int, ...]:
    """Union cycle type of two perfect matchings, as a partition of h.

    The union of two perfect matchings is a disjoint union of even cycles
    (a shared edge counting as a 2-cycle).  Halving the cycle lengths gives
    the classical coset type / association-scheme relation label.
    """
    a = mate_map(left)
    b = mate_map(right)
    seen = set()
    parts = []
    for start in a:
        if start in seen:
            continue
        length = 0
        node = start
        use_a = True
        while True:
            seen.add(node)
            node = a[node] if use_a else b[node]
            length += 1
            use_a = not use_a
            if node == start and use_a:
                break
        assert length % 2 == 0
        parts.append(length // 2)
    return tuple(sorted(parts, reverse=True))


def switch_neighbors(matching):
    """Two-switch neighbours: replace ab|cd by ac|bd or ad|bc.

    Degree h(h-1) = 2*C(h,2).
    """
    matching = tuple(matching)
    answer = []
    for i, j in combinations(range(len(matching)), 2):
        a, b = matching[i]
        c, d = matching[j]
        rest = tuple(v for k, v in enumerate(matching) if k not in (i, j))
        answer.append(tuple(sorted(rest + (edge(a, c), edge(b, d)))))
        answer.append(tuple(sorted(rest + (edge(a, d), edge(b, c)))))
    assert len(answer) == len(set(answer)) == len(matching) * (len(matching) - 1)
    return tuple(answer)


class MatchingSpace:
    """C[PM(K_2h)] with the two-switch adjacency A_h."""

    def __init__(self, h: int, vertices=None):
        self.h = h
        self.vertices = tuple(range(2 * h)) if vertices is None else tuple(vertices)
        assert len(self.vertices) == 2 * h
        self.points = tuple(perfect_matchings(self.vertices))
        assert len(self.points) == double_factorial_odd(2 * h - 1)
        self.index = {m: i for i, m in enumerate(self.points)}
        self.adjacency = tuple(
            tuple(self.index[n] for n in switch_neighbors(m)) for m in self.points
        )

    def apply_A(self, vector):
        return tuple(sum(vector[j] for j in row) for row in self.adjacency)

    def constant(self, value=1):
        return tuple(Q(value) for _ in self.points)

    def edge_indicator(self, e):
        e = edge(*e)
        return tuple(Q(int(e in m)) for m in self.points)

    def partial_matching_indicator(self, partial):
        partial = frozenset(edge(*e) for e in partial)
        return tuple(Q(int(partial <= frozenset(m))) for m in self.points)


# --------------------------------------------------- exact linear algebra

def row_reduce(vectors):
    """Return (rank, pivot basis dict) for a list of exact vectors."""
    basis = {}
    for original in vectors:
        values = [Q(v) for v in original]
        for pivot in sorted(basis):
            if values[pivot]:
                c = values[pivot]
                values = [x - c * y for x, y in zip(values, basis[pivot], strict=True)]
        pivot = next((i for i, v in enumerate(values) if v), None)
        if pivot is None:
            continue
        c = values[pivot]
        basis[pivot] = tuple(v / c for v in values)
    return len(basis), basis


def rank(vectors):
    return row_reduce(vectors)[0]


def minimal_polynomial_on_vector(apply_op, vector, max_degree=40):
    """Monic minimal polynomial of `apply_op` on the cyclic span of `vector`.

    Returns the coefficient list [c0,...,c_{d-1},1] of  x^d + ... + c0.
    Exact: found as the first linear dependency among Krylov vectors.
    """
    vector = tuple(Q(v) for v in vector)
    krylov = [vector]
    # reduced basis with the expressing coefficients in terms of krylov index
    basis = {}          # pivot -> (reduced vector, coefficient vector)
    def reduce_vector(vec, coeffs):
        vec = list(vec)
        coeffs = list(coeffs)
        for pivot in sorted(basis):
            if vec[pivot]:
                c = vec[pivot]
                bvec, bco = basis[pivot]
                vec = [x - c * y for x, y in zip(vec, bvec, strict=True)]
                coeffs = [x - c * y for x, y in
                          zip(coeffs, bco + [Q(0)] * (len(coeffs) - len(bco)),
                              strict=True)]
        return vec, coeffs

    current = vector
    for degree in range(max_degree + 1):
        coeffs = [Q(0)] * (degree + 1)
        coeffs[degree] = Q(1)
        reduced, rcoeffs = reduce_vector(current, coeffs)
        pivot = next((i for i, v in enumerate(reduced) if v), None)
        if pivot is None:
            # dependency: rcoeffs expresses 0 = sum rcoeffs[i] A^i v, monic in degree
            lead = rcoeffs[degree]
            assert lead
            return [c / lead for c in rcoeffs]
        c = reduced[pivot]
        basis[pivot] = ([v / c for v in reduced], [v / c for v in rcoeffs])
        current = tuple(apply_op(current))
        krylov.append(current)
    raise RuntimeError("minimal polynomial degree exceeded bound")


def poly_eval(coeffs, x):
    answer = Q(0)
    for c in reversed(coeffs):
        answer = answer * x + c
    return answer


def integer_roots_from_candidates(coeffs, candidates):
    return sorted({c for c in candidates if poly_eval(coeffs, Q(c)) == 0})


def fit_polynomial(points):
    """Exact Lagrange interpolation.  points = [(x, y), ...] -> coefficient list."""
    n = len(points)
    coeffs = [Q(0)] * n
    for i, (xi, yi) in enumerate(points):
        denom = Q(1)
        for j, (xj, _) in enumerate(points):
            if i == j:
                continue
            denom *= (Q(xi) - Q(xj))
        num = [Q(1)]
        for j, (xj, _) in enumerate(points):
            if i == j:
                continue
            new = [Q(0)] * (len(num) + 1)
            for k, c in enumerate(num):
                new[k + 1] += c
                new[k] += -Q(xj) * c
            num = new
        scale = Q(yi) / denom
        for k, c in enumerate(num):
            coeffs[k] += scale * c
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()
    return coeffs


def difference_table(values):
    """Successive differences; returns list of rows."""
    rows = [list(values)]
    while len(rows[-1]) > 1:
        prev = rows[-1]
        rows.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])
    return rows


def poly_str(coeffs, var="h"):
    terms = []
    for k in range(len(coeffs) - 1, -1, -1):
        c = coeffs[k]
        if c == 0:
            continue
        if k == 0:
            terms.append(f"{c}")
        elif k == 1:
            terms.append(f"{c}*{var}")
        else:
            terms.append(f"{c}*{var}^{k}")
    return " + ".join(terms) if terms else "0"


# ------------------------------------------------- Young / dimension helpers

def partitions(n, largest=None):
    if largest is None:
        largest = n
    if n == 0:
        yield ()
        return
    for first in range(min(n, largest), 0, -1):
        for tail in partitions(n - first, first):
            yield (first,) + tail


def hook_dimension(shape) -> int:
    """Number of standard Young tableaux of `shape` (hook length formula)."""
    shape = tuple(shape)
    n = sum(shape)
    conj = [sum(1 for row in shape if row > c) for c in range(shape[0])]
    numerator = 1
    for k in range(1, n + 1):
        numerator *= k
    denominator = 1
    for i, row in enumerate(shape):
        for j in range(row):
            denominator *= (row - j) + (conj[j] - i) - 1
    assert numerator % denominator == 0
    return numerator // denominator


def double_shape(lam):
    return tuple(2 * p for p in lam)


# ---------------------------------------------------------- occurrence space

def occurrences(vertices):
    vertices = tuple(vertices)
    answer = []
    for p in vertices:
        for s in vertices:
            if p == s:
                continue
            rest = tuple(v for v in vertices if v not in (p, s))
            for m in perfect_matchings(rest):
                answer.append((p, s, m))
    return tuple(answer)


def occurrence_count(h: int) -> int:
    return 2 * h * (2 * h - 1) * double_factorial_odd(2 * h - 3)


def endpoint_neighbors(occ, vertices):
    """B_h: move exactly one ordered endpoint through one residual edge."""
    p, s, matching = occ
    partner = mate_map(matching)
    answer = []
    for t in vertices:
        if t in (p, s):
            continue
        u = partner[t]
        rest = tuple(e for e in matching if t not in e)
        answer.append((t, s, tuple(sorted(rest + (edge(p, u),)))))
        answer.append((p, t, tuple(sorted(rest + (edge(s, u),)))))
    assert len(answer) == len(set(answer)) == 4 * len(matching)
    return tuple(answer)


def charts(sites):
    """All insertion charts: the new pair in every role."""
    answer = []
    for a, b in combinations(sites, 2):
        pair = (a, b)
        answer.append((pair, "residual", a, b))
        answer.append((pair, "p", a, b))
        answer.append((pair, "p", b, a))
        answer.append((pair, "s", a, b))
        answer.append((pair, "s", b, a))
        answer.append((pair, "both", a, b))
        answer.append((pair, "both", b, a))
    return tuple(answer)


def extend(occ, chart):
    p, s, matching = occ
    _pair, kind, new, bridge = chart
    if kind == "residual":
        return (p, s, tuple(sorted(matching + (edge(new, bridge),))))
    if kind == "p":
        return (new, s, tuple(sorted(matching + (edge(bridge, p),))))
    if kind == "s":
        return (p, new, tuple(sorted(matching + (edge(bridge, s),))))
    assert kind == "both"
    return (new, bridge, tuple(sorted(matching + (edge(p, s),))))


def marked_occurrence(h: int):
    """Marked occurrence of order h+1 on sites 0..2h+1."""
    return (0, 1, tuple((2 * i, 2 * i + 1) for i in range(1, h + 1)))

"""Exact primitives for the U7H (minimal pure-cofactor matching-covered core) audit.

UNAUDITED EXTERNAL IMPORT AUDIT.  Nothing here is a repository claim.

All arithmetic is exact: weights are elements of Q or of Q(i) (see `GQ`).
No floating point anywhere.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from typing import Dict, Iterable, List, Sequence, Set, Tuple

Edge = Tuple[int, int]
Matching = Tuple[Edge, ...]


class GQ:
    """Exact Gaussian rational a + b*i with Fraction components."""

    __slots__ = ("re", "im")

    def __init__(self, re=0, im=0):
        self.re = Fraction(re)
        self.im = Fraction(im)

    def __add__(self, other):
        other = _gq(other)
        return GQ(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return GQ(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-_gq(other))

    def __rsub__(self, other):
        return _gq(other) + (-self)

    def __mul__(self, other):
        other = _gq(other)
        return GQ(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = _gq(other)
        norm = other.re * other.re + other.im * other.im
        if norm == 0:
            raise ZeroDivisionError("GQ division by zero")
        return GQ(
            (self.re * other.re + self.im * other.im) / norm,
            (self.im * other.re - self.re * other.im) / norm,
        )

    def __eq__(self, other):
        other = _gq(other)
        return self.re == other.re and self.im == other.im

    def __hash__(self):
        return hash((self.re, self.im))

    def __bool__(self):
        return self.re != 0 or self.im != 0

    def __repr__(self):
        if self.im == 0:
            return str(self.re)
        return f"({self.re}{'+' if self.im > 0 else '-'}{abs(self.im)}i)"


def _gq(value) -> GQ:
    if isinstance(value, GQ):
        return value
    return GQ(value, 0)


ZERO = GQ(0)
ONE = GQ(1)


def edge(a: int, b: int) -> Edge:
    return (a, b) if a < b else (b, a)


# --------------------------------------------------------------------------
# perfect matchings / hafnians
# --------------------------------------------------------------------------


def perfect_matchings(vertices: Sequence[int]) -> List[Matching]:
    """All perfect matchings of the complete graph on `vertices`."""
    vertices = tuple(vertices)
    if not vertices:
        return [()]
    head = vertices[0]
    out: List[Matching] = []
    for k in range(1, len(vertices)):
        rest = vertices[1:k] + vertices[k + 1 :]
        for sub in perfect_matchings(rest):
            out.append((edge(head, vertices[k]),) + sub)
    return out


def supported_matchings(vertices: Sequence[int], w: Dict[Edge, GQ]) -> List[Matching]:
    """Perfect matchings all of whose edges carry a nonzero weight."""
    return [m for m in perfect_matchings(vertices) if all(w.get(e) for e in m)]


def matching_weight(m: Matching, w: Dict[Edge, GQ]) -> GQ:
    acc = ONE
    for e in m:
        acc = acc * w.get(e, ZERO)
    return acc


def hafnian(vertices: Sequence[int], w: Dict[Edge, GQ]) -> GQ:
    """Exact hafnian of the principal submatrix on `vertices` (sum over matchings)."""
    acc = ZERO
    for m in supported_matchings(vertices, w):
        acc = acc + matching_weight(m, w)
    return acc


# --------------------------------------------------------------------------
# the objects of the external claim
# --------------------------------------------------------------------------


def least_cancellation(vertices: Sequence[int], w: Dict[Edge, GQ]):
    """Least-cardinality even R with h(R)=0 and support(Z[R]) having a PM.

    Returns None when no such R exists.  This is the external claim's
    minimality quantifier: over *vertex subsets*, not over cell supports.
    """
    vertices = tuple(sorted(vertices))
    for size in range(2, len(vertices) + 1, 2):
        for subset in combinations(vertices, size):
            if supported_matchings(subset, w) and not hafnian(subset, w):
                return subset
    return None


def all_least_cancellations(vertices: Sequence[int], w: Dict[Edge, GQ]):
    """Every minimiser, not just the lexicographically first."""
    vertices = tuple(sorted(vertices))
    for size in range(2, len(vertices) + 1, 2):
        hits = [
            s
            for s in combinations(vertices, size)
            if supported_matchings(s, w) and not hafnian(s, w)
        ]
        if hits:
            return hits
    return []


def active_cofactor_graph(vertices: Sequence[int], w: Dict[Edge, GQ]) -> Set[Edge]:
    """A_R = { ij : C_ij = z_ij * h(R - {i,j}) != 0 }."""
    out: Set[Edge] = set()
    for a, b in combinations(sorted(vertices), 2):
        z = w.get((a, b), ZERO)
        if not z:
            continue
        rest = tuple(v for v in vertices if v != a and v != b)
        if z * hafnian(rest, w):
            out.add((a, b))
    return out


def allowed_edge_graph(vertices: Sequence[int], w: Dict[Edge, GQ]) -> Set[Edge]:
    """Allow(G_R) = union of all support perfect matchings of G_R."""
    return {e for m in supported_matchings(vertices, w) for e in m}


def support_graph(vertices: Sequence[int], w: Dict[Edge, GQ]) -> Set[Edge]:
    return {
        (a, b) for a, b in combinations(sorted(vertices), 2) if w.get((a, b), ZERO)
    }


def components(vertices: Sequence[int], edges: Iterable[Edge]):
    adj: Dict[int, Set[int]] = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    unseen = set(vertices)
    out = []
    while unseen:
        start = min(unseen)
        seen = {start}
        stack = [start]
        while stack:
            cur = stack.pop()
            for nb in adj[cur]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        unseen -= seen
        out.append(tuple(sorted(seen)))
    return tuple(out)


def degrees(vertices: Sequence[int], edges: Iterable[Edge]) -> Dict[int, int]:
    d = {v: 0 for v in vertices}
    for a, b in edges:
        d[a] += 1
        d[b] += 1
    return d


def is_connected(vertices: Sequence[int], edges: Iterable[Edge]) -> bool:
    return len(components(vertices, edges)) == 1


def is_matching_covered(vertices: Sequence[int], edges: Set[Edge]) -> bool:
    """Lovasz-Plummer: connected, at least one edge, every edge in some PM.

    Perfect matchings are computed *inside the given edge set* only.
    """
    vertices = tuple(sorted(vertices))
    if len(vertices) < 2 or not edges:
        return False
    if not is_connected(vertices, edges):
        return False
    unit = {e: ONE for e in edges}
    covered: Set[Edge] = set()
    for m in supported_matchings(vertices, unit):
        covered.update(m)
    return covered == set(edges)


def alternating_cycle_witness(
    vertices: Sequence[int], edges: Set[Edge], reference: Matching
) -> Dict[Edge, Tuple[Edge, ...]]:
    """For each edge, a P-alternating even cycle inside `edges` containing it.

    Raises AssertionError if some edge admits none.
    """
    unit = {e: ONE for e in edges}
    matchings = supported_matchings(tuple(sorted(vertices)), unit)
    ref = set(reference)
    out: Dict[Edge, Tuple[Edge, ...]] = {}
    for e in edges:
        found = None
        for q in matchings:
            diff = ref ^ set(q)
            if e not in diff:
                continue
            adj: Dict[int, List[Edge]] = {}
            for f in diff:
                adj.setdefault(f[0], []).append(f)
                adj.setdefault(f[1], []).append(f)
            assert all(len(v) == 2 for v in adj.values())
            sel: Set[Edge] = set()
            stack = [e]
            while stack:
                f = stack.pop()
                if f in sel:
                    continue
                sel.add(f)
                for v in f:
                    stack.extend(g for g in adj[v] if g not in sel)
            assert len(sel) % 2 == 0 and len(sel) >= 4
            found = tuple(sorted(sel))
            break
        assert found is not None, f"no alternating cycle for {e}"
        out[e] = found
    return out


def cyclomatic_rank(vertices: Sequence[int], edges: Set[Edge]) -> int:
    return len(edges) - len(vertices) + 1


# --------------------------------------------------------------------------
# our model: bicoloured cells a_uv(i,j) on N vertices, palette size d
# --------------------------------------------------------------------------

Cell = Tuple[int, int, int, int]  # (u, v, i, j) with u < v


def fibre_weights(cells: Dict[Cell, GQ], chi: Sequence[int], n: int) -> Dict[Edge, GQ]:
    """Weight matrix W^chi_uv = a_uv(chi_u, chi_v) of one colouring fibre."""
    w: Dict[Edge, GQ] = {}
    for u, v in combinations(range(n), 2):
        val = cells.get((u, v, chi[u], chi[v]))
        if val:
            w[(u, v)] = val
    return w


def fibre_coefficient(cells: Dict[Cell, GQ], chi: Sequence[int], n: int) -> GQ:
    return hafnian(tuple(range(n)), fibre_weights(cells, chi, n))

#!/usr/bin/env python3
"""UNAUDITED PROBE (W2) -- the coordinate/monomial regime kill engine.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01
Plan: notes/2026-08-15-resolution-master-plan.md, lemma J.2.
Nothing here is a proved claim.  Exact integer/rational arithmetic only.

SETTING (the regime).  N named sites, V_v = C^3.  A *coordinate template*
assigns to every unordered pair uv either ABSENT or one ordered colour label
(a, b), meaning

    A_uv = w_uv * e_a^{(u)} (x) e_b^{(v)},     w_uv in C^*.

Then every supported perfect matching M induces exactly one vertex colouring
c(M), and

    H_N(A)_c = sum over { M : M supported, c(M) = c } of  prod_{uv in M} w_uv,

a sum of DISTINCT Laurent monomials with all coefficients +1.  Exactness asks

    (mixed)     sum over fibre(c) = 0            for every non-constant c,
    (constant)  sum over fibre(r,...,r) != 0     for r = 0,1,2

(the three constant values need only be nonzero: the local diagonal gauge
e_c^{(v)} -> mu_c e_c^{(v)} at every vertex rescales them independently and
keeps the template coordinate; cf. proofs/six-site-arbitrary-complex-
obstruction.md section 2).

THE COMMITTED KILL MECHANISMS, in the exact form used downstream:

  (K0) missing constant   some constant fibre is EMPTY            -> 0 != 1.
  (O2) singleton class    a mixed fibre whose live terms occupy ONE class of
                          the character quotient Z^E / L has a nonzero
                          monomial value.  The classical *singleton mixed
                          fibre* (|fibre| = 1) is the case L = 0.
  (O1) odd holonomy       an integer dependency among the derived relations
                          on which the prescribed character is nontrivial
                          (the "1 = -1" certificate).
  (K3) pure vanishing     a constant fibre all of whose classes cancel.

This module implements the *closure* of these: binomial (and, recursively,
two-class) mixed fibres generate relations  x^d = gamma  with gamma in Q^*;
the character is tested for consistency by an exact integer kernel and an
exact factorisation of the gammas inside Q^* = {+-1} x (+)_p Z.  This is
literally the procedure of proofs/six-site-arbitrary-complex-obstruction.md
section 5.2 ("terms are grouped modulo this lattice and their exact signed
multiplicities are computed; a unique nonzero signed class is impossible in
characteristic zero") lifted from -1 characters to Q^* characters.

SOUNDNESS.  Every verdict != "survivor" is a proof that the template admits
no nonzero complex weighting.  "survivor" means only that this closure did
not refute it.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from typing import Iterable

Q = 3
ABSENT = None


# ------------------------------------------------------------- combinatorics


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for matching in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + matching))


def edge_list(size: int):
    return tuple(combinations(range(size), 2))


class Geometry:
    """Fixed combinatorial data of K_size: edges, matchings, incidences."""

    def __init__(self, size: int):
        self.size = size
        self.edges = edge_list(size)
        self.index = {edge: n for n, edge in enumerate(self.edges)}
        self.matchings = tuple(perfect_matchings(tuple(range(size))))
        self.matching_edges = tuple(
            tuple(self.index[edge] for edge in matching)
            for matching in self.matchings)

    def exponent(self, number: int):
        row = [0] * len(self.edges)
        for e in self.matching_edges[number]:
            row[e] += 1
        return tuple(row)


GEOMETRY: dict[int, Geometry] = {}


def geometry(size: int) -> Geometry:
    if size not in GEOMETRY:
        GEOMETRY[size] = Geometry(size)
    return GEOMETRY[size]


def fibres(geo: Geometry, labels):
    """labels[e] is None or (a, b) with a the colour at edges[e][0].

    Returns {colouring: [matching numbers]}.
    """
    out: dict[tuple[int, ...], list[int]] = {}
    for number, matching in enumerate(geo.matchings):
        colouring = [-1] * geo.size
        ok = True
        for u, v in matching:
            label = labels[geo.index[(u, v)]]
            if label is None:
                ok = False
                break
            colouring[u], colouring[v] = label
        if ok:
            out.setdefault(tuple(colouring), []).append(number)
    return out


def is_mixed(colouring) -> bool:
    return len(set(colouring)) > 1


def support_size(labels) -> int:
    return sum(1 for label in labels if label is not None)


# --------------------------------------------------------- Q^* as a Z-module


def factor_rational(value: Fraction):
    """Q^* -> {0,1} x (finite exponent dict).  Exact, small numbers only."""
    sign = 0
    numerator, denominator = value.numerator, value.denominator
    if numerator < 0:
        sign = 1
        numerator = -numerator
    if numerator == 0:
        raise ValueError("zero is not in Q^*")
    exponents: dict[int, int] = {}
    for base, direction in ((numerator, 1), (denominator, -1)):
        n = base
        divisor = 2
        while divisor * divisor <= n:
            while n % divisor == 0:
                exponents[divisor] = exponents.get(divisor, 0) + direction
                n //= divisor
            divisor += 1 if divisor == 2 else 2
        if n > 1:
            exponents[n] = exponents.get(n, 0) + direction
    return sign, {p: e for p, e in exponents.items() if e}


# ------------------------------------------------------- integer row lattice


def hermite_with_transform(rows: list[list[int]]):
    """Return (H, U) with U unimodular and U * rows = H in row echelon form.

    H's nonzero rows come first.  Pure Python integers; no dependencies.
    """
    m = len(rows)
    n = len(rows[0]) if m else 0
    H = [list(row) for row in rows]
    U = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    pivot_row = 0
    pivots: list[int] = []
    for column in range(n):
        target = None
        for r in range(pivot_row, m):
            if H[r][column] != 0:
                target = r
                break
        if target is None:
            continue
        H[pivot_row], H[target] = H[target], H[pivot_row]
        U[pivot_row], U[target] = U[target], U[pivot_row]
        # Euclidean elimination below the pivot.
        for r in range(pivot_row + 1, m):
            while H[r][column] != 0:
                a, b = H[pivot_row][column], H[r][column]
                if abs(b) >= abs(a):
                    factor = b // a
                    for c in range(n):
                        H[r][c] -= factor * H[pivot_row][c]
                    for c in range(m):
                        U[r][c] -= factor * U[pivot_row][c]
                else:
                    H[pivot_row], H[r] = H[r], H[pivot_row]
                    U[pivot_row], U[r] = U[r], U[pivot_row]
        if H[pivot_row][column] < 0:
            H[pivot_row] = [-x for x in H[pivot_row]]
            U[pivot_row] = [-x for x in U[pivot_row]]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == m:
            break
    return H, U, pivots, pivot_row


class Character:
    """Relations x^{d_j} = gamma_j and the exact consistency/closure tests."""

    def __init__(self, width: int):
        self.width = width
        self.rows: list[list[int]] = []
        self.gammas: list[Fraction] = []
        self._dirty = True
        self._H: list[list[int]] = []
        self._U: list[list[int]] = []
        self._pivots: list[int] = []
        self._rank = 0

    def add(self, row: Iterable[int], gamma: Fraction) -> None:
        self.rows.append(list(row))
        self.gammas.append(Fraction(gamma))
        self._dirty = True

    def _refresh(self) -> None:
        if not self._dirty:
            return
        if not self.rows:
            self._H, self._U, self._pivots, self._rank = [], [], [], 0
        else:
            self._H, self._U, self._pivots, self._rank = hermite_with_transform(
                self.rows)
        self._dirty = False

    # -- (O1) ---------------------------------------------------------------
    def odd_relation(self):
        """A kernel vector on which the prescribed character is nontrivial."""
        self._refresh()
        if not self.rows:
            return None
        for r in range(self._rank, len(self.rows)):
            relation = self._U[r]
            sign = 0
            exponents: dict[int, int] = {}
            for coefficient, gamma in zip(relation, self.gammas):
                if coefficient == 0:
                    continue
                s, table = factor_rational(gamma)
                sign ^= (s * coefficient) & 1
                for prime, exponent in table.items():
                    exponents[prime] = exponents.get(prime, 0) + coefficient * exponent
            if sign or any(exponents.values()):
                return relation
        return None

    # -- class arithmetic ---------------------------------------------------
    def solve(self, target: list[int]):
        """lambda with lambda * rows = target, or None (integer solvability)."""
        self._refresh()
        if not self.rows:
            return [0] * 0 if all(x == 0 for x in target) else None
        residue = list(target)
        coefficients = [0] * len(self.rows)
        for r, column in enumerate(self._pivots):
            if residue[column] == 0:
                continue
            pivot = self._H[r][column]
            if residue[column] % pivot:
                return None
            factor = residue[column] // pivot
            coefficients[r] = factor
            for c in range(self.width):
                residue[c] -= factor * self._H[r][c]
        if any(residue):
            return None
        # coefficients are with respect to H; pull back through U.
        out = [0] * len(self.rows)
        for r, factor in enumerate(coefficients):
            if factor == 0:
                continue
            for c in range(len(self.rows)):
                out[c] += factor * self._U[r][c]
        return out

    def value(self, target: list[int]):
        """gamma(target) if target lies in the lattice, else None."""
        coefficients = self.solve(target)
        if coefficients is None:
            return None
        result = Fraction(1)
        for coefficient, gamma in zip(coefficients, self.gammas):
            if coefficient:
                result *= gamma ** coefficient
        return result


# ------------------------------------------------------------ the kill engine


def class_decomposition(character: Character, exponents: list[tuple[int, ...]]):
    """Group terms of one fibre into character classes with signed weights.

    Returns [(representative index, coefficient)] with coefficient in Q.
    """
    classes: list[list] = []          # [rep index, coefficient]
    for index, vector in enumerate(exponents):
        placed = False
        for entry in classes:
            difference = [a - b for a, b in zip(vector, exponents[entry[0]])]
            gamma = character.value(difference)
            if gamma is not None:
                entry[1] += gamma
                placed = True
                break
        if not placed:
            classes.append([index, Fraction(1)])
    return classes


def analyse(geo: Geometry, labels, max_rounds: int = 40, table=None):
    """Exact verdict for one coordinate template.

    Phases, in the order the committed artifacts use them:
      K0  every constant fibre nonempty                (six-site sec. 4 item 3)
      O2a literal singleton mixed fibre                (six-site sec. 4 item 4)
      O1  odd holonomy of the binomial relation lattice
          (notes/n8-toric-binomial-lattice-audit.md: consistent over the
           complex torus iff (0,1) not in L; here in the equivalent kernel form)
      O2b one live class modulo that lattice           (single-fibre Laurent
          conflict, proofs/low-rank-graph-laurent-obstruction.md)
      ...  two live classes generate a NEW relation x^d = gamma in Q^*; iterate
      K3  a constant fibre all of whose classes cancel (pure vanishing)

    verdict in {'missing-constant', 'O2-literal-singleton', 'O1-odd-holonomy',
                'O2-one-live-class', 'K3-pure-vanishing', 'survivor'}.
    """
    if table is None:
        table = fibres(geo, labels)
    mixed = {c: members for c, members in table.items() if is_mixed(c)}
    constants = {c: table.get(c, []) for c in
                 (tuple([r] * geo.size) for r in range(Q))}

    for colour, members in constants.items():
        if not members:
            return {"verdict": "missing-constant", "colour": list(colour)}

    singleton_words = [c for c, members in mixed.items() if len(members) == 1]
    if singleton_words:
        return {"verdict": "O2-literal-singleton",
                "words": [list(w) for w in singleton_words],
                "singletons": len(singleton_words)}

    width = len(geo.edges)
    character = Character(width)
    exponents = {number: geo.exponent(number)
                 for members in table.values() for number in members}

    # -- O1: all binomial mixed fibres at once, then the exact kernel test.
    binomials = [(c, members) for c, members in sorted(mixed.items())
                 if len(members) == 2]
    for _colouring, (first, second) in binomials:
        difference = [a - b for a, b in zip(exponents[first], exponents[second])]
        character.add(difference, Fraction(-1))
    relation = character.odd_relation()
    if relation is not None:
        used = [binomials[i][0] for i, x in enumerate(relation) if x]
        return {"verdict": "O1-odd-holonomy",
                "coefficients": [x for x in relation if x],
                "words": [list(w) for w in used],
                "binomials": len(binomials)}

    # -- O2b / relation propagation on the remaining fibres.
    for _ in range(max_rounds):
        changed = False
        for colouring, members in sorted(mixed.items()):
            if len(members) == 2:
                continue
            vectors = [exponents[number] for number in members]
            classes = class_decomposition(character, vectors)
            live = [entry for entry in classes if entry[1] != 0]
            if len(live) == 1:
                return {"verdict": "O2-one-live-class",
                        "word": list(colouring), "terms": len(members),
                        "classes": len(classes)}
            if len(live) == 2:
                (i, ci), (j, cj) = live
                difference = [a - b for a, b in zip(vectors[i], vectors[j])]
                character.add(difference, Fraction(-1) * cj / ci)
                relation = character.odd_relation()
                if relation is not None:
                    return {"verdict": "O1-odd-holonomy",
                            "detail": "after class propagation",
                            "coefficients": [x for x in relation if x]}
                changed = True
        if not changed:
            break

    for colour, members in constants.items():
        vectors = [exponents[number] for number in members]
        classes = class_decomposition(character, vectors)
        if all(entry[1] == 0 for entry in classes):
            return {"verdict": "K3-pure-vanishing", "colour": list(colour),
                    "terms": len(members)}

    return {"verdict": "survivor", "relations": len(character.rows),
            "mixed_fibres": len(mixed),
            "mixed_histogram": dict(sorted(
                {k: v for k, v in fibre_profile(table)[1].items()}.items()))}


def fibre_profile(table):
    """(#mixed singleton fibres, size histogram of mixed fibres)."""
    histogram: dict[int, int] = {}
    singletons = 0
    for colouring, members in table.items():
        if not is_mixed(colouring):
            continue
        histogram[len(members)] = histogram.get(len(members), 0) + 1
        if len(members) == 1:
            singletons += 1
    return singletons, histogram

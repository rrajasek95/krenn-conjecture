#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- general bicoloured template kill engine at N = 8.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5
Plan: notes/2026-08-15-resolution-master-plan.md, v8 addendum (W8 mission).
Nothing here is a proved claim.  Every verdict uses exact arithmetic
(Python ints / Fraction).  numpy is used ONLY for boolean fibre membership
(integer/bool, no floats) and its output is cross-checked against a pure
Python reference in w8_controls.py.

MODEL.  N = 8 sites, V_v = C^3, one 3x3 block A_uv per edge uv of K_8
(rows = colour at the smaller endpoint u, columns = colour at v).  For a word
w in {0,1,2}^8

    H(A)_w = sum over perfect matchings M of K_8 of
             prod_{uv in M} A_uv[w_u][w_v].

Exactness: H_w = 1 on the three constant words, H_w = 0 on the 6558 mixed
words.  The diagonal gauge e_c^{(v)} -> mu_{v,c} e_c^{(v)} multiplies H_w by
prod_v mu_{v,w_v}; it preserves every template and rescales the three
constant values independently (3 conditions, 24 parameters), so

    EXACT SOURCE with template T  <=>  values x on the occupied cells, all
    nonzero, with (mixed) sum over fibre = 0 and (constant) sum != 0.

TEMPLATE.  T[e] is a 9-bit mask; bit 3*i+j set means cell (i,j) of edge e is
occupied.  supp(T) = number of nonzero blocks (this is "m", the band's
support; it counts EDGES, not cells -- cf. the committed occurrence-CNF
semantics audit).  Sigma(T) = number of occupied cells.

FIBRE.  For a word w, the matching M contributes iff every edge uv in M has
cell (w_u,w_v) occupied; the contribution is the monomial
prod_{uv in M} x_{uv,w_u,w_v}.  Distinct (M,w) give distinct monomials, and
each monomial occurs in exactly one equation.  |fibre| = 1 on a mixed word is
the O2 kill.

ADMISSIBILITY (committed support-level necessary conditions for an exact
source).  Beyond "some perfect matching is supported for each constant
colouring" (proofs/saturated-rank-graph-obstruction.md sec. 1 item 1) we
impose the committed FORCED INCIDENT-EDGE THEOREM (notes/slice-cover.md
sec. 2, eq. (6)):

  (FIE) for every vertex p and every colour r there is a neighbour j with
        A_pj = a (x) e_r^{(j)}, C_pj != 0,

i.e. the block on pj is nonzero and its support is contained in the single
FAR-END colour r.  Call such a block "r-thin at j".  A block thin at both
ends is a single cell; a block thin at exactly one end has 2 or 3 cells in
one line; all other nonzero blocks ("fat") serve no demand.  Counting the
24 demands (p,r) with <= 1 served per edge-endpoint gives

        2*beta + h >= 24,   beta + h + fat = m,   hence beta >= 24 - m
                                                   and  fat <= m - 12,

which re-derives W6's J.1d floor beta >= 3N - m and adds the far-end
structure W6's searches did not impose.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from typing import Iterable

import numpy as np

N = 8
Q = 3
FULL = (1 << 9) - 1


def perfect_matchings(vertices):
    if not vertices:
        return [()]
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            out.append(tuple(sorted(((first, vertices[index]),) + tail)))
    return out


class Geometry:
    def __init__(self, size=N):
        self.size = size
        self.edges = tuple(combinations(range(size), 2))
        self.index = {e: n for n, e in enumerate(self.edges)}
        self.matchings = tuple(perfect_matchings(tuple(range(size))))
        self.matching_edges = tuple(tuple(self.index[e] for e in m)
                                    for m in self.matchings)
        colours = np.indices((Q,) * size).reshape(size, -1).T
        self.colour = np.ascontiguousarray(colours.astype(np.int8))
        self.words = [tuple(int(x) for x in row) for row in self.colour]
        self.mixed = (self.colour != self.colour[:, :1]).any(axis=1)
        self.mixed_rows = np.nonzero(self.mixed)[0]
        self.constant_rows = [int(np.ravel_multi_index(tuple([r] * size),
                                                       (Q,) * size))
                              for r in range(Q)]
        # cellidx[e][word] = 3*w_u + w_v  (the cell edge e uses on that word)
        self.cellidx = np.empty((len(self.edges), len(self.colour)),
                                dtype=np.int64)
        for n, (u, v) in enumerate(self.edges):
            self.cellidx[n] = 3 * self.colour[:, u].astype(np.int64) \
                + self.colour[:, v].astype(np.int64)
        self.incident = tuple(tuple(self.index[tuple(sorted((p, j)))]
                                    for j in range(size) if j != p)
                              for p in range(size))


GEO_CACHE = {}


def geometry(size=N):
    if size not in GEO_CACHE:
        GEO_CACHE[size] = Geometry(size)
    return GEO_CACHE[size]


# --------------------------------------------------------------- fibres


def compat_matrix(geo, template):
    """(#matchings, #words) boolean: matching M is compatible with word w."""
    bits = np.asarray(template, dtype=np.int64)
    allowed = ((bits[:, None] >> geo.cellidx) & 1).astype(bool)
    out = np.empty((len(geo.matchings), len(geo.colour)), dtype=bool)
    for n, edges in enumerate(geo.matching_edges):
        row = allowed[edges[0]]
        for e in edges[1:]:
            row = row & allowed[e]
        out[n] = row
    return out


def fibre_sizes(geo, template, compat=None):
    if compat is None:
        compat = compat_matrix(geo, template)
    return compat.sum(axis=0, dtype=np.int64)


def fibre_table(geo, template, compat=None):
    """{word index: [matching indices]} for every word with a nonempty fibre."""
    if compat is None:
        compat = compat_matrix(geo, template)
    table = {}
    for w in np.nonzero(compat.any(axis=0))[0]:
        table[int(w)] = [int(x) for x in np.nonzero(compat[:, w])[0]]
    return table


def mixed_singletons(geo, template, compat=None):
    if compat is None:
        compat = compat_matrix(geo, template)
    sizes = compat.sum(axis=0, dtype=np.int64)
    return [int(w) for w in np.nonzero((sizes == 1) & geo.mixed)[0]]


def fibre_histogram(geo, template, compat=None):
    if compat is None:
        compat = compat_matrix(geo, template)
    sizes = compat.sum(axis=0, dtype=np.int64)[geo.mixed]
    hist = {}
    for s in sizes:
        s = int(s)
        if s:
            hist[s] = hist.get(s, 0) + 1
    return hist


# -------------------------------------------------- template bookkeeping


def support(template):
    return sum(1 for mask in template if mask)


def sigma(template):
    return sum(bin(mask).count("1") for mask in template)


def cells(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def far_thin_colour(mask, at_second):
    """The unique far colour if the block is thin at that endpoint, else None.

    at_second=True asks about the SECOND endpoint (columns), else the first.
    """
    if not mask:
        return None
    seen = set()
    for i, j in cells(mask):
        seen.add(j if at_second else i)
    if len(seen) == 1:
        return seen.pop()
    return None


def block_class(mask):
    """'zero' | 'single' | 'thin' (one end only) | 'fat'."""
    if not mask:
        return "zero"
    n = bin(mask).count("1")
    if n == 1:
        return "single"
    a = far_thin_colour(mask, False) is not None
    b = far_thin_colour(mask, True) is not None
    return "thin" if (a or b) else "fat"


def fie_demands(geo, template):
    """{(p,r): [edges serving it]} for all 24 demands."""
    out = {}
    for p in range(geo.size):
        for r in range(Q):
            servers = []
            for e in geo.incident[p]:
                u, v = geo.edges[e]
                colour = far_thin_colour(template[e], at_second=(u == p))
                if colour == r:
                    servers.append(e)
            out[(p, r)] = servers
    return out


def fie_ok(geo, template):
    return all(v for v in fie_demands(geo, template).values())


def constants_ok(geo, template, compat=None):
    if compat is None:
        compat = compat_matrix(geo, template)
    return all(bool(compat[:, row].any()) for row in geo.constant_rows)


def rectangular(mask):
    rows = sorted({i for i, _ in cells(mask)})
    cols = sorted({j for _, j in cells(mask)})
    return bin(mask).count("1") == len(rows) * len(cols)


def audit(geo, template, compat=None):
    if compat is None:
        compat = compat_matrix(geo, template)
    classes = [block_class(mask) for mask in template]
    beta = classes.count("single")
    thin = classes.count("thin")
    fat = classes.count("fat")
    return {
        "m": support(template), "sigma": sigma(template),
        "beta": beta, "thin": thin, "fat": fat,
        "fie": fie_ok(geo, template),
        "constants": constants_ok(geo, template, compat),
        "mixed_singletons": len(mixed_singletons(geo, template, compat)),
        "fibre_histogram": fibre_histogram(geo, template, compat),
        "budget_floor_ok": beta >= max(0, 3 * geo.size - support(template)),
        "H_blocks": sum(1 for mask in template if mask and not rectangular(mask)),
    }


# ------------------------------------------------------ Q^* as a Z-module
# (verbatim in substance from W2's w2_monomial.py -- exact, small integers)


def factor_rational(value: Fraction):
    sign = 0
    numerator, denominator = value.numerator, value.denominator
    if numerator < 0:
        sign = 1
        numerator = -numerator
    if numerator == 0:
        raise ValueError("zero is not in Q^*")
    exponents = {}
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


def hermite_with_transform(rows):
    m = len(rows)
    n = len(rows[0]) if m else 0
    H = [list(row) for row in rows]
    U = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    pivot_row = 0
    pivots = []
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
    """Relations x^{d_j} = gamma_j in Q^* with exact consistency/closure."""

    def __init__(self, width: int):
        self.width = width
        self.rows = []
        self.gammas = []
        self._dirty = True
        self._H, self._U, self._pivots, self._rank = [], [], [], 0

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
            self._H, self._U, self._pivots, self._rank = \
                hermite_with_transform(self.rows)
        self._dirty = False

    def odd_relation(self):
        """A Z-dependency among the relations on which the character is != 1."""
        self._refresh()
        if not self.rows:
            return None
        for r in range(self._rank, len(self.rows)):
            relation = self._U[r]
            sign = 0
            exponents = {}
            for coefficient, gamma in zip(relation, self.gammas):
                if coefficient == 0:
                    continue
                s, table = factor_rational(gamma)
                sign ^= (s * coefficient) & 1
                for prime, exponent in table.items():
                    exponents[prime] = exponents.get(prime, 0) \
                        + coefficient * exponent
            if sign or any(exponents.values()):
                return relation
        return None

    def solve(self, target):
        self._refresh()
        if not self.rows:
            return [] if all(x == 0 for x in target) else None
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
        out = [0] * len(self.rows)
        for r, factor in enumerate(coefficients):
            if factor == 0:
                continue
            for c in range(len(self.rows)):
                out[c] += factor * self._U[r][c]
        return out

    def value(self, target):
        coefficients = self.solve(target)
        if coefficients is None:
            return None
        result = Fraction(1)
        for coefficient, gamma in zip(coefficients, self.gammas):
            if coefficient:
                result *= gamma ** coefficient
        return result


def class_decomposition(character, exponents):
    classes = []
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


# -------------------------------------------------------- exponent maps


class CellCoords:
    """Monomial exponents in the occupied CELL variables x_{e,i,j}."""

    name = "cell"

    def __init__(self, geo, template):
        self.geo = geo
        self.index = {}
        for e, mask in enumerate(template):
            for c in range(9):
                if (mask >> c) & 1:
                    self.index[(e, c)] = len(self.index)
        self.width = len(self.index)

    def exponent(self, matching, word):
        row = [0] * self.width
        for e in self.geo.matching_edges[matching]:
            u, v = self.geo.edges[e]
            c = 3 * word[u] + word[v]
            row[self.index[(e, c)]] += 1
        return tuple(row)


class RankOneCoords:
    """Exponents after the rank-one substitution x_{e,i,j} = u^e_i v^e_j.

    Legitimate exactly when every nonzero block is rank one, i.e. (support
    level) rectangular.  Strictly stronger than CellCoords: the relation
    lattice is pushed forward along a projection, so classes can only merge.
    """

    name = "rank1"

    def __init__(self, geo, template):
        self.geo = geo
        self.index = {}
        for e, mask in enumerate(template):
            if not mask:
                continue
            if not rectangular(mask):
                raise ValueError("rank-one refinement needs rectangular blocks")
            for i, j in cells(mask):
                for key in ((e, 0, i), (e, 1, j)):
                    if key not in self.index:
                        self.index[key] = len(self.index)
        self.width = len(self.index)

    def exponent(self, matching, word):
        row = [0] * self.width
        for e in self.geo.matching_edges[matching]:
            u, v = self.geo.edges[e]
            row[self.index[(e, 0, word[u])]] += 1
            row[self.index[(e, 1, word[v])]] += 1
        return tuple(row)


# ------------------------------------------------------------ kill engine


def analyse(geo, template, coords=None, max_rounds=40, compat=None,
            collect=True):
    """Exact verdict for one template.

    Phases (the committed order, lifted from R_cell to general blocks):
      K0  a constant fibre is empty                       -> 0 != nonzero
      O2  a literal mixed singleton fibre
      O1  odd holonomy of the binomial relation lattice   -> "1 = -1"
      O2b one live class modulo that lattice
      ..  two live classes generate a new relation x^d = gamma in Q^*; iterate
      K3  a constant fibre all of whose classes cancel

    'survivor' means only that this closure did not refute the template.
    """
    if compat is None:
        compat = compat_matrix(geo, template)
    table = fibre_table(geo, template, compat)
    constants = {row: table.get(row, []) for row in geo.constant_rows}
    for row, members in constants.items():
        if not members:
            return {"verdict": "K0-missing-constant", "word": geo.words[row]}

    mixed = {w: members for w, members in table.items()
             if bool(geo.mixed[w])}
    singles = [w for w, members in mixed.items() if len(members) == 1]
    if singles:
        return {"verdict": "O2-literal-singleton", "count": len(singles),
                "word": geo.words[singles[0]],
                "matching": geo.matchings[mixed[singles[0]][0]]}

    if coords is None:
        coords = CellCoords(geo, template)
    exponent = {}

    def expo(w, mnum):
        key = (w, mnum)
        if key not in exponent:
            exponent[key] = coords.exponent(mnum, geo.words[w])
        return exponent[key]

    character = Character(coords.width)
    binomials = [(w, members) for w, members in sorted(mixed.items())
                 if len(members) == 2]
    for w, (first, second) in binomials:
        difference = [a - b for a, b in zip(expo(w, first), expo(w, second))]
        character.add(difference, Fraction(-1))
    relation = character.odd_relation()
    if relation is not None:
        used = [geo.words[binomials[i][0]]
                for i, x in enumerate(relation) if x]
        return {"verdict": "O1-odd-holonomy",
                "coefficients": [x for x in relation if x],
                "words": used[:12], "binomials": len(binomials)}

    rounds = 0
    for _ in range(max_rounds):
        rounds += 1
        changed = False
        for w, members in sorted(mixed.items()):
            if len(members) == 2:
                continue
            vectors = [expo(w, mnum) for mnum in members]
            groups = class_decomposition(character, vectors)
            live = [entry for entry in groups if entry[1] != 0]
            if len(live) == 1:
                return {"verdict": "O2-one-live-class", "word": geo.words[w],
                        "terms": len(members), "classes": len(groups)}
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

    for row, members in constants.items():
        vectors = [expo(row, mnum) for mnum in members]
        groups = class_decomposition(character, vectors)
        if all(entry[1] == 0 for entry in groups):
            return {"verdict": "K3-pure-vanishing", "word": geo.words[row],
                    "terms": len(members)}

    out = {"verdict": "survivor", "relations": len(character.rows),
           "mixed_fibres": len(mixed), "rounds": rounds,
           "coords": coords.name, "width": coords.width}
    if collect:
        out["mixed_histogram"] = dict(sorted(
            fibre_histogram(geo, template, compat).items()))
    return out


def analyse_best(geo, template, **kw):
    """Cell verdict; if it survives and all blocks are rectangular, also try
    the strictly stronger rank-one refinement."""
    first = analyse(geo, template, coords=CellCoords(geo, template), **kw)
    if first["verdict"] != "survivor":
        return first, None
    if all(rectangular(mask) for mask in template if mask):
        second = analyse(geo, template, coords=RankOneCoords(geo, template),
                         **kw)
        return first, second
    return first, None


# --------------------------------------------------------------- symmetry


def apply_symmetry(geo, template, perm, colour_perm):
    """perm: site permutation (tuple of 8); colour_perm: tuple of 3."""
    out = [0] * len(geo.edges)
    for e, mask in enumerate(template):
        if not mask:
            continue
        u, v = geo.edges[e]
        pu, pv = perm[u], perm[v]
        flip = pu > pv
        target = geo.index[(pv, pu)] if flip else geo.index[(pu, pv)]
        new = 0
        for i, j in cells(mask):
            a, b = colour_perm[i], colour_perm[j]
            if flip:
                a, b = b, a
            new |= 1 << (3 * a + b)
        out[target] = new
    return tuple(out)


def canonical(geo, template, perms=None, colour_perms=None):
    """Lexicographic canonical form under S_8 x S_3 (40320*6 images)."""
    from itertools import permutations
    if perms is None:
        perms = list(permutations(range(geo.size)))
    if colour_perms is None:
        colour_perms = list(permutations(range(Q)))
    best = None
    for perm in perms:
        for cp in colour_perms:
            image = apply_symmetry(geo, template, perm, cp)
            if best is None or image < best:
                best = image
    return best

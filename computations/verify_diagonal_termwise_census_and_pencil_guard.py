#!/usr/bin/env python3
"""The diagonal termwise census, the pencil identity, and the pencil
guard: what the committed diagonal recurrence engine can and cannot be
asked to prove.

Companion note: `notes/diagonal-termwise-census-and-pencil-guard.md`
(hand proofs).  Committed companions of this cluster:

  * `proofs/diagonal-hafnian-recurrence-obstruction.md` with checker
    `computations/verify_diagonal_recurrence_obstruction.py` -- the
    Boolean engine.  The shape-restricted encoder of section F below
    does NOT re-implement it: it imports `even_masks`, `add_iff_and`,
    `add_zero_forbids_unique`, `canonical_matching`,
    `integer_partitions` and `matching_of_cycle_type` from that module
    and, in the unrestricted mode, reproduces its CNF clause for
    clause, which is required here.
  * `notes/exact-source-live-split-forcing.md` (Theorem A/B, C4, C5) and
    `notes/good-crossing-matching-forcing.md` (C4', C5', Theorem C).
    Section G of this checker recomputes the crossing-pair counts X of
    both notes and the composition they support at N = 8.

This artifact AUDITS and UPGRADES the four unaudited scratch claims
recorded in section 6 of `notes/good-crossing-matching-forcing.md`.
What is established here, and at which strength:

  P   THE PENCIL IDENTITY (a polynomial identity in the edge weights,
      proved by hand in the note).  For symmetric zero-diagonal edge
      matrices W_0, W_1, W_2 on an even vertex set V,

        haf(x_0 W_0 + x_1 W_1 + x_2 W_2)[V]
          = sum over ordered even partitions (S_0,S_1,S_2) of V of
            x_0^{|S_0|/2} x_1^{|S_1|/2} x_2^{|S_2|/2}
            h_0(S_0) h_1(S_1) h_2(S_2).

      Verified at n = 4, 6, 8 on deterministic integer and Fraction
      packets, the two sides computed by different routes (a polynomial
      hafnian recursion versus per-colour scalar hafnian tables summed
      over 3^n colourings).  Every instance must contribute NONZERO
      monomials on both sides and at least one MIXED monomial, and a
      sharpness probe deletes one nonzero split term from the right-hand
      side and requires the two sides to disagree afterwards.

  D   DIAG-infinity: the uniform target is the TERMWISE statement, and
      the summed pencil form is a GUARD, not a target.
        T(k) (termwise): there are no W_0,W_1,W_2 with h_r(V) != 0 for
          every r and h_0(S_0)h_1(S_1)h_2(S_2) = 0 for every proper
          ordered even split.  This is exactly the hypothesis system (2)
          of proofs/diagonal-hafnian-recurrence-obstruction.md, and it
          is what a diagonal aggregate source forces.  It is SOLUBLE at
          k = 2 (the three one-factors of K_4 -- and the census of
          section U proves those are the only 0/1 solutions), INSOLUBLE
          at k = 3, 4, 5 by the cited SAT theorem, and conjectured
          insoluble for every k >= 3; k >= 6 is open.
        P(k) (summed): haf(x_0W_0 + x_1W_1 + x_2W_2) = x_0^k + x_1^k
          + x_2^k.  By the identity T(k) implies P(k), so a diagonal
          realization would solve P(k) -- but P(k) is SOLUBLE FOR EVERY
          k >= 2 and therefore obstructs nothing.  The checker verifies
          the general solution exactly: the alternating 2k-cycle over
          Q(zeta_2k) with odd edges x_0 and i-th even edge
          x_1 - zeta_i x_2, zeta_i the k roots of t^k = -1, for
          k = 2..6, with its live splits counted at k <= 5 (they must
          exist at k = 3,4,5, or the committed SAT theorem would be
          contradicted); and two RATIONAL solutions at k = 2, 3 that
          also carry live splits, so the failure of the converse needs
          no field extension.  Hence pencil insolubility cannot be a
          route to Krenn's conjecture: the identity's role is to show
          where the content is NOT.

  C   TWO-COLOUR SATISFIABILITY.  The alternating 2k-cycle solves both
      the summed and the termwise two-colour problems at every k
      (verified exactly for k = 2..6): haf(xW_0 + yW_1) = x^k + y^k,
      the two anchors are 1, and every split with an empty part is
      dead.  Hence no argument that looks at two colours at a time --
      equivalently at splits with an empty part -- can obstruct
      anything, and every uniform proof must be three-colour
      simultaneous.

  H   HAMILTONIAN TRIPLES.  D(n) = the first three factors F_0,F_1,F_2
      of the round-robin one-factorization of K_n.  For every even
      n >= 4 the three unions F_r u F_s are single Hamiltonian cycles
      (hand proof in the note; verified n = 4..24 together with the
      reflection description and the gcd step the proof uses), whence
      h_r(V) = 1 and EVERY split with an empty part is dead (verified
      n = 4..16 by exhaustion over all 2^n masks and all six colour
      orders).  In particular the shape (0,2,n-2) is dead at every even
      order: its liveness CANNOT be forced, which inverts the naive
      reading of the failing-shape analysis of the committed notes.  A
      second witness, the K_4-block family at n = 8, 12, has live
      two-part splits of shape (0,4,n-4) and still no live (0,2,n-2).

  U   LEMMA U2 (proved).  If every split with an empty part is dead
      then a pair lying in two co-supports C_r n C_s is a NON-EDGE of
      both colours; consequently the pair-deletion step of a naive
      induction on n is never available.  Its hypothesis and its
      overlap conclusion are never simultaneously realizable on the two
      exhaustive censuses run here (0/1 packets at n = 4; one-factor
      unions at n = 6), which is DISCLOSED as a vacuity: what the
      censuses verify non-vacuously is the lemma's mechanism through
      its contrapositive -- on every instance where a co-support
      overlap carries a cell, the predicted split (the pair alone in
      the colour where it is an edge, its complement in the other) is
      REQUIRED to be returned by the same independent empty-part scan
      (two_part_census) that every other section uses, on 490176 and
      1026720 instances respectively.  The censuses' own deadness
      verdict is routed through that scan as well, and a census-level
      positive control exhibits a packet on which a same-mask scan and
      the complement scan disagree on the verdict itself, with the
      verdict required live.  Both censuses also classify their
      solutions: the packets with every empty-part split dead are
      exactly the ordered triples of distinct one-factors (6 at
      n = 4, 60 at n = 6).

  S   THE SHAPE-RESTRICTED CENSUS (needs a SAT solver; see below).
      n = 6 unrestricted UNSAT (reproducing the committed engine's own
      verdict and its 411/2904/5 counts); n = 6 dropping the shape
      (0,2,4) SAT; n = 8 dropping the shape (0,2,6) UNSAT -- the new
      theorem, which section 6 of `notes/good-crossing-matching-
      forcing.md` cites as unaudited scratch; n = 8 dropping both
      shapes with X <= 2N SAT; n = 6, 8 keeping only the two-part
      clauses SAT, with D(n)'s own Boolean shadow as an explicit model.
      n = 10 is UNRESOLVED and is not attempted (opt-in `--n10`, which
      reports the solver's verdict without asserting an expectation).

  G   COMPOSITION at N = 8.  Every diagonal packet with the three pure
      anchors has a live split of shape != (0,2,6) (S); every N = 8
      shape other than (0,2,6) has X > 3N/2 (recomputed here); so by
      C4' of `notes/good-crossing-matching-forcing.md` a good crossing
      PAIR exists unconditionally at N = 8.  The caveat is the
      committed note's own: a good crossing pair is strictly weaker
      than Theorem C's conclusion that some nonzero crossing matching
      has ALL its crossing edges good.  The census also shows the
      C4'/C5' improvement is load-bearing: with the committed C4/C5
      bound X <= 2N one must drop (0,4,4) as well, and that instance is
      SAT.

SOLVER AVAILABILITY.  The committed engine imports PySAT at module
scope and dies if it is missing; several other checkers in this
repository raise `SystemExit("python-sat is required; ...")`.  Here the
exact sections P, D, C, H, U, G need no solver at all and always run,
while section S imports PySAT *and* the committed engine lazily: if
either import fails -- which happens under `python3 -S`, where
site-packages is not on the path -- the census is SKIPPED with a loud
flag, its verdicts are reported as NOT ESTABLISHED in this run, and the
SAT ledger is not hashed.  No verdict is ever faked.  Run with
`--require-solver` to make a missing solver a hard failure instead
(exit code 1, with the diagnostic text used by the repository's other
solver-dependent checkers).

Exact stdlib arithmetic only: int and Fraction.  No floats, no numpy,
no bare asserts.  Krenn's conjecture remains open.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import sys
from fractions import Fraction
from hashlib import sha256
from math import gcd

EXPECTED_LEDGER_SHA256 = (
    "fb019894c5dbf111dd6536c870812c7c20a07919025d3ce0ad79dcf2b31a4a5c")
EXPECTED_SAT_LEDGER_SHA256 = (
    "da4b6196c5182b7d66e0f46f99e23e0409ef3486a907ba3882935790681f3b82")

# The counts published in `proofs/diagonal-hafnian-recurrence-obstruction.md`
# section 3 for the unrestricted engine.  They are additionally required to
# agree with the committed builder's own output, so a change upstream breaks
# this checker rather than silently drifting away from it.
PUBLISHED_ENGINE_COUNTS = {6: (411, 2904, 5), 8: (2988, 23844, 9)}

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    # `python3 -I` does not prepend the script directory, so the committed
    # sibling module is imported through an explicit, file-relative path.
    sys.path.insert(0, _HERE)


def require(condition, detail):
    """Assertion that survives `python3 -O` (never use a bare assert)."""
    if not condition:
        raise RuntimeError(detail)


# --------------------------------------------------------------- hashing


def canonical(value):
    """Canonical JSON-able image of exact data (Fractions become strings)."""
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, Fraction):
        return "F" + str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return {str(canonical(key)): canonical(item)
                for key, item in sorted(value.items(), key=lambda kv: str(kv[0]))}
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted(str(canonical(item)) for item in value)
    raise RuntimeError("uncanonicalizable value in the ledger: %r" % (value,))


def content_hash(value):
    encoded = json.dumps(canonical(value), sort_keys=True, separators=(",", ":"))
    return sha256(encoded.encode("ascii")).hexdigest()


# -------------------------------------------------------------- hafnians


def hafnian_table(n, weight):
    """h[mask] = haf(W[mask]) for every even mask, by lowest-vertex pivot.

    Exact: the entries are whatever ring elements `weight` returns (int or
    Fraction here).  Odd masks are absent from the table by construction.
    """
    table = {0: 1}
    for mask in range(1 << n):
        if mask.bit_count() % 2 or mask == 0:
            continue
        pivot = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << pivot)
        total = 0
        other = rest
        while other:
            bit = other & -other
            vertex = bit.bit_length() - 1
            other ^= bit
            cell = weight(pivot, vertex)
            if cell:
                total += cell * table[rest ^ bit]
        table[mask] = total
    return table


def dict_weight(entries):
    """Edge-weight callable for a dict keyed by frozenset({u,v})."""

    def weight(u, v):
        return entries.get(frozenset((u, v)), 0)

    return weight


def matching_entries(matching):
    return {frozenset(edge): 1 for edge in matching}


# ------------------------------------------------ polynomials in x0,x1,x2


def poly_add(left, right):
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, 0) + value
    return {key: value for key, value in out.items() if value}


def poly_mul(left, right):
    out = {}
    for key_left, value_left in left.items():
        for key_right, value_right in right.items():
            key = (key_left[0] + key_right[0],
                   key_left[1] + key_right[1],
                   key_left[2] + key_right[2])
            out[key] = out.get(key, 0) + value_left * value_right
    return {key: value for key, value in out.items() if value}


def poly_hafnian(n, entry):
    """Hafnian of a matrix with polynomial entries, same pivot recursion."""
    table = {0: {(0, 0, 0): 1}}
    for mask in range(1 << n):
        if mask.bit_count() % 2 or mask == 0:
            continue
        pivot = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << pivot)
        total = {}
        other = rest
        while other:
            bit = other & -other
            vertex = bit.bit_length() - 1
            other ^= bit
            cell = entry(pivot, vertex)
            if cell:
                total = poly_add(total, poly_mul(cell, table[rest ^ bit]))
        table[mask] = total
    return table[(1 << n) - 1]


def pencil_entry(packet):
    """The entry callable of x_0 W_0 + x_1 W_1 + x_2 W_2."""

    def entry(u, v):
        key = frozenset((u, v))
        out = {}
        for colour in range(3):
            cell = packet[colour].get(key, 0)
            if cell:
                out[tuple(1 if index == colour else 0 for index in range(3))] = cell
        return out

    return entry


def pure_target(n):
    """The polynomial x_0^{n/2} + x_1^{n/2} + x_2^{n/2}."""
    return {tuple(n // 2 if index == colour else 0 for index in range(3)): 1
            for colour in range(3)}


# ------------------------------------------------- exact cyclotomic field


def integer_poly_divide(numerator, divisor):
    """Exact quotient of two integer polynomials (little-endian, monic)."""
    numerator = list(numerator)
    degree = len(divisor) - 1
    require(divisor[-1] == 1, "the divisor of an exact division is not monic")
    quotient = [0] * max(1, len(numerator) - degree)
    for index in range(len(numerator) - 1, degree - 1, -1):
        coefficient = numerator[index]
        if not coefficient:
            continue
        quotient[index - degree] = coefficient
        for offset in range(degree + 1):
            numerator[index - degree + offset] -= coefficient * divisor[offset]
    require(not any(numerator),
            "an exact polynomial division left a remainder")
    return tuple(quotient)


def cyclotomic_polynomial(order, _cache={}):
    """Phi_order, computed from s^order - 1 by exact division."""
    if order in _cache:
        return _cache[order]
    numerator = [0] * (order + 1)
    numerator[0] = -1
    numerator[order] = 1
    numerator = tuple(numerator)
    for divisor in range(1, order):
        if order % divisor:
            continue
        numerator = integer_poly_divide(
            numerator, cyclotomic_polynomial(divisor))
    _cache[order] = numerator
    return numerator


class CyclotomicField:
    """Q(zeta_order) = Q[s]/Phi_order(s), exact over Fraction.

    Phi_order is irreducible over Q (classical), so this quotient is a
    field embedded in C by s -> exp(2 pi i / order); an element is zero
    here exactly when its complex image is zero.  The pencil equation
    of section D/C below is VERIFIED as an equality in Q[s]/Phi_2k(s),
    and equality is preserved by any ring homomorphism -- in particular
    by s -> exp(i pi / k) into C.  (Verifying it in Z[s]/(s^k+1)
    instead would NOT do: that quotient is not a domain when s^k+1 is
    reducible, and the equation is FALSE there for k = 3, 5, 6 -- at
    k = 3 the coefficient of x_1^2 x_2 of prod_i (x_1 - s^(2i+1) x_2)
    is 1 + s^2 - s != 0 in Z[s]/(s^3+1); the probe
    z_quotient_probe() verifies exactly this.)  Irreducibility is used
    only for the LIVENESS counts: a nonzero field element has a
    nonzero complex image.
    """

    def __init__(self, order):
        self.order = order
        self.modulus = cyclotomic_polynomial(order)
        self.degree = len(self.modulus) - 1

    def element(self, coefficients):
        return Cyclotomic(self, coefficients)

    def zero(self):
        return self.element([])

    def one(self):
        return self.element([1])

    def generator_power(self, exponent):
        coefficients = [0] * (exponent + 1)
        coefficients[exponent] = 1
        return self.element(coefficients)


class Cyclotomic:
    """An element of a CyclotomicField; exact Fraction coefficients."""

    __slots__ = ("field", "coefficients")

    def __init__(self, field, coefficients):
        working = [Fraction(value) for value in coefficients]
        modulus = field.modulus
        degree = field.degree
        for index in range(len(working) - 1, degree - 1, -1):
            coefficient = working[index]
            if not coefficient:
                continue
            for offset in range(degree + 1):
                working[index - degree + offset] -= coefficient * modulus[offset]
        working = working[:degree]
        while len(working) < degree:
            working.append(Fraction(0))
        self.field = field
        self.coefficients = tuple(working)

    def _coerce(self, other):
        if isinstance(other, Cyclotomic):
            require(other.field is self.field,
                    "cyclotomic elements of different fields were combined")
            return other
        return Cyclotomic(self.field, [other])

    def __add__(self, other):
        other = self._coerce(other)
        return Cyclotomic(self.field, [a + b for a, b in
                                       zip(self.coefficients,
                                           other.coefficients)])

    __radd__ = __add__

    def __neg__(self):
        return Cyclotomic(self.field, [-a for a in self.coefficients])

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __mul__(self, other):
        other = self._coerce(other)
        product = [Fraction(0)] * (2 * self.field.degree)
        for index, left in enumerate(self.coefficients):
            if not left:
                continue
            for offset, right in enumerate(other.coefficients):
                if right:
                    product[index + offset] += left * right
        return Cyclotomic(self.field, product)

    __rmul__ = __mul__

    def __bool__(self):
        return any(self.coefficients)

    def __eq__(self, other):
        if not isinstance(other, Cyclotomic):
            other = self._coerce(other)
        return self.coefficients == other.coefficients

    def __hash__(self):
        return hash((id(self.field), self.coefficients))

    def __repr__(self):
        return "Cyc(%s)" % ",".join(str(value) for value in self.coefficients)


def z_quotient_probe():
    """The withdrawn claim 'the pencil equation holds already in
    Z[s]/(s^k+1)' is falsifiable and FALSE: this probe computes the
    k = 3 counterexample.  The coefficient of x_1^2 x_2 in
    prod_{i=0}^{2} (x_1 - s^(2i+1) x_2) is -(s + s^3 + s^5), which
    reduces in Z[s]/(s^3+1) (where s^3 = -1) to 1 - s + s^2 -- a
    NONZERO residue, although the pencil equation needs it to vanish.
    In Q[s]/Phi_6(s), with Phi_6 = s^2 - s + 1, the same coefficient
    IS zero, which is why the guard's verification is carried out
    there and transported to C by a ring homomorphism.
    """
    # coefficient of x_1^2 x_2: -(s^1 + s^3 + s^5), little-endian.
    coefficients = [0] * 6
    for index in range(3):
        coefficients[2 * index + 1] -= 1
    residue = [0, 0, 0]
    for exponent, value in enumerate(coefficients):
        quotient, remainder = divmod(exponent, 3)
        residue[remainder] += value if quotient % 2 == 0 else -value
    require(residue == [1, -1, 1],
            "Z[s]/(s^3+1) probe: the coefficient of x_1^2 x_2 of "
            "prod_i (x_1 - s^(2i+1) x_2) did not reduce to 1 - s + s^2 "
            "modulo s^3 + 1")
    require(any(residue),
            "Z[s]/(s^3+1) probe: the coefficient 1 + s^2 - s vanished in "
            "Z[s]/(s^3+1), i.e. the withdrawn claim 'the pencil equation "
            "holds already in Z[s]/(s^k+1)' would be TRUE at k = 3; it must "
            "be false, since s^3+1 = (s+1)Phi_6(s) is reducible and the "
            "equation needs the quotient by Phi_6 alone")
    image_in_field = CyclotomicField(6).element(coefficients)
    require(not image_in_field,
            "Z[s]/(s^3+1) probe: the same coefficient is NOT zero in "
            "Q[s]/Phi_6(s), so the k = 3 cycle guard could never have "
            "verified the pencil equation there")
    return {"k": 3, "ring": "Z[s]/(s^3+1)",
            "coefficient_of_x1^2_x2_mod_s3_plus_1": residue,
            "nonzero_in_Z_quotient": bool(any(residue)),
            "zero_in_Q_mod_Phi6": not image_in_field}


# ------------------------------------------------------------- splits


def colour_masks(n):
    """Yield the mask triples of every proper ordered even split of V."""
    full = (1 << n) - 1
    for colouring in itertools.product(range(3), repeat=n):
        masks = [0, 0, 0]
        for vertex, colour in enumerate(colouring):
            masks[colour] |= 1 << vertex
        if any(mask.bit_count() % 2 for mask in masks):
            continue
        if any(mask == full for mask in masks):
            continue
        yield tuple(masks)


def split_census(n, tables):
    """Every live proper ordered even split, with its shape and products."""
    live = []
    examined = 0
    for masks in colour_masks(n):
        examined += 1
        products = tuple(tables[colour][masks[colour]] for colour in range(3))
        if all(products):
            shape = tuple(sorted(mask.bit_count() for mask in masks))
            live.append((masks, shape, products))
    return live, examined


def two_part_census(n, tables):
    """Every live split with an empty part, scanned over all masks.

    Counting convention: the entries are ORDERED (mask, first, second),
    with tables[first] live on the mask and tables[second] live on its
    complement, so each empty-part split -- an assignment of S to one
    colour and V \\ S to another, third part empty -- is counted TWICE,
    once as (S, a, b) and once as (V \\ S, b, a).  split_census counts
    the same split once, as a single ordered triple (S_0, S_1, S_2); a
    live count here is therefore twice the corresponding (0, ., .)
    shape count of split_census.
    """
    full = (1 << n) - 1
    live = []
    examined = 0
    for mask in range(1 << n):
        if mask.bit_count() % 2 or mask in (0, full):
            continue
        for first, second in itertools.permutations(range(3), 2):
            examined += 1
            if tables[first][mask] and tables[second][full ^ mask]:
                live.append((mask, first, second))
    return live, examined


def co_supports(n, tables):
    """C_r = { pairs uv : h_r(V \\ {u,v}) != 0 }."""
    full = (1 << n) - 1
    return [frozenset(frozenset((u, v))
                      for u in range(n) for v in range(u + 1, n)
                      if tables[colour][full ^ (1 << u) ^ (1 << v)])
            for colour in range(3)]


def recurrence_shadow_is_model(n, tables):
    """Rules (i),(ii) of the committed engine, read off actual hafnians."""
    for colour in range(3):
        table = tables[colour]
        for mask in range(1 << n):
            if mask.bit_count() % 2 or mask.bit_count() < 4:
                continue
            vertices = [v for v in range(n) if mask >> v & 1]
            for pivot in vertices:
                terms = 0
                for other in vertices:
                    if other == pivot:
                        continue
                    edge_mask = (1 << pivot) | (1 << other)
                    if table[edge_mask] and table[mask ^ edge_mask]:
                        terms += 1
                if table[mask]:
                    if terms < 1:
                        return False
                elif terms == 1:
                    return False
    return True


# ------------------------------------------------------- one-factors


def one_factors(n):
    """Round-robin one-factorization of K_n: the n-1 factors F_0..F_{n-2}.

    Vertex n-1 plays the role of infinity; F_r pairs it with r and pairs
    x with 2r-x modulo m = n-1 for the other vertices.
    """
    require(n % 2 == 0 and n >= 4, "one_factors needs an even n >= 4")
    modulus = n - 1
    factors = []
    for r in range(modulus):
        matching = [(r, n - 1)]
        for offset in range(1, n // 2):
            first = (r + offset) % modulus
            second = (r - offset) % modulus
            matching.append((min(first, second), max(first, second)))
        factors.append(tuple(sorted(matching)))
    seen = set()
    for factor in factors:
        cover = set()
        for u, v in factor:
            require(u != v, "one-factor carries a loop")
            cover |= {u, v}
            require(frozenset((u, v)) not in seen,
                    "the round-robin factors are not pairwise disjoint")
            seen.add(frozenset((u, v)))
        require(cover == set(range(n)),
                "a round-robin factor is not a perfect matching")
    return tuple(factors)


def reflection_factor(n, r):
    """F_r described as the reflection x -> 2r-x on Z_{n-1} plus {r, oo}."""
    modulus = n - 1
    edges = {frozenset((r, n - 1))}
    for x in range(modulus):
        y = (2 * r - x) % modulus
        if x != y:
            edges.add(frozenset((x, y)))
    return frozenset(edges)


def union_is_hamiltonian(n, first, second):
    """Is the union of two disjoint perfect matchings a single n-cycle?"""
    adjacency = {vertex: [] for vertex in range(n)}
    for u, v in list(first) + list(second):
        adjacency[u].append(v)
        adjacency[v].append(u)
    if any(len(neighbours) != 2 for neighbours in adjacency.values()):
        return False
    seen, current, previous = {0}, 0, None
    while True:
        following = next((w for w in adjacency[current] if w != previous), None)
        if following is None or following == 0:
            break
        if following in seen:
            return False
        seen.add(following)
        previous, current = current, following
    return len(seen) == n


def deterministic_ints(seed, count, low=-4, high=4):
    """Tiny reproducible LCG; no `random`, no numpy, no floats."""
    state = seed
    out = []
    span = high - low + 1
    for _ in range(count):
        state = (1103515245 * state + 12345) % (1 << 31)
        out.append(low + state % span)
    return out


# ============================================================ section P


def pencil_identity_instance(n, seed, fractional=False):
    """One instance of the pencil identity, both sides computed apart."""
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    values = deterministic_ints(seed, 3 * len(pairs))
    packet = []
    for colour in range(3):
        entries = {}
        for index, pair in enumerate(pairs):
            cell = values[colour * len(pairs) + index]
            if fractional:
                cell = Fraction(cell, index + 2)
            entries[frozenset(pair)] = cell
        packet.append(entries)

    left = poly_hafnian(n, pencil_entry(packet))

    tables = [hafnian_table(n, dict_weight(entries)) for entries in packet]
    right = {}
    terms = []
    for colouring in itertools.product(range(3), repeat=n):
        masks = [0, 0, 0]
        for vertex, colour in enumerate(colouring):
            masks[colour] |= 1 << vertex
        if any(mask.bit_count() % 2 for mask in masks):
            continue
        product = (tables[0][masks[0]] * tables[1][masks[1]]
                   * tables[2][masks[2]])
        if not product:
            continue
        key = tuple(mask.bit_count() // 2 for mask in masks)
        right[key] = right.get(key, 0) + product
        terms.append((tuple(masks), key, product))
    right = {key: value for key, value in right.items() if value}

    require(left == right,
            "pencil identity failed at n=%d seed=%d: the polynomial hafnian "
            "of the pencil differs from the sum over ordered even splits"
            % (n, seed))
    require(left, "pencil identity instance is vacuous: both sides are the "
                  "zero polynomial at n=%d seed=%d" % (n, seed))
    mixed = sum(1 for key in left if max(key) < n // 2)
    require(mixed >= 1,
            "pencil identity instance carries no MIXED monomial at n=%d "
            "seed=%d, so it tests nothing beyond the three pure hafnians"
            % (n, seed))
    require(terms, "pencil identity instance has no nonzero split term at "
                   "n=%d seed=%d" % (n, seed))

    # Sharpness: delete one nonzero split term from the right-hand side and
    # require the two sides to disagree.  Without this an identity assembled
    # from an over-general grouping would still pass.
    dropped_masks, dropped_key, dropped_product = terms[0]
    perturbed = dict(right)
    perturbed[dropped_key] = perturbed.get(dropped_key, 0) - dropped_product
    perturbed = {key: value for key, value in perturbed.items() if value}
    require(perturbed != left,
            "pencil identity sharpness probe is vacuous at n=%d seed=%d: "
            "deleting a nonzero split term left the two sides equal"
            % (n, seed))

    return {
        "n": n,
        "seed": seed,
        "fractional": fractional,
        "monomials": len(left),
        "mixed_monomials": mixed,
        "split_terms": len(terms),
        "dropped_term": [list(dropped_masks), list(dropped_key)],
        "left_hash": content_hash(sorted((list(k), v) for k, v in left.items())),
    }


def section_pencil_identity():
    instances = []
    for n in (4, 6, 8):
        for seed in (11, 2027):
            instances.append(pencil_identity_instance(n, seed))
    instances.append(pencil_identity_instance(4, 5, fractional=True))
    instances.append(pencil_identity_instance(6, 5, fractional=True))
    total_mixed = sum(instance["mixed_monomials"] for instance in instances)
    total_terms = sum(instance["split_terms"] for instance in instances)
    require(total_mixed > 0 and total_terms > 0,
            "the pencil identity was never exercised on a nonvacuous packet")
    return {
        "instances": len(instances),
        "orders": sorted({instance["n"] for instance in instances}),
        "total_mixed_monomials": total_mixed,
        "total_nonzero_split_terms": total_terms,
        "fractional_instances": sum(1 for instance in instances
                                    if instance["fractional"]),
        "detail": instances,
    }


# ============================================================ section D


def analyse_packet(n, packet, with_shapes=True):
    """Anchors, two-part census, co-supports and (optionally) shapes."""
    full = (1 << n) - 1
    tables = [hafnian_table(n, dict_weight(entries)) for entries in packet]
    anchors = tuple(table[full] for table in tables)
    two_part_live, two_part_examined = two_part_census(n, tables)
    supports = co_supports(n, tables)
    record = {
        "n": n,
        "anchors": [str(anchor) for anchor in anchors],
        "two_part_live": len(two_part_live),
        "two_part_examined": two_part_examined,
        "shape_0_2_live": sum(1 for mask, _, _ in two_part_live
                              if min(mask.bit_count(),
                                     n - mask.bit_count()) == 2),
        "co_support_sizes": [len(support) for support in supports],
        "co_support_pairwise": [len(supports[r] & supports[s])
                                for r, s in itertools.combinations(range(3), 2)],
        "co_support_triple": len(supports[0] & supports[1] & supports[2]),
    }
    if with_shapes:
        live, examined = split_census(n, tables)
        shapes = {}
        for _masks, shape, _products in live:
            shapes[shape] = shapes.get(shape, 0) + 1
        record["live_splits"] = len(live)
        record["splits_examined"] = examined
        record["live_shapes"] = {str(shape): count
                                 for shape, count in sorted(shapes.items())}
        record["first_live_split"] = ([list(live[0][0]), list(live[0][1])]
                                      if live else None)
    return tables, record


def strictness_witness(n, packet, label):
    """A packet solving the SUMMED pencil equation but not the termwise one."""
    tables, record = analyse_packet(n, packet)
    pencil = poly_hafnian(n, pencil_entry(packet))
    require(pencil == pure_target(n),
            "strictness witness %s does not solve haf(pencil) = "
            "x_0^k + x_1^k + x_2^k" % label)
    live, _examined = split_census(n, tables)
    require(live,
            "strictness witness %s is vacuous: it has no live split, so it "
            "does not separate the summed pencil equation from the termwise "
            "condition" % label)
    # The mechanism: inside at least one shape, two or more nonzero split
    # products cancel.  Without a cancelling shape the witness would be a
    # coincidence of the enumeration rather than of the algebra.
    by_exponent = {}
    for masks, _shape, products in live:
        key = tuple(mask.bit_count() // 2 for mask in masks)
        product = products[0] * products[1] * products[2]
        by_exponent.setdefault(key, []).append(product)
    cancelling = {key: values for key, values in by_exponent.items()
                  if len(values) >= 2 and sum(values) == 0}
    require(cancelling,
            "strictness witness %s has no shape in which two or more nonzero "
            "split products cancel" % label)
    record["label"] = label
    record["pencil_is_pure"] = bool(pencil == pure_target(n))
    record["cancelling_exponents"] = {
        str(list(key)): [str(value) for value in values]
        for key, values in sorted(cancelling.items())}
    record["packet"] = [sorted([sorted(pair), str(cell)]
                               for pair, cell in entries.items() if cell)
                        for entries in packet]
    return record


def witness_k2():
    """k = 2 witness, built by hand (see the note, section 3)."""
    return [
        {frozenset((0, 1)): 1, frozenset((2, 3)): 1},
        {frozenset((0, 1)): 1, frozenset((2, 3)): -1, frozenset((0, 2)): 1,
         frozenset((1, 3)): 1, frozenset((0, 3)): 1, frozenset((1, 2)): 1},
        {frozenset((0, 2)): 2, frozenset((1, 3)): 4, frozenset((0, 3)): 1,
         frozenset((1, 2)): -7},
    ]


def witness_k3():
    """k = 3 witness: D(6) with two edges added, one per colour."""
    factors = one_factors(6)[:3]
    packet = [dict(matching_entries(factor)) for factor in factors]
    for colour, pair, cell in ((0, (0, 1), 1), (1, (0, 3), -2)):
        key = frozenset(pair)
        packet[colour][key] = packet[colour].get(key, 0) + cell
    return packet


def section_diag_infinity(family_orders):
    """T(k) => P(k), and two witnesses that the converse fails.

    Termwise solutions exist only at k = 2 among the audited orders -- at
    k = 3,4,5 the cited SAT theorem forbids them -- so the full implication
    is exercised there, on the six ordered triples of one-factors of K_4
    that the n = 4 census proves are the only 0/1 solutions.  At larger
    orders the implication is exercised in the form D(n) does satisfy: the
    deadness of every EMPTY-PART split must kill exactly the monomials with
    one zero exponent, and nothing else.
    """
    termwise = []
    for order in itertools.permutations(range(3)):
        base = one_factors(4)
        packet = [matching_entries(base[index]) for index in order]
        tables = [hafnian_table(4, dict_weight(entries)) for entries in packet]
        live, examined = split_census(4, tables)
        require(not live and examined > 0,
                "the k=2 termwise packet %s is not termwise dead" % (order,))
        pencil = poly_hafnian(4, pencil_entry(packet))
        require(pencil == pure_target(4),
                "a termwise-dead packet at k=2 does not solve the summed "
                "pencil equation, contradicting the identity")
        termwise.append(list(order))

    empty_part = []
    for n in family_orders:
        packet = [matching_entries(factor) for factor in one_factors(n)[:3]]
        pencil = poly_hafnian(n, pencil_entry(packet))
        for colour in range(3):
            require(pencil.get(tuple(n // 2 if index == colour else 0
                                     for index in range(3))) == 1,
                    "D(%d): a pure monomial of the pencil is not 1" % n)
        two_colour_monomials = [key for key in pencil
                                if sum(1 for exponent in key if exponent == 0) == 1]
        require(not two_colour_monomials,
                "D(%d): the pencil carries a two-colour monomial although "
                "every split with an empty part is dead" % n)
        fully_mixed = sorted((list(key), value) for key, value in pencil.items()
                             if all(key))
        require(n == 4 or fully_mixed,
                "D(%d): the pencil has no fully mixed monomial, so the "
                "vanishing of the two-colour ones tests nothing" % n)
        empty_part.append({"n": n,
                           "fully_mixed_monomials": [[key, str(value)]
                                                     for key, value in fully_mixed]})

    witnesses = [strictness_witness(4, witness_k2(), "k=2"),
                 strictness_witness(6, witness_k3(), "k=3")]
    return {
        "termwise_packets_at_k2": termwise,
        "empty_part_implication": empty_part,
        "witnesses": witnesses,
        "termwise_insoluble_orders": [6, 8, 10],
        "summed_soluble_orders": [4, 6],
    }


# ============================================================ section C


def cycle_pencil_guard(k):
    """The alternating 2k-cycle over Q(zeta_2k) with the pencil weights.

    Odd edges carry x_0; the i-th even edge carries x_1 - zeta_i x_2, with
    zeta_i = s^{2i+1} the k distinct roots of t^k = -1.  A 2k-cycle has
    exactly two perfect matchings, so the hafnian of the pencil is
    x_0^k + prod_i (x_1 - zeta_i x_2) = x_0^k + x_1^k + x_2^k.
    """
    field = CyclotomicField(2 * k)
    n = 2 * k
    packet = [{}, {}, {}]
    roots = []
    for index in range(k):
        packet[0][frozenset((2 * index, 2 * index + 1))] = field.one()
        edge = frozenset((2 * index + 1, (2 * index + 2) % n))
        root = field.generator_power(2 * index + 1)
        roots.append(root)
        packet[1][edge] = field.one()
        packet[2][edge] = -root
    return field, n, packet, roots


def section_pencil_guard(max_k, max_live_k):
    """The summed pencil equation is SOLUBLE at every k: it is not a target."""
    records = []
    for k in range(2, max_k + 1):
        field, n, packet, roots = cycle_pencil_guard(k)
        power = field.one()
        for root in roots:
            candidate = field.one()
            for _ in range(k):
                candidate = candidate * root
            require(candidate == -field.one(),
                    "cycle guard k=%d: a designated weight is not a root of "
                    "t^k = -1" % k)
            power = power * root
        require(len({root.coefficients for root in roots}) == k,
                "cycle guard k=%d: the k roots of t^k = -1 are not distinct" % k)

        target = {key: field.one() for key in pure_target(n)}
        pencil = poly_hafnian(n, pencil_entry(packet))
        require(pencil == target,
                "cycle guard k=%d: haf(x_0W_0 + x_1W_1 + x_2W_2) is not "
                "x_0^k + x_1^k + x_2^k" % k)

        support = {}
        for entries in packet:
            for edge in entries:
                support[edge] = 1
        support_table = hafnian_table(n, dict_weight(support))
        require(support_table[(1 << n) - 1] == 2,
                "cycle guard k=%d: the support graph does not have exactly "
                "two perfect matchings, which is the mechanism of the "
                "construction" % k)

        tables = [hafnian_table(n, dict_weight(entries)) for entries in packet]
        anchors = [tables[colour][(1 << n) - 1] for colour in range(3)]
        require(all(anchor == field.one() for anchor in anchors),
                "cycle guard k=%d: a pure anchor is not 1" % k)

        record = {"k": k, "n": n, "field": "Q(zeta_%d)" % (2 * k),
                  "degree": field.degree,
                  "modulus": list(field.modulus),
                  "pencil_is_pure": bool(pencil == target),
                  "perfect_matchings_of_the_support":
                      support_table[(1 << n) - 1]}
        if k <= max_live_k:
            live, examined = split_census(n, tables)
            record["live_splits"] = len(live)
            record["splits_examined"] = examined
            record["live_shapes"] = sorted({str(list(shape))
                                            for _masks, shape, _p in live})
            if k >= 3:
                # At k = 3,4,5 the committed SAT theorem forbids a termwise
                # solution, so a pencil solution there MUST have a live
                # split; this is the consistency check between the two.
                require(live,
                        "cycle guard k=%d has NO live split, i.e. it is a "
                        "termwise solution, which would contradict the "
                        "committed SAT theorem" % k)
        records.append(record)
    return {"orders": [record["k"] for record in records],
            "z_quotient_probe": z_quotient_probe(),
            "detail": records}


def alternating_cycle(k):
    """The two alternating perfect matchings of the 2k-cycle."""
    n = 2 * k
    first = {frozenset((2 * i, 2 * i + 1)): 1 for i in range(k)}
    second = {frozenset((2 * i + 1, (2 * i + 2) % n)): 1 for i in range(k)}
    require(not (set(first) & set(second)),
            "the two alternating matchings of the 2k-cycle overlap")
    return n, first, second


def section_two_colour():
    records = []
    for k in range(2, 7):
        n, first, second = alternating_cycle(k)
        packet = [first, second, {}]
        pencil = poly_hafnian(n, pencil_entry(packet))
        target = {(k, 0, 0): 1, (0, k, 0): 1}
        require(pencil == target,
                "the alternating %d-cycle does not satisfy haf(xW_0 + yW_1) "
                "= x^%d + y^%d" % (n, k, k))
        tables = [hafnian_table(n, dict_weight(entries)) for entries in packet]
        require(tables[0][(1 << n) - 1] == 1 and tables[1][(1 << n) - 1] == 1,
                "an anchor of the alternating %d-cycle is not 1" % n)
        # The mechanism of the hand proof: the 2k-cycle has exactly two
        # perfect matchings, computed here rather than assumed.
        cycle = dict(first)
        cycle.update(second)
        cycle_table = hafnian_table(n, dict_weight(cycle))
        require(cycle_table[(1 << n) - 1] == 2,
                "the %d-cycle does not have exactly two perfect matchings"
                % n)
        live, examined = two_part_census(n, tables)
        two_colour_live = [entry for entry in live if 2 not in entry[1:]]
        require(not two_colour_live,
                "the alternating %d-cycle has a live two-colour split with an "
                "empty part" % n)
        require(examined > 0,
                "the two-part scan of the alternating %d-cycle examined "
                "nothing" % n)
        records.append({
            "k": k,
            "n": n,
            "monomials": len(pencil),
            "perfect_matchings_of_the_cycle": cycle_table[(1 << n) - 1],
            "two_part_splits_examined": examined,
            "two_colour_live": len(two_colour_live),
        })
    return {"orders": [record["k"] for record in records], "detail": records}


# ============================================================ section H


def section_hamiltonian_construction(max_order):
    """D(n) exists at every even n in 4..max_order, with the proof's data."""
    records = []
    for n in range(4, max_order + 1, 2):
        factors = one_factors(n)[:3]
        modulus = n - 1
        for index, factor in enumerate(factors):
            require(frozenset(frozenset(edge) for edge in factor)
                    == reflection_factor(n, index),
                    "F_%d at n=%d is not the reflection x -> 2r-x plus the "
                    "infinity edge, so the hand proof's model and the "
                    "constructed object have drifted apart" % (index, n))
        unions = []
        for first, second in itertools.combinations(range(3), 2):
            step = 2 * (first - second)
            require(gcd(abs(step), modulus) == 1,
                    "the gcd step of the Hamiltonicity proof fails at n=%d "
                    "for the pair (%d,%d)" % (n, first, second))
            hamiltonian = union_is_hamiltonian(n, factors[first],
                                               factors[second])
            require(hamiltonian,
                    "D(%d): the union of colours %d and %d is not a single "
                    "Hamiltonian cycle" % (n, first, second))
            unions.append([first, second, hamiltonian])
        edges = [frozenset(frozenset(edge) for edge in factor)
                 for factor in factors]
        for first, second in itertools.combinations(range(3), 2):
            require(not (edges[first] & edges[second]),
                    "D(%d): colours %d and %d share an edge" % (n, first, second))
        records.append({"n": n, "unions": unions})
    return records


def section_hamiltonian_hafnians(max_two_part, max_shapes):
    records = []
    for n in range(4, max_two_part + 1, 2):
        factors = one_factors(n)[:3]
        packet = [matching_entries(factor) for factor in factors]
        tables, record = analyse_packet(n, packet, with_shapes=n <= max_shapes)
        require(record["anchors"] == ["1", "1", "1"],
                "D(%d): the pure anchors are not all 1" % n)
        require(record["two_part_examined"] > 0,
                "D(%d): the two-part scan examined nothing" % n)
        require(record["two_part_live"] == 0,
                "D(%d): a split with an empty part is live, contradicting the "
                "Hamiltonian-triple lemma" % n)
        require(record["shape_0_2_live"] == 0,
                "D(%d): a split of shape (0,2,n-2) is live" % n)
        supports = co_supports(n, tables)
        for colour, factor in enumerate(factors):
            require(supports[colour]
                    == frozenset(frozenset(edge) for edge in factor),
                    "D(%d): the co-support of colour %d is not its own "
                    "matching" % (n, colour))
        require(record["co_support_pairwise"] == [0, 0, 0],
                "D(%d): two co-supports meet" % n)
        require(record["co_support_triple"] == 0,
                "D(%d): a pair is deletable in all three colours" % n)
        shadow_is_model = bool(recurrence_shadow_is_model(n, tables))
        require(shadow_is_model,
                "D(%d): the Boolean shadow is not a model of the recurrence "
                "rules of the committed engine" % n)
        record["recurrence_shadow_model"] = shadow_is_model
        if "live_splits" in record:
            require(all(not shape.startswith("(0,")
                        for shape in record["live_shapes"]),
                    "D(%d): a live shape has an empty part" % n)
            if n >= 6:
                require(record["live_splits"] > 0,
                        "D(%d): no live split at all, which would contradict "
                        "the committed SAT theorem at n in {6,8,10}" % n)
        records.append(record)
    return records


def section_two_part_control():
    """A positive control for the empty-part scan itself.

    D(n) and the alternating cycles are packets on which the scan is
    supposed to report NOTHING, so on them a scan that compared a mask
    with itself instead of with its complement would look identical.
    This four-site packet has one designed live empty-part split,
    S_0 = {0,1} in colour 0 against S_1 = {2,3} in colour 1, and colour
    1 is deliberately zero on the pair {0,1}, so the two scans give
    different answers here.
    """
    packet = [
        {frozenset((0, 1)): 1, frozenset((2, 3)): 1},
        {frozenset((2, 3)): 1, frozenset((0, 2)): 1, frozenset((1, 3)): 1},
        {frozenset((0, 2)): 1, frozenset((1, 3)): 1},
    ]
    tables = [hafnian_table(4, dict_weight(entries)) for entries in packet]
    require(all(table[(1 << 4) - 1] for table in tables),
            "two-part control: an anchor vanishes")
    designed = (1 << 0) | (1 << 1)
    require(tables[1][designed] == 0,
            "two-part control is not discriminating: colour 1 is nonzero on "
            "the designed pair, so a same-mask scan would agree with a "
            "complement scan here")
    live, examined = two_part_census(4, tables)
    require(examined > 0, "two-part control: the scan examined nothing")
    designed_found = (designed, 0, 1) in live
    require(designed_found,
            "two-part control: the empty-part scan missed the designed live "
            "split S_0={0,1}, S_1={2,3}")
    return {"live": len(live), "examined": examined,
            "designed_split_found": designed_found}


def k4_block_family(n):
    """The K_4-block family: three one-factors inside each block of four."""
    require(n % 4 == 0, "the K_4-block family needs n divisible by 4")
    blocks = [tuple(range(4 * index, 4 * index + 4)) for index in range(n // 4)]
    base = one_factors(4)
    packet = []
    for colour in range(3):
        entries = {}
        for block in blocks:
            for u, v in base[colour]:
                entries[frozenset((block[u], block[v]))] = 1
        packet.append(entries)
    return packet


def section_k4_blocks():
    records = []
    for n in (8, 12):
        _tables, record = analyse_packet(n, k4_block_family(n))
        require(record["anchors"] == ["1", "1", "1"],
                "K_4-block family at n=%d: the anchors are not all 1" % n)
        require(record["shape_0_2_live"] == 0,
                "K_4-block family at n=%d: a split of shape (0,2,n-2) is live"
                % n)
        require(record["two_part_live"] > 0,
                "K_4-block family at n=%d has no live two-part split, so it "
                "is not the second witness it is advertised to be" % n)
        records.append(record)
    return records


# ============================================================ section U


def empty_part_deadness(n, tables):
    """The deadness verdict of the section-U censuses.

    Routed through two_part_census -- the same empty-part scan that
    sections C and H and the positive control of
    section_two_part_control exercise -- rather than re-implemented
    inline, so a same-mask corruption of the scan is caught by the
    controls instead of passing silently here.  Returns
    (dead, live_entries), live_entries in two_part_census's ordered
    (mask, first, second) convention.
    """
    live, _examined = two_part_census(n, tables)
    return not live, live


def u2_deadness_control():
    """A census-level positive control for the U2 deadness verdict.

    On D(n) and on the one-factor triples the verdict is DEAD, so a
    scan that compared a mask with itself instead of with its
    complement would produce the same verdict there.  This n = 6
    packet is designed so that the two scans DISAGREE on the verdict
    itself: no proper even mask is live in two colours at once (a
    same-mask scan would report every empty-part split dead), yet
    S = {0,1} is live in colour 0 and V \\ S = {2,3,4,5} is live in
    colour 1, so the complement scan must report the packet live.
    All three anchors are nonzero, so the packet would be usable in
    the censuses.
    """
    packet = [
        {frozenset((0, 1)): 1, frozenset((0, 2)): 1, frozenset((1, 3)): 1,
         frozenset((4, 5)): 1},
        {frozenset((0, 3)): 1, frozenset((1, 5)): 1, frozenset((2, 4)): 1,
         frozenset((3, 5)): 1},
        {frozenset((0, 5)): 1, frozenset((1, 2)): 1, frozenset((3, 4)): 1},
    ]
    n = 6
    full = (1 << n) - 1
    tables = [hafnian_table(n, dict_weight(entries)) for entries in packet]
    require(all(table[full] for table in tables),
            "U2 deadness control: an anchor vanishes, so the packet would "
            "not be usable in the census")
    same_mask_live = 0
    for mask in range(1 << n):
        if mask.bit_count() % 2 or mask in (0, full):
            continue
        if sum(1 for colour in range(3) if tables[colour][mask]) >= 2:
            same_mask_live += 1
    require(same_mask_live == 0,
            "U2 deadness control is not discriminating: some proper even "
            "mask is live in two colours at once, so a same-mask scan would "
            "agree with the complement scan on this packet")
    dead, live = empty_part_deadness(n, tables)
    designed = (1 << 0) | (1 << 1)
    designed_found = (designed, 0, 1) in live
    require(designed_found,
            "U2 deadness control: the designed live split S={0,1} in colour "
            "0 against its complement {2,3,4,5} in colour 1 was not "
            "returned by the deadness scan")
    require(not dead,
            "U2 deadness control: the census deadness verdict on the "
            "designed packet is DEAD, which is what a same-mask scan would "
            "report; the complement scan must find S={0,1} against "
            "{2,3,4,5} and report the packet live")
    return {"n": n, "live": len(live),
            "designed_split_found": designed_found,
            "same_mask_live_masks": same_mask_live,
            "dead_verdict": dead}


def u2_census(n, matrices, label):
    """Lemma U2 and its contrapositive over an explicit family of packets.

    The deadness verdict is empty_part_deadness (i.e. two_part_census);
    the contrapositive check requires, on every instance where a
    co-support overlap carries a cell, that the split named in the
    lemma's proof is RETURNED BY that same scan -- an independent
    check that exercises the scan, rather than a recomputation of a
    product which the antecedent (the pair lies in both co-supports
    and is an edge of the sink colour) already forces to be nonzero.
    """
    full = (1 << n) - 1
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    profiles = []
    for entries in matrices:
        table = hafnian_table(n, dict_weight(entries))
        profiles.append({
            "anchor": table[full],
            "co_support": frozenset(frozenset(pair) for pair in pairs
                                    if table[full ^ (1 << pair[0])
                                             ^ (1 << pair[1])]),
            "edges": frozenset(frozenset(pair) for pair in pairs
                               if entries.get(frozenset(pair), 0)),
            "table": table,
            "entries": entries,
        })
    usable = [profile for profile in profiles if profile["anchor"]]

    dead_packets = []
    nonvacuous = 0
    violations = 0
    contrapositive = 0
    packets_examined = 0
    for triple in itertools.product(usable, repeat=3):
        packets_examined += 1
        dead, packet_live = empty_part_deadness(
            n, [profile["table"] for profile in triple])
        overlaps = [(first, second, pair)
                    for first, second in itertools.combinations(range(3), 2)
                    for pair in (triple[first]["co_support"]
                                 & triple[second]["co_support"])]
        carried = [(first, second, pair) for first, second, pair in overlaps
                   if pair in triple[first]["edges"]
                   or pair in triple[second]["edges"]]
        if dead:
            dead_packets.append(triple)
            if overlaps:
                nonvacuous += 1
            if carried:
                violations += 1
        elif carried:
            packet_live_set = set(packet_live)
            for first, second, pair in carried:
                # The lemma's own proof names the split that must be live:
                # the pair alone in one colour, its complement in the other.
                # Requiring the INDEPENDENT empty-part scan to return that
                # split exercises the scan; the antecedent (the pair lies
                # in both co-supports and is an edge of the sink colour)
                # already forces the split product nonzero, so recomputing
                # the product here would be tautological.
                u, v = sorted(pair)
                pair_mask = (1 << u) | (1 << v)
                for source, sink in ((first, second), (second, first)):
                    if pair not in triple[sink]["edges"]:
                        continue
                    cell = triple[sink]["entries"].get(pair, 0)
                    require(triple[sink]["table"][pair_mask] == cell,
                            "%s: the hafnian of a two-set disagrees with its "
                            "edge weight" % label)
                    require((pair_mask, sink, source) in packet_live_set,
                            "%s: the split predicted by Lemma U2's proof -- "
                            "the overlapping pair alone in the colour where "
                            "it is an edge, its complement in the other -- "
                            "is not returned by the empty-part scan" % label)
                    contrapositive += 1

    require(violations == 0,
            "%s: Lemma U2 is violated -- a packet with every empty-part split "
            "dead has an overlapping co-support pair carrying a cell" % label)
    require(contrapositive > 0,
            "%s: the Lemma U2 census is vacuous -- no overlapping co-support "
            "pair carrying a cell was ever exhibited, so neither the lemma "
            "nor its contrapositive was exercised" % label)
    require(dead_packets,
            "%s: no packet in the family satisfies the empty-part deadness "
            "hypothesis at all" % label)
    return {
        "label": label,
        "n": n,
        "matrices": len(matrices),
        "usable_matrices": len(usable),
        "packets_examined": packets_examined,
        "dead_packets": len(dead_packets),
        "u2_nonvacuous_packets": nonvacuous,
        "u2_violations": violations,
        "contrapositive_instances": contrapositive,
    }, dead_packets


def zero_one_matrices(n):
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    out = []
    for bits in range(1 << len(pairs)):
        out.append({frozenset(pair): (bits >> index) & 1
                    for index, pair in enumerate(pairs)})
    return out


def one_factor_union_matrices(n):
    factors = one_factors(n)
    out = []
    for bits in range(1 << len(factors)):
        entries = {}
        for index, factor in enumerate(factors):
            if bits >> index & 1:
                for edge in factor:
                    key = frozenset(edge)
                    entries[key] = entries.get(key, 0) + 1
        out.append(entries)
    return out


def section_u2():
    control = u2_deadness_control()
    census4, dead4 = u2_census(4, zero_one_matrices(4), "n=4 0/1 census")
    factor_sets4 = {frozenset(frozenset(edge) for edge in factor)
                    for factor in one_factors(4)}
    for triple in dead4:
        supports = [profile["edges"] for profile in triple]
        require(all(support in factor_sets4 for support in supports)
                and len(set(supports)) == 3,
                "n=4 0/1 census: a packet with all splits dead is not an "
                "ordered triple of distinct one-factors of K_4")
    require(census4["dead_packets"] == 6,
            "n=4 0/1 census: the number of packets solving the termwise "
            "condition is not the 6 orderings of the three one-factors")

    census6, dead6 = u2_census(6, one_factor_union_matrices(6),
                               "n=6 one-factor-union census")
    factor_sets6 = {frozenset(frozenset(edge) for edge in factor)
                    for factor in one_factors(6)}
    for triple in dead6:
        supports = [profile["edges"] for profile in triple]
        require(all(support in factor_sets6 for support in supports)
                and len(set(supports)) == 3,
                "n=6 one-factor-union census: a packet with all empty-part "
                "splits dead is not an ordered triple of distinct one-factors")
    require(census6["dead_packets"] == 60,
            "n=6 one-factor-union census: the empty-part-dead packets are not "
            "exactly the 60 ordered triples of distinct one-factors")
    return {"censuses": [census4, census6],
            "deadness_control": control,
            "u2_nonvacuous_packets_total": (census4["u2_nonvacuous_packets"]
                                            + census6["u2_nonvacuous_packets"]),
            "contrapositive_total": (census4["contrapositive_instances"]
                                     + census6["contrapositive_instances"])}


# ============================================================ section G


def shapes_of(n):
    """Even shapes a <= b <= c with a+b+c = n and c != n, with their X."""
    out = []
    for a in range(0, n + 1, 2):
        for b in range(a, n + 1, 2):
            c = n - a - b
            if c < b or c == n:
                continue
            out.append(((a, b, c), a * b + a * c + b * c))
    return out


def section_composition():
    """The counting arithmetic of C5 (X <= 2N) and C5' (X <= 3N/2)."""
    table = {}
    for n in range(6, 61, 2):
        entries = shapes_of(n)
        table[n] = {
            "committed_C5": [list(shape) for shape, x in entries if x <= 2 * n],
            "improved_C5prime": [list(shape) for shape, x in entries
                                 if 2 * x <= 3 * n],
        }
    require(table[8]["improved_C5prime"] == [[0, 2, 6]],
            "C5' recomputation broken: N=8 does not leave exactly the shape "
            "(0,2,6)")
    require(table[8]["committed_C5"] == [[0, 2, 6], [0, 4, 4]],
            "C5 recomputation broken: N=8 does not leave exactly (0,2,6) and "
            "(0,4,4)")
    for n in range(10, 61, 2):
        require(table[n]["improved_C5prime"] == [],
                "C5' recomputation broken: a shape with X <= 3N/2 survives at "
                "N=%d" % n)
    survivors = [list(shape) for shape, x in shapes_of(8) if 2 * x > 3 * 8]
    require(sorted(survivors) == [[0, 4, 4], [2, 2, 4]],
            "the N=8 shapes with X > 3N/2 are not (0,4,4) and (2,2,4)")
    return {
        "max_order": 60,
        "N8_shapes_and_X": [[list(shape), x] for shape, x in shapes_of(8)],
        "N8_committed_C5": table[8]["committed_C5"],
        "N8_improved_C5prime": table[8]["improved_C5prime"],
        "orders_with_a_C5prime_survivor": [n for n in table
                                           if table[n]["improved_C5prime"]],
        "N8_shapes_with_a_forced_good_crossing_pair": survivors,
    }


# ============================================================ section S


def import_solver():
    """Lazy import of PySAT and of the committed engine, as one unit."""
    try:
        from pysat.formula import CNF, IDPool
        from pysat.solvers import Solver
        import verify_diagonal_recurrence_obstruction as engine
    except ImportError as error:  # pragma: no cover - dependency diagnostic
        return None, "%s: %s" % (type(error).__name__, error)
    return (CNF, IDPool, Solver, engine), ""


def kept_shape(shape, n, mode):
    """Which split clauses a mode keeps.  `shape` is sorted ascending."""
    a, b, c = shape
    if mode == "full":
        return True
    if mode == "drop-0-2":
        return shape != (0, 2, n - 2)
    if mode == "drop-exceptional":
        # The committed C5 bound: shapes with X <= 2N escape the C4 count.
        return a * b + a * c + b * c > 2 * n
    if mode == "only-two-part":
        return a == 0
    raise RuntimeError("unknown shape-restriction mode %r" % (mode,))


def build_shape_restricted(solver_api, n, mode):
    """The committed encoder with the split clauses restricted by shape."""
    CNF, IDPool, _Solver, engine = solver_api
    pool = IDPool()
    cnf = CNF()
    evens = engine.even_masks(n)
    full = (1 << n) - 1

    def z(colour, mask):
        return pool.id(("z", colour, mask))

    for colour in range(3):
        cnf.append([z(colour, 0)])
        cnf.append([z(colour, full)])
        for mask in evens:
            if mask.bit_count() < 4:
                continue
            vertices = tuple(v for v in range(n) if mask >> v & 1)
            for pivot in vertices:
                terms = []
                for other in vertices:
                    if other == pivot:
                        continue
                    edge_mask = (1 << pivot) | (1 << other)
                    rest = mask ^ edge_mask
                    term = pool.id(("term", colour, mask, edge_mask))
                    engine.add_iff_and(cnf, term, z(colour, edge_mask),
                                       z(colour, rest))
                    terms.append(term)
                cnf.append([-z(colour, mask)] + terms)
                engine.add_zero_forbids_unique(cnf, z(colour, mask), terms)

    kept = 0
    dropped_shapes = set()
    for masks in colour_masks(n):
        shape = tuple(sorted(mask.bit_count() for mask in masks))
        if kept_shape(shape, n, mode):
            cnf.append([-z(colour, masks[colour]) for colour in range(3)])
            kept += 1
        else:
            dropped_shapes.add(shape)
    return pool, cnf, z, kept, sorted(dropped_shapes)


def symmetry_branches(solver_api, n, z):
    """The committed engine's exhaustive symmetry branches, verbatim."""
    _CNF, _IDPool, _Solver, engine = solver_api
    base = engine.edge_assumptions(z, 0, engine.canonical_matching(n))
    types = tuple(engine.integer_partitions(n // 2))
    coincident = (1,) * (n // 2)
    branches = []
    for cycle_type in types:
        first = engine.edge_assumptions(
            z, 1, engine.matching_of_cycle_type(n, cycle_type))
        if cycle_type != coincident:
            branches.append((str(cycle_type), base + first))
            continue
        for third_type in types:
            third = engine.edge_assumptions(
                z, 2, engine.matching_of_cycle_type(n, third_type))
            branches.append(("%s; colour2=%s" % (cycle_type, third_type),
                             base + first + third))
    return branches


def audit_countermodel(solver_api, n, z, positive, mode):
    """Independently re-audit a SAT assignment and read off its live shapes."""
    _CNF, _IDPool, _Solver, engine = solver_api
    full = (1 << n) - 1
    families = tuple(frozenset(mask for mask in engine.even_masks(n)
                               if z(colour, mask) in positive)
                     for colour in range(3))
    for colour, family in enumerate(families):
        require(0 in family and full in family,
                "countermodel audit (n=%d mode=%s): a unit z_%d is false"
                % (n, mode, colour))
        for mask in engine.even_masks(n):
            if mask.bit_count() < 4:
                continue
            vertices = [v for v in range(n) if mask >> v & 1]
            for pivot in vertices:
                count = sum(((1 << pivot) | (1 << other)) in family
                            and (mask ^ (1 << pivot) ^ (1 << other)) in family
                            for other in vertices if other != pivot)
                if mask in family:
                    require(count >= 1,
                            "countermodel audit (n=%d mode=%s): a feasible set "
                            "has no feasible pivot term" % (n, mode))
                else:
                    require(count != 1,
                            "countermodel audit (n=%d mode=%s): an infeasible "
                            "set has exactly one feasible pivot term"
                            % (n, mode))
    live_shapes = {}
    for masks in colour_masks(n):
        if all(masks[colour] in families[colour] for colour in range(3)):
            shape = tuple(sorted(mask.bit_count() for mask in masks))
            require(not kept_shape(shape, n, mode),
                    "countermodel audit (n=%d mode=%s): a KEPT split clause is "
                    "violated by the model" % (n, mode))
            live_shapes[shape] = live_shapes.get(shape, 0) + 1
    return families, live_shapes


def run_shape_restricted(solver_api, n, mode, expected):
    """Solve every symmetry branch; return the verdict and the audit.

    `expected` is the recorded verdict this run must reproduce; None
    means there is no recorded expectation and the verdict is REPORTED
    without being asserted (used for the unresolved n = 10 instance,
    which the note refuses to prejudge).  The internal consistency
    audits -- branch exhaustion on UNSAT, the countermodel re-audit on
    SAT -- run either way.
    """
    _CNF, _IDPool, Solver, _engine = solver_api
    pool, cnf, z, kept, dropped = build_shape_restricted(solver_api, n, mode)
    branches = symmetry_branches(solver_api, n, z)
    verdicts = []
    live_shapes = None
    model_hash = None
    with Solver(name="cadical195", bootstrap_with=cnf) as solver:
        for label, assumptions in branches:
            satisfiable = solver.solve(assumptions=assumptions)
            verdicts.append((label, satisfiable))
            if satisfiable:
                positive = {literal for literal in solver.get_model()
                            if literal > 0}
                families, live_shapes = audit_countermodel(
                    solver_api, n, z, positive, mode)
                model_hash = content_hash(
                    [sorted(family) for family in families])
                break
    verdict = "SAT" if any(flag for _label, flag in verdicts) else "UNSAT"
    if expected is not None:
        require(verdict == expected,
                "shape-restricted census: n=%d mode=%s returned %s, not the "
                "recorded %s" % (n, mode, verdict, expected))
    if verdict == "UNSAT":
        require(len(verdicts) == len(branches),
                "shape-restricted census: n=%d mode=%s did not exhaust its "
                "symmetry branches" % (n, mode))
    else:
        require(live_shapes,
                "shape-restricted census: n=%d mode=%s is SAT but its model "
                "has no live split at all" % (n, mode))
        for shape in live_shapes:
            require(shape in set(dropped),
                    "shape-restricted census: n=%d mode=%s has a model whose "
                    "live shape is not one of the dropped shapes" % (n, mode))
    return {
        "n": n,
        "mode": mode,
        "verdict": verdict,
        "variables": pool.top,
        "clauses": len(cnf.clauses),
        "split_clauses_kept": kept,
        "dropped_shapes": [list(shape) for shape in dropped],
        "branches": len(branches),
        "branches_solved": len(verdicts),
        "live_shapes_of_the_model": (
            {str(list(shape)): count
             for shape, count in sorted(live_shapes.items())}
            if live_shapes else None),
        "model_hash": model_hash,
    }


def section_sat_census(solver_api, attempt_n10):
    _CNF, _IDPool, _Solver, engine = solver_api
    encoder = {}
    for n in (6, 8):
        pool, cnf, z_full, kept, dropped = build_shape_restricted(
            solver_api, n, "full")
        reference_pool, reference_cnf, _ref_z = engine.build(n)
        mine = sorted(tuple(sorted(clause)) for clause in cnf.clauses)
        theirs = sorted(tuple(sorted(clause))
                        for clause in reference_cnf.clauses)
        require(mine == theirs,
                "the unrestricted encoder does not reproduce the committed "
                "engine's CNF at n=%d clause for clause" % n)
        require((pool.top, len(cnf.clauses))
                == (reference_pool.top, len(reference_cnf.clauses)),
                "the unrestricted encoder disagrees with the committed "
                "engine's variable/clause counts at n=%d" % n)
        published_vars, published_clauses, published_branches = \
            PUBLISHED_ENGINE_COUNTS[n]
        require((pool.top, len(cnf.clauses)) == (published_vars,
                                                 published_clauses),
                "the unrestricted encoder disagrees with the counts published "
                "in proofs/diagonal-hafnian-recurrence-obstruction.md at n=%d "
                "(%d vars, %d clauses)" % (n, pool.top, len(cnf.clauses)))
        branch_count = len(symmetry_branches(solver_api, n, z_full))
        require(branch_count == published_branches,
                "the symmetry branch count at n=%d disagrees with the "
                "committed proof" % n)
        require(dropped == [],
                "the unrestricted mode dropped a shape at n=%d" % n)
        encoder[n] = {"variables": pool.top, "clauses": len(cnf.clauses),
                      "split_clauses": kept, "branches": branch_count}

    runs = [
        run_shape_restricted(solver_api, 6, "full", "UNSAT"),
        run_shape_restricted(solver_api, 6, "drop-0-2", "SAT"),
        run_shape_restricted(solver_api, 6, "only-two-part", "SAT"),
        run_shape_restricted(solver_api, 8, "drop-0-2", "UNSAT"),
        run_shape_restricted(solver_api, 8, "drop-exceptional", "SAT"),
        run_shape_restricted(solver_api, 8, "only-two-part", "SAT"),
    ]
    if attempt_n10:
        # The n = 10 instance is UNRESOLVED: no expectation is recorded,
        # so the verdict is reported without being asserted.
        runs.append(run_shape_restricted(solver_api, 10, "drop-0-2", None))

    by_key = {(run["n"], run["mode"]): run for run in runs}
    require(by_key[(8, "drop-0-2")]["verdict"] == "UNSAT",
            "the new n=8 theorem (dropping the shape (0,2,6) is UNSAT) does "
            "not hold")
    require(by_key[(8, "drop-exceptional")]["verdict"] == "SAT",
            "dropping both X <= 2N shapes at n=8 is not SAT, so the C4'/C5' "
            "improvement would not be load-bearing")
    for key in ((6, "only-two-part"), (8, "only-two-part")):
        require(by_key[key]["verdict"] == "SAT",
                "the two-part fragment at n=%d is not SAT, contradicting the "
                "D(n) model" % key[0])
    return {
        "encoder": encoder,
        "runs": runs,
        "n10_attempted": bool(attempt_n10),
        "n10_status": ("attempted" if attempt_n10
                       else "UNRESOLVED: not attempted (opt-in --n10)"),
    }


# ============================================================== ledger


def audit(attempt_n10=False, require_solver=False):
    pencil = section_pencil_identity()
    two_colour = section_two_colour()
    construction = section_hamiltonian_construction(24)
    families = section_hamiltonian_hafnians(16, 12)
    two_part_control = section_two_part_control()
    k4_blocks = section_k4_blocks()
    diag = section_diag_infinity([record["n"] for record in families
                                  if "live_splits" in record])
    pencil_guard = section_pencil_guard(6, 5)
    u2 = section_u2()
    composition = section_composition()

    ledger = {
        "pencil_identity": pencil,
        "diag_infinity": diag,
        "pencil_guard": pencil_guard,
        "two_colour": two_colour,
        "hamiltonian_construction": construction,
        "hamiltonian_families": families,
        "two_part_control": two_part_control,
        "k4_block_families": k4_blocks,
        "lemma_u2": u2,
        "composition": composition,
        "proved": (
            "the pencil identity (a polynomial identity, hand proof in the "
            "note, verified on nonvacuous instances at n = 4,6,8); the "
            "two-colour realization by the alternating 2k-cycle at every k "
            "(verified k = 2..6, hand proof uniform in k); the "
            "Hamiltonian-triple lemma, whence D(n) kills every split with an "
            "empty part at every even n (hand proof uniform in n, verified "
            "n = 4..24 for the construction and n = 4..16 for the hafnians); "
            "Lemma U2 and the blocked pair-deletion induction"
        ),
        "not_proved": (
            "DIAG-infinity -- the TERMWISE condition T(k) is insoluble for "
            "every k >= 3 -- is proved only for k = 3,4,5, by the cited SAT "
            "theorem of proofs/diagonal-hafnian-recurrence-obstruction.md, "
            "and is CONJECTURED for k >= 6.  The SUMMED pencil equation P(k) "
            "is NOT a target at all: it is soluble for every k >= 2 (the "
            "alternating 2k-cycle over Q(zeta_2k), verified k = 2..6, and "
            "rational solutions at k = 2,3), so no proof can run through "
            "pencil insolubility.  The n = 10 shape-restricted instance is "
            "UNRESOLVED.  Krenn's conjecture remains open"
        ),
        "scope": (
            "everything here is about DIAGONAL packets: symmetric "
            "zero-diagonal scalar edge matrices W_0,W_1,W_2, which is the "
            "shadow an exact ternary source induces through Theorem B of "
            "notes/exact-source-live-split-forcing.md.  Nothing here supplies "
            "a live split at N >= 12, and nothing here improves Theorem C of "
            "notes/good-crossing-matching-forcing.md: the composition at "
            "N = 8 yields a good crossing PAIR, which is strictly weaker than "
            "a nonzero crossing matching all of whose crossing edges are good"
        ),
    }
    digest = content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "diagonal termwise census and pencil guard ledger changed")

    solver_api, reason = import_solver()
    if solver_api is None:
        if require_solver:
            raise SystemExit(
                "python-sat is required; run with `uv run --with python-sat "
                "python ...` (import failed: %s)" % reason)
        sat_ledger = {"status": "SKIPPED", "reason": reason}
        sat_digest = None
    else:
        sat_ledger = section_sat_census(solver_api, attempt_n10)
        sat_ledger["status"] = "RUN"
        sat_digest = content_hash(sat_ledger)
        if EXPECTED_SAT_LEDGER_SHA256 != "TO_BE_FROZEN" and not attempt_n10:
            require(sat_digest == EXPECTED_SAT_LEDGER_SHA256,
                    "shape-restricted SAT census ledger changed")
    return ledger, digest, sat_ledger, sat_digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n10", action="store_true",
                        help="attempt the unresolved n=10 drop-(0,2,8) "
                             "instance (may not terminate)")
    parser.add_argument("--require-solver", action="store_true",
                        help="fail, as the committed engine does, when PySAT "
                             "is unavailable instead of skipping section S")
    arguments = parser.parse_args()
    ledger, digest, sat_ledger, sat_digest = audit(arguments.n10,
                                                   arguments.require_solver)

    print("diagonal termwise census and pencil guard: PASS (exact)")
    pencil = ledger["pencil_identity"]
    print("pencil identity: %d instances at n=%s (%d of them over Fractions), "
          "%d mixed monomials and %d nonzero split terms in total; every "
          "instance survives the drop-one-term sharpness probe"
          % (pencil["instances"], pencil["orders"],
             pencil["fractional_instances"], pencil["total_mixed_monomials"],
             pencil["total_nonzero_split_terms"]))
    diag = ledger["diag_infinity"]
    print("DIAG-infinity: T(2) => P(2) on all %d termwise-dead k=2 packets, "
          "and the empty-part implication on D(n) for n=%s; T(k) is insoluble "
          "at k=%s by the cited SAT theorem and conjectured insoluble for "
          "k >= 6"
          % (len(diag["termwise_packets_at_k2"]),
             [record["n"] for record in diag["empty_part_implication"]],
             [n // 2 for n in diag["termwise_insoluble_orders"]]))
    for witness in diag["witnesses"]:
        print("  rational P(k) solution %s: haf(pencil) = x_0^k+x_1^k+x_2^k "
              "with %d live splits, cancelling exponents %s -- so P(k) does "
              "NOT imply T(k)"
              % (witness["label"], witness["live_splits"],
                 list(witness["cancelling_exponents"])))
    guard = ledger["pencil_guard"]
    print("pencil GUARD (the summed form is soluble at every k): the "
          "alternating 2k-cycle over Q(zeta_2k) solves P(k) for k=%s; live "
          "splits %s -- so P(k) obstructs nothing and only T(k) can"
          % (guard["orders"],
             {record["k"]: record.get("live_splits", "not counted")
              for record in guard["detail"]}))
    two_colour = ledger["two_colour"]
    print("two colours: the alternating 2k-cycle solves haf(xW_0+yW_1) = "
          "x^k+y^k and kills every empty-part split for k=%s (each cycle has "
          "exactly two perfect matchings)" % two_colour["orders"])
    construction = ledger["hamiltonian_construction"]
    print("Hamiltonian triples D(n): constructed and verified for n=%s; all "
          "three unions are single Hamiltonian cycles at every order"
          % [record["n"] for record in construction])
    print("D(n) hafnians: anchors (1,1,1), %d live empty-part splits over %d "
          "scanned, shape (0,2,n-2) live %d, C_0 n C_1 n C_2 empty, for n=%s"
          % (sum(record["two_part_live"] for record in ledger["hamiltonian_families"]),
             sum(record["two_part_examined"] for record in ledger["hamiltonian_families"]),
             sum(record["shape_0_2_live"] for record in ledger["hamiltonian_families"]),
             [record["n"] for record in ledger["hamiltonian_families"]]))
    for record in ledger["hamiltonian_families"]:
        if "live_shapes" in record:
            print("    n=%2d live shapes %s" % (record["n"],
                                                record["live_shapes"] or "NONE"))
    control = ledger["two_part_control"]
    print("empty-part scan control: %d live of %d scanned on the designed "
          "four-site packet, the designed split found" % (control["live"],
                                                          control["examined"]))
    for record in ledger["k4_block_families"]:
        print("  K_4 blocks at n=%d: %d live empty-part splits (ordered "
              "colour pairs: each split is counted twice, as (S,a,b) and as "
              "(V\\S,b,a), so this is twice the (0,.,.) shape counts), none "
              "of shape (0,2,n-2); live shapes %s"
              % (record["n"], record["two_part_live"], record["live_shapes"]))
    u2 = ledger["lemma_u2"]
    control = u2["deadness_control"]
    print("Lemma U2 deadness control: verdict %s on the designed n=6 packet "
          "(%d live empty-part entries, designed split found; a same-mask "
          "scan would report DEAD: %d masks live in two colours)"
          % ("DEAD" if control["dead_verdict"] else "LIVE", control["live"],
             control["same_mask_live_masks"]))
    for census in u2["censuses"]:
        print("Lemma U2 %s: %d packets, %d satisfy empty-part deadness, %d of "
              "those have a co-support overlap (DISCLOSED vacuity if 0), %d "
              "violations, %d contrapositive instances"
              % (census["label"], census["packets_examined"],
                 census["dead_packets"], census["u2_nonvacuous_packets"],
                 census["u2_violations"], census["contrapositive_instances"]))
    composition = ledger["composition"]
    print("composition: N=8 shapes with X > 3N/2 are %s (C5' leaves %s; the "
          "committed C5 additionally kept %s), verified to N=%d"
          % (composition["N8_shapes_with_a_forced_good_crossing_pair"],
             composition["N8_improved_C5prime"],
             composition["N8_committed_C5"], composition["max_order"]))
    print("sha256:", digest)

    if sat_ledger["status"] == "SKIPPED":
        print("shape-restricted SAT census: SKIPPED -- %s" % sat_ledger["reason"])
        print("  the census verdicts (n=6 UNSAT, n=6 drop-(0,2,4) SAT, n=8 "
              "drop-(0,2,6) UNSAT, n=8 drop-both SAT) are NOT ESTABLISHED in "
              "this run; they require python-sat.  Re-run with a solver, or "
              "with --require-solver to make this a hard failure.")
        print("  the N=8 composition of section G is therefore CONDITIONAL on "
              "that census in this run.")
        return
    for n, counts in sorted(sat_ledger["encoder"].items()):
        print("encoder at n=%d reproduces the committed engine clause for "
              "clause: %d vars, %d clauses, %d branches"
              % (n, counts["variables"], counts["clauses"], counts["branches"]))
    for run in sat_ledger["runs"]:
        print("  n=%2d mode=%-16s %-5s vars=%d clauses=%d kept=%d dropped=%s "
              "branches=%d live shapes of the model %s"
              % (run["n"], run["mode"], run["verdict"], run["variables"],
                 run["clauses"], run["split_clauses_kept"],
                 run["dropped_shapes"], run["branches"],
                 run["live_shapes_of_the_model"]))
    print("  n=10: %s" % sat_ledger["n10_status"])
    print("sat sha256:", sat_digest)


if __name__ == "__main__":
    main()

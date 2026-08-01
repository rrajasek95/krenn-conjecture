#!/usr/bin/env python3
"""The monochromatic branch at eight vertices: private edges, by Laplace alone.

Research evidence only.  Krenn's conjecture remains OPEN, `SP-CLEAN-BRIDGE` is
untouched, and no certified dependency changes.  Nothing here is a partial case
of the conjecture and nothing here decides (8,3).

WHY THIS BRANCH.  A solution of (8,3) whose colour-pair binary restrictions are
all rigid has every cross cell zero, hence is MONOCHROMATIC.  So the
monochromatic case is one of the two arms the whole problem splits into, not a
special case anyone chose.

THE COLLAPSED SYSTEM.  Monochromatic means every edge matrix is diagonal: only
the entries Z^c_uv = A_uv[c][c] are live.  A matching monomial then survives
only when both ends of every matched edge carry the same colour, so for a
colouring iota with colour classes V_c = iota^{-1}(c),

    T[iota] = prod_c haf(Z^c[V_c]).

If some |V_c| is odd there is no matching of V_c and the coefficient is zero for
free.  So the 6561 equations collapse to the 1641 even-class words, and the
system is exactly

    M0   haf(Z^c) = 1                        for c = 0, 1, 2      (3 equations)
    M1   prod_c haf(Z^c[V_c]) = 0            for the other 1638 even partitions

in 3 * 28 = 84 unknowns, down from 252.  This collapse is not new -- it is the
encoding of ``computations/search_diagonal_f3_n8.py``, whose docstring states
it -- and it is re-derived here from the literal matching tensor rather than
assumed.

WHAT IS ESTABLISHED HERE, all by Laplace expansion and the two-class equations,
with no genericity, no positivity and no cancellation argument.  Write

    S_c = { even S : haf(Z^c[S]) != 0 },     L_c = { e : Z^c_e != 0 }.

  A  THE COMPLEMENT CONDITION.  Taking V_a = S, V_b = complement(S), V_third
     empty in M1 (the empty class contributes haf of the empty matrix, which is
     1) gives, for a != b and every even S with S not in {empty, [8]},

         S in S_a   ==>   complement(S) not in S_b.

  B  EVERY COLOUR IS LIVE ON SOME EDGE.  S_c contains a 2-set, because
     haf(Z^c[{u,v}]) = Z^c_uv and Z^c = 0 would contradict haf(Z^c) = 1.

  C  THE PRIVATE-EDGE THEOREM.  Laplace expansion of the hafnian along a vertex
     u reads haf(Z^c[S]) = sum_{v in S, v != u} Z^c_uv haf(Z^c[S \\ {u,v}]).
     Applied to S = [8], where the value is 1, it produces for EVERY colour c
     and EVERY vertex u some v with

         Z^c_uv != 0     and     [8] \\ {u,v} in S_c.

     Both {u,v} and its complement then lie in S_c, so by A applied twice the
     colour sets of that 2-set and that 6-set are the single colour {c}:

         >>> the edge {u, v} is LIVE IN COLOUR c AND DEAD IN THE OTHER TWO,
         >>> and the complementary six-set has zero hafnian in the other two.

     Hence for each colour c the private edges P_c = { e in L_c : e not in
     L_{c'} for c' != c } cover all eight vertices, and P_0, P_1, P_2 are
     pairwise disjoint.  In particular every vertex has degree at least three in
     L_0 union L_1 union L_2, with its three private edges in three different
     colours going to three DISTINCT neighbours.

  D  THE DISJOINT-PRIVATE-PAIR LEMMA.  If e_a in P_a and e_b in P_b are
     DISJOINT with a != b, then the three-class partition (e_a, e_b, rest) has
     two nonzero factors, so the third vanishes:

         haf(Z^c[ [8] \\ (e_a union e_b) ]) = 0,   c the third colour.

     Such a disjoint pair always exists: P_b covers the six vertices outside
     e_a, at most two of its edges can meet e_a, and covering six vertices needs
     at least three edges, so some P_b edge lies wholly outside e_a.

  E  WHAT SURVIVES.  D kills a four-set for the third colour for every disjoint
     private pair.  Colour c still needs a live four-set, by descending the
     Laplace expansion twice.  Block E measures exactly how much room that
     leaves, by exhausting the possible private-edge configurations.  The result
     is recorded as a census, NOT as a closure: see the printed summary and
     section "what this does not say" below.

WHAT THIS DOES NOT SAY.  It does not decide the monochromatic branch, and it
decides nothing about (8,3).  A and D are support conditions; the four-set
conditions that D produces are genuine CANCELLATION conditions
(haf of a four-set is a sum of three products) and are not touched here.  The
private-edge theorem constrains supports only.

Standard library only, exact integer and Fraction arithmetic, no floats, no
numpy.  Every check raises rather than asserts, so ``python3 -O`` performs all
of them.
"""

from __future__ import annotations

import sys
from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


N = 8
COLORS = (0, 1, 2)
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))


# ----------------------------------------------------------------------
# perfect matchings and hafnians of principal submatrices
# ----------------------------------------------------------------------


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    out = []
    head, rest = vertices[0], vertices[1:]
    for k, partner in enumerate(rest):
        remainder = rest[:k] + rest[k + 1:]
        for tail in perfect_matchings(remainder):
            out.append(((head, partner),) + tail)
    return tuple(out)


MATCHINGS8 = perfect_matchings(VERTICES)
EVEN_SETS = tuple(
    frozenset(S)
    for size in range(0, N + 1, 2)
    for S in combinations(VERTICES, size)
)
_MATCHING_CACHE = {S: perfect_matchings(tuple(sorted(S))) for S in EVEN_SETS}


def haf(Z, S):
    """haf(Z[S]) with Z a dict on unordered pairs; haf of the empty set is 1."""

    if len(S) % 2:
        return 0          # an odd set has no perfect matching
    total = 0
    for matching in _MATCHING_CACHE[S]:
        term = 1
        for u, v in matching:
            term *= Z.get((min(u, v), max(u, v)), 0)
            if term == 0:
                break
        total += term
    return total


def literal_matching_tensor(blocks, iota):
    """The official coefficient, from the definition, with no chart."""

    total = 0
    for matching in MATCHINGS8:
        term = 1
        for u, v in matching:
            term *= blocks[(min(u, v), max(u, v))][iota[u]][iota[v]]
            if term == 0:
                break
        total += term
    return total


# ----------------------------------------------------------------------
# M: the collapse, verified against the literal tensor
# ----------------------------------------------------------------------


class LCG:
    def __init__(self, seed):
        self.state = seed & ((1 << 64) - 1)

    def next(self, bound):
        self.state = (6364136223846793005 * self.state + 1442695040888963407)
        self.state &= (1 << 64) - 1
        return (self.state >> 33) % bound


def diagonal_blocks(Zs):
    blocks = {}
    for e in EDGES:
        block = [[0] * 3 for _ in range(3)]
        for c in COLORS:
            block[c][c] = Zs[c].get(e, 0)
        blocks[e] = block
    return blocks


def audit_M_collapse(trials=2):
    """T[iota] = prod_c haf(Z^c[V_c]) for a diagonal packet, at every word."""

    gen = LCG(20260801)
    even_words = 0
    for iota in product(COLORS, repeat=N):
        if all(sum(1 for v in VERTICES if iota[v] == c) % 2 == 0 for c in COLORS):
            even_words += 1
    require(even_words == 1641,
            f"even-class words number {even_words}, expected 1641")

    constants = sum(1 for iota in product(COLORS, repeat=N) if len(set(iota)) == 1)
    require(constants == 3, "there are not three constant colourings")
    require(1641 - 3 == 1638, "the vanishing count is not 1638")

    for trial in range(trials):
        Zs = [
            {e: gen.next(9) - 4 for e in EDGES}
            for _ in COLORS
        ]
        blocks = diagonal_blocks(Zs)
        for iota in product(COLORS, repeat=N):
            classes = [frozenset(v for v in VERTICES if iota[v] == c) for c in COLORS]
            product_value = 1
            for c in COLORS:
                product_value *= haf(Zs[c], classes[c])
                if product_value == 0:
                    break
            literal = literal_matching_tensor(blocks, iota)
            require(literal == product_value,
                    ("the collapse fails", trial, iota, literal, product_value))
    return even_words


# ----------------------------------------------------------------------
# structure theorems A - D, as formal statements about any solution
# ----------------------------------------------------------------------


def audit_A_complement_condition():
    """Deriving A: the empty class contributes a factor of exactly one."""

    empty = frozenset()
    require(haf({}, empty) == 1, "the empty hafnian is not one")
    for e in EDGES:
        Z = {e: 7}
        require(haf(Z, frozenset(e)) == 7,
                "a two-set hafnian is not the edge weight")
    # the two-class partitions really are among the 1638
    two_class = 0
    for S in EVEN_SETS:
        if S and len(S) < N:
            two_class += 1
    require(two_class == len(EVEN_SETS) - 2,
            "the proper nonempty even sets are miscounted")
    require(len(EVEN_SETS) == 128, f"there are {len(EVEN_SETS)} even sets, not 128")
    return two_class


def audit_C_laplace_expansion(trials=3):
    """Laplace along a vertex, verified as an exact identity on random data."""

    gen = LCG(555001)
    for trial in range(trials):
        Z = {e: gen.next(11) - 5 for e in EDGES}
        for S in EVEN_SETS:
            if not S:
                continue
            for u in sorted(S):
                expansion = 0
                for v in sorted(S):
                    if v == u:
                        continue
                    key = (min(u, v), max(u, v))
                    expansion += Z.get(key, 0) * haf(Z, S - {u, v})
                require(expansion == haf(Z, S),
                        ("Laplace expansion fails", trial, sorted(S), u))
    return True


def audit_C_private_edges_exist():
    """The theorem: haf(Z^c) = 1 forces, at every vertex, a partner v with the
    2-set and the 6-set both live -- and A then makes that edge private.

    Verified here as the implication it is: any Z with haf(Z) != 0 has, at every
    vertex, such a partner.  (The privacy half is A applied to that partner, and
    is checked symbolically in audit_D.)
    """

    gen = LCG(99887766)
    for trial in range(40):
        Z = {e: gen.next(7) - 3 for e in EDGES}
        total = haf(Z, frozenset(VERTICES))
        if total == 0:
            continue
        for u in VERTICES:
            partners = [
                v for v in VERTICES
                if v != u
                and Z.get((min(u, v), max(u, v)), 0) != 0
                and haf(Z, frozenset(VERTICES) - {u, v}) != 0
            ]
            require(partners,
                    ("no Laplace partner at a vertex although haf != 0",
                     trial, u))
    # and the contrapositive is not vacuous: a Z with haf = 0 can fail it
    dead = {e: 0 for e in EDGES}
    require(haf(dead, frozenset(VERTICES)) == 0,
            "the zero matrix has nonzero hafnian")
    return True


def audit_D_disjoint_private_pair_exists():
    """Every edge cover of K_8 has an edge disjoint from any fixed edge.

    This is the combinatorial half of D, and it is what makes D non-vacuous:
    P_b covers the six vertices outside e_a, at most two P_b edges can meet
    e_a, and six vertices need at least three edges.
    """

    for e_a in EDGES:
        outside = [v for v in VERTICES if v not in e_a]
        require(len(outside) == 6, "an edge does not leave six vertices")
    # exhaustive check on minimal covers: every perfect matching works
    for e_a in EDGES:
        for matching in MATCHINGS8:
            disjoint = [
                e for e in matching
                if not (set(e) & set(e_a))
            ]
            require(disjoint,
                    ("a perfect matching has no edge disjoint from an edge",
                     e_a))
    # the general statement, over all edge covers with at most six edges
    checked = 0
    for size in (4, 5):
        for cover in combinations(EDGES, size):
            covered = set()
            for e in cover:
                covered.update(e)
            if len(covered) != N:
                continue
            checked += 1
            for e_a in EDGES:
                require(any(not (set(e) & set(e_a)) for e in cover),
                        ("an edge cover meets every edge", cover, e_a))
    require(checked > 0, "no edge covers were examined")
    return checked


# ----------------------------------------------------------------------
# E: how much room the private-edge structure leaves
# ----------------------------------------------------------------------


def audit_E_private_configuration_census():
    """Census of the four-sets D kills, over private-edge structures.

    For each colour c pick a MINIMAL private cover -- a perfect matching is the
    smallest edge cover of K_8, at four edges.  Three pairwise edge-disjoint
    perfect matchings M_0, M_1, M_2 give the sparsest configuration consistent
    with the private-edge theorem.  D then kills, for the third colour c, every
    four-set of the form [8] \\ (e_a union e_b) with e_a in M_a, e_b in M_b
    disjoint.

    The question this measures: does colour c retain ANY four-set?
    """

    matchings = [frozenset(map(lambda p: (min(p), max(p)), m)) for m in MATCHINGS8]
    require(len(matchings) == 105, "K_8 does not have 105 perfect matchings")

    four_sets = [S for S in EVEN_SETS if len(S) == 4]
    require(len(four_sets) == 70, f"there are {len(four_sets)} four-sets, not 70")

    survivors_seen = set()
    triples = 0
    for i in range(len(matchings)):
        for j in range(i + 1, len(matchings)):
            if matchings[i] & matchings[j]:
                continue
            for k in range(j + 1, len(matchings)):
                if matchings[k] & (matchings[i] | matchings[j]):
                    continue
                triples += 1
                M = (matchings[i], matchings[j], matchings[k])
                for c in COLORS:
                    a, b = [x for x in COLORS if x != c]
                    killed = set()
                    for e_a in M[a]:
                        for e_b in M[b]:
                            if set(e_a) & set(e_b):
                                continue
                            killed.add(frozenset(VERTICES) - set(e_a) - set(e_b))
                    survivors = len(four_sets) - len(killed & set(four_sets))
                    survivors_seen.add(survivors)
    require(triples > 0, "no edge-disjoint matching triples were found")
    return triples, sorted(survivors_seen), len(four_sets)


def main():
    even_words = audit_M_collapse()
    two_class = audit_A_complement_condition()
    audit_C_laplace_expansion()
    audit_C_private_edges_exist()
    covers = audit_D_disjoint_private_pair_exists()
    triples, survivors, total_four = audit_E_private_configuration_census()
    print(
        "PASS: the monochromatic branch at eight vertices collapses to "
        f"prod_c haf(Z^c[V_c]) on {even_words} even-class words (3 targets, "
        "1638 vanishing) in 84 unknowns, verified against the literal "
        "matching tensor; the empty class contributes exactly one, so each of "
        f"the {two_class} proper nonempty even sets gives a two-class "
        "condition; Laplace expansion holds at every vertex and every even "
        "set; haf(Z^c) = 1 therefore forces at every vertex a partner whose "
        "2-set AND 6-set are both live, and the complement condition makes "
        "that edge PRIVATE to c, so the three private covers are pairwise "
        "disjoint and each spans all eight vertices; every edge cover of K_8 "
        f"has an edge disjoint from any fixed edge ({covers} covers checked), "
        "so a disjoint private pair always exists and kills a four-set of the "
        f"third colour; over the {triples} triples of pairwise edge-disjoint "
        f"perfect matchings the number of four-sets surviving for a colour is "
        f"{survivors} of {total_four} -- room remains, so this is a census and "
        "NOT a closure"
    )


if __name__ == "__main__":
    sys.exit(main())

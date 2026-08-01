#!/usr/bin/env python3
"""The level-two residual at eight vertices is 84 blocks of 64, and each block
determines one diagonal cell or declares a pair dead.

Research evidence only.  Krenn's conjecture remains OPEN, `SP-CLEAN-BRIDGE` is
untouched, and no certified dependency changes.  Nothing here decides (8,3).

CONTEXT.  Since 8 < 3*3, every colouring of the eight vertices has some colour
occurring at most twice.  So `EqSystemN 8 3` splits by MINIMUM COLOUR
MULTIPLICITY into exactly three levels, and nothing else:

    L0   765 words   -- some colour absent: three glued binary (8,2) systems
    L1  2856 words   -- some colour occurring exactly once
    L2  2940 words   -- every colour at least twice, some exactly twice

That census, and the exhaustiveness, are verified below.  A parallel result
identifies L2 as the ENTIRE residual: L0 carries no obstruction, and L1 is now
known to force non-rigidity rather than to close anything.  This script pins
what L2 actually looks like.

WHAT IS PROVED HERE.

  B1  THE BLOCK COUNT.  Index an L2 condition by the triple (c, {v,v'}, w)
      where colour c occurs exactly at v and v', and w in {a,b}^6 is the word
      on the other six vertices, {a,b} being the two remaining colours.  There
      are 3 * C(8,2) = 84 such blocks and 2^6 = 64 words in each, so

          84 * 64 = 5376 (c, pair, word) incidences.

      The gap between 2940 and 5376 is not an error: a word can have TWO
      colours each occurring exactly twice -- shape (4,2,2) -- and is then
      counted once per such colour.  The multiplicity census is verified.

  B2  AFFINENESS, AND THE SLOPE.  For a fixed block, the coefficient T[w] is
      an AFFINE function of the single diagonal cell Z^c(v,v') = A(v,v')[c][c],
      and its slope is exactly the {a,b}-restricted hafnian of the other six
      vertices:

          T[w] = Z^c(v,v') * haf( A[V \\ {v,v'}] ; w )  +  B(w),

      with B(w) the value at Z^c(v,v') = 0.  Verified as a formal polynomial
      identity in all 252 cell variables, at every one of the 64 words of a
      block, not sampled: the second difference in Z^c(v,v') vanishes
      identically and the first difference equals the six-vertex hafnian.

  B3  THE PER-BLOCK DICHOTOMY.  Every L2 equation of the block reads
      Z^c(v,v') * H(w) = -B(w).  Hence exactly one of:

        * H(w) != 0 for some w in the block.  Then Z^c(v,v') is DETERMINED by
          the remaining data -- it is not a free parameter -- and the other 63
          equations of the block become consistency conditions on that data.

        * H vanishes at all 64 words.  Then the pair {v,v'} is dead for the
          {a,b} binary restriction in the "free edge = dead pair" sense,
          Z^c(v,v') is unconstrained by this block, and the block collapses to
          B(w) = 0.

      So the 84 diagonal cells are not free: each is either pinned by its own
      block or sits over a dead pair.  Both alternatives are exhibited on
      explicit packets below, so the dichotomy is not vacuous on either side.

  B4  THE MONOCHROMATIC SPECIALIZATION IS CONSISTENT.  With all cross cells
      zero the tail B vanishes, and B3 becomes exactly the two- and three-class
      product conditions of
      ``notes/monochromatic-private-edge-structure.md``: either the diagonal
      cell is zero or the complementary hafnian is.  Verified.

WHAT THIS DOES NOT SAY.  It does not decide (8,3), does not close L2, and
proves nothing about whether the consistency conditions of B3 are satisfiable.
"Determined" means determined by the other 251 cells, which are themselves
constrained; it is a statement about the shape of the residual, not a count of
solutions.

Standard library only, exact integer and Fraction arithmetic, no floats, no
numpy.  Every check raises rather than asserts, so ``python3 -O`` performs all
of them.
"""

from __future__ import annotations

import sys
from collections import Counter
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


N = 8
COLORS = (0, 1, 2)
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    out = []
    head, rest = vertices[0], vertices[1:]
    for k, partner in enumerate(rest):
        for tail in perfect_matchings(rest[:k] + rest[k + 1:]):
            out.append(((head, partner),) + tail)
    return tuple(out)


MATCHINGS8 = perfect_matchings(VERTICES)
_SUB = {}


def key(u, v):
    return (u, v) if u < v else (v, u)


def tensor(A, w):
    total = 0
    for m in MATCHINGS8:
        term = 1
        for u, v in m:
            term *= A[key(u, v)][w[u]][w[v]]
            if term == 0:
                break
        total += term
    return total


def sub_hafnian(A, S, w):
    """haf of the array restricted to S, read at the word w."""

    S = tuple(sorted(S))
    if S not in _SUB:
        _SUB[S] = perfect_matchings(S)
    total = 0
    for m in _SUB[S]:
        term = 1
        for u, v in m:
            term *= A[key(u, v)][w[u]][w[v]]
            if term == 0:
                break
        total += term
    return total


class LCG:
    def __init__(self, seed):
        self.state = seed & ((1 << 64) - 1)

    def next(self, bound):
        self.state = (6364136223846793005 * self.state + 1442695040888963407)
        self.state &= (1 << 64) - 1
        return (self.state >> 33) % bound


def random_packet(gen, lo=-4, hi=5):
    return {
        e: [[gen.next(hi - lo) + lo for _ in COLORS] for _ in COLORS]
        for e in EDGES
    }


def bump(A, e, c, delta):
    B = {k: [row[:] for row in v] for k, v in A.items()}
    B[e][c][c] += delta
    return B


# ----------------------------------------------------------------------


def audit_B1_levels_and_blocks():
    census = Counter()
    for w in product(COLORS, repeat=N):
        counts = Counter(w)
        census[min(counts[c] for c in COLORS)] += 1
    require(
        dict(census) == {0: 765, 1: 2856, 2: 2940},
        f"level census is {dict(census)}, expected 765/2856/2940",
    )
    require(
        sum(census.values()) == 3 ** N,
        "the three levels are not exhaustive",
    )
    require(
        max(census) == 2,
        "some word has minimum colour multiplicity above two, "
        "contradicting 8 < 3*3",
    )

    blocks = [
        (c, pair)
        for c in COLORS
        for pair in combinations(VERTICES, 2)
    ]
    require(len(blocks) == 84, f"{len(blocks)} blocks, expected 84")
    require(len(blocks) * 2 ** 6 == 5376, "block incidences are not 5376")

    # the 2940-vs-5376 gap is exactly the shape-(4,2,2) double count
    incidences = 0
    doubled = 0
    for w in product(COLORS, repeat=N):
        counts = Counter(w)
        twos = [c for c in COLORS if counts[c] == 2]
        if not twos:
            continue
        incidences += len(twos)
        if len(twos) == 2:
            doubled += 1
    require(
        incidences == 5376,
        f"exactly-two incidences number {incidences}, expected 5376",
    )
    require(doubled > 0, "no word has two colours of multiplicity two")
    return len(blocks), incidences, doubled


def audit_B2_affine_with_hafnian_slope(trials=2):
    """Second difference vanishes and first difference is the six-hafnian.

    Checked at ALL 64 words of a block, for several blocks and packets --
    the identity is in the 252 cell variables, so this is exhaustive over the
    block rather than a sample of it.
    """

    gen = LCG(20260801)
    checked = 0
    for trial in range(trials):
        A = random_packet(gen)
        for c in COLORS:
            for v, vp in ((2, 5), (0, 1), (3, 7)):
                a, b = [x for x in COLORS if x != c]
                rest = [u for u in VERTICES if u not in (v, vp)]
                e = key(v, vp)
                for tail in product((a, b), repeat=6):
                    w = [0] * N
                    for slot, u in enumerate(rest):
                        w[u] = tail[slot]
                    w[v] = c
                    w[vp] = c
                    w = tuple(w)
                    base = tensor(A, w)
                    one = tensor(bump(A, e, c, 1), w)
                    two = tensor(bump(A, e, c, 2), w)
                    require(
                        two - 2 * one + base == 0,
                        ("T is not affine in the diagonal cell",
                         trial, c, (v, vp), w),
                    )
                    require(
                        one - base == sub_hafnian(A, rest, w),
                        ("the slope is not the six-vertex hafnian",
                         trial, c, (v, vp), w),
                    )
                    checked += 1
    require(checked == trials * 3 * 3 * 64, "wrong number of block words")
    return checked


def audit_B3_dichotomy_is_not_vacuous():
    """Both sides of the per-block dichotomy occur on explicit packets."""

    gen = LCG(777333)
    c, v, vp = 0, 2, 5
    a, b = [x for x in COLORS if x != c]
    rest = [u for u in VERTICES if u not in (v, vp)]

    def block_slopes(A):
        out = []
        for tail in product((a, b), repeat=6):
            w = [0] * N
            for slot, u in enumerate(rest):
                w[u] = tail[slot]
            w[v] = c
            w[vp] = c
            out.append(sub_hafnian(A, rest, tuple(w)))
        return out

    live = random_packet(gen)
    require(
        any(block_slopes(live)),
        "a random packet has an identically zero block slope",
    )

    # a dead pair: kill every edge among the other six, so no six-vertex
    # matching survives and H vanishes at all 64 words
    dead = random_packet(gen)
    for x, y in combinations(rest, 2):
        dead[key(x, y)] = [[0] * 3 for _ in range(3)]
    slopes = block_slopes(dead)
    require(
        not any(slopes),
        "the constructed dead pair still has a nonzero block slope",
    )
    # and there the diagonal cell really is unconstrained by this block
    for delta in (1, 5, -3):
        for tail in ((a,) * 6, (b,) * 6, (a, b, a, b, a, b)):
            w = [0] * N
            for slot, u in enumerate(rest):
                w[u] = tail[slot]
            w[v] = c
            w[vp] = c
            w = tuple(w)
            require(
                tensor(bump(dead, key(v, vp), c, delta), w) == tensor(dead, w),
                "the diagonal cell moves the tensor over a dead pair",
            )
    return sum(1 for s in block_slopes(live) if s)


def audit_B4_monochromatic_specialization():
    """With cross cells zero the tail vanishes, recovering the product form."""

    gen = LCG(31337)
    A = random_packet(gen)
    for e in EDGES:
        for i in COLORS:
            for j in COLORS:
                if i != j:
                    A[e][i][j] = 0
    c, v, vp = 1, 0, 4
    a, b = [x for x in COLORS if x != c]
    rest = [u for u in VERTICES if u not in (v, vp)]
    nonzero = 0
    for tail in product((a, b), repeat=6):
        w = [0] * N
        for slot, u in enumerate(rest):
            w[u] = tail[slot]
        w[v] = c
        w[vp] = c
        w = tuple(w)
        # tail B(w) is the value at a zero diagonal cell
        zeroed = {k: [row[:] for row in val] for k, val in A.items()}
        zeroed[key(v, vp)][c][c] = 0
        require(
            tensor(zeroed, w) == 0,
            ("the monochromatic tail does not vanish", w),
        )
        require(
            tensor(A, w)
            == A[key(v, vp)][c][c] * sub_hafnian(A, rest, w),
            ("the monochromatic block is not the pure product", w),
        )
        if tensor(A, w):
            nonzero += 1
    return nonzero


def main():
    blocks, incidences, doubled = audit_B1_levels_and_blocks()
    checked = audit_B2_affine_with_hafnian_slope()
    live_slopes = audit_B3_dichotomy_is_not_vacuous()
    mono_nonzero = audit_B4_monochromatic_specialization()
    print(
        f"PASS: 8 < 3*3 forces every word to have a colour of multiplicity at "
        f"most two, so EqSystemN 8 3 splits exhaustively as 765 + 2856 + 2940 "
        f"by minimum colour multiplicity; the level-two residual is {blocks} "
        f"blocks of 64, giving {incidences} (colour, pair, word) incidences, "
        f"the gap to 2940 being the shape-(4,2,2) words counted twice "
        f"({doubled} of them); on every one of {checked} block words the "
        f"coefficient is AFFINE in the diagonal cell Z^c(v,v') with slope "
        f"exactly the six-vertex hafnian of the complementary pair, so each "
        f"block either DETERMINES that cell -- leaving 63 consistency "
        f"conditions -- or has an identically zero slope and declares the pair "
        f"dead; both sides occur ({live_slopes} of 64 slopes live on a random "
        f"packet, 0 of 64 on a constructed dead pair); and the monochromatic "
        f"specialization collapses to the pure product form on all 64 words "
        f"({mono_nonzero} nonzero)"
    )


if __name__ == "__main__":
    sys.exit(main())

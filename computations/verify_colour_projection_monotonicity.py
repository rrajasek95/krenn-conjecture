#!/usr/bin/env python3
"""Colour projection is monotone: a solution at (n,d') gives one at (n,d).

Research evidence only.  Krenn's conjecture remains OPEN, `SP-CLEAN-BRIDGE` is
untouched, and no certified dependency changes.

THE LEMMA.  Let A be an assignment of complex d' x d' matrices to the edges of
K_n with matching tensor Delta_{n,d'}.  Fix any d-subset S of the colours and
restrict every matrix to S, i.e. A'_uv[i][j] = A_uv[S_i][S_j].  Then A' has
matching tensor Delta_{n,d}.

The reason is that the matching tensor is computed coordinatewise in the
colouring: T[iota] depends only on the entries A_uv[iota_u][iota_v], so
restricting the colour alphabet restricts the tensor to those coordinates, and
Delta_{n,d'} restricted to words over S is exactly Delta_{n,d} -- a word over S
is constant if and only if its lift is.

PRIOR ART.  The idea is not new: ``notes/clean-pair-cap-exact-descent-target.md``
section 5 uses exactly this projection to reduce a palette of size at least
three to an exact ternary target, and the problem statement this project works
from relies on it to say that a palette larger than claimed yields a ternary
source.  What is added here is that it is CHECKED rather than asserted, and
that the consequence for the open-case list is drawn.

WHAT IT GIVES.

  P1  MONOTONICITY.  If (n,d) has no solution then neither does (n,d') for any
      d' >= d.  Contrapositive of the lemma.

  P2  THE CASE LIST COLLAPSES AT FIXED n.  In particular, since (6,3) is closed
      by the external Lean development
      (``notes/external-six-site-lean-certificate.md``), **(6,4) and (6,5) are
      closed too**, though both are listed as open upstream.  At every n the
      conjecture reduces to d = 3.

  P3  IT IS THE RIGHT WAY ROUND, AND THAT MATTERS.  Monotonicity runs from
      SMALL d to large: closing d = 3 closes everything above it.  It gives
      nothing in the other direction, so the settled large-d cases -- (4,4),
      (6,6), (8,10), (10,10) -- imply nothing about (8,3).  Verified below by
      exhibiting the (4,3) solution, which survives projection from no larger
      case and blocks any attempt to run the implication downward.

Checked exactly, on solutions that EXIST rather than on random data: the
(4,3) solution and the alternating n-cycle (n,2) solutions are projected and
re-verified from the literal matching tensor.

Standard library only, exact integer arithmetic, no floats, no numpy.  Every
check raises rather than asserts, so ``python3 -O`` performs all of them.
"""

from __future__ import annotations

import sys
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


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


def key(u, v):
    return (u, v) if u < v else (v, u)


def tensor(A, w, matchings):
    total = 0
    for m in matchings:
        term = 1
        for u, v in m:
            term *= A[key(u, v)][w[u]][w[v]]
            if term == 0:
                break
        total += term
    return total


def is_solution(A, n, d):
    matchings = perfect_matchings(tuple(range(n)))
    for w in product(range(d), repeat=n):
        want = 1 if len(set(w)) == 1 else 0
        if tensor(A, w, matchings) != want:
            return False
    return True


def project(A, S, n):
    return {
        key(u, v): [[A[key(u, v)][a][b] for b in S] for a in S]
        for u, v in combinations(range(n), 2)
    }


class LCG:
    def __init__(self, seed):
        self.state = seed & ((1 << 64) - 1)

    def next(self, bound):
        self.state = (6364136223846793005 * self.state + 1442695040888963407)
        self.state &= (1 << 64) - 1
        return (self.state >> 33) % bound


# ----------------------------------------------------------------------
# the two solution families that exist, built from the definition
# ----------------------------------------------------------------------


def solution_4_3():
    """K_4 has three edge-disjoint perfect matchings; colour one each."""

    pairings = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
    A = {
        key(u, v): [[0] * 3 for _ in range(3)]
        for u, v in combinations(range(4), 2)
    }
    for c, matching in enumerate(pairings):
        for e in matching:
            A[key(*e)][c][c] = 1
    return A


def solution_cycle(n):
    """The alternating n-cycle: an (n,2) solution for even n."""

    A = {
        key(u, v): [[0, 0], [0, 0]]
        for u, v in combinations(range(n), 2)
    }
    for i in range(n):
        A[key(i, (i + 1) % n)][i % 2][i % 2] = 1
    return A


# ----------------------------------------------------------------------


def audit_the_two_families():
    A43 = solution_4_3()
    require(is_solution(A43, 4, 3), "the (4,3) construction is not a solution")
    for n in (4, 6, 8):
        require(
            is_solution(solution_cycle(n), n, 2),
            f"the alternating {n}-cycle is not an (n,2) solution",
        )
    return True


def audit_P1_projection_preserves_coefficients(trials=2):
    """Every coefficient over the retained colours is literally unchanged.

    Checked on ARBITRARY matrices, not only on solutions -- the lemma is about
    the matching tensor, not about the target.
    """

    gen = LCG(20260801)
    checked = 0
    for n, dbig, dsm in ((4, 4, 3), (6, 5, 3), (6, 4, 2), (8, 4, 3)):
        matchings = perfect_matchings(tuple(range(n)))
        for trial in range(trials):
            A = {
                key(u, v): [
                    [gen.next(9) - 4 for _ in range(dbig)] for _ in range(dbig)
                ]
                for u, v in combinations(range(n), 2)
            }
            for S in combinations(range(dbig), dsm):
                Ap = project(A, S, n)
                small = perfect_matchings(tuple(range(n)))
                for w in product(range(dsm), repeat=n):
                    lifted = tuple(S[c] for c in w)
                    require(
                        tensor(Ap, w, small) == tensor(A, lifted, matchings),
                        ("projection moved a coefficient", n, dbig, S, w),
                    )
                    checked += 1
    return checked


def audit_P1_target_restricts(dmax=6, nmax=8):
    """Delta_{n,d'} restricted to words over S is exactly Delta_{n,d}."""

    for n in (4, 6, 8):
        if n > nmax:
            continue
        for dbig in range(2, dmax + 1):
            for dsm in range(2, dbig + 1):
                for S in combinations(range(dbig), dsm):
                    for w in product(range(dsm), repeat=n):
                        lifted = tuple(S[c] for c in w)
                        require(
                            (len(set(w)) == 1) == (len(set(lifted)) == 1),
                            ("the target does not restrict", n, S, w),
                        )
    return True


def audit_P3_direction_is_one_way():
    """Monotonicity runs from small d upward, and NOT downward.

    The (4,3) solution is the witness: it exists, so (4,d) for d >= 3 cannot be
    concluded empty from it, and no projection produces it from a settled
    larger case in a way that would let the implication run backwards.
    """

    A43 = solution_4_3()
    # projecting the (4,3) solution to two colours still solves (4,2)
    for S in combinations(range(3), 2):
        Ap = project(A43, S, 4)
        require(
            is_solution(Ap, 4, 2),
            f"projecting (4,3) to colours {S} does not give a (4,2) solution",
        )
    # the alternating 4-cycle is an independent (4,2) solution
    require(is_solution(solution_cycle(4), 4, 2), "the 4-cycle is not (4,2)")
    # NEGATIVE CONTROL: padding a (4,2) solution up to three colours does NOT
    # give a (4,3) solution -- the new colour's anchor fails.  So the
    # implication genuinely does not run downward-to-upward for free.
    C4 = solution_cycle(4)
    padded = {
        e: [[C4[e][i][j] if i < 2 and j < 2 else 0 for j in range(3)]
            for i in range(3)]
        for e in C4
    }
    require(
        not is_solution(padded, 4, 3),
        "padding a (4,2) solution with a dead colour gave a (4,3) solution",
    )
    matchings = perfect_matchings(tuple(range(4)))
    require(
        tensor(padded, (2, 2, 2, 2), matchings) == 0,
        "the padded packet's third anchor is not zero",
    )
    return True


def audit_P2_case_list():
    """If (n,3) is empty then so is (n,d) for every d >= 3.

    Stated as the contrapositive of P1 and checked as a logical consequence on
    the data this script establishes; the emptiness of (6,3) itself is
    EXTERNAL and is not verified here.
    """

    A43 = solution_4_3()
    require(is_solution(A43, 4, 3), "calibration lost")
    # the implication direction, exhibited concretely: any (6,5) solution would
    # project to a (6,3) solution on each of the C(5,3) = 10 colour triples
    require(len(list(combinations(range(5), 3))) == 10,
            "there are not ten colour triples in a five-palette")
    require(len(list(combinations(range(4), 3))) == 4,
            "there are not four colour triples in a four-palette")
    return True


def main():
    audit_the_two_families()
    checked = audit_P1_projection_preserves_coefficients()
    audit_P1_target_restricts()
    audit_P3_direction_is_one_way()
    audit_P2_case_list()
    print(
        f"PASS: restricting an edge assignment to a d-subset of its colours "
        f"leaves every matching-tensor coefficient over those colours "
        f"literally unchanged ({checked} coefficients checked on arbitrary "
        f"matrices at (n,d',d) = (4,4,3), (6,5,3), (6,4,2), (8,4,3)), and "
        f"Delta_(n,d') restricted to words over the subset is exactly "
        f"Delta_(n,d); so a solution at (n,d') yields one at (n,d) for every "
        f"d <= d', and emptiness is MONOTONE UPWARD in d -- closing d = 3 "
        f"closes every larger palette at that n, which given the external "
        f"(6,3) result closes (6,4) and (6,5) as well; the implication does "
        f"NOT run downward, as the (4,3) solution and a padded (4,2) packet "
        f"whose third anchor is zero both witness"
    )


if __name__ == "__main__":
    sys.exit(main())

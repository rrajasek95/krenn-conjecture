#!/usr/bin/env python3
"""Exhaustive check of the three-term step in ``notes/slice-cover.md``.

Section 1 of that note reduces the one-slice covering lemma to the claim that
in

    sum_{r=0}^2 c_r l_{1,r} (x) ... (x) l_{m,r} = 0,     c_0 c_1 c_2 != 0,

with ``l_{j,r}`` the restriction to ``U_j <= C^3`` of the ``r``-th coordinate
functional and ``dim U_j >= 2``, every displayed pure tensor vanishes.  The
proof written in the note uses no classification of decomposable
dependences.  It evaluates the identity at explicitly chosen points, and it
needs only two field-independent facts:

* (K) the three coordinate restrictions at a mode span ``U_j^*``, which has
  dimension at least two, so they never lie in one line; and
* (A) if ``l != 0`` and ``l'`` is not a multiple of ``l`` then some point
  has ``l != 0`` and ``l' = 0``, while if ``l`` and ``l'`` are both nonzero
  then some point has both nonzero -- a space is never the union of two
  proper subspaces.

So the same statement holds over any field, and an exhaustive search over a
small finite field is a genuine adversarial test of the written argument.
This script performs two such searches with exact integer arithmetic modulo a
prime.  No floating-point value and no external solver is involved, and every
check raises rather than asserts, so ``python3 -O`` still performs it.

Both checks test the THREE-TERM STEP, not the one-slice covering lemma itself;
the lemma is what that step is used to prove.

Check A replays the three-term step in exactly the shape above: it enumerates
every configuration and confirms that whenever the identity holds, all three
pure tensors vanish.  At m = 2 it finds NO identities at all -- three colors
need three distinct modes -- so check A is vacuous there and only check B
exercises the sharp case.

Check B replays the note's case analysis.  For every configuration in which
the distinguished pure tensor is nonzero, it determines which of the three
cases applies, requires that each evaluation point the proof prescribes
really exists, and requires that the case excluded by (K) -- both colors
free at the same single mode -- never occurs.

Neither check is a substitute for the proof over C; each is a finite,
independent confirmation that the field-independent argument has no
counterexample in the smallest cases.  Check B covers the sharp case m = 2.
"""

from __future__ import annotations

import argparse
import itertools
import time


DEFAULT_COVERING_CASES = (
    (2, 2),
    (2, 3),
    (2, 4),
    (3, 2),
    (3, 3),
    (3, 4),
    (5, 2),
    (5, 3),
)
FULL_COVERING_CASES = DEFAULT_COVERING_CASES + ((2, 5),)
DEFAULT_CASE_ANALYSIS_CASES = (
    (2, 2),
    (2, 3),
    (2, 4),
    (3, 2),
    (3, 3),
    (5, 2),
)
FULL_CASE_ANALYSIS_CASES = DEFAULT_CASE_ANALYSIS_CASES + ((3, 4), (5, 3))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def normalize(vector, p):
    """Scale ``vector`` so that its first nonzero entry is one."""

    lead = next(value for value in vector if value)
    inverse = pow(lead, p - 2, p)
    return tuple(value * inverse % p for value in vector)


def independent(first, second, p):
    """True when ``second`` is not a scalar multiple of ``first``."""

    return all(
        any((c * first[t] - second[t]) % p for t in range(len(first)))
        for c in range(p)
    )


def subspace_bases(p):
    """A basis of every subspace of F_p^3 of dimension two or three."""

    vectors = [v for v in itertools.product(range(p), repeat=3) if any(v)]
    covectors = sorted({normalize(v, p) for v in vectors})
    bases = []
    for covector in covectors:
        kernel = [
            v
            for v in vectors
            if sum(x * y for x, y in zip(covector, v, strict=True)) % p == 0
        ]
        first = kernel[0]
        second = next(v for v in kernel[1:] if independent(first, v, p))
        require(
            len(kernel) == p * p - 1,
            f"kernel of {covector} has {len(kernel)} nonzero vectors",
        )
        bases.append((first, second))
    bases.append(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    require(
        len(bases) == p * p + p + 2,
        f"subspace count for p={p}: {len(bases)} != {p * p + p + 2}",
    )
    return tuple(bases)


def coordinate_restrictions(basis):
    """``l_r`` in the coordinates dual to ``basis``."""

    return tuple(tuple(vector[r] for vector in basis) for r in range(3))


def pure_tensor_vanishes(factors):
    return any(not any(factor) for factor in factors)


def check_covering_lemma(p, m):
    """Exhaust every configuration of the displayed shape over F_p."""

    bases = subspace_bases(p)
    units = tuple(range(1, p))
    configurations = 0
    identities = 0
    for choice in itertools.product(bases, repeat=m):
        local = [coordinate_restrictions(basis) for basis in choice]
        ranges = [range(len(basis)) for basis in choice]
        for coefficients in itertools.product(units, repeat=3):
            configurations += 1
            vanishes = True
            for index in itertools.product(*ranges):
                total = 0
                for r in range(3):
                    term = coefficients[r]
                    for j in range(m):
                        term = term * local[j][r][index[j]] % p
                    total += term
                if total % p:
                    vanishes = False
                    break
            if not vanishes:
                continue
            identities += 1
            for r in range(3):
                require(
                    pure_tensor_vanishes([local[j][r] for j in range(m)]),
                    f"p={p} m={m}: pure tensor {r} survives for "
                    f"bases={choice} coefficients={coefficients}",
                )
    return configurations, identities


def in_line(functional, anchor, p):
    """True when ``functional`` is a scalar multiple of ``anchor``."""

    return any(
        all((c * anchor[t] - functional[t]) % p == 0 for t in range(len(anchor)))
        for c in range(p)
    )


def evaluate(functional, vector, p):
    return sum(x * y for x, y in zip(functional, vector, strict=True)) % p


def points(dimension, p):
    return tuple(itertools.product(range(p), repeat=dimension))


def find_point(space, live, dead, p, dead_is_zero):
    """A point of ``space`` on which ``live`` is nonzero and ``dead`` is
    zero (``dead_is_zero``) or nonzero."""

    for u in space:
        if not evaluate(live, u, p):
            continue
        value = evaluate(dead, u, p)
        if (value == 0) == dead_is_zero:
            return u
    return None


def check_case_analysis(p, m):
    """Replay the note's case analysis on every configuration over F_p.

    The three cases are those of the proof: two distinct free modes, one
    common free mode, and a color with no free mode.  For each configuration
    with ``T_r != 0`` the corresponding evaluation points must exist, and the
    middle case must never occur, since (K) rules it out.
    """

    bases = subspace_bases(p)
    seen = {"two-free": 0, "one-free": 0, "no-free": 0}
    for choice in itertools.product(bases, repeat=m):
        local = [coordinate_restrictions(basis) for basis in choice]
        spaces = [points(len(basis), p) for basis in choice]
        for r in range(3):
            anchors = [local[j][r] for j in range(m)]
            if any(not any(anchor) for anchor in anchors):
                continue  # T_r is already zero; nothing to prove
            others = [s for s in range(3) if s != r]
            free = {
                s: [
                    j
                    for j in range(m)
                    if not in_line(local[j][s], anchors[j], p)
                ]
                for s in others
            }
            pair = next(
                (
                    (j1, j2)
                    for j1 in free[others[0]]
                    for j2 in free[others[1]]
                    if j1 != j2
                ),
                None,
            )
            if pair is not None:
                seen["two-free"] += 1
                j1, j2 = pair
                for mode, colour in ((j1, others[0]), (j2, others[1])):
                    require(
                        find_point(
                            spaces[mode], anchors[mode], local[mode][colour],
                            p, True,
                        )
                        is not None,
                        f"p={p} m={m}: no killing point at mode {mode}",
                    )
                for mode in range(m):
                    require(
                        any(evaluate(anchors[mode], u, p) for u in spaces[mode]),
                        f"p={p} m={m}: anchor {mode} vanishes identically",
                    )
                continue
            if free[others[0]] and free[others[1]]:
                # Both free sets are nonempty yet no two distinct modes can
                # be drawn from them, so they are the same singleton.  (K)
                # must have excluded this.
                seen["one-free"] += 1
                require(
                    False,
                    f"p={p} m={m}: bases={choice} colour={r} has "
                    f"F={free[others[0]]} for both colors, which (K) "
                    "is supposed to exclude",
                )
            seen["no-free"] += 1
            dead_colour = others[0] if not free[others[0]] else others[1]
            live_colour = others[0] if others[1] == dead_colour else others[1]
            for mode in range(m):
                require(
                    mode in free[live_colour],
                    f"p={p} m={m}: (K) fails to free colour {live_colour} "
                    f"at mode {mode}",
                )
                require(
                    find_point(
                        spaces[mode], anchors[mode], local[mode][live_colour],
                        p, False,
                    )
                    is not None,
                    f"p={p} m={m}: no doubly live point at mode {mode}",
                )
                require(
                    find_point(
                        spaces[mode], anchors[mode], local[mode][live_colour],
                        p, True,
                    )
                    is not None,
                    f"p={p} m={m}: no replacement point at mode {mode}",
                )
    require(
        seen["one-free"] == 0,
        f"p={p} m={m}: the (K)-excluded common-free-mode case occurred",
    )
    return seen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full",
        action="store_true",
        help="add the larger cases (about 30% slower, same conclusion)",
    )
    arguments = parser.parse_args()
    covering = FULL_COVERING_CASES if arguments.full else DEFAULT_COVERING_CASES
    analysis = (
        FULL_CASE_ANALYSIS_CASES
        if arguments.full
        else DEFAULT_CASE_ANALYSIS_CASES
    )

    started = time.monotonic()
    print("check A: three-term step, exhaustive over F_p")
    for p, m in covering:
        configurations, identities = check_covering_lemma(p, m)
        require(
            identities > 0 or m < 3,
            f"p={p} m={m}: the search found no vanishing identity to test",
        )
        print(
            f"  p={p} m={m}: {configurations} configurations, "
            f"{identities} vanishing identities, every pure tensor vanishes"
        )
    print("check B: the note's case analysis, exhaustive over F_p")
    for p, m in analysis:
        seen = check_case_analysis(p, m)
        require(
            seen["two-free"] > 0 and seen["no-free"] > 0,
            f"p={p} m={m}: {seen} leaves a case of the analysis untested",
        )
        print(
            f"  p={p} m={m}: two-distinct-free-modes {seen['two-free']}, "
            f"no-free-mode {seen['no-free']}, "
            f"common-free-mode {seen['one-free']} (excluded by (K)); "
            "every prescribed evaluation point exists"
        )
    print(
        "slice-cover three-term step verified in "
        f"{time.monotonic() - started:.2f}s"
    )


if __name__ == "__main__":
    main()

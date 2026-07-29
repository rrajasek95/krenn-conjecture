#!/usr/bin/env python3
"""Exact SAT search for a first-order ternary lift from the binary boundary.

The requested congruence is

    H_6(A) = e0^6 + e1^6 + 2 e2^6                  (mod 4),

with arbitrary asymmetric 3-by-3 aggregate matrices over Z/4.  Reducing
modulo two gives binary GHZ, while the high bit asks whether the missing
third color can enter at first 2-adic order.

This is a discovery tool.  ``--orbit`` fixes one of the 16 relative orbits
of supported color-zero and color-one perfect matchings, which is exhaustive
under vertex symmetry when all orbit values are checked.
"""

from __future__ import annotations

import argparse
import itertools
import time

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


N = 6
Q = 3


def perfect_matchings(vertices=tuple(range(N))):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def matching_orbit_representatives(matchings, canonical):
    def act(matching, permutation):
        return tuple(
            sorted(
                tuple(sorted((permutation[u], permutation[v])))
                for u, v in matching
            )
        )

    stabilizer = tuple(
        permutation
        for permutation in itertools.permutations(range(N))
        if act(canonical, permutation) == canonical
    )
    remaining = set(matchings)
    representatives = []
    while remaining:
        representative = min(remaining)
        orbit = {act(representative, permutation) for permutation in stabilizer}
        representatives.append(representative)
        remaining.difference_update(orbit)
    return tuple(representatives)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, default=0)
    parser.add_argument(
        "--profile",
        choices=("rank2-boundary", "base-ghz"),
        default="rank2-boundary",
    )
    parser.add_argument(
        "--primitive-type",
        choices=("same", "cross"),
        help="for base-ghz, normalize a primitive same- or cross-color entry",
    )
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument(
        "--boolean-entries",
        action="store_true",
        help="restrict every aggregate entry to 0 or 1 modulo four",
    )
    parser.add_argument(
        "--no-three",
        action="store_true",
        help="forbid residue 3 (high bit cannot accompany an odd low bit)",
    )
    parser.add_argument(
        "--no-two",
        action="store_true",
        help="forbid residue 2 (a high bit requires an odd low bit)",
    )
    parser.add_argument(
        "--seek-mod8-lift",
        action="store_true",
        help="enumerate mod-4 models until finding one with a mod-8 correction",
    )
    parser.add_argument("--max-models", type=int, default=10000)
    parser.add_argument(
        "--direct-mod8",
        action="store_true",
        help="add a third entry bit and solve the target identity directly modulo eight",
    )
    args = parser.parse_args()

    matchings = tuple(perfect_matchings())
    canonical = ((0, 1), (2, 3), (4, 5))
    representatives = matching_orbit_representatives(matchings, canonical)
    if not 0 <= args.orbit < len(representatives):
        parser.error(f"orbit must lie in [0,{len(representatives)-1}]")
    second = representatives[args.orbit]

    pool = IDPool()
    cnf = CNF()

    def entry(u, v, a, b, high):
        if u > v:
            u, v, a, b = v, u, b, a
        return pool.id(("entry", u, v, a, b, high))

    def and_gate(literals, tag):
        out = pool.id(("and", tag))
        for literal in literals:
            cnf.append([-out, literal])
        cnf.append([out] + [-literal for literal in literals])
        return out

    def xor2(left, right, tag):
        out = pool.id(("xor", tag))
        cnf.extend(
            [
                [left, right, -out],
                [-left, -right, -out],
                [left, -right, out],
                [-left, right, out],
            ]
        )
        return out

    def xor_many(literals, tag):
        value = literals[0]
        for index, literal in enumerate(literals[1:]):
            value = xor2(value, literal, (tag, index))
        return value

    def carry3(first, second, third, tag):
        """High carry bit of the sum of three Boolean bits."""
        pairs = (
            and_gate((first, second), (tag, 0)),
            and_gate((first, third), (tag, 1)),
            and_gate((second, third), (tag, 2)),
        )
        return xor_many(pairs, (tag, "xor"))

    if args.profile == "rank2-boundary":
        # Normalize one odd matching monomial in each unit target coefficient.
        for color, matching in ((0, canonical), (1, second)):
            for u, v in matching:
                cnf.append([entry(u, v, color, color, False)])
    else:
        if args.primitive_type is None:
            parser.error("base-ghz requires --primitive-type")
        if args.primitive_type == "same":
            cnf.append([entry(0, 1, 0, 0, False)])
        else:
            cnf.append([entry(0, 1, 0, 1, False)])

    if args.boolean_entries:
        for u, v in itertools.combinations(range(N), 2):
            for a, b in itertools.product(range(Q), repeat=2):
                cnf.append([-entry(u, v, a, b, True)])
    if args.no_three:
        for u, v in itertools.combinations(range(N), 2):
            for a, b in itertools.product(range(Q), repeat=2):
                cnf.append(
                    [
                        -entry(u, v, a, b, False),
                        -entry(u, v, a, b, True),
                    ]
                )
    if args.no_two:
        for u, v in itertools.combinations(range(N), 2):
            for a, b in itertools.product(range(Q), repeat=2):
                cnf.append(
                    [
                        -entry(u, v, a, b, True),
                        entry(u, v, a, b, False),
                    ]
                )

    # The exact integral degree-nine identity P-C=2R gives a useful
    # certificate-level necessary condition.  On a putative solution the
    # mixed columns vanish, P=2 (mod 4), and hence R(A mod 2)=1.  Every
    # monomial of R is a perfect matching of all 18 vertex/color ports.
    # Therefore the odd-entry support must contain at least one such port
    # matching.  Encode its existence explicitly; this is redundant but a
    # substantial SAT propagation aid.
    if args.profile == "rank2-boundary":
        selectors = {}
        for u, v in itertools.combinations(range(N), 2):
            for a, b in itertools.product(range(Q), repeat=2):
                selector = pool.id(("balanced", u, v, a, b))
                selectors[u, a, v, b] = selector
                cnf.append([-selector, entry(u, v, a, b, False)])
        for u in range(N):
            for a in range(Q):
                incident = []
                for v in range(N):
                    if u == v:
                        continue
                    for b in range(Q):
                        if u < v:
                            incident.append(selectors[u, a, v, b])
                        else:
                            incident.append(selectors[v, b, u, a])
                cnf.append(incident)
                for left, right in itertools.combinations(incident, 2):
                    cnf.append([-left, -right])

    for coloring_index, coloring in enumerate(
        itertools.product(range(Q), repeat=N)
    ):
        term_bits = []
        for matching_index, matching in enumerate(matchings):
            lows = [
                entry(u, v, coloring[u], coloring[v], False)
                for u, v in matching
            ]
            highs = [
                entry(u, v, coloring[u], coloring[v], True)
                for u, v in matching
            ]
            tops = [
                entry(u, v, coloring[u], coloring[v], "top")
                for u, v in matching
            ]
            low = and_gate(lows, ("term-low", coloring_index, matching_index))
            high_parts = []
            for exceptional in range(3):
                factors = [highs[exceptional]] + [
                    lows[index] for index in range(3) if index != exceptional
                ]
                high_parts.append(
                    and_gate(
                        factors,
                        ("term-high", coloring_index, matching_index, exceptional),
                    )
                )
            high = xor_many(
                high_parts, ("term-high-xor", coloring_index, matching_index)
            )
            if args.direct_mod8:
                first_order_carry = carry3(
                    *high_parts,
                    ("term-first-carry", coloring_index, matching_index),
                )
                top_parts = []
                for exceptional in range(3):
                    factors = [tops[exceptional]] + [
                        lows[index] for index in range(3) if index != exceptional
                    ]
                    top_parts.append(
                        and_gate(
                            factors,
                            ("term-top", coloring_index, matching_index, exceptional),
                        )
                    )
                for first, second in itertools.combinations(range(3), 2):
                    remaining = 3 - first - second
                    top_parts.append(
                        and_gate(
                            (highs[first], highs[second], lows[remaining]),
                            (
                                "term-two-highs",
                                coloring_index,
                                matching_index,
                                first,
                                second,
                            ),
                        )
                    )
                top = xor_many(
                    top_parts + [first_order_carry],
                    ("term-top-xor", coloring_index, matching_index),
                )
            else:
                top = None
            term_bits.append((low, high, top))

        # Ripple addition in Z/4.  Adding (l,h) and (l',h') gives
        # low=l xor l' and high=h xor h' xor (l and l').
        total_low, total_high, total_top = term_bits[0]
        for matching_index, (low, high, top) in enumerate(term_bits[1:], 1):
            carry = and_gate(
                (total_low, low), ("sum-carry", coloring_index, matching_index)
            )
            if args.direct_mod8:
                high_carry = carry3(
                    total_high,
                    high,
                    carry,
                    ("sum-high-carry", coloring_index, matching_index),
                )
                total_top = xor_many(
                    (total_top, top, high_carry),
                    ("sum-top", coloring_index, matching_index),
                )
            total_high = xor_many(
                (total_high, high, carry),
                ("sum-high", coloring_index, matching_index),
            )
            total_low = xor2(
                total_low, low, ("sum-low", coloring_index, matching_index)
            )

        if args.profile == "rank2-boundary" and len(set(coloring)) == 1 and coloring[0] in (0, 1):
            target_low, target_high = 1, 0
        elif args.profile == "rank2-boundary" and coloring == (2,) * N:
            target_low, target_high = 0, 1
        elif args.profile == "base-ghz" and len(set(coloring)) == 1:
            target_low, target_high = 0, 1
        else:
            target_low, target_high = 0, 0
        cnf.append([total_low if target_low else -total_low])
        cnf.append([total_high if target_high else -total_high])
        if args.direct_mod8:
            cnf.append([-total_top])

    print(
        f"profile={args.profile} orbit={args.orbit}/{len(representatives)} second={second} "
        f"vars={pool.top} clauses={len(cnf.clauses)}",
        flush=True,
    )
    started = time.time()

    entry_keys = tuple(
        (u, v, a, b)
        for u, v in itertools.combinations(range(N), 2)
        for a, b in itertools.product(range(Q), repeat=2)
    )

    def decode(positive):
        matrices = {}
        for u, v in itertools.combinations(range(N), 2):
            table = tuple(
                tuple(
                    int(entry(u, v, a, b, False) in positive)
                    + 2 * int(entry(u, v, a, b, True) in positive)
                    + 4 * int(
                        args.direct_mod8
                        and entry(u, v, a, b, "top") in positive
                    )
                    for b in range(Q)
                )
                for a in range(Q)
            )
            if any(any(row) for row in table):
                matrices[u, v] = table
        return matrices

    zero = ((0,) * Q,) * Q

    def target_value(coloring):
        if args.profile == "rank2-boundary" and len(set(coloring)) == 1 and coloring[0] in (0, 1):
            return 1
        if args.profile == "rank2-boundary" and coloring == (2,) * N:
            return 2
        if args.profile == "base-ghz" and len(set(coloring)) == 1:
            return 2
        return 0

    def direct_coefficients(matrices):
        values = {}
        for coloring in itertools.product(range(Q), repeat=N):
            total = 0
            for matching in matchings:
                term = 1
                for u, v in matching:
                    term *= matrices.get((u, v), zero)[coloring[u]][coloring[v]]
                total += term
            values[coloring] = total
        return values

    def mod8_correction(matrices):
        """Solve H(A+4C)=target (mod 8) as a GF(2) linear system."""
        variable_index = {key: index for index, key in enumerate(entry_keys)}
        number_variables = len(entry_keys)
        values = direct_coefficients(matrices)
        pivots = {}
        for coloring in itertools.product(range(Q), repeat=N):
            coefficient_bits = 0
            for matching in matchings:
                base = [
                    matrices.get((u, v), zero)[coloring[u]][coloring[v]] & 1
                    for u, v in matching
                ]
                for exceptional, (u, v) in enumerate(matching):
                    if all(
                        base[index]
                        for index in range(len(matching))
                        if index != exceptional
                    ):
                        key = (u, v, coloring[u], coloring[v])
                        coefficient_bits ^= 1 << variable_index[key]
            difference = target_value(coloring) - values[coloring]
            assert difference % 4 == 0
            rhs = (difference // 4) & 1
            row = coefficient_bits | (rhs << number_variables)
            while row:
                pivot = (row & -row).bit_length() - 1
                if pivot == number_variables:
                    return None
                if pivot in pivots:
                    row ^= pivots[pivot]
                else:
                    pivots[pivot] = row
                    break

        solution = 0
        variable_mask = (1 << number_variables) - 1
        for pivot in sorted(pivots, reverse=True):
            row = pivots[pivot]
            rhs = (row >> number_variables) & 1
            current = ((row & variable_mask & solution).bit_count()) & 1
            if rhs ^ current:
                solution |= 1 << pivot
        return {
            key for index, key in enumerate(entry_keys) if solution >> index & 1
        }

    with Solver(name=args.solver, bootstrap_with=cnf) as solver:
        tested = 0
        correction = None
        while solver.solve():
            positive = {literal for literal in solver.get_model() if literal > 0}
            matrices = decode(positive)
            tested += 1
            if not args.seek_mod8_lift:
                break
            correction = mod8_correction(matrices)
            if correction is not None:
                print(
                    f"found mod-8 lift after {tested} mod-4 models "
                    f"time={time.time()-started:.2f}s",
                    flush=True,
                )
                break
            if tested >= args.max_models:
                print(
                    f"no mod-8 lift among {tested} models "
                    f"time={time.time()-started:.2f}s",
                    flush=True,
                )
                return
            blocking = []
            for u, v, a, b in entry_keys:
                for high in (False, True):
                    literal = entry(u, v, a, b, high)
                    blocking.append(-literal if literal in positive else literal)
            solver.add_clause(blocking)
            if tested % 100 == 0:
                print(f"tested mod-4 models={tested}", flush=True)
        else:
            print(
                f"sat=False tested={tested} time={time.time()-started:.2f}s",
                flush=True,
            )
            return

        print(f"sat=True time={time.time()-started:.2f}s", flush=True)
        print("matrices =", matrices)

        # Independent direct audit over Z/4 or Z/8.
        values = direct_coefficients(matrices)
        modulus = 8 if args.direct_mod8 else 4
        for coloring, total in values.items():
            assert total % modulus == target_value(coloring)
        print(f"independent exact Z/{modulus} audit passed")

        if args.seek_mod8_lift:
            assert correction is not None
            lifted = {
                (u, v): tuple(
                    tuple(
                        matrices.get((u, v), zero)[a][b]
                        + 4 * int((u, v, a, b) in correction)
                        for b in range(Q)
                    )
                    for a in range(Q)
                )
                for u, v in itertools.combinations(range(N), 2)
            }
            lifted_values = direct_coefficients(lifted)
            for coloring, total in lifted_values.items():
                assert total % 8 == target_value(coloring)
            print("mod8_correction =", sorted(correction))
            print("independent exact Z/8 audit passed")


if __name__ == "__main__":
    main()

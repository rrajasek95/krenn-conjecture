#!/usr/bin/env python3
"""Exact SAT search for a counterexample to the binary Pfaffian partition lemma.

For each color ``r`` this script chooses an alternating matrix ``A_r`` over
``F_2``.  A Boolean recurrence computes every principal Pfaffian, and the SAT
formula asks that

    Pf(A_0[S_0]) Pf(A_1[S_1]) Pf(A_2[S_2]) = 0

for every proper ordered partition into even blocks, while all three full
Pfaffians are one.  Thus SAT is exactly a counterexample and UNSAT proves the
lemma at the requested order.

Two safe symmetry reductions are used.  A supported perfect matching of
``A_0`` is sent to the canonical matching by a vertex permutation.  A
supported perfect matching of ``A_1`` is then classified, under the stabilizer
of the first, by the cycle lengths in the union of the two matchings.  These
cycle types are the integer partitions of ``n/2``; the script solves one exact
branch per type.  No assumption is made about the remaining support edges.

Run, for example, with an ephemeral PySAT dependency:

    uv run --with python-sat python \
      computations/search_diagonal_mod2_uniform_sat.py --n 10
"""

from __future__ import annotations

import argparse
from itertools import permutations, product
from time import monotonic

try:
    from pysat.solvers import Solver
except ImportError as error:  # pragma: no cover - dependency diagnostic
    raise SystemExit(
        "python-sat is required; run with `uv run --with python-sat python ...`"
    ) from error


Q = 3


class Formula:
    def __init__(self, native_xor: bool = False) -> None:
        self.top = 0
        self.clauses: list[list[int]] = []
        self.native_xor = native_xor
        self.xors: list[tuple[tuple[int, ...], bool]] = []

    def new(self) -> int:
        self.top += 1
        return self.top

    def equivalence(self, left: int, right: int) -> None:
        self.clauses.extend(([-left, right], [left, -right]))

    def and_gate(self, inputs: tuple[int, ...]) -> int:
        if len(inputs) == 1:
            return inputs[0]
        output = self.new()
        self.clauses.extend([-output, value] for value in inputs)
        self.clauses.append([output] + [-value for value in inputs])
        return output

    def xor2_gate(self, left: int, right: int) -> int:
        output = self.new()
        self.clauses.extend(
            (
                [-left, -right, -output],
                [left, right, -output],
                [left, -right, output],
                [-left, right, output],
            )
        )
        return output

    def xor_gate(self, inputs: list[int]) -> int:
        assert inputs
        if self.native_xor:
            output = self.new()
            # output = XOR(inputs), equivalently XOR(inputs, output) = 0.
            self.xors.append((tuple(inputs) + (output,), False))
            return output
        value = inputs[0]
        for next_value in inputs[1:]:
            value = self.xor2_gate(value, next_value)
        return value


def integer_partitions(total: int, maximum: int | None = None):
    """Yield nonincreasing integer partitions of ``total``."""

    if total == 0:
        yield ()
        return
    if maximum is None or maximum > total:
        maximum = total
    for first in range(maximum, 0, -1):
        for rest in integer_partitions(total - first, first):
            yield (first,) + rest


def canonical_matching(size: int) -> tuple[tuple[int, int], ...]:
    return tuple((2 * index, 2 * index + 1) for index in range(size // 2))


def matching_of_cycle_type(
    size: int, cycle_type: tuple[int, ...]
) -> tuple[tuple[int, int], ...]:
    """A matching whose union with the canonical one has ``cycle_type``."""

    assert sum(cycle_type) == size // 2
    answer = []
    first_pair = 0
    for part in cycle_type:
        pair_numbers = tuple(range(first_pair, first_pair + part))
        first_pair += part
        if part == 1:
            pair = pair_numbers[0]
            answer.append((2 * pair, 2 * pair + 1))
            continue
        for position, pair in enumerate(pair_numbers):
            next_pair = pair_numbers[(position + 1) % part]
            answer.append((2 * pair + 1, 2 * next_pair))
    return tuple(sorted((min(u, v), max(u, v)) for u, v in answer))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + matching))


def stabilizer_of_canonical_matching(size: int):
    half = size // 2
    for pair_permutation in permutations(range(half)):
        for flips in product(range(2), repeat=half):
            vertex_permutation = [0] * size
            for pair in range(half):
                for bit in range(2):
                    vertex_permutation[2 * pair + bit] = (
                        2 * pair_permutation[pair] + (bit ^ flips[pair])
                    )
            yield tuple(vertex_permutation)


def relabel_matching(matching, vertex_permutation):
    return tuple(
        sorted(
            (min(vertex_permutation[u], vertex_permutation[v]),
             max(vertex_permutation[u], vertex_permutation[v]))
            for u, v in matching
        )
    )


def third_matching_orbit_representatives(
    size: int, cycle_type: tuple[int, ...]
) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Quotient color-two matchings by the fixed first-pair stabilizer."""

    second = matching_of_cycle_type(size, cycle_type)
    stabilizer = tuple(
        vertex_permutation
        for vertex_permutation in stabilizer_of_canonical_matching(size)
        if relabel_matching(second, vertex_permutation) == second
    )
    unseen = set(perfect_matchings(tuple(range(size))))
    representatives = []
    while unseen:
        representative = min(unseen)
        orbit = {
            relabel_matching(representative, vertex_permutation)
            for vertex_permutation in stabilizer
        }
        unseen.difference_update(orbit)
        representatives.append(representative)
    return tuple(representatives)


def masks_of_size(size: int, parity: int = 0) -> tuple[int, ...]:
    return tuple(mask for mask in range(1 << size) if mask.bit_count() % 2 == parity)


def ordered_even_partitions(size: int):
    """Yield all ordered partitions as three disjoint bit masks."""

    full = (1 << size) - 1
    for choices in product(range(Q), repeat=size):
        masks = [0] * Q
        for vertex, color in enumerate(choices):
            masks[color] |= 1 << vertex
        if any(mask.bit_count() % 2 for mask in masks):
            continue
        if full in masks:  # one of the three constant partitions
            continue
        yield tuple(masks)


def build_formula(
    size: int, cycle_type: tuple[int, ...], native_xor: bool = False
):
    formula = Formula(native_xor=native_xor)
    full = (1 << size) - 1

    # Independent upper-triangular support bits of the three matrices.
    edge: dict[tuple[int, int, int], int] = {}
    for color in range(Q):
        for u in range(size):
            for v in range(u + 1, size):
                edge[color, u, v] = formula.new()

    # h[r,S] is exactly Pf(A_r[S]).  Expanding at the least vertex gives
    # h(S) = XOR_{v in S-u} A[u,v] AND h(S-u-v).  We construct masks in
    # increasing order, so every smaller Pfaffian has already been defined.
    pfaffian: dict[tuple[int, int], int | None] = {
        (color, 0): None for color in range(Q)
    }
    for color in range(Q):
        for mask in masks_of_size(size):
            if mask == 0:
                continue
            u_bit = mask & -mask
            u = u_bit.bit_length() - 1
            remainder = mask ^ u_bit
            terms = []
            while remainder:
                v_bit = remainder & -remainder
                v = v_bit.bit_length() - 1
                submask = mask ^ u_bit ^ v_bit
                edge_variable = edge[color, min(u, v), max(u, v)]
                subpfaffian = pfaffian[color, submask]
                term = (
                    edge_variable
                    if subpfaffian is None
                    else formula.and_gate((edge_variable, subpfaffian))
                )
                terms.append(term)
                remainder ^= v_bit
            output = formula.new()
            formula.equivalence(output, formula.xor_gate(terms))
            pfaffian[color, mask] = output

    # Nonsingularity of all three full matrices.
    for color in range(Q):
        formula.clauses.append([pfaffian[color, full]])

    # Every nonsingular support contains a perfect matching.  Use vertex
    # symmetry to make one in color zero canonical, then branch over all
    # stabilizer orbits of a supported color-one matching.
    for u, v in canonical_matching(size):
        formula.clauses.append([edge[0, u, v]])
    for u, v in matching_of_cycle_type(size, cycle_type):
        formula.clauses.append([edge[1, u, v]])

    partition_count = 0
    for masks in ordered_even_partitions(size):
        clause = []
        for color, mask in enumerate(masks):
            value = pfaffian[color, mask]
            if value is not None:  # Pf(empty)=1, so its negation is false.
                clause.append(-value)
        assert clause
        formula.clauses.append(clause)
        partition_count += 1

    return formula, edge, pfaffian, partition_count


def verify_model(size: int, positive: set[int], edge) -> tuple[int, int, int] | None:
    """Recompute principal Pfaffians directly and return a mixed witness."""

    values = {
        key: int(variable in positive) for key, variable in edge.items()
    }
    cache: dict[tuple[int, int], int] = {}

    def pf(color: int, mask: int) -> int:
        if mask == 0:
            return 1
        key = color, mask
        if key in cache:
            return cache[key]
        u_bit = mask & -mask
        u = u_bit.bit_length() - 1
        remainder = mask ^ u_bit
        answer = 0
        while remainder:
            v_bit = remainder & -remainder
            v = v_bit.bit_length() - 1
            answer ^= values[color, min(u, v), max(u, v)] & pf(
                color, mask ^ u_bit ^ v_bit
            )
            remainder ^= v_bit
        cache[key] = answer
        return answer

    full = (1 << size) - 1
    assert all(pf(color, full) for color in range(Q))
    for masks in ordered_even_partitions(size):
        if all(pf(color, mask) for color, mask in enumerate(masks)):
            return masks
    return None


def solve_branch(size: int, cycle_type: tuple[int, ...], solver_name: str):
    native_xor = solver_name == "cryptosat-native"
    formula, edge, _pfaffian, partition_count = build_formula(
        size, cycle_type, native_xor=native_xor
    )
    print(
        f"  type={cycle_type}: {formula.top} variables, "
        f"{len(formula.clauses)} clauses, {len(formula.xors)} XORs, "
        f"{partition_count} partitions",
        flush=True,
    )
    started = monotonic()
    if native_xor:
        from pycryptosat import Solver as CryptoSolver

        solver = CryptoSolver()
        for clause in formula.clauses:
            solver.add_clause(clause)
        for variables, rhs in formula.xors:
            solver.add_xor_clause(list(variables), rhs)
        satisfiable, model = solver.solve()
        elapsed = monotonic() - started
        print(
            f"    {'SAT' if satisfiable else 'UNSAT'} in {elapsed:.2f}s",
            flush=True,
        )
        if not satisfiable:
            return None
        positive = {
            variable
            for variable in range(1, len(model))
            if model[variable]
        }
        witness = verify_model(size, positive, edge)
        assert witness is None, "SAT assignment violates a forbidden partition"
        return positive, edge
    with Solver(name=solver_name, bootstrap_with=formula.clauses) as solver:
        satisfiable = solver.solve()
        elapsed = monotonic() - started
        print(
            f"    {'SAT' if satisfiable else 'UNSAT'} in {elapsed:.2f}s",
            flush=True,
        )
        if not satisfiable:
            return None
        positive = {literal for literal in solver.get_model() if literal > 0}
    witness = verify_model(size, positive, edge)
    assert witness is None, "SAT assignment violates a forbidden partition"
    return positive, edge


def solve_with_third_matching_branches(
    size: int, cycle_type: tuple[int, ...], solver_name: str
):
    """Solve one first-pair type via exact color-two matching orbits.

    The full color-two Pfaffian is one, so its support contains a perfect
    matching.  Fixing that matching in each stabilizer orbit is therefore an
    exhaustive disjunction.  Assumption solving lets all branches share the
    learned clauses of the common base formula.
    """

    native_xor = solver_name == "cryptosat-native"
    formula, edge, _pfaffian, partition_count = build_formula(
        size, cycle_type, native_xor=native_xor
    )
    representatives = third_matching_orbit_representatives(size, cycle_type)
    print(
        f"  type={cycle_type}: {formula.top} variables, "
        f"{len(formula.clauses)} clauses, {len(formula.xors)} XORs, "
        f"{partition_count} partitions, "
        f"{len(representatives)} third-matching orbits",
        flush=True,
    )
    started = monotonic()
    if native_xor:
        from pycryptosat import Solver as CryptoSolver

        solver = CryptoSolver()
        for clause in formula.clauses:
            solver.add_clause(clause)
        for variables, rhs in formula.xors:
            solver.add_xor_clause(list(variables), rhs)
        for branch, matching in enumerate(representatives, 1):
            assumptions = [edge[2, u, v] for u, v in matching]
            satisfiable, model = solver.solve(assumptions=assumptions)
            if satisfiable:
                elapsed = monotonic() - started
                print(
                    f"    SAT in orbit {branch}/{len(representatives)} "
                    f"after {elapsed:.2f}s",
                    flush=True,
                )
                positive = {
                    variable
                    for variable in range(1, len(model))
                    if model[variable]
                }
                witness = verify_model(size, positive, edge)
                assert witness is None, (
                    "SAT assignment violates a forbidden partition"
                )
                return positive, edge
            if branch % 10 == 0 or branch == len(representatives):
                print(
                    f"    {branch}/{len(representatives)} orbits UNSAT "
                    f"({monotonic() - started:.2f}s)",
                    flush=True,
                )
        return None
    with Solver(name=solver_name, bootstrap_with=formula.clauses) as solver:
        for branch, matching in enumerate(representatives, 1):
            assumptions = [edge[2, u, v] for u, v in matching]
            if solver.solve(assumptions=assumptions):
                elapsed = monotonic() - started
                print(
                    f"    SAT in orbit {branch}/{len(representatives)} "
                    f"after {elapsed:.2f}s",
                    flush=True,
                )
                positive = {
                    literal for literal in solver.get_model() if literal > 0
                }
                witness = verify_model(size, positive, edge)
                assert witness is None, (
                    "SAT assignment violates a forbidden partition"
                )
                return positive, edge
            if branch % 10 == 0 or branch == len(representatives):
                print(
                    f"    {branch}/{len(representatives)} orbits UNSAT "
                    f"({monotonic() - started:.2f}s)",
                    flush=True,
                )
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, choices=(6, 8, 10, 12), default=8)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument(
        "--fix-third-matching",
        action="store_true",
        help=(
            "also branch over color-two supported-matching orbits; this is "
            "usually much faster at n=10 but creates more branches"
        ),
    )
    parser.add_argument(
        "--only-type",
        help=(
            "solve only one cycle type, written as a comma-separated "
            "partition of n/2 (for example 3,2,1)"
        ),
    )
    arguments = parser.parse_args()
    size = arguments.n
    cycle_types = tuple(integer_partitions(size // 2))
    if arguments.only_type:
        selected = tuple(int(part) for part in arguments.only_type.split(","))
        if selected not in cycle_types:
            raise SystemExit(
                f"invalid cycle type {selected}; expected one of {cycle_types}"
            )
        cycle_types = (selected,)
    print(
        f"n={size}: {len(cycle_types)} "
        "supported-matching cycle types",
        flush=True,
    )
    for cycle_type in cycle_types:
        if arguments.fix_third_matching:
            result = solve_with_third_matching_branches(
                size, cycle_type, arguments.solver
            )
        else:
            result = solve_branch(size, cycle_type, arguments.solver)
        if result is not None:
            print(f"counterexample found in branch {cycle_type}", flush=True)
            raise SystemExit(1)
    print(f"verified: no binary counterexample at n={size}", flush=True)


if __name__ == "__main__":
    main()

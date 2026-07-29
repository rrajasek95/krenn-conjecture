#!/usr/bin/env python3
"""Characteristic-free diagonal hafnian obstruction through n=12.

For a scalar symmetric edge matrix A_r and an even set S, let z[r,S]
mean ``haf(A_r[S]) != 0``.  The only algebra used here is the Laplace
recurrence at every pivot u in S:

    haf(A_r[S]) = sum_{v in S-u} a^r_uv haf(A_r[S-{u,v}]).

Over a field, a nonzero sum has a nonzero summand, while a zero sum cannot
have exactly one nonzero summand.  We encode precisely these two necessary
support implications.  We then forbid a proper ordered even partition
S_0 + S_1 + S_2 = V with all three z[r,S_r] true.

UNSAT is therefore a rigorous obstruction for arbitrary complex weights;
SAT would only be a support-level survivor.  Symmetry breaking is exhaustive:
a recursively supported perfect matching of color zero is made canonical,
and a supported color-one matching is classified by the alternating-cycle
type of its union with the canonical matching.  In the coincident-matching
branch the unchanged stabilizer similarly classifies a color-two matching.
"""

from __future__ import annotations

import argparse
import itertools
from time import monotonic

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


def even_masks(n: int) -> tuple[int, ...]:
    return tuple(mask for mask in range(1 << n) if mask.bit_count() % 2 == 0)


def integer_partitions(total: int, maximum: int | None = None):
    """Yield nonincreasing integer partitions of total."""
    if total == 0:
        yield ()
        return
    if maximum is None or maximum > total:
        maximum = total
    for first in range(maximum, 0, -1):
        for rest in integer_partitions(total - first, first):
            yield (first,) + rest


def canonical_matching(n: int) -> tuple[tuple[int, int], ...]:
    return tuple((u, u + 1) for u in range(0, n, 2))


def matching_of_cycle_type(
    n: int, cycle_type: tuple[int, ...]
) -> tuple[tuple[int, int], ...]:
    """Representative relative to (01)(23)... for a partition of n/2."""
    assert sum(cycle_type) == n // 2 and all(part > 0 for part in cycle_type)
    answer: list[tuple[int, int]] = []
    first_pair = 0
    for part in cycle_type:
        pairs = tuple(range(first_pair, first_pair + part))
        first_pair += part
        if part == 1:
            pair = pairs[0]
            answer.append((2 * pair, 2 * pair + 1))
            continue
        for position, pair in enumerate(pairs):
            next_pair = pairs[(position + 1) % part]
            answer.append(tuple(sorted((2 * pair + 1, 2 * next_pair))))
    return tuple(sorted(answer))


def add_iff_and(cnf: CNF, output: int, left: int, right: int) -> None:
    cnf.append([-output, left])
    cnf.append([-output, right])
    cnf.append([output, -left, -right])


def add_zero_forbids_unique(cnf: CNF, value: int, terms: list[int]) -> None:
    """If value is false, terms may not contain exactly one true literal."""
    for index, term in enumerate(terms):
        cnf.append([value, -term] + terms[:index] + terms[index + 1 :])


def perfect_matchings(vertices: tuple[int, ...]):
    """Yield every perfect matching of an ordered even vertex tuple."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def add_iff_all(cnf: CNF, output: int, literals: tuple[int, ...]) -> None:
    """Encode output iff every literal is true."""
    for literal in literals:
        cnf.append([-output, literal])
    cnf.append([output] + [-literal for literal in literals])


def build(n: int, *, include_partitions: bool = True):
    pool = IDPool()
    cnf = CNF()
    evens = even_masks(n)
    full = (1 << n) - 1

    def z(color: int, mask: int) -> int:
        assert mask.bit_count() % 2 == 0
        return pool.id(("z", color, mask))

    for color in range(3):
        cnf.append([z(color, 0)])
        cnf.append([z(color, full)])
        for mask in evens:
            if mask.bit_count() < 4:
                continue
            vertices = tuple(v for v in range(n) if mask >> v & 1)
            defined_terms: set[int] = set()
            for pivot in vertices:
                terms: list[int] = []
                for other in vertices:
                    if other == pivot:
                        continue
                    edge_mask = (1 << pivot) | (1 << other)
                    rest = mask ^ edge_mask
                    term = pool.id(("term", color, mask, edge_mask))
                    # The same unordered edge occurs from its two pivots.
                    # Keep the historic duplicated clauses in the audited
                    # n<=10 counts, but deduplicate them in the much larger
                    # n=12 formula.
                    if n < 12 or term not in defined_terms:
                        add_iff_and(cnf, term, z(color, edge_mask), z(color, rest))
                        defined_terms.add(term)
                    terms.append(term)
                # Nonzero total => at least one nonzero summand.
                cnf.append([-z(color, mask)] + terms)
                # Zero total => zero or at least two nonzero summands.
                add_zero_forbids_unique(cnf, z(color, mask), terms)

        if n >= 12:
            # A useful *derived* size-six consequence of the same recurrence
            # is compiled for propagation.  Inductively, a feasible set has
            # a perfect matching of feasible two-sets; conversely a unique
            # such perfect matching forces feasibility (expand at a pivot
            # and apply the induction hypothesis to its complement).  These
            # clauses therefore do not strengthen the recurrence shadow.
            for mask in evens:
                if mask.bit_count() != 6:
                    continue
                vertices = tuple(v for v in range(n) if mask >> v & 1)
                matching_terms: list[int] = []
                for matching in perfect_matchings(vertices):
                    term = pool.id(("matching-term", color, mask, matching))
                    add_iff_all(
                        cnf,
                        term,
                        tuple(
                            z(color, (1 << u) | (1 << v)) for u, v in matching
                        ),
                    )
                    matching_terms.append(term)
                cnf.append([-z(color, mask)] + matching_terms)
                add_zero_forbids_unique(cnf, z(color, mask), matching_terms)

    # A nonconstant even coloring would have coefficient
    # h_0(S_0) h_1(S_1) h_2(S_2), so at least one factor must vanish.
    if include_partitions:
        for coloring in itertools.product(range(3), repeat=n):
            masks = [0, 0, 0]
            for vertex, color in enumerate(coloring):
                masks[color] |= 1 << vertex
            if any(mask.bit_count() % 2 for mask in masks):
                continue
            if any(mask == full for mask in masks):
                continue
            cnf.append([-z(color, masks[color]) for color in range(3)])

    return pool, cnf, z


def edge_assumptions(z, color: int, matching) -> list[int]:
    return [z(color, (1 << u) | (1 << v)) for u, v in matching]


def audit_countermodel(n: int, positive: set[int], z) -> tuple[int, int, int]:
    """Independently audit and compactly encode a SAT support assignment."""
    full = (1 << n) - 1
    evens = even_masks(n)
    families = tuple(
        frozenset(mask for mask in evens if z(color, mask) in positive)
        for color in range(3)
    )
    for family in families:
        assert 0 in family and full in family

    for color, family in enumerate(families):
        for mask in evens:
            if mask.bit_count() < 4:
                continue
            vertices = tuple(v for v in range(n) if mask >> v & 1)
            for pivot in vertices:
                term_count = 0
                for other in vertices:
                    if other == pivot:
                        continue
                    edge_mask = (1 << pivot) | (1 << other)
                    rest = mask ^ edge_mask
                    term_count += edge_mask in family and rest in family
                if mask in family:
                    assert term_count >= 1, (color, mask, pivot, term_count)
                else:
                    assert term_count != 1, (color, mask, pivot, term_count)

    for coloring in itertools.product(range(3), repeat=n):
        masks = [0, 0, 0]
        for vertex, color in enumerate(coloring):
            masks[color] |= 1 << vertex
        if any(mask.bit_count() % 2 for mask in masks):
            continue
        if any(mask == full for mask in masks):
            continue
        assert not all(masks[color] in families[color] for color in range(3))

    # Bit position ``mask`` is one precisely when that even subset is
    # feasible.  Three hexadecimal integers are a complete exact model.
    return tuple(sum(1 << mask for mask in family) for family in families)


def verify(
    n: int,
    solver_name: str = "cadical195",
    branch_number: int | None = None,
    third_number: int | None = None,
) -> None:
    started = monotonic()
    pool, cnf, z = build(n)
    canonical = canonical_matching(n)
    base = edge_assumptions(z, 0, canonical)
    types = tuple(integer_partitions(n // 2))
    coincident = (1,) * (n // 2)
    branches: list[tuple[str, list[int]]] = []
    third_branches: list[list[tuple[str, list[int]]]] = []

    if n >= 12:
        # Extract the color-zero matching recursively from z[0,V], recording
        # its deletion order, and only then relabel its ordered edges to
        # 01,23,... .  Thus every suffix in this particular order is
        # feasible.  This consumes the pair-permutation symmetry, so unlike
        # the smaller audits we do not simultaneously normalize color one.
        full = (1 << n) - 1
        prefix = 0
        suffix = full
        for u, v in canonical[:-1]:
            edge_mask = (1 << u) | (1 << v)
            prefix |= edge_mask
            suffix ^= edge_mask
            base.append(z(0, suffix))
            # These literals also follow from the forbidden-partition clause
            # for (suffix,prefix,empty); state them explicitly for propagation.
            base.append(-z(1, prefix))
            base.append(-z(2, prefix))
        # At the common pivot 0, colors one and two each have a removable
        # edge.  Neither can be 01 (that would cover V with the feasible
        # color-zero pair), and the two edges cannot coincide (they would
        # cover V with colors one and two).  Endpoint flips inside the five
        # remaining canonical pairs leave exactly the representatives below.
        partner_pairs = tuple(range(1, n // 2))
        full = (1 << n) - 1
        for first_pair in partner_pairs:
            first_partner = 2 * first_pair
            first_edge = (1 << 0) | (1 << first_partner)
            for second_pair in partner_pairs:
                if second_pair == first_pair:
                    second_partner = 2 * second_pair + 1
                else:
                    second_partner = 2 * second_pair
                second_edge = (1 << 0) | (1 << second_partner)
                first_assumptions = base + [
                    z(1, first_edge),
                    z(1, full ^ first_edge),
                    -z(0, first_edge),
                    -z(2, first_edge),
                    z(2, second_edge),
                    z(2, full ^ second_edge),
                    -z(0, second_edge),
                    -z(1, second_edge),
                ]
                # Branch once more on the recursive terms at pivot 1 in
                # the two feasible complements.  These choices are
                # exhaustive and turn one difficult disjunction into small
                # incremental branches while retaining learned clauses.
                first_complement = full ^ first_edge
                second_complement = full ^ second_edge
                first_seconds = tuple(
                    vertex
                    for vertex in range(n)
                    if vertex != 1 and (first_complement >> vertex) & 1
                )
                second_seconds = tuple(
                    vertex
                    for vertex in range(n)
                    if vertex != 1 and (second_complement >> vertex) & 1
                )
                for first_second in first_seconds:
                    first_second_edge = (1 << 1) | (1 << first_second)
                    for second_second in second_seconds:
                        second_second_edge = (1 << 1) | (1 << second_second)
                        first_prefix = first_edge | first_second_edge
                        second_prefix = second_edge | second_second_edge
                        assumptions = first_assumptions + [
                            z(1, first_second_edge),
                            z(1, first_complement ^ first_second_edge),
                            -z(0, first_prefix),
                            -z(2, first_prefix),
                            z(2, second_second_edge),
                            z(2, second_complement ^ second_second_edge),
                            -z(0, second_prefix),
                            -z(1, second_prefix),
                        ]
                        branches.append(
                            (
                                "ordered chains; partners="
                                f"{first_partner},{second_partner}; "
                                f"second={first_second},{second_second}",
                                assumptions,
                            )
                        )
                        # If a unit-compiled branch remains difficult, split
                        # the two feasible eight-sets once more, at their
                        # least vertices.  This is just another direct use of
                        # the nonzero recurrence implication, with all 7x7
                        # possible removable-edge pairs retained.
                        first_remainder = first_complement ^ first_second_edge
                        second_remainder = second_complement ^ second_second_edge
                        first_third_pivot = next(
                            vertex
                            for vertex in range(n)
                            if (first_remainder >> vertex) & 1
                        )
                        second_third_pivot = next(
                            vertex
                            for vertex in range(n)
                            if (second_remainder >> vertex) & 1
                        )
                        refinements: list[tuple[str, list[int]]] = []
                        for first_third in range(n):
                            if (
                                first_third == first_third_pivot
                                or not (first_remainder >> first_third) & 1
                            ):
                                continue
                            first_third_edge = (
                                (1 << first_third_pivot) | (1 << first_third)
                            )
                            for second_third in range(n):
                                if (
                                    second_third == second_third_pivot
                                    or not (second_remainder >> second_third) & 1
                                ):
                                    continue
                                second_third_edge = (
                                    (1 << second_third_pivot) | (1 << second_third)
                                )
                                first_new_prefix = first_prefix | first_third_edge
                                second_new_prefix = second_prefix | second_third_edge
                                refinements.append(
                                    (
                                        f"third={first_third_pivot}-"
                                        f"{first_third},{second_third_pivot}-"
                                        f"{second_third}",
                                        [
                                            z(1, first_third_edge),
                                            z(1, first_remainder ^ first_third_edge),
                                            -z(0, first_new_prefix),
                                            -z(2, first_new_prefix),
                                            z(2, second_third_edge),
                                            z(2, second_remainder ^ second_third_edge),
                                            -z(0, second_new_prefix),
                                            -z(1, second_new_prefix),
                                        ],
                                    )
                                )
                        assert len(refinements) == 49
                        third_branches.append(refinements)
    else:
        for cycle_type in types:
            first = edge_assumptions(z, 1, matching_of_cycle_type(n, cycle_type))
            if cycle_type != coincident:
                branches.append((str(cycle_type), base + first))
                continue
            # Here colors zero and one use the same fixed matching, so its full
            # stabilizer remains and classifies a supported color-two matching.
            for third_type in types:
                third = edge_assumptions(z, 2, matching_of_cycle_type(n, third_type))
                branches.append((f"{cycle_type}; color2={third_type}", base + first + third))

    symmetry_branch_count = len(branches)
    if n >= 12 and branch_number is None:
        # Assumption variables are frozen by several SAT backends and make
        # these otherwise easy branches unexpectedly hard.  Compile the
        # exhaustive union of branches into one ordinary CNF disjunction so
        # preprocessing remains available.  Common symmetry literals become
        # units; a selector implies only the residual literals of its branch.
        common = set(branches[0][1])
        for _label, assumptions in branches[1:]:
            common.intersection_update(assumptions)
        for literal in sorted(common, key=abs):
            cnf.append([literal])

        selectors = []
        for index, (_label, assumptions) in enumerate(branches):
            selector = pool.id(("n12-symmetry-branch", index))
            selectors.append(selector)
            for literal in assumptions:
                if literal not in common:
                    cnf.append([-selector, literal])
        cnf.append(selectors)
        branches = [("disjunction of all ordered-chain branches", [])]
    elif branch_number is not None:
        assert 1 <= branch_number <= len(branches)
        selected_label, selected_assumptions = branches[branch_number - 1]
        if third_number is not None:
            assert n >= 12
            assert 1 <= third_number <= len(third_branches[branch_number - 1])
            third_label, third_assumptions = third_branches[branch_number - 1][
                third_number - 1
            ]
            selected_label += "; " + third_label
            selected_assumptions += third_assumptions
        for literal in selected_assumptions:
            cnf.append([literal])
        branches = [(selected_label, [])]

    with Solver(name=solver_name, bootstrap_with=cnf) as solver:
        for branch_index, (label, assumptions) in enumerate(branches, 1):
            sat = solver.solve(assumptions=assumptions)
            if sat or len(branches) <= 100 or branch_index % 100 == 0:
                print(
                    f"n={n} branch={branch_index}/{len(branches)} "
                    f"label={label} sat={sat}",
                    flush=True,
                )
            if sat:
                positive = {literal for literal in solver.get_model() if literal > 0}
                encoded = audit_countermodel(n, positive, z)
                print(
                    "EXACT RECURRENCE COUNTERMODEL (bit position = subset mask):",
                    *(hex(bits) for bits in encoded),
                    sep="\n",
                    flush=True,
                )
                return

    expected = {
        6: (411, 2904, 5),
        8: (2988, 23844, 9),
        10: (18681, 159336, 13),
    }.get(n)
    if expected is not None:
        assert (pool.top, len(cnf.clauses), len(branches)) == expected
    print(
        f"VERIFIED n={n}: vars={pool.top} clauses={len(cnf.clauses)} "
        f"branches={symmetry_branch_count} solver={solver_name} "
        f"seconds={monotonic() - started:.3f}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, choices=(6, 8, 10, 12))
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--branch-number", type=int)
    parser.add_argument("--third-number", type=int)
    args = parser.parse_args()
    for n in ((args.n,) if args.n else (6, 8, 10)):
        verify(n, args.solver, args.branch_number, args.third_number)


if __name__ == "__main__":
    main()

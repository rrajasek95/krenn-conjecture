#!/usr/bin/env python3
"""SAT relaxation for three scalar hafnian set-functions.

For each color r, z[r,S] records whether Haf(A_r[S]) is nonzero and
w[r,e] whether the scalar edge is nonzero.  Hafnian expansion gives exact
support implications: a nonzero z has at least one supported expansion term,
while a zero z cannot have exactly one.  We ask whether three such abstract
systems can avoid every nonconstant rainbow partition of the vertex set.

UNSAT is a rigorous obstruction for diagonal edge matrices.  SAT merely
returns an abstract survivor; it need not be realizable by complex weights.
"""

from __future__ import annotations

import argparse
import itertools
import math

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver
import sympy as sp


def matching_of_cycle_type(n: int, cycle_type: tuple[int, ...]):
    """Representative relative to (01)(23)... for a partition of n/2."""
    assert sum(cycle_type) == n // 2 and all(part > 0 for part in cycle_type)
    answer = []
    first_pair = 0
    for part in cycle_type:
        pairs = tuple(range(first_pair, first_pair + part))
        first_pair += part
        if part == 1:
            pair = pairs[0]
            answer.append((2 * pair, 2 * pair + 1))
        else:
            for position, pair in enumerate(pairs):
                next_pair = pairs[(position + 1) % part]
                answer.append(tuple(sorted((2 * pair + 1, 2 * next_pair))))
    return tuple(sorted(answer))


def even_masks(n: int):
    return tuple(mask for mask in range(1 << n) if mask.bit_count() % 2 == 0)


def add_iff_and(cnf: CNF, y: int, literals: tuple[int, ...]):
    for literal in literals:
        cnf.append([-y, literal])
    cnf.append([y] + [-literal for literal in literals])


def add_not_exactly_one(cnf: CNF, guard_false: int, terms: list[int]):
    """If guard_false is true, forbid exactly one true term."""
    for index, term in enumerate(terms):
        cnf.append([-guard_false, -term] + terms[:index] + terms[index + 1:])


def build(
    n: int,
    fix_color_zero_matching: bool = False,
    *,
    use_pooled: bool = True,
    use_raw: bool = True,
    use_factorization: bool = True,
    color_one_cycle_type: tuple[int, ...] | None = None,
    color_two_cycle_type: tuple[int, ...] | None = None,
    min_recurrence_size: int = 0,
    recurrence_sizes: frozenset[int] | None = None,
):
    pool = IDPool()
    cnf = CNF()
    evens = even_masks(n)
    edges = tuple(itertools.combinations(range(n), 2))

    def z(r: int, mask: int):
        return pool.id(("z", r, mask))

    def w(r: int, edge: tuple[int, int]):
        return pool.id(("w", r, edge))

    for r in range(3):
        cnf.append([z(r, 0)])
        cnf.append([z(r, (1 << n) - 1)])
        for mask in evens:
            if mask == 0:
                continue
            terms = []
            vertices = tuple(v for v in range(n) if mask >> v & 1)
            for edge in itertools.combinations(vertices, 2):
                rest = mask ^ (1 << edge[0]) ^ (1 << edge[1])
                y = pool.id(("term", r, mask, edge))
                add_iff_and(cnf, y, (w(r, edge), z(r, rest)))
                terms.append(y)
            # z != 0 implies at least one nonzero summand.
            if use_pooled:
                cnf.append([-z(r, mask)] + terms)
                # z == 0 implies zero or >=2 nonzero summands.
                add_not_exactly_one(cnf, -z(r, mask), terms)

            # The same implications hold for the genuine Laplace expansion
            # at *each* pivot vertex u:
            #
            #   haf A[S] = sum_{v in S-u} a_uv haf A[S-{u,v}].
            #
            # Pooling all pairs above is useful but strictly weaker.  In
            # particular, a nonzero hafnian must have a nonzero recursive
            # term incident with every chosen pivot, while a zero hafnian
            # cannot have exactly one such term at any pivot.
            use_size = (
                len(vertices) == 2
                or (recurrence_sizes is not None and len(vertices) in recurrence_sizes)
                or (recurrence_sizes is None and len(vertices) >= min_recurrence_size)
            )
            if use_size:
                for pivot in vertices:
                    pivot_terms = [
                        pool.id(("term", r, mask, tuple(sorted((pivot, other)))))
                        for other in vertices
                        if other != pivot
                    ]
                    cnf.append([-z(r, mask)] + pivot_terms)
                    add_not_exactly_one(cnf, -z(r, mask), pivot_terms)

            # Direct expansion over perfect matchings is stronger than the
            # recursive-term relaxation when a complementary hafnian has
            # canceled.  Again, nonzero needs a term and zero forbids a
            # unique raw matching monomial.
            raw_terms = []
            vertices_tuple = tuple(vertices)

            def perfect_matchings(vs):
                if not vs:
                    yield ()
                    return
                first = vs[0]
                for pos in range(1, len(vs)):
                    second = vs[pos]
                    rest_vs = vs[1:pos] + vs[pos + 1:]
                    for tail in perfect_matchings(rest_vs):
                        yield ((first, second),) + tail

            for matching in perfect_matchings(vertices_tuple):
                y = pool.id(("raw", r, mask, matching))
                add_iff_and(cnf, y, tuple(w(r, tuple(sorted(edge))) for edge in matching))
                raw_terms.append(y)
            if use_raw:
                cnf.append([-z(r, mask)] + raw_terms)
                add_not_exactly_one(cnf, -z(r, mask), raw_terms)

        # If an even vertex set splits into two nonempty even shores with no
        # supported edge across, its hafnian factors exactly.  Encode the
        # corresponding conditional Boolean equivalence.
        if not use_factorization:
            continue
        for mask in evens:
            if mask == 0:
                continue
            first_vertex = (mask & -mask).bit_length() - 1
            submask = (mask - 1) & mask
            while submask:
                other = mask ^ submask
                if (submask >> first_vertex) & 1 and other and submask.bit_count() % 2 == 0:
                    left = tuple(v for v in range(n) if submask >> v & 1)
                    right = tuple(v for v in range(n) if other >> v & 1)
                    cross = [w(r, tuple(sorted((u, v)))) for u in left for v in right]
                    cnf.append(cross + [-z(r, mask), z(r, submask)])
                    cnf.append(cross + [-z(r, mask), z(r, other)])
                    cnf.append(cross + [-z(r, submask), -z(r, other), z(r, mask)])
                submask = (submask - 1) & mask

    # Since z(0,V) is nonzero, at least one raw perfect-matching monomial
    # of color zero is supported.  Vertex relabeling sends it to the
    # canonical matching without changing any condition in the formula.
    if fix_color_zero_matching:
        for u in range(0, n, 2):
            cnf.append([w(0, (u, u + 1))])
    if color_one_cycle_type is not None:
        assert fix_color_zero_matching
        for edge in matching_of_cycle_type(n, color_one_cycle_type):
            cnf.append([w(1, edge)])
    if color_two_cycle_type is not None:
        assert fix_color_zero_matching
        for edge in matching_of_cycle_type(n, color_two_cycle_type):
            cnf.append([w(2, edge)])

    # No nonconstant partition into three even feasible color classes.
    full = (1 << n) - 1
    for assignment in itertools.product(range(3), repeat=n):
        masks = [0, 0, 0]
        for v, r in enumerate(assignment):
            masks[r] |= 1 << v
        if any(mask.bit_count() % 2 for mask in masks):
            continue
        if any(mask == full for mask in masks):
            continue
        cnf.append([-z(0, masks[0]), -z(1, masks[1]), -z(2, masks[2])])
    return pool, cnf, z, w, evens, edges


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--cegar", action="store_true")
    parser.add_argument("--max-cuts", type=int, default=10000)
    parser.add_argument("--fix-color-zero-matching", action="store_true")
    parser.add_argument("--no-pooled", action="store_true")
    parser.add_argument("--no-raw", action="store_true")
    parser.add_argument("--no-factorization", action="store_true")
    parser.add_argument(
        "--color-one-cycle-type",
        help="comma-separated integer partition of n/2; requires the fixed color-zero matching",
    )
    parser.add_argument(
        "--color-two-cycle-type",
        help="comma-separated cycle type relative to the canonical matching",
    )
    parser.add_argument("--min-recurrence-size", type=int, default=0)
    parser.add_argument(
        "--recurrence-sizes",
        help="comma-separated even sizes; overrides --min-recurrence-size",
    )
    args = parser.parse_args()
    cycle_type = (
        tuple(map(int, args.color_one_cycle_type.split(",")))
        if args.color_one_cycle_type
        else None
    )
    cycle_type_two = (
        tuple(map(int, args.color_two_cycle_type.split(",")))
        if args.color_two_cycle_type
        else None
    )
    recurrence_sizes = (
        frozenset(map(int, args.recurrence_sizes.split(",")))
        if args.recurrence_sizes
        else None
    )
    pool, cnf, z, w, evens, edges = build(
        args.n,
        args.fix_color_zero_matching,
        use_pooled=not args.no_pooled,
        use_raw=not args.no_raw,
        use_factorization=not args.no_factorization,
        color_one_cycle_type=cycle_type,
        color_two_cycle_type=cycle_type_two,
        min_recurrence_size=args.min_recurrence_size,
        recurrence_sizes=recurrence_sizes,
    )
    with Solver(name="cadical195", bootstrap_with=cnf) as solver:
        cuts = 0
        while True:
            sat = solver.solve()
            if not sat or not args.cegar:
                break
            positive = set(lit for lit in solver.get_model() if lit > 0)
            equations = []
            for r in range(3):
                for mask in evens:
                    if mask == 0 or z(r, mask) in positive:
                        continue
                    vertices = tuple(v for v in range(args.n) if mask >> v & 1)

                    def pms(vs):
                        if not vs:
                            yield ()
                            return
                        first = vs[0]
                        for pos in range(1, len(vs)):
                            second = vs[pos]
                            rest = vs[1:pos] + vs[pos + 1:]
                            for tail in pms(rest):
                                yield ((first, second),) + tail

                    all_matchings = tuple(pms(vertices))
                    supported = [m for m in all_matchings
                                 if pool.id(("raw", r, mask, m)) in positive]
                    if len(supported) != 2:
                        continue
                    row = [0] * (3 * len(edges))
                    for sign, matching in ((1, supported[0]), (-1, supported[1])):
                        for edge in matching:
                            index = edges.index(tuple(sorted(edge)))
                            row[r * len(edges) + index] += sign
                    equations.append((r, mask, all_matchings, tuple(supported), row))
            relation = None
            if equations:
                matrix = sp.Matrix([item[4] for item in equations]).T
                for vector in matrix.nullspace():
                    denominator = math.lcm(*(term.q for term in vector))
                    integers = [int(term * denominator) for term in vector]
                    divisor = math.gcd(*integers)
                    integers = [value // divisor for value in integers]
                    if sum(integers) % 2:
                        relation = integers
                        break
            if relation is None:
                print(f"CEGAR survivor after {cuts} cuts: no odd primitive rational-kernel basis vector")
                break
            clause = []
            used = 0
            for coefficient, (r, mask, all_matchings, supported, _) in zip(relation, equations):
                if coefficient == 0:
                    continue
                used += 1
                clause.append(z(r, mask))
                supported_set = set(supported)
                for matching in all_matchings:
                    raw = pool.id(("raw", r, mask, matching))
                    clause.append(-raw if matching in supported_set else raw)
            solver.add_clause(clause)
            cuts += 1
            if cuts % 100 == 0:
                print(f"cuts={cuts} last_relation_equations={used}", flush=True)
            if cuts >= args.max_cuts:
                print(f"stopped at max cuts={cuts}")
                break
        print(f"n={args.n} vars={pool.top} clauses={len(cnf.clauses)} sat={sat}")
        if not sat:
            return
        model = set(lit for lit in solver.get_model() if lit > 0)
        for r in range(3):
            feasible_by_size = {
                k: sum(z(r, mask) in model for mask in evens if mask.bit_count() == k)
                for k in range(0, args.n + 1, 2)
            }
            supported_edges = [edge for edge in edges if w(r, edge) in model]
            print(f"color={r} feasible={feasible_by_size} edges={supported_edges}")
            canceled = []
            for mask in evens:
                if mask == 0 or z(r, mask) in model:
                    continue
                vertices = tuple(v for v in range(args.n) if mask >> v & 1)
                count = 0

                def pms(vs):
                    if not vs:
                        yield ()
                        return
                    first = vs[0]
                    for pos in range(1, len(vs)):
                        second = vs[pos]
                        rest = vs[1:pos] + vs[pos + 1:]
                        for tail in pms(rest):
                            yield ((first, second),) + tail

                for matching in pms(vertices):
                    if all(tuple(sorted(edge)) in supported_edges for edge in matching):
                        count += 1
                if count >= 2:
                    canceled.append((vertices, count))
            print(f"color={r} required_cancellations={canceled}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""CEGAR audit for the color-sensitive partition-rank deletion identity.

For each support chart in the rank-graph SAT relaxation, search over Q for
diagonal local operators whose sum fixes every constant-color target term
and which kill all but at most two aggregate edges.  Such a chart is
impossible because Delta_(6,3) has partition rank three.  Exact support
blocking clauses enumerate the remaining charts; no numerical linear algebra
is used.  For an exceptional triangle, the stronger witness kills every
outside edge and leaves each triangle matrix exactly unchanged.  The
exceptional-triangle rigidity lemma then forces those matrices to have rank
one; see proofs/exceptional-triangle-obstruction.md.
"""

from __future__ import annotations

import argparse
import itertools
from collections import Counter

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from pysat.solvers import Solver

import search_f5_support_sat as base
import verify_f4_support_obstruction as previous


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


FIELD_CHARACTERISTIC = 0


def equation_row(u, v, a, b):
    row = [0] * 18
    row[3 * u + a] = 1
    row[3 * v + b] = 1
    return row


SUM_ROWS = tuple(
    [int(index % 3 == color) for index in range(18)]
    for color in base.COLORS
)


def extract_supports(pool, model, exceptional):
    supports = {}
    for u, v in base.ALL_EDGES:
        if (u, v) in exceptional:
            cells = {
                (a, b)
                for a, b in base.CELLS
                if pool.id(("entry", (u, v), a, b)) in model
            }
        else:
            left = {
                a
                for a in base.COLORS
                if pool.id(("factor", v, u, a)) in model
            }
            right = {
                b
                for b in base.COLORS
                if pool.id(("factor", u, v, b)) in model
            }
            cells = set(itertools.product(left, right))
        if cells:
            supports[u, v] = cells
    return supports


def affine_consistent(supports, killed, fixed=()):
    rows = []
    rhs = []
    for u, v in killed:
        for a, b in supports[u, v]:
            rows.append(equation_row(u, v, a, b))
            rhs.append(0)
    for (u, v), value in fixed:
        for a, b in supports[u, v]:
            rows.append(equation_row(u, v, a, b))
            rhs.append(value)
    rows.extend(SUM_ROWS)
    rhs.extend((1, 1, 1))
    if FIELD_CHARACTERISTIC == 2:
        # Linear consistency over the algebraic closure of F_2 is the same
        # as consistency over F_2 itself.  Bit elimination avoids any
        # accidental use of rational stabilizers with even denominators.
        pivots = {}
        for row, value in zip(rows, rhs):
            bits = sum((entry & 1) << index for index, entry in enumerate(row))
            value &= 1
            while bits:
                pivot = bits.bit_length() - 1
                if pivot not in pivots:
                    pivots[pivot] = (bits, value)
                    break
                old_bits, old_value = pivots[pivot]
                bits ^= old_bits
                value ^= old_value
            else:
                if value:
                    return False
        return True
    matrix = sp.polys.matrices.DomainMatrix.from_list_sympy(
        len(rows), 18, rows
    ).to_field()
    augmented = sp.polys.matrices.DomainMatrix.from_list_sympy(
        len(rows), 19, [row + [value] for row, value in zip(rows, rhs)]
    ).to_field()
    return matrix.rank() == augmented.rank()


def can_kill(supports, killed):
    return affine_consistent(supports, killed)


def deletion_witness(supports):
    edges = tuple(supports)
    # It is enough to leave zero, one, or two of the active edges.  Testing
    # exactly two also covers smaller survivor sets by adding arbitrary edges.
    if len(edges) <= 2:
        return (), edges
    for survivors in itertools.combinations(edges, 2):
        killed = tuple(edge for edge in edges if edge not in survivors)
        if can_kill(supports, killed):
            return killed, survivors
    return None


def triangle_rank_witness(supports, exceptional):
    """Leave an exceptional triangle unchanged and kill every other edge."""
    edges = tuple(supports)
    for triangle in itertools.combinations(edges, 3):
        vertices = set().union(*[set(edge) for edge in triangle])
        degrees = {v: sum(v in edge for edge in triangle) for v in vertices}
        if len(vertices) != 3 or set(degrees.values()) != {2}:
            continue
        if not set(triangle) <= exceptional:
            continue
        killed = tuple(edge for edge in edges if edge not in triangle)
        if affine_consistent(
            supports, killed, tuple((edge, 1) for edge in triangle)
        ):
            return killed, triangle
    return None


def factor_support_at(supports, edge, vertex):
    """Recover one endpoint support from a rank-one Cartesian chart."""
    cells = supports[edge]
    if vertex == edge[0]:
        return {a for a, _ in cells}
    require(vertex == edge[1], f"vertex {vertex} is not an endpoint of {edge}")
    return {b for _, b in cells}


def rainbow_triangle_cofactor_witness(supports, exceptional):
    """Detect a fixed rainbow triangle with an impossible pure cofactor.

    A color-sensitive stabilizer may kill every outside edge while fixing a
    triangle.  Three-term rigidity then makes its three rank-one matrices
    distinct same-color basis cells and makes each complementary H4 tensor
    pure in that color.  The quotient test below recognizes a conservative
    support pattern for which the three rank-one matching terms of such an
    H4 tensor cannot sum to a pure tensor.
    """
    if exceptional:
        return None
    all_vertices = set(base.VERTICES)
    for triangle_vertices in itertools.combinations(base.VERTICES, 3):
        triangle = tuple(itertools.combinations(triangle_vertices, 2))
        killed = tuple(edge for edge in supports if edge not in triangle)
        if not affine_consistent(
            supports, killed, tuple((edge, 1) for edge in triangle)
        ):
            continue
        edge_colors = {}
        valid_rainbow = True
        for edge in triangle:
            cells = supports.get(edge, set())
            if len(cells) != 1:
                valid_rainbow = False
                break
            (a, b), = cells
            if a != b:
                valid_rainbow = False
                break
            edge_colors[edge] = a
        if not valid_rainbow or set(edge_colors.values()) != set(base.COLORS):
            # The fixed-triangle rigidity lemma already contradicts a
            # non-rainbow support, but that more general cut is kept out of
            # this support-only detector until its orbit certificate is
            # separately audited.
            continue

        for triangle_edge, target_color in edge_colors.items():
            complement = tuple(sorted(all_vertices - set(triangle_edge)))
            terms = tuple(perfect_matchings(complement))
            require(len(terms) == 3, f"complement has {len(terms)} matchings, expected 3")
            local_supports = []
            for matching in terms:
                local_supports.append(
                    {
                        vertex: factor_support_at(
                            supports,
                            next(edge for edge in matching if vertex in edge),
                            vertex,
                        )
                        for vertex in complement
                    }
                )

            for center in complement:
                for singled in range(3):
                    if local_supports[singled][center] != {target_color}:
                        continue
                    other = tuple(index for index in range(3) if index != singled)
                    if any(
                        local_supports[index][center] <= {target_color}
                        for index in other
                    ):
                        continue

                    remaining = tuple(v for v in complement if v != center)
                    # Projecting the center modulo the target axis makes the
                    # two other nonzero pure tensors cancel.  Their factors
                    # at every remaining mode must therefore be proportional.
                    unequal = next(
                        (
                            vertex
                            for vertex in remaining
                            if local_supports[other[0]][vertex]
                            != local_supports[other[1]][vertex]
                        ),
                        None,
                    )
                    if unequal is not None:
                        return triangle, triangle_edge, center, singled, "unequal"

                    for quotient_vertex in remaining:
                        common = local_supports[other[0]][quotient_vertex]
                        if common == {target_color}:
                            continue
                        if any(
                            local_supports[singled][third] != {target_color}
                            for third in remaining
                            if third != quotient_vertex
                        ):
                            return (
                                triangle,
                                triangle_edge,
                                center,
                                singled,
                                "two-quotient",
                            )
    return None


def perfect_matchings(vertices=tuple(base.VERTICES)):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings())


def supported_fiber(supports, coloring):
    return tuple(
        matching
        for matching in MATCHINGS
        if all((coloring[u], coloring[v]) in supports.get((u, v), set()) for u, v in matching)
    )


def cycle_cancellation_witness(supports, exceptional):
    """Detect two universal rank-one PMs forced to cancel identically.

    This is used only when every edge is rank one.  A two-term mixed fiber
    says the ratio of the two matching monomials is -1.  Pairs of such
    fibers differing at one vertex force every local factor in that ratio to
    be color-independent.  A mixed three-term fiber then leaves one nonzero
    monomial after the universal pair cancels.
    """
    if any(supports.get(edge) for edge in exceptional):
        return None
    full = set(itertools.product(base.COLORS, repeat=2))
    universal = tuple(
        matching
        for matching in MATCHINGS
        if all(supports.get(edge) == full for edge in matching)
    )
    colorings = tuple(itertools.product(base.COLORS, repeat=6))
    fibers = {coloring: supported_fiber(supports, coloring) for coloring in colorings}
    for first, second in itertools.combinations(universal, 2):
        pair = {first, second}
        variation_witnesses = []
        valid = True
        for vertex in base.VERTICES:
            for target_color in (1, 2):
                found = None
                for coloring in colorings:
                    if coloring[vertex] != 0 or len(set(coloring)) == 1:
                        continue
                    changed = list(coloring)
                    changed[vertex] = target_color
                    changed = tuple(changed)
                    if len(set(changed)) == 1:
                        continue
                    if set(fibers[coloring]) == pair and set(fibers[changed]) == pair:
                        found = (coloring, changed)
                        break
                if found is None:
                    valid = False
                    break
                variation_witnesses.append(found)
            if not valid:
                break
        if not valid:
            continue
        for coloring in colorings:
            fiber = fibers[coloring]
            if len(set(coloring)) > 1 and len(fiber) == 3 and pair <= set(fiber):
                return first, second, tuple(variation_witnesses), coloring, fiber
    return None


def rectangle_cancellation_witness(supports, exceptional):
    """Find a constant corner forced to cancel by three mixed corners.

    When every matrix is rank one, the ratio of the monomials of two fixed
    perfect matchings factors vertex-by-vertex.  Hence on any two-coloring
    coordinate rectangle its four values obey the multiplicative rectangle
    identity.  If the same two matchings are the exact supported fiber at
    all four corners, three mixed zero coefficients force ratio -1 there;
    the fourth, constant corner then also has ratio -1 and vanishes.
    """
    if any(supports.get(edge) for edge in exceptional):
        return None
    colorings = tuple(itertools.product(base.COLORS, repeat=6))
    fibers = {coloring: supported_fiber(supports, coloring) for coloring in colorings}
    for constant_color in base.COLORS:
        constant = (constant_color,) * 6
        pair = fibers[constant]
        if len(pair) != 2:
            continue
        for first_vertex, second_vertex in itertools.combinations(base.VERTICES, 2):
            for first_color in base.COLORS:
                if first_color == constant_color:
                    continue
                for second_color in base.COLORS:
                    if second_color == constant_color:
                        continue
                    first_changed = list(constant)
                    first_changed[first_vertex] = first_color
                    second_changed = list(constant)
                    second_changed[second_vertex] = second_color
                    both_changed = list(first_changed)
                    both_changed[second_vertex] = second_color
                    corners = (
                        tuple(first_changed),
                        tuple(second_changed),
                        tuple(both_changed),
                    )
                    if all(fibers[coloring] == pair for coloring in corners):
                        return pair, constant, corners
    return None


def char2_binomial_parity_witness(supports, signatures):
    """Reduce odd mixed fibers modulo all exact binomial equalities.

    In characteristic two, a mixed fiber with exactly two supported
    monomials identifies those Laurent monomials.  When their exponent
    lattice is saturated, rational row-space equality is exact integer
    lattice equality.  If an odd mixed fiber has exactly one quotient class
    of odd multiplicity, all other classes cancel pairwise and one nonzero
    Laurent monomial remains.
    """
    if FIELD_CHARACTERISTIC != 2:
        return None
    fibers = {
        coloring: tuple(
            MATCHING_INDEX[frozenset(matching)]
            for matching in supported_fiber(supports, coloring)
        )
        for coloring in itertools.product(base.COLORS, repeat=6)
    }
    rows = []
    binomial_colorings = []
    for coloring, supported in fibers.items():
        if len(set(coloring)) == 1 or len(supported) != 2:
            continue
        first, second = supported
        rows.append(
            [
                a - b
                for a, b in zip(
                    signatures[coloring, second],
                    signatures[coloring, first],
                    strict=True,
                )
            ]
        )
        binomial_colorings.append(coloring)
    if not rows:
        return None

    matrix = sp.Matrix(rows)
    smith = smith_normal_form(matrix, domain=ZZ)
    invariant_factors = [
        abs(int(smith[index, index]))
        for index in range(min(smith.shape))
        if smith[index, index]
    ]
    # This conservative detector declines nonsaturated lattices rather than
    # making an invalid root-extraction inference.
    if any(factor != 1 for factor in invariant_factors):
        return None
    reduced, pivots = matrix.rref()

    def quotient_class(vector):
        answer = [sp.Rational(value) for value in vector]
        for row_index, pivot in enumerate(pivots):
            coefficient = answer[pivot]
            if coefficient:
                answer = [
                    value - coefficient * reduced[row_index, column]
                    for column, value in enumerate(answer)
                ]
        return tuple(answer)

    for coloring, supported in fibers.items():
        if len(set(coloring)) == 1 or len(supported) < 3 or len(supported) % 2 == 0:
            continue
        parity = Counter(
            quotient_class(signatures[coloring, index]) for index in supported
        )
        odd_classes = tuple(key for key, count in parity.items() if count % 2)
        if len(odd_classes) == 1:
            return (
                coloring,
                supported,
                len(rows),
                len(invariant_factors),
                tuple(binomial_colorings),
            )
    return None


def support_variables(pool, exceptional):
    variables = []
    for edge in base.ALL_EDGES:
        if edge in exceptional:
            variables.extend(
                pool.id(("entry", edge, a, b)) for a, b in base.CELLS
            )
        else:
            u, v = edge
            variables.extend(
                pool.id(("factor", v, u, a)) for a in base.COLORS
            )
            variables.extend(
                pool.id(("factor", u, v, b)) for b in base.COLORS
            )
    return tuple(variables)


def graph_automorphisms(exceptional):
    answer = []
    for permutation in itertools.permutations(base.VERTICES):
        image = {
            tuple(sorted((permutation[u], permutation[v])))
            for u, v in exceptional
        }
        if image == exceptional:
            answer.append(permutation)
    return tuple(answer)


def transform_supports(supports, vertex_permutation, color_permutation):
    answer = {}
    for (u, v), cells in supports.items():
        uu, vv = vertex_permutation[u], vertex_permutation[v]
        mapped = {(color_permutation[a], color_permutation[b]) for a, b in cells}
        if uu > vv:
            uu, vv = vv, uu
            mapped = {(b, a) for a, b in mapped}
        answer[uu, vv] = mapped
    return answer


MATCHING_INDEX = {
    frozenset(matching): index for index, matching in enumerate(MATCHINGS)
}


def transform_fiber(coloring, supported, vertex_permutation, color_permutation):
    """Transport one exact coefficient-fiber pattern by a chart symmetry."""
    mapped_coloring = [None] * len(base.VERTICES)
    for vertex, color in enumerate(coloring):
        mapped_coloring[vertex_permutation[vertex]] = color_permutation[color]
    mapped_supported = []
    for matching in supported:
        mapped_matching = frozenset(
            tuple(sorted((vertex_permutation[u], vertex_permutation[v])))
            for u, v in matching
        )
        mapped_supported.append(MATCHING_INDEX[mapped_matching])
    return tuple(mapped_coloring), tuple(sorted(mapped_supported))


def exact_fiber_block(pool, coloring, supported_indices):
    """One clause negating an exact supported-matching fiber."""
    supported_indices = set(supported_indices)
    return [
        (
            -pool.id(("monomial", coloring, index))
            if index in supported_indices
            else pool.id(("monomial", coloring, index))
        )
        for index in range(len(MATCHINGS))
    ]


def fiber_witness_orbit_clauses(
    pool,
    automorphisms,
    fiber_patterns,
):
    """Forbid a conjunction of exact fibers throughout its symmetry orbit."""
    clauses = set()
    for vertex_permutation in automorphisms:
        for color_permutation in itertools.permutations(base.COLORS):
            clause = []
            for coloring, supported in fiber_patterns:
                mapped_coloring, mapped_supported = transform_fiber(
                    coloring,
                    supported,
                    vertex_permutation,
                    color_permutation,
                )
                clause.extend(
                    exact_fiber_block(
                        pool, mapped_coloring, mapped_supported
                    )
                )
            clauses.add(tuple(clause))
    return clauses


def exact_support_clause(pool, exceptional, supports):
    clause = []
    for edge in base.ALL_EDGES:
        cells = supports.get(edge, set())
        if edge in exceptional:
            for a, b in base.CELLS:
                variable = pool.id(("entry", edge, a, b))
                clause.append(-variable if (a, b) in cells else variable)
        else:
            u, v = edge
            left = {a for a, _ in cells}
            right = {b for _, b in cells}
            for a in base.COLORS:
                variable = pool.id(("factor", v, u, a))
                clause.append(-variable if a in left else variable)
            for b in base.COLORS:
                variable = pool.id(("factor", u, v, b))
                clause.append(-variable if b in right else variable)
    return clause


def subsupport_escape_clause(pool, exceptional, supports):
    """Forbid every chart whose coordinate support is contained in ``supports``.

    The deletion and exceptional-triangle witnesses are monotone under
    deleting supported entries/factor coordinates: the same alpha still
    kills the same outside edges and retains at most the same summands.
    Hence a future chart can escape such a witness only by switching on a
    coordinate that is absent from the current chart.  This stronger clause
    is exact for those two witness kinds and avoids enumerating all their
    subcharts one at a time.
    """
    clause = []
    for edge in base.ALL_EDGES:
        cells = supports.get(edge, set())
        if edge in exceptional:
            for a, b in base.CELLS:
                if (a, b) not in cells:
                    clause.append(pool.id(("entry", edge, a, b)))
        else:
            u, v = edge
            left = {a for a, _ in cells}
            right = {b for _, b in cells}
            for a in base.COLORS:
                if a not in left:
                    clause.append(pool.id(("factor", v, u, a)))
            for b in base.COLORS:
                if b not in right:
                    clause.append(pool.id(("factor", u, v, b)))
    return clause


def audit(name, exceptional, limit=100000, artifact_sink=None):
    formula, pool, _active = base.support_formula(exceptional)
    signatures = previous.formal_signatures(exceptional, pool)
    support_vars = support_variables(pool, exceptional)
    automorphisms = graph_automorphisms(exceptional)
    blocks = 0
    transfers = 0
    witness_counts = Counter()
    semantic_records = []
    recorded_clauses = [list(clause) for clause in formula.clauses]

    def conclude(value):
        if artifact_sink is not None:
            artifact_sink.clear()
            artifact_sink.update(
                records=semantic_records,
                variables=pool.top,
                clauses=recorded_clauses,
                support_blocks=blocks,
                transfers=transfers,
                witness_counts=dict(witness_counts),
            )
        return value

    with Solver(name="cadical195", bootstrap_with=formula) as solver:
        while solver.solve():
            model = {literal for literal in solver.get_model() if literal > 0}
            supports = extract_supports(pool, model, exceptional)
            witness = deletion_witness(supports)
            witness_kind = "partition-rank"
            if witness is None:
                witness = triangle_rank_witness(supports, exceptional)
                witness_kind = "triangle-rank"
            cycle_witness = None
            rectangle_witness = None
            rainbow_witness = None
            char2_witness = None
            if witness is None:
                rainbow_witness = rainbow_triangle_cofactor_witness(
                    supports, exceptional
                )
                if rainbow_witness is not None:
                    witness = ((), rainbow_witness[0])
                    witness_kind = "rainbow-triangle-cofactor"
            if witness is None:
                rectangle_witness = rectangle_cancellation_witness(
                    supports, exceptional
                )
                if rectangle_witness is not None:
                    witness = ((), rectangle_witness[0])
                    witness_kind = "rectangle-cancellation"
            if witness is None:
                cycle_witness = cycle_cancellation_witness(supports, exceptional)
                if cycle_witness is not None:
                    witness = ((), cycle_witness[:2])
                    witness_kind = "cycle-cancellation"
            if witness is None:
                char2_witness = char2_binomial_parity_witness(
                    supports, signatures
                )
                if char2_witness is not None:
                    witness = ((), char2_witness[1])
                    witness_kind = "char2-binomial-parity"
            if witness is None:
                added = previous.add_cancellation_transfers(
                    solver, pool, signatures, clause_sink=recorded_clauses
                )
                survives, count = added
                transfers += count
                if not survives:
                    print(
                        f"{name}: UNSAT; support_blocks={blocks}, "
                        f"transfers={transfers}, "
                        f"witnesses={dict(witness_counts)}"
                    )
                    return conclude(True)
                model = {
                    literal for literal in solver.get_model() if literal > 0
                }
                supports = extract_supports(pool, model, exceptional)
                witness = deletion_witness(supports)
                witness_kind = "partition-rank"
                rectangle_witness = None
                cycle_witness = None
                rainbow_witness = None
                char2_witness = None
                if witness is None:
                    witness = triangle_rank_witness(supports, exceptional)
                    witness_kind = "triangle-rank"
                if witness is None:
                    rainbow_witness = rainbow_triangle_cofactor_witness(
                        supports, exceptional
                    )
                    if rainbow_witness is not None:
                        witness = ((), rainbow_witness[0])
                        witness_kind = "rainbow-triangle-cofactor"
                if witness is None:
                    rectangle_witness = rectangle_cancellation_witness(
                        supports, exceptional
                    )
                    if rectangle_witness is not None:
                        witness = ((), rectangle_witness[0])
                        witness_kind = "rectangle-cancellation"
                if witness is None:
                    cycle_witness = cycle_cancellation_witness(supports, exceptional)
                    if cycle_witness is not None:
                        witness = ((), cycle_witness[:2])
                        witness_kind = "cycle-cancellation"
                if witness is None:
                    char2_witness = char2_binomial_parity_witness(
                        supports, signatures
                    )
                    if char2_witness is not None:
                        witness = ((), char2_witness[1])
                        witness_kind = "char2-binomial-parity"
                if witness is None:
                    triple = None
                    edges = tuple(supports)
                    for survivors3 in itertools.combinations(edges, 3):
                        killed3 = tuple(edge for edge in edges if edge not in survivors3)
                        if can_kill(supports, killed3):
                            triple = survivors3
                            break
                    print(
                        f"{name}: survivor; support_blocks={blocks}, "
                        f"transfers={transfers}, active={len(supports)}, "
                        f"three_survivors={triple}"
                    )
                    print(f"{name}: supports={dict(sorted(supports.items()))}")
                    return conclude(False)
            witness_counts[witness_kind] += 1
            semantic_records.append(
                {
                    "kind": witness_kind,
                    "supports": tuple(
                        (edge, tuple(sorted(cells)))
                        for edge, cells in sorted(supports.items())
                    ),
                }
            )
            if witness_kind == "rectangle-cancellation":
                pair, constant, corners = rectangle_witness
                patterns = tuple(
                    (coloring, pair)
                    for coloring in (constant,) + tuple(corners)
                )
                orbit_clauses = fiber_witness_orbit_clauses(
                    pool, automorphisms, patterns
                )
            elif witness_kind == "cycle-cancellation":
                first, second, variations, coloring, fiber = cycle_witness
                pair = (first, second)
                patterns = []
                for before, after in variations:
                    patterns.extend(((before, pair), (after, pair)))
                patterns.append((coloring, fiber))
                orbit_clauses = fiber_witness_orbit_clauses(
                    pool, automorphisms, tuple(patterns)
                )
            else:
                orbit_clauses = set()
                for vertex_permutation in automorphisms:
                    for color_permutation in itertools.permutations(base.COLORS):
                        mapped = transform_supports(
                            supports, vertex_permutation, color_permutation
                        )
                        if witness_kind in {"partition-rank", "triangle-rank"}:
                            clause = subsupport_escape_clause(
                                pool, exceptional, mapped
                            )
                        else:
                            clause = exact_support_clause(
                                pool, exceptional, mapped
                            )
                        orbit_clauses.add(tuple(clause))
            for clause in orbit_clauses:
                solver.add_clause(list(clause))
                recorded_clauses.append(list(clause))
            blocks += 1
            if blocks <= 5 or blocks % 100 == 0:
                killed, survivors = witness
                print(
                    f"{name}: block={blocks}, kind={witness_kind}, "
                    f"killed={len(killed)}, "
                    f"survivors={survivors}, orbit={len(orbit_clauses)}",
                    flush=True,
                )
            require(blocks < limit, f"support block limit {limit} exhausted")
    print(
        f"{name}: UNSAT; support_blocks={blocks}, transfers={transfers}, "
        f"witnesses={dict(witness_counts)}"
    )
    return conclude(True)


def main():
    cases = (
        ("C3+3P1", {(0, 1), (0, 2), (1, 2)}),
        ("P4+2P1", {(0, 1), (1, 2), (2, 3)}),
        ("P3+P2+P1", {(0, 1), (1, 2), (3, 4)}),
        ("2P2+2P1", {(0, 1), (2, 3)}),
        ("P3+3P1", {(0, 1), (1, 2)}),
        ("P2+4P1", {(0, 1)}),
        ("empty", set()),
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--only",
        choices=tuple(name for name, _ in cases),
        help="run just one named exceptional-graph audit",
    )
    parser.add_argument(
        "--characteristic-two",
        action="store_true",
        help="perform all color-sensitive affine consistency tests over F_2",
    )
    args = parser.parse_args()
    global FIELD_CHARACTERISTIC
    FIELD_CHARACTERISTIC = 2 if args.characteristic_two else 0
    for name, exceptional in cases:
        if args.only is not None and name != args.only:
            continue
        audit(name, exceptional)


if __name__ == "__main__":
    main()

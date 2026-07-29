#!/usr/bin/env python3
"""Exact support audit for a coordinate K_{4,4} complement chart.

Fix the identity perfect matching F in K_{4,4}.  Every edge outside F is
assumed to be a nonzero coordinate rank-one matrix.  At both bipartition
classes, the endpoint labels of these twelve edges are assumed to be proper
3-edge-colourings of K_{4,4}-F.  The four matrices on F have arbitrary
zero/nonzero supports.

The audit asks only two necessary conditions for an exact GHZ_3 tensor:

* each of the three constant colourings has a supported perfect matching;
* no mixed colouring has exactly one supported perfect matching.

All cases are UNSAT.  Thus the chart is excluded before using numerical
weights or cancellation ratios.
"""

from __future__ import annotations

from itertools import combinations, permutations, product

try:
    from pysat.solvers import Solver
except ImportError as error:  # pragma: no cover - dependency diagnostic
    raise SystemExit(
        "python-sat is required; run with "
        "`uv run --with python-sat python computations/"
        "verify_k44_coordinate_complement_obstruction.py`"
    ) from error


Q = 3
N = 4
PERMUTATIONS = tuple(permutations(range(N)))
DERANGEMENTS = tuple(
    permutation
    for permutation in PERMUTATIONS
    if all(permutation[index] != index for index in range(N))
)


def one_factorizations():
    """The four unordered one-factorizations of K_{4,4}-F."""

    all_edges = {(left, right) for left in range(N) for right in range(N)
                 if left != right}
    answer = []
    for indices in combinations(range(len(DERANGEMENTS)), Q):
        factors = tuple(DERANGEMENTS[index] for index in indices)
        edge_sets = [
            {(left, factor[left]) for left in range(N)} for factor in factors
        ]
        if set().union(*edge_sets) == all_edges and sum(map(len, edge_sets)) == 12:
            answer.append(factors)
    assert len(answer) == 4
    return tuple(answer)


FACTORIZATIONS = one_factorizations()


def colored_factorization(factorization, color_order=(0, 1, 2)):
    labels = {}
    for factor_number, factor in enumerate(factorization):
        color = color_order[factor_number]
        for left, right in enumerate(factor):
            labels[left, right] = color
    assert len(labels) == 12
    return labels


class VariablePool:
    def __init__(self):
        self.top = 0

    def new(self):
        self.top += 1
        return self.top


def fixed_cell(pool, left, left_color, right_color):
    """Variable for cell (left_color,right_color) on F-edge left--left."""

    return 1 + left * Q * Q + left_color * Q + right_color


def build_formula(left_labels, right_labels):
    # Variables 1,...,36 are the arbitrary supports of the four F matrices.
    pool = VariablePool()
    pool.top = N * Q * Q
    clauses: list[list[int]] = []

    for left_colors in product(range(Q), repeat=N):
        for right_colors in product(range(Q), repeat=N):
            supported = []
            for matching in PERMUTATIONS:
                requirements = []
                compatible = True
                for left, right in enumerate(matching):
                    if left == right:
                        requirements.append(
                            fixed_cell(
                                pool,
                                left,
                                left_colors[left],
                                right_colors[right],
                            )
                        )
                    elif (
                        left_labels[left, right] != left_colors[left]
                        or right_labels[left, right] != right_colors[right]
                    ):
                        compatible = False
                        break
                if not compatible:
                    continue

                requirements = sorted(set(requirements))
                witness = pool.new()
                supported.append(witness)
                # witness <=> conjunction(requirements).  An empty
                # conjunction is true, as required for a D-only matching.
                clauses.extend([-witness, cell] for cell in requirements)
                clauses.append([witness] + [-cell for cell in requirements])

            is_constant = len(set(left_colors + right_colors)) == 1
            if is_constant:
                clauses.append(supported)
            else:
                # If one matching is supported, some distinct compatible
                # matching must also be supported to cancel its monomial.
                clauses.extend(
                    [-witness]
                    + [other for other in supported if other != witness]
                    for witness in supported
                )

    return pool.top, clauses


def run():
    # Simultaneous index conjugation has two orbits on the four
    # factorizations: the all-double-transposition factorization and the
    # other three.  A global output-colour permutation fixes the left colour
    # order.  The right side still ranges over all four factorizations and
    # all six colour orders: 2*4*6=48 exact orbit representatives.
    left_representatives = (FACTORIZATIONS[0], FACTORIZATIONS[1])
    cases = 0
    for left_type, left_factorization in enumerate(left_representatives):
        left_labels = colored_factorization(left_factorization)
        for right_type, right_factorization in enumerate(FACTORIZATIONS):
            for color_order in permutations(range(Q)):
                right_labels = colored_factorization(
                    right_factorization, color_order
                )
                variables, clauses = build_formula(left_labels, right_labels)
                with Solver(name="cadical195", bootstrap_with=clauses) as solver:
                    satisfiable = solver.solve()
                print(
                    f"left={left_type} right={right_type} "
                    f"colors={color_order}: "
                    f"{'SAT' if satisfiable else 'UNSAT'} "
                    f"({variables} variables, {len(clauses)} clauses)"
                )
                assert not satisfiable
                cases += 1
    assert cases == 48
    print("verified: all 48 symmetry classes are UNSAT")


if __name__ == "__main__":
    run()

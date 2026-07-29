#!/usr/bin/env python3
"""Exact audit of the exposed-grid obstruction for two equality geometries.

The algebraic proof is in
``notes/rank-budget-path-triangle-exposed-grid-obstruction.md``.  This
checker verifies the symbolic branches of the crossed-target lemma, builds
the complete quotient grids directly from the omission sets, and exhausts
the resulting pure endpoint-type constraints.  It makes no matching-term
support assumption.
"""

from itertools import product

import sympy as sp


def phi(left, right):
    """Phi((P,S),(P',S')) = P S'^t + P' S^t."""
    p, s = left
    q, t = right
    return p * t.T + q * s.T


def audit_crossed_target_algebra():
    """Check every non-pure branch in the crossed-target lemma."""
    p = sp.Matrix(sp.symbols("p0:3"))
    s = sp.Matrix(sp.symbols("s0:3"))
    q = sp.Matrix(sp.symbols("q0:3"))
    t = sp.Matrix(sp.symbols("t0:3"))
    lam, mu = sp.symbols("lambda mu", nonzero=True)

    mixed = (p, s)
    mixed_antipode = (lam * p, -lam * s)
    other_mixed = (q, t)
    other_antipode = (mu * q, -mu * t)

    first_target = phi(mixed, other_mixed)
    second_target = phi(mixed_antipode, other_antipode)
    proportional_residual = (second_target + lam * mu * first_target).applyfunc(
        sp.expand
    )
    assert proportional_residual == sp.zeros(3)

    # If the second zero-pair is pure P, the two target matrices share one
    # right factor.  If it is pure S, they share one left factor.  Distinct
    # diagonal units have neither property.  The ranks below are exact.
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            eii = sp.zeros(3)
            ejj = sp.zeros(3)
            eii[i, i] = 1
            ejj[j, j] = 1
            assert eii.col_join(ejj).rank() == 2  # no common right factor
            assert eii.row_join(ejj).rank() == 2  # no common left factor
            assert sp.Matrix.hstack(
                sp.Matrix(eii).reshape(9, 1),
                sp.Matrix(ejj).reshape(9, 1),
            ).rank() == 2  # not proportional


def pair(left, right):
    return frozenset((left, right))


def exposed_grid(omissions, omitted_pairs):
    """Return target and zero point-pairs in every typed double quotient."""
    targets = {}
    zeros = set()
    for colour, (left_site, right_site) in omitted_pairs.items():
        for left_colour in omissions[left_site]:
            for right_colour in omissions[right_site]:
                cell = pair(
                    (left_site, left_colour),
                    (right_site, right_colour),
                )
                if left_colour == right_colour == colour:
                    assert cell not in targets
                    targets[cell] = colour
                else:
                    zeros.add(cell)
    assert len(targets) == 3
    assert not (set(targets) & zeros)
    return targets, zeros


def crossed_pair_is_exposed(targets, zeros, first_colour, second_colour,
                            cross_one, cross_two):
    target_by_colour = {
        colour: edge for edge, colour in targets.items()
    }
    assert pair(*cross_one) in zeros
    assert pair(*cross_two) in zeros
    first = target_by_colour[first_colour]
    second = target_by_colour[second_colour]
    assert set(cross_one) <= set(first | second)
    assert set(cross_two) <= set(first | second)


def pure_type_solutions(targets, zeros):
    """Enumerate P/S types after crossed-target purity is established."""
    points = tuple(sorted(set().union(*targets)))
    assert len(points) == 6
    solutions = []
    for bits in product((0, 1), repeat=len(points)):
        endpoint_type = dict(zip(points, bits, strict=True))
        # A nonzero target joins opposite pure endpoint types.  A zero Phi
        # between nonzero pure points joins equal types.
        if any(
            endpoint_type[left] == endpoint_type[right]
            for left, right in map(tuple, targets)
        ):
            continue
        if any(
            endpoint_type[left] != endpoint_type[right]
            for left, right in map(tuple, zeros)
        ):
            continue
        solutions.append(endpoint_type)
    return solutions


def audit_path():
    omissions = {
        "A": (0,),
        "B": (0, 1),
        "C": (1, 2),
        "D": (2,),
        "E": (),
        "F": (),
    }
    omitted_pairs = {0: ("A", "B"), 1: ("B", "C"), 2: ("C", "D")}
    targets, zeros = exposed_grid(omissions, omitted_pairs)
    assert len(zeros) == 5

    crossed_pair_is_exposed(
        targets, zeros, 0, 1,
        (("A", 0), ("B", 1)),
        (("B", 0), ("C", 1)),
    )
    crossed_pair_is_exposed(
        targets, zeros, 1, 2,
        (("B", 1), ("C", 2)),
        (("C", 1), ("D", 2)),
    )
    assert pair(("B", 0), ("C", 2)) in zeros
    assert pure_type_solutions(targets, zeros) == []


def audit_triangle():
    omissions = {
        "A": (0, 2),
        "B": (0, 1),
        "C": (1, 2),
        "D": (),
        "E": (),
        "F": (),
    }
    omitted_pairs = {0: ("A", "B"), 1: ("B", "C"), 2: ("C", "A")}
    targets, zeros = exposed_grid(omissions, omitted_pairs)
    assert len(zeros) == 9

    crossed_pair_is_exposed(
        targets, zeros, 0, 1,
        (("A", 0), ("B", 1)),
        (("B", 0), ("C", 1)),
    )
    crossed_pair_is_exposed(
        targets, zeros, 1, 2,
        (("B", 1), ("C", 2)),
        (("C", 1), ("A", 2)),
    )
    crossed_pair_is_exposed(
        targets, zeros, 2, 0,
        (("C", 2), ("A", 0)),
        (("A", 2), ("B", 0)),
    )
    assert pair(("B", 0), ("C", 2)) in zeros
    assert pure_type_solutions(targets, zeros) == []


def audit_wedge_frontier():
    """The same exposed clauses remain consistent for wedge plus disjoint."""
    omissions = {
        "A": (0,),
        "B": (0, 1),
        "C": (1,),
        "D": (2,),
        "E": (2,),
        "F": (),
    }
    omitted_pairs = {0: ("A", "B"), 1: ("B", "C"), 2: ("D", "E")}
    targets, zeros = exposed_grid(omissions, omitted_pairs)
    assert len(zeros) == 2
    solutions = pure_type_solutions(targets, zeros)
    assert len(solutions) == 4


def main():
    audit_crossed_target_algebra()
    audit_path()
    audit_triangle()
    audit_wedge_frontier()
    print("crossed-target algebraic branches: exact PASS")
    print("three-edge path exposed grid: 3 targets, 5 zeros, UNSAT")
    print("triangle exposed grid: 3 targets, 9 zeros, UNSAT")
    print("wedge plus disjoint exposed grid: 4 pure-type assignments remain")


if __name__ == "__main__":
    main()

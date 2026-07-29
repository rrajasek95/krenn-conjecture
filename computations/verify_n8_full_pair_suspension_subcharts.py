#!/usr/bin/env python3
"""Exact audits for two fixed six-site pair-suspension subcharts.

For a quadratic ``q`` on six physical sites put

    H_q(Z) = Z q^2 / 2.

The full two-deleted-vertex equations for an eight-site ternary source are

    H_q(a_cd q + 3 p_c s_d) = delta_cd X_c.                 (1)

This script checks two finite certificates concerning (1).

* For the rational ``q`` in ``paircap_example`` it checks a 17-coordinate
  functional which annihilates the entire image of H_q but is nonzero on
  each of X_0, X_1, X_2.
* For the sparse three-completed-matchings ``q`` it checks that, modulo the
  one coordinate H_q(q), the 27 coefficients exposed by the site pairs
  01, 02, 12 are independent singleton rows.  Those rows give the triangle
  of symmetrized rank-one equations used in the accompanying proof.

All arithmetic is rational.  This is a fixed-q subchart audit, not an
exhaustive search over eight-site sources.
"""

from __future__ import annotations

import itertools
from fractions import Fraction as F

from verify_polarized_paircap_counterexample import (
    COLORINGS,
    EDGES,
    paircap_example,
    polarized_coefficients,
    unrestricted_example,
)


CELLS = tuple((edge, a, b) for edge in EDGES for a in range(3) for b in range(3))


# The entries are coefficients of output colorings.  Omitted colorings have
# coefficient zero.  Multiplying by six gives an integral certificate.
RATIONAL_LEFT_CERTIFICATE = {
    (0, 0, 0, 0, 0, 0): F(1),
    (0, 1, 1, 0, 0, 1): F(-1, 2),
    (0, 1, 1, 0, 1, 1): F(1),
    (0, 2, 0, 0, 0, 0): F(1),
    (1, 0, 0, 1, 1, 0): F(-1),
    (1, 1, 1, 1, 1, 1): F(-1, 2),
    (1, 1, 2, 1, 1, 1): F(-1, 2),
    (1, 2, 0, 1, 1, 0): F(-1),
    (2, 0, 1, 1, 0, 2): F(-1, 6),
    (2, 0, 1, 1, 1, 2): F(1, 6),
    (2, 0, 1, 2, 2, 2): F(-1, 2),
    (2, 0, 2, 1, 1, 2): F(-1, 6),
    (2, 2, 1, 1, 0, 2): F(-1, 6),
    (2, 2, 1, 1, 1, 2): F(1, 6),
    (2, 2, 1, 2, 2, 2): F(-1, 2),
    (2, 2, 2, 1, 0, 2): F(-1, 6),
    (2, 2, 2, 2, 2, 2): F(-1, 2),
}


def pairing_rows(q):
    """Rows of H_q as exact vectors indexed by quadratic cells."""
    columns = [polarized_coefficients(q, {cell: F(1)}) for cell in CELLS]
    return {
        coloring: tuple(column[coloring] for column in columns)
        for coloring in COLORINGS
    }


def audit_rational_left_certificate():
    q, _, _, _ = paircap_example()
    rows = pairing_rows(q)

    # This is the finite identity ell o H_q = 0 on a basis of all 135
    # quadratic cells.
    for column_index, cell in enumerate(CELLS):
        value = sum(
            coefficient * rows[coloring][column_index]
            for coloring, coefficient in RATIONAL_LEFT_CERTIFICATE.items()
        )
        assert value == 0, (cell, value)

    pure_values = tuple(
        RATIONAL_LEFT_CERTIFICATE.get((color,) * 6, F(0))
        for color in range(3)
    )
    assert pure_values == (F(1), F(-1, 2), F(-1, 2))


def q_pair_terms(q):
    """Record the two-q-edge contribution exposing each output row."""
    q_cells = tuple(q)
    terms = {coloring: [] for coloring in COLORINGS}
    for left_index, right_index in itertools.combinations(range(len(q_cells)), 2):
        left = q_cells[left_index]
        right = q_cells[right_index]
        left_edge, left_a, left_b = left
        right_edge, right_a, right_b = right
        if set(left_edge) & set(right_edge):
            continue
        remaining = tuple(
            sorted(set(range(6)) - set(left_edge) - set(right_edge))
        )
        assert len(remaining) == 2
        for a, b in itertools.product(range(3), repeat=2):
            coloring = [None] * 6
            coloring[left_edge[0]] = left_a
            coloring[left_edge[1]] = left_b
            coloring[right_edge[0]] = right_a
            coloring[right_edge[1]] = right_b
            coloring[remaining[0]] = a
            coloring[remaining[1]] = b
            terms[tuple(coloring)].append(
                (remaining, (a, b), left_index, right_index)
            )
    return q_cells, {coloring: row for coloring, row in terms.items() if row}


def audit_sparse_quotient_rows():
    q, _ = unrestricted_example()
    q_cells, terms = q_pair_terms(q)

    # There are 54 two-q-edge terms.  Fifty-one expose distinct output
    # coordinates; the remaining three meet at the sole q^3 coloring.
    singleton = {coloring: row for coloring, row in terms.items() if len(row) == 1}
    collisions = {coloring: row for coloring, row in terms.items() if len(row) > 1}
    gamma = (2, 1, 0, 0, 1, 2)
    assert len(singleton) == 51
    assert set(collisions) == {gamma}
    assert len(collisions[gamma]) == 3

    hq = polarized_coefficients(q, q)
    assert {coloring: value for coloring, value in hq.items() if value} == {
        gamma: F(3)
    }

    # The three pure q-edge pairs expose the full 3 x 3 cell matrices on
    # edges 01, 02, 12.  Every such row is a singleton and hence survives
    # independently modulo span(H_q(q)).
    exposed = (
        ((0, 1), 0, (0, 1)),
        ((0, 2), 1, (2, 3)),
        ((1, 2), 2, (4, 5)),
    )
    for edge, fixed_color, q_indices in exposed:
        for a, b in itertools.product(range(3), repeat=2):
            coloring = [fixed_color] * 6
            coloring[edge[0]] = a
            coloring[edge[1]] = b
            coloring = tuple(coloring)
            assert coloring in singleton
            remaining, local_colors, left_index, right_index = singleton[coloring][0]
            assert remaining == edge
            assert local_colors == (a, b)
            assert (left_index, right_index) == q_indices

    # Audit the six selected endpoint labels and all zero/target incidences
    # used by the abstract triangle proof.
    A = (0, 0)
    B = (1, 0)
    C = (0, 1)
    D = (2, 1)
    E = (1, 2)
    G = (2, 2)  # named G here to avoid shadowing Fraction F
    targets = {(A, B): 0, (C, D): 1, (E, G): 2}
    zeros = {
        (A, E), (C, B), (C, E),
        (A, D), (A, G), (C, G),
        (B, D), (B, G), (E, D),
    }
    for (left, right), target_color in targets.items():
        assert left[0] != right[0]
        assert left[1] == right[1] == target_color
    for left, right in zeros:
        assert left[0] != right[0]
    assert {(A, E), (A, D), (E, D)} <= zeros
    assert {(C, B), (C, G), (B, G)} <= zeros
    assert (A, G) in zeros

    # Keep the declared support synchronized with the table in the proof.
    assert q_cells == (
        ((2, 3), 0, 0),
        ((4, 5), 0, 0),
        ((1, 4), 1, 1),
        ((3, 5), 1, 1),
        ((0, 5), 2, 2),
        ((3, 4), 2, 2),
    )


def main():
    audit_rational_left_certificate()
    audit_sparse_quotient_rows()
    print("rational fixed-q left-kernel certificate: exact PASS")
    print("sparse three-completed-matchings quotient rows: exact PASS")
    print("scope: two fixed internal-q pair-suspension subcharts")


if __name__ == "__main__":
    main()

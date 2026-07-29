#!/usr/bin/env python3
"""Exact audit for A_23=t E_21+s E_00 with arbitrary complex t,s.

Four normalized support strata are checked over Q/C.  An exact diagonal
vertex-colour torus calculation proves that they represent every complex
parameter pair while preserving the target tensor and all quotient spaces.
"""

from __future__ import annotations

import collections
import shutil
import subprocess

import sympy as sp

import explore_three_cut_internal_23_perturbation as explore


Q = explore.Q
SIX = explore.SIX
COLOURS = explore.COLOURS


REPRESENTATIVES = {
    # (t,s): (reachable words, weighted atoms, multiplicities)
    (0, 0): (100, 126, {1: 78, 2: 18, 3: 4}),
    (1, 0): (126, 162, {1: 96, 2: 25, 3: 4, 4: 1}),
    (0, 1): (126, 162, {1: 96, 2: 25, 3: 4, 4: 1}),
    (1, 1): (152, 198, {1: 114, 2: 32, 3: 4, 4: 2}),
}


def marker_values(output: str, marker: str, count: int):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    start = lines.index(marker) + 1
    return tuple(int(lines[start + offset]) for offset in range(count))


def exact_segre_audit(word_terms, basis, active_colours, expected_components):
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required for this exact audit")
    program, diagonal_counts, off_count = explore.singular_program(
        word_terms, basis, active_colours
    )
    normal_dimension = len(explore.cylinders.echelon(basis))
    per_fibre = len(word_terms) - normal_dimension
    assert diagonal_counts == (per_fibre,) * len(active_colours)
    assert off_count == len(active_colours) * (len(active_colours) - 1) * per_fibre
    completed = subprocess.run(
        [singular, "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=600,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    assert marker_values(
        completed.stdout, "COMPONENTS", len(expected_components)
    ) == expected_components
    expected_checked = 1
    for count in expected_components:
        expected_checked *= count
    assert marker_values(completed.stdout, "CHECKED", 1) == (expected_checked,)
    assert marker_values(completed.stdout, "LIVE", 1) == (0,)


def audit_representative(t: int, s: int):
    blocks = explore.blocks_at(Q(t), Q(s))
    expected_hs = explore.vector_sum(
        explore.scaled(explore.U0, Q(t)),
        {explore.E0: Q(s)} if s else {},
        explore.UPLUS,
    )
    assert explore.cylinders.matching_tensor(SIX, blocks) == expected_hs

    word_terms = explore.reconstruct_word_terms(blocks)
    expected_words, expected_atoms, expected_multiplicities = REPRESENTATIVES[t, s]
    assert len(word_terms) == expected_words
    assert sum(map(len, word_terms.values())) == expected_atoms
    assert collections.Counter(map(len, word_terms.values())) == expected_multiplicities

    moving = explore.vector_sum(
        explore.scaled(explore.U0, Q(t)),
        {explore.E0: Q(s)} if s else {},
    )
    plane = [moving, explore.UPLUS] if moving else [explore.UPLUS]
    line = [expected_hs]
    for cuts in ((2, 3, 4, 0), (2, 3, 4, 1)):
        observed = explore.cylinders.cylinder_intersection(cuts, blocks)
        assert explore.same_span(observed, plane)
    observed = explore.cylinders.cylinder_intersection((2, 3, 4, 5), blocks)
    assert explore.same_span(observed, line)

    # Each possible fourth cut remains target-active.  This prevents the
    # obstruction from being a vacuous zero-quotient statement.
    for z in (0, 1, 5):
        u_sites = tuple(site for site in SIX if site != z)
        columns = explore.cylinders.insertion_columns(u_sites, blocks)
        constants = [
            explore.cylinders.unit((colour,) * 5) for colour in COLOURS
        ]
        defect = (
            len(explore.cylinders.echelon(columns + constants))
            - len(explore.cylinders.echelon(columns))
        )
        assert defect > 0
    return word_terms, plane, line


def audit_torus_normalization():
    """Symbolically check the scaling used for the nonzero/nonzero stratum."""
    t, s, a = sp.symbols("t s a", nonzero=True)
    g = {(site, colour): sp.Integer(1) for site in range(8) for colour in COLOURS}
    g[5, 0] = a
    g[4, 0] = 1 / a
    g[2, 0] = 1 / a
    g[3, 1] = 1 / a
    g[2, 2] = a / t
    g[3, 0] = a / s

    fixed_cells = (
        (0, 1, 0, 0), (4, 5, 0, 0),
        (0, 2, 1, 1), (1, 4, 1, 1),
        (0, 4, 2, 2), (1, 3, 2, 2),
        (2, 5, 0, 0), (3, 5, 1, 0),
    )
    for left, right, colour_left, colour_right in fixed_cells:
        assert sp.simplify(g[left, colour_left] * g[right, colour_right]) == 1
    assert sp.simplify(t * g[2, 2] * g[3, 1]) == 1
    assert sp.simplify(s * g[2, 0] * g[3, 0]) == 1

    # Boundary star entries and A_67 are unrestricted, so sites 6 and 7 may
    # absorb the remaining scale independently in each colour.  This makes
    # every diagonal target coefficient exactly one.
    for colour in COLOURS:
        internal_product = sp.prod(g[site, colour] for site in SIX)
        g[6, colour] = 1
        g[7, colour] = 1 / internal_product
        assert sp.simplify(sp.prod(g[site, colour] for site in range(8))) == 1

    # On the full five-cell plane locus, the allowed entries have scaling
    # monomials r0*c0, r0^2, r0*c2, r1*r0, r2*r0.  The exponent lattice has
    # full rank (index two); over C the required square roots exist, so each
    # zero/nonzero support is a single torus orbit.
    exponent_matrix = sp.Matrix([
        [1, 1, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ])
    assert abs(exponent_matrix.det()) == 2


def main():
    audit_torus_normalization()
    data = {
        representative: audit_representative(*representative)
        for representative in REPRESENTATIVES
    }

    # At (0,0), cuts 0,1,5 all have the same line normal.
    exact_segre_audit(data[0, 0][0], data[0, 0][2], (0, 1, 2), (9, 12, 9))

    # The already-audited fixed cell is rerun here in the common generator.
    exact_segre_audit(data[1, 0][0], data[1, 0][1], (0, 1, 2), (15, 13, 14))
    exact_segre_audit(data[1, 0][0], data[1, 0][2], (0, 1, 2), (9, 11, 9))

    # At (0,1), [0^6] belongs to the plane normal.  Full feasibility is
    # equivalent to the colours 1,2 subsystem: set p^0=q^0=0 to extend any
    # subsystem point.
    exact_segre_audit(data[0, 1][0], data[0, 1][1], (1, 2), (13, 10))
    exact_segre_audit(data[0, 1][0], data[0, 1][2], (0, 1, 2), (31, 11, 9))

    exact_segre_audit(data[1, 1][0], data[1, 1][1], (0, 1, 2), (25, 13, 10))
    exact_segre_audit(data[1, 1][0], data[1, 1][2], (0, 1, 2), (10, 11, 9))

    print("internal A23=tE21+sE00 fourth-cut obstruction: PASS")
    print("four torus strata (00,10,01,11), all exact component ideals: PASS")
    print("cuts 2340, 2341, and 2345 infeasible for every complex (t,s): PASS")
    print("endpoint order, shared stars, off-diagonal fibres, and unit targets: PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact Q/C audit for replacing the internal cell 23:E21 by 23:E00.

The endpoint-ordered combinatorics and cylinder intersections are computed
over Q.  Singular then proves that the actual shared two-star equations have
no complex point for either fourth-cut normal form.
"""

from __future__ import annotations

import collections
import shutil
import subprocess

import explore_three_cut_internal_23_perturbation as explore


Q = explore.Q
SIX = explore.SIX
COLOURS = explore.COLOURS


EXPECTED_COFACTORS = {
    (0, 1): ((0, 0, 0, 0),),
    (0, 2): ((1, 1, 1, 0), (2, 2, 0, 0)),
    (0, 3): ((1, 0, 1, 0),),
    (0, 4): ((2, 0, 2, 0),),
    (0, 5): ((1, 0, 0, 1),),
    (1, 2): ((2, 1, 2, 0),),
    (1, 3): ((1, 1, 0, 0), (2, 0, 2, 0)),
    (1, 4): ((1, 1, 1, 0),),
    (1, 5): ((2, 0, 0, 2),),
    (2, 3): ((0, 0, 0, 0),),
    (2, 4): ((0, 0, 1, 0),),
    (2, 5): ((2, 2, 2, 2),),
    (3, 4): ((0, 0, 0, 0),),
    (3, 5): ((1, 1, 1, 1),),
    (4, 5): ((0, 0, 0, 0), (1, 2, 1, 2)),
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
    dimension = len(explore.cylinders.echelon(basis))
    per_fibre = len(word_terms) - dimension
    assert diagonal_counts == (per_fibre,) * len(active_colours)
    assert off_count == len(active_colours) * (len(active_colours) - 1) * per_fibre
    result = subprocess.run(
        [singular, "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=600,
    )
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    assert marker_values(
        result.stdout, "COMPONENTS", len(expected_components)
    ) == expected_components
    checked = 1
    for count in expected_components:
        checked *= count
    assert marker_values(result.stdout, "CHECKED", 1) == (checked,)
    assert marker_values(result.stdout, "LIVE", 1) == (0,)


def audit_combinatorics():
    blocks = explore.blocks_at(Q(0), Q(1))
    expected_hs = explore.vector_sum({explore.E0: Q(1)}, explore.UPLUS)
    assert explore.cylinders.matching_tensor(SIX, blocks) == expected_hs

    observed_cofactors = {}
    for i in SIX:
        for j in range(i + 1, 6):
            rest = tuple(site for site in SIX if site not in (i, j))
            tensor = explore.cylinders.matching_tensor(rest, blocks)
            assert all(coefficient == 1 for coefficient in tensor.values())
            observed_cofactors[i, j] = tuple(sorted(tensor))
    assert observed_cofactors == EXPECTED_COFACTORS

    word_terms = explore.reconstruct_word_terms(blocks)
    assert sum(map(len, word_terms.values())) == 162
    assert len(word_terms) == 126
    assert collections.Counter(map(len, word_terms.values())) == {
        1: 96,
        2: 25,
        3: 4,
        4: 1,
    }

    plane = [{explore.E0: Q(1)}, explore.UPLUS]
    line = [expected_hs]
    for cuts in ((2, 3, 4, 0), (2, 3, 4, 1)):
        observed = explore.cylinders.cylinder_intersection(cuts, blocks)
        assert explore.same_span(observed, plane)
        assert len(observed) == 2
    observed = explore.cylinders.cylinder_intersection((2, 3, 4, 5), blocks)
    assert explore.same_span(observed, line)
    assert len(observed) == 1

    expected_defects = {
        0: ((True, False, False), 2),
        1: ((True, False, False), 2),
        2: ((True, False, True), 1),
        3: ((True, True, False), 1),
        4: ((True, False, False), 2),
        5: ((False, True, True), 1),
    }
    for z in SIX:
        u_sites = tuple(site for site in SIX if site != z)
        columns = explore.cylinders.insertion_columns(u_sites, blocks)
        span = explore.cylinders.echelon(columns)
        constants = [
            explore.cylinders.unit((colour,) * 5) for colour in COLOURS
        ]
        flags = tuple(explore.cylinders.member(vector, span) for vector in constants)
        defect = len(explore.cylinders.echelon(columns + constants)) - len(span)
        assert (flags, defect) == expected_defects[z]
    return word_terms, plane, line


def main():
    word_terms, plane, line = audit_combinatorics()

    # In the plane case [0^6] is already in the normal.  Hence a full
    # solution exists iff the colours 1 and 2 subsystem exists: the omitted
    # p^0,q^0 can be set to zero in the reverse implication.
    exact_segre_audit(word_terms, plane, (1, 2), (13, 10))
    exact_segre_audit(word_terms, line, (0, 1, 2), (31, 11, 9))

    print("internal 23:E00 replacement fourth-cut obstruction: PASS")
    print("cuts 2340/2341: 13*10=130 exact unit component pairs")
    print("cut 2345: 31*11*9=3069 exact unit component triples")
    print("all shared-star entries, endpoint order, and unit targets retained")


if __name__ == "__main__":
    main()

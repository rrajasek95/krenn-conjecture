#!/usr/bin/env python3
"""Verify that an exact-three path survivor must consist of three zeros.

The new input is the sparse-reference cofactor collapse.  If a reference
block row has at most three nonzero maps whose generic images are linearly
independent, the corresponding coefficients in its dead-line vector
identity vanish separately.  The resulting zero-Per3 status constraints
exclude every nonzero corner.  After transposition, 352 residual models for
a rank-one arm are excluded by projective-frame singleton contractions.
"""

from __future__ import annotations

from collections import Counter
import hashlib

import verify_two_k4_exact_three_incidence_boundary as boundary3
import verify_two_k4_exact_three_matching_obstruction as frame


VERTICES = tuple(range(4))
PATH = boundary3.POSITION_ORBITS["path"]


def sparse_reference_constraints(row_matroids, nonzero_columns):
    """Status consequences of separately zero sparse-row cofactors.

    The exceptional reference row is row 0.  ``nonzero_columns`` lists its
    generically independent nonzero vector summands, and therefore exactly
    the complementary cofactors which vanish separately.
    """

    singulars = tuple(
        (row, column, row_matroid)
        for (row, column), row_matroid in zip(PATH, row_matroids)
    )
    constraints = []
    for triangle, (hole, assignment) in enumerate(boundary3.LINES):
        if hole != 0:
            continue
        selected_color = dict(assignment)
        for omitted_column in nonzero_columns:
            columns = set(VERTICES) - {omitted_column}
            dirty_columns = {
                column
                for row, column, row_matroid in singulars
                if (
                    row != hole
                    and column in columns
                    and selected_color[row] in row_matroid.zero_colors
                )
            }
            demand = 2 if not dirty_columns else int(
                bool(columns - dirty_columns)
            )
            if demand:
                constraints.append(
                    (triangle, tuple(sorted(columns)), demand)
                )
    return tuple(constraints)


def satisfies(masks, constraints):
    return all(
        sum(bool(masks[column] >> triangle & 1) for column in columns)
        >= demand
        for triangle, columns, demand in constraints
    )


def audit_nonzero_corner():
    # Put the zero arm at B_01.  The earlier two-shore rank audit says that
    # the other arm has rank at most one.  If B_00 is nonzero, reference row
    # 0 has the three generically independent summands in columns 0,2,3.
    patterns = {(1, 0, 0), (1, 0, 1), (2, 0, 0), (2, 0, 1)}
    type_counts = Counter()
    model_counts = Counter()
    enhanced_count = 0
    for row_matroids in boundary3.matroid_survivors("path"):
        ranks = tuple(row_matroid.rank for row_matroid in row_matroids)
        if ranks not in patterns:
            continue
        type_counts[ranks] += 1
        constraints = sparse_reference_constraints(
            row_matroids, (0, 2, 3)
        )
        models = frame.incidence_models(row_matroids, PATH)
        model_counts[ranks] += len(models)
        enhanced_count += sum(
            satisfies(masks, constraints) for masks in models
        )

    assert type_counts == {
        (1, 0, 0): 6,
        (1, 0, 1): 20,
        (2, 0, 0): 7,
        (2, 0, 1): 7,
    }
    assert model_counts == {
        (1, 0, 0): 50_564,
        (1, 0, 1): 69_370,
        (2, 0, 0): 6_340,
        (2, 0, 1): 3_268,
    }
    assert sum(type_counts.values()) == 40
    assert sum(model_counts.values()) == 129_542
    assert enhanced_count == 0


def audit_rank_one_arm_after_transposition():
    # Once the corner is zero, suppose the other arm is rank one.  Transpose
    # so that row 0 contains B_00=0 and the nonzero rank-one block B_01.
    # Its nonzero reference summands lie in columns 1,2,3.
    survivors = tuple(
        row_matroids
        for row_matroids in boundary3.matroid_survivors("path")
        if tuple(item.rank for item in row_matroids) == (0, 1, 0)
    )
    assert tuple(
        tuple(item.name for item in row_matroids)
        for row_matroids in survivors
    ) == (("0", "S1", "0"), ("0", "S2", "0"), ("0", "S12", "0"))

    records = []
    enhanced_counts = {}
    for row_matroids in survivors:
        names = tuple(item.name for item in row_matroids)
        constraints = sparse_reference_constraints(
            row_matroids, (1, 2, 3)
        )
        enhanced = tuple(
            masks
            for masks in frame.incidence_models(row_matroids, PATH)
            if satisfies(masks, constraints)
        )
        enhanced_counts[names] = len(enhanced)
        for masks in enhanced:
            witness = frame.contraction_witness(row_matroids, masks, PATH)
            assert witness is not None, (names, masks)
            records.append((names, masks, witness))

    assert enhanced_counts == {
        ("0", "S1", "0"): 176,
        ("0", "S2", "0"): 176,
        ("0", "S12", "0"): 0,
    }
    assert len(records) == 352
    representatives = {
        ("0", "S1", "0"): (
            (0xF5, 0x60, 0x8A, 0x9A),
            ((2, 0, 0, 1), (0, 2, 3), (2, 1, 0, 3)),
        ),
        ("0", "S2", "0"): (
            (0xFA, 0x25, 0x65, 0x90),
            ((0, 1, 0, 2), (0, 1, 2), (2, 1, 0, 3)),
        ),
    }
    for names, (masks, witness) in representatives.items():
        assert (names, masks, witness) in records

    digest = hashlib.sha256(repr(sorted(records)).encode()).hexdigest()
    assert digest == (
        "ceb25b1f89cbacaa0438b621d5f216c88f37464b0910ca599086c2c470fe2af7"
    ), digest


def main():
    assert PATH == ((0, 0), (0, 1), (1, 0))
    assert tuple(hole for hole, _assignment in boundary3.LINES[:2]) == (0, 0)
    audit_nonzero_corner()
    audit_rank_one_arm_after_transposition()
    print(
        "PASS: every exact-three path survivor has three zero blocks "
        "(129542 nonzero-corner models eliminated; 352 arm models contracted)"
    )


if __name__ == "__main__":
    main()

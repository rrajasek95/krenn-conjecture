#!/usr/bin/env python3
"""Exclude the literal all-zero exact-three path.

The sparse corner row gives two one-defect zero-Per3 tensors on each of the
two hole-zero triangle lines.  Their exact rank dichotomy, generalized
projective-frame singleton contractions, and a final dirty-rank-one versus
clean-rank-three obstruction eliminate every incidence model.
"""

from __future__ import annotations

import hashlib
import itertools

import verify_two_k4_exact_three_incidence_boundary as boundary3
import verify_two_k4_exact_three_matching_obstruction as frame


PATH = boundary3.POSITION_ORBITS["path"]
ZERO = boundary3.boundary.RANK_ZERO_TYPES[0]
ROW_MATROIDS = (ZERO, ZERO, ZERO)


def generalized_contraction_witness(masks):
    """Allow a singleton signature after contracting 1--4 framed factors."""

    columns = frame.projective_column_data(ROW_MATROIDS, masks, PATH)
    for word in frame.DEAD_WORDS:
        active_permutations = tuple(
            permutation
            for permutation in frame.PERMUTATIONS
            if all(
                (row, word[row]) in columns[column][0]
                for row, column in enumerate(permutation)
            )
        )
        for number in range(1, 5):
            for contracted_columns in itertools.combinations(
                frame.VERTICES, number
            ):
                if not all(
                    frame.roots_are_independent(
                        {
                            columns[column][1][row, word[row]]
                            for row in frame.VERTICES
                            if (row, word[row]) in columns[column][0]
                        },
                        columns[column],
                    )
                    for column in contracted_columns
                ):
                    continue

                groups = {}
                for permutation in active_permutations:
                    inverse = {
                        column: row
                        for row, column in enumerate(permutation)
                    }
                    signature = tuple(
                        columns[column][1][
                            inverse[column], word[inverse[column]]
                        ]
                        for column in contracted_columns
                    )
                    groups.setdefault(signature, []).append(permutation)
                for permutations in groups.values():
                    if len(permutations) == 1:
                        return word, contracted_columns, permutations[0]
    return None


def one_defect_compatible(masks):
    """Necessary dichotomy for C_2=C_3=0 on hole-zero lines.

    Physical column 0 has exactly one selected zero row.  If its two active
    vectors are independent, both good factors in the zero Per3 must have
    rank one.  Otherwise column 0 itself is a status.
    """

    for triangle in (0, 1):
        status = lambda column: bool(masks[column] >> triangle & 1)
        # C_2 uses physical columns 0,1,3; C_3 uses 0,1,2.
        if not (status(0) or (status(1) and status(3))):
            return False
        if not (status(0) or (status(1) and status(2))):
            return False
    return True


def residual_has_forbidden_local_configuration(masks):
    """Check dirty rank one and an independently framed clean factor."""

    columns = frame.projective_column_data(ROW_MATROIDS, masks, PATH)
    for triangle in (0, 1):
        assert masks[0] >> triangle & 1
        _hole, assignment = boundary3.LINES[triangle]
        relevant_roots = {
            columns[1][1][label]
            for label in assignment
            if label in columns[1][0]
        }
        if not frame.roots_are_independent(relevant_roots, columns[1]):
            return False
    return True


def main():
    assert PATH == ((0, 0), (0, 1), (1, 0))
    models = frame.incidence_models(ROW_MATROIDS, PATH)
    assert len(models) == 46_854

    defect_models = tuple(
        masks for masks in models if one_defect_compatible(masks)
    )
    assert len(defect_models) == 892

    contracted = []
    residual = []
    for masks in defect_models:
        witness = generalized_contraction_witness(masks)
        if witness is None:
            residual.append(masks)
        else:
            contracted.append((masks, witness))
    assert len(contracted) == 838
    assert len(residual) == 54
    assert all(
        residual_has_forbidden_local_configuration(masks)
        for masks in residual
    )

    contracted_digest = hashlib.sha256(
        repr(sorted(contracted)).encode()
    ).hexdigest()
    assert contracted_digest == (
        "02af118f831dfad0bdb941e5b053a3d3037fd95e093bd92c10dc4e99740285be"
    ), contracted_digest
    residual_digest = hashlib.sha256(
        repr(sorted(residual)).encode()
    ).hexdigest()
    assert residual_digest == (
        "d3e28974994bd4adbe7f1c85bb47c73f92b04e650ca1fde63de1c10a2e9146d6"
    ), residual_digest

    assert contracted[0] == (
        (0xF3, 0x0C, 0x64, 0x98),
        ((0, 1, 1, 0), (0, 3), (2, 1, 0, 3)),
    )
    assert residual[0] == (0xF3, 0x3C, 0x0C, 0xC0)
    assert residual[-1] == (0xF3, 0xFC, 0xC0, 0x0C)

    print(
        "PASS: all-zero exact-three path excluded "
        "(46854 -> 892 -> 54; every residual is dirty-rank1/clean-rank3)"
    )


if __name__ == "__main__":
    main()

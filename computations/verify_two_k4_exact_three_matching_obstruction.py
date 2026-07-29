#!/usr/bin/env python3
"""Exact projective-frame obstruction for the exact-three matching orbit.

The incidence audit leaves 28 row-matroid triples on singular positions
``B_00,B_11,B_22``.  For every nonzero triple, this checker enumerates every
admissible 32-bit status pattern and finds a dead left word whose four-cross
permanent has a unique term after contraction in three independently framed
right factors.  The all-zero triple is handled by the stronger two-/three-
defect zero-Per3 lemma, which forces three explicit status masks before the
same singleton contraction is applied.
"""

from __future__ import annotations

import hashlib
import itertools

from pysat.solvers import Cadical153

import verify_two_k4_dead_slice_determinantal_boundary as dense
import verify_two_k4_exact_three_incidence_boundary as boundary3


VERTICES = tuple(range(4))
COLORS = tuple(range(3))
LINES = boundary3.LINES
POSITIONS = boundary3.POSITION_ORBITS["matching"]
PERMUTATIONS = tuple(itertools.permutations(VERTICES))
DEAD_WORDS = tuple(
    word
    for word in itertools.product(COLORS, repeat=4)
    if dense.is_dead(word)
)


class UnionFind:
    def __init__(self, active):
        self.parent = {item: item for item in active}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, first, second):
        first, second = self.find(first), self.find(second)
        if first != second:
            self.parent[second] = first


def incidence_models(row_matroids, positions=POSITIONS):
    """Enumerate every exact four-column status mask satisfying the audit."""

    singulars = tuple(
        (row, column, row_matroid)
        for (row, column), row_matroid in zip(positions, row_matroids)
    )
    domains = []
    for column in VERTICES:
        exceptional = tuple(
            sorted(
                (row, row_matroid)
                for row, block_column, row_matroid in singulars
                if block_column == column
            )
        )
        domains.append(boundary3.status_masks(exceptional))

    variable = lambda triangle, column: 1 + 8 * column + triangle
    clauses = []
    for column, domain in enumerate(domains):
        domain = set(domain)
        for mask in range(1 << len(LINES)):
            if mask in domain:
                continue
            clauses.append([
                -variable(triangle, column)
                if mask >> triangle & 1
                else variable(triangle, column)
                for triangle in range(len(LINES))
            ])
    for triangle, columns, demand in boundary3.cofactor_constraints(
        positions, row_matroids
    ):
        if demand == 1:
            clauses.append([
                variable(triangle, column) for column in columns
            ])
        else:
            assert demand == 2
            clauses.extend(
                [variable(triangle, first), variable(triangle, second)]
                for first, second in itertools.combinations(columns, 2)
            )

    answers = []
    with Cadical153(bootstrap_with=clauses) as solver:
        while solver.solve():
            model = solver.get_model()
            masks = tuple(
                sum(
                    (model[variable(triangle, column) - 1] > 0) << triangle
                    for triangle in range(len(LINES))
                )
                for column in VERTICES
            )
            answers.append(masks)
            solver.add_clause([
                -variable(triangle, column)
                if masks[column] >> triangle & 1
                else variable(triangle, column)
                for column in VERTICES
                for triangle in range(len(LINES))
            ])
    return tuple(sorted(answers))


def projective_column_data(row_matroids, masks, positions=POSITIONS):
    singular_at = {
        position: row_matroid
        for position, row_matroid in zip(positions, row_matroids)
    }
    answer = []
    for column, mask in enumerate(masks):
        exceptional = {
            row: row_matroid
            for (row, block_column), row_matroid in singular_at.items()
            if block_column == column
        }
        classes = {
            vertex: exceptional.get(
                vertex, boundary3.boundary.INVERTIBLE
            ).projective_classes
            for vertex in VERTICES
        }
        active = {
            (vertex, color)
            for vertex in VERTICES
            for projective_class in classes[vertex]
            for color in projective_class
        }
        original_class = {
            (vertex, color): class_number
            for vertex in VERTICES
            for class_number, projective_class in enumerate(classes[vertex])
            for color in projective_class
        }
        union_find = UnionFind(active)
        for vertex in VERTICES:
            for projective_class in classes[vertex]:
                labels = tuple((vertex, color) for color in projective_class)
                for label in labels[1:]:
                    union_find.union(labels[0], label)
        for triangle, (_hole, assignment) in enumerate(LINES):
            if not (mask >> triangle & 1):
                continue
            selected = tuple(label for label in assignment if label in active)
            for label in selected[1:]:
                union_find.union(selected[0], label)

        roots = {label: union_find.find(label) for label in active}
        assert all(
            not (
                roots[first] == roots[second]
                and original_class[first] != original_class[second]
            )
            for vertex in VERTICES
            for first, second in itertools.combinations(
                [
                    (vertex, color)
                    for projective_class in classes[vertex]
                    for color in projective_class
                ],
                2,
            )
        )
        answer.append((active, roots, frozenset(exceptional)))
    return tuple(answer)


def roots_are_independent(relevant_roots, column_data):
    """Certify roots as a subset of one invertible block's row basis."""

    _active, roots, exceptional_vertices = column_data
    return any(
        relevant_roots
        <= {roots[vertex, color] for color in COLORS}
        for vertex in VERTICES
        if vertex not in exceptional_vertices
    )


def contraction_witness(row_matroids, masks, positions=POSITIONS):
    """Find ``(dead word, three factors, unique matching permutation)``."""

    columns = projective_column_data(row_matroids, masks, positions)
    for word in DEAD_WORDS:
        active_permutations = tuple(
            permutation
            for permutation in PERMUTATIONS
            if all(
                (row, word[row]) in columns[column][0]
                for row, column in enumerate(permutation)
            )
        )
        for contracted_columns in itertools.combinations(VERTICES, 3):
            if not all(
                roots_are_independent(
                    {
                        columns[column][1][row, word[row]]
                        for row in VERTICES
                        if (row, word[row]) in columns[column][0]
                    },
                    columns[column],
                )
                for column in contracted_columns
            ):
                continue

            groups = {}
            for permutation in active_permutations:
                inverse = {column: row for row, column in enumerate(permutation)}
                signature = tuple(
                    columns[column][1][inverse[column], word[inverse[column]]]
                    for column in contracted_columns
                )
                groups.setdefault(signature, []).append(permutation)
            for permutations in groups.values():
                if len(permutations) == 1:
                    return word, contracted_columns, permutations[0]
    return None


def audit_defect_lemmas_and_all_zero_case():
    # If the second and third local maps kill distinct coordinates 1 and 2,
    # precisely these three Per_3 terms survive.  Grouping by either dirty
    # factor proves that both dirty maps have rank one on their active rows.
    two_defect = tuple(
        permutation
        for permutation in itertools.permutations(COLORS)
        if permutation[1] != 1 and permutation[2] != 2
    )
    assert two_defect == ((0, 2, 1), (1, 2, 0), (2, 0, 1))

    # If factor j kills coordinate j, only the two derangements survive;
    # equality of two nonzero pure tensors makes every active pair
    # proportional.
    three_defect = tuple(
        permutation
        for permutation in itertools.permutations(COLORS)
        if all(permutation[factor] != factor for factor in COLORS)
    )
    assert three_defect == ((1, 2, 0), (2, 0, 1))

    zero = boundary3.boundary.RANK_ZERO_TYPES[0]
    row_matroids = (zero, zero, zero)
    # Applying the two-defect lemma on holes 0,1,2 and the three-defect
    # lemma on hole 3 forces these exact maximal masks in columns 0,1,2.
    masks = (0xFC, 0xF3, 0xCF, 0x00)
    for column, mask in enumerate(masks[:3]):
        domain = boundary3.status_masks(((column, zero),))
        assert mask in domain
        assert not any(mask != larger and mask & ~larger == 0 for larger in domain)

    witness = contraction_witness(row_matroids, masks)
    assert witness == ((0, 1, 0, 2), (0, 1, 2), (3, 0, 1, 2))


def audit_all_nonzero_matroid_cases():
    survivors = boundary3.matroid_survivors("matching")
    zero_names = ("0", "0", "0")
    assert len(survivors) == 28

    model_count = 0
    records = []
    for row_matroids in survivors:
        names = tuple(row_matroid.name for row_matroid in row_matroids)
        if names == zero_names:
            continue
        models = incidence_models(row_matroids)
        assert models
        for masks in models:
            witness = contraction_witness(row_matroids, masks)
            assert witness is not None, (names, masks)
            model_count += 1
            records.append((names, masks, witness))
    assert model_count == 3591

    # Freeze one transparent certificate in each of the two terminal rank
    # patterns from the incidence note.  Z2 is the rank-two type with row 2
    # zero; S0 is the rank-one type supported on the common coordinate row 0.
    representative_certificates = {
        ("Z2", "0", "0"): (
            (0x65, 0x65, 0x9A, 0x9A),
            ((0, 1, 0, 2), (0, 1, 2), (1, 0, 3, 2)),
        ),
        ("S0", "S0", "S0"): (
            (0x9A, 0x65, 0x65, 0x9A),
            ((0, 1, 1, 0), (0, 1, 2), (0, 2, 3, 1)),
        ),
    }
    for names, (masks, witness) in representative_certificates.items():
        matching_records = [
            record
            for record in records
            if record[0] == names and record[1] == masks
        ]
        assert matching_records == [(names, masks, witness)]

    digest = hashlib.sha256(repr(sorted(records)).encode()).hexdigest()
    # Freeze the complete finite witness table against accidental drift.
    assert digest == (
        "d689ff89121dbdec6b2cf708d0143a47ef0028619e9b412e4fba4586449355d8"
    ), digest


def main():
    assert len(DEAD_WORDS) == 30
    audit_defect_lemmas_and_all_zero_case()
    audit_all_nonzero_matroid_cases()
    print(
        "PASS: exact-three matching orbit excluded by projective-frame "
        "singleton contractions (3591 nonzero models plus all-zero case)"
    )


if __name__ == "__main__":
    main()

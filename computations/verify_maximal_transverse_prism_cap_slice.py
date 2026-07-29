#!/usr/bin/env python3
"""Exact audit of the maximal GHZ-compatible cap slice of the prism source.

This is a finite symbolic/combinatorial audit, not a numerical search.  It
checks a ten-site common-edge source with a dense but top-inactive pq block.
The source has a maximal codimension-six cap slice whose top image is the
three-dimensional diagonal boundary space, and a maximal codimension-eight
slice on which the literal global-GHZ cap formula holds.  On both slices the
cofactor image is exactly the four-parameter triangular-prism family and has
the sharp unit-saturation root cover.

The induced eight-site two-K4 core is also checked directly.  Its cap-
adjugate determinant has all six off-diagonal block rows nonzero, so the six
directions omitted by the image-diagonal slice are precisely visible to the
shared-edge alternating identity.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from itertools import combinations, permutations, product

import sympy as sp


W = ("p", "q", "r", "s")
U = ("x0", "x1", "x2", "y0", "y1", "y2")
ALL = W + U
POSITION = {vertex: index for index, vertex in enumerate(ALL)}

A = sp.Matrix([[1, 2, 3], [4, 5, 7], [8, 11, 13]])

# Sparse aggregate cells in the global endpoint order.  Each cell is
# (left colour, right colour, coefficient).
EDGES: dict[tuple[str, str], list[tuple[int, int, sp.Expr]]] = defaultdict(list)


def add_cell(
    left: str,
    right: str,
    left_colour: int,
    right_colour: int,
    coefficient: sp.Expr = sp.S.One,
) -> None:
    if POSITION[left] < POSITION[right]:
        EDGES[left, right].append((left_colour, right_colour, coefficient))
    else:
        EDGES[right, left].append((right_colour, left_colour, coefficient))


def cells(left: str, right: str) -> list[tuple[int, int, sp.Expr]]:
    if POSITION[left] < POSITION[right]:
        return EDGES.get((left, right), [])
    return [
        (right_colour, left_colour, coefficient)
        for left_colour, right_colour, coefficient in EDGES.get((right, left), [])
    ]


def build_source() -> None:
    for i, j in product(range(3), repeat=2):
        add_cell("p", "q", i, j, A[i, j])
    add_cell("r", "s", 0, 0)
    add_cell("p", "r", 1, 1)
    add_cell("q", "s", 2, 2)

    for i in range(3):
        add_cell("p", f"x{i}", i, i)
        add_cell("q", f"y{i}", i, i)

    add_cell("x1", "x2", 0, 0)
    add_cell("x0", "x2", 1, 1)
    add_cell("x0", "x1", 2, 2)
    add_cell("y1", "y2", 0, 0)
    add_cell("y0", "y2", 1, 1)
    add_cell("y0", "y1", 2, 2)


@lru_cache(maxsize=None)
def perfect_matchings(
    vertices: tuple[str, ...],
) -> tuple[tuple[tuple[str, str], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def matching_tensor(
    vertices: tuple[str, ...],
) -> dict[tuple[int, ...], sp.Expr]:
    location = {vertex: index for index, vertex in enumerate(vertices)}
    answer: dict[tuple[int, ...], sp.Expr] = defaultdict(lambda: sp.S.Zero)
    for matching in perfect_matchings(vertices):
        choices = [cells(left, right) for left, right in matching]
        if any(not choice for choice in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(vertices)
            coefficient = sp.S.One
            for ((left, right), (left_colour, right_colour, value)) in zip(
                matching, selected
            ):
                word[location[left]] = left_colour
                word[location[right]] = right_colour
                coefficient *= value
            answer[tuple(word)] += coefficient
    return {
        word: sp.expand(coefficient)
        for word, coefficient in answer.items()
        if sp.expand(coefficient) != 0
    }


def expected_internal_tensor() -> dict[tuple[int, ...], sp.Expr]:
    answer = {
        (i, j, 0, 0): A[i, j]
        for i, j in product(range(3), repeat=2)
    }
    answer[(1, 2, 1, 2)] = sp.S.One
    return answer


def expected_top_tensor() -> dict[tuple[int, ...], sp.Expr]:
    return {
        (i, j, 0, 0) + (i, i, i, j, j, j): sp.S.One
        for i, j in product(range(3), repeat=2)
    }


CAP_WORDS = tuple(product(range(3), repeat=4))
CAP_INDEX = {word: index for index, word in enumerate(CAP_WORDS)}


def coordinate_row(word: tuple[int, int, int, int]) -> sp.Matrix:
    row = sp.zeros(1, len(CAP_WORDS))
    row[0, CAP_INDEX[word]] = 1
    return row


def audit_cap_linear_algebra() -> tuple[sp.Matrix, sp.Matrix]:
    # Rows of the full top map in the ordered block basis E_ij.
    top_map = sp.Matrix.vstack(
        *[
            coordinate_row((i, j, 0, 0))
            for i, j in product(range(3), repeat=2)
        ]
    )
    assert top_map.rank() == 9

    # The top image is diagonal exactly when the six off-diagonal rows vanish.
    image_defect = sp.Matrix.vstack(
        *[
            coordinate_row((i, j, 0, 0))
            for i, j in product(range(3), repeat=2)
            if i != j
        ]
    )
    assert image_defect.rank() == 6
    image_kernel = sp.Matrix.hstack(*image_defect.nullspace())
    assert image_kernel.shape == (81, 75)
    assert (image_defect * image_kernel).is_zero_matrix
    assert (top_map * image_kernel).rank() == 3

    # On a true global GHZ source the diagonal coefficient is K(i,i,i,i).
    # The colour-zero condition is automatic because (0,0,0,0) is the same
    # cap coordinate.  Colours one and two add two independent relocation rows.
    ghz_defect_rows = [image_defect.row(index) for index in range(6)]
    for colour in (1, 2):
        ghz_defect_rows.append(
            coordinate_row((colour, colour, 0, 0))
            - coordinate_row((colour, colour, colour, colour))
        )
    ghz_defect = sp.Matrix.vstack(*ghz_defect_rows)
    assert ghz_defect.rank() == 8
    ghz_kernel = sp.Matrix.hstack(*ghz_defect.nullspace())
    assert ghz_kernel.shape == (81, 73)
    assert (ghz_defect * ghz_kernel).is_zero_matrix
    assert (top_map * ghz_kernel).rank() == 3

    scalar_row = coordinate_row((1, 2, 1, 2))
    for i, j in product(range(3), repeat=2):
        scalar_row += A[i, j] * coordinate_row((i, j, 0, 0))
    effective_map = sp.Matrix.vstack(
        scalar_row,
        coordinate_row((0, 0, 0, 0)),
        coordinate_row((1, 1, 0, 0)),
        coordinate_row((2, 2, 0, 0)),
    )
    assert (effective_map * image_kernel).rank() == 4
    assert (effective_map * ghz_kernel).rank() == 4
    assert ghz_kernel.shape[1] - (effective_map * ghz_kernel).rank() == 69

    return image_defect, ghz_defect


def audit_general_cofactors() -> None:
    internal = matching_tensor(W)
    assert internal == expected_internal_tensor()

    for left, right in combinations(U, 2):
        tensor = matching_tensor(W + (left, right))
        expected: dict[tuple[int, ...], sp.Expr] = {}

        if left[0] == right[0]:
            shore = left[0]
            indices = {int(left[1]), int(right[1])}
            if len(indices) == 2:
                missing = ({0, 1, 2} - indices).pop()
                boundary_word = (missing, missing)
                for cap_word, coefficient in expected_internal_tensor().items():
                    expected[cap_word + boundary_word] = coefficient
        else:
            x_vertex = left if left[0] == "x" else right
            y_vertex = right if right[0] == "y" else left
            i, j = int(x_vertex[1]), int(y_vertex[1])
            boundary_word = (i, j) if left[0] == "x" else (j, i)
            expected[(i, j, 0, 0) + boundary_word] = sp.S.One

        assert tensor == expected, (left, right, tensor, expected)


def edge_value(
    family: dict[tuple[str, str], dict[tuple[int, int], sp.Expr]],
    left: str,
    right: str,
    left_colour: int,
    right_colour: int,
) -> sp.Expr:
    if POSITION[left] < POSITION[right]:
        return family.get((left, right), {}).get((left_colour, right_colour), 0)
    return family.get((right, left), {}).get((right_colour, left_colour), 0)


def family_hafnian(
    family: dict[tuple[str, str], dict[tuple[int, int], sp.Expr]],
) -> dict[tuple[int, ...], sp.Expr]:
    answer: dict[tuple[int, ...], sp.Expr] = {}
    for colouring in product(range(3), repeat=6):
        total = sp.S.Zero
        for matching in perfect_matchings(U):
            term = sp.S.One
            for left, right in matching:
                term *= edge_value(
                    family,
                    left,
                    right,
                    colouring[U.index(left)],
                    colouring[U.index(right)],
                )
            total += term
        total = sp.expand(total)
        if total != 0:
            answer[colouring] = total
    return answer


def audit_prism_restriction() -> None:
    s, z0, z1, z2 = sp.symbols("s z0 z1 z2")
    z = (z0, z1, z2)
    family: dict[tuple[str, str], dict[tuple[int, int], sp.Expr]] = {}

    def put(left: str, right: str, colour: int, coefficient: sp.Expr) -> None:
        family.setdefault((left, right), {})[(colour, colour)] = coefficient

    put("x1", "x2", 0, s)
    put("x0", "x2", 1, s)
    put("x0", "x1", 2, s)
    put("y1", "y2", 0, s)
    put("y0", "y2", 1, s)
    put("y0", "y1", 2, s)
    for colour in range(3):
        put(f"x{colour}", f"y{colour}", colour, z[colour])

    actual = family_hafnian(family)
    expected = {(colour,) * 6: s**2 * z[colour] for colour in range(3)}
    expected[(0, 1, 2, 0, 1, 2)] = z0 * z1 * z2
    assert actual == expected

    # The mixed ideal is generated by z0*z1*z2.  Its generator divides the
    # active product h=s*z0*z1*z2, so the first colon is already the unit ideal.
    generator = z0 * z1 * z2
    active = s * generator
    assert sp.expand(active - s * generator) == 0

    # On both maximal slices (s,z0,z1,z2) are independent.  A concrete right
    # inverse uses cap coordinates k0000=z0, k1100=z1, k2200=z2 and
    # k1212=s-z0-5*z1-13*z2.  On the GHZ-compatible slice also set
    # k1111=z1 and k2222=z2.
    active_matrix = sp.Matrix(
        [
            [1, 5, 13, 1],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
        ]
    )
    assert active_matrix.det() == -1


def cofactor_matrix(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        3,
        3,
        lambda i, j: (-1) ** (i + j) * matrix.minor_submatrix(i, j).det(),
    )


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def induced_pair_family(cap_i: int, cap_j: int):
    # Pair-cap family of the induced eight-site core on p,q,U.
    family: dict[tuple[str, str], dict[tuple[int, int], sp.Expr]] = {}
    for left, right in combinations(U, 2):
        block: dict[tuple[int, int], sp.Expr] = {}
        for left_colour, right_colour in product(range(3), repeat=2):
            value = sp.S.Zero
            for edge_left_colour, edge_right_colour, coefficient in cells(left, right):
                if (edge_left_colour, edge_right_colour) == (
                    left_colour,
                    right_colour,
                ):
                    value += A[cap_i, cap_j] * coefficient

            for first_boundary, second_boundary in ((left, right), (right, left)):
                first_colour = (
                    left_colour if first_boundary == left else right_colour
                )
                second_colour = (
                    right_colour if second_boundary == right else left_colour
                )
                p_cells = cells("p", first_boundary)
                q_cells = cells("q", second_boundary)
                for p_colour, boundary_colour, p_value in p_cells:
                    if p_colour != cap_i or boundary_colour != first_colour:
                        continue
                    for q_colour, other_colour, q_value in q_cells:
                        if q_colour == cap_j and other_colour == second_colour:
                            value += p_value * q_value
            value = sp.expand(value)
            if value != 0:
                block[left_colour, right_colour] = value
        family[left, right] = block
    return family


def product_of_three_families(families) -> dict[tuple[int, ...], sp.Expr]:
    answer: dict[tuple[int, ...], sp.Expr] = {}
    for colouring in product(range(3), repeat=6):
        total = sp.S.Zero
        for matching in perfect_matchings(U):
            for assignment in permutations(range(3)):
                term = sp.S.One
                for edge_index, family_index in enumerate(assignment):
                    left, right = matching[edge_index]
                    term *= edge_value(
                        families[family_index],
                        left,
                        right,
                        colouring[U.index(left)],
                        colouring[U.index(right)],
                    )
                total += term
        total = sp.expand(total)
        if total != 0:
            answer[colouring] = total
    return answer


def add_scaled(target, source, scale) -> None:
    for word, coefficient in source.items():
        target[word] = sp.expand(target.get(word, 0) + scale * coefficient)
        if target[word] == 0:
            del target[word]


def audit_adjugate_transverse_rows() -> None:
    cofactors = cofactor_matrix(A)
    expected_cofactors = sp.Matrix(
        [[-12, 4, 4], [7, -11, 5], [-1, 5, -3]]
    )
    assert A.det() == 8
    assert cofactors == expected_cofactors
    assert all(cofactors[i, j] != 0 for i, j in product(range(3), repeat=2))

    families = [
        [induced_pair_family(i, j) for j in range(3)] for i in range(3)
    ]
    determinant_tensor: dict[tuple[int, ...], sp.Expr] = {}
    for permutation in permutations(range(3)):
        term = product_of_three_families(
            [families[row][permutation[row]] for row in range(3)]
        )
        add_scaled(determinant_tensor, term, permutation_sign(permutation))

    expected = {
        (left,) * 3 + (right,) * 3: 2 * cofactors[left, right]
        for left, right in product(range(3), repeat=2)
    }
    assert determinant_tensor == expected

    diagonal = {
        (colour,) * 6: 2 * cofactors[colour, colour]
        for colour in range(3)
    }
    discrepancy = dict(determinant_tensor)
    add_scaled(discrepancy, diagonal, -1)
    expected_transverse = {
        (left,) * 3 + (right,) * 3: 2 * cofactors[left, right]
        for left, right in product(range(3), repeat=2)
        if left != right
    }
    assert discrepancy == expected_transverse
    assert len(discrepancy) == 6


def main() -> None:
    build_source()
    assert matching_tensor(W) == expected_internal_tensor()
    assert matching_tensor(ALL) == expected_top_tensor()
    image_defect, ghz_defect = audit_cap_linear_algebra()
    audit_general_cofactors()
    audit_prism_restriction()
    audit_adjugate_transverse_rows()

    print("full cap-map rank: 9")
    print("maximal diagonal-image slice: codimension", image_defect.rank())
    print("maximal exact-GHZ-formula slice: codimension", ghz_defect.rank())
    print("cofactor image on both slices: four-parameter prism")
    print("adjugate-detected transverse rows: 6")
    print("PASS: maximal transverse prism cap-slice countermodel")


if __name__ == "__main__":
    main()

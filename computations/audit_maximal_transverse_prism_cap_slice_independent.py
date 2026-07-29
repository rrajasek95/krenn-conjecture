#!/usr/bin/env python3
"""Clean-room audit of the maximal transverse prism cap slice.

This checker does not import the primary verifier.  It reconstructs the
ten-site source by a subset matching recurrence, computes the cap maps as
81-coordinate linear maps, evaluates the prism hafnian in a separate
square-free coloured-site algebra, and expands the induced eight-site
cap-adjugate determinant directly.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import sympy as sy


PRIMARY_HASHES = {
    "notes/maximal-transverse-prism-cap-slice-countermodel.md":
        "c6936267f51683f659fdc9188ba8e1b69d228c79e9a79f8bd089f3a9d39898aa",
    "computations/verify_maximal_transverse_prism_cap_slice.py":
        "dfd146c42471e2cbb2bb1b70e336e5f5d1fd25b247dbf8fe0a472e36e2a7a965",
}
EXPECTED_LEDGER_SHA256 = "438b55c95bd56a72640f1a78652f64149c331b7a1665fe2f27c974be5f71bb35"

W = ("p", "q", "r", "s")
U = ("x0", "x1", "x2", "y0", "y1", "y2")
ALL = W + U
GLOBAL_POSITION = {vertex: index for index, vertex in enumerate(ALL)}
A = sy.Matrix(((1, 2, 3), (4, 5, 7), (8, 11, 13)))


class SparseSource:
    """Sparse aggregate cells retaining the physical endpoint order."""

    def __init__(self) -> None:
        self.data: dict[tuple[str, str], list[tuple[int, int, sy.Expr]]] = {}

    def add(
        self,
        u: str,
        v: str,
        colour_u: int,
        colour_v: int,
        coefficient: sy.Expr | int = 1,
    ) -> None:
        if GLOBAL_POSITION[u] < GLOBAL_POSITION[v]:
            key = (u, v)
            cell = (colour_u, colour_v, sy.sympify(coefficient))
        else:
            key = (v, u)
            cell = (colour_v, colour_u, sy.sympify(coefficient))
        self.data.setdefault(key, []).append(cell)

    def cells(self, u: str, v: str) -> tuple[tuple[int, int, sy.Expr], ...]:
        if GLOBAL_POSITION[u] < GLOBAL_POSITION[v]:
            return tuple(self.data.get((u, v), ()))
        return tuple(
            (colour_v, colour_u, coefficient)
            for colour_u, colour_v, coefficient in self.data.get((v, u), ())
        )


def build_source() -> SparseSource:
    source = SparseSource()
    for i, j in product(range(3), repeat=2):
        source.add("p", "q", i, j, A[i, j])
    source.add("r", "s", 0, 0)
    source.add("p", "r", 1, 1)
    source.add("q", "s", 2, 2)
    for colour in range(3):
        source.add("p", f"x{colour}", colour, colour)
        source.add("q", f"y{colour}", colour, colour)
        other = tuple(index for index in range(3) if index != colour)
        source.add(f"x{other[0]}", f"x{other[1]}", colour, colour)
        source.add(f"y{other[0]}", f"y{other[1]}", colour, colour)
    return source


def matching_tensor(
    vertices: tuple[str, ...], source: SparseSource
) -> dict[tuple[int, ...], sy.Expr]:
    """Matching tensor by least-vertex subset recursion, not matching lists."""

    @lru_cache(maxsize=None)
    def recurse(remaining: tuple[str, ...]):
        if not remaining:
            return (((), sy.S.One),)
        first = remaining[0]
        answer: dict[tuple[int, ...], sy.Expr] = {}
        for partner_index in range(1, len(remaining)):
            second = remaining[partner_index]
            rest = remaining[1:partner_index] + remaining[partner_index + 1 :]
            for first_colour, second_colour, edge_value in source.cells(first, second):
                for tail_word, tail_value in recurse(rest):
                    assignment = dict(zip(rest, tail_word))
                    assignment[first] = first_colour
                    assignment[second] = second_colour
                    word = tuple(assignment[vertex] for vertex in remaining)
                    answer[word] = sy.expand(
                        answer.get(word, sy.S.Zero) + edge_value * tail_value
                    )
        return tuple(sorted((word, value) for word, value in answer.items() if value != 0))

    return dict(recurse(vertices))


CAP_WORDS = tuple(product(range(3), repeat=4))
CAP_INDEX = {word: index for index, word in enumerate(CAP_WORDS)}
TOP_WORDS = tuple(
    (i, i, i, j, j, j) for i, j in product(range(3), repeat=2)
)
TOP_INDEX = {word: index for index, word in enumerate(TOP_WORDS)}


def cap_output_matrix(
    tensor: dict[tuple[int, ...], sy.Expr], boundary_size: int
) -> sy.Matrix:
    rows = sy.zeros(len(TOP_WORDS), len(CAP_WORDS))
    for word, coefficient in tensor.items():
        cap_word = word[:4]
        boundary_word = word[4 : 4 + boundary_size]
        if boundary_word in TOP_INDEX:
            rows[TOP_INDEX[boundary_word], CAP_INDEX[cap_word]] += coefficient
        else:
            raise AssertionError(("unexpected top boundary word", boundary_word))
    return rows


def coordinate_row(word: tuple[int, int, int, int]) -> sy.Matrix:
    row = sy.zeros(1, 81)
    row[0, CAP_INDEX[word]] = 1
    return row


def kernel_basis(matrix: sy.Matrix) -> sy.Matrix:
    return sy.Matrix.hstack(*matrix.nullspace())


def audit_source_and_cap_maps(source: SparseSource):
    # The asymmetric direct block must transpose when the physical order does.
    assert dict(((i, j), value) for i, j, value in source.cells("q", "p"))[(1, 2)] == A[2, 1]

    internal = matching_tensor(W, source)
    expected_internal = {
        (i, j, 0, 0): A[i, j] for i, j in product(range(3), repeat=2)
    }
    expected_internal[(1, 2, 1, 2)] = sy.S.One
    assert internal == expected_internal

    top = matching_tensor(ALL, source)
    expected_top = {
        (i, j, 0, 0, i, i, i, j, j, j): sy.S.One
        for i, j in product(range(3), repeat=2)
    }
    assert top == expected_top

    desired_global = {(colour,) * 10: sy.S.One for colour in range(3)}
    common = set(top).intersection(desired_global)
    assert common == {(0,) * 10}
    assert len(set(top) - set(desired_global)) == 8
    assert len(set(desired_global) - set(top)) == 2

    top_map = cap_output_matrix(top, 6)
    assert top_map.rank() == 9

    off_diagonal_rows = [
        TOP_INDEX[(i, i, i, j, j, j)]
        for i, j in product(range(3), repeat=2)
        if i != j
    ]
    image_defect = top_map.extract(off_diagonal_rows, range(81))
    assert image_defect.rank() == 6
    image_kernel = kernel_basis(image_defect)
    assert image_kernel.shape == (81, 75)
    assert (top_map * image_kernel).rank() == 3

    target_map = sy.zeros(9, 81)
    for colour in range(3):
        output = TOP_INDEX[(colour,) * 6]
        target_map[output, CAP_INDEX[(colour,) * 4]] = 1
    ghz_defect = top_map - target_map
    assert ghz_defect.rank() == 8
    ghz_kernel = kernel_basis(ghz_defect)
    assert ghz_kernel.shape == (81, 73)
    assert (top_map * ghz_kernel).rank() == 3

    scalar_row = sy.zeros(1, 81)
    for word, coefficient in internal.items():
        scalar_row[0, CAP_INDEX[word]] += coefficient
    z_rows = sy.Matrix.vstack(
        *(coordinate_row((colour, colour, 0, 0)) for colour in range(3))
    )
    effective_map = sy.Matrix.vstack(scalar_row, z_rows)
    assert (effective_map * image_kernel).rank() == 4
    assert (effective_map * ghz_kernel).rank() == 4
    assert image_kernel.shape[1] - (effective_map * image_kernel).rank() == 71
    assert ghz_kernel.shape[1] - (effective_map * ghz_kernel).rank() == 69

    # Explicit right inverse for (s,z0,z1,z2) on the GHZ-formula kernel.
    right_inverse = sy.zeros(81, 4)
    right_inverse[CAP_INDEX[(1, 2, 1, 2)], 0] = 1
    for colour, diagonal_weight in enumerate((1, 5, 13)):
        column = colour + 1
        right_inverse[CAP_INDEX[(colour, colour, 0, 0)], column] = 1
        right_inverse[CAP_INDEX[(colour,) * 4], column] = 1
        right_inverse[CAP_INDEX[(1, 2, 1, 2)], column] = -diagonal_weight
    # At colour zero the two coordinates coincide; do not add it twice.
    right_inverse[CAP_INDEX[(0, 0, 0, 0)], 1] = 1
    assert ghz_defect * right_inverse == sy.zeros(9, 4)
    assert effective_map * right_inverse == sy.eye(4)

    return internal, top, image_defect, ghz_defect


def audit_every_cofactor(source: SparseSource, internal) -> int:
    transverse_rows = 0
    for left, right in combinations(U, 2):
        actual = matching_tensor(W + (left, right), source)
        expected: dict[tuple[int, ...], sy.Expr] = {}
        if left[0] == right[0]:
            missing = ({0, 1, 2} - {int(left[1]), int(right[1])}).pop()
            for cap_word, coefficient in internal.items():
                expected[cap_word + (missing, missing)] = coefficient
        else:
            i = int(left[1])
            j = int(right[1])
            expected[(i, j, 0, 0, i, j)] = sy.S.One
            if i != j:
                transverse_rows += 1
        assert actual == expected, (left, right, actual, expected)
    assert transverse_rows == 6
    return transverse_rows


# A coloured square-free boundary element is keyed by a six-slot word; -1
# means that the site is not occupied yet.
EMPTY = (-1,) * 6
SquareFree = dict[tuple[int, ...], sy.Expr]


def sf_clean(element: SquareFree) -> SquareFree:
    return {
        word: sy.expand(coefficient)
        for word, coefficient in element.items()
        if sy.expand(coefficient) != 0
    }


def sf_add(left: SquareFree, right: SquareFree, scale=sy.S.One) -> SquareFree:
    answer = dict(left)
    for word, coefficient in right.items():
        answer[word] = answer.get(word, sy.S.Zero) + scale * coefficient
    return sf_clean(answer)


def sf_multiply(left: SquareFree, right: SquareFree) -> SquareFree:
    answer: SquareFree = {}
    for word_left, coefficient_left in left.items():
        for word_right, coefficient_right in right.items():
            if any(a != -1 and b != -1 for a, b in zip(word_left, word_right)):
                continue
            word = tuple(a if a != -1 else b for a, b in zip(word_left, word_right))
            answer[word] = answer.get(word, sy.S.Zero) + coefficient_left * coefficient_right
    return sf_clean(answer)


def sf_power(element: SquareFree, exponent: int) -> SquareFree:
    answer = {EMPTY: sy.S.One}
    for _ in range(exponent):
        answer = sf_multiply(answer, element)
    return answer


def edge_element(
    u: str, v: str, colour_u: int, colour_v: int, coefficient
) -> SquareFree:
    word = [-1] * 6
    word[U.index(u)] = colour_u
    word[U.index(v)] = colour_v
    return {tuple(word): sy.sympify(coefficient)}


def shore_quadratic() -> SquareFree:
    answer: SquareFree = {}
    for shore in ("x", "y"):
        for colour in range(3):
            other = tuple(index for index in range(3) if index != colour)
            answer = sf_add(
                answer,
                edge_element(
                    f"{shore}{other[0]}", f"{shore}{other[1]}",
                    colour, colour, 1,
                ),
            )
    return answer


def audit_prism_and_normalization():
    s, z0, z1, z2 = sy.symbols("s z0 z1 z2")
    z = (z0, z1, z2)
    edge_sum: SquareFree = {}
    for word, coefficient in shore_quadratic().items():
        edge_sum[word] = s * coefficient
    for colour in range(3):
        edge_sum = sf_add(
            edge_sum,
            edge_element(
                f"x{colour}", f"y{colour}", colour, colour, z[colour]
            ),
        )

    # The third square-free power counts each perfect matching in 3! orders.
    cube = sf_power(edge_sum, 3)
    hafnian = {word: sy.expand(value / 6) for word, value in cube.items()}
    expected_hafnian = {(colour,) * 6: s**2 * z[colour] for colour in range(3)}
    mixed_word = (0, 1, 2, 0, 1, 2)
    expected_hafnian[mixed_word] = z0 * z1 * z2
    assert hafnian == expected_hafnian
    assert cube == {word: 6 * value for word, value in expected_hafnian.items()}

    capped_top = {(colour,) * 6: z[colour] for colour in range(3)}
    discrepancy = {
        word: sy.expand(
            6 * (s**2 * capped_top.get(word, 0) - hafnian.get(word, 0))
        )
        for word in set(capped_top).union(hafnian)
    }
    discrepancy = {word: value for word, value in discrepancy.items() if value != 0}
    generator = z0 * z1 * z2
    assert discrepancy == {mixed_word: -6 * generator}

    # Exact localization test for I=(generator) at h=s*generator.
    localizer = sy.symbols("localizer")
    h = s * generator
    groebner = sy.groebner(
        (generator, 1 - localizer * h),
        localizer, s, z0, z1, z2,
        order="lex",
    )
    assert groebner.reduce(sy.S.One)[1] == 0
    assert h.subs({s: 1, z0: 1, z1: 1, z2: 1}) == 1
    assert generator.subs({z0: 1, z1: 1, z2: 1}) == 1
    return discrepancy, groebner


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def cofactor_matrix(matrix: sy.Matrix) -> sy.Matrix:
    return sy.Matrix(
        3,
        3,
        lambda i, j: (-1) ** (i + j) * matrix.minor_submatrix(i, j).det(),
    )


def audit_adjugate_rows():
    x = shore_quadratic()
    families: list[list[SquareFree]] = []
    for i in range(3):
        row = []
        for j in range(3):
            direct = {word: A[i, j] * coefficient for word, coefficient in x.items()}
            response = edge_element(f"x{i}", f"y{j}", i, j, 1)
            row.append(sf_add(direct, response))
        families.append(row)

    determinant: SquareFree = {}
    for permutation in permutations(range(3)):
        term = {EMPTY: sy.S.One}
        for i in range(3):
            term = sf_multiply(term, families[i][permutation[i]])
        determinant = sf_add(determinant, term, permutation_sign(permutation))

    cofactors = cofactor_matrix(A)
    expected_cofactors = sy.Matrix(((-12, 4, 4), (7, -11, 5), (-1, 5, -3)))
    assert A.det() == 8
    assert cofactors == expected_cofactors
    expected = {
        (i, i, i, j, j, j): 2 * cofactors[i, j]
        for i, j in product(range(3), repeat=2)
    }
    assert determinant == expected

    diagonal = {(colour,) * 6: 2 * cofactors[colour, colour] for colour in range(3)}
    transverse = sf_add(determinant, diagonal, -1)
    expected_transverse = {
        (i, i, i, j, j, j): 2 * cofactors[i, j]
        for i, j in product(range(3), repeat=2)
        if i != j
    }
    assert transverse == expected_transverse
    assert len(transverse) == 6
    assert all(value != 0 for value in transverse.values())
    return cofactors, transverse


def audit_frozen_inputs() -> None:
    root = Path(__file__).resolve().parents[1]
    for relative_path, expected in PRIMARY_HASHES.items():
        actual = sha256((root / relative_path).read_bytes()).hexdigest()
        assert actual == expected, (relative_path, expected, actual)


def main() -> None:
    audit_frozen_inputs()
    source = build_source()
    internal, top, image_defect, ghz_defect = audit_source_and_cap_maps(source)
    transverse_cofactor_rows = audit_every_cofactor(source, internal)
    discrepancy, groebner = audit_prism_and_normalization()
    cofactors, transverse_determinant = audit_adjugate_rows()

    ledger = {
        "top_terms": len(top),
        "globally_mixed_top_terms": 8,
        "full_top_rank": 9,
        "diagonal_slice_codimension": image_defect.rank(),
        "diagonal_slice_dimension": 81 - image_defect.rank(),
        "ghz_slice_codimension": ghz_defect.rank(),
        "ghz_slice_dimension": 81 - ghz_defect.rank(),
        "effective_rank_on_ghz_slice": 4,
        "common_kernel_on_ghz_slice": 69,
        "transverse_cofactor_rows": transverse_cofactor_rows,
        "adjugate_transverse_rows": len(transverse_determinant),
        "cofactor_matrix": tuple(int(value) for value in cofactors),
        "discrepancy_support": tuple(sorted(discrepancy)),
        "localized_basis": tuple(map(str, groebner.polys)),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True, default=list).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        assert digest == EXPECTED_LEDGER_SHA256, (EXPECTED_LEDGER_SHA256, digest)
    print("full top rank / terms:", ledger["full_top_rank"], ledger["top_terms"])
    print("maximal slice dimensions:", ledger["diagonal_slice_dimension"], ledger["ghz_slice_dimension"])
    print("effective rank / GHZ-slice common kernel:", 4, 69)
    print("cofactor and adjugate transverse rows:", transverse_cofactor_rows, len(transverse_determinant))
    print("independent semantic ledger SHA-256:", digest)
    print("PASS: maximal transverse prism cap-slice independent audit")


if __name__ == "__main__":
    main()

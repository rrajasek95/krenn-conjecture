#!/usr/bin/env python3
"""Exact N=8 to N=10 forced-pair contraction for coefficient cylinders.

Vertices 8 and 9 are adjoined with the isolated diagonal source
E_(89;00)+E_(89;11)+E_(89;22), which retains all three pure anchors.  The
controlled diagonal trace keeps the appended colour equal to the colour at
old vertex zero.  It contracts the lifted matching tensor and Delta_10 to
their N=8 counterparts.  On every old three-site cut, old-hole insertion
columns contract to the N=8 columns and new-hole columns vanish.  The checker
verifies the identity literally and transports one nonzero affine and one
nonzero bilinear quotient-row functional.
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path


Q = Fraction
B8 = tuple(range(8))
B10 = tuple(range(10))
NEW_PAIR = (8, 9)
CUT = 2
C_SET = (2, 6, 7)
U8 = (0, 1, 3, 4, 5)
U10 = U8 + NEW_PAIR

AFFINE_FIXED = (0, 1, 0, 1)
AFFINE_VARIABLE = (1, 4, 0, 1)
AFFINE_BOUNDARY_WORD = (0, 0, 0)
AFFINE_QUOTIENT_INDEX = 27
AFFINE_FUNCTIONAL = {0: Q(-1), 27: Q(1)}

BILINEAR_LEFT = (2, 4, 2, 0)
BILINEAR_RIGHT = (2, 6, 0, 1)
BILINEAR_BOUNDARY_WORD = (2, 1, 1)
BILINEAR_QUOTIENT_INDEX = 10
BILINEAR_FUNCTIONAL = {10: Q(1)}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_positive_moduli_certificate():
    path = Path(__file__).with_name(
        "verify_n8_four_cylinder_positive_moduli_certificate.py"
    )
    spec = importlib.util.spec_from_file_location("positive_moduli", path)
    require(spec is not None and spec.loader is not None, "cannot load certificate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def word_index(word):
    answer = 0
    for colour in word:
        answer = 3 * answer + colour
    return answer


def index_word(index, length):
    word = [0] * length
    for position in range(length - 1, -1, -1):
        word[position] = index % 3
        index //= 3
    require(index == 0, "word index exceeded its declared length")
    return tuple(word)


def tensor_difference(left, right):
    answer = {}
    for word in set(left) | set(right):
        value = left.get(word, Q(0)) - right.get(word, Q(0))
        if value:
            answer[word] = value
    return answer


def delta_tensor(vertices):
    return {(colour,) * len(vertices): Q(1) for colour in range(3)}


def lift_cells(module, old_cells):
    cells = {edge: list(entries) for edge, entries in old_cells.items()}
    module.add_sources(
        cells,
        (
            (8, 9, 0, 0, 1),
            (8, 9, 1, 1, 1),
            (8, 9, 2, 2, 1),
        ),
    )
    return cells


def insertion_columns(module, u_set, cells):
    columns = {}
    for hole in u_set:
        remaining = tuple(vertex for vertex in u_set if vertex != hole)
        cofactor = module.matching_tensor(remaining, cells)
        for colour in range(3):
            column = {}
            for hole_word, coefficient in cofactor.items():
                assignment = {hole: colour}
                assignment.update(zip(remaining, hole_word))
                index = word_index(tuple(assignment[vertex] for vertex in u_set))
                column[index] = column.get(index, Q(0)) + coefficient
                if not column[index]:
                    column.pop(index)
            columns[(hole, colour)] = column
    return columns


def flatten_rows(tensor, vertices, c_set, u_set):
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    rows = {}
    for word, coefficient in tensor.items():
        boundary_word = tuple(word[positions[vertex]] for vertex in c_set)
        interior_word = tuple(word[positions[vertex]] for vertex in u_set)
        row = rows.setdefault(boundary_word, {})
        index = word_index(interior_word)
        row[index] = row.get(index, Q(0)) + coefficient
        if not row[index]:
            row.pop(index)
    return rows


def cut_data(module, vertices, u_set, cells):
    tensor = module.matching_tensor(vertices, cells)
    residual = tensor_difference(tensor, delta_tensor(vertices))
    return {
        "tensor": tensor,
        "residual": residual,
        "columns": insertion_columns(module, u_set, cells),
        "rows": flatten_rows(residual, vertices, C_SET, u_set),
    }


def controlled_pair_contraction_tensor(tensor):
    answer = {}
    for word, coefficient in tensor.items():
        if word[-2] != word[-1] or word[-1] != word[0]:
            continue
        old_word = word[:-2]
        answer[old_word] = answer.get(old_word, Q(0)) + coefficient
        if not answer[old_word]:
            answer.pop(old_word)
    return answer


def controlled_pair_contraction_row(row):
    answer = {}
    for index, coefficient in row.items():
        word = index_word(index, 7)
        if word[-2] != word[-1] or word[-1] != word[0]:
            continue
        old_index = word_index(word[:-2])
        answer[old_index] = answer.get(old_index, Q(0)) + coefficient
        if not answer[old_index]:
            answer.pop(old_index)
    return answer


def lift_functional(functional):
    answer = {}
    for old_index, coefficient in functional.items():
        old_word = index_word(old_index, 5)
        selector_colour = old_word[0]
        lifted_index = word_index(old_word + (selector_colour, selector_colour))
        answer[lifted_index] = coefficient
    return answer


def functional_value(functional, vector):
    return sum(
        coefficient * vector.get(index, Q(0))
        for index, coefficient in functional.items()
    )


def quotient_coordinate_functional(two_cell, basis, quotient_index, dimension):
    functional = {}
    for index in range(dimension):
        value = two_cell.quotient_remainder({index: Q(1)}, basis).get(
            quotient_index, Q(0)
        )
        if value:
            functional[index] = value
    return functional


def sparse_difference(left, right):
    return {
        index: left.get(index, Q(0)) - right.get(index, Q(0))
        for index in set(left) | set(right)
        if left.get(index, Q(0)) != right.get(index, Q(0))
    }


def audit_point(module, old_cells):
    new_cells = lift_cells(module, old_cells)
    old = cut_data(module, B8, U8, old_cells)
    new = cut_data(module, B10, U10, new_cells)

    require(
        controlled_pair_contraction_tensor(new["tensor"]) == old["tensor"],
        "matching tensor did not contract",
    )
    require(
        controlled_pair_contraction_tensor(delta_tensor(B10)) == delta_tensor(B8),
        "target tensor did not contract",
    )
    require(
        controlled_pair_contraction_tensor(new["residual"]) == old["residual"],
        "full residual did not contract",
    )
    for label, old_column in old["columns"].items():
        require(
            controlled_pair_contraction_row(new["columns"][label]) == old_column,
            f"old-hole cofactor column did not contract at {label}",
        )
    for hole in NEW_PAIR:
        for colour in range(3):
            require(
                not new["columns"][(hole, colour)],
                f"new-hole cofactor column is nonzero at {(hole, colour)}",
            )
    for boundary_word in set(old["rows"]) | set(new["rows"]):
        require(
            controlled_pair_contraction_row(new["rows"].get(boundary_word, {}))
            == old["rows"].get(boundary_word, {}),
            f"residual boundary row did not contract at {boundary_word}",
        )
    return old, new


def audit_affine_functional(certificate, two_cell, one_cell, module, base):
    old_data = certificate.affine_cut_data(
        one_cell,
        module,
        base,
        AFFINE_FIXED,
        AFFINE_VARIABLE,
        CUT,
    )
    old_basis = module.rational_basis(
        list(old_data["columns0"]) + list(old_data["column_derivatives"])
    )
    require(len(old_basis) == 17, "affine coefficient-cylinder rank changed")
    old_functional = quotient_coordinate_functional(
        two_cell, old_basis, AFFINE_QUOTIENT_INDEX, 3**5
    )
    require(old_functional == AFFINE_FUNCTIONAL, "affine row functional changed")
    for column in list(old_data["columns0"]) + list(
        old_data["column_derivatives"]
    ):
        require(
            functional_value(old_functional, column) == 0,
            "affine functional does not annihilate N=8 cylinder",
        )
    require(
        functional_value(
            old_functional, old_data["rows0"][AFFINE_BOUNDARY_WORD]
        )
        == 1,
        "affine residual constant changed",
    )
    require(
        functional_value(
            old_functional,
            old_data["row_derivatives"][AFFINE_BOUNDARY_WORD],
        )
        == 0,
        "affine residual derivative changed",
    )

    new_corners = []
    for parameter in (Q(0), Q(1), Q(2)):
        old_cells = certificate.affine_cells(
            module, base, AFFINE_FIXED, AFFINE_VARIABLE, parameter
        )
        _old, new = audit_point(module, old_cells)
        new_corners.append(new)

    new_functional = lift_functional(old_functional)
    require(len(new_functional) == 2, "lifted affine functional support changed")
    new_columns0 = new_corners[0]["columns"]
    for label in new_columns0:
        derivative = sparse_difference(
            new_corners[1]["columns"][label], new_columns0[label]
        )
        require(
            functional_value(new_functional, new_columns0[label]) == 0
            and functional_value(new_functional, derivative) == 0,
            f"lifted affine functional sees cofactor label {label}",
        )
        require(
            sparse_difference(new_corners[2]["columns"][label], new_columns0[label])
            == {index: 2 * value for index, value in derivative.items()},
            f"lifted affine cofactor is not affine at {label}",
        )
    row0 = new_corners[0]["rows"].get(AFFINE_BOUNDARY_WORD, {})
    row1 = new_corners[1]["rows"].get(AFFINE_BOUNDARY_WORD, {})
    row2 = new_corners[2]["rows"].get(AFFINE_BOUNDARY_WORD, {})
    derivative = sparse_difference(row1, row0)
    require(
        functional_value(new_functional, row0) == 1
        and functional_value(new_functional, derivative) == 0,
        "lifted affine obstruction was not preserved",
    )
    require(
        sparse_difference(row2, row0)
        == {index: 2 * value for index, value in derivative.items()},
        "lifted affine residual is not affine",
    )
    return old_functional, new_functional


def audit_bilinear_functional(certificate, two_cell, one_cell, module, base):
    old_corner_cells = {
        (left, right): certificate.bilinear_cells(
            module,
            base,
            BILINEAR_LEFT,
            BILINEAR_RIGHT,
            Q(left),
            Q(right),
        )
        for left in (0, 1)
        for right in (0, 1)
    }
    old_corners = {
        corner: cut_data(module, B8, U8, cells)
        for corner, cells in old_corner_cells.items()
    }
    old_column_components = []
    labels = tuple(old_corners[(0, 0)]["columns"])
    for label in labels:
        old_column_components.extend(
            certificate.bilinear_components(
                one_cell,
                old_corners[(0, 0)]["columns"][label],
                old_corners[(1, 0)]["columns"][label],
                old_corners[(0, 1)]["columns"][label],
                old_corners[(1, 1)]["columns"][label],
            )
        )
    old_basis = module.rational_basis(old_column_components)
    require(len(old_basis) == 14, "bilinear coefficient-cylinder rank changed")
    old_functional = quotient_coordinate_functional(
        two_cell, old_basis, BILINEAR_QUOTIENT_INDEX, 3**5
    )
    require(
        old_functional == BILINEAR_FUNCTIONAL,
        "bilinear row functional changed",
    )
    require(
        all(
            functional_value(old_functional, column) == 0
            for column in old_column_components
        ),
        "bilinear functional does not annihilate N=8 cylinder",
    )

    old_row_components = certificate.bilinear_components(
        one_cell,
        old_corners[(0, 0)]["rows"].get(BILINEAR_BOUNDARY_WORD, {}),
        old_corners[(1, 0)]["rows"].get(BILINEAR_BOUNDARY_WORD, {}),
        old_corners[(0, 1)]["rows"].get(BILINEAR_BOUNDARY_WORD, {}),
        old_corners[(1, 1)]["rows"].get(BILINEAR_BOUNDARY_WORD, {}),
    )
    require(
        tuple(functional_value(old_functional, row) for row in old_row_components)
        == (0, 1, 0, 0),
        "N=8 bilinear obstruction coefficients changed",
    )

    new_corners = {}
    for corner, old_cells in old_corner_cells.items():
        _old, new_corners[corner] = audit_point(module, old_cells)
    extra_cells = certificate.bilinear_cells(
        module,
        base,
        BILINEAR_LEFT,
        BILINEAR_RIGHT,
        Q(2),
        Q(3),
    )
    _old_extra, new_extra = audit_point(module, extra_cells)

    new_functional = lift_functional(old_functional)
    require(len(new_functional) == 1, "lifted bilinear functional support changed")
    new_labels = tuple(new_corners[(0, 0)]["columns"])
    for label in new_labels:
        components = certificate.bilinear_components(
            one_cell,
            new_corners[(0, 0)]["columns"][label],
            new_corners[(1, 0)]["columns"][label],
            new_corners[(0, 1)]["columns"][label],
            new_corners[(1, 1)]["columns"][label],
        )
        require(
            all(
                functional_value(new_functional, component) == 0
                for component in components
            ),
            f"lifted bilinear functional sees cofactor label {label}",
        )
        require(
            certificate.sparse_bilinear_evaluate(
                one_cell, components, Q(2), Q(3)
            )
            == new_extra["columns"][label],
            f"lifted cofactor column is not bilinear at {label}",
        )
    new_row_components = certificate.bilinear_components(
        one_cell,
        new_corners[(0, 0)]["rows"].get(BILINEAR_BOUNDARY_WORD, {}),
        new_corners[(1, 0)]["rows"].get(BILINEAR_BOUNDARY_WORD, {}),
        new_corners[(0, 1)]["rows"].get(BILINEAR_BOUNDARY_WORD, {}),
        new_corners[(1, 1)]["rows"].get(BILINEAR_BOUNDARY_WORD, {}),
    )
    require(
        tuple(functional_value(new_functional, row) for row in new_row_components)
        == (0, 1, 0, 0),
        "lifted bilinear obstruction was not preserved",
    )
    require(
        certificate.sparse_bilinear_evaluate(
            one_cell, new_row_components, Q(2), Q(3)
        )
        == new_extra["rows"].get(BILINEAR_BOUNDARY_WORD, {}),
        "lifted residual row is not bilinear",
    )
    return old_functional, new_functional


def main() -> None:
    certificate = load_positive_moduli_certificate()
    two_cell = certificate.load_two_cell_audit()
    one_cell = two_cell.load_one_cell_elimination()
    unit_gate = one_cell.load_unit_gate()
    module = unit_gate.load_three_cut_verifier()
    base = unit_gate.build_base(module)
    unit_gate.audit_base(module, base)
    lifted_base_tensor = module.matching_tensor(B10, lift_cells(module, base))
    require(
        tuple(lifted_base_tensor.get((colour,) * 10, Q(0)) for colour in range(3))
        == (1, 1, 1),
        "diagonal matched-pair lift did not retain the three pure anchors",
    )

    affine_old, affine_new = audit_affine_functional(
        certificate, two_cell, one_cell, module, base
    )
    bilinear_old, bilinear_new = audit_bilinear_functional(
        certificate, two_cell, one_cell, module, base
    )

    print("N=8 -> N=10 forced-pair coefficient-cylinder contraction: PASS")
    print(
        "affine functional: "
        f"N8 support={len(affine_old)}, N10 support={len(affine_new)}, "
        "residual coefficients=(1,0)"
    )
    print(
        "bilinear functional: "
        f"N8 support={len(bilinear_old)}, N10 support={len(bilinear_new)}, "
        "residual coefficients=(0,1,0,0)"
    )
    print(
        "identity: controlled diagonal contraction sends lifted tensor, target, "
        "residual rows, and old-hole coefficient cylinders to N=8; "
        "new-hole columns vanish"
    )
    print(
        "scope: exact stability under an isolated diagonal matched-pair lift, "
        "not a contraction theorem for arbitrary N=10 sources"
    )


if __name__ == "__main__":
    main()

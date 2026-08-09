#!/usr/bin/env python3
"""Exact one-cross-edge extension of the N=8 -> N=10 cylinder contraction.

Start with the isolated diagonal matched-pair lift and add one source joining
vertex 8 or 9 to an old vertex, with arbitrary weight.  Parity prevents that
source from entering a full ten-site matching.  It can enter only the three
cofactor columns whose hole is the opposite new vertex.

For each cut, control the pair contraction by the old endpoint when that
endpoint lies on the insertion shore.  Every cross contribution then either
vanishes or contracts exactly to the old insertion column at that endpoint.
The checker audits all 144 endpoint-colour coordinates, all six cuts, and the
affine weight identity at 0, 1, 2 over Q.
"""

from __future__ import annotations

import importlib.util
from collections import Counter
from fractions import Fraction
from pathlib import Path


Q = Fraction
B8 = tuple(range(8))
B10 = tuple(range(10))
S = tuple(range(6))
NEW_VERTICES = (8, 9)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_forced_pair_contraction():
    path = Path(__file__).with_name(
        "verify_n8_to_n10_forced_pair_coefficient_cylinder_contraction.py"
    )
    spec = importlib.util.spec_from_file_location("forced_pair", path)
    require(spec is not None and spec.loader is not None, "cannot load contraction")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_cross_source(module, lifted_base, coordinate, weight):
    cells = {edge: list(entries) for edge, entries in lifted_base.items()}
    old, new, old_colour, new_colour = coordinate
    if weight:
        module.add_sources(
            cells,
            ((old, new, old_colour, new_colour, Q(weight)),),
        )
    return cells


def controlled_row_contraction(forced_pair, row, old_u_set, controller):
    new_u_set = old_u_set + NEW_VERTICES
    controller_position = new_u_set.index(controller)
    answer = {}
    for index, coefficient in row.items():
        word = forced_pair.index_word(index, len(new_u_set))
        if word[-2] != word[-1]:
            continue
        if word[-1] != word[controller_position]:
            continue
        old_index = forced_pair.word_index(word[:-2])
        answer[old_index] = answer.get(old_index, Q(0)) + coefficient
        if not answer[old_index]:
            answer.pop(old_index)
    return answer


def controlled_tensor_contraction(tensor, controller):
    answer = {}
    for word, coefficient in tensor.items():
        if word[-2] != word[-1] or word[-1] != word[controller]:
            continue
        old_word = word[:-2]
        answer[old_word] = answer.get(old_word, Q(0)) + coefficient
        if not answer[old_word]:
            answer.pop(old_word)
    return answer


def cut_rows(forced_pair, module, vertices, z, u_set, tensor):
    residual = forced_pair.tensor_difference(
        tensor, forced_pair.delta_tensor(vertices)
    )
    return forced_pair.flatten_rows(residual, vertices, (z, 6, 7), u_set)


def audit_coordinate(
    forced_pair,
    module,
    base,
    lifted_base,
    base_tensor8,
    base_tensor10,
    coordinate,
):
    old, new, old_colour, new_colour = coordinate
    other_new = 17 - new
    cells1 = add_cross_source(module, lifted_base, coordinate, Q(1))
    cells2 = add_cross_source(module, lifted_base, coordinate, Q(2))
    tensor1 = module.matching_tensor(B10, cells1)
    tensor2 = module.matching_tensor(B10, cells2)
    require(
        tensor1 == base_tensor10 and tensor2 == base_tensor10,
        f"one cross edge entered a full matching at {coordinate}",
    )

    signature = []
    census = Counter()
    for z in S:
        old_u_set = tuple(vertex for vertex in S if vertex != z)
        new_u_set = old_u_set + NEW_VERTICES
        controller = old if old in old_u_set else old_u_set[0]
        old_columns = forced_pair.insertion_columns(module, old_u_set, base)
        old_basis = module.rational_basis(list(old_columns.values()))
        columns0 = forced_pair.insertion_columns(module, new_u_set, lifted_base)
        columns1 = forced_pair.insertion_columns(module, new_u_set, cells1)
        columns2 = forced_pair.insertion_columns(module, new_u_set, cells2)

        require(
            controlled_tensor_contraction(base_tensor10, controller) == base_tensor8,
            f"base tensor contraction failed at {(coordinate, z)}",
        )
        require(
            controlled_tensor_contraction(
                forced_pair.delta_tensor(B10), controller
            )
            == forced_pair.delta_tensor(B8),
            f"target contraction failed at {(coordinate, z)}",
        )

        for label, old_column in old_columns.items():
            require(
                controlled_row_contraction(
                    forced_pair, columns0[label], old_u_set, controller
                )
                == old_column,
                f"base old-hole column did not contract at {(coordinate, z, label)}",
            )

        nonzero_contracted = 0
        for label in columns0:
            derivative = forced_pair.sparse_difference(
                columns1[label], columns0[label]
            )
            require(
                forced_pair.sparse_difference(columns2[label], columns0[label])
                == {index: 2 * value for index, value in derivative.items()},
                f"cross cofactor is not affine at {(coordinate, z, label)}",
            )
            contracted = controlled_row_contraction(
                forced_pair, derivative, old_u_set, controller
            )
            require(
                module.rational_member(contracted, old_basis),
                f"cross direction survived modulo old cylinder at {(coordinate, z, label)}",
            )

            hole, inserted_colour = label
            expected = {}
            if (
                old in old_u_set
                and hole == other_new
                and old_colour == new_colour == inserted_colour
            ):
                expected = old_columns[(old, old_colour)]
            require(
                contracted == expected,
                f"contracted cross column formula failed at {(coordinate, z, label)}",
            )
            if contracted:
                nonzero_contracted += 1

            if hole in old_u_set or hole == new:
                require(
                    not derivative,
                    f"cross edge entered a forbidden cofactor column at {(coordinate, z, label)}",
                )

        if nonzero_contracted:
            require(nonzero_contracted == 1, "more than one cross direction survived")
            census["old_column"] += 1
        elif old in old_u_set and old_colour != new_colour:
            census["colour_mismatch_zero"] += 1
        else:
            census["boundary_or_zero"] += 1

        rows10 = cut_rows(
            forced_pair, module, B10, z, new_u_set, base_tensor10
        )
        basis1 = module.rational_basis(list(columns1.values()))
        basis2 = module.rational_basis(list(columns2.values()))
        full1 = all(module.rational_member(row, basis1) for row in rows10.values())
        full2 = all(module.rational_member(row, basis2) for row in rows10.values())
        require(
            not full1 and not full2,
            f"one cross edge created a complete N=10 cylinder at {(coordinate, z)}",
        )
        signature.append((nonzero_contracted, full1, full2))

    return tuple(signature), census


def main() -> None:
    forced_pair = load_forced_pair_contraction()
    certificate = forced_pair.load_positive_moduli_certificate()
    two_cell = certificate.load_two_cell_audit()
    one_cell = two_cell.load_one_cell_elimination()
    unit_gate = one_cell.load_unit_gate()
    module = unit_gate.load_three_cut_verifier()
    base = unit_gate.build_base(module)
    unit_gate.audit_base(module, base)
    lifted_base = forced_pair.lift_cells(module, base)
    base_tensor8 = module.matching_tensor(B8, base)
    base_tensor10 = module.matching_tensor(B10, lifted_base)

    signatures = {}
    total_census = Counter()
    coordinates = []
    for new in NEW_VERTICES:
        for old in B8:
            for old_colour in range(3):
                for new_colour in range(3):
                    coordinate = (old, new, old_colour, new_colour)
                    coordinates.append(coordinate)
                    signature, census = audit_coordinate(
                        forced_pair,
                        module,
                        base,
                        lifted_base,
                        base_tensor8,
                        base_tensor10,
                        coordinate,
                    )
                    signatures[coordinate] = signature
                    total_census.update(census)

    require(len(coordinates) == 144, "cross-coordinate census is incomplete")
    for old in B8:
        for old_colour in range(3):
            for new_colour in range(3):
                require(
                    signatures[(old, 8, old_colour, new_colour)]
                    == signatures[(old, 9, old_colour, new_colour)],
                    f"new-pair swap symmetry failed at {(old, old_colour, new_colour)}",
                )
    require(
        total_census
        == Counter(
            {
                "old_column": 180,
                "colour_mismatch_zero": 360,
                "boundary_or_zero": 324,
            }
        ),
        "cross-edge cut census changed",
    )

    print("N=10 one-cross-edge coefficient-cylinder contraction: PASS")
    print("coordinates: 144 = 72 classes under swapping vertices 8 and 9")
    print(
        "coordinate-cut cases: 864; contracted directions="
        f"old-column {total_census['old_column']}, "
        f"colour-mismatch zero {total_census['colour_mismatch_zero']}, "
        f"boundary/zero {total_census['boundary_or_zero']}"
    )
    print("directions outside the contracted N=8 cylinders: 0")
    print("complete N=10 cylinders at weights 1 or 2: 0 of 864")
    print(
        "verdict: one arbitrary cross edge is eliminated modulo every old cut "
        "cylinder; a failure of induction needs at least two cross edges"
    )


if __name__ == "__main__":
    main()

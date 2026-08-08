#!/usr/bin/env python3
"""Exact arbitrary-complex one-cell elimination for the anchored N=8 gate.

The base is the sixteen-source, three-pure, three-active-cut family audited by
verify_n8_four_cut_unit_cell_falsification_gate.py. For every one of the 236
absent endpoint-colour coordinates x, consider A(t) = A + t*x over C.

For 230 coordinates, the character of x is independent of the characters of
the base support and the three target constraints. A target-stabilizing
one-parameter subgroup therefore fixes A and normalizes every nonzero t to
one; the exact unit representative is tested directly.

The remaining six characters are dependent. For each, an exact affine
cofactor-span calculation produces a row derivative outside the universal
span of all cofactor columns. Hence every nonzero t destroys one of the three
fixed complete cuts. The calculation uses only Q arithmetic; t is eliminated
symbolically by affine linearity, not sampled.
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_unit_gate():
    path = Path(__file__).with_name(
        "verify_n8_four_cut_unit_cell_falsification_gate.py"
    )
    spec = importlib.util.spec_from_file_location("unit_gate", path)
    require(spec is not None and spec.loader is not None, "cannot load unit gate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sparse_difference(left, right):
    return {
        key: left.get(key, Q(0)) - right.get(key, Q(0))
        for key in set(left) | set(right)
        if left.get(key, Q(0)) != right.get(key, Q(0))
    }


def sparse_linear_combination(*terms):
    answer = {}
    for scalar, vector in terms:
        for key, value in vector.items():
            total = answer.get(key, Q(0)) + Q(scalar) * value
            if total:
                answer[key] = total
            else:
                answer.pop(key, None)
    return answer


def coordinate_character(coordinate):
    u, v, colour_u, colour_v = coordinate
    return {3 * u + colour_u: Q(1), 3 * v + colour_v: Q(1)}


def all_coordinates():
    return tuple(
        (u, v, colour_u, colour_v)
        for u in range(8)
        for v in range(u + 1, 8)
        for colour_u in range(3)
        for colour_v in range(3)
    )


def support_coordinates(base):
    return {
        (u, v, colour_u, colour_v)
        for (u, v), entries in base.items()
        for colour_u, colour_v, weight in entries
        if weight
    }


def target_characters():
    return tuple(
        {3 * vertex + colour: Q(1) for vertex in range(8)}
        for colour in range(3)
    )


def add_parameter(module, base, coordinate, value):
    cells = {edge: list(entries) for edge, entries in base.items()}
    if value:
        module.add_sources(cells, ((*coordinate, Q(value)),))
    return cells


def residual_tensor(module, cells):
    return module.tensor_sum(
        module.matching_tensor(module.B, cells), module.scaled(module.DELTA, -1)
    )


def insertion_columns(module, u_set, cells):
    # Retain all fifteen labelled columns, including literal zero columns, so
    # finite differences compare the same source maps at t=0,1,2.
    return tuple(
        module.insertion_column(u_set, hole, colour, cells)
        for hole in u_set
        for colour in range(3)
    )


DEPENDENT_WITNESSES = {
    # coordinate: (cut z, boundary word on C_z)
    (2, 4, 2, 0): (2, (2, 1, 1)),
    (2, 6, 0, 1): (3, (2, 1, 1)),
    (3, 4, 0, 0): (3, (0, 2, 2)),
    (3, 7, 0, 2): (2, (1, 2, 2)),
    (4, 6, 0, 1): (2, (0, 1, 1)),
    (5, 7, 0, 2): (2, (1, 1, 2)),
}


def classify_characters(module, base):
    support = support_coordinates(base)
    require(len(support) == 16, "anchored base support size changed")
    absent = tuple(coordinate for coordinate in all_coordinates() if coordinate not in support)
    require(len(absent) == 236, "absent-coordinate count changed")

    constraints = [coordinate_character(coordinate) for coordinate in sorted(support)]
    constraints.extend(target_characters())
    constraint_basis = module.rational_basis(constraints)
    require(len(constraint_basis) == 15, "base-plus-target character rank changed")

    dependent = tuple(
        coordinate
        for coordinate in absent
        if module.rational_member(coordinate_character(coordinate), constraint_basis)
    )
    independent = tuple(coordinate for coordinate in absent if coordinate not in dependent)
    require(len(independent) == 230, "normalizable-character count changed")
    require(set(dependent) == set(DEPENDENT_WITNESSES), "exceptional characters changed")
    return independent, dependent


def audit_normalizable_representatives(unit_gate, module, base, independent):
    counts = {"pure": 0, "triple": 0, "fourth": 0}
    triple_coordinates = []
    for coordinate in independent:
        cells = add_parameter(module, base, coordinate, Q(1))
        tensor = module.matching_tensor(module.B, cells)
        if unit_gate.pure_tuple(module, tensor) != (1, 1, 1):
            continue
        counts["pure"] += 1
        if not all(
            unit_gate.active_complete(module.cut_record(z, cells))
            for z in unit_gate.THREE_CUTS
        ):
            continue
        counts["triple"] += 1
        triple_coordinates.append(coordinate)
        for z in unit_gate.FOURTH_CUT_CANDIDATES:
            if unit_gate.active_complete(module.cut_record(z, cells)):
                counts["fourth"] += 1
                raise RuntimeError(
                    f"normalizable arbitrary-weight falsifier at {coordinate}, cut {z}"
                )

    require(
        counts == {"pure": 230, "triple": 14, "fourth": 0},
        "normalizable representative census changed",
    )
    require(len(set(triple_coordinates)) == 14, "triple ledger has duplicates")
    return counts


def audit_dependent_direction(module, base, coordinate, witness):
    z, boundary_word = witness
    u_set = tuple(vertex for vertex in module.S if vertex != z)
    c_set = (z, 6, 7)
    cells0 = add_parameter(module, base, coordinate, Q(0))
    cells1 = add_parameter(module, base, coordinate, Q(1))
    cells2 = add_parameter(module, base, coordinate, Q(2))

    columns0 = insertion_columns(module, u_set, cells0)
    columns1 = insertion_columns(module, u_set, cells1)
    columns2 = insertion_columns(module, u_set, cells2)
    derivatives = tuple(
        sparse_difference(column1, column0)
        for column0, column1 in zip(columns0, columns1)
    )
    for column0, column1, column2 in zip(columns0, columns1, columns2):
        require(
            not sparse_linear_combination((1, column2), (-2, column1), (1, column0)),
            f"cofactor column is not affine for {coordinate}",
        )

    base_basis = module.rational_basis(list(columns0))
    universal_basis = module.rational_basis(list(columns0) + list(derivatives))
    require(len(universal_basis) == 14, f"universal rank changed for {coordinate}")

    rows = []
    for cells in (cells0, cells1, cells2):
        rows.append(module.flatten_rows(residual_tensor(module, cells), c_set, u_set))
    all_boundary_words = set(rows[0]) | set(rows[1]) | set(rows[2])
    for word in all_boundary_words:
        row0 = rows[0].get(word, {})
        row1 = rows[1].get(word, {})
        row2 = rows[2].get(word, {})
        require(
            not sparse_linear_combination((1, row2), (-2, row1), (1, row0)),
            f"residual row is not affine for {coordinate}",
        )

    row0 = rows[0].get(boundary_word, {})
    row1 = rows[1].get(boundary_word, {})
    derivative = sparse_difference(row1, row0)
    require(
        module.rational_member(row0, base_basis),
        f"base row left its insertion space for {coordinate}",
    )
    require(len(derivative) == 1, f"witness derivative is not one-sparse for {coordinate}")
    require(
        not module.rational_member(derivative, universal_basis),
        f"witness derivative entered universal cofactor span for {coordinate}",
    )
    return z, boundary_word, next(iter(derivative.values()))


def main() -> None:
    unit_gate = load_unit_gate()
    module = unit_gate.load_three_cut_verifier()
    base = unit_gate.build_base(module)
    unit_gate.audit_base(module, base)
    require(
        not any(
            unit_gate.active_complete(module.cut_record(z, base))
            for z in unit_gate.FOURTH_CUT_CANDIDATES
        ),
        "base unexpectedly has a fourth active cut",
    )

    independent, dependent = classify_characters(module, base)
    counts = audit_normalizable_representatives(unit_gate, module, base, independent)
    witness_records = tuple(
        (coordinate,)
        + audit_dependent_direction(
            module, base, coordinate, DEPENDENT_WITNESSES[coordinate]
        )
        for coordinate in dependent
    )
    require(len(witness_records) == 6, "dependent witness count changed")
    require(
        all(value == 1 for *_prefix, value in witness_records),
        "dependent derivative coefficient changed",
    )

    print("N=8 arbitrary-weight one-cell four-cut elimination: PASS")
    print("absent coordinates: 236 = 230 torus-normalizable + 6 dependent")
    print(
        "unit representatives: "
        f"pure={counts['pure']}, triple-active={counts['triple']}, "
        f"fourth-cut={counts['fourth']}"
    )
    print("dependent directions: 6/6 have exact affine out-of-span witnesses")
    print("verdict: no arbitrary complex one-cell addition reaches a fourth active cut")


if __name__ == "__main__":
    main()

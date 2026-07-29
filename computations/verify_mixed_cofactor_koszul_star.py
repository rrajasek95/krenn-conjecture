#!/usr/bin/env python3
"""Audit the mixed common-cofactor Koszul star in the active binary gadget."""

from __future__ import annotations

import itertools
from fractions import Fraction

from verify_active_ranktwo_binary_gadget import MATRICES, N, induced_tensor
from verify_binary_spinflip_cycle_identity import perfect_matchings


VERTICES = tuple(range(N))
COLORINGS = tuple(itertools.product((0, 1), repeat=N))


def incident_cells(p):
    """Yield (neighbor, p_color, neighbor_color, value)."""
    for (u, v), matrix in MATRICES.items():
        if p == u:
            for p_color, neighbor_color in itertools.product((0, 1), repeat=2):
                value = matrix[p_color][neighbor_color]
                if value:
                    yield v, p_color, neighbor_color, value
        elif p == v:
            for neighbor_color, p_color in itertools.product((0, 1), repeat=2):
                value = matrix[neighbor_color][p_color]
                if value:
                    yield u, p_color, neighbor_color, value


def derivative_atom(p, neighbor, p_color, neighbor_color):
    complement = tuple(v for v in VERTICES if v not in (p, neighbor))
    cofactor = induced_tensor(complement)
    vector = []
    for coloring in COLORINGS:
        if coloring[p] != p_color or coloring[neighbor] != neighbor_color:
            vector.append(0)
        else:
            vector.append(cofactor[tuple(coloring[v] for v in complement)])
    return tuple(vector)


def rank(columns):
    if not columns:
        return 0
    matrix = [list(map(Fraction, row)) for row in zip(*columns)]
    rows = len(matrix)
    cols = len(matrix[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for r in range(rows):
            if r != pivot_row and matrix[r][col]:
                scale = matrix[r][col]
                matrix[r] = [
                    entry - scale * pivot_entry
                    for entry, pivot_entry in zip(matrix[r], matrix[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def sparse(vector):
    return {COLORINGS[index]: value for index, value in enumerate(vector) if value}


def full_tensor(matrices):
    answer = {}
    for coloring in COLORINGS:
        value = 0
        for matching in perfect_matchings(VERTICES):
            term = 1
            for u, v in matching:
                term *= matrices.get((u, v), ((0, 0), (0, 0)))[coloring[u]][
                    coloring[v]
                ]
            value += term
        answer[coloring] = value
    return answer


def verify_fixed_star_zero():
    p = 0
    cells = list(incident_cells(p))
    assert cells == [
        (1, 0, 0, 1),
        (2, 0, 1, -1),
        (5, 1, 1, 1),
    ]

    atom_01 = derivative_atom(0, 1, 0, 0)
    atom_02 = derivative_atom(0, 2, 0, 1)
    atom_05 = derivative_atom(0, 5, 1, 1)
    zero = (0, 0, 0, 0, 0, 0)
    defect = (0, 0, 1, 1, 0, 0)
    one = (1, 1, 1, 1, 1, 1)
    assert sparse(atom_01) == {zero: 1, defect: 1}
    assert sparse(atom_02) == {defect: 1}
    assert sparse(atom_05) == {one: 1}
    assert rank((atom_01, atom_02)) == 2

    reconstructed_zero = tuple(a - b for a, b in zip(atom_01, atom_02))
    assert sparse(reconstructed_zero) == {zero: 1}
    assert sparse(atom_05) == {one: 1}


def audit_all_stars():
    report = {}
    for p in VERTICES:
        for p_color in (0, 1):
            cells = [cell for cell in incident_cells(p) if cell[1] == p_color]
            atoms = [
                derivative_atom(p, neighbor, p_color, neighbor_color)
                for neighbor, _, neighbor_color, _ in cells
            ]
            report[(p, p_color)] = (len(atoms), rank(atoms))
    return report


def verify_second_center_lift():
    defect = (0, 0, 1, 1, 0, 0)
    one = (1, 1, 1, 1, 1, 1)

    atom_23_at_2 = derivative_atom(2, 3, 1, 1)
    atom_20 = derivative_atom(2, 0, 1, 0)
    atom_21 = derivative_atom(2, 1, 1, 1)
    assert sparse(atom_23_at_2) == {defect: 1}
    assert atom_23_at_2 == atom_20
    assert sparse(atom_21) == {one: 1}

    atom_23_at_3 = derivative_atom(3, 2, 1, 1)
    atom_31 = derivative_atom(3, 1, 1, 0)
    atom_34 = derivative_atom(3, 4, 1, 1)
    assert sparse(atom_23_at_3) == {defect: 1}
    assert tuple(a + b for a, b in zip(atom_23_at_3, atom_31)) == (0,) * 64
    assert sparse(atom_34) == {one: 1}

    reduced = dict(MATRICES)
    reduced[(2, 3)] = ((1, 0), (0, 0))
    del reduced[(0, 2)]
    for coloring, value in full_tensor(reduced).items():
        assert value == int(not any(coloring) or all(coloring)), coloring


def main():
    verify_fixed_star_zero()
    verify_second_center_lift()
    report = audit_all_stars()
    assert report[(0, 0)] == (2, 2)
    assert report[(0, 1)] == (1, 1)
    dependent = {
        key: dimensions
        for key, dimensions in report.items()
        if dimensions[0] != dimensions[1]
    }
    assert dependent == {(2, 1): (3, 2), (3, 1): (3, 2)}
    print("verified mixed defect cancellation at p=0 with independent row atoms")
    print("verified clean lifts and support reduction at defect centers 2 and 3")
    print("all-star (nonzero incident cells, derivative rank):", report)
    print("locally dependent star rows:", dependent)


if __name__ == "__main__":
    main()

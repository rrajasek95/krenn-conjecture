#!/usr/bin/env python3
"""Exact support/cylinder tools for an arbitrary 3x3 A_23 block.

The eight other internal aggregate cells remain fixed.  Cells of A_23 use
row-major bit order.  This driver exposes the nine disjoint variable output
blocks, torus exponent vectors, cylinder intersections, and coordinate
quotients used to extend the five-cell theorem.
"""

from __future__ import annotations

import argparse
import collections
import itertools

import explore_three_cut_internal_23_perturbation as equations


Q = equations.Q
SIX = equations.SIX
COLOURS = equations.COLOURS
CELLS = tuple(itertools.product(COLOURS, repeat=2))
CELL_NAMES = tuple(f"x{a}{b}" for a, b in CELLS)
DIAGONAL_BITS = (0, 4, 8)
OUTSIDE_BITS = (3, 5, 6, 8)  # outside the old L; x22 is also diagonal
OLD_L_BITS = (0, 1, 2, 4, 7)
UPLUS = equations.cylinders.matching_tensor(
    SIX,
    {edge: dict(block) for edge, block in equations.cylinders.aggregate().items()
     if edge != (2, 3)},
)


def support_name(mask: int):
    names = [name for bit, name in enumerate(CELL_NAMES) if mask & (1 << bit)]
    return "+".join(names) if names else "zero"


def blocks_for_coefficients(coefficients):
    blocks = equations.cylinders.aggregate()
    block = {
        cell: Q(value) for cell, value in coefficients.items() if value
    }
    blocks[2, 3] = block
    return blocks


def blocks_for_mask(mask: int):
    return blocks_for_coefficients({
        cell: Q(1) for bit, cell in enumerate(CELLS) if mask & (1 << bit)
    })


def subtract(left, right):
    answer = dict(left)
    for word, coefficient in right.items():
        equations.cylinders.add(answer, word, -coefficient)
    return answer


def cell_coordinate_block(bit: int):
    zero = blocks_for_mask(0)
    cell = blocks_for_mask(1 << bit)
    coordinates = set()
    details = {}
    for i, j in ((0, 1), (0, 5), (1, 5), (4, 5)):
        rest = tuple(site for site in SIX if site not in (i, j))
        variable = subtract(
            equations.cylinders.matching_tensor(rest, cell),
            equations.cylinders.matching_tensor(rest, zero),
        )
        details[i, j] = variable
        for rest_word in variable:
            for ci, cj in itertools.product(COLOURS, repeat=2):
                assignment = dict(zip(rest, rest_word))
                assignment[i] = ci
                assignment[j] = cj
                coordinates.add(tuple(assignment[site] for site in SIX))
    return coordinates, details


def killed_coordinates(maximal_mask: int, retained_bits=()):
    killed = set()
    retained = set(retained_bits)
    for bit in range(9):
        if maximal_mask & (1 << bit) and bit not in retained:
            killed.update(cell_coordinate_block(bit)[0])
    killed.update(UPLUS)
    for bit in retained:
        killed.difference_update(cell_coordinate_block(bit)[0])
    return killed


def project_vector(vector, killed):
    return {word: value for word, value in vector.items() if word not in killed}


def projected_problem(coefficients, maximal_mask, retained_bits=(), normal="line"):
    killed = killed_coordinates(maximal_mask, retained_bits)
    blocks = blocks_for_coefficients(coefficients)
    terms = equations.reconstruct_word_terms(blocks)
    projected = collections.defaultdict(list)
    for word, values in terms.items():
        if word not in killed:
            projected[word].extend(values)
    hs = equations.cylinders.matching_tensor(SIX, blocks)
    moving = subtract(hs, UPLUS)
    raw = (hs,) if normal == "line" else (moving, UPLUS)
    basis = [project_vector(vector, killed) for vector in raw]
    basis = [vector for vector in basis if vector]
    return projected, killed, basis


def projected_cylinder_columns(z, blocks, killed):
    u_sites = tuple(site for site in SIX if site != z)
    five_columns = equations.cylinders.insertion_columns(u_sites, blocks)
    lifted = []
    for colour_z in COLOURS:
        for column in five_columns:
            vector = {}
            for u_word, coefficient in column.items():
                assignment = dict(zip(u_sites, u_word))
                assignment[z] = colour_z
                word = tuple(assignment[site] for site in SIX)
                if word not in killed:
                    equations.cylinders.add(vector, word, coefficient)
            if vector:
                lifted.append(vector)
    return list(equations.cylinders.echelon(lifted).values())


def projected_cylinder_intersection(cuts, blocks, killed):
    spaces = {
        z: projected_cylinder_columns(z, blocks, killed) for z in cuts
    }
    coordinates = tuple(sorted({
        word for columns in spaces.values() for vector in columns for word in vector
    }))
    equations_all = []
    for columns in spaces.values():
        equations_all.extend(
            equations.cylinders.annihilator_basis(columns, coordinates)
        )
    return equations.cylinders.annihilator_basis(equations_all, coordinates)


def expanded_projected_cylinder_intersection(cuts, block_families, killed):
    """Intersect cylinders after independently spanning supplied parameters.

    For each cut, take the span of its projected cylinder spaces over every
    supplied block specialization.  This contains the cylinder at every
    linear combination of those specializations and hence gives a safe,
    parameter-independent upper bound on the projected common normal.
    """
    spaces = {}
    for z in cuts:
        columns = []
        for blocks in block_families:
            columns.extend(projected_cylinder_columns(z, blocks, killed))
        spaces[z] = list(equations.cylinders.echelon(columns).values())
    coordinates = tuple(sorted({
        word for columns in spaces.values() for vector in columns for word in vector
    }))
    equations_all = []
    for columns in spaces.values():
        equations_all.extend(
            equations.cylinders.annihilator_basis(columns, coordinates)
        )
    return equations.cylinders.annihilator_basis(equations_all, coordinates)


def torus_exponent(cell):
    a, b = cell
    vector = [0] * 5  # r0,c0,c2,r1,r2
    vector[{0: 0, 1: 3, 2: 4}[a]] += 1
    vector[{0: 1, 1: 0, 2: 2}[b]] += 1
    return tuple(vector)


def target_absorption(basis, killed):
    span = equations.cylinders.echelon(basis)
    return tuple(
        c for c in COLOURS
        if (c,) * 6 in killed
        or equations.cylinders.member({(c,) * 6: Q(1)}, span)
    )


def census(coefficients):
    blocks = blocks_for_coefficients(coefficients)
    hs = equations.cylinders.matching_tensor(SIX, blocks)
    normals = {
        z: equations.cylinders.cylinder_intersection((2, 3, 4, z), blocks)
        for z in (0, 1, 5)
    }
    return hs, normals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mask", type=lambda value: int(value, 0), default=1 << 3)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    coefficients = {
        cell: Q(1) for bit, cell in enumerate(CELLS) if args.mask & (1 << bit)
    }
    hs, normals = census(coefficients)
    print("mask", args.mask, support_name(args.mask))
    print("torus_rank", __import__("sympy").Matrix([
        torus_exponent(cell) for bit, cell in enumerate(CELLS)
        if args.mask & (1 << bit)
    ]).rank())
    print("H_terms", len(hs))
    for z in (0, 1, 5):
        print(
            "cut", z, "normal_dim", len(normals[z]),
            "line_H", equations.same_span(normals[z], [hs]),
            "absorbed", target_absorption(normals[z], set()),
        )
    if args.verbose:
        for z in (0, 1, 5):
            print("normal", z, normals[z])


if __name__ == "__main__":
    main()

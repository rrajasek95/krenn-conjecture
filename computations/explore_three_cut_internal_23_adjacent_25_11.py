#!/usr/bin/env python3
"""Exact reconnaissance for arbitrary A_23 and A_25=E_00+t E_11.

The edges 23 and 25 share site 2, so no perfect matching can use an A_23
cell and the moving E_11 cell of A_25 simultaneously.  This script checks
that separation literally, reconstructs the fixed-cell stabilizer, compares
the ten variable-output coordinate blocks, and tests small coordinate
quotients that preserve two diagonal target fibres.

It is an exploration helper, not a theorem certificate.
"""

from __future__ import annotations

import itertools

import sympy as sp

import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


Q = full.Q
SIX = full.SIX
COLOURS = full.COLOURS
T_EDGE = (2, 5)
T_CELL = (1, 1)
ALL_X_BITS = tuple(range(9))


def blocks_for(coefficients, t=Q(0)):
    blocks = full.blocks_for_coefficients(coefficients)
    block = dict(blocks[T_EDGE])
    if t:
        block[T_CELL] = block.get(T_CELL, Q(0)) + Q(t)
    blocks[T_EDGE] = block
    return blocks


def subtract(left, right):
    answer = dict(left)
    for word, coefficient in right.items():
        equations.cylinders.add(answer, word, -coefficient)
    return answer


def variable_coordinate_block(edge, cell):
    zero = blocks_for({}, Q(0))
    moved = blocks_for(
        {cell: Q(1)} if edge == (2, 3) else {},
        Q(1) if edge == T_EDGE else Q(0),
    )
    coordinates = set()
    details = {}
    for i in SIX:
        for j in range(i + 1, 6):
            rest = tuple(site for site in SIX if site not in (i, j))
            variable = subtract(
                equations.cylinders.matching_tensor(rest, moved),
                equations.cylinders.matching_tensor(rest, zero),
            )
            if not variable:
                continue
            details[i, j] = variable
            for rest_word in variable:
                for ci, cj in itertools.product(COLOURS, repeat=2):
                    assignment = dict(zip(rest, rest_word))
                    assignment[i] = ci
                    assignment[j] = cj
                    coordinates.add(tuple(assignment[site] for site in SIX))
    return coordinates, details


X_BLOCKS = tuple(full.cell_coordinate_block(bit)[0] for bit in ALL_X_BITS)
T_BLOCK, T_DETAILS = variable_coordinate_block(T_EDGE, T_CELL)


def no_mixed_x_t_terms():
    base = blocks_for({}, Q(0))
    t_only = blocks_for({}, Q(1))
    for bit, cell in enumerate(full.CELLS):
        x_only = blocks_for({cell: Q(1)}, Q(0))
        both = blocks_for({cell: Q(1)}, Q(1))
        for size in (0, 2, 4, 6):
            for sites in itertools.combinations(SIX, size):
                mixed = subtract(
                    subtract(
                        equations.cylinders.matching_tensor(sites, both),
                        equations.cylinders.matching_tensor(sites, x_only),
                    ),
                    subtract(
                        equations.cylinders.matching_tensor(sites, t_only),
                        equations.cylinders.matching_tensor(sites, base),
                    ),
                )
                assert not mixed, (bit, sites, mixed)


def site_weight(site, colour):
    vector = [0] * 18
    vector[3 * site + colour] = 1
    return sp.Matrix([vector])


def cell_weight(edge, cell):
    i, j = edge
    a, b = cell
    return site_weight(i, a) + site_weight(j, b)


def stabilizer_audit():
    fixed = (
        ((0, 1), (0, 0)),
        ((4, 5), (0, 0)),
        ((0, 2), (1, 1)),
        ((1, 4), (1, 1)),
        ((0, 4), (2, 2)),
        ((1, 3), (2, 2)),
        ((2, 5), (0, 0)),
        ((3, 5), (1, 0)),
    )
    constraints = sp.Matrix.vstack(*(cell_weight(edge, cell) for edge, cell in fixed))
    assert constraints.rank() == 8
    kernel_columns = constraints.nullspace()
    assert len(kernel_columns) == 10
    kernel = sp.Matrix.hstack(*kernel_columns)
    x_rows = sp.Matrix.vstack(*(
        cell_weight((2, 3), cell) * kernel for cell in full.CELLS
    ))
    t_row = cell_weight(T_EDGE, T_CELL) * kernel
    assert x_rows.rank() == 5
    assert sp.Matrix.vstack(x_rows, t_row).rank() == 6
    # The moving A_25 weight adds one independent effective character.
    for mask in range(1 << 9):
        rows = [
            x_rows.row(bit) for bit in ALL_X_BITS if mask & (1 << bit)
        ]
        x_rank = sp.Matrix.vstack(*rows).rank() if rows else 0
        xt_rank = sp.Matrix.vstack(*(rows + [t_row])).rank()
        assert xt_rank == x_rank + 1
    return constraints, x_rows, t_row


def quotient_killed(retained_x=(), retain_t=False):
    retained_x = set(retained_x)
    retained_union = set().union(*(X_BLOCKS[bit] for bit in retained_x))
    if retain_t:
        retained_union.update(T_BLOCK)
    # Fixed U_+ coordinates may be resurrected when a retained moving block
    # needs them.  Coordinates belonging to an unretained variable block may
    # not: killing them is what makes that coefficient genuinely arbitrary.
    killed = set(full.UPLUS) - retained_union
    for bit in ALL_X_BITS:
        if bit not in retained_x:
            killed.update(X_BLOCKS[bit])
    if not retain_t:
        killed.update(T_BLOCK)
    return killed


def projected_terms(blocks, killed):
    return {
        word: tuple(values)
        for word, values in equations.reconstruct_word_terms(blocks).items()
        if word not in killed
    }


def quotient_record(retained_x, retain_t, coefficients, t, colours):
    killed = quotient_killed(retained_x, retain_t)
    blocks = blocks_for(coefficients, t)
    terms = projected_terms(blocks, killed)
    normals = tuple(
        full.projected_cylinder_intersection((2, 3, 4, z), blocks, killed)
        for z in (0, 1, 5)
    )
    same = (
        equations.same_span(normals[0], normals[1])
        and equations.same_span(normals[0], normals[2])
    )
    target_state = tuple(
        (
            colour,
            (colour,) * 6 in killed,
            equations.cylinders.member(
                {(colour,) * 6: Q(1)},
                equations.cylinders.echelon(normals[0]),
            ),
        )
        for colour in colours
    )
    hs = equations.cylinders.matching_tensor(SIX, blocks)
    hs_in = equations.cylinders.member(
        full.project_vector(hs, killed),
        equations.cylinders.echelon(normals[0]),
    )
    return {
        "kept": 3 ** 6 - len(killed),
        "terms": len(terms),
        "dims": tuple(len(normal) for normal in normals),
        "same": same,
        "targets": target_state,
        "hs_in": hs_in,
    }


def print_coordinate_audit():
    print("no_x_t_mixed_matching_terms PASS")
    print("x_block_sizes", tuple(len(block) for block in X_BLOCKS))
    print("t_block_size", len(T_BLOCK), "dependent_deleted_pairs", tuple(T_DETAILS))
    overlaps = tuple(len(T_BLOCK & block) for block in X_BLOCKS)
    print("t_x_overlaps", dict(zip(full.CELL_NAMES, overlaps)))
    print("t_uplus_overlap", len(T_BLOCK & set(full.UPLUS)))
    for colour in COLOURS:
        word = (colour,) * 6
        print(
            "target", colour,
            "in_t", word in T_BLOCK,
            "in_x", tuple(
                full.CELL_NAMES[bit] for bit, block in enumerate(X_BLOCKS)
                if word in block
            ),
        )


def print_small_quotients():
    candidates = (
        ("kill_t_keep_x00_x22", (0, 8), False, (0, 2)),
        ("keep_t_x11_x22", (4, 8), True, (1, 2)),
        ("keep_t_x00_x22", (0, 8), True, (0, 2)),
    )
    for name, retained, retain_t, colours in candidates:
        print("QUOTIENT", name, "retained", retained, "colours", colours)
        for pattern in range(1 << len(retained)):
            coefficients = {
                full.CELLS[bit]: Q(1)
                for offset, bit in enumerate(retained)
                if pattern & (1 << offset)
            }
            record = quotient_record(
                retained, retain_t, coefficients,
                Q(1) if retain_t else Q(0), colours,
            )
            print(" pattern", pattern, record)


def print_crossratio_geometry():
    retained = (4, 5, 7, 8)
    base_coefficients = {
        full.CELLS[4]: Q(1),
        full.CELLS[5]: Q(1),
        full.CELLS[8]: Q(1),
    }
    one_coefficients = dict(base_coefficients)
    one_coefficients[full.CELLS[7]] = Q(1)
    killed = quotient_killed(retained, retain_t=True)
    base_blocks = blocks_for(base_coefficients, Q(1))
    one_blocks = blocks_for(one_coefficients, Q(1))
    hs_base = full.project_vector(
        equations.cylinders.matching_tensor(SIX, base_blocks), killed
    )
    hs_one = full.project_vector(
        equations.cylinders.matching_tensor(SIX, one_blocks), killed
    )
    print("CROSSRATIO", "kept", 3 ** 6 - len(killed))
    print(" h0", hs_base)
    print(" h1", hs_one)
    for cut in (0, 1, 5):
        expanded = full.expanded_projected_cylinder_intersection(
            (2, 3, 4, cut), (base_blocks, one_blocks), killed
        )
        at_zero = full.projected_cylinder_intersection(
            (2, 3, 4, cut), base_blocks, killed
        )
        at_one = full.projected_cylinder_intersection(
            (2, 3, 4, cut), one_blocks, killed
        )
        print(
            " cut", cut, "expanded_dim", len(expanded),
            "zero_dim", len(at_zero), "one_dim", len(at_one),
            "expanded_basis", expanded,
        )


def main():
    no_mixed_x_t_terms()
    _constraints, x_rows, t_row = stabilizer_audit()
    print(
        "fixed_stabilizer_dimension", 10,
        "effective_x_rank", x_rows.rank(),
        "effective_x_t_rank", sp.Matrix.vstack(x_rows, t_row).rank(),
    )
    print_coordinate_audit()
    print_small_quotients()
    print_crossratio_geometry()


if __name__ == "__main__":
    main()

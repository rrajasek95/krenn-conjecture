#!/usr/bin/env python3
"""Exact reconnaissance for all one-cell directions out of E00 in A25.

This deliberately reuses the audited endpoint-ordered matching/cylinder
implementation, but replaces the moving A25 cell before rebuilding its
coordinate block.  It reports the torus rank and the quotient geometry used
by the E11 proof for every other cell.  It does not claim a theorem: the
resulting shared-star ideals are checked by the standalone verifier.
"""

from __future__ import annotations

import itertools

import sympy as sp

import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import verify_three_cut_internal_23_arbitrary_block_fourth_cut_obstruction as old_full
import verify_three_cut_internal_23_plane_support_fourth_cut_obstruction as old_locus
import test_three_cut_internal_23_x12_crossratio_symbolic as old_symbolic


Q = full.Q
COLOUR_PAIRS = tuple(itertools.combinations(full.COLOURS, 2))
LOCAL_TO_FULL = (0, 1, 2, 4, 7)


def select_direction(cell):
    adjacent.T_CELL = cell
    adjacent.T_BLOCK, adjacent.T_DETAILS = adjacent.variable_coordinate_block(
        adjacent.T_EDGE, cell
    )


def torus_rows():
    fixed = (
        ((0, 1), (0, 0)), ((4, 5), (0, 0)),
        ((0, 2), (1, 1)), ((1, 4), (1, 1)),
        ((0, 4), (2, 2)), ((1, 3), (2, 2)),
        ((2, 5), (0, 0)), ((3, 5), (1, 0)),
    )
    constraints = sp.Matrix.vstack(*(
        adjacent.cell_weight(edge, cell) for edge, cell in fixed
    ))
    kernel = sp.Matrix.hstack(*constraints.nullspace())
    x_rows = sp.Matrix.vstack(*(
        adjacent.cell_weight((2, 3), cell) * kernel for cell in full.CELLS
    ))
    t_row = adjacent.cell_weight(adjacent.T_EDGE, adjacent.T_CELL) * kernel
    return x_rows, t_row


def admissible_pairs(normal, killed):
    span = equations.cylinders.echelon(normal)
    answer = []
    for pair in COLOUR_PAIRS:
        if all(
            (colour,) * 6 not in killed
            and not equations.cylinders.member(
                {(colour,) * 6: Q(1)}, span
            )
            for colour in pair
        ):
            answer.append(pair)
    return tuple(answer)


def outside_geometry():
    records = []
    for name, spec in old_full.FAMILIES.items():
        for pattern in spec["patterns"]:
            for x21 in spec["x21"]:
                if name == "x12" and pattern == 6 and x21:
                    continue
                coefficients = old_full.coefficients_for_case(spec, pattern, x21)
                blocks = adjacent.blocks_for(coefficients, Q(1))
                killed = adjacent.quotient_killed(spec["retained"], retain_t=True)
                normals = tuple(
                    full.projected_cylinder_intersection(
                        (2, 3, 4, cut), blocks, killed
                    )
                    for cut in (0, 1, 5)
                )
                same = (
                    equations.same_span(normals[0], normals[1])
                    and equations.same_span(normals[0], normals[2])
                )
                hs = full.project_vector(
                    equations.cylinders.matching_tensor(full.SIX, blocks), killed
                )
                hs_in = equations.cylinders.member(
                    hs, equations.cylinders.echelon(normals[0])
                )
                records.append((
                    name, pattern, x21, len(normals[0]), same, hs_in,
                    admissible_pairs(normals[0], killed), len(killed),
                ))
    return tuple(records)


def local_full_bits(mask):
    return tuple(
        LOCAL_TO_FULL[bit] for bit in range(5) if mask & (1 << bit)
    )


def old_geometry():
    records = []
    for spec in old_locus.CLASS_SPECS:
        name, maximal, retained_local = spec[:3]
        representative = sum(1 << bit for bit in retained_local)
        maximal_full = set(local_full_bits(maximal))
        retained_full = {LOCAL_TO_FULL[bit] for bit in retained_local}
        retained_union = set(adjacent.T_BLOCK)
        for bit in retained_full:
            retained_union.update(adjacent.X_BLOCKS[bit])
        killed = set(full.UPLUS) - retained_union
        for bit in maximal_full - retained_full:
            killed.update(adjacent.X_BLOCKS[bit])
        coefficients = {
            full.CELLS[bit]: Q(1) for bit in local_full_bits(representative)
        }
        blocks = adjacent.blocks_for(coefficients, Q(1))
        normals = tuple(
            full.projected_cylinder_intersection(
                (2, 3, 4, cut), blocks, killed
            )
            for cut in (0, 1, 5)
        )
        same = (
            equations.same_span(normals[0], normals[1])
            and equations.same_span(normals[0], normals[2])
        )
        hs = full.project_vector(
            equations.cylinders.matching_tensor(full.SIX, blocks), killed
        )
        hs_in = equations.cylinders.member(
            hs, equations.cylinders.echelon(normals[0])
        )
        records.append((
            name, len(normals[0]), same, hs_in,
            admissible_pairs(normals[0], killed), len(killed),
        ))
    return tuple(records)


def crossratio_geometry():
    retained = (4, 5, 7, 8)
    base_coefficients = {
        full.CELLS[5]: Q(1), full.CELLS[4]: Q(1), full.CELLS[8]: Q(1),
    }
    one_coefficients = dict(base_coefficients)
    one_coefficients[full.CELLS[7]] = Q(1)
    killed = adjacent.quotient_killed(retained, retain_t=True)
    base_blocks = adjacent.blocks_for(base_coefficients, Q(1))
    one_blocks = adjacent.blocks_for(one_coefficients, Q(1))
    normals = tuple(
        full.expanded_projected_cylinder_intersection(
            (2, 3, 4, cut), (base_blocks, one_blocks), killed
        )
        for cut in (0, 1, 5)
    )
    h_base = full.project_vector(
        equations.cylinders.matching_tensor(full.SIX, base_blocks), killed
    )
    h_one = full.project_vector(
        equations.cylinders.matching_tensor(full.SIX, one_blocks), killed
    )
    expected = ({old_symbolic.E_WORD: Q(1)}, h_base)
    direct_plane = equations.same_span(normals[0], expected)
    affine_direct = adjacent.subtract(h_one, h_base) == expected[0]
    locked = True
    for cut in (0, 1, 5):
        at_zero = old_symbolic.raw_projected_cylinder_columns(
            cut, base_blocks, killed
        )
        at_one = old_symbolic.raw_projected_cylinder_columns(
            cut, one_blocks, killed
        )
        for column_zero, column_one in zip(at_zero, at_one):
            delta_e = (
                column_one.get(old_symbolic.E_WORD, Q(0))
                - column_zero.get(old_symbolic.E_WORD, Q(0))
            )
            delta_a = (
                column_one.get(old_symbolic.A_WORD, Q(0))
                - column_zero.get(old_symbolic.A_WORD, Q(0))
            )
            locked &= (
                column_zero.get(old_symbolic.E_WORD, Q(0)) == 0
                and delta_e - column_zero.get(old_symbolic.A_WORD, Q(0)) == 0
                and delta_a == 0
            )
    return (
        tuple(len(normal) for normal in normals),
        equations.same_span(normals[0], normals[1])
        and equations.same_span(normals[0], normals[2]),
        admissible_pairs(normals[0], killed),
        len(killed),
        direct_plane,
        affine_direct,
        locked,
    )


def main():
    for cell in full.CELLS[1:]:
        select_direction(cell)
        x_rows, t_row = torus_rows()
        outside = outside_geometry()
        old = old_geometry()
        print(
            "DIRECTION", cell,
            "torus_ranks", (x_rows.rank(), sp.Matrix.vstack(x_rows, t_row).rank()),
            "t_block", len(adjacent.T_BLOCK),
            "x_overlaps", tuple(
                len(adjacent.T_BLOCK & block) for block in adjacent.X_BLOCKS
            ),
            "uplus_overlap", len(adjacent.T_BLOCK & set(full.UPLUS)),
            "targets", tuple(
                (colour,) * 6 in adjacent.T_BLOCK for colour in full.COLOURS
            ),
        )
        print(" outside", outside)
        print(" old", old)
        print(" crossratio", crossratio_geometry())


if __name__ == "__main__":
    main()

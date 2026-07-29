#!/usr/bin/env python3
"""Exact reconnaissance for the two cross-ratio directions E10, E20 in A25.

The adjacent one-cell frontier on the fixed repaired interior has two
remaining directions, A25 = E00 + t*E10 and A25 = E00 + t*E20.  Unlike the
closed directions, the moving stabilizer character is dependent:
wt(t) = wt(x10) - wt(x00) or wt(t) = wt(x20) - wt(x00), so the fully
nonzero stratum keeps the invariant lambda = t*x00/x10 or t*x00/x20.

This script records, for each direction:

* the exact coupled-mask census: the A23 supports whose character rows
  already contain the moving t-character (no independent t normalization);
* the mixed-term separation audit (edges 23 and 25 share site 2);
* for every one of the 512 A23 supports, sampled unprojected four-cylinder
  intersection dimensions for final cuts 0, 1, 5, whether the intersection
  is exactly the direct-tensor line, and whether any active target word
  lies in the intersection.

It is an exploration helper, not a theorem certificate.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import itertools
import random

import sympy as sp

import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


Q = full.Q
DIRECTIONS = ((1, 0), (2, 0))
CUTS = (0, 1, 5)


def torus_rows(cell):
    fixed = (
        ((0, 1), (0, 0)), ((4, 5), (0, 0)),
        ((0, 2), (1, 1)), ((1, 4), (1, 1)),
        ((0, 4), (2, 2)), ((1, 3), (2, 2)),
        ((2, 5), (0, 0)), ((3, 5), (1, 0)),
    )
    constraints = sp.Matrix.vstack(*(
        adjacent.cell_weight(edge, fixed_cell) for edge, fixed_cell in fixed
    ))
    assert constraints.rank() == 8
    kernel = sp.Matrix.hstack(*constraints.nullspace())
    x_rows = tuple(
        adjacent.cell_weight((2, 3), x_cell) * kernel for x_cell in full.CELLS
    )
    t_row = adjacent.cell_weight((2, 5), cell) * kernel
    return x_rows, t_row


def coupled_census(cell):
    x_rows, t_row = torus_rows(cell)
    # exact dependence relation used in the write-up
    difference = x_rows[full.CELLS.index(cell)] - x_rows[0]
    relation_holds = (t_row - difference).is_zero_matrix
    coupled = []
    for mask in range(1 << 9):
        rows = [x_rows[bit] for bit in range(9) if mask & (1 << bit)]
        x_rank = sp.Matrix.vstack(*rows).rank() if rows else 0
        xt_rank = sp.Matrix.vstack(*(rows + [t_row])).rank()
        if xt_rank == x_rank:
            coupled.append(mask)
    return relation_holds, tuple(coupled)


def sample_record(cell, mask, seed):
    adjacent.T_CELL = cell
    rng = random.Random(f"{cell}-{mask}-{seed}")
    coefficients = {
        full.CELLS[bit]: Q(rng.choice((1, 2, 3, 5, 7, -1, -2, -3)))
        for bit in range(9) if mask & (1 << bit)
    }
    t = Q(rng.choice((1, 2, 3, 5, -1, -2, 4)))
    blocks = adjacent.blocks_for(coefficients, t)
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    record = []
    for cut in CUTS:
        normal = equations.cylinders.cylinder_intersection((2, 3, 4, cut), blocks)
        span = equations.cylinders.echelon(normal)
        assert equations.cylinders.member(hs, span)
        line = equations.same_span(normal, [hs])
        targets = tuple(
            colour for colour in full.COLOURS
            if equations.cylinders.member({(colour,) * 6: Q(1)}, span)
        )
        record.append((cut, len(normal), line, targets))
    return mask, t, tuple(record)


def scan_direction(cell, samples, workers, masks):
    jobs = [(cell, mask, seed) for mask in masks for seed in range(samples)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(_worker, jobs, chunksize=8))
    profiles = {}
    for mask, _t, record in results:
        key = tuple((cut, dimension, line, targets) for cut, dimension, line, targets in record)
        profiles.setdefault(key, set()).add(mask)
    return profiles


def _worker(job):
    cell, mask, seed = job
    return sample_record(cell, mask, seed)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=2)
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--limit", type=int, default=512)
    parser.add_argument("--direction", choices=("10", "20"), action="append")
    args = parser.parse_args()
    wanted = tuple(
        cell for cell in DIRECTIONS
        if not args.direction or f"{cell[0]}{cell[1]}" in args.direction
    )
    for cell in wanted:
        adjacent.T_CELL = cell
        adjacent.T_BLOCK, adjacent.T_DETAILS = adjacent.variable_coordinate_block(
            adjacent.T_EDGE, cell
        )
        adjacent.no_mixed_x_t_terms()
        relation_holds, coupled = coupled_census(cell)
        print(
            "DIRECTION", cell,
            "t_row_equals_xcd_minus_x00", relation_holds,
            "coupled_masks", len(coupled), flush=True,
        )
        both_bits = tuple(
            mask for mask in coupled
            if (mask & 1) and (mask & (1 << full.CELLS.index(cell)))
        )
        print(
            " coupled_all_have_x00_and_xcd",
            len(both_bits) == len(coupled),
            "example", coupled[:4], flush=True,
        )
        profiles = scan_direction(
            cell, args.samples, args.workers, tuple(range(args.limit))
        )
        for key in sorted(profiles, key=lambda item: (-len(profiles[item]),)):
            masks = profiles[key]
            print(
                " PROFILE", key, "count", len(masks),
                "examples", sorted(masks)[:6],
                "x00_in", tuple(sorted({bool(mask & 1) for mask in masks})),
                flush=True,
            )


if __name__ == "__main__":
    main()

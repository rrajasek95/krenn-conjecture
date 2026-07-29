#!/usr/bin/env python3
"""Exact census for all support orbits in the A_23 plane-normal locus.

The eight fixed internal aggregate cells are retained and the block on 23
is supported on

    L = {(0,0), (0,1), (0,2), (1,1), (2,1)}.

The fixed-cell-preserving colour torus makes each zero/nonzero support a
single orbit over C, so coefficients may be normalized to one.  This file
reconstructs every internal matching tensor, the cuts 234z cylinder
intersection, the pure target directions absorbed by that normal, and the
literal two-star cofactor expansion.  It is a discovery/census driver; the
characteristic-zero eliminations live in a separate verifier.
"""

from __future__ import annotations

import argparse
import collections
import itertools

import explore_three_cut_internal_23_perturbation as base


Q = base.Q
SIX = base.SIX
COLOURS = base.COLOURS
CELLS = ((0, 0), (0, 1), (0, 2), (1, 1), (2, 1))
CELL_NAMES = ("x00", "x01", "x02", "x11", "x21")


def support_from_mask(mask: int):
    return tuple(cell for bit, cell in enumerate(CELLS) if mask & (1 << bit))


def support_name(mask: int) -> str:
    names = [name for bit, name in enumerate(CELL_NAMES) if mask & (1 << bit)]
    return "+".join(names) if names else "zero"


def blocks_for_mask(mask: int):
    blocks = base.cylinders.aggregate()
    blocks[(2, 3)] = {cell: Q(1) for cell in support_from_mask(mask)}
    return blocks


def same_span(left, right) -> bool:
    return base.same_span(left, right)


def target_absorption(basis):
    span = base.cylinders.echelon(basis)
    return tuple(
        colour
        for colour in COLOURS
        if base.cylinders.member(
            base.cylinders.unit((colour,) * 6), span
        )
    )


def vector_text(vector):
    def term(item):
        word, coefficient = item
        label = "[" + "".join(map(str, word)) + "]"
        return label if coefficient == 1 else f"{coefficient}*{label}"

    return "+".join(term(item) for item in sorted(vector.items())) or "0"


def census(mask: int):
    blocks = blocks_for_mask(mask)
    hs = base.cylinders.matching_tensor(SIX, blocks)
    normals = {
        z: base.cylinders.cylinder_intersection((2, 3, 4, z), blocks)
        for z in (0, 1, 5)
    }
    words = base.reconstruct_word_terms(blocks)
    return {
        "mask": mask,
        "support": support_name(mask),
        "hs": hs,
        "three_dim": len(base.cylinders.cylinder_intersection((2, 3, 4), blocks)),
        "normals": normals,
        "absorbed": {z: target_absorption(normals[z]) for z in normals},
        "reachable": len(words),
        "atoms": sum(map(len, words.values())),
        "multiplicities": dict(sorted(collections.Counter(map(len, words.values())).items())),
    }


def group_identical_normals(rows):
    groups = []
    for row in rows:
        placed = False
        for representative, members in groups:
            if all(
                same_span(row["normals"][z], representative["normals"][z])
                for z in (0, 1, 5)
            ):
                members.append(row["mask"])
                placed = True
                break
        if not placed:
            groups.append((row, [row["mask"]]))
    return groups


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mask", type=lambda value: int(value, 0))
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    masks = (args.mask,) if args.mask is not None else range(32)
    rows = [census(mask) for mask in masks]
    for row in rows:
        dims = tuple(len(row["normals"][z]) for z in (0, 1, 5))
        absorbed = tuple(row["absorbed"][z] for z in (0, 1, 5))
        print(
            f"{row['mask']:02d} {row['support']:<23} "
            f"H={len(row['hs']):2d} C234={row['three_dim']:2d} "
            f"N015={dims} absorbed={absorbed} "
            f"words={row['reachable']:3d} atoms={row['atoms']:3d}"
        )
        if args.verbose:
            print("  H_S", vector_text(row["hs"]))
            for z in (0, 1, 5):
                print(f"  N{z}")
                for vector in row["normals"][z]:
                    print("   ", vector_text(vector))

    if args.mask is None:
        groups = group_identical_normals(rows)
        print("identical_normal_triples", len(groups))
        for index, (representative, members) in enumerate(groups):
            print(
                "group", index,
                "masks", ",".join(f"{mask:02d}" for mask in members),
                "dims", tuple(len(representative["normals"][z]) for z in (0, 1, 5)),
                "absorbed", tuple(representative["absorbed"][z] for z in (0, 1, 5)),
            )


if __name__ == "__main__":
    main()

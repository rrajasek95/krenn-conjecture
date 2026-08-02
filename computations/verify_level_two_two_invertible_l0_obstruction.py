#!/usr/bin/env python3
"""Exact L0 tangent-incidence obstruction to the 2I+2R+2Z guard."""

from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
guard = run_path(str(HERE / "verify_level_two_two_invertible_r2_guard.py"))
l0_core = run_path(str(
    HERE / "verify_level_two_three_invertible_l0_obstruction.py"
))

core = guard["core"]
M = guard["M"]
RHO = guard["RHO"]
SITES = tuple(range(6))
COLOURS = (0, 1)
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLOURS, repeat=6))


def append_columns(matrix, *columns):
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def ranks_over_three_fields(matrix):
    return (
        core["rational_rank"](matrix),
        core["modular_rank"](matrix, 101),
        core["modular_rank"](matrix, 1_000_003),
    )


def audit_l0_screen():
    # This is the universal 15+90 endpoint matching partition and formal
    # W*Psi+dPsi(N) identity on all four endpoint slices.
    formal_slices = l0_core["audit_matching_partition_and_slice_formula"]()
    require(formal_slices == 256, "formal L0 slice count changed")

    slope = core["matching_tensor"](M)
    require(
        core["apply_differential"](M, M)
        == [3 * value for value in slope],
        "Euler identity failed",
    )

    derivative = core["differential_matrix"](M)
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    mixed = [
        row for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = {
        "D": ranks_over_three_fields(derivative),
        "D_mixed": ranks_over_three_fields(mixed),
        "D|e0": ranks_over_three_fields(
            append_columns(derivative, pure_zero)
        ),
        "D|e1": ranks_over_three_fields(
            append_columns(derivative, pure_one)
        ),
        "D|e0,e1": ranks_over_three_fields(
            append_columns(derivative, pure_zero, pure_one)
        ),
    }
    require(ranks == {
        "D": (55, 55, 55),
        "D_mixed": (55, 55, 55),
        "D|e0": (56, 56, 56),
        "D|e1": (56, 56, 56),
        "D|e0,e1": (57, 57, 57),
    }, ("L0 screen ranks changed", ranks))
    return formal_slices, ranks


def audit_free_block_scope():
    positive = frozenset(
        edge for edge in EDGES
        if RHO[edge[0]] + RHO[edge[1]] != 0
        and edge != (4, 5)
    )
    free = frozenset(
        edge for edge in EDGES
        if RHO[edge[0]] + RHO[edge[1]] == 0
    )
    forced_zero = frozenset(((4, 5),))
    require(positive == frozenset((
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 3), (2, 3),
    )), ("positive-multiplier blocks changed", positive))
    require(free == frozenset((
        (0, 4), (0, 5), (1, 4), (1, 5),
        (2, 4), (2, 5), (3, 4), (3, 5),
    )), ("zero-multiplier free blocks changed", free))
    require(positive | free | forced_zero == frozenset(EDGES),
            "block scope does not partition all residual edges")
    require(4 * len(free) == 32, "free scalar-cell count changed")

    # The exact obstruction fixes all 60 residual cells; the remaining
    # ternary cells lie outside D and cannot alter its image.
    total_ternary = len(tuple(combinations(range(8), 2))) * 9
    residual_binary = len(EDGES) * 4
    require((total_ternary, residual_binary,
             total_ternary - residual_binary) == (252, 60, 192),
            "fixed/outside cell count changed")
    return positive, free, forced_zero


def main():
    formal_slices, ranks = audit_l0_screen()
    positive, free, forced_zero = audit_free_block_scope()
    print(
        "two-invertible L0 obstruction: "
        f"{formal_slices} formal slices; ranks {ranks}; "
        f"determined/free/zero blocks {len(positive)}/{len(free)}/"
        f"{len(forced_zero)}"
    )


if __name__ == "__main__":
    main()

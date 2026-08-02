#!/usr/bin/env python3
"""Exact linear-L0 obstruction to the dense transverse-column guard.

The fixed rank-55/R2 packet from the transverse-column potential boundary
has mixed-row differential rank 55, and neither pure coordinate target lies
in its tangent image.  Hence this exact packet has no full L0 completion.

Standard library only; checks remain live under python -O and python -I -S.
"""

from itertools import combinations
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
guard = run_path(str(
    HERE / "verify_level_two_two_invertible_transverse_column_potential_boundary.py"
))
l0_core = run_path(str(
    HERE / "verify_level_two_three_invertible_l0_obstruction.py"
))

rank_core = guard["rank_core"]
dense_core = guard["dense_core"]
SITES = guard["SITES"]
EDGES = guard["EDGES"]
CELLS = guard["CELLS"]
PACKET = guard["PACKET"]
POTENTIAL = guard["DENSE_POTENTIAL"]
WORDS = rank_core["WORDS"]
PRIMES = (101, 32_003, 1_000_003)


def append_columns(matrix, *columns):
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def ranks_over_fields(matrix):
    return (
        dense_core["rational_rank"](matrix),
        *(rank_core["rank_mod"](matrix, prime) for prime in PRIMES),
    )


def audit_l0_incidence():
    formal_slices = l0_core["audit_matching_partition_and_slice_formula"]()
    require(formal_slices == 256, "formal L0 slice count changed")

    derivative = rank_core["differential"](PACKET)
    slope = [
        rank_core["hafnian"](PACKET, SITES, word)
        for word in WORDS
    ]
    radial = [PACKET[cell] for cell in CELLS]
    require(
        rank_core["matrix_vector_product"](derivative, radial)
        == [3 * value for value in slope],
        "six-site Euler identity failed",
    )

    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    mixed = [
        row
        for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = {
        "D": ranks_over_fields(derivative),
        "D_mixed": ranks_over_fields(mixed),
        "D|e0": ranks_over_fields(
            append_columns(derivative, pure_zero)
        ),
        "D|e1": ranks_over_fields(
            append_columns(derivative, pure_one)
        ),
        "D|e0,e1": ranks_over_fields(
            append_columns(derivative, pure_zero, pure_one)
        ),
    }
    require(ranks == {
        "D": (55, 55, 55, 55),
        "D_mixed": (55, 55, 55, 55),
        "D|e0": (56, 56, 56, 56),
        "D|e1": (56, 56, 56, 56),
        "D|e0,e1": (57, 57, 57, 57),
    }, ("transverse L0 incidence ranks changed", ranks))
    return formal_slices, ranks


def audit_block_scope():
    positive = frozenset(
        pair for pair in EDGES
        if POTENTIAL[pair[0]] + POTENTIAL[pair[1]] != 0
        and pair != (4, 5)
    )
    free = frozenset(
        pair for pair in EDGES
        if POTENTIAL[pair[0]] + POTENTIAL[pair[1]] == 0
    )
    forced_zero = frozenset(((4, 5),))
    require(positive == frozenset(combinations((0, 1, 2, 3), 2)),
            ("positive transverse blocks changed", positive))
    require(free == frozenset((
        (0, 4), (0, 5), (1, 4), (1, 5),
        (2, 4), (2, 5), (3, 4), (3, 5),
    )), ("free transverse blocks changed", free))
    require(positive | free | forced_zero == frozenset(EDGES),
            "transverse block scope does not partition all edges")
    require(4 * len(free) == 32, "free scalar-cell count changed")

    total_ternary = len(tuple(combinations(range(8), 2))) * 9
    residual_binary = len(EDGES) * 4
    require(
        (total_ternary, residual_binary,
         total_ternary - residual_binary) == (252, 60, 192),
        "fixed/outside ternary cell count changed",
    )
    return positive, free, forced_zero


def main():
    normal = guard["audit_covariant_core_normal_form"]()
    generic = guard["audit_dense_generic_kernel"]()
    selected = guard["audit_dense_selected_rows"]()
    differential_ranks = guard["audit_dense_rank"]()
    r2 = guard["audit_dense_r2"]()
    spokes = guard["audit_dense_spokes"]()
    formal_slices, incidence = audit_l0_incidence()
    positive, free, forced = audit_block_scope()
    print("dense transverse-column L0 obstruction: all checks passed")
    print(f"  normalized/generic scalars   : {normal}/{generic}")
    print(f"  selected rows/support        : {selected}")
    print(f"  differential ranks          : {differential_ranks}")
    print(f"  R2 roots/invertible spokes  : {len(r2)}/6, {spokes}")
    print(f"  formal L0 slices            : {formal_slices}")
    print(f"  L0 incidence ranks          : {incidence}")
    print(
        "  determined/free/zero blocks : "
        f"{len(positive)}/{len(free)}/{len(forced)}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact 3I+1R+2Z packet surviving the linear L0 incidence screen.

Research evidence only.  This changes one scalar on the zero-multiplier cut
of the three-invertible R2 guard.  The generic-kernel equation, all selected
level-two rows, differential rank 55, and the literal R2 exits remain exact,
while the mixed-row differential rank drops to 53 and both pure L0 targets
enter its image.
"""

from itertools import product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
guard = run_path(str(
    HERE / "verify_level_two_three_invertible_r2_guard.py"
))
l0 = run_path(str(
    HERE / "verify_level_two_three_invertible_l0_obstruction.py"
))

COLOURS = (0, 1)
WORDS = tuple(product(COLOURS, repeat=6))
CHANGED_CELL = (3, 4, 1, 0)
REPLACEMENT = {
    (3, 4): ((12, 0), (0, 0)),
}

ORIGINAL_BLOCKS = dict(guard["BLOCKS"])
BLOCKS = dict(ORIGINAL_BLOCKS)
BLOCKS.update(REPLACEMENT)
M = guard["packet_from_blocks"](BLOCKS)

# ``run_path`` returns a shallow copy on this Python version, so assignments
# to that returned dictionary do not replace the function-global bindings.
# Substitute the candidate in the actual globals used by the exact audits.
guard_globals = guard["audit_generic_kernel_equation"].__globals__
guard_globals["BLOCKS"] = BLOCKS
guard_globals["M"] = M


def append_columns(matrix, *columns):
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def ranks_over_fields(matrix):
    return (
        guard["rational_rank"](matrix),
        guard["modular_rank"](matrix, 101),
        guard["modular_rank"](matrix, 32_003),
        guard["modular_rank"](matrix, 1_000_003),
    )


def audit_replacement_scope():
    changed_edges = frozenset(
        edge for edge in BLOCKS
        if BLOCKS[edge] != ORIGINAL_BLOCKS[edge]
    )
    require(changed_edges == frozenset(REPLACEMENT),
            ("replacement scope changed", changed_edges))
    changed_cells = frozenset(
        (u, v, a, b)
        for (u, v), block in BLOCKS.items()
        for a, b in product(COLOURS, repeat=2)
        if block[a][b] != ORIGINAL_BLOCKS[u, v][a][b]
    )
    require(changed_cells == frozenset((CHANGED_CELL,)),
            ("more than one scalar changed", changed_cells))
    require(ORIGINAL_BLOCKS[3, 4][1][0] == 2
            and BLOCKS[3, 4][1][0] == 0,
            "the one-scalar specialization changed")
    require(guard["RHO"][3] + guard["RHO"][4] == 0,
            "the changed block no longer has zero multiplier")
    require(BLOCKS[3, 4][0][0] == 12,
            "the root-3 pure-zero R2 exit vanished")
    return changed_cells


def audit_l0_incidence():
    formal_slices = l0["audit_matching_partition_and_slice_formula"]()
    require(formal_slices == 256, "formal L0 slice count changed")

    slope = guard["matching_tensor"](M)
    require(
        guard["apply_differential"](M, M)
        == [3 * value for value in slope],
        "Euler identity failed",
    )

    derivative = guard["differential_matrix"](M)
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    mixed = [
        row for row, word in zip(derivative, WORDS)
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
    expected = {
        "D": (55, 55, 55, 55),
        "D_mixed": (53, 53, 53, 53),
        "D|e0": (55, 55, 55, 55),
        "D|e1": (55, 55, 55, 55),
        "D|e0,e1": (55, 55, 55, 55),
    }
    require(ranks == expected, ("L0 incidence ranks changed", ranks))
    return formal_slices, slope, ranks


def main():
    changed = audit_replacement_scope()
    guard_slope = guard["audit_generic_kernel_equation"]()
    differential_ranks = guard["audit_rank_55"]()
    r2_tables = guard["audit_literal_r2"]()
    formal_slices, slope, incidence_ranks = audit_l0_incidence()
    require(slope == guard_slope, "the two slope computations disagree")
    print(
        "three-invertible L0 incidence survivor: "
        f"{len(changed)} changed zero-multiplier scalar; "
        "60 generic-kernel scalars, 64 selected rows; "
        f"differential ranks {differential_ranks}; "
        f"slope support {sum(value != 0 for value in slope)}/64; "
        f"R2 roots {len(r2_tables)}/6; "
        f"{formal_slices} formal slices; L0 ranks {incidence_ranks}"
    )


if __name__ == "__main__":
    main()

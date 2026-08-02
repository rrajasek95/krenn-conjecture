#!/usr/bin/env python3
"""Exact 2I+2R+2Z packet surviving the linear L0 incidence screen."""

from itertools import product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
guard = run_path(str(HERE / "verify_level_two_two_invertible_r2_guard.py"))
l0 = run_path(str(
    HERE / "verify_level_two_three_invertible_l0_obstruction.py"
))

core = guard["core"]
COLOURS = (0, 1)
WORDS = tuple(product(COLOURS, repeat=6))
FREE_EDGES = frozenset((
    (0, 4), (0, 5), (1, 4), (1, 5),
    (2, 4), (2, 5), (3, 4), (3, 5),
))
REPLACEMENT = {
    (0, 4): ((0, 85), (0, 87)),
    (0, 5): ((84, 87), (0, 28)),
    (1, 4): ((0, 74), (0, 66)),
    (1, 5): ((0, 76), (37, 0)),
    (2, 4): ((0, 46), (0, 23)),
    (2, 5): ((56, 0), (0, 0)),
    (3, 4): ((0, 3), (29, 0)),
    (3, 5): ((0, 51), (0, 96)),
}

ORIGINAL_BLOCKS = dict(guard["BLOCKS"])
BLOCKS = dict(ORIGINAL_BLOCKS)
BLOCKS.update(REPLACEMENT)
M = guard["packet_from_blocks"](BLOCKS)

# ``run_path`` returns a shallow copy on this Python version, so assigning
# through the returned dictionary does not replace the function-global
# bindings.  Substitute the candidate in the actual globals shared by the
# imported audits, leaving their independent assertions unchanged.
AUDIT_NAMES = (
    "audit_generic_kernel_and_selected_rows",
    "audit_rank_and_kernel",
    "audit_r2",
)
guard_globals = guard[AUDIT_NAMES[0]].__globals__
require(all(
    guard[name].__globals__ is guard_globals for name in AUDIT_NAMES
), "the imported guard audits no longer share globals")
guard_globals["BLOCKS"] = BLOCKS
guard_globals["M"] = M


def append_columns(matrix, *columns):
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def ranks_over_fields(matrix):
    return (
        core["rational_rank"](matrix),
        core["modular_rank"](matrix, 101),
        core["modular_rank"](matrix, 32_003),
        core["modular_rank"](matrix, 1_000_003),
    )


def audit_replacement_scope():
    require(guard_globals["BLOCKS"] is BLOCKS
            and guard_globals["M"] is M,
            "the imported guard audits are not using the replacement")
    require(frozenset(REPLACEMENT) == FREE_EDGES,
            "replacement does not cover the eight free blocks")
    changed = frozenset(
        edge for edge in BLOCKS
        if BLOCKS[edge] != ORIGINAL_BLOCKS[edge]
    )
    require(changed == FREE_EDGES,
            ("a determined block changed", changed))
    require(all(
        guard["RHO"][u] + guard["RHO"][v] == 0
        for u, v in FREE_EDGES
    ), "a replacement block has nonzero multiplier")
    return changed


def audit_l0_incidence():
    formal_slices = l0["audit_matching_partition_and_slice_formula"]()
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
        "D_mixed": (53, 53, 53, 53),
        "D|e0": (55, 55, 55, 55),
        "D|e1": (55, 55, 55, 55),
        "D|e0,e1": (55, 55, 55, 55),
    }, ("L0 incidence ranks changed", ranks))
    return formal_slices, ranks


def main():
    changed = audit_replacement_scope()
    checked, slope = guard["audit_generic_kernel_and_selected_rows"]()
    differential_ranks = guard["audit_rank_and_kernel"]()
    r2_tables = guard["audit_r2"]()
    formal_slices, incidence_ranks = audit_l0_incidence()
    print(
        "two-invertible L0 incidence survivor: "
        f"{len(changed)} free blocks; "
        f"{checked} generic-kernel scalars, 64 selected rows; "
        f"differential ranks {differential_ranks}; "
        f"slope support {sum(value != 0 for value in slope)}/64; "
        f"R2 roots {len(r2_tables)}/6; "
        f"{formal_slices} formal slices; L0 ranks {incidence_ranks}"
    )


if __name__ == "__main__":
    main()

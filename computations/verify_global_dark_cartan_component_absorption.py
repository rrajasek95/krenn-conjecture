#!/usr/bin/env python3
"""Verify the global bright-component or dark-kernel alternative.

The complete physical Cartan column must not be projected to a partial
source row.  Instead decompose the complete literal presentation into its
source-connected components.  On each corank-one zero-holonomy block, a
nonzero left charge gives the Schur-unit branch; if every charge is dark,
the component potentials assemble.  Exhaustivity makes their complete
residual zero, hence gives one genuine unit-coefficient kernel class.
An incomplete component inventory leaves an explicit complementary residual,
which is the typed-exit branch under fine-label saturation.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_oo_zero_holonomy_schur_interference_reduction.py":
        "1e96bf98e997e55d2b050de6c56e7f597cd507737aefa6386296c44adab03631",
    "computations/verify_uniform_cartan_critical_component_placement_gate.py":
        "68c56c1a9144dd92fa803962697de60b78b58a125191450f1af1abcd1befe2a1",
    "computations/verify_uniform_physical_bar_occurrence_splitter_cokernel.py":
        "403819751753802f4bb01b07cca2540fc6abf0479b9be5569ee74f414ea667ad",
    "computations/verify_dark_cartan_terminal_safe_cancellation.py":
        "124963d21d779920322fcfc3d238351ce204093cc2587d1bba199ebc85b650d4",
    "computations/verify_oo_dark_R_physical_generator_annihilator.py":
        "e4e1da1b1784f3c86d085965d9a556b17e4695c026daab8b109bcc4549c04abf",
}
EXPECTED_LEDGER_SHA256 = "60547efc8b6d06b2bea0d55932fbe85e6227b99e16b138de43c8a02b4ee87880"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix, strict=True))


def mat_vec(matrix, vector):
    return tuple(sum(Q(a) * Q(b) for a, b in
                     zip(row, vector, strict=True)) for row in matrix)


def rref(matrix):
    work = [list(map(Q, row)) for row in matrix]
    if not work:
        return (), ()
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    pivots = []
    for column in range(columns):
        found = next((row for row in range(pivot_row, rows)
                      if work[row][column]), None)
        if found is None:
            continue
        work[pivot_row], work[found] = work[found], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [entry / pivot for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [a - factor * b
                         for a, b in zip(work[row], work[pivot_row],
                                         strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    columns = len(matrix[0]) if matrix else 0
    free = [column for column in range(columns) if column not in pivots]
    answer = []
    for free_column in free:
        vector = [Q(0)] * columns
        vector[free_column] = Q(1)
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[row][free_column]
        answer.append(tuple(vector))
    return tuple(answer)


def left_nullspace(matrix):
    return nullspace(transpose(matrix))


def block_diag(blocks):
    total_rows = sum(len(block) for block in blocks)
    total_columns = sum(len(block[0]) for block in blocks)
    result = [[Q(0)] * total_columns for _ in range(total_rows)]
    row_offset = 0
    column_offset = 0
    for block in blocks:
        for row, values in enumerate(block):
            for column, value in enumerate(values):
                result[row_offset + row][column_offset + column] = Q(value)
        row_offset += len(block)
        column_offset += len(block[0])
    return tuple(tuple(row) for row in result)


def combine(block, y):
    return mat_vec(block, y)


def audit_packet(blocks, local_g, outside=()):
    """Classify a block-diagonal component packet.

    Each block has corank one.  ``local_g`` supplies the complete Cartan
    projection to that block.  ``outside`` is the complementary literal
    residual not yet assigned to a saturated component.
    """
    require(len(blocks) == len(local_g), "component count changed")
    dark = []
    bright = []
    potentials = []
    for index, (block, g) in enumerate(zip(blocks, local_g, strict=True)):
        require(len(block) == len(block[0]), "critical block is not square")
        require(rank(block) == len(block) - 1,
                "critical block stopped being corank one")
        left = left_nullspace(block)
        right = nullspace(block)
        require(len(left) == len(right) == 1,
                "critical charges stopped being one-dimensional")
        charge = sum(Q(a) * Q(b)
                     for a, b in zip(left[0], g, strict=True))
        if charge:
            bright.append({"component": index, "charge": str(charge)})
            potentials.append(None)
            continue
        dark.append(index)
        # Solve block*y=g by RREF of the augmented matrix.  Since the left
        # charge vanishes, consistency is guaranteed.
        augmented = tuple(tuple(map(Q, row)) + (Q(value),)
                          for row, value in zip(block, g, strict=True))
        reduced, pivots = rref(augmented)
        require(len(block) not in pivots, "dark component became inconsistent")
        variables = len(block[0])
        y = [Q(0)] * variables
        for row, pivot in enumerate(pivots):
            if pivot < variables:
                y[pivot] = reduced[row][-1]
        require(combine(block, y) == tuple(map(Q, g)),
                "component potential failed")
        potentials.append(tuple(y))

    complete_block = block_diag(blocks)
    complete_g = tuple(Q(value) for g in local_g for value in g) + tuple(
        map(Q, outside))
    global_y = tuple(value for y in potentials if y is not None for value in y)

    if bright:
        return {
            "outcome": "bright_component",
            "bright": bright,
            "dark_components": dark,
            "outside_residual": list(map(str, outside)),
        }

    require(len(global_y) == len(complete_block[0]),
            "global potential lost a component")
    absorbed = mat_vec(complete_block, global_y)
    residual = tuple(a - b for a, b in
                     zip(complete_g[:len(absorbed)], absorbed, strict=True))
    require(not any(residual), "dark component potentials did not assemble")
    if outside:
        require(any(outside), "outside residual was vacuous")
        return {
            "outcome": "typed_exit",
            "bright": [],
            "dark_components": dark,
            "outside_residual": list(map(str, outside)),
        }

    # Add the complete Cartan column and verify the assembled unit kernel.
    matrix_with_g = tuple(row + (complete_g[row_index],)
                          for row_index, row in enumerate(complete_block))
    kernel_vector = tuple(-value for value in global_y) + (Q(1),)
    require(mat_vec(matrix_with_g, kernel_vector)
            == (Q(0),) * len(matrix_with_g),
            "assembled dark class was not a complete kernel")
    require(rank(matrix_with_g) == rank(complete_block),
            "dark Cartan column changed the complete image")
    return {
        "outcome": "global_unit_kernel",
        "bright": [],
        "dark_components": dark,
        "outside_residual": [],
        "global_potential": list(map(str, global_y)),
        "kernel_vector": list(map(str, kernel_vector)),
        "rank_before": rank(complete_block),
        "rank_after": rank(matrix_with_g),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    # Two weighted zero-holonomy components.  Each is a rank-one 2-cycle.
    blocks = (
        ((1, -1), (2, -2)),
        ((1, -2), (3, -6)),
    )
    dark_packet = audit_packet(
        blocks,
        local_g=((3, 6), (5, 15)),
    )
    require(dark_packet["outcome"] == "global_unit_kernel",
            "all-dark packet stopped assembling")

    bright_packet = audit_packet(
        blocks,
        local_g=((3, 6), (5, 14)),
    )
    require(bright_packet["outcome"] == "bright_component"
            and bright_packet["bright"][0]["component"] == 1,
            "bright component stopped being detected")

    exit_packet = audit_packet(
        blocks,
        local_g=((3, 6), (5, 15)),
        outside=(0, 7, 0),
    )
    require(exit_packet["outcome"] == "typed_exit",
            "complementary residual stopped being an exit")

    # Exhaust small two-component weighted cycles.  This mutation guard
    # verifies that the three outcomes are exhaustive once the component
    # projections and complement are fixed.
    blocks_seen = 0
    outcome_counts = {
        "bright_component": 0,
        "global_unit_kernel": 0,
        "typed_exit": 0,
    }
    # Use projectively distinct weighted two-cycles.  The exhaustive guard is
    # deliberately small enough to run in every interpreter mode; the proof
    # above is dimension-free linear algebra, while these packets catch sign,
    # assembly, and complement-routing regressions.
    candidate_blocks = [
        ((1, -1), (1, -1)),
        ((1, -1), (-2, 2)),
        ((1, 1), (2, 2)),
        ((1, 2), (-1, -2)),
        ((2, 1), (2, 1)),
        ((1, -2), (2, -4)),
        ((2, -1), (-2, 1)),
        ((2, 3), (4, 6)),
    ]
    for left in candidate_blocks:
        for right in candidate_blocks:
            for g_flat in product((-1, 0, 1), repeat=4):
                g = (g_flat[:2], g_flat[2:])
                for outside_flag in (False, True):
                    outside = (1,) if outside_flag else ()
                    record = audit_packet((left, right), g, outside)
                    outcome_counts[record["outcome"]] += 1
                    blocks_seen += 1

    ledger = {
        "pins": PINS,
        "theorem": (
            "decompose the complete fine-label-saturated source incidence "
            "presentation into connected critical blocks.  If any Cartan "
            "projection has nonzero left charge in an anchor-critical block, "
            "its Schur block is bright. "
            "If all projections are dark, their component potentials "
            "assemble without projecting the physical Cartan row.  A "
            "nonzero complement is a typed exit; an exhaustive inventory "
            "gives one unit-coefficient kernel class of the complete map"
        ),
        "dark_example": dark_packet,
        "bright_example": bright_packet,
        "exit_example": exit_packet,
        "small_packets_checked": blocks_seen,
        "small_outcomes": outcome_counts,
        "proof_consequence": (
            "an occurrence-local physical component projector is not needed "
            "for the Schur/dark alternative.  Component projections are "
            "used only analytically.  The complete Cartan chain remains "
            "intact; either one connected block is bright, a new literal "
            "label enlarges the inventory, or all dark potentials produce "
            "a genuine global correction-kernel class"
        ),
        "scope": (
            "the incidence decomposition must be exhaustive and block "
            "diagonal after every column touching two blocks joins them. "
            "Every block called bright must also carry the nonzero pure-anchor "
            "charge required by the Schur minor.  The theorem does not prove "
            "that arbitrary source components admit such an anchor-critical "
            "corank-one cover, construct the physical terminal on the global "
            "kernel, or land a typed exit at four-good rank"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("global dark Cartan component absorption: PASS")
    print("small packets:", ledger["small_packets_checked"])
    print("outcomes:", ledger["small_outcomes"])
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()

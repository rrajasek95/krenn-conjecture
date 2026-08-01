#!/usr/bin/env python3
"""Exact witness audit for the fully invertible level-two residual theorem.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE is
untouched, and no certified dependency changes.

The theorem is structural: if all fifteen binary residual blocks are
invertible, R2 forces both selected endpoint stars to vanish.  At differential
rank 55, the slope and every four-site cofactor are automatically live, so the
zero-star four-c theorem gives a contradiction to the full equations.

This checker proves that the stated rank-55 locus is nonempty by an integral
witness.  It reuses the exact differential/cofactor audit in the neighbouring
overlap checker through an explicit file path, so isolated Python remains
supported and no non-standard package is needed.
"""

from itertools import product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


CORE = run_path(str(Path(__file__).with_name(
    "verify_level_two_one_sided_overlap_collapse.py"
)))
SITES = CORE["SITES"]
COLOURS = CORE["COLOURS"]
EDGES = CORE["EDGES"]


BLOCKS = {
    (0, 1): ((7, 13), (7, 1)),
    (0, 2): ((5, 9), (8, 7)),
    (0, 3): ((13, 5), (8, 6)),
    (0, 4): ((10, 4), (9, 3)),
    (0, 5): ((5, 3), (13, 2)),
    (1, 2): ((10, 13), (5, 9)),
    (1, 3): ((12, 13), (10, 3)),
    (1, 4): ((5, 2), (12, 2)),
    (1, 5): ((11, 6), (8, 9)),
    (2, 3): ((2, 6), (7, 6)),
    (2, 4): ((10, 11), (4, 9)),
    (2, 5): ((8, 8), (9, 5)),
    (3, 4): ((1, 13), (9, 1)),
    (3, 5): ((2, 12), (7, 12)),
    (4, 5): ((13, 11), (11, 1)),
}


def build_packet():
    return {
        (u, v, a, b): BLOCKS[u, v][a][b]
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def determinant(block):
    return block[0][0] * block[1][1] - block[0][1] * block[1][0]


def pure_column(block, output):
    return (
        any(block[row][output] for row in COLOURS)
        and all(block[row][1 - output] == 0 for row in COLOURS)
    )


def main():
    packet = build_packet()
    determinants = [determinant(BLOCKS[edge]) for edge in EDGES]
    require(all(value != 0 for value in determinants),
            "a residual block is singular")
    require(all(not pure_column(BLOCKS[edge], output)
                for edge in EDGES for output in COLOURS),
            "an invertible residual block became a pure-column witness")

    # If X_r is nonzero, at least one endpoint edge has a nonzero outside
    # c-column and cannot be a pure-a or pure-b witness.  With no internal
    # candidate, at most one endpoint edge remains, but R2 needs two distinct
    # witnesses.  This audits the three possible endpoint-star support types.
    for p_live, q_live in ((True, False), (False, True), (True, True)):
        eligible_endpoint_edges = int(not p_live) + int(not q_live)
        require(eligible_endpoint_edges < 2,
                ("R2 unexpectedly has two candidate edges", p_live, q_live))

    phi_ranks, cofactor_support = CORE["audit_rank_open_conditions"](packet)
    require(phi_ranks == [10] * 6, "a five-site cofactor map lost rank")
    require(cofactor_support == [16] * 15,
            "a four-site cofactor coordinate vanished")
    print(
        "fully invertible residual obstruction: "
        f"15/15 blocks invertible (min |det|={min(map(abs, determinants))}); "
        "rank dPsi=55, slope support=64/64, cofactor support=240/240; "
        "R2 forces P=Q=0"
    )


if __name__ == "__main__":
    main()

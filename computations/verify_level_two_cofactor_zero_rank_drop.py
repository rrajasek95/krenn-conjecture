#!/usr/bin/env python3
"""Exact sharp audit for the four-site-cofactor-zero rank drop.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE is
untouched, and no certified dependency changes.

If the four-site cofactor complementary to an edge uv vanishes identically,
all four uv cell directions lie in ker dPsi.  A connected nonbipartite live
graph after deleting u makes those directions transverse to the five
trace-zero vertex gauges, so rank(dPsi)<=51.

The integral witness below has exactly one zero cofactor tensor and exact rank
51.  Standard library only; checks remain live under python -O and
python -I -S.
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
WORDS = CORE["WORDS"]
CELLS = CORE["CELLS"]
CELL_INDEX = {cell: index for index, cell in enumerate(CELLS)}
DEAD_EDGE = (0, 1)


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
    (2, 3): ((2, 3), (4, 6)),
    (2, 4): ((3, 5), (6, 10)),
    (2, 5): ((5, 7), (10, 14)),
    (3, 4): ((-12, -20), (-18, -30)),
    (3, 5): ((10, 14), (15, 21)),
    (4, 5): ((15, 21), (25, 35)),
}


def build_packet():
    return {
        (u, v, a, b): BLOCKS[u, v][a][b]
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def matrix_vector_product(matrix, vector):
    return [sum(entry * coefficient
                for entry, coefficient in zip(row, vector))
            for row in matrix]


def cofactor_values(packet, edge):
    complement = tuple(x for x in SITES if x not in edge)
    values = []
    for local_word in product(COLOURS, repeat=4):
        word = [0] * 6
        for x, value in zip(complement, local_word):
            word[x] = value
        values.append(CORE["hafnian"](packet, complement, word))
    return values


def edge_cell_vectors(edge):
    vectors = []
    for a, b in product(COLOURS, repeat=2):
        vector = [0] * 60
        vector[CELL_INDEX[edge + (a, b)]] = 1
        vectors.append(vector)
    return vectors


def main():
    packet = build_packet()
    derivative = CORE["differential"](packet)
    gauges = CORE["gauge_vectors"](packet)
    edge_directions = edge_cell_vectors(DEAD_EDGE)

    zero_cofactors = [
        edge for edge in EDGES
        if not any(cofactor_values(packet, edge))
    ]
    require(zero_cofactors == [DEAD_EDGE],
            ("wrong zero-cofactor set", zero_cofactors))

    require(all(matrix_vector_product(derivative, vector) == [0] * 64
                for vector in edge_directions),
            "a dead-edge cell direction left the differential kernel")
    require(all(matrix_vector_product(derivative, vector) == [0] * 64
                for vector in gauges),
            "a vertex gauge left the differential kernel")

    combined_kernel = gauges + edge_directions
    require(CORE["rank_mod"](combined_kernel, 101) == 9,
            "the gauge and edge-block kernels are not transverse")
    require(CORE["rank_mod"](combined_kernel, 1_000_003) == 9,
            "kernel transversality failed at the second prime")

    ranks = (
        CORE["rank_mod"](derivative, 101),
        CORE["rank_mod"](derivative, 1_000_003),
    )
    require(ranks == (51, 51), ("rank-51 calibration failed", ranks))

    deletion = tuple(x for x in SITES if x != DEAD_EDGE[0])
    live_deletion_edges = [
        (u, v) for u, v in EDGES
        if u in deletion and v in deletion
        and any(packet[u, v, a, b] for a, b in product(COLOURS, repeat=2))
    ]
    require(len(live_deletion_edges) == 10,
            "the endpoint deletion live graph is not K5")

    # The complementary four-site packet is a vertex-factor packet whose
    # three scalar matching weights are 1, 1, and -2.
    require(all(value == 0 for value in cofactor_values(packet, DEAD_EDGE)),
            "the advertised scalar Pluecker cancellation failed")
    print(
        "cofactor-zero rank drop: one zero tensor, K5 endpoint deletion, "
        "5 gauge + 4 edge-cell kernels independent; "
        "rank dPsi<=51 and exact calibration rank=51"
    )


if __name__ == "__main__":
    main()

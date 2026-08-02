#!/usr/bin/env python3
"""Rebind the exact linear-L0 survivor to the 1I+5Z zero-potential chart.

The all-zero-potential 1I+5Z generic-kernel component permits arbitrary
residual M.  Use the committed 2I+2R+2Z incidence-survivor packet as M, but
replace its selected endpoint data by X_0=I and X_1=...=X_5=0.  The packet
has differential rank 55, both pure targets in its differential image,
and literal selected residual R2 at all roots.

This is only a linear-incidence survivor.  The same residual M is already
known to fail a factored pure-zero cut.  Standard library only; checks stay
live under -O and -I -S.
"""

from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
SURVIVOR = run_path(str(
    HERE / "verify_level_two_two_invertible_l0_incidence_survivor.py"
))
L0 = run_path(str(
    HERE / "verify_level_two_three_invertible_l0_obstruction.py"
))

SITES = tuple(range(6))
ENDPOINTS = (6, 7)
COLOURS = (0, 1)
RARE = 2
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLOURS, repeat=6))
M = SURVIVOR["M"]
BLOCKS = SURVIVOR["BLOCKS"]
CORE = SURVIVOR["core"]
X = {
    site: ((1, 0), (0, 1)) if site == 0 else ((0, 0), (0, 0))
    for site in SITES
}
POTENTIALS = (0,) * 6


def append_columns(matrix, *columns):
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def ranks_over_fields(matrix):
    return (
        CORE["rational_rank"](matrix),
        CORE["modular_rank"](matrix, 101),
        CORE["modular_rank"](matrix, 32_003),
        CORE["modular_rank"](matrix, 1_000_003),
    )


def audit_one_invertible_selected_block():
    ranks = tuple(CORE["matrix_rank"](X[site]) for site in SITES)
    require(ranks == (2, 0, 0, 0, 0, 0),
            ("one-invertible endpoint ranks changed", ranks))

    checked = 0
    for u, v in EDGES:
        numerator = CORE["matrix_product"](
            CORE["matrix_product"](X[u], ((0, 1), (1, 0))),
            CORE["transpose"](X[v]),
        )
        for a, b in product(COLOURS, repeat=2):
            require(
                numerator[a][b]
                == (POTENTIALS[u] + POTENTIALS[v]) * M[u, v, a, b],
                ("one-invertible generic-kernel identity failed",
                 u, v, a, b),
            )
            checked += 1
    require(checked == 60, "generic-kernel scalar census changed")

    # With only X_0 nonzero, the selected tangent and direct value both
    # vanish.  Hence all 64 selected rows are literally zero.
    selected_tangent = {
        (u, v, a, b): (
            X[u][a][0] * X[v][b][1]
            + X[u][a][1] * X[v][b][0]
        )
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }
    require(not any(selected_tangent.values()),
            "one-invertible selected tangent is nonzero")
    require(-sum(POTENTIALS) == 0,
            "one-invertible direct selected value is nonzero")
    require(CORE["apply_differential"](M, selected_tangent) == [0] * 64,
            "a one-invertible selected row survived")
    return ranks, checked


def audit_rank_and_linear_l0():
    # Rebind the exact 15+90 endpoint-slice identity to this residual M.
    names = (
        "literal_slice_counter",
        "derived_slice_counter",
        "audit_matching_partition_and_slice_formula",
    )
    globals_dict = L0[names[0]].__globals__
    require(all(L0[name].__globals__ is globals_dict for name in names),
            "the imported L0 functions no longer share globals")
    globals_dict["M"] = M
    require(L0["audit_matching_partition_and_slice_formula"]() == 256,
            "formal endpoint-slice census changed")

    derivative = CORE["differential_matrix"](M)
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    mixed = [
        row for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = {
        "D": ranks_over_fields(derivative),
        "D_mixed": ranks_over_fields(mixed),
        "D|e0": ranks_over_fields(append_columns(derivative, pure_zero)),
        "D|e1": ranks_over_fields(append_columns(derivative, pure_one)),
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
    }, ("one-invertible L0 incidence ranks changed", ranks))

    slope = CORE["matching_tensor"](M)
    require(
        CORE["apply_differential"](M, M)
        == [3 * value for value in slope],
        "Euler identity failed on the rebound survivor",
    )
    return derivative, ranks


def oriented_value(packet, root, neighbour, root_colour, neighbour_colour):
    if root < neighbour:
        return packet.get((root, neighbour, root_colour, neighbour_colour), 0)
    return packet.get((neighbour, root, neighbour_colour, root_colour), 0)


def pure_column(packet, root, neighbour, output):
    return (
        any(oriented_value(packet, root, neighbour, row, output)
            for row in COLOURS)
        and all(
            oriented_value(packet, root, neighbour, row, column) == 0
            for row in COLOURS
            for column in (0, 1, 2)
            if column != output
        )
    )


def build_selected_eight_packet():
    packet = dict(M)
    for site in SITES:
        for colour in COLOURS:
            packet[site, ENDPOINTS[0], colour, RARE] = X[site][colour][0]
            packet[site, ENDPOINTS[1], colour, RARE] = X[site][colour][1]
    packet[ENDPOINTS[0], ENDPOINTS[1], RARE, RARE] = 0
    return packet


def audit_selected_residual_r2():
    packet = build_selected_eight_packet()
    tables = {}
    for root in SITES:
        preserves = all(
            oriented_value(packet, root, neighbour, row, RARE) == 0
            for neighbour in range(8)
            if neighbour != root
            for row in COLOURS
        )
        pure = {
            output: tuple(
                neighbour
                for neighbour in range(8)
                if neighbour != root
                and pure_column(packet, root, neighbour, output)
            )
            for output in COLOURS
        }
        if root == 0:
            require(not preserves, "the invertible root unexpectedly preserves")
            require(2 in pure[0] and 4 in pure[1],
                    ("root-zero witnesses changed", pure))
            require(2 != 4, "root-zero R2 witnesses coincide")
        else:
            require(preserves, ("a zero endpoint root does not preserve", root))
        tables[root] = (preserves, pure)

    # The two advertised internal witnesses have active complementary
    # four-site cofactors in this exact residual packet.
    for neighbour in (2, 4):
        complement = tuple(
            site for site in SITES if site not in (0, neighbour)
        )
        require(any(
            CORE["hafnian"](M, complement, word) != 0 for word in WORDS
        ), ("an advertised R2 witness has zero cofactor", neighbour))
    return tables


def audit_factored_obstruction_identity():
    # The committed factored-L0 theorem is literally about this same M.
    replacement = {
        pair: tuple(tuple(BLOCKS[pair][a][b] for b in COLOURS)
                    for a in COLOURS)
        for pair in SURVIVOR["FREE_EDGES"]
    }
    require(replacement == SURVIVOR["REPLACEMENT"],
            "the rebound residual packet is not the factored-cut packet")
    return len(replacement)


def main():
    endpoint_ranks, generic = audit_one_invertible_selected_block()
    _derivative, incidence = audit_rank_and_linear_l0()
    r2 = audit_selected_residual_r2()
    replacement_blocks = audit_factored_obstruction_identity()
    print("one-invertible five-zero L0 incidence survivor: all checks passed")
    print(f"  endpoint ranks                : {endpoint_ranks}")
    print(f"  generic-kernel scalars        : {generic}/60")
    print("  selected level-two rows       : 64/64")
    print(f"  selected residual R2 roots    : {len(r2)}/6")
    print(f"  linear-L0 incidence ranks     : {incidence}")
    print(f"  rebound free blocks           : {replacement_blocks}/8")
    print("  scope                          : linear survivor; factored cut fails")


if __name__ == "__main__":
    main()

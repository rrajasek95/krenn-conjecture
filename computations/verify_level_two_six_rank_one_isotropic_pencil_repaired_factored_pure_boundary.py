#!/usr/bin/env python3
"""Rank-55 factored-pure/R2 guards through the full 6R isotropic pencil.

Starting from SHARP_M, replace blocks 04 and 15 by E10.  The change leaves
the two localized factored pure tangents exact and preserves differential
rank 55/53, while giving roots 4 and 5 their missing pure-one residual R2
witnesses.  Any subset of the six selected sites may then carry rank-one
matrices on the common isotropic input line e_0.  Standard library only;
live under -O and -I -S.
"""

from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
BOUNDARY = run_path(str(
    HERE
    / "verify_level_two_one_invertible_five_zero_factored_pure_slice_survivor.py"
))
SHARP = BOUNDARY["SHARP"]
SITES = BOUNDARY["SITES"]
COLOURS = BOUNDARY["COLOURS"]
EDGES = BOUNDARY["EDGES"]
WORDS = BOUNDARY["WORDS"]
CELLS = BOUNDARY["CELLS"]
ZERO_MATRIX = ((0, 0), (0, 0))
E10 = ((0, 0), (1, 0))
POTENTIALS = (0,) * len(SITES)
OUTPUT_FACTORS = {
    0: (1, 2),
    1: (2, 3),
    2: (3, 5),
    3: (5, 7),
    4: (7, 11),
    5: (11, 13),
}
WITNESSES = {
    0: {0: 3, 1: 2},
    1: {0: 2, 1: 3},
    2: {0: 3, 1: 0},
    3: {0: 2, 1: 1},
    4: {0: 5, 1: 0},
    5: {0: 4, 1: 1},
}


def repaired_packet():
    packet = dict(BOUNDARY["M"])
    for edge in ((0, 4), (1, 5)):
        for a, b in product(COLOURS, repeat=2):
            packet[edge + (a, b)] = E10[a][b]
    return packet


M = repaired_packet()


def selected_family(active):
    selected = {site: ZERO_MATRIX for site in SITES}
    for site in active:
        h0, h1 = OUTPUT_FACTORS[site]
        selected[site] = ((h0, 0), (h1, 0))
    return selected


def ranks_over_fields(matrix):
    return (
        SHARP["rational_rank"](matrix),
        SHARP["modular_rank"](matrix, 101),
        SHARP["modular_rank"](matrix, 32_003),
        SHARP["modular_rank"](matrix, 1_000_003),
    )


def append_columns(matrix, *columns):
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def audit_residual_rank_and_pure_incidence():
    changed = tuple(
        cell for cell in CELLS if M[cell] != BOUNDARY["M"][cell]
    )
    require(len(changed) == 8 and {cell[:2] for cell in changed} == {(0, 4), (1, 5)},
            ("the repaired-cell support changed", changed))
    derivative = SHARP["differential_matrix"](M)
    mixed = [
        row for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
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
    }, ("the repaired residual ranks changed", ranks))
    return derivative, ranks, changed


def audit_selected_equations(selected):
    tangent = {}
    checks = 0
    for u, v in EDGES:
        for a, b in product(COLOURS, repeat=2):
            numerator = sum(
                selected[u][a][i] * selected[v][b][1 - i]
                for i in COLOURS
            )
            require(
                numerator
                == (POTENTIALS[u] + POTENTIALS[v]) * M[u, v, a, b],
                ("repaired isotropic generic-kernel identity failed", u, v, a, b),
            )
            tangent[u, v, a, b] = numerator
            checks += 1
    require(checks == 60, "repaired isotropic scalar census changed")
    require(SHARP["apply_differential"](M, tangent) == [0] * 64,
            "a repaired isotropic selected row survived")
    return checks


def with_packet_and_selected(packet, selected, function, *args):
    globals_dict = function.__globals__
    old_m = globals_dict["M"]
    old_x = globals_dict["X"]
    try:
        globals_dict["M"] = packet
        globals_dict["X"] = selected
        return function(*args)
    finally:
        globals_dict["M"] = old_m
        globals_dict["X"] = old_x


def audit_factored_faces():
    selected = selected_family(SITES)
    zero = with_packet_and_selected(
        M, selected, BOUNDARY["audit_factored_three_slice_completion"], 0
    )
    one = with_packet_and_selected(
        M, selected, BOUNDARY["audit_factored_three_slice_completion"], 1
    )
    require(zero == (256, (0, 1, 0, 0))
            and one == (256, (4, 5, 1, 1)),
            ("the repaired factored faces changed", zero, one))
    return zero, one


def audit_literal_selected_slice(selected):
    u_star, v_star, direct = BOUNDARY["endpoint_stars"](0)
    function = BOUNDARY["eight_site_value"]
    globals_dict = function.__globals__
    old_m = globals_dict["M"]
    old_x = globals_dict["X"]
    try:
        globals_dict["M"] = M
        globals_dict["X"] = selected
        values = [
            function(u_star, v_star, direct, word + (BOUNDARY["RARE"],) * 2)
            for word in WORDS
        ]
    finally:
        globals_dict["M"] = old_m
        globals_dict["X"] = old_x
    require(values == [0] * 64,
            "a repaired isotropic literal selected slice survived")
    return len(values)


def audit_r2_witnesses():
    table = {}
    for root in SITES:
        pure = {}
        for output, neighbour in WITNESSES[root].items():
            require(BOUNDARY["pure_column"](M, root, neighbour, output),
                    ("a repaired pure witness vanished", root, output, neighbour))
            complement = tuple(
                site for site in SITES if site not in (root, neighbour)
            )
            nonzero = sum(
                SHARP["hafnian"](M, complement, word) != 0
                for word in WORDS
            )
            require(nonzero,
                    ("a repaired R2 cofactor vanished", root, output, neighbour))
            pure[output] = (neighbour, nonzero)
        require(pure[0][0] != pure[1][0],
                ("the repaired witnesses collided", root, pure))
        table[root] = pure
    return table


def main():
    _derivative, ranks, changed = audit_residual_rank_and_pure_incidence()
    faces = audit_factored_faces()
    witnesses = audit_r2_witnesses()
    counts = {size: 0 for size in range(7)}
    selected_checks = 0
    literal_checks = 0
    calibrations = {}
    for size in range(7):
        for active in combinations(SITES, size):
            selected = selected_family(active)
            endpoint_ranks = tuple(
                SHARP["rational_rank"](selected[site]) for site in SITES
            )
            require(sum(endpoint_ranks) == size,
                    ("repaired endpoint ranks changed", active, endpoint_ranks))
            selected_checks += audit_selected_equations(selected)
            literal_checks += audit_literal_selected_slice(selected)
            for root in active:
                require(witnesses[root],
                        ("an active repaired root lost R2", active, root))
            for root in set(SITES) - set(active):
                require(selected[root] == ZERO_MATRIX,
                        ("an inactive repaired root lost preservation", active, root))
            counts[size] += 1
            calibrations.setdefault(size, (active, endpoint_ranks))
    require(counts == {0: 1, 1: 6, 2: 15, 3: 20, 4: 15, 5: 6, 6: 1},
            ("the repaired subset census changed", counts))
    print("six-rank-one repaired isotropic-pencil boundary: all checks passed")
    print(f"  changed cells/residual ranks : {len(changed)}/60, {ranks}")
    print(f"  separate factored faces      : {faces}")
    print(f"  six-root R2 witnesses        : {witnesses}")
    print(f"  active-subset census         : {counts}")
    print(f"  rank-profile calibrations    : {calibrations}")
    print(f"  selected/literal checks      : {selected_checks}/{literal_checks}")
    print("  conclusion                   : kR+(6-k)Z reaches rank 55 for all k")


if __name__ == "__main__":
    main()

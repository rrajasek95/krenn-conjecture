#!/usr/bin/env python3
"""Shared full-L0 rank-51 guards through the 6R endpoint pattern.

Starting from the rank-42 four-root repair, add E11 cells on edges 24
and 25 with coefficients in the ratio right_4:-right_5.  Two further
right-weight pairs and one left-weight pair raise the rank without changing
any endpoint slice.  Roots 4 and 5 gain their missing output-one witnesses.
Any subset of all six selected matrices can then be activated on the common
isotropic input line e_0; alternatively, one arbitrary selected matrix may
be active at any root.  Standard library only; live under -O and -I -S.
"""

from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
FOUR = run_path(str(
    HERE / "verify_level_two_four_rank_one_two_zero_gauge_coupled_repair.py"
))
BASE = FOUR["BASE"]
CORE = FOUR["CORE"]
SITES = FOUR["SITES"]
COLOURS = FOUR["COLOURS"]
EDGES = FOUR["EDGES"]
ZERO_MATRIX = FOUR["ZERO_MATRIX"]
CAPABLE = SITES
OUTPUT_FACTORS = {
    0: (2, 3),
    1: (3, 5),
    2: (5, 7),
    3: (7, 11),
    4: (11, 13),
    5: (13, 17),
}
WITNESSES = {
    0: {0: 3, 1: 2},
    1: {0: 2, 1: 3},
    2: {0: 3, 1: 0},
    3: {0: 2, 1: 1},
    4: {0: 5, 1: 2},
    5: {0: 4, 1: 2},
}
POTENTIALS = (0,) * len(SITES)
INVERTIBLE_SELECTED = ((2, 3), (5, 7))


def rank50_member():
    packet, u_star, v_star, first_repair = FOUR["repaired_member"]()
    _p, _q, _beta, _gamma, _left, right = (
        FOUR["RIGID"]["integrated_member"]()[3]
    )
    d, f = right[4], -right[5]
    require(d * right[5] + f * right[4] == 0,
            "the two-edge mixed-slice cancellation changed")
    packet[2, 4, 1, 1] = d
    packet[2, 5, 1, 1] = f
    for root in (0, 1):
        packet[root, 4, 1, 1] = -right[4]
        packet[root, 5, 1, 1] = right[5]

    _p, _q, _beta, _gamma, left, _right = (
        FOUR["RIGID"]["integrated_member"]()[3]
    )
    g0, g1 = left[0], left[1]
    require(g0 * left[1] - g1 * left[0] == 0,
            "the left-weight cancellation changed")
    packet[0, 4, 0, 0] = g0
    packet[1, 4, 0, 0] = g1
    return packet, u_star, v_star, (
        first_repair, d, f, right, left,
    )


LINE_CHANGES = {
    (0, 1, 0, 0): 13,
    (0, 1, 1, 0): 13,
    (0, 3, 0, 0): -26,
    (0, 3, 1, 0): -26,
    (0, 5, 0, 0): -22,
    (1, 5, 0, 0): -26,
}


def repaired_member():
    packet, u_star, v_star, previous = rank50_member()
    for cell, change in LINE_CHANGES.items():
        packet[cell] += change
    return packet, u_star, v_star, (previous, LINE_CHANGES)


def selected_family(active):
    selected = {site: ZERO_MATRIX for site in SITES}
    for site in active:
        h0, h1 = OUTPUT_FACTORS[site]
        selected[site] = ((h0, 0), (h1, 0))
    return selected


def audit_rank_and_l0(packet, u_star, v_star):
    tangents = {
        (s, t): BASE["factored_tangent"](u_star, v_star, s, t)
        for s, t in product(COLOURS, repeat=2)
    }
    outputs = {
        key: CORE["apply_differential"](packet, tangent)
        for key, tangent in tangents.items()
    }
    require(outputs == {
        (0, 0): [int(word == (0,) * 6) for word in CORE["WORDS"]],
        (0, 1): [0] * 64,
        (1, 0): [0] * 64,
        (1, 1): [int(word == (1,) * 6) for word in CORE["WORDS"]],
    }, "the six-rank-one repair lost its four L0 slices")
    derivative = CORE["differential_matrix"](packet)
    mixed = [
        row for row, word in zip(derivative, CORE["WORDS"])
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = (
        BASE["ranks_over_fields"](derivative),
        BASE["ranks_over_fields"](mixed),
    )
    require(ranks == (
        (51, 51, 51, 51),
        (49, 49, 49, 49),
    ), ("the six-rank-one repaired ranks changed", ranks))
    return ranks


def audit_exact_affine_line():
    base_packet, u_star, v_star, _repair = rank50_member()
    expected_outputs = {
        (0, 0): [int(word == (0,) * 6) for word in CORE["WORDS"]],
        (0, 1): [0] * 64,
        (1, 0): [0] * 64,
        (1, 1): [int(word == (1,) * 6) for word in CORE["WORDS"]],
    }
    ranks = []
    for scalar in (0, 1, 2):
        packet = dict(base_packet)
        for cell, change in LINE_CHANGES.items():
            packet[cell] += scalar * change
        outputs = {
            (s, t): CORE["apply_differential"](
                packet, BASE["factored_tangent"](u_star, v_star, s, t)
            )
            for s, t in product(COLOURS, repeat=2)
        }
        require(outputs == expected_outputs,
                ("the exact affine repair line changed", scalar))
        derivative = CORE["differential_matrix"](packet)
        mixed = [
            row for row, word in zip(derivative, CORE["WORDS"])
            if word not in ((0,) * 6, (1,) * 6)
        ]
        ranks.append((
            BASE["ranks_over_fields"](derivative),
            BASE["ranks_over_fields"](mixed),
        ))
    require(ranks == [
        ((50, 50, 50, 50), (48, 48, 48, 48)),
        ((51, 51, 51, 51), (49, 49, 49, 49)),
        ((51, 51, 51, 51), (49, 49, 49, 49)),
    ], ("the affine-line rank calibration changed", ranks))
    return ranks


def audit_selected_equations(packet, selected):
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
                == (POTENTIALS[u] + POTENTIALS[v]) * packet[u, v, a, b],
                ("six-rank-one generic-kernel identity failed",
                 u, v, a, b),
            )
            tangent[u, v, a, b] = numerator
            checks += 1
    require(checks == 60, "six-rank-one scalar census changed")
    require(CORE["apply_differential"](packet, tangent) == [0] * 64,
            "a six-rank-one selected row survived")
    return checks


def audit_literal_slices(packet, u_star, v_star, selected):
    function = BASE["audit_literal_eight_site_slices"]
    globals_dict = function.__globals__
    old_x = globals_dict["X"]
    try:
        globals_dict["X"] = selected
        checked = function(packet, u_star, v_star)
    finally:
        globals_dict["X"] = old_x
    require(checked == 256, "the six-rank-one literal slice census changed")
    return checked


def audit_capable_root(packet, root):
    table = {}
    for output, neighbour in WITNESSES[root].items():
        require(BASE["pure_internal_column"](packet, root, neighbour, output),
                ("a six-rank-one pure witness vanished",
                 root, output, neighbour))
        complement = tuple(
            site for site in SITES if site not in (root, neighbour)
        )
        nonzero = sum(
            CORE["hafnian"](packet, complement, word) != 0
            for word in CORE["WORDS"]
        )
        require(nonzero,
                ("a six-rank-one witness cofactor vanished",
                 root, output, neighbour))
        table[output] = (neighbour, nonzero)
    return table


def audit_single_invertible_cases(packet, u_star, v_star, witnesses):
    cases = {}
    for root in SITES:
        selected = {site: ZERO_MATRIX for site in SITES}
        selected[root] = INVERTIBLE_SELECTED
        endpoint_ranks = tuple(
            CORE["rational_rank"](selected[site]) for site in SITES
        )
        require(endpoint_ranks[root] == 2
                and sum(endpoint_ranks) == 2,
                ("the single-invertible endpoint ranks changed",
                 root, endpoint_ranks))
        generic = audit_selected_equations(packet, selected)
        literal = audit_literal_slices(packet, u_star, v_star, selected)
        require(witnesses[root],
                ("the single-invertible root lost R2", root))
        cases[root] = (endpoint_ranks, generic, literal)
    require(len(cases) == 6,
            ("the single-invertible case count changed", cases))
    return cases


def main():
    line_ranks = audit_exact_affine_line()
    packet, u_star, v_star, repair = repaired_member()
    ranks = audit_rank_and_l0(packet, u_star, v_star)
    witness_tables = {
        root: audit_capable_root(packet, root) for root in CAPABLE
    }
    counts = {size: 0 for size in range(7)}
    cases = 0
    for size in range(7):
        for active in combinations(CAPABLE, size):
            selected = selected_family(active)
            endpoint_ranks = tuple(
                CORE["rational_rank"](selected[site]) for site in SITES
            )
            require(sum(endpoint_ranks) == size,
                    ("six-rank-one endpoint ranks changed",
                     active, endpoint_ranks))
            require(audit_selected_equations(packet, selected) == 60,
                    ("six-rank-one selected census changed", active))
            require(audit_literal_slices(packet, u_star, v_star, selected)
                    == 256,
                    ("six-rank-one literal census changed", active))
            for root in active:
                require(witness_tables[root],
                        ("an active six-rank-one root lost R2", active, root))
            counts[size] += 1
            cases += 1
    require(counts == {0: 1, 1: 6, 2: 15, 3: 20,
                       4: 15, 5: 6, 6: 1},
            ("the six-rank-one subset census changed", counts))
    require(cases == 64, ("the six-rank-one case count changed", cases))
    invertible_cases = audit_single_invertible_cases(
        packet, u_star, v_star, witness_tables
    )
    print("six-rank-one gauge-coupled repair: all checks passed")
    print(f"  multi-stage repair           : {repair}")
    print(f"  affine-line rank calibration : {line_ranks}")
    print(f"  differential ranks          : {ranks}")
    print(f"  capable-root witnesses      : {witness_tables}")
    print(f"  active-subset census        : {counts}")
    print("  selected rank cases         : 64/64")
    print(f"  single-invertible cases     : {len(invertible_cases)}/6")
    print("  conclusion                  : shared full L0 reaches 6R at rank 51")


if __name__ == "__main__":
    main()

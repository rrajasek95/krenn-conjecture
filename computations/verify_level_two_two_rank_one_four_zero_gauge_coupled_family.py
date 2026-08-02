#!/usr/bin/env python3
"""Shared full-L0 rank-38 guards through the 2R+4Z endpoint pattern.

The integrated gauge-coupled packet has two R2-capable roots, 2 and 3.
Activate either or both with rank-one selected matrices on the common
isotropic input line e_0.  Pairwise generic-kernel numerators and the
rare/rare slice remain zero, while both roots use fixed internal witnesses.
Standard library only; live under -O and -I -S.
"""

from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
RIGID = run_path(str(
    HERE
    / "verify_level_two_one_invertible_gauge_coupled_deformation_rigidity.py"
))
BASE = RIGID["BASE"]
CORE = RIGID["CORE"]
SITES = BASE["SITES"]
COLOURS = BASE["COLOURS"]
EDGES = BASE["EDGES"]
ZERO_MATRIX = ((0, 0), (0, 0))
CAPABLE = (2, 3)
OUTPUT_FACTORS = {
    2: (2, 3),
    3: (5, 7),
}
WITNESSES = {
    2: {0: 3, 1: 0},
    3: {0: 2, 1: 1},
}
POTENTIALS = (0,) * len(SITES)


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
    }, "the two-rank-one family lost its four L0 slices")
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
        (38, 38, 38, 38),
        (36, 36, 36, 36),
    ), ("the two-rank-one family ranks changed", ranks))
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
                ("two-rank-one generic-kernel identity failed", u, v, a, b),
            )
            tangent[u, v, a, b] = numerator
            checks += 1
    require(checks == 60, "two-rank-one scalar census changed")
    require(CORE["apply_differential"](packet, tangent) == [0] * 64,
            "a two-rank-one selected row survived")
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
    require(checked == 256, "the two-rank-one literal slice census changed")
    return checked


def audit_capable_root(packet, root):
    table = {}
    for output, neighbour in WITNESSES[root].items():
        require(BASE["pure_internal_column"](packet, root, neighbour, output),
                ("a two-rank-one pure witness vanished",
                 root, output, neighbour))
        complement = tuple(
            site for site in SITES if site not in (root, neighbour)
        )
        nonzero = sum(
            CORE["hafnian"](packet, complement, word) != 0
            for word in CORE["WORDS"]
        )
        require(nonzero,
                ("a two-rank-one witness cofactor vanished",
                 root, output, neighbour))
        table[output] = (neighbour, nonzero)
    return table


def main():
    _jacobian, rank, nullity, residual, endpoint = RIGID["audit_exact_jacobian"]()
    packet, u_star, v_star, _parameters = RIGID["integrated_member"]()
    ranks = audit_rank_and_l0(packet, u_star, v_star)
    witness_tables = {
        root: audit_capable_root(packet, root) for root in CAPABLE
    }
    counts = {size: 0 for size in range(3)}
    results = {}
    for size in range(3):
        for active in combinations(CAPABLE, size):
            selected = selected_family(active)
            endpoint_ranks = tuple(
                CORE["rational_rank"](selected[site]) for site in SITES
            )
            require(sum(endpoint_ranks) == size,
                    ("two-rank-one endpoint ranks changed",
                     active, endpoint_ranks))
            generic = audit_selected_equations(packet, selected)
            literal = audit_literal_slices(packet, u_star, v_star, selected)
            for root in active:
                require(witness_tables[root],
                        ("an active two-rank-one root lost R2", active, root))
            for root in set(SITES) - set(active):
                require(selected[root] == ZERO_MATRIX,
                        ("an inactive root lost preservation", active, root))
            counts[size] += 1
            results[active] = (endpoint_ranks, generic, literal)
    require(counts == {0: 1, 1: 2, 2: 1},
            ("the two-rank-one subset census changed", counts))
    print("two-rank-one gauge-coupled family: all checks passed")
    print(f"  enlarged ansatz Jacobian    : 40x34, rank {rank}, nullity {nullity}")
    print(f"  residual/endpoint tangents  : {residual}/{endpoint}")
    print(f"  differential ranks          : {ranks}")
    print(f"  capable-root witnesses      : {witness_tables}")
    print(f"  active-subset census        : {counts}")
    print(f"  selected rank cases         : {results}")
    print("  conclusion                  : shared full L0 reaches 2R+4Z at rank 38")


if __name__ == "__main__":
    main()

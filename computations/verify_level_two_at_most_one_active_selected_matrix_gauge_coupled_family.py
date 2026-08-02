#!/usr/bin/env python3
"""Audit the rank-38 full-L0 family with at most one active selected matrix.

The gauge-coupled residual packet and endpoint stars work unchanged when
only X_2 may be nonzero.  Pairwise generic-kernel numerators and selected
rows vanish, the rare/rare slice is zero, and the active root has two fixed
internal R2 witnesses.  Exact representatives of ranks 0, 1, and 2 are
checked.  Standard library only; live under -O and -I -S.
"""

from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
RIGID = run_path(str(
    HERE / "verify_level_two_one_invertible_gauge_coupled_deformation_rigidity.py"
))
BASE = RIGID["BASE"]
CORE = RIGID["CORE"]
SITES = BASE["SITES"]
COLOURS = BASE["COLOURS"]
EDGES = tuple(combinations(SITES, 2))
ZERO_MATRIX = ((0, 0), (0, 0))
POTENTIALS = (0,) * len(SITES)
REPRESENTATIVES = {
    0: ZERO_MATRIX,
    1: ((1, 2), (3, 6)),
    2: ((1, 2), (3, 7)),
}


def selected_family(active_matrix):
    return {
        site: active_matrix if site == 2 else ZERO_MATRIX
        for site in SITES
    }


def audit_selected_equations(packet, selected):
    endpoint_ranks = tuple(CORE["rational_rank"](selected[site]) for site in SITES)
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
                ("one-active generic-kernel identity failed", u, v, a, b),
            )
            tangent[u, v, a, b] = numerator
            checks += 1
    require(checks == 60, "one-active generic scalar census changed")
    require(CORE["apply_differential"](packet, tangent) == [0] * 64,
            "a one-active selected level-two row survived")
    require(-sum(POTENTIALS) == 0,
            "the one-active direct selected value is nonzero")
    return endpoint_ranks, checks


def audit_literal_slices(packet, u_star, v_star, selected):
    audit = BASE["audit_literal_eight_site_slices"]
    globals_dict = audit.__globals__
    require(globals_dict is BASE["full_edge_value"].__globals__,
            "the imported literal evaluators lost shared globals")
    old_x = globals_dict["X"]
    try:
        globals_dict["X"] = selected
        checked = audit(packet, u_star, v_star)
    finally:
        globals_dict["X"] = old_x
    require(checked == 256, "the one-active literal slice census changed")
    return checked


def audit_r2(packet, selected):
    preserving = tuple(site for site in SITES if selected[site] == ZERO_MATRIX)
    require(preserving == (0, 1, 3, 4, 5),
            ("the one-active preserving roots changed", preserving))
    require(BASE["pure_internal_column"](packet, 2, 3, 0),
            "the active-root pure-zero witness vanished")
    require(BASE["pure_internal_column"](packet, 2, 0, 1),
            "the active-root pure-one witness vanished")
    for neighbour in (3, 0):
        complement = tuple(site for site in SITES if site not in (2, neighbour))
        require(any(
            CORE["hafnian"](packet, complement, word) != 0
            for word in CORE["WORDS"]
        ), ("an active-root R2 cofactor vanished", neighbour))
    return preserving, (3, 0)


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
    }, "the one-active family lost its four L0 slices")
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
    ), ("the one-active family ranks changed", ranks))
    return ranks


def main():
    _jacobian, rank, nullity, residual, endpoint = RIGID["audit_exact_jacobian"]()
    packet, u_star, v_star, _parameters = RIGID["integrated_member"]()
    ranks = audit_rank_and_l0(packet, u_star, v_star)
    results = {}
    for expected_rank, active_matrix in REPRESENTATIVES.items():
        selected = selected_family(active_matrix)
        endpoint_ranks, generic = audit_selected_equations(packet, selected)
        require(endpoint_ranks[2] == expected_rank,
                ("active representative rank changed", expected_rank, endpoint_ranks))
        literal = audit_literal_slices(packet, u_star, v_star, selected)
        if expected_rank:
            preserving, witnesses = audit_r2(packet, selected)
        else:
            preserving = SITES
            witnesses = ()
        results[expected_rank] = {
            "endpoint_ranks": endpoint_ranks,
            "generic": generic,
            "literal": literal,
            "preserving": len(preserving),
            "witnesses": witnesses,
        }
    print("at-most-one-active selected-matrix family: all checks passed")
    print(f"  enlarged ansatz Jacobian    : 40x34, rank {rank}, nullity {nullity}")
    print(f"  residual/endpoint tangents  : {residual}/{endpoint}")
    print(f"  differential ranks          : {ranks}")
    print(f"  selected rank cases         : {results}")
    print("  conclusion                  : 6Z, 1R+5Z, and 1I+5Z share rank 38")


if __name__ == "__main__":
    main()

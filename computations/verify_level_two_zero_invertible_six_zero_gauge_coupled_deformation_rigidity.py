#!/usr/bin/env python3
"""Rebind the rigid gauge-coupled full-L0 chart from 1I+5Z to 6Z.

The residual packet, endpoint stars, four L0 equations, and differential do
not depend on the selected endpoint matrices.  Setting all six matrices and
potentials to zero makes the generic-kernel, selected, and residual-R2 rows
automatic.  The enlarged sparse chart therefore still has differential rank
38/36 and the same 40-by-34 rigidity calculation.  Standard library only;
all checks remain live under -O and -I -S.
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
X_ZERO = {site: ZERO_MATRIX for site in SITES}
POTENTIALS = (0,) * len(SITES)


def audit_zero_selected_rows(packet):
    endpoint_ranks = tuple(CORE["rational_rank"](X_ZERO[site]) for site in SITES)
    require(endpoint_ranks == (0, 0, 0, 0, 0, 0),
            ("six-zero endpoint ranks changed", endpoint_ranks))

    tangent = {}
    checks = 0
    for u, v in EDGES:
        for a, b in product(COLOURS, repeat=2):
            numerator = sum(
                X_ZERO[u][a][i] * X_ZERO[v][b][1 - i]
                for i in COLOURS
            )
            require(
                numerator
                == (POTENTIALS[u] + POTENTIALS[v]) * packet[u, v, a, b],
                ("six-zero generic-kernel identity failed", u, v, a, b),
            )
            tangent[u, v, a, b] = numerator
            checks += 1
    require(checks == 60, "six-zero generic scalar census changed")
    require(CORE["apply_differential"](packet, tangent) == [0] * 64,
            "a six-zero selected level-two row survived")
    require(-sum(POTENTIALS) == 0,
            "the six-zero direct selected value is nonzero")
    return endpoint_ranks, checks


def audit_literal_slices_with_zero_selected_matrices(packet, u_star, v_star):
    # The imported literal evaluator and audit share one module-global X.
    # Rebind it only for this call so the rare/rare slice is genuinely 6Z.
    audit = BASE["audit_literal_eight_site_slices"]
    globals_dict = audit.__globals__
    require(globals_dict is BASE["full_edge_value"].__globals__,
            "the imported literal evaluators lost shared globals")
    old_x = globals_dict["X"]
    try:
        globals_dict["X"] = X_ZERO
        checked = audit(packet, u_star, v_star)
    finally:
        globals_dict["X"] = old_x
    require(checked == 256, "the six-zero literal slice census changed")
    return checked


def audit_residual_r2_preservation():
    preserving = tuple(
        site for site in SITES
        if X_ZERO[site] == ZERO_MATRIX
    )
    require(preserving == SITES,
            ("a six-zero root lost residual preservation", preserving))
    return preserving


def audit_integrated_member():
    packet, u_star, v_star, _parameters = RIGID["integrated_member"]()
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
    }, "the six-zero integrated member lost its four L0 slices")

    derivative = CORE["differential_matrix"](packet)
    mixed = [
        row for row, word in zip(derivative, CORE["WORDS"])
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = {
        "D": BASE["ranks_over_fields"](derivative),
        "D_mixed": BASE["ranks_over_fields"](mixed),
    }
    require(ranks == {
        "D": (38, 38, 38, 38),
        "D_mixed": (36, 36, 36, 36),
    }, ("the six-zero integrated ranks changed", ranks))
    literal = audit_literal_slices_with_zero_selected_matrices(
        packet, u_star, v_star
    )
    endpoint_ranks, generic = audit_zero_selected_rows(packet)
    preserving = audit_residual_r2_preservation()
    return ranks, literal, endpoint_ranks, generic, preserving


def main():
    _jacobian, rank, nullity, residual, endpoint = RIGID["audit_exact_jacobian"]()
    cross = RIGID["audit_classification_implications"]()
    ranks, literal, endpoint_ranks, generic, preserving = audit_integrated_member()
    print("zero-invertible gauge-coupled deformation rigidity: all checks passed")
    print(f"  enlarged ansatz Jacobian    : 40x34, rank {rank}, nullity {nullity}")
    print(f"  residual/endpoint tangents  : {residual}/{endpoint}")
    print(f"  classified cross weights    : {cross}/4, rank-one rectangle")
    print(f"  integrated differential     : {ranks}")
    print(f"  literal full-L0 slices      : {literal}/256")
    print(f"  endpoint ranks              : {endpoint_ranks}")
    print(f"  generic/selected checks     : {generic}/60, 64/64")
    print(f"  residual-R2 preserving roots: {len(preserving)}/6")
    print("  conclusion                  : enlarged 6Z sparse chart stays rank 38")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact finite ledger for the carrier Grassmann incidence compactification."""

from __future__ import annotations

from hashlib import sha256
import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_carrier_incidence_compactification.json"
TORUS_RESULT = (HERE.parent /
    "unaudited-codex-carrier-torus-covariance-2026-08-21" /
    "results_carrier_torus_covariance.json")
TAIL_RESULT = (HERE.parent /
    "unaudited-codex-tail-polar-source-lift-2026-08-21" /
    "results_tail_polar_source_lift.json")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main(write_results=False):
    torus = json.loads(TORUS_RESULT.read_text())
    require(torus["status"].startswith("PASS"), "torus audit not frozen")

    # The pure-preserving one-parameter subgroup realizing the exact curve.
    one_ps = {
        (site, colour): (0 if colour else (1 if site == 2 else
                                          -1 if site == 3 else 0))
        for site in range(8) for colour in range(3)
    }
    require(all(sum(one_ps[site, colour] for site in range(8)) == 0
                for colour in range(3)),
            "one-parameter subgroup left the pure subtorus")
    nonzero_curve_cells = {
        (0, 1, 0, 0): 0,
        (2, 3, 0, 0): 0,
        (4, 5, 0, 0): 0,
        (6, 7, 0, 0): 0,
        (0, 1, 1, 1): 0,
        (2, 3, 1, 1): 0,
        (4, 5, 1, 1): 0,
        (6, 7, 1, 1): 0,
        (0, 1, 2, 2): 0,
        (2, 3, 2, 2): 0,
        (4, 5, 2, 2): 0,
        (6, 7, 2, 2): 0,
        (1, 6, 0, 0): 0,
        (2, 7, 0, 0): 1,
    }
    for value, expected in nonzero_curve_cells.items():
        u, v, i, j = value
        require(one_ps[u, i] + one_ps[v, j] == expected,
                "curve cell weight changed")

    # Rank/Schubert boundary signatures for a nonzero chosen blocker.
    fixed_rank_ledger = {}
    total_signatures_one_blocker = 0
    for r in range(1, 10):
        records = []
        for s in range(r):
            # ell not in the actual rowspace: it must be supplied by the
            # ghost quotient W/U.
            ghost_dimension = (r - s - 1) * (9 - r)
            records.append({
                "generic_rank_r": r,
                "special_rank_s": s,
                "blocker_position": "ghost_only",
                "fiber": f"Gr({r-s-1},{8-s})",
                "fiber_dimension": ghost_dimension,
            })
            if s >= 1:
                actual_dimension = (r - s) * (9 - r)
                records.append({
                    "generic_rank_r": r,
                    "special_rank_s": s,
                    "blocker_position": "already_in_actual_rowspace",
                    "fiber": f"Gr({r-s},{9-s})",
                    "fiber_dimension": actual_dimension,
                })
        require(len(records) == 2 * r - 1,
                "fixed-r Schubert signature count changed")
        fixed_rank_ledger[str(r)] = records
        total_signatures_one_blocker += len(records)
    require(total_signatures_one_blocker == 81,
            "all-r single-blocker signature count changed")

    # Two blocker types after S3 (diagonal/direct), two carrier types
    # (star/triangle).  This is only the smallest rank/Schubert ledger; it
    # deliberately does not count simultaneous choices at 728 carriers.
    global_boundary_signatures = 81 * 2 * 2
    require(global_boundary_signatures == 324,
            "global minimal boundary signature count changed")

    result = {
        "status": "PASS proper carrier incidence compactification audit",
        "proper_incidence": {
            "ambient": "X x Gr(r,9)",
            "universal_subbundle": "S subset O^9",
            "closed_row_incidence": (
                "I_r={(A,W): row(L(A)) subset W}; it is the zero locus of "
                "the composite row(L):O^m -> O^9 -> O^9/S"
            ),
            "closed_blocker_incidence": (
                "I_(r,beta)=I_r intersect {ell_beta(A) in W}; the second "
                "condition is the zero locus of ell_beta in O^9/S"
            ),
            "graph_closure": (
                "Gamma_(r,beta)=closure of {(A,rowspan L(A)):rank L=r, "
                "ell_beta in rowspan L} inside X x Gr(r,9)"
            ),
            "containment": "Gamma_(r,beta) subset I_(r,beta), generally strict",
            "properness": (
                "Gr(r,9) is projective; both closed incidences and the graph "
                "closure project properly to X, so their images are closed"
            ),
            "meaning": (
                "The proper image is the closure of the affine fixed-r blocker "
                "branch, not the original unstratified membership set."
            ),
        },
        "torus_lift": {
            "source_action": "A -> lambda.A",
            "Grassmann_action": "W -> W*D_kappa",
            "response_covariance": "L(lambda.A)=D_rho*L(A)*D_kappa",
            "incidence_preserved": True,
            "diagonal_blocker": (
                "the coordinate line <K_dd> is fixed projectively because "
                "K_dd has character kappa_dd^-1"
            ),
            "direct_blocker": (
                "ell_A transforms as ell_A*D_kappa, so ell_A in W is equivariant"
            ),
            "graph_closure_torus_invariant": True,
        },
        "explicit_ghost_curve": {
            "source_curve": torus["pure_normalized_nonclosedness_counterexample"]["curve"],
            "pure_H_values": [1, 1, 1],
            "pure_preserving_1PS_weights": {
                f"mu_{site},{colour}": one_ps[site, colour]
                for site in range(8) for colour in range(3)
            },
            "nonzero_coordinate_weights": {
                f"a_{u}{v}_{i}{j}": value
                for (u, v, i, j), value in nonzero_curve_cells.items()
            },
            "carrier": {"pair": [6, 7], "kind": "star", "centre": 0},
            "generic_response": "L(t)=t*E_(row 12:00,column K00)",
            "generic_rank": 1,
            "generic_rowspace": "W(t)=<K00>",
            "special_response": "L(0)=0",
            "special_rank": 0,
            "Grassmann_limit": "W_0=<K00>",
            "ghost_quotient": "W_0/rowspan(L(0))=<K00>",
            "blocker_retained": "K00 in W_0",
            "fiber_check": (
                "for r=1,s=0 and ell=K00 notin rowspan L(0), the blocker "
                "fiber is Gr(0,8), one point: W_0=<K00>"
            ),
            "interpretation": (
                "The Grassmann graph remembers the normalized leading row "
                "t^-1 L(t)=E_00 that disappears from the affine special fiber."
            ),
        },
        "boundary_fiber_lemma": {
            "setup": (
                "At A_0 let U=rowspan L(A_0), dim U=s<r, and let ell be a "
                "nonzero chosen blocker.  The full incidence fiber consists "
                "of r-planes W containing U and ell."
            ),
            "ell_in_U": {
                "fiber": "Gr(r-s,9-s)",
                "dimension": "(r-s)(9-r)",
            },
            "ell_not_in_U": {
                "fiber": "Gr(r-s-1,8-s)",
                "dimension": "(r-s-1)(9-r)",
            },
            "graph_closure_guard": (
                "Only those W arising as leading rowspaces of rank-r arcs "
                "belong to Gamma_r; the displayed Grassmannians are the larger "
                "naive incidence fibers."
            ),
        },
        "smallest_finite_rank_Schubert_target": {
            "per_fixed_rank_nonzero_blocker": "2r-1 signatures",
            "fixed_rank_ledger": fixed_rank_ledger,
            "all_ranks_one_blocker_type": total_signatures_one_blocker,
            "blocker_types_mod_S3": ["diagonal", "direct"],
            "carrier_types": ["star", "triangle"],
            "global_boundary_signatures_before_matroids": global_boundary_signatures,
            "direct_zero_guard": (
                "The 324 count assumes a nonzero direct blocker line.  The "
                "closed divisor A_pq=0 is a separate inactive-pair stratum; "
                "there ell_direct=0 lies in every W without a Schubert condition."
            ),
            "simultaneous_carrier_guard": (
                "This does not quotient the independent blocker assignments "
                "across 728 carriers; the naive global disjunction is still enormous."
            ),
        },
        "Hilbert_Mumford_boundary_data": {
            "required": [
                "special source point A_0 and rank s of L(A_0)",
                "generic rank r and chosen blocker type beta",
                "actual rowspace U and ghost quotient W/U",
                "Plucker support (realizable column matroid) and 1PS weights",
                "leading normalized response row module along the arc",
                "leading blocker line if the direct blocker vanishes at A_0",
                "initial/tangent equations certifying that the arc remains in X5",
            ],
            "torus_limit_rule": (
                "The Grassmann limit is determined by minimum-weight nonzero "
                "Plucker coordinates; equivalently by the initial matroid face."
            ),
            "finite_but_not_small_refinement": (
                "Rank/Schubert signatures must be refined by realizable rank-r "
                "matroids on nine columns modulo endpoint-colour symmetry. "
                "Matroid strata are finite but can carry coefficient moduli."
            ),
        },
        "tail_response_interaction": {
            "naive_incidence_base_change": (
                "Pulling I_(r,beta) back to the tail/X5 source locus changes "
                "only A.  Its fiber over a fixed A_0 remains the same displayed "
                "Grassmannian because the tail equations contain no W variables."
            ),
            "graph_closure_possibility": (
                "Tail equations can eliminate a ghost plane only by forbidding "
                "every rank-r arc with that leading rowspace.  This is a tangent/"
                "Rees-algebra condition on the r-minor ideal, not a consequence "
                "of the frozen 380x12 coefficient rank theorem."
            ),
            "current_frozen_interface": (
                "No source identity maps the tail-response Fitting module to "
                "the carrier complete-collineation/Rees data."
            ),
            "verdict": (
                "The naive proper incidence merely enlarges the state space. "
                "The smaller graph closure could help only after a new X5 "
                "arc/initial-module theorem; none is presently frozen."
            ),
        },
        "rigorous_diagram": [
            "Z^o_(r,beta)={(A,rowspan L):rank L=r, ell_beta in rowspan L}",
            "Z^o_(r,beta) -> Gamma_(r,beta) -> I_(r,beta) subset X x Gr(r,9)",
            "Gamma_(r,beta) --proper--> closure_X(projection Z^o_(r,beta))",
            "I_(r,beta) --proper--> a generally larger closed rank-drop locus",
            "base change to X5 preserves properness but not equality Gamma=I",
        ],
        "terminal_verdict": (
            "Grassmann/complete-collineation compactification repairs torus "
            "specialization by retaining ghost blocker planes, but it does not "
            "reduce the proof without controlling X5-compatible leading row "
            "modules.  At the currently frozen interface it increases, rather "
            "than decreases, the finite state space."
        ),
        "upstream_sha256": {
            "torus_result": file_hash(TORUS_RESULT),
            "tail_result": file_hash(TAIL_RESULT),
        },
    }
    result["logical_sha256"] = logical_hash(result)
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "ghost": result["explicit_ghost_curve"]["Grassmann_limit"],
        "fixed_rank_signature_counts": {
            r: len(records) for r, records in fixed_rank_ledger.items()
        },
        "global_boundary_signatures": global_boundary_signatures,
        "tail_verdict": result["tail_response_interaction"]["verdict"],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)

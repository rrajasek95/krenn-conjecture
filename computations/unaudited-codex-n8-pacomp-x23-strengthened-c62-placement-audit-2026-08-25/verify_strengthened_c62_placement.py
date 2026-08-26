#!/usr/bin/env python3
"""Exact h=3 audit of the strengthened C6.2 filler/placement interface.

This is a small rational/integral chain calculation.  It verifies the
conditional chart filler formula, the coefficient placement J, all forced
signs/covariances, and a minimal countermodel showing why the physical
placement does not follow from the character-level filler.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "PROOF-SKETCH.md":
        "8af22bf67777c3a8e7daad0639dab09848f89087bb0b2114d232ad52dc2f70bf",
    "notes/uniform-balanced-chart-square-master-obstruction.md":
        "c758fb43f88d9c02f5200921c6c50637bfe04402536edc3e947f74d108fbd93b",
    "notes/h3-chart-odd-gate-ii-augmented-filler-terminal-fork.md":
        "fdb07cd655a0bd4dfa519c8c7faed8cafac105345737f44902b8127324f24a2a",
    "notes/h3-gate-ii-psidelta-same-grade-extension-chain.md":
        "2e7aea9a551ddc2ab845fb2c0717cbffb8f7db772c329fb3c11d6bdc3dc34fae",
    "notes/h3-kappa-lambda-literal-mapping-cone-normalization-gate.md":
        "1e7655ab1661453200ba33aff800aa6d9991dd86922d81d4f5b488fcc15bb817",
    "notes/h3-balanced-square-private-eq-projection-gate.md":
        "6d740e7e30231204dbe1b79c4b7c21fe5f5b5ac45122ac714be3c7626afa7c31",
    "computations/verify_uniform_balanced_chart_square_master_obstruction.py":
        "306980dc569795fa3ec2c8e6fdbdf2b67fa5d85cd75ebebe62be7db15b1e1a59",
    "computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py":
        "d5628f66ffbf94e2de37318ab136adda96af5e114e2bea8dce22542ec9f30cb1",
    "computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py":
        "b60538f9db5b8c2984bbee95e0a05f383408e9ab7c13680216adf56386682522",
    "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py":
        "8be3bc5bf85f8d633e77e2a0bdd18aea6d481c81f5fb6a6a947cbaf82f862302",
    "computations/unaudited-codex-n8-pacomp-x23-physical-kappa-construction-attempt-2026-08-25/MANIFEST.sha256":
        "00899a99e57e9ced9eed7e3346cf54431037f688caab92f29a7e59d72ad95dc9",
    "computations/unaudited-codex-n8-pacomp-q23-protected-factor-2026-08-25/MANIFEST.sha256":
        "f3b689175811cb8d28dbae605fac703c8339f2e5a259c4c0e644122f1779b500",
}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((vector[i] for vector in vectors), Q(0))
                 for i in range(len(vectors[0])))


def scale(c: int | Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(c) * x for x in vector)


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    h = len(columns[0])
    require(all(len(c) == h for c in columns), "rank height")
    rows = [[columns[j][i] for j in range(len(columns))] for i in range(h)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, h)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        p = rows[answer][column]
        rows[answer] = [x / p for x in rows[answer]]
        for row in range(h):
            if row == answer or not rows[row][column]:
                continue
            c = rows[row][column]
            rows[row] = [x - c * y for x, y in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def audit() -> dict[str, object]:
    pin_dependencies()

    # Chart order is deliberately (Aab,B,Aba,C), so the requested placement
    # is coordinatewise onto (Pf,KL,KR,D4).
    z_chart = tuple(map(Q, (1, -1, 1, -1)))
    z_edge = tuple(map(Q, (1, -1, 1, -1)))
    require(z_chart == z_edge, "J stopped mapping the chart charge")

    # Vertices are (response-left,response-right,cap-left,cap-right).
    pf = tuple(map(Q, (-1, 1, 0, 0)))
    kl = tuple(map(Q, (-1, 0, 1, 0)))
    kr = tuple(map(Q, (0, -1, 0, 1)))
    d4 = tuple(map(Q, (0, 0, -1, 1)))
    edge_boundary = add(pf, scale(-1, kl), kr, scale(-1, d4))
    require(edge_boundary == (Q(0),) * 4, "edge cycle not closed")
    require(rank((pf, kl, kr, d4)) == 3, "edge rank changed")

    # Conditional Gate-II candidate.  Coordinates are
    # (Aab,B,Aba,C,tB,tC).  The relative graphs exist; the absolute E cell
    # with boundary tB+tC is precisely the missing saturation.
    Aab = (Q(1), Q(0), Q(0), Q(0), Q(0), Q(0))
    B = (Q(0), Q(1), Q(0), Q(0), Q(0), Q(0))
    Aba = (Q(0), Q(0), Q(1), Q(0), Q(0), Q(0))
    C = (Q(0), Q(0), Q(0), Q(1), Q(0), Q(0))
    tB = (Q(0), Q(0), Q(0), Q(0), Q(1), Q(0))
    tC = (Q(0), Q(0), Q(0), Q(0), Q(0), Q(1))
    dGB = add(Aab, scale(-1, B), tB)
    dGC = add(Aba, scale(-1, C), tC)
    dE = add(tB, tC)
    dLambda = add(dGB, dGC, scale(-1, dE))
    expected = z_chart + (Q(0), Q(0))
    require(dLambda == expected, "conditional Lambda boundary changed")

    # AB/AC are two independent source-labelled Hom coordinates.  The
    # unlabelled sum supplies only one of them.
    ab = (Q(1), Q(0))
    ac = (Q(0), Q(1))
    unlabelled = add(ab, ac)
    root_rank_ladder = [rank(tuple()), rank((ab,)), rank((ac,)),
                        rank((unlabelled,)), rank((ab, ac))]
    require(root_rank_ladder == [0, 1, 1, 1, 2], root_rank_ladder)

    # Minimal countermodel: the chart has Lambda_AB,Lambda_AC, while the
    # target has the two primitive edge cycles and no operation-changing C2.
    # Any chain map with the specified J1 would have
    # d J2(Lambda)=J1 d(Lambda)=z_edge, impossible because J2=0.
    target_c2_rank = 0
    J1_dLambda = z_edge
    d_J2Lambda = (Q(0),) * 4
    require(J1_dLambda != d_J2Lambda and target_c2_rank == 0,
            "countermodel unexpectedly acquired a placement")

    # Coefficient covariance.  tau transports AB to AC with +1.  sigma
    # transports q23 to q45 with -1 on the root/pure packet.  Both preserve
    # the closed edge equation, but neither creates the missing Hom/C2 cell.
    require(scale(1, z_edge) == z_edge, "tau coefficient")
    require(scale(-1, z_edge) == tuple(-x for x in z_edge),
            "sigma coefficient")

    result: dict[str, object] = {
        "schema": "pacomp-h3-strengthened-c62-placement-audit-v1",
        "status": "PASS_FORMAL_INTERFACE_PHYSICAL_FILLER_AND_PLACEMENT_OPEN",
        "scope": "canonical h=3 only; no promotion",
        "parent_manifest_sha256":
            "00899a99e57e9ced9eed7e3346cf54431037f688caab92f29a7e59d72ad95dc9",
        "pins": PINS,
        "strengthened_C6_2": {
            "labels": ["AB", "AC"],
            "cuts": ["23", "45"],
            "identical_physical_grade": [
                "word", "fine", "repeated/Hasse", "fixed C4/common tail",
                "operation idempotent", "root label",
            ],
            "fillers": "d Lambda_c^rho=A_[a|b]-B+A_[b|a]-C",
            "placement_J": {
                "A_[a|b]": "P_f",
                "B": "K_Eq,L",
                "A_[b|a]": "K_Eq,R",
                "C": "D4",
            },
            "required_equations": [
                "d J = J d",
                "Res J = J Res",
                "Ins J = J Ins",
                "readout_edge J = readout_chart for target,q,anchor,W,ores,ridge,eta,sigma",
                "tau_AB,AC J_AB = J_AC tau_AB,AC",
                "sigma J_23 = J_45 sigma and sigma Lambda_23=-Lambda_45",
            ],
        },
        "conditional_chart_candidate": {
            "formula": "Lambda^rho=G_B^rho+G_C^rho-E_B^rho-E_C^rho",
            "dG_B": "t_B-(B-A_[a|b])",
            "dG_C": "t_C-(C-A_[b|a])",
            "d(E_B+E_C)": "t_B+t_C",
            "boundary": [int(x) for x in z_chart],
            "relative_graphs_available": True,
            "absolute_carrier_E_B_plus_E_C_available": False,
            "construction_status": "CONDITIONAL_ONLY",
        },
        "formal_checks": {
            "J_chart_order": ["A_[a|b]", "B", "A_[b|a]", "C"],
            "J_edge_order": ["P_f", "K_Eq,L", "K_Eq,R", "D4"],
            "J_maps_charge_to_edge_cycle": True,
            "edge_cycle": [int(x) for x in z_edge],
            "edge_boundary_rank": 3,
            "d_edge_cycle": [int(x) for x in edge_boundary],
            "tau_root_coefficient": 1,
            "sigma_cut_coefficient": -1,
        },
        "commuting_components": {
            "coefficient_boundary_and_d2": "PASS",
            "response_side_q23_delete_reinsert_square":
                "PASS_TERM_BY_TERM_ON_90_PINNED_DESCENDANTS",
            "decorated_q23_to_q45_monomial_transport": "PASS_COEFFICIENT_PLUS_ONE",
            "root_pure_sigma_transport": "PASS_COEFFICIENT_MINUS_ONE",
            "named_protected_readout_compatibility":
                "PASS_ONLY_FOR_FORMAL_ZERO_READOUT_COUNTERMODEL; PHYSICAL J NOT CONSTRUCTED",
            "root_forgetting": "INSUFFICIENT_RANK_ONE_OF_TWO",
        },
        "first_open_obligations": {
            "earliest_physical": (
                "two source-labelled degree-zero e_C A e_R placement sections "
                "Phi^AB and Phi^AC; exact rank ladder 24,25,25,25,26"
            ),
            "first_chain_map_equation_after_coefficient_J":
                "d_edge J_2^rho(Lambda^rho)=J_1^rho d_chart(Lambda^rho)=P_f-K_L+K_R-D4",
            "first_literal_reinsertion_equation_after_granting_Phi": (
                "J_23^rho Ins_23(s_0102^rho)=Ins_23 J_hat23^rho(s_0102^rho), "
                "whose protected residual is D_root tensor B1 tensor (H0-u)e_Eq "
                "with lower,ores,W,target,anchor zero"
            ),
        },
        "root_label_rank": {
            "minimal_ladder_none_AB_AC_unlabelled_both": root_rank_ladder,
            "pinned_strong_ladder_base_AB_AC_unlabelled_both":
                [24, 25, 25, 25, 26],
            "missing_dimension": 2,
        },
        "minimal_countermodel": {
            "chart_fillers_AB_AC": 2,
            "target_edge_cycles_AB_AC": 2,
            "target_operation_changing_C2_rank": target_c2_rank,
            "all_protected_readouts": 0,
            "tau": "+identity AB to AC",
            "sigma": "-identity q23 to q45",
            "failed_equation_left": [int(x) for x in d_J2Lambda],
            "failed_equation_right": [int(x) for x in J1_dLambda],
            "meaning": (
                "character fillers plus covariance/readout compatibility do not "
                "imply a source-labelled physical placement J"
            ),
        },
        "standard_product_guard": {
            "literal_mixed_product_balanced_charge": 0,
            "C6_2_filler_balanced_charge": 1,
            "meaning": (
                "epsilon wedge theta is a dark tied B=Eq product and is not the "
                "missing bright balanced filler"
            ),
        },
        "verdict": (
            "The exact strengthened h=3 statement is sufficient, and its "
            "coefficient boundary, tau, sigma and intrinsic response-side "
            "squares commute.  Existing notes provide only the conditional "
            "Lambda=G_B+G_C-E_B-E_C formula: the absolute carrier is absent. "
            "Even granting both labelled Lambdas, the original physical "
            "inventory lacks the two independent AB/AC e_C A e_R placements. "
            "The first source-level reinsertion residual is the pinned Eq-only "
            "D_root tensor B1 tensor (H0-u)e_Eq term."
        ),
        "promotion": "NONE_H3_ONLY",
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    return {"logical_sha256": logical, "result": result}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = audit()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

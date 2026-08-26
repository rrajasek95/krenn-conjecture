#!/usr/bin/env python3
"""Fail-closed h=3 audit of the proposed total carrier d E_T=t_B+t_C.

This is finite symbolic linear algebra only.  It does not search for, or
adjoin, an unregistered physical generator.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PINS = {
    "computations/unaudited-codex-n8-pacomp-x23-absolute-carrier-boundary-audit-2026-08-25/MANIFEST.sha256":
        "f443971c89f61ecd255e5e23840936b52f41e3aea10a29ef1c544239223bcdc4",
    "notes/h3-gate-ii-fixed-face-relative-c4-localization-projection-gate.md":
        "5b141a46ea54a44acfc98a62272d3e57a734f005e6bf86df00af0f279dcb5ea3",
    "computations/verify_h3_gate_ii_fixed_face_relative_c4_localization_projection_gate.py":
        "48bb5568b6d3360dd592011ed09aca364cfdbd24770d2e2419c1f99464825878",
    "notes/h3-first-collision-minimal-augp2-bimodule-candidate-gate.md":
        "8a6fe1f77b536f5469d23d904a4327f12a1481f8a5c994f7b1b9d2b3379c52cf",
    "computations/verify_h3_first_collision_minimal_augp2_bimodule_candidate_gate.py":
        "48703772c5bba258e32a032d42d8389bf449a794bf45bde4739e01a7d15c877f",
    "notes/h3-h2-chart-scalar-capped-c4-augmented-gate.md":
        "baee4965bcb9315fc7e9f51693aebcf3cfb6c8a147c76144eb287f7c9c74c998",
    "computations/verify_h3_h2_chart_scalar_capped_c4_augmented_gate.py":
        "18cb73805ffca0a080bc061c88cb42f6c0c83d57efd60c574455b757009785b4",
    "notes/h3-gate-ii-primitive-c4-joint-cobar-label-gate.md":
        "1adefa3bf3427a8f0c9c415376561bdd6b56c2f358fb236260b9956e7d7b0e62",
    "computations/verify_h3_gate_ii_primitive_c4_joint_cobar_label_gate.py":
        "d77f4fd853673c434d4a0bb4027bf9ba046f1bb7ea4d752028a609e832255f44",
    "notes/h3-primitive-c4-covariance-pointed-bridge-gate.md":
        "6ab0a309bdad75fe572d710b5c42c5be661159e349a3cabcf82a61c25d99edaf",
    "computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py":
        "a14339fee59134b28229fb17fcae2292bc544264ea829db60c953875f96fef41",
    "notes/h3-gate-ii-uniform-response-relative-carrier-landing-gate.md":
        "e1d0b1185cd72ff4d0d915abb1db25835f2848f65f1509458aee9f2325699084",
    "computations/verify_h3_gate_ii_uniform_response_relative_carrier_landing_gate.py":
        "9b9c05a6789d2ade9359934f279eeb429591b2e85651ebaba8485195050417eb",
    "notes/h3-gate-ii-switch-weyl-product-rule-idempotent-gate.md":
        "432a612161538958c069de828b1f0f0a3321e5bdaa758be104942140df768b7d",
    "computations/verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py":
        "fbd4815eb5c6d46b8dbcd018f6e75237f004e3f52b1ccf47631479b698f9db35",
}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(v) for v in vectors}) == 1, "add width")
    return tuple(sum((v[i] for v in vectors), Q(0))
                 for i in range(len(vectors[0])))


def scale(c: int | Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(c) * x for x in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((x * y for x, y in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    require(len({len(c) for c in columns}) == 1, "rank height")
    rows = [[columns[j][i] for j in range(len(columns))]
            for i in range(len(columns[0]))]
    answer = 0
    for column in range(len(columns)):
        pivot = next((r for r in range(answer, len(rows))
                      if rows[r][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        p = rows[answer][column]
        rows[answer] = [x / p for x in rows[answer]]
        for r in range(len(rows)):
            if r == answer or not rows[r][column]:
                continue
            c = rows[r][column]
            rows[r] = [x - c * y for x, y in
                       zip(rows[r], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("dependency changed", relative,
                                     actual, expected))


def audit() -> dict[str, object]:
    pin_dependencies()

    # Coordinates (A,B,C,tB,tC).  These are the two genuine source-labelled
    # relative endpoint-choice graphs from the parent audit.
    A = tuple(map(Q, (1, 0, 0, 0, 0)))
    B = tuple(map(Q, (0, 1, 0, 0, 0)))
    C = tuple(map(Q, (0, 0, 1, 0, 0)))
    tB = tuple(map(Q, (0, 0, 0, 1, 0)))
    tC = tuple(map(Q, (0, 0, 0, 0, 1)))
    response = add(A, B, C)
    gB = add(tB, A, scale(-1, B))
    gC = add(tC, A, scale(-1, C))
    T = add(tB, tC)
    L01 = add(scale(2, A), scale(-1, B), scale(-1, C))
    require(add(gB, gC) == add(T, L01), "parent boundary identity")

    # E exists iff the balanced total filler Lambda exists:
    # Lambda=GammaB+GammaC-E and E=GammaB+GammaC-Lambda.
    require(add(add(gB, gC), scale(-1, T)) == L01,
            "E_T/Lambda equivalence")

    relative_rank = rank((response, gB, gC))
    with_total_rank = rank((response, gB, gC, T))
    with_split_rank = rank((response, gB, gC, tB, tC))
    require((relative_rank, with_total_rank, with_split_rank) == (3, 4, 5),
            "H0 ranks")

    # Fixed-source restriction has only the zero canonical fold or the raw
    # H0-changing fold.
    r3 = tuple(map(Q, (1, 1, 1)))
    raw_b = tuple(map(Q, (-1, 1, 0)))
    raw_c = tuple(map(Q, (-1, 0, 1)))
    require(rank((r3,)) == 1 and rank((r3, raw_b, raw_c)) == 3,
            "restriction ranks")

    # Earliest chart quotient: endpoint charts do not span L01.
    B3 = tuple(map(Q, (0, 1, 0)))
    C3 = tuple(map(Q, (0, 0, 1)))
    L3 = tuple(map(Q, (2, -1, -1)))
    require(rank((B3, C3)) == 2 and rank((B3, C3, L3)) == 3,
            "L01 chart quotient")

    # The required operation-changing four-corner packet is a K2,2.  Both
    # switch types are necessary; its alternating charge is its unique
    # (one-dimensional) annihilator.
    mates = (
        tuple(map(Q, (1, 0, 1, 0))),
        tuple(map(Q, (1, 0, 0, 1))),
        tuple(map(Q, (0, 1, 1, 0))),
        tuple(map(Q, (0, 1, 0, 1))),
    )
    alternating = tuple(map(Q, (1, 1, -1, -1)))
    require(rank(mates) == 3 and all(dot(alternating, edge) == 0
                                    for edge in mates), "K2,2 charge")

    # Exact 36-face PP census of L01: three tails, two derivatives per tail
    # and two derivatives per direction pair, in three charts.
    coefficients = {"DQ": 2, "PS01": -1, "PS10": -1}
    tail_faces = {chart: 3 * 2 for chart in coefficients}
    direction_faces = {chart: 3 * 2 for chart in coefficients}
    require(sum(tail_faces.values()) == 18
            and sum(direction_faces.values()) == 18, "36-face census")

    # Relative C4 reinsertion.  Coordinates are
    # (x'yH,xy'H,x'yr,xy'r,x'y'U).  The two mixed faces cancel exactly.
    reinsertion_1 = tuple(map(Q, (1, 0, -1, 0, 1)))
    reinsertion_2 = tuple(map(Q, (0, 1, 0, -1, -1)))
    reinsertion_sum = tuple(map(Q, (1, 1, -1, -1, 0)))
    require(add(reinsertion_1, reinsertion_2) == reinsertion_sum,
            "relative reinsertion cancellation")

    # dU=H-r is presentation-safe; the absolute specialization r=0 is not.
    H = tuple(map(Q, (1, 0)))
    r = tuple(map(Q, (0, 1)))
    relative_u = add(H, scale(-1, r))
    require(2 - rank((relative_u,)) == 1 and 1 - rank(((Q(1),),)) == 0,
            "relative C4 H0")

    # The face-complete selected-row quotient after relative reinsertion.
    # Coordinates (core,z00,z01,z10,z11).
    f_a0 = tuple(map(Q, (1, 1, 1, 0, 0)))
    f_a1 = tuple(map(Q, (1, 0, 0, 1, 1)))
    f_b0 = tuple(map(Q, (1, 1, 0, 1, 0)))
    f_b1 = tuple(map(Q, (1, 0, 1, 0, 1)))
    core = tuple(map(Q, (1, 0, 0, 0, 0)))
    eta = (Q(1), Q(-1, 2), Q(-1, 2), Q(-1, 2), Q(-1, 2))
    complete_rows = (f_a0, f_a1, f_b0, f_b1)
    require(add(f_a0, f_a1, scale(-1, f_b0), scale(-1, f_b1))
            == tuple(map(Q, (0, 0, 0, 0, 0))), "centered row relation")
    require(rank(complete_rows) == 3
            and rank(complete_rows + (core,)) == 4
            and all(dot(eta, row) == 0 for row in complete_rows)
            and dot(eta, core) == 1, "retained face quotient")

    # Formal covariance characters.  These checks do not manufacture a
    # typed physical cell.
    tau_a = (2, 3, 0, 1)
    tau_b = (3, 2, 1, 0)
    permute = lambda v, p: tuple(v[p[i]] for i in range(len(p)))
    require(permute(alternating, tau_a) == scale(-1, alternating)
            and permute(alternating, tau_b) == scale(-1, alternating),
            "tau character")
    cut_sigma = {2: 5, 5: 2, 3: 4, 4: 3}
    tails = (((2, 3), (4, 5)), ((2, 4), (3, 5)), ((2, 5), (3, 4)))
    move = lambda tail: tuple(sorted(tuple(sorted((cut_sigma[x], cut_sigma[y])))
                                          for x, y in tail))
    require({move(tail) for tail in tails}
            == {tuple(sorted(tail)) for tail in tails}, "cut sigma")

    retained = (
        "-2*((dD)*q01+D*(dq01))*r_DQ "
        "+((dp0)*s1+p0*(ds1))*r_PS01 "
        "+((dp1)*s0+p1*(ds0))*r_PS10"
    )
    result: dict[str, object] = {
        "schema": "pacomp-h3-total-carrier-et-construction-audit-v1",
        "status": "PASS_NO_EXISTING_CONSTRUCTION_ONE_DIMENSIONAL_FACE_OBSTRUCTION",
        "scope": "canonical h=3 source-labelled symbolic audit only",
        "parent_manifest_sha256": PINS[next(iter(PINS))],
        "pins": PINS,
        "exact_reduction": {
            "known": "d(Gamma_B+Gamma_C)=T+L01",
            "T": "t_B+t_C",
            "L01": "2*D*q01*H-p0*s1*H-p1*s0*H",
            "equivalence": (
                "dE_T=T iff dLambda_01=L01, via "
                "Lambda_01=Gamma_B+Gamma_C-E_T"
            ),
            "consequence": "constructing E_T cannot bypass the open L01 filler",
        },
        "source_inventory": {
            "available": [
                "Gamma_B with dGamma_B=t_B+A-B",
                "Gamma_C with dGamma_C=t_C+A-C",
                "honest endpoint-choice covariance bar",
            ],
            "relative_formal_totalization": [
                "dU_j=H-r_j in DQ,PS01,PS10",
                "K_j=-d(x_j*y_j)*U_j with exact mixed-face cancellation",
            ],
            "not_available_as_source_columns": [
                "fixed-source DQ<->PS01 operation switch",
                "fixed-source DQ<->PS10 operation switch",
                "selected db01 tail carrier and reversed mate",
                "absolute direct U_C4[D,Q01;2345] reinsertion",
                "combined retained-r landing",
            ],
        },
        "h0_and_restriction": {
            "relative_presentation_rank": relative_rank,
            "relative_H0_dimension": 5 - relative_rank,
            "after_one_total_E_T_rank": with_total_rank,
            "after_one_total_E_T_H0_dimension": 5 - with_total_rank,
            "after_split_tB_tC_rank": with_split_rank,
            "after_split_tB_tC_H0_dimension": 5 - with_split_rank,
            "meaning": (
                "one absolute total carrier kills exactly the balanced carrier "
                "class; it is an attachment, not a presentation-safe rewrite"
            ),
            "canonical_restriction": "zero switch boundary; old chart H0 dimension 2",
            "raw_restriction": "B-A and C-A but chart H0 dimension 0",
            "relative_U": "dU=H-r leaves one H0 class per C4 block",
            "absolute_U": "dU=H kills that H0 class",
        },
        "pp_faces": {
            "total": 36,
            "tail": {"total": 18, "per_chart": tail_faces,
                     "coefficients": coefficients},
            "direction": {"total": 18, "per_chart": direction_faces,
                          "coefficients": coefficients},
            "mixed_reinsertion": "PASS: +x'y'U and -x'y'U cancel termwise",
            "retained_after_relative_C4": retained,
        },
        "obstructions_in_order": [
            {
                "level": 0,
                "name": "balanced chart/operation quotient",
                "dimension": 1,
                "evidence": "rank(B,C)=2; rank(B,C,L01)=3",
                "source_faithful_refinement": (
                    "fixed-window rank 46; first switch family gives 47; "
                    "second switch family gives 48"
                ),
            },
            {
                "level": 1,
                "name": "face-complete retained-r/common-core quotient",
                "dimension": 1,
                "evidence": (
                    "rank(F_A0,F_A1,F_B0,F_B1)=3; adjoining core gives 4; "
                    "eta=(1,-1/2,-1/2,-1/2,-1/2) reads core as 1"
                ),
                "representative": retained,
            },
            {
                "level": 2,
                "name": "root-labelled cap-Eq complement",
                "dimension": "not collapsed here",
                "evidence": (
                    "after formally granting all four DQ/PS mates, 66 literal "
                    "neither-a-nor-b terms remain for each of AB and AC"
                ),
            },
        ],
        "minimal_extension": {
            "single_total_cell_form": (
                "one source-labelled total Lambda_01 with leading boundary L01, "
                "fixed-window PP corrections, and no extra descendants; then "
                "E_T=Gamma_B+Gamma_C-Lambda_01"
            ),
            "constructor_level_requirements": [
                "both fixed-window DQ<->PS switch families",
                "the selected tail carriers for all 18 tail faces",
                "relative C4 reinsertion in all three blocks",
                "one covariant Pi_r with dPi_r=-(retained_after_relative_C4)",
            ],
            "downstream_X23_guard": (
                "deploying this carrier as the AB/AC EqSystem-to-AugP2 map "
                "additionally requires separately root-labelled 66-term "
                "cap-Eq complements; that is not part of the standalone "
                "equation dE_T=T"
            ),
            "smallest_next_generator": (
                "Pi_r,01 in the one-dimensional retained-face quotient with "
                "dPi_r,01=2*((dD)q01+D(dq01))*r_DQ "
                "-((dp0)s1+p0(ds1))*r_PS01 "
                "-((dp1)s0+p1(ds0))*r_PS10"
            ),
        },
        "covariance": {
            "tau_a": "balanced K2,2 character -1",
            "tau_b": "balanced K2,2 character -1",
            "cut_sigma": "fixes the symmetric three-tail H as a set",
            "required_new_cell_character": "tau-anti-equivariant and cut-sigma covariant",
            "AB_AC": (
                "must be two literal root-labelled copies related by root relabelling; "
                "no cross-root cancellation is allowed"
            ),
            "physical_verdict": (
                "UNTYPED until Lambda_01/Pi_r is supplied as a source column; "
                "coefficient covariance is only a necessary guard"
            ),
        },
        "promotion": "NONE_H3_ONLY",
        "verdict": (
            "No explicit E_T can be constructed from the pinned source-labelled "
            "chains.  E_T is exactly equivalent to the unresolved balanced L01 "
            "total filler.  The earliest chart quotient is one-dimensional and "
            "requires both operation-switch families.  Even after their formal "
            "grant and exact relative-C4 reinsertion, a second one-dimensional "
            "face-complete quotient survives on r_DQ/r_PS, detected by eta."
        ),
    }
    logical = sha256(json.dumps(result, sort_keys=True, separators=(",", ":"))
                     .encode()).hexdigest()
    return {"logical_sha256": logical, "result": result}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    wrapped = audit()
    encoded = json.dumps(wrapped, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()

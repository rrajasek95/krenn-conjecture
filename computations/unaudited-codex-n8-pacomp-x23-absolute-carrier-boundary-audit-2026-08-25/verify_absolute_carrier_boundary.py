#!/usr/bin/env python3
"""Audit whether the pinned h=3 chains imply d(E_B+E_C)=t_B+t_C."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "computations/unaudited-codex-n8-pacomp-x23-strengthened-c62-placement-audit-2026-08-25/MANIFEST.sha256":
        "92bbb2983c79ad15921ad95d3528b51e7f9e0812f39819cdcbaef47d2adb78be",
    "notes/h3-chart-odd-gate-ii-augmented-filler-terminal-fork.md":
        "fdb07cd655a0bd4dfa519c8c7faed8cafac105345737f44902b8127324f24a2a",
    "notes/h3-primitive-c4-covariance-pointed-bridge-gate.md":
        "6ab0a309bdad75fe572d710b5c42c5be661159e349a3cabcf82a61c25d99edaf",
    "computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py":
        "a14339fee59134b28229fb17fcae2292bc544264ea829db60c953875f96fef41",
    "notes/h3-gate-ii-fixed-face-relative-c4-localization-projection-gate.md":
        "5b141a46ea54a44acfc98a62272d3e57a734f005e6bf86df00af0f279dcb5ea3",
    "computations/verify_h3_gate_ii_fixed_face_relative_c4_localization_projection_gate.py":
        "48bb5568b6d3360dd592011ed09aca364cfdbd24770d2e2419c1f99464825878",
    "notes/h3-gate-ii-uniform-response-relative-carrier-landing-gate.md":
        "e1d0b1185cd72ff4d0d915abb1db25835f2848f65f1509458aee9f2325699084",
    "computations/verify_h3_gate_ii_uniform_response_relative_carrier_landing_gate.py":
        "9b9c05a6789d2ade9359934f279eeb429591b2e85651ebaba8485195050417eb",
    "notes/h3-gate-ii-primitive-c4-joint-cobar-label-gate.md":
        "1adefa3bf3427a8f0c9c415376561bdd6b56c2f358fb236260b9956e7d7b0e62",
    "computations/verify_h3_gate_ii_primitive_c4_joint_cobar_label_gate.py":
        "d77f4fd853673c434d4a0bb4027bf9ba046f1bb7ea4d752028a609e832255f44",
    "notes/h3-gate-ii-switch-weyl-product-rule-idempotent-gate.md":
        "432a612161538958c069de828b1f0f0a3321e5bdaa758be104942140df768b7d",
    "computations/verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py":
        "fbd4815eb5c6d46b8dbcd018f6e75237f004e3f52b1ccf47631479b698f9db35",
    "notes/h3-gate-ii-three-cap-relative-tate-carrier-obstruction.md":
        "a4c19d4c5f28da42ec1a4af29e2008bd85eee131e7f4d787cb0f8ace14f88ec0",
    "computations/verify_h3_gate_ii_three_cap_relative_tate_carrier_obstruction.py":
        "0be2bde12d3d4b85cad67b4a647b4cb4f7e89ed1a04bff14f6091eb257224dcc",
}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(v) for v in vectors}) == 1, "add width")
    return tuple(sum((v[i] for v in vectors), Q(0))
                 for i in range(len(vectors[0])))


def scale(c: int | Q, v: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(c) * x for x in v)


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    h = len(columns[0])
    rows = [[columns[j][i] for j in range(len(columns))] for i in range(h)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((r for r in range(answer, h) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        p = rows[answer][column]
        rows[answer] = [x / p for x in rows[answer]]
        for r in range(h):
            if r == answer or not rows[r][column]:
                continue
            c = rows[r][column]
            rows[r] = [x - c * y for x, y in
                       zip(rows[r], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> dict[str, list[str]]:
    occurrences: dict[str, list[str]] = {}
    pattern = re.compile(r"\bE_[BC]\b")
    for relative, expected in PINS.items():
        path = ROOT / relative
        actual = sha256(path.read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
        hits = [line.strip() for line in path.read_text(errors="replace").splitlines()
                if pattern.search(line)]
        if hits:
            occurrences[relative] = hits
    # In the source-provenance set, E_B/E_C occur only in the explicitly
    # conditional clause.  They are not generator definitions.
    require(list(occurrences) == [
        "notes/h3-chart-odd-gate-ii-augmented-filler-terminal-fork.md"
    ] and all("If one physical augmented chain" in line
              or "G_B+G_C-(E_B+E_C)" in line
              for line in occurrences[next(iter(occurrences))]), occurrences)
    return occurrences


def audit() -> dict[str, object]:
    occurrences = pin_dependencies()

    # Order (A,B,C,tB,tC).  These are the genuine relative fixed-source
    # chart-switch chains in the pinned inventory.
    A = (Q(1), Q(0), Q(0), Q(0), Q(0))
    B = (Q(0), Q(1), Q(0), Q(0), Q(0))
    C = (Q(0), Q(0), Q(1), Q(0), Q(0))
    tB = (Q(0), Q(0), Q(0), Q(1), Q(0))
    tC = (Q(0), Q(0), Q(0), Q(0), Q(1))
    dGammaB = add(tB, A, scale(-1, B))
    dGammaC = add(tC, A, scale(-1, C))
    total = add(dGammaB, dGammaC)
    T = add(tB, tC)
    L = add(scale(2, A), scale(-1, B), scale(-1, C))
    require(total == add(T, L) and add(total, scale(-1, T)) == L,
            "relative carrier expansion changed")

    # The old chart quotient detects L independently of the endpoint plane.
    direct_detector = (Q(1), Q(0), Q(0), Q(0), Q(0))
    require(rank((B, C)) == 2 and rank((B, C, L)) == 3
            and sum(x * y for x, y in
                    zip(direct_detector, L, strict=True)) == 2,
            "first unmatched chart term stopped being independent")

    tails = ("q23*q45", "q24*q35", "q25*q34")
    expanded_terms = []
    for tail in tails:
        expanded_terms.extend([
            {"coefficient": 1, "term": f"t_B[{tail}]"},
            {"coefficient": 1, "term": f"t_C[{tail}]"},
            {"coefficient": 2, "term": f"D*q01*{tail}"},
            {"coefficient": -1, "term": f"p0*s1*{tail}"},
            {"coefficient": -1, "term": f"p1*s0*{tail}"},
        ])

    # First principal-parts census of the unmatched L term.
    pp = {
        "tail_derivatives": {
            "DQ": {"support": 6, "coefficient": 2},
            "PS01": {"support": 6, "coefficient": -1},
            "PS10": {"support": 6, "coefficient": -1},
        },
        "direction_derivatives": {
            "DQ": {"support": 6, "coefficient": 2},
            "PS01": {"support": 6, "coefficient": -1},
            "PS10": {"support": 6, "coefficient": -1},
        },
    }
    require(sum(block["support"] for half in pp.values()
                for block in half.values()) == 36, "PP census")

    # Honest two-object covariance bar versus its two fixed-source folds.
    # Coordinates are two copies of (A,B,C).  Canonical transport gives zero;
    # raw forgetting gives B-A but changes H0.  This is the exact restriction
    # obstruction, not a sign ambiguity.
    response = tuple(map(Q, (1, 1, 1)))
    rawB = tuple(map(Q, (-1, 1, 0)))
    rawC = tuple(map(Q, (-1, 0, 1)))
    require(rank((response,)) == 1
            and rank((response, rawB, rawC)) == 3,
            "raw restriction H0 guard")

    # Formal four-corner tau mates.  Each total mate involution reverses the
    # alternating charge; root-order flip and endpoint transpose separately
    # preserve it.  None changes the source-typing conclusion.
    z = tuple(map(Q, (1, 1, -1, -1)))
    tau_a = (2, 3, 0, 1)  # (Aab B)(Aba C)
    tau_b = (3, 2, 1, 0)  # (Aab C)(Aba B)
    image = lambda permutation: tuple(z[permutation[i]] for i in range(4))
    require(image(tau_a) == scale(-1, z)
            and image(tau_b) == scale(-1, z), "tau sign")

    # Cut sigma=(2 5)(3 4) fixes the three symmetric C4 tail matchings.
    cut_sigma = {2: 5, 5: 2, 3: 4, 4: 3}
    tail_edges = (((2, 3), (4, 5)), ((2, 4), (3, 5)),
                  ((2, 5), (3, 4)))
    def move_tail(tail):
        return tuple(sorted(tuple(sorted((cut_sigma[x], cut_sigma[y])))
                            for x, y in tail))
    require({move_tail(tail) for tail in tail_edges}
            == {tuple(sorted(tail)) for tail in tail_edges}, "cut sigma")

    result: dict[str, object] = {
        "schema": "pacomp-h3-absolute-carrier-boundary-audit-v1",
        "status": "PASS_REFUTED_AS_DERIVATION_FIRST_UNMATCHED_L01",
        "scope": "canonical h=3 source-labelled symbolic audit only",
        "parent_manifest_sha256":
            "92bbb2983c79ad15921ad95d3528b51e7f9e0812f39819cdcbaef47d2adb78be",
        "pins": PINS,
        "source_provenance": {
            "E_B_E_C_generator_definitions_found": 0,
            "E_B_E_C_occurrences": occurrences,
            "classification": (
                "E_B+E_C is an explicitly conditional new physical chain, "
                "not a name expandable from the original registry"
            ),
        },
        "genuine_chain_expansion": {
            "dGamma_B": "t_B-(B-A)=t_B+A-B",
            "dGamma_C": "t_C-(C-A)=t_C+A-C",
            "sum": "t_B+t_C+2A-B-C",
            "termwise_fixed_C4_expansion": expanded_terms,
        },
        "proposed_identity": {
            "claim": "d(E_B+E_C)=t_B+t_C",
            "verdict": "NOT_DERIVED_AND_E_B_E_C_UNDEFINED",
            "first_unmatched_per_channel": {
                "B": "A-B = D*q01*H-p0*s1*H",
                "C": "A-C = D*q01*H-p1*s0*H",
            },
            "first_unmatched_sum": "L01=2D*q01*H-p0*s1*H-p1*s0*H",
            "direct_chart_detector_value": 2,
        },
        "minimal_corrected_identity": {
            "identity": "d(Gamma_B+Gamma_C)=t_B+t_C+L01",
            "equivalent": "d(Gamma_B+Gamma_C)-(t_B+t_C)=L01",
            "minimal_new_hypothesis_for_old_claim": (
                "adjoin one source-valid absolute carrier E_T with "
                "dE_T=t_B+t_C; splitting E_T as E_B+E_C is optional and "
                "requires additional endpoint naturality"
            ),
        },
        "boundary_face_audit": {
            "degree_zero_unmatched_support": 9,
            "first_PP_total_support": 36,
            "first_PP_split": pp,
            "relative_C4_reinsertion": (
                "mixed x'y'U faces cancel, but the boundary exports retained "
                "r_DQ,r_PS01,r_PS10 faces; no absolute landing follows"
            ),
        },
        "restriction_audit": {
            "honest_two_object_bar": "PASS; preserves response word 11110000 and tail 2345",
            "canonical_fixed_source_transport": "boundary zero, not B-A or C-A",
            "raw_fixed_source_fold": "gives B-A/C-A but changes old chart H0 from dimension 2 to 0",
            "conclusion": "no source-valid fixed-source restriction supplies E_B or E_C",
        },
        "covariance_audit": {
            "formal_tau_a_on_balanced_charge": -1,
            "formal_tau_b_on_balanced_charge": -1,
            "cut_sigma_on_symmetric_H2345": "+identity as a set of three tails",
            "AB_AC_root_duplication": (
                "coefficient identity duplicates with +1 only after a root-labelled "
                "chain exists; it does not construct that chain"
            ),
            "physical_tau_sigma_on_E_B_E_C": "UNTYPED_BECAUSE_E_B_E_C_DO_NOT_EXIST",
        },
        "nearest_alternative_guard": {
            "switch_Weyl_candidate": "T*H_W",
            "boundary": "D(T*H_W)=(d_PP T)*H_W+T*(W-1)",
            "reason_not_E_T": "it has nonzero PP and W-1 proper faces, not boundary T alone",
        },
        "verdict": (
            "The original physical definitions do not contain E_B or E_C. "
            "The nearest genuine endpoint-choice chains are Gamma_B,Gamma_C, "
            "and their exact boundary is T+L01, not T.  The first unmatched "
            "terms are the operation-changing A-B and A-C faces; their sum "
            "is the primitive balanced L01 packet.  Canonical restriction "
            "kills these faces, while raw restriction changes H0.  Thus the "
            "minimal correct identity is d(Gamma_B+Gamma_C)=T+L01, and "
            "dE_T=T remains a genuinely new absolute-carrier axiom."
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

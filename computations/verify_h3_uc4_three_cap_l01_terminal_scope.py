#!/usr/bin/env python3
"""Audit whether the protected U_C4 signature constructs its own source cell.

It does not.  Capping the lower symmetric C4 tail in the three endpoint
charts produces AH, BH, CH.  Their centered combination has scalar boundary
L01=(2A-B-C)H.  Presentation-safe chart cylinders retain that scalar as the
sum of two graph coordinates.  Complete response rows, coordinate Euler
rows, and one capped DQ section do not contain it.  Hence zero augmented
readouts on the desired lower column do not supply source provenance.

Once a literal same-grade response-to-relative placement is constructed,
the pinned augmented dual theorem is exhaustive: protected filler or
terminal.  It cannot be invoked before that placement.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gate_ii_chiw_chart_complete_h2_face.py":
        "a80e5ec2a1aaa90814b412d13b1c7981f345bb41ca5a5450d5361ae2bc9f5773",
    "notes/h3-gate-ii-chiw-chart-complete-h2-face.md":
        "95fcde72841aa4b859ffa0711fb30149cd9d3406ad44dcba228445f0023c5505",
    "computations/verify_h3_h2_chart_scalar_capped_c4_augmented_gate.py":
        "18cb73805ffca0a080bc061c88cb42f6c0c83d57efd60c574455b757009785b4",
    "notes/h3-h2-chart-scalar-capped-c4-augmented-gate.md":
        "baee4965bcb9315fc7e9f51693aebcf3cfb6c8a147c76144eb287f7c9c74c998",
    "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py":
        "59babf6e706973f2eaa8a8fdd7cdb624ddf88560c08243c5fcd05c3a5425a5d7",
    "notes/h3-h2-l01-three-cap-first-pp-curvature-gate.md":
        "d43b196a448045b9cf40a9537e5a30d9aad658a9c8636047052a023b45c4db7f",
    "computations/verify_h3_h2_c4_trivial_tag_euler_scalar_face_gate.py":
        "47378f8ce904021bb802e0e4fd59de1591f0cd7333e1fcbc645e62cf40deb499",
    "notes/h3-h2-c4-trivial-tag-euler-scalar-face-gate.md":
        "3d16b7a1b77030eaaa5ba3fc342b927a7ee750db2c4f8091868591acc261477f",
    "computations/verify_h3_h2_full_site_chart_swap_pointed_scalar_guard.py":
        "bc35781e0f57bbd1202711e2dc818417d76fa87c69e33d3d4b01540e06865557",
    "notes/h3-h2-full-site-chart-swap-pointed-scalar-guard.md":
        "77771f8eee2a4bbaeb5a9575961efb9c7728833e28bca86d33102806aeffa6c2",
    "computations/verify_h3_h2_fixed_chart_l01_reset_augmented_gate.py":
        "6acd2eec727e1030c58d14da6a2c8b26f884bb0ed5ada02b904c5e4c54d6ca6f",
    "notes/h3-h2-fixed-chart-l01-reset-augmented-gate.md":
        "110e850f43b4520a5a47e53d74f190ae7012547ff87d27da1e27ba4c5568f701",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
    "notes/h3-o2-augmented-terminal-cap-cartan-extension-gate.md":
        "e9c0cf3c76cbe4c8061574d2b977bf1189a1fa299ef17ae1d2e463c08a313429",
}
EXPECTED_LEDGER_SHA256 = "8f02780b3d170cb7dd04db1b8e95b925b18b494c95211decea5a19bd838902a0"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((index for index in range(pivot_row, len(work))
                      if work[index][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for index in range(len(work)):
            if index == pivot_row or not work[index][column]:
                continue
            value = work[index][column]
            work[index] = [left - value * right for left, right in
                           zip(work[index], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((min(first, second), max(first, second)),)
                               + tail))


def edge(left, right):
    return (min(left, right), max(left, right))


P, S = 6, 7


def matching(*edges):
    return tuple(sorted(edge(left, right) for left, right in edges))


def occurrence_audit() -> dict[str, object]:
    matchings = tuple(sorted(set(perfect_matchings(range(8)))))
    require(len(matchings) == 105, len(matchings))
    index = {value: position for position, value in enumerate(matchings)}
    all_edges = tuple((left, right) for left in range(8)
                      for right in range(left + 1, 8))
    incidence = [tuple(int(edge_value in value) for value in matchings)
                 for edge_value in all_edges]
    complete = (1,) * len(matchings)

    residuals = (((2, 3), (4, 5)),
                 ((2, 4), (3, 5)),
                 ((2, 5), (3, 4)))
    chart_edges = {
        "A": ((P, S), (0, 1)),
        "B": ((P, 0), (S, 1)),
        "C": ((P, 1), (S, 0)),
    }
    chart_vectors = {}
    for name, prefix in chart_edges.items():
        vector = [0] * len(matchings)
        for tail in residuals:
            vector[index[matching(*(prefix + tail))]] = 1
        chart_vectors[name] = tuple(vector)
    a_vec, b_vec, c_vec = (chart_vectors[name] for name in "ABC")
    l01 = tuple(2 * a - b - c for a, b, c in
                zip(a_vec, b_vec, c_vec, strict=True))
    r01 = tuple(a + b + c for a, b, c in
                zip(a_vec, b_vec, c_vec, strict=True))
    r_rest = tuple(left - right for left, right in
                   zip(complete, r01, strict=True))
    require(sum(a_vec) == sum(b_vec) == sum(c_vec) == 3
            and sum(l01) == 0 and sum(r01) == 9
            and sum(r_rest) == 96
            and rank(incidence) == 21
            and rank(incidence + [complete]) == 21
            and rank(incidence + [l01]) == 22,
            "the K8 response/Euler ranks changed")

    # The twelve-term exact separator from the fixed-chart audit.
    signed = (
        (1, matching((P, S), (0, 1), (2, 3), (4, 5))),
        (-1, matching((P, S), (0, 3), (1, 4), (2, 5))),
        (-1, matching((P, S), (0, 5), (1, 2), (3, 4))),
        (1, matching((P, S), (0, 5), (1, 4), (2, 3))),
        (-1, matching((P, 0), (S, 1), (2, 3), (4, 5))),
        (1, matching((P, 0), (S, 1), (2, 5), (3, 4))),
        (-1, matching((P, 0), (S, 2), (1, 3), (4, 5))),
        (1, matching((P, 0), (S, 3), (1, 2), (4, 5))),
        (-1, matching((P, 1), (S, 0), (2, 3), (4, 5))),
        (1, matching((P, 1), (S, 2), (0, 3), (4, 5))),
        (1, matching((P, 2), (S, 0), (1, 3), (4, 5))),
        (-1, matching((P, 2), (S, 3), (0, 1), (4, 5))),
    )
    psi = [Q(0)] * len(matchings)
    for numerator, value in signed:
        psi[index[value]] += Q(numerator, 3)
    require(all(dot(psi, row) == 0 for row in incidence)
            and dot(psi, complete) == 0
            and dot(psi, l01) == 1,
            "the literal L01 Euler separator changed")

    # A lower symmetric U has normalized tail augmentation one.  Capping it
    # separately by A,B,C gives these three occurrence vectors.  The
    # centered cap is L01, not zero.
    require(tuple(2 * a - b - c for a, b, c in
                  zip(a_vec, b_vec, c_vec, strict=True)) == l01,
            "the centered three-cap boundary changed")
    return {
        "complete_response_occurrences": 105,
        "local_three_cap_occurrences": 9,
        "outside_occurrences": 96,
        "lower_H_raw_augmentation": 3,
        "lower_H_normalized_augmentation": 1,
        "centered_top_augmentation": sum(l01),
        "incidence_rank": rank(incidence),
        "incidence_plus_complete_rank": rank(incidence + [complete]),
        "incidence_plus_L01_rank": rank(incidence + [l01]),
        "separator_values": {
            "all_coordinate_Euler_rows": 0,
            "complete_response": int(dot(psi, complete)),
            "L01": int(dot(psi, l01)),
        },
        "three_cap_identity": "2(A cap U)-B cap U-C cap U has boundary L01",
    }


def chart_graph_audit() -> dict[str, object]:
    # Coordinates A,B,C,u1,u2.  The presentation-safe graph relations retain
    # u1 and u2; raw folding is obtained only by setting them to zero.
    response = (1, 1, 1, 0, 0)
    graph_b = (-1, 1, 0, -1, 0)
    graph_c = (-1, 0, 1, 0, -1)
    l01 = (2, -1, -1, 0, 0)
    retained = (0, 0, 0, -1, -1)
    combination = tuple(-left - right + tail for left, right, tail in
                        zip(graph_b, graph_c, retained, strict=True))
    require(combination == l01
            and rank((response, graph_b, graph_c)) == 3
            and rank((response[:3], graph_b[:3], graph_c[:3])) == 3,
            "the pointed chart graph identity changed")
    return {
        "coordinates": ["A", "B", "C", "u1", "u2"],
        "relations": [list(response), list(graph_b), list(graph_c)],
        "identity": "L01=-(graph_B+graph_C)-(u1+u2)",
        "quotient_identity": "[L01]=-[u1+u2]",
        "graph_quotient_dimension": 2,
        "raw_fold_quotient_dimension": 0,
        "setting_u1_u2_zero_is_source_valid": False,
    }


def product(left, right):
    """Bivariate squarefree Hasse product through order (1,1)."""
    return {
        "0": left["0"] * right["0"],
        "x": left["x"] * right["0"] + left["0"] * right["x"],
        "y": left["y"] * right["0"] + left["0"] * right["y"],
        "xy": (left["xy"] * right["0"]
               + left["x"] * right["y"]
               + left["y"] * right["x"]
               + left["0"] * right["xy"]),
    }


def sub(*vectors):
    return {grade: vectors[0][grade] - sum(vector[grade]
                                           for vector in vectors[1:])
            for grade in ("0", "x", "y", "xy")}


def pivot_hasse_audit() -> dict[str, object]:
    # For P=alpha*U-d*V-alpha, the mixed Hasse face contains seven proper
    # product-rule terms besides alpha*U_xy-d*V_xy.  The coloop inverse row
    # alpha*Cc=1 controls only the four alpha/Cc terms and cannot remove the
    # U_x/U_y/V/V_x/V_y companions.
    terms = (
        "alpha*U_xy", "-d*V_xy",
        "alpha_x*U_y", "alpha_y*U_x", "alpha_xy*(U-1)",
        "-d_x*V_y", "-d_y*V_x", "-d_xy*V",
    )
    require(len(terms) == 8 and len(set(terms)) == 8,
            "the differentiated pivot term list changed")

    # Exact integrated redistribution guard.  All complete pivot and coloop
    # identities hold as polynomials in a parameter t, hence every Hasse
    # derivative holds.  The selected occurrence f still moves while g
    # compensates.  Jets are encoded as (0,x,y,xy); only x is used.
    zero = {grade: Q(0) for grade in ("0", "x", "y", "xy")}
    one = dict(zero, **{"0": Q(1)})
    half_plus_t = dict(zero, **{"0": Q(1, 2), "x": Q(1)})
    half_minus_t = dict(zero, **{"0": Q(1, 2), "x": Q(-1)})
    alpha = one
    d = zero
    C = zero
    Cc = one
    U = {grade: half_plus_t[grade] + half_minus_t[grade]
         for grade in zero}
    V = zero
    pivot = sub(product(alpha, U), product(d, V), alpha)
    mixed = sub(product(d, C), one)
    # The first row is d*C+U=1, not d*C-1=0.
    pure_row = {grade: product(d, C)[grade] + U[grade] - one[grade]
                for grade in zero}
    exchange_row = {grade: product(alpha, C)[grade] + V[grade]
                    for grade in zero}
    coloop_row = sub(product(alpha, Cc), one)
    require(all(value == 0 for vector in
                (pivot, pure_row, exchange_row, coloop_row)
                for value in vector.values())
            and half_plus_t["x"] == 1
            and half_minus_t["x"] == -1,
            "the differentiated coloop pivot redistribution guard changed")
    return {
        "pivot": "alpha*U-d*V=alpha",
        "coloop_unit": "alpha*Cc=1",
        "mixed_Hasse_product_rule_terms": list(terms),
        "unit_alpha_removes_leading_denominator": True,
        "unit_alpha_selects_R01_or_one_occurrence": False,
        "coloop_inverse_cancels_all_proper_faces": False,
        "uncancelled_families": [
            "alpha_x*U_y and alpha_y*U_x",
            "d_x*V_y and d_y*V_x",
            "alpha_xy*(U-1) and d_xy*V",
            "the occurrence-block redistribution inside U or V",
        ],
        "integrated_guard": {
            "alpha,d,C,Cc,U,V": [1, 0, 0, 1, 1, 0],
            "occurrences": "f=1/2+t, g=1/2-t, U=f+g",
            "all_complete_and_coloop_Hasse_jets": 0,
            "selected_df": 1,
        },
        "consequence": (
            "even the full differentiated pivot does not supply the selected "
            "R01 projector; a chart/Hasse operator can cap U_C4 only together "
            "with the retained product-rule and occurrence-redistribution faces"
        ),
    }


def augmented_scope_audit() -> dict[str, object]:
    lower_signature = {
        "occurrence_augmentation": 1,
        "target": 0,
        "ainc": 0,
        "q=M-a": 0,
        "Eq": 0,
        "W": 0,
        "ordinary_residue": 0,
        "shifted_ridge": 0,
    }
    return {
        "desired_U_C4_signature": lower_signature,
        "signature_implies_domain_source_provenance": False,
        "reason": (
            "cap/reinsertion obeys Leibniz; dD and dq01 proper faces and the "
            "pointed scalar L01 are not values of the lower augmented rows"
        ),
        "first_remaining_face": {
            "name": "L01",
            "literal_grade": (
                "parent response word/fine/repeated grade with the coupled "
                "Hasse[2](DQ,PS,PS) chart tags retained"
            ),
            "occurrence_augmentation": 0,
            "target": 0,
            "ainc/q/Eq/W/residue/ridge": (
                "undefined until a source-labelled physical placement"
            ),
        },
        "terminal_fork": {
            "after_literal_same_grade_placement": [
                "protected-zero physical filler",
                "augmented terminal",
            ],
            "before_placement": "not applicable",
            "dual_extension": (
                "q=ainc=Eq=0; target_j=W_j=-mu_j; ores_j=mu_j; "
                "ridge=-sum alpha_j*mu_j"
            ),
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 U_C4 three-cap source-provenance and L01 terminal scope",
        "pins": PINS,
        "complete_occurrence_and_Euler_test": occurrence_audit(),
        "presentation_safe_chart_graph": chart_graph_audit(),
        "differentiated_coloop_pivot": pivot_hasse_audit(),
        "augmented_and_terminal_scope": augmented_scope_audit(),
        "verdict": (
            "The zero augmented signature and normalized augmentation-one "
            "tail of U_C4 do not make it a source cell.  Capping the lower "
            "H by A,B,C and taking the required centered combination leaves "
            "the nonzero pointed scalar L01.  Complete response and all "
            "constant coordinate Euler rows miss L01, with an exact twelve-"
            "occurrence separator.  Presentation-safe chart swaps retain "
            "L01=-(u1+u2)H rather than killing it.  A covariant physical "
            "three-cap family would construct L01, but its existence is "
            "equivalent to the missing placement, not a consequence of the "
            "lower U_C4 signature.  The augmented filler-or-terminal theorem "
            "is exhaustive only after that same-grade placement."
        ),
        "shortest_remaining_theorem": (
            "construct one source-labelled covariant three-cap/endpoint-even "
            "C+ totalization whose centered boundary is L01 and whose first "
            "PP faces retain the literal word/fine/repeated, q, anchor, W, "
            "ridge and eta/sigma data; then the pinned augmented dual theorem "
            "closes by filler or terminal"
        ),
        "scope": (
            "exact h3 K8 occurrence, Euler, chart-graph, coefficient and "
            "terminal-scope audit.  It does not exclude higher non-diagonal "
            "Spencer cells outside the named chart/Euler/three-cap interface."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("U_C4 three-cap ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("U_C4 lower signature: DOES NOT SUPPLY SOURCE PROVENANCE")
    print("centered three-cap boundary: L01")
    print("complete response + coordinate Euler: MISS L01")
    print("presentation-safe chart graph: RETAINS -(u1+u2)H")
    print("same-grade augmented fork: CONDITIONAL ON PHYSICAL PLACEMENT")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

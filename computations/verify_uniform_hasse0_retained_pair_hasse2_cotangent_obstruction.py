#!/usr/bin/env python3
"""Locate the cotangent obstruction to Hasse[0] -> retained Hasse[2].

Let R be the complete response hafnian on 2h+2 augmented vertices and let
a,b be two disjoint retained direction edges.  The desired lower packet is

    H_ab = D_a D_b R = Haf(R on the complement of a union b).

For the mixed GHZ source A=P/(R), coordinate differentiation does not
descend to A.  Even after the first directions are made tangent, the mixed
Hasse--Schmidt equation is

    J_R zeta + H_R(xi,eta) = 0.

For the coordinate retained pair, H_ab has degree h-1, whereas every
Jacobian generator has degree h and R has degree h+1.  Hence H_ab gives a
nonzero class in T^1_A=P/(R,J_R).  A singular specialization with one
complement matching equal to one has R=0, J_R=0 and H_ab=1, so no global
source-valid correction can exist in the old principal-parts complex.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_chart_switch_word_target_affine_gate.py":
        "c0f0eb10c26816d7ad7033fc22f8d8ff8fe45a9825ef9e158dfe8d739db409a4",
    "notes/uniform-chart-switch-word-target-affine-gate.md":
        "edb1083524d65036b374af26be47d29bd6493f7f086fe744d25865f4e1c046ab",
    "computations/audit_h3_augmented_hasse_schmidt_separation_independent.py":
        "df5e126fa895408fe763d39f619d0cf3ea640b3cb4cde72d72191b8e9f44c274",
    "notes/h3-augmented-hasse-schmidt-separation-independent-audit.md":
        "682a2ec3564a7855a22f5fd90530fdc12f2837db969621027d20345256a1fb5a",
    "computations/verify_uniform_response_h2_full_site_tag_contraction.py":
        "5709b5ba93e775d372e5caa5ba33b0c1e168177d9866ff52137245db3f1dc1c0",
    "notes/uniform-response-h2-full-site-tag-contraction.md":
        "6f83f12b94ac14db9ee4c6599ac05cbabfce7cd2a817fd2f2cc84bc7adf621ca",
    "computations/verify_reciprocal_response_hasse_bianchi.py":
        "d5bb78f9a0ca2cfab30932ccfcaeca8c6de9d3bff5351983045e66fee4d1d432",
}
EXPECTED_LEDGER_SHA256 = (
    "1dede0b06ac71b28c956bb7a292a4e8dddbd59914ef79141ababa7e7a5db1e4e"
)

Edge = tuple[int, int]
Monomial = tuple[Edge, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left: int, right: int) -> Edge:
    return tuple(sorted((left, right)))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


def odd_double_factorial(value: int) -> int:
    require(value >= -1 and value % 2 == 1, value)
    return 1 if value <= 0 else math.prod(range(1, value + 1, 2))


def hasse_derivative(monomials: tuple[Monomial, ...],
                     directions: tuple[Edge, ...]) -> tuple[Monomial, ...]:
    require(len(set(directions)) == len(directions), directions)
    answer = []
    for monomial in monomials:
        if not all(direction in monomial for direction in directions):
            continue
        remainder = list(monomial)
        for direction in directions:
            remainder.remove(direction)
        answer.append(tuple(remainder))
    return tuple(sorted(answer))


def evaluate(monomials: tuple[Monomial, ...], values: dict[Edge, Q]) -> Q:
    answer = Q(0)
    for monomial in monomials:
        product = Q(1)
        for value in monomial:
            product *= values.get(value, Q(0))
        answer += product
    return answer


def audit_order(h: int) -> dict[str, object]:
    require(h >= 2, h)
    vertices = tuple(range(2 * h + 2))
    a, b = edge(0, 1), edge(2, 3)
    response = tuple(perfect_matchings(vertices))
    d_a = hasse_derivative(response, (a,))
    d_b = hasse_derivative(response, (b,))
    h_ab = hasse_derivative(response, (a, b))
    h_ba = hasse_derivative(response, (b, a))
    require(h_ab == h_ba, "mixed Hasse derivatives stopped commuting")

    require(len(response) == odd_double_factorial(2 * h + 1)
            and len(d_a) == len(d_b) == odd_double_factorial(2 * h - 1)
            and len(h_ab) == odd_double_factorial(2 * h - 3),
            (h, len(response), len(d_a), len(h_ab)))
    require({len(value) for value in response} == {h + 1}
            and {len(value) for value in d_a + d_b} == {h}
            and {len(value) for value in h_ab} == {h - 1},
            "a Hasse polynomial degree changed")

    # Singular retained-pair guard: choose one complement matching and set
    # exactly its h-1 edges to one.  There are too few nonzero edges for R
    # or any first cofactor, while H_ab contains this matching once.
    tail = h_ab[0]
    values = {value: Q(1) for value in tail}
    response_value = evaluate(response, values)
    gradient_values = {}
    all_edges = tuple(edge(left, right) for left in vertices
                      for right in vertices if left < right)
    for direction in all_edges:
        gradient_values[direction] = evaluate(
            hasse_derivative(response, (direction,)), values
        )
    h_value = evaluate(h_ab, values)
    require(response_value == 0
            and set(gradient_values.values()) == {Q(0)}
            and h_value == 1,
            (h, response_value, Counter(gradient_values.values()), h_value))

    # The homogeneous ideal (R,J_R) is generated in degrees h+1 and h.
    # Its component in degree h-1 is zero, while H_ab is nonzero.
    require(h - 1 < h < h + 1 and h_ab,
            "the homogeneous T1 degree separator disappeared")
    return {
        "h": h,
        "augmented_vertices": len(vertices),
        "response_degree": h + 1,
        "response_terms": len(response),
        "first_Jacobian_degree": h,
        "one_first_Hasse_terms": len(d_a),
        "retained_pair": [list(a), list(b)],
        "retained_Hasse2_degree": h - 1,
        "retained_Hasse2_terms": len(h_ab),
        "mixed_Hasse_normalization": 1,
        "H_ab_equals_H_ba": True,
        "T1_degree_separator": (
            f"degree {h - 1} H_ab is nonzero; ideal (R,J_R) has no "
            f"nonzero component below degree {h}"
        ),
        "singular_guard": {
            "nonzero_edges": [list(value) for value in tail],
            "R": str(response_value),
            "all_first_Hasse_values": "0",
            "H_ab": str(h_value),
            "Jacobian_rank": 0,
            "rank_after_H_ab": 1,
        },
    }


def mixed_jet_and_principal_parts_audit() -> dict[str, object]:
    # In Q[eps,delta]/(eps^2,delta^2), the mixed coefficient for
    # x'=x+eps*xi+delta*eta+eps*delta*zeta is J*zeta+H(xi,eta), with no 2.
    j = (Q(2), Q(-3), Q(5))
    zeta = (Q(7), Q(1, 2), Q(-4))
    hessian_value = Q(11, 3)
    mixed = sum(left * right for left, right in zip(j, zeta)) + hessian_value
    require(mixed == Q(-23, 6), mixed)

    # On a Jacobian chart J_c is a unit, solve the mixed equation.  This is
    # only valid after the first directions are tangent and uses a normal
    # acceleration; it does not make H itself a source equation.
    j_c, h_value = Q(5, 2), Q(7, 3)
    z_c = -h_value / j_c
    require(j_c * z_c + h_value == 0 and z_c == Q(-14, 15), z_c)
    return {
        "dual_number_ring": "Q[eps,delta]/(eps^2,delta^2)",
        "source_two_jet": "x+eps*xi+delta*eta+eps*delta*zeta",
        "first_equations": ["J xi=0", "J eta=0"],
        "mixed_equation": "J zeta + Hess_R(xi,eta)=0",
        "mixed_Hasse_coefficient": 1,
        "existence_criterion": "-[Hess_R(xi,eta)] lies in im J",
        "protected_criterion": (
            "with allowed correction map a:L->T_source, replace im J by im(Ja)"
        ),
        "Jacobian_open_local_solution": {
            "hypotheses": "first jets already tangent and J_c invertible",
            "formula": "zeta_c=-H/J_c",
            "example": {"J_c": "5/2", "H": "7/3", "zeta_c": "-14/15"},
            "preserves_H0_to_mixed_order": True,
            "makes_H_zero_as_a_separate_equation": False,
        },
        "principal_parts_interpretation": (
            "delta R=0 in P^2_A is one filtered relation.  Extracting the "
            "retained eps*delta coefficient sends it to H_ab; coefficient "
            "extraction is not a map of P^2_A unless the mixed equation is "
            "split by zeta"
        ),
    }


def source_complex_audit() -> dict[str, object]:
    # Cotangent complex of the mixed hypersurface A=P/(R):
    # [A*e_R -> Omega_P tensor A], e_R |-> dR.  Its deformation obstruction
    # T1 is A/J_R.  The retained Hasse class is nonzero there by grading.
    word_gate = (ROOT / "notes/uniform-chart-switch-word-target-affine-gate.md").read_text()
    hasse_gate = (ROOT / "notes/h3-augmented-hasse-schmidt-separation-independent-audit.md").read_text()
    require("mixed target value zero  does not imply  lower Hasse H=0" in word_gate
            and "mixed correction equation" in hasse_gate
            and "there is no factor two" in hasse_gate,
            "a pinned Hasse/source scope statement changed")
    return {
        "mixed_source": "A=P/(R), with mixed GHZ target value zero",
        "cotangent_complex": "[A e_R --dR--> Omega_P tensor A]",
        "deformation_obstruction_module": "T^1_A=A/J_R",
        "retained_pair_class": "[D_a D_b R] in T^1_A",
        "class_nonzero_uniformly": True,
        "coordinate_Hasse_operator_descends_to_A": False,
        "first_order_reason": (
            "D_a R has degree h and is nonzero, hence is not in the "
            "principal ideal (R) generated in degree h+1"
        ),
        "second_order_reason_after_tangency": (
            "D_aD_b R has a nonzero degree h-1 class modulo the degree-h "
            "Jacobian ideal"
        ),
        "old_PP_complex_contains_H_as_zero_row": False,
        "what_the_old_PP_complex_contains": (
            "the coupled mixed equation J*zeta+H=0; on a singular guard "
            "J=0 and H=1, so even the coupled equation has no filler"
        ),
        "minimal_enlargement": (
            "either restrict to a Jacobian-open chart and retain the normal "
            "acceleration plus all product-rule faces, or adjoin a new Tate/"
            "Spencer generator for the nonzero T1 class; the latter changes "
            "the old derived source unless justified by additional equations"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    orders = tuple(audit_order(h) for h in range(2, 7))
    require(orders[1]["h"] == 3
            and orders[1]["response_terms"] == 105
            and orders[1]["retained_Hasse2_terms"] == 3,
            orders[1])
    ledger = {
        "theorem": "uniform Hasse0 to retained-pair Hasse2 cotangent obstruction",
        "pins": PINS,
        "uniform_orders": orders,
        "mixed_jet_and_PP": mixed_jet_and_principal_parts_audit(),
        "source_complex": source_complex_audit(),
        "verdict": (
            "The needed lower H=0 is not a derivative equation in the old "
            "cotangent/principal-parts complex.  Coordinate Hasse operators "
            "do not descend to A=P/(R).  After tangent first jets are "
            "supplied, the mixed equation is J*zeta+H=0, and H defines a "
            "nonzero class in T1=A/J because deg H=h-1<deg J=h.  The "
            "explicit complement-matching source point has R=J=0,H=1."
        ),
        "shortest_positive_local_theorem": (
            "on a Jacobian open where one admitted normal cofactor J_c is a "
            "unit, and after both first jets are physically tangent, take "
            "zeta_c=-H/J_c and retain its restriction/product-rule faces.  "
            "This preserves H0 through mixed order but expresses H as a "
            "Jacobian boundary; it does not make H a separate coefficient "
            "equation or extend across the singular guard"
        ),
        "scope": (
            "uniform complete response hafnian at h>=2 and a compatible "
            "two-edge retained direction pair in a mixed target-zero word. "
            "This isolates the obstruction from H0 alone; additional full-"
            "source equations could only help by contributing new Jacobian/"
            "Tate columns and must be checked explicitly."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    h3 = ledger["uniform_orders"][1]
    print("h3 response/Hasse2 terms: " +
          str(h3["response_terms"]) + "/" +
          str(h3["retained_Hasse2_terms"]))
    print("mixed jet equation: J*zeta+H=0 (coefficient 1)")
    print("retained H class in T1=A/J: NONZERO BY DEGREE")
    print("singular guard: R=0, J=0, H=1")
    print("global Hasse0 -> Hasse2 algebraization: NO")
    print("Jacobian-open corrected jet: YES, CONDITIONAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

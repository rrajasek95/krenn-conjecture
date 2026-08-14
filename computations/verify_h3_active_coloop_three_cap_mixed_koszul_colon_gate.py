#!/usr/bin/env python3
"""Audit kappa_mix in the active-coloop three-cap algebra.

Work on the literal fixed window with

    A = D*q*H,  B = p*s*H,  C = r*t*H,
    R01 = A+B+C,

and impose the active-coloop relation q*H=1.  Then q and H are units, but
A=D and neither D nor p*s is a unit.  The canonical resolution of the
single hypersurface R01 has one odd Koszul generator and no pairwise
DQ/PS two-cell.  A pairwise cell appears only after replacing the one
equation by the three-equation ideal (A,B,C), which changes H0.

Before localization, the common H factor does create the familiar Tor line
for the pair (H*D*q,H*p*s): it is supported on H=0.  Since H is a unit on
the active-coloop chart, that Tor line vanishes there.  Thus using it after
localization is exactly saturation, not a new physical source cell.

The formal split Koszul cell has all product-rule faces recorded here, but
its canonical B/Eq projection is dark.  The active relation does not fix a
mixed-cell augmentation; a bright delta component remains extra physical
cap/descent data.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py":
        "c0c6c075388a2eb2d5dad6d133166a3f211dd268183d3e2a5433d922e2ea8ceb",
    "computations/verify_h3_cross_word_mapping_cylinder_d2_augmentation_freedom_gate.py":
        "3704235f1030a07556aaebed3225bec8ea0fb9fa4d6a4d3aa124a7727a3bebec",
    "computations/verify_h3_four_site_full_source_exhaustiveness_decomposition_gate.py":
        "269a1b775e0790c3e4f1f6390b83673c1118270e491885ce9383e703f07b3278",
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "computations/verify_h3_generic_symmetric_c4_core_saturation_tor_gate.py":
        "7307cb245996376f9847ff4852a4fdcd0a774152b4011ed92822022f93af03e5",
    "notes/h3-hyperbolic-root-collision-tate-cobar-totalization-gate.md":
        "673722b62a59f10b00aa20796236146df052a4d45eda0764053737bca401e95a",
    "notes/h3-cross-word-mapping-cylinder-d2-augmentation-freedom-gate.md":
        "ef33bdd1f600fb3f58e91ca191a2fcfcfab516d5680907661a006ca5d358cec0",
}
EXPECTED_LEDGER_SHA256 = "d1e697f5a173c5056c6460c2ae5e71139f8c3413fe61f9aed60d24099908b216"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


# Laurent polynomials over Q in q,D,p,s,r,t.  H is represented by q^-1.
VARIABLES = ("q", "D", "p", "s", "r", "t")
Monomial = tuple[int, ...]
Poly = dict[Monomial, Q]


def polynomial(*terms: tuple[Q | int, Monomial]) -> Poly:
    answer: Poly = {}
    for coefficient, monomial in terms:
        value = answer.get(monomial, Q(0)) + Q(coefficient)
        if value:
            answer[monomial] = value
        else:
            answer.pop(monomial, None)
    return answer


def variable(name: str, exponent: int = 1) -> Poly:
    index = VARIABLES.index(name)
    monomial = [0] * len(VARIABLES)
    monomial[index] = exponent
    return polynomial((1, tuple(monomial)))


ONE = polynomial((1, (0,) * len(VARIABLES)))


def add(*values: Poly) -> Poly:
    return polynomial(*(item for value in values for item in
                        ((coefficient, monomial)
                         for monomial, coefficient in value.items())))


def scale(coefficient: Q | int, value: Poly) -> Poly:
    return polynomial(*((Q(coefficient) * scalar, monomial)
                        for monomial, scalar in value.items()))


def multiply(*values: Poly) -> Poly:
    answer = ONE
    for value in values:
        terms = []
        for left, left_coefficient in answer.items():
            for right, right_coefficient in value.items():
                terms.append((left_coefficient * right_coefficient,
                              tuple(a + b for a, b in
                                    zip(left, right, strict=True))))
        answer = polynomial(*terms)
    return answer


def derivative(value: Poly, variable_name: str) -> Poly:
    index = VARIABLES.index(variable_name)
    terms = []
    for monomial, coefficient in value.items():
        exponent = monomial[index]
        if not exponent:
            continue
        derived = list(monomial)
        derived[index] -= 1
        terms.append((coefficient * exponent, tuple(derived)))
    return polynomial(*terms)


def evaluate(value: Poly, assignment: dict[str, Q | int]) -> Q:
    answer = Q(0)
    for monomial, coefficient in value.items():
        term = coefficient
        for name, exponent in zip(VARIABLES, monomial, strict=True):
            term *= Q(assignment[name]) ** exponent
        answer += term
    return answer


def ring_and_unit_audit() -> tuple[dict[str, Poly], dict[str, object]]:
    q = variable("q")
    H = variable("q", -1)
    D = variable("D")
    p = variable("p")
    s = variable("s")
    r = variable("r")
    t = variable("t")
    A = multiply(D, q, H)
    B = multiply(p, s, H)
    C = multiply(r, t, H)
    g = add(multiply(D, q), multiply(p, s), multiply(r, t))
    f = add(A, B, C)
    require(multiply(q, H) == ONE
            and A == D
            and f == multiply(H, g),
            "the active-coloop Laurent reduction changed")

    # A literal active-coloop point on the zero chart-core branch.  It proves
    # that q,H being units does not make D, ps, or R01 a unit.
    guard = {"q": Q(2), "D": Q(0), "p": Q(0), "s": Q(1),
             "r": Q(0), "t": Q(1)}
    require(evaluate(q, guard) * evaluate(H, guard) == 1
            and evaluate(A, guard) == evaluate(B, guard)
                == evaluate(C, guard) == evaluate(f, guard) == 0,
            "the active-coloop zero-core guard changed")
    return {"q": q, "H": H, "D": D, "p": p, "s": s, "r": r,
            "t": t, "A": A, "B": B, "C": C, "g": g, "f": f}, {
        "normalized_ring": "Q[q^+-1,D,p,s,r,t], H=q^-1",
        "active_coloop_identity": "q*H=1",
        "units_forced": ["q", "H"],
        "chart_coefficients": {
            "A=D*q*H": "D",
            "B=p*s*H": "q^-1*p*s",
            "C=r*t*H": "q^-1*r*t",
        },
        "R01_on_active_chart": "D+q^-1*(p*s+r*t)",
        "not_forced_units": ["D", "D*q", "p*s", "r*t", "R01"],
        "literal_guard": {
            "q": "2", "H": "1/2", "D": "0", "p": "0", "r": "0",
            "qH": "1", "A": "0", "B": "0", "C": "0", "R01": "0",
        },
    }


def dot_polynomial(left: tuple[Poly, ...], right: tuple[Poly, ...]) -> Poly:
    require(len(left) == len(right), "module dot width")
    return add(*(multiply(a, b) for a, b in
                 zip(left, right, strict=True)))


def hypersurface_versus_split_resolution_audit(values) -> dict[str, object]:
    A, B, C, f = (values[name] for name in ("A", "B", "C", "f"))

    # The artificial three-generator Koszul resolution has pairwise cells.
    # Verify their boundaries are syzygies of the split degree-one row.
    d1 = (A, B, C)
    zero: Poly = {}
    k_ab = (B, scale(-1, A), zero)
    k_ac = (C, zero, scale(-1, A))
    k_bc = (zero, C, scale(-1, B))
    require(dot_polynomial(d1, k_ab) == zero
            and dot_polynomial(d1, k_ac) == zero
            and dot_polynomial(d1, k_bc) == zero,
            "the split pairwise Koszul identities changed")

    # The split ideal changes H0.  At this point f=A+B+C=0 but A and B are
    # individually nonzero, so it is a point of the hypersurface and not of
    # the split complete intersection.
    witness = {"q": Q(1), "D": Q(1), "p": Q(1), "s": Q(-1),
               "r": Q(0), "t": Q(1)}
    require(evaluate(f, witness) == 0
            and evaluate(A, witness) == 1
            and evaluate(B, witness) == -1,
            "the H0-changing split witness changed")
    return {
        "canonical_hypersurface_resolution": (
            "0 -> S*e_f --R01--> S -> S/(R01) -> 0"
        ),
        "canonical_degree_two_DQ_PS_cell": False,
        "reason": (
            "there is one odd generator e_f for the one equation; its "
            "exterior square is zero"
        ),
        "artificial_split_ideal": "J=(A,B,C)=(D,p*s,r*t) on qH=1",
        "formal_split_pairwise_cells": {
            "d(kappa_AB)": "B*e_A-A*e_B",
            "d(kappa_AC)": "C*e_A-A*e_C",
            "d(kappa_BC)": "C*e_B-B*e_C",
        },
        "split_Koszul_d1_d2": "0 for all three pairwise cells",
        "split_resolution_H0": "S/(A,B,C), not S/(A+B+C)",
        "H0_difference_witness": (
            "q=H=1,D=1,p=1,s=-1,r=0 gives R01=0 but A=1,B=-1"
        ),
        "consequence": (
            "the formal kappa_AB exists only after changing the source "
            "presentation/H0 or retaining it as a relative carrier"
        ),
    }


def monomial_gcd(left: tuple[int, ...], right: tuple[int, ...]):
    return tuple(min(a, b) for a, b in zip(left, right, strict=True))


def monomial_lcm(left: tuple[int, ...], right: tuple[int, ...]):
    return tuple(max(a, b) for a, b in zip(left, right, strict=True))


def colon_and_tor_audit() -> dict[str, object]:
    # Polynomial-ring order H,q,D,p,s,r,t.  Before qH=1 the AB chart
    # monomials share exactly H.
    order = ("H", "q", "D", "p", "s", "r", "t")
    A0 = (1, 1, 1, 0, 0, 0, 0)
    B0 = (1, 0, 0, 1, 1, 0, 0)
    gcd = monomial_gcd(A0, B0)
    lcm = monomial_lcm(A0, B0)
    product = tuple(a + b for a, b in zip(A0, B0, strict=True))
    quotient_factor = tuple(a - b for a, b in
                            zip(product, lcm, strict=True))
    H_monomial = (1, 0, 0, 0, 0, 0, 0)
    require(gcd == quotient_factor == H_monomial,
            "the common-H Tor factor changed")
    return {
        "unlocalized_ring": "S0=Q[H,q,D,p,s,r,t]",
        "chart_pair": ["A0=H*D*q", "B0=H*p*s"],
        "monomial_order": list(order),
        "gcd_A0_B0": "H",
        "intersection": "(A0) intersect (B0)=(H*D*q*p*s)",
        "product": "(A0)*(B0)=(H^2*D*q*p*s)",
        "Tor1_pair": (
            "((A0) intersect (B0))/(A0*B0) = (S0/(H))*[H*D*q*p*s]"
        ),
        "common_factor_colon": "((H*g):H)=(g)",
        "common_factor_colon_quotient": "(g)/(H*g)=(S0/(H))*g",
        "after_active_coloop_qH_equals_1": (
            "H is a unit, (H*g)=(g), and both H-supported quotients vanish"
        ),
        "active_ring_principal_colons": {
            "(R01):H^infinity": "(R01)",
            "(R01):q^infinity": "(R01)",
            "(R01):(D*q)^infinity": "(R01)",
            "(R01):(p*s)^infinity": "(R01)",
        },
        "principal_colon_reason": (
            "R01=D+q^-1*(p*s+r*t) is monic irreducible in D over the "
            "Laurent coefficient UFD and is coprime to D*q and p*s"
        ),
        "chart_pair_ideal": "(A,B)=(D,p*s)",
        "chart_pair_syzygy_module": "S*(p*s,-D)",
        "chart_pair_colons": ["(D):(p*s)=(D)", "(p*s):D=(p*s)"],
        "one_in_chart_pair_ideal": False,
        "zero_branch": "D=p=0 is compatible with qH=1",
        "verdict": (
            "inverting H cancels only the common tail; inverting D*q or p*s "
            "would delete the literal zero branch and is precisely a new "
            "localization/saturation hypothesis"
        ),
    }


def differential_as_one_forms(value: Poly) -> dict[str, Poly]:
    return {f"d{name}": derivative(value, name) for name in VARIABLES
            if derivative(value, name)}


def first_proper_faces_audit(values, hyperbolic) -> dict[str, object]:
    A, B, C = (values[name] for name in ("A", "B", "C"))
    dA = differential_as_one_forms(A)
    dB = differential_as_one_forms(B)
    dC = differential_as_one_forms(C)
    require(set(dA) == {"dD"}
            and set(dB) == {"dq", "dp", "ds"}
            and set(dC) == {"dq", "dr", "dt"},
            (dA, dB, dC))

    hyperbolic_ledger, hyperbolic_digest = hyperbolic.audit()
    require(hyperbolic_digest == hyperbolic.EXPECTED_LEDGER_SHA256,
            "the physical hyperbolic-root ledger changed")
    response = hyperbolic_ledger["complete_response_boundaries"]
    unary = hyperbolic_ledger["unary_and_root_order_boundaries"]
    pp = hyperbolic_ledger["complete_and_selected_PP_boundaries"]
    require([record["complete_root_residual_terms"]
             for record in response["records"]] == [24] * 4
            and unary["shared_selected_Cartan_face"]
                == "q01*H2345 (3 of 15 unary matchings)"
            and pp["selected_labelled_PP_flags"] == 48,
            "the physical first-face census changed")

    return {
        "formal_split_kappa_AB_boundary": "B*e_A-A*e_B",
        "raw_PP_Leibniz_boundary": (
            "dB*e_A+B*d(e_A)-dA*e_B-A*d(e_B)"
        ),
        "raw_A_coefficient_faces": [
            "(dD)*q*H", "D*(dq)*H", "D*q*(dH)"
        ],
        "raw_B_coefficient_faces": [
            "(dp)*s*H", "p*(ds)*H", "p*s*(dH)"
        ],
        "literal_occurrence_counts": {
            "each dD,dq,dp,ds factor times H": 3,
            "each Dq*dH or ps*dH tail packet": 6,
            "A_side_total": 12,
            "B_side_total": 12,
            "coefficient_PP_total": 24,
            "carrier_reinsertion_families": 2,
        },
        "active_relation_on_one_forms": "H*dq+q*dH=0",
        "reduced_A_face": "d(D*q*H)=dD",
        "reduced_B_face": (
            "d(p*s*H)=s*H*dp+p*H*ds-p*s*H^2*dq"
        ),
        "formal_first_faces_closed_by_d_squared": True,
        "physical_root_faces_before_any_mixed_cell": [
            "-D*s1*H", "+p0*q*H", "-D*s0*H", "+p1*q*H"
        ],
        "physical_complete_response_residuals": (
            "four independent signed 24-term collision splitters"
        ),
        "selected_unary_return_on_active_chart": (
            "q*H=1 coefficientwise, but it is still the selected 3-of-15 "
            "occurrence vector, not the complete unary row"
        ),
        "physical_selected_PP_flags": pp["selected_labelled_PP_flags"],
        "first_forward_lower_failure": pp["first_forward_typed_failure"],
        "reverse_lower_scope": pp["reverse_P2_scope"],
        "consequence": (
            "the formal split Koszul PP cell does not totalize the physical "
            "root square; active scalar normalization leaves its occurrence, "
            "collision, operation and word/fine faces independent"
        ),
    }


def chi(value) -> Q:
    delta = (Q(1), Q(1), Q(-1), Q(-1))
    return sum((delta[index] * Q(value[index])
                - delta[index] * Q(value[4 + index])
                for index in range(4)), Q(0))


def augmentation_audit(augmentation_freedom) -> dict[str, object]:
    u_ab = (1, 0, 1, 0)
    u_ac = (1, 0, 0, 1)
    delta = (1, 1, -1, -1)
    zero = (0, 0, 0, 0)
    require(chi(u_ab + zero) == chi(u_ac + zero) == 0
            and chi(u_ab + u_ab) == chi(u_ac + u_ac) == 0
            and chi(u_ab + delta) == chi(u_ac + delta) == -4,
            "the formal mixed-cell B/Eq controls changed")

    freedom = augmentation_freedom.augmentation_audit()
    quotient = augmentation_freedom.quotient_audit()
    counterguard = freedom["same_source_boundary_counterguard"]
    require(counterguard["both_satisfy_d_squared_zero"]
            and counterguard["dark_filler"]["chi"] == 0
            and counterguard["bright_filler"]["chi"] == 4
            and quotient["set_of_d_squared_compatible_values_over_Q"]
                == "chi=4*lambda, lambda arbitrary in Q",
            "the mixed-cell augmentation freedom changed")
    return {
        "formal_split_private_top_AB": list(u_ab),
        "formal_split_private_top_AC": list(u_ac),
        "canonical_split_Koszul_Eq_projection": [0, 0, 0, 0],
        "chi_with_zero_Eq": 0,
        "chi_with_tied_Eq": 0,
        "chi_with_balanced_Eq_delta": -4,
        "active_coloop_relation_constrains_Eq_augmentation": False,
        "d_squared_compatible_quotient": "chi=4*lambda, lambda arbitrary",
        "reason": (
            "qH=1 is a coefficient-ring identity; it gives no chain map "
            "from the formal Koszul cell to corner-resolved cap Eq rows"
        ),
        "physical_chi_bright_column_constructed": False,
    }


def audit():
    pin_dependencies()
    hyperbolic = load(
        "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py",
        "active_three_cap_hyperbolic")
    augmentation_freedom = load(
        "computations/verify_h3_cross_word_mapping_cylinder_d2_augmentation_freedom_gate.py",
        "active_three_cap_augmentation")

    values, ring_data = ring_and_unit_audit()
    resolution = hypersurface_versus_split_resolution_audit(values)
    colon = colon_and_tor_audit()
    proper_faces = first_proper_faces_audit(values, hyperbolic)
    augmented = augmentation_audit(augmentation_freedom)
    ledger = {
        "theorem": "h3 active-coloop three-cap mixed Koszul colon gate",
        "pins": PINS,
        "active_coloop_local_ring": ring_data,
        "canonical_hypersurface_versus_split_Koszul": resolution,
        "common_factor_colon_and_Tor": colon,
        "formal_and_physical_first_proper_faces": proper_faces,
        "private_reduced_Eq_augmentation": augmented,
        "verdict": (
            "The active-coloop relation makes q and H units and reduces the "
            "direct chart A to D.  It does not make D*q, p*s, or R01 a unit. "
            "The canonical one-equation hypersurface resolution of R01 has "
            "no DQ/PS mixed two-cell.  A formal pairwise Koszul cell appears "
            "only in the three-equation split ideal and changes H0.  The "
            "only extra common-H Tor class is supported on H=0 and vanishes "
            "on qH=1, so reusing it is exactly saturation.  Its complete PP "
            "faces remain distinct from the physical collision/root faces, "
            "and neither the canonical dark Eq projection nor qH=1 forces a "
            "bright augmentation."
        ),
        "classification": "EXACT COLON/TOR OBSTRUCTION; NO PHYSICAL CHI-BRIGHT COLUMN",
        "shortest_positive_extra_hypothesis": (
            "construct a source-labelled pointed DQ/PS mapping-cylinder "
            "two-cell in the one-equation source, including the four signed "
            "collision splitters, selected-unary occurrence return, DSQ/PQQ "
            "lower faces, cross-word cap descent, and a specified nonzero "
            "B/Eq scalar lambda"
        ),
        "nonclaims": [
            "the split Koszul resolution is not called the R01 hypersurface resolution",
            "H cancellation is not called D or p*s inversion",
            "the selected 3-of-15 qH occurrence is not called the complete unary unit",
            "a formal pairwise syzygy is not called a physical chart-switch cell",
            "d-squared augmentation freedom is not assigned lambda=1",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("active-coloop three-cap ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("active-coloop three-cap algebra: q,H UNITS; D,ps,R01 NONUNITS")
    print("canonical R01 hypersurface mixed DQ/PS two-cell: ABSENT")
    print("split Koszul kappa: EXISTS BUT CHANGES H0")
    print("common-H Tor: S/(H), VANISHES ON qH=1")
    print("formal kappa PP faces: 24 COEFFICIENT TERMS + 2 REINSERTIONS")
    print("B/Eq value: UNFORCED; canonical dark, bright needs extra lambda")
    print("verdict: SATURATION RESTATEMENT / NO PHYSICAL CHI-BRIGHT COLUMN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

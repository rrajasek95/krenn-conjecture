#!/usr/bin/env python3
"""Exclude the first h=3 axis-pure support-27 stratum by coefficients.

The strongest contradiction is internal to the colour-2 K2,4.  Write its
edges as y_ij=qij:22 for i in {0,1}, j in {2,3,4,5}.  Three off-target
q^[3] equations contain

    F23=y02*y13+y03*y12,
    F24=y02*y14+y04*y12,
    F34=y03*y14+y04*y13.

Their exact syzygy is

    y14*F23-y13*F24+y12*F34=2*y03*y12*y14,

which is impossible on the support torus in characteristic zero.  A second,
target-aware certificate comes from the colour-1 K2,2 tail

    Q1=q24:11*q35:11+q25:11*q34:11.

The off-target q^[3] coefficient at word 001111 is q01:00*Q1, while the
required target response G11[111111] is E1*Q1, where

    E1=p1@0*s1@1+p1@1*s1@0.

Thus q01:00*Q1=0 and q01:00!=0 force Q1=0 and hence the target response
vanishes.  Polynomially, if f_q=q01*Q1 and f_t=E1*Q1-X1, then

    q01*f_t-E1*f_q=-q01*X1.

Both q01 and the prescribed target X1 are nonzero.  This is a denominator-
free infeasibility certificate.  The second S6 orbit is its colour-1/2
transpose, so all support-27 closures are excluded.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = "computations/verify_h3_axis_pure_cancellation_support_lower_bound.py"
PINS = {
    BASE_PATH:
        "c7c501de4c4646b98e5525d616012bbced15957dcaaa836ebe38341c56385397",
    "notes/h3-axis-pure-cancellation-support-lower-bound.md":
        "b81542ec64eb0667c7c70109d15a0e92932d8e1ffeb124c87992a0abe96a41cc",
    "computations/verify_h3_axis_pure_singleton_mate_closure_coloop_gate.py":
        "5e79bd4cf1cdc090e75da25518044ff85e1f993f1d074049eed4f327e22f01e9",
    "notes/h3-axis-pure-singleton-mate-closure-coloop-gate.md":
        "d9d0486e7424db3720a91ea9421f837393dd2102f24f118f655b477704d6421c",
}
EXPECTED_LEDGER_SHA256 = "7f07fd0b9cfe7deec07920b0078ba6e9dc34573246df3e440dfb977716e2363c"

Polynomial = Counter[tuple[str, ...]]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load_base():
    specification = importlib.util.spec_from_file_location(
        "axis_pure_support27_base", ROOT / BASE_PATH)
    require(specification is not None and specification.loader is not None,
            "cannot import base checker")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def clean(polynomial: Polynomial) -> Polynomial:
    return Counter({monomial: coefficient
                    for monomial, coefficient in polynomial.items()
                    if coefficient})


def add(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return clean(answer)


def scale(coefficient: int | Q, polynomial: Polynomial) -> Polynomial:
    return clean(Counter({monomial: Q(coefficient)*value
                          for monomial, value in polynomial.items()}))


def multiply(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = Counter({(): Q(1)})
    for polynomial in polynomials:
        product: Polynomial = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                product[tuple(sorted(left + right))] += (
                    left_coefficient*right_coefficient
                )
        answer = clean(product)
    return answer


def variable(name: str) -> Polynomial:
    return Counter({(name,): Q(1)})


def support_from_names(base, names: tuple[str, ...]):
    lookup = {base.coordinate_key(coordinate): coordinate
              for coordinate in base.ALL_COORDINATES}
    require(set(names) <= set(lookup), "unknown support coordinate")
    return frozenset(lookup[name] for name in names)


REPRESENTATIVE = tuple("""
p1@0:1 p1@1:1 p2@2:2 p2@3:2 p2@4:2 p2@5:2
q01:00 q02:22 q03:22 q04:22 q05:22 q12:22 q13:22 q14:22 q15:22
q23:00 q24:11 q25:11 q34:11 q35:11 q45:00
s1@0:1 s1@1:1 s2@2:2 s2@3:2 s2@4:2 s2@5:2
""".split())


def fibre_polynomial(base, terms, support) -> Polynomial:
    answer: Polynomial = Counter()
    for term in terms:
        if term <= support:
            monomial = tuple(sorted(base.coordinate_key(coordinate)
                                    for coordinate in term))
            answer[monomial] += Q(1)
    return clean(answer)


def full_equation_and_factor_audit() -> dict[str, object]:
    base = load_base()
    support = support_from_names(base, REPRESENTATIVE)
    require(len(support) == 27, "the representative support size changed")
    terms_by_fibre = base.all_matching_terms()

    active = {}
    active_count_histogram = Counter()
    target_term_counts = []
    off_target_term_counts = []
    for fibre, terms in terms_by_fibre.items():
        polynomial = fibre_polynomial(base, terms, support)
        if not polynomial:
            continue
        active[fibre] = polynomial
        active_count_histogram[len(polynomial)] += 1
        if base.is_target_fibre(fibre):
            target_term_counts.append(len(polynomial))
        else:
            off_target_term_counts.append(len(polynomial))

    require(len(active) == 41
            and active_count_histogram == {1: 1, 2: 38, 4: 1, 24: 1}
            and sorted(target_term_counts) == [1, 4, 24]
            and off_target_term_counts == [2]*38,
            ("the complete active coefficient system changed",
             len(active), active_count_histogram,
             target_term_counts, Counter(off_target_term_counts)))

    q_tail = add(
        multiply(variable("q24:11"), variable("q35:11")),
        multiply(variable("q25:11"), variable("q34:11")),
    )
    endpoint = add(
        multiply(variable("p1@0:1"), variable("s1@1:1")),
        multiply(variable("p1@1:1"), variable("s1@0:1")),
    )
    q_off_fibre = ("q3", (0, 0, 1, 1, 1, 1))
    endpoint_off_fibre = ("G", 1, 1, (1, 1, 0, 0, 0, 0))
    target_fibre = ("G", 1, 1, (1, 1, 1, 1, 1, 1))
    q_off = active[q_off_fibre]
    endpoint_off = active[endpoint_off_fibre]
    target = active[target_fibre]
    require(q_off == multiply(variable("q01:00"), q_tail),
            "q3[001111] stopped factoring through the K2,2 tail")
    require(endpoint_off == multiply(
                variable("q23:00"), variable("q45:00"), endpoint),
            "G11[110000] stopped factoring through the endpoint permanent")
    require(target == multiply(endpoint, q_tail),
            "G11[111111] stopped being the product E1*Q1")

    y02, y03, y04 = (variable(f"q0{site}:22") for site in (2, 3, 4))
    y12, y13, y14 = (variable(f"q1{site}:22") for site in (2, 3, 4))
    f23 = add(multiply(y02, y13), multiply(y03, y12))
    f24 = add(multiply(y02, y14), multiply(y04, y12))
    f34 = add(multiply(y03, y14), multiply(y04, y13))
    z45 = variable("q45:00")
    a35 = variable("q35:11")
    a25 = variable("q25:11")
    actual_e23 = active[("q3", (2, 2, 2, 2, 0, 0))]
    actual_e24 = active[("q3", (2, 2, 2, 1, 2, 1))]
    actual_e34 = active[("q3", (2, 2, 1, 2, 2, 1))]
    require(actual_e23 == multiply(z45, f23)
            and actual_e24 == multiply(a35, f24)
            and actual_e34 == multiply(a25, f34),
            "the three actual K2,4 coefficient equations changed")
    k24_certificate = add(
        multiply(a35, a25, y14, actual_e23),
        scale(-1, multiply(z45, a25, y13, actual_e24)),
        multiply(z45, a35, y12, actual_e34),
    )
    k24_nonzero = scale(2, multiply(
        z45, a35, a25, y03, y12, y14
    ))
    require(k24_certificate == k24_nonzero,
            "the denominator-free K2,4 syzygy changed")

    target_parameter = variable("X1")
    target_equation = add(target, scale(-1, target_parameter))
    certificate_left = add(
        multiply(variable("q01:00"), target_equation),
        scale(-1, multiply(endpoint, q_off)),
    )
    certificate_right = scale(
        -1, multiply(variable("q01:00"), target_parameter)
    )
    require(certificate_left == certificate_right,
            "the denominator-free infeasibility certificate changed")

    return {
        "representative_support_size": len(support),
        "representative_support": list(base.support_key(support)),
        "active_output_fibres": len(active),
        "active_term_count_histogram": dict(sorted(active_count_histogram.items())),
        "target_equation_term_counts": sorted(target_term_counts),
        "off_target_equations": len(off_target_term_counts),
        "off_target_term_counts": dict(sorted(Counter(
            off_target_term_counts).items())),
        "primary_q_only_obstruction": {
            "K24_variables": "y_ij=qij:22, i in {0,1}, j in {2,3,4,5}",
            "relations": [
                "F23=y02*y13+y03*y12",
                "F24=y02*y14+y04*y12",
                "F34=y03*y14+y04*y13",
            ],
            "actual_coefficient_equations": [
                "q45:00*F23=0 at q3[222200]",
                "q35:11*F24=0 at q3[222121]",
                "q25:11*F34=0 at q3[221221]",
            ],
            "ratio_form": "r_i=y0i/y1i; r_i=-r_j for all pairs",
            "characteristic_requirement": "2!=0",
            "bare_syzygy": (
                "y14*F23-y13*F24+y12*F34=2*y03*y12*y14"
            ),
            "denominator_free_actual_syzygy": (
                "q35*q25*y14*e23-q45*q25*y13*e24+"
                "q45*q35*y12*e34="
                "2*q45*q35*q25*y03*y12*y14"
            ),
            "right_hand_side_nonzero_on_support_torus": True,
        },
        "secondary_target_factor_obstruction": {
        "selected_bright_colour": 1,
        "K22_tail": "Q1=q24:11*q35:11+q25:11*q34:11",
        "endpoint_permanent": (
            "E1=p1@0:1*s1@1:1+p1@1:1*s1@0:1"
        ),
        "off_target_q_equation": "f_q=q01:00*Q1=0 at q3[001111]",
        "off_target_endpoint_equation": (
            "q23:00*q45:00*E1=0 at G11[110000]"
        ),
        "required_target_equation": (
            "f_t=E1*Q1-X1=0 at G11[111111], X1!=0"
        ),
        "denominator_free_certificate": (
            "q01:00*f_t-E1*f_q=-q01:00*X1"
        ),
        "certificate_uses_nonzero_coordinates": ["q01:00", "X1"],
        },
        "coefficient_system_solvable_on_support_torus": False,
    }


def symmetry_and_consequence_audit() -> dict[str, object]:
    # These counts and the colour-transpose statement are pinned to the
    # exhaustive support theorem.  The coefficient certificate is natural
    # under site permutations and exchanges colours 1 and 2.
    return {
        "support27_labelled_closures": 12,
        "F0_normalized_supports": 2,
        "S6_orbits": 2,
        "S6_orbit_sizes": [45, 45],
        "second_orbit": "colour swap 1<->2 of the displayed certificate",
        "site_permutation_naturality": True,
        "all_support27_closures_inconsistent": True,
        "improved_exact_support_lower_bound": 28,
        "arbitrary_coloop_normalization_needed_at_support27": False,
        "remaining_scope": (
            "supports >=28 may contain enlarged coloop/circuit packets and "
            "still require an arbitrary-coloop normalization or a further "
            "coefficient/support reduction"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 axis-pure support-27 coefficient inconsistency",
        "pins": PINS,
        "complete_coefficient_system": full_equation_and_factor_audit(),
        "symmetry_and_consequence": symmetry_and_consequence_audit(),
        "verdict": (
            "The first no-singleton support stratum has no coefficient point. "
            "Three off-target q3 equations on the K2,4 give an exact nonzero "
            "torus certificate with right side 2*q45*q35*q25*y03*y12*y14. "
            "Independently, its K2,2 tail Q1 occurs both in off-target "
            "q3[001111] and required target G11[111111], giving the second "
            "certificate q01*f_t-E1*f_q=-q01*X1. "
            "Site covariance and bright-colour transpose exclude all twelve "
            "closures, improving the axis-pure support bound from 27 to 28."
        ),
        "scope": (
            "canonical h=3 axis-purified five-tensor equations over a field; "
            "one F0-normalized support representative plus the exhaustive "
            "site/bright-colour orbit classification pinned from dbee33d"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("axis-pure support-27 complete coefficient system: INCONSISTENT")
    print("primary certificate: three K2,4 permanents force 2*unit=0")
    print("secondary certificate: q01*f_target-E1*f_q=-q01*X1")
    print("all 12 closures excluded by site/bright-colour covariance")
    print("exact axis-pure support lower bound: >=28")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

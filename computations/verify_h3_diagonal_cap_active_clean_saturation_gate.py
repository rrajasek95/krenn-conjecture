#!/usr/bin/env python3
"""Audit the nonlinear diagonal-cap selection and its active saturation.

For K(lambda)=sum_i lambda_i E_ii at h=3, expand

    6 E(K) = 3 s(K) r(K)^2 x + r(K)^3.

There are three pure and seven mixed cubic lambda coefficients.  The checker
replays the exact expansion and gives a minimal Laurent unit guard made only
from pairwise mixed coefficients:

    F0=l0^2*l1, F1=l1^2*l2, F2=l2^2*l0,
    F0*F1*F2=(l0*l1*l2)^3.

Thus coordinatewise cleanliness, and even ordinary resultant vanishing from
axis roots, do not imply an active diagonal zero.

On a genuine exact eight-site source the conclusion is stronger.  An active
clean diagonal zero would give, by the exact cap identity and one-site
diagonal normalization, a six-site realization of Delta_(6,3), contrary to
the certified SP-K6 theorem.  Hence the full diagonal clean ideal, saturated
by lambda_0 lambda_1 lambda_2 s(lambda), is the unit ideal on the exact-source
scheme.  A theorem forcing such a zero is therefore equivalent to emptiness
of the h=3 exact-source scheme, not a weaker constructive cap lemma.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_endpoint_polarized_nine_coordinate_cap_evaluation_gate.py":
        "401a3b33b8e0082b75fe86b1476bbc94b8ab61266c2241aa86e168ce8c91f1ab",
    "computations/verify_identity_cap_activity_and_k6_obstruction.py":
        "345a6ce635978abce30b79208fc8442dbebb97e42cac5a1aeddfc66ca96d0a24",
    "notes/clean-bridge-at-eight-is-the-open-case.md":
        "86b4f7d19443ab48c2df4a29cb644829fbcb5c24b1d5c7a200253d0ee394b468",
    "proofs/six-site-arbitrary-complex-obstruction.md":
        "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713",
    "computations/audit_cap_condition_projective_height_obstruction_independent.py":
        "ca633c152e0ee425dfdd8282bef011b15de2dfb62bd4bd84e0c82015f12d67a7",
}
EXPECTED_LEDGER_SHA256 = (
    "527cb54f0ab0331f783d90b548c99999c1f0cee6003380772a2c8cda51907d42"
)

COLOURS = tuple(range(3))
ZERO_EXPONENT = (0, 0, 0)
ACTIVE_TORUS_EXPONENT = (1, 1, 1)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def exponent_add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def monomial_multiply(left, right):
    return exponent_add(left, right)


def monomial_power(value, power: int):
    result = ZERO_EXPONENT
    for _ in range(power):
        result = monomial_multiply(result, value)
    return result


def evaluate_monomial(exponent, point):
    result = Q(1)
    for power, value in zip(exponent, point, strict=True):
        result *= Q(value) ** power
    return result


def exact_diagonal_cubic_audit(polarized):
    record = polarized.diagonal_clean_polarization_audit()
    require(record["h3_clean_error"]
            == "6E(K)=3*s(K)*r(K)^2*x+r(K)^3"
            and record["diagonal_cubic_lambda_monomials"] == 10
            and record["coordinate_pure_cubics"] == 3
            and record["new_mixed_polarization_conditions"] == 7,
            record)
    return {
        "cap": "K(lambda)=lambda_0 E_00+lambda_1 E_11+lambda_2 E_22",
        "scalar": "s(lambda)=sum_i lambda_i A_67[ii]",
        "error": "6E(lambda)=3*s(lambda)*r(lambda)^2*x+r(lambda)^3",
        "lambda_degree": 3,
        "coefficient_census": {
            "pure_lambda_i_cubed": 3,
            "ordered_lambda_i_squared_lambda_j": 6,
            "lambda_0_lambda_1_lambda_2": 1,
        },
        "ordered_pair_coefficient": (
            "C_iij=3*s_j*r_i^2*x+6*s_i*r_i*r_j*x+3*r_i^2*r_j"
        ),
        "triple_coefficient": (
            "C_012=6*(s_0*r_1*r_2+s_1*r_0*r_2+s_2*r_0*r_1)*x"
            "+6*r_0*r_1*r_2"
        ),
        "activity_denominator":
            "D=lambda_0*lambda_1*lambda_2*s(lambda)",
    }


def pair_cycle_laurent_saturation_audit():
    f0 = (2, 1, 0)
    f1 = (0, 2, 1)
    f2 = (1, 0, 2)
    product_exponent = monomial_multiply(monomial_multiply(f0, f1), f2)
    denominator_cube = monomial_power(ACTIVE_TORUS_EXPONENT, 3)
    require(product_exponent == denominator_cube == (3, 3, 3),
            (product_exponent, denominator_cube))

    # The ordinary projective system has the three coordinate points as
    # common roots, so its homogeneous resultant vanishes.  None is active.
    axes = ((Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)),
            (Q(0), Q(0), Q(1)))
    require(all(all(evaluate_monomial(generator, point) == 0
                    for generator in (f0, f1, f2))
                for point in axes), axes)
    torus_samples = ((Q(1), Q(1), Q(1)),
                     (Q(2), Q(-3), Q(5)),
                     (Q(-1), Q(7), Q(4)))
    require(all(all(evaluate_monomial(generator, point) != 0
                    for generator in (f0, f1, f2))
                for point in torus_samples), torus_samples)

    reverse = ((2, 0, 1), (1, 2, 0), (0, 1, 2))
    reverse_product = ZERO_EXPONENT
    for generator in reverse:
        reverse_product = monomial_multiply(reverse_product, generator)
    require(reverse_product == denominator_cube, reverse_product)
    return {
        "guard": [
            "F_0=lambda_0^2*lambda_1",
            "F_1=lambda_1^2*lambda_2",
            "F_2=lambda_2^2*lambda_0",
        ],
        "pure_coordinate_cubics": "all zero",
        "triple_polarization": "zero",
        "ordinary_projective_resultant": 0,
        "resultant_reason":
            "the three coordinate-axis points are common projective zeros",
        "active_laurent_certificate": (
            "F_0*F_1*F_2=(lambda_0*lambda_1*lambda_2)^3"
        ),
        "active_torus_saturation": "unit ideal",
        "reverse_directed_cycle_has_same_certificate": True,
        "consequence": (
            "ordinary resultant vanishing and coordinatewise cleanliness "
            "do not imply an active diagonal zero; pairwise mixed "
            "polarizations already support a Laurent unit"
        ),
    }


def exact_source_active_saturation_theorem(identity):
    # Replay the only formal normalization ingredient used in the descent:
    # if the clean cap gives coefficients kappa_i/s on the three pure words,
    # scaling one residual site by s/kappa_i makes all coefficients one.
    samples = (
        (Q(2), (Q(3), Q(-5), Q(7))),
        (Q(-11), (Q(4), Q(9), Q(-2))),
    )
    for scalar, kappas in samples:
        require(scalar and all(kappas), (scalar, kappas))
        capped = tuple(kappa / scalar for kappa in kappas)
        diagonal = tuple(scalar / kappa for kappa in kappas)
        require(tuple(left * right for left, right in zip(
            capped, diagonal, strict=True)) == (Q(1), Q(1), Q(1)),
            (scalar, kappas))

    # Pin the existing exact cap/K6 interface and its scope.  The checker is
    # deliberately cited for the global six-site theorem rather than trying
    # to replace its certified nineteen-stratum proof here.
    require(identity.identity_cap() == [
        [Q(1), Q(0), Q(0)],
        [Q(0), Q(1), Q(0)],
        [Q(0), Q(0), Q(1)],
    ], "identity-cap convention changed")
    identity.audit_D1_diagonal_site_map()
    identity.audit_D_normalization_on_the_six_cycle()

    return {
        "exact_source_rows": 9 * 3 ** 6,
        "diagonal_clean_coordinates": 3 ** 6,
        "active_open_set":
            "lambda_0*lambda_1*lambda_2*s(lambda) != 0",
        "descent_implication": (
            "exact source + active diagonal E(lambda)=0 gives a six-site "
            "aggregate with pure coefficients kappa_i/s; one invertible "
            "diagonal map at one site sends it to Delta_(6,3)"
        ),
        "certified_terminal":
            "SP-K6: no arbitrary-complex six-site aggregate realizes Delta_(6,3)",
        "fibrewise_verdict":
            "every genuine exact-source fibre has no active clean diagonal cap",
        "global_saturated_ideal": (
            "(J_EqSystem + <E_w(lambda):w in {0,1,2}^6>) "
            ": (lambda_0*lambda_1*lambda_2*s(lambda))^infinity = (1)"
        ),
        "finite_affine_unit_form": (
            "J_EqSystem + <E_w(lambda)> + "
            "<z*lambda_0*lambda_1*lambda_2*s(lambda)-1> = (1)"
        ),
        "why_this_is_exact_without_an_explicit_source_point": (
            "a common zero would itself be an exact source with an active "
            "clean cap and would contradict SP-K6; Nullstellensatz then "
            "gives the displayed unit ideal"
        ),
        "explicit_groebner_certificate_status": (
            "not extracted from the 7,291-generator affine universal ideal; the "
            "unit theorem is certified through exact descent plus SP-K6"
        ),
    }


def source_identity_frontier_audit():
    return {
        "linear_exact_source_identity": (
            "haf_w(s*q+R(K))=s(K)^2*sum_lm K_lm*Row(l,m,w)+E_w(K)"
        ),
        "on_the_source_scheme": (
            "the rows identify E as the higher clean error; they do not "
            "make it vanish"
        ),
        "first_uncontrolled_colour_support": 2,
        "first_uncontrolled_coefficients": (
            "the six C_iij=[lambda_i^2 lambda_j](6E), i!=j"
        ),
        "minimal_exact_counterguard": (
            "the directed cycle C_001,C_112,C_220 can carry the Laurent "
            "unit F0,F1,F2 even when all pure and triple coefficients vanish"
        ),
        "minimum_new_source_derived_relation": (
            "a mixed second-polarized source syzygy excluding both directed "
            "three-cycles in the six C_iij, followed by compatibility with "
            "the triple C_012; equivalently, prove that the active saturation "
            "of the full coefficient ideal is proper"
        ),
        "load_bearing_warning": (
            "on the genuine exact-source scheme that active saturation is "
            "already the unit ideal by SP-K6.  Therefore a theorem making it "
            "proper for every source point is equivalent to proving the h=3 "
            "source scheme empty"
        ),
        "identity_cap_specialization": (
            "lambda=(1,1,1) reduces the same issue to tr(A_67)!=0 and "
            "E_67(I)=0, already known to be equivalent to the open h=3 case"
        ),
        "not_a_missing_presentation_atom": True,
    }


def audit():
    pin_dependencies()
    polarized = load(
        "computations/verify_h3_endpoint_polarized_nine_coordinate_cap_evaluation_gate.py",
        "diagonal_selection_polarized",
    )
    identity = load(
        "computations/verify_identity_cap_activity_and_k6_obstruction.py",
        "diagonal_selection_identity",
    )
    ledger = {
        "theorem": (
            "the h=3 diagonal clean equations form a vector-valued ternary "
            "cubic with seven mixed coefficients.  Pairwise mixed terms "
            "already admit an exact Laurent unit despite zero pure cubics "
            "and vanishing ordinary resultant.  More decisively, exact cap "
            "descent plus SP-K6 proves that the full clean ideal has unit "
            "active saturation on the exact-source scheme.  Thus selecting "
            "an active diagonal zero for every source is equivalent to "
            "proving that source scheme empty"
        ),
        "pins": PINS,
        "explicit_diagonal_cubic": exact_diagonal_cubic_audit(polarized),
        "resultant_versus_active_saturation":
            pair_cycle_laurent_saturation_audit(),
        "exact_source_saturation":
            exact_source_active_saturation_theorem(identity),
        "first_missing_source_coefficient_identity":
            source_identity_frontier_audit(),
        "scope": (
            "exact characteristic-zero h=3 diagonal cap algebra, active "
            "torus saturation, the full 6,561-row source scheme, exact cap "
            "descent and certified SP-K6.  The small pair-cycle is an "
            "abstract coefficient guard, not an asserted exact-source "
            "point; no exact eight-site source point is constructed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
    else:
        print("h3 diagonal active-clean selection: SATURATED NO-ZERO")
        print("mode", arguments.mode)
        print("ordinary resultant alone: INSUFFICIENT")
        print("pair-mixed Laurent unit guard: EXACT")
        print("exact-source active saturation: UNIT by descent + SP-K6")
        print("active-zero theorem: EQUIVALENT TO h3 SOURCE EMPTINESS")
        print("ledger_sha256", digest)


if __name__ == "__main__":
    main()

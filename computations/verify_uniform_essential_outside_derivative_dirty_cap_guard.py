#!/usr/bin/env python3
"""Classify the first-jet essential outside branch and freeze its guard.

The actual sharp C6 outside derivative is a literal one-colour pure state.
Support-minimum completion of the other colours emits a mixed unit, but a
complete physical derivative tensor does not determine the nonlinear clean
cap error.  This script gives the smallest three-channel, N=8 abstract
full-GHZ-compatible boundary signature with three independent pure outside
states, no mixed coordinate, and no active clean covector.

The guard is deliberately not asserted to be a realizable common-edge
aggregate source.  It isolates the missing hypothesis: shared-edge/star
integrability of the higher boundary response, not more first-jet data.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from itertools import product
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_tight_c6_augmented_derivative_contraction.py":
        "ccfbc79dadd3869ab2d80e94deb26021456bd2f7eb3c52c5305179281e9353c6",
    "notes/2026-08-14-uniform-tight-c6-augmented-derivative-contraction.md":
        "5124943ec06e5344aeebb704f55a5b804834bb748af50b31d74fefc01a6db4f4",
    "computations/verify_c6_three_direct_minimal_pure_escape_unit_gate.py":
        "b6d27b3ecb69e1bc62f23d583c97cd026b1b2ec2d3050f1ed5ecba2cd32df263",
    "notes/c6-three-direct-minimal-pure-escape-unit-gate.md":
        "8b9c1cd9d9acebbaca7b1f85c2b14b3c8af50b5c94da99cdc5d0638e5c82a72d",
    "computations/verify_cap_condition_projective_height_obstruction.py":
        "05c0cad18f5d820e025e6c1a93127fe6a288cfa1639bc8509045b3a873a60583",
    "notes/cap-condition-projective-height-obstruction.md":
        "4a4ce688a5835c7d887df86c332bed420e83c7f920768c054a41631465f6fb82",
    "computations/audit_cap_condition_projective_height_obstruction_independent.py":
        "ca633c152e0ee425dfdd8282bef011b15de2dfb62bd4bd84e0c82015f12d67a7",
    "notes/clean-pair-cap-exact-descent-target.md":
        "90f49ac4fde9b793409d9081977e7a7135ebd76c1b5df5d699387d142c2b9b75",
}
EXPECTED_LEDGER_SHA256 = (
    "40c3f63190b420840f8fbc1c27f49f83b2afecc7e32078c6f8594f522abd1b12"
)


SITES = tuple(range(6))
COLOURS = tuple(range(3))
EMPTY_WORD = (-1,) * len(SITES)
WORDS = tuple(product(COLOURS, repeat=len(SITES)))
Polynomial = dict[tuple[int, ...], Q]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned outside/cap theorem changed", relative,
                 actual, expected))


def add(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def scale(scalar: Q, polynomial: Polynomial) -> Polynomial:
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for left_word, left_coefficient in left.items():
        for right_word, right_coefficient in right.items():
            if any(a != -1 and b != -1
                   for a, b in zip(left_word, right_word, strict=True)):
                continue
            word = tuple(b if a == -1 else a
                         for a, b in zip(left_word, right_word, strict=True))
            answer[word] = answer.get(word, Q(0)) \
                + left_coefficient * right_coefficient
            if not answer[word]:
                del answer[word]
    return answer


def power(polynomial: Polynomial, exponent: int) -> Polynomial:
    answer = {EMPTY_WORD: Q(1)}
    for _ in range(exponent):
        answer = multiply(answer, polynomial)
    return answer


def decorated_edge(left: int, right: int,
                   left_colour: int, right_colour: int) -> Polynomial:
    word = [-1] * len(SITES)
    word[left] = left_colour
    word[right] = right_colour
    return {tuple(word): Q(1)}


def pure(colour: int) -> Polynomial:
    return {(colour,) * len(SITES): Q(1)}


def rank(columns: tuple[Polynomial, ...]) -> int:
    basis: dict[tuple[int, ...], Polynomial] = {}
    for column in columns:
        vector = dict(column)
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                coefficient = vector[pivot]
                basis[pivot] = scale(Q(1) / coefficient, vector)
                break
            coefficient = vector[pivot]
            vector = add(vector, scale(-coefficient, basis[pivot]))
    return len(basis)


def target(kappas: tuple[Q, Q, Q]) -> Polynomial:
    return add(*(scale(kappa, pure(colour))
                 for colour, kappa in enumerate(kappas)))


def dirty_signature(kappas: tuple[Q, Q, Q], x: Polynomial):
    scalar = sum(kappas, Q(0))
    x_squared = power(x, 2)
    x_cubed = power(x, 3)
    c2 = scale(-scalar, x)
    c4: Polynomial = {}
    c6 = add(target(kappas), scale(scalar / 3, x_cubed))
    top = add(
        c6,
        multiply(c4, x),
        scale(Q(1, 2), multiply(c2, x_squared)),
        scale(scalar / 6, x_cubed),
    )
    sx_plus_c2 = add(scale(scalar, x), c2)
    error = add(
        scale(6 * scalar * scalar, target(kappas)),
        scale(Q(-1), power(sx_plus_c2, 3)),
    )
    return {
        "s": scalar,
        "kappa": kappas,
        "C2": c2,
        "C4": c4,
        "C6": c6,
        "top": top,
        "error": error,
    }


def symbolic_polynomial_add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def symbolic_polynomial_multiply(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in
                             zip(left_monomial, right_monomial, strict=True))
            answer[monomial] = answer.get(monomial, Q(0)) \
                + left_coefficient * right_coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def symbolic_polynomial_scale(scalar, polynomial):
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def symbolic_polynomial_power(polynomial, exponent):
    answer = {(0, 0, 0, 0, 0): Q(1)}
    for _ in range(exponent):
        answer = symbolic_polynomial_multiply(answer, polynomial)
    return answer


def saturation_unit_certificate() -> dict[str, object]:
    # Variables are (t,s,k0,k1,k2).  With G0=6*s^2*k0 and
    # h=s*k0*k1*k2, verify
    # 1=(1-th)(1+th)+t^2*(k0*k1^2*k2^2/6)*G0.
    one = {(0, 0, 0, 0, 0): Q(1)}
    t = {(1, 0, 0, 0, 0): Q(1)}
    s = {(0, 1, 0, 0, 0): Q(1)}
    k0 = {(0, 0, 1, 0, 0): Q(1)}
    k1 = {(0, 0, 0, 1, 0): Q(1)}
    k2 = {(0, 0, 0, 0, 1): Q(1)}
    h = symbolic_polynomial_multiply(
        symbolic_polynomial_multiply(s, k0),
        symbolic_polynomial_multiply(k1, k2),
    )
    th = symbolic_polynomial_multiply(t, h)
    first = symbolic_polynomial_multiply(
        symbolic_polynomial_add(one, symbolic_polynomial_scale(-1, th)),
        symbolic_polynomial_add(one, th),
    )
    g0 = symbolic_polynomial_scale(
        6,
        symbolic_polynomial_multiply(symbolic_polynomial_power(s, 2), k0),
    )
    multiplier = symbolic_polynomial_scale(
        Q(1, 6),
        symbolic_polynomial_multiply(
            symbolic_polynomial_power(t, 2),
            symbolic_polynomial_multiply(
                k0,
                symbolic_polynomial_multiply(
                    symbolic_polynomial_power(k1, 2),
                    symbolic_polynomial_power(k2, 2),
                ),
            ),
        ),
    )
    certificate = symbolic_polynomial_add(
        first, symbolic_polynomial_multiply(multiplier, g0)
    )
    require(certificate == one, certificate)
    return {
        "error_ideal": "(6*s^2*k0,6*s^2*k1,6*s^2*k2)",
        "activity_character": "h=s*k0*k1*k2",
        "identity": (
            "1=(1-t*h)*(1+t*h)+t^2*(k0*k1^2*k2^2/6)*(6*s^2*k0)"
        ),
        "saturated_ideal": "(1)",
    }


def full_ghz_compatible_guard() -> dict[str, object]:
    # x is a literal three-edge mixed one-factor.  Its cube has the single
    # mixed word 012012 with coefficient 3!=6.
    x = add(
        decorated_edge(0, 1, 0, 1),
        decorated_edge(2, 3, 2, 0),
        decorated_edge(4, 5, 1, 2),
    )
    x_cubed = power(x, 3)
    mixed_word = (0, 1, 2, 0, 1, 2)
    require(x_cubed == {mixed_word: Q(6)}, x_cubed)

    outside_columns = tuple(target(tuple(Q(int(index == colour))
                                          for index in COLOURS))
                            for colour in COLOURS)
    require(rank(outside_columns) == 3
            and add(*outside_columns) == target((Q(1), Q(1), Q(1))),
            outside_columns)
    outside_records = []
    for colour in COLOURS:
        kappas = tuple(Q(int(index == colour)) for index in COLOURS)
        signature = dirty_signature(kappas, x)
        require(signature["s"] == 1
                and signature["top"] == pure(colour)
                and signature["error"] == scale(6, pure(colour)),
                (colour, signature))
        require(all(len(set(word)) == 1
                    for word in signature["top"]), signature["top"])
        outside_records.append({
            "parameter": f"eta_{colour}",
            "literal_cap_coordinate": f"K_{colour}{colour}",
            "direct_scalar_s": "1",
            "complete_derivative_tensor": str(colour) * 6,
            "mixed_derivative_coordinates": 0,
            "rank_without_with": [2, 3],
            "clean_error_coordinate": {str(colour) * 6: "6"},
            "active_clean": False,
            "reason": "the other two kappa values vanish",
        })

    # Every basis direction is essential, their sum is the full target, and
    # even the active diagonal direction is unclean.
    active = dirty_signature((Q(1), Q(1), Q(1)), x)
    require(active["s"] == 3
            and active["top"] == target((Q(1), Q(1), Q(1)))
            and active["error"]
            == scale(54, target((Q(1), Q(1), Q(1)))),
            active)

    # Exact zero-locus argument: D_i=6*s^2*k_i.  If s is nonzero and every
    # D_i vanishes, all k_i vanish, contradicting s=k0+k1+k2.  Thus every
    # clean covector lies on the inactive trace hyperplane s=0.
    sample_clean = dirty_signature((Q(1), Q(-1), Q(0)), x)
    require(sample_clean["s"] == 0 and not sample_clean["error"],
            sample_clean)
    for kappas in product(range(-2, 3), repeat=3):
        rational = tuple(map(Q, kappas))
        signature = dirty_signature(rational, x)
        if not signature["error"]:
            require(signature["s"] == 0,
                    ("clean active sample", rational, signature))

    return {
        "ambient_order": 8,
        "residual_sites": 6,
        "complete_derivative_coordinates": len(WORDS),
        "pure_coordinates": 3,
        "mixed_coordinates": len(WORDS) - 3,
        "cap_parameter_space": (
            "diagonal K=diag(k0,k1,k2), embedded in the physical 9-space"
        ),
        "direct_block": "I_3",
        "direct_scalar": "s=k0+k1+k2",
        "target_pairings": "kappa_i=k_i",
        "fixed_internal_x": "01;01 + 23;20 + 45;12",
        "x_cubed": {"012012": "6"},
        "signature": {
            "C0": "s",
            "C2": "-s*x",
            "C4": "0",
            "C6": "sum_i k_i*X_i + (s/3)*x^3",
        },
        "full_GHZ_contraction_identity": (
            "C6+C2*x^2/2+s*x^3/6=sum_i k_i*X_i"
        ),
        "outside_columns": tuple(outside_records),
        "outside_column_rank": rank(outside_columns),
        "sum_of_outside_columns": "Delta_(6,3)",
        "active_test_direction": {
            "kappa": [1, 1, 1],
            "s": 3,
            "top": "Delta_(6,3)",
            "clean_error": "54*Delta_(6,3)",
        },
        "clean_locus": "s=0",
        "every_clean_covector_inactive": True,
        "mixed_unit": False,
        "typed_active_clean_cap": False,
        "saturation": saturation_unit_certificate(),
        "minimality": (
            "three independent single-colour columns are necessary to sum "
            "to the three independent pure target tensors; N=8 is the "
            "first live inductive cap boundary over the excluded N=6 base"
        ),
        "scope": (
            "exact abstract full-GHZ-compatible boundary signature; C2/C6 "
            "are not asserted to arise from one common-edge aggregate source"
        ),
    }


def actual_c6_first_jet() -> dict[str, object]:
    contraction = load(
        "computations/verify_uniform_tight_c6_augmented_derivative_contraction.py",
        "essential_outside_contraction",
    )
    ledger = contraction.audit()
    c6 = ledger["complete_C6_augmented_span"]
    require(c6["escape_cases"] == 12
            and c6["complete_cap_derivative_span_rank"] == 0
            and c6["complete_augmented_rank"] == 1,
            c6)
    require(all(record["escape_mixed_support"] == 0
                and record["classification"]
                == "active outside tight-cut channel"
                for record in c6["records"]), c6["records"])
    return {
        "literal_C6_escape_cases": c6["escape_cases"],
        "complete_rank_cap_to_escape": [0, 1],
        "complete_tensor": "one nonzero pure-one coordinate",
        "mixed_coordinates": 0,
        "literal_cofactor_occurrences_per_derivative": 1,
        "typed_cut_cell": True,
        "typed_active_clean_cap": False,
        "first_failure": (
            "one-colour escape has only kappa_1 nonzero, so cap activity "
            "fails before the nonlinear cleanliness equation is reached"
        ),
        "support_minimum_completion": (
            "the pinned 3d78125 theorem supplies either missing pure colour "
            "with a literal mixed singleton in all 192 first completions"
        ),
        "nonminimum_completion": "not classified by the support-minimum theorem",
    }


def theorem_boundary() -> dict[str, object]:
    return {
        "proved_restricted_branch": (
            "the literal sharp C6 outside state is pure rank one and "
            "inactive; every support-minimum next-colour completion is a "
            "mixed unit by 3d78125"
        ),
        "refuted_uniform_inference": (
            "complete 3^N derivative tensors plus the full linear GHZ cap "
            "identity do not force a mixed unit or an active clean cap"
        ),
        "missing_source_hypothesis": (
            "C2,C4,C6 must be the contractions of matching cofactors built "
            "from one common endpoint-ordered edge family; equivalently, "
            "shared-star/alternating-ear integrability must make the clean "
            "ideal nonunit after localizing the outside pure coordinate and "
            "s*kappa0*kappa1*kappa2"
        ),
        "required_saturation": (
            "I_clean:(u_out*s*kappa0*kappa1*kappa2)^infinity != (1), or a "
            "source-labelled mixed singleton/private cap occurs first"
        ),
        "ear_scope": (
            "matching-covered/ear structure controls which occurrences and "
            "tails exist, but not the higher response C2; it becomes useful "
            "only when its flips are proved to preserve the common-edge "
            "cofactor products source-naturally"
        ),
    }


def audit() -> dict[str, object]:
    pin_dependencies()
    return {
        "theorem": "essential outside derivative first-jet classification",
        "pins": PINS,
        "actual_C6_branch": actual_c6_first_jet(),
        "smallest_full_GHZ_compatible_guard": full_ghz_compatible_guard(),
        "terminal_boundary": theorem_boundary(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    arguments = parser.parse_args()
    ledger = {"mode_independent": True, "audit": audit()}
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    print("essential outside derivative / dirty-cap guard: PASS")
    print("mode", arguments.mode)
    print("actual C6: pure rank-one outside, inactive as a clean cap")
    print("support-minimum completion: mixed unit")
    print("general first-jet implication: FALSE (N=8 abstract GHZ guard)")
    print("missing input: common-edge higher-response integrability")
    print("sha256:", digest)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Classify the universal response 2x3 Segre tangent and its dark arms.

For

    Y=[[A*x0,A*x1,A*x2], [B*x0,B*x1,B*x2]],

the all-ones direction has linearized 2x2 minors

    (A-B)*(xi-xj).

Over the characteristic-zero theorem field it is tangent to rank(Y)<=1 iff
``A=B`` or ``x0=x1=x2``.  This includes every zero degeneration.

The first arm is endpoint-odd dark and leaves only the residual matching
standard module.  The second is matching-standard dark and leaves only the
endpoint-odd line.  A nonzero product is a genuine mixed conormal, but the
current source typing does not identify its two factors with an offdiagonal
decorated cell and its signed physical cofactor.  Hence the private-site
fan theorem remains conditional on one incidence/grade-placement square.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py":
        "4493274dfbda62cec0d6823272762fb01c3a798123a1da206559e91890ba9047",
    "notes/h3-universal-response-ks-augmented-readout-extension-gate.md":
        "f201fd4c4599a27173a824d7475ade679ef2de55e7c91bc3dd9cc917ac16ee37",
    "computations/verify_h3_matching_face_residual_flip_semidirect_gate.py":
        "0769314fa55e0978a24680a16f5f5bd4bad8b176322d9709cb42c8b73e025f1e",
    "notes/h3-matching-face-residual-flip-semidirect-gate.md":
        "7e93c5dbf094748371b274bbacce6f677f3eeb8fc8476aca38956652bfae3bf9",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "notes/h3-physical-cartan-source-orbit-descent.md":
        "4f0ab9035124319cc491bb2cc9914ef58ced228774f41625699e8c1cb2ca65d1",
    "computations/verify_h3_evaluated_determinant_transverse_landing_reduction.py":
        "73b7a1249c9856c4ac79e0c82a5bf8c024261d85199eef1781a51d4848732ca5",
    "notes/h3-evaluated-determinant-transverse-landing-reduction.md":
        "cbeeeb2c3821268ec6f56a0a2cb7d7684254b44f9510b6ed9056cee653e53196",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "notes/h3-active-fan-coloop-or-four-good.md":
        "9be8996264fa2070a8f5d7f725f3fcb154b6ee2df2b3e5d3ccd4a6412ec5b03a",
}
EXPECTED_LEDGER_SHA256 = "0b32d8cde4f6b53886d6b989c142fc076531f297f1a089a5ec1b607cfabf554e"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def rank(vectors: tuple[tuple[Q, ...], ...]) -> int:
    basis: dict[int, tuple[Q, ...]] = {}
    for original in vectors:
        values = [Q(value) for value in original]
        for pivot in sorted(basis):
            if values[pivot]:
                coefficient = values[pivot]
                values = [left - coefficient * right for left, right in
                          zip(values, basis[pivot], strict=True)]
        pivot = next((index for index, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        coefficient = values[pivot]
        basis[pivot] = tuple(value / coefficient for value in values)
    return len(basis)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def linearized_minor(A: Q, B: Q, values: tuple[Q, ...],
                     left: int, right: int) -> Q:
    # d(Y_0l Y_1r-Y_0r Y_1l) on the all-ones 2x3 direction.
    return (
        B * values[right] + A * values[left]
        - B * values[left] - A * values[right]
    )


def exact_tangent_iff_audit() -> dict[str, object]:
    samples = 0
    tangent_samples = 0
    endpoint_dark_only = 0
    matching_dark_only = 0
    both_dark = 0
    bright = 0
    for raw in product(range(-2, 3), repeat=5):
        A, B, x0, x1, x2 = map(Q, raw)
        values = (x0, x1, x2)
        derivatives = tuple(
            linearized_minor(A, B, values, left, right)
            for left, right in ((0, 1), (0, 2), (1, 2))
        )
        expected = tuple(
            (A - B) * (values[left] - values[right])
            for left, right in ((0, 1), (0, 2), (1, 2))
        )
        endpoint_dark = A == B
        matching_dark = x0 == x1 == x2
        tangent = not any(derivatives)
        require(derivatives == expected
                and tangent == (endpoint_dark or matching_dark),
                ("the Segre tangent iff changed", raw, derivatives, expected))
        samples += 1
        tangent_samples += tangent
        bright += not tangent
        endpoint_dark_only += endpoint_dark and not matching_dark
        matching_dark_only += matching_dark and not endpoint_dark
        both_dark += endpoint_dark and matching_dark
    require(samples == 5 ** 5
            and tangent_samples == (
                endpoint_dark_only + matching_dark_only + both_dark
            ),
            "the zero-inclusive Segre tangent census changed")
    return {
        "matrix": "[[A*x0,A*x1,A*x2],[B*x0,B*x1,B*x2]]",
        "direction": "the all-ones 2x3 occurrence shear",
        "linearized_minors_01_02_12": [
            "(A-B)(x0-x1)",
            "(A-B)(x0-x2)",
            "(A-B)(x1-x2)",
        ],
        "exact_iff_over_field": "A=B or x0=x1=x2",
        "zero_cases_included": True,
        "grid_samples": samples,
        "grid_tangent": tangent_samples,
        "grid_bright": bright,
        "grid_endpoint_dark_only": endpoint_dark_only,
        "grid_matching_dark_only": matching_dark_only,
        "grid_both_dark": both_dark,
        "ring_scope": (
            "field/integral domain; the reverse implication can fail over "
            "a ring with zero divisors"
        ),
    }


def representation_dark_arm_audit() -> dict[str, object]:
    # Endpoint invariant/odd splitting and matching invariant/standard
    # splitting.  Two independent minor rows span odd_endpoint tensor
    # matching_standard.
    endpoint_invariant = tuple(map(Q, (1, 1)))
    endpoint_odd = tuple(map(Q, (1, -1)))
    matching_invariant = tuple(map(Q, (1, 1, 1)))
    matching_standard = (
        tuple(map(Q, (1, -1, 0))),
        tuple(map(Q, (1, 0, -1))),
    )
    require(rank((endpoint_invariant, endpoint_odd)) == 2
            and rank((matching_invariant,) + matching_standard) == 3,
            "the endpoint/matching representation splitting changed")
    return {
        "conormal_representation": (
            "endpoint-odd line tensor the two-dimensional matching-standard "
            "module"
        ),
        "endpoint_dark_arm": {
            "equation": "A=B",
            "endpoint_odd_value": 0,
            "surviving_coefficient_sector": "matching-standard x_i-x_j",
            "existing_physical_result": (
                "the residual-flip V4 standard module is rationally "
                "contractible by normalized C2 bars once a termwise "
                "PP-natural pointed source section is supplied"
            ),
            "current_gap": (
                "the aggregate matching face does not supply those termwise "
                "bars or transport them to cap/E14 repeated grade"
            ),
        },
        "matching_dark_arm": {
            "equation": "x0=x1=x2",
            "matching_standard_value": [0, 0],
            "surviving_coefficient_sector": "endpoint-odd A-B",
            "existing_physical_result": (
                "the endpoint-odd Cartan prism is source-provenant and "
                "target-safe on its canonical physical source orbit"
            ),
            "current_gap": (
                "its existence does not place the universal response KS "
                "generator or its cap/E14 augmented readouts"
            ),
        },
        "intersection": (
            "A=B and x0=x1=x2: the block is invariant in both factors and "
            "the all-ones direction has no toric conormal face"
        ),
        "one_factor_brightness_in_a_dark_arm_is_a_terminal": False,
    }


def nonzero_arm_incidence_audit() -> dict[str, object]:
    # Small bright point: the two independent linearized minors are nonzero.
    A, B = Q(1), Q(0)
    values = (Q(1), Q(0), Q(0))
    derivatives = tuple(
        linearized_minor(A, B, values, left, right)
        for left, right in ((0, 1), (0, 2), (1, 2))
    )
    require(derivatives == (Q(1), Q(1), Q(0)),
            "the minimal bright Segre point changed")

    # Current typed factors live in the response coefficient/conormal block.
    # The active-fan input has separate coordinates: an offdiagonal physical
    # cell, its signed cofactor/common-q, and a complete mixed-row incidence.
    # Keeping these as independent summands freezes the missing map.
    toric_product = tuple(map(Q, (1, 0, 0)))
    offdiagonal_cell = tuple(map(Q, (0, 1, 0)))
    signed_cofactor = tuple(map(Q, (0, 0, 1)))
    require(rank((toric_product, offdiagonal_cell, signed_cofactor)) == 3,
            "the toric/private-site incidence guard changed")
    return {
        "minimal_bright_values": {
            "A": 1, "B": 0, "x": [1, 0, 0],
            "linearized_minors": [1, 1, 0],
        },
        "positive_information": (
            "both the endpoint-odd value and one matching-standard value "
            "are nonzero in one same-word Segre conormal"
        ),
        "current_tail_decorations": "residual q_ij:00 products",
        "current_endpoint_factor": (
            "p1*s0-p0*s1, an orientation/KS line rather than an individual "
            "offdiagonal decorated pair cell"
        ),
        "evaluated_private_site_fan_follows_now": False,
        "direct_sum_rank_toric_cell_cofactor": 3,
        "first_missing_incidence": (
            "a source-labelled, grade-preserving map which sends one "
            "endpoint-odd summand to an actual nonzero offdiagonal cell "
            "e=A_uv^(ab), a!=b, and the same residual matching-standard "
            "summand to its signed physical cofactor/common-q in one "
            "complete zero mixed-response row"
        ),
        "conditional_landing": (
            "after that incidence square, nonzero product gives the "
            "source-provenant private-site fan; complete pure supports then "
            "give four-good or a literal pure-colour coloop"
        ),
        "not_supplied_by": [
            "coefficient factorization alone",
            "the endpoint-odd Cartan prism alone",
            "the aggregate matching face alone",
            "physical q/anchor shadows, which vanish on the mixed conormal",
        ],
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "universal response 2x3 Segre tangent dark-arm gate",
        "pins": PINS,
        "exact_tangent_iff": exact_tangent_iff_audit(),
        "representation_and_dark_arms": representation_dark_arm_audit(),
        "nonzero_arm_private_site_incidence": nonzero_arm_incidence_audit(),
        "verdict": (
            "The all-ones occurrence shear is tangent to the fixed-endpoint "
            "2x3 Segre block exactly when A=B or x0=x1=x2, including every "
            "zero degeneration.  These are respectively endpoint-odd dark "
            "and matching-standard dark.  The former reduces to the "
            "conditional residual-flip bar construction; the latter to the "
            "already source-provenant endpoint-odd Cartan prism.  A nonzero "
            "mixed product is a genuine toric conormal but is not yet an "
            "evaluated private-site fan: the missing datum is one literal "
            "incidence square identifying its factors with an offdiagonal "
            "decorated cell and its physical cofactor in the same row/grade."
        ),
        "scope": (
            "canonical h=3 response 2x3 endpoint/matching block over a "
            "characteristic-zero field.  No full GHZ counterexample, "
            "terminal promotion, or active-fan incidence is claimed."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    tangent = ledger["exact_tangent_iff"]
    print("Segre all-ones tangent iff: A=B OR x0=x1=x2")
    print("zero-inclusive samples:", tangent["grid_samples"])
    print("endpoint-dark: MATCHING-STANDARD BAR CONDITIONAL")
    print("matching-dark: ENDPOINT-ODD CARTAN PHYSICAL, PLACEMENT OPEN")
    print("bright arm: OFFDIAGONAL CELL/COFACTOR INCIDENCE OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

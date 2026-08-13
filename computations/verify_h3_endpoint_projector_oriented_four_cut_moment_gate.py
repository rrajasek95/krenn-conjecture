#!/usr/bin/env python3
"""Audit the endpoint-projector route to the oriented c0/c1 carriers.

The h=3 association projector reconstructs occurrence coefficients from a
centered part plus the constant augmentation.  It does not by itself give a
chain-level restriction/insertion map to the two oriented four-cut carriers.
If such one common physical map is supplied, the two curvature factors add
to 2q-r and the dark-dark branch is exactly c0=0.  A first unweighted
endpoint/Hasse face does not determine c1: an explicit polynomial bubble
preserves the unweighted moment and endpoint 1-jets but changes the first
weighted moment.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md":
        "48e39dd9e2667208eb2a08d98aa5dc58151daeaa7029437270d92a966c9e2542",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "notes/scalar-unit-c0-four-cut-common-carrier-gate.md":
        "a06018da73d6a954f14706fcfdeaae5ace1c2424e02530ab87602c1e77271000",
    "computations/verify_scalar_unit_c0_four_cut_common_carrier_gate.py":
        "56421c894acd613300841b7ae41d1bafecc6d65fcc9618982dc61ac198c2fa66",
    "notes/scalar-unit-moment-transgression-source-lift-based-loop-torsor.md":
        "8df4b715775194282542cf1ea057b8305223744504687e5e480c4c262fcecd4a",
    "computations/verify_scalar_unit_moment_transgression_source_lift_based_loop_torsor.py":
        "4bff53e1568a74cfe262fac185558aa14337fe1a2e31e6c46141645e78e8e839",
    "notes/uniform-hasse-moment-augmented-membership-gate.md":
        "2b111d884b3cb8ad332cbdaf8b96b3a8d442517e20171bbad7ad4cfe542f054f",
    "computations/verify_uniform_hasse_moment_augmented_membership_gate.py":
        "f5f663715507d46e6d96b37a1a05c21e9f0b045dcedd878bf657dfb4b32091c3",
}
EXPECTED_LEDGER_SHA256 = (
    "dc74d4b55fbde24c60dc9c8972da17df6ecec0549d8647016f636eb4e7e72ad7"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def centered_reconstruction_audit() -> dict[str, object]:
    """Check C=90I-J and the indispensable constant augmentation."""
    count = 90
    samples = [
        [Fraction((11 * index + 7) % 13 - 6) for index in range(count)],
        [Fraction(1 if index in (0, 17, 89) else 0) for index in range(count)],
    ]
    records = []
    for vector in samples:
        augmentation = sum(vector, Fraction(0))
        centered = [count * entry - augmentation for entry in vector]
        require(sum(centered, Fraction(0)) == 0,
                "centered projector gained augmentation")
        recovered = [
            (entry + augmentation) / count for entry in centered
        ]
        require(recovered == vector,
                "centered plus constant failed to reconstruct")
        # Adding a constant changes the augmentation and not the normalized
        # centered component.  Thus centered data alone misses one line.
        shifted = [entry + 1 for entry in vector]
        shifted_augmentation = sum(shifted, Fraction(0))
        shifted_centered = [
            count * entry - shifted_augmentation for entry in shifted
        ]
        require(shifted_centered == centered,
                "constant line became visible to centered projector")
        records.append({
            "augmentation": str(augmentation),
            "centered_sum": str(sum(centered, Fraction(0))),
            "constant_shift_is_invisible": True,
        })
    return {
        "occurrences": count,
        "operator": "C=90 I-J",
        "formula": "y=(Cy+augmentation(y)*1)/90",
        "centered_rank": 89,
        "missing_line": "constant H0 augmentation",
        "samples": records,
    }


def oriented_dark_dark_audit() -> dict[str, object]:
    """Verify exact orientation signs on one common carrier."""
    # Basis q,r,x.  x is the orientation-swapped response term.
    right = [Fraction(1), Fraction(0), Fraction(-1)]
    left = [Fraction(1), Fraction(-1), Fraction(1)]
    total = [a + b for a, b in zip(right, left, strict=True)]
    require(total == [Fraction(2), Fraction(-1), Fraction(0)],
            "oriented curvature sum changed")
    c_zero = [-entry for entry in total]
    require(c_zero == [Fraction(-2), Fraction(1), Fraction(0)],
            "c0 sign changed")

    # This implication uses one common H0.  It does not hold for unrelated
    # restricted carriers; an explicit scalar sample records the mismatch.
    q, r, x = Fraction(3), Fraction(5), Fraction(1)
    h_right, h_left = Fraction(0), Fraction(7)
    k_right = dot(right, [q, r, x])
    k_left = dot(left, [q, r, x])
    require(k_right * h_right == 0, "right test is not dark")
    require(k_left * h_left != 0, "restricted-carrier test collapsed")
    return {
        "K_right": "q-x",
        "K_left": "q-r+x",
        "sum": "2q-r",
        "common_dark_dark": "(r-2q)H0=0",
        "hypothesis": (
            "one source-valid chain map whose two projections use the same "
            "H0 before evaluation"
        ),
        "not_supplied_by_C": (
            "orientation multiplication and restriction/insertion "
            "base-change"
        ),
    }


def polynomial_value(coefficients: list[Fraction], value: Fraction) -> Fraction:
    return sum((coefficient * value ** degree
                for degree, coefficient in enumerate(coefficients)),
               Fraction(0))


def derivative(coefficients: list[Fraction]) -> list[Fraction]:
    return [
        Fraction(degree) * coefficient
        for degree, coefficient in enumerate(coefficients)
        if degree
    ]


def integral(coefficients: list[Fraction], weight: int = 0) -> Fraction:
    return sum((coefficient / Fraction(degree + weight + 1)
                for degree, coefficient in enumerate(coefficients)),
               Fraction(0))


def first_moment_counterguard_audit() -> dict[str, object]:
    """A based bubble invisible to H0 and endpoint 1-jets changes H1."""
    # z=t^2(1-t)^2(t-1/2)
    z = [
        Fraction(0), Fraction(0), Fraction(-1, 2), Fraction(2),
        Fraction(-5, 2), Fraction(1),
    ]
    dz = derivative(z)
    require(polynomial_value(z, Fraction(0)) == 0
            and polynomial_value(z, Fraction(1)) == 0,
            "bubble stopped vanishing at endpoints")
    require(polynomial_value(dz, Fraction(0)) == 0
            and polynomial_value(dz, Fraction(1)) == 0,
            "bubble stopped preserving endpoint first jets")
    unweighted = integral(z)
    weighted = integral(z, weight=1)
    require(unweighted == 0, "bubble changed H0")
    require(weighted == Fraction(1, 840),
            ("first weighted residue changed", weighted))
    return {
        "bubble": "t^2(1-t)^2(t-1/2)",
        "endpoint_values": ["0", "0"],
        "endpoint_first_derivatives": ["0", "0"],
        "unweighted_integral": str(unweighted),
        "first_weighted_integral": str(weighted),
        "consequence": (
            "unweighted endpoint-projector data, even with endpoint "
            "1-jets, does not determine H1"
        ),
    }


def source_typing_audit() -> dict[str, object]:
    endpoint = (ROOT / "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md").read_text()
    c_zero = (ROOT / "notes/scalar-unit-c0-four-cut-common-carrier-gate.md").read_text()
    loops = (ROOT / "notes/scalar-unit-moment-transgression-source-lift-based-loop-torsor.md").read_text()
    require("01211222" in endpoint
            and "t*q_(v,N),  odd-site type P3+K2" in endpoint,
            "endpoint projector word/fine grade changed")
    require("common-carrier typing" in c_zero
            and "first **weighted moment**" in c_zero,
            "oriented comparison scope changed")
    require("common carrier needs a chain-level base-change square" in loops.lower()
            and "zero indeterminacy" in loops.lower(),
            "based-loop source criterion changed")
    return {
        "endpoint_projector_scope": "h=3, N=90",
        "endpoint_projector_word": "01211222",
        "endpoint_projector_fine_grade": "t_v*q_(v,N), repeated P3+K2",
        "four_cut_scope": (
            "general scalar-unit selected top-word carrier with ordered "
            "response endpoints"
        ),
        "unproved_grade_map": (
            "a source-valid word/fine/repeated-grade map from the local "
            "projector cap to both complete oriented H0 restrictions"
        ),
        "parameter_warning": (
            "the common-tail cell t_v is a physical decorated-cell "
            "multiplier; it is not the affine integration parameter t "
            "whose weight defines H1"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 endpoint projector / oriented four-cut moment gate",
        "pins": PINS,
        "centered_reconstruction": centered_reconstruction_audit(),
        "oriented_composition": oriented_dark_dark_audit(),
        "moment_counterguard": first_moment_counterguard_audit(),
        "typing": source_typing_audit(),
        "verdict": (
            "Coefficientwise, the endpoint projector reconstructs every "
            "occurrence family only after adjoining its constant H0 "
            "augmentation.  If one physical common-tail lift commutes with "
            "both ordered four-cut restrictions and orientation "
            "multiplication, its two projections are K_right H0 and "
            "K_left H0; a nonzero projection is the existing active-clean "
            "branch and two zero projections give c0=0.  The committed "
            "projector has no such word/fine/repeated-grade base-change "
            "map.  Its unweighted or first endpoint face also does not give "
            "c1: the displayed based bubble preserves H0 and endpoint "
            "1-jets but changes H1.  A horizontal weighted one-form / "
            "Bockstein with zero loop residue remains separate."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("endpoint/four-cut moment ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("endpoint occurrence projector: COEFFICIENT RECONSTRUCTION ONLY")
    print("common physical orientation lift => active-clean OR c0=0")
    print("first unweighted/endpoint Hasse face => c1: FALSE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""The physical Koszul cell cannot absorb the shifted filler Eq defect.

Over R=Q[u,H0,Hm], put F0=H0-u and

  d r0 = F0 eEq,  d rm = Hm eEq,  d T = -Yw,
  K_m = Hm*r0-F0*rm.

Then dK_m=0 and, for every polynomial c,

  d((r0-T)+c*K_m) = Yw+F0*eEq.

Even allowing an arbitrary polynomial b*rm would require b*Hm=-F0.
Specialization Hm=H0=0 leaves u=0, impossible in Q[u].
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    "notes/h3-shifted-denominator-chart-filler-augmented-commutator.md":
        "1d89c1e592fdc723bb58b1b75e2ba846b812401efad33c8cd88d4265dc0a7743",
    "computations/verify_h3_single_koszul_cell_face_star_no_go.py":
        "5b94a8b213213ce64dd8536baf638e619a4773a2dfc4a2318e1820742f8f8165",
    "notes/h3-single-koszul-cell-face-star-no-go.md":
        "b9b3051f929e7704ac95b645d2a7a3ede3cd5bd7684fda12117e7d96847a9d4b",
}
EXPECTED_LEDGER_SHA256 = "9b63dd33425b1086103ee324a8dd5fa41ee7a219fc9b43b406342c8581155dc7"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def poly_add(left, right):
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, 0) + coefficient
        if not answer[monomial]:
            del answer[monomial]
    return answer


def poly_scale(value, polynomial):
    return {monomial: value * coefficient
            for monomial, coefficient in polynomial.items()
            if value * coefficient}


def poly_multiply(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b
                             in zip(left_monomial, right_monomial))
            answer[monomial] = (answer.get(monomial, 0)
                                + left_coefficient * right_coefficient)
            if not answer[monomial]:
                del answer[monomial]
    return answer


ZERO = {}
ONE = {(0, 0, 0, 0): 1}
U = {(1, 0, 0, 0): 1}
H0 = {(0, 1, 0, 0): 1}
HM = {(0, 0, 1, 0): 1}
C = {(0, 0, 0, 1): 1}  # a universal polynomial coefficient is enough
F0 = poly_add(H0, poly_scale(-1, U))


def chain_add(left, right):
    answer = dict(left)
    for generator, coefficient in right.items():
        answer[generator] = poly_add(answer.get(generator, ZERO), coefficient)
        if not answer[generator]:
            del answer[generator]
    return answer


def chain_scale(coefficient, chain):
    return {generator: poly_multiply(coefficient, value)
            for generator, value in chain.items()}


def differential(chain):
    # Output coordinates are Eq and Yw.
    answer = {}
    maps = {
        "r0": {"Eq": F0},
        "rm": {"Eq": HM},
        "T": {"Yw": poly_scale(-1, ONE)},
    }
    for generator, coefficient in chain.items():
        for output, value in maps[generator].items():
            answer[output] = poly_add(
                answer.get(output, ZERO), poly_multiply(coefficient, value)
            )
            if not answer[output]:
                del answer[output]
    return answer


def specialize_hm_h0_zero(polynomial):
    # Retain only monomials whose H0 and Hm exponents vanish; result is in
    # Q[u,c].
    return {(monomial[0], monomial[3]): coefficient
            for monomial, coefficient in polynomial.items()
            if monomial[1] == 0 and monomial[2] == 0}


def audit():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")

    koszul = chain_add(
        chain_scale(HM, {"r0": ONE}),
        chain_scale(poly_scale(-1, F0), {"rm": ONE}),
    )
    require(differential(koszul) == {},
            "K_m stopped being the physical closed Koszul cell")

    shifted = {"r0": ONE, "T": poly_scale(-1, ONE)}
    shifted_boundary = differential(shifted)
    require(shifted_boundary == {"Eq": F0, "Yw": ONE},
            "the shifted filler boundary changed")
    corrected = chain_add(shifted, chain_scale(C, koszul))
    require(differential(corrected) == shifted_boundary,
            "a polynomial multiple of K_m changed the Eq defect")

    # A more general correction b*rm changes Eq by b*Hm.  Cancellation
    # would give b*Hm=-F0.  The specialization Hm=H0=0 has zero left side
    # and +u on the right, proving nonmembership without localization.
    arbitrary_b = poly_add(ONE, C)
    cancellation_equation = poly_add(poly_multiply(arbitrary_b, HM), F0)
    specialized = specialize_hm_h0_zero(cancellation_equation)
    require(specialized == {(1, 0): -1},
            "the Hm=H0=0 nondivisibility witness changed")

    ledger = {
        "ring": "Q[u,H0,Hm,c]",
        "physical_differential": {
            "d(r0)": "(H0-u)e_Eq",
            "d(rm)": "Hm e_Eq",
            "d(T)": "-Yw",
        },
        "koszul_cell": "K_m=Hm*r0-(H0-u)*rm",
        "identities": {
            "dK_m": "0",
            "d((r0-T)+cK_m)": "Yw+(H0-u)e_Eq",
        },
        "general_rm_correction": (
            "b*rm cancels Eq only if b*Hm=-(H0-u), impossible because "
            "Hm=H0=0 specializes this equation to 0=u"
        ),
        "earliest_residual": "F0 e_Eq; at q=0 it is -u e_Eq",
        "required_new_input": (
            "a genuine target/residue-zero lower face with Eq boundary 1, "
            "or a localization/divisibility theorem not present in the "
            "underived polynomial source"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Koszul absorption no-go ledger changed: {digest}")
    return ledger, digest


def main():
    _, digest = audit()
    print("h3 shifted filler Koszul absorption no-go: PASS")
    print("d((r0-T)+cK_m)=Yw+F0*e_Eq for every polynomial c")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()

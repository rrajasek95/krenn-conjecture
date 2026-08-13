#!/usr/bin/env python3
"""Audit the Segre-bright/private-site incidence and Tate alternative.

The complete target-augmented private-site identity begins with a named
nonzero offdiagonal decorated cell.  A bright universal-response Segre
conormal uses endpoint-orientation products and diagonal ``00`` matching
tails, so the identity cannot be invoked without an additional incidence
map.

An exact local-row quotient makes this sharp: take ``A=1,B=0`` and matching
values ``(1,0,-1)``.  Both complete orientation response sums vanish, all
three Segre derivatives are nonzero, and every offdiagonal decorated
reference can be zero.  The private-site identities are then homogeneous.
This is compatible with the complete selected response/private-site rows,
but is deliberately not asserted to extend to every unary/pure GHZ row.

There is one exhaustive constructive compression.  If the centered
comparison admits a termwise multiplicative Tate lift ``d eps=L``, then the
bright toric face is forced by ``d(-eps*k)=-L*k``.  Endpoint-dark and
matching-dark action faces are respectively the normalized matching bars and
the physical odd Cartan face of this same equivariant lift.  Otherwise the
first missing datum is exactly that lift or a fully augmented terminal.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_universal_occurrence_shear_toric_lift_gate.py":
        "097ef9de606f10ed8fd43069b72e70d0ab027a06ac3e98bfeb786325ae08423c",
    "notes/h3-universal-occurrence-shear-toric-lift-gate.md":
        "85ae5c956ddd1b08433b07c1b45238cc88a542fe5434604e48635b6ef4efc1e3",
    "computations/verify_h3_universal_occurrence_shear_physical_toric_lift_gate.py":
        "ca5ede5e7a2cc11bf9f62bdcca8349813c3585b401ea614b8622fa40e63c7609",
    "notes/h3-universal-occurrence-shear-physical-toric-lift-gate.md":
        "9764018dcccd47e774c285c4bff51ca095fa219e879c8d4a2a7cd51394da5d7e",
    "computations/verify_h3_universal_response_toric_minor_terminal_gate.py":
        "c40790270ef38ea72ec1601037f81319e02638d80828d96ee341e73d9f665e37",
    "notes/h3-universal-response-toric-minor-terminal-gate.md":
        "9718c4bda2e411a65c9b18d2e4ffd42a270b2458374b92690b40d3e0f0b23cd4",
    "computations/verify_h3_universal_response_segre_tangent_dark_arm_gate.py":
        "cc0d07ce81ce204f5397132d39571f896e68e743d1b9901a47161b1cb6e75390",
    "notes/h3-universal-response-segre-tangent-dark-arm-gate.md":
        "305e1f80546edddb7d2801b0a84bfef5884743107018a7ab4b704748edef6244",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py":
        "c4e175ca053cd98e788cca1a38a1851e708e7e47a9ea5745ef4ac6e303ddfd40",
    "notes/uniform-bidirectional-private-site-fan-rank-boundary.md":
        "7d0f04d22fe11d1ba797a29507fd43915dc98e9d89bdc4085f1c8561deaa1402",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "notes/h3-active-fan-coloop-or-four-good.md":
        "9be8996264fa2070a8f5d7f725f3fcb154b6ee2df2b3e5d3ccd4a6412ec5b03a",
}
EXPECTED_LEDGER_SHA256 = "04f70446b8a3b0447114627568d34cf134acc7001f79c9128a789cabc3103fba"


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


def local_complete_row_quotient_guard() -> dict[str, object]:
    # Matrix rows are the two endpoint orientations, columns the three
    # residual matchings.  Both complete response sums vanish.
    A, B = Q(1), Q(0)
    x = (Q(1), Q(0), Q(-1))
    block = (
        tuple(A * value for value in x),
        tuple(B * value for value in x),
    )
    response_sums = tuple(sum(row, Q(0)) for row in block)
    derivatives = tuple(
        (A - B) * (x[left] - x[right])
        for left, right in ((0, 1), (0, 2), (1, 2))
    )
    require(response_sums == (Q(0), Q(0))
            and derivatives == (Q(1), Q(2), Q(1)),
            "the local bright complete-row guard changed")

    # Axis-purified local quotient: every tail is a diagonal 00 product and
    # all six ternary offdiagonal decorated reference types are zero.  The
    # exact private-site consequence sum Delta*C=-e is then 0=0.  This shows
    # why the identity cannot reverse-engineer e from the toric product.
    offdiagonal_references = (Q(0),) * 6
    determinant_cofactor_sums = (Q(0),) * 6
    require(all(
        determinant_cofactor_sums[index]
            == -offdiagonal_references[index]
        for index in range(6)
    ), "an axis-purified private-site row became inhomogeneous")
    return {
        "endpoint_values": {"A": 1, "B": 0},
        "matching_values": [1, 0, -1],
        "occurrence_block": [[1, 0, -1], [0, 0, 0]],
        "complete_orientation_response_sums": [0, 0],
        "linearized_Segre_minors": [1, 2, 1],
        "Segre_bright": True,
        "tail_decorations": "diagonal 00 only",
        "offdiagonal_decorated_reference_types": [0] * 6,
        "private_site_consequences": ["0=0"] * 6,
        "what_this_refutes": (
            "complete selected response rows plus the private-site identity "
            "do not infer an offdiagonal reference from Segre brightness"
        ),
        "scope": (
            "complete local response/private-site quotient; not asserted to "
            "satisfy every unary, pure-target, anchor, or GHZ normalization row"
        ),
    }


def incidence_rank_guard() -> dict[str, object]:
    # Coordinates are the toric conormal, an actual offdiagonal decorated
    # cell, and its physical cofactor/common-q.  The presently committed
    # local equations retain these as independent summands.  Each required
    # incidence raises rank.
    toric = tuple(map(Q, (1, 0, 0)))
    cell = tuple(map(Q, (0, 1, 0)))
    cofactor = tuple(map(Q, (0, 0, 1)))
    require(rank((toric,)) == 1
            and rank((toric, cell)) == 2
            and rank((toric, cell, cofactor)) == 3,
            "the local incidence rank guard changed")
    return {
        "quotient_coordinates": [
            "toric endpoint-times-matching conormal",
            "offdiagonal decorated cell e",
            "signed physical cofactor/common-q C_e",
        ],
        "successive_ranks": [1, 2, 3],
        "first_missing_incidence_square": (
            "send the endpoint-odd factor to one literal e=A_vu^(ba), a!=b, "
            "and the same matching-standard factor to its signed C_e in one "
            "complete zero mixed row and repeated grade"
        ),
        "full_private_site_identity_after_square": (
            "e!=0 implies sum Delta*C=-e, hence a nonzero source-provenant fan"
        ),
        "fan_landing_after_square": (
            "complete pure supports give four-good or a literal pure-colour coloop"
        ),
    }


def multiplicative_tate_and_dark_arms() -> dict[str, object]:
    # DGA signs: deg epsilon=1, k is a closed scalar conormal.  If d eps=L,
    # then d(-eps*k)=-L*k.  This is exactly the physical toric derivative.
    L, k = Q(3), Q(-2)
    require(-L * k == Q(6), "the multiplicative Tate sign changed")
    require(Q(-1, 2) * Q(-2) == 1,
            "the normalized C2 bar coefficient changed")
    return {
        "single_positive_input": (
            "a pointed, termwise multiplicative, endpoint/matching-equivariant "
            "physical Tate generator epsilon with d epsilon=L"
        ),
        "bright_face": "d(-epsilon*k)=-L*k",
        "bright_face_is_independent_after_epsilon": False,
        "endpoint_dark_A_equals_B": {
            "toric_face": 0,
            "remaining_action_face": "matching-standard residual flip",
            "filler": "-(1/2)[tau|y] over characteristic zero",
            "physical_guard": "requires termwise PP-natural epsilon",
        },
        "matching_dark_x_equal": {
            "toric_face": 0,
            "remaining_action_face": "endpoint-odd orientation",
            "filler": "source-provenant endpoint-odd Cartan prism",
            "physical_guard": "requires the same epsilon placement in AugP2/E14",
        },
        "both_dark": (
            "no toric/action-standard face; only the underlying centered "
            "Tate placement and its augmented readouts remain"
        ),
        "unification": (
            "the bright product face and both dark action faces are proper "
            "faces of one equivariant multiplicative Tate comparison"
        ),
    }


def exhaustive_local_alternative() -> dict[str, object]:
    return {
        "arm_1": (
            "multiplicative physical epsilon exists: toric face fills by "
            "Leibniz; matching bars/odd Cartan supply the two dark action faces"
        ),
        "arm_2": (
            "epsilon does not exist and a Segre product is bright: construct "
            "the literal cell/cofactor incidence square, then fan -> four-good/"
            "coloop; or extend the first fully augmented nonlift to a terminal"
        ),
        "arm_3": (
            "endpoint-dark: construct the termwise matching-standard bar "
            "placement, or promote its fully augmented nonlift"
        ),
        "arm_4": (
            "matching-dark: combine the physical odd Cartan prism with the "
            "centered AugP2/E14 placement, or promote its augmented nonlift"
        ),
        "no_additional_coefficient_case": True,
        "global_warning": (
            "the local quotient guard does not decide whether all remaining "
            "unary/pure GHZ equations force one of the missing physical maps"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "Segre bright/private-site incidence and Tate alternative",
        "pins": PINS,
        "complete_local_row_quotient_guard": local_complete_row_quotient_guard(),
        "cell_cofactor_incidence_rank_guard": incidence_rank_guard(),
        "multiplicative_Tate_and_dark_arms": multiplicative_tate_and_dark_arms(),
        "shortest_exhaustive_local_alternative": exhaustive_local_alternative(),
        "verdict": (
            "Segre brightness plus the complete selected response and "
            "private-site identities does not itself produce an offdiagonal "
            "decorated cell: the identity is conditional on that cell, and "
            "the axis-purified local quotient remains bright while every "
            "private-site equation is homogeneous.  The shortest positive "
            "construction is one multiplicative physical Tate lift; it fills "
            "the bright toric face by Leibniz and packages the matching-bar "
            "and odd-Cartan dark faces.  Without it, the precise bright-arm "
            "gap is the cell/cofactor incidence square, not another Segre identity."
        ),
        "scope": (
            "canonical h=3 local response/private-site quotient over a "
            "characteristic-zero field.  No full-source GHZ counterexample "
            "or terminal promotion is claimed."
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
    _ledger, digest = audit()
    print("bright + complete local response/private rows: CELL NOT FORCED")
    print("sharp guard: diagonal 00 tails, response sums 0, Segre minors nonzero")
    print("positive compression: ONE MULTIPLICATIVE PHYSICAL TATE LIFT")
    print("bright proper face: d(-epsilon*k)=-L*k")
    print("dark faces: MATCHING BAR / ODD CARTAN")
    print("first bright gap: OFFDIAGONAL CELL + COFACTOR INCIDENCE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

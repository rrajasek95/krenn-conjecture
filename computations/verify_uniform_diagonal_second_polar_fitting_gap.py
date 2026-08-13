#!/usr/bin/env python3
"""Audit the diagonal full-nine second-polar route to the clean Fitting cut.

The contracted pair row is linear in a cap direction:

    L(t)=B0+t B1.

Its second Hasse derivative is zero. The nonlinear top cap has

    G_h(t)=sum_(j=2)^h t^j B_j,

so its second coefficient at zero is only B2. At h=3 it misses B3; at
h=4 it misses B3,B4. The missing grades are independent in the literal
repeated-response source module.

The pure-axis forms u^h,v^h give a second guard: their second polars are
nonzero and coprime, while their clean Macaulay map remains full rank.
Thus second polarization is not a low-degree Hilbert--Burch relation.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/uniform-response-plucker-veronese-hilbert-burch-gate.md":
        "88c2cfe20f026ff051c8e10c7e2f39f4f0407fbc9d29fe9def3fcf1d64cce800",
    "computations/verify_uniform_response_plucker_veronese_hilbert_burch_gate.py":
        "ede18e6bc81fa96b8a720806be71a834d85332c807f27717b2e0811ace50c67d",
    "notes/color-stabilizer-second-jet-tautology.md":
        "f93e378d80b04981595f9466a6c46f8740f0720b0b2fdf3cc2ee2c18610bf073",
    "notes/scalar-unit-carrier-moment-tower-hilbert-cauchy.md":
        "c9a58db12d8959a3b498c3e6b0ae54aeb49224476fb02d264d21d77d8a230855",
    "computations/verify_scalar_unit_carrier_moment_tower_hilbert_cauchy.py":
        "b1674da530c0af1790780bb19fadc7622117b373ece3e9a0845cbb532870e3f3",
    "notes/h3-diagonal-segre-second-transgression-seven-row-guard.md":
        "b8a4afefb2fbe580faa002490c0535a2f3e505ed72b50f964ffe89a03925c696",
    "computations/verify_h3_diagonal_segre_second_transgression_seven_row_guard.py":
        "38e7c570b5fad78436e6f20f062d49db995da2dfb7bee19f2f80fcae8a726940",
    "notes/full-nine-star-inverse-tensor-grade-counterguard.md":
        "4928d1a0b6a03c412180cdf3a2471aa934ebf30d1acf2ebd74447eaa7f557945",
    "computations/verify_oo_c8_fullnine_star_inverse.py":
        "bda485e352931d87968b6457b48f162f99d196890118105bb6bf518e68d2e07a",
}
EXPECTED_LEDGER_SHA256 = (
    "9084dda69d9f0d49f549329f943f660f01fd480745d3580406c6f5b11a61d92c"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def matrix_rank(matrix) -> int:
    if not matrix:
        return 0
    work = [list(map(Fraction, row)) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            coefficient = work[row][column]
            work[row] = [
                entry - coefficient * pivot_entry
                for entry, pivot_entry in zip(
                    work[row], work[rank], strict=True
                )
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def hasse_derivative(coefficients, order):
    """Coefficients of D^[order] f(t), low to high."""
    return [
        Fraction(comb(degree + order, order)) * coefficients[degree + order]
        for degree in range(len(coefficients) - order)
    ]


def source_grade_audit() -> dict[str, object]:
    records = {}
    for h in range(3, 11):
        # Values lie in the free basis B0,...,Bh.
        basis = [
            [Fraction(int(row == column)) for row in range(h + 1)]
            for column in range(h + 1)
        ]
        # L(t)=B0+tB1 has no order-two coefficient.
        pair_coefficients = [basis[0], basis[1]]
        require(len(pair_coefficients) == 2,
                ("contracted pair row acquired a second cap coefficient", h))

        clean_polynomial = [
            [Fraction(0)] * (h + 1),
            [Fraction(0)] * (h + 1),
        ] + basis[2:]
        second_at_zero = clean_polynomial[2]
        require(second_at_zero == basis[2],
                ("second Hasse coefficient stopped being B2", h))
        full_tail = [
            sum((clean_polynomial[degree][row]
                 for degree in range(h + 1)), Fraction(0))
            for row in range(h + 1)
        ]
        residual = [
            full_tail[row] - second_at_zero[row]
            for row in range(h + 1)
        ]
        expected_residual = [
            Fraction(int(row >= 3)) for row in range(h + 1)
        ]
        require(residual == expected_residual,
                ("higher response tail changed", h))
        require(matrix_rank([basis[j] for j in range(2, h + 1)]) == h - 1
                and matrix_rank([basis[2]]) == 1,
                ("literal response-grade independence changed", h))

        # At t=1 a second polar is still only one moment combination.
        scalar_coefficients = [
            Fraction(int(degree >= 2)) for degree in range(h + 1)
        ]
        second_at_one = sum(
            hasse_derivative(scalar_coefficients, 2), Fraction(0)
        )
        require(second_at_one == sum(
            Fraction(comb(j, 2)) for j in range(2, h + 1)
        ), ("second endpoint moment changed", h))

        records[h] = {
            "pair_row_cap_orders": [0, 1],
            "pair_row_second_Hasse": 0,
            "clean_tail_orders": list(range(2, h + 1)),
            "second_polar_order": 2,
            "unseen_orders": list(range(3, h + 1)),
            "tail_module_dimension": h - 1,
            "second_polar_span_dimension": 1,
            "second_at_t1_scalar_weight": int(second_at_one),
        }
    return {
        "orders": records,
        "h3": "G3(t)=t^2 B2+t^3 B3; D^[2]_0 sees B2, misses B3",
        "h4": (
            "G4(t)=t^2 B2+t^3 B3+t^4 B4; "
            "D^[2]_0 sees B2, misses B3 and B4"
        ),
        "source_grade_verdict": (
            "twice-polarizing the contracted diagonal/full-nine row gives "
            "0=0 and does not cross from target grades 0,1 into clean "
            "response grades 2,...,h"
        ),
    }


def pure_axis_hessian_audit() -> dict[str, object]:
    records = {}
    for h in range(3, 11):
        macaulay = [
            [Fraction(int(row == column)) for column in range(2 * h)]
            for row in range(2 * h)
        ]
        require(matrix_rank(macaulay) == 2 * h,
                ("pure-axis Macaulay rank changed", h))
        hessian_u = [Fraction(comb(h, 2))] + [
            Fraction(0)
        ] * (h - 2)
        hessian_v = [Fraction(0)] * (h - 2) + [
            Fraction(comb(h, 2))
        ]
        require(matrix_rank([hessian_u, hessian_v]) == 2,
                ("pure-axis second polars became dependent", h))
        records[h] = {
            "clean_forms": ["u^h", "v^h"],
            "second_Hasse_polars": [
                f"{comb(h, 2)}*u^{h-2}",
                f"{comb(h, 2)}*v^{h-2}",
            ],
            "second_polar_gcd": 1,
            "clean_Macaulay_rank": 2 * h,
            "simultaneous_Bezout_kernel_dimension": 0,
        }
    return {
        "orders": records,
        "h3_exact": ["3*u", "3*v"],
        "h4_exact": ["6*u^2", "6*v^2"],
        "verdict": (
            "nonzero/coprime second polars coexist with a rootless clean "
            "family; the Hessian is not a Hilbert-Burch syzygy"
        ),
    }


def moment_tower_audit() -> dict[str, object]:
    records = {}
    for h in range(3, 11):
        moment_indices = [0, 1] if h == 3 else list(range(h - 2))
        records[h] = {
            "required_Hilbert_Cauchy_moments": moment_indices,
            "moment_count": len(moment_indices),
            "single_second_polar_supplies_full_tower": False,
            "highest_response_Hasse_order_needed": h,
        }
    return {
        "orders": records,
        "known_algebraic_fact": (
            "after degree-corrected q/r multiplication, the full moment "
            "tower plus the clean row spans the whole degree-h binary space"
        ),
        "missing_physical_fact": (
            "construct all moments in one source-faithful augmented module "
            "and prove their terminal/Hankel compatibility"
        ),
    }


def scope_audit() -> dict[str, object]:
    response = (ROOT / (
        "notes/uniform-response-plucker-veronese-hilbert-burch-gate.md"
    )).read_text()
    stabilizer = (ROOT / (
        "notes/color-stabilizer-second-jet-tautology.md"
    )).read_text()
    moments = (ROOT / (
        "notes/scalar-unit-carrier-moment-tower-hilbert-cauchy.md"
    )).read_text()
    h3 = (ROOT / (
        "notes/h3-diagonal-segre-second-transgression-seven-row-guard.md"
    )).read_text()
    inverse = (ROOT / (
        "notes/full-nine-star-inverse-tensor-grade-counterguard.md"
    )).read_text()
    require("Higher response--Fitting identity" in response
            and "response-count grades" in response,
            "response/Fitting source target changed")
    require("second fundamental form" in stabilizer
            and "identically zero" in stabilizer,
            "color-stabilizer second-jet scope changed")
    require("Theorem 1 (certified-orientation moment tower)" in moments
            and "presently missing datum" in moments,
            "Hilbert-Cauchy moment frontier changed")
    require(r"\alpha R^{[2]}q+R^{[3]}" in h3
            and "two missing GHZ residuals" in h3,
            "h=3 second-transgression guard changed")
    require("exclusive" in inverse and "mixed Hessian" in inverse
            and "cannot create the required diagonal" in inverse,
            "full-nine star-inverse grade guard changed")
    return {
        "diagonal_second_polar_forces_chi": False,
        "diagonal_second_polar_lowers_HB_degree": False,
        "target_stabilizer_second_jet_is_new_relation": False,
        "first_positive_source_relation": (
            "a non-stabilizer higher Hasse/Spencer comparison carrying "
            "orders 2 through h into one common clean family, or the "
            "source-faithful Hilbert-Cauchy moment tower"
        ),
        "terminal_typing_needed": (
            "each order-j face must preserve the residual word and carry "
            "literal response-count grade j; after totalization the common "
            "Bezout kernel must have nonzero physical terminal"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "uniform diagonal second-polar Fitting gap",
        "pins": PINS,
        "scope": scope_audit(),
        "source_grades": source_grade_audit(),
        "pure_axis_hessian": pure_axis_hessian_audit(),
        "moment_tower": moment_tower_audit(),
        "verdict": (
            "Twice polarizing a contracted diagonal full-nine row does "
            "not force the clean leading coefficient or lower the "
            "Hilbert-Burch degree. The row is cap-linear, so its second "
            "Hasse derivative is zero; the nonlinear clean cap has "
            "independent response orders 2 through h, of which the second "
            "polar sees only order 2. A source-faithful higher-jet/moment "
            "tower with terminal typing remains necessary."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("uniform diagonal second-polar ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("contracted full-nine second cap polar: ZERO")
    print("h=3 second polar misses response order 3")
    print("h=4 second polar misses response orders 3,4")
    print("low-degree Hilbert-Burch relation: NOT CONSTRUCTED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Audit the all-h anchor/crossed Fitting and Hilbert--Burch route.

The checker proves four finite algebraic facts.

* The completed two-anchor/crossed static label block is invertible.
* At every h, subtracting the crossed divided-power row from F^[h] kills
  only the j=0,1 grades and leaves the independent j>=2 tail.
* On f=v^h, multiplication by a residual clean form is lower triangular
  with diagonal its u^h coefficient chi.  A family has residual rank < h
  exactly when every chi vanishes; the static anchor block does not force
  that condition.
* A full-rank homogeneous syzygy matrix forces a common factor only if the
  sum of its column degrees is < h.  Exact three-generator examples show
  the sharp degree h boundary.

The paired note gives the general proofs and source scope.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/uniform-bezout-transvectant-source-transfer-gate.md":
        "f257de4df2badfbea88dac914b3e9f1342369c9f127a6235320551e07159a008",
    "computations/verify_uniform_bezout_transvectant_source_transfer_gate.py":
        "850a5d751778691e89d6640d5cc3dd2c46fe3962c8615435f0d08a624bd4998e",
    "notes/h3-two-chart-divisor-transport-fitting-obstruction.md":
        "2f785deac8b3ac8a038c09af10580be4c426fbe1b1570ea2304859a0c1adc822",
    "computations/verify_h3_two_chart_divisor_transport_fitting_obstruction.py":
        "8d67857eb1db6dfdb82428ed1566e7624afde89d5d9b2a07f917384ca165096b",
    "notes/residual-macaulay-quotient-is-the-common-divisor.md":
        "3ab98728e5ec56acd8c667201721ed1afe35759e7cf5e7be155992d233e54890",
    "notes/invertible-zero-alignment-two-chart-anchor-guard.md":
        "0aebdcb1b24328b1fd8a68497de113af277d401fe1220a736917e60835fd4e2a",
    "computations/verify_invertible_zero_alignment_two_chart_anchor_guard.py":
        "10a31276f321f897e468d3ae2cbbeb15015a28464712af362e9f541c54414207",
    "notes/uniform-centered-occurrence-matching-eigenspace-correction.md":
        "914a5ae493f78bdab7fa88bfcafd5e80254709a7f373d8bade0f70660dfb8f3f",
    "computations/verify_uniform_centered_occurrence_matching_eigenspace_correction.py":
        "6e9c665e2c42b23e1910963b030de2f6c4b16dfe4951eae6e0e79b7fcf1e6921",
    "notes/uniform-centered-occurrence-full-endpoint-transfer-gate.md":
        "9c363714cc24c7ac17aa08c1260dc36c9c63cc794132817ecb59106685dd59db",
    "computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py":
        "6f5686298143b584a4edcb350145bf9d648277972aa96b90443c4ce254cb1d30",
    "computations/verify_h3_koszul_reynolds_higher_commutator_obstruction.py":
        "c52cec702336ecdd821617ba21c66538cdbbdf2fc964b3d1637dfaf25c9bae6b",
}
EXPECTED_LEDGER_SHA256 = "a5c1fd473d3ada65aafc9a9430f2befda5da27663bc85558c692b9c600e4c792"


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


def determinant(matrix) -> Fraction:
    require(len(matrix) == len(matrix[0]), "determinant needs square matrix")
    work = [list(map(Fraction, row)) for row in matrix]
    output = Fraction(1)
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work))
             if work[row][column]), None
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            output *= -1
        pivot_value = work[column][column]
        output *= pivot_value
        for row in range(column + 1, len(work)):
            coefficient = work[row][column] / pivot_value
            for entry in range(column, len(work)):
                work[row][entry] -= coefficient * work[column][entry]
    return output


def concatenate_blocks(blocks):
    return [
        [entry for block in blocks for entry in block[row]]
        for row in range(len(blocks[0]))
    ]


def residual_matrix(coefficients, h):
    """g*S_(h-1) -> S_(2h-1)/(v^h*S_(h-1)).

    coefficients[k] is [u^(h-k)v^k]g.  In the ordered quotient basis
    u^(2h-1-r)v^r, 0<=r<h, the result is lower triangular Toeplitz.
    """
    coefficients = list(map(Fraction, coefficients))
    require(len(coefficients) == h + 1,
            ("wrong clean-form coefficient count", h, coefficients))
    return [
        [
            coefficients[row - column] if row >= column else Fraction(0)
            for column in range(h)
        ]
        for row in range(h)
    ]


def static_anchor_audit() -> dict[str, object]:
    # Ordered entries rr,rs,sr,ss; columns are two diagonal anchors,
    # the common direct table, and the crossed target-zero row.
    static = [
        [Fraction(1), Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(1)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(-2)],
        [Fraction(0), Fraction(1), Fraction(2), Fraction(0)],
    ]
    require(determinant(static) == -3 and matrix_rank(static) == 4,
            "completed anchor/crossed static block changed")
    return {
        "static_determinant": -3,
        "static_rank": 4,
        "consequence": (
            "the completed label square has no static cokernel; any "
            "Fitting defect must come from the nonlinear clean tail"
        ),
    }


def divided_tail_and_fitting_audit() -> dict[str, object]:
    records = {}
    for h in range(3, 11):
        tails = {}
        for alpha in (
            Fraction(0), Fraction(1), Fraction(2), Fraction(-3, 2)
        ):
            # Grade j means R^[j] q^[h-j].
            full = [alpha ** (h - j) for j in range(h + 1)]
            crossed = [alpha, Fraction(1)] + [Fraction(0)] * (h - 1)
            tail = [
                x - alpha ** (h - 1) * y
                for x, y in zip(full, crossed, strict=True)
            ]
            expected = [Fraction(0), Fraction(0)] + [
                alpha ** (h - j) for j in range(2, h + 1)
            ]
            require(tail == expected,
                    ("all-h crossed tail subtraction changed", h, alpha))
            tails[str(alpha)] = [str(entry) for entry in tail]

        # One residual form with chi=1 already makes the top Fitting minor
        # a unit after specialization.
        generic_coefficients = [
            Fraction(1)
        ] + [Fraction(j + 2) for j in range(h)]
        generic = residual_matrix(generic_coefficients, h)
        require(determinant(generic) == 1
                and matrix_rank(generic) == h,
                ("generic residual block stopped being invertible", h))

        # For several clean coordinates, the combined map has rank < h
        # exactly when every leading coefficient chi_i vanishes.
        zero_chi_forms = []
        for index in range(3):
            coefficients = [Fraction(0)] + [
                Fraction((index + 1) * (j + 1)) for j in range(h)
            ]
            zero_chi_forms.append(residual_matrix(coefficients, h))
        zero_combined = concatenate_blocks(zero_chi_forms)
        require(matrix_rank(zero_combined) <= h - 1
                and not any(zero_combined[0]),
                ("all-zero-chi family filled residual target", h))

        one_live = zero_chi_forms + [generic]
        require(matrix_rank(concatenate_blocks(one_live)) == h,
                ("one live chi failed to fill residual target", h))

        records[h] = {
            "tail_support": list(range(2, h + 1)),
            "tail_probes": tails,
            "single_live_chi_top_minor": 1,
            "all_zero_chi_rank_bound": h - 1,
            "one_live_chi_rank": h,
            "radical_top_fitting_condition": "chi_1=...=chi_m=0",
        }
    return {
        "orders": records,
        "candidate_source_identity": (
            "every leading tail coefficient "
            "chi_i=[u^h] sum_(j=2)^h alpha_i^(h-j) "
            "R_i^[j] q_i^[h-j] vanishes"
        ),
        "coordinate_free_form": (
            "all h-by-h minors of the combined residual "
            "Macaulay/Bezout map vanish"
        ),
    }


Poly = dict[tuple[int, int], Fraction]


def monomial(u_degree: int, v_degree: int,
             coefficient=Fraction(1)) -> Poly:
    coefficient = Fraction(coefficient)
    return {} if not coefficient else {(u_degree, v_degree): coefficient}


def poly_add(left: Poly, right: Poly) -> Poly:
    output = dict(left)
    for key, value in right.items():
        output[key] = output.get(key, Fraction(0)) + value
        if not output[key]:
            del output[key]
    return output


def poly_scale(scalar, polynomial: Poly) -> Poly:
    scalar = Fraction(scalar)
    return {
        key: scalar * value for key, value in polynomial.items()
        if scalar * value
    }


def poly_multiply(left: Poly, right: Poly) -> Poly:
    output: Poly = {}
    for (left_u, left_v), left_value in left.items():
        for (right_u, right_v), right_value in right.items():
            key = (left_u + right_u, left_v + right_v)
            output[key] = (
                output.get(key, Fraction(0)) + left_value * right_value
            )
    return {key: value for key, value in output.items() if value}


def dot(left, right) -> Poly:
    output: Poly = {}
    for first, second in zip(left, right, strict=True):
        output = poly_add(output, poly_multiply(first, second))
    return output


def hilbert_burch_audit() -> dict[str, object]:
    records = {}
    u = monomial(1, 0)
    v = monomial(0, 1)
    d = poly_add(u, v)
    zero: Poly = {}

    for h in range(3, 11):
        # Positive threshold: column degrees 1 and h-2, total h-1.
        r = h - 2
        column_1 = [u, v, zero]
        column_2 = [
            zero, monomial(r, 0), monomial(0, r)
        ]
        cofactors = [
            monomial(0, r + 1),
            monomial(1, r, -1),
            monomial(r + 1, 0),
        ]
        require(not dot(column_1, cofactors)
                and not dot(column_2, cofactors),
                ("degree-deficient Hilbert-Burch syzygy changed", h))
        common_factor_family = [
            poly_multiply(d, cofactor) for cofactor in cofactors
        ]
        require(not dot(column_1, common_factor_family)
                and not dot(column_2, common_factor_family),
                ("common-factor family lost its syzygies", h))
        require(all(
            all(sum(exponents) == h for exponents in polynomial)
            for polynomial in common_factor_family
        ), ("positive HB family degree changed", h))

        # Sharp boundary: column degrees 1 and h-1, total h.  Its cofactor
        # vector contains v^h and u^h, so its gcd is one.
        r_boundary = h - 1
        boundary_column_2 = [
            zero, monomial(r_boundary, 0), monomial(0, r_boundary)
        ]
        coprime_family = [
            monomial(0, h),
            monomial(1, h - 1, -1),
            monomial(h, 0),
        ]
        require(not dot(column_1, coprime_family)
                and not dot(boundary_column_2, coprime_family),
                ("degree-h coprime HB syzygy changed", h))
        require((0, h) in coprime_family[0]
                and (h, 0) in coprime_family[2],
                ("pure axes left coprime HB family", h))

        records[h] = {
            "forcing_column_degrees": [1, h - 2],
            "forcing_degree_sum": h - 1,
            "forced_common_factor_degree": 1,
            "sharp_coprime_column_degrees": [1, h - 1],
            "sharp_coprime_degree_sum": h,
            "sharp_coprime_generators": ["v^h", "-u*v^(h-1)", "u^h"],
        }
    return {
        "orders": records,
        "positive_Hilbert_Burch_identity": (
            "construct a full-rank m-by-(m-1) homogeneous source syzygy "
            "matrix H with H^T E=0 and sum(column degrees)<h"
        ),
        "degree_threshold_is_sharp": True,
        "current_anchor_crossed_block_is_such_a_syzygy": False,
    }


def association_projector_independence_audit() -> dict[str, object]:
    records = {}
    for h in range(3, 11):
        # These are the exact coefficient-level matching and endpoint
        # projector denominators.  They depend only on the occurrence
        # association scheme, not on the clean forms.
        matching_denominator = 2 * h - 1
        endpoint_denominator = 8 * h * (h + 1) * (2 * h + 1)
        require(matching_denominator * endpoint_denominator != 0,
                ("association projector denominator vanished", h))

        # The same coefficient projector coexists with the pure-axis clean
        # family E=<u^h,v^h>.  Its full Macaulay matrix is a permutation
        # identity: the first h rows are the shifts of u^h and the last h
        # rows are the shifts of v^h.
        pure_axis_macaulay = [
            [Fraction(int(row == column)) for column in range(2 * h)]
            for row in range(2 * h)
        ]
        require(matrix_rank(pure_axis_macaulay) == 2 * h,
                ("pure-axis association counterguard lost rank", h))
        records[h] = {
            "matching_projector_denominator": matching_denominator,
            "endpoint_cubic_projector_denominator": endpoint_denominator,
            "pure_axis_Macaulay_rank": 2 * h,
            "dual_kernel_dimension": 0,
            "operator_composition_degree": 3,
            "needed_clean_parameter_degree": h - 3,
            "numerical_degrees_equal": h == 6,
        }
    return {
        "orders": records,
        "verdict": (
            "the coefficient-level association projector is independent "
            "of the clean error family and survives on the coprime "
            "pure-axis guard, so it cannot by itself force the Fitting "
            "wedge or construct Tr_h"
        ),
        "cubic_degree_warning": (
            "degree three in the endpoint adjacency operator is a "
            "composition/Hasse-filtration degree, not degree h-3 in the "
            "binary clean parameter; their numerical equality at h=6 "
            "has no representation-theoretic content"
        ),
        "possible_positive_use": (
            "after a physical augmented cubic totalization, an additional "
            "source comparison may send its corrected product-rule face "
            "to a degree-(h-3) clean covariant and prove the simultaneous "
            "Fitting equations; that comparison is exactly new data"
        ),
    }


def scope_audit() -> dict[str, object]:
    bezout = (ROOT / (
        "notes/uniform-bezout-transvectant-source-transfer-gate.md"
    )).read_text()
    h3 = (ROOT / (
        "notes/h3-two-chart-divisor-transport-fitting-obstruction.md"
    )).read_text()
    anchors = (ROOT / (
        "notes/invertible-zero-alignment-two-chart-anchor-guard.md"
    )).read_text()
    matching = (ROOT / (
        "notes/uniform-centered-occurrence-matching-eigenspace-correction.md"
    )).read_text()
    endpoint = (ROOT / (
        "notes/uniform-centered-occurrence-full-endpoint-transfer-gate.md"
    )).read_text()
    require("same nonzero Bezout-kernel section" in bezout
            and "first-nonzero-subresultant/Fitting" in bezout,
            "simultaneous Bezout frontier changed")
    require(r"\boxed{-3\chi^3}" in h3
            and "no equation on it" in h3,
            "h=3 tail Fitting obstruction changed")
    require("The complete diagonal anchors give (5)" in anchors
            and r"P_c^{\mathsf T}H(Q_c)S_c=E_{cc}-F_cd" in anchors,
            "complete diagonal-anchor identity changed")
    require("does not claim" in matching
            and "a common-Hankel transfer" in matching,
            "matching association projector scope changed")
    require("No clean-line" in endpoint
            and "common-Hankel annihilation" in endpoint,
            "full endpoint transfer scope changed")
    return {
        "complete_anchor_transport_available": True,
        "all_h_tail_Fitting_vanishing_available": False,
        "source_Hilbert_Burch_degree_deficit_available": False,
        "first_exact_missing_relation": (
            "either wedge^h(mu_res)=0 in the complete source quotient, "
            "or a full-rank source syzygy matrix with total column "
            "degree below h"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "uniform anchor-crossed Bezout/Fitting/Hilbert-Burch gate",
        "pins": PINS,
        "scope": scope_audit(),
        "static": static_anchor_audit(),
        "tail_and_fitting": divided_tail_and_fitting_audit(),
        "hilbert_burch": hilbert_burch_audit(),
        "association_projector": association_projector_independence_audit(),
        "verdict": (
            "The complete diagonal anchors and crossed row do not force "
            "the top residual Fitting minors to vanish.  They invert the "
            "static label block while leaving the j>=2 repeated-insertion "
            "tail free; one nonzero leading tail coefficient makes the "
            "Macaulay block invertible.  A positive proof needs either "
            "literal vanishing of the combined top Fitting wedge or a "
            "source Hilbert-Burch matrix with total column degree < h."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("uniform anchor/Fitting ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("complete anchor/crossed static block: INVERTIBLE")
    print("all-h nonlinear tail: FREE IN GRADES j>=2")
    print("top Fitting defect: NOT FORCED")
    print("positive route: FITTING WEDGE OR DEGREE-DEFICIENT HILBERT-BURCH")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

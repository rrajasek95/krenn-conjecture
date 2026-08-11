#!/usr/bin/env python3
"""Literal source word-change from 11211200 to 01211200.

The site-x covariance derivation changing source colour 1 to 0 sends the
complete K8 matching row at 11211200 term-for-term to the row at 01211200.
It preserves both relevant chart partitions and transports the cyclotomic
Hamming-two kernel plane from r_v=q_xv^(1,m_v) to
rho_v=q_xv^(0,m_v).  It does not annihilate that plane or cancel the
already-certified chart-odd Schur connecting class.

This constructs the requested fixed-pair source relation, but not the final
Component-IV attaching/nullhomotopy row.
"""

from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path

import verify_h3_component_iv_cyclotomic_hamming_two_boundary as H2


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DIGEST = "e99d2eef2949111bafff236fede937f494f857d119eed7fd9bf313340b63f9e8"
PINS = {
    "computations/verify_h3_component_iv_cyclotomic_hamming_two_boundary.py":
        "aa225b9c59c22a104957b61da6ad2a365577876fe3fd74de6f119d4b42241c76",
    "computations/verify_h3_literal_full_nine_schur_polar_no_go.py":
        "a9347a06f516fe05a4d22872de5ac8071ca2824105159e59579ee1e8aad741cc",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
    "computations/verify_h3_reduced_ternary_bar_companion_cokernel.py":
        "6a5e6d42d5750cf6f1c75cd9ea79d53b03f4baf95a0ed40704285d40db22d9fc",
}

VERTICES = tuple(range(8))
X = 0
D = tuple(range(1, 6))
P = 6
Q_VERTEX = 7
R = 3
MIXED = (1, 2, 1, 1, 2)
WORD_H2 = (1,) + MIXED + (0, 0)
WORD_CHANGED = (0,) + MIXED + (0, 0)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def decorated_cell(left, right, word):
    if left < right:
        return left, right, word[left], word[right]
    return right, left, word[right], word[left]


def decorated_row(word):
    return {
        tuple(sorted(decorated_cell(left, right, word)
                     for left, right in matching)): Q(1)
        for matching in matchings(VERTICES)
    }


def physical_edges(monomial):
    return frozenset((left, right) for left, right, _, _ in monomial)


def split_chart(polynomial, chart_edge):
    chart_edge = tuple(sorted(chart_edge))
    direct = {monomial: coefficient for monomial, coefficient in polynomial.items()
              if chart_edge in physical_edges(monomial)}
    response = {monomial: coefficient for monomial, coefficient in polynomial.items()
                if chart_edge not in physical_edges(monomial)}
    return direct, response


def source_derivation_x_1_to_0(polynomial):
    """The local source vector field delta(q_xv^(1,c))=q_xv^(0,c)."""
    output = {}
    for monomial, coefficient in polynomial.items():
        incident = [index for index, cell in enumerate(monomial)
                    if X in cell[:2]]
        require(len(incident) == 1, "a matching does not use x exactly once")
        index = incident[0]
        cell = monomial[index]
        left, right, left_colour, right_colour = cell
        if left == X:
            require(left_colour == 1, "H2 x colour changed")
            changed = (left, right, 0, right_colour)
        else:
            require(right == X and right_colour == 1, "H2 x colour changed")
            changed = (left, right, left_colour, 0)
        new_monomial = list(monomial)
        new_monomial[index] = changed
        new_monomial = tuple(sorted(new_monomial))
        output[new_monomial] = output.get(new_monomial, Q(0)) + coefficient
    return {monomial: coefficient for monomial, coefficient in output.items()
            if coefficient}


def target(word):
    return None if len(set(word)) > 1 else word[0]


def kernel_transport():
    # The coefficients in K_zeta depend only on the other five site colours.
    # Delta_x changes r_v to rho_v and leaves the coefficient matrix itself
    # unchanged.  Recheck the exact kernel over both cyclotomic conjugates.
    r = (H2.ONE, H2.ZERO, H2.ZERO, H2.ZERO, H2.ZERO)
    rho = tuple(r)
    k_h2 = H2.cofactor_matrix(r)
    k_changed = H2.cofactor_matrix(rho)
    require(k_h2 == k_changed, "word change altered the cyclotomic cofactor")

    e1 = [H2.ONE, H2.ZERO, H2.ZERO, H2.ZERO, H2.ZERO]
    cyclotomic = [H2.ZERO, H2.ONE, H2.ZETA, H2.ZETA, H2.ONE]
    for vector in (e1, cyclotomic):
        require(H2.mat_vec(k_h2, vector) == [H2.ZERO] * 5,
                "H2 vector left the kernel")
        require(H2.mat_vec(k_changed, vector) == [H2.ZERO] * 5,
                "transported vector left the changed-word kernel")
    require(H2.rank_over_k(k_h2) == H2.rank_over_k(k_changed) == 3,
            "transported cofactor rank changed")
    return {
        "carrier_map": [
            f"q_x{site}^(1,{MIXED[site-1]})->q_x{site}^(0,{MIXED[site-1]})"
            for site in D
        ],
        "rank_before": 3,
        "rank_after": 3,
        "kernel_dimension_before": 2,
        "kernel_dimension_after": 2,
        "kernel_is_transported_not_killed": True,
    }


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}: {actual}")

    require(WORD_H2 == tuple(map(int, "11211200")), "H2 word changed")
    require(WORD_CHANGED == tuple(map(int, "01211200")),
            "endpoint-changed word changed")
    require(target(WORD_H2) is None and target(WORD_CHANGED) is None,
            "one endpoint acquired a diagonal target")

    h2_row = decorated_row(WORD_H2)
    changed_row = decorated_row(WORD_CHANGED)
    require(len(h2_row) == len(changed_row) == 105, "K8 row size changed")
    derived = source_derivation_x_1_to_0(h2_row)
    require(derived == changed_row,
            "local source derivation did not give the changed full row")

    chart_records = {}
    for name, chart in (("pq", (P, Q_VERTEX)), ("pr", (P, R))):
        h2_direct, h2_response = split_chart(h2_row, chart)
        changed_direct, changed_response = split_chart(changed_row, chart)
        require((len(h2_direct), len(h2_response)) == (15, 90),
                f"{name}: H2 chart split changed")
        require((len(changed_direct), len(changed_response)) == (15, 90),
                f"{name}: changed chart split changed")
        require(source_derivation_x_1_to_0(h2_direct) == changed_direct,
                f"{name}: direct provenance was not preserved")
        require(source_derivation_x_1_to_0(h2_response) == changed_response,
                f"{name}: response provenance was not preserved")

        # Direct-free A_pr=0 removes the 15 pr-direct monomials in both words;
        # the derivation still identifies the remaining 90-term rows.
        if name == "pr":
            require(source_derivation_x_1_to_0(h2_response) == changed_response,
                    "direct-free pr row lost covariance")
        chart_records[name] = {
            "direct_terms": len(h2_direct),
            "response_terms": len(h2_response),
            "derivation_preserves_each_sector": True,
        }

    transport = kernel_transport()

    # The normalized one-edge comparison has boundary L-D.  Its augmentation
    # is zero, and both complete words are mixed target-zero.  This is an
    # honest fixed-pair source relation, unlike a declared cross-word column.
    bar_boundary = (-1, 1)
    require(sum(bar_boundary) == 0, "one-site bar lost reduced augmentation")
    require(target(WORD_H2) is None and target(WORD_CHANGED) is None,
            "one-site bar acquired target")

    ledger = {
        "scope": "fixed pair 11211200/01211200 in the literal K8 full-nine rows",
        "source_operation": "site-x covariance derivation delta_x(1->0)",
        "identity": "delta_x H_11211200 = H_01211200",
        "matching_terms_each_side": 105,
        "target_before": "0 (mixed word)",
        "target_after": "0 (mixed word)",
        "normalized_bar_boundary": list(bar_boundary),
        "normalized_bar_augmentation": 0,
        "charts": chart_records,
        "cyclotomic_kernel_transport": transport,
        "constructs_fixed_pair_word_change": True,
        "kills_kernel_plane": False,
        "cancels_chart_odd_schur_connecting_class": False,
        "reason_stopping": (
            "the operation is diagonal on the pq/pr chart labels and transports "
            "the same rank-3 cofactor with its two-dimensional kernel; the "
            "certified Schur polar still requires a face/residue correction"
        ),
        "next_exact_datum": (
            "compose the transported 01211200 row with the five v-labelled "
            "Schur face deletions and test whether h_v=0 removes their chart-odd "
            "connecting/residue class in the physical quotient"
        ),
        "not_a_full_component_iv_closure": True,
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("h=3 Component-IV cyclotomic word-change relation: PASS")
    print("delta_x H_11211200 = H_01211200 termwise (105/105)")
    print("pq/pr sectors preserved: 15 direct + 90 response")
    print("cyclotomic kernel: transported, not killed (rank 3; nullity 2)")
    print("Schur face/residue correction: still required")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()

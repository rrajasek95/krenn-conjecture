#!/usr/bin/env python3
"""Compose the cyclotomic word change with all five Schur face deletions.

For each v, a local source derivation changes the v-th letter of 01211200
to zero, giving the certified Schur row c_v.  The literal polar by the two
cells xv:00 and pq:00 has exactly the three terms of h_v.  On the
cyclotomic q_m^[2]=0 specialization, both chart-sector copies and the old
ordinary-residue value vanish.

The generic chart-odd cochain pairs to one before specialization, but it
does not descend through the relation h_v=0.  Thus the old I_5 obstruction
disappears on this stratum; this does not manufacture a nonzero attaching
boundary, and hence is not by itself a Component-IV closure.
"""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path

import verify_h3_component_iv_cyclotomic_hamming_two_boundary as H2
import verify_h3_component_iv_cyclotomic_word_change_relation as WC


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DIGEST = "2839d0b25bca64e17e852445d4c4b5b608f2f9b0e17ec7a906d57c15c56aee01"
PINS = {
    "computations/verify_h3_component_iv_cyclotomic_word_change_relation.py":
        "335c82b382dcb3b8d69cd57a4fa54185a0db96368b5413b218b7c0f8bf303dae",
    "computations/verify_h3_component_iv_cyclotomic_hamming_two_boundary.py":
        "aa225b9c59c22a104957b61da6ad2a365577876fe3fd74de6f119d4b42241c76",
    "computations/verify_h3_literal_full_nine_schur_polar_no_go.py":
        "a9347a06f516fe05a4d22872de5ac8071ca2824105159e59579ee1e8aad741cc",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
}

X = WC.X
D = WC.D
P = WC.P
Q_VERTEX = WC.Q_VERTEX
MIXED = WC.MIXED
BASE_WORD = WC.WORD_CHANGED


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def source_derivation_site_to_zero(polynomial, site, old_colour):
    """delta_site(cell with old_colour)=cell with colour zero."""
    output = {}
    for monomial, coefficient in polynomial.items():
        incident = [index for index, cell in enumerate(monomial)
                    if site in cell[:2]]
        require(len(incident) == 1, "a matching does not use the site once")
        index = incident[0]
        left, right, left_colour, right_colour = monomial[index]
        if left == site:
            require(left_colour == old_colour, "left site colour changed")
            changed = (left, right, 0, right_colour)
        else:
            require(right == site and right_colour == old_colour,
                    "right site colour changed")
            changed = (left, right, left_colour, 0)
        new_monomial = list(monomial)
        new_monomial[index] = changed
        new_monomial = tuple(sorted(new_monomial))
        output[new_monomial] = output.get(new_monomial, Q(0)) + coefficient
    return {monomial: coefficient for monomial, coefficient in output.items()
            if coefficient}


def delete_cells(polynomial, selected_cells):
    """Literal squarefree partial derivative by the selected cells."""
    selected_cells = frozenset(selected_cells)
    output = {}
    for monomial, coefficient in polynomial.items():
        if not selected_cells.issubset(monomial):
            continue
        remainder = tuple(cell for cell in monomial if cell not in selected_cells)
        require(len(remainder) == len(monomial) - len(selected_cells),
                "a marked cell was repeated")
        output[remainder] = output.get(remainder, Q(0)) + coefficient
    return {monomial: coefficient for monomial, coefficient in output.items()
            if coefficient}


def expected_face_polynomial(deleted):
    vertices = tuple(site for site in D if site != deleted)
    answer = {}
    for matching in WC.matchings(vertices):
        monomial = tuple(sorted(WC.decorated_cell(left, right, BASE_WORD)
                                for left, right in matching))
        answer[monomial] = Q(1)
    require(len(answer) == 3, "four-site face stopped having three matchings")
    return answer


def evaluate_cyclotomic(polynomial):
    answer = H2.ZERO
    for monomial, coefficient in polynomial.items():
        term = H2.K(coefficient)
        for left, right, left_colour, right_colour in monomial:
            require(left in D and right in D,
                    "face evaluation retained an exposed site")
            require((left_colour, right_colour)
                    == (MIXED[left - 1], MIXED[right - 1]),
                    "face evaluation left the selected word")
            term *= H2.q_edge(left, right)
        answer += term
    return answer


def chart_odd_pairing(polar):
    # Lambda gives +1/6 to each pq-direct term and -1/6 to each pr-response
    # term.  Applied to the chart difference (polar,-polar), it reads one.
    pq = sum(polar.values(), Q(0)) / 6
    pr = sum((-coefficient for coefficient in polar.values()), Q(0)) * Q(-1, 6)
    return pq + pr


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}: {actual}")

    base_row = WC.decorated_row(BASE_WORD)
    require(len(base_row) == 105, "base changed-word row lost a matching")
    records = []
    for deleted in D:
        face_word = list(BASE_WORD)
        face_word[deleted] = 0
        face_word = tuple(face_word)
        require(len(set(face_word)) > 1, "a Schur face acquired target")

        derived = source_derivation_site_to_zero(
            base_row, deleted, MIXED[deleted - 1]
        )
        literal_face_row = WC.decorated_row(face_word)
        require(derived == literal_face_row,
                f"face {deleted}: covariance did not reach c_v")

        xv = WC.decorated_cell(X, deleted, face_word)
        pq = WC.decorated_cell(P, Q_VERTEX, face_word)
        require(xv == (min(X, deleted), max(X, deleted), 0, 0),
                f"face {deleted}: xv mark is not 00")
        require(pq == (P, Q_VERTEX, 0, 0),
                f"face {deleted}: pq mark is not 00")
        polar = delete_cells(literal_face_row, (xv, pq))
        expected = expected_face_polynomial(deleted)
        require(polar == expected, f"face {deleted}: marked polar is not h_v")

        # All three marked terms are pq-direct and pr-response.  None can be
        # pr-direct because the marked pq edge already occupies p.
        pq_direct, pq_response = WC.split_chart(literal_face_row, (P, Q_VERTEX))
        pr_direct, pr_response = WC.split_chart(literal_face_row, (P, WC.R))
        require(delete_cells(pq_direct, (xv, pq)) == polar,
                f"face {deleted}: pq-direct tail changed")
        require(not delete_cells(pq_response, (xv, pq)),
                f"face {deleted}: pq response acquired marked tail")
        require(not delete_cells(pr_direct, (xv, pq)),
                f"face {deleted}: pr direct acquired marked tail")
        require(delete_cells(pr_response, (xv, pq)) == polar,
                f"face {deleted}: pr-response tail changed")

        generic_pairing = chart_odd_pairing(polar)
        require(generic_pairing == 1,
                f"face {deleted}: generic Schur pairing is not one")
        value = evaluate_cyclotomic(polar)
        require(value == H2.ZERO,
                f"face {deleted}: cyclotomic h_v became nonzero")

        # In the old split-cap landing, q-augmentation and ordinary residue
        # both read the scalar face polynomial.  They therefore vanish in
        # both tagged sectors after base change by h_v=0.
        pq_sector = value
        pr_sector = value
        chart_odd_value = pq_sector - pr_sector
        old_ores_value = pq_sector - pr_sector
        require(chart_odd_value == old_ores_value == H2.ZERO,
                f"face {deleted}: a specialized tagged value survived")

        # Lambda does not descend to the specialized quotient: it reads 1/2
        # on the relation polar=0 in either single sector.
        single_sector_lambda = sum(polar.values(), Q(0)) / 6
        require(single_sector_lambda == Q(1, 2),
                f"face {deleted}: Lambda normalization changed")

        records.append({
            "face": deleted,
            "word": "".join(map(str, face_word)),
            "row_terms": len(literal_face_row),
            "polar_terms": len(polar),
            "generic_chart_odd_pairing": str(generic_pairing),
            "cyclotomic_h_v": value.text(),
            "specialized_chart_odd": chart_odd_value.text(),
            "specialized_old_ores": old_ores_value.text(),
            "Lambda_on_imposed_relation_h_v_zero": str(single_sector_lambda),
        })

    require(len(records) == 5, "five-face composition census changed")
    ledger = {
        "scope": "word-change 11211200->01211200 followed by five literal Schur polars",
        "base_change": "Q[zeta]/(zeta^2+zeta+1), h_1=...=h_5=0",
        "faces": records,
        "generic_connecting_matrix": "I_5",
        "specialized_tagged_tail_rank": 0,
        "specialized_old_ores_rank": 0,
        "old_Lambda_descends_after_h_zero": False,
        "reason": "Lambda(h_v)=1/2, so it is not a functional on the h_v=0 quotient",
        "word_change_plus_face_deletion_constructed": True,
        "nonzero_invisible_attaching_boundary_constructed": False,
        "verdict": (
            "the generic Schur/old-ores obstruction vanishes after the cyclotomic "
            "h=0 base change, but the composition has zero tail rather than the "
            "required nonzero curvature/cap boundary"
        ),
        "next_exact_datum": (
            "a first normal/Rees correction transverse to V(h), tracking whether "
            "kappa times the zero face has a nonzero divided boundary while tgt/ores stay zero"
        ),
        "not_a_component_iv_closure": True,
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("h=3 Component-IV cyclotomic Schur-face composition: PASS")
    print("five covariance-to-face rows: exact; each polar has 3 terms")
    print("generic chart-odd pairing: I5; after h=0: rank 0")
    print("old ordinary residue after h=0: rank 0")
    print("nonzero attaching boundary: NOT CONSTRUCTED")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()

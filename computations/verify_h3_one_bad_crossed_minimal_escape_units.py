#!/usr/bin/env python3
"""Exact closure of the two minimal escapes from the crossed affine unit.

Extend the complete 36-repair plus seven-gauge affine chart in exactly one of
two ways:

  A. add the previously absent physical cell x03_11; or
  B. add one transverse parameter to x06_11, splitting it from x06_22.

The checker reconstructs all literal full-output rows and all persistent
literal shared-arm reselections over Q[z_0,...,z_43].  Escape A retains a
two-row ordinary source unit.  Escape B has a four-row ordinary source unit.
Thus neither extension is a new coefficient packet, despite both carrying
many generic active curved four-good OO candidates.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_crossed_pair_reselection_census.py":
        "bec99e6dd24a459b661f54db71cc74a9b0b7e0c004161a944a40f8c5ed5dca99",
    "notes/h3-one-bad-crossed-pair-reselection-census.md":
        "155a5600604480597a2ab34ee3557b4b84428a5db27106111bcf3b29a32b163e",
}
EXPECTED_LEDGER_SHA256 = (
    "f61dafce5b28522103318ce307d7e4c2e1a4f4878471ca301db0ee7990e5a165"
)

ESCAPES = {
    "new_support_x03_11": (0, 3, 1, 1),
    "transverse_split_x06_11": (0, 6, 1, 1),
}
A_WORDS = ("12222212", "22222222")
B_WORDS = ("11111111", "21012122", "21111121", "22222222")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies(census, all_order, second, first):
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")
    census.pin_dependencies(all_order, second, first)


def add_parameter(census, forms, coordinate_id, cell, parameter=43):
    extended = [dict(form) for form in forms]
    index = coordinate_id[cell]
    extended[index] = census.add_polynomials(
        (extended[index], 1), ({(parameter,): Fraction(1)}, 1)
    )
    return extended


def full_generator_tensor(census, oo, forms, coordinate_id):
    """All nonzero polynomials among the literal 3^8 full-output rows."""

    tensor = {}
    matching_support = {}
    for matching in oo.perfect_matchings(tuple(range(8))):
        choices = []
        for u, v in matching:
            available = [
                (a, b, form)
                for a in range(3) for b in range(3)
                if (form := census.form_entry(
                    forms, coordinate_id, u, v, a, b
                ))
            ]
            if not available:
                choices = []
                break
            choices.append(available)
        if not choices:
            continue
        for selected in product(*choices):
            word = [None] * 8
            polynomial = {(): Fraction(1)}
            for (u, v), (a, b, form) in zip(
                    matching, selected, strict=True):
                word[u], word[v] = a, b
                polynomial = census.multiply(polynomial, form)
            word = tuple(word)
            tensor[word] = census.add_polynomials(
                (tensor.get(word, {}), 1), (polynomial, 1)
            )
            matching_support.setdefault(word, set()).add(matching)

    for colour in range(3):
        word = (colour,) * 8
        tensor[word] = census.add_polynomials(
            (tensor.get(word, {}), 1), ({(): Fraction(1)}, -1)
        )
    tensor = {word: polynomial for word, polynomial in tensor.items()
              if polynomial}
    return tensor, matching_support


def linear_form(census, constant=0, **coefficients):
    polynomial = {} if not constant else {(): Fraction(constant)}
    for name, value in coefficients.items():
        require(name.startswith("z"), f"bad parameter name: {name}")
        polynomial[(int(name[1:]),)] = Fraction(value)
    return polynomial


def audit_reselections(census, oo, forms, coordinate_id):
    blocks = census.literal_coordinate_blocks(forms, coordinate_id)
    candidates = census.candidate_pairs(blocks)
    activity_cache = {}
    records = tuple(
        census.candidate_record(
            oo, forms, coordinate_id, candidate, activity_cache
        )
        for candidate in candidates
    )
    require(all(record["star_ranks"] == [3, 3, 3, 3]
                for record in records),
            "an escape acquired a rank-deficient persistent candidate")
    return blocks, candidates, records


def source_row(all_order, oo, census, forms, coordinate_id, word_text):
    word = tuple(map(int, word_text))
    polynomial, matchings = all_order.hafnian_coefficient(
        oo, forms, coordinate_id, word
    )
    if len(set(word)) == 1:
        polynomial = census.add_polynomials(
            (polynomial, 1), ({(): Fraction(1)}, -1)
        )
    return polynomial, matchings


def main():
    census = importlib.import_module(
        "verify_h3_one_bad_crossed_pair_reselection_census")
    all_order = importlib.import_module(
        "verify_h3_one_bad_crossed_all_order_affine_unit")
    first = importlib.import_module(
        "verify_h3_one_bad_crossed_first_rank_repair_obstruction")
    second = importlib.import_module(
        "verify_h3_one_bad_crossed_second_hasse_obstruction")
    pin_dependencies(census, all_order, second, first)
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    closure = importlib.import_module(
        "verify_h3_one_bad_second_principal_parts_companion_closure")
    oo = importlib.import_module(
        "verify_oo_doubly_good_two_anchor_counterguard")

    source = first.build_crossed_source(base, closure)
    cells, coordinate_id, directions, forms = census.build_affine_chart(
        first, second, all_order, oo, source
    )
    require(len(directions) == 43, "the underlying affine chart changed")

    extended = {
        name: add_parameter(census, forms, coordinate_id, cell)
        for name, cell in ESCAPES.items()
    }
    full_rows = {}
    matching_support = {}
    row_ledgers = {}
    for name, escaped_forms in extended.items():
        rows, support = full_generator_tensor(
            census, oo, escaped_forms, coordinate_id
        )
        full_rows[name], matching_support[name] = rows, support
        row_ledgers[name] = {
            "full_output_rows_checked": 3 ** 8,
            "nonzero_source_rows": len(rows),
            "collected_terms": sum(map(len, rows.values())),
            "monomial_degree_histogram": dict(sorted(Counter(
                len(monomial)
                for polynomial in rows.values()
                for monomial in polynomial
            ).items())),
        }
    require(
        (row_ledgers["new_support_x03_11"]["nonzero_source_rows"],
         row_ledgers["new_support_x03_11"]["collected_terms"])
        == (292, 8313),
        "escape A's full-row ledger changed",
    )
    require(
        (row_ledgers["transverse_split_x06_11"]["nonzero_source_rows"],
         row_ledgers["transverse_split_x06_11"]["collected_terms"])
        == (256, 7910),
        "escape B's full-row ledger changed",
    )

    # Escape A: a different pure/mixed pair, unaffected by x03_11, has the
    # same sole physical matching and hence an ordinary two-row unit.
    a_rows = full_rows["new_support_x03_11"]
    a_mixed, a_pure = (tuple(map(int, word)) for word in A_WORDS)
    a_unit = census.add_polynomials(
        (a_rows[a_mixed], 1), (a_rows[a_pure], -1)
    )
    require(a_unit == {(): Fraction(1)},
            f"escape A's two-row unit changed: {a_unit}")
    a_matching = ((0, 6), (1, 5), (2, 3), (4, 7))
    require(
        matching_support["new_support_x03_11"][a_mixed] == {a_matching}
        and matching_support["new_support_x03_11"][a_pure] == {a_matching},
        "escape A's two unique matchings changed",
    )

    # Escape B: exact four-row certificate.  Write
    #
    #   M=(z36-z37)(1+z39)(z38-z39-z40+z42),
    #   L=z36+z37+z38+z40-z42-1.
    #
    # Then (ML)G_11111111 + G_21012122
    #      - M(L-z43)G_21111121 - G_22222222 = 1.
    b_forms = extended["transverse_split_x06_11"]
    b_rows = {}
    b_matchings = {}
    for word in B_WORDS:
        b_rows[word], b_matchings[word] = source_row(
            all_order, oo, census, b_forms, coordinate_id, word
        )
        require(b_rows[word] == full_rows["transverse_split_x06_11"][
            tuple(map(int, word))
        ], f"escape B row reconstruction changed at {word}")

    factor_one = linear_form(census, z36=1, z37=-1)
    factor_two = linear_form(census, 1, z39=1)
    factor_three = linear_form(
        census, z38=1, z39=-1, z40=-1, z42=1
    )
    m_polynomial = census.multiply(
        census.multiply(factor_one, factor_two), factor_three
    )
    l_polynomial = linear_form(
        census, -1, z36=1, z37=1, z38=1, z40=1, z42=-1
    )
    l_minus_t = census.add_polynomials(
        (l_polynomial, 1), ({(43,): Fraction(1)}, -1)
    )
    multiplier_111 = census.multiply(m_polynomial, l_polynomial)
    multiplier_211 = census.multiply(m_polynomial, l_minus_t)
    b_unit = census.add_polynomials(
        (census.multiply(multiplier_111, b_rows["11111111"]), 1),
        (b_rows["21012122"], 1),
        (census.multiply(multiplier_211, b_rows["21111121"]), -1),
        (b_rows["22222222"], -1),
    )
    require(b_unit == {(): Fraction(1)},
            f"escape B's four-row unit changed: {b_unit}")
    require((len(m_polynomial), len(multiplier_111), len(multiplier_211))
            == (16, 50, 66),
            "escape B's factored multiplier ledger changed")

    # Both extensions also retain the structural OO landing data.  This is
    # recorded but not used: the ordinary source units close the charts first.
    reselection_ledgers = {}
    for name, escaped_forms in extended.items():
        blocks, candidates, records = audit_reselections(
            census, oo, escaped_forms, coordinate_id
        )
        reselection_ledgers[name] = {
            "literal_coordinate_blocks": [list(block) for block in blocks],
            "shared_distinct_outer_line_candidates": len(candidates),
            "four_good_active_curved_candidates": len(records),
            "candidate_vertices": [list(candidate[:3]) for candidate in candidates],
        }
    require(
        (len(reselection_ledgers["new_support_x03_11"]
             ["literal_coordinate_blocks"]),
         reselection_ledgers["new_support_x03_11"]
             ["shared_distinct_outer_line_candidates"])
        == (12, 24),
        "escape A's reselection census changed",
    )
    require(
        (len(reselection_ledgers["transverse_split_x06_11"]
             ["literal_coordinate_blocks"]),
         reselection_ledgers["transverse_split_x06_11"]
             ["shared_distinct_outer_line_candidates"])
        == (11, 20),
        "escape B's reselection census changed",
    )

    ledger = {
        "dependencies": PINS,
        "affine_parameters_before_escape": len(directions),
        "affine_parameters_after_escape": 44,
        "full_rows": row_ledgers,
        "escape_A": {
            "cell": list(ESCAPES["new_support_x03_11"]),
            "unit_rows": list(A_WORDS),
            "common_unique_matching": [list(edge) for edge in a_matching],
            "identity": "G_12222212-G_22222222=1",
            "category": "ordinary_two_row_source_unit",
        },
        "escape_B": {
            "cell": list(ESCAPES["transverse_split_x06_11"]),
            "unit_rows": list(B_WORDS),
            "M": "(z36-z37)(1+z39)(z38-z39-z40+z42)",
            "L": "z36+z37+z38+z40-z42-1",
            "identity": (
                "(M*L)G_11111111+G_21012122"
                "-M(L-z43)G_21111121-G_22222222=1"
            ),
            "multiplier_term_counts": [
                len(multiplier_111), 1, len(multiplier_211), 1
            ],
            "category": "ordinary_four_row_source_unit",
        },
        "reselections": reselection_ledgers,
        "verdict": (
            "both minimal departures from the crossed affine unit are "
            "coefficient-empty by ordinary source-row identities; neither "
            "defines a new finite packet, and clean-cap/OO transport is not "
            "needed despite the surviving generic OO candidates"
        ),
        "scope": (
            "exactly one added parameter, either on the absent cell x03_11 "
            "or as the transverse x06_11-x06_22 split; no other support cell "
            "and no higher-order deformation is admitted"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the crossed minimal-escape ledger changed: {digest}")

    print("h=3 crossed minimal escape units: PASS")
    print("A x03_11: 292 rows; two-row ordinary unit")
    print("B x06_11-x06_22: 256 rows; four-row ordinary unit")
    print("A reselections: 24/24 four-good, active, curved")
    print("B reselections: 20/20 four-good, active, curved")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

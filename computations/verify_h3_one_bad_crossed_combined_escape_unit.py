#!/usr/bin/env python3
"""Exact unit test for the combined two-escape crossed critical face.

Starting from the complete 43-parameter crossed affine chart, add exactly

  z43 at x03_11, and
  z44 at x06_11 (splitting x06_11 from x06_22).

No third departure is admitted.  Reconstruct all 3^8 literal source rows,
verify the persistent shared-pair census, and compute the exact Q standard
basis in two monomial orders.  Both bases are [1].
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_crossed_minimal_escape_units.py":
        "517a1d71b3ba393847eab433c93c067f13ba38d53aa315f573a798f79ab5a3a9",
    "notes/h3-one-bad-crossed-minimal-escape-units.md":
        "26dfc8b9569391ce2868beb2aba7ff3af0eae1973fe0755c9e3a2b91697b1037",
}
EXPECTED_SOURCE_SHA256 = (
    "43d847a2e4c1d13a24dcc0ff61c94b8075e775c80cfbc06fd2d9a40b9ff3618f"
)
EXPECTED_LEDGER_SHA256 = (
    "3f6cf147ae02c3f8b36f6bb62fc3cab15990a8d7d003453e0c431d49efaabdc9"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies(escape, census, all_order, second, first):
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")
    escape.pin_dependencies(census, all_order, second, first)


def singular_polynomial(polynomial):
    terms = []
    for monomial, coefficient in sorted(
            polynomial.items(), key=lambda item: (len(item[0]), item[0])):
        variable = "*".join(f"z{index}" for index in monomial) or "1"
        if coefficient.denominator == 1:
            scalar = str(coefficient.numerator)
        else:
            scalar = f"({coefficient.numerator}/{coefficient.denominator})"
        terms.append(f"{scalar}*{variable}")
    return "+".join(terms).replace("+-", "-")


def singular_unit_program(generators, order):
    variables = ",".join(f"z{index}" for index in range(45))
    code = f"ring r=0,({variables}),{order}; option(redSB);\n"
    code += "ideal I=" + ",".join(generators) + ";\n"
    code += "ideal G=slimgb(I);\n"
    code += (
        "if(size(G)!=1 || G[1]!=1)"
        f"{{ print(\"UNIT_{order}_FAILED\"); exit(1); }}\n"
    )
    code += f"print(\"UNIT_{order}_PASS\");\n"
    return code


def run_unit_basis(generators, order):
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"),
        input=singular_unit_program(generators, order),
        text=True,
        capture_output=True,
        check=False,
        timeout=15,
    )
    require(result.returncode == 0,
            f"Singular failed in order {order}: {result.stderr or result.stdout}")
    require(f"UNIT_{order}_PASS" in result.stdout,
            f"the exact Q unit verdict failed in order {order}: {result.stdout}")
    return result.stdout.strip()


def main():
    escape = importlib.import_module(
        "verify_h3_one_bad_crossed_minimal_escape_units")
    census = importlib.import_module(
        "verify_h3_one_bad_crossed_pair_reselection_census")
    all_order = importlib.import_module(
        "verify_h3_one_bad_crossed_all_order_affine_unit")
    first = importlib.import_module(
        "verify_h3_one_bad_crossed_first_rank_repair_obstruction")
    second = importlib.import_module(
        "verify_h3_one_bad_crossed_second_hasse_obstruction")
    pin_dependencies(escape, census, all_order, second, first)
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
    require(len(directions) == 43, "the crossed affine chart changed")
    forms = escape.add_parameter(
        census, forms, coordinate_id, (0, 3, 1, 1), 43
    )
    forms = escape.add_parameter(
        census, forms, coordinate_id, (0, 6, 1, 1), 44
    )

    rows, matching_support = escape.full_generator_tensor(
        census, oo, forms, coordinate_id
    )
    require(len(rows) == 292,
            f"the combined critical face row count changed: {len(rows)}")
    require(sum(map(len, rows.values())) == 8713,
            "the combined critical face term count changed")
    require(len(matching_support) == 292,
            "the literal matching-support row count changed")
    degree_histogram = Counter(
        len(monomial)
        for polynomial in rows.values()
        for monomial in polynomial
    )
    require(degree_histogram == Counter({
        0: 10, 1: 114, 2: 980, 3: 3410, 4: 4199,
    }), f"the combined monomial-degree histogram changed: {degree_histogram}")

    items = tuple(sorted(rows.items()))
    labels = tuple("".join(map(str, word)) for word, _polynomial in items)
    generators = tuple(
        singular_polynomial(polynomial) for _word, polynomial in items
    )
    source_payload = json.dumps(
        list(zip(labels, generators, strict=True)),
        separators=(",", ":"),
    )
    source_digest = sha256(source_payload.encode()).hexdigest()
    if EXPECTED_SOURCE_SHA256 != "TO_BE_FILLED":
        require(source_digest == EXPECTED_SOURCE_SHA256,
                f"the combined source input changed: {source_digest}")

    # Neither old short identity remains a unit once the other escape is
    # present.  This is why the two-parameter face is a genuine critical-pair
    # check rather than a restatement of e97a968.
    a_mixed, a_pure = (tuple(map(int, word))
                       for word in escape.A_WORDS)
    old_a_difference = census.add_polynomials(
        (rows[a_mixed], 1), (rows[a_pure], -1)
    )
    require(old_a_difference != {(): Fraction(1)}
            and any(44 in monomial for monomial in old_a_difference),
            "the old A unit unexpectedly survived the transverse split")

    b_rows = {}
    for word in escape.B_WORDS:
        b_rows[word], _matchings = escape.source_row(
            all_order, oo, census, forms, coordinate_id, word
        )
    factor_one = escape.linear_form(census, z36=1, z37=-1)
    factor_two = escape.linear_form(census, 1, z39=1)
    factor_three = escape.linear_form(
        census, z38=1, z39=-1, z40=-1, z42=1
    )
    m_polynomial = census.multiply(
        census.multiply(factor_one, factor_two), factor_three
    )
    l_polynomial = escape.linear_form(
        census, -1, z36=1, z37=1, z38=1, z40=1, z42=-1
    )
    l_minus_t = census.add_polynomials(
        (l_polynomial, 1), ({(44,): Fraction(1)}, -1)
    )
    old_b_combination = census.add_polynomials(
        (census.multiply(
            census.multiply(m_polynomial, l_polynomial),
            b_rows["11111111"],
        ), 1),
        (b_rows["21012122"], 1),
        (census.multiply(
            census.multiply(m_polynomial, l_minus_t),
            b_rows["21111121"],
        ), -1),
        (b_rows["22222222"], -1),
    )
    require(old_b_combination != {(): Fraction(1)}
            and any(43 in monomial for monomial in old_b_combination),
            "the old B unit unexpectedly survived x03_11")

    # Independent exact-Q standard-basis computations.  Dp reverses the
    # variable comparison relative to dp, so the identical [1] verdict is not
    # tied to one critical-pair schedule.
    basis_verdicts = {
        order: run_unit_basis(generators, order) for order in ("dp", "Dp")
    }

    blocks, candidates, records = escape.audit_reselections(
        census, oo, forms, coordinate_id
    )
    require((len(blocks), len(candidates), len(records)) == (12, 24, 24),
            "the combined reselection census changed")
    require(all(record["star_ranks"] == [3, 3, 3, 3]
                for record in records),
            "a combined-face persistent reselection is rank deficient")

    ledger = {
        "dependencies": PINS,
        "parameters": {
            "base_affine": 43,
            "x03_11": 43,
            "x06_11_minus_x06_22": 44,
            "total": 45,
        },
        "full_source": {
            "rows_checked": 3 ** 8,
            "nonzero_rows": len(rows),
            "collected_terms": sum(map(len, rows.values())),
            "degree_histogram": dict(sorted(degree_histogram.items())),
            "source_sha256": source_digest,
        },
        "critical_pair": {
            "old_A_two_row_unit_survives": False,
            "old_A_residual_terms": len(old_a_difference),
            "old_B_four_row_unit_survives": False,
            "old_B_residual_terms": len(old_b_combination),
            "exact_Q_standard_bases": basis_verdicts,
            "ideal": "unit",
        },
        "reselections": {
            "literal_coordinate_blocks": len(blocks),
            "shared_distinct_outer_line_candidates": len(candidates),
            "four_good_active_curved_candidates": len(records),
            "candidate_vertices": [list(candidate[:3]) for candidate in candidates],
        },
        "verdict": (
            "the simultaneous x03_11 and transverse x06 split critical face "
            "is empty over Q; it is not a coefficient-feasible packet"
        ),
        "certificate_boundary": (
            "two exact standard-basis computations return [1]; the full "
            "ordinary source multiplier lift was capped after 120 seconds, "
            "so no compact row-level Nullstellensatz identity is claimed"
        ),
        "scope": (
            "exactly the two simultaneous departures named by e97a968, with "
            "no third support cell, coefficient split, or higher-order jet"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the combined escape ledger changed: {digest}")

    print("h=3 crossed combined two-escape critical pair: PASS")
    print("45 variables; 292 nonzero rows; 8713 collected terms")
    print("exact Q standard bases: dp=[1], Dp=[1]")
    print("persistent reselections: 24/24 four-good, active, curved")
    print(f"source sha256: {source_digest}")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()

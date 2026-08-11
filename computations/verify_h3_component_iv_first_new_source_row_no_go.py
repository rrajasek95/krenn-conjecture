#!/usr/bin/env python3
"""Exact no-go for constructing Component-IV n_c from existing source rows.

The audit combines the complete first compatible fine-degree block with the
all-word polynomial reset lock.  It then reconstructs the five independent
denominator initials which specify the first genuinely new relative row.
No rational calibration or Jacobian is used.
"""

from collections import defaultdict
from contextlib import redirect_stdout
from hashlib import sha256
from itertools import product
import io
import json

import verify_h3_component_iv_physical_definability_gate as GATE
import verify_h3_direct_free_complete_first_fine_degree_membership as FIRST
import verify_h3_reset_lane_ores_descent_lock as RESET
import verify_h3_universal_denominator_reset_polynomial_no_go as DENOM


EXPECTED_DIGEST = "e788138f3e8f1752546e97cb48ac66955bc61864877dd1df38f9cdafaddb4528"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def first_fine_degree():
    records = [FIRST.face_audit(site) for site in FIRST.ODD_SITES]
    for record in records:
        denominator = record["denominator"]
        eqsystem = record["eqsystem"]
        require(denominator["terms_inspected"] == 3645,
                "denominator term census moved")
        require(denominator["terms_dividing_lambda"] == 0,
                "raw denominator acquired a first-degree column")
        require(eqsystem["one_chart_columns"] == 48
                and eqsystem["two_chart_columns"] == 96,
                "first full-word column count moved")
        require(eqsystem["one_chart_boundary_rank"] == 48
                and eqsystem["two_chart_boundary_rank"] == 48,
                "first full-word boundary rank moved")
        require(eqsystem["kernel_dimension"] == 48
                and eqsystem["kernel_common_coefficient_rank"] == 0
                and eqsystem["kernel_physical_target_rank"] == 0,
                "first full-word kernel acquired the missing signature")
    return [{
        "deleted_site": record["deleted_site"],
        "face": record["face"],
        "denominator_terms": record["denominator"]["terms_inspected"],
        "raw_denominator_columns":
            record["denominator"]["homogeneous_columns_admitted"],
        "chart_columns": [
            record["eqsystem"]["one_chart_columns"],
            record["eqsystem"]["two_chart_columns"],
        ],
        "boundary_ranks": [
            record["eqsystem"]["one_chart_boundary_rank"],
            record["eqsystem"]["two_chart_boundary_rank"],
        ],
        "kernel_dimension": record["eqsystem"]["kernel_dimension"],
        "kernel_common_coefficient_rank":
            record["eqsystem"]["kernel_common_coefficient_rank"],
        "kernel_target_rank": record["eqsystem"]["kernel_physical_target_rank"],
    } for record in records]


def denominator_initials():
    words = tuple(product(DENOM.COLORS, repeat=len(DENOM.SITES)))
    columns = tuple((site, colour)
                    for site in DENOM.SITES for colour in DENOM.COLORS)

    owners = defaultdict(set)
    for word in words:
        for site, colour in columns:
            for term in DENOM.denominator_entry(word, site, colour):
                owners[((site, colour), term)].add(word)
    require(len(owners) == 3645 and all(len(value) == 1 for value in owners.values()),
            "universal denominator initial map lost unique ownership")

    mixed = [DENOM.denominator_entry(DENOM.MIXED, site,
                                     DENOM.MIXED[DENOM.SITES.index(site)])
             for site in DENOM.SITES]
    pure = [DENOM.denominator_entry(DENOM.PURE, site, 0)
            for site in DENOM.SITES]
    require(all(len(vector) == 3 for vector in mixed + pure),
            "four-face hafnian term count moved")

    monomials = sorted({term for vector in pure + mixed for term in vector})
    index = {term: position for position, term in enumerate(monomials)}
    rows = []
    for vector in pure + mixed:
        row = [0] * len(monomials)
        for term in vector:
            row[index[term]] += 1
        rows.append(row)
    pure_rank = DENOM.matrix_rank(rows[:5])
    combined_rank = DENOM.matrix_rank(rows)
    require((pure_rank, combined_rank) == (5, 10),
            "five denominator defect classes lost independence")

    face_words = []
    for deleted in DENOM.SITES:
        face_words.append("".join(
            str(DENOM.MIXED[DENOM.SITES.index(site)])
            for site in DENOM.SITES if site != deleted
        ))
    return {
        "word_coordinates": len(words),
        "denominator_columns": len(columns),
        "degree_two_features": len(owners),
        "constant_initial_rank": len(words),
        "old_pure_face_rank": pure_rank,
        "pure_plus_mixed_rank": combined_rank,
        "new_face_rank": combined_rank - pure_rank,
        "required_rows": [
            {"deleted_site": site,
             "face_word": word,
             "name": f"tau_{site}^{{{word}->0000}}"}
            for site, word in zip(DENOM.SITES, face_words, strict=True)
        ],
    }


def all_word_polynomial_lock():
    captured = io.StringIO()
    with redirect_stdout(captured):
        RESET.main()
    output = captured.getvalue()
    require(RESET.EXPECTED_LEDGER_DIGEST in output,
            "reset-lock dependency lost its exact ledger")
    lock = RESET.LEDGER["lock"]
    require(lock["rows_checked"] == 3**8
            and lock["edge_degree"] == 4
            and lock["u_coefficient_in_F0"] == "-1",
            "all-word u-extraction lock moved")
    require(RESET.LEDGER["leak_rank"] == 12
            and RESET.LEDGER["leak_monomial_count"] == 22,
            "proper-face leak module moved")
    return {
        "EqSystem_rows": lock["rows_checked"],
        "hafnian_edge_degree": lock["edge_degree"],
        "unique_edge_zero_u_coefficient": lock["u_coefficient_in_F0"],
        "proper_face_leak_rank": RESET.LEDGER["leak_rank"],
        "proper_face_leak_monomials": RESET.LEDGER["leak_monomial_count"],
        "scope": (
            "all polynomial combinations of ordinary EqSystem rows plus T,rho; "
            "no source-equation localization"
        ),
        "verdict": "no chain has (boundary,target,ores)=(kappa*Y*w,0,0)",
    }


def physical_signature():
    gate = GATE.source_relative_gate()["downstairs"]
    require(gate["separator"] == [1, 1, 1, -1]
            and gate["desired_chain"] == [0, 1, 0, 0]
            and gate["separator_value"] == "1",
            "Component-IV primitive signature moved")
    return gate


def main():
    ledger = {
        "scope": "first new source row for the h=3 Component-IV relative chain",
        "first_complete_fine_degree": first_fine_degree(),
        "all_word_polynomial_lock": all_word_polynomial_lock(),
        "physical_signature": physical_signature(),
        "denominator_initials": denominator_initials(),
        "conclusion": {
            "existing_rows": (
                "no EqSystem/Koszul/Bianchi/reset/principal-parts combination "
                "landing in the committed physical module constructs n_c"
            ),
            "first_new_source_type": (
                "five face-labelled relative rows tau_v (one equivariant family), "
                "with initial boundary h_v*Y_0 and zero target/ores"
            ),
            "full_required_boundary": (
                "d tau_v=h_v*Y_0+delta(eta_v)+higher full-nine rows"
            ),
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, ("ledger changed", digest))

    print("h=3 Component-IV first-new-source-row no-go: PASS")
    print("complete first fine degree: five faces, only 48 chart-difference kernels")
    print("all 6561 EqSystem rows + arbitrary polynomial multipliers: locked")
    print("first new source type: five independent tau_v denominator commutators")
    print("literal n_c from committed source rows: DOES NOT EXIST")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()

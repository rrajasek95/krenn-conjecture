#!/usr/bin/env python3
"""Adversarially audit the reproducible claims in external spine audit 2.

The external package contains only REPORT.md, not the transcripts and
mutation scripts named by that report.  This checker therefore distinguishes
claims reproducible from committed artifacts from claims for which the
external evidence is absent.

It also supplies two independent exact tests which were missing from the
committed layer:

* untying one of the four asserted B=Eq response rows preserves the rank-7
  projection but destroys the displayed delta.(B-Eq) annihilator; and
* the literal matching/endpoint projector composite, previously asserted but
  not evaluated in its checker, sends the actual Gram row to a nonzero
  constant at h=3 and h=4.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = ROOT / "computations/unaudited-external-spine-audit-2-2026-08-13"
PINS = {
    "computations/unaudited-external-spine-audit-2-2026-08-13/REPORT.md":
        "058d6f4f469f9ed3526e699d42ced6eb4c2e32c8604bd14c5017201556d6387d",
    "computations/verify_h3_db01_dl01_literal_private_eq_conservation_gate.py":
        "1a27b00d28be6334a27e0603a0ef776367d3c71b6f8fa45d3005963f8dff4c6c",
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "computations/verify_uniform_centered_occurrence_full_endpoint_transfer_gate.py":
        "6f5686298143b584a4edcb350145bf9d648277972aa96b90443c4ce254cb1d30",
    "computations/verify_uniform_centered_occurrence_matching_eigenspace_correction.py":
        "6e9c665e2c42b23e1910963b030de2f6c4b16dfe4951eae6e0e79b7fcf1e6921",
    "computations/verify_uniform_centered_occurrence_endpoint_association_projector.py":
        "0ef88312cead100120e4600ea3a2d0616262a96bf27726d07817610d11b43f59",
    "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py":
        "e5f2664b99c5ba58e0be385ca52dc52c6d2f6d6d0b793e655ebe297542dce291",
    "PROOF-SKETCH.md":
        "bf23880743cfbde7f3bd21cd197aeda1f5b4b50bd3f2d26e67eace0e0be52d74",
    "notes/2026-08-13-three-interface-proof-frontier.md":
        "45c3434a764295d97b63518348373607e4115e4b3ae4ac76e4c5cf312c81837b",
}
EXPECTED_LEDGER_SHA256 = "ae9bbadee72382167942a17db44741d7f558eb89c3e4f545eee24dee6014e352"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(columns)
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(len(columns[0]))]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[answer], matrix[pivot] = matrix[pivot], matrix[answer]
        value = matrix[answer][column]
        matrix[answer] = [entry / value for entry in matrix[answer]]
        for row in range(len(matrix)):
            if row == answer or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def evidence_inventory_audit() -> dict[str, object]:
    files = tuple(sorted(str(path.relative_to(EXTERNAL))
                         for path in EXTERNAL.rglob("*") if path.is_file()))
    require(files == ("REPORT.md",), files)
    report = (EXTERNAL / "REPORT.md").read_text()
    require("~40 mutation scripts + independent re-derivations" in report
            and "Full agent transcripts in the session" in report,
            "the external evidence claim changed")
    return {
        "files_present": list(files),
        "promised_transcripts_present": False,
        "promised_mutation_scripts_present": False,
        "consequence": (
            "the report is a lead list, not an independently replayable audit package"
        ),
    }


def beq_tie_sensitivity_audit() -> dict[str, object]:
    # Coordinates are B0..B3, Eq0..Eq3.  The four diagonal response rows and
    # four signless K2,2 companions are the exact top projection used by the
    # local terminal checker after matching-occurrence aggregation.
    delta = tuple(map(Q, (1, 1, -1, -1)))
    chi = delta + tuple(-value for value in delta)
    diagonals = []
    for corner in range(4):
        unit = tuple(Q(index == corner) for index in range(4))
        diagonals.append(unit + unit)
    companions = []
    for direct in (0, 1):
        for endpoint in (2, 3):
            edge = tuple(Q(index in (direct, endpoint)) for index in range(4))
            companions.append(edge + (Q(0),) * 4)
    tied = tuple(diagonals + companions)
    require(rank(tied) == 7 and all(dot(chi, row) == 0 for row in tied),
            "the tied rank-seven packet changed")

    mutations = []
    for corner in range(4):
        unit = tuple(Q(index == corner) for index in range(4))
        rows = list(tied)
        rows[corner] = unit + (Q(0),) * 4
        mutations.append({
            "corner": corner,
            "rank": rank(rows),
            "old_chi_on_mutated_row": str(dot(chi, rows[corner])),
        })
    require({entry["rank"] for entry in mutations} == {7}
            and {entry["old_chi_on_mutated_row"] for entry in mutations}
                == {"-1", "1"},
            mutations)
    return {
        "tied_rank": rank(tied),
        "tied_chi_annihilates": True,
        "single_corner_untie_mutations": mutations,
        "verdict": (
            "B=Eq is load-bearing: rank 7 alone does not determine the claimed dual"
        ),
    }


def projector_scope_and_composite_audit() -> dict[str, object]:
    matching = load(
        "computations/verify_uniform_centered_occurrence_matching_eigenspace_correction.py",
        "external_spine2_matching",
    )
    endpoint = load(
        "computations/verify_uniform_centered_occurrence_endpoint_association_projector.py",
        "external_spine2_endpoint",
    )

    # Pi_match is only a projector on 1+E1, as its own docstring says.  A
    # matching-basis vector at h=3 has components in other eigenspaces.
    h = 3
    matchings = tuple(matching.BASE.perfect_matchings(tuple(range(2 * h))))
    lookup_matching = {value: index for index, value in enumerate(matchings)}
    adjacency = tuple(tuple(lookup_matching[value]
                            for value in matching.switch_neighbors(item))
                      for item in matchings)
    lam = Q(h * h - 3 * h + 1)
    denominator = Q(2 * h - 1)

    def pi_match(vector):
        return tuple((sum(vector[index] for index in neighbors)
                      - lam * vector[row]) / denominator
                     for row, neighbors in enumerate(adjacency))

    basis = tuple(Q(index == 0) for index in range(len(matchings)))
    once = pi_match(basis)
    twice = pi_match(once)
    require(once != twice, "Pi_match accidentally became a global projector")

    records = []
    for h in (3, 4):
        occurrences, marked, gram = matching.full_gram_row(h)
        lookup = {value: index for index, value in enumerate(occurrences)}
        vector = tuple(Q(gram[value]) for value in occurrences)
        lam = Q(h * h - 3 * h + 1)
        matching_numerator = []
        for occurrence in occurrences:
            switched_sum = sum((
                vector[lookup[(occurrence[0], occurrence[1], switched)]]
                for switched in matching.switch_neighbors(occurrence[2])
            ), Q(0))
            matching_numerator.append(switched_sum - lam * vector[
                lookup[occurrence]])
        matching_numerator = tuple(matching_numerator)
        closed_form = endpoint.matching_flat_row(h, occurrences, marked)
        require(matching_numerator == closed_form,
                ("matching numerator did not equal the endpoint input", h))

        sites = tuple(range(2 * h + 2))
        operator = lambda values: endpoint.apply_endpoint(
            values, occurrences, lookup, sites)
        projected = endpoint.polynomial_apply(
            matching_numerator, (-2, 2 * h - 2, 2 * h), operator)
        require(len(set(projected)) == 1 and projected[0],
                ("full projector composite was not nonzero constant", h))
        records.append({
            "h": h,
            "occurrences": len(occurrences),
            "integral_composite_constant": str(projected[0]),
            "marked_matching_numerator": str(
                matching_numerator[lookup[marked]]),
        })
    return {
        "Pi_match_global_idempotent": False,
        "correct_scope": "projector on the constant plus E1 subspace",
        "actual_Gram_row_composite_checks": records,
        "new_positive_finding": (
            "Pi_end Pi_match is directly verified on the actual Gram row at h=3,4"
        ),
        "remaining_scope": (
            "this bounded computation does not construct the physical augmented lift"
        ),
    }


def current_head_scope_audit() -> dict[str, object]:
    conservation = (ROOT / (
        "computations/verify_h3_db01_dl01_literal_private_eq_conservation_gate.py"
    )).read_text()
    gamma = (ROOT / (
        "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py"
    )).read_text()
    proof = (ROOT / "PROOF-SKETCH.md").read_text()
    frontier = (ROOT / "notes/2026-08-13-three-interface-proof-frontier.md").read_text()
    endpoint = (ROOT / (
        "computations/verify_uniform_centered_occurrence_endpoint_association_projector.py"
    )).read_text()
    coefficient_body = endpoint.split("def full_coefficient_projector_audit()", 1)[1] \
        .split("def physical_lift_audit()", 1)[0]
    require("defined by zero-extension" in conservation
            and "no source-labelled response-to-AugP2" in conservation
            and "a completed full decorated physical source equivalence beyond this grammar"
                in gamma
            and "[P-prose]" in proof
            and "Hypotheses A2–A4 and" in proof
            and "A11 are independent open statements" in proof
            and "The all-order coefficient problem is now completely solved"
                in frontier
            and "polynomial_apply" not in coefficient_body
            and "apply_endpoint" not in coefficient_body,
            "a current-head disclosure/certification boundary changed")
    return {
        "c24_zero_extension_disclosed": True,
        "c24_cross_grade_comparison_disclosed_missing": True,
        "Theorem_B_now_labelled": "P-prose",
        "Proposition_5_2_now_lists": ["A2", "A3", "A4", "A11"],
        "Gamma_star_census_closed_for": "declared canonical cellular grammar",
        "Gamma_star_full_physical_equivalence_proved": False,
        "frontier_all_order_wording_still_stronger_than_committed_composite_test": True,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "external spine audit 2 adversarial reproducibility audit",
        "pins": PINS,
        "external_evidence_inventory": evidence_inventory_audit(),
        "B_Eq_tie_sensitivity": beq_tie_sensitivity_audit(),
        "projector_scope_and_actual_composite": projector_scope_and_composite_audit(),
        "current_HEAD_scope": current_head_scope_audit(),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("external spine2 audit ledger changed", digest))
    print("external audit2 evidence package: REPORT ONLY")
    print("B=Eq single-corner untie: RANK 7 SURVIVES, CLAIMED DUAL FAILS")
    print("Pi_match global idempotence: FALSE (documented scope 1+E1)")
    print("actual Pi_end Pi_match Gram composite h=3,4: NONZERO CONSTANT")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

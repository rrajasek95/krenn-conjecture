#!/usr/bin/env python3
"""Read-only theorem-hypothesis audit for the exact K24 charge residual."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

PINS = {
    "computations/unaudited-codex-orbit0-k24-complete35-audit-2026-08-24/results_k24_complete35_exact.json": "c9823d5c33b7e11b0c92eb89a50b33de0223fea5fdf53b2838b1094e13b9dfe6",
    "computations/unaudited-codex-orbit0-k16-cycle-partition-referee-2026-08-23/results_balanced_cycle_partition_referee.json": "9418fda557577fdf8828bf9a3faba595fba17c32e23c12ea8e9bccff8788d1aa",
    "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/REPORT.md": "6f7690a64a5b40656f2fb716f4464d63e7a5c12f7e4cd86d6ace2be3bc830ecb",
    "computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/results_k24_availability_schedule.json": "ec91fa81b164d1ecd83d234f5aa5d6c8ae5921f76f7b6d5c2145c4be3737f733",
    "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json": "469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa",
    "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/run_k24_charge_k14_source.rs": "dd9510f3324b160a3b496ba6d0b5bdfb9335699a1fc99cd75c18dadaf8eeca6d",
}


def fail(message: str) -> None:
    raise ValueError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(relative: str) -> dict:
    value = json.loads((ROOT / relative).read_text())
    if not isinstance(value, dict):
        fail(f"object required: {relative}")
    return value


def audit(assembly: dict, theorem: dict, reducer_report: str, schedule: dict) -> dict:
    if assembly.get("status") != "PASS_COMPLETE_K24_35_ID_SOURCE_EXTRACTED_ASSEMBLY_WITH_NONZERO_CONSERVATION_RESIDUAL":
        fail("source-extracted assembly status")
    coverage = assembly.get("coverage", {})
    if coverage.get("exact_set_equality") is not True or coverage.get("assembled_groups") != 10 or coverage.get("assembled_ids") != 35:
        fail("35-ID/10-group coverage")
    if assembly.get("actual_minus_forced_charge", {}).get("numerator") != 19_715_328 or assembly.get("actual_minus_forced_charge", {}).get("denominator") != 1:
        fail("exact residual")
    if assembly.get("cumulative_K14_through_K24", {}).get("numerator") != 19_715_328:
        fail("cumulative residual")
    if theorem.get("status") != "PASS_EXACT_Q_ABSTRACT_SEPARATOR_WITH_CONSERVATION_GUARD":
        fail("annihilator theorem status")
    if theorem.get("original_structured_aT_guard", {}).get("pairing") != 0:
        fail("structured target is not killed")
    if theorem.get("exact_linear_algebra", {}).get("abstract_profiles_annihilated") != 1162:
        fail("complete balanced profiles are not all killed")
    scope = theorem.get("theorem_scope", {})
    if "Every balanced degree24 mixed source column" not in scope.get("positive", ""):
        fail("complete-source annihilation scope missing")
    if "cannot prove localized or full-source nonmembership" not in scope.get("negative_guard", ""):
        fail("theorem negative guard missing")
    if "choice, not a pivot-independence theorem" not in reducer_report:
        fail("pivot nonconfluence guard missing")
    if schedule.get("status") != "PASS_EXACT_K24_35_ID_AVAILABILITY_SCHEDULE_NO_CHARGE" or schedule.get("required_ids") != 35:
        fail("availability schedule scope")
    if schedule.get("charge_run") is not False or schedule.get("residual_run") is not False:
        fail("availability schedule promoted to charge/residual proof")

    return {
        "status": "PASS_EXACT_K24_CONSERVATION_HYPOTHESIS_CLASSIFICATION",
        "exact_residual": {"charge": "19715328", "scaled_U": "7897796743805337600"},
        "theorem": {
            "statement": "If the structured target is killed by the functional and the ledger is the complete exact subtraction of complete balanced source columns, then the total charge over all filtration layers is zero.",
            "proof_rule": "linearity: the functional kills the target and each complete source column",
            "policy_dependence": "a pivot policy may redistribute charge between pages, but no complete exact source-column subtraction can acquire nonzero total charge",
        },
        "hypotheses": [
            {"name": "functional_kills_original_structured_target", "state": "MET", "evidence": "original_structured_aT_guard.pairing=0"},
            {"name": "functional_kills_every_complete_balanced_source_column", "state": "MET", "evidence": "1162/1162 abstract profiles annihilated exactly over Q"},
            {"name": "K24_manifest_is_exact_frozen_DAG_partition", "state": "MET", "evidence": "10 groups, 35 unique IDs, no missing/duplicate/extra"},
            {"name": "K24_group_scalars_and_occurrencewise_terminal_charges_are_exact_as_artifacts", "state": "MET", "evidence": "source-extracted pinned values; full=irreducible; grouped scalar counted once"},
            {"name": "assembled_K14_through_K24_ledger_is_one_complete_exact_source_column_subtraction", "state": "NOT_MET_AND_CONTRADICTED", "evidence": "its exact total is 19715328, whereas the two met annihilation premises force zero for any such subtraction"},
            {"name": "chosen_filtered_recurrence_is_policy_independent_or_confluent", "state": "NOT_MET", "evidence": "the frozen reducer records a literal K16 critical-pair obstruction and calls all-pivot averaging a choice"},
        ],
        "yes_no": {
            "is_the_residual_possible_for_a_genuine_complete_exact_source_column_subtraction": False,
            "does_the_theorem_rule_out_accepting_this_ledger_as_complete_and_source_faithful": True,
            "are_all_hypotheses_met_to_identify_the_numeric_ledger_with_that_subtraction": False,
            "does_the_theorem_invalidate_the_source_extracted_10_group_arithmetic_sum": False,
            "does_the_residual_prove_K24_nonmembership": False,
            "does_the_residual_decide_the_Krenn_Gu_conjecture": False,
        },
        "verdict": "The residual is a valid conservation acceptance obstruction, not a conjecture or nonmembership obstruction: it proves that at least one completeness/provenance/sign/normalization linkage in the purported full filtered ledger is false, but does not locate which one.",
        "required_repair_guard": "Do not promote the K24 ledger to a complete reduction, terminal normal form, relative-span result, or conjecture verdict until a source-labelled K14-through-K24 replay under one specified policy has exact zero total and its lower transfers are pinned.",
        "source_pins": PINS,
        "python_optimize": sys.flags.optimize,
    }


def self_test(assembly: dict, theorem: dict, reducer: str, schedule: dict) -> dict:
    cases = []
    mutations = []
    x = copy.deepcopy(assembly); x["coverage"]["assembled_ids"] = 34; mutations.append(("incomplete_coverage", x, theorem, reducer, schedule))
    x = copy.deepcopy(assembly); x["actual_minus_forced_charge"]["numerator"] += 1; mutations.append(("wrong_residual", x, theorem, reducer, schedule))
    t = copy.deepcopy(theorem); t["original_structured_aT_guard"]["pairing"] = 1; mutations.append(("target_not_killed", assembly, t, reducer, schedule))
    t = copy.deepcopy(theorem); t["exact_linear_algebra"]["abstract_profiles_annihilated"] = 1161; mutations.append(("incomplete_annihilator", assembly, t, reducer, schedule))
    mutations.append(("missing_nonconfluence_guard", assembly, theorem, reducer.replace("choice, not a pivot-independence theorem", "unproved"), schedule))
    s = copy.deepcopy(schedule); s["charge_run"] = True; mutations.append(("availability_promoted_to_charge", assembly, theorem, reducer, s))
    for name, a, t, r, s in mutations:
        try:
            audit(a, t, r, s)
        except (ValueError, KeyError, TypeError) as exc:
            cases.append({"case": name, "rejected": True, "error": str(exc)})
        else:
            fail(f"hostile accepted: {name}")
    return {"status": "PASS_K24_CONSERVATION_HYPOTHESIS_HOSTILES", "cases": cases, "cases_passed": len(cases), "python_optimize": sys.flags.optimize}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE / "results_k24_conservation_hypothesis_audit.json")
    args = parser.parse_args()
    for relative, digest in PINS.items():
        if sha(ROOT / relative) != digest:
            fail(f"source pin mismatch: {relative}")
    assembly = load(next(key for key in PINS if key.endswith("results_k24_complete35_exact.json")))
    theorem = load(next(key for key in PINS if key.endswith("results_balanced_cycle_partition_referee.json")))
    reducer = (ROOT / next(key for key in PINS if key.endswith("filtered-k24-reducer-design-2026-08-23/REPORT.md"))).read_text()
    schedule = load(next(key for key in PINS if key.endswith("results_k24_availability_schedule.json")))
    result = self_test(assembly, theorem, reducer, schedule) if args.self_test else audit(assembly, theorem, reducer, schedule)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Lightweight terminal referee for the landed 16-path direct K21 charge."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "run_k21_direct_charge.rs"
PROVIDER = (ROOT / "computations"
            / "unaudited-codex-orbit0-filtered-k18-charge-2026-08-23"
            / "run_k18_charge.rs")
RESULT = HERE / "results_k21_direct_charge.json"
PLAN = HERE / "results_k21_direct_plan_referee.json"
DAG = (ROOT / "computations"
       / "unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23"
       / "results_recurrence_dag.json")
OUT = HERE / "results_k21_direct_terminal_referee.json"

U = 400_591_699_200
EXPECTED_HASHES = {
    "run_k21_direct_charge.rs":
        "b8387f0cda67d39ed605fc1c4aab2801d4231b7d71d50c5dae5cca361f61968d",
    "run_k18_charge.rs":
        "24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045",
    "results_k21_direct_charge.json":
        "3fb99bdf3e8f230bcc8fe61936de5cb9020623d628efc4f5bcefac9e73fe5899",
    "results_k21_direct_plan_referee.json":
        "6af4880ca1b398160d6a6e96dd0ecafe723e06c218c42052b62dfe93acd41300",
}
EXPECTED_IDS = [
    ["D17:234|R:4", "D17:243|R:4", "D17:324|R:4", "D17:333|R:4",
     "D17:342|R:4", "D17:423|R:4", "D17:432|R:4"],
    ["D18:244|R:3", "D18:334|R:3", "D18:343|R:3", "D18:424|R:3",
     "D18:433|R:3", "D18:442|R:3"],
    ["D19:344|R:2", "D19:434|R:2", "D19:443|R:2"],
]
TAIL_COUNTS = (60, 32, 12)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def fraction_record(value):
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": (str(value.numerator) if value.denominator == 1
                 else f"{value.numerator}/{value.denominator}"),
    }


def main():
    hashes = {
        SOURCE.name: digest(SOURCE),
        PROVIDER.name: digest(PROVIDER),
        RESULT.name: digest(RESULT),
        PLAN.name: digest(PLAN),
    }
    require(hashes == EXPECTED_HASHES, (hashes, EXPECTED_HASHES))

    result = json.loads(RESULT.read_text())
    plan = json.loads(PLAN.read_text())
    dag = json.loads(DAG.read_text())
    require(result["status"] == "PASS_COMPLETE_16_DIRECT_ID_K21_CHARGE",
            result["status"])
    require(plan["status"] ==
            "PASS_EXACT_SIGNATURE_LEVEL_DIRECT_K21_PLAN_REFEREE",
            plan["status"])
    require(plan["logical_sha256"] ==
            "1a05bf60b018d7d3eeed471de3cd9b6211029c4a8be9baa37f944e803e863292",
            plan["logical_sha256"])
    require(int(result["scale_U"]) == U, result["scale_U"])
    require(result["workers"] == 8 and 0 < result["elapsed_seconds"] < 300,
            (result["workers"], result["elapsed_seconds"]))
    require(result["individual_id_charges"] is None,
            result["individual_id_charges"])

    plan_by_degree = {group["source_degree"]: group
                      for group in plan["groups"]}
    checked_groups = []
    total_scaled = 0
    total_occurrences = 0
    total_parents = 0
    total_pivotable = 0
    total_pivot_uses = 0
    for index, (landed, expected_ids, tail_count) in enumerate(
            zip(result["groups"], EXPECTED_IDS, TAIL_COUNTS, strict=True)):
        degree = 17 + index
        expected = plan_by_degree[degree]
        require(landed["ids"] == expected_ids == expected["ids"],
                (degree, landed["ids"], expected_ids, expected["ids"]))
        comparisons = {
            "parents": "raw_parents",
            "pivotable_parents": "pivotable_parents",
            "pivot_uses": "pivot_uses",
            "full_occurrences": "full_K21_tail_occurrences",
            "irreducible_occurrences": "irreducible_K21_tail_occurrences",
        }
        for landed_key, plan_key in comparisons.items():
            require(landed[landed_key] == expected[plan_key],
                    (degree, landed_key, landed[landed_key], expected[plan_key]))
        require(landed["full_occurrences"] ==
                tail_count * landed["pivot_uses"],
                (degree, landed["full_occurrences"],
                 tail_count * landed["pivot_uses"]))
        require(landed["full_occurrences"] == landed["irreducible_occurrences"],
                (degree, landed["full_occurrences"],
                 landed["irreducible_occurrences"]))
        require(landed["full_charge_scaled"] ==
                landed["irreducible_charge_scaled"],
                (degree, landed["full_charge_scaled"],
                 landed["irreducible_charge_scaled"]))
        scaled = int(landed["full_charge_scaled"])
        charge = Fraction(scaled, U)
        require(charge < 0, (degree, charge))
        checked_groups.append({
            "source_degree": degree,
            "ids": landed["ids"],
            "parents": landed["parents"],
            "pivotable_parents": landed["pivotable_parents"],
            "pivot_uses": landed["pivot_uses"],
            "tail_terms_per_pivot": tail_count,
            "full_and_irreducible_occurrences": landed["full_occurrences"],
            "full_and_irreducible_charge_scaled_U": str(scaled),
            "full_and_irreducible_charge": fraction_record(charge),
        })
        total_scaled += scaled
        total_occurrences += landed["full_occurrences"]
        total_parents += landed["parents"]
        total_pivotable += landed["pivotable_parents"]
        total_pivot_uses += landed["pivot_uses"]

    expected_totals = (402_806_080, 330_638_080, 640_044_800,
                       25_738_368_000, -632_143_793_867_760_599_040)
    observed_totals = (total_parents, total_pivotable, total_pivot_uses,
                       total_occurrences, total_scaled)
    require(observed_totals == expected_totals,
            (observed_totals, expected_totals))

    covered = {item for group in EXPECTED_IDS for item in group}
    required_k21 = set(
        dag["required_reachable_lineage_ids_by_degree"]["21"])
    require(covered <= required_k21 and len(covered) == 16
            and len(required_k21) == 52,
            (len(covered), len(required_k21), sorted(covered - required_k21)))
    require(dag["model"]["direct_sign"] == -1
            and dag["model"]["response_sign_flip"] is True
            and dag["model"]["last_pivotable_parent_degree"] == 20,
            dag["model"])

    source = SOURCE.read_text()
    source_guards = {
        "scale_U_exact": "const U:i128=400_591_699_200;" in source,
        "signed_R8prime_mass":
            "(r.size as i128)*(r.coefficient as i128)" in source,
        "positive_response_weight":
            "let w=mass*U/(ps.len()as i128);" in source,
        "occurrence_level_exact_division":
            "assert_eq!(mass*U%(ps.len()as i128),0);" in source,
        "K17_K4_call": "mass,4,&e" in source,
        "K18_K3_call": "mass,3,&e" in source,
        "K19_K2_call": "mass,2,&e" in source,
        "atomic_result_write": "rename(tmp,OUT).unwrap()" in source,
    }
    require(all(source_guards.values()), source_guards)

    total_charge = Fraction(total_scaled, U)
    referee = {
        "schema": "orbit0-k21-direct-terminal-referee-v1",
        "status": "PASS_INDEPENDENT_TERMINAL_REFEREE_DIRECT16_K21_CHARGE",
        "scope": ("Hash/arithmetic/count/sign validation of the landed 16-path "
                  "direct-parent K21 charge; no rerun of the full parent job."),
        "terminal_result": {
            "covered_ids": 16,
            "required_K21_ids": 52,
            "is_complete_K21_page": False,
            "groups": checked_groups,
            "totals": {
                "parents": total_parents,
                "pivotable_parents": total_pivotable,
                "pivot_uses": total_pivot_uses,
                "full_and_irreducible_occurrences": total_occurrences,
                "full_and_irreducible_charge_scaled_U": str(total_scaled),
                "full_and_irreducible_charge": fraction_record(total_charge),
            },
        },
        "sign_and_scale_audit": {
            "direct_sign_from_P": -1,
            "one_response_sign_flip": -1,
            "response_sign_relative_to_signed_R8prime_mass": 1,
            "source_weight": "w=U*M_r/m with exact (U*M_r) mod m == 0 assertion",
            "observed_cycle_charge_sign": "negative in each group and total",
            "sign_guard": ("The positive response coefficient and negative cycle "
                           "charge are compatible because lambda(child) is signed."),
            "all_K21_children_irreducible": True,
            "reason": ("Independent signature enumeration gives full=irreducible "
                       "for all 25,738,368,000 tails; DAG last pivotable degree is K20."),
        },
        "source_guards": source_guards,
        "pinned_sha256": {
            str(SOURCE.relative_to(ROOT)): hashes[SOURCE.name],
            str(PROVIDER.relative_to(ROOT)): hashes[PROVIDER.name],
            str(RESULT.relative_to(ROOT)): hashes[RESULT.name],
            str(PLAN.relative_to(ROOT)): hashes[PLAN.name],
            str(DAG.relative_to(ROOT)): digest(DAG),
        },
    }
    logical = json.dumps(referee, sort_keys=True,
                         separators=(",", ":")).encode()
    referee["logical_sha256"] = sha256(logical).hexdigest()
    OUT.write_text(json.dumps(referee, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": referee["status"],
        "totals": referee["terminal_result"]["totals"],
        "source_sha256": hashes[SOURCE.name],
        "result_sha256": hashes[RESULT.name],
        "logical_sha256": referee["logical_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()

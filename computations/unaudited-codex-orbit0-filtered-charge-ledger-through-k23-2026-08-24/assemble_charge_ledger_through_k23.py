#!/usr/bin/env python3
"""Build the exact filtered charge-conservation ledger through complete K23."""

from fractions import Fraction
from pathlib import Path
import argparse
import copy
import hashlib
import json


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
THROUGH_K20 = ROOT / "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k20-2026-08-24/results_charge_ledger_through_k20.json"
THROUGH_K22 = ROOT / "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k22-2026-08-24/results_charge_ledger_through_k22.json"
K21_MANIFEST = ROOT / "computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24/k21_manifest_complete_52.json"
K21_RESULT = ROOT / "computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24/results_k21_complete_52_exact.json"
K22_MANIFEST = ROOT / "computations/unaudited-codex-orbit0-k22-charge-assembly-2026-08-24/k22_manifest_complete_76.json"
K22_RESULT = ROOT / "computations/unaudited-codex-orbit0-k22-charge-assembly-2026-08-24/results_k22_complete_76_exact.json"
K23_MANIFEST = ROOT / "computations/unaudited-codex-orbit0-k23-direct-k15-production-interface-2026-08-24/k23_manifest_complete_59_of_59.json"
K23_RESULT = ROOT / "computations/unaudited-codex-orbit0-k23-direct-k15-production-interface-2026-08-24/results_k23_complete_59_of_59.json"
STALE_K23_MANIFEST = ROOT / "computations/unaudited-codex-orbit0-k23-d14-source-three-fold-2026-08-24/k23_manifest_current_47_of_59.json"
STALE_K23_RESULT = ROOT / "computations/unaudited-codex-orbit0-k23-d14-source-three-fold-2026-08-24/results_k23_current_47_of_59_partial.json"
PINS = {
    THROUGH_K20: "696f9205f9411cc58b1b17f014c97fdc6d9ce5fbb936c36cf42870ffb3db5c25",
    THROUGH_K22: "2bddded61e04f7e789b633503ac40419833c00091fd1caa72b2092a99e066741",
    K21_MANIFEST: "9085dec995d7bbbc26f4f875b43cc54c8f5ad9e9d34af413e6dd3a4a4889fe96",
    K21_RESULT: "4df5a6316a8bfac70efb793d27f7e72ea269b491d8a565ecedb17d7997f81340",
    K22_MANIFEST: "731f6a111ce02ce2bfb40ccf465f0c7c631f1ed68106647ab5ca33288c82fdfe",
    K22_RESULT: "7e955126cf391d2b6cfcbbb694004a2a5a8915981332cd9cc80e26460d7624f1",
    K23_MANIFEST: "940d3c97e8dc3d91e1b003d5d37cc3123aa7e97f3051b046b37be4a95a973fe0",
    K23_RESULT: "ed8678d12c7ebd7a301951f9dfd9dc814a0f9dac8fd729086ad35143c916df7b",
    STALE_K23_MANIFEST: "35089c36f649a5942c3203ce0f6b1c612aef9ce9dd741e159edeb946074b13b1",
    STALE_K23_RESULT: "4308457e52b79396332b9a13a9310c22c85609f25017f3677698cbeb96018a87",
}
U = 400_591_699_200
EXPECTED_CHARGES = {
    "K14": Fraction(0),
    "K15": Fraction(0),
    "K16": Fraction(375127296),
    "K17": Fraction(-9747200926208, 6545),
    "K18": Fraction(109863564487489024, 24838275),
    "K19": Fraction(-2117855228554753792, 173867925),
    "K20": Fraction(12162234158979734656, 521603775),
    "K21": Fraction(-15276224591027275648, 521603775),
    "K22": Fraction(4753487002993355488, 173867925),
    "K23": Fraction(-428913276887351456, 24838275),
}
EXPECTED_COVERAGE = {"K18": 17, "K19": 24, "K20": 36,
                     "K21": 52, "K22": 76, "K23": 59}


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def logical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def rational(value):
    return Fraction(int(value["numerator"]), int(value["denominator"]))


def render(value):
    return {"numerator": value.numerator, "denominator": value.denominator,
            "text": str(value)}


def source(path, **extra):
    answer = {"path": str(path.relative_to(ROOT)), "sha256": PINS[path]}
    answer.update(extra)
    return answer


def validate_through_k22(ledger):
    require(ledger["status"] == "PASS_CORRECTED_COMPLETE_CHARGE_LEDGER_THROUGH_K22",
            "through-K22 status")
    require(set(ledger["charges"]) == set(EXPECTED_CHARGES) - {"K23"},
            "through-K22 degree set")
    for degree, expected in list(EXPECTED_CHARGES.items())[:-1]:
        require(rational(ledger["charges"][degree]) == expected,
                f"sealed {degree} charge")
    require(ledger["coverage"] == {key: EXPECTED_COVERAGE[key]
                                   for key in ("K18", "K19", "K20", "K21", "K22")},
            "through-K22 coverage")
    require(rational(ledger["cumulative_K14_through_K22"]) ==
            Fraction(144864541808678432, 11591195), "through-K22 cumulative")


def validate_complete_k23(result, manifest):
    require((result.get("status"), result.get("complete_K23_claim"),
             result.get("required_paths"), result.get("covered_paths"),
             result.get("required_scalar_groups"), result.get("scalar_groups")) ==
            ("PASS_COMPLETE_K23_59_ID_EXACT_Q", True, 59, 59, 17, 17),
            "K23 completion")
    require(result.get("missing_paths") == result.get("duplicate_paths") ==
            result.get("extra_paths") == [], "K23 path partition")
    require(result.get("missing_scalar_groups") == [], "K23 scalar-group coverage")
    ids = result.get("covered_ids")
    require(isinstance(ids, list) and len(ids) == len(set(ids)) == 59,
            "K23 exact ID census")
    require(manifest.get("degree") == 23 and int(manifest.get("scale_U", 0)) == U,
            "K23 manifest header")
    groups = manifest.get("groups")
    require(isinstance(groups, list) and len(groups) == 17 and
            sum(len(entry.get("ids", [])) for entry in groups) == 59,
            "K23 manifest completeness")
    require(result.get("manifest_logical_sha256") == logical(manifest),
            "K23 manifest logical digest")
    full = rational(result["full"])
    irreducible = rational(result["irreducible"])
    require(full == irreducible == EXPECTED_CHARGES["K23"] and
            result.get("full_equals_irreducible") is True, "K23 exact charge")
    require(Fraction(int(result["full_scaled_U"]), U) == full and
            result["full_scaled_U"] == result["irreducible_scaled_U"],
            "K23 scaled-U charge")


def build(through_k22, k23_result, k23_manifest):
    validate_through_k22(through_k22)
    validate_complete_k23(k23_result, k23_manifest)
    charges = copy.deepcopy(through_k22["charges"])
    charges["K23"] = render(EXPECTED_CHARGES["K23"])
    require(set(charges) == set(EXPECTED_CHARGES), "ledger degree set")
    cumulative = sum((rational(charges[key]) for key in EXPECTED_CHARGES), Fraction())
    require(cumulative == Fraction(-829424811081283712, 173867925),
            "cumulative through K23")
    compensation = -cumulative
    coverage = dict(through_k22["coverage"])
    coverage["K23"] = 59
    require(coverage == EXPECTED_COVERAGE, "complete coverage ledger")
    return {
        "status": "PASS_COMPLETE_FILTERED_CHARGE_LEDGER_THROUGH_K23",
        "charges": charges,
        "coverage": coverage,
        "cumulative_K14_through_K23": render(cumulative),
        "necessary_K24_aggregate_charge_under_conservation": render(compensation),
        "conservation_equation": "sum_{k=14}^{24} charge(K_k)=0, hence charge(K24)=-sum_{k=14}^{23} charge(K_k)",
        "condition_scope": {
            "necessary_only": True,
            "assumption": "the frozen filtered 77-cycle recurrence is completed through K24 under the same charge convention and its total charge is zero",
            "does_not_establish_K24_charge_computation": True,
            "does_not_establish_residual_membership": True,
            "does_not_establish_terminal_span": True,
            "does_not_establish_conjecture_verdict": True,
        },
        "sources": {
            "K14_through_K20_ledger": source(THROUGH_K20),
            "K21_manifest": source(K21_MANIFEST),
            "K21_result": source(K21_RESULT),
            "K22_manifest": source(K22_MANIFEST),
            "K22_result": source(K22_RESULT),
            "K14_through_K22_ledger": source(THROUGH_K22),
            "K23_manifest": source(K23_MANIFEST,
                                   logical_sha256=logical(k23_manifest)),
            "K23_result": source(K23_RESULT),
        },
        "scope": "Exact filtered charge ledger through complete K23. The displayed K24 number is only the necessary aggregate compensation imposed by charge conservation, not a K24 membership or terminal-span result.",
    }


def load():
    for path, digest in PINS.items():
        require(path.is_file() and sha(path) == digest, f"pin {path}")
    return (json.loads(THROUGH_K22.read_text()), json.loads(K23_RESULT.read_text()),
            json.loads(K23_MANIFEST.read_text()))


def self_test(inputs):
    through_k22, complete_result, complete_manifest = inputs
    good = build(*inputs)
    require(good["coverage"]["K23"] == 59, "positive self-test")
    rejected = []

    partial_result = json.loads(STALE_K23_RESULT.read_text())
    partial_manifest = json.loads(STALE_K23_MANIFEST.read_text())
    try:
        build(through_k22, partial_result, partial_manifest)
    except ValueError as error:
        require("K23 completion" in str(error), "actual partial rejection reason")
        rejected.append("actual_stale_47_of_59_result_and_manifest")
    else:
        raise ValueError("actual stale 47/59 K23 accepted")

    mutation = copy.deepcopy(complete_result)
    mutation["covered_paths"] = 58
    try:
        build(through_k22, mutation, complete_manifest)
    except ValueError as error:
        require("K23 completion" in str(error), "forged partial rejection reason")
        rejected.append("forged_58_of_59_complete_status")
    else:
        raise ValueError("forged partial K23 accepted")

    try:
        build(through_k22, complete_result, partial_manifest)
    except ValueError as error:
        require("manifest completeness" in str(error) or "logical digest" in str(error),
                "stale manifest rejection reason")
        rejected.append("complete_result_with_stale_47_of_59_manifest")
    else:
        raise ValueError("stale K23 manifest accepted")

    mutation = copy.deepcopy(complete_result)
    mutation["irreducible"]["numerator"] += 1
    try:
        build(through_k22, mutation, complete_manifest)
    except ValueError as error:
        require("exact charge" in str(error), "charge mutation rejection reason")
        rejected.append("mutated_K23_charge")
    else:
        raise ValueError("mutated K23 charge accepted")

    return {
        "status": "PASS_CHARGE_LEDGER_THROUGH_K23_HOSTILE_SELFTEST",
        "pinned_hashes": True,
        "rejected": rejected,
        "stale_or_partial_K23_rejected": True,
        "K24_condition_kept_aggregate_only": True,
    }


def atomic(path, value):
    require(not path.exists(), f"refuse overwrite {path}")
    temporary = Path(str(path) + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    inputs = load()
    if args.self_test:
        result = self_test(inputs)
        atomic(HERE / "results_charge_ledger_through_k23_hostile_selftest.json", result)
    else:
        result = build(*inputs)
        atomic(HERE / "results_charge_ledger_through_k23.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

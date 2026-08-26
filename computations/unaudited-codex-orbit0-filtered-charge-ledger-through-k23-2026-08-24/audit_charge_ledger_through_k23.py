#!/usr/bin/env python3
"""Independent fail-closed audit of the complete filtered ledger through K23."""

from fractions import Fraction
from pathlib import Path
import copy
import hashlib
import json


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEDGER = HERE / "results_charge_ledger_through_k23.json"
BUILDER = HERE / "assemble_charge_ledger_through_k23.py"
SELFTEST = HERE / "results_charge_ledger_through_k23_hostile_selftest.json"
THROUGH20 = ROOT / "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k20-2026-08-24/results_charge_ledger_through_k20.json"
THROUGH22 = ROOT / "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k22-2026-08-24/results_charge_ledger_through_k22.json"
K21_MANIFEST = ROOT / "computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24/k21_manifest_complete_52.json"
K21_RESULT = ROOT / "computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24/results_k21_complete_52_exact.json"
K22_MANIFEST = ROOT / "computations/unaudited-codex-orbit0-k22-charge-assembly-2026-08-24/k22_manifest_complete_76.json"
K22_RESULT = ROOT / "computations/unaudited-codex-orbit0-k22-charge-assembly-2026-08-24/results_k22_complete_76_exact.json"
K23_MANIFEST = ROOT / "computations/unaudited-codex-orbit0-k23-direct-k15-production-interface-2026-08-24/k23_manifest_complete_59_of_59.json"
K23_RESULT = ROOT / "computations/unaudited-codex-orbit0-k23-direct-k15-production-interface-2026-08-24/results_k23_complete_59_of_59.json"
STALE_K23_RESULT = ROOT / "computations/unaudited-codex-orbit0-k23-d14-source-three-fold-2026-08-24/results_k23_current_47_of_59_partial.json"
PINS = {
    LEDGER: "45c94294cee372dc0674efd68e1cd02144f5af9c1366c9b1c7f9ff02b72b01a8",
    BUILDER: "91f1dc682da9180a9bd59517a8797b618c8e4d0223df7ea7ec46eeabfea08015",
    SELFTEST: "44d951fc4a081e39832f3db08d6f522f01703eb7da7802346e0db5e598e2fbcb",
    THROUGH20: "696f9205f9411cc58b1b17f014c97fdc6d9ce5fbb936c36cf42870ffb3db5c25",
    THROUGH22: "2bddded61e04f7e789b633503ac40419833c00091fd1caa72b2092a99e066741",
    K21_MANIFEST: "9085dec995d7bbbc26f4f875b43cc54c8f5ad9e9d34af413e6dd3a4a4889fe96",
    K21_RESULT: "4df5a6316a8bfac70efb793d27f7e72ea269b491d8a565ecedb17d7997f81340",
    K22_MANIFEST: "731f6a111ce02ce2bfb40ccf465f0c7c631f1ed68106647ab5ca33288c82fdfe",
    K22_RESULT: "7e955126cf391d2b6cfcbbb694004a2a5a8915981332cd9cc80e26460d7624f1",
    K23_MANIFEST: "940d3c97e8dc3d91e1b003d5d37cc3123aa7e97f3051b046b37be4a95a973fe0",
    K23_RESULT: "ed8678d12c7ebd7a301951f9dfd9dc814a0f9dac8fd729086ad35143c916df7b",
    STALE_K23_RESULT: "4308457e52b79396332b9a13a9310c22c85609f25017f3677698cbeb96018a87",
}
EXPECTED = {
    "K14": Fraction(0), "K15": Fraction(0),
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
TOP_KEYS = {"status", "charges", "coverage", "cumulative_K14_through_K23",
            "necessary_K24_aggregate_charge_under_conservation",
            "conservation_equation", "condition_scope", "sources", "scope"}
CONDITION_KEYS = {"necessary_only", "assumption",
                  "does_not_establish_K24_charge_computation",
                  "does_not_establish_residual_membership",
                  "does_not_establish_terminal_span",
                  "does_not_establish_conjecture_verdict"}
SOURCE_KEYS = {"K14_through_K20_ledger", "K14_through_K22_ledger",
               "K21_manifest", "K21_result", "K22_manifest", "K22_result",
               "K23_manifest", "K23_result"}


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def logical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def rational(value):
    require(type(value) is dict and set(value) == {"numerator", "denominator", "text"},
            "rational schema")
    answer = Fraction(int(value["numerator"]), int(value["denominator"]))
    require(value["text"] == str(answer), "rational rendering")
    return answer


def validate_direct_sources():
    through20 = json.loads(THROUGH20.read_text())
    require(through20["status"] == "PASS_CORRECTED_COMPLETE_CHARGE_LEDGER_THROUGH_K20",
            "through20 status")
    for degree in list(EXPECTED)[:7]:
        require(rational(through20["charges"][degree]) == EXPECTED[degree],
                f"direct source {degree}")
    expected_results = [
        (K21_RESULT, "PASS_COMPLETE_K21_52_ID_EXACT_Q", 52, EXPECTED["K21"]),
        (K22_RESULT, "PASS_COMPLETE_K22_76_ID_EXACT_Q", 76, EXPECTED["K22"]),
        (K23_RESULT, "PASS_COMPLETE_K23_59_ID_EXACT_Q", 59, EXPECTED["K23"]),
    ]
    for path, status, count, charge in expected_results:
        result = json.loads(path.read_text())
        require(result["status"] == status and result["required_paths"] ==
                result["covered_paths"] == count, f"direct completion {path.name}")
        require(result["missing_paths"] == result["duplicate_paths"] ==
                result["extra_paths"] == [], f"direct partition {path.name}")
        require(rational(result["full"]) == rational(result["irreducible"]) == charge,
                f"direct charge {path.name}")
    k23 = json.loads(K23_RESULT.read_text())
    manifest = json.loads(K23_MANIFEST.read_text())
    require(k23["complete_K23_claim"] is True and k23["scalar_groups"] == 17 and
            len(k23["covered_ids"]) == len(set(k23["covered_ids"])) == 59,
            "direct complete K23 shape")
    require(k23["manifest_logical_sha256"] == logical(manifest) and
            len(manifest["groups"]) == 17, "direct K23 manifest")
    stale = json.loads(STALE_K23_RESULT.read_text())
    require(stale["status"] == "REJECT_INCOMPLETE_K23_59_ID_GATE" and
            stale["complete_K23_claim"] is False and stale["covered_paths"] == 47,
            "pinned stale K23 control")


def validate_ledger(ledger):
    require(type(ledger) is dict and set(ledger) == TOP_KEYS, "ledger exact keys")
    require(ledger["status"] == "PASS_COMPLETE_FILTERED_CHARGE_LEDGER_THROUGH_K23",
            "ledger status")
    require(type(ledger["charges"]) is dict and set(ledger["charges"]) == set(EXPECTED),
            "charge degree set")
    observed = {}
    for degree, expected in EXPECTED.items():
        observed[degree] = rational(ledger["charges"][degree])
        require(observed[degree] == expected, f"ledger {degree} charge")
    require(ledger["coverage"] == EXPECTED_COVERAGE, "coverage")
    cumulative = sum(observed.values(), Fraction())
    require(cumulative == Fraction(-829424811081283712, 173867925),
            "independent cumulative")
    require(rational(ledger["cumulative_K14_through_K23"]) == cumulative,
            "reported cumulative")
    compensation = rational(ledger["necessary_K24_aggregate_charge_under_conservation"])
    require(compensation == -cumulative == Fraction(829424811081283712, 173867925),
            "necessary K24 aggregate compensation")
    require(ledger["conservation_equation"] ==
            "sum_{k=14}^{24} charge(K_k)=0, hence charge(K24)=-sum_{k=14}^{23} charge(K_k)",
            "conservation equation")
    condition = ledger["condition_scope"]
    require(type(condition) is dict and set(condition) == CONDITION_KEYS,
            "condition exact keys")
    require(condition["necessary_only"] is True and
            all(condition[key] is True for key in CONDITION_KEYS if key.startswith("does_not_")),
            "necessary-only guards")
    require("completed through K24" in condition["assumption"] and
            "total charge is zero" in condition["assumption"], "condition assumption")
    require("not a K24 membership or terminal-span result" in ledger["scope"],
            "scope boundary")
    require(set(ledger["sources"]) == SOURCE_KEYS, "source set")
    expected_source_paths = {
        "K14_through_K20_ledger": THROUGH20, "K14_through_K22_ledger": THROUGH22,
        "K21_manifest": K21_MANIFEST, "K21_result": K21_RESULT,
        "K22_manifest": K22_MANIFEST, "K22_result": K22_RESULT,
        "K23_manifest": K23_MANIFEST, "K23_result": K23_RESULT,
    }
    for name, path in expected_source_paths.items():
        entry = ledger["sources"][name]
        require(entry["path"] == str(path.relative_to(ROOT)) and
                entry["sha256"] == PINS[path], f"source pin {name}")
        if name == "K23_manifest":
            require(entry["logical_sha256"] == logical(json.loads(path.read_text())),
                    "K23 manifest logical pin")
        else:
            require(set(entry) == {"path", "sha256"}, f"source schema {name}")
    return cumulative, compensation


def reject(label, mutation, expected):
    try:
        validate_ledger(mutation)
    except ValueError as error:
        require(expected in str(error), f"{label}: wrong rejection {error}")
        return label
    raise ValueError(f"hostile ledger accepted: {label}")


def main():
    for path, digest in PINS.items():
        require(path.is_file() and sha(path) == digest, f"file pin {path}")
    validate_direct_sources()
    ledger = json.loads(LEDGER.read_text())
    cumulative, compensation = validate_ledger(ledger)
    rejected = []
    mutation = copy.deepcopy(ledger)
    mutation["charges"]["K23"]["numerator"] += 1
    mutation["charges"]["K23"]["text"] = str(Fraction(
        mutation["charges"]["K23"]["numerator"],
        mutation["charges"]["K23"]["denominator"]))
    rejected.append(reject("mutated_K23_charge", mutation, "ledger K23 charge"))
    mutation = copy.deepcopy(ledger)
    mutation["sources"]["K23_result"]["sha256"] = PINS[STALE_K23_RESULT]
    rejected.append(reject("stale_47_of_59_result_hash", mutation, "source pin K23_result"))
    mutation = copy.deepcopy(ledger)
    mutation["coverage"]["K23"] = 47
    rejected.append(reject("partial_K23_coverage", mutation, "coverage"))
    mutation = copy.deepcopy(ledger)
    mutation["necessary_K24_aggregate_charge_under_conservation"]["numerator"] *= -1
    mutation["necessary_K24_aggregate_charge_under_conservation"]["text"] = str(
        -compensation)
    rejected.append(reject("wrong_compensation_sign", mutation,
                           "necessary K24 aggregate compensation"))
    mutation = copy.deepcopy(ledger)
    mutation["condition_scope"]["necessary_only"] = False
    rejected.append(reject("condition_promoted_to_sufficient", mutation,
                           "necessary-only guards"))
    mutation = copy.deepcopy(ledger)
    mutation["condition_scope"]["K24_membership_established"] = True
    rejected.append(reject("injected_membership_claim", mutation, "condition exact keys"))
    payload = {
        "status": "PASS_INDEPENDENT_FILTERED_CHARGE_LEDGER_THROUGH_K23_AUDIT",
        "degrees": list(EXPECTED),
        "coverage": EXPECTED_COVERAGE,
        "cumulative_K14_through_K23": str(cumulative),
        "necessary_K24_aggregate_charge_under_conservation": str(compensation),
        "condition_is_necessary_not_sufficient": True,
        "does_not_establish_K24_membership_span_or_conjecture": True,
        "direct_degree_results_and_manifest_hashes_replayed": True,
        "actual_stale_47_of_59_control_rejected": True,
        "hostile_rejected": rejected,
        "ledger_sha256": PINS[LEDGER],
        "builder_sha256": PINS[BUILDER],
        "builder_hostile_selftest_sha256": PINS[SELFTEST],
    }
    payload["logical_sha256"] = logical(payload)
    output = HERE / "results_charge_ledger_through_k23_independent_audit.json"
    require(not output.exists(), f"refuse overwrite {output}")
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

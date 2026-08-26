#!/usr/bin/env python3
"""Independent exact-Q audit of the complete 35-ID K24 charge ledger.

This is deliberately a charge-only audit.  A nonzero completed total rejects
the claimed filtered decomposition; it is not promoted to ideal nonmembership.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
U = 400_591_699_200


def rp(relative: str) -> Path:
    return ROOT / relative


CONTRACT = rp("computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/k24_expected_scalar_groups.json")
DAG = rp("computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json")
MANIFEST = HERE / "k24_manifest_complete_35_of_35.json"
K23_LEDGER = rp("computations/unaudited-codex-orbit0-k23-complete59-audit-2026-08-24/results_charge_ledger_through_k23.json")
K23_AUDIT = rp("computations/unaudited-codex-orbit0-k23-complete59-audit-2026-08-24/results_k23_complete59_independent_audit.json")
THEOREM = rp("computations/unaudited-codex-orbit0-k16-cycle-partition-referee-2026-08-23/results_balanced_cycle_partition_referee.json")
K23_REPORT = rp("computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k23-2026-08-24/REPORT.md")
REDUCER_REPORT = rp("computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/REPORT.md")
CHART_REPORT = rp("computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21/REPORT.md")
TERMINAL_REPORT = rp("computations/unaudited-codex-orbit0-k24-terminal-structure-2026-08-23/REPORT.md")


RESULTS = {
    "hidden_collected": rp("computations/unaudited-codex-orbit0-k24-hidden-collected-fast-launch-acceptance-2026-08-24/results_hidden_collected_complete.json"),
    "hidden_decorated": rp("computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_hidden_decorated_complete.json"),
    "k14": rp("computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k14_source_complete.json"),
    "k15": rp("computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_direct_k15_complete_fragment.json"),
    "k16_r224": rp("computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k16_r224_complete.json"),
    "k16_r44": rp("computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_k16_r44_support_v4_complete.json"),
    "direct17": rp("computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_direct_d17_d18_complete.json"),
}


ACCEPTANCE = {
    "hidden_collected": rp("computations/unaudited-codex-orbit0-k24-hidden-collected-fast-launch-acceptance-2026-08-24/results_hidden_collected_complete.acceptance.json"),
    "hidden_decorated": rp("computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_hidden_decorated_complete_independent_referee.json"),
    "k14": rp("computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_k14_source_complete_referee.json"),
    "k15": rp("computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_direct_k15_complete_acceptance.json"),
    "k16_r224": rp("computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k16_r224_two_half_merge_validation.json"),
    "k16_r44": rp("computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_k16_r44_support_v4_complete_validation.json"),
    "direct17": rp("computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_direct_d17_d18_complete_referee.json"),
}


PINS = {
    CONTRACT: "9ee7c5b6c31b70a7e06f8a4909c8b9aa77a87444cb12992c9971b5259bb8a986",
    DAG: "469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa",
    K23_LEDGER: "5f9249642fdc9feb0efc9be8052a8cecf8d56270c17e868debebd9334b5f1b56",
    K23_AUDIT: "b822cc1510a8a09fbc9b077a4aa37eaf4863fe1ca0880d4c25b868ac0b224f45",
    THEOREM: "9418fda557577fdf8828bf9a3faba595fba17c32e23c12ea8e9bccff8788d1aa",
    K23_REPORT: "28135687e700ada8dca7bda143565886c16d5514ff224c922427bcd81d04cd80",
    REDUCER_REPORT: "6f7690a64a5b40656f2fb716f4464d63e7a5c12f7e4cd86d6ace2be3bc830ecb",
    CHART_REPORT: "e42f3ea829a0c3c0cfe9b03aed64d1059ed512ff9f3d1f0fba2c14ed46707f41",
    TERMINAL_REPORT: "6ad4447dd63eec6110fd5765290e06bc7e0e30774e71a5ad15764b7eb5fb3c41",
    RESULTS["hidden_collected"]: "61a763a59c9419bf5b272b6c4f2679c0eb495627c6c3f319d87723cb44ed6e42",
    RESULTS["hidden_decorated"]: "5ee0aff3cc6e95ad25a2c5e74a03cbb3cac340979ad3f04ed37dd56519155e52",
    RESULTS["k14"]: "f188ec896a6782cff185c91b369b9e71fcbe661bbafbe61d625cdc51e02ba442",
    RESULTS["k15"]: "1b6c76e99a527cd82632f59ef9abc3d25dca088a28a55ef75acb7f5c008e174f",
    RESULTS["k16_r224"]: "4d5ad45e7b0d7f29a607e623e3f045f928cdfeae6fc8074cb2cdb054be501b12",
    RESULTS["k16_r44"]: "90148636cd74671efa96fa70c8c0e4bd2195d81c7fe5aa3ff17db53e4ffeef76",
    RESULTS["direct17"]: "cc838dded783de9f41845626f4e49b8d8250bf328497cc978cab6096d888546b",
    ACCEPTANCE["hidden_collected"]: "34d9da48f426f6831e1e861f8613eae9aa6c176406c24310a12badeec74e0507",
    ACCEPTANCE["hidden_decorated"]: "cf7935b6deb335213cadd64b1718f7b5d826fca9e0f7d6ee79132109caf673a4",
    ACCEPTANCE["k14"]: "a161996106815e6221a97ad8af8c11c99649539466315b503952fb548d6986b3",
    ACCEPTANCE["k15"]: "6c8ec30ee38920592dc7f9d4a5cf3db88debe0a5305434b9ad4978b2ae44ff44",
    ACCEPTANCE["k16_r224"]: "de4da6ddb44f27709219d2b640e3efd4fe8354247895ccb81852a865dbd35077",
    ACCEPTANCE["k16_r44"]: "73ff3d550aa23a509a196d22674dfa6e6a239c9f829942f29455a384c7aeb2a5",
    ACCEPTANCE["direct17"]: "0f9a1720a20465ffec3b9abcb33285c9594c8c36f96af9805b225e98c1e62f3c",
}


EXPECTED_STATUSES = {
    "hidden_collected": "PASS_COMPLETE_HIDDEN_COLLECTED_FAST_PRODUCTION_ACCEPTANCE",
    "hidden_decorated": "PASS_INDEPENDENT_K24_HIDDEN_DECORATED_COMPLETE_REFEREE",
    "k14": "PASS_COMPLETE_K24_K14_CHARGE_REFEREE_WITH_LITERAL_ZERO_SUPPORT_DISCLOSURE",
    "k15": "PASS_COMPLETE_STRICT_GROUPED_K15_SIX_ID_K24_CHARGE_ACCEPTED",
    "k16_r224": "PASS_COMPLETE_K24_K16_R224_TWO_HALF_MERGE_STRUCTURE",
    "k16_r44": "PASS_COMPLETE_K24_FAST_K16_R44_STRUCTURE",
    "direct17": "PASS_COMPLETE_K24_DIRECT_D17_D18_CHARGE_REFEREE",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ValueError(str(message))


def frac(value: object) -> Fraction:
    if isinstance(value, dict):
        return Fraction(int(value["numerator"]), int(value["denominator"]))
    return Fraction(value)


def render(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator, "text": str(value)}


def source_groups(documents: dict[str, dict]) -> dict[str, dict]:
    """Extract the ten group records directly from seven heterogeneous results."""
    answer: dict[str, dict] = {}

    hidden = documents["hidden_collected"]
    answer["source_D14_R2_2_2_4"] = {
        "ids": [hidden["strict_id"]],
        "scaled": int(hidden["full_charge_scaled_U"]),
        "irreducible_scaled": int(hidden["irreducible_charge_scaled_U"]),
        "occurrences": int(hidden["full_occurrences"]),
    }

    decorated = documents["hidden_decorated"]
    answer["source_D14_R2_4_4"] = {
        "ids": decorated["covered_lineage_ids"],
        "scaled": int(decorated["sink"]["full_charge_scaled_U"]),
        "irreducible_scaled": int(decorated["sink"]["irreducible_charge_scaled_U"]),
        "occurrences": int(decorated["sink"]["full_occurrences"]),
    }

    k14 = documents["k14"]
    for group_id, lineage in (
        ("source_D14_R3_3_4", "D14:222|R:3-3-4"),
        ("source_D14_R4_2_4", "D14:222|R:4-2-4"),
    ):
        sink = k14["sinks"][lineage]
        answer[group_id] = {
            "ids": [lineage],
            "scaled": int(sink["full_charge_scaled_U"]),
            "irreducible_scaled": int(sink["irreducible_charge_scaled_U"]),
            "occurrences": int(sink["full_occurrences"]),
        }

    k15 = documents["k15"]
    for group_id, group in k15["groups"].items():
        answer[group_id] = {
            "ids": group["ids"],
            "scaled": int(group["charge_scaled_U"]),
            "irreducible_scaled": int(group["charge_scaled_U"]),
            "occurrences": int(group["full_occurrences"]),
        }

    for key, group_id in (("k16_r224", "source_D16_R2_2_4"), ("k16_r44", "source_D16_R4_4")):
        document = documents[key]
        answer[group_id] = {
            "ids": document["ids"],
            "scaled": int(document["full_charge_scaled_U"]),
            "irreducible_scaled": int(document["irreducible_charge_scaled_U"]),
            "occurrences": int(document["full_occurrences"]),
        }

    direct = documents["direct17"]
    for group in direct["groups"]:
        answer[group["group_id"]] = {
            "ids": group["ids"],
            "scaled": int(group["full_charge_scaled_U"]),
            "irreducible_scaled": int(group["irreducible_charge_scaled_U"]),
            "occurrences": int(group["full_occurrences"]),
        }
    return answer


def validate_acceptances(acceptance: dict[str, dict]) -> None:
    for family, expected in EXPECTED_STATUSES.items():
        require(acceptance[family].get("status") == expected, (family, acceptance[family].get("status")))

    require(acceptance["hidden_collected"]["result_sha256"] == PINS[RESULTS["hidden_collected"]], "hidden result linkage")
    require(acceptance["hidden_collected"]["literal_witnesses"] == 257, "hidden witnesses")
    require(acceptance["hidden_collected"]["literal_witnesses_source_backed"] is True, "hidden source backing")

    require(acceptance["hidden_decorated"]["result"]["sha256"] == PINS[RESULTS["hidden_decorated"]], "decorated result linkage")
    require(acceptance["hidden_decorated"]["literal_referee"]["literal_aggregates_replayed"] == 257, "decorated witnesses")
    require(acceptance["hidden_decorated"]["verdict"].startswith("ACCEPT_COMPLETE"), "decorated verdict")

    require(acceptance["k14"]["producer_evidence"]["result_sha256"] == PINS[RESULTS["k14"]], "K14 result linkage")
    require(acceptance["k14"]["literal_referee"]["witnesses_replayed"] == 514, "K14 witnesses")

    require(acceptance["k15"]["strict_fragment_sha256"] == PINS[RESULTS["k15"]], "K15 fragment linkage")
    require(acceptance["k15"]["no_gap"] and acceptance["k15"]["no_overlap"], "K15 intervals")
    require(acceptance["k15"]["merged_literal_witnesses_replayed"] == 514, "K15 witnesses")

    require(acceptance["k16_r224"]["merged_result_sha256"] == PINS[RESULTS["k16_r224"]], "K16 R224 result linkage")
    require(acceptance["k16_r224"]["no_gap_no_overlap"] is True, "K16 R224 intervals")
    require(acceptance["k16_r224"]["witnesses"] == 257, "K16 R224 witnesses")

    require(acceptance["k16_r44"]["result_sha256"] == PINS[RESULTS["k16_r44"]], "K16 R44 result linkage")
    require(acceptance["k16_r44"]["realized_support_bins"] == 37, "K16 R44 support")
    require(acceptance["k16_r44"]["witnesses"] == 257, "K16 R44 witnesses")

    require(acceptance["direct17"]["producer_evidence"]["result_sha256"] == PINS[RESULTS["direct17"]], "direct17 result linkage")
    repair = acceptance["direct17"]["literal_sample_repair"]
    require(repair["status"] == "PASS" and repair["witnesses_replayed"] == 514, "direct17 witnesses")


def validate_scope(scope: dict) -> None:
    require(scope == {
        "valid_filtered_conservation_obstruction": True,
        "obstructed_claim": "the frozen orbit0 same-convention 35-ID ledger is a complete source-faithful K14-through-K24 reduction",
        "ideal_nonmembership_certificate": False,
        "conjecture_counterexample": False,
        "policy_independent_nonzero_normal_form": False,
        "other_30_charts_covered": False,
        "literal_K24_residual_frozen": False,
        "terminal_span_or_relative_membership_decided": False,
    }, "scope promotion or weakening")


def audit(manifest: dict, documents: dict[str, dict], acceptance: dict[str, dict], ledger: dict, theorem: dict) -> dict:
    contract = load(CONTRACT)
    dag = load(DAG)
    expected = contract["groups"]
    required = dag["required_reachable_lineage_ids_by_degree"]["24"]
    require(contract["degree"] == 24 and int(contract["scale_U"]) == U, "contract degree/U")
    require(manifest.get("degree") == 24 and int(manifest.get("scale_U", 0)) == U, "manifest degree/U")
    require(len(expected) == 10 and sum(map(len, expected.values())) == 35, "contract census")
    require(len(required) == len(set(required)) == 35, "DAG census")
    require(set(required) == {lineage for ids in expected.values() for lineage in ids}, "contract/DAG set")

    extracted = source_groups(documents)
    require(set(extracted) == set(expected), ("source groups", sorted(set(expected) - set(extracted)), sorted(set(extracted) - set(expected))))
    validate_acceptances(acceptance)

    entries = manifest.get("groups")
    require(isinstance(entries, list), "manifest groups")
    group_counts = Counter(entry.get("group_id") for entry in entries)
    require(group_counts == Counter({group_id: 1 for group_id in expected}), ("manifest group counts", group_counts))
    covered: list[str] = []
    group_output = []
    for entry in entries:
        group_id = entry["group_id"]
        source = extracted[group_id]
        require(entry["ids"] == expected[group_id] == source["ids"], (group_id, "IDs"))
        require(entry["evidence_path"] == str(RESULTS[next(key for key, value in RESULTS.items() if PINS[value] == entry["evidence_sha256"])].relative_to(ROOT)), (group_id, "evidence path"))
        require(sha(rp(entry["evidence_path"])) == entry["evidence_sha256"], (group_id, "evidence hash"))
        full_scaled = int(entry["full_scaled_U"])
        irreducible_scaled = int(entry["irreducible_scaled_U"])
        require(full_scaled == irreducible_scaled == source["scaled"] == source["irreducible_scaled"], (group_id, "scalar"))
        require(frac(entry["full"]) == frac(entry["irreducible"]) == Fraction(full_scaled, U), (group_id, "rational"))
        covered.extend(entry["ids"])
        group_output.append({
            "group_id": group_id,
            "ids": entry["ids"],
            "full_scaled_U": str(full_scaled),
            "full": str(Fraction(full_scaled, U)),
            "full_occurrences": source["occurrences"],
            "evidence_sha256": entry["evidence_sha256"],
        })

    counts = Counter(covered)
    missing = sorted(set(required) - set(covered))
    duplicate = sorted(item for item, count in counts.items() if count != 1)
    extra = sorted(set(covered) - set(required))
    require(not missing and not duplicate and not extra and len(covered) == 35, (missing, duplicate, extra))

    total_scaled = sum(int(entry["full_scaled_U"]) for entry in entries)
    k24 = Fraction(total_scaled, U)
    require(total_scaled == 1_918_892_561_475_083_010_048, total_scaled)
    require(k24 == Fraction(832_852_674_251_338_112, 173_867_925), k24)

    require(ledger["status"] == "PASS_COMPLETE_CHARGE_LEDGER_THROUGH_K23", ledger["status"])
    require(ledger["coverage"] == {"K18": 17, "K19": 24, "K20": 36, "K21": 52, "K22": 76, "K23": 59}, "K23 coverage")
    through_k23 = frac(ledger["cumulative_K14_through_K23"])
    require(through_k23 == Fraction(-829_424_811_081_283_712, 173_867_925), through_k23)
    target = -through_k23
    target_scaled = target * U
    require(target_scaled.denominator == 1, target_scaled)
    mismatch = k24 - target
    cumulative = through_k23 + k24
    require(mismatch == cumulative == Fraction(19_715_328), mismatch)
    mismatch_scaled = mismatch * U
    require(mismatch_scaled == 7_897_796_743_805_337_600, mismatch_scaled)

    require(theorem["status"] == "PASS_EXACT_Q_ABSTRACT_SEPARATOR_WITH_CONSERVATION_GUARD", theorem["status"])
    require(theorem["original_structured_aT_guard"]["pairing"] == 0, "target charge")
    require(theorem["exact_linear_algebra"]["abstract_profiles_annihilated"] == 1162, "source profiles")
    positive = theorem["theorem_scope"]["positive"]
    require("Every balanced degree24 mixed source column" in positive and "annihilated" in positive, positive)
    require("cannot prove localized or full-source nonmembership" in theorem["theorem_scope"]["negative_guard"], "negative theorem guard")

    scope = {
        "valid_filtered_conservation_obstruction": True,
        "obstructed_claim": "the frozen orbit0 same-convention 35-ID ledger is a complete source-faithful K14-through-K24 reduction",
        "ideal_nonmembership_certificate": False,
        "conjecture_counterexample": False,
        "policy_independent_nonzero_normal_form": False,
        "other_30_charts_covered": False,
        "literal_K24_residual_frozen": False,
        "terminal_span_or_relative_membership_decided": False,
    }
    validate_scope(scope)

    return {
        "status": "PASS_EXACT_COMPLETE_K24_35_ID_SUM__FILTERED_CONSERVATION_OBSTRUCTION",
        "degree": 24,
        "scale_U": U,
        "coverage": {
            "required_ids": 35,
            "covered_ids": 35,
            "required_groups": 10,
            "covered_groups": 10,
            "missing": missing,
            "duplicate": duplicate,
            "extra": extra,
            "group_scalar_counted_once": True,
        },
        "groups": group_output,
        "K24": {"scaled_U": str(total_scaled), "charge": render(k24)},
        "forced_K24_target_from_K14_through_K23": {"scaled_U": str(target_scaled.numerator), "charge": render(target)},
        "K24_minus_forced_target": {"scaled_U": str(mismatch_scaled.numerator), "charge": render(mismatch)},
        "cumulative_K14_through_K24": render(cumulative),
        "conservation_implication": "Because the structured target and every complete balanced source column pair to zero, any complete exact source-column subtraction has total charge zero. The nonzero total therefore rejects completeness/source-faithful linkage of this frozen ledger; it cannot separate the target from the source ideal.",
        "presentation_vs_scope": {
            "H_orbit_representatives": "presentation only for exact orbit-mass sums; Reynolds/H-invariance leaves the aggregate charge unchanged",
            "pivot_policy": "may redistribute page/lineage charges and change representatives, but cannot change zero total for a complete exact source-column reduction",
            "other_filtered_branches": "one valid exact branch would suffice positively; a nonconfluent nonzero normal cannot prove nonmembership without confluence or an exact terminal dual",
            "other_charts": "genuine uncovered global scope; full S8xS3 transports between fixed charts and does not quotient the present terminal page",
        },
        "scope": scope,
        "remaining_exhaustive_scope": [
            "locate and repair the missing, duplicated, sign-flipped, U-misnormalized, or provenance-mislinked contribution causing the conservation failure",
            "reassemble a zero-total source-faithful orbit0 K14-through-K24 ledger under one fully specified pivot policy",
            "freeze the literal K24 H-orbit-mass residual with exact lower-correction provenance",
            "decide the relative terminal condition R24 in image(A24), or produce a dual nonmembership certificate pairing nonzero with R24",
            "supply the separate chart transports/overlap data for the other 30 charts and close the global induction hypotheses",
        ],
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in sorted(PINS.items(), key=lambda item: str(item[0]))},
        "manifest_sha256": sha(MANIFEST),
    }


def self_test() -> dict:
    manifest = load(MANIFEST)
    documents = {key: load(path) for key, path in RESULTS.items()}
    acceptance = {key: load(path) for key, path in ACCEPTANCE.items()}
    ledger = load(K23_LEDGER)
    theorem = load(THEOREM)
    baseline = audit(manifest, documents, acceptance, ledger, theorem)

    mutations = []
    changed_scalar = copy.deepcopy(manifest)
    changed_scalar["groups"][0]["full_scaled_U"] = str(int(changed_scalar["groups"][0]["full_scaled_U"]) + 1)
    mutations.append(("scalar", changed_scalar, documents, acceptance, ledger, theorem))
    missing = copy.deepcopy(manifest); missing["groups"].pop()
    mutations.append(("missing_group", missing, documents, acceptance, ledger, theorem))
    duplicate = copy.deepcopy(manifest); duplicate["groups"][0]["ids"] = duplicate["groups"][1]["ids"]
    mutations.append(("duplicate_or_regrouped_id", duplicate, documents, acceptance, ledger, theorem))
    wrong_u = copy.deepcopy(manifest); wrong_u["scale_U"] = U + 1
    mutations.append(("wrong_U", wrong_u, documents, acceptance, ledger, theorem))
    wrong_acceptance = copy.deepcopy(acceptance); wrong_acceptance["k16_r44"]["status"] = "PASS_FORGED"
    mutations.append(("acceptance", manifest, documents, wrong_acceptance, ledger, theorem))
    wrong_ledger = copy.deepcopy(ledger); wrong_ledger["cumulative_K14_through_K23"]["numerator"] *= -1
    mutations.append(("wrong_target_sign", manifest, documents, acceptance, wrong_ledger, theorem))
    wrong_theorem = copy.deepcopy(theorem); wrong_theorem["original_structured_aT_guard"]["pairing"] = 1
    mutations.append(("target_nonzero", manifest, documents, acceptance, ledger, wrong_theorem))
    failures = []
    for name, m, d, a, l, t in mutations:
        try:
            audit(m, d, a, l, t)
        except (ValueError, KeyError, StopIteration):
            failures.append(name)
        else:
            raise AssertionError(f"hostile accepted: {name}")

    hostile_scope = copy.deepcopy(baseline["scope"])
    hostile_scope["conjecture_counterexample"] = True
    try:
        validate_scope(hostile_scope)
    except ValueError:
        failures.append("conjecture_promotion")
    else:
        raise AssertionError("conjecture promotion accepted")

    return {
        "status": "PASS_K24_COMPLETE35_CONSERVATION_AUDIT_HOSTILES",
        "cases": failures,
        "count": len(failures),
        "expected_count": 8,
        "all_rejected": len(failures) == 8,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    for path, digest in PINS.items():
        require(sha(path) == digest, (str(path.relative_to(ROOT)), sha(path), digest))
    if args.self_test:
        result = self_test()
    else:
        result = audit(
            load(MANIFEST),
            {key: load(path) for key, path in RESULTS.items()},
            {key: load(path) for key, path in ACCEPTANCE.items()},
            load(K23_LEDGER),
            load(THEOREM),
        )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = Path(args.output)
        temporary = Path(str(output) + ".tmp")
        temporary.write_text(text)
        temporary.replace(output)
    print(text, end="")


if __name__ == "__main__":
    main()

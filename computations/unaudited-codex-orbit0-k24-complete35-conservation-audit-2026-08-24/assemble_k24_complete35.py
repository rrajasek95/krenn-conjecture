#!/usr/bin/env python3
"""Strict grouped-once K24 assembler and K14--K24 conservation check."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
U = 400_591_699_200

AVAIL = ROOT / "computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/results_k24_availability_schedule.json"
THROUGH23 = ROOT / "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k23-2026-08-24/results_charge_ledger_through_k23.json"
DIRECT = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_direct_d17_d18_complete.json"
K14 = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k14_source_complete.json"
K15 = ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_direct_k15_complete_fragment.json"
R224 = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k16_r224_complete.json"
R44 = ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_k16_r44_support_v4_complete.json"
HC = ROOT / "computations/unaudited-codex-orbit0-k24-hidden-collected-fast-launch-acceptance-2026-08-24/results_hidden_collected_complete.json"
HD = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_hidden_decorated_complete.json"

EVIDENCE = {
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_direct_d17_d18_complete_validation.json": "866e61be6e5f3e8e70880135e8fc01a63dd5ce9221a4d72f1722410577b8af0d",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_direct_d17_d18_complete_referee.json": "0f9a1720a20465ffec3b9abcb33285c9594c8c36f96af9805b225e98c1e62f3c",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k14_source_complete_validation.json": "dfcce3bb5c8aebf6b9f41245a3caa754bd6181b5917ac3a9556244b4daf5a747",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_k14_source_complete_referee.json": "a161996106815e6221a97ad8af8c11c99649539466315b503952fb548d6986b3",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_direct_k15_complete_acceptance.json": "6c8ec30ee38920592dc7f9d4a5cf3db88debe0a5305434b9ad4978b2ae44ff44",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_direct_k15_complete_merge_referee.json": "3e8928ad56cd614893be1932db0264e97f2d7d8df8ed6b3a55f164d0eb351e00",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_direct_k15_complete_literal_referee.json": "349be9168b1e3344c96719b0fe8294c5f08b67627972907ce681dbda605a8481",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k16_r224_two_half_merge_validation.json": "de4da6ddb44f27709219d2b640e3efd4fe8354247895ccb81852a865dbd35077",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k16_r224_complete_literal_referee.json": "3591a2413bc7ac438a0d39ff52fc7b589e4e973f00936c93a6bec3d69b382e02",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_k16_r44_support_v4_complete_validation.json": "73ff3d550aa23a509a196d22674dfa6e6a239c9f829942f29455a384c7aeb2a5",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_k16_r44_support_v4_complete_literal_referee.json": "b0e82c14e38bce30a78547210542c5be687d56889ef1d4ab67a17bd9262dc660",
    ROOT / "computations/unaudited-codex-orbit0-k24-k16-r44-support-v4-independent-audit-2026-08-24/results_independent_support_v4_audit.json": "e9a698052e6fa4a51413d07e5fd1ce76a3cd9108fdcd86199a26ed15df0a1aca",
    ROOT / "computations/unaudited-codex-orbit0-k24-hidden-collected-fast-launch-acceptance-2026-08-24/results_hidden_collected_complete.acceptance.json": "34d9da48f426f6831e1e861f8613eae9aa6c176406c24310a12badeec74e0507",
    ROOT / "computations/unaudited-codex-orbit0-k24-hidden-collected-fast-launch-acceptance-2026-08-24/results_hidden_collected_complete.validation.json": "5bad45144b3395389e14ca14fe4731e3ca3065664f6a797803073d1baa6c40e1",
    ROOT / "computations/unaudited-codex-orbit0-k24-hidden-collected-fast-launch-acceptance-2026-08-24/results_hidden_collected_complete.literal_referee.json": "b1392008a577ac70bcb343cf30311429f09239694d718131ef5453acb3fb8112",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_hidden_decorated_complete_validation.json": "9d32b55960ed5f4b8e2ff679a37d037aadae6d127bbfeaca03449a553134e47e",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_hidden_decorated_complete_independent_referee.json": "cf7935b6deb335213cadd64b1718f7b5d826fca9e0f7d6ee79132109caf673a4",
    ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/results_hidden_decorated_complete_literal_referee.json": "c0fede25f1d33131255cb939e55c142353e38ecf88a49ef230cee766944a9678",
}

PINS = {
    AVAIL: "ec91fa81b164d1ecd83d234f5aa5d6c8ae5921f76f7b6d5c2145c4be3737f733",
    THROUGH23: "45c94294cee372dc0674efd68e1cd02144f5af9c1366c9b1c7f9ff02b72b01a8",
    DIRECT: "cc838dded783de9f41845626f4e49b8d8250bf328497cc978cab6096d888546b",
    K14: "f188ec896a6782cff185c91b369b9e71fcbe661bbafbe61d625cdc51e02ba442",
    K15: "1b6c76e99a527cd82632f59ef9abc3d25dca088a28a55ef75acb7f5c008e174f",
    R224: "4d5ad45e7b0d7f29a607e623e3f045f928cdfeae6fc8074cb2cdb054be501b12",
    R44: "90148636cd74671efa96fa70c8c0e4bd2195d81c7fe5aa3ff17db53e4ffeef76",
    HC: "61a763a59c9419bf5b272b6c4f2679c0eb495627c6c3f319d87723cb44ed6e42",
    HD: "5ee0aff3cc6e95ad25a2c5e74a03cbb3cac340979ad3f04ed37dd56519155e52",
    ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/results_k16_cycle_partition_quotient.json": "d4cbc7350253bcec3cb34768386b7a83265251ef569b3f4654507da389a9b8bb",
    ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/REPORT.md": "1d6f71fbcdaa3369233bc78d6ba77c7482253ac29a27d4d9aa0c9dbb0908c5c7",
    ROOT / "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k23-2026-08-24/results_charge_ledger_through_k23_independent_audit.json": "a26e63c2e38f5c75135231bb578b5cb1d2c7ead7a32516eb7157c78d02249e3c",
    ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21/REPORT.md": "e42f3ea829a0c3c0cfe9b03aed64d1059ed512ff9f3d1f0fba2c14ed46707f41",
    ROOT / "computations/unaudited-codex-orbit0-global-residual-interface-audit-2026-08-23/REPORT.md": "7c5bdfb120532866b8558f9fdb5e334478e67b7e87cbb2316c8e8849fd543d3f",
    ROOT / "computations/unaudited-codex-orbit0-k16-literal-kcycle-certificate-2026-08-23/REPORT.md": "930b29308a8f7e6b6615c70824dfb41e830508a5affac60c70d7ba6e59f3c0e0",
    ROOT / "computations/unaudited-codex-current-route-archive-audit-2026-08-22/REPORT.md": "2c22b369256633328ebfbee4a073718c763b13aaeb343dddec5ddceab873e147",
    ROOT / "computations/unaudited-codex-orbit0-k24-relative-column-interface-gate-2026-08-24/REPORT.md": "947d8b63e17175879b02c5c8f5ba0098f08b9944c5f184cc9c43626d4c28d266",
    ROOT / "README.md": "b15e963db7a5151210367204bd20ebc38bf777a392b3c9086bb60b0ce91fd120",
    **EVIDENCE,
}


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise ValueError(detail)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rat(value: dict) -> Fraction:
    require(type(value) is dict and set(value) == {"numerator", "denominator", "text"}, "rational schema")
    answer = Fraction(int(value["numerator"]), int(value["denominator"]))
    require(value["text"] == str(answer), "rational text")
    return answer


def rendered(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator, "text": str(value)}


def group(gid: str, ids: list[str], charge, full, irreducible, source: Path) -> dict:
    charge = int(charge)
    full = int(full)
    irreducible = int(irreducible)
    require(full == irreducible, f"{gid}: full/irreducible occurrence mismatch")
    return {
        "group_id": gid,
        "ids": list(ids),
        "covered_ids": len(ids),
        "grouped_scalar_once": True,
        "full_charge_scaled_U": str(charge),
        "irreducible_charge_scaled_U": str(charge),
        "full_occurrences": full,
        "irreducible_occurrences": irreducible,
        "source_result": str(source.relative_to(ROOT)),
        "source_sha256": PINS[source],
    }


def extract_groups() -> list[dict]:
    direct = json.loads(DIRECT.read_text())
    require(direct["degree"] == 24 and int(direct["scale_U"]) == U and direct["source_interval"] == [0, 485], "direct constants")
    require(direct["covered_ids"] == 13 and direct["scalar_groups"] == 2, "direct scope")
    out = []
    for item in direct["groups"]:
        require(item["full_charge_scaled_U"] == item["irreducible_charge_scaled_U"], "direct charge equality")
        out.append(group(item["group_id"], item["ids"], item["full_charge_scaled_U"], item["full_occurrences"], item["irreducible_occurrences"], DIRECT))

    k14 = json.loads(K14.read_text())
    require(k14["status"] == "PASS_COMPLETE_D14_222_K24_CHARGE_ONLY" and k14["covered_lineage_ids"] == ["D14:222|R:3-3-4", "D14:222|R:4-2-4"], "K14 scope")
    for ident, gid in [("D14:222|R:3-3-4", "source_D14_R3_3_4"), ("D14:222|R:4-2-4", "source_D14_R4_2_4")]:
        item = k14["sinks"][ident]
        require(item["full_charge_scaled_U"] == item["irreducible_charge_scaled_U"], "K14 charge equality")
        out.append(group(gid, [ident], item["full_charge_scaled_U"], item["full_occurrences"], item["irreducible_occurrences"], K14))

    k15 = json.loads(K15.read_text())
    require(k15["status"] == "PASS_COMPLETE_STRICT_GROUPED_K15_SIX_ID_K24_CHARGE_FRAGMENT" and k15["covered_ids"] == 6 and k15["scalar_groups"] == 2, "K15 scope")
    for gid, item in k15["groups"].items():
        require(item["grouped_scalar_once"] is True, "K15 grouped-once")
        out.append(group(gid, item["ids"], item["charge_scaled_U"], item["full_occurrences"], item["irreducible_occurrences"], K15))

    for path, expected_status in [(R224, "PASS_COMPLETE_GROUPED_SIX_D16_R_2_2_4_K24_CHARGE_ONLY"), (R44, "PASS_COMPLETE_GROUPED_SIX_D16_K24_R44_CHARGE_ONLY")]:
        item = json.loads(path.read_text())
        require(item["status"] == expected_status and item["record_interval"] == [0, 24097095], f"{path.name}: complete scope")
        require(item["individual_id_charges"] is None and item["covered_ids"] == 6, f"{path.name}: grouped scope")
        require(item["full_charge_scaled_U"] == item["irreducible_charge_scaled_U"], f"{path.name}: charge equality")
        out.append(group(item["group_id"], item["ids"], item["full_charge_scaled_U"], item["full_occurrences"], item["irreducible_occurrences"], path))

    hc = json.loads(HC.read_text())
    require(hc["status"] == "PASS_COMPLETE_HIDDEN_COLLECTED_K18_K24_SINGLETON_CHARGE" and hc["input_interval"] == [0, 158439965], "hidden collected scope")
    require(hc["full_charge_scaled_U"] == hc["irreducible_charge_scaled_U"] and hc["full_equals_irreducible"] is True, "hidden collected equality")
    out.append(group("source_D14_R2_2_2_4", [hc["strict_id"]], hc["full_charge_scaled_U"], hc["full_occurrences"], hc["irreducible_occurrences"], HC))

    hd = json.loads(HD.read_text())
    require(hd["status"] == "PASS_COMPLETE_K24_HIDDEN_DECORATED_R244_CHARGE_ONLY" and hd["input_interval"] == [0, 101545723], "hidden decorated scope")
    sink = hd["sink"]
    require(sink["full_charge_scaled_U"] == sink["irreducible_charge_scaled_U"], "hidden decorated equality")
    out.append(group("source_D14_R2_4_4", hd["covered_lineage_ids"], sink["full_charge_scaled_U"], sink["full_occurrences"], sink["irreducible_occurrences"], HD))
    return out


def validate_groups(groups: list[dict], availability: dict, expected_values: dict[str, tuple[str, int]]) -> list[dict]:
    require(int(availability["scale_U"]) == U and availability["required_ids"] == 35 and availability["scalar_groups"] == 10, "availability constants")
    partition = availability["exact_group_partition"]
    expected = {item["group_id"]: item["ids"] for item in partition}
    require(len(expected) == 10 and sum(map(len, expected.values())) == 35, "availability partition")
    require(len(groups) == 10, "group count")
    observed = {}
    ids = []
    for item in groups:
        gid = item["group_id"]
        require(gid not in observed and gid in expected, "duplicate/extra group")
        require(item["grouped_scalar_once"] is True, "grouped-once guard")
        require(item["ids"] == expected[gid] and item["covered_ids"] == len(expected[gid]), "group ID partition")
        require(item["full_charge_scaled_U"] == item["irreducible_charge_scaled_U"], "group charge equality")
        require(item["full_occurrences"] == item["irreducible_occurrences"], "group occurrence equality")
        charge, occurrence = expected_values[gid]
        require(item["full_charge_scaled_U"] == charge and item["full_occurrences"] == occurrence, "group scalar/sign/occurrence pin")
        observed[gid] = item
        ids.extend(item["ids"])
    require(set(observed) == set(expected), "missing group")
    require(len(ids) == len(set(ids)) == 35 and set(ids) == {x["id"] for x in availability["lineages"]}, "exact 35-ID equality")
    require(all(x["terminal"] and x["child_anchor_mass"] == 0 and x["tail_terms_per_selected_pivot"] == 60 for x in availability["lineages"]), "universal terminality")
    return [observed[item["group_id"]] for item in partition]


def assemble() -> dict:
    for path, digest in PINS.items():
        require(path.is_file() and sha(path) == digest, f"source hash pin: {path}")
    for path in EVIDENCE:
        evidence = json.loads(path.read_text())
        require(str(evidence.get("status", "")).startswith("PASS"), f"evidence status: {path}")
    availability = json.loads(AVAIL.read_text())
    dual_path = ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/results_k16_cycle_partition_quotient.json"
    dual = json.loads(dual_path.read_text())
    require(dual["status"] == "EXACT_Q_SEPARATOR" and dual["all_abstract_four_path_cycle_profiles"] == dual["all_abstract_profile_pairings_zero"] == 1162, "77-functional source annihilation")
    require(dual["original_structured_aT_pairing"] == 0 and dual["original_structured_aT_terms"] == 1_157_625, "structured aT conservation premise")
    require("omitted K17--K24 tails must carry the opposite charge" in dual["conservation_scope_guard"], "77-functional scope guard")
    extracted = extract_groups()
    expected_values = {x["group_id"]: (x["full_charge_scaled_U"], x["full_occurrences"]) for x in extracted}
    groups = validate_groups(extracted, availability, expected_values)
    total_scaled = sum(int(x["full_charge_scaled_U"]) for x in groups)
    total = Fraction(total_scaled, U)
    through23 = json.loads(THROUGH23.read_text())
    require(through23["status"] == "PASS_COMPLETE_FILTERED_CHARGE_LEDGER_THROUGH_K23", "through-K23 status")
    cumulative23 = rat(through23["cumulative_K14_through_K23"])
    target = rat(through23["necessary_K24_aggregate_charge_under_conservation"])
    target_scaled = target * U
    require(target_scaled.denominator == 1, "target not integral at U")
    mismatch = total - target
    cumulative24 = cumulative23 + total
    require(mismatch == cumulative24, "conservation mismatch/cumulative identity")
    require(mismatch == Fraction(19_715_328), "unexpected conservation mismatch")
    source_pins = {str(path.relative_to(ROOT)): digest for path, digest in sorted(PINS.items(), key=lambda x: str(x[0]))}
    return {
        "status": "FAIL_FILTERED_CHARGE_CONSERVATION_NONZERO_CUMULATIVE",
        "assembly_status": "PASS_COMPLETE_K24_35_ID_10_GROUP_ASSEMBLY",
        "degree": 24,
        "scale_U": U,
        "covered_ids": sorted(x["id"] for x in availability["lineages"]),
        "required_ids": 35,
        "covered_id_count": 35,
        "missing_ids": [],
        "duplicate_ids": [],
        "extra_ids": [],
        "scalar_groups": 10,
        "grouped_scalars_counted_once": True,
        "groups": groups,
        "K24_charge_scaled_U": str(total_scaled),
        "K24_charge": rendered(total),
        "conservation_target_K24_scaled_U": str(target_scaled.numerator),
        "conservation_target_K24": rendered(target),
        "K24_target_mismatch_scaled_U": str(total_scaled - target_scaled.numerator),
        "K24_target_mismatch": rendered(mismatch),
        "cumulative_K14_through_K23": rendered(cumulative23),
        "cumulative_K14_through_K24": rendered(cumulative24),
        "conservation_zero": False,
        "terminality": availability["terminality_proof"],
        "conservation_theorem_audit": {
            "functional_annihilates_complete_balanced_source_columns": True,
            "original_structured_aT_functional_value": 0,
            "valid_complete_source_subtraction_must_preserve_total_zero": True,
            "observed_nonzero_cumulative": "19715328",
            "logical_effect": "reject the assembled deterministic filtered recurrence as a conservation-valid completion until a provenance, coverage, sign, or scalar defect is repaired",
            "genuine_filtered_acceptance_obstruction": True,
            "ideal_nonmembership_certificate": False,
            "reason_not_nonmembership": "the same functional pairs with the original structured a*T as zero, so it cannot separate a*T from the mixed source span; the mismatch makes the claimed source-reduction data inconsistent with conservation",
            "general_Krenn_Gu_conjecture_verdict": False,
        },
        "scope": {
            "resolved": "the present 35-ID charge assembly cannot be accepted as the complete frozen orbit-zero deterministic filtered reduction",
            "not_resolved": [
                "literal K24 residual membership or nonmembership in the relative terminal source span",
                "globalization from the orbit-zero anchors-one chart to the other 30 charts",
                "the general bicoloured n=8,d=3 Krenn-Gu conjecture",
                "the all-even-n conjecture",
            ],
            "next_local_certificate": "repair conservation first; a valid local nonmembership result would then require a complete relative solve/rank certificate for B=(L,T), equivalently R24 outside T(ker L), or another dual that annihilates source columns but pairs nonzero with a*T",
            "remaining_global_branch": "X5 plus all 560 triangle carriers blocked implies contradiction (or a same-source clean cap/descent), with a provenance-preserving globalization beyond the single orbit-zero chart",
        },
        "source_sha256": source_pins,
    }


def self_test() -> dict:
    availability = json.loads(AVAIL.read_text())
    baseline = extract_groups()
    expected = {x["group_id"]: (x["full_charge_scaled_U"], x["full_occurrences"]) for x in baseline}
    validate_groups(copy.deepcopy(baseline), availability, expected)
    rejected = []

    def reject(label, mutate):
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        try:
            validate_groups(candidate, availability, expected)
        except ValueError:
            rejected.append(label)
            return
        raise RuntimeError(f"hostile accepted: {label}")

    reject("omitted_group", lambda x: x.pop())
    reject("duplicate_group", lambda x: x.__setitem__(-1, copy.deepcopy(x[0])))
    reject("duplicate_lineage", lambda x: x[1]["ids"].__setitem__(0, x[0]["ids"][0]))
    reject("regrouped_lineage", lambda x: x[4]["ids"].reverse())
    reject("sign_flip", lambda x: x[0].__setitem__("full_charge_scaled_U", str(-int(x[0]["full_charge_scaled_U"]))))
    reject("wrong_U_semantics_via_group_multiply", lambda x: x[4].__setitem__("full_charge_scaled_U", str(3 * int(x[4]["full_charge_scaled_U"]))))
    wrong_availability = copy.deepcopy(availability)
    wrong_availability["scale_U"] = 1
    try:
        validate_groups(copy.deepcopy(baseline), wrong_availability, expected)
    except ValueError:
        rejected.append("wrong_U")
    else:
        raise RuntimeError("hostile accepted: wrong_U")
    require(len(rejected) == 7, "hostile count")
    return {"status": "PASS_K24_COMPLETE35_HOSTILE_SELFTEST", "rejected": rejected, "production_launched": False}


def write_atomic(path: Path, value: dict) -> None:
    temp = Path(str(path) + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temp.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        value = self_test()
        write_atomic(HERE / "results_k24_complete35_hostile_selftest.json", value)
    else:
        value = assemble()
        write_atomic(HERE / "results_k24_complete35_conservation.json", value)
    print(json.dumps(value, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

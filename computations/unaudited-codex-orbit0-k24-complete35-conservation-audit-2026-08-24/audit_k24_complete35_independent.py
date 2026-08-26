#!/usr/bin/env python3
"""Independent fail-closed audit of complete K24 grouped charge and scope."""
from __future__ import annotations

import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_k24_complete35_conservation.json"
BUILDER = HERE / "assemble_k24_complete35.py"
SELFTEST = HERE / "results_k24_complete35_hostile_selftest.json"
U = 400_591_699_200
TARGET = Fraction(829_424_811_081_283_712, 173_867_925)
CUM23 = -TARGET

EXPECTED = {
    "source_D14_R2_2_2_4": (["D14:222|R:2-2-2-4"], 645926683714155380736, 34216879080),
    "source_D14_R2_4_4": (["D14:222|R:2-4-4"], 97324923903254986752, 60681898800),
    "source_D14_R3_3_4": (["D14:222|R:3-3-4"], 104945403010833285120, 161268940800),
    "source_D14_R4_2_4": (["D14:222|R:4-2-4"], 64033288812772392960, 82522944000),
    "source_D15_R2_3_4": (["D15:223|R:2-3-4", "D15:232|R:2-3-4", "D15:322|R:2-3-4"], 232469436926413209600, 358355558400),
    "source_D15_R3_2_4": (["D15:223|R:3-2-4", "D15:232|R:3-2-4", "D15:322|R:3-2-4"], 220287135823033466880, 193212825600),
    "source_D16_R2_2_4": (["D16:224|R:2-2-4", "D16:233|R:2-2-4", "D16:242|R:2-2-4", "D16:323|R:2-2-4", "D16:332|R:2-2-4", "D16:422|R:2-2-4"], 107213275439239495680, 164736458640),
    "source_D16_R4_4": (["D16:224|R:4-4", "D16:233|R:4-4", "D16:242|R:4-4", "D16:323|R:4-4", "D16:332|R:4-4", "D16:422|R:4-4"], 150102648402491473920, 71208252000),
    "source_D17_R3_4": (["D17:234|R:3-4", "D17:243|R:3-4", "D17:324|R:3-4", "D17:333|R:3-4", "D17:342|R:3-4", "D17:423|R:3-4", "D17:432|R:3-4"], 233614955677836902400, 50538086400),
    "source_D18_R2_4": (["D18:244|R:2-4", "D18:334|R:2-4", "D18:343|R:2-4", "D18:424|R:2-4", "D18:433|R:2-4", "D18:442|R:2-4"], 62974809765052416000, 13856256000),
}
ORDER = list(EXPECTED)
RESULT_SHA = "7a33791664ac3b92dc6489c1a8160364a8fd3347508ff7cf760803e0b7372df8"
BUILDER_SHA = "7067bf36ce88f09402133519fe83f601d0e4f6b4d47bb31d09567fb311df194e"
SELFTEST_SHA = "9cb25e351584d64ee15970348d6d2bc45f352bb1aaae6c64c1b958ec525e3c7d"


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


def validate(value: dict) -> dict:
    require(value["status"] == "FAIL_FILTERED_CHARGE_CONSERVATION_NONZERO_CUMULATIVE", "status")
    require(value["assembly_status"] == "PASS_COMPLETE_K24_35_ID_10_GROUP_ASSEMBLY", "assembly status")
    require(value["degree"] == 24 and value["scale_U"] == U, "degree/U")
    require(value["required_ids"] == value["covered_id_count"] == 35 and value["scalar_groups"] == 10, "coverage constants")
    require(value["missing_ids"] == value["duplicate_ids"] == value["extra_ids"] == [], "partition gaps")
    require(value["grouped_scalars_counted_once"] is True, "grouped-once declaration")
    groups = value["groups"]
    require(len(groups) == 10 and [x["group_id"] for x in groups] == ORDER, "group order/set")
    all_ids = []
    total_scaled = 0
    for item in groups:
        gid = item["group_id"]
        ids, charge, occurrences = EXPECTED[gid]
        require(item["ids"] == ids and item["covered_ids"] == len(ids), f"{gid}: ID set")
        require(item["grouped_scalar_once"] is True, f"{gid}: grouped once")
        require(int(item["full_charge_scaled_U"]) == int(item["irreducible_charge_scaled_U"]) == charge, f"{gid}: charge/sign")
        require(item["full_occurrences"] == item["irreducible_occurrences"] == occurrences, f"{gid}: occurrences")
        source = ROOT / item["source_result"]
        require(source.is_file() and sha(source) == item["source_sha256"], f"{gid}: source pin")
        total_scaled += charge
        all_ids.extend(ids)
    require(len(all_ids) == len(set(all_ids)) == 35 and sorted(all_ids) == value["covered_ids"], "exact 35 IDs")
    require(total_scaled == 1_918_892_561_475_083_010_048 == int(value["K24_charge_scaled_U"]), "K24 scaled total")
    total = Fraction(total_scaled, U)
    require(rat(value["K24_charge"]) == total == Fraction(832_852_674_251_338_112, 173_867_925), "K24 rational total")
    require(rat(value["conservation_target_K24"]) == TARGET and int(value["conservation_target_K24_scaled_U"]) == TARGET * U, "K24 target")
    require(rat(value["cumulative_K14_through_K23"]) == CUM23, "through-K23 cumulative")
    mismatch = total - TARGET
    require(mismatch == Fraction(19_715_328), "mismatch value")
    require(rat(value["K24_target_mismatch"]) == rat(value["cumulative_K14_through_K24"]) == mismatch, "mismatch/cumulative")
    require(int(value["K24_target_mismatch_scaled_U"]) == mismatch * U == 7_897_796_743_805_337_600, "scaled mismatch")
    require(value["conservation_zero"] is False, "nonzero flag")
    term = value["terminality"]
    require(term["formula"] == "4 - 4 + 0 = 0" and term["child_anchor_mass"] == 0 and "all 35 K24 outputs are terminal" in term["conclusion"], "terminality")
    theorem = value["conservation_theorem_audit"]
    require(theorem["functional_annihilates_complete_balanced_source_columns"] is True and theorem["original_structured_aT_functional_value"] == 0, "conservation premises")
    require(theorem["genuine_filtered_acceptance_obstruction"] is True and theorem["ideal_nonmembership_certificate"] is False and theorem["general_Krenn_Gu_conjecture_verdict"] is False, "scope classification")
    require("cannot separate a*T" in theorem["reason_not_nonmembership"], "nonmembership guard")
    scope = value["scope"]
    require("cannot be accepted" in scope["resolved"] and any("general bicoloured n=8,d=3 Krenn-Gu conjecture" in item for item in scope["not_resolved"]), "conjecture boundary")
    require("R24 outside T(ker L)" in scope["next_local_certificate"] and "560 triangle carriers" in scope["remaining_global_branch"], "remaining certificates")
    pins = value["source_sha256"]
    for name, digest in pins.items():
        path = ROOT / name
        require(path.is_file() and sha(path) == digest, f"global source pin {name}")
    dual = json.loads((ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/results_k16_cycle_partition_quotient.json").read_text())
    require(dual["all_abstract_profile_pairings_zero"] == 1162 and dual["original_structured_aT_pairing"] == 0, "direct dual theorem")
    readme = (ROOT / "README.md").read_text()
    require("general bicoloured" in readme and "`n = 8, d = 3`" in readme and "remains open" in readme, "repository conjecture status")
    route = (ROOT / "computations/unaudited-codex-current-route-archive-audit-2026-08-22/REPORT.md").read_text()
    require("X5 + all 560 triangle carriers blocked  ==>  contradiction" in route, "global missing arrow")
    relative = (ROOT / "computations/unaudited-codex-orbit0-k24-relative-column-interface-gate-2026-08-24/REPORT.md").read_text()
    require("A24_rel = T restricted to ker(L)" in relative and "B*x=(0,0,0,R24)" in relative, "relative certificate definition")
    return {"total_scaled_U": total_scaled, "total": str(total), "mismatch": str(mismatch), "ids": len(all_ids), "groups": len(groups)}


def hostile(baseline: dict) -> list[str]:
    rejected = []

    def reject(label, mutate):
        x = copy.deepcopy(baseline)
        mutate(x)
        try:
            validate(x)
        except (ValueError, KeyError, TypeError):
            rejected.append(label)
            return
        raise RuntimeError(f"hostile accepted: {label}")

    reject("omission", lambda x: x["groups"].pop())
    reject("duplicate_group", lambda x: x["groups"].__setitem__(-1, copy.deepcopy(x["groups"][0])))
    reject("duplicate_lineage", lambda x: x["groups"][1]["ids"].__setitem__(0, x["groups"][0]["ids"][0]))
    reject("regroup", lambda x: x["groups"][4]["ids"].reverse())
    reject("sign", lambda x: x["groups"][0].__setitem__("full_charge_scaled_U", str(-int(x["groups"][0]["full_charge_scaled_U"]))))
    reject("U", lambda x: x.__setitem__("scale_U", 1))
    reject("group_scalar_multiply", lambda x: x["groups"][4].__setitem__("full_charge_scaled_U", str(3 * int(x["groups"][4]["full_charge_scaled_U"]))))
    reject("wrong_target_sign", lambda x: x["conservation_target_K24"].__setitem__("numerator", -x["conservation_target_K24"]["numerator"]))
    reject("promoted_to_nonmembership", lambda x: x["conservation_theorem_audit"].__setitem__("ideal_nonmembership_certificate", True))
    reject("promoted_to_conjecture", lambda x: x["conservation_theorem_audit"].__setitem__("general_Krenn_Gu_conjecture_verdict", True))
    return rejected


def main() -> None:
    require(sha(RESULT) == RESULT_SHA and sha(BUILDER) == BUILDER_SHA and sha(SELFTEST) == SELFTEST_SHA, "local package pins")
    selftest = json.loads(SELFTEST.read_text())
    require(selftest["status"] == "PASS_K24_COMPLETE35_HOSTILE_SELFTEST" and len(selftest["rejected"]) == 7, "builder selftest")
    baseline = json.loads(RESULT.read_text())
    summary = validate(baseline)
    rejected = hostile(baseline)
    require(len(rejected) == 10, "hostile rejection count")
    output = {
        "status": "PASS_INDEPENDENT_K24_COMPLETE35_CONSERVATION_AND_SCOPE_AUDIT",
        "summary": summary,
        "result_sha256": RESULT_SHA,
        "builder_sha256": BUILDER_SHA,
        "builder_selftest_sha256": SELFTEST_SHA,
        "hostile_rejected": rejected,
        "conservation_mismatch_is_recurrence_acceptance_obstruction_not_nonmembership": True,
        "general_Krenn_Gu_conjecture_remains_open": True,
        "production_launched": False,
    }
    path = HERE / "results_k24_complete35_independent_audit.json"
    temp = Path(str(path) + ".tmp")
    temp.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    temp.replace(path)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

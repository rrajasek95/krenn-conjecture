#!/usr/bin/env python3
"""Fail-closed independent exact-set referee for the current K23 44/59 ledger."""
import copy
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ASSEMBLER = ROOT / "computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/assemble_k23_59_exact.py"
MANIFEST = HERE / "k23_manifest_current_44_of_59.json"
RESULT = HERE / "results_k23_current_44_of_59_partial.json"
PINS = {
    ASSEMBLER: "b189ddf195af4e5e896aee495bf7adbc074af0108a4f026ae852fbbabaacbaaf",
    ROOT / "computations/unaudited-codex-orbit0-k23-direct23-source-fold-2026-08-24/k23_direct23_fragment_manifest.json": "57cdec4a6445c52bd7d35e1a97d37ef5f476f85e6c1de5b598d8c354b5db2d3b",
    ROOT / "computations/unaudited-codex-orbit0-k23-direct-k16-18-charge-2026-08-24/k23_direct_k16_18_fragment_manifest.json": "9c37703f0c4e5c32f8993caf486eca18b8ed9d2bf46dab8a0192abc5af1397a1",
    ROOT / "computations/unaudited-codex-orbit0-k23-hidden-collected-k18-2026-08-24/k23_hidden_collected_singleton_fragment_manifest.json": "ac797c5f1e529de2fd2dc12d5a761fd55d6216bf3213da45f7701c8dfe9cb06d",
    HERE / "k23_hidden_decorated_pair_fragment_manifest.json": "6d9f9253830d3d7f2e92f985d65859cc720cfbe3e0411946d8af316c2beba787",
}
EXPECTED_MISSING = [
    "D14:222|R:3-2-4", "D14:222|R:3-3-3", "D14:222|R:4-2-3",
    "D15:223|R:2-2-4", "D15:223|R:2-3-3", "D15:223|R:3-2-3", "D15:223|R:4-4",
    "D15:232|R:2-2-4", "D15:232|R:2-3-3", "D15:232|R:3-2-3", "D15:232|R:4-4",
    "D15:322|R:2-2-4", "D15:322|R:2-3-3", "D15:322|R:3-2-3", "D15:322|R:4-4",
]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_module():
    spec = importlib.util.spec_from_file_location("strict_k23", ASSEMBLER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reject(module, manifest, needle):
    try:
        module.assemble(manifest, allow_partial=True)
    except ValueError as error:
        need(needle in str(error), f"hostile reason {needle}: {error}")
    else:
        need(False, f"hostile mutation accepted: {needle}")


def main():
    for path, digest in PINS.items():
        need(path.is_file() and sha(path) == digest, f"pin {path}")
    manifest = json.loads(MANIFEST.read_text())
    result = json.loads(RESULT.read_text())
    module = exact_module()
    required = {identifier for ids in module.EXPECTED_GROUPS.values() for identifier in ids}
    need(len(required) == 59, "frozen required set")
    groups = manifest["groups"]
    covered = [identifier for group in groups for identifier in group["ids"]]
    need(len(groups) == 10 and len(covered) == len(set(covered)) == 44, "10-group/44-ID uniqueness")
    need(set(covered) <= required and required - set(covered) == set(EXPECTED_MISSING), "exact 44+15 set partition")
    need([identifier for identifier in result["covered_ids"]] == covered, "covered order")
    need(result["missing_paths"] == EXPECTED_MISSING, "exact ordered gap")
    for group in groups:
        need(group["group_id"] in module.EXPECTED_GROUPS and group["ids"] == module.EXPECTED_GROUPS[group["group_id"]], "schedule-exact group")
        evidence = ROOT / group["evidence_path"]
        need(evidence.is_file() and sha(evidence) == group["evidence_sha256"], "group evidence")
        need(group["full_scaled_U"] == group["irreducible_scaled_U"], "group terminality")
        need(Fraction(int(group["full_scaled_U"]), 400_591_699_200) == Fraction(group["full"]) == Fraction(group["irreducible"]), "group exact rational")
    need(len(manifest["fragment_inputs"]) == 4, "four disjoint sealed family inputs")
    for item in manifest["fragment_inputs"]:
        path = ROOT / item["path"]
        need(path in PINS and sha(path) == item["sha256"] == PINS[path], "fragment hash")
    replay = module.assemble(manifest, allow_partial=True)
    for key in ("status", "complete_K23_claim", "covered_ids", "covered_paths", "scalar_groups", "missing_paths", "missing_scalar_groups", "duplicate_paths", "extra_paths", "full_scaled_U", "irreducible_scaled_U", "full", "irreducible", "full_equals_irreducible", "manifest_logical_sha256"):
        need(result[key] == replay[key], f"exact replay {key}")
    need((result["status"], result["complete_K23_claim"], result["covered_paths"], result["scalar_groups"]) == ("REJECT_INCOMPLETE_K23_59_ID_GATE", False, 44, 10), "strict incomplete status")
    need(len(result["missing_paths"]) == 15 and len(result["missing_scalar_groups"]) == 7, "strict gaps")
    need(result["duplicate_paths"] == result["extra_paths"] == [], "duplicates/extras")
    once = sum(int(group["full_scaled_U"]) for group in groups)
    need(once == -4_634_943_212_188_792_553_472, "group-scalar-once subtotal")
    need(int(result["full_scaled_U"]) == int(result["irreducible_scaled_U"]) == once, "partial subtotal")
    need(Fraction(result["full"]["text"]) == Fraction(-2_011_694_102_512_496_768, 173_867_925), "partial exact rational")
    try:
        module.assemble(manifest, allow_partial=False)
    except ValueError as error:
        need("missing 15 K23 IDs" in str(error), "complete-gate rejection reason")
    else:
        need(False, "44-ID ledger accepted as complete")
    hostile = copy.deepcopy(manifest)
    hostile["groups"].append(copy.deepcopy(hostile["groups"][-1]))
    reject(module, hostile, "duplicate_group")
    hostile = copy.deepcopy(manifest)
    hostile["groups"][8]["ids"] = hostile["groups"][7]["ids"]
    reject(module, hostile, "partition/order")
    hostile = copy.deepcopy(manifest)
    hostile["groups"][8]["full_scaled_U"] = "0"
    reject(module, hostile, "scaled/rational")
    print(json.dumps({
        "status": "PASS_STRICT_K23_CURRENT_44_OF_59_PARTIAL_REFEREE",
        "covered_paths": 44,
        "missing_paths": 15,
        "scalar_groups": 10,
        "missing_scalar_groups": 7,
        "partial_scaled_U": str(once),
        "partial": result["full"]["text"],
        "exact_set_equality": True,
        "duplicates": [],
        "extras": [],
        "complete_K23_claim": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()

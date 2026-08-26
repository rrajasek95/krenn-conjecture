#!/usr/bin/env python3
"""Fail-closed audit of the current direct23 + direct-K16 41/59 ledger."""
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ASSEMBLER = ROOT / "computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/assemble_k23_59_exact.py"
MANIFEST = HERE / "k23_manifest_current_41_of_59.json"
RESULT = HERE / "results_k23_current_41_of_59_partial.json"
EXPECTED_GROUPS = {
    "source_D16_R2_2_3", "source_D16_R3_4", "source_D16_R4_3",
    "source_D17_R2_4", "source_D17_R3_3", "source_D18_R2_3", "source_D19_R4",
}
EXPECTED_SCALED = -2_230_156_832_035_793_633_280


def need(condition, message):
    if not condition:
        raise SystemExit(f"REJECT: {message}")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_exact():
    spec = importlib.util.spec_from_file_location("k23_exact", ASSEMBLER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    need(sha(ASSEMBLER) == "b189ddf195af4e5e896aee495bf7adbc074af0108a4f026ae852fbbabaacbaaf", "assembler hash")
    manifest = json.loads(MANIFEST.read_text())
    result = json.loads(RESULT.read_text())
    exact = load_exact()
    groups = manifest.get("groups", [])
    need(len(groups) == 7, "scalar group count")
    need({entry.get("group_id") for entry in groups} == EXPECTED_GROUPS, "group scope")
    covered = [item for entry in groups for item in entry.get("ids", [])]
    need(len(covered) == len(set(covered)) == 41, "exact 41-ID coverage")
    for entry in groups:
        need(entry["ids"] == exact.EXPECTED_GROUPS[entry["group_id"]], f"schedule grouping {entry['group_id']}")
        path = ROOT / entry["evidence_path"]
        need(path.is_file() and sha(path) == entry["evidence_sha256"], f"evidence {entry['group_id']}")
    replay = exact.assemble(manifest, allow_partial=True)
    for key in (
        "status", "complete_K23_claim", "degree", "scale_U", "required_paths",
        "covered_paths", "scalar_groups", "required_scalar_groups", "missing_scalar_groups",
        "missing_paths", "duplicate_paths", "extra_paths", "full_scaled_U",
        "irreducible_scaled_U", "full", "irreducible", "covered_ids",
        "full_equals_irreducible", "dag_logical_sha256", "manifest_logical_sha256",
    ):
        need(result.get(key) == replay.get(key), f"result replay {key}")
    need((result["status"], result["complete_K23_claim"], result["covered_paths"], len(result["missing_paths"])) == ("REJECT_INCOMPLETE_K23_59_ID_GATE", False, 41, 18), "incomplete gate")
    need(int(result["full_scaled_U"]) == int(result["irreducible_scaled_U"]) == EXPECTED_SCALED, "partial subtotal")
    need(result["full"]["text"] == result["irreducible"]["text"] == "-6430066189952/1155", "partial rational")
    try:
        exact.assemble(manifest, allow_partial=False)
    except ValueError as error:
        need("missing 18 K23 IDs" in str(error), "strict complete rejection reason")
    else:
        need(False, "incomplete manifest accepted as complete")
    print(json.dumps({"status": "PASS_STRICT_K23_CURRENT_41_OF_59_PARTIAL", "complete_K23_claim": False, "covered_paths": 41, "missing_paths": 18, "scalar_groups": 7, "partial_scaled_U": str(EXPECTED_SCALED), "partial": "-6430066189952/1155", "future_fragment_ingestion": "build_k23_current_partial.py --fragment MANIFEST"}, sort_keys=True))


if __name__ == "__main__":
    main()

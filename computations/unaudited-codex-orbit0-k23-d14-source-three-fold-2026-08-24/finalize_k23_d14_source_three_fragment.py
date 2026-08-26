#!/usr/bin/env python3
"""Create the strict three-singleton K23 fragment after merge and literal referee pass."""

import argparse
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTRACT = ROOT / "computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/k23_expected_scalar_groups.json"
CONTRACT_SHA = "6d59f1a24771e3a5e595ab79d8d0309881edea085da62c34b8e70cf93757c9ab"
U = 400_591_699_200
SPECS = [
    ("source_D14_R3_2_4", "D14:222|R:3-2-4", 60),
    ("source_D14_R3_3_3", "D14:222|R:3-3-3", 32),
    ("source_D14_R4_2_3", "D14:222|R:4-2-3", 32),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--merged", type=Path, default=HERE / "results_k23_d14_source_three.json")
    parser.add_argument("--referee", type=Path, default=HERE / "results_k23_d14_source_three_literal_referee.json")
    parser.add_argument("--output", type=Path, default=HERE / "k23_d14_source_three_fragment_manifest.json")
    parser.add_argument("--audit-output", type=Path, default=HERE / "results_k23_d14_source_three_fragment_audit.json")
    args = parser.parse_args()
    assert sha(CONTRACT) == CONTRACT_SHA
    contract = json.loads(CONTRACT.read_text())
    expected = {entry["group_id"]: entry["ids"] for entry in contract["groups"]}
    merged = json.loads(args.merged.read_text())
    referee = json.loads(args.referee.read_text())
    ids = [lineage for _, lineage, _ in SPECS]
    assert merged["status"] == "PASS_COMPLETE_D14_222_K23_SOURCE_THREE_CHARGE"
    assert merged["covered_lineage_ids"] == ids and int(merged["scale_U"]) == U
    assert merged["source_shards"] == [[0, 243], [243, 485]]
    assert (merged["R8_records_consumed"], merged["R8_records_declared"], merged["source_heads"]) == (485, 485, 838_080)
    assert merged["all_realized_cached_K23_responses_terminal"] is True
    assert merged["literal_sample_guard"]["records"] == 771
    assert merged["literal_sample_guard"]["records_per_sink"] == [257, 257, 257]
    assert referee["status"] == "PASS_INDEPENDENT_K23_D14_SOURCE_THREE_LITERAL_REFEREE"
    assert referee["samples"] == 771 and referee["samples_per_sink"] == [257, 257, 257]
    assert referee["complete_257_bins_per_sink"] is True
    for field in (
        "source_heads_reconstructed_from_frozen_R8", "all_literal_path_counts_and_charges_equal",
        "all_U_divisions_exact", "all_terminal_K23_children_nonpivotable",
        "all_abstract_literal_cycle_keys_equal",
    ):
        assert referee[field] is True

    evidence_path = str(args.merged.resolve().relative_to(ROOT.resolve()))
    evidence_sha = sha(args.merged)
    groups = []
    for group_id, lineage, terminal_tails in SPECS:
        assert expected[group_id] == [lineage]
        sink = merged["sinks"][lineage]
        assert sink["K23_terminal_occurrences"] == terminal_tails * sink["selected_p3_uses"]
        assert sink["full_occurrences"] == sink["irreducible_occurrences"] == sink["K23_terminal_occurrences"]
        assert sink["full_charge_scaled_U"] == sink["irreducible_charge_scaled_U"]
        scaled = int(sink["full_charge_scaled_U"])
        exact = str(Fraction(scaled, U))
        groups.append({
            "group_id": group_id,
            "ids": [lineage],
            "full_scaled_U": str(scaled),
            "irreducible_scaled_U": str(scaled),
            "full": exact,
            "irreducible": exact,
            "evidence_path": evidence_path,
            "evidence_sha256": evidence_sha,
        })
    manifest = {
        "degree": 23,
        "scale_U": U,
        "groups": groups,
        "scope": "strict three-singleton D14 K23 source-three fragment; each scalar counted once; no complete K23 claim",
    }
    temporary = Path(str(args.output) + ".tmp")
    temporary.write_text(json.dumps(manifest, indent=2) + "\n")
    os.replace(temporary, args.output)
    audit = {
        "status": "PASS_K23_D14_SOURCE_THREE_STRICT_3_ID_FRAGMENT",
        "covered_ids": 3,
        "scalar_groups": 3,
        "group_scalar_once": True,
        "full_equals_irreducible": True,
        "merged_sha256": evidence_sha,
        "literal_referee_sha256": sha(args.referee),
        "fragment_sha256": sha(args.output),
        "contract_sha256": sha(CONTRACT),
        "scope": "fragment finalization only; no complete K23, K24, membership, or conjecture claim",
    }
    temporary = Path(str(args.audit_output) + ".tmp")
    temporary.write_text(json.dumps(audit, indent=2) + "\n")
    os.replace(temporary, args.audit_output)
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()

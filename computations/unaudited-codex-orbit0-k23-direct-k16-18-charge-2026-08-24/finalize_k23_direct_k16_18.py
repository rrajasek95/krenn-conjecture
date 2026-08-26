#!/usr/bin/env python3
"""Fail-closed fragment assembler for the three grouped direct-K16 K23 sinks."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
U = 400_591_699_200
BASE = ("224", "233", "242", "323", "332", "422")
SPECS = (
    ("source_D16_R3_4", "3-4", "results_k23_direct_k16_34.json",
     "PASS_COMPLETE_MERGED_GROUPED_SIX_D16_R_3_4_K23", 2_041_782_688, 122_506_961_280),
    ("source_D16_R4_3", "4-3", "results_k23_direct_k16_43.json",
     "PASS_COMPLETE_GROUPED_SIX_D16_K23_TWO_RESPONSE", 1_186_804_200, 37_977_734_400),
    ("source_D16_R2_2_3", "2-2-3", "results_k23_direct_k16_223.json",
     "PASS_COMPLETE_GROUPED_SIX_D16_R_2_2_3_K23", 2_745_607_644, 87_859_444_608),
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path, text):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(text)
    tmp.replace(path)


def main():
    assert sha(ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin") == "93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3"
    groups = []
    manifest_groups = []
    all_ids = []
    total = 0
    for group_id, recurrence, filename, status, terminal_uses, occurrences in SPECS:
        path = HERE / filename
        doc = json.loads(path.read_text())
        expected_ids = [f"D16:{packet}|R:{recurrence}" for packet in BASE]
        assert (doc["status"], doc["group_id"], doc["degree"], int(doc["scale_U"])) == (status, group_id, 23, U)
        assert doc["ids"] == expected_ids and doc["covered_ids"] == 6
        assert doc["individual_id_charges"] is None
        assert (doc["source_rows"], int(doc["signed_source_coefficient"]), int(doc["l1_source_coefficient"])) == (24_097_095, 1_464_625_152, 13_978_655_136)
        assert (doc["pivotable_K16_rows"], doc["p1_uses"]) == (24_003_767, 129_939_187)
        uses = doc.get("p3_uses", doc["p2_uses"])
        assert (uses, doc["K23_terminal_occurrences"]) == (terminal_uses, occurrences)
        assert doc["full_occurrences"] == doc["irreducible_occurrences"] == occurrences
        scaled = int(doc["full_charge_scaled_U"])
        assert scaled == int(doc["irreducible_charge_scaled_U"])
        sample_path = Path(doc["sample_ledger"])
        lines = sample_path.read_text().splitlines()
        assert len(lines) == 258
        assert [int(line.split("\t")[0]) for line in lines[1:]] == list(range(257))
        terminal_column = 14 if group_id == "source_D16_R2_2_3" else 12
        assert all(int(line.split("\t")[terminal_column]) != 0 for line in lines[1:])
        charge = Fraction(scaled, U)
        evidence_path = path.relative_to(ROOT).as_posix()
        evidence_sha = sha(path)
        groups.append({
            "group_id": group_id, "ids": expected_ids,
            "p1_uses": 129_939_187,
            **({"p2_uses": int(doc["p2_uses"]), "p3_uses": int(doc["p3_uses"])} if "p3_uses" in doc else {"p2_uses": int(doc["p2_uses"])}),
            "K23_terminal_occurrences": occurrences,
            "full_charge_scaled_U": str(scaled),
            "irreducible_charge_scaled_U": str(scaled),
            "charge": str(charge), "evidence_sha256": evidence_sha,
        })
        manifest_groups.append({
            "ids": expected_ids, "full_scaled_U": str(scaled),
            "irreducible_scaled_U": str(scaled), "full": str(charge),
            "irreducible": str(charge), "evidence_path": evidence_path,
            "evidence_sha256": evidence_sha,
        })
        all_ids.extend(expected_ids)
        total += scaled
    assert len(all_ids) == len(set(all_ids)) == 18
    subtotal = Fraction(total, U)
    result = {
        "status": "PASS_COMPLETE_GROUPED_18_ID_DIRECT_K16_K23_FRAGMENT",
        "degree": 23, "scale_U": str(U), "covered_ids": 18,
        "scalar_groups": 3, "groups": groups,
        "full_charge_scaled_U": str(total),
        "irreducible_charge_scaled_U": str(total),
        "full": str(subtotal), "irreducible": str(subtotal),
        "literal_samples": 771,
        "packet_grouping_guard": "the retained direct-K16 checkpoint has canonical rows and collected coefficients but no packet labels; each recurrence sink is therefore exactly one grouped six-ID scalar",
        "scope": "strict grouped 18-ID K23 fragment only; no individual packet scalar, other K23/K24 ID, row output, membership, or conjecture claim",
    }
    manifest = {
        "degree": 23, "scale_U": U, "groups": manifest_groups,
        "scope": "three grouped scalars counted once, covering exactly the 18 frozen direct-K16 K23 IDs",
    }
    atomic(HERE / "results_k23_direct_k16_18.json", json.dumps(result, indent=2, sort_keys=True) + "\n")
    atomic(HERE / "k23_direct_k16_18_fragment_manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "covered_ids": 18, "scalar_groups": 3, "subtotal_scaled_U": str(total), "subtotal": str(subtotal)}, sort_keys=True))


if __name__ == "__main__":
    main()

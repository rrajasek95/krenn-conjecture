#!/usr/bin/env python3
"""Fail-closed exact package audit, including hostile manifest mutations."""
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
U = 400_591_699_200
BASE = ("224", "233", "242", "323", "332", "422")
PINS = {
    "results_k23_direct_k16_34.json": "371463f3feaf52183238af0d54b0c7f61773761e509bd0c075442225b1ad08ec",
    "results_k23_direct_k16_34.json.samples.tsv": "afe6074e2fdbb93ddce17bf56d208b37fac229fc65d24978324263547c508312",
    "results_k23_direct_k16_43.json": "d75a8afd74e6fa2990aebec237d01319ee365fc202786bd0d24ee1639205a4db",
    "results_k23_direct_k16_43.json.samples.tsv": "1c220eb97f7cc36138d4ff69feec26fb9a50d710802613fd423b3c060f861eed",
    "results_k23_direct_k16_223.json": "ac15faad3d2d249ee57787ac28d2d7f48d6f6dbdb388b4d7c95279e2067eb6da",
    "results_k23_direct_k16_223.json.samples.tsv": "02ab395f75526f370a846ce92bc5f55f0cd3b4b443f5aaba21a9d587e8049ef2",
    "results_k23_direct_k16_18.json": "ba05ebd7bdd28528b6ff6ed78df60b776e43a7b0fcc19597d8023bad5ca403f0",
    "k23_direct_k16_18_fragment_manifest.json": "9c37703f0c4e5c32f8993caf486eca18b8ed9d2bf46dab8a0192abc5af1397a1",
    "results_k23_direct_k16_18_literal_referee.json": "56ed7ef4b831b22c43fc5218646114490dcca14a34c1c5d162afcf2401bfcd98",
    "results_k23_direct_k16_34_shard0_reconciliation.json": "63ed09f5334b5ea406bf8f7dcdbf59815674a91d94e4df505a2fee8f2ba6c746",
}
SPECS = (
    ("source_D16_R3_4", "3-4", "results_k23_direct_k16_34.json", 2_041_782_688, 122_506_961_280, -513_238_474_044_726_312_960),
    ("source_D16_R4_3", "4-3", "results_k23_direct_k16_43.json", 1_186_804_200, 37_977_734_400, -198_502_467_495_831_797_760),
    ("source_D16_R2_2_3", "2-2-3", "results_k23_direct_k16_223.json", 2_745_607_644, 87_859_444_608, -576_585_529_193_622_896_640),
)
TOTAL = -1_288_326_470_734_181_007_360


class Reject(Exception):
    pass


def need(condition, message):
    if not condition:
        raise Reject(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_ids(recurrence):
    return [f"D16:{packet}|R:{recurrence}" for packet in BASE]


def audit(fragment, manifest):
    need((fragment.get("status"), fragment.get("degree"), int(fragment.get("scale_U", 0))) == ("PASS_COMPLETE_GROUPED_18_ID_DIRECT_K16_K23_FRAGMENT", 23, U), "fragment header")
    need((fragment.get("covered_ids"), fragment.get("scalar_groups"), fragment.get("literal_samples")) == (18, 3, 771), "fragment cardinalities")
    need(len(fragment.get("groups", [])) == len(manifest.get("groups", [])) == 3, "group count")
    need((manifest.get("degree"), int(manifest.get("scale_U", 0))) == (23, U), "manifest header")
    seen = []
    total = 0
    for index, (group_id, recurrence, filename, terminal_uses, occurrences, scaled) in enumerate(SPECS):
        ids = expected_ids(recurrence)
        group = fragment["groups"][index]
        entry = manifest["groups"][index]
        doc_path = HERE / filename
        doc = json.loads(doc_path.read_text())
        need(group.get("group_id") == group_id and group.get("ids") == ids, f"fragment group {group_id}")
        need(entry.get("ids") == ids, f"manifest ids {group_id}")
        need(doc.get("group_id") == group_id and doc.get("ids") == ids, f"evidence ids {group_id}")
        need((doc.get("source_rows"), int(doc.get("signed_source_coefficient", 0)), int(doc.get("l1_source_coefficient", 0))) == (24_097_095, 1_464_625_152, 13_978_655_136), f"source pins {group_id}")
        need((doc.get("pivotable_K16_rows"), doc.get("p1_uses")) == (24_003_767, 129_939_187), f"pivot pins {group_id}")
        uses = doc.get("p3_uses", doc.get("p2_uses"))
        need((uses, doc.get("K23_terminal_occurrences")) == (terminal_uses, occurrences), f"terminal counts {group_id}")
        need(doc.get("full_occurrences") == doc.get("irreducible_occurrences") == occurrences, f"terminality {group_id}")
        need(int(doc.get("full_charge_scaled_U", 0)) == int(doc.get("irreducible_charge_scaled_U", 1)) == scaled, f"scaled charge {group_id}")
        charge = str(Fraction(scaled, U))
        need((group.get("full_charge_scaled_U"), group.get("irreducible_charge_scaled_U"), group.get("charge")) == (str(scaled), str(scaled), charge), f"fragment scalar {group_id}")
        need((entry.get("full_scaled_U"), entry.get("irreducible_scaled_U"), entry.get("full"), entry.get("irreducible")) == (str(scaled), str(scaled), charge, charge), f"manifest scalar {group_id}")
        evidence_path = doc_path.relative_to(ROOT).as_posix()
        evidence_sha = sha(doc_path)
        need((entry.get("evidence_path"), entry.get("evidence_sha256"), group.get("evidence_sha256")) == (evidence_path, evidence_sha, evidence_sha), f"evidence pin {group_id}")
        sample_path = Path(doc["sample_ledger"])
        if not sample_path.is_absolute():
            sample_path = ROOT / sample_path
        lines = sample_path.read_text().splitlines()
        need(len(lines) == 258, f"sample count {group_id}")
        need([int(line.split("\t")[0]) for line in lines[1:]] == list(range(257)), f"sample ordinals {group_id}")
        terminal_column = 14 if group_id == "source_D16_R2_2_3" else 12
        need(all(int(line.split("\t")[terminal_column]) != 0 for line in lines[1:]), f"sample nonzero {group_id}")
        seen.extend(ids)
        total += scaled
    need(len(seen) == len(set(seen)) == 18, "duplicate/missing coverage")
    need(set(seen) == {item for _, recurrence, *_ in SPECS for item in expected_ids(recurrence)}, "extra coverage")
    need(total == TOTAL, "subtotal scaled")
    need((fragment.get("full_charge_scaled_U"), fragment.get("irreducible_charge_scaled_U"), fragment.get("full"), fragment.get("irreducible")) == (str(TOTAL), str(TOTAL), str(Fraction(TOTAL, U)), str(Fraction(TOTAL, U))), "fragment subtotal")
    referee = json.loads((HERE / "results_k23_direct_k16_18_literal_referee.json").read_text())
    need(referee == {"status": "PASS_INDEPENDENT_K23_DIRECT_K16_18_LITERAL_REPLAY", "R3_4_samples": 257, "R4_3_samples": 257, "R2_2_3_samples": 257, "total_samples": 771, "all_nonzero_terminal_irreducible_sign_U_exact": True}, "literal referee")


def main():
    need(sha(ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin") == "93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3", "checkpoint hash")
    need(sha(ROOT / "computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/k23_expected_scalar_groups.json") == "6d59f1a24771e3a5e595ab79d8d0309881edea085da62c34b8e70cf93757c9ab", "schedule hash")
    for filename, digest in PINS.items():
        need(sha(HERE / filename) == digest, f"hash pin {filename}")
    fragment = json.loads((HERE / "results_k23_direct_k16_18.json").read_text())
    manifest = json.loads((HERE / "k23_direct_k16_18_fragment_manifest.json").read_text())
    if len(sys.argv) == 3 and sys.argv[1] == "--hostile":
        hostile = sys.argv[2]
        f2, m2 = deepcopy(fragment), deepcopy(manifest)
        if hostile == "missing":
            m2["groups"].pop()
        elif hostile == "duplicate":
            m2["groups"][1]["ids"][0] = m2["groups"][0]["ids"][0]
        elif hostile == "extra":
            m2["groups"][0]["ids"].append("D16:999|R:3-4")
        elif hostile == "scaled":
            m2["groups"][0]["full_scaled_U"] = str(int(m2["groups"][0]["full_scaled_U"]) + 1)
        else:
            raise SystemExit("unknown hostile mode")
        try:
            audit(f2, m2)
        except Reject as exc:
            print(json.dumps({"status": "PASS_HOSTILE_REJECTED", "mode": hostile, "reason": str(exc)}, sort_keys=True))
            return
        raise SystemExit("hostile mutation was accepted")
    need(len(sys.argv) == 1, "arguments")
    audit(fragment, manifest)
    print(json.dumps({"status": "PASS_K23_DIRECT_K16_18_PACKAGE", "covered_ids": 18, "scalar_groups": 3, "subtotal_scaled_U": str(TOTAL), "subtotal": str(Fraction(TOTAL, U)), "literal_samples": 771}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Reject as exc:
        raise SystemExit(f"REJECT: {exc}")

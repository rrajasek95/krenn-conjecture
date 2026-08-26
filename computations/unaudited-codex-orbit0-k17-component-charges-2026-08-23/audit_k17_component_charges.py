#!/usr/bin/env python3
"""Small exact replay guard for the charge-only K17 component result."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULT = HERE / "results_k17_component_charges.json"
INTERFACE = HERE / "k17_charge_interface.bin"
FROZEN = (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23"
          / "results_filtered_k17_checkpoint_audit.json")
K15 = (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23"
       / "checkpoint_direct_k15.bin")


def main():
    r = json.loads(RESULT.read_text())
    if "--mutate" in sys.argv:
        r["A_K14_K3"]["irreducible"] = "-323083775/1"
    frozen = json.loads(FROZEN.read_text())["components"]
    assert r["status"] == "EXACT_K17_COMPONENT_CHARGES"
    assert sha256(INTERFACE.read_bytes()).hexdigest() == "ffc668375c1d33cfc4b2b41e48686df13cca19b6e4802046850e685dacf63556"
    assert sha256(K15.read_bytes()).hexdigest() == "e79b752f94ad3b16ce4cf7d3f044e8887bda54bba5c6298ab31338bb121fa20f"
    a = Fraction(r["A_K14_K3"]["irreducible"])
    b = Fraction(r["B_K15_K2"]["irreducible"])
    assert a == Fraction(frozen["from_K14_K3"]["cycle_pairing"])
    assert b == Fraction(frozen["from_K15_K2"]["cycle_pairing"])
    assert Fraction(r["A_K14_K3"]["full"]) - a == Fraction(r["A_K14_K3"]["pivotable"])
    assert Fraction(r["B_K15_K2"]["full"]) - b == Fraction(r["B_K15_K2"]["pivotable"])
    total = Fraction(-62_386_176) + a + b
    assert total == Fraction(r["sum_with_direct"]["using_irreducible_A_B"])
    assert total == Fraction(frozen["combined"]["cycle_pairing"])
    assert r["A_K14_K3"]["pivot_uses"] == 6_619_280
    assert r["A_K14_K3"]["tail_occurrences"] == 211_816_960
    assert r["B_K15_K2"]["checkpoint_rows"] == 5_311_211
    assert r["B_K15_K2"]["tail_occurrences"] == 532_114_572
    logical = {k: v for k, v in r.items() if k != "elapsed_seconds"}
    digest = sha256(json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    print(json.dumps({"status": "PASS", "logical_sha256": digest}, sort_keys=True))


if __name__ == "__main__":
    main()

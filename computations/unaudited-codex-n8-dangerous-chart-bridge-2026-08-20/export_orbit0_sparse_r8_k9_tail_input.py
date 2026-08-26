#!/usr/bin/env python3
"""Serialize the full-column K9 tail of the sparse cutoff-nine solution."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
T2_PATH = HERE / "audit_orbit0_t2_pivot_setup.py"
SPEC = importlib.util.spec_from_file_location("tail_t2", T2_PATH)
T2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(T2)
CERT = HERE / "results_orbit0_cutoff9_sparse_r8.json"
TARGET_SEED = HERE / "orbit0_cutoff10_seed.txt"
OUT = HERE / "orbit0_sparse_r8_k9_tail_input.txt"


def main() -> None:
    cert = json.loads(CERT.read_text())
    lines = [
        "KRENN_ORBIT0_SPARSE_R8_K9_TAIL_V1",
        "ANCHORS " + bytes(sorted(T2.ANCHORS)).hex(),
    ]
    action_count = 0
    target_count = 0
    target_mass = Fraction()
    for line in TARGET_SEED.read_text().splitlines():
        fields = line.split()
        if fields and fields[0] == "ACTION":
            lines.append(line)
            action_count += 1
        elif fields and fields[0] == "TARGET":
            row = bytes.fromhex(fields[1])
            if T2.row_k_degree(row) == 9:
                value = Fraction(int(fields[2]), int(fields[3]))
                assert value.denominator == 1
                lines.append(f"TARGET {fields[1]} {value.numerator}")
                target_count += 1
                target_mass += value
    assert action_count == 2304
    assert target_count == 103 and target_mass == 171_008

    source_count = 0
    for term in cert["terms"]:
        coefficient = Fraction(*term["coefficient"])
        assert coefficient.denominator == 1
        multiplier = bytes(term["multiplier_cell_ids"])
        assert len(multiplier) == 8
        lines.append("SOURCE %d %s %s" % (
            coefficient.numerator, term["word"], multiplier.hex()
        ))
        source_count += 1
    assert source_count == cert["full_source_terms"] == 9607
    payload = "\n".join(lines) + "\n"
    OUT.write_text(payload)
    print("actions/target/source:", action_count, target_count, source_count)
    print("target mass:", target_mass)
    print("bytes:", len(payload))
    print("sha256:", sha256(payload.encode("ascii")).hexdigest())
    print("path:", OUT)


if __name__ == "__main__":
    main()
